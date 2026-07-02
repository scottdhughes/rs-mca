#!/usr/bin/env python3
"""Verify the M1 a=327 upstream B47-robust skeleton search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_upstream_b47_robust_skeleton_search.json")
LOCAL_BASIN_PATH = Path("experimental/data/m1_a327_local_basin_conservation_note.json")
V2_GRID_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_upstream_b47_robust_skeleton_search.md")

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


def margin_score(capacity: int, pair_values: list[int]) -> int:
    return min(
        capacity - TARGET_AGREEMENT,
        pair_values[1] - PAIR_TARGET,
        pair_values[2] - PAIR_TARGET,
        pair_values[3] - PAIR_TARGET,
        pair_values[4] - PAIR_TARGET,
    )


def verify(record: dict[str, Any], local: dict[str, Any], v2: dict[str, Any], note_text: str) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "f2c7823", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    conservation = record["local_basin_conservation"]
    local_grid = local["full_v2_grid"]
    require(conservation["systems_tested"] == local_grid["systems_tested"] == 45, "wrong conservation system count")
    require(conservation["exact_vectors_constructed"] == local_grid["exact_vectors_constructed"] == 30, "wrong exact vector count")
    require(conservation["capacity_preserving_vectors"] == 0, "capacity-preserving vectors should be zero")
    require(conservation["pair_guard_preserving_vectors"] == 0, "pair guard vectors should be zero")
    require(conservation["status"] == "ROUTE_CUT_LOCAL_BASIN", "wrong conservation status")

    search = record["upstream_b47_search"]
    require(search["systems_tested"] == 0, "initial upstream ledger should not claim new exact systems")
    require(search["exact_vectors_constructed"] == 0, "initial upstream ledger should not claim new vectors")
    require(search["source_skeletons_analyzed"] >= 1, "missing source skeletons")
    require(search["split_probe_vectors"] == v2["compensated_grid"]["exact_vectors_constructed"] == 30, "wrong split probe count")
    require(search["split_resilient_skeletons"] == 0, "unexpected split-resilient source skeleton")
    require(search["fragile_1457_candidate_skeletons"] >= 1, "expected fragile 1457 candidates")
    require(search["best_failure_mode"] == "UPSTREAM_B47_NOT_ROBUST", "wrong initial upstream failure mode")

    best_pre_pairs = search["best_pre_split_pair_B_values"]
    require(search["best_pre_split_capacity"] == 333, "wrong best pre-split capacity")
    require(best_pre_pairs == [1024, 657, 656, 1024, 1024], "wrong best pre-split pairs")
    require(search["best_pre_split_robustness_score"] == margin_score(333, best_pre_pairs), "wrong pre robust score")

    best_probe_pairs = search["best_probe_split_pair_B_values"]
    require(search["best_probe_split_capacity"] == 261, "wrong best probe capacity")
    require(best_probe_pairs == [1024, 657, 656, 519, 1024], "wrong best probe pairs")
    require(search["best_probe_robustness_score"] == margin_score(261, best_probe_pairs), "wrong probe robust score")

    for probe in search["split_probe_results"]:
        require(probe["guard_preserving"] is False, "probe unexpectedly preserves guards")
        require(probe["robustness_score_after_split"] < 0, "probe score should be negative")

    require(record["proof_status"] == "PARTIAL", "wrong proof status")
    for phrase in [
        "not an MCA row",
        "not a protocol claim",
        "not a public-board update",
        "not a global obstruction theorem",
    ]:
        require(phrase in note_text, f"note missing non-claim phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "source_skeletons_analyzed": search["source_skeletons_analyzed"],
        "split_probe_vectors": search["split_probe_vectors"],
        "split_resilient_skeletons": search["split_resilient_skeletons"],
        "best_pre_split_capacity": search["best_pre_split_capacity"],
        "best_pre_split_pair_B_values": search["best_pre_split_pair_B_values"],
        "best_probe_split_capacity": search["best_probe_split_capacity"],
        "best_probe_split_pair_B_values": search["best_probe_split_pair_B_values"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(
        load_json(DATA_PATH),
        load_json(LOCAL_BASIN_PATH),
        load_json(V2_GRID_PATH),
        NOTE_PATH.read_text(),
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 upstream B47 ledger ({result['split_probe_vectors']} probes)")


if __name__ == "__main__":
    main()
