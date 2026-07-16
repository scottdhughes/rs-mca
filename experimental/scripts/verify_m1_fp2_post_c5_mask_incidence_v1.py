#!/usr/bin/env python3
"""Verify the M1 F_(p^2) mask audit and post-projective-C5 incidence split."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-fp2-post-c5-mask-incidence-v1"
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/m1-fp2-post-c5-mask-incidence-v1"
)
CERT_PATH = CERT_DIR / "m1_fp2_post_c5_mask_incidence_v1.json"

NOTE_REL = Path("experimental/notes/m1/m1_fp2_post_c5_mask_incidence_v1.md")
VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.sage"
)
PREDECESSOR_NOTE_REL = Path(
    "experimental/notes/m1/m1_fp2_residual_route_cut_v1.md"
)
PREDECESSOR_CERT_REL = Path(
    "experimental/data/certificates/m1-fp2-residual-route-cut-v1/"
    "m1_fp2_residual_route_cut_v1.json"
)
PREDECESSOR_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py"
)
KB_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
)
KB_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/"
    "kb_mca_1116048_first_match_ledger_v1.json"
)
PROJECTIVE_REL = Path(
    "experimental/notes/thresholds/projective_syndrome_c5_first_match.md"
)
FRONTIERS_REL = Path("experimental/asymptotic_rs_mca_frontiers.tex")
COMPACT_REL = Path("experimental/asymptotic_rs_mca.tex")
TRANSVERSE_REL = Path(
    "experimental/notes/thresholds/agreement_weighted_transverse_secant.md"
)
BASE_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-base-slope-universe-v2/"
    "kb_mca_1116048_base_slope_universe_v2.json"
)

P = 2_130_706_433
P2 = P**2
P3 = P**3
P6 = P**6
N = 2_097_152
K_DIM = 1_048_576
A = 1_116_048
J = N - A
T = A - K_DIM
W = T - 1
B_STAR = P6 // (1 << 128)
U_PAID = 2_602_153_473
B_REM = B_STAR - U_PAID
SCALARIZED_QUOTIENT_DIMENSION = 3 * T
LOW_EXCESS_CAP = math.comb((N - K_DIM) + 2, 3) // math.comb(A - K_DIM + 1, 2)

KB_FIRST_FIVE = [
    "contained_or_noncontained_failure",
    "rank_drop_or_pivot_failure",
    "tangent_common_line_residue",
    "quotient_periodic_or_divisor_stabilized",
    "planted_prefix_structured",
]
PROJECTIVE_FIRST_FIVE = [
    "quotient_pullback",
    "chebyshev_dihedral",
    "planted_block",
    "tangent_deep_common_line",
    "extension_proper_field_descent",
]

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "provenance",
    "source_bindings",
    "row",
    "policy_compatibility",
    "mask_inventory",
    "projective_c5_refinement",
    "incidence_classification",
    "global_rank_components",
    "full_field_control",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}


class VerificationError(RuntimeError):
    """Raised for parser, source-binding, or semantic certificate failures."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def require_int(value: Any, label: str) -> None:
    require(type(value) is int, f"{label} is not an exact JSON integer")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in out, f"duplicate JSON key: {key}")
        out[key] = value
    return out


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON value is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON artifact: {path.relative_to(ROOT)}")
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    payload = copy.deepcopy(value)
    payload["payload_sha256"] = ""
    return canonical_hash(payload)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding(binding_id: str, rel_path: Path, role: str) -> dict[str, str]:
    path = ROOT / rel_path
    require(path.is_file(), f"missing source binding: {rel_path}")
    return {
        "binding_id": binding_id,
        "path": rel_path.as_posix(),
        "sha256": file_hash(path),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        source_binding("packet-note", NOTE_REL, "human-readable proof audit"),
        source_binding("python-verifier", VERIFIER_REL, "builder and mutation verifier"),
        source_binding("sage-control", SAGE_REL, "independent full-field rank-two control"),
        source_binding("fp2-predecessor-note", PREDECESSOR_NOTE_REL, "scalarization and open mask interface"),
        source_binding("fp2-predecessor-certificate", PREDECESSOR_CERT_REL, "machine-readable predecessor"),
        source_binding("fp2-predecessor-verifier", PREDECESSOR_VERIFIER_REL, "predecessor semantic replay"),
        source_binding("kb-first-match-note", KB_NOTE_REL, "frozen branch order and source statuses"),
        source_binding("kb-first-match-certificate", KB_CERT_REL, "machine-readable branch metadata"),
        source_binding("projective-c5", PROJECTIVE_REL, "integrated #660 canonical proper-field coverage and post-C5 theorem"),
        source_binding("frontiers-cells", FRONTIERS_REL, "profile cells and first-match definitions"),
        source_binding("compact-catalogue", COMPACT_REL, "C1-C5 catalogue order"),
        source_binding("rank-one-source", TRANSVERSE_REL, "integrated #670 rank-one and fixed-low-excess owner"),
        source_binding("base-ledger", BASE_CERT_REL, "current paid baseline and first-match order"),
    ]


def mask_inventory() -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "branch": KB_FIRST_FIVE[0],
            "machine_status": "MACHINE_EXACT_GATE_ONLY",
            "executable_predicate": "ALL_SIX_SCALARIZED_SUPPORT_QUOTIENT_SYNDROMES_ZERO",
            "actual_slope_projector_complete": False,
            "paid_owner": False,
            "source_status": "INTERFACE_BUCKET_NOT_A_DEDUCTED_SAFE_CELL",
            "blocker": "GATE_IS_EXACT_BUT_SOURCE_DOES_NOT_DEFINE_A_PAID_BRANCH_PROJECTOR",
        },
        {
            "order": 2,
            "branch": KB_FIRST_FIVE[1],
            "machine_status": "UNBOUND_SOURCE_SYMBOL",
            "executable_predicate": None,
            "actual_slope_projector_complete": False,
            "paid_owner": False,
            "source_status": "OPEN_EXACT_MINOR_OR_PIVOT_BUCKET_REQUIRED",
            "blocker": "NO_DEPLOYED_SUPPORT_TO_B0_BUILDER_OR_COMPLETE_PIVOT_ORDER",
        },
        {
            "order": 3,
            "branch": KB_FIRST_FIVE[2],
            "machine_status": "SOURCE_STATUS_ONLY",
            "executable_predicate": None,
            "actual_slope_projector_complete": False,
            "paid_owner": False,
            "source_status": "OPEN_FOR_THIS_ROW",
            "blocker": "NO_ROW_SPECIFIC_MATRIX_INDEPENDENT_MINORS_OR_SLOPE_PROJECTOR",
        },
        {
            "order": 4,
            "branch": KB_FIRST_FIVE[3],
            "machine_status": "PARTIAL_FAMILY_NO_COMPLETE_PROJECTOR",
            "executable_predicate": "DECLARED_Q0_DYADIC_RUNG_PREDICATES_ONLY",
            "actual_slope_projector_complete": False,
            "paid_owner": False,
            "source_status": "PARTIAL_PROVED_DESCENT_WITH_TERMINAL_RAW_PAID",
            "blocker": "LOWER_RUNG_OBLIGATIONS_AND_LARGE_PLANTED_TAILS_REMAIN_OPEN",
        },
        {
            "order": 5,
            "branch": KB_FIRST_FIVE[4],
            "machine_status": "SOURCE_STATUS_ONLY",
            "executable_predicate": None,
            "actual_slope_projector_complete": False,
            "paid_owner": False,
            "source_status": "OPEN_EXACT_IMAGE_COST_REQUIRED",
            "blocker": "NO_EXHAUSTIVE_ALGEBRAICALLY_PLANTED_FAMILY_OR_PROJECTOR",
        },
    ]


def incidence_counts(q: int, m: int) -> dict[str, int]:
    require(q >= 2 and m >= 1, "invalid incidence count parameters")
    space = q**m
    return {
        "q": q,
        "m": m,
        "quotient_space_size": space,
        "ordered_pair_total": space**2,
        "contained_zero_zero": 1,
        "zero_second_inconsistent": space - 1,
        "unique_root_pairs": q * (space - 1),
        "nonproportional_inconsistent": space**2 - (q + 1) * space + q,
    }


EDGE_CASES = [
    "After KoalaBear branch 5 and post-projective-C5 are different predicates.",
    "The proper intermediate fields of F_(p^6)/F_p have degrees 1, 2, and 3.",
    "The projective-field test belongs to the global pair syndrome, not a support quotient.",
    "Canonical C5 coverage is not a finite KoalaBear payment.",
    "Zero/zero quotient columns are contained and cannot be retained as a noncontained witness.",
    "Fixed-support uniqueness does not imply d_eff<=1 or a support-union bound.",
    "Within-line roots are deduplicated; across lines the operation is a supremum or maximum.",
    "Null is not zero.",
]

REMAINING_RISKS = [
    "KoalaBear branches 2 through 5 do not have a complete executable predicate adapter.",
    "The canonical proper-field C5 refinement is routed but not assigned a finite KoalaBear charge.",
    "Field-full syndrome-rank-two roots may vary over exponentially many supports.",
    "The exact full-field control is not proved to survive the deployed KoalaBear branch-1-through-5 masks.",
    "U_Q and U_A remain open, so no adjacent-row inequality is decided.",
]

NONCLAIMS = [
    "This packet does not identify KoalaBear branch 5 with projective C5.",
    "This packet does not claim a complete branch-1-through-5 mask replay.",
    "This packet does not pay the proper-field C5 cell or the field-full rank-two residual.",
    "This packet does not promote fixed-support uniqueness to a support-union bound.",
    "This packet does not set U_2, U_Q, or U_A, change the ledger, or improve the public frontier.",
    "This packet does not begin the degree-three parameter-field class.",
]


def build_certificate() -> dict[str, Any]:
    inventory = mask_inventory()
    control_counts = incidence_counts(4, 2)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": "M1_FP2_POST_C5_MASK_INCIDENCE_ROUTE_CUT",
        "status": "PROVED_NEW_POLICY_AND_TWO_COLUMN_SPLIT_IMPORTED_C5_RANK_CLOSURES_APPLIED_ROW_OPEN",
        "provenance": {
            "integrated_imports": [
                {
                    "source_pr": 660,
                    "source_commit": "0be98005cc5055ff34fd73c6c9c222ba4377a604",
                    "integration_commit": "ea4eb0784417ca5ab503a3c31a7eef6464ad100a",
                    "applied_results": [
                        "CANONICAL_PROPER_FIELD_C5_COVERAGE",
                        "GLOBAL_SYNDROME_RANK_ZERO_EMPTINESS",
                        "POST_C5_NONEMPTY_IMPLIES_FULL_PROJECTIVE_FIELD",
                    ],
                },
                {
                    "source_pr": 670,
                    "source_commits": [
                        "19c28c758abed1813b79e67ca996fb18392240a1",
                        "3a35278f81b63e6247dd660fc147d2a87fc89ba5",
                        "08198f1b7c116710f3b0ba80d4bc00427ed0fe7a",
                    ],
                    "integration_commit": "ea4eb0784417ca5ab503a3c31a7eef6464ad100a",
                    "applied_results": [
                        "GLOBAL_SYNDROME_RANK_ONE_AT_MOST_ONE_SLOPE",
                        "FIXED_LOW_EXCESS_U_CAP_84416263",
                    ],
                },
            ],
            "new_in_this_packet": [
                "KB_VS_PROJECTIVE_POLICY_MISMATCH",
                "FROZEN_SOURCE_STATUS_INVENTORY",
                "EXACT_QUOTIENT_PAIR_CENSUS",
                "BASIS_RELATIVE_DISJOINT_PIVOT_ATLAS",
                "FULL_FIELD_QUADRATIC_COMPATIBILITY_CONTROL",
                "FIELD_FULL_RANK_TWO_UNPAID_ROUTE_CUT",
            ],
        },
        "source_bindings": expected_source_bindings(),
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "ambient_extension_degree": 6,
            "parameter_extension_degree": 2,
            "q_line": str(P6),
            "parameter_field_order": str(P2),
            "n": N,
            "k": K_DIM,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
            "prefix_depth_w": W,
            "B_star": str(B_STAR),
            "U_paid": str(U_PAID),
            "B_remaining": str(B_REM),
            "U_Q": None,
            "U_A": None,
        },
        "policy_compatibility": {
            "kb_first_five": KB_FIRST_FIVE,
            "projective_first_five": PROJECTIVE_FIRST_FIVE,
            "orders_identical": False,
            "kb_branch_5": "planted_prefix_structured",
            "projective_c5": "extension_proper_field_descent",
            "kb_branch_5_equals_projective_c5": False,
            "literal_adapter_proved": False,
            "current_fp2_post5_implies_full_projective_field": False,
            "reason": "THE_PREDECESSOR_SUBTRACTS_KB_BRANCHES_1_TO_5_BUT_NOT_THE_SEPARATE_CANONICAL_PROPER_FIELD_C5_CELL",
            "required_branch_6_refinement": [
                "6a_projective_proper_field_C5",
                "6b_extension_slope_pair_field_full",
            ],
        },
        "mask_inventory": {
            "records": inventory,
            "record_count": len(inventory),
            "canonical_sha256": canonical_hash(inventory),
            "complete_executable_adapter": False,
            "first_missing_executable_branch": 2,
            "machine_exact_gate_count": 1,
            "complete_slope_projector_count": 0,
            "verdict": "UNPAID_MASK_ADAPTER_MISSING",
        },
        "projective_c5_refinement": {
            "provenance": "IMPORTED_FROM_INTEGRATED_PR_660_AND_APPLIED_IN_NEW_PARTITION",
            "global_syndrome_matrix": "Y_R=[y_0 y_1]",
            "positive_rank_values": [1, 2],
            "proper_intermediate_degrees": [1, 2, 3],
            "proper_intermediate_orders": [str(P), str(P2), str(P3)],
            "field_definition_test": "rank([Y_R|Y_R^(p^e)])=rank(Y_R)",
            "full_field_test": "rank([Y_R|Y_R^(p^e)])>rank(Y_R)_FOR_e_IN_1_2_3",
            "support_quotient_substitution_allowed": False,
            "proper_field_cell_witness_exhaustive": True,
            "proper_field_cell_paid_in_this_packet": False,
            "post_c5_nonempty_implies_full_projective_field": True,
            "refined_components": {
                "6a_projective_proper_field_C5": "ROUTED_UNPAID_COVERAGE_NOT_PAYMENT",
                "6b_extension_slope_pair_field_full": "ACTIVE_INCIDENCE_CLASSIFICATION",
            },
        },
        "incidence_classification": {
            "ambient_quotient": "Q_E=(K^(n-k)/V_E(K))^3",
            "equation": "ybar_0+gamma*ybar_1=0",
            "nonbase_condition": "gamma^p-gamma!=0",
            "cases": [
                {
                    "case_id": "ZERO_ZERO",
                    "predicate": "ybar_0=0_AND_ybar_1=0",
                    "terminal": "CONTAINED_BRANCH_1_INTERFACE",
                    "root_count": None,
                    "retained_noncontained": False,
                },
                {
                    "case_id": "ZERO_SECOND_NONZERO_FIRST",
                    "predicate": "ybar_1=0_AND_ybar_0!=0",
                    "terminal": "AFFINE_INCONSISTENT",
                    "root_count": 0,
                    "retained_noncontained": False,
                },
                {
                    "case_id": "NONPROPORTIONAL",
                    "predicate": "rank_K([ybar_0 ybar_1])=2",
                    "terminal": "AFFINE_INCONSISTENT",
                    "root_count": 0,
                    "retained_noncontained": False,
                },
                {
                    "case_id": "PROPORTIONAL_NONZERO_SECOND",
                    "predicate": "ybar_1!=0_AND_ybar_0=c*ybar_1",
                    "terminal": "UNIQUE_ROOT_gamma=-c",
                    "root_count": 1,
                    "retained_noncontained": True,
                },
            ],
            "unique_root_subroutes": [
                "gamma_in_F_p_TO_RESIDUAL_BASE_SLOPE_UNIVERSE_OUTSIDE_R2",
                "gamma_in_F_(p^2)_MINUS_F_p_AND_PAIR_FIELD_PROPER_TO_6a",
                "gamma_in_F_(p^2)_MINUS_F_p_AND_PAIR_FIELD_FULL_TO_6b",
            ],
            "fixed_support_root_cap": 1,
            "fixed_support_cap_extends_to_support_union": False,
            "basis_relative_pivot_atlas": {
                "coordinate_dimension": SCALARIZED_QUOTIENT_DIMENSION,
                "pivot_labels_per_support": SCALARIZED_QUOTIENT_DIMENSION,
                "coordinate_model": "FIX_ANY_ORDERED_K_BASIS_OF_Q_E_PER_SUPPORT",
                "deterministic_support_to_basis_adapter_deployed": False,
                "pivot_rule": "j=FIRST_NONZERO_COORDINATE_OF_v_E",
                "earlier_zero_equations": "v_E[i]=0_FOR_i<j",
                "pivot_inequation": "v_E[j]!=0",
                "proportionality_equations": "v_E[j]*u_E[l]-u_E[j]*v_E[l]=0_FOR_l!=j",
                "root_formula": "gamma=-u_E[j]/v_E[j]",
                "nonbase_inequation": "gamma^p-gamma!=0",
                "charts_disjoint": True,
                "charts_exhaust_unique_nonbase_root_locus": True,
                "is_kb_branch_1_to_5_mask_atlas": False,
            },
            "symbolic_census": {
                "contained": "1",
                "zero_second_inconsistent": "q^m-1",
                "unique_root_pairs": "q*(q^m-1)",
                "nonproportional_inconsistent": "q^(2m)-(q+1)*q^m+q",
            },
            "exact_control_q4_m2": control_counts,
            "control_partition_sums_to_total": (
                control_counts["contained_zero_zero"]
                + control_counts["zero_second_inconsistent"]
                + control_counts["unique_root_pairs"]
                + control_counts["nonproportional_inconsistent"]
                == control_counts["ordered_pair_total"]
            ),
        },
        "global_rank_components": [
            {
                "component_id": "GLOBAL_SYNDROME_RANK_0",
                "condition": "rank(Y_R)=0",
                "provenance": "IMPORTED_FROM_INTEGRATED_PR_660_AND_APPLIED_HERE",
                "terminal": "EMPTY_NONCONTAINED_WITNESS_INCIDENCE",
                "uniform_slope_cap": 0,
                "closed": True,
            },
            {
                "component_id": "POST_C5_FULL_FIELD_GLOBAL_SYNDROME_RANK_1",
                "condition": "F_proj(R)=F_(p^6)_AND_rank(Y_R)=1",
                "provenance": "IMPORTED_FROM_INTEGRATED_PR_670_AND_APPLIED_HERE",
                "terminal": "BUDGET_FITTING_EXACT_ROOT_UNION_DEGREE_AT_MOST_1",
                "uniform_slope_cap": 1,
                "closed": True,
            },
            {
                "component_id": "POST_C5_FULL_FIELD_GLOBAL_SYNDROME_RANK_2",
                "condition": "F_proj(R)=F_(p^6)_AND_rank(Y_R)=2",
                "provenance": "NEW_ROUTE_CUT_IN_THIS_PACKET",
                "terminal": "UNPAID_SUPPORT_TO_SLOPE_UNION",
                "uniform_slope_cap": None,
                "closed": False,
                "existing_owner_subroute": {
                    "owner": "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT_FIXED_LOW_EXCESS_U",
                    "provenance": "IMPORTED_FROM_INTEGRATED_PR_670_AND_APPLIED_CONDITIONALLY",
                    "hypothesis": "|U|=(n-k)+2_AND_ALL_SELECTED_DISCREPANCIES_SUBSET_U",
                    "uniform_slope_cap": LOW_EXCESS_CAP,
                    "fits_current_remainder": LOW_EXCESS_CAP <= B_REM,
                    "exhaustive_low_excess_shadow_cover_proved": False,
                },
            },
        ],
        "full_field_control": {
            "purpose": "REFUTE_FULL_PAIR_FIELD_IMPLIES_NO_QUADRATIC_PARAMETER_ROOT",
            "base_field": "F_7",
            "parameter_field": "F_(7^2)",
            "ambient_field": "F_(7^6)",
            "code": "weighted_RS_F(D={0,1,2,3},k=1)",
            "discrepancy_support": [0, 1],
            "agreement_support": [2, 3],
            "global_syndrome_rank": 2,
            "gamma_in_parameter_field": True,
            "gamma_in_base_field": False,
            "projective_field_full": True,
            "fixed_support_equation_holds": True,
            "support_noncontained": True,
            "received_pair_realizable": True,
            "survives_deployed_kb_branches_1_to_5_proved": False,
            "verdict": "FULL_FIELD_RANK2_K_MINUS_B_ROOT_IS_COMPATIBLE",
        },
        "ledger": {
            "rank_zero_component_closed": True,
            "rank_one_component_closed": True,
            "rank_one_uniform_cap": 1,
            "pair_rank_cases_combine_by": "MAXIMUM_NOT_SUM",
            "proper_field_c5_charge": None,
            "field_full_rank_two_charge": None,
            "U_2": None,
            "U_Q": None,
            "U_A": None,
            "ledger_consequence": False,
            "row_complete": False,
            "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
            "next_attack": "ROW_SPECIFIC_BRANCH_2_PIVOT_MATRIX_AND_SUPPORT_TO_ROW_ADAPTER",
        },
        "audit_sections": {
            "parameter_dependence": "FIELD_TEST_UNIFORM_TOWER_AND_MASK_AUDIT_REPOSITORY_SPECIFIC_ROW_LEDGER_KOALABEAR_SPECIFIC",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "numerical_evidence": "EXACT_IDENTITIES_AND_EXACT_SAGE_CONTROL_ONLY",
            "edge_cases": EDGE_CASES,
            "remaining_risks": REMAINING_RISKS,
        },
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list, "source_bindings is not a list")
    require(bindings == expected_source_bindings(), "source binding path/hash/role drift")
    ids = [entry["binding_id"] for entry in bindings]
    require(len(ids) == len(set(ids)), "duplicate source binding id")


def validate_sources() -> None:
    predecessor = load_json(ROOT / PREDECESSOR_CERT_REL)
    require(
        predecessor["first_match_scope"]["mask_predicates_machine_encoded"] is False,
        "predecessor no longer records the missing mask adapter",
    )
    require(
        predecessor["first_match_scope"]["earlier_branch_count"] == 5,
        "predecessor earlier-branch count drift",
    )
    kb = load_json(ROOT / KB_CERT_REL)
    branches = kb["first_match_branches"]
    require(
        [entry["branch"] for entry in branches[:5]] == KB_FIRST_FIVE,
        "KB first-five order drift",
    )
    expected_statuses = [
        entry["source_status"] for entry in mask_inventory()
    ]
    require(
        [entry["status"] for entry in branches[:5]] == expected_statuses,
        "KB first-five source status drift",
    )
    base = load_json(ROOT / BASE_CERT_REL)
    require(
        base["first_match"]["v2_order"][:5] == KB_FIRST_FIVE,
        "base-v2 first-five order drift",
    )
    require(int(base["arithmetic"]["new_U_paid"]) == U_PAID, "current paid baseline drift")


def validate(artifact: dict[str, Any], *, exact_rebuild: bool = True) -> None:
    require(set(artifact) == TOP_KEYS, "top-level keys drift")
    require(artifact["schema"] == SCHEMA, "schema drift")
    require(
        artifact["artifact_kind"]
        == "M1_FP2_POST_C5_MASK_INCIDENCE_ROUTE_CUT",
        "artifact kind drift",
    )
    require(
        artifact["status"]
        == "PROVED_NEW_POLICY_AND_TWO_COLUMN_SPLIT_IMPORTED_C5_RANK_CLOSURES_APPLIED_ROW_OPEN",
        "status drift",
    )
    provenance = artifact["provenance"]
    require(
        [entry["source_pr"] for entry in provenance["integrated_imports"]]
        == [660, 670],
        "integrated provenance PR order drift",
    )
    require(
        provenance["integrated_imports"][0]["integration_commit"]
        == provenance["integrated_imports"][1]["integration_commit"]
        == "ea4eb0784417ca5ab503a3c31a7eef6464ad100a",
        "integration provenance drift",
    )
    require(
        provenance["new_in_this_packet"]
        == [
            "KB_VS_PROJECTIVE_POLICY_MISMATCH",
            "FROZEN_SOURCE_STATUS_INVENTORY",
            "EXACT_QUOTIENT_PAIR_CENSUS",
            "BASIS_RELATIVE_DISJOINT_PIVOT_ATLAS",
            "FULL_FIELD_QUADRATIC_COMPATIBILITY_CONTROL",
            "FIELD_FULL_RANK_TWO_UNPAID_ROUTE_CUT",
        ],
        "new-result provenance drift",
    )
    validate_source_bindings(artifact["source_bindings"])
    validate_sources()

    row = artifact["row"]
    for key in (
        "p",
        "ambient_extension_degree",
        "parameter_extension_degree",
        "n",
        "k",
        "agreement_A",
        "error_count_j",
        "syndrome_depth_t",
        "prefix_depth_w",
    ):
        require_int(row[key], f"row.{key}")
    require(
        (
            row["p"],
            row["ambient_extension_degree"],
            row["parameter_extension_degree"],
            row["n"],
            row["k"],
            row["agreement_A"],
            row["error_count_j"],
            row["syndrome_depth_t"],
            row["prefix_depth_w"],
        )
        == (P, 6, 2, N, K_DIM, A, J, T, W),
        "row arithmetic drift",
    )
    require(int(row["q_line"]) == P6, "line field drift")
    require(int(row["parameter_field_order"]) == P2, "parameter field drift")
    require(int(row["B_star"]) == B_STAR, "B_star drift")
    require(int(row["U_paid"]) == U_PAID and int(row["B_remaining"]) == B_REM, "ledger arithmetic drift")
    require(row["U_Q"] is None and row["U_A"] is None, "open row terms changed")

    policy = artifact["policy_compatibility"]
    require(policy["kb_first_five"] == KB_FIRST_FIVE, "KB policy drift")
    require(policy["projective_first_five"] == PROJECTIVE_FIRST_FIVE, "projective policy drift")
    require(policy["orders_identical"] is False, "incompatible policies called identical")
    require(policy["kb_branch_5_equals_projective_c5"] is False, "C5 falsely aliased")
    require(policy["literal_adapter_proved"] is False, "missing adapter invented")
    require(
        policy["current_fp2_post5_implies_full_projective_field"] is False,
        "predecessor residual falsely called post-projective-C5",
    )
    require(
        policy["required_branch_6_refinement"]
        == [
            "6a_projective_proper_field_C5",
            "6b_extension_slope_pair_field_full",
        ],
        "branch-6 refinement drift",
    )

    inventory = artifact["mask_inventory"]
    expected_inventory = mask_inventory()
    require(inventory["records"] == expected_inventory, "mask inventory drift")
    require(inventory["record_count"] == 5, "mask inventory count drift")
    require(
        inventory["canonical_sha256"] == canonical_hash(expected_inventory),
        "mask inventory digest drift",
    )
    require(inventory["complete_executable_adapter"] is False, "mask adapter falsely complete")
    require(inventory["first_missing_executable_branch"] == 2, "first missing branch drift")
    require(inventory["machine_exact_gate_count"] == 1, "exact gate count drift")
    require(inventory["complete_slope_projector_count"] == 0, "complete projector invented")
    require(inventory["verdict"] == "UNPAID_MASK_ADAPTER_MISSING", "mask verdict drift")

    c5 = artifact["projective_c5_refinement"]
    require(
        c5["provenance"]
        == "IMPORTED_FROM_INTEGRATED_PR_660_AND_APPLIED_IN_NEW_PARTITION",
        "C5 provenance drift",
    )
    require(c5["positive_rank_values"] == [1, 2], "positive rank list drift")
    require(c5["proper_intermediate_degrees"] == [1, 2, 3], "proper field degree list drift")
    require(
        [int(value) for value in c5["proper_intermediate_orders"]]
        == [P, P2, P3],
        "proper field orders drift",
    )
    require(c5["support_quotient_substitution_allowed"] is False, "local quotient substituted for global field test")
    require(c5["proper_field_cell_witness_exhaustive"] is True, "canonical C5 coverage lost")
    require(c5["proper_field_cell_paid_in_this_packet"] is False, "proper-field C5 falsely paid")
    require(c5["post_c5_nonempty_implies_full_projective_field"] is True, "post-C5 theorem lost")
    require(
        c5["refined_components"]["6a_projective_proper_field_C5"]
        == "ROUTED_UNPAID_COVERAGE_NOT_PAYMENT",
        "proper-field route status drift",
    )

    incidence = artifact["incidence_classification"]
    require(incidence["equation"] == "ybar_0+gamma*ybar_1=0", "incidence equation drift")
    cases = incidence["cases"]
    require([entry["case_id"] for entry in cases] == [
        "ZERO_ZERO",
        "ZERO_SECOND_NONZERO_FIRST",
        "NONPROPORTIONAL",
        "PROPORTIONAL_NONZERO_SECOND",
    ], "incidence case order drift")
    require(cases[0]["retained_noncontained"] is False and cases[0]["root_count"] is None, "zero/zero classification drift")
    require(cases[1]["root_count"] == 0, "zero-second case assigned a root")
    require(cases[2]["root_count"] == 0, "nonproportional case assigned a root")
    require(cases[3]["root_count"] == 1 and cases[3]["retained_noncontained"], "unique-root case drift")
    require(
        incidence["unique_root_subroutes"][0]
        == "gamma_in_F_p_TO_RESIDUAL_BASE_SLOPE_UNIVERSE_OUTSIDE_R2",
        "base root retained in R2",
    )
    require(incidence["fixed_support_root_cap"] == 1, "fixed-support root cap drift")
    require(
        incidence["fixed_support_cap_extends_to_support_union"] is False,
        "fixed-support cap promoted to union",
    )
    pivot = incidence["basis_relative_pivot_atlas"]
    require(
        pivot["coordinate_dimension"]
        == pivot["pivot_labels_per_support"]
        == SCALARIZED_QUOTIENT_DIMENSION
        == 202_416,
        "basis-relative pivot dimension drift",
    )
    require(
        pivot["coordinate_model"]
        == "FIX_ANY_ORDERED_K_BASIS_OF_Q_E_PER_SUPPORT",
        "pivot coordinate model drift",
    )
    require(
        pivot["deterministic_support_to_basis_adapter_deployed"] is False,
        "undeployed deterministic quotient-basis adapter invented",
    )
    require(pivot["pivot_rule"] == "j=FIRST_NONZERO_COORDINATE_OF_v_E", "pivot rule drift")
    require(pivot["earlier_zero_equations"] == "v_E[i]=0_FOR_i<j", "earlier pivot zero equations drift")
    require(pivot["pivot_inequation"] == "v_E[j]!=0", "pivot inequation drift")
    require(
        pivot["proportionality_equations"]
        == "v_E[j]*u_E[l]-u_E[j]*v_E[l]=0_FOR_l!=j",
        "pivot proportionality equations drift",
    )
    require(pivot["nonbase_inequation"] == "gamma^p-gamma!=0", "pivot nonbase inequation drift")
    require(pivot["charts_disjoint"] is True, "pivot charts not disjoint")
    require(pivot["charts_exhaust_unique_nonbase_root_locus"] is True, "pivot atlas not exhaustive")
    require(pivot["is_kb_branch_1_to_5_mask_atlas"] is False, "incidence pivots mislabelled as KB masks")
    control_counts = incidence_counts(4, 2)
    require(incidence["exact_control_q4_m2"] == control_counts, "q=4,m=2 census drift")
    require(incidence["control_partition_sums_to_total"] is True, "incidence partition sum drift")
    require(
        sum(
            control_counts[key]
            for key in (
                "contained_zero_zero",
                "zero_second_inconsistent",
                "unique_root_pairs",
                "nonproportional_inconsistent",
            )
        )
        == control_counts["ordered_pair_total"]
        == 256,
        "exact incidence control arithmetic failure",
    )

    components = artifact["global_rank_components"]
    require([entry["component_id"] for entry in components] == [
        "GLOBAL_SYNDROME_RANK_0",
        "POST_C5_FULL_FIELD_GLOBAL_SYNDROME_RANK_1",
        "POST_C5_FULL_FIELD_GLOBAL_SYNDROME_RANK_2",
    ], "global rank component order drift")
    require(components[0]["closed"] and components[0]["uniform_slope_cap"] == 0, "rank-zero closure drift")
    require(components[1]["closed"] and components[1]["uniform_slope_cap"] == 1, "rank-one closure drift")
    require(components[2]["closed"] is False and components[2]["uniform_slope_cap"] is None, "rank-two route cut drift")
    require(
        components[0]["provenance"] == "IMPORTED_FROM_INTEGRATED_PR_660_AND_APPLIED_HERE"
        and components[1]["provenance"] == "IMPORTED_FROM_INTEGRATED_PR_670_AND_APPLIED_HERE"
        and components[2]["provenance"] == "NEW_ROUTE_CUT_IN_THIS_PACKET",
        "rank-component provenance drift",
    )
    low_excess = components[2]["existing_owner_subroute"]
    require(
        low_excess["owner"]
        == "AGREEMENT_WEIGHTED_TRANSVERSE_SECANT_FIXED_LOW_EXCESS_U",
        "low-excess owner drift",
    )
    require(
        low_excess["provenance"]
        == "IMPORTED_FROM_INTEGRATED_PR_670_AND_APPLIED_CONDITIONALLY",
        "low-excess provenance drift",
    )
    require(low_excess["uniform_slope_cap"] == LOW_EXCESS_CAP == 84_416_263, "low-excess cap drift")
    require(low_excess["fits_current_remainder"] is True, "low-excess cap no longer fits")
    require(
        low_excess["exhaustive_low_excess_shadow_cover_proved"] is False,
        "low-excess cover invented",
    )

    control = artifact["full_field_control"]
    for key in (
        "gamma_in_parameter_field",
        "projective_field_full",
        "fixed_support_equation_holds",
        "support_noncontained",
        "received_pair_realizable",
    ):
        require(control[key] is True, f"full-field control lost property: {key}")
    require(control["gamma_in_base_field"] is False, "control gamma became base-valued")
    require(control["global_syndrome_rank"] == 2, "control syndrome rank drift")
    require(
        control["survives_deployed_kb_branches_1_to_5_proved"] is False,
        "toy control promoted to deployed survivor",
    )

    ledger = artifact["ledger"]
    require(ledger["rank_zero_component_closed"] is True, "rank-zero ledger flag drift")
    require(ledger["rank_one_component_closed"] is True and ledger["rank_one_uniform_cap"] == 1, "rank-one ledger flag drift")
    require(ledger["pair_rank_cases_combine_by"] == "MAXIMUM_NOT_SUM", "rank cases summed across lines")
    require(ledger["proper_field_c5_charge"] is None, "proper-field C5 charged")
    require(ledger["field_full_rank_two_charge"] is None, "rank-two residual charged")
    require(ledger["U_2"] is None and ledger["U_Q"] is None and ledger["U_A"] is None, "null ledger term changed")
    require(ledger["ledger_consequence"] is False and ledger["row_complete"] is False, "row closure overclaim")

    audit = artifact["audit_sections"]
    require(audit["layer_cake_dyadic_summability"] == "NOT_APPLICABLE", "layer-cake drift")
    require(audit["moment_markov_chebyshev"] == "NOT_APPLICABLE", "moment drift")
    require(audit["edge_cases"] == EDGE_CASES, "edge-case list drift")
    require(audit["remaining_risks"] == REMAINING_RISKS, "risk list drift")
    require(artifact["nonclaims"] == NONCLAIMS, "nonclaims drift")
    require(artifact["payload_sha256"] == payload_hash(artifact), "payload hash drift")

    if exact_rebuild:
        require(
            canonical_bytes(artifact) == canonical_bytes(build_certificate()),
            "deterministic certificate rebuild drift",
        )


def expect_reject(name: str, artifact: dict[str, Any]) -> None:
    try:
        validate(artifact)
    except (VerificationError, KeyError, TypeError, ValueError):
        return
    raise VerificationError(f"tamper accepted: {name}")


def run_tamper_selftest(artifact: dict[str, Any]) -> int:
    cases: list[tuple[str, dict[str, Any]]] = []

    def mutate(name: str, path: tuple[Any, ...], value: Any) -> None:
        candidate = copy.deepcopy(artifact)
        target: Any = candidate
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        candidate["payload_sha256"] = payload_hash(candidate)
        cases.append((name, candidate))

    mutate("c5-aliased-to-kb5", ("policy_compatibility", "kb_branch_5_equals_projective_c5"), True)
    mutate("current-post5-called-full-field", ("policy_compatibility", "current_fp2_post5_implies_full_projective_field"), True)
    mutate("literal-adapter-invented", ("policy_compatibility", "literal_adapter_proved"), True)
    mutate("mask-adapter-falsely-complete", ("mask_inventory", "complete_executable_adapter"), True)
    mutate("branch2-called-exact", ("mask_inventory", "records", 1, "machine_status"), "MACHINE_EXACT")
    mutate("branch3-projector-invented", ("mask_inventory", "records", 2, "actual_slope_projector_complete"), True)
    mutate("branch4-called-complete", ("mask_inventory", "records", 3, "actual_slope_projector_complete"), True)
    mutate("branch5-called-paid", ("mask_inventory", "records", 4, "paid_owner"), True)
    mutate("omit-degree3-subfield", ("projective_c5_refinement", "proper_intermediate_degrees"), [1, 2])
    mutate("local-quotient-used-for-field", ("projective_c5_refinement", "support_quotient_substitution_allowed"), True)
    mutate("proper-field-c5-called-paid", ("projective_c5_refinement", "proper_field_cell_paid_in_this_packet"), True)
    mutate("zerozero-retained", ("incidence_classification", "cases", 0, "retained_noncontained"), True)
    mutate("zero-second-root", ("incidence_classification", "cases", 1, "root_count"), 1)
    mutate("nonproportional-root", ("incidence_classification", "cases", 2, "root_count"), 1)
    mutate("unique-root-lost", ("incidence_classification", "cases", 3, "root_count"), 0)
    mutate("base-root-retained", ("incidence_classification", "unique_root_subroutes", 0), "gamma_in_F_p_RETAIN_IN_R2")
    mutate("support-cap-unioned", ("incidence_classification", "fixed_support_cap_extends_to_support_union"), True)
    mutate("import-provenance-erased", ("provenance", "integrated_imports", 0, "source_pr"), 0)
    mutate("new-provenance-overclaimed", ("provenance", "new_in_this_packet", 0), "CANONICAL_C5")
    mutate("pivot-dimension-drift", ("incidence_classification", "basis_relative_pivot_atlas", "coordinate_dimension"), 202_415)
    mutate("pivot-basis-model-erased", ("incidence_classification", "basis_relative_pivot_atlas", "coordinate_model"), "UNDECLARED")
    mutate("pivot-basis-adapter-invented", ("incidence_classification", "basis_relative_pivot_atlas", "deterministic_support_to_basis_adapter_deployed"), True)
    mutate("pivot-earlier-zero-omitted", ("incidence_classification", "basis_relative_pivot_atlas", "earlier_zero_equations"), "OMITTED")
    mutate("pivot-nonbase-omitted", ("incidence_classification", "basis_relative_pivot_atlas", "nonbase_inequation"), "OMITTED")
    mutate("pivot-called-kb-mask-atlas", ("incidence_classification", "basis_relative_pivot_atlas", "is_kb_branch_1_to_5_mask_atlas"), True)
    mutate("census-unique-root-drift", ("incidence_classification", "exact_control_q4_m2", "unique_root_pairs"), 59)
    mutate("census-partition-false", ("incidence_classification", "control_partition_sums_to_total"), False)
    mutate("rank0-nonempty", ("global_rank_components", 0, "uniform_slope_cap"), 1)
    mutate("rank1-cap-two", ("global_rank_components", 1, "uniform_slope_cap"), 2)
    mutate("rank2-falsely-closed", ("global_rank_components", 2, "closed"), True)
    mutate("low-excess-cap-drift", ("global_rank_components", 2, "existing_owner_subroute", "uniform_slope_cap"), LOW_EXCESS_CAP - 1)
    mutate("low-excess-cover-invented", ("global_rank_components", 2, "existing_owner_subroute", "exhaustive_low_excess_shadow_cover_proved"), True)
    mutate("control-not-full-field", ("full_field_control", "projective_field_full"), False)
    mutate("control-base-gamma", ("full_field_control", "gamma_in_base_field"), True)
    mutate("control-promoted-to-kb-survivor", ("full_field_control", "survives_deployed_kb_branches_1_to_5_proved"), True)
    mutate("rank-cases-summed", ("ledger", "pair_rank_cases_combine_by"), "SUM")
    mutate("proper-field-charge-zero", ("ledger", "proper_field_c5_charge"), "0")
    mutate("rank2-charge-zero", ("ledger", "field_full_rank_two_charge"), "0")
    mutate("U2-null-to-zero", ("ledger", "U_2"), "0")
    mutate("UQ-null-to-zero", ("ledger", "U_Q"), "0")
    mutate("UA-null-to-zero", ("ledger", "U_A"), "0")
    mutate("row-falsely-complete", ("ledger", "row_complete"), True)
    mutate("source-hash-drift", ("source_bindings", 0, "sha256"), "0" * 64)
    mutate("erase-edge-cases", ("audit_sections", "edge_cases"), ["none"])
    mutate("erase-risks", ("audit_sections", "remaining_risks"), ["none"])
    mutate("erase-nonclaims", ("nonclaims",), ["none"])

    unknown = copy.deepcopy(artifact)
    unknown["unknown_field"] = True
    unknown["payload_sha256"] = payload_hash(unknown)
    cases.append(("unknown-key", unknown))

    bad_payload = copy.deepcopy(artifact)
    bad_payload["payload_sha256"] = "0" * 64
    cases.append(("payload-hash", bad_payload))

    bool_as_int = copy.deepcopy(artifact)
    bool_as_int["row"]["agreement_A"] = True
    bool_as_int["payload_sha256"] = payload_hash(bool_as_int)
    cases.append(("bool-as-integer", bool_as_int))

    for name, candidate in cases:
        expect_reject(name, candidate)

    parser_cases = 0
    for text, name in [
        ('{"schema":1,"schema":1}', "duplicate-key"),
        ('{"x":NaN}', "nonstandard-constant"),
    ]:
        try:
            parse_json(text, name)
        except VerificationError:
            parser_cases += 1
        else:
            raise VerificationError(f"tamper accepted: {name}")
    return len(cases) + parser_cases


def emit() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    artifact = build_certificate()
    CERT_PATH.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {CERT_PATH.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.emit:
        emit()
        return 0

    artifact = load_json(CERT_PATH)
    validate(artifact)
    if args.tamper_selftest:
        rejected = run_tamper_selftest(artifact)
        print(
            "M1_FP2_POST_C5_MASK_INCIDENCE_V1_TAMPER_PASS "
            f"rejected={rejected}/{rejected}"
        )
    else:
        print("M1_FP2_POST_C5_MASK_INCIDENCE_V1_VERIFY_PASS")
        print(
            "frozen mask inventory: incomplete at branch 2; "
            "integrated #660 C5 applied as branch-6 refinement"
        )
        print(
            "imported closures applied: #660 rank 0 -> empty; "
            "#670 post-C5 full-field rank 1 -> at most one slope"
        )
        print(
            "route cut: post-C5 full-field rank 2 support union unpaid; "
            "U_2/U_Q/U_A remain null"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
