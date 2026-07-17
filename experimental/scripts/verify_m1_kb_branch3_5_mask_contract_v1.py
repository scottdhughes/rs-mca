#!/usr/bin/env python3
"""Verify the KoalaBear branch-3--5 slope-projection contract.

This is a source-status and quantifier certificate.  It deliberately makes no
deployed slope-count or ledger-payment claim.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "rs-mca-m1-kb-branch3-5-mask-contract-v1"
STATUS = (
    "PROVED_SOURCE_STATUS_QUANTIFIER_CONTRACT_"
    "Q0_MEMBERSHIP_GLOBAL_MASK_REPLAY_OPEN"
)

P = 2_130_706_433
EXTENSION_DEGREE = 6
Q_LINE = P**EXTENSION_DEGREE
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
T = A - K
W_PREFIX = T - 1
R_STAR = R // 3
DEEP_COMPOSITE_CAP = R_STAR + 1
BRANCH2_CHARGE = T
DEEP_INCREMENT = DEEP_COMPOSITE_CAP - BRANCH2_CHARGE
B_STAR = (Q_LINE - 1) // (1 << 128)
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID

V2_ORDER = [
    "contained_or_noncontained_failure",
    "rank_drop_or_pivot_failure",
    "tangent_common_line_residue",
    "quotient_periodic_or_divisor_stabilized",
    "planted_prefix_structured",
    "extension_valued_slope",
    "residual_base_slope_universe",
    "sparse_sigma_or_sparse_support",
    "m1_half_turn_or_coefficient_shadow",
    "primitive_qfin_residual",
]

NOTE_REL = Path("experimental/notes/m1/m1_kb_branch3_5_mask_contract_v1.md")
SCRIPT_REL = Path("experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.py")
SAGE_REL = Path("experimental/scripts/verify_m1_kb_branch3_5_mask_contract_v1.sage")
CERT_DIR_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-5-mask-contract-v1"
)
README_REL = CERT_DIR_REL / "README.md"
CERT_REL = CERT_DIR_REL / "m1_kb_branch3_5_mask_contract_v1.json"

BRANCH2_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch2-rank-deep-owner-v1/"
    "m1_kb_branch2_rank_deep_owner_v1.json"
)
BRANCH2_VERIFY_REL = Path(
    "experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py"
)
BRANCH3_DEEP_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-deep-ccl-tdd-v1/"
    "m1_kb_branch3_deep_ccl_tdd_v1.json"
)
BRANCH3_DEEP_VERIFY_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py"
)
BRANCH3_TDD_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-tdd-excess-v1/"
    "m1_kb_branch3_tdd_excess_v1.json"
)
BRANCH3_TDD_VERIFY_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py"
)
BRANCH3_SPARSE_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-rank9-sparse-chart-boundary-v1/"
    "m1_kb_branch3_rank9_sparse_chart_boundary_v1.json"
)
BRANCH3_SPARSE_VERIFY_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_rank9_sparse_chart_boundary_v1.py"
)
Q0_CERT_REL = Path(
    "experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/"
    "kb_mca_1116048_first_match_ledger_v1.json"
)
Q0_VERIFY_REL = Path(
    "experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py"
)
POST_C5_CERT_REL = Path(
    "experimental/data/certificates/m1-fp2-post-c5-mask-incidence-v1/"
    "m1_fp2_post_c5_mask_incidence_v1.json"
)
POST_C5_VERIFY_REL = Path(
    "experimental/scripts/verify_m1_fp2_post_c5_mask_incidence_v1.py"
)
Q0_NOTE_REL = Path(
    "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md"
)

SOURCE_RELS = [
    NOTE_REL,
    README_REL,
    SCRIPT_REL,
    SAGE_REL,
    Path("experimental/asymptotic_rs_mca_frontiers.tex"),
    Path("experimental/notes/m1/m1_fp2_post_c5_mask_incidence_v1.md"),
    Path("experimental/notes/m1/m1_kb_branch2_hankel_pivot_adapter_v1.md"),
    Path("experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md"),
    Path("experimental/notes/m1/m1_kb_branch3_deep_ccl_tdd_v1.md"),
    Path("experimental/notes/m1/m1_kb_branch3_tdd_excess_v1.md"),
    Path("experimental/notes/m1/m1_kb_branch3_rank9_sparse_chart_boundary_v1.md"),
    Q0_NOTE_REL,
    BRANCH2_CERT_REL,
    BRANCH2_VERIFY_REL,
    BRANCH3_DEEP_CERT_REL,
    BRANCH3_DEEP_VERIFY_REL,
    BRANCH3_TDD_CERT_REL,
    BRANCH3_TDD_VERIFY_REL,
    BRANCH3_SPARSE_CERT_REL,
    BRANCH3_SPARSE_VERIFY_REL,
    Q0_CERT_REL,
    Q0_VERIFY_REL,
    POST_C5_CERT_REL,
    POST_C5_VERIFY_REL,
]


class ContractError(RuntimeError):
    """Raised when a source or semantic contract fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


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


def reject_nonfinite(token: str) -> None:
    raise ContractError(f"non-finite JSON number rejected: {token}")


def parse_finite_float(token: str) -> float:
    value = float(token)
    require(math.isfinite(value), f"non-finite JSON float rejected: {token}")
    return value


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key rejected: {key}")
        result[key] = value
    return result


def parse_json_strict(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite,
            parse_float=parse_finite_float,
        )
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON in {label}: {exc}") from exc
    require(type(value) is dict, f"top-level JSON object required in {label}")
    return value


def load_json_strict(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON source: {path}")
    return parse_json_strict(path.read_text(encoding="utf-8"), str(path))


def exact_value(value: Any, expected: Any, label: str) -> Any:
    require(type(value) is type(expected), f"{label}: exact type drift")
    require(value == expected, f"{label}: semantic value drift")
    return value


def at_path(value: Any, path: tuple[Any, ...], label: str) -> Any:
    cursor = value
    for key in path:
        require(type(cursor) in (dict, list), f"{label}: invalid path container")
        try:
            cursor = cursor[key]
        except (KeyError, IndexError, TypeError) as exc:
            raise ContractError(f"{label}: missing path {path}") from exc
    return cursor


def require_path(
    value: dict[str, Any], path: tuple[Any, ...], expected: Any, label: str
) -> Any:
    return exact_value(at_path(value, path, label), expected, label)


def verify_payload_hash(
    certificate: dict[str, Any], label: str, *, blank_field: bool = False
) -> str:
    stored = at_path(certificate, ("payload_sha256",), label)
    require(type(stored) is str and len(stored) == 64, f"{label}: payload hash shape")
    payload = copy.deepcopy(certificate)
    if blank_field:
        payload["payload_sha256"] = ""
    else:
        payload.pop("payload_sha256", None)
    require(stored == canonical_hash(payload), f"{label}: payload hash mismatch")
    return stored


def source_bindings(root: Path) -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    for relative in SOURCE_RELS:
        absolute = root / relative
        require(absolute.is_file(), f"missing source binding: {relative}")
        bindings.append({"path": str(relative), "sha256": sha256_file(absolute)})
    return bindings


def predecessor_semantics(
    root: Path,
    overrides: dict[Path, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Validate the exact predecessor claims imported by this packet."""
    def load(relative: Path) -> dict[str, Any]:
        if overrides is not None and relative in overrides:
            return copy.deepcopy(overrides[relative])
        return load_json_strict(root / relative)

    branch2 = load(BRANCH2_CERT_REL)
    require_path(
        branch2,
        ("schema",),
        "rs-mca-m1-kb-branch2-rank-deep-owner-v1",
        "branch2 schema",
    )
    require_path(
        branch2,
        ("status",),
        (
            "PROVED_FIELD_NATIVE_RANK_DROP_POLICY_DEEP_MCA_OWNER_"
            "BRANCH2_CLOSED_LEGACY_BRIDGE_RETIRED_PARTIAL_LEDGER"
        ),
        "branch2 status",
    )
    branch2_payload = verify_payload_hash(branch2, "branch2")
    require_path(branch2, ("rank_drop_policy", "rank_field"), "AMBIENT_F", "branch2 rank field")
    require_path(branch2, ("rank_drop_policy", "rank_threshold"), T, "branch2 rank threshold")
    require_path(
        branch2,
        ("rank_drop_policy", "requires_actual_bad_incidence"),
        True,
        "branch2 actual-incidence gate",
    )
    require_path(branch2, ("deep_mca_owner", "upper_bound"), T, "branch2 owner cap")
    require_path(
        branch2,
        ("branch2_first_match", "v2_order"),
        V2_ORDER,
        "branch2 first-match order",
    )
    require_path(
        branch2,
        ("branch2_first_match", "branch1_projector_complete"),
        False,
        "branch2 branch1 status",
    )
    require_path(
        branch2,
        ("branch2_first_match", "branch2_local_policy_complete"),
        True,
        "branch2 local status",
    )
    require_path(
        branch2,
        ("branch2_first_match", "global_mask_replay_complete"),
        False,
        "branch2 global replay",
    )
    require_path(
        branch2,
        ("branch2_first_match", "pivot_failure_empty_imported_from_predecessor"),
        True,
        "branch2 empty pivot cell",
    )
    require_path(
        branch2,
        ("branch2_first_match", "pivot_failure_owner"),
        "EMPTY_ACTUAL_BAD_SLOPE_SET",
        "branch2 pivot owner",
    )
    require_path(
        branch2,
        ("branch2_first_match", "pivot_failure_charge"),
        "0",
        "branch2 pivot charge",
    )
    require_path(
        branch2,
        ("branch2_first_match", "full_row_rank_pivot_success_survives_to_branch"),
        3,
        "branch2 successor branch",
    )
    require_path(branch2, ("ledger", "branch2_closed"), True, "branch2 ledger closure")
    require_path(branch2, ("ledger", "U_Q"), None, "branch2 U_Q")
    require_path(branch2, ("ledger", "U_A"), None, "branch2 U_A")

    branch3_deep = load(BRANCH3_DEEP_CERT_REL)
    require_path(
        branch3_deep,
        ("schema",),
        "rs-mca-m1-kb-branch3-deep-ccl-tdd-v1",
        "branch3-deep schema",
    )
    require_path(
        branch3_deep,
        ("status",),
        (
            "PROVED_DEEP_OWNER_EXTENSION_EXACT_SHARED_ENVELOPE_ACCOUNTING_"
            "DELTA_PROVED_CCL_TDD_DICHOTOMY_BRANCH3_ROW_OPEN"
        ),
        "branch3-deep status",
    )
    branch3_deep_payload = verify_payload_hash(branch3_deep, "branch3-deep")
    require_path(
        branch3_deep,
        ("deep_owner_extension", "membership"),
        "exists declared exact-A noncontained witness with |E_gamma|<=r_star",
        "branch3-deep membership",
    )
    require_path(
        branch3_deep,
        ("deep_owner_extension", "r_star"),
        R_STAR,
        "branch3-deep r_star",
    )
    require_path(
        branch3_deep,
        ("deep_owner_extension", "composite_upper_bound"),
        DEEP_COMPOSITE_CAP,
        "branch3-deep composite cap",
    )
    require_path(
        branch3_deep,
        ("deep_owner_extension", "incremental_charge"),
        DEEP_INCREMENT,
        "branch3-deep increment",
    )
    require_path(
        branch3_deep,
        ("heavy_residual", "intrinsic_deletion"),
        "remove every slope admitting any declared witness with |E_gamma|<=r_star",
        "branch3-deep deletion quantifier",
    )
    require_path(
        branch3_deep,
        ("branch_scope", "v2_order"),
        V2_ORDER,
        "branch3-deep first-match order",
    )
    require_path(
        branch3_deep,
        ("branch_scope", "branch1_projector_complete"),
        False,
        "branch3-deep branch1 status",
    )
    require_path(
        branch3_deep,
        ("branch_scope", "global_mask_replay_complete"),
        False,
        "branch3-deep global replay",
    )
    require_path(
        branch3_deep,
        ("branch_scope", "branch3_closed"),
        False,
        "branch3-deep closure",
    )
    require_path(
        branch3_deep,
        ("branch_scope", "literal_branch3_subset_of_full_row_rank_envelope"),
        True,
        "branch3-deep successor envelope",
    )
    require_path(
        branch3_deep,
        ("branch_scope", "monotone_under_earlier_first_match_deletion"),
        True,
        "branch3-deep monotonicity",
    )
    require_path(
        branch3_deep,
        ("ledger", "U_paid_after"),
        str(U_PAID),
        "branch3-deep paid total",
    )
    require_path(
        branch3_deep,
        ("ledger", "B_remaining_after"),
        str(B_REMAINING),
        "branch3-deep remaining budget",
    )

    branch3_tdd = load(BRANCH3_TDD_CERT_REL)
    require_path(
        branch3_tdd,
        ("schema",),
        "rs-mca-m1-kb-branch3-tdd-excess-v1",
        "branch3-tdd schema",
    )
    require_path(
        branch3_tdd,
        ("status",),
        (
            "PROVED_EXACT_TDD_SHORTENING_DEFECT_SPAN_BRIDGE_RANK3_GLOBAL_"
            "TERMINAL_FAIL_CLOSED_NO_LEDGER_MOVEMENT"
        ),
        "branch3-tdd status",
    )
    branch3_tdd_payload = verify_payload_hash(branch3_tdd, "branch3-tdd")
    require_path(
        branch3_tdd,
        ("owner_registry", "global_carrier_owner_uses_minimum_over_complete_selectors"),
        True,
        "branch3-tdd minimum selector quantifier",
    )
    require_path(
        branch3_tdd,
        ("owner_registry", "carrier_complement_makes_every_complete_selector_high_union"),
        True,
        "branch3-tdd universal complement",
    )
    require_path(
        branch3_tdd,
        ("predecessor_state", "global_carrier_paid_through_excess"),
        10,
        "branch3-tdd carrier cutoff",
    )
    require_path(
        branch3_tdd,
        ("classifier_contract", "deployed_complete_selector_certificate_present"),
        False,
        "branch3-tdd deployed selector inventory",
    )
    require_path(
        branch3_tdd,
        ("ledger", "packet_banked_charge"),
        "0",
        "branch3-tdd banked charge",
    )

    branch3_sparse = load(BRANCH3_SPARSE_CERT_REL)
    require_path(
        branch3_sparse,
        ("schema",),
        "rs-mca-m1-kb-branch3-rank9-sparse-chart-boundary-v1",
        "branch3-sparse schema",
    )
    require_path(
        branch3_sparse,
        ("status",),
        (
            "PROVED_LOCAL_SPARSE_TANGENT_AND_CHART_BOUNDARY_CONDITIONAL_CAP_"
            "REGULAR_ROUTE_OPEN_NO_LEDGER_MOVEMENT"
        ),
        "branch3-sparse status",
    )
    branch3_sparse_payload = verify_payload_hash(branch3_sparse, "branch3-sparse")
    require_path(
        branch3_sparse,
        ("charges", "global_first_match_aggregation_proved"),
        False,
        "branch3-sparse global aggregation",
    )
    require_path(
        branch3_sparse,
        ("charges", "packet_banked_charge"),
        "0",
        "branch3-sparse banked charge",
    )
    require_path(
        branch3_sparse,
        ("first_match_classifier", "later_owner_masks_pending"),
        True,
        "branch3-sparse later masks",
    )
    require_path(
        branch3_sparse,
        (
            "first_match_classifier",
            "local_partition_precedes_global_owner_intersection",
        ),
        True,
        "branch3-sparse local partition",
    )
    require_path(
        branch3_sparse,
        ("first_match_classifier", "tangent_first"),
        True,
        "branch3-sparse tangent order",
    )
    require_path(
        branch3_sparse,
        ("first_match_classifier", "sparse_subcell_order"),
        [
            "SPARSE_TANGENT_RANK9_CONDITIONAL_CAP",
            "SPARSE_CHART_BOUNDARY_RANK9_CONDITIONAL_CAP",
            "REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE",
        ],
        "branch3-sparse subcell order",
    )
    require_path(
        branch3_sparse,
        ("first_match_classifier", "regular_terminal_is_route_not_payment"),
        True,
        "branch3-sparse regular terminal",
    )

    q0 = load(Q0_CERT_REL)
    require_path(q0, ("status",), "CONDITIONAL", "Q0 source status")
    require_path(q0, ("row_packet", "n"), N, "Q0 n")
    require_path(q0, ("row_packet", "k"), K, "Q0 k")
    require_path(q0, ("row_packet", "agreement"), A, "Q0 agreement")
    require_path(q0, ("row_packet", "B_star"), B_STAR, "Q0 budget")
    require_path(
        q0,
        ("quotient_planted_descent", "condition_for_descent"),
        "r_c <= w",
        "Q0 descent gate",
    )
    require_path(
        q0,
        ("quotient_planted_descent", "fiber_bound"),
        "top c-quotient/planted fiber injects into lower Phi_{w_c} fiber",
        "Q0 fixed-fibre injection",
    )
    require_path(
        q0,
        ("quotient_planted_descent", "terminal_raw_paid_cost"),
        471_447_040,
        "Q0 terminal cost",
    )
    terminals = at_path(
        q0,
        ("quotient_planted_descent", "terminal_raw_paid_rungs"),
        "Q0 terminal rungs",
    )
    require(type(terminals) is list and len(terminals) == 2, "Q0 terminal rung count")
    require_path(terminals[0], ("c",), 65_536, "Q0 first terminal rung")
    require_path(terminals[0], ("raw_quotient_count",), 471_435_600, "Q0 first terminal cost")
    require_path(terminals[1], ("c",), 131_072, "Q0 second terminal rung")
    require_path(terminals[1], ("raw_quotient_count",), 11_440, "Q0 second terminal cost")
    first_match = at_path(q0, ("first_match_branches",), "Q0 first-match branches")
    require(type(first_match) is list, "Q0 first-match branch list")
    q0_cells = [
        cell
        for cell in first_match
        if type(cell) is dict
        and cell.get("branch") == "quotient_periodic_or_divisor_stabilized"
    ]
    require(len(q0_cells) == 1, "Q0 first-match branch uniqueness")
    require_path(q0_cells[0], ("cost",), 471_447_040, "Q0 first-match cost")
    require_path(q0_cells[0], ("order",), 4, "Q0 first-match order")
    require_path(
        q0_cells[0],
        ("deducted_in_proved_ledger",),
        True,
        "Q0 first-match deduction",
    )
    q0_note = (root / Q0_NOTE_REL).read_text(encoding="utf-8")
    require(
        (
            "If `r_c <= w`, then inside each top prefix fiber "
            "`Phi_w^{-1}(z)`, the map"
        )
        in q0_note,
        "Q0 fixed-top-prefix source anchor missing",
    )

    post_c5 = load(POST_C5_CERT_REL)
    require_path(
        post_c5,
        ("schema",),
        "rs-mca-m1-fp2-post-c5-mask-incidence-v1",
        "post-C5 schema",
    )
    require_path(
        post_c5,
        ("status",),
        (
            "PROVED_NEW_POLICY_AND_TWO_COLUMN_SPLIT_IMPORTED_C5_RANK_"
            "CLOSURES_APPLIED_ROW_OPEN"
        ),
        "post-C5 status",
    )
    post_c5_payload = verify_payload_hash(post_c5, "post-C5", blank_field=True)
    require_path(
        post_c5,
        ("mask_inventory", "record_count"),
        5,
        "post-C5 branch record count",
    )
    require_path(
        post_c5,
        ("mask_inventory", "complete_executable_adapter"),
        False,
        "post-C5 adapter status",
    )
    require_path(
        post_c5,
        ("mask_inventory", "first_missing_executable_branch"),
        2,
        "post-C5 first missing branch",
    )
    inventory_records = at_path(
        post_c5, ("mask_inventory", "records"), "post-C5 branch records"
    )
    require(
        type(inventory_records) is list and len(inventory_records) == 5,
        "post-C5 branch records shape",
    )
    for index, branch in enumerate(V2_ORDER[:5], start=1):
        require_path(
            inventory_records[index - 1],
            ("order",),
            index,
            f"post-C5 branch {index} order",
        )
        require_path(
            inventory_records[index - 1],
            ("branch",),
            branch,
            f"post-C5 branch {index} label",
        )
    require_path(
        inventory_records[0],
        ("actual_slope_projector_complete",),
        False,
        "post-C5 branch1 projector",
    )
    require_path(
        inventory_records[1],
        ("machine_status",),
        "UNBOUND_SOURCE_SYMBOL",
        "post-C5 historical branch2 status",
    )
    require_path(
        inventory_records[3],
        ("machine_status",),
        "PARTIAL_FAMILY_NO_COMPLETE_PROJECTOR",
        "post-C5 branch4 status",
    )
    require_path(
        inventory_records[4],
        ("machine_status",),
        "SOURCE_STATUS_ONLY",
        "post-C5 branch5 status",
    )
    require_path(
        inventory_records[4],
        ("executable_predicate",),
        None,
        "post-C5 branch5 predicate",
    )
    require_path(
        inventory_records[4],
        ("actual_slope_projector_complete",),
        False,
        "post-C5 branch5 projector",
    )
    require_path(
        post_c5,
        ("ledger", "ledger_consequence"),
        False,
        "post-C5 ledger consequence",
    )
    require_path(post_c5, ("ledger", "U_Q"), None, "post-C5 U_Q")
    require_path(post_c5, ("ledger", "U_A"), None, "post-C5 U_A")
    require_path(post_c5, ("ledger", "row_complete"), False, "post-C5 row status")

    def record(
        cert_rel: Path, verifier_rel: Path, schema: str | None, payload: str | None
    ) -> dict[str, Any]:
        return {
            "certificate": str(cert_rel),
            "certificate_sha256": sha256_file(root / cert_rel),
            "verifier": str(verifier_rel),
            "verifier_sha256": sha256_file(root / verifier_rel),
            "schema": schema,
            "payload_sha256": payload,
        }

    return {
        "branch2_rank_deep_owner": {
            **record(
                BRANCH2_CERT_REL,
                BRANCH2_VERIFY_REL,
                branch2["schema"],
                branch2_payload,
            ),
            "rank_field": branch2["rank_drop_policy"]["rank_field"],
            "rank_threshold": branch2["rank_drop_policy"]["rank_threshold"],
            "global_charge": branch2["deep_mca_owner"]["upper_bound"],
            "v2_order": branch2["branch2_first_match"]["v2_order"],
            "pivot_failure_empty": branch2["branch2_first_match"][
                "pivot_failure_empty_imported_from_predecessor"
            ],
            "branch1_projector_complete": False,
            "branch2_local_policy_complete": True,
            "global_mask_replay_complete": False,
        },
        "branch3_deep_owner": {
            **record(
                BRANCH3_DEEP_CERT_REL,
                BRANCH3_DEEP_VERIFY_REL,
                branch3_deep["schema"],
                branch3_deep_payload,
            ),
            "membership": branch3_deep["deep_owner_extension"]["membership"],
            "r_star": branch3_deep["deep_owner_extension"]["r_star"],
            "composite_cap": branch3_deep["deep_owner_extension"]["composite_upper_bound"],
            "incremental_charge": branch3_deep["deep_owner_extension"]["incremental_charge"],
            "branch3_closed": False,
        },
        "branch3_complete_selector": {
            **record(
                BRANCH3_TDD_CERT_REL,
                BRANCH3_TDD_VERIFY_REL,
                branch3_tdd["schema"],
                branch3_tdd_payload,
            ),
            "minimum_over_complete_selectors": True,
            "universal_complement": True,
            "paid_through_excess": 10,
            "deployed_complete_selector_inventory_present": False,
        },
        "branch3_rank9_sparse": {
            **record(
                BRANCH3_SPARSE_CERT_REL,
                BRANCH3_SPARSE_VERIFY_REL,
                branch3_sparse["schema"],
                branch3_sparse_payload,
            ),
            "global_first_match_aggregation_proved": False,
            "local_partition_precedes_global_owner_intersection": True,
            "later_owner_masks_pending": True,
            "regular_terminal_is_route_not_payment": True,
        },
        "branch4_q0": {
            **record(Q0_CERT_REL, Q0_VERIFY_REL, None, None),
            "status": q0["status"],
            "condition_for_descent": q0["quotient_planted_descent"]["condition_for_descent"],
            "fiber_bound": q0["quotient_planted_descent"]["fiber_bound"],
            "first_match_order": q0_cells[0]["order"],
            "terminal_raw_paid_cost": q0["quotient_planted_descent"]["terminal_raw_paid_cost"],
            "terminal_rungs": [65_536, 131_072],
            "source_scope": "FIXED_TOP_PREFIX_FIBRE_ONLY",
        },
        "historical_post_c5_inventory": {
            **record(
                POST_C5_CERT_REL,
                POST_C5_VERIFY_REL,
                post_c5["schema"],
                post_c5_payload,
            ),
            "ledger_consequence": False,
            "historical_branch2_machine_status": inventory_records[1]["machine_status"],
            "branch5_machine_status": inventory_records[4]["machine_status"],
            "row_complete": False,
            "U_Q": None,
            "U_A": None,
        },
    }


def q0_decomposition(
    n: int, j: int, c: int, co_support: Iterable[int]
) -> dict[str, Any]:
    """Rebuild the canonical Q0 full-fibre decomposition on exponent indices."""
    require(type(n) is int and type(j) is int and type(c) is int, "Q0 integers required")
    require(n > 0 and n % c == 0, "c must divide n")
    require(0 <= j <= n, "invalid co-support size")
    raw_points = list(co_support)
    require(
        all(type(value) is int for value in raw_points),
        "co-support indices must be exact integers",
    )
    points = set(raw_points)
    require(len(points) == j, "co-support cardinality mismatch")
    require(all(0 <= value < n for value in points), "co-support index out of range")

    n_c = n // c
    j_c, r_c = divmod(j, c)
    full_fibres: list[int] = []
    covered: set[int] = set()
    for residue in range(n_c):
        fibre = {residue + lift * n_c for lift in range(c)}
        if fibre <= points:
            full_fibres.append(residue)
            covered.update(fibre)
    leftover = sorted(points - covered)
    qualifies = len(full_fibres) == j_c and len(leftover) == r_c
    return {
        "qualifies": qualifies,
        "tautological_zero_quotient_core": j_c == 0,
        "branch4_route_eligible": qualifies and j_c >= 1,
        "c": c,
        "n_c": n_c,
        "j_c": j_c,
        "r_c": r_c,
        "full_fibre_residues": full_fibres,
        "leftover": leftover,
    }


def first_q0_rung(
    n: int, j: int, co_support: Iterable[int], ordered_rungs: Iterable[int]
) -> int | None:
    points = tuple(co_support)
    rungs = tuple(ordered_rungs)
    require(all(type(c) is int for c in rungs), "Q0 rungs must be exact integers")
    for c in rungs:
        if q0_decomposition(n, j, c, points)["branch4_route_eligible"]:
            return c
    return None


def project_existential_witness_cell(
    witnesses: Iterable[dict[str, Any]], predicate
) -> set[int]:
    projected: set[int] = set()
    for witness in witnesses:
        slope = witness["slope"]
        require(type(slope) is int, "witness slope must be an exact integer")
        if predicate(witness):
            projected.add(slope)
    return projected


def complete_selector_gate(
    excesses: Iterable[int],
    *,
    selector_universe_exhaustive: bool,
    cutoff: int = 10,
) -> dict[str, Any]:
    require(
        type(selector_universe_exhaustive) is bool,
        "selector-universe exhaustiveness must be an exact Boolean",
    )
    values = list(excesses)
    require(
        all(type(value) is int for value in values),
        "selector excesses must be exact integers",
    )
    require(values, "complete-selector family must be nonempty")
    minimum = min(values)
    return {
        "input_role": "TOY_EXHAUSTIVE_SELECTOR_LIST",
        "selector_universe_exhaustive": selector_universe_exhaustive,
        "minimum_excess": minimum,
        "owner_eligible": minimum <= cutoff,
        "universal_complement_certified": (
            selector_universe_exhaustive and minimum >= cutoff + 1
        ),
    }


def q0_rung_table() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for exponent in range(1, 22):
        c = 1 << exponent
        n_c = N // c
        j_c, r_c = divmod(J, c)
        w_c = W_PREFIX // c
        descent = r_c <= W_PREFIX
        terminal = c in (65_536, 131_072)
        if j_c == 0:
            status = "TAUTOLOGICAL_DIAGNOSTIC_NOT_OWNER"
        elif descent and c <= 16:
            status = "PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND"
        elif descent and c < 65_536:
            status = "PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND"
        elif descent and terminal:
            status = "PROVED_DESCENT_AND_RAW_PAID"
        else:
            status = "OPEN_PLANTED_TAIL_R_GREATER_THAN_W"
        rows.append(
            {
                "c": c,
                "n_c": n_c,
                "j_c": j_c,
                "r_c": r_c,
                "w_c": w_c,
                "descent_condition_r_c_le_w": descent,
                "terminal_raw_paid": terminal,
                "terminal_raw_count": math.comb(n_c, j_c) if terminal else None,
                "positive_quotient_core": j_c >= 1,
                "zero_core_membership_tautological": j_c == 0,
                "branch4_route_can_use_rung": j_c >= 1,
                "status": status,
            }
        )
    return rows


def toy_controls() -> dict[str, Any]:
    n = 16
    j = 7
    rungs = [2, 4, 8, 16]
    overlap = [0, 4, 8, 12, 1, 9, 2]
    c4_only = [0, 4, 8, 12, 1, 2, 3]
    neither = [0, 1, 2, 3, 4, 5, 6]

    overlap_c2 = q0_decomposition(n, j, 2, overlap)
    overlap_c4 = q0_decomposition(n, j, 4, overlap)
    c4_only_c2 = q0_decomposition(n, j, 2, c4_only)
    c4_only_c4 = q0_decomposition(n, j, 4, c4_only)
    neither_c2 = q0_decomposition(n, j, 2, neither)
    neither_c4 = q0_decomposition(n, j, 4, neither)
    neither_c8 = q0_decomposition(n, j, 8, neither)
    neither_c16 = q0_decomposition(n, j, 16, neither)

    require(overlap_c2["qualifies"] and overlap_c4["qualifies"], "overlap toy drift")
    require(not c4_only_c2["qualifies"] and c4_only_c4["qualifies"], "c4-only toy drift")
    require(not neither_c2["qualifies"] and not neither_c4["qualifies"], "negative toy drift")
    require(neither_c8["qualifies"] and neither_c16["qualifies"], "zero-core diagnostic drift")
    require(
        not neither_c8["branch4_route_eligible"]
        and not neither_c16["branch4_route_eligible"],
        "zero-core rung entered branch 4",
    )
    require(first_q0_rung(n, j, overlap, rungs) == 2, "Q0 first rung drift")
    require(first_q0_rung(n, j, c4_only, rungs) == 4, "Q0 c4 rung drift")
    require(first_q0_rung(n, j, neither, rungs) is None, "Q0 negative rung drift")

    witnesses = [
        {"slope": 11, "witness_id": "heavy-first", "error_weight": 5},
        {"slope": 11, "witness_id": "light-second", "error_weight": 2},
        {"slope": 13, "witness_id": "heavy-only", "error_weight": 4},
    ]
    deep_projection = project_existential_witness_cell(
        witnesses, lambda witness: witness["error_weight"] <= 2
    )
    require(deep_projection == {11}, "existential witness projection drift")

    selector_mixed = complete_selector_gate(
        [12, 10], selector_universe_exhaustive=True
    )
    selector_high = complete_selector_gate(
        [12, 11], selector_universe_exhaustive=True
    )
    selector_high_incomplete = complete_selector_gate(
        [12, 11], selector_universe_exhaustive=False
    )
    require(selector_mixed["owner_eligible"], "existential selector gate drift")
    require(not selector_mixed["universal_complement_certified"], "selector complement drift")
    require(not selector_high["owner_eligible"], "high selector owner drift")
    require(selector_high["universal_complement_certified"], "universal selector complement drift")
    require(
        not selector_high_incomplete["universal_complement_certified"],
        "incomplete selector list certified a universal complement",
    )

    q0_witnesses = [
        {"slope": 17, "witness_id": "negative-first", "co_support": neither},
        {"slope": 17, "witness_id": "overlap-second", "co_support": overlap},
        {"slope": 19, "witness_id": "c4-only", "co_support": c4_only},
        {"slope": 23, "witness_id": "negative", "co_support": neither},
    ]
    assignments: dict[str, int] = {}
    for slope in sorted({record["slope"] for record in q0_witnesses}):
        eligible = []
        for record in q0_witnesses:
            if record["slope"] != slope:
                continue
            rung = first_q0_rung(n, j, record["co_support"], rungs)
            if rung is not None:
                eligible.append(rung)
        if eligible:
            assignments[str(slope)] = min(eligible, key=rungs.index)
    require(assignments == {"17": 2, "19": 4}, "slope-level Q0 assignment drift")

    return {
        "row": {"n": n, "j": j, "ordered_rungs": rungs},
        "co_supports": {
            "overlap_c2_c4": overlap,
            "c4_only": c4_only,
            "neither": neither,
        },
        "q0": {
            "overlap_c2": overlap_c2,
            "overlap_c4": overlap_c4,
            "c4_only_c2": c4_only_c2,
            "c4_only_c4": c4_only_c4,
            "neither_c2": neither_c2,
            "neither_c4": neither_c4,
            "neither_c8_tautological": neither_c8,
            "neither_c16_tautological": neither_c16,
            "first_rung_overlap": 2,
            "first_rung_c4_only": 4,
            "first_rung_neither": None,
            "slope_projection_assignments": assignments,
            "first_witness_only_classifier_would_be_wrong_for_slope": 17,
        },
        "witness_projection": {
            "records": witnesses,
            "deep_cutoff": 2,
            "deep_slope_projection": sorted(deep_projection),
            "first_witness_only_classifier_would_be_wrong_for_slope": 11,
        },
        "selector_quantifiers": {
            "mixed_excesses": [12, 10],
            "mixed_result": selector_mixed,
            "all_high_excesses": [12, 11],
            "all_high_result": selector_high,
            "incomplete_high_result": selector_high_incomplete,
        },
    }


def build_artifact(root: Path) -> dict[str, Any]:
    semantics = predecessor_semantics(root)
    rows = q0_rung_table()
    terminal_rows = [row for row in rows if row["terminal_raw_paid"]]
    terminal_cost = sum(int(row["terminal_raw_count"]) for row in terminal_rows)
    open_rows = [row["c"] for row in rows if row["status"].startswith("OPEN_")]
    positive_core_open_rows = [
        row["c"]
        for row in rows
        if row["status"].startswith("OPEN_") and row["positive_quotient_core"]
    ]
    zero_core_rows = [row["c"] for row in rows if row["zero_core_membership_tautological"]]
    require([row["c"] for row in terminal_rows] == [65_536, 131_072], "terminal rung drift")
    require(terminal_cost == 471_447_040, "terminal Q0 cost drift")
    require(open_rows == [262_144, 524_288], "open rung drift")
    require(positive_core_open_rows == [262_144, 524_288], "positive-core open rung drift")
    require(zero_core_rows == [1_048_576, 2_097_152], "zero-core rung drift")
    require(B_STAR == 274_980_728_111_395_087, "target budget drift")
    require(B_REMAINING == 274_980_725_508_892_088, "remaining budget drift")

    return {
        "schema": SCHEMA,
        "status": STATUS,
        "source_bindings": source_bindings(root),
        "predecessor_semantics": semantics,
        "row": {
            "p": P,
            "ambient_degree": EXTENSION_DEGREE,
            "q_line": Q_LINE,
            "n": N,
            "k": K,
            "agreement_A": A,
            "redundancy_R": R,
            "co_support_size_j": J,
            "hankel_row_count_t": T,
            "prefix_depth_w": W_PREFIX,
        },
        "first_match": {
            "order": semantics["branch2_rank_deep_owner"]["v2_order"],
            "cell_projection": "Z(C)={gamma: EXISTS witness over gamma in C}",
            "first_match_formula": "Z_i_circ=Z(C_i)_MINUS_UNION_h_lt_i Z(C_h)",
            "eligibility_quantifier": "EXISTS_WITNESS_AT_SLOPE",
            "complement_quantifier": "ALL_WITNESSES_AT_SLOPE_FAIL",
            "choose_one_witness_before_projection": False,
            "complete_global_replay": False,
        },
        "branch1": {
            "literal_slope_projector_complete": False,
            "status": "UNBOUND_SLOPE_LEVEL_PROJECTOR",
        },
        "branch2": {
            "historical_post_c5_inventory_status": semantics[
                "historical_post_c5_inventory"
            ]["historical_branch2_machine_status"],
            "historical_status_superseded": True,
            "envelope_predicate_source_bound": True,
            "envelope": "Bad_A(f,g) INTERSECT {gamma: rank_F M_A(gamma)<t}",
            "ambient_rank_field": "F",
            "pivot_failure_empty_on_actual_noncontained_incidence": semantics[
                "branch2_rank_deep_owner"
            ]["pivot_failure_empty"],
            "global_envelope_charge": semantics["branch2_rank_deep_owner"]["global_charge"],
            "successor_envelope": "Bad_A(f,g)_MINUS_Z_2_env(f,g)",
            "successor_full_row_rank": True,
            "literal_first_match_projector_complete": False,
            "literal_blocker": "Z_1(f,g) has no source-bound slope-level projector",
        },
        "branch3": {
            "deep_owner": {
                "actual_error_weight_cutoff_r_star": R_STAR,
                "eligibility": "EXISTS valid witness with |E_gamma|<=r_star",
                "complement": "ALL valid witnesses have |E_gamma|>=r_star+1",
                "branch2_plus_deep_shared_cap": DEEP_COMPOSITE_CAP,
                "already_charged_branch2": BRANCH2_CHARGE,
                "banked_increment": DEEP_INCREMENT,
            },
            "low_excess_selector_owner": {
                "kappa_definition": "MIN_complete_selector max(0,|UNION E_gamma|-R)",
                "cutoff": semantics["branch3_complete_selector"]["paid_through_excess"],
                "eligibility": "EXISTS complete selector with kappa<=10",
                "complement": (
                    "ALL complete selectors have kappa>=11, only after a "
                    "certified exhaustive complete-selector universe"
                ),
                "failure_of_one_supplied_selector_is_complement": False,
                "deployed_complete_selector_inventory_present": semantics[
                    "branch3_complete_selector"
                ]["deployed_complete_selector_inventory_present"],
                "helper_role": "TOY_LOGICAL_QUANTIFIER_ONLY_NOT_DEPLOYED_ENUMERATOR",
            },
            "rank9_sparse_local_partition_proved": semantics[
                "branch3_rank9_sparse"
            ]["local_partition_precedes_global_owner_intersection"],
            "rank9_sparse_global_first_match_aggregation_proved": False,
            "regular_terminal": "REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE",
            "branch_complete": False,
        },
        "branch4_q0": {
            "input_object": "size-j padded co-support T=D\\S",
            "not_input_object": "actual nonzero error support",
            "membership": (
                "T=P DISJOINT_UNION pi_c^-1(Q), "
                "|Q|=floor(j/c), |P|=j mod c"
            ),
            "canonical_complete_fibre_test": True,
            "slope_eligibility": (
                "EXISTS witness over gamma satisfying Q0 membership with "
                "floor(j/c)>=1"
            ),
            "branch4_route_filter": "Q0 membership AND floor(j/c)>=1",
            "zero_core_rule": (
                "floor(j/c)=0 makes raw membership tautological and does not "
                "create a branch-4 route"
            ),
            "rung_first_match": "FIRST positive-core eligible c in frozen dyadic order",
            "rungs": rows,
            "terminal_rungs": [65_536, 131_072],
            "terminal_raw_union_cost": terminal_cost,
            "open_tail_rungs": open_rows,
            "positive_core_open_tail_rungs": positive_core_open_rows,
            "zero_core_tautological_rungs": zero_core_rows,
            "source_open_tail_rungs_before_route_filter": [
                262_144,
                524_288,
                1_048_576,
                2_097_152,
            ],
            "all_rungs_paid": False,
            "support_periodicity_implies_invariant_data_descent": False,
            "terminal_payment_scope": semantics["branch4_q0"]["source_scope"],
            "membership_alone_instantiates_terminal_payment": False,
            "terminal_raw_cost_is_imported_not_newly_banked": True,
        },
        "branch5": {
            "status": "UNBOUND_SOURCE_FAMILY",
            "algebraic_plant_family_declared": False,
            "candidate_census_proved": False,
            "residual_prefix_scale_declared": False,
            "distinct_slope_projection_bound_proved": False,
            "complement_available": False,
        },
        "downstream_contract": {
            "exact_after_branches_3_5_residual_available": False,
            "forbidden_claim": "DEPLOYED_COMPLEMENT_AFTER_BRANCHES_3_TO_5",
            "allowed_monotone_strategy": (
                "bound an explicitly declared successor envelope in full, "
                "without subtracting unbound later masks"
            ),
            "full_projective_or_gm_control_is_deployed_residual": False,
        },
        "toy_controls": toy_controls(),
        "ledger": {
            "B_star": B_STAR,
            "U_paid_before": U_PAID,
            "U_paid_after": U_PAID,
            "B_remaining_before": B_REMAINING,
            "B_remaining_after": B_REMAINING,
            "U_Q": None,
            "U_A": None,
            "ledger_movement": 0,
            "koalabear_row_closed": False,
        },
        "conclusions": [
            "BRANCH2_ENVELOPE_STATUS_REFRESHED",
            "BRANCH3_SELECTOR_QUANTIFIERS_FROZEN",
            "Q0_CO_SUPPORT_MEMBERSHIP_EXECUTABLE",
            "Q0_ZERO_CORE_TAUTOLOGY_EXCLUDED_FROM_BRANCH4",
            "GLOBAL_BRANCH1_TO_5_MASK_REPLAY_REMAINS_OPEN",
            "BRANCH5_COMPLEMENT_FORBIDDEN",
            "NO_LEDGER_MOVEMENT",
        ],
    }


def validate_artifact(
    artifact: dict[str, Any],
    root: Path,
    *,
    expected: dict[str, Any] | None = None,
) -> None:
    require(type(artifact) is dict, "artifact must be an exact JSON object")
    if expected is None:
        expected = build_artifact(root)
    require(
        canonical_bytes(artifact) == canonical_bytes(expected),
        "artifact differs from regenerated canonical contract",
    )

    require(artifact["schema"] == SCHEMA, "schema drift")
    require(artifact["status"] == STATUS, "status drift")
    require(artifact["row"]["co_support_size_j"] == N - A == 981_104, "j drift")
    require(artifact["row"]["hankel_row_count_t"] == A - K == 67_472, "t drift")
    require(not artifact["branch1"]["literal_slope_projector_complete"], "branch 1 invented")
    require(artifact["branch2"]["envelope_predicate_source_bound"], "branch 2 envelope lost")
    require(not artifact["branch2"]["literal_first_match_projector_complete"], "branch 2 literal replay invented")
    require(not artifact["branch3"]["branch_complete"], "branch 3 incorrectly closed")
    require(not artifact["branch4_q0"]["all_rungs_paid"], "Q0 open rungs erased")
    require(
        artifact["branch4_q0"]["zero_core_tautological_rungs"]
        == [1_048_576, 2_097_152],
        "Q0 zero-core rungs drift",
    )
    for row in artifact["branch4_q0"]["rungs"]:
        if row["zero_core_membership_tautological"]:
            require(
                not row["branch4_route_can_use_rung"],
                "Q0 zero-core rung entered branch 4",
            )
    require(not artifact["branch5"]["complement_available"], "branch 5 complement invented")
    require(not artifact["downstream_contract"]["exact_after_branches_3_5_residual_available"], "downstream residual invented")
    require(
        type(artifact["ledger"]["ledger_movement"]) is int,
        "ledger movement must be an exact integer",
    )
    require(artifact["ledger"]["ledger_movement"] == 0, "ledger moved")
    require(
        type(artifact["branch5"]["complement_available"]) is bool,
        "branch 5 complement must be an exact Boolean",
    )
    require(
        type(artifact["row"]["co_support_size_j"]) is int,
        "co-support size must be an exact integer",
    )
    require(artifact["ledger"]["U_Q"] is None and artifact["ledger"]["U_A"] is None, "null owner changed")


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    cursor = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def refresh_payload_hash(document: dict[str, Any], *, blank_field: bool) -> None:
    if blank_field:
        document["payload_sha256"] = ""
        document["payload_sha256"] = canonical_hash(document)
    else:
        document.pop("payload_sha256", None)
        document["payload_sha256"] = canonical_hash(document)


def predecessor_source_mutation_selftest(root: Path) -> int:
    mutations: list[
        tuple[str, Path, tuple[Any, ...], Any, bool | None]
    ] = [
        (
            "branch2-first-match-order",
            BRANCH2_CERT_REL,
            ("branch2_first_match", "v2_order"),
            list(reversed(V2_ORDER)),
            False,
        ),
        (
            "branch2-empty-pivot",
            BRANCH2_CERT_REL,
            (
                "branch2_first_match",
                "pivot_failure_empty_imported_from_predecessor",
            ),
            False,
            False,
        ),
        (
            "branch3-sparse-local-partition",
            BRANCH3_SPARSE_CERT_REL,
            (
                "first_match_classifier",
                "local_partition_precedes_global_owner_intersection",
            ),
            False,
            False,
        ),
        (
            "q0-first-match-order",
            Q0_CERT_REL,
            ("first_match_branches", 3, "order"),
            9,
            None,
        ),
        (
            "q0-fixed-fibre-scope",
            Q0_CERT_REL,
            ("quotient_planted_descent", "fiber_bound"),
            "GLOBAL_ACROSS_ALL_PREFIX_TARGETS",
            None,
        ),
        (
            "post-c5-historical-branch2-status",
            POST_C5_CERT_REL,
            ("mask_inventory", "records", 1, "machine_status"),
            "PAID_COMPLETE",
            True,
        ),
        (
            "post-c5-branch5-family",
            POST_C5_CERT_REL,
            ("mask_inventory", "records", 4, "executable_predicate"),
            "DECLARED_PLANTED_FAMILY",
            True,
        ),
    ]
    caught = 0
    for name, relative, path, replacement, payload_mode in mutations:
        candidate = load_json_strict(root / relative)
        set_path(candidate, path, replacement)
        if payload_mode is not None:
            refresh_payload_hash(candidate, blank_field=payload_mode)
        try:
            predecessor_semantics(root, overrides={relative: candidate})
        except ContractError:
            caught += 1
        else:
            raise ContractError(f"predecessor source mutation escaped: {name}")
    require(caught == len(mutations), "predecessor source mutation count drift")
    return caught


def tamper_selftest(root: Path) -> int:
    baseline = build_artifact(root)
    mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("schema", ("schema",), "wrong-schema"),
        ("status", ("status",), "GREEN_CLOSED"),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
        (
            "predecessor-semantic-field",
            ("predecessor_semantics", "branch2_rank_deep_owner", "rank_field"),
            "BASE_FIELD",
        ),
        (
            "predecessor-payload",
            ("predecessor_semantics", "branch3_deep_owner", "payload_sha256"),
            "0" * 64,
        ),
        ("j", ("row", "co_support_size_j"), 980_104),
        ("j-float", ("row", "co_support_size_j"), float(J)),
        ("t", ("row", "hankel_row_count_t"), 67_471),
        ("first-match-complete", ("first_match", "complete_global_replay"), True),
        ("chosen-witness", ("first_match", "choose_one_witness_before_projection"), True),
        ("branch1", ("branch1", "literal_slope_projector_complete"), True),
        ("branch2-supersession", ("branch2", "historical_status_superseded"), False),
        ("branch2-envelope", ("branch2", "envelope_predicate_source_bound"), False),
        ("branch2-field", ("branch2", "ambient_rank_field"), "K"),
        ("branch2-charge", ("branch2", "global_envelope_charge"), 67_471),
        ("branch2-literal", ("branch2", "literal_first_match_projector_complete"), True),
        ("deep-cutoff", ("branch3", "deep_owner", "actual_error_weight_cutoff_r_star"), 349_524),
        ("deep-cap", ("branch3", "deep_owner", "branch2_plus_deep_shared_cap"), 349_525),
        ("deep-increment", ("branch3", "deep_owner", "banked_increment"), 282_055),
        ("selector-cutoff", ("branch3", "low_excess_selector_owner", "cutoff"), 11),
        ("selector-complement", ("branch3", "low_excess_selector_owner", "failure_of_one_supplied_selector_is_complement"), True),
        (
            "selector-inventory",
            ("branch3", "low_excess_selector_owner", "deployed_complete_selector_inventory_present"),
            True,
        ),
        ("sparse-global", ("branch3", "rank9_sparse_global_first_match_aggregation_proved"), True),
        ("branch3-close", ("branch3", "branch_complete"), True),
        ("q0-input", ("branch4_q0", "input_object"), "actual error support"),
        ("q0-canonical", ("branch4_q0", "canonical_complete_fibre_test"), False),
        ("q0-terminal", ("branch4_q0", "terminal_raw_union_cost"), 471_447_039),
        ("q0-open", ("branch4_q0", "open_tail_rungs"), []),
        ("q0-zero-core", ("branch4_q0", "zero_core_tautological_rungs"), []),
        (
            "q0-zero-core-route",
            ("branch4_q0", "rungs", 19, "branch4_route_can_use_rung"),
            True,
        ),
        ("q0-paid", ("branch4_q0", "all_rungs_paid"), True),
        ("q0-payment-scope", ("branch4_q0", "terminal_payment_scope"), "GLOBAL_ALL_TARGETS"),
        ("q0-membership-pays", ("branch4_q0", "membership_alone_instantiates_terminal_payment"), True),
        ("quotient-descent", ("branch4_q0", "support_periodicity_implies_invariant_data_descent"), True),
        ("branch5-family", ("branch5", "algebraic_plant_family_declared"), True),
        ("branch5-projection", ("branch5", "distinct_slope_projection_bound_proved"), True),
        ("branch5-complement", ("branch5", "complement_available"), True),
        ("branch5-bool-as-int", ("branch5", "complement_available"), 0),
        ("downstream", ("downstream_contract", "exact_after_branches_3_5_residual_available"), True),
        ("deployed-control", ("downstream_contract", "full_projective_or_gm_control_is_deployed_residual"), True),
        ("toy-first-rung", ("toy_controls", "q0", "first_rung_overlap"), 4),
        ("toy-projection", ("toy_controls", "witness_projection", "deep_slope_projection"), []),
        (
            "toy-incomplete-selector",
            (
                "toy_controls",
                "selector_quantifiers",
                "incomplete_high_result",
                "universal_complement_certified",
            ),
            True,
        ),
        ("U-paid", ("ledger", "U_paid_after"), U_PAID + 1),
        ("UQ-null", ("ledger", "U_Q"), 0),
        ("UA-null", ("ledger", "U_A"), 0),
        ("ledger-move", ("ledger", "ledger_movement"), 1),
        ("ledger-bool-as-int", ("ledger", "ledger_movement"), False),
        ("row-close", ("ledger", "koalabear_row_closed"), True),
    ]

    caught = 0
    for name, path, replacement in mutations:
        candidate = copy.deepcopy(baseline)
        set_path(candidate, path, replacement)
        try:
            validate_artifact(candidate, root, expected=baseline)
        except ContractError:
            caught += 1
        else:
            raise ContractError(f"mutation escaped: {name}")
    require(caught == len(mutations), "mutation count drift")
    parser_mutations = [
        ('{"schema":"first","schema":"second"}', "duplicate-key"),
        ('{"value":NaN}', "nonfinite-NaN"),
        ('{"value":Infinity}', "nonfinite-infinity"),
        ('{"value":1e9999}', "nonfinite-exponent-overflow"),
    ]
    parser_caught = 0
    for serialized, name in parser_mutations:
        try:
            parse_json_strict(serialized, name)
        except ContractError:
            parser_caught += 1
        else:
            raise ContractError(f"serialized mutation escaped: {name}")
    require(parser_caught == len(parser_mutations), "parser mutation count drift")
    source_caught = predecessor_source_mutation_selftest(root)
    print(
        f"PASS tamper self-test: {caught}/{len(mutations)} semantic/type mutations "
        f"and {parser_caught}/{len(parser_mutations)} parser mutations and "
        f"{source_caught} predecessor-source mutations rejected"
    )
    return 0


def write_artifact(root: Path) -> int:
    path = root / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    artifact = build_artifact(root)
    path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE {CERT_REL}")
    return 0


def check_artifact(root: Path) -> int:
    path = root / CERT_REL
    require(path.is_file(), f"missing certificate: {CERT_REL}")
    artifact = load_json_strict(path)
    validate_artifact(artifact, root)
    print("PASS m1-kb-branch3-5-mask-contract-v1")
    print("  branch 2 envelope: source-bound; literal replay blocked by branch 1")
    print("  branch 3: existential/universal selector quantifiers frozen")
    print("  branch 4: exact Q0 co-support membership and rung order")
    print("  branch 5: UNBOUND_SOURCE_FAMILY")
    print("  ledger movement: 0")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    root = repo_root()
    try:
        if args.write:
            return write_artifact(root)
        if args.check:
            return check_artifact(root)
        return tamper_selftest(root)
    except (ContractError, OSError, ValueError, KeyError, TypeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
