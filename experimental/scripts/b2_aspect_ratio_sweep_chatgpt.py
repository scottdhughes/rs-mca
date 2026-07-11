#!/usr/bin/env python3
"""
Exact fixed-weight syndrome-fiber sweep for cyclic Reed–Solomon/MDS checks.

For each w = 1,...,max_w, this enumerates all m-subsets S of the n-th
roots of unity in F_p and counts fibers of

    Phi_w(S) = (sum_{a in S} a^j)_{j=1}^w.

It then evaluates the exact centered quantity

    J_v = p^n (N_v - binom(n,m)/p^w)
        = p^(n-w) (p^w N_v - binom(n,m)),

including unattained syndromes N_v = 0, and reports its largest
base-p exponent.  This directly tests the gamma = (w+1)/n dependence.

Default toy: p=193, n=32, m=4, max_w=8 (35,960 subsets).
"""

from __future__ import annotations

import argparse
import itertools
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


def distinct_prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def primitive_root_mod_prime(p: int) -> int:
    """Return a primitive root modulo an odd prime p."""
    if p <= 2:
        raise ValueError("p must be an odd prime")
    factors = distinct_prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // q, p) != 1 for q in factors):
            return candidate
    raise RuntimeError("No primitive root found; check that p is prime.")


def log_base_int(value: int, base: int) -> float:
    if value <= 0:
        raise ValueError("value must be positive")
    return math.log(value) / math.log(base)


@dataclass(frozen=True)
class SweepRow:
    w: int
    c: int
    gamma: float
    attained: int
    total_syndromes: int
    n_max: int
    mean: Fraction
    max_discrepancy: Fraction
    rounding_lower_bound: Fraction
    alpha_max: float
    pointwise_floor: float


def enumerate_prefix_fibers(
    p: int,
    n: int,
    m: int,
    max_w: int,
) -> list[Counter[tuple[int, ...]]]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} must divide p-1={p-1}")
    if not (0 <= m <= n):
        raise ValueError("m must satisfy 0 <= m <= n")
    if not (1 <= max_w < n):
        raise ValueError("max_w must satisfy 1 <= max_w < n")

    generator = primitive_root_mod_prime(p)
    omega = pow(generator, (p - 1) // n, p)
    roots = [pow(omega, i, p) for i in range(n)]
    if len(set(roots)) != n or pow(omega, n, p) != 1:
        raise RuntimeError("Failed to construct n distinct n-th roots of unity.")

    # columns[i][j-1] = roots[i]^j for j=1,...,max_w
    columns = [
        [pow(root, degree, p) for degree in range(1, max_w + 1)]
        for root in roots
    ]
    counters: list[Counter[tuple[int, ...]]] = [
        Counter() for _ in range(max_w)
    ]

    for subset in itertools.combinations(range(n), m):
        syndrome = [0] * max_w
        for index in subset:
            column = columns[index]
            for j in range(max_w):
                syndrome[j] = (syndrome[j] + column[j]) % p
        syndrome_tuple = tuple(syndrome)
        for w in range(1, max_w + 1):
            counters[w - 1][syndrome_tuple[:w]] += 1

    return counters


def build_rows(
    p: int,
    n: int,
    m: int,
    counters: Iterable[Counter[tuple[int, ...]]],
) -> list[SweepRow]:
    domain_size = math.comb(n, m)
    rows: list[SweepRow] = []

    for w, counter in enumerate(counters, start=1):
        syndrome_count = p**w
        mean = Fraction(domain_size, syndrome_count)

        # |N_v - mean| = |p^w N_v - D| / p^w.
        discrepancy_numerators = [
            abs(syndrome_count * multiplicity - domain_size)
            for multiplicity in counter.values()
        ]
        if len(counter) < syndrome_count:
            # At least one unattained syndrome has N_v = 0.
            discrepancy_numerators.append(domain_size)

        max_numerator = max(discrepancy_numerators)
        max_discrepancy = Fraction(max_numerator, syndrome_count)

        quotient, remainder = divmod(domain_size, syndrome_count)
        del quotient
        if remainder == 0:
            rounding_lower_bound = Fraction(0, 1)
        else:
            rounding_lower_bound = Fraction(
                max(remainder, syndrome_count - remainder),
                syndrome_count,
            )

        # J_max = p^(n-w) * max_v |p^w N_v - D|.
        log_p_j_max = (n - w) + log_base_int(max_numerator, p)
        alpha_max = log_p_j_max / n

        rows.append(
            SweepRow(
                w=w,
                c=w + 1,
                gamma=(w + 1) / n,
                attained=len(counter),
                total_syndromes=syndrome_count,
                n_max=max(counter.values()),
                mean=mean,
                max_discrepancy=max_discrepancy,
                rounding_lower_bound=rounding_lower_bound,
                alpha_max=alpha_max,
                pointwise_floor=(n - w) / n,
            )
        )

    return rows


def format_float_fraction(value: Fraction, digits: int = 6) -> str:
    return f"{float(value):.{digits}g}"


def print_rows(p: int, n: int, m: int, rows: list[SweepRow]) -> None:
    print(f"p={p}, n={n}, m={m}, domain=binom(n,m)={math.comb(n,m)}")
    print(
        " w   c    gamma     attained       Nmax        mean"
        "      max|N-mu|   alpha_max  floor"
    )
    for row in rows:
        print(
            f"{row.w:2d}  {row.c:2d}  {row.gamma:8.5f}  "
            f"{row.attained:11d}  {row.n_max:9d}  "
            f"{format_float_fraction(row.mean, 5):>10}  "
            f"{format_float_fraction(row.max_discrepancy, 5):>12}  "
            f"{row.alpha_max:9.6f}  {row.pointwise_floor:6.4f}"
        )

    print()
    print("Definitions:")
    print("  alpha_max = log_p(max_v |p^n (N_v-mu)|) / n")
    print("  floor     = (n-w)/n, from the exact p-adic valuation")
    print("              v_p(p^n(N_v-mu)) = n-w when p > n.")
    print("  The max over v includes unattained syndromes N_v=0.")


def print_deployment_check() -> None:
    p = 2**31 - 2**24 + 1
    n = 2**21
    w = 67_471
    c = w + 1
    d = n - c
    gamma = c / n

    pointwise_c_min = 1 / (2 * gamma) - 1
    uniform_c_min = 1 / (2 * gamma)
    log_p_2 = math.log(2) / math.log(p)
    bit_constraint_rate = c * math.log2(p) / n

    print()
    print("Deployment arithmetic check")
    print("---------------------------")
    print(f"p = {p}")
    print(f"n = {n}, w = {w}, c = {c}, d = {d}")
    print(f"gamma = c/n = {gamma:.15f}")
    print(f"log_p(2) = {log_p_2:.15f}")
    print(f"c log_2(p) / n = {bit_constraint_rate:.15f}")
    print(f"pointwise C must be >= {pointwise_c_min:.12f}")
    print(f"uniform-in-v C must be >= {uniform_c_min:.12f}")
    print(
        "Every fixed-weight centered value obeys "
        "|p^n(N_v-mu)| >= p^(n-w) = p^(d+1), because p>n."
    )
    print(
        "For the maximum over syndromes, "
        "max_v |p^n(N_v-mu)| >= p^n/2."
    )

    # Global all-subset average, useful as a quick independent check.
    modulus = p**c
    quotient, remainder = divmod(1 << n, modulus)
    del quotient
    theta = remainder / modulus
    print()
    print("All-subset (augmented c-check) average:")
    print(f"  fractional part of 2^n/p^c = {theta:.15f}")
    print(
        "  hence max_beta |N_beta-2^n/p^c| >= "
        f"{max(theta, 1-theta):.15f}"
    )
    print(f"  log_2(2^n/p^c) = {n - c * math.log2(p):.12f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=193)
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--m", type=int, default=4)
    parser.add_argument("--max-w", type=int, default=8)
    parser.add_argument(
        "--deployment-check",
        action="store_true",
        help="also print the exact KoalaBear deployment arithmetic barrier",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    counters = enumerate_prefix_fibers(args.p, args.n, args.m, args.max_w)
    rows = build_rows(args.p, args.n, args.m, counters)
    print_rows(args.p, args.n, args.m, rows)
    if args.deployment_check:
        print_deployment_check()


if __name__ == "__main__":
    main()
