#!/usr/bin/env python3
"""Verify the KoalaBear rank-nine sparse chart-boundary route cut.

The packet specializes the proved fixed-residual-excess Padé--Hankel argument
to the sparse terminal exported by the rank-nine syndrome-rank packet.  It
certifies two disjoint conditional subcell caps:

* at most ``j`` tangent bad slopes; and
* at most ``R-j`` non-tangent bad slopes on the boundary of one fixed chosen
  maximal-minor chart.

The regular split-locator chart remains open.  The two caps are not added to
the shared ledger, a chosen-minor root is not called global rank drop, and all
semantic prerequisites are fail closed.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-rank9-sparse-chart-boundary-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_RANK9_SPARSE_CHART_BOUNDARY_ROUTE_CUT"
STATUS = (
    "PROVED_LOCAL_SPARSE_TANGENT_AND_CHART_BOUNDARY_CONDITIONAL_CAP_"
    "REGULAR_ROUTE_OPEN_NO_LEDGER_MOVEMENT"
)

PREDECESSOR_PAID = "NON_CA_RANK9_SYNDROME_REDUCTION_PAID"
PREDECESSOR_SPARSE = "CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA"
TANGENT_TERMINAL = "SPARSE_TANGENT_RANK9_CONDITIONAL_CAP"
BOUNDARY_TERMINAL = "SPARSE_CHART_BOUNDARY_RANK9_CONDITIONAL_CAP"
REGULAR_TERMINAL = "REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE"
REJECTED = "REJECT_UNCERTIFIED_INPUT"

PROVED_TANGENT = "PROVED_TANGENT"
PROVED_NON_TANGENT = "PROVED_NON_TANGENT"
PROVED_MINOR_ROOT = "PROVED_MINOR_ROOT"
PROVED_MINOR_NONROOT = "PROVED_MINOR_NONROOT"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-rank9-sparse-chart-boundary-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_rank9_sparse_chart_boundary_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-sparse-chart-boundary-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.sage"
)

PREDECESSOR_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md"
)
PREDECESSOR_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-syndrome-rank-reduction-v1/"
    "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.json"
)
PREDECESSOR_PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py"
)
PREDECESSOR_SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.sage"
)
FIXED_EXCESS_REL = Path(
    "experimental/notes/thresholds/"
    "cap25_v12_fixed_residual_excess_audit.md"
)
SPARSE_HANKEL_REL = Path(
    "experimental/notes/thresholds/"
    "cap25_v12_sparse_sigma_first_layer_audit.md"
)
SPARSIFICATION_REL = Path("experimental/rs_mca_thresholds.tex")
FIRST_MATCH_LEDGER_REL = Path(
    "experimental/notes/thresholds/"
    "kb_mca_1116048_first_match_ledger_v1.md"
)
SUPPORT_THRESHOLD_REL = Path("tex/towards-prize.tex")

STACK_BASE_COMMIT = "beb213b6ad7c42d02be7eb09a22c0e1b51d9e18e"
PREDECESSOR_INTEGRATION_COMMIT = "48115af63b7178a543db35a631e252eba7e35ba3"
PREDECESSOR_SCHEMA = "rs-mca-m1-kb-branch3-rank9-syndrome-rank-reduction-v1"

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
MATRIX_ROWS = R - J
MATRIX_COLUMNS = J + 1
RESIDUAL_EXCESS_H = 2 * J - R - 1
REGULAR_KERNEL_DIMENSION = MATRIX_COLUMNS - MATRIX_ROWS
NON_TANGENT_SUPPORT_FLOOR = MATRIX_ROWS + 1
TANGENT_CAP = J
CHART_BOUNDARY_CAP = MATRIX_ROWS
TWO_CELL_CONDITIONAL_CAP = TANGENT_CAP + CHART_BOUNDARY_CAP

RANK_S = 9
WITNESS_COLUMN_RANK_T = 10

DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "row",
    "predecessor_contract",
    "sparse_translation_contract",
    "hankel_specialization",
    "minor_selection_contract",
    "first_match_classifier",
    "quantifier_scope",
    "exact_controls",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not prove a new generic sparse-sigma theorem.",
    "This packet does not call a chosen-minor root a global rank drop.",
    "This packet does not drop the same-support noncontainment gate H_2*ell_T!=0.",
    "This packet does not call the regular residual final primitive.",
    "This packet does not prove later first-match owner masks exhaustive.",
    "This packet does not move U_paid or B_remaining.",
    "This packet does not close rank nine, branch 3, or the KoalaBear row.",
    "This packet does not attack intrinsic rank at least ten.",
    "The Sage control is not a deployed-field census or a proof of the symbolic lemma.",
    "This packet does not authorize Lean or stable-paper promotion.",
]


class VerificationError(RuntimeError):
    """A source, arithmetic, schema, or semantic check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise VerificationError(f"nonstandard JSON constant: {value}")


def parse_json(text: str, label: str) -> dict[str, Any]:
    value = json.loads(
        text,
        object_pairs_hook=reject_duplicate_keys,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"top-level JSON is not an object: {label}")
    return value


def load_json(path: Path) -> dict[str, Any]:
    return parse_json(path.read_text(encoding="utf-8"), str(path))


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def canonical_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def payload_hash(value: dict[str, Any]) -> str:
    clean = copy.deepcopy(value)
    clean.pop("payload_sha256", None)
    return canonical_hash(clean)


def file_hash(relative: Path) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing bound source: {relative}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(binding_id: str, relative: Path, role: str) -> dict[str, str]:
    return {
        "binding_id": binding_id,
        "path": relative.as_posix(),
        "sha256": file_hash(relative),
        "role": role,
    }


def expected_source_bindings() -> list[dict[str, str]]:
    return [
        binding("packet-note", NOTE_REL, "load-bearing row specialization"),
        binding("packet-readme", README_REL, "replay and scope contract"),
        binding("packet-verifier", PYTHON_REL, "exact fail-closed verifier"),
        binding("sage-control", SAGE_REL, "independent finite-field control"),
        binding(
            "predecessor-note",
            PREDECESSOR_NOTE_REL,
            "rank-nine column-far versus sparse route",
        ),
        binding(
            "predecessor-certificate",
            PREDECESSOR_CERT_REL,
            "frozen rank-nine route state",
        ),
        binding(
            "predecessor-verifier",
            PREDECESSOR_PYTHON_REL,
            "predecessor exact replay",
        ),
        binding(
            "predecessor-sage",
            PREDECESSOR_SAGE_REL,
            "predecessor finite-field guardrails",
        ),
        binding(
            "fixed-residual-excess-proof",
            FIXED_EXCESS_REL,
            "generic tangent full-rank and chosen-minor proof",
        ),
        binding(
            "exact-hankel-formulation",
            SPARSE_HANKEL_REL,
            "same-support split-locator equivalence",
        ),
        binding(
            "challenge-sparsification",
            SPARSIFICATION_REL,
            "SP3 translation preserving the bad-slope set",
        ),
        binding(
            "canonical-first-match-order",
            FIRST_MATCH_LEDGER_REL,
            "global owner-order and sparse branch guardrail",
        ),
        binding(
            "support-threshold-theorem",
            SUPPORT_THRESHOLD_REL,
            "direct low-support exclusion for non-tangent bad slopes",
        ),
    ]


def _contains_all(text: str, anchors: list[str], label: str) -> None:
    for anchor in anchors:
        require(anchor in text, f"{label} semantic anchor missing: {anchor}")


def validate_source_contracts(
    *,
    predecessor_override: dict[str, Any] | None = None,
    sparsification_override: str | None = None,
    fixed_excess_override: str | None = None,
    sparse_hankel_override: str | None = None,
    first_match_override: str | None = None,
    support_threshold_override: str | None = None,
    note_override: str | None = None,
) -> None:
    """Validate semantic anchors before blessing whole-file hashes."""

    predecessor = (
        predecessor_override
        if predecessor_override is not None
        else load_json(ROOT / PREDECESSOR_CERT_REL)
    )
    require(
        predecessor.get("schema") == PREDECESSOR_SCHEMA,
        "rank-nine predecessor schema drift",
    )
    require(
        predecessor.get("payload_sha256") == payload_hash(predecessor),
        "rank-nine predecessor payload drift",
    )
    require(
        predecessor.get("artifact_kind")
        == "M1_KB_BRANCH3_RANK9_SYNDROME_RANK_REDUCTION_ROUTE_CUT",
        "rank-nine predecessor artifact drift",
    )
    row = predecessor.get("row", {})
    require(
        (
            row.get("n"),
            row.get("k"),
            row.get("agreement_A"),
            row.get("redundancy_R"),
            row.get("error_cap_j"),
            row.get("zero_mask_surplus_Delta0"),
        )
        == (N, K, A, R, J, MATRIX_ROWS),
        "rank-nine predecessor row drift",
    )
    classifier = predecessor.get("classifier_contract", {})
    require(
        classifier.get("terminals")
        == [PREDECESSOR_PAID, PREDECESSOR_SPARSE],
        "rank-nine predecessor terminal order drift",
    )
    require(
        classifier.get("terminal_count") == 2,
        "rank-nine predecessor terminal count drift",
    )
    require(
        classifier.get("partition_object")
        == "ORIGINAL_RECEIVED_PAIR_COLUMN_FAR_AT_AGREEMENT_A",
        "rank-nine predecessor partition drift",
    )
    require(
        classifier.get("CA_terminal_is_route_not_payment") is True,
        "rank-nine predecessor sparse terminal became payment",
    )
    reduction = predecessor.get("deterministic_rank_reduction", {})
    require(
        reduction.get("correlated_agreement_terminal") == PREDECESSOR_SPARSE
        and reduction.get("non_correlated_agreement_terminal")
        == PREDECESSOR_PAID
        and reduction.get("sparse_route_paid_here") is False,
        "rank-nine predecessor marked sparse route paid",
    )
    charges = predecessor.get("charges", {})
    require(charges.get("packet_banked_charge") == "0", "predecessor charge moved")
    require(
        charges.get("correlated_agreement_branch_paid") is False,
        "predecessor sparse branch charge drift",
    )
    ledger = predecessor.get("ledger", {})
    require(
        ledger.get("U_paid_before") == ledger.get("U_paid_after") == str(U_PAID),
        "predecessor U_paid drift",
    )
    require(
        ledger.get("B_remaining_before")
        == ledger.get("B_remaining_after")
        == str(B_REMAINING),
        "predecessor remaining-budget drift",
    )
    require(
        ledger.get("rank9_status") == "YELLOW_OPEN_SPARSE_SIGMA_ONLY",
        "predecessor rank-nine status drift",
    )
    require(
        ledger.get("next_route") == "SPARSE_SIGMA_FIRST_MATCH_AUDIT",
        "predecessor next-route drift",
    )

    sparsification = (
        sparsification_override
        if sparsification_override is not None
        else (ROOT / SPARSIFICATION_REL).read_text(encoding="utf-8")
    )
    _contains_all(
        sparsification,
        [
            r"\tag{SP3}\label{eq:challenge-sparsification}",
            "translation sends",
            "is a bijection between witness supports",
            "It also preserves simultaneous",
        ],
        "SP3",
    )

    fixed_excess = (
        fixed_excess_override
        if fixed_excess_override is not None
        else (ROOT / FIXED_EXCESS_REL).read_text(encoding="utf-8")
    )
    _contains_all(
        fixed_excess,
        [
            "rank M(gamma) = m-r.",
            "dim ker M(gamma) = (r+1) - (m-r) = h+2.",
            "non-tangent bad slope `gamma_0`",
            "deg Delta <= m-r.",
            "slopes with `Delta(gamma)=0` contribute at most `m-r`.",
            "H_2 ell_T != 0",
        ],
        "fixed-residual-excess proof",
    )

    sparse_hankel = (
        sparse_hankel_override
        if sparse_hankel_override is not None
        else (ROOT / SPARSE_HANKEL_REL).read_text(encoding="utf-8")
    )
    _contains_all(
        sparse_hankel,
        [
            "(H_1 + gamma H_2) ell_T = 0,",
            "H_2 ell_T != 0.",
            "same-support noncontainment test",
            "D-split squarefree",
        ],
        "exact Hankel formulation",
    )

    first_match = (
        first_match_override
        if first_match_override is not None
        else (ROOT / FIRST_MATCH_LEDGER_REL).read_text(encoding="utf-8")
    )
    _contains_all(
        first_match,
        [
            "## First-match branches",
            "3. tangent / common-line / residue-line",
            "8. sparse sigma or sparse-support",
            "10. primitive Q-fin residual",
        ],
        "first-match ledger",
    )

    support_threshold = (
        support_threshold_override
        if support_threshold_override is not None
        else (ROOT / SUPPORT_THRESHOLD_REL).read_text(encoding="utf-8")
    )
    _contains_all(
        support_threshold,
        [
            r"\begin{theorem}[support threshold]\label{thm:sparse-threshold}",
            r"If $e\le w_{\min}-1-r$",
            r"requires $e\ge w_{\min}-r$",
        ],
        "support-threshold theorem",
    )

    note = (
        note_override
        if note_override is not None
        else (ROOT / NOTE_REL).read_text(encoding="utf-8")
    )
    _contains_all(
        note,
        [
            TANGENT_TERMINAL,
            BOUNDARY_TERMINAL,
            REGULAR_TERMINAL,
            r"H_2\ell_T\ne0",
            r"\widetilde c_\eta=c_\eta-c_0-\eta c_1",
            "partitions that sparse bad set locally, before intersection with",
            "not be called a global rank-drop owner",
            "does not prove the aggregation",
        ],
        "packet note",
    )


def expected_row() -> dict[str, Any]:
    return {
        "row_id": "koalabear-mca-A1116048",
        "p": P,
        "ambient_extension_degree": EXTENSION_DEGREE,
        "q_line": str(Q_LINE),
        "n": N,
        "k": K,
        "agreement_A": A,
        "redundancy_R": R,
        "error_cap_j": J,
        "R_minus_j": MATRIX_ROWS,
        "minimum_distance_d": R + 1,
        "residual_excess_h": RESIDUAL_EXCESS_H,
        "matrix_rows": MATRIX_ROWS,
        "matrix_columns": MATRIX_COLUMNS,
        "regular_kernel_dimension": REGULAR_KERNEL_DIMENSION,
        "non_tangent_support_floor": NON_TANGENT_SUPPORT_FLOOR,
        "B_star": str(B_STAR),
        "U_paid": str(U_PAID),
        "B_remaining": str(B_REMAINING),
    }


def expected_predecessor_contract() -> dict[str, Any]:
    predecessor = load_json(ROOT / PREDECESSOR_CERT_REL)
    return {
        "stack_base_commit": STACK_BASE_COMMIT,
        "predecessor_integration_commit": PREDECESSOR_INTEGRATION_COMMIT,
        "immediate_schema": PREDECESSOR_SCHEMA,
        "immediate_payload_sha256": predecessor["payload_sha256"],
        "entry_terminal": PREDECESSOR_SPARSE,
        "column_far_terminal": PREDECESSOR_PAID,
        "partition_object": "ORIGINAL_RECEIVED_PAIR_COLUMN_FAR_AT_AGREEMENT_A",
        "entry_terminal_is_route_not_payment": True,
        "same_original_pair_required": True,
        "same_selector_and_restricted_map_required": True,
        "same_retained_finite_slope_family_required": True,
        "intrinsic_affine_rank_s": RANK_S,
        "witness_column_rank_t": WITNESS_COLUMN_RANK_T,
        "rank_and_locator_families_linked_only_as_downstream_context": True,
        "packet_banked_charge": "0",
        "ledger_unchanged": True,
    }


def expected_sparse_translation_contract() -> dict[str, Any]:
    return {
        "theorem_label": "SP3_CHALLENGE_RESTRICTED_EXACT_SPARSIFICATION",
        "common_support_size_at_least_A": True,
        "epsilon_1_definition": "epsilon_1=f-c_0",
        "epsilon_2_definition": "epsilon_2=g-c_1",
        "actual_support_union": "E=supp(epsilon_1) UNION supp(epsilon_2)",
        "zero_padded_declared_support_forbidden": True,
        "support_union_size_at_most_j": True,
        "exact_bad_slope_set_preserved": True,
        "exact_witness_supports_preserved": True,
        "same_support_noncontainment_preserved": True,
        "translated_selected_codeword": "c_tilde_eta=c_eta-c_0-eta*c_1",
        "selected_error_identity": (
            "epsilon_1+eta*epsilon_2-c_tilde_eta=f+eta*g-c_eta=e_eta"
        ),
        "selected_error_supports_and_ranks_unchanged": True,
        "finite_challenge_family_only": True,
        "field_typing": "gamma lies in the same ambient scalar field as the Hankel pencil",
    }


def expected_hankel_specialization() -> dict[str, Any]:
    return {
        "RS_evaluation_points_distinct_and_finite": True,
        "GRS_column_multipliers_and_syndrome_weights_nonzero": True,
        "redundancy_m": R,
        "closed_ball_radius_r": J,
        "pencil": "M(gamma)=H_1+gamma*H_2",
        "matrix_rows": MATRIX_ROWS,
        "matrix_columns": MATRIX_COLUMNS,
        "residual_excess_h": RESIDUAL_EXCESS_H,
        "regular_kernel_dimension": REGULAR_KERNEL_DIMENSION,
        "locator_equation": "M(gamma)*ell_T=0",
        "same_support_noncontainment": "H_2*ell_T!=0",
        "locator_size": J,
        "locator_monic": True,
        "locator_roots_distinct": True,
        "locator_roots_subset_D": True,
        "locator_is_D_split_squarefree": True,
        "tangent_definition": (
            "EXISTS x IN E: epsilon_1(x)+gamma*epsilon_2(x)=0"
        ),
        "finite_tangent_slopes_deduplicated": True,
        "tangent_cap": TANGENT_CAP,
        "low_support_branch_e_at_most_R_minus_j_has_no_non_tangent_bad_slope": True,
        "non_tangent_support_floor": NON_TANGENT_SUPPORT_FLOOR,
        "non_tangent_rank_formula": "rank M(gamma)=min(|E|,R-j)",
        "non_tangent_bad_full_row_rank": MATRIX_ROWS,
    }


def expected_minor_selection_contract() -> dict[str, Any]:
    return {
        "empty_non_tangent_case": "TANGENT_ONLY_NO_MINOR_REQUIRED",
        "selection_protocol": (
            "CHOOSE_ONE_NON_TANGENT_BAD_gamma_0_THEN_ONE_MAXIMAL_MINOR_"
            "NONZERO_AT_gamma_0"
        ),
        "anchor_is_actual_non_tangent_bad_slope": True,
        "one_minor_fixed_for_entire_sparse_pair_and_retained_family": True,
        "slope_dependent_minor_forbidden": True,
        "minor_size": MATRIX_ROWS,
        "determinant_symbol": "Delta(gamma)",
        "Delta_at_anchor_nonzero": True,
        "determinant_nonzero_polynomial": True,
        "univariate_over_same_slope_field": True,
        "degree_cap": CHART_BOUNDARY_CAP,
        "distinct_finite_root_cap": CHART_BOUNDARY_CAP,
        "minor_root_is_chart_boundary_not_global_rank_drop": True,
        "full_matrix_rank_at_non_tangent_bad_minor_roots": MATRIX_ROWS,
    }


def expected_first_match_classifier() -> dict[str, Any]:
    return {
        "ordered_terminals": [
            PREDECESSOR_PAID,
            TANGENT_TERMINAL,
            BOUNDARY_TERMINAL,
            REGULAR_TERMINAL,
        ],
        "sparse_subcell_order": [
            TANGENT_TERMINAL,
            BOUNDARY_TERMINAL,
            REGULAR_TERMINAL,
        ],
        "set_partition": {
            "tangent": "Z_tan=Z_sparse INTERSECT Tangent",
            "boundary": "Z_boundary=(Z_sparse SETMINUS Z_tan) INTERSECT {Delta=0}",
            "regular": "Z_regular=Z_sparse SETMINUS (Z_tan UNION Z_boundary)",
        },
        "tangent_first": True,
        "boundary_explicitly_excludes_tangent": True,
        "duplicate_assignment_forbidden": True,
        "global_owner_overlap_must_be_subtracted_before_ledger_aggregation": True,
        "local_partition_precedes_global_owner_intersection": True,
        "unknown_tangent_state_rejected": REJECTED,
        "unknown_minor_root_state_rejected": REJECTED,
        "minor_without_non_tangent_full_rank_rejected": REJECTED,
        "minor_without_pair_global_anchor_rejected": REJECTED,
        "missing_noncontainment_rejected": REJECTED,
        "fail_closed_defaults": REJECTED,
        "regular_terminal_is_route_not_payment": True,
        "later_owner_masks_pending": True,
        "regular_residual_final_primitive": False,
    }


def expected_quantifier_scope() -> dict[str, Any]:
    return {
        "object": "ONE_FIXED_COMPLETE_AFFINE_RANK9_SELECTOR_AND_ONE_TRANSLATED_SPARSE_PAIR",
        "tangent_cap_scope": "DISTINCT_FINITE_SLOPES_FOR_ONE_SPARSE_PAIR",
        "minor_cap_scope": "ROOTS_OF_ONE_FIXED_NONZERO_MINOR_FOR_ONE_SPARSE_PAIR",
        "minor_may_vary_between_different_sparse_pairs": True,
        "minor_may_not_vary_between_slopes_of_one_pair": True,
        "conditional_union_cap_not_global_profile_sum": True,
        "global_first_match_aggregation_proved": False,
        "regular_residual": [
            "Delta(gamma)!=0",
            "M(gamma)*ell_T=0",
            "H_2*ell_T!=0",
            f"|T|={J}",
            "L_T squarefree and D-split",
        ],
    }


def expected_exact_controls() -> dict[str, Any]:
    return {
        "constant_identities": {
            "R_equals_n_minus_k": R == N - K,
            "j_equals_n_minus_A": J == N - A,
            "R_minus_j_equals_A_minus_k": MATRIX_ROWS == A - K,
            "matrix_columns_equals_j_plus_1": MATRIX_COLUMNS == J + 1,
            "h_equals_2j_minus_R_minus_1": RESIDUAL_EXCESS_H == 2 * J - R - 1,
            "kernel_dimension_equals_h_plus_2": (
                REGULAR_KERNEL_DIMENSION == RESIDUAL_EXCESS_H + 2
            ),
            "support_floor_equals_R_minus_j_plus_1": (
                NON_TANGENT_SUPPORT_FLOOR == MATRIX_ROWS + 1
            ),
            "two_cell_cap_equals_R": TWO_CELL_CONDITIONAL_CAP == R,
            "B_star_equals_U_paid_plus_B_remaining": (
                B_STAR == U_PAID + B_REMAINING
            ),
        },
        "tangent_cap_exact": TANGENT_CAP,
        "chosen_minor_degree_cap_exact": CHART_BOUNDARY_CAP,
        "chosen_minor_root_cap_exact": CHART_BOUNDARY_CAP,
        "two_cell_conditional_union_cap_exact": TWO_CELL_CONDITIONAL_CAP,
        "deployed_field_census_performed": False,
        "numerical_scale": "EXACT_KOALABEAR_BIG_INTEGERS_PLUS_SAGE_TOY_CONTROL",
        "fixed_h_bound_called_uniform_in_growing_h": False,
    }


def expected_charges() -> dict[str, Any]:
    return {
        "tangent_conditional_cap": TANGENT_CAP,
        "chosen_minor_root_conditional_cap": CHART_BOUNDARY_CAP,
        "two_cell_conditional_union_cap": TWO_CELL_CONDITIONAL_CAP,
        "caps_are_disjoint_by_local_first_match": True,
        "column_far_alternative_cap_added": False,
        "global_first_match_aggregation_proved": False,
        "packet_banked_charge": "0",
        "reason_no_ledger_movement": (
            "REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE_REMAINS_AND_GLOBAL_"
            "AGGREGATION_IS_UNPROVED"
        ),
    }


def expected_ledger() -> dict[str, Any]:
    return {
        "U_paid_before": str(U_PAID),
        "U_paid_after": str(U_PAID),
        "B_remaining_before": str(B_REMAINING),
        "B_remaining_after": str(B_REMAINING),
        "rank9_status": "YELLOW_OPEN_REGULAR_SPLIT_LOCATOR",
        "branch3_status": "YELLOW_OPEN",
        "koalabear_row_status": "YELLOW_OPEN",
        "next_route": "REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_FIRST_MATCH_OWNER_AUDIT",
    }


def expected_audit_sections() -> dict[str, Any]:
    return {
        "statement": "KoalaBear rank-nine sparse tangent and chosen-minor chart split",
        "dependency_status": (
            "PROVED_LOCAL_SPECIALIZATION_PLUS_PROVED_PREDECESSOR_"
            "REGULAR_SPLIT_LOCATOR_UNPAID"
        ),
        "parameter_dependence": "EXACT_KOALABEAR_FINITE_ROW; LOCAL_LEMMA_FIELD_UNIFORM",
        "layer_cake_dyadic_summability": "NOT_APPLICABLE",
        "moment_markov_chebyshev": "NOT_APPLICABLE",
        "edge_cases": (
            "EMPTY_NON_TANGENT_SET_ACTUAL_SUPPORT_FIXED_MINOR_FIELD_TYPING_"
            "AND_NONCONTAINMENT_ARE_LOAD_BEARING"
        ),
        "numerical_evidence": (
            "EXACT_INTEGER_CERTIFICATE_AND_TOY_SAGE_CONTROL_NOT_DEPLOYED_CENSUS"
        ),
        "packet_verdict": "GREEN_LOCAL_CONDITIONAL_TWO_SUBCELL_ROUTE_CUT",
        "global_verdict": "YELLOW_RANK9_BRANCH3_SPARSE_SIGMA_AND_ROW_OPEN",
    }


def expected_certificate() -> dict[str, Any]:
    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "row": expected_row(),
        "predecessor_contract": expected_predecessor_contract(),
        "sparse_translation_contract": expected_sparse_translation_contract(),
        "hankel_specialization": expected_hankel_specialization(),
        "minor_selection_contract": expected_minor_selection_contract(),
        "first_match_classifier": expected_first_match_classifier(),
        "quantifier_scope": expected_quantifier_scope(),
        "exact_controls": expected_exact_controls(),
        "charges": expected_charges(),
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
        "nonclaims": NONCLAIMS,
    }
    certificate["payload_sha256"] = payload_hash(certificate)
    return certificate


def classify(
    *,
    predecessor_certified: bool,
    column_far: bool,
    sp3_translated: bool = False,
    same_pair_selector_and_slope_family: bool = False,
    sparse_actual_support_certified: bool = False,
    bad_witness_certified: bool = False,
    noncontainment_certified: bool = False,
    tangent_state: str = "UNKNOWN",
    non_tangent_full_row_rank_certified: bool = False,
    pair_global_minor_anchor_certified: bool = False,
    minor_degree_cap_certified: bool = False,
    minor_root_state: str = "UNKNOWN",
    later_owner_masks_pending: bool = True,
) -> str:
    """Fail-closed local classifier for a certified predecessor input."""

    bool_values = [
        predecessor_certified,
        column_far,
        sp3_translated,
        same_pair_selector_and_slope_family,
        sparse_actual_support_certified,
        bad_witness_certified,
        noncontainment_certified,
        non_tangent_full_row_rank_certified,
        pair_global_minor_anchor_certified,
        minor_degree_cap_certified,
        later_owner_masks_pending,
    ]
    if any(type(value) is not bool for value in bool_values):
        return REJECTED
    if not predecessor_certified:
        return REJECTED
    if column_far:
        return PREDECESSOR_PAID

    common_sparse_gates = [
        sp3_translated,
        same_pair_selector_and_slope_family,
        sparse_actual_support_certified,
        bad_witness_certified,
        noncontainment_certified,
    ]
    if not all(common_sparse_gates):
        return REJECTED

    if tangent_state == PROVED_TANGENT:
        return TANGENT_TERMINAL
    if tangent_state != PROVED_NON_TANGENT:
        return REJECTED

    minor_gates = [
        non_tangent_full_row_rank_certified,
        pair_global_minor_anchor_certified,
        minor_degree_cap_certified,
    ]
    if not all(minor_gates):
        return REJECTED
    if minor_root_state == PROVED_MINOR_ROOT:
        return BOUNDARY_TERMINAL
    if minor_root_state == PROVED_MINOR_NONROOT and later_owner_masks_pending:
        return REGULAR_TERMINAL
    return REJECTED


def validate_classifier_contract() -> None:
    base = {
        "predecessor_certified": True,
        "column_far": False,
        "sp3_translated": True,
        "same_pair_selector_and_slope_family": True,
        "sparse_actual_support_certified": True,
        "bad_witness_certified": True,
        "noncontainment_certified": True,
        "tangent_state": PROVED_NON_TANGENT,
        "non_tangent_full_row_rank_certified": True,
        "pair_global_minor_anchor_certified": True,
        "minor_degree_cap_certified": True,
        "minor_root_state": PROVED_MINOR_NONROOT,
        "later_owner_masks_pending": True,
    }
    require(classify(**base) == REGULAR_TERMINAL, "regular classifier drift")

    tangent = dict(base)
    tangent["tangent_state"] = PROVED_TANGENT
    tangent["non_tangent_full_row_rank_certified"] = False
    tangent["pair_global_minor_anchor_certified"] = False
    tangent["minor_degree_cap_certified"] = False
    tangent["minor_root_state"] = "UNKNOWN"
    require(classify(**tangent) == TANGENT_TERMINAL, "tangent classifier drift")

    boundary = dict(base)
    boundary["minor_root_state"] = PROVED_MINOR_ROOT
    require(classify(**boundary) == BOUNDARY_TERMINAL, "boundary classifier drift")

    column_far = dict(base)
    column_far["column_far"] = True
    require(classify(**column_far) == PREDECESSOR_PAID, "column-far classifier drift")

    for key in [
        "predecessor_certified",
        "sp3_translated",
        "same_pair_selector_and_slope_family",
        "sparse_actual_support_certified",
        "bad_witness_certified",
        "noncontainment_certified",
    ]:
        bad = dict(base)
        bad[key] = False
        require(classify(**bad) == REJECTED, f"classifier accepted missing {key}")

    for key in [
        "non_tangent_full_row_rank_certified",
        "pair_global_minor_anchor_certified",
        "minor_degree_cap_certified",
    ]:
        bad = dict(base)
        bad[key] = False
        require(classify(**bad) == REJECTED, f"classifier accepted missing {key}")

    bad = dict(base)
    bad["tangent_state"] = "UNKNOWN"
    require(classify(**bad) == REJECTED, "classifier accepted unknown tangent state")
    bad = dict(base)
    bad["minor_root_state"] = "UNKNOWN"
    require(classify(**bad) == REJECTED, "classifier accepted unknown minor state")
    bad = dict(base)
    bad["later_owner_masks_pending"] = False
    require(classify(**bad) == REJECTED, "classifier called residual final")
    bad = dict(base)
    bad["predecessor_certified"] = 1  # type: ignore[assignment]
    require(classify(**bad) == REJECTED, "classifier accepted non-boolean gate")


def validate_certificate(certificate: dict[str, Any]) -> None:
    validate_source_contracts()
    require(set(certificate) == TOP_KEYS, "certificate top-level key drift")
    require(
        certificate.get("payload_sha256") == payload_hash(certificate),
        "certificate payload hash mismatch",
    )
    expected = expected_certificate()
    for key in sorted(TOP_KEYS - {"payload_sha256"}):
        require(certificate.get(key) == expected[key], f"certificate field drift: {key}")
    require(
        certificate["payload_sha256"] == expected["payload_sha256"],
        "certificate expected payload drift",
    )

    require(0 < K < A <= N, "deployed agreement ordering failed")
    require(MATRIX_ROWS == A - K > 0, "positive row dimension failed")
    require(J <= R - 1, "closed-ball radius exceeds redundancy range")
    require(REGULAR_KERNEL_DIMENSION == RESIDUAL_EXCESS_H + 2, "kernel identity failed")
    require(TWO_CELL_CONDITIONAL_CAP == R, "two-cell cap identity failed")
    charges = certificate["charges"]
    require(charges["packet_banked_charge"] == "0", "packet charge moved")
    require(
        charges["global_first_match_aggregation_proved"] is False,
        "global aggregation overclaimed",
    )
    ledger = certificate["ledger"]
    require(ledger["U_paid_before"] == ledger["U_paid_after"], "U_paid moved")
    require(
        ledger["B_remaining_before"] == ledger["B_remaining_after"],
        "B_remaining moved",
    )
    require(ledger["branch3_status"] == "YELLOW_OPEN", "branch 3 closed")
    validate_classifier_contract()


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    current: Any = value
    for key in path[:-1]:
        current = current[key]
    current[path[-1]] = replacement


def mutation_cases(baseline: dict[str, Any]) -> list[tuple[str, tuple[Any, ...], Any]]:
    return [
        ("schema", ("schema",), "rs-mca-mutated"),
        ("artifact", ("artifact_kind",), "MUTATED"),
        ("status", ("status",), "GREEN_ROW_CLOSED"),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
        ("source-path", ("source_bindings", 0, "path"), "wrong.md"),
        ("source-role", ("source_bindings", 0, "role"), "decorative"),
        ("row-n", ("row", "n"), N - 1),
        ("row-k", ("row", "k"), K - 1),
        ("row-A", ("row", "agreement_A"), A - 1),
        ("row-R", ("row", "redundancy_R"), R - 1),
        ("row-j", ("row", "error_cap_j"), J - 1),
        ("row-gap", ("row", "R_minus_j"), MATRIX_ROWS - 1),
        ("row-h", ("row", "residual_excess_h"), RESIDUAL_EXCESS_H - 1),
        ("matrix-rows", ("row", "matrix_rows"), MATRIX_ROWS - 1),
        ("matrix-columns", ("row", "matrix_columns"), MATRIX_COLUMNS - 1),
        ("kernel-dimension", ("row", "regular_kernel_dimension"), REGULAR_KERNEL_DIMENSION - 1),
        ("support-floor", ("row", "non_tangent_support_floor"), MATRIX_ROWS),
        ("stack-base", ("predecessor_contract", "stack_base_commit"), "0" * 40),
        ("predecessor-schema", ("predecessor_contract", "immediate_schema"), "wrong"),
        ("predecessor-integration", ("predecessor_contract", "predecessor_integration_commit"), "0" * 40),
        ("predecessor-payload", ("predecessor_contract", "immediate_payload_sha256"), "0" * 64),
        ("predecessor-terminal", ("predecessor_contract", "entry_terminal"), PREDECESSOR_PAID),
        ("predecessor-sparse-paid", ("predecessor_contract", "entry_terminal_is_route_not_payment"), False),
        ("same-pair", ("predecessor_contract", "same_original_pair_required"), False),
        ("same-family", ("predecessor_contract", "same_retained_finite_slope_family_required"), False),
        ("rank-s", ("predecessor_contract", "intrinsic_affine_rank_s"), 8),
        ("rank-t", ("predecessor_contract", "witness_column_rank_t"), 9),
        ("sp3", ("sparse_translation_contract", "theorem_label"), "MISSING"),
        ("support-union", ("sparse_translation_contract", "actual_support_union"), "DECLARED_E"),
        ("zero-padding", ("sparse_translation_contract", "zero_padded_declared_support_forbidden"), False),
        ("support-cap", ("sparse_translation_contract", "support_union_size_at_most_j"), False),
        ("bad-set", ("sparse_translation_contract", "exact_bad_slope_set_preserved"), False),
        ("witness-set", ("sparse_translation_contract", "exact_witness_supports_preserved"), False),
        ("selected-error", ("sparse_translation_contract", "selected_error_identity"), "UNLINKED"),
        ("selected-rank", ("sparse_translation_contract", "selected_error_supports_and_ranks_unchanged"), False),
        ("finite-slope", ("sparse_translation_contract", "finite_challenge_family_only"), False),
        ("distinct-D", ("hankel_specialization", "RS_evaluation_points_distinct_and_finite"), False),
        ("nonzero-weights", ("hankel_specialization", "GRS_column_multipliers_and_syndrome_weights_nonzero"), False),
        ("pencil", ("hankel_specialization", "pencil"), "M=H_1"),
        ("locator-size", ("hankel_specialization", "locator_size"), J - 1),
        ("locator-split", ("hankel_specialization", "locator_is_D_split_squarefree"), False),
        ("noncontainment", ("hankel_specialization", "same_support_noncontainment"), "DROPPED"),
        ("tangent-cap", ("hankel_specialization", "tangent_cap"), J + 1),
        ("low-support", ("hankel_specialization", "low_support_branch_e_at_most_R_minus_j_has_no_non_tangent_bad_slope"), False),
        ("non-tangent-rank", ("hankel_specialization", "non_tangent_bad_full_row_rank"), MATRIX_ROWS - 1),
        ("minor-anchor", ("minor_selection_contract", "anchor_is_actual_non_tangent_bad_slope"), False),
        ("minor-global", ("minor_selection_contract", "one_minor_fixed_for_entire_sparse_pair_and_retained_family"), False),
        ("slope-dependent-minor", ("minor_selection_contract", "slope_dependent_minor_forbidden"), False),
        ("minor-size", ("minor_selection_contract", "minor_size"), MATRIX_ROWS - 1),
        ("minor-nonzero", ("minor_selection_contract", "Delta_at_anchor_nonzero"), False),
        ("minor-degree", ("minor_selection_contract", "degree_cap"), MATRIX_ROWS + 1),
        ("minor-root-cap", ("minor_selection_contract", "distinct_finite_root_cap"), MATRIX_ROWS + 1),
        ("minor-called-rank-drop", ("minor_selection_contract", "minor_root_is_chart_boundary_not_global_rank_drop"), False),
        ("terminal-order", ("first_match_classifier", "sparse_subcell_order", 0), BOUNDARY_TERMINAL),
        ("overlap", ("first_match_classifier", "boundary_explicitly_excludes_tangent"), False),
        ("duplicate", ("first_match_classifier", "duplicate_assignment_forbidden"), False),
        ("local-vs-global", ("first_match_classifier", "local_partition_precedes_global_owner_intersection"), False),
        ("default", ("first_match_classifier", "fail_closed_defaults"), REGULAR_TERMINAL),
        ("unknown-tangent", ("first_match_classifier", "unknown_tangent_state_rejected"), TANGENT_TERMINAL),
        ("unknown-root", ("first_match_classifier", "unknown_minor_root_state_rejected"), BOUNDARY_TERMINAL),
        ("residual-payment", ("first_match_classifier", "regular_terminal_is_route_not_payment"), False),
        ("later-owners", ("first_match_classifier", "later_owner_masks_pending"), False),
        ("primitive", ("first_match_classifier", "regular_residual_final_primitive"), True),
        ("minor-varies-slopes", ("quantifier_scope", "minor_may_not_vary_between_slopes_of_one_pair"), False),
        ("global-sum", ("quantifier_scope", "conditional_union_cap_not_global_profile_sum"), False),
        ("global-aggregation", ("quantifier_scope", "global_first_match_aggregation_proved"), True),
        ("control-tangent", ("exact_controls", "tangent_cap_exact"), TANGENT_CAP + 1),
        ("control-minor", ("exact_controls", "chosen_minor_root_cap_exact"), CHART_BOUNDARY_CAP + 1),
        ("control-union", ("exact_controls", "two_cell_conditional_union_cap_exact"), TWO_CELL_CONDITIONAL_CAP + 1),
        ("deployed-census", ("exact_controls", "deployed_field_census_performed"), True),
        ("fixed-h-uniform", ("exact_controls", "fixed_h_bound_called_uniform_in_growing_h"), True),
        ("charge-tangent", ("charges", "tangent_conditional_cap"), TANGENT_CAP + 1),
        ("charge-minor", ("charges", "chosen_minor_root_conditional_cap"), CHART_BOUNDARY_CAP + 1),
        ("charge-union", ("charges", "two_cell_conditional_union_cap"), TWO_CELL_CONDITIONAL_CAP + 1),
        ("add-column-far", ("charges", "column_far_alternative_cap_added"), True),
        ("packet-charge", ("charges", "packet_banked_charge"), str(R)),
        ("ledger-paid", ("ledger", "U_paid_after"), str(U_PAID + R)),
        ("ledger-budget", ("ledger", "B_remaining_after"), str(B_REMAINING - R)),
        ("rank9-close", ("ledger", "rank9_status"), "GREEN_CLOSED"),
        ("branch-close", ("ledger", "branch3_status"), "GREEN_CLOSED"),
        ("row-close", ("ledger", "koalabear_row_status"), "GREEN_CLOSED"),
        ("global-verdict", ("audit_sections", "global_verdict"), "GREEN_ROW_CLOSED"),
        ("nonclaim", ("nonclaims", 1), "Chosen-minor roots are global rank drops."),
    ]


def tamper_selftest() -> None:
    baseline = load_json(CERT_PATH)
    validate_certificate(baseline)
    rejected = 0
    cases = mutation_cases(baseline)
    for name, path, replacement in cases:
        mutated = copy.deepcopy(baseline)
        set_path(mutated, path, replacement)
        mutated["payload_sha256"] = payload_hash(mutated)
        try:
            validate_certificate(mutated)
        except (VerificationError, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise VerificationError(f"mutation accepted: {name}")

    duplicate_binding = copy.deepcopy(baseline)
    duplicate_binding["source_bindings"].append(
        copy.deepcopy(duplicate_binding["source_bindings"][0])
    )
    duplicate_binding["payload_sha256"] = payload_hash(duplicate_binding)
    try:
        validate_certificate(duplicate_binding)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("duplicate source binding accepted")

    extra_key = copy.deepcopy(baseline)
    extra_key["unexpected"] = True
    extra_key["payload_sha256"] = payload_hash(extra_key)
    try:
        validate_certificate(extra_key)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("unknown top-level key accepted")

    for raw, label in [
        ('{"schema":"a","schema":"b"}', "duplicate JSON key"),
        ('{"x":NaN}', "nonstandard JSON constant"),
    ]:
        try:
            parse_json(raw, label)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"raw JSON tamper accepted: {label}")

    predecessor_bad = load_json(ROOT / PREDECESSOR_CERT_REL)
    predecessor_bad["classifier_contract"]["terminals"].reverse()
    predecessor_bad["payload_sha256"] = payload_hash(predecessor_bad)
    try:
        validate_source_contracts(predecessor_override=predecessor_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("predecessor terminal-order tamper accepted")

    predecessor_charge_bad = load_json(ROOT / PREDECESSOR_CERT_REL)
    predecessor_charge_bad["charges"]["packet_banked_charge"] = "1"
    predecessor_charge_bad["payload_sha256"] = payload_hash(predecessor_charge_bad)
    try:
        validate_source_contracts(predecessor_override=predecessor_charge_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("predecessor charge tamper accepted")

    predecessor_route_bad = load_json(ROOT / PREDECESSOR_CERT_REL)
    predecessor_route_bad["deterministic_rank_reduction"][
        "correlated_agreement_terminal"
    ] = PREDECESSOR_PAID
    predecessor_route_bad["payload_sha256"] = payload_hash(predecessor_route_bad)
    try:
        validate_source_contracts(predecessor_override=predecessor_route_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("predecessor route-terminal tamper accepted")

    predecessor_next_bad = load_json(ROOT / PREDECESSOR_CERT_REL)
    predecessor_next_bad["ledger"]["next_route"] = "OWNER"
    predecessor_next_bad["payload_sha256"] = payload_hash(predecessor_next_bad)
    try:
        validate_source_contracts(predecessor_override=predecessor_next_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("predecessor next-route tamper accepted")

    source_mutations = [
        (
            "SP3",
            SPARSIFICATION_REL,
            r"\tag{SP3}\label{eq:challenge-sparsification}",
            r"\tag{SP3-REMOVED}\label{eq:challenge-sparsification-removed}",
            "sparsification_override",
        ),
        (
            "fixed-minor",
            FIXED_EXCESS_REL,
            "deg Delta <= m-r.",
            "deg Delta <= UNBOUNDED.",
            "fixed_excess_override",
        ),
        (
            "noncontainment",
            SPARSE_HANKEL_REL,
            "H_2 ell_T != 0.",
            "H_2 ell_T MAY VANISH.",
            "sparse_hankel_override",
        ),
        (
            "first-match",
            FIRST_MATCH_LEDGER_REL,
            "8. sparse sigma or sparse-support",
            "8. REMOVED",
            "first_match_override",
        ),
        (
            "support-threshold",
            SUPPORT_THRESHOLD_REL,
            r"requires $e\ge w_{\min}-r$",
            r"requires $e\ge UNBOUNDED$",
            "support_threshold_override",
        ),
        (
            "packet-terminal",
            NOTE_REL,
            REGULAR_TERMINAL,
            "UNPAID_PRIMITIVE",
            "note_override",
        ),
    ]
    for label, path, old, new, keyword in source_mutations:
        text = (ROOT / path).read_text(encoding="utf-8")
        require(old in text, f"selftest source anchor drift: {label}")
        kwargs = {keyword: text.replace(old, new)}
        try:
            validate_source_contracts(**kwargs)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"source semantic tamper accepted: {label}")

    total = len(cases) + 14
    require(rejected == total, "tamper rejection count drift")
    print(f"PASS tamper-selftest: {rejected}/{total} mutations rejected")


def write_certificate() -> None:
    validate_source_contracts()
    validate_classifier_contract()
    certificate = expected_certificate()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(certificate, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {CERT_PATH.relative_to(ROOT)}")


def check_certificate() -> None:
    certificate = load_json(CERT_PATH)
    validate_certificate(certificate)
    print(f"PASS {SCHEMA}")
    print(
        "conditional sparse subcells: "
        f"tangent<={TANGENT_CAP}; chart-boundary<={CHART_BOUNDARY_CAP}; "
        f"disjoint union<={TWO_CELL_CONDITIONAL_CAP}=R"
    )
    print(
        "regular route: Delta!=0, M(gamma)*ell_T=0, H_2*ell_T!=0; "
        "later owner masks pending"
    )
    print("ledger: no movement; rank nine, branch 3, and KoalaBear row remain open")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write:
            write_certificate()
        elif args.check:
            check_certificate()
        else:
            tamper_selftest()
    except (VerificationError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
