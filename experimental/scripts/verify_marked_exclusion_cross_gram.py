#!/usr/bin/env python3
"""Replay the marked-exclusion cross-Gram identities on an exact RS source."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb, isqrt, sqrt


N = 7
P = 14_197
GENERATOR = 1_054
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


def add(*vectors):
    return tuple(sum(entries) % P for entries in zip(*vectors))


def scale(scalar, vector):
    return tuple((scalar * entry) % P for entry in vector)


def syndrome(indices, values):
    zero = (0,) * len(values[0])
    return add(zero, *(values[index] for index in indices))


def assert_counter_equal(left, right, label):
    for key in set(left) | set(right):
        assert left[key] == right[key], (
            f"{label} failed at {key}: {left[key]} != {right[key]}"
        )


def marked_single(values):
    a = Fraction(R - 1, N)
    total = Counter()
    cross = Counter()
    covariance = Counter()
    genuine = Counter()
    excluded = Counter()

    for base in combinations(range(N), R - 1):
        base_set = set(base)
        for point in range(N):
            output = add(syndrome(base, values), values[point])
            is_excluded = point in base_set
            coefficient = (1 - a) if is_excluded else -a
            total[output] += 1
            cross[output] += coefficient
            covariance[output] += coefficient * coefficient
            if is_excluded:
                excluded[output] += 1
            else:
                genuine[output] += 1

    reconstructed = Counter()
    covariance_defect = Counter()
    excluded_defect = Counter()
    for output in total:
        reconstructed[output] = (1 - a) * total[output] - cross[output]
        covariance_defect[output] = (
            (1 - a) ** 2 * total[output] - covariance[output]
        )
        excluded_defect[output] = covariance[output] - a**2 * total[output]

    assert_counter_equal(reconstructed, genuine, "single cross-Gram")
    assert_counter_equal(
        covariance_defect,
        Counter({key: (1 - 2 * a) * value for key, value in genuine.items()}),
        "single covariance defect",
    )
    assert_counter_equal(
        excluded_defect,
        Counter({key: (1 - 2 * a) * value for key, value in excluded.items()}),
        "single excluded defect",
    )
    assert sum(covariance.values()) / sum(genuine.values()) == a

    genuine_singular = Counter()
    excluded_singular = Counter()
    for output, count in genuine.items():
        genuine_singular[count] += 1
    for output, count in excluded.items():
        if genuine[output] == 0:
            excluded_singular[(1 - a) ** 2 * count] += 1

    assert genuine_singular == Counter({R: comb(N, R)})
    assert excluded_singular == Counter(
        {(1 - a) ** 2: (R - 1) * comb(N, R - 1)}
    )
    assert sum(genuine.values()) == R * comb(N, R)
    assert len(genuine) == comb(N, R)

    return {
        "a": a,
        "total": total,
        "cross": cross,
        "covariance": covariance,
        "genuine": genuine,
        "excluded": excluded,
    }


def marked_pair(values):
    b = Fraction(2 * R - 1, N)
    total = Counter()
    cross = Counter()
    covariance = Counter()
    genuine = Counter()

    points = tuple(range(N))
    for positive_base in combinations(points, R - 1):
        positive_set = set(positive_base)
        available = tuple(point for point in points if point not in positive_set)
        for negative in combinations(available, R):
            negative_set = set(negative)
            negative_sum = syndrome(negative, values)
            for point in points:
                output = add(
                    syndrome(positive_base, values),
                    scale(-1, negative_sum),
                    values[point],
                )
                is_excluded = point in positive_set or point in negative_set
                coefficient = (1 - b) if is_excluded else -b
                total[output] += 1
                cross[output] += coefficient
                covariance[output] += coefficient * coefficient
                if not is_excluded:
                    genuine[output] += 1

    reconstructed = Counter()
    covariance_defect = Counter()
    for output in total:
        reconstructed[output] = (1 - b) * total[output] - cross[output]
        covariance_defect[output] = (
            (1 - b) ** 2 * total[output] - covariance[output]
        )

    assert_counter_equal(reconstructed, genuine, "pair cross-Gram")
    assert_counter_equal(
        covariance_defect,
        Counter({key: (1 - 2 * b) * value for key, value in genuine.items()}),
        "pair covariance defect",
    )
    assert set(genuine.values()) == {R}
    assert len(genuine) == comb(N, R) * comb(N - R, R)

    return {
        "b": b,
        "total": total,
        "cross": cross,
        "covariance": covariance,
        "genuine": genuine,
    }


def elementary(power_sums):
    s1 = power_sums[0]
    if len(power_sums) == 1:
        return (s1,)
    s2 = power_sums[1]
    e2 = (s1 * s1 - s2) * pow(2, -1, P) % P
    if len(power_sums) == 2:
        return (s1, e2)
    s3 = power_sums[2]
    e3 = (
        (s1**3 - 3 * s1 * s2 + 2 * s3) * pow(6, -1, P)
    ) % P
    return (s1, e2, e3)


def check_newton(values, single_report):
    mapped = Counter()
    for output, count in single_report["total"].items():
        mapped[elementary(output)] += count
    assert len(mapped) == len(single_report["total"])
    assert sorted(mapped.values()) == sorted(single_report["total"].values())

    supports = tuple(combinations(range(N), R))
    power_outputs = {support: syndrome(support, values) for support in supports}
    coefficient_outputs = {
        support: elementary(power_outputs[support]) for support in supports
    }
    for left in supports:
        for right in supports:
            assert (power_outputs[left] == power_outputs[right]) == (
                coefficient_outputs[left] == coefficient_outputs[right]
            )


def check_injection(domain):
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


def check_half_density_symbolically():
    a = Fraction(1, 2)
    for total, excluded in ((2, 1), (18, 9), (100, 50)):
        genuine = total - excluded
        covariance = (1 - a) ** 2 * excluded + a**2 * genuine
        assert covariance == Fraction(total, 4)
        cross = (1 - a) * excluded - a * genuine
        assert (1 - a) * total - cross == genuine


def main():
    assert is_prime(P)
    domain = tuple(pow(GENERATOR, index, P) for index in range(N))
    assert domain == EXPECTED_DOMAIN
    assert pow(GENERATOR, N, P) == 1
    check_injection(domain)
    check_half_density_symbolically()

    for width in (2, 3):
        values = tuple(
            tuple(pow(point, exponent, P) for exponent in range(1, width + 1))
            for point in domain
        )
        single = marked_single(values)
        pair = marked_pair(values)
        check_newton(values, single)
        print(f"w={width}: single_cross_gram=PASS")
        print(f"w={width}: pair_cross_gram=PASS")
        print(f"w={width}: single_image={len(single['genuine'])}")
        print(f"w={width}: pair_image={len(pair['genuine'])}")
        print(
            f"w={width}: hs_ratio="
            f"{sum(single['covariance'].values())/sum(single['genuine'].values())}"
        )
        print(f"w={width}: newton_single=PASS")

    a = Fraction(R - 1, N)
    print("RESULT: PASS")
    print(f"parameters=n:{N},p:{P},g:{GENERATOR},r:{R}")
    print(f"single_genuine_singular=sqrt({R}) x {comb(N,R)}")
    print(f"single_repeat_singular={1-a} x {(R-1)*comb(N,R-1)}")
    print("half_density_covariance_singularity=PASS")
    print("tamper_free_exact_arithmetic=PASS")


if __name__ == "__main__":
    main()
