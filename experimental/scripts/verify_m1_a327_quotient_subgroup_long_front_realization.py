#!/usr/bin/env python3
"""Verify the M1 a=327 quotient-subgroup long-front realization ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_long_front_realization.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_long_front_realization.md")


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
    previous = record["previous_long_cpsat_front"]
    require(previous["cp_feasible_screens"] == 3, "wrong previous feasible count")
    result = record["long_front_realization"]
    require(result["screens_realized"] == len(record["realization_results"]), "wrong realized count")
    require(result["proxy_positive_screens"] <= result["screens_realized"], "bad positive count")
    for row in record["realization_results"]:
        require(row["support_vector"] == [327] * 7, "support changed")
        require(min(row["pair7_counts"]) >= 142, "pair7 guard failed")
        require(row["max_pair_equal_h_count"] <= 255, "pair cap failed")
        require(row["best_proxy_nullity"] == row["best_matrix_shape"][1] - row["best_proxy_rank"], "bad nullity")
    expected = (
        "CANDIDATE / LONG_FRONT_REALIZATION_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if result["proxy_positive_screens"] > 0
        else "EXACT_EXTRACTION_NO_A327 / LONG_FRONT_REALIZATION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected, "wrong proof status")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")
    for phrase in ["LONG_FRONT_REALIZATION", "GF(193)", "not an MCA row"]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {"status": "PASS", "proof_status": record["proof_status"], **result}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 quotient-subgroup long-front realization (status={result['proof_status']})")


if __name__ == "__main__":
    main()
