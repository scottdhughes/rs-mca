#!/usr/bin/env python3
"""Verify the M1 a=327 two-level pairwise-divisibility checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_two_level_pairwise_divisibility.json")

EXPECTED_CANDIDATES = {
    "anchor_relaxed_boundary_11",
    "anchor_relaxed_boundary_10",
    "common_six_fiber_residual_11",
    "common_six_fiber_residual_10",
    "punctured_eight_fiber_11",
    "punctured_eight_fiber_10",
    "seven_fibers_plus_residual_11",
    "seven_fibers_plus_residual_10",
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
    assert row["construction_family"] in {
        "anchor_relaxed_boundary",
        "common_six_fiber_residual",
        "punctured_eight_fiber",
        "seven_fibers_plus_residual",
    }
    assert row["construction_mode"] == "two_level_pairwise_divisibility"
    assert row["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATE"

    design = row["pairwise_design"]
    assert len(design["pair_equality_counts"]) == 21
    assert sorted(design["pair_equality_counts"].values()) == design["pair_equality_values"]
    assert design["max_pair_equality_size"] == 255
    assert design["min_witness_pair_equality_total"] >= 327
    assert len(design["witness_pair_equality_totals"]) == 7
    assert len(design["full_fiber_counts"]) == 21
    assert len(design["residual_counts"]) == 21
    assert len(design["quotient_fiber_profile"]) == 21
    assert len(design["pair_set_hash"]) == 64

    if row["construction_family"] == "anchor_relaxed_boundary":
        assert design["min_pair_equality_size"] == 224
        assert design["pair_equalities_at_255"] == 15
        assert row["sage_exact_rank"]["compressed_variables"] == 192
    else:
        assert design["min_pair_equality_size"] == 255
        assert design["pair_equalities_at_255"] == 21
        assert row["sage_exact_rank"]["compressed_variables"] == 6

    structural = row["structural_score"]
    assert structural["method"] == "two_level_pairwise_divisibility_structural_screen"
    assert structural["family"] == row["construction_family"]
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
    assert record["construction_mode"] == "two_level_pairwise_divisibility"

    summary = record["search_summary"]
    assert summary["generated_spec_count"] == 48
    assert summary["valid_pairwise_design_count"] == 48
    assert summary["rank_screen_candidate_count"] == 16
    assert summary["retained_candidate_count"] == 8
    assert summary["exact_audited_count"] == 8
    assert summary["random_seed"] == 2026062805
    assert summary["families"] == [
        "seven_fibers_plus_residual",
        "punctured_eight_fiber",
        "common_six_fiber_residual",
        "anchor_relaxed_boundary",
    ]
    assert summary["valid_family_counts"] == {
        "anchor_relaxed_boundary": 12,
        "common_six_fiber_residual": 12,
        "punctured_eight_fiber": 12,
        "seven_fibers_plus_residual": 12,
    }
    assert summary["retained_family_counts"] == {
        "anchor_relaxed_boundary": 2,
        "common_six_fiber_residual": 2,
        "punctured_eight_fiber": 2,
        "seven_fibers_plus_residual": 2,
    }
    assert summary["rank_proxy"] == "GF(12289) two-level pairwise-divisibility reduced rank"
    assert summary["surrogate_field"] == "GF(12289), 512 | 12288"
    assert summary["exact_field"] == "GF(17^32)"
    assert summary["proxy_positive_count"] == 0
    assert summary["best_exact_nullity"] == 0
    assert summary["candidate_found"] is False
    assert summary["status"] == "ROUTE_CUT_TESTED_CANDIDATES"

    assert len(record["candidates"]) == 8
    assert {row["candidate_id"] for row in record["candidates"]} == EXPECTED_CANDIDATES
    for row in record["candidates"]:
        verify_candidate(row)

    assert record["interpretation"] == {
        "pairwise_equalities_designed_jointly": True,
        "quotient_fiber_structure_used": True,
        "residual_defects_used": True,
        "exact_audited_candidate_found_nullity": False,
        "a327_certificate_found": False,
        "global_Lambda_mu_327_upper_bound": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["open_layers"] == {
        "larger_two_level_pairwise_systems": True,
        "non_diagonal_nullspace_extraction": True,
        "value_class_max_min_after_positive_nullity": True,
        "symbolic_reduced_rank_obstruction": True,
        "global_Lambda_mu_327_upper_bound": True,
        "status": "PARTIAL",
    }
    assert record["sage_audit"]["script"] == (
        "experimental/scripts/audit_m1_a327_two_level_pairwise_divisibility.sage"
    )
    assert record["sage_audit"]["constructs_GF_17_32"] is True
    assert record["repo_claim"]["mca_counted"] is False
    assert "a=327 interleaved-list certificate" in record["repo_claim"]["not_claimed"]
    assert "global Lambda_mu(C,327) <= 6" in record["repo_claim"]["not_claimed"]
    assert "global two-level pairwise-divisibility obstruction" in record["repo_claim"]["not_claimed"]
    assert "improvement over PR #133" in record["repo_claim"]["not_claimed"]
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    assert record["status"] == "M1_A327_TWO_LEVEL_PAIRWISE_DIVISIBILITY_PARTIAL"

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
        print("48 two-level pairwise-divisibility specs generated")
        print("8 retained candidates exact-audited over GF(17^32)")
        print("all retained reduced rank gates have nullity 0")


if __name__ == "__main__":
    main()
