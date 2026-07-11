#!/usr/bin/env python3
"""Exact replay for the low-direction hybrid exact-weight compiler."""

from collections import defaultdict
from itertools import combinations, product


def add(first, second, modulus):
    return tuple((x + y) % modulus for x, y in zip(first, second))


def scale(scalar, vector, modulus):
    return tuple(scalar * x % modulus for x in vector)


def vector_sum(first, second, modulus):
    return add(first, second, modulus)


def weight(vector):
    return sum(value != 0 for value in vector)


def support(vector):
    return tuple(index for index, value in enumerate(vector) if value)


def parity_columns(modulus, length, redundancy, weights=None):
    if weights is None:
        weights = [1] * length
    return [
        tuple(
            weights[index] * pow(index, degree, modulus) % modulus
            for degree in range(redundancy)
        )
        for index in range(length)
    ]


def syndrome(word, columns, modulus):
    return tuple(
        sum(word[index] * columns[index][degree] for index in range(len(word)))
        % modulus
        for degree in range(len(columns[0]))
    )


def low_weight_words(modulus, length, radius):
    yield (0,) * length
    for size in range(1, radius + 1):
        for selected in combinations(range(length), size):
            for values in product(range(1, modulus), repeat=size):
                word = [0] * length
                for index, value in zip(selected, values):
                    word[index] = value
                yield tuple(word)


def matrix_rank(rows, modulus):
    if not rows:
        return 0
    matrix = [list(row) for row in rows]
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, modulus)
        matrix[pivot_row] = [value * inverse % modulus for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (value - factor * pivot_value) % modulus
                for value, pivot_value in zip(matrix[row], matrix[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def hybrid_term(length, redundancy, radius, direction_distance, exact_weight):
    kappa = length - redundancy
    punctured_length = length - direction_distance
    punctured_distance = redundancy + 1 - direction_distance
    assert punctured_distance == punctured_length - kappa + 1
    effective_distance = min(
        punctured_length,
        max(
            punctured_distance,
            direction_distance + 2 * exact_weight - 2 * radius,
        ),
    )
    denominator = (
        punctured_length * effective_distance
        - 2 * punctured_length * exact_weight
        + exact_weight * exact_weight
    )
    cluster_height = max(1, direction_distance + exact_weight - radius)
    assert denominator == (
        (punctured_length - exact_weight) ** 2
        - punctured_length * (punctured_length - effective_distance)
    )
    if denominator > 0:
        assert effective_distance > exact_weight
        numerator = punctured_length * (effective_distance - exact_weight)
        assert numerator - denominator == (
            exact_weight * (punctured_length - exact_weight)
        )
        list_factor = numerator // denominator
        cluster_factor = direction_distance // cluster_height
        summand = cluster_factor * list_factor
    else:
        numerator = None
        list_factor = None
        cluster_factor = None
        summand = None
    return {
        "e": exact_weight,
        "D": effective_distance,
        "J": denominator,
        "h": cluster_height,
        "numerator": numerator,
        "list_factor": list_factor,
        "cluster_factor": cluster_factor,
        "summand": summand,
    }


def hybrid_terms(length, redundancy, radius, direction_distance):
    return [
        hybrid_term(
            length, redundancy, radius, direction_distance, exact_weight
        )
        for exact_weight in range(radius + 1)
    ]


def hybrid_bound(length, redundancy, radius, direction_distance):
    punctured_length = length - direction_distance
    if radius >= punctured_length:
        return None
    terms = hybrid_terms(length, redundancy, radius, direction_distance)
    if any(term["J"] <= 0 for term in terms):
        return None
    bound = sum(term["summand"] for term in terms)
    assert bound <= length**4
    return bound


def span_for_support(selected, columns, modulus):
    span = set()
    for coefficients in product(range(modulus), repeat=len(selected)):
        word = [0] * len(columns)
        for index, coefficient in zip(selected, coefficients):
            word[index] = coefficient
        span.add(syndrome(tuple(word), columns, modulus))
    return span


def exhaustive_chart(modulus, length, redundancy, radius):
    columns = parity_columns(modulus, length, redundancy)
    zero = (0,) * redundancy
    syndromes = list(product(range(modulus), repeat=redundancy))

    minimum_weight = {}
    kernel_minimum = None
    kernel_size = 0
    for word in product(range(modulus), repeat=length):
        value = syndrome(word, columns, modulus)
        word_weight = weight(word)
        old = minimum_weight.get(value)
        if old is None or word_weight < old:
            minimum_weight[value] = word_weight
        if value == zero:
            kernel_size += 1
            if word_weight:
                kernel_minimum = (
                    word_weight
                    if kernel_minimum is None
                    else min(kernel_minimum, word_weight)
                )

    assert len(minimum_weight) == modulus**redundancy
    assert kernel_size == modulus ** (length - redundancy)
    assert kernel_minimum == redundancy + 1

    supports_by_syndrome = defaultdict(set)
    for word in low_weight_words(modulus, length, radius):
        supports_by_syndrome[syndrome(word, columns, modulus)].add(support(word))

    support_spans = {
        selected: span_for_support(selected, columns, modulus)
        for selected in {
            item
            for support_set in supports_by_syndrome.values()
            for item in support_set
        }
    }

    eligible_directions = []
    for y_1 in syndromes:
        if y_1 == zero:
            continue
        direction_distance = minimum_weight[y_1]
        bound = hybrid_bound(
            length, redundancy, radius, direction_distance
        )
        if bound is not None:
            eligible_directions.append((y_1, direction_distance, bound))

    line_checks = 0
    minimum_slack = None
    maximum_slopes = 0
    for y_1, direction_distance, bound in eligible_directions:
        for y_0 in syndromes:
            slope_count = 0
            for gamma in range(modulus):
                target = add(y_0, scale(gamma, y_1, modulus), modulus)
                transverse = any(
                    not (
                        y_0 in support_spans[selected]
                        and y_1 in support_spans[selected]
                    )
                    for selected in supports_by_syndrome.get(target, ())
                )
                slope_count += transverse

            assert slope_count <= bound, (
                modulus,
                length,
                redundancy,
                radius,
                y_0,
                y_1,
                direction_distance,
                slope_count,
                bound,
            )
            line_checks += 1
            maximum_slopes = max(maximum_slopes, slope_count)
            slack = bound - slope_count
            minimum_slack = slack if minimum_slack is None else min(
                minimum_slack, slack
            )

    return {
        "q": modulus,
        "N": length,
        "R": redundancy,
        "t": radius,
        "eligible_directions": len(eligible_directions),
        "line_checks": line_checks,
        "max_slopes": maximum_slopes,
        "minimum_slack": minimum_slack,
    }


def family_expected_distance(m, exact_weight):
    if exact_weight <= 24 * m:
        return 36 * m + 1
    if exact_weight < 26 * m:
        return 2 * exact_weight - 12 * m
    return 40 * m


def family_expected_denominator(m, exact_weight):
    if exact_weight <= 24 * m:
        return (
            exact_weight * exact_weight
            - 80 * m * exact_weight
            + 1440 * m * m
            + 40 * m
        )
    if exact_weight < 26 * m:
        return exact_weight * exact_weight - 480 * m * m
    return (40 * m - exact_weight) ** 2


def check_family_all_weights(maximum_m=200):
    for m in range(1, maximum_m + 1):
        length = 90 * m
        redundancy = 86 * m
        kappa = 4 * m
        radius = 31 * m
        direction_distance = 50 * m
        punctured_length = 40 * m
        punctured_distance = 36 * m + 1

        assert length == redundancy + kappa
        assert (length - radius) ** 2 == 3481 * m * m
        assert length * (length - direction_distance) == 3600 * m * m
        assert (length - radius) ** 2 < length * (length - direction_distance)
        old_denominator = (
            punctured_distance * punctured_length
            - 2 * radius * punctured_length
            + radius * radius
        )
        assert old_denominator == m * (40 - 79 * m) < 0
        assert 3 * radius == 93 * m > redundancy

        terms = hybrid_terms(
            length, redundancy, radius, direction_distance
        )
        exact_bound = 0
        for term in terms:
            exact_weight = term["e"]
            assert term["D"] == family_expected_distance(m, exact_weight)
            assert term["J"] == family_expected_denominator(m, exact_weight)
            assert term["J"] >= 81 * m * m > 0
            assert term["h"] == 19 * m + exact_weight
            assert term["cluster_factor"] <= 2
            if exact_weight >= 6 * m + 1:
                assert term["cluster_factor"] <= 1
            assert term["list_factor"] <= 4
            if exact_weight <= 6 * m:
                assert term["list_factor"] <= 1
            exact_bound += term["summand"]

        exact_bound_from_function = hybrid_bound(
            length, redundancy, radius, direction_distance
        )
        assert exact_bound == exact_bound_from_function
        assert exact_bound <= 112 * m + 2

        attained = terms[6 * m]
        assert attained["h"] == 25 * m
        assert attained["cluster_factor"] == 2
        assert attained["list_factor"] == 1
        assert attained["summand"] == 2


def check_family_interval_certificates(maximum_m=10_000):
    for m in range(1, maximum_m + 1):
        at_24m = hybrid_term(90 * m, 86 * m, 31 * m, 50 * m, 24 * m)
        at_24m_plus_1 = hybrid_term(
            90 * m, 86 * m, 31 * m, 50 * m, 24 * m + 1
        )
        at_31m = hybrid_term(90 * m, 86 * m, 31 * m, 50 * m, 31 * m)

        assert at_24m["J"] == 96 * m * m + 40 * m
        assert at_24m_plus_1["J"] == 96 * m * m + 48 * m + 1
        assert at_31m["J"] == 81 * m * m

        # Discrete differences certify the monotonicity used at each endpoint.
        assert 2 * (24 * m - 1) + 1 - 80 * m < 0
        assert 2 * (24 * m + 1) + 1 > 0
        assert -2 * (40 * m - 31 * m) + 1 < 0

        low_endpoint = 6 * m
        low_certificate = (
            2 * low_endpoint * low_endpoint
            - 120 * m * low_endpoint
            + 1440 * m * m
            + 40 * m
        )
        assert low_certificate == 792 * m * m + 40 * m > 0
        assert 4 * (6 * m - 1) + 2 - 120 * m < 0

        first_endpoint = 24 * m
        global_certificate = (
            5 * first_endpoint * first_endpoint
            - 360 * m * first_endpoint
            + 5760 * m * m
            + 160 * m
        )
        assert global_certificate == 160 * m > 0
        assert 10 * (24 * m - 1) + 5 - 360 * m < 0

        for exact_weight in (24 * m + 1, 26 * m - 1):
            effective_distance = 2 * exact_weight - 12 * m
            denominator = exact_weight * exact_weight - 480 * m * m
            left = (
                5 * denominator
                - 40 * m * (effective_distance - exact_weight)
            )
            right = 5 * (exact_weight - 24 * m) * (
                exact_weight + 16 * m
            )
            assert left == right > 0

        assert 40 * m < 5 * (40 * m - 31 * m)
        assert 2 * (6 * m + 1) + 4 * (25 * m) == 112 * m + 2


def check_complementary_wall_formulas(maximum_length=24):
    nonpositive_cases = 0
    for length in range(2, maximum_length + 1):
        for redundancy in range(1, length):
            for direction_distance in range(1, redundancy + 1):
                punctured_length = length - direction_distance
                punctured_distance = redundancy + 1 - direction_distance
                for radius in range(redundancy):
                    if radius >= punctured_length:
                        continue
                    for exact_weight in range(radius + 1):
                        term = hybrid_term(
                            length,
                            redundancy,
                            radius,
                            direction_distance,
                            exact_weight,
                        )
                        raw_distance = (
                            direction_distance
                            + 2 * exact_weight
                            - 2 * radius
                        )
                        if term["D"] == punctured_length:
                            assert term["J"] == (
                                punctured_length - exact_weight
                            ) ** 2
                            assert term["J"] > 0
                            continue

                        if raw_distance <= punctured_distance:
                            assert term["D"] == punctured_distance
                            assert term["J"] == (
                                exact_weight * exact_weight
                                - 2 * punctured_length * exact_weight
                                + punctured_length * punctured_distance
                            )
                            wall = "punctured"
                        else:
                            assert punctured_distance < raw_distance < punctured_length
                            assert term["D"] == raw_distance
                            assert term["J"] == (
                                exact_weight * exact_weight
                                - punctured_length
                                * (2 * radius - direction_distance)
                            )
                            wall = "mixed"

                        if term["J"] <= 0:
                            nonpositive_cases += 1
                            if wall == "punctured":
                                assert raw_distance <= punctured_distance
                            else:
                                assert punctured_distance < raw_distance < punctured_length
                                assert exact_weight * exact_weight <= (
                                    punctured_length
                                    * (2 * radius - direction_distance)
                                )
    assert nonpositive_cases > 0
    return nonpositive_cases


def polynomial_from_roots(roots, modulus):
    coefficients = [1]
    for root in roots:
        updated = [0] * (len(coefficients) + 1)
        for degree, coefficient in enumerate(coefficients):
            updated[degree] = (updated[degree] - root * coefficient) % modulus
            updated[degree + 1] = (updated[degree + 1] + coefficient) % modulus
        coefficients = updated
    return coefficients


def polynomial_value(coefficients, point, modulus):
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * point + coefficient) % modulus
    return value


def check_actual_weighted_rs_realization():
    modulus = 97
    m = 1
    length = 90
    redundancy = 86
    kappa = 4
    points = list(range(length))
    weights = [point + 1 for point in points]
    columns = parity_columns(modulus, length, redundancy, weights)
    zero_syndrome = (0,) * redundancy

    assert matrix_rank(
        [tuple(column[degree] for column in columns) for degree in range(redundancy)],
        modulus,
    ) == redundancy

    omega = []
    for index, point in enumerate(points):
        derivative = 1
        for other in points:
            if other != point:
                derivative = derivative * (point - other) % modulus
        omega.append(pow(weights[index] * derivative % modulus, -1, modulus))

    kernel_basis = [
        tuple(
            omega[index] * pow(point, degree, modulus) % modulus
            for index, point in enumerate(points)
        )
        for degree in range(kappa)
    ]
    assert matrix_rank(kernel_basis, modulus) == kappa
    assert all(
        syndrome(vector, columns, modulus) == zero_syndrome
        for vector in kernel_basis
    )

    t_0 = tuple(range(40))
    t_0_set = set(t_0)
    direction_support = tuple(range(40, 90))
    polynomial = polynomial_from_roots(t_0, modulus)
    assert len(polynomial) == 41
    assert polynomial[-1] == 1

    f_values = [
        polynomial_value(polynomial, point, modulus) for point in points
    ]
    assert support(f_values) == direction_support
    direction_lift = tuple(
        omega[index] * f_values[index] % modulus for index in range(length)
    )
    assert weight(direction_lift) == 50 * m
    y_1 = syndrome(direction_lift, columns, modulus)
    assert y_1 != zero_syndrome

    punctured_kernel_basis = [
        tuple(vector[index] for index in t_0) for vector in kernel_basis
    ]
    assert matrix_rank(punctured_kernel_basis, modulus) == kappa

    s_set = set(range(6))
    b_1 = set(range(40, 65))
    b_2 = set(range(65, 90))
    gamma_1, gamma_2 = 1, 2

    punctured_word = tuple(1 if index in s_set else 0 for index in range(length))
    u = list(punctured_word)
    for index in b_1:
        u[index] = -gamma_1 * direction_lift[index] % modulus
    for index in b_2:
        u[index] = -gamma_2 * direction_lift[index] % modulus
    u = tuple(u)

    c_1 = vector_sum(u, scale(gamma_1, direction_lift, modulus), modulus)
    c_2 = vector_sum(u, scale(gamma_2, direction_lift, modulus), modulus)
    assert set(support(c_1)) == s_set | b_2
    assert set(support(c_2)) == s_set | b_1
    assert weight(c_1) == weight(c_2) == 31 * m

    y_0 = syndrome(u, columns, modulus)
    assert syndrome(c_1, columns, modulus) == add(
        y_0, scale(gamma_1, y_1, modulus), modulus
    )
    assert syndrome(c_2, columns, modulus) == add(
        y_0, scale(gamma_2, y_1, modulus), modulus
    )

    for witness in (c_1, c_2):
        selected_columns = [columns[index] for index in support(witness)]
        assert matrix_rank(selected_columns, modulus) == len(selected_columns)
        assert matrix_rank(selected_columns + [y_1], modulus) == (
            len(selected_columns) + 1
        )

    puncture_1 = tuple(c_1[index] for index in t_0)
    puncture_2 = tuple(c_2[index] for index in t_0)
    expected_puncture = tuple(punctured_word[index] for index in t_0)
    assert puncture_1 == puncture_2 == expected_puncture
    assert weight(expected_puncture) == 6 * m
    assert matrix_rank(
        punctured_kernel_basis + [expected_puncture], modulus
    ) == kappa + 1

    term = hybrid_terms(length, redundancy, 31, 50)[6]
    assert term["h"] == 25
    assert term["cluster_factor"] == 2
    assert term["list_factor"] == 1
    assert term["summand"] == 2

    # The degree-40 leading term cannot be changed by a degree-<4 kernel
    # polynomial; the standard root bound therefore certifies d=50.
    assert len(polynomial) - 1 == 40
    assert max(range(kappa)) < 40
    assert len(t_0_set) == 40 and len(direction_support) == 50

    return {
        "q": modulus,
        "m": m,
        "N": length,
        "R": redundancy,
        "kernel_dimension": kappa,
        "direction_weight": weight(direction_lift),
        "witness_weights": (weight(c_1), weight(c_2)),
        "punctured_weight": weight(expected_puncture),
    }


def main():
    expected = {
        (5, 4, 2, 1): (600, 0),
        (5, 5, 2, 1): (600, 0),
        (5, 5, 3, 1): (15_500, 1),
        (5, 5, 4, 2): (112_500, 2),
    }
    rows = []
    for parameters, (line_checks, minimum_slack) in expected.items():
        row = exhaustive_chart(*parameters)
        assert row["line_checks"] == line_checks
        assert row["minimum_slack"] == minimum_slack
        rows.append(row)

    check_family_all_weights()
    check_family_interval_certificates()
    wall_cases = check_complementary_wall_formulas()
    realization = check_actual_weighted_rs_realization()

    print("object: low-direction hybrid exact-weight compiler")
    for row in rows:
        print(
            "exhaustive "
            f"F_{row['q']} (N,R,t)=({row['N']},{row['R']},{row['t']}): "
            f"directions={row['eligible_directions']}, "
            f"line_checks={row['line_checks']}, "
            f"max_slopes={row['max_slopes']}, "
            f"minimum_slack={row['minimum_slack']}"
        )
    print("strict family all exact weights, m=1..200: PASS")
    print("strict family interval identities, m=1..10000: PASS")
    print(
        "complementary wall partition, integer charts N<=24: "
        f"PASS ({wall_cases} nonpositive cases)"
    )
    print(f"actual weighted-RS realization: {realization}")
    print("status: PASS")


if __name__ == "__main__":
    main()
