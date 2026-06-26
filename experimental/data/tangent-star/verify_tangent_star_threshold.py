#!/usr/bin/env python3
"""Verify the arithmetic in the tangent-star high-agreement barrier note.

This script is intentionally dependency-free.  It checks the integer gates for
C = RS[F_{17^32}, H, 256] with |H| = 512 under the finite-slope support-wise
MCA convention.
"""

from __future__ import annotations


def tangent_ld(n: int, a: int) -> int:
    if not (0 <= a <= n):
        raise ValueError("agreement a must lie in [0,n]")
    return n - a + 1


def main() -> None:
    n = 512
    k = 256
    q = 17**32
    eps_den = 2**128

    exact_from = (2 * n + k + 2) // 3  # ceil((2n+k)/3)
    assert 3 * exact_from - 2 * n >= k
    assert 3 * (exact_from - 1) - 2 * n < k

    ld_506 = tangent_ld(n, 506)
    ld_507 = tangent_ld(n, 507)
    assert exact_from == 427
    assert ld_506 == 7
    assert ld_507 == 6

    lower_margin = q - 6 * eps_den
    upper_margin = 7 * eps_den - q
    assert lower_margin > 0
    assert upper_margin > 0

    print("tangent-star high-agreement arithmetic check")
    print(f"n={n}, k={k}, q=17^32={q}")
    print(f"exact tangent-star staircase applies for a >= {exact_from}")
    print(f"LD_sw(506) = {ld_506}")
    print(f"LD_sw(507) = {ld_507}")
    print(f"floor(q / 2^128) = {q // eps_den}")
    print(f"q - 6*2^128 = {lower_margin}")
    print(f"7*2^128 - q = {upper_margin}")
    print("finite-slope budget conclusion: agreement 507 safe, agreement 506 unsafe")


if __name__ == "__main__":
    main()
