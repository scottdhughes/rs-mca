#!/usr/bin/env python3
"""Dependency-free verifier for the M1 a=327 high-overlap value-class beam."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import scan_m1_a327_valueclass_high_overlap_beam as scanner


DATA_PATH = Path("experimental/data/m1_a327_valueclass_high_overlap_beam.json")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    candidates = scanner.candidate_designs()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == scanner.TARGET_AGREEMENT, "wrong target")
    require(record["construction_mode"] == "valueclass_high_overlap_beam", "wrong mode")
    require(record["candidate_count"] == len(candidates) == 64, "candidate count mismatch")
    require(record["candidate_design_hash"] == scanner.hash_payload(candidates), "candidate hash mismatch")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    require(record["seed_candidate_count"] == len(scanner.seed_candidates()), "seed count mismatch")
    require(record["trajectories_per_seed"] == scanner.TRAJECTORIES_PER_SEED, "trajectory count mismatch")
    require(record["mutation_steps"] == scanner.MUTATION_STEPS, "mutation step mismatch")

    max_pairs_at_255 = 0
    max_pairs_at_or_above_250 = 0
    max_membership_sizes = set()
    for candidate in candidates:
        summary = candidate["summary"]
        require(summary["support_sizes"] == [scanner.TARGET_AGREEMENT] * scanner.LIST_SIZE, "support size mismatch")
        require(summary["min_support_size"] == scanner.TARGET_AGREEMENT, "min support mismatch")
        require(summary["max_pair_intersection"] <= scanner.PAIR_CAP, "pair cap exceeded")
        require(set(summary["membership_size_support"]).issubset({3, 4, 5, 6}), "bad membership size")
        require({3, 6}.issubset(set(summary["membership_size_support"])), "mutation did not introduce 3/6 sizes")
        max_pairs_at_255 = max(max_pairs_at_255, summary["pairs_at_255"])
        max_pairs_at_or_above_250 = max(max_pairs_at_or_above_250, summary["pairs_at_or_above_250"])
        max_membership_sizes.update(summary["membership_size_support"])
    require(max_pairs_at_255 >= 9, "high-overlap target not reached")
    require(max_pairs_at_or_above_250 >= 9, "near-boundary target not reached")
    require({3, 4, 5, 6}.issubset(max_membership_sizes), "membership diversity target not reached")

    rank_gate = record["rank_gate"]
    if rank_gate["status"] == "SAGE_PROXY_RANKED":
        retained = rank_gate["retained_results"]
        require(rank_gate["all_result_count"] == len(candidates), "rank result count mismatch")
        require(rank_gate["retained_proxy_count"] == len(retained), "retained count mismatch")
        require(len(retained) <= scanner.RETAINED_PROXY_COUNT, "too many retained results")
        require(rank_gate["best"] == retained[0], "best should be first retained result")
        require(rank_gate["all_result_hash"], "missing full rank-result hash")
        require(rank_gate["proxy_field"] == "GF(12289)", "wrong proxy field")
        require(rank_gate["exact_field"] == "GF(17^32)", "wrong exact field")
        retained_ids = {row["candidate_id"] for row in retained}
        candidate_ids = {item["candidate_id"] for item in candidates}
        require(retained_ids.issubset(candidate_ids), "unknown retained candidate")
        best = rank_gate["best"]
        if rank_gate["proxy_positive_count"] == 0:
            require(best["proxy_nullity"] == 0, "unexpected best proxy nullity")
            require(record["proof_status"] == "TESTED_DESIGNS_NO_PROXY_NULLITY", "wrong no-proxy-nullity status")
            require(record["exact_audited_count"] == 0, "unexpected exact audit")
        else:
            require(record["proof_status"] in {"CANDIDATE", "PROOF_RECORD"}, "wrong positive-nullity status")
    else:
        require(record["proof_status"] == "PARTIAL", "non-ranked record must be partial")

    return {
        "status": "PASS",
        "candidate_count": record["candidate_count"],
        "proof_status": record["proof_status"],
        "proxy_positive_count": rank_gate["proxy_positive_count"],
        "retained_proxy_count": rank_gate["retained_proxy_count"],
        "best_proxy_nullity": None if rank_gate["best"] is None else rank_gate["best"]["proxy_nullity"],
        "max_pairs_at_255": max_pairs_at_255,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "PASS: M1 a=327 high-overlap value-class beam record "
            f"({result['candidate_count']} candidates, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
