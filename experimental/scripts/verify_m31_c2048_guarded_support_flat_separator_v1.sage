#!/usr/bin/env sage
"""Independent Sage replay for the guarded support-flat separator interface."""


def require(condition, label):
    if not condition:
        raise AssertionError(label)


# A small exact MDS fixture over GF(11).
F = GF(11)
n = 6
k = 3
points = list(F)[:n]
G = Matrix(F, [[x^j for x in points] for j in range(k)])
require(G.rank() == k, "toy RS generator rank")
H = G.right_kernel_matrix()
require(H.nrows() == n-k and H.ncols() == n, "toy dual dimensions")
require(G*H.transpose() == 0, "toy dual orthogonality")
v_dim = H.nrows()
radius = 2
w = v_dim-radius
require(w == 1 and radius < n-k+1, "toy boundary parameters")


def shortened_coeff_space(E):
    """Coefficient vectors a with a*H supported outside E."""
    restricted = H.matrix_from_columns(sorted(E))
    return restricted.transpose().right_kernel()


def annihilator_basis(space):
    if space.dimension() == 0:
        return VectorSpace(F, v_dim)
    matrix = Matrix(F, space.basis())
    return matrix.right_kernel()


supports = [frozenset(E) for E in Subsets(range(n), radius)]
spaces = {E: shortened_coeff_space(E) for E in supports}
for E in supports:
    require(spaces[E].dimension() == w, "toy shortened dimension")
    for x in E:
        extension = shortened_coeff_space(E.difference({x}))
        require(extension.dimension() == w+1, "toy escape dimension")
        require(spaces[E].is_subspace(extension), "toy flat inside escape")


# Search a literal two-support failure of VT.  Since 2R<|F|, union avoidance
# must produce an actual nonzero syndrome satisfying both exact supports.
chosen = None
for i in range(len(supports)):
    for j in range(i+1, len(supports)):
        E1 = supports[i]
        E2 = supports[j]
        X = spaces[E1] + spaces[E2]
        if X.dimension() == v_dim:
            continue
        absorbed = False
        for E in (E1, E2):
            for x in E:
                if shortened_coeff_space(E.difference({x})).is_subspace(X):
                    absorbed = True
        if not absorbed:
            chosen = (E1, E2, X)
            break
    if chosen is not None:
        break
require(chosen is not None, "toy VT-failure family exists")
E1, E2, X = chosen
L = annihilator_basis(X)
require(L.dimension() >= 1, "toy common annihilator nonzero")

good = []
for phi in L:
    if phi == 0:
        continue
    valid = True
    for E in (E1, E2):
        for x in E:
            extension = shortened_coeff_space(E.difference({x}))
            if all(phi.dot_product(v) == 0 for v in extension.basis()):
                valid = False
    if valid:
        good.append(phi)
require(len(good) > 0, "toy union avoidance survivor")
phi = good[0]

# Syndrome surjectivity: H*y^T=phi on the chosen dual basis.
y = H.solve_right(vector(F, phi))
require(H*y == vector(F, phi), "toy syndrome realization")
for E in (E1, E2):
    require(all(phi.dot_product(v) == 0 for v in spaces[E].basis()),
            "toy flat containment")
    for x in E:
        extension = shortened_coeff_space(E.difference({x}))
        require(any(phi.dot_product(v) != 0 for v in extension.basis()),
                "toy one-point escape")


# Independent locator-coefficient realization and rank-increment tests.
R.<T> = PolynomialRing(F)


def coefficient_vector(poly, length):
    return vector(F, [poly[i] for i in range(length)])


def locator_space(E):
    locator = prod(T-points[i] for i in E)
    rows = [coefficient_vector(T^r*locator, k) for r in range(k-len(E))]
    return span(F, rows), locator


for E in supports:
    flat, locator = locator_space(E)
    require(flat.dimension() == w, "toy locator flat dimension")
    for x in E:
        extension, smaller = locator_space(E.difference({x}))
        require(flat.is_subspace(extension), "toy locator escape inclusion")
        require(extension.dimension() == flat.dimension()+1,
                "toy locator escape quotient one")
        require(locator == (T-points[x])*smaller,
                "toy locator division identity")


# A pinned rank-16 fixture over GF(67^2).  The first fifteen support flats
# are independent, the sixteenth remains compatible, every one-point escape
# is proper, and one one-point support mutation forces VT1.
Ft = GF(67^2, name="a")
Rt.<Z> = PolynomialRing(Ft)
toy_n = 62
toy_K = 31
toy_radius = 29
toy_w = toy_K-toy_radius
toy_masks = [
    0x289c74a698305b3e, 0x0a9e14273591cfc8,
    0x085c2b48f3fca189, 0x1363292c82cbeae1,
    0x1c93b8f7170700c5, 0x0e472f050a2af8d3,
    0x3990613b5110fada, 0x0ae93d41d5a88669,
    0x02f8b93c467740b8, 0x02c449e8c56b7e83,
    0x094eb825472cbb92, 0x3708c32432f86bc3,
    0x06d753ab0b001f6a, 0x041de1e33233cea2,
    0x11c1d60b357740ab, 0x3c5f30c93700d1f0,
]


def mask_support(mask):
    return [i for i in range(toy_n) if (mask >> i) & 1]


def rt_coefficients(poly):
    return vector(Ft, [poly[i] for i in range(toy_K)])


toy_supports = [mask_support(mask) for mask in toy_masks]
require(len(set(toy_masks)) == 16, "rank-16 fixture support uniqueness")
require(all(len(E) == toy_radius for E in toy_supports),
        "rank-16 fixture support weights")
toy_locators = [prod(Z-Ft(i) for i in E) for E in toy_supports]
require(all((-L[28], L[27]) == (Ft(40), Ft(58)) for L in toy_locators),
        "rank-16 common locator prefix")

toy_rows = []
for L in toy_locators:
    toy_rows.extend([rt_coefficients(L), rt_coefficients(Z*L)])
M15 = Matrix(Ft, toy_rows[:30])
M16 = Matrix(Ft, toy_rows)
require(M15.rank() == 30 and M16.rank() == 30,
        "rank-16 compatible shifted ranks")
lambda_coeff = vector(Ft, [0]*28+[1, 40, 1])
require(all(row*lambda_coeff == 0 for row in toy_rows),
        "rank-16 explicit annihilator")

escape_count = 0
for E, L in zip(toy_supports, toy_locators):
    for x in E:
        Q, rem = L.quo_rem(Z-Ft(x))
        require(rem == 0, "rank-16 exact locator division")
        qrow = rt_coefficients(Q)
        require(qrow*lambda_coeff == 1,
                "rank-16 explicit escape evaluation")
        require(Matrix(Ft, toy_rows+[qrow]).rank() == toy_K,
                "rank-16 escape raises rank")
        escape_count += 1
require(escape_count == 464 and escape_count < Ft.cardinality(),
        "rank-16 target-field escape union gate")

negative_mask = 0x3c5f30c93700d1e1
negative_support = mask_support(negative_mask)
require(set(negative_support) ==
        (set(toy_supports[-1]).difference({4}).union({0})),
        "rank-16 negative support mutation")
negative_locator = prod(Z-Ft(i) for i in negative_support)
negative_rows = toy_rows[:30] + [
    rt_coefficients(negative_locator),
    rt_coefficients(Z*negative_locator),
]
require(Matrix(Ft, negative_rows).rank() == toy_K,
        "rank-16 negative mutation forces VT1")


# Deployed arithmetic and first containment-rank gate.
p = 2^31 - 1
q = p^4
N = 2^21
K = 2^20
A = 1116023
boundary_radius = N-A
boundary_w = K-boundary_radius
B_star = p^4 // 2^100
require((boundary_radius, boundary_w, B_star) ==
        (981129, 67447, 16777215), "deployed constants")
require(15*boundary_w == 1011705 and K-15*boundary_w == 36871,
        "fifteen-support automatic compatibility")
require(16*boundary_w == 1079152 and 16*boundary_w-K == 30576,
        "sixteen-support excess")
require(16*boundary_w-(K-1) == 30577,
        "sixteen-support compatible nullity")

gates = [
    (9216781, 9042852106878),
    (16773485, 16456953545694),
    (16777215, 16460613156864),
]
for U, expected_guards in gates:
    guards = (U+1)*boundary_radius
    require(guards == expected_guards, "deployed guard product")
    require(guards < q, "target-field union gate")

print("M31 c=2048 guarded support-flat Sage replay")
print("toy_supports=%d chosen=%s,%s survivor_count=%d" %
      (len(supports), sorted(E1), sorted(E2), len(good)))
print("support-flat/escape/syndrome realization: PASS")
print("shifted-locator rank interface: PASS")
print("GF(67^2) guarded rank-16 fixture: PASS")
print("union gates and 15/16 threshold: PASS")
