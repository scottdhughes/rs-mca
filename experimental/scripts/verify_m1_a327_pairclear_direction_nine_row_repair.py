#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear direction nine-row repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_direction_nine_row_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_direction_nine_row_repair.md")

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
    require(record["source_commit"] == "402d88c", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "PAIRCLEAR_DIRECTION_NINE_ROW_REPAIR", "wrong realization status")
    require(
        record["proof_status"] == "CANDIDATE / NINEROW_FIXED_DIRECTION_STABLE / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_pairclear_slot_row_syzygy"]
    require(previous["commit"] == "402d88c", "wrong previous commit")
    require(previous["proof_status"] == "CANDIDATE / PCSYZ_DIRECTION_REDUCE_ROWS / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["best_mutation_id"] == "base_w1_c3_d1", "wrong previous mutation")
    require(previous["best_direction_vector"] == [0, 5, 0, 0, 0, 1], "wrong previous direction")
    require(previous["best_direction_nonzero_rows"] == 9, "wrong previous row count")
    require(previous["best_direction_forced_pair_count"] == 0, "wrong previous forced-pair count")
    require(previous["best_direction_forced_pairs"] == [], "unexpected previous forced pairs")
    require(previous["best_failure_mode"] == "PCSYZ_DIRECTION_REDUCE_ROWS", "wrong previous failure")

    target = record["target_nine_row_system"]
    require(target["target_basis_class_indices"] == [1, 4, 7, 8, 9, 10], "wrong target basis")
    require(target["pinned_direction"] == [0, 5, 0, 0, 0, 1], "wrong pinned direction")
    require(target["previous_active_row_classes"] == [0, 2, 3, 5, 6, 11, 12, 14, 15], "wrong active row classes")

    search = record["nine_row_repair"]
    require(search["base_mutation_id"] == "base_w1_c3_d1", "wrong base mutation")
    require(search["mutations_generated"] == 72, "wrong mutation count")
    require(search["milp_profiles_constructed"] == 72, "wrong MILP profile count")
    require(search["candidate_systems_constructed"] == 216, "wrong candidate count")
    require(search["structural_pass_candidates"] == 210, "wrong structural pass count")
    require(search["structural_pass_candidates_analyzed"] == 36, "wrong analyzed count")
    require(search["structural_pass_candidates_skipped"] == 174, "wrong skipped count")
    require(search["direction_max_extra"] == 2, "wrong direction max-extra")
    require(search["target_basis_profiles_present"] == 27, "wrong target basis profile count")
    require(search["directions_tested"] == 71307, "wrong direction count")
    require(search["pair_clear_directions"] == 2883, "wrong pair-clear direction count")
    require(search["row_reduced_directions"] == 0, "unexpected row-reduced direction")
    require(search["pair_clear_direction_kernels"] == 0, "unexpected direction kernel")
    require(search["fixed_direction_pair_clear_profiles"] == 3, "wrong fixed pair-clear profile count")
    require(search["fixed_direction_row_reduced_profiles"] == 0, "unexpected fixed row reduction")
    require(search["fixed_direction_kernel_profiles"] == 0, "unexpected fixed kernel")
    require(search["local_direction_row_reduced_profiles"] == 0, "unexpected local row reduction")
    require(search["local_direction_kernel_profiles"] == 0, "unexpected local kernel")
    require(search["best_template_id"] == "ninerow_base_w1_c3_d1", "wrong best template")
    require(search["best_mutation_id"] == "base_w1_c3_d1", "wrong best mutation")
    require(search["best_assignment_strategy"] == "fiber_round_robin", "wrong best assignment")
    require(search["best_fixed_direction_nonzero_rows"] == 9, "wrong fixed direction rows")
    require(search["best_fixed_direction_forced_pair_count"] == 0, "wrong fixed forced-pair count")
    require(search["best_local_direction_nonzero_rows"] == 9, "wrong local direction rows")
    require(search["best_local_direction_forced_pair_count"] == 0, "wrong local forced-pair count")
    require(search["best_local_direction_vector"] == [0, 5, 0, 0, 0, 1], "wrong local direction vector")
    require(search["best_failure_mode"] == "NINEROW_FIXED_DIRECTION_STABLE", "wrong best failure")
    require(search["failure_counts"]["NINEROW_FIXED_DIRECTION_STABLE"] == 3, "wrong stable failure count")
    require(search["failure_counts"]["NINEROW_DIRECTION_FORCED_PAIR"] == 24, "wrong forced-pair failure count")
    require(search["failure_counts"]["NINEROW_TARGET_BASIS_MISSING"] == 9, "wrong missing-basis failure count")
    require(search["screen_counts"]["NINEROW_STRUCTURAL_PASS"] == 210, "wrong structural pass screen count")
    require(search["screen_counts"]["NINEROW_LOW_FUNCTIONAL_SPAN"] == 6, "wrong low-span screen count")

    best = record["best_candidate"]
    require(best["template_id"] == "ninerow_base_w1_c3_d1", "wrong best candidate template")
    require(best["mutation_id"] == "base_w1_c3_d1", "wrong best candidate mutation")
    require(best["assignment_strategy"] == "fiber_round_robin", "wrong best candidate assignment")
    require(best["support_vector"] == [327] * 7, "wrong support vector")
    require(best["max_pair_count"] == 253, "wrong max pair count")
    require(best["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(best["functional_classes"] == 20, "wrong functional class count")
    require(best["functional_span_rank"] == 6, "wrong functional span")
    require(best["forced_functional_identities"] == 0, "unexpected forced identities")
    fixed = best["fixed_direction"]
    local = best["best_local_direction"]
    for label, direction in [("fixed", fixed), ("local", local)]:
        require(direction["basis_id"] == "basisaware_1_4_7_8_9_10", f"wrong {label} basis")
        require(direction["basis_class_indices"] == [1, 4, 7, 8, 9, 10], f"wrong {label} basis classes")
        require(direction["direction_vector"] == [0, 5, 0, 0, 0, 1], f"wrong {label} direction vector")
        require(direction["direction_weight"] == 2, f"wrong {label} direction weight")
        require(direction["direction_nonzero_rows"] == 9, f"wrong {label} row count")
        require(direction["direction_nonzero_row_classes"] == [0, 2, 3, 5, 6, 11, 12, 14, 15], f"wrong {label} row classes")
        require(direction["previous_active_rows_retained"] == 9, f"wrong {label} retained rows")
        require(direction["previous_active_rows_removed"] == [], f"unexpected {label} removed rows")
        require(direction["new_active_rows_introduced"] == [], f"unexpected {label} new rows")
        require(direction["forced_pair_count"] == 0, f"wrong {label} forced-pair count")
        require(direction["forced_pairs"] == [], f"unexpected {label} forced pairs")
        require(all(int(value) % 17 for value in direction["pair_projection_scalars"].values()), f"{label} has zero pair scalar")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "mutations generated = 72",
        "directions tested = 71307",
        "row-reduced directions = 0",
        "direction vector = [0,5,0,0,0,1]",
        "direction nonzero rows = 9",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "mutations_generated": search["mutations_generated"],
        "directions_tested": search["directions_tested"],
        "best_fixed_direction_nonzero_rows": search["best_fixed_direction_nonzero_rows"],
        "row_reduced_directions": search["row_reduced_directions"],
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
        print(f"PASS: M1 a=327 pair-clear direction nine-row repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
