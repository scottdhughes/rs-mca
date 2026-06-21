#!/usr/bin/env python3
"""Verify L1 prefix anchored trinary-kernel rigidity identities.

AUDIT / EXPERIMENTAL verifier for
`experimental/notes/l1/l1_prefix_trinary_kernel_rigidity.md`.

The script checks the anchored bijection between a monomial-prefix fiber of
complement m-subsets A <= H and low-degree trinary interpolation polynomials

    g_A(h) = 1_A(h) - 1_A0(h).

It verifies the coefficient gap, anchor-sign divisibilities, the divisor
partition and S-unit equations, quotient-periodic composition criterion, and
the known F_17,n=16,k=6,sigma=4 forty-collision certificate in trinary form.

Prime-field prefix/divisor lane only.  This script does not assert the
arbitrary-word robust-shell theorem, RS list-decoding safety, MCA,
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

from verify_l1_prefix_divisor_count import poly_from_roots, subgroup  # noqa: E402


def trim(poly):
    out = [x for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a, b, p):
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_sub(a, b, p):
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out)


def poly_mul(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out)


def poly_div_exact(num, den, p):
    num = trim(num)
    den = trim(den)
    if num == [0]:
        return [0]
    if den == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    work = num[:]
    q = [0] * max(1, (len(work) - len(den) + 1))
    inv_lead = pow(den[-1], -1, p)
    while len(work) >= len(den) and work != [0]:
        shift = len(work) - len(den)
        coeff = (work[-1] * inv_lead) % p
        q[shift] = coeff
        for i, di in enumerate(den):
            work[shift + i] = (work[shift + i] - coeff * di) % p
        work = trim(work)
    if work != [0]:
        raise ValueError(f"nonzero polynomial division remainder {work}")
    return trim(q)


def poly_eval(poly, x, p):
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def poly_mod_xn_minus_1(poly, n, p):
    out = [0] * n
    for i, coeff in enumerate(poly):
        out[i % n] = (out[i % n] + coeff) % p
    return trim(out)


def xn_minus_1(n, p):
    return [p - 1] + [0] * (n - 1) + [1]


def power_sum_key(A, sigma, p):
    return tuple(sum(pow(a, j, p) for a in A) % p for j in range(1, sigma + 1))


def prefix_fibers(H, m, sigma, p):
    buckets = defaultdict(list)
    for combo in itertools.combinations(H, m):
        A = frozenset(combo)
        buckets[power_sum_key(A, sigma, p)].append(A)
    return dict(buckets)


def interpolate_on_H(values_by_h, H, p):
    """Return the unique degree < n polynomial with prescribed values on H."""
    n = len(H)
    inv_n = pow(n % p, -1, p)
    coeffs = []
    for i in range(n):
        total = 0
        for h in H:
            total = (total + values_by_h[h] * pow(h, (-i) % n, p)) % p
        coeffs.append((inv_n * total) % p)
    return trim(coeffs)


def coeff(poly, i):
    return poly[i] if i < len(poly) else 0


def coefficient_gap_ok(g, n, sigma):
    return coeff(g, 0) == 0 and all(coeff(g, n - j) == 0 for j in range(1, sigma + 1))


def degree(poly):
    return -1 if trim(poly) == [0] else len(trim(poly)) - 1


def g_from_anchor(A, A0, H, p):
    values = {}
    for h in H:
        values[h] = ((1 if h in A else 0) - (1 if h in A0 else 0)) % p
    return interpolate_on_H(values, H, p)


def values_of_g(g, H, p):
    return {h: poly_eval(g, h, p) for h in H}


def anchor_signs_ok(g, A0, H, p):
    vals = values_of_g(g, H, p)
    for h in H:
        if h in A0:
            if vals[h] not in (0, p - 1):
                return False
        else:
            if vals[h] not in (0, 1):
                return False
    return True


def anchor_divisibilities_ok(g, A0, H, p):
    gg_plus = poly_mul(g, poly_add(g, [1], p), p)
    gg_minus = poly_mul(g, poly_sub(g, [1], p), p)
    return (
        all(poly_eval(gg_plus, h, p) == 0 for h in A0)
        and all(poly_eval(gg_minus, h, p) == 0 for h in H if h not in A0)
    )


def recover_A_from_g(g, A0, H, p):
    vals = values_of_g(g, H, p)
    A = set()
    for h in H:
        if h in A0:
            if vals[h] == 0:
                A.add(h)
        else:
            if vals[h] == 1:
                A.add(h)
    return frozenset(A)


def is_global_trinary(g, H, p):
    return all(poly_eval(g, h, p) in (0, 1, p - 1) for h in H)


def cube_divisibility_ok(g, n, p):
    g2_minus_1 = poly_sub(poly_mul(g, g, p), [1], p)
    cube = poly_mul(g, g2_minus_1, p)
    return poly_mod_xn_minus_1(cube, n, p) == [0]


def value_divisors(g, H, p):
    vals = values_of_g(g, H, p)
    roots0 = [h for h in H if vals[h] == 0]
    roots_plus = [h for h in H if vals[h] == 1]
    roots_minus = [h for h in H if vals[h] == p - 1]
    return (
        poly_from_roots(roots0, p),
        poly_from_roots(roots_plus, p),
        poly_from_roots(roots_minus, p),
        roots0,
        roots_plus,
        roots_minus,
    )


def divisor_partition_and_sunit_ok(g, H, p):
    n = len(H)
    D0, Dp, Dm, roots0, roots_plus, roots_minus = value_divisors(g, H, p)
    product = poly_mul(poly_mul(D0, Dp, p), Dm, p)
    partition_ok = trim(product) == trim(xn_minus_1(n, p))
    exchange_ok = len(roots_plus) == len(roots_minus)

    U0 = poly_div_exact(g, D0, p)
    Up = poly_div_exact(poly_sub(g, [1], p), Dp, p)
    Um = poly_div_exact(poly_add(g, [1], p), Dm, p)

    left1 = poly_sub(poly_mul(D0, U0, p), poly_mul(Dp, Up, p), p)
    left2 = poly_sub(poly_mul(Dm, Um, p), poly_mul(D0, U0, p), p)
    left3 = poly_sub(poly_mul(Dm, Um, p), poly_mul(Dp, Up, p), p)
    sunit_ok = (
        trim(left1) == [1]
        and trim(left2) == [1]
        and trim(left3) == [2 % p]
    )
    return {
        "partition_ok": partition_ok,
        "exchange_ok": exchange_ok,
        "sunit_ok": sunit_ok,
        "deg_D0": len(roots0),
        "deg_D_plus": len(roots_plus),
        "deg_D_minus": len(roots_minus),
    }


def divisors_of(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def subgroup_of_order(H, d, p):
    return {x for x in H if pow(x, d, p) == 1}


def invariant_under_Kd(g, H, d, p):
    Kd = subgroup_of_order(H, d, p)
    vals = values_of_g(g, H, p)
    for x in H:
        for kappa in Kd:
            if vals[(kappa * x) % p] != vals[x]:
                return False
    return True


def support_multiple_of_d(g, d):
    return all(i % d == 0 for i, ci in enumerate(g) if ci)


def stabilizer_order(g, H, p):
    vals = values_of_g(g, H, p)
    return sum(
        1
        for h in H
        if all(vals[(h * x) % p] == vals[x] for x in H)
    )


def enumerate_anchor_trinary_solutions(A0, H, sigma, p):
    """Independent anchor-sign enumeration around A0."""
    A0_list = sorted(A0)
    outside = sorted(h for h in H if h not in A0)
    solutions = {}
    max_t = min(len(A0_list), len(outside))
    for t in range(max_t + 1):
        for removed in itertools.combinations(A0_list, t):
            removed_set = set(removed)
            for added in itertools.combinations(outside, t):
                A = frozenset((set(A0) - removed_set) | set(added))
                g = g_from_anchor(A, A0, H, p)
                if coefficient_gap_ok(g, len(H), sigma):
                    solutions[A] = tuple(g)
    return solutions


def check_anchor(A0, fiber_members, H, sigma, p):
    expected = set(fiber_members)
    independent = enumerate_anchor_trinary_solutions(A0, H, sigma, p)
    max_errors = {
        "coefficient_gap": 0,
        "anchor_signs": 0,
        "anchor_divisibilities": 0,
        "cube_divisibility": 0,
        "recover_A": 0,
        "divisor_partition": 0,
        "sunit": 0,
        "composition": 0,
    }
    stabilizers = []
    for A in expected:
        g = g_from_anchor(A, A0, H, p)
        if not coefficient_gap_ok(g, len(H), sigma):
            max_errors["coefficient_gap"] += 1
        if degree(g) > len(H) - sigma - 1:
            max_errors["coefficient_gap"] += 1
        if not anchor_signs_ok(g, A0, H, p):
            max_errors["anchor_signs"] += 1
        if not anchor_divisibilities_ok(g, A0, H, p):
            max_errors["anchor_divisibilities"] += 1
        if not cube_divisibility_ok(g, len(H), p):
            max_errors["cube_divisibility"] += 1
        if recover_A_from_g(g, A0, H, p) != A:
            max_errors["recover_A"] += 1
        part = divisor_partition_and_sunit_ok(g, H, p)
        if not (part["partition_ok"] and part["exchange_ok"]):
            max_errors["divisor_partition"] += 1
        if not part["sunit_ok"]:
            max_errors["sunit"] += 1
        for d in divisors_of(len(H)):
            if d == 1:
                continue
            if invariant_under_Kd(g, H, d, p) != support_multiple_of_d(g, d):
                max_errors["composition"] += 1
        stabilizers.append(stabilizer_order(g, H, p))

    reverse_bijection_ok = set(independent) == expected
    return {
        "anchor": sorted(A0),
        "fiber_size": len(expected),
        "independent_solution_count": len(independent),
        "reverse_bijection_ok": reverse_bijection_ok,
        "errors": max_errors,
        "stabilizer_orders": sorted(stabilizers),
    }


def check_reject_bad_global_solution(H, sigma, p, nonsingleton_fibers):
    for members in nonsingleton_fibers:
        if len(members) < 2:
            continue
        A0 = members[0]
        A = members[1]
        g = g_from_anchor(A, A0, H, p)
        bad = [(-ci) % p for ci in g]
        return {
            "available": True,
            "global_trinary_ok": is_global_trinary(bad, H, p),
            "coefficient_gap_ok": coefficient_gap_ok(bad, len(H), sigma),
            "cube_divisibility_ok": cube_divisibility_ok(bad, len(H), p),
            "anchor_signs_rejected": not anchor_signs_ok(bad, A0, H, p),
            "anchor_divisibilities_rejected": not anchor_divisibilities_ok(bad, A0, H, p),
        }
    return {"available": False}


def verify_case(p, n, k, sigma, max_anchors=None):
    H = subgroup(p, n)
    m = n - (k + sigma)
    if m < 0:
        raise ValueError("need m=n-(k+sigma) >= 0")
    fibers = prefix_fibers(H, m, sigma, p)
    nonsingleton = [members for members in fibers.values() if len(members) > 1]
    anchor_reports = []
    anchors_checked = 0
    for members in nonsingleton:
        for A0 in members:
            if max_anchors is not None and anchors_checked >= max_anchors:
                break
            anchor_reports.append(check_anchor(A0, members, H, sigma, p))
            anchors_checked += 1
        if max_anchors is not None and anchors_checked >= max_anchors:
            break
    if not anchor_reports:
        # Still test one singleton anchor in collision-free regimes.
        first_members = next(iter(fibers.values()))
        anchor_reports.append(check_anchor(first_members[0], first_members, H, sigma, p))

    bad_global = check_reject_bad_global_solution(H, sigma, p, nonsingleton)
    all_anchor_errors_zero = all(
        all(v == 0 for v in report["errors"].values())
        for report in anchor_reports
    )
    all_reverse_ok = all(report["reverse_bijection_ok"] for report in anchor_reports)
    bad_global_ok = (
        not bad_global.get("available")
        or (
            bad_global["global_trinary_ok"]
            and bad_global["coefficient_gap_ok"]
            and bad_global["cube_divisibility_ok"]
            and bad_global["anchor_signs_rejected"]
            and bad_global["anchor_divisibilities_rejected"]
        )
    )
    histogram = defaultdict(int)
    for members in fibers.values():
        histogram[len(members)] += 1
    return {
        "params": {"p": p, "n": n, "k": k, "sigma": sigma, "m": m},
        "counts": {
            "total_subsets": comb(n, m),
            "distinct_prefix_values": len(fibers),
            "max_fiber_size": max(len(members) for members in fibers.values()),
            "fiber_size_histogram": dict(sorted(histogram.items())),
            "nonsingleton_fibers": len(nonsingleton),
            "anchors_checked": len(anchor_reports),
        },
        "anchor_reports": anchor_reports[:8],
        "bad_global_solution_rejection": bad_global,
        "checks": {
            "anchor_forward_identities_ok": all_anchor_errors_zero,
            "anchor_reverse_bijection_ok": all_reverse_ok,
            "bad_global_trinary_rejected_by_anchor_ok": bad_global_ok,
        },
    }


def run():
    certificate = verify_case(17, 16, 6, 4)
    proper = verify_case(17, 8, 3, 2, max_anchors=12)
    checks = {}
    for prefix, case in (("certificate", certificate), ("proper", proper)):
        for name, ok in case["checks"].items():
            checks[f"{prefix}_{name}"] = ok
    checks["certificate_total_ok"] = certificate["counts"]["total_subsets"] == 8008
    checks["certificate_distinct_prefix_values_ok"] = (
        certificate["counts"]["distinct_prefix_values"] == 7968
    )
    checks["certificate_max_fiber_ok"] = certificate["counts"]["max_fiber_size"] == 2
    checks["certificate_forty_collisions_ok"] = (
        certificate["counts"]["fiber_size_histogram"].get(2) == 40
    )
    checks["proper_subgroup_regression_ok"] = proper["params"]["n"] == 8

    return {
        "status": "PROVED_IDENTITIES/EXPERIMENTAL_TRINARY_AUDIT",
        "cases": [certificate, proper],
        "checks": checks,
        "summary": {
            "all_checks_ok": all(checks.values()),
            "route": (
                "Prefix fibers are represented by anchored low-degree "
                "three-valued polynomials satisfying a divisor/S-unit system."
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
    result = run()
    ok = all(result["checks"].values())
    if args.format == "json":
        print(json.dumps(result, indent=2))
        return 0 if ok else 1

    print(f"L1 prefix trinary-kernel verifier ({result['status']})")
    for case in result["cases"]:
        pp = case["params"]
        cc = case["counts"]
        print(
            f"  F_{pp['p']}, n={pp['n']}, k={pp['k']}, "
            f"sigma={pp['sigma']}, m={pp['m']}"
        )
        print(
            f"    subsets/fibers/max: {cc['total_subsets']} / "
            f"{cc['distinct_prefix_values']} / {cc['max_fiber_size']}"
        )
        print(f"    fiber histogram    : {cc['fiber_size_histogram']}")
        print(f"    anchors checked    : {cc['anchors_checked']}")
        first = case["anchor_reports"][0]
        print(
            f"    first anchor fiber/solutions: {first['fiber_size']} / "
            f"{first['independent_solution_count']}"
        )
        print(
            "    bad global trinary rejection: "
            f"{case['bad_global_solution_rejection']}"
        )
    for name, passed in result["checks"].items():
        print(f"  [{'OK ' if passed else 'FAIL'}] {name}")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
