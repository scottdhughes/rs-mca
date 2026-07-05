#!/usr/bin/env python3
"""Verify the M1 a=327 mu_8 exact rank batch and carrier probe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


RANK_PATH = Path("experimental/data/m1_a327_mu8_exact_rank_batch_64.json")
CLASS_PATH = Path("experimental/data/m1_a327_mu8_kernel_classification.json")
WITNESS_PATH = Path("experimental/data/m1_a327_mu8_exact_witness_audit.json")
CARRIER_PATH = Path("experimental/data/m1_a327_mu8_rank_one_carrier_probe.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_mu8_exact_rank_batch.md")

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
    require(record["source_commit"] == "01bc0e3", f"{name}: wrong source commit")
    require(record["mca_counted"] is False, f"{name}: MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), f"{name}: missing nonclaims")


def verify() -> dict[str, Any]:
    rank = load_json(RANK_PATH)
    classification = load_json(CLASS_PATH)
    witness = load_json(WITNESS_PATH)
    carrier = load_json(CARRIER_PATH)
    note_text = NOTE_PATH.read_text()
    for name, record in [
        ("rank", rank),
        ("classification", classification),
        ("witness", witness),
        ("carrier", carrier),
    ]:
        check_header(name, record)
    batch = rank["rank_batch"]
    require(rank["proof_status"] == "EXACT_EXTRACTION_NO_A327 / MU8_SELECTED_MUTATION_FULL_COLUMN_RANK / PARTIAL / EXPERIMENTAL", "rank: wrong status")
    require(batch["field"] == "GF(17^32)", "rank: wrong field")
    require(batch["schedules_planned"] == 64, "rank: wrong planned count")
    require(batch["schedules_tested"] == 64, "rank: wrong tested count")
    require(batch["full_rank_schedules"] == 64, "rank: not all full rank")
    require(batch["positive_nullity_schedules"] == 0, "rank: unexpected nullity")
    require(batch["best_nullity"] == 0, "rank: wrong best nullity")
    for row in rank["schedule_ranks"]:
        require(row["matrix_shape"] == [264, 224], f"{row['candidate_id']}: wrong matrix shape")
        require(row["rank"] == 224, f"{row['candidate_id']}: wrong rank")
        require(row["nullity"] == 0, f"{row['candidate_id']}: unexpected nullity")
        require(row["status"] == "MU8_SELECTED_MUTATION_FULL_COLUMN_RANK", f"{row['candidate_id']}: wrong status")
    kernel = classification["kernel_classification"]
    require(kernel["positive_nullity_schedules"] == 0, "classification: unexpected positive kernels")
    require(kernel["pair_visible_kernels"] == 0, "classification: unexpected pair-visible kernels")
    require(kernel["pair_forced_kernels"] == 0, "classification: unexpected pair-forced kernels")
    require(kernel["classifications"] == [], "classification: expected empty classifications")
    wa = witness["witness_audit"]
    require(wa["constructed"] is False, "witness: unexpected construction")
    require(wa["status"] == "NO_EXACT_WITNESS_CONSTRUCTED", "witness: wrong status")
    probe = carrier["rank_one_carrier_probe"]
    require(carrier["proof_status"] == "EXACT_EXTRACTION_NO_A327 / MU8_RANK_ONE_NO_PAIR_VISIBLE_CARRIER / PARTIAL / EXPERIMENTAL", "carrier: wrong status")
    require(probe["schedules_tested"] == 64, "carrier: wrong tested count")
    require(probe["pair_visible_carriers_found"] == 0, "carrier: unexpected carrier")
    require(probe["exact_witnesses_found"] == 0, "carrier: unexpected witness")
    require(probe["best_pair_visible_carrier_coverage"] == 1, "carrier: unexpected best coverage")
    for phrase in [
        "64",
        "full column rank",
        "rank-one carrier",
        "coverage",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {
        "status": "PASS",
        "rank_status": rank["proof_status"],
        "carrier_status": carrier["proof_status"],
        "schedules_tested": batch["schedules_tested"],
        "best_carrier_coverage": probe["best_pair_visible_carrier_coverage"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 mu_8 exact rank batch")


if __name__ == "__main__":
    main()
