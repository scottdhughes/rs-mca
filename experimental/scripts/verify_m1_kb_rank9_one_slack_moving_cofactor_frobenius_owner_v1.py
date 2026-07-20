#!/usr/bin/env python3
"""Verify the one-slack moving-cofactor source-Frobenius owner.

The companion theorem closes only the r=1, (h,u,ell)=(0,1,0)
moving-linear-cofactor component.  It charges the roots of one canonical
source-only four-anchor eliminant, deletes the exact incoming intersection,
and restarts selectors.  The r>=2 full-outside residual, non-full-outside
source load, U_Q, residual U_A, and the KoalaBear row remain open.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_one_slack_twist_subline_owner_v1 as predecessor


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-one-slack-moving-cofactor-frobenius-owner-v1"
ARTIFACT_KIND = "M1_KB_RANK9_ONE_SLACK_MOVING_COFACTOR_SOURCE_FROBENIUS_OWNER"
STATUS = (
    "PROVED_LOCAL_PAIR_GLOBAL_SOURCE_FROBENIUS_OWNER_"
    "MOVING_COFACTOR_ONE_SLACK_COMPONENT_CLOSED_REVIEWS_GREEN_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-one-slack-moving-cofactor-frobenius-owner-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-one-slack-moving-cofactor-frobenius-owner-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1.sage"
)
MOVING_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_moving_root_slack_c5_boundary_v1.md"
)
MOVING_SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.sage"
)
SOURCE_RATIONAL_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_source_rational_owner_splice_v1.md"
)
SOURCE_RATIONAL_SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_source_rational_owner_splice_v1.sage"
)
RICH_ATLAS_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_rank9_rich_pencil_atlas_v1.md"
)

P = predecessor.P
N = predecessor.N
K = predecessor.K
A = predecessor.A
J = predecessor.J
T = predecessor.T
EXTENSION_DEGREE = predecessor.EXTENSION_DEGREE
RICH_X_MAX = predecessor.RICH_X_MAX
CUTOFF_D = predecessor.CUTOFF_D

SOURCE_SIZE = T + 2
SLACK_R = 1
REDUCED_X_MIN = (SOURCE_SIZE + 1) // 2 - 1
REDUCED_E_MIN = REDUCED_X_MIN + 1
REDUCED_E_MAX = RICH_X_MAX + 1
SOURCE_COMBINATION_SUPPORT_MIN = SOURCE_SIZE - REDUCED_E_MAX
FULL_MEMBER_BASE_LOCATOR_DEGREE = K - 2

OWNER_CAP = 2 * P + 2
U_PAID_BEFORE = predecessor.U_PAID_AFTER
B_REMAINING_BEFORE = predecessor.B_REMAINING_AFTER
B_STAR = predecessor.B_STAR
LEDGER_MOVEMENT = OWNER_CAP
U_PAID_AFTER = U_PAID_BEFORE + LEDGER_MOVEMENT
B_REMAINING_AFTER = B_STAR - U_PAID_AFTER

NEXT_SOURCE_SIZE = SOURCE_SIZE + 1
NEXT_REDUCED_DEGREE_MIN = (NEXT_SOURCE_SIZE + 1) // 2
NEXT_FULL_GCD_MAX = K - 1 - NEXT_REDUCED_DEGREE_MIN

EXPECTED_TAIL_TARGET = 17_900_043_416_181
EXPECTED_E_MAX = int(
    "5204235748184821982241887438598935212904144649"
)
EXPECTED_K_REMAINING = 4_807_520
EXPECTED_BREAK_J = 164

SOURCE_RATIONAL_OWNER = predecessor.SOURCE_RATIONAL_OWNER
TWIST_OWNER_ID = predecessor.TWIST_OWNER_ID
MOVING_OWNER_ID = "source_frobenius_moving_linear_cofactor"
PAID_TERMINAL = "PAID_PAIR_GLOBAL_SOURCE_FROBENIUS_MOVING_LINEAR_COFACTOR"
CLOSED_TERMINAL = "UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR"
OPEN_TERMINAL = "UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67475"

FIRST_MATCH_ORDER = list(predecessor.FIRST_MATCH_ORDER)
twist_index = FIRST_MATCH_ORDER.index(TWIST_OWNER_ID)
FIRST_MATCH_ORDER.insert(twist_index + 1, MOVING_OWNER_ID)

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessors",
    "one_slack_record",
    "source_frobenius_eliminant",
    "nonvanishing_lemma",
    "pair_global_owner",
    "first_match_partition",
    "selector_restart",
    "exact_control",
    "ledger",
    "rank9_updated_gate",
    "revised_residual",
    "residual_route_cuts",
    "scope_guards",
    "nonclaims",
    "source_bindings",
    "payload_sha256",
}


class ContractError(RuntimeError):
    """Raised for parser, source, semantic, or arithmetic drift."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ContractError(f"nonstandard JSON constant: {value}")


def reject_float(value: str) -> None:
    raise ContractError(f"floating-point JSON number: {value}")


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
        parse_float=reject_float,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {path}")
    return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def payload_hash(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing source binding: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("proof-note", NOTE_REL, "source-Frobenius owner theorem and splice"),
        source_binding("python-verifier", SCRIPT_REL, "certificate, arithmetic, and mutations"),
        source_binding("sage-control", SAGE_REL, "determinant and Segre-interface controls"),
        source_binding("readme", README_REL, "replay and scope contract"),
        source_binding(
            "twist-predecessor-note",
            predecessor.NOTE_REL,
            "closed sibling cell and banked ledger",
        ),
        source_binding(
            "twist-predecessor-sage",
            predecessor.SAGE_REL,
            "closed sibling exact control",
        ),
        source_binding(
            "twist-predecessor-certificate",
            predecessor.CERT_PATH.relative_to(ROOT),
            "banked exact ledger payload",
        ),
        source_binding(
            "twist-predecessor-verifier",
            predecessor.SCRIPT_REL,
            "banked ledger and restart semantics",
        ),
        source_binding("moving-slack-note", MOVING_NOTE_REL, "one-slack normal form"),
        source_binding("moving-slack-sage", MOVING_SAGE_REL, "predecessor toy interface"),
        source_binding(
            "source-rational-note",
            SOURCE_RATIONAL_NOTE_REL,
            "reduced-degree floor and subset stability",
        ),
        source_binding(
            "source-rational-sage",
            SOURCE_RATIONAL_SAGE_REL,
            "earlier owner edge controls",
        ),
        source_binding("rich-pencil-note", RICH_ATLAS_NOTE_REL, "moving-set identities"),
    ]


def validate_predecessors() -> None:
    document = predecessor.load_json(predecessor.CERT_PATH)
    predecessor.validate_certificate(document)
    require(
        document["ledger"]["U_paid_after"] == str(U_PAID_BEFORE),
        "banked U_paid drift",
    )
    require(
        document["ledger"]["B_remaining_after"] == str(B_REMAINING_BEFORE),
        "banked remaining budget drift",
    )
    require(
        document["pair_global_owner"]["closed_terminal"]
        == predecessor.CLOSED_TERMINAL,
        "common-twist predecessor terminal drift",
    )

    moving = (ROOT / MOVING_NOTE_REL).read_text(encoding="utf-8")
    for token in (
        "moving-cofactor cell \\((0,1,0)\\)",
        CLOSED_TERMINAL,
        "J_L\\ge21",
        "\\deg A_\\eta\\le1-\\delta_\\eta",
    ):
        require(token in moving, f"moving-slack predecessor token missing: {token}")

    source_rational = (ROOT / SOURCE_RATIONAL_NOTE_REL).read_text(encoding="utf-8")
    for token in (
        SOURCE_RATIONAL_OWNER,
        "e\\ge E(s)+1",
        "complete-selector universe",
    ):
        require(token in source_rational, f"source-rational predecessor token missing: {token}")


def exact_rank9_update() -> dict[str, Any]:
    gate = predecessor.ledger_base.tangent.one_cut_gate(
        B_REMAINING_AFTER, CUTOFF_D, N, 1
    )
    tail = int(gate["largest_sufficient_low_deficit_cap_T_star"])
    e_max = predecessor.ledger_base.tangent.aggregate_excess_max(tail)
    k_remaining = predecessor.ledger_base.tangent.exact_k_remaining(B_REMAINING_AFTER)
    maximal_binomial = math.comb(K - 2, 8)
    break_j = (
        predecessor.ledger_base.tangent.UNIFORM_CAP
        + e_max // maximal_binomial
        + 1
    )
    require(tail == EXPECTED_TAIL_TARGET, "tail target drift")
    require(e_max == EXPECTED_E_MAX, "aggregate excess maximum drift")
    require(k_remaining == EXPECTED_K_REMAINING, "K_remaining drift")
    require(break_j == EXPECTED_BREAK_J, "break J drift")
    return {
        "cutoff_D": CUTOFF_D,
        "old_tail_target": str(predecessor.EXPECTED_TAIL_TARGET),
        "new_tail_target": str(tail),
        "tail_target_drop": str(predecessor.EXPECTED_TAIL_TARGET - tail),
        "new_aggregate_excess_max": str(e_max),
        "K_remaining": k_remaining,
        "old_maximal_gcd_break_J": predecessor.EXPECTED_BREAK_J,
        "new_maximal_gcd_break_J": break_j,
        "gate": gate,
    }


_EXPECTED_CACHE: dict[str, Any] | None = None


def expected_certificate() -> dict[str, Any]:
    global _EXPECTED_CACHE
    if _EXPECTED_CACHE is not None:
        return copy.deepcopy(_EXPECTED_CACHE)

    validate_predecessors()
    note = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        PAID_TERMINAL,
        CLOSED_TERMINAL,
        OPEN_TERMINAL,
        "E_T(Z)",
        "2p+2=4{,}261{,}412{,}868",
        MOVING_OWNER_ID,
    ):
        require(token in note, f"proof-note token missing: {token}")

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "extension_degree": EXTENSION_DEGREE,
            "q_line": str(P**EXTENSION_DEGREE),
            "n": N,
            "k": K,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
            "domain_subset_base_nonzero": True,
        },
        "predecessors": {
            "common_twist_owner": predecessor.NOTE_REL.as_posix(),
            "moving_root_slack_c5_boundary": MOVING_NOTE_REL.as_posix(),
            "source_rational_owner": SOURCE_RATIONAL_NOTE_REL.as_posix(),
            "banked_ledger_payload": "payload-sha256:"
            + predecessor.load_json(predecessor.CERT_PATH)["payload_sha256"],
            "stacked_on_pr_989_head": "663cfbbaf3bfc5ea50d502e834bceca59811e732",
            "curated_upstream_may_omit_pr_side_json_and_python": True,
        },
        "one_slack_record": {
            "scope": (
                "full-outside coefficient-rank-two rich record after C5, "
                "source-rational, and common-twist restarts"
            ),
            "source_size_s": SOURCE_SIZE,
            "slack_r": SLACK_R,
            "slack_tuple_h_u_ell": [0, 1, 0],
            "full_gcd": "H=L_C in B[X]",
            "reduced_degree_e_equals_x_plus_one": True,
            "reduced_x_min": REDUCED_X_MIN,
            "reduced_x_max": RICH_X_MAX,
            "reduced_e_min": REDUCED_E_MIN,
            "reduced_e_max": REDUCED_E_MAX,
            "selected_deficits": [0, 1],
            "selected_rich_slopes_at_least": 21,
            "projectively_base_members_at_most": 1,
            "genuine_nonbase_linear_members_at_least": 20,
            "moving_member_identity": (
                "Pbar+eta*Qbar=kappa_eta*L_F_eta*(X-zeta_eta)"
            ),
            "zeta_eta_nonbase_for_genuine_member": True,
            "full_member_base_locator_degree": FULL_MEMBER_BASE_LOCATOR_DEGREE,
            "moving_sets_pairwise_disjoint": True,
        },
        "source_frobenius_eliminant": {
            "source_linear_form": "S_a(Z)=epsilon_0(a)+Z*epsilon_1(a)",
            "fingerprint": (
                "S_a(eta)^(p-1)=kappa_eta^(p-1)*"
                "(a-zeta_eta^p)/(a-zeta_eta)"
            ),
            "four_anchor_row": [
                "a*S_a(Z)^p",
                "S_a(Z)^p",
                "a*S_a(Z)",
                "S_a(Z)",
            ],
            "every_selected_slope_annihilates_every_four_anchor_minor": True,
            "projectively_base_exception_also_annihilates": True,
            "degree_cap": OWNER_CAP,
            "degree_formula": "2*p+2",
            "source_only": True,
            "selector_chosen_minor_forbidden": True,
            "union_over_minors_forbidden": True,
        },
        "nonvanishing_lemma": {
            "source_combination_support_min": SOURCE_COMBINATION_SUPPORT_MIN,
            "support_min_greater_than_one": True,
            "M_diagonal_distinct_nonzero": True,
            "all_minors_zero_implies_bivariate_wedge_zero": True,
            "separated_exponents": [
                i * P + j for i in range(3) for j in range(3)
            ],
            "separated_exponents_distinct": True,
            "low_span_case_max_dimension": 3,
            "low_span_forces_degree_at_most_one_source_map": True,
            "source_agreement_points_at_least": SOURCE_SIZE,
            "cross_determinant_degree_at_most": REDUCED_E_MAX + 1,
            "source_agreement_strictly_exceeds_cross_degree": True,
            "high_span_dimension": 4,
            "U_y_lines_pairwise_skew": True,
            "V_z_lines_dimension_two_and_distinct": True,
            "every_V_z_meeting_three_U_y_is_opposite_ruling": True,
            "opposite_ruling_shape": "(r*I+s*M)*span(epsilon_0,epsilon_1)",
            "invertible_opposite_parameter_contradicts_direct_sum": True,
            "singular_opposite_parameters_at_most_source_size": SOURCE_SIZE,
            "extension_field_size": str(P**EXTENSION_DEGREE),
            "extension_field_size_exceeds_source_size": True,
            "canonical_nonzero_minor_exists_if_record_exists": True,
        },
        "pair_global_owner": {
            "owner_id": MOVING_OWNER_ID,
            "owner_intrinsic_to_fixed_source_pair": True,
            "owner_definition": (
                "roots of lexicographically first nonzero four-anchor eliminant"
            ),
            "empty_if_all_source_minors_zero": True,
            "assigned_cell": "Z_mov=Gamma_in intersect roots(E_T_star)",
            "outgoing_cell": "Gamma_out=Gamma_in setminus Z_mov",
            "finite_slope_cap": OWNER_CAP,
            "ordinary_nonzero_polynomial_root_bound_used": True,
            "earlier_overlap_removed_by_exact_incoming_intersection": True,
            "later_overlap_removed_by_exact_deletion": True,
            "subset_stable_for_every_Gamma_subset_Gamma_in": True,
            "post_restart_moving_cofactor_record_impossible": True,
            "paid_terminal": PAID_TERMINAL,
            "closed_terminal": CLOSED_TERMINAL,
        },
        "first_match_partition": {
            "order": FIRST_MATCH_ORDER,
            "common_twist_index_one_based": FIRST_MATCH_ORDER.index(TWIST_OWNER_ID) + 1,
            "moving_owner_index_one_based": FIRST_MATCH_ORDER.index(MOVING_OWNER_ID) + 1,
            "residual_extension_index_one_based": FIRST_MATCH_ORDER.index(
                "residual_extension_valued_strata"
            ) + 1,
            "residual_base_index_one_based": FIRST_MATCH_ORDER.index(
                "residual_base_slope_universe"
            ) + 1,
            "incoming_exact_residual_required": True,
            "later_owners_receive_exact_set_difference": True,
            "per_selector_eliminant_charge_forbidden": True,
            "owner_may_conservatively_delete_bounded_intrinsic_set": True,
        },
        "selector_restart": {
            "complete_selector_restriction_certifies_nonempty_new_universe": True,
            "new_minimum_rank_at_most_old_minimum_rank": True,
            "complete_selector_universe_must_be_rebuilt": True,
            "restart_order": list(predecessor.ledger_base.tangent.RESTART_ORDER),
            "global_carrier_and_small_family_gates_rerun": True,
            "affine_rank_minimizer_recomputed": True,
            "stale_selector_fields_forbidden": list(
                predecessor.expected_certificate()["selector_restart"][
                    "stale_selector_fields_forbidden"
                ]
            ),
            "same_received_pair_source_and_sp3_translation_downstream": True,
            "all_rank_le_9_terminals_replayed_in_frozen_order": True,
            "rank_at_least_10_not_authorized": True,
        },
        "exact_control": {
            "base_field": "GF(13)",
            "extension_field": "GF(13^2)",
            "source_points_nonzero": True,
            "source_size": 6,
            "source_points": [1, 2, 3, 4, 5, 6],
            "moving_points": [7, 8, 9, 10, 11, 12],
            "source_and_moving_points_disjoint": True,
            "primitive_reduced_map": "R(X)=X^2+zeta*X",
            "reduced_degree": 2,
            "selected_fiber_count": 6,
            "moving_base_root_count_per_member": 1,
            "moving_nonbase_root_count_per_member": 1,
            "selected_source_support": 6,
            "universal_source_support_minimum": 5,
            "anchor_count": 15,
            "canonical_nonzero_minor_found": True,
            "first_nonzero_anchor": [0, 1, 2, 3],
            "first_nonzero_minor_degree": 26,
            "first_nonzero_minor_root_count": 13,
            "minor_degree_at_most_2p_plus_2": True,
            "selected_slopes_are_minor_roots": True,
            "four_dimensional_source_span": True,
            "U_y_plane_count": 169,
            "V_z_plane_count": 169,
            "singular_opposite_parameter_count": 6,
            "singular_opposite_parameter_cap_checked": True,
            "projectively_base_exception_checked": True,
            "degree_one_degenerate_source_all_minors_zero": True,
            "sage_interface_mutations": 40,
            "complete_selector_constructed": False,
            "deployed_rank9_record_constructed": False,
            "scale": "EXACT_TOY_CONTROL_NOT_DEPLOYED_SELECTOR_CENSUS_OR_PROOF",
        },
        "ledger": {
            "B_star": str(B_STAR),
            "new_owner_cap": str(OWNER_CAP),
            "ledger_movement": str(LEDGER_MOVEMENT),
            "U_paid_before": str(U_PAID_BEFORE),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "charge_is_once_per_received_pair_not_per_selector": True,
            "moving_cofactor_one_slack_component_paid": True,
            "U_Q": None,
            "residual_U_A": None,
            "complete_upper_inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "rank9_updated_gate": exact_rank9_update(),
        "revised_residual": {
            "zero_slack_boundary_owned": True,
            "all_three_one_slack_cells_owned": True,
            "next_source_size_min": NEXT_SOURCE_SIZE,
            "next_reduced_degree_min": NEXT_REDUCED_DEGREE_MIN,
            "next_full_gcd_degree_max": NEXT_FULL_GCD_MAX,
            "terminal": OPEN_TERMINAL,
        },
        "residual_route_cuts": [
            {
                "terminal": OPEN_TERMINAL,
                "condition": "full-outside coefficient-rank-two rich records with r>=2",
                "status": "UNPAID",
            },
            {
                "terminal": "UNBOUND_POST_TANGENT_SOURCE_LOAD",
                "condition": "non-full-outside and other source-load cells",
                "status": "UNPAID",
            },
            {
                "terminal": "UNPAID_U_Q_AND_RESIDUAL_U_A",
                "condition": "global finite adjacent upper ledger",
                "status": "UNPAID",
            },
        ],
        "scope_guards": {
            "common_factor_one_slack_component_closed": True,
            "moving_cofactor_one_slack_owner_proved": True,
            "moving_cofactor_one_slack_component_closed": True,
            "all_one_slack_cells_closed": True,
            "non_full_outside_source_load_paid": False,
            "residual_extension_all_paid": False,
            "U_Q_determined": False,
            "residual_U_A_determined": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": [
            "No alternative SP3 translations are unioned.",
            "No selector-chosen or per-record eliminant is charged.",
            "The determinant condition is necessary, not sufficient.",
            "The Sage control is toy-scale and is not the symbolic proof.",
            "No deployed complete selector or rank-nine census is constructed.",
            "Non-full-outside source load remains open.",
            "U_Q and residual U_A remain undetermined.",
            "The complete profile envelope and lower reserve remain open.",
            "Rank nine and KoalaBear remain open.",
            "Rank at least ten, Lean, and stable-paper promotion are not authorized.",
        ],
        "source_bindings": expected_source_bindings(),
        "payload_sha256": "",
    }
    result["payload_sha256"] = payload_hash(result)
    _EXPECTED_CACHE = copy.deepcopy(result)
    return result


def validate_certificate(document: dict[str, Any]) -> None:
    require(set(document) == TOP_KEYS, "top-level key drift")
    require(document["schema"] == SCHEMA, "schema drift")
    require(document["artifact_kind"] == ARTIFACT_KIND, "artifact kind drift")
    require(document["payload_sha256"] == payload_hash(document), "payload hash mismatch")
    expected = expected_certificate()
    require(document == expected, "certificate semantic or source-binding drift")


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("schema", lambda d: d.__setitem__("schema", "wrong")),
        ("status", lambda d: d.__setitem__("status", "GLOBAL_GREEN")),
        ("field", lambda d: d["row"].__setitem__("p", P + 1)),
        ("domain-zero", lambda d: d["row"].__setitem__("domain_subset_base_nonzero", False)),
        ("source-size", lambda d: d["one_slack_record"].__setitem__("source_size_s", SOURCE_SIZE - 1)),
        ("slack", lambda d: d["one_slack_record"].__setitem__("slack_tuple_h_u_ell", [1, 0, 0])),
        ("gcd-nonbase", lambda d: d["one_slack_record"].__setitem__("full_gcd", "nonbase")),
        ("degree-shape", lambda d: d["one_slack_record"].__setitem__("reduced_degree_e_equals_x_plus_one", False)),
        ("x-min", lambda d: d["one_slack_record"].__setitem__("reduced_x_min", REDUCED_X_MIN + 1)),
        ("x-max", lambda d: d["one_slack_record"].__setitem__("reduced_x_max", RICH_X_MAX - 1)),
        ("deficit", lambda d: d["one_slack_record"].__setitem__("selected_deficits", [0, 1, 2])),
        ("two-base", lambda d: d["one_slack_record"].__setitem__("projectively_base_members_at_most", 2)),
        ("few-nonbase", lambda d: d["one_slack_record"].__setitem__("genuine_nonbase_linear_members_at_least", 19)),
        ("base-zeta", lambda d: d["one_slack_record"].__setitem__("zeta_eta_nonbase_for_genuine_member", False)),
        ("locator-degree", lambda d: d["one_slack_record"].__setitem__("full_member_base_locator_degree", K - 1)),
        ("fingerprint", lambda d: d["source_frobenius_eliminant"].__setitem__("fingerprint", "wrong")),
        ("minor-not-universal", lambda d: d["source_frobenius_eliminant"].__setitem__("every_selected_slope_annihilates_every_four_anchor_minor", False)),
        ("base-exception", lambda d: d["source_frobenius_eliminant"].__setitem__("projectively_base_exception_also_annihilates", False)),
        ("degree-cap", lambda d: d["source_frobenius_eliminant"].__setitem__("degree_cap", OWNER_CAP + 1)),
        ("selector-minor", lambda d: d["source_frobenius_eliminant"].__setitem__("selector_chosen_minor_forbidden", False)),
        ("union-minors", lambda d: d["source_frobenius_eliminant"].__setitem__("union_over_minors_forbidden", False)),
        ("support-min", lambda d: d["nonvanishing_lemma"].__setitem__("source_combination_support_min", 1)),
        ("M-zero", lambda d: d["nonvanishing_lemma"].__setitem__("M_diagonal_distinct_nonzero", False)),
        ("exponents", lambda d: d["nonvanishing_lemma"].__setitem__("separated_exponents_distinct", False)),
        ("low-span", lambda d: d["nonvanishing_lemma"].__setitem__("low_span_forces_degree_at_most_one_source_map", False)),
        ("agreement", lambda d: d["nonvanishing_lemma"].__setitem__("source_agreement_points_at_least", REDUCED_E_MAX + 1)),
        ("cross-degree", lambda d: d["nonvanishing_lemma"].__setitem__("cross_determinant_degree_at_most", REDUCED_E_MAX + 2)),
        ("span-dim", lambda d: d["nonvanishing_lemma"].__setitem__("high_span_dimension", 3)),
        ("skew", lambda d: d["nonvanishing_lemma"].__setitem__("U_y_lines_pairwise_skew", False)),
        ("V-repeat", lambda d: d["nonvanishing_lemma"].__setitem__("V_z_lines_dimension_two_and_distinct", False)),
        ("ruling", lambda d: d["nonvanishing_lemma"].__setitem__("every_V_z_meeting_three_U_y_is_opposite_ruling", False)),
        ("invertible", lambda d: d["nonvanishing_lemma"].__setitem__("invertible_opposite_parameter_contradicts_direct_sum", False)),
        ("singular-count", lambda d: d["nonvanishing_lemma"].__setitem__("singular_opposite_parameters_at_most_source_size", SOURCE_SIZE + 1)),
        ("field-small", lambda d: d["nonvanishing_lemma"].__setitem__("extension_field_size_exceeds_source_size", False)),
        ("minor-none", lambda d: d["nonvanishing_lemma"].__setitem__("canonical_nonzero_minor_exists_if_record_exists", False)),
        ("chosen-owner", lambda d: d["pair_global_owner"].__setitem__("owner_intrinsic_to_fixed_source_pair", False)),
        ("owner-nonempty-degenerate", lambda d: d["pair_global_owner"].__setitem__("empty_if_all_source_minors_zero", False)),
        ("wrong-cap", lambda d: d["pair_global_owner"].__setitem__("finite_slope_cap", OWNER_CAP + 1)),
        ("no-root-bound", lambda d: d["pair_global_owner"].__setitem__("ordinary_nonzero_polynomial_root_bound_used", False)),
        ("not-subset-stable", lambda d: d["pair_global_owner"].__setitem__("subset_stable_for_every_Gamma_subset_Gamma_in", False)),
        ("record-survives", lambda d: d["pair_global_owner"].__setitem__("post_restart_moving_cofactor_record_impossible", False)),
        ("owner-order", lambda d: d["first_match_partition"]["order"].reverse()),
        ("owner-index", lambda d: d["first_match_partition"].__setitem__("moving_owner_index_one_based", 99)),
        ("per-selector-charge", lambda d: d["first_match_partition"].__setitem__("per_selector_eliminant_charge_forbidden", False)),
        ("later-not-difference", lambda d: d["first_match_partition"].__setitem__("later_owners_receive_exact_set_difference", False)),
        ("no-restart", lambda d: d["selector_restart"].__setitem__("complete_selector_universe_must_be_rebuilt", False)),
        ("stale-fields", lambda d: d["selector_restart"].__setitem__("stale_selector_fields_forbidden", [])),
        ("rank10", lambda d: d["selector_restart"].__setitem__("rank_at_least_10_not_authorized", False)),
        ("toy-deployed", lambda d: d["exact_control"].__setitem__("deployed_rank9_record_constructed", True)),
        ("toy-overlap", lambda d: d["exact_control"].__setitem__("source_and_moving_points_disjoint", False)),
        ("toy-count", lambda d: d["exact_control"].__setitem__("selected_fiber_count", 5)),
        ("toy-support", lambda d: d["exact_control"].__setitem__("universal_source_support_minimum", 4)),
        ("toy-anchor-count", lambda d: d["exact_control"].__setitem__("anchor_count", 14)),
        ("toy-minor", lambda d: d["exact_control"].__setitem__("canonical_nonzero_minor_found", False)),
        ("toy-minor-degree", lambda d: d["exact_control"].__setitem__("first_nonzero_minor_degree", 27)),
        ("toy-root-count", lambda d: d["exact_control"].__setitem__("first_nonzero_minor_root_count", 14)),
        ("toy-U-planes", lambda d: d["exact_control"].__setitem__("U_y_plane_count", 168)),
        ("toy-singular", lambda d: d["exact_control"].__setitem__("singular_opposite_parameter_count", 7)),
        ("toy-degenerate", lambda d: d["exact_control"].__setitem__("degree_one_degenerate_source_all_minors_zero", False)),
        ("toy-mutations", lambda d: d["exact_control"].__setitem__("sage_interface_mutations", 39)),
        ("ledger-cap", lambda d: d["ledger"].__setitem__("new_owner_cap", str(OWNER_CAP + 1))),
        ("ledger-movement", lambda d: d["ledger"].__setitem__("ledger_movement", str(LEDGER_MOVEMENT - 1))),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("B-remaining", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_AFTER - 1))),
        ("UQ-zero", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("UA-zero", lambda d: d["ledger"].__setitem__("residual_U_A", 0)),
        ("tail", lambda d: d["rank9_updated_gate"].__setitem__("new_tail_target", str(EXPECTED_TAIL_TARGET + 1))),
        ("Emax", lambda d: d["rank9_updated_gate"].__setitem__("new_aggregate_excess_max", str(EXPECTED_E_MAX + 1))),
        ("Kremaining", lambda d: d["rank9_updated_gate"].__setitem__("K_remaining", EXPECTED_K_REMAINING + 1)),
        ("break-J", lambda d: d["rank9_updated_gate"].__setitem__("new_maximal_gcd_break_J", EXPECTED_BREAK_J + 1)),
        ("next-source", lambda d: d["revised_residual"].__setitem__("next_source_size_min", SOURCE_SIZE)),
        ("next-degree", lambda d: d["revised_residual"].__setitem__("next_reduced_degree_min", NEXT_REDUCED_DEGREE_MIN - 1)),
        ("next-gcd", lambda d: d["revised_residual"].__setitem__("next_full_gcd_degree_max", NEXT_FULL_GCD_MAX + 1)),
        ("moving-open", lambda d: d["scope_guards"].__setitem__("moving_cofactor_one_slack_component_closed", False)),
        ("row-closed", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("lean", lambda d: d["scope_guards"].__setitem__("lean_authorized", True)),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("source-path", lambda d: d["source_bindings"][0].__setitem__("path", d["source_bindings"][1]["path"])),
        ("duplicate-binding", lambda d: d["source_bindings"][1].__setitem__("binding_id", d["source_bindings"][0]["binding_id"])),
        ("payload", lambda d: d.__setitem__("payload_sha256", "1" * 64)),
    ]


def run_parser_tamper_selftest() -> int:
    rejected = 0
    for payload in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1.5}'):
        try:
            json.loads(
                payload,
                object_pairs_hook=reject_duplicate_keys,
                parse_constant=reject_constant,
                parse_float=reject_float,
            )
        except ContractError:
            rejected += 1
        else:
            raise ContractError(f"parser mutation survived: {payload}")
    require(rejected == 3, "parser mutation count drift")
    return rejected


def run_tamper_selftest() -> int:
    baseline = expected_certificate()
    validate_certificate(baseline)
    rejected = 0
    for name, mutate in mutation_cases():
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        if name != "payload":
            candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except (ContractError, KeyError, IndexError, TypeError):
            rejected += 1
        else:
            raise ContractError(f"certificate mutation survived: {name}")
    parser_rejected = run_parser_tamper_selftest()
    total = rejected + parser_rejected
    require(rejected == len(mutation_cases()), "semantic mutation count drift")
    print(f"M1 moving-cofactor Frobenius owner mutations: {total}/{total} PASS")
    return 0


def write_certificate() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(expected_certificate(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_check() -> int:
    document = load_json(CERT_PATH)
    validate_certificate(document)
    print("M1 one-slack moving-cofactor source-Frobenius owner: PASS")
    print(f"  canonical eliminant degree / owner cap: 2p+2={OWNER_CAP:,}")
    print(
        "  one-slack x/e range: "
        f"{REDUCED_X_MIN:,}..{RICH_X_MAX:,} / "
        f"{REDUCED_E_MIN:,}..{REDUCED_E_MAX:,}"
    )
    print(f"  U_paid: {U_PAID_BEFORE:,} -> {U_PAID_AFTER:,}")
    print(f"  B_remaining: {B_REMAINING_BEFORE:,} -> {B_REMAINING_AFTER:,}")
    print(f"  T_18,014: {EXPECTED_TAIL_TARGET:,}; break J={EXPECTED_BREAK_J}")
    print(f"  terminal paid: {PAID_TERMINAL}")
    print(f"  terminal open: {OPEN_TERMINAL}")
    print("  U_Q/residual U_A/complete envelope/lower reserve remain open; row YELLOW")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return run_tamper_selftest()
    if args.print_certificate:
        print(json.dumps(expected_certificate(), indent=2, sort_keys=True))
        return 0
    if args.write:
        write_certificate()
        print(CERT_PATH)
        return 0
    return run_check()


if __name__ == "__main__":
    raise SystemExit(main())
