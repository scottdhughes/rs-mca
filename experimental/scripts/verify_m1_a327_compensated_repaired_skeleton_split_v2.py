#!/usr/bin/env python3
"""Verifier for cached compensated repaired-skeleton split v2."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_compensated_repaired_skeleton_split_v2.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SYSTEMS_PLANNED = 45
CACHE_HASH = "f77410189226820cf8e8a2830f3a48523a92e485347702754c854fa8955addb4"
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
    "COMP_REPAIRED_SPLIT_PROJECTION_ERROR",
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
    require(record["source_commit"] == "c181b13", "wrong source commit")
    require(record["construction_mode"] == "compensated_repaired_skeleton_split_v2", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    cache = record["cache"]
    require(cache["cache_type"] == "SAGE_NATIVE", "wrong cache type")
    require(cache["cache_hash"] == CACHE_HASH, "wrong cache hash")
    require(cache["append_status"] == "CACHE_SMALL_APPEND_PASS", "cache append did not pass")

    base = record["baseline"]
    require(base["capacity"] == 333, "wrong baseline capacity")
    require(base["pair_B_values"] == [1024, 657, 656, 1024, 1024], "wrong baseline pairs")
    require(base["collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong baseline collapse")

    failed = record["failed_split"]
    require(failed["split_family"] == "split_4_from_157", "wrong failed split family")
    require(failed["capacity"] == 315, "wrong failed split capacity")
    require(failed["pair_B_values"] == [1024, 593, 592, 512, 1024], "wrong failed split pairs")
    require(failed["damage"] == {"capacity": -18, "B27": -64, "B37": -64, "B47": -512, "B57": 0}, "wrong damage")

    grid = record["compensated_grid"]
    require(grid["systems_planned"] == SYSTEMS_PLANNED, "wrong planned system count")
    require(0 <= grid["systems_tested"] <= SYSTEMS_PLANNED, "bad tested count")
    require(0 <= grid["timeouts"] <= grid["systems_tested"], "bad timeout count")
    require(grid["exact_vectors_constructed"] <= grid["systems_tested"], "too many exact vectors")
    require(grid["capacity_preserving_vectors"] <= grid["exact_vectors_constructed"], "bad capacity count")
    require(grid["pair_guard_preserving_vectors"] <= grid["exact_vectors_constructed"], "bad pair guard count")
    require(grid["partial_split_vectors"] <= grid["exact_vectors_constructed"], "bad partial split count")
    require(grid["nondegenerate_vectors"] <= grid["exact_vectors_constructed"], "bad nondegenerate count")
    require(len(grid["results"]) == grid["systems_tested"], "wrong result count")

    exact_candidate_count = 0
    for result in grid["results"]:
        failure = result["failure_mode"]
        require(failure in ALLOWED_FAILURES, f"bad result failure {failure}")
        if failure in {
            "COMP_REPAIRED_SPLIT_TIMEOUT",
            "COMP_REPAIRED_SPLIT_INCONSISTENT",
            "COMP_REPAIRED_SPLIT_PROJECTION_ERROR",
        }:
            continue
        best = result["best"]
        require(best["failure_mode"] == failure, "case/best failure mismatch")
        pairs = best["pair_B_values"]
        require(len(pairs) == 5, "wrong pair vector length")
        if failure == "COMP_REPAIRED_SPLIT_EXACT_CANDIDATE":
            exact_candidate_count += 1
            require(best.get("exact_max_min", -1) >= TARGET_AGREEMENT, "candidate below target")
            require(best.get("distinct_codewords") is True, "candidate not distinct")
            require(best.get("capacity_upper_bound", 0) >= TARGET_AGREEMENT, "candidate capacity deficit")
            require(pairs[1] >= PAIR_TARGET and pairs[2] >= PAIR_TARGET, "candidate B27/B37 deficit")
            require(pairs[3] >= PAIR_TARGET and pairs[4] >= PAIR_TARGET, "candidate B47/B57 deficit")

    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "candidate should be proof record")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
        require(grid["exact_vectors_constructed"] > 0, "negative status without vectors")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": grid["systems_tested"],
        "timeouts": grid["timeouts"],
        "exact_vectors_constructed": grid["exact_vectors_constructed"],
        "capacity_preserving_vectors": grid["capacity_preserving_vectors"],
        "pair_guard_preserving_vectors": grid["pair_guard_preserving_vectors"],
        "partial_split_vectors": grid["partial_split_vectors"],
        "nondegenerate_vectors": grid["nondegenerate_vectors"],
        "best_capacity": grid["best_capacity"],
        "best_pair_B_values": grid["best_pair_B_values"],
        "best_collapse_pattern": grid["best_collapse_pattern"],
        "best_failure_mode": grid["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 compensated repaired-skeleton split v2 ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
