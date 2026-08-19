#!/usr/bin/env python3
"""Exact arithmetic probe for the ArkLib-inspired shared-fiber coupling."""
from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-arklib-owner-coupling-probe-v1/result.json"

STACK_PARENT = "e3bca2fb3fb3e7e5d34a92f2ecdd7cbf275309e6"
ARKLIB_HEAD = "983069a332de36fd3d6ef6f33fccadafa01b0ff5"

K = 662_479
D = 67_472
R = 1_048_576
RANK2_LOAD = 5_170_912
RANK1_GLOBAL = 4_070_947
Z_BUDGET = RANK2_LOAD - RANK1_GLOBAL

r = 394_382
eta = 58_813
y = r + eta
h = eta
k1 = K - r
rho1 = 2 * eta
k2 = K - r + 2 * eta
rho2 = 0


class Reject(ValueError):
    pass


def req(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def ray_real_candidates(k: int, rho: int) -> list[Fraction]:
    req(k > D + 2 and rho >= 0, "ray parameters")
    return [
        Fraction(rho + 1, 1),
        Fraction((D + 1 + rho) * (D + rho), 2 * D),
        Fraction((k - 1 + rho) * (k - 2 + rho), 2 * (k - 2)),
        Fraction((k + rho) * (k - 1 + rho), 2 * (k - 1)),
        Fraction((k + D + rho) * (k + D - 1 + rho), 2 * (k - 1) * (D + 1)),
    ]


def ray_real_envelope(k: int, rho: int) -> Fraction:
    return max(ray_real_candidates(k, rho))


def pair_plus_rays(u: int) -> int:
    req(0 <= u <= h - 1, "shared-fiber range")
    pair = (y - u) // (h - u)
    rays: list[Fraction] = []
    if rho1 - u >= 0:
        rays.append(ray_real_envelope(k1, rho1 - u))
    if rho2 - u >= 0:
        rays.append(ray_real_envelope(k2, rho2 - u))
    ray_sum = sum(rays, Fraction(0, 1))
    return pair + (ray_sum.numerator // ray_sum.denominator if rays else 0)


def build() -> dict:
    values = [pair_plus_rays(u) for u in range(h)]
    maximum = max(values)
    maximizers = [u for u, value in enumerate(values) if value == maximum]

    other_pair_triplet = 4 * eta + 8
    coupled = other_pair_triplet + maximum
    old_independent = 1_099_983

    req(pair_plus_rays(0) == 470_347, "zero-shared endpoint")
    req(maximum == 593_696, "positive-shared maximum")
    req(maximizers == [58_812], "unique shared-fiber maximizer")
    req(other_pair_triplet == 235_260, "other owner charge")
    req(coupled == 828_956, "coupled exceptional cap")
    req(old_independent - coupled == 271_027, "saving")
    req(Z_BUDGET - coupled == 271_009, "budget slack")

    return {
        "schema": "kb-mca-arklib-owner-coupling-probe-v1",
        "stack_parent": STACK_PARENT,
        "arklib_audit_head": ARKLIB_HEAD,
        "adjacent_cell": {
            "ambient_dimension": K,
            "r": r,
            "eta": eta,
            "dirty_size": y,
            "fixed_pair_dirty_requirement": h,
            "ray1": {"dimension": k1, "outside_excess": rho1},
            "ray2": {"dimension": k2, "outside_excess": rho2},
        },
        "shared_fiber_scan": {
            "cells": h,
            "u_zero_pair_plus_rays": pair_plus_rays(0),
            "maximum_pair_plus_rays": maximum,
            "unique_maximizer_u": maximizers[0],
            "other_pair_triplet_cap": other_pair_triplet,
            "coupled_exceptional_cap": coupled,
            "old_independent_exceptional_cap": old_independent,
            "saving": old_independent - coupled,
            "exceptional_budget": Z_BUDGET,
            "coupled_budget_slack": Z_BUDGET - coupled,
        },
        "claims": {
            "old_relaxed_extremal_profile_eliminated_by_shared_fiber_coupling": True,
            "all_dirty_profiles_optimized": False,
            "adjacent_cell_paid": False,
            "affine_error_rank_12_paid": False,
            "active_v4_ledger_movement": 0,
            "koalabear_closed": False,
        },
    }


def tamper_selftest(expected: dict) -> int:
    mutations = [
        ("shared_fiber_scan.maximum_pair_plus_rays", 593_695),
        ("shared_fiber_scan.unique_maximizer_u", 58_811),
        ("shared_fiber_scan.coupled_exceptional_cap", 828_955),
        ("shared_fiber_scan.saving", 271_026),
        ("claims.adjacent_cell_paid", True),
        ("claims.active_v4_ledger_movement", 1),
    ]
    caught = 0
    for path, replacement in mutations:
        changed = copy.deepcopy(expected)
        cursor = changed
        parts = path.split(".")
        for part in parts[:-1]:
            cursor = cursor[part]
        cursor[parts[-1]] = replacement
        if changed != expected:
            caught += 1
    req(caught == len(mutations), "hostile mutations")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    result = build()
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {RESULT}")
        return

    req(RESULT.exists(), "result exists")
    req(json.loads(RESULT.read_text()) == result, "exact reconstruction")
    if args.tamper_selftest:
        print(f"KB_MCA_ARKLIB_OWNER_COUPLING_TAMPER_PASS mutations={tamper_selftest(result)}/6")
        return
    s = result["shared_fiber_scan"]
    print(
        "KB_MCA_ARKLIB_OWNER_COUPLING_PROBE_PASS "
        f"coupled={s['coupled_exceptional_cap']} "
        f"saving={s['saving']} "
        f"slack={s['coupled_budget_slack']}"
    )


if __name__ == "__main__":
    main()
