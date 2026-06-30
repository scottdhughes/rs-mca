#!/usr/bin/env python3
"""Verifier for the M1 a=327 residual-degeneracy separation packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_residual_degeneracy_separation.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_STATUS = {
    "PIN_INCONSISTENT",
    "PIN_SPLITS_BUT_DESTROYS_CAPACITY",
    "PIN_SPLITS_CAPACITY_OK_LOW_RESCHEDULE",
    "PIN_DOES_NOT_SPLIT",
    "DEGENERATE_CODEWORDS",
    "CANDIDATE_A327",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "8255f1c", "wrong source commit")
    require(record["construction_mode"] == "residual_degeneracy_separation", "wrong mode")
    require(record["exact_field"] == "GF(17^32)", "wrong exact field")
    require(record["subgroup_order"] == 512, "wrong subgroup")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    require(record["baseline"]["best_degenerate_capacity_upper_bound"] == 374, "bad baseline")
    require(record["baseline"]["best_pinned_nondegenerate_capacity_upper_bound"] == 82, "bad pin baseline")
    require(record["proof_status"] in {"CANDIDATE", "EXACT_EXTRACTION_NO_A327"}, "bad proof status")
    search = record["separation_search"]
    require(search["pin_sets_tested"] > 0, "no pin sets")
    require(search["best_failure_mode"] in ALLOWED_STATUS, "bad best failure")
    exact_hits = 0
    pin_sets = 0
    exact_vectors = 0
    nondegenerate = 0
    cap_preserving = 0
    for result in record["results"]:
        ledger = result["degeneracy_ledger"]
        require(ledger["capacity_upper_bound"] >= TARGET_AGREEMENT, "ledger not high capacity")
        require(ledger["distinct_evaluation_vectors"] < 7, "ledger not degenerate")
        require(ledger["witness_equivalence_classes"], "missing equivalence classes")
        pin_sets += result["pin_sets_tested"]
        exact_vectors += result["exact_vectors_constructed"]
        nondegenerate += result["nondegenerate_vectors"]
        cap_preserving += result["capacity_preserving_nondegenerate_vectors"]
        exact_hits += result["exact_a327_vectors"]
        for sample in result["evaluations"]:
            status = sample["evaluation"]["status"] if sample["evaluation"] is not None else sample["solve"]["status"]
            require(status in ALLOWED_STATUS, f"bad sample status {status}")
            if sample["evaluation"] is None:
                continue
            require(sample["evaluation"]["capacity_upper_bound"] <= 512, "capacity impossible")
            if sample["evaluation"]["status"] == "CANDIDATE_A327":
                require(sample["evaluation"]["assignment"]["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(pin_sets == search["pin_sets_tested"], "pin set mismatch")
    require(exact_vectors == search["exact_vectors_constructed"], "exact vector mismatch")
    require(nondegenerate == search["nondegenerate_vectors"], "nondegenerate mismatch")
    require(cap_preserving == search["capacity_preserving_nondegenerate_vectors"], "capacity-preserving mismatch")
    require(exact_hits == record["exact_a327_vector_count"], "hit mismatch")
    require(record["candidate"]["reaches_327_exact"] == (exact_hits > 0), "candidate mismatch")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_hits == 0, "negative status with exact hit")
    return {
        "status": "PASS",
        "systems_tested": record["diagnostic"]["systems_tested"],
        "pin_sets_tested": search["pin_sets_tested"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "nondegenerate_vectors": search["nondegenerate_vectors"],
        "capacity_preserving_nondegenerate_vectors": search["capacity_preserving_nondegenerate_vectors"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "best_exact_max_min": search["best_exact_max_min"],
        "best_failure_mode": search["best_failure_mode"],
        "proof_status": record["proof_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "PASS: M1 a=327 residual-degeneracy separation "
            f"({result['pin_sets_tested']} pin sets, cap-preserving={result['capacity_preserving_nondegenerate_vectors']})"
        )


if __name__ == "__main__":
    main()
