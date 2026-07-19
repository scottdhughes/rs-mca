#!/usr/bin/env python3
"""Verify the KoalaBear one-slack common-twist source-subline owner.

The companion theorem closes only the r=1, (h,u,ell)=(1,0,0) nonbase
common-linear-gcd component.  It charges one pair-global projective
F_p-subline, deletes its exact incoming intersection, and restarts selectors.
The moving-cofactor component, U_Q, residual U_A, and the row remain open.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_source_mobius_owner_splice_v1 as ledger_base


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-one-slack-twist-subline-owner-v1"
ARTIFACT_KIND = "M1_KB_RANK9_ONE_SLACK_COMMON_TWIST_SOURCE_SUBLINE_OWNER"
STATUS = (
    "PROVED_LOCAL_PAIR_GLOBAL_SOURCE_SUBLINE_OWNER_"
    "COMMON_FACTOR_ONE_SLACK_COMPONENT_CLOSED_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-one-slack-twist-subline-owner-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_one_slack_twist_subline_owner_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_one_slack_twist_subline_owner_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-one-slack-twist-subline-owner-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_one_slack_twist_subline_owner_v1.sage"
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
PROJECTIVE_FIELD_NOTE_REL = Path(
    "experimental/notes/thresholds/projective_syndrome_c5_first_match.md"
)

P = ledger_base.P
N = ledger_base.N
K = ledger_base.K
A = ledger_base.A
J = ledger_base.J
T = ledger_base.T
EXTENSION_DEGREE = ledger_base.tangent.EXTENSION_DEGREE
RICH_X_MAX = ledger_base.RICH_X_MAX
CUTOFF_D = ledger_base.CUTOFF_D

SOURCE_SIZE = T + 2
REDUCED_DEGREE_MIN = (SOURCE_SIZE + 1) // 2
SOURCE_BLOCK_MIN = SOURCE_SIZE - RICH_X_MAX
PROJECTIVE_SUBLINE_SIZE = P + 1
OWNER_CAP = P - 1

U_PAID_BEFORE = ledger_base.U_PAID_AFTER
B_REMAINING_BEFORE = ledger_base.B_REMAINING_AFTER
B_STAR = ledger_base.tangent.B_STAR
LEDGER_MOVEMENT = OWNER_CAP
U_PAID_AFTER = U_PAID_BEFORE + LEDGER_MOVEMENT
B_REMAINING_AFTER = B_STAR - U_PAID_AFTER

EXPECTED_TAIL_TARGET = 17_905_060_408_872
EXPECTED_E_MAX = int(
    "5257709828544841979217262061165603756190013974"
)
EXPECTED_K_REMAINING = 4_807_520
EXPECTED_BREAK_J = 166

SOURCE_RATIONAL_OWNER = "source_rational_full_outside_bounded_degree"
TWIST_OWNER_ID = "source_subline_common_linear_gcd_twist"
PAID_TERMINAL = "PAID_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST"
CLOSED_TERMINAL = "UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST"
OPEN_TERMINAL = "UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR"

FIRST_MATCH_ORDER = list(ledger_base.FIRST_MATCH_ORDER)
old_index = FIRST_MATCH_ORDER.index(ledger_base.SOURCE_OWNER_ID)
FIRST_MATCH_ORDER[old_index] = SOURCE_RATIONAL_OWNER
FIRST_MATCH_ORDER.insert(old_index + 1, TWIST_OWNER_ID)

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessors",
    "one_slack_record",
    "source_subline_geometry",
    "source_label_partition",
    "two_label_frobenius_fingerprint",
    "pair_global_owner",
    "first_match_partition",
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
        source_binding("proof-note", NOTE_REL, "source-subline owner theorem and splice"),
        source_binding("python-verifier", SCRIPT_REL, "certificate, arithmetic, and mutations"),
        source_binding("sage-control", SAGE_REL, "three-label and two-label exact controls"),
        source_binding("readme", README_REL, "replay and scope contract"),
        source_binding("moving-slack-note", MOVING_NOTE_REL, "one-slack common-factor predecessor"),
        source_binding("moving-slack-sage", MOVING_SAGE_REL, "predecessor exact toy interface"),
        source_binding("source-rational-note", SOURCE_RATIONAL_NOTE_REL, "subset-stable earlier owner"),
        source_binding("source-rational-sage", SOURCE_RATIONAL_SAGE_REL, "earlier owner edge controls"),
        source_binding("rich-pencil-note", RICH_ATLAS_NOTE_REL, "moving-set and rich-line identities"),
        source_binding("projective-field-note", PROJECTIVE_FIELD_NOTE_REL, "C5 and subline distinction"),
        source_binding(
            "ledger-predecessor-certificate",
            ledger_base.CERT_PATH.relative_to(ROOT),
            "banked exact ledger and restart arithmetic",
        ),
        source_binding("ledger-predecessor-verifier", ledger_base.SCRIPT_REL, "banked ledger semantics"),
    ]


def validate_predecessors() -> None:
    predecessor = ledger_base.load_json(ledger_base.CERT_PATH)
    ledger_base.validate_certificate(predecessor)
    require(
        predecessor["ledger"]["U_paid_after"] == str(U_PAID_BEFORE),
        "banked U_paid drift",
    )
    require(
        predecessor["ledger"]["B_remaining_after"] == str(B_REMAINING_BEFORE),
        "banked remaining budget drift",
    )

    moving = (ROOT / MOVING_NOTE_REL).read_text(encoding="utf-8")
    for token in (
        "(h,u,\\ell)=(1,0,0)",
        CLOSED_TERMINAL,
        OPEN_TERMINAL,
        "s\\ge67{,}474",
        "e\\ge33{,}737",
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
    gate = ledger_base.tangent.one_cut_gate(B_REMAINING_AFTER, CUTOFF_D, N, 1)
    tail = int(gate["largest_sufficient_low_deficit_cap_T_star"])
    e_max = ledger_base.tangent.aggregate_excess_max(tail)
    k_remaining = ledger_base.tangent.exact_k_remaining(B_REMAINING_AFTER)
    maximal_binomial = math.comb(K - 2, 8)
    break_j = ledger_base.tangent.UNIFORM_CAP + e_max // maximal_binomial + 1
    require(tail == EXPECTED_TAIL_TARGET, "tail target drift")
    require(e_max == EXPECTED_E_MAX, "aggregate excess maximum drift")
    require(k_remaining == EXPECTED_K_REMAINING, "K_remaining drift")
    require(break_j == EXPECTED_BREAK_J, "break J drift")
    return {
        "cutoff_D": CUTOFF_D,
        "old_tail_target": str(ledger_base.EXPECTED_TAIL_TARGET),
        "new_tail_target": str(tail),
        "tail_target_drop": str(ledger_base.EXPECTED_TAIL_TARGET - tail),
        "new_aggregate_excess_max": str(e_max),
        "K_remaining": k_remaining,
        "maximal_gcd_break_J": break_j,
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
        "rho _1(h)^{p-1}",
        "source_subline_common_linear_gcd_twist",
    ):
        require(token in note, f"proof-note token missing: {token}")

    stale_fields = list(
        ledger_base.tangent_doc_for_restart()["residual_selector_contract"][
            "stale_fields_forbidden"
        ]
    ) if hasattr(ledger_base, "tangent_doc_for_restart") else list(
        ledger_base.expected_certificate()["selector_restart"][
            "stale_selector_fields_forbidden"
        ]
    )

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
        },
        "predecessors": {
            "source_rational_owner": SOURCE_RATIONAL_NOTE_REL.as_posix(),
            "moving_root_slack_c5_boundary": MOVING_NOTE_REL.as_posix(),
            "banked_ledger_payload": "payload-sha256:"
            + ledger_base.load_json(ledger_base.CERT_PATH)["payload_sha256"],
            "curated_upstream_omits_source_rational_and_moving_json": True,
        },
        "one_slack_record": {
            "scope": "full-outside coefficient-rank-two rich record after C5 and source-rational restart",
            "source_size_s": SOURCE_SIZE,
            "slack_r": 1,
            "slack_tuple_h_u_ell": [1, 0, 0],
            "reduced_degree_e_equals_x": True,
            "reduced_degree_x_min": REDUCED_DEGREE_MIN,
            "reduced_degree_x_max": RICH_X_MAX,
            "all_selected_deficits_zero": True,
            "full_gcd": "H=L_C*(X-zeta)",
            "zeta_nonbase": True,
            "base_zeta_already_C5_owned": True,
            "selected_rich_slopes_at_least": 21,
            "moving_member_identity": "Pbar+eta*Qbar=kappa_eta*L_F_eta",
            "moving_locators_monic_base_degree_x": True,
            "two_members_give_base_polynomial_basis": True,
        },
        "source_subline_geometry": {
            "reduced_map": "psi=[-Pbar:Qbar]",
            "record_subline": "S_L=PGL2(F)-image of P1(B)",
            "record_subline_size": PROJECTIVE_SUBLINE_SIZE,
            "all_source_labels_on_S_L": True,
            "all_selected_moving_slopes_on_S_L": True,
            "projective_syndrome_field_need_not_be_proper": True,
            "common_factor_alone_not_used_as_C5_descent": True,
        },
        "source_label_partition": {
            "fixed_label_set": "Lambda={[-epsilon_0(h):epsilon_1(h)]:h in Sigma}",
            "one_label_impossible": True,
            "one_label_reason": "nonzero degree-at-most-x fibre polynomial cannot have s>x roots",
            "three_or_more_labels_unique_B_subline": True,
            "three_label_uniqueness_group": "PGL2(B) acts sharply three-transitively",
            "exactly_two_labels_normalized_pair_globally_to": ["0", "infinity"],
            "alternative_normalizations_per_selector_forbidden": True,
            "two_label_block_lower_bound_formula": "s-x",
            "two_label_block_lower_bound": SOURCE_BLOCK_MIN,
            "both_blocks_have_at_least_three_points": True,
        },
        "two_label_frobenius_fingerprint": {
            "normalized_pair_shape": [
                "P'=alpha*L_C*(X-zeta)*U",
                "Q'=beta*L_C*(X-zeta)*V",
            ],
            "U_V_base_polynomials": True,
            "on_zero_block": "rho_1(h)=beta*(h-zeta)*b_h with b_h in B*",
            "fingerprint": "rho_1(h)^(p-1)=beta^(p-1)*(h-zeta^p)/(h-zeta)",
            "fingerprint_nonconstant_because_zeta_nonbase": True,
            "three_points_force_equal_mobius_functions": True,
            "cross_determinant_degree_at_most": 2,
            "both_blocks_at_least_three_required": True,
            "unique_common_nonbase_zeta_required": True,
            "nonzero_constants_c0_cinfinity_required": True,
            "both_constants_in_p_minus_one_power_image_required": True,
            "unique_pole_recovers_zeta": True,
            "kernel_of_p_minus_one_power": "B*",
            "inverse_power_fibres_are_unique_B_star_cosets": True,
            "zero_block_recovers_beta_coset": True,
            "infinity_block_recovers_alpha_coset": True,
            "ratio_coset_recovers_normalized_subline": True,
            "any_failed_existence_uniqueness_block_or_power_condition_gives_empty_owner": True,
            "subline_pair_global_across_selectors": True,
        },
        "pair_global_owner": {
            "owner_id": TWIST_OWNER_ID,
            "owner_intrinsic_to_fixed_source_pair": True,
            "owner_chosen_from_selector_forbidden": True,
            "owner_projective_set": "S_src subseteq P1(F)",
            "assigned_cell": "Z_twist={eta in Gamma_in:[eta:1] in S_src}",
            "outgoing_cell": "Gamma_out=Gamma_in setminus Z_twist",
            "projective_subline_size": PROJECTIVE_SUBLINE_SIZE,
            "finite_slope_cap_after_tangent_deletion": OWNER_CAP,
            "ambient_infinity_not_counted_as_finite_slope": True,
            "p_plus_one_cap_is_sharp_for_nonstandard_affine_subline": True,
            "all_finite_source_labels_deleted_by_earlier_tangent_owner": True,
            "at_least_two_projective_source_labels": True,
            "earlier_overlap_removed_by_exact_incoming_intersection": True,
            "later_overlap_removed_by_exact_deletion": True,
            "subset_stable_for_every_Gamma_subset_Gamma_in": True,
            "post_restart_common_factor_record_impossible": True,
            "paid_terminal": PAID_TERMINAL,
            "closed_terminal": CLOSED_TERMINAL,
        },
        "first_match_partition": {
            "order": FIRST_MATCH_ORDER,
            "C5_index_one_based": FIRST_MATCH_ORDER.index("projective_base_pair_C5") + 1,
            "source_rational_index_one_based": FIRST_MATCH_ORDER.index(SOURCE_RATIONAL_OWNER) + 1,
            "twist_subline_index_one_based": FIRST_MATCH_ORDER.index(TWIST_OWNER_ID) + 1,
            "residual_extension_index_one_based": FIRST_MATCH_ORDER.index("residual_extension_valued_strata") + 1,
            "residual_base_index_one_based": FIRST_MATCH_ORDER.index("residual_base_slope_universe") + 1,
            "incoming_exact_residual_required": True,
            "later_owners_receive_exact_set_difference": True,
            "per_selector_subline_charge_forbidden": True,
            "owner_may_conservatively_delete_bounded_intrinsic_set": True,
        },
        "selector_restart": {
            "complete_selector_restriction_certifies_nonempty_new_universe": True,
            "new_minimum_rank_at_most_old_minimum_rank": True,
            "complete_selector_universe_must_be_rebuilt": True,
            "restart_order": list(ledger_base.tangent.RESTART_ORDER),
            "global_carrier_and_small_family_gates_rerun": True,
            "affine_rank_minimizer_recomputed": True,
            "stale_selector_fields_forbidden": stale_fields,
            "same_received_pair_source_and_sp3_translation_downstream": True,
            "all_rank_le_9_terminals_replayed_in_frozen_order": True,
            "rank_at_least_10_not_authorized": True,
        },
        "exact_control": {
            "base_field": "GF(13)",
            "extension_field": "GF(13^2)",
            "toy_row": {"n": 13, "k": 6, "A": 10, "j": 3, "t": 4},
            "one_slack_tuple": [1, 0, 0],
            "source_label_count": 2,
            "source_block_sizes": [3, 3],
            "selected_extension_slopes": 2,
            "moving_witnesses_exact_radius": True,
            "unique_nonbase_pole_candidates": 1,
            "recovered_subline_size": 14,
            "three_label_permutation_checks": 6,
            "three_label_subline_all_affine": True,
            "sage_interface_mutations": 16,
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
            "common_factor_one_slack_component_paid": True,
            "U_Q": None,
            "residual_U_A": None,
            "complete_upper_inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "rank9_updated_gate": exact_rank9_update(),
        "residual_route_cuts": [
            {
                "terminal": OPEN_TERMINAL,
                "condition": "one-slack tuple (h,u,ell)=(0,1,0)",
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
            "common_factor_one_slack_owner_proved": True,
            "common_factor_one_slack_component_closed": True,
            "moving_cofactor_one_slack_component_closed": False,
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
            "No alternative SP3 translation or received pair is unioned.",
            "No per-selector, per-line, support, chart, basis, witness, or determinant multiplicity is charged.",
            "A base-defined reduced pencil is not confused with a base-defined projective syndrome plane.",
            "The exact toy control is not deployed-field evidence or a theorem proof.",
            "The moving-cofactor one-slack component remains open.",
            "No value is assigned to U_Q or residual U_A.",
            "The complete profile envelope and unsafe-side reserve are not compared.",
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
        ("status", lambda d: d.__setitem__("status", "KOALABEAR_CLOSED")),
        ("row-p", lambda d: d["row"].__setitem__("p", P + 1)),
        ("source-size", lambda d: d["one_slack_record"].__setitem__("source_size_s", SOURCE_SIZE - 1)),
        ("slack-tuple", lambda d: d["one_slack_record"].__setitem__("slack_tuple_h_u_ell", [0, 1, 0])),
        ("zeta-base", lambda d: d["one_slack_record"].__setitem__("zeta_nonbase", False)),
        ("too-few-rich", lambda d: d["one_slack_record"].__setitem__("selected_rich_slopes_at_least", 1)),
        ("not-base-locators", lambda d: d["one_slack_record"].__setitem__("moving_locators_monic_base_degree_x", False)),
        ("source-off-subline", lambda d: d["source_subline_geometry"].__setitem__("all_source_labels_on_S_L", False)),
        ("slope-off-subline", lambda d: d["source_subline_geometry"].__setitem__("all_selected_moving_slopes_on_S_L", False)),
        ("force-C5", lambda d: d["source_subline_geometry"].__setitem__("projective_syndrome_field_need_not_be_proper", False)),
        ("one-label-allowed", lambda d: d["source_label_partition"].__setitem__("one_label_impossible", False)),
        ("three-label-not-unique", lambda d: d["source_label_partition"].__setitem__("three_or_more_labels_unique_B_subline", False)),
        ("selector-normalization", lambda d: d["source_label_partition"].__setitem__("alternative_normalizations_per_selector_forbidden", False)),
        ("block-too-small", lambda d: d["source_label_partition"].__setitem__("two_label_block_lower_bound", 2)),
        ("fingerprint-wrong", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("fingerprint", "rho=h-zeta")),
        ("constant-fingerprint", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("fingerprint_nonconstant_because_zeta_nonbase", False)),
        ("four-points", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("three_points_force_equal_mobius_functions", False)),
        ("cross-degree", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("cross_determinant_degree_at_most", 3)),
        ("small-block-accepted", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("both_blocks_at_least_three_required", False)),
        ("nonunique-zeta-accepted", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("unique_common_nonbase_zeta_required", False)),
        ("zero-constant-accepted", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("nonzero_constants_c0_cinfinity_required", False)),
        ("power-image-skipped", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("both_constants_in_p_minus_one_power_image_required", False)),
        ("pole-not-unique", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("unique_pole_recovers_zeta", False)),
        ("wrong-kernel", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("kernel_of_p_minus_one_power", "F*")),
        ("beta-not-recovered", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("zero_block_recovers_beta_coset", False)),
        ("failed-condition-nonempty", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("any_failed_existence_uniqueness_block_or_power_condition_gives_empty_owner", False)),
        ("subline-not-global", lambda d: d["two_label_frobenius_fingerprint"].__setitem__("subline_pair_global_across_selectors", False)),
        ("chosen-owner", lambda d: d["pair_global_owner"].__setitem__("owner_chosen_from_selector_forbidden", False)),
        ("wrong-cap", lambda d: d["pair_global_owner"].__setitem__("finite_slope_cap_after_tangent_deletion", P)),
        ("count-infinity", lambda d: d["pair_global_owner"].__setitem__("ambient_infinity_not_counted_as_finite_slope", False)),
        ("not-subset-stable", lambda d: d["pair_global_owner"].__setitem__("subset_stable_for_every_Gamma_subset_Gamma_in", False)),
        ("record-survives", lambda d: d["pair_global_owner"].__setitem__("post_restart_common_factor_record_impossible", False)),
        ("owner-order", lambda d: d["first_match_partition"]["order"].reverse()),
        ("owner-index", lambda d: d["first_match_partition"].__setitem__("twist_subline_index_one_based", 10)),
        ("per-selector-charge", lambda d: d["first_match_partition"].__setitem__("per_selector_subline_charge_forbidden", False)),
        ("later-not-difference", lambda d: d["first_match_partition"].__setitem__("later_owners_receive_exact_set_difference", False)),
        ("no-restart", lambda d: d["selector_restart"].__setitem__("complete_selector_universe_must_be_rebuilt", False)),
        ("stale-fields", lambda d: d["selector_restart"].__setitem__("stale_selector_fields_forbidden", [])),
        ("rank10", lambda d: d["selector_restart"].__setitem__("rank_at_least_10_not_authorized", False)),
        ("toy-deployed", lambda d: d["exact_control"].__setitem__("deployed_rank9_record_constructed", True)),
        ("toy-poles", lambda d: d["exact_control"].__setitem__("unique_nonbase_pole_candidates", 2)),
        ("toy-cap", lambda d: d["exact_control"].__setitem__("recovered_subline_size", 13)),
        ("ledger-cap", lambda d: d["ledger"].__setitem__("new_owner_cap", str(P))),
        ("ledger-movement", lambda d: d["ledger"].__setitem__("ledger_movement", str(P))),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("B-remaining", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_AFTER - 1))),
        ("UQ-zero", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("UA-zero", lambda d: d["ledger"].__setitem__("residual_U_A", 0)),
        ("tail", lambda d: d["rank9_updated_gate"].__setitem__("new_tail_target", str(EXPECTED_TAIL_TARGET + 1))),
        ("Emax", lambda d: d["rank9_updated_gate"].__setitem__("new_aggregate_excess_max", str(EXPECTED_E_MAX + 1))),
        ("Kremaining", lambda d: d["rank9_updated_gate"].__setitem__("K_remaining", EXPECTED_K_REMAINING + 1)),
        ("break-J", lambda d: d["rank9_updated_gate"].__setitem__("maximal_gcd_break_J", EXPECTED_BREAK_J + 1)),
        ("moving-closed", lambda d: d["scope_guards"].__setitem__("moving_cofactor_one_slack_component_closed", True)),
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
    print(f"M1 one-slack twist-subline owner mutations: {total}/{total} PASS")
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
    print("M1 one-slack common-twist source-subline owner: PASS")
    print(
        "  projective subline size / post-tangent owner cap: "
        f"p+1={PROJECTIVE_SUBLINE_SIZE:,} / p-1={OWNER_CAP:,}"
    )
    print(f"  two-label source blocks: at least {SOURCE_BLOCK_MIN:,} points each")
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
