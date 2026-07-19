#!/usr/bin/env python3
"""Verify the KoalaBear projective-base-pair C5 owner.

The companion note proves a pairwise first-match dichotomy.  A positive-rank
pair with intrinsic projective syndrome field GF(p) has at most p+1 remaining
finite slopes and canonical C5 owns all of them.  Otherwise the existing
residual base-slope owner has at most p slopes.  The joint owner therefore
replaces the old p charge by p+1, for exact ledger movement one.

This checker binds the theorem and predecessor state, recomputes every
downstream integer, and fail-closes the field-full and lower-gcd residuals.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_kb_mca_1116048_base_slope_universe_v2 as base_owner
import verify_m1_fp2_post_c5_mask_incidence_v1 as post_c5
import verify_m1_kb_rank9_outside_rank2_base_slope_absorption_v1 as outside
import verify_m1_kb_rank9_tangent_owner_splice_v1 as tangent


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-projective-base-pair-c5-owner-v1"
ARTIFACT_KIND = "M1_KB_PROJECTIVE_BASE_PAIR_C5_JOINT_OWNER"
STATUS = (
    "PROVED_PROJECTIVE_BASE_PAIR_C5_OWNER_"
    "FULL_OUTSIDE_SPLIT_MAXIMAL_GCD_ABSORBED_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-projective-base-pair-c5-owner-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_projective_base_pair_c5_owner_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_projective_base_pair_c5_owner_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-projective-base-pair-c5-owner-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_projective_base_pair_c5_owner_v1.sage"
)
PROJECTIVE_C5_NOTE_REL = Path(
    "experimental/notes/thresholds/projective_syndrome_c5_first_match.md"
)
POST_C5_NOTE_REL = post_c5.NOTE_REL
POST_C5_CERT_REL = post_c5.CERT_PATH.relative_to(ROOT)
POST_C5_SCRIPT_REL = post_c5.VERIFIER_REL
OUTSIDE_NOTE_REL = outside.NOTE_REL
OUTSIDE_CERT_REL = outside.CERT_PATH.relative_to(ROOT)
OUTSIDE_SCRIPT_REL = outside.SCRIPT_REL
TANGENT_NOTE_REL = tangent.NOTE_REL
TANGENT_CERT_REL = tangent.CERT_PATH.relative_to(ROOT)
TANGENT_SCRIPT_REL = tangent.PYTHON_REL
BASE_NOTE_REL = base_owner.NOTE_REL
BASE_CERT_REL = base_owner.CERT_PATH.relative_to(ROOT)
BASE_SCRIPT_REL = base_owner.VERIFIER_REL
ACTIVE_SOURCE_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_active_source_matroid_reindex_v1.md"
)

POST_C5_PAYLOAD = (
    "1925171dce23cee6dd7e5088bb6774580dd362bd8dbd794cea1c5883456baabc"
)
OUTSIDE_PAYLOAD = (
    "6f278f7c14123872b78b03a0937d63d23a31e8cf328e5dca45ac6fa482cc55e4"
)
TANGENT_PAYLOAD = (
    "0d5753ae6055d6f1dc0edb49f0e0322596da8a70b68b113993dcec11934e7eed"
)
BASE_PAYLOAD = (
    "6ea64d19ecd298fb5be1bff9b17e7c41d3239553e0aa9ebfd7c9ff9d17896a56"
)

P = tangent.P
P2 = P**2
P3 = P**3
P6 = P**6
OLD_BASE_BLOCK_CAP = P
NEW_JOINT_BLOCK_CAP = P + 1
LEDGER_MOVEMENT = NEW_JOINT_BLOCK_CAP - OLD_BASE_BLOCK_CAP

U_PAID_BEFORE = tangent.U_PAID_AFTER
B_REMAINING_BEFORE = tangent.B_REMAINING_AFTER
U_PAID_AFTER = U_PAID_BEFORE + LEDGER_MOVEMENT
B_REMAINING_AFTER = tangent.B_STAR - U_PAID_AFTER

CUTOFF_D = tangent.CUTOFF_D
OLD_TAIL_TARGET = tangent.EXPECTED_NEW_TAIL_TARGET
NEW_TAIL_TARGET = 17_907_571_352_522
OLD_E_MAX = tangent.EXPECTED_NEW_E_MAX
NEW_E_MAX = int(
    "5284472953546090246987229221937957984923412724"
)
E_MAX_DROP = math.comb(tangent.DELTA_ZERO + tangent.CORE_R, tangent.CORE_R)
K_REMAINING = tangent.EXPECTED_K_REMAINING
MAXIMAL_GCD_BINOMIAL = math.comb(tangent.K - 2, 8)
MAXIMAL_GCD_BREAK_J = 166
NEW_MAXIMAL_GCD_EXCESS = (
    MAXIMAL_GCD_BINOMIAL * (MAXIMAL_GCD_BREAK_J - tangent.UNIFORM_CAP)
    - NEW_E_MAX
)

FIRST_FIVE = list(post_c5.KB_FIRST_FIVE)
NEW_FIRST_MATCH_ORDER = [
    *FIRST_FIVE,
    "projective_base_pair_C5",
    "residual_extension_valued_strata",
    "residual_base_slope_universe",
    "sparse_sigma_or_sparse_support",
    "m1_half_turn_or_coefficient_shadow",
    "primitive_qfin_residual",
]

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessors",
    "counted_object_contract",
    "first_match_partition",
    "joint_owner_theorem",
    "full_outside_split_maximal_gcd_absorption",
    "exact_control",
    "ledger",
    "rank9_updated_gate",
    "residual_route_cuts",
    "scope_guards",
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


def source_binding(
    binding_id: str, relative: Path, role: str
) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("proof-note", NOTE_REL, "symbolic owner and route-cut proof"),
        source_binding("python-verifier", SCRIPT_REL, "exact certificate builder and mutations"),
        source_binding("sage-control", SAGE_REL, "exact sharp finite-chart C5 control"),
        source_binding("readme", README_REL, "replay contract"),
        source_binding(
            "projective-c5-theorem",
            PROJECTIVE_C5_NOTE_REL,
            "intrinsic field, subline confinement, and C5 witness exhaustion",
        ),
        source_binding("post-c5-note", POST_C5_NOTE_REL, "KoalaBear policy adapter"),
        source_binding("post-c5-certificate", POST_C5_CERT_REL, "previous unpaid C5 state"),
        source_binding("post-c5-verifier", POST_C5_SCRIPT_REL, "post-C5 semantics"),
        source_binding("outside-note", OUTSIDE_NOTE_REL, "predecessor maximal-gcd terminal"),
        source_binding("outside-certificate", OUTSIDE_CERT_REL, "current ledger and terminal"),
        source_binding("outside-verifier", OUTSIDE_SCRIPT_REL, "predecessor semantics"),
        source_binding("tangent-note", TANGENT_NOTE_REL, "deployed ledger and one-cut splice"),
        source_binding("tangent-certificate", TANGENT_CERT_REL, "exact current thresholds"),
        source_binding("tangent-verifier", TANGENT_SCRIPT_REL, "exact one-cut compiler"),
        source_binding("base-owner-note", BASE_NOTE_REL, "global residual base-slope owner"),
        source_binding("base-owner-certificate", BASE_CERT_REL, "banked p cap"),
        source_binding("base-owner-verifier", BASE_SCRIPT_REL, "base-owner semantics"),
        source_binding(
            "active-source-note",
            ACTIVE_SOURCE_NOTE_REL,
            "full-outside source coupling and maximal-gcd equations",
        ),
    ]


def validate_predecessors() -> tuple[
    dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]
]:
    post_doc = post_c5.load_json(ROOT / POST_C5_CERT_REL)
    post_c5.validate(post_doc, exact_rebuild=True)
    require(post_doc["payload_sha256"] == POST_C5_PAYLOAD, "post-C5 payload drift")

    outside_doc = outside.load_json(ROOT / OUTSIDE_CERT_REL)
    outside.validate_certificate(outside_doc)
    require(outside_doc["payload_sha256"] == OUTSIDE_PAYLOAD, "outside payload drift")

    tangent_doc = tangent.load_json(ROOT / TANGENT_CERT_REL)
    tangent.verify_semantics(tangent_doc)
    require(tangent_doc["payload_sha256"] == TANGENT_PAYLOAD, "tangent payload drift")

    base_doc = base_owner.load_json(ROOT / BASE_CERT_REL)
    base_owner.validate_certificate(base_doc)
    require(base_doc["payload_sha256"] == BASE_PAYLOAD, "base payload drift")
    return post_doc, outside_doc, tangent_doc, base_doc


def validate_consumed_source_facts(
    post_doc: dict[str, Any],
    outside_doc: dict[str, Any],
    tangent_doc: dict[str, Any],
    base_doc: dict[str, Any],
) -> None:
    refinement = post_doc["projective_c5_refinement"]
    require(
        refinement["proper_intermediate_degrees"] == [1, 2, 3],
        "proper-field tower drift",
    )
    require(
        refinement["proper_field_cell_witness_exhaustive"] is True,
        "C5 exhaustion drift",
    )
    require(
        refinement["proper_field_cell_paid_in_this_packet"] is False,
        "historical unpaid-C5 status drift",
    )
    require(
        post_doc["policy_compatibility"]["kb_first_five"] == FIRST_FIVE,
        "KoalaBear first-five drift",
    )
    require(
        post_doc["ledger"]["pair_rank_cases_combine_by"] == "MAXIMUM_NOT_SUM",
        "pairwise combination rule drift",
    )

    require(
        outside_doc["ledger"]["U_paid"] == str(U_PAID_BEFORE),
        "current U_paid drift",
    )
    require(
        outside_doc["ledger"]["B_remaining"] == str(B_REMAINING_BEFORE),
        "current B_remaining drift",
    )
    require(
        "UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2"
        in outside_doc["residual_terminals"],
        "predecessor maximal-gcd terminal drift",
    )

    require(
        tangent_doc["ledger"]["U_paid_after"] == str(U_PAID_BEFORE),
        "tangent paid total drift",
    )
    require(
        tangent_doc["ledger"]["B_remaining_after"] == str(B_REMAINING_BEFORE),
        "tangent budget drift",
    )
    require(
        tangent_doc["rank9_updated_gate"]["new_tail_target"]
        == str(OLD_TAIL_TARGET),
        "old rank-nine tail drift",
    )
    require(
        tangent_doc["rank9_updated_gate"]["new_aggregate_excess_max"]
        == str(OLD_E_MAX),
        "old E_max drift",
    )

    theorem = base_doc["theorem"]
    require(theorem["set_inclusion"] == "residual_set subseteq F_p", "base set drift")
    require(theorem["global_once_bound"] == str(P), "base cap drift")
    require(theorem["infinity_included"] is False, "base finite-chart drift")


def exact_rank9_update() -> dict[str, Any]:
    old_gate = tangent.one_cut_gate(
        B_REMAINING_BEFORE, CUTOFF_D, tangent.N, 1
    )
    new_gate = tangent.one_cut_gate(
        B_REMAINING_AFTER, CUTOFF_D, tangent.N, 1
    )
    old_tail = int(old_gate["largest_sufficient_low_deficit_cap_T_star"])
    new_tail = int(new_gate["largest_sufficient_low_deficit_cap_T_star"])
    old_e = tangent.aggregate_excess_max(old_tail)
    new_e = tangent.aggregate_excess_max(new_tail)
    k_before = tangent.exact_k_remaining(B_REMAINING_BEFORE)
    k_after = tangent.exact_k_remaining(B_REMAINING_AFTER)

    require(old_tail == OLD_TAIL_TARGET, "old tail target drift")
    require(new_tail == NEW_TAIL_TARGET, "new tail target drift")
    require(old_e == OLD_E_MAX, "old E_max drift")
    require(new_e == NEW_E_MAX, "new E_max drift")
    require(old_e - new_e == E_MAX_DROP, "E_max drop drift")
    require(k_before == k_after == K_REMAINING, "K_remaining drift")

    break_j = tangent.UNIFORM_CAP + new_e // MAXIMAL_GCD_BINOMIAL + 1
    require(break_j == MAXIMAL_GCD_BREAK_J, "maximal-gcd break J drift")
    require(
        NEW_MAXIMAL_GCD_EXCESS
        == int(
            "7448808889738108616161388508793170037185582"
        ),
        "maximal-gcd excess drift",
    )
    return {
        "cutoff_D": CUTOFF_D,
        "old_tail_target": str(old_tail),
        "new_tail_target": str(new_tail),
        "tail_target_drop": str(old_tail - new_tail),
        "old_aggregate_excess_max": str(old_e),
        "new_aggregate_excess_max": str(new_e),
        "aggregate_excess_drop": str(old_e - new_e),
        "aggregate_excess_drop_formula": "C(67480,8)",
        "K_remaining_before": k_before,
        "K_remaining_after": k_after,
        "maximal_gcd_break_J": break_j,
        "maximal_gcd_break_J_unchanged": True,
        "new_maximal_gcd_break_excess": str(NEW_MAXIMAL_GCD_EXCESS),
        "new_gate": new_gate,
    }


def expected_certificate() -> dict[str, Any]:
    post_doc, outside_doc, tangent_doc, base_doc = validate_predecessors()
    validate_consumed_source_facts(
        post_doc, outside_doc, tangent_doc, base_doc
    )
    note_text = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        "PAID_PAIR_PROJECTIVE_BASE_SUBLINE_C5",
        "UNPAID_NONSTANDARD_SUBLINE_FULL_PAIR_FIELD",
        "UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2",
        "UNPAID_FULL_PROJECTIVE_OR_NONSPLIT_MAXIMAL_GCD_SUBLINE_OUTSIDE_CARRIER_RANK2",
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
            "extension_degree": tangent.EXTENSION_DEGREE,
            "q_line": str(P6),
            "n": tangent.N,
            "k": tangent.K,
            "agreement_A": tangent.A,
            "error_count_j": tangent.J,
            "syndrome_depth_t": tangent.DELTA_ZERO,
        },
        "predecessors": {
            "post_c5_mask_incidence": "payload-sha256:" + POST_C5_PAYLOAD,
            "outside_rank2_base_absorption": "payload-sha256:" + OUTSIDE_PAYLOAD,
            "tangent_owner_splice": "payload-sha256:" + TANGENT_PAYLOAD,
            "base_slope_universe": "payload-sha256:" + BASE_PAYLOAD,
        },
        "counted_object_contract": {
            "object": "distinct finite exact-witness slopes",
            "scope": "one fixed received pair",
            "supports_are_unioned_before_counting": True,
            "witnesses_supports_and_charts_are_not_counted": True,
            "cross_received_pair_union_required": False,
            "projective_infinity_is_not_a_finite_slope": True,
        },
        "first_match_partition": {
            "order": NEW_FIRST_MATCH_ORDER,
            "earlier_branch_count": 5,
            "projective_base_pair_C5_index_one_based": 6,
            "residual_extension_index_one_based": 7,
            "residual_base_index_one_based": 8,
            "projective_base_pair_cell_owns_all_post5_slopes": True,
            "projective_base_pair_cell_is_not_extension_only": True,
            "later_cells_empty_when_projective_field_is_base": True,
            "earlier_masks_machine_executable_in_this_packet": False,
            "monotone_under_actual_earlier_deletion": True,
        },
        "joint_owner_theorem": {
            "rank_zero_noncontained_fiber_empty": True,
            "base_projective_pair_condition": "rank(Y_R)>0 and F_proj(R)=F_p",
            "one_pair_global_projectivity_for_all_supports": True,
            "projective_subline_size": P + 1,
            "finite_chart_uniform_cap": P + 1,
            "projective_base_pair_C5_cap": str(P + 1),
            "nonbase_projective_pair_C5_cell_empty": True,
            "residual_base_slope_cap_when_C5_empty": str(P),
            "case_combination": "MAXIMUM_NOT_SUM",
            "joint_cap_formula": "max(p+1,p)=p+1",
            "joint_uniform_cap": str(P + 1),
            "replaces_existing_base_block": True,
            "adds_second_independent_block": False,
            "earlier_deletion_can_increase_cap": False,
        },
        "full_outside_split_maximal_gcd_absorption": {
            "scope": "predecessor full-outside c_L=k-2 split maximal-gcd rank-two source subcell",
            "full_outside_source_zero_off_Sigma": True,
            "split_common_root_count": "c_L=k-2",
            "common_root_locator": "G=L_C in F_p[X], deg(G)=k-2",
            "degree_gcd_k_minus_2_alone_implies_split_base_locator": False,
            "polynomial_pair": "(P,Q)=(G(aX+b),G(cX+d))",
            "coefficient_matrix": "[[a,c],[b,d]]",
            "coefficient_matrix_invertible": True,
            "base_pair": "(1_Sigma*G*X,1_Sigma*G)",
            "source_pair_factorization": "R_epsilon=R_base*A",
            "restored_codewords_are_gauge": True,
            "transverse_source_syndrome_rank": 2,
            "intrinsic_projective_field": "F_p",
            "canonical_C5_witness_exhaustive": True,
            "old_terminal_component": "UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2",
            "corrected_terminal": "PAID_PAIR_PROJECTIVE_BASE_SUBLINE_C5",
            "generic_support_local_subline_implies_global_descent": False,
            "generic_nonsplit_maximal_gcd_absorbed": False,
        },
        "exact_control": {
            "field": "GF(5^6)",
            "base_field": "GF(5)",
            "code": "[5,1,5] repetition RS",
            "agreement_size": 2,
            "sparse_source_union": 3,
            "source_syndrome_rank": 2,
            "intrinsic_projective_field": "GF(5)",
            "projective_directions": 6,
            "finite_slopes": 6,
            "base_slopes": 1,
            "degree_six_extension_slopes": 5,
            "exact_two_point_noncontained_witnesses": 6,
            "GL2_normalization_to_base_pair": True,
            "finite_p_plus_one_cap_sharp": True,
            "nonsplit_countercontrol_field": "GF(11^2)",
            "nonsplit_countercontrol_code": "[9,3,7] RS",
            "nonsplit_countercontrol_gcd_degree": "k-2",
            "nonsplit_countercontrol_domain_common_roots": 0,
            "nonsplit_countercontrol_source_syndrome_rank": 2,
            "nonsplit_countercontrol_intrinsic_projective_field": "GF(11^2)",
            "nonsplit_countercontrol_exact_witnesses": 6,
            "degree_alone_base_descent_refuted": True,
            "scale": "EXACT_TOY_CONTROL_NOT_SYMBOLIC_PROOF",
        },
        "ledger": {
            "B_star": str(tangent.B_STAR),
            "old_base_block_cap": str(OLD_BASE_BLOCK_CAP),
            "new_joint_block_cap": str(NEW_JOINT_BLOCK_CAP),
            "replacement_not_addition": True,
            "ledger_movement": str(LEDGER_MOVEMENT),
            "U_paid_before": str(U_PAID_BEFORE),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "projective_base_stratum_deleted_before_residual_U_A": True,
            "U_Q": None,
            "residual_U_A": None,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "rank9_updated_gate": exact_rank9_update(),
        "residual_route_cuts": [
            {
                "terminal": "UNPAID_FULL_PROJECTIVE_OR_NONSPLIT_MAXIMAL_GCD_SUBLINE_OUTSIDE_CARRIER_RANK2",
                "condition": "F_proj(R)=F_(p^6), or deg gcd=k-2 without c_L=k-2/base-locator descent",
                "reason": "local subline and gcd degree alone do not determine the pair-global field",
            },
            {
                "terminal": "UNPAID_TOWER_PROPER_FIELD_C5",
                "condition": "F_proj(R)=F_(p^2) or F_(p^3)",
                "reason": "C5 coverage imported but no row-fitting finite payment",
            },
            {
                "terminal": "UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP",
                "condition": "deg gcd(P,Q)<k-2",
                "reason": "gcd-reduced map need not be projective linear",
            },
        ],
        "scope_guards": {
            "projective_base_pair_owner_proved": True,
            "full_outside_split_maximal_gcd_coefficient_deformation_closed": True,
            "general_maximal_gcd_coefficient_deformation_closed": False,
            "field_full_local_subline_closed": False,
            "degree_two_or_three_proper_field_payment_proved": False,
            "lower_gcd_payment_proved": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "source_bindings": expected_source_bindings(),
        "payload_sha256": "",
    }
    result["payload_sha256"] = payload_hash(result)
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
        ("kind", lambda d: d.__setitem__("artifact_kind", "ROW_CLOSURE")),
        ("status", lambda d: d.__setitem__("status", "KOALABEAR_CLOSED")),
        ("row-p", lambda d: d["row"].__setitem__("p", P + 1)),
        ("object", lambda d: d["counted_object_contract"].__setitem__("object", "witnesses")),
        ("cross-pair", lambda d: d["counted_object_contract"].__setitem__("cross_received_pair_union_required", True)),
        ("infinity-finite", lambda d: d["counted_object_contract"].__setitem__("projective_infinity_is_not_a_finite_slope", False)),
        ("owner-order", lambda d: d["first_match_partition"]["order"].reverse()),
        ("owner-index", lambda d: d["first_match_partition"].__setitem__("projective_base_pair_C5_index_one_based", 7)),
        ("extension-only", lambda d: d["first_match_partition"].__setitem__("projective_base_pair_cell_is_not_extension_only", False)),
        ("not-all-post5", lambda d: d["first_match_partition"].__setitem__("projective_base_pair_cell_owns_all_post5_slopes", False)),
        ("later-not-empty", lambda d: d["first_match_partition"].__setitem__("later_cells_empty_when_projective_field_is_base", False)),
        ("not-monotone", lambda d: d["first_match_partition"].__setitem__("monotone_under_actual_earlier_deletion", False)),
        ("rank-zero", lambda d: d["joint_owner_theorem"].__setitem__("rank_zero_noncontained_fiber_empty", False)),
        ("support-projectivity", lambda d: d["joint_owner_theorem"].__setitem__("one_pair_global_projectivity_for_all_supports", False)),
        ("projective-size-p", lambda d: d["joint_owner_theorem"].__setitem__("projective_subline_size", P)),
        ("finite-cap-p", lambda d: d["joint_owner_theorem"].__setitem__("finite_chart_uniform_cap", P)),
        ("sum-cases", lambda d: d["joint_owner_theorem"].__setitem__("case_combination", "SUM")),
        ("wrong-formula", lambda d: d["joint_owner_theorem"].__setitem__("joint_cap_formula", "2p+1")),
        ("add-block", lambda d: d["joint_owner_theorem"].__setitem__("adds_second_independent_block", True)),
        ("not-replace", lambda d: d["joint_owner_theorem"].__setitem__("replaces_existing_base_block", False)),
        ("earlier-increase", lambda d: d["joint_owner_theorem"].__setitem__("earlier_deletion_can_increase_cap", True)),
        ("source-not-zero", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("full_outside_source_zero_off_Sigma", False)),
        ("not-split", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("split_common_root_count", "c_L<k-2")),
        ("degree-implies-split", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("degree_gcd_k_minus_2_alone_implies_split_base_locator", True)),
        ("matrix-singular", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("coefficient_matrix_invertible", False)),
        ("field-full", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("intrinsic_projective_field", "F_(p^6)")),
        ("rank-one", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("transverse_source_syndrome_rank", 1)),
        ("generic-descent", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("generic_support_local_subline_implies_global_descent", True)),
        ("generic-gcd-closed", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("generic_nonsplit_maximal_gcd_absorbed", True)),
        ("old-terminal", lambda d: d["full_outside_split_maximal_gcd_absorption"].__setitem__("corrected_terminal", "UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2")),
        ("toy-five", lambda d: d["exact_control"].__setitem__("finite_slopes", 5)),
        ("toy-base", lambda d: d["exact_control"].__setitem__("base_slopes", 6)),
        ("toy-field", lambda d: d["exact_control"].__setitem__("intrinsic_projective_field", "GF(5^6)")),
        ("nonsplit-base", lambda d: d["exact_control"].__setitem__("nonsplit_countercontrol_intrinsic_projective_field", "GF(11)")),
        ("degree-descent", lambda d: d["exact_control"].__setitem__("degree_alone_base_descent_refuted", False)),
        ("toy-proof", lambda d: d["exact_control"].__setitem__("scale", "SYMBOLIC_PROOF")),
        ("old-cap", lambda d: d["ledger"].__setitem__("old_base_block_cap", str(P + 1))),
        ("new-cap", lambda d: d["ledger"].__setitem__("new_joint_block_cap", str(P))),
        ("ledger-sum", lambda d: d["ledger"].__setitem__("replacement_not_addition", False)),
        ("ledger-move", lambda d: d["ledger"].__setitem__("ledger_movement", str(P + 1))),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("B-rem", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_BEFORE))),
        ("UA-stale", lambda d: d["ledger"].__setitem__("projective_base_stratum_deleted_before_residual_U_A", False)),
        ("UQ", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("tail", lambda d: d["rank9_updated_gate"].__setitem__("new_tail_target", str(OLD_TAIL_TARGET))),
        ("E-max", lambda d: d["rank9_updated_gate"].__setitem__("new_aggregate_excess_max", str(OLD_E_MAX))),
        ("E-drop", lambda d: d["rank9_updated_gate"].__setitem__("aggregate_excess_drop", str(E_MAX_DROP - 1))),
        ("K-rem", lambda d: d["rank9_updated_gate"].__setitem__("K_remaining_after", K_REMAINING - 1)),
        ("break-J", lambda d: d["rank9_updated_gate"].__setitem__("maximal_gcd_break_J", 165)),
        ("route-delete", lambda d: d["residual_route_cuts"].pop()),
        ("field-full-closed", lambda d: d["scope_guards"].__setitem__("field_full_local_subline_closed", True)),
        ("general-gcd-closed", lambda d: d["scope_guards"].__setitem__("general_maximal_gcd_coefficient_deformation_closed", True)),
        ("p2-paid", lambda d: d["scope_guards"].__setitem__("degree_two_or_three_proper_field_payment_proved", True)),
        ("lower-gcd-paid", lambda d: d["scope_guards"].__setitem__("lower_gcd_payment_proved", True)),
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
    print(
        "M1 projective-base-pair C5 owner mutations: "
        f"{rejected}/{rejected} PASS"
    )
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
    print("M1 projective-base-pair C5 owner: PASS")
    print(f"  joint owner cap: p -> p+1 ({P:,} -> {P + 1:,})")
    print(f"  U_paid: {U_PAID_BEFORE:,} -> {U_PAID_AFTER:,}")
    print(
        "  B_remaining: "
        f"{B_REMAINING_BEFORE:,} -> {B_REMAINING_AFTER:,}"
    )
    print(f"  rank-nine T_{CUTOFF_D}: {NEW_TAIL_TARGET:,}")
    print(
        "  full-outside split-maximal-gcd coefficient deformation: "
        "PAID_PAIR_PROJECTIVE_BASE_SUBLINE_C5"
    )
    print(
        "  nonsplit/field-full/lower-gcd residuals: OPEN; "
        "KoalaBear row remains YELLOW"
    )
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
