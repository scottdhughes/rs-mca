#!/usr/bin/env python3
"""Exact arithmetic verifier for the M31 boundary cross-G route cut.

This is deliberately a route-cut verifier, not a list-size certificate.  It
checks the strongest consequences currently available from pairwise
root/support incidence, locates the exact Johnson transitions, and records a
large support-only Chebyshev countermodel.  In particular it never promotes
the support model to a common received word, a common unit ``V``, or an RS
list.

All proof-critical checks use explicit exceptions and remain live under
``python -O``.  The verifier uses only the Python standard library and no
floating-point comparisons.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from itertools import combinations
from math import prod
from typing import Any, Callable, Iterable


P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
BUDGET = 16_777_215
FORBIDDEN = BUDGET + 1

M_MIN = W + 1
M_MAX = R
ROOT_DEFICIT = R - W

FIXED_POSITIVE_WINGS = ((67_448, 72_858), (908_271, 981_129))
FIXED_3730_WINGS = ((67_448, 72_837), (908_292, 981_129))
FIXED_46_WINGS = ((67_448, 71_176), (909_953, 981_129))

UNIFORM_POSITIVE_S = 177_835
UNIFORM_3730_S = 177_901
UNIFORM_46_S = 183_167
WHOLE_JOHNSON_S = 366_887


class VerificationError(RuntimeError):
    """Raised when an exact gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    """Fail closed without relying on ``assert``."""

    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> str:
    try:
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


def fixed_denominator(m: int, slack: int) -> int:
    return (m + slack) ** 2 - R * (m - W - 1)


def fixed_numerator(slack: int) -> int:
    return R * (W + slack + 1)


def fixed_cap(m: int, slack: int) -> int | None:
    denominator = fixed_denominator(m, slack)
    if denominator <= 0:
        return None
    return fixed_numerator(slack) // denominator


def scan_fixed_slack(slack: int) -> dict[str, Any]:
    positive: list[int] = []
    maximum_cap = -1
    maximum_cap_m = -1
    minimum_denominator: int | None = None
    minimum_denominator_m = -1
    numerator = fixed_numerator(slack)
    # Legal pairs satisfy h >= m+slack and h <= R, hence m <= R-slack.
    for m in range(M_MIN, M_MAX - slack + 1):
        denominator = fixed_denominator(m, slack)
        if minimum_denominator is None or denominator < minimum_denominator:
            minimum_denominator = denominator
            minimum_denominator_m = m
        if denominator > 0:
            positive.append(m)
            cap = numerator // denominator
            if cap > maximum_cap:
                maximum_cap = cap
                maximum_cap_m = m
    require(minimum_denominator is not None, "empty fixed-G scan")
    return {
        "positive_intervals": [list(pair) for pair in intervals(positive)],
        "minimum_denominator": minimum_denominator,
        "minimum_denominator_m": minimum_denominator_m,
        "maximum_cap": maximum_cap if positive else None,
        "maximum_cap_m": maximum_cap_m if positive else None,
    }


def cap_intervals_at_zero(cap: int) -> tuple[tuple[int, int], ...]:
    return intervals(
        m
        for m in range(M_MIN, M_MAX + 1)
        if fixed_denominator(m, 0) > 0 and fixed_cap(m, 0) <= cap
    )


def cap_gate_slack(m: int, slack: int, cap: int) -> int:
    """Positive exactly when floor(numerator/denominator) <= cap."""

    return (cap + 1) * fixed_denominator(m, slack) - fixed_numerator(slack)


def minimum_cap_gate(slack: int, cap: int) -> tuple[int, int]:
    best: int | None = None
    best_m = -1
    for m in range(M_MIN, M_MAX - slack + 1):
        value = cap_gate_slack(m, slack, cap)
        if best is None or value < best:
            best = value
            best_m = m
    require(best is not None, "empty cap-gate scan")
    return best, best_m


def whole_denominator(slack: int) -> int:
    agreement = A + slack
    return agreement * agreement - N * (K - 1)


def whole_numerator(slack: int) -> int:
    agreement = A + slack
    return N * (agreement - K + 1)


def whole_moment_polynomial(slack: int, list_size: int) -> int:
    return list_size * whole_denominator(slack) - whole_numerator(slack)


def packing_ratio_floor(deficit: int) -> int:
    """floor(binomial(N,K)/binomial(N-deficit,K)) without huge binomials."""

    numerator = prod(N - index for index in range(deficit))
    denominator = prod(N - K - index for index in range(deficit))
    return numerator // denominator


def exact_parameters() -> dict[str, int]:
    require(P == 2_147_483_647, "M31 prime integer drift")
    require(N == 2_097_152 and K == 1_048_576, "length/dimension drift")
    require(N == 2 * K, "N=2K gate")
    require(R == 981_129, "radius drift")
    require(W == 67_447, "agreement excess drift")
    require(P**4 // 2**100 == BUDGET, "budget arithmetic drift")
    require(FORBIDDEN == 2**24, "forbidden list size drift")
    require(ROOT_DEFICIT == 913_682, "root-deficit arithmetic drift")
    return {
        "p": P,
        "n": N,
        "K": K,
        "agreement": A,
        "R": R,
        "w": W,
        "budget": BUDGET,
        "forbidden": FORBIDDEN,
    }


def fixed_g_johnson_summary() -> dict[str, Any]:
    at_zero = scan_fixed_slack(0)
    require(
        tuple(map(tuple, at_zero["positive_intervals"])) == FIXED_POSITIVE_WINGS,
        "s=0 positive-wing endpoints",
    )
    wings_3730 = cap_intervals_at_zero(3_730)
    wings_46 = cap_intervals_at_zero(46)
    require(wings_3730 == FIXED_3730_WINGS, "s=0 cap-3730 wings")
    require(wings_46 == FIXED_46_WINGS, "s=0 cap-46 wings")

    before_positive = scan_fixed_slack(UNIFORM_POSITIVE_S - 1)
    at_positive = scan_fixed_slack(UNIFORM_POSITIVE_S)
    require(
        before_positive["minimum_denominator"] <= 0,
        "uniform-positive predecessor must fail",
    )
    require(
        at_positive["minimum_denominator"] > 0,
        "uniform-positive threshold must pass",
    )
    require(at_positive["maximum_cap"] == 327_043, "threshold maximum cap")
    require(
        2 * (M_MIN + UNIFORM_POSITIVE_S) > 0,
        "denominator monotonicity after positivity threshold",
    )

    cap_records: dict[str, Any] = {}
    for cap, threshold, predecessor_max, threshold_max in (
        (3_730, UNIFORM_3730_S, 3_731, 3_675),
        (46, UNIFORM_46_S, 47, 46),
    ):
        predecessor = scan_fixed_slack(threshold - 1)
        current = scan_fixed_slack(threshold)
        predecessor_gate, predecessor_m = minimum_cap_gate(threshold - 1, cap)
        current_gate, current_m = minimum_cap_gate(threshold, cap)
        derivative_floor = 2 * (cap + 1) * (M_MIN + threshold) - R
        require(predecessor["maximum_cap"] == predecessor_max,
                f"cap-{cap} predecessor maximum")
        require(current["maximum_cap"] == threshold_max,
                f"cap-{cap} threshold maximum")
        require(predecessor_gate <= 0, f"cap-{cap} predecessor sharpness")
        require(current_gate > 0, f"cap-{cap} threshold pass")
        require(derivative_floor > 0, f"cap-{cap} monotonicity")
        cap_records[str(cap)] = {
            "first_uniform_slack": threshold,
            "predecessor_maximum_cap": predecessor_max,
            "threshold_maximum_cap": threshold_max,
            "predecessor_minimum_gate": predecessor_gate,
            "predecessor_gate_m": predecessor_m,
            "threshold_minimum_gate": current_gate,
            "threshold_gate_m": current_m,
            "future_monotonicity_derivative_floor": derivative_floor,
        }

    direct_singleton_m = R - W
    require(direct_singleton_m == 913_682, "direct singleton threshold")
    require(
        (direct_singleton_m - 1) + W + 1 == R,
        "two-support predecessor union can fit exactly",
    )
    require(
        direct_singleton_m + W + 1 == R + 1,
        "two-support singleton threshold",
    )

    return {
        "bound": "N_G(s)<=floor(R*(w+s+1)/D)",
        "denominator": "D=(m+s)^2-R*(m-w-1)",
        "m_range": [M_MIN, M_MAX],
        "s_zero": {
            "positive_wings": [list(pair) for pair in FIXED_POSITIVE_WINGS],
            "cap_at_most_3730_wings": [list(pair) for pair in FIXED_3730_WINGS],
            "cap_at_most_46_wings": [list(pair) for pair in FIXED_46_WINGS],
        },
        "uniform_positive": {
            "first_slack": UNIFORM_POSITIVE_S,
            "predecessor_has_nonpositive_denominator": True,
            "maximum_cap_at_threshold": 327_043,
            "maximum_cap_m_at_threshold": at_positive["maximum_cap_m"],
        },
        "uniform_caps": cap_records,
        "direct_pair_union": {
            "intersection_root_bound": "|H1 intersect H2|<=m-w-1",
            "union_lower": "|H1 union H2|>=m+w+1",
            "N_G_at_most_one_from_m": direct_singleton_m,
        },
    }


def whole_list_johnson_summary() -> dict[str, Any]:
    before = WHOLE_JOHNSON_S - 1
    denominator_before = whole_denominator(before)
    denominator_at = whole_denominator(WHOLE_JOHNSON_S)
    numerator_at = whole_numerator(WHOLE_JOHNSON_S)
    require(denominator_before == -2_056_119, "whole Johnson predecessor D")
    require(denominator_at == 909_700, "whole Johnson threshold D")
    require(numerator_at == 910_866_513_920, "whole Johnson numerator")
    cap = numerator_at // denominator_at
    require(cap == 1_001_282, "whole Johnson threshold cap")
    require(cap <= BUDGET, "whole Johnson threshold budget fit")

    polynomial_before = whole_moment_polynomial(before, BUDGET)
    polynomial_at = whole_moment_polynomial(WHOLE_JOHNSON_S, BUDGET)
    require(polynomial_before == -35_406_814_945_353,
            "moment polynomial predecessor")
    require(polynomial_at == 14_351_365_971_580,
            "moment polynomial threshold")
    require(polynomial_before < 0 < polynomial_at,
            "exact moment root bracket")
    derivative_floor = 2 * BUDGET * (A + before) - N
    require(derivative_floor > 0, "moment polynomial monotonicity")

    shallow_total = FORBIDDEN - cap
    shallow_nonanchors = shallow_total - 1
    require(shallow_nonanchors == 15_775_933,
            "forbidden shallow-nonanchor residue")
    substituted_high_weight_count = WHOLE_JOHNSON_S
    substituted_rank46_baseline = cap + 45 * substituted_high_weight_count
    parent_rank46_baseline = 3_730 + 45 * 366_969
    require(substituted_rank46_baseline == 17_511_197,
            "rank-46 substituted baseline")
    require(substituted_rank46_baseline - BUDGET == 733_982,
            "rank-46 substituted baseline excess")
    require(parent_rank46_baseline == 16_517_335,
            "parent rank-46 baseline")
    return {
        "bound": "L<=floor(n*(A_s-K+1)/(A_s^2-n*(K-1)))",
        "A_s": "agreement+s",
        "first_positive_denominator_slack": WHOLE_JOHNSON_S,
        "threshold_cap": cap,
        "predecessor_fits_budget": False,
        "forbidden_list_shallow_nonanchors_lower": shallow_nonanchors,
        "rank46_cutoff_substitution": {
            "bankable_replacement": False,
            "high_weight_count": substituted_high_weight_count,
            "parent_baseline": parent_rank46_baseline,
            "substituted_baseline": substituted_rank46_baseline,
            "substituted_baseline_exceeds_budget_by": 733_982,
        },
        "moment_polynomial": {
            "definition": "P_L(s)=L*((A+s)^2-n*(K-1))-n*(A+s-K+1)",
            "list_size": BUDGET,
            "at_366886": polynomial_before,
            "at_366887": polynomial_at,
            "unique_root_in_open_interval": [366_886, 366_887],
            "future_derivative_positive": True,
        },
    }


def wronskian_and_dimension_summary() -> dict[str, Any]:
    d_min = M_MIN - W
    d_max = M_MAX - W
    n4 = (P**4 - 1) // (P - 1)
    h4 = (P**3 - 1) // (P - 1)
    scalar_left = FORBIDDEN * R * h4
    scalar_right = (W + 1) * n4
    scalar_margin = scalar_right - scalar_left
    require(d_min == 1 and d_max == ROOT_DEFICIT,
            "coefficient-dimension range")
    require(P - 1 > BUDGET, "one base-field coefficient already exceeds budget")
    require(FORBIDDEN < P, "base-field fresh-symbol gate")
    require(n4 == 9_903_520_305_059_670_166_633_185_280,
            "scalar-descent N4")
    require(h4 == 4_611_686_016_279_904_257,
            "scalar-descent H4")
    require(scalar_left == 75_911_179_514_902_718_909_260_442_370_048,
            "scalar-descent left side")
    require(scalar_right == 667_972_637_535_664_633_399_075_080_765_440,
            "scalar-descent right side")
    require(scalar_margin == 592_061_458_020_761_914_489_814_638_395_392,
            "scalar-descent strict margin")
    return {
        "cross_g_determinant": {
            "polynomial": "W_12=G_1*b_2-G_2*b_1",
            "nonzero_for_distinct_canonical_pairs": True,
            "nonzero_reason": "gcd(b_i,G_i)=1 and monic G_i force equality of both pairs if W_12=0",
            "degree_bound": "deg(W_12)<=m_1+m_2-w-1",
            "support_implication": "H_1 intersect H_2 is contained in Z(W_12)",
            "intersection_bound": "|H_1 intersect H_2|<=m_1+m_2-w-1",
            "root_deficit_R_minus_w": ROOT_DEFICIT,
        },
        "fixed_g_specialization": {
            "degree_bound": "deg(b_1-b_2)<=m-w-1",
            "intersection_bound": "|H_1 intersect H_2|<=m-w-1",
        },
        "base_field_dimension_route_cut": {
            "ambient_dimension_over_Fp": "4d",
            "dimension_upper_bound_over_Fp": "d",
            "d_definition": "d=m-w",
            "d_range": [d_min, d_max],
            "uniform_minimum_codimension_over_Fp": "3d",
            "V_equals_1_attains_dimension_d": True,
            "smallest_raw_nonzero_b_count": P - 1,
            "smallest_raw_count_exceeds_budget": True,
            "V_equals_1_boundary_equality": "H=G-b, deg(H)=m, b=G-H",
            "general_unit_V_forced_to_1": False,
            "dimension_count_is_a_census": False,
            "live_counterexample_reduction": {
                "base_field": "F_p",
                "boundary_forcing_after_projection": True,
                "every_base_unit_V_still_realizable": True,
                "fresh_symbol_gate": "2^24<p",
                "projected_b_coefficients_in_base_field": True,
                "projected_V_in_base_residue_ring": True,
                "quartic_violation_implies_base_boundary_violation": True,
                "scalar_descent_is_ledger_payment": False,
                "scalar_descent_margin": scalar_margin,
                "strict_scalar_descent_gate": True,
            },
        },
    }


def support_only_gilbert_summary() -> dict[str, Any]:
    # For x=1/16 and 0<x<1,
    #   x^W sum_{i<=W} C(R,i) <= (1+x)^R.
    # Therefore V(R,W) <= 17^R / 16^(R-W).  The following comparison is an
    # exact integer proof that this is <44^W; no logarithms or floats enter.
    require(pow(17, R) < pow(44, W) * pow(16, R - W),
            "exact rational Gilbert volume comparison")
    require(44 < 2**6, "44^w<2^(6w)")
    gilbert_exponent = R - 6 * W
    require(gilbert_exponent == 576_447, "Gilbert exponent")
    require(R < 2**20, "weight-shell divisor bound")
    shell_exponent = gilbert_exponent - 20
    require(shell_exponent == 576_427, "fixed-shell exponent")
    require(2**shell_exponent > BUDGET, "fixed-shell budget separation")

    require(K - W == R, "remaining T2 fibres equal R")
    require(2 * W + R == A, "support size algebra")
    require(W <= K // 2, "distinct T4 host fibres exist")
    require(A - (W + 1) == K - 1, "MDS pair-intersection gate")

    return {
        "binary_gilbert": {
            "ambient_length": R,
            "minimum_distance": W + 1,
            "volume": "sum_{i=0}^w binom(R,i)",
            "rational_volume_witness": "x=1/16",
            "exact_integer_gate": "17^R < 44^w*16^(R-w)",
            "volume_strict_upper": "44^w<2^(6w)",
            "family_size_strict_lower": f"2^{gilbert_exponent}",
            "translate_to_contain_zero": True,
            "fixed_nonzero_weight_shell_strict_lower": f"2^{shell_exponent}",
            "requested_weaker_shell_lower_holds": "shell_size>2^576426",
        },
        "chebyshev_support_model": {
            "T2_fibres": K,
            "T4_fibres": K // 2,
            "fixed_complete_T2_fibres": W,
            "complete_T2_hosts_distinct_mod_T4": True,
            "remaining_singleton_T2_fibres": R,
            "support_size": A,
            "full_T2_count": W,
            "full_T4_count": 0,
            "pair_intersection": "A-HammingDistance(z,z')",
            "pair_intersection_at_most": K - 1,
            "relative_to_zero_G_size": "weight(z)",
            "relative_to_zero_H_size": "weight(z)",
            "fixed_weight_slack_s": 0,
        },
        "scope_guards": {
            "same_received_word_RS_list": False,
            "common_V_realized": False,
            "polynomial_G_b_realized": False,
            "support_only_pairwise_root_budget_control": True,
        },
    }


def k_subset_packing_summary() -> dict[str, Any]:
    cap_23 = packing_ratio_floor(23)
    cap_24 = packing_ratio_floor(24)
    require(cap_23 == 8_389_620, "K-subset packing cap at n-23")
    require(cap_24 == 16_779_424, "K-subset packing cap at n-24")
    require(cap_23 <= BUDGET < cap_24, "K-subset transition")
    max_nonanchor_agreement = N - (W + 1)
    require(max_nonanchor_agreement == 2_029_704,
            "maximum nonanchor agreement")
    require(max_nonanchor_agreement < N - 24,
            "packing transition is unreachable by nonanchors")
    return {
        "method": "disjoint K-subsets of pairwise agreement sets",
        "last_budget_fitting_agreement": N - 23,
        "cap_at_n_minus_23": cap_23,
        "first_nonfitting_agreement": N - 24,
        "cap_at_n_minus_24": cap_24,
        "maximum_nonanchor_agreement": max_nonanchor_agreement,
        "minimum_nonanchor_deficit": W + 1,
        "closes_boundary_census": False,
    }


def polynomial_value(coefficients: tuple[int, ...], x: int, modulus: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * x + coefficient) % modulus
    return value


def v_equals_1_route_cut_summary() -> dict[str, Any]:
    toy_p = 7
    toy_domain = tuple(range(6))
    toy_k = 2
    toy_a = 3
    toy_center = (0, 0, 0, 1, 5, 4)

    prefix_counts = [0] * toy_p
    for support in combinations(toy_domain, toy_a):
        prefix_counts[(-sum(support)) % toy_p] += 1
    require(tuple(prefix_counts) == (3, 3, 3, 2, 3, 3, 3),
            "F7 depth-one prefix fibres")
    require(max(prefix_counts) - 1 == 2,
            "F7 maximum V=1 companion census")

    listed: list[dict[str, Any]] = []
    for constant in range(toy_p):
        for slope in range(toy_p):
            support = [
                x for x, received in zip(toy_domain, toy_center)
                if (constant + slope * x) % toy_p == received
            ]
            if len(support) >= toy_a:
                listed.append({
                    "polynomial": [constant, slope],
                    "agreement_support": support,
                })
    require(listed == [
        {"polynomial": [0, 0], "agreement_support": [0, 1, 2]},
        {"polynomial": [0, 5], "agreement_support": [0, 3, 5]},
        {"polynomial": [2, 6], "agreement_support": [2, 4, 5]},
        {"polynomial": [3, 4], "agreement_support": [1, 3, 4]},
    ], "F7 exact boundary list")

    h0 = (6, 5, 3)
    v = (1, 3, 5)
    error_domain = (3, 4, 5)
    h0_table = tuple(polynomial_value(h0, x, toy_p) for x in error_domain)
    v_table = tuple(polynomial_value(v, x, toy_p) for x in error_domain)
    require(h0_table == (6, 4, 1), "F7 H0 table")
    require(v_table == (6, 2, 1), "F7 V table")
    require(all((left * right) % toy_p == 1
                for left, right in zip(h0_table, v_table)),
            "F7 V is inverse to H0 on E0")

    source_list_floor = 6_796_405
    source_companion_floor = source_list_floor - 1
    companion_target = BUDGET - 1
    require(source_companion_floor == 6_796_404,
            "deployed V=1 companion floor")
    require(companion_target - source_companion_floor == 9_980_810,
            "deployed V=1 headroom")
    require(P > W, "Newton identities characteristic gate")

    return {
        "exact_identity": "#X_S(1)=|Fib_w(prefix_w(L_S))|-1",
        "all_pairs_are_boundary": True,
        "boundary_equations": "H=G-b; deg(H)=deg(G)=m; b=G-H",
        "newton_power_sum_equivalence_gate": "p>w",
        "deployed_source_list_floor": source_list_floor,
        "deployed_source_companion_floor": source_companion_floor,
        "deployed_companion_target": companion_target,
        "deployed_headroom_after_source": 9_980_810,
        "source_floor_is_uniform_over_anchors": False,
        "toy_nonextremality": {
            "field": "F_7",
            "domain": list(toy_domain),
            "K": toy_k,
            "agreement": toy_a,
            "center": list(toy_center),
            "depth_one_prefix_fibre_sizes": prefix_counts,
            "maximum_V_equals_1_companions": 2,
            "boundary_anchor_support": [0, 1, 2],
            "H0_coefficients_low_to_high": list(h0),
            "V_coefficients_low_to_high": list(v),
            "H0_table_on_E0": list(h0_table),
            "V_table_on_E0": list(v_table),
            "list": listed,
            "arbitrary_V_companions": len(listed) - 1,
            "arbitrary_V_beats_global_V_equals_1": True,
        },
        "general_reduction_to_V_equals_1": False,
        "deployed_domain_comparison_proved": False,
        "ledger_payment": False,
    }


def build_summary() -> dict[str, Any]:
    whole = whole_list_johnson_summary()
    moment = copy.deepcopy(whole.pop("moment_polynomial"))
    wronskian_and_dimension = wronskian_and_dimension_summary()
    support_countermodel = support_only_gilbert_summary()
    summary = {
        "schema": "m31-boundary-common-v-cross-g-route-cut-summary-v1",
        "theorem_id": "M31_BOUNDARY_COMMON_V_CROSS_G_ROUTE_CUT_V1",
        "row_contract": {
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "quantifier": "EVERY_BOUNDARY_ANCHOR_TRIPLE_A0_L0_V",
            "remaining_exact_census": "sum_G #admissible_b <= 16777214",
            "remaining_exact_census_proved": False,
            "terminal": "UNPAID_BOUNDARY_COMMON_V_FULL_LOCATOR_COEFFICIENT_INCIDENCE",
        },
        "deployed_parameters": exact_parameters(),
        "fixed_G_bound": fixed_g_johnson_summary(),
        "wronskian_route_cut": {
            "cross_G": wronskian_and_dimension["cross_g_determinant"],
            "fixed_G": wronskian_and_dimension["fixed_g_specialization"],
        },
        "split_support_moment": {
            "method": "whole-list pairwise agreement-set second moment",
            **moment,
        },
        "whole_list_deep_cut": whole,
        "base_field_route_cut": wronskian_and_dimension[
            "base_field_dimension_route_cut"
        ],
        "v_equals_1_route_cut": v_equals_1_route_cut_summary(),
        "chebyshev_support_countermodel": support_countermodel,
        "singleton_packing": k_subset_packing_summary(),
        "nonclaims": {
            "pairwise_bounds_close_global_sum": False,
            "support_only_folding_closes_global_sum": False,
            "common_V_inference_authorized": False,
            "uniform_pair_census_proved": False,
            "same_received_word_RS_list_from_countermodel": False,
            "polynomial_realization_from_countermodel": False,
        },
        "ledger_state": {
            "ledger_movement": 0,
            "U_paid_added": None,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "U_new": None,
            "row_closed": False,
        },
        "status": "PROVED_EXACT_ROUTE_CUTS_SHALLOW_COMMON_V_FULL_LOCATOR_RESIDUAL_OPEN",
    }
    return summary


def validate_summary(candidate: Any, expected: dict[str, Any]) -> None:
    require(type(candidate) is dict, "summary must be an object")
    require(canonical_json(candidate) == canonical_json(expected),
            "summary differs from exact recomputation")


def set_path(obj: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    current: Any = obj
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = value


def mutation_suite(expected: dict[str, Any]) -> dict[str, Any]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("agreement_off_by_one", lambda d: set_path(d, ("deployed_parameters", "agreement"), A + 1)),
        ("radius_off_by_one", lambda d: set_path(d, ("deployed_parameters", "R"), R - 1)),
        ("positive_left_wing_endpoint", lambda d: d["fixed_G_bound"]["s_zero"]["positive_wings"][0].__setitem__(1, 72_859)),
        ("cap_3730_wing_endpoint", lambda d: d["fixed_G_bound"]["s_zero"]["cap_at_most_3730_wings"][1].__setitem__(0, 908_291)),
        ("cap_46_wing_endpoint", lambda d: d["fixed_G_bound"]["s_zero"]["cap_at_most_46_wings"][0].__setitem__(1, 71_177)),
        ("uniform_positive_off_by_one", lambda d: set_path(d, ("fixed_G_bound", "uniform_positive", "first_slack"), 177_834)),
        ("uniform_3730_off_by_one", lambda d: set_path(d, ("fixed_G_bound", "uniform_caps", "3730", "first_uniform_slack"), 177_900)),
        ("uniform_46_off_by_one", lambda d: set_path(d, ("fixed_G_bound", "uniform_caps", "46", "first_uniform_slack"), 183_166)),
        ("direct_singleton_off_by_one", lambda d: set_path(d, ("fixed_G_bound", "direct_pair_union", "N_G_at_most_one_from_m"), 913_681)),
        ("whole_threshold_off_by_one", lambda d: set_path(d, ("whole_list_deep_cut", "first_positive_denominator_slack"), 366_886)),
        ("whole_cap_off_by_one", lambda d: set_path(d, ("whole_list_deep_cut", "threshold_cap"), 1_001_283)),
        ("moment_predecessor_sign", lambda d: set_path(d, ("split_support_moment", "at_366886"), 1)),
        ("moment_threshold_sign", lambda d: set_path(d, ("split_support_moment", "at_366887"), -1)),
        ("shallow_nonanchor_off_by_one", lambda d: set_path(d, ("whole_list_deep_cut", "forbidden_list_shallow_nonanchors_lower"), 15_775_934)),
        ("false_rank46_cutoff_payment", lambda d: set_path(d, ("whole_list_deep_cut", "rank46_cutoff_substitution", "bankable_replacement"), True)),
        ("rank46_substituted_baseline", lambda d: set_path(d, ("whole_list_deep_cut", "rank46_cutoff_substitution", "substituted_baseline"), 17_511_196)),
        ("wronskian_zero", lambda d: set_path(d, ("wronskian_route_cut", "cross_G", "nonzero_for_distinct_canonical_pairs"), False)),
        ("root_deficit_off_by_one", lambda d: set_path(d, ("wronskian_route_cut", "cross_G", "root_deficit_R_minus_w"), 913_681)),
        ("dimension_off_by_one", lambda d: d["base_field_route_cut"]["d_range"].__setitem__(1, 913_681)),
        ("false_general_V_equals_1", lambda d: set_path(d, ("base_field_route_cut", "general_unit_V_forced_to_1"), True)),
        ("false_dimension_census", lambda d: set_path(d, ("base_field_route_cut", "dimension_count_is_a_census"), True)),
        ("scalar_descent_margin", lambda d: set_path(d, ("base_field_route_cut", "live_counterexample_reduction", "scalar_descent_margin"), 1)),
        ("projection_collision", lambda d: set_path(d, ("base_field_route_cut", "live_counterexample_reduction", "quartic_violation_implies_base_boundary_violation"), False)),
        ("false_scalar_payment", lambda d: set_path(d, ("base_field_route_cut", "live_counterexample_reduction", "scalar_descent_is_ledger_payment"), True)),
        ("V1_prefix_identity", lambda d: set_path(d, ("v_equals_1_route_cut", "exact_identity"), "#X_S(1)=|Fib_w|-1")),
        ("V1_source_floor", lambda d: set_path(d, ("v_equals_1_route_cut", "deployed_source_companion_floor"), 6_796_403)),
        ("V1_false_extremality", lambda d: set_path(d, ("v_equals_1_route_cut", "toy_nonextremality", "arbitrary_V_beats_global_V_equals_1"), False)),
        ("V1_false_reduction", lambda d: set_path(d, ("v_equals_1_route_cut", "general_reduction_to_V_equals_1"), True)),
        ("gilbert_exponent_off_by_one", lambda d: set_path(d, ("chebyshev_support_countermodel", "binary_gilbert", "family_size_strict_lower"), "2^576446")),
        ("shell_exponent_off_by_one", lambda d: set_path(d, ("chebyshev_support_countermodel", "binary_gilbert", "fixed_nonzero_weight_shell_strict_lower"), "2^576426")),
        ("full_T2_off_by_one", lambda d: set_path(d, ("chebyshev_support_countermodel", "chebyshev_support_model", "full_T2_count"), W + 1)),
        ("false_full_T4", lambda d: set_path(d, ("chebyshev_support_countermodel", "chebyshev_support_model", "full_T4_count"), 1)),
        ("false_received_word", lambda d: set_path(d, ("chebyshev_support_countermodel", "scope_guards", "same_received_word_RS_list"), True)),
        ("false_common_V", lambda d: set_path(d, ("chebyshev_support_countermodel", "scope_guards", "common_V_realized"), True)),
        ("false_polynomial_realization", lambda d: set_path(d, ("chebyshev_support_countermodel", "scope_guards", "polynomial_G_b_realized"), True)),
        ("packing_23_cap", lambda d: set_path(d, ("singleton_packing", "cap_at_n_minus_23"), 8_389_621)),
        ("packing_24_transition", lambda d: set_path(d, ("singleton_packing", "first_nonfitting_agreement"), N - 23)),
        ("max_nonanchor_agreement", lambda d: set_path(d, ("singleton_packing", "maximum_nonanchor_agreement"), N - W)),
        ("false_pairwise_summation", lambda d: set_path(d, ("nonclaims", "pairwise_bounds_close_global_sum"), True)),
        ("false_uniform_census", lambda d: set_path(d, ("nonclaims", "uniform_pair_census_proved"), True)),
        ("false_payment", lambda d: set_path(d, ("ledger_state", "ledger_movement"), 1)),
        ("false_paid_atom", lambda d: set_path(d, ("ledger_state", "U_paid_added"), 1)),
        ("false_closure", lambda d: set_path(d, ("ledger_state", "row_closed"), True)),
        ("unknown_top_level", lambda d: d.__setitem__("unexpected", True)),
    ]
    rejected: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(expected)
        mutate(candidate)
        try:
            validate_summary(candidate, expected)
        except VerificationError:
            rejected.append(name)
        else:
            raise VerificationError(f"mutation survived: {name}")
    require(len(rejected) == len(mutations), "not all mutations rejected")
    return {"mutations": len(mutations), "rejected": len(rejected), "names": rejected}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run exact checks")
    parser.add_argument("--json-summary", action="store_true", help="emit canonical summary")
    parser.add_argument(
        "--print-template",
        action="store_true",
        help="emit the canonical unsigned packet body",
    )
    parser.add_argument("--tamper-selftest", action="store_true", help="run hostile mutations")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    emit_json = args.json_summary or args.print_template
    run_check = args.check or not (emit_json or args.tamper_selftest)
    expected = build_summary()
    validate_summary(expected, expected)

    stream = sys.stderr if emit_json else sys.stdout
    if run_check:
        print(
            "PASS m31-boundary-cross-g-route-cut-v1 "
            f"checks={CHECKS} status={expected['status']}",
            file=stream,
        )
    if args.tamper_selftest:
        result = mutation_suite(expected)
        print(
            f"PASS tamper-selftest rejected={result['rejected']}/{result['mutations']}",
            file=stream,
        )
    if emit_json:
        sys.stdout.write(canonical_json(expected) + "\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
