#!/usr/bin/env python3
"""Replay the dense-exclusion centered-norm route cut exactly."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb, isqrt


N = 7
P = 14_197
G = 1_054
R = 3
EXPECTED_DOMAIN = (1, 1_054, 3_550, 7_889, 9_761, 9_466, 10_870)
EXPECTED_PATTERN_COUNT = 12_328


def is_prime(value):
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def add_vectors(*vectors):
    return tuple(sum(entries) % P for entries in zip(*vectors))


def scale_vector(scalar, vector):
    return tuple((scalar * entry) % P for entry in vector)


def syndrome(indices, values):
    zero = (0,) * len(values[0])
    return add_vectors(zero, *(values[index] for index in indices))


def subset_census(size, values):
    out = Counter()
    for subset in combinations(range(N), size):
        out[syndrome(subset, values)] += 1
    return out


def disjoint_census(positive_size, negative_size, values):
    out = Counter()
    points = tuple(range(N))
    for negative_tuple in combinations(points, negative_size):
        negative = set(negative_tuple)
        available = tuple(point for point in points if point not in negative)
        negative_sum = syndrome(negative_tuple, values)
        for positive_tuple in combinations(available, positive_size):
            target = add_vectors(
                syndrome(positive_tuple, values), scale_vector(-1, negative_sum)
            )
            out[target] += 1
    return out


def convolve(left, right):
    out = Counter()
    for first, first_count in left.items():
        for second, second_count in right.items():
            out[add_vectors(first, second)] += first_count * second_count
    return out


def linear_combination(*terms):
    out = Counter()
    for scalar, counter in terms:
        for target, count in counter.items():
            out[target] += scalar * count
    return +out


def assert_counters_equal(left, right, label):
    for target in set(left) | set(right):
        if left[target] != right[target]:
            raise AssertionError(
                f"{label} failed at {target}: {left[target]} != {right[target]}"
            )


def centered_norm_square(correction, proxy, scalar):
    total = Fraction(0)
    for target in set(correction) | set(proxy):
        value = Fraction(correction[target]) - scalar * proxy[target]
        total += value * value
    return total


def check_coefficient_injection(domain):
    patterns = tuple(
        coefficients
        for coefficients in product((-1, 0, 1, 2), repeat=N)
        if 0 <= sum(coefficients) <= N - 1
    )
    residues = {
        sum(coefficient * domain[index] for index, coefficient in enumerate(pattern))
        % P
        for pattern in patterns
    }
    assert len(patterns) == EXPECTED_PATTERN_COUNT
    assert len(residues) == len(patterns)
    return len(patterns)


def repeated_single_census(values):
    out = Counter()
    points = tuple(range(N))
    for point in points:
        available = tuple(index for index in points if index != point)
        for remainder in combinations(available, R - 2):
            target = add_vectors(
                syndrome(remainder, values), scale_vector(2, values[point])
            )
            out[target] += 1
    return out


def repeated_pair_census(values):
    out = Counter()
    points = tuple(range(N))
    for point in points:
        without_point = tuple(index for index in points if index != point)
        for negative_tuple in combinations(without_point, R):
            negative = set(negative_tuple)
            available = tuple(
                index for index in without_point if index not in negative
            )
            for positive_tuple in combinations(available, R - 2):
                target = add_vectors(
                    syndrome(positive_tuple, values),
                    scale_vector(2, values[point]),
                    scale_vector(-1, syndrome(negative_tuple, values)),
                )
                out[target] += 1
    return out


def check_width(width, domain):
    values = tuple(
        tuple(pow(point, exponent, P) for exponent in range(1, width + 1))
        for point in domain
    )
    point_measure = Counter(values)

    nu_previous = subset_census(R - 1, values)
    nu_current = subset_census(R, values)
    single_convolution = convolve(nu_previous, point_measure)
    single_correction = repeated_single_census(values)
    single_rhs = linear_combination(
        (R, nu_current), (1, single_correction)
    )
    assert_counters_equal(single_convolution, single_rhs, "single recursion")

    omega_previous = disjoint_census(R - 1, R, values)
    omega_current = disjoint_census(R, R, values)
    omega_lower = disjoint_census(R - 1, R - 1, values)
    pair_convolution = convolve(omega_previous, point_measure)
    pair_correction = repeated_pair_census(values)
    height = N - 2 * R + 2
    pair_rhs = linear_combination(
        (R, omega_current), (1, pair_correction), (height, omega_lower)
    )
    assert_counters_equal(pair_convolution, pair_rhs, "pair recursion")

    single_image = comb(N, R)
    pair_image = comb(N, R) * comb(N - R, R)
    assert len(nu_current) == single_image
    assert len(omega_current) == pair_image
    assert set(nu_current.values()) == {1}
    assert set(omega_current.values()) == {1}

    a = Fraction(R - 1, N)
    single_norm = centered_norm_square(
        single_correction, single_convolution, a
    )
    expected_single = (
        comb(N, R) * (a * R) ** 2
        + (R - 1) * comb(N, R - 1) * (1 - a) ** 2
    )
    assert single_norm == expected_single == Fraction(330, 7)

    b = Fraction(2 * R - 1, N)
    centered_pair_correction = linear_combination(
        (1, pair_correction), (height, omega_lower)
    )
    pair_norm = centered_norm_square(
        centered_pair_correction, pair_convolution, b
    )
    pair_mass = comb(N, R) * comb(N - R, R)
    transition_mass = comb(N, R) * comb(N - R, R - 1)
    cancellation_mass = comb(N, R - 1) * comb(N - R + 1, R - 1)
    c = 1 - b
    expected_pair = (
        pair_mass * (b * R) ** 2
        + (R - 1) * transition_mass * c**2
        + cancellation_mass * (c * height) ** 2
    )
    assert pair_norm == expected_pair == Fraction(5_820, 7)

    return {
        "width": width,
        "single_image": single_image,
        "pair_image": pair_image,
        "single_norm": single_norm,
        "pair_norm": pair_norm,
    }


def main():
    assert is_prime(P)
    domain = tuple(pow(G, index, P) for index in range(N))
    assert domain == EXPECTED_DOMAIN
    assert pow(G, N, P) == 1
    assert G % P != 1
    assert len(set(domain)) == N

    pattern_count = check_coefficient_injection(domain)
    reports = tuple(check_width(width, domain) for width in (2, 3))

    print(f"parameters: n={N} p={P} g={G} r={R}")
    print(f"domain: {domain}")
    print(
        "coefficient injection: PASS "
        f"({pattern_count:,} patterns, {pattern_count:,} distinct residues)"
    )
    for report in reports:
        width = report["width"]
        print(
            f"w={width}: singleton images PASS "
            f"(|im nu_3|={report['single_image']}, "
            f"|im omega_(3,3)|={report['pair_image']})"
        )
        print(f"w={width}: pointwise single recursion PASS")
        print(f"w={width}: pointwise pair recursion PASS")
        print(f"w={width}: ||E_3||_2^2={report['single_norm']}")
        print(f"w={width}: ||K_3||_2^2={report['pair_norm']}")
    print("theorem: b2_dense_exclusion_norm_route_cut")
    print("status: COUNTEREXAMPLE / PROVED exact finite replay")


if __name__ == "__main__":
    main()
