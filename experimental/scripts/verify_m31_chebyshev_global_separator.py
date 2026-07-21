#!/usr/bin/env python3
"""Verify the M31 Chebyshev stabilizer and a four-flat global separator.

This packet has three exact outputs.

* The standard-position M31 x-domain is the zero divisor of ``T_(2^21)``
  and its full projective, permutation, and monomial symmetry is only sign.
* Pairwise cross-support incidence survives literally; the first
  containment-only Macaulay obstruction is the already named rank-16 gate.
* A concrete Chebyshev-fibre-aligned embedding of four blocks inside the
  ``2^24`` local support model is rejected by the full shortened-flat system.
  The deployed computation reduces to a 132 by 132 quotient determinant.

The deployed row remains open.  All checks use explicit exceptions, so
``python -O`` performs the same work as ordinary Python.  Only the standard
library is required.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from array import array
from itertools import permutations
from math import comb
from pathlib import Path
from typing import Any, Iterable, Sequence


P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
SIGMA = AGREEMENT - K
RADIUS = N - AGREEMENT
BUDGET = P**4 // 2**100
FORBIDDEN = BUDGET + 1
BASE_COMMIT = "d019ba8ebeaf28e4589f9282c7598fe2e54741cf"

FOLD = 2**10
QUOTIENT_SIZE = N // FOLD
CHUNK = 33
LOWER_FACTOR_DEGREE = CHUNK
LOWER_LOCATOR_DEGREE = 3 * CHUNK
LIFTED_FACTOR_DEGREE = CHUNK * FOLD
LIFTED_LOCATOR_DEGREE = LOWER_LOCATOR_DEGREE * FOLD
COMMON_CORE = RADIUS - LIFTED_LOCATOR_DEGREE

EXPECTED_Q = (462_183_554, 751_088_031, 26_070_540)
EXPECTED_Q_DELTA = 1_653_303_809
EXPECTED_Q_I = 299_132_536
EXPECTED_Q_J = 1_054_263_609
EXPECTED_Q_DISC = 1_954_910_887
EXPECTED_Q_RATIO = 872_293_539
EXPECTED_QUOTIENT_DETERMINANT = 398_200_308
EXPECTED_QUOTIENT_PREFIX_HASH = 1_877_696_184
EXPECTED_QUOTIENT_CHUNK_FIRST = (
    1_699_686_235,
    248_665_676,
    1_028_986_868,
    892_769_096,
    1_125_557_233,
    1_775_285_913,
)

ROOT = Path(__file__).resolve().parents[2]
NOTE_PATH = (
    ROOT
    / "experimental/notes/thresholds/m31_chebyshev_global_separator.md"
)
SAGE_PATH = (
    ROOT
    / "experimental/scripts/verify_m31_chebyshev_global_separator.sage"
)
PYTHON_PATH = (
    ROOT
    / "experimental/scripts/verify_m31_chebyshev_global_separator.py"
)
README_PATH = (
    ROOT
    / "experimental/data/certificates/m31-chebyshev-global-separator/README.md"
)
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/m31-chebyshev-global-separator/manifest.json"
)

SOURCE_PATHS = (
    ROOT / "tex/cs25_cap_v13_2.tex",
    ROOT / "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
    ROOT / "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md",
    ROOT / "experimental/scripts/verify_m31_shortened_flat_hyperplane_wall.py",
    NOTE_PATH,
    PYTHON_PATH,
    SAGE_PATH,
    README_PATH,
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(payload: Any) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def seal_certificate(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("certificate_sha256", None)
    out["certificate_sha256"] = hashlib.sha256(canonical_json(out)).hexdigest()
    return out


def verify_self_hash(payload: dict[str, Any]) -> None:
    claimed = payload.get("certificate_sha256")
    require(isinstance(claimed, str) and len(claimed) == 64, "certificate hash shape")
    unsealed = copy.deepcopy(payload)
    unsealed.pop("certificate_sha256", None)
    require(hashlib.sha256(canonical_json(unsealed)).hexdigest() == claimed, "certificate hash")


def poly_mul(left: Sequence[int], right: Sequence[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def poly_eval(coefficients: Sequence[int], point: int, p: int) -> int:
    out = 0
    for coefficient in reversed(coefficients):
        out = (out * point + coefficient) % p
    return out


def locator(points: Iterable[int], p: int) -> list[int]:
    out = [1]
    for point in points:
        out = poly_mul(out, ((-point) % p, 1), p)
    return out


def determinant_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    rows = [list(map(lambda value: value % p, row)) for row in matrix]
    require(len(rows) == len(rows[0]), "determinant square")
    size = len(rows)
    determinant = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if rows[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = -determinant % p
        value = rows[column][column]
        determinant = determinant * value % p
        inverse = pow(value, -1, p)
        for index in range(column, size):
            rows[column][index] = rows[column][index] * inverse % p
        for row in range(column + 1, size):
            scale = rows[row][column]
            if not scale:
                continue
            for index in range(column, size):
                rows[row][index] = (
                    rows[row][index] - scale * rows[column][index]
                ) % p
    return determinant


def rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    if not matrix:
        return 0
    rows = [list(map(lambda value: value % p, row)) for row in matrix]
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "rank matrix width")
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, p)
        rows[pivot_row] = [value * inverse % p for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (value - scale * pivot_value) % p
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def null_vector_mod(matrix: Sequence[Sequence[int]], p: int) -> tuple[int, ...]:
    rows = [list(map(lambda value: value % p, row)) for row in matrix]
    width = len(rows[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, p)
        rows[pivot_row] = [value * inverse % p for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or rows[row][column] == 0:
                continue
            scale = rows[row][column]
            rows[row] = [
                (value - scale * pivot_value) % p
                for value, pivot_value in zip(rows[row], rows[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
    free = next((column for column in range(width) if column not in pivot_columns), None)
    require(free is not None and len(pivot_columns) == width - 1, "unique projective map")
    vector = [0] * width
    vector[free] = 1
    for row, pivot in enumerate(pivot_columns):
        vector[pivot] = -rows[row][free] % p
    return tuple(vector)


def chebyshev_value(degree: int, x: int, p: int) -> int:
    if degree == 0:
        return 1
    if degree == 1:
        return x % p
    previous, current = 1, x % p
    for _ in range(2, degree + 1):
        previous, current = current, (2 * x * current - previous) % p
    return current


def chebyshev_roots(p: int, degree: int) -> tuple[int, ...]:
    return tuple(x for x in range(p) if chebyshev_value(degree, x, p) == 0)


def mobius_stabilizer_size(domain: Sequence[int], p: int) -> int:
    source = tuple(domain[:3])
    domain_set = set(domain)
    maps: set[tuple[int, int, int, int]] = set()
    for target in permutations(domain, 3):
        equations = [
            (x % p, 1, (-y * x) % p, (-y) % p)
            for x, y in zip(source, target)
        ]
        a, b, c, d = null_vector_mod(equations, p)
        first = next(value for value in (a, b, c, d) if value)
        inverse = pow(first, -1, p)
        normalized = tuple(value * inverse % p for value in (a, b, c, d))
        if normalized in maps:
            continue
        image: set[int] = set()
        valid = True
        for x in domain:
            denominator = (c * x + d) % p
            if denominator == 0:
                valid = False
                break
            image.add((a * x + b) * pow(denominator, -1, p) % p)
        if valid and image == domain_set:
            maps.add(normalized)
    return len(maps)


def quartic_covariant_coefficients(n: int, p: int) -> tuple[int, int, int]:
    """Compute (F,F)_(n-2) for F=homog(T_n) in O(n) field operations.

    Each derivative of order n-2 leaves a quadratic.  For an input monomial
    X^(n-2j) Z^(2j), only i=2j-h with h in {0,1,2} can survive.  This reduces
    the nominal transvectant to the three exact one-dimensional sums below.
    """

    require(n % 2 == 0 and 2 <= n < p, "covariant parameter range")
    half = n // 2
    order = n - 2

    factorial = array("I", [1])
    for value in range(1, n + 1):
        factorial.append(factorial[-1] * value % p)
    inverse_factorial = array("I", [0]) * (n + 1)
    inverse_factorial[n] = pow(factorial[n], p - 2, p)
    for value in range(n, 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % p

    coefficients = array("I", [0]) * (half + 1)
    power_two = pow(2, n - 1, p)
    inverse_four = pow(4, p - 2, p)
    for j in range(half + 1):
        x_degree = n - 2 * j
        coefficient = n * power_two % p
        coefficient = coefficient * factorial[n - j - 1] % p
        coefficient = coefficient * inverse_factorial[j] % p
        coefficient = coefficient * inverse_factorial[x_degree] % p
        coefficients[j] = (-coefficient if j % 2 else coefficient) % p
        power_two = power_two * inverse_four % p

    order_factorial = factorial[order]

    def coefficient_sum(index_sum: int, heights: Sequence[int]) -> int:
        total = 0
        for j in range(half + 1):
            other = index_sum - j
            if not 0 <= other <= half:
                continue
            for height in heights:
                derivative_y_first = 2 * j - height
                first_x, first_y = 2 - height, height
                second_x = n - 2 * index_sum + height
                second_y = 2 - second_x
                if not (
                    0 <= derivative_y_first <= order
                    and min(first_x, first_y, second_x, second_y) >= 0
                ):
                    continue
                x_degree, y_degree = n - 2 * j, 2 * j
                other_x, other_y = n - 2 * other, 2 * other
                value = coefficients[j] * coefficients[other] % p
                value = value * order_factorial % p
                value = value * inverse_factorial[derivative_y_first] % p
                value = value * inverse_factorial[order - derivative_y_first] % p
                value = value * factorial[x_degree] % p
                value = value * inverse_factorial[first_x] % p
                value = value * factorial[y_degree] % p
                value = value * inverse_factorial[first_y] % p
                value = value * factorial[other_x] % p
                value = value * inverse_factorial[second_x] % p
                value = value * factorial[other_y] % p
                value = value * inverse_factorial[second_y] % p
                if derivative_y_first % 2:
                    value = -value
                total = (total + value) % p
        return total

    return (
        coefficient_sum(half - 1, (0,)),
        coefficient_sum(half, (0, 1, 2)),
        coefficient_sum(half + 1, (2,)),
    )


Elt = tuple[int, int]


def circle_mul(left: Elt, right: Elt, p: int = P) -> Elt:
    return (
        (left[0] * right[0] - left[1] * right[1]) % p,
        (left[0] * right[1] + left[1] * right[0]) % p,
    )


def circle_pow(value: Elt, exponent: int, p: int = P) -> Elt:
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = circle_mul(out, value, p)
        value = circle_mul(value, value, p)
        exponent >>= 1
    return out


def quotient_domain() -> tuple[int, ...]:
    # Stereographic parameter t=2 gives a fixed full-order norm-one element.
    generator = (1_717_986_917, 1_288_490_189)
    require(
        (generator[0] ** 2 + generator[1] ** 2) % P == 1,
        "norm-one generator",
    )
    require(circle_pow(generator, 2**30) == (P - 1, 0), "generator full order")

    quotient_generator = circle_pow(generator, 2**18)
    require(circle_pow(quotient_generator, 8192) == (1, 0), "quotient order upper")
    require(
        circle_pow(quotient_generator, 4096) == (P - 1, 0),
        "quotient order exact",
    )
    step = circle_mul(quotient_generator, quotient_generator)
    current = quotient_generator
    roots: list[int] = []
    for _ in range(QUOTIENT_SIZE):
        roots.append(current[0])
        current = circle_mul(current, step)
    require(len(set(roots)) == QUOTIENT_SIZE, "quotient roots distinct")
    require(all(chebyshev_value(QUOTIENT_SIZE, x, P) == 0 for x in roots), "T_2048 roots")
    return tuple(roots)


def quotient_separator() -> dict[str, Any]:
    domain = quotient_domain()
    chunks = tuple(
        domain[index * CHUNK : (index + 1) * CHUNK]
        for index in range(6)
    )
    require(all(len(chunk) == CHUNK for chunk in chunks), "six quotient chunks")
    require(len(set().union(*map(set, chunks))) == 6 * CHUNK, "chunks disjoint")

    a0, a1, b0, b1, c0, c1 = (locator(chunk, P) for chunk in chunks)
    lower_locators = (
        poly_mul(poly_mul(a0, b0, P), c0, P),
        poly_mul(poly_mul(a1, b0, P), c1, P),
        poly_mul(poly_mul(a0, b1, P), c1, P),
        poly_mul(poly_mul(a1, b1, P), c0, P),
    )
    require(all(len(value) == LOWER_LOCATOR_DEGREE + 1 for value in lower_locators), "lower degrees")

    size = LOWER_LOCATOR_DEGREE + CHUNK
    macaulay = [[0] * (4 * CHUNK) for _ in range(size)]
    for block, polynomial in enumerate(lower_locators):
        for shift in range(CHUNK):
            for degree, coefficient in enumerate(polynomial):
                macaulay[degree + shift][block * CHUNK + shift] = coefficient
    determinant = determinant_mod(macaulay, P)

    prefix_hash = sum((index + 1) * value for index, value in enumerate(domain[:198])) % P
    return {
        "domain_size": len(domain),
        "domain_is_T_2048_zero_set": True,
        "chunks": 6,
        "chunk_size": CHUNK,
        "chunk_first": [chunk[0] for chunk in chunks],
        "prefix_hash": prefix_hash,
        "lower_factor_degree": CHUNK,
        "lower_locator_degree": LOWER_LOCATOR_DEGREE,
        "macaulay_rows": size,
        "macaulay_columns": 4 * CHUNK,
        "macaulay_determinant": determinant,
        "macaulay_bijective": determinant != 0,
        "lower_forney_indices": [CHUNK, CHUNK, CHUNK],
        "lift_fold_degree": FOLD,
        "lifted_forney_indices": [LIFTED_FACTOR_DEGREE] * 3,
        "lifted_locator_degree": LIFTED_LOCATOR_DEGREE,
        "common_error_core": COMMON_CORE,
        "common_core_shortened_dimension": K - COMMON_CORE,
        "sigma_decomposition": {"quotient": SIGMA // FOLD, "remainder": SIGMA % FOLD},
        "all_lifted_indices_below_sigma": LIFTED_FACTOR_DEGREE < SIGMA,
        "fibres_used": 6 * CHUNK,
        "points_used_by_variable_pairs": 6 * CHUNK * FOLD,
        "variable_pairs": 3 * CHUNK * FOLD,
        "remaining_points_after_variable_pairs": N - 6 * CHUNK * FOLD,
        "points_consumed_by_common_pairs": 2 * COMMON_CORE,
        "unused_points": N - 6 * CHUNK * FOLD - 2 * COMMON_CORE,
        "four_flat_sum_equals_common_core_shortening": True,
        "all_four_exact_supports_compatible": False,
        "frozen_local_model_rejected": True,
        "all_pair_embeddings_rejected": False,
    }


def shifted_basis(domain: Sequence[int], excluded: frozenset[int], k: int, p: int) -> list[tuple[int, ...]]:
    loc = locator(excluded, p)
    basis: list[tuple[int, ...]] = []
    for power in range(k - len(excluded)):
        values = []
        for x in domain:
            values.append(poly_eval(loc, x, p) * pow(x, power, p) % p)
        basis.append(tuple(values))
    return basis


def incidence_equivariance_toy() -> dict[str, int]:
    p = 31
    degree = 8
    k = 4
    domain = chebyshev_roots(p, degree)
    require(len(domain) == degree and set(domain) == {-x % p for x in domain}, "toy sign domain")
    index = {x: position for position, x in enumerate(domain)}
    permutation = tuple(index[-x % p] for x in domain)
    center = tuple((7 * x * x + 3 * x + 9) % p for x in domain)
    checks = 0
    escape_checks = 0
    for mask in range(1 << len(domain)):
        excluded = frozenset(
            domain[position] for position in range(len(domain)) if mask & (1 << position)
        )
        if len(excluded) >= k:
            continue
        mirror = frozenset(-x % p for x in excluded)
        left = shifted_basis(domain, excluded, k, p)
        right = shifted_basis(domain, mirror, k, p)
        permuted_left = [tuple(row[position] for position in permutation) for row in left]
        require(rank_mod(left, p) == rank_mod(right, p), "toy dimensions")
        require(rank_mod(permuted_left + right, p) == rank_mod(right, p), "toy W transport")
        mirrored_center = tuple(center[position] for position in permutation)
        left_contained = all(sum(a * b for a, b in zip(center, row)) % p == 0 for row in left)
        right_contained = all(
            sum(a * b for a, b in zip(mirrored_center, row)) % p == 0
            for row in right
        )
        require(left_contained == right_contained, "toy containment transport")
        checks += 1
        for x in excluded:
            smaller = excluded - {x}
            smaller_mirror = mirror - {-x % p}
            left_small = shifted_basis(domain, smaller, k, p)
            right_small = shifted_basis(domain, smaller_mirror, k, p)
            left_escape = not all(
                sum(a * b for a, b in zip(center, row)) % p == 0
                for row in left_small
            )
            right_escape = not all(
                sum(a * b for a, b in zip(mirrored_center, row)) % p == 0
                for row in right_small
            )
            require(left_escape == right_escape, "toy escape transport")
            escape_checks += 1
    return {"field": p, "domain_size": degree, "containment_checks": checks, "escape_checks": escape_checks}


def build_certificate() -> dict[str, Any]:
    require(P == 2_147_483_647 and P % 4 == 3, "M31 prime shape")
    require(N == 2_097_152 and K == 1_048_576, "M31 dimensions")
    require(AGREEMENT == 1_116_023 and SIGMA == 67_447, "M31 boundary")
    require(RADIUS == 981_129 and FORBIDDEN == 2**24, "M31 forbidden size")

    q_a, q_b, q_c = quartic_covariant_coefficients(N, P)
    require((q_a, q_b, q_c) == EXPECTED_Q, "quartic covariant coefficients")
    q_delta = (q_b * q_b - 4 * q_a * q_c) % P
    q_i = (q_b * q_b + 12 * q_a * q_c) % P
    q_j = (72 * q_a * q_b * q_c - 2 * q_b**3) % P
    q_disc = (4 * q_i**3 - q_j**2) % P
    q_ratio = q_c * pow(q_a, -1, P) % P
    require(q_delta == EXPECTED_Q_DELTA and q_delta != 0, "quartic split discriminant")
    require(q_i == EXPECTED_Q_I and q_i != 0, "quartic I")
    require(q_j == EXPECTED_Q_J and q_j != 0, "quartic J")
    require(q_disc == EXPECTED_Q_DISC and q_disc != 0, "quartic discriminant")
    require(q_ratio == EXPECTED_Q_RATIO, "quartic reciprocal ratio")
    require(pow(q_ratio, (P - 1) // 2, P) == P - 1, "reciprocal ratio nonsquare")

    top = pow(2, N - 1, P)
    next_top = -N * pow(2, N - 3, P) % P
    next_bottom = -N * N * pow(2, -1, P) % P
    bottom = 1
    reciprocal_mu = pow(2, 1 - N, P)
    reciprocal_kappa_sq = pow(2 * N, -1, P)
    reciprocal_kappa_n_claim = pow(2, 2 - 2 * N, P)
    exponent_from_square = (-22 * 2**20) % 31
    exponent_from_constant = (2 - 2**22) % 31
    require((top, next_top, next_bottom, bottom) == (2, 2_146_435_071, 2_147_482_623, 1), "Chebyshev edge coefficients")
    require(pow(2, 31, P) == 1 and 2 % P != 1, "order of two is 31")
    require((exponent_from_square, exponent_from_constant) == (9, 29), "reciprocal exponent contradiction")
    require(pow(2, exponent_from_square, P) != pow(2, exponent_from_constant, P), "reciprocal candidates excluded")

    toy_31 = chebyshev_roots(31, 8)
    toy_127 = chebyshev_roots(127, 16)
    toy_31_stabilizer = mobius_stabilizer_size(toy_31, 31)
    toy_127_stabilizer = mobius_stabilizer_size(toy_127, 127)
    require((len(toy_31), toy_31_stabilizer) == (8, 6), "exceptional toy stabilizer")
    require((len(toy_127), toy_127_stabilizer) == (16, 2), "faithful toy stabilizer")

    separator = quotient_separator()
    require(separator["chunk_first"] == list(EXPECTED_QUOTIENT_CHUNK_FIRST), "quotient chunks")
    require(separator["prefix_hash"] == EXPECTED_QUOTIENT_PREFIX_HASH, "quotient prefix hash")
    require(separator["macaulay_determinant"] == EXPECTED_QUOTIENT_DETERMINANT, "quotient determinant")
    require(separator["macaulay_bijective"] is True, "quotient Macaulay bijective")
    require(separator["lifted_forney_indices"] == [33_792] * 3, "lifted Forney profile")
    require(separator["unused_points"] == 134_894, "embedding unused points")

    minimum_cross_union = 2 * (K + 1) - (K - 137)
    pair_annihilator_dimension = K - 2 * SIGMA
    pair_guard_margin = P - 2 * RADIUS
    rank16_source = 16 * SIGMA
    rank16_forced_nullity = rank16_source - (K - 1)
    require(minimum_cross_union == K + 139, "first cross-block union")
    require(pair_annihilator_dimension == 913_682, "pair annihilator")
    require(pair_guard_margin == 2_145_521_389 > 0, "pair escape union bound")
    require(15 * SIGMA == 1_011_705 < K < rank16_source, "rank-16 threshold")
    require(rank16_forced_nullity == 30_577, "rank-16 nullity")

    equivariance = incidence_equivariance_toy()

    payload: dict[str, Any] = {
        "schema": "m31-chebyshev-global-separator-v1",
        "base_commit": BASE_COMMIT,
        "status": "PROVED_STABILIZER_AND_FROZEN_FOUR_FLAT_SEPARATOR_GLOBAL_ROW_OPEN",
        "parameters": {
            "p": P,
            "n": N,
            "k": K,
            "agreement": AGREEMENT,
            "sigma": SIGMA,
            "radius": RADIUS,
            "budget": BUDGET,
            "forbidden_size": FORBIDDEN,
        },
        "standard_position_domain": {
            "torus_order": P + 1,
            "g_order": 4 * N,
            "twin_coset_subgroup_order": N,
            "domain_equals_roots_of_T_n": True,
            "domain_locator": "2^(1-n)*T_n",
            "domain_negation_invariant": True,
            "zero_not_in_domain": True,
            "byte_level_generator_pinned": False,
        },
        "quartic_covariant": {
            "definition": "(homog(T_n),homog(T_n))_(n-2)",
            "coefficients_AX4_BX2Z2_CZ4": [q_a, q_b, q_c],
            "B2_minus_4AC": q_delta,
            "I": q_i,
            "J": q_j,
            "4I3_minus_J2": q_disc,
            "C_over_A": q_ratio,
            "C_over_A_legendre": -1,
            "geometric_quartic_stabilizer": "V4",
            "reciprocal_mu": reciprocal_mu,
            "reciprocal_kappa_squared": reciprocal_kappa_sq,
            "reciprocal_kappa_n_claim": reciprocal_kappa_n_claim,
            "reciprocal_exponents_mod_31": [exponent_from_square, exponent_from_constant],
            "reciprocal_candidates_excluded_even_over_algebraic_closure": True,
        },
        "automorphism_groups": {
            "pgl2_domain_stabilizer": "C2_SIGN",
            "permutation_aut_C": "C2_SIGN",
            "permutation_aut_dual": "C2_SIGN",
            "monomial_aut_C": "F_p^* x C2_SIGN",
            "monomial_aut_dual": "F_p^* x C2_SIGN",
            "nrc_uniqueness_gate_n_ge_k_plus_2": N >= K + 2,
            "nrc_field_gate_k_lt_p": K < P,
            "diagonal_kernel_global_scalars_only": True,
            "containment_preserved": True,
            "one_point_escape_preserved": True,
            "global_line_system_preserved": True,
            "useful_orbit_compression": False,
            "maximum_support_orbit_size": 2,
        },
        "cross_support_boundary": {
            "binary_block_intersection_max": K - 137,
            "minimum_dual_support_union": minimum_cross_union,
            "minimum_union_excess_over_k": 139,
            "first_cross_block_shortening_dimension": 139,
            "plucker_coordinates": comb(139, 2),
            "wedge_coordinates": comb(139, 3),
            "pairwise_exact_support_survives": True,
            "pair_annihilator_dimension": pair_annihilator_dimension,
            "pair_escape_guards": 2 * RADIUS,
            "pair_union_bound_margin": pair_guard_margin,
            "containment_only_first_possible_flat_count": 16,
            "rank15_source_dimension": 15 * SIGMA,
            "rank16_source_dimension": rank16_source,
            "rank16_target_dimension": K,
            "rank16_common_syndrome_nullity_floor": rank16_forced_nullity,
            "rank16_forney_gate": SIGMA + 1,
            "escape_aware_counts_3_through_15": "OPEN",
        },
        "fibre_aligned_four_flat_separator": separator,
        "toy_controls": {
            "exceptional_field": 31,
            "exceptional_degree": 8,
            "exceptional_stabilizer_size": toy_31_stabilizer,
            "faithful_field": 127,
            "faithful_degree": 16,
            "faithful_stabilizer_size": toy_127_stabilizer,
            "incidence_equivariance": equivariance,
        },
        "ledger": {
            "prime_field_row_closed": False,
            "quartic_field_row_closed": False,
            "U_Q": None,
            "U_A": None,
            "ledger_movement": 0,
            "prize_claimed": False,
        },
        "provenance": {
            "parent_pr": 1001,
            "parent_head": BASE_COMMIT,
            "domain_source": "tex/cs25_cap_v13_2.tex:4031-4036",
            "nrc_primary_source": "arXiv:1611.04341, Lemma 2.9 and Theorem 2.10",
            "rational_chebyshev_comparison": "arXiv:2101.00348, Theorem 1.3",
            "rank16_source": "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
        },
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS
        },
    }
    return seal_certificate(payload)


def validate_certificate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    verify_self_hash(candidate)
    require(candidate == expected, "canonical certificate payload")
    require(candidate["ledger"]["ledger_movement"] == 0, "zero ledger movement")
    require(candidate["ledger"]["prime_field_row_closed"] is False, "prime row open")
    require(candidate["ledger"]["quartic_field_row_closed"] is False, "quartic row open")
    require(candidate["fibre_aligned_four_flat_separator"]["all_pair_embeddings_rejected"] is False, "embedding scope guard")
    require(candidate["automorphism_groups"]["useful_orbit_compression"] is False, "orbit route cut")


def set_path(payload: dict[str, Any], path: Sequence[str], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations: tuple[tuple[tuple[str, ...], Any], ...] = (
        (("base_commit",), "0" * 40),
        (("parameters", "sigma"), SIGMA + 1),
        (("standard_position_domain", "g_order"), 2 * N),
        (("standard_position_domain", "domain_equals_roots_of_T_n"), False),
        (("quartic_covariant", "coefficients_AX4_BX2Z2_CZ4"), [1, 2, 3]),
        (("quartic_covariant", "I"), 0),
        (("quartic_covariant", "J"), 0),
        (("quartic_covariant", "C_over_A_legendre"), 1),
        (("quartic_covariant", "reciprocal_candidates_excluded_even_over_algebraic_closure"), False),
        (("automorphism_groups", "pgl2_domain_stabilizer"), "DIHEDRAL"),
        (("automorphism_groups", "maximum_support_orbit_size"), 4),
        (("automorphism_groups", "containment_preserved"), False),
        (("cross_support_boundary", "pairwise_exact_support_survives"), False),
        (("cross_support_boundary", "minimum_union_excess_over_k"), 138),
        (("cross_support_boundary", "containment_only_first_possible_flat_count"), 15),
        (("cross_support_boundary", "rank16_common_syndrome_nullity_floor"), 30_576),
        (("fibre_aligned_four_flat_separator", "macaulay_determinant"), 0),
        (("fibre_aligned_four_flat_separator", "macaulay_bijective"), False),
        (("fibre_aligned_four_flat_separator", "lifted_forney_indices"), [67_448, 0, 0]),
        (("fibre_aligned_four_flat_separator", "common_error_core"), COMMON_CORE - 1),
        (("fibre_aligned_four_flat_separator", "frozen_local_model_rejected"), False),
        (("fibre_aligned_four_flat_separator", "all_pair_embeddings_rejected"), True),
        (("toy_controls", "exceptional_stabilizer_size"), 2),
        (("ledger", "ledger_movement"), 1),
        (("ledger", "prime_field_row_closed"), True),
        (("ledger", "U_Q"), 0),
        (("provenance", "parent_pr"), 1000),
        (
            (
                "source_sha256",
                "experimental/scripts/verify_m31_chebyshev_global_separator.py",
            ),
            "0" * 64,
        ),
    )
    rejected = 0
    for path, value in mutations:
        mutated = copy.deepcopy(expected)
        set_path(mutated, path, value)
        mutated = seal_certificate(mutated)
        try:
            validate_certificate(mutated, expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {'.'.join(path)}")

    # Exercise the self-hash failure path separately from the resealed semantic
    # mutations above.
    raw_hash_corruption = copy.deepcopy(expected)
    raw_hash_corruption["certificate_sha256"] = "0" * 64
    raw_payload_corruption = copy.deepcopy(expected)
    raw_payload_corruption["parameters"]["sigma"] = SIGMA + 1
    for label, mutated in (
        ("raw certificate hash", raw_hash_corruption),
        ("raw payload", raw_payload_corruption),
    ):
        try:
            validate_certificate(mutated, expected)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")

    require(rejected == len(mutations) + 2, "all tampers rejected")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="compare with the pinned manifest")
    parser.add_argument("--print-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build_certificate()
    if args.print_certificate:
        print(json.dumps(expected, indent=2, sort_keys=True))
        return
    if args.tamper_selftest:
        rejected = tamper_selftest(expected)
        print(f"m31 Chebyshev global-separator tampers: {rejected}/{rejected} rejected PASS")
        return

    require(CERTIFICATE_PATH.exists(), "pinned manifest exists")
    pinned = json.loads(CERTIFICATE_PATH.read_text())
    validate_certificate(pinned, expected)
    print(f"m31 Chebyshev global separator: {CHECKS} exact checks PASS")
    print(
        "quartic covariant: "
        f"A={EXPECTED_Q[0]} B={EXPECTED_Q[1]} C={EXPECTED_Q[2]} "
        "PGL2 stabilizer=C2 PASS"
    )
    print(
        "quotient Macaulay: "
        f"132x132 det={EXPECTED_QUOTIENT_DETERMINANT} "
        "lifted Forney=(33792,33792,33792) PASS"
    )
    print("pairwise exact-support survivor: PASS; first containment gate: rank 16")
    print("frozen four-flat local model: REJECTED BY GLOBAL SEPARATOR")
    print("M31 list row: OPEN; U_Q/U_A: null; ledger movement: 0")


if __name__ == "__main__":
    main()
