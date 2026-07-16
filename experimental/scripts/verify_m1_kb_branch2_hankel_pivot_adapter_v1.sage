#!/usr/bin/env sage
"""Exact Sage replay for the KoalaBear branch-2 Hankel pivot adapter.

The deployed claim is only the Paper-D finite-pivot subgate.  The small tower
control below proves that deterministic support-wise pivots, rank two, and
full projective syndrome field do not by themselves collapse the global
support union to one quadratic root.
"""

from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch2-hankel-pivot-adapter-v1/"
    "m1_kb_branch2_hankel_pivot_adapter_v1.json"
)

p = 7
B = GF(p)
F.<z> = GF(p^6)
K = F.subfield(2)
eta = F(K.gen())

# Weighted RS[F,D,k] with the full evaluation domain in the base field.
D = [F(value) for value in range(6)]
n = len(D)
k = 2
r = n - k
j = 2
t = r - j
assert (n, k, r, j, t) == (6, 2, 4, 2, 2)


def dual_weights(domain):
    weights = []
    for index, point in enumerate(domain):
        denominator = F(1)
        for other_index, other in enumerate(domain):
            if index != other_index:
                denominator *= point - other
        weights.append(denominator^-1)
    return weights


weights = dual_weights(D)
H = matrix(
    F,
    r,
    n,
    lambda row, column: weights[column] * D[column]^row,
)
assert H.rank() == r
assert H * vector(F, [1 for _ in D]) == 0
assert H * vector(F, D) == 0
columns = [H.column(index) for index in range(n)]

R.<X> = PolynomialRing(F)


def locator_coefficients(co_support):
    locator = prod(X - D[index] for index in co_support)
    assert locator.is_monic()
    assert locator.degree() == j
    return vector(F, [locator[degree] for degree in range(j + 1)])


def hankel_times_locator(syndrome, locator):
    return vector(
        F,
        [
            sum(
                syndrome[row + column] * locator[column]
                for column in range(j + 1)
            )
            for row in range(t)
        ],
    )


def explained_on_complement(word, co_support):
    locator = locator_coefficients(co_support)
    return hankel_times_locator(H * word, locator) == 0


def is_degree_less_than_k_evaluation(word):
    interpolation = R.lagrange_polynomial(
        [(D[index], word[index]) for index in range(n)]
    )
    return interpolation.degree() < k


# Distinct proper-quadratic slopes in the unique F_(7^2) subfield.
gamma1 = eta
gamma2 = eta + 1
assert gamma1 != gamma2
for gamma in (gamma1, gamma2):
    assert gamma^(p^2) == gamma
    assert gamma^p != gamma

# Two disjoint co-supports with target syndrome vectors in their parity spans.
T1 = (0, 1)
T2 = (2, 4)
assert set(T1).isdisjoint(T2)
error1 = vector(F, [1, 1, 0, 0, 0, 0])
error2 = vector(F, [0, 0, 1, 0, z, 0])
w1 = H * error1
w2 = H * error2
assert w1 == columns[0] + columns[1]
assert w2 == columns[2] + z * columns[4]

# Solve u+gamma_i*v=w_i and realize u,v as received-word syndromes.
v = (w1 - w2) / (gamma1 - gamma2)
u = w1 - gamma1 * v
assert u + gamma1 * v == w1
assert u + gamma2 * v == w2
f = H.solve_right(u)
g = H.solve_right(v)
assert H * f == u
assert H * g == v

# The received-pair syndrome space is rank two and is not defined over any
# proper subfield F_(7^e), e=1,2,3.
Y = matrix(F, [list(u), list(v)]).transpose()
assert Y.nrows() == r and Y.ncols() == 2
assert Y.rank() == 2
frobenius_augmented_ranks = {}
for e in (1, 2, 3):
    Y_e = Y.apply_map(lambda value: value^(p^e))
    augmented_rank = Y.augment(Y_e).rank()
    frobenius_augmented_ranks[e] = augmented_rank
    assert augmented_rank == 3

records = []
for co_support, gamma, error, expected_pivot in (
    (T1, gamma1, error1, 0),
    (T2, gamma2, error2, 1),
):
    locator = locator_coefficients(co_support)
    A_T = hankel_times_locator(u, locator)
    B_T = hankel_times_locator(v, locator)

    assert B_T != 0
    assert A_T + gamma * B_T == 0
    pivot = next(
        index for index, value in enumerate(B_T) if value != 0
    )
    assert pivot == expected_pivot
    assert all(B_T[index] == 0 for index in range(pivot))
    assert gamma == -A_T[pivot] / B_T[pivot]
    assert all(
        A_T[index] * B_T[pivot] - A_T[pivot] * B_T[index] == 0
        for index in range(t)
    )

    combined = f + gamma * g
    codeword = combined - error
    assert H * codeword == 0
    assert is_degree_less_than_k_evaluation(codeword)
    assert all(
        error[index] == 0
        for index in set(range(n)) - set(co_support)
    )
    assert all(error[index] != 0 for index in co_support)
    assert explained_on_complement(combined, co_support)
    assert not explained_on_complement(g, co_support)
    assert not (
        explained_on_complement(f, co_support)
        and explained_on_complement(g, co_support)
    )

    records.append(
        {
            "co_support": co_support,
            "gamma": gamma,
            "pivot": pivot,
        }
    )

# Recover roots from every size-two co-support without inserting the target
# slopes.  There are exactly two, and their least pivots differ.
support_roots = {}
support_pivots = {}
for co_support in combinations(range(n), j):
    locator = locator_coefficients(co_support)
    A_T = hankel_times_locator(u, locator)
    B_T = hankel_times_locator(v, locator)
    if B_T == 0:
        continue
    pivot = next(
        index for index, value in enumerate(B_T) if value != 0
    )
    if all(
        A_T[index] * B_T[pivot] - A_T[pivot] * B_T[index] == 0
        for index in range(t)
    ):
        support_roots[co_support] = -A_T[pivot] / B_T[pivot]
        support_pivots[co_support] = pivot

assert support_roots == {T1: gamma1, T2: gamma2}
assert support_pivots == {T1: 0, T2: 1}

artifact = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
control = artifact["two_root_control"]
assert control["domain"] == [0, 1, 2, 3, 4, 5]
assert control["co_supports"] == [[0, 1], [2, 4]]
assert control["agreement_supports"] == [
    [2, 3, 4, 5],
    [0, 1, 3, 5],
]
assert control["least_pivots"] == [0, 1]
assert control["exact_support_root_count"] == 2
assert control["frobenius_augmented_ranks"] == {
    "1": 3,
    "2": 3,
    "3": 3,
}
assert control["survives_rank_policy_proved"] is False
assert control["survives_branches_3_to_5_proved"] is False

scalar = artifact["scalarization_replay"]
assert scalar["scalar_stack_rank_equivalent_to_ambient_matrix"] is False
assert (
    scalar["scalar_replay_scan_order"]
    == "ROW_h_FIRST_THEN_BASIS_COMPONENT_i"
)

print("M1_KB_BRANCH2_HANKEL_PIVOT_ADAPTER_V1_SAGE_PASS")
print("parameters:", (p, n, k, r, j, t))
print(
    "supports/pivots:",
    [(record["co_support"], record["pivot"]) for record in records],
)
print("Frobenius augmented ranks:", frobenius_augmented_ranks)
print("exact support roots:", support_roots)
