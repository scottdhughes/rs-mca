#!/usr/bin/env python3
"""Verify adaptive rank-2 mu_8 ratio-column ledgers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ADAPTIVE_PATH = Path("experimental/data/m1_a327_mu8_rank2_adaptive_ratio_columns.json")
SCHEDULE_PATH = Path("experimental/data/m1_a327_mu8_rank2_adaptive_schedule_candidates.json")
NEAR_PATH = Path("experimental/data/m1_a327_mu8_rank2_adaptive_near_front_exact.json")
EXACT_PATH = Path("experimental/data/m1_a327_mu8_rank2_adaptive_exact_interpolation.json")
WITNESS_PATH = Path("experimental/data/m1_a327_mu8_rank2_adaptive_witness_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_mu8_rank2_adaptive_ratio_columns.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
SOURCE_COMMIT = "14684a5"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def check_header(name: str, record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", f"{name}: wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", f"{name}: wrong row")
    require(record["denominator"] == "17^32", f"{name}: wrong denominator")
    require(record["agreement_target"] == 327, f"{name}: wrong target")
    require(record["source_commit"] == SOURCE_COMMIT, f"{name}: wrong source commit")
    require(record["mca_counted"] is False, f"{name}: MCA counted")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), f"{name}: missing nonclaims")


def verify() -> dict[str, Any]:
    adaptive = load_json(ADAPTIVE_PATH)
    schedule = load_json(SCHEDULE_PATH)
    near = load_json(NEAR_PATH)
    exact = load_json(EXACT_PATH)
    witness = load_json(WITNESS_PATH)
    for name, record in [
        ("adaptive", adaptive),
        ("schedule", schedule),
        ("near", near),
        ("exact", exact),
        ("witness", witness),
    ]:
        check_header(name, record)
    meta = adaptive["adaptive_ratio_columns"]
    sched_meta = schedule["adaptive_schedule_candidates"]
    require(meta["planes_solved"] > 0, "adaptive: no planes solved")
    require(meta["start_width"] >= 1, "adaptive: invalid start width")
    require(meta["max_width"] >= meta["start_width"], "adaptive: max width below start")
    require(meta["best_min_support"] >= 0, "adaptive: invalid best support")
    require(meta["best_total_incidence"] >= 0, "adaptive: invalid best incidence")
    require(sched_meta["menu_ratio_limit"] == meta["max_width"], "schedule: menu limit mismatch")
    require(sched_meta["plane_limit"] == meta["planes_solved"], "schedule: plane limit mismatch")
    require(sched_meta["stored_candidates"] == len(schedule["candidates"]), "schedule: stored count mismatch")
    support_passes = [row for row in schedule["candidates"] if row.get("support_pair_pass")]
    near_fronts = [row for row in schedule["candidates"] if row.get("near_front")]
    require(len(support_passes) == sched_meta["support_pair_candidates"], "schedule: support-pass count mismatch")
    require(len(near_fronts) == sched_meta["near_front_candidates"], "schedule: near-front count mismatch")
    for row in support_passes + near_fronts:
        require("chosen_options" in row, f"{row.get('candidate_id')}: missing exact-audit choices")
    require(near["near_front_exact"]["systems_tested"] <= sched_meta["near_front_candidates"], "near: too many systems")
    require(exact["exact_interpolation"]["systems_tested"] <= sched_meta["support_pair_candidates"], "exact: too many systems")
    require(witness["witness_audit"]["constructed"] in (True, False), "witness: malformed constructed flag")
    note = NOTE_PATH.read_text()
    for phrase in ["adaptive ratio", "near-front", "not an MCA row"]:
        require(phrase in note, f"note missing {phrase}")
    return {
        "status": "PASS",
        "proof_status": adaptive["proof_status"],
        "best_min_support": meta["best_min_support"],
        "best_total_incidence": meta["best_total_incidence"],
        "near_front_candidates": sched_meta["near_front_candidates"],
        "support_pair_candidates": sched_meta["support_pair_candidates"],
        "near_systems_tested": near["near_front_exact"]["systems_tested"],
        "support_pair_systems_tested": exact["exact_interpolation"]["systems_tested"],
        "witness_status": witness["proof_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 mu_8 rank-2 adaptive ratio columns")


if __name__ == "__main__":
    main()
