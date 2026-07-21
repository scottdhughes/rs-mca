"""Independent Sage replay for the coupled escape--Forney route cut.

This is an exact finite-field and integer computation, not a proof of the
symbolic theorem and not a payment of the M31 ledger row.
"""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def deployed_thresholds():
    p_m31 = 2^31 - 1
    K_m31 = 2^20
    R_m31 = 981129
    D0 = K_m31 - R_m31
    S = 2 * R_m31 - K_m31 - 1

    width16 = S // (16 - 2)
    width15 = S // (15 - 2)
    width30 = (2 * S) // (30 - 2)
    width29 = (2 * S) // (29 - 2)
    space16 = (16 - 2) * (D0 + 1) - S

    forbidden67 = 67 * R_m31 + binomial(67, 2) * S
    forbidden68 = 68 * R_m31 + binomial(68, 2) * S
    margin67 = p_m31 - forbidden67
    excess68 = forbidden68 - p_m31

    require((D0, S) == (67447, 913681), "deployed D0/S changed")
    require((width16, width15) == (65262, 70283),
            "16/15 threshold changed")
    require(width16 < D0 < width15, "16/15 cutoff inequalities failed")
    require(13 * (D0 + 1) <= S, "15-column obstruction profile disappeared")
    require((width30, width29) == (65262, 67680),
            "30/29 threshold changed")
    require(width30 < D0 < width29, "30/29 cutoff inequalities failed")
    require(space16 == 30591, "16-column dimension lower bound changed")
    require((forbidden67, forbidden68) == (2085884334, 2148082090),
            "67/68 forbidden-hyperplane count changed")
    require((margin67, excess68) == (61599313, 598443),
            "67/68 threshold margins changed")
    require(forbidden67 < p_m31 < forbidden68,
            "67/68 hyperplane threshold inequalities failed")

    return {
        "D0": D0,
        "S": S,
        "width16": width16,
        "width15": width15,
        "width30": width30,
        "width29": width29,
        "space16": space16,
        "margin67": margin67,
        "excess68": excess68,
    }


def forney_profile(polynomials):
    """Recover the row indices from exact coefficient-map cokernels."""
    e = polynomials[0].degree()
    require(all(P.degree() == e for P in polynomials),
            "locator degrees are not uniform")
    cokers = []
    for multiplier_width in range(8):
        target_dimension = e + multiplier_width
        columns = []
        for P in polynomials:
            for shift in range(multiplier_width):
                Q = X^shift * P
                columns.append(vector(F, [Q[k] for k in range(target_dimension)]))
        if columns:
            coefficient_map = matrix(F, target_dimension, len(columns),
                                     lambda row, col: columns[col][row])
        else:
            coefficient_map = matrix(F, target_dimension, 0)
        cokers.append(target_dimension - coefficient_map.rank())

    require(cokers[-1] == 0, "coefficient maps did not reach surjectivity")
    greater_than = [cokers[d] - cokers[d + 1]
                    for d in range(len(cokers) - 1)]
    profile = [0] * ((len(polynomials) - 1) - greater_than[0])
    for cutoff in range(1, len(greater_than)):
        multiplicity = greater_than[cutoff - 1] - greater_than[cutoff]
        require(multiplicity >= 0, "cokernel sequence is not convex")
        profile.extend([cutoff] * multiplicity)
    require(len(profile) == len(polynomials) - 1,
            "failed to recover every locator-row index")
    return tuple(profile)


def gf11_full_layer():
    global F, X
    F = GF(11)
    R.<X> = PolynomialRing(F)
    domain = tuple(F(a) for a in range(8))
    K = 4
    moments = tuple(F(a) for a in (0, 0, 1, 0))

    def locator(points):
        return R.prod(X - a for a in points)

    def functional(P):
        require(P.degree() < len(moments), "functional moment range exceeded")
        return sum(P[k] * moments[k] for k in range(len(moments)))

    def divided_numerator(P):
        # lambda_X((P(X)-P(Y))/(X-Y)), returned as a polynomial in Y.
        answer = R.zero()
        for k in range(1, P.degree() + 1):
            for h in range(k):
                answer += P[k] * moments[k - 1 - h] * X^h
        return answer

    def exact_support(points):
        P = locator(points)
        if functional(P) != 0:
            return False
        return all(functional(P // (X - a)) != 0 for a in points)

    layer = tuple(points for points in combinations(domain, 3)
                  if exact_support(points))
    expected = (
        (F(0), F(4), F(7)),
        (F(0), F(5), F(6)),
        (F(1), F(3), F(7)),
        (F(1), F(4), F(6)),
        (F(2), F(3), F(6)),
        (F(2), F(4), F(5)),
    )
    require(layer == expected, "GF(11) full exact layer changed")
    common_core = set(layer[0])
    for support in layer[1:]:
        common_core.intersection_update(support)
    require(common_core == set(), "GF(11) fixture acquired a common core")

    locators = tuple(locator(points) for points in layer)
    numerators = tuple(divided_numerator(P) for P in locators)
    escapes = tuple(tuple(functional(P // (X - a)) for a in points)
                    for points, P in zip(layer, locators))
    require(all(B == R.one() for B in numerators),
            "GF(11) divided numerators changed")
    require(all(values == (F.one(), F.one(), F.one()) for values in escapes),
            "GF(11) escape values changed")

    locator_coefficients = matrix(F, [
        [P[degree] for P in locators] for degree in range(4)
    ])
    numerator_coefficients = matrix(F, [[B[0] for B in numerators]])
    joint_coefficients = locator_coefficients.stack(numerator_coefficients)
    locator_kernel = locator_coefficients.right_kernel()
    joint_kernel = joint_coefficients.right_kernel()
    require(locator_kernel.dimension() == 3,
            "constant locator-kernel dimension changed")
    require(joint_kernel.dimension() == 3,
            "constant joint-kernel dimension changed")
    for row in joint_kernel.basis():
        require(sum(row[i] * locators[i] for i in range(len(locators))) == 0,
                "constant locator relation failed")
        require(sum(row[i] * numerators[i] for i in range(len(numerators))) == 0,
                "constant numerator relation failed")

    profile = forney_profile(locators)
    require(profile == (0, 0, 0, 1, 2), "locator Forney profile changed")

    row_a, row_c = joint_kernel.basis()[:2]
    require(matrix(F, [row_a, row_c]).rank() == 2,
            "selected joint rows are not independent")
    deltas = matrix(F, len(locators), len(locators),
                    lambda i, j: row_a[i] * row_c[j] - row_a[j] * row_c[i])
    nonzero_minors = sum(1 for i, j in combinations(range(len(locators)), 2)
                         if deltas[i, j] != 0)
    require(nonzero_minors > 0, "selected independent rows lost every Pluecker minor")
    for i in range(len(locators)):
        require(sum(deltas[i, j] * locators[j]
                    for j in range(len(locators))) == 0,
                "Pluecker locator contraction failed")
        require(sum(deltas[i, j] * numerators[j]
                    for j in range(len(numerators))) == 0,
                "Pluecker numerator contraction failed")

    collision_energy = 0
    collision_allowance = 0
    cauchy_binet = R.zero()
    for i, j in combinations(range(len(locators)), 2):
        Pi, Pj = locators[i], locators[j]
        Bi, Bj = numerators[i], numerators[j]
        overlap = tuple(sorted(set(layer[i]).intersection(layer[j])))
        Q = Pi.gcd(Pj).monic()
        require(Q == locator(overlap), "pair gcd is not the overlap locator")
        omega = Pi * Bj - Pj * Bi
        require(omega != 0, "distinct reduced fractions became equal")
        quotient, remainder = omega.quo_rem(Q)
        require(remainder == 0, "pair gcd did not divide the cross determinant")

        union_excess = len(set(layer[i]).union(layer[j])) - (K + 1)
        require(quotient.degree() <= union_excess,
                "collision quotient exceeded the union-excess cap")
        for a in set(layer[i]).symmetric_difference(layer[j]):
            require(quotient(a) != 0,
                    "collision quotient vanished on a one-sided support point")

        pair_collisions = 0
        for a in overlap:
            rho_i = Bi(a) / Pi.derivative()(a)
            rho_j = Bj(a) / Pj.derivative()(a)
            is_collision = (rho_i == rho_j)
            require((quotient(a) == 0) == is_collision,
                    "quotient root/normalized-escape equivalence failed")
            pair_collisions += ZZ(is_collision)
        require(pair_collisions <= union_excess,
                "pair collision count exceeded the union-excess cap")
        collision_energy += pair_collisions
        collision_allowance += union_excess
        cauchy_binet += omega * deltas[i, j]

    require(cauchy_binet == 0, "Cauchy--Binet contraction failed")
    require((collision_energy, collision_allowance) == (0, 3),
            "collision-free route-cut totals changed")

    return {
        "layer_size": len(layer),
        "profile": profile,
        "kernel_dimension": joint_kernel.dimension(),
        "nonzero_minors": nonzero_minors,
        "pair_count": binomial(len(layer), 2),
        "collision_energy": collision_energy,
        "collision_allowance": collision_allowance,
    }


def common_core_factor_fixture():
    """Replay the coupled factor identity without discarding a core root."""
    global F, X
    F = GF(11)
    R.<X> = PolynomialRing(F)
    domain = tuple(F(a) for a in range(8))
    K = 4
    moments = tuple(F(a) for a in (1, 0, 1, 4))

    def locator(points):
        return R.prod(X - a for a in points)

    def functional(P):
        require(P.degree() < len(moments), "full functional moment range exceeded")
        return sum(P[k] * moments[k] for k in range(len(moments)))

    def divided_numerator(P, reduced_moments):
        answer = R.zero()
        for k in range(1, P.degree() + 1):
            for h in range(k):
                answer += P[k] * reduced_moments[k - 1 - h] * X^h
        return answer

    def exact_support(points):
        L = locator(points)
        return functional(L) == 0 and all(
            functional(L // (X - a)) != 0 for a in points
        )

    layer = tuple(points for points in combinations(domain, 3)
                  if exact_support(points))
    expected = (
        (F(0), F(1), F(3)),
        (F(1), F(2), F(4)),
        (F(1), F(5), F(7)),
    )
    require(layer == expected, "common-core GF(11) full layer changed")
    core = set(layer[0])
    for support in layer[1:]:
        core.intersection_update(support)
    require(core == {F(1)}, "common-core GF(11) intersection changed")

    G = locator(tuple(core))
    full_locators = tuple(locator(points) for points in layer)
    reduced_locators = tuple(L // G for L in full_locators)
    require(gcd(reduced_locators) == 1, "reduced locator row is not primitive")

    reduced_moments = tuple(functional(G * X^r) for r in range(K - len(core)))
    numerators = tuple(divided_numerator(P, reduced_moments)
                       for P in reduced_locators)
    require(all(B.gcd(P) == 1 for P, B in zip(reduced_locators, numerators)),
            "reduced numerator/locator pair ceased to be coprime")

    domain_locator = locator(domain)
    domain_derivative = domain_locator.derivative()
    dual_weights = {a: F.one() / domain_derivative(a) for a in domain}
    errors = []
    for support, L in zip(layer, full_locators):
        values = {a: F.zero() for a in domain}
        for a in support:
            escape = functional(L // (X - a))
            values[a] = escape / (dual_weights[a] * L.derivative()(a))
            require(values[a] != 0, "actual error lost an exact-support point")
        errors.append(values)

    gamma = F(10)
    require(gamma != 0, "coupled-factor scalar vanished")
    pair_count = 0
    core_checks = 0
    for i, j in combinations(range(len(layer)), 2):
        Pi, Pj = reduced_locators[i], reduced_locators[j]
        Bi, Bj = numerators[i], numerators[j]
        Q = Pi.gcd(Pj).monic()
        omega = Pi * Bj - Pj * Bi
        omega_over_q, omega_remainder = omega.quo_rem(Q)
        require(omega_remainder == 0, "reduced pair gcd did not divide Omega")

        # Since y=c_i+e_i=c_j+e_j, c_j-c_i=e_i-e_j.  Interpolate that
        # actual codeword from all domain values, rather than merely fitting
        # the union points.
        difference_values = {a: errors[i][a] - errors[j][a] for a in domain}
        codeword = sum(
            difference_values[a] * (domain_locator // (X - a)) / domain_derivative(a)
            for a in domain
        )
        require(codeword.degree() < K, "reconstructed difference is not a codeword")
        union = set(layer[i]).union(layer[j])
        require(all(codeword(a) == 0 for a in set(domain).difference(union)),
                "difference codeword escaped its support union")
        V = locator(tuple(sorted(set(domain).difference(union))))
        h, h_remainder = codeword.quo_rem(V)
        require(h_remainder == 0, "outside-union locator did not divide codeword")
        require(omega_over_q == gamma * h,
                "coupled Omega/Q and codeword/V factors changed scalar")
        for a in union:
            require(omega_over_q(a) == gamma * h(a),
                    "coupled factor identity failed on a union point")
        for a in core:
            require(a in union, "core point disappeared from a pair union")
            require(omega_over_q(a) == gamma * h(a),
                    "coupled factor identity failed at the core point")
            require(omega_over_q(a) != 0 and h(a) != 0,
                    "common-core factor check became vacuous")
            core_checks += 1
        pair_count += 1

    require((pair_count, core_checks, gamma) == (3, 3, F(10)),
            "common-core coupled-factor totals changed")
    return {
        "layer_size": len(layer),
        "core": next(iter(core)),
        "pair_count": pair_count,
        "core_checks": core_checks,
        "gamma": gamma,
    }


thresholds = deployed_thresholds()
fixture = gf11_full_layer()
core_fixture = common_core_factor_fixture()

print("M31_COUPLED_ESCAPE_FORNEY_PLUCKER_ROUTE_CUT_SAGE")
print("arithmetic=PASS D0={} S={} width16={} width15={}".format(
    thresholds["D0"], thresholds["S"], thresholds["width16"],
    thresholds["width15"]))
print("two_row=PASS width30={} width29={} space16={}".format(
    thresholds["width30"], thresholds["width29"], thresholds["space16"]))
print("joint_full_layer=PASS size={} forney={} joint_constant_rows={}".format(
    fixture["layer_size"], ",".join(str(v) for v in fixture["profile"]),
    fixture["kernel_dimension"]))
print("escape_pluecker=PASS nonzero_minors={}".format(
    fixture["nonzero_minors"]))
print("pair_collision=PASS pairs={} energy={} allowance={}".format(
    fixture["pair_count"], fixture["collision_energy"],
    fixture["collision_allowance"]))
print("common_core_factor=PASS size={} core={} pairs={} gamma={}".format(
    core_fixture["layer_size"], core_fixture["core"],
    core_fixture["pair_count"], core_fixture["gamma"]))
print("generic_avoidance=PASS max_packet=67 margin={} next_excess={}".format(
    thresholds["margin67"], thresholds["excess68"]))
print("RESULT=SAGE_REPLAY_PASS")
