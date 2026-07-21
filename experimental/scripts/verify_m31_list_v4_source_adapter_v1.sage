"""Independent Sage controls for the M31 v4 LIST source adapter.

The finite-field fixtures below run over GF(11^2), with the evaluation
domain fixed inside the embedded GF(11).  They are exact toy-scale
cross-checks of field-generic identities.  They are not proofs of the
symbolic source-lift lemma, not v4 owners, not ledger payments, and not a
closure of the M31 row.

The deployed integer section only replays arithmetic consequences already
proved symbolically.  In particular, the final hyperplane check proves only
that the 67-support obstruction count is smaller than (2^31-1)^4.  It does
not assert a 68-support cutoff over the quartic field.
"""

from itertools import combinations


def require(condition, message):
    """An always-active assertion, including under optimized Python."""
    if not condition:
        raise RuntimeError(message)


# Use an explicit irreducible polynomial so that the extension and its
# embedded prime field are reproducible across Sage installations.
F0 = GF(11)
T.<T> = PolynomialRing(F0)
F.<z> = GF(11^2, modulus=T^2 + 1)
R.<X> = PolynomialRing(F)
S.<XX, YY> = PolynomialRing(F, 2)

DOMAIN = tuple(F(a) for a in range(8))
CODE_DIMENSION = 4
THETA = z + F(3)

require(z^2 == -F.one(), "explicit GF(11^2) modulus changed")
require(z^11 != z, "chosen extension generator fell into GF(11)")
require(THETA != 0 and THETA^11 != THETA,
        "fixture scalar is not genuinely extension-valued")
require(len(set(DOMAIN)) == len(DOMAIN), "evaluation domain is not distinct")
require(all(a^11 == a for a in DOMAIN),
        "evaluation domain left the embedded GF(11)")


def locator(points):
    return R.prod(X - a for a in points)


def functional(P, moments):
    require(P.degree() < len(moments), "functional moment range exceeded")
    return sum((P[k] * moments[k] for k in range(len(moments))), F.zero())


def divided_numerator(P, moments):
    """Compute lambda_X((P(X)-P(Y))/(X-Y)) in two independent ways."""
    by_coefficients = R.zero()
    for k in range(1, P.degree() + 1):
        for h in range(k):
            by_coefficients += P[k] * moments[k - 1 - h] * X^h

    p_x = sum((P[k] * XX^k for k in range(P.degree() + 1)), S.zero())
    p_y = sum((P[k] * YY^k for k in range(P.degree() + 1)), S.zero())
    divided = sum(
        (P[k] * sum((XX^(k - 1 - h) * YY^h for h in range(k)), S.zero())
         for k in range(1, P.degree() + 1)),
        S.zero(),
    )
    require((XX - YY) * divided == p_x - p_y,
            "bivariate divided-difference identity failed")

    by_bivariate = R.zero()
    for (x_degree, y_degree), coefficient in divided.dict().items():
        require(x_degree < len(moments),
                "bivariate functional moment range exceeded")
        by_bivariate += coefficient * moments[x_degree] * X^y_degree
    require(by_coefficients == by_bivariate,
            "coefficient and bivariate divided numerators disagree")
    return by_coefficients


def exact_layer(support_size, moments):
    """Enumerate the complete exact-support layer for one functional."""
    layer = []
    for support in combinations(DOMAIN, support_size):
        L = locator(support)
        if functional(L, moments) != 0:
            continue
        escapes = tuple(functional(L // (X - a), moments) for a in support)
        if all(value != 0 for value in escapes):
            layer.append(support)
    return tuple(layer)


DOMAIN_LOCATOR = locator(DOMAIN)
DOMAIN_DERIVATIVE = DOMAIN_LOCATOR.derivative()
DUAL_WEIGHTS = {a: F.one() / DOMAIN_DERIVATIVE(a) for a in DOMAIN}


def interpolate(values):
    answer = R.zero()
    for a in DOMAIN:
        answer += (
            values[a]
            * (DOMAIN_LOCATOR // (X - a))
            / DOMAIN_DERIVATIVE(a)
        )
    return answer


def exact_errors(layer, moments):
    """Recover extension-valued exact errors from all one-point escapes."""
    errors = []
    for support in layer:
        L = locator(support)
        values = {a: F.zero() for a in DOMAIN}
        for a in support:
            escape = functional(L // (X - a), moments)
            values[a] = escape / (DUAL_WEIGHTS[a] * L.derivative()(a))
            require(values[a] != 0, "one-point escape vanished")
        require({a for a in DOMAIN if values[a] != 0} == set(support),
                "recovered error does not have the advertised exact support")
        errors.append(values)

    # Make the first error the received word.  Every other difference must
    # interpolate to a degree-<K codeword, so all errors have one syndrome.
    received = dict(errors[0])
    codewords = []
    for error in errors:
        values = {a: received[a] - error[a] for a in DOMAIN}
        codeword = interpolate(values)
        require(codeword.degree() < CODE_DIMENSION,
                "equal-syndrome error difference is not an RS codeword")
        require(all(received[a] - codeword(a) == error[a] for a in DOMAIN),
                "received-word reconstruction failed")
        codewords.append(codeword)

    require(len(set(codewords)) == len(codewords),
            "distinct exact supports produced duplicate codewords")
    require(any(value^11 != value for error in errors for value in error.values()),
            "toy exact layer never left the embedded base field")
    return tuple(errors), tuple(codewords)


def no_core_full_layer_fixture():
    """Full extension-field layer, collisions, and three joint syzygies."""
    moments = tuple(THETA * F(a) for a in (0, 0, 1, 0))
    layer = exact_layer(3, moments)
    expected = (
        (F(0), F(4), F(7)),
        (F(0), F(5), F(6)),
        (F(1), F(3), F(7)),
        (F(1), F(4), F(6)),
        (F(2), F(3), F(6)),
        (F(2), F(4), F(5)),
    )
    require(layer == expected, "GF(11^2) complete no-core layer changed")

    core = set(layer[0])
    for support in layer[1:]:
        core.intersection_update(support)
    require(core == set(), "no-core full layer acquired a common root")

    locators = tuple(locator(support) for support in layer)
    numerators = tuple(divided_numerator(P, moments) for P in locators)
    require(all(B == THETA for B in numerators),
            "extension-valued divided numerators changed")
    require(gcd(locators) == R.one(), "no-core locator row is not primitive")
    require(all(P.gcd(B) == R.one() for P, B in zip(locators, numerators)),
            "a locator/numerator fraction is not reduced")

    errors, codewords = exact_errors(layer, moments)
    collision_energy = 0
    collision_allowance = 0
    pair_factor_checks = 0
    for i, j in combinations(range(len(layer)), 2):
        Pi, Pj = locators[i], locators[j]
        Bi, Bj = numerators[i], numerators[j]
        overlap = set(layer[i]).intersection(layer[j])
        union = set(layer[i]).union(layer[j])
        Q = Pi.gcd(Pj).monic()
        require(Q == locator(tuple(sorted(overlap))),
                "pair gcd is not the overlap locator")

        omega = Pi * Bj - Pj * Bi
        require(omega != 0, "distinct reduced fractions became equal")
        omega_over_q, remainder = omega.quo_rem(Q)
        require(remainder == 0, "pair gcd does not divide pair minor")

        difference = codewords[j] - codewords[i]
        V = locator(tuple(sorted(set(DOMAIN).difference(union))))
        h, h_remainder = difference.quo_rem(V)
        require(h_remainder == 0, "outside-union locator does not divide codeword")
        require(omega_over_q == -h,
                "pair minor is not the normalized collision polynomial")

        union_excess = len(union) - (CODE_DIMENSION + 1)
        require(h.degree() <= union_excess,
                "collision polynomial exceeded the union-excess cap")
        for a in set(layer[i]).symmetric_difference(layer[j]):
            require(h(a) != 0, "collision polynomial vanished on one-sided support")

        pair_collisions = 0
        for a in overlap:
            rho_i = Bi(a) / Pi.derivative()(a)
            rho_j = Bj(a) / Pj.derivative()(a)
            is_collision = (difference(a) == 0)
            require((h(a) == 0) == is_collision,
                    "collision-polynomial root equivalence failed")
            require((rho_i == rho_j) == is_collision,
                    "normalized-escape collision equivalence failed")
            pair_collisions += ZZ(is_collision)
        require(pair_collisions <= union_excess,
                "pair collision count exceeded the union-excess cap")
        collision_energy += pair_collisions
        collision_allowance += union_excess
        pair_factor_checks += 1

    require((pair_factor_checks, collision_energy, collision_allowance) == (15, 0, 3),
            "no-core pair/collision totals changed")

    # Five columns have a rank-three joint kernel over F[X].  The three
    # displayed Pluecker rows are independent over F(X) and annihilate both
    # the locator and divided-numerator rows.
    packet_locators = locators[:5]
    packet_numerators = numerators[:5]
    packet_size = len(packet_locators)

    def omega(i, j):
        return (
            packet_locators[i] * packet_numerators[j]
            - packet_locators[j] * packet_numerators[i]
        )

    pivot_minor = omega(0, 1)
    require(pivot_minor != 0, "joint-kernel pivot minor vanished")
    syzygies = []
    for k in range(2, packet_size):
        row = [R.zero() for _ in range(packet_size)]
        row[0] = omega(1, k)
        row[1] = -omega(0, k)
        row[k] = pivot_minor
        require(sum((row[i] * packet_locators[i] for i in range(packet_size)),
                    R.zero()) == 0,
                "Pluecker row failed on the locator row")
        require(sum((row[i] * packet_numerators[i] for i in range(packet_size)),
                    R.zero()) == 0,
                "Pluecker row failed on the numerator row")
        syzygies.append(row)

    fraction_field = R.fraction_field()
    joint_matrix = matrix(R, [packet_locators, packet_numerators])
    require(joint_matrix.change_ring(fraction_field).rank() == 2,
            "toy joint polynomial row lost rank two")
    require(matrix(R, syzygies).change_ring(fraction_field).rank() == 3,
            "three toy joint syzygies are not independent")
    require(packet_size - joint_matrix.change_ring(fraction_field).rank() == 3,
            "toy joint-kernel rank is not three")

    return {
        "layer_size": len(layer),
        "pair_checks": pair_factor_checks,
        "collision_energy": collision_energy,
        "joint_kernel_rank": 3,
    }


def common_core_fixture():
    """Nontrivial full-layer core and the exact determinantal identity."""
    moments = tuple(THETA * F(a) for a in (1, 0, 1, 4))
    layer = exact_layer(3, moments)
    expected = (
        (F(0), F(1), F(3)),
        (F(1), F(2), F(4)),
        (F(1), F(5), F(7)),
    )
    require(layer == expected, "GF(11^2) complete common-core layer changed")

    core = set(layer[0])
    for support in layer[1:]:
        core.intersection_update(support)
    require(core == {F(1)}, "full-layer common core changed")
    G = locator(tuple(core))

    full_locators = tuple(locator(support) for support in layer)
    reduced_locators = tuple(L // G for L in full_locators)
    require(gcd(reduced_locators) == R.one(),
            "common-core division did not make the locator row primitive")

    reduced_moments = tuple(
        functional(G * X^r, moments)
        for r in range(CODE_DIMENSION - len(core))
    )
    numerators = tuple(
        divided_numerator(P, reduced_moments) for P in reduced_locators
    )
    require(all(P.gcd(B) == R.one()
                for P, B in zip(reduced_locators, numerators)),
            "reduced common-core fractions are not coprime")

    errors, codewords = exact_errors(layer, moments)
    pair_checks = 0
    core_noncollision_checks = 0
    omegas = {}
    for i, j in combinations(range(len(layer)), 2):
        Pi, Pj = reduced_locators[i], reduced_locators[j]
        Bi, Bj = numerators[i], numerators[j]
        Q = Pi.gcd(Pj).monic()
        omega = Pi * Bj - Pj * Bi
        require(omega != 0, "common-core pair minor vanished")
        omegas[(i, j)] = omega
        omega_over_q, remainder = omega.quo_rem(Q)
        require(remainder == 0, "reduced overlap gcd does not divide pair minor")

        union = set(layer[i]).union(layer[j])
        difference = codewords[j] - codewords[i]
        V = locator(tuple(sorted(set(DOMAIN).difference(union))))
        h, h_remainder = difference.quo_rem(V)
        require(h_remainder == 0, "common-core difference did not factor")
        require(omega_over_q == -h,
                "common-core pair minor/collision factor identity failed")

        actual_overlap_locator = G * Q
        for a in set(layer[i]).intersection(layer[j]):
            require(actual_overlap_locator(a) == 0,
                    "actual overlap escaped G times the reduced pair gcd")
            require((h(a) == 0) == (difference(a) == 0),
                    "common-core collision root equivalence failed")
        for a in core:
            require(h(a) != 0 and omega_over_q(a) != 0,
                    "common-core factor check became vacuous")
            core_noncollision_checks += 1
        pair_checks += 1

    # For three columns, the complementary pair minors generate one joint
    # syzygy.  Removing their determinantal gcd gives its primitive row, and
    # its row degree is exactly tau-deg(d), the m=3 instance of the index sum.
    omega01 = omegas[(0, 1)]
    omega02 = omegas[(0, 2)]
    omega12 = omegas[(1, 2)]
    cofactor_row = (omega12, -omega02, omega01)
    require(sum((cofactor_row[i] * reduced_locators[i] for i in range(3)),
                R.zero()) == 0,
            "common-core cofactor row failed on locators")
    require(sum((cofactor_row[i] * numerators[i] for i in range(3)),
                R.zero()) == 0,
            "common-core cofactor row failed on numerators")

    determinantal_divisor = gcd((omega01, omega02, omega12)).monic()
    primitive_row = tuple(entry // determinantal_divisor for entry in cofactor_row)
    tau = max(omega.degree() for omega in (omega01, omega02, omega12))
    row_degree = max(entry.degree() for entry in primitive_row)
    require(row_degree == tau - determinantal_divisor.degree(),
            "toy joint-index/determinantal-divisor identity failed")

    fraction_field = R.fraction_field()
    joint_matrix = matrix(R, [reduced_locators, numerators])
    require(joint_matrix.change_ring(fraction_field).rank() == 2,
            "common-core joint row lost rank two")
    require(3 - joint_matrix.change_ring(fraction_field).rank() == 1,
            "common-core joint-kernel rank is not one")
    require((pair_checks, core_noncollision_checks) == (3, 3),
            "common-core pair totals changed")

    return {
        "layer_size": len(layer),
        "core_size": len(core),
        "pair_checks": pair_checks,
        "joint_kernel_rank": 1,
        "joint_index": row_degree,
    }


def deployed_integer_replay():
    """Replay the rank-three and global route-cut integers exactly."""
    p = 2^31 - 1
    K = 2^20
    RADIUS = 981129
    index_count = 44
    index_sum_max = 2 * RADIUS - K - 1
    cutoff = K - RADIUS

    quotient, remainder = divmod(index_sum_max, index_count)

    def ordered_prefix_max(prefix):
        return (
            prefix * quotient
            + max(0, remainder - (index_count - prefix))
        )

    prefix1 = ordered_prefix_max(1)
    prefix2 = ordered_prefix_max(2)
    prefix3 = ordered_prefix_max(3)
    prefix4 = ordered_prefix_max(4)
    require((index_sum_max, quotient, remainder) == (913681, 20765, 21),
            "deployed index-sum division changed")
    require((prefix1, prefix2, prefix3, prefix4) ==
            (20765, 41530, 62295, 83060),
            "deployed balanced prefix bounds changed")
    require(prefix3 < cutoff <= prefix4 and cutoff == 67447,
            "deployed rank-three cutoff comparison changed")

    signed_allowance = 259880
    require(4 * prefix3 == 249180,
            "four-union route-cut arithmetic changed")
    require(signed_allowance - 4 * prefix3 == 10700,
            "route-cut remainder changed")
    require(5 * prefix3 == 311475 > signed_allowance,
            "five-union obstruction changed")

    # This is deliberately only the valid quartic-field 67-support
    # nonforcing inequality.  No 68-support quantity is computed or used.
    hyperplanes_67 = 67 * RADIUS + binomial(67, 2) * index_sum_max
    quartic_field_size = p^4
    require(hyperplanes_67 == 2085884334,
            "67-support forbidden-hyperplane count changed")
    require(hyperplanes_67 < quartic_field_size,
            "67-support obstruction count no longer fits GF(p^4)")

    return {
        "index_sum_max": index_sum_max,
        "prefix3": prefix3,
        "cutoff": cutoff,
        "signed_remainder": signed_allowance - 4 * prefix3,
        "hyperplanes_67": hyperplanes_67,
        "quartic_field_size": quartic_field_size,
    }


no_core = no_core_full_layer_fixture()
with_core = common_core_fixture()
deployed = deployed_integer_replay()

print("M31_LIST_V4_SOURCE_ADAPTER_V1_SAGE")
print("scope=TOY_SCALE_CROSS_CHECK_NOT_PROOF_NOT_PAYMENT")
print("extension_domain=PASS field=GF(11^2) domain=embedded_GF(11) extension_values=true")
print("full_exact_layer=PASS size={} pair_checks={} collisions={}".format(
    no_core["layer_size"], no_core["pair_checks"],
    no_core["collision_energy"]))
print("common_core_divided_difference=PASS size={} core_size={} pairs={}".format(
    with_core["layer_size"], with_core["core_size"],
    with_core["pair_checks"]))
print("joint_kernel=PASS rank3_fixture={} core_rank={} core_index={}".format(
    no_core["joint_kernel_rank"], with_core["joint_kernel_rank"],
    with_core["joint_index"]))
print("deployed_rank3_arithmetic=PASS sum={} prefix3={} cutoff={} remainder={}".format(
    deployed["index_sum_max"], deployed["prefix3"], deployed["cutoff"],
    deployed["signed_remainder"]))
print("quartic_hyperplane_67=PASS count={} field_size={} no_68_cutoff_claim=true".format(
    deployed["hyperplanes_67"], deployed["quartic_field_size"]))
print("RESULT=SAGE_REPLAY_PASS")
