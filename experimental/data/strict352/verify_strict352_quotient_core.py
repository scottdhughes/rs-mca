#!/usr/bin/env python3
"""
Verify the dyadic quotient-core strict-352 arithmetic for the RS-MCA
experimental note.

Parameters:
  F = GF(17^32), |H| = 512, k = 256.
For each agreement a, the script optimizes over dyadic quotient maps x -> x^c
with c | 512.  It computes the quotient-prefix augmented-list lower bound and
then the quantitative deep-point lower bound for distinct support-wise MCA-bad
slopes.
"""
from math import comb, gcd, log2

p = 17
field_degree = 32
q = p ** field_degree
n = 512
k = 256
EPS_BITS = 128
DIVISORS = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]


def order_mod(a: int, m: int) -> int:
    if m <= 1:
        return 1
    x = 1
    for d in range(1, 10_000):
        x = (x * a) % m
        if x == 1:
            return d
    raise RuntimeError(f"order of {a} modulo {m} not found")


def quotient_floor(a: int, c: int):
    """Return dictionary for quotient c at agreement a, or None if invalid."""
    N = n // c
    m, r = divmod(a, c)
    if r == 0:
        if m > N:
            return None
        total = comb(N, m)
    else:
        if m > N - 1 or r > c:
            return None
        total = comb(N - 1, m)
    d = order_mod(p, N)
    q0 = p ** d
    s = max(0, (a - (k + 1)) // c)
    denom = q0 ** s
    L = (total + denom - 1) // denom
    return {
        "a": a,
        "c": c,
        "N": N,
        "m": m,
        "r": r,
        "d": d,
        "q0": q0,
        "s": s,
        "total": total,
        "denom": denom,
        "L": L,
    }


def deep_point_distinct_slope_floor(L: int) -> int:
    """Ceiling of L(q-n)/(q-n+k(L-1))."""
    numerator = L * (q - n)
    denominator = (q - n) + k * (L - 1)
    return (numerator + denominator - 1) // denominator


def best_row(a: int):
    rows = []
    for c in DIVISORS:
        row = quotient_floor(a, c)
        if row is None:
            continue
        row["M"] = deep_point_distinct_slope_floor(row["L"])
        rows.append(row)
    return max(rows, key=lambda row: (row["M"], row["L"], -row["c"]))


def main() -> None:
    print("Strict-352 dyadic quotient-core arithmetic")
    print(f"q_line = 17^32 = {q}")
    print(f"7*2^128 - q_line = {7 * 2**EPS_BITS - q}")
    print(f"16*2^128 - q_line = {16 * 2**EPS_BITS - q}")
    print()
    print("quotient degrees:")
    for c in DIVISORS:
        N = n // c
        print(f"  c={c:3d}, N={N:3d}, ord_N(17)={order_mod(p, N):2d}, q0=17^{order_mod(p, N)}")
    print()
    print("a,c,N,d,m,r,s,total,denom,L,M,log2_M")
    last = None
    best_rows = []
    for a in range(264, 354):
        row = best_row(a)
        best_rows.append(row)
        print(
            f"{a},{row['c']},{row['N']},{row['d']},{row['m']},{row['r']},"
            f"{row['s']},{row['total']},{row['denom']},{row['L']},{row['M']},"
            f"{log2(row['M']):.6f}"
        )
        if row["M"] >= 7:
            last = a
    print()
    g = gcd(n - last, n)
    print(f"last agreement in this guaranteed floor with M >= 7: {last}")
    print(f"corresponding delta = 1 - {last}/512 = {(n-last)//g}/{n//g}")
    print(f"best row at {last}: {best_row(last)}")
    print(f"best row at {last + 1}: {best_row(last + 1)}")


if __name__ == "__main__":
    main()
