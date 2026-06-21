#!/usr/bin/env python3
"""Verify dyadic characteristic-zero first-moment rigidity for L1 prefix cores.

AUDIT / EXPERIMENTAL verifier for
`experimental/notes/l1/l1_prefix_dyadic_charzero_rigidity.md`.

The script checks the exact signed first-moment rigidity theorem for dyadic
domains, its prime-power K_l generalization, and the one-coefficient norm-event
certificate on the F_17,n=16,k=6,sigma=4 collision set.

Prime-field prefix/exchange lane only.  This script does not assert the
arbitrary-word robust-shell theorem, RS list-decoding safety, MCA,
line-decoding, or protocol safety.
"""

import argparse
import itertools
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from verify_l1_prefix_divisor_count import subgroup  # noqa: E402
from verify_l1_prefix_low_excess_norm_sieve import (  # noqa: E402
    canonical_pair,
    collision_pair_orbits,
    collision_pairs,
    elem_eval_mod_p,
    elem_exponents,
    element_norm_abs,
    lift_delta_coeffs,
    prefix_fibers,
    set_to_exponents,
)


def signed_coeffs(B, B0, n):
    coeffs = [0] * n
    for i in B:
        coeffs[i % n] += 1
    for i in B0:
        coeffs[i % n] -= 1
    return coeffs


def dyadic_phi_divides(coeffs):
    n = len(coeffs)
    half = n // 2
    return all(coeffs[i] == coeffs[i + half] for i in range(half))


def antipodal_invariant(B, n):
    Bset = {x % n for x in B}
    half = n // 2
    return all((x + half) % n in Bset for x in Bset)


def locator_even_exponents(B, n, norm_cache):
    """B=-B iff prod_{b in B}(X-zeta^b) is a polynomial in X^2."""
    coeffs = [[0] * n]
    coeffs[0][0] = 1
    for b in sorted(B):
        new = [[0] * n for _ in range(len(coeffs) + 1)]
        minus_root = [0] * n
        minus_root[b % n] = -1
        for i, coeff in enumerate(coeffs):
            # Constant term multiplication by -zeta^b.
            shifted = [0] * n
            for j, val in enumerate(coeff):
                if val:
                    shifted[(j + b) % n] -= val
            new[i] = [a + c for a, c in zip(new[i], shifted)]
            new[i + 1] = [a + c for a, c in zip(new[i + 1], coeff)]
        coeffs = new
    return all(
        element_norm_abs(elem, n, norm_cache) == 0
        for degree, elem in enumerate(coeffs)
        if degree % 2 == 1
    )


def enumerate_dyadic_signed_tests(n):
    elems = range(n)
    cases = []
    for mask_pos in range(1 << n):
        pos = {i for i in elems if mask_pos & (1 << i)}
        remaining = [i for i in elems if i not in pos]
        for mask_neg in range(1 << len(remaining)):
            neg = {remaining[j] for j in range(len(remaining)) if mask_neg & (1 << j)}
            coeffs = signed_coeffs(pos, neg, n)
            divides = dyadic_phi_divides(coeffs)
            if divides:
                cases.append((pos, neg))
                if not (antipodal_invariant(pos, n) and antipodal_invariant(neg, n)):
                    return False, cases
    return True, cases


def prime_power_phi_divides(coeffs, ell):
    n = len(coeffs)
    block = n // ell
    return all(
        len({coeffs[i + j * block] for j in range(ell)}) == 1
        for i in range(block)
    )


def kell_invariant(B, n, ell):
    Bset = {x % n for x in B}
    block = n // ell
    return all((x + j * block) % n in Bset for x in Bset for j in range(ell))


def enumerate_prime_power_tests(n, ell):
    elems = range(n)
    cases = []
    for mask_pos in range(1 << n):
        pos = {i for i in elems if mask_pos & (1 << i)}
        remaining = [i for i in elems if i not in pos]
        for mask_neg in range(1 << len(remaining)):
            neg = {remaining[j] for j in range(len(remaining)) if mask_neg & (1 << j)}
            coeffs = signed_coeffs(pos, neg, n)
            divides = prime_power_phi_divides(coeffs, ell)
            if divides:
                cases.append((pos, neg))
                if not (kell_invariant(pos, n, ell) and kell_invariant(neg, n, ell)):
                    return False, cases
    return True, cases


def analyze_f17_collisions():
    p, n, k, sigma = 17, 16, 6, 4
    H = subgroup(p, n)
    m = n - (k + sigma)
    fibers = prefix_fibers(H, m, sigma, p)
    pairs = collision_pairs(fibers)
    orbits = collision_pair_orbits(pairs, H, p)
    exp_of = elem_exponents(H)
    norm_cache = {}
    omega = H[1]
    reports = []
    swapped_by_negation = 0
    misclassified_swapped = 0
    for orbit in orbits:
        pair = orbit[0]
        A0 = frozenset(pair[0])
        A = frozenset(pair[1])
        B = A - A0
        B0 = A0 - A
        t = len(B)
        B_exp = set_to_exponents(B, exp_of)
        B0_exp = set_to_exponents(B0, exp_of)
        delta = lift_delta_coeffs(B_exp, B0_exp, n)
        first_j = t - 1
        first_delta = delta[first_j]
        norm = element_norm_abs(first_delta, n, norm_cache)
        first_reduces_to_zero = elem_eval_mod_p(first_delta, omega, p) == 0
        B_antipodal = antipodal_invariant(B_exp, n)
        B0_antipodal = antipodal_invariant(B0_exp, n)
        neg_pair = canonical_pair(
            tuple(sorted((-x) % p for x in A0)),
            tuple(sorted((-x) % p for x in A)),
        )
        neg_swaps_pair = neg_pair == canonical_pair(tuple(sorted(A)), tuple(sorted(A0)))
        swapped_by_negation += int(neg_swaps_pair)
        misclassified_swapped += int(neg_swaps_pair and B_antipodal and B0_antipodal)
        reports.append({
            "orbit_size": len(orbit),
            "t": t,
            "first_j": first_j,
            "first_delta_norm_abs": norm,
            "p_divides_first_norm": norm != 0 and norm % p == 0,
            "first_delta_reduces_to_zero_mod_p": first_reduces_to_zero,
            "first_delta_algebraically_nonzero": norm != 0,
            "B_antipodal": B_antipodal,
            "B0_antipodal": B0_antipodal,
            "negation_swaps_complements": neg_swaps_pair,
        })
    return {
        "params": {"p": p, "n": n, "k": k, "sigma": sigma, "m": m},
        "collision_pairs": len(pairs),
        "orbit_count": len(orbits),
        "reports": reports,
        "swapped_by_negation_orbits": swapped_by_negation,
        "misclassified_swapped_orbits": misclassified_swapped,
        "checks": {
            "forty_collisions_ok": len(pairs) == 40,
            "three_orbits_ok": len(orbits) == 3,
            "first_delta_nonzero_all_orbits_ok": all(
                r["first_delta_algebraically_nonzero"] for r in reports
            ),
            "first_norm_divisible_by_17_ok": all(
                r["p_divides_first_norm"] for r in reports
            ),
            "first_delta_reduces_mod_17_ok": all(
                r["first_delta_reduces_to_zero_mod_p"] for r in reports
            ),
            "no_exchange_core_antipodal_orbits_ok": all(
                not (r["B_antipodal"] and r["B0_antipodal"]) for r in reports
            ),
            "negation_swap_not_misclassified_ok": misclassified_swapped == 0,
        },
    }


def run():
    dyadic8_ok, dyadic8_cases = enumerate_dyadic_signed_tests(8)
    dyadic16_ok, dyadic16_cases = enumerate_dyadic_signed_tests(16)
    prime9_ok, prime9_cases = enumerate_prime_power_tests(9, 3)
    f17 = analyze_f17_collisions()
    locator_norm_cache = {}
    checks = {
        "dyadic_n8_signed_antipodal_classification_ok": dyadic8_ok,
        "dyadic_n16_signed_antipodal_classification_ok": dyadic16_ok,
        "dyadic_locator_even_equivalence_sample_ok": all(
            locator_even_exponents(B, 16, locator_norm_cache)
            == antipodal_invariant(B, 16)
            for B, _ in dyadic16_cases[:128]
        ),
        "prime_power_n9_K3_classification_ok": prime9_ok,
    }
    for name, ok in f17["checks"].items():
        checks[f"f17_{name}"] = ok
    return {
        "status": "PROVED_IDENTITIES/EXPERIMENTAL_FIRST_MOMENT_AUDIT",
        "dyadic": {
            "n8_cases": len(dyadic8_cases),
            "n16_cases": len(dyadic16_cases),
            "n8_ok": dyadic8_ok,
            "n16_ok": dyadic16_ok,
        },
        "prime_power": {
            "n9_ell3_cases": len(prime9_cases),
            "n9_ell3_ok": prime9_ok,
        },
        "f17": f17,
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

    print(f"L1 prefix dyadic char-zero verifier ({result['status']})")
    print(
        f"  dyadic signed cases n=8/n=16 : "
        f"{result['dyadic']['n8_cases']} / {result['dyadic']['n16_cases']}"
    )
    print(
        f"  prime-power n=9, ell=3 cases : "
        f"{result['prime_power']['n9_ell3_cases']}"
    )
    f17 = result["f17"]
    print(
        f"  F_17 collisions/orbits        : "
        f"{f17['collision_pairs']} / {f17['orbit_count']}"
    )
    print(
        f"  negation-swap orbits          : "
        f"{f17['swapped_by_negation_orbits']}"
    )
    for idx, report in enumerate(f17["reports"], start=1):
        print(
            f"    orbit {idx}: size={report['orbit_size']} "
            f"j={report['first_j']} norm={report['first_delta_norm_abs']} "
            f"div17={report['p_divides_first_norm']} "
            f"B=-B? {report['B_antipodal']} "
            f"B0=-B0? {report['B0_antipodal']} "
            f"neg-swaps={report['negation_swaps_complements']}"
        )
    for name, passed in result["checks"].items():
        print(f"  [{'OK ' if passed else 'FAIL'}] {name}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
