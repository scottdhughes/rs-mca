#!/usr/bin/env python3
"""Verify the M1 a=327 mu_8 block/rank-feedback ledgers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BLOCK_PATH = Path("experimental/data/m1_a327_mu8_block_decomposition_audit.json")
SCAN_PATH = Path("experimental/data/m1_a327_mu8_block_rank_feedback_scan.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_mu8_block_rank_feedback.md")

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
    block = load_json(BLOCK_PATH)
    scan = load_json(SCAN_PATH)
    note_text = NOTE_PATH.read_text()
    for name, record in [("block", block), ("scan", scan)]:
        require(record["track"] == "INTERLEAVED_LIST", f"{name}: wrong track")
        require(record["row"] == "RS[F_17^32,H,256]", f"{name}: wrong row")
        require(record["denominator"] == "17^32", f"{name}: wrong denominator")
        require(record["agreement_target"] == 327, f"{name}: wrong agreement target")
        require(record["mca_counted"] is False, f"{name}: MCA counted unexpectedly")
        require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), f"{name}: missing nonclaims")
    require(block["source_commit"] == "dd07a87", "block: wrong source commit")
    require(scan["source_commit"] == "dd07a87", "scan: wrong source commit")
    audit = block["block_audit"]
    require(audit["schedules_audited"] == 9, "block: wrong audited count")
    require(audit["canonical_reproduction_pass"] is True, "block: canonical reproduction failed")
    require(audit["equivariance_certified_schedules"] == 0, "block: unexpected equivariance certification")
    require(audit["positive_full_nullity_schedules"] == 0, "block: unexpected full nullity")
    require(audit["positive_residue_subset_schedules"] == 0, "block: unexpected residue nullity")
    require(audit["best_failure_mode"] == "MU8_BLOCK_AUDIT_FULL_RANK", "block: wrong failure")
    for row in block["schedule_audits"]:
        require(row["canonical_reproduces_source"] is True, f"{row['schedule_id']}: reproduction failed")
        require(row["canonical_matrix_shape"] == [264, 224], f"{row['schedule_id']}: wrong shape")
        require(row["canonical_rank"] == 224, f"{row['schedule_id']}: wrong rank")
        require(row["canonical_nullity"] == 0, f"{row['schedule_id']}: wrong nullity")
        require(row["equivariance"]["equivariance_checked"] is True, f"{row['schedule_id']}: no equivariance check")
        require(row["equivariance"]["block_decomposition_used"] is False, f"{row['schedule_id']}: bogus block split")
    front = scan["mutation_front"]
    require(scan["proof_status"] == "CANDIDATE / MU8_RANK_FEEDBACK_EXACT_RANK_PENDING / PARTIAL / EXPERIMENTAL", "scan: wrong status")
    require(front["raw_guard_passing_mutations"] >= 1000, "scan: too few mutations")
    require(front["selected_for_exact_followup"] == 64, "scan: wrong followup count")
    require(front["best_failure_mode"] == "MU8_RANK_FEEDBACK_EXACT_RANK_PENDING", "scan: wrong failure")
    require(len(scan["candidate_schedules"]) == 64, "scan: selected candidate mismatch")
    for row in scan["candidate_schedules"]:
        require(row["support_per_codeword"] >= 327, f"{row['candidate_id']}: support guard failed")
        require(row["ambient_pair_bound"] <= 255, f"{row['candidate_id']}: pair guard failed")
        require(row["exact_rank_status"] == "NOT_RUN", f"{row['candidate_id']}: exact status should be pending")
    for phrase in [
        "canonical matrix",
        "equivariance",
        "1,737",
        "64",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {
        "status": "PASS",
        "block_status": block["proof_status"],
        "scan_status": scan["proof_status"],
        "schedules_audited": audit["schedules_audited"],
        "rank_feedback_candidates": front["selected_for_exact_followup"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 mu_8 block/rank-feedback ledgers")


if __name__ == "__main__":
    main()
