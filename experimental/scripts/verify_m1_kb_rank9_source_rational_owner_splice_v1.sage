#!/usr/bin/env sage
"""Exact toy controls for the bounded-degree source--rational owner.

The control is deliberately small: it works over GF(13), constructs two
selector-carrier proxies with distinct full gcds and one common reduced
degree-two projective rational map, and checks the sharp ``2e+1`` anchor
threshold.  It does not construct a deployed KoalaBear selector, prove
selector provenance, or replace the symbolic rational-map rigidity proof.
"""

import json


B = GF(13)
R.<X> = PolynomialRing(B)

OWNER = "source_rational_full_outside_bounded_degree"
RESIDUAL = "UNPAID_FULL_OUTSIDE_REDUCED_DEGREE_AT_LEAST_18418"


def require(condition, message):
    """Fail closed in both ordinary and optimized Python modes."""
    if not condition:
        raise RuntimeError(message)


def normalize_projective(pair):
    """Return the canonical affine/infinity representative of a pair."""
    a, b = pair
    if a == 0 and b == 0:
        raise ValueError("projective basepoint")
    if b != 0:
        return (a / b, B.one())
    return (B.one(), B.zero())


def projective_value(pair, x):
    """Evaluate a polynomial pair at a finite source point."""
    A, C = pair
    return normalize_projective((A(x), C(x)))


def projective_value_p1(pair, point, degree):
    """Evaluate a degree-bounded homogenized pair on P^1(B)."""
    A, C = pair
    x, z = point
    if z != 0:
        return projective_value(pair, x / z)
    return normalize_projective((A[degree], C[degree]))


def is_reduced_pair(pair):
    A, C = pair
    return gcd(A, C).degree() == 0


def incidence_matrix(anchors, labels, degree):
    """Linear equations for a degree-bounded pair with given labels."""
    rows = []
    for h in anchors:
        u, v = labels[h]
        powers = [h^j for j in range(degree + 1)]
        # [A(h):C(h)]=[u:v] iff v*A(h)-u*C(h)=0.
        rows.append(
            [v * power for power in powers]
            + [-u * power for power in powers]
        )
    return matrix(B, rows)


# Five anchors are the exact rigidity threshold for degree e=2.
degree_bound = 2
Sigma = [B(i) for i in range(1, 6)]
D = list(B)
D_outside = [x for x in D if x not in Sigma]
require(len(Sigma) == 2 * degree_bound + 1, "anchor threshold drift")

# The common reduced map is psi(x)=[1:x^2].  In the source convention this
# is [-Pbar:Qbar], with Pbar=-1 and Qbar=x^2.
A_common = R.one()
C_common = X^2
Pbar = -A_common
Qbar = C_common
require(is_reduced_pair((A_common, C_common)), "common pair is not reduced")
require(
    max(A_common.degree(), C_common.degree()) == degree_bound,
    "common reduced degree drift",
)

# Distinct monic full gcds agree at all five anchors.  Multiplying the same
# reduced pair by either one models two distinct selector records without
# changing their projective source labels.
L_sigma = prod(X - h for h in Sigma)
G1 = (X^2 + B(2))^3
G2 = G1 + L_sigma
require(G1.is_monic() and G2.is_monic(), "full gcd proxy is not monic")
require(G1.degree() == G2.degree() == 6, "full gcd proxy degree drift")
require(G1 != G2, "full gcd proxies unexpectedly coincide")
require(
    all(G1(h) == G2(h) != 0 for h in Sigma),
    "full gcd proxy source values drift",
)

P1, Q1 = G1 * Pbar, G1 * Qbar
P2, Q2 = G2 * Pbar, G2 * Qbar
require(gcd(P1, Q1).monic() == G1, "selector-one full gcd drift")
require(gcd(P2, Q2).monic() == G2, "selector-two full gcd drift")

source_labels_1 = {
    h: normalize_projective((-P1(h), Q1(h))) for h in Sigma
}
source_labels_2 = {
    h: normalize_projective((-P2(h), Q2(h))) for h in Sigma
}
require(source_labels_1 == source_labels_2, "selector source labels differ")
require(
    all(
        source_labels_1[h] == projective_value((A_common, C_common), h)
        for h in Sigma
    ),
    "source labels do not match the common reduced map",
)

# The five anchor equations have a one-dimensional coefficient kernel, so
# the degree-two pair is unique up to one common nonzero scalar.
anchor_system = incidence_matrix(Sigma, source_labels_1, degree_bound)
require(anchor_system.rank() == 5, "anchor matrix rank drift")
require(
    anchor_system.right_kernel().dimension() == 1,
    "anchor kernel is not projectively unique",
)

# Use different outside moving roots for the two selector proxies.  The
# associated finite slopes satisfy P_i(x)+eta_i Q_i(x)=0 exactly.
moving_root_1 = B(6)
moving_root_2 = B(8)
require(
    moving_root_1 in D_outside and moving_root_2 in D_outside,
    "moving root entered the source",
)
require(
    G1(moving_root_1) != 0 and G2(moving_root_2) != 0,
    "moving root is a common root",
)

moving_label_1 = projective_value((A_common, C_common), moving_root_1)
moving_label_2 = projective_value((A_common, C_common), moving_root_2)
require(
    moving_label_1[1] != 0 and moving_label_2[1] != 0,
    "moving label is not finite",
)
eta_1 = moving_label_1[0]
eta_2 = moving_label_2[0]
require(
    P1(moving_root_1) + eta_1 * Q1(moving_root_1) == 0,
    "selector-one moving-root equation failed",
)
require(
    P2(moving_root_2) + eta_2 * Q2(moving_root_2) == 0,
    "selector-two moving-root equation failed",
)

# Degree-two maps need not be injective.  The outside points 6 and -6=7
# collide, while the outside point 0 is a genuine projective pole.
collision_pair = (B(6), B(7))
require(collision_pair[0] != collision_pair[1], "collision inputs coincide")
require(
    all(x in D_outside for x in collision_pair),
    "collision input entered the source",
)
require(
    projective_value((A_common, C_common), collision_pair[0])
    == projective_value((A_common, C_common), collision_pair[1]),
    "expected degree-two collision failed",
)

pole = B(0)
require(pole in D_outside, "pole entered the source")
require(
    projective_value((A_common, C_common), pole) == (B.one(), B.zero()),
    "projective pole drift",
)
outside_image = {
    projective_value((A_common, C_common), x) for x in D_outside
}
finite_outside_image = {point for point in outside_image if point[1] != 0}
require(len(outside_image) <= len(D_outside), "projective image cap failed")
require(
    len(finite_outside_image) < len(D_outside),
    "finite image did not omit the pole/collision mass",
)

# Sharpness at exactly 2e anchors: x^2 and 1/x^2 are distinct degree-two
# maps but agree at precisely the four affine roots of x^4=1 in GF(13).
square_map = (X^2, R.one())
inverse_square_map = (R.one(), X^2)
projective_line = [
    (x, B.one()) for x in B
] + [(B.one(), B.zero())]
sharp_agreement_points = [
    point
    for point in projective_line
    if projective_value_p1(square_map, point, degree_bound)
    == projective_value_p1(inverse_square_map, point, degree_bound)
]
require(square_map != inverse_square_map, "sharpness maps coincide")
require(
    len(sharp_agreement_points) == 2 * degree_bound,
    "sharp agreement count drift",
)
require(
    sorted(int(point[0]) for point in sharp_agreement_points) == [1, 5, 8, 12],
    "sharp agreement roots drift",
)

sharp_anchors = [point[0] for point in sharp_agreement_points]
sharp_labels = {
    h: projective_value(square_map, h) for h in sharp_anchors
}
sharp_system = incidence_matrix(sharp_anchors, sharp_labels, degree_bound)
require(sharp_system.rank() == 4, "sharp anchor matrix rank drift")
require(
    sharp_system.right_kernel().dimension() == 2,
    "sharp anchor kernel dimension drift",
)

# Mutation 1: four anchors are insufficient for a uniqueness claim.
insufficient_anchor_rejected = (
    len(sharp_anchors) <= 2 * degree_bound
    and sharp_system.right_kernel().dimension() > 1
)
require(insufficient_anchor_rejected, "insufficient-anchor mutation survived")

# Mutation 2: changing one selector's source label breaks the fixed-source
# compatibility prerequisite, even if an unrelated interpolant may exist.
incompatible_labels = dict(source_labels_2)
incompatible_labels[Sigma[-1]] = normalize_projective((B(2), B.one()))
if incompatible_labels[Sigma[-1]] == source_labels_1[Sigma[-1]]:
    incompatible_labels[Sigma[-1]] = normalize_projective((B(3), B.one()))
incompatible_labels_rejected = incompatible_labels != source_labels_1
require(incompatible_labels_rejected, "incompatible-label mutation survived")

# Mutation 3: a pair vanishing simultaneously at an anchor is not a
# projective map there.
basepoint_pair = (X - Sigma[0], (X - Sigma[0]) * X^2)
try:
    projective_value(basepoint_pair, Sigma[0])
    basepoint_rejected = False
except ValueError:
    basepoint_rejected = True
require(basepoint_rejected, "basepoint mutation survived")

# Mutation 4: a raw common-factor representation must be reduced before its
# degree is used.  The factor is outside Sigma so this is distinct from the
# anchor-basepoint guard above.
common_factor_pair = (
    (X - B(6)) * A_common,
    (X - B(6)) * C_common,
)
common_factor_rejected = not is_reduced_pair(common_factor_pair)
require(common_factor_rejected, "common-factor mutation survived")

mutation_results = {
    "basepoint": bool(basepoint_rejected),
    "common_factor": bool(common_factor_rejected),
    "incompatible_labels": bool(incompatible_labels_rejected),
    "insufficient_anchors": bool(insufficient_anchor_rejected),
}
require(all(mutation_results.values()), "Sage mutation suite failed")

result = {
    "anchor_count": int(len(Sigma)),
    "anchor_kernel_dimension": int(anchor_system.right_kernel().dimension()),
    "anchor_matrix_rank": int(anchor_system.rank()),
    "collision_pair": [int(x) for x in collision_pair],
    "common_reduced_degree": int(degree_bound),
    "distinct_full_gcds": True,
    "field_order": int(B.order()),
    "finite_outside_image_count": int(len(finite_outside_image)),
    "moving_roots": [int(moving_root_1), int(moving_root_2)],
    "mutation_count": int(len(mutation_results)),
    "mutation_rejections": int(sum(1 for passed in mutation_results.values() if passed)),
    "outside_domain_count": int(len(D_outside)),
    "outside_projective_image_count": int(len(outside_image)),
    "owner": OWNER,
    "pole": int(pole),
    "residual": RESIDUAL,
    "selector_count": int(2),
    "sharp_agreement_count": int(len(sharp_agreement_points)),
    "sharp_anchor_kernel_dimension": int(sharp_system.right_kernel().dimension()),
    "status": "PASS",
    "toy_only": True,
}

print("SOURCE_RATIONAL_OWNER_CONTROL=" + json.dumps(
    result, sort_keys=True, separators=(",", ":")
))
print("SOURCE_RATIONAL_OWNER_MUTATIONS=" + json.dumps(
    mutation_results, sort_keys=True, separators=(",", ":")
))
print("SCALE=EXACT_TOY_CONTROL_NOT_DEPLOYED_CENSUS_OR_PROOF")
