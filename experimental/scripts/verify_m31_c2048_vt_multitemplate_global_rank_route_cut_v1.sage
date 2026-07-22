#!/usr/bin/env sage
"""Independent exact controls for the M31 VT multitemplate rank route cut.

These are finite-field algebra fixtures for the rank-one/template-line
classification, the exact two-support inverse-residue escape criterion, and
the canonical depth-one analogue of source-coset separation.  They are not a
deployed VT census or an asymptotic proof.
"""

from itertools import combinations

F = GF(17)
RX.<X> = PolynomialRing(F)


def locator(points):
    out = RX.one()
    for point in points:
        out *= X - F(point)
    return out


def coefficient_row(poly, ambient):
    return vector(F, [poly[i] for i in range(ambient)])


def shifted_space(poly, width, ambient):
    return span(F, [coefficient_row(X^j * poly, ambient)
                    for j in range(width)])


def escape_absorbed(E, Gset, x, width):
    radius = len(E)
    ambient = radius + width
    LE = locator(E)
    LF = locator(Gset)
    WE = shifted_space(LE, width, ambient)
    WF = shifted_space(LF, width, ambient)
    extension = shifted_space(LE // (X - F(x)), width + 1, ambient)
    return extension.is_subspace(WE + WF)


def inverse_residue_degree(E, Gset, x):
    common = set(E).intersection(Gset)
    A = locator(set(E).difference(common))
    B = locator(set(Gset).difference(common))
    Ax = A // (X - F(x))
    q = (Ax * B.inverse_mod(A)).mod(A)
    return q.degree(), q


# Pairwise escape criterion: the canonical inverse residue has exactly d-1
# roots, so close pairs absorb and wide pairs never do.
width = 2
close_fixture = ({0, 1, 2, 3}, {0, 1, 2, 4}, 3)
wide_fixture = ({0, 1, 2, 3}, {0, 4, 5, 6}, 1)
pairwise_fixtures = [
    (*close_fixture, len(close_fixture[0].difference(close_fixture[1]))),
    (*wide_fixture, len(wide_fixture[0].difference(wide_fixture[1]))),
]
for E, Gset, x, d in pairwise_fixtures:
    residue_degree, q = inverse_residue_degree(E, Gset, x)
    if residue_degree != d - 1:
        raise RuntimeError("inverse residue did not have exact degree d-1")
    predicted = residue_degree < width
    actual = escape_absorbed(E, Gset, x, width)
    if predicted != actual:
        raise RuntimeError("inverse-residue escape criterion failed")
    if d <= width and not actual:
        raise RuntimeError("close-pair automatic absorption failed")
    if d > width and actual:
        raise RuntimeError("wide pair unexpectedly absorbed")


# Rank-one/template-line classification in a complete-fiber toy.
# Over GF(13), phi=X^3 has four nonzero quotient labels, each with a
# complete three-point fiber in D=F^*.
K0 = GF(13)
SX.<Z> = PolynomialRing(K0)
ST.<T> = PolynomialRing(K0)
KT = ST.fraction_field()
phi = Z^3
D = list(K0)[1:]
fibers = {}
for z in D:
    fibers.setdefault(z^3, []).append(z)
if sorted(len(values) for values in fibers.values()) != [3, 3, 3, 3]:
    raise RuntimeError("complete-fiber toy failed")


def module_column(poly):
    """Coordinates in 1,Z,Z^2 over K0[T] for phi=Z^3."""
    rows = [ST.zero(), ST.zero(), ST.zero()]
    for exponent, coefficient in poly.dict().items():
        rows[exponent % 3] += coefficient * T^(exponent // 3)
    return vector(ST, rows)


def locator0(points):
    out = SX.one()
    for point in points:
        out *= Z - point
    return out


partial = K0(1)
partial_label = partial^3
moving_labels = sorted([b for b in fibers if b != partial_label])
line_locators = []
line_supports = []
for b in moving_labels:
    support = {partial}.union(fibers[b])
    line_supports.append(support)
    line_locators.append(locator0(support))

columns = [module_column(poly) for poly in line_locators]
matrix_line = matrix(KT, 3, len(columns),
                     [KT(columns[j][i]) for i in range(3)
                      for j in range(len(columns))])
if matrix_line.rank() != 1:
    raise RuntimeError("fixed template did not give one primitive locator line")

primitive = vector(ST, [-1, 1, 0])  # Z-1
if gcd(list(primitive)) != 1:
    raise RuntimeError("primitive locator column gcd")
for b, column in zip(moving_labels, columns):
    if column != (T - b) * primitive:
        raise RuntimeError("rank-one factorization mismatch")

# A different partial template gives a genuinely different primitive line.
partial2 = next(z for z in D if z^3 != partial_label)
label2 = partial2^3
moving2 = next(b for b in fibers if b != label2)
locator2 = locator0({partial2}.union(fibers[moving2]))
column2 = module_column(locator2)
two_line_matrix = matrix(KT, 3, 2,
                         [KT(columns[0][i]) if j == 0 else KT(column2[i])
                          for i in range(3) for j in range(2)])
if two_line_matrix.rank() != 2:
    raise RuntimeError("different templates collapsed to one primitive line")

# Each locator has the fixed partial point and one moving complete fiber.
for support, b in zip(line_supports, moving_labels):
    if support != {partial}.union(fibers[b]):
        raise RuntimeError("rank-one support decomposition mismatch")


# Canonical source-coset signature control (the depth-one analogue of
# Theorem 5.1).  Here phi=X^2 on GF(17)^*, agreement A=7, K=4, one partial
# agreement point, three complete agreement fibers, and one fixed quotient
# coefficient eta.  Equality modulo F[X]_<4 is exactly equality of the four
# high coefficients in degrees 4,...,7.
D1 = tuple(F(i) for i in range(1, 17))
Q1 = tuple(sorted(set(x^2 for x in D1), key=int))
source_keys = []
source_signatures = {}
scaled_signatures = {}
for beta in Q1:
    fiber = [x for x in D1 if x^2 == beta]
    available = [b for b in Q1 if b != beta]
    for point in fiber:
        buckets = {}
        for labels in combinations(available, 3):
            eta = -sum(labels)
            buckets.setdefault(eta, 0)
            buckets[eta] += 1
        for eta in buckets:
            center = (X - point) * (X^6 + eta * X^4)
            signature = tuple(center[j] for j in range(4, 8))
            key = (beta, point, eta)
            source_keys.append(key)
            source_signatures.setdefault(signature, []).append(key)
            for scalar in F:
                if scalar == 0:
                    continue
                scaled = tuple(scalar * entry for entry in signature)
                scaled_key = (key, scalar)
                scaled_signatures.setdefault(scaled, []).append(scaled_key)

if len(source_keys) != 256 or len(source_signatures) != 256:
    raise RuntimeError("canonical source signatures were not injective")
if max(len(values) for values in source_signatures.values()) != 1:
    raise RuntimeError("canonical source signature collision")
if len(scaled_signatures) != 4096:
    raise RuntimeError("projectively scaled source signatures collided")
if max(len(values) for values in scaled_signatures.values()) != 1:
    raise RuntimeError("scaled source signature collision")

print("PASS M31_C2048_VT_MULTITEMPLATE_GLOBAL_RANK_ROUTE_CUT_V1")
print("pairwise_selected_checks", len(pairwise_fixtures))
print("pairwise_close", close_fixture)
print("pairwise_wide", wide_fixture)
print("rank_one_line_size", len(line_locators))
print("different_template_rank", two_line_matrix.rank())
print("canonical_source_signatures", len(source_signatures))
print("scaled_source_signatures", len(scaled_signatures))
