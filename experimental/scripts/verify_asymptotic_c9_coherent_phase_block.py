#!/usr/bin/env python3
"""Finite replay checks for the coherent-phase C9 frequency block."""

from __future__ import annotations

import argparse
import cmath
import math
from itertools import combinations, product


NUMERICAL_TOLERANCE = 1e-10


class VerificationError(RuntimeError):
    """Raised when a replay check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def factor_distinct(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(prime: int) -> int:
    factors = factor_distinct(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // ell, prime) != 1 for ell in factors):
            return candidate
    raise VerificationError("primitive root not found")


def subgroup(prime: int, order: int) -> list[int]:
    require((prime - 1) % order == 0, "subgroup order must divide p-1")
    generator = pow(primitive_root(prime), (prime - 1) // order, prime)
    points = [pow(generator, i, prime) for i in range(order)]
    require(len(set(points)) == order, "subgroup generator has wrong order")
    return points


def centered(value: int, prime: int) -> int:
    value %= prime
    if value > prime // 2:
        value -= prime
    return value


def eval_poly(coefficients: tuple[int, ...], point: int, prime: int) -> int:
    return sum(
        coefficient * pow(point, degree, prime)
        for degree, coefficient in enumerate(coefficients, start=1)
    ) % prime


def coherent_phase_set(
    prime: int,
    points: list[int],
    degree: int,
    q: int,
) -> list[tuple[int, ...]]:
    radius = prime // q
    out: list[tuple[int, ...]] = []
    for coefficients in product(range(prime), repeat=degree):
        base = eval_poly(coefficients, points[0], prime)
        if all(
            abs(centered(eval_poly(coefficients, point, prime) - base, prime))
            <= radius
            for point in points
        ):
            out.append(coefficients)
    return out


def character(value: int, prime: int) -> complex:
    return cmath.exp(2j * math.pi * (value % prime) / prime)


def verify_coherent_phase_block() -> int:
    prime = 97
    order = 4
    degree = 2
    points = subgroup(prime, order)

    difference_images = set()
    for coefficients in product(range(prime), repeat=degree):
        base = eval_poly(coefficients, points[0], prime)
        differences = tuple(
            (eval_poly(coefficients, points[j], prime) - base) % prime
            for j in range(1, degree + 1)
        )
        difference_images.add(differences)
    require(
        len(difference_images) == prime**degree,
        "evaluation-difference map is not bijective",
    )

    lower = math.cos(math.pi / 6)
    checks = 1

    for weight in range(1, order + 1):
        q = 12 * weight
        phase_set = coherent_phase_set(prime, points, degree, q)
        h_q = 2 * (prime // q) + 1
        require(len(phase_set) <= h_q**degree, "coherent-phase count failed")
        checks += 1

        supports = list(combinations(range(order), weight))
        masks = [
            [
                supports[index]
                for index in range(len(supports))
                if bits & (1 << index)
            ]
            for bits in range(1, 1 << len(supports))
        ]

        for coefficients in phase_set:
            values = [eval_poly(coefficients, point, prime) for point in points]
            base = values[0]
            deltas = [centered(value - base, prime) for value in values]
            for support in supports:
                delta_sum = sum(deltas[index] for index in support)
                require(
                    12 * abs(delta_sum) <= prime,
                    "weight-m phase left the exact pi/6 sector",
                )
                require(
                    math.cos(2 * math.pi * delta_sum / prime)
                    >= lower - NUMERICAL_TOLERANCE,
                    "sector cosine smoke test failed",
                )
                checks += 1

            for mask in masks:
                coefficient = sum(
                    character(sum(values[index] for index in support), prime)
                    for support in mask
                )
                require(
                    abs(coefficient)
                    >= lower * len(mask) - NUMERICAL_TOLERANCE,
                    "arbitrary-mask coefficient lower bound failed",
                )
                checks += 1

        # Numerically exhaust the partial Fourier sum for the full slice.
        nonzero = [coefficients for coefficients in phase_set if any(coefficients)]
        fourier_coefficients: dict[tuple[int, ...], complex] = {}
        for coefficients in nonzero:
            values = [eval_poly(coefficients, point, prime) for point in points]
            fourier_coefficients[coefficients] = sum(
                character(sum(values[index] for index in support), prime)
                for support in supports
            )
        bound = len(supports) * (h_q / prime) ** degree
        for y in product(range(prime), repeat=degree):
            block_sum = sum(
                value
                * character(
                    -sum(
                        c_i * y_i for c_i, y_i in zip(coefficients, y)
                    ),
                    prime,
                )
                for coefficients, value in fourier_coefficients.items()
            ) / prime**degree
            require(
                abs(block_sum) <= bound + NUMERICAL_TOLERANCE,
                "partial Fourier-block smoke test failed",
            )
            checks += 1
    return checks


def projective_lines(prime: int) -> list[tuple[int, int]]:
    return [(0, 1)] + [(1, slope) for slope in range(prime)]


def verify_projective_ubiquity() -> int:
    prime = 29
    order = 4
    degree = 2
    q = 3
    require(prime > q ** (order - 1), "Dirichlet box hypothesis failed")
    points = subgroup(prime, order)
    phase_set = set(coherent_phase_set(prime, points, degree, q))
    require(1 < len(phase_set) < prime**degree, "projective fixture is vacuous")
    checks = 2
    for line in projective_lines(prime):
        require(
            any(
                tuple((scalar * coordinate) % prime for coordinate in line)
                in phase_set
                for scalar in range(1, prime)
            ),
            f"projective line {line} misses the coherent-phase set",
        )
        checks += 1

    value_set_line = (1, 0)
    witness = next(
        tuple((scalar * coordinate) % prime for coordinate in value_set_line)
        for scalar in range(1, prime)
        if tuple((scalar * coordinate) % prime for coordinate in value_set_line)
        in phase_set
    )
    values = [eval_poly(witness, point, prime) for point in points]
    require(len(set(values)) == order, "value-set route-cut witness is not injective")
    checks += 1
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact checks")
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")

    coherent_checks = verify_coherent_phase_block()
    projective_checks = verify_projective_ubiquity()
    total = coherent_checks + projective_checks
    print(f"coherent_phase_checks={coherent_checks}")
    print(f"projective_line_checks={projective_checks}")
    print(f"numerical_tolerance={NUMERICAL_TOLERANCE:.1e}")
    print(f"RESULT: PASS (checks={total})")


if __name__ == "__main__":
    main()
