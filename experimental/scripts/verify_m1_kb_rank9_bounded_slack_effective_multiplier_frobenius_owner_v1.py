#!/usr/bin/env python3
"""Verify the ledger-maximal bounded-slack source-Frobenius owner.

The local algebra works through effective-multiplier degree 9208.  The
inherited rank-nine one-cut plus aggregate-excess ledger remains meaningful
only through degree 195.  This certificate therefore replaces the prior
four-anchor owner by one degree-195 owner, closes every full-outside slack
layer 1 <= r <= 195, and records degree 196 as the exact accounting route
cut.  It does not close rank nine or KoalaBear.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Callable

import verify_m1_kb_rank9_one_slack_moving_cofactor_frobenius_owner_v1 as predecessor


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "rs-mca-m1-kb-rank9-bounded-slack-effective-multiplier-frobenius-owner-v1"
ARTIFACT_KIND = "M1_KB_RANK9_BOUNDED_SLACK_EFFECTIVE_MULTIPLIER_FROBENIUS_OWNER"
STATUS = (
    "PROVED_LOCAL_R1_TO_R195_CLOSED_EXACT_R196_LEDGER_ROUTE_CUT_"
    "INDEPENDENT_PROOF_AND_ARTIFACT_REVIEWS_GREEN_ROW_OPEN"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-rank9-bounded-slack-effective-multiplier-frobenius-owner-v1"
)
CERT_PATH = (
    CERT_DIR
    / "m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.json"
)
NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-rank9-bounded-slack-effective-multiplier-frobenius-owner-v1/README.md"
)
SCRIPT_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/"
    "verify_m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.sage"
)
MOVING_ROOT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_moving_root_slack_c5_boundary_v1.md"
)
MOVING_ROOT_SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_moving_root_slack_c5_boundary_v1.sage"
)
SOURCE_RATIONAL_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_source_rational_owner_splice_v1.md"
)
TANGENT_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_rank9_tangent_owner_splice_v1.md"
)
TANGENT_SCRIPT_REL = Path(
    "experimental/scripts/verify_m1_kb_rank9_tangent_owner_splice_v1.py"
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
B_STAR = predecessor.B_STAR

REPLACED_OWNER_ID = predecessor.MOVING_OWNER_ID
REPLACED_OWNER_CAP = predecessor.OWNER_CAP
OWNER_ID = "source_frobenius_effective_multiplier_degree_at_most_195"
PAID_TERMINAL = (
    "PAID_PAIR_GLOBAL_SOURCE_FROBENIUS_"
    "EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_195"
)
REPLACED_OPEN_TERMINAL = predecessor.OPEN_TERMINAL
OPEN_TERMINAL = "UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67669"

DEPLOYED_M = 195
FIRST_UNPAID_M = 196
ALGEBRAIC_MAX_M = 9_208
FIRST_ALGEBRAIC_FAILURE_M = ALGEBRAIC_MAX_M + 1
ANCHOR_SIZE = 2 * (DEPLOYED_M + 1)
CROSS_MULTIPLIER_DEGREE = 2 * DEPLOYED_M
SUPPORT_FLOOR = T + 1 - RICH_X_MAX
UNIFORM_REDUCED_DEGREE_FLOOR = (T + 2 + 1) // 2
EXPONENT_COUNT = (DEPLOYED_M + 2) ** 2

OWNER_CAP = (DEPLOYED_M + 1) * (P + 1)
LEDGER_MOVEMENT = OWNER_CAP - REPLACED_OWNER_CAP
U_PAID_BEFORE = predecessor.U_PAID_AFTER
B_REMAINING_BEFORE = predecessor.B_REMAINING_AFTER
U_PAID_AFTER = U_PAID_BEFORE + LEDGER_MOVEMENT
B_REMAINING_AFTER = B_STAR - U_PAID_AFTER

NEXT_SOURCE_SIZE = T + FIRST_UNPAID_M + 1
NEXT_REDUCED_DEGREE_MIN = (NEXT_SOURCE_SIZE + 1) // 2
NEXT_FULL_GCD_MAX = K - 1 - NEXT_REDUCED_DEGREE_MIN

EXPECTED_TAIL_TARGET = 17_413_395_125_116
EXPECTED_E_MAX = int(
    "17249952857855762969687793243974375796302274"
)
EXPECTED_K_REMAINING = 4_807_513
EXPECTED_BREAK_J = 21

M196_OWNER_CAP = 419_749_167_498
M196_U_PAID = 424_485_436_766
M196_B_REMAINING = 274_980_303_625_958_321
M196_TAIL_TARGET = 17_410_886_628_770
M196_E_MAX = -int(
    "9487087327483531737221376676045581877928676"
)

LAST_ONE_CUT_DEFINED_M = 7_136
FIRST_ONE_CUT_UNDEFINED_M = 7_137

PROFILE_COUNT = math.comb(DEPLOYED_M + 3, 3) - 1
DEFICIT_SHAPE_COUNT = math.comb(DEPLOYED_M + 4, 4) - 1
BOUNDARY_PROFILE_COUNT = math.comb(DEPLOYED_M + 2, 2)

FIRST_MATCH_ORDER = list(predecessor.FIRST_MATCH_ORDER)
owner_index = FIRST_MATCH_ORDER.index(REPLACED_OWNER_ID)
FIRST_MATCH_ORDER[owner_index] = OWNER_ID

TANGENT = predecessor.predecessor.ledger_base.tangent

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "row",
    "predecessor",
    "owner_replacement",
    "slack_profile_compiler",
    "effective_multiplier",
    "source_frobenius_eliminant",
    "nonvanishing_lemma",
    "pair_global_owner",
    "first_match_partition",
    "selector_restart",
    "exact_control",
    "ledger",
    "ledger_maximality",
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
    predecessor_cert_rel = predecessor.CERT_PATH.relative_to(ROOT)
    return [
        source_binding("proof-note", NOTE_REL, "bounded-slack theorem and route cut"),
        source_binding("python-verifier", SCRIPT_REL, "certificate, optimizer, mutations"),
        source_binding("sage-control", SAGE_REL, "exact specialization and guardrails"),
        source_binding("readme", README_REL, "replay and scope contract"),
        source_binding(
            "one-slack-predecessor-note",
            predecessor.NOTE_REL,
            "replaced four-anchor owner",
        ),
        source_binding(
            "one-slack-predecessor-verifier",
            predecessor.SCRIPT_REL,
            "predecessor owner and banked ledger",
        ),
        source_binding(
            "one-slack-predecessor-certificate",
            predecessor_cert_rel,
            "predecessor payload and source bindings",
        ),
        source_binding(
            "moving-root-slack-note",
            MOVING_ROOT_NOTE_REL,
            "slack simplex and moving-root divisibility",
        ),
        source_binding(
            "moving-root-slack-sage",
            MOVING_ROOT_SAGE_REL,
            "exact slack-interface controls",
        ),
        source_binding(
            "source-rational-note",
            SOURCE_RATIONAL_NOTE_REL,
            "post-restart reduced-degree floor",
        ),
        source_binding(
            "tangent-ledger-note",
            TANGENT_NOTE_REL,
            "one-cut and aggregate-excess semantics",
        ),
        source_binding(
            "tangent-ledger-verifier",
            TANGENT_SCRIPT_REL,
            "exact one-cut and aggregate-excess arithmetic",
        ),
    ]


def validate_predecessor() -> dict[str, Any]:
    document = predecessor.load_json(predecessor.CERT_PATH)
    predecessor.validate_certificate(document)
    require(
        document["payload_sha256"]
        == "6c2bf4a322177f04223356f67b8476a2aa730a777bd3e95930f49173c3cadc8e",
        "predecessor payload drift",
    )
    require(
        document["pair_global_owner"]["owner_id"] == REPLACED_OWNER_ID,
        "replaced owner id drift",
    )
    require(
        int(document["ledger"]["new_owner_cap"]) == REPLACED_OWNER_CAP,
        "replaced owner cap drift",
    )
    require(
        int(document["ledger"]["U_paid_after"]) == U_PAID_BEFORE,
        "predecessor U_paid drift",
    )
    require(
        int(document["ledger"]["B_remaining_after"]) == B_REMAINING_BEFORE,
        "predecessor remaining budget drift",
    )
    return document


def compile_slack_profiles() -> tuple[list[dict[str, int]], int, int]:
    """Exhaust the (h,u,ell) simplex without serializing 1.27M triples."""
    summaries: list[dict[str, int]] = []
    profile_total = 0
    deficit_shape_total = 0
    for r in range(1, DEPLOYED_M + 1):
        profile_count = 0
        deficit_shape_count = 0
        effective_max = -1
        for h in range(r + 1):
            for u in range(r - h + 1):
                ell = r - h - u
                require(h >= 0 and u >= 0 and ell >= 0, "negative slack coordinate")
                require(h + u + ell == r, "slack simplex drift")
                profile_count += 1
                deficit_shape_count += u + 1
                effective_max = max(effective_max, h + u)
                require(h + u == r - ell <= r, "effective degree bound drift")
                require(
                    h + u - 0 <= r and h + u - u == h >= 0,
                    "deficit endpoint drift",
                )
        expected_profiles = math.comb(r + 2, 2)
        expected_deficit_shapes = math.comb(r + 3, 3)
        require(profile_count == expected_profiles, "profile count drift")
        require(
            deficit_shape_count == expected_deficit_shapes,
            "deficit-shape count drift",
        )
        require(effective_max == r, "profile maximum drift")
        source_size = T + r + 1
        e_min = (source_size + 1) // 2
        e_max = RICH_X_MAX + r
        support_floor = source_size - e_max
        require(support_floor == SUPPORT_FLOOR, "support floor drift")
        summaries.append(
            {
                "r": r,
                "source_size": source_size,
                "profile_count": profile_count,
                "deficit_shape_count": expected_deficit_shapes,
                "effective_multiplier_degree_max": effective_max,
                "reduced_degree_min": e_min,
                "reduced_degree_max": e_max,
                "source_combination_support_min": support_floor,
            }
        )
        profile_total += profile_count
        deficit_shape_total += deficit_shape_count
    require(profile_total == PROFILE_COUNT, "cumulative profile count drift")
    require(
        deficit_shape_total == DEFICIT_SHAPE_COUNT,
        "cumulative deficit-shape count drift",
    )
    return summaries, profile_total, deficit_shape_total


def candidate_ledger(m: int) -> dict[str, Any]:
    require(1 <= m <= ALGEBRAIC_MAX_M, "candidate m outside algebraic scan")
    cap = (m + 1) * (P + 1)
    increment = cap - REPLACED_OWNER_CAP
    u_paid = U_PAID_BEFORE + increment
    remaining = B_STAR - u_paid
    result: dict[str, Any] = {
        "m": m,
        "owner_cap": cap,
        "incremental_movement": increment,
        "U_paid": u_paid,
        "B_remaining": remaining,
        "one_cut_defined": False,
        "one_cut_error": None,
        "tail_target": None,
        "aggregate_excess_max": None,
        "aggregate_excess_nonnegative": False,
        "bankable_under_inherited_gate": False,
    }
    try:
        gate = TANGENT.one_cut_gate(remaining, CUTOFF_D, N, 1)
    except TANGENT.VerificationError as exc:
        result["one_cut_error"] = str(exc)
        return result
    tail = int(gate["largest_sufficient_low_deficit_cap_T_star"])
    e_max = TANGENT.aggregate_excess_max(tail)
    result.update(
        {
            "one_cut_defined": True,
            "tail_target": tail,
            "aggregate_excess_max": e_max,
            "aggregate_excess_nonnegative": e_max >= 0,
            "bankable_under_inherited_gate": e_max >= 0,
            "gate": gate,
        }
    )
    return result


_OPTIMIZER_CACHE: dict[str, Any] | None = None


def exact_optimizer() -> dict[str, Any]:
    global _OPTIMIZER_CACHE
    if _OPTIMIZER_CACHE is not None:
        return copy.deepcopy(_OPTIMIZER_CACHE)

    digest = hashlib.sha256()
    bankable: list[int] = []
    gate_defined: list[int] = []
    first_negative: int | None = None
    previous_tail: int | None = None
    previous_e: int | None = None
    for m in range(1, ALGEBRAIC_MAX_M + 1):
        row = candidate_ledger(m)
        if row["one_cut_defined"]:
            gate_defined.append(m)
            tail = int(row["tail_target"])
            e_max = int(row["aggregate_excess_max"])
            if previous_tail is not None:
                require(tail <= previous_tail, "tail target is not monotone")
                require(e_max <= previous_e, "aggregate excess is not monotone")
            previous_tail = tail
            previous_e = e_max
            if e_max < 0 and first_negative is None:
                first_negative = m
        if row["bankable_under_inherited_gate"]:
            bankable.append(m)
        digest.update(
            canonical_bytes(
                [
                    m,
                    row["owner_cap"],
                    row["B_remaining"],
                    row["one_cut_defined"],
                    row["one_cut_error"],
                    row["tail_target"],
                    row["aggregate_excess_max"],
                    row["bankable_under_inherited_gate"],
                ]
            )
        )

    require(bankable == list(range(1, DEPLOYED_M + 1)), "bankable prefix drift")
    require(first_negative == FIRST_UNPAID_M, "first negative aggregate drift")
    require(
        gate_defined == list(range(1, LAST_ONE_CUT_DEFINED_M + 1)),
        "one-cut defined interval drift",
    )
    result = {
        "scan_min_m": 1,
        "scan_max_m": ALGEBRAIC_MAX_M,
        "scan_count": ALGEBRAIC_MAX_M,
        "scan_sha256": digest.hexdigest(),
        "bankable_prefix_min_m": 1,
        "bankable_prefix_max_m": DEPLOYED_M,
        "first_nonbankable_m": FIRST_UNPAID_M,
        "first_negative_aggregate_excess_m": first_negative,
        "last_one_cut_defined_m": max(gate_defined),
        "first_one_cut_undefined_m": max(gate_defined) + 1,
        "monotonicity": (
            "owner cap and U_paid increase; B_remaining, T_star, and Emax "
            "do not increase while the one-cut gate is defined"
        ),
    }
    _OPTIMIZER_CACHE = copy.deepcopy(result)
    return result


def exact_rank9_update() -> dict[str, Any]:
    row = candidate_ledger(DEPLOYED_M)
    require(row["owner_cap"] == OWNER_CAP, "deployed owner cap drift")
    require(row["U_paid"] == U_PAID_AFTER, "deployed U_paid drift")
    require(row["B_remaining"] == B_REMAINING_AFTER, "deployed budget drift")
    require(row["tail_target"] == EXPECTED_TAIL_TARGET, "tail target drift")
    require(row["aggregate_excess_max"] == EXPECTED_E_MAX, "Emax drift")
    k_remaining = TANGENT.exact_k_remaining(B_REMAINING_AFTER)
    maximal_binomial = math.comb(K - 2, 8)
    break_j = TANGENT.UNIFORM_CAP + EXPECTED_E_MAX // maximal_binomial + 1
    require(k_remaining == EXPECTED_K_REMAINING, "K_remaining drift")
    require(break_j == EXPECTED_BREAK_J, "maximal-gcd break J drift")
    return {
        "cutoff_D": CUTOFF_D,
        "tail_target": str(EXPECTED_TAIL_TARGET),
        "aggregate_excess_max": str(EXPECTED_E_MAX),
        "aggregate_excess_nonnegative": True,
        "K_remaining": k_remaining,
        "maximal_gcd_break_J": break_j,
        "gate": row["gate"],
    }


def boundary_route_cut() -> dict[str, Any]:
    row = candidate_ledger(FIRST_UNPAID_M)
    require(row["owner_cap"] == M196_OWNER_CAP, "m196 cap drift")
    require(row["U_paid"] == M196_U_PAID, "m196 U_paid drift")
    require(row["B_remaining"] == M196_B_REMAINING, "m196 budget drift")
    require(row["one_cut_defined"] is True, "m196 one-cut unexpectedly undefined")
    require(row["tail_target"] == M196_TAIL_TARGET, "m196 tail drift")
    require(row["aggregate_excess_max"] == M196_E_MAX, "m196 Emax drift")
    require(row["bankable_under_inherited_gate"] is False, "m196 wrongly bankable")
    return {
        "m": FIRST_UNPAID_M,
        "owner_cap": str(row["owner_cap"]),
        "incremental_movement": str(row["incremental_movement"]),
        "U_paid": str(row["U_paid"]),
        "B_remaining": str(row["B_remaining"]),
        "one_cut_defined": True,
        "tail_target": str(row["tail_target"]),
        "aggregate_excess_max": str(row["aggregate_excess_max"]),
        "aggregate_excess_nonnegative": False,
        "bankable_under_inherited_gate": False,
        "route_cut": (
            "current hypotheses provide no nonnegative aggregate-excess "
            "allowance after this owner replacement"
        ),
    }


_EXPECTED_CACHE: dict[str, Any] | None = None


def expected_certificate() -> dict[str, Any]:
    global _EXPECTED_CACHE
    if _EXPECTED_CACHE is not None:
        return copy.deepcopy(_EXPECTED_CACHE)

    predecessor_document = validate_predecessor()
    summaries, profile_total, deficit_shape_total = compile_slack_profiles()
    optimizer = exact_optimizer()
    rank9 = exact_rank9_update()
    m196 = boundary_route_cut()

    note = (ROOT / NOTE_REL).read_text(encoding="utf-8")
    for token in (
        OWNER_ID,
        REPLACED_OWNER_ID,
        PAID_TERMINAL,
        OPEN_TERMINAL,
        "196(p+1)=417{,}618{,}461{,}064",
        "r=196",
        "m=9{,}208",
        "diagonal Krylov",
        "33{,}737",
    ):
        require(token in note, f"proof-note token missing: {token}")

    exponents = {
        i * P + j
        for i in range(DEPLOYED_M + 2)
        for j in range(DEPLOYED_M + 2)
    }
    require(len(exponents) == EXPONENT_COUNT, "exponent collision")
    require(max(exponents) == OWNER_CAP, "eliminant degree endpoint drift")
    require(P > DEPLOYED_M + 1, "field characteristic too small")
    require(SUPPORT_FLOOR > CROSS_MULTIPLIER_DEGREE, "support guard failed")
    require(
        UNIFORM_REDUCED_DEGREE_FLOOR > CROSS_MULTIPLIER_DEGREE,
        "coprimality contradiction floor failed",
    )
    require(
        ALGEBRAIC_MAX_M == (SUPPORT_FLOOR - 1) // 2,
        "algebraic endpoint drift",
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
            "rich_x_max": RICH_X_MAX,
            "domain_subset_base_nonzero": True,
        },
        "predecessor": {
            "note": predecessor.NOTE_REL.as_posix(),
            "payload_sha256": predecessor_document["payload_sha256"],
            "stacked_on_pr_991_commit": "1152de129688997f04280dee0b5c41b1729fa75f",
            "curated_upstream_may_omit_pr_side_json_and_python": True,
        },
        "owner_replacement": {
            "replaced_owner_id": REPLACED_OWNER_ID,
            "replacement_owner_id": OWNER_ID,
            "same_first_match_slot": True,
            "old_owner_not_retained_as_additive_block": True,
            "old_cap": str(REPLACED_OWNER_CAP),
            "new_cap": str(OWNER_CAP),
            "incremental_cap": str(LEDGER_MOVEMENT),
            "incremental_formula": "196*(p+1)-2*(p+1)=194*(p+1)",
            "retains_entire_predecessor_closure": True,
        },
        "slack_profile_compiler": {
            "slack_definition": "r=s-t-1=h+u+ell",
            "deployed_r_min": 1,
            "deployed_r_max": DEPLOYED_M,
            "source_size_min": T + 2,
            "source_size_max": T + DEPLOYED_M + 1,
            "profile_count": profile_total,
            "profile_count_formula": "C(198,3)-1",
            "deficit_shape_count": deficit_shape_total,
            "deficit_shape_count_formula": "C(199,4)-1",
            "boundary_profile_count": BOUNDARY_PROFILE_COUNT,
            "boundary_profile_count_formula": "C(197,2)",
            "allowed_deficit": "0<=delta_eta<=u",
            "per_r_summaries": summaries,
            "exhaustive_over_integer_h_u_ell": True,
        },
        "effective_multiplier": {
            "factorization": "H=L_C*G; Pbar+eta*Qbar=L_F_eta*A_eta",
            "definition": "B_eta=G*A_eta",
            "degree_formula": "deg(B_eta)<=h+u-delta_eta=r-ell-delta_eta<=r",
            "uniform_degree_max": DEPLOYED_M,
            "all_profiles_r1_through_r195_covered": True,
            "source_identity": "S_a(eta)=L_C(a)*L_F_eta(a)*B_eta(a)",
            "source_base_multiplier_nonzero": True,
            "coefficient_frobenius_not_polynomial_pth_power": True,
        },
        "source_frobenius_eliminant": {
            "name": "2(m+1)-anchor diagonal source-Frobenius determinant",
            "deployed_m": DEPLOYED_M,
            "anchor_size": ANCHOR_SIZE,
            "row_blocks": [
                "a^i*S_a(Z)^p for 0<=i<=m",
                "a^i*S_a(Z) for 0<=i<=m",
            ],
            "kernel_coefficients": "(b_0,...,b_m,-b_0^p,...,-b_m^p)",
            "every_claimed_selected_slope_annihilates_every_minor": True,
            "degree_formula": "(m+1)*(p+1)",
            "degree_cap": str(OWNER_CAP),
            "diagonal_exponent_range": "i*p+j, 0<=i,j<=m+1",
            "diagonal_exponent_count": EXPONENT_COUNT,
            "diagonal_exponents_distinct": True,
            "source_only": True,
            "selector_chosen_minor_forbidden": True,
            "union_over_minors_records_or_profiles_forbidden": True,
        },
        "nonvanishing_lemma": {
            "name": "commuting diagonal Krylov nondegeneracy",
            "source_combination_support_min": SUPPORT_FLOOR,
            "Krylov_dimension": DEPLOYED_M + 1,
            "cross_multiplier_degree_max": CROSS_MULTIPLIER_DEGREE,
            "support_minus_cross_degree": SUPPORT_FLOOR - CROSS_MULTIPLIER_DEGREE,
            "source_minus_e_plus_cross_degree_min": (
                SUPPORT_FLOOR - CROSS_MULTIPLIER_DEGREE
            ),
            "common_cross_vector_nonzero": True,
            "source_root_count_promotes_identity": True,
            "coprimality_forces_reduced_degrees_at_most": CROSS_MULTIPLIER_DEGREE,
            "uniform_reduced_degree_floor": UNIFORM_REDUCED_DEGREE_FLOOR,
            "contradiction": "e<=390<33737",
            "Segre_or_opposite_ruling_inference_used": False,
            "diagonal_M_commutativity_used": True,
            "canonical_nonzero_minor_exists_if_record_exists": True,
        },
        "pair_global_owner": {
            "owner_id": OWNER_ID,
            "owner_definition": (
                "finite roots of the lexicographically first nonzero "
                "392-anchor source eliminant"
            ),
            "intrinsic_to_fixed_source_pair": True,
            "empty_if_all_source_minors_zero": True,
            "finite_slope_cap": str(OWNER_CAP),
            "ordinary_nonzero_polynomial_root_bound_used": True,
            "subset_stable_for_every_incoming_slope_subset": True,
            "post_restart_r1_through_r195_records_impossible": True,
            "paid_terminal": PAID_TERMINAL,
            "replaced_open_terminal": REPLACED_OPEN_TERMINAL,
        },
        "first_match_partition": {
            "order": FIRST_MATCH_ORDER,
            "replacement_index_one_based": FIRST_MATCH_ORDER.index(OWNER_ID) + 1,
            "old_owner_absent": REPLACED_OWNER_ID not in FIRST_MATCH_ORDER,
            "incoming_exact_residual_required": True,
            "later_owners_receive_exact_set_difference": True,
            "per_selector_charge_forbidden": True,
            "replacement_not_additive": True,
        },
        "selector_restart": {
            "complete_selector_universe_must_be_rebuilt": True,
            "restart_order": list(TANGENT.RESTART_ORDER),
            "global_carrier_and_small_family_gates_rerun": True,
            "affine_rank_minimizer_recomputed": True,
            "same_received_pair_source_and_sp3_translation_downstream": True,
            "all_rank_le_9_terminals_replayed_in_frozen_order": True,
            "rank_at_least_10_not_authorized": True,
        },
        "exact_control": {
            "base_field": "GF(13)",
            "extension_field": "GF(13^2)",
            "fixture_role": "degree-two specialization of general theorem",
            "source_points": [1, 2, 3, 4, 5, 6],
            "moving_points": [7, 8, 9, 10, 11, 12],
            "six_anchor_minor_nonzero": True,
            "selected_slopes_are_minor_roots": True,
            "all_three_step_Krylov_ranks_full": True,
            "coefficient_frobenius_degrees_checked": [0, 1, 2],
            "low_degree_all_minors_zero_control": True,
            "root_count_equality_control": True,
            "skew_block_plane_incidence_countercontrol": True,
            "deployed_m_arithmetic_checked": True,
            "algebraic_endpoint_checked": True,
            "ledger_boundary_checked": True,
            "sage_interface_mutations": 50,
            "complete_selector_constructed": False,
            "deployed_rank9_record_constructed": False,
            "scale": "EXACT_SPECIALIZATION_AND_INTEGER_CONTROL_NOT_DEPLOYED_CENSUS_OR_PROOF",
        },
        "ledger": {
            "B_star": str(B_STAR),
            "replaced_owner_cap": str(REPLACED_OWNER_CAP),
            "replacement_owner_cap": str(OWNER_CAP),
            "incremental_movement": str(LEDGER_MOVEMENT),
            "full_new_cap_not_added_to_predecessor": True,
            "U_paid_before": str(U_PAID_BEFORE),
            "U_paid_after": str(U_PAID_AFTER),
            "B_remaining_before": str(B_REMAINING_BEFORE),
            "B_remaining_after": str(B_REMAINING_AFTER),
            "charge_is_once_per_received_pair_not_per_selector": True,
            "rank9_updated_gate": rank9,
            "U_Q": None,
            "residual_U_A": None,
            "complete_upper_inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        },
        "ledger_maximality": {
            "optimizer": optimizer,
            "deployed_m": DEPLOYED_M,
            "active_maximality_gate": "aggregate_excess_max>=0",
            "m196_boundary": m196,
            "last_one_cut_defined_m": LAST_ONE_CUT_DEFINED_M,
            "first_one_cut_undefined_m": FIRST_ONE_CUT_UNDEFINED_M,
            "algebraic_max_m": ALGEBRAIC_MAX_M,
            "first_algebraic_failure_m": FIRST_ALGEBRAIC_FAILURE_M,
            "algebraic_support_floor": SUPPORT_FLOOR,
            "algebraic_strict_condition": "2*m<18418",
            "algebraic_m9208_margin": SUPPORT_FLOOR - 2 * ALGEBRAIC_MAX_M,
            "m9209_equality_fails_strictness": True,
            "current_ledger_blocks_before_algebra_blocks": True,
        },
        "revised_residual": {
            "zero_slack_boundary_owned_upstream": True,
            "all_full_outside_slack_layers_r1_through_r195_owned": True,
            "next_slack_r_min": FIRST_UNPAID_M,
            "next_source_size_min": NEXT_SOURCE_SIZE,
            "next_reduced_degree_min": NEXT_REDUCED_DEGREE_MIN,
            "next_full_gcd_degree_max": NEXT_FULL_GCD_MAX,
            "terminal": OPEN_TERMINAL,
        },
        "residual_route_cuts": [
            {
                "terminal": OPEN_TERMINAL,
                "condition": "full-outside coefficient-rank-two rich records with r>=196",
                "status": "UNPAID",
                "missing_lemma": (
                    "stronger rank-nine incidence/accounting bound replacing "
                    "the exhausted aggregate-excess allowance"
                ),
            },
            {
                "terminal": "ALGEBRAIC_EFFECTIVE_MULTIPLIER_ENDPOINT_R9209",
                "condition": "current coarse support floor equals 2r",
                "status": "ROUTE_CUT_FOR_THIS_KRYLOV_METHOD",
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
            "old_four_anchor_owner_replaced": True,
            "old_four_anchor_charge_retained_additively": False,
            "r1_through_r195_closed": True,
            "r196_closed": False,
            "r9208_banked": False,
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
            "No alternative SP3 translations are unioned.",
            "No selector-chosen, per-record, or per-profile eliminant is charged.",
            "The determinant condition is necessary, not sufficient.",
            "The degree-two Sage fixture is a specialization, not a degree-195 construction.",
            "The algebraic m=9208 endpoint is not banked in the inherited ledger.",
            "A negative aggregate-excess value is a failed gate, not a usable break index.",
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
    require(document == expected_certificate(), "certificate semantic/source drift")


def mutation_cases() -> list[tuple[str, Callable[[dict[str, Any]], None]]]:
    return [
        ("schema", lambda d: d.__setitem__("schema", "wrong")),
        ("status", lambda d: d.__setitem__("status", "GLOBAL_GREEN")),
        ("field", lambda d: d["row"].__setitem__("p", P + 1)),
        ("domain-zero", lambda d: d["row"].__setitem__("domain_subset_base_nonzero", False)),
        ("predecessor-payload", lambda d: d["predecessor"].__setitem__("payload_sha256", "0" * 64)),
        ("replacement-id", lambda d: d["owner_replacement"].__setitem__("replacement_owner_id", "wrong")),
        ("retain-old", lambda d: d["owner_replacement"].__setitem__("old_owner_not_retained_as_additive_block", False)),
        ("old-cap", lambda d: d["owner_replacement"].__setitem__("old_cap", str(REPLACED_OWNER_CAP + 1))),
        ("new-cap", lambda d: d["owner_replacement"].__setitem__("new_cap", str(OWNER_CAP + 1))),
        ("increment", lambda d: d["owner_replacement"].__setitem__("incremental_cap", str(LEDGER_MOVEMENT + 1))),
        ("r-max", lambda d: d["slack_profile_compiler"].__setitem__("deployed_r_max", FIRST_UNPAID_M)),
        ("profile-count", lambda d: d["slack_profile_compiler"].__setitem__("profile_count", PROFILE_COUNT - 1)),
        ("deficit-count", lambda d: d["slack_profile_compiler"].__setitem__("deficit_shape_count", DEFICIT_SHAPE_COUNT - 1)),
        ("boundary-count", lambda d: d["slack_profile_compiler"].__setitem__("boundary_profile_count", BOUNDARY_PROFILE_COUNT - 1)),
        ("profile-source", lambda d: d["slack_profile_compiler"]["per_r_summaries"][-1].__setitem__("source_size", NEXT_SOURCE_SIZE)),
        ("profile-degree", lambda d: d["slack_profile_compiler"]["per_r_summaries"][-1].__setitem__("effective_multiplier_degree_max", FIRST_UNPAID_M)),
        ("profile-support", lambda d: d["slack_profile_compiler"]["per_r_summaries"][0].__setitem__("source_combination_support_min", SUPPORT_FLOOR - 1)),
        ("multiplier-max", lambda d: d["effective_multiplier"].__setitem__("uniform_degree_max", FIRST_UNPAID_M)),
        ("base-nonzero", lambda d: d["effective_multiplier"].__setitem__("source_base_multiplier_nonzero", False)),
        ("anchor-size", lambda d: d["source_frobenius_eliminant"].__setitem__("anchor_size", ANCHOR_SIZE - 1)),
        ("det-degree", lambda d: d["source_frobenius_eliminant"].__setitem__("degree_cap", str(OWNER_CAP - 1))),
        ("exponent-count", lambda d: d["source_frobenius_eliminant"].__setitem__("diagonal_exponent_count", EXPONENT_COUNT - 1)),
        ("selector-minor", lambda d: d["source_frobenius_eliminant"].__setitem__("selector_chosen_minor_forbidden", False)),
        ("support-floor", lambda d: d["nonvanishing_lemma"].__setitem__("source_combination_support_min", SUPPORT_FLOOR - 1)),
        ("cross-degree", lambda d: d["nonvanishing_lemma"].__setitem__("cross_multiplier_degree_max", CROSS_MULTIPLIER_DEGREE + 1)),
        ("uniform-e-floor", lambda d: d["nonvanishing_lemma"].__setitem__("uniform_reduced_degree_floor", 33_738)),
        ("common-vector", lambda d: d["nonvanishing_lemma"].__setitem__("common_cross_vector_nonzero", False)),
        ("segre", lambda d: d["nonvanishing_lemma"].__setitem__("Segre_or_opposite_ruling_inference_used", True)),
        ("owner-cap", lambda d: d["pair_global_owner"].__setitem__("finite_slope_cap", str(OWNER_CAP + 1))),
        ("pair-global", lambda d: d["pair_global_owner"].__setitem__("intrinsic_to_fixed_source_pair", False)),
        ("first-match-order", lambda d: d["first_match_partition"]["order"].reverse()),
        ("per-selector", lambda d: d["first_match_partition"].__setitem__("per_selector_charge_forbidden", False)),
        ("restart", lambda d: d["selector_restart"].__setitem__("complete_selector_universe_must_be_rebuilt", False)),
        ("rank10", lambda d: d["selector_restart"].__setitem__("rank_at_least_10_not_authorized", False)),
        ("sage-count", lambda d: d["exact_control"].__setitem__("sage_interface_mutations", 49)),
        ("deployed-selector", lambda d: d["exact_control"].__setitem__("complete_selector_constructed", True)),
        ("ledger-old-cap", lambda d: d["ledger"].__setitem__("replaced_owner_cap", str(REPLACED_OWNER_CAP + 1))),
        ("ledger-new-cap", lambda d: d["ledger"].__setitem__("replacement_owner_cap", str(OWNER_CAP + 1))),
        ("ledger-additive", lambda d: d["ledger"].__setitem__("full_new_cap_not_added_to_predecessor", False)),
        ("U-paid", lambda d: d["ledger"].__setitem__("U_paid_after", str(U_PAID_AFTER + 1))),
        ("B-rem", lambda d: d["ledger"].__setitem__("B_remaining_after", str(B_REMAINING_AFTER + 1))),
        ("tail", lambda d: d["ledger"]["rank9_updated_gate"].__setitem__("tail_target", str(EXPECTED_TAIL_TARGET + 1))),
        ("Emax", lambda d: d["ledger"]["rank9_updated_gate"].__setitem__("aggregate_excess_max", str(EXPECTED_E_MAX + 1))),
        ("Kremaining", lambda d: d["ledger"]["rank9_updated_gate"].__setitem__("K_remaining", EXPECTED_K_REMAINING + 1)),
        ("break-J", lambda d: d["ledger"]["rank9_updated_gate"].__setitem__("maximal_gcd_break_J", EXPECTED_BREAK_J + 1)),
        ("optimizer-digest", lambda d: d["ledger_maximality"]["optimizer"].__setitem__("scan_sha256", "0" * 64)),
        ("optimizer-max", lambda d: d["ledger_maximality"]["optimizer"].__setitem__("bankable_prefix_max_m", FIRST_UNPAID_M)),
        ("first-fail", lambda d: d["ledger_maximality"]["optimizer"].__setitem__("first_nonbankable_m", DEPLOYED_M)),
        ("m196-cap", lambda d: d["ledger_maximality"]["m196_boundary"].__setitem__("owner_cap", str(M196_OWNER_CAP - 1))),
        ("m196-tail", lambda d: d["ledger_maximality"]["m196_boundary"].__setitem__("tail_target", str(M196_TAIL_TARGET + 1))),
        ("m196-E", lambda d: d["ledger_maximality"]["m196_boundary"].__setitem__("aggregate_excess_max", str(M196_E_MAX + 1))),
        ("m196-accepted", lambda d: d["ledger_maximality"]["m196_boundary"].__setitem__("bankable_under_inherited_gate", True)),
        ("last-one-cut", lambda d: d["ledger_maximality"].__setitem__("last_one_cut_defined_m", LAST_ONE_CUT_DEFINED_M + 1)),
        ("alg-max", lambda d: d["ledger_maximality"].__setitem__("algebraic_max_m", FIRST_ALGEBRAIC_FAILURE_M)),
        ("alg-margin", lambda d: d["ledger_maximality"].__setitem__("algebraic_m9208_margin", 0)),
        ("m9208-bank", lambda d: d["scope_guards"].__setitem__("r9208_banked", True)),
        ("r196-close", lambda d: d["scope_guards"].__setitem__("r196_closed", True)),
        ("next-r", lambda d: d["revised_residual"].__setitem__("next_slack_r_min", DEPLOYED_M)),
        ("next-source", lambda d: d["revised_residual"].__setitem__("next_source_size_min", NEXT_SOURCE_SIZE - 1)),
        ("next-degree", lambda d: d["revised_residual"].__setitem__("next_reduced_degree_min", NEXT_REDUCED_DEGREE_MIN - 1)),
        ("next-gcd", lambda d: d["revised_residual"].__setitem__("next_full_gcd_degree_max", NEXT_FULL_GCD_MAX + 1)),
        ("row-closed", lambda d: d["scope_guards"].__setitem__("koalabear_row_closed", True)),
        ("UQ", lambda d: d["scope_guards"].__setitem__("U_Q_determined", True)),
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
    print(f"M1 bounded-slack effective-multiplier mutations: {total}/{total} PASS")
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
    print("M1 bounded-slack effective-multiplier Frobenius owner: PASS")
    print(
        f"  source-Frobenius slot: {REPLACED_OWNER_CAP:,} -> {OWNER_CAP:,}; "
        f"increment {LEDGER_MOVEMENT:,}"
    )
    print(f"  closed slack layers: 1..{DEPLOYED_M}; profiles: {PROFILE_COUNT:,}")
    print(f"  U_paid: {U_PAID_BEFORE:,} -> {U_PAID_AFTER:,}")
    print(f"  B_remaining: {B_REMAINING_BEFORE:,} -> {B_REMAINING_AFTER:,}")
    print(f"  T_18,014: {EXPECTED_TAIL_TARGET:,}; break J={EXPECTED_BREAK_J}")
    print(f"  exact ledger route cut: r={FIRST_UNPAID_M}; Emax={M196_E_MAX:,}")
    print(f"  local algebra endpoint: r={ALGEBRAIC_MAX_M}; strictness fails at {FIRST_ALGEBRAIC_FAILURE_M}")
    print(f"  terminal paid: {PAID_TERMINAL}")
    print(f"  terminal open: {OPEN_TERMINAL}")
    print("  U_Q/residual U_A/non-full-outside load remain open; row YELLOW")
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
