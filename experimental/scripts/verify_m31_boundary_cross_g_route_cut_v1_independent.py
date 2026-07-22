#!/usr/bin/env python3
"""Independent exact arithmetic replay for the M31 boundary cross-G cut.

This stdlib-only verifier imports no code from the primary verifier.  It
recomputes the integer thresholds used by the boundary-anchor route-cut
packet:

* the fixed-G auxiliary Johnson intervals and uniform excess thresholds;
* the whole-list Johnson deep-excess cap and residual mass;
* the split-support second-moment sign gate and feasible mu interval;
* the Wronskian overlap thresholds;
* the base-field scalarization dimension arithmetic;
* the Chebyshev support-only countermodel inequalities; and
* the K-subset (Singleton packing) threshold.

The script certifies arithmetic consequences of the stated combinatorial and
linear-algebra lemmas.  It does not prove the common-V cross-G coefficient
incidence theorem and does not move the v4 LIST ledger.
"""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from itertools import combinations
from typing import Any, Callable


class CheckFailure(RuntimeError):
    """Raised when an exact verifier gate fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


PARAMETERS = {
    "n": 2_097_152,
    "K": 1_048_576,
    "a": 1_116_023,
    "R": 981_129,
    "w": 67_447,
    "B": 16_777_215,
}


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def fixed_g_denominator(m: int, s: int, *, R: int, w: int) -> int:
    return (m + s) ** 2 - R * (m - w - 1)


def fixed_g_cap(m: int, s: int, *, R: int, w: int) -> int | None:
    denominator = fixed_g_denominator(m, s, R=R, w=w)
    if denominator <= 0:
        return None
    return R * (w + s + 1) // denominator


def minimum_fixed_g_denominator(
    s: int, *, R: int, w: int
) -> tuple[int, int]:
    """Return the legal minimum, where w+1 <= m <= R-s."""

    lower, upper = w + 1, R - s
    require(lower <= upper, "nonempty legal fixed-G range")
    # The real vertex is (R-2s)/2; an integer minimum occurs at an adjacent
    # integer or at a clamped endpoint.
    vertex_floor = (R - 2 * s) // 2
    candidates = {
        lower,
        upper,
        max(lower, min(upper, vertex_floor)),
        max(lower, min(upper, vertex_floor + 1)),
    }
    return min(
        (fixed_g_denominator(m, s, R=R, w=w), m) for m in candidates
    )


def append_truth_interval(
    intervals: list[list[int]], active_start: int | None, point: int, truth: bool
) -> int | None:
    if truth and active_start is None:
        return point
    if not truth and active_start is not None:
        intervals.append([active_start, point - 1])
        return None
    return active_start


def fixed_g_s0_scan(*, R: int, w: int) -> dict[str, Any]:
    interval_sets: dict[str, list[list[int]]] = {
        "positive": [],
        "cap_at_most_3730": [],
        "cap_at_most_46": [],
    }
    starts: dict[str, int | None] = {key: None for key in interval_sets}
    boundary_points = {
        67_448,
        71_176,
        71_177,
        72_837,
        72_838,
        72_858,
        72_859,
        908_270,
        908_271,
        908_291,
        908_292,
        909_952,
        909_953,
        913_681,
        913_682,
        981_129,
    }
    boundary: dict[str, dict[str, int | None]] = {}

    for m in range(w + 1, R + 1):
        denominator = fixed_g_denominator(m, 0, R=R, w=w)
        cap = R * (w + 1) // denominator if denominator > 0 else None
        truths = {
            "positive": denominator > 0,
            "cap_at_most_3730": cap is not None and cap <= 3_730,
            "cap_at_most_46": cap is not None and cap <= 46,
        }
        for key, truth in truths.items():
            starts[key] = append_truth_interval(
                interval_sets[key], starts[key], m, truth
            )
        if m in boundary_points:
            boundary[str(m)] = {"denominator": denominator, "cap": cap}

    for key, start in starts.items():
        if start is not None:
            interval_sets[key].append([start, R])
    return {"intervals": interval_sets, "boundary_values": boundary}


def uniform_s_scan(*, R: int, w: int) -> dict[str, Any]:
    first_positive: int | None = None
    first_data: dict[str, int] | None = None
    last_bad = {3_730: -1, 46: -1}
    predecessor_caps: dict[int, int | None] = {}

    # At s=R-w no legal m remains, so the last nonempty stratum is R-w-1.
    for s in range(0, R - w):
        minimum, argmin = minimum_fixed_g_denominator(s, R=R, w=w)
        cap = R * (w + s + 1) // minimum if minimum > 0 else None
        if minimum > 0 and first_positive is None:
            first_positive = s
            first_data = {
                "s": s,
                "minimum_denominator": minimum,
                "least_argmin_m": argmin,
                "maximum_cap": cap,
            }
        for target in last_bad:
            if cap is None or cap > target:
                last_bad[target] = s

    require(first_positive is not None and first_data is not None, "uniform positivity")
    thresholds: dict[str, dict[str, int | None]] = {}
    for target, bad in last_bad.items():
        threshold = bad + 1
        minimum, argmin = minimum_fixed_g_denominator(threshold, R=R, w=w)
        cap = R * (w + threshold + 1) // minimum
        previous_minimum, _ = minimum_fixed_g_denominator(
            threshold - 1, R=R, w=w
        )
        previous_cap = (
            R * (w + threshold) // previous_minimum
            if previous_minimum > 0
            else None
        )
        predecessor_caps[target] = previous_cap
        thresholds[str(target)] = {
            "first_uniform_s": threshold,
            "minimum_denominator": minimum,
            "least_argmin_m": argmin,
            "maximum_cap": cap,
            "predecessor_cap": previous_cap,
        }
    return {
        "first_all_denominators_positive": first_data,
        "cap_thresholds": thresholds,
    }


def whole_list_denominator(s: int, *, n: int, K: int, a: int) -> int:
    return (a + s) ** 2 - n * (K - 1)


def whole_list_summary(*, n: int, K: int, a: int, w: int, B: int) -> dict[str, Any]:
    lower, upper = 0, n - a
    require(whole_list_denominator(upper, n=n, K=K, a=a) > 0, "whole-list positive endpoint")
    while lower < upper:
        middle = (lower + upper) // 2
        if whole_list_denominator(middle, n=n, K=K, a=a) > 0:
            upper = middle
        else:
            lower = middle + 1
    threshold = lower
    denominator = whole_list_denominator(threshold, n=n, K=K, a=a)
    predecessor = whole_list_denominator(threshold - 1, n=n, K=K, a=a)
    numerator = n * (w + threshold + 1)
    cap = numerator // denominator
    substituted_baseline = cap + 45 * threshold
    parent_baseline = 3_730 + 45 * 366_969
    return {
        "first_positive_s": threshold,
        "predecessor_denominator": predecessor,
        "denominator": denominator,
        "numerator": numerator,
        "deep_cap": cap,
        "shallow_residual": B - cap,
        "rank46_cutoff_substitution": {
            "bankable_replacement": substituted_baseline <= B,
            "high_weight_count": threshold,
            "parent_baseline": parent_baseline,
            "substituted_baseline": substituted_baseline,
            "substituted_baseline_exceeds_budget_by": substituted_baseline - B,
        },
    }


def moment_F(
    sigma: int, *, n: int, a: int, R: int, w: int, L: int
) -> int:
    return L * (sigma * sigma + 2 * a * sigma - a * R + n * (w + 1)) - n * (
        sigma + w + 1
    )


def moment_q(
    mu: Fraction | int,
    sigma: int,
    *,
    a: int,
    R: int,
    w: int,
    L: int,
) -> Fraction:
    mu = Fraction(mu)
    return (
        L
        * (
            R * mu * mu
            + a * (mu + sigma) * (mu + sigma)
            - 2 * a * R * mu
            + a * R * (w + 1)
        )
        - a * R * (sigma + w + 1)
    )


def first_integer_nonpositive(
    left: int, right: int, predicate: Callable[[int], bool]
) -> int:
    require(left < right and not predicate(left) and predicate(right), "left root bracket")
    while left + 1 < right:
        middle = (left + right) // 2
        if predicate(middle):
            right = middle
        else:
            left = middle
    return right


def last_integer_nonpositive(
    left: int, right: int, predicate: Callable[[int], bool]
) -> int:
    require(left < right and predicate(left) and not predicate(right), "right root bracket")
    while left + 1 < right:
        middle = (left + right) // 2
        if predicate(middle):
            left = middle
        else:
            right = middle
    return left


def rational_root_brackets(
    sigma: int,
    integer_interval: tuple[int, int],
    *,
    a: int,
    R: int,
    w: int,
    L: int,
    scale: int = 1_000_000,
) -> dict[str, list[str]]:
    first, last = integer_interval

    def nonpositive_scaled(value: int) -> bool:
        return moment_q(
            Fraction(value, scale), sigma, a=a, R=R, w=w, L=L
        ) <= 0

    lower_left, lower_right = (first - 1) * scale, first * scale
    lower_hit = first_integer_nonpositive(
        lower_left, lower_right, nonpositive_scaled
    )
    upper_left, upper_right = last * scale, (last + 1) * scale
    upper_hit = last_integer_nonpositive(
        upper_left, upper_right, nonpositive_scaled
    )
    return {
        "lower_root": [
            fraction_text(Fraction(lower_hit - 1, scale)),
            fraction_text(Fraction(lower_hit, scale)),
        ],
        "upper_root": [
            fraction_text(Fraction(upper_hit, scale)),
            fraction_text(Fraction(upper_hit + 1, scale)),
        ],
    }


def moment_summary(*, n: int, a: int, R: int, w: int, B: int) -> dict[str, Any]:
    shallow, deep = 366_886, 366_887
    values = {
        str(sigma): moment_F(sigma, n=n, a=a, R=R, w=w, L=B)
        for sigma in (shallow, deep)
    }
    minimizer = Fraction(a * (R - shallow), n)
    center = minimizer.numerator // minimizer.denominator
    predicate = lambda mu: moment_q(mu, shallow, a=a, R=R, w=w, L=B) <= 0
    first = first_integer_nonpositive(w + 1, center, predicate)
    last = last_integer_nonpositive(center, R, predicate)
    interval = (first, last)
    brackets = rational_root_brackets(
        shallow, interval, a=a, R=R, w=w, L=B
    )
    q_at_minimizer = moment_q(
        minimizer, shallow, a=a, R=R, w=w, L=B
    )
    proportional = Fraction(a * R, n) * values[str(shallow)]
    require(q_at_minimizer == proportional, "moment F proportionality")
    return {
        "F_values": values,
        "sign_gate": values[str(shallow)] < 0 < values[str(deep)],
        "shallow_sigma": shallow,
        "first_infeasible_sigma": deep,
        "mu_minimizer": fraction_text(minimizer),
        "integer_feasible_mu_interval": [first, last],
        "integer_boundary_q_values": {
            str(first - 1): int(
                moment_q(first - 1, shallow, a=a, R=R, w=w, L=B)
            ),
            str(first): int(moment_q(first, shallow, a=a, R=R, w=w, L=B)),
            str(last): int(moment_q(last, shallow, a=a, R=R, w=w, L=B)),
            str(last + 1): int(
                moment_q(last + 1, shallow, a=a, R=R, w=w, L=B)
            ),
        },
        "rational_root_brackets_width_at_most": "1/1000000",
        "rational_root_brackets": brackets,
    }


def wronskian_summary(*, a: int, R: int, w: int) -> dict[str, Any]:
    threshold = R - w
    lower_x, upper_x = 2 * (w + 1), 2 * R

    def forced_minus_allowed(x: int) -> int:
        forced = max(0, x - a) + max(0, x - R)
        allowed = x - w - 1
        return forced - allowed

    candidates = {
        lower_x,
        upper_x,
        *(
            point
            for breakpoint in (R, a)
            for point in (breakpoint - 1, breakpoint, breakpoint + 1)
            if lower_x <= point <= upper_x
        ),
    }
    maximum, argmax = max((forced_minus_allowed(x), x) for x in candidates)
    return {
        "H_overlap_only_excess_sum_threshold": threshold,
        "fixed_G_direct_overlap_degree_threshold": threshold,
        "s0_combined_forced_overlap_max_minus_wronskian_allowance": maximum,
        "s0_combined_forced_overlap_argmax_degree_sum": argmax,
        "s0_support_overlap_alone_contradicts": maximum > 0,
    }


def base_field_summary(*, R: int, w: int, B: int) -> dict[str, Any]:
    d_min, d_max = 1, R - w
    p = 2**31 - 1
    forbidden = B + 1
    n4 = 1 + p + p**2 + p**3
    h4 = 1 + p + p**2
    left = forbidden * R * h4
    right = (w + 1) * n4
    return {
        "d_range": [d_min, d_max],
        "dimension_upper_bound_formula": "dim_Fp <= d",
        "V_equals_1_dimension_formula": "dim_Fp = d",
        "ambient_dimension_formula": "4d",
        "true_V_equals_1_codimension_formula": "3d",
        "fake_3m_independence_deficit": 3 * w,
        "conclusion": "NO_UNIFORM_P_MINUS_3M_GAIN_FROM_THE_BASE_FIELD_GATE",
        "live_counterexample_reduction": {
            "N4": n4,
            "H4": h4,
            "left": left,
            "right": right,
            "strict_margin": right - left,
            "strict_scalar_descent_gate": left < right,
            "fresh_symbol_gate": forbidden < p,
            "quartic_violation_implies_base_boundary_violation": left < right and forbidden < p,
            "projected_V_and_b_are_base_field": True,
            "scalar_descent_is_ledger_payment": False,
        },
    }


def chebyshev_summary(*, n: int, K: int, a: int, R: int, w: int, B: int) -> dict[str, Any]:
    require(n == 2 * K, "two-point fiber decomposition")
    require(R == K - w and a == K + w, "Chebyshev support cardinalities")
    volume_base = 44
    dyadic_base = 64
    # With x=1/16, x^w*Vol(R,w) <= (1+x)^R.  The following
    # integer comparison is therefore an exact proof that Vol(R,w)<44^w.
    rational_volume_gate = pow(17, R) < pow(volume_base, w) * pow(16, R - w)
    greedy_exponent = R - 6 * w
    shell_exponent = greedy_exponent - 20
    return {
        "T2_fibers": K,
        "T4_fibers": K // 2,
        "fixed_full_T2_fibers": w,
        "binary_coordinates": R,
        "support_size": 2 * w + R,
        "no_full_T4_capacity_gate": w <= K // 2,
        "integer_e_bound": {
            "three_R": 3 * R,
            "forty_four_w": volume_base * w,
            "strict": 3 * R < volume_base * w,
        },
        "rational_volume_witness": "x=1/16",
        "rational_volume_integer_gate": "17^R<44^w*16^(R-w)",
        "rational_volume_gate": rational_volume_gate,
        "volume_chain": "Vol(R,w)<44^w<64^w=2^(6w)",
        "volume_base_gate": volume_base < dyadic_base,
        "greedy_code_size_strictly_exceeds_power_of_two_exponent": greedy_exponent,
        "R_below_power_of_two_exponent": 20,
        "R_below_power_gate": R < 2**20,
        "fixed_weight_shell_strictly_exceeds_power_of_two_exponent": shell_exponent,
        "budget_below_power_of_two_exponent": 24,
        "fixed_weight_shell_exceeds_budget": shell_exponent > 24 and B < 2**24,
        "minimum_binary_distance": w + 1,
        "route_cut": "SUPPORT_MDS_AND_T2_T4_COUNTS_ALONE_CANNOT_CLOSE_BOUNDARY_CENSUS",
    }


def k_subset_ratio_floor(n: int, K: int, errors: int) -> int:
    require(0 <= errors <= n - K, "K-subset ratio range")
    ratio = Fraction(1)
    for index in range(errors):
        ratio *= Fraction(n - index, n - K - index)
    return ratio.numerator // ratio.denominator


def singleton_summary(*, n: int, K: int, w: int, B: int) -> dict[str, Any]:
    floors = {str(errors): k_subset_ratio_floor(n, K, errors) for errors in (23, 24)}
    first_failure = next(
        errors for errors in range(0, 25) if k_subset_ratio_floor(n, K, errors) > B
    )
    return {
        "ratio_formula": "floor(binomial(n,K)/binomial(n-errors,K))",
        "ratio_floors": floors,
        "last_budget_fitting_errors": first_failure - 1,
        "first_nonfitting_errors": first_failure,
        "last_budget_fitting_agreement": n - (first_failure - 1),
        "first_nonfitting_agreement": n - first_failure,
        "maximum_nonanchor_agreement": n - (w + 1),
        "minimum_nonanchor_error_count": w + 1,
        "budget_fitting_transition_reachable_by_nonanchor": w + 1 <= first_failure - 1,
    }


def v1_summary(*, w: int, B: int) -> dict[str, Any]:
    residues = list(range(7))
    fibre_sizes: dict[str, int] = {str(value): 0 for value in residues}
    for support in combinations(range(6), 3):
        key = str((-sum(support)) % 7)
        fibre_sizes[key] += 1

    received = (0, 0, 0, 1, 5, 4)
    rows: list[dict[str, Any]] = []
    for a0 in residues:
        for a1 in residues:
            support = tuple(
                x for x in range(6) if (a0 + a1 * x) % 7 == received[x]
            )
            if len(support) >= 3:
                rows.append({"coefficients": [a0, a1], "support": list(support)})

    def evaluate(poly: tuple[int, ...], x: int) -> int:
        return sum(coefficient * pow(x, degree, 7)
                   for degree, coefficient in enumerate(poly)) % 7

    h0 = (6, 5, 3)
    unit = (1, 3, 5)
    error_points = (3, 4, 5)
    h_values = [evaluate(h0, x) for x in error_points]
    v_values = [evaluate(unit, x) for x in error_points]
    source_list_floor = 6_796_405
    source_companion_floor = source_list_floor - 1
    target = B - 1
    return {
        "prefix_identity": "#X_S(1)=N_w(prefix_w(L_S))-1",
        "newton_gate": (2**31 - 1) > w,
        "source_list_floor": source_list_floor,
        "source_companion_floor": source_companion_floor,
        "companion_target": target,
        "source_headroom": target - source_companion_floor,
        "source_floor_uniform": False,
        "F7_control": {
            "prefix_fibre_sizes": fibre_sizes,
            "maximum_prefix_fibre": max(fibre_sizes.values()),
            "maximum_V1_companions": max(fibre_sizes.values()) - 1,
            "boundary_list": rows,
            "boundary_list_size": len(rows),
            "arbitrary_V_companions": len(rows) - 1,
            "H0_values": h_values,
            "V_values": v_values,
            "inverse_gate": all((left * right) % 7 == 1
                                for left, right in zip(h_values, v_values)),
            "arbitrary_V_strictly_beats_global_V1":
                len(rows) - 1 > max(fibre_sizes.values()) - 1,
        },
        "general_V1_reduction": False,
        "ledger_payment": False,
    }


def build_summary() -> dict[str, Any]:
    p = PARAMETERS
    require(p["R"] == p["n"] - p["a"], "radius identity")
    require(p["w"] == p["a"] - p["K"], "agreement shift identity")
    require(p["B"] == 2**24 - 1, "M31 budget identity")
    return {
        "schema": "m31-boundary-cross-g-route-cut-independent-summary-v1",
        "parameters": dict(p),
        "fixed_G": {
            "s0": fixed_g_s0_scan(R=p["R"], w=p["w"]),
            "uniform_s": uniform_s_scan(R=p["R"], w=p["w"]),
            "direct_overlap_threshold": p["R"] - p["w"],
        },
        "whole_list_Johnson": whole_list_summary(
            n=p["n"], K=p["K"], a=p["a"], w=p["w"], B=p["B"]
        ),
        "split_support_moment": moment_summary(
            n=p["n"], a=p["a"], R=p["R"], w=p["w"], B=p["B"]
        ),
        "Wronskian": wronskian_summary(a=p["a"], R=p["R"], w=p["w"]),
        "base_field_scalarization": base_field_summary(R=p["R"], w=p["w"], B=p["B"]),
        "V_equals_1_route_cut": v1_summary(w=p["w"], B=p["B"]),
        "Chebyshev_support_countermodel": chebyshev_summary(**p),
        "Singleton_K_subset": singleton_summary(
            n=p["n"], K=p["K"], w=p["w"], B=p["B"]
        ),
        "ledger_movement": 0,
        "row_closed": False,
        "remaining_terminal": "UNPAID_BOUNDARY_COMMON_V_FULL_LOCATOR_COEFFICIENT_INCIDENCE",
    }


def validate_summary(summary: dict[str, Any]) -> None:
    require(summary["schema"] == "m31-boundary-cross-g-route-cut-independent-summary-v1", "schema")
    require(summary["parameters"] == PARAMETERS, "parameters")

    fixed = summary["fixed_G"]
    intervals = fixed["s0"]["intervals"]
    require(intervals["positive"] == [[67_448, 72_858], [908_271, 981_129]], "fixed-G positivity intervals")
    require(intervals["cap_at_most_3730"] == [[67_448, 72_837], [908_292, 981_129]], "fixed-G 3730 intervals")
    require(intervals["cap_at_most_46"] == [[67_448, 71_176], [909_953, 981_129]], "fixed-G 46 intervals")
    require(fixed["direct_overlap_threshold"] == 913_682, "fixed-G direct overlap")
    boundary = fixed["s0"]["boundary_values"]
    require(boundary["72858"] == {"denominator": 380_274, "cap": 174_019}, "positive left inner endpoint")
    require(boundary["72859"] == {"denominator": -455_138, "cap": None}, "nonpositive gap endpoint")
    require(boundary["908270"] == {"denominator": -455_138, "cap": None}, "nonpositive symmetric gap")
    require(boundary["908271"] == {"denominator": 380_274, "cap": 174_019}, "positive right inner endpoint")
    require(boundary["72837"]["cap"] == 3_691 and boundary["72838"]["cap"] == 3_872, "3730 transition")
    require(boundary["71176"]["cap"] == 46 and boundary["71177"]["cap"] == 47, "46 transition")

    uniform = fixed["uniform_s"]
    require(
        uniform["first_all_denominators_positive"]
        == {
            "s": 177_835,
            "minimum_denominator": 735_847,
            "least_argmin_m": 312_729,
            "maximum_cap": 327_043,
        },
        "uniform positivity threshold",
    )
    require(
        uniform["cap_thresholds"]["3730"]
        == {
            "first_uniform_s": 177_901,
            "minimum_denominator": 65_490_361,
            "least_argmin_m": 312_663,
            "maximum_cap": 3_675,
            "predecessor_cap": 3_731,
        },
        "uniform 3730 threshold",
    )
    require(
        uniform["cap_thresholds"]["46"]
        == {
            "first_uniform_s": 183_167,
            "minimum_denominator": 5_232_115_675,
            "least_argmin_m": 307_397,
            "maximum_cap": 46,
            "predecessor_cap": 47,
        },
        "uniform 46 threshold",
    )

    whole = summary["whole_list_Johnson"]
    require(whole == {
        "first_positive_s": 366_887,
        "predecessor_denominator": -2_056_119,
        "denominator": 909_700,
        "numerator": 910_866_513_920,
        "deep_cap": 1_001_282,
        "shallow_residual": 15_775_933,
        "rank46_cutoff_substitution": {
            "bankable_replacement": False,
            "high_weight_count": 366_887,
            "parent_baseline": 16_517_335,
            "substituted_baseline": 17_511_197,
            "substituted_baseline_exceeds_budget_by": 733_982,
        },
    }, "whole-list Johnson threshold")

    moment = summary["split_support_moment"]
    require(moment["F_values"] == {
        "366886": -35_406_814_945_353,
        "366887": 14_351_365_971_580,
    }, "moment F endpoint values")
    require(moment["sign_gate"] is True, "moment sign gate")
    require(moment["mu_minimizer"] == "685509315589/2097152", "moment exact minimizer")
    require(moment["integer_feasible_mu_interval"] == [326_152, 327_601], "moment feasible integer interval")
    q_values = moment["integer_boundary_q_values"]
    require(q_values == {
        "326151": 23_241_237_726_638_592,
        "326152": -27_763_007_869_531_638,
        "327601": -8_794_305_700_930_908,
        "327602": 42_236_121_678_770_862,
    }, "moment integer root brackets")
    require(moment["rational_root_brackets_width_at_most"] == "1/1000000", "rational bracket width")
    lower_left, lower_right = map(
        Fraction, moment["rational_root_brackets"]["lower_root"]
    )
    upper_left, upper_right = map(
        Fraction, moment["rational_root_brackets"]["upper_root"]
    )
    require(
        lower_right - lower_left <= Fraction(1, 1_000_000)
        and upper_right - upper_left <= Fraction(1, 1_000_000),
        "rational bracket exact width",
    )
    require(
        moment_q(
            lower_left,
            366_886,
            a=PARAMETERS["a"],
            R=PARAMETERS["R"],
            w=PARAMETERS["w"],
            L=PARAMETERS["B"],
        )
        > 0
        >= moment_q(
            lower_right,
            366_886,
            a=PARAMETERS["a"],
            R=PARAMETERS["R"],
            w=PARAMETERS["w"],
            L=PARAMETERS["B"],
        ),
        "lower rational root sign bracket",
    )
    require(
        moment_q(
            upper_left,
            366_886,
            a=PARAMETERS["a"],
            R=PARAMETERS["R"],
            w=PARAMETERS["w"],
            L=PARAMETERS["B"],
        )
        <= 0
        < moment_q(
            upper_right,
            366_886,
            a=PARAMETERS["a"],
            R=PARAMETERS["R"],
            w=PARAMETERS["w"],
            L=PARAMETERS["B"],
        ),
        "upper rational root sign bracket",
    )

    wronskian = summary["Wronskian"]
    require(wronskian == {
        "H_overlap_only_excess_sum_threshold": 913_682,
        "fixed_G_direct_overlap_degree_threshold": 913_682,
        "s0_combined_forced_overlap_max_minus_wronskian_allowance": -67_446,
        "s0_combined_forced_overlap_argmax_degree_sum": 1_962_258,
        "s0_support_overlap_alone_contradicts": False,
    }, "Wronskian thresholds")

    base = summary["base_field_scalarization"]
    require(base["d_range"] == [1, 913_682], "base-field d range")
    require(base["dimension_upper_bound_formula"] == "dim_Fp <= d", "base-field dimension ceiling")
    require(base["V_equals_1_dimension_formula"] == "dim_Fp = d", "base-field sharp control")
    require(base["ambient_dimension_formula"] == "4d", "base-field ambient dimension")
    require(base["true_V_equals_1_codimension_formula"] == "3d", "base-field true codimension")
    require(base["fake_3m_independence_deficit"] == 202_341, "base-field dependency deficit")
    require(base["conclusion"] == "NO_UNIFORM_P_MINUS_3M_GAIN_FROM_THE_BASE_FIELD_GATE", "base-field route cut")
    descent = base["live_counterexample_reduction"]
    require(descent == {
        "N4": 9_903_520_305_059_670_166_633_185_280,
        "H4": 4_611_686_016_279_904_257,
        "left": 75_911_179_514_902_718_909_260_442_370_048,
        "right": 667_972_637_535_664_633_399_075_080_765_440,
        "strict_margin": 592_061_458_020_761_914_489_814_638_395_392,
        "strict_scalar_descent_gate": True,
        "fresh_symbol_gate": True,
        "quartic_violation_implies_base_boundary_violation": True,
        "projected_V_and_b_are_base_field": True,
        "scalar_descent_is_ledger_payment": False,
    }, "scalar-descent boundary composition")

    v1 = summary["V_equals_1_route_cut"]
    require(v1["prefix_identity"] == "#X_S(1)=N_w(prefix_w(L_S))-1",
            "V=1 prefix identity")
    require(v1["newton_gate"] is True, "V=1 Newton gate")
    require(v1["source_list_floor"] == 6_796_405, "V=1 source list floor")
    require(v1["source_companion_floor"] == 6_796_404,
            "V=1 source companion floor")
    require(v1["companion_target"] == 16_777_214, "V=1 companion target")
    require(v1["source_headroom"] == 9_980_810, "V=1 source headroom")
    require(v1["source_floor_uniform"] is False, "V=1 nonuniform source guard")
    f7 = v1["F7_control"]
    require(f7["prefix_fibre_sizes"] == {
        "0": 3, "1": 3, "2": 3, "3": 2, "4": 3, "5": 3, "6": 3,
    }, "F7 prefix fibre sizes")
    require(f7["maximum_V1_companions"] == 2, "F7 V=1 maximum")
    require(f7["boundary_list_size"] == 4, "F7 list size")
    require(f7["arbitrary_V_companions"] == 3, "F7 arbitrary-V companions")
    require(f7["H0_values"] == [6, 4, 1], "F7 H0 values")
    require(f7["V_values"] == [6, 2, 1], "F7 V values")
    require(f7["inverse_gate"] is True, "F7 inverse gate")
    require(f7["arbitrary_V_strictly_beats_global_V1"] is True,
            "F7 arbitrary V beats global V=1")
    require(v1["general_V1_reduction"] is False, "general V=1 reduction guard")
    require(v1["ledger_payment"] is False, "V=1 zero-payment guard")

    chebyshev = summary["Chebyshev_support_countermodel"]
    require(chebyshev["support_size"] == PARAMETERS["a"], "Chebyshev support size")
    require(chebyshev["no_full_T4_capacity_gate"] is True, "Chebyshev T4 capacity")
    require(chebyshev["integer_e_bound"] == {
        "three_R": 2_943_387,
        "forty_four_w": 2_967_668,
        "strict": True,
    }, "Chebyshev e-bound arithmetic")
    require(chebyshev["rational_volume_witness"] == "x=1/16", "Chebyshev rational witness")
    require(chebyshev["rational_volume_integer_gate"] == "17^R<44^w*16^(R-w)", "Chebyshev exact volume formula")
    require(chebyshev["rational_volume_gate"] is True, "Chebyshev exact volume inequality")
    require(chebyshev["volume_base_gate"] is True, "Chebyshev volume base")
    require(chebyshev["volume_chain"] == "Vol(R,w)<44^w<64^w=2^(6w)", "Chebyshev volume chain")
    require(chebyshev["greedy_code_size_strictly_exceeds_power_of_two_exponent"] == 576_447, "Chebyshev greedy exponent")
    require(chebyshev["fixed_weight_shell_strictly_exceeds_power_of_two_exponent"] == 576_427, "Chebyshev shell exponent")
    require(chebyshev["R_below_power_gate"] is True, "Chebyshev shell pigeonhole denominator")
    require(chebyshev["fixed_weight_shell_exceeds_budget"] is True, "Chebyshev fixed shell exceeds budget")
    require(chebyshev["minimum_binary_distance"] == 67_448, "Chebyshev minimum distance")

    singleton = summary["Singleton_K_subset"]
    require(singleton["ratio_formula"] == "floor(binomial(n,K)/binomial(n-errors,K))", "Singleton formula")
    require(singleton["ratio_floors"] == {"23": 8_389_620, "24": 16_779_424}, "Singleton floors")
    require(singleton["last_budget_fitting_errors"] == 23, "Singleton last fit")
    require(singleton["first_nonfitting_errors"] == 24, "Singleton first miss")
    require(singleton["last_budget_fitting_agreement"] == 2_097_129, "Singleton n-23")
    require(singleton["first_nonfitting_agreement"] == 2_097_128, "Singleton n-24")
    require(singleton["maximum_nonanchor_agreement"] == 2_029_704, "maximum nonanchor agreement")
    require(singleton["budget_fitting_transition_reachable_by_nonanchor"] is False, "Singleton route cut")

    require(summary["ledger_movement"] == 0, "zero ledger movement")
    require(summary["row_closed"] is False, "row remains open")
    require(summary["remaining_terminal"] == "UNPAID_BOUNDARY_COMMON_V_FULL_LOCATOR_COEFFICIENT_INCIDENCE", "remaining terminal")


def set_path(value: dict[str, Any], path: tuple[str, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def run_mutations(summary: dict[str, Any]) -> list[str]:
    mutations: list[tuple[str, tuple[str, ...], Any]] = [
        ("n", ("parameters", "n"), PARAMETERS["n"] + 1),
        ("positive_interval", ("fixed_G", "s0", "intervals", "positive"), [[67_448, 72_859], [908_271, 981_129]]),
        ("fixed_3730_endpoint", ("fixed_G", "s0", "intervals", "cap_at_most_3730"), [[67_448, 72_838], [908_292, 981_129]]),
        ("fixed_46_endpoint", ("fixed_G", "s0", "intervals", "cap_at_most_46"), [[67_448, 71_177], [909_953, 981_129]]),
        ("fixed_overlap", ("fixed_G", "direct_overlap_threshold"), 913_681),
        ("uniform_positive", ("fixed_G", "uniform_s", "first_all_denominators_positive", "s"), 177_834),
        ("uniform_positive_cap", ("fixed_G", "uniform_s", "first_all_denominators_positive", "maximum_cap"), 327_044),
        ("uniform_3730", ("fixed_G", "uniform_s", "cap_thresholds", "3730", "first_uniform_s"), 177_900),
        ("uniform_3730_predecessor", ("fixed_G", "uniform_s", "cap_thresholds", "3730", "predecessor_cap"), 3_730),
        ("uniform_46", ("fixed_G", "uniform_s", "cap_thresholds", "46", "first_uniform_s"), 183_166),
        ("whole_threshold", ("whole_list_Johnson", "first_positive_s"), 366_886),
        ("whole_cap", ("whole_list_Johnson", "deep_cap"), 1_001_281),
        ("shallow_mass", ("whole_list_Johnson", "shallow_residual"), 15_775_932),
        ("false_rank46_cutoff_payment", ("whole_list_Johnson", "rank46_cutoff_substitution", "bankable_replacement"), True),
        ("moment_left_sign", ("split_support_moment", "F_values", "366886"), 1),
        ("moment_right_sign", ("split_support_moment", "F_values", "366887"), -1),
        ("moment_gate", ("split_support_moment", "sign_gate"), False),
        ("moment_mu_left", ("split_support_moment", "integer_feasible_mu_interval"), [326_151, 327_601]),
        ("moment_rational_lower", ("split_support_moment", "rational_root_brackets", "lower_root"), ["326151/1", "326152/1"]),
        ("wronskian_threshold", ("Wronskian", "H_overlap_only_excess_sum_threshold"), 913_681),
        ("wronskian_false_closure", ("Wronskian", "s0_support_overlap_alone_contradicts"), True),
        ("base_dimension_deficit", ("base_field_scalarization", "fake_3m_independence_deficit"), 202_340),
        ("base_dimension_formula", ("base_field_scalarization", "dimension_upper_bound_formula"), "dim_Fp <= 3d"),
        ("scalar_descent_margin", ("base_field_scalarization", "live_counterexample_reduction", "strict_margin"), 1),
        ("scalar_descent_collision", ("base_field_scalarization", "live_counterexample_reduction", "quartic_violation_implies_base_boundary_violation"), False),
        ("V1_source_floor", ("V_equals_1_route_cut", "source_companion_floor"), 6_796_403),
        ("V1_toy_list", ("V_equals_1_route_cut", "F7_control", "boundary_list_size"), 3),
        ("V1_toy_extremality", ("V_equals_1_route_cut", "F7_control", "arbitrary_V_strictly_beats_global_V1"), False),
        ("V1_false_reduction", ("V_equals_1_route_cut", "general_V1_reduction"), True),
        ("chebyshev_e_gate", ("Chebyshev_support_countermodel", "integer_e_bound", "strict"), False),
        ("chebyshev_exact_volume", ("Chebyshev_support_countermodel", "rational_volume_gate"), False),
        ("chebyshev_greedy_exponent", ("Chebyshev_support_countermodel", "greedy_code_size_strictly_exceeds_power_of_two_exponent"), 576_446),
        ("chebyshev_pigeonhole", ("Chebyshev_support_countermodel", "R_below_power_gate"), False),
        ("chebyshev_shell", ("Chebyshev_support_countermodel", "fixed_weight_shell_exceeds_budget"), False),
        ("singleton_23", ("Singleton_K_subset", "ratio_floors", "23"), 8_389_621),
        ("singleton_24", ("Singleton_K_subset", "ratio_floors", "24"), 16_777_215),
        ("singleton_reach", ("Singleton_K_subset", "budget_fitting_transition_reachable_by_nonanchor"), True),
        ("ledger_movement", ("ledger_movement",), 1),
        ("false_closure", ("row_closed",), True),
        ("terminal", ("remaining_terminal",), "SAFE"),
    ]
    passed: list[str] = []
    for name, path, replacement in mutations:
        mutated = copy.deepcopy(summary)
        set_path(mutated, path, replacement)
        try:
            validate_summary(mutated)
        except (CheckFailure, KeyError, TypeError, ValueError, ZeroDivisionError):
            passed.append(name)
        else:
            raise CheckFailure(f"mutation survived: {name}")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="run all exact gates and load-bearing mutation tests",
    )
    parser.add_argument(
        "--print-template",
        action="store_true",
        help="print the deterministic independently derived summary",
    )
    args = parser.parse_args()

    summary = build_summary()
    validate_summary(summary)
    if args.print_template:
        output: dict[str, Any] = summary
    else:
        mutations = run_mutations(summary)
        output = {
            "status": "PASS",
            "implementation": "INDEPENDENT_STDLIB_EXACT",
            "mutation_tests_passed": len(mutations),
            "mutation_names": mutations,
            "summary": summary,
        }
    print(json.dumps(output, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


if __name__ == "__main__":
    main()
