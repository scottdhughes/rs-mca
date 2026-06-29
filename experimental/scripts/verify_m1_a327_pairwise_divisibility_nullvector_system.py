#!/usr/bin/env python3
"""Verify the M1 a=327 pairwise-divisibility null-vector checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairwise_divisibility_nullvector_system.json")

EXPECTED_CANDIDATES = {
    "balanced_clique_m2_o1",
    "balanced_clique_m6_o1",
    "balanced_clique_m5_o1",
    "balanced_clique_m2_o0",
    "balanced_clique_m6_o0",
    "balanced_clique_m1_o0",
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
    assert row["construction_family"] == "balanced_clique_blocks"
    assert row["construction_mode"] == "pairwise_divisibility_nullvector"
    assert row["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATE"

    design = row["equality_design"]
    assert design["coordinate_count"] == 512
    assert design["min_witness_equality_incidence"] >= 327
    assert len(design["witness_equality_incidences"]) == 7
    assert len(design["pair_equality_counts"]) == 21
    assert len(design["pair_equality_values"]) == 21
    assert sorted(design["pair_equality_counts"].values()) == design["pair_equality_values"]
    assert design["max_pair_equality_size"] <= 255
    assert design["pair_equalities_at_255"] == 0
    assert design["pair_equality_sum"] == sum(design["pair_equality_values"])
    assert sum(design["block_size_histogram"].values()) >= 512
    assert design["partition_pattern_count"] > 0
    assert len(design["partition_pattern_histogram_hash"]) == 64
    assert len(design["equality_pattern_hash"]) == 64
    assert len(design["quotient_fiber_profile"]) == 16

    structural = row["structural_score"]
    assert structural["method"] == "pairwise_divisibility_structural_screen"
    assert structural["compressed_variables_estimate"] == row["surrogate_rank_gate"][
        "compressed_variables"
    ]
    assert structural["status"] == "SCORED"

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
    assert record["denominator"] == "17^32"
    assert int(record["field_denominator"]) == 17**32
    assert record["target_bits"] == 128
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert 6 * 2**128 < 17**32 < 7 * 2**128
    assert record["agreement_target"] == 327
    assert record["baseline"] == {
        "current_pr_133_agreement": 326,
        "current_pr_133_lambda_lower": 7,
        "source": "PR #133 hybrid quotient-residual certificate",
    }
    assert record["construction_mode"] == "pairwise_divisibility_nullvector"

    summary = record["search_summary"]
    assert summary["generated_spec_count"] == 48
    assert summary["valid_pairwise_design_count"] == 19
    assert summary["rank_screen_candidate_count"] == 12
    assert summary["retained_candidate_count"] == 6
    assert summary["exact_audited_count"] == 6
    assert summary["random_seed"] == 2026062804
    assert summary["families"] == [
        "balanced_clique_blocks",
        "quotient_fiber_pairwise_blocks",
        "pair_boundary_design",
        "mixed_clique_design",
    ]
    assert summary["valid_family_counts"] == {
        "balanced_clique_blocks": 11,
        "mixed_clique_design": 8,
    }
    assert summary["retained_family_counts"] == {"balanced_clique_blocks": 6}
    assert summary["rank_proxy"] == "GF(12289) pairwise-divisibility reduced rank"
    assert summary["surrogate_field"] == "GF(12289), 512 | 12288"
    assert summary["exact_field"] == "GF(17^32)"
    assert summary["proxy_positive_count"] == 0
    assert summary["best_exact_nullity"] == 0
    assert summary["candidate_found"] is False
    assert summary["status"] == "ROUTE_CUT_TESTED_CANDIDATES"

    assert len(record["candidates"]) == 6
    assert {row["candidate_id"] for row in record["candidates"]} == EXPECTED_CANDIDATES
    for row in record["candidates"]:
        verify_candidate(row)

    assert record["interpretation"] == {
        "pairwise_equalities_designed_jointly": True,
        "support_packing_only": False,
        "exact_audited_candidate_found_nullity": False,
        "a327_certificate_found": False,
        "global_Lambda_mu_327_upper_bound": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["open_layers"] == {
        "larger_pairwise_divisibility_systems": True,
        "non_diagonal_nullspace_extraction": True,
        "value_class_max_min_after_positive_nullity": True,
        "two_level_quotient_plus_residual": True,
        "global_Lambda_mu_327_upper_bound": True,
        "status": "PARTIAL",
    }
    assert record["sage_audit"]["script"] == (
        "experimental/scripts/audit_m1_a327_pairwise_divisibility_nullvector_system.sage"
    )
    assert record["sage_audit"]["constructs_GF_17_32"] is True
    assert record["repo_claim"]["mca_counted"] is False
    assert "a=327 interleaved-list certificate" in record["repo_claim"]["not_claimed"]
    assert "global Lambda_mu(C,327) <= 6" in record["repo_claim"]["not_claimed"]
    assert "global pairwise-divisibility obstruction" in record["repo_claim"]["not_claimed"]
    assert "improvement over PR #133" in record["repo_claim"]["not_claimed"]
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["status"] == "M1_A327_PAIRWISE_DIVISIBILITY_NULLVECTOR_SYSTEM_PARTIAL"

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
        print("48 pairwise-divisibility specs generated")
        print("6 retained candidates exact-audited over GF(17^32)")
        print("all retained reduced rank gates have nullity 0")


if __name__ == "__main__":
    main()
