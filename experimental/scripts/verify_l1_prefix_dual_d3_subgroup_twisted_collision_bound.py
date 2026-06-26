#!/usr/bin/env python3
"""Verify the d=3 proper-subgroup twisted collision bound."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from collections import Counter
from fractions import Fraction
from typing import Any


PRIMES = (7, 11, 17, 31)
K_VALUES = (2, 3)
DIRECT_PAIR_BUDGET = 2_000_000
TOL = 1e-8
FOURIER_TOL = 1e-4


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
        raise ValueError("the d=3 twisted collision bound requires p>5")


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
    return tuple(d for d in range(1, p) if (p - 1) % d == 0)


def powers_for_domain(domain: tuple[int, ...], p: int) -> dict[int, tuple[int, int, int]]:
    return {x: (x, pow(x, 3, p), pow(x, 5, p)) for x in domain}


def phase_value(a1: int, a3: int, a5: int, x: int, p: int) -> int:
    return (a1 * x + a3 * pow(x, 3, p) + a5 * pow(x, 5, p)) % p


def additive_roots(p: int) -> list[complex]:
    return [complex(math.cos(2 * math.pi * t / p), math.sin(2 * math.pi * t / p)) for t in range(p)]


def character_roots(m: int) -> list[complex]:
    return [complex(math.cos(2 * math.pi * t / m), math.sin(2 * math.pi * t / m)) for t in range(m)]


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


def moment_key(tup: tuple[int, ...], p: int) -> tuple[int, int, int]:
    powers = powers_for_domain(tuple(set(tup)), p)
    return (
        sum(powers[x][0] for x in tup) % p,
        sum(powers[x][1] for x in tup) % p,
        sum(powers[x][2] for x in tup) % p,
    )


def moment_histogram(domain: tuple[int, ...], p: int, k: int) -> Counter[tuple[int, int, int]]:
    powers = powers_for_domain(domain, p)
    hist: Counter[tuple[int, int, int]] = Counter()
    for tup in itertools.product(domain, repeat=k):
        hist[
            (
                sum(powers[x][0] for x in tup) % p,
                sum(powers[x][1] for x in tup) % p,
                sum(powers[x][2] for x in tup) % p,
            )
        ] += 1
    return hist


def count_from_histogram(hist: Counter[tuple[int, int, int]]) -> int:
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
    roots = additive_roots(p)
    powers = tuple(powers_for_domain(domain, p).values())
    total = 0.0
    for a1 in range(p):
        for a3 in range(p):
            for a5 in range(p):
                value = 0j
                for x1, x3, x5 in powers:
                    value += roots[(a1 * x1 + a3 * x3 + a5 * x5) % p]
                abs_square = value.real * value.real + value.imag * value.imag
                total += abs_square**k
    reconstructed = total / (p**3)
    rounded = int(round(reconstructed))
    return {
        "rounded_count": rounded,
        "rounding_error": abs(reconstructed - rounded),
    }


def fraction_to_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def fraction_to_float(value: Fraction) -> float:
    return value.numerator / value.denominator


def subgroup_error_bound(p: int, k: int) -> Fraction:
    linear_part = Fraction((p - 1) * (p**k), p**3)
    cubic_part = Fraction(p * (p - 1) * ((9 * p) ** k), p**3)
    quintic_part = Fraction((p**2) * (p - 1) * ((25 * p) ** k), p**3)
    return linear_part + cubic_part + quintic_part


def normalized_error_bound(p: int, n: int, k: int) -> Fraction:
    return subgroup_error_bound(p, k) / (n ** (2 * k))


def katz_constant_C_1_d_e(d: int, e: int) -> int:
    # Katz's n=1 formula: sum_{a+b=1}(d-1)^a(e-1)^b + sum_{a+b=0}1.
    return (d - 1) + (e - 1) + 1


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

            gauss_ok = max_linear_trivial_abs <= 1.0 + TOL and max_linear_nontrivial_ratio <= 1.0 + TOL
            cubic_ok = max_cubic_ratio <= 3.0 + TOL
            quintic_ok = max_quintic_ratio <= 5.0 + TOL
            row_ok = gauss_ok and cubic_ok and quintic_ok
            ok = ok and row_ok
            rows.append(
                {
                    "p": p,
                    "n": n,
                    "m": m,
                    "gauss_linear_bound_ok": gauss_ok,
                    "cubic_mixed_bound_ok": cubic_ok,
                    "quintic_mixed_bound_ok": quintic_ok,
                    "max_observed_linear_trivial_abs": max_linear_trivial_abs,
                    "max_observed_linear_nontrivial_ratio": max_linear_nontrivial_ratio,
                    "max_observed_cubic_ratio": max_cubic_ratio,
                    "max_observed_quintic_ratio": max_quintic_ratio,
                    "linear_nontrivial_ratio_bound": 1.0,
                    "linear_trivial_abs_bound": 1.0,
                    "cubic_ratio_bound": 3.0,
                    "quintic_ratio_bound": 5.0,
                    "ok": row_ok,
                }
            )
    return {"rows": rows, "ok": ok}


def stratum_count_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        principal = 1
        linear = p - 1
        cubic = p * (p - 1)
        quintic = p * p * (p - 1)
        row_ok = principal + linear + cubic + quintic == p**3
        ok = ok and row_ok
        rows.append(
            {
                "p": p,
                "principal_count": principal,
                "linear_count": linear,
                "cubic_lower_count": cubic,
                "quintic_top_count": quintic,
                "total": principal + linear + cubic + quintic,
                "expected_total": p**3,
                "ok": row_ok,
            }
        )
    return {"rows": rows, "ok": ok}


def stratum_bound_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        roots_p = additive_roots(p)
        sqrt_p = math.sqrt(p)
        for n in subgroup_orders(p):
            H = subgroup(p, n)
            principal_abs = abs(direct_S_H(p, H, roots_p, 0, 0, 0))
            max_linear = 0.0
            max_cubic = 0.0
            max_quintic = 0.0
            for a1 in range(1, p):
                max_linear = max(max_linear, abs(direct_S_H(p, H, roots_p, a1, 0, 0)))
            for a1 in range(p):
                for a3 in range(1, p):
                    max_cubic = max(max_cubic, abs(direct_S_H(p, H, roots_p, a1, a3, 0)))
            for a1 in range(p):
                for a3 in range(p):
                    for a5 in range(1, p):
                        max_quintic = max(max_quintic, abs(direct_S_H(p, H, roots_p, a1, a3, a5)))
            row_ok = (
                abs(principal_abs - n) <= TOL
                and max_linear <= sqrt_p + TOL
                and max_cubic <= 3.0 * sqrt_p + TOL
                and max_quintic <= 5.0 * sqrt_p + TOL
            )
            ok = ok and row_ok
            rows.append(
                {
                    "p": p,
                    "n": n,
                    "m": (p - 1) // n,
                    "principal_abs": principal_abs,
                    "linear_max_abs": max_linear,
                    "cubic_lower_max_abs": max_cubic,
                    "quintic_top_max_abs": max_quintic,
                    "linear_bound": sqrt_p,
                    "cubic_lower_bound": 3.0 * sqrt_p,
                    "quintic_top_bound": 5.0 * sqrt_p,
                    "ok": row_ok,
                }
            )
    return {"rows": rows, "ok": ok}


def collision_count_row(p: int, n: int, k: int) -> dict[str, Any]:
    H = subgroup(p, n)
    hist = moment_histogram(H, p, k)
    exact_count = count_from_histogram(hist)
    direct = direct_pair_count(H, p, k)
    if direct["status"] == "PASS" and direct["count"] != exact_count:
        raise AssertionError((p, n, k, direct["count"], exact_count))
    fourier = fourier_reconstruction_count(H, p, k)
    if fourier["rounded_count"] != exact_count or fourier["rounding_error"] > FOURIER_TOL:
        raise AssertionError((p, n, k, fourier, exact_count))

    random_main = Fraction(n ** (2 * k), p**3)
    error = Fraction(exact_count, 1) - random_main
    bound = subgroup_error_bound(p, k)
    normalized_error = error / (n ** (2 * k))
    normalized_bound = normalized_error_bound(p, n, k)
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
        "histogram_reconstruction": {
            "status": "PASS",
            "tuple_count": n**k,
            "bucket_count": len(hist),
            "exact_count": exact_count,
        },
        "fourier_reconstruction": fourier,
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


def count_domain_separation_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p in PRIMES:
        for n in subgroup_orders(p):
            for k in K_VALUES:
                subgroup_main = Fraction(n ** (2 * k), p**3)
                full_affine_main = p ** (2 * k - 3)
                full_torus_main = Fraction((p - 1) ** (2 * k), p**3)
                is_full_group = n == p - 1
                row_ok = True
                if is_full_group:
                    row_ok = subgroup_main == full_torus_main
                else:
                    row_ok = subgroup_main != full_affine_main and subgroup_main != full_torus_main
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


def exponential_decay_cases() -> dict[str, Any]:
    rows = []
    ok = True
    for p, n in ((1009, 168), (1009, 252), (1009, 504), (1009, 1008)):
        validate_prime(p)
        if (p - 1) % n:
            raise AssertionError("test n must divide p-1")
        base = 5.0 * math.sqrt(p) / n
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
                "base_5sqrtp_over_n": base,
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
    stratum_counts = stratum_count_cases()
    stratum_bounds = stratum_bound_cases()
    collisions = collision_count_cases()
    count_domains = count_domain_separation_cases()
    exponential_decay = exponential_decay_cases()
    rejections = rejection_cases()
    all_ok = (
        indicators["ok"]
        and character_expansions["ok"]
        and source_constants["ok"]
        and standard_inputs["ok"]
        and stratum_counts["ok"]
        and stratum_bounds["ok"]
        and collisions["ok"]
        and count_domains["ok"]
        and exponential_decay["ok"]
        and rejections["ok"]
    )
    return {
        "indicator_expansion": indicators,
        "character_expansion": character_expansions,
        "source_constant_cases": source_constants,
        "standard_input_bound_cases": standard_inputs,
        "stratum_count_cases": stratum_counts,
        "stratum_bound_cases": stratum_bounds,
        "collision_counts": collisions,
        "count_domain_separation": count_domains,
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
        print("L1 d=3 proper-subgroup twisted collision verifier")
        print(f"  indicator_expansion: ok={result['indicator_expansion']['ok']}")
        print(f"  character_expansion: ok={result['character_expansion']['ok']}")
        print(f"  source_constant_cases: ok={result['source_constant_cases']['ok']}")
        print(f"  standard_input_bound_cases: ok={result['standard_input_bound_cases']['ok']}")
        print(f"  stratum_count_cases: ok={result['stratum_count_cases']['ok']}")
        print(f"  stratum_bound_cases: ok={result['stratum_bound_cases']['ok']}")
        print(
            "  collision_counts: ok={ok} summary={summary}".format(
                ok=result["collision_counts"]["ok"],
                summary=result["collision_counts"]["summary"],
            )
        )
        print(f"  count_domain_separation: ok={result['count_domain_separation']['ok']}")
        print(f"  exponential_decay: ok={result['exponential_decay']['ok']}")
        print(f"  rejection_cases: ok={result['rejection_cases']['ok']}")
        print(f"ALL_CHECKS_OK={result['ALL_CHECKS_OK']}")
    if not result["ALL_CHECKS_OK"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
