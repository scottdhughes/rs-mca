#!/usr/bin/env python3
"""Verify the M31 universal base-field fixed-G RS embedding.

The theorem checked here is a hardness embedding, not a list-size upper
bound.  For a selected ordinary RS(E0,d) list, an exact averaging argument
chooses a constant translation and enough common roots in S0 to make every
translated polynomial coprime to one split locator G.  Multiplication by the
complementary locator then embeds the selected list, together with a boundary
anchor, into the deployed M31 code.

This standard-library verifier checks all deployed integer identities and an
exhaustive direct-table GF(11) fixture.  Every proof-critical gate uses an
explicit exception and therefore remains active under ``python -O``.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from itertools import combinations
from typing import Any, Callable, Iterable, Sequence


P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
FORBIDDEN_LIST_SIZE = B_STAR + 1

M_MIN = W + 1
M_MAX = R
D_MIN = 1
D_MAX = R - W

ALLOWED_CONSTANT_LOWER = P - R
BAD_ROOT_UPPER = (B_STAR * A) // ALLOWED_CONSTANT_LOWER
GOOD_ROOT_LOWER = A - BAD_ROOT_UPPER
GOOD_ROOT_MARGIN_OVER_R = GOOD_ROOT_LOWER - R
DIVISION_REMAINDER = (B_STAR * A) % ALLOWED_CONSTANT_LOWER

# floor(L*a/(p-R)) <= a-R is equivalent to
# L*a < (a-R+1)*(p-R).
UNIFORM_L_MAX = ((A - R + 1) * ALLOWED_CONSTANT_LOWER - 1) // A

SCHEMA_ID = "m31-fixed-g-universal-rs-embedding-summary-v1"
THEOREM_ID = "M31_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_V1"
ARCHITECTURE_ID = THEOREM_ID
STATUS = "PROVED_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_ORDINARY_LIST_BOUND_OPEN"
TERMINAL = "UNPAID_UNIFORM_DETERMINISTIC_PUNCTURED_RS_LIST_BOUND"


class VerificationError(RuntimeError):
    """Raised whenever an exact verifier gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    """Fail closed without relying on assertions."""

    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any, *, pretty: bool = False) -> str:
    """Serialize with the one canonical key order used by this packet."""

    try:
        if pretty:
            return json.dumps(
                value,
                sort_keys=True,
                indent=2,
                ensure_ascii=True,
                allow_nan=False,
            )
        return json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("summary is not canonical JSON") from exc


def intervals(values: Iterable[int]) -> tuple[tuple[int, int], ...]:
    """Compress a sorted integer iterable into closed intervals."""

    data = list(values)
    if not data:
        return ()
    out: list[tuple[int, int]] = []
    lo = previous = data[0]
    for value in data[1:]:
        if value != previous + 1:
            out.append((lo, previous))
            lo = value
        previous = value
    out.append((lo, previous))
    return tuple(out)


def worst_case_bad_root_upper(list_size: int) -> int:
    """Worst-case union bound after averaging over allowed translations."""

    require(list_size >= 0, "list size nonnegative")
    return (list_size * A) // ALLOWED_CONSTANT_LOWER


def uniform_embedding_gate(list_size: int, agreement: int) -> bool:
    """Whether the worst-case averaging guarantee leaves agreement roots."""

    require(M_MIN <= agreement <= M_MAX, "legal M31 fixed-G agreement")
    return A - worst_case_bad_root_upper(list_size) >= agreement


# ---------------------------------------------------------------------------
# Tiny prime-field polynomial and table controls
# ---------------------------------------------------------------------------


def poly_trim(poly: Sequence[int], q: int) -> tuple[int, ...]:
    values = [value % q for value in poly]
    while values and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_add(left: Sequence[int], right: Sequence[int], q: int) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return poly_trim(
        [
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(size)
        ],
        q,
    )


def poly_scale(poly: Sequence[int], scalar: int, q: int) -> tuple[int, ...]:
    return poly_trim([(scalar * value) % q for value in poly], q)


def poly_mul(left: Sequence[int], right: Sequence[int], q: int) -> tuple[int, ...]:
    if not left or not right:
        return ()
    out = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            out[left_index + right_index] += left_value * right_value
    return poly_trim(out, q)


def poly_eval(poly: Sequence[int], x: int, q: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % q
    return value


def poly_degree(poly: Sequence[int], q: int) -> int:
    return len(poly_trim(poly, q)) - 1


def locator(roots: Sequence[int], q: int) -> tuple[int, ...]:
    result: tuple[int, ...] = (1,)
    for root in roots:
        result = poly_mul(result, ((-root) % q, 1), q)
    return result


def interpolate(xs: Sequence[int], ys: Sequence[int], q: int) -> tuple[int, ...]:
    """Lagrange interpolation over the prime field GF(q)."""

    require(len(xs) == len(ys), "interpolation table dimensions")
    require(len(set(xs)) == len(xs), "interpolation nodes distinct")
    result: tuple[int, ...] = ()
    for index, x_value in enumerate(xs):
        others = [other for j, other in enumerate(xs) if j != index]
        basis = locator(others, q)
        denominator = 1
        for other in others:
            denominator = (denominator * (x_value - other)) % q
        coefficient = ys[index] * pow(denominator, -1, q)
        result = poly_add(result, poly_scale(basis, coefficient, q), q)
    require(
        all(poly_eval(result, x, q) == y % q for x, y in zip(xs, ys)),
        "interpolation replay",
    )
    return result


def toy_embedding(
    *,
    q: int,
    e_roots: Sequence[int],
    s_roots: Sequence[int],
    received: Sequence[int],
    polynomials: Sequence[Sequence[int]],
    translation: int,
    g_roots: Sequence[int],
    w: int,
) -> dict[str, Any]:
    """Construct and directly verify one fixed-G boundary-anchor embedding."""

    domain = tuple(e_roots) + tuple(s_roots)
    a = len(s_roots)
    radius = len(e_roots)
    m = len(g_roots)
    d = m - w
    dimension = a - w
    require(d >= 1, "toy RS dimension positive")
    require(set(e_roots).isdisjoint(s_roots), "toy domains disjoint")
    require(set(g_roots).issubset(s_roots), "toy G roots lie in S0")
    require(len(set(g_roots)) == m, "toy G roots distinct")
    require(
        all((received[index] + translation) % q != 0 for index in range(radius)),
        "toy translation avoids -r(E0)",
    )

    a0 = locator(s_roots, q)
    g_poly = locator(g_roots, q)
    complement_roots = tuple(root for root in s_roots if root not in set(g_roots))
    complement = locator(complement_roots, q)
    require(poly_mul(g_poly, complement, q) == a0, "toy A0=G*C factorization")

    translated = [poly_add(poly, (translation,), q) for poly in polynomials]
    require(all(translated), "toy translated b_i nonzero")
    require(
        all(poly_degree(poly, q) < d for poly in translated),
        "toy translated degree gate",
    )
    require(
        all(poly_eval(poly, root, q) != 0 for poly in translated for root in g_roots),
        "toy gcd(b_i,G)=1",
    )

    v_values = []
    for index, x_value in enumerate(e_roots):
        denominator = (received[index] + translation) % q
        v_values.append(poly_eval(g_poly, x_value, q) * pow(denominator, -1, q) % q)
    require(all(v_values), "toy V is a unit table")
    v_poly = interpolate(e_roots, v_values, q)
    h0_values = [pow(value, -1, q) for value in v_values]
    h0_poly = interpolate(e_roots, h0_values, q)
    received_poly = poly_mul(a0, h0_poly, q)
    require(poly_degree(received_poly, q) < len(domain), "toy received interpolant degree")

    received_table = {x: poly_eval(received_poly, x, q) for x in domain}
    require(
        all(received_table[x] == 0 for x in s_roots)
        and all(received_table[x] != 0 for x in e_roots),
        "toy zero anchor is exact boundary",
    )
    require(
        all(
            received_table[x]
            == poly_eval(complement, x, q)
            * (received[index] + translation)
            % q
            for index, x in enumerate(e_roots)
        ),
        "toy received table direct formula",
    )

    codeword_polys = [poly_mul(complement, poly, q) for poly in translated]
    require(
        all(poly_degree(poly, q) < dimension for poly in codeword_polys),
        "toy embedded codeword degree less than K",
    )
    require(
        len(set(codeword_polys)) == len(codeword_polys),
        "toy embedded codewords distinct",
    )
    require(all(codeword_polys), "toy nonanchors distinct from zero anchor")

    records: list[dict[str, Any]] = []
    for original, shifted, codeword in zip(polynomials, translated, codeword_polys):
        h_roots = tuple(
            x
            for index, x in enumerate(e_roots)
            if poly_eval(original, x, q) == received[index] % q
        )
        exact_gcd_roots = tuple(
            x
            for x in e_roots
            if (
                poly_eval(g_poly, x, q)
                - poly_eval(shifted, x, q) * poly_eval(v_poly, x, q)
            )
            % q
            == 0
        )
        require(exact_gcd_roots == h_roots, "toy H is the full gcd locator")
        require(len(h_roots) >= m, "toy ordinary agreement threshold")
        require(
            all(poly_eval(shifted, x, q) != 0 for x in h_roots),
            "toy gcd(b_i,H_i)=1",
        )
        expected_support = tuple(
            x for x in domain if x in complement_roots or x in h_roots
        )
        actual_support = tuple(
            x
            for x in domain
            if poly_eval(codeword, x, q) == received_table[x]
        )
        require(actual_support == expected_support, "toy exact agreement support")
        require(len(actual_support) >= a, "toy codeword inside radius")
        records.append(
            {
                "original_b": list(poly_trim(original, q)),
                "translated_b": list(shifted),
                "codeword": list(codeword),
                "H_roots": list(h_roots),
                "agreement_support": list(actual_support),
                "agreement": len(actual_support),
                "distance": len(domain) - len(actual_support),
            }
        )

    anchor_support = tuple(x for x in domain if received_table[x] == 0)
    require(anchor_support == tuple(s_roots), "toy anchor support exactly S0")
    require(len(anchor_support) == a, "toy anchor lies on radius boundary")
    return {
        "translation": translation,
        "G_roots": list(g_roots),
        "G": list(g_poly),
        "complement_locator": list(complement),
        "V_values_on_E0": v_values,
        "V": list(v_poly),
        "received_table_on_D": [received_table[x] for x in domain],
        "anchor_agreement_support": list(anchor_support),
        "anchor_distance": radius,
        "codewords": records,
        "all_nonanchors_share_one_G": True,
        "list_size_including_anchor": len(records) + 1,
    }


def gf11_control() -> dict[str, Any]:
    """Exhaust every translation and every available 3-root fixed G."""

    q = 11
    e_roots = (0, 1, 2, 3, 4)
    s_roots = (5, 6, 7, 8)
    d = 2
    w = 1
    m = d + w
    received = (0, 0, 0, 3, 4)
    polynomials = ((0,), (0, 1))  # f0=0 and f1=X

    agreement_sets = [
        tuple(
            x
            for index, x in enumerate(e_roots)
            if poly_eval(poly, x, q) == received[index]
        )
        for poly in polynomials
    ]
    require(agreement_sets == [(0, 1, 2), (0, 3, 4)], "GF(11) source lists")

    forbidden = sorted({(-value) % q for value in received})
    allowed = [value for value in range(q) if value not in forbidden]
    require(forbidden == [0, 7, 8], "GF(11) forbidden translations")
    require(allowed == [1, 2, 3, 4, 5, 6, 9, 10], "GF(11) allowed translations")

    translations: list[dict[str, Any]] = []
    construction_count = 0
    selected: dict[str, Any] | None = None
    for translation in allowed:
        bad_roots = tuple(
            x
            for x in s_roots
            if any(
                (poly_eval(poly, x, q) + translation) % q == 0
                for poly in polynomials
            )
        )
        good_roots = tuple(x for x in s_roots if x not in bad_roots)
        require(len(good_roots) >= m, "GF(11) every allowed translation embeds")
        g_choices = list(combinations(good_roots, m))
        translations.append(
            {
                "c": translation,
                "bad_union_roots": list(bad_roots),
                "bad_union_size": len(bad_roots),
                "good_roots": list(good_roots),
                "fixed_G_choices": len(g_choices),
            }
        )
        for roots in g_choices:
            record = toy_embedding(
                q=q,
                e_roots=e_roots,
                s_roots=s_roots,
                received=received,
                polynomials=polynomials,
                translation=translation,
                g_roots=roots,
                w=w,
            )
            construction_count += 1
            if translation == 1 and roots == (5, 6, 7):
                selected = record

    require(construction_count == 20, "GF(11) exhaustive construction count")
    require(selected is not None, "GF(11) selected construction exists")
    require(
        [entry["agreement_support"] for entry in selected["codewords"]]
        == [[0, 1, 2, 8], [0, 3, 4, 8]],
        "GF(11) selected exact supports",
    )
    require(
        selected["received_table_on_D"] == [3, 4, 5, 2, 2, 0, 0, 0, 0],
        "GF(11) selected received table",
    )
    return {
        "field": "GF(11)",
        "q": q,
        "E0": list(e_roots),
        "S0": list(s_roots),
        "d": d,
        "w": w,
        "m": m,
        "K": len(s_roots) - w,
        "r_on_E0": list(received),
        "source_polynomials": ["0", "X"],
        "source_agreement_sets": [list(values) for values in agreement_sets],
        "forbidden_translations": forbidden,
        "allowed_translations": allowed,
        "allowed_translation_count": len(allowed),
        "averaging_bad_union_upper": (
            len(polynomials) * len(s_roots) // len(allowed)
        ),
        "translations": translations,
        "exhaustive_fixed_G_constructions": construction_count,
        "selected_construction": selected,
        "scope": "exact finite-table algebra control, not a deployed list upper",
    }


# ---------------------------------------------------------------------------
# Deployed summary and verification contract
# ---------------------------------------------------------------------------


def deployed_arithmetic() -> dict[str, Any]:
    require(P == 2_147_483_647, "M31 prime integer")
    require(N == 2_097_152 and K == 1_048_576, "M31 length/dimension")
    require(A == 1_116_023 and R == 981_129, "M31 agreement/radius")
    require(W == 67_447, "M31 gap w")
    require(P**4 // 2**100 == B_STAR, "M31 list budget")
    require(ALLOWED_CONSTANT_LOWER == 2_146_502_518, "p-R denominator")
    require(BAD_ROOT_UPPER == 8_722, "deployed bad-root quotient")
    require(DIVISION_REMAINDER == 1_962_853_949, "deployed division remainder")
    require(GOOD_ROOT_LOWER == 1_107_301, "deployed good-root lower")
    require(GOOD_ROOT_MARGIN_OVER_R == 126_172, "deployed root margin")
    require(UNIFORM_L_MAX == 259_450_259, "uniform Lmax")
    require(worst_case_bad_root_upper(UNIFORM_L_MAX) == A - R, "Lmax boundary")
    require(
        worst_case_bad_root_upper(UNIFORM_L_MAX + 1) == A - R + 1,
        "Lmax successor failure",
    )
    return {
        "p": P,
        "n": N,
        "K": K,
        "a": A,
        "R": R,
        "w": W,
        "B_star": B_STAR,
        "forbidden_list_size": FORBIDDEN_LIST_SIZE,
        "legal_d_interval": [D_MIN, D_MAX],
        "legal_m_interval": [M_MIN, M_MAX],
        "allowed_constant_lower_p_minus_R": ALLOWED_CONSTANT_LOWER,
        "deployed_division": {
            "numerator_L_times_a": B_STAR * A,
            "denominator_p_minus_R": ALLOWED_CONSTANT_LOWER,
            "quotient": BAD_ROOT_UPPER,
            "remainder": DIVISION_REMAINDER,
        },
        "good_S0_root_lower": GOOD_ROOT_LOWER,
        "good_root_margin_over_R": GOOD_ROOT_MARGIN_OVER_R,
        "uniform_Lmax": UNIFORM_L_MAX,
        "Lmax_bad_root_upper": worst_case_bad_root_upper(UNIFORM_L_MAX),
        "Lmax_good_root_lower": A - worst_case_bad_root_upper(UNIFORM_L_MAX),
        "Lmax_successor_bad_root_upper": worst_case_bad_root_upper(
            UNIFORM_L_MAX + 1
        ),
        "Lmax_successor_good_root_lower": A
        - worst_case_bad_root_upper(UNIFORM_L_MAX + 1),
    }


def johnson_middle() -> dict[str, Any]:
    nonpositive = intervals(
        m
        for m in range(M_MIN, M_MAX + 1)
        if m * m - R * ((m - W) - 1) <= 0
    )
    require(nonpositive == ((72_859, 908_270),), "Johnson middle m interval")
    d_intervals = tuple((lo - W, hi - W) for lo, hi in nonpositive)
    require(d_intervals == ((5_412, 840_823),), "Johnson middle d interval")
    require(72_858**2 - R * ((72_858 - W) - 1) > 0, "Johnson lower wing")
    require(72_859**2 - R * ((72_859 - W) - 1) <= 0, "Johnson lower edge")
    require(908_270**2 - R * ((908_270 - W) - 1) <= 0, "Johnson upper edge")
    require(908_271**2 - R * ((908_271 - W) - 1) > 0, "Johnson upper wing")
    return {
        "denominator": "m^2-R*(d-1), with d=m-w",
        "nonpositive_m_interval": [list(pair) for pair in nonpositive],
        "nonpositive_d_interval": [list(pair) for pair in d_intervals],
        "route_cut": (
            "the fixed-G subproblem contains arbitrary ordinary RS lists "
            "throughout the broad post-Johnson middle"
        ),
    }


def build_summary() -> dict[str, Any]:
    parameters = deployed_arithmetic()
    toy = gf11_control()
    return {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture": ARCHITECTURE_ID,
        "status": STATUS,
        "terminal": TERMINAL,
        "row": {
            "name": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "coefficient_field": "F_p embedded in F_(p^4)",
            "evaluation_domain": "every partition D=S0 disjoint_union E0 of the deployed D",
            "B_star": B_STAR,
        },
        "parameters": parameters,
        "averaging_lemma": {
            "allowed_constants": "C=F_p\\{-r(x):x in E0}",
            "allowed_constant_count": "p-|r(E0)|>=p-R",
            "bad_object": "union of S0 points where some b_i(x)+c=0",
            "incidence_upper": "sum_(c in C)|bad_union(c)|<=L*a",
            "uses_union_not_pair_multiplicity": True,
            "bad_union_upper": "floor(L*a/(p-|r(E0)|))",
            "worst_case_bad_union_upper": "floor(L*a/(p-R))",
            "general_gate": "a-floor(L*a/(p-|r(E0)|))>=m=d+w",
            "deployed_worst_case_gate": "a-floor(L*a/(p-R))>=m",
            "deployed_B_star_bad_union_upper": BAD_ROOT_UPPER,
            "deployed_B_star_good_root_lower": GOOD_ROOT_LOWER,
            "deployed_gate_holds_for_every_legal_m": uniform_embedding_gate(
                B_STAR, M_MAX
            ),
        },
        "embedding": {
            "source": (
                "L distinct b_i in RS_Fp(E0,d), each agreeing with arbitrary "
                "r:E0->F_p on at least m=d+w points"
            ),
            "translation": "b_i'=b_i+c and r'=r+c, with r' nowhere zero",
            "root_choice": "choose m common good roots in S0",
            "fixed_locator": "G=L_T divides A0 and deg(G)=m",
            "complement": "C=A0/G",
            "common_unit": "V(x)=G(x)/(r(x)+c) on E0",
            "full_gcd": "H_i=gcd(L0,G-b_i'V)=agreement locator of b_i with r",
            "codeword": "c_i=C*b_i'",
            "received_word": "y=0 on S0 and y=C*(r+c) on E0",
            "exact_agreement_support": "(S0\\Z(G)) disjoint_union Agr_E0(b_i,r)",
            "maximum_codeword_degree": K - 1,
            "translated_polynomials_distinct": True,
            "all_nonanchors_share_one_G": True,
            "zero_anchor_is_boundary": True,
            "base_field_construction": True,
            "target_field_embedding_valid": True,
        },
        "threshold_consequence": {
            "ordinary_companions": B_STAR,
            "boundary_anchor": 1,
            "M31_list_size": FORBIDDEN_LIST_SIZE,
            "M31_forbidden_threshold": FORBIDDEN_LIST_SIZE,
            "fixed_G_threshold_equivalence": (
                "ordinary L-list exists iff a base-field boundary-anchor "
                "fixed-G subfamily with L nonanchors exists, under the gate"
            ),
            "M_ord_required_upper_if_M31_safe": B_STAR - 1,
            "M_ord_statement": (
                "for every E0 subset of deployed D, every 1<=d<=R-w, and "
                "every r:E0->F_p, at most B_star-1 polynomials agree on d+w points"
            ),
            "global_varying_G_converse": False,
            "ordinary_RS_upper_proved": False,
        },
        "uniform_range": {
            "exact_gate": "a-floor(L*a/(p-R))>=m",
            "works_for_all_legal_m_through_L": UNIFORM_L_MAX,
            "at_Lmax_good_roots": R,
            "successor": UNIFORM_L_MAX + 1,
            "successor_good_roots": R - 1,
            "successor_fails_uniform_m_equals_R_gate": True,
        },
        "johnson_middle": johnson_middle(),
        "small_prime_control": toy,
        "ledger": {
            "movement": 0,
            "official_endpoint_movement": 0,
            "U_paid": 3_730,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "U_new": None,
            "row_closed": False,
        },
        "nonclaims": [
            "no deterministic ordinary RS list upper is proved",
            "no global varying-G M31 converse is proved",
            "boundary means the zero anchor; companions may be interior",
            "no v4 atom, owner, ledger, endpoint, or score movement",
            "the GF(11) exhaustion is an algebra control, not deployed evidence",
        ],
    }


def verify_summary(summary: dict[str, Any]) -> None:
    require(summary.get("schema") == SCHEMA_ID, "schema ID")
    require(summary.get("theorem_id") == THEOREM_ID, "theorem ID")
    require(summary.get("architecture") == ARCHITECTURE_ID, "architecture ID")
    require(summary.get("status") == STATUS, "status")
    require(summary.get("terminal") == TERMINAL, "terminal")

    row = summary["row"]
    require(row["coefficient_field"] == "F_p embedded in F_(p^4)", "base-field scope")
    require(row["B_star"] == B_STAR, "row budget")
    require(
        row["evaluation_domain"]
        == "every partition D=S0 disjoint_union E0 of the deployed D",
        "deployed-domain quantifier",
    )

    params = summary["parameters"]
    require(params["p"] == P and params["n"] == N, "deployed p,n")
    require(params["K"] == K and params["a"] == A, "deployed K,a")
    require(params["R"] == R and params["w"] == W, "deployed R,w")
    require(params["B_star"] == B_STAR, "deployed B_star")
    require(params["forbidden_list_size"] == B_STAR + 1, "forbidden off-by-one")
    require(params["legal_d_interval"] == [1, 913_682], "legal d interval")
    require(params["legal_m_interval"] == [67_448, 981_129], "legal m interval")
    require(
        params["allowed_constant_lower_p_minus_R"] == 2_146_502_518,
        "allowed-constant denominator p-R",
    )
    division = params["deployed_division"]
    require(division["numerator_L_times_a"] == 18_723_757_815_945, "division numerator")
    require(division["denominator_p_minus_R"] == 2_146_502_518, "division denominator")
    require(division["quotient"] == 8_722, "division quotient")
    require(division["remainder"] == 1_962_853_949, "division remainder")
    require(params["good_S0_root_lower"] == 1_107_301, "good-root lower")
    require(params["good_root_margin_over_R"] == 126_172, "good-root margin")
    require(params["uniform_Lmax"] == 259_450_259, "uniform Lmax")
    require(params["Lmax_bad_root_upper"] == 134_894, "Lmax bad roots")
    require(params["Lmax_good_root_lower"] == R, "Lmax exact root boundary")
    require(params["Lmax_successor_bad_root_upper"] == 134_895, "Lmax successor bad roots")
    require(params["Lmax_successor_good_root_lower"] == R - 1, "Lmax successor failure")

    averaging = summary["averaging_lemma"]
    require(
        averaging["allowed_constants"] == "C=F_p\\{-r(x):x in E0}",
        "allowed constants exclude -r(E0)",
    )
    require(averaging["allowed_constant_count"] == "p-|r(E0)|>=p-R", "allowed count")
    require(
        averaging["bad_object"]
        == "union of S0 points where some b_i(x)+c=0",
        "bad object is root union",
    )
    require(
        averaging["incidence_upper"] == "sum_(c in C)|bad_union(c)|<=L*a",
        "averaging incidence upper",
    )
    require(averaging["uses_union_not_pair_multiplicity"] is True, "union semantics")
    require(
        averaging["general_gate"] == "a-floor(L*a/(p-|r(E0)|))>=m=d+w",
        "general embedding gate",
    )
    require(averaging["deployed_B_star_bad_union_upper"] == 8_722, "B_star bad union")
    require(averaging["deployed_B_star_good_root_lower"] == 1_107_301, "B_star roots")
    require(
        averaging["deployed_gate_holds_for_every_legal_m"] is True,
        "deployed general gate",
    )

    embedding = summary["embedding"]
    require(embedding["root_choice"] == "choose m common good roots in S0", "root choice")
    require(embedding["fixed_locator"] == "G=L_T divides A0 and deg(G)=m", "fixed G")
    require(embedding["common_unit"] == "V(x)=G(x)/(r(x)+c) on E0", "common unit")
    require(
        embedding["full_gcd"]
        == "H_i=gcd(L0,G-b_i'V)=agreement locator of b_i with r",
        "full gcd locator",
    )
    require(embedding["maximum_codeword_degree"] == K - 1, "codeword degree")
    require(embedding["translated_polynomials_distinct"] is True, "distinctness")
    require(embedding["all_nonanchors_share_one_G"] is True, "one fixed G")
    require(embedding["zero_anchor_is_boundary"] is True, "boundary anchor")
    require(embedding["base_field_construction"] is True, "base-field construction")
    require(embedding["target_field_embedding_valid"] is True, "target-field lift")

    threshold = summary["threshold_consequence"]
    require(threshold["ordinary_companions"] == B_STAR, "ordinary companion count")
    require(threshold["boundary_anchor"] == 1, "one boundary anchor")
    require(threshold["M31_list_size"] == B_STAR + 1, "anchor/list off-by-one")
    require(threshold["M31_forbidden_threshold"] == B_STAR + 1, "forbidden threshold")
    require(threshold["M_ord_required_upper_if_M31_safe"] == B_STAR - 1, "M_ord consequence")
    require(threshold["global_varying_G_converse"] is False, "no global converse")
    require(threshold["ordinary_RS_upper_proved"] is False, "ordinary upper remains open")

    uniform = summary["uniform_range"]
    require(uniform["works_for_all_legal_m_through_L"] == 259_450_259, "uniform range")
    require(uniform["at_Lmax_good_roots"] == R, "Lmax exact gate")
    require(uniform["successor"] == 259_450_260, "Lmax successor")
    require(uniform["successor_good_roots"] == R - 1, "successor root loss")
    require(uniform["successor_fails_uniform_m_equals_R_gate"] is True, "successor fails")

    johnson = summary["johnson_middle"]
    require(johnson["nonpositive_m_interval"] == [[72_859, 908_270]], "Johnson m interval")
    require(johnson["nonpositive_d_interval"] == [[5_412, 840_823]], "Johnson d interval")

    toy = summary["small_prime_control"]
    require(toy["field"] == "GF(11)" and toy["q"] == 11, "GF(11) field")
    require(toy["E0"] == [0, 1, 2, 3, 4], "GF(11) E0")
    require(toy["S0"] == [5, 6, 7, 8], "GF(11) S0")
    require((toy["d"], toy["w"], toy["m"]) == (2, 1, 3), "GF(11) d,w,m")
    require(toy["r_on_E0"] == [0, 0, 0, 3, 4], "GF(11) received table")
    require(toy["allowed_translations"] == [1, 2, 3, 4, 5, 6, 9, 10], "GF(11) allowed c")
    require(toy["averaging_bad_union_upper"] == 1, "GF(11) averaging upper")
    require(toy["exhaustive_fixed_G_constructions"] == 20, "GF(11) exhaustive count")
    selected = toy["selected_construction"]
    require(selected["translation"] == 1, "GF(11) selected translation")
    require(selected["G_roots"] == [5, 6, 7], "GF(11) selected roots")
    require(selected["all_nonanchors_share_one_G"] is True, "GF(11) fixed G")
    require(selected["anchor_distance"] == 5, "GF(11) boundary anchor distance")
    require(selected["list_size_including_anchor"] == 3, "GF(11) list off-by-one")
    require(
        [entry["agreement_support"] for entry in selected["codewords"]]
        == [[0, 1, 2, 8], [0, 3, 4, 8]],
        "GF(11) exact supports",
    )
    require(
        all(entry["distance"] == 5 for entry in selected["codewords"]),
        "GF(11) boundary companions",
    )

    ledger = summary["ledger"]
    require(ledger["movement"] == 0, "zero ledger movement")
    require(ledger["official_endpoint_movement"] == 0, "zero endpoint movement")
    require(ledger["U_paid"] == 3_730, "inherited U_paid")
    require(
        all(ledger[key] is None for key in ("U_Q", "U_list_int", "U_ext", "U_new")),
        "null atoms remain null",
    )
    require(ledger["row_closed"] is False, "row remains open")
    require(len(summary["nonclaims"]) >= 5, "explicit nonclaims")
    canonical_json(summary)


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_suite() -> list[Mutation]:
    return [
        ("schema", lambda s: s.__setitem__("schema", "wrong")),
        ("theorem", lambda s: s.__setitem__("theorem_id", "wrong")),
        ("architecture", lambda s: s.__setitem__("architecture", "wrong")),
        ("status", lambda s: s.__setitem__("status", "PROVED_ROW_CLOSED")),
        ("terminal", lambda s: s.__setitem__("terminal", "PAID")),
        ("denominator-p-minus-R", lambda s: s["parameters"].__setitem__(
            "allowed_constant_lower_p_minus_R", ALLOWED_CONSTANT_LOWER + 1)),
        ("division-quotient", lambda s: s["parameters"]["deployed_division"].__setitem__(
            "quotient", BAD_ROOT_UPPER + 1)),
        ("incidence-vs-union", lambda s: s["averaging_lemma"].__setitem__(
            "uses_union_not_pair_multiplicity", False)),
        ("bad-object", lambda s: s["averaging_lemma"].__setitem__(
            "bad_object", "number of polynomial-point incidences with multiplicity")),
        ("allowed-constants", lambda s: s["averaging_lemma"].__setitem__(
            "allowed_constants", "C=F_p")),
        ("general-gate", lambda s: s["averaging_lemma"].__setitem__(
            "general_gate", "a-floor(L*a/p)>=m")),
        ("good-roots", lambda s: s["parameters"].__setitem__(
            "good_S0_root_lower", GOOD_ROOT_LOWER - 1)),
        ("root-choice", lambda s: s["embedding"].__setitem__(
            "root_choice", "choose roots separately for each b_i")),
        ("degree", lambda s: s["embedding"].__setitem__(
            "maximum_codeword_degree", K)),
        ("distinctness", lambda s: s["embedding"].__setitem__(
            "translated_polynomials_distinct", False)),
        ("base-field-scope", lambda s: s["row"].__setitem__(
            "coefficient_field", "arbitrary target-field list")),
        ("deployed-domain-scope", lambda s: s["row"].__setitem__(
            "evaluation_domain", "arbitrary E0 outside deployed D")),
        ("fixed-G", lambda s: s["embedding"].__setitem__(
            "all_nonanchors_share_one_G", False)),
        ("anchor-boundary", lambda s: s["embedding"].__setitem__(
            "zero_anchor_is_boundary", False)),
        ("anchor-list-off-by-one", lambda s: s["threshold_consequence"].__setitem__(
            "M31_list_size", B_STAR)),
        ("ordinary-threshold", lambda s: s["threshold_consequence"].__setitem__(
            "ordinary_companions", B_STAR - 1)),
        ("M-ord-consequence", lambda s: s["threshold_consequence"].__setitem__(
            "M_ord_required_upper_if_M31_safe", B_STAR)),
        ("false-global-converse", lambda s: s["threshold_consequence"].__setitem__(
            "global_varying_G_converse", True)),
        ("Lmax", lambda s: s["uniform_range"].__setitem__(
            "works_for_all_legal_m_through_L", UNIFORM_L_MAX + 1)),
        ("Lmax-successor", lambda s: s["uniform_range"].__setitem__(
            "successor_fails_uniform_m_equals_R_gate", False)),
        ("Johnson-m", lambda s: s["johnson_middle"].__setitem__(
            "nonpositive_m_interval", [[72_860, 908_270]])),
        ("Johnson-d", lambda s: s["johnson_middle"].__setitem__(
            "nonpositive_d_interval", [[5_413, 840_823]])),
        ("toy-allowed-translations", lambda s: s["small_prime_control"].__setitem__(
            "allowed_translations", [0, 1, 2, 3, 4, 5, 6, 9, 10])),
        ("toy-roots", lambda s: s["small_prime_control"]["selected_construction"].__setitem__(
            "G_roots", [5, 6, 8])),
        ("toy-degree", lambda s: s["small_prime_control"].__setitem__("d", 3)),
        ("toy-distinctness", lambda s: s["small_prime_control"]["selected_construction"].__setitem__(
            "list_size_including_anchor", 2)),
        ("toy-support", lambda s: s["small_prime_control"]["selected_construction"]["codewords"][0].__setitem__(
            "agreement_support", [0, 1, 2, 7])),
        ("toy-exhaustion", lambda s: s["small_prime_control"].__setitem__(
            "exhaustive_fixed_G_constructions", 19)),
        ("ledger", lambda s: s["ledger"].__setitem__("movement", 1)),
        ("atom", lambda s: s["ledger"].__setitem__("U_Q", 0)),
        ("false-upper", lambda s: s["threshold_consequence"].__setitem__(
            "ordinary_RS_upper_proved", True)),
        ("false-closure", lambda s: s["ledger"].__setitem__("row_closed", True)),
    ]


def run_mutation_selftest(summary: dict[str, Any]) -> dict[str, Any]:
    passed: list[str] = []
    for name, mutate in mutation_suite():
        candidate = copy.deepcopy(summary)
        mutate(candidate)
        try:
            verify_summary(candidate)
        except VerificationError:
            passed.append(name)
        else:
            raise VerificationError(f"mutation escaped detection: {name}")
    require(len(passed) == len(mutation_suite()), "all mutations detected")
    return {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "mutation_selftest": "PASS",
        "mutations_detected": len(passed),
        "mutation_names": passed,
        "ordinary_RS_upper_proved": False,
        "row_closed": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    parser.add_argument(
        "--mutation-selftest",
        "--tamper-selftest",
        dest="mutation_selftest",
        action="store_true",
        help="prove that proof-critical summary mutations fail closed",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = build_summary()
    verify_summary(summary)
    output = run_mutation_selftest(summary) if args.mutation_selftest else summary
    print(canonical_json(output, pretty=args.pretty))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
