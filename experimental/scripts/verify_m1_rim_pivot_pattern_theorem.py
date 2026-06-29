#!/usr/bin/env python3
"""Dependency-free verifier for the M1 RIM pivot-pattern audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")
SOURCE_DATA = Path("experimental/data/m1_rim_support_pattern_pivot_replay.json")

EXPECTED_SOURCE_FAMILY_COUNTS = {
    "balanced_clique": 6,
    "support_pattern": 20,
    "two_level_quotient_residual": 8,
}

EXPECTED_SOURCE_PACKET_COUNTS = {
    "constructive_rank_defect_support_design": 8,
    "pairwise_divisibility_nullvector_system": 6,
    "support_pattern_multiplicity_mutation_search": 6,
    "support_pattern_surrogate_rank_feedback_search": 6,
    "two_level_pairwise_divisibility": 8,
}

EXPECTED_MODEL_COUNTS = {
    "pairwise_divisibility": 6,
    "support_design_reduced_intersection_matrix": 20,
    "two_level_pairwise_divisibility": 8,
}

EXPECTED_ROW_TYPE_COUNTS = {
    "balanced_or_generic_pairwise_row": 1226,
    "quotient_full_fiber_row": 383,
    "residual_or_partial_fiber_row": 37,
    "support_overlap_row": 1901,
}

EXPECTED_PATTERN_COUNTS = {
    "generic_pairwise_rref_pivot": 6,
    "quotient_residual_rref_pivot": 8,
    "rref_pivot_minor_certificate": 34,
    "support_overlap_rref_pivot": 20,
}

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "global RIM full-rank theorem",
    "deterministic pivot-pattern theorem",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def aggregate_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        value = str(item[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def add_counts(dst: dict[str, int], src: dict[str, int]) -> None:
    for key, value in src.items():
        dst[key] = dst.get(key, 0) + value


def aggregate_row_types(profiles: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for profile in profiles:
        add_counts(out, profile["pivot_pattern"]["row_type_counts"])
    return dict(sorted(out.items()))


def aggregate_pairs(profiles: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for profile in profiles:
        add_counts(out, profile["pivot_pattern"]["pair_pivot_counts"])
    return dict(sorted(out.items()))


def expected_minor_hash(cert: dict[str, Any]) -> str:
    return hash_payload(
        {
            "pivot_rows_hash": cert["pivot_rows_hash"],
            "pivot_cols_hash": cert["pivot_cols_hash"],
            "pivot_pairs_hash": cert["pivot_pairs_hash"],
            "source_matrix_metadata_hash": cert["source_matrix_metadata_hash"],
        }
    )


def validate_profile(profile: dict[str, Any], source_by_key: dict[str, dict[str, Any]]) -> None:
    source = source_by_key[profile["source_key"]]
    cert = source["pivot_certificate"]
    matrix_rows, matrix_cols = profile["matrix_shape"]
    pivot = profile["pivot_pattern"]

    assert profile["candidate_id"] == source["candidate_id"]
    assert profile["source_packet"] == source["source_packet"]
    assert profile["source_family"] == source["source_family"]
    assert profile["matrix_model"] == source["matrix_model"]
    assert profile["rank"] == source["rank"] == matrix_cols
    assert profile["nullity"] == source["nullity"] == 0
    assert profile["compressed_variables"] == matrix_cols
    assert profile["pivot_certificate_status"] == "CERTIFIED"
    assert profile["certificate_type"] == "RREF_PIVOT"
    assert profile["source_matrix_metadata_hash"] == source["source_matrix_metadata_hash"]
    assert profile["status"] == "PATTERN_PROFILED"

    assert cert["matrix_rows"] == matrix_rows
    assert cert["matrix_cols"] == matrix_cols
    assert cert["rank"] == matrix_cols
    assert cert["nullity"] == 0
    assert cert["minor_rank_full"] is True
    assert cert["determinant_nonzero"] is True

    assert pivot["rref_pivot_blocks"] == matrix_cols
    assert pivot["private_pivot_blocks"] == matrix_cols
    assert pivot["pivot_rows_used"] == matrix_cols
    assert pivot["pivot_columns_used"] == matrix_cols
    assert pivot["row_type_total"] == matrix_cols
    assert pivot["row_type_counts"] == cert["pivot_row_type_counts"]
    assert pivot["pair_pivot_counts"] == cert["pivot_pair_counts"]
    assert pivot["pivot_rows_hash"] == cert["pivot_rows_hash"]
    assert pivot["pivot_cols_hash"] == cert["pivot_cols_hash"]
    assert pivot["pivot_pairs_hash"] == cert["pivot_pairs_hash"]
    assert pivot["minor_hash"] == expected_minor_hash(cert)
    assert pivot["block_triangular_order_exists"] is False
    assert pivot["block_triangular_order_status"] == "NOT_PROVED"
    assert pivot["pair_profile"]["pair_pivot_total"] == matrix_cols

    if profile["source_family"] == "support_pattern":
        assert profile["classification"] == "support_overlap_rref_pivot"
        assert pivot["support_overlap_schedule"] is True
        assert pivot["generic_pairwise_schedule"] is False
        assert pivot["quotient_residual_schedule"] is False
        assert pivot["category_counts"] == {
            "generic_pairwise_pivots": 0,
            "quotient_fiber_pivots": 0,
            "residual_pivots": 0,
            "support_overlap_pivots": matrix_cols,
        }
    elif profile["source_family"] == "balanced_clique":
        assert profile["classification"] == "generic_pairwise_rref_pivot"
        assert pivot["generic_pairwise_schedule"] is True
        assert pivot["support_overlap_schedule"] is False
        assert pivot["quotient_residual_schedule"] is False
        assert pivot["category_counts"]["generic_pairwise_pivots"] == matrix_cols
    elif profile["source_family"] == "two_level_quotient_residual":
        assert profile["classification"] == "quotient_residual_rref_pivot"
        assert pivot["quotient_residual_schedule"] is True
        assert pivot["support_overlap_schedule"] is False
        assert pivot["generic_pairwise_schedule"] is False
        assert (
            pivot["category_counts"]["quotient_fiber_pivots"]
            + pivot["category_counts"]["residual_pivots"]
            == matrix_cols
        )
    else:
        raise AssertionError(f"unexpected source family: {profile['source_family']}")


def validate_patterns(record: dict[str, Any]) -> None:
    patterns = record["common_pattern_candidates"]
    by_id = {pattern["pattern_id"]: pattern for pattern in patterns}
    assert set(by_id) == set(EXPECTED_PATTERN_COUNTS)
    for pattern_id, expected_count in EXPECTED_PATTERN_COUNTS.items():
        pattern = by_id[pattern_id]
        assert pattern["covered_count"] == expected_count
        assert pattern["uncovered_count"] == 34 - expected_count
        if pattern_id == "rref_pivot_minor_certificate":
            assert pattern["status"] == "CERTIFICATE_PATTERN"
            assert pattern["global_coverage"] is True
            assert pattern["candidate_theorem"]["proved"] is True
            assert pattern["candidate_theorem"]["status"] == "COMPUTATIONAL_CERTIFICATE"
        else:
            assert pattern["status"] == "CANDIDATE_PATTERN"
            assert pattern["global_coverage"] is False
            assert pattern["candidate_theorem"]["proved"] is False
            assert pattern["candidate_theorem"]["status"] == "CANDIDATE_THEOREM"


def validate_record(record: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert record["denominator"] == "17^32"
    assert record["n"] == 512
    assert record["k"] == 256
    assert record["agreement_target"] == 327
    assert record["target_bits"] == 128
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert record["construction_mode"] == "rim_pivot_pattern_theorem_audit"

    assert record["source_replay"] == {
        "path": str(SOURCE_DATA),
        "record_hash": source["record_hash"],
        "source_matrices": 34,
        "pivot_covered": 34,
        "status": "PIVOT_COVERAGE_COMPLETE",
    }

    profiles = record["matrix_profiles"]
    assert len(profiles) == 34
    source_by_key = {row["source_key"]: row for row in source["certificates"]}
    assert set(source_by_key) == {profile["source_key"] for profile in profiles}
    for profile in profiles:
        validate_profile(profile, source_by_key)

    summary = record["profile_summary"]
    assert summary["source_matrices"] == 34
    assert summary["pivot_covered"] == 34
    assert summary["source_family_counts"] == EXPECTED_SOURCE_FAMILY_COUNTS
    assert summary["source_packet_counts"] == EXPECTED_SOURCE_PACKET_COUNTS
    assert summary["matrix_model_counts"] == EXPECTED_MODEL_COUNTS
    assert summary["aggregate_row_type_counts"] == EXPECTED_ROW_TYPE_COUNTS
    assert summary["aggregate_row_type_counts"] == aggregate_row_types(profiles)
    assert summary["aggregate_pair_pivot_counts"] == aggregate_pairs(profiles)
    assert summary["support_pattern_rows"] == 20
    assert summary["support_pattern_all_support_overlap"] is True
    assert summary["global_common_structural_pattern_found"] is False
    assert summary["global_certificate_pattern_found"] is True
    assert summary["status"] == "PIVOT_PROFILED"

    validate_patterns(record)
    assert record["theorem_status"] == {
        "candidate_theorem_count": 3,
        "proved_theorem_count": 0,
        "common_pivot_pattern_theorem_proved": False,
        "support_overlap_schedule_candidate": True,
        "status": "CANDIDATE_THEOREM_ONLY",
    }
    assert record["interpretation"] == {
        "a327_certificate_found": False,
        "candidate_found": False,
        "global_Lambda_mu_327_upper_bound": False,
        "pivot_profiles_mined": True,
        "common_pivot_pattern_theorem_proved": False,
        "status": "AUDIT",
    }
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "CANDIDATE_THEOREM_ONLY",
    }
    assert record["repo_claim"]["mca_counted"] is False
    assert set(record["repo_claim"]["not_claimed"]) == REQUIRED_NONCLAIMS

    expected_hash = hash_payload(
        {
            "source_replay": record["source_replay"],
            "profile_summary": record["profile_summary"],
            "common_pattern_candidates": record["common_pattern_candidates"],
            "matrix_profiles": record["matrix_profiles"],
            "theorem_status": record["theorem_status"],
            "interpretation": record["interpretation"],
            "global": record["global_status"],
        }
    )
    assert record["record_hash"] == expected_hash
    return {
        "source_matrices": len(profiles),
        "pattern_candidates": record["theorem_status"]["candidate_theorem_count"],
        "support_pattern_profiles": summary["support_pattern_rows"],
        "status": record["global_status"]["status"],
        "record_hash": record["record_hash"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=DATA_PATH, type=Path)
    parser.add_argument("--source", default=SOURCE_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = validate_record(load_json(args.data), load_json(args.source))
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("M1_RIM_PIVOT_PATTERN_THEOREM_VERIFY_OK")
        print(f"source matrices: {summary['source_matrices']}")
        print(f"pattern candidates: {summary['pattern_candidates']}")
        print(f"support-pattern profiles: {summary['support_pattern_profiles']}")
        print(f"status: {summary['status']}")


if __name__ == "__main__":
    main()
