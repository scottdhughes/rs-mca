#!/usr/bin/env python3
"""Verify the M1 a=327 order-8 degree-3 partition codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_order8_degree3_partition_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_order8_degree3_partition_codesign.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
}


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
    require(record["source_commit"] == "4e6fb16", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_primal_kernel_codesign"]
    require(previous["locator_feasible_allocations"] == 0, "unexpected previous feasible allocation")

    search = record["order8_degree3_codesign"]
    require(search["field"] == "GF(17)", "wrong field")
    require(len(search["order8_domain"]) == 8, "wrong order-8 domain")
    require(search["degree_in_X"] == 192, "wrong degree")
    require(search["candidates_tested"] >= search["candidate_trials"], "candidate count too small")
    require(search["best_failure_mode"].startswith("ORDER8_DEGREE3_") or search["best_failure_mode"].startswith("ORDER8_PARTITION_"), "bad failure label")

    for attempt in [*record["attempt_sample"], record["best_candidate"]]:
        require(len(attempt["coefficients_by_witness"]) == 6, "wrong coefficient count")
        require(len(attempt["zero_counts_by_witness"]) == 6, "wrong zero-count vector")
        require(attempt["max_ambient_pair_count"] <= 512, "bad ambient pair count")
        if attempt["allocation_feasible"]:
            require(attempt["allocation_support_vector"] == [327] * 7, "support vector changed")
            require(min(attempt["allocation_pair7_counts"]) >= 142, "pair7 guard failed")
            require(attempt["max_ambient_pair_count"] <= 255, "ambient pair cap failed")

    expected = (
        "CANDIDATE / ORDER8_DEGREE3_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        if search["exact_candidates"] > 0
        else "EXACT_EXTRACTION_NO_A327 / ORDER8_DEGREE3_NO_ALLOCATION / PARTIAL / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected, "wrong proof status")
    require(record["candidate"]["constructed"] is (search["exact_candidates"] > 0), "candidate flag mismatch")

    for phrase in ["ORDER8_DEGREE3", "partition-first", "degree-3", "not an MCA row"]:
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
        print(f"PASS: M1 a=327 order-8 degree-3 partition codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
