#!/usr/bin/env python3
"""Exact arithmetic certificate for the M31 canonical-Popov/rank-46 route cut.

This verifier pins the arithmetic contract and guards the hand-proved compiler
and two sharp route cuts; it does not formalize those polynomial-module
arguments or prove the M31 list bound.  Its deployed arithmetic is stdlib-only
and deterministic.  Every assertion remains active under ``python -O``.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable


P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
SHIFT = AGREEMENT - K
RADIUS = N - AGREEMENT
BUDGET = P**4 // 2**100
FORBIDDEN = BUDGET + 1

WEIGHT_CUTOFF = 614_160
PACKING_SIZE = N - WEIGHT_CUTOFF
PACKING_INTERSECTION = K - 1
PACKING_CAP = 3_730
PACKING_FIRST_EXCLUDED = PACKING_CAP + 1
HIGH_LAYER_COUNT = RADIUS - WEIGHT_CUTOFF
FREE_BASELINE = 45
FORCED_RANK = FREE_BASELINE + 1
FORCED_TAIL = FORBIDDEN - PACKING_CAP - FREE_BASELINE * HIGH_LAYER_COUNT
SAFE_TAIL = FORCED_TAIL - 1

FORNEY_INDEX_COUNT = FORCED_RANK - 1
SMALL_INDEX_COUNT = FORNEY_INDEX_COUNT - 1
SMALL_INDEX_SUM_MAX = 2 * RADIUS - K - 1
CUTOFF_MIN = K - RADIUS

PR1005_HEAD = "568242657e69d9594c621814e12e53e7a9211332"
PR1007_HEAD = "97b7c94fd1822f897910589cf2aa786021f5ee01"
OPTIMIZER_ROWS_SHA256 = "bed6d505904de120e76e7e4b5464b9682756a015dec8c993e4ed4c8d11815763"

ROOT = Path(__file__).resolve().parents[2]
PYTHON_PATH = ROOT / "experimental/scripts/verify_m31_canonical_popov_rank46_compiler.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_canonical_popov_rank46_compiler.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_canonical_popov_rank46_compiler.md"
README_PATH = ROOT / "experimental/data/certificates/m31-canonical-popov-rank46-compiler/README.md"
CERTIFICATE_PATH = ROOT / "experimental/data/certificates/m31-canonical-popov-rank46-compiler/manifest.json"

SOURCE_PATHS = (
    ROOT / "tex/cs25_cap_v13_2.tex",
    ROOT / "experimental/grande_finale.tex",
    ROOT / "experimental/notes/l1/l1_arbitrary_fiber_repair.md",
    ROOT / "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
    ROOT / "experimental/notes/thresholds/split_pencil_ray_collapse.md",
    ROOT / "experimental/notes/thresholds/m31_actual_hyperplane_packet_activation_route_cut.md",
    NOTE_PATH,
    PYTHON_PATH,
    SAGE_PATH,
    README_PATH,
)


class VerificationError(RuntimeError):
    """Raised when an exact gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(payload: Any) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("certificate_sha256", None)
    out["certificate_sha256"] = hashlib.sha256(canonical_json(out)).hexdigest()
    return out


def balanced_pair_lower(member_count: int, set_size: int) -> tuple[int, int, int]:
    """Exact minimum of sum_x binom(r_x,2) for total incidence M*s."""
    quotient, remainder = divmod(member_count * set_size, N)
    lower = N * quotient * (quotient - 1) // 2 + remainder * quotient
    return lower, quotient, remainder


def packing_feasible(member_count: int, set_size: int) -> bool:
    lower, _, _ = balanced_pair_lower(member_count, set_size)
    upper = math.comb(member_count, 2) * PACKING_INTERSECTION
    return lower <= upper


def packing_cutoff_scan() -> tuple[dict[str, Any], dict[int, int]]:
    """Scan every relevant J>=K/2 with positive packing denominator.

    The cap is the first member count rejected by the exact integer inequality,
    minus one.  It is monotone as the chosen agreement subsets shrink, so a
    single moving pointer performs the exhaustive scan.
    """
    start = K // 2
    cap = 1
    caps: dict[int, int] = {}
    digest = hashlib.sha256()
    best: dict[int, tuple[int, int, int]] = {
        baseline: (-10**30, -1, -1) for baseline in range(1, 51)
    }

    last = start - 1
    for cutoff in range(start, RADIUS):
        set_size = N - cutoff
        if set_size * set_size <= N * PACKING_INTERSECTION:
            break
        require(packing_feasible(cap, set_size), "moving packing cap remains feasible")
        while packing_feasible(cap + 1, set_size):
            cap += 1
        require(not packing_feasible(cap + 1, set_size), "first excluded packing size")
        caps[cutoff] = cap
        digest.update(f"{cutoff},{cap}\n".encode())
        last = cutoff
        layers = RADIUS - cutoff
        for baseline in best:
            tail = FORBIDDEN - cap - baseline * layers
            if tail > best[baseline][0]:
                best[baseline] = (tail, cutoff, cap)

    require(last == 614_242, "last positive-denominator cutoff")
    require(caps[last] == 1_001_281, "last packing cap")
    require(caps[WEIGHT_CUTOFF] == PACKING_CAP, "selected packing cap")
    require(best[FREE_BASELINE] == (FORCED_TAIL, WEIGHT_CUTOFF, PACKING_CAP),
            "rank-46 optimum")
    require(best[FREE_BASELINE + 1][0] == -107_088, "rank-47 not forced")

    pareto = []
    for baseline in range(30, 47):
        tail, cutoff, cutoff_cap = best[baseline]
        pareto.append({
            "baseline": baseline,
            "forced_rank": baseline + 1,
            "best_cutoff": cutoff,
            "low_prefix_cap": cutoff_cap,
            "forced_tail_lower": max(0, tail),
            "raw_tail_margin": tail,
        })

    return ({
        "first_cutoff": start,
        "last_cutoff": last,
        "rows_scanned": len(caps),
        "rows_sha256": digest.hexdigest(),
        "last_cap": caps[last],
        "pareto_baselines_30_46": pareto,
        "selected_baseline_is_global_scan_optimum": True,
        "largest_forced_rank": FORCED_RANK,
        "rank_47_forced": False,
    }, caps)


def same_weight_feasible(member_count: int, weight: int) -> bool:
    lower, _, _ = balanced_pair_lower(member_count, weight)
    overlap_cap = 2 * weight - K - 1
    if overlap_cap < 0:
        return member_count <= 1
    return lower <= math.comb(member_count, 2) * overlap_cap


def first_same_weight_feasible(member_count: int) -> int:
    first: int | None = None
    for weight in range(K // 2, RADIUS + 1):
        feasible = same_weight_feasible(member_count, weight)
        if feasible and first is None:
            first = weight
        if first is not None:
            require(feasible, "same-weight feasibility stays monotone after first pass")
    require(first is not None, "same-weight feasibility interval nonempty")
    require(same_weight_feasible(member_count, first), "same-weight boundary feasible")
    require(not same_weight_feasible(member_count, first - 1), "same-weight predecessor fails")
    return first


def selected_packing_gate() -> dict[str, Any]:
    feasible_lower, feasible_q, feasible_r = balanced_pair_lower(PACKING_CAP, PACKING_SIZE)
    feasible_upper = math.comb(PACKING_CAP, 2) * PACKING_INTERSECTION
    fail_lower, fail_q, fail_r = balanced_pair_lower(PACKING_FIRST_EXCLUDED, PACKING_SIZE)
    fail_upper = math.comb(PACKING_FIRST_EXCLUDED, 2) * PACKING_INTERSECTION
    cauchy_cap = N * (PACKING_SIZE - PACKING_INTERSECTION) // (
        PACKING_SIZE * PACKING_SIZE - N * PACKING_INTERSECTION
    )

    require((feasible_q, feasible_r) == (2_637, 1_370_336), "3730 quotient/remainder")
    require(feasible_upper - feasible_lower == 202_311, "3730 feasible margin")
    require((fail_q, fail_r) == (2_638, 756_176), "3731 quotient/remainder")
    require(fail_lower - fail_upper == 19_019, "3731 exclusion margin")
    require(cauchy_cap == 3_732, "plain Cauchy cap")

    return {
        "weight_cutoff": WEIGHT_CUTOFF,
        "chosen_agreement_subset_size": PACKING_SIZE,
        "pair_intersection_upper": PACKING_INTERSECTION,
        "certified_low_prefix_cap": PACKING_CAP,
        "cap_feasible_relaxation": {
            "members": PACKING_CAP,
            "quotient": feasible_q,
            "remainder": feasible_r,
            "balanced_lower": feasible_lower,
            "pair_upper": feasible_upper,
            "margin": feasible_upper - feasible_lower,
        },
        "first_excluded": {
            "members": PACKING_FIRST_EXCLUDED,
            "quotient": fail_q,
            "remainder": fail_r,
            "balanced_lower": fail_lower,
            "pair_upper": fail_upper,
            "contradiction_margin": fail_lower - fail_upper,
        },
        "plain_cauchy_cap": cauchy_cap,
        "integer_rounding_is_load_bearing": True,
        "variable_error_weights_are_allowed": True,
        "codeword_to_chosen_subset_injective": True,
    }


def occupancy_compiler(caps: dict[int, int]) -> dict[str, Any]:
    base_mass = PACKING_CAP + FREE_BASELINE * HIGH_LAYER_COUNT
    require(base_mass == 16_517_335, "rank-46 occupancy base")
    require(BUDGET - base_mass == SAFE_TAIL, "rank-46 safety threshold")
    require(FORCED_TAIL == 259_881, "rank-46 forbidden tail")

    extra_start = RADIUS - FORCED_TAIL + 1
    require(extra_start == 721_249, "extremizer extra interval")
    total = PACKING_CAP + FREE_BASELINE * HIGH_LAYER_COUNT + FORCED_TAIL
    require(total == FORBIDDEN, "arithmetic extremizer total")

    minimum_prefix_slack: int | None = None
    for cutoff, cap in caps.items():
        if cutoff < WEIGHT_CUTOFF:
            cumulative = 0
        else:
            cumulative = (
                PACKING_CAP
                + FREE_BASELINE * (cutoff - WEIGHT_CUTOFF)
                + max(0, cutoff - extra_start + 1)
            )
        require(cumulative <= cap, "arithmetic extremizer respects every prefix cap")
        slack = cap - cumulative
        minimum_prefix_slack = slack if minimum_prefix_slack is None else min(minimum_prefix_slack, slack)
    require(minimum_prefix_slack == 0, "extremizer touches a prefix cap")

    j45 = first_same_weight_feasible(45)
    j46 = first_same_weight_feasible(46)
    j47 = first_same_weight_feasible(47)
    require((j45, j46, j47) == (607_348, 607_634, 607_783),
            "same-weight feasibility thresholds")
    require(WEIGHT_CUTOFF + 1 >= j45, "baseline layers pass same-weight relaxation")
    require(extra_start >= j46, "extra layers pass same-weight relaxation")

    return {
        "high_weight_interval": [WEIGHT_CUTOFF + 1, RADIUS],
        "high_layer_count": HIGH_LAYER_COUNT,
        "free_baseline": FREE_BASELINE,
        "base_mass": base_mass,
        "tail_definition": "sum_(j>J0) max(M_j-45,0)",
        "credit_identity": (
            "list_size=3730+45H+tail-(3730-N_low)-"
            "sum_(r=1)^45(H-H_r)"
        ),
        "safe_iff_signed_occupancy_at_most": SAFE_TAIL,
        "forbidden_implies_signed_occupancy_at_least": FORCED_TAIL,
        "canonical_anchor_count": FREE_BASELINE,
        "one_extra_support_one_marked_rank46_key": True,
        "marked_rank46_keys_forced_lower": FORCED_TAIL,
        "arithmetic_extremizer": {
            "low_mass_at_weight": WEIGHT_CUTOFF,
            "low_mass": PACKING_CAP,
            "baseline_multiplicity": FREE_BASELINE,
            "extra_interval": [extra_start, RADIUS],
            "extra_multiplicity": 1,
            "total": total,
            "maximum_layer_multiplicity": FORCED_RANK,
            "all_prefix_caps_respected": True,
            "minimum_prefix_slack": minimum_prefix_slack,
            "same_weight_thresholds": {"45": j45, "46": j46, "47": j47},
            "source_realized": False,
            "role": "sharp arithmetic relaxation only",
        },
        "rank47_not_forced_by_current_incidence_hypotheses": True,
    }


def ordered_prefix_max(total: int, ordered_count: int, prefix_count: int) -> int:
    quotient, remainder = divmod(total, ordered_count)
    return prefix_count * quotient + max(0, remainder - (ordered_count - prefix_count))


def rank46_forney() -> dict[str, Any]:
    require((FORNEY_INDEX_COUNT, SMALL_INDEX_COUNT) == (45, 44), "Forney index counts")
    require(SMALL_INDEX_SUM_MAX == 913_681, "small-index sum")
    p1 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_INDEX_COUNT, 1)
    p2 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_INDEX_COUNT, 2)
    p3 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_INDEX_COUNT, 3)
    p4 = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_INDEX_COUNT, 4)
    require((p1, p2, p3, p4) == (20_765, 41_530, 62_295, 83_060),
            "ordered partial-sum bounds")
    require(p3 < CUTOFF_MIN < p4,
            "aggregate bound certifies rank three but not rank four")
    high_small = SMALL_INDEX_SUM_MAX // CUTOFF_MIN
    low_indices = FORNEY_INDEX_COUNT - (high_small + 1)
    require((high_small, low_indices) == (13, 31), "low-index count")

    return {
        "packet_columns": FORCED_RANK,
        "forney_indices": FORNEY_INDEX_COUNT,
        "small_indices": SMALL_INDEX_COUNT,
        "small_index_sum_uniform_max": SMALL_INDEX_SUM_MAX,
        "cutoff_uniform_min": CUTOFF_MIN,
        "ordered_partial_sum_max": {
            "1": p1,
            "2": p2,
            "3": p3,
            "4": p4,
        },
        "rank3_minor_degree_max": p3,
        "rank3_strictly_below_cutoff": True,
        "rank4_certified_strictly_below_cutoff_by_aggregate_bound": False,
        "indices_below_cutoff_lower": low_indices,
        "pluecker_gcd_divisibility": (
            "gcd(P_k:k notin I) divides Delta_I for every nonzero r-minor"
        ),
        "distinguished_extra_dichotomy": {
            "NONCOLOOP_RANK3": {
                "old_column_basis_size": 3,
                "complementary_subfamily_size": 43,
                "distinguished_extra_retained": True,
                "additional_common_core_degree_max": p3,
                "payment_status": "UNPAID_COMMON_CORE_ADD_BACK",
            },
            "COLOOP_RANK2": {
                "old_anchor_columns": FREE_BASELINE,
                "old_column_rank_max": 2,
                "payment_status": "UNPAID_RANK2_COLOOP",
            },
        },
    }


def root_union_route_cut() -> dict[str, Any]:
    rank2_degree = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_INDEX_COUNT, 2)
    rank3_degree = ordered_prefix_max(SMALL_INDEX_SUM_MAX, SMALL_INDEX_COUNT, 3)
    rank2_global_keys = SAFE_TAIL // rank2_degree
    rank3_global_keys = SAFE_TAIL // rank3_degree
    require((rank2_global_keys, rank3_global_keys) == (6, 4), "global root-key allowances")
    require(SAFE_TAIL - rank2_global_keys * rank2_degree == 10_700,
            "rank2 root residual")
    require(SAFE_TAIL - rank3_global_keys * rank3_degree == 10_700,
            "rank3 root residual")
    require((rank2_global_keys + 1) * rank2_degree > SAFE_TAIL,
            "seventh rank2 key exceeds")
    require((rank3_global_keys + 1) * rank3_degree > SAFE_TAIL,
            "fifth rank3 key exceeds")
    require(FORCED_RANK <= rank2_degree < rank3_degree,
            "arithmetic extremizer survives optimistic per-layer root caps")
    return {
        "optimistic_local_owner": "entire layer injects into roots of one low minor",
        "rank2_minor_degree_max": rank2_degree,
        "rank3_minor_degree_max": rank3_degree,
        "arithmetic_extremizer_max_layer": FORCED_RANK,
        "arithmetic_extremizer_survives_each_per_layer_bound": True,
        "independent_per_layer_root_unions_close_row": False,
        "global_distinct_key_allowance": {
            "rank2_degree_keys": rank2_global_keys,
            "rank3_degree_keys": rank3_global_keys,
            "residual_after_max_keys": 10_700,
        },
        "required_new_input": (
            "cross-layer/source-key deduplication, exact semantic owner refund, "
            "or primitive-component elimination"
        ),
    }


def canonical_combinatorial_toy() -> dict[str, Any]:
    """Finite set-system control for the lex-first canonical padding factor."""
    toy_n, toy_k, toy_a = 12, 5, 7
    candidates = [set(c) for size in (9, 8, 7)
                  for c in itertools.combinations(range(toy_n), size)]
    family: list[set[int]] = []
    for agreement_set in candidates:
        if all(len(agreement_set & old) <= toy_k - 1 for old in family):
            family.append(agreement_set)
        if len(family) == 7:
            break
    require(len(family) >= 4, "canonical toy family")

    canonical_supports: set[tuple[int, ...]] = set()
    rows = []
    padded_rows = 0
    for agreement_set in family:
        selected = tuple(sorted(agreement_set)[:toy_a])
        require(len(selected) == toy_a, "toy canonical selector size")
        require(selected not in canonical_supports, "toy selector injection")
        canonical_supports.add(selected)
        pivot = selected[-1]
        roots = set(range(toy_n)) - set(selected)
        errors = set(range(toy_n)) - agreement_set
        padding = agreement_set - set(selected)
        require(roots == errors | padding and not errors & padding, "error-padding factorization")
        require(all(point in roots for point in range(pivot + 1, toy_n)), "suffix divides locator")
        require(pivot not in roots, "pivot is selected agreement")
        require(len([x for x in roots if x < pivot]) == pivot + 1 - toy_a,
                "prefix root degree")
        padded_rows += bool(padding)
        rows.append((tuple(sorted(agreement_set)), selected, pivot,
                     tuple(sorted(errors)), tuple(sorted(padding))))

    digest = hashlib.sha256(repr(rows).encode()).hexdigest()
    require(padded_rows > 0, "toy exercises padding")
    return {
        "n": toy_n,
        "K": toy_k,
        "a": toy_a,
        "family_size": len(family),
        "padded_rows": padded_rows,
        "rows_sha256": digest,
        "selector_injective_under_pairwise_K_minus_1_overlap": True,
        "locator_equals_error_times_padding": True,
        "complete_suffix_factor": True,
    }


def global_popov_compiler() -> dict[str, Any]:
    parameter_dimension = RADIUS - SHIFT + 1
    require(parameter_dimension == 913_683, "balanced coefficient dimension")
    require(parameter_dimension == 2 * RADIUS - K + 1, "dimension identity")
    require(parameter_dimension == SMALL_INDEX_SUM_MAX + 2, "global/local gap")
    require(2 * SHIFT <= N - K, "near-rational hypothesis")
    require(RADIUS + 1 == 981_130, "canonical pivot cell count")
    return {
        "ordered_domain_required": True,
        "canonical_boundary_selector": "first a agreement points",
        "whole_list_bijection": (
            "c <-> (W_c,N_c)=(Lambda_(D\\T_c),Lambda_(D\\T_c)c) "
            "inside the Paper-D lattice census with the lex-first mask"
        ),
        "boundary_locator_degree": RADIUS,
        "canonical_pivot_cells": RADIUS + 1,
        "pivot_index_range_one_based": [AGREEMENT, N],
        "suffix_cell": (
            "h=a+r; W=Q_h P with Q_h=product_(i>h)(X-x_i), "
            "deg P=r, and prefix roots required to be actual errors"
        ),
        "suffix_division_equivalence": (
            "Q_h(P,M) in M_y iff (P,M) is in the interpolation lattice "
            "of y restricted to the first h domain points"
        ),
        "near_rational": {
            "condition": "d1<=w",
            "list_upper": 1,
            "owner": "NEAR_RATIONAL_SINGLETON",
        },
        "balanced": {
            "condition": "d1>=w+1",
            "row_degree_sum": N - K + 1,
            "coefficient_dimension": parameter_dimension,
            "terminal": "CANONICAL_MASKED_SPLIT_PENCIL",
        },
        "nested_packing_selector": {
            "first_s_size": PACKING_SIZE,
            "first_a_size": AGREEMENT,
            "same_domain_order": True,
            "first_a_subset_of_first_s": True,
        },
        "interior_factorization": "W_c=Lambda_(E_c) Q_c",
        "padding_points_are_agreements": True,
        "padding_points_have_one_point_escape": False,
        "global_popov_locator_equals_actual_error_locator_only_at_weight_R": True,
        "interior_padding_bridge": "UNPAID_PADDING_BRIDGE",
        "local_rank46_frame_automatically_embeds_in_global_rank2_lattice": False,
    }


def regressions() -> dict[str, Any]:
    f241_lhs = 58_081 * (10 - 3)
    f241_rhs = 7 * 44_100
    require((f241_lhs, f241_rhs, f241_lhs - f241_rhs) == (406_567, 308_700, 97_867),
            "PR1005 F241 regression")
    return {
        "pr1005_support_only_3plus7_counterexample": {
            "dependency_head": PR1005_HEAD,
            "field": 241,
            "prefix_denominator": 58_081,
            "rooted_degree": 10,
            "ambient_shell": 44_100,
            "lhs": f241_lhs,
            "rhs": f241_rhs,
            "margin": f241_lhs - f241_rhs,
            "support_only_owner_assignment_allowed": False,
            "required_terminal": "REQUIRES_SEMANTIC_FIRST_MATCH",
        },
        "pr1007_literal_packet_route_cut": {
            "dependency_head": PR1007_HEAD,
            "actual_parity_free_packet_sizes": [36, 230],
            "arbitrary_packet_forces_parity_face": False,
            "full_center_budget_status": "UNKNOWN",
        },
        "canonical_padding": canonical_combinatorial_toy(),
    }


def build_payload() -> dict[str, Any]:
    optimizer, caps = packing_cutoff_scan()
    payload = {
        "schema": "m31-canonical-popov-rank46-compiler-v1",
        "artifact_kind": "M31_MAXIMAL_MASS_COMPILER_AND_ROUTE_CUT",
        "dependencies": {
            "pr1005_rooted_shell_head": PR1005_HEAD,
            "pr1007_rank36_head_and_local_parent": PR1007_HEAD,
        },
        "deployed": {
            "p": P,
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "shift": SHIFT,
            "radius": RADIUS,
            "budget": BUDGET,
            "forbidden_size": FORBIDDEN,
        },
        "canonical_global_popov": global_popov_compiler(),
        "balanced_prefix_packing": selected_packing_gate(),
        "cutoff_optimizer": optimizer,
        "occupancy_rank46_compiler": occupancy_compiler(caps),
        "rank46_forney_pluecker": rank46_forney(),
        "root_union_route_cut": root_union_route_cut(),
        "semantic_first_match_terminals": [
            "ZERO_SYNDROME",
            "NEAR_RATIONAL_SINGLETON",
            "NAMED_EXISTING_OWNER_WITH_EXACT_CHARGE_AND_REFUND",
            "CANONICAL_MASKED_SPLIT_PENCIL",
            "UNPAID_PADDING_BRIDGE",
            "UNPAID_COMMON_CORE_ADD_BACK",
            "UNPAID_RANK2_COLOOP",
        ],
        "regressions": regressions(),
        "literature_audit": {
            "theoremsearch_result": "predictable-degree property located; no semantic padding theorem",
            "outside_primary_search": [
                "Jeannerod-Neiger-Villard, Fast computation of approximant bases in canonical form, arXiv:1801.04553",
                "Jeannerod-Neiger-Schost-Villard, Fast computation of minimal interpolation bases in Popov form, arXiv:1602.00651",
                "Beckermann-Labahn-Villard, Normal forms for general polynomial matrices, JSC 41 (2006)",
            ],
            "project_specific_owner_refund_or_padding_bridge_found": False,
        },
        "scope_guards": {
            "m31_list_row_closed": False,
            "ledger_movement": 0,
            "owner_charge": None,
            "arithmetic_extremizer_source_realized": False,
            "stable_tex_modified": False,
            "lean_used_for_discovery": False,
        },
        "source_sha256": {str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS},
    }
    return payload


def verify_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "m31-canonical-popov-rank46-compiler-v1", "schema")
    require(payload["artifact_kind"] == "M31_MAXIMAL_MASS_COMPILER_AND_ROUTE_CUT", "artifact kind")
    deployed = payload["deployed"]
    require((deployed["p"], deployed["n"], deployed["K"]) == (P, N, K), "deployed field/code")
    require((deployed["agreement"], deployed["shift"], deployed["radius"]) ==
            (AGREEMENT, SHIFT, RADIUS), "deployed agreement")
    require((deployed["budget"], deployed["forbidden_size"]) == (BUDGET, FORBIDDEN), "budget")

    packing = payload["balanced_prefix_packing"]
    require(packing["weight_cutoff"] == WEIGHT_CUTOFF, "packing cutoff")
    require(packing["chosen_agreement_subset_size"] == PACKING_SIZE, "packing size")
    require(packing["certified_low_prefix_cap"] == PACKING_CAP, "packing cap")
    require(packing["cap_feasible_relaxation"]["margin"] == 202_311, "feasible margin")
    require(packing["first_excluded"]["contradiction_margin"] == 19_019, "failure margin")
    require(packing["plain_cauchy_cap"] == 3_732, "Cauchy regression")
    require(packing["integer_rounding_is_load_bearing"] is True, "integer packing gate")

    optimizer = payload["cutoff_optimizer"]
    require(optimizer["last_cutoff"] == 614_242, "optimizer endpoint")
    require(optimizer["rows_scanned"] == 89_955, "optimizer row count")
    require(optimizer["rows_sha256"] == OPTIMIZER_ROWS_SHA256, "optimizer digest")
    require(optimizer["selected_baseline_is_global_scan_optimum"] is True,
            "optimizer selected baseline")
    require(optimizer["largest_forced_rank"] == FORCED_RANK, "optimizer rank")
    require(optimizer["rank_47_forced"] is False, "rank47 route cut")
    row45 = next(row for row in optimizer["pareto_baselines_30_46"]
                 if row["baseline"] == FREE_BASELINE)
    require((row45["best_cutoff"], row45["low_prefix_cap"], row45["forced_tail_lower"]) ==
            (WEIGHT_CUTOFF, PACKING_CAP, FORCED_TAIL), "baseline45 optimum")

    occupancy = payload["occupancy_rank46_compiler"]
    require(occupancy["high_layer_count"] == HIGH_LAYER_COUNT, "high layers")
    require(occupancy["free_baseline"] == FREE_BASELINE, "free baseline")
    require(occupancy["safe_iff_signed_occupancy_at_most"] == SAFE_TAIL, "safe tail")
    require(occupancy["forbidden_implies_signed_occupancy_at_least"] == FORCED_TAIL,
            "forbidden tail")
    require(occupancy["canonical_anchor_count"] == FREE_BASELINE, "anchor count")
    require(occupancy["marked_rank46_keys_forced_lower"] == FORCED_TAIL, "source keys")
    extremizer = occupancy["arithmetic_extremizer"]
    require(extremizer["total"] == FORBIDDEN, "extremizer total")
    require(extremizer["maximum_layer_multiplicity"] == FORCED_RANK, "extremizer maximum")
    require(extremizer["all_prefix_caps_respected"] is True, "extremizer prefix gates")
    require(extremizer["source_realized"] is False, "extremizer nonclaim")

    forney = payload["rank46_forney_pluecker"]
    require((forney["packet_columns"], forney["forney_indices"], forney["small_indices"]) ==
            (46, 45, 44), "Forney shape")
    require(forney["ordered_partial_sum_max"] ==
            {"1": 20_765, "2": 41_530, "3": 62_295, "4": 83_060},
            "Forney partial sums")
    require(forney["rank3_strictly_below_cutoff"] is True, "rank3 cutoff")
    require(forney["rank4_certified_strictly_below_cutoff_by_aggregate_bound"] is False,
            "rank4 aggregate-bound route cut")
    require(forney["indices_below_cutoff_lower"] == 31, "low indices")
    require(forney["distinguished_extra_dichotomy"]["NONCOLOOP_RANK3"]
            ["payment_status"] == "UNPAID_COMMON_CORE_ADD_BACK", "noncoloop unpaid")
    require(forney["distinguished_extra_dichotomy"]["COLOOP_RANK2"]
            ["payment_status"] == "UNPAID_RANK2_COLOOP", "coloop unpaid")

    root_cut = payload["root_union_route_cut"]
    require(root_cut["rank2_minor_degree_max"] == 41_530, "root-cut rank2 degree")
    require(root_cut["rank3_minor_degree_max"] == 62_295, "root-cut rank3 degree")
    require(root_cut["arithmetic_extremizer_survives_each_per_layer_bound"] is True,
            "root-cut extremizer")
    require(root_cut["independent_per_layer_root_unions_close_row"] is False,
            "per-layer route cut")
    require(root_cut["global_distinct_key_allowance"] == {
        "rank2_degree_keys": 6,
        "rank3_degree_keys": 4,
        "residual_after_max_keys": 10_700,
    }, "global key allowance")

    popov = payload["canonical_global_popov"]
    require(popov["boundary_locator_degree"] == RADIUS, "boundary locator")
    require(popov["canonical_pivot_cells"] == RADIUS + 1, "pivot cells")
    require(popov["balanced"]["coefficient_dimension"] == 913_683, "Popov dimension")
    require(popov["interior_padding_bridge"] == "UNPAID_PADDING_BRIDGE", "padding terminal")
    require(popov["padding_points_have_one_point_escape"] is False, "padding escape")
    require(popov["local_rank46_frame_automatically_embeds_in_global_rank2_lattice"] is False,
            "no false Popov merger")

    f241 = payload["regressions"]["pr1005_support_only_3plus7_counterexample"]
    require(f241["margin"] == 97_867, "F241 margin")
    require(f241["support_only_owner_assignment_allowed"] is False, "F241 semantic guard")
    require(f241["required_terminal"] == "REQUIRES_SEMANTIC_FIRST_MATCH", "F241 terminal")
    require(payload["regressions"]["pr1007_literal_packet_route_cut"]
            ["arbitrary_packet_forces_parity_face"] is False, "parity regression")

    guards = payload["scope_guards"]
    require(guards["m31_list_row_closed"] is False, "row remains open")
    require(guards["ledger_movement"] == 0, "ledger movement")
    require(guards["owner_charge"] is None, "owner charge null")
    require(guards["arithmetic_extremizer_source_realized"] is False, "source nonclaim")
    require(payload["literature_audit"]["project_specific_owner_refund_or_padding_bridge_found"]
            is False, "literature boundary")

    hashes = payload["source_sha256"]
    require(set(hashes) == {str(path.relative_to(ROOT)) for path in SOURCE_PATHS}, "source hash keys")
    require(hashes == {str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS},
            "live source hashes")

    claimed = payload.get("certificate_sha256")
    require(isinstance(claimed, str) and len(claimed) == 64, "certificate hash shape")
    unsealed = copy.deepcopy(payload)
    unsealed.pop("certificate_sha256", None)
    require(hashlib.sha256(canonical_json(unsealed)).hexdigest() == claimed, "certificate self hash")


def mutate_path(payload: dict[str, Any], path: tuple[str, ...], value: Any) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    cursor: Any = out
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return seal(out)


def tamper_selftest(expected: dict[str, Any]) -> None:
    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("field", lambda d: mutate_path(d, ("deployed", "p"), P - 1)),
        ("budget", lambda d: mutate_path(d, ("deployed", "budget"), BUDGET + 1)),
        ("cutoff", lambda d: mutate_path(d, ("balanced_prefix_packing", "weight_cutoff"), WEIGHT_CUTOFF - 1)),
        ("packing-cap", lambda d: mutate_path(d, ("balanced_prefix_packing", "certified_low_prefix_cap"), PACKING_CAP + 1)),
        ("rounding-margin", lambda d: mutate_path(d, ("balanced_prefix_packing", "first_excluded", "contradiction_margin"), 0)),
        ("cauchy", lambda d: mutate_path(d, ("balanced_prefix_packing", "plain_cauchy_cap"), PACKING_CAP)),
        ("optimizer-end", lambda d: mutate_path(d, ("cutoff_optimizer", "last_cutoff"), 614_241)),
        ("optimizer-count", lambda d: mutate_path(d, ("cutoff_optimizer", "rows_scanned"), 89_954)),
        ("optimizer-digest", lambda d: mutate_path(d, ("cutoff_optimizer", "rows_sha256"), "0" * 64)),
        ("optimizer-global", lambda d: mutate_path(d, ("cutoff_optimizer", "selected_baseline_is_global_scan_optimum"), False)),
        ("rank47", lambda d: mutate_path(d, ("cutoff_optimizer", "rank_47_forced"), True)),
        ("safe-tail", lambda d: mutate_path(d, ("occupancy_rank46_compiler", "safe_iff_signed_occupancy_at_most"), FORCED_TAIL)),
        ("anchor-count", lambda d: mutate_path(d, ("occupancy_rank46_compiler", "canonical_anchor_count"), 44)),
        ("source-keys", lambda d: mutate_path(d, ("occupancy_rank46_compiler", "marked_rank46_keys_forced_lower"), FORCED_TAIL - 1)),
        ("extremizer-realized", lambda d: mutate_path(d, ("occupancy_rank46_compiler", "arithmetic_extremizer", "source_realized"), True)),
        ("extremizer-max", lambda d: mutate_path(d, ("occupancy_rank46_compiler", "arithmetic_extremizer", "maximum_layer_multiplicity"), 47)),
        ("mu12", lambda d: mutate_path(d, ("rank46_forney_pluecker", "ordered_partial_sum_max", "2"), 41_531)),
        ("mu123", lambda d: mutate_path(d, ("rank46_forney_pluecker", "ordered_partial_sum_max", "3"), 62_296)),
        ("rank4", lambda d: mutate_path(d, ("rank46_forney_pluecker", "rank4_certified_strictly_below_cutoff_by_aggregate_bound"), True)),
        ("low-index", lambda d: mutate_path(d, ("rank46_forney_pluecker", "indices_below_cutoff_lower"), 30)),
        ("pay-coloop", lambda d: mutate_path(d, ("rank46_forney_pluecker", "distinguished_extra_dichotomy", "COLOOP_RANK2", "payment_status"), "PAID")),
        ("per-layer-closes", lambda d: mutate_path(d, ("root_union_route_cut", "independent_per_layer_root_unions_close_row"), True)),
        ("global-root-keys", lambda d: mutate_path(d, ("root_union_route_cut", "global_distinct_key_allowance", "rank3_degree_keys"), 5)),
        ("Popov-dimension", lambda d: mutate_path(d, ("canonical_global_popov", "balanced", "coefficient_dimension"), 913_681)),
        ("padding-paid", lambda d: mutate_path(d, ("canonical_global_popov", "interior_padding_bridge"), "PAID")),
        ("padding-escape", lambda d: mutate_path(d, ("canonical_global_popov", "padding_points_have_one_point_escape"), True)),
        ("false-merger", lambda d: mutate_path(d, ("canonical_global_popov", "local_rank46_frame_automatically_embeds_in_global_rank2_lattice"), True)),
        ("F241-owner", lambda d: mutate_path(d, ("regressions", "pr1005_support_only_3plus7_counterexample", "support_only_owner_assignment_allowed"), True)),
        ("parity-face", lambda d: mutate_path(d, ("regressions", "pr1007_literal_packet_route_cut", "arbitrary_packet_forces_parity_face"), True)),
        ("ledger", lambda d: mutate_path(d, ("scope_guards", "ledger_movement"), 1)),
        ("closure", lambda d: mutate_path(d, ("scope_guards", "m31_list_row_closed"), True)),
        ("owner-charge", lambda d: mutate_path(d, ("scope_guards", "owner_charge"), 0)),
        ("literature-overclaim", lambda d: mutate_path(d, ("literature_audit", "project_specific_owner_refund_or_padding_bridge_found"), True)),
        ("source-hash", lambda d: mutate_path(
            d,
            ("source_sha256", str(NOTE_PATH.relative_to(ROOT))),
            "0" * 64,
        )),
    ]
    rejected = 0
    for label, mutator in mutations:
        candidate = mutator(expected)
        try:
            verify_payload(candidate)
        except (VerificationError, KeyError, StopIteration, TypeError):
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")
    require(rejected == len(mutations), "all mutations rejected")
    print(f"tamper-selftest: PASS ({rejected}/{len(mutations)})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.write or args.check or args.tamper_selftest):
        args.check = True

    expected = seal(build_payload())
    verify_payload(expected)

    if args.write:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_bytes(canonical_json(expected))
        print(f"wrote {CERTIFICATE_PATH.relative_to(ROOT)}")

    if args.check:
        require(CERTIFICATE_PATH.exists(), "certificate exists")
        actual = json.loads(CERTIFICATE_PATH.read_text())
        verify_payload(actual)
        require(actual == expected, "certificate equals regenerated payload")

    if args.tamper_selftest:
        tamper_selftest(expected)

    print("M31 canonical-Popov rank-46 compiler: PASS")
    print(f"cutoff={WEIGHT_CUTOFF} low_cap={PACKING_CAP} high_layers={HIGH_LAYER_COUNT}")
    print(f"forced rank-46 keys={FORCED_TAIL}; safe signed tail={SAFE_TAIL}")
    print("Forney: mu1+mu2<=41530, mu1+mu2+mu3<=62295<67447")
    print("terminals: UNPAID_PADDING_BRIDGE / UNPAID_COMMON_CORE_ADD_BACK / UNPAID_RANK2_COLOOP")
    print("M31 row: OPEN; ledger movement: 0")
    print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
