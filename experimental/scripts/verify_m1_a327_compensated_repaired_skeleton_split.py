#!/usr/bin/env python3
"""Verifier for compensated repaired-skeleton split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "COMP_REPAIRED_SPLIT_CAPACITY_NOT_RESTORED",
    "COMP_REPAIRED_SPLIT_PAIR27_37_LOSS",
    "COMP_REPAIRED_SPLIT_PAIR47_LOSS",
    "COMP_REPAIRED_SPLIT_PAIR57_LOSS",
    "COMP_REPAIRED_SPLIT_COLLAPSE_RETURNS",
    "COMP_REPAIRED_SPLIT_PARTIAL_DISTINCT",
    "COMP_REPAIRED_SPLIT_LOW_RESCHEDULE",
    "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE",
    "COMP_REPAIRED_SPLIT_TIMEOUT",
    "COMP_REPAIRED_SPLIT_INCONSISTENT",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "30d0cdb", "wrong source commit")
    require(record["construction_mode"] == "compensated_repaired_skeleton_split", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["capacity"] == 333, "wrong baseline capacity")
    require(baseline["pair_B_values"] == [1024, 657, 656, 1024, 1024], "wrong baseline pairs")
    require(baseline["collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong baseline collapse")

    failed = record["failed_split"]
    require(failed["split_family"] == "split_4_from_157", "wrong failed split family")
    require(failed["capacity"] == 315, "wrong failed split capacity")
    require(failed["pair_B_values"] == [1024, 593, 592, 512, 1024], "wrong failed split pairs")
    require(failed["collapse_pattern"] == [[1, 5, 6, 7], [4], [3], [2]], "wrong failed split collapse")
    require(failed["damage"] == {"capacity": -18, "B27": -64, "B37": -64, "B47": -512, "B57": 0}, "wrong damage vector")

    search = record["compensated_split"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["base_system"] == "postsplit_microrepair_stage2_triple_237_budget32", "wrong base system")
    require(search["systems_tested"] >= 1, "no systems tested")
    require(search.get("planned_systems", search["systems_tested"]) >= search["systems_tested"], "bad planned count")
    require(search["timeouts"] >= 0, "bad timeout count")
    require(search["exact_vectors_constructed"] <= search["systems_tested"], "too many exact vectors")
    require(search["capacity_preserving_vectors"] <= search["exact_vectors_constructed"], "bad capacity count")
    require(search["pair_guard_preserving_vectors"] <= search["exact_vectors_constructed"], "bad pair guard count")
    require(search["partial_split_vectors"] <= search["exact_vectors_constructed"], "bad partial split count")
    require(search["nondegenerate_vectors"] <= search["exact_vectors_constructed"], "bad nondegenerate count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(len(search["results"]) == search["systems_tested"], "wrong result length")

    exact_candidate_count = 0
    for result in search["results"]:
        failure = result["failure_mode"]
        require(failure in ALLOWED_FAILURES, f"bad result failure {failure}")
        if failure in {"COMP_REPAIRED_SPLIT_TIMEOUT", "COMP_REPAIRED_SPLIT_INCONSISTENT"}:
            continue
        row = result["best"]
        pair_values = row["pair_B_values"]
        require(len(pair_values) == 5, "wrong pair vector length")
        require(row["failure_mode"] == failure, "case/best failure mismatch")
        if failure == "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE":
            exact_candidate_count += 1
            require(row.get("exact_max_min", -1) >= TARGET_AGREEMENT, "candidate below target")
            require(row.get("distinct_codewords") is True, "candidate not distinct")
            require(row.get("capacity_upper_bound", 0) >= TARGET_AGREEMENT, "candidate capacity deficit")
            require(pair_values[1] >= PAIR_TARGET and pair_values[2] >= PAIR_TARGET, "candidate B27/B37 deficit")
            require(pair_values[3] >= PAIR_TARGET and pair_values[4] >= PAIR_TARGET, "candidate B47/B57 deficit")

    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
        require(search["exact_vectors_constructed"] > 0, "negative exact status without constructed vectors")
    if record["proof_status"] == "PARTIAL":
        require(search["best_failure_mode"] == "COMP_REPAIRED_SPLIT_TIMEOUT", "partial status should explain timeout")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "timeouts": search["timeouts"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "capacity_preserving_vectors": search["capacity_preserving_vectors"],
        "pair_guard_preserving_vectors": search["pair_guard_preserving_vectors"],
        "partial_split_vectors": search["partial_split_vectors"],
        "nondegenerate_vectors": search["nondegenerate_vectors"],
        "best_capacity": search["best_capacity"],
        "best_pair_B_values": search["best_pair_B_values"],
        "best_collapse_pattern": search["best_collapse_pattern"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 compensated repaired-skeleton split ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
