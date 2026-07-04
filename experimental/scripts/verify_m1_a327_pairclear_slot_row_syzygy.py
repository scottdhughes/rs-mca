#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear slot row-syzygy ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_slot_row_syzygy.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_slot_row_syzygy.md")

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
    require(record["source_commit"] == "8ae0631", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "PAIRCLEAR_SLOT_ROW_SYZYGY", "wrong realization status")
    require(
        record["proof_status"] == "CANDIDATE / PCSYZ_DIRECTION_REDUCE_ROWS / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_pairclear_slot_row_reduction"]
    require(previous["commit"] == "8ae0631", "wrong previous commit")
    require(previous["proof_status"] == "CANDIDATE / PCSLOT_PAIR_CLEAR_SLOT_REDUCE_ROWS / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["best_mutation_id"] == "w1_c3_d1", "wrong previous mutation")
    require(previous["pair_clear_slot_profiles"] == 684, "wrong previous pair-clear slot count")
    require(previous["pair_clear_slot_kernel_profiles"] == 0, "unexpected previous slot kernel")
    require(previous["best_forced_pair_count"] == 0, "wrong previous forced-pair count")
    require(previous["best_forced_pairs"] == [], "unexpected previous forced pairs")
    require(previous["best_slot_nonzero_rows"] == 11, "wrong previous slot rows")
    require(previous["best_coefficient_nullity"] == 0, "wrong previous coefficient nullity")
    require(previous["best_failure_mode"] == "PCSLOT_PAIR_CLEAR_SLOT_REDUCE_ROWS", "wrong previous failure")

    search = record["pairclear_slot_row_syzygy"]
    require(search["base_mutation_id"] == "w1_c3_d1", "wrong base mutation")
    require(search["mutations_generated"] == 48, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 48, "wrong MILP profile count")
    require(search["candidate_systems_constructed"] == 144, "wrong candidate count")
    require(search["structural_pass_candidates"] == 138, "wrong structural pass count")
    require(search["structural_pass_candidates_analyzed"] == 24, "wrong analyzed count")
    require(search["structural_pass_candidates_skipped"] == 114, "wrong skipped count")
    require(search["top_classes"] == 14, "wrong top class count")
    require(search["random_bases"] == 0, "wrong random basis count")
    require(search["direction_max_extra"] == 1, "wrong direction max-extra")
    require(search["basis_profiles_tested"] == 25854, "wrong basis profile count")
    require(search["slot_profiles_tested"] == 155124, "wrong slot profile count")
    require(search["pair_clear_slot_profiles"] == 126, "wrong pair-clear slot count")
    require(search["pair_clear_slot_kernel_profiles"] == 0, "unexpected pair-clear slot kernel")
    require(search["direction_profiles_tested"] == 48, "wrong direction profile count")
    require(search["direction_vectors_tested"] == 3888, "wrong direction vector count")
    require(search["pair_clear_direction_profiles"] == 48, "wrong pair-clear direction count")
    require(search["pair_clear_direction_kernel_profiles"] == 0, "unexpected direction kernel")
    require(search["row_reduced_direction_profiles"] == 48, "wrong row-reduced direction count")
    require(search["best_template_id"] == "pcsyzygy_base_w1_c3_d1", "wrong best template")
    require(search["best_mutation_id"] == "base_w1_c3_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_unit_slot_nonzero_rows"] == 11, "wrong best unit slot rows")
    require(search["best_direction_nonzero_rows"] == 9, "wrong best direction rows")
    require(search["best_direction_forced_pair_count"] == 0, "wrong best direction forced-pair count")
    require(search["best_direction_forced_pairs"] == [], "unexpected best direction forced pairs")
    require(search["best_direction_vector"] == [0, 5, 0, 0, 0, 1], "wrong best direction vector")
    require(search["best_failure_mode"] == "PCSYZ_DIRECTION_REDUCE_ROWS", "wrong best failure")
    require(search["failure_counts"]["PCSYZ_DIRECTION_REDUCE_ROWS"] == 6, "wrong direction-reduce failure count")
    require(search["failure_counts"]["PCSLOT_PAIR_CLEAR_LOST"] == 18, "wrong pair-clear lost count")
    require(search["screen_counts"]["PCSYZ_STRUCTURAL_PASS"] == 138, "wrong structural pass screen count")
    require(search["screen_counts"]["PCSYZ_LOW_FUNCTIONAL_SPAN"] == 6, "wrong low-span screen count")

    best = record["best_candidate"]
    require(best["template_id"] == "pcsyzygy_base_w1_c3_d1", "wrong best candidate template")
    require(best["mutation_id"] == "base_w1_c3_d1", "wrong best candidate mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best candidate assignment")
    require(best["support_vector"] == [327] * 7, "wrong support vector")
    require(best["max_pair_count"] == 253, "wrong max pair count")
    require(best["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(best["functional_classes"] == 20, "wrong functional class count")
    require(best["functional_span_rank"] == 6, "wrong functional span")
    require(best["forced_functional_identities"] == 0, "unexpected forced identities")
    require(best["pair_clear_slot_profiles"] == 24, "wrong best candidate pair-clear slot count")
    profile = best["best_profile"]
    require(profile["basis_id"] == "basisaware_1_4_7_8_9_12", "wrong best unit basis")
    require(profile["coefficient_matrix_shape"] == [14, 6], "wrong unit coefficient shape")
    require(profile["coefficient_rank"] == 6, "wrong unit coefficient rank")
    require(profile["coefficient_nullity"] == 0, "wrong unit coefficient nullity")
    require(profile["proxy_kernel_slot"] == 5, "wrong unit proxy slot")
    require(profile["slot_nonzero_rows"] == 11, "wrong unit slot rows")
    require(profile["forced_pair_count"] == 0, "wrong unit forced-pair count")
    require(profile["forced_pairs"] == [], "unexpected unit forced pairs")
    direction = best["best_direction"]
    require(direction["basis_id"] == "basisaware_1_4_7_8_9_10", "wrong direction basis")
    require(direction["anchor_slot"] == 5, "wrong direction anchor")
    require(direction["direction_vector"] == [0, 5, 0, 0, 0, 1], "wrong direction vector")
    require(direction["direction_weight"] == 2, "wrong direction weight")
    require(direction["direction_nonzero_rows"] == 9, "wrong direction row count")
    require(direction["direction_nonzero_row_classes"] == [0, 2, 3, 5, 6, 11, 12, 14, 15], "wrong direction row classes")
    require(direction["forced_pair_count"] == 0, "wrong direction forced-pair count")
    require(direction["forced_pairs"] == [], "unexpected direction forced pairs")
    require(all(int(value) % 17 for value in direction["pair_projection_scalars"].values()), "direction has zero pair scalar")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "mutations generated = 48",
        "direction vectors tested = 3888",
        "direction vector = [0,5,0,0,0,1]",
        "direction nonzero rows = 9",
        "slot rows improved 11 -> 9",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "mutations_generated": search["mutations_generated"],
        "best_direction_nonzero_rows": search["best_direction_nonzero_rows"],
        "best_direction_forced_pair_count": search["best_direction_forced_pair_count"],
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
        print(f"PASS: M1 a=327 pair-clear slot row syzygy (status={result['proof_status']})")


if __name__ == "__main__":
    main()
