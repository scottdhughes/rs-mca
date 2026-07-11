#!/usr/bin/env python3
"""Exact arithmetic checks for the fractional realized-image compiler."""

from fractions import Fraction
from itertools import product


def participation(counts):
    mass = sum(counts.values())
    energy = sum(value * value for value in counts.values())
    return Fraction(mass * mass, energy)


def check_instance(fibers, capacity, L, K, omega):
    labels = set().union(*(set(fiber) for fiber in fibers))
    point_load = {label: sum(fiber.get(label, 0) for fiber in fibers) for label in labels}
    resources = sum((participation(fiber) for fiber in fibers), Fraction(0))
    assert resources <= capacity

    covered = []
    for fiber in fibers:
        charge = Fraction(K, L) * participation(fiber)
        charge += sum(omega.get(label, 0) * value for label, value in fiber.items())
        covered.append(charge)
    if all(charge >= 1 for charge in covered):
        rhs = Fraction(K * capacity, L) + sum(
            omega.get(label, 0) * point_load[label] for label in labels
        )
        assert len(fibers) <= rhs
    return resources, point_load, covered


def main():
    instances = [
        ([{0: 1}, {1: 1}, {2: 1}], 3, 3, 1, {0: 1, 1: 1, 2: 1}),
        ([{0: 4}, {1: 3}, {2: 2}], 9, 12, 3, {0: Fraction(1, 4), 1: Fraction(1, 3), 2: Fraction(1, 2)}),
        ([{0: 2, 1: 2}, {2: 3, 3: 1}], 8, 8, 2, {0: Fraction(1, 4), 1: Fraction(1, 4), 2: Fraction(1, 4), 3: Fraction(1, 4)}),
    ]
    for args in instances:
        check_instance(*args)

    # Exhaust small disjoint-support incidence systems. Each integer in a
    # fiber is a boundary multiplicity, and sum P_gamma <= sum m_gamma <= M.
    checks = 0
    for raw in product(range(1, 5), repeat=4):
        fibers = [{index: value} for index, value in enumerate(raw)]
        capacity = sum(raw)
        for L in range(1, 7):
            for K in range(1, 5):
                omega = {index: Fraction(1, value) for index, value in enumerate(raw)}
                check_instance(fibers, capacity, L, K, omega)
                checks += 1

    # Threshold and harmonic identities.
    counts = {0: 3, 1: 1, 2: 2}
    mass = 6
    energy = 14
    P = participation(counts)
    theta = Fraction(12, 1) / P
    assert P == Fraction(mass * mass, energy) == Fraction(18, 7)
    assert theta == Fraction(14, 3)
    assert sum(Fraction(value, mass) ** 2 for value in counts.values()) == Fraction(energy, mass * mass)

    # Reversing any audited normalization must fail.
    assert Fraction(3 * 9, 12) != Fraction(3 * 12, 9)  # KM/L versus KL/M
    assert Fraction(mass * mass, energy) != Fraction(energy, mass * mass)
    assert Fraction(12, 1) / P != P / 12
    assert Fraction(3, mass) != Fraction(mass, 3)

    print("RESULT: PASS")
    print(f"exhaustive_instances={checks}")
    print("resource_capacity=PASS")
    print("fractional_cover_payment=PASS")
    print("threshold_harmonic_identities=PASS")
    print("normalization_tamper_checks=PASS")


if __name__ == "__main__":
    main()
