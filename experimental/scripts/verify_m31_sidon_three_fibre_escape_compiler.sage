#!/usr/bin/env sage
"""Independent Sage replay for the M31 Sidon/three-fibre/escape packet."""

from itertools import combinations, permutations, product


def theta_matrix(polynomials, D):
    base = polynomials[0].base_ring()
    degree = max(poly.degree() for poly in polynomials)
    out = matrix(base, degree + D, len(polynomials) * D)
    for block, poly in enumerate(polynomials):
        for shift in range(D):
            for exponent, coefficient in enumerate(poly.list()):
                out[exponent + shift, block * D + shift] = coefficient
    return out


def parity_products(factors):
    A0, A1, B0, B1, C0, C1 = factors
    return (A0 * B0 * C0, A1 * B0 * C1, A0 * B1 * C1, A1 * B1 * C0)


def normalized_projective(vector):
    first = next(value for value in vector if value != 0)
    return vector / first


def normalized_pgl2(p):
    representatives = set()
    for entries in product(range(p), repeat=int(4)):
        a, b, c, d = entries
        if (a * d - b * c) % p == 0:
            continue
        first = next(value for value in entries if value)
        inverse = inverse_mod(first, p)
        representatives.add(tuple((value * inverse) % p for value in entries))
    return sorted(representatives)


def pgl_action(matrix_entries, point, p):
    a, b, c, d = matrix_entries
    denominator = (c * point + d) % p
    if denominator == 0:
        return None
    return ((a * point + b) * inverse_mod(denominator, p)) % p


# Exact deployed arithmetic and every defect cell.
p = 2^31 - 1
n = 2^21
K = 2^20
agreement = 1116023
sigma = agreement - K
radius = n - agreement
budget = p^4 // 2^100
forbidden = budget + 1
r = 33 * 1024
e = 3 * r
core = radius - e
assert (p, n, K, agreement) == (2147483647, 2097152, 1048576, 1116023)
assert (sigma, radius, budget, forbidden) == (67447, 981129, 16777215, 16777216)
assert (r, e, core) == (33792, 101376, 879753)
assert forbidden - K//2 == 16252928
assert radius - K//2 == 456841
assert ceil((forbidden - K//2) / (radius - K//2)) == 36
assert 16*(K-radius) - (K-1) == 30577
assert 36*(K-radius) - (K-1) == 1379517
assert 4*radius == 3924516
assert p - 4*radius == 2143559131
for tau in range(137):
    h = 137 - tau
    degree_lower = 2*r - 2*tau
    degree_upper = 2*r + 2*tau
    simple_lower = 2*r - 4*tau
    assert 1 <= h <= 137
    assert degree_lower <= degree_upper < p
    assert simple_lower > 0
assert (2*r-2*136, 2*r+2*136, 2*r-4*136, 6*136) == (67312, 67856, 67040, 816)
assert 6*r - 6*136 == 201936
assert 6*r - 12*136 == 201120


# The exact GF(2^24) modulus and an exhaustive GF(2^6) Sidon replay.
R2.<x2> = PolynomialRing(GF(2))
modulus24 = x2^24+x2^16+x2^15+x2^14+x2^13+x2^10+x2^9+x2^7+x2^5+x2^3+1
assert modulus24.is_irreducible()
F24.<z24> = GF(2^24, modulus=modulus24)
assert F24.cardinality() == forbidden

modulus6 = x2^6 + x2 + 1
assert modulus6.is_irreducible()
F64.<z6> = GF(2^6, modulus=modulus6)
pair_sums = {}
elements64 = list(F64)
for left, right in combinations(elements64, int(2)):
    key = (left + right, left^3 + right^3)
    assert key not in pair_sums
    pair_sums[key] = (left, right)
assert len(pair_sums) == binomial(64, 2)

# Simplex/direct-sum parameters.  A nonzero linear functional on F_2^12
# takes value one on exactly half of all vectors, hence on 2^11 nonzero
# coordinate columns.
assert 2^12 - 1 == 4095
assert 2^11 == 2048
assert 33*2048 == 67584
assert 4*33*4095 == 540540
assert radius - 4*33*4095 == 440589
assert n - 2*radius == 134894
assert agreement - 67584 == K - 137


# Literal Chebyshev T8/F31 census.
F31 = GF(31)
R31.<X> = PolynomialRing(F31)
T_previous = R31(1)
T_current = X
for degree in range(2, 9):
    T_previous, T_current = T_current, 2*X*T_current - T_previous
T8 = T_current
roots31 = tuple(Integer(value) for value in F31 if T8(value) == 0)
assert roots31 == (2, 5, 10, 11, 20, 21, 26, 29)

rank_counts = {3: 0, 4: 0}
escape_valid = 0
faces = set()
first_drop = None
for values in permutations(roots31, int(6)):
    a0, a1, b0, b1, c0, c1 = values
    factors = tuple(X - F31(value) for value in values)
    polynomials = parity_products(factors)
    theta = theta_matrix(polynomials, 1)
    rank = theta.rank()
    assert rank in rank_counts
    rank_counts[rank] += 1
    if rank != 3:
        continue
    if first_drop is None:
        first_drop = values
    functional = normalized_projective(theta.left_kernel().basis()[0])
    support_roots = (
        (a0, b0, c0),
        (a1, b0, c1),
        (a0, b1, c1),
        (a1, b1, c0),
    )
    all_guards = True
    for index, local_roots in enumerate(support_roots):
        for alpha in local_roots:
            direction = polynomials[index] // (X - F31(alpha))
            direction_vector = vector(F31, direction.list() + [F31(0)]*(4-len(direction.list())))
            if functional.dot_product(direction_vector) == 0:
                all_guards = False
    if all_guards:
        escape_valid += 1
    face = tuple(sorted(tuple(sorted(support)) for support in support_roots))
    faces.add(face)

assert rank_counts == {3: 720, 4: 19440}
assert escape_valid == 720
assert first_drop == (2, 5, 10, 20, 11, 29)
assert len(faces) == 30


# Exhaust the literal domain stabilizer and verify every one of the 30 faces
# has trivial support stabilizer.
pgl31 = normalized_pgl2(31)
assert len(pgl31) == 31*(31^2-1)
domain_set = set(roots31)
domain_stabilizer = []
for gamma in pgl31:
    image = [pgl_action(gamma, point, 31) for point in roots31]
    if None not in image and set(image) == domain_set:
        domain_stabilizer.append(gamma)
assert domain_stabilizer == [
    (1, 0, 0, 1),
    (1, 0, 0, 30),
    (1, 3, 1, 30),
    (1, 3, 30, 1),
    (1, 28, 1, 1),
    (1, 28, 30, 30),
]
for face in faces:
    target = set(face)
    stabilizer = []
    for gamma in domain_stabilizer:
        image = {
            tuple(sorted(pgl_action(gamma, point, 31) for point in support))
            for support in face
        }
        if image == target:
            stabilizer.append(gamma)
    assert stabilizer == [(1, 0, 0, 1)]

# Every nontrivial dyadic Chebyshev fold has uniform even fibres on D, so no
# three-point support in any surviving face is a union of complete fibres.
chebyshev = {1: X}
previous, current = R31(1), X
for degree in range(2, 9):
    previous, current = current, 2*X*current - previous
    if degree in (2, 4, 8):
        chebyshev[degree] = current
for fold_degree in (2, 4, 8):
    fibres = {}
    for point in roots31:
        value = chebyshev[fold_degree](F31(point))
        fibres.setdefault(value, set()).add(point)
    assert set(len(fibre) for fibre in fibres.values()) == {fold_degree}
    for face in faces:
        for support in face:
            selected_fibres = [fibre for fibre in fibres.values() if fibre <= set(support)]
            selected_union = set().union(*selected_fibres) if selected_fibres else set()
            assert selected_union != set(support)


# Explicit primitive source-valid fixture, Pluecker quotients, and full list.
fixture = (2, 5, 10, 20, 11, 29)
fixture_factors = tuple(X - F31(value) for value in fixture)
fixture_polynomials = parity_products(fixture_factors)
S = vector(R31, (1, 26, 18, 17))
T = vector(R31, (1, 23*X, 25*X+17, 14*X+14))
assert sum(S[index]*fixture_polynomials[index] for index in range(4)) == 0
assert sum(T[index]*fixture_polynomials[index] for index in range(4)) == 0
Delta = {(i, j): S[i]*T[j]-S[j]*T[i] for i in range(4) for j in range(i+1, 4)}
A0, A1, B0, B1, C0, C1 = fixture_factors
quotients = {
    "A0": Delta[1, 3] // A0,
    "A1": Delta[0, 2] // A1,
    "B0": Delta[2, 3] // B0,
    "B1": Delta[0, 1] // B1,
    "C0": Delta[1, 2] // C0,
    "C1": Delta[0, 3] // C1,
}
assert quotients == {"A0": 4, "A1": 25, "B0": 13, "B1": 23, "C0": 19, "C1": 14}
assert gcd(list(Delta.values())) == 1

qA0, qA1 = quotients["A0"], quotients["A1"]
qB0, qB1 = quotients["B0"], quotients["B1"]
qC0, qC1 = quotients["C0"], quotients["C1"]
MA = A0*A1*qA0*qA1
MB = B0*B1*qB0*qB1
MC = C0*C1*qC0*qC1
assert MA == MB + MC
g = gcd(MA, MC)
assert g == 1
NA, NB, NC = MA//g, MB//g, MC//g
assert gcd(NA, NB) == gcd(NA, NC) == gcd(NB, NC) == 1
assert NA.degree() == NB.degree() == NC.degree() == 2
assert set(NA.roots(multiplicities=False)) == {F31(2), F31(5)}
assert set(NB.roots(multiplicities=False)) == {F31(10), F31(20)}
assert set(NC.roots(multiplicities=False)) == {F31(11), F31(29)}

received = (28, 0, 21, 25, 0, 0, 0, 0)
explanations = (
    R31(0),
    30+23*X+11*X^2+4*X^3,
    12+26*X+2*X^2+25*X^3,
    29+17*X+4*X^2+13*X^3,
)
expected_supports = (
    {2, 10, 11},
    {5, 10, 29},
    {2, 20, 29},
    {5, 11, 20},
)
for explanation, expected in zip(explanations, expected_supports):
    support = {
        point for point, value in zip(roots31, received)
        if F31(value) - explanation(F31(point)) != 0
    }
    assert support == expected

radius_three = {}
weight_counts = {}
for coefficients in product(F31, repeat=int(4)):
    explanation = sum(coefficients[index]*X^index for index in range(4))
    support = tuple(
        point for point, value in zip(roots31, received)
        if F31(value) - explanation(F31(point)) != 0
    )
    if len(support) <= 3:
        assert support not in radius_three
        radius_three[support] = tuple(Integer(value) for value in coefficients)
        weight_counts[len(support)] = weight_counts.get(len(support), 0) + 1
assert weight_counts == {3: 5}
assert radius_three[(5, 21, 26)] == (22, 27, 29, 26)

print("M31 Sidon/three-fibre/escape Sage replay PASS")
print("GF(2^24) modulus irreducible; GF(2^6) Sidon census PASS")
print("T8/F31 census: 19440 rank4 + 720 rank3; all 720 escape-valid PASS")
print("30 unordered symmetry/dyadic-primitive faces; explicit closed list size 5 PASS")
print("RESULT: ESCAPE_AWARE_COMMON_HYPERPLANE_ACTIVATION_REQUIRED")
print("M31 rows remain OPEN; ledger movement 0")
