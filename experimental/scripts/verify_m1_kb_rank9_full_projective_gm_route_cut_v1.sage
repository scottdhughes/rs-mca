#!/usr/bin/env sage
"""Independent Sage replay of the full-projective rank-nine route cut."""

from itertools import combinations
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_hash(value):
    data = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
        default=int,
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-full-projective-gm-route-cut-v1/"
    "m1_kb_rank9_full_projective_gm_route_cut_v1.json"
)

F2 = GF(2)
S = PolynomialRing(F2, "x")
x = S.gen()
field_modulus = x^138 + x^8 + x^7 + x + 1
require(field_modulus.is_irreducible(), "ambient modulus is reducible")
F = GF(2^138, name="alpha", modulus=field_modulus)
alpha = F.gen()

q = ZZ(2)^23
v = alpha^((F.cardinality() - 1) // (q - 1))
require(v^(q - 1) == 1, "power generator left the base field")
require(v^((q - 1) // 47) != 1, "base generator lost factor 47")
require(v^((q - 1) // 178481) != 1, "base generator lost factor 178481")
require(all(alpha^(q^e) != alpha for e in (1, 2, 3)),
        "alpha lies in a proper intermediate field")
require(alpha^(q^6) == alpha, "alpha left the ambient field")

a = F(0)
b = F(1)
ratio_exponents = [ZZ(2)^index for index in range(22)]
ratios = [v^exponent for exponent in ratio_exponents]
moving_points = [1 / (1 - ratio) for ratio in ratios]
c = v
D = [a, b] + moving_points + [c]
require(len(D) == len(set(D)) == 25, "domain collision")
require(all(point^q == point for point in D), "domain left the base field")
require(c not in [a, b] + moving_points, "new point collided with old domain")
require(all((b - moving_points[i]) / (a - moving_points[i]) == ratios[i]
            for i in range(22)), "point-to-ratio convention drift")

all_twelve_sums = {
    sum(ratio_exponents[index] for index in subset)
    for subset in combinations(range(22), 12)
}
require(len(all_twelve_sums) == binomial(22, 12),
        "12-subset products lost injectivity")

n = ZZ(25)
k = ZZ(13)
R = n - k
j = ZZ(11)
A = n - j
require((R, j, A, R - j) == (12, 11, 14, 1), "row drift")

lambdas = []
for point in D:
    denominator = prod(point - other for other in D if other != point)
    require(denominator != 0, "dual denominator vanished")
    lambdas.append(1 / denominator)
require(all(value^q == value for value in lambdas), "dual weight left base field")

H = matrix(
    F,
    R,
    n,
    lambda row, column: lambdas[column] * D[column]^row,
)
require(H.rank() == R, "parity check lost rank")

PR = PolynomialRing(F, "X")
X = PR.gen()


def root_polynomial(indices):
    return prod(X - moving_points[index] for index in indices)


def coefficient_vector(polynomial, degree):
    return vector(F, [polynomial[index] for index in range(degree + 1)])


def integer_encoding(value):
    return ZZ(value.to_integer())


cores = [
    (3, 5, 6, 7, 9, 11, 13, 16, 17, 20, 21),
    (0, 2, 3, 6, 7, 8, 9, 10, 12, 13, 19),
    (1, 2, 4, 6, 7, 8, 10, 15, 17, 20, 21),
    (2, 3, 5, 9, 11, 12, 13, 14, 19, 20, 21),
    (0, 1, 2, 5, 6, 12, 14, 15, 18, 20, 21),
]
root_sets = []
for core in cores:
    for moving_root in range(22):
        if moving_root not in core:
            root_sets.append(tuple(sorted(core + (moving_root,))))
require(len(root_sets) == len(set(root_sets)) == 55,
        "five pencils do not give 55 root sets")

code_polynomials = []
gammas = []
for root_set in root_sets:
    polynomial = root_polynomial(root_set)
    polynomial /= polynomial(a)
    code_polynomials.append(polynomial)
    gammas.append(polynomial(b))
require(all(polynomial.degree() == 12 for polynomial in code_polynomials),
        "code polynomial degree drift")
require(all(gamma != 0 and gamma^q == gamma for gamma in gammas),
        "base gamma drift")
require(len(set(gammas)) == 55, "declared base slopes collided")
require(all(gammas[index] == prod(ratios[z] for z in root_sets[index])
            for index in range(55)), "subset-product formula failed")

f0 = vector(F, [1, 0] + [0] * 22 + [alpha])
g = vector(F, [0, 1] + [0] * 23)
f = f0 + alpha * g
y0 = H * f
y1 = H * g
require(matrix(F, [y0, y1]).rank() == 2, "syndrome line is degenerate")
zero_codeword_support = (0, 1, n - 1)
g_support = tuple(index for index, value in enumerate(g) if value != 0)
require(g_support == (1,), "g support drift")
require(y1 == H.column(1), "g syndrome left the b column")
zero_padded_support = zero_codeword_support + tuple(range(2, 10))
require(len(set(zero_padded_support)) == j, "canonical zero padding drift")
zero_padded_locator = prod(X - D[index] for index in zero_padded_support)
zero_padded_h2 = lambdas[1] * zero_padded_locator(b)
require(zero_padded_h2 == 0, "contained zero witness passed H2 ell")

frobenius_ranks = []
for e in (1, 2, 3):
    y0_frob = vector(F, [value^(q^e) for value in y0])
    y1_frob = vector(F, [value^(q^e) for value in y1])
    rank = matrix(F, [y0, y1, y0_frob, y1_frob]).rank()
    require(rank == 3, "syndrome plane descended at degree %s" % e)
    frobenius_ranks.append(ZZ(rank))
absolute_subfield_degrees = [1, 2, 3, 6, 23, 46, 69]
absolute_frobenius_ranks = []
for degree in absolute_subfield_degrees:
    y0_frob = vector(F, [value^(2^degree) for value in y0])
    y1_frob = vector(F, [value^(2^degree) for value in y1])
    rank = matrix(F, [y0, y1, y0_frob, y1_frob]).rank()
    require(rank == 3, "syndrome plane descended to GF(2^%s)" % degree)
    absolute_frobenius_ranks.append(ZZ(rank))

errors = []
supports = []
locators = []
etas = []

for root_set, polynomial, gamma in zip(root_sets, code_polynomials, gammas):
    eta = gamma + alpha
    sparse_word = f + eta * g
    require(tuple(index for index, value in enumerate(sparse_word) if value != 0)
            == zero_codeword_support,
            "zero-codeword discrepancy support drift")
    codeword = vector(F, [polynomial(point) for point in D])
    error = sparse_word - codeword
    moving_support = tuple(index for index in range(22)
                           if index not in set(root_set))
    support = moving_support + (22,)
    locator = root_polynomial(moving_support) * (X - c)

    require(all(eta^(q^e) != eta for e in (1, 2, 3)),
            "twisted slope entered a proper intermediate field")
    require(H * codeword == 0, "degree-12 word left RS")
    require(H * error == y0 + eta * y1, "error left syndrome line")
    require(error.hamming_weight() == j, "error weight drift")
    actual_support = tuple(
        [index for index, value in enumerate(error[2:24]) if value != 0]
        + ([22] if error[-1] != 0 else [])
    )
    require(actual_support == support, "actual support drift")
    require(all(sparse_word[index] != 0 for index in (0, 1, 24)),
            "tangent slope retained")
    require(locator.degree() == j and locator.is_monic() and locator.is_squarefree(),
            "locator shape drift")
    require(all(coefficient^q == coefficient for coefficient in locator),
            "locator coefficient left base field")

    recurrence = sum(
        lambdas[index] * sparse_word[index] * locator(D[index])
        for index in range(n)
    )
    h2_locator = lambdas[1] * locator(b)
    require(recurrence == 0 and h2_locator != 0,
            "regular noncontained recurrence failed")

    support_columns = [2 + index for index in moving_support] + [24]
    require(H.matrix_from_columns(support_columns).rank() == j,
            "support image lost MDS rank")
    require(H.matrix_from_columns(support_columns + [1]).rank() == j + 1,
            "y1 entered support image")

    errors.append(error)
    supports.append(support)
    locators.append(locator)
    etas.append(eta)

raw_rank = matrix(F, errors).rank()
affine_rank = matrix(F, [error - errors[0] for error in errors[1:]]).rank()
locator_rows = [coefficient_vector(locator, j) for locator in locators]
locator_rank = matrix(F, locator_rows).rank()
require((raw_rank, affine_rank, locator_rank) == (10, 9, 11),
        "rank triple drift")

basis_indices = [0, 1, 11, 12, 22, 23, 33, 34, 44, 45]
require(matrix(F, [errors[index] for index in basis_indices]).rank() == 10,
        "ten selected errors lost rank")
basis_carrier = set().union(*(set(supports[index]) for index in basis_indices))
carrier = set().union(*(set(support) for support in supports))
require(basis_carrier == carrier == set(range(23)), "carrier recovery drift")
require((len(carrier), len(carrier) - R) == (23, 11), "carrier excess drift")

gm_indices = [0, 1, 2, 11, 12, 22, 23, 33, 34, 44, 45]
gm_supports = [supports[index] for index in gm_indices]
gm_min_slack = []
gm_tight_count = 0
for size in range(1, 12):
    level = []
    for subset in combinations(range(11), size):
        intersection = set(gm_supports[subset[0]])
        for index in subset[1:]:
            intersection.intersection_update(gm_supports[index])
        slack = (j + 1) - (size + len(intersection))
        require(slack >= 0, "GM--MDS inequality failed")
        level.append(slack)
        gm_tight_count += (slack == 0)
    gm_min_slack.append(ZZ(min(level)))
require(gm_min_slack == [0, 0, 0, 2, 1, 2, 2, 2, 1, 1, 0],
        "GM slack profile drift")
gm_matrix = matrix(F, [locator_rows[index] for index in gm_indices])
require(gm_matrix.rank() == 11, "GM tuple locator rank drift")
gm_pivots = gm_matrix.pivots()
gm_determinant = gm_matrix.matrix_from_columns(gm_pivots).det()
require(gm_determinant != 0, "GM tuple minor vanished")

# The only nonzero agreement profiles before using alpha not in the base are
# (11,3), (12,2), and (12,3).  The note proves that every realization involving
# c is impossible; the surviving profile is (12,2) at a,b, and the subset
# product injection makes its witness unique.  The zero word has discrepancy
# support {a,b,c}, while supp(g)={b} is contained in that support; hence Hg is
# in the support-column span and the zero witness is same-support contained.
agreement_profiles = [
    [roots, agreements]
    for roots in range(13)
    for agreements in range(4)
    if roots + agreements >= A
]
require(agreement_profiles == [[11, 3], [12, 2], [12, 3]],
        "agreement profile arithmetic drift")
require((f + etas[0] * g).hamming_weight() == 3,
        "zero-codeword contained control drift")

certificate = json.loads(CERT_PATH.read_text(encoding="utf-8"))
control = certificate["exact_control"]

domain_ints = [integer_encoding(value) for value in D]
lambda_ints = [integer_encoding(value) for value in lambdas]
gamma_ints = [integer_encoding(value) for value in gammas]
eta_ints = [integer_encoding(value) for value in etas]
error_ints = [[integer_encoding(value) for value in row] for row in errors]
locator_ints = [
    [integer_encoding(locator[index]) for index in range(j + 1)]
    for locator in locators
]

require(control["field_tower"]["ambient_modulus"] ==
        "x^138 + x^8 + x^7 + x + 1", "certificate modulus drift")
require(control["field_tower"]["base_generator_integer_encoding"] == integer_encoding(v),
        "certificate base generator drift")
require(control["domain"]["domain_sha256"] == canonical_hash(domain_ints),
        "certificate domain hash drift")
require(control["domain"]["dual_weights_sha256"] == canonical_hash(lambda_ints),
        "certificate dual-weight hash drift")
require(control["construction"]["gamma_sha256"] == canonical_hash(gamma_ints),
        "certificate gamma hash drift")
require(control["construction"]["eta_sha256"] == canonical_hash(eta_ints),
        "certificate eta hash drift")
require(control["construction"]["errors_sha256"] == canonical_hash(error_ints),
        "certificate error hash drift")
require(control["construction"]["locators_sha256"] == canonical_hash(locator_ints),
        "certificate locator hash drift")
require(control["projective_syndrome_field"]["relative_frobenius_augmented_ranks"] ==
        list(map(int, frobenius_ranks)), "certificate projective ranks drift")
require(control["projective_syndrome_field"]["tested_absolute_proper_subfield_degrees"] ==
        absolute_subfield_degrees, "certificate absolute subfield list drift")
require(control["projective_syndrome_field"]["absolute_frobenius_augmented_ranks"] ==
        list(map(int, absolute_frobenius_ranks)),
        "certificate absolute projective ranks drift")
require(control["gm_fixed_domain_subtuple"]["minimum_slack_by_subset_size"] ==
        list(map(int, gm_min_slack)), "certificate GM slack drift")
require(control["gm_fixed_domain_subtuple"]["tight_inequality_count"] ==
        int(gm_tight_count), "certificate GM tight count drift")
require(control["gm_fixed_domain_subtuple"]["nonzero_minor"]["columns"] ==
        list(map(int, gm_pivots)), "certificate GM pivot drift")
require(control["gm_fixed_domain_subtuple"]["nonzero_minor"]
        ["determinant_integer_encoding"] == integer_encoding(gm_determinant),
        "certificate GM determinant drift")
require(control["unique_witness_proof"]["zero_codeword_discrepancy_support_indices"] ==
        list(zero_codeword_support), "certificate zero support drift")
require(control["unique_witness_proof"]["g_support_indices"] ==
        list(g_support), "certificate g support drift")
require(control["unique_witness_proof"]["canonical_padded_support_indices"] ==
        list(zero_padded_support), "certificate zero padding drift")
require(control["unique_witness_proof"]["canonical_padded_H2_locator_zero"] is True,
        "certificate zero H2 containment drift")

payload = {
    "schema": "rs-mca-m1-kb-rank9-full-projective-gm-route-cut-v1-sage",
    "status": "PASS",
    "classification": "GENERIC_FULL_PROJECTIVE_OR_GM_EMPTINESS_SHORTCUT_REFUTED",
    "field": {
        "base_cardinality": q,
        "ambient_cardinality": F.cardinality(),
        "ambient_modulus": str(field_modulus),
    },
    "row": {"n": n, "k": k, "R": R, "j": j, "A": A},
    "selector": {
        "declared_slope_count": len(etas),
        "all_degree_six_over_base": True,
        "raw_rank": raw_rank,
        "affine_rank": affine_rank,
        "locator_rank": locator_rank,
        "carrier_size": len(carrier),
        "carrier_excess": len(carrier) - R,
    },
    "relative_projective_frobenius_ranks": frobenius_ranks,
    "absolute_proper_subfield_degrees": absolute_subfield_degrees,
    "absolute_projective_frobenius_ranks": absolute_frobenius_ranks,
    "gm": {
        "indices": gm_indices,
        "inequality_count": 2^11 - 1,
        "minimum_slack_by_size": gm_min_slack,
        "locator_rank": gm_matrix.rank(),
        "minor_nonzero": True,
    },
    "scope_guards": {
        "declared_Gamma_exhausts_full_bad_set": False,
        "deployed_first_match_checked": False,
        "owner_or_payment_claimed": False,
        "ledger_movement": 0,
    },
}
print(json.dumps(payload, sort_keys=True, default=int))
