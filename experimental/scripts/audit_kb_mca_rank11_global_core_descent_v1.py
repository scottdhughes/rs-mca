#!/usr/bin/env python3
"""Separate exact product/recurrence audit for the rank-eleven payment."""

from __future__ import annotations

import json
from fractions import Fraction
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank11-global-core-descent-v1/result.json"

R = 1_048_576
D = 67_472
K0 = 1_048_576
BUDGET = 274_980_728_111_395_087
NEAR = 134_944


def ceil_fraction(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def fall_fraction(x: int, length: int) -> int:
    value = 1
    for index in range(length):
        value *= x - index
    return value


def rise_fraction(x: int, length: int) -> int:
    value = 1
    for index in range(length):
        value *= x + index
    return value


def resource(rank: int, dimension: int) -> int:
    first = Fraction(
        fall_fraction(R + dimension, rank + 1),
        (D + dimension) * rise_fraction(D + 1, rank - 1),
    )
    second = Fraction(
        fall_fraction(R + rank, rank + 1),
        rise_fraction(D + 1, rank),
    )
    value = max(first, second)
    return value.numerator // value.denominator


def incidence(load: int, rank: int, dimension: int) -> int:
    return ceil_fraction(
        Fraction(load * (D + dimension) - resource(rank, dimension), R + dimension)
    )


def reconstruct_loads() -> dict[int, int]:
    values = {10: BUDGET - NEAR + 1}
    for rank in range(10, 1, -1):
        values[rank - 1] = incidence(values[rank], rank, rank)
    return values


def verify_monotonicity(loads: dict[int, int]) -> int:
    checked = 0
    for rank in range(2, 11):
        tail = rise_fraction(D + 1, rank - 1)
        fixed = Fraction(
            fall_fraction(R + rank, rank + 1),
            rise_fraction(D + 1, rank),
        )
        fixed_floor = fixed.numerator // fixed.denominator
        dimension = rank
        moving_numerator = fall_fraction(R + dimension, rank + 1)
        prior = None
        first = None
        while dimension <= K0:
            moving_floor = moving_numerator // ((D + dimension) * tail)
            res = max(moving_floor, fixed_floor)
            value = -(-(loads[rank] * (D + dimension) - res) // (R + dimension))
            if prior is not None and value < prior:
                raise AssertionError((rank, dimension, prior, value))
            if first is None:
                first = value
            prior = value
            checked += 1
            if dimension < K0:
                moving_numerator = (
                    moving_numerator * (R + dimension + 1)
                    // (R + dimension - rank)
                )
            dimension += 1
        assert first == loads[rank - 1]
    return checked


def endpoint_bound() -> tuple[int, tuple[int, int, int, int, Fraction], int]:
    n = R + 1
    m = D + 1
    q = (m - 1) // 2
    low = comb(n, 2) // (q * (q + 1))
    best: tuple[int, int, int, int, Fraction] | None = None
    for classes in range(1, n // (q + 1) + 1):
        for unit in range(classes + 1):
            large = classes - unit
            outside = n - classes * m + unit + large * q
            if outside < 0:
                continue
            value = Fraction(classes * (classes - 1), 1) + outside * (
                Fraction(unit, 1) + Fraction(large, q)
            )
            row = (classes, unit, large, outside, value)
            if best is None or row[-1] > best[-1]:
                best = row
    assert best is not None
    high = best[-1].numerator // best[-1].denominator
    assert best[:4] == (8, 8, 0, 508_801)
    assert high == 4_070_464
    assert low == 483
    return low + high, best, low


def endpoint_reduction_controls() -> int:
    """Check the one-variable endpoint reduction on a finite rational grid."""
    checked = 0
    for c0 in range(-8, 9):
        for qnum in range(1, 10):
            for upper in range(2, 12):
                values = [
                    Fraction(c0 + a, 1) * (Fraction(qnum, 7) + Fraction(1, a))
                    for a in range(1, upper + 1)
                    if c0 + a >= 0
                ]
                if not values:
                    continue
                assert max(values) == max(values[0], values[-1])
                checked += 1
    return checked


def main() -> None:
    frozen = json.loads(RESULT.read_text())
    loads = reconstruct_loads()
    expected = {int(key): value for key, value in frozen["descent_loads"].items()}
    assert loads == expected
    cells = verify_monotonicity(loads)
    cap, extremizer, low = endpoint_bound()
    assert cap == frozen["final_contradiction"]["rank_one_upper_bound"]
    assert loads[1] - cap == frozen["final_contradiction"]["slack"]
    controls = endpoint_reduction_controls()
    print(
        "KB_MCA_RANK11_GLOBAL_CORE_AUDIT_PASS "
        f"cells={cells} endpoint_cap={cap} low={low} "
        f"extremizer={extremizer[:4]} endpoint_controls={controls}"
    )


if __name__ == "__main__":
    main()
