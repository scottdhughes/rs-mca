#!/usr/bin/env python3
r"""Verify the moving-root cofactor/slack and C5 boundary packet.

For a qualifying post-source-rational full-outside rank-two record, the
entire moving-zero set is a root set of the full-gcd-reduced polynomial
``Pbar + eta*Qbar``.  This gives ``x+delta <= e`` and the exact slack identity

    (deg(H)-c) + (e-x) + (k-1-deg(H)-e) = s-t-1.

The zero-slack boundary ``s=t+1`` is projectively base-defined and is already
owned by canonical C5.  The surviving route cut is therefore

    s >= 67,474, e >= 33,737, deg(H) <= 1,014,838.

This is a zero-ledger-movement local theorem.  It does not construct a
deployed selector, pay the two one-slack primitive components, or close the
KoalaBear row.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_branch3_rank9_rich_pencil_atlas_v1 as rich_atlas
import verify_m1_kb_projective_base_pair_c5_owner_v1 as c5_owner
import verify_m1_kb_rank9_source_rational_owner_splice_v1 as source_rational


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-moving-root-slack-c5-boundary-v1"
ARTIFACT_KIND = "M1_KB_RANK9_MOVING_ROOT_SLACK_C5_BOUNDARY"
STATUS = (
    "PROVED_MOVING_ROOT_COFACTOR_SLACK_C5_ZERO_BOUNDARY_"
    "ZERO_LEDGER_MOVEMENT_ONE_SLACK_RESIDUAL_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-moving-root-slack-c5-boundary-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_rank9_moving_root_slack_c5_boundary_v1.json"
NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_moving_root_slack_c5_boundary_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-moving-root-slack-c5-boundary-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.sage"
)

SOURCE_RATIONAL_PAYLOAD = (
    "773de0cabafe7bf79d38adfb927bcf99b3e9f345bcd5102e06c13813b39a03d6"
)
RICH_ATLAS_PAYLOAD = (
    "343b3bbc6ac526da12ff06988c1a280b9845f2a6117c8bc75820d55b594f6258"
)
C5_OWNER_PAYLOAD = (
    "14e7112a3cc8aafce591d1962543c1e8789b7815c333ef4cd4f3b12279b5c6bb"
)

P = source_rational.P
N = source_rational.N
K = source_rational.K
A = source_rational.A
J = source_rational.J
T = source_rational.T
RICH_X_MAX = source_rational.RICH_X_MAX

OLD_SOURCE_FLOOR = source_rational.SURVIVOR_SIGMA_FLOOR
OLD_DEGREE_FLOOR = source_rational.SURVIVOR_DEGREE_FLOOR
OLD_GCD_CEILING = source_rational.SURVIVOR_GCD_CEILING
OLD_CLOSED_GCD_COUNT = source_rational.ADAPTIVELY_CLOSED_GCD_COUNT

ZERO_SLACK_SOURCE = T + 1
RESIDUAL_SOURCE_FLOOR = T + 2
RESIDUAL_DEGREE_FLOOR = (RESIDUAL_SOURCE_FLOOR + 1) // 2
RESIDUAL_GCD_CEILING = K - 1 - RESIDUAL_DEGREE_FLOOR
CLOSED_GCD_FLOOR = RESIDUAL_GCD_CEILING + 1
CLOSED_GCD_CEILING = K - 2
CLOSED_GCD_COUNT = CLOSED_GCD_CEILING - CLOSED_GCD_FLOOR + 1
ADDITIONAL_CLOSED_GCD_COUNT = CLOSED_GCD_COUNT - OLD_CLOSED_GCD_COUNT

U_PAID_BEFORE = source_rational.U_PAID_AFTER
U_PAID_AFTER = U_PAID_BEFORE
B_REMAINING_BEFORE = source_rational.B_REMAINING_AFTER
B_REMAINING_AFTER = B_REMAINING_BEFORE
LEDGER_MOVEMENT = 0

PREDECESSOR_TERMINAL = source_rational.HIGH_DEGREE_TERMINAL
PAID_ZERO_SLACK_TERMINAL = "PAID_PROJECTIVE_BASE_PAIR_C5_AT_SOURCE_SLACK_ZERO"
PAID_ONE_SLACK_TERMINAL = "PAID_PROJECTIVE_BASE_PAIR_C5_AT_ONE_SOURCE_SLACK"
NEW_TERMINAL = "UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67474"
GCD_TWIST_TERMINAL = "UNPAID_NONBASE_COMMON_LINEAR_GCD_TWIST"
MOVING_COFACTOR_TERMINAL = (
    "UNPAID_SPLIT_GCD_NONBASE_LINEAR_MOVING_COFACTOR"
)
SOURCE_LOAD_TERMINAL = source_rational.SOURCE_LOAD_TERMINAL

FIRST_MATCH_ORDER = list(source_rational.FIRST_MATCH_ORDER)
C5_OWNER_ID = "projective_base_pair_C5"
SOURCE_RATIONAL_OWNER_ID = source_rational.SOURCE_OWNER_ID

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessors",
    "counted_object_contract",
    "inherited_record_contract",
    "moving_root_cofactor",
    "slack_normal_form",
    "c5_boundary_absorption",
    "revised_residual",
    "one_slack_frontier",
    "first_match_partition",
    "exact_control",
    "ledger",
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
        source_binding("proof-note", NOTE_REL, "cofactor, slack, and C5 boundary proof"),
        source_binding("python-verifier", SCRIPT_REL, "certificate, arithmetic, and mutations"),
        source_binding("sage-control", SAGE_REL, "exact base-descent and one-slack controls"),
        source_binding("readme", README_REL, "replay and scope contract"),
        source_binding(
            "source-rational-note",
            source_rational.NOTE_REL,
            "immediate predecessor and adaptive residual",
        ),
        source_binding(
            "source-rational-certificate",
            source_rational.CERT_PATH.relative_to(ROOT),
            "immediate predecessor payload",
        ),
        source_binding(
            "source-rational-verifier",
            source_rational.SCRIPT_REL,
            "post-restart source-rational semantics",
        ),
        source_binding(
            "source-rational-sage",
            source_rational.SAGE_REL,
            "predecessor exact controls",
        ),
        source_binding(
            "rich-pencil-note",
            rich_atlas.NOTE_REL,
            "full moving-zero identity and support equations",
        ),
        source_binding(
            "rich-pencil-certificate",
            rich_atlas.CERT_PATH.relative_to(ROOT),
            "moving-zero predecessor payload",
        ),
        source_binding(
            "rich-pencil-verifier",
            rich_atlas.PYTHON_REL,
            "moving-zero semantic contract",
        ),
        source_binding(
            "rich-pencil-sage",
            rich_atlas.SAGE_REL,
            "predecessor exact atlas controls",
        ),
        source_binding(
            "c5-owner-note",
            c5_owner.NOTE_REL,
            "projective-base C5 owner and gauge descent",
        ),
        source_binding(
            "c5-owner-certificate",
            c5_owner.CERT_PATH.relative_to(ROOT),
            "C5 predecessor payload",
        ),
        source_binding(
            "c5-owner-verifier",
            c5_owner.SCRIPT_REL,
            "C5 first-match and ledger semantics",
        ),
        source_binding(
            "c5-owner-sage",
            c5_owner.SAGE_REL,
            "C5 exact projective controls",
        ),
        source_binding(
            "projective-c5-theorem",
            c5_owner.PROJECTIVE_C5_NOTE_REL,
            "intrinsic field and witness-exhaustive C5 theorem",
        ),
    ]


def validate_predecessors() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_doc = source_rational.load_json(source_rational.CERT_PATH)
    source_rational.validate_certificate(source_doc)
    require(
        source_doc["payload_sha256"] == SOURCE_RATIONAL_PAYLOAD,
        "source-rational payload drift",
    )

    rich_doc = rich_atlas.load_json(rich_atlas.CERT_PATH)
    rich_atlas.validate_certificate(rich_doc)
    require(
        rich_doc["payload_sha256"] == RICH_ATLAS_PAYLOAD,
        "rich-pencil payload drift",
    )

    c5_doc = c5_owner.load_json(c5_owner.CERT_PATH)
    c5_owner.validate_certificate(c5_doc)
    require(c5_doc["payload_sha256"] == C5_OWNER_PAYLOAD, "C5 payload drift")
    return source_doc, rich_doc, c5_doc


def validate_consumed_facts(
    source_doc: dict[str, Any],
    rich_doc: dict[str, Any],
    c5_doc: dict[str, Any],
) -> None:
    pair = source_doc["pair_global_source_contract"]
    require(pair["fixed_received_pair"] is True, "received-pair scope drift")
    require(pair["fixed_sp3_translation"] is True, "translation drift")
    require(pair["source_label_nonzero_on_Sigma"] is True, "source support drift")
    require(pair["pair_global_fields_survive_selector_restart"] == [
        "epsilon_0", "epsilon_1", "Sigma", "s"
    ], "restart source fields drift")

    record = source_doc["cross_selector_containment"]
    require(
        record["full_outside_each_selector"] == "V_sigma INTERSECT Sigma is empty",
        "full-outside drift",
    )
    require(record["coefficient_rank_each_line"] == 2, "rank-two drift")
    require(record["contributing_beta_positive"] is True, "beta drift")
    require(record["contributing_J_at_least"] == 21, "J floor drift")
    require(record["full_monic_gcd_used_each_line"] is True, "full-gcd drift")
    require(record["post_restart_application_to_Gamma_out"] is True, "restart drift")
    require(record["subset_stable_for_every_Gamma_subset_Gamma_in"] is True, "subset stability drift")

    residual = source_doc["adaptive_residual"]
    require(
        residual["survivor_degree_condition"] == "e_L>=E(s)+1=ceil(s/2)",
        "adaptive survivor drift",
    )
    require(
        residual["rank_two_reduced_degree_upper_bound"] == "e_L<=s+x_L-t-1",
        "reduced-degree upper bound drift",
    )
    require(residual["terminal"] == PREDECESSOR_TERMINAL, "predecessor terminal drift")

    moving = rich_doc["moving_zero_system"]
    require(moving["x_definition"] == "x_L=M_L-j", "moving x definition drift")
    require(
        moving["moving_zero_size"] == "|F_eta,L|=x_L+delta_eta",
        "whole moving-zero identity drift",
    )
    require(moving["moving_zero_disjoint"] is True, "moving-set disjointness drift")
    require(
        moving["transversality_floor"] == "x_L+delta_eta>=1",
        "moving transversality drift",
    )
    sparse = rich_doc["sparse_pencil"]
    require(
        sparse["codeword_form"]
        == ["a_L=epsilon_0-ev(P_L)", "b_L=epsilon_1-ev(Q_L)"],
        "source coupling drift",
    )
    require(
        sparse["gcd_locator"]
        == "L_((D-W_L)-Sigma) divides gcd(P_L,Q_L)",
        "forced locator drift",
    )

    c5_joint = c5_doc["joint_owner_theorem"]
    require(
        c5_joint["base_projective_pair_condition"]
        == "rank(Y_R)>0 and F_proj(R)=F_p",
        "C5 condition drift",
    )
    require(c5_joint["rank_zero_noncontained_fiber_empty"] is True, "rank-zero drift")
    require(
        c5_doc["first_match_partition"]["projective_base_pair_cell_owns_all_post5_slopes"] is True,
        "C5 exhaustion drift",
    )
    require(
        c5_doc["first_match_partition"]["later_cells_empty_when_projective_field_is_base"] is True,
        "C5 later-cell drift",
    )

    ledger = source_doc["ledger"]
    require(ledger["U_paid_after"] == str(U_PAID_BEFORE), "U_paid drift")
    require(ledger["B_remaining_after"] == str(B_REMAINING_BEFORE), "B_remaining drift")
    require(ledger["incremental_ledger_movement"] == "0", "predecessor movement drift")
    require(ledger["U_Q"] is None, "U_Q drift")


def slack_profile(
    source_size: int,
    x_value: int,
    reduced_degree: int,
    gcd_degree: int,
) -> dict[str, int]:
    for value, label in (
        (source_size, "source size"),
        (x_value, "x"),
        (reduced_degree, "reduced degree"),
        (gcd_degree, "gcd degree"),
    ):
        exact_int(value, label)
    c_value = A - x_value - source_size
    return {
        "r": source_size - T - 1,
        "h": gcd_degree - c_value,
        "u": reduced_degree - x_value,
        "ell": K - 1 - gcd_degree - reduced_degree,
        "c": c_value,
    }


def nonnegative_triples(total: int) -> list[list[int]]:
    exact_int(total, "slack total")
    require(total >= 0, "negative slack total")
    return [
        [h, u, total - h - u]
        for h in range(total + 1)
        for u in range(total - h + 1)
    ]


def validate_exact_arithmetic() -> None:
    require(ZERO_SLACK_SOURCE == 67_473, "zero-slack source drift")
    require(RESIDUAL_SOURCE_FLOOR == 67_474, "residual source drift")
    require(RESIDUAL_DEGREE_FLOOR == 33_737, "residual degree drift")
    require(RESIDUAL_GCD_CEILING == 1_014_838, "residual gcd drift")
    require(CLOSED_GCD_FLOOR == 1_014_839, "closed gcd floor drift")
    require(CLOSED_GCD_CEILING == 1_048_574, "closed gcd ceiling drift")
    require(CLOSED_GCD_COUNT == 33_736, "closed gcd count drift")
    require(ADDITIONAL_CLOSED_GCD_COUNT == 15_319, "additional count drift")
    require(OLD_SOURCE_FLOOR == 36_836, "predecessor source floor drift")
    require(OLD_DEGREE_FLOOR == 18_418, "predecessor degree floor drift")
    require(OLD_GCD_CEILING == 1_030_157, "predecessor gcd ceiling drift")
    require(OLD_CLOSED_GCD_COUNT == 18_417, "predecessor closed count drift")
    require(nonnegative_triples(0) == [[0, 0, 0]], "zero-slack simplex drift")
    require(
        nonnegative_triples(1) == [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
        "one-slack simplex drift",
    )

    # Exhaust small exact slack values.  This checks the printed identity,
    # not the existence of selector records.
    profiles_checked = 0
    for r_value in range(8):
        source_size = T + 1 + r_value
        for h_value, u_value, ell_value in nonnegative_triples(r_value):
            x_value = 10 + r_value
            c_value = A - x_value - source_size
            gcd_degree = c_value + h_value
            reduced_degree = x_value + u_value
            profile = slack_profile(source_size, x_value, reduced_degree, gcd_degree)
            require(
                [profile["h"], profile["u"], profile["ell"]]
                == [h_value, u_value, ell_value],
                "slack reconstruction drift",
            )
            require(profile["h"] + profile["u"] + profile["ell"] == profile["r"], "slack sum drift")
            profiles_checked += 1
    require(profiles_checked == 120, "slack exhaust count drift")
    require(LEDGER_MOVEMENT == 0, "ledger movement drift")
    require(U_PAID_AFTER == U_PAID_BEFORE, "U_paid changed")
    require(B_REMAINING_AFTER == B_REMAINING_BEFORE, "B_remaining changed")


_EXPECTED_CACHE: dict[str, Any] | None = None


def expected_certificate() -> dict[str, Any]:
    global _EXPECTED_CACHE
    if _EXPECTED_CACHE is not None:
        return copy.deepcopy(_EXPECTED_CACHE)

    source_doc, rich_doc, c5_doc = validate_predecessors()
    validate_consumed_facts(source_doc, rich_doc, c5_doc)
    validate_exact_arithmetic()

    note_text = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        "Lemma 3.1 (full moving-root cofactor)",
        "Lemma 4.1 (slack simplex)",
        "Theorem 5.1 (zero-slack boundary is already C5-owned)",
        NEW_TERMINAL,
        GCD_TWIST_TERMINAL,
        MOVING_COFACTOR_TERMINAL,
    ):
        require(token in note_text, f"proof-note token missing: {token}")

    sage_text = (ROOT / SAGE_REL).read_text(encoding="utf-8")
    require("def require(condition, message):" in sage_text, "Sage fail-closed helper missing")
    require(
        all(not line.lstrip().startswith("assert ") for line in sage_text.splitlines()),
        "bare Sage assert is unsafe under optimized Python",
    )

    result: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "row": {
            "row_id": "koalabear-mca-A1116048",
            "p": P,
            "extension_degree": source_rational.tangent.EXTENSION_DEGREE,
            "q_line": str(P ** source_rational.tangent.EXTENSION_DEGREE),
            "n": N,
            "k": K,
            "agreement_A": A,
            "error_count_j": J,
            "syndrome_depth_t": T,
            "rich_x_max": RICH_X_MAX,
        },
        "predecessors": {
            "source_rational_owner": "payload-sha256:" + SOURCE_RATIONAL_PAYLOAD,
            "rich_pencil_atlas": "payload-sha256:" + RICH_ATLAS_PAYLOAD,
            "projective_base_pair_C5_owner": "payload-sha256:" + C5_OWNER_PAYLOAD,
        },
        "counted_object_contract": {
            "object": "distinct support-wise MCA-bad finite slopes of one fixed received pair",
            "new_owner_added": False,
            "new_slope_set_charged": False,
            "boundary_routes_to_existing_C5_owner": True,
            "per_selector_charge_forbidden": True,
            "determinant_mass_counted": False,
            "support_line_basis_or_witness_multiplicity_counted": False,
            "projective_infinity_counted_as_finite": False,
        },
        "inherited_record_contract": {
            "scope": "post-C5 post-source-rational rebuilt complete selector",
            "fixed_received_pair": True,
            "fixed_sp3_translation": True,
            "full_outside": "V INTERSECT Sigma is empty",
            "coefficient_rank": 2,
            "beta_positive": True,
            "J_at_least": 21,
            "selected_slopes_finite": True,
            "low_deficit": "delta_eta=j-|E_eta|>=0",
            "full_monic_gcd": "H=gcd(P,Q)",
            "reduced_pair": "P=H*Pbar, Q=H*Qbar, gcd(Pbar,Qbar)=1",
            "reduced_degree": "e=max(deg(Pbar),deg(Qbar))",
            "source_coupling": [
                "a=epsilon_0-ev(P)",
                "b=epsilon_1-ev(Q)",
            ],
            "source_zero_on_W": True,
            "forced_outside_locator": "L_C divides H, c=|C|=A-x-s",
            "degree_contract": "deg(H)+e<=k-1",
            "post_owner_survivor": "e>=ceil(s/2)",
            "complete_selector_inventory_required": False,
        },
        "moving_root_cofactor": {
            "moving_set": "F_eta={z in W:a(z)+eta*b(z)=0}",
            "whole_set_cardinality": "|F_eta|=x+delta_eta",
            "single_chosen_root_is_insufficient": True,
            "F_eta_subset_W_subset_V_subset_D_minus_Sigma": True,
            "source_vanishes_on_F_eta": True,
            "P_plus_eta_Q_vanishes_on_F_eta": True,
            "H_nonzero_on_F_eta": True,
            "common_root_in_W_forbidden": True,
            "reduced_combination_nonzero": True,
            "locator_divisibility": "L_F_eta divides Pbar+eta*Qbar",
            "cofactor": "Pbar+eta*Qbar=L_F_eta*A_eta",
            "cofactor_degree_bound": "deg(A_eta)<=e-x-delta_eta",
            "moving_degree_inequality": "x+delta_eta<=e",
        },
        "slack_normal_form": {
            "definitions": {
                "r": "s-t-1",
                "h": "deg(H)-c",
                "u": "e-x",
                "ell": "k-1-deg(H)-e",
            },
            "nonnegative": ["r", "h", "u", "ell"],
            "identity": "h+u+ell=r",
            "deficit_bound": "0<=delta_eta<=u",
            "source_bound_each_selected_slope": "s>=t+delta_eta+1",
            "zero_slack_source": ZERO_SLACK_SOURCE,
            "predecessor_nominal_boundary_empty": True,
            "exact_small_slack_profiles_checked": 120,
            "atlas_word_u_not_reused_in_proof_note_without_warning": True,
        },
        "c5_boundary_absorption": {
            "boundary_source_size": ZERO_SLACK_SOURCE,
            "forced_slacks": [0, 0, 0],
            "all_deficits_zero": True,
            "forced_equalities": ["e=x", "deg(H)=c", "H=L_C"],
            "H_is_base_locator": True,
            "moving_members": "Pbar+eta*Qbar=kappa_eta*L_F_eta",
            "two_distinct_slopes_from_same_line": True,
            "two_slope_matrix_invertible": True,
            "base_words": "1_Sigma*L_C*L_F_eta_i in B^D",
            "translated_pair_GL2_equivalent_to_base_pair": True,
            "restored_codewords_are_syndrome_gauge": True,
            "rank_zero_noncontained_residual_empty": True,
            "positive_rank_intrinsic_projective_field": "B=F_p",
            "existing_owner": C5_OWNER_ID,
            "existing_owner_witness_exhaustive": True,
            "later_boundary_record_impossible": True,
            "paid_terminal": PAID_ZERO_SLACK_TERMINAL,
        },
        "revised_residual": {
            "old_terminal": PREDECESSOR_TERMINAL,
            "new_terminal": NEW_TERMINAL,
            "survivor_source_floor": RESIDUAL_SOURCE_FLOOR,
            "survivor_reduced_degree_floor": RESIDUAL_DEGREE_FLOOR,
            "survivor_full_gcd_degree_ceiling": RESIDUAL_GCD_CEILING,
            "closed_full_gcd_degree_floor": CLOSED_GCD_FLOOR,
            "closed_full_gcd_degree_ceiling": CLOSED_GCD_CEILING,
            "closed_full_gcd_degree_count_total": CLOSED_GCD_COUNT,
            "predecessor_closed_full_gcd_degree_count": OLD_CLOSED_GCD_COUNT,
            "additional_closed_full_gcd_degree_count": ADDITIONAL_CLOSED_GCD_COUNT,
            "source_sizes_at_most_67472_empty": True,
            "source_size_67473_C5_owned": True,
            "source_size_67474_or_more_paid": False,
        },
        "one_slack_frontier": {
            "source_size": RESIDUAL_SOURCE_FLOOR,
            "r": 1,
            "triples_h_u_ell": nonnegative_triples(1),
            "degree_slack_cell": {
                "triple": [0, 0, 1],
                "C5_owned": True,
                "paid_terminal": PAID_ONE_SLACK_TERMINAL,
            },
            "common_factor_cell": {
                "triple": [1, 0, 0],
                "reduced_pencil_base_defined": True,
                "H_over_L_C_monic_degree": 1,
                "base_linear_factor_C5_owned": True,
                "primitive_requires_nonbase_linear_factor": True,
                "terminal": GCD_TWIST_TERMINAL,
            },
            "moving_cofactor_cell": {
                "triple": [0, 1, 0],
                "H_equals_base_locator": True,
                "delta_values": [0, 1],
                "cofactor_degree_bound": "deg(A_eta)<=1-delta_eta",
                "two_projectively_base_members_force_C5": True,
                "two_delta_one_members_force_C5": True,
                "primitive_delta_one_count_at_most": 1,
                "primitive_delta_zero_count_at_least": 20,
                "terminal": MOVING_COFACTOR_TERMINAL,
            },
            "generic_elimination_authorized": False,
        },
        "first_match_partition": {
            "order": FIRST_MATCH_ORDER,
            "C5_index_one_based": FIRST_MATCH_ORDER.index(C5_OWNER_ID) + 1,
            "source_rational_index_one_based": FIRST_MATCH_ORDER.index(SOURCE_RATIONAL_OWNER_ID) + 1,
            "C5_precedes_source_rational": FIRST_MATCH_ORDER.index(C5_OWNER_ID) < FIRST_MATCH_ORDER.index(SOURCE_RATIONAL_OWNER_ID),
            "no_owner_inserted": True,
            "boundary_absorbed_by_earlier_owner": True,
            "selector_restart_retains_fixed_source_data": True,
            "stale_selector_data_reused": False,
        },
        "exact_control": {
            "scale": "EXACT_TOY_CONTROL_NOT_DEPLOYED_SELECTOR_OR_PROOF",
            "field_order": 121,
            "base_field_order": 11,
            "zero_slack": {
                "t": 2,
                "s": 3,
                "x": 2,
                "e": 2,
                "c": 2,
                "deg_H": 2,
                "slacks": [0, 0, 0],
                "moving_set_sizes": [2, 2],
                "translated_pair_base_rank": 2,
                "C5_coordinate_recovery": True,
            },
            "one_slack_triples": [[0, 0, 1], [0, 1, 0], [1, 0, 0]],
            "nonbase_gcd_twist": True,
            "nonbase_linear_moving_cofactors": 2,
            "mutation_count": 10,
            "mutation_rejections": 10,
            "toy_only": True,
            "normal_optimized_transcript_parity_required": True,
            "generated_sage_python_is_temporary_build_product": True,
            "fail_closed_explicit_checks": True,
        },
        "ledger": {
            "replacement_or_new_owner": "NEITHER_ROUTE_CUT_ONLY",
            "existing_C5_charge_reused": True,
            "incremental_ledger_movement": str(LEDGER_MOVEMENT),
            "U_paid_before": str(U_PAID_BEFORE),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "U_Q": None,
            "balanced_core_or_sparse_residual": None,
            "complete_profile_envelope_status": "OPEN",
        },
        "residual_route_cuts": [
            {
                "terminal": NEW_TERMINAL,
                "status": "UNPAID",
                "reason": "post-C5 survivor has s>=67474, e>=33737, deg(H)<=1014838",
            },
            {
                "terminal": GCD_TWIST_TERMINAL,
                "status": "UNPAID_ONE_SLACK_COMPONENT",
                "reason": "one genuinely nonbase common linear factor remains",
            },
            {
                "terminal": MOVING_COFACTOR_TERMINAL,
                "status": "UNPAID_ONE_SLACK_COMPONENT",
                "reason": "at least twenty potentially nonbase linear moving cofactors remain",
            },
            {
                "terminal": SOURCE_LOAD_TERMINAL,
                "status": "UNPAID_DISJOINT_NON_FULL_OUTSIDE_SCOPE",
                "reason": "whole-moving-set proof used V disjoint from Sigma",
            },
        ],
        "scope_guards": {
            "moving_root_cofactor_lemma_proved": True,
            "slack_normal_form_proved": True,
            "zero_slack_C5_absorption_proved": True,
            "one_slack_degree_cell_C5_absorbed": True,
            "all_one_slack_cells_paid": False,
            "deployed_complete_selector_constructed": False,
            "complete_selector_inventory_required_for_uniform_implication": False,
            "non_full_outside_source_load_paid": False,
            "determinant_weighted_incidence_paid": False,
            "U_Q_determined": False,
            "complete_profile_envelope_compared": False,
            "complete_rank9_payment_proved": False,
            "koalabear_row_closed": False,
            "rank_at_least_ten_authorized": False,
            "lean_authorized": False,
            "stable_paper_promotion_authorized": False,
        },
        "nonclaims": [
            "No deployed complete selector or terminal census is constructed.",
            "No one-root bridge is substituted for the whole moving-zero identity.",
            "No non-full-outside or coefficient-rank-one record is paid.",
            "No determinant, support, line, basis, or witness multiplicity is counted.",
            "No nonbase linear component is forced into C5.",
            "No claim is made that either one-slack primitive component is nonempty.",
            "No new owner or ledger charge is added.",
            "No toy control is promoted to deployed-field evidence.",
            "No value is assigned to U_Q or the balanced-core/sparse residual.",
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
        ("row-t", lambda d: d["row"].__setitem__("syndrome_depth_t", T - 1)),
        ("row-k", lambda d: d["row"].__setitem__("k", K - 1)),
        ("predecessor-source", lambda d: d["predecessors"].__setitem__("source_rational_owner", "payload-sha256:" + "0" * 64)),
        ("predecessor-rich", lambda d: d["predecessors"].__setitem__("rich_pencil_atlas", "payload-sha256:" + "0" * 64)),
        ("predecessor-c5", lambda d: d["predecessors"].__setitem__("projective_base_pair_C5_owner", "payload-sha256:" + "0" * 64)),
        ("new-owner", lambda d: d["counted_object_contract"].__setitem__("new_owner_added", True)),
        ("new-charge", lambda d: d["counted_object_contract"].__setitem__("new_slope_set_charged", True)),
        ("per-selector", lambda d: d["counted_object_contract"].__setitem__("per_selector_charge_forbidden", False)),
        ("infinity", lambda d: d["counted_object_contract"].__setitem__("projective_infinity_counted_as_finite", True)),
        ("not-full-outside", lambda d: d["inherited_record_contract"].__setitem__("full_outside", "V INTERSECT Sigma nonempty")),
        ("rank-one", lambda d: d["inherited_record_contract"].__setitem__("coefficient_rank", 1)),
        ("beta-zero", lambda d: d["inherited_record_contract"].__setitem__("beta_positive", False)),
        ("J-twenty", lambda d: d["inherited_record_contract"].__setitem__("J_at_least", 20)),
        ("infinity-slope", lambda d: d["inherited_record_contract"].__setitem__("selected_slopes_finite", False)),
        ("negative-deficit", lambda d: d["inherited_record_contract"].__setitem__("low_deficit", "delta_eta<0")),
        ("forced-gcd", lambda d: d["inherited_record_contract"].__setitem__("full_monic_gcd", "H=L_C")),
        ("not-coprime", lambda d: d["inherited_record_contract"].__setitem__("reduced_pair", "gcd(Pbar,Qbar)!=1")),
        ("source-on-W", lambda d: d["inherited_record_contract"].__setitem__("source_zero_on_W", False)),
        ("inventory-required", lambda d: d["inherited_record_contract"].__setitem__("complete_selector_inventory_required", True)),
        ("one-root", lambda d: d["moving_root_cofactor"].__setitem__("whole_set_cardinality", "F_eta nonempty")),
        ("one-root-sufficient", lambda d: d["moving_root_cofactor"].__setitem__("single_chosen_root_is_insufficient", False)),
        ("F-not-W", lambda d: d["moving_root_cofactor"].__setitem__("F_eta_subset_W_subset_V_subset_D_minus_Sigma", False)),
        ("source-nonzero-F", lambda d: d["moving_root_cofactor"].__setitem__("source_vanishes_on_F_eta", False)),
        ("P-not-zero-F", lambda d: d["moving_root_cofactor"].__setitem__("P_plus_eta_Q_vanishes_on_F_eta", False)),
        ("H-zero-F", lambda d: d["moving_root_cofactor"].__setitem__("H_nonzero_on_F_eta", False)),
        ("common-in-W", lambda d: d["moving_root_cofactor"].__setitem__("common_root_in_W_forbidden", False)),
        ("zero-combination", lambda d: d["moving_root_cofactor"].__setitem__("reduced_combination_nonzero", False)),
        ("no-divisibility", lambda d: d["moving_root_cofactor"].__setitem__("locator_divisibility", "one root only")),
        ("cofactor-degree", lambda d: d["moving_root_cofactor"].__setitem__("cofactor_degree_bound", "deg(A_eta)<=e-x")),
        ("moving-inequality", lambda d: d["moving_root_cofactor"].__setitem__("moving_degree_inequality", "x<=e")),
        ("slack-r", lambda d: d["slack_normal_form"]["definitions"].__setitem__("r", "s-t")),
        ("slack-h", lambda d: d["slack_normal_form"]["definitions"].__setitem__("h", "deg(H)")),
        ("slack-u", lambda d: d["slack_normal_form"]["definitions"].__setitem__("u", "e")),
        ("slack-ell", lambda d: d["slack_normal_form"]["definitions"].__setitem__("ell", "k-deg(H)-e")),
        ("slack-negative", lambda d: d["slack_normal_form"].__setitem__("nonnegative", ["r"])),
        ("slack-sum", lambda d: d["slack_normal_form"].__setitem__("identity", "h+u+ell<=r")),
        ("deficit-u", lambda d: d["slack_normal_form"].__setitem__("deficit_bound", "delta_eta<=e")),
        ("source-bound", lambda d: d["slack_normal_form"].__setitem__("source_bound_each_selected_slope", "s>=t+1")),
        ("zero-source", lambda d: d["slack_normal_form"].__setitem__("zero_slack_source", ZERO_SLACK_SOURCE - 1)),
        ("nominal-nonempty", lambda d: d["slack_normal_form"].__setitem__("predecessor_nominal_boundary_empty", False)),
        ("boundary-source", lambda d: d["c5_boundary_absorption"].__setitem__("boundary_source_size", ZERO_SLACK_SOURCE + 1)),
        ("boundary-slacks", lambda d: d["c5_boundary_absorption"].__setitem__("forced_slacks", [0, 0, 1])),
        ("boundary-deficit", lambda d: d["c5_boundary_absorption"].__setitem__("all_deficits_zero", False)),
        ("boundary-H", lambda d: d["c5_boundary_absorption"].__setitem__("H_is_base_locator", False)),
        ("one-slope", lambda d: d["c5_boundary_absorption"].__setitem__("two_distinct_slopes_from_same_line", False)),
        ("singular-matrix", lambda d: d["c5_boundary_absorption"].__setitem__("two_slope_matrix_invertible", False)),
        ("nonbase-words", lambda d: d["c5_boundary_absorption"].__setitem__("base_words", "words in F^D")),
        ("no-GL2", lambda d: d["c5_boundary_absorption"].__setitem__("translated_pair_GL2_equivalent_to_base_pair", False)),
        ("not-gauge", lambda d: d["c5_boundary_absorption"].__setitem__("restored_codewords_are_syndrome_gauge", False)),
        ("rank-zero-live", lambda d: d["c5_boundary_absorption"].__setitem__("rank_zero_noncontained_residual_empty", False)),
        ("field-full", lambda d: d["c5_boundary_absorption"].__setitem__("positive_rank_intrinsic_projective_field", "F")),
        ("wrong-owner", lambda d: d["c5_boundary_absorption"].__setitem__("existing_owner", "residual_base_slope_universe")),
        ("not-exhaustive", lambda d: d["c5_boundary_absorption"].__setitem__("existing_owner_witness_exhaustive", False)),
        ("boundary-survives", lambda d: d["c5_boundary_absorption"].__setitem__("later_boundary_record_impossible", False)),
        ("residual-source", lambda d: d["revised_residual"].__setitem__("survivor_source_floor", RESIDUAL_SOURCE_FLOOR - 1)),
        ("residual-degree", lambda d: d["revised_residual"].__setitem__("survivor_reduced_degree_floor", RESIDUAL_DEGREE_FLOOR - 1)),
        ("residual-gcd", lambda d: d["revised_residual"].__setitem__("survivor_full_gcd_degree_ceiling", RESIDUAL_GCD_CEILING + 1)),
        ("closed-count", lambda d: d["revised_residual"].__setitem__("closed_full_gcd_degree_count_total", CLOSED_GCD_COUNT - 1)),
        ("additional-count", lambda d: d["revised_residual"].__setitem__("additional_closed_full_gcd_degree_count", ADDITIONAL_CLOSED_GCD_COUNT - 1)),
        ("new-terminal-paid", lambda d: d["revised_residual"].__setitem__("source_size_67474_or_more_paid", True)),
        ("triples", lambda d: d["one_slack_frontier"].__setitem__("triples_h_u_ell", [[1, 0, 0]])),
        ("degree-cell-unpaid", lambda d: d["one_slack_frontier"]["degree_slack_cell"].__setitem__("C5_owned", False)),
        ("base-factor-unpaid", lambda d: d["one_slack_frontier"]["common_factor_cell"].__setitem__("base_linear_factor_C5_owned", False)),
        ("twist-base", lambda d: d["one_slack_frontier"]["common_factor_cell"].__setitem__("primitive_requires_nonbase_linear_factor", False)),
        ("cofactor-delta", lambda d: d["one_slack_frontier"]["moving_cofactor_cell"].__setitem__("delta_values", [0, 1, 2])),
        ("two-delta-live", lambda d: d["one_slack_frontier"]["moving_cofactor_cell"].__setitem__("two_delta_one_members_force_C5", False)),
        ("delta-one-count", lambda d: d["one_slack_frontier"]["moving_cofactor_cell"].__setitem__("primitive_delta_one_count_at_most", 2)),
        ("delta-zero-count", lambda d: d["one_slack_frontier"]["moving_cofactor_cell"].__setitem__("primitive_delta_zero_count_at_least", 19)),
        ("generic-elimination", lambda d: d["one_slack_frontier"].__setitem__("generic_elimination_authorized", True)),
        ("owner-order", lambda d: d["first_match_partition"]["order"].reverse()),
        ("C5-index", lambda d: d["first_match_partition"].__setitem__("C5_index_one_based", 7)),
        ("C5-after", lambda d: d["first_match_partition"].__setitem__("C5_precedes_source_rational", False)),
        ("insert-owner", lambda d: d["first_match_partition"].__setitem__("no_owner_inserted", False)),
        ("stale-selector", lambda d: d["first_match_partition"].__setitem__("stale_selector_data_reused", True)),
        ("toy-deployed", lambda d: d["exact_control"].__setitem__("scale", "DEPLOYED_PROOF")),
        ("toy-field", lambda d: d["exact_control"].__setitem__("field_order", 11)),
        ("toy-C5", lambda d: d["exact_control"]["zero_slack"].__setitem__("C5_coordinate_recovery", False)),
        ("toy-mutations", lambda d: d["exact_control"].__setitem__("mutation_rejections", 9)),
        ("ledger-new-owner", lambda d: d["ledger"].__setitem__("replacement_or_new_owner", "NEW_OWNER")),
        ("ledger-C5-new", lambda d: d["ledger"].__setitem__("existing_C5_charge_reused", False)),
        ("ledger-movement", lambda d: d["ledger"].__setitem__("incremental_ledger_movement", "1")),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("B-remaining", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_AFTER - 1))),
        ("UQ-zero", lambda d: d["ledger"].__setitem__("U_Q", 0)),
        ("route-paid", lambda d: d["residual_route_cuts"][0].__setitem__("status", "PAID")),
        ("all-r1-paid", lambda d: d["scope_guards"].__setitem__("all_one_slack_cells_paid", True)),
        ("invent-selector", lambda d: d["scope_guards"].__setitem__("deployed_complete_selector_constructed", True)),
        ("non-full-paid", lambda d: d["scope_guards"].__setitem__("non_full_outside_source_load_paid", True)),
        ("rank9-closed", lambda d: d["scope_guards"].__setitem__("complete_rank9_payment_proved", True)),
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
        except (ContractError, KeyError, IndexError, TypeError, ValueError):
            rejected += 1
        else:
            raise ContractError(f"certificate mutation survived: {name}")
    parser_rejected = run_parser_tamper_selftest()
    total = rejected + parser_rejected
    require(rejected == len(mutation_cases()), "semantic mutation count drift")
    print(f"M1 moving-root slack/C5 mutations: {total}/{total} PASS")
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
    print("M1 moving-root cofactor/slack and C5 boundary: PASS")
    print("  whole moving set: L_F_eta | Pbar+eta*Qbar; x+delta_eta<=e")
    print("  slack identity: h+u+ell=s-t-1; delta_eta<=u")
    print(f"  C5-owned zero-slack source size: {ZERO_SLACK_SOURCE:,}")
    print(
        "  survivor: "
        f"s>={RESIDUAL_SOURCE_FLOOR:,}, e>={RESIDUAL_DEGREE_FLOOR:,}, "
        f"deg(H)<={RESIDUAL_GCD_CEILING:,}"
    )
    print(
        "  closed gcd degrees: "
        f"{CLOSED_GCD_COUNT:,} total; {ADDITIONAL_CLOSED_GCD_COUNT:,} additional"
    )
    print(f"  incremental ledger movement: {LEDGER_MOVEMENT}")
    print(f"  route cut: {NEW_TERMINAL}")
    print(f"  one-slack residuals: {GCD_TWIST_TERMINAL}; {MOVING_COFACTOR_TERMINAL}")
    print("  non-full-outside/U_Q/profile envelope remain open; row YELLOW")
    return 0


def sage_transcript_lines(output: str) -> str:
    prefixes = (
        "MOVING_ROOT_SLACK_C5_CONTROL=",
        "MOVING_ROOT_SLACK_C5_MUTATIONS=",
        "SCALE=",
    )
    lines = [line for line in output.splitlines() if line.startswith(prefixes)]
    require(len(lines) == 3, "Sage replay did not emit exactly three control lines")
    return "\n".join(lines) + "\n"


def expected_sage_transcript(document: dict[str, Any]) -> str:
    exact = copy.deepcopy(document["exact_control"])
    exact.pop("normal_optimized_transcript_parity_required")
    exact.pop("generated_sage_python_is_temporary_build_product")
    exact.pop("fail_closed_explicit_checks")
    mutation_result = {
        "base_descent": True,
        "cofactor_degree": True,
        "common_root_in_W": True,
        "deficit_bound": True,
        "distinct_slopes": True,
        "full_gcd": True,
        "nonbase_gcd_twist": True,
        "nonbase_moving_cofactor": True,
        "slack_identity": True,
        "source_on_W": True,
    }
    return (
        "MOVING_ROOT_SLACK_C5_CONTROL="
        + json.dumps(exact, sort_keys=True, separators=(",", ":"))
        + "\nMOVING_ROOT_SLACK_C5_MUTATIONS="
        + json.dumps(mutation_result, sort_keys=True, separators=(",", ":"))
        + "\nSCALE="
        + document["exact_control"]["scale"]
        + "\n"
    )


def run_sage_parity_check() -> int:
    document = load_json(CERT_PATH)
    validate_certificate(document)
    expected = expected_sage_transcript(document)
    sage_executable = Path("/usr/local/bin/sage")
    require(sage_executable.is_file(), f"missing Sage executable: {sage_executable}")

    with tempfile.TemporaryDirectory(prefix="rs-mca-moving-root-slack-sage-") as tmp:
        temporary_sage = Path(tmp) / SAGE_REL.name
        shutil.copyfile(ROOT / SAGE_REL, temporary_sage)
        env = dict(os.environ)
        env["HOME"] = str(Path(tmp) / "home")
        Path(env["HOME"]).mkdir()

        normal = subprocess.run(
            [str(sage_executable), str(temporary_sage)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        require(normal.returncode == 0, "ordinary Sage replay failed: " + normal.stderr)

        generated_python = temporary_sage.with_name(temporary_sage.name + ".py")
        require(generated_python.is_file(), "Sage did not emit temporary Python product")
        optimized = subprocess.run(
            [str(sage_executable), "-python", "-O", str(generated_python)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        require(optimized.returncode == 0, "optimized Sage replay failed: " + optimized.stderr)

        normal_transcript = sage_transcript_lines(normal.stdout)
        optimized_transcript = sage_transcript_lines(optimized.stdout)
        require(normal_transcript == expected, "ordinary Sage transcript drift")
        require(optimized_transcript == expected, "optimized Sage transcript drift")
        require(normal_transcript == optimized_transcript, "Sage mode transcript mismatch")

    print("M1 moving-root slack/C5 Sage parity: PASS (ordinary == optimized)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--sage-parity-check", action="store_true")
    group.add_argument("--print-certificate", action="store_true")
    group.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return run_tamper_selftest()
    if args.sage_parity_check:
        return run_sage_parity_check()
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
