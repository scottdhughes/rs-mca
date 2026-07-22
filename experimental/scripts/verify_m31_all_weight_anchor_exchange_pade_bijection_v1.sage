"""Independent Sage replay for the all-weight anchor-exchange Padé map.

This script deliberately imports no code from the primary Python verifier.  It
checks the corrected row orientation of the interpolation module and exhausts
two small finite-field models.  These are exact universal-identity controls;
they are not a deployed Mersenne-31 list bound.

Rows are ordered as ``(W, N)``.  For a translated anchor zero codeword, put

    U = A0*H0,  Lambda_D = A0*L0,  V*H0 = 1 (mod L0).

Then

    M_U = {(W,N): N = W*U (mod Lambda_D)}

has the ordered basis ``(L0,0), (V,A0)``.  The exchange variables ``(G,b)``
are *not* those basis coordinates.  If

    H = gcd(L0, G-b*V),

then the reconstructed census row has basis coordinates

    alpha = (G-b*V)/H,  beta = b*L0/H.
"""

from itertools import combinations, product


class ContractRejected(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def locator(PR, points):
    answer = PR.one()
    X = PR.gen()
    for point in points:
        answer *= X - point
    return answer


def exact_quotient(numerator, denominator, label):
    quotient, remainder = numerator.quo_rem(denominator)
    require(remainder == 0, "%s is not an exact quotient" % label)
    return quotient


def bounded_polynomials(PR, elements, bound):
    """All polynomials of degree strictly below ``bound``."""
    require(bound >= 0, "negative coefficient bound")
    for coefficients in product(elements, repeat=bound):
        yield PR(list(coefficients))


def polynomial_key(polynomial):
    return tuple(polynomial.list())


def pair_key(G, b):
    return (polynomial_key(G), polynomial_key(b))


def codeword_key(c, K):
    return tuple(c[i] for i in range(K))


def monic_gcd(first, second):
    answer = first.gcd(second)
    require(answer != 0, "zero gcd")
    return answer.monic()


def build_anchor_data(field, PR, domain, K, radius, values):
    """Build the translated-anchor data, rejecting the j0=0 edge."""
    n = len(domain)
    require(len(values) == n, "received word length")
    require(len(set(domain)) == n, "domain points must be distinct")
    require(0 < K < n, "RS dimension range")

    U = PR.lagrange_polynomial(list(zip(domain, values)))
    require(U.degree() < n, "interpolant degree")
    S0 = tuple(point for point in domain if U(point) == 0)
    E0 = tuple(point for point in domain if U(point) != 0)
    s0 = len(S0)
    j0 = len(E0)
    if j0 == 0:
        raise ContractRejected(
            "j0=0 has H0=0 and no inverse V; it is outside this adapter"
        )
    require(j0 <= radius, "the translated anchor is not listed")

    A0 = locator(PR, S0)
    L0 = locator(PR, E0)
    Lambda = locator(PR, domain)
    require(A0 * L0 == Lambda, "anchor locator partition")
    H0 = exact_quotient(U, A0, "U/A0")
    require(H0.degree() < j0, "H0 degree cap")
    require(H0.gcd(L0).degree() == 0, "H0 is not a unit modulo L0")
    V = H0.inverse_mod(L0) % L0
    require(V.degree() < j0, "reduced inverse degree")
    require((V * H0 - 1) % L0 == 0, "inverse congruence")

    return {
        "field": field,
        "PR": PR,
        "domain": domain,
        "K": K,
        "radius": radius,
        "n": n,
        "U": U,
        "S0": S0,
        "E0": E0,
        "s0": s0,
        "j0": j0,
        "w0": s0 - K,
        "A0": A0,
        "L0": L0,
        "Lambda": Lambda,
        "H0": H0,
        "V": V,
    }


def in_module(data, W, N):
    return (N - W * data["U"]) % data["Lambda"] == 0


def verify_oriented_basis(data):
    """Check the (W,N) orientation and exact coordinate recovery."""
    PR = data["PR"]
    X = PR.gen()
    A0 = data["A0"]
    L0 = data["L0"]
    V = data["V"]

    # Correct ordered rows: (L0,0), (V,A0).
    require(in_module(data, L0, PR.zero()), "first oriented basis row")
    require(in_module(data, V, A0), "second oriented basis row")
    require(L0 * A0 == data["Lambda"], "oriented basis determinant")
    # Swapping the two coordinates gives the old, incorrectly oriented rows.
    require(not (
        in_module(data, PR.zero(), L0)
        and in_module(data, A0, V)
    ), "coordinate-swapped basis was incorrectly accepted")

    probes = (PR.zero(), PR.one(), X, X + 1)
    rows_checked = 0
    for alpha in probes:
        for beta in probes:
            W = alpha * L0 + beta * V
            N = beta * A0
            require(in_module(data, W, N), "basis combination left module")
            beta_recovered = exact_quotient(N, A0, "module beta")
            alpha_recovered = exact_quotient(
                W - beta_recovered * V, L0, "module alpha"
            )
            require(alpha_recovered == alpha, "alpha recovery")
            require(beta_recovered == beta, "beta recovery")
            rows_checked += 1
    return rows_checked


def enumerate_exchange_pairs(data):
    """Enumerate exactly the admissible (G,b) side of the bijection."""
    PR = data["PR"]
    elements = tuple(data["field"])
    output = {}
    h_histogram = {}
    pregate_H_one = 0
    for g in range(max(0, data["w0"] + 1), data["s0"] + 1):
        coefficient_bound = g - data["w0"]
        require(coefficient_bound >= 1, "nonpositive b coefficient bound")
        for G_support in combinations(data["S0"], g):
            G = locator(PR, G_support)
            require(G.is_monic(), "G normalization")
            require(data["A0"] % G == 0, "G does not divide A0")
            for b in bounded_polynomials(PR, elements, coefficient_bound):
                if b == 0 or b.gcd(G).degree() != 0:
                    continue
                difference = G - b * data["V"]
                H = monic_gcd(data["L0"], difference)
                h = H.degree()
                threshold = data["j0"] + g - data["radius"]
                if H == 1:
                    pregate_H_one += 1
                if h < threshold:
                    continue

                key = pair_key(G, b)
                require(key not in output, "duplicate exchange pair")
                output[key] = (G, b, H)
                h_histogram[(g, h)] = h_histogram.get((g, h), 0) + 1
    return output, h_histogram, pregate_H_one


def pair_to_codeword(data, G, b, H):
    """Reverse map, including the corrected module-coordinate identity."""
    PR = data["PR"]
    g = G.degree()
    h = H.degree()
    t = data["radius"] - data["j0"]
    w = data["n"] - data["radius"] - data["K"]
    m = g - t
    require(data["w0"] == w + t, "slack-normal w0=w+t")
    require(m >= w + 1, "slack-normal m>=w+1")
    require(b.degree() < m - w, "slack-normal degree bound")
    require(H == monic_gcd(data["L0"], G - b * data["V"]), "full H")
    require(h >= data["j0"] + g - data["radius"], "exchange threshold")
    require(h >= m, "slack-normal h>=m")

    A0_over_G = exact_quotient(data["A0"], G, "A0/G")
    L0_over_H = exact_quotient(data["L0"], H, "L0/H")
    c = A0_over_G * b
    require(c.degree() < data["K"], "reconstructed codeword degree")

    W = G * L0_over_H
    N = W * c
    require(N == data["A0"] * b * L0_over_H, "Padé numerator identity")
    alpha = exact_quotient(G - b * data["V"], H, "exchange alpha")
    beta = b * L0_over_H
    require(W == alpha * data["L0"] + beta * data["V"],
            "corrected W-coordinate identity")
    require(N == beta * data["A0"], "corrected N-coordinate identity")
    require(in_module(data, W, N), "reconstructed row outside module")

    errors = tuple(point for point in data["domain"]
                   if data["U"](point) != c(point))
    require(len(errors) == data["j0"] + g - h, "weight formula")
    require(len(errors) == data["radius"] + m - h,
            "slack-normal j=R+m-h")
    require(len(errors) <= data["radius"], "reverse codeword is not listed")
    require(locator(PR, errors) == W, "exact error locator")
    return c, W, N, alpha, beta


def codeword_to_pair(data, c):
    """Forward map from a nonanchor listed codeword."""
    PR = data["PR"]
    require(c != 0, "anchor sent through nonanchor map")
    errors = tuple(point for point in data["domain"]
                   if data["U"](point) != c(point))
    require(len(errors) <= data["radius"], "unlisted forward codeword")

    G_support = tuple(point for point in data["S0"] if c(point) != 0)
    G = locator(PR, G_support)
    g = G.degree()
    require(g >= data["w0"] + 1, "nonzero polynomial zero-count gate")
    b = exact_quotient(c * G, data["A0"], "forward b")
    require(b != 0, "forward b vanished")
    require(b.degree() < g - data["w0"], "forward b degree")
    require(b.gcd(G).degree() == 0, "forward exact-new-error gate")
    H = monic_gcd(data["L0"], G - b * data["V"])
    h = H.degree()
    require(h >= data["j0"] + g - data["radius"], "forward threshold")
    require(locator(PR, errors) == G * exact_quotient(data["L0"], H, "forward L0/H"),
            "forward exact error locator")
    return G, b, H


def verify_configuration(data):
    basis_rows = verify_oriented_basis(data)
    candidates, h_histogram, pregate_H_one = enumerate_exchange_pairs(data)

    elements = tuple(data["field"])
    direct = {}
    direct_code_checks = 0
    anchor_count = 0
    for c in bounded_polynomials(data["PR"], elements, data["K"]):
        direct_code_checks += 1
        errors = tuple(point for point in data["domain"]
                       if data["U"](point) != c(point))
        if len(errors) > data["radius"]:
            continue
        if c == 0:
            require(errors == data["E0"], "translated anchor error set")
            anchor_count += 1
            continue
        G, b, H = codeword_to_pair(data, c)
        key = pair_key(G, b)
        require(key not in direct, "two direct codewords gave one pair")
        direct[key] = codeword_key(c, data["K"])

    require(anchor_count == 1, "translated anchor multiplicity")
    require(set(direct) == set(candidates), "forward/reverse pair-key mismatch")

    reverse_codewords = {}
    module_exchange_rows = 0
    for key, (G, b, H) in candidates.items():
        c, W, N, alpha, beta = pair_to_codeword(data, G, b, H)
        ckey = codeword_key(c, data["K"])
        require(direct[key] == ckey, "round-trip codeword mismatch")
        require(ckey not in reverse_codewords, "pair map is not injective")
        reverse_codewords[ckey] = key
        module_exchange_rows += 1
    require(len(reverse_codewords) == len(direct), "reverse census size")

    return {
        "configurations": 1,
        "basis_rows": basis_rows,
        "direct_code_checks": direct_code_checks,
        "nonanchor_incidences": len(candidates),
        "module_exchange_rows": module_exchange_rows,
        "h_histogram": h_histogram,
        "pregate_H_one": pregate_H_one,
        "candidates": candidates,
    }


def add_histogram(target, source):
    for key, value in source.items():
        target[key] = target.get(key, 0) + value


def exhaustive_unit_table_toy(field, PR, domain, K, radius):
    """Exhaust every anchor support and every unit-valued V table on E0."""
    nonzero = tuple(value for value in field if value != 0)
    totals = {
        "configurations": 0,
        "basis_rows": 0,
        "direct_code_checks": 0,
        "nonanchor_incidences": 0,
        "module_exchange_rows": 0,
        "h_histogram": {},
        "pregate_H_one": 0,
    }
    for E0 in combinations(domain, radius):
        E0_set = set(E0)
        S0 = tuple(point for point in domain if point not in E0_set)
        A0 = locator(PR, S0)
        for V_table in product(nonzero, repeat=radius):
            # Parameterize exactly as the theorem does: V is an arbitrary
            # unit-valued reduced table on E0 and H0 is its pointwise inverse.
            V_expected = PR.lagrange_polynomial(list(zip(E0, V_table)))
            H0_expected = PR.lagrange_polynomial([
                (point, value^(-1)) for point, value in zip(E0, V_table)
            ])
            U = A0 * H0_expected
            values = tuple(U(point) for point in domain)
            data = build_anchor_data(field, PR, domain, K, radius, values)
            require(data["A0"] == A0, "unit-table A0")
            require(data["H0"] == H0_expected, "unit-table H0")
            require(data["V"] == V_expected, "unit-table inverse V")
            result = verify_configuration(data)
            for key in (
                "configurations", "basis_rows", "direct_code_checks",
                "nonanchor_incidences", "module_exchange_rows", "pregate_H_one",
            ):
                totals[key] += result[key]
            add_histogram(totals["h_histogram"], result["h_histogram"])
    return totals


def boundary_V_one_toy():
    """Exhaust the j0=R, V=1 shift-pair boundary over GF(7)."""
    field = GF(7)
    PR = PolynomialRing(field, "X")
    domain = tuple(field(index) for index in range(7))
    K = 3
    radius = 3
    totals = {
        "supports": 0,
        "basis_rows": 0,
        "direct_code_checks": 0,
        "nonanchor_incidences": 0,
        "module_exchange_rows": 0,
        "h_histogram": {},
        "pregate_H_one": 0,
        "shift_pairs": 0,
    }

    for E0 in combinations(domain, radius):
        E0_set = set(E0)
        S0 = tuple(point for point in domain if point not in E0_set)
        A0 = locator(PR, S0)
        values = tuple(A0(point) for point in domain)
        data = build_anchor_data(field, PR, domain, K, radius, values)
        require(data["j0"] == radius, "boundary j0")
        require(data["H0"] == 1 and data["V"] == 1, "V=1 boundary fixture")
        result = verify_configuration(data)
        totals["supports"] += 1
        for key in (
            "basis_rows", "direct_code_checks", "nonanchor_incidences",
            "module_exchange_rows", "pregate_H_one",
        ):
            totals[key] += result[key]
        add_histogram(totals["h_histogram"], result["h_histogram"])

        # Independently enumerate the shift-pair formulation.  At V=1,
        # deg(G-b)=g, so h<=g; the boundary gate h>=g forces H=G-b and h=g.
        accepted_shift_keys = set()
        for g in range(data["w0"] + 1, min(data["s0"], data["j0"]) + 1):
            for G_support in combinations(data["S0"], g):
                G = locator(PR, G_support)
                for H_support in combinations(data["E0"], g):
                    H = locator(PR, H_support)
                    b = G - H
                    if (b != 0 and b.degree() < g - data["w0"]
                            and b.gcd(G).degree() == 0):
                        accepted_shift_keys.add(
                            (polynomial_key(G), polynomial_key(b), polynomial_key(H))
                        )

        exchange_shift_keys = set()
        for G, b, H in result["candidates"].values():
            g = G.degree()
            h = H.degree()
            require((G - b).degree() == g, "V=1 difference degree")
            require(h <= g, "V=1 gcd degree upper")
            require(h >= g, "boundary gcd degree lower")
            require(h == g, "boundary companion degree")
            require(H == G - b, "boundary H=G-b")
            require(b == G - H, "boundary b=G-H")
            exchange_shift_keys.add(
                (polynomial_key(G), polynomial_key(b), polynomial_key(H))
            )
        require(exchange_shift_keys == accepted_shift_keys,
                "V=1 shift-pair census mismatch")
        totals["shift_pairs"] += len(accepted_shift_keys)

    return totals


def rejected_edges():
    field = GF(7)
    PR = PolynomialRing(field, "X")
    domain = tuple(field(index) for index in range(6))
    rejected_j0_zero = False
    try:
        build_anchor_data(field, PR, domain, 3, 2,
                          tuple(field.zero() for _ in domain))
    except ContractRejected:
        rejected_j0_zero = True
    require(rejected_j0_zero, "j0=0 edge was accepted")
    return 1


def boundary_forcing_toy():
    """Independently replay the fresh-symbol boundary reduction."""
    field = GF(7)
    PR = PolynomialRing(field, "X")
    X = PR.gen()
    domain = tuple(field(index) for index in range(6))
    zero = tuple(field.zero() for _ in domain)
    other = tuple((X * (X - 1))(point) for point in domain)
    received = list(zero)
    received[2] = other[2]
    received[3] = other[3]
    selected = (zero, other)
    radius = 3
    agreement = len(domain) - radius

    initial = tuple(sum(received[i] != row[i] for i in range(len(domain)))
                    for row in selected)
    require(initial == (2, 2), "boundary forcing starts interior")
    agreement_counts = [len(domain) - value for value in initial]
    anchor_index = min(range(len(selected)), key=lambda i: agreement_counts[i])
    t = agreement_counts[anchor_index] - agreement
    coordinates = [i for i in range(len(domain))
                   if received[i] == selected[anchor_index][i]][:t]
    require(len(coordinates) == t, "boundary forcing coordinate supply")
    for coordinate in coordinates:
        used = {row[coordinate] for row in selected}
        fresh = next(value for value in field if value not in used)
        received[coordinate] = fresh

    final = tuple(sum(received[i] != row[i] for i in range(len(domain)))
                  for row in selected)
    require(all(value <= radius for value in final), "boundary forcing retention")
    require(final[anchor_index] == radius, "boundary forcing exact radius")
    return {"initial": initial, "final": final, "changed": t}


# Main deployed-analogue GF(7) control requested by the certificate contract.
F7 = GF(7)
R7 = PolynomialRing(F7, "X")
D7 = tuple(F7(index) for index in range(6))
toy7 = exhaustive_unit_table_toy(F7, R7, D7, K=3, radius=2)
require(toy7["configurations"] == 540, "GF(7) configuration count")
require(toy7["direct_code_checks"] == 185220, "GF(7) direct checks")
require(toy7["nonanchor_incidences"] == 540, "GF(7) pair census")
require(toy7["module_exchange_rows"] == 540, "GF(7) module rows")


# Boundary companion / shift-pair census.
boundary7 = boundary_V_one_toy()
require(boundary7["supports"] == 35, "boundary support count")
require(boundary7["direct_code_checks"] == 12005, "boundary direct checks")
require(boundary7["nonanchor_incidences"] == 140, "boundary incidence count")
require(boundary7["shift_pairs"] == 140, "boundary shift-pair count")
require(boundary7["h_histogram"] == {(2, 2): 126, (3, 3): 14},
        "boundary (g,h) histogram")
require(boundary7["pregate_H_one"] == 7525, "H=1 rejection census")


# Characteristic-two control: the same universal map over GF(8), on six
# distinct points, exhausting every two-point anchor error support and every
# unit-valued table on that support.
F8 = GF(8, name="z")
z = F8.gen()
R8 = PolynomialRing(F8, "X")
D8 = (F8.zero(), F8.one(), z, z^2, z^3, z^4)
require(len(set(D8)) == 6, "GF(8) toy domain")
toy8 = exhaustive_unit_table_toy(F8, R8, D8, K=3, radius=2)
require(toy8["configurations"] == 735, "GF(8) configuration count")
require(toy8["direct_code_checks"] == 376320, "GF(8) direct checks")
require(toy8["nonanchor_incidences"] == 630, "GF(8) pair census")
require(toy8["module_exchange_rows"] == 630, "GF(8) module rows")


edge_rejections = rejected_edges()
boundary_force = boundary_forcing_toy()

print("M31 all-weight anchor-exchange Padé independent Sage replay")
print("GF(7) arbitrary-unit toy: %d configurations, %d direct code checks, %d nonanchor incidences" % (
    toy7["configurations"], toy7["direct_code_checks"], toy7["nonanchor_incidences"]
))
print("GF(7) arbitrary-unit module: %d basis probe rows, %d exchange rows" % (
    toy7["basis_rows"], toy7["module_exchange_rows"]
))
print("GF(7) V=1 boundary: %d supports, %d direct code checks, %d shift-pair incidences" % (
    boundary7["supports"], boundary7["direct_code_checks"], boundary7["shift_pairs"]
))
print("GF(7) V=1 boundary (g,h): %s" % sorted(boundary7["h_histogram"].items()))
print("GF(7) V=1 boundary H=1 pregate rejections: %d" % boundary7["pregate_H_one"])
print("GF(8) characteristic-two toy: %d configurations, %d direct code checks, %d nonanchor incidences" % (
    toy8["configurations"], toy8["direct_code_checks"], toy8["nonanchor_incidences"]
))
print("GF(8) characteristic-two module: %d basis probe rows, %d exchange rows" % (
    toy8["basis_rows"], toy8["module_exchange_rows"]
))
print("Slack-normal identities checked on %d replayed incidences" % (
    toy7["module_exchange_rows"]
    + boundary7["module_exchange_rows"]
    + toy8["module_exchange_rows"]
))
print("Rejected edge fixtures: j0=0 (%d), H=1 (%d)" % (
    edge_rejections, boundary7["pregate_H_one"]
))
print("Fresh-symbol boundary forcing: %s -> %s (%d coordinate)" % (
    boundary_force["initial"], boundary_force["final"], boundary_force["changed"]
))
print("RESULT: PASS")
