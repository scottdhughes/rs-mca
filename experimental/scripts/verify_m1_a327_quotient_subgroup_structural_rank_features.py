#!/usr/bin/env python3
"""Verify M1 a=327 quotient-subgroup structural-rank feature ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_structural_rank_features.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_structural_rank_features.md")


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
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "e472d07", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    previous = record["previous_long_cpsat_front"]
    require(previous["cp_feasible_screens"] == 3, "wrong previous feasible screen count")
    features = record["structural_rank_features"]
    require(features["screens_tested"] == len(record["screen_diagnostics"]), "wrong screen count")
    for screen in record["screen_diagnostics"]:
        require(screen["support_vector"] == [327] * 7, "support changed")
        require(min(screen["pair7_counts"]) >= 142, "pair7 guard failed")
        require(screen["max_pair_equal_h_count"] <= 255, "pair cap failed")
        require(screen["labellings_tested"] == len(screen["diagnostics"]), "wrong labelling count")
        for row in screen["diagnostics"]:
            require(row["structural_rank"] <= row["variable_count"], "rank exceeds variables")
            require(
                row["structural_nullity_upper_bound"] == row["variable_count"] - row["structural_rank"],
                "bad structural nullity upper bound",
            )
            require(row["row_support_diversity"]["row_count"] == row["equation_count"], "bad row count")
    expected = (
        "CANDIDATE / STRUCTURAL_RANK_DEFECT_TARGET / PARTIAL / EXPERIMENTAL"
        if features["structural_positive_screens"] > 0
        else "EXACT_EXTRACTION_NO_A327 / STRUCTURAL_RANK_FULL_COLUMN_MATCHING / PARTIAL / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected, "wrong proof status")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")
    for phrase in ["STRUCTURAL_RANK", "full-column matching", "not an MCA row"]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {"status": "PASS", "proof_status": record["proof_status"], **features}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 quotient-subgroup structural-rank features (status={result['proof_status']})")


if __name__ == "__main__":
    main()
