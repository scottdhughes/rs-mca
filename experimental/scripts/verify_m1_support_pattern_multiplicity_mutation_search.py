#!/usr/bin/env python3
"""Verify the M1 support-pattern multiplicity-mutation search checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_support_pattern_multiplicity_mutation_search.json")


EXPECTED_CANDIDATES = {
    "multiplicity_spread_cyclic_3456_balanced_seed_202607204",
    "multiplicity_spread_cyclic_45_balanced_seed_202607014",
    "multiplicity_spread_cyclic_45_interval_high_overlap_seed_202606919",
    "multiplicity_spread_cyclic_3456_near_boundary_seed_202607109",
    "mixed_boundary_spread_cyclic_3456_balanced_seed_202607280",
    "mixed_boundary_spread_cyclic_45_balanced_seed_202607090",
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def verify_rank_gate(gate: dict[str, Any], exact: bool) -> None:
    assert gate["field_mode"] == ("exact" if exact else "surrogate")
    assert gate["field_label"] == ("GF(17^32)" if exact else "GF(12289)_surrogate")
    assert int(gate["field_size"]) == (17**32 if exact else 12289)
    assert 0 < gate["compressed_variables"] <= 6 * 256
    assert gate["rank"] == gate["compressed_variables"]
    assert gate["nullity"] == 0
    assert gate["non_diagonal_solution_found"] is False
    assert sum(gate["compressed_dimensions_by_witness"].values()) == gate["compressed_variables"]
    assert sum(gate["remaining_equations_by_pair"].values()) == gate["remaining_pairwise_equations"]
    assert len(gate["matrix_metadata_hash"]) == 64
    assert gate["status"] == "RANK_COMPUTED"


def verify_candidate(row: dict[str, Any]) -> None:
    assert row["candidate_id"] in EXPECTED_CANDIDATES
    assert row["mutation_family"] == "degree_preserving_pair_replacement_membership_hypergraph"
    assert row["search_objective"] in {"multiplicity_spread", "mixed_boundary_spread"}
    assert row["mutation_steps"] == 1800
    assert row["valid_mutation_attempts"] >= row["accepted_mutations"] >= 0
    assert row["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATE"

    support = row["support_design"]
    assert support["witness_support_sizes"] == [327] * 7
    assert support["pair_intersection_max"] == 255
    assert support["pair_intersections_at_255"] >= 6
    assert len(support["pair_intersection_values"]) == 21
    assert sorted(support["pair_intersections"].values()) == support["pair_intersection_values"]
    assert support["pair_intersection_sum"] == sum(support["pair_intersection_values"])
    assert support["pair_intersection_square_sum"] == sum(
        value * value for value in support["pair_intersection_values"]
    )
    assert sum(int(size) * count for size, count in support["multiplicity_histogram"].items()) == 7 * 327
    assert sum(support["multiplicity_histogram"].values()) == 512
    assert {"1", "2", "6", "7"}.issubset(support["multiplicity_histogram"])
    assert support["membership_pattern_count"] >= 40
    assert len(support["membership_pattern_histogram_hash"]) == 64
    assert len(support["support_hash"]) == 64

    profile = row["quotient_fiber_profile"]
    assert profile["fiber_count"] == 16
    assert profile["fiber_size"] == 32
    assert len(profile["distinct_pattern_counts"]) == 16
    assert len(profile["largest_pattern_multiplicities"]) == 16
    assert len(profile["multiplicity_profiles"]) == 16
    for fiber_profile in profile["multiplicity_profiles"]:
        assert sum(fiber_profile.values()) == 32

    proxy = row["rank_proxy"]
    assert proxy["method"] == "multiplicity_pair_boundary_row_pattern_proxy"
    assert isinstance(proxy["proxy_score"], int)
    assert proxy["compressed_variables"] == row["sage_exact_rank"]["compressed_variables"]
    assert proxy["multiplicity_spread_score"] > 0
    assert proxy["status"] == "SCORED"

    verify_rank_gate(row["surrogate_rank_gate"], exact=False)
    verify_rank_gate(row["sage_exact_rank"], exact=True)
    assert row["surrogate_rank_gate"]["compressed_dimensions_by_witness"] == row["sage_exact_rank"][
        "compressed_dimensions_by_witness"
    ]
    assert row["surrogate_rank_gate"]["remaining_equations_by_pair"] == row["sage_exact_rank"][
        "remaining_equations_by_pair"
    ]
    assert row["extraction"] == {
        "non_diagonal_solution_found": False,
        "agreement_verified": False,
        "status": "NOT_RUN",
    }


def verify_record(record: dict[str, Any]) -> None:
    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert record["n"] == 512
    assert record["k"] == 256
    assert int(record["field_denominator"]) == 17**32
    assert record["field_denominator_label"] == "17^32"
    assert record["target_bits"] == 128
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert 6 * 2**128 < 17**32 < 7 * 2**128
    assert record["target_agreement"] == 327
    assert record["baseline"] == {
        "current_pr_133_agreement": 326,
        "current_pr_133_lambda_lower": 7,
        "source": "PR #133 hybrid quotient-residual certificate",
    }

    summary = record["search_summary"]
    assert summary["generated_candidate_count"] == 20
    assert summary["retained_candidate_count"] == 6
    assert summary["exact_audited_count"] == 6
    assert summary["candidate_family"] == "multiplicity-changing degree-preserving pair replacements"
    assert summary["surrogate_field"] == "GF(12289), 512 | 12288"
    assert summary["exact_field"] == "GF(17^32)"
    assert summary["best_exact_nullity"] == 0
    assert summary["status"] == "ROUTE_CUT_TESTED_CANDIDATES"

    assert len(record["candidates"]) == 6
    assert {row["candidate_id"] for row in record["candidates"]} == EXPECTED_CANDIDATES
    for row in record["candidates"]:
        verify_candidate(row)

    assert record["interpretation"] == {
        "support_packing_blocks_a327": False,
        "multiplicity_mutation_found_exact_nullity": False,
        "candidate_found": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["open_layers"] == {
        "larger_mutation_search": True,
        "positive_exact_nullity_candidate": False,
        "non_diagonal_nullspace_extraction": True,
        "global_Lambda_mu_327_upper_bound": True,
        "status": "PARTIAL",
    }
    assert record["sage_audit"]["script"] == (
        "experimental/scripts/audit_m1_support_pattern_multiplicity_mutation_search.sage"
    )
    assert record["repo_claim"]["mca_counted"] is False
    assert "a=327 interleaved-list certificate" in record["repo_claim"]["not_claimed"]
    assert "global Lambda_mu(C,327) <= 6" in record["repo_claim"]["not_claimed"]
    assert "improvement over PR #133" in record["repo_claim"]["not_claimed"]
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["status"] == "M1_SUPPORT_PATTERN_MULTIPLICITY_MUTATION_SEARCH_ROUTE_CUT_PARTIAL"

    expected_hash = hash_payload(
        {
            "search_summary": record["search_summary"],
            "candidates": record["candidates"],
            "interpretation": record["interpretation"],
            "open": record["open_layers"],
            "global": record["global_status"],
        }
    )
    assert record["record_hash"] == expected_hash


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    record = json.loads(DATA_PATH.read_text())
    verify_record(record)
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("six multiplicity-changing support-pattern mutations exact-audited")
        print("all exact reduced rank gates have nullity 0")


if __name__ == "__main__":
    main()
