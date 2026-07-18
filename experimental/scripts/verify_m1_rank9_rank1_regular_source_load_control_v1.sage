#!/usr/bin/env sage
"""Exact rank-one, rank-nine, regular-chart source-load countercontrol.

This is a record-level local implication control over GF(1009).  It is not a
complete selector for the full bad-slope family and is not a KoalaBear row.
"""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


F = GF(1009)
X = PolynomialRing(F, "X").gen()
D = [F(index) for index in range(50)]
n = 50
k = 10
R = 40
j = 36
A = 14
t = 4

H_poly = prod(X - F(root) for root in range(9))
require(
    [ZZ(value) for value in H_poly.list()]
    == [0, 969, 397, 71, 319, 251, 509, 546, 973, 1],
    "H coefficients drift",
)

epsilon_0_values = [
    0, 0, 0, 0, 230, 809, 909, 167, 329, 6, 949, 40, 120, 718,
    959, 773, 221, 213, 6, 437, 170, 847, 272, 394, 658, 167,
    934, 522, 326, 158, 253, 38, 917, 887, 190,
]
epsilon_1_values = [
    649, 436, 380, 511, 674, 815, 980, 44, 602, 931, 1001, 738,
    362, 196, 873, 443, 182, 446, 468, 33, 377, 706, 164, 792,
    122, 45, 955, 939, 598, 119, 294, 438, 84, 708, 782,
]
epsilon_0 = vector(F, [0] * 9 + epsilon_0_values + [0] * 6)
epsilon_1 = vector(F, [0] * 9 + epsilon_1_values + [0] * 6)
Sigma = set(epsilon_0.support()).union(epsilon_1.support())
require(Sigma == set(range(9, 44)) and len(Sigma) == 35 <= j,
        "source support drift")

rich_slopes = list(range(1, 22)) + [47, 75, 547, 623, 657, 806, 819, 864, 934, 989]
outlier_slopes = list(range(101, 109))
require(len(rich_slopes) == 31 and len(set(rich_slopes + outlier_slopes)) == 39,
        "slope inventory drift")

outlier_cores = [
    [1, 2, 3, 4, 5, 6, 7, 9, 11],
    [0, 1, 3, 4, 5, 6, 8, 9, 10],
    [0, 2, 3, 4, 7, 9, 10, 11, 12],
    [0, 2, 3, 4, 5, 6, 7, 10, 11],
    [0, 1, 3, 4, 6, 7, 8, 10, 12],
    [1, 2, 4, 7, 8, 9, 10, 11, 12],
    [1, 2, 3, 5, 8, 9, 10, 11, 12],
    [0, 2, 3, 4, 5, 8, 9, 11, 12],
]
outlier_source_zeros = [
    [26, 30, 34, 39, 41],
    [16, 20, 21, 32, 38],
    [13, 15, 36, 40, 42],
    [14, 22, 37, 41, 42],
    [17, 27, 28, 31, 37],
    [23, 24, 29, 33, 35],
    [19, 34, 35, 36, 40],
    [18, 25, 38, 39, 43],
]


def evaluate(polynomial):
    return vector(F, [polynomial(point) for point in D])


def root_polynomial(indices):
    return prod(X - D[index] for index in indices)


generator = matrix(F, [[point**degree for point in D] for degree in range(k)])
require(generator.rank() == k, "RS generator rank drift")
lambdas = [
    1 / prod(point - other for other in D if other != point)
    for point in D
]
parity = matrix(
    F,
    R,
    n,
    lambda row, column: lambdas[column] * D[column]**row,
)
require(parity.rank() == R and parity * generator.transpose() == 0,
        "RS parity check drift")
y_0 = parity * epsilon_0
y_1 = parity * epsilon_1
require(matrix(F, [y_0, y_1]).rank() == 2, "source syndrome line drift")

records = []
q_polynomials = []
for slope in rich_slopes:
    polynomial = F(slope) * H_poly
    error = epsilon_0 + F(slope) * epsilon_1 - evaluate(polynomial)
    records.append((slope, polynomial, error, "RICH"))

for slope, core, source_zeros in zip(
    outlier_slopes, outlier_cores, outlier_source_zeros
):
    q_poly = root_polynomial(core)
    polynomial = F(slope) * H_poly + q_poly
    error = epsilon_0 + F(slope) * epsilon_1 - evaluate(polynomial)
    require(
        set(index for index, value in enumerate(error) if value == 0)
        == set(core).union(source_zeros),
        "outlier zero support drift",
    )
    q_polynomials.append(q_poly)
    records.append((slope, polynomial, error, "OUTLIER"))

require(len(records) == 39, "record count drift")


def restricted_membership(values, support):
    restricted = generator.matrix_from_columns(list(support)).transpose()
    augmented = restricted.augment(
        matrix(F, len(support), 1, [values[index] for index in support])
    )
    return restricted.rank() == augmented.rank()


def locator_coefficients(support):
    locator = root_polynomial(support)
    require(locator.degree() == j, "locator degree drift")
    return vector(F, [locator[degree] for degree in range(j + 1)])


def moments(values):
    return [
        sum(lambdas[index] * values[index] * D[index]**degree
            for index in range(n))
        for degree in range(R)
    ]


moments_0 = moments(epsilon_0)
moments_1 = moments(epsilon_1)
M_0 = matrix(F, t, j + 1,
             lambda row, column: moments_0[row + column])
M_1 = matrix(F, t, j + 1,
             lambda row, column: moments_1[row + column])

expected_minors = [
    227, 590, 650, 178, 261, 275, 912, 144, 286, 933, 978, 630, 405,
    117, 896, 143, 611, 315, 604, 107, 787, 696, 826, 896, 959, 969,
    9, 207, 492, 655, 330, 91, 90, 189, 589, 789, 595, 120, 793,
]
regular_minors = []
supports = []
errors = []
for slope, polynomial, error, label in records:
    support = tuple(error.support())
    zero_support = tuple(index for index in range(n) if index not in support)
    require(len(support) == j and len(zero_support) == A,
            "record weight/agreement drift")
    require(parity * error == y_0 + F(slope) * y_1,
            "record syndrome incidence drift")
    require(parity * evaluate(polynomial) == 0, "explainer left RS code")
    contained_0 = restricted_membership(epsilon_0, zero_support)
    contained_1 = restricted_membership(epsilon_1, zero_support)
    require(not contained_0 and not contained_1,
            "an individual source became explainable on a support")
    ell = locator_coefficients(support)
    matrix_slope = M_0 + F(slope) * M_1
    require(matrix_slope * ell == 0, "regular Hankel equation failed")
    require(M_1 * ell != 0, "H2 locator equation vanished")
    minor = matrix_slope.matrix_from_columns([0, 1, 2, 3]).determinant()
    require(minor != 0, "fixed regular minor vanished")
    regular_minors.append(ZZ(minor))
    supports.append(support)
    errors.append(error)

require(regular_minors == expected_minors, "regular-minor list drift")
carrier = set().union(*(set(support) for support in supports))
require(carrier == set(range(n)), "carrier is not full domain")

raw_rank = matrix(F, errors).rank()
affine_space = matrix(F, [error - errors[0] for error in errors[1:]])
affine_rank = affine_space.rank()
require((affine_rank, raw_rank) == (9, 10), "rank tuple drift")

q_words = [evaluate(polynomial) for polynomial in q_polynomials]
K0 = matrix(F, q_words)
require(K0.rank() == 8, "K0 rank drift")
require(matrix(F, list(affine_space.rows()) + q_words).rank() == affine_rank,
        "K0 left affine direction space")
stack_rank = matrix(F, list(affine_space.rows()) + list(generator.rows())).rank()
intersection_rank = affine_rank + generator.rank() - stack_rank
require(intersection_rank == K0.rank() == 8,
        "affine/code intersection drift")

rich_errors = [error for _, _, error, label in records if label == "RICH"]
Z = {
    index for index in range(n)
    if all(error[index] == 0 for error in rich_errors)
}
require(Z == set(range(13)), "rich common-zero set drift")
plant = sorted(Z.intersection(Sigma))
outside_common = sorted(Z - Sigma)
require(plant == [9, 10, 11, 12] and outside_common == list(range(9)),
        "rank-one plant split drift")
require(len(plant) == t - 1 + 1, "plant-floor equality drift")

g_rows = [[word[index] for word in q_words] for index in sorted(Z)]
beta = ZZ(sum(
    matrix(F, [g_rows[index] for index in basis]).rank() == 8
    for basis in combinations(range(len(g_rows)), 8)
))
require(beta == 1197, "determinant basis mass drift")
E20 = beta * (len(rich_slopes) - 20)
require(E20 == 13167, "rank-one line weight drift")

for index in plant:
    require(epsilon_1[index] != 0, "plant gained infinity label")
    require(-epsilon_0[index] / epsilon_1[index] == 0,
            "plant source label drift")

tangent = {
    -epsilon_0[index] / epsilon_1[index]
    for index in Sigma
    if epsilon_1[index] != 0
}
selected_slopes = {F(slope) for slope in rich_slopes + outlier_slopes}
require(F(0) in tangent and not tangent.intersection(selected_slopes),
        "post-tangent slope inventory drift")
component_slopes = set()
H_values = evaluate(H_poly)
for index in set(range(n)) - Z:
    denominator = epsilon_1[index] - H_values[index]
    if denominator != 0:
        component_slopes.add(-epsilon_0[index] / denominator)
require(component_slopes == {F(0)}.union(F(slope) for slope in rich_slopes),
        "scalar-H component completeness drift")

print(
    "PASS",
    {
        "field": 1009,
        "records": len(records),
        "raw_rank": raw_rank,
        "affine_rank": affine_rank,
        "K0_rank": K0.rank(),
        "intersection_rank": intersection_rank,
        "beta": beta,
        "E20": E20,
        "plant": plant,
        "tangent_size": len(tangent),
        "all_regular_minors_nonzero": all(regular_minors),
    },
)
