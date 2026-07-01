#!/usr/bin/env python3
"""Verifier for capacity-skeleton protected split placement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_capacity_skeleton_protected_split_placement.json")
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
    "SPLIT_DESTROYS_PAIR57",
    "SPLIT_CAPACITY_LOSS",
    "SPLIT_DOES_NOT_REDUCE_COLLAPSE",
    "SPLIT_PAIR27_37_STALLS",
    "SPLIT_LOW_RESCHEDULE",
    "SPLIT_EXACT_CANDIDATE",
    "SPLIT_INCONSISTENT",
    "SPLIT_TIMEOUT",
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
    require(record["source_commit"] == "6aa1f9e", "wrong source commit")
    require(record["construction_mode"] == "capacity_skeleton_protected_split_placement", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["previous_pair_B_values"] == [1024, 577, 576, 1024, 1024], "wrong previous pair values")
    require(baseline["split_pair_B_values"] == [1024, 593, 592, 1024, 514], "wrong split pair values")
    require(baseline["split_capacity"] == 315, "wrong split capacity")
    require(baseline["split_collapse_pattern"] == [[1, 4, 6, 7], [5], [3], [2]], "wrong split collapse")
    require(baseline["failure_mode"] == "PAIRCLASS_SPLIT_CAPACITY_LOSS", "wrong baseline failure")

    search = record["capacity_skeleton_search"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["target_sizes"] == [128], "wrong target sizes")
    require(search["systems_tested"] == 15, "wrong system count")
    require(search["pair_row_extensions"] == [32, 64, 96], "wrong pair extensions")
    require(
        search["split_families"]
        == [
            "keep_57_split_146_vs_57",
            "keep_567_split_14_vs_567",
            "keep_1457_split_6",
            "keep_157_split_46",
            "capacity_slack_only",
        ],
        "wrong split families",
    )
    require(search["free_patterns"] == ["d2_first_free", "d2_first4_free", "d2_even_sparse"], "wrong free patterns")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(search["timeouts"] == 0, "unexpected timeout count")
    require(search["exact_vectors_constructed"] == 45, "wrong exact vector count")
    require(search["capacity_preserving_vectors"] == 0, "wrong capacity-preserving count")
    require(search["pair57_preserving_vectors"] == 27, "wrong pair57-preserving count")
    require(search["pair27_37_improved_vectors"] == 15, "wrong pair27/37-improved count")
    require(search["collapse_reduced_vectors"] == 45, "wrong collapse-reduced count")
    require(search["best_pair_B_values"] == [1024, 593, 592, 1024, 1024], "wrong best pair values")
    require(search["best_capacity_upper_bound"] == 315, "wrong best capacity")
    require(search["best_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong best collapse")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["best_failure_mode"] == "SPLIT_CAPACITY_LOSS", "wrong best failure")
    require(
        search["failure_mode_counts"] == {"SPLIT_CAPACITY_LOSS": 27, "SPLIT_DESTROYS_PAIR57": 18},
        "wrong failure counts",
    )

    exact_candidate_count = 0
    vector_count = 0
    for result in search["results"]:
        require(result["failure_mode"] in ALLOWED_FAILURES, f"bad result failure {result['failure_mode']}")
        for row in result.get("vector_results", []):
            vector_count += 1
            require(row["failure_mode"] in ALLOWED_FAILURES, f"bad vector failure {row['failure_mode']}")
            if row["failure_mode"] == "SPLIT_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(row["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
                require(min(row["pair_B_values"]) >= PAIR_TARGET, "candidate pair values below target")
    require(vector_count == search["exact_vectors_constructed"], "vector count mismatch")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "capacity_preserving_vectors": search["capacity_preserving_vectors"],
        "pair57_preserving_vectors": search["pair57_preserving_vectors"],
        "pair27_37_improved_vectors": search["pair27_37_improved_vectors"],
        "best_pair_B_values": search["best_pair_B_values"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
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
        print(
            "PASS: M1 a=327 capacity-skeleton protected split placement "
            f"({result['systems_tested']} systems)"
        )


if __name__ == "__main__":
    main()
