#!/usr/bin/env python3
"""CAP25 v13 row-sharp Q: finite moment-order floor checker.

Verifies the exact average ceilings using one large integer binomial and
nearby recurrence updates. Logarithmic moment thresholds use libm logs; the
ceiling values are stable at the displayed precision.
"""
from __future__ import annotations

from math import comb, lgamma, log, log2, ceil

N = 2**21
K_LIST = 2**20
K_MCA = 2**20 + 1
ROWS = [
    # name, p, extension/list exponent s, lambda target, a_plus, K, orbit_len_for_table
    ("KoalaBear MCA", 2**31 - 2**24 + 1, 6, 128, 1116048, K_MCA, N),
    ("KoalaBear list", 2**31 - 2**24 + 1, 6, 128, 1116047, K_LIST, N),
    # Mersenne line-round rows have no multiplicative twist orbit on the x-domain;
    # L=1 is therefore the theorem-facing safe value.
    ("Mersenne-31 MCA", 2**31 - 1, 4, 100, 1116024, K_MCA, 1),
    ("Mersenne-31 list", 2**31 - 1, 4, 100, 1116023, K_LIST, 1),
]


def log2_binom(n: int, k: int) -> float:
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)) / log(2.0)


def ceil_div(a: int, b: int) -> int:
    return (a + b - 1) // b


def nearby_binoms(n: int, ks: list[int]) -> dict[int, int]:
    """Return C(n,k) for nearby k values using one comb at max(ks)."""
    kmax = max(ks)
    vals = {kmax: comb(n, kmax)}
    c = vals[kmax]
    for k in range(kmax, min(ks), -1):
        # C(n,k-1) = C(n,k) * k / (n-k+1)
        c = (c * k) // (n - k + 1)
        vals[k - 1] = c
    return vals


def main() -> None:
    binoms = nearby_binoms(N, [row[4] for row in ROWS])
    print("row,w,ceil_average,Bstar,Delta_bits,r_full,L_orbit,r_orbit")
    for name, p, s, lam, a_plus, K, L in ROWS:
        w = a_plus - K
        C = binoms[a_plus]
        den = pow(p, w)
        ceil_avg = ceil_div(C, den)
        Bstar = pow(p, s) // pow(2, lam)
        delta = log2(Bstar) + w * log2(p) - log2_binom(N, a_plus)
        numerator_full = w * log2(p)
        r_full = ceil(numerator_full / delta)
        numerator_orbit = numerator_full - log2(L)
        r_orbit = ceil(numerator_orbit / delta)
        print(f"{name},{w},{ceil_avg},{Bstar},{delta:.12f},{r_full},{L},{r_orbit}")

    print("\nMersenne-31 list: residual mass fraction theta needed for selected moment orders (no orbit).")
    name, p, s, lam, a_plus, K, L = ROWS[-1]
    w = a_plus - K
    Bstar = pow(p, s) // pow(2, lam)
    delta = log2(Bstar) + w * log2(p) - log2_binom(N, a_plus)
    beta_w = w * log2(p)
    for r in [2, 3, 4, 10, 100, 1000, 10000, 100000, 200000, 500000, 680397]:
        log2_theta = delta - beta_w / r
        print(f"r={r}: log2(theta) <= {log2_theta:.12f}")


if __name__ == "__main__":
    main()
