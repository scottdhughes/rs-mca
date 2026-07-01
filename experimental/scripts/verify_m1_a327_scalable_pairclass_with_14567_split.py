#!/usr/bin/env python3
"""Verifier for scalable pair-class creation with [1,4,5,6,7] split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_scalable_pairclass_with_14567_split.json")
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
    "PAIRCLASS_GROWTH_STALLS",
    "PAIRCLASS_SPLIT_INCONSISTENT",
    "PAIRCLASS_SPLIT_CAPACITY_LOSS",
    "PAIRCLASS_SPLIT_PAIR_LOSS",
    "PAIRCLASS_SPLIT_LOW_RESCHEDULE",
    "PAIRCLASS_SPLIT_TIMEOUT",
    "PAIRCLASS_EXACT_CANDIDATE",
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
    require(record["source_commit"] == "e99acf6", "wrong source commit")
    require(record["construction_mode"] == "scalable_pairclass_with_14567_split", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["best_pair_B_values"] == [1024, 577, 576, 1024, 1024], "wrong baseline pair values")
    require(baseline["best_capacity_upper_bound"] == 384, "wrong baseline capacity")
    require(baseline["collapse_pattern"] == [[1, 4, 5, 6, 7], [3], [2]], "wrong baseline collapse")
    require(baseline["pair27_deficit_to_654"] == 77, "wrong pair27 deficit")
    require(baseline["pair37_deficit_to_654"] == 78, "wrong pair37 deficit")

    search = record["pairclass_split_search"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["target_sizes"] == [128], "wrong target sizes")
    require(search["systems_tested"] == 12, "wrong system count")
    require(search["pair_row_extensions"] == [32, 64, 96], "wrong pair extensions")
    require(
        search["split_families"]
        == ["split_7_from_1456", "split_14_567", "split_145_67", "chain_split_14567"],
        "wrong split families",
    )
    require(search["free_patterns"] == ["d2_first_free", "d2_first4_free", "d2_even_sparse"], "wrong free patterns")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(search["case_timeout_seconds"] == 55, "wrong timeout")
    require(search["timeouts"] == 0, "unexpected timeout count")
    require(search["exact_vectors_constructed"] == 36, "wrong exact vector count")
    require(search["capacity_preserving_vectors"] == 0, "unexpected capacity-preserving vector")
    require(search["pair_values_improved_vectors"] == 12, "wrong pair-improved count")
    require(search["collapse_reduced_vectors"] == 36, "wrong collapse-reduced count")
    require(search["failure_mode_counts"] == {"PAIRCLASS_SPLIT_CAPACITY_LOSS": 36}, "wrong failure counts")
    require(search["best_pair_B_values"] == [1024, 593, 592, 1024, 514], "wrong best pair values")
    require(search["best_capacity_upper_bound"] == 315, "wrong best capacity")
    require(search["best_collapse_pattern"] == [[1, 4, 6, 7], [5], [3], [2]], "wrong best collapse")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["best_failure_mode"] == "PAIRCLASS_SPLIT_CAPACITY_LOSS", "wrong best failure")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")

    exact_candidate_count = 0
    vector_count = 0
    for result in search["results"]:
        require(result["failure_mode"] in ALLOWED_FAILURES, f"bad result failure {result['failure_mode']}")
        require(result["failure_mode"] == "PAIRCLASS_SPLIT_CAPACITY_LOSS", "wrong case failure")
        require(result["rank_after"] == result["row_count"], "rank/row mismatch")
        for row in result.get("vector_results", []):
            vector_count += 1
            require(row["failure_mode"] in ALLOWED_FAILURES, f"bad vector failure {row['failure_mode']}")
            require(row["failure_mode"] == "PAIRCLASS_SPLIT_CAPACITY_LOSS", "wrong vector failure")
            require(row["collapse_reduced"] is True, "collapse was not reduced")
            require(row["distinct_codewords"] is False, "unexpected distinct codewords")
            require(row["capacity_upper_bound"] < TARGET_AGREEMENT, "capacity unexpectedly preserved")
            if row["pair_row_extension"] == 32:
                require(row["pair_B_values"][1:3] == [561, 560], "wrong extension-32 weak pairs")
            elif row["pair_row_extension"] == 64:
                require(row["pair_B_values"][1:3] == [577, 576], "wrong extension-64 weak pairs")
            elif row["pair_row_extension"] == 96:
                require(row["pair_B_values"][1:3] == [593, 592], "wrong extension-96 weak pairs")
            else:
                raise AssertionError("unexpected pair-row extension")
            if row["failure_mode"] == "PAIRCLASS_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(row["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(vector_count == search["exact_vectors_constructed"], "vector count mismatch")
    require(record["proof_status"] == "EXACT_EXTRACTION_NO_A327", "wrong proof status")
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
        "pair_values_improved_vectors": search["pair_values_improved_vectors"],
        "collapse_reduced_vectors": search["collapse_reduced_vectors"],
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
            "PASS: M1 a=327 scalable pairclass with 14567 split "
            f"({result['systems_tested']} systems)"
        )


if __name__ == "__main__":
    main()
