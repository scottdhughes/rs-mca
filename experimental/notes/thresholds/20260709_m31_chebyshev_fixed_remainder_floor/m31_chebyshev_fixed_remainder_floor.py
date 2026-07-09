#!/usr/bin/env python3
"""Exact replay for the CAP25 v13 M31 Chebyshev fixed-remainder floor.

This script checks the finite arithmetic used in the accompanying experimental
note. It is not a row-sharp Q proof.
"""

from math import comb, log2


def ceil_div(num: int, den: int) -> int:
    return (num + den - 1) // den


P = 2**31 - 1
N = 2**21
K = 2**20
A_PLUS_LIST = 1_116_023
W_LIST = A_PLUS_LIST - K
BSTAR = 2**24 - 1
AVG_CEIL = 1_993_678


def fixed_remainder_floor(c: int) -> dict[str, int]:
    if N % c:
        raise ValueError(f"c={c} does not divide n={N}")
    f = A_PLUS_LIST // c
    r = A_PLUS_LIST % c
    t = W_LIST // c
    quotient_points = N // c - (1 if r else 0)
    floor = ceil_div(comb(quotient_points, f), P**t)
    return {
        "c": c,
        "quotient_points": quotient_points,
        "f": f,
        "r": r,
        "t": t,
        "floor": floor,
    }


rows = [fixed_remainder_floor(2**j) for j in range(21)]
best = max(rows, key=lambda row: row["floor"])
dyadic_sum = sum(row["floor"] for row in rows)
m31_mca_watch = ceil_div(comb(1024, 545), P**32)

assert P == 2_147_483_647
assert W_LIST == 67_447
assert BSTAR == 16_777_215
assert AVG_CEIL == 1_993_678

assert best == {
    "c": 2048,
    "quotient_points": 1023,
    "f": 544,
    "r": 1911,
    "t": 32,
    "floor": 6_796_405,
}
assert dyadic_sum == 16_548_620
assert BSTAR - best["floor"] == 9_980_810
assert m31_mca_watch == 12_769_758
assert BSTAR - m31_mca_watch == 4_007_457

print("CAP25 v13 M31 Chebyshev fixed-remainder floor")
print(f"p={P}")
print(f"n={N}")
print(f"k={K}")
print(f"a_plus_list={A_PLUS_LIST}")
print(f"w_list={W_LIST}")
print(f"Bstar={BSTAR}")
print(f"avg_ceil={AVG_CEIL}")
print(f"log2(Bstar/avg_ceil)={log2(BSTAR / AVG_CEIL):.15f}")
print()
print("dyadic fixed-remainder floors, c=2^j, 0<=j<=20")
for row in rows:
    print(
        "c={c:7d} quotient_points={quotient_points:7d} "
        "f={f:7d} r={r:6d} t={t:5d} floor={floor}".format(**row)
    )
print()
print(f"best_c={best['c']}")
print(f"best_floor={best['floor']}")
print(f"Bstar_minus_best={BSTAR - best['floor']}")
print(f"log2(Bstar/best_floor)={log2(BSTAR / best['floor']):.15f}")
print(
    "log2((Bstar-best_floor)/avg_ceil)="
    f"{log2((BSTAR - best['floor']) / AVG_CEIL):.15f}"
)
print(f"dyadic_sum={dyadic_sum}")
print(f"Bstar_minus_dyadic_sum={BSTAR - dyadic_sum}")
print(f"m31_mca_c2048_watch={m31_mca_watch}")
print(f"Bstar_minus_m31_mca_watch={BSTAR - m31_mca_watch}")
