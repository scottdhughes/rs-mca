#!/usr/bin/env python3
"""Verify the M1 a=327 mu_8 rank-one and rank-2 carrier ledgers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


RANK_ONE_PATH = Path("experimental/data/m1_a327_mu8_rank_one_carrier_obstruction.json")
MENU_PATH = Path("experimental/data/m1_a327_mu8_rank2_carrier_menu_scan.json")
SCHEDULE_PATH = Path("experimental/data/m1_a327_mu8_rank2_carrier_schedule_candidates.json")
EXACT_PATH = Path("experimental/data/m1_a327_mu8_rank2_carrier_exact_interpolation.json")
WITNESS_PATH = Path("experimental/data/m1_a327_mu8_rank2_exact_witness_audit.json")
RANK_ONE_NOTE = Path("experimental/notes/m1/m1_a327_mu8_rank_one_carrier_obstruction.md")
RANK2_NOTE = Path("experimental/notes/m1/m1_a327_mu8_rank2_carrier_generator.md")

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
    require(record["source_commit"] == "83c6f93", f"{name}: wrong source commit")
    require(record["mca_counted"] is False, f"{name}: MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), f"{name}: missing nonclaims")


def verify() -> dict[str, Any]:
    rank_one = load_json(RANK_ONE_PATH)
    menu = load_json(MENU_PATH)
    schedule = load_json(SCHEDULE_PATH)
    exact = load_json(EXACT_PATH)
    witness = load_json(WITNESS_PATH)
    for name, record in [
        ("rank_one", rank_one),
        ("menu", menu),
        ("schedule", schedule),
        ("exact", exact),
        ("witness", witness),
    ]:
        check_header(name, record)

    obstruction = rank_one["rank_one_mu8_carrier_obstruction"]
    require(obstruction["quotient_roots_max"] == 31, "rank-one: wrong quotient root ceiling")
    require(obstruction["common_zero_coordinates_max"] == 248, "rank-one: wrong common zero ceiling")
    require(obstruction["outside_pair_equalities_max"] == 147, "rank-one: wrong outside pair ceiling")
    require(obstruction["selected_incidence_ceiling"] == 2147, "rank-one: wrong incidence ceiling")
    require(obstruction["required_selected_incidences"] == 2289, "rank-one: wrong required incidence")
    require(obstruction["contradiction"] is True, "rank-one: expected contradiction")
    require(obstruction["status"] == "MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION", "rank-one: wrong status")

    generator = menu["rank2_carrier_generator"]
    require(generator["planes_generated"] == 64, "menu: wrong plane count")
    require(menu["proof_status"] == "CANDIDATE / MU8_RANK2_CARRIER_EXACT_MENU_PENDING / PARTIAL / EXPERIMENTAL", "menu: wrong status")
    require(len(menu["carrier_planes"]) == 64, "menu: plane ledger mismatch")
    for plane in menu["carrier_planes"]:
        require(plane["forced_equal_pairs"] == [], f"{plane['plane_id']}: forced pairs not filtered")

    sched = schedule["schedule_candidates"]
    require(sched["planes_audited"] == 64, "schedule: wrong audited count")
    require(sched["constructed"] == 64, "schedule: wrong constructed count")
    require(sched["guard_passing"] == 0, "schedule: unexpected guard pass")
    require(sched["selected_for_exact_interpolation"] == 0, "schedule: unexpected exact candidate")
    require(sched["best_failure_mode"] == "MU8_RANK2_CARRIER_NO_GUARD_PASS", "schedule: wrong failure")
    require(schedule["proof_status"] == "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_GUARD_PASS / PARTIAL / EXPERIMENTAL", "schedule: wrong status")
    require(all(not row["guard_pass"] for row in schedule["candidates"]), "schedule: candidate guard mismatch")

    interp = exact["exact_interpolation"]
    require(interp["systems_tested"] == 0, "exact: unexpected systems")
    require(interp["positive_nullity_systems"] == 0, "exact: unexpected nullity")
    require(exact["systems"] == [], "exact: expected empty systems")
    require(exact["proof_status"] == "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE / PARTIAL / EXPERIMENTAL", "exact: wrong status")

    wa = witness["witness_audit"]
    require(wa["constructed"] is False, "witness: unexpected construction")
    require(witness["proof_status"] == "EXACT_EXTRACTION_NO_A327 / NO_EXACT_WITNESS_CONSTRUCTED / PARTIAL / EXPERIMENTAL", "witness: wrong status")

    rank_one_text = RANK_ONE_NOTE.read_text()
    rank2_text = RANK2_NOTE.read_text()
    for phrase in ["2147", "2289", "rank-one", "not an MCA row"]:
        require(phrase in rank_one_text, f"rank-one note missing: {phrase}")
    for phrase in ["rank-2", "64", "no guard-passing", "not an MCA row"]:
        require(phrase in rank2_text, f"rank2 note missing: {phrase}")

    return {
        "status": "PASS",
        "rank_one_status": rank_one["proof_status"],
        "rank2_schedule_status": schedule["proof_status"],
        "planes_audited": sched["planes_audited"],
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
        print("PASS: M1 a=327 mu_8 rank-2 carrier generator ledger")


if __name__ == "__main__":
    main()
