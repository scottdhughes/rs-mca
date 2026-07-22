#!/usr/bin/env sage
"""Independent Sage replay of the M31 universal fixed-G embedding.

This is a tiny-field algebra control over GF(11).  It exhausts the allowed
constant translations and every resulting degree-three locator choice for a
frozen two-word ordinary RS list, then reconstructs the fixed-G M31 boundary
list and checks the exact gcd, support, degree, distinctness, anchor, and lift
identities.  It is not evidence for the deployed ordinary-list upper and
moves no ledger atom.
"""

import argparse
import json
import sys
from itertools import combinations

from sage.all import GF, PolynomialRing


SCHEMA = "m31-fixed-g-universal-rs-embedding-sage-v1"
THEOREM_ID = "M31_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_V1"
ARCHITECTURE_ID = THEOREM_ID
STATUS = "PROVED_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_ORDINARY_LIST_BOUND_OPEN"
TERMINAL = "UNPAID_UNIFORM_DETERMINISTIC_PUNCTURED_RS_LIST_BOUND"


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


def normalized_gcd(left, right):
    value = left.gcd(right)
    return value.monic() if value != 0 else value


def quotient_exact(numerator, denominator, label):
    quotient, remainder = numerator.quo_rem(denominator)
    require(remainder == 0, label)
    return quotient


def inverse_mod(PR, value, modulus):
    gcd_value, coefficient, _ = value.xgcd(modulus)
    require(gcd_value == 1, "unit has inverse modulo L0")
    inverse = coefficient % modulus
    require((value * inverse) % modulus == 1, "inverse identity modulo L0")
    return PR(inverse)


def field_int(value):
    return int(value)


def roots_as_ints(roots):
    return [field_int(root) for root in roots]


def frozen_fixture():
    F = GF(11)
    PR = PolynomialRing(F, "X")
    X = PR.gen()

    E = [F(value) for value in (0, 1, 2, 3, 4)]
    S = [F(value) for value in (5, 6, 7, 8)]
    d = 2
    w = 1
    m = d + w
    toy_K = len(S) - w
    functions = [PR.zero(), X]
    received_values = [F(value) for value in (0, 0, 0, 3, 4)]
    received = dict(zip(E, received_values))

    require(len(E) == 5 and len(S) == 4, "frozen domain sizes")
    require(set(E).isdisjoint(set(S)), "frozen domains disjoint")
    require((d, w, m, toy_K) == (2, 1, 3, 3), "frozen degree parameters")
    require(len(functions) == 2 and functions[0] != functions[1],
            "frozen ordinary words distinct")

    forbidden = {-received[x] for x in E}
    allowed = [kappa for kappa in F if kappa not in forbidden]
    require(roots_as_ints(allowed) == [1, 2, 3, 4, 5, 6, 9, 10],
            "allowed translation table")
    require(len(allowed) >= F.order() - len(E),
            "conservative allowed-constant lower bound")

    translation_rows = []
    for kappa in allowed:
        bad_union = [
            point for point in S
            if any(function(point) + kappa == 0 for function in functions)
        ]
        incidences = [
            (index, point)
            for index, function in enumerate(functions)
            for point in S
            if function(point) + kappa == 0
        ]
        good = [point for point in S if point not in bad_union]
        require(len(bad_union) <= len(incidences),
                "bad union bounded by incidences")
        require(len(good) >= m, "every allowed translation has m good roots")
        translation_rows.append({
            "kappa": field_int(kappa),
            "bad_union": roots_as_ints(bad_union),
            "bad_union_size": len(bad_union),
            "incidences": [
                {"function_index": index, "root": field_int(point)}
                for index, point in incidences
            ],
            "incidence_count": len(incidences),
            "good_roots": roots_as_ints(good),
            "degree_m_locator_choices": len(list(combinations(good, m))),
        })

    total_bad_union = sum(row["bad_union_size"] for row in translation_rows)
    total_incidences = sum(row["incidence_count"] for row in translation_rows)
    require(total_bad_union <= total_incidences <= len(functions) * len(S),
            "summed avoidance double count")
    conservative_bad_cap = (len(functions) * len(S)) // (F.order() - len(E))
    require(conservative_bad_cap == 1, "toy conservative floor")
    require(min(row["bad_union_size"] for row in translation_rows)
            <= conservative_bad_cap, "averaging witness exists")

    witness_kappa = F(3)
    witness_row = next(row for row in translation_rows
                       if row["kappa"] == field_int(witness_kappa))
    require(witness_row["bad_union"] == [8], "frozen witness bad root")
    require(witness_row["good_roots"] == [5, 6, 7],
            "frozen witness common good roots")

    return {
        "F": F,
        "PR": PR,
        "X": X,
        "E": E,
        "S": S,
        "d": d,
        "w": w,
        "m": m,
        "toy_K": toy_K,
        "functions": functions,
        "received": received,
        "allowed": allowed,
        "translation_rows": translation_rows,
        "witness_kappa": witness_kappa,
        "avoidance_summary": {
            "field": "GF(11)",
            "E": roots_as_ints(E),
            "S": roots_as_ints(S),
            "d": d,
            "w": w,
            "m": m,
            "ordinary_functions": ["0", "X"],
            "received_values_on_E": [field_int(received[x]) for x in E],
            "forbidden_constants": sorted(field_int(value) for value in forbidden),
            "allowed_constant_count": len(allowed),
            "conservative_allowed_count_q_minus_E": F.order() - len(E),
            "conservative_bad_union_cap": conservative_bad_cap,
            "translation_rows": translation_rows,
            "summed_bad_union": total_bad_union,
            "summed_incidences": total_incidences,
            "witness_kappa": field_int(witness_kappa),
        },
    }


def construct_embedding(fixture, kappa, selected_roots, label):
    PR = fixture["PR"]
    X = fixture["X"]
    E = fixture["E"]
    S = fixture["S"]
    functions = fixture["functions"]
    received = fixture["received"]
    d = fixture["d"]
    w = fixture["w"]
    m = fixture["m"]
    toy_K = fixture["toy_K"]

    require(len(selected_roots) == m, "%s selected-root size" % label)
    require(all(
        function(point) + kappa != 0
        for function in functions for point in selected_roots
    ), "%s simultaneous nonvanishing on G" % label)

    A0 = locator(PR, S)
    L0 = locator(PR, E)
    G = locator(PR, selected_roots)
    C = quotient_exact(A0, G, "%s G divides A0" % label)
    shifted = [function + kappa for function in functions]
    shifted_received = {point: received[point] + kappa for point in E}
    require(all(value != 0 for value in shifted_received.values()),
            "%s translated received table nowhere zero" % label)

    V_values = [G(point) / shifted_received[point] for point in E]
    V = interpolate(PR, E, V_values)
    require(V.degree() < len(E), "%s interpolated V degree" % label)
    require(normalized_gcd(V, L0) == 1, "%s V unit modulo L0" % label)
    recovered_shifted_received = [G(point) / V(point) for point in E]
    require(recovered_shifted_received
            == [shifted_received[point] for point in E],
            "%s fixed-G table recovers translated ordinary center" % label)
    H_inverse = inverse_mod(PR, V, L0)
    U = A0 * H_inverse

    direct_received = {
        point: PR.zero()(point) if point in S else C(point) * shifted_received[point]
        for point in S + E
    }
    require(all(U(point) == direct_received[point] for point in S + E),
            "%s polynomial and table received words agree" % label)

    H_values = []
    codewords = []
    support_rows = []
    for index, (function, b) in enumerate(zip(functions, shifted)):
        require(b != 0, "%s shifted message nonzero" % label)
        require(b.degree() < d, "%s shifted message degree" % label)
        require(normalized_gcd(b, G) == 1, "%s gcd(b,G)=1" % label)

        ordinary_roots = [point for point in E
                          if function(point) == received[point]]
        H_expected = locator(PR, ordinary_roots)
        H_actual = normalized_gcd(L0, G - b * V)
        require(H_actual == H_expected, "%s exact full gcd" % label)
        require(H_actual.degree() >= m, "%s ordinary agreement threshold" % label)
        require(normalized_gcd(b, H_actual) == 1,
                "%s gcd(b,H)=1" % label)
        require(all(
            (G(point) - b(point) * V(point) == 0)
            == (function(point) == received[point])
            for point in E
        ), "%s pointwise gcd/agreement equivalence" % label)

        codeword = C * b
        require(codeword.degree() < toy_K, "%s ambient codeword degree" % label)
        actual_support = [point for point in S + E
                          if codeword(point) == U(point)]
        expected_support = [point for point in S if G(point) != 0]
        expected_support += ordinary_roots
        require(set(actual_support) == set(expected_support),
                "%s exact ambient agreement support" % label)
        require(len(actual_support) >= len(S),
                "%s ambient agreement threshold" % label)

        H_values.append(H_actual)
        codewords.append(codeword)
        support_rows.append({
            "index": index,
            "function": "0" if index == 0 else "X",
            "shifted_message": str(b),
            "ordinary_agreement_roots": roots_as_ints(ordinary_roots),
            "H": str(H_actual),
            "H_degree": int(H_actual.degree()),
            "codeword": str(codeword),
            "codeword_degree": int(codeword.degree()),
            "ambient_agreement_support": roots_as_ints(actual_support),
        })

    require(len({str(codeword) for codeword in codewords}) == len(codewords),
            "%s nonanchor codewords distinct" % label)
    require(all(codeword != 0 for codeword in codewords),
            "%s nonanchor codewords nonzero" % label)
    anchor_support = [point for point in S + E if U(point) == 0]
    require(set(anchor_support) == set(S), "%s zero anchor exact boundary" % label)

    W = G * shifted[1] - G * shifted[0]
    J = normalized_gcd(H_values[0], H_values[1])
    Delta = quotient_exact(H_values[0] * H_values[1], J**2,
                           "%s symmetric-difference locator" % label)
    require(W % J == 0, "%s Wronskian intersection vanishing" % label)
    require(normalized_gcd(Delta, W) == 1,
            "%s Wronskian symmetric-difference nonvanishing" % label)

    lift_coefficient = X + 2
    V_lift = V + lift_coefficient * L0
    require(V_lift % L0 == V % L0, "%s lift residue invariance" % label)
    require(normalized_gcd(V_lift, L0) == 1, "%s lifted V remains unit" % label)
    for b, H in zip(shifted, H_values):
        require(normalized_gcd(L0, G - b * V_lift) == H,
                "%s lifted exact full gcd" % label)
    H_inverse_lift = inverse_mod(PR, V_lift, L0)
    U_lift = A0 * H_inverse_lift
    require(all(U_lift(point) == U(point) for point in S + E),
            "%s lift leaves received table unchanged" % label)

    return {
        "kappa": field_int(kappa),
        "selected_G_roots": roots_as_ints(selected_roots),
        "A0": str(A0),
        "L0": str(L0),
        "G": str(G),
        "G_degree": int(G.degree()),
        "cofactor_A0_over_G": str(C),
        "V": str(V),
        "V_values_on_E": [field_int(V(point)) for point in E],
        "recovered_translated_received_on_E": [
            field_int(value) for value in recovered_shifted_received
        ],
        "inverse_V_mod_L0": str(H_inverse),
        "received_polynomial_U": str(U),
        "ambient_received_table_y": [
            {"point": field_int(point), "value": field_int(direct_received[point])}
            for point in S + E
        ],
        "zero_anchor_support": roots_as_ints(anchor_support),
        "nonanchors": support_rows,
        "pairwise_W": str(W),
        "pairwise_intersection_locator_J": str(J),
        "pairwise_symmetric_difference_locator_Delta": str(Delta),
        "lift_invariance": True,
    }


def exhaustive_translation_locator_control(fixture):
    constructions = 0
    codeword_checks = 0
    per_translation = []
    witness = None

    for kappa in fixture["allowed"]:
        good = [
            point for point in fixture["S"]
            if all(function(point) + kappa != 0
                   for function in fixture["functions"])
        ]
        locator_choices = list(combinations(good, fixture["m"]))
        require(locator_choices, "allowed translation has a locator choice")
        for choice_index, selected_roots in enumerate(locator_choices):
            label = "kappa-%d-choice-%d" % (field_int(kappa), choice_index)
            result = construct_embedding(fixture, kappa, selected_roots, label)
            constructions += 1
            codeword_checks += len(result["nonanchors"])
            if kappa == fixture["witness_kappa"]:
                witness = result
        per_translation.append({
            "kappa": field_int(kappa),
            "good_root_count": len(good),
            "locator_choices": len(locator_choices),
        })

    require(constructions == 20, "frozen exhaustive construction count")
    require(codeword_checks == 40, "frozen exhaustive codeword count")
    require(witness is not None, "frozen witness construction retained")
    require(witness["selected_G_roots"] == [5, 6, 7],
            "frozen witness locator roots")

    return {
        "field": "GF(11)",
        "allowed_translations": len(fixture["allowed"]),
        "per_translation": per_translation,
        "exhaustive_translation_locator_constructions": constructions,
        "exact_codeword_support_checks": codeword_checks,
        "ordinary_table_to_fixed_G_and_back": True,
        "witness": witness,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    fixture = frozen_fixture()
    exhaustive = exhaustive_translation_locator_control(fixture)
    scope = {
        "ledger_movement": 0,
        "row_closed": False,
        "ordinary_list_upper_16777214_proved": False,
        "global_split_rational_incidence_upper_proved": False,
        "arbitrary_ambient_Fp4_received_word_equivalence_proved": False,
        "deployed_counterexample_constructed": False,
        "toy_controls_are_deployed_evidence": False,
        "stable_paper_modified": False,
    }
    require(scope["ledger_movement"] == 0, "zero ledger movement")
    require(scope["row_closed"] is False, "row remains open")
    require(scope["ordinary_list_upper_16777214_proved"] is False,
            "ordinary-list upper remains open")
    require(scope["toy_controls_are_deployed_evidence"] is False,
            "toy controls remain nondeployed")

    summary = {
        "schema": SCHEMA,
        "theorem_id": THEOREM_ID,
        "architecture_id": ARCHITECTURE_ID,
        "status": STATUS,
        "terminal": TERMINAL,
        "avoidance_control": fixture["avoidance_summary"],
        "exhaustive_embedding_control": exhaustive,
        "deployed_scope": scope,
        "checks": CHECKS,
    }
    print(json.dumps(
        summary,
        sort_keys=True,
        indent=2 if args.pretty else None,
        separators=None if args.pretty else (",", ":"),
        allow_nan=False,
        default=int,
    ))


try:
    main()
except CheckFailure as error:
    print("verification failed: %s" % error, file=sys.stderr)
    raise SystemExit(1)
