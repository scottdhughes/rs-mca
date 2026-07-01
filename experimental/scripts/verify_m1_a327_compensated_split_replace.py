#!/usr/bin/env python3
"""Verifier for compensated split-and-replace search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_compensated_split_replace.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "COMP_SPLIT_CAPACITY_NOT_RESTORED",
    "COMP_SPLIT_PAIR57_LOSS",
    "COMP_SPLIT_COLLAPSE_RETURNS",
    "COMP_SPLIT_PAIR27_37_STALLS",
    "COMP_SPLIT_LOW_RESCHEDULE",
    "COMP_SPLIT_EXACT_CANDIDATE",
    "COMP_SPLIT_INCONSISTENT",
    "COMP_SPLIT_TIMEOUT",
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
    require(record["source_commit"] == "976d215", "wrong source commit")
    require(record["construction_mode"] == "compensated_split_replace", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["pre_split_pair_B_values"] == [1024, 577, 576, 1024, 1024], "wrong pre-split pairs")
    require(baseline["pre_split_capacity"] == 384, "wrong pre-split capacity")
    require(baseline["post_split_pair_B_values"] == [1024, 593, 592, 1024, 1024], "wrong post-split pairs")
    require(baseline["post_split_capacity"] == 315, "wrong post-split capacity")
    require(baseline["post_split_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong collapse")
    require(baseline["split_gain_B27_B37"] == [16, 16], "wrong split gain")
    require(baseline["capacity_loss"] == 69, "wrong capacity loss")

    exchange = record["compensated_exchange"]
    require(exchange["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exchange["base_system"] == "scalable_pairclass_overlap_all_extension96", "wrong base system")
    require(exchange["split_candidates"] == 5, "wrong split candidate count")
    require(
        exchange["exchange_types"]
        == [
            "one_for_one_same_fiber",
            "one_for_two_same_fiber",
            "one_for_two_neighbor_fiber",
            "one_for_two_balanced",
            "one_for_two_pair57_restore",
            "one_for_two_capacity_backfill",
        ],
        "wrong exchange types",
    )
    require(exchange["systems_tested"] == 30, "wrong system count")
    require(exchange["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(exchange["timeouts"] == 0, "unexpected timeout count")
    require(exchange["exact_vectors_constructed"] == 30, "wrong exact vector count")
    require(exchange["capacity_restored_vectors"] == 0, "wrong capacity-restored count")
    require(exchange["pair27_37_improved_vectors"] == 30, "wrong pair27/37-improved count")
    require(exchange["pair57_preserving_vectors"] == 30, "wrong pair57-preserving count")
    require(exchange["collapse_reduced_vectors"] == 30, "wrong collapse-reduced count")
    require(exchange["best_pair_B_values"] == [1024, 593, 592, 1024, 1024], "wrong best pair values")
    require(exchange["best_capacity_upper_bound"] == 315, "wrong best capacity")
    require(exchange["best_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong best collapse")
    require(exchange["best_exact_max_min"] is None, "unexpected exact max-min")
    require(exchange["best_failure_mode"] == "COMP_SPLIT_CAPACITY_NOT_RESTORED", "wrong best failure")
    require(exchange["failure_mode_counts"] == {"COMP_SPLIT_CAPACITY_NOT_RESTORED": 30}, "wrong failure counts")

    exact_candidate_count = 0
    vector_count = 0
    for result in exchange["results"]:
        require(result["failure_mode"] in ALLOWED_FAILURES, f"bad result failure {result['failure_mode']}")
        for row in result.get("vector_results", []):
            vector_count += 1
            require(row["failure_mode"] in ALLOWED_FAILURES, f"bad vector failure {row['failure_mode']}")
            if row["failure_mode"] == "COMP_SPLIT_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(row["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(vector_count == exchange["exact_vectors_constructed"], "vector count mismatch")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": exchange["systems_tested"],
        "exact_vectors_constructed": exchange["exact_vectors_constructed"],
        "capacity_restored_vectors": exchange["capacity_restored_vectors"],
        "pair27_37_improved_vectors": exchange["pair27_37_improved_vectors"],
        "pair57_preserving_vectors": exchange["pair57_preserving_vectors"],
        "collapse_reduced_vectors": exchange["collapse_reduced_vectors"],
        "best_pair_B_values": exchange["best_pair_B_values"],
        "best_capacity_upper_bound": exchange["best_capacity_upper_bound"],
        "best_collapse_pattern": exchange["best_collapse_pattern"],
        "best_failure_mode": exchange["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 compensated split-replace ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
