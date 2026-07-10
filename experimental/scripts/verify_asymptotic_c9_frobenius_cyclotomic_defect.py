#!/usr/bin/env python3
"""Exact checks for the Frobenius cyclotomic-defect C9 note."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations


def multiplicative_order(a: int, modulus: int) -> int:
    if modulus == 1:
        return 1
    x = 1
    for order in range(1, modulus + 1):
        x = (x * a) % modulus
        if x == 1:
            return order
    raise AssertionError("order not found")


def v2(value: int) -> int:
    assert value > 0
    out = 0
    while value % 2 == 0:
        value //= 2
        out += 1
    return out


def orbit(n: int, p: int, start: int) -> set[int]:
    out: set[int] = set()
    value = start % n
    while value not in out:
        out.add(value)
        value = (p * value) % n
    return out


def ceil_log2_ratio(numerator: int, denominator: int) -> int:
    """Return ceil(log2(numerator/denominator)) using integer arithmetic."""
    assert numerator > 0 and denominator > 0
    exponent = 0
    value = denominator
    while value < numerator:
        value <<= 1
        exponent += 1
    return exponent


def verify_orbit_structure(max_s: int) -> int:
    checks = 0
    for s in range(3, max_s + 1):
        n = 1 << s
        assert multiplicative_order(5, n) == 1 << (s - 2)
        checks += 1
        for k in range(1, n):
            valuation = v2(k)
            if valuation > s - 2:
                continue
            residue = k % (1 << (valuation + 2))
            expected = {
                x
                for x in range(n)
                if x != 0
                and v2(x) == valuation
                and x % (1 << (valuation + 2)) == residue
            }
            assert orbit(n, 5, k) == expected
            checks += 1
    return checks


def verify_all_intervals(max_s: int) -> int:
    checks = 0
    for s in range(1, max_s + 1):
        n = 1 << s
        orbit_masks = []
        for k in range(n):
            mask = 0
            for value in orbit(n, 5, k):
                mask |= 1 << value
            orbit_masks.append(mask)

        for start in range(n):
            covered = 0
            for length in range(1, n + 1):
                covered |= orbit_masks[(start + length - 1) % n]
                defect = n - covered.bit_count()
                j = ceil_log2_ratio(4 * n, length)
                bound = 1 << (j - 1)
                assert defect <= bound, (
                    "dyadic defect failure",
                    n,
                    start,
                    length,
                    defect,
                    bound,
                )
                checks += 1
    return checks


# F_25 = F_5[u]/(u^2-3), encoded as a+5b.
def f25_add(x: int, y: int) -> int:
    return ((x % 5 + y % 5) % 5) + 5 * ((x // 5 + y // 5) % 5)


def f25_mul(x: int, y: int) -> int:
    a, b = x % 5, x // 5
    c, d = y % 5, y // 5
    return ((a * c + 3 * b * d) % 5) + 5 * ((a * d + b * c) % 5)


def f25_pow(value: int, exponent: int) -> int:
    out = 1
    while exponent:
        if exponent & 1:
            out = f25_mul(out, value)
        value = f25_mul(value, value)
        exponent >>= 1
    return out


def f25_order(value: int) -> int:
    assert value != 0
    out = 1
    for order in range(1, 25):
        out = f25_mul(out, value)
        if out == 1:
            return order
    raise AssertionError("F_25 order not found")


def verify_small_weighted_fibers() -> int:
    primitive = next(value for value in range(2, 25) if f25_order(value) == 24)
    zeta = f25_pow(primitive, 3)
    assert f25_order(zeta) == 8

    n = 8
    subsets = list(combinations(range(n), 4))
    twists = [
        (1,) * n,
        (1, 2, 3, 4, 1, 2, 3, 4),
        (4, 3, 2, 1, 4, 3, 2, 1),
    ]
    checks = 0

    for units in twists:
        for shift in range(n):
            for depth in range(1, n + 1):
                columns = []
                for i in range(n):
                    t_i = f25_pow(zeta, i)
                    rho_i = f25_mul(units[i], f25_pow(zeta, shift * i))
                    columns.append(
                        tuple(
                            f25_mul(rho_i, f25_pow(t_i, j))
                            for j in range(depth)
                        )
                    )

                fibers: Counter[tuple[int, ...]] = Counter()
                for support in subsets:
                    syndrome = (0,) * depth
                    for i in support:
                        syndrome = tuple(
                            f25_add(syndrome[j], columns[i][j])
                            for j in range(depth)
                        )
                    fibers[syndrome] += 1

                interval = {(shift + j) % n for j in range(depth)}
                closed = set().union(*(orbit(n, 5, k) for k in interval))
                bound = 5 ** (n - len(closed))
                assert max(fibers.values()) <= bound
                checks += 1
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact checks")
    parser.add_argument(
        "--max-s",
        type=int,
        default=11,
        help="exhaust every interval through N=2^max_s (default: 11)",
    )
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")
    if not 3 <= args.max_s <= 13:
        parser.error("--max-s must lie between 3 and 13")

    orbit_checks = verify_orbit_structure(args.max_s)
    interval_checks = verify_all_intervals(args.max_s)
    fiber_checks = verify_small_weighted_fibers()
    total = orbit_checks + interval_checks + fiber_checks
    print(f"orbit_structure_checks={orbit_checks}")
    print(f"dyadic_interval_checks={interval_checks}")
    print(f"gf25_weighted_fiber_checks={fiber_checks}")
    print(f"RESULT: PASS ({total}/{total} checks)")


if __name__ == "__main__":
    main()
