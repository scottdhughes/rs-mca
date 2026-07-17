#!/usr/bin/env python3
"""Verify the full-projective extension-slope rank-nine route cut.

The exact control works in GF(2^138) with its unique GF(2^23) subfield.  It
extends the five-pencil control from the rank-nine locator-span falsifier by
one base-field evaluation point and twists the sparse received line.  The 55
declared slopes are then outside the base field, the global syndrome plane has
full projective field, and the rank-nine/GM--MDS local data all survive.

This is a generic-local countercontrol.  It does not instantiate KoalaBear's
deployed subgroup domain, exhaust the full retained bad-slope family, replay
the deployed first-match masks, pay an owner, or move a ledger value.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-rank9-full-projective-gm-route-cut-v1"
ARTIFACT_KIND = "M1_RANK9_FULL_PROJECTIVE_EXTENSION_SLOPE_GENERIC_LOCAL_ROUTE_CUT"
STATUS = "PROVED_EXACT_GENERIC_LOCAL_STRENGTHENED_SHORTCUT_FALSE"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-full-projective-gm-route-cut-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_full_projective_gm_route_cut_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_full_projective_gm_route_cut_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-projective-gm-route-cut-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_full_projective_gm_route_cut_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_full_projective_gm_route_cut_v1.sage"
)

LOCATOR_SPAN_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.md"
)
LOCATOR_SPAN_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-rank9-regular-locator-span-shortcut-refuted-v1/"
    "m1_rank9_regular_locator_span_shortcut_refuted_v1.json"
)
LOCATOR_SPAN_PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py"
)
LOCATOR_SPAN_SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.sage"
)

GM_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_gm_mds_fixed_domain_gate_v1.md"
)
GM_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-gm-mds-fixed-domain-gate-v1/"
    "m1_kb_rank9_gm_mds_fixed_domain_gate_v1.json"
)
GM_PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.py"
)
GM_SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.sage"
)

SPARSE_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"
)
PROJECTIVE_FIELD_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "projective_syndrome_c5_first_match.md"
)

BASE_DEGREE = 23
EXTENSION_DEGREE = 6
DEGREE = BASE_DEGREE * EXTENSION_DEGREE
BASE_Q = 1 << BASE_DEGREE
Q = 1 << DEGREE
MODULUS = (1 << 138) | (1 << 8) | (1 << 7) | (1 << 1) | 1
MASK = Q - 1
ALPHA = 2
BASE_ORDER_FACTORS = (47, 178_481)
BASE_GENERATOR_EXPONENT = (Q - 1) // (BASE_Q - 1)
ABSOLUTE_PROPER_SUBFIELD_DEGREES = (1, 2, 3, 6, 23, 46, 69)

N = 25
K = 13
R = N - K
J = 11
A = N - J
SPARSE_SUPPORT_SIZE = 3

CORES = (
    (3, 5, 6, 7, 9, 11, 13, 16, 17, 20, 21),
    (0, 2, 3, 6, 7, 8, 9, 10, 12, 13, 19),
    (1, 2, 4, 6, 7, 8, 10, 15, 17, 20, 21),
    (2, 3, 5, 9, 11, 12, 13, 14, 19, 20, 21),
    (0, 1, 2, 5, 6, 12, 14, 15, 18, 20, 21),
)

BASIS_INDICES = (0, 1, 11, 12, 22, 23, 33, 34, 44, 45)
GM_TUPLE_INDICES = (0, 1, 2, 11, 12, 22, 23, 33, 34, 44, 45)

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "exact_control",
    "route_cut",
    "scope_guards",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not instantiate the deployed KoalaBear subgroup domain.",
    "This packet does not assert that declared Gamma exhausts the full bad-slope set.",
    "This packet does not prove that the declared slopes survive the deployed first-match order.",
    "This packet does not execute periodic, quotient, Johnson, B11, C5-payment, or sparse-sigma owners.",
    "This packet does not convert one GM-admissible tuple into a count for the complete retained family.",
    "This packet does not move U_paid or B_remaining.",
    "This packet does not close rank nine, branch 3, sparse sigma, or the KoalaBear row.",
    "This packet does not attack intrinsic rank at least ten.",
    "This packet does not authorize Lean or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """An arithmetic, source, schema, or semantic gate failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def gf_mul(left: int, right: int) -> int:
    require(0 <= left < Q and 0 <= right < Q, "field operand out of range")
    result = 0
    a = left
    b = right
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & Q:
            a ^= MODULUS
    return result & MASK


def binary_poly_mod(dividend: int, divisor: int) -> int:
    require(divisor > 0, "zero polynomial divisor")
    remainder = dividend
    divisor_degree = divisor.bit_length() - 1
    while remainder and remainder.bit_length() - 1 >= divisor_degree:
        remainder ^= divisor << ((remainder.bit_length() - 1) - divisor_degree)
    return remainder


def binary_poly_gcd(left: int, right: int) -> int:
    a = left
    b = right
    while b:
        a, b = b, binary_poly_mod(a, b)
    return a


def gf_pow(base: int, exponent: int) -> int:
    require(exponent >= 0, "negative field exponent")
    result = 1
    value = base
    power = exponent
    while power:
        if power & 1:
            result = gf_mul(result, value)
        value = gf_mul(value, value)
        power >>= 1
    return result


def gf_inv(value: int) -> int:
    require(value != 0, "division by zero")
    inverse = gf_pow(value, Q - 2)
    require(gf_mul(value, inverse) == 1, "field inverse check failed")
    return inverse


def gf_div(numerator: int, denominator: int) -> int:
    return gf_mul(numerator, gf_inv(denominator))


def poly_trim(polynomial: Sequence[int]) -> tuple[int, ...]:
    values = list(polynomial)
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] ^= gf_mul(a, b)
    return poly_trim(result)


def poly_scale(polynomial: Sequence[int], scalar: int) -> tuple[int, ...]:
    return poly_trim([gf_mul(value, scalar) for value in polynomial])


def poly_eval(polynomial: Sequence[int], point: int) -> int:
    result = 0
    for coefficient in reversed(polynomial):
        result = gf_mul(result, point) ^ coefficient
    return result


def root_polynomial(points: Iterable[int]) -> tuple[int, ...]:
    polynomial: tuple[int, ...] = (1,)
    for point in points:
        polynomial = poly_mul(polynomial, (point, 1))
    return polynomial


def pad_row(row: Sequence[int], width: int) -> list[int]:
    require(len(row) <= width, "row exceeds declared width")
    return list(row) + [0] * (width - len(row))


def rref_rank_pivots(rows: Sequence[Sequence[int]]) -> tuple[int, list[int]]:
    if not rows:
        return 0, []
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    matrix = [list(row) for row in rows]
    pivot_row = 0
    pivots: list[int] = []
    for column in range(width):
        chosen = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if chosen is None:
            continue
        matrix[pivot_row], matrix[chosen] = matrix[chosen], matrix[pivot_row]
        inverse = gf_inv(matrix[pivot_row][column])
        matrix[pivot_row] = [gf_mul(value, inverse) for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value ^ gf_mul(factor, pivot)
                for value, pivot in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row, pivots


def matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    return rref_rank_pivots(rows)[0]


def determinant(rows: Sequence[Sequence[int]]) -> int:
    size = len(rows)
    require(size > 0 and all(len(row) == size for row in rows), "determinant needs square matrix")
    matrix = [list(row) for row in rows]
    result = 1
    for column in range(size):
        chosen = next(
            (row for row in range(column, size) if matrix[row][column]),
            None,
        )
        require(chosen is not None, "singular determinant witness")
        matrix[column], matrix[chosen] = matrix[chosen], matrix[column]
        pivot = matrix[column][column]
        result = gf_mul(result, pivot)
        inverse = gf_inv(pivot)
        for row in range(column + 1, size):
            if matrix[row][column] == 0:
                continue
            factor = gf_mul(matrix[row][column], inverse)
            for entry in range(column, size):
                matrix[row][entry] ^= gf_mul(factor, matrix[column][entry])
    return result


def nonzero_minor(rows: Sequence[Sequence[int]]) -> dict[str, Any]:
    rank, pivots = rref_rank_pivots(rows)
    require(rank == len(rows), "declared rows are not independent")
    square = [[row[column] for column in pivots] for row in rows]
    value = determinant(square)
    require(value != 0, "selected rank minor vanished")
    return {"columns": pivots, "determinant_integer_encoding": value}


def matrix_vector(rows: Sequence[Sequence[int]], vector: Sequence[int]) -> list[int]:
    require(all(len(row) == len(vector) for row in rows), "matrix-vector dimension mismatch")
    output: list[int] = []
    for row in rows:
        value = 0
        for left, right in zip(row, vector, strict=True):
            value ^= gf_mul(left, right)
        output.append(value)
    return output


def matrix_columns(rows: Sequence[Sequence[int]], columns: Sequence[int]) -> list[list[int]]:
    return [[row[column] for column in columns] for row in rows]


def vector_scale(vector: Sequence[int], scalar: int) -> list[int]:
    return [gf_mul(value, scalar) for value in vector]


def vector_add(left: Sequence[int], right: Sequence[int]) -> list[int]:
    return [a ^ b for a, b in zip(left, right, strict=True)]


def sha256_int_rows(rows: Sequence[Sequence[int]]) -> str:
    return canonical_hash([list(row) for row in rows])


@functools.lru_cache(maxsize=1)
def _exact_control_json() -> str:
    require((N, K, R, J, A) == (25, 13, 12, 11, 14), "RS row drift")
    require(MODULUS == (1 << 138) | (1 << 8) | (1 << 7) | (1 << 1) | 1, "field modulus drift")
    require(gf_pow(ALPHA, 1 << DEGREE) == ALPHA, "ambient modulus failed Frobenius closure")
    require(
        all(
            binary_poly_gcd(
                MODULUS,
                gf_pow(ALPHA, 1 << (DEGREE // prime)) ^ ALPHA,
            )
            == 1
            for prime in (2, 3, 23)
        ),
        "ambient modulus is reducible",
    )
    require(gf_pow(ALPHA, Q - 1) == 1, "alpha did not lie in the field")

    base_generator = gf_pow(ALPHA, BASE_GENERATOR_EXPONENT)
    require(gf_pow(base_generator, BASE_Q - 1) == 1, "base generator left GF(2^23)")
    require(
        all(
            gf_pow(base_generator, (BASE_Q - 1) // prime) != 1
            for prime in BASE_ORDER_FACTORS
        ),
        "base generator is not primitive",
    )
    require(
        all(gf_pow(ALPHA, BASE_Q**degree) != ALPHA for degree in (1, 2, 3)),
        "alpha lies in a proper intermediate field",
    )
    require(gf_pow(ALPHA, BASE_Q**6) == ALPHA, "alpha left GF((2^23)^6)")

    exponents = tuple(1 << index for index in range(22))
    ratios = tuple(gf_pow(base_generator, exponent) for exponent in exponents)
    moving_points = tuple(gf_inv(1 ^ ratio) for ratio in ratios)
    c = base_generator
    domain = (0, 1) + moving_points + (c,)
    require(len(domain) == N and len(set(domain)) == N, "evaluation domain collision")
    require(all(gf_pow(point, BASE_Q) == point for point in domain), "domain left base field")
    require(all(point not in (0, 1, c) for point in moving_points), "moving point hit sparse support")
    require(
        all(gf_div(1 ^ moving_points[index], moving_points[index]) == ratios[index] for index in range(22)),
        "point-to-ratio formula drift",
    )
    max_sum = sum(exponents)
    require(max_sum == (1 << 22) - 1 < BASE_Q - 1, "subset exponent envelope drift")
    twelve_sums = {
        sum(exponents[index] for index in subset)
        for subset in itertools.combinations(range(22), 12)
    }
    require(len(twelve_sums) == 646_646, "12-subset products lost injectivity")

    lambdas: list[int] = []
    for point in domain:
        denominator = 1
        for other in domain:
            if other != point:
                denominator = gf_mul(denominator, point ^ other)
        lambdas.append(gf_inv(denominator))
    require(all(gf_pow(value, BASE_Q) == value for value in lambdas), "dual weight left base field")
    parity = [
        [gf_mul(lambdas[column], gf_pow(domain[column], row)) for column in range(N)]
        for row in range(R)
    ]
    require(matrix_rank(parity) == R, "parity check lost rank")

    require(all(len(core) == len(set(core)) == 11 for core in CORES), "core size drift")
    require(not set.intersection(*(set(core) for core in CORES)), "core intersection is nonempty")

    root_sets: list[tuple[int, ...]] = []
    offsets: list[int] = []
    for core in CORES:
        offsets.append(len(root_sets))
        for moving in range(22):
            if moving not in core:
                root_sets.append(tuple(sorted(core + (moving,))))
    require(len(root_sets) == len(set(root_sets)) == 55, "five pencils are not 55 distinct root sets")

    f0 = [0] * N
    f0[0] = 1
    f0[-1] = ALPHA
    g = [0] * N
    g[1] = 1
    f = vector_add(f0, vector_scale(g, ALPHA))
    y0 = matrix_vector(parity, f)
    y1 = matrix_vector(parity, g)
    require(matrix_rank([y0, y1]) == 2, "syndrome line is degenerate")
    zero_codeword_support = (0, 1, N - 1)
    g_support = tuple(index for index, value in enumerate(g) if value)
    require(g_support == (1,), "g support drift")
    require(y1 == [row[1] for row in parity], "g syndrome left the b column")
    zero_padded_support = zero_codeword_support + tuple(range(2, 10))
    require(len(set(zero_padded_support)) == J, "canonical zero padding drift")
    zero_padded_locator = root_polynomial(domain[index] for index in zero_padded_support)
    zero_padded_h2 = gf_mul(lambdas[1], poly_eval(zero_padded_locator, domain[1]))
    require(zero_padded_h2 == 0, "contained zero witness passed H2 ell")

    frobenius_ranks: list[int] = []
    for degree in (1, 2, 3):
        exponent = BASE_Q**degree
        y0_frob = [gf_pow(value, exponent) for value in y0]
        y1_frob = [gf_pow(value, exponent) for value in y1]
        rank = matrix_rank([y0, y1, y0_frob, y1_frob])
        require(rank == 3, f"projective syndrome plane descended at degree {degree}")
        frobenius_ranks.append(rank)
    absolute_frobenius_ranks: list[int] = []
    for degree in ABSOLUTE_PROPER_SUBFIELD_DEGREES:
        exponent = 1 << degree
        y0_frob = [gf_pow(value, exponent) for value in y0]
        y1_frob = [gf_pow(value, exponent) for value in y1]
        rank = matrix_rank([y0, y1, y0_frob, y1_frob])
        require(rank == 3, f"syndrome plane descended to GF(2^{degree})")
        absolute_frobenius_ranks.append(rank)

    code_polynomials: list[tuple[int, ...]] = []
    gammas: list[int] = []
    etas: list[int] = []
    errors: list[list[int]] = []
    supports: list[tuple[int, ...]] = []
    locators: list[tuple[int, ...]] = []

    for root_set in root_sets:
        root_poly = root_polynomial(moving_points[index] for index in root_set)
        require(len(root_poly) == 13, "root polynomial degree drift")
        code_poly = poly_scale(root_poly, gf_inv(poly_eval(root_poly, 0)))
        gamma = poly_eval(code_poly, 1)
        eta = gamma ^ ALPHA
        expected_gamma = 1
        for index in root_set:
            expected_gamma = gf_mul(expected_gamma, ratios[index])
        require(gamma == expected_gamma != 0, "slope formula or nontangency failed")
        require(gf_pow(gamma, BASE_Q) == gamma, "gamma left base field")
        require(
            all(gf_pow(eta, BASE_Q**degree) != eta for degree in (1, 2, 3)),
            "twisted slope entered a proper intermediate field",
        )

        codeword = [poly_eval(code_poly, point) for point in domain]
        sparse_word = vector_add(f, vector_scale(g, eta))
        require(
            tuple(index for index, value in enumerate(sparse_word) if value)
            == zero_codeword_support,
            "zero-codeword discrepancy support drift",
        )
        error = vector_add(sparse_word, codeword)
        moving_support = tuple(index for index in range(22) if index not in set(root_set))
        support = moving_support + (22,)
        locator = root_polynomial(
            [moving_points[index] for index in moving_support] + [c]
        )

        require(matrix_vector(parity, codeword) == [0] * R, "degree-12 word left RS code")
        require(
            matrix_vector(parity, error) == vector_add(y0, vector_scale(y1, eta)),
            "error left syndrome line",
        )
        require(sum(value != 0 for value in error) == J, "error is not full weight")
        actual_support = tuple(
            [index for index, value in enumerate(error[2:24]) if value]
            + ([22] if error[-1] else [])
        )
        require(actual_support == support, "actual support drift")
        require(all(sparse_word[index] != 0 for index in (0, 1, 24)), "tangent slope retained")
        require(len(locator) == J + 1 and locator[-1] == 1, "locator degree/monicity drift")
        require(all(gf_pow(value, BASE_Q) == value for value in locator), "locator coefficient left base field")
        require(
            all(poly_eval(locator, moving_points[index]) == 0 for index in moving_support)
            and poly_eval(locator, c) == 0,
            "locator split failed",
        )

        recurrence = 0
        for index in range(N):
            recurrence ^= gf_mul(
                gf_mul(lambdas[index], sparse_word[index]),
                poly_eval(locator, domain[index]),
            )
        h2_locator = gf_mul(lambdas[1], poly_eval(locator, 1))
        require(recurrence == 0, "M(eta) ell failed")
        require(h2_locator != 0, "H2 ell noncontainment or regular pivot failed")

        support_columns = [2 + index for index in moving_support] + [24]
        require(matrix_rank(matrix_columns(parity, support_columns)) == J, "support image lost MDS rank")
        require(
            matrix_rank(matrix_columns(parity, support_columns + [1])) == J + 1,
            "y1 entered support image",
        )

        code_polynomials.append(code_poly)
        gammas.append(gamma)
        etas.append(eta)
        errors.append(error)
        supports.append(support)
        locators.append(locator)

    require(len(set(gammas)) == len(set(etas)) == 55, "declared slopes are not distinct")
    require(len(set(supports)) == 55, "declared supports are not distinct")

    raw_rank = matrix_rank(errors)
    affine_rank = matrix_rank(
        [vector_add(error, errors[0]) for error in errors[1:]]
    )
    locator_rows = [pad_row(locator, J + 1) for locator in locators]
    locator_rank = matrix_rank(locator_rows)
    require((raw_rank, affine_rank, locator_rank) == (10, 9, 11), "rank triple drift")

    basis_errors = [errors[index] for index in BASIS_INDICES]
    require(matrix_rank(basis_errors) == 10, "ten-witness basis drift")
    basis_carrier = set().union(*(set(supports[index]) for index in BASIS_INDICES))
    carrier = set().union(*(set(support) for support in supports))
    require(basis_carrier == carrier == set(range(23)), "basis supports lost carrier")
    n_v = len(carrier)
    nu = n_v - R
    require((n_v, nu) == (23, 11), "carrier excess drift")
    carrier_columns = [2 + index for index in range(22)] + [24]
    carrier_parity = matrix_columns(parity, carrier_columns)
    require(matrix_rank(carrier_parity) == R, "carrier parity rank drift")
    require(len(carrier_parity[0]) - matrix_rank(carrier_parity) == 11, "carrier kernel drift")

    gm_supports = [supports[index] for index in GM_TUPLE_INDICES]
    gm_min_slack_by_size: list[int] = []
    gm_tight_count = 0
    for size in range(1, 12):
        slacks: list[int] = []
        for subset in itertools.combinations(range(11), size):
            intersection = set(gm_supports[subset[0]])
            for index in subset[1:]:
                intersection.intersection_update(gm_supports[index])
            slack = (J + 1) - (size + len(intersection))
            require(slack >= 0, "GM--MDS intersection inequality failed")
            slacks.append(slack)
            if slack == 0:
                gm_tight_count += 1
        gm_min_slack_by_size.append(min(slacks))
    require(
        gm_min_slack_by_size == [0, 0, 0, 2, 1, 2, 2, 2, 1, 1, 0],
        "GM slack profile drift",
    )
    gm_locator_rows = [locator_rows[index] for index in GM_TUPLE_INDICES]
    require(matrix_rank(gm_locator_rows) == 11, "GM tuple locator rank drift")
    gm_minor = nonzero_minor(gm_locator_rows)

    # Exact uniqueness profile.  For a nonzero degree-at-most-12 witness let
    # r be its roots outside E={a,b,c} and s its agreements on E.  Then
    # r+s>=14, r<=12, s<=3.  Any profile involving c makes the remaining
    # scalar/linear factor base-valued from its other base agreements, so its
    # value at c is base-valued and cannot equal alpha.  Without c one must
    # have (r,s)=(12,2), agree at a,b, and the injective subset-product map
    # fixes the root set.  The zero word has discrepancy support E, while
    # supp(g)={b} is contained in E, so Hg belongs to the E-column span and
    # the zero witness is same-support contained.
    possible_profiles = [
        [roots, agreements]
        for roots in range(13)
        for agreements in range(4)
        if roots + agreements >= A
    ]
    require(
        possible_profiles == [[11, 3], [12, 2], [12, 3]],
        "agreement profile arithmetic drift",
    )
    require(gf_pow(ALPHA, BASE_Q) != ALPHA, "alpha/base separation vanished")
    require(all(gf_pow(value, BASE_Q) == value for value in gammas), "base agreement value drift")
    require(sum(value != 0 for value in f) == 3, "sparse word support drift")

    control = {
        "field_tower": {
            "characteristic": 2,
            "base_degree": BASE_DEGREE,
            "extension_degree_over_base": EXTENSION_DEGREE,
            "absolute_degree": DEGREE,
            "base_cardinality": BASE_Q,
            "ambient_cardinality": Q,
            "ambient_modulus": "x^138 + x^8 + x^7 + x + 1",
            "ambient_modulus_irreducible": True,
            "alpha_integer_encoding": ALPHA,
            "alpha_has_degree_six_over_base": True,
            "base_generator_exponent": BASE_GENERATOR_EXPONENT,
            "base_generator_integer_encoding": base_generator,
            "base_generator_order": BASE_Q - 1,
            "base_generator_order_prime_factors": list(BASE_ORDER_FACTORS),
        },
        "row": {
            "n": N,
            "k": K,
            "redundancy_R": R,
            "radius_j": J,
            "agreement_A": A,
            "R_minus_j": R - J,
            "sparse_support_size": SPARSE_SUPPORT_SIZE,
        },
        "domain": {
            "contained_in_base_field": True,
            "a_integer_encoding": 0,
            "b_integer_encoding": 1,
            "c_integer_encoding": c,
            "moving_point_count": len(moving_points),
            "formula": "z_i=(1-v^(2^i))^(-1), 0<=i<22",
            "all_distinct": True,
            "domain_sha256": canonical_hash(list(domain)),
            "dual_weights_sha256": canonical_hash(lambdas),
        },
        "construction": {
            "five_cores": [list(core) for core in CORES],
            "root_set_count": len(root_sets),
            "root_sets_sha256": canonical_hash([list(root_set) for root_set in root_sets]),
            "declared_slope_count": len(etas),
            "distinct_base_gamma_count": len(set(gammas)),
            "distinct_extension_eta_count": len(set(etas)),
            "all_eta_outside_base": True,
            "all_eta_degree_six_over_base": True,
            "gamma_sha256": canonical_hash(gammas),
            "eta_sha256": canonical_hash(etas),
            "code_polynomials_sha256": sha256_int_rows(code_polynomials),
            "errors_sha256": sha256_int_rows(errors),
            "locators_sha256": sha256_int_rows(locator_rows),
        },
        "projective_syndrome_field": {
            "global_syndrome_rank": 2,
            "tested_relative_intermediate_degrees_over_base": [1, 2, 3],
            "relative_frobenius_augmented_ranks": frobenius_ranks,
            "tested_absolute_proper_subfield_degrees": list(ABSOLUTE_PROPER_SUBFIELD_DEGREES),
            "absolute_frobenius_augmented_ranks": absolute_frobenius_ranks,
            "intrinsic_projective_field_is_full_ambient": True,
            "test_applied_to_global_pair_not_support_quotient": True,
        },
        "selector": {
            "complete_on_declared_Gamma": True,
            "declared_Gamma_exhausts_full_bad_set": False,
            "declared_Gamma_is_proper_subfamily": True,
            "unique_noncontained_witness_per_declared_slope": True,
            "rank_minimizing_on_declared_Gamma_because_unique": True,
            "all_full_weight": True,
            "all_transverse": True,
            "all_non_tangent": True,
            "all_regular_on_t1_chart": True,
            "all_squarefree_base_split_locators": True,
            "raw_witness_rank_t": raw_rank,
            "affine_difference_rank_s_star": affine_rank,
            "locator_vector_rank": locator_rank,
            "basis_indices": list(BASIS_INDICES),
            "basis_supports_recover_carrier": True,
        },
        "carrier": {
            "N_V": n_v,
            "R": R,
            "nu": nu,
            "kappa_star_on_declared_selector": nu,
            "restricted_kernel_dimension": n_v - R,
            "restricted_MDS_distance": R + 1,
        },
        "gm_fixed_domain_subtuple": {
            "indices": list(GM_TUPLE_INDICES),
            "support_count": 11,
            "locator_degree_j": J,
            "coefficient_width_K": J + 1,
            "inequality_count": (1 << 11) - 1,
            "all_intersection_inequalities_hold": True,
            "minimum_slack_by_subset_size": gm_min_slack_by_size,
            "tight_inequality_count": gm_tight_count,
            "fixed_domain_locator_rank": 11,
            "nonzero_minor": gm_minor,
        },
        "unique_witness_proof": {
            "possible_nonzero_agreement_profiles_before_base_separation": possible_profiles,
            "profiles_involving_c_eliminated_by_alpha_not_in_base": [[11, 3], [12, 2], [12, 3]],
            "remaining_noncontained_profile": [12, 2],
            "remaining_E_agreements": ["a", "b"],
            "twelve_subset_product_map_injective": True,
            "ambient_twelve_subset_count": len(twelve_sums),
            "zero_codeword_discrepancy_support_indices": list(zero_codeword_support),
            "g_support_indices": list(g_support),
            "every_size_j_padding_contains_b": True,
            "canonical_padded_support_indices": list(zero_padded_support),
            "canonical_padded_H2_locator_zero": True,
            "zero_codeword_witness_is_same_support_contained": True,
        },
    }
    return json.dumps(control, sort_keys=True, allow_nan=False)


def exact_control() -> dict[str, Any]:
    return json.loads(_exact_control_json())


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing bound source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        binding("packet-note", NOTE_REL, "exact theorem, uniqueness proof, and scope"),
        binding("packet-readme", README_REL, "replay and fail-closed contract"),
        binding("packet-python", PYTHON_REL, "bit-packed independent GF(2^138) verifier"),
        binding("packet-sage", SAGE_REL, "independent Sage finite-field replay"),
        binding("locator-span-note", LOCATOR_SPAN_NOTE_REL, "five-pencil predecessor construction"),
        binding("locator-span-certificate", LOCATOR_SPAN_CERT_REL, "frozen predecessor ranks and scope"),
        binding("locator-span-python", LOCATOR_SPAN_PYTHON_REL, "predecessor Python replay"),
        binding("locator-span-sage", LOCATOR_SPAN_SAGE_REL, "predecessor Sage replay"),
        binding("gm-gate-note", GM_NOTE_REL, "declared-tuple GM--MDS/fixed-domain interface"),
        binding("gm-gate-certificate", GM_CERT_REL, "frozen GM trichotomy"),
        binding("gm-gate-python", GM_PYTHON_REL, "GM gate Python verifier"),
        binding("gm-gate-sage", GM_SAGE_REL, "GM gate Sage replay"),
        binding("sparse-chart-note", SPARSE_NOTE_REL, "regular rank-nine residual producer"),
        binding("projective-field-note", PROJECTIVE_FIELD_NOTE_REL, "intrinsic projective syndrome field test"),
    ]


def expected_certificate() -> dict[str, Any]:
    document: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "exact_control": exact_control(),
        "route_cut": {
            "refuted_implication": (
                "base-domain + extension-valued slopes + full projective syndrome field + "
                "regular rank-nine selector + GM-admissible fixed-domain rank-eleven subtuple "
                "does not force emptiness, GM failure, fixed-domain rank drop, or selector rank above nine"
            ),
            "generic_local_strengthened_shortcut_refuted": True,
            "full_bad_family_or_deployed_first_match_strengthened_statement_refuted": False,
            "missing_load_bearing_inputs": [
                "deployed KoalaBear subgroup domain",
                "complete retained-family exhaustion",
                "deployed first-match survival",
                "a theorem converting the local tuple into a complete-family count",
            ],
            "owner_assignment": "NOT_CLASSIFIED_LOCAL_COMPATIBILITY_CONTROL_ONLY",
            "ledger_movement": 0,
        },
        "scope_guards": {
            "control_only_n25_j11": True,
            "koalabear_domain_instantiated": False,
            "declared_Gamma_exhausts_full_bad_set": False,
            "deployed_first_match_masks_checked": False,
            "proper_field_C5_payment_claimed": False,
            "periodic_quotient_Johnson_B11_owner_claimed": False,
            "complete_retained_family_bound_claimed": False,
            "rank_nine_closed": False,
            "branch_three_closed": False,
            "koalabear_row_closed": False,
            "ledger_movement": 0,
            "lean_authorized": False,
        },
        "audit_sections": {
            "dependencies": "PROVED predecessors plus exact new scalar extension/twist",
            "parameter_dependence": "exact finite control over GF((2^23)^6); not asymptotic",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "numerical_evidence": "exact finite-field identities, not a deployed census",
            "local_verdict": "GREEN",
            "deployed_payment_verdict": "YELLOW",
        },
        "nonclaims": NONCLAIMS,
    }
    document["payload_sha256"] = payload_hash(document)
    return document


def verify_document(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(set(document) == TOP_KEYS, "top-level schema drift")
    require(document.get("payload_sha256") == payload_hash(document), "payload hash mismatch")
    require(document == expected, "certificate differs from recomputed exact document")


def set_path(document: dict[str, Any], path: Sequence[Any], value: Any) -> None:
    cursor: Any = document
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value


MUTATIONS: tuple[tuple[str, tuple[Any, ...], Any], ...] = (
    ("schema", ("schema",), "wrong-schema"),
    ("artifact-kind", ("artifact_kind",), "wrong-kind"),
    ("status", ("status",), "UNPROVED"),
    ("base-degree", ("exact_control", "field_tower", "base_degree"), 22),
    ("extension-degree", ("exact_control", "field_tower", "extension_degree_over_base"), 3),
    ("ambient-degree", ("exact_control", "field_tower", "absolute_degree"), 137),
    ("base-cardinality", ("exact_control", "field_tower", "base_cardinality"), BASE_Q + 1),
    ("ambient-modulus", ("exact_control", "field_tower", "ambient_modulus"), "x^138+x+1"),
    ("modulus-irreducible", ("exact_control", "field_tower", "ambient_modulus_irreducible"), False),
    ("alpha-degree", ("exact_control", "field_tower", "alpha_has_degree_six_over_base"), False),
    ("base-generator", ("exact_control", "field_tower", "base_generator_integer_encoding"), 1),
    ("row-n", ("exact_control", "row", "n"), 24),
    ("row-k", ("exact_control", "row", "k"), 14),
    ("row-R", ("exact_control", "row", "redundancy_R"), 11),
    ("row-j", ("exact_control", "row", "radius_j"), 10),
    ("row-A", ("exact_control", "row", "agreement_A"), 15),
    ("domain-base", ("exact_control", "domain", "contained_in_base_field"), False),
    ("domain-c", ("exact_control", "domain", "c_integer_encoding"), 0),
    ("domain-count", ("exact_control", "domain", "moving_point_count"), 21),
    ("domain-distinct", ("exact_control", "domain", "all_distinct"), False),
    ("domain-hash", ("exact_control", "domain", "domain_sha256"), "00" * 32),
    ("root-count", ("exact_control", "construction", "root_set_count"), 54),
    ("slope-count", ("exact_control", "construction", "declared_slope_count"), 56),
    ("extension-slope", ("exact_control", "construction", "all_eta_outside_base"), False),
    ("full-degree-slope", ("exact_control", "construction", "all_eta_degree_six_over_base"), False),
    ("eta-hash", ("exact_control", "construction", "eta_sha256"), "11" * 32),
    ("error-hash", ("exact_control", "construction", "errors_sha256"), "22" * 32),
    ("locator-hash", ("exact_control", "construction", "locators_sha256"), "33" * 32),
    ("syndrome-rank", ("exact_control", "projective_syndrome_field", "global_syndrome_rank"), 1),
    ("relative-frobenius-ranks", ("exact_control", "projective_syndrome_field", "relative_frobenius_augmented_ranks"), [2, 3, 3]),
    ("absolute-subfields", ("exact_control", "projective_syndrome_field", "tested_absolute_proper_subfield_degrees"), [23, 46, 69]),
    ("absolute-frobenius-ranks", ("exact_control", "projective_syndrome_field", "absolute_frobenius_augmented_ranks"), [3] * 6 + [2]),
    ("full-projective", ("exact_control", "projective_syndrome_field", "intrinsic_projective_field_is_full_ambient"), False),
    ("complete-selector", ("exact_control", "selector", "complete_on_declared_Gamma"), False),
    ("proper-subfamily", ("exact_control", "selector", "declared_Gamma_is_proper_subfamily"), False),
    ("unique-witness", ("exact_control", "selector", "unique_noncontained_witness_per_declared_slope"), False),
    ("raw-rank", ("exact_control", "selector", "raw_witness_rank_t"), 11),
    ("affine-rank", ("exact_control", "selector", "affine_difference_rank_s_star"), 8),
    ("locator-rank", ("exact_control", "selector", "locator_vector_rank"), 10),
    ("carrier-N", ("exact_control", "carrier", "N_V"), 22),
    ("carrier-excess", ("exact_control", "carrier", "nu"), 10),
    ("gm-indices", ("exact_control", "gm_fixed_domain_subtuple", "indices"), list(range(11))),
    ("gm-count", ("exact_control", "gm_fixed_domain_subtuple", "inequality_count"), 2046),
    ("gm-pass", ("exact_control", "gm_fixed_domain_subtuple", "all_intersection_inequalities_hold"), False),
    ("gm-slack", ("exact_control", "gm_fixed_domain_subtuple", "minimum_slack_by_subset_size"), [0] * 11),
    ("gm-rank", ("exact_control", "gm_fixed_domain_subtuple", "fixed_domain_locator_rank"), 10),
    ("gm-minor", ("exact_control", "gm_fixed_domain_subtuple", "nonzero_minor", "determinant_integer_encoding"), 0),
    ("profile", ("exact_control", "unique_witness_proof", "remaining_noncontained_profile"), [11, 3]),
    ("subset-injection", ("exact_control", "unique_witness_proof", "twelve_subset_product_map_injective"), False),
    ("zero-support", ("exact_control", "unique_witness_proof", "zero_codeword_discrepancy_support_indices"), [0, 1, 23]),
    ("g-support", ("exact_control", "unique_witness_proof", "g_support_indices"), [0]),
    ("zero-padding", ("exact_control", "unique_witness_proof", "canonical_padded_support_indices"), [0, 1, 24] + list(range(2, 9))),
    ("zero-H2", ("exact_control", "unique_witness_proof", "canonical_padded_H2_locator_zero"), False),
    ("zero-contained", ("exact_control", "unique_witness_proof", "zero_codeword_witness_is_same_support_contained"), False),
    ("route-cut", ("route_cut", "generic_local_strengthened_shortcut_refuted"), False),
    ("deployed-refuted", ("route_cut", "full_bad_family_or_deployed_first_match_strengthened_statement_refuted"), True),
    ("owner", ("route_cut", "owner_assignment"), "UNPAID_PRIMITIVE"),
    ("ledger", ("route_cut", "ledger_movement"), 1),
    ("koalabear", ("scope_guards", "koalabear_domain_instantiated"), True),
    ("first-match", ("scope_guards", "deployed_first_match_masks_checked"), True),
    ("complete-bound", ("scope_guards", "complete_retained_family_bound_claimed"), True),
    ("row-closed", ("scope_guards", "koalabear_row_closed"), True),
    ("lean", ("scope_guards", "lean_authorized"), True),
    ("verdict", ("audit_sections", "deployed_payment_verdict"), "GREEN"),
    ("nonclaim", ("nonclaims", 0), "This packet closes KoalaBear."),
    ("source-path", ("source_bindings", 0, "path"), "wrong/path.md"),
    ("source-hash", ("source_bindings", 0, "sha256"), "44" * 32),
)


def tamper_selftest(expected: dict[str, Any]) -> None:
    caught = 0
    for label, path, value in MUTATIONS:
        mutant = copy.deepcopy(expected)
        set_path(mutant, path, value)
        mutant["payload_sha256"] = payload_hash(mutant)
        try:
            verify_document(mutant, expected)
        except VerificationError:
            caught += 1
        else:
            raise VerificationError(f"mutation escaped: {label}")

    bad_hash = copy.deepcopy(expected)
    bad_hash["payload_sha256"] = "ff" * 32
    try:
        verify_document(bad_hash, expected)
    except VerificationError:
        caught += 1
    else:
        raise VerificationError("payload-hash mutation escaped")

    duplicate = '{"schema":"a","schema":"b"}'
    try:
        parse_json(duplicate, "duplicate-key-control")
    except VerificationError:
        caught += 1
    else:
        raise VerificationError("duplicate-key mutation escaped")

    nonfinite = '{"x":NaN}'
    try:
        parse_json(nonfinite, "nonfinite-control")
    except VerificationError:
        caught += 1
    else:
        raise VerificationError("nonfinite mutation escaped")

    expected_count = len(MUTATIONS) + 3
    require(caught == expected_count, "tamper count drift")
    print(f"tamper self-test: {caught}/{expected_count} mutations detected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify the committed certificate")
    parser.add_argument("--write", action="store_true", help="write the recomputed certificate")
    parser.add_argument("--tamper-selftest", action="store_true", help="run semantic mutation controls")
    parser.add_argument("path", nargs="?", type=Path, default=CERT_PATH)
    args = parser.parse_args()

    require(args.check or args.write or args.tamper_selftest, "choose --check, --write, or --tamper-selftest")
    expected = expected_certificate()

    if args.write:
        args.path.parent.mkdir(parents=True, exist_ok=True)
        args.path.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {args.path}")

    if args.check:
        document = load_json(args.path)
        verify_document(document, expected)
        print(
            "PASS: full-projective extension-slope rank-nine local route cut; "
            "no deployed owner or ledger movement"
        )

    if args.tamper_selftest:
        tamper_selftest(expected)


if __name__ == "__main__":
    main()
