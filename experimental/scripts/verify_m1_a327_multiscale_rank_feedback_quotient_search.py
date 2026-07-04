#!/usr/bin/env python3
"""Verify M1 a=327 multiscale rank-feedback quotient search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_multiscale_rank_feedback_quotient_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_multiscale_rank_feedback_quotient_search.md")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict:
    record = load_json(DATA_PATH)
    note = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong target")
    require(record["source_commit"] == "a1f304c", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    for claim in ["MCA N_bad", "protocol soundness", "Sage GF(17^32) exact lift"]:
        require(claim in record["not_claimed"], f"missing nonclaim: {claim}")

    previous = record["previous_multiscale"]
    require(previous["best_failure_mode"] == "MULTISCALE_INTERPOLATION_NO_CANDIDATE", "previous status changed")

    search = record["rank_feedback_search"]
    require(search["orders_tested"] == [16, 32], "unexpected quotient orders")
    require(search["block_sizes"] == [1, 2, 3, 4, 5, 6, 7], "unexpected block sizes")
    require(search["best_failure_mode"].startswith("RANK_FEEDBACK_"), "bad failure label")
    require(search["total_samples_tested"] >= 1, "no rank-feedback samples tested")

    for result in record["results"]:
        require(result["quotient_order"] in {16, 32}, "unexpected order")
        require(result["bucket_size"] * result["quotient_order"] == 512, "bucket/order mismatch")
        require(result["degree_bound"] == 255 // result["bucket_size"], "bad degree bound")
        structural = result["structural_defect_screen"]
        require(structural["best_failure_mode"].startswith("RANK_FEEDBACK_STRUCTURAL_DEFECT_"), "bad structural label")
        for sample in result["samples"]:
            if "interpolation_audit" not in sample:
                continue
            schedule = sample["schedule"]
            audit = sample["interpolation_audit"]
            require(schedule["support_vector"] == [327] * 7, "support vector changed")
            require(min(schedule["pair7_counts"]) >= 142, "pair7 guard failed")
            require(max(schedule["selected_pair_counts"].values()) <= 255, "selected pair cap failed")
            require(schedule["max_ambient_pair_buckets"] <= result["degree_bound"], "ambient cap failed")
            expected_cols = 6 * (result["degree_bound"] + 1)
            require(audit["matrix_shape"][1] == expected_cols, "wrong interpolation variable count")
            require(audit["rank"] + audit["nullity"] == expected_cols, "rank/nullity mismatch")
            if audit["candidate_constructed"]:
                require(not audit["forced_equal_pairs"], "candidate has forced equal pairs")

    if search["candidate_orders"]:
        expected = "CANDIDATE / RANK_FEEDBACK_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
    elif search["positive_nullity_orders"]:
        expected = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_POSITIVE_NULLITY_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
    elif all(result["best_failure_mode"] == "RANK_FEEDBACK_FULL_RANK_FRONT" for result in record["results"]):
        expected = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_FULL_RANK_FRONT / PARTIAL / EXPERIMENTAL"
    else:
        expected = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_CP_UNRESOLVED / PARTIAL / EXPERIMENTAL"
    require(record["proof_status"] == expected, "wrong proof status")
    for phrase in ["RANK_FEEDBACK", "no-good", "positive nullity", "not an MCA row"]:
        require(phrase in note, f"note missing phrase: {phrase}")
    return {"status": "PASS", "proof_status": record["proof_status"], **search}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 multiscale rank-feedback quotient search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
