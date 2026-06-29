#!/usr/bin/env python3
"""Verify the M1 support-pattern surrogate-rank feedback search checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_support_pattern_surrogate_rank_feedback_search.json")


EXPECTED_CANDIDATES = {
    "multiplicity_spread_cyclic_45_balanced_r2_seed_202607755",
    "multiplicity_spread_cyclic_3456_balanced_r0_seed_202608129",
    "multiplicity_spread_cyclic_45_balanced_r0_seed_202607721",
    "multiplicity_spread_cyclic_45_balanced_r1_seed_202607738",
    "multiplicity_spread_cyclic_3456_balanced_r2_seed_202608163",
    "multiplicity_spread_cyclic_3456_balanced_r1_seed_202608146",
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
    assert row["mutation_family"] == "surrogate_rank_feedback_pair_replacement_membership_hypergraph"
    assert row["seed_design"] in {"cyclic_45_balanced", "cyclic_3456_balanced"}
    assert row["search_objective"] == "multiplicity_spread"
    assert row["mutation_steps"] == 900
    assert row["valid_mutation_attempts"] >= row["accepted_mutations"] >= 0
    assert row["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATE"

    support = row["support_design"]
    assert support["witness_support_sizes"] == [327] * 7
    assert support["pair_intersection_max"] <= 255
    assert len(support["pair_intersection_values"]) == 21
    assert sorted(support["pair_intersections"].values()) == support["pair_intersection_values"]
    assert support["pair_intersection_sum"] == sum(support["pair_intersection_values"])
    assert support["pair_intersection_square_sum"] == sum(
        value * value for value in support["pair_intersection_values"]
    )
    assert sum(int(size) * count for size, count in support["multiplicity_histogram"].items()) == 7 * 327
    assert sum(support["multiplicity_histogram"].values()) == 512
    assert {"1", "2", "6", "7"}.issubset(support["multiplicity_histogram"])
    assert support["membership_pattern_count"] >= 80
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

    pre = row["pre_rank_proxy"]
    assert pre["method"] == "multiplicity_pair_boundary_prefilter"
    assert isinstance(pre["proxy_score"], int)
    assert pre["status"] == "SCORED"

    feedback = row["rank_feedback"]
    assert feedback["method"] == "exact_GF_12289_rank_feedback_after_prefilter"
    assert feedback["prefilter_limit"] == 12
    assert feedback["surrogate_nullity"] == 0
    assert feedback["rank_defect_found"] is False
    assert feedback["compressed_variables"] == row["surrogate_rank_gate"]["compressed_variables"]
    assert feedback["surrogate_rank"] == row["surrogate_rank_gate"]["rank"]
    assert feedback["status"] == "SCORED"

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
    assert summary["generated_candidate_count"] == 48
    assert summary["prefiltered_for_surrogate_rank_count"] == 12
    assert summary["retained_candidate_count"] == 6
    assert summary["exact_audited_count"] == 6
    assert summary["candidate_family"] == "surrogate-rank-feedback multiplicity-changing pair replacements"
    assert summary["rank_proxy"] == "actual GF(12289) reduced rank after multiplicity/pair-boundary prefilter"
    assert summary["proxy_positive_count"] == 0
    assert summary["best_exact_nullity"] == 0
    assert summary["status"] == "ROUTE_CUT_TESTED_CANDIDATES"

    assert len(record["candidates"]) == 6
    assert {row["candidate_id"] for row in record["candidates"]} == EXPECTED_CANDIDATES
    for row in record["candidates"]:
        verify_candidate(row)

    assert record["interpretation"] == {
        "support_packing_blocks_a327": False,
        "surrogate_rank_feedback_found_proxy_nullity": False,
        "exact_audited_candidate_found_nullity": False,
        "candidate_found": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["open_layers"] == {
        "larger_stochastic_beam": True,
        "constructive_rank_defect_objective": True,
        "positive_exact_nullity_candidate": False,
        "non_diagonal_nullspace_extraction": True,
        "global_support_pattern_rank_nullity_classification": True,
        "global_Lambda_mu_327_upper_bound": True,
        "status": "PARTIAL",
    }
    assert record["sage_audit"]["script"] == (
        "experimental/scripts/audit_m1_support_pattern_surrogate_rank_feedback_search.sage"
    )
    assert record["repo_claim"]["mca_counted"] is False
    assert "a=327 interleaved-list certificate" in record["repo_claim"]["not_claimed"]
    assert "global Lambda_mu(C,327) <= 6" in record["repo_claim"]["not_claimed"]
    assert "global support-pattern rank-nullity classification" in record["repo_claim"]["not_claimed"]
    assert "improvement over PR #133" in record["repo_claim"]["not_claimed"]
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["status"] == "M1_SUPPORT_PATTERN_SURROGATE_RANK_FEEDBACK_SEARCH_ROUTE_CUT_PARTIAL"

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
        print("six surrogate-rank-feedback candidates exact-audited")
        print("all exact reduced rank gates have nullity 0")


if __name__ == "__main__":
    main()
