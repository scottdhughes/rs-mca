#!/usr/bin/env python3
"""Verify the M1 a=327 P23 slot-kernel codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_p23_slot_kernel_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_p23_slot_kernel_codesign.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
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
    require(record["source_commit"] == "ae37b1a", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "P23_SLOT_KERNEL_CODESIGN", "wrong realization status")
    require(record["proof_status"] == "CANDIDATE / P23SLOT_PAIR_CLEAR_SLOT / PARTIAL / EXPERIMENTAL", "wrong proof status")

    previous = record["previous_template_vector_repair"]
    require(previous["commit"] == "ae37b1a", "wrong previous commit")
    require(previous["best_mutation_id"] == "w1_c0_d16", "wrong previous mutation")
    require(previous["best_forced_pair_count"] == 1, "wrong previous forced-pair count")
    require(previous["best_forced_pairs"] == ["P23"], "wrong previous forced pairs")
    require(previous["best_slot_nonzero_rows"] == 12, "wrong previous slot rows")
    require(previous["best_failure_mode"] == "TVPAIR_SLOT_PAIR_CLEAR_BROKEN", "wrong previous failure")

    search = record["p23_slot_codesign"]
    require(search["base_mutation_id"] == "w1_c0_d16", "wrong base mutation")
    require(search["target_pair"] == "P23", "wrong target pair")
    require(search["mutations_generated"] == 36, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 36, "wrong MILP profile count")
    require(search["candidate_systems_constructed"] == 108, "wrong candidate count")
    require(search["structural_pass_candidates"] == 99, "wrong structural pass count")
    require(search["structural_pass_candidates_analyzed"] == 24, "wrong analyzed count")
    require(search["structural_pass_candidates_skipped"] == 75, "wrong skipped count")
    require(search["top_classes"] == 14, "wrong top class count")
    require(search["random_bases"] == 0, "wrong random basis count")
    require(search["basis_profiles_tested"] == 13278, "wrong basis profile count")
    require(search["slot_profiles_tested"] == 79668, "wrong slot profile count")
    require(search["pair_clear_slot_profiles"] == 54, "wrong pair-clear slot count")
    require(search["pair_clear_slot_kernel_profiles"] == 0, "unexpected pair-clear slot kernel")
    require(search["best_template_id"] == "p23slot_w2_c1_d1", "wrong best template")
    require(search["best_mutation_id"] == "w2_c1_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_forced_pair_count"] == 0, "wrong best forced-pair count")
    require(search["best_forced_pairs"] == [], "unexpected best forced pairs")
    require(search["best_slot_nonzero_rows"] == 14, "wrong best slot-nonzero count")
    require(search["best_coefficient_nullity"] == 0, "wrong best coefficient nullity")
    require(search["best_failure_mode"] == "P23SLOT_PAIR_CLEAR_SLOT", "wrong best failure")

    best = record["best_candidate"]
    require(best["template_id"] == "p23slot_w2_c1_d1", "wrong best candidate template")
    require(best["mutation_id"] == "w2_c1_d1", "wrong best candidate mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best candidate assignment")
    require(best["support_vector"] == [327] * 7, "wrong support vector")
    require(best["max_pair_count"] == 253, "wrong max pair count")
    require(best["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(best["functional_span_rank"] == 6, "wrong functional span")
    require(best["forced_functional_identities"] == 0, "unexpected forced identities")
    require(best["pair_clear_slot_profiles"] == 9, "wrong best candidate pair-clear slot count")
    profile = best["best_profile"]
    require(profile["basis_id"] == "basisaware_1_6_7_8_10_12", "wrong best basis")
    require(profile["coefficient_matrix_shape"] == [14, 6], "wrong coefficient shape")
    require(profile["coefficient_rank"] == 6, "wrong coefficient rank")
    require(profile["coefficient_nullity"] == 0, "wrong coefficient nullity")
    require(profile["proxy_kernel_slot"] == 0, "wrong proxy kernel slot")
    require(profile["slot_nonzero_rows"] == 14, "wrong slot nonzero count")
    require(profile["forced_pair_count"] == 0, "wrong profile forced-pair count")
    require(profile["forced_pairs"] == [], "unexpected profile forced pairs")
    require(profile["p23_forced"] is False, "P23 still forced")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "mutations generated = 36",
        "slot profiles tested = 79668",
        "pair-clear slot profiles = 54",
        "forced pair count = 0",
        "slot nonzero rows = 14",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "mutations_generated": search["mutations_generated"],
        "pair_clear_slot_profiles": search["pair_clear_slot_profiles"],
        "best_forced_pair_count": search["best_forced_pair_count"],
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
        print(f"PASS: M1 a=327 P23 slot-kernel codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
