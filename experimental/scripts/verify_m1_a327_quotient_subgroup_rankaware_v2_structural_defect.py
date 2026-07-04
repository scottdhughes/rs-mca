#!/usr/bin/env python3
"""Verify M1 a=327 rank-aware v2 structural-defect ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_rankaware_v2_structural_defect.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_rankaware_v2_structural_defect.md")


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
    require(record["source_commit"] == "e472d07", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    previous = record["previous_structural_rank_features"]
    require(previous["structural_positive_screens"] == 0, "unexpected previous structural positive")
    v2 = record["rankaware_v2"]
    require(v2["models_tested"] == len(record["models"]), "wrong model count")
    for model in record["models"]:
        if not model["feasible"]:
            continue
        require(model["support_vector"] == [327] * 7, "support changed")
        require(min(model["pair7_counts"]) >= 142, "pair7 guard failed")
        require(model["max_pair_equal_h_count"] <= 255, "pair cap failed")
        require(model["equation_gap_to_structural_defect"] == model["equation_count"] - (model["variable_count"] - 1), "bad gap")
    expected = (
        "CANDIDATE / RANKAWARE_V2_STRUCTURAL_DEFECT_TARGET / PARTIAL / EXPERIMENTAL"
        if v2["structural_defect_targets_found"] > 0
        else "EXACT_EXTRACTION_NO_A327 / RANKAWARE_V2_NO_STRUCTURAL_DEFECT / PARTIAL / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected, "wrong proof status")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")
    for phrase in ["RANKAWARE_V2", "equation_count < variable_count", "not an MCA row"]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {"status": "PASS", "proof_status": record["proof_status"], **v2}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 rank-aware v2 structural defect (status={result['proof_status']})")


if __name__ == "__main__":
    main()
