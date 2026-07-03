#!/usr/bin/env python3
"""Verify the M1 a=327 low-rank forced-identity repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_forced_identity_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_lowrank_template_forced_identity_repair.md")

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
    "LOWRANK_REPAIR_PROXY_NOT_POSITIVE",
    "LOWRANK_REPAIR_FORCED_SPAN_COLLAPSES",
    "LOWRANK_REPAIR_REDUCED_DIM_TOO_SMALL",
    "LOWRANK_REPAIR_FORCED_PAIR_EQUALITY",
    "LOWRANK_REPAIR_SATURATION_PASS",
    "LOWRANK_REPAIR_NO_SURVIVOR",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify_candidate(row: dict[str, Any]) -> None:
    require(row["best_failure_mode"] in ALLOWED_FAILURES, "bad candidate failure")
    require(row["support_vector"] == [TARGET_AGREEMENT] * 7, "bad support vector")
    require(row["proxy_rank"] is None or row["proxy_rank"] + row["proxy_nullity"] == row["variable_count"], "bad proxy rank/nullity")
    sat = row["saturation"]
    require(sat["reduced_template_dimension"] == row["template_dimension"] - sat["forced_rank"], "bad reduced dimension")
    require(sat["min_pair_projection_rank"] in (0, 1), "bad min projection rank")
    require(len(sat["pair_projection_rank_by_pair"]) == 21, "bad projection rank count")
    if row["best_failure_mode"] == "LOWRANK_REPAIR_SATURATION_PASS":
        require(row["proxy_nullity"] and row["proxy_nullity"] > 0, "passing candidate is not proxy positive")
        require(sat["reduced_template_dimension"] >= 2, "passing candidate has low dimension")
        require(not sat["forced_equal_pairs"], "passing candidate has forced pairs")
        require(sat["min_pair_projection_rank"] == 1, "passing candidate has zero pair projection")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "ff3c0da", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_lowrank_search"]
    require(previous["proxy_positive_candidates"] == 8, "wrong previous proxy-positive count")
    require(previous["best_proxy_rank"] == 1280, "wrong previous best proxy rank")
    require(previous["best_proxy_nullity"] == 256, "wrong previous best proxy nullity")

    search = record["forced_identity_repair"]
    require(search["candidates_tested"] == 10, "wrong candidate count")
    require(search["proxy_positive_candidates"] == 8, "wrong proxy-positive count")
    require(search["saturation_pass_candidates"] == 2, "wrong saturation-pass count")
    require(search["best_failure_mode"] == "LOWRANK_REPAIR_SATURATION_PASS", "wrong search failure")
    require(search["best_template_id"] == "random_matroid_seeded_0_m6", "wrong best template")
    require(search["best_reduced_template_dimension"] == 6, "wrong best reduced dimension")
    require(search["best_forced_equal_pair_count"] == 0, "wrong best forced pair count")
    require(search["failure_counts"]["LOWRANK_REPAIR_SATURATION_PASS"] == 2, "bad pass failure count")
    for row in search["candidates"]:
        verify_candidate(row)

    best = record["best_candidate"]
    require(best is not None, "missing best candidate")
    verify_candidate(best)
    require(best["template_id"] == search["best_template_id"], "best candidate mismatch")

    sage = record["sage_exact_check"]
    require(sage["field"] == "GF(17^32)", "wrong Sage field")
    if sage["run"]:
        require(sage["best_template_id"] == "random_matroid_seeded_0_m6", "wrong Sage template")
        require(sage["forced_rank"] == 0, "wrong Sage forced rank")
        require(sage["reduced_template_dimension"] == 6, "wrong Sage reduced dimension")
        require(sage["forced_equal_pairs"] == 0, "wrong Sage forced pair count")
        require(sage["status"] == "PASS", "Sage check did not pass")

    for phrase in [
        "forced-identity saturation",
        "random_matroid_seeded_0_m6",
        "mixed_rank6",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "saturation_pass_candidates": search["saturation_pass_candidates"],
        "best_template_id": search["best_template_id"],
        "best_reduced_template_dimension": search["best_reduced_template_dimension"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 low-rank forced-identity repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
