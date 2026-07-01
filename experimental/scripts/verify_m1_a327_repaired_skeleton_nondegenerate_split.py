#!/usr/bin/env python3
"""Verifier for repaired-skeleton nondegenerate split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_nondegenerate_split.json")
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
    "REPAIRED_SPLIT_NOT_DISTINCT",
    "REPAIRED_SPLIT_PARTIAL_DISTINCT",
    "REPAIRED_SPLIT_CAPACITY_LOSS",
    "REPAIRED_SPLIT_PAIR27_37_LOSS",
    "REPAIRED_SPLIT_PAIR57_LOSS",
    "REPAIRED_SPLIT_COLLAPSE_RETURNS",
    "REPAIRED_SPLIT_LOW_RESCHEDULE",
    "REPAIRED_SPLIT_EXACT_CANDIDATE",
    "REPAIRED_SPLIT_INCONSISTENT",
    "REPAIRED_SPLIT_TIMEOUT",
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
    require(record["source_commit"] == "2dfd1d9", "wrong source commit")
    require(record["construction_mode"] == "repaired_skeleton_nondegenerate_split", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["capacity"] == 333, "wrong baseline capacity")
    require(baseline["pair_B_values"] == [1024, 657, 656, 1024, 1024], "wrong baseline pairs")
    require(baseline["pair_hall_bound"] == 328, "wrong baseline pair Hall bound")
    require(baseline["B27_deficit"] == -3, "wrong baseline B27 deficit")
    require(baseline["B37_deficit"] == -2, "wrong baseline B37 deficit")
    require(baseline["B57"] == 1024, "wrong baseline B57")
    require(baseline["collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong baseline collapse")
    require(baseline["distinct_codewords"] is False, "baseline should be degenerate")
    require(baseline["failure_mode"] == "MICROREPAIR_STAGE2_LOW_RESCHEDULE", "wrong baseline failure")

    search = record["repaired_skeleton_split"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["base_system"] == "postsplit_microrepair_stage2_triple_237_budget32", "wrong base system")
    require(search["systems_tested"] >= 1, "no systems tested")
    require(search["timeouts"] >= 0, "bad timeout count")
    require(search["exact_vectors_constructed"] <= 3 * search["systems_tested"], "too many exact vectors")
    require(search["nondegenerate_vectors"] <= search["exact_vectors_constructed"], "bad nondegenerate count")
    require(search["partial_split_vectors"] <= search["exact_vectors_constructed"], "bad partial split count")
    require(search["capacity_preserving_vectors"] <= search["exact_vectors_constructed"], "bad capacity count")
    require(search["pair_guard_preserving_vectors"] <= search["exact_vectors_constructed"], "bad pair guard count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(len(search["results"]) == search["systems_tested"], "wrong result length")

    exact_candidate_count = 0
    for result in search["results"]:
        require("vector_results" in result, "case missing vector results")
        for row in result["vector_results"]:
            failure = row["failure_mode"]
            require(failure in ALLOWED_FAILURES, f"bad result failure {failure}")
            if failure == "REPAIRED_SPLIT_TIMEOUT":
                continue
            if row.get("pair_B_values") is None:
                require(failure == "REPAIRED_SPLIT_INCONSISTENT", "missing pair values outside inconsistent result")
                continue
            pair_values = row["pair_B_values"]
            require(len(pair_values) == 5, "wrong pair vector length")
            if failure == "REPAIRED_SPLIT_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(row.get("exact_max_min", -1) >= TARGET_AGREEMENT, "candidate below target")
                require(row.get("distinct_codewords") is True, "candidate not distinct")
                require(pair_values[1] >= PAIR_TARGET and pair_values[2] >= PAIR_TARGET, "candidate pair deficit")
                require(pair_values[4] >= PAIR_TARGET, "candidate pair57 deficit")
                require(row.get("capacity_upper_bound", 0) >= TARGET_AGREEMENT, "candidate capacity deficit")

    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "timeouts": search["timeouts"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "nondegenerate_vectors": search["nondegenerate_vectors"],
        "partial_split_vectors": search["partial_split_vectors"],
        "capacity_preserving_vectors": search["capacity_preserving_vectors"],
        "pair_guard_preserving_vectors": search["pair_guard_preserving_vectors"],
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
        print(f"PASS: M1 a=327 repaired-skeleton split ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
