#!/usr/bin/env python3
"""Verify the M1 a=327 realization-aware proxy-slot generator ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_realization_aware_proxy_slot_generator.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_realization_aware_proxy_slot_generator.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "synthetic rowspace edits",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "8032816", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "ACTUAL_TEMPLATE_ROWSPACES_ONLY", "wrong realization status")
    require(record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / RAWARE_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL", "wrong proof status")

    previous = record["previous_template_realization"]
    require(previous["commit"] == "8032816", "wrong previous commit")
    require(previous["target_template_id"] == "sheared_outside_seed_001", "wrong previous target")
    require(previous["proxy_rank"] == 1267, "wrong previous proxy rank")
    require(previous["proxy_nullity"] == 253, "wrong previous proxy nullity")
    require(previous["linear_rank"] == 35, "wrong previous linear rank")
    require(previous["linear_nullity"] == 7, "wrong previous linear nullity")
    require(previous["rowspace_valid_samples"] == 0, "unexpected previous rowspace success")
    require(previous["best_failure_mode"] == "TEMPLATE_REALIZATION_ROWSPACE_FAIL", "wrong previous failure")

    search = record["realization_aware_search"]
    require(search["templates_tested"] == 36, "wrong template count")
    require(search["systems_tested"] == 216, "wrong systems tested")
    require(search["structural_pass_candidates"] == 210, "wrong structural pass count")
    require(search["stable_basis_combinations"] == 23663322, "wrong stable-basis combination count")
    require(search["stable_basis_profiles_tested"] == 12312, "wrong stable-basis profile count")
    require(search["slot_profiles_tested"] == 73872, "wrong slot profile count")
    require(search["actual_zero_slot_profiles"] == 0, "unexpected actual zero-slot profile")
    require(search["pair_projection_clear_actual_slots"] == 0, "unexpected pair-clear actual slot")
    require(search["proxy_positive_actual_slots"] == 0, "unexpected proxy-positive actual slot")
    require(search["best_template_id"] == "single_outside_w7_v3", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best assignment")
    require(search["best_slot_nonzero_rows"] == 2, "wrong best slot residual count")
    require(search["best_failure_mode"] == "RAWARE_SLOT_NOT_KERNEL", "wrong best failure")

    candidate = record["best_candidate"]
    require(candidate["template_id"] == "single_outside_w7_v3", "wrong candidate template")
    require(candidate["assignment_strategy"] == "signature_fiber_blocks", "wrong candidate assignment")
    require(candidate["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(candidate["pair7_counts"] == [253, 253, 253, 253, 253], "pair7 mismatch")
    require(candidate["max_pair_count"] == 253, "max pair mismatch")
    require(candidate["functional_classes"] == 18, "wrong functional class count")
    require(candidate["functional_span_rank"] == 6, "wrong functional span rank")
    require(candidate["forced_functional_identities"] == 0, "unexpected forced identity")
    require(candidate["actual_zero_slot_profiles"] == 0, "unexpected candidate zero slot")

    profile = candidate["best_profile"]
    require(profile["basis_id"] == "slot_union_142_5_7_9_11_13_17", "wrong basis id")
    require(profile["basis_class_indices"] == [5, 7, 9, 11, 13, 17], "wrong basis indices")
    require(profile["basis_support_sizes"] == [74, 74, 74, 74, 37, 31], "wrong basis supports")
    require(profile["proxy_kernel_slot"] == 3, "wrong kernel slot")
    require(profile["basis_zero_union_size"] == 142, "wrong basis union")
    require(profile["stable_common_multiplier_dimension"] == 114, "wrong stable dimension")
    require(profile["q_variable_count"] == 1172, "wrong q count")
    require(profile["proxy_kernel_block_degree"] == 182, "wrong block degree")
    require(profile["coefficient_matrix_shape"] == [12, 6], "wrong coefficient shape")
    require(profile["coefficient_rank"] == 6, "wrong coefficient rank")
    require(profile["coefficient_nullity"] == 0, "wrong coefficient nullity")
    require(profile["slot_nonzero_rows"] == 2, "wrong slot residual count")
    require(profile["actual_template_realized"] is True, "profile not actual-realized")
    require(profile["forced_pair_count"] == 15, "wrong forced pair count")
    require(profile["best_failure_mode"] == "RAWARE_SLOT_NOT_KERNEL", "wrong profile failure")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "actual zero-slot profiles = 0",
        "best slot nonzero rows = 2",
        "coefficient rank/nullity = 6 / 0",
        "forced pair count in that slot = 15",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "actual_zero_slot_profiles": search["actual_zero_slot_profiles"],
        "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 realization-aware proxy-slot generator (status={result['proof_status']})")


if __name__ == "__main__":
    main()
