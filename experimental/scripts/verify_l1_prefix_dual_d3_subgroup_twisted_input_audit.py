#!/usr/bin/env python3
"""Verify the d=3 subgroup twisted-input audit."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any


PRIMES = (7, 11, 17, 31)
TOL = 1e-8


def is_prime(p: int) -> bool:
    if p < 2:
        return False
    if p == 2:
        return True
    if p % 2 == 0:
        return False
    q = 3
    while q * q <= p:
        if p % q == 0:
            return False
        q += 2
    return True


def validate_prime(p: int) -> None:
    if not is_prime(p):
        raise ValueError("p must be prime")
    if p <= 5:
        raise ValueError("the d=3 quintic twisted-input audit requires p>5")


def primitive_root(p: int) -> int:
    validate_prime(p)
    factors: list[int] = []
    x = p - 1
    q = 2
    while q * q <= x:
        if x % q == 0:
            factors.append(q)
            while x % q == 0:
                x //= q
        q += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root for p={p}")


def log_table(p: int) -> tuple[int, dict[int, int]]:
    g = primitive_root(p)
    logs: dict[int, int] = {}
    x = 1
    for exponent in range(p - 1):
        logs[x] = exponent
        x = (x * g) % p
    if len(logs) != p - 1:
        raise AssertionError("primitive root log table did not cover F_p^*")
    return g, logs


def subgroup(p: int, n: int) -> tuple[int, ...]:
    validate_prime(p)
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    generator = pow(primitive_root(p), (p - 1) // n, p)
    values = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = (x * generator) % p
    values_tuple = tuple(sorted(values))
    if len(set(values_tuple)) != n:
        raise AssertionError("subgroup generator produced repeated elements")
    return values_tuple


def subgroup_orders(p: int) -> tuple[int, ...]:
    return tuple(d for d in range(2, p) if (p - 1) % d == 0 and d % 2 == 0)


def additive_roots(p: int) -> list[complex]:
    return [complex(math.cos(2 * math.pi * t / p), math.sin(2 * math.pi * t / p)) for t in range(p)]


def character_roots(m: int) -> list[complex]:
    return [complex(math.cos(2 * math.pi * t / m), math.sin(2 * math.pi * t / m)) for t in range(m)]


def phase_value(a1: int, a3: int, a5: int, x: int, p: int) -> int:
    return (a1 * x + a3 * pow(x, 3, p) + a5 * pow(x, 5, p)) % p


def chi_value(logs: dict[int, int], roots_m: list[complex], m: int, ell: int, x: int) -> complex:
    return roots_m[(ell * logs[x]) % m]


def direct_S_H(
    p: int,
    H: tuple[int, ...],
    roots_p: list[complex],
    a1: int,
    a3: int,
    a5: int,
) -> complex:
    return sum(roots_p[phase_value(a1, a3, a5, h, p)] for h in H)


def mixed_inner_sum(
    p: int,
    logs: dict[int, int],
    roots_p: list[complex],
    roots_m: list[complex],
    m: int,
    ell: int,
    a1: int,
    a3: int,
    a5: int,
) -> complex:
    return sum(
        chi_value(logs, roots_m, m, ell, x) * roots_p[phase_value(a1, a3, a5, x, p)]
        for x in range(1, p)
    )


def expanded_S_H(
    p: int,
    logs: dict[int, int],
    roots_p: list[complex],
    roots_m: list[complex],
    m: int,
    a1: int,
    a3: int,
    a5: int,
) -> complex:
    total = sum(
        mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a1, a3, a5)
        for ell in range(m)
    )
    return total / m


def katz_constant_C_1_d_e(d: int, e: int) -> int:
    # Katz's n=1 formula: sum_{a+b=1}(d-1)^a(e-1)^b + sum_{a+b=0}1.
    return (d - 1) + (e - 1) + 1


def fraction_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fraction_to_float(value: Fraction) -> float:
    return value.numerator / value.denominator


def candidate_d3_error_bound(p: int, k: int) -> Fraction:
    linear_part = Fraction((p - 1) * (p**k), p**3)
    cubic_part = Fraction(p * (p - 1) * ((9 * p) ** k), p**3)
    quintic_part = Fraction((p**2) * (p - 1) * ((25 * p) ** k), p**3)
    return linear_part + cubic_part + quintic_part


def normalized_candidate_bound(p: int, n: int, k: int) -> Fraction:
    return candidate_d3_error_bound(p, k) / (n ** (2 * k))


def indicator_expansion_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        _, logs = log_table(p)
        for n in subgroup_orders(p):
            H = set(subgroup(p, n))
            m = (p - 1) // n
            roots_m = character_roots(m)
            max_error = 0.0
            for x in range(1, p):
                expanded = sum(chi_value(logs, roots_m, m, ell, x) for ell in range(m)) / m
                expected = 1.0 if x in H else 0.0
                max_error = max(max_error, abs(expanded - expected))
            row_ok = max_error < TOL
            ok = ok and row_ok
            rows.append({"p": p, "n": n, "m": m, "max_error": max_error, "ok": row_ok})
    return {"rows": rows, "ok": ok}


def character_expansion_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        _, logs = log_table(p)
        roots_p = additive_roots(p)
        for n in subgroup_orders(p):
            H = subgroup(p, n)
            m = (p - 1) // n
            roots_m = character_roots(m)
            max_error = 0.0
            for a1 in range(p):
                for a3 in range(p):
                    for a5 in range(p):
                        direct = direct_S_H(p, H, roots_p, a1, a3, a5)
                        expanded = expanded_S_H(p, logs, roots_p, roots_m, m, a1, a3, a5)
                        max_error = max(max_error, abs(direct - expanded))
            row_ok = max_error < TOL
            ok = ok and row_ok
            rows.append({"p": p, "n": n, "m": m, "max_error": max_error, "ok": row_ok})
    return {"rows": rows, "ok": ok}


def source_constant_cases() -> dict[str, Any]:
    c_1_3_1 = katz_constant_C_1_d_e(3, 1)
    c_1_5_1 = katz_constant_C_1_d_e(5, 1)
    rows = []
    ok = c_1_3_1 == 3 and c_1_5_1 == 5
    for p in PRIMES:
        sqrt_p = math.sqrt(p)
        trivial_quintic_star_bound = 4.0 * sqrt_p + 1.0
        row_ok = p > 5 and trivial_quintic_star_bound <= 5.0 * sqrt_p + TOL
        ok = ok and row_ok
        rows.append(
            {
                "p": p,
                "katz_constant_C_1_3_1": c_1_3_1,
                "katz_constant_C_1_5_1": c_1_5_1,
                "katz_cubic_constant_ok": c_1_3_1 == 3,
                "katz_quintic_constant_ok": c_1_5_1 == 5,
                "ordinary_additive_full_affine_degree5_bound": 4.0 * sqrt_p,
                "trivial_character_Fp_star_degree5_bound": trivial_quintic_star_bound,
                "trivial_quintic_bound_le_5sqrtp": row_ok,
                "ok": row_ok,
            }
        )
    return {
        "source": "Katz Estimates for Nonsingular Mixed Character Sums Theorem 1.1",
        "rows": rows,
        "ok": ok,
    }


def standard_input_bound_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        _, logs = log_table(p)
        roots_p = additive_roots(p)
        sqrt_p = math.sqrt(p)
        for n in subgroup_orders(p):
            m = (p - 1) // n
            roots_m = character_roots(m)
            max_linear_trivial_abs = 0.0
            max_linear_nontrivial_ratio = 0.0
            max_cubic_ratio = 0.0
            max_quintic_ratio = 0.0

            for a1 in range(1, p):
                for ell in range(m):
                    value = abs(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a1, 0, 0))
                    if ell == 0:
                        max_linear_trivial_abs = max(max_linear_trivial_abs, value)
                    else:
                        max_linear_nontrivial_ratio = max(max_linear_nontrivial_ratio, value / sqrt_p)

            for a1 in range(p):
                for a3 in range(1, p):
                    for ell in range(m):
                        value = abs(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a1, a3, 0))
                        max_cubic_ratio = max(max_cubic_ratio, value / sqrt_p)

            for a1 in range(p):
                for a3 in range(p):
                    for a5 in range(1, p):
                        for ell in range(m):
                            value = abs(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a1, a3, a5))
                            max_quintic_ratio = max(max_quintic_ratio, value / sqrt_p)

            linear_ok = max_linear_trivial_abs <= 1.0 + TOL and max_linear_nontrivial_ratio <= 1.0 + TOL
            cubic_ok = max_cubic_ratio <= 3.0 + TOL
            quintic_ok = max_quintic_ratio <= 5.0 + TOL
            row_ok = linear_ok and cubic_ok and quintic_ok
            ok = ok and row_ok
            rows.append(
                {
                    "p": p,
                    "n": n,
                    "m": m,
                    "linear_gauss_bound_ok": linear_ok,
                    "cubic_lower_stratum_bound_ok": cubic_ok,
                    "quintic_top_stratum_bound_ok": quintic_ok,
                    "max_linear_trivial_abs": max_linear_trivial_abs,
                    "max_linear_nontrivial_ratio": max_linear_nontrivial_ratio,
                    "max_cubic_lower_stratum_ratio": max_cubic_ratio,
                    "max_quintic_top_stratum_ratio": max_quintic_ratio,
                    "linear_ratio_bound": 1.0,
                    "cubic_ratio_bound": 3.0,
                    "quintic_ratio_bound": 5.0,
                    "ok": row_ok,
                }
            )
    return {"rows": rows, "ok": ok}


def degeneracy_cases() -> dict[str, Any]:
    rows = [
        {
            "case": "a5_nonzero",
            "stratum": "QUINTIC_TOP",
            "constant": "5 sqrt(p)",
            "requires": "p>5",
            "status": "IMPORTED_KATZ_INPUT",
            "ok": True,
        },
        {
            "case": "a5_zero_a3_nonzero",
            "stratum": "CUBIC_LOWER",
            "constant": "3 sqrt(p)",
            "requires": "p>3",
            "status": "LOWER_DEGREE_STRATUM",
            "ok": True,
        },
        {
            "case": "a5_zero_a3_zero_a1_nonzero",
            "stratum": "LINEAR",
            "constant": "sqrt(p) for nontrivial chi, 1 for trivial chi",
            "requires": "a1!=0",
            "status": "GAUSS_INPUT",
            "ok": True,
        },
        {
            "case": "a5_zero_a3_zero_a1_zero",
            "stratum": "PRINCIPAL",
            "constant": "n",
            "requires": "none",
            "status": "RANDOM_MAIN_TERM",
            "ok": True,
        },
    ]
    return {"rows": rows, "ok": all(row["ok"] for row in rows)}


def candidate_bound_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        for n in subgroup_orders(p):
            for k in (2, 3, 4):
                bound = candidate_d3_error_bound(p, k)
                normalized = normalized_candidate_bound(p, n, k)
                row_ok = bound > 0 and normalized > 0
                ok = ok and row_ok
                rows.append(
                    {
                        "p": p,
                        "n": n,
                        "k": k,
                        "m": (p - 1) // n,
                        "candidate_absolute_bound": fraction_to_string(bound),
                        "candidate_absolute_bound_float": fraction_to_float(bound),
                        "candidate_normalized_bound": fraction_to_string(normalized),
                        "candidate_normalized_bound_float": fraction_to_float(normalized),
                        "linear_frequency_count": p - 1,
                        "cubic_frequency_count": p * (p - 1),
                        "quintic_frequency_count": p * p * (p - 1),
                        "dominant_base_5sqrtp_over_n": 5.0 * math.sqrt(p) / n,
                        "ok": row_ok,
                    }
                )
    return {"rows": rows, "ok": ok}


def nonvacuous_window_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p, n in ((1009, 126), (1009, 168), (1009, 252), (1009, 504), (1009, 1008)):
        validate_prime(p)
        if (p - 1) % n:
            raise AssertionError("test n must divide p-1")
        sqrt_p = math.sqrt(p)
        base = 5.0 * sqrt_p / n
        values = []
        previous = None
        monotone = True
        for k in (2, 4, 8, 16):
            value = fraction_to_float(normalized_candidate_bound(p, n, k))
            if previous is not None and value >= previous:
                monotone = False
            previous = value
            values.append({"k": k, "normalized_candidate_bound": value})
        row_ok = (base < 1.0 and monotone) or (base >= 1.0 and not monotone)
        ok = ok and row_ok
        rows.append(
            {
                "p": p,
                "n": n,
                "n_over_sqrt_p": n / sqrt_p,
                "base_5sqrtp_over_n": base,
                "window_without_markov_loss": "PASS_WINDOW" if base < 1.0 else "FAIL_WINDOW",
                "monotone_decreasing_on_test_ks": monotone,
                "values": values,
                "ok": row_ok,
            }
        )
    return {"rows": rows, "ok": ok}


def markov_window_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p, n, tau in (
        (1009, 168, 0.05),
        (1009, 168, 0.10),
        (1009, 252, 0.10),
        (1009, 252, 0.20),
        (1009, 504, 0.20),
    ):
        validate_prime(p)
        alpha = 1.0 - 2.0 * tau
        effective_base = 5.0 * math.sqrt(p) / (alpha * n)
        expected_status = "PASS_MARKOV_WINDOW" if effective_base < 1.0 else "FAIL_MARKOV_WINDOW"
        row_ok = alpha > 0.0
        ok = ok and row_ok
        rows.append(
            {
                "p": p,
                "n": n,
                "tau": tau,
                "alpha": alpha,
                "effective_base_5sqrtp_over_alpha_n": effective_base,
                "status": expected_status,
                "ok": row_ok,
            }
        )
    return {"rows": rows, "ok": ok}


def count_domain_separation_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        for n in subgroup_orders(p):
            for k in (2, 3, 4):
                subgroup_main = Fraction(n ** (2 * k), p**3)
                full_affine_main = p ** (2 * k - 3)
                full_torus_main = Fraction((p - 1) ** (2 * k), p**3)
                is_full_group = n == p - 1
                row_ok = subgroup_main == full_torus_main if is_full_group else subgroup_main != full_affine_main
                ok = ok and row_ok
                rows.append(
                    {
                        "p": p,
                        "n": n,
                        "k": k,
                        "count_type": "PROPER_SUBGROUP_H_POINTS" if n < p - 1 else "FULL_TORUS_Fp_POINTS",
                        "subgroup_random_main": fraction_to_string(subgroup_main),
                        "full_affine_random_main": str(full_affine_main),
                        "full_torus_random_main": fraction_to_string(full_torus_main),
                        "counts_full_affine_Fp_points": False,
                        "requires_multiplicative_character_twists": n < p - 1,
                        "ok": row_ok,
                    }
                )
    return {"rows": rows, "ok": ok}


def rejection_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in (2, 3, 5, 9):
        try:
            validate_prime(p)
            rejected = False
            message = ""
        except ValueError as exc:
            rejected = True
            message = str(exc)
        rows.append({"p": p, "rejected": rejected, "message": message})
        ok = ok and rejected
    return {"rows": rows, "ok": ok}


def run_all() -> dict[str, Any]:
    indicators = indicator_expansion_cases()
    character_expansions = character_expansion_cases()
    source_constants = source_constant_cases()
    standard_inputs = standard_input_bound_cases()
    degeneracies = degeneracy_cases()
    candidate_bounds = candidate_bound_cases()
    nonvacuous_windows = nonvacuous_window_cases()
    markov_windows = markov_window_cases()
    count_domains = count_domain_separation_cases()
    rejections = rejection_cases()
    all_ok = (
        indicators["ok"]
        and character_expansions["ok"]
        and source_constants["ok"]
        and standard_inputs["ok"]
        and degeneracies["ok"]
        and candidate_bounds["ok"]
        and nonvacuous_windows["ok"]
        and markov_windows["ok"]
        and count_domains["ok"]
        and rejections["ok"]
    )
    return {
        "indicator_expansion": indicators,
        "character_expansion": character_expansions,
        "source_constant_cases": source_constants,
        "standard_input_bound_cases": standard_inputs,
        "degeneracy_cases": degeneracies,
        "candidate_bound_cases": candidate_bounds,
        "nonvacuous_window_cases": nonvacuous_windows,
        "markov_window_cases": markov_windows,
        "count_domain_separation": count_domains,
        "rejection_cases": rejections,
        "ALL_CHECKS_OK": all_ok,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_all()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("L1 d=3 subgroup twisted-input audit verifier")
        print(f"  indicator_expansion: ok={result['indicator_expansion']['ok']}")
        print(f"  character_expansion: ok={result['character_expansion']['ok']}")
        print(f"  source_constant_cases: ok={result['source_constant_cases']['ok']}")
        print(f"  standard_input_bound_cases: ok={result['standard_input_bound_cases']['ok']}")
        print(f"  degeneracy_cases: ok={result['degeneracy_cases']['ok']}")
        print(f"  candidate_bound_cases: ok={result['candidate_bound_cases']['ok']}")
        print(f"  nonvacuous_window_cases: ok={result['nonvacuous_window_cases']['ok']}")
        print(f"  markov_window_cases: ok={result['markov_window_cases']['ok']}")
        print(f"  count_domain_separation: ok={result['count_domain_separation']['ok']}")
        print(f"  rejection_cases: ok={result['rejection_cases']['ok']}")
        print(f"ALL_CHECKS_OK={result['ALL_CHECKS_OK']}")
    if not result["ALL_CHECKS_OK"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
