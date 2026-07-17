#!/usr/bin/env python3
"""Verify the KoalaBear rank-nine syndrome-rank route cut.

The packet specializes a deterministic correlated-agreement rank-reduction
argument to the one fixed rank-minimizing selector exported by the branch-3
rank ladder.  On certified inputs it has exactly two mathematical terminals:

* ``NON_CA_RANK9_SYNDROME_REDUCTION_PAID``; or
* ``CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA``.

The second terminal is a route, not a payment.  Accordingly this packet does
not close rank nine, move the ledger, or claim that sparse sigma is bounded.
All arithmetic is exact and every semantic prerequisite is fail closed.
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

SCHEMA = "rs-mca-m1-kb-branch3-rank9-syndrome-rank-reduction-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_RANK9_SYNDROME_RANK_REDUCTION_ROUTE_CUT"
STATUS = (
    "PROVED_NON_CA_RANK9_SYNDROME_REDUCTION_PAYMENT_"
    "CA_ROUTE_TO_OPEN_SPARSE_SIGMA_NO_LEDGER_MOVEMENT"
)

PAID_TERMINAL = "NON_CA_RANK9_SYNDROME_REDUCTION_PAID"
SPARSE_TERMINAL = "CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA"
REJECTED = "REJECT_UNCERTIFIED_INPUT"

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-rank9-syndrome-rank-reduction-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-syndrome-rank-reduction-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.sage"
)

MASK_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md"
)
MASK_CERT_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-mask-deficit-v1/"
    "m1_kb_branch3_rank9_mask_deficit_v1.json"
)
MASK_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py"
)
RANK_NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_actual_core_mds_rank_ladder_v1.md"
)
RANK_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-actual-core-mds-v1/"
    "m1_kb_branch3_actual_core_mds_v1.json"
)
RANK_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py"
)
SPARSIFICATION_REL = Path("experimental/rs_mca_thresholds.tex")

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
DELTA_ZERO = R - J
MINIMUM_DISTANCE = R + 1

RANK_S = 9
SYNDROME_SPAN_H = 2
WITNESS_COLUMN_RANK_T = RANK_S + 1
REDUCTION_EXPONENT = WITNESS_COLUMN_RANK_T - SYNDROME_SPAN_H
RETAINED_FAMILY_FLOOR = 16

DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID

GAMMA_NUMERATOR = MINIMUM_DISTANCE - J
GAMMA_DENOMINATOR = MINIMUM_DISTANCE
BALL_FACTOR = J + 1
CAP_NUMERATOR = BALL_FACTOR * GAMMA_DENOMINATOR**REDUCTION_EXPONENT
CAP_DENOMINATOR = GAMMA_NUMERATOR**REDUCTION_EXPONENT
NON_CA_CAP = CAP_NUMERATOR // CAP_DENOMINATOR
NON_CA_MARGIN = B_REMAINING - NON_CA_CAP

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "literature_import",
    "row",
    "predecessor_contract",
    "syndrome_rank_adapter",
    "deterministic_rank_reduction",
    "classifier_contract",
    "exact_controls",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not use the paper's probabilistic random-code theorems.",
    "This packet does not prove that the correlated-agreement branch is paid.",
    "This packet does not prove a KoalaBear sparse-sigma bound.",
    "This packet does not identify a full low-weight syndrome line with one common support.",
    "This packet does not close the complete intrinsic rank-nine residual.",
    "This packet does not close branch 3 or the KoalaBear row.",
    "This packet does not move U_paid or B_remaining.",
    "This packet does not attack intrinsic rank at least ten.",
    "The Sage control is not a deployed-field census or a proof of the symbolic lemma.",
    "This packet does not authorize Lean or Paper-D promotion.",
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
        binding("packet-note", NOTE_REL, "load-bearing specialized proof"),
        binding("packet-readme", README_REL, "replay and scope contract"),
        binding("packet-verifier", PYTHON_REL, "exact fail-closed verifier"),
        binding("sage-control", SAGE_REL, "independent finite-field control"),
        binding("mask-note", MASK_NOTE_REL, "immediate route-cut predecessor"),
        binding("mask-certificate", MASK_CERT_REL, "frozen rank-nine row state"),
        binding("mask-verifier", MASK_VERIFIER_REL, "predecessor replay"),
        binding("rank-note", RANK_NOTE_REL, "affine-rank and transversality source"),
        binding("rank-certificate", RANK_CERT_REL, "frozen selector contract"),
        binding("rank-verifier", RANK_VERIFIER_REL, "rank-ladder replay"),
        binding(
            "exact-sparsification",
            SPARSIFICATION_REL,
            "correlated-agreement to sparse-sigma bridge",
        ),
    ]


def validate_source_contracts(
    *,
    mask_override: dict[str, Any] | None = None,
    rank_override: dict[str, Any] | None = None,
    sparsification_override: str | None = None,
    note_override: str | None = None,
) -> None:
    """Validate semantic predecessor anchors before blessing source hashes."""

    mask = mask_override if mask_override is not None else load_json(ROOT / MASK_CERT_REL)
    require(
        mask.get("schema") == "rs-mca-m1-kb-branch3-rank9-mask-deficit-v1",
        "mask-deficit predecessor schema drift",
    )
    require(
        mask.get("payload_sha256") == payload_hash(mask),
        "mask-deficit predecessor payload drift",
    )
    row = mask.get("row", {})
    require(
        (
            row.get("n"),
            row.get("k"),
            row.get("agreement_A"),
            row.get("redundancy_R"),
            row.get("error_cap_j"),
            row.get("minimum_distance"),
            row.get("B_remaining"),
        )
        == (N, K, A, R, J, MINIMUM_DISTANCE, str(B_REMAINING)),
        "mask-deficit deployed row drift",
    )
    predecessor = mask.get("predecessor_contract", {})
    require(
        predecessor.get("intrinsic_affine_rank_s") == RANK_S
        and predecessor.get("actual_core_rank_r") == RANK_S - 1
        and predecessor.get("basis_support_count") == RANK_S + 1
        and predecessor.get("one_rank_minimizing_complete_selector") is True
        and predecessor.get("basis_carrier_equals_complete_union") is True
        and predecessor.get("same_selector_and_restricted_H_V_required") is True
        and predecessor.get("selected_weight_range") == [349_526, J],
        "mask-deficit rank-nine selector contract drift",
    )
    require(
        mask.get("charges", {}).get("packet_banked_charge") == "0"
        and mask.get("ledger", {}).get("branch3_status") == "YELLOW_OPEN",
        "mask-deficit open-ledger contract drift",
    )

    rank = rank_override if rank_override is not None else load_json(ROOT / RANK_CERT_REL)
    require(
        rank.get("schema") == "rs-mca-m1-kb-branch3-actual-core-mds-v1",
        "rank-ladder predecessor schema drift",
    )
    require(
        rank.get("payload_sha256") == payload_hash(rank),
        "rank-ladder predecessor payload drift",
    )
    rank_contract = rank.get("predecessor_contract", {})
    require(
        rank_contract.get("retained_family_size_gt_15") is True
        and rank_contract.get("rank_minimizing_complete_selector_fixed_before_anchors")
        is True
        and rank_contract.get("syndrome_line")
        == "H e_eta = y0 + eta*y1 WITH y1 != 0"
        and rank_contract.get("transverse_actual_witness_contract") is True
        and rank_contract.get("selected_difference_space")
        == "D_sel=span{e_eta-e_alpha}"
        and rank_contract.get("selected_error_weight_cap") == J,
        "rank-ladder syndrome-line contract drift",
    )
    ladder = rank.get("rank_ladder", {})
    require(
        ladder.get("first_rank_not_uniformly_paid") == RANK_S
        and ladder.get("rank9_residual_core_rank") == RANK_S - 1
        and ladder.get("rank9_basis_carrier_supports") == RANK_S + 1,
        "rank-ladder rank-nine boundary drift",
    )

    sparsification = (
        sparsification_override
        if sparsification_override is not None
        else (ROOT / SPARSIFICATION_REL).read_text(encoding="utf-8")
    )
    sparsification_anchors = [
        r"\label{thm:exact-sparsification}",
        r"B_C^{\rm MCA}(a)=",
        r"\max\{B_C^{\rm CA}(a),\sigma_C(a)\}",
        r"\abs{\supp(e_0)\cup\supp(e_1)}\le t",
        r"B_{C,\Gamma}^{\rm MCA}(a)",
        r"\max\{B_{C,\Gamma}^{\rm CA}(a),\sigma_{C,\Gamma}(a)\}",
        r"\tag{SP3}\label{eq:challenge-sparsification}",
    ]
    for anchor in sparsification_anchors:
        require(anchor in sparsification, f"exact-sparsification anchor drift: {anchor}")

    note = (
        note_override
        if note_override is not None
        else (ROOT / NOTE_REL).read_text(encoding="utf-8")
    )
    note_anchors = [
        PAID_TERMINAL,
        SPARSE_TERMINAL,
        r"e_\eta=f+\eta g-c_\eta",
        r"y_0=Hf",
        r"y_1=Hg",
        "zero extension identifies its restricted and original",
        "zero extension would produce original-code words explaining the pair",
    ]
    for anchor in note_anchors:
        require(anchor in note, f"packet-note semantic anchor drift: {anchor}")


def floor_ratio(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator > 0, "invalid floor ratio")
    return numerator // denominator


def rank_reduction_cap(
    *,
    error_radius: int,
    minimum_distance: int,
    witness_rank: int,
    syndrome_span_rank: int,
) -> int:
    require(0 < error_radius < minimum_distance, "rank-reduction radius outside 0<E<d")
    require(witness_rank >= syndrome_span_rank >= 2, "invalid witness/syndrome ranks")
    exponent = witness_rank - syndrome_span_rank
    numerator = (error_radius + 1) * minimum_distance**exponent
    denominator = (minimum_distance - error_radius) ** exponent
    return floor_ratio(numerator, denominator)


def classify_rank9_selector(
    *,
    predecessor_rank9_contract_present: bool = False,
    one_complete_rank_minimizing_selector: bool = False,
    intrinsic_affine_rank: int | None = None,
    retained_family_gt_15: bool = False,
    transverse_actual_witnesses: bool = False,
    same_restricted_map_and_selector: bool = False,
    syndrome_line_nondegenerate: bool = False,
    syndrome_span_rank: int | None = None,
    witness_column_rank: int | None = None,
    selected_weights_at_most_j: bool = False,
    restricted_code_minimum_distance: int | None = None,
    distinct_slopes: bool = False,
    global_column_far_partition_certified: bool = False,
    global_column_far_state: str | None = None,
    local_lift_to_global_CA_bridge_present: bool = False,
    exact_sparsification_bridge_present: bool = False,
) -> str:
    common = (
        predecessor_rank9_contract_present
        and one_complete_rank_minimizing_selector
        and intrinsic_affine_rank == RANK_S
        and retained_family_gt_15
        and transverse_actual_witnesses
        and same_restricted_map_and_selector
        and syndrome_line_nondegenerate
        and syndrome_span_rank == SYNDROME_SPAN_H
        and witness_column_rank == WITNESS_COLUMN_RANK_T
        and selected_weights_at_most_j
        and restricted_code_minimum_distance == MINIMUM_DISTANCE
        and distinct_slopes
        and global_column_far_partition_certified
    )
    if not common:
        return REJECTED
    if global_column_far_state == "PROVED_NOT_COLUMN_FAR":
        if not exact_sparsification_bridge_present:
            return REJECTED
        return SPARSE_TERMINAL
    if global_column_far_state == "PROVED_COLUMN_FAR":
        if not local_lift_to_global_CA_bridge_present:
            return REJECTED
        if rank_reduction_cap(
            error_radius=J,
            minimum_distance=MINIMUM_DISTANCE,
            witness_rank=WITNESS_COLUMN_RANK_T,
            syndrome_span_rank=SYNDROME_SPAN_H,
        ) > B_REMAINING:
            return REJECTED
        return PAID_TERMINAL
    return REJECTED


def expected_literature_import() -> dict[str, Any]:
    return {
        "title": (
            "A Syndrome--Space Approach to Proximity Gaps and Correlated "
            "Agreement for Random Linear Codes and Random Reed--Solomon Codes"
        ),
        "authors": ["Chen Yuan", "Ruiqi Zhu"],
        "arxiv_id": "2605.07595",
        "arxiv_version_audited": "v2",
        "url": "https://arxiv.org/abs/2605.07595",
        "imported_scope": (
            "DETERMINISTIC_ONE_DIMENSIONAL_CORRELATED_AGREEMENT_"
            "RANK_REDUCTION_ONLY"
        ),
        "local_specialized_reproof_present": True,
        "probabilistic_random_code_results_used": False,
        "proximity_only_full_line_alternative_used": False,
    }


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
        "zero_mask_surplus_Delta0": DELTA_ZERO,
        "restricted_code_minimum_distance_d": MINIMUM_DISTANCE,
        "distance_gap_d_minus_j": GAMMA_NUMERATOR,
        "B_star": str(B_STAR),
        "U_paid": str(U_PAID),
        "B_remaining": str(B_REMAINING),
    }


def expected_predecessor_contract() -> dict[str, Any]:
    return {
        "immediate_predecessor_schema": "rs-mca-m1-kb-branch3-rank9-mask-deficit-v1",
        "rank_ladder_schema": "rs-mca-m1-kb-branch3-actual-core-mds-v1",
        "one_rank_minimizing_complete_selector": True,
        "intrinsic_affine_rank_s": RANK_S,
        "actual_core_rank_r": RANK_S - 1,
        "basis_support_count": RANK_S + 1,
        "basis_carrier_equals_complete_union": True,
        "retained_family_size_gt_15": True,
        "selected_error_weight_cap": J,
        "same_selector_and_restricted_H_V_required": True,
        "transverse_actual_witness_contract": True,
        "rank_at_least_ten_out_of_scope": True,
        "source_semantic_contracts_validated": True,
    }


def expected_syndrome_rank_adapter() -> dict[str, Any]:
    return {
        "selected_syndrome_line": "H_V e_eta=y0+eta*y1 WITH y1!=0",
        "transversality": "{y0,y1} NOT_SUBSET H_V(F^{E_eta}) FOR_EACH_ETA",
        "nondegeneracy_argument": (
            "IF y0 IN span(y1), EVERY NONZERO_SYNDROME_SELECTED_SUPPORT "
            "CONTAINS y0 AND y1; AT_MOST_ONE_SLOPE_HAS_ZERO_SYNDROME; "
            "|Gamma|>15 CONTRADICTS_TRANSVERSALITY"
        ),
        "syndrome_line_nondegenerate": True,
        "syndrome_span_rank_h": SYNDROME_SPAN_H,
        "affine_difference_rank_s": RANK_S,
        "witness_column_rank_identity": "t=s+1",
        "witness_column_rank_t": WITNESS_COLUMN_RANK_T,
        "rank_identity_argument": (
            "span{e_eta}=span({e_alpha} UNION D_sel); "
            "H(D_sel)=span(y1); NONDEGENERACY_GIVES H(e_alpha) NOTIN span(y1)"
        ),
        "selected_columns_are_distinct_slope_witnesses": True,
        "same_field_as_restricted_GRS_code": True,
        "same_selector_and_restricted_map": True,
        "selected_column_weight_bound": J,
        "restricted_kernel_parameters": "[R+nu,nu,R+1]_F",
        "restricted_minimum_distance": MINIMUM_DISTANCE,
    }


def expected_rank_reduction() -> dict[str, Any]:
    return {
        "theorem_scope": "DETERMINISTIC_LINEAR_CODE_CORRELATED_AGREEMENT",
        "E": J,
        "E_plus": J,
        "d": MINIMUM_DISTANCE,
        "hypothesis_0_lt_E_le_Eplus_lt_d": 0 < J <= J < MINIMUM_DISTANCE,
        "gamma_exact": f"{GAMMA_NUMERATOR}/{GAMMA_DENOMINATOR}",
        "gamma_numerator_d_minus_E": GAMMA_NUMERATOR,
        "gamma_denominator_d": GAMMA_DENOMINATOR,
        "witness_rank_t": WITNESS_COLUMN_RANK_T,
        "syndrome_span_rank_h": SYNDROME_SPAN_H,
        "exponent_t_minus_h": REDUCTION_EXPONENT,
        "ball_factor_B_E_Eplus": BALL_FACTOR,
        "no_CA_inequality": (
            "|Gamma|*((d-E)/d)^(t-h)<=FLOOR((Eplus+1)/(Eplus-E+1))"
        ),
        "cap_formula": "FLOOR((j+1)*(R+1)^8/(R+1-j)^8)",
        "cap_numerator": str(CAP_NUMERATOR),
        "cap_denominator": str(CAP_DENOMINATOR),
        "non_CA_cap": str(NON_CA_CAP),
        "cap_fits_remaining_budget": NON_CA_CAP <= B_REMAINING,
        "margin_to_B_remaining": str(NON_CA_MARGIN),
        "budget_factor_floor": B_REMAINING // NON_CA_CAP,
        "correlated_agreement_definition": (
            "EXISTS x0,x1 WITH H_V*x_i=y_i AND "
            "|supp(x0) UNION supp(x1)|<=j"
        ),
        "classification_object": "ORIGINAL_RECEIVED_PAIR_COLUMN_FAR_AT_AGREEMENT_A",
        "column_far_implies_no_restricted_common_lift": (
            "ZERO_EXTEND_ANY_COMMON_H_V_LIFTS; SUBTRACT_FROM_THE_ORIGINAL_PAIR; "
            "OBTAIN_ORIGINAL_CODEWORDS_WITH_COMMON_AGREEMENT_AT_LEAST_A"
        ),
        "correlated_agreement_owner": SPARSE_TERMINAL,
        "non_correlated_agreement_owner": PAID_TERMINAL,
        "sparse_owner_paid_here": False,
    }


def classifier_base() -> dict[str, Any]:
    return {
        "predecessor_rank9_contract_present": True,
        "one_complete_rank_minimizing_selector": True,
        "intrinsic_affine_rank": RANK_S,
        "retained_family_gt_15": True,
        "transverse_actual_witnesses": True,
        "same_restricted_map_and_selector": True,
        "syndrome_line_nondegenerate": True,
        "syndrome_span_rank": SYNDROME_SPAN_H,
        "witness_column_rank": WITNESS_COLUMN_RANK_T,
        "selected_weights_at_most_j": True,
        "restricted_code_minimum_distance": MINIMUM_DISTANCE,
        "distinct_slopes": True,
        "global_column_far_partition_certified": True,
        "local_lift_to_global_CA_bridge_present": True,
        "exact_sparsification_bridge_present": True,
    }


def expected_classifier_contract() -> dict[str, Any]:
    base = classifier_base()
    return {
        "partition_object": "ORIGINAL_RECEIVED_PAIR_COLUMN_FAR_AT_AGREEMENT_A",
        "owner_terminals": [PAID_TERMINAL, SPARSE_TERMINAL],
        "owner_terminal_count": 2,
        "fail_closed_nonterminal": REJECTED,
        "fail_closed_defaults": classify_rank9_selector(),
        "valid_column_far_non_CA": classify_rank9_selector(
            **base,
            global_column_far_state="PROVED_COLUMN_FAR",
        ),
        "valid_not_column_far_sparse_route": classify_rank9_selector(
            **base,
            global_column_far_state="PROVED_NOT_COLUMN_FAR",
        ),
        "unknown_column_far_state_rejected": classify_rank9_selector(**base),
        "CA_without_sparsification_rejected": classify_rank9_selector(
            **{**base, "exact_sparsification_bridge_present": False},
            global_column_far_state="PROVED_NOT_COLUMN_FAR",
        ),
        "column_far_without_local_bridge_rejected": classify_rank9_selector(
            **{**base, "local_lift_to_global_CA_bridge_present": False},
            global_column_far_state="PROVED_COLUMN_FAR",
        ),
        "degenerate_line_rejected": classify_rank9_selector(
            **{**base, "syndrome_line_nondegenerate": False},
            global_column_far_state="PROVED_COLUMN_FAR",
        ),
        "wrong_witness_rank_rejected": classify_rank9_selector(
            **{**base, "witness_column_rank": RANK_S},
            global_column_far_state="PROVED_COLUMN_FAR",
        ),
        "wrong_distance_rejected": classify_rank9_selector(
            **{**base, "restricted_code_minimum_distance": R},
            global_column_far_state="PROVED_COLUMN_FAR",
        ),
        "terminals_disjoint_and_exhaustive_for_certified_column_far_partition": True,
        "CA_terminal_is_route_not_payment": True,
    }


def expected_exact_controls() -> dict[str, Any]:
    return {
        "constant_identities": {
            "R_equals_n_minus_k": R == N - K,
            "j_equals_n_minus_A": J == N - A,
            "Delta0_equals_R_minus_j_equals_A_minus_k": (
                DELTA_ZERO == R - J == A - K
            ),
            "d_equals_R_plus_1": MINIMUM_DISTANCE == R + 1,
            "d_minus_j_equals_Delta0_plus_1": (
                GAMMA_NUMERATOR == DELTA_ZERO + 1
            ),
            "t_equals_s_plus_1": WITNESS_COLUMN_RANK_T == RANK_S + 1,
            "exponent_equals_t_minus_h": (
                REDUCTION_EXPONENT
                == WITNESS_COLUMN_RANK_T - SYNDROME_SPAN_H
            ),
            "B_star_equals_U_paid_plus_B_remaining": (
                B_STAR == U_PAID + B_REMAINING
            ),
        },
        "cap_floor_lower_check": NON_CA_CAP * CAP_DENOMINATOR <= CAP_NUMERATOR,
        "cap_floor_upper_check": CAP_NUMERATOR < (NON_CA_CAP + 1) * CAP_DENOMINATOR,
        "cap_remainder": str(CAP_NUMERATOR % CAP_DENOMINATOR),
        "cap_exact": str(NON_CA_CAP),
        "margin_exact": str(NON_CA_MARGIN),
        "first_forbidden_non_CA_size": str(NON_CA_CAP + 1),
        "first_forbidden_violates_rank_reduction": (
            (NON_CA_CAP + 1) * CAP_DENOMINATOR > CAP_NUMERATOR
        ),
        "q_line_exceeds_remaining_budget": Q_LINE > B_REMAINING,
        "numerical_scale": "EXACT_KOALABEAR_BIG_INTEGERS_PLUS_SAGE_TOY_CONTROL",
        "deployed_field_census_performed": False,
    }


def expected_certificate() -> dict[str, Any]:
    validate_source_contracts()
    certificate: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "literature_import": expected_literature_import(),
        "row": expected_row(),
        "predecessor_contract": expected_predecessor_contract(),
        "syndrome_rank_adapter": expected_syndrome_rank_adapter(),
        "deterministic_rank_reduction": expected_rank_reduction(),
        "classifier_contract": expected_classifier_contract(),
        "exact_controls": expected_exact_controls(),
        "charges": {
            "packet_banked_charge": "0",
            "non_CA_branch_paid_against_remaining_budget": True,
            "correlated_agreement_branch_paid": False,
            "reason_no_ledger_movement": "OPEN_SPARSE_SIGMA_ROUTE_REMAINS",
        },
        "ledger": {
            "U_paid_before": str(U_PAID),
            "U_paid_after": str(U_PAID),
            "B_remaining_before": str(B_REMAINING),
            "B_remaining_after": str(B_REMAINING),
            "rank9_status": "YELLOW_OPEN_SPARSE_SIGMA_ONLY",
            "branch3_status": "YELLOW_OPEN",
            "koalabear_row_status": "YELLOW_OPEN",
            "next_route": "SPARSE_SIGMA_FIRST_MATCH_OWNER_AUDIT",
        },
        "audit_sections": {
            "statement": "fixed-selector rank-nine syndrome-rank CA dichotomy",
            "dependency_status": (
                "PROVED_SPECIALIZED_DETERMINISTIC_LEMMA_PLUS_PROVED_PREDECESSORS_"
                "SPARSE_SIGMA_UNPAID"
            ),
            "parameter_dependence": "EXACT_KOALABEAR_FINITE_ROW_ONLY",
            "layer_cake_dyadic_summability": "NOT_APPLICABLE",
            "moment_markov_chebyshev": "NOT_APPLICABLE",
            "edge_cases": (
                "NONDEGENERACY_t_EQUALS_s_PLUS_1_d_EQUALS_R_PLUS_1_"
                "FLOOR_AND_CA_NOT_PAID_ARE_LOAD_BEARING"
            ),
            "numerical_evidence": (
                "EXACT_INTEGER_CERTIFICATE_AND_TOY_SAGE_CONTROL_NOT_"
                "DEPLOYED_CENSUS"
            ),
            "packet_verdict": "GREEN_NON_CA_ROUTE_CUT",
            "global_verdict": "YELLOW_RANK9_SPARSE_SIGMA_AND_BRANCH3_OPEN",
        },
        "nonclaims": NONCLAIMS,
    }
    certificate["payload_sha256"] = payload_hash(certificate)
    return certificate


def validate_certificate(certificate: dict[str, Any]) -> None:
    require(set(certificate) == TOP_KEYS, "top-level key drift")
    require(certificate["schema"] == SCHEMA, "schema drift")
    require(certificate["artifact_kind"] == ARTIFACT_KIND, "artifact kind drift")
    require(certificate["status"] == STATUS, "status drift")
    require(
        certificate["payload_sha256"] == payload_hash(certificate),
        "payload hash mismatch",
    )

    expected = expected_certificate()
    for key in TOP_KEYS - {"payload_sha256"}:
        require(certificate[key] == expected[key], f"section drift: {key}")
    require(
        certificate["payload_sha256"] == expected["payload_sha256"],
        "expected payload drift",
    )

    bindings = certificate["source_bindings"]
    ids = [row["binding_id"] for row in bindings]
    paths = [row["path"] for row in bindings]
    require(len(ids) == len(set(ids)), "duplicate source binding id")
    require(len(paths) == len(set(paths)), "duplicate source binding path")

    literature = certificate["literature_import"]
    require(
        literature["local_specialized_reproof_present"] is True,
        "external theorem imported without local specialized proof",
    )
    require(
        literature["probabilistic_random_code_results_used"] is False,
        "random-code theorem silently imported",
    )
    require(
        literature["proximity_only_full_line_alternative_used"] is False,
        "weaker full-line alternative substituted for CA dichotomy",
    )

    adapter = certificate["syndrome_rank_adapter"]
    require(adapter["syndrome_line_nondegenerate"], "syndrome line is degenerate")
    require(
        adapter["witness_column_rank_t"] == RANK_S + 1,
        "witness-column rank is not s+1",
    )
    require(
        adapter["syndrome_span_rank_h"] == SYNDROME_SPAN_H,
        "syndrome span rank drift",
    )

    reduction = certificate["deterministic_rank_reduction"]
    require(
        reduction["hypothesis_0_lt_E_le_Eplus_lt_d"],
        "rank-reduction radius hypothesis failed",
    )
    require(
        reduction["exponent_t_minus_h"] == REDUCTION_EXPONENT,
        "rank-reduction exponent drift",
    )
    require(
        int(reduction["non_CA_cap"])
        == rank_reduction_cap(
            error_radius=J,
            minimum_distance=MINIMUM_DISTANCE,
            witness_rank=WITNESS_COLUMN_RANK_T,
            syndrome_span_rank=SYNDROME_SPAN_H,
        ),
        "rank-reduction cap arithmetic drift",
    )
    require(reduction["cap_fits_remaining_budget"], "non-CA cap no longer fits")
    require(int(reduction["margin_to_B_remaining"]) == NON_CA_MARGIN, "margin drift")
    require(reduction["sparse_owner_paid_here"] is False, "sparse owner promoted")

    classifier = certificate["classifier_contract"]
    require(classifier["owner_terminal_count"] == 2, "terminal count drift")
    require(
        classifier["owner_terminals"] == [PAID_TERMINAL, SPARSE_TERMINAL],
        "owner terminal set/order drift",
    )
    require(
        classifier["partition_object"]
        == "ORIGINAL_RECEIVED_PAIR_COLUMN_FAR_AT_AGREEMENT_A",
        "classifier partitioned a restricted lift rather than the original pair",
    )
    require(
        classifier["valid_column_far_non_CA"] == PAID_TERMINAL,
        "column-far non-CA branch not paid",
    )
    require(
        classifier["valid_not_column_far_sparse_route"] == SPARSE_TERMINAL,
        "not-column-far branch not routed to sparse sigma",
    )
    for key in [
        "fail_closed_defaults",
        "unknown_column_far_state_rejected",
        "CA_without_sparsification_rejected",
        "column_far_without_local_bridge_rejected",
        "degenerate_line_rejected",
        "wrong_witness_rank_rejected",
        "wrong_distance_rejected",
    ]:
        require(classifier[key] == REJECTED, f"fail-closed classifier drift: {key}")
    require(classifier["CA_terminal_is_route_not_payment"], "CA route became payment")

    controls = certificate["exact_controls"]
    require(controls["cap_floor_lower_check"], "floor lower inequality failed")
    require(controls["cap_floor_upper_check"], "floor upper inequality failed")
    require(
        controls["first_forbidden_violates_rank_reduction"],
        "first forbidden cap boundary failed",
    )

    charges = certificate["charges"]
    require(charges["packet_banked_charge"] == "0", "charge moved")
    require(charges["non_CA_branch_paid_against_remaining_budget"], "non-CA payment lost")
    require(charges["correlated_agreement_branch_paid"] is False, "CA branch marked paid")
    ledger = certificate["ledger"]
    require(ledger["U_paid_before"] == ledger["U_paid_after"], "U_paid ledger moved")
    require(
        ledger["B_remaining_before"] == ledger["B_remaining_after"],
        "remaining budget moved",
    )
    require(ledger["branch3_status"] == "YELLOW_OPEN", "branch 3 incorrectly closed")


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
        ("paper-id", ("literature_import", "arxiv_id"), "wrong"),
        ("random-code", ("literature_import", "probabilistic_random_code_results_used"), True),
        ("local-proof", ("literature_import", "local_specialized_reproof_present"), False),
        ("full-line", ("literature_import", "proximity_only_full_line_alternative_used"), True),
        ("row-n", ("row", "n"), N - 1),
        ("row-j", ("row", "error_cap_j"), J - 1),
        ("row-d", ("row", "restricted_code_minimum_distance_d"), R),
        ("row-gap", ("row", "distance_gap_d_minus_j"), GAMMA_NUMERATOR - 1),
        ("row-budget", ("row", "B_remaining"), str(B_REMAINING - 1)),
        ("rank-s", ("predecessor_contract", "intrinsic_affine_rank_s"), 8),
        ("selector", ("predecessor_contract", "one_rank_minimizing_complete_selector"), False),
        ("transverse", ("predecessor_contract", "transverse_actual_witness_contract"), False),
        ("family", ("predecessor_contract", "retained_family_size_gt_15"), False),
        ("nondegenerate", ("syndrome_rank_adapter", "syndrome_line_nondegenerate"), False),
        ("h", ("syndrome_rank_adapter", "syndrome_span_rank_h"), 1),
        ("t", ("syndrome_rank_adapter", "witness_column_rank_t"), RANK_S),
        ("rank-identity", ("syndrome_rank_adapter", "witness_column_rank_identity"), "t=s"),
        ("same-map", ("syndrome_rank_adapter", "same_selector_and_restricted_map"), False),
        ("selected-weight", ("syndrome_rank_adapter", "selected_column_weight_bound"), J + 1),
        ("E", ("deterministic_rank_reduction", "E"), J - 1),
        ("Eplus", ("deterministic_rank_reduction", "E_plus"), J + 1),
        ("gamma-num", ("deterministic_rank_reduction", "gamma_numerator_d_minus_E"), GAMMA_NUMERATOR - 1),
        ("exponent", ("deterministic_rank_reduction", "exponent_t_minus_h"), REDUCTION_EXPONENT - 1),
        ("ball-factor", ("deterministic_rank_reduction", "ball_factor_B_E_Eplus"), J),
        ("cap-formula", ("deterministic_rank_reduction", "cap_formula"), "CEIL(...)"),
        ("cap", ("deterministic_rank_reduction", "non_CA_cap"), str(NON_CA_CAP + 1)),
        ("cap-fits", ("deterministic_rank_reduction", "cap_fits_remaining_budget"), False),
        ("margin", ("deterministic_rank_reduction", "margin_to_B_remaining"), str(NON_CA_MARGIN - 1)),
        ("sparse-paid", ("deterministic_rank_reduction", "sparse_owner_paid_here"), True),
        ("terminal-count", ("classifier_contract", "owner_terminal_count"), 1),
        ("terminal-paid", ("classifier_contract", "owner_terminals", 0), "PAID"),
        ("classifier-object", ("classifier_contract", "partition_object"), "RESTRICTED_COMMON_LIFT"),
        ("classifier-nonca", ("classifier_contract", "valid_column_far_non_CA"), SPARSE_TERMINAL),
        ("classifier-ca", ("classifier_contract", "valid_not_column_far_sparse_route"), PAID_TERMINAL),
        ("classifier-default", ("classifier_contract", "fail_closed_defaults"), PAID_TERMINAL),
        ("classifier-unknown", ("classifier_contract", "unknown_column_far_state_rejected"), PAID_TERMINAL),
        ("classifier-local-bridge", ("classifier_contract", "column_far_without_local_bridge_rejected"), PAID_TERMINAL),
        ("classifier-bridge", ("classifier_contract", "CA_without_sparsification_rejected"), SPARSE_TERMINAL),
        ("classifier-route", ("classifier_contract", "CA_terminal_is_route_not_payment"), False),
        ("floor-lower", ("exact_controls", "cap_floor_lower_check"), False),
        ("floor-upper", ("exact_controls", "cap_floor_upper_check"), False),
        ("control-cap", ("exact_controls", "cap_exact"), str(NON_CA_CAP + 1)),
        ("forbidden", ("exact_controls", "first_forbidden_non_CA_size"), str(NON_CA_CAP)),
        ("charge", ("charges", "packet_banked_charge"), "1"),
        ("ca-charge", ("charges", "correlated_agreement_branch_paid"), True),
        ("ledger-paid", ("ledger", "U_paid_after"), str(U_PAID + 1)),
        ("ledger-budget", ("ledger", "B_remaining_after"), str(B_REMAINING - 1)),
        ("rank9-close", ("ledger", "rank9_status"), "GREEN_CLOSED"),
        ("branch-close", ("ledger", "branch3_status"), "GREEN_CLOSED"),
        ("verdict", ("audit_sections", "global_verdict"), "GREEN_ROW_CLOSED"),
        ("nonclaim", ("nonclaims", 1), "The correlated-agreement branch is paid."),
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

    mask_bad = load_json(ROOT / MASK_CERT_REL)
    mask_bad["predecessor_contract"]["intrinsic_affine_rank_s"] = 8
    mask_bad["payload_sha256"] = payload_hash(mask_bad)
    try:
        validate_source_contracts(mask_override=mask_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("mask predecessor semantic tamper accepted")

    mask_weight_bad = load_json(ROOT / MASK_CERT_REL)
    mask_weight_bad["predecessor_contract"]["selected_weight_range"][-1] = J + 1
    mask_weight_bad["payload_sha256"] = payload_hash(mask_weight_bad)
    try:
        validate_source_contracts(mask_override=mask_weight_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("mask predecessor weight-cap tamper accepted")

    rank_bad = load_json(ROOT / RANK_CERT_REL)
    rank_bad["predecessor_contract"]["transverse_actual_witness_contract"] = False
    rank_bad["payload_sha256"] = payload_hash(rank_bad)
    try:
        validate_source_contracts(rank_override=rank_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("rank predecessor semantic tamper accepted")

    rank_weight_bad = load_json(ROOT / RANK_CERT_REL)
    rank_weight_bad["predecessor_contract"]["selected_error_weight_cap"] = J + 1
    rank_weight_bad["payload_sha256"] = payload_hash(rank_weight_bad)
    try:
        validate_source_contracts(rank_override=rank_weight_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("rank predecessor weight-cap tamper accepted")

    sparsification = (ROOT / SPARSIFICATION_REL).read_text(encoding="utf-8")
    sparsification_bad = sparsification.replace(
        r"\tag{SP3}\label{eq:challenge-sparsification}",
        r"\tag{SP3-REMOVED}\label{eq:challenge-sparsification-removed}",
    )
    try:
        validate_source_contracts(sparsification_override=sparsification_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("exact-sparsification semantic tamper accepted")

    note = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    note_bad = note.replace(PAID_TERMINAL, "NON_CA_OWNER_REMOVED")
    try:
        validate_source_contracts(note_override=note_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("packet-note terminal tamper accepted")

    note_bridge_bad = note.replace(
        r"e_\eta=f+\eta g-c_\eta",
        r"e_\eta=UNBOUND_SELECTED_ERROR",
    )
    try:
        validate_source_contracts(note_override=note_bridge_bad)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("packet-note original-pair bridge tamper accepted")

    total = len(cases) + 11
    require(rejected == total, "tamper rejection count drift")
    print(f"PASS tamper-selftest: {rejected}/{total} mutations rejected")


def write_certificate() -> None:
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
        "non-CA rank-nine cap: "
        f"{NON_CA_CAP} <= B_remaining={B_REMAINING}; margin={NON_CA_MARGIN}"
    )
    print(f"terminals: {PAID_TERMINAL} | {SPARSE_TERMINAL}")
    print("ledger: no movement; sparse sigma remains open")


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
