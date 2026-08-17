#!/usr/bin/env python3
"""Independent arithmetic and finite-control audit of the rank-12 four-block payment."""
from __future__ import annotations

import json
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank12-four-block-owner-payment-v1/result.json"
R, D, T = 1_048_576, 67_472, 981_104
LOAD, LINE = 5_170_912, 4_070_947


def ceilq(a: int, b: int) -> int:
    return -(-a // b)


def theta(K: int) -> int:
    a = (R + K) * (R + K - 1) * (R + K - 2) // ((D + K) * (D + 1))
    b = (R + 2) * (R + 1) * R // ((D + 1) * (D + 2))
    return max(a, b)


def incidence(K: int) -> int:
    return ceilq(LOAD * (D + K) - theta(K), R + K)


@lru_cache(maxsize=None)
def line_cap(k: int) -> int:
    n, m = R + k, D + k
    q, a = m // 2, m - m // 2 - 1
    low = comb(n, 2) // (q * (m - q))
    best_num, best_den = -1, 1
    for h in range(1, n // (q + 1) + 1):
        C = n - h * m + h * a
        b = a - 1
        candidates = {0, h}
        if b:
            v = (C - h) // (2 * b)
            candidates.update((v - 1, v, v + 1, v + 2, C // b, C // b + 1))
        for p in candidates:
            if p < 0 or p > h:
                continue
            W = n - h * m + p + (h - p) * a
            if W < 0:
                continue
            num = h * (h - 1) * a + W * (p * a + h - p)
            if num * best_den > best_num * a:
                best_num, best_den = num, a
    return low + best_num // best_den


def pointer_at(K: int, prior: int | None = None) -> int:
    target = incidence(K)
    if prior is None:
        lo, hi, ans = 1, 100_000, 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if line_cap(mid) >= target:
                ans, lo = mid, mid + 1
            else:
                hi = mid - 1
        return ans
    p = prior
    while line_cap(p) < target:
        p -= 1
    return p


def envelope(k: int, rho: int) -> Fraction:
    vals = [Fraction(rho + 1, 1)]
    vals.append(Fraction((D + 1 + rho) * (D + rho), 2 * D))
    vals.append(Fraction((k - 1 + rho) * (k - 2 + rho), 2 * (k - 2)))
    vals.append(Fraction((k + rho) * (k - 1 + rho), 2 * (k - 1)))
    vals.append(Fraction((k + D + rho) * (k + D - 1 + rho), 2 * (k - 1) * (D + 1)))
    return max(vals)


def ray_exact(K: int, r: int) -> int:
    vals = [r + 1]
    for M in (D + 1, K - 1, K, K + D):
        B = M - 1 if M <= K - 1 else (K - 1) * (M - K + 1)
        vals.append(comb(M + r, 2) // B)
    return max(vals)


def exceptional(K: int, c: int) -> int:
    m = K + D
    r = T - c
    if r < 0:
        return 0
    delta, eta = 3 * r - m, 2 * r - m
    if delta < 0:
        return ray_exact(K, r)
    if eta < 0:
        return 4 + max(0, 2 * delta - r + 1)
    assert 4 * eta < r
    rays = envelope(K - r, 2 * eta) + envelope(K - r + 2 * eta, 0)
    return r + 4 * eta + 9 + rays.numerator // rays.denominator


def determinant_control() -> int:
    count = 0
    for p in (7, 11):
        for slopes in combinations(range(p), 4):
            for missing in range(4):
                idx = [i for i in range(4) if i != missing]
                s = [sum(slopes[j] for j in range(4) if j != i) % p for i in idx]
                u = []
                for i in idx:
                    o = [slopes[j] for j in range(4) if j != i]
                    u.append(sum(o[a] * o[b] for a in range(3) for b in range(a + 1, 3)) % p)
                coeff = ((s[1] - s[2]) * u[0] + (s[2] - s[0]) * u[1] + (s[0] - s[1]) * u[2]) % p
                if coeff == 0:
                    raise AssertionError("triplet coefficient")
                count += 1
    return count


def main() -> None:
    result = json.loads(RESULT.read_text())
    expected = {
        662_479: (75_757, 586_722, 1_099_983, -18),
        662_480: (75_757, 586_723, 1_099_960, 5),
        680_378: (73_200, 607_178, 680_401, 419_564),
        680_379: (73_200, 607_179, 373_928, 726_037),
        765_277: (61_756, 703_521, 4, 1_099_961),
        765_278: (61_756, 703_522, 882_311, 217_654),
        858_618: (52_277, 806_341, 621_857, 478_108),
        1_048_576: (40_231, 1_008_345, 0, 1_099_965),
    }

    p = pointer_at(662_479)
    max_cap, max_K = -1, None
    checked = 0
    for K in range(662_479, 1_048_577):
        if K != 662_479:
            p = pointer_at(K, p)
        c = K - p
        z = exceptional(K, c)
        slack = LOAD - LINE - z
        if z > max_cap and K >= 662_480:
            max_cap, max_K = z, K
        if K in expected:
            got = (p, c, z, slack)
            if got != expected[K]:
                raise AssertionError((K, got, expected[K]))
        if K >= 662_480 and slack <= 0:
            raise AssertionError((K, slack))
        checked += 1

    if (max_cap, max_K) != (1_099_960, 662_480):
        raise AssertionError("maximum")
    if result["first_paid_cell"]["slack"] != 5:
        raise AssertionError("certificate")

    # Independent exact first-cell ray arithmetic.
    r, eta, K = 394_381, 58_810, 662_480
    f1, f2 = envelope(K - r, 2 * eta), envelope(K - r + 2 * eta, 0)
    if (f1, f2, (f1 + f2).numerator // (f1 + f2).denominator) != (
        Fraction(24_796_460_207, 89_366), Fraction(385_719, 2), 470_330
    ):
        raise AssertionError("first ray")

    triplets = determinant_control()
    print(
        "KB_MCA_RANK12_FOUR_BLOCK_AUDIT_PASS "
        f"ambient={checked} triplets={triplets} max={max_cap} first={max_K}"
    )


if __name__ == "__main__":
    main()
