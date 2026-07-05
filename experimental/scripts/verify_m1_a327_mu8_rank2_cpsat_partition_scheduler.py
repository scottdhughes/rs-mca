#!/usr/bin/env python3
"""Verify the M1 a=327 mu_8 rank-2 CP-SAT scheduler ledgers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MENU_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_menu.json")
SCHEDULE_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_schedule_candidates.json")
EXACT_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_exact_interpolation.json")
WITNESS_PATH = Path("experimental/data/m1_a327_mu8_rank2_cpsat_witness_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_mu8_rank2_cpsat_partition_scheduler.md")

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


def check_header(name: str, record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", f"{name}: wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", f"{name}: wrong row")
    require(record["denominator"] == "17^32", f"{name}: wrong denominator")
    require(record["agreement_target"] == 327, f"{name}: wrong target")
    require(record["source_commit"] == "ddc7fe9", f"{name}: wrong source commit")
    require(record["mca_counted"] is False, f"{name}: MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), f"{name}: missing nonclaims")


def verify() -> dict[str, Any]:
    menu = load_json(MENU_PATH)
    schedule = load_json(SCHEDULE_PATH)
    exact = load_json(EXACT_PATH)
    witness = load_json(WITNESS_PATH)
    note_text = NOTE_PATH.read_text()
    for name, record in [
        ("menu", menu),
        ("schedule", schedule),
        ("exact", exact),
        ("witness", witness),
    ]:
        check_header(name, record)

    require(menu["proof_status"] == "CANDIDATE / MU8_RANK2_CPSAT_MENU_READY / PARTIAL / EXPERIMENTAL", "menu: wrong status")
    require(menu["menu"]["planes"] == 64, "menu: wrong plane count")
    require(menu["menu"]["quotient_points"] == 64, "menu: wrong quotient count")
    require(menu["menu"]["ratio_limit"] == 4, "menu: wrong ratio limit")
    require(menu["menu"]["stored_as"] == "compact_summary", "menu: expected compact summary")
    require(menu["menu"]["exact_menu_rebuild_required_for_interpolation"] is True, "menu: rebuild flag missing")
    require(len(menu["plane_ids"]) == 64, "menu: plane ids mismatch")

    sched = schedule["cpsat_scheduler"]
    require(schedule["proof_status"] == "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_PLANE_SUPPORT_PAIR_SLACK_INFEASIBLE / PARTIAL / EXPERIMENTAL", "schedule: wrong status")
    require(sched["planes_solved"] == 64, "schedule: wrong solved count")
    require(sched["ratio_limit"] == 4, "schedule: wrong ratio limit")
    require(sched["guard_passing_schedules"] == 0, "schedule: unexpected guard pass")
    require(sched["best_min_support"] == 291, "schedule: wrong best min support")
    require(sched["best_selected_incidence_total"] == 2041, "schedule: wrong best incidence")
    require(sched["interpolation_row_cap"] == 63, "schedule: wrong row cap")
    require(sched["best_failure_mode"] == "MU8_RANK2_CARRIER_PLANE_SUPPORT_PAIR_SLACK_INFEASIBLE", "schedule: wrong failure")
    require(len(schedule["candidates"]) == 64, "schedule: candidate count mismatch")
    require(all(not row.get("guard_pass") for row in schedule["candidates"]), "schedule: guard-pass mismatch")

    interp = exact["exact_interpolation"]
    require(exact["proof_status"] == "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE / PARTIAL / EXPERIMENTAL", "exact: wrong status")
    require(interp["systems_tested"] == 0, "exact: unexpected systems")
    require(interp["positive_nullity_systems"] == 0, "exact: unexpected nullity")
    require(exact["systems"] == [], "exact: expected empty systems")

    wa = witness["witness_audit"]
    require(witness["proof_status"] == "EXACT_EXTRACTION_NO_A327 / NO_EXACT_WITNESS_CONSTRUCTED / PARTIAL / EXPERIMENTAL", "witness: wrong status")
    require(wa["constructed"] is False, "witness: unexpected construction")

    for phrase in [
        "CP-SAT",
        "64",
        "291",
        "2041",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "menu_status": menu["proof_status"],
        "schedule_status": schedule["proof_status"],
        "exact_status": exact["proof_status"],
        "planes_solved": sched["planes_solved"],
        "best_min_support": sched["best_min_support"],
        "best_selected_incidence_total": sched["best_selected_incidence_total"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 mu_8 rank-2 CP-SAT scheduler")


if __name__ == "__main__":
    main()
