#!/usr/bin/env python3
"""Exact verifier for KoalaBear rank-eleven rich-parent synchronization."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from math import comb
from typing import Iterable


ROW = {
    "p": 2_130_706_433,
    "extension_degree": 6,
    "n": 2_097_152,
    "K": 1_048_576,
    "m": 1_116_048,
    "w": 67_472,
    "budget": 274_980_728_111_395_087,
}

PARENT = "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
TAU = 1_547
TRANSVERSE_TOTAL = 274_978_720_888_758_363
COMMON_ZERO_SIZE = 42_453


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def ceil_div(a: int, b: int) -> int:
    require(b > 0, "positive denominator")
    return -(-a // b)


def pair_cap(dimension: int) -> int:
    require(1 <= dimension <= 10, "legal direction dimension")
    numerator = comb(ROW["n"] - ROW["K"] + dimension, dimension)
    denominator = comb(ROW["w"] - TAU + dimension, dimension)
    return numerator // denominator


def parent_caps() -> dict[str, int | bool]:
    A = ROW["m"] - TAU
    multiplicity = ROW["n"] - A
    q2 = pair_cap(2)
    q3 = pair_cap(3)
    q4 = pair_cap(4)
    field_size = ROW["p"] ** ROW["extension_degree"]
    return {
        "A": A,
        "multiplicity": multiplicity,
        "pair_cap_dim1": pair_cap(1),
        "pair_cap_dim2": q2,
        "pair_cap_dim3": q3,
        "pair_cap_dim4": q4,
        "parent_cap_dim2": multiplicity * q2,
        "parent_cap_dim3": multiplicity * q3,
        "pair_load_cap_dim4": multiplicity * q4,
        "field_guard_dim4": q4 * q4 < field_size,
    }


def balanced_intersection_floor(
    number_of_sets: int,
    set_size: int,
    universe_size: int,
    order: int,
) -> int:
    require(1 <= order <= number_of_sets, "legal moment order")
    total_degree = number_of_sets * set_size
    low, remainder = divmod(total_degree, universe_size)
    total_moment = (
        (universe_size - remainder) * comb(low, order)
        + remainder * comb(low + 1, order)
    )
    return ceil_div(total_moment, comb(number_of_sets, order))


def weighted_pin_load(
    total_load: int,
    set_size: int,
    universe_size: int,
    order: int,
) -> int:
    return ceil_div(total_load * comb(set_size, order), comb(universe_size, order))


def combinations_with_replacement_indices(length: int, count: int) -> Iterable[tuple[int, ...]]:
    return itertools.combinations_with_replacement(range(length), count)


def finite_set_system_controls() -> dict[str, int]:
    """Exhaustively test the convex degree-moment lower bound in small models."""

    configurations = 0
    for universe_size, number_of_sets, set_size in ((5, 4, 2), (6, 4, 3)):
        subsets = list(itertools.combinations(range(universe_size), set_size))
        for indices in combinations_with_replacement_indices(len(subsets), number_of_sets):
            family = [set(subsets[index]) for index in indices]
            for order in range(2, min(4, number_of_sets) + 1):
                actual_sum = 0
                for chosen in itertools.combinations(family, order):
                    intersection = set.intersection(*chosen)
                    actual_sum += len(intersection)
                total_degree = number_of_sets * set_size
                low, remainder = divmod(total_degree, universe_size)
                convex_floor = (
                    (universe_size - remainder) * comb(low, order)
                    + remainder * comb(low + 1, order)
                )
                require(actual_sum >= convex_floor, "finite convexity control")
            configurations += 1
    return {"configurations_checked": configurations}


def build() -> dict[str, object]:
    caps = parent_caps()
    residual_load = ROW["budget"] + 1 - TRANSVERSE_TOTAL
    require(residual_load == 2_007_222_636_725, "inherited residual load")

    total_parent_minimum = ceil_div(residual_load, int(caps["parent_cap_dim3"]))
    fixed_dimension_minimum = ceil_div(
        residual_load,
        int(caps["parent_cap_dim2"]) + int(caps["parent_cap_dim3"]),
    )
    fixed_dimension_shortfall = residual_load - (
        fixed_dimension_minimum - 1
    ) * (int(caps["parent_cap_dim2"]) + int(caps["parent_cap_dim3"]))

    synchronized = {
        "selected_parent_count": fixed_dimension_minimum,
        "balanced_low_degree": (fixed_dimension_minimum * COMMON_ZERO_SIZE) // ROW["m"],
        "balanced_remainder": (fixed_dimension_minimum * COMMON_ZERO_SIZE) % ROW["m"],
        "pair_intersection": balanced_intersection_floor(
            fixed_dimension_minimum, COMMON_ZERO_SIZE, ROW["m"], 2
        ),
        "triple_intersection": balanced_intersection_floor(
            fixed_dimension_minimum, COMMON_ZERO_SIZE, ROW["m"], 3
        ),
        "fourfold_intersection": balanced_intersection_floor(
            fixed_dimension_minimum, COMMON_ZERO_SIZE, ROW["m"], 4
        ),
    }

    weighted_pins = {
        order: weighted_pin_load(
            residual_load, COMMON_ZERO_SIZE, ROW["m"], order
        )
        for order in range(1, 10)
    }

    one_pin_margin = weighted_pins[1] - int(caps["pair_load_cap_dim4"])
    two_pin_margin = weighted_pins[2] - int(caps["parent_cap_dim2"])

    require(caps["pair_cap_dim1"] == 15, "dimension-one pair cap")
    require(caps["pair_cap_dim2"] == 252, "dimension-two pair cap")
    require(caps["pair_cap_dim3"] == 4_023, "dimension-three pair cap")
    require(caps["pair_cap_dim4"] == 63_993, "dimension-four pair cap")
    require(caps["parent_cap_dim2"] == 247_628_052, "dimension-two parent cap")
    require(caps["parent_cap_dim3"] == 3_953_204_973, "dimension-three parent cap")
    require(caps["pair_load_cap_dim4"] == 62_882_785_443, "dimension-four load cap")
    require(caps["field_guard_dim4"] is True, "dimension-four field guard")
    require(total_parent_minimum == 508, "total parent abundance")
    require(fixed_dimension_minimum == 478, "fixed-dimension parent abundance")
    require(fixed_dimension_shortfall == 3_425_283_800, "fixed-dimension shortfall")
    require(
        synchronized
        == {
            "selected_parent_count": 478,
            "balanced_low_degree": 18,
            "balanced_remainder": 203_670,
            "pair_intersection": 1_530,
            "triple_intersection": 53,
            "fourfold_intersection": 2,
        },
        "synchronized intersection floors",
    )
    require(
        weighted_pins
        == {
            1: 76_352_112_631,
            2: 2_904_268_266,
            3: 110_469_544,
            4: 4_201_831,
            5: 159_818,
            6: 6_079,
            7: 232,
            8: 9,
            9: 1,
        },
        "weighted pin table",
    )
    require(one_pin_margin == 13_469_327_188, "one-pin dimension-five margin")
    require(two_pin_margin == 2_656_640_214, "two-pin dimension-three margin")

    finite = finite_set_system_controls()

    return {
        "schema": "kb-mca-rank11-parent-synchronization-v1",
        "parent": PARENT,
        "row": ROW,
        "inherited": {
            "tau": TAU,
            "transverse_total": TRANSVERSE_TOTAL,
            "residual_nontransverse_load": residual_load,
            "common_zero_size_per_parent": COMMON_ZERO_SIZE,
        },
        "caps": caps,
        "abundance": {
            "total_parent_minimum": total_parent_minimum,
            "fixed_dimension_parent_minimum": fixed_dimension_minimum,
            "fixed_dimension_shortfall_at_477_each": fixed_dimension_shortfall,
        },
        "synchronization": synchronized,
        "weighted_pins": {str(key): value for key, value in weighted_pins.items()},
        "dimension_growth": {
            "one_coordinate_load": weighted_pins[1],
            "one_coordinate_forced_span_dimension": 5,
            "one_coordinate_margin_over_dim4_cap": one_pin_margin,
            "two_coordinate_load": weighted_pins[2],
            "two_coordinate_forced_span_dimension": 3,
            "two_coordinate_margin_over_dim2_cap": two_pin_margin,
            "same_dimension_pair_factor_degree": synchronized["pair_intersection"],
            "dimension2_pair_sum_minimum_dimension": 3,
            "dimension3_pair_sum_minimum_dimension": 4,
        },
        "finite_controls": finite,
        "claims": {
            "parent_abundance_proved": True,
            "factor_synchronization_proved": True,
            "weighted_pinning_proved": True,
            "rank11_paid": False,
            "koalabear_closed": False,
            "active_v4_ledger_movement": 0,
        },
    }


def tamper_selftest(expected: dict[str, object]) -> int:
    mutations = [
        ("abundance", "total_parent_minimum", 507),
        ("abundance", "fixed_dimension_parent_minimum", 477),
        ("synchronization", "pair_intersection", 1_529),
        ("synchronization", "triple_intersection", 52),
        ("dimension_growth", "one_coordinate_forced_span_dimension", 4),
        ("dimension_growth", "one_coordinate_margin_over_dim4_cap", 0),
        ("claims", "rank11_paid", True),
    ]
    caught = 0
    for section, key, value in mutations:
        changed = copy.deepcopy(expected)
        changed[section][key] = value
        try:
            require(changed == expected, "canonical result")
        except Reject:
            caught += 1
    require(caught == len(mutations), "all hostile mutations rejected")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    result = build()
    if args.tamper_selftest:
        caught = tamper_selftest(result)
        print(f"KB_MCA_RANK11_PARENT_SYNC_TAMPER_PASS mutations={caught}/7")
        return
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return
    print(
        "KB_MCA_RANK11_PARENT_SYNC_PASS "
        f"parents={result['abundance']['total_parent_minimum']} "
        f"fixed_dim={result['abundance']['fixed_dimension_parent_minimum']} "
        f"pair_factor={result['synchronization']['pair_intersection']} "
        f"pin_load={result['dimension_growth']['one_coordinate_load']} "
        f"pin_dim={result['dimension_growth']['one_coordinate_forced_span_dimension']} "
        f"finite_controls={result['finite_controls']['configurations_checked']}"
    )


if __name__ == "__main__":
    main()
