#!/usr/bin/env python3
"""Dependency-free verifier for full M1 RIM pivot-certificate replay."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_rim_support_pattern_pivot_replay.json")

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

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "global RIM full-rank theorem",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_record(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def aggregate_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        value = str(row[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def aggregate_pivot_row_types(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        for row_type, count in row["pivot_certificate"]["pivot_row_type_counts"].items():
            out[row_type] = out.get(row_type, 0) + count
    return dict(sorted(out.items()))


def certified_by_source_packet(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    for row in rows:
        packet = row["source_packet"]
        if packet not in out:
            out[packet] = {"source_matrices": 0, "certified": 0, "pending": 0}
        out[packet]["source_matrices"] += 1
        out[packet]["certified"] += 1
    return dict(sorted(out.items()))


def validate_certificate(row: dict[str, Any]) -> None:
    cert = row["pivot_certificate"]
    matrix_rows, matrix_cols = row["matrix_shape"]

    assert row["status"] == "CERTIFIED_FULL_RANK"
    assert row["certificate_type"] == "RREF_PIVOT"
    assert row["pivot_certificate_status"] == "CERTIFIED"
    assert cert["certificate_type"] == "RREF_PIVOT"
    assert cert["pivot_certificate_status"] == "CERTIFIED"
    assert cert["status"] == "CERTIFIED_FULL_RANK"
    assert cert["matrix_rows"] == matrix_rows
    assert cert["matrix_cols"] == matrix_cols
    assert cert["rank"] == row["rank"] == matrix_cols
    assert cert["nullity"] == row["nullity"] == 0
    assert cert["minor_size"] == matrix_cols
    assert cert["pivot_minor_size"] == matrix_cols
    assert cert["minor_rank"] == matrix_cols
    assert cert["minor_rank_full"] is True
    assert cert["determinant_nonzero"] is True
    assert len(cert["pivot_rows_hash"]) == 64
    assert len(cert["pivot_cols_hash"]) == 64
    assert len(cert["pivot_pairs_hash"]) == 64
    assert cert["source_matrix_metadata_hash"] == row["source_matrix_metadata_hash"]
    assert cert["source_family"] == row["source_family"]
    assert sum(cert["pivot_row_type_counts"].values()) == matrix_cols
    assert sum(cert["pivot_pair_counts"].values()) == matrix_cols

    if row["source_packet"] == "pairwise_divisibility_nullvector_system":
        assert row["source_family"] == "balanced_clique"
        assert row["matrix_model"] == "pairwise_divisibility"
        assert cert["generic_row_count"] == matrix_cols
        assert cert["quotient_row_count"] == 0
        assert cert["residual_row_count"] == 0
        assert cert["support_overlap_row_count"] == 0
    elif row["source_packet"] == "two_level_pairwise_divisibility":
        assert row["source_family"] == "two_level_quotient_residual"
        assert row["matrix_model"] == "two_level_pairwise_divisibility"
        assert cert["generic_row_count"] == 0
        assert cert["quotient_row_count"] + cert["residual_row_count"] == matrix_cols
        assert cert["support_overlap_row_count"] == 0
    else:
        assert row["source_family"] == "support_pattern"
        assert row["matrix_model"] == "support_design_reduced_intersection_matrix"
        assert cert["generic_row_count"] == 0
        assert cert["quotient_row_count"] == 0
        assert cert["residual_row_count"] == 0
        assert cert["support_overlap_row_count"] == matrix_cols


def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert record["denominator"] == "17^32"
    assert record["n"] == 512
    assert record["k"] == 256
    assert record["agreement_target"] == 327
    assert record["target_bits"] == 128
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert record["construction_mode"] == "rim_support_pattern_pivot_replay"

    certificates = record["certificates"]
    assert len(certificates) == 34
    assert all(row["status"] == "CERTIFIED_FULL_RANK" for row in certificates)
    assert aggregate_by(certificates, "source_packet") == EXPECTED_SOURCE_PACKET_COUNTS
    assert aggregate_by(certificates, "matrix_model") == EXPECTED_MODEL_COUNTS

    summary = record["source_summary"]
    assert summary["source_matrix_count"] == 34
    assert summary["previous_certified_count"] == 14
    assert summary["new_certified_count"] == 20
    assert summary["total_certified_after"] == 34
    assert summary["deferred_count_after"] == 0
    assert summary["source_packet_counts"] == EXPECTED_SOURCE_PACKET_COUNTS
    assert summary["matrix_model_counts"] == EXPECTED_MODEL_COUNTS
    assert summary["certified_by_source_packet"] == certified_by_source_packet(certificates)
    assert summary["exact_field"] == "GF(17^32)"
    assert summary["status"] == "PIVOT_COVERAGE_COMPLETE"

    for row in certificates:
        validate_certificate(row)

    pivot_summary = record["pivot_summary"]
    assert pivot_summary == {
        "certificate_type": "RREF_PIVOT",
        "pivot_row_type_counts": aggregate_pivot_row_types(certificates),
        "common_pivot_pattern_found": False,
        "all_source_matrices_certified": True,
        "status": "PIVOT_COVERAGE_COMPLETE",
    }
    assert record["interpretation"] == {
        "a327_certificate_found": False,
        "candidate_found": False,
        "global_Lambda_mu_327_upper_bound": False,
        "coverage_increased_from_14_to_34": True,
        "status": "PIVOT_COVERAGE_COMPLETE",
    }
    assert record["open_layers"] == {
        "common_pivot_pattern_theorem": True,
        "global_Lambda_mu_327_upper_bound": True,
        "status": "PARTIAL",
    }
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "PIVOT_COVERAGE_COMPLETE",
    }
    assert record["repo_claim"]["mca_counted"] is False
    assert set(record["repo_claim"]["not_claimed"]) == REQUIRED_NONCLAIMS

    expected_hash = hash_payload(
        {
            "source_summary": record["source_summary"],
            "pivot_summary": record["pivot_summary"],
            "certificates": record["certificates"],
            "interpretation": record["interpretation"],
            "open": record["open_layers"],
            "global": record["global_status"],
        }
    )
    assert record["record_hash"] == expected_hash

    return {
        "source_matrices": len(certificates),
        "certified_count": len(certificates),
        "support_pattern_certified": EXPECTED_MODEL_COUNTS[
            "support_design_reduced_intersection_matrix"
        ],
        "status": record["global_status"]["status"],
        "record_hash": record["record_hash"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=DATA_PATH, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = validate_record(load_record(args.data))
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("M1_RIM_SUPPORT_PATTERN_PIVOT_REPLAY_VERIFY_OK")
        print(f"source matrices: {summary['source_matrices']}")
        print(f"certified: {summary['certified_count']}")
        print(f"support-pattern certified: {summary['support_pattern_certified']}")
        print(f"status: {summary['status']}")


if __name__ == "__main__":
    main()
