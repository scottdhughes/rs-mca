#!/usr/bin/env python3
"""Independent exact replay of the rank-eleven factor synchronization packet."""

from __future__ import annotations

import argparse
import json
from math import prod


def choose(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    value = 1
    for j in range(1, k + 1):
        value = value * (n - k + j) // j
    return value


def falling(n: int, k: int) -> int:
    return prod(range(n - k + 1, n + 1))


def up(a: int, b: int) -> int:
    return (a + b - 1) // b


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    n = 2_097_152
    K = 1_048_576
    m = 1_116_048
    w = 67_472
    tau = 1_549
    h = 42_447
    budget = 274_980_728_111_395_087
    theta = 106_618_568_137_036_225_644

    A = m - tau
    overlap = 2 * A - n
    q = h + 1
    multiplicity = n - A

    m2 = choose(n - K + 2, 2) // choose(w - tau + 2, 2)
    m3 = choose(n - K + 3, 3) // choose(w - tau + 3, 3)
    r2 = m2 * multiplicity
    r3 = m3 * multiplicity

    n1 = falling(m, 9) // (overlap - h) ** 9
    n2 = falling(m, 8) // (overlap - h) ** 8
    total = (
        134_944
        + theta // (tau + 1)
        + multiplicity
        + n1 * 8_147_918
        + n2 * r2
    )
    load = budget + 1 - total
    parents = up(load, r3)
    incidence = parents * q
    low, remainder = divmod(incidence, m)

    intersections = {}
    for order in range(2, 6):
        numerator = (
            (m - remainder) * choose(low, order)
            + remainder * choose(low + 1, order)
        )
        intersections[str(order)] = up(numerator, choose(parents, order))

    weighted = {
        str(order): up(load * choose(q, order), choose(m, order))
        for order in range(1, 11)
    }

    result = {
        "A": A,
        "overlap": overlap,
        "q": q,
        "m2": m2,
        "m3": m3,
        "r2": r2,
        "r3": r3,
        "transverse_total": total,
        "load": load,
        "parents": parents,
        "incidence": incidence,
        "balanced": [low, remainder],
        "intersections": intersections,
        "weighted": weighted,
    }

    assert result == {
        "A": 1114499,
        "overlap": 131846,
        "q": 42448,
        "m2": 252,
        "m3": 4023,
        "r2": 247628556,
        "r3": 3953213019,
        "transverse_total": 274871033266908609,
        "load": 109694844486479,
        "parents": 27749,
        "incidence": 1177889552,
        "balanced": [1055, 458912],
        "intersections": {"2": 1614, "3": 62, "4": 3, "5": 1},
        "weighted": {
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
    }

    if args.json:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    else:
        print(
            "KB_MCA_RANK11_FACTOR_SYNC_AUDIT_PASS "
            f"parents={parents} pair={intersections['2']} "
            f"triple={intersections['3']} weighted4={weighted['4']}"
        )


if __name__ == "__main__":
    main()
