#!/usr/bin/env sage
"""Exact toy controls for maximal-gcd three-point synchronization.

This replay checks projective bookkeeping over GF(5) inside GF(5^6).  It is
not a deployed KoalaBear selector or a proof of selector provenance.
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


base_projective_line = [
    (F(b), F.one()) for b in B
] + [(F.one(), F.zero())]

# A nonstandard reduced map with a pole at the base point zero:
# phi([X:Z]) = [-(z X + Z):X].
M = matrix(F, [[-z, -1], [1, 0]])
assert M.det() != 0
assert z^5 != z

Sigma = [F(0), F(1), F(2)]
L_sigma = prod(X - h for h in Sigma)

# Toy k=6, so the maximal gcd degree is k-2=4.  The two monic, nonbase
# factors are distinct but agree exactly at every source anchor.
G1 = X^4 + z
G2 = G1 + z^2 * L_sigma
assert G1 != G2
assert G1.degree() == G2.degree() == 4
assert any(c^5 != c for c in G1.list())
assert any(c^5 != c for c in G2.list())
assert all(G1(h) == G2(h) != 0 for h in Sigma)

Pbar = z * X + 1
Qbar = X
P1, Q1 = G1 * Pbar, G1 * Qbar
P2, Q2 = G2 * Pbar, G2 * Qbar

assert gcd(P1, Q1).monic() == G1.monic()
assert gcd(P2, Q2).monic() == G2.monic()
assert all((P1(h), Q1(h)) == (P2(h), Q2(h)) for h in Sigma)
assert all(P1(h) != 0 or Q1(h) != 0 for h in Sigma)

for h in Sigma:
    source_label = normalize_projective((-P1(h), Q1(h)))
    assert projective_action(M, (h, F.one())) == source_label
    assert projective_action(M, (h, F.one())) == normalize_projective((-P2(h), Q2(h)))

common_subline = {projective_action(M, point) for point in base_projective_line}
assert len(common_subline) == 6
assert (F.one(), F.zero()) in common_subline
assert sum(1 for point in common_subline if point[1] != 0) == 5

# Every base-domain moving zero produces the common projective slope.
for G, P, Q in ((G1, P1, Q1), (G2, P2, Q2)):
    for x in map(F, B):
        assert G(x) != 0
        label = projective_action(M, (x, F.one()))
        if label[1] == 0:
            assert Q(x) == 0 and P(x) != 0
        else:
            eta = label[0]
            assert P(x) + eta * Q(x) == 0

# Two anchors do not synchronize projective maps.  Identity and a nonbase
# dilation agree at zero and infinity but not at one.  Their two base
# sublines meet in exactly those two points and have union size 10 > 6.
M1 = identity_matrix(F, 2)
M2 = matrix(F, [[z, 0], [0, 1]])
zero = (F.zero(), F.one())
infinity = (F.one(), F.zero())
one = (F.one(), F.one())
assert projective_action(M1, zero) == projective_action(M2, zero)
assert projective_action(M1, infinity) == projective_action(M2, infinity)
assert projective_action(M1, one) != projective_action(M2, one)
subline1 = {projective_action(M1, point) for point in base_projective_line}
subline2 = {projective_action(M2, point) for point in base_projective_line}
assert len(subline1 & subline2) == 2
assert len(subline1 | subline2) == 10

print("M1 full-outside maximal-gcd synchronization Sage control: PASS")
print("  GF(5^6): two distinct nonbase degree-four gcd factors")
print("  three anchors: common six-point projective subline")
print("  pole control: five finite images plus projective infinity")
print("  two-anchor countercontrol: union 10 > p+1=6")
print("  scale: EXACT_TOY_CONTROL_NOT_DEPLOYED_PROVENANCE")
