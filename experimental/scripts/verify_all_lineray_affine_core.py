#!/usr/bin/env python3
"""Verify the finite content of the all-LineRay affine-core packet.

The checker is deterministic, uses only the Python standard library, and
does not use ``assert`` so that ``python -O`` runs the same checks.  It
validates complete small-field pair families, both exact set-pair charges,
the sharp same-slope and split-hierarchy families, and the two conditional
finite calibrations.

Usage:
  python3 experimental/scripts/verify_all_lineray_affine_core.py --summary-only
  python3 experimental/scripts/verify_all_lineray_affine_core.py --check
  python3 experimental/scripts/verify_all_lineray_affine_core.py --tamper-selftest
"""

import argparse
import copy
import json
import math
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/all-lineray-affine-core"
    / "all_lineray_affine_core.json"
)

TWO_LEVEL_FORMULA = "sum 1/(selector_binom*fiber_binom) <= 1"

SHARP_PRIMES = (2, 3, 5, 7)
SWEEP_PRIMES = (2, 3)
FINITE_ROWS = (
    {
        "name": "KoalaBear",
        "n": 2_097_152,
        "m": 1_116_046,
        "s": 1,
        "stripped_first_interior_floor": 65_065_153_468,
    },
    {
        "name": "Mersenne-31",
        "n": 2_097_152,
        "m": 1_116_022,
        "s": 1,
        "stripped_first_interior_floor": 1_993_678,
    },
)
EXPECTED_CERTIFICATE_KEYS = {
    "schema",
    "status",
    "lean_status",
    "hard_input",
    "theorem",
    "formula",
    "two_level_formula",
    "sources",
    "computed_summary",
    "nonclaims",
}
EXPECTED_SOURCES = {
    "base": "fe93bb5",
    "selected_witness_predecessor": 681,
    "all_pair_target": 715,
    "lineray_identity": 721,
}


class VerificationError(RuntimeError):
    """A fail-closed packet check failed."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def add(first, second, modulus):
    require(len(first) == len(second), "vector length mismatch")
    return tuple((x + y) % modulus for x, y in zip(first, second))


def subtract(first, second, modulus):
    require(len(first) == len(second), "vector length mismatch")
    return tuple((x - y) % modulus for x, y in zip(first, second))


def scale(scalar, vector, modulus):
    return tuple((scalar * value) % modulus for value in vector)


def linear_combination(coefficients, vectors, modulus, length):
    require(len(coefficients) == len(vectors), "coefficient count mismatch")
    result = [0] * length
    for coefficient, vector in zip(coefficients, vectors):
        require(len(vector) == length, "combination vector length mismatch")
        for index, value in enumerate(vector):
            result[index] = (result[index] + coefficient * value) % modulus
    return tuple(result)


def weight(vector):
    return sum(value != 0 for value in vector)


def support(vector):
    return frozenset(index for index, value in enumerate(vector) if value != 0)


def rref(matrix, modulus, width=None):
    if not matrix:
        require(width is not None, "empty matrix needs a width")
        return [], []
    work = [list(row) for row in matrix]
    column_count = len(work[0])
    require(all(len(row) == column_count for row in work), "ragged matrix")
    pivots = []
    active = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(active, len(work))
                if work[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        work[active], work[pivot] = work[pivot], work[active]
        inverse = pow(work[active][column] % modulus, -1, modulus)
        work[active] = [value * inverse % modulus for value in work[active]]
        for row in range(len(work)):
            if row == active:
                continue
            factor = work[row][column] % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[active])
                ]
        pivots.append(column)
        active += 1
        if active == len(work):
            break
    return work, pivots


def matrix_rank(matrix, modulus, width=None):
    return len(rref(matrix, modulus, width=width)[1])


def determinant(matrix, modulus):
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant is not square")
    if size == 0:
        return 1
    work = [list(row) for row in matrix]
    value = 1
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        pivot_value = work[column][column] % modulus
        value = value * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % modulus
            for later in range(column, size):
                work[row][later] = (
                    work[row][later] - factor * work[column][later]
                ) % modulus
    return value % modulus


def solve_square(matrix, target, modulus):
    size = len(matrix)
    require(len(target) == size, "linear-system target length mismatch")
    require(all(len(row) == size for row in matrix), "linear system not square")
    if size == 0:
        return ()
    augmented = [
        [value % modulus for value in row] + [rhs % modulus]
        for row, rhs in zip(matrix, target)
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if augmented[row][column] % modulus
            ),
            None,
        )
        require(pivot is not None, "singular reconstruction minor")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse = pow(augmented[column][column] % modulus, -1, modulus)
        augmented[column] = [
            value * inverse % modulus for value in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column] % modulus
            if factor:
                augmented[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return tuple(augmented[row][-1] % modulus for row in range(size))


def mat_vec(matrix, vector, modulus):
    require(all(len(row) == len(vector) for row in matrix), "matrix/vector mismatch")
    return tuple(
        sum(entry * value for entry, value in zip(row, vector)) % modulus
        for row in matrix
    )


def nullspace_basis(matrix, modulus, width):
    if not matrix:
        return [
            tuple(1 if index == free else 0 for index in range(width))
            for free in range(width)
        ]
    reduced, pivots = rref(matrix, modulus)
    require(len(matrix[0]) == width, "nullspace width mismatch")
    free_columns = [column for column in range(width) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free]) % modulus
        basis.append(tuple(vector))
    return basis


def kernel_distance(matrix, modulus, width):
    basis = nullspace_basis(matrix, modulus, width)
    if not basis:
        return width + 1
    require(
        modulus ** len(basis) <= 100_000,
        "kernel too large for this exhaustive certificate",
    )
    best = width + 1
    for coefficients in product(range(modulus), repeat=len(basis)):
        if all(coefficient == 0 for coefficient in coefficients):
            continue
        vector = linear_combination(coefficients, basis, modulus, width)
        best = min(best, weight(vector))
    return best


def independent_basis(vectors, modulus, width):
    basis = []
    rank = 0
    for vector in vectors:
        require(len(vector) == width, "basis candidate length mismatch")
        candidate_rank = matrix_rank(basis + [vector], modulus, width=width)
        if candidate_rank > rank:
            basis.append(vector)
            rank = candidate_rank
    return basis


def in_span(vector, generators, modulus):
    if not generators:
        return all(value % modulus == 0 for value in vector)
    width = len(vector)
    require(all(len(item) == width for item in generators), "span width mismatch")
    return matrix_rank(generators + [vector], modulus) == matrix_rank(
        generators, modulus
    )


def support_image_columns(matrix, indices):
    if not matrix:
        return []
    return [tuple(row[index] for row in matrix) for index in sorted(indices)]


def affine_basis(errors, modulus):
    require(errors, "affine basis needs a nonempty family")
    base = errors[0]
    differences = [subtract(error, base, modulus) for error in errors[1:]]
    return base, independent_basis(differences, modulus, len(base))


def verify_pair_family(modulus, matrix, y0, y1, pairs, t, label):
    require(pairs, label + ": family is empty")
    require(modulus > 1, label + ": bad modulus")
    ambient = len(pairs[0][1])
    target = len(matrix)
    require(target == len(y0) == len(y1), label + ": target dimension mismatch")
    require(all(len(row) == ambient for row in matrix), label + ": ambient mismatch")
    require(any(value % modulus for value in y1), label + ": y1 is zero")
    require(
        len({(gamma, tuple(error)) for gamma, error in pairs}) == len(pairs),
        label + ": duplicate pair",
    )
    distance = kernel_distance(matrix, modulus, ambient)
    require(distance > t, label + ": kernel distance hypothesis fails")

    errors = []
    for gamma, error in pairs:
        require(len(error) == ambient, label + ": inconsistent error length")
        expected = add(y0, scale(gamma, y1, modulus), modulus)
        require(mat_vec(matrix, error, modulus) == expected, label + ": bad syndrome")
        require(weight(error) <= t, label + ": error exceeds t")
        image = support_image_columns(matrix, support(error))
        transverse = not (
            in_span(y0, image, modulus) and in_span(y1, image, modulus)
        )
        require(transverse, label + ": transversality fails")
        errors.append(tuple(error))

    base, basis = affine_basis(errors, modulus)
    dimension = len(basis)
    minors = []
    supports = [support(error) for error in errors]
    reconstructed = 0
    for pair_index, error in enumerate(errors):
        zero_mask = tuple(index for index in range(ambient) if error[index] == 0)
        restriction = [
            [basis[column][index] for column in range(dimension)]
            for index in zero_mask
        ]
        require(
            matrix_rank(restriction, modulus, width=dimension) == dimension,
            label + ": zero-mask restriction is not injective",
        )
        chosen = None
        for indices in combinations(zero_mask, dimension):
            square = [
                [basis[column][index] for column in range(dimension)]
                for index in indices
            ]
            if determinant(square, modulus):
                chosen = tuple(indices)
                break
        require(chosen is not None, label + ": no invertible zero minor")
        square = [
            [basis[column][index] for column in range(dimension)]
            for index in chosen
        ]
        rhs = tuple((-base[index]) % modulus for index in chosen)
        coefficients = solve_square(square, rhs, modulus)
        recovered = add(
            base,
            linear_combination(coefficients, basis, modulus, ambient),
            modulus,
        )
        require(recovered == error, label + ": canonical minor did not recover error")
        minors.append(chosen)
        reconstructed += 1

    crossings = 0
    for first in range(len(pairs)):
        for second in range(len(pairs)):
            if first == second:
                continue
            require(
                set(minors[first]) & supports[second],
                label + ": ordered cross-intersection fails",
            )
            crossings += 1

    charge = sum(
        (Fraction(1, math.comb(dimension + weight(error), dimension)) for error in errors),
        Fraction(0, 1),
    )
    require(charge <= 1, label + ": nonuniform Bollobas charge exceeds one")
    maximum_weight = max(weight(error) for error in errors)
    first_bound = math.comb(dimension + maximum_weight, dimension)
    second_bound = math.comb(ambient, dimension)
    require(len(pairs) <= first_bound, label + ": first binomial bound fails")
    require(first_bound <= second_bound, label + ": ambient binomial bound fails")
    require(
        dimension + maximum_weight <= ambient,
        label + ": dimension/weight zero-mask bound fails",
    )
    return {
        "pairs": len(pairs),
        "dimension": dimension,
        "max_weight": maximum_weight,
        "charge": str(charge),
        "minors": reconstructed,
        "ordered_crossings": crossings,
        "distance": distance,
    }


def verify_two_level_charge(modulus, pairs, label):
    require(pairs, label + ": two-level family is empty")
    errors = [error for _, error in pairs]
    _, global_basis = affine_basis(errors, modulus)
    slopes = sorted({gamma for gamma, _ in pairs})
    representatives = [
        next(pair for pair in pairs if pair[0] == gamma) for gamma in slopes
    ]
    representative_errors = [error for _, error in representatives]
    _, representative_basis = affine_basis(representative_errors, modulus)
    representative_dimension = len(representative_basis)
    representative_weight = max(weight(error) for error in representative_errors)
    outer_charge = sum(
        (
            Fraction(
                1,
                math.comb(
                    representative_dimension + weight(error),
                    representative_dimension,
                ),
            )
            for error in representative_errors
        ),
        Fraction(0, 1),
    )
    require(outer_charge <= 1, label + ": representative charge exceeds one")

    nested_charge = Fraction(0, 1)
    fiber_caps = []
    fiber_dimensions = []
    local_equalities = 0
    for gamma, representative_error in representatives:
        fiber_errors = [
            error for slope, error in pairs if slope == gamma
        ]
        _, fiber_basis = affine_basis(fiber_errors, modulus)
        fiber_dimension = len(fiber_basis)
        fiber_weight = max(weight(error) for error in fiber_errors)
        local_charge = sum(
            (
                Fraction(
                    1,
                    math.comb(fiber_dimension + weight(error), fiber_dimension),
                )
                for error in fiber_errors
            ),
            Fraction(0, 1),
        )
        require(local_charge <= 1, label + ": local fiber charge exceeds one")
        local_equalities += int(local_charge == 1)
        outer_factor = Fraction(
            1,
            math.comb(
                representative_dimension + weight(representative_error),
                representative_dimension,
            ),
        )
        nested_charge += outer_factor * local_charge
        fiber_caps.append(math.comb(fiber_dimension + fiber_weight, fiber_dimension))
        fiber_dimensions.append(fiber_dimension)

    require(nested_charge <= 1, label + ": nested two-level charge exceeds one")
    outer_cap = math.comb(
        representative_dimension + representative_weight,
        representative_dimension,

    )
    product_bound = outer_cap * max(fiber_caps)
    require(len(pairs) <= product_bound, label + ": two-level product bound fails")
    global_dimension = len(global_basis)
    global_weight = max(weight(error) for error in errors)
    base_bound = math.comb(global_dimension + global_weight, global_dimension)
    return {
        "representative_dimension": representative_dimension,
        "max_fiber_dimension": max(fiber_dimensions),
        "nested_charge": str(nested_charge),
        "outer_charge": str(outer_charge),
        "local_equalities": local_equalities,
        "product_bound": product_bound,
        "base_bound": base_bound,
        "strict_bound_improvement": product_bound < base_bound,
        "rank_separation": global_dimension
        > representative_dimension + max(fiber_dimensions),
    }


def accumulate_two_level(counters, metrics):
    counters["two_level_families"] += 1
    counters["two_level_charge_equalities"] += int(metrics["nested_charge"] == "1")
    counters["two_level_bound_improvements"] += int(
        metrics["strict_bound_improvement"]
    )
    counters["two_level_rank_separations"] += int(metrics["rank_separation"])


def sharp_family(modulus):
    ambient = modulus + 1
    matrix = []
    for finite_coordinate in range(1, modulus):
        row = [0] * ambient
        row[0] = -1 % modulus
        row[finite_coordinate] = 1
        matrix.append(tuple(row))
    infinity_row = [0] * ambient
    infinity_row[-1] = 1
    matrix.append(tuple(infinity_row))
    errors = [
        tuple((a + coordinate) % modulus for coordinate in range(modulus)) + (0,)
        for a in range(modulus)
    ]
    y0 = mat_vec(matrix, errors[0], modulus)
    y1 = tuple(0 for _ in range(modulus - 1)) + (1,)
    pairs = [(0, error) for error in errors]
    return matrix, y0, y1, pairs, modulus - 1


def verify_split_hierarchy_families():
    rows = []
    for modulus in SHARP_PRIMES:
        base_matrix, base_y0, _, base_pairs, t = sharp_family(modulus)
        block_length = modulus + 1
        zero_block = tuple(0 for _ in range(block_length))
        zero_target = tuple(0 for _ in range(modulus))
        matrix = [
            tuple(row) + zero_block for row in base_matrix
        ] + [
            zero_block + tuple(row) for row in base_matrix
        ]
        y0 = tuple(base_y0) + zero_target
        y1 = scale(-1, base_y0, modulus) + tuple(base_y0)
        pairs = [
            (0, tuple(error) + zero_block) for _, error in base_pairs
        ] + [
            (1, zero_block + tuple(error)) for _, error in base_pairs
        ]
        metrics = verify_pair_family(
            modulus,
            matrix,
            y0,
            y1,
            pairs,
            t,
            "split-hierarchy-F" + str(modulus),
        )
        hierarchy = verify_two_level_charge(
            modulus, pairs, "split-two-level-F" + str(modulus)
        )
        require(metrics["dimension"] == 3, "split family global rank changed")
        require(
            hierarchy["representative_dimension"] == 1,
            "split family representative rank changed",
        )
        require(
            hierarchy["max_fiber_dimension"] == 1,
            "split family local rank changed",
        )
        require(hierarchy["rank_separation"], "split family lost rank separation")
        require(
            hierarchy["strict_bound_improvement"] == (modulus >= 3),
            "split family product/base comparison changed",
        )
        rows.append(
            {
                "field": modulus,
                "pairs": len(pairs),
                "global_dimension": metrics["dimension"],
                "representative_dimension": hierarchy["representative_dimension"],
                "max_fiber_dimension": hierarchy["max_fiber_dimension"],
                "nested_charge": hierarchy["nested_charge"],
                "two_level_product_bound": hierarchy["product_bound"],
                "global_rank_bound": hierarchy["base_bound"],
                "strict_improvement": hierarchy["strict_bound_improvement"],
            }
        )
    return rows


def verify_sharp_families():
    rows = []
    for modulus in SHARP_PRIMES:
        matrix, y0, y1, pairs, t = sharp_family(modulus)
        metrics = verify_pair_family(
            modulus, matrix, y0, y1, pairs, t, "sharp-F" + str(modulus)
        )
        require(metrics["dimension"] == 1, "sharp family has wrong dimension")
        require(metrics["max_weight"] == modulus - 1, "sharp family has wrong weight")
        require(metrics["pairs"] == modulus, "sharp family has wrong pair count")
        require(metrics["charge"] == "1", "sharp family does not attain equality")
        hierarchy = verify_two_level_charge(
            modulus, pairs, "sharp-two-level-F" + str(modulus)
        )
        require(hierarchy["representative_dimension"] == 0, "sharp outer rank changed")
        require(hierarchy["max_fiber_dimension"] == 1, "sharp fiber rank changed")
        require(hierarchy["nested_charge"] == "1", "sharp nested charge is not exact")

        u = pairs[0][1]
        v = tuple(0 for _ in range(modulus)) + (1,)
        codewords = []
        for _, error in pairs:
            codeword = subtract(u, error, modulus)
            require(
                mat_vec(matrix, codeword, modulus) == tuple(0 for _ in y0),
                "sharp LineRay codeword is not in the kernel",
            )
            recovered_error = subtract(add(u, scale(0, v, modulus), modulus), codeword, modulus)
            require(recovered_error == error, "sharp LineRay realization changed the error")
            require(
                len(error) - weight(error) == 2,
                "sharp LineRay agreement is not exactly two",
            )
            codewords.append(codeword)
        require(len(set(codewords)) == modulus, "sharp LineRay codewords are not distinct")
        kernel_basis = nullspace_basis(matrix, modulus, len(u))
        kernel_words = {
            linear_combination(coefficients, kernel_basis, modulus, len(u))
            for coefficients in product(
                range(modulus), repeat=len(kernel_basis)
            )
        }
        require(
            set(codewords) == kernel_words,
            "sharp family does not exhaust the threshold-two rays at slope zero",
        )
        common_two_supports = 0
        for coordinates in combinations(range(len(u)), 2):
            u_agrees = any(
                all(u[index] == codeword[index] for index in coordinates)
                for codeword in kernel_words
            )
            v_agrees = any(
                all(v[index] == codeword[index] for index in coordinates)
                for codeword in kernel_words
            )
            common_two_supports += int(u_agrees and v_agrees)
        require(common_two_supports == 0, "sharp family has a common two-support")
        rows.append(
            {
                "field": modulus,
                "pairs": metrics["pairs"],
                "affine_dimension": metrics["dimension"],
                "weight": metrics["max_weight"],
                "charge": metrics["charge"],
                "agreement": 2,
                "all_threshold_two_rays": True,
                "common_two_supports": common_two_supports,
                "representative_dimension": hierarchy["representative_dimension"],
                "max_fiber_dimension": hierarchy["max_fiber_dimension"],
                "nested_charge": hierarchy["nested_charge"],
                "two_level_product_bound": hierarchy["product_bound"],
            }
        )
    return rows


def all_vectors(modulus, length):
    return [tuple(values) for values in product(range(modulus), repeat=length)]


def verify_small_sweeps():
    counters = {
        "parameter_rows": 0,
        "nonempty_complete_families": 0,
        "complete_pairs": 0,
        "deletion_families": 0,
        "slope_slice_families": 0,
        "verified_pairs": 0,
        "verified_minors": 0,
        "ordered_crossings": 0,
        "two_level_families": 0,
        "two_level_charge_equalities": 0,
        "two_level_bound_improvements": 0,
        "two_level_rank_separations": 0,
    }
    per_field = []
    for modulus in SWEEP_PRIMES:
        matrix, _, _, _, _ = sharp_family(modulus)
        ambient = modulus + 1
        target = modulus
        vectors = all_vectors(modulus, ambient)
        target_vectors = all_vectors(modulus, target)
        syndromes = {vector: mat_vec(matrix, vector, modulus) for vector in vectors}
        distance = kernel_distance(matrix, modulus, ambient)
        field_start = dict(counters)
        for y0 in target_vectors:
            for y1 in target_vectors:
                if not any(y1):
                    continue
                for t in range(distance):
                    counters["parameter_rows"] += 1
                    pairs = []
                    for gamma in range(modulus):
                        wanted = add(y0, scale(gamma, y1, modulus), modulus)
                        for error in vectors:
                            if weight(error) > t or syndromes[error] != wanted:
                                continue
                            image = support_image_columns(matrix, support(error))
                            if in_span(y0, image, modulus) and in_span(
                                y1, image, modulus
                            ):
                                continue
                            pairs.append((gamma, error))
                    if not pairs:
                        continue
                    metrics = verify_pair_family(
                        modulus,
                        matrix,
                        y0,
                        y1,
                        pairs,
                        t,
                        "sweep-F{}-row{}".format(
                            modulus, counters["parameter_rows"]
                        ),
                    )
                    hierarchy = verify_two_level_charge(
                        modulus,
                        pairs,
                        "sweep-two-level-F{}-row{}".format(
                            modulus, counters["parameter_rows"]
                        ),
                    )
                    accumulate_two_level(counters, hierarchy)
                    counters["nonempty_complete_families"] += 1
                    counters["complete_pairs"] += len(pairs)
                    counters["verified_pairs"] += metrics["pairs"]
                    counters["verified_minors"] += metrics["minors"]
                    counters["ordered_crossings"] += metrics["ordered_crossings"]

                    if len(pairs) > 1:
                        deletion = pairs[::2]
                        deletion_metrics = verify_pair_family(
                            modulus,
                            matrix,
                            y0,
                            y1,
                            deletion,
                            t,
                            "sweep-deletion-F{}-row{}".format(
                                modulus, counters["parameter_rows"]
                            ),
                        )
                        counters["deletion_families"] += 1
                        deletion_hierarchy = verify_two_level_charge(
                            modulus,
                            deletion,
                            "sweep-two-level-deletion-F{}-row{}".format(
                                modulus, counters["parameter_rows"]
                            ),
                        )
                        accumulate_two_level(counters, deletion_hierarchy)
                        counters["verified_pairs"] += deletion_metrics["pairs"]
                        counters["verified_minors"] += deletion_metrics["minors"]
                        counters["ordered_crossings"] += deletion_metrics[
                            "ordered_crossings"
                        ]

                    slopes = sorted({gamma for gamma, _ in pairs})
                    for gamma in slopes:
                        slope_slice = [pair for pair in pairs if pair[0] == gamma]
                        if len(slope_slice) <= 1:
                            continue
                        slice_metrics = verify_pair_family(
                            modulus,
                            matrix,
                            y0,
                            y1,
                            slope_slice,
                            t,
                            "sweep-slope-F{}-row{}-gamma{}".format(
                                modulus, counters["parameter_rows"], gamma
                            ),
                        )
                        counters["slope_slice_families"] += 1
                        slice_hierarchy = verify_two_level_charge(
                            modulus,
                            slope_slice,
                            "sweep-two-level-slope-F{}-row{}-gamma{}".format(
                                modulus, counters["parameter_rows"], gamma
                            ),
                        )
                        accumulate_two_level(counters, slice_hierarchy)
                        counters["verified_pairs"] += slice_metrics["pairs"]
                        counters["verified_minors"] += slice_metrics["minors"]
                        counters["ordered_crossings"] += slice_metrics[
                            "ordered_crossings"
                        ]
        per_field.append(
            {
                "field": modulus,
                **{
                    key: counters[key] - field_start[key]
                    for key in counters
                },
            }
        )
    return {"totals": counters, "by_field": per_field}


def verify_finite_rows():
    rows = []
    for source in FINITE_ROWS:
        row = dict(source)
        residual_weight = row["n"] - row["m"]
        bound = math.comb(row["s"] + residual_weight, row["s"])
        require(
            bound < row["stripped_first_interior_floor"],
            row["name"] + ": conditional bound does not pay floor",
        )
        row["residual_weight"] = residual_weight
        row["lineray_bound"] = bound
        row["conditional_on_affine_dimension"] = row["s"]
        row["conditional_branch_paid"] = True
        row["deployed_residual_dimension_certified"] = False
        rows.append(row)
    require(rows[0]["lineray_bound"] == 981_107, "KoalaBear calibration changed")
    require(rows[1]["lineray_bound"] == 981_131, "Mersenne-31 calibration changed")
    return rows


def compute_summary():
    return {
        "schema": 1,
        "theorem": "all-LineRay affine-core set-pair",
        "formula": "sum 1/binom(s+wt(e),s) <= 1",
        "two_level_formula": TWO_LEVEL_FORMULA,
        "sharp_families": verify_sharp_families(),
        "split_hierarchy_families": verify_split_hierarchy_families(),
        "small_sweeps": verify_small_sweeps(),
        "finite_rows": verify_finite_rows(),
    }


def reject_json_constant(value):
    raise VerificationError("nonstandard JSON constant: " + value)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_certificate_text(text):
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_json_constant,
        )
    except json.JSONDecodeError as error:
        raise VerificationError("invalid certificate JSON: " + str(error)) from error


def strict_equal(first, second):
    if type(first) is not type(second):
        return False
    if isinstance(first, dict):
        return first.keys() == second.keys() and all(
            strict_equal(first[key], second[key]) for key in first
        )
    if isinstance(first, list):
        return len(first) == len(second) and all(
            strict_equal(left, right) for left, right in zip(first, second)
        )
    return first == second


def load_certificate():
    require(CERTIFICATE.is_file(), "certificate file is missing")
    try:
        text = CERTIFICATE.read_text(encoding="utf-8")
    except OSError as error:
        raise VerificationError("cannot read certificate: " + str(error)) from error
    return parse_certificate_text(text)


def validate_certificate(certificate, summary):
    require(type(certificate) is dict, "certificate root is not an object")
    require(
        certificate.keys() == EXPECTED_CERTIFICATE_KEYS,
        "certificate top-level keys mismatch",
    )
    require(type(certificate["schema"]) is int, "certificate schema type mismatch")
    require(certificate["schema"] == 1, "certificate schema mismatch")
    require(type(certificate["status"]) is str, "certificate status type mismatch")
    require(certificate["status"] == "PROVED", "certificate status mismatch")
    require(
        type(certificate["lean_status"]) is str
        and certificate["lean_status"] == "UNPROVED STATEMENT TARGET",
        "certificate Lean status mismatch",
    )
    require(
        type(certificate["hard_input"]) is int and certificate["hard_input"] == 3,
        "certificate route mismatch",
    )
    require(
        type(certificate["theorem"]) is str
        and certificate["theorem"] == summary["theorem"],
        "certificate theorem mismatch",
    )
    require(
        type(certificate["formula"]) is str
        and certificate["formula"] == summary["formula"],
        "certificate formula mismatch",
    )
    require(
        type(certificate["two_level_formula"]) is str
        and certificate["two_level_formula"] == TWO_LEVEL_FORMULA,
        "certificate two-level formula mismatch",
    )
    require(
        strict_equal(certificate["sources"], EXPECTED_SOURCES),
        "certificate sources mismatch",
    )
    require(
        strict_equal(certificate["computed_summary"], summary),
        "certificate computed summary mismatch",
    )
    require(
        strict_equal(
            certificate["nonclaims"],
            [
                "no general payment for a linear-rank same-slope affine list",
                "no theorem forcing sublinear selector and local ranks",
                "no raw-LineRay transversality before common-support removal",
                "no deployed residual affine-dimension certificate",
                "no general rational-host extraction",
                "no Grand MCA/List theorem or prize threshold",
            ],
        ),
        "certificate nonclaims mismatch",
    )


def tamper_selftest(summary):
    certificate = load_certificate()
    validate_certificate(certificate, summary)
    mutations = []

    changed = copy.deepcopy(certificate)
    changed["status"] = "CONDITIONAL"
    mutations.append(("status", changed))

    changed = copy.deepcopy(certificate)
    changed["formula"] = "sum <= 2"
    mutations.append(("formula", changed))

    changed = copy.deepcopy(certificate)
    changed["two_level_formula"] = "nested sum <= 2"
    mutations.append(("two-level-formula", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["sharp_families"][2]["pairs"] += 1
    mutations.append(("sharp-family-count", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["split_hierarchy_families"][2]["pairs"] += 1
    mutations.append(("split-hierarchy-count", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["small_sweeps"]["totals"]["verified_minors"] -= 1
    mutations.append(("sweep-minor-count", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["finite_rows"][0]["lineray_bound"] += 1
    mutations.append(("finite-bound", changed))

    changed = copy.deepcopy(certificate)
    changed["sources"]["base"] = "tampered"
    mutations.append(("source-pin", changed))

    changed = copy.deepcopy(certificate)
    changed["unexpected"] = "payload"
    mutations.append(("unknown-key", changed))

    changed = copy.deepcopy(certificate)
    changed["schema"] = True
    mutations.append(("schema-type-alias", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["finite_rows"][0][
        "conditional_branch_paid"
    ] = 1
    mutations.append(("boolean-type-alias", changed))

    changed = copy.deepcopy(certificate)
    changed["nonclaims"] = changed["nonclaims"][:-1]
    mutations.append(("nonclaim", changed))

    rejected = 0
    parser_tampers = [
        ("duplicate-key", '{"schema": 1, "schema": 1}'),
        ("nonstandard-constant", '{"value": NaN}'),
    ]
    for name, mutation in mutations:
        try:
            validate_certificate(mutation, summary)
        except VerificationError:
            rejected += 1
            continue
        raise VerificationError("tamper was accepted: " + name)
    for name, text in parser_tampers:
        try:
            parse_certificate_text(text)
        except VerificationError:
            rejected += 1
            continue
        raise VerificationError("parser tamper was accepted: " + name)
    tamper_cases = len(mutations) + len(parser_tampers)
    require(rejected == tamper_cases, "not every tamper was rejected")
    return {"tamper_cases": tamper_cases, "rejected": rejected}


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--summary-only", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    try:
        summary = compute_summary()
        if args.summary_only:
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        if args.check:
            validate_certificate(load_certificate(), summary)
            print(json.dumps({"status": "ok", "summary": summary}, sort_keys=True))
            return 0
        result = tamper_selftest(summary)
        print(json.dumps({"status": "ok", **result}, sort_keys=True))
        return 0
    except VerificationError as error:
        print("verification failed: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
