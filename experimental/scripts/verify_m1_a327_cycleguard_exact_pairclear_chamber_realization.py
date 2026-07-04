#!/usr/bin/env python3
"""Verify the M1 a=327 cycleguard exact pair-clear chamber realization ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_cycleguard_exact_pairclear_chamber_realization.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_cycleguard_exact_pairclear_chamber_realization.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_cycleguard_exact_pairclear_chamber_realization.py")

CYCLE_PAIRS = ["P14", "P16", "P17", "P45", "P46", "P47", "P56", "P57", "P67"]

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested cycle-guarded chamber",
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
    scan_text = SCAN_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "0fc5a00", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / CYCLEG_REALIZATION_STABLE_WINDOW / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    front = record["cycle_guarded_front"]
    require(front["commit"] == "0fc5a00", "wrong front commit")
    require(
        front["proof_status"] == "CANDIDATE / CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK / PARTIAL / EXPERIMENTAL",
        "wrong front status",
    )
    require(front["basis_profiles_tested"] == 876, "wrong front profile count")
    require(front["exact_pairclear_profiles"] == 291, "wrong front exact pair-clear count")
    require(front["exact_pairclear_rank_slack_profiles"] == 80, "wrong front rank-slack count")
    require(front["best_template_id"] == "ninerow_P57_shear_c1_d1", "wrong front best template")
    require(front["best_basis_id"] == "basisaware_0_1_2_3_4_5", "wrong front best basis")
    require(front["best_failure_mode"] == "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK", "wrong front failure")

    structural = record["candidate_structural_row"]
    require(structural["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "wrong support vector")
    require(structural["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(structural["max_pair_count"] == 253, "wrong max pair count")
    require(structural["selected_class_size_counts"] == {"3": 185, "4": 43, "5": 142, "6": 142}, "wrong class sizes")
    require(structural["functional_classes"] == 25, "wrong functional class count")
    require(structural["functional_span_rank"] == 6, "wrong functional span rank")
    require(structural["forced_functional_identities"] == 0, "unexpected forced identities")
    require(structural["annihilator_dimension"] == 0, "unexpected annihilator")
    require(structural["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS", "wrong structural status")

    realization = record["chamber_realization"]
    require(realization["reconstruction_matches_source"] is True, "source reconstruction mismatch")
    require(realization["template_id"] == "ninerow_P57_shear_c1_d1", "wrong template")
    require(realization["mutation_id"] == "P57_shear_c1_d1", "wrong mutation")
    require(realization["assignment_strategy"] == "fiber_round_robin", "wrong assignment")
    require(realization["assignment_seed"] == 179986, "wrong assignment seed")
    require(realization["seed_offset"] == 0, "wrong seed offset")
    require(realization["basis_id"] == "basisaware_0_1_2_3_4_5", "wrong basis")
    require(realization["basis_class_indices"] == [0, 1, 2, 3, 4, 5], "wrong basis classes")
    require(realization["basis_support_sizes"] == [216, 142, 142, 105, 105, 74], "wrong basis supports")
    require(realization["coefficient_matrix_shape"] == [19, 6], "wrong coefficient shape")
    require(realization["row_classes"] == [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], "wrong row classes")
    require(realization["forced_pairs"] == [], "forced pairs remain")
    require(realization["zero_class_union_size"] == 253, "wrong zero union")
    require(realization["stable_window_dimension"] == 3, "wrong stable window")
    require(realization["active_class_union_size"] == 364, "wrong active union")
    require(realization["inactive_rank"] == 4, "wrong inactive rank")
    require(realization["inactive_kernel_nullity"] == 2, "wrong inactive nullity")
    require(realization["best_failure_mode"] == "CYCLEG_REALIZATION_STABLE_WINDOW", "wrong failure")

    chamber = realization["best_chamber"]
    require(chamber["direction"] == [1, 4, 0, 0, 10, 0], "wrong direction")
    require(chamber["forced_pairs"] == [], "best chamber does not clear pair projections")
    require(chamber["cycle_forced_count"] == 0, "cycle pair forced")
    require(chamber["cycle_pairs_cleared"] == CYCLE_PAIRS, "wrong cycle pairs cleared")
    require(chamber["zero_row_count"] == 8, "wrong zero row count")
    require(chamber["zero_row_classes"] == [7, 8, 9, 13, 17, 19, 21, 23], "wrong zero classes")
    require(chamber["inactive_rank"] == 4, "wrong chamber rank")
    require(chamber["inactive_kernel_nullity"] == 2, "wrong chamber nullity")

    slack = realization["rank_slack_subspace"]
    require(slack["basis"] == [[0, 0, 1, 0, 0, 0], [12, 14, 0, 0, 1, 0]], "wrong slack basis")
    require(slack["projective_directions_tested"] == 18, "wrong projective direction count")
    require(slack["pairclear_directions"] == 11, "wrong pair-clear directions")
    require(slack["forced_pair_pattern_counts"][""] == 11, "wrong empty forced-pattern count")

    zero_ledger = realization["zero_class_ledger"]
    require([row["class_index"] for row in zero_ledger] == [7, 8, 9, 13, 17, 19, 21, 23], "wrong zero ledger classes")
    require([row["support_size"] for row in zero_ledger] == [74, 74, 74, 68, 37, 37, 37, 31], "wrong zero supports")
    require(all(row["forced_identity"] is False for row in zero_ledger), "zero ledger forced identity")

    for phrase in [
        "CANDIDATE / CYCLEG_REALIZATION_STABLE_WINDOW",
        "zero class union size = 253",
        "stable window dimension = 3",
        "pair-clear directions = 11",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "CYCLEG_REALIZATION_STABLE_WINDOW",
        "zero_class_union_size",
        "rank_slack_subspace",
        "global obstruction outside the tested cycle-guarded chamber",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "template_id": realization["template_id"],
        "basis_id": realization["basis_id"],
        "direction": chamber["direction"],
        "forced_pairs": realization["forced_pairs"],
        "zero_class_union_size": realization["zero_class_union_size"],
        "stable_window_dimension": realization["stable_window_dimension"],
        "pairclear_directions": slack["pairclear_directions"],
        "best_failure_mode": realization["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 cycleguard chamber realization (status={result['proof_status']})")


if __name__ == "__main__":
    main()
