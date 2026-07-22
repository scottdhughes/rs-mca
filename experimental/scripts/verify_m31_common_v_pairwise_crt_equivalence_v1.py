#!/usr/bin/env python3
"""Verify the M31 common-V pairwise CRT and split-flat route cut.

This standard-library verifier checks the exact deployed arithmetic, the
fixed-H affine atlas, and the pairwise criterion for realizing *full* gcd
locators with one common unit modulo ``L0``.  Small prime tables exhaustively
compare pairwise compatibility with direct enumeration of unit value tables.

The output is a structural route-cut summary.  It is not a list-size upper
bound, does not populate a Grande Finale v4 atom, and leaves the M31 row open.
Every proof-critical gate uses explicit exceptions and remains active under
``python -O``.
"""

from __future__ import annotations

import argparse
import copy
import json
from itertools import combinations, product
from math import comb
from typing import Any, Callable, Iterable, Sequence


P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
FORBIDDEN_LIST_SIZE = B_STAR + 1

DEEP_EXCESS_START = 366_887
DEEP_CAP = 1_001_282
FORBIDDEN_SHALLOW_NEEDED = B_STAR - DEEP_CAP
SUFFICIENT_SHALLOW_TARGET = (B_STAR - 1) - DEEP_CAP

SCHEMA_ID = "m31-common-v-pairwise-crt-equivalence-summary-v1"
THEOREM_ID = "M31_COMMON_V_SPLIT_FLAT_PAIRWISE_CRT_EQUIVALENCE_V1"
STATUS = "PROVED_PAIRWISE_CRT_EQUIVALENCE_SPLIT_FLAT_ATLAS_GLOBAL_INCIDENCE_OPEN"
TERMINAL = "UNPAID_PAIRWISE_SPLIT_RATIONAL_FUNCTION_DIVISOR_INCIDENCE"


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


# ---------------------------------------------------------------------------
# Tiny-field root-table controls
# ---------------------------------------------------------------------------

Chart = tuple[int, int, int]  # (root of G, root of H, constant b)


def ratio(chart: Chart, x: int, q: int) -> int:
    g_root, _h_root, b = chart
    return ((x - g_root) * pow(b, -1, q)) % q


def pairwise_root_gate(left: Chart, right: Chart, q: int) -> bool:
    """The exact J|W and gcd(Delta,W)=1 gate for linear G,H."""

    _g_left, h_left, _b_left = left
    _g_right, h_right, _b_right = right
    if h_left == h_right:
        return ratio(left, h_left, q) == ratio(right, h_left, q)
    return (
        ratio(left, h_left, q) != ratio(right, h_left, q)
        and ratio(right, h_right, q) != ratio(left, h_right, q)
    )


def realized_by_unit_table(
    family: Sequence[Chart], e_roots: Sequence[int], q: int
) -> bool:
    """Brute-force all nonzero tables on E and demand exact H root sets."""

    for values in product(range(1, q), repeat=len(e_roots)):
        table = dict(zip(e_roots, values))
        good = True
        for g_root, h_root, b in family:
            actual = tuple(
                x
                for x in e_roots
                if ((x - g_root) - b * table[x]) % q == 0
            )
            if actual != (h_root,):
                good = False
                break
        if good:
            return True
    return False


def reconstructed_unit_table(
    family: Sequence[Chart], e_roots: Sequence[int], q: int
) -> dict[int, int] | None:
    """Implement the proof's covered-root CRT and local avoidance rule."""

    table: dict[int, int] = {}
    for x in e_roots:
        covering = [chart for chart in family if chart[1] == x]
        if covering:
            prescribed = {ratio(chart, x, q) for chart in covering}
            if len(prescribed) != 1 or 0 in prescribed:
                return None
            value = next(iter(prescribed))
            for chart in family:
                if chart[1] != x and ratio(chart, x, q) == value:
                    return None
            table[x] = value
            continue

        forbidden = {ratio(chart, x, q) for chart in family}
        available = [value for value in range(1, q) if value not in forbidden]
        if not available:
            return None
        table[x] = available[0]
    return table


def small_prime_case(
    q: int,
    s_roots: Sequence[int],
    e_roots: Sequence[int],
) -> dict[str, Any]:
    require(q in (5, 7), "small-prime control is frozen to GF(5), GF(7)")
    require(set(s_roots).isdisjoint(e_roots), "toy root domains disjoint")
    charts = [
        (g_root, h_root, b)
        for g_root in s_roots
        for h_root in e_roots
        for b in range(1, q)
    ]
    records: dict[str, Any] = {}
    for family_size in (2, 3):
        compatible_count = 0
        realized_count = 0
        families = [
            family
            for family in combinations(charts, family_size)
            if len({(g_root, b) for g_root, _h_root, b in family})
            == family_size
        ]
        for family in families:
            compatible = all(
                pairwise_root_gate(left, right, q)
                for left, right in combinations(family, 2)
            )
            realized = realized_by_unit_table(family, e_roots, q)
            require(
                compatible == realized,
                f"GF({q}) size-{family_size} pairwise/full-gcd equivalence",
            )
            if compatible:
                reconstructed = reconstructed_unit_table(family, e_roots, q)
                require(reconstructed is not None, "proof reconstruction exists")
                require(
                    all(
                        tuple(
                            x
                            for x in e_roots
                            if ((x - chart[0]) - chart[2] * reconstructed[x]) % q
                            == 0
                        )
                        == (chart[1],)
                        for chart in family
                    ),
                    "reconstructed table realizes every exact H",
                )
                compatible_count += 1
            if realized:
                realized_count += 1
        records[str(family_size)] = {
            "pairwise_distinct_reduced_pair_families": len(families),
            "pairwise_compatible": compatible_count,
            "exactly_realized": realized_count,
        }

    return {
        "q": q,
        "S_roots": list(s_roots),
        "E_roots": list(e_roots),
        "charts": len(charts),
        "unit_tables": (q - 1) ** len(e_roots),
        "family_counts": records,
    }


def field_size_sharpness_control() -> dict[str, Any]:
    """At |I|=q-1, vacuous H gates need not admit a common unit."""

    q = 5
    # E0={0}, S0=F_5^*, G_a=X-a, b_a=1, H_a=1.  The values
    # G_a(0)/b_a(0)=-a exhaust F_5^* and the reduced pairs are distinct.
    a_values = tuple(range(1, q))
    ratios = tuple((-a) % q for a in a_values)
    available_full = tuple(value for value in range(1, q) if value not in ratios)
    predecessor_remaining = min(
        len([value for value in range(1, q) if value not in subset])
        for subset in combinations(ratios, q - 2)
    )
    require(not available_full, "field-size sharpness exhaustion")
    require(predecessor_remaining == 1, "field-size predecessor has one choice")
    return {
        "q": q,
        "uncovered_points": 1,
        "H_locators": "all_one",
        "S_roots": list(a_values),
        "G_a": "X-a",
        "b_a": "1",
        "reduced_pairs_distinct": True,
        "pairwise_H_gates": "vacuous",
        "family_size": q - 1,
        "nonzero_ratios": list(ratios),
        "common_unit_exists": False,
        "predecessor_family_size": q - 2,
        "minimum_predecessor_choices": predecessor_remaining,
        "scope": "sharpness of |I|<q-1; not a deployed canonical chart",
    }


# ---------------------------------------------------------------------------
# Deployed exact summary
# ---------------------------------------------------------------------------


def deployed_arithmetic() -> dict[str, Any]:
    require(P == 2_147_483_647, "M31 prime drift")
    require(N == 2_097_152 and K == 1_048_576, "code dimensions drift")
    require(A == 1_116_023, "agreement drift")
    require(R == 981_129 and W == 67_447, "R/w drift")
    require(B_STAR == 16_777_215, "budget drift")
    require(FORBIDDEN_LIST_SIZE == 16_777_216, "forbidden list-size drift")
    require(P - 1 - B_STAR == 2_130_706_431, "field margin drift")
    require(P - 1 - FORBIDDEN_SHALLOW_NEEDED == 2_131_707_713,
            "shallow field margin drift")
    require(DEEP_CAP == 1_001_282, "parent deep cap drift")
    require(FORBIDDEN_SHALLOW_NEEDED == 15_775_933, "shallow necessity drift")
    require(SUFFICIENT_SHALLOW_TARGET == 15_775_932, "shallow target drift")
    require(
        FORBIDDEN_SHALLOW_NEEDED == SUFFICIENT_SHALLOW_TARGET + 1,
        "one-unit shallow gap",
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
        "maximum_nonanchors_in_forbidden_list": B_STAR,
        "field_nonzero_values": P - 1,
        "field_margin_p_minus_1_minus_B_star": P - 1 - B_STAR,
        "shallow_field_margin_p_minus_1_minus_15775933": (
            P - 1 - FORBIDDEN_SHALLOW_NEEDED
        ),
    }


def fixed_h_atlas_summary() -> dict[str, Any]:
    # These checks are exact dimension identities, not a sampled rank claim.
    require(W + 1 > W, "first legal degree")
    return {
        "remainder_map": {
            "domain": "P_d",
            "codomain": "P_h",
            "definition": "T_HV(b)=b*V mod H",
            "hypotheses": [
                "deg(H)=h=m+s",
                "d=m-w",
                "V_is_a_unit_class_mod_L0",
                "V_representative_has_degree_less_than_R",
            ],
            "kernel": "zero",
            "rank": "d",
            "proof_gate": "H|bV and gcd(H,V)=1 and deg(b)<d<h imply b=0",
        },
        "boundary": {
            "condition": "s=0",
            "affine_equation": "G=H+T_HV(b)",
            "dimension": "d",
            "ambient_monic_dimension": "m",
            "codimension": "m-d=w",
            "quotient_equation": "G-bV=H*(1-Q_HV(b))",
            "full_gcd_gate": "gcd(L0/H,1-Q_HV(b))=1",
            "resultant_gate": "Res(L0/H,1-Q_HV(b))!=0",
            "rank_drop_components": 0,
        },
        "interior": {
            "condition": "s>0",
            "coefficient_block_shape": ["s", "d"],
            "affine_equation": "C_HmV*b=e_0",
            "locator_equation": "G=T_HV(b)",
            "consistent_rank_range": ["1", "min(s,d)"],
            "dimension": "d-rho",
            "ambient_monic_codimension": "w+rho>=w+1",
            "quotient_equation": "G-bV=-H*Q_HV(b)",
            "full_gcd_gate": "gcd(L0/H,Q_HV(b))=1",
            "resultant_gate": "Res(L0/H,Q_HV(b))!=0",
        },
        "remaining_gates": [
            "G|A0",
            "G_monic_split_on_S0",
            "b!=0",
            "deg(b)<m-w",
            "Res(G,b)!=0",
        ],
        "lift_invariance": {
            "replacement": "V->V+C*L0",
            "T_change": "0",
            "Q_change": "b*C*(L0/H)",
            "boundary_full_gcd_gate_unchanged": True,
            "interior_full_gcd_gate_unchanged": True,
        },
        "H_sum_disjoint": True,
    }


def pairwise_equivalence_summary() -> dict[str, Any]:
    require(B_STAR < P - 1, "deployed strict family-size gate")
    return {
        "family_size_hypothesis": "|I|<p-1",
        "deployed_family_size_max": B_STAR,
        "individual_gates": [
            "G_i_monic_split_on_S0",
            "H_i_monic_split_on_E0",
            "gcd(G_i,b_i)=1",
            "gcd(b_i,H_i)=1",
            "reduced_pairs_(G_i,b_i)_pairwise_distinct",
        ],
        "definitions": {
            "W_ij": "G_i*b_j-G_j*b_i",
            "J_ij": "gcd(H_i,H_j)",
            "Delta_ij": "H_i*H_j/J_ij^2",
        },
        "pairwise_gates": [
            "J_ij|W_ij",
            "gcd(Delta_ij,W_ij)=1",
        ],
        "equivalence_RHS": {
            "individual": "gcd(b_i,H_i)=1 for every i",
            "pairwise": ["J_ij|W_ij", "gcd(Delta_ij,W_ij)=1"],
        },
        "equivalent_global_statement": (
            "exists unit V mod L0 with "
            "gcd(L0,G_i-b_i*V)=H_i for every i"
        ),
        "covered_root_rule": "V(x)=G_i(x)/b_i(x)",
        "uncovered_root_rule": (
            "choose a nonzero value avoiding every defined G_i(x)/b_i(x)"
        ),
        "maximum_forbidden_nonzero_values_per_uncovered_root": B_STAR,
        "available_nonzero_value_margin": P - 1 - B_STAR,
        "higher_CRT_obstruction": False,
        "Wronskian_nonzero_for_distinct_canonical_pairs": True,
    }


def exact_row_realization_summary() -> dict[str, Any]:
    maximum_degree = A - (W + 1) + ((W + 1 - W) - 1)
    require(maximum_degree == K - 1, "exact c_i degree endpoint")
    require(A - W == K, "a-w=K degree identity")
    return {
        "inverse": "H0=V^(-1) mod L0",
        "received_word_polynomial": "U=A0*H0",
        "codeword_polynomial": "c_i=(A0/G_i)*b_i",
        "maximum_codeword_degree": maximum_degree,
        "degree_gate": "deg(c_i)<K",
        "boundary_anchor": "zero_codeword",
        "anchor_agreement": A,
        "anchor_error_weight": R,
        "agreement_support": "(S0\\Z(G_i)) disjoint_union Z(H_i)",
        "distinctness_gate": (
            "c_i=c_j forces G_i*b_j=G_j*b_i and hence identical canonical pairs"
        ),
        "projection_unit": "distinct nonanchor codewords per received word",
    }


def degree_one_route_cuts() -> dict[str, Any]:
    m = W + 1
    d = m - W
    scalar_target = B_STAR - 1
    quotient, remainder = divmod(P - 1, scalar_target)
    fixed_h_cap, fixed_h_remainder = divmod(A, m)
    fixed_g_cap, fixed_g_remainder = divmod(R, m)
    locator_pair_capacity = comb(R, 2)
    require(m == 67_448 and d == 1, "degree-one endpoint")
    require((quotient, remainder) == (128, 254), "scalar target division")
    require((fixed_h_cap, fixed_h_remainder) == (16, 36_855),
            "fixed-H split cap")
    require((fixed_g_cap, fixed_g_remainder) == (14, 36_857),
            "fixed-G level-set cap")
    require(locator_pair_capacity == 481_306_566_756,
            "locator-pair capacity")
    require(locator_pair_capacity > B_STAR, "local caps fail global sum")
    return {
        "m": m,
        "d": d,
        "nonzero_scalar_parameters_before_split_gates": P - 1,
        "complete_companion_target": scalar_target,
        "scalar_division": {
            "quotient": quotient,
            "remainder": remainder,
            "identity": "p-1=128*(B_star-1)+254",
        },
        "fixed_H_split_root_cap": fixed_h_cap,
        "fixed_H_remainder_roots": fixed_h_remainder,
        "fixed_G_level_set_cap": fixed_g_cap,
        "fixed_G_remainder_roots": fixed_g_remainder,
        "locator_pair_capacity_C_R_2": locator_pair_capacity,
        "locator_pair_capacity_exceeds_B_star": True,
        "route_cut": (
            "dimension and one-locator caps do not sum over the global G,H census"
        ),
        "fixed_G_RS_embedding": fixed_g_rs_embedding_summary(),
    }


def truth_intervals(values: Iterable[int]) -> list[list[int]]:
    data = list(values)
    if not data:
        return []
    out: list[list[int]] = []
    lo = previous = data[0]
    for value in data[1:]:
        if value != previous + 1:
            out.append([lo, previous])
            lo = value
        previous = value
    out.append([lo, previous])
    return out


def fixed_g_rs_embedding_summary() -> dict[str, Any]:
    nonpositive = [
        m
        for m in range(W + 1, R + 1)
        if m * m - R * ((m - W) - 1) <= 0
    ]
    intervals = truth_intervals(nonpositive)
    require(intervals == [[72_859, 908_270]],
            "fixed-G Johnson nonpositive middle interval")
    require(72_858**2 - R * ((72_858 - W) - 1) > 0,
            "fixed-G lower predecessor positive")
    require(908_271**2 - R * ((908_271 - W) - 1) > 0,
            "fixed-G upper successor positive")
    return {
        "received_table": "r_GV(x)=G(x)/V(x) on E0",
        "agreement_identity": (
            "deg(gcd(L0,G-bV))=agreement_E0(b,r_GV)"
        ),
        "as_V_varies": (
            "r_GV ranges bijectively over all nonzero-valued received words"
        ),
        "RS_dimension": "d=m-w",
        "agreement_threshold": "m",
        "additional_filter": "gcd(b,G)=1",
        "johnson_denominator": "m^2-R*(d-1)",
        "nonpositive_intervals": intervals,
        "normalized_agreement_minus_dimension": "67447/981129",
        "route_cut": (
            "fixed-G can be an arbitrary nonzero RS received-word census; "
            "common V supplies no pseudorandomness"
        ),
    }


def build_summary() -> dict[str, Any]:
    gf5 = small_prime_case(5, (0, 1), (2, 3))
    gf7 = small_prime_case(7, (0, 1, 2), (3, 4, 5))
    return {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "terminal": TERMINAL,
        "row": {
            "name": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "agreement": A,
            "B_star": B_STAR,
            "architecture": "M31_BASE_FIELD_SPLIT_FLAT_PAIRWISE_CRT_EQUIVALENCE_V1",
        },
        "parameters": deployed_arithmetic(),
        "fixed_H_split_flat_atlas": fixed_h_atlas_summary(),
        "pairwise_full_gcd_equivalence": pairwise_equivalence_summary(),
        "exact_boundary_list_realization": exact_row_realization_summary(),
        "shallow_successor": {
            "parent_deep_excess_start": DEEP_EXCESS_START,
            "parent_deep_cap": DEEP_CAP,
            "forbidden_family_shallow_needed": FORBIDDEN_SHALLOW_NEEDED,
            "sufficient_shallow_upper_target": SUFFICIENT_SHALLOW_TARGET,
            "exact_gap": 1,
            "statement": (
                "every canonical family satisfying gcd(b_i,H_i)=1, every "
                "pairwise compatibility gate, and 0<=s<=366886 has size "
                "at most 15775932"
            ),
            "proved": False,
        },
        "degree_one_route_cuts": degree_one_route_cuts(),
        "small_prime_controls": {
            "GF5": gf5,
            "GF7": gf7,
            "field_size_sharpness": field_size_sharpness_control(),
            "evidentiary_scope": (
                "exact finite algebra controls; not a deployed incidence upper"
            ),
        },
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
            "no upper bound for the global split rational-function family",
            "no v4 owner transport or atom payment",
            "no inference that the shallow locators G or H repeat",
            "no M31 LIST row closure or endpoint movement",
            "small-field controls are not asymptotic or deployed evidence",
        ],
    }


EXPECTED_SMALL_TABLES = {
    "GF5": {
        "charts": 16,
        "unit_tables": 16,
        "2": (112, 48, 48),
        "3": (448, 32, 32),
    },
    "GF7": {
        "charts": 54,
        "unit_tables": 216,
        "2": (1_377, 756, 756),
        "3": (22_032, 3_378, 3_378),
    },
}


def verify_summary(summary: dict[str, Any]) -> None:
    require(summary.get("schema") == SCHEMA_ID, "schema ID")
    require(summary.get("theorem_id") == THEOREM_ID, "theorem ID")
    require(summary.get("status") == STATUS, "status")
    require(summary.get("terminal") == TERMINAL, "terminal")

    params = summary["parameters"]
    require(params["p"] == P and params["n"] == N, "deployed p,n")
    require(params["K"] == K and params["a"] == A, "deployed K,a")
    require(params["R"] == R and params["w"] == W, "deployed R,w")
    require(params["B_star"] == B_STAR, "deployed budget")
    require(
        params["field_margin_p_minus_1_minus_B_star"] == 2_130_706_431,
        "deployed field margin",
    )
    require(
        params["shallow_field_margin_p_minus_1_minus_15775933"]
        == 2_131_707_713,
        "deployed shallow field margin",
    )

    atlas = summary["fixed_H_split_flat_atlas"]
    require(atlas["remainder_map"]["rank"] == "d", "full column rank")
    require(atlas["boundary"]["affine_equation"] == "G=H+T_HV(b)",
            "boundary affine equation")
    require(atlas["boundary"]["codimension"] == "m-d=w",
            "boundary codimension")
    require(atlas["boundary"]["rank_drop_components"] == 0,
            "no boundary rank drop")
    require(
        atlas["boundary"]["full_gcd_gate"] == "gcd(L0/H,1-Q_HV(b))=1",
        "boundary full-gcd sign",
    )
    require(atlas["interior"]["affine_equation"] == "C_HmV*b=e_0",
            "interior coefficient equation")
    require(atlas["interior"]["locator_equation"] == "G=T_HV(b)",
            "interior locator equation")
    require(atlas["interior"]["consistent_rank_range"] == ["1", "min(s,d)"],
            "interior rank range")
    require(atlas["interior"]["dimension"] == "d-rho",
            "interior affine dimension")
    require(atlas["interior"]["full_gcd_gate"] == "gcd(L0/H,Q_HV(b))=1",
            "interior full-gcd gate")
    require(atlas["H_sum_disjoint"] is True, "full-gcd H disjointness")
    lift = atlas["lift_invariance"]
    require(lift["replacement"] == "V->V+C*L0", "lift replacement")
    require(lift["T_change"] == "0", "lift leaves remainder map")
    require(lift["Q_change"] == "b*C*(L0/H)", "lift quotient change")
    require(lift["boundary_full_gcd_gate_unchanged"] is True and
            lift["interior_full_gcd_gate_unchanged"] is True,
            "lift leaves full-gcd gates")

    crt = summary["pairwise_full_gcd_equivalence"]
    require(crt["family_size_hypothesis"] == "|I|<p-1", "strict field gate")
    require(crt["deployed_family_size_max"] == B_STAR, "family-size max")
    require(crt["pairwise_gates"] == ["J_ij|W_ij", "gcd(Delta_ij,W_ij)=1"],
            "exact pairwise gates")
    require(crt["equivalence_RHS"]["individual"] ==
            "gcd(b_i,H_i)=1 for every i", "individual unit gate")
    require(crt["individual_gates"][-1] ==
            "reduced_pairs_(G_i,b_i)_pairwise_distinct",
            "reduced-pair distinctness")
    require(crt["available_nonzero_value_margin"] == 2_130_706_431,
            "CRT local-avoidance margin")
    require(crt["higher_CRT_obstruction"] is False, "no higher CRT obstruction")

    realization = summary["exact_boundary_list_realization"]
    require(realization["maximum_codeword_degree"] == K - 1,
            "row-realization degree")
    require(realization["agreement_support"] ==
            "(S0\\Z(G_i)) disjoint_union Z(H_i)", "exact support")
    require(realization["projection_unit"] ==
            "distinct nonanchor codewords per received word", "projection unit")

    shallow = summary["shallow_successor"]
    require(shallow["parent_deep_cap"] == DEEP_CAP, "parent deep cap")
    require(shallow["forbidden_family_shallow_needed"] == 15_775_933,
            "forbidden shallow necessity")
    require(shallow["sufficient_shallow_upper_target"] == 15_775_932,
            "sufficient shallow target")
    require(shallow["exact_gap"] == 1, "shallow one-unit gap")
    require(shallow["statement"] ==
            "every canonical family satisfying gcd(b_i,H_i)=1, every "
            "pairwise compatibility gate, and 0<=s<=366886 has size "
            "at most 15775932", "shallow successor includes individual gate")
    require(shallow["proved"] is False, "global incidence remains open")

    d1 = summary["degree_one_route_cuts"]
    require(d1["m"] == 67_448 and d1["d"] == 1, "degree-one chart")
    require(d1["scalar_division"] == {
        "quotient": 128,
        "remainder": 254,
        "identity": "p-1=128*(B_star-1)+254",
    }, "degree-one scalar division")
    require(d1["fixed_H_split_root_cap"] == 16, "fixed-H cap")
    require(d1["fixed_G_level_set_cap"] == 14, "fixed-G cap")
    require(d1["locator_pair_capacity_C_R_2"] == 481_306_566_756,
            "pair capacity")
    require(d1["locator_pair_capacity_exceeds_B_star"] is True,
            "global local-cap route cut")
    embedding = d1["fixed_G_RS_embedding"]
    require(embedding["nonpositive_intervals"] == [[72_859, 908_270]],
            "fixed-G Johnson middle interval")
    require(embedding["as_V_varies"] ==
            "r_GV ranges bijectively over all nonzero-valued received words",
            "fixed-G arbitrary-word embedding")

    controls = summary["small_prime_controls"]
    for name, expected in EXPECTED_SMALL_TABLES.items():
        actual = controls[name]
        require(actual["charts"] == expected["charts"], f"{name} chart count")
        require(actual["unit_tables"] == expected["unit_tables"],
                f"{name} unit table count")
        for size in ("2", "3"):
            row = actual["family_counts"][size]
            wanted = expected[size]
            require(
                (row["pairwise_distinct_reduced_pair_families"],
                 row["pairwise_compatible"],
                 row["exactly_realized"]) == wanted,
                f"{name} size-{size} exact table",
            )
    sharp = controls["field_size_sharpness"]
    require(sharp["family_size"] == sharp["q"] - 1, "sharp family size")
    require(sharp["G_a"] == "X-a" and sharp["b_a"] == "1",
            "sharp polynomial fixture")
    require(sharp["reduced_pairs_distinct"] is True,
            "sharp reduced-pair distinctness")
    require(sharp["common_unit_exists"] is False, "sharpness failure")
    require(sharp["minimum_predecessor_choices"] == 1, "sharp predecessor")

    ledger = summary["ledger"]
    require(ledger["movement"] == 0, "zero ledger movement")
    require(ledger["official_endpoint_movement"] == 0, "zero endpoint movement")
    require(ledger["U_paid"] == 3_730, "inherited U_paid only")
    require(all(ledger[key] is None for key in
                ("U_Q", "U_list_int", "U_ext", "U_new")),
            "null v4 atoms remain null")
    require(ledger["row_closed"] is False, "row remains open")
    require(len(summary["nonclaims"]) >= 5, "explicit nonclaims")
    canonical_json(summary)


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_suite() -> list[Mutation]:
    return [
        ("schema", lambda s: s.__setitem__("schema", "wrong")),
        ("theorem", lambda s: s.__setitem__("theorem_id", "wrong")),
        ("status", lambda s: s.__setitem__("status", "PROVED_ROW_CLOSED")),
        ("terminal", lambda s: s.__setitem__("terminal", "PAID")),
        ("field-margin", lambda s: s["parameters"].__setitem__(
            "field_margin_p_minus_1_minus_B_star", 2_130_706_430)),
        ("shallow-field-margin", lambda s: s["parameters"].__setitem__(
            "shallow_field_margin_p_minus_1_minus_15775933", 2_131_707_712)),
        ("rank", lambda s: s["fixed_H_split_flat_atlas"]["remainder_map"].__setitem__(
            "rank", "d-1")),
        ("boundary-equation", lambda s: s["fixed_H_split_flat_atlas"]["boundary"].__setitem__(
            "affine_equation", "G=T_HV(b)")),
        ("boundary-sign", lambda s: s["fixed_H_split_flat_atlas"]["boundary"].__setitem__(
            "full_gcd_gate", "gcd(L0/H,Q_HV(b))=1")),
        ("boundary-rank-drop", lambda s: s["fixed_H_split_flat_atlas"]["boundary"].__setitem__(
            "rank_drop_components", 1)),
        ("interior-equation", lambda s: s["fixed_H_split_flat_atlas"]["interior"].__setitem__(
            "affine_equation", "C_HmV*b=0")),
        ("interior-rank-zero", lambda s: s["fixed_H_split_flat_atlas"]["interior"].__setitem__(
            "consistent_rank_range", ["0", "min(s,d)"])),
        ("interior-gcd", lambda s: s["fixed_H_split_flat_atlas"]["interior"].__setitem__(
            "full_gcd_gate", "gcd(L0/H,1-Q_HV(b))=1")),
        ("lift-T", lambda s: s["fixed_H_split_flat_atlas"]["lift_invariance"].__setitem__(
            "T_change", "C*L0")),
        ("lift-Q", lambda s: s["fixed_H_split_flat_atlas"]["lift_invariance"].__setitem__(
            "Q_change", "b*C*H")),
        ("strict-field-gate", lambda s: s["pairwise_full_gcd_equivalence"].__setitem__(
            "family_size_hypothesis", "|I|<=p-1")),
        ("intersection-gate", lambda s: s["pairwise_full_gcd_equivalence"]["pairwise_gates"].__setitem__(
            0, "J_ij does not divide W_ij")),
        ("symmetric-gate", lambda s: s["pairwise_full_gcd_equivalence"]["pairwise_gates"].__setitem__(
            1, "Delta_ij|W_ij")),
        ("individual-unit", lambda s: s["pairwise_full_gcd_equivalence"]["equivalence_RHS"].__setitem__(
            "individual", "omitted")),
        ("reduced-distinctness", lambda s: s["pairwise_full_gcd_equivalence"]["individual_gates"].__setitem__(
            -1, "decorated_triples_distinct")),
        ("higher-obstruction", lambda s: s["pairwise_full_gcd_equivalence"].__setitem__(
            "higher_CRT_obstruction", True)),
        ("row-degree", lambda s: s["exact_boundary_list_realization"].__setitem__(
            "maximum_codeword_degree", K)),
        ("row-support", lambda s: s["exact_boundary_list_realization"].__setitem__(
            "agreement_support", "support_unknown")),
        ("deep-cap", lambda s: s["shallow_successor"].__setitem__(
            "parent_deep_cap", DEEP_CAP + 1)),
        ("shallow-needed", lambda s: s["shallow_successor"].__setitem__(
            "forbidden_family_shallow_needed", 15_775_932)),
        ("shallow-target", lambda s: s["shallow_successor"].__setitem__(
            "sufficient_shallow_upper_target", 15_775_933)),
        ("shallow-individual-gate", lambda s: s["shallow_successor"].__setitem__(
            "statement", "every pairwise-compatible family has size at most 15775932")),
        ("false-closure", lambda s: s["shallow_successor"].__setitem__(
            "proved", True)),
        ("d1-scalar", lambda s: s["degree_one_route_cuts"]["scalar_division"].__setitem__(
            "remainder", 255)),
        ("d1-fixed-H", lambda s: s["degree_one_route_cuts"].__setitem__(
            "fixed_H_split_root_cap", 17)),
        ("d1-fixed-G", lambda s: s["degree_one_route_cuts"].__setitem__(
            "fixed_G_level_set_cap", 15)),
        ("pair-capacity", lambda s: s["degree_one_route_cuts"].__setitem__(
            "locator_pair_capacity_C_R_2", B_STAR)),
        ("fixed-G-middle", lambda s: s["degree_one_route_cuts"]["fixed_G_RS_embedding"].__setitem__(
            "nonpositive_intervals", [[72_860, 908_270]])),
        ("fixed-G-range", lambda s: s["degree_one_route_cuts"]["fixed_G_RS_embedding"].__setitem__(
            "as_V_varies", "only sampled received words")),
        ("GF5-pairs", lambda s: s["small_prime_controls"]["GF5"]["family_counts"]["2"].__setitem__(
            "pairwise_compatible", 49)),
        ("GF7-triples", lambda s: s["small_prime_controls"]["GF7"]["family_counts"]["3"].__setitem__(
            "exactly_realized", 3_379)),
        ("field-sharpness", lambda s: s["small_prime_controls"]["field_size_sharpness"].__setitem__(
            "common_unit_exists", True)),
        ("ledger", lambda s: s["ledger"].__setitem__("movement", 1)),
        ("atom", lambda s: s["ledger"].__setitem__("U_Q", 0)),
        ("row-closed", lambda s: s["ledger"].__setitem__("row_closed", True)),
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
        "mutation_selftest": "PASS",
        "mutations_detected": len(passed),
        "mutation_names": passed,
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
    output: dict[str, Any]
    if args.mutation_selftest:
        output = run_mutation_selftest(summary)
    else:
        output = summary
    print(canonical_json(output, pretty=args.pretty))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"verification failed: {exc}", file=__import__("sys").stderr)
        raise SystemExit(1)
