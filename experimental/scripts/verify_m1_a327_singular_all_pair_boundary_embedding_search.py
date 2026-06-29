#!/usr/bin/env python3
"""Verifier for the M1 a=327 singular all-pair-boundary embedding search."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SCAN_DATA_PATH = Path("experimental/data/m1_a327_singular_all_pair_boundary_embedding_search.json")
EXACT_DATA_PATH = Path("experimental/data/m1_a327_singular_all_pair_boundary_embedding_search_exact_audit.json")
SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_singular_all_pair_boundary_embedding_search.py")

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
    "all_pair_boundary_block",
    "all_pair_boundary_bit_reversal",
    "all_pair_boundary_fiber_round_robin",
    "all_pair_boundary_random_shuffle_0000",
    "all_pair_boundary_random_shuffle_0001",
    "all_pair_boundary_random_shuffle_0017",
    "all_pair_boundary_random_shuffle_0064",
    "all_pair_boundary_random_shuffle_0255",
    "all_pair_boundary_random_shuffle_0511",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def load_scanner():
    spec = importlib.util.spec_from_file_location("singular_all_pair_boundary_scanner", SCANNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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
    return {
        "support_sizes": supports,
        "membership_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "max_pair_intersection": max(pair_values),
        "min_pair_intersection": min(pair_values),
        "pairs_at_255": sum(1 for value in pair_values if value == PAIR_CAP),
        "pairs_at_or_above_250": sum(1 for value in pair_values if value >= 250),
        "pair_intersections": dict(sorted(pair_counts.items())),
    }


def compact_summary(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "support_sizes": summary["support_sizes"],
        "membership_histogram": summary["membership_histogram"],
        "max_pair_intersection": summary["max_pair_intersection"],
        "min_pair_intersection": summary["min_pair_intersection"],
        "pairs_at_255": summary["pairs_at_255"],
        "pairs_at_or_above_250": summary["pairs_at_or_above_250"],
    }


def verify_scan(scan: dict[str, Any], regenerated: dict[str, Any]) -> None:
    require(scan["track"] == "INTERLEAVED_LIST", "wrong track")
    require(scan["denominator"] == "17^32", "wrong denominator")
    require(scan["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(scan["construction_mode"] == "singular_all_pair_boundary_embedding_search", "wrong mode")
    require(scan["candidate_count"] == 515, "wrong candidate count")
    require(scan["candidate_records_include_membership_masks"] is False, "scan should not store full masks")
    require(scan["deterministic_embedding_count"] == 3, "wrong deterministic count")
    require(scan["random_embedding_count"] == 512, "wrong random count")
    require(scan["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(scan["exact_field"] == "GF(17^32)", "wrong exact field")
    require(scan["proxy_singular_count"] == 0, "unexpected proxy singular")
    require(scan["proxy_full_rank_count"] == scan["candidate_count"], "not all proxy ranks full")
    require(scan["proof_status"] == "TESTED_EMBEDDINGS_NO_PROXY_SINGULAR", "wrong scan status")
    require(scan["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(scan["not_claimed"])), "missing non-claims")
    require(scan["profile_summary"]["pairs_at_255"] == 21, "source profile is not all-pair boundary")

    for row in scan["results"]:
        candidate = regenerated[row["candidate_id"]]
        summary = summarize_masks(candidate["membership_masks"])
        require(compact_summary(summary) == row["summary"], f"summary mismatch for {row['candidate_id']}")
        require(candidate["membership_mask_hash"] == row["membership_mask_hash"], "membership hash mismatch")
        require(row["summary"]["support_sizes"] == [TARGET_AGREEMENT] * LIST_SIZE, "support mismatch")
        require(row["summary"]["pairs_at_255"] == 21, "not all pairs at cap")
        require(row["compressed_variables"] == LIST_SIZE - 1, "wrong compressed variable count")
        require(row["remaining_equations"] == 659, "wrong effective equation count")
        require(row["proxy_rank"] == LIST_SIZE - 1, "proxy rank not full")
        require(row["proxy_nullity"] == 0, "proxy nullity not zero")
        require(row["status"] == "PROXY_FULL_RANK", "wrong proxy status")


def verify_exact(scan: dict[str, Any], exact: dict[str, Any]) -> None:
    require(exact["track"] == "INTERLEAVED_LIST", "exact wrong track")
    require(exact["denominator"] == "17^32", "exact wrong denominator")
    require(exact["agreement_target"] == TARGET_AGREEMENT, "exact wrong target")
    require(exact["construction_mode"] == "singular_all_pair_boundary_embedding_exact_audit", "exact wrong mode")
    require(exact["source"]["source_candidate_count"] == scan["candidate_count"], "source count mismatch")
    require(exact["source"]["source_result_hash"] == scan["result_hash"], "source hash mismatch")
    require(exact["source"]["source_proxy_singular_count"] == 0, "source proxy singular mismatch")
    require(exact["exact_field"] == "GF(17^32)", "wrong exact field")
    require(exact["subgroup_order"] == N, "wrong subgroup order")
    require(exact["degree_bound"] == K, "wrong degree bound")
    require(exact["exact_audited_count"] == len(EXPECTED_EXACT_SELECTION), "wrong exact audit count")
    require(exact["exact_full_rank_count"] == len(EXPECTED_EXACT_SELECTION), "not all exact ranks full")
    require(exact["exact_positive_nullity_count"] == 0, "positive exact nullity present")
    require(exact["proof_status"] == "ROUTE_CUT_TESTED_EMBEDDINGS", "wrong exact status")
    require(exact["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(exact["not_claimed"])), "exact missing non-claims")
    result_ids = {row["candidate_id"] for row in exact["results"]}
    require(result_ids == EXPECTED_EXACT_SELECTION, "wrong exact selection")
    for row in exact["results"]:
        require(row["support_sizes"] == [TARGET_AGREEMENT] * LIST_SIZE, "exact support mismatch")
        require(row["pairs_at_255"] == 21, "exact pair cap mismatch")
        require(row["proxy_rank"] == LIST_SIZE - 1, "proxy rank mismatch")
        require(row["proxy_nullity"] == 0, "proxy nullity mismatch")
        require(row["compressed_variables"] == LIST_SIZE - 1, "exact compressed variable mismatch")
        require(row["remaining_equations"] == 659, "exact equation count mismatch")
        require(row["exact_rank"] == LIST_SIZE - 1, "exact rank not full")
        require(row["exact_nullity"] == 0, "exact nullity not zero")
        require(row["status"] == "EXACT_FULL_RANK", "wrong exact row status")
        require(row["agreement_verified"] is False, "unexpected agreement certificate")
        require(row["non_diagonal_solution_found"] is False, "unexpected extracted solution")


def verify() -> dict[str, Any]:
    scan = load_json(SCAN_DATA_PATH)
    exact = load_json(EXACT_DATA_PATH)
    scanner = load_scanner()
    regenerated = {}
    for candidate in scanner.candidate_embeddings():
        candidate_id = f"all_pair_boundary_{candidate['embedding_id']}"
        regenerated[candidate_id] = {
            "membership_masks": candidate["membership_masks"],
            "membership_mask_hash": scanner.hash_payload(candidate["membership_masks"]),
        }
    require(set(regenerated) == {row["candidate_id"] for row in scan["results"]}, "regenerated candidate ids mismatch")
    verify_scan(scan, regenerated)
    verify_exact(scan, exact)
    return {
        "status": "PASS",
        "candidate_count": scan["candidate_count"],
        "proxy_singular_count": scan["proxy_singular_count"],
        "exact_audited_count": exact["exact_audited_count"],
        "proof_status": exact["proof_status"],
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
            "PASS: M1 a=327 singular all-pair-boundary embedding search "
            f"({result['candidate_count']} embeddings, status={result['proof_status']})"
        )


if __name__ == "__main__":
    main()
