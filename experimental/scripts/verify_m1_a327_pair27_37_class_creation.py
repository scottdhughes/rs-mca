#!/usr/bin/env python3
"""Verifier for the M1 a=327 pair {2,7}/{3,7} class-creation packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pair27_37_class_creation.json")
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
    "PAIR_CLASS_SYSTEM_INCONSISTENT",
    "PAIR_CLASS_UNDOES_D2_SPLIT",
    "PAIR_CLASS_COLLAPSE_RETURNS",
    "PAIR_CLASS_CAPACITY_LOSS",
    "PAIR_CLASS_PARTIAL_REPAIR",
    "PAIR_CLASS_LOW_RESCHEDULE",
    "PAIR_CLASS_EXACT_CANDIDATE",
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
    require(record["source_commit"] == "618321c", "wrong source commit")
    require(record["construction_mode"] == "pair27_37_class_creation", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["B27"] == 514, "wrong baseline B27")
    require(baseline["B37"] == 513, "wrong baseline B37")
    require(baseline["deficit27"] == PAIR_TARGET - 514, "wrong deficit27")
    require(baseline["deficit37"] == PAIR_TARGET - 513, "wrong deficit37")
    require(baseline["pair27_shared_coordinates"] == [0, 18], "wrong pair27 shared coordinates")
    require(baseline["pair37_shared_coordinates"] == [18], "wrong pair37 shared coordinates")
    require(baseline["exchange_graph_feasible"] is False, "baseline exchange graph unexpectedly feasible")

    search = record["pair_class_creation"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["systems_tested"] == 6, "wrong system count")
    require(search["T27_sizes"] == [32], "wrong T27 sizes")
    require(search["T37_sizes"] == [32], "wrong T37 sizes")
    require(search["planned_larger_sizes"] == [64, 96, 128, 160], "wrong larger-size ledger")
    require(search["designs_tested"] == ["disjoint_low_high", "overlap_all", "even_odd"], "wrong designs")
    require(search["free_patterns"] == ["d2_first_free"], "wrong free patterns")
    require(search["exact_vectors_constructed"] == 6, "wrong exact vector count")
    require(search["D2_split_vectors"] == 6, "wrong D2 split count")
    require(search["low_collapse_vectors"] == 2, "wrong low-collapse count")
    require(search["pair27_repaired_vectors"] == 0, "unexpected pair27 repair")
    require(search["pair37_repaired_vectors"] == 0, "unexpected pair37 repair")
    require(search["full_pair_repaired_vectors"] == 0, "unexpected full pair repair")
    require(search["best_pair_values"] == [1024, 545, 544, 1024, 1024], "wrong best pair values")
    require(search["best_B27"] == 545, "wrong best B27")
    require(search["best_B37"] == 544, "wrong best B37")
    require(search["best_capacity_upper_bound"] == 375, "wrong best capacity")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["best_failure_mode"] == "PAIR_CLASS_PARTIAL_REPAIR", "wrong best failure")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")

    exact_candidate_count = 0
    system_count = 0
    total_attempts = 0
    failure_counts: dict[str, int] = {}
    for result in search["results"]:
        require(result["system_count"] == 3, "wrong per-candidate system count")
        require(result["vector_count"] == 3, "wrong per-candidate vector count")
        require(result["failure_mode_counts"] == {
            "PAIR_CLASS_COLLAPSE_RETURNS": 2,
            "PAIR_CLASS_PARTIAL_REPAIR": 1,
        }, "wrong per-candidate failure counts")
        system_count += len(result["systems"])
        for system in result["systems"]:
            require(system["best"]["failure_mode"] in ALLOWED_FAILURES, "bad system failure")
            require(len(system["vector_results"]) == 1, "wrong vector count per system")
            total_attempts += len(system["vector_results"])
            for row in system["vector_results"]:
                failure_counts[row["failure_mode"]] = failure_counts.get(row["failure_mode"], 0) + 1
                require(row["d2_split"] is True, "D2 split was not retained")
                require(row["capacity_upper_bound"] == 375, "wrong vector capacity")
                require(row["pair27_B"] == 545, "wrong vector B27")
                require(row["pair37_B"] == 544, "wrong vector B37")
                require(row["distinct_codewords"] is False, "unexpected distinct codewords")
            if system["best"]["failure_mode"] == "PAIR_CLASS_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(system["best"]["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(system_count == search["systems_tested"], "system count mismatch")
    require(total_attempts == search["exact_vectors_constructed"], "attempt count mismatch")
    require(failure_counts == {
        "PAIR_CLASS_COLLAPSE_RETURNS": 4,
        "PAIR_CLASS_PARTIAL_REPAIR": 2,
    }, "wrong total failure counts")
    require(record["proof_status"] == "EXACT_EXTRACTION_NO_A327", "wrong proof status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative extraction status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "D2_split_vectors": search["D2_split_vectors"],
        "low_collapse_vectors": search["low_collapse_vectors"],
        "pair27_repaired_vectors": search["pair27_repaired_vectors"],
        "pair37_repaired_vectors": search["pair37_repaired_vectors"],
        "full_pair_repaired_vectors": search["full_pair_repaired_vectors"],
        "best_pair_values": search["best_pair_values"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
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
            "PASS: M1 a=327 pair27/37 class creation "
            f"({result['systems_tested']} systems)"
        )


if __name__ == "__main__":
    main()
