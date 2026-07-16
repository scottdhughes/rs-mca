#!/usr/bin/env sage
"""Independent exact replay for the KoalaBear branch-2 rank/deep owner.

The toy row realizes the sharp t-slope branch-2 charge, checks the ambient
Hankel rank against actual nonzero error weight with a padded co-support, and
shows why raw rank drop without a bad incidence is not payable.
"""

from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch2-rank-deep-owner-v1/"
    "m1_kb_branch2_rank_deep_owner_v1.json"
)

F = GF(7)
D = [F(value) for value in range(7)]
n = len(D)
k = 1
R = n - k
A = 4
j = n - A
t = A - k
r0 = t - 1
A_deep = n - r0
assert (n, k, R, A, j, t, r0, A_deep) == (7, 1, 6, 4, 3, 3, 2, 5)
assert 3 * r0 <= R


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
    R,
    n,
    lambda row, column: weights[column] * D[column]^row,
)
assert H.rank() == R
assert H * vector(F, [1 for _ in D]) == 0


def hankel_matrix(syndrome):
    return matrix(
        F,
        t,
        j + 1,
        lambda row, column: syndrome[row + column],
    )


def explained_by_constant(word, support):
    return len({word[index] for index in support}) <= 1


def bad_supports(f, g, gamma, agreement):
    word = f + gamma * g
    records = []
    for support in combinations(range(n), agreement):
        if not explained_by_constant(word, support):
            continue
        jointly_contained = (
            explained_by_constant(f, support)
            and explained_by_constant(g, support)
        )
        if not jointly_contained:
            records.append(support)
    return records


# Sharp tangent-floor pair on three coordinates.
tangent_coordinates = [0, 1, 2]
sharp_slopes = [F(0), F(1), F(2)]
f = vector(F, n)
g = vector(F, n)
for index, gamma in zip(tangent_coordinates, sharp_slopes):
    f[index] = -gamma
    g[index] = 1

u = H * f
v = H * g

original_bad = []
deep_bad = []
branch2_slopes = []
ranks = {}
error_weights = {}
for gamma in F:
    word = f + gamma * g
    matrix_gamma = hankel_matrix(u + gamma * v)
    ranks[int(gamma)] = matrix_gamma.rank()
    error_weights[int(gamma)] = sum(value != 0 for value in word)
    original_supports = bad_supports(f, g, gamma, A)
    deep_supports = bad_supports(f, g, gamma, A_deep)
    if original_supports:
        original_bad.append(gamma)
    if deep_supports:
        deep_bad.append(gamma)
    if original_supports and matrix_gamma.rank() < t:
        branch2_slopes.append(gamma)

assert original_bad == sharp_slopes
assert deep_bad == sharp_slopes
assert branch2_slopes == sharp_slopes
assert all(ranks[int(gamma)] == r0 for gamma in sharp_slopes)
assert all(error_weights[int(gamma)] == r0 for gamma in sharp_slopes)


# Padded exact-A support: the actual error has two points, while the chosen
# co-support has three points and contains one zero-amplitude pad.
gamma = F(0)
word = f + gamma * g
actual_error_indices = [
    index for index, value in enumerate(word) if value != 0
]
exact_support = (0, 3, 4, 5)
co_support = tuple(
    index for index in range(n) if index not in exact_support
)
padded_zero_indices = sorted(
    set(co_support) - set(actual_error_indices)
)
assert actual_error_indices == [1, 2]
assert co_support == (1, 2, 6)
assert padded_zero_indices == [6]
assert exact_support in bad_supports(f, g, gamma, A)

matrix_gamma = hankel_matrix(H * word)
left = matrix(
    F,
    t,
    len(actual_error_indices),
    lambda row, column: (
        weights[actual_error_indices[column]]
        * word[actual_error_indices[column]]
        * D[actual_error_indices[column]]^row
    ),
)
right = matrix(
    F,
    len(actual_error_indices),
    j + 1,
    lambda row, column: D[actual_error_indices[row]]^column,
)
factorization = left * right
assert matrix_gamma == factorization
assert matrix_gamma.rank() == len(actual_error_indices) == r0

full_agreement_support = tuple(
    index for index in range(n) if index not in actual_error_indices
)
assert len(full_agreement_support) == A_deep
assert set(exact_support).issubset(full_agreement_support)
assert full_agreement_support in bad_supports(f, g, gamma, A_deep)


# Negative incidence control: a contained codeword pair has raw rank drop at
# every slope but no MCA-bad slope.
contained_f = vector(F, n)
contained_g = vector(F, n)
contained_rank_drop = []
contained_bad = []
for gamma in F:
    matrix_gamma = hankel_matrix(H * (contained_f + gamma * contained_g))
    if matrix_gamma.rank() < t:
        contained_rank_drop.append(gamma)
    if bad_supports(contained_f, contained_g, gamma, A):
        contained_bad.append(gamma)

assert contained_rank_drop == list(F)
assert contained_bad == []


artifact = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
assert artifact["schema"] == "rs-mca-m1-kb-branch2-rank-deep-owner-v1"
assert artifact["rank_drop_policy"]["rank_field"] == "AMBIENT_F"
assert artifact["rank_drop_policy"]["rank_threshold"] == 67472
assert artifact["rank_drop_policy"]["requires_actual_bad_incidence"] is True
assert artifact["rank_drop_policy"]["raw_algebraic_rank_drop_paid"] is False
assert artifact["rank_drop_policy"]["literal_first_match_residual_subset_of_envelope"] is True
assert artifact["exact_support_rank_bridge"]["rank_identity"] == (
    "rank_F(M_A(gamma))=min(t,|E_gamma|)"
)
assert artifact["deep_witness_lift"]["deep_agreement"] == 2029681
assert artifact["deep_witness_lift"]["noncontainment_persists_upward"] is True
assert artifact["deep_mca_owner"]["owner_id"] == "DEEP_MCA_RANK_DROP"
assert artifact["deep_mca_owner"]["upper_bound"] == 67472
assert artifact["deep_mca_owner"]["charge_sharp"] is True
assert artifact["branch2_first_match"]["branch2_local_policy_complete"] is True
assert artifact["branch2_first_match"]["literal_rank_drop_cell_subset_of_envelope"] is True
assert artifact["legacy_bridge_retirement"]["status"] == (
    "RETIRED_NOT_REQUIRED_FOR_DEPLOYED_BRANCH2"
)
assert artifact["ledger"]["branch2_closed"] is True
assert artifact["ledger"]["row_complete"] is False
assert artifact["ledger"]["U_2"] is None
assert artifact["ledger"]["U_Q"] is None
assert artifact["ledger"]["U_A"] is None

control = artifact["small_field_control"]
assert control["p"] == 7
assert control["branch2_slopes"] == [0, 1, 2]
assert control["branch2_count"] == 3
assert control["designed_co_support"] == [1, 2, 6]
assert control["designed_actual_error_support"] == [1, 2]
assert control["designed_padded_zero_points"] == [6]
assert control["factorization_exact"] is True
assert control["sharp_charge_realized"] is True
assert control["contained_raw_rank_drop_slopes"] == list(range(7))
assert control["contained_bad_slopes"] == []
assert control["raw_rank_drop_requires_actual_bad_incidence"] is True

print("M1_KB_BRANCH2_RANK_DEEP_OWNER_V1_SAGE_PASS")
print("parameters:", (n, k, A, j, t, r0, A_deep))
print("branch2 slopes:", [int(gamma) for gamma in branch2_slopes])
print("branch2 ranks:", {key: ranks[key] for key in (0, 1, 2)})
print("padded co-support / actual error:", co_support, actual_error_indices)
print("contained raw rank-drop slopes / bad slopes:", len(contained_rank_drop), 0)
