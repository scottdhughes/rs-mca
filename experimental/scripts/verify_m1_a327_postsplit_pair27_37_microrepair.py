#!/usr/bin/env python3
"""Verifier for post-split pair {2,7}/{3,7} microrepair."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_postsplit_pair27_37_microrepair.json")
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
    "MICROREPAIR_PAIRCLASS_NOT_REPAIRED",
    "MICROREPAIR_CAPACITY_LOSS",
    "MICROREPAIR_PAIR57_LOSS",
    "MICROREPAIR_COLLAPSE_RETURNS",
    "MICROREPAIR_LOW_RESCHEDULE",
    "MICROREPAIR_EXACT_CANDIDATE",
    "MICROREPAIR_INCONSISTENT",
    "MICROREPAIR_TIMEOUT",
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
    require(record["source_commit"] == "6c54e44", "wrong source commit")
    require(record["construction_mode"] == "postsplit_pair27_37_microrepair", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["post_split_capacity"] == 329, "wrong baseline post capacity")
    require(baseline["post_split_pair_B_values"] == [1024, 641, 640, 1024, 1024], "wrong baseline pairs")
    require(baseline["B27_deficit"] == 13, "wrong baseline B27 deficit")
    require(baseline["B37_deficit"] == 14, "wrong baseline B37 deficit")
    require(baseline["collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong baseline collapse")
    require(baseline["failure_mode"] == "RESERVE_NOT_CREATED", "wrong baseline failure")

    search = record["microrepair"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["base_system"] == "reserve_pairclass_codesign_quotient_fiber_buffer_extension96", "wrong base system")
    require(search["repair_budgets"] == [8], "wrong repair budgets")
    require(search["planned_repair_budgets"] == [8, 16, 24, 32], "wrong planned repair budgets")
    require(
        search["planned_repair_families"]
        == [
            "pair27_micro",
            "pair37_micro",
            "balanced_pair27_37_micro",
            "triple_237",
            "postsplit_survivor_pair_micro",
            "quotient_fiber_pair27_37_micro",
        ],
        "wrong planned repair families",
    )
    require(search["repair_families"] == ["triple_237"], "wrong repair families")
    require(search["systems_tested"] == 1, "wrong system count")
    require(search["timeouts"] >= 0, "bad timeout count")
    require(search["exact_vectors_constructed"] <= search["systems_tested"], "too many exact vectors")
    require(search["capacity_preserving_vectors"] <= search["exact_vectors_constructed"], "bad capacity count")
    require(search["pair27_37_repaired_vectors"] <= search["exact_vectors_constructed"], "bad repair count")
    require(search["pair57_preserving_vectors"] <= search["exact_vectors_constructed"], "bad pair57 count")
    require(search["collapse_preserving_vectors"] <= search["exact_vectors_constructed"], "bad collapse count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(len(search["results"]) == search["systems_tested"], "wrong result length")

    exact_candidate_count = 0
    for result in search["results"]:
        failure = result["failure_mode"]
        require(failure in ALLOWED_FAILURES, f"bad result failure {failure}")
        if failure == "MICROREPAIR_TIMEOUT":
            require("timeout_seconds" in result, "timeout missing seconds")
            continue
        if result.get("pair_B_values") is None:
            require(failure == "MICROREPAIR_INCONSISTENT", "missing pair values outside inconsistent result")
            continue
        pair_values = result["pair_B_values"]
        require(len(pair_values) == 5, "wrong pair vector length")
        if failure == "MICROREPAIR_EXACT_CANDIDATE":
            exact_candidate_count += 1
            require(result.get("exact_max_min", -1) >= TARGET_AGREEMENT, "candidate below target")
            require(pair_values[1] >= PAIR_TARGET and pair_values[2] >= PAIR_TARGET, "candidate pair deficit")
            require(pair_values[4] >= PAIR_TARGET, "candidate pair57 deficit")
            require(result.get("capacity_upper_bound", 0) >= TARGET_AGREEMENT, "candidate capacity deficit")

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
        "capacity_preserving_vectors": search["capacity_preserving_vectors"],
        "pair27_37_repaired_vectors": search["pair27_37_repaired_vectors"],
        "pair57_preserving_vectors": search["pair57_preserving_vectors"],
        "best_capacity": search["best_capacity"],
        "best_pair_B_values": search["best_pair_B_values"],
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
        print(f"PASS: M1 a=327 post-split pair27/37 microrepair ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
