#!/usr/bin/env sage
"""Sage audit for the M1 a=327 RIM pivot-pattern profile ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from sage.all import GF


DATA_PATH = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")
SOURCE_DATA = Path("experimental/data/m1_rim_support_pattern_pivot_replay.json")


def hash_payload(payload):
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path):
    return json.loads(path.read_text())


def expected_minor_hash(cert):
    return hash_payload(
        {
            "pivot_rows_hash": cert["pivot_rows_hash"],
            "pivot_cols_hash": cert["pivot_cols_hash"],
            "pivot_pairs_hash": cert["pivot_pairs_hash"],
            "source_matrix_metadata_hash": cert["source_matrix_metadata_hash"],
        }
    )


def category_counts(cert):
    rows = cert["pivot_row_type_counts"]
    return {
        "generic_pairwise_pivots": rows.get("balanced_or_generic_pairwise_row", 0),
        "quotient_fiber_pivots": rows.get("quotient_full_fiber_row", 0),
        "residual_pivots": rows.get("residual_or_partial_fiber_row", 0),
        "support_overlap_pivots": rows.get("support_overlap_row", 0),
    }


def validate_profile(profile, source_row):
    cert = source_row["pivot_certificate"]
    matrix_cols = source_row["matrix_shape"][1]
    pivot = profile["pivot_pattern"]

    assert profile["candidate_id"] == source_row["candidate_id"]
    assert profile["source_packet"] == source_row["source_packet"]
    assert profile["source_family"] == source_row["source_family"]
    assert profile["matrix_model"] == source_row["matrix_model"]
    assert profile["matrix_shape"] == source_row["matrix_shape"]
    assert profile["rank"] == source_row["rank"] == matrix_cols
    assert profile["nullity"] == source_row["nullity"] == 0
    assert profile["compressed_variables"] == matrix_cols
    assert profile["source_matrix_metadata_hash"] == source_row[
        "source_matrix_metadata_hash"
    ]

    assert cert["rank"] == matrix_cols
    assert cert["nullity"] == 0
    assert cert["minor_rank_full"] is True
    assert cert["determinant_nonzero"] is True
    assert cert["pivot_certificate_status"] == "CERTIFIED"

    assert pivot["rref_pivot_blocks"] == matrix_cols
    assert pivot["private_pivot_blocks"] == matrix_cols
    assert pivot["pivot_rows_used"] == matrix_cols
    assert pivot["pivot_columns_used"] == matrix_cols
    assert pivot["row_type_total"] == matrix_cols
    assert pivot["row_type_counts"] == cert["pivot_row_type_counts"]
    assert pivot["pair_pivot_counts"] == cert["pivot_pair_counts"]
    assert pivot["category_counts"] == category_counts(cert)
    assert pivot["pivot_rows_hash"] == cert["pivot_rows_hash"]
    assert pivot["pivot_cols_hash"] == cert["pivot_cols_hash"]
    assert pivot["pivot_pairs_hash"] == cert["pivot_pairs_hash"]
    assert pivot["minor_hash"] == expected_minor_hash(cert)
    assert pivot["pair_profile"]["pair_pivot_total"] == matrix_cols
    assert pivot["block_triangular_order_exists"] is False
    assert pivot["block_triangular_order_status"] == "NOT_PROVED"

    if profile["source_family"] == "support_pattern":
        assert profile["classification"] == "support_overlap_rref_pivot"
        assert pivot["support_overlap_schedule"] is True
        assert pivot["category_counts"]["support_overlap_pivots"] == matrix_cols
    elif profile["source_family"] == "balanced_clique":
        assert profile["classification"] == "generic_pairwise_rref_pivot"
        assert pivot["generic_pairwise_schedule"] is True
        assert pivot["category_counts"]["generic_pairwise_pivots"] == matrix_cols
    elif profile["source_family"] == "two_level_quotient_residual":
        assert profile["classification"] == "quotient_residual_rref_pivot"
        assert pivot["quotient_residual_schedule"] is True
        assert (
            pivot["category_counts"]["quotient_fiber_pivots"]
            + pivot["category_counts"]["residual_pivots"]
            == matrix_cols
        )
    else:
        raise AssertionError("unexpected source family")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # Construct the field used by the audited source certificates. This audit
    # intentionally does not recompute all expensive rank gates.
    F = GF(17**32, "z")
    assert F.cardinality() == 17**32

    record = load_json(DATA_PATH)
    source = load_json(SOURCE_DATA)
    assert record["source_replay"]["record_hash"] == source["record_hash"]
    assert source["source_summary"]["exact_field"] == "GF(17^32)"
    assert source["source_summary"]["total_certified_after"] == 34
    assert record["profile_summary"]["source_matrices"] == 34
    assert record["profile_summary"]["pivot_covered"] == 34
    assert record["profile_summary"]["global_certificate_pattern_found"] is True
    assert record["profile_summary"]["global_common_structural_pattern_found"] is False

    source_by_key = {row["source_key"]: row for row in source["certificates"]}
    profiles = record["matrix_profiles"]
    assert len(profiles) == len(source_by_key) == 34
    for profile in profiles:
        assert profile["source_key"] in source_by_key
        validate_profile(profile, source_by_key[profile["source_key"]])

    patterns = {item["pattern_id"]: item for item in record["common_pattern_candidates"]}
    assert patterns["support_overlap_rref_pivot"]["covered_count"] == 20
    assert patterns["generic_pairwise_rref_pivot"]["covered_count"] == 6
    assert patterns["quotient_residual_rref_pivot"]["covered_count"] == 8
    assert patterns["rref_pivot_minor_certificate"]["covered_count"] == 34
    assert patterns["rref_pivot_minor_certificate"]["candidate_theorem"]["proved"] is True
    for pattern_id in [
        "support_overlap_rref_pivot",
        "generic_pairwise_rref_pivot",
        "quotient_residual_rref_pivot",
    ]:
        assert patterns[pattern_id]["candidate_theorem"]["proved"] is False

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
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "CANDIDATE_THEOREM_ONLY",
    }

    summary = {
        "field": "GF(17^32)",
        "source_matrices": 34,
        "profiles_checked": len(profiles),
        "candidate_theorems": record["theorem_status"]["candidate_theorem_count"],
        "status": record["global_status"]["status"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("SAGE_AUDIT_M1_RIM_PIVOT_PATTERN_THEOREM_OK")


if __name__ == "__main__":
    main()
