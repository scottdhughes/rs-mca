#!/usr/bin/env python3
"""Verify the M1 a=327 realized-slot near-miss repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_realized_slot_nearmiss_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_realized_slot_nearmiss_repair.md")

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
    require(record["source_commit"] == "e8ce88b", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "ACTUAL_TEMPLATE_ROWSPACES_ONLY", "wrong realization status")
    require(record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / NREPAIR_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL", "wrong proof status")

    previous = record["previous_realization_aware"]
    require(previous["commit"] == "e8ce88b", "wrong previous commit")
    require(previous["best_template_id"] == "single_outside_w7_v3", "wrong previous template")
    require(previous["best_assignment_strategy"] == "signature_fiber_blocks", "wrong previous assignment")
    require(previous["best_slot_nonzero_rows"] == 2, "wrong previous slot residual count")
    require(previous["actual_zero_slot_profiles"] == 0, "unexpected previous zero-slot profile")
    require(previous["best_failure_mode"] == "RAWARE_SLOT_NOT_KERNEL", "wrong previous failure")

    search = record["nearmiss_repair_search"]
    require(search["mutation_profiles_tested"] == 177, "wrong mutation count")
    require(search["systems_tested"] == 1062, "wrong systems tested")
    require(search["structural_pass_candidates"] == 1050, "wrong structural pass count")
    require(search["stable_basis_combinations"] == 853704, "wrong stable-basis combination count")
    require(search["stable_basis_profiles_tested"] == 30738, "wrong stable-basis profile count")
    require(search["slot_profiles_tested"] == 184428, "wrong slot profile count")
    require(search["actual_zero_slot_profiles"] == 0, "unexpected actual zero-slot profile")
    require(search["pair_projection_clear_actual_slots"] == 0, "unexpected pair-clear slot")
    require(search["proxy_positive_actual_slots"] == 0, "unexpected proxy-positive slot")
    require(search["best_template_id"] == "nearmiss_w7_c1_v9", "wrong best template")
    require(search["best_mutation_id"] == "w7_c1_v9", "wrong best mutation")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best assignment")
    require(search["best_slot_nonzero_rows"] == 2, "wrong best slot residual count")
    require(search["best_forced_pair_count"] == 10, "wrong best forced-pair count")
    require(search["best_failure_mode"] == "NREPAIR_SLOT_NOT_KERNEL", "wrong best failure")

    candidate = record["best_candidate"]
    require(candidate["template_id"] == "nearmiss_w7_c1_v9", "wrong candidate template")
    require(candidate["mutation_id"] == "w7_c1_v9", "wrong candidate mutation")
    require(candidate["base_template_id"] == "single_outside_w7_v3", "wrong base template")
    require(candidate["assignment_strategy"] == "signature_fiber_blocks", "wrong candidate assignment")
    require(candidate["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(candidate["pair7_counts"] == [253, 253, 253, 253, 253], "pair7 mismatch")
    require(candidate["max_pair_count"] == 253, "max pair mismatch")
    require(candidate["functional_classes"] == 17, "wrong functional class count")
    require(candidate["functional_span_rank"] == 6, "wrong functional span rank")
    require(candidate["forced_functional_identities"] == 0, "unexpected forced identity")
    require(candidate["effective_cost"] == 1777, "wrong effective cost")

    profile = candidate["best_profile"]
    require(profile["basis_id"] == "slot_union_142_6_8_10_12_15_16", "wrong basis id")
    require(profile["basis_class_indices"] == [6, 8, 10, 12, 15, 16], "wrong basis indices")
    require(profile["basis_support_sizes"] == [74, 74, 74, 37, 37, 31], "wrong basis supports")
    require(profile["proxy_kernel_slot"] == 3, "wrong kernel slot")
    require(profile["basis_zero_union_size"] == 142, "wrong basis union")
    require(profile["stable_common_multiplier_dimension"] == 114, "wrong stable dimension")
    require(profile["q_variable_count"] == 1209, "wrong q count")
    require(profile["proxy_kernel_block_degree"] == 219, "wrong block degree")
    require(profile["coefficient_matrix_shape"] == [11, 6], "wrong coefficient shape")
    require(profile["coefficient_rank"] == 6, "wrong coefficient rank")
    require(profile["coefficient_nullity"] == 0, "wrong coefficient nullity")
    require(profile["slot_nonzero_rows"] == 2, "wrong slot residual count")
    require(profile["actual_template_realized"] is True, "profile not actual-realized")
    require(profile["forced_pair_count"] == 10, "wrong forced pair count")
    require(profile["best_failure_mode"] == "RAWARE_SLOT_NOT_KERNEL", "wrong profile failure")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "mutation profiles tested = 177",
        "actual zero-slot profiles = 0",
        "slot nonzero rows = 2",
        "forced pair count = 10",
        "coefficient rank/nullity = 6 / 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "actual_zero_slot_profiles": search["actual_zero_slot_profiles"],
        "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
        "best_forced_pair_count": search["best_forced_pair_count"],
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
        print(f"PASS: M1 a=327 realized-slot near-miss repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
