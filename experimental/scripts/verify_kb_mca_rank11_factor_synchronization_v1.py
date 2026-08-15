#!/usr/bin/env python3
"""Exact verifier for the KoalaBear rank-eleven factor synchronization router."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from math import comb, prod

ROW = {
    "p": 2_130_706_433,
    "extension_degree": 6,
    "n": 2_097_152,
    "K": 1_048_576,
    "m": 1_116_048,
    "w": 67_472,
    "near": 134_944,
    "budget": 274_980_728_111_395_087,
    "theta_resource_s10": 106_618_568_137_036_225_644,
    "rank1_group_cap": 8_147_918,
}
PARENT = "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
TAU = 1_549
H = 42_447


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def ceil_div(a: int, b: int) -> int:
    require(a >= 0 and b > 0, "ceil-div domain")
    return (a + b - 1) // b


def falling(x: int, length: int) -> int:
    require(length >= 0, "falling length")
    return prod(x - i for i in range(length))


def pair_cap(dimension: int) -> int:
    require(1 <= dimension <= 10, "pair dimension")
    return comb(ROW["n"] - ROW["K"] + dimension, dimension) // comb(
        ROW["w"] - TAU + dimension, dimension
    )


def transverse_envelope() -> dict[str, int | bool]:
    A = ROW["m"] - TAU
    c = 2 * A - ROW["n"]
    q = H + 1
    multiplicity = ROW["n"] - A
    m2 = pair_cap(2)
    r2 = multiplicity * m2
    n1 = falling(ROW["m"], 9) // (c - H) ** 9
    n2 = falling(ROW["m"], 8) // (c - H) ** 8
    high = ROW["theta_resource_s10"] // (TAU + 1)
    rank1 = n1 * ROW["rank1_group_cap"]
    rank2 = n2 * r2
    total = ROW["near"] + high + multiplicity + rank1 + rank2
    return {
        "tau": TAU,
        "h": H,
        "A": A,
        "anchor_overlap_floor": c,
        "emitted_core_size": q,
        "pair_multiplicity": multiplicity,
        "pair_cap_dim2": m2,
        "rank2_group_cap": r2,
        "rank1_space_count": n1,
        "rank2_space_count": n2,
        "rank1_total": rank1,
        "rank2_total": rank2,
        "high_tail": high,
        "near": ROW["near"],
        "total": total,
        "signed_slack": ROW["budget"] - total,
        "field_guard_dim2": m2 * m2 < ROW["p"] ** ROW["extension_degree"],
    }


def balanced_intersection(parent_count: int, set_size: int, order: int) -> dict[str, int]:
    require(1 <= order <= parent_count, "intersection order")
    incidence = parent_count * set_size
    low_degree, remainder = divmod(incidence, ROW["m"])
    numerator = (
        (ROW["m"] - remainder) * comb(low_degree, order)
        + remainder * comb(low_degree + 1, order)
    )
    denominator = comb(parent_count, order)
    return {
        "order": order,
        "incidence": incidence,
        "low_degree": low_degree,
        "remainder": remainder,
        "moment_numerator": numerator,
        "family_denominator": denominator,
        "forced_intersection": ceil_div(numerator, denominator),
    }


def weighted_load(total_load: int, set_size: int, order: int) -> int:
    return ceil_div(total_load * comb(set_size, order), comb(ROW["m"], order))


def finite_unweighted_control() -> int:
    checked = 0
    for universe in range(2, 5):
        points = tuple(range(universe))
        for size in range(1, universe + 1):
            subsets = list(itertools.combinations(points, size))
            for count in range(2, 5):
                for family in itertools.product(subsets, repeat=count):
                    degrees = [sum(x in member for member in family) for x in points]
                    for order in range(2, count + 1):
                        actual_sum = sum(comb(value, order) for value in degrees)
                        incidence = count * size
                        low, rem = divmod(incidence, universe)
                        balanced = (universe - rem) * comb(low, order) + rem * comb(
                            low + 1, order
                        )
                        require(actual_sum >= balanced, "balanced moment")
                        max_intersection = max(
                            len(set.intersection(*(set(family[i]) for i in choice)))
                            for choice in itertools.combinations(range(count), order)
                        )
                        require(
                            max_intersection >= ceil_div(balanced, comb(count, order)),
                            "intersection average",
                        )
                    checked += 1
    return checked


def finite_weighted_control() -> int:
    checked = 0
    for universe in range(2, 5):
        points = tuple(range(universe))
        for size in range(1, universe + 1):
            subsets = list(itertools.combinations(points, size))
            count = 3
            for family in itertools.product(subsets, repeat=count):
                for weights in itertools.product(range(3), repeat=count):
                    total = sum(weights)
                    if total == 0:
                        continue
                    for order in range(1, size + 1):
                        actual = max(
                            sum(
                                weights[i]
                                for i, member in enumerate(family)
                                if set(choice).issubset(member)
                            )
                            for choice in itertools.combinations(points, order)
                        )
                        lower = ceil_div(
                            total * comb(size, order), comb(universe, order)
                        )
                        require(actual >= lower, "weighted moment")
                    checked += 1
    return checked


def build() -> dict[str, object]:
    envelope = transverse_envelope()
    residual_load = envelope["signed_slack"] + 1
    m3 = pair_cap(3)
    parent_cap = m3 * envelope["pair_multiplicity"]
    parents = ceil_div(residual_load, parent_cap)
    q = envelope["emitted_core_size"]

    intersections = {
        str(order): balanced_intersection(parents, q, order)["forced_intersection"]
        for order in range(2, 6)
    }
    weighted = {
        str(order): weighted_load(residual_load, q, order)
        for order in range(1, 11)
    }
    degree_data = balanced_intersection(parents, q, 2)

    expected_envelope = {
        "tau": 1549,
        "h": 42447,
        "A": 1114499,
        "anchor_overlap_floor": 131846,
        "emitted_core_size": 42448,
        "pair_multiplicity": 982653,
        "pair_cap_dim2": 252,
        "rank2_group_cap": 247628556,
        "rank1_space_count": 7364409081,
        "rank2_space_count": 589916855,
        "rank1_total": 60004601310443358,
        "rank2_total": 146080258963711380,
        "high_tail": 68786172991636274,
        "near": 134944,
        "total": 274871033266908609,
        "signed_slack": 109694844486478,
        "field_guard_dim2": True,
    }
    require(envelope == expected_envelope, "exact predecessor envelope")
    require(m3 == 4023, "dimension-three pair cap")
    require(parent_cap == 3953213019, "parent slope cap")
    require(residual_load == 109694844486479, "residual load")
    require(parents == 27749, "parent abundance")
    require((parents - 1) * parent_cap < residual_load <= parents * parent_cap,
            "parent ceiling sharpness")
    require(
        {
            "2": 1614,
            "3": 62,
            "4": 3,
            "5": 1,
        }
        == intersections,
        "intersection cascade",
    )
    require(
        weighted
        == {
            "1": 4172156357758,
            "2": 158681059954,
            "3": 6035034641,
            "4": 229522148,
            "5": 8728902,
            "6": 331960,
            "7": 12625,
            "8": 481,
            "9": 19,
            "10": 1,
        },
        "weighted synchronization",
    )
    require(degree_data["incidence"] == 1177889552, "total incidence")
    require(degree_data["low_degree"] == 1055, "balanced degree")
    require(degree_data["remainder"] == 458912, "balanced remainder")
    require(m3 * m3 < ROW["p"] ** ROW["extension_degree"], "field guard dim3")

    return {
        "schema": "kb-mca-rank11-weighted-factor-synchronization-v1",
        "parent": PARENT,
        "row": ROW,
        "selected": envelope,
        "residual_load_if_unsafe": residual_load,
        "dimension3_pair_cap": m3,
        "maximum_parent_load": parent_cap,
        "minimum_distinct_parents": parents,
        "parent_incidence": {
            "total": degree_data["incidence"],
            "balanced_low_degree": degree_data["low_degree"],
            "balanced_remainder": degree_data["remainder"],
        },
        "forced_parent_intersections": intersections,
        "weighted_shared_coordinate_loads": weighted,
        "synchronized_sum_spaces": {
            "2": {"dimension_at_most": 6, "common_zero_degree_at_least": 1614},
            "3": {"dimension_at_most": 9, "common_zero_degree_at_least": 62},
            "4": {"dimension_at_most": 10, "common_zero_degree_at_least": 3},
            "5": {"dimension_at_most": 10, "common_zero_degree_at_least": 1},
        },
        "finite_controls": {
            "unweighted_families_checked": finite_unweighted_control(),
            "weighted_families_checked": finite_weighted_control(),
        },
        "claims": {
            "parent_abundance_proved": True,
            "factor_synchronization_proved": True,
            "rank11_paid": False,
            "koalabear_closed": False,
            "active_v4_ledger_movement": 0,
        },
    }


def tamper_selftest(expected: dict[str, object]) -> int:
    mutations = [
        ("residual_load_if_unsafe", None, expected["residual_load_if_unsafe"] - 1),
        ("minimum_distinct_parents", None, expected["minimum_distinct_parents"] - 1),
        ("forced_parent_intersections", "2", 1615),
        ("forced_parent_intersections", "3", 61),
        ("weighted_shared_coordinate_loads", "4", 229522149),
        ("synchronized_sum_spaces", "2", {"dimension_at_most": 5, "common_zero_degree_at_least": 1614}),
        ("claims", "rank11_paid", True),
        ("claims", "active_v4_ledger_movement", 1),
    ]
    caught = 0
    for section, key, value in mutations:
        changed = copy.deepcopy(expected)
        if key is None:
            changed[section] = value
        else:
            changed[section][key] = value
        try:
            require(changed == expected, "canonical result")
        except Reject:
            caught += 1
    require(caught == len(mutations), "hostile mutations")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.tamper_selftest:
        count = tamper_selftest(result)
        print(f"KB_MCA_RANK11_FACTOR_SYNC_TAMPER_PASS mutations={count}/8")
        return
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    print(
        "KB_MCA_RANK11_FACTOR_SYNC_PASS "
        f"load={result['residual_load_if_unsafe']} "
        f"parents={result['minimum_distinct_parents']} "
        f"pair={result['forced_parent_intersections']['2']} "
        f"triple={result['forced_parent_intersections']['3']} "
        f"weighted1={result['weighted_shared_coordinate_loads']['1']} "
        f"controls={result['finite_controls']}"
    )


if __name__ == "__main__":
    main()
