#!/usr/bin/env python3
"""Verify rank-2 mu_8 full-menu ablation and synthesis ledgers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


WIDTH_PATH = Path("experimental/data/m1_a327_mu8_rank2_width_ablation.json")
SCHEDULE_PATH = Path("experimental/data/m1_a327_mu8_rank2_fullmenu_schedule_candidates.json")
SYNTH_PATH = Path("experimental/data/m1_a327_mu8_rank2_synthesized_carrier_planes.json")
EXACT_PATH = Path("experimental/data/m1_a327_mu8_rank2_fullmenu_exact_interpolation.json")
WITNESS_PATH = Path("experimental/data/m1_a327_mu8_rank2_fullmenu_witness_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_mu8_rank2_fullmenu_carrier_synthesis.md")

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
    require(record["source_commit"] == "46a0755", f"{name}: wrong source commit")
    require(record["mca_counted"] is False, f"{name}: MCA counted")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), f"{name}: missing nonclaims")


def verify() -> dict[str, Any]:
    width = load_json(WIDTH_PATH)
    schedule = load_json(SCHEDULE_PATH)
    synth = load_json(SYNTH_PATH)
    exact = load_json(EXACT_PATH)
    witness = load_json(WITNESS_PATH)
    for name, record in [
        ("width", width),
        ("schedule", schedule),
        ("synth", synth),
        ("exact", exact),
        ("witness", witness),
    ]:
        check_header(name, record)
    ablation = width["width_ablation"]
    require(ablation["hard_row_slack_gate"] is False, "width: row slack still hard")
    require(4 in ablation["widths_tested"], "width: width 4 missing")
    require(8 in ablation["widths_tested"], "width: width 8 missing")
    require(ablation["best_min_support"] == 313, "width: unexpected best support")
    require(ablation["best_total_incidence"] == 2193, "width: unexpected best incidence")
    require(ablation["guard_passing_candidates"] == 0, "width: unexpected guard pass")
    require(width["proof_status"] == "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_FULL_MENU_SUPPORT_PAIR_INFEASIBLE / PARTIAL / EXPERIMENTAL", "width: wrong status")
    require(schedule["schedule_candidates"]["guard_passing_candidates"] == 0, "schedule: unexpected guard pass")
    require(synth["synthesis"]["planes_emitted"] > 64, "synth: no synthesized planes emitted")
    require(exact["exact_interpolation"]["systems_tested"] == 0, "exact: unexpected systems")
    require(witness["witness_audit"]["constructed"] is False, "witness: unexpected construction")
    note = NOTE_PATH.read_text()
    for phrase in ["width", "313", "2193", "not an MCA row"]:
        require(phrase in note, f"note missing {phrase}")
    return {
        "status": "PASS",
        "width_status": width["proof_status"],
        "synth_planes": synth["synthesis"]["planes_emitted"],
        "best_min_support": ablation["best_min_support"],
        "best_total_incidence": ablation["best_total_incidence"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 mu_8 rank-2 full-menu ablation")


if __name__ == "__main__":
    main()
