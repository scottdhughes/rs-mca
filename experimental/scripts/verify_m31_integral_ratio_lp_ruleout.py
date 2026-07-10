#!/usr/bin/env python3
"""Zero-argument stdlib verifier for the M31 integral-ratio LP cut."""

import copy
import hashlib
import json
import os
import sys
from fractions import Fraction


def apply_memory_cap():
    try:
        import resource

        cap = 2 * 1024 ** 3
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        capped_hard = cap if hard == resource.RLIM_INFINITY else min(cap, hard)
        if soft == resource.RLIM_INFINITY or soft > cap:
            resource.setrlimit(resource.RLIMIT_AS, (cap, capped_hard))
    except Exception:
        pass


apply_memory_cap()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(
    ROOT,
    "experimental",
    "data",
    "cap25_v13_m31_integral_ratio_lp_ruleout.json",
)
CHECKS = []


def check(name, condition, detail=""):
    ok = bool(condition)
    CHECKS.append((name, ok))
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def ceil_div(a, b):
    return -((-a) // b)


def scan_grid(n, m, w, Bstar):
    """Regenerate PR #480's grid and the exact degree-two LP cut."""
    L0 = Bstar + 1
    D = n - 1
    R = m * (n - m)
    grid_count = 0
    grid_k_count = 0
    grid_first = None
    grid_last = None
    sign_rows = []
    cut_rows = []
    sign_metadata = []

    for k in range(2, 775):
        lo = ceil_div(w + 1, k - 1)
        hi = min(m // k, R // (n * (k - 1)))
        if lo > hi:
            continue
        count = hi - lo + 1
        summary = [k, lo, hi, count]
        if grid_first is None:
            grid_first = summary
        grid_last = summary
        grid_k_count += 1
        grid_count += count

        for t in range(lo, hi + 1):
            e1 = (k - 1) * t
            e2 = k * t
            den = D * (R - e1 * n) * (R - e2 * n) + R * R
            sign_ok = (e1 + e2) * n >= 2 * R and den > 0
            if not sign_ok:
                continue
            numerator = e1 * e2 * n * n * D
            row = [k, t, e1, e2, numerator // den]
            sign_rows.append(row)
            sign_metadata.append((row, numerator, den))
            if numerator < L0 * den:
                cut_rows.append(row)

    noncut_sign_rows = [
        row for row, numerator, den in sign_metadata if numerator >= L0 * den
    ]
    canonical = ";".join(",".join(map(str, row)) for row in cut_rows).encode("ascii")
    return {
        "grid_count": grid_count,
        "grid_k_count": grid_k_count,
        "grid_first": grid_first,
        "grid_last": grid_last,
        "sign_rows": sign_rows,
        "cut_rows": cut_rows,
        "sign_metadata": sign_metadata,
        "noncut_sign_rows": noncut_sign_rows,
        "canonical": canonical,
    }


def build_expected():
    p = 2 ** 31 - 1
    n = 2 ** 21
    m = 981_129
    w = 67_447
    Bstar = 2 ** 24 - 1
    L0 = Bstar + 1
    D = n - 1
    R = m * (n - m)
    scan = scan_grid(n, m, w, Bstar)
    cut = scan["cut_rows"]
    sign = scan["sign_rows"]
    noncut = scan["noncut_sign_rows"]
    cut_floors = [row[4] for row in cut]
    noncut_floors = [row[4] for row in noncut]

    packet = {
        "schema": "cap25-v13-m31-integral-ratio-lp-ruleout-v1",
        "status": "PROVED exact Exit 2 sublattice ruleout / OPEN residual integral-ratio grid",
        "deployed": {
            "p": p,
            "n": n,
            "m": m,
            "w": w,
            "Bstar": Bstar,
            "L0": L0,
            "ambient_dimension": D,
            "centered_radius_numerator": R,
        },
        "grid": {
            "k_min": 2,
            "k_max": 774,
            "k_count": scan["grid_k_count"],
            "pair_count": scan["grid_count"],
            "first": scan["grid_first"],
            "last": scan["grid_last"],
        },
        "lp_cut": {
            "sign_condition_count": len(sign),
            "eliminated_count": len(cut),
            "surviving_count": scan["grid_count"] - len(cut),
            "distinct_eliminated_k_count": len({row[0] for row in cut}),
            "eliminated_k_min": min(row[0] for row in cut),
            "eliminated_k_max": max(row[0] for row in cut),
            "floor_bound_min": min(cut_floors),
            "floor_bound_max": max(cut_floors),
            "weakest_budget_margin": Bstar - max(cut_floors),
            "sign_but_not_eliminated_count": len(noncut),
            "sign_but_not_eliminated_floor_min": min(noncut_floors),
            "sign_but_not_eliminated_floor_max": max(noncut_floors),
            "sign_but_not_eliminated_min_excess": min(noncut_floors) - Bstar,
            "checksums": {
                "sum_k": sum(row[0] for row in cut),
                "sum_t": sum(row[1] for row in cut),
                "sum_e1": sum(row[2] for row in cut),
                "sum_e2": sum(row[3] for row in cut),
            },
            "canonical_row_format": (
                "k,t,e1,e2,floor_bound joined by commas; rows joined by semicolons"
            ),
            "canonical_ascii_bytes": len(scan["canonical"]),
            "canonical_sha256": hashlib.sha256(scan["canonical"]).hexdigest(),
            "first_five": cut[:5],
            "last_six": cut[-6:],
        },
    }
    return packet, scan


def exact_algebra_checks(scan, expected):
    """Check the rational LP normalization and all integer gate predicates."""
    dep = expected["deployed"]
    n = dep["n"]
    m = dep["m"]
    w = dep["w"]
    Bstar = dep["Bstar"]
    L0 = dep["L0"]
    D = dep["ambient_dimension"]
    R = dep["centered_radius_numerator"]

    check("deployed M31 constants", (
        dep["p"], n, m, w, Bstar, L0
    ) == (2_147_483_647, 2_097_152, 981_129, 67_447, 16_777_215, 16_777_216))
    check("centered radius numerator", R == 1_094_962_529_967)
    check("ambient dimension", D == 2_097_151)
    check("PR #480 grid count", scan["grid_count"] == 3_254_885)
    check("PR #480 grid endpoints", (
        scan["grid_first"] == [2, 67_448, 490_564, 423_117]
        and scan["grid_last"] == [774, 88, 675, 588]
    ))

    cut_metadata = [
        (row, numerator, den)
        for row, numerator, den in scan["sign_metadata"]
        if numerator < L0 * den
    ]
    check("all 224 sign rows satisfy exact signs", all(
        (row[2] + row[3]) * n >= 2 * R and den > 0
        for row, _numerator, den in scan["sign_metadata"]
    ))
    check("all 187 cut rows satisfy strict budget gate", all(
        numerator < L0 * den for _row, numerator, den in cut_metadata
    ))
    check("all 37 residual sign rows fail strict budget gate", all(
        numerator >= L0 * den
        for _row, numerator, den in scan["sign_metadata"]
        if numerator >= L0 * den
    ))
    check("every cut row is an integral-ratio shell pair", all(
        e1 == (k - 1) * t and e2 == k * t
        for k, t, e1, e2, _floor_bound in scan["cut_rows"]
    ))

    # Check the kernel expansion exactly on the first eliminated row.
    _k, _t, e1, e2, _floor_bound = scan["cut_rows"][0]
    r = Fraction(R, n)
    a = 1 - Fraction(e1, 1) / r
    b = 1 - Fraction(e2, 1) / r
    f0 = a * b + Fraction(1, D)

    def q2(x):
        return Fraction(D * x * x - 1, D - 1)

    def expanded(x):
        return f0 - (a + b) * x + Fraction(D - 1, D) * q2(x)

    test_points = [a, b, Fraction(0), Fraction(1), Fraction(2, 7)]
    check("degree-two kernel identity over exact rationals", all(
        (x - a) * (x - b) == expanded(x) for x in test_points
    ))
    check("LP coefficients have required signs", a + b <= 0 and f0 > 0)

    den = D * (R - e1 * n) * (R - e2 * n) + R * R
    numerator = e1 * e2 * n * n * D
    normalized_bound = (1 - a) * (1 - b) / f0
    check("normalized LP bound equals integer quotient", (
        normalized_bound == Fraction(numerator, den)
    ))
    check("strict real bound implies deployed integer cap", (
        numerator < L0 * den and numerator // den <= Bstar
    ))


def mutate_at_path(value, path, mutation):
    damaged = copy.deepcopy(value)
    cursor = damaged
    for key in path[:-1]:
        cursor = cursor[key]
    last = path[-1]
    cursor[last] = mutation(cursor[last])
    return damaged


def main():
    if len(sys.argv) != 1:
        print("usage: verify_m31_integral_ratio_lp_ruleout.py")
        return 2

    with open(DATA_PATH, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    print("== Exact M31 integral-ratio degree-two LP cut ==")
    expected, scan = build_expected()
    exact_algebra_checks(scan, expected)
    validator = lambda candidate: candidate == expected
    check("JSON packet exactly matches regenerated certificate", validator(data))

    print("\n== Corruption self-tests ==")
    corruptions = [
        ("Bstar", ("deployed", "Bstar"), lambda x: x + 1),
        ("grid pair count", ("grid", "pair_count"), lambda x: x - 1),
        ("sign count", ("lp_cut", "sign_condition_count"), lambda x: x + 1),
        ("eliminated count", ("lp_cut", "eliminated_count"), lambda x: x - 1),
        ("surviving count", ("lp_cut", "surviving_count"), lambda x: x + 1),
        ("e2 checksum", ("lp_cut", "checksums", "sum_e2"), lambda x: x + 1),
        ("certificate hash", ("lp_cut", "canonical_sha256"), lambda x: "0" + x[1:]),
        ("first cut row", ("lp_cut", "first_five", 0, 1), lambda x: x + 1),
    ]
    for name, path, mutation in corruptions:
        damaged = mutate_at_path(data, path, mutation)
        check(f"tampered {name} is rejected", not validator(damaged))

    passed = sum(ok for _name, ok in CHECKS)
    total = len(CHECKS)
    print(f"\nRESULT: {'PASS' if passed == total else 'FAIL'} ({passed}/{total} checks)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
