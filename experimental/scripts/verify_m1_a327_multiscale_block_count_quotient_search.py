#!/usr/bin/env python3
"""Verify M1 a=327 multiscale block-count quotient search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_multiscale_block_count_quotient_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_multiscale_block_count_quotient_search.md")


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
    require(record["source_commit"] == "f5dcd61", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    for claim in ["MCA N_bad", "protocol soundness", "Sage GF(17^32) exact lift"]:
        require(claim in record["not_claimed"], f"missing nonclaim: {claim}")

    previous = record["previous_order8_block_count"]
    require(previous["ambient_pair_cap_feasible"] is False, "previous order8 status changed")

    search = record["multiscale_search"]
    require(search["orders_tested"] == [16, 32], "unexpected quotient orders")
    require(search["block_sizes"] == [1, 2, 3, 4, 5, 6, 7], "unexpected block sizes")
    require(search["models_tested"] == 8, "wrong diagnostic model count")
    require(search["best_failure_mode"].startswith("MULTISCALE_"), "bad failure label")

    for result in record["results"]:
        order = result["quotient_order"]
        require(order in {16, 32}, "unexpected order result")
        require(result["bucket_size"] * order == 512, "bucket/order mismatch")
        require(result["degree_bound"] == 255 // result["bucket_size"], "bad degree bound")
        if order == 16:
            require(result["field"] == "GF(17)", "wrong order16 field")
        if order == 32:
            require(result["field"] == "GF(17^2)", "wrong order32 field")
        for model in result["models"]:
            if not model["feasible"]:
                continue
            require(model["support_vector"] == [327] * 7, "support vector changed")
            if model["mode"] in {"pair7_guard", "pair_cap", "ambient_pair_cap"}:
                require(min(model["pair7_counts"]) >= 142, "pair7 guard failed")
            if model["mode"] in {"pair_cap", "ambient_pair_cap"}:
                require(max(model["selected_pair_counts"].values()) <= 255, "selected pair cap failed")
            if model["mode"] == "ambient_pair_cap":
                require(model["max_ambient_pair_buckets"] <= result["degree_bound"], "ambient cap failed")
        audit = result["interpolation_audit"]
        if audit["attempted"]:
            expected_cols = 6 * (result["degree_bound"] + 1)
            require(audit["matrix_shape"][1] == expected_cols, "wrong interpolation variable count")
            require(audit["rank"] + audit["nullity"] == expected_cols, "rank/nullity mismatch")
            if audit["candidate_constructed"]:
                require(not audit["forced_equal_pairs"], "candidate has forced equal pairs")

    if search["candidate_orders"]:
        expected = "CANDIDATE / MULTISCALE_QUOTIENT_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
    elif any(result["summary"]["interpolation_audit_attempted"] for result in record["results"]):
        expected = "EXACT_EXTRACTION_NO_A327 / MULTISCALE_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
    elif all(result["summary"]["ambient_pair_cap_feasible"] is False for result in record["results"]):
        expected = "EXACT_EXTRACTION_NO_A327 / MULTISCALE_AMBIENT_INFEASIBLE / PARTIAL / EXPERIMENTAL"
    else:
        expected = "EXACT_EXTRACTION_NO_A327 / MULTISCALE_CP_UNRESOLVED / PARTIAL / EXPERIMENTAL"
    require(record["proof_status"] == expected, "wrong proof status")
    for phrase in ["MULTISCALE", "order 16", "order 32", "not an MCA row"]:
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
        print(f"PASS: M1 a=327 multiscale block-count quotient search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
