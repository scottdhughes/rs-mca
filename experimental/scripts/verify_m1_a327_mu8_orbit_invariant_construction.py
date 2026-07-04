#!/usr/bin/env python3
"""Verify the M1 a=327 mu_8 orbit-invariant construction ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_mu8_orbit_invariant_construction.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_mu8_orbit_invariant_construction.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "2e551d7", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    model = record["mu8_orbit_model"]
    require(model["field"] == "GF(17^32)", "wrong field")
    require(model["H_order"] == 512, "wrong H order")
    require(model["mu_order"] == 8, "wrong mu order")
    require(model["quotient_order"] == 64, "wrong quotient order")
    require(model["unknowns"] == 224, "wrong unknown count")
    require(model["target_support_per_codeword"] == 328, "wrong support target")
    search = record["search"]
    require(search["schedules_tested"] == 29, "wrong schedule count")
    require(search["guard_passing_schedules"] == 9, "wrong guard-passing count")
    require(search["positive_nullity_schedules"] == 0, "unexpected positive nullity")
    require(search["exact_candidates"] == 0, "unexpected exact candidate")
    require(search["best_rank"] == 224, "wrong best rank")
    require(search["best_nullity"] == 0, "wrong best nullity")
    require(search["best_failure_mode"] == "MU8_ORBIT_NULLITY_ZERO", "wrong best failure")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / MU8_ORBIT_NULLITY_ZERO_FRONT / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )
    guard_passing = [row for row in record["schedule_results"] if row["status"] != "MU8_SCHEDULE_GUARD_FAIL"]
    require(len(guard_passing) == 9, "guard-passing rows mismatch")
    for row in guard_passing:
        require(row["support_per_codeword"] == 328, f"{row['schedule_id']}: wrong support")
        require(row["ambient_pair_bound"] <= 255, f"{row['schedule_id']}: ambient pair cap fail")
        require(row["matrix_shape"] == [264, 224], f"{row['schedule_id']}: wrong matrix shape")
        require(row["rank"] == 224, f"{row['schedule_id']}: not full column rank")
        require(row["nullity"] == 0, f"{row['schedule_id']}: unexpected nullity")
    for phrase in [
        "mu_8 orbit-invariant",
        "29",
        "9",
        "224/0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "schedules_tested": search["schedules_tested"],
        "guard_passing_schedules": search["guard_passing_schedules"],
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
        print("PASS: M1 a=327 mu_8 orbit-invariant construction ledger")


if __name__ == "__main__":
    main()
