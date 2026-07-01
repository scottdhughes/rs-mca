#!/usr/bin/env python3
"""Verifier for scalable M1 a=327 pair {2,7}/{3,7} class creation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pair27_37_class_creation_scalable.json")
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
    "SCALABLE_SYSTEM_TIMEOUT",
    "SCALABLE_SYSTEM_FULL_RANK",
    "PAIR_CLASS_PARTIAL_REPAIR",
    "PAIR_CLASS_CAPACITY_LOSS",
    "PAIR_CLASS_UNDOES_D2_SPLIT",
    "PAIR_CLASS_COLLAPSE_RETURNS",
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
    require(record["source_commit"] == "07e987c", "wrong source commit")
    require(record["construction_mode"] == "pair27_37_class_creation_scalable", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["systems_tested"] == 6, "wrong baseline systems")
    require(baseline["best_pair_B_values"] == [1024, 545, 544, 1024, 1024], "wrong baseline pairs")
    require(baseline["best_capacity_upper_bound"] == 375, "wrong baseline capacity")
    require(baseline["D2_split"] is True, "baseline D2 split missing")
    require(baseline["low_collapse_vectors"] == 2, "wrong baseline low-collapse count")
    require(baseline["failure_mode"] == "PAIR_CLASS_PARTIAL_REPAIR", "wrong baseline failure")

    search = record["scalable_class_creation"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["T27_sizes"] == [64, 96], "wrong T27 sizes")
    require(search["T37_sizes"] == [64, 96], "wrong T37 sizes")
    require(search["designs_tested"] == ["overlap_all", "same_fiber_shifted", "disjoint_low_high"], "wrong designs")
    require(search["extension_row_blocks"] == [32, 64], "wrong row blocks")
    require(search["systems_tested"] == 12, "wrong system count")
    require(search["incremental_blocks_tested"] == 12, "wrong block count")
    require(search["case_timeout_seconds"] == 35, "wrong timeout")
    require(search["timeouts"] == 0, "unexpected timeout count")
    require(search["exact_vectors_constructed"] == 12, "wrong exact vector count")
    require(search["D2_split_vectors"] == 12, "wrong D2 split count")
    require(search["low_collapse_vectors"] == 10, "wrong low-collapse count")
    require(search["pair27_repaired_vectors"] == 0, "unexpected pair27 repair")
    require(search["pair37_repaired_vectors"] == 0, "unexpected pair37 repair")
    require(search["full_pair_repaired_vectors"] == 0, "unexpected full pair repair")
    require(search["failure_mode_counts"] == {
        "PAIR_CLASS_COLLAPSE_RETURNS": 2,
        "PAIR_CLASS_PARTIAL_REPAIR": 10,
    }, "wrong failure counts")
    require(search["best_pair_B_values"] == [1024, 577, 576, 1024, 1024], "wrong best pair values")
    require(search["best_B27"] == 577, "wrong best B27")
    require(search["best_B37"] == 576, "wrong best B37")
    require(search["best_capacity_upper_bound"] == 384, "wrong best capacity")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["best_failure_mode"] == "PAIR_CLASS_PARTIAL_REPAIR", "wrong best failure")
    require(search["pair27_repaired_vectors"] >= search["full_pair_repaired_vectors"], "bad pair27 count")
    require(search["pair37_repaired_vectors"] >= search["full_pair_repaired_vectors"], "bad pair37 count")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")

    exact_candidate_count = 0
    for row in search["results"]:
        require(row["failure_mode"] in ALLOWED_FAILURES, f"bad failure mode {row['failure_mode']}")
        require(row["d2_split"] is True, "D2 split was not retained")
        require(row["distinct_codewords"] is False, "unexpected distinct codewords")
        require(row["capacity_upper_bound"] in {379, 384}, "wrong capacity value")
        require(row["degenerate_classes"] == [[1, 4, 5, 6, 7], [3], [2]], "wrong degeneracy pattern")
        if row["extension_row_block"] == 32:
            require(row["pair_B_values"] == [1024, 561, 560, 1024, 1024], "wrong block-32 pair values")
            require(row["row_count"] == 161, "wrong block-32 row count")
            require(row["rank_after"] == 161, "wrong block-32 rank")
            require(row["nullity_after"] == 1375, "wrong block-32 nullity")
        elif row["extension_row_block"] == 64:
            require(row["pair_B_values"] == [1024, 577, 576, 1024, 1024], "wrong block-64 pair values")
            require(row["row_count"] == 193, "wrong block-64 row count")
            require(row["rank_after"] == 193, "wrong block-64 rank")
            require(row["nullity_after"] == 1343, "wrong block-64 nullity")
        else:
            raise AssertionError("unexpected extension row block")
        if row["failure_mode"] == "PAIR_CLASS_EXACT_CANDIDATE":
            exact_candidate_count += 1
            require(row["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
            require(min(row["pair_B_values"]) >= PAIR_TARGET, "candidate pair values below target")
    require(record["proof_status"] == "EXACT_EXTRACTION_NO_A327", "wrong proof status")
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
        "D2_split_vectors": search["D2_split_vectors"],
        "low_collapse_vectors": search["low_collapse_vectors"],
        "pair27_repaired_vectors": search["pair27_repaired_vectors"],
        "pair37_repaired_vectors": search["pair37_repaired_vectors"],
        "full_pair_repaired_vectors": search["full_pair_repaired_vectors"],
        "best_pair_B_values": search["best_pair_B_values"],
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
            "PASS: M1 a=327 scalable pair27/37 class creation "
            f"({result['systems_tested']} systems)"
        )


if __name__ == "__main__":
    main()
