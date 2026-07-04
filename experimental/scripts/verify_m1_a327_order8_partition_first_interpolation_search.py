#!/usr/bin/env python3
"""Verify M1 a=327 order-8 partition-first interpolation search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_order8_partition_first_interpolation_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_order8_partition_first_interpolation_search.md")


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
    require(record["source_commit"] == "bcb9ac5", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    for claim in ["MCA N_bad", "protocol soundness", "Sage GF(17^32) exact lift"]:
        require(claim in record["not_claimed"], f"missing nonclaim: {claim}")

    previous = record["previous_order8_degree3_codesign"]
    require(previous["feasible_allocations"] == 0, "unexpected previous feasible allocation")

    search = record["partition_first_search"]
    require(search["variable_count"] == 24, "wrong variable count")
    require(search["best_failure_mode"].startswith("PARTITION_FIRST_"), "bad failure label")
    for model in record["models"]:
        if not model["feasible"]:
            continue
        require(model["support_vector"] == [327] * 7, "support vector changed")
        require(min(model["pair7_counts"]) >= 142, "pair7 guard failed")
        require(model["max_ambient_pair_buckets"] <= 3, "ambient pair cap failed")
        require(model["equation_count"] is not None, "missing equation count")

    audit = record["interpolation_audit"]
    if audit["attempted"]:
        require(audit["matrix_shape"][1] == 24, "wrong interpolation variable count")
        require(audit["rank"] + audit["nullity"] == 24, "rank/nullity mismatch")
        if audit["candidate_constructed"]:
            require(not audit["forced_equal_pairs"], "candidate has forced equal pairs")
            require(record["candidate"]["agreement_vector"] == [327] * 7, "candidate support changed")

    expected = (
        "CANDIDATE / PARTITION_FIRST_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        if search["candidate_constructed"]
        else "EXACT_EXTRACTION_NO_A327 / PARTITION_FIRST_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected, "wrong proof status")
    for phrase in ["PARTITION_FIRST", "degree-3 interpolation", "CP-SAT", "not an MCA row"]:
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
        print(f"PASS: M1 a=327 order-8 partition-first interpolation search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
