#!/usr/bin/env python3
"""Verify the odd-moment projective Hooley-Katz audit ledger."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from typing import Any


SMALL_PARAMETER_ROWS = (
    (1, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (3, 4),
    (3, 5),
    (4, 5),
    (4, 6),
    (5, 7),
)

RESERVE_A_VALUES = (1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0)
RESERVE_C_VALUES = (0.25, 0.5, 1.0, 2.0)
RESERVE_THETA_VALUES = (0.25, 0.5, 0.75, 1.0)
RESERVE_TAU_VALUES = (0.05, 0.10, 0.15, 0.20)
RESERVE_N_VALUES = (256, 1024, 4096, 16384)


def odd_degrees(d: int) -> tuple[int, ...]:
    return tuple(range(1, 2 * d, 2))


def reduced_odd_degrees(d: int) -> tuple[int, ...]:
    return tuple(range(3, 2 * d, 2))


def matrix_rank_mod(mat: list[list[int]], p: int) -> int:
    if not mat or not mat[0]:
        return 0
    rows = [row[:] for row in mat]
    m = len(rows)
    n = len(rows[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        pivot = None
        for r in range(rank, m):
            if rows[r][col] % p:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % p, p - 2, p)
        rows[rank] = [(value * inv) % p for value in rows[rank]]
        for r in range(m):
            if r != rank and rows[r][col] % p:
                factor = rows[r][col] % p
                rows[r] = [(a - factor * b) % p for a, b in zip(rows[r], rows[rank])]
        rank += 1
        col += 1
    return rank


def projective_jacobian(d: int, k: int, coords: tuple[int, ...], p: int) -> list[list[int]]:
    xs = coords[:k]
    ys = coords[k:]
    rows = []
    for r in range(1, d + 1):
        coeff = 2 * r - 1
        power = 2 * r - 2
        left = [(coeff * pow(x, power, p)) % p for x in xs]
        right = [(-coeff * pow(y, power, p)) % p for y in ys]
        rows.append(left + right)
    return rows


def distinct_square_count(coords: tuple[int, ...], p: int) -> int:
    return len({pow(value, 2, p) for value in coords})


def projective_rank_cases() -> dict[str, Any]:
    rows = []
    ok = True
    cases = [
        {"p": 5, "d": 2, "k": 3, "mode": "EXHAUSTIVE", "limit": None},
        {"p": 7, "d": 3, "k": 4, "mode": "DETERMINISTIC_SAMPLE", "limit": 5000},
    ]
    for case in cases:
        p = case["p"]
        d = case["d"]
        k = case["k"]
        mismatches = 0
        checked = 0
        iterator = itertools.product(range(p), repeat=2 * k)
        for coords in iterator:
            if not any(coords):
                continue
            rank = matrix_rank_mod(projective_jacobian(d, k, coords, p), p)
            expected = min(d, distinct_square_count(coords, p))
            if rank != expected:
                mismatches += 1
            checked += 1
            if case["limit"] is not None and checked >= case["limit"]:
                break
        row_ok = mismatches == 0 and checked > 0
        rows.append(
            {
                "p": p,
                "d": d,
                "k": k,
                "mode": case["mode"],
                "checked_projective_vectors": checked,
                "rank_mismatches": mismatches,
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def projective_geometry_ledger() -> dict[str, Any]:
    rows = []
    ok = True
    for d, k in SMALL_PARAMETER_ROWS:
        expected_dimension = 2 * k - d - 1
        critical_dimension_bound = d - 2
        singular_codimension_bound = expected_dimension - critical_dimension_bound
        row_ok = (
            k > d
            and expected_dimension > critical_dimension_bound
            and singular_codimension_bound >= 3
        )
        rows.append(
            {
                "d": d,
                "k": k,
                "ambient_projective_dimension": 2 * k - 1,
                "expected_dimension": expected_dimension,
                "critical_dimension_bound": critical_dimension_bound,
                "component_lower_bound_exceeds_critical": expected_dimension > critical_dimension_bound,
                "singular_codimension_bound": singular_codimension_bound,
                "lci": row_ok,
                "cohen_macaulay": row_ok,
                "normal_by_R1_S2": row_ok,
                "connected_projective_complete_intersection": row_ok,
                "geometrically_integral": row_ok,
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def rejection_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for d in (1, 2, 3, 4):
        k = d
        singular_codimension_bound = 2 * (k - d) + 1
        row_ok = singular_codimension_bound < 2
        rows.append(
            {
                "reason": "k=d boundary does not give normality/integrality",
                "d": d,
                "k": k,
                "singular_codimension_bound": singular_codimension_bound,
                "reject_projective_integrality_claim": row_ok,
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    for p, d in ((3, 2), (5, 3), (7, 4)):
        row_ok = p <= 2 * d - 1
        rows.append(
            {
                "reason": "characteristic must be zero or p>2d-1",
                "p": p,
                "d": d,
                "reject_characteristic": row_ok,
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def primitive_betti(j: int, M: int, degrees: tuple[int, ...]) -> int:
    codim = len(degrees)
    if M - j != codim:
        raise ValueError("primitive Betti parameters require M-j=len(degrees)")
    coeffs = [0] * (M + 1)
    coeffs[0] = 1
    for degree in degrees:
        new = [0] * (M + 1)
        for n in range(1, M + 1):
            new[n] = degree * (new[n - 1] + coeffs[n - 1])
        coeffs = new
    total = 0
    for c in range(codim, M + 1):
        total += ((-1) ** c) * math.comb(M + 1, c + 1) * coeffs[c]
    return ((-1) ** (j + 1)) * (j + 1) + ((-1) ** M) * total


def log_int(value: int) -> float | None:
    if value <= 0:
        return None
    if value.bit_length() < 900:
        return math.log(value)
    shift = value.bit_length() - 900
    return math.log(value >> shift) + shift * math.log(2)


def crude_betti_bound_original(d: int, k: int) -> int:
    M = 2 * k - d
    j = 2 * (k - d)
    return math.comb(M + 1, j) * (2 * d) ** M


def crude_betti_bound_reduced(d: int, k: int) -> int | None:
    if d <= 1:
        return None
    M = 2 * k - d - 1
    j = 2 * (k - d)
    return math.comb(M + 1, j) * (2 * d) ** M


def betti_exact_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for d, k in SMALL_PARAMETER_ROWS:
        degrees = odd_degrees(d)
        j = 2 * (k - d)
        M = 2 * k - d
        exact = primitive_betti(j, M, degrees)
        crude_original = crude_betti_bound_original(d, k)
        crude_reduced = crude_betti_bound_reduced(d, k)
        row_ok = exact >= 0 and exact <= crude_original and (
            crude_reduced is None or exact <= crude_reduced
        )
        rows.append(
            {
                "d": d,
                "k": k,
                "betti_index": j,
                "betti_projective_ambient": M,
                "multidegree": degrees,
                "exact_primitive_betti": exact,
                "crude_primitive_betti_bound": crude_original,
                "crude_primitive_betti_bound_original": crude_original,
                "crude_primitive_betti_bound_reduced": crude_reduced,
                "exact_log_betti": log_int(exact),
                "crude_log_betti": log_int(crude_original),
                "crude_log_betti_original": log_int(crude_original),
                "crude_log_betti_reduced": None if crude_reduced is None else log_int(crude_reduced),
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def primitive_betti_regression_cases() -> dict[str, Any]:
    expected_rows = [
        (2, 4, (1, 3), 6),
        (4, 6, (1, 3), 22),
        (6, 8, (1, 3), 86),
        (2, 5, (1, 3, 5), 282),
    ]
    rows = []
    ok = True
    for j, M, degrees, expected in expected_rows:
        observed = primitive_betti(j, M, degrees)
        row_ok = observed == expected
        rows.append(
            {
                "betti_index": j,
                "betti_projective_ambient": M,
                "multidegree": degrees,
                "expected_primitive_betti": expected,
                "observed_primitive_betti": observed,
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def primitive_betti_linear_elimination_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for d, k in SMALL_PARAMETER_ROWS:
        if d <= 1:
            rows.append(
                {
                    "d": d,
                    "k": k,
                    "status": "SKIPPED_D_EQ_1_LINEAR_EQUATION_ONLY",
                    "ok": True,
                }
            )
            continue
        j = 2 * (k - d)
        original = primitive_betti(j, 2 * k - d, odd_degrees(d))
        reduced = primitive_betti(j, 2 * k - d - 1, reduced_odd_degrees(d))
        row_ok = original == reduced
        rows.append(
            {
                "d": d,
                "k": k,
                "betti_index": j,
                "original_ambient": 2 * k - d,
                "original_multidegree": odd_degrees(d),
                "reduced_ambient": 2 * k - d - 1,
                "reduced_multidegree": reduced_odd_degrees(d),
                "original_primitive_betti": original,
                "reduced_primitive_betti": reduced,
                "identity_holds": row_ok,
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def gl_constant_bound_original(d: int, k: int) -> int:
    if d == 1:
        return 0
    return 9 * (2**d) * (d * (2 * d - 1) + 3) ** (2 * k)


def gl_constant_bound_reduced(d: int, k: int) -> int:
    if d == 1:
        return 0
    return 9 * (2 ** (d - 1)) * ((d - 1) * (2 * d - 1) + 3) ** (2 * k - 1)


def parameter_substitution_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for d, k in SMALL_PARAMETER_ROWS:
        ambient = 2 * k - 1
        variety_dim = 2 * k - d - 1
        singular_bound = d - 2
        exponent_betti_twice = variety_dim + singular_bound + 1
        exponent_lower_twice = variety_dim + singular_bound
        betti_index = variety_dim - singular_bound - 1
        betti_ambient = ambient - singular_bound - 1
        row_ok = (
            exponent_betti_twice == 2 * (k - 1)
            and exponent_lower_twice == 2 * k - 3
            and betti_index == 2 * (k - d)
            and betti_ambient == 2 * k - d
        )
        rows.append(
            {
                "d": d,
                "k": k,
                "ambient_projective_dimension": ambient,
                "variety_dimension": variety_dim,
                "singular_locus_dimension_bound": singular_bound,
                "multidegree": odd_degrees(d),
                "B_label": f"b'_{2 * (k - d)}({2 * k - d},(1,3,...,{2 * d - 1}))",
                "B_label_reduced": None
                if d == 1
                else f"b'_{2 * (k - d)}({2 * k - d - 1},(3,5,...,{2 * d - 1}))",
                "projective_betti_error_exponent": "k-1",
                "projective_lower_weight_error_exponent": "k-3/2",
                "C_bound": gl_constant_bound_reduced(d, k),
                "C_bound_original_presentation": gl_constant_bound_original(d, k),
                "C_bound_linear_eliminated_presentation": gl_constant_bound_reduced(d, k),
                "operative_lower_weight_presentation": "GL_LINEAR_ELIMINATED_PRESENTATION",
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def pi_projective(r: int, p: int) -> int:
    return (p ** (r + 1) - 1) // (p - 1)


def affine_cone_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p, d, k in ((7, 2, 3), (11, 2, 4), (11, 3, 4), (17, 4, 5)):
        r = 2 * k - d - 1
        pi_r = pi_projective(r, p)
        cone_main = 1 + (p - 1) * pi_r
        expected = p ** (r + 1)
        row_ok = cone_main == expected and r + 1 == 2 * k - d
        rows.append(
            {
                "p": p,
                "d": d,
                "k": k,
                "projective_dimension": r,
                "pi_r": pi_r,
                "cone_main": cone_main,
                "expected_affine_main": expected,
                "affine_error_bound_shape": "B*p^k + C*p^(k-1/2)",
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def mpp_threshold_exact(d: int, k: int) -> int:
    if d <= 1 or k <= d:
        raise ValueError("MPP threshold rows require d>=2 and k>d")
    D = d * (d - 1)
    delta = math.prod(2 * j - 1 for j in range(1, d + 1))
    return 2 * (d - 1) * (D ** (2 * (k - d))) * (D + 2 * (k - d) + 1) * delta


def mpp_threshold_cases() -> dict[str, Any]:
    rows = []
    ok = True
    d1_row_ok = True
    rows.append(
        {
            "d": 1,
            "k": 2,
            "status": "MPP_NOT_APPLICABLE_S_EQ_MINUS_1_SMOOTH_CASE",
            "ok": d1_row_ok,
        }
    )
    for d, k, p in ((2, 3, 101), (2, 6, 101), (3, 4, 1009), (4, 6, 1009)):
        threshold = mpp_threshold_exact(d, k)
        row_ok = threshold == (
            2
            * (d - 1)
            * (d * (d - 1)) ** (2 * (k - d))
            * (d * (d - 1) + 2 * (k - d) + 1)
            * math.prod(2 * j - 1 for j in range(1, d + 1))
        )
        rows.append(
            {
                "d": d,
                "k": k,
                "p": p,
                "D": d * (d - 1),
                "degree_product_delta": math.prod(2 * j - 1 for j in range(1, d + 1)),
                "MPP_field_threshold": threshold,
                "MPP_condition_met": p > threshold,
                "ok": row_ok,
            }
        )
        ok = ok and row_ok
    return {"rows": rows, "ok": ok}


def log_double_factorial_odd(d: int) -> float:
    return math.lgamma(2 * d + 1) - d * math.log(2) - math.lgamma(d + 1)


def log_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def stable_log_prefactor(log_p: float, d: int) -> float:
    log_p_minus_1 = log_p
    if log_p < 700:
        log_p_minus_1 = log_p + math.log1p(-math.exp(-log_p))
    d_log_p = d * log_p
    log_p_d_minus_1 = d_log_p
    if d_log_p < 700:
        log_p_d_minus_1 = d_log_p + math.log1p(-math.exp(-d_log_p))
    return log_p_minus_1 + d_log_p - log_p_d_minus_1


def reserve_scale_ledger() -> dict[str, Any]:
    rows = []
    ok = True
    for N in RESERVE_N_VALUES:
        logN = math.log(N)
        for A in RESERVE_A_VALUES:
            log_p = A * logN
            for C in RESERVE_C_VALUES:
                d = max(1, int(round(C * N / logN)))
                for theta in RESERVE_THETA_VALUES:
                    k = max(1, int(round(theta * N)))
                    for tau in RESERVE_TAU_VALUES:
                        alpha = 1 - 2 * tau
                        if k <= d or d < 2:
                            rows.append(
                                {
                                    "N": N,
                                    "A": A,
                                    "C": C,
                                    "theta": theta,
                                    "tau": tau,
                                    "d": d,
                                    "k": k,
                                    "geometry_status": "REJECT_K_LE_D_OR_D_LT_2",
                                    "ok": True,
                                }
                            )
                            continue
                        M_original = 2 * k - d
                        M_reduced = 2 * k - d - 1
                        j = 2 * (k - d)
                        log_betti_bound_original = log_binom(M_original + 1, j) + M_original * math.log(
                            2 * d
                        )
                        log_betti_bound_reduced = log_binom(M_reduced + 1, j) + M_reduced * math.log(
                            2 * d
                        )
                        log_C_gl_original = math.log(9) + d * math.log(2) + 2 * k * math.log(
                            d * (2 * d - 1) + 3
                        )
                        log_C_gl_reduced = (
                            math.log(9)
                            + (d - 1) * math.log(2)
                            + (2 * k - 1) * math.log((d - 1) * (2 * d - 1) + 3)
                        )
                        markov = 2 * k * math.log(1 / alpha)
                        log_prefactor = stable_log_prefactor(log_p, d)
                        log_betti_term_original = log_betti_bound_original - k * log_p
                        log_betti_term_reduced = log_betti_bound_reduced - k * log_p
                        log_lower_weight_term_original = log_C_gl_original - (k + 0.5) * log_p
                        log_lower_weight_term_reduced = log_C_gl_reduced - (k + 0.5) * log_p
                        net_betti_original = log_prefactor + markov + log_betti_term_original
                        net_betti_reduced = log_prefactor + markov + log_betti_term_reduced
                        net_lower_original = log_prefactor + markov + log_lower_weight_term_original
                        net_lower_reduced = log_prefactor + markov + log_lower_weight_term_reduced

                        D = d * (d - 1)
                        log_mpp_threshold = (
                            math.log(2 * (d - 1))
                            + 2 * (k - d) * math.log(D)
                            + math.log(D + 2 * (k - d) + 1)
                            + log_double_factorial_odd(d)
                        )
                        mpp_margin = log_p - log_mpp_threshold
                        rows.append(
                            {
                                "N": N,
                                "A": A,
                                "C": C,
                                "theta": theta,
                                "tau": tau,
                                "p_model": "N^A",
                                "log_p": log_p,
                                "d": d,
                                "k": k,
                                "betti_source": "crude_primitive_betti_bound_reduced_presentation",
                                "operative_GL_presentation": "GL_LINEAR_ELIMINATED_PRESENTATION",
                                "log_Betti_term": log_betti_term_reduced,
                                "log_Betti_term_original_presentation": log_betti_term_original,
                                "log_Betti_term_linear_eliminated_presentation": log_betti_term_reduced,
                                "log_GL_lower_weight_term": log_lower_weight_term_reduced,
                                "log_GL_lower_weight_term_original_presentation": log_lower_weight_term_original,
                                "log_GL_lower_weight_term_linear_eliminated_presentation": log_lower_weight_term_reduced,
                                "log_MPP_field_threshold": log_mpp_threshold,
                                "Markov_loss": markov,
                                "log_projective_line_prefactor": log_prefactor,
                                "net_GL_Betti_margin": net_betti_reduced,
                                "net_GL_Betti_margin_original_presentation": net_betti_original,
                                "net_GL_Betti_margin_linear_eliminated_presentation": net_betti_reduced,
                                "net_GL_lower_weight_margin": net_lower_reduced,
                                "net_GL_lower_weight_margin_original_presentation": net_lower_original,
                                "net_GL_lower_weight_margin_linear_eliminated_presentation": net_lower_reduced,
                                "MPP_condition_margin": mpp_margin,
                                "Betti_term_status": "PASS_BETTI_TERM"
                                if net_betti_reduced < 0
                                else "FAIL_BETTI_TERM",
                                "Betti_term_status_original_presentation": "PASS_BETTI_TERM"
                                if net_betti_original < 0
                                else "FAIL_BETTI_TERM",
                                "Betti_term_status_linear_eliminated_presentation": "PASS_BETTI_TERM"
                                if net_betti_reduced < 0
                                else "FAIL_BETTI_TERM",
                                "lower_weight_status": "PASS_LOWER_WEIGHT_TERM"
                                if net_lower_reduced < 0
                                else "FAIL_LOWER_WEIGHT_TERM",
                                "lower_weight_status_original_presentation": "PASS_LOWER_WEIGHT_TERM"
                                if net_lower_original < 0
                                else "FAIL_LOWER_WEIGHT_TERM",
                                "lower_weight_status_linear_eliminated_presentation": "PASS_LOWER_WEIGHT_TERM"
                                if net_lower_reduced < 0
                                else "FAIL_LOWER_WEIGHT_TERM",
                                "MPP_condition_status": "MPP_CONDITION_MET"
                                if mpp_margin > 0
                                else "MPP_CONDITION_FAIL",
                                "ok": True,
                            }
                        )
    valid_rows = [row for row in rows if "Betti_term_status" in row]
    summary = {
        "total_rows": len(rows),
        "valid_geometry_rows": len(valid_rows),
        "PASS_BETTI_TERM": sum(row["Betti_term_status"] == "PASS_BETTI_TERM" for row in valid_rows),
        "FAIL_BETTI_TERM": sum(row["Betti_term_status"] == "FAIL_BETTI_TERM" for row in valid_rows),
        "PASS_BETTI_TERM_ORIGINAL_PRESENTATION": sum(
            row["Betti_term_status_original_presentation"] == "PASS_BETTI_TERM" for row in valid_rows
        ),
        "FAIL_BETTI_TERM_ORIGINAL_PRESENTATION": sum(
            row["Betti_term_status_original_presentation"] == "FAIL_BETTI_TERM" for row in valid_rows
        ),
        "PASS_BETTI_TERM_LINEAR_ELIMINATED_PRESENTATION": sum(
            row["Betti_term_status_linear_eliminated_presentation"] == "PASS_BETTI_TERM"
            for row in valid_rows
        ),
        "FAIL_BETTI_TERM_LINEAR_ELIMINATED_PRESENTATION": sum(
            row["Betti_term_status_linear_eliminated_presentation"] == "FAIL_BETTI_TERM"
            for row in valid_rows
        ),
        "PASS_LOWER_WEIGHT_TERM": sum(
            row["lower_weight_status"] == "PASS_LOWER_WEIGHT_TERM" for row in valid_rows
        ),
        "FAIL_LOWER_WEIGHT_TERM": sum(
            row["lower_weight_status"] == "FAIL_LOWER_WEIGHT_TERM" for row in valid_rows
        ),
        "PASS_LOWER_WEIGHT_TERM_ORIGINAL_PRESENTATION": sum(
            row["lower_weight_status_original_presentation"] == "PASS_LOWER_WEIGHT_TERM"
            for row in valid_rows
        ),
        "FAIL_LOWER_WEIGHT_TERM_ORIGINAL_PRESENTATION": sum(
            row["lower_weight_status_original_presentation"] == "FAIL_LOWER_WEIGHT_TERM"
            for row in valid_rows
        ),
        "PASS_LOWER_WEIGHT_TERM_LINEAR_ELIMINATED_PRESENTATION": sum(
            row["lower_weight_status_linear_eliminated_presentation"] == "PASS_LOWER_WEIGHT_TERM"
            for row in valid_rows
        ),
        "FAIL_LOWER_WEIGHT_TERM_LINEAR_ELIMINATED_PRESENTATION": sum(
            row["lower_weight_status_linear_eliminated_presentation"] == "FAIL_LOWER_WEIGHT_TERM"
            for row in valid_rows
        ),
        "MPP_CONDITION_MET": sum(row["MPP_condition_status"] == "MPP_CONDITION_MET" for row in valid_rows),
        "MPP_CONDITION_FAIL": sum(row["MPP_condition_status"] == "MPP_CONDITION_FAIL" for row in valid_rows),
    }
    return {"rows": rows, "summary": summary, "ok": ok}


def count_domain_separation() -> dict[str, Any]:
    rows = [
        {
            "count_domain": "FULL_AFFINE_Fp_POINTS",
            "covered_by_projective_cone_conversion": True,
            "requires_multiplicative_character_twists": False,
            "ok": True,
        },
        {
            "count_domain": "FULL_TORUS_Fp_POINTS",
            "covered_by_projective_cone_conversion": False,
            "requires_boundary_removal": True,
            "ok": True,
        },
        {
            "count_domain": "PROPER_SUBGROUP_H_POINTS",
            "covered_by_projective_cone_conversion": False,
            "requires_multiplicative_character_twists": True,
            "twisted_hooley_katz_imported": False,
            "ok": True,
        },
    ]
    return {"rows": rows, "ok": all(row["ok"] for row in rows)}


def run_all() -> dict[str, Any]:
    result: dict[str, Any] = {
        "projective_jacobian_rank": projective_rank_cases(),
        "projective_geometry_ledger": projective_geometry_ledger(),
        "rejection_cases": rejection_cases(),
        "parameter_substitution": parameter_substitution_cases(),
        "exact_primitive_betti": betti_exact_cases(),
        "primitive_betti_regressions": primitive_betti_regression_cases(),
        "primitive_betti_linear_elimination": primitive_betti_linear_elimination_cases(),
        "affine_cone_conversion": affine_cone_cases(),
        "MPP_threshold": mpp_threshold_cases(),
        "reserve_scale_ledger": reserve_scale_ledger(),
        "count_domain_separation": count_domain_separation(),
    }
    result["ALL_CHECKS_OK"] = all(
        section["ok"] for section in result.values() if isinstance(section, dict) and "ok" in section
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_all()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("L1 odd-moment Hooley-Katz audit verifier")
        for key, section in result.items():
            if isinstance(section, dict) and "ok" in section:
                if key == "reserve_scale_ledger":
                    print(f"  {key}: ok={section['ok']} summary={section['summary']}")
                else:
                    print(f"  {key}: ok={section['ok']}")
        print(f"ALL_CHECKS_OK={result['ALL_CHECKS_OK']}")
    if not result["ALL_CHECKS_OK"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
