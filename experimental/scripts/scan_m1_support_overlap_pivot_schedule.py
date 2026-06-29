#!/usr/bin/env python3
"""Extract the support-overlap pivot-schedule layer from M1 RIM profiles."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")
OUTPUT_DATA = Path("experimental/data/m1_support_overlap_pivot_schedule.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
TARGET_BITS = 128
FIELD_DENOMINATOR = P**FIELD_DEGREE

REQUIRED_NONCLAIMS = [
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
]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


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


def matrix_schedule(profile: dict[str, Any]) -> dict[str, Any]:
    pivot = profile["pivot_pattern"]
    cols = profile["compressed_variables"]
    assert profile["classification"] == "support_overlap_rref_pivot"
    assert pivot["support_overlap_schedule"] is True
    assert pivot["category_counts"]["support_overlap_pivots"] == cols
    return {
        "candidate_id": profile["candidate_id"],
        "source_key": profile["source_key"],
        "source_packet": profile["source_packet"],
        "source_family": profile["source_family"],
        "matrix_model": profile["matrix_model"],
        "matrix_shape": profile["matrix_shape"],
        "rank": profile["rank"],
        "nullity": profile["nullity"],
        "source_matrix_metadata_hash": profile["source_matrix_metadata_hash"],
        "pattern_class": "support_overlap_rref_pivot",
        "pivot_schedule": {
            "schedule_origin": "RREF_DERIVED_PATTERN",
            "schedule_status": "CERTIFIED_RREF_DERIVED",
            "covered_columns": cols,
            "pivot_rows_used": cols,
            "pivot_columns_used": cols,
            "rref_private_pivot_count": cols,
            "combinatorial_private_pivot_count": None,
            "support_overlap_pivot_count": cols,
            "support_overlap_pivot_fraction": "1",
            "block_triangular_order_exists": False,
            "block_triangular_order_status": "NOT_PROVED",
            "deterministic_combinatorial_schedule": False,
            "pivot_rows_hash": pivot["pivot_rows_hash"],
            "pivot_cols_hash": pivot["pivot_cols_hash"],
            "pivot_pairs_hash": pivot["pivot_pairs_hash"],
            "minor_hash": pivot["minor_hash"],
            "pair_pivot_counts": pivot["pair_pivot_counts"],
            "pair_profile": pivot["pair_profile"],
            "row_type_counts": pivot["row_type_counts"],
            "row_type_signature": pivot["row_type_signature"],
        },
        "route_cut_status": "ROUTE_CUT_CERTIFIED_CANDIDATE",
        "schedule_classification": "RREF_DERIVED_PATTERN",
        "status": "CERTIFIED_RREF_DERIVED",
    }


def build_result(source: dict[str, Any]) -> dict[str, Any]:
    assert threshold_floor() == 6
    assert source["status"] == "M1_RIM_PIVOT_PATTERN_THEOREM_AUDIT"
    assert source["theorem_status"]["support_overlap_schedule_candidate"] is True
    profiles = [
        profile
        for profile in source["matrix_profiles"]
        if profile["classification"] == "support_overlap_rref_pivot"
    ]
    profiles.sort(key=lambda item: (item["compressed_variables"], item["candidate_id"]))
    schedules = [matrix_schedule(profile) for profile in profiles]
    assert len(schedules) == 20
    source_packets = aggregate_by(schedules, "source_packet")
    pair_counts = aggregate_pairs(schedules)
    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "denominator": "17^32",
        "field_denominator": str(FIELD_DENOMINATOR),
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "support_overlap_pivot_schedule",
        "source_profile": {
            "path": str(SOURCE_DATA),
            "record_hash": source["record_hash"],
            "source_matrices": source["profile_summary"]["source_matrices"],
            "support_overlap_profiles": len(schedules),
            "status": source["global_status"]["status"],
        },
        "schedule_summary": {
            "support_overlap_matrices": len(schedules),
            "source_packet_counts": source_packets,
            "compressed_variable_range": [
                min(item["matrix_shape"][1] for item in schedules),
                max(item["matrix_shape"][1] for item in schedules),
            ],
            "all_pivots_support_overlap": True,
            "all_schedules_rref_derived": True,
            "deterministic_combinatorial_schedule_found": False,
            "block_triangular_order_proved": False,
            "route_cut_certified_candidates": len(schedules),
            "aggregate_pair_pivot_counts": pair_counts,
            "status": "RREF_DERIVED_PATTERN",
        },
        "matrix_schedules": schedules,
        "theorem_assessment": {
            "target_statement": (
                "For every reduced matrix in the support_overlap_rref_pivot "
                "class, a deterministic support-overlap schedule selects a "
                "full column-rank minor over GF(17^32)."
            ),
            "tested_rows_support_rref_schedule": True,
            "deterministic_schedule_proved": False,
            "reason_not_proved": (
                "The certified schedules are extracted from Sage RREF pivot "
                "rows; no rank-free combinatorial row-ordering rule has been "
                "verified for the class."
            ),
            "status": "RREF_DERIVED_PATTERN_ONLY",
        },
        "interpretation": {
            "a327_certificate_found": False,
            "candidate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "support_overlap_candidates_certified_full_rank": True,
            "deterministic_pivot_schedule_theorem_proved": False,
            "status": "AUDIT",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_support_overlap_pivot_schedule.sage",
            "checks_GF_17_32": True,
            "reconstructs_20_support_matrices": True,
            "recomputes_rref_schedule_hashes": True,
            "verifies_selected_minors_full_rank": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": REQUIRED_NONCLAIMS,
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": "RREF_DERIVED_PATTERN_ONLY",
        },
        "status": "M1_SUPPORT_OVERLAP_PIVOT_SCHEDULE_AUDIT",
    }
    result["record_hash"] = hash_payload(
        {
            "source_profile": result["source_profile"],
            "schedule_summary": result["schedule_summary"],
            "matrix_schedules": result["matrix_schedules"],
            "theorem_assessment": result["theorem_assessment"],
            "interpretation": result["interpretation"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE_DATA, type=Path)
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_result(load_json(args.source))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output, result)
        print(f"WROTE {args.output}")
        print(
            "support-overlap matrices: "
            f"{result['schedule_summary']['support_overlap_matrices']}"
        )
        print(
            "deterministic schedule proved: "
            f"{result['theorem_assessment']['deterministic_schedule_proved']}"
        )
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
