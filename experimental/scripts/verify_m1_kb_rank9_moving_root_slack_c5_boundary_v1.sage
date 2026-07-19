#!/usr/bin/env sage
"""Exact toy controls for the moving-root slack/C5 boundary lemma.

The controls work over GF(11) inside GF(11^2).  They check the whole-fibre
divisibility, the zero-slack base descent, and representatives of the two
one-slack primitive shapes.  They do not construct a complete selector,
realize the deployed beta/J contracts, or replace the symbolic proof.
"""

import json


B = GF(11)
F.<zeta> = GF(11^2)
R.<X> = PolynomialRing(F)

SCALE = "EXACT_TOY_CONTROL_NOT_DEPLOYED_SELECTOR_OR_PROOF"


def require(condition, message):
    """Fail closed in ordinary and optimized generated-Python modes."""
    if not condition:
        raise RuntimeError(message)


def locator(points):
    return prod(X - F(point) for point in points)


def is_base_element(value):
    return value^B.order() == value


def is_base_polynomial(poly):
    return all(is_base_element(coefficient) for coefficient in poly.list())


def slack_tuple(k, t, s, x, e, c, d_H):
    A = k + t
    require(c == A - x - s, "toy common-root count drift")
    return (
        d_H - c,
        e - x,
        k - 1 - d_H - e,
    )


# -------------------------------------------------------------------------
# Zero source slack: r=s-t-1=0.
# -------------------------------------------------------------------------

k0 = 5
t0 = 2
A0 = k0 + t0
s0 = t0 + 1
x0 = 2
e0 = 2
c0 = A0 - x0 - s0

D = [F(i) for i in range(11)]
Sigma = [F(2), F(3), F(4)]
C0 = [F(0), F(1)]
moving0 = [F(5), F(6)]
moving1 = [F(7), F(8)]

require(c0 == 2, "zero-slack c drift")
require(
    len(set(Sigma + C0 + moving0 + moving1))
    == len(Sigma + C0 + moving0 + moving1),
    "toy supports overlap",
)

H0 = locator(C0)
L0 = locator(moving0)
L1 = locator(moving1)
eta0 = F.zero()
eta1 = zeta
kappa0 = F.one()
kappa1 = zeta + F.one()

Pbar0 = L0
Qbar0 = (kappa1 * L1 - L0) / eta1
P0 = H0 * Pbar0
Q0 = H0 * Qbar0

require(eta0 != eta1, "toy slopes coincide")
require(gcd(Pbar0, Qbar0).degree() == 0, "zero-slack reduced pair not coprime")
require(max(Pbar0.degree(), Qbar0.degree()) == e0, "zero-slack e drift")
require(gcd(P0, Q0).monic() == H0.monic(), "zero-slack full gcd drift")
require(Pbar0 + eta0 * Qbar0 == kappa0 * L0, "first full fibre drift")
require(Pbar0 + eta1 * Qbar0 == kappa1 * L1, "second full fibre drift")
require(all((Pbar0 + eta0 * Qbar0)(point) == 0 for point in moving0), "first moving roots drift")
require(all((Pbar0 + eta1 * Qbar0)(point) == 0 for point in moving1), "second moving roots drift")
require(all(H0(point) != 0 for point in moving0 + moving1), "moving root became common")
require(is_base_polynomial(H0) and is_base_polynomial(L0) and is_base_polynomial(L1), "base locator drift")

epsilon0 = [P0(point) if point in Sigma else F.zero() for point in D]
epsilon1 = [Q0(point) if point in Sigma else F.zero() for point in D]
base_word0 = [H0(point) * L0(point) if point in Sigma else F.zero() for point in D]
base_word1 = [H0(point) * L1(point) if point in Sigma else F.zero() for point in D]

require(all(is_base_element(value) for value in base_word0 + base_word1), "base words left B")
require(
    all(epsilon0[i] + eta0 * epsilon1[i] == kappa0 * base_word0[i] for i in range(len(D))),
    "first source combination drift",
)
require(
    all(epsilon0[i] + eta1 * epsilon1[i] == kappa1 * base_word1[i] for i in range(len(D))),
    "second source combination drift",
)

source_matrix = matrix(F, [epsilon0, epsilon1])
base_matrix = matrix(F, [base_word0, base_word1])
require(source_matrix.rank() == 2, "translated source rank drift")
require(base_matrix.rank() == 2, "base source rank drift")
require(source_matrix.row_space() == base_matrix.row_space(), "GL2 base descent drift")
require(slack_tuple(k0, t0, s0, x0, e0, c0, H0.degree()) == (0, 0, 0), "zero-slack tuple drift")


# -------------------------------------------------------------------------
# One source slack, common nonbase linear gcd twist: (h,u,ell)=(1,0,0).
# -------------------------------------------------------------------------

k1 = 6
t1 = 2
A1 = k1 + t1
s1 = t1 + 2
x1 = 2
e1 = 2
c1 = A1 - x1 - s1
H_twist = H0 * (X - zeta)
P_twist = H_twist * Pbar0
Q_twist = H_twist * Qbar0

require(c1 == H0.degree(), "twist forced locator degree drift")
require(gcd(P_twist, Q_twist).monic() == H_twist.monic(), "twist full gcd drift")
require(not is_base_polynomial(H_twist), "nonbase gcd twist became base")
twist_quotient, twist_remainder = H_twist.quo_rem(H0)
require(twist_remainder == 0 and twist_quotient.degree() == 1, "gcd twist is not linear")
require(all(H_twist(point) != 0 for point in moving0 + moving1), "twist root entered moving set")
require(slack_tuple(k1, t1, s1, x1, e1, c1, H_twist.degree()) == (1, 0, 0), "gcd-twist slack drift")


# -------------------------------------------------------------------------
# One source slack, split gcd and two nonbase linear moving cofactors:
# (h,u,ell)=(0,1,0).
# -------------------------------------------------------------------------

x2 = 1
e2 = 2
c2 = A1 - x2 - s1
C2 = [F(0), F(1), F(2)]
H2 = locator(C2)
moving2_0 = [F(7)]
moving2_1 = [F(8)]
cofactor0 = X - zeta
cofactor1 = X - (zeta + F.one())
member0 = locator(moving2_0) * cofactor0
member1 = locator(moving2_1) * cofactor1
eta2_0 = F.zero()
eta2_1 = F.one()
Pbar2 = member0
Qbar2 = member1 - member0

require(c2 == H2.degree() == 3, "moving-cofactor c drift")
require(gcd(Pbar2, Qbar2).degree() == 0, "moving-cofactor pair not coprime")
require(max(Pbar2.degree(), Qbar2.degree()) == e2, "moving-cofactor e drift")
require(Pbar2 + eta2_0 * Qbar2 == member0, "first moving cofactor member drift")
require(Pbar2 + eta2_1 * Qbar2 == member1, "second moving cofactor member drift")
require(all(member0(point) == 0 for point in moving2_0), "first one-root fibre drift")
require(all(member1(point) == 0 for point in moving2_1), "second one-root fibre drift")
require(cofactor0.degree() == cofactor1.degree() == 1, "cofactor degree drift")
require(not is_base_polynomial(cofactor0), "first nonbase cofactor became base")
require(not is_base_polynomial(cofactor1), "second nonbase cofactor became base")
require(slack_tuple(k1, t1, s1, x2, e2, c2, H2.degree()) == (0, 1, 0), "moving-cofactor slack drift")


one_slack_triples = sorted([
    [int(h), int(u), int(1 - h - u)]
    for h in range(2)
    for u in range(2 - h)
])
require(one_slack_triples == [[0, 0, 1], [0, 1, 0], [1, 0, 0]], "one-slack trichotomy drift")


# Fail-closed interface mutations.  First derive ten claims from the exact
# objects above, then flip each claim in turn and require the strict interface
# validator to reject the mutated record.  This is not a claim that the toy
# data form a complete MCA selector.
interface_claims = {
    "base_descent": bool(source_matrix.row_space() == base_matrix.row_space()),
    "cofactor_degree": bool(member0.quo_rem(locator(moving2_0))[0].degree() == 1),
    "common_root_in_W": bool(all(H0(point) != 0 for point in moving0 + moving1)),
    "deficit_bound": bool(x0 <= e0 and x2 <= e2),
    "distinct_slopes": bool(eta0 != eta1),
    "full_gcd": bool(gcd(P0, Q0).monic() == H0.monic()),
    "nonbase_gcd_twist": bool(not is_base_polynomial(H_twist)),
    "nonbase_moving_cofactor": bool(not is_base_polynomial(cofactor0) and not is_base_polynomial(cofactor1)),
    "slack_identity": bool(sum(slack_tuple(k1, t1, s1, x2, e2, c2, H2.degree())) == s1 - t1 - 1),
    "source_on_W": bool(all(epsilon0[i] == epsilon1[i] == 0 for i, point in enumerate(D) if point not in Sigma)),
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
    "field_order": int(F.order()),
    "mutation_count": int(len(mutation_results)),
    "mutation_rejections": int(sum(1 for value in mutation_results.values() if value)),
    "nonbase_gcd_twist": True,
    "nonbase_linear_moving_cofactors": int(2),
    "one_slack_triples": one_slack_triples,
    "scale": SCALE,
    "toy_only": True,
    "zero_slack": {
        "C5_coordinate_recovery": True,
        "c": int(c0),
        "deg_H": int(H0.degree()),
        "e": int(e0),
        "moving_set_sizes": [int(len(moving0)), int(len(moving1))],
        "s": int(s0),
        "slacks": [int(0), int(0), int(0)],
        "t": int(t0),
        "translated_pair_base_rank": int(base_matrix.rank()),
        "x": int(x0),
    },
}

print("MOVING_ROOT_SLACK_C5_CONTROL=" + json.dumps(
    control, sort_keys=True, separators=(",", ":")
))
print("MOVING_ROOT_SLACK_C5_MUTATIONS=" + json.dumps(
    mutation_results, sort_keys=True, separators=(",", ":")
))
print("SCALE=" + SCALE)
