#!/usr/bin/env python3
"""Exhaustive toy scan for the centered Hankel--Gauss rank conjecture.

For a prime p and n | (p-1), this enumerates all fibers with fixed weight m
and first w moments, computes the quadratic-delta Fourier sums G_v(lambda),
stratifies by rank(A_lambda), and tests

    R(v,r) = |T_r(v)| / p^(n + (r_* - r)/2),

where T_r is the syndrome-centered rank-r sum and
r_* = n - 2(w+1).

The deployment-sufficient conjecture in the accompanying note is R(v,r) <= p^2.
The computation is exponential in n (roughly p^n), so use only tiny examples.
The multidimensional FFT is floating point; exact zeroes appear at roundoff scale.

Examples:
    python hankel_gauss_dense_rank_scan.py
    python hankel_gauss_dense_rank_scan.py --p 11 --n 5 --w 1 --m 2
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter

import numpy as np


def primitive_root(p: int) -> int:
    """Return a primitive root modulo an odd prime p."""
    factors: list[int] = []
    x = p - 1
    q = 2
    while q * q <= x:
        if x % q == 0:
            factors.append(q)
            while x % q == 0:
                x //= q
        q += 1
    if x > 1:
        factors.append(x)

    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError("No primitive root found")


def matrix_rank_mod(M: np.ndarray, p: int) -> int:
    """Row-reduction rank over F_p."""
    A = np.array(M, dtype=np.int64) % p
    rows, cols = A.shape
    rank = 0
    for col in range(cols):
        pivot = next((i for i in range(rank, rows) if A[i, col] % p), None)
        if pivot is None:
            continue
        if pivot != rank:
            A[[rank, pivot]] = A[[pivot, rank]]
        A[rank] = (A[rank] * pow(int(A[rank, col]), -1, p)) % p
        for i in range(rows):
            if i != rank and A[i, col] % p:
                A[i] = (A[i] - A[i, col] * A[rank]) % p
        rank += 1
        if rank == rows:
            break
    return rank


def scan(p: int, n: int, w: int, m: int) -> None:
    if p < 3 or any(p % q == 0 for q in range(2, int(p**0.5) + 1)):
        raise ValueError("p must be an odd prime")
    if (p - 1) % n != 0:
        raise ValueError("n must divide p-1")
    if not (0 <= w < n):
        raise ValueError("Need 0 <= w < n")
    if not (0 <= m <= n):
        raise ValueError("Need 0 <= m <= n")

    cdim = w + 1
    d = n - cdim
    r_star = 2 * d - n
    if d <= 0:
        raise ValueError("Need d=n-w-1 > 0 for this scan")

    root = pow(primitive_root(p), (p - 1) // n, p)
    H = [pow(root, i, p) for i in range(n)]
    free = list(range(1, d + 1))

    # Evaluation matrix for free coefficients; P[a,i] = a^i.
    P = np.array([[pow(a, i, p) for i in free] for a in H], dtype=np.int64)
    inv_n = pow(n, -1, p)

    coeffs = np.array(list(itertools.product(range(p), repeat=d)), dtype=np.int64)
    lambdas = np.array(list(itertools.product(range(p), repeat=n)), dtype=np.int64)
    supports = np.count_nonzero(lambdas, axis=1)

    # Rank A_lambda, A_ij = sum_a lambda_a a^(i+j).
    ranks = np.empty(len(lambdas), dtype=np.int64)
    for idx, lam in enumerate(lambdas):
        A = (P.astype(np.int64).T @ (lam.astype(np.int64)[:, None] * P)) % p
        ranks[idx] = matrix_rank_mod(A, p)

    syndromes = list(itertools.product(range(p), repeat=w))
    G_all = np.empty((len(syndromes), len(lambdas)), dtype=np.complex128)
    fiber_sizes: list[int] = []

    # np.fft.fftn uses the negative additive-character sign; conjugation switches it.
    for vi, v in enumerate(syndromes):
        fixed = np.zeros(n, dtype=np.int64)
        fixed[0] = (m * inv_n) % p
        for j, vj in enumerate(v, start=1):
            fixed[n - j] = (vj * inv_n) % p

        values = (coeffs.astype(np.int64) @ P.astype(np.int64).T + fixed @ np.array(
            [[pow(a, r, p) for a in H] for r in range(n)], dtype=np.int64
        )) % p

        fiber_sizes.append(int(np.sum(np.all((values == 0) | (values == 1), axis=1))))

        qvec = (values * values - values) % p
        linear_index = np.zeros(len(qvec), dtype=np.int64)
        for j in range(n):
            linear_index = linear_index * p + qvec[:, j]
        hist = np.bincount(linear_index, minlength=p**n).reshape((p,) * n)
        G_all[vi] = np.conjugate(np.fft.fftn(hist)).ravel()

    G_bar = G_all.mean(axis=0)
    centered = G_all - G_bar

    low_error = 0.0
    for t in range(min(d, n) + 1):
        mask = supports == t
        if np.any(mask):
            low_error = max(low_error, float(np.max(np.abs(centered[:, mask].sum(axis=1)))))

    max_ratio = 0.0
    argmax: tuple[tuple[int, ...], int, int] | None = None
    for vi, v in enumerate(syndromes):
        for r in range(max(0, r_star), d + 1):
            mask = ranks == r
            if not np.any(mask):
                continue
            T_r = centered[vi, mask].sum()
            scale = p ** (n + (r_star - r) / 2)
            ratio = abs(T_r) / scale
            if ratio > max_ratio:
                max_ratio = float(ratio)
                argmax = (v, fiber_sizes[vi], r)

    print("parameters (p,n,w,m) =", (p, n, w, m))
    print("H =", H)
    print("fiber sizes =", fiber_sizes)
    print("average fiber =", sum(fiber_sizes) / len(fiber_sizes))
    print("rank distribution =", Counter(int(x) for x in ranks))
    print("d =", d, "r_* =", r_star)
    print("max centered support<=d error =", low_error)
    print("max normalized dense-rank ratio =", max_ratio)
    print("attained at (v,N(v),rank) =", argmax)
    print("comparison n^2 =", n * n)
    print("deployment-style comparison p^2 =", p * p)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=7)
    parser.add_argument("--n", type=int, default=6)
    parser.add_argument("--w", type=int, default=1)
    parser.add_argument("--m", type=int, default=3)
    args = parser.parse_args()
    scan(args.p, args.n, args.w, args.m)


if __name__ == "__main__":
    main()
