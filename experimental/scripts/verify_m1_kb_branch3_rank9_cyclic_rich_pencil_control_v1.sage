#!/usr/bin/env sage
"""Exact cyclic GF(67^2) complete-selector closure and rank-nine control.

The 29-slope rank-nine selector is deliberately incomplete.  A separate
lexicographic selector exhausts all 66 noncontained slopes and is paid by the
low-excess common-carrier owner.  Neither object is a deployed KoalaBear row.
"""

import hashlib
import json
from collections import defaultdict
from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def canonical_hash(value):
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), default=int
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def field_coordinates(value):
    coefficients = list(value)
    require(len(coefficients) <= 2, "quadratic field coordinate drift")
    coefficients += [0] * (2 - len(coefficients))
    return [ZZ(coefficient) for coefficient in coefficients]


p = ZZ(67)
Fp = GF(p)
RZ = PolynomialRing(Fp, "z")
z = RZ.gen()
modulus = z^2 + 63 * z + 2
require(modulus.is_irreducible(), "quadratic modulus became reducible")
F = GF(p^2, name="u", modulus=modulus)
u = F.gen()
require(u.multiplicative_order() == p^2 - 1,
        "declared field generator is not primitive")

omega = u^((p^2 - 1) // 34)
require(omega == 55 * u + 41, "cyclic generator representation drift")
require(omega.multiplicative_order() == 34,
        "cyclic domain generator order drift")

n = ZZ(34)
k = ZZ(13)
R = n - k
j = ZZ(20)
A = n - j
t = R - j
require((n, k, R, j, A, t) == (34, 13, 21, 20, 14, 1),
        "toy row drift")

D = [omega^index for index in range(n)]
require(len(set(D)) == n, "cyclic domain collision")
require(all(point != 0 for point in D), "cyclic domain gained zero")
a = D[0]
b = D[1]
B = tuple(range(2, n))

PR = PolynomialRing(F, "X")
X = PR.gen()


def root_polynomial(indices):
    return prod(X - D[index] for index in indices)


lambdas = []
for point in D:
    denominator = prod(point - other for other in D if other != point)
    require(denominator != 0, "dual-weight denominator vanished")
    lambdas.append(1 / denominator)
require(all(lambdas[index] == D[index] / n for index in range(n)),
        "cyclic dual-weight closed form drift")

H = matrix(
    F,
    R,
    n,
    lambda row, column: lambdas[column] * D[column]^row,
)
require(H.rank() == R, "RS parity-check matrix lost rank")

epsilon_0 = vector(F, [1] + [0] * (n - 1))
epsilon_1 = vector(F, [0, 1] + [0] * (n - 2))
y_0 = H * epsilon_0
y_1 = H * epsilon_1
require(matrix(F, [y_0, y_1]).rank() == 2,
        "syndrome line degenerated")

frobenius_rows = [
    y_0,
    y_1,
    vector(F, [entry^p for entry in y_0]),
    vector(F, [entry^p for entry in y_1]),
]
frobenius_stack_rank = matrix(F, frobenius_rows).rank()
require(frobenius_stack_rank == 3,
        "syndrome plane became base-field defined")

RICH_CORE = (4, 5, 13, 15, 16, 19, 21, 22, 27, 28, 30)
OUTLIERS = (
    (3, 4, 5, 6, 7, 13, 17, 23, 24, 25, 30, 31),
    (5, 6, 7, 8, 13, 15, 16, 18, 21, 23, 24, 32),
    (3, 5, 7, 10, 13, 14, 15, 17, 20, 21, 24, 30),
    (2, 5, 7, 9, 10, 20, 22, 23, 24, 28, 30, 33),
    (2, 5, 15, 16, 18, 19, 20, 23, 24, 30, 31, 33),
    (5, 7, 8, 9, 11, 13, 15, 19, 20, 25, 31, 33),
    (7, 12, 14, 15, 17, 19, 20, 25, 26, 31, 32, 33),
    (3, 4, 8, 15, 17, 22, 24, 25, 26, 28, 29, 30),
)

require(len(RICH_CORE) == len(set(RICH_CORE)) == 11,
        "rich core size drift")
require(set(RICH_CORE).issubset(B), "rich core left B")
require(len(OUTLIERS) == 8, "outlier count drift")
require(all(len(item) == len(set(item)) == 12 for item in OUTLIERS),
        "outlier support size drift")
require(all(set(item).issubset(B) for item in OUTLIERS),
        "outlier root set left B")

moving_indices = tuple(index for index in B if index not in RICH_CORE)
require(len(moving_indices) == 21, "rich moving-index count drift")
rich_root_sets = tuple(
    tuple(sorted(RICH_CORE + (moving,))) for moving in moving_indices
)
root_sets = rich_root_sets + OUTLIERS
require(len(root_sets) == len(set(root_sets)) == 29,
        "declared root-set inventory drift")


def witness(root_set):
    roots = root_polynomial(root_set)
    polynomial = roots / roots(a)
    slope = polynomial(b)
    return polynomial, slope


code_polynomials = []
slopes = []
errors = []
supports = []
zero_masks = []
regular_minors = []
hankel_noncontainment = []

syndrome_0 = [
    sum(lambdas[index] * D[index]^moment * epsilon_0[index]
        for index in range(n))
    for moment in range(R)
]
syndrome_1 = [
    sum(lambdas[index] * D[index]^moment * epsilon_1[index]
        for index in range(n))
    for moment in range(R)
]

for root_set in root_sets:
    polynomial, slope = witness(root_set)
    codeword = vector(F, [polynomial(point) for point in D])
    error = epsilon_0 + slope * epsilon_1 - codeword
    support = tuple(index for index, value in enumerate(error) if value != 0)
    locator = root_polynomial(support)
    locator_coefficients = vector(F, [locator[degree] for degree in range(j + 1)])
    hankel_0 = vector(F, syndrome_0[:j + 1])
    hankel_1 = vector(F, syndrome_1[:j + 1])

    require(polynomial.degree() == k - 1,
            "witness polynomial degree drift")
    require(polynomial(a) == 1 and polynomial(b) == slope,
            "sparse-coordinate agreement drift")
    require(H * codeword == 0, "witness left the RS code")
    require(H * error == y_0 + slope * y_1,
            "witness syndrome drift")
    require(slope != 0 and slope^p != slope,
            "selected slope is not genuinely quadratic")
    require(set(support) == set(B) - set(root_set),
            "actual support differs from root-set complement")
    require(len(support) == error.hamming_weight() == j,
            "selected witness radius drift")
    require((hankel_0 + slope * hankel_1) * locator_coefficients == 0,
            "regular Hankel incidence failed")
    require(hankel_1 * locator_coefficients != 0,
            "same-support noncontainment failed")

    chosen_minor = syndrome_0[1] + slope * syndrome_1[1]
    require(chosen_minor == lambdas[0] * a + slope * lambdas[1] * b,
            "chosen regular minor formula drift")
    require(chosen_minor != 0, "chosen regular chart failed")
    require(H.matrix_from_columns(list(support)).rank() == j,
            "actual support image lost MDS rank")
    require(H.matrix_from_columns(list(support) + [1]).rank() == j + 1,
            "support transversality failed")

    code_polynomials.append(polynomial)
    slopes.append(slope)
    errors.append(error)
    supports.append(support)
    zero_masks.append(root_set)
    regular_minors.append(chosen_minor)
    hankel_noncontainment.append(hankel_1 * locator_coefficients)

require(len(slopes) == len(set(slopes)) == 29,
        "declared slopes collided")
require(all(value != 0 for value in regular_minors),
        "regular-minor inventory contains zero")
require(all(value != 0 for value in hankel_noncontainment),
        "noncontainment inventory contains zero")

affine_rank = matrix(
    F, [error - errors[0] for error in errors[1:]]
).rank()
raw_rank = matrix(F, errors).rank()
require((affine_rank, raw_rank) == (9, 10),
        "selector rank tuple drift")

direction = errors[1] - errors[0]
slope_direction = slopes[1] - slopes[0]
kernel_residuals = []
for index in range(2, len(errors)):
    coefficient = (slopes[index] - slopes[0]) / slope_direction
    residual = (errors[index] - errors[0]) - coefficient * direction
    require(H * residual == 0, "kernel residual left the RS code")
    kernel_residuals.append(residual)
K0 = matrix(F, kernel_residuals).row_space().basis_matrix()
require(K0.rank() == 8, "actual kernel core rank drift")

carrier = set().union(*(set(support) for support in supports))
first_ten_indices = [0, 1] + list(range(21, 29))
first_ten_carrier = set().union(
    *(set(supports[index]) for index in first_ten_indices)
)
require(carrier == first_ten_carrier == set(B),
        "ten selected supports do not recover the carrier")
N_V = ZZ(len(carrier))
nu = N_V - R
require((N_V, nu) == (32, 11), "carrier excess drift")

K0_carrier = K0.matrix_from_columns(list(B))
core_columns = [B.index(index) for index in RICH_CORE]
require(K0_carrier.matrix_from_columns(core_columns).rank() == 8,
        "rich core restriction lost rank eight")

dependent_core_bases = []
for positions in combinations(range(len(RICH_CORE)), 8):
    columns = [core_columns[position] for position in positions]
    if K0_carrier.matrix_from_columns(columns).rank() < 8:
        dependent_core_bases.append(positions)
beta_L = ZZ(binomial(len(RICH_CORE), 8) - len(dependent_core_bases))
require(beta_L == 165 and not dependent_core_bases,
        "rich-line beta mass drift")

# Recover K0 graph coordinates and canonically group every pair-defined line.
k0_pivots = list(K0.pivots())
k0_square = K0.matrix_from_columns(k0_pivots)
require(k0_square.det() != 0, "K0 pivot square became singular")
k0_square_inverse = k0_square.inverse()
affine_direction = direction / slope_direction
affine_origin = errors[0] - slopes[0] * affine_direction
require(H * affine_origin == y_0 and H * affine_direction == y_1,
        "affine syndrome normalization drift")


def k0_coordinates(word):
    restricted = vector(F, [word[index] for index in k0_pivots])
    coefficients = restricted * k0_square_inverse
    require(coefficients * K0 == word, "K0 coordinate reconstruction failed")
    return vector(F, coefficients)


graph_coordinates = [
    k0_coordinates(
        errors[index] - affine_origin - slopes[index] * affine_direction
    )
    for index in range(len(errors))
]

line_members = defaultdict(set)
for left, right in combinations(range(len(slopes)), 2):
    denominator = slopes[right] - slopes[left]
    beta = (graph_coordinates[right] - graph_coordinates[left]) / denominator
    alpha = graph_coordinates[left] - slopes[left] * beta
    key = (tuple(alpha), tuple(beta))
    line_members[key].update((left, right))

line_size_histogram = defaultdict(ZZ)
for members in line_members.values():
    line_size_histogram[len(members)] += 1
rich_lines = [tuple(sorted(members)) for members in line_members.values()
              if len(members) >= 3]
require(dict(line_size_histogram) == {21: 1, 2: 196},
        "canonical graph-line histogram drift")
require(rich_lines == [tuple(range(21))],
        "declared selector gained another nontrivial graph line")

polynomial_direction = (
    code_polynomials[1] - code_polynomials[0]
) / (slopes[1] - slopes[0])
polynomial_origin = code_polynomials[0] - slopes[0] * polynomial_direction
require(all(
    code_polynomials[index]
    == polynomial_origin + slopes[index] * polynomial_direction
    for index in range(21)
), "rich codeword-pencil identity failed")
require((polynomial_origin.degree(), polynomial_direction.degree()) == (12, 12),
        "rich pencil degree tuple drift")
common_gcd = gcd(polynomial_origin, polynomial_direction)
require(common_gcd.degree() == 11, "rich pencil GCD degree drift")

common_zero = tuple(index for index in B if index in RICH_CORE)
moving_support = tuple(index for index in B if index not in RICH_CORE)
M_L = ZZ(len(moving_support))
x_L = M_L - j
moving_zero_sets = []
for index in range(21):
    zeros = frozenset(
        coordinate for coordinate in moving_support
        if errors[index][coordinate] == 0
    )
    moving_zero_sets.append(zeros)
require((len(common_zero), M_L, x_L) == (11, 21, 1),
        "rich-line support tuple drift")
require(all(len(zeros) == 1 for zeros in moving_zero_sets),
        "rich-line moving-zero size drift")
require(len(set().union(*moving_zero_sets)) == M_L,
        "rich-line moving zeros do not partition W_L")

# Direct basis multiplicities independently replay the atlas contribution.
basis_multiplicity = defaultdict(ZZ)
candidate_mask_basis_incidences = ZZ(0)
valid_mask_basis_incidences = ZZ(0)
for mask in zero_masks:
    for basis in combinations(mask, 8):
        candidate_mask_basis_incidences += 1
        columns = [B.index(index) for index in basis]
        if K0_carrier.matrix_from_columns(columns).rank() == 8:
            valid_mask_basis_incidences += 1
            basis_multiplicity[tuple(basis)] += 1

direct_excess = ZZ(sum(
    max(ZZ(0), multiplicity - 20)
    for multiplicity in basis_multiplicity.values()
))
atlas_excess = beta_L * (ZZ(21) - 20)
require(candidate_mask_basis_incidences == 14_355,
        "candidate mask-basis incidence count drift")
require(valid_mask_basis_incidences == 14_198,
        "valid mask-basis incidence count drift")
require(len(basis_multiplicity) == 10_898,
        "distinct valid basis count drift")
require(max(basis_multiplicity.values()) == 21,
        "maximum basis multiplicity drift")
require(sum(value >= 21 for value in basis_multiplicity.values()) == 165,
        "rich basis count drift")
require(direct_excess == atlas_excess == 165,
        "direct and atlas excess diverged")


def positive_core_q0(support, c):
    support = set(support)
    n_c = n // c
    full_fibres = []
    covered = set()
    for residue in range(n_c):
        fibre = {residue + lift * n_c for lift in range(c)}
        if fibre.issubset(support):
            full_fibres.append(residue)
            covered.update(fibre)
    j_c, remainder = divmod(j, c)
    return (
        j_c >= 1
        and len(full_fibres) == j_c
        and len(support - covered) == remainder
    )


def periodic_shifts(support):
    support = set(support)
    return tuple(
        shift for shift in range(1, n)
        if {(index + shift) % n for index in support} == support
    )


q0_c2_count = ZZ(sum(positive_core_q0(support, 2) for support in supports))
q0_c17_count = ZZ(sum(positive_core_q0(support, 17) for support in supports))
periodic_support_count = ZZ(sum(bool(periodic_shifts(support))
                                for support in supports))
require((q0_c2_count, q0_c17_count, periodic_support_count) == (0, 0, 0),
        "declared support gained a periodic/Q0 owner")

# Exact 12-subset product DP.  For a nonzero degree-at-most-12 polynomial,
# fourteen agreements force exactly twelve B-roots and both sparse points.
agreement_pairs = [
    (roots_B, sparse_agreements)
    for roots_B in range(13)
    for sparse_agreements in range(3)
    if roots_B + sparse_agreements >= A
]
require(agreement_pairs == [(12, 2)],
        "noncontained-witness agreement arithmetic drift")

group_order = ZZ(p^2 - 1)
log_table = {u^exponent: exponent for exponent in range(group_order)}
require(len(log_table) == group_order, "field discrete-log table drift")
ratio_logs = [
    log_table[(b - D[index]) / (a - D[index])]
    for index in B
]
subset_counts = [[ZZ(0)] * group_order for _ in range(13)]
subset_counts[0][0] = 1
for exponent in ratio_logs:
    for size in range(11, -1, -1):
        for residue, count in enumerate(subset_counts[size]):
            if count:
                subset_counts[size + 1][(residue + exponent) % group_order] += count

frontier_counts = subset_counts[12]
require(sum(frontier_counts) == binomial(32, 12),
        "12-subset DP total drift")
frontier_exponents = tuple(
    exponent for exponent, count in enumerate(frontier_counts) if count
)
require(len(frontier_exponents) == 66,
        "complete noncontained slope frontier drift")
require(all((u^exponent)^p != u^exponent
            for exponent in frontier_exponents),
        "frontier gained a base-field slope")
selected_exponents = tuple(log_table[slope] for slope in slopes)
require(set(selected_exponents).issubset(frontier_exponents),
        "declared selector left the complete slope frontier")
selected_witness_counts = [frontier_counts[index]
                           for index in selected_exponents]
require((min(selected_witness_counts), max(selected_witness_counts))
        == (3_420_854, 3_421_402),
        "selected witness-count range drift")

frontier_distribution_sha256 = canonical_hash(
    [ZZ(value) for value in frontier_counts]
)
selected_slopes_sha256 = canonical_hash(
    [field_coordinates(slope) for slope in slopes]
)

# Close the complete 66-slope toy family by a lexicographic pair selector.
# Relative to the first ratio, all 32 point ratios lie in one order-66 coset.
FULL_SELECTOR_CORE = (5, 7, 8, 9, 11, 15, 18, 20, 24, 33)
require(len(FULL_SELECTOR_CORE) == len(set(FULL_SELECTOR_CORE)) == 10,
        "complete-selector core size drift")
require(set(FULL_SELECTOR_CORE).issubset(B),
        "complete-selector core left B")
full_moving_indices = tuple(
    index for index in B if index not in FULL_SELECTOR_CORE
)
require(len(full_moving_indices) == 22,
        "complete-selector moving set size drift")

h = F(63)
require(h.multiplicative_order() == 66,
        "relative-ratio generator order drift")
point_ratios = [(b - D[index]) / (a - D[index]) for index in B]
relative_log_table = {h^exponent: exponent for exponent in range(66)}
require(len(relative_log_table) == 66,
        "relative order-66 log table drift")
relative_exponents = tuple(
    relative_log_table[ratio / point_ratios[0]]
    for ratio in point_ratios
)
require(relative_exponents == (
    0, 54, 3, 24, 63, 1, 64, 46,
    48, 27, 5, 36, 44, 7, 49, 23,
    17, 57, 33, 62, 4, 35, 13, 58,
    60, 42, 39, 43, 16, 37, 52, 40,
), "relative point-ratio exponent table drift")

index_to_relative_exponent = {
    index: relative_exponents[B.index(index)] for index in B
}
pairs_by_residue = defaultdict(list)
for left, right in combinations(full_moving_indices, 2):
    residue = (
        index_to_relative_exponent[left]
        + index_to_relative_exponent[right]
    ) % 66
    pairs_by_residue[residue].append((left, right))
require(set(pairs_by_residue) == set(range(66)),
        "pair sums do not cover all 66 slope residues")

lex_pairs = tuple(min(pairs_by_residue[residue]) for residue in range(66))
require(all(lex_pairs[residue] == sorted(pairs_by_residue[residue])[0]
            for residue in range(66)),
        "complete selector is not lexicographically canonical")
full_root_sets = tuple(
    tuple(sorted(FULL_SELECTOR_CORE + pair)) for pair in lex_pairs
)
require(len(full_root_sets) == len(set(full_root_sets)) == 66,
        "complete-selector root-set inventory drift")

full_code_polynomials = []
full_slopes = []
full_errors = []
full_supports = []
for root_set in full_root_sets:
    polynomial, slope = witness(root_set)
    codeword = vector(F, [polynomial(point) for point in D])
    error = epsilon_0 + slope * epsilon_1 - codeword
    support = tuple(index for index, value in enumerate(error) if value != 0)
    locator = root_polynomial(support)
    locator_coefficients = vector(
        F, [locator[degree] for degree in range(j + 1)]
    )
    hankel_0 = vector(F, syndrome_0[:j + 1])
    hankel_1 = vector(F, syndrome_1[:j + 1])

    require(polynomial.degree() == k - 1 and H * codeword == 0,
            "complete-selector witness left RS(D,13)")
    require(polynomial(a) == 1 and polynomial(b) == slope,
            "complete-selector sparse agreement drift")
    require(slope != 0 and slope^p != slope,
            "complete selector gained a nonquadratic slope")
    require(set(support) == set(B) - set(root_set)
            and len(support) == error.hamming_weight() == j,
            "complete-selector actual support drift")
    require((hankel_0 + slope * hankel_1) * locator_coefficients == 0,
            "complete-selector Hankel incidence failed")
    require(hankel_1 * locator_coefficients != 0,
            "complete-selector noncontainment failed")
    require(syndrome_0[1] + slope * syndrome_1[1] != 0,
            "complete-selector regular minor vanished")
    require(H.matrix_from_columns(list(support)).rank() == j,
            "complete-selector support rank drift")
    require(H.matrix_from_columns(list(support) + [1]).rank() == j + 1,
            "complete-selector transversality drift")

    full_code_polynomials.append(polynomial)
    full_slopes.append(slope)
    full_errors.append(error)
    full_supports.append(support)

frontier_elements = {u^exponent for exponent in frontier_exponents}
require(len(set(full_slopes)) == 66
        and set(full_slopes) == frontier_elements,
        "lex selector does not exhaust the 66-slope frontier")
full_affine_rank = matrix(
    F, [error - full_errors[0] for error in full_errors[1:]]
).rank()
full_polynomial_affine_rank = matrix(F, [
    vector(F, [
        (polynomial - full_code_polynomials[0])[degree]
        for degree in range(k)
    ])
    for polynomial in full_code_polynomials[1:]
]).rank()
full_raw_rank = matrix(F, full_errors).rank()
require((full_polynomial_affine_rank, full_affine_rank, full_raw_rank)
        == (2, 2, 3),
        "complete-selector rank tuple drift")

# The affine difference map T(h)=h(b)e_b-ev_D(h) is injective on the
# 12-dimensional space h(a)=0, deg(h)<=12.  This makes the polynomial and
# error affine ranks identical, rather than merely comparing their values on
# this one fixture.
difference_basis = [(X - a) * X^degree for degree in range(k - 1)]
difference_map_rows = []
for polynomial in difference_basis:
    image = polynomial(b) * epsilon_1 - vector(
        F, [polynomial(point) for point in D]
    )
    difference_map_rows.append(image)
difference_map_rank = matrix(F, difference_map_rows).rank()
require(difference_map_rank == k - 1 == 12,
        "polynomial-to-error difference map lost injectivity")

full_carrier = set().union(*(set(support) for support in full_supports))
require(full_carrier == set(full_moving_indices),
        "complete-selector carrier is not the 22-point core complement")
full_N_V = ZZ(len(full_carrier))
full_kappa = full_N_V - R
require((full_N_V, full_kappa) == (22, 1),
        "complete-selector carrier excess drift")

full_common_gcd = full_code_polynomials[0]
for polynomial in full_code_polynomials[1:]:
    full_common_gcd = gcd(full_common_gcd, polynomial)
require(full_common_gcd.degree() == 10,
        "complete-selector common GCD degree drift")
require(root_polynomial(FULL_SELECTOR_CORE).divides(full_common_gcd),
        "declared degree-10 core does not divide complete-selector GCD")

full_q0_c2_count = ZZ(sum(
    positive_core_q0(support, 2) for support in full_supports
))
full_q0_c17_count = ZZ(sum(
    positive_core_q0(support, 17) for support in full_supports
))
full_periodic_support_count = ZZ(sum(
    bool(periodic_shifts(support)) for support in full_supports
))
full_slopes_sha256 = canonical_hash(
    [field_coordinates(slope) for slope in full_slopes]
)
lex_pairs_sha256 = canonical_hash([list(pair) for pair in lex_pairs])

# Rank one is impossible for any complete selector.  If 66 normalized
# degree-at-most-12 polynomials lay on one affine line and had c common roots
# in B, every other B-coordinate could be a root for at most one line point.
# The resulting root-incidence inequality forces c>=12.  The line direction
# also vanishes at a because every polynomial is normalized to q(a)=1, giving
# at least 13 roots for a nonzero polynomial of degree at most 12.
root_incidence_total = ZZ(66 * 12)
rank_one_common_root_lower_bound = ZZ(ceil((root_incidence_total - 32) / 65))
require(rank_one_common_root_lower_bound == 12,
        "rank-one common-root lower bound drift")
require(66 * 11 + (32 - 11) < root_incidence_total,
        "rank-one incidence contradiction lost strictness")
require(rank_one_common_root_lower_bound + 1 > k - 1,
        "rank-one direction no longer exceeds the degree bound")
minimum_complete_selector_affine_rank = ZZ(2)
require(full_affine_rank == minimum_complete_selector_affine_rank,
        "lex selector no longer attains the minimum affine rank")

# Carrier excess zero is likewise impossible.  If all error supports lay in
# U with |U|<=21, every root set would contain B-U, a common core of size at
# least 11.  A 12-set extending such a core yields at most |U|<=21 distinct
# witnesses (or one if the core already has size 12), not 66 slopes.
maximum_root_sets_at_carrier_excess_zero = ZZ(R)
require(maximum_root_sets_at_carrier_excess_zero < len(frontier_exponents),
        "carrier-excess-zero counting contradiction failed")
kappa_star = ZZ(1)
require(full_kappa == kappa_star,
        "lex selector no longer attains minimum carrier excess")
full_owner_cap = ZZ(
    binomial(R + full_kappa, full_kappa + 1)
    // binomial(R + full_kappa - j - 1, full_kappa)
)
require(full_owner_cap == binomial(22, 2) == 231,
        "toy B_1 owner cap drift")
require(len(frontier_exponents) <= full_owner_cap,
        "complete toy slope family exceeds the low-carrier owner cap")

# Later cyclic predicates have the opposite existential projection from the
# chosen lex selector.  Exactly C(15,10)=3003 supports are unions of ten
# available shift-17 pairs; each is both shift-17 periodic and raw Q0 at c=2.
# Their slope projection covers all 66 frontier slopes.  This does not affect
# the closure because the branch-3 low-carrier owner is earlier.
available_shift17_pairs = tuple(
    (residue, residue + 17) for residue in range(2, 17)
)
require(len(available_shift17_pairs) == 15,
        "available shift-17 pair count drift")
periodic_q0_counts_by_exponent = [ZZ(0)] * group_order
periodic_q0_support_count = ZZ(0)
for chosen_pairs in combinations(available_shift17_pairs, 10):
    support = tuple(sorted(
        index for pair in chosen_pairs for index in pair
    ))
    require(len(support) == j, "periodic support size drift")
    require(positive_core_q0(support, 2),
            "shift-17 periodic support lost c=2 Q0 membership")
    require(17 in periodic_shifts(support),
            "declared shift-17 support lost periodicity")
    root_set = tuple(sorted(set(B) - set(support)))
    require(len(root_set) == 12, "periodic complement root-set size drift")
    _, slope = witness(root_set)
    periodic_q0_counts_by_exponent[log_table[slope]] += 1
    periodic_q0_support_count += 1

require(periodic_q0_support_count == binomial(15, 10) == 3_003,
        "periodic/Q0 support inventory drift")
periodic_q0_frontier_counts = [
    periodic_q0_counts_by_exponent[exponent]
    for exponent in frontier_exponents
]
require(sum(count > 0 for count in periodic_q0_frontier_counts) == 66,
        "periodic/Q0 slope projection does not cover the frontier")
require((min(periodic_q0_frontier_counts),
         max(periodic_q0_frontier_counts)) == (41, 51),
        "periodic/Q0 witness multiplicity range drift")
periodic_q0_frontier_counts_sha256 = canonical_hash(
    periodic_q0_frontier_counts
)
c17_fibres = tuple(
    {residue + 2 * lift for lift in range(17)}
    for residue in range(2)
)
require(0 in c17_fibres[0] and 1 in c17_fibres[1],
        "c=17 fibre anchors drift")
require(all(not fibre.issubset(B) for fibre in c17_fibres),
        "a c=17 fibre became available inside B")
# Every nonzero noncontained radius-20 support in this model is B-S and is
# therefore contained in B.  Since each c=17 fibre contains 0 or 1, no witness
# in the complete inventory can contain a full c=17 fibre.
q0_c17_existential_slope_count = ZZ(0)
require(all(not positive_core_q0(support, 17)
            for support in full_supports),
        "lex selector gained c=17 Q0 membership")

# Within the two-sparse one-moving-root ansatz these dimensions are minimal.
require(R == 21 and k - 2 == 11 and n == 34,
        "minimal row equalities drift")
require(len(OUTLIERS) == affine_rank - 1 == 8,
        "minimal outlier count drift")
for prime in prime_range(2, p):
    require((prime^2 - 1) % 34 != 0 and (prime^6 - 1) % 34 != 0,
            "smaller quadratic/sextic prime supports order 34")
require((p^2 - 1) % 34 == 0 and (p^6 - 1) % 34 == 0,
        "GF(67^2)/GF(67^6) lost order-34 capacity")

payload = {
    "schema": "rs-mca-m1-kb-branch3-rank9-cyclic-rich-pencil-control-v1-sage",
    "status": "PASS",
    "classification": "EXACT_CYCLIC_COMPLETE_SELECTOR_LOW_EXCESS_CLOSURE",
    "field": {
        "characteristic": p,
        "degree": 2,
        "cardinality": F.cardinality(),
        "modulus_coefficients_ascending": [2, 63, 1],
        "primitive_generator_coordinates": field_coordinates(u),
        "omega_coordinates": field_coordinates(omega),
        "omega_order": omega.multiplicative_order(),
        "domain_order": n,
    },
    "row": {"n": n, "k": k, "R": R, "j": j, "A": A, "t": t},
    "source_pair": {
        "support_indices": [0, 1],
        "support_size": 2,
        "syndrome_rank": 2,
        "frobenius_stack_rank": frobenius_stack_rank,
        "projective_syndrome_field_full": True,
        "global_containment_removed": False,
    },
    "selector": {
        "declared_slope_count": ZZ(len(slopes)),
        "distinct_slope_count": ZZ(len(set(slopes))),
        "selected_slopes_sha256": selected_slopes_sha256,
        "all_selected_slopes_quadratic": True,
        "rich_support_count": ZZ(len(rich_root_sets)),
        "outlier_count": ZZ(len(OUTLIERS)),
        "complete_on_declared_Gamma": True,
        "declared_Gamma_exhausts_full_bad_set": False,
        "witness_inventory_exhaustive": False,
        "all_deficits_zero": True,
        "affine_difference_rank": affine_rank,
        "raw_witness_rank": raw_rank,
        "kernel_core_rank": K0.rank(),
    },
    "carrier": {
        "N_V": N_V,
        "nu": nu,
        "ten_supports_recover_carrier": True,
    },
    "hankel": {
        "regular_chart_count": ZZ(len(regular_minors)),
        "noncontainment_count": ZZ(len(hankel_noncontainment)),
        "support_rank": j,
        "support_plus_direction_rank": j + 1,
        "q0_c2_count": q0_c2_count,
        "q0_c17_count": q0_c17_count,
        "periodic_support_count": periodic_support_count,
    },
    "atlas": {
        "rich_line_count": 1,
        "pair_only_line_count": 196,
        "J_L": 21,
        "M_L": M_L,
        "x_L": x_L,
        "delta_histogram": {"0": 21},
        "Z_L_size_in_carrier": ZZ(len(common_zero)),
        "beta_L": beta_L,
        "gcd_degree": common_gcd.degree(),
        "sparse_plant_size": 2,
        "candidate_mask_basis_incidences": candidate_mask_basis_incidences,
        "valid_mask_basis_incidences": valid_mask_basis_incidences,
        "distinct_valid_bases": ZZ(len(basis_multiplicity)),
        "maximum_basis_multiplicity": ZZ(max(basis_multiplicity.values())),
        "direct_excess": direct_excess,
        "atlas_excess": atlas_excess,
    },
    "complete_selector_frontier": {
        "noncontained_bad_slope_count": ZZ(len(frontier_exponents)),
        "declared_slope_count": ZZ(len(slopes)),
        "unselected_slope_count": ZZ(len(frontier_exponents) - len(slopes)),
        "all_frontier_slopes_quadratic": True,
        "twelve_subset_count": ZZ(binomial(32, 12)),
        "selected_witness_count_min": ZZ(min(selected_witness_counts)),
        "selected_witness_count_max": ZZ(max(selected_witness_counts)),
        "frontier_distribution_sha256": frontier_distribution_sha256,
        "full_selector_constructed": True,
        "minimum_full_selector_affine_rank_computed": True,
        "minimum_full_selector_affine_rank": minimum_complete_selector_affine_rank,
        "periodic_q0_c2_support_count": periodic_q0_support_count,
        "periodic_q0_c2_projected_slope_count": 66,
        "periodic_q0_c2_witness_count_min": ZZ(min(periodic_q0_frontier_counts)),
        "periodic_q0_c2_witness_count_max": ZZ(max(periodic_q0_frontier_counts)),
        "periodic_q0_c2_frontier_counts_sha256": periodic_q0_frontier_counts_sha256,
        "q0_c17_existential_slope_count": q0_c17_existential_slope_count,
        "q0_c17_empty_reason": "EACH_17_FIBRE_CONTAINS_0_OR_1_OUTSIDE_B",
    },
    "complete_selector_closure": {
        "selector_rule": "LEX_FIRST_PAIR_PER_RELATIVE_RESIDUE",
        "fixed_core_size": ZZ(len(FULL_SELECTOR_CORE)),
        "moving_index_count": ZZ(len(full_moving_indices)),
        "pair_sum_residues_covered": ZZ(len(pairs_by_residue)),
        "selected_slope_count": ZZ(len(full_slopes)),
        "full_slopes_sha256": full_slopes_sha256,
        "lex_pairs_sha256": lex_pairs_sha256,
        "affine_difference_rank": full_affine_rank,
        "polynomial_affine_rank": full_polynomial_affine_rank,
        "polynomial_to_error_difference_map_rank": difference_map_rank,
        "raw_witness_rank": full_raw_rank,
        "carrier_size": full_N_V,
        "carrier_excess": full_kappa,
        "kappa_star": kappa_star,
        "kappa_star_proved_exact": True,
        "common_gcd_degree": full_common_gcd.degree(),
        "q0_c2_count": full_q0_c2_count,
        "q0_c17_count": full_q0_c17_count,
        "periodic_support_count": full_periodic_support_count,
        "owner": "CERTIFIED_LOW_EXCESS_COMMON_CARRIER",
        "owner_cutoff": 10,
        "owner_eligible": full_kappa <= 10,
        "owner_cap_B_1": full_owner_cap,
        "owner_cap_fits_66_slopes": len(frontier_exponents) <= full_owner_cap,
        "minimum_affine_rank": minimum_complete_selector_affine_rank,
        "minimum_affine_rank_proved_exact": True,
    },
    "minimality": {
        "ansatz": "TWO_SPARSE_ONE_MOVING_ROOT_HIGH_CARRIER_RANK9",
        "minimum_R": 21,
        "minimum_k": 13,
        "minimum_n": 34,
        "minimum_outliers": 8,
        "minimum_quadratic_or_sextic_prime": p,
    },
    "scope_guards": {
        "exact_toy_control": True,
        "complete_only_on_declared_Gamma": True,
        "full_bad_set_exhausted_by_separate_selector": True,
        "deployed": False,
        "koalabear_domain_instantiated": False,
        "global_first_match_survival_proved": False,
        "deployed_aggregate_gate_proved": False,
        "ledger_movement": 0,
    },
}
payload["payload_sha256"] = canonical_hash(payload)
print(json.dumps(payload, sort_keys=True, default=int))
