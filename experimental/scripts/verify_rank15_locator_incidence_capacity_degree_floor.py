#!/usr/bin/env python3
"""Replay the rank-15 M=218 incidence-capacity degree-floor certificate."""

from __future__ import annotations

import hashlib
import json
from math import isqrt


def fail(message: str) -> None:
    raise RuntimeError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def ceil_div(a: int, b: int) -> int:
    if b <= 0:
        fail("ceil_div requires a positive denominator")
    return (a + b - 1) // b


def bareiss_det(matrix: list[list[int]]) -> int:
    """Exact determinant by fraction-free Bareiss elimination."""
    n = len(matrix)
    check(n > 0, "empty determinant")
    check(all(len(row) == n for row in matrix), "matrix is not square")
    a = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot = next((i for i in range(k + 1, n) if a[i][k] != 0), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        pivot_value = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot_value - a[i][k] * a[k][j]
                check(numerator % previous == 0, "Bareiss division was not exact")
                a[i][j] = numerator // previous
        previous = pivot_value
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[n - 1][n - 1]


def factor_integer(value: int) -> dict[int, int]:
    value = abs(value)
    check(value > 0, "cannot factor zero")
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def residual_matrix(cycle_lengths: tuple[int, ...]) -> list[list[int]]:
    """Return 14I-A_R when the complement of R has these cycles."""
    check(sum(cycle_lengths) == 10, "cycle partition must have size ten")
    check(all(length >= 3 for length in cycle_lengths), "simple cycles need length >= 3")
    adjacency_complement = [[0] * 10 for _ in range(10)]
    offset = 0
    for length in cycle_lengths:
        vertices = list(range(offset, offset + length))
        for index, vertex in enumerate(vertices):
            neighbor = vertices[(index + 1) % length]
            adjacency_complement[vertex][neighbor] = 1
            adjacency_complement[neighbor][vertex] = 1
        offset += length

    # A_R = J-I-A_complement, hence 14I-A_R = 15I-J+A_complement.
    return [
        [15 * int(i == j) - 1 + adjacency_complement[i][j] for j in range(10)]
        for i in range(10)
    ]


def merged_factor_exponents(det_r: int) -> dict[int, int]:
    # 225 * 7^25 * 15^182 * det_r.
    factors = {3: 2 + 182, 5: 2 + 182, 7: 25}
    for prime, exponent in factor_integer(det_r).items():
        factors[prime] = factors.get(prime, 0) + exponent
    return factors


def main() -> None:
    n_coordinates = 1_053_556
    agreement = 72_451
    points = 218
    rich_size = 15
    w_218 = 1_044_534
    required = points * agreement
    check(required == 15_794_318, "M*a mismatch")

    uncovered_edges = points * (points - 1) // 2 - points * (rich_size * (rich_size - 1) // 2)
    check(uncovered_edges == 763, "uncovered edge count mismatch")
    check(2 * uncovered_edges == points * 7, "uncovered graph is not 7-regular")

    assigned_d = 4_792
    assigned_upper = 8 * n_coordinates + 7 * points * assigned_d
    check(assigned_upper == 15_741_040, "assigned upper bound mismatch")
    check(required - assigned_upper == 53_278, "assigned deficit mismatch")

    for degree in range(4_792, 4_827):
        check(216 * degree < w_218, f"coverage gate failed at d={degree}")
        upper_218 = 8 * n_coordinates + 7 * 218 * degree
        upper_217 = 8 * n_coordinates + 1_525 * degree
        check(upper_218 < required, f"b=218 not eliminated at d={degree}")
        check(upper_217 < required, f"b=217 not eliminated at d={degree}")
    check(8 * n_coordinates + 7 * 218 * 4_826 == 15_792_924, "d=4826 b=218 bound")
    check(8 * n_coordinates + 1_525 * 4_826 == 15_788_098, "d=4826 b=217 bound")

    d_border = 4_827
    check(216 * d_border < w_218, "d=4827 coverage gate")
    border_218_217 = 8 * n_coordinates + 7 * 217 * d_border
    border_217 = 8 * n_coordinates + 1_525 * d_border
    check(border_218_217 == 15_760_661, "d=4827 b=218,t=217 bound")
    check(border_217 == 15_789_623, "d=4827 b=t=217 bound")
    check(border_218_217 < required and border_217 < required, "d=4827 t=217 survives")
    border_margin = 8 * n_coordinates + 7 * 218 * d_border - required
    check(border_margin == 132, "d=4827 incidence margin")
    check(agreement - rich_size * d_border == 46, "per-point non-rich demand")
    check((7 * border_margin) // 46 == 20, "residual vertex ceiling")

    expected_factors = {
        (10,): {7: 1, 11: 2, 13: 1, 19: 2, 239: 2},
        (7, 3): {2: 2, 7: 3, 17: 1, 3121: 2},
        (6, 4): {2: 10, 3: 2, 5: 2, 7: 3, 13: 2, 17: 1},
        (5, 5): {7: 1, 11: 4, 17: 1, 19: 4},
        (4, 3, 3): {2: 4, 3: 2, 5: 2, 7: 5, 13: 1, 17: 2},
    }
    determinant_rows = []
    for cycles, expected in expected_factors.items():
        det_r = bareiss_det(residual_matrix(cycles))
        actual = factor_integer(det_r)
        check(actual == expected, f"determinant factorization mismatch for {cycles}: {actual}")
        full_factors = merged_factor_exponents(det_r)
        odd_primes = sorted(prime for prime, exponent in full_factors.items() if exponent % 2)
        expected_witness = 13 if cycles in ((10,), (4, 3, 3)) else 17
        check(expected_witness in odd_primes, f"missing odd valuation for {cycles}")
        determinant_rows.append(
            {
                "complement_cycles": list(cycles),
                "det_14I_minus_A_R": det_r,
                "odd_valuation_primes": odd_primes,
            }
        )

    residual_rows = []
    for k_seven_lines in range(3):
        outside = 18 - 7 * k_seven_lines
        nonseven_needed = ceil_div(46 * outside, 6)
        maximum = 7 * 121 - nonseven_needed
        check(maximum < 828, f"c=25 residual capacity survives for k={k_seven_lines}")
        residual_rows.append(
            {
                "k7_lines": k_seven_lines,
                "outside_vertices": outside,
                "nonseven_sections_needed": nonseven_needed,
                "maximum_incidence": maximum,
            }
        )
    check([row["maximum_incidence"] for row in residual_rows] == [709, 762, 816], "K7 table")

    first_d = 4_828
    check(216 * first_d < w_218, "d=4828 coverage gate")
    first_t217_b218 = 8 * n_coordinates + 7 * 217 * first_d
    first_b217 = 8 * n_coordinates + 1_525 * first_d
    check(first_t217_b218 == 15_762_180, "d=4828 b=218,t=217 bound")
    check(first_b217 == 15_791_148, "d=4828 b=t=217 bound")
    check(first_t217_b218 < required and first_b217 < required, "d=4828 t=217 survives")
    first_margin = 8 * n_coordinates + 7 * 218 * first_d - required
    degree_room = 218 * first_d - w_218
    check(first_margin == 1_658, "d=4828 incidence margin")
    check(degree_room == 7_970, "d=4828 degree room")
    check(4_979 - first_d == 151, "d=4828 r ceiling")

    certificate = {
        "assigned_branch": {
            "d": assigned_d,
            "upper_at_r0": assigned_upper,
            "required": required,
            "deficit_at_r0": required - assigned_upper,
        },
        "degree_floor": 4_828,
        "determinant_rows": determinant_rows,
        "first_residual": {
            "d": first_d,
            "t": 218,
            "b": 218,
            "r_max": 151,
            "incidence_margin": first_margin,
            "degree_room": degree_room,
        },
        "residual_k7_rows": residual_rows,
    }
    canonical = json.dumps(certificate, sort_keys=True, separators=(",", ":")).encode("ascii")
    digest = hashlib.sha256(canonical).hexdigest()

    print("RANK15_LOCATOR_INCIDENCE_CAPACITY_DEGREE_FLOOR")
    print(f"assigned_deficit_r0={required - assigned_upper}")
    print("eliminated_degrees=4792..4827")
    for row in determinant_rows:
        cycles = "+".join(str(x) for x in row["complement_cycles"])
        odd = ",".join(str(x) for x in row["odd_valuation_primes"])
        print(f"determinant cycles={cycles} odd_valuation_primes={odd}")
    for row in residual_rows:
        print(
            "residual "
            f"k7={row['k7_lines']} outside={row['outside_vertices']} "
            f"nonseven_needed={row['nonseven_sections_needed']} "
            f"max_incidence={row['maximum_incidence']}"
        )
    print("first_residual=d4828,t218,b218,r<=151,margin1658,degree_room7970")
    print(f"certificate_sha256={digest}")
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
