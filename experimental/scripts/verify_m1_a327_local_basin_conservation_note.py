#!/usr/bin/env python3
"""Verify the M1 a=327 local-basin conservation audit packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_local_basin_conservation_note.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_local_basin_conservation_note.md")
SOURCE_GRID_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")

TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "global obstruction outside the tested basin",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_against_source(record: dict[str, Any], source: dict[str, Any]) -> None:
    grid = source["compensated_grid"]
    full = record["full_v2_grid"]
    require(full["systems_tested"] == grid["systems_tested"], "systems_tested mismatch")
    require(full["timeouts"] == grid["timeouts"], "timeouts mismatch")
    require(full["exact_vectors_constructed"] == grid["exact_vectors_constructed"], "exact vector mismatch")
    require(full["capacity_preserving_vectors"] == grid["capacity_preserving_vectors"], "capacity count mismatch")
    require(full["pair_guard_preserving_vectors"] == grid["pair_guard_preserving_vectors"], "pair guard count mismatch")
    require(full["partial_split_vectors"] == grid["partial_split_vectors"], "partial split count mismatch")
    require(full["nondegenerate_vectors"] == grid["nondegenerate_vectors"], "nondegenerate count mismatch")
    require(full["failure_mode_counts"] == grid["failure_mode_counts"], "failure counts mismatch")
    require(full["best_capacity"] == grid["best_capacity"], "best capacity mismatch")
    require(full["best_pair_B_values"] == grid["best_pair_B_values"], "best pair values mismatch")
    require(full["best_collapse_pattern"] == grid["best_collapse_pattern"], "best collapse mismatch")
    require(full["best_failure_mode"] == grid["best_failure_mode"], "best failure mismatch")


def verify(record: dict[str, Any], source: dict[str, Any], note_text: str) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    commits = record["source_commits"]
    require(commits["persistent_state"] == "30d0cdb", "wrong persistent-state commit")
    require(commits["sage_native_cache"] == "c181b13", "wrong Sage-native cache commit")
    require(commits["v2_runner"] == "c491cdb", "wrong v2 runner commit")
    require(commits["priority_batch"] == "d913a87", "wrong priority-batch commit")
    require(commits["full_grid"] == "62c15cc", "wrong full-grid commit")

    base = record["baseline_repaired_skeleton"]
    require(base["capacity"] == 333, "wrong baseline capacity")
    require(base["pair_B_values"] == [1024, 657, 656, 1024, 1024], "wrong baseline pair values")
    require(base["pair_hall_bound"] == 328, "wrong pair Hall bound")
    require(base["six_class_dominance"] == 0, "wrong six-class dominance")
    require(base["collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong baseline collapse")

    damage = record["failed_split_damage"]
    require(damage["split_family"] == "split_4_from_157", "wrong split family")
    require(damage["capacity_loss"] == 18, "wrong capacity loss")
    require(damage["B27_loss"] == 64, "wrong B27 loss")
    require(damage["B37_loss"] == 64, "wrong B37 loss")
    require(damage["B47_loss"] == 512, "wrong B47 loss")
    require(damage["B57_loss"] == 0, "wrong B57 loss")

    full = record["full_v2_grid"]
    require(full["systems_tested"] == 45, "wrong systems tested")
    require(full["timeouts"] == 0, "timeouts should be zero")
    require(full["exact_vectors_constructed"] == 30, "wrong exact vector count")
    require(full["inconsistent_systems"] == 15, "wrong inconsistent count")
    require(full["capacity_preserving_vectors"] == 0, "capacity was unexpectedly preserved")
    require(full["pair_guard_preserving_vectors"] == 0, "pair guards were unexpectedly preserved")
    require(full["partial_split_vectors"] == 30, "wrong partial split count")
    require(full["nondegenerate_vectors"] == 3, "wrong nondegenerate count")
    require(full["failure_mode_counts"] == {
        "COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED": 30,
        "COMP_REPAIRED_SPLIT_INCONSISTENT": 15,
    }, "wrong failure counts")
    require(full["best_capacity"] == 174, "wrong best capacity")
    require(full["best_pair_B_values"] == [583, 657, 656, 524, 524], "wrong best pair values")
    require(full["best_collapse_pattern"] == [[4, 5], [7], [6], [3], [2], [1]], "wrong best collapse")
    require(full["best_failure_mode"] == "COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED", "wrong best failure")

    route = record["local_route_cut"]
    require(route["tested_basin"] == "repaired_skeleton_compensated_split_v2", "wrong tested basin")
    require(route["not_global"] is True, "route cut must be marked local")
    require(route["required_guards"] == {
        "capacity": TARGET_AGREEMENT,
        "B27": PAIR_TARGET,
        "B37": PAIR_TARGET,
        "B47": PAIR_TARGET,
        "B57": PAIR_TARGET,
    }, "wrong guard thresholds")
    require(record["proof_status"] == "AUDIT / ROUTE_CUT_LOCAL_BASIN / EXPERIMENTAL", "wrong proof status")

    verify_against_source(record, source)

    for phrase in [
        "not an MCA row",
        "not a protocol claim",
        "global obstruction theorem",
        "No global `Lambda_mu(C,327) <= 6` theorem",
    ]:
        require(phrase in note_text, f"note missing non-claim phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": full["systems_tested"],
        "exact_vectors_constructed": full["exact_vectors_constructed"],
        "inconsistent_systems": full["inconsistent_systems"],
        "capacity_preserving_vectors": full["capacity_preserving_vectors"],
        "pair_guard_preserving_vectors": full["pair_guard_preserving_vectors"],
        "best_capacity": full["best_capacity"],
        "best_pair_B_values": full["best_pair_B_values"],
        "best_failure_mode": full["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(
        load_json(DATA_PATH),
        load_json(SOURCE_GRID_PATH),
        NOTE_PATH.read_text(),
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 local-basin conservation note ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
