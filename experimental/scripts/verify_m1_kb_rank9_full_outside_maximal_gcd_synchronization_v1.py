#!/usr/bin/env python3
"""Verify the full-outside maximal-gcd synchronization route cut.

The proof note establishes a uniform local theorem: within one fixed
source-bound complete selector, all full-outside rank-two lines whose full
gcd has degree k-2 share one reduced Mobius map, and their deduplicated finite
slopes have cap p+1.  Current artifacts do not supply the deployed selector
provenance, so this checker keeps the ledger unchanged and fail-closes the
prospective owner.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1 as rich
import verify_m1_kb_projective_base_pair_c5_owner_v1 as c5_owner
import verify_m1_kb_rank9_active_source_matroid_reindex_v1 as active
import verify_m1_kb_rank9_deployed_source_incidence_contract_v1 as deployed
import verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1 as outside
import verify_m1_kb_rank9_projective_source_load_v1 as source_load


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-full-outside-maximal-gcd-synchronization-v1"
ARTIFACT_KIND = "M1_KB_RANK9_FULL_OUTSIDE_MAXIMAL_GCD_SYNCHRONIZATION_ROUTE_CUT"
STATUS = "PROVED_CONDITIONAL_THREE_POINT_SYNCHRONIZATION_DEPLOYED_PROVENANCE_OPEN"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-full-outside-maximal-gcd-synchronization-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-full-outside-maximal-gcd-synchronization-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_full_outside_maximal_gcd_synchronization_v1.sage"
)

C5_PAYLOAD = "9ed24d23e8c72e230a35f9b7b1360853bfc62f7bd1bd8aec70cd14552f1aafcc"
OUTSIDE_PAYLOAD = "b116567c779205f0ef60fdfe6be02fd99abbd3fe545169bd3cc66706cefd3721"
ACTIVE_PAYLOAD = "09794373c29898d13dc481b597fa61016cc9c2f3086404e96e9c875ef3636f0a"
SOURCE_LOAD_PAYLOAD = "4f3d3cf162c516c58b5b979cc7a3ba36be3a9e9ed622239b14408f0022ed2267"
DEPLOYED_PAYLOAD = "f35c148c23f0ef939525ac273178473152e555f6dda8270e82339508f1bf88c8"
RICH_PAYLOAD = "343b3bbc6ac526da12ff06988c1a280b9845f2a6117c8bc75820d55b594f6258"

P = c5_owner.P
N = c5_owner.tangent.N
K = c5_owner.tangent.K
A = c5_owner.tangent.A
J = c5_owner.tangent.J
T = c5_owner.tangent.DELTA_ZERO
CUTOFF_D = c5_owner.CUTOFF_D
RICH_X_MAX = J // c5_owner.tangent.UNIFORM_CAP
SIGMA_FLOOR = T - RICH_X_MAX + 2
SYNCHRONIZED_CAP = P + 1

U_PAID_CURRENT = c5_owner.U_PAID_AFTER
B_REMAINING_CURRENT = c5_owner.B_REMAINING_AFTER
PROSPECTIVE_U_PAID = U_PAID_CURRENT + SYNCHRONIZED_CAP
PROSPECTIVE_B_REMAINING = c5_owner.tangent.B_STAR - PROSPECTIVE_U_PAID
PROSPECTIVE_TAIL_TARGET = 17_905_062_856_176
PROSPECTIVE_E_MAX = int(
    "5257735913360750952280320052017938027249181774"
)
PROSPECTIVE_K_REMAINING = 4_807_520
PROSPECTIVE_BREAK_J = 166

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessors",
    "counted_object_contract",
    "synchronization_lemma",
    "noncontainment_moving_root_bridge",
    "provenance_audit",
    "exact_control",
    "prospective_owner",
    "ledger",
    "prospective_rank9_gate",
    "residual_route_cuts",
    "scope_guards",
    "nonclaims",
    "source_bindings",
    "payload_sha256",
}


class ContractError(RuntimeError):
    """Raised for certificate, source, or exact-arithmetic drift."""


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


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path}")
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
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
        source_binding("proof-note", NOTE_REL, "conditional theorem and deployed route cut"),
        source_binding("python-verifier", SCRIPT_REL, "certificate, arithmetic, and mutations"),
        source_binding("sage-control", SAGE_REL, "three-anchor and two-anchor exact controls"),
        source_binding("readme", README_REL, "replay and scope contract"),
        source_binding("c5-note", c5_owner.NOTE_REL, "current owner and ledger"),
        source_binding(
            "c5-certificate",
            c5_owner.CERT_PATH.relative_to(ROOT),
            "current ledger fingerprint",
        ),
        source_binding("c5-verifier", c5_owner.SCRIPT_REL, "current ledger semantics"),
        source_binding("outside-note", outside.NOTE_REL, "maximal-gcd predecessor terminal"),
        source_binding(
            "outside-certificate",
            outside.CERT_PATH.relative_to(ROOT),
            "maximal-gcd predecessor fingerprint",
        ),
        source_binding("outside-verifier", outside.SCRIPT_REL, "maximal-gcd predecessor semantics"),
        source_binding("active-source-note", active.NOTE_REL, "full-outside source floor"),
        source_binding(
            "active-source-certificate",
            active.CERT_PATH.relative_to(ROOT),
            "full-outside contract fingerprint",
        ),
        source_binding("active-source-verifier", active.SCRIPT_REL, "full-outside contract semantics"),
        source_binding("source-load-note", source_load.NOTE_REL, "same-selector source equations"),
        source_binding(
            "source-load-certificate",
            source_load.CERT_PATH.relative_to(ROOT),
            "source-load contract fingerprint",
        ),
        source_binding("source-load-verifier", source_load.SCRIPT_REL, "source-load semantics"),
        source_binding("rich-atlas-note", rich.NOTE_REL, "moving-zero bridge"),
        source_binding(
            "rich-atlas-certificate",
            rich.CERT_PATH.relative_to(ROOT),
            "moving-zero contract fingerprint",
        ),
        source_binding("rich-atlas-verifier", rich.PYTHON_REL, "rich-atlas semantics"),
        source_binding("deployed-source-note", deployed.NOTE_REL, "Routes S/U/C and readiness cut"),
        source_binding(
            "deployed-source-certificate",
            deployed.CERT_PATH.relative_to(ROOT),
            "deployed readiness fingerprint",
        ),
        source_binding("deployed-source-verifier", deployed.PYTHON_REL, "deployed readiness semantics"),
    ]


def validate_predecessors() -> tuple[dict[str, Any], ...]:
    c5_doc = c5_owner.load_json(c5_owner.CERT_PATH)
    c5_owner.validate_certificate(c5_doc)
    require(c5_doc["payload_sha256"] == C5_PAYLOAD, "C5 predecessor payload drift")

    outside_doc = outside.load_json(outside.CERT_PATH)
    outside.validate_certificate(outside_doc)
    require(outside_doc["payload_sha256"] == OUTSIDE_PAYLOAD, "outside predecessor payload drift")

    active_doc = load_json(active.CERT_PATH)
    active.validate_certificate(active_doc)
    require(active_doc["payload_sha256"] == ACTIVE_PAYLOAD, "active-source payload drift")

    source_doc = load_json(source_load.CERT_PATH)
    source_load.validate_certificate(source_doc)
    require(source_doc["payload_sha256"] == SOURCE_LOAD_PAYLOAD, "source-load payload drift")

    deployed_doc = deployed.load_json(deployed.CERT_PATH)
    deployed.validate_certificate(deployed_doc)
    require(deployed_doc["payload_sha256"] == DEPLOYED_PAYLOAD, "deployed-source payload drift")

    rich_doc = rich.load_json(rich.CERT_PATH)
    rich.validate_certificate(rich_doc)
    require(rich_doc["payload_sha256"] == RICH_PAYLOAD, "rich-atlas payload drift")
    return c5_doc, outside_doc, active_doc, source_doc, deployed_doc, rich_doc


def validate_consumed_facts(
    c5_doc: dict[str, Any],
    outside_doc: dict[str, Any],
    active_doc: dict[str, Any],
    source_doc: dict[str, Any],
    deployed_doc: dict[str, Any],
    rich_doc: dict[str, Any],
) -> None:
    require(
        any(
            item["terminal"]
            == "UNPAID_FULL_PROJECTIVE_OR_NONSPLIT_MAXIMAL_GCD_SUBLINE_OUTSIDE_CARRIER_RANK2"
            for item in c5_doc["residual_route_cuts"]
        ),
        "maximal-gcd predecessor terminal drift",
    )
    require(
        "UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2"
        in outside_doc["residual_terminals"],
        "outside residual terminal drift",
    )
    full_outside = active_doc["full_outside_source_subcell"]
    require(full_outside["hypothesis"] == "Sigma INTERSECT V is empty", "full-outside hypothesis drift")
    require(full_outside["rank_one_excluded_by_source_syndrome_rank_two"] is True, "rank-one exclusion drift")
    require(full_outside["rank_two_source_floor"] == "|Sigma|>=t-x_L+2", "source floor drift")
    require(full_outside["actual_eight_outlier_rank9_binding_constructed"] is False, "eight-outlier readiness drift")
    require(full_outside["regular_first_match_binding_constructed"] is False, "regular binding drift")

    chain = source_doc["same_selector_chain"]
    require(chain["fixed_sp3_translation"] is True, "SP3 translation drift")
    require(chain["cross_selector_mixing_forbidden"] is True, "selector mixing guard drift")
    require(chain["post_deletion_selector_data_required"] is True, "selector restart guard drift")

    moving = rich_doc["moving_zero_system"]
    require(moving["transversality_floor"] == "x_L+delta_eta>=1", "moving-zero floor drift")
    require(moving["rich_x_max"] == RICH_X_MAX, "rich x maximum drift")

    current = deployed_doc["current_inputs"]
    require(current["complete_global_first_match_replay"] is False, "first-match readiness drift")
    require(current["deployed_complete_selector_inventory"] is False, "selector inventory drift")
    require(current["paying_selector_source_family_coverage"] is False, "source coverage drift")
    require(current["deployed_rich_pencil_selector_constructed"] is False, "selector construction drift")
    require(current["deployed_rich_pencil_census"] is False, "selector census drift")
    require(
        deployed_doc["implementation_scope"]["full_deployed_producer_validator_implemented"] is False,
        "producer validator readiness drift",
    )
    routes = deployed_doc["route_assessment"]
    require(routes["coverage_disjunction_satisfied"] is False, "coverage disjunction drift")
    require(routes["terminal"] == "UNBOUND_DEPLOYED_SOURCE_INCIDENCE", "enclosing terminal drift")


def exact_prospective_gate() -> dict[str, Any]:
    tangent = c5_owner.tangent
    gate = tangent.one_cut_gate(PROSPECTIVE_B_REMAINING, CUTOFF_D, N, 1)
    tail = int(gate["largest_sufficient_low_deficit_cap_T_star"])
    e_max = tangent.aggregate_excess_max(tail)
    k_remaining = tangent.exact_k_remaining(PROSPECTIVE_B_REMAINING)
    beta_cap = math.comb(K - 2, 8)
    break_j = tangent.UNIFORM_CAP + e_max // beta_cap + 1
    require(tail == PROSPECTIVE_TAIL_TARGET, "prospective tail target drift")
    require(e_max == PROSPECTIVE_E_MAX, "prospective E_max drift")
    require(k_remaining == PROSPECTIVE_K_REMAINING, "prospective K_remaining drift")
    require(break_j == PROSPECTIVE_BREAK_J, "prospective break J drift")
    return {
        "conditional_only": True,
        "cutoff_D": CUTOFF_D,
        "tail_target": str(tail),
        "aggregate_excess_max": str(e_max),
        "K_remaining": k_remaining,
        "maximal_gcd_break_J": break_j,
        "gate": gate,
    }


_EXPECTED_CACHE: dict[str, Any] | None = None


def expected_certificate() -> dict[str, Any]:
    global _EXPECTED_CACHE
    if _EXPECTED_CACHE is not None:
        return copy.deepcopy(_EXPECTED_CACHE)

    docs = validate_predecessors()
    validate_consumed_facts(*docs)
    note_text = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        "UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE",
        "UNBOUND_DEPLOYED_SOURCE_INCIDENCE",
        "UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP",
    ):
        require(token in note_text, f"proof-note terminal missing: {token}")

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "extension_degree": c5_owner.tangent.EXTENSION_DEGREE,
            "q_line": str(P**6),
            "n": N,
            "k": K,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
        },
        "predecessors": {
            "projective_base_pair_c5_owner": "payload-sha256:" + C5_PAYLOAD,
            "outside_rank2_base_absorption": "payload-sha256:" + OUTSIDE_PAYLOAD,
            "active_source_reindex": "payload-sha256:" + ACTIVE_PAYLOAD,
            "projective_source_load": "payload-sha256:" + SOURCE_LOAD_PAYLOAD,
            "deployed_source_contract": "payload-sha256:" + DEPLOYED_PAYLOAD,
            "rich_pencil_atlas": "payload-sha256:" + RICH_PAYLOAD,
        },
        "counted_object_contract": {
            "object": "distinct finite selected exact-witness slopes",
            "scope": "one fixed received pair and one fixed source-bound complete selector",
            "current_residual_intersection_required": True,
            "supports_are_unioned_before_counting": True,
            "lines_witnesses_supports_charts_and_bases_not_counted": True,
            "cross_received_pair_union_required": False,
            "projective_infinity_is_not_a_finite_slope": True,
            "exact_delete_then_selector_restart_required": True,
        },
        "synchronization_lemma": {
            "status": "PROVED_UNDER_PRINTED_HYPOTHESES",
            "same_received_pair": True,
            "same_selector": True,
            "same_sp3_source_pair": True,
            "same_Sigma_and_carrier": True,
            "full_outside": "Sigma INTERSECT V is empty",
            "source_syndrome_rank": 2,
            "coefficient_rank_each_line": 2,
            "full_gcd_symbol": "H_L=gcd(P_L,Q_L)",
            "full_gcd_degree": "k-2",
            "forced_domain_locator_may_be_smaller": True,
            "reduced_pair": "Pbar_L=U_L1*X+U_L0; Qbar_L=V_L1*X+V_L0",
            "reduced_determinant_nonzero": True,
            "projective_map": "phi_L([X:Z])=[-(U_L1*X+U_L0*Z):V_L1*X+V_L0*Z]",
            "source_anchor_equality": "phi_L([h:1])=[-epsilon_0(h):epsilon_1(h)]",
            "gcd_nonzero_on_source_anchors": True,
            "rich_x_max": RICH_X_MAX,
            "source_anchor_floor_formula": "t-floor(j/20)+2",
            "source_anchor_floor": SIGMA_FLOOR,
            "three_distinct_anchors_available": True,
            "two_anchors_sufficient": False,
            "mobius_three_point_rigidity": True,
            "all_reduced_maps_common": True,
            "common_projective_subline_size": P + 1,
            "deduplicated_finite_cap": str(SYNCHRONIZED_CAP),
            "nonsplit_full_gcd_allowed": True,
            "field_full_received_pair_allowed": True,
            "pair_global_projective_descent_claimed": False,
        },
        "noncontainment_moving_root_bridge": {
            "contributing_line_beta_positive": True,
            "contributing_line_J_at_least": 21,
            "transversality_forces_F_eta_L_nonempty": True,
            "one_base_domain_moving_root_required_per_selected_slope": True,
            "moving_root_x_in_W_L_subset_V_subset_D_subset_F_p": True,
            "source_pair_zero_on_carrier_under_full_outside": True,
            "source_coupling_implies_P_plus_eta_Q_zero_at_x": True,
            "x_is_not_common_root": True,
            "selected_projective_slope_equals_phi_of_x": True,
            "bridge_is_load_bearing": True,
        },
        "provenance_audit": {
            "deployed_terminal_record_artifact": None,
            "deployed_terminal_record_count": None,
            "all_terminal_records_checked": False,
            "deployed_complete_selector_inventory": False,
            "full_deployed_producer_validator_implemented": False,
            "paying_selector_source_family_coverage": False,
            "actual_eight_outlier_rank9_binding_constructed": False,
            "regular_first_match_binding_constructed": False,
            "complete_global_first_match_replay": False,
            "route_S_present": False,
            "route_U_present": False,
            "route_C_present": False,
            "uniform_local_lemma_proved": True,
            "uniform_deployed_coverage_proved": False,
            "first_match_disjointness_proved": False,
            "ledger_payment_authorized": False,
            "enclosing_terminal": "UNBOUND_DEPLOYED_SOURCE_INCIDENCE",
            "terminal": "UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE",
        },
        "exact_control": {
            "field": "GF(5^6)",
            "base_field": "GF(5)",
            "toy_k": 6,
            "maximal_gcd_degree": 4,
            "distinct_nonbase_full_gcd_factors": 2,
            "source_anchor_count": 3,
            "same_exact_source_pair_on_anchors": True,
            "same_reduced_projective_map": True,
            "common_projective_subline_points": 6,
            "finite_image_points": 5,
            "projective_infinity_present": True,
            "two_anchor_countercontrol_maps": 2,
            "two_anchor_countercontrol_intersection": 2,
            "two_anchor_countercontrol_union": 10,
            "two_anchor_union_exceeds_p_plus_one": True,
            "scale": "EXACT_TOY_CONTROL_NOT_DEPLOYED_PROVENANCE",
        },
        "prospective_owner": {
            "status": "CONDITIONAL_NOT_BANKED",
            "owner": "PAID_FULL_OUTSIDE_MAXIMAL_GCD_SYNCHRONIZED_SUBLINE",
            "activation_condition": "Route S, U, or C plus first-match residual intersection/deletion/restart",
            "cap": str(SYNCHRONIZED_CAP),
            "current_U_paid": str(U_PAID_CURRENT),
            "prospective_U_paid": str(PROSPECTIVE_U_PAID),
            "current_B_remaining": str(B_REMAINING_CURRENT),
            "prospective_B_remaining": str(PROSPECTIVE_B_REMAINING),
            "included_in_current_ledger": False,
        },
        "ledger": {
            "B_star": str(c5_owner.tangent.B_STAR),
            "U_paid_before": str(U_PAID_CURRENT),
            "U_paid_after": str(U_PAID_CURRENT),
            "B_remaining_before": str(B_REMAINING_CURRENT),
            "B_remaining_after": str(B_REMAINING_CURRENT),
            "ledger_movement": "0",
            "conditional_cap_excluded_from_U_paid": True,
            "U_Q": None,
            "residual_U_A": None,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "prospective_rank9_gate": exact_prospective_gate(),
        "residual_route_cuts": [
            {
                "terminal": "UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE",
                "condition": "no deployed Route S, U, or C and no terminal-record artifact",
                "reason": "the local p+1 lemma cannot be applied to an unbound selector universe",
            },
            {
                "terminal": "UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP",
                "condition": "deg gcd(P_L,Q_L)<k-2",
                "reason": "the gcd-reduced map can have degree greater than one",
            },
            {
                "terminal": "UNBOUND_POST_TANGENT_SOURCE_LOAD",
                "condition": "non-full-outside and other source-load cells",
                "reason": "three-point synchronization addresses only the full-outside maximal-gcd cell",
            },
        ],
        "scope_guards": {
            "conditional_synchronization_lemma_proved": True,
            "deployed_maximal_gcd_owner_banked": False,
            "general_lower_gcd_payment_proved": False,
            "non_full_outside_source_load_paid": False,
            "U_Q_determined": False,
            "residual_U_A_determined": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": [
            "No deployed terminal records are invented or represented by an empty file.",
            "No complete selector, eight-outlier binding, or regular first-match chart is constructed.",
            "No generic full-projective or GM emptiness implication is asserted.",
            "No local subline is promoted to pair-global projective descent.",
            "No lower-gcd rational map is paid.",
            "No toy control is extrapolated to the deployed row.",
            "No p+1 owner charge is included in U_paid.",
            "No value is assigned to U_Q or residual U_A.",
            "The KoalaBear row remains open.",
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
        ("predecessor-956", lambda d: d["predecessors"].__setitem__("projective_base_pair_c5_owner", "payload-sha256:" + "0" * 64)),
        ("predecessor-active", lambda d: d["predecessors"].__setitem__("active_source_reindex", "payload-sha256:" + "0" * 64)),
        ("predecessor-source-load", lambda d: d["predecessors"].__setitem__("projective_source_load", "payload-sha256:" + "0" * 64)),
        ("predecessor-deployed-source", lambda d: d["predecessors"].__setitem__("deployed_source_contract", "payload-sha256:" + "0" * 64)),
        ("count-witnesses", lambda d: d["counted_object_contract"].__setitem__("object", "witnesses")),
        ("cross-received-pair", lambda d: d["counted_object_contract"].__setitem__("cross_received_pair_union_required", True)),
        ("no-residual-intersection", lambda d: d["counted_object_contract"].__setitem__("current_residual_intersection_required", False)),
        ("no-selector-restart", lambda d: d["counted_object_contract"].__setitem__("exact_delete_then_selector_restart_required", False)),
        ("same-selector-false", lambda d: d["synchronization_lemma"].__setitem__("same_selector", False)),
        ("same-source-pair-false", lambda d: d["synchronization_lemma"].__setitem__("same_sp3_source_pair", False)),
        ("full-outside-false", lambda d: d["synchronization_lemma"].__setitem__("full_outside", "Sigma INTERSECT V nonempty")),
        ("sigma-floor", lambda d: d["synchronization_lemma"].__setitem__("source_anchor_floor", SIGMA_FLOOR - 1)),
        ("only-two-anchors", lambda d: d["synchronization_lemma"].__setitem__("three_distinct_anchors_available", False)),
        ("two-anchors-sufficient", lambda d: d["synchronization_lemma"].__setitem__("two_anchors_sufficient", True)),
        ("g-zero-anchor", lambda d: d["synchronization_lemma"].__setitem__("gcd_nonzero_on_source_anchors", False)),
        ("gcd-degree", lambda d: d["synchronization_lemma"].__setitem__("full_gcd_degree", "k-3")),
        ("reduced-rank-one", lambda d: d["synchronization_lemma"].__setitem__("coefficient_rank_each_line", 1)),
        ("determinant-zero", lambda d: d["synchronization_lemma"].__setitem__("reduced_determinant_nonzero", False)),
        ("maps-not-common", lambda d: d["synchronization_lemma"].__setitem__("all_reduced_maps_common", False)),
        ("subline-size-p", lambda d: d["synchronization_lemma"].__setitem__("common_projective_subline_size", P)),
        ("infinity-finite", lambda d: d["counted_object_contract"].__setitem__("projective_infinity_is_not_a_finite_slope", False)),
        ("beta-not-positive", lambda d: d["noncontainment_moving_root_bridge"].__setitem__("contributing_line_beta_positive", False)),
        ("moving-root-not-required", lambda d: d["noncontainment_moving_root_bridge"].__setitem__("one_base_domain_moving_root_required_per_selected_slope", False)),
        ("moving-root-empty", lambda d: d["noncontainment_moving_root_bridge"].__setitem__("transversality_forces_F_eta_L_nonempty", False)),
        ("common-root", lambda d: d["noncontainment_moving_root_bridge"].__setitem__("x_is_not_common_root", False)),
        ("bridge-not-load-bearing", lambda d: d["noncontainment_moving_root_bridge"].__setitem__("bridge_is_load_bearing", False)),
        ("terminal-records-present", lambda d: d["provenance_audit"].__setitem__("deployed_terminal_record_artifact", "records.jsonl")),
        ("record-count-zero", lambda d: d["provenance_audit"].__setitem__("deployed_terminal_record_count", 0)),
        ("all-records-checked", lambda d: d["provenance_audit"].__setitem__("all_terminal_records_checked", True)),
        ("inventory-present", lambda d: d["provenance_audit"].__setitem__("deployed_complete_selector_inventory", True)),
        ("producer-validator", lambda d: d["provenance_audit"].__setitem__("full_deployed_producer_validator_implemented", True)),
        ("coverage-proved", lambda d: d["provenance_audit"].__setitem__("uniform_deployed_coverage_proved", True)),
        ("first-match-proved", lambda d: d["provenance_audit"].__setitem__("first_match_disjointness_proved", True)),
        ("ledger-authorized", lambda d: d["provenance_audit"].__setitem__("ledger_payment_authorized", True)),
        ("toy-deployed", lambda d: d["exact_control"].__setitem__("scale", "DEPLOYED_PROOF")),
        ("two-anchor-union", lambda d: d["exact_control"].__setitem__("two_anchor_countercontrol_union", 6)),
        ("prospective-cap-p", lambda d: d["prospective_owner"].__setitem__("cap", str(P))),
        ("prospective-U", lambda d: d["prospective_owner"].__setitem__("prospective_U_paid", str(PROSPECTIVE_U_PAID + 1))),
        ("prospective-included", lambda d: d["prospective_owner"].__setitem__("included_in_current_ledger", True)),
        ("ledger-movement", lambda d: d["ledger"].__setitem__("ledger_movement", str(SYNCHRONIZED_CAP))),
        ("U-paid-moved", lambda d: d["ledger"].__setitem__("U_paid_after", str(PROSPECTIVE_U_PAID))),
        ("B-remaining-moved", lambda d: d["ledger"].__setitem__("B_remaining_after", str(PROSPECTIVE_B_REMAINING))),
        ("UQ-zero", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("UA-zero", lambda d: d["ledger"].__setitem__("residual_U_A", 0)),
        ("prospective-tail", lambda d: d["prospective_rank9_gate"].__setitem__("tail_target", str(PROSPECTIVE_TAIL_TARGET + 1))),
        ("lower-gcd-closed", lambda d: d["scope_guards"].__setitem__("general_lower_gcd_payment_proved", True)),
        ("row-closed", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("rank10", lambda d: d["scope_guards"].__setitem__("rank_at_least_ten_authorized", True)),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("source-path", lambda d: d["source_bindings"][0].__setitem__("path", d["source_bindings"][1]["path"])),
        ("duplicate-binding", lambda d: d["source_bindings"][1].__setitem__("binding_id", d["source_bindings"][0]["binding_id"])),
        ("payload", lambda d: d.__setitem__("payload_sha256", "1" * 64)),
    ]


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
    require(rejected == len(mutation_cases()), "mutation count drift")
    print(f"M1 maximal-gcd synchronization mutations: {rejected}/{rejected} PASS")
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
    print("M1 full-outside maximal-gcd synchronization: PASS")
    print(f"  conditional common-subline cap: p+1 = {SYNCHRONIZED_CAP:,}")
    print(f"  source anchors: at least {SIGMA_FLOOR:,} (> 2)")
    print("  deployed terminal records: ABSENT; Routes S/U/C: ABSENT")
    print(f"  ledger movement: 0; U_paid remains {U_PAID_CURRENT:,}")
    print("  terminal: UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE")
    print("  KoalaBear row remains YELLOW")
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
