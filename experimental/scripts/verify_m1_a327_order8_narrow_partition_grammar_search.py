#!/usr/bin/env python3
"""Verify M1 a=327 order-8 narrow partition grammar search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_order8_narrow_partition_grammar_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_order8_narrow_partition_grammar_search.md")


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
    require(record["source_commit"] == "43a18ee", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    for claim in ["MCA N_bad", "protocol soundness", "Sage GF(17^32) exact lift"]:
        require(claim in record["not_claimed"], f"missing nonclaim: {claim}")

    previous = record["previous_partition_first"]
    require(previous["structural_defect_target_feasible"] is False, "previous structural target changed")
    require(previous["support_feasibility_feasible"] is False, "previous support status changed")

    search = record["narrow_grammar_search"]
    require(search["models_tested"] >= search["feasible_support_schedules"], "bad model counts")
    require(search["best_failure_mode"].startswith("NARROW_GRAMMAR_"), "bad failure label")
    require(search["root_patterns_generated"] <= search["root_patterns_requested"], "generated too many roots")

    for model in record["models"]:
        if not model["feasible"]:
            continue
        require(model["support_vector"] == [327] * 7, "support vector changed")
        require(min(model["pair7_counts"]) >= 142, "pair7 guard failed")
        require(max(model["selected_pair_counts"].values()) <= 255, "selected pair cap failed")
        require(model["max_ambient_pair_buckets"] <= 3, "ambient pair cap failed")
        require(model["equation_count"] is not None, "missing equation count")
        for witness, buckets in model["root_buckets_by_witness"].items():
            require(len(buckets) == 3, f"witness {witness} does not have three root buckets")

    audit = record["interpolation_audit"]
    if audit["attempted"]:
        require(audit["matrix_shape"][1] == 24, "wrong interpolation variable count")
        require(audit["rank"] + audit["nullity"] == 24, "rank/nullity mismatch")
        if audit["candidate_constructed"]:
            require(not audit["forced_equal_pairs"], "candidate has forced equal pairs")
            require(record["candidate"]["agreement_vector"] == [327] * 7, "candidate support changed")

    if search["exact_candidates"]:
        expected = "CANDIDATE / NARROW_GRAMMAR_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
    elif search["feasible_support_schedules"]:
        expected = (
            "EXACT_EXTRACTION_NO_A327 / NARROW_GRAMMAR_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
        )
    else:
        expected = "EXACT_EXTRACTION_NO_A327 / NARROW_GRAMMAR_NO_SUPPORT_SCHEDULE / PARTIAL / EXPERIMENTAL"
    require(record["proof_status"] == expected, "wrong proof status")
    for phrase in ["NARROW_GRAMMAR", "zero block", "degree-3 interpolation", "not an MCA row"]:
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
        print(f"PASS: M1 a=327 order-8 narrow partition grammar search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
