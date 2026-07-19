#!/usr/bin/env sage
"""Exact toy controls for the pair-global source--Mobius owner.

This replay works over GF(5) inside GF(5^6).  It checks two distinct
selector-carrier proxies for one fixed source pair and several load-bearing
countercontrols.  It constructs no complete selector witness assignment or
rich-line beta/J predicates.  It is not a deployed KoalaBear census or a
proof of the symbolic theorem.
"""


B = GF(5)
F.<z> = GF(5^6, modulus="primitive")
R.<X> = PolynomialRing(F)


def normalize_projective(pair):
    a, b = pair
    assert a != 0 or b != 0
    if b != 0:
        return (a / b, F.one())
    return (F.one(), F.zero())


def projective_action(matrix, point):
    x, y = point
    return normalize_projective(
        (
            matrix[0, 0] * x + matrix[0, 1] * y,
            matrix[1, 0] * x + matrix[1, 1] * y,
        )
    )


D = [F(b) for b in B]
Sigma = [F(0), F(1), F(2)]
D_outside = [x for x in D if x not in Sigma]
assert D_outside == [F(3), F(4)]

# One fixed source map for both selectors:
# phi([X:Z]) = [-(z X + Z):X].
M = matrix(F, [[-z, -1], [1, 0]])
assert M.det() != 0

L_sigma = prod(X - h for h in Sigma)
G1 = X^4 + z
G2 = G1 + z^2 * L_sigma
assert G1 != G2
assert G1.degree() == G2.degree() == 4
assert all(G1(h) == G2(h) != 0 for h in Sigma)
assert all(G(x) != 0 for G in (G1, G2) for x in D)

Pbar = z * X + 1
Qbar = X
P1, Q1 = G1 * Pbar, G1 * Qbar
P2, Q2 = G2 * Pbar, G2 * Qbar
assert gcd(P1, Q1).monic() == G1.monic()
assert gcd(P2, Q2).monic() == G2.monic()

# The fixed translated source pair equals the polynomial values on Sigma and
# is zero on D\Sigma.  The two distinct lines therefore have exactly the same
# pair-global source labels.
epsilon_0 = {x: (P1(x) if x in Sigma else F.zero()) for x in D}
epsilon_1 = {x: (Q1(x) if x in Sigma else F.zero()) for x in D}
assert all((epsilon_0[h], epsilon_1[h]) != (0, 0) for h in Sigma)
assert all((P1(h), Q1(h)) == (P2(h), Q2(h)) for h in Sigma)
for h in Sigma:
    source_label = normalize_projective((-epsilon_0[h], epsilon_1[h]))
    assert projective_action(M, (h, F.one())) == source_label

# Treat V_1={3} and V_2={4} as two distinct full-outside selector-carrier
# proxies.  No complete selector witness assignment is claimed.
V1 = {F(3)}
V2 = {F(4)}
assert V1 != V2
assert V1.isdisjoint(set(Sigma))
assert V2.isdisjoint(set(Sigma))

eta1 = projective_action(M, (F(3), F.one()))
eta2 = projective_action(M, (F(4), F.one()))
assert eta1[1] != 0 and eta2[1] != 0
assert P1(F(3)) + eta1[0] * Q1(F(3)) == 0
assert P2(F(4)) + eta2[0] * Q2(F(4)) == 0

source_mobius_image = {
    projective_action(M, (x, F.one()))
    for x in D_outside
    if projective_action(M, (x, F.one()))[1] != 0
}
cross_proxy_union = {eta1, eta2}
assert len(source_mobius_image) == 2
assert len(cross_proxy_union) == 2
assert cross_proxy_union <= source_mobius_image

# A different-source-label map is a proxy for the forbidden cross-translation
# union.  The different reduced map gives four distinct finite images on the
# same two outside inputs, exceeding the fixed-source-map cap two.  This does
# not claim to construct two valid SP3 translations of one received pair.
M_alt = matrix(F, [[-z^2, -1], [1, 0]])
assert M_alt.det() != 0 and M_alt != M
alt_image = {
    projective_action(M_alt, (x, F.one()))
    for x in D_outside
}
assert all(point[1] != 0 for point in alt_image)
assert any(
    projective_action(M, (h, F.one()))
    != projective_action(M_alt, (h, F.one()))
    for h in Sigma
)
assert len(source_mobius_image | alt_image) == 4

# Two affine source anchors do not synchronize projective maps.  Identity and
# a nonbase map agree at zero and one but not at two; their two GF(5)
# projective sublines have union ten rather than six.
base_projective_line = [
    (F(b), F.one()) for b in B
] + [(F.one(), F.zero())]
M1 = identity_matrix(F, 2)
M2 = matrix(F, [[z + 1, 0], [z, 1]])
assert M2.det() != 0
zero = (F.zero(), F.one())
one = (F.one(), F.one())
two = (F(2), F.one())
assert projective_action(M1, zero) == projective_action(M2, zero)
assert projective_action(M1, one) == projective_action(M2, one)
assert projective_action(M1, two) != projective_action(M2, two)
subline1 = {projective_action(M1, point) for point in base_projective_line}
subline2 = {projective_action(M2, point) for point in base_projective_line}
assert len(subline1 & subline2) == 2
assert len(subline1 | subline2) == 10

# Repeated target labels at distinct source inputs cannot come from PGL2,
# because every projective linear map is injective.
incompatible_labels = {
    F(0): (F.zero(), F.one()),
    F(1): (F.zero(), F.one()),
    F(2): (F.one(), F.one()),
}
assert incompatible_labels[F(0)] == incompatible_labels[F(1)]
assert F(0) != F(1)

# A moving root in Sigma is outside the allowed D\Sigma image.  Injectivity
# ensures its projective image cannot be hidden among the outside images.
source_root_image = projective_action(M, (F(1), F.one()))
assert source_root_image not in source_mobius_image

# A pole in D\Sigma produces projective infinity, which is discarded from
# the finite owner rather than counted as a finite slope.
M_pole = matrix(F, [[1, 0], [1, -3]])
assert M_pole.det() != 0
pole_images = {
    projective_action(M_pole, (x, F.one())) for x in D_outside
}
assert sum(1 for point in pole_images if point[1] == 0) == 1
assert sum(1 for point in pole_images if point[1] != 0) == 1

print("M1 pair-global source-Mobius owner Sage control: PASS")
print("  GF(5^6): two selector-carrier proxies and nonbase gcd factors")
print("  fixed translation: two selected slopes in phi(D\\Sigma), cap 2")
print("  different-source-map proxy: union 4 > fixed-source-map cap 2")
print("  two-anchor countercontrol: projective-subline union 10 > 6")
print("  incompatible labels, source-root, and projective-pole guards: PASS")
print("  scale: EXACT_TOY_CONTROL_NOT_DEPLOYED_CENSUS_OR_PROOF")
