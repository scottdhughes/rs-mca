#!/usr/bin/env sage
"""Independent Sage controls for the M31 pairwise-CRT split-flat packet.

The exhaustive computations below are deliberately tiny-field algebra
controls.  They verify the quotient/remainder atlas, the different boundary
and interior full-gcd gates, lift invariance, the pairwise CRT equivalence,
the load-bearing individual unit gate, and sharpness of ``|I| < q-1``.
They do not prove the deployed global incidence bound or move a ledger atom.
"""

import argparse
import json
import sys
from itertools import combinations, product


SCHEMA = "m31-common-v-pairwise-crt-equivalence-sage-v1"
THEOREM_ID = "M31_COMMON_V_SPLIT_FLAT_PAIRWISE_CRT_EQUIVALENCE_V1"
STATUS = "PROVED_PAIRWISE_CRT_EQUIVALENCE_SPLIT_FLAT_ATLAS_GLOBAL_INCIDENCE_OPEN"
TERMINAL = "UNPAID_PAIRWISE_SPLIT_RATIONAL_FUNCTION_DIVISOR_INCIDENCE"


class CheckFailure(RuntimeError):
    pass


CHECKS = 0


def require(condition, label):
    global CHECKS
    CHECKS += 1
    if not bool(condition):
        raise CheckFailure(label)


def locator(PR, roots):
    X = PR.gen()
    out = PR.one()
    for root in roots:
        out *= X - root
    return out


def interpolate(PR, points, values):
    F = PR.base_ring()
    X = PR.gen()
    out = PR.zero()
    for i, point in enumerate(points):
        basis = PR.one()
        denominator = F.one()
        for j, other in enumerate(points):
            if i == j:
                continue
            basis *= X - other
            denominator *= point - other
        out += values[i] * basis / denominator
    return out


def polynomials_below(PR, degree):
    F = PR.base_ring()
    X = PR.gen()
    return [
        sum((coefficients[j] * X**j for j in range(degree)), PR.zero())
        for coefficients in product(list(F), repeat=degree)
    ]


def monic_polynomials(PR, degree):
    X = PR.gen()
    return [X**degree + lower for lower in polynomials_below(PR, degree)]


def normalized_gcd(left, right):
    value = left.gcd(right)
    return value.monic() if value != 0 else value


def quotient_exact(numerator, denominator, label):
    quotient, remainder = numerator.quo_rem(denominator)
    require(remainder == 0, label)
    return quotient


def unit_representatives(PR, roots):
    F = PR.base_ring()
    nonzero = [value for value in F if value != 0]
    return [
        interpolate(PR, roots, values)
        for values in product(nonzero, repeat=len(roots))
    ]


def coefficient_matrix(PR, H, V, d):
    F = PR.base_ring()
    X = PR.gen()
    h = H.degree()
    columns = []
    for j in range(d):
        _Q, T = (X**j * V).quo_rem(H)
        columns.append([T[row] for row in range(h)])
    return matrix(F, h, d, lambda row, col: columns[col][row])


def atlas_control():
    """Exhaust GF(5) charts with deg(H)<=2 inside a three-point L0."""

    F = GF(5)
    PR = PolynomialRing(F, "X")
    X = PR.gen()
    e_roots = [F(2), F(3), F(4)]
    L0 = locator(PR, e_roots)
    representatives = unit_representatives(PR, e_roots)
    C_lift = X + 1

    chart_cases = 0
    boundary_parameter_tests = 0
    interior_parameter_tests = 0
    monic_equivalence_tests = 0
    full_gcd_tests = 0
    resultant_tests = 0
    lift_tests = 0
    interior_nonempty = 0
    observed_interior_ranks = set()

    for h in (1, 2):
        for roots in combinations(e_roots, h):
            H = locator(PR, roots)
            J = quotient_exact(L0, H, "H divides L0")
            require(normalized_gcd(H, J) == 1, "squarefree H/J split")
            for V in representatives:
                require(normalized_gcd(V, L0) == 1, "V is a unit modulo L0")
                for m in range(1, h + 1):
                    for d in range(1, m + 1):
                        chart_cases += 1
                        T_matrix = coefficient_matrix(PR, H, V, d)
                        require(T_matrix.rank() == d, "remainder map full column rank")
                        b_values = polynomials_below(PR, d)
                        monic_values = monic_polynomials(PR, m)

                        if h == m:
                            require(h - d == m - d, "boundary codimension identity")
                            for b in b_values:
                                Q, T = (b * V).quo_rem(H)
                                candidate = H + T
                                require(candidate.degree() == m and candidate.is_monic(),
                                        "boundary candidate monic degree m")
                                for G in monic_values:
                                    actual = (G - b * V) % H == 0
                                    expected = G == candidate
                                    require(actual == expected,
                                            "boundary quotient/remainder equivalence")
                                    monic_equivalence_tests += 1

                                actual_full = normalized_gcd(L0, candidate - b * V) == H
                                gcd_gate = normalized_gcd(J, 1 - Q) == 1
                                resultant_gate = J.resultant(1 - Q) != 0
                                require(actual_full == gcd_gate,
                                        "boundary full-gcd uses 1-Q")
                                require(gcd_gate == resultant_gate,
                                        "boundary resultant equivalence")
                                full_gcd_tests += 1
                                resultant_tests += 1

                                V_lift = V + C_lift * L0
                                Q_lift, T_lift = (b * V_lift).quo_rem(H)
                                require(T_lift == T, "lift leaves T unchanged")
                                require(Q_lift == Q + b * C_lift * J,
                                        "lift changes Q by b*C*J")
                                require(
                                    (normalized_gcd(J, 1 - Q_lift) == 1) == gcd_gate,
                                    "boundary full-gcd gate is lift invariant",
                                )
                                lift_tests += 1
                                boundary_parameter_tests += 1
                        else:
                            s = h - m
                            C_matrix = T_matrix.matrix_from_rows(range(m, h))
                            require(C_matrix.nrows() == s and C_matrix.ncols() == d,
                                    "interior coefficient block shape")
                            target = vector(F, [1] + [0] * (s - 1))
                            solution_count = 0
                            for b in b_values:
                                b_vector = vector(F, [b[j] for j in range(d)])
                                Q, T = (b * V).quo_rem(H)
                                coefficient_gate = C_matrix * b_vector == target
                                monic_remainder = T.degree() == m and T[m] == 1
                                require(coefficient_gate == monic_remainder,
                                        "interior top-row affine equation")
                                if coefficient_gate:
                                    solution_count += 1
                                for G in monic_values:
                                    actual = (G - b * V) % H == 0
                                    expected = coefficient_gate and G == T
                                    require(actual == expected,
                                            "interior quotient/remainder equivalence")
                                    monic_equivalence_tests += 1

                                if coefficient_gate:
                                    actual_full = normalized_gcd(L0, T - b * V) == H
                                    gcd_gate = normalized_gcd(J, Q) == 1
                                    resultant_gate = J.resultant(Q) != 0
                                    require(actual_full == gcd_gate,
                                            "interior full-gcd uses Q")
                                    require(gcd_gate == resultant_gate,
                                            "interior resultant equivalence")
                                    full_gcd_tests += 1
                                    resultant_tests += 1

                                V_lift = V + C_lift * L0
                                Q_lift, T_lift = (b * V_lift).quo_rem(H)
                                require(T_lift == T, "interior lift leaves T")
                                require(Q_lift == Q + b * C_lift * J,
                                        "interior lift changes Q by b*C*J")
                                require(
                                    (normalized_gcd(J, Q_lift) == 1)
                                    == (normalized_gcd(J, Q) == 1),
                                    "interior full-gcd gate is lift invariant",
                                )
                                lift_tests += 1
                                interior_parameter_tests += 1

                            rho = C_matrix.rank()
                            if solution_count:
                                require(1 <= rho <= min(s, d),
                                        "nonempty interior rank range")
                                require(solution_count == F.order() ** (d - rho),
                                        "interior affine solution count")
                                observed_interior_ranks.add(int(rho))
                                interior_nonempty += 1

    require(boundary_parameter_tests > 0 and interior_parameter_tests > 0,
            "both atlas chart types exercised")
    require(full_gcd_tests > 0 and resultant_tests == full_gcd_tests,
            "full-gcd/resultant controls exercised")
    require(lift_tests == boundary_parameter_tests + interior_parameter_tests,
            "every parameter tested for lift invariance")
    require(interior_nonempty > 0, "nonempty interior charts exercised")
    return {
        "field": "GF(5)",
        "L0_degree": 3,
        "unit_representatives": len(representatives),
        "chart_cases": chart_cases,
        "boundary_parameter_tests": boundary_parameter_tests,
        "interior_parameter_tests": interior_parameter_tests,
        "monic_equivalence_tests": monic_equivalence_tests,
        "full_gcd_tests": full_gcd_tests,
        "resultant_tests": resultant_tests,
        "lift_invariance_tests": lift_tests,
        "nonempty_interior_charts": interior_nonempty,
        "observed_nonempty_interior_ranks": sorted(observed_interior_ranks),
    }


def pair_gate(PR, left, right):
    G_i, b_i, H_i = left
    G_j, b_j, H_j = right
    W_ij = G_i * b_j - G_j * b_i
    require(W_ij != 0, "distinct reduced pairs have nonzero Wronskian")
    J_ij = normalized_gcd(H_i, H_j)
    Delta_ij = quotient_exact(H_i * H_j, J_ij**2, "symmetric locator exact")
    return W_ij % J_ij == 0 and normalized_gcd(Delta_ij, W_ij) == 1


def reconstruct_common_unit(PR, L0, e_roots, family):
    F = PR.base_ring()
    values = []
    for x in e_roots:
        covering = [triple for triple in family if triple[2](x) == 0]
        if covering:
            prescribed = {G(x) / b(x) for G, b, _H in covering}
            if len(prescribed) != 1 or F.zero() in prescribed:
                return None
            value = next(iter(prescribed))
            for G, b, H in family:
                if H(x) != 0 and b(x) != 0 and G(x) / b(x) == value:
                    return None
            values.append(value)
        else:
            forbidden = {
                G(x) / b(x) for G, b, _H in family if b(x) != 0
            }
            available = [v for v in F if v != 0 and v not in forbidden]
            if not available:
                return None
            values.append(available[0])
    V = interpolate(PR, e_roots, values)
    require(normalized_gcd(V, L0) == 1, "reconstructed V is a unit")
    return V


def pairwise_crt_control():
    F = GF(5)
    PR = PolynomialRing(F, "X")
    X = PR.gen()
    s_roots = [F(0), F(1)]
    e_roots = [F(2), F(3)]
    L0 = locator(PR, e_roots)
    unit_V = unit_representatives(PR, e_roots)
    charts = [
        (X - g, PR(b), X - h)
        for g in s_roots
        for h in e_roots
        for b in F if b != 0
    ]

    expected = {2: (112, 48), 3: (448, 32)}
    output = {}
    reconstruction_tests = 0
    for size in (2, 3):
        total = 0
        compatible_count = 0
        realized_count = 0
        for family in combinations(charts, size):
            reduced = {(str(G), str(b)) for G, b, _H in family}
            if len(reduced) != size:
                continue
            total += 1
            individual = all(normalized_gcd(b, H) == 1 for _G, b, H in family)
            compatible = individual and all(
                pair_gate(PR, left, right)
                for left, right in combinations(family, 2)
            )
            realized = any(
                all(normalized_gcd(L0, G - b * V) == H for G, b, H in family)
                for V in unit_V
            )
            require(compatible == realized,
                    "exhaustive pairwise iff common full-gcd unit")
            if compatible:
                V = reconstruct_common_unit(PR, L0, e_roots, family)
                require(V is not None, "covered/uncovered reconstruction succeeds")
                require(all(normalized_gcd(L0, G - b * V) == H
                            for G, b, H in family),
                        "reconstructed V has every exact full gcd")
                compatible_count += 1
                reconstruction_tests += 1
            if realized:
                realized_count += 1
        require((total, compatible_count) == expected[size],
                "frozen GF(5) family table")
        require(realized_count == compatible_count,
                "realized count equals pairwise count")
        output[str(size)] = {
            "pairwise_distinct_reduced_pair_families": total,
            "pairwise_compatible": compatible_count,
            "exactly_realized": realized_count,
        }

    return {
        "field": "GF(5)",
        "charts": len(charts),
        "unit_tables": len(unit_V),
        "family_counts": output,
        "reconstruction_tests": reconstruction_tests,
    }


def hostile_singleton_control():
    F = GF(5)
    PR = PolynomialRing(F, "X")
    X = PR.gen()
    L0 = X - 2
    G = X
    b = X - 2
    H = L0
    require(normalized_gcd(G, b) == 1, "hostile singleton reduced")
    require(normalized_gcd(b, H) != 1, "hostile singleton violates individual gate")
    units = unit_representatives(PR, [F(2)])
    require(all(normalized_gcd(L0, G - b * V) != H for V in units),
            "pairwise-vacuous singleton is not realizable")
    return {
        "field": "GF(5)",
        "family_size": 1,
        "pairwise_gates": "vacuous",
        "gcd_b_H": str(normalized_gcd(b, H)),
        "common_unit_exists": False,
        "conclusion": "individual gcd(b,H)=1 is load-bearing",
    }


def field_size_sharpness_control():
    F = GF(5)
    PR = PolynomialRing(F, "X")
    X = PR.gen()
    L0 = X
    H = PR.one()
    family = [(X - a, PR.one(), H) for a in F if a != 0]
    require(len(family) == F.order() - 1, "sharp family has q-1 members")
    require(len({str(G) for G, _b, _H in family}) == len(family),
            "sharp reduced pairs distinct")
    require(all(pair_gate(PR, left, right)
                for left, right in combinations(family, 2)),
            "sharp fixture passes every pairwise gate")
    units = unit_representatives(PR, [F.zero()])
    require(not any(all(normalized_gcd(L0, G - b * V) == H
                        for G, b, H in family) for V in units),
            "q-1 ratios exhaust all unit values")
    for predecessor in combinations(family, F.order() - 2):
        require(any(all(normalized_gcd(L0, G - b * V) == H
                        for G, b, H in predecessor) for V in units),
                "every q-2 predecessor has an available unit")
    return {
        "field": "GF(5)",
        "family_size": len(family),
        "pairwise_compatible": True,
        "common_unit_exists": False,
        "every_q_minus_2_subfamily_realizable": True,
        "strict_gate": "|I|<q-1",
    }


def boundary_reconstruction_control():
    F = GF(5)
    PR = PolynomialRing(F, "X")
    X = PR.gen()
    s_roots = [F(0), F(1)]
    e_roots = [F(2), F(3)]
    A0 = locator(PR, s_roots)
    L0 = locator(PR, e_roots)
    charts = [
        (X - g, PR(b), X - h)
        for g in s_roots for h in e_roots for b in F if b != 0
    ]
    family = None
    for candidate in combinations(charts, 3):
        if len({(str(G), str(b)) for G, b, _H in candidate}) != 3:
            continue
        if all(pair_gate(PR, left, right)
               for left, right in combinations(candidate, 2)):
            family = candidate
            break
    require(family is not None, "compatible boundary reconstruction fixture")
    V = reconstruct_common_unit(PR, L0, e_roots, family)
    require(V is not None, "boundary fixture common unit")
    gcd_value, H0, _cofactor = V.xgcd(L0)
    require(gcd_value == 1, "boundary fixture V invertible")
    H0 %= L0
    require((V * H0) % L0 == 1, "boundary inverse modulo L0")
    U = A0 * H0
    codewords = []
    for G, b, H in family:
        c = quotient_exact(A0, G, "G divides A0 in boundary fixture") * b
        require(c.degree() < len(s_roots), "toy codeword degree bound")
        actual_support = {
            point for point in s_roots + e_roots if U(point) == c(point)
        }
        expected_support = {
            point for point in s_roots if G(point) != 0
        }.union({point for point in e_roots if H(point) == 0})
        require(actual_support == expected_support,
                "exact boundary agreement support")
        codewords.append(c)
    require(len({str(c) for c in codewords}) == len(codewords),
            "reduced pairs give distinct codewords")
    anchor_support = {point for point in s_roots + e_roots if U(point) == 0}
    require(anchor_support == set(s_roots), "zero boundary anchor exact support")
    return {
        "field": "GF(5)",
        "family_size": len(family),
        "distinct_codewords": len(codewords),
        "exact_supports": True,
        "zero_anchor_support_size": len(anchor_support),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    summary = {
        "schema": SCHEMA,
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "terminal": TERMINAL,
        "atlas_control": atlas_control(),
        "pairwise_crt_control": pairwise_crt_control(),
        "hostile_singleton_control": hostile_singleton_control(),
        "field_size_sharpness": field_size_sharpness_control(),
        "boundary_reconstruction": boundary_reconstruction_control(),
        "deployed_scope": {
            "ledger_movement": 0,
            "row_closed": False,
            "global_incidence_upper_15775932_proved": False,
            "toy_controls_are_deployed_evidence": False,
        },
    }
    require(summary["deployed_scope"]["ledger_movement"] == 0,
            "zero ledger movement")
    require(summary["deployed_scope"]["row_closed"] is False,
            "row remains open")
    output = json.dumps(
        summary,
        sort_keys=True,
        indent=2 if args.pretty else None,
        separators=None if args.pretty else (",", ":"),
        allow_nan=False,
        default=int,
    )
    print(output)


try:
    main()
except CheckFailure as error:
    print("verification failed: %s" % error, file=sys.stderr)
    raise SystemExit(1)
