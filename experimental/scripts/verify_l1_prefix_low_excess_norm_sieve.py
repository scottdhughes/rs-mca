#!/usr/bin/env python3
"""Verify L1 prefix low-excess cyclotomic norm-sieve identities.

AUDIT / EXPERIMENTAL verifier for
`experimental/notes/l1/l1_prefix_low_excess_norm_sieve.md`.

The script recovers prefix-fiber collisions of complement subsets A,A0 <= H,
computes their exchange locators

    P=L_{A\\A0},        Q=L_{A0\\A},

checks the finite-field low-gap condition deg(P-Q) <= e=t-sigma-1, lifts P,Q to
Z[zeta_n][X], and verifies that every nonzero high-gap coefficient norm is
divisible by p.

The norm computation uses exact resultants via sympy.  Prime-field prefix lane
only; this script does not assert the arbitrary-word robust-shell theorem, RS
list-decoding safety, MCA, line-decoding, or protocol safety.
"""

import argparse
import itertools
import json
import sys
from collections import defaultdict
from math import comb
from pathlib import Path

from sympy import Poly, cyclotomic_poly, resultant, symbols

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from verify_l1_prefix_divisor_count import poly_from_roots, subgroup  # noqa: E402
from verify_l1_prefix_trinary_kernel_rigidity import (  # noqa: E402
    g_from_anchor,
    support_multiple_of_d,
)


def trim(poly):
    out = [x for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_sub(a, b, p):
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out)


def degree(poly):
    poly = trim(poly)
    return -1 if poly == [0] else len(poly) - 1


def divisors_of(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def power_sum_key(A, sigma, p):
    return tuple(sum(pow(a, j, p) for a in A) % p for j in range(1, sigma + 1))


def prefix_fibers(H, m, sigma, p):
    buckets = defaultdict(list)
    for combo in itertools.combinations(H, m):
        A = frozenset(combo)
        buckets[power_sum_key(A, sigma, p)].append(A)
    return dict(buckets)


def canonical_pair(A, B):
    left = tuple(sorted(A))
    right = tuple(sorted(B))
    return (left, right) if left <= right else (right, left)


def collision_pairs(fibers):
    pairs = []
    for members in fibers.values():
        if len(members) <= 1:
            continue
        for A0, A in itertools.combinations(members, 2):
            pairs.append(canonical_pair(A0, A))
    return sorted(set(pairs))


def dilate_set_tuple(A_tuple, h, p):
    return tuple(sorted((h * a) % p for a in A_tuple))


def collision_pair_orbits(pairs, H, p):
    pair_set = set(pairs)
    seen = set()
    orbits = []
    for pair in pairs:
        if pair in seen:
            continue
        orbit = set()
        for h in H:
            image = canonical_pair(
                dilate_set_tuple(pair[0], h, p),
                dilate_set_tuple(pair[1], h, p),
            )
            if image in pair_set:
                orbit.add(image)
        seen.update(orbit)
        orbits.append(sorted(orbit))
    return orbits


def elem_exponents(H):
    return {h: i for i, h in enumerate(H)}


def set_to_exponents(A, exp_of):
    return sorted(exp_of[a] for a in A)


def elem_zero(n):
    return [0] * n


def elem_one(n):
    out = [0] * n
    out[0] = 1
    return out


def elem_add(a, b):
    return [x + y for x, y in zip(a, b)]


def elem_sub(a, b):
    return [x - y for x, y in zip(a, b)]


def elem_shift(a, shift):
    n = len(a)
    out = [0] * n
    for i, coeff in enumerate(a):
        out[(i + shift) % n] += coeff
    return out


def elem_neg(a):
    return [-x for x in a]


def elem_is_zero(a):
    return all(x == 0 for x in a)


def lift_locator_coeffs(exponents, n):
    """Return coeffs of prod_{a in exponents}(X-zeta^a), low degree first."""
    coeffs = [elem_one(n)]
    for a in exponents:
        new = [elem_zero(n) for _ in range(len(coeffs) + 1)]
        minus_root = elem_neg(elem_shift(elem_one(n), a))
        for i, coeff in enumerate(coeffs):
            new[i] = elem_add(new[i], elem_mul_by_element(coeff, minus_root))
            new[i + 1] = elem_add(new[i + 1], coeff)
        coeffs = new
    return coeffs


def elem_mul_by_element(a, b):
    n = len(a)
    out = [0] * n
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj:
                out[(i + j) % n] += ai * bj
    return out


def elem_eval_mod_p(a, omega, p):
    return sum(coeff * pow(omega, i, p) for i, coeff in enumerate(a)) % p


def element_norm_abs(a, n, cache):
    key = tuple(a)
    if key in cache:
        return cache[key]
    if elem_is_zero(a):
        cache[key] = 0
        return 0
    x = symbols("x")
    phi = Poly(cyclotomic_poly(n, x), x, domain="ZZ")
    expr = sum(coeff * x**i for i, coeff in enumerate(a) if coeff)
    poly = Poly(expr, x, domain="ZZ")
    norm = abs(int(resultant(phi, poly, x)))
    cache[key] = norm
    return norm


def lift_delta_coeffs(B_exp, B0_exp, n):
    P = lift_locator_coeffs(B_exp, n)
    Q = lift_locator_coeffs(B0_exp, n)
    width = max(len(P), len(Q))
    delta = []
    for i in range(width):
        left = P[i] if i < len(P) else elem_zero(n)
        right = Q[i] if i < len(Q) else elem_zero(n)
        delta.append(elem_sub(left, right))
    return delta


def quotient_composition_orders(A0, A, H, p):
    n = len(H)
    g = g_from_anchor(frozenset(A), frozenset(A0), H, p)
    return [d for d in divisors_of(n) if d > 1 and support_multiple_of_d(g, d)]


def analyze_pair(pair, H, p, sigma, norm_cache):
    A0 = frozenset(pair[0])
    A = frozenset(pair[1])
    C = A & A0
    B = A - A0
    B0 = A0 - A
    t = len(B)
    e = t - sigma - 1
    P = poly_from_roots(sorted(B), p)
    Q = poly_from_roots(sorted(B0), p)
    R = poly_sub(P, Q, p)
    finite_gap_ok = degree(R) <= e

    exp_of = elem_exponents(H)
    B_exp = set_to_exponents(B, exp_of)
    B0_exp = set_to_exponents(B0, exp_of)
    delta = lift_delta_coeffs(B_exp, B0_exp, len(H))
    omega = H[1] if len(H) > 1 else 1
    reduction_ok = True
    norm_rows = []
    high_nonzero_count = 0
    high_norm_divisible_count = 0
    for j, elem in enumerate(delta):
        finite_coeff = R[j] if j < len(R) else 0
        if elem_eval_mod_p(elem, omega, p) != finite_coeff % p:
            reduction_ok = False
        if j <= e:
            continue
        if elem_is_zero(elem):
            norm_rows.append({
                "j": j,
                "zero": True,
                "algebraic_zero": True,
                "norm_abs": 0,
                "p_divides": True,
            })
            continue
        norm = element_norm_abs(elem, len(H), norm_cache)
        if norm == 0:
            norm_rows.append({
                "j": j,
                "zero": False,
                "algebraic_zero": True,
                "norm_abs": 0,
                "p_divides": True,
            })
            continue
        high_nonzero_count += 1
        divides = norm % p == 0
        high_norm_divisible_count += int(divides)
        norm_rows.append({
            "j": j,
            "zero": False,
            "algebraic_zero": False,
            "norm_abs": norm,
            "p_divides": divides,
        })

    exact_char_zero_low_gap = high_nonzero_count == 0
    return {
        "A0": sorted(A0),
        "A": sorted(A),
        "C_size": len(C),
        "t": t,
        "e": e,
        "finite_R": R,
        "finite_R_degree": degree(R),
        "finite_gap_ok": finite_gap_ok,
        "lift_reduction_ok": reduction_ok,
        "exact_char_zero_low_gap": exact_char_zero_low_gap,
        "high_nonzero_coefficients": high_nonzero_count,
        "high_norm_divisible_count": high_norm_divisible_count,
        "all_high_norms_divisible_by_p": high_nonzero_count == high_norm_divisible_count,
        "norm_rows": norm_rows,
        "composition_orders": quotient_composition_orders(A0, A, H, p),
    }


def verify_case(p=17, n=16, k=6, sigma=4):
    H = subgroup(p, n)
    m = n - (k + sigma)
    fibers = prefix_fibers(H, m, sigma, p)
    pairs = collision_pairs(fibers)
    orbits = collision_pair_orbits(pairs, H, p)
    norm_cache = {}
    pair_reports = [analyze_pair(pair, H, p, sigma, norm_cache) for pair in pairs]
    orbit_reps = [orbit[0] for orbit in orbits]
    orbit_reports = [analyze_pair(pair, H, p, sigma, norm_cache) for pair in orbit_reps]

    e_distribution = defaultdict(int)
    t_distribution = defaultdict(int)
    finite_gap_ok = True
    reduction_ok = True
    norm_divisibility_ok = True
    exact_char_zero_count = 0
    compositional_count = 0
    for report in pair_reports:
        e_distribution[report["e"]] += 1
        t_distribution[report["t"]] += 1
        finite_gap_ok = finite_gap_ok and report["finite_gap_ok"]
        reduction_ok = reduction_ok and report["lift_reduction_ok"]
        norm_divisibility_ok = (
            norm_divisibility_ok and report["all_high_norms_divisible_by_p"]
        )
        exact_char_zero_count += int(report["exact_char_zero_low_gap"])
        compositional_count += int(bool(report["composition_orders"]))

    orbit_sizes = sorted(len(orbit) for orbit in orbits)
    return {
        "status": "PROVED_IDENTITIES/EXPERIMENTAL_NORM_SIEVE_AUDIT",
        "params": {"p": p, "n": n, "k": k, "sigma": sigma, "m": m},
        "counts": {
            "total_subsets": comb(n, m),
            "distinct_prefix_values": len(fibers),
            "collision_pairs": len(pairs),
            "collision_pair_orbits": len(orbits),
            "orbit_sizes": orbit_sizes,
            "t_distribution": dict(sorted(t_distribution.items())),
            "e_distribution": dict(sorted(e_distribution.items())),
            "exact_char_zero_low_gap_pairs": exact_char_zero_count,
            "compositional_pairs": compositional_count,
            "norm_cache_entries": len(norm_cache),
        },
        "orbit_representatives": orbit_reports,
        "checks": {
            "certificate_collision_count_ok": len(pairs) == 40,
            "three_dilation_orbits_ok": len(orbits) == 3,
            "all_collisions_e1_ok": dict(e_distribution) == {1: 40},
            "all_collisions_t6_ok": dict(t_distribution) == {6: 40},
            "finite_low_gap_ok": finite_gap_ok,
            "lift_reduction_ok": reduction_ok,
            "norm_divisibility_ok": norm_divisibility_ok,
            "nontrivial_norm_event_seen_ok": any(
                report["high_nonzero_coefficients"] > 0 for report in pair_reports
            ),
        },
    }


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--format", choices=["human", "json"], default="human")
    args = ap.parse_args(argv)
    result = verify_case()
    ok = all(result["checks"].values())
    if args.format == "json":
        print(json.dumps(result, indent=2))
        return 0 if ok else 1

    pp = result["params"]
    cc = result["counts"]
    print(f"L1 prefix low-excess norm-sieve verifier ({result['status']})")
    print(
        f"  F_{pp['p']}, n={pp['n']}, k={pp['k']}, "
        f"sigma={pp['sigma']}, m={pp['m']}"
    )
    print(
        f"  subsets/fibers/collisions: {cc['total_subsets']} / "
        f"{cc['distinct_prefix_values']} / {cc['collision_pairs']}"
    )
    print(
        f"  collision orbits          : {cc['collision_pair_orbits']} "
        f"with sizes {cc['orbit_sizes']}"
    )
    print(f"  t distribution            : {cc['t_distribution']}")
    print(f"  e distribution            : {cc['e_distribution']}")
    print(
        f"  exact char-zero low gaps  : "
        f"{cc['exact_char_zero_low_gap_pairs']}"
    )
    print(f"  compositional pairs       : {cc['compositional_pairs']}")
    for idx, report in enumerate(result["orbit_representatives"], start=1):
        norms = [
            (row["j"], row["norm_abs"], row["p_divides"])
            for row in report["norm_rows"]
            if not row["zero"]
        ]
        print(
            f"  orbit rep {idx}: t={report['t']} e={report['e']} "
            f"degR={report['finite_R_degree']} "
            f"high-nonzero={report['high_nonzero_coefficients']} "
            f"composition={report['composition_orders']}"
        )
        print(f"    nonzero high norms       : {norms}")
    for name, passed in result["checks"].items():
        print(f"  [{'OK ' if passed else 'FAIL'}] {name}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
