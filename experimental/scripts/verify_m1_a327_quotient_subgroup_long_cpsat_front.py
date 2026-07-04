#!/usr/bin/env python3
"""Verify the M1 a=327 quotient-subgroup long CP-SAT front ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_long_cpsat_front.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_long_cpsat_front.md")


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
    require(record["source_commit"] == "59b268b", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    previous = record["previous_quotient_subgroup_rank_aware_schedule_generator"]
    require(previous["proxy_positive_schedules"] == 0, "unexpected previous proxy positive")
    require(previous["best_proxy_rank"] == 384, "wrong previous proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous proxy nullity")
    front = record["long_cpsat_front"]
    require(front["s_values"] == [8, 16, 32], "wrong s-values")
    require(front["screens_tested"] == len(record["screens"]), "wrong screen count")
    require(front["cp_feasible_screens"] <= front["screens_tested"], "bad feasible count")
    for screen in record["screens"]:
        require(screen["s"] in [8, 16, 32], "unexpected s")
        if screen["feasible"]:
            require(screen["support_vector"] == [327] * 7, "support changed")
            require(min(screen["pair7_counts"]) >= 142, "pair7 guard failed")
            require(screen["max_pair_equal_h_count"] <= 255, "pair cap failed")
    expected_status = (
        "CANDIDATE / LONG_CPSAT_QUOTIENT_CP_FEASIBLE / PARTIAL / EXPERIMENTAL"
        if front["cp_feasible_screens"] > 0
        else "PARTIAL / LONG_CPSAT_UNRESOLVED / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected_status, "wrong proof status")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")
    for phrase in ["LONG_CPSAT", "s = 8, 16, 32", "not an MCA row"]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {"status": "PASS", "proof_status": record["proof_status"], **front}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 quotient-subgroup long CP-SAT front (status={result['proof_status']})")


if __name__ == "__main__":
    main()
