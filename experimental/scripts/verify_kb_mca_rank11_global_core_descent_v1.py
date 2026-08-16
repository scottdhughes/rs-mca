#!/usr/bin/env python3
"""Exact verifier for the KoalaBear rank-eleven global-core descent payment."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from fractions import Fraction
from math import comb, prod
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank11-global-core-descent-v1/result.json"

PARENT = "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
ROW = {
    "p": 2_130_706_433,
    "extension_degree": 6,
    "R": 1_048_576,
    "d": 67_472,
    "n": 2_097_152,
    "K": 1_048_576,
    "m": 1_116_048,
    "near": 134_944,
    "budget": 274_980_728_111_395_087,
}


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def falling(x: int, length: int) -> int:
    return prod(x - index for index in range(length))


def rising(x: int, length: int) -> int:
    return prod(x + index for index in range(length))


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def theta_resource(rank: int, dimension: int) -> int:
    """The exact pointwise support-margin resource in row (R+K,K,d+K)."""

    R, d = ROW["R"], ROW["d"]
    require(1 <= rank <= dimension, "legal rank/dimension")
    n = R + dimension
    m = d + dimension

    # Both endpoint resources increase with the affine rank:
    # A_(r+1)/A_r=(n-r-1)/(d+r)>1 and B_(r+1)/B_r=(R+r+1)/(d+r+1)>1.
    first = falling(n, rank + 1) // (m * rising(d + 1, rank - 1))
    second = falling(R + rank, rank + 1) // rising(d + 1, rank)
    return max(first, second)


def incidence_floor(load: int, rank: int, dimension: int) -> int:
    R, d = ROW["R"], ROW["d"]
    return ceil_div(
        load * (d + dimension) - theta_resource(rank, dimension),
        R + dimension,
    )


def descent_loads() -> dict[int, int]:
    loads = {10: ROW["budget"] - ROW["near"] + 1}
    for rank in range(10, 1, -1):
        loads[rank - 1] = incidence_floor(loads[rank], rank, rank)
    return loads


def monotonicity_scan(loads: dict[int, int]) -> dict[str, dict[str, int]]:
    """Check every deployed dimension; delayed dimension descent is worst."""

    R, d, K0 = ROW["R"], ROW["d"], ROW["K"]
    result: dict[str, dict[str, int]] = {}

    for rank in range(2, 11):
        denominator_tail = rising(d + 1, rank - 1)
        constant_endpoint = falling(R + rank, rank + 1) // rising(d + 1, rank)
        dimension = rank
        numerator = falling(R + dimension, rank + 1)
        previous: int | None = None
        minimum: int | None = None
        maximum: int | None = None
        strict_decreases = 0
        argmin = dimension

        while dimension <= K0:
            moving_endpoint = numerator // ((d + dimension) * denominator_tail)
            resource = max(moving_endpoint, constant_endpoint)
            value = ceil_div(loads[rank] * (d + dimension) - resource, R + dimension)

            if previous is not None and value < previous:
                strict_decreases += 1
            if minimum is None or value < minimum:
                minimum = value
                argmin = dimension
            if maximum is None or value > maximum:
                maximum = value
            previous = value

            if dimension < K0:
                n = R + dimension
                # falling(n+1,r+1)/falling(n,r+1)=(n+1)/(n-rank)
                numerator = numerator * (n + 1) // (n - rank)
            dimension += 1

        require(strict_decreases == 0, f"rank-{rank} incidence monotonicity")
        require(minimum == loads[rank - 1], f"rank-{rank} delayed endpoint minimum")
        require(argmin == rank, f"rank-{rank} endpoint argmin")
        result[str(rank)] = {
            "minimum": int(minimum),
            "maximum": int(maximum),
            "argmin_dimension": argmin,
            "strict_decreases": strict_decreases,
            "dimensions_checked": K0 - rank + 1,
        }

    return result


def rank_one_endpoint() -> dict[str, Any]:
    """Exact weighted affine-line bound in the final K=1 row."""

    R, d = ROW["R"], ROW["d"]
    n = R + 1
    m = d + 1
    half = (m - 1) // 2

    # Low-dominant exact witnesses: cross-clone pairs are unique to a point.
    low_pair_floor = half * (half + 1)
    low_cap = comb(n, 2) // low_pair_floor

    # High-dominant points.  If h clone classes can dominate and p of their
    # effective outside deficiencies are 1 while q=h-p are half, the relaxed
    # cap is h(h-1)+W0(p+q/half).  Convexity reduces the general optimization
    # to these endpoint vectors.
    rows: list[dict[str, Any]] = []
    max_dominants = n // (half + 1)
    best_value = Fraction(-1, 1)
    best_row: dict[str, Any] | None = None
    per_h: dict[str, dict[str, Any]] = {}

    for h in range(1, max_dominants + 1):
        best_h = Fraction(-1, 1)
        best_h_row: dict[str, Any] | None = None
        for p in range(h + 1):
            q = h - p
            outside = n - h * m + p + q * half
            if outside < 0:
                continue
            value = Fraction(h * (h - 1), 1) + outside * (
                Fraction(p, 1) + Fraction(q, half)
            )
            row = {
                "dominant_classes": h,
                "unit_deficiencies": p,
                "half_deficiencies": q,
                "outside_weight": outside,
                "bound_numerator": value.numerator,
                "bound_denominator": value.denominator,
                "bound_floor": value.numerator // value.denominator,
            }
            rows.append(row)
            if value > best_h:
                best_h = value
                best_h_row = row
            if value > best_value:
                best_value = value
                best_row = row
        require(best_h_row is not None, f"nonempty high table h={h}")
        per_h[str(h)] = best_h_row

    require(best_row is not None, "nonempty high table")
    high_cap = best_value.numerator // best_value.denominator
    total_cap = low_cap + high_cap

    require(low_cap == 483, "rank-one low cap")
    require(high_cap == 4_070_464, "rank-one high cap")
    require(best_row == {
        "dominant_classes": 8,
        "unit_deficiencies": 8,
        "half_deficiencies": 0,
        "outside_weight": 508_801,
        "bound_numerator": 4_070_464,
        "bound_denominator": 1,
        "bound_floor": 4_070_464,
    }, "rank-one high extremizer")
    require(total_cap == 4_070_947, "rank-one total cap")

    return {
        "n": n,
        "K": 1,
        "m": m,
        "half": half,
        "maximum_dominant_classes": max_dominants,
        "low_cross_pair_floor": low_pair_floor,
        "low_cap": low_cap,
        "high_cap": high_cap,
        "high_extremizer": best_row,
        "high_best_by_class_count": per_h,
        "total_cap": total_cap,
        "endpoint_rows_checked": len(rows),
    }


def small_controls() -> dict[str, int]:
    """Finite controls for the two elementary combinatorial inequalities."""

    low_checked = 0
    for total in range(3, 15, 2):
        half = (total - 1) // 2
        # Positive compositions with every part at most half.
        def rec(rem: int, maximum: int, prefix: tuple[int, ...]) -> None:
            nonlocal low_checked
            if rem == 0:
                if len(prefix) >= 2:
                    cross = sum(prefix[i] * prefix[j]
                                for i in range(len(prefix))
                                for j in range(i + 1, len(prefix)))
                    require(cross >= half * (half + 1), "small low cross-pair floor")
                    low_checked += 1
                return
            start = min(maximum, rem, half)
            for part in range(start, 0, -1):
                rec(rem - part, part, prefix + (part,))
        rec(total, half, ())

    high_checked = 0
    # Verify the high-resource inequality for small weight multisets and every
    # legal dominant class.  This is independent of geometric realizability.
    for weights in itertools.product(range(1, 6), repeat=4):
        total = sum(weights)
        m = 5
        dominant = [i for i, weight in enumerate(weights) if weight > m // 2]
        h = len(dominant)
        if h == 0:
            continue
        deficiencies = {i: max(1, m - min(weights[i], m - 1)) for i in dominant}
        outside_relaxed = total - sum(m - deficiencies[i] for i in dominant)
        require(outside_relaxed >= total - sum(weights[i] for i in dominant),
                "small relaxed outside weight")
        for i in dominant:
            a = deficiencies[i]
            resource = sum(min(weights[j], a) for j in range(len(weights)) if j != i)
            relaxed = (h - 1) * a + outside_relaxed
            require(resource <= relaxed, "small high resource inequality")
            high_checked += 1

    return {
        "low_compositions_checked": low_checked,
        "high_weight_cells_checked": high_checked,
    }


def build() -> dict[str, Any]:
    loads = descent_loads()
    monotonicity = monotonicity_scan(loads)
    endpoint = rank_one_endpoint()
    controls = small_controls()

    expected_loads = {
        10: 274_980_728_111_260_144,
        9: 17_695_628_624_859_819,
        8: 1_138_737_729_126_327,
        7: 73_278_302_796_469,
        6: 4_715_427_489_703,
        5: 303_431_536_894,
        4: 19_525_148_223,
        3: 1_256_382_675,
        2: 80_843_204,
        1: 5_201_865,
    }
    require(loads == expected_loads, "descent load table")
    slack = loads[1] - endpoint["total_cap"]
    require(slack == 1_130_918, "final contradiction slack")

    return {
        "schema": "kb-mca-rank11-global-core-descent-v1",
        "parent": PARENT,
        "row": ROW,
        "descent_loads": {str(rank): loads[rank] for rank in range(10, 0, -1)},
        "endpoint_theta_resources": {
            str(rank): theta_resource(rank, rank) for rank in range(10, 1, -1)
        },
        "monotonicity": monotonicity,
        "rank_one_endpoint": endpoint,
        "finite_controls": controls,
        "final_contradiction": {
            "forced_rank_one_load": loads[1],
            "rank_one_upper_bound": endpoint["total_cap"],
            "slack": slack,
        },
        "claims": {
            "post_near_affine_error_rank_11_paid": True,
            "near_addback": ROW["near"],
            "complete_affine_error_rank_11_branch_paid": True,
            "active_v4_ledger_movement": 0,
            "koalabear_closed": False,
        },
    }


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = [
        ("descent_loads", "1", expected["descent_loads"]["1"] + 1),
        ("rank_one_endpoint", "low_cap", 482),
        ("rank_one_endpoint", "high_cap", 4_070_465),
        ("final_contradiction", "slack", expected["final_contradiction"]["slack"] - 1),
        ("claims", "complete_affine_error_rank_11_branch_paid", False),
        ("claims", "active_v4_ledger_movement", 1),
        ("claims", "koalabear_closed", True),
        ("parent", "", "WRONG"),
    ]
    caught = 0
    for section, key, replacement in mutations:
        changed = copy.deepcopy(expected)
        if section == "parent":
            changed["parent"] = replacement
        else:
            changed[section][key] = replacement
        try:
            require(changed == expected, "canonical result")
        except Reject:
            caught += 1
    require(caught == len(mutations), "all hostile mutations rejected")
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
    if RESULT.exists():
        actual = json.loads(RESULT.read_text())
        require(actual == result, "result file matches exact reconstruction")
    if args.tamper_selftest:
        print(f"KB_MCA_RANK11_GLOBAL_CORE_TAMPER_PASS mutations={tamper_selftest(result)}/8")
        return
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    print(
        "KB_MCA_RANK11_GLOBAL_CORE_PASS "
        f"rank1_load={result['final_contradiction']['forced_rank_one_load']} "
        f"rank1_cap={result['final_contradiction']['rank_one_upper_bound']} "
        f"slack={result['final_contradiction']['slack']}"
    )


if __name__ == "__main__":
    main()
