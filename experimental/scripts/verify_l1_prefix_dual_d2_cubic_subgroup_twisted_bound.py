#!/usr/bin/env python3
"""Verify the d=2 cubic proper-subgroup twisted moment bound."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from typing import Any

import mpmath as mp


PRIMES = (7, 11, 17, 31)
K_VALUES = (2, 3, 4)
DIRECT_PAIR_BUDGET = 2_000_000
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
    if p <= 3:
        raise ValueError("the cubic twisted bound requires p>3")


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


def phase_value(a: int, b: int, x: int, p: int) -> int:
    return (a * x + b * pow(x, 3, p)) % p


def additive_roots(p: int) -> list[complex]:
    return [complex(math.cos(2 * math.pi * t / p), math.sin(2 * math.pi * t / p)) for t in range(p)]


def character_roots(m: int) -> list[complex]:
    return [complex(math.cos(2 * math.pi * t / m), math.sin(2 * math.pi * t / m)) for t in range(m)]


def chi_value(logs: dict[int, int], roots_m: list[complex], m: int, ell: int, x: int) -> complex:
    return roots_m[(ell * logs[x]) % m]


def direct_S_H(p: int, H: tuple[int, ...], roots_p: list[complex], a: int, b: int) -> complex:
    return sum(roots_p[phase_value(a, b, h, p)] for h in H)


def mixed_inner_sum(
    p: int,
    logs: dict[int, int],
    roots_p: list[complex],
    roots_m: list[complex],
    m: int,
    ell: int,
    a: int,
    b: int,
) -> complex:
    return sum(
        chi_value(logs, roots_m, m, ell, x) * roots_p[phase_value(a, b, x, p)]
        for x in range(1, p)
    )


def expanded_S_H(
    p: int,
    logs: dict[int, int],
    roots_p: list[complex],
    roots_m: list[complex],
    m: int,
    a: int,
    b: int,
) -> complex:
    return sum(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a, b) for ell in range(m)) / m


def moment_key(tup: tuple[int, ...], p: int) -> tuple[int, int]:
    return sum(tup) % p, sum(pow(x, 3, p) for x in tup) % p


def moment_histogram(domain: tuple[int, ...], p: int, k: int) -> Counter[tuple[int, int]]:
    cubes = {x: pow(x, 3, p) for x in domain}
    hist: Counter[tuple[int, int]] = Counter()
    for tup in itertools.product(domain, repeat=k):
        hist[(sum(tup) % p, sum(cubes[x] for x in tup) % p)] += 1
    return hist


def count_from_histogram(hist: Counter[tuple[int, int]]) -> int:
    return sum(count * count for count in hist.values())


def direct_pair_count(domain: tuple[int, ...], p: int, k: int) -> dict[str, Any]:
    pair_space = len(domain) ** (2 * k)
    if pair_space > DIRECT_PAIR_BUDGET:
        return {
            "status": "SKIPPED_BUDGET",
            "pair_space": pair_space,
            "budget": DIRECT_PAIR_BUDGET,
        }
    tuples = list(itertools.product(domain, repeat=k))
    keys = [moment_key(tup, p) for tup in tuples]
    count = 0
    for left_key in keys:
        for right_key in keys:
            if left_key == right_key:
                count += 1
    return {
        "status": "PASS",
        "pair_space": pair_space,
        "count": count,
    }


def fourier_reconstruction_count(domain: tuple[int, ...], p: int, k: int) -> dict[str, Any]:
    mp.mp.dps = 90
    roots = [mp.e ** (2j * mp.pi * t / p) for t in range(p)]
    cubes = {x: pow(x, 3, p) for x in domain}
    total = mp.mpf("0")
    for a in range(p):
        for b in range(p):
            value = mp.mpc(0)
            for x in domain:
                value += roots[(a * x + b * cubes[x]) % p]
            abs_square = value.real * value.real + value.imag * value.imag
            total += abs_square**k
    reconstructed = total / (p * p)
    rounded = int(mp.floor(reconstructed + mp.mpf("0.5")))
    return {
        "rounded_count": rounded,
        "rounding_error": float(abs(reconstructed - rounded)),
    }


def fraction_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fraction_to_float(value: Fraction) -> float:
    return value.numerator / value.denominator


def subgroup_error_bound(p: int, k: int) -> Fraction:
    linear_part = Fraction((p - 1) * (p**k), p * p)
    cubic_part = Fraction((p - 1) * ((9 * p) ** k), p)
    return linear_part + cubic_part


def normalized_error_bound(p: int, n: int, k: int) -> Fraction:
    return subgroup_error_bound(p, k) / (n ** (2 * k))


def katz_constant_C_1_d_e(d: int, e: int) -> int:
    # Katz's n=1 formula: sum_{a+b=1}(d-1)^a(e-1)^b + sum_{a+b=0}1.
    return (d - 1) + (e - 1) + 1


def prior_full_torus_bound_float(p: int, k: int) -> float:
    return (p - 1) / (p * p) + ((p - 1) / p) * (2 * math.sqrt(p) + 1) ** (2 * k)


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
            for a in range(p):
                for b in range(p):
                    direct = direct_S_H(p, H, roots_p, a, b)
                    expanded = expanded_S_H(p, logs, roots_p, roots_m, m, a, b)
                    max_error = max(max_error, abs(direct - expanded))
            row_ok = max_error < TOL
            ok = ok and row_ok
            rows.append({"p": p, "n": n, "m": m, "max_error": max_error, "ok": row_ok})
    return {"rows": rows, "ok": ok}


def twisted_sum_bound_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        _, logs = log_table(p)
        roots_p = additive_roots(p)
        sqrt_p = math.sqrt(p)
        for n in subgroup_orders(p):
            H = subgroup(p, n)
            m = (p - 1) // n
            roots_m = character_roots(m)
            max_SH_b0 = 0.0
            max_inner_b0_trivial = 0.0
            max_inner_b0_nontrivial = 0.0
            max_SH_bneq0 = 0.0
            max_inner_bneq0 = 0.0
            for a in range(1, p):
                max_SH_b0 = max(max_SH_b0, abs(direct_S_H(p, H, roots_p, a, 0)))
                for ell in range(m):
                    inner = abs(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a, 0))
                    if ell == 0:
                        max_inner_b0_trivial = max(max_inner_b0_trivial, inner)
                    else:
                        max_inner_b0_nontrivial = max(max_inner_b0_nontrivial, inner)
            for a in range(p):
                for b in range(1, p):
                    max_SH_bneq0 = max(max_SH_bneq0, abs(direct_S_H(p, H, roots_p, a, b)))
                    for ell in range(m):
                        max_inner_bneq0 = max(
                            max_inner_bneq0,
                            abs(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a, b)),
                        )
            row_ok = (
                max_SH_b0 <= sqrt_p + TOL
                and max_inner_b0_trivial <= 1.0 + TOL
                and max_inner_b0_nontrivial <= sqrt_p + TOL
                and max_SH_bneq0 <= 3.0 * sqrt_p + TOL
                and max_inner_bneq0 <= 3.0 * sqrt_p + TOL
            )
            ok = ok and row_ok
            rows.append(
                {
                    "p": p,
                    "n": n,
                    "m": m,
                    "sqrt_p": sqrt_p,
                    "max_abs_S_H_b0_a_nonzero": max_SH_b0,
                    "max_abs_inner_b0_trivial": max_inner_b0_trivial,
                    "max_abs_inner_b0_nontrivial": max_inner_b0_nontrivial,
                    "max_abs_S_H_b_nonzero": max_SH_bneq0,
                    "max_abs_inner_b_nonzero": max_inner_bneq0,
                    "linear_bound": sqrt_p,
                    "cubic_bound": 3.0 * sqrt_p,
                    "ok": row_ok,
                }
            )
    return {"rows": rows, "ok": ok}


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
            max_b0_abs = 0.0
            max_b0_ratio = 0.0
            max_b0_trivial_abs = 0.0
            max_b0_nontrivial_ratio = 0.0
            max_b_nonzero_abs = 0.0
            max_b_nonzero_ratio = 0.0
            for a in range(1, p):
                for ell in range(m):
                    value = abs(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a, 0))
                    max_b0_abs = max(max_b0_abs, value)
                    max_b0_ratio = max(max_b0_ratio, value / sqrt_p)
                    if ell == 0:
                        max_b0_trivial_abs = max(max_b0_trivial_abs, value)
                    else:
                        max_b0_nontrivial_ratio = max(max_b0_nontrivial_ratio, value / sqrt_p)
            for a in range(p):
                for b in range(1, p):
                    for ell in range(m):
                        value = abs(mixed_inner_sum(p, logs, roots_p, roots_m, m, ell, a, b))
                        max_b_nonzero_abs = max(max_b_nonzero_abs, value)
                        max_b_nonzero_ratio = max(max_b_nonzero_ratio, value / sqrt_p)
            gauss_ok = max_b0_trivial_abs <= 1.0 + TOL and max_b0_nontrivial_ratio <= 1.0 + TOL
            twisted_ok = max_b_nonzero_ratio <= 3.0 + TOL
            row_ok = gauss_ok and twisted_ok
            ok = ok and row_ok
            rows.append(
                {
                    "p": p,
                    "n": n,
                    "m": m,
                    "gauss_linear_bound_ok": gauss_ok,
                    "twisted_cubic_bound_ok": twisted_ok,
                    "max_observed_b0_abs": max_b0_abs,
                    "max_observed_b0_ratio": max_b0_ratio,
                    "max_observed_b0_trivial_abs": max_b0_trivial_abs,
                    "max_observed_b0_nontrivial_ratio": max_b0_nontrivial_ratio,
                    "max_observed_b_nonzero_abs": max_b_nonzero_abs,
                    "max_observed_b_nonzero_ratio": max_b_nonzero_ratio,
                    "gauss_ratio_bound": 1.0,
                    "twisted_cubic_ratio_bound": 3.0,
                    "ok": row_ok,
                }
            )
    return {"rows": rows, "ok": ok}


def source_constant_cases() -> dict[str, Any]:
    c_1_3_1 = katz_constant_C_1_d_e(3, 1)
    rows = []
    ok = c_1_3_1 == 3
    for p in PRIMES:
        sqrt_p = math.sqrt(p)
        trivial_b_nonzero_bound = 2.0 * sqrt_p + 1.0
        row_ok = p > 3 and trivial_b_nonzero_bound <= 3.0 * sqrt_p + TOL
        ok = ok and row_ok
        rows.append(
            {
                "p": p,
                "katz_constant_C_1_3_1": c_1_3_1,
                "katz_constant_ok": c_1_3_1 == 3,
                "ordinary_additive_full_affine_degree3_bound": 2.0 * sqrt_p,
                "trivial_character_Fp_star_bound": trivial_b_nonzero_bound,
                "trivial_b_nonzero_bound_le_3sqrtp": row_ok,
                "ok": row_ok,
            }
        )
    return {
        "source": "Katz Estimates for Nonsingular Mixed Character Sums Theorem 1.1",
        "rows": rows,
        "ok": ok,
    }


def collision_count_row(p: int, n: int, k: int) -> dict[str, Any]:
    H = subgroup(p, n)
    hist = moment_histogram(H, p, k)
    exact_count = count_from_histogram(hist)
    direct = direct_pair_count(H, p, k)
    if direct["status"] == "PASS" and direct["count"] != exact_count:
        raise AssertionError((p, n, k, direct["count"], exact_count))
    fourier = fourier_reconstruction_count(H, p, k)
    if fourier["rounded_count"] != exact_count:
        raise AssertionError((p, n, k, fourier["rounded_count"], exact_count))

    random_main = Fraction(n ** (2 * k), p * p)
    error = Fraction(exact_count, 1) - random_main
    bound = subgroup_error_bound(p, k)
    normalized_bound = normalized_error_bound(p, n, k)
    normalized_error = error / (n ** (2 * k))
    row_ok = error >= 0 and error <= bound
    return {
        "p": p,
        "n": n,
        "k": k,
        "m": (p - 1) // n,
        "exact_count": exact_count,
        "random_main": fraction_to_string(random_main),
        "absolute_error": fraction_to_string(error),
        "absolute_error_float": fraction_to_float(error),
        "absolute_bound": fraction_to_string(bound),
        "absolute_bound_float": fraction_to_float(bound),
        "bound_ratio_to_error": None if error == 0 else fraction_to_float(bound / error),
        "normalized_error": fraction_to_string(normalized_error),
        "normalized_error_float": fraction_to_float(normalized_error),
        "normalized_bound": fraction_to_string(normalized_bound),
        "normalized_bound_float": fraction_to_float(normalized_bound),
        "direct_tuple_enumeration": direct,
        "fourier_reconstruction": fourier,
        "histogram_tuple_count": n**k,
        "histogram_bucket_count": len(hist),
        "full_group": n == p - 1,
        "proper_subgroup": n < p - 1,
        "ok": row_ok,
    }


def collision_count_cases() -> dict[str, Any]:
    rows = []
    ok = True
    direct_pass = 0
    direct_skipped = 0
    full_group_rows = 0
    proper_rows = 0
    for p in PRIMES:
        for n in subgroup_orders(p):
            for k in K_VALUES:
                row = collision_count_row(p, n, k)
                rows.append(row)
                ok = ok and row["ok"]
                if row["direct_tuple_enumeration"]["status"] == "PASS":
                    direct_pass += 1
                else:
                    direct_skipped += 1
                if row["full_group"]:
                    full_group_rows += 1
                else:
                    proper_rows += 1
    return {
        "rows": rows,
        "summary": {
            "row_count": len(rows),
            "direct_pair_pass": direct_pass,
            "direct_pair_skipped_budget": direct_skipped,
            "full_group_rows": full_group_rows,
            "proper_subgroup_rows": proper_rows,
        },
        "ok": ok,
    }


def full_group_benchmark_comparison_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        n = p - 1
        for k in K_VALUES:
            subgroup_bound = fraction_to_float(subgroup_error_bound(p, k))
            prior_torus_bound = prior_full_torus_bound_float(p, k)
            row_ok = subgroup_bound >= prior_torus_bound
            ok = ok and row_ok
            rows.append(
                {
                    "p": p,
                    "n": n,
                    "k": k,
                    "subgroup_twisted_bound": subgroup_bound,
                    "prior_full_torus_bound": prior_torus_bound,
                    "subgroup_bound_is_conservative": row_ok,
                    "ok": row_ok,
                }
            )
    return {"rows": rows, "ok": ok}


def count_domain_separation_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        for n in subgroup_orders(p):
            for k in K_VALUES:
                subgroup_main = Fraction(n ** (2 * k), p * p)
                full_affine_main = p ** (2 * k - 2)
                full_torus_main = Fraction((p - 1) ** (2 * k), p * p)
                is_full_group = n == p - 1
                row_ok = True
                if is_full_group:
                    row_ok = subgroup_main == full_torus_main
                else:
                    row_ok = subgroup_main != full_torus_main and subgroup_main != full_affine_main
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
                        "matches_full_torus_only_when_H_is_full_group": is_full_group,
                        "counts_full_affine_Fp_points": False,
                        "requires_multiplicative_character_twists": n < p - 1,
                        "ok": row_ok,
                    }
                )
    return {"rows": rows, "ok": ok}


def exponential_decay_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p, n in ((1009, 126), (1009, 252), (1009, 504)):
        validate_prime(p)
        if (p - 1) % n:
            raise AssertionError("test n must divide p-1")
        base = 3.0 * math.sqrt(p) / n
        row_values = []
        previous = None
        monotone = True
        for k in (2, 4, 8, 16):
            value = fraction_to_float(normalized_error_bound(p, n, k))
            if previous is not None and value >= previous:
                monotone = False
            previous = value
            row_values.append({"k": k, "normalized_bound": value})
        row_ok = base < 1.0 and monotone
        ok = ok and row_ok
        rows.append(
            {
                "p": p,
                "n": n,
                "base_3sqrtp_over_n": base,
                "n_over_sqrt_p": n / math.sqrt(p),
                "values": row_values,
                "monotone_decreasing_on_test_ks": monotone,
                "ok": row_ok,
            }
        )
    return {"rows": rows, "ok": ok}


def rejection_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in (2, 3, 4, 9):
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
    twisted_bounds = twisted_sum_bound_cases()
    standard_inputs = standard_input_bound_cases()
    source_constants = source_constant_cases()
    collisions = collision_count_cases()
    full_group_comparison = full_group_benchmark_comparison_cases()
    count_domain_separation = count_domain_separation_cases()
    exponential_decay = exponential_decay_cases()
    rejections = rejection_cases()
    all_ok = (
        indicators["ok"]
        and character_expansions["ok"]
        and twisted_bounds["ok"]
        and standard_inputs["ok"]
        and source_constants["ok"]
        and collisions["ok"]
        and full_group_comparison["ok"]
        and count_domain_separation["ok"]
        and exponential_decay["ok"]
        and rejections["ok"]
    )
    return {
        "indicator_expansion": indicators,
        "character_expansion": character_expansions,
        "twisted_sum_bounds": twisted_bounds,
        "standard_input_bound_cases": standard_inputs,
        "source_constant_cases": source_constants,
        "collision_counts": collisions,
        "full_group_benchmark_comparison": full_group_comparison,
        "count_domain_separation": count_domain_separation,
        "exponential_decay": exponential_decay,
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
        print("L1 d=2 cubic proper-subgroup twisted-bound verifier")
        print(f"  indicator_expansion: ok={result['indicator_expansion']['ok']}")
        print(f"  character_expansion: ok={result['character_expansion']['ok']}")
        print(f"  twisted_sum_bounds: ok={result['twisted_sum_bounds']['ok']}")
        print(f"  standard_input_bound_cases: ok={result['standard_input_bound_cases']['ok']}")
        print(f"  source_constant_cases: ok={result['source_constant_cases']['ok']}")
        print(
            "  collision_counts: ok={ok} summary={summary}".format(
                ok=result["collision_counts"]["ok"],
                summary=result["collision_counts"]["summary"],
            )
        )
        print(f"  full_group_benchmark_comparison: ok={result['full_group_benchmark_comparison']['ok']}")
        print(f"  count_domain_separation: ok={result['count_domain_separation']['ok']}")
        print(f"  exponential_decay: ok={result['exponential_decay']['ok']}")
        print(f"  rejection_cases: ok={result['rejection_cases']['ok']}")
        print(f"ALL_CHECKS_OK={result['ALL_CHECKS_OK']}")
    if not result["ALL_CHECKS_OK"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
