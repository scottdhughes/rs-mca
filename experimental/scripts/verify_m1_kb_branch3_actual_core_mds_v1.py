#!/usr/bin/env python3
"""Verify the KoalaBear branch-3 actual-core MDS rank-ladder splice.

The load-bearing implication is deterministic and exact.  The predecessor
supplies one complete rank-minimizing actual-witness selector whose basis
carrier is its complete support union.  Restricting the RS parity check to
that carrier produces an MDS kernel.  The imported actual-core
basis-multiplicity theorem then pays intrinsic affine ranks four through
eight; its conservative rank-nine cap does not fit.

No deployed-field census, unconditional ledger movement, branch-3 closure,
or KoalaBear-row closure is claimed.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

SCHEMA = "rs-mca-m1-kb-branch3-actual-core-mds-v1"
ARTIFACT_KIND = "M1_KB_BRANCH3_ACTUAL_CORE_MDS_RANK_LADDER"
STATUS = (
    "PROVED_IMPORTED_ACTUAL_CORE_MDS_SPLICE_RANKS_4_TO_8_UNIFORM_"
    "RANK9_JOINT_CUT_NO_LEDGER_MOVEMENT"
)

CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "m1-kb-branch3-actual-core-mds-v1"
)
CERT_PATH = CERT_DIR / "m1_kb_branch3_actual_core_mds_v1.json"

NOTE_REL = Path(
    "experimental/notes/m1/"
    "m1_kb_branch3_actual_core_mds_rank_ladder_v1.md"
)
README_REL = Path(
    "experimental/data/certificates/"
    "m1-kb-branch3-actual-core-mds-v1/README.md"
)
PYTHON_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py"
)
SAGE_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.sage"
)
PREDECESSOR_NOTE_REL = Path(
    "experimental/notes/m1/m1_kb_branch3_tdd_excess_v1.md"
)
PREDECESSOR_CERT_REL = Path(
    "experimental/data/certificates/m1-kb-branch3-tdd-excess-v1/"
    "m1_kb_branch3_tdd_excess_v1.json"
)
PREDECESSOR_VERIFIER_REL = Path(
    "experimental/scripts/verify_m1_kb_branch3_tdd_excess_v1.py"
)
ACTUAL_CORE_NOTE_REL = Path(
    "experimental/notes/thresholds/"
    "a6_actual_witness_core_rank_preflight.md"
)
ACTUAL_CORE_VERIFIER_REL = Path(
    "experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py"
)

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
MIN_GLOBAL_UNPAID_EXCESS = 11

DENOMINATOR = 1 << 128
B_STAR = (Q_LINE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID
K_REM = 4_807_520

FIRST_NEW_RANK = 4
LARGEST_PAID_RANK = 8
FIRST_NONUNIFORM_RANK = 9

TOP_KEYS = {
    "schema",
    "artifact_kind",
    "status",
    "source_bindings",
    "row",
    "predecessor_contract",
    "restricted_mds_splice",
    "rank_ladder",
    "owner_registry",
    "classifier_contract",
    "exact_controls",
    "charges",
    "ledger",
    "audit_sections",
    "nonclaims",
    "payload_sha256",
}

NONCLAIMS = [
    "This packet does not prove branch 3 closed.",
    "This packet does not prove the KoalaBear row safe.",
    "This packet does not bank an unconditional charge.",
    "This packet does not determine the deployed intrinsic selector rank.",
    "This packet does not add rank caps or charge them per subfamily.",
    "This packet does not claim an extension factor ell_q larger than one.",
    "This packet does not pay the entire intrinsic affine-rank-nine stratum.",
    "This packet does not prove a canonical TDD-union injection.",
    "This packet does not determine U_2, U_Q, or U_A.",
    "This packet does not begin a higher-m or degree-three parameter class.",
    "This packet does not authorize Lean or Paper-D theorem promotion.",
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
        binding("packet-note", NOTE_REL, "load-bearing theorem splice"),
        binding("packet-readme", README_REL, "replay instructions"),
        binding("packet-verifier", PYTHON_REL, "exact certificate verifier"),
        binding("sage-control", SAGE_REL, "independent tiny MDS control"),
        binding(
            "predecessor-note",
            PREDECESSOR_NOTE_REL,
            "complete-selector rank and basis-carrier bridge",
        ),
        binding(
            "predecessor-certificate",
            PREDECESSOR_CERT_REL,
            "frozen KoalaBear TDD predecessor state",
        ),
        binding(
            "predecessor-verifier",
            PREDECESSOR_VERIFIER_REL,
            "predecessor replay",
        ),
        binding(
            "actual-core-theorem",
            ACTUAL_CORE_NOTE_REL,
            "imported actual-core basis-multiplicity theorem",
        ),
        binding(
            "actual-core-verifier",
            ACTUAL_CORE_VERIFIER_REL,
            "imported theorem replay",
        ),
    ]


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator > 0, "invalid ceiling division")
    return (numerator + denominator - 1) // denominator


def rank_row(s: int) -> dict[str, Any]:
    require(FIRST_NEW_RANK <= s <= FIRST_NONUNIFORM_RANK, "rank out of scan")
    r = s - 1
    basis_multiplicity_numerator = math.comb(DELTA_ZERO + r, r)
    mu = ceil_div(basis_multiplicity_numerator, s)
    cap = math.comb(N, s) // mu
    total = U_PAID + cap
    margin = B_STAR - total
    fits = cap <= B_REMAINING
    return {
        "intrinsic_affine_rank_s": s,
        "residual_core_rank_r": r,
        "basis_carrier_supports": s + 1,
        "multiplicity_binomial": str(basis_multiplicity_numerator),
        "mu_s": str(mu),
        "ambient_binomial": str(math.comb(N, s)),
        "cap_B_s": str(cap),
        "conditional_total_with_paid_baseline": str(total),
        "margin_to_B_star": str(margin),
        "fits_remaining_budget": fits,
        "terminal": (
            "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK_4_TO_8"
            if fits
            else "UNPAID_UNIFORM_WORST_CASE_REQUIRES_RANK9_JOINT_BOUNDARY"
        ),
    }


def rank_rows() -> list[dict[str, Any]]:
    return [rank_row(s) for s in range(FIRST_NEW_RANK, FIRST_NONUNIFORM_RANK + 1)]


def rank9_mu(extension_factor: int) -> int:
    require(
        1 <= extension_factor <= DELTA_ZERO,
        "rank-nine extension factor outside source-distance range",
    )
    denominator = math.comb(DELTA_ZERO + FIRST_NONUNIFORM_RANK - 1, 8)
    return ceil_div(extension_factor * denominator, FIRST_NONUNIFORM_RANK)


def rank9_actual_cap(carrier_size: int, extension_factor: int) -> int:
    require(
        R + MIN_GLOBAL_UNPAID_EXCESS <= carrier_size <= N,
        "rank-nine carrier size outside residual range",
    )
    return math.comb(carrier_size, FIRST_NONUNIFORM_RANK) // rank9_mu(
        extension_factor
    )


def largest_paid_rank9_carrier(extension_factor: int) -> int:
    lower = R + MIN_GLOBAL_UNPAID_EXCESS
    upper = N
    if rank9_actual_cap(upper, extension_factor) <= B_REMAINING:
        return upper
    require(
        rank9_actual_cap(lower, extension_factor) <= B_REMAINING,
        "rank-nine residual begins below minimum carrier",
    )
    while lower < upper:
        middle = (lower + upper + 1) // 2
        if rank9_actual_cap(middle, extension_factor) <= B_REMAINING:
            lower = middle
        else:
            upper = middle - 1
    return lower


def rank9_boundary_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for extension_factor in range(1, 8):
        maximum = largest_paid_rank9_carrier(extension_factor)
        row: dict[str, Any] = {
            "extension_factor_ell_q": extension_factor,
            "mu_9": str(rank9_mu(extension_factor)),
            "largest_paid_carrier_size": maximum,
            "cap_at_largest_paid_carrier": str(
                rank9_actual_cap(maximum, extension_factor)
            ),
            "all_carriers_through_n_paid": maximum == N,
        }
        if maximum < N:
            row["first_unpaid_carrier_size"] = maximum + 1
            row["cap_at_first_unpaid_carrier"] = str(
                rank9_actual_cap(maximum + 1, extension_factor)
            )
        else:
            row["first_unpaid_carrier_size"] = None
            row["cap_at_first_unpaid_carrier"] = None
        rows.append(row)
    return rows


def classify_intrinsic_rank(
    *,
    named_owner: bool = False,
    global_carrier_certificate_present: bool = False,
    complete_selector: bool = False,
    selector_attains_intrinsic_minimum: bool = False,
    basis_carrier_equals_complete_union: bool = False,
    transversality_contract: bool = False,
    selected_error_weight_within_j: bool = False,
    selector_rank_carrier_lift_coherent: bool = False,
    matched_extension_factor_certified: bool = False,
    minimum_global_carrier_excess: int | None = None,
    intrinsic_affine_rank: int | None = None,
    carrier_size: int | None = None,
    extension_factor: int | None = None,
) -> str:
    if named_owner:
        return "PAID_NAMED_PREDECESSOR_OWNER"
    if minimum_global_carrier_excess is not None:
        require(
            minimum_global_carrier_excess >= 0,
            "negative global carrier excess",
        )
        if minimum_global_carrier_excess <= 10:
            return (
                "PAID_ONE_GLOBAL_CARRIER_EXCESS_LE_10"
                if global_carrier_certificate_present
                else "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
            )
    if carrier_size is not None and minimum_global_carrier_excess is not None:
        require(
            R + minimum_global_carrier_excess <= carrier_size <= N,
            "selector carrier size inconsistent with intrinsic minimum",
        )
    if extension_factor is not None:
        require(
            1 <= extension_factor <= DELTA_ZERO,
            "extension factor outside source-distance range",
        )
    if (
        not complete_selector
        or not basis_carrier_equals_complete_union
        or not transversality_contract
        or not selected_error_weight_within_j
        or not selector_rank_carrier_lift_coherent
        or minimum_global_carrier_excess is None
        or intrinsic_affine_rank is None
    ):
        return "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
    require(intrinsic_affine_rank >= 0, "negative intrinsic affine rank")
    if intrinsic_affine_rank <= 3:
        return "PAID_COMPLETE_SELECTOR_AFFINE_RANK_LE_3"
    if intrinsic_affine_rank <= LARGEST_PAID_RANK:
        return "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK_4_TO_8"
    if intrinsic_affine_rank == FIRST_NONUNIFORM_RANK:
        if carrier_size is None or extension_factor is None:
            return "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        if extension_factor > 1 and not matched_extension_factor_certified:
            return "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        if rank9_actual_cap(carrier_size, extension_factor) <= B_REMAINING:
            return "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK9_JOINT_BOUNDARY"
        if selector_attains_intrinsic_minimum:
            return "UNPAID_BY_COARSE_UNIFORM_RANK9_MDS_JOINT_BOUND"
        return "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
    if selector_attains_intrinsic_minimum:
        return "UNPAID_PRIMITIVE_INTRINSIC_RANK_AT_LEAST_10_TDD_SPREAD"
    return "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"


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
        "minimum_distance": MINIMUM_DISTANCE,
        "B_star": str(B_STAR),
        "U_paid": str(U_PAID),
        "B_remaining": str(B_REMAINING),
    }


def expected_predecessor_contract() -> dict[str, Any]:
    return {
        "predecessor_schema": "rs-mca-m1-kb-branch3-tdd-excess-v1",
        "retained_family_size_gt_15": True,
        "selector_set": "ALL_COMPLETE_VALID_ACTUAL_WITNESS_SELECTORS",
        "rank_minimizing_complete_selector_fixed_before_anchors": True,
        "global_carrier_owner_existential_over_complete_selectors": True,
        "carrier_complement_kappa_star_minimum": MIN_GLOBAL_UNPAID_EXCESS,
        "kappa_star_ge_11_makes_every_complete_selector_high_union": True,
        "syndrome_line": "H e_eta = y0 + eta*y1 WITH y1 != 0",
        "selected_error_weight_cap": J,
        "transverse_actual_witness_contract": True,
        "selected_difference_space": "D_sel=span{e_eta-e_alpha}",
        "residual_codeword_space": "R_sel=span{r_eta}",
        "rank_identity": "s_star=1+dim(R_sel)",
        "basis_carrier_support_count": "s_star+1",
        "basis_carrier_equals_complete_selected_union": True,
        "predecessor_first_unpaid_rank": FIRST_NEW_RANK,
        "predecessor_first_unpaid_residual_rank": FIRST_NEW_RANK - 1,
        "predecessor_first_unpaid_basis_supports": FIRST_NEW_RANK + 1,
    }


def expected_restricted_mds_splice() -> dict[str, Any]:
    return {
        "carrier_notation": "N_V=|V|=R+nu",
        "carrier_excess_range": [MIN_GLOBAL_UNPAID_EXCESS, K],
        "restriction_preserves_all_selected_weights": True,
        "restriction_preserves_transversality_support_images": True,
        "parity_check_dimensions": "R BY (R+nu)",
        "every_R_columns_independent": True,
        "restricted_kernel": "[R+nu,nu,R+1]_F_MDS",
        "restricted_kernel_dimension": "nu",
        "restricted_kernel_distance": R + 1,
        "actual_core": "K0=D_sel INTERSECT K_V=R_sel",
        "actual_core_rank": "r=s_star-1",
        "imported_witness_budget_t": J,
        "witness_budget_below_redundancy_R": J < R,
        "complete_zero_mask_floor": "q=N_V-j=nu+Delta0",
        "q_minus_kappa_plus_r": "Delta0+s_star-1",
        "q_at_least_kappa_plus_1": True,
        "source_minimum_lift": "d_V=MIN{wt(z):H_V z=y1}",
        "extension_factor": "ell_q=MAX(1,d_V-j)",
        "only_extension_lower_bound_used": 1,
        "uniform_mu_formula": (
            "CEIL(BINOM(Delta0+s-1,s-1)/s)"
        ),
        "uniform_cap_formula": "FLOOR(BINOM(n,s)/mu_s)",
        "carrier_excess_cancels_from_mu": True,
        "rank_carrier_lift_values_from_same_selector_and_restriction": True,
        "matched_extension_factor_certificate_required_above_one": True,
        "cap_applied_once_to_complete_retained_family": True,
    }


def expected_rank_ladder() -> dict[str, Any]:
    rows = rank_rows()
    paid_rows = [row for row in rows if row["fits_remaining_budget"]]
    unpaid_rows = [row for row in rows if not row["fits_remaining_budget"]]
    caps = [int(row["cap_B_s"]) for row in rows]
    worst_paid = max(paid_rows, key=lambda row: int(row["cap_B_s"]))
    return {
        "scan_range": [FIRST_NEW_RANK, FIRST_NONUNIFORM_RANK],
        "rows": rows,
        "caps_strictly_increasing_on_scan": all(
            left < right for left, right in zip(caps, caps[1:])
        ),
        "paid_intrinsic_rank_range": [FIRST_NEW_RANK, LARGEST_PAID_RANK],
        "first_rank_not_uniformly_paid": FIRST_NONUNIFORM_RANK,
        "rank9_residual_core_rank": FIRST_NONUNIFORM_RANK - 1,
        "rank9_basis_carrier_supports": FIRST_NONUNIFORM_RANK + 1,
        "rank9_joint_boundary": rank9_boundary_rows(),
        "rank9_all_carriers_paid_extension_floor": 7,
        "rank9_coarse_uniform_failure_predicate": (
            "ell_q_IN_1_TO_6_AND_N_V_GT_N_MAX(ell_q)"
        ),
        "larger_actual_masks_or_nonuniform_sum_may_pay_inside_failure_region": True,
        "worst_paid_rank": worst_paid["intrinsic_affine_rank_s"],
        "worst_paid_cap": worst_paid["cap_B_s"],
        "worst_paid_conditional_total": worst_paid[
            "conditional_total_with_paid_baseline"
        ],
        "worst_paid_margin": worst_paid["margin_to_B_star"],
        "paid_row_count": len(paid_rows),
        "unpaid_row_count": len(unpaid_rows),
        "rank_caps_are_alternatives_not_a_sum": True,
    }


def expected_owner_registry() -> dict[str, Any]:
    return {
        "first_match_order": [
            "NAMED_ALREADY_PAID_QUOTIENT_PERIODIC_JOHNSON_COMMON_SUPPORT",
            "ONE_GLOBAL_CARRIER_EXCESS_LE_10",
            "COMPLETE_SELECTOR_AFFINE_RANK_LE_3",
            "ACTUAL_CORE_MDS_INTRINSIC_RANK_4_TO_8",
            "ACTUAL_CORE_MDS_INTRINSIC_RANK9_JOINT_BOUNDARY",
            "FUTURE_DEDUPLICATED_TDD_ROOT_UNION_WITH_PROVED_MULTIPLICITY",
            "UNPAID_BY_COARSE_RANK9_JOINT_OR_RANK_AT_LEAST_10_TDD_SPREAD",
        ],
        "actual_core_owner_requires_complete_selector": True,
        "paid_actual_core_owner_requires_rank_minimizing_selector": False,
        "unpaid_intrinsic_residual_requires_rank_minimizing_selector": True,
        "actual_core_owner_applies_once_globally": True,
        "actual_core_owner_is_not_per_triple": True,
        "actual_core_owner_is_not_per_rank_sum": True,
        "future_union_owner_proved": False,
        "forbidden_inferences": [
            "ARBITRARY_SELECTOR_RANK_EQUALS_INTRINSIC_RANK",
            "LOCAL_TRIPLE_RANK_IMPLIES_COMPLETE_SELECTOR_RANK",
            "REPEATED_ACTUAL_CORE_CAP_WITHOUT_BOUNDED_COVER",
            "SUM_MUTUALLY_EXCLUSIVE_INTRINSIC_RANK_CAPS",
            "ELL_Q_EXCEEDS_ONE_WITHOUT_SOURCE_DISTANCE_PROOF",
            "FORCE_ALL_RANK9_INTO_UNIFORM_RANK8_OWNER",
            "DISCARD_ACTUAL_RANK9_CARRIER_SIZE_OR_EXTENSION_FACTOR",
        ],
    }


def expected_classifier_contract() -> dict[str, Any]:
    base = {
        "global_carrier_certificate_present": True,
        "complete_selector": True,
        "selector_attains_intrinsic_minimum": True,
        "basis_carrier_equals_complete_union": True,
        "transversality_contract": True,
        "selected_error_weight_within_j": True,
        "selector_rank_carrier_lift_coherent": True,
        "matched_extension_factor_certified": True,
        "minimum_global_carrier_excess": 11,
        "carrier_size": N,
        "extension_factor": 1,
    }
    return {
        "cases": {
            "named_owner": classify_intrinsic_rank(
                **base, named_owner=True, intrinsic_affine_rank=9
            ),
            "global_carrier_10": classify_intrinsic_rank(
                **{**base, "minimum_global_carrier_excess": 10},
                intrinsic_affine_rank=9,
            ),
            "uncertified_global_carrier_10": classify_intrinsic_rank(
                minimum_global_carrier_excess=10
            ),
            "rank_3": classify_intrinsic_rank(
                **base, intrinsic_affine_rank=3
            ),
            "rank_4": classify_intrinsic_rank(
                **base, intrinsic_affine_rank=4
            ),
            "rank_8": classify_intrinsic_rank(
                **base, intrinsic_affine_rank=8
            ),
            "rank_9": classify_intrinsic_rank(
                **base, intrinsic_affine_rank=9
            ),
            "rank_9_boundary_plus_1": classify_intrinsic_rank(
                **{**base, "carrier_size": 1_699_345},
                intrinsic_affine_rank=9,
            ),
            "rank_9_small_carrier": classify_intrinsic_rank(
                **{**base, "carrier_size": 1_699_344},
                intrinsic_affine_rank=9,
            ),
            "rank_9_extension_7": classify_intrinsic_rank(
                **{**base, "extension_factor": 7},
                intrinsic_affine_rank=9,
            ),
            "rank_10": classify_intrinsic_rank(
                **base, intrinsic_affine_rank=10
            ),
            "noncomplete_rank_4": classify_intrinsic_rank(
                **{**base, "complete_selector": False},
                intrinsic_affine_rank=4,
            ),
            "nonminimizing_rank_4": classify_intrinsic_rank(
                **{**base, "selector_attains_intrinsic_minimum": False},
                intrinsic_affine_rank=4,
            ),
            "nonminimizing_rank_9_failure": classify_intrinsic_rank(
                **{**base, "selector_attains_intrinsic_minimum": False},
                intrinsic_affine_rank=9,
            ),
            "nonminimizing_rank_10": classify_intrinsic_rank(
                **{**base, "selector_attains_intrinsic_minimum": False},
                intrinsic_affine_rank=10,
            ),
            "missing_complete_union": classify_intrinsic_rank(
                **{**base, "basis_carrier_equals_complete_union": False},
                intrinsic_affine_rank=4,
            ),
            "missing_transversality": classify_intrinsic_rank(
                **{**base, "transversality_contract": False},
                intrinsic_affine_rank=4,
            ),
            "missing_weight_contract": classify_intrinsic_rank(
                **{**base, "selected_error_weight_within_j": False},
                intrinsic_affine_rank=4,
            ),
            "incoherent_selector_data": classify_intrinsic_rank(
                **{**base, "selector_rank_carrier_lift_coherent": False},
                intrinsic_affine_rank=9,
            ),
            "unmatched_extension_7": classify_intrinsic_rank(
                **{
                    **base,
                    "extension_factor": 7,
                    "matched_extension_factor_certified": False,
                },
                intrinsic_affine_rank=9,
            ),
            "missing_rank9_carrier": classify_intrinsic_rank(
                **{**base, "carrier_size": None},
                intrinsic_affine_rank=9,
            ),
            "missing_rank9_extension": classify_intrinsic_rank(
                **{**base, "extension_factor": None},
                intrinsic_affine_rank=9,
            ),
            "minimal_rank4_call": classify_intrinsic_rank(
                intrinsic_affine_rank=4
            ),
            "unknown_rank": classify_intrinsic_rank(
                **base, intrinsic_affine_rank=None
            ),
            "unknown_carrier_minimum": classify_intrinsic_rank(
                **{**base, "minimum_global_carrier_excess": None},
                intrinsic_affine_rank=4,
            ),
        },
        "deployed_complete_selector_certificate_present": False,
        "deployed_intrinsic_affine_rank_known": False,
        "deployed_terminal": (
            "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        ),
        "mathematical_dichotomy": (
            "s_star_LE_8_PAID_OR_RANK9_JOINT_TEST_OR_s_star_GE_10_RESIDUAL"
        ),
        "classifier_banks_unconditional_charge": False,
    }


def expected_exact_controls() -> dict[str, Any]:
    rows = rank_rows()
    row4 = rows[0]
    row8 = rows[LARGEST_PAID_RANK - FIRST_NEW_RANK]
    row9 = rows[FIRST_NONUNIFORM_RANK - FIRST_NEW_RANK]
    return {
        "derived_arithmetic": {
            "R_equals_n_minus_k": R == N - K,
            "j_equals_n_minus_A": J == N - A,
            "Delta0_equals_R_minus_j_equals_A_minus_k": (
                DELTA_ZERO == R - J == A - K
            ),
            "B_star_equals_U_paid_plus_B_remaining": (
                B_STAR == U_PAID + B_REMAINING
            ),
            "carrier_minimum_excess": MIN_GLOBAL_UNPAID_EXCESS,
            "carrier_minimum_size": R + MIN_GLOBAL_UNPAID_EXCESS,
            "carrier_maximum_size": N,
        },
        "rank4_anchor": {
            "binom_67475_3": row4["multiplicity_binomial"],
            "mu_4": row4["mu_s"],
            "cap_4": row4["cap_B_s"],
            "cap_4_less_than_2_pow_36": int(row4["cap_B_s"]) < (1 << 36),
            "cap_4_fits": row4["fits_remaining_budget"],
        },
        "rank8_boundary": {
            "cap_8": row8["cap_B_s"],
            "conditional_total": row8[
                "conditional_total_with_paid_baseline"
            ],
            "margin": row8["margin_to_B_star"],
            "fits": row8["fits_remaining_budget"],
        },
        "rank9_boundary": {
            "cap_9": row9["cap_B_s"],
            "shortfall": str(-int(row9["margin_to_B_star"])),
            "uniform_worst_case_fits": row9["fits_remaining_budget"],
            "ell_1_largest_paid_carrier": 1_699_344,
            "ell_1_cap_at_boundary": str(rank9_actual_cap(1_699_344, 1)),
            "ell_1_cap_after_boundary": str(rank9_actual_cap(1_699_345, 1)),
            "ell_7_cap_at_full_domain": str(rank9_actual_cap(N, 7)),
            "ell_7_pays_full_domain": rank9_actual_cap(N, 7) <= B_REMAINING,
        },
        "integer_arithmetic_only": True,
        "deployed_field_enumeration": False,
        "sage_control_expected_schema": (
            "rs-mca-m1-kb-branch3-actual-core-mds-v1-sage-control"
        ),
    }


def expected_ledger() -> dict[str, Any]:
    ladder = expected_rank_ladder()
    return {
        "U_paid_before": str(U_PAID),
        "B_remaining_before": str(B_REMAINING),
        "conditional_paid_rank_range": [FIRST_NEW_RANK, LARGEST_PAID_RANK],
        "conditional_worst_rank_cap": ladder["worst_paid_cap"],
        "conditional_worst_total": ladder["worst_paid_conditional_total"],
        "conditional_worst_margin": ladder["worst_paid_margin"],
        "conditional_terminal_proved": True,
        "rank9_joint_terminal_proved": True,
        "rank9_all_carriers_paid_extension_floor": 7,
        "rank9_ell1_largest_paid_carrier": 1_699_344,
        "conditional_terminal_exhaustive_for_deployed_residual": False,
        "packet_banked_charge": "0",
        "actual_core_mds_charge": None,
        "U_paid_after": str(U_PAID),
        "B_remaining_after": str(B_REMAINING),
        "K_rem": K_REM,
        "ledger_consequence": False,
        "branch3_closed": False,
        "U_2": None,
        "U_Q": None,
        "U_A": None,
        "lhs": None,
        "row_complete": False,
        "inequality_status": "UNDECIDED_OPEN_COMPONENTS",
        "next_attack": (
            "COARSE_UNIFORM_INTRINSIC_RANK9_MDS_JOINT_FAILURE_"
            "OR_RANK_AT_LEAST_10_TDD_SPREAD"
        ),
    }


def expected_audit_sections() -> dict[str, Any]:
    return {
        "statement_audited": (
            "PREDECESSOR_COMPLETE_BASIS_CARRIER_IMPLIES_IMPORTED_"
            "ACTUAL_CORE_MDS_CAP_FOR_RANKS_4_TO_8_AND_RANK9_JOINT_CUT"
        ),
        "dependency_status": {
            "complete_selector_and_basis_carrier": "PROVEN_PREDECESSOR",
            "restricted_weighted_RS_MDS_kernel": "PROVEN_DIRECT",
            "actual_core_basis_multiplicity": "IMPORTED_PROVEN_LOCAL_THEOREM",
            "rank_ladder_arithmetic": "PROVEN_EXACT_BIG_INTEGERS",
            "deployed_intrinsic_rank": "UNVERIFIED_NOT_NEEDED_FOR_DICHOTOMY",
            "complete_rank9_payment": "UNPROVEN_PARTIAL_JOINT_CUT_ONLY",
        },
        "parameter_dependence": (
            "FIELD_GENERAL_SPLICE_THEN_EXACT_KOALABEAR_"
            "N_R_J_DELTA0_AND_BUDGET"
        ),
        "layer_cake_dyadic_summability": "NOT_APPLICABLE",
        "moment_markov_chebyshev": "NOT_APPLICABLE",
        "edge_cases": [
            "ONE_COMPLETE_RANK_MINIMIZING_SELECTOR_ONLY",
            "BASIS_CARRIER_IS_EXACT_COMPLETE_UNION_NOT_LOCAL_TRIPLE_UNION",
            "GLOBAL_CARRIER_AND_RANK_MINIMIZERS_NEED_NOT_COINCIDE",
            "TRANSVERSALITY_SUPPORT_IMAGE_PRESERVED_UNDER_RESTRICTION",
            "ELL_Q_LOWER_BOUND_ONE_ONLY",
            "RANK_CAPS_ARE_MUTUALLY_EXCLUSIVE_NOT_ADDITIVE",
            "RANK9_UNIFORM_FAILURE_DOES_NOT_MEAN_EVERY_RANK9_CASE_FAILS",
        ],
        "numerical_evidence": (
            "EXACT_BIG_INTEGER_CERTIFICATE_AND_TINY_GF17_CONTROL_ONLY_"
            "NO_DEPLOYED_FIELD_CENSUS_NO_ASYMPTOTIC_EXTRAPOLATION"
        ),
        "verdict": (
            "GREEN_IMPORTED_SPLICE_RANK4_TO_8_AND_RANK9_JOINT_CUT_"
            "YELLOW_BRANCH3_AND_ROW"
        ),
        "remaining_risks": [
            "RANK9_JOINT_FAILURE_REGION_AND_RANK_AT_LEAST_10_REMAIN_OPEN",
            "NO_DEPLOYED_SELECTOR_CLASSIFICATION_CERTIFICATE",
            "NO_PROVED_EXTENSION_FACTOR_GAIN_BEYOND_ONE",
            "BRANCHES_4_AND_5_U2_UQ_UA_AND_ROW_REMAIN_OPEN",
        ],
    }


def validate_sources() -> None:
    predecessor = load_json(ROOT / PREDECESSOR_CERT_REL)
    require(
        predecessor.get("schema")
        == "rs-mca-m1-kb-branch3-tdd-excess-v1",
        "predecessor schema drift",
    )
    row = predecessor.get("row", {})
    require(
        row.get("n") == N
        and row.get("k") == K
        and row.get("agreement_A") == A
        and row.get("redundancy_R") == R
        and row.get("error_cap_j") == J,
        "predecessor row drift",
    )
    require(
        int(row.get("U_paid", "-1")) == U_PAID
        and int(row.get("B_remaining", "-1")) == B_REMAINING,
        "predecessor budget drift",
    )
    bridge = predecessor.get("defect_span_bridge", {})
    require(
        bridge.get("chosen_selector_attains_intrinsic_minimum") is True
        and bridge.get("kappa_star_ge_11_implies_every_selector_high_union")
        is True
        and bridge.get("rank_identity")
        == "s_star=1+dim(R_sel)_FOR_MINIMIZING_SELECTOR"
        and bridge.get("basis_carrier_equals_complete_selected_union") is True
        and bridge.get("first_unpaid_intrinsic_affine_rank_stratum")
        == FIRST_NEW_RANK,
        "predecessor selector/basis-carrier contract drift",
    )
    ledger = predecessor.get("ledger", {})
    require(
        ledger.get("packet_banked_charge") == "0"
        and ledger.get("branch3_closed") is False
        and ledger.get("row_complete") is False,
        "predecessor ledger state drift",
    )

    predecessor_text = (ROOT / PREDECESSOR_NOTE_REL).read_text(
        encoding="utf-8"
    )
    for anchor in (
        "s_*(\\Gamma)=s(\\sigma_*)=1+\\dim\\mathcal R",
        "V=\\bigcup_{\\eta\\in\\Gamma}E_\\eta",
        "basis carrier consisting of",
        "first unpaid intrinsic affine-rank stratum",
    ):
        require(anchor in predecessor_text, f"predecessor note anchor missing: {anchor}")

    actual_core_text = (ROOT / ACTUAL_CORE_NOTE_REL).read_text(
        encoding="utf-8"
    )
    for anchor in (
        "### Theorem (actual-core basis multiplicity)",
        "K=[N,kappa,R+1] is MDS",
        "sum_gamma mu_gamma<=binom(N,s)",
        "|Z|<=floor(binom(N,s)/mu_q)",
        "ell_q=max(1,d+q-N)",
    ):
        require(anchor in actual_core_text, f"actual-core anchor missing: {anchor}")


def build_certificate() -> dict[str, Any]:
    validate_sources()
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "source_bindings": expected_source_bindings(),
        "row": expected_row(),
        "predecessor_contract": expected_predecessor_contract(),
        "restricted_mds_splice": expected_restricted_mds_splice(),
        "rank_ladder": expected_rank_ladder(),
        "owner_registry": expected_owner_registry(),
        "classifier_contract": expected_classifier_contract(),
        "exact_controls": expected_exact_controls(),
        "charges": [],
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
        "nonclaims": NONCLAIMS,
        "payload_sha256": "",
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def require_exact_keys(
    value: dict[str, Any], expected: set[str], label: str
) -> None:
    require(set(value) == expected, f"{label} keys drift")


def validate_source_bindings(bindings: Any) -> None:
    require(type(bindings) is list, "source_bindings is not a list")
    require(
        canonical_bytes(bindings) == canonical_bytes(expected_source_bindings()),
        "source binding path/hash/role drift",
    )
    seen: set[str] = set()
    for source in bindings:
        require(type(source) is dict, "source binding is not an object")
        require_exact_keys(
            source,
            {"binding_id", "path", "sha256", "role"},
            "source binding",
        )
        require(
            all(
                type(source[key]) is str
                for key in ("binding_id", "path", "sha256", "role")
            ),
            "source binding type drift",
        )
        source_id = source["binding_id"]
        require(source_id not in seen, "duplicate source binding id")
        seen.add(source_id)
        path = Path(source["path"])
        require(
            not path.is_absolute() and ".." not in path.parts,
            "unsafe source path",
        )
        require(
            source["sha256"] == file_hash(path),
            f"source hash drift: {path}",
        )


def validate_certificate(
    artifact: dict[str, Any], *, exact_rebuild: bool = False
) -> None:
    require_exact_keys(artifact, TOP_KEYS, "top-level")
    require(artifact["schema"] == SCHEMA, "schema drift")
    require(artifact["artifact_kind"] == ARTIFACT_KIND, "artifact kind drift")
    require(artifact["status"] == STATUS, "status drift")
    require(
        artifact["payload_sha256"] == payload_hash(artifact),
        "payload hash drift",
    )
    validate_source_bindings(artifact["source_bindings"])

    expected_sections = {
        "row": expected_row(),
        "predecessor_contract": expected_predecessor_contract(),
        "restricted_mds_splice": expected_restricted_mds_splice(),
        "rank_ladder": expected_rank_ladder(),
        "owner_registry": expected_owner_registry(),
        "classifier_contract": expected_classifier_contract(),
        "exact_controls": expected_exact_controls(),
        "charges": [],
        "ledger": expected_ledger(),
        "audit_sections": expected_audit_sections(),
        "nonclaims": NONCLAIMS,
    }
    for key, expected in expected_sections.items():
        require(
            canonical_bytes(artifact[key]) == canonical_bytes(expected),
            f"{key} drift",
        )

    row = artifact["row"]
    require(
        row["redundancy_R"] == row["n"] - row["k"],
        "R=n-k relation drift",
    )
    require(
        row["error_cap_j"] == row["n"] - row["agreement_A"],
        "j=n-A relation drift",
    )
    require(
        row["zero_mask_surplus_Delta0"]
        == row["redundancy_R"] - row["error_cap_j"],
        "Delta0 relation drift",
    )

    ladder = artifact["rank_ladder"]
    rows = ladder["rows"]
    require(
        [item["intrinsic_affine_rank_s"] for item in rows]
        == list(range(FIRST_NEW_RANK, FIRST_NONUNIFORM_RANK + 1)),
        "rank ladder range drift",
    )
    for item in rows:
        s = item["intrinsic_affine_rank_s"]
        expected = rank_row(s)
        require(
            canonical_bytes(item) == canonical_bytes(expected),
            f"rank-{s} arithmetic drift",
        )
    require(
        all(item["fits_remaining_budget"] for item in rows[:-1])
        and rows[-1]["fits_remaining_budget"] is False,
        "uniform rank boundary drift",
    )
    joint_rows = ladder["rank9_joint_boundary"]
    require(len(joint_rows) == 7, "rank-nine joint boundary length drift")
    for joint in joint_rows[:6]:
        require(
            joint["all_carriers_through_n_paid"] is False
            and int(joint["cap_at_largest_paid_carrier"]) <= B_REMAINING
            and int(joint["cap_at_first_unpaid_carrier"]) > B_REMAINING,
            "rank-nine finite carrier boundary drift",
        )
    require(
        joint_rows[-1]["all_carriers_through_n_paid"] is True
        and joint_rows[-1]["largest_paid_carrier_size"] == N
        and int(joint_rows[-1]["cap_at_largest_paid_carrier"])
        <= B_REMAINING,
        "rank-nine extension-seven boundary drift",
    )

    order = artifact["owner_registry"]["first_match_order"]
    require(len(order) == len(set(order)), "duplicate owner in first-match order")
    require(
        order[-1]
        == "UNPAID_BY_COARSE_RANK9_JOINT_OR_RANK_AT_LEAST_10_TDD_SPREAD",
        "primitive residual owner drift",
    )

    classifier = artifact["classifier_contract"]
    require(
        classifier["cases"]["rank_4"]
        == "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK_4_TO_8"
        and classifier["cases"]["rank_8"]
        == "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK_4_TO_8"
        and classifier["cases"]["rank_9"]
        == "UNPAID_BY_COARSE_UNIFORM_RANK9_MDS_JOINT_BOUND"
        and classifier["cases"]["rank_9_small_carrier"]
        == "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK9_JOINT_BOUNDARY"
        and classifier["cases"]["rank_9_extension_7"]
        == "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK9_JOINT_BOUNDARY"
        and classifier["cases"]["rank_10"]
        == "UNPAID_PRIMITIVE_INTRINSIC_RANK_AT_LEAST_10_TDD_SPREAD"
        and classifier["cases"]["nonminimizing_rank_4"]
        == "PAID_ACTUAL_CORE_MDS_INTRINSIC_RANK_4_TO_8"
        and classifier["cases"]["nonminimizing_rank_9_failure"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and classifier["cases"]["nonminimizing_rank_10"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED",
        "classifier rank boundary drift",
    )
    require(
        classifier["cases"]["global_carrier_10"]
        == "PAID_ONE_GLOBAL_CARRIER_EXCESS_LE_10"
        and classifier["cases"]["rank_9_boundary_plus_1"]
        == "UNPAID_BY_COARSE_UNIFORM_RANK9_MDS_JOINT_BOUND",
        "classifier carrier/rank-nine boundary drift",
    )
    for fail_closed_case in (
        "uncertified_global_carrier_10",
        "noncomplete_rank_4",
        "nonminimizing_rank_9_failure",
        "nonminimizing_rank_10",
        "missing_complete_union",
        "missing_transversality",
        "missing_weight_contract",
        "incoherent_selector_data",
        "unmatched_extension_7",
        "missing_rank9_carrier",
        "missing_rank9_extension",
        "minimal_rank4_call",
        "unknown_rank",
        "unknown_carrier_minimum",
    ):
        require(
            classifier["cases"][fail_closed_case]
            == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED",
            f"classifier fail-closed case accepted: {fail_closed_case}",
        )
    require(
        classifier["deployed_terminal"]
        == "UNPAID_INTRINSIC_SELECTOR_CLASSIFICATION_NOT_CERTIFIED"
        and classifier["classifier_banks_unconditional_charge"] is False,
        "deployed classifier fail-closed drift",
    )

    ledger = artifact["ledger"]
    require(
        ledger["packet_banked_charge"] == "0"
        and ledger["actual_core_mds_charge"] is None
        and ledger["U_paid_after"] == ledger["U_paid_before"]
        and ledger["B_remaining_after"] == ledger["B_remaining_before"]
        and ledger["branch3_closed"] is False
        and ledger["row_complete"] is False,
        "fail-closed ledger drift",
    )

    if exact_rebuild:
        expected = build_certificate()
        require(
            canonical_bytes(artifact) == canonical_bytes(expected),
            "certificate is not the exact deterministic rebuild",
        )


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    target = value
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = replacement


def run_tamper_selftest(artifact: dict[str, Any]) -> int:
    mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("schema", ("schema",), SCHEMA + "-bad"),
        ("artifact-kind", ("artifact_kind",), ARTIFACT_KIND + "-bad"),
        ("status", ("status",), STATUS + "-bad"),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
        ("source-path", ("source_bindings", 0, "path"), "../unsafe"),
        (
            "duplicate-binding",
            ("source_bindings", 1, "binding_id"),
            "packet-note",
        ),
        ("row-n", ("row", "n"), N - 1),
        ("row-k", ("row", "k"), K - 1),
        ("row-A", ("row", "agreement_A"), A - 1),
        ("row-R", ("row", "redundancy_R"), R - 1),
        ("row-j", ("row", "error_cap_j"), J - 1),
        ("row-Delta0", ("row", "zero_mask_surplus_Delta0"), DELTA_ZERO - 1),
        ("row-budget", ("row", "B_remaining"), str(B_REMAINING - 1)),
        (
            "predecessor-selector",
            ("predecessor_contract", "rank_minimizing_complete_selector_fixed_before_anchors"),
            False,
        ),
        (
            "predecessor-carrier",
            ("predecessor_contract", "basis_carrier_equals_complete_selected_union"),
            False,
        ),
        (
            "predecessor-transverse",
            ("predecessor_contract", "transverse_actual_witness_contract"),
            False,
        ),
        (
            "mds-range",
            ("restricted_mds_splice", "carrier_excess_range"),
            [10, K],
        ),
        (
            "mds-columns",
            ("restricted_mds_splice", "every_R_columns_independent"),
            False,
        ),
        (
            "mds-kernel",
            ("restricted_mds_splice", "restricted_kernel"),
            "NOT_MDS",
        ),
        (
            "mds-core-rank",
            ("restricted_mds_splice", "actual_core_rank"),
            "r=s_star",
        ),
        (
            "mds-weight-budget",
            ("restricted_mds_splice", "witness_budget_below_redundancy_R"),
            False,
        ),
        (
            "mask-floor",
            ("restricted_mds_splice", "complete_zero_mask_floor"),
            "q=nu+Delta0-1",
        ),
        (
            "ell-gain",
            ("restricted_mds_splice", "only_extension_lower_bound_used"),
            2,
        ),
        (
            "selector-data-coherence",
            (
                "restricted_mds_splice",
                "rank_carrier_lift_values_from_same_selector_and_restriction",
            ),
            False,
        ),
        (
            "rank4-mu",
            ("rank_ladder", "rows", 0, "mu_s"),
            str(int(rank_rows()[0]["mu_s"]) - 1),
        ),
        (
            "rank4-cap",
            ("rank_ladder", "rows", 0, "cap_B_s"),
            str(int(rank_rows()[0]["cap_B_s"]) + 1),
        ),
        (
            "rank8-fit",
            ("rank_ladder", "rows", 4, "fits_remaining_budget"),
            False,
        ),
        (
            "rank9-fit",
            ("rank_ladder", "rows", 5, "fits_remaining_budget"),
            True,
        ),
        (
            "rank-boundary",
            ("rank_ladder", "first_rank_not_uniformly_paid"),
            10,
        ),
        (
            "rank9-carrier-boundary",
            (
                "rank_ladder",
                "rank9_joint_boundary",
                0,
                "largest_paid_carrier_size",
            ),
            1_699_345,
        ),
        (
            "rank9-extension-floor",
            ("rank_ladder", "rank9_all_carriers_paid_extension_floor"),
            6,
        ),
        (
            "rank-sum",
            ("rank_ladder", "rank_caps_are_alternatives_not_a_sum"),
            False,
        ),
        (
            "owner-order",
            ("owner_registry", "first_match_order", 3),
            "UNPAID_BY_COARSE_RANK9_JOINT_OR_RANK_AT_LEAST_10_TDD_SPREAD",
        ),
        (
            "owner-complete",
            ("owner_registry", "actual_core_owner_requires_complete_selector"),
            False,
        ),
        (
            "owner-global",
            ("owner_registry", "actual_core_owner_applies_once_globally"),
            False,
        ),
        (
            "classifier-rank8",
            ("classifier_contract", "cases", "rank_8"),
            "UNPAID",
        ),
        (
            "classifier-rank9",
            ("classifier_contract", "cases", "rank_9"),
            "PAID",
        ),
        (
            "classifier-rank9-boundary",
            ("classifier_contract", "cases", "rank_9_boundary_plus_1"),
            "PAID",
        ),
        (
            "classifier-uncertified-carrier",
            ("classifier_contract", "cases", "uncertified_global_carrier_10"),
            "PAID",
        ),
        (
            "classifier-missing-weight",
            ("classifier_contract", "cases", "missing_weight_contract"),
            "PAID",
        ),
        (
            "classifier-incoherent-data",
            ("classifier_contract", "cases", "incoherent_selector_data"),
            "PAID",
        ),
        (
            "classifier-unmatched-ell",
            ("classifier_contract", "cases", "unmatched_extension_7"),
            "PAID",
        ),
        (
            "classifier-minimal-call",
            ("classifier_contract", "cases", "minimal_rank4_call"),
            "PAID",
        ),
        (
            "classifier-deployed",
            ("classifier_contract", "deployed_complete_selector_certificate_present"),
            True,
        ),
        (
            "rank4-anchor",
            ("exact_controls", "rank4_anchor", "cap_4"),
            "1",
        ),
        (
            "rank9-shortfall",
            ("exact_controls", "rank9_boundary", "shortfall"),
            "0",
        ),
        ("ledger-charge", ("ledger", "packet_banked_charge"), "1"),
        ("ledger-owner-charge", ("ledger", "actual_core_mds_charge"), "1"),
        ("ledger-close", ("ledger", "branch3_closed"), True),
        ("ledger-row", ("ledger", "row_complete"), True),
        ("ledger-next", ("ledger", "next_attack"), "RANK8"),
        (
            "audit-verdict",
            ("audit_sections", "verdict"),
            "GREEN_ROW_CLOSED",
        ),
        ("nonclaim", ("nonclaims", 0), "This packet proves branch 3 closed."),
    ]

    rejected = 0
    for name, path, replacement in mutations:
        candidate = copy.deepcopy(artifact)
        set_path(candidate, path, replacement)
        candidate["payload_sha256"] = payload_hash(candidate)
        try:
            validate_certificate(candidate)
        except VerificationError:
            rejected += 1
            continue
        raise VerificationError(f"tamper accepted: {name}")

    candidate = copy.deepcopy(artifact)
    candidate["unexpected"] = True
    candidate["payload_sha256"] = payload_hash(candidate)
    try:
        validate_certificate(candidate)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: unknown top-level key")

    candidate = copy.deepcopy(artifact)
    candidate["row"]["unexpected"] = True
    candidate["payload_sha256"] = payload_hash(candidate)
    try:
        validate_certificate(candidate)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: unknown nested key")

    bad_payload = copy.deepcopy(artifact)
    bad_payload["payload_sha256"] = "0" * 64
    try:
        validate_certificate(bad_payload)
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: payload hash")

    try:
        parse_json('{"schema":"a","schema":"b"}', "duplicate-control")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: duplicate JSON key")

    try:
        parse_json('{"value":NaN}', "nan-control")
    except VerificationError:
        rejected += 1
    else:
        raise VerificationError("tamper accepted: NaN")

    return rejected


def write_certificate(artifact: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(
        json.dumps(artifact, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    artifact = build_certificate()

    if args.write:
        validate_certificate(artifact, exact_rebuild=True)
        write_certificate(artifact)
        print(f"WROTE {CERT_PATH.relative_to(ROOT)}")
        return 0

    if args.check:
        loaded = load_json(CERT_PATH)
        validate_certificate(loaded, exact_rebuild=True)
        ladder = loaded["rank_ladder"]
        print("PASS m1-kb-branch3-actual-core-mds-v1")
        print(
            "paid intrinsic ranks: %d..%d; worst cap=%s; margin=%s"
            % (
                FIRST_NEW_RANK,
                LARGEST_PAID_RANK,
                ladder["worst_paid_cap"],
                ladder["worst_paid_margin"],
            )
        )
        print(
            "first rank not uniformly paid: %d; worst cap=%s; "
            "ell=1 carrier boundary=%d"
            % (
                FIRST_NONUNIFORM_RANK,
                ladder["rows"][-1]["cap_B_s"],
                ladder["rank9_joint_boundary"][0][
                    "largest_paid_carrier_size"
                ],
            )
        )
        print(
            "ledger: no unconditional charge; U_paid=%d; B_remaining=%d"
            % (U_PAID, B_REMAINING)
        )
        return 0

    rejected = run_tamper_selftest(artifact)
    print(f"PASS tamper-selftest: {rejected}/{rejected} mutations rejected")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
