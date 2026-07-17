#!/usr/bin/env sage
"""Exact GF(2^37) replay of the fixed-basis cap-20 counterexample.

This is the j=20 specialization of the five-pencil family.  It verifies a
complete declared rank-nine selector with 21 full-weight masks through one
fixed eight-row K0 basis.  It does not exhaust the ambient bad-slope set or
instantiate the KoalaBear domain.
"""

import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


degree = ZZ(37)
F = GF(2 ** degree, name="u")
g = F.multiplicative_generator()
require(g.multiplicative_order() == 2 ** degree - 1,
        "chosen field element is not primitive")

j = ZZ(20)
n = j + 14
k = ZZ(13)
R = n - k
A = n - j
require((n, k, R, j, A, R - j) == (34, 13, 21, 20, 14, 1),
        "toy row drift")

a = F(0)
b = F(1)
B_size = j + 12
ratio_exponents = [ZZ(2) ** index for index in range(B_size)]
require(sum(ratio_exponents) == 2 ** B_size - 1 < g.multiplicative_order(),
        "binary exponent range wrapped")
ratios = [g ** exponent for exponent in ratio_exponents]
B_points = [1 / (1 - ratio) for ratio in ratios]
D = [a, b] + B_points
require(len(D) == n and len(set(D)) == n, "domain collision")
require(all((b - B_points[i]) / (a - B_points[i]) == ratios[i]
            for i in range(B_size)), "point-ratio identity failed")

# Every subset has a unique binary exponent sum, and the largest possible
# sum is below the primitive element's order.  Hence all subset products,
# in particular all twelve-subset products, are injective without enumerating
# the enormous C(32,12) family.
require(ratio_exponents == [2 ** index for index in range(B_size)],
        "binary exponent basis drift")

lambdas = []
for point in D:
    denominator = prod(point - other for other in D if other != point)
    require(denominator != 0, "parity denominator vanished")
    lambdas.append(1 / denominator)

H = matrix(F, R, n,
           lambda row, column: lambdas[column] * D[column] ** row)
require(H.rank() == R, "parity check lost rank")

PR = PolynomialRing(F, "X")
X = PR.gen()


def root_polynomial(indices):
    return prod(X - B_points[index] for index in indices)


cores = [
    (3, 5, 6, 7, 9, 11, 13, 16, 17, 20, 21),
    (0, 2, 3, 6, 7, 8, 9, 10, 12, 13, 19),
    (1, 2, 4, 6, 7, 8, 10, 15, 17, 20, 21),
    (2, 3, 5, 9, 11, 12, 13, 14, 19, 20, 21),
    (0, 1, 2, 5, 6, 12, 14, 15, 18, 20, 21),
]
require(all(len(core) == len(set(core)) == 11 for core in cores),
        "core size drift")
require(set.intersection(*(set(core) for core in cores)) == set(),
        "cores gained common point")

root_sets = []
pencil_offsets = []
for core in cores:
    pencil_offsets.append(len(root_sets))
    for moving_root in range(B_size):
        if moving_root not in core:
            root_sets.append(tuple(sorted(core + (moving_root,))))
require(len(root_sets) == len(set(root_sets)) == 5 * (j + 1),
        "five-pencil size drift")

code_polynomials = []
slopes = []
errors = []
supports = []
zero_masks = []

epsilon_1 = vector(F, [1, 0] + [0] * B_size)
epsilon_2 = vector(F, [0, 1] + [0] * B_size)
y_0 = H * epsilon_1
y_1 = H * epsilon_2
require(matrix(F, [y_0, y_1]).rank() == 2,
        "syndrome line degenerated")

for root_set in root_sets:
    p = root_polynomial(root_set)
    q = p / p(a)
    gamma = q(b)
    codeword = vector(F, [q(point) for point in D])
    sparse_word = epsilon_1 + gamma * epsilon_2
    error = sparse_word - codeword
    support = tuple(index for index in range(B_size)
                    if index not in set(root_set))

    require(q.degree() == k - 1 and q(a) == 1,
            "code polynomial normalization failed")
    require(H * codeword == 0, "degree-12 evaluation left RS code")
    require(H * error == y_0 + gamma * y_1,
            "selected error left syndrome line")
    require(error.hamming_weight() == j, "deficit is not zero")
    require(tuple(index for index, value in enumerate(error[2:])
                  if value != 0) == support, "actual support drift")

    locator = root_polynomial(support)
    M_times_locator = sum(
        lambdas[index] * sparse_word[index] * locator(D[index])
        for index in range(n)
    )
    H2_times_locator = lambdas[1] * locator(b)
    chosen_minor = lambdas[0] * a + gamma * lambdas[1] * b
    require(M_times_locator == 0, "regular Pade equation failed")
    require(H2_times_locator != 0, "same-support noncontainment failed")
    require(chosen_minor == lambdas[1] * gamma != 0,
            "fixed regular chart failed")

    support_columns = [2 + index for index in support]
    require(H.matrix_from_columns(support_columns).rank() == j,
            "support image lost MDS rank")
    require(H.matrix_from_columns(support_columns + [1]).rank() == j + 1,
            "transversality failed")

    code_polynomials.append(q)
    slopes.append(gamma)
    errors.append(error)
    supports.append(support)
    zero_masks.append(root_set)

require(len(set(slopes)) == len(slopes), "declared slopes collided")
require(len(set(supports)) == len(supports), "selected supports collided")

raw_rank = matrix(F, errors).rank()
affine_rank = matrix(F, [error - errors[0]
                         for error in errors[1:]]).rank()
require((affine_rank, raw_rank) == (9, 10), "selector rank tuple drift")

basis_indices = []
for offset in pencil_offsets:
    basis_indices.extend([offset, offset + 1])
carrier = set().union(*(set(support) for support in supports))
basis_carrier = set().union(*(set(supports[index])
                              for index in basis_indices))
require(carrier == basis_carrier == set(range(B_size)),
        "ten supports no longer recover carrier")
N_V = ZZ(len(carrier))
nu = N_V - R
require((N_V, nu) == (32, 11), "carrier excess drift")

# Build K0 from affine differences whose syndrome is killed by subtracting
# the first nonzero syndrome direction.
direction = errors[1] - errors[0]
slope_direction = slopes[1] - slopes[0]
kernel_residuals = []
for index in range(2, len(errors)):
    coefficient = (slopes[index] - slopes[0]) / slope_direction
    residual = (errors[index] - errors[0]) - coefficient * direction
    require(H * residual == 0, "residual did not enter kernel")
    kernel_residuals.append(residual)
K0 = matrix(F, kernel_residuals).row_space().basis_matrix()
require(K0.rank() == 8, "K0 rank drift")

# K0 coordinates on the carrier B are columns 2,...,33 of the full word.
K0_carrier = K0.matrix_from_columns(list(range(2, n)))
core_ranks = [
    K0_carrier.matrix_from_columns(list(core)).rank()
    for core in cores
]
require(core_ranks == [8, 8, 8, 8, 8],
        "a fixed core lost K0 row rank eight")

first_core_matrix = K0_carrier.matrix_from_columns(list(cores[0]))
pivot_positions = list(first_core_matrix.pivots())
fixed_basis = tuple(cores[0][position] for position in pivot_positions)
require(len(fixed_basis) == 8, "fixed core basis size drift")
first_pencil_masks = zero_masks[:j + 1]
fixed_basis_multiplicity = sum(
    set(fixed_basis).issubset(set(mask)) for mask in first_pencil_masks
)
require(fixed_basis_multiplicity == j + 1 == 21,
        "fixed basis did not occur in all 21 pencil masks")

# Unique noncontained radius-j witness arithmetic: degree <=12 gives at most
# twelve roots on B, and the two sparse coordinates give at most two more
# agreements.  Radius j requires A=14 agreements, hence exactly (12,2).
agreement_pairs = [
    (roots_B, agreements_E)
    for roots_B in range(13)
    for agreements_E in range(3)
    if roots_B + agreements_E >= A
]
require(agreement_pairs == [(12, 2)], "unique-witness arithmetic drift")

payload = {
    "schema": "rs-mca-m1-kb-branch3-rank9-fixed-basis-fibre-v1-sage",
    "status": "PASS",
    "classification": "COUNTEREXAMPLE_TO_GENERIC_LOCAL_UNIFORM_FIXED_BASIS_CAP20",
    "field": {
        "cardinality": ZZ(F.cardinality()),
        "degree": degree,
        "generator_order": ZZ(g.multiplicative_order()),
    },
    "row": {"n": n, "k": k, "R": R, "j": j, "A": A},
    "selector": {
        "declared_slope_count": ZZ(len(slopes)),
        "distinct_slope_count": ZZ(len(set(slopes))),
        "complete_on_declared_Gamma": True,
        "declared_Gamma_exhausts_full_bad_set": False,
        "unique_noncontained_witness_per_slope": True,
        "all_deficits_zero": True,
        "affine_difference_rank": ZZ(affine_rank),
        "raw_witness_rank": ZZ(raw_rank),
    },
    "carrier": {
        "N_V": N_V,
        "nu": nu,
        "kappa_star": nu,
        "ten_basis_supports_recover_carrier": True,
    },
    "fixed_basis": {
        "core_restriction_ranks": core_ranks,
        "basis_indices_in_B": list(fixed_basis),
        "pencil_mask_count": ZZ(len(first_pencil_masks)),
        "multiplicity": ZZ(fixed_basis_multiplicity),
        "uniform_cap20_refuted": True,
    },
    "scope_guards": {
        "generic_local_implication_refuted": True,
        "koalabear_domain_instantiated": False,
        "deployed_aggregate_tail_refuted": False,
        "ledger_movement": 0,
    },
}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"),
                       default=int)
payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
print(json.dumps(payload, sort_keys=True, default=int))
