#!/usr/bin/env python3
"""Replay the 75-row ledger for the frozen ``(3,2,1)`` CRT packet.

The existing-owner certificate leaves all 1,152 aggregate cofactor-support
keys unpaid.  The total-degree-six reduced-CRT packet gives each such key a
candidate charge one.  This verifier reconstructs the exact post-#801 ledger,
replaces only the named ``d=3,r=1`` row, and recomputes the complete totals.

The generated certificate mirrors the linked CRT packet's content-addressed
review gate: it remains unbanked until both declared reviews authorize the
lemma, and it becomes banked only after the gate is satisfied.  Candidate
arithmetic is never itself treated as review authorization.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Iterable

from verify_l1_b9_d4r0_shared_auxiliary_ledger import (
    UNRESOLVED_ROUTES,
    apply_shared_scope as apply_d4r0_scope,
    current_post_41331_rows,
    is_shared_scope as is_d4r0_scope,
)


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIR = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31321-total-degree-crt"
)
CERTIFICATE_PATH = CERTIFICATE_DIR / "ledger_certificate.json"
CRT_CERTIFICATE_PATH = CERTIFICATE_DIR / "certificate.json"
OWNER_CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-frontier-31321-owner-partition/certificate.json"
)
PRIOR_LEDGER_PATH = (
    ROOT
    / "experimental/data/certificates/l1-b9-d4r0-shared-auxiliary/ledger_certificate.json"
)
INDEPENDENT_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_frontier_31321_total_degree_crt_final_package_independent_review.md"
)
CROSS_MODEL_REVIEW_PATH = (
    ROOT
    / "experimental/notes/l1/reviews/l1_b9_frontier_31321_total_degree_crt_final_package_cross_model_review.md"
)

OWNER_ID = "B9_FRONTIER_31321_TOTAL_DEGREE_SIX_REDUCED_CRT"
EXPECTED_PROFILE = {
    "ell": 4,
    "d": 3,
    "r": 1,
    "t": 3,
    "a_i": [3, 2, 1],
    "G2": 3,
    "GR": 4,
    "lambda": 0,
    "lambda_J": 1,
    "lambda_minus_lambda_J": -1,
    "d_minus_ell": -1,
}
EXPECTED_NEXT_PROFILE = {
    "ell": 4,
    "d": 4,
    "r": 2,
    "t": 2,
    "a_i": [3, 3],
    "G2": 2,
    "GR": 3,
    "support_pattern_count": 48,
    "refined_injection_exponent": 2,
    "refined_injection_bound": 17_328,
}


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_json(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def render_certificate_json(report: dict[str, object]) -> str:
    """Pretty-print metadata with one complete canonical owner per line."""
    marker = "__RS_MCA_31321_CANONICAL_OWNER_ROWS__"
    rows = report["pattern_owners"]
    compact = copy.deepcopy(report)
    compact["pattern_owners"] = marker
    rendered = json.dumps(compact, indent=2, sort_keys=True)
    needle = f'  "pattern_owners": "{marker}"'
    if rendered.count(needle) != 1:
        raise RuntimeError("hybrid certificate marker drift")
    row_block = (
        '  "pattern_owners": [\n'
        + ",\n".join(
            "    " + json.dumps(row, sort_keys=True, separators=(",", ":"))
            for row in rows
        )
        + "\n  ]"
    )
    rendered = rendered.replace(needle, row_block) + "\n"
    if json.loads(rendered) != report:
        raise RuntimeError("hybrid certificate round-trip failed")
    return rendered


def target_row(row: dict[str, object]) -> bool:
    return (
        int(row["d"]) - int(row["d_minus_ell"]) == 4
        and int(row["d"]) == 3
        and int(row["r"]) == 1
        and int(row["t"]) == 3
        and row["a_i"] == [3, 2, 1]
        and int(row["G2"]) == 3
        and int(row["GR"]) == 4
        and int(row["lambda"]) == 0
        and int(row["lambda_J"]) == 1
        and int(row["lambda_minus_lambda_J"]) == -1
    )


def canonical_assignment(pattern: dict[str, object]) -> dict[str, object]:
    return {
        "background_support": list(pattern["background_support"]),
        "petal_size_assignment": list(pattern["petal_size_assignment"]),
        "petal_supports": [list(support) for support in pattern["petal_supports"]],
        "selected_cofactor_support": list(pattern["selected_cofactor_support"]),
        "selected_cofactor_support_mask": int(
            pattern["selected_cofactor_support_mask"]
        ),
    }


def crt_canonical_key(pattern: dict[str, object]) -> dict[str, object]:
    """Normalize an owner row to the key emitted by the Sage CRT census."""
    return {
        "background_support": list(pattern["background_support"]),
        "petal_size_assignment": list(pattern["petal_size_assignment"]),
        "petal_supports": [list(support) for support in pattern["petal_supports"]],
    }


def canonical_set_sha256(rows: list[dict[str, object]]) -> str:
    ordered = sorted(
        rows,
        key=lambda row: json.dumps(row, sort_keys=True, separators=(",", ":")),
    )
    return sha256_json(ordered)


def largest_row_record(row: dict[str, object]) -> dict[str, object]:
    return {
        "ell": int(row["d"]) - int(row["d_minus_ell"]),
        **{
            key: row[key]
            for key in (
                "d",
                "r",
                "t",
                "a_i",
                "d_minus_ell",
                "G2",
                "GR",
                "lambda",
                "lambda_J",
                "lambda_minus_lambda_J",
                "support_pattern_count",
                "refined_injection_exponent",
                "refined_injection_bound",
                "b11_box_route",
            )
        },
    }


def current_post_d4r0_rows() -> list[dict[str, object]]:
    """Reconstruct and authenticate the exact banked PR #801 ledger."""
    prior = load_json(PRIOR_LEDGER_PATH)
    rows = [
        apply_d4r0_scope(row) if is_d4r0_scope(row) else dict(row)
        for row in current_post_41331_rows()
    ]
    candidate = prior["ledger_consequence"]["candidate_result"]
    unresolved = [
        row for row in rows if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    matches = [row for row in rows if target_row(row)]
    if not (
        prior["schema"]
        == "rs-mca-l1-b9-d4r0-shared-auxiliary-ledger-v1"
        and prior["status"]
        == "EXACT_D4R0_SHARED_ENVELOPE_REPLAY_FRESH_REVIEWS_GREEN"
        and prior["verdict"]
        == "GREEN_LOCAL_D4R0_SHARED_AUXILIARY_LEDGER_BANKED"
        and prior["ledger_consequence"]["banked"] is True
        and len(rows) == 75
        and len(matches) == 1
        and int(matches[0]["support_pattern_count"]) == 1_152
        and int(matches[0]["refined_injection_exponent"]) == 1
        and int(matches[0]["refined_injection_bound"]) == 21_888
        and sum(int(row["refined_injection_bound"]) for row in rows)
        == 641_512
        and sum(int(row["refined_injection_bound"]) for row in unresolved)
        == 104_914
        and candidate["all_profile_bound"] == 641_512
        and candidate["unresolved_bound"] == 104_914
        and sha256_json(rows) == candidate["profile_sha256"]
    ):
        raise RuntimeError("post-#801 d4r0 ledger reconstruction drift")
    return rows


def validate_owner_certificate(owner: dict[str, object]) -> None:
    patterns = owner["patterns"]
    assignments = [canonical_assignment(pattern) for pattern in patterns]
    result = owner["result"]
    consequence = owner["ledger_consequence"]
    previous = owner["previous_ledger"]
    if not (
        owner["schema"]
        == "rs-mca-l1-b9-frontier-31321-owner-partition-v1"
        and owner["status"] == "AUDIT/EXACT_GF19_EXISTING_OWNER_PARTITION"
        and owner["verdict"].startswith("YELLOW - all 1,152 aggregate keys")
        and previous["path"] == str(PRIOR_LEDGER_PATH.relative_to(ROOT))
        and previous["sha256"] == sha256_file(PRIOR_LEDGER_PATH)
        and previous["banked"] is True
        and previous["all_profile_bound"] == 641_512
        and previous["unresolved_bound"] == 104_914
        and len(patterns) == 1_152
        and len({pattern["pattern_id"] for pattern in patterns}) == 1_152
        and len({sha256_json(assignment) for assignment in assignments}) == 1_152
        and len(
            {
                int(assignment["selected_cofactor_support_mask"])
                for assignment in assignments
            }
        )
        == 1_152
        and all(pattern["owner"] == "UNPAID_PRIMITIVE" for pattern in patterns)
        and all(
            pattern["profile"]
            == {
                "G2": 3,
                "GR": 4,
                "a_i": [3, 2, 1],
                "d": 3,
                "ell": 4,
                "lambda": 0,
                "lambda_J": 1,
                "r": 1,
                "t": 3,
            }
            for pattern in patterns
        )
        and result["support_pattern_count"] == 1_152
        and result["unpaid_primitive_patterns"] == 1_152
        and result["paid_existing_owner_patterns"] == 0
        and result["restored_core_refinement_count"] == 4_608
        and result["periodic_full_support_refinement_count"] == 12
        and result["patterns_with_periodic_full_support_refinement"] == 12
        and consequence["old_profile_charge"] == 21_888
        and consequence["residual_profile_charge"] == 21_888
        and consequence["paid_mass_removed"] == 0
        and consequence["new_all_profile_bound"] == 641_512
        and consequence["new_unresolved_bound"] == 104_914
    ):
        raise RuntimeError("31321 existing-owner certificate linkage failed")


def review_file_record(path: Path) -> dict[str, object]:
    exists = path.exists()
    content = path.read_text(encoding="utf-8") if exists else ""
    row: dict[str, object] = {
        "path": str(path.relative_to(ROOT)),
        "exists": exists,
        "verdict_green": any(
            line.strip() == "Verdict: GREEN" for line in content.splitlines()
        ),
        "ledger_authorization_yes": any(
            line.strip() == "Ledger authorization: YES"
            for line in content.splitlines()
        ),
    }
    if exists:
        row["sha256"] = sha256_file(path)
    return row


def expected_review_gate() -> dict[str, object]:
    reviews = {
        "independent_review": review_file_record(INDEPENDENT_REVIEW_PATH),
        "cross_model_review": review_file_record(CROSS_MODEL_REVIEW_PATH),
    }
    satisfied = all(
        row["exists"]
        and row["verdict_green"]
        and row["ledger_authorization_yes"]
        for row in reviews.values()
    )
    present_count = sum(bool(row["exists"]) for row in reviews.values())
    status = (
        "SATISFIED_TWO_HASH_LINKED_GREEN_REVIEWS"
        if satisfied
        else (
            "PRESENT_BUT_NOT_GREEN"
            if present_count == len(reviews)
            else "PENDING_REQUIRED_REVIEW_FILES"
        )
    )
    return {
        "required_review_count": 2,
        "reviews": reviews,
        "satisfied": satisfied,
        "status": status,
    }


def validate_crt_certificate(crt: dict[str, object]) -> None:
    frozen = crt["frozen_system"]
    parameters = crt["parameters"]
    exact = crt["exact_GF19"]
    proof = crt["proof_certificate"]
    banked = bool(crt["ledger_consequence"]["banked"])
    verdict = str(crt["verdict"])
    review_gate = expected_review_gate()
    expected_status = (
        "PROVED_LOCAL_ALGEBRA_EXACT_GF19_CONTROL_FRESH_REVIEWS_GREEN"
        if banked
        else "PROVED_LOCAL_ALGEBRA_EXACT_GF19_CONTROL_PENDING_FRESH_REVIEW"
    )
    expected_verdict = (
        "GREEN_LOCAL_31321_LEMMA_LEDGER_AUTHORIZED"
        if banked
        else "YELLOW_LOCAL_PACKET_PENDING_FRESH_INDEPENDENT_REVIEW"
    )
    expected_authorization = (
        "YES_TWO_HASH_LINKED_GREEN_REVIEWS"
        if banked
        else "NO_PENDING_TWO_HASH_LINKED_GREEN_REVIEWS"
    )
    owner_patterns = load_json(OWNER_CERTIFICATE_PATH)["patterns"]
    owner_key_hash = canonical_set_sha256(
        [crt_canonical_key(pattern) for pattern in owner_patterns]
    )
    if not (
        crt["schema"] == "rs-mca-l1-b9-frontier-31321-total-degree-crt-v1"
        and crt["status"] == expected_status
        and parameters["labels"] == [1, 2, 3]
        and parameters["label_hypothesis"] == "pairwise distinct and nonzero"
        and parameters["core_size"] == 4
        and parameters["support_locator_degrees_sorted"] == [3, 2, 1]
        and parameters["quotient_degrees_for_sorted_supports"] == [0, 1, 2]
        and parameters["support_locator_hypotheses"]
        == (
            "B1,B2,B3 are monic, positive-degree, pairwise coprime, and "
            "each is coprime to R"
        )
        and parameters["profile_bridge_hypotheses"]
        == [
            "the core, background, and labelled selected petal supports are pairwise disjoint",
            "the received word is zero on the core and retained background point",
            "the received word on labelled petal i is c_i*L_C",
            "the exact profile has one restored core agreement and one retained background agreement",
        ]
        and parameters["bridge_hypotheses"]
        == [
            "C consists of four distinct field points",
            "h is in C and D=C\\{h}",
            "F=L_D is monic, split, and squarefree",
            "gcd(R,L_C)=1",
            "the received word is zero on C and at the root of R",
            "H=L_C/F=X-h and W=R*H*V",
        ]
        and frozen["fixed_F_matrix_shape"] == [12, 9]
        and frozen["universal_fixed_rank"] == 9
        and frozen["moving_monic_F_matrix_shape"] == [12, 12]
        and frozen["reduced_affine_map_shape"] == [3, 3]
        and frozen["compatibility_degrees"] == [3, 4, 5]
        and exact["support_pattern_count"] == 1_152
        and exact["canonical_assignment_count"] == 1_152
        and exact["canonical_assignment_set_sha256"] == owner_key_hash
        and exact["fixed_matrix_rank_histogram"] == {"9": 1_152}
        and exact["moving_rank_histogram"]
        == {"rankC=11,rankAug=12": 44, "rankC=12,rankAug=12": 1_108}
        and exact["reduced_rank_histogram"]
        == {"rankM=2,rankAug=3": 44, "rankM=3,rankAug=3": 1_108}
        and exact["monic_solution_count_histogram"] == {"0": 44, "1": 1_108}
        and exact["compatible_rankdrop_pattern_count"] == 0
        and exact["compatible_rankdrop_zero_gcd_count"] == 0
        and exact["actual_rankdrop_bridge_failure_count"] == 0
        and exact["transcript_sha256"]
        == "2256ea69620c10d5c15012df4ebce046babaaa3e314b948221eeb3107ad80972"
        and proof["fixed_rank_nine"] is True
        and proof["full_rank_bound_per_key"] == 1
        and proof["compatible_rankdrop_gcd_positive"] is True
        and proof["exact_d3_migration_under_bridge"] is True
        and crt["pointwise_bridge_certificate"][
            "validator_accepts_positive_control"
        ]
        is True
        and crt["ledger_consequence"]["candidate_prior_charge"] == 21_888
        and crt["ledger_consequence"][
            "candidate_replacement_charge_after_fresh_green_review"
        ]
        == 1_152
        and crt["ledger_consequence"]["candidate_support_pattern_count"]
        == 1_152
        and crt["fresh_review_gate"] == review_gate
        and banked == bool(review_gate["satisfied"])
        and crt["ledger_consequence"]["authorization"]
        == expected_authorization
        and verdict == expected_verdict
    ):
        raise RuntimeError("31321 total-degree CRT certificate linkage failed")


def linked_inputs() -> tuple[dict[str, object], bool, str]:
    owner = load_json(OWNER_CERTIFICATE_PATH)
    crt = load_json(CRT_CERTIFICATE_PATH)
    current_post_d4r0_rows()
    validate_owner_certificate(owner)
    validate_crt_certificate(crt)
    paths = {
        "prior_banked_ledger": PRIOR_LEDGER_PATH,
        "existing_owner_partition": OWNER_CERTIFICATE_PATH,
        "total_degree_crt": CRT_CERTIFICATE_PATH,
    }
    documents = {
        "prior_banked_ledger": load_json(PRIOR_LEDGER_PATH),
        "existing_owner_partition": owner,
        "total_degree_crt": crt,
    }
    links = {
        name: {
            "path": str(path.relative_to(ROOT)),
            "schema": documents[name]["schema"],
            "sha256": sha256_file(path),
        }
        for name, path in paths.items()
    }
    banked = bool(crt["ledger_consequence"]["banked"])
    if banked:
        for name, path in (
            ("fresh_independent_review", INDEPENDENT_REVIEW_PATH),
            ("fresh_cross_model_review", CROSS_MODEL_REVIEW_PATH),
        ):
            links[name] = {
                "path": str(path.relative_to(ROOT)),
                "review_status": "GREEN_LEDGER_AUTHORIZED",
                "sha256": sha256_file(path),
            }
    return links, banked, str(crt["verdict"])


def apply_candidate_owner(row: dict[str, object], banked: bool) -> dict[str, object]:
    updated = dict(row)
    updated.update(
        {
            "prior_refined_owner": row["refined_owner"],
            "prior_refined_injection_exponent": int(
                row["refined_injection_exponent"]
            ),
            "prior_refined_injection_bound": int(row["refined_injection_bound"]),
            "refined_owner": OWNER_ID,
            "refined_injection_exponent": 0,
            "refined_injection_bound": 1_152,
            "full_rank_monic_cubic_charge": 1_152,
            "compatible_rankdrop_exact_d3_charge": 0,
            "restored_core_multiplier_applied": 1,
            "periodic_refinement_subtraction": 0,
            "review_status": (
                "BANKED_FRESH_REVIEWS_GREEN"
                if banked
                else "CANDIDATE_PENDING_FRESH_REVIEWS"
            ),
        }
    )
    return updated


def build_report() -> dict[str, object]:
    links, banked, crt_verdict = linked_inputs()
    owner = load_json(OWNER_CERTIFICATE_PATH)
    prior_rows = current_post_d4r0_rows()
    matches = [row for row in prior_rows if target_row(row)]
    if len(matches) != 1:
        raise RuntimeError(f"expected one frozen target row, found {len(matches)}")
    old_row = matches[0]

    source_assignments = [
        canonical_assignment(pattern) for pattern in owner["patterns"]
    ]
    crt_key_hash = canonical_set_sha256(
        [crt_canonical_key(pattern) for pattern in owner["patterns"]]
    )
    if len({sha256_json(assignment) for assignment in source_assignments}) != 1_152:
        raise RuntimeError("owner source contains duplicate canonical assignments")
    promotion_status = (
        "BANKED_FRESH_REVIEWS_GREEN"
        if banked
        else "CANDIDATE_PENDING_FRESH_REVIEWS"
    )
    pattern_owners = [
        {
            "pattern_id": pattern["pattern_id"],
            "canonical_assignment": canonical_assignment(pattern),
            "prior_existing_owner": pattern["owner"],
            "owner": OWNER_ID,
            "charge": 1,
            "unpaid_primitive": False,
            "promotion_status": promotion_status,
        }
        for pattern in owner["patterns"]
    ]

    candidate_rows = [
        apply_candidate_owner(row, banked) if row is old_row else dict(row)
        for row in prior_rows
    ]
    candidate_matches = [row for row in candidate_rows if target_row(row)]
    if len(candidate_matches) != 1:
        raise RuntimeError("candidate target replacement multiplicity drift")
    candidate_target = candidate_matches[0]
    prior_unresolved = [
        row for row in prior_rows if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    candidate_unresolved = [
        row
        for row in candidate_rows
        if row["b11_box_route"] in UNRESOLVED_ROUTES
    ]
    candidate_unresolved.sort(
        key=lambda row: int(row["refined_injection_bound"]), reverse=True
    )
    prior_all = sum(int(row["refined_injection_bound"]) for row in prior_rows)
    prior_unresolved_total = sum(
        int(row["refined_injection_bound"]) for row in prior_unresolved
    )
    candidate_all = sum(
        int(row["refined_injection_bound"]) for row in candidate_rows
    )
    candidate_unresolved_total = sum(
        int(row["refined_injection_bound"]) for row in candidate_unresolved
    )
    if not (
        len(candidate_rows) == 75
        and prior_all == 641_512
        and prior_unresolved_total == 104_914
        and candidate_all == 620_776
        and candidate_unresolved_total == 84_178
        and int(candidate_target["refined_injection_bound"]) == 1_152
        and int(candidate_target["refined_injection_exponent"]) == 0
    ):
        raise RuntimeError("31321 candidate ledger total drift")
    next_largest = largest_row_record(candidate_unresolved[0])
    if any(next_largest[key] != value for key, value in EXPECTED_NEXT_PROFILE.items()):
        raise RuntimeError("31321 dynamic next-largest row drift")

    return {
        "schema": "rs-mca-l1-b9-frontier-31321-total-degree-crt-ledger-v1",
        "status": (
            "EXACT_BANKED_LEDGER_REPLAY_FRESH_REVIEWS_GREEN"
            if banked
            else "EXACT_CANDIDATE_LEDGER_REPLAY_PENDING_FRESH_REVIEWS"
        ),
        "statement": (
            "the total-degree-six reduced-CRT candidate replaces the aggregate "
            "q charge by one on each of 1,152 canonical cofactor-support keys"
        ),
        "profile": EXPECTED_PROFILE,
        "component_partition": [
            {
                "component": "fixed-F CRT interpolation",
                "matrix_shape": [12, 9],
                "rank": 9,
                "role": "UNIVERSAL_LEFT_KERNEL_HAS_DIMENSION_THREE",
            },
            {
                "component": "rank(M)=3 for the reduced affine map",
                "reduced_affine_map_shape": [3, 3],
                "owner": "TOTAL_DEGREE_SIX_FULL_RANK_MONIC_UNIQUENESS",
                "bound_per_canonical_key": 1,
            },
            {
                "component": "rank(M)<3 and rank([M|-u])>rank(M)",
                "owner": "EMPTY_AFFINE_INCONSISTENT",
                "bound_per_canonical_key": 0,
            },
            {
                "component": "rank(M)<3 and rank([M|-u])=rank(M)",
                "algebraic_classification": "NONCONSTANT_GCD_PROVED",
                "owner": "EMPTY_EXACT_D3_BY_MISSED_CORE_MIGRATION",
                "bound_per_canonical_key": 0,
            },
        ],
        "aggregate_key_semantics": {
            "canonical_key_count": 1_152,
            "canonical_key_set_sha256": crt_key_hash,
            "restored_core_refinement_count": 4_608,
            "restored_core_multiplier_applied": 1,
            "periodic_full_support_refinement_count": 12,
            "periodic_refinements_subtracted_from_aggregate_charge": 0,
            "reason": (
                "the reduced-CRT injection is by aggregate cofactor-support "
                "key; no factor four and no periodic-refinement subtraction"
            ),
        },
        "pattern_owners": pattern_owners,
        "pattern_owner_sha256": sha256_json(pattern_owners),
        "result": {
            "support_pattern_count": 1_152,
            "owner_histogram": {OWNER_ID: 1_152},
            "unpaid_primitive_patterns": 0,
            "prior_profile_charge": 21_888,
            "candidate_profile_charge": 1_152,
            "candidate_saved_mass": 20_736,
            "candidate_change": -20_736,
        },
        "ledger_consequence": {
            "prior_all_profile_bound": prior_all,
            "prior_unresolved_bound": prior_unresolved_total,
            "prior_profile_sha256": sha256_json(prior_rows),
            "candidate_result": {
                "all_profile_bound": candidate_all,
                "unresolved_bound": candidate_unresolved_total,
                "profile_sha256": sha256_json(candidate_rows),
                "largest_remaining_unresolved_profile": next_largest,
            },
            "banked": banked,
            "closure_verdict": "POSITIVE_UNRESOLVED_MASS_REMAINS",
        },
        "promotion_gate": {
            "crt_packet_verdict": crt_verdict,
            "fresh_independent_review": (
                "LINKED_GREEN_IN_CRT_CERTIFICATE" if banked else "PENDING"
            ),
            "fresh_cross_model_review": (
                "LINKED_GREEN_IN_CRT_CERTIFICATE" if banked else "PENDING"
            ),
            "ledger_authorization": "YES" if banked else "NO_PENDING_REVIEW",
            "review_hashes_required_before_bank": True,
            "banked": banked,
        },
        "linked_inputs": links,
        "proof_status": {
            "exact": [
                "the banked post-#801 75-row ledger and profile hash are replayed",
                "all 1,152 existing-owner keys survive to the algebraic packet",
                "all canonical assignments are unique independently of pattern identifiers",
                "the 12x9 rank-nine and reduced 3x3 dimensions are linked to the CRT certificate",
                "each candidate key receives charge one and rank drop receives exact-d3 charge zero",
                "the all-profile and unresolved totals are recomputed from all 75 rows",
                "the next largest unresolved row is selected dynamically",
                "the prior ledger, owner partition, and CRT packet are hash-linked",
            ],
            "review_gate": (
                "satisfied and banked" if banked else "pending; candidate only"
            ),
        },
        "nonclaims": [
            "candidate arithmetic is not a banked theorem before fresh reviews",
            "the twelve periodic full-support refinements are not subtracted",
            "no restored-core factor four is applied",
            "the charge applies only to the frozen named profile",
            "no global mixed-petal theorem, m>2, PR #763, or Lean claim is made",
        ],
        "verdict": (
            "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED"
            if banked
            else "YELLOW_CANDIDATE_LEDGER_REFINEMENT_PENDING_FRESH_REVIEWS"
        ),
    }


def validate_report(report: dict[str, object]) -> bool:
    try:
        expected = build_report()
        owners = report["pattern_owners"]
        source = load_json(OWNER_CERTIFICATE_PATH)["patterns"]
        source_assignments = [canonical_assignment(pattern) for pattern in source]
        observed_assignments = [entry["canonical_assignment"] for entry in owners]
        component = report["component_partition"]
        aggregate = report["aggregate_key_semantics"]
        result = report["result"]
        ledger = report["ledger_consequence"]
        candidate = ledger["candidate_result"]
        largest = candidate["largest_remaining_unresolved_profile"]
        promotion = report["promotion_gate"]
        banked = bool(ledger["banked"])
        return (
            report == expected
            and report["schema"]
            == "rs-mca-l1-b9-frontier-31321-total-degree-crt-ledger-v1"
            and report["profile"] == EXPECTED_PROFILE
            and len(owners) == 1_152
            and len({entry["pattern_id"] for entry in owners}) == 1_152
            and observed_assignments == source_assignments
            and len({sha256_json(value) for value in observed_assignments}) == 1_152
            and all(
                entry["prior_existing_owner"] == "UNPAID_PRIMITIVE"
                and entry["owner"] == OWNER_ID
                and int(entry["charge"]) == 1
                and not bool(entry["unpaid_primitive"])
                for entry in owners
            )
            and report["pattern_owner_sha256"] == sha256_json(owners)
            and component[0]["matrix_shape"] == [12, 9]
            and component[0]["rank"] == 9
            and component[1]["reduced_affine_map_shape"] == [3, 3]
            and component[1]["bound_per_canonical_key"] == 1
            and component[3]["owner"]
            == "EMPTY_EXACT_D3_BY_MISSED_CORE_MIGRATION"
            and aggregate["canonical_key_count"] == 1_152
            and aggregate["canonical_key_set_sha256"]
            == canonical_set_sha256([crt_canonical_key(pattern) for pattern in source])
            and aggregate["restored_core_refinement_count"] == 4_608
            and aggregate["restored_core_multiplier_applied"] == 1
            and aggregate["periodic_full_support_refinement_count"] == 12
            and aggregate["periodic_refinements_subtracted_from_aggregate_charge"]
            == 0
            and result["prior_profile_charge"] == 21_888
            and result["candidate_profile_charge"] == 1_152
            and result["candidate_saved_mass"] == 20_736
            and ledger["prior_all_profile_bound"] == 641_512
            and ledger["prior_unresolved_bound"] == 104_914
            and candidate["all_profile_bound"] == 620_776
            and candidate["unresolved_bound"] == 84_178
            and all(largest[key] == value for key, value in EXPECTED_NEXT_PROFILE.items())
            and promotion["banked"] is banked
            and promotion["ledger_authorization"]
            == ("YES" if banked else "NO_PENDING_REVIEW")
            and (
                (
                    banked
                    and report["verdict"] == "GREEN_LOCAL_LEDGER_REFINEMENT_BANKED"
                    and report["status"]
                    == "EXACT_BANKED_LEDGER_REPLAY_FRESH_REVIEWS_GREEN"
                )
                or (
                    not banked
                    and report["verdict"]
                    == "YELLOW_CANDIDATE_LEDGER_REFINEMENT_PENDING_FRESH_REVIEWS"
                    and report["status"]
                    == "EXACT_CANDIDATE_LEDGER_REPLAY_PENDING_FRESH_REVIEWS"
                    and promotion["fresh_independent_review"] == "PENDING"
                    and promotion["fresh_cross_model_review"] == "PENDING"
                )
            )
        )
    except (KeyError, RuntimeError, TypeError, ValueError):
        return False


def tamper_selftest(report: dict[str, object]) -> int:
    mutations: list[tuple[str, dict[str, object]]] = []

    changed = copy.deepcopy(report)
    changed["pattern_owners"][1]["canonical_assignment"] = copy.deepcopy(
        changed["pattern_owners"][0]["canonical_assignment"]
    )
    changed["pattern_owners"][1]["pattern_id"] = "fresh-id-duplicate-assignment"
    changed["pattern_owner_sha256"] = sha256_json(changed["pattern_owners"])
    mutations.append(("duplicate_canonical_key", changed))

    changed = copy.deepcopy(report)
    changed["profile"]["r"] = 2
    mutations.append(("target_profile_scope", changed))

    changed = copy.deepcopy(report)
    changed["pattern_owners"][0]["charge"] = 4
    changed["pattern_owner_sha256"] = sha256_json(changed["pattern_owners"])
    mutations.append(("restored_core_factor", changed))

    changed = copy.deepcopy(report)
    changed["aggregate_key_semantics"][
        "periodic_refinements_subtracted_from_aggregate_charge"
    ] = 12
    mutations.append(("periodic_subtraction", changed))

    changed = copy.deepcopy(report)
    changed["aggregate_key_semantics"]["canonical_key_set_sha256"] = "0" * 64
    mutations.append(("canonical_key_set", changed))

    changed = copy.deepcopy(report)
    changed["component_partition"][0]["rank"] = 8
    mutations.append(("fixed_rank", changed))

    changed = copy.deepcopy(report)
    changed["component_partition"][0]["matrix_shape"] = [12, 10]
    mutations.append(("fixed_matrix_dimension", changed))

    changed = copy.deepcopy(report)
    changed["component_partition"][1]["reduced_affine_map_shape"] = [3, 4]
    mutations.append(("reduced_matrix_dimension", changed))

    changed = copy.deepcopy(report)
    changed["component_partition"][3]["owner"] = "UNPAID_PRIMITIVE"
    mutations.append(("rankdrop_component", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["prior_banked_ledger"]["sha256"] = "0" * 64
    mutations.append(("prior_ledger_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["existing_owner_partition"]["sha256"] = "0" * 64
    mutations.append(("owner_partition_link", changed))

    changed = copy.deepcopy(report)
    changed["linked_inputs"]["total_degree_crt"]["sha256"] = "0" * 64
    mutations.append(("crt_certificate_link", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"]["all_profile_bound"] += 1
    mutations.append(("all_profile_total", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"]["unresolved_bound"] -= 1
    mutations.append(("unresolved_total", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["candidate_result"][
        "largest_remaining_unresolved_profile"
    ]["refined_injection_bound"] = 21_888
    mutations.append(("next_largest_row", changed))

    changed = copy.deepcopy(report)
    changed["ledger_consequence"]["banked"] = not bool(
        changed["ledger_consequence"]["banked"]
    )
    mutations.append(("banked_status", changed))

    changed = copy.deepcopy(report)
    changed["promotion_gate"]["fresh_independent_review"] = "GREEN"
    mutations.append(("review_status", changed))

    for link_name in (
        "fresh_independent_review",
        "fresh_cross_model_review",
    ):
        if link_name not in report["linked_inputs"]:
            continue
        changed = copy.deepcopy(report)
        changed["linked_inputs"][link_name]["sha256"] = "0" * 64
        mutations.append((f"{link_name}_link", changed))

    failed = False
    for name, mutation in mutations:
        caught = not validate_report(mutation)
        print(f"  tamper {name:<28}: {'CAUGHT' if caught else 'MISSED'}")
        failed |= not caught

    forged_crt = load_json(CRT_CERTIFICATE_PATH)
    if forged_crt["ledger_consequence"]["banked"]:
        forged_crt["fresh_review_gate"]["satisfied"] = False
    else:
        forged_crt["ledger_consequence"]["banked"] = True
    try:
        validate_crt_certificate(forged_crt)
        forged_caught = False
    except RuntimeError:
        forged_caught = True
    print(
        "  tamper forged_banked_crt          : "
        f"{'CAUGHT' if forged_caught else 'MISSED'}"
    )
    failed |= not forged_caught
    print(f"TAMPER-SELFTEST: {'FAIL' if failed else 'PASS'}")
    return 1 if failed else 0


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(list(argv))

    report = build_report()
    if not validate_report(report):
        raise RuntimeError("internally generated 31321 ledger failed validation")
    if args.tamper_selftest:
        return tamper_selftest(report)
    if args.write_certificate:
        CERTIFICATE_DIR.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            render_certificate_json(report), encoding="utf-8"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
        return 0
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    if not CERTIFICATE_PATH.exists():
        raise RuntimeError(f"frozen certificate missing: {CERTIFICATE_PATH}")
    frozen = load_json(CERTIFICATE_PATH)
    if frozen != report or not validate_report(frozen):
        raise RuntimeError("frozen 31321 ledger certificate drift")
    print("PASS l1-b9-frontier-31321-total-degree-crt-ledger")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
