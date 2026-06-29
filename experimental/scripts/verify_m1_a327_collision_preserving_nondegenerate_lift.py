#!/usr/bin/env python3
"""Verifier for the M1 a=327 collision-preserving nondegenerate lift packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_collision_preserving_nondegenerate_lift.json")
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
    "DEGENERATE_CODEWORDS",
    "LOW_RESCHEDULE",
    "PIN_DESTROYS_COLLISION",
    "PIN_INCONSISTENT",
    "EXACT_A327_ASSIGNMENT",
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
    require(record["construction_mode"] == "collision_preserving_nondegenerate_lift", "wrong mode")
    require(record["source_commit"] == "9c2f278", "wrong source commit")
    require(record["exact_field"] == "GF(17^32)", "wrong exact field")
    require(record["subgroup_order"] == 512, "wrong subgroup order")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    require(record["baseline"]["best_high_capacity_degenerate_capacity"] == 448, "wrong baseline capacity")
    require(record["baseline"]["best_degenerate_max_min"] == 288, "wrong baseline max-min")
    require(record["baseline"]["best_nondegenerate_capacity"] == 94, "wrong baseline nondegenerate capacity")
    require(record["proof_status"] in {"CANDIDATE", "EXACT_EXTRACTION_NO_A327"}, "bad proof status")
    search = record["pin_search"]
    require(search["systems_tested"] == len(record["results"]) >= 1, "wrong system count")
    require(search["exact_vectors_constructed"] > 0, "no vectors")
    require(search["nondegenerate_vectors"] >= search["nondegenerate_high_capacity_vectors"], "bad high-cap count")
    require(search["best_failure_mode"] in ALLOWED_STATUS, "bad best failure mode")
    exact_hits = 0
    total_vectors = 0
    nondegenerate = 0
    high_capacity = 0
    for result in record["results"]:
        require(result["exact_vectors_constructed"] == len(result["evaluations"]), "evaluation mismatch")
        require(result["common_pivot_count"] == 640, "pivot count mismatch")
        require(result["common_free_count"] == 896, "free count mismatch")
        total_vectors += result["exact_vectors_constructed"]
        exact_hits += result["exact_a327_vectors"]
        nondegenerate += result["nondegenerate_vectors"]
        high_capacity += result["nondegenerate_high_capacity_vectors"]
        for sample in result["evaluations"]:
            if sample["evaluation"] is None:
                require(sample["solve"]["status"] == "PIN_INCONSISTENT", "bad null evaluation")
                continue
            status = sample["evaluation"]["status"]
            require(status in ALLOWED_STATUS, f"bad sample status {status}")
            require(sample["evaluation"]["capacity_upper_bound"] <= 512, "capacity impossible")
            if status == "EXACT_A327_ASSIGNMENT":
                require(sample["evaluation"]["assignment"]["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
            if sample["evaluation"]["distinct_codewords"]:
                nonzero = set(sample["evaluation"]["nonzero_witness_blocks"])
                require(nonzero == {"D_2", "D_3", "D_4", "D_5", "D_6", "D_7"}, "distinct sample missing block support")
    require(total_vectors == search["exact_vectors_constructed"], "total vector mismatch")
    require(nondegenerate == search["nondegenerate_vectors"], "nondegenerate mismatch")
    require(high_capacity == search["nondegenerate_high_capacity_vectors"], "high-cap mismatch")
    require(exact_hits == record["exact_a327_vector_count"], "hit mismatch")
    require(record["candidate"]["reaches_327_exact"] == (exact_hits > 0), "candidate mismatch")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_hits == 0, "negative status with hit")
    return {
        "status": "PASS",
        "systems_tested": search["systems_tested"],
        "exact_vectors_constructed": total_vectors,
        "nondegenerate_vectors": nondegenerate,
        "nondegenerate_high_capacity_vectors": high_capacity,
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
            "PASS: M1 a=327 collision-preserving nondegenerate lift "
            f"({result['exact_vectors_constructed']} vectors, high-cap={result['nondegenerate_high_capacity_vectors']})"
        )


if __name__ == "__main__":
    main()
