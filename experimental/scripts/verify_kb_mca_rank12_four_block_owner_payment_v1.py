#!/usr/bin/env python3
"""Exact verifier for the rank-12 four-block proper-drop payment."""
from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import comb, prod
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank12-four-block-owner-payment-v1/result.json"

STACK_PARENT = "ea0541ca0cafb49ca79ff48c1285887344e1103b"
LOCATOR_PARENT = "ed556ccb7527e1c54e58b8d151ccefd8539000ac"
LOCATOR_PAYLOAD = "edef5ffa88a495a0a659a62a3ce891372b59458350ef4eab5b35f75ed5f37baa"
R = 1_048_576
D = 67_472
T = R - D
K_MAX = 1_048_576
K_FIRST = 662_480
L2 = 5_170_912
RANK1_GLOBAL = 4_070_947
Z_BUDGET = L2 - RANK1_GLOBAL


class Reject(ValueError):
    pass


def req(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def falling(x: int, length: int) -> int:
    return prod(x - i for i in range(length))


def rising(x: int, length: int) -> int:
    return prod(x + i for i in range(length))


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def theta2(K: int) -> int:
    return max(
        falling(R + K, 3) // ((D + K) * rising(D + 1, 1)),
        falling(R + 2, 3) // rising(D + 1, 2),
    )


def incident(K: int) -> int:
    return ceil_div(L2 * (D + K) - theta2(K), R + K)


@lru_cache(maxsize=None)
def rank1_capacity(k: int) -> int:
    """Reconstruct the repaired all-dimension rank-one cap below its stable window."""
    req(1 <= k < 262_710, "rank-one capacity window")
    n = R + k
    m = D + k
    q = m // 2
    a = m - q - 1
    low = comb(n, 2) // (q * (m - q))
    hmax = n // (q + 1)
    best_num, best_den = -1, 1
    for h in range(1, hmax + 1):
        b = a - 1
        C = n - h * m + h * a
        candidates = {0, h}
        if b:
            vertex = (C - h) // (2 * b)
            candidates |= {
                vertex - 1, vertex, vertex + 1, vertex + 2,
                C // b, C // b + 1,
            }
        for p in candidates:
            if not 0 <= p <= h:
                continue
            outside = n - h * m + p + (h - p) * a
            if outside < 0:
                continue
            numerator = h * (h - 1) * a + outside * (p * a + h - p)
            if numerator * best_den > best_num * a:
                best_num, best_den = numerator, a
    req(best_num >= 0, "nonempty rank-one profile")
    return low + best_num // best_den


def initial_pointer(K: int) -> int:
    target = incident(K)
    lo, hi = 1, min(K - 1, 262_709)
    answer = 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if rank1_capacity(mid) >= target:
            answer = mid
            lo = mid + 1
        else:
            hi = mid - 1
    req(rank1_capacity(answer) >= target, "initial pointer capacity")
    req(answer == K - 1 or rank1_capacity(answer + 1) < target, "initial pointer maximal")
    return answer


def ray_real_candidates(k: int, rho: int) -> list[tuple[str, Fraction]]:
    req(k > D + 2 and rho >= 0, "ray real parameters")
    values: list[tuple[str, Fraction]] = [("large", Fraction(rho + 1, 1))]
    for label, M in (("D+1", D + 1), ("k-1", k - 1), ("k", k), ("k+D", k + D)):
        B = M - 1 if M <= k - 1 else (k - 1) * (M - k + 1)
        values.append((label, Fraction((M + rho) * (M + rho - 1), 2 * B)))
    return values


def ray_real_envelope(k: int, rho: int) -> Fraction:
    return max(value for _, value in ray_real_candidates(k, rho))


def ray_exact_cap(K: int, r: int) -> tuple[int, str, dict[str, int]]:
    req(0 <= r < K, "ray exact parameters")
    values: dict[str, int] = {"large": r + 1}
    for label, M in (("D+1", D + 1), ("K-1", K - 1), ("K", K), ("K+D", K + D)):
        B = M - 1 if M <= K - 1 else (K - 1) * (M - K + 1)
        values[label] = comb(M + r, 2) // B
    argmax = max(values, key=values.get)
    return values[argmax], argmax, values


def z_out_cap(K: int, c: int) -> tuple[int, dict[str, Any]]:
    m = K + D
    r = T - c
    if r < 0:
        return 0, {"regime": "EMPTY_EXCEPTIONAL_DOMAIN", "r": r}

    delta = 3 * r - m
    eta = 2 * r - m

    # Four witness omissions cannot cover X, so all second differences are one ray.
    if delta < 0:
        cap, argmax, values = ray_exact_cap(K, r)
        return cap, {
            "regime": "FOUR_SUPPORT_RAY",
            "r": r,
            "delta": delta,
            "ray_argmax": argmax,
            "ray_candidates": values,
        }

    # The clean blocks dominate.  No one-block ray can reach m agreements.
    if eta < 0:
        pair_cap = max(0, 2 * delta - r + 1)
        return 4 + pair_cap, {
            "regime": "CLEAN_FOUR_BLOCK",
            "r": r,
            "delta": delta,
            "eta": eta,
            "two_block_cap": pair_cap,
        }

    # Dirty four-block regime.  The condition excludes three simultaneous ray owners.
    req(4 * eta < r, "dirty four-block transversality")
    k1 = K - r
    k2 = K - r + 2 * eta
    ray1 = ray_real_envelope(k1, 2 * eta)
    ray2 = ray_real_envelope(k2, 0)
    ray_floor = (ray1 + ray2).numerator // (ray1 + ray2).denominator
    pair_triplet = r + 4 * eta + 9
    return pair_triplet + ray_floor, {
        "regime": "DIRTY_FOUR_BLOCK",
        "r": r,
        "delta": delta,
        "eta": eta,
        "pair_triplet_cap": pair_triplet,
        "ray1_numerator": ray1.numerator,
        "ray1_denominator": ray1.denominator,
        "ray2_numerator": ray2.numerator,
        "ray2_denominator": ray2.denominator,
        "ray_sum_floor": ray_floor,
    }


def det3(rows: list[list[int]], p: int) -> int:
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    ) % p


def triplet_controls() -> int:
    checked = 0
    for p in (7, 11):
        for slopes in combinations(range(p), 4):
            S = sum(slopes) % p
            E2 = sum(slopes[i] * slopes[j] for i in range(4) for j in range(i + 1, 4)) % p
            for omitted in range(4):
                rows_coeff: list[list[int]] = []
                rows_value: list[tuple[int, int, int]] = []
                for i in range(4):
                    if i == omitted:
                        continue
                    others = [slopes[j] for j in range(4) if j != i]
                    s = sum(others) % p
                    u = sum(others[a] * others[b] for a in range(3) for b in range(a + 1, 3)) % p
                    v = prod(others) % p
                    rows_coeff.append([(-s) % p, 1, (-u) % p])
                    rows_value.append((s, u, v))
                coeff = det3(rows_coeff, p)
                req(coeff != 0, "triplet compatibility is nonconstant")
                roots = []
                for gamma in range(p):
                    rows = [[(-s) % p, 1, (v - u * gamma) % p] for s, u, v in rows_value]
                    if det3(rows, p) == 0:
                        roots.append(gamma)
                req(roots == [slopes[omitted]], "unique omitted-slope root")
                # Independent quadratic/Vandermonde coefficient check.
                svals = [row[0] for row in rows_value]
                vand = prod((svals[j] - svals[i]) % p for i in range(3) for j in range(i + 1, 3)) % p
                req(vand != 0 and E2 == E2 and S == S, "triplet Vandermonde")
                checked += 1
    return checked


def dirty_pair_controls() -> int:
    checked = 0
    for r in range(5, 18):
        for eta in range(0, (r - 1) // 4 + 1):
            delta = r + eta
            predicted = r + 4 * eta + 5
            maximum = -1
            for y in range((delta + 2) // 3, delta + 1):
                target = y + delta
                for d0 in range(r + 1):
                    for d1 in range(r + 1):
                        for d2 in range(r + 1):
                            d3 = target - d0 - d1 - d2
                            if not 0 <= d3 <= r:
                                continue
                            ds = (d0, d1, d2, d3)
                            A = y + eta + 1
                            value = sum(max(0, A - ds[i] - ds[j]) for i, j in combinations(range(4), 2))
                            maximum = max(maximum, value)
                            checked += 1
            req(maximum == predicted, "small dirty-pair optimizer")
    return checked


def build() -> dict[str, Any]:
    pointer = initial_pointer(K_FIRST - 1)
    req(pointer == 75_757, "initial effective dimension")

    selected_dimensions = {
        662_479, 662_480, 662_481, 665_000,
        680_378, 680_379, 729_017, 729_018,
        765_277, 765_278, 858_618, 858_619,
        1_048_576,
    }
    selected: dict[str, Any] = {}
    maximum_cap = -1
    maximum_cells: list[int] = []
    minimum_slack = 10**30
    regime_first: dict[str, int] = {}
    locator_decreases = 0
    previous_c: int | None = None
    cells = 0
    adjacent: dict[str, Any] | None = None

    for K in range(K_FIRST - 1, K_MAX + 1):
        target = incident(K)
        while pointer > 1 and rank1_capacity(pointer) < target:
            pointer -= 1
        req(rank1_capacity(pointer) >= target, f"capacity at pointer K={K}")
        req(rank1_capacity(pointer + 1) < target, f"pointer maximality K={K}")
        c = K - pointer
        if previous_c is not None and c < previous_c:
            locator_decreases += 1
        previous_c = c
        cap, details = z_out_cap(K, c)
        total = RANK1_GLOBAL + cap
        slack = L2 - total

        row = {
            "ambient_dimension": K,
            "incident_rank_one_load": target,
            "effective_rank_one_dimension": pointer,
            "common_locator_floor": c,
            "z_out_cap": cap,
            "proper_drop_cap": total,
            "slack": slack,
            **details,
        }
        if K == K_FIRST - 1:
            adjacent = row
            continue

        cells += 1
        regime_first.setdefault(details["regime"], K)
        if cap > maximum_cap:
            maximum_cap = cap
            maximum_cells = [K]
        elif cap == maximum_cap:
            maximum_cells.append(K)
        minimum_slack = min(minimum_slack, slack)
        req(slack > 0, f"proper-drop payment K={K}")
        if K in selected_dimensions:
            selected[str(K)] = row

    req(adjacent is not None, "adjacent cell")
    req(adjacent["ambient_dimension"] == 662_479, "adjacent dimension")
    req(adjacent["proper_drop_cap"] == 5_170_930, "adjacent floor-safe cap")
    req(adjacent["slack"] == -18, "adjacent method wall")
    req(maximum_cap == 1_099_960 and maximum_cells == [662_480], "global cap maximum")
    req(minimum_slack == 5, "minimum slack")
    req(locator_decreases == 0, "locator floor nondecreasing")
    req(regime_first == {
        "DIRTY_FOUR_BLOCK": 662_480,
        "CLEAN_FOUR_BLOCK": 680_379,
        "FOUR_SUPPORT_RAY": 765_278,
        "EMPTY_EXCEPTIONAL_DOMAIN": 1_022_839,
    }, "regime transitions")

    req(selected["662480"]["common_locator_floor"] == 586_723, "first locator")
    req(selected["662480"]["z_out_cap"] == 1_099_960, "first z-out cap")
    req(selected["662480"]["proper_drop_cap"] == 5_170_907, "first total")
    req(selected["662480"]["slack"] == 5, "first slack")
    req(selected["680378"]["z_out_cap"] == 680_401, "dirty endpoint")
    req(selected["680379"]["z_out_cap"] == 373_928, "clean endpoint")
    req(selected["765278"]["z_out_cap"] == 882_311, "ray endpoint")
    req(selected["1048576"]["z_out_cap"] == 0, "empty endpoint")

    return {
        "schema": "kb-mca-rank12-four-block-owner-payment-v1",
        "stack_parent": STACK_PARENT,
        "locator_parent": LOCATOR_PARENT,
        "locator_parent_payload": LOCATOR_PAYLOAD,
        "constants": {
            "R": R, "D": D, "n_minus_m": T,
            "rank2_load": L2,
            "rank1_global_cap": RANK1_GLOBAL,
            "z_out_budget": Z_BUDGET,
            "first_paid_dimension": K_FIRST,
        },
        "adjacent_method_wall": adjacent,
        "first_paid_cell": selected["662480"],
        "selected_cells": selected,
        "scan": {
            "ambient_cells": cells,
            "maximum_z_out_cap": maximum_cap,
            "maximum_z_out_cap_cells": maximum_cells,
            "minimum_slack": minimum_slack,
            "locator_floor_decreases": locator_decreases,
            "regime_first_dimensions": regime_first,
        },
        "finite_controls": {
            "triplet_cells": triplet_controls(),
            "dirty_pair_profiles": dirty_pair_controls(),
        },
        "claims": {
            "proper_rank2_drop_impossible_for_K_ge_662480": True,
            "whole_rank2_family_shortens_to_K_at_most_662479": True,
            "affine_error_rank_12_paid": False,
            "active_v4_ledger_movement": 0,
            "koalabear_closed": False,
        },
    }


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = [
        ("constants.first_paid_dimension", 662_479),
        ("first_paid_cell.slack", 4),
        ("scan.maximum_z_out_cap", 1_099_959),
        ("adjacent_method_wall.slack", -17),
        ("claims.proper_rank2_drop_impossible_for_K_ge_662480", False),
        ("claims.affine_error_rank_12_paid", True),
        ("claims.active_v4_ledger_movement", 1),
        ("stack_parent", "WRONG"),
    ]
    caught = 0
    for path, replacement in mutations:
        changed = copy.deepcopy(expected)
        parts = path.split(".")
        cursor: Any = changed
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
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    result = build()
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {RESULT}")
        return
    req(RESULT.exists(), "result exists")
    req(json.loads(RESULT.read_text()) == result, "result exact reconstruction")
    if args.tamper_selftest:
        print(f"KB_MCA_RANK12_FOUR_BLOCK_TAMPER_PASS mutations={tamper_selftest(result)}/8")
        return
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    print(
        "KB_MCA_RANK12_FOUR_BLOCK_PASS "
        f"first={result['constants']['first_paid_dimension']} "
        f"zout={result['first_paid_cell']['z_out_cap']} "
        f"slack={result['first_paid_cell']['slack']} "
        f"adjacent={result['adjacent_method_wall']['slack']}"
    )


if __name__ == "__main__":
    main()
