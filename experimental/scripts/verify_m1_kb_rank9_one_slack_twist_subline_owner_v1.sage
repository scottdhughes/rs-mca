#!/usr/bin/env sage
"""Exact toy controls for the one-slack common-twist subline owner.

The GF(13^2) construction checks two independent mechanisms:

* three fixed projective labels determine one B-subline; and
* for an exact two-label source, the p-1 Frobenius fingerprint uniquely
  recovers a nonbase common linear twist and the two scalar cosets.

It also realizes two exact moving-fibre witnesses in the one-slack
common-factor shape.  It is not a deployed complete selector, a rank-nine
census, or a proof of the symbolic theorem.
"""

import json
from itertools import permutations


SCALE = "EXACT_TOY_CONTROL_NOT_DEPLOYED_SELECTOR_CENSUS_OR_PROOF"


def require(condition, message):
    """Fail closed in ordinary and optimized generated-Python modes."""
    if not condition:
        raise RuntimeError(message)


B = GF(13)
BZ = PolynomialRing(B, "z")
z = BZ.gen()
modulus = z^2 + 12*z + 2
require(modulus.is_irreducible(), "quadratic modulus became reducible")
F = GF(13^2, name="xi", modulus=modulus)
xi = F.gen()
require(xi.multiplicative_order() == F.order() - 1,
        "declared extension generator is not primitive")

R = PolynomialRing(F, "X")
X = R.gen()
p = ZZ(B.order())


def is_base(value):
    return value^p == value


def projective(a, b):
    require(a != 0 or b != 0, "zero projective pair")
    if b != 0:
        return (a/b, F.one())
    return (F.one(), F.zero())


def apply_matrix(M, point):
    column = M * vector(F, point)
    return projective(column[0], column[1])


P1B = [projective(F(value), F.one()) for value in B]
P1B.append(projective(F.one(), F.zero()))
require(len(P1B) == p + 1, "base projective line size drift")


# -------------------------------------------------------------------------
# Three-label synchronization and the sharp p+1 finite cap.
# -------------------------------------------------------------------------

g = matrix(F, [[xi, F.one()], [F.one(), xi]])
require(g.det() != 0, "three-label projectivity became singular")
subline_three = {apply_matrix(g, point) for point in P1B}
require(len(subline_three) == p + 1, "three-label subline size drift")
require(all(point[1] != 0 for point in subline_three),
        "sharp nonstandard subline unexpectedly contains ambient infinity")

standard_triple = [
    projective(F.zero(), F.one()),
    projective(F.one(), F.one()),
    projective(F.one(), F.zero()),
]
target_triple = [apply_matrix(g, point) for point in standard_triple]
require(len(set(target_triple)) == 3, "three target labels collided")


def projectivity_from_triple(targets):
    rows = []
    for source, target in zip(standard_triple, targets):
        sx, sy = source
        tx, ty = target
        rows.append([sx*ty, sy*ty, -sx*tx, -sy*tx])
    kernel = matrix(F, rows).right_kernel()
    require(kernel.dimension() == 1, "three-point projectivity not unique")
    a, b, c, d = kernel.basis()[0]
    M = matrix(F, [[a, b], [c, d]])
    require(M.det() != 0, "recovered projectivity singular")
    return M


permutation_subline_checks = 0
for permuted in permutations(target_triple):
    recovered = projectivity_from_triple(list(permuted))
    recovered_subline = {apply_matrix(recovered, point) for point in P1B}
    require(recovered_subline == subline_three,
            "ordering changed the three-label subline")
    permutation_subline_checks += 1
require(permutation_subline_checks == 6,
        "three-label permutation count drift")


# -------------------------------------------------------------------------
# Exact r=1, h=1, u=ell=0 two-label common-twist control.
# -------------------------------------------------------------------------

D = [F(value) for value in B]
n = ZZ(13)
k = ZZ(6)
A = ZZ(10)
j = n - A
t = A - k
s = t + 2
x = ZZ(3)
c = A - x - s
require((n, k, A, j, t, s, x, c) == (13, 6, 10, 3, 4, 6, 3, 1),
        "toy row drift")


def cube_fibre(value):
    return tuple(point for point in D if point^3 == F(value))


Sigma_0 = cube_fibre(1)
Sigma_inf = cube_fibre(5)
moving_0 = cube_fibre(8)
moving_1 = cube_fibre(12)
C = (F.zero(),)
Sigma = tuple(Sigma_0 + Sigma_inf)
W = tuple(moving_0 + moving_1)

require(all(len(block) == 3 for block in
            (Sigma_0, Sigma_inf, moving_0, moving_1)),
        "cube-fibre size drift")
require(len(set(Sigma + W + C)) == n,
        "toy domain partition overlap")

L_C = X
zeta = xi
H = L_C * (X - zeta)
U = X^3 - F.one()
V = X^3 - F(5)
alpha = xi + F(2)
beta = xi + F(4)
Pbar = alpha * U
Qbar = beta * V
P = H * Pbar
Q = H * Qbar

require(H.degree() == c + 1, "one-slack gcd degree drift")
require(P.degree() == Q.degree() == k - 1, "degree budget drift")
require(gcd(P, Q).monic() == H.monic(), "full gcd drift")
require(gcd(Pbar, Qbar).degree() == 0, "reduced pair not coprime")
require(not is_base(zeta), "twist became base")
require(max(Pbar.degree(), Qbar.degree()) == x, "reduced degree drift")

epsilon_0 = vector(F, [P(point) if point in Sigma else F.zero()
                       for point in D])
epsilon_1 = vector(F, [Q(point) if point in Sigma else F.zero()
                       for point in D])
require(set(index for index, value in enumerate(epsilon_0) if value != 0)
        == set(D.index(point) for point in Sigma_inf),
        "first normalized source block drift")
require(set(index for index, value in enumerate(epsilon_1) if value != 0)
        == set(D.index(point) for point in Sigma_0),
        "second normalized source block drift")

source_labels = {
    projective(-epsilon_0[D.index(point)], epsilon_1[D.index(point)])
    for point in Sigma
}
require(source_labels == {
    projective(F.zero(), F.one()),
    projective(F.one(), F.zero()),
}, "source did not have exactly two labels")


def moving_slope(value):
    value = F(value)
    return alpha * (value - F.one()) / (beta * (F(5) - value))


selected_values = (F(8), F(12))
selected_slopes = tuple(moving_slope(value) for value in selected_values)
require(len(set(selected_slopes)) == 2, "moving slopes collided")
require(all(not is_base(value) for value in selected_slopes),
        "selected slope lost extension value")

errors = []
supports = []
for value, eta in zip(selected_values, selected_slopes):
    member = Pbar + eta * Qbar
    quotient, remainder = member.quo_rem(X^3 - value)
    require(remainder == 0 and quotient.degree() == 0
            and quotient[0] != 0,
            "moving member is not a scalar base locator")
    codeword = vector(F, [(P + eta*Q)(point) for point in D])
    received = epsilon_0 + eta*epsilon_1
    error = received - codeword
    support = tuple(index for index, entry in enumerate(error) if entry != 0)
    expected = set(D.index(point) for point in W if point^3 != value)
    require(set(support) == expected, "moving witness support drift")
    require(len(support) == error.hamming_weight() == j,
            "moving witness radius drift")
    errors.append(error)
    supports.append(support)

# A base-defined parity check confirms exact RS witness incidence.
vandermonde = matrix(F, k, n,
                     lambda row, column: D[column]^row)
parity = vandermonde.right_kernel().basis_matrix()
require(parity.rank() == n-k, "parity-check rank drift")
require(parity * vandermonde.transpose() == 0,
        "parity check does not kill the code")
y0 = parity * epsilon_0
y1 = parity * epsilon_1
require(matrix(F, [y0, y1]).rank() == 2,
        "toy source syndrome line degenerated")
require(all(parity*error == y0 + eta*y1
            for error, eta in zip(errors, selected_slopes)),
        "syndrome incidence drift")

# Fingerprint recovery on Sigma_0.  Enumeration is toy-scale only.
fingerprint_1 = {
    h: epsilon_1[D.index(h)]^(p-1) for h in Sigma_0
}
pole_candidates = []
first_h = Sigma_0[0]
for candidate in F:
    if is_base(candidate):
        continue
    shape_first = (first_h - candidate^p) / (first_h - candidate)
    scalar = fingerprint_1[first_h] / shape_first
    if all(
        fingerprint_1[h]
        == scalar * (h - candidate^p) / (h - candidate)
        for h in Sigma_0
    ):
        pole_candidates.append((candidate, scalar))

require(len(pole_candidates) == 1,
        "three-point fingerprint did not recover a unique pole")
recovered_zeta, recovered_beta_power = pole_candidates[0]
require(recovered_zeta == zeta, "recovered pole drift")
require(recovered_beta_power == beta^(p-1),
        "recovered beta coset fingerprint drift")

fingerprint_0 = {
    h: epsilon_0[D.index(h)]^(p-1) for h in Sigma_inf
}
recovered_alpha_powers = {
    fingerprint_0[h] * (h-zeta) / (h-zeta^p)
    for h in Sigma_inf
}
require(recovered_alpha_powers == {alpha^(p-1)},
        "alpha coset fingerprint drift")


def same_base_coset(left, right):
    return is_base(left/right) and left/right != 0


beta_coset = {value for value in F if value != 0
              and value^(p-1) == recovered_beta_power}
alpha_coset = {value for value in F if value != 0
               and value^(p-1) == next(iter(recovered_alpha_powers))}
require(len(beta_coset) == len(alpha_coset) == p-1,
        "scalar coset size drift")
require(all(same_base_coset(value, beta) for value in beta_coset),
        "beta coset recovery drift")
require(all(same_base_coset(value, alpha) for value in alpha_coset),
        "alpha coset recovery drift")

normalized_subline = {
    projective(-alpha*a, beta*b) for a, b in P1B
}
require(len(normalized_subline) == p+1,
        "two-label recovered subline size drift")
require(all(projective(eta, F.one()) in normalized_subline
            for eta in selected_slopes),
        "moving slopes left recovered source subline")


interface_claims = {
    "base_domain": all(is_base(point) for point in D),
    "common_twist_nonbase": not is_base(zeta),
    "coefficient_rank_two": matrix(F, [Pbar.list(), Qbar.list()]).rank() == 2,
    "exact_two_source_labels": len(source_labels) == 2,
    "fingerprint_blocks_have_three_points": min(len(Sigma_0), len(Sigma_inf)) >= 3,
    "full_gcd": gcd(P, Q).monic() == H.monic(),
    "moving_members_scalar_base_locators": True,
    "moving_slopes_in_recovered_subline": all(
        projective(eta, F.one()) in normalized_subline
        for eta in selected_slopes
    ),
    "one_slack_tuple": (H.degree()-c, x-x, k-1-H.degree()-x) == (1, 0, 0),
    "pole_unique": len(pole_candidates) == 1,
    "projective_cap_p_plus_one": len(normalized_subline) == p+1,
    "scalar_cosets_recovered": len(beta_coset) == len(alpha_coset) == p-1,
    "source_outside_zero": all(
        epsilon_0[index] == epsilon_1[index] == 0
        for index, point in enumerate(D) if point not in Sigma
    ),
    "three_label_order_independent": permutation_subline_checks == 6,
    "three_label_sharp_finite_cap": all(point[1] != 0 for point in subline_three),
    "witness_radius_exact": all(len(support) == j for support in supports),
}
require(all(interface_claims.values()), "Sage interface control failed")


def accepts_interface_claims(candidate):
    return set(candidate) == set(interface_claims) and all(candidate.values())


mutation_results = {}
for name in sorted(interface_claims):
    mutated = dict(interface_claims)
    mutated[name] = False
    mutation_results[name] = not accepts_interface_claims(mutated)
require(all(mutation_results.values()), "Sage interface mutation suite failed")

control = {
    "base_field_order": int(B.order()),
    "extension_field_order": int(F.order()),
    "mutation_count": int(len(mutation_results)),
    "mutation_rejections": int(sum(mutation_results.values())),
    "one_slack_tuple": [int(1), int(0), int(0)],
    "selected_extension_slopes": int(len(selected_slopes)),
    "source_block_sizes": [int(len(Sigma_0)), int(len(Sigma_inf))],
    "source_label_count": int(len(source_labels)),
    "three_label_permutation_checks": int(permutation_subline_checks),
    "three_label_subline_all_affine": True,
    "toy_pole_candidates": int(len(pole_candidates)),
    "recovered_subline_size": int(len(normalized_subline)),
    "scale": SCALE,
    "toy_only": True,
}

print("ONE_SLACK_TWIST_SUBLINE_CONTROL=" + json.dumps(
    control, sort_keys=True, separators=(",", ":")
))
print("ONE_SLACK_TWIST_SUBLINE_MUTATIONS=" + json.dumps(
    mutation_results, sort_keys=True, separators=(",", ":")
))
print("SCALE=" + SCALE)
