#!/usr/bin/env python3
"""Dependency-free verifier for M1 support-overlap pivot schedules."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_support_overlap_pivot_schedule.json")
SOURCE_DATA = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")

EXPECTED_SOURCE_PACKET_COUNTS = {
    "constructive_rank_defect_support_design": 8,
    "support_pattern_multiplicity_mutation_search": 6,
    "support_pattern_surrogate_rank_feedback_search": 6,
}

EXPECTED_PAIR_COUNTS = {
    "1,2": 569,
    "1,3": 386,
    "1,4": 404,
    "1,5": 353,
    "1,6": 189,
}

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "global RIM full-rank theorem",
    "deterministic combinatorial pivot schedule",
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


def add_counts(dst: dict[str, int], src: dict[str, int]) -> None:
    for key, value in src.items():
        dst[key] = dst.get(key, 0) + value


def aggregate_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        value = str(item[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def aggregate_pairs(schedules: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for schedule in schedules:
        add_counts(out, schedule["pivot_schedule"]["pair_pivot_counts"])
    return dict(sorted(out.items()))


def source_support_profiles(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        profile["source_key"]: profile
        for profile in source["matrix_profiles"]
        if profile["classification"] == "support_overlap_rref_pivot"
    }


def validate_schedule(schedule: dict[str, Any], source_profile: dict[str, Any]) -> None:
    pivot = schedule["pivot_schedule"]
    source_pivot = source_profile["pivot_pattern"]
    matrix_rows, matrix_cols = schedule["matrix_shape"]

    assert schedule["candidate_id"] == source_profile["candidate_id"]
    assert schedule["source_packet"] == source_profile["source_packet"]
    assert schedule["source_family"] == "support_pattern"
    assert schedule["source_family"] == source_profile["source_family"]
    assert schedule["matrix_model"] == "support_design_reduced_intersection_matrix"
    assert schedule["matrix_model"] == source_profile["matrix_model"]
    assert schedule["rank"] == source_profile["rank"] == matrix_cols
    assert schedule["nullity"] == source_profile["nullity"] == 0
    assert schedule["source_matrix_metadata_hash"] == source_profile[
        "source_matrix_metadata_hash"
    ]
    assert schedule["pattern_class"] == "support_overlap_rref_pivot"
    assert schedule["route_cut_status"] == "ROUTE_CUT_CERTIFIED_CANDIDATE"
    assert schedule["schedule_classification"] == "RREF_DERIVED_PATTERN"
    assert schedule["status"] == "CERTIFIED_RREF_DERIVED"

    assert matrix_rows > matrix_cols > 0
    assert pivot["schedule_origin"] == "RREF_DERIVED_PATTERN"
    assert pivot["schedule_status"] == "CERTIFIED_RREF_DERIVED"
    assert pivot["covered_columns"] == matrix_cols
    assert pivot["pivot_rows_used"] == matrix_cols
    assert pivot["pivot_columns_used"] == matrix_cols
    assert pivot["rref_private_pivot_count"] == matrix_cols
    assert pivot["combinatorial_private_pivot_count"] is None
    assert pivot["support_overlap_pivot_count"] == matrix_cols
    assert pivot["support_overlap_pivot_fraction"] == "1"
    assert pivot["block_triangular_order_exists"] is False
    assert pivot["block_triangular_order_status"] == "NOT_PROVED"
    assert pivot["deterministic_combinatorial_schedule"] is False
    assert pivot["row_type_counts"] == {"support_overlap_row": matrix_cols}
    assert pivot["row_type_signature"] == f"support_overlap_row:{matrix_cols}"
    assert pivot["pair_profile"]["pair_pivot_total"] == matrix_cols
    assert sum(pivot["pair_pivot_counts"].values()) == matrix_cols

    for key in ["pivot_rows_hash", "pivot_cols_hash", "pivot_pairs_hash", "minor_hash"]:
        assert len(pivot[key]) == 64
        assert pivot[key] == source_pivot[key]
    assert pivot["pair_pivot_counts"] == source_pivot["pair_pivot_counts"]
    assert pivot["pair_profile"] == source_pivot["pair_profile"]
    assert pivot["row_type_counts"] == source_pivot["row_type_counts"]


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
    assert record["construction_mode"] == "support_overlap_pivot_schedule"

    source_profiles = source_support_profiles(source)
    schedules = record["matrix_schedules"]
    assert len(source_profiles) == 20
    assert len(schedules) == 20
    assert set(source_profiles) == {item["source_key"] for item in schedules}
    for schedule in schedules:
        validate_schedule(schedule, source_profiles[schedule["source_key"]])

    summary = record["schedule_summary"]
    assert summary == {
        "support_overlap_matrices": 20,
        "source_packet_counts": EXPECTED_SOURCE_PACKET_COUNTS,
        "compressed_variable_range": [19, 159],
        "all_pivots_support_overlap": True,
        "all_schedules_rref_derived": True,
        "deterministic_combinatorial_schedule_found": False,
        "block_triangular_order_proved": False,
        "route_cut_certified_candidates": 20,
        "aggregate_pair_pivot_counts": EXPECTED_PAIR_COUNTS,
        "status": "RREF_DERIVED_PATTERN",
    }
    assert summary["source_packet_counts"] == aggregate_by(schedules, "source_packet")
    assert summary["aggregate_pair_pivot_counts"] == aggregate_pairs(schedules)

    assert record["source_profile"] == {
        "path": str(SOURCE_DATA),
        "record_hash": source["record_hash"],
        "source_matrices": 34,
        "support_overlap_profiles": 20,
        "status": "CANDIDATE_THEOREM_ONLY",
    }
    assert record["theorem_assessment"] == {
        "target_statement": (
            "For every reduced matrix in the support_overlap_rref_pivot class, "
            "a deterministic support-overlap schedule selects a full "
            "column-rank minor over GF(17^32)."
        ),
        "tested_rows_support_rref_schedule": True,
        "deterministic_schedule_proved": False,
        "reason_not_proved": (
            "The certified schedules are extracted from Sage RREF pivot rows; "
            "no rank-free combinatorial row-ordering rule has been verified "
            "for the class."
        ),
        "status": "RREF_DERIVED_PATTERN_ONLY",
    }
    assert record["interpretation"] == {
        "a327_certificate_found": False,
        "candidate_found": False,
        "global_Lambda_mu_327_upper_bound": False,
        "support_overlap_candidates_certified_full_rank": True,
        "deterministic_pivot_schedule_theorem_proved": False,
        "status": "AUDIT",
    }
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "RREF_DERIVED_PATTERN_ONLY",
    }
    assert record["repo_claim"]["mca_counted"] is False
    assert set(record["repo_claim"]["not_claimed"]) == REQUIRED_NONCLAIMS

    expected_hash = hash_payload(
        {
            "source_profile": record["source_profile"],
            "schedule_summary": record["schedule_summary"],
            "matrix_schedules": record["matrix_schedules"],
            "theorem_assessment": record["theorem_assessment"],
            "interpretation": record["interpretation"],
            "global": record["global_status"],
        }
    )
    assert record["record_hash"] == expected_hash
    return {
        "support_overlap_matrices": len(schedules),
        "route_cut_certified_candidates": summary["route_cut_certified_candidates"],
        "deterministic_schedule_proved": record["theorem_assessment"][
            "deterministic_schedule_proved"
        ],
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
        print("M1_SUPPORT_OVERLAP_PIVOT_SCHEDULE_VERIFY_OK")
        print(f"support-overlap matrices: {summary['support_overlap_matrices']}")
        print(
            "route-cut certified candidates: "
            f"{summary['route_cut_certified_candidates']}"
        )
        print(
            "deterministic schedule proved: "
            f"{summary['deterministic_schedule_proved']}"
        )
        print(f"status: {summary['status']}")


if __name__ == "__main__":
    main()
