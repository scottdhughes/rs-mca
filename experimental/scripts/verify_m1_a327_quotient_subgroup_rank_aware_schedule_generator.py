#!/usr/bin/env python3
"""Verify the M1 a=327 rank-aware quotient schedule-generator ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_rank_aware_schedule_generator.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_rank_aware_schedule_generator.md")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong target")
    require(record["source_commit"] == "7e21f1d", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")

    previous = record["previous_label_rank_feedback"]
    require(previous["labellings_tested"] == 72, "wrong previous labelled count")
    require(previous["proxy_positive_labellings"] == 0, "unexpected previous positive")
    require(previous["best_proxy_rank"] == 384, "wrong previous rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous nullity")

    search = record["rank_aware_schedule_generator"]
    require(search["schedules_tested"] == len(record["generated_schedules"]), "wrong schedule count")
    require(search["cp_feasible_schedules"] <= search["schedules_tested"], "bad feasible count")
    require(search["proxy_positive_schedules"] <= search["cp_feasible_schedules"], "bad positive count")
    if search["cp_feasible_schedules"]:
        require(search["best_proxy_rank"] <= 384, "rank too high")
        require(search["best_proxy_nullity"] == 384 - search["best_proxy_rank"], "bad nullity")
        require(search["best_matrix_shape"][1] == 384, "wrong matrix columns")
    for schedule in record["generated_schedules"]:
        if not schedule["feasible"]:
            continue
        require(schedule["support_vector"] == [327] * 7, "support changed")
        require(min(schedule["pair7_counts"]) >= 142, "pair7 guard failed")
        require(schedule["max_pair_equal_h_count"] <= 255, "pair cap failed")
        feedback = schedule["proxy_label_feedback"]
        require(feedback["best_proxy_nullity"] == 384 - feedback["best_proxy_rank"], "schedule nullity mismatch")

    expected_status = (
        "CANDIDATE / RANK_AWARE_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if search["proxy_positive_schedules"] > 0
        else "EXACT_EXTRACTION_NO_A327 / RANK_AWARE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
    )
    if search["cp_feasible_schedules"] == 0:
        expected_status = "PARTIAL / RANK_AWARE_CP_UNRESOLVED / EXPERIMENTAL"
    require(record["proof_status"] == expected_status, "wrong proof status")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")
    for phrase in ["RANK_AWARE", "GF(257)", "not an MCA row", "rank-aware schedule generator"]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {"status": "PASS", "proof_status": record["proof_status"], **search}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 rank-aware quotient schedule generator (status={result['proof_status']})")


if __name__ == "__main__":
    main()
