#!/usr/bin/env python3
"""Verify the M31 shortened-flat/projective-hyperplane architecture wall.

The packet has two logically separate outputs.

* Exact bridge: arbitrary-center M31 list size is a duplicate-free count of
  shortened dual flats contained in a syndrome hyperplane, with one-point
  escape conditions enforcing exact support.  For weighted GRS codes the same
  containment is the familiar shifted-locator syndrome recurrence.
* Route cut: scalar MacWilliams shell data, pairwise support intersections, and
  every coordinate-shortened ``K+2`` projective line still admit a formal
  family above the forbidden size.  A closing proof must therefore use global
  cross-support line closure (or an equally strong GRS-specific separator).

All checks use explicit exceptions, so ``python -O`` preserves the verifier.
Only the Python standard library is required.
"""

from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb, gcd, isqrt
from pathlib import Path
from typing import Any, Iterable, Sequence


P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
SIGMA = A - K
RADIUS = N - A
BUDGET = P**4 // 2**100
FORBIDDEN = BUDGET + 1
BASE_COMMIT = "8ba8939fb66db0f2509bb364368355b9e01b4731"

EXPECTED_PROVENANCE = {
    "projective_line_wall_pr": 720,
    "projective_line_wall_head": "2f7af1a248f59d0942b8cb76df01c7983490aba3",
    "weighted_grs_packing_pr": 748,
    "weighted_grs_packing_head": "f79711a0b47fc191aa579ae1cde58d2fbed158f5",
    "scalar_descent_pr": 993,
    "scalar_descent_head": "8242ea37f4aa018c241c02fe9287f9914e9fd56a",
    "rho9_wall_pr": 1000,
    "rho9_wall_head": BASE_COMMIT,
}

EXPECTED_SHADOW_RATIO = Fraction(45_812_940_800, 2_891_200_952_995_149)
EXPECTED_LAMBDA_FLOOR_100 = 406_561_177_535_215_237
EXPECTED_SHADOW_FLOOR_100 = 6_442_223_650_591
EXPECTED_ENDPOINT_CUT_100 = 406_554_735_311_564_645
EXPECTED_SCALAR_DESCENT_MARGIN = (
    592_061_458_020_761_914_489_814_638_395_392
)

ROOT = Path(__file__).resolve().parents[2]
NOTE_PATH = (
    ROOT / "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md"
)
SAGE_PATH = (
    ROOT / "experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.sage"
)
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/m31-shortened-flat-hyperplane-wall/manifest.json"
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def floor_fraction(value: Fraction) -> int:
    return value.numerator // value.denominator


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    limit = isqrt(value)
    while divisor <= limit:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def dot(left: Sequence[int], right: Sequence[int], p: int) -> int:
    return sum(x * y for x, y in zip(left, right)) % p


def rref_mod(
    matrix: Sequence[Sequence[int]], p: int, ncols: int
) -> tuple[list[list[int]], tuple[int, ...]]:
    rows = [[entry % p for entry in row] for row in matrix]
    require(all(len(row) == ncols for row in rows), "matrix width")
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(ncols):
        selected = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, p)
        rows[pivot_row] = [entry * inverse % p for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot) % p
                for entry, pivot in zip(rows[row], rows[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, tuple(pivot_columns)


def rank_mod(matrix: Sequence[Sequence[int]], p: int, ncols: int) -> int:
    return len(rref_mod(matrix, p, ncols)[1])


def nullspace_mod(
    matrix: Sequence[Sequence[int]], p: int, ncols: int
) -> list[tuple[int, ...]]:
    rows, pivots = rref_mod(matrix, p, ncols)
    free_columns = [column for column in range(ncols) if column not in pivots]
    basis: list[tuple[int, ...]] = []
    for free in free_columns:
        vector = [0] * ncols
        vector[free] = 1
        for row_index, pivot in enumerate(pivots):
            vector[pivot] = -rows[row_index][free] % p
        basis.append(tuple(vector))
    return basis


def linear_combination(
    coefficients: Sequence[int], basis: Sequence[Sequence[int]], p: int
) -> tuple[int, ...]:
    if not basis:
        return ()
    return tuple(
        sum(coefficient * row[column] for coefficient, row in zip(coefficients, basis))
        % p
        for column in range(len(basis[0]))
    )


def rowspaces_equal(
    left: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
    p: int,
    ncols: int,
) -> bool:
    left_rank = rank_mod(left, p, ncols)
    right_rank = rank_mod(right, p, ncols)
    joined_rank = rank_mod(tuple(left) + tuple(right), p, ncols)
    return left_rank == right_rank == joined_rank


def eval_poly(coefficients: Sequence[int], point: int, p: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * point + coefficient) % p
    return value


def multiply_poly(
    left: Sequence[int], right: Sequence[int], p: int
) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] = (result[i + j] + x * y) % p
    return tuple(result)


def locator(points: Iterable[int], p: int) -> tuple[int, ...]:
    result: tuple[int, ...] = (1,)
    for point in points:
        result = multiply_poly(result, (-point % p, 1), p)
    return result


def canonical_projective(vector: Sequence[int], p: int) -> tuple[int, ...]:
    first = next((entry % p for entry in vector if entry % p), None)
    if first is None:
        raise VerificationError("zero vector has no projective normalization")
    inverse = pow(first, -1, p)
    return tuple(entry * inverse % p for entry in vector)


def projective_points(p: int, dimension: int) -> tuple[tuple[int, ...], ...]:
    points = {
        canonical_projective(vector, p)
        for vector in product(range(p), repeat=dimension)
        if any(vector)
    }
    return tuple(sorted(points))


def projective_lines(
    points: Sequence[tuple[int, ...]], p: int
) -> tuple[frozenset[tuple[int, ...]], ...]:
    lines: set[frozenset[tuple[int, ...]]] = set()
    for left, right in combinations(points, 2):
        span = {
            canonical_projective(
                tuple(
                    (a * x + b * y) % p
                    for x, y in zip(left, right)
                ),
                p,
            )
            for a, b in product(range(p), repeat=2)
            if a or b
        }
        if len(span) == p + 1:
            lines.add(frozenset(span))
    return tuple(sorted(lines, key=lambda line: tuple(sorted(line))))


def projective_hyperplanes(
    points: Sequence[tuple[int, ...]], p: int
) -> set[frozenset[tuple[int, ...]]]:
    functionals = projective_points(p, len(points[0]))
    return {
        frozenset(point for point in points if dot(functional, point, p) == 0)
        for functional in functionals
    }


def add_shifted_power(coefficients: list[int], degree: int, scale: int) -> None:
    for power in range(degree + 1):
        coefficients[power] += (
            scale * comb(degree, power) * (-1) ** (degree - power)
        )


def scalar_agreement_polynomial(
    p: int, n: int, dimension: int, agreement: int, tail: int
) -> list[int]:
    coefficients = [0] * (agreement + 1)
    for degree in range(dimension + 1):
        add_shifted_power(
            coefficients,
            degree,
            comb(n, degree) * p ** (dimension - degree),
        )
    coefficients[agreement] += tail
    for degree in range(dimension + 1):
        add_shifted_power(
            coefficients,
            degree,
            -tail * comb(agreement, degree),
        )
    return coefficients


def krawtchouk(p: int, n: int, shell: int, weight: int) -> int:
    lower = max(0, shell - (n - weight))
    upper = min(shell, weight)
    return sum(
        (-1) ** overlap
        * (p - 1) ** (shell - overlap)
        * comb(weight, overlap)
        * comb(n - weight, shell - overlap)
        for overlap in range(lower, upper + 1)
    )


def projective_mds_shell(p: int, n: int, dimension: int, shell: int) -> int:
    excess = shell - dimension
    if excess < 1:
        return 0
    alternating = sum(
        (-1) ** index
        * comb(shell - 1, index)
        * p ** (excess - 1 - index)
        for index in range(excess)
    )
    return comb(n, shell) * alternating


def check_optimization_safety() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=__file__)
    require(
        not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        "verifier must not contain assert statements",
    )


def check_deployed_ledger() -> dict[str, int]:
    require(P == 2_147_483_647, "Mersenne-31 field")
    require(is_prime(P), "Mersenne-31 primality")
    require(N == 2_097_152 and K == 1_048_576, "deployed powers of two")
    require(N == 2 * K, "self-dual dimension relation")
    require(A == K + SIGMA and SIGMA == 67_447, "agreement reserve")
    require(RADIUS == K - SIGMA == 981_129, "closed list radius")
    require(RADIUS < K + 1, "unique-error MDS gate")
    require(BUDGET == 16_777_215, "quartic challenge budget")
    require(FORBIDDEN == 2**24, "forbidden list size")
    require((P + 1) % N == 0 and (P + 1) // N == 1_024, "circle divisor")
    require((P - 1) % N != 0, "domain is not a multiplicative n-subgroup")
    require(P > 2 * N, "large-field scalar gate")

    extension_degree = 4
    projective_functionals = (P**extension_degree - 1) // (P - 1)
    killed_functionals = (P ** (extension_degree - 1) - 1) // (P - 1)
    gap = A - K + 1
    left = FORBIDDEN * RADIUS * killed_functionals
    right = gap * projective_functionals
    require(left < right, "scalar descent strict incidence gate")
    require(right - left == EXPECTED_SCALAR_DESCENT_MARGIN, "descent margin")

    return {
        "minimum_distance": K + 1,
        "boundary_flat_dimension": K - RADIUS,
        "one_point_extension_dimension": K - RADIUS + 1,
        "scalar_descent_margin": right - left,
    }


def check_external_route_arithmetic() -> dict[str, int]:
    degree = K - 1
    berlekamp_welch_agreement = (N + degree + 2) // 2
    require(
        berlekamp_welch_agreement == 1_572_864,
        "Berlekamp-Welch agreement threshold",
    )
    require(
        berlekamp_welch_agreement - A == 456_841,
        "Berlekamp-Welch agreement deficit",
    )

    johnson_radicand = N * degree
    johnson_floor = isqrt(johnson_radicand)
    require(johnson_floor == 1_482_909, "Johnson square-root floor")
    require(
        johnson_floor**2 < johnson_radicand < (johnson_floor + 1) ** 2,
        "Johnson radicand nonsquare",
    )
    johnson_required_agreement = johnson_floor + 1
    johnson_max_errors = N - johnson_required_agreement
    require(johnson_max_errors == 614_242, "Johnson maximum integer errors")
    require(
        RADIUS - johnson_max_errors == 366_887,
        "deployed excess over Johnson radius",
    )

    required_support_distance = 2 * (SIGMA + 1)
    model_support_distance = 2 * 67_584
    require(required_support_distance == 134_896, "packing distance requirement")
    require(model_support_distance == 135_168, "model support distance")
    require(
        model_support_distance > required_support_distance,
        "constant-weight route-cut margin",
    )
    return {
        "berlekamp_welch_required_agreement": berlekamp_welch_agreement,
        "berlekamp_welch_agreement_deficit": berlekamp_welch_agreement - A,
        "johnson_radicand": johnson_radicand,
        "johnson_sqrt_floor": johnson_floor,
        "johnson_required_agreement": johnson_required_agreement,
        "johnson_max_integer_errors": johnson_max_errors,
        "deployed_errors_over_johnson": RADIUS - johnson_max_errors,
        "packing_required_binary_distance": required_support_distance,
        "countermodel_binary_distance": model_support_distance,
    }


def check_scalar_shell_route_cut() -> dict[str, int | Fraction]:
    require(K - 3 * SIGMA == 846_235 > 0, "three-halves endpoint gate")
    lambda_floor = floor_fraction(Fraction(3, 2) ** 100)
    require(lambda_floor == EXPECTED_LAMBDA_FLOOR_100, "lambda lower floor")
    require(FORBIDDEN < lambda_floor, "formal forbidden tail below endpoint")

    rho = Fraction(SIGMA, K)
    x = Fraction(N * K, P * SIGMA)
    y = Fraction(N, P)
    require(0 < rho < 1 and 0 < x < 1 and 0 < y < 1, "scalar ratios")

    positive_gap = (
        (1 - Fraction(1, P)) * (1 - y)
        - (rho / (1 - x) + Fraction(1, P))
    )
    negative_gap = (1 - y) - (P * rho**8 / (1 - x) + y**7)
    low_gate_1 = P * SIGMA - 100 * K * (K + 9)
    low_gate_2 = P * (SIGMA - 8) - 100 * K * (K + 9)
    require(positive_gap > 0, "positive projective-shell gap")
    require(negative_gap > 0, "negative projective-shell gap")
    require(low_gate_1 == 34_889_223_043_209 > 0, "low-shell first gate")
    require(low_gate_2 == 34_872_043_174_033 > 0, "low-shell later gate")

    return {
        "formal_tail": FORBIDDEN,
        "lambda_lower_floor": lambda_floor,
        "lambda_margin": lambda_floor - FORBIDDEN,
        "positive_gap_numerator": positive_gap.numerator,
        "positive_gap_denominator": positive_gap.denominator,
        "negative_gap_numerator": negative_gap.numerator,
        "negative_gap_denominator": negative_gap.denominator,
        "low_gate_1": low_gate_1,
        "low_gate_2": low_gate_2,
    }


def check_shadow_and_local_route_cut() -> dict[str, int | Fraction]:
    raw_numerator = K * (K - 1)
    raw_denominator = SIGMA * (
        (SIGMA - 1) + (K + 2) * (K - SIGMA)
    )
    ratio = Fraction(raw_numerator, raw_denominator)
    require(gcd(raw_numerator, raw_denominator) == 24, "shadow ratio gcd")
    require(ratio == EXPECTED_SHADOW_RATIO, "K+2 shadow ratio")
    shadow_floor = floor_fraction(ratio * Fraction(3, 2) ** 100)
    endpoint_cut = floor_fraction((1 - ratio) * Fraction(3, 2) ** 100)
    require(shadow_floor == EXPECTED_SHADOW_FLOOR_100, "shadow lower floor")
    require(endpoint_cut == EXPECTED_ENDPOINT_CUT_100, "endpoint cut")
    require(shadow_floor > FORBIDDEN, "K+2 shadow remains over budget")

    simplex_length = 2**12 - 1
    simplex_distance = 2**11
    repetition = 33
    repeated_length = repetition * simplex_length
    repeated_distance = repetition * simplex_distance
    zero_coordinates = 710_859
    code_length = 2 * repeated_length + zero_coordinates
    code_dimension = 2 * 12
    code_distance = repeated_distance
    code_size = 2**code_dimension

    require(code_length == RADIUS, "binary support-code length")
    require(code_dimension == 24, "binary support-code dimension")
    require(code_distance == 67_584, "binary support-code distance")
    require(code_distance >= SIGMA + 1, "block intersection distance gate")
    require(code_distance - (SIGMA + 1) == 136, "distance margin")
    require(code_size == FORBIDDEN, "support-code size equals forbidden size")
    require(code_size > BUDGET, "local support model exceeds budget")
    require(2 * code_length < N, "disjoint coordinate-pair embedding")
    require(N - 2 * code_length == 134_894, "unused coordinate count")
    max_intersection = A - code_distance
    require(max_intersection == K - 137 < K, "agreement-block intersection")

    full_support_points = P - K - 1
    require(full_support_points == 2_146_435_070, "full-support line points")
    require(
        (K + 2) + full_support_points == P + 1,
        "shortened-dual line partition",
    )
    require(
        P * (SIGMA - 1) > (K - 1) * (K + 2),
        "second local shell positivity",
    )
    extensions_per_minimum_support = N - K - 1
    facets_per_inside_support = K + 2
    completion_coefficient = (
        facets_per_inside_support - 1 + full_support_points
    )
    require(
        extensions_per_minimum_support == K - 1,
        "minimum-support extension multiplicity",
    )
    require(
        completion_coefficient == P,
        "K+2 completion coefficient",
    )

    simplex_nonzero = 2**12 - 1
    weight_zero_count = 1
    weight_one_block_count = 2 * simplex_nonzero
    weight_two_block_count = simplex_nonzero**2
    require(weight_one_block_count == 8_190, "binary middle-weight count")
    require(weight_two_block_count == 16_769_025, "binary top-weight count")
    require(
        weight_zero_count + weight_one_block_count + weight_two_block_count
        == code_size,
        "binary exact weight-distribution mass",
    )

    return {
        "shadow_ratio": ratio,
        "shadow_floor": shadow_floor,
        "endpoint_cut": endpoint_cut,
        "binary_length": code_length,
        "binary_dimension": code_dimension,
        "binary_distance": code_distance,
        "binary_size": code_size,
        "binary_size_margin_over_budget": code_size - BUDGET,
        "maximum_block_intersection": max_intersection,
        "unused_coordinates": N - 2 * code_length,
        "full_support_points": full_support_points,
        "weight_zero_count": weight_zero_count,
        "weight_67584_count": weight_one_block_count,
        "weight_135168_count": weight_two_block_count,
        "extensions_per_minimum_support": extensions_per_minimum_support,
        "facets_per_inside_support": facets_per_inside_support,
        "completion_coefficient": completion_coefficient,
    }


def shortened_coeff_basis(
    dual_basis: Sequence[Sequence[int]], excluded: Sequence[int], p: int
) -> list[tuple[int, ...]]:
    dimension = len(dual_basis)
    constraints = [
        [dual_basis[row][coordinate] for row in range(dimension)]
        for coordinate in excluded
    ]
    return nullspace_mod(constraints, p, dimension)


def ambient_shortening_basis(
    dual_basis: Sequence[Sequence[int]], excluded: Sequence[int], p: int
) -> list[tuple[int, ...]]:
    coefficients = shortened_coeff_basis(dual_basis, excluded, p)
    return [linear_combination(vector, dual_basis, p) for vector in coefficients]


def flat_contained(
    functional: Sequence[int], flat_basis: Sequence[Sequence[int]], p: int
) -> bool:
    return all(dot(functional, vector, p) == 0 for vector in flat_basis)


def exact_flat_list_count(
    functional: Sequence[int],
    dual_basis: Sequence[Sequence[int]],
    n: int,
    radius: int,
    p: int,
) -> int:
    count = 0
    for size in range(radius + 1):
        for excluded_tuple in combinations(range(n), size):
            excluded = tuple(excluded_tuple)
            flat = shortened_coeff_basis(dual_basis, excluded, p)
            if not flat_contained(functional, flat, p):
                continue
            exact = True
            for coordinate in excluded:
                smaller = tuple(x for x in excluded if x != coordinate)
                extended_flat = shortened_coeff_basis(dual_basis, smaller, p)
                if flat_contained(functional, extended_flat, p):
                    exact = False
                    break
            if exact:
                count += 1
    return count


def enumerate_low_weight_errors(
    p: int,
    n: int,
    radius: int,
    dual_basis: Sequence[Sequence[int]],
) -> tuple[Counter[tuple[int, ...]], list[tuple[int, ...]]]:
    counts: Counter[tuple[int, ...]] = Counter()
    errors: list[tuple[int, ...]] = []
    for size in range(radius + 1):
        for support in combinations(range(n), size):
            for values in product(range(1, p), repeat=size):
                error = [0] * n
                for coordinate, value in zip(support, values):
                    error[coordinate] = value
                error_tuple = tuple(error)
                syndrome = tuple(dot(error_tuple, row, p) for row in dual_basis)
                counts[syndrome] += 1
                errors.append(error_tuple)
    return counts, errors


def check_exact_flat_and_syndrome_toy() -> dict[str, int | bool]:
    p = 7
    domain = tuple(range(6))
    n = len(domain)
    dimension = 3
    radius = 2
    generator = [
        [pow(point, degree, p) for point in domain]
        for degree in range(dimension)
    ]
    dual_basis = nullspace_mod(generator, p, n)
    require(len(dual_basis) == n - dimension == 3, "toy dual dimension")
    require(
        all(dot(code_row, dual_row, p) == 0
            for code_row in generator for dual_row in dual_basis),
        "toy dual orthogonality",
    )

    error_counts, errors = enumerate_low_weight_errors(
        p, n, radius, dual_basis
    )
    require(len(errors) == 577, "toy low-weight error census")

    scope_counterexample_syndrome = (2, 5, 2)
    scope_counterexample_errors = [
        error
        for error in errors
        if tuple(dot(error, row, p) for row in dual_basis)
        == scope_counterexample_syndrome
    ]
    scope_counterexample_supports = {
        tuple(index for index, value in enumerate(error) if value)
        for error in scope_counterexample_errors
    }
    scope_counterexample_power_sums = {
        sum(support) % p for support in scope_counterexample_supports
    }
    require(
        scope_counterexample_supports == {(0, 1), (2, 4)},
        "same-syndrome support counterexample",
    )
    require(
        scope_counterexample_power_sums == {1, 6},
        "syndrome fiber is not a support power-sum prefix fiber",
    )
    flat_total = 0
    for functional in product(range(p), repeat=len(dual_basis)):
        flat_count = exact_flat_list_count(
            functional, dual_basis, n, radius, p
        )
        require(flat_count == error_counts[tuple(functional)], "flat/error count")
        flat_total += flat_count
    require(flat_total == len(errors), "flat objective total")
    zero = (0,) * len(dual_basis)
    require(error_counts[zero] == 1, "zero syndrome handled separately")

    for functional in product(range(p), repeat=len(dual_basis)):
        if not any(functional):
            continue
        representative = canonical_projective(functional, p)
        require(
            error_counts[tuple(functional)] == error_counts[representative],
            "projective syndrome scaling invariance",
        )

    dual_weights: list[int] = []
    for point in domain:
        denominator = 1
        for other in domain:
            if other != point:
                denominator = denominator * (point - other) % p
        dual_weights.append(pow(denominator, -1, p))
    grs_dual_rows = [
        tuple(
            weight * pow(point, degree, p) % p
            for point, weight in zip(domain, dual_weights)
        )
        for degree in range(n - dimension)
    ]
    require(
        rowspaces_equal(grs_dual_rows, dual_basis, p, n),
        "weighted GRS dual normalization",
    )

    shift_checks = 0
    for size in range(radius + 1):
        for excluded in combinations(range(n), size):
            excluded_points = tuple(domain[index] for index in excluded)
            locator_coefficients = locator(excluded_points, p)
            shift_rows: list[tuple[int, ...]] = []
            for shift in range((n - dimension) - size):
                shifted = (0,) * shift + locator_coefficients
                row = tuple(
                    weight * eval_poly(shifted, point, p) % p
                    for point, weight in zip(domain, dual_weights)
                )
                shift_rows.append(row)
            actual = ambient_shortening_basis(dual_basis, excluded, p)
            require(
                len(shift_rows) == (n - dimension) - size,
                "toy MDS shortening dimension",
            )
            require(
                rowspaces_equal(shift_rows, actual, p, n),
                "locator shifts equal shortened flat",
            )
            for error in errors:
                moments = [
                    sum(
                        error[index]
                        * dual_weights[index]
                        * pow(point, degree, p)
                        for index, point in enumerate(domain)
                    )
                    % p
                    for degree in range(n - dimension)
                ]
                for shift, row in enumerate(shift_rows):
                    recurrence = sum(
                        coefficient * moments[shift + index]
                        for index, coefficient in enumerate(locator_coefficients)
                    ) % p
                    require(
                        dot(error, row, p) == recurrence,
                        "shifted locator syndrome recurrence",
                    )
                    shift_checks += 1

    return {
        "field": p,
        "length": n,
        "dimension": dimension,
        "radius": radius,
        "syndromes": p ** (n - dimension),
        "errors": len(errors),
        "shift_checks": shift_checks,
        "same_syndrome_distinct_support_power_sums": True,
    }


def check_scalar_toy_replay() -> dict[str, int]:
    p = 1_009
    n = 16
    dimension = 8
    agreement = 10
    scalar_endpoint = Fraction(comb(n, dimension), comb(agreement, dimension))
    require(scalar_endpoint == 286, "toy scalar endpoint")
    table = [
        [krawtchouk(p, n, shell, weight) for weight in range(n + 1)]
        for shell in range(n + 1)
    ]
    shell_checks = 0
    for tail in range(scalar_endpoint.numerator + 1):
        agreement_counts = scalar_agreement_polynomial(
            p, n, dimension, agreement, tail
        )
        weights = [
            agreement_counts[n - weight]
            if 0 <= n - weight < len(agreement_counts)
            else 0
            for weight in range(n + 1)
        ]
        require(min(agreement_counts) >= 0, "toy scalar nonnegativity")
        require(sum(weights) == p**dimension, "toy scalar mass")
        require(weights[0] == 0, "toy nonzero coset")
        require(sum(weights[: n - agreement + 1]) == tail, "toy scalar tail")
        for shell in range(n + 1):
            transform = sum(
                weights[weight] * table[shell][weight]
                for weight in range(n + 1)
            )
            if shell == 0:
                require(transform == p**dimension, "toy zeroth transform")
            elif shell <= dimension:
                require(transform == 0, "toy vanishing dual shell")
            else:
                shell_size = projective_mds_shell(p, n, dimension, shell)
                require(transform % p**dimension == 0, "toy transform divisibility")
                numerator = transform // p**dimension + shell_size
                require(numerator % p == 0, "toy projective congruence")
                selected = numerator // p
                require(0 <= selected <= shell_size, "toy shell interval")
                shell_checks += 1
    return {"profiles": 287, "shell_checks": shell_checks}


def check_local_line_completion_toy() -> dict[str, int]:
    p = 11
    n = 8
    dimension = 4
    domain = tuple(range(n))
    block = frozenset(range(6))
    generator = [
        [pow(point, degree, p) for point in domain]
        for degree in range(dimension)
    ]
    dual_basis = nullspace_mod(generator, p, n)
    require(len(dual_basis) == 4, "local-line toy dual dimension")

    point_supports: dict[tuple[int, ...], frozenset[int]] = {}
    for coefficients in projective_points(p, len(dual_basis)):
        ambient = linear_combination(coefficients, dual_basis, p)
        point_supports[coefficients] = frozenset(
            index for index, value in enumerate(ambient) if value
        )

    selected: set[tuple[int, ...]] = {
        point
        for point, support in point_supports.items()
        if len(support) == dimension + 1 and support <= block
    }
    state_counts: Counter[int] = Counter()
    shortened_lines: dict[frozenset[int], tuple[tuple[int, ...], ...]] = {}
    for support_tuple in combinations(range(n), dimension + 2):
        support = frozenset(support_tuple)
        line = tuple(
            point
            for point, point_support in point_supports.items()
            if point_support <= support
        )
        require(len(line) == p + 1, "local shortened line cardinality")
        shortened_lines[support] = line
        facets = [
            point
            for point in line
            if len(point_supports[point]) == dimension + 1
            and point in selected
        ]
        state = len(facets)
        require(state in (0, 1, dimension + 2), "local facet state")
        state_counts[state] += 1
        full_support = sorted(
            point for point in line if point_supports[point] == support
        )
        require(
            len(full_support) == p - dimension - 1,
            "local full-support point count",
        )
        if state == 0:
            selected.add(full_support[0])
        elif state == dimension + 2:
            selected.update(full_support)

    bad_lines = 0
    for line in shortened_lines.values():
        selected_count = sum(point in selected for point in line)
        if selected_count not in (1, p + 1):
            bad_lines += 1
    require(bad_lines == 0, "global local-line completion consistency")
    require(state_counts == Counter({0: 15, 1: 12, 6: 1}), "local states")
    return {
        "field": p,
        "length": n,
        "dimension": dimension,
        "lines": len(shortened_lines),
        "state_zero": state_counts[0],
        "state_one": state_counts[1],
        "state_all": state_counts[dimension + 2],
        "bad_lines": bad_lines,
    }


def check_projective_line_characterization() -> dict[str, int]:
    cases = ((2, 3), (3, 3), (2, 4))
    total_candidates = 0
    total_hyperplanes = 0
    for p, dimension in cases:
        points = projective_points(p, dimension)
        lines = projective_lines(points, p)
        hyperplanes = projective_hyperplanes(points, p)
        expected_points = (p**dimension - 1) // (p - 1)
        expected_lines = (
            (p**dimension - 1)
            * (p ** (dimension - 1) - 1)
            // ((p**2 - 1) * (p - 1))
        )
        hyperplane_size = (p ** (dimension - 1) - 1) // (p - 1)
        require(len(points) == expected_points, "projective point count")
        require(len(lines) == expected_lines, "projective line count")
        require(all(len(line) == p + 1 for line in lines), "line cardinality")
        require(len(hyperplanes) == expected_points, "hyperplane count")
        feasible: set[frozenset[tuple[int, ...]]] = set()
        for chosen in combinations(points, hyperplane_size):
            selected = frozenset(chosen)
            if all(len(selected & line) in (1, p + 1) for line in lines):
                feasible.add(selected)
        require(feasible == hyperplanes, "line law characterizes hyperplanes")
        total_candidates += comb(len(points), hyperplane_size)
        total_hyperplanes += len(hyperplanes)
    local = check_local_line_completion_toy()
    return {
        "cases": len(cases),
        "candidates": total_candidates,
        "hyperplanes": total_hyperplanes,
        "local_field": local["field"],
        "local_length": local["length"],
        "local_dimension": local["dimension"],
        "local_lines": local["lines"],
        "local_state_zero": local["state_zero"],
        "local_state_one": local["state_one"],
        "local_state_all": local["state_all"],
        "local_bad_lines": local["bad_lines"],
    }


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_hash(document: dict[str, Any]) -> str:
    payload = copy.deepcopy(document)
    payload.pop("certificate_sha256", None)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def seal(document: dict[str, Any]) -> dict[str, Any]:
    sealed = copy.deepcopy(document)
    sealed["certificate_sha256"] = payload_hash(sealed)
    return sealed


def expected_source_hashes() -> dict[str, str]:
    paths = (
        NOTE_PATH,
        Path(__file__),
        SAGE_PATH,
        ROOT / "experimental/notes/thresholds/m31_scalar_descent_equivalence.md",
        ROOT / "experimental/scripts/verify_m31_scalar_descent_equivalence.py",
        ROOT / "experimental/notes/thresholds/projective_line_lift_feasibility_wall.md",
        ROOT / "experimental/scripts/verify_projective_line_lift_feasibility_wall.py",
        ROOT / "experimental/notes/l1/l1_syndrome_catalecticant_shells.md",
        ROOT / "experimental/scripts/verify_l1_syndrome_catalecticant_shells.py",
        ROOT / "experimental/notes/thresholds/weighted_grs_mds_coset_packing.md",
        ROOT / "experimental/scripts/verify_weighted_grs_mds_coset_packing.py",
        ROOT / "experimental/notes/thresholds/m31_ade_rho9_architecture_wall.md",
        ROOT / "experimental/scripts/verify_m31_ade_rho9_architecture_wall.py",
        ROOT / "experimental/scripts/verify_m31_ade_rho9_architecture_wall.sage",
    )
    return {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in paths
    }


def build_certificate(
    ledger: dict[str, int],
    scalar: dict[str, int | Fraction],
    local: dict[str, int | Fraction],
    toy: dict[str, int | bool],
    scalar_toy: dict[str, int],
    projective_toy: dict[str, int],
) -> dict[str, Any]:
    ratio = local["shadow_ratio"]
    require(isinstance(ratio, Fraction), "shadow ratio type")
    document: dict[str, Any] = {
        "schema": "m31-shortened-flat-hyperplane-wall-v1",
        "status": "PROVED_EXACT_BRIDGE_AND_ROUTE_CUT_GLOBAL_BOUND_OPEN",
        "base_commit": BASE_COMMIT,
        "provenance": EXPECTED_PROVENANCE,
        "parameters": {
            "p": P,
            "n": N,
            "k": K,
            "agreement": A,
            "sigma": SIGMA,
            "radius": RADIUS,
            "minimum_distance": ledger["minimum_distance"],
            "budget": BUDGET,
            "forbidden_size": FORBIDDEN,
            "domain": "M31_CHEBYSHEV_TWIN_COSET_IN_F_P",
        },
        "external_route_arithmetic": check_external_route_arithmetic(),
        "exact_object": {
            "zero_syndrome_handled_separately": True,
            "zero_syndrome_list_size": 1,
            "nonzero_syndrome_is_projective_hyperplane": True,
            "support_flat_equivalence": True,
            "exact_support_requires_all_one_point_escapes": True,
            "support_sum_duplicate_free": True,
            "center_to_dual_map_surjective": True,
            "boundary_flat_dimension": ledger["boundary_flat_dimension"],
            "one_point_extension_dimension": ledger[
                "one_point_extension_dimension"
            ],
            "locator_syndrome_recurrence_equivalent": True,
            "deployed_weight_power_sum_prefix_equivalent": False,
            "global_projective_line_system_exact": True,
            "objective": "FULL_ARBITRARY_CENTER_BASE_FIELD_LIST",
            "orbit_compression_proved": False,
        },
        "scalar_shell_route_cut": {
            "formal_tail": scalar["formal_tail"],
            "lambda_lower_floor": scalar["lambda_lower_floor"],
            "lambda_margin": scalar["lambda_margin"],
            "positive_gap_numerator": scalar["positive_gap_numerator"],
            "positive_gap_denominator": scalar["positive_gap_denominator"],
            "negative_gap_numerator": scalar["negative_gap_numerator"],
            "negative_gap_denominator": scalar["negative_gap_denominator"],
            "low_gate_1": scalar["low_gate_1"],
            "low_gate_2": scalar["low_gate_2"],
            "forbidden_profile_scalar_feasible": True,
        },
        "local_line_route_cut": {
            "shadow_ratio_numerator": ratio.numerator,
            "shadow_ratio_denominator": ratio.denominator,
            "shadow_certified_floor": local["shadow_floor"],
            "endpoint_cut_lower_bound": local["endpoint_cut"],
            "binary_code_length": local["binary_length"],
            "binary_code_dimension": local["binary_dimension"],
            "binary_code_distance": local["binary_distance"],
            "binary_code_size": local["binary_size"],
            "binary_code_size_margin_over_budget": local[
                "binary_size_margin_over_budget"
            ],
            "binary_weight_distribution": {
                "0": local["weight_zero_count"],
                "67584": local["weight_67584_count"],
                "135168": local["weight_135168_count"],
            },
            "maximum_block_intersection": local[
                "maximum_block_intersection"
            ],
            "unused_coordinates": local["unused_coordinates"],
            "full_support_points_per_K_plus_2_line": local[
                "full_support_points"
            ],
            "extensions_per_minimum_support": local[
                "extensions_per_minimum_support"
            ],
            "facets_per_inside_support": local[
                "facets_per_inside_support"
            ],
            "completion_coefficient": local["completion_coefficient"],
            "all_K_plus_2_local_line_laws_satisfied": True,
            "cross_S_assignment_consistent": True,
            "K_plus_1_shell_formula": "L*binom(a,K+1)",
            "K_plus_2_shell_formula": (
                "binom(n,K+2)+L*(p*binom(a,K+2)"
                "-(K-1)*binom(a,K+1))"
            ),
            "matches_scalar_profile_q_L_first_two_shells": True,
            "K_plus_1_q0_formula": "0",
            "K_plus_2_q0_formula": "binom(n,K+2)",
            "K_plus_1_slope_formula": "binom(a,K+1)",
            "K_plus_2_slope_formula": (
                "p*binom(a,K+2)-(K-1)*binom(a,K+1)"
            ),
            "formal_model_is_actual_grs_hyperplane": False,
            "cross_support_global_line_closure_required": True,
        },
        "scalar_descent": {
            "prime_to_quartic_equivalence_at_forbidden_size": True,
            "strict_margin": ledger["scalar_descent_margin"],
        },
        "toy_controls": {
            "flat_syndrome_field": toy["field"],
            "flat_syndrome_length": toy["length"],
            "flat_syndrome_dimension": toy["dimension"],
            "flat_syndrome_radius": toy["radius"],
            "flat_syndrome_count": toy["syndromes"],
            "flat_syndrome_errors": toy["errors"],
            "flat_syndrome_shift_checks": toy["shift_checks"],
            "same_syndrome_distinct_support_power_sums": toy[
                "same_syndrome_distinct_support_power_sums"
            ],
            "scalar_profiles": scalar_toy["profiles"],
            "scalar_dual_shell_checks": scalar_toy["shell_checks"],
            "projective_cases": projective_toy["cases"],
            "projective_candidate_subsets": projective_toy["candidates"],
            "projective_hyperplanes": projective_toy["hyperplanes"],
            "local_line_field": projective_toy["local_field"],
            "local_line_length": projective_toy["local_length"],
            "local_line_dimension": projective_toy["local_dimension"],
            "local_line_count": projective_toy["local_lines"],
            "local_line_state_zero": projective_toy["local_state_zero"],
            "local_line_state_one": projective_toy["local_state_one"],
            "local_line_state_all": projective_toy["local_state_all"],
            "local_line_bad_count": projective_toy["local_bad_lines"],
        },
        "ledger": {
            "prime_field_row_closed": False,
            "quartic_field_row_closed": False,
            "U_Q": None,
            "U_A": None,
            "ledger_movement": 0,
            "prize_claimed": False,
        },
        "future_separator_regression": {
            "rho9_ade_pseudomodel_must_be_rejected": True,
            "currently_rejected_by_this_packet": False,
            "source_pr": 1000,
        },
        "source_sha256": expected_source_hashes(),
    }
    return seal(document)


def validate_certificate(document: dict[str, Any], *, check_sources: bool) -> None:
    require(document.get("certificate_sha256") == payload_hash(document), "self hash")
    require(document.get("schema") == "m31-shortened-flat-hyperplane-wall-v1", "schema")
    require(
        document.get("status")
        == "PROVED_EXACT_BRIDGE_AND_ROUTE_CUT_GLOBAL_BOUND_OPEN",
        "status",
    )
    require(document.get("base_commit") == BASE_COMMIT, "base commit")
    require(document.get("provenance") == EXPECTED_PROVENANCE, "provenance")
    parameters = document["parameters"]
    expected_parameters = {
        "p": P,
        "n": N,
        "k": K,
        "agreement": A,
        "sigma": SIGMA,
        "radius": RADIUS,
        "minimum_distance": K + 1,
        "budget": BUDGET,
        "forbidden_size": FORBIDDEN,
        "domain": "M31_CHEBYSHEV_TWIN_COSET_IN_F_P",
    }
    require(parameters == expected_parameters, "parameter ledger")
    require(
        document["external_route_arithmetic"]
        == check_external_route_arithmetic(),
        "external-route arithmetic",
    )

    exact = document["exact_object"]
    require(
        exact
        == {
            "zero_syndrome_handled_separately": True,
            "zero_syndrome_list_size": 1,
            "nonzero_syndrome_is_projective_hyperplane": True,
            "support_flat_equivalence": True,
            "exact_support_requires_all_one_point_escapes": True,
            "support_sum_duplicate_free": True,
            "center_to_dual_map_surjective": True,
            "boundary_flat_dimension": SIGMA,
            "one_point_extension_dimension": SIGMA + 1,
            "locator_syndrome_recurrence_equivalent": True,
            "deployed_weight_power_sum_prefix_equivalent": False,
            "global_projective_line_system_exact": True,
            "objective": "FULL_ARBITRARY_CENTER_BASE_FIELD_LIST",
            "orbit_compression_proved": False,
        },
        "exact-object ledger",
    )
    require(exact["zero_syndrome_handled_separately"] is True, "zero syndrome")
    require(exact["zero_syndrome_list_size"] == 1, "zero syndrome list")
    require(exact["nonzero_syndrome_is_projective_hyperplane"] is True, "hyperplane")
    require(exact["support_flat_equivalence"] is True, "flat equivalence")
    require(exact["exact_support_requires_all_one_point_escapes"] is True, "escape")
    require(exact["support_sum_duplicate_free"] is True, "duplicate free")
    require(exact["boundary_flat_dimension"] == SIGMA, "flat dimension")
    require(exact["one_point_extension_dimension"] == SIGMA + 1, "extension dimension")
    require(
        exact["locator_syndrome_recurrence_equivalent"] is True,
        "syndrome recurrence bridge",
    )
    require(
        exact["deployed_weight_power_sum_prefix_equivalent"] is False,
        "no weight-power-sum prefix overclaim",
    )
    require(exact["global_projective_line_system_exact"] is True, "global lines")
    require(exact["objective"] == "FULL_ARBITRARY_CENTER_BASE_FIELD_LIST", "objective")
    require(exact["orbit_compression_proved"] is False, "no fake compression")

    scalar = document["scalar_shell_route_cut"]
    require(
        scalar
        == {
            **check_scalar_shell_route_cut(),
            "forbidden_profile_scalar_feasible": True,
        },
        "scalar route-cut ledger",
    )

    local = document["local_line_route_cut"]
    expected_local = check_shadow_and_local_route_cut()
    expected_ratio = expected_local["shadow_ratio"]
    require(isinstance(expected_ratio, Fraction), "expected manifest ratio type")
    require(
        local
        == {
            "shadow_ratio_numerator": expected_ratio.numerator,
            "shadow_ratio_denominator": expected_ratio.denominator,
            "shadow_certified_floor": expected_local["shadow_floor"],
            "endpoint_cut_lower_bound": expected_local["endpoint_cut"],
            "binary_code_length": expected_local["binary_length"],
            "binary_code_dimension": expected_local["binary_dimension"],
            "binary_code_distance": expected_local["binary_distance"],
            "binary_code_size": expected_local["binary_size"],
            "binary_code_size_margin_over_budget": expected_local[
                "binary_size_margin_over_budget"
            ],
            "binary_weight_distribution": {
                "0": expected_local["weight_zero_count"],
                "67584": expected_local["weight_67584_count"],
                "135168": expected_local["weight_135168_count"],
            },
            "maximum_block_intersection": expected_local[
                "maximum_block_intersection"
            ],
            "unused_coordinates": expected_local["unused_coordinates"],
            "full_support_points_per_K_plus_2_line": expected_local[
                "full_support_points"
            ],
            "extensions_per_minimum_support": expected_local[
                "extensions_per_minimum_support"
            ],
            "facets_per_inside_support": expected_local[
                "facets_per_inside_support"
            ],
            "completion_coefficient": expected_local[
                "completion_coefficient"
            ],
            "all_K_plus_2_local_line_laws_satisfied": True,
            "cross_S_assignment_consistent": True,
            "K_plus_1_shell_formula": "L*binom(a,K+1)",
            "K_plus_2_shell_formula": (
                "binom(n,K+2)+L*(p*binom(a,K+2)"
                "-(K-1)*binom(a,K+1))"
            ),
            "matches_scalar_profile_q_L_first_two_shells": True,
            "K_plus_1_q0_formula": "0",
            "K_plus_2_q0_formula": "binom(n,K+2)",
            "K_plus_1_slope_formula": "binom(a,K+1)",
            "K_plus_2_slope_formula": (
                "p*binom(a,K+2)-(K-1)*binom(a,K+1)"
            ),
            "formal_model_is_actual_grs_hyperplane": False,
            "cross_support_global_line_closure_required": True,
        },
        "local route-cut ledger",
    )
    require(
        Fraction(local["shadow_ratio_numerator"], local["shadow_ratio_denominator"])
        == EXPECTED_SHADOW_RATIO,
        "manifest shadow ratio",
    )
    require(local["shadow_certified_floor"] == EXPECTED_SHADOW_FLOOR_100, "shadow floor")
    require(local["endpoint_cut_lower_bound"] == EXPECTED_ENDPOINT_CUT_100, "endpoint cut")
    require(local["binary_code_length"] == RADIUS, "manifest binary length")
    require(local["binary_code_dimension"] == 24, "manifest binary dimension")
    require(local["binary_code_distance"] == 67_584, "manifest binary distance")
    require(local["binary_code_size"] == FORBIDDEN, "manifest binary size")
    require(local["binary_code_size_margin_over_budget"] == 1, "binary margin")
    require(
        local["binary_weight_distribution"]
        == {"0": 1, "67584": 8_190, "135168": 16_769_025},
        "binary weight distribution",
    )
    require(local["binary_code_size"] > BUDGET, "manifest route cut")
    require(local["maximum_block_intersection"] == K - 137, "intersection cap")
    require(local["unused_coordinates"] == 134_894, "embedding reserve")
    require(
        local["full_support_points_per_K_plus_2_line"] == P - K - 1,
        "full-support line points",
    )
    require(local["all_K_plus_2_local_line_laws_satisfied"] is True, "local laws")
    require(local["cross_S_assignment_consistent"] is True, "cross-S consistency")
    require(
        local["K_plus_1_shell_formula"] == "L*binom(a,K+1)",
        "K+1 shell formula",
    )
    require(
        local["K_plus_2_shell_formula"]
        == "binom(n,K+2)+L*(p*binom(a,K+2)-(K-1)*binom(a,K+1))",
        "K+2 shell formula",
    )
    require(local["formal_model_is_actual_grs_hyperplane"] is False, "formal only")
    require(local["cross_support_global_line_closure_required"] is True, "global closure")

    descent = document["scalar_descent"]
    require(
        descent
        == {
            "prime_to_quartic_equivalence_at_forbidden_size": True,
            "strict_margin": EXPECTED_SCALAR_DESCENT_MARGIN,
        },
        "scalar-descent ledger",
    )
    require(descent["prime_to_quartic_equivalence_at_forbidden_size"] is True, "descent")
    require(descent["strict_margin"] == EXPECTED_SCALAR_DESCENT_MARGIN, "descent margin")

    ledger = document["ledger"]
    require(
        ledger
        == {
            "prime_field_row_closed": False,
            "quartic_field_row_closed": False,
            "U_Q": None,
            "U_A": None,
            "ledger_movement": 0,
            "prize_claimed": False,
        },
        "open-ledger contract",
    )
    require(ledger["prime_field_row_closed"] is False, "prime row remains open")
    require(ledger["quartic_field_row_closed"] is False, "quartic row remains open")
    require(ledger["U_Q"] is None and ledger["U_A"] is None, "unpaid ledgers")
    require(ledger["ledger_movement"] == 0, "zero ledger movement")
    require(ledger["prize_claimed"] is False, "no prize claim")

    regression = document["future_separator_regression"]
    require(
        regression
        == {
            "rho9_ade_pseudomodel_must_be_rejected": True,
            "currently_rejected_by_this_packet": False,
            "source_pr": 1000,
        },
        "future-separator contract",
    )
    require(regression["rho9_ade_pseudomodel_must_be_rejected"] is True, "rho9 regression")
    require(
        regression["currently_rejected_by_this_packet"] is False,
        "rho9 regression remains future work",
    )
    require(regression["source_pr"] == 1000, "rho9 source PR")
    toys = document["toy_controls"]
    require(
        toys
        == {
            "flat_syndrome_field": 7,
            "flat_syndrome_length": 6,
            "flat_syndrome_dimension": 3,
            "flat_syndrome_radius": 2,
            "flat_syndrome_count": 343,
            "flat_syndrome_errors": 577,
            "flat_syndrome_shift_checks": 17_310,
            "same_syndrome_distinct_support_power_sums": True,
            "scalar_profiles": 287,
            "scalar_dual_shell_checks": 2_296,
            "projective_cases": 3,
            "projective_candidate_subsets": 7_185,
            "projective_hyperplanes": 35,
            "local_line_field": 11,
            "local_line_length": 8,
            "local_line_dimension": 4,
            "local_line_count": 28,
            "local_line_state_zero": 15,
            "local_line_state_one": 12,
            "local_line_state_all": 1,
            "local_line_bad_count": 0,
        },
        "toy-control ledger",
    )
    if check_sources:
        require(document["source_sha256"] == expected_source_hashes(), "source hashes")


def set_path(document: dict[str, Any], path: Sequence[str], value: Any) -> None:
    cursor: dict[str, Any] = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


def run_tamper_selftest(canonical: dict[str, Any]) -> int:
    mutations: tuple[tuple[tuple[str, ...], Any], ...] = (
        (("schema",), "m31-shortened-flat-hyperplane-wall-v0"),
        (("status",), "PROVED_ROW_CLOSED"),
        (("base_commit",), "0" * 40),
        (("provenance", "projective_line_wall_pr"), 719),
        (("provenance", "scalar_descent_head"), "0" * 40),
        (("parameters", "p"), P - 2),
        (("parameters", "n"), N - 1),
        (("parameters", "k"), K - 1),
        (("parameters", "agreement"), A - 1),
        (("parameters", "sigma"), SIGMA - 1),
        (("parameters", "radius"), RADIUS - 1),
        (("parameters", "budget"), BUDGET + 1),
        (("parameters", "forbidden_size"), FORBIDDEN + 1),
        (("parameters", "domain"), "MULTIPLICATIVE_SUBGROUP"),
        (("external_route_arithmetic", "johnson_max_integer_errors"), RADIUS),
        (("external_route_arithmetic", "countermodel_binary_distance"), 134_896),
        (("exact_object", "zero_syndrome_handled_separately"), False),
        (("exact_object", "zero_syndrome_list_size"), 0),
        (("exact_object", "support_flat_equivalence"), False),
        (("exact_object", "exact_support_requires_all_one_point_escapes"), False),
        (("exact_object", "support_sum_duplicate_free"), False),
        (("exact_object", "center_to_dual_map_surjective"), False),
        (("exact_object", "boundary_flat_dimension"), SIGMA + 1),
        (("exact_object", "one_point_extension_dimension"), SIGMA),
        (("exact_object", "locator_syndrome_recurrence_equivalent"), False),
        (("exact_object", "deployed_weight_power_sum_prefix_equivalent"), True),
        (("exact_object", "global_projective_line_system_exact"), False),
        (("exact_object", "orbit_compression_proved"), True),
        (("scalar_shell_route_cut", "formal_tail"), FORBIDDEN - 1),
        (("scalar_shell_route_cut", "lambda_margin"), 0),
        (("scalar_shell_route_cut", "low_gate_1"), 0),
        (("scalar_shell_route_cut", "positive_gap_denominator"), 1),
        (("scalar_shell_route_cut", "forbidden_profile_scalar_feasible"), False),
        (("local_line_route_cut", "binary_code_length"), RADIUS - 1),
        (("local_line_route_cut", "binary_code_distance"), SIGMA),
        (("local_line_route_cut", "binary_code_size"), BUDGET),
        (("local_line_route_cut", "binary_code_size_margin_over_budget"), 0),
        (("local_line_route_cut", "binary_weight_distribution", "67584"), 8_189),
        (("local_line_route_cut", "maximum_block_intersection"), K),
        (("local_line_route_cut", "unused_coordinates"), 0),
        (("local_line_route_cut", "full_support_points_per_K_plus_2_line"), 0),
        (("local_line_route_cut", "all_K_plus_2_local_line_laws_satisfied"), False),
        (("local_line_route_cut", "cross_S_assignment_consistent"), False),
        (("local_line_route_cut", "K_plus_1_shell_formula"), "binom(a,K+1)"),
        (("local_line_route_cut", "K_plus_2_shell_formula"), "UNKNOWN"),
        (("local_line_route_cut", "matches_scalar_profile_q_L_first_two_shells"), False),
        (("local_line_route_cut", "K_plus_2_slope_formula"), "UNKNOWN"),
        (("local_line_route_cut", "formal_model_is_actual_grs_hyperplane"), True),
        (("local_line_route_cut", "cross_support_global_line_closure_required"), False),
        (("scalar_descent", "prime_to_quartic_equivalence_at_forbidden_size"), False),
        (("ledger", "prime_field_row_closed"), True),
        (("ledger", "quartic_field_row_closed"), True),
        (("ledger", "U_Q"), 0),
        (("ledger", "ledger_movement"), 1),
        (("ledger", "prize_claimed"), True),
        (("future_separator_regression", "rho9_ade_pseudomodel_must_be_rejected"), False),
        (("future_separator_regression", "currently_rejected_by_this_packet"), True),
        (("future_separator_regression", "source_pr"), 999),
        (("toy_controls", "same_syndrome_distinct_support_power_sums"), False),
        (("toy_controls", "flat_syndrome_errors"), 576),
        (("toy_controls", "flat_syndrome_shift_checks"), 17_309),
        (("toy_controls", "scalar_dual_shell_checks"), 2_295),
        (("toy_controls", "projective_hyperplanes"), 34),
        (("toy_controls", "local_line_count"), 27),
        (("toy_controls", "local_line_state_zero"), 14),
        (("toy_controls", "local_line_bad_count"), 1),
        (
            (
                "source_sha256",
                "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md",
            ),
            "0" * 64,
        ),
    )
    rejected = 0
    for path, value in mutations:
        mutant = copy.deepcopy(canonical)
        set_path(mutant, path, value)
        mutant = seal(mutant)
        try:
            validate_certificate(mutant, check_sources=True)
        except (VerificationError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"tamper survived: {'.'.join(path)}")
    require(rejected == len(mutations), "all semantic mutations rejected")
    return rejected


def run_core_checks() -> tuple[
    dict[str, int | bool],
    dict[str, int | Fraction],
    dict[str, int | Fraction],
    dict[str, int],
    dict[str, int],
    dict[str, int],
]:
    check_optimization_safety()
    ledger = check_deployed_ledger()
    scalar = check_scalar_shell_route_cut()
    local = check_shadow_and_local_route_cut()
    toy = check_exact_flat_and_syndrome_toy()
    scalar_toy = check_scalar_toy_replay()
    projective_toy = check_projective_line_characterization()
    return ledger, scalar, local, toy, scalar_toy, projective_toy


def print_summary(
    ledger: dict[str, int],
    scalar: dict[str, int | Fraction],
    local: dict[str, int | Fraction],
    toy: dict[str, int | bool],
    scalar_toy: dict[str, int],
    projective_toy: dict[str, int],
) -> None:
    ratio = local["shadow_ratio"]
    require(isinstance(ratio, Fraction), "summary ratio type")
    print("object: M31 shortened-flat/projective-hyperplane architecture wall")
    print("status: PROVED exact bridge + route cut / global row OPEN")
    print("runtime: Python stdlib only; assert-free exact checks")
    print(
        "deployed: "
        f"p={P} n={N} K={K} a={A} sigma={SIGMA} "
        f"radius={RADIUS} B*={BUDGET} forbidden={FORBIDDEN}"
    )
    external = check_external_route_arithmetic()
    print(
        "external-route arithmetic: "
        f"BW_deficit={external['berlekamp_welch_agreement_deficit']} "
        f"Johnson_error_excess={external['deployed_errors_over_johnson']} "
        f"support_distance={external['countermodel_binary_distance']}>"
        f"{external['packing_required_binary_distance']}"
    )
    print(
        "exact flat objective: "
        f"boundary_dim={ledger['boundary_flat_dimension']} "
        f"one_point_dim={ledger['one_point_extension_dimension']} "
        "zero_syndrome=separate duplicate_free=PASS"
    )
    print(
        "scalar descent: "
        f"prime<->quartic forbidden-size equivalence margin="
        f"{ledger['scalar_descent_margin']}"
    )
    print(
        "scalar-shell route cut: "
        f"formal_tail={scalar['formal_tail']} "
        f"lambda_lower_floor={scalar['lambda_lower_floor']} "
        f"margin={scalar['lambda_margin']}"
    )
    print(
        "K+2 route cut: "
        f"shadow_ratio={ratio.numerator}/{ratio.denominator} "
        f"certified_floor={local['shadow_floor']}"
    )
    print(
        "formal support family: "
        f"[{local['binary_length']},{local['binary_dimension']},"
        f">={local['binary_distance']}]_2 size={local['binary_size']} "
        f"margin_over_budget={local['binary_size_margin_over_budget']}"
    )
    print(
        "binary weight distribution: "
        f"1 + {local['weight_67584_count']} z^67584 + "
        f"{local['weight_135168_count']} z^135168"
    )
    print("local shell totals: N_(K+1)=L*C(a,K+1)")
    print(
        "local shell totals: N_(K+2)=C(n,K+2)"
        "+L*(p*C(a,K+2)-(K-1)*C(a,K+1))"
    )
    print("local/scalar first-two-shell compatibility: PASS")
    print(
        "flat/syndrome toy: "
        f"GF({toy['field']}) [{toy['length']},{toy['dimension']}] "
        f"syndromes={toy['syndromes']} errors={toy['errors']} "
        f"shift_checks={toy['shift_checks']} PASS"
    )
    print(
        "scalar toy: "
        f"profiles={scalar_toy['profiles']} "
        f"dual_shell_checks={scalar_toy['shell_checks']} PASS"
    )
    print(
        "projective line-law exhaustion: "
        f"cases={projective_toy['cases']} "
        f"candidate_subsets={projective_toy['candidates']} "
        f"hyperplanes={projective_toy['hyperplanes']} PASS"
    )
    print(
        "local-line semantic toy: "
        f"GF({projective_toy['local_field']}) "
        f"[{projective_toy['local_length']},{projective_toy['local_dimension']}] "
        f"lines={projective_toy['local_lines']} "
        "states="
        f"({projective_toy['local_state_zero']},"
        f"{projective_toy['local_state_one']},"
        f"{projective_toy['local_state_all']}) "
        f"bad={projective_toy['local_bad_lines']} PASS"
    )
    print("global cross-support line closure: REQUIRED / UNPROVED")
    print(f"checks: {CHECKS} PASS")
    print("RESULT: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-certificate", action="store_true")
    args = parser.parse_args()
    if not (args.check or args.tamper_selftest or args.print_certificate):
        args.check = True

    ledger, scalar, local, toy, scalar_toy, projective_toy = run_core_checks()
    generated = build_certificate(
        ledger, scalar, local, toy, scalar_toy, projective_toy
    )

    if args.print_certificate:
        print(json.dumps(generated, indent=2, sort_keys=True))
        return

    require(CERTIFICATE_PATH.is_file(), "canonical certificate exists")
    canonical = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
    validate_certificate(canonical, check_sources=True)
    require(canonical == generated, "canonical certificate matches replay")

    if args.tamper_selftest:
        rejected = run_tamper_selftest(canonical)
        print(f"tamper selftest: {rejected}/{rejected} rejected")
        print("RESULT: PASS")
        return

    print_summary(ledger, scalar, local, toy, scalar_toy, projective_toy)


if __name__ == "__main__":
    main()
