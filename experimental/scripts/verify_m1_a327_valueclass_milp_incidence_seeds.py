#!/usr/bin/env python3
"""Dependency-free verifier for the M1 a=327 MILP incidence seed audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_valueclass_milp_incidence_seeds.json")
RANK_DATA_PATH = Path("experimental/data/m1_a327_valueclass_milp_incidence_seeds_rank_audit.json")

N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = K - 1

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

EXPECTED_EXACT_SELECTION = {
    "all_sizes_max_pairs_at255_block",
    "all_sizes_max_pairs_at255_bit_reversal",
    "all_sizes_max_pairs_at255_fiber_round_robin",
    "all_sizes_min_anchor_variables_block",
    "sizes_3_7_max_pairs_at255_block",
    "sizes_3_7_max_pairs_at255_fiber_round_robin",
    "sizes_3_6_max_pairs_at255_block",
    "sizes_4_5_max_pairs_at255_block",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def members(mask: int) -> list[int]:
    return [idx for idx in range(LIST_SIZE) if mask & (1 << idx)]


def pair_key(i: int, j: int) -> str:
    if i > j:
        i, j = j, i
    return f"{i},{j}"


def summarize_masks(masks: list[int]) -> dict[str, Any]:
    supports = [0] * LIST_SIZE
    pair_counts = {pair_key(i, j): 0 for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)}
    histogram: dict[str, int] = {}
    for mask in masks:
        bits = members(mask)
        histogram[str(len(bits))] = histogram.get(str(len(bits)), 0) + 1
        for item in bits:
            supports[item] += 1
        for idx, left in enumerate(bits):
            for right in bits[idx + 1 :]:
                pair_counts[pair_key(left, right)] += 1
    pair_values = list(pair_counts.values())
    anchor_pair_sum = sum(pair_counts[pair_key(0, witness)] for witness in range(1, LIST_SIZE))
    return {
        "support_sizes": supports,
        "min_support_size": min(supports),
        "max_support_size": max(supports),
        "max_pair_intersection": max(pair_values),
        "min_pair_intersection": min(pair_values),
        "pair_intersections": dict(sorted(pair_counts.items())),
        "membership_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "membership_size_support": sorted(int(size) for size, count in histogram.items() if count),
        "pairs_at_255": sum(1 for value in pair_values if value == PAIR_CAP),
        "pairs_at_or_above_250": sum(1 for value in pair_values if value >= 250),
        "pairs_at_or_above_245": sum(1 for value in pair_values if value >= 245),
        "pair_intersection_sum": sum(pair_values),
        "anchor_compressed_variables": (LIST_SIZE - 1) * K - anchor_pair_sum,
    }


def verify_scan(scan: dict[str, Any]) -> None:
    require(scan["track"] == "INTERLEAVED_LIST", "scan wrong track")
    require(scan["denominator"] == "17^32", "scan wrong denominator")
    require(scan["agreement_target"] == TARGET_AGREEMENT, "scan wrong target")
    require(scan["construction_mode"] == "valueclass_milp_incidence_seeds", "scan wrong mode")
    require(scan["candidate_count"] == 18, "scan candidate count mismatch")
    require(len(scan["profiles"]) == 6, "profile count mismatch")
    require(scan["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(scan["not_claimed"])), "scan missing non-claims")

    for candidate in scan["candidates"]:
        masks = candidate["membership_masks"]
        require(len(masks) == N, "candidate does not cover H")
        summary = summarize_masks(masks)
        require(summary["support_sizes"] == [TARGET_AGREEMENT] * LIST_SIZE, "support target mismatch")
        require(summary["max_pair_intersection"] <= PAIR_CAP, "pair cap exceeded")
        require(summary["membership_histogram"] == candidate["summary"]["membership_histogram"], "histogram mismatch")
        require(summary["pair_intersections"] == candidate["summary"]["pair_intersections"], "pair counts mismatch")
        require(summary["pairs_at_255"] == candidate["summary"]["pairs_at_255"], "cap count mismatch")


def verify_rank(scan: dict[str, Any], rank: dict[str, Any]) -> None:
    require(rank["track"] == "INTERLEAVED_LIST", "rank wrong track")
    require(rank["denominator"] == "17^32", "rank wrong denominator")
    require(rank["agreement_target"] == TARGET_AGREEMENT, "rank wrong target")
    require(rank["construction_mode"] == "valueclass_milp_incidence_seed_rank_audit", "rank wrong mode")
    require(rank["candidate_count"] == scan["candidate_count"] == 18, "rank candidate count mismatch")
    require(rank["profile_count"] == len(scan["profiles"]) == 6, "rank profile count mismatch")
    require(rank["source"]["source_candidate_design_hash"] == scan["candidate_design_hash"], "source hash mismatch")
    require(rank["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(rank["exact_field"] == "GF(17^32)", "wrong exact field")
    require(rank["subgroup_order"] == N, "wrong subgroup order")
    require(rank["degree_bound"] == K, "wrong degree bound")
    require(rank["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(rank["not_claimed"])), "rank missing non-claims")
    require(rank["proxy_positive_count"] == 0, "unexpected proxy-positive candidate")
    require(rank["exact_selected_count"] == len(EXPECTED_EXACT_SELECTION), "exact selection count mismatch")
    require(rank["exact_minor_full_rank_count"] == len(EXPECTED_EXACT_SELECTION), "not all exact minors full rank")
    require(rank["exact_minor_singular_count"] == 0, "singular exact minor present")
    require(rank["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATES", "wrong proof status")

    results = rank["results"]
    require(len(results) == 18, "result count mismatch")
    exact_ids = {row["candidate_id"] for row in results if row["exact_selected"]}
    require(exact_ids == EXPECTED_EXACT_SELECTION, "wrong exact selection")
    for row in results:
        require(row["support_sizes"] == [TARGET_AGREEMENT] * LIST_SIZE, "rank support mismatch")
        require(row["max_pair_intersection"] <= PAIR_CAP, "rank pair cap exceeded")
        require(row["compressed_variables"] == row["anchor_compressed_variables"], "compressed variable mismatch")
        require(row["proxy_rank"] == row["compressed_variables"], "proxy rank not full")
        require(row["proxy_nullity"] == 0, "proxy nullity not zero")
        require(row["agreement_verified"] is False, "unexpected agreement certificate")
        require(row["non_diagonal_solution_found"] is False, "unexpected extracted solution")
        if row["exact_selected"]:
            require(row["status"] == "EXACT_MINOR_FULL_RANK", "selected exact status mismatch")
            require(row["exact_minor_rank"] == row["compressed_variables"], "exact rank not full")
            require(row["exact_nullity"] == 0, "exact nullity not zero")
        else:
            require(row["status"] == "EXACT_NOT_SELECTED", "unselected status mismatch")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    rank = load_json(RANK_DATA_PATH)
    verify_scan(scan)
    verify_rank(scan, rank)
    all_pair_cap = [
        row
        for row in rank["results"]
        if row["profile_id"] == "all_sizes_max_pairs_at255"
    ]
    require(len(all_pair_cap) == 3, "all-pair-cap embedding count mismatch")
    require(all(row["pairs_at_255"] == 21 for row in all_pair_cap), "all-pair-cap profile not at cap")
    require(all(row["compressed_variables"] == 6 for row in all_pair_cap), "all-pair-cap compressed variable mismatch")
    require(all(row["status"] == "EXACT_MINOR_FULL_RANK" for row in all_pair_cap), "all-pair-cap exact route cut missing")
    return {
        "status": "PASS",
        "candidate_count": rank["candidate_count"],
        "proxy_positive_count": rank["proxy_positive_count"],
        "exact_selected_count": rank["exact_selected_count"],
        "proof_status": rank["proof_status"],
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
            "PASS: M1 a=327 MILP incidence seed audit "
            f"({result['candidate_count']} candidates, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
