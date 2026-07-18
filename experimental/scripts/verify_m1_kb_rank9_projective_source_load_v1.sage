#!/usr/bin/env sage
"""Independent GF(11) controls for the projective source-load route cut."""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


F = GF(11)
R.<X> = PolynomialRing(F)


def in_rs_restriction(values, support, domain, k):
    rows = [[domain[index]^degree for degree in range(k)] for index in support]
    augmented = [row + [values[index]] for row, index in zip(rows, support)]
    return Matrix(F, rows).rank() == Matrix(F, augmented).rank()


def coefficient_row(polynomial, width):
    coefficients = polynomial.list()
    return coefficients + [F(0)] * (width - len(coefficients))


def run_fixture(kind):
    if kind in {"RANK_TWO", "RANK_TWO_INFINITY"}:
        n, k, j = 10, 3, 6
    else:
        n, k, j = 9, 2, 6
    domain = [F(index) for index in range(n)]
    agreement = n - j
    t = agreement - k
    selected_slopes = [F(2), F(3), F(4)]
    cap = 2
    a_word = [F(0)] * n
    b_word = [F(0)] * n

    if kind == "RANK_TWO":
        P = X * (X - 2)
        Q = X - 2
        for index in range(3, n):
            a_word[index] = -P(domain[index])
            b_word[index] = -Q(domain[index])
        expected_tangent = {F(0), F(10)}
        expected_fibers = {"FINITE:0", "FINITE:10"}
        expected_rank = 2
    elif kind == "RANK_TWO_INFINITY":
        P = X - 2
        Q = (X - 2) * (X - 1)
        for index in range(3, n):
            a_word[index] = -P(domain[index])
            b_word[index] = -Q(domain[index])
        expected_tangent = {F(1)}
        expected_fibers = {"FINITE:1", "INFINITY"}
        expected_rank = 2
    elif kind == "RANK_ONE_FINITE":
        P = R(-1)
        Q = R(-1)
        for index in range(2, n):
            a_word[index] = F(1)
            b_word[index] = F(1)
        for slope in selected_slopes:
            a_word[ZZ(slope)] = -slope
        expected_tangent = {F(10)}
        expected_fibers = {"FINITE:10"}
        expected_rank = 1
    elif kind == "RANK_ONE_INFINITY":
        P = R(-5)
        Q = R(0)
        for index in range(2, n):
            a_word[index] = F(5)
        for slope in selected_slopes:
            a_word[ZZ(slope)] = -slope
            b_word[ZZ(slope)] = F(1)
        expected_tangent = {F(7), F(8), F(9)}
        expected_fibers = {"INFINITY"}
        expected_rank = 1
    else:
        raise RuntimeError("unknown fixture")

    epsilon_0 = [a_word[index] + P(domain[index]) for index in range(n)]
    epsilon_1 = [b_word[index] + Q(domain[index]) for index in range(n)]
    sigma = {
        index
        for index in range(n)
        if (epsilon_0[index], epsilon_1[index]) != (F(0), F(0))
    }
    require(len(sigma) <= j, "source support exceeds j")

    selected = []
    for slope in selected_slopes:
        word = [a_word[index] + slope * b_word[index] for index in range(n)]
        support = [index for index, value in enumerate(word) if value != 0]
        zero_support = [index for index in range(n) if index not in support]
        require(len(support) <= j, "selected word exceeds j")
        contained_0 = in_rs_restriction(epsilon_0, zero_support, domain, k)
        contained_1 = in_rs_restriction(epsilon_1, zero_support, domain, k)
        require(not (contained_0 and contained_1), "support-wise noncontainment failed")
        selected.append((slope, support))

    common_zero = [
        index
        for index in range(n)
        if (a_word[index], b_word[index]) == (F(0), F(0))
    ]
    moving_support = [index for index in range(n) if index not in common_zero]
    x_value = len(moving_support) - j
    require(x_value == 1, "fixture x value drift")
    require(len(common_zero) == agreement - x_value, "common-zero identity failed")

    generator_rows = [vector(F, [1, point]) for point in domain]
    basis_mass = sum(
        1
        for basis in combinations(common_zero, 2)
        if Matrix(F, [generator_rows[index] for index in basis]).rank() == 2
    )
    line_weight = basis_mass * (len(selected) - cap)
    require(line_weight > 0, "line weight is not positive")

    plant = sorted(set(common_zero).intersection(sigma))
    outside_common = sorted(set(common_zero).difference(sigma))
    require(len(plant) == agreement - x_value - len(outside_common), "plant identity failed")
    require(len(plant) >= t - x_value + 1 > 0, "positive plant floor failed")

    G = prod(X - domain[index] for index in outside_common)
    require(P % G == 0 and Q % G == 0, "forced common factor failed")
    reduced_P = P // G
    reduced_Q = Q // G
    pair_rank = Matrix(F, [coefficient_row(P, k), coefficient_row(Q, k)]).rank()
    reduced_rank = Matrix(
        F,
        [coefficient_row(reduced_P, k), coefficient_row(reduced_Q, k)],
    ).rank()
    require(pair_rank == reduced_rank == expected_rank, "polynomial-pair rank drift")
    reduced_cap = k - 1 - len(outside_common)
    require(reduced_cap == len(plant) + x_value - t - 1, "reduced degree identity failed")

    tangent_image = {
        -epsilon_0[index] / epsilon_1[index]
        for index in sigma
        if epsilon_1[index] != 0
    }
    require(tangent_image == expected_tangent, "tangent image drift")
    require(not tangent_image.intersection(selected_slopes), "tangent slope survived")

    fiber_counts = {}
    point_load = QQ(line_weight) / len(plant)
    load_sum = QQ(0)
    for index in plant:
        require(P(domain[index]) == epsilon_0[index], "P source coupling failed")
        require(Q(domain[index]) == epsilon_1[index], "Q source coupling failed")
        if epsilon_1[index] == 0:
            require(Q(domain[index]) == 0 and P(domain[index]) != 0, "infinity chart failed")
            fiber = "INFINITY"
        else:
            theta = -epsilon_0[index] / epsilon_1[index]
            require(P(domain[index]) + theta * Q(domain[index]) == 0, "finite chart failed")
            fiber = "FINITE:%s" % ZZ(theta)
        fiber_counts[fiber] = fiber_counts.get(fiber, 0) + 1
        load_sum += point_load
    require(set(fiber_counts) == expected_fibers, "projective fiber partition drift")
    require(load_sum == line_weight, "normalized source-load identity failed")

    if pair_rank == 1 and Q != 0:
        q_row = coefficient_row(Q, k)
        p_row = coefficient_row(P, k)
        pivot = next(index for index, value in enumerate(q_row) if value != 0)
        scalar = p_row[pivot] / q_row[pivot]
        require(-scalar in tangent_image, "rank-one finite zero slope is not tangent-owned")
        require(set(fiber_counts) == {"FINITE:%s" % ZZ(-scalar)}, "rank-one finite fiber split")
    elif pair_rank == 1:
        require(Q == 0 and set(fiber_counts) == {"INFINITY"}, "rank-one infinity drift")
    else:
        require(all(count <= reduced_cap for count in fiber_counts.values()), "rank-two root cap failed")
        require(len(outside_common) == 1, "rank-two control lost its forced factor")
        require(reduced_cap == 1, "rank-two control lost the injective regime")

    return {
        "kind": kind,
        "n": n,
        "k": k,
        "A": agreement,
        "j": j,
        "t": t,
        "x": x_value,
        "outside_common": len(outside_common),
        "plant": len(plant),
        "basis_mass": basis_mass,
        "line_weight": line_weight,
        "pair_rank": pair_rank,
        "reduced_cap": reduced_cap,
        "load_sum": load_sum,
    }


results = [
    run_fixture("RANK_ONE_FINITE"),
    run_fixture("RANK_ONE_INFINITY"),
    run_fixture("RANK_TWO"),
    run_fixture("RANK_TWO_INFINITY"),
]

print("M1 projective source-load GF(11) controls: PASS")
for result in results:
    print(
        "  %(kind)s: (n,k,A,j,t)=(%(n)s,%(k)s,%(A)s,%(j)s,%(t)s), "
        "x=%(x)s, c=%(outside_common)s, s=%(plant)s, beta=%(basis_mass)s, "
        "w=%(line_weight)s, rank=%(pair_rank)s, d_proj=%(reduced_cap)s, "
        "load=%(load_sum)s" % result
    )
print("  exact generic-local controls only; deployed source-load payment remains open")
