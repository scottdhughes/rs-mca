#!/usr/bin/env python3
"""Independent arithmetic audit of the rank-eleven parent synchronization packet."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from math import comb


N = 2_097_152
K = 1_048_576
M = 1_116_048
W = 67_472
TAU = 1_547
BUDGET = 274_980_728_111_395_087
TRANSVERSE = 274_978_720_888_758_363
Q = 42_453
P = 2_130_706_433


def ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def cap(dimension: int) -> int:
    top = 1
    bottom = 1
    for j in range(1, dimension + 1):
        top *= N - K + j
        bottom *= W - TAU + j
    return top // bottom


def balanced_floor(number: int, size: int, universe: int, order: int) -> int:
    low, rem = divmod(number * size, universe)
    total = (universe - rem) * comb(low, order) + rem * comb(low + 1, order)
    return ceiling(Fraction(total, comb(number, order)))


def build() -> dict[str, object]:
    A = M - TAU
    multiplicity = N - A
    residual = BUDGET + 1 - TRANSVERSE

    q1, q2, q3, q4 = (cap(dimension) for dimension in range(1, 5))
    r2 = multiplicity * q2
    r3 = multiplicity * q3
    r4 = multiplicity * q4

    total_parents = ceiling(Fraction(residual, r3))
    fixed_parents = ceiling(Fraction(residual, r2 + r3))
    pin_values = {
        order: ceiling(Fraction(residual * comb(Q, order), comb(M, order)))
        for order in range(1, 10)
    }

    result = {
        "A": A,
        "multiplicity": multiplicity,
        "residual": residual,
        "pair_caps": [q1, q2, q3, q4],
        "packet_caps": [r2, r3, r4],
        "total_parent_minimum": total_parents,
        "fixed_dimension_parent_minimum": fixed_parents,
        "intersections": {
            "pair": balanced_floor(fixed_parents, Q, M, 2),
            "triple": balanced_floor(fixed_parents, Q, M, 3),
            "four": balanced_floor(fixed_parents, Q, M, 4),
        },
        "pins": pin_values,
        "one_pin_margin": pin_values[1] - r4,
        "two_pin_margin": pin_values[2] - r2,
        "field_guard": q4 * q4 < P**6,
    }

    assert result == {
        "A": 1_114_501,
        "multiplicity": 982_651,
        "residual": 2_007_222_636_725,
        "pair_caps": [15, 252, 4_023, 63_993],
        "packet_caps": [247_628_052, 3_953_204_973, 62_882_785_443],
        "total_parent_minimum": 508,
        "fixed_dimension_parent_minimum": 478,
        "intersections": {"pair": 1_530, "triple": 53, "four": 2},
        "pins": {
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
        "one_pin_margin": 13_469_327_188,
        "two_pin_margin": 2_656_640_214,
        "field_guard": True,
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = build()
    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(
            "KB_MCA_RANK11_PARENT_SYNC_AUDIT_PASS "
            f"parents={result['total_parent_minimum']} "
            f"fixed={result['fixed_dimension_parent_minimum']} "
            f"pair={result['intersections']['pair']} "
            f"pin_margin={result['one_pin_margin']}"
        )


if __name__ == "__main__":
    main()
