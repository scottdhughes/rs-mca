#!/usr/bin/env python3
"""Verify prime-power characteristic-zero prefix-fiber rigidity.

AUDIT / EXPERIMENTAL verifier for
`experimental/notes/l1/l1_prefix_prime_power_charzero_fibers.md`.

The script checks the iterated K_{ell^r} moment-rigidity theorem on small
prime-power domains, validates the exact anchored characteristic-zero fiber
formula, verifies the global maximum formula, and cross-checks the finite
F_17 prefix coordinates against top locator coefficients by Newton identities.

Prime-field / characteristic-zero prefix lane only.  This script does not
assert the arbitrary-word robust-shell theorem, RS list-decoding safety, MCA,
line-decoding, or protocol safety.
"""

import argparse
import itertools
import json
import sys
from collections import defaultdict
from math import comb
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from verify_l1_prefix_divisor_count import (  # noqa: E402
    poly_from_roots,
    subgroup,
    top_sigma_key,
)
from verify_l1_prefix_low_excess_norm_sieve import (  # noqa: E402
    collision_pairs,
    prefix_fibers,
)


def prime_power_base(n):
    for ell in range(2, n + 1):
        value = ell
        while value < n:
            value *= ell
        if value == n:
            return ell
    raise ValueError(f"n={n} is not a prime power")


def d_sigma(ell, sigma):
    d = 1
    while d <= sigma:
        d *= ell
    return d


def moment_zero_prime_power(coeffs, n, ell, j):
    """Exact test for sum_i coeff_i zeta_n^{ij}=0."""
    # zeta_n^j has order N=n/gcd(n,j).  Since n is an ell-power, N is also an
    # ell-power.  Reduce coefficients modulo N and test divisibility by Phi_N.
    g = gcd(n, j)
    N = n // g
    if N == 1:
        return sum(coeffs) == 0
    block = N // ell
    reduced = [0] * N
    for i, coeff in enumerate(coeffs):
        reduced[i % N] += coeff
    return all(
        len({reduced[i + q * block] for q in range(ell)}) == 1
        for i in range(block)
    )


def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def k_d_invariant_signed(coeffs, n, d):
    block = n // d
    return all(
        len({coeffs[i + q * block] for q in range(d)}) == 1
        for i in range(block)
    )


def signed_classification_audit(n):
    ell = prime_power_base(n)
    counts = {sigma: 0 for sigma in range(1, n)}
    bad_invariance = {sigma: 0 for sigma in range(1, n)}
    # Stream the full ternary search.  For n=16 this is 3^16 cases, so
    # materializing the candidates would turn a finite audit into a memory
    # stress test.
    for coeffs in itertools.product((-1, 0, 1), repeat=n):
        active = True
        for sigma in range(1, n):
            if active:
                active = moment_zero_prime_power(coeffs, n, ell, sigma)
            if not active:
                break
            d = d_sigma(ell, sigma)
            counts[sigma] += 1
            if not k_d_invariant_signed(coeffs, n, d):
                bad_invariance[sigma] += 1

    sigma_reports = []
    for sigma in range(1, n):
        d = d_sigma(ell, sigma)
        expected = 3 ** (n // d)
        sigma_reports.append({
            "sigma": sigma,
            "d_sigma": d,
            "candidate_count": counts[sigma],
            "expected_count": expected,
            "bad_invariance_count": bad_invariance[sigma],
            "classification_ok": bad_invariance[sigma] == 0 and counts[sigma] == expected,
        })
    return {
        "n": n,
        "ell": ell,
        "sigma_reports": sigma_reports,
        "all_sigma_ok": all(row["classification_ok"] for row in sigma_reports),
    }


def kd_cosets(n, d):
    block = n // d
    return [frozenset(i + q * block for q in range(d)) for i in range(block)]


def anchor_uv(A0, n, d):
    A0 = set(A0)
    u = v = mixed = 0
    for coset in kd_cosets(n, d):
        count = len(A0 & coset)
        if count == len(coset):
            u += 1
        elif count == 0:
            v += 1
        else:
            mixed += 1
    return u, v, mixed


def anchored_formula_count(A0, n, d):
    u, v, _ = anchor_uv(A0, n, d)
    return comb(u + v, u)


def signed_coeffs(A, A0, n):
    coeffs = [0] * n
    for i in A:
        coeffs[i % n] += 1
    for i in A0:
        coeffs[i % n] -= 1
    return coeffs


def charzero_same_prefix(A, A0, n, sigma):
    ell = prime_power_base(n)
    coeffs = signed_coeffs(A, A0, n)
    return all(moment_zero_prime_power(coeffs, n, ell, j) for j in range(1, sigma + 1))


def direct_anchor_formula_audit(n):
    ell = prime_power_base(n)
    reports = []
    all_ok = True
    elems = list(range(n))
    for sigma in range(1, n):
        d = d_sigma(ell, sigma)
        for m in range(n + 1):
            subsets = [frozenset(c) for c in itertools.combinations(elems, m)]
            for A0 in subsets:
                direct = sum(1 for A in subsets if charzero_same_prefix(A, A0, n, sigma))
                formula = anchored_formula_count(A0, n, d)
                if direct != formula:
                    all_ok = False
                    reports.append({
                        "sigma": sigma,
                        "m": m,
                        "anchor": sorted(A0),
                        "direct": direct,
                        "formula": formula,
                    })
                    return {"n": n, "all_ok": False, "failures": reports}
    return {"n": n, "all_ok": all_ok, "failures": reports}


def global_max_formula_audit(n):
    ell = prime_power_base(n)
    elems = list(range(n))
    reports = []
    all_ok = True
    for sigma in range(1, n):
        d = d_sigma(ell, sigma)
        for m in range(n + 1):
            max_by_anchors = 0
            for A0 in itertools.combinations(elems, m):
                max_by_anchors = max(max_by_anchors, anchored_formula_count(A0, n, d))
            predicted = comb((m // d) + ((n - m) // d), m // d)
            ok = max_by_anchors == predicted
            all_ok = all_ok and ok
            reports.append({
                "sigma": sigma,
                "d_sigma": d,
                "m": m,
                "max_by_anchors": max_by_anchors,
                "predicted": predicted,
                "ok": ok,
            })
    return {"n": n, "all_ok": all_ok, "reports": reports}


def generated_anchor_sets(A0, n, d):
    A0 = set(A0)
    full = []
    empty = []
    for coset in kd_cosets(n, d):
        count = len(A0 & coset)
        if count == len(coset):
            full.append(coset)
        elif count == 0:
            empty.append(coset)
    out = []
    for r in range(min(len(full), len(empty)) + 1):
        for removed in itertools.combinations(full, r):
            removed_points = set().union(*removed) if removed else set()
            for added in itertools.combinations(empty, r):
                added_points = set().union(*added) if added else set()
                out.append(frozenset((A0 - removed_points) | added_points))
    return set(out)


def positive_structured_example():
    n = 16
    ell = 2
    sigma = 4
    d = d_sigma(ell, sigma)
    cosets = kd_cosets(n, d)
    A0 = set(cosets[0])
    A = set(cosets[1])
    return {
        "n": n,
        "sigma": sigma,
        "d_sigma": d,
        "A0": sorted(A0),
        "A": sorted(A),
        "exchange_t": len(A0),
        "d_divides_t": len(A0) % d == 0,
        "same_prefix": charzero_same_prefix(A, A0, n, sigma),
        "anchor_formula_count": anchored_formula_count(A0, n, d),
    }


def mixed_anchor_distinction_example():
    n = 16
    sigma = 3
    d = d_sigma(2, sigma)
    cosets = kd_cosets(n, d)
    # One full exchange source coset, one empty target coset, and one mixed
    # common coset.  The exchange core is K_d-structured, but neither full
    # anchored complement is globally K_d-periodic.
    A0 = set(cosets[0]) | {next(iter(cosets[2]))}
    A = set(cosets[1]) | {next(iter(cosets[2]))}
    return {
        "n": n,
        "sigma": sigma,
        "d_sigma": d,
        "A0": sorted(A0),
        "A": sorted(A),
        "same_prefix": charzero_same_prefix(A, A0, n, sigma),
        "A0_global_kd_union": any(
            0 < len(set(A0) & coset) < len(coset) for coset in cosets
        ) is False,
        "A_global_kd_union": any(
            0 < len(set(A) & coset) < len(coset) for coset in cosets
        ) is False,
    }


def finite_newton_equivalence_audit():
    p, n = 17, 16
    H = subgroup(p, n)
    all_ok = True
    checked = 0
    for sigma in range(1, n):
        for m in range(n + 1):
            power_buckets = defaultdict(list)
            coeff_buckets = defaultdict(list)
            for combo in itertools.combinations(H, m):
                A = frozenset(combo)
                power_key = tuple(
                    sum(pow(a, j, p) for a in A) % p
                    for j in range(1, sigma + 1)
                )
                coeff_key = top_sigma_key(poly_from_roots(combo, p), sigma)
                power_buckets[power_key].append(A)
                coeff_buckets[coeff_key].append(A)
            power_partition = sorted(sorted(map(tuple, bucket)) for bucket in power_buckets.values())
            coeff_partition = sorted(sorted(map(tuple, bucket)) for bucket in coeff_buckets.values())
            checked += 1
            if power_partition != coeff_partition:
                all_ok = False
                return {"checked": checked, "all_ok": False, "sigma": sigma, "m": m}
    return {"checked": checked, "all_ok": all_ok}


def n16_sigma4_t6_impossibility():
    p, n, k, sigma = 17, 16, 6, 4
    H = subgroup(p, n)
    m = n - (k + sigma)
    fibers = prefix_fibers(H, m, sigma, p)
    pairs = collision_pairs(fibers)
    d = d_sigma(2, sigma)
    t_values = set()
    for pair in pairs:
        A0, A = set(pair[0]), set(pair[1])
        t_values.add(len(A - A0))
    return {
        "d_sigma": d,
        "t_values": sorted(t_values),
        "all_t_not_divisible_by_d": all(t % d != 0 for t in t_values),
        "collision_pairs": len(pairs),
    }


def reserve_scale_bound_sample(n=1024, C=4):
    log2n = n.bit_length() - 1
    sigma = (C * n + log2n - 1) // log2n
    d = d_sigma(2, sigma)
    exponent = n / d
    return {
        "n": n,
        "C": C,
        "sigma_sample": sigma,
        "d_sigma": d,
        "n_over_d": exponent,
        "polynomial_exponent_bound": 1 / C,
        "n_over_sigma": n / sigma,
        "log2n_over_C": log2n / C,
        "bound_check": exponent <= n / sigma <= log2n / C,
    }


def run():
    class8 = signed_classification_audit(8)
    class16 = signed_classification_audit(16)
    class9 = signed_classification_audit(9)
    anchor8 = direct_anchor_formula_audit(8)
    anchor9 = direct_anchor_formula_audit(9)
    max16 = global_max_formula_audit(16)
    positive = positive_structured_example()
    mixed = mixed_anchor_distinction_example()
    newton = finite_newton_equivalence_audit()
    impossible = n16_sigma4_t6_impossibility()
    reserve = reserve_scale_bound_sample()
    checks = {
        "classification_n8_all_sigma_ok": class8["all_sigma_ok"],
        "classification_n16_all_sigma_ok": class16["all_sigma_ok"],
        "classification_n9_all_sigma_ok": class9["all_sigma_ok"],
        "direct_anchor_formula_n8_ok": anchor8["all_ok"],
        "direct_anchor_formula_n9_ok": anchor9["all_ok"],
        "global_max_formula_n16_ok": max16["all_ok"],
        "positive_structured_example_ok": (
            positive["d_divides_t"]
            and positive["same_prefix"]
            and positive["anchor_formula_count"] == 2
        ),
        "mixed_anchor_not_global_quotient_ok": (
            mixed["same_prefix"]
            and not mixed["A0_global_kd_union"]
            and not mixed["A_global_kd_union"]
        ),
        "finite_newton_equivalence_ok": newton["all_ok"],
        "n16_sigma4_t6_charzero_impossible_ok": (
            impossible["collision_pairs"] == 40
            and impossible["all_t_not_divisible_by_d"]
        ),
        "reserve_scale_bound_sample_ok": reserve["bound_check"],
    }
    return {
        "status": "PROVED_IDENTITIES/EXPERIMENTAL_CHARZERO_FIBER_AUDIT",
        "classification": [class8, class16, class9],
        "direct_anchor": [anchor8, anchor9],
        "global_max_n16": {
            "all_ok": max16["all_ok"],
            "reports_checked": len(max16["reports"]),
            "sample_reports": max16["reports"][:8],
        },
        "positive_structured_example": positive,
        "mixed_anchor_distinction_example": mixed,
        "finite_newton_equivalence": newton,
        "n16_sigma4_t6_impossibility": impossible,
        "reserve_scale_bound_sample": reserve,
        "checks": checks,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)
    result = run()
    ok = all(result["checks"].values())
    if args.format == "json":
        print(json.dumps(result, indent=2))
        return 0 if ok else 1

    print(f"L1 prime-power char-zero fiber verifier ({result['status']})")
    for row in result["classification"]:
        print(
            f"  classification n={row['n']} ell={row['ell']}: "
            f"{'OK' if row['all_sigma_ok'] else 'FAIL'}"
        )
    print(
        "  direct anchor formula n=8/n=9: "
        f"{result['direct_anchor'][0]['all_ok']} / "
        f"{result['direct_anchor'][1]['all_ok']}"
    )
    print(
        "  global max formula n=16 reports: "
        f"{result['global_max_n16']['reports_checked']}"
    )
    print(
        "  positive structured example: "
        f"{result['positive_structured_example']}"
    )
    print(
        "  mixed anchor distinction: "
        f"{result['mixed_anchor_distinction_example']}"
    )
    print(
        "  Newton finite equivalence checked cases: "
        f"{result['finite_newton_equivalence']['checked']}"
    )
    print(
        "  n=16,sigma=4,t=6 impossibility: "
        f"{result['n16_sigma4_t6_impossibility']}"
    )
    for name, passed in result["checks"].items():
        print(f"  [{'OK ' if passed else 'FAIL'}] {name}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
