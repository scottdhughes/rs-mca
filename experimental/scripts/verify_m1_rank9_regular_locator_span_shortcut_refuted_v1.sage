#!/usr/bin/env sage
"""Independent Sage replay of the rank-nine locator-span route cut.

This exact GF(2^23) specialization checks the load-bearing finite control.
The companion note proves the parametric scalar-extension construction.
"""

from itertools import combinations
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# Frozen field and RS row.
F2 = GF(2)
S = PolynomialRing(F2, "x")
x = S.gen()
field_modulus = x ** 23 + x ** 5 + 1
F = GF(2 ** 23, name="u", modulus=field_modulus)
u = F.gen()

require(F.modulus() == field_modulus, "field modulus drift")
require(u.multiplicative_order() == 2 ** 23 - 1,
        "the frozen generator is not primitive")

n = ZZ(24)
k = ZZ(13)
R = n - k
j = ZZ(10)
A = n - j
require((R, j, A, R - j) == (11, 10, 14, 1), "row drift")

a = F(0)
b = F(1)
ratio_exponents = [ZZ(2) ** index for index in range(22)]
ratios = [u ** exponent for exponent in ratio_exponents]
B = [1 / (1 - ratio) for ratio in ratios]
D = [a, b] + B

require(len(D) == n and len(set(D)) == n, "domain collision")
require(all(point not in {a, b} for point in B), "moving point hit E")
require(all((b - B[i]) / (a - B[i]) == ratios[i] for i in range(22)),
        "point/ratio convention drift")
full_binary_sum = sum(ratio_exponents)
require(full_binary_sum == 2 ** 22 - 1 < u.multiplicative_order(),
        "binary exponent envelope drift")
all_twelve_sums = {
    sum(ratio_exponents[index] for index in subset)
    for subset in combinations(range(22), 12)
}
require(len(all_twelve_sums) == binomial(22, 12),
        "12-subset product map is not injective")

lambdas = []
for point in D:
    denominator = prod(point - other for other in D if other != point)
    require(denominator != 0, "parity denominator vanished")
    lambdas.append(1 / denominator)

H = matrix(
    F,
    R,
    n,
    lambda row, column: lambdas[column] * D[column] ** row,
)
require(H.rank() == R, "parity check lost rank")

PR = PolynomialRing(F, "X")
X = PR.gen()


def root_polynomial(indices):
    return prod(X - B[index] for index in indices)


def coefficient_vector(polynomial, degree):
    return vector(F, [polynomial[index] for index in range(degree + 1)])


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
        "five cores have a common point")
minimum_symmetric_difference = min(
    len(set(left).symmetric_difference(set(right)))
    for left, right in combinations(cores, 2)
)
require(minimum_symmetric_difference >= 8,
        "core separation drift")

root_sets = []
pencil_offsets = []
for core in cores:
    pencil_offsets.append(len(root_sets))
    for moving_root in range(22):
        if moving_root not in core:
            root_sets.append(tuple(sorted(core + (moving_root,))))
require(len(root_sets) == len(set(root_sets)) == 55,
        "five pencils do not give 55 distinct root sets")

root_polynomials = [root_polynomial(root_set) for root_set in root_sets]
code_polynomials = [polynomial / polynomial(a) for polynomial in root_polynomials]
slopes = [polynomial(b) for polynomial in code_polynomials]
require(all(polynomial.degree() == k - 1 for polynomial in code_polynomials),
        "code polynomial degree drift")
require(all(polynomial(a) == 1 for polynomial in code_polynomials),
        "normalization at a failed")
require(all(slope != 0 for slope in slopes), "tangent slope retained")
require(len(set(slopes)) == len(slopes), "slopes are not distinct")
for root_set, slope in zip(root_sets, slopes):
    require(slope == prod(ratios[index] for index in root_set),
            "subset-product slope formula failed")

epsilon_1 = vector(F, [1, 0] + [0] * 22)
epsilon_2 = vector(F, [0, 1] + [0] * 22)
y_0 = H * epsilon_1
y_1 = H * epsilon_2
require(matrix(F, [y_0, y_1]).rank() == 2,
        "syndrome line is degenerate")

errors = []
supports = []
locators = []

for root_set, polynomial, slope in zip(root_sets, code_polynomials, slopes):
    zero_set = set(root_set)
    support = tuple(index for index in range(22) if index not in zero_set)
    locator = root_polynomial(support)
    codeword = vector(F, [polynomial(point) for point in D])
    sparse_word = epsilon_1 + slope * epsilon_2
    error = sparse_word - codeword

    require(H * codeword == 0, "degree-12 evaluation left RS")
    require(H * error == y_0 + slope * y_1, "error left syndrome line")
    require(error.hamming_weight() == j, "error is not full weight")
    actual_support = tuple(
        index for index, value in enumerate(error[2:]) if value != 0
    )
    require(actual_support == support, "actual support differs from B\\Z")
    require(locator.degree() == j and locator.is_monic() and locator.is_squarefree(),
            "locator degree/splitting drift")
    require(all(locator(B[index]) == 0 for index in support),
            "locator missed a support point")

    # R-j=1.  In low-to-high coefficient order this is M(gamma) ell.
    M_times_locator = sum(
        lambdas[index] * sparse_word[index] * locator(D[index])
        for index in range(n)
    )
    H2_times_locator = lambdas[1] * locator(b)
    require(M_times_locator == 0, "M(gamma) ell failed")
    require(H2_times_locator != 0, "H2 ell noncontainment failed")

    # Fixed Hankel column 1: Delta(gamma)=lambda_b gamma.
    chosen_minor = lambdas[0] * a + slope * lambdas[1] * b
    require(chosen_minor == lambdas[1] * slope != 0,
            "fixed regular chart failed")

    support_columns = [2 + index for index in support]
    support_image = H.matrix_from_columns(support_columns)
    augmented = H.matrix_from_columns(support_columns + [1])
    require(support_image.rank() == j, "support columns lost MDS rank")
    require(augmented.rank() == j + 1, "y1 entered support image")

    errors.append(error)
    supports.append(support)
    locators.append(locator)

require(len(set(supports)) == 55, "supports are not distinct")
raw_rank = matrix(F, errors).rank()
affine_rank = matrix(F, [error - errors[0] for error in errors[1:]]).rank()
locator_rank = matrix(
    F, [coefficient_vector(locator, j) for locator in locators]
).rank()
require((affine_rank, raw_rank, locator_rank) == (9, 10, 11),
        "rank triple drift")

basis_indices = []
for offset in pencil_offsets:
    basis_indices.extend([offset, offset + 1])
basis_polynomial_matrix = matrix(
    F,
    [coefficient_vector(code_polynomials[index], k - 1) for index in basis_indices],
)
require(basis_polynomial_matrix.rank() == 10, "ten polynomial basis lost rank")
basis_pivots = basis_polynomial_matrix.pivots()
basis_minor = basis_polynomial_matrix.matrix_from_columns(basis_pivots).det()
require(basis_minor != 0, "ten-polynomial minor vanished")
expected_basis_minor = (
    u ** 22 + u ** 16 + u ** 15 + u ** 14 + u ** 12 + u ** 11
    + u ** 10 + u ** 7 + u ** 6 + u ** 5 + u ** 2 + 1
)
require(basis_minor == expected_basis_minor,
        "frozen ten-polynomial determinant drift")

require(matrix(F, [errors[index] for index in basis_indices]).rank() == 10,
        "ten selected errors lost rank")
basis_carrier = set().union(*(set(supports[index]) for index in basis_indices))
carrier = set().union(*(set(support) for support in supports))
require(basis_carrier == carrier == set(range(22)),
        "ten basis supports do not recover carrier")
N_V = ZZ(len(carrier))
nu = N_V - R
require((N_V, nu) == (22, 11), "carrier excess drift")

H_V = H.matrix_from_columns([2 + index for index in sorted(carrier)])
require(H_V.rank() == R and H_V.ncols() - H_V.rank() == 11,
        "restricted MDS dimensions drift")

# One pencil is the Lagrange basis {prod_{x in Q\\{z}}(X-x)}_{z in Q}.
one_pencil_locator_matrix = matrix(
    F, [coefficient_vector(locator, j) for locator in locators[:j + 1]]
)
require(one_pencil_locator_matrix.rank() == j + 1,
        "one-pencil Lagrange locator basis failed")

# Any nonzero degree<=12 witness at radius j has exactly 12 B-roots and
# agrees at both E points.  The subset-product injection then makes it unique.
agreement_pairs = [
    (roots_B, agreements_E)
    for roots_B in range(13)
    for agreements_E in range(3)
    if roots_B + agreements_E >= A
]
require(agreement_pairs == [(12, 2)], "unique-witness arithmetic drift")
require((epsilon_1 + slopes[0] * epsilon_2).hamming_weight() == 2,
        "contained zero-codeword control drift")

# Exact integer identities behind the parametric family.
for radius in [10, 11, 17, 100, 1000]:
    n_family = radius + 14
    R_family = radius + 1
    B_size = radius + 12
    require(n_family - 13 == R_family, "family redundancy identity failed")
    require(B_size - R_family == 11, "family carrier excess failed")
    require(5 * (radius + 1) > 15, "family slope floor failed")
    require(radius + 1 > 10 or radius == 10,
            "family locator-rank identity failed")

payload = {
    "schema": "rs-mca-m1-rank9-regular-locator-span-shortcut-refuted-v1-sage",
    "status": "PASS",
    "classification": "COUNTEREXAMPLE_TO_GENERIC_LOCAL_RANK_TO_LOCATOR_SPAN",
    "field": {
        "cardinality": ZZ(F.cardinality()),
        "modulus": str(field_modulus),
        "generator_order": ZZ(u.multiplicative_order()),
    },
    "row": {"n": n, "k": k, "R": R, "j": j, "A": A},
    "five_pencils": {
        "cores": [list(core) for core in cores],
        "minimum_pairwise_symmetric_difference": minimum_symmetric_difference,
        "slope_count": ZZ(len(slopes)),
        "distinct_slope_count": ZZ(len(set(slopes))),
    },
    "selector": {
        "complete_on_declared_Gamma": True,
        "declared_Gamma_exhausts_full_bad_set": False,
        "ambient_noncontained_bad_slope_count": ZZ(binomial(22, 12)),
        "unique_noncontained_witness_per_slope": True,
        "rank_minimizing_because_unique": True,
        "all_full_weight_transverse_regular_residual": True,
        "affine_difference_rank_s_star": ZZ(affine_rank),
        "raw_witness_rank_t": ZZ(raw_rank),
        "locator_vector_rank": ZZ(locator_rank),
    },
    "rank_witness": {
        "basis_indices": basis_indices,
        "basis_polynomial_pivot_columns": list(basis_pivots),
        "basis_polynomial_minor": str(basis_minor),
        "one_pencil_locator_rank": ZZ(one_pencil_locator_matrix.rank()),
    },
    "carrier": {
        "N_V": N_V,
        "R": R,
        "nu": nu,
        "kappa_star": nu,
        "ten_basis_supports_recover_carrier": True,
    },
    "parametric_identity": {
        "for_every_j_at_least_10": True,
        "fixed_rank_tuple_s_t_nu": [9, 10, 11],
        "locator_rank": "j+1",
        "field_existence_proof_is_in_companion_note": True,
    },
    "scope_guards": {
        "generic_local_implication_refuted": True,
        "declared_Gamma_exhausts_full_bad_set": False,
        "full_bad_family_or_deployed_first_match_strengthened_statement_refuted": False,
        "koalabear_domain_instantiated": False,
        "project_owner_masks_checked": False,
        "koalabear_residual_refuted": False,
        "ledger_movement": 0,
    },
}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=int)
payload["payload_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
print(json.dumps(payload, sort_keys=True, default=int))
