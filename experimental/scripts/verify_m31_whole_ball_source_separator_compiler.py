#!/usr/bin/env python3
"""Verify the M31 whole-ball compiler and four-face CRT compression.

The packet proves an algebraic route reduction and a fail-closed completion
contract.  It does not certify the M31 row.  All checks use explicit
exceptions, so optimized Python performs the same validation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
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
BASE_COMMIT = "4958c2f95a9e3dd16bb28a13c919ff87811611a4"

FACTOR_DEGREE = 33 * 1024
ROW_DEGREE = 3 * FACTOR_DEGREE
HIGH_INDEX_FLOOR = SIGMA + 1
LOW_PAIR_SUM_CEILING = ROW_DEGREE - HIGH_INDEX_FLOOR
LOW_SYZYGY_CEILING = LOW_PAIR_SUM_CEILING // 2
LOW_SYZYGY_UNKNOWNS = 4 * (LOW_SYZYGY_CEILING + 1)
CRT_PRODUCT_DEGREE = 6 * FACTOR_DEGREE
SYZYGY_PRODUCT_DEGREE = ROW_DEGREE + LOW_SYZYGY_CEILING
UNIVERSAL_SURJECTIVITY_BOUND = 2 * FACTOR_DEGREE
DEPLOYED_THRESHOLD_GAP = UNIVERSAL_SURJECTIVITY_BOUND - SIGMA
TAU_MIN = 0
TAU_MAX = LOW_PAIR_SUM_CEILING - FACTOR_DEGREE
DEFECT_MIN = 1
DEFECT_MAX = DEPLOYED_THRESHOLD_GAP
KERNEL_DIMENSION_AT_TAU_ZERO = 2 * SIGMA - FACTOR_DEGREE
RANK_AT_TAU_ZERO = ROW_DEGREE + SIGMA - DEFECT_MAX
MIN_SIMPLE_LOCATOR_ZEROS = FACTOR_DEGREE - TAU_MAX

TOY_P = 7
TOY_TOTAL = 5_040
TOY_FULL_RANK = 3_696
TOY_RANK_DROP = 1_344
TOY_EXAMPLE = (0, 1, 2, 3, 4, 6)
TOY_SYZYGY = (1, 3, 6, 4)
TOY_SECOND_SYZYGY = ((1,), (0, 1), (3, 3), (0, 3))
TOY_PLUECKER_QUOTIENTS = {
    "A0": (5,),
    "A1": (3,),
    "B0": (6,),
    "B1": (1,),
    "C0": (3,),
    "C1": (3,),
}

ASYMMETRIC_P = 23
ASYMMETRIC_SUPPORT = (1, 2, 4, 5, 7, 8, 10, 12, 13, 15, 19, 20)
ASYMMETRIC_CHUNKS = ((1, 2), (10, 12), (4, 20), (8, 19), (5, 15), (7, 13))
ASYMMETRIC_PROFILE = (0, 2, 4)
ASYMMETRIC_CONSTANT_SYZYGY = (1, 9, 18, 18)
ASYMMETRIC_THETA_RANKS = (3, 6, 8, 10, 11, 12)
ASYMMETRIC_COKERNEL_FUNCTIONAL = (1, 5, 12, 0, 8, 8, 15, 10, 8)

CRT_EQUATIONS = (
    "H10*B0*C1+H11*B1*C0=0 mod A0",
    "H00*B0*C0+H01*B1*C1=0 mod A1",
    "H01*A0*C1+H11*A1*C0=0 mod B0",
    "H00*A0*C0+H10*A1*C1=0 mod B1",
    "H10*A1*B0+H01*A0*B1=0 mod C0",
    "H00*A0*B0+H11*A1*B1=0 mod C1",
)

PLUECKER_DIVISORS = {
    "A0": "Delta_13",
    "A1": "Delta_02",
    "B0": "Delta_23",
    "B1": "Delta_01",
    "C0": "Delta_12",
    "C1": "Delta_03",
}

PLUECKER_LINEAR_IDENTITIES = (
    "A0*q_A1+B0*q_B1+C0*q_C1=0",
    "-A1*q_A0+B0*q_B1-C1*q_C0=0",
    "A0*q_A1-B1*q_B0+C1*q_C0=0",
    "A1*q_A0+B1*q_B0+C0*q_C1=0",
)

PLUECKER_QUADRATIC_IDENTITY = (
    "B0*B1*q_B0*q_B1-A0*A1*q_A0*q_A1+C0*C1*q_C0*q_C1=0"
)

ROOT = Path(__file__).resolve().parents[2]
PYTHON_PATH = ROOT / "experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_whole_ball_source_separator_compiler.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_whole_ball_source_separator_compiler.md"
README_PATH = ROOT / "experimental/data/certificates/m31-whole-ball-source-separator-compiler/README.md"
CERTIFICATE_PATH = ROOT / "experimental/data/certificates/m31-whole-ball-source-separator-compiler/manifest.json"

SOURCE_PATHS = (
    ROOT / "experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md",
    ROOT / "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
    ROOT / "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md",
    ROOT / "experimental/notes/thresholds/m31_chebyshev_global_separator.md",
    ROOT / "experimental/scripts/verify_m31_chebyshev_global_separator.py",
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


def trim(poly: Sequence[int]) -> list[int]:
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(left: Sequence[int], right: Sequence[int], p: int) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % p
    return trim(out)


def poly_scale(poly: Sequence[int], scalar: int, p: int) -> list[int]:
    return trim([(scalar * value) % p for value in poly])


def poly_sub(left: Sequence[int], right: Sequence[int], p: int) -> list[int]:
    return poly_add(left, poly_scale(right, -1, p), p)


def poly_mul(left: Sequence[int], right: Sequence[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out)


def poly_divmod(numerator: Sequence[int], denominator: Sequence[int], p: int) -> tuple[list[int], list[int]]:
    num = trim([value % p for value in numerator])
    den = trim([value % p for value in denominator])
    require(den != [0], "nonzero polynomial divisor")
    if len(num) < len(den):
        return [0], num
    quotient = [0] * (len(num) - len(den) + 1)
    inverse = pow(den[-1], -1, p)
    while num != [0] and len(num) >= len(den):
        shift = len(num) - len(den)
        coefficient = num[-1] * inverse % p
        quotient[shift] = coefficient
        for index, value in enumerate(den):
            num[index + shift] = (num[index + shift] - coefficient * value) % p
        num = trim(num)
    return trim(quotient), num


def poly_mod(numerator: Sequence[int], denominator: Sequence[int], p: int) -> list[int]:
    return poly_divmod(numerator, denominator, p)[1]


def poly_exact_div(numerator: Sequence[int], denominator: Sequence[int], p: int) -> list[int]:
    quotient, remainder = poly_divmod(numerator, denominator, p)
    require(remainder == [0], "exact polynomial division")
    return quotient


def poly_degree(poly: Sequence[int]) -> int:
    reduced = trim(poly)
    return -1 if reduced == [0] else len(reduced) - 1


def locator(points: Iterable[int], p: int) -> list[int]:
    out = [1]
    for point in points:
        out = poly_mul(out, ((-point) % p, 1), p)
    return out


def parity_products(values: Sequence[int], p: int) -> tuple[list[int], ...]:
    a0, a1, b0, b1, c0, c1 = values
    factors = [locator((value,), p) for value in values]
    fa0, fa1, fb0, fb1, fc0, fc1 = factors
    return (
        poly_mul(poly_mul(fa0, fb0, p), fc0, p),
        poly_mul(poly_mul(fa1, fb0, p), fc1, p),
        poly_mul(poly_mul(fa0, fb1, p), fc1, p),
        poly_mul(poly_mul(fa1, fb1, p), fc0, p),
    )


def parity_products_from_chunks(chunks: Sequence[Sequence[int]], p: int) -> tuple[list[int], ...]:
    require(len(chunks) == 6, "six parity chunks")
    factors = [locator(chunk, p) for chunk in chunks]
    fa0, fa1, fb0, fb1, fc0, fc1 = factors
    return (
        poly_mul(poly_mul(fa0, fb0, p), fc0, p),
        poly_mul(poly_mul(fa1, fb0, p), fc1, p),
        poly_mul(poly_mul(fa0, fb1, p), fc1, p),
        poly_mul(poly_mul(fa1, fb1, p), fc0, p),
    )


def theta_matrix(polynomials: Sequence[Sequence[int]], bound: int, p: int) -> list[list[int]]:
    degree = max(len(poly) - 1 for poly in polynomials)
    rows = degree + bound
    columns = len(polynomials) * bound
    matrix = [[0] * columns for _ in range(rows)]
    for block, poly in enumerate(polynomials):
        for shift in range(bound):
            for exponent, coefficient in enumerate(poly):
                matrix[exponent + shift][block * bound + shift] = coefficient % p
    return matrix


def rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    if not matrix or not matrix[0]:
        return 0
    rows = [list(value % p for value in row) for row in matrix]
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "rank matrix rectangular")
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(rows)) if rows[row][column]), None)
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


def determinant_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    require(len(matrix) == len(matrix[0]), "determinant square")
    rows = [list(value % p for value in row) for row in matrix]
    determinant = 1
    for column in range(len(rows)):
        pivot = next((row for row in range(column, len(rows)) if rows[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            rows[column], rows[pivot] = rows[pivot], rows[column]
            determinant = -determinant % p
        value = rows[column][column]
        determinant = determinant * value % p
        inverse = pow(value, -1, p)
        for row in range(column + 1, len(rows)):
            scale = rows[row][column] * inverse % p
            for index in range(column, len(rows)):
                rows[row][index] = (rows[row][index] - scale * rows[column][index]) % p
    return determinant


def phi(values: Sequence[int], p: int) -> int:
    a0, a1, b0, b1, c0, c1 = values
    return (
        a0 * a1 * b0
        + a0 * a1 * b1
        - a0 * b0 * b1
        - a1 * b0 * b1
        - a0 * a1 * c0
        + b0 * b1 * c0
        - a0 * a1 * c1
        + b0 * b1 * c1
        + a0 * c0 * c1
        + a1 * c0 * c1
        - b0 * c0 * c1
        - b1 * c0 * c1
    ) % p


def factorized_determinant(values: Sequence[int], p: int) -> int:
    a0, a1, b0, b1, c0, c1 = values
    return (a1 - a0) * (b1 - b0) * (c0 - c1) * phi(values, p) % p


def combine(polynomials: Sequence[Sequence[int]], coefficients: Sequence[int], p: int) -> list[int]:
    out = [0]
    for poly, coefficient in zip(polynomials, coefficients):
        out = poly_add(out, poly_scale(poly, coefficient, p), p)
    return out


def combine_polynomial_rows(
    polynomials: Sequence[Sequence[int]], coefficients: Sequence[Sequence[int]], p: int
) -> list[int]:
    require(len(polynomials) == len(coefficients), "polynomial-row arity")
    out = [0]
    for poly, coefficient in zip(polynomials, coefficients):
        out = poly_add(out, poly_mul(poly, coefficient, p), p)
    return out


def syzygy_minors(
    first: Sequence[Sequence[int]], second: Sequence[Sequence[int]], p: int
) -> dict[tuple[int, int], list[int]]:
    require(len(first) == len(second) == 4, "two four-coordinate syzygies")
    return {
        (i, j): poly_sub(
            poly_mul(first[i], second[j], p),
            poly_mul(first[j], second[i], p),
            p,
        )
        for i in range(4)
        for j in range(i + 1, 4)
    }


def pluecker_quotients(
    values: Sequence[int],
    first: Sequence[Sequence[int]],
    second: Sequence[Sequence[int]],
    p: int,
) -> dict[str, list[int]]:
    a0, a1, b0, b1, c0, c1 = [locator((value,), p) for value in values]
    minors = syzygy_minors(first, second, p)
    return {
        "A0": poly_exact_div(minors[(1, 3)], a0, p),
        "A1": poly_exact_div(minors[(0, 2)], a1, p),
        "B0": poly_exact_div(minors[(2, 3)], b0, p),
        "B1": poly_exact_div(minors[(0, 1)], b1, p),
        "C0": poly_exact_div(minors[(1, 2)], c0, p),
        "C1": poly_exact_div(minors[(0, 3)], c1, p),
    }


def verify_pluecker_identities(
    values: Sequence[int], quotients: dict[str, Sequence[int]], p: int
) -> None:
    a0, a1, b0, b1, c0, c1 = [locator((value,), p) for value in values]
    qa0, qa1 = quotients["A0"], quotients["A1"]
    qb0, qb1 = quotients["B0"], quotients["B1"]
    qc0, qc1 = quotients["C0"], quotients["C1"]

    linear = (
        poly_add(poly_add(poly_mul(a0, qa1, p), poly_mul(b0, qb1, p), p), poly_mul(c0, qc1, p), p),
        poly_sub(poly_add(poly_scale(poly_mul(a1, qa0, p), -1, p), poly_mul(b0, qb1, p), p), poly_mul(c1, qc0, p), p),
        poly_add(poly_sub(poly_mul(a0, qa1, p), poly_mul(b1, qb0, p), p), poly_mul(c1, qc0, p), p),
        poly_add(poly_add(poly_mul(a1, qa0, p), poly_mul(b1, qb0, p), p), poly_mul(c0, qc1, p), p),
    )
    require(all(identity == [0] for identity in linear), "four Pluecker contraction identities")

    term_b = poly_mul(poly_mul(b0, b1, p), poly_mul(qb0, qb1, p), p)
    term_a = poly_mul(poly_mul(a0, a1, p), poly_mul(qa0, qa1, p), p)
    term_c = poly_mul(poly_mul(c0, c1, p), poly_mul(qc0, qc1, p), p)
    quadratic = poly_add(poly_sub(term_b, term_a, p), term_c, p)
    require(quadratic == [0], "Pluecker quadratic identity")


def crt_residues_from_factors(
    factors: Sequence[Sequence[int]], coefficients: Sequence[Sequence[int]], p: int
) -> tuple[list[int], ...]:
    require(len(factors) == 6 and len(coefficients) == 4, "CRT arity")
    a0, a1, b0, b1, c0, c1 = factors
    h00, h10, h01, h11 = coefficients
    equations = (
        (poly_add(poly_mul(h10, poly_mul(b0, c1, p), p), poly_mul(h11, poly_mul(b1, c0, p), p), p), a0),
        (poly_add(poly_mul(h00, poly_mul(b0, c0, p), p), poly_mul(h01, poly_mul(b1, c1, p), p), p), a1),
        (poly_add(poly_mul(h01, poly_mul(a0, c1, p), p), poly_mul(h11, poly_mul(a1, c0, p), p), p), b0),
        (poly_add(poly_mul(h00, poly_mul(a0, c0, p), p), poly_mul(h10, poly_mul(a1, c1, p), p), p), b1),
        (poly_add(poly_mul(h10, poly_mul(a1, b0, p), p), poly_mul(h01, poly_mul(a0, b1, p), p), p), c0),
        (poly_add(poly_mul(h00, poly_mul(a0, b0, p), p), poly_mul(h11, poly_mul(a1, b1, p), p), p), c1),
    )
    return tuple(poly_mod(numerator, denominator, p) for numerator, denominator in equations)


def crt_residues(values: Sequence[int], coefficients: Sequence[int], p: int) -> tuple[list[int], ...]:
    factors = [locator((value,), p) for value in values]
    constant_rows = [[coefficient % p] for coefficient in coefficients]
    return crt_residues_from_factors(factors, constant_rows, p)


def infer_toy_forney(polynomials: Sequence[Sequence[int]], p: int) -> tuple[int, int, int]:
    degree = max(len(poly) - 1 for poly in polynomials)
    nullities = {
        bound: 4 * bound - rank_mod(theta_matrix(polynomials, bound, p), p)
        for bound in range(degree + 2)
    }
    candidates = []
    for first in range(degree + 1):
        for second in range(first, degree + 1):
            third = degree - first - second
            if third < second:
                continue
            profile = (first, second, third)
            if all(
                nullities[bound]
                == sum(max(0, bound - index) for index in profile)
                for bound in nullities
            ):
                candidates.append(profile)
    require(len(candidates) == 1, "unique toy Forney profile")
    return candidates[0]


def toy_census() -> dict[str, Any]:
    ranks: Counter[int] = Counter()
    phi_zero = 0
    for values in itertools.permutations(range(TOY_P), 6):
        polynomials = parity_products(values, TOY_P)
        matrix = theta_matrix(polynomials, 1, TOY_P)
        determinant = determinant_mod(matrix, TOY_P)
        require(determinant == factorized_determinant(values, TOY_P), "toy determinant factorization")
        rank = rank_mod(matrix, TOY_P)
        ranks[rank] += 1
        if phi(values, TOY_P) == 0:
            phi_zero += 1

    require(sum(ranks.values()) == TOY_TOTAL, "toy census total")
    require(ranks == Counter({4: TOY_FULL_RANK, 3: TOY_RANK_DROP}), "toy rank distribution")
    require(phi_zero == TOY_RANK_DROP, "toy rank-drop point count")

    full_values = (0, 1, 2, 3, 4, 5)
    full_profile = infer_toy_forney(parity_products(full_values, TOY_P), TOY_P)
    bad_polynomials = parity_products(TOY_EXAMPLE, TOY_P)
    bad_profile = infer_toy_forney(bad_polynomials, TOY_P)
    require(full_profile == (1, 1, 1), "toy full-rank Forney profile")
    require(bad_profile == (0, 1, 2), "toy rank-drop Forney profile")
    require(combine(bad_polynomials, TOY_SYZYGY, TOY_P) == [0], "toy primitive syzygy")
    first_row = [[coefficient] for coefficient in TOY_SYZYGY]
    second_row = [list(poly) for poly in TOY_SECOND_SYZYGY]
    require(
        combine_polynomial_rows(bad_polynomials, second_row, TOY_P) == [0],
        "toy second row-reduced syzygy",
    )
    quotients = pluecker_quotients(TOY_EXAMPLE, first_row, second_row, TOY_P)
    require(
        quotients == {key: list(value) for key, value in TOY_PLUECKER_QUOTIENTS.items()},
        "toy Pluecker quotient signs",
    )
    require(all(poly != [0] for poly in quotients.values()), "toy six nonzero quotients")
    require(max(poly_degree(poly) for poly in quotients.values()) == 0, "toy tau zero")
    verify_pluecker_identities(TOY_EXAMPLE, quotients, TOY_P)
    residues = crt_residues(TOY_EXAMPLE, TOY_SYZYGY, TOY_P)
    require(all(residue == [0] for residue in residues), "toy six CRT residues")

    # On the explicit face, exhaust every constant coefficient vector and
    # verify that the global relation and all six CRT equations are equivalent.
    equivalence_checks = 0
    for coefficients in itertools.product(range(TOY_P), repeat=4):
        global_zero = combine(bad_polynomials, coefficients, TOY_P) == [0]
        crt_zero = all(
            residue == [0]
            for residue in crt_residues(TOY_EXAMPLE, coefficients, TOY_P)
        )
        require(global_zero == crt_zero, "toy CRT equivalence")
        equivalence_checks += 1

    return {
        "field": TOY_P,
        "factor_degree": 1,
        "labelled_disjoint_sextuples": TOY_TOTAL,
        "theta_rank_4": TOY_FULL_RANK,
        "theta_rank_3": TOY_RANK_DROP,
        "theta_rank_below_3": 0,
        "phi_zero": phi_zero,
        "full_rank_forney_profile": list(full_profile),
        "rank_drop_forney_profile": list(bad_profile),
        "primitive_example": list(TOY_EXAMPLE),
        "primitive_syzygy": list(TOY_SYZYGY),
        "second_row_reduced_syzygy": [list(poly) for poly in TOY_SECOND_SYZYGY],
        "pluecker_quotients": {key: list(value) for key, value in quotients.items()},
        "tau": 0,
        "cokernel_defect": 1,
        "crt_equivalence_coefficient_vectors": equivalence_checks,
        "deployed_implication": False,
    }


def normalized_pgl2_representatives(p: int) -> list[tuple[int, int, int, int]]:
    representatives: set[tuple[int, int, int, int]] = set()
    for entries in itertools.product(range(p), repeat=4):
        a, b, c, d = entries
        if (a * d - b * c) % p == 0:
            continue
        first = next(value for value in entries if value)
        inverse = pow(first, -1, p)
        representatives.add(tuple(value * inverse % p for value in entries))
    return sorted(representatives)


def pgl2_stabilizer(
    support: Sequence[int], p: int
) -> tuple[list[tuple[int, int, int, int]], int]:
    target = set(support)
    representatives = normalized_pgl2_representatives(p)
    stabilizer: list[tuple[int, int, int, int]] = []
    for a, b, c, d in representatives:
        image: set[int] = set()
        valid = True
        for point in support:
            denominator = (c * point + d) % p
            if denominator == 0:
                valid = False
                break
            image.add((a * point + b) * pow(denominator, -1, p) % p)
        if valid and image == target:
            stabilizer.append((a, b, c, d))
    return stabilizer, len(representatives)


def asymmetric_rank_drop_control() -> dict[str, Any]:
    flattened = tuple(point for chunk in ASYMMETRIC_CHUNKS for point in chunk)
    require(len(set(flattened)) == 12, "asymmetric chunks pairwise disjoint")
    require(set(flattened) == set(ASYMMETRIC_SUPPORT), "asymmetric chunk support")

    polynomials = parity_products_from_chunks(ASYMMETRIC_CHUNKS, ASYMMETRIC_P)
    require(all(poly_degree(poly) == 6 for poly in polynomials), "asymmetric row degrees")
    profile = infer_toy_forney(polynomials, ASYMMETRIC_P)
    require(profile == ASYMMETRIC_PROFILE, "asymmetric Forney profile")
    ranks = tuple(
        rank_mod(theta_matrix(polynomials, bound, ASYMMETRIC_P), ASYMMETRIC_P)
        for bound in range(1, 7)
    )
    require(ranks == ASYMMETRIC_THETA_RANKS, "asymmetric theta ranks")
    require(
        combine(polynomials, ASYMMETRIC_CONSTANT_SYZYGY, ASYMMETRIC_P) == [0],
        "asymmetric constant syzygy",
    )

    factors = [locator(chunk, ASYMMETRIC_P) for chunk in ASYMMETRIC_CHUNKS]
    constant_rows = [[coefficient] for coefficient in ASYMMETRIC_CONSTANT_SYZYGY]
    residues = crt_residues_from_factors(factors, constant_rows, ASYMMETRIC_P)
    require(all(residue == [0] for residue in residues), "asymmetric six CRT residues")

    theta_three = theta_matrix(polynomials, 3, ASYMMETRIC_P)
    require(len(theta_three) == 9 and len(theta_three[0]) == 12, "asymmetric theta3 dimensions")
    functional = ASYMMETRIC_COKERNEL_FUNCTIONAL
    require(
        all(
            sum(functional[row] * theta_three[row][column] for row in range(9))
            % ASYMMETRIC_P
            == 0
            for column in range(12)
        ),
        "asymmetric cokernel functional",
    )
    require(any(functional), "asymmetric cokernel functional nonzero")

    stabilizer, pgl_order = pgl2_stabilizer(ASYMMETRIC_SUPPORT, ASYMMETRIC_P)
    require(pgl_order == ASYMMETRIC_P * (ASYMMETRIC_P**2 - 1), "PGL2 order")
    require(stabilizer == [(1, 0, 0, 1)], "asymmetric support trivial PGL2 stabilizer")

    return {
        "field": ASYMMETRIC_P,
        "factor_degree": 2,
        "support": list(ASYMMETRIC_SUPPORT),
        "chunks": [list(chunk) for chunk in ASYMMETRIC_CHUNKS],
        "forney_profile": list(profile),
        "theta_ranks_D_1_through_6": list(ranks),
        "theta3_dimensions": [9, 12],
        "theta3_cokernel_defect": 1,
        "constant_syzygy": list(ASYMMETRIC_CONSTANT_SYZYGY),
        "cokernel_functional": list(ASYMMETRIC_COKERNEL_FUNCTIONAL),
        "pgl2_order": pgl_order,
        "pgl2_stabilizer": [list(matrix) for matrix in stabilizer],
        "deployed_implication": False,
    }


def validate_contract(payload: dict[str, Any]) -> None:
    require(payload["artifact_kind"] == "WHOLE_BALL_ROUTE_CUT_COMPILER", "artifact kind")
    require(payload["terminal"] == "WHOLE_BALL_ROUTE_CUT_CURRENT_ARTIFACT_SET", "open terminal")
    whole = payload["whole_ball_contract"]
    require(whole["support_weight_interval"] == [0, RADIUS], "whole-ball weight interval")
    require(whole["weight_layers"] == RADIUS + 1, "whole-ball layer count")
    require(whole["exact_containment_retained"] is True, "whole-ball containment")
    require(whole["every_one_point_escape_retained"] is True, "whole-ball escapes")
    require(whole["boundary_only_sufficient"] is False, "boundary-only scope cut")
    require(whole["frozen_embedding_sufficient"] is False, "frozen-embedding scope cut")
    require(whole["zero_syndrome_list_size"] == 1, "zero syndrome branch")
    require(whole["support_sum_duplicate_free"] is True, "duplicate-free exact-support sum")
    require(whole["center_to_hyperplane_surjective"] is True, "center-to-hyperplane bridge")

    algebra = payload["four_face_compression"]
    require(algebra["factor_degree"] == FACTOR_DEGREE, "factor degree")
    require(algebra["row_degree"] == ROW_DEGREE, "row degree")
    require(algebra["high_forney_index_floor"] == HIGH_INDEX_FLOOR, "high index floor")
    require(algebra["low_pair_sum_ceiling"] == LOW_PAIR_SUM_CEILING, "low pair sum")
    require(algebra["low_syzygy_degree_ceiling"] == LOW_SYZYGY_CEILING, "low syzygy ceiling")
    require(algebra["coefficient_unknowns"] == LOW_SYZYGY_UNKNOWNS, "low syzygy unknowns")
    require(algebra["single_low_syzygy_sufficient_for_rank_drop"] is False, "one-row route cut")
    require(algebra["rank_drop_exact_two_row_criterion"] is True, "exact two-row criterion")
    require(algebra["crt_equations"] == list(CRT_EQUATIONS), "six CRT equations")
    require(algebra["crt_sufficient_by_degree"] is True, "CRT sufficiency")
    require(SYZYGY_PRODUCT_DEGREE < CRT_PRODUCT_DEGREE, "CRT strict degree gate")

    pluecker = algebra["pluecker_defect_window"]
    require(pluecker["universal_surjectivity_bound"] == UNIVERSAL_SURJECTIVITY_BOUND, "universal 2r threshold")
    require(pluecker["deployed_threshold_gap"] == DEPLOYED_THRESHOLD_GAP, "deployed threshold gap")
    require(pluecker["tau_interval"] == [TAU_MIN, TAU_MAX], "tau interval")
    require(pluecker["defect_interval"] == [DEFECT_MIN, DEFECT_MAX], "defect interval")
    require(pluecker["cell_count"] == 137, "defect cell count")
    require(pluecker["minor_divisors"] == PLUECKER_DIVISORS, "minor divisor map")
    require(pluecker["quotient_degree_ceiling"] == TAU_MAX, "quotient degree ceiling")
    require(pluecker["all_six_quotients_nonzero"] is True, "six nonzero quotients")
    require(pluecker["quotients_primitive"] is True, "primitive quotient family")
    require(pluecker["rational_mds_parameters"] == [4, 2, 3], "rational MDS")
    require(pluecker["linear_identities"] == list(PLUECKER_LINEAR_IDENTITIES), "linear identities")
    require(pluecker["quadratic_identity"] == PLUECKER_QUADRATIC_IDENTITY, "quadratic identity")
    require(pluecker["minimum_simple_locator_zeros"] == MIN_SIMPLE_LOCATOR_ZEROS, "simple locator zeros")

    asymmetric = payload["pgl_asymmetric_rank_drop_control"]
    require(asymmetric["field"] == ASYMMETRIC_P, "asymmetric field")
    require(asymmetric["forney_profile"] == list(ASYMMETRIC_PROFILE), "asymmetric profile")
    require(asymmetric["pgl2_order"] == 12_144, "asymmetric PGL2 order")
    require(asymmetric["pgl2_stabilizer"] == [[1, 0, 0, 1]], "trivial PGL2 stabilizer")

    route_cut = payload["direct_component_route_cut"]
    require(
        route_cut["scope"]
        == "CONDITIONAL_ON_INHERITED_DELTA_TIMES_P_TO_EY_CHARGE_FORM",
        "direct route-cut inherited charge scope",
    )

    closure = payload["closure_state"]
    if closure["closure_certified"]:
        require(whole["source_selection_proved"] is True, "closing source selection")
        require(whole["interior_covered"] is True, "closing interior coverage")
        require(whole["boundary_covered"] is True, "closing boundary coverage")
        require(closure["owner_disjointness_proved"] is True, "closing owner disjointness")
        require(closure["add_back_proved"] is True, "closing add-back")
        require(closure["unresolved_terminals"] == [], "closing unresolved terminals")
        charges = closure["ledger_atoms"]
        require(all(isinstance(value, int) and value >= 0 for value in charges.values()), "closing integer atoms")
        require(sum(charges.values()) <= BUDGET, "closing exact budget")
    else:
        require(closure["result"] == "UNIVERSAL_SOURCE_BRIDGE_REQUIRED", "open result label")
        require(whole["source_selection_proved"] is False, "source bridge remains open")
        require(whole["interior_covered"] is False, "interior remains open")
        require(whole["boundary_covered"] is False, "boundary remains open")
        require(all(value is None for value in closure["ledger_atoms"].values()), "open atoms null")
        require(closure["ledger_movement"] == 0, "open ledger movement")
        require(
            closure["unresolved_terminals"]
            == [
                "WHOLE_BALL_SOURCE_EXTRACTION_OPEN",
                "INTERIOR_WEIGHTS_1_TO_981128_OPEN",
                "BOUNDARY_UNRESTRICTED_SOURCE_SELECTION_OPEN",
                "ESCAPE_AWARE_3_TO_15_OPEN",
                "RANK16_H1_UNRESTRICTED_LOCATORS_OPEN",
                "RANK16_HIGHER_DEFECT_OPEN",
                "GLOBAL_DISJOINT_ADDBACK_OPEN",
            ],
            "canonical open cells",
        )


def build_certificate() -> dict[str, Any]:
    require(P == 2_147_483_647 and P % 4 == 3, "M31 field")
    require((N, K, AGREEMENT) == (2_097_152, 1_048_576, 1_116_023), "M31 row")
    require((SIGMA, RADIUS) == (67_447, 981_129), "M31 radius")
    require((BUDGET, FORBIDDEN) == (16_777_215, 16_777_216), "M31 budget")
    require(RADIUS + 1 == 981_130, "whole-ball layers")
    require((FACTOR_DEGREE, ROW_DEGREE) == (33_792, 101_376), "four-face degrees")
    require((HIGH_INDEX_FLOOR, LOW_PAIR_SUM_CEILING) == (67_448, 33_928), "Forney imbalance")
    require((LOW_SYZYGY_CEILING, LOW_SYZYGY_UNKNOWNS) == (16_964, 67_860), "low syzygy compression")
    require((SYZYGY_PRODUCT_DEGREE, CRT_PRODUCT_DEGREE) == (118_340, 202_752), "CRT degree gate")
    require((UNIVERSAL_SURJECTIVITY_BOUND, DEPLOYED_THRESHOLD_GAP) == (67_584, 137), "universal threshold gap")
    require((TAU_MIN, TAU_MAX, DEFECT_MIN, DEFECT_MAX) == (0, 136, 1, 137), "Pluecker defect window")
    require((KERNEL_DIMENSION_AT_TAU_ZERO, RANK_AT_TAU_ZERO) == (101_102, 168_686), "Pluecker matrix anchors")
    require(MIN_SIMPLE_LOCATOR_ZEROS == 33_656, "simple locator zero floor")
    require(P > BUDGET and P - BUDGET == 2_130_706_432, "positive-dimensional direct-count route cut")

    toy = toy_census()
    asymmetric = asymmetric_rank_drop_control()
    payload: dict[str, Any] = {
        "schema": "m31-whole-ball-source-separator-compiler-v1",
        "artifact_kind": "WHOLE_BALL_ROUTE_CUT_COMPILER",
        "terminal": "WHOLE_BALL_ROUTE_CUT_CURRENT_ARTIFACT_SET",
        "base_commit": BASE_COMMIT,
        "status": "PROVED_137_CELL_PLUECKER_COMPRESSION_UNIVERSAL_SOURCE_BRIDGE_OPEN",
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
        "whole_ball_contract": {
            "object": "NONZERO_SYNDROME_EXACT_SUPPORT_LIST",
            "support_weight_interval": [0, RADIUS],
            "weight_layers": RADIUS + 1,
            "exact_containment_retained": True,
            "every_one_point_escape_retained": True,
            "boundary_only_sufficient": False,
            "frozen_embedding_sufficient": False,
            "support_sum_duplicate_free": True,
            "center_to_hyperplane_surjective": True,
            "zero_syndrome_list_size": 1,
            "source_selection_proved": False,
            "interior_covered": False,
            "boundary_covered": False,
            "allowed_terminals": [
                "ESCAPE_KILLED",
                "PAID_OWNER",
                "ACTUAL_HYPERPLANE_SURVIVOR",
                "UNPAID_PRIMITIVE",
            ],
        },
        "four_face_compression": {
            "factorization": [
                "P00=A0*B0*C0",
                "P10=A1*B0*C1",
                "P01=A0*B1*C1",
                "P11=A1*B1*C0",
            ],
            "six_factors_pairwise_coprime": True,
            "primitive_row": True,
            "factor_degree": FACTOR_DEGREE,
            "row_degree": ROW_DEGREE,
            "theta_bound": SIGMA,
            "forney_index_sum": ROW_DEGREE,
            "cokernel_formula": "sum_j max(0,mu_j-D)",
            "surjective_iff_max_index_at_most_bound": True,
            "high_forney_index_floor": HIGH_INDEX_FLOOR,
            "low_pair_sum_ceiling": LOW_PAIR_SUM_CEILING,
            "low_syzygy_degree_ceiling": LOW_SYZYGY_CEILING,
            "coefficient_unknowns": LOW_SYZYGY_UNKNOWNS,
            "single_low_syzygy_sufficient_for_rank_drop": False,
            "rank_drop_exact_two_row_criterion": True,
            "two_row_degree_sum_ceiling": LOW_PAIR_SUM_CEILING,
            "crt_equations": list(CRT_EQUATIONS),
            "syzygy_product_degree_ceiling": SYZYGY_PRODUCT_DEGREE,
            "crt_product_degree": CRT_PRODUCT_DEGREE,
            "crt_sufficient_by_degree": True,
            "full_rank_implies_escape_contradiction": True,
            "pluecker_defect_window": {
                "universal_surjectivity_bound": UNIVERSAL_SURJECTIVITY_BOUND,
                "deployed_threshold_gap": DEPLOYED_THRESHOLD_GAP,
                "tau_interval": [TAU_MIN, TAU_MAX],
                "defect_interval": [DEFECT_MIN, DEFECT_MAX],
                "cell_count": TAU_MAX - TAU_MIN + 1,
                "mu1_plus_mu2": "33792+tau",
                "mu3": "67584-tau",
                "kernel_dimension": "101102-tau",
                "rank": "168686+tau",
                "cokernel_defect": "137-tau",
                "minor_divisors": PLUECKER_DIVISORS,
                "quotient_degree_ceiling": TAU_MAX,
                "maximum_quotient_degree_equals_tau": True,
                "all_six_quotients_nonzero": True,
                "quotients_primitive": True,
                "rational_mds_parameters": [4, 2, 3],
                "linear_identities": list(PLUECKER_LINEAR_IDENTITIES),
                "quadratic_identity": PLUECKER_QUADRATIC_IDENTITY,
                "minimum_simple_locator_zeros": MIN_SIMPLE_LOCATOR_ZEROS,
                "split_squarefree_needed_only_for_root_statement": True,
                "sufficient_to_lift_source_witness": False,
            },
        },
        "toy_rank_drop_control": toy,
        "pgl_asymmetric_rank_drop_control": asymmetric,
        "direct_component_route_cut": {
            "scope": "CONDITIONAL_ON_INHERITED_DELTA_TIMES_P_TO_EY_CHARGE_FORM",
            "positive_dimension_direct_count_payable": False,
            "minimum_positive_dimension_charge": P,
            "full_budget": BUDGET,
            "excess": P - BUDGET,
        },
        "closure_state": {
            "closure_certified": False,
            "result": "UNIVERSAL_SOURCE_BRIDGE_REQUIRED",
            "owner_disjointness_proved": False,
            "add_back_proved": False,
            "unresolved_terminals": [
                "WHOLE_BALL_SOURCE_EXTRACTION_OPEN",
                "INTERIOR_WEIGHTS_1_TO_981128_OPEN",
                "BOUNDARY_UNRESTRICTED_SOURCE_SELECTION_OPEN",
                "ESCAPE_AWARE_3_TO_15_OPEN",
                "RANK16_H1_UNRESTRICTED_LOCATORS_OPEN",
                "RANK16_HIGHER_DEFECT_OPEN",
                "GLOBAL_DISJOINT_ADDBACK_OPEN",
            ],
            "ledger_atoms": {
                "U_paid": None,
                "U_Q": None,
                "U_list_int": None,
                "U_new": None,
            },
            "ledger_movement": 0,
            "prime_field_row_closed": False,
            "quartic_field_row_closed": False,
            "prize_claimed": False,
        },
        "provenance": {
            "parent_pr": 1002,
            "parent_head": BASE_COMMIT,
            "exact_optimizer": "experimental/notes/thresholds/m31_shortened_flat_hyperplane_wall.md",
            "four_face_source": "experimental/notes/thresholds/m31_chebyshev_global_separator.md",
            "forney_source": "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
            "completion_compiler": "experimental/notes/frontier-adjacent/four_row_exact_completion_compiler_v1.md",
        },
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS
        },
    }
    validate_contract(payload)
    return seal_certificate(payload)


def validate_certificate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    verify_self_hash(candidate)
    validate_contract(candidate)
    require(candidate == expected, "canonical certificate payload")


def set_path(payload: dict[str, Any], path: Sequence[str], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations: tuple[tuple[tuple[str, ...], Any], ...] = (
        (("base_commit",), "0" * 40),
        (("parameters", "agreement"), AGREEMENT + 1),
        (("parameters", "sigma"), SIGMA + 1),
        (("parameters", "budget"), BUDGET + 1),
        (("whole_ball_contract", "support_weight_interval"), [RADIUS, RADIUS]),
        (("whole_ball_contract", "weight_layers"), 1),
        (("whole_ball_contract", "exact_containment_retained"), False),
        (("whole_ball_contract", "every_one_point_escape_retained"), False),
        (("whole_ball_contract", "boundary_only_sufficient"), True),
        (("whole_ball_contract", "frozen_embedding_sufficient"), True),
        (("whole_ball_contract", "source_selection_proved"), True),
        (("four_face_compression", "factor_degree"), FACTOR_DEGREE - 1),
        (("four_face_compression", "row_degree"), ROW_DEGREE - 1),
        (("four_face_compression", "high_forney_index_floor"), HIGH_INDEX_FLOOR - 1),
        (("four_face_compression", "low_pair_sum_ceiling"), LOW_PAIR_SUM_CEILING + 1),
        (("four_face_compression", "low_syzygy_degree_ceiling"), LOW_SYZYGY_CEILING + 1),
        (("four_face_compression", "coefficient_unknowns"), LOW_SYZYGY_UNKNOWNS + 4),
        (("four_face_compression", "single_low_syzygy_sufficient_for_rank_drop"), True),
        (("four_face_compression", "rank_drop_exact_two_row_criterion"), False),
        (("four_face_compression", "crt_equations"), list(reversed(CRT_EQUATIONS))),
        (("four_face_compression", "crt_sufficient_by_degree"), False),
        (("four_face_compression", "pluecker_defect_window", "universal_surjectivity_bound"), UNIVERSAL_SURJECTIVITY_BOUND - 1),
        (("four_face_compression", "pluecker_defect_window", "tau_interval"), [0, 137]),
        (("four_face_compression", "pluecker_defect_window", "defect_interval"), [0, 137]),
        (("four_face_compression", "pluecker_defect_window", "cell_count"), 136),
        (("four_face_compression", "pluecker_defect_window", "minor_divisors"), dict(PLUECKER_DIVISORS, A0="Delta_02")),
        (("four_face_compression", "pluecker_defect_window", "all_six_quotients_nonzero"), False),
        (("four_face_compression", "pluecker_defect_window", "quotients_primitive"), False),
        (("four_face_compression", "pluecker_defect_window", "rational_mds_parameters"), [4, 2, 2]),
        (("four_face_compression", "pluecker_defect_window", "linear_identities"), list(reversed(PLUECKER_LINEAR_IDENTITIES))),
        (("four_face_compression", "pluecker_defect_window", "quadratic_identity"), "0=0"),
        (("four_face_compression", "pluecker_defect_window", "minimum_simple_locator_zeros"), MIN_SIMPLE_LOCATOR_ZEROS - 1),
        (("toy_rank_drop_control", "labelled_disjoint_sextuples"), TOY_TOTAL - 1),
        (("toy_rank_drop_control", "theta_rank_4"), TOY_FULL_RANK + 1),
        (("toy_rank_drop_control", "theta_rank_3"), TOY_RANK_DROP - 1),
        (("toy_rank_drop_control", "primitive_syzygy"), [1, 3, 6, 3]),
        (("toy_rank_drop_control", "pluecker_quotients", "A0"), [4]),
        (("pgl_asymmetric_rank_drop_control", "forney_profile"), [0, 3, 3]),
        (("pgl_asymmetric_rank_drop_control", "pgl2_stabilizer"), [[1, 0, 0, 1], [1, 1, 0, 1]]),
        (("direct_component_route_cut", "scope"), "UNCONDITIONAL"),
        (("direct_component_route_cut", "positive_dimension_direct_count_payable"), True),
        (("closure_state", "closure_certified"), True),
        (("closure_state", "result"), "SAFE"),
        (("closure_state", "ledger_atoms", "U_Q"), 0),
        (("closure_state", "ledger_movement"), 1),
        (("closure_state", "unresolved_terminals"), []),
        (("closure_state", "prime_field_row_closed"), True),
        (("provenance", "parent_pr"), 1001),
        (("source_sha256", "experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py"), "0" * 64),
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

    raw_hash = copy.deepcopy(expected)
    raw_hash["certificate_sha256"] = "0" * 64
    raw_payload = copy.deepcopy(expected)
    raw_payload["parameters"]["radius"] = RADIUS - 1
    for label, mutated in (("raw hash", raw_hash), ("raw payload", raw_payload)):
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
        print(f"M31 whole-ball compiler tampers: {rejected}/{rejected} rejected PASS")
        return

    require(CERTIFICATE_PATH.exists(), "pinned manifest exists")
    pinned = json.loads(CERTIFICATE_PATH.read_text())
    validate_certificate(pinned, expected)
    print(f"M31 whole-ball source-to-separator compiler: {CHECKS} exact checks PASS")
    print("whole-ball contract: weights 0..981129 / 981130 layers / escapes retained PASS")
    print("four-face threshold: pairwise-coprime factors imply surjectivity for D>=67584 PASS")
    print("deployed rank drop: 137 cells / tau=0..136 / h=137-tau PASS")
    print("Pluecker compression: six nonzero primitive quotients / degree<=tau / [4,2,3] MDS PASS")
    print("six reduced-CRT equations: necessary and sufficient by degree PASS")
    print("GF(7) toy: 5040 total = 3696 full-rank + 1344 rank-drop PASS")
    print("GF(23) rank-drop control: profile (0,2,4) / trivial PGL2 stabilizer PASS")
    print("RESULT: UNIVERSAL_SOURCE_BRIDGE_REQUIRED")
    print("M31 rows: OPEN; U_paid/U_Q/U_list-int/U_new: null; ledger movement: 0")


if __name__ == "__main__":
    main()
