#!/usr/bin/env python3
"""Dependency-free verifier for the M1 quotient-residual RIM pivot audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_quotient_residual_rim_pivot_certificates.json")

EXPECTED_SOURCE_PACKET_COUNTS = {
    "constructive_rank_defect_support_design": 8,
    "pairwise_divisibility_nullvector_system": 6,
    "support_pattern_multiplicity_mutation_search": 6,
    "support_pattern_surrogate_rank_feedback_search": 6,
    "two_level_pairwise_divisibility": 8,
}

EXPECTED_MATRIX_MODEL_COUNTS = {
    "pairwise_divisibility": 6,
    "support_design_reduced_intersection_matrix": 20,
    "two_level_pairwise_divisibility": 8,
}

CERTIFIED_TWO_LEVEL_IDS = {
    "common_six_fiber_residual_10",
    "common_six_fiber_residual_11",
    "punctured_eight_fiber_10",
    "punctured_eight_fiber_11",
    "seven_fibers_plus_residual_10",
    "seven_fibers_plus_residual_11",
}

ANCHOR_RELAXED_IDS = {
    "anchor_relaxed_boundary_10",
    "anchor_relaxed_boundary_11",
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
    assert record["construction_mode"] == "rim_pivot_certificate_audit"

    certificates = record["certificates"]
    assert isinstance(certificates, list)
    assert len(certificates) == 34

    summary = record["source_summary"]
    assert summary["source_packet_count"] == 5
    assert summary["source_matrix_count"] == 34
    assert summary["certified_full_rank_count"] == 6
    assert summary["pending_certificate_count"] == 28
    assert summary["source_packet_counts"] == EXPECTED_SOURCE_PACKET_COUNTS
    assert summary["matrix_model_counts"] == EXPECTED_MATRIX_MODEL_COUNTS
    assert summary["exact_field"] == "GF(17^32)"
    assert summary["status"] == "PARTIAL"

    certified = [row for row in certificates if row["status"] == "CERTIFIED_FULL_RANK"]
    pending = [row for row in certificates if row["status"] == "PENDING"]
    assert len(certified) == 6
    assert len(pending) == 28
    assert {row["candidate_id"] for row in certified} == CERTIFIED_TWO_LEVEL_IDS
    assert {row["source_packet"] for row in certified} == {"two_level_pairwise_divisibility"}

    for row in certified:
        assert row["certificate_type"] == "RREF_PIVOT_MINOR"
        assert row["rank"] == row["matrix_shape"][1] == 6
        assert row["nullity"] == 0
        cert = row["pivot_certificate"]
        assert cert["certificate_type"] == "RREF_PIVOT_MINOR"
        assert cert["minor_size"] == 6
        assert cert["matrix_cols"] == 6
        assert cert["rank"] == 6
        assert cert["nullity"] == 0
        assert cert["minor_rank"] == 6
        assert cert["minor_rank_full"] is True
        assert cert["minor_det_nonzero"] is True
        assert cert["status"] == "CERTIFIED_FULL_RANK"
        assert len(cert["pivot_rows_hash"]) == 64
        assert len(cert["pivot_cols_hash"]) == 64
        assert len(cert["pivot_pairs_hash"]) == 64
        assert cert["source_matrix_metadata_hash"] == row["source_matrix_metadata_hash"]
        assert sum(cert["pivot_row_type_counts"].values()) == 6
        assert sum(cert["pivot_pair_counts"].values()) == 6
        assert cert["pivot_pair_counts"] == {
            "1,2": 2,
            "1,3": 1,
            "1,4": 1,
            "1,5": 1,
            "1,6": 1,
        }
        assert cert["compressed_dimensions_by_witness"] == {
            "1": 1,
            "2": 1,
            "3": 1,
            "4": 1,
            "5": 1,
            "6": 1,
        }
        assert set(cert["remaining_equations_by_pair"].values()) == {255}

    certified_profile = {
        row["candidate_id"]: row["pivot_certificate"]["pivot_row_type_counts"]
        for row in certified
    }
    assert certified_profile["seven_fibers_plus_residual_10"] == {"quotient_full_fiber_row": 6}
    assert certified_profile["seven_fibers_plus_residual_11"] == {"quotient_full_fiber_row": 6}
    assert certified_profile["punctured_eight_fiber_10"] == {
        "quotient_full_fiber_row": 5,
        "residual_or_partial_fiber_row": 1,
    }
    assert certified_profile["punctured_eight_fiber_11"] == {
        "quotient_full_fiber_row": 5,
        "residual_or_partial_fiber_row": 1,
    }
    assert certified_profile["common_six_fiber_residual_10"] == {
        "quotient_full_fiber_row": 1,
        "residual_or_partial_fiber_row": 5,
    }
    assert certified_profile["common_six_fiber_residual_11"] == {
        "quotient_full_fiber_row": 1,
        "residual_or_partial_fiber_row": 5,
    }

    pending_by_id = {row["candidate_id"]: row for row in pending}
    assert ANCHOR_RELAXED_IDS.issubset(pending_by_id)
    for candidate_id in ANCHOR_RELAXED_IDS:
        row = pending_by_id[candidate_id]
        cert = row["pivot_certificate"]
        assert row["source_packet"] == "two_level_pairwise_divisibility"
        assert cert["certificate_type"] == "PIVOT_CERTIFICATE_PENDING_LARGE_MATRIX"
        assert cert["compressed_variables"] == 192
        assert cert["pivot_column_limit"] == 64
        assert cert["status"] == "PIVOT_EXTRACTION_DEFERRED"

    for row in pending:
        cert = row["pivot_certificate"]
        assert cert["status"] in {"SOURCE_REPLAY_PENDING", "PIVOT_EXTRACTION_DEFERRED"}
        if row["candidate_id"] not in ANCHOR_RELAXED_IDS:
            assert cert["certificate_type"] == "SOURCE_REPLAY_PENDING"
            assert cert["status"] == "SOURCE_REPLAY_PENDING"

    pivot_summary = record["pivot_summary"]
    assert pivot_summary == {
        "certificate_type": "RREF_PIVOT_MINOR",
        "all_certified_minors_full_rank": False,
        "pivot_row_type_counts": {
            "quotient_full_fiber_row": 24,
            "residual_or_partial_fiber_row": 12,
        },
        "status": "PARTIAL",
    }

    assert record["interpretation"] == {
        "full_rank_replaced_by_replayable_pivot_certificates": False,
        "candidate_found": False,
        "a327_certificate_found": False,
        "global_Lambda_mu_327_upper_bound": False,
        "status": "PARTIAL",
    }
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "PARTIAL",
    }
    assert record["open_layers"] == {
        "symbolic_pivot_pattern_theorem": True,
        "quotient_residual_designs_outside_sources": True,
        "global_Lambda_mu_327_upper_bound": True,
        "status": "PARTIAL",
    }

    repo_claim = record["repo_claim"]
    assert repo_claim["mca_counted"] is False
    assert set(repo_claim["not_claimed"]) == REQUIRED_NONCLAIMS

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
        "status": "OK",
        "source_matrix_count": len(certificates),
        "certified_full_rank_count": len(certified),
        "pending_certificate_count": len(pending),
        "record_hash": record["record_hash"],
        "global_status": record["global_status"]["status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", default=DATA_PATH, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = validate_record(load_record(args.path))
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("VERIFY_M1_QUOTIENT_RESIDUAL_RIM_PIVOT_CERTIFICATES_OK")
        print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
