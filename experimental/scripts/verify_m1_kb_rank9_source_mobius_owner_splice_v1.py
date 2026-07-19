#!/usr/bin/env python3
"""Verify the pair-global KoalaBear source--Mobius owner splice.

The companion note upgrades the #960 same-selector synchronization theorem
to a selector-free owner for one fixed received pair and SP3 translation.
It binds the cross-selector containment, exact first-match deletion/restart,
and maximum-not-sum replacement of the existing C5/base joint block.
Lower-gcd and non-full-outside cells, U_Q, U_A, and the row remain open.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_projective_base_pair_c5_owner_v1 as c5_owner
import verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1 as sync


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-source-mobius-owner-splice-v1"
ARTIFACT_KIND = "M1_KB_RANK9_PAIR_GLOBAL_SOURCE_MOBIUS_OWNER_SPLICE"
STATUS = (
    "PROVED_PAIR_GLOBAL_SOURCE_MOBIUS_OWNER_"
    "EXACT_FIRST_MATCH_SPLICE_MAXIMAL_GCD_CELL_PAID_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-source-mobius-owner-splice-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_source_mobius_owner_splice_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_source_mobius_owner_splice_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-source-mobius-owner-splice-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_source_mobius_owner_splice_v1.sage"
)

SYNC_PAYLOAD = "62a42b283457f2f198e5c2968b2e82de87fde35421f2289b074f7b60c1b7d76b"
C5_PAYLOAD = "14e7112a3cc8aafce591d1962543c1e8789b7815c333ef4cd4f3b12279b5c6bb"
TANGENT_PAYLOAD = "0d5753ae6055d6f1dc0edb49f0e0322596da8a70b68b113993dcec11934e7eed"

tangent = c5_owner.tangent
P = sync.P
N = sync.N
K = sync.K
A = sync.A
J = sync.J
T = sync.T
SIGMA_FLOOR = sync.SIGMA_FLOOR
RICH_X_MAX = sync.RICH_X_MAX

SOURCE_MOBIUS_CAP = N - SIGMA_FLOOR
OLD_JOINT_CAP = P + 1
C5_BASE_CASE_CAP = P + 1
NONBASE_SOURCE_BASE_CASE_CAP = P + SOURCE_MOBIUS_CAP
NEW_JOINT_CAP = max(C5_BASE_CASE_CAP, NONBASE_SOURCE_BASE_CASE_CAP)
LEDGER_MOVEMENT = NEW_JOINT_CAP - OLD_JOINT_CAP

U_PAID_BEFORE = c5_owner.U_PAID_AFTER
B_REMAINING_BEFORE = c5_owner.B_REMAINING_AFTER
U_PAID_AFTER = U_PAID_BEFORE + LEDGER_MOVEMENT
B_REMAINING_AFTER = tangent.B_STAR - U_PAID_AFTER

CUTOFF_D = c5_owner.CUTOFF_D
EXPECTED_TAIL_TARGET = 17_907_568_905_216
EXPECTED_E_MAX = int(
    "5284446868708864089047283796538880969739059774"
)
EXPECTED_K_REMAINING = 4_807_520
EXPECTED_BREAK_J = 166

SOURCE_OWNER_ID = "source_mobius_full_outside_maximal_gcd"
PAID_TERMINAL = "PAID_PAIR_GLOBAL_SOURCE_MOBIUS_MAXIMAL_GCD"

FIRST_MATCH_ORDER = list(c5_owner.NEW_FIRST_MATCH_ORDER)
_C5_INDEX = FIRST_MATCH_ORDER.index("projective_base_pair_C5")
FIRST_MATCH_ORDER.insert(_C5_INDEX + 1, SOURCE_OWNER_ID)

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessors",
    "counted_object_contract",
    "pair_global_source_contract",
    "source_mobius_owner",
    "cross_selector_containment",
    "first_match_partition",
    "joint_owner_theorem",
    "selector_restart",
    "exact_control",
    "ledger",
    "rank9_updated_gate",
    "residual_route_cuts",
    "scope_guards",
    "nonclaims",
    "source_bindings",
    "payload_sha256",
}


class ContractError(RuntimeError):
    """Raised for parser, source, semantic, or exact-arithmetic drift."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def exact_int(value: object, label: str) -> int:
    require(type(value) is int, f"{label} is not an exact integer")
    return int(value)


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
        source_binding("proof-note", NOTE_REL, "pair-global theorem and ledger splice"),
        source_binding("python-verifier", SCRIPT_REL, "certificate, arithmetic, and mutations"),
        source_binding(
            "sage-control",
            SAGE_REL,
            "selector-carrier-proxy and edge-case exact controls",
        ),
        source_binding("readme", README_REL, "replay and scope contract"),
        source_binding("sync-note", sync.NOTE_REL, "same-selector synchronization predecessor"),
        source_binding(
            "sync-certificate",
            sync.CERT_PATH.relative_to(ROOT),
            "synchronization predecessor fingerprint",
        ),
        source_binding("sync-verifier", sync.SCRIPT_REL, "anchor and moving-root semantics"),
        source_binding("sync-sage", sync.SAGE_REL, "predecessor exact projective control"),
        source_binding("c5-note", c5_owner.NOTE_REL, "C5/base case maximum"),
        source_binding(
            "c5-certificate",
            c5_owner.CERT_PATH.relative_to(ROOT),
            "current ledger fingerprint",
        ),
        source_binding("c5-verifier", c5_owner.SCRIPT_REL, "joint-block semantics"),
        source_binding("tangent-note", tangent.NOTE_REL, "fixed-translation owner restart"),
        source_binding(
            "tangent-certificate",
            tangent.CERT_PATH.relative_to(ROOT),
            "first-match restart fingerprint",
        ),
        source_binding("tangent-verifier", tangent.PYTHON_REL, "selector restart semantics"),
    ]


def validate_predecessors() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    sync_doc = sync.load_json(sync.CERT_PATH)
    sync.validate_certificate(sync_doc)
    require(sync_doc["payload_sha256"] == SYNC_PAYLOAD, "#960 payload drift")

    c5_doc = c5_owner.load_json(c5_owner.CERT_PATH)
    c5_owner.validate_certificate(c5_doc)
    require(c5_doc["payload_sha256"] == C5_PAYLOAD, "C5 payload drift")

    tangent_doc = tangent.load_json(tangent.CERT_PATH)
    tangent.verify_semantics(tangent_doc)
    require(tangent_doc["payload_sha256"] == TANGENT_PAYLOAD, "tangent payload drift")
    return sync_doc, c5_doc, tangent_doc


def validate_consumed_facts(
    sync_doc: dict[str, Any],
    c5_doc: dict[str, Any],
    tangent_doc: dict[str, Any],
) -> None:
    lemma = sync_doc["synchronization_lemma"]
    require(lemma["same_received_pair"] is True, "received-pair scope drift")
    require(lemma["same_sp3_source_pair"] is True, "source-pair scope drift")
    require(lemma["source_anchor_floor"] == SIGMA_FLOOR, "source floor drift")
    require(lemma["three_distinct_anchors_available"] is True, "three-anchor drift")
    require(lemma["mobius_three_point_rigidity"] is True, "rigidity drift")
    require(lemma["full_gcd_degree"] == "k-2", "full-gcd degree drift")
    require(lemma["coefficient_rank_each_line"] == 2, "coefficient-rank drift")

    moving = sync_doc["noncontainment_moving_root_bridge"]
    require(moving["transversality_forces_F_eta_L_nonempty"] is True, "moving-root drift")
    require(
        moving["moving_root_x_in_W_L_subset_V_subset_D_subset_F_p"] is True,
        "moving-root domain drift",
    )
    require(moving["x_is_not_common_root"] is True, "common-root guard drift")

    provenance = sync_doc["provenance_audit"]
    require(provenance["uniform_local_lemma_proved"] is True, "local lemma drift")
    require(provenance["ledger_payment_authorized"] is False, "predecessor payment drift")
    require(
        provenance["terminal"] == "UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE",
        "predecessor route cut drift",
    )

    c5_joint = c5_doc["joint_owner_theorem"]
    require(c5_joint["rank_zero_noncontained_fiber_empty"] is True, "rank-zero guard drift")
    require(c5_joint["case_combination"] == "MAXIMUM_NOT_SUM", "C5 maximum drift")
    require(c5_joint["projective_base_pair_C5_cap"] == str(P + 1), "C5 cap drift")
    require(c5_joint["residual_base_slope_cap_when_C5_empty"] == str(P), "base cap drift")
    require(c5_joint["replaces_existing_base_block"] is True, "replacement drift")
    require(c5_joint["adds_second_independent_block"] is False, "addition guard drift")

    counted = tangent_doc["counted_object_contract"]
    require(counted["sp3_one_translation_fixed_for_entire_received_pair"] is True, "SP3 drift")
    require(counted["alternative_translation_union_forbidden"] is True, "translation guard drift")
    partition = tangent_doc["first_match_partition"]
    require(partition["incoming_exact_residual_required"] is True, "incoming residual drift")
    require(partition["later_owners_receive_exact_set_difference"] is True, "deletion drift")
    residual = tangent_doc["residual_selector_contract"]
    require(residual["complete_selector_universe_must_be_rebuilt"] is True, "restart drift")
    require(residual["affine_rank_minimizer_must_be_recomputed"] is True, "rank restart drift")
    require(residual["same_sp3_translation_required_downstream"] is True, "translation restart drift")


def exact_rank9_update() -> dict[str, Any]:
    gate = tangent.one_cut_gate(B_REMAINING_AFTER, CUTOFF_D, N, 1)
    tail = int(gate["largest_sufficient_low_deficit_cap_T_star"])
    e_max = tangent.aggregate_excess_max(tail)
    k_remaining = tangent.exact_k_remaining(B_REMAINING_AFTER)
    maximal_binomial = math.comb(K - 2, 8)
    break_j = tangent.UNIFORM_CAP + e_max // maximal_binomial + 1
    require(tail == EXPECTED_TAIL_TARGET, "tail target drift")
    require(e_max == EXPECTED_E_MAX, "E_max drift")
    require(k_remaining == EXPECTED_K_REMAINING, "K_remaining drift")
    require(break_j == EXPECTED_BREAK_J, "break J drift")
    return {
        "cutoff_D": CUTOFF_D,
        "old_tail_target": str(c5_owner.NEW_TAIL_TARGET),
        "new_tail_target": str(tail),
        "tail_target_drop": str(c5_owner.NEW_TAIL_TARGET - tail),
        "old_aggregate_excess_max": str(c5_owner.NEW_E_MAX),
        "new_aggregate_excess_max": str(e_max),
        "aggregate_excess_drop": str(c5_owner.NEW_E_MAX - e_max),
        "K_remaining": k_remaining,
        "maximal_gcd_break_J": break_j,
        "gate": gate,
    }


_EXPECTED_CACHE: dict[str, Any] | None = None


def expected_certificate() -> dict[str, Any]:
    global _EXPECTED_CACHE
    if _EXPECTED_CACHE is not None:
        return copy.deepcopy(_EXPECTED_CACHE)

    sync_doc, c5_doc, tangent_doc = validate_predecessors()
    validate_consumed_facts(sync_doc, c5_doc, tangent_doc)
    note_text = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        PAID_TERMINAL,
        "UNPAID_NO_COMPATIBLE_SOURCE_MOBIUS_RECORD",
        "UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP",
        "UNBOUND_POST_TANGENT_SOURCE_LOAD",
    ):
        require(token in note_text, f"proof-note terminal missing: {token}")

    stale_fields = list(
        tangent_doc["residual_selector_contract"]["stale_fields_forbidden"]
    )
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "extension_degree": tangent.EXTENSION_DEGREE,
            "q_line": str(P**tangent.EXTENSION_DEGREE),
            "n": N,
            "k": K,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
            "rich_uniform_cap": tangent.UNIFORM_CAP,
        },
        "predecessors": {
            "maximal_gcd_synchronization": "payload-sha256:" + SYNC_PAYLOAD,
            "projective_base_pair_c5_owner": "payload-sha256:" + C5_PAYLOAD,
            "tangent_owner_splice": "payload-sha256:" + TANGENT_PAYLOAD,
        },
        "counted_object_contract": {
            "object": "distinct support-wise MCA-bad finite slopes of one received pair",
            "charge_scope": "FIRST_MATCH_GLOBAL_ONCE_PER_RECEIVED_PAIR",
            "cross_received_pair_union_required": False,
            "selectors_are_unioned_only_at_slope_set_level": True,
            "per_selector_charge_forbidden": True,
            "determinant_atlas_mass_cross_selector_mixing_forbidden": True,
            "witness_support_line_chart_and_basis_counts_forbidden": True,
            "projective_infinity_is_not_a_finite_slope": True,
        },
        "pair_global_source_contract": {
            "fixed_received_pair": True,
            "fixed_sp3_translation": True,
            "alternative_translation_union_forbidden": True,
            "source_pair": "(epsilon_0,epsilon_1)",
            "Sigma": "supp(epsilon_0) UNION supp(epsilon_1) subseteq D",
            "source_label": "lambda(h)=[-epsilon_0(h):epsilon_1(h)]",
            "source_label_nonzero_on_Sigma": True,
            "source_anchor_floor_formula": "t-floor(j/20)+2",
            "rich_x_max": RICH_X_MAX,
            "source_anchor_floor": SIGMA_FLOOR,
            "pair_global_fields_survive_selector_restart": [
                "epsilon_0",
                "epsilon_1",
                "Sigma",
            ],
        },
        "source_mobius_owner": {
            "owner_id": SOURCE_OWNER_ID,
            "owner_is_intrinsic_not_chosen_from_selector": True,
            "compatibility_condition": (
                "|Sigma|>=18419 and exactly one phi in PGL2(F) matches all source labels"
            ),
            "unique_map_for_three_or_more_anchors": True,
            "incompatible_or_small_source_owner_is_empty": True,
            "nonempty_owner_without_compatible_map_forbidden": True,
            "domain": "D SETMINUS Sigma",
            "using_all_D_forbidden": True,
            "finite_image": (
                "M={eta in F: [eta:1]=phi([x:1]) for some x in D SETMINUS Sigma}"
            ),
            "assigned_cell": "Z_SMob=Gamma_in INTERSECT M",
            "outgoing_cell": "Gamma_out=Gamma_in SETMINUS Z_SMob",
            "actual_cap_formula": "|M|<=n-|Sigma|",
            "uniform_cap_formula": "n-18419",
            "uniform_cap": SOURCE_MOBIUS_CAP,
            "earlier_overlap_removed": True,
            "later_overlap_deleted_exactly": True,
        },
        "cross_selector_containment": {
            "quantifier": "all source-bound complete selectors and all qualifying lines",
            "same_carrier_across_selectors_required": False,
            "full_outside_each_selector": "V_sigma INTERSECT Sigma is empty",
            "coefficient_rank_each_line": 2,
            "full_monic_gcd_degree": "k-2",
            "contributing_beta_positive": True,
            "contributing_J_at_least": 21,
            "contributing_x_at_most": RICH_X_MAX,
            "source_rank_two_floor_each_line": "|Sigma|>=t-x_L+2",
            "anchor_equality_each_line": (
                "phi_sigma_L([h:1])=[-epsilon_0(h):epsilon_1(h)] for all h in Sigma"
            ),
            "three_point_rigidity_across_selectors": True,
            "all_qualifying_maps_common": True,
            "moving_root_x_in_W_subset_V_subset_D_minus_Sigma": True,
            "moving_root_is_not_common_root": True,
            "selected_finite_slope_equals_common_phi_of_x": True,
            "union_containment": (
                "UNION_sigma UNION_L Gamma_sigma_L_fin subseteq M(epsilon_0,epsilon_1)"
            ),
            "no_qualifying_record_if_compatibility_fails": True,
            "selector_inventory_or_Route_S_U_C_required": False,
            "determinant_weights_transferred_across_selectors": False,
        },
        "first_match_partition": {
            "order": FIRST_MATCH_ORDER,
            "projective_base_pair_C5_index_one_based": FIRST_MATCH_ORDER.index(
                "projective_base_pair_C5"
            )
            + 1,
            "source_mobius_index_one_based": FIRST_MATCH_ORDER.index(SOURCE_OWNER_ID) + 1,
            "residual_extension_index_one_based": FIRST_MATCH_ORDER.index(
                "residual_extension_valued_strata"
            )
            + 1,
            "residual_base_index_one_based": FIRST_MATCH_ORDER.index(
                "residual_base_slope_universe"
            )
            + 1,
            "incoming_exact_residual_required": True,
            "earlier_owner_intersection_removed": True,
            "later_owners_receive_exact_set_difference": True,
            "owner_may_delete_bounded_slopes_without_qualifying_record": True,
            "later_uniform_caps_valid_on_smaller_residual": True,
        },
        "joint_owner_theorem": {
            "rank_zero_noncontained_exact_witness_residual_empty": True,
            "positive_rank_cases_exhaustive": True,
            "base_projective_case_condition": "rank(Y_R)>0 and F_proj(R)=F_p",
            "base_projective_case_C5_owns_all_post5_slopes": True,
            "base_projective_case_later_cells_empty": True,
            "base_projective_case_cap": str(C5_BASE_CASE_CAP),
            "nonbase_case_condition": "rank(Y_R)>0 and F_proj(R)!=F_p",
            "nonbase_case_C5_cell_empty": True,
            "nonbase_source_mobius_cap": str(SOURCE_MOBIUS_CAP),
            "nonbase_later_residual_base_cap": str(P),
            "source_and_later_base_disjoint_by_exact_deletion": True,
            "nonbase_case_cap": str(NONBASE_SOURCE_BASE_CASE_CAP),
            "case_combination": "MAXIMUM_NOT_SUM",
            "joint_cap_formula": "max(p+1,p+n-18419)=p+n-18419",
            "joint_uniform_cap": str(NEW_JOINT_CAP),
            "old_joint_cap": str(OLD_JOINT_CAP),
            "replaces_existing_joint_block": True,
            "adds_independent_joint_block": False,
        },
        "selector_restart": {
            "complete_selector_restriction_certifies_nonempty_new_universe": True,
            "old_rank9_selector_restricts_to_rank_at_most_9": True,
            "rank_at_least_10_can_be_new_minimum": False,
            "later_pair_global_owner_cells_applied_to_exact_outgoing_set": True,
            "complete_selector_universe_must_be_rebuilt": True,
            "restart_order": list(tangent.RESTART_ORDER),
            "global_carrier_gate_must_be_rerun": True,
            "small_family_gate_must_be_rerun": True,
            "affine_rank_minimizer_must_be_recomputed": True,
            "stale_selector_fields_forbidden": stale_fields,
            "same_sp3_translation_required_downstream": True,
            "low_carrier_cap": str(tangent.LOW_CARRIER_CAP),
            "low_carrier_post_charge_margin": str(
                tangent.B_STAR - U_PAID_AFTER - tangent.LOW_CARRIER_CAP
            ),
            "small_family_cap": tangent.SMALL_FAMILY_CAP,
            "rank_le_3_cap": str(tangent.RANK_LE_3_CAP),
            "rank_le_3_post_charge_margin": str(
                tangent.B_STAR - U_PAID_AFTER - tangent.RANK_LE_3_CAP
            ),
            "rank_4_to_8_cap": str(tangent.RANK_4_TO_8_CAP),
            "rank_4_to_8_post_charge_margin": str(
                tangent.B_STAR - U_PAID_AFTER - tangent.RANK_4_TO_8_CAP
            ),
            "rank_caps_are_alternatives_not_sum": True,
            "rank9_coarse_gate_must_be_replayed": True,
        },
        "exact_control": {
            "field": "GF(5^6)",
            "base_field": "GF(5)",
            "toy_domain_size": 5,
            "source_anchor_count": 3,
            "outside_domain_count": 2,
            "selector_carrier_proxy_count": 2,
            "distinct_selector_carrier_proxies": True,
            "carriers_disjoint_from_Sigma": True,
            "complete_selector_witness_assignment_constructed": False,
            "rich_beta_J_predicates_constructed": False,
            "distinct_nonbase_full_gcd_factors": 2,
            "maximal_gcd_degree": 4,
            "same_source_labels": True,
            "same_reduced_mobius_map": True,
            "cross_proxy_selected_finite_union": 2,
            "source_mobius_finite_image_size": 2,
            "cross_proxy_union_contained": True,
            "different_source_map_proxy_differs": True,
            "different_source_map_proxy_union_size": 4,
            "different_source_map_proxy_union_exceeds_owner_cap": True,
            "proxy_is_not_claimed_as_two_valid_same_pair_sp3_translations": True,
            "two_anchor_countercontrol_intersection": 2,
            "two_anchor_countercontrol_union": 10,
            "repeated_source_label_incompatible_with_PGL2": True,
            "root_in_Sigma_excluded_from_D_minus_Sigma_image": True,
            "pole_control_finite_images": 1,
            "pole_control_projective_infinity_images": 1,
            "scale": "EXACT_TOY_CONTROL_NOT_DEPLOYED_CENSUS_OR_PROOF",
        },
        "ledger": {
            "B_star": str(tangent.B_STAR),
            "old_joint_C5_base_cap": str(OLD_JOINT_CAP),
            "new_joint_C5_source_mobius_base_cap": str(NEW_JOINT_CAP),
            "replacement_not_addition": True,
            "source_mobius_uniform_cap": str(SOURCE_MOBIUS_CAP),
            "ledger_movement": str(LEDGER_MOVEMENT),
            "U_paid_before": str(U_PAID_BEFORE),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "full_outside_maximal_gcd_cell_deleted_before_residual_U_A": True,
            "U_Q": None,
            "residual_U_A": None,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "rank9_updated_gate": exact_rank9_update(),
        "residual_route_cuts": [
            {
                "terminal": "UNPAID_NO_COMPATIBLE_SOURCE_MOBIUS_RECORD",
                "condition": "slope survives the intrinsic source-Mobius owner",
                "reason": "no compatible full-outside maximal-gcd source-Mobius record can own it",
            },
            {
                "terminal": "UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP",
                "condition": "deg gcd(P_L,Q_L)<k-2",
                "reason": "the gcd-reduced map can have degree greater than one",
            },
            {
                "terminal": "UNBOUND_POST_TANGENT_SOURCE_LOAD",
                "condition": "non-full-outside and other source-load cells",
                "reason": "the pair-global theorem uses V_sigma INTERSECT Sigma empty",
            },
        ],
        "scope_guards": {
            "pair_global_source_mobius_owner_proved": True,
            "cross_selector_slope_union_proved": True,
            "first_match_splice_proved": True,
            "full_outside_maximal_gcd_cell_paid": True,
            "complete_selector_inventory_required_for_this_cell": False,
            "general_lower_gcd_payment_proved": False,
            "non_full_outside_source_load_paid": False,
            "determinant_weighted_incidence_paid": False,
            "U_Q_determined": False,
            "residual_U_A_determined": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": [
            "No alternative SP3 translations or received pairs are unioned.",
            "No per-selector charge is taken and no determinant mass is mixed across selectors.",
            "No pair-global base-field descent is asserted; the common map is in PGL2(F).",
            "No selector, support, line, chart, basis, witness, or coordinate multiplicity is counted.",
            "No complete-selector inventory or deployed terminal census is invented.",
            "No lower-gcd rational map or non-full-outside source-load cell is paid.",
            "No exact toy control is promoted to deployed-field evidence or theorem proof.",
            "No value is assigned to U_Q or residual U_A.",
            "The KoalaBear row remains open.",
            "Rank at least ten, Lean, and stable-paper promotion remain unauthorized.",
        ],
        "source_bindings": expected_source_bindings(),
        "payload_sha256": "",
    }
    result["payload_sha256"] = payload_hash(result)
    _EXPECTED_CACHE = copy.deepcopy(result)
    return result


def strict_match(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type mismatch at {path}")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"key mismatch at {path}")
        for key in expected:
            strict_match(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"length mismatch at {path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            strict_match(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"value mismatch at {path}")


def validate_certificate(document: dict[str, Any]) -> None:
    require(set(document) == TOP_KEYS, "top-level key set drift")
    require(document.get("payload_sha256") == payload_hash(document), "payload hash mismatch")
    strict_match(document, expected_certificate())


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def mutation_cases() -> list[Mutation]:
    return [
        ("schema", lambda d: d.__setitem__("schema", SCHEMA + "-mutated")),
        ("status", lambda d: d.__setitem__("status", "ROW_CLOSED")),
        ("row-p", lambda d: d["row"].__setitem__("p", P + 1)),
        ("predecessor-960", lambda d: d["predecessors"].__setitem__("maximal_gcd_synchronization", "payload-sha256:" + "0" * 64)),
        ("predecessor-c5", lambda d: d["predecessors"].__setitem__("projective_base_pair_c5_owner", "payload-sha256:" + "0" * 64)),
        ("predecessor-tangent", lambda d: d["predecessors"].__setitem__("tangent_owner_splice", "payload-sha256:" + "0" * 64)),
        ("per-selector-charge", lambda d: d["counted_object_contract"].__setitem__("per_selector_charge_forbidden", False)),
        ("mix-determinant-mass", lambda d: d["counted_object_contract"].__setitem__("determinant_atlas_mass_cross_selector_mixing_forbidden", False)),
        ("infinity-finite", lambda d: d["counted_object_contract"].__setitem__("projective_infinity_is_not_a_finite_slope", False)),
        ("alternative-translation", lambda d: d["pair_global_source_contract"].__setitem__("alternative_translation_union_forbidden", False)),
        ("source-label-zero", lambda d: d["pair_global_source_contract"].__setitem__("source_label_nonzero_on_Sigma", False)),
        ("source-floor", lambda d: d["pair_global_source_contract"].__setitem__("source_anchor_floor", SIGMA_FLOOR - 1)),
        ("chosen-selector-map", lambda d: d["source_mobius_owner"].__setitem__("owner_is_intrinsic_not_chosen_from_selector", False)),
        ("only-two-anchors", lambda d: d["source_mobius_owner"].__setitem__("unique_map_for_three_or_more_anchors", False)),
        ("nonempty-incompatible", lambda d: d["source_mobius_owner"].__setitem__("nonempty_owner_without_compatible_map_forbidden", False)),
        ("use-all-D", lambda d: d["source_mobius_owner"].__setitem__("domain", "D")),
        ("wrong-source-cap", lambda d: d["source_mobius_owner"].__setitem__("uniform_cap", SOURCE_MOBIUS_CAP + 1)),
        ("no-residual-intersection", lambda d: d["source_mobius_owner"].__setitem__("assigned_cell", "Z_SMob=M")),
        ("no-exact-delete", lambda d: d["source_mobius_owner"].__setitem__("later_overlap_deleted_exactly", False)),
        ("same-carrier-required", lambda d: d["cross_selector_containment"].__setitem__("same_carrier_across_selectors_required", True)),
        ("full-outside-false", lambda d: d["cross_selector_containment"].__setitem__("full_outside_each_selector", "V_sigma INTERSECT Sigma nonempty")),
        ("gcd-degree", lambda d: d["cross_selector_containment"].__setitem__("full_monic_gcd_degree", "k-3")),
        ("rank-one", lambda d: d["cross_selector_containment"].__setitem__("coefficient_rank_each_line", 1)),
        ("beta-zero", lambda d: d["cross_selector_containment"].__setitem__("contributing_beta_positive", False)),
        ("x-too-large", lambda d: d["cross_selector_containment"].__setitem__("contributing_x_at_most", RICH_X_MAX + 1)),
        ("maps-not-common", lambda d: d["cross_selector_containment"].__setitem__("all_qualifying_maps_common", False)),
        ("root-in-Sigma", lambda d: d["cross_selector_containment"].__setitem__("moving_root_x_in_W_subset_V_subset_D_minus_Sigma", False)),
        ("common-root", lambda d: d["cross_selector_containment"].__setitem__("moving_root_is_not_common_root", False)),
        ("selector-inventory-required", lambda d: d["cross_selector_containment"].__setitem__("selector_inventory_or_Route_S_U_C_required", True)),
        ("owner-order", lambda d: d["first_match_partition"]["order"].reverse()),
        ("owner-index", lambda d: d["first_match_partition"].__setitem__("source_mobius_index_one_based", 9)),
        ("later-not-difference", lambda d: d["first_match_partition"].__setitem__("later_owners_receive_exact_set_difference", False)),
        ("sum-cases", lambda d: d["joint_owner_theorem"].__setitem__("case_combination", "SUM")),
        ("rank-zero-nonempty", lambda d: d["joint_owner_theorem"].__setitem__("rank_zero_noncontained_exact_witness_residual_empty", False)),
        ("C5-not-empty", lambda d: d["joint_owner_theorem"].__setitem__("nonbase_case_C5_cell_empty", False)),
        ("source-base-overlap", lambda d: d["joint_owner_theorem"].__setitem__("source_and_later_base_disjoint_by_exact_deletion", False)),
        ("wrong-joint-cap", lambda d: d["joint_owner_theorem"].__setitem__("joint_uniform_cap", str(NEW_JOINT_CAP + 1))),
        ("add-block", lambda d: d["joint_owner_theorem"].__setitem__("adds_independent_joint_block", True)),
        ("not-replacement", lambda d: d["joint_owner_theorem"].__setitem__("replaces_existing_joint_block", False)),
        ("no-selector-restart", lambda d: d["selector_restart"].__setitem__("complete_selector_universe_must_be_rebuilt", False)),
        ("stale-selector-fields", lambda d: d["selector_restart"].__setitem__("stale_selector_fields_forbidden", [])),
        ("translation-recomputed", lambda d: d["selector_restart"].__setitem__("same_sp3_translation_required_downstream", False)),
        ("rank10-minimum", lambda d: d["selector_restart"].__setitem__("rank_at_least_10_can_be_new_minimum", True)),
        ("rank-sum", lambda d: d["selector_restart"].__setitem__("rank_caps_are_alternatives_not_sum", False)),
        ("toy-deployed", lambda d: d["exact_control"].__setitem__("scale", "DEPLOYED_PROOF")),
        ("toy-complete-selector", lambda d: d["exact_control"].__setitem__("complete_selector_witness_assignment_constructed", True)),
        ("toy-different-source-map-union", lambda d: d["exact_control"].__setitem__("different_source_map_proxy_union_size", 2)),
        ("old-joint", lambda d: d["ledger"].__setitem__("old_joint_C5_base_cap", str(P))),
        ("ledger-addition", lambda d: d["ledger"].__setitem__("replacement_not_addition", False)),
        ("ledger-movement", lambda d: d["ledger"].__setitem__("ledger_movement", str(SOURCE_MOBIUS_CAP))),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("B-remaining", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_AFTER - 1))),
        ("UQ-zero", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("UA-zero", lambda d: d["ledger"].__setitem__("residual_U_A", 0)),
        ("tail", lambda d: d["rank9_updated_gate"].__setitem__("new_tail_target", str(EXPECTED_TAIL_TARGET + 1))),
        ("Emax", lambda d: d["rank9_updated_gate"].__setitem__("new_aggregate_excess_max", str(EXPECTED_E_MAX + 1))),
        ("Kremaining", lambda d: d["rank9_updated_gate"].__setitem__("K_remaining", EXPECTED_K_REMAINING + 1)),
        ("break-J", lambda d: d["rank9_updated_gate"].__setitem__("maximal_gcd_break_J", EXPECTED_BREAK_J + 1)),
        ("lower-gcd-closed", lambda d: d["scope_guards"].__setitem__("general_lower_gcd_payment_proved", True)),
        ("non-full-outside-closed", lambda d: d["scope_guards"].__setitem__("non_full_outside_source_load_paid", True)),
        ("rank9-closed", lambda d: d["scope_guards"].__setitem__("complete_rank9_payment_proved", True)),
        ("row-closed", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("rank10", lambda d: d["scope_guards"].__setitem__("rank_at_least_ten_authorized", True)),
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
    print(f"M1 source-Mobius owner mutations: {total}/{total} PASS")
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
    print("M1 pair-global source-Mobius owner splice: PASS")
    print(
        "  owner cap: n-18,419 = "
        f"{SOURCE_MOBIUS_CAP:,}; cross-selector slope union only"
    )
    print(
        "  joint C5/source/base cap: "
        f"{OLD_JOINT_CAP:,} -> {NEW_JOINT_CAP:,} (MAXIMUM_NOT_SUM)"
    )
    print(f"  ledger movement: {LEDGER_MOVEMENT:,}")
    print(f"  U_paid: {U_PAID_BEFORE:,} -> {U_PAID_AFTER:,}")
    print(f"  B_remaining: {B_REMAINING_BEFORE:,} -> {B_REMAINING_AFTER:,}")
    print(f"  T_18,014: {EXPECTED_TAIL_TARGET:,}; break J={EXPECTED_BREAK_J}")
    print(f"  terminal paid: {PAID_TERMINAL}")
    print("  lower-gcd/non-full-outside/U_Q/U_A remain open; row YELLOW")
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
