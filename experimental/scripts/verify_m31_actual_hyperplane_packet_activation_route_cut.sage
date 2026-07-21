#!/usr/bin/env sage
"""Independent Sage replay for the M31 36-packet activation route cut.

This verifier has two deliberately separate layers.

* The deployed layer uses exact M31 integers, the literal 36 subsets, and
  degree-16 Chebyshev algebra over GF(2^31-1).  It does not instantiate the
  degree-131072 fibre locators.
* The toy layer instantiates the same coefficient-module construction on the
  complete 64-point Chebyshev domain over GF(8191).  It constructs an explicit
  annihilating functional which is nonzero on every support escape.

The toy is a control for the linear-algebra mechanism, not a proof by scale.
The deployed proof still uses the symbolic degree bands and the finite-field
hyperplane-union argument recorded in the accompanying note/Python packet.
"""


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def ceil_div(numerator, denominator):
    return (numerator + denominator - 1) // denominator


def chebyshev_polynomial(degree, variable):
    """Standard T_d: T_0=1, T_1=X, T_d=2XT_{d-1}-T_{d-2}."""
    ring = variable.parent()
    if degree == 0:
        return ring.one()
    if degree == 1:
        return variable
    old = ring.one()
    current = variable
    for _ in range(2, degree + 1):
        old, current = current, 2 * variable * current - old
    return current


SUPPORTS = (
    (0, 4, 7, 8),
    (1, 6, 7, 10),
    (2, 4, 7, 11),
    (3, 4, 9, 11),
    (0, 5, 6, 8),
    (2, 5, 7, 9),
    (1, 3, 7, 9),
    (4, 5, 6, 10),
    (1, 2, 4, 8),
    (0, 6, 7, 11),
    (2, 4, 7, 8),
    (5, 9, 10, 11),
    (0, 2, 4, 10),
    (0, 3, 5, 8),
    (1, 3, 4, 9),
    (2, 8, 10, 11),
    (3, 6, 9, 11),
    (1, 3, 4, 10),
    (4, 5, 7, 10),
    (2, 3, 5, 7),
    (3, 8, 9, 10),
    (1, 7, 10, 11),
    (1, 3, 8, 9),
    (0, 4, 9, 10),
    (1, 6, 9, 10),
    (4, 5, 6, 8),
    (0, 2, 9, 11),
    (2, 6, 9, 11),
    (1, 4, 8, 10),
    (1, 6, 7, 11),
    (2, 3, 4, 10),
    (0, 1, 3, 11),
    (1, 3, 5, 6),
    (2, 4, 7, 9),
    (0, 4, 6, 7),
    (1, 5, 6, 7),
)


def bitmask(support):
    return sum(1 << index for index in support)


def coefficient_vector(polynomial, length):
    return vector(polynomial.base_ring(), [polynomial[index] for index in range(length)])


# ---------------------------------------------------------------------------
# Deployed exact arithmetic and the literal constant-weight Sidon packet.
# ---------------------------------------------------------------------------

p = 2^31 - 1
n = 2^21
K = 2^20
agreement = 1116023
sigma = agreement - K
radius = n - agreement
fibre_degree = 2^17
variable_degree = 4 * fibre_degree
common_core = radius - variable_degree

check(
    (p, n, K, agreement, sigma, radius)
    == (2147483647, 2097152, 1048576, 1116023, 67447, 981129),
    "deployed constants",
)
check(variable_degree == 524288, "variable degree")
check(common_core == 456841, "common-core size")
check(4 * fibre_degree >= common_core, "four unused fibres contain the core")
check(16 * fibre_degree == n, "sixteen complete fibres fill the domain")

identity_floor = ceil_div(binomial(n, agreement), p^sigma)
check(identity_floor == 1993678, "exact identity-prefix floor")

masks = [bitmask(support) for support in SUPPORTS]
check(len(SUPPORTS) == 36, "packet size")
check(all(len(support) == 4 for support in SUPPORTS), "constant weight four")
check(all(len(set(support)) == 4 for support in SUPPORTS), "no repeated label")
check(all(min(support) >= 0 and max(support) < 12 for support in SUPPORTS), "label range")
check(len(set(SUPPORTS)) == 36, "distinct supports")
check(len(set(masks)) == 36, "distinct incidence vectors")

pair_xors = {}
minimum_union_labels = 12
for left in range(36):
    for right in range(left + 1, 36):
        xor = masks[left] ^^ masks[right]
        check(xor not in pair_xors, "all 630 pair XORs are distinct")
        pair_xors[xor] = (left, right)
        minimum_union_labels = min(
            minimum_union_labels,
            len(set(SUPPORTS[left]).union(SUPPORTS[right])),
        )
check(len(pair_xors) == binomial(36, 2) == 630, "pair-XOR census")
check(minimum_union_labels == 5, "minimum pair union uses five fibres")
pair_union_floor = common_core + minimum_union_labels * fibre_degree
check(pair_union_floor == 1112201, "pair-union floor")
check(pair_union_floor - (K + 1) == 63624, "MDS-distance excess")

# The 36 locator rows lie in five T_s bands.  Since sigma<s, the top band of
# an escape of degree 4s-1 cannot occur, and the lower three bands end earlier.
module_dimension_ceiling = 5 * sigma
lower_band_ceiling = 3 * fibre_degree + sigma - 1
escape_degree = 4 * fibre_degree - 1
check(module_dimension_ceiling == 337235 < K, "five-band dimension ceiling")
check(lower_band_ceiling == 460662 < escape_degree == 524287, "escape degree gap")
check(p - 36 * radius == 2112163003 > 0, "deployed guard-union margin")


# ---------------------------------------------------------------------------
# Exact degree-16 Chebyshev fibre labels over the deployed field.
# ---------------------------------------------------------------------------

Fp = GF(p)
RY.<Y> = PolynomialRing(Fp)
T16 = chebyshev_polynomial(16, Y)
check(T16.degree() == 16, "T16 degree")
check(gcd(T16, T16.derivative()) == 1, "T16 squarefree")
deployed_roots_with_multiplicity = T16.roots()
check(len(deployed_roots_with_multiplicity) == 16, "T16 splits over GF(p)")
check(all(multiplicity == 1 for _, multiplicity in deployed_roots_with_multiplicity), "T16 simple roots")
betas = sorted((root for root, _ in deployed_roots_with_multiplicity), key=lambda value: int(value))
check(len(set(betas)) == 16, "sixteen distinct deployed fibre labels")

selected_betas = betas[:12]
q_rows = [prod(Y - selected_betas[index] for index in support) for support in SUPPORTS]
check(all(polynomial.degree() == 4 and polynomial.is_monic() for polynomial in q_rows), "monic quartic rows")
q_matrix = matrix(Fp, [coefficient_vector(polynomial, 5) for polynomial in q_rows])
check(q_matrix.rank() == 5, "quartic locator span has exact rank five")
check(gcd(q_rows) == 1, "quartic rows have no common fibre label")
check(set.intersection(*(set(support) for support in SUPPORTS)) == set(), "support labels have empty common intersection")


# ---------------------------------------------------------------------------
# Independent arithmetic for the universal 36-row Forney consequence.
# ---------------------------------------------------------------------------

# After removing a common core of size c, a primitive 1 x 36 locator row has
# 35 sorted Forney indices with total e=radius-c.  Failure of degree-D source
# surjectivity forces the largest index >=D+1, where D=K-radius.  At c=0 the
# remaining 34 indices therefore have the worst-case sum below.
D = K - radius
forney_low_sum_ceiling = 2 * radius - K - 1
check(D == sigma == 67447, "source degree D")
check(forney_low_sum_ceiling == 913681, "low-index sum ceiling")

mu1_ceiling = forney_low_sum_ceiling // 34
mu12_ceiling = forney_low_sum_ceiling // 17
large_low_indices_ceiling = forney_low_sum_ceiling // D
indices_strictly_below_D_floor = 34 - large_low_indices_ceiling
check(mu1_ceiling == 26872, "mu1 ceiling")
check(mu12_ceiling == 53745 < D, "mu1+mu2 ceiling")
check(large_low_indices_ceiling == 13, "at most thirteen low-side indices reach D")
check(indices_strictly_below_D_floor == 21, "at least twenty-one indices lie below D")

# Exhaust the two extremal integer implications rather than only recomputing
# their quotients.  A violation would force a sum strictly above the ceiling.
check(34 * (mu1_ceiling + 1) > forney_low_sum_ceiling, "mu1 extremality")
check(17 * (mu12_ceiling + 1) > forney_low_sum_ceiling, "mu1+mu2 extremality")
check(14 * D > forney_low_sum_ceiling, "twenty-one-small-index extremality")


# ---------------------------------------------------------------------------
# Literal small Chebyshev/RS coefficient-module replay over GF(8191).
# ---------------------------------------------------------------------------

toy_p = 8191
toy_field = GF(toy_p)
RX.<X> = PolynomialRing(toy_field)
toy_fibre_degree = 4
toy_sigma = 2
toy_common_core_size = 3
toy_variable_degree = 4 * toy_fibre_degree
toy_radius = toy_common_core_size + toy_variable_degree
toy_K = toy_radius + toy_sigma

toy_T4 = chebyshev_polynomial(4, X)
toy_T16 = chebyshev_polynomial(16, X)
toy_T64 = chebyshev_polynomial(64, X)
check(toy_T16(toy_T4) == toy_T64, "toy Chebyshev composition T16 o T4 = T64")

toy_domain = sorted((root for root, multiplicity in toy_T64.roots()), key=lambda value: int(value))
check(len(toy_domain) == 64, "toy T64 has 64 roots")
check(gcd(toy_T64, toy_T64.derivative()) == 1, "toy domain is simple")

toy_labels = sorted((root for root, multiplicity in toy_T16.roots()), key=lambda value: int(value))
check(len(toy_labels) == 16, "toy T16 has 16 labels")
toy_fibres = {
    beta: tuple(root for root in toy_domain if toy_T4(root) == beta)
    for beta in toy_labels
}
check(all(len(fibre) == 4 for fibre in toy_fibres.values()), "toy fibres are exactly four-to-one")
check(len(set().union(*(set(fibre) for fibre in toy_fibres.values()))) == 64, "toy fibres partition the domain")

toy_selected_labels = toy_labels[:12]
toy_unused_points = sorted(
    set().union(*(set(toy_fibres[beta]) for beta in toy_labels[12:])),
    key=lambda value: int(value),
)
toy_core = tuple(toy_unused_points[:toy_common_core_size])
toy_core_locator = prod(X - point for point in toy_core)
toy_fibre_locators = [toy_T4 - beta for beta in toy_selected_labels]
toy_variable_locators = [
    prod(toy_fibre_locators[index] for index in support)
    for support in SUPPORTS
]
toy_full_locators = [toy_core_locator * locator for locator in toy_variable_locators]
check(all(locator.degree() == toy_radius for locator in toy_full_locators), "toy full locator degrees")

toy_support_points = []
for support in SUPPORTS:
    points = set(toy_core)
    for index in support:
        points.update(toy_fibres[toy_selected_labels[index]])
    toy_support_points.append(tuple(sorted(points, key=lambda value: int(value))))
check(all(len(points) == toy_radius for points in toy_support_points), "toy support sizes")
check(
    all(
        len(set(toy_support_points[i]).union(toy_support_points[j])) >= toy_common_core_size + 5 * toy_fibre_degree > toy_K
        for i in range(36)
        for j in range(i + 1, 36)
    ),
    "toy pair unions exceed K",
)

# I=sum_i L_i * F[X]_{<sigma}, embedded in F[X]_{<K}.
toy_generators = [
    locator * X^shift
    for locator in toy_full_locators
    for shift in range(toy_sigma)
]
toy_generator_matrix = matrix(
    toy_field,
    [coefficient_vector(polynomial, toy_K) for polynomial in toy_generators],
).transpose()
check(toy_generator_matrix.rank() == 5 * toy_sigma == 10, "toy module has exact five-band rank")

# Removing any support point gives the escape L_i/(X-alpha).  Check every one
# directly against I.  This includes both variable-fibre and common-core points.
toy_escape_vectors = []
toy_escape_metadata = []
toy_rank = toy_generator_matrix.rank()
for support_index, (locator, points) in enumerate(zip(toy_full_locators, toy_support_points)):
    for point in points:
        quotient, remainder = locator.quo_rem(X - point)
        check(remainder == 0 and quotient.degree() == toy_radius - 1, "toy escape division")
        escape_vector = coefficient_vector(quotient, toy_K)
        augmented = toy_generator_matrix.augment(matrix(toy_field, toy_K, 1, list(escape_vector)))
        check(augmented.rank() == toy_rank + 1, "every toy escape lies outside I")
        toy_escape_vectors.append(escape_vector)
        toy_escape_metadata.append((support_index, int(point)))
check(len(toy_escape_vectors) == 36 * toy_radius == 684 < toy_p, "toy guard count below field size")

# Construct an explicit functional lambda in Ann(I) avoiding all 684 guard
# hyperplanes.  The polynomial curve sum_j t^j b_j through an annihilator
# basis is deterministic.  Every guard gives a nonzero polynomial in t; the
# degree/root union is <8191, so scanning t must find a survivor.
annihilator_basis = toy_generator_matrix.transpose().right_kernel().basis()
check(len(annihilator_basis) == toy_K - toy_rank == 11, "toy annihilator dimension")
for escape in toy_escape_vectors:
    check(any(basis_vector.dot_product(escape) != 0 for basis_vector in annihilator_basis), "guard restricts nontrivially to Ann(I)")
check(len(toy_escape_vectors) * (len(annihilator_basis) - 1) < toy_p, "polynomial-curve union bound")

toy_functional = None
toy_parameter = None
for parameter_as_integer in range(toy_p):
    parameter = toy_field(parameter_as_integer)
    candidate = sum(
        (parameter^index) * basis_vector
        for index, basis_vector in enumerate(annihilator_basis)
    )
    if all(candidate.dot_product(escape) != 0 for escape in toy_escape_vectors):
        toy_functional = candidate
        toy_parameter = parameter_as_integer
        break
check(toy_functional is not None, "construct explicit all-guard toy functional")
check(toy_generator_matrix.transpose() * toy_functional == 0, "toy functional annihilates I")
check(all(toy_functional.dot_product(escape) != 0 for escape in toy_escape_vectors), "toy functional misses every escape hyperplane")

print("Sage M31 actual-hyperplane packet activation route cut: PASS")
print("deployed identity-prefix floor:", identity_floor)
print("36-packet pair XORs:", len(pair_xors), "(all distinct)")
print("deployed T16 roots:", len(betas), "quartic span rank:", q_matrix.rank())
print("Forney ceilings: S=%s mu1<=%s mu1+mu2<=%s; >=%s indices <D" % (
    forney_low_sum_ceiling,
    mu1_ceiling,
    mu12_ceiling,
    indices_strictly_below_D_floor,
))
print("toy module: GF(%s), n=64, K=%s, rank(I)=%s, guards=%s, lambda parameter=%s" % (
    toy_p,
    toy_K,
    toy_rank,
    len(toy_escape_vectors),
    toy_parameter,
))
print("scope: deployed packet route cut + literal small coefficient-module control")
print("M31 global theorem: OPEN; ledger movement: 0")
