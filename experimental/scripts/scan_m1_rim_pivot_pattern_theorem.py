#!/usr/bin/env python3
"""Mine pivot-pattern profiles from the 34 certified M1 a=327 RIM matrices."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_rim_support_pattern_pivot_replay.json")
OUTPUT_DATA = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
TARGET_BITS = 128
FIELD_DENOMINATOR = P**FIELD_DEGREE

PATTERN_BY_SOURCE_FAMILY = {
    "balanced_clique": "generic_pairwise_rref_pivot",
    "support_pattern": "support_overlap_rref_pivot",
    "two_level_quotient_residual": "quotient_residual_rref_pivot",
}

REQUIRED_NONCLAIMS = [
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


def pivot_category_counts(cert: dict[str, Any]) -> dict[str, int]:
    rows = cert["pivot_row_type_counts"]
    return {
        "generic_pairwise_pivots": rows.get("balanced_or_generic_pairwise_row", 0),
        "quotient_fiber_pivots": rows.get("quotient_full_fiber_row", 0),
        "residual_pivots": rows.get("residual_or_partial_fiber_row", 0),
        "support_overlap_pivots": rows.get("support_overlap_row", 0),
    }


def pair_profile(pair_counts: dict[str, int]) -> dict[str, Any]:
    values = list(pair_counts.values())
    if not values:
        return {
            "active_pairs": 0,
            "max_pair_pivots": 0,
            "min_pair_pivots": 0,
            "pair_pivot_total": 0,
            "dominant_pair": None,
        }
    dominant_pair = max(pair_counts.items(), key=lambda item: (item[1], item[0]))[0]
    return {
        "active_pairs": len(values),
        "max_pair_pivots": max(values),
        "min_pair_pivots": min(values),
        "pair_pivot_total": sum(values),
        "dominant_pair": dominant_pair,
    }


def matrix_profile(row: dict[str, Any]) -> dict[str, Any]:
    cert = row["pivot_certificate"]
    matrix_rows, matrix_cols = row["matrix_shape"]
    category_counts = pivot_category_counts(cert)
    row_type_signature = ";".join(
        f"{key}:{value}" for key, value in sorted(cert["pivot_row_type_counts"].items())
    )
    pattern_id = PATTERN_BY_SOURCE_FAMILY[row["source_family"]]
    structural_family = {
        "generic_pairwise_rref_pivot": "balanced_or_generic_pairwise_rows_only",
        "support_overlap_rref_pivot": "support_overlap_rows_only",
        "quotient_residual_rref_pivot": "quotient_fiber_plus_residual_rows",
    }[pattern_id]
    row_type_total = sum(cert["pivot_row_type_counts"].values())
    pair_counts = cert["pivot_pair_counts"]
    return {
        "candidate_id": row["candidate_id"],
        "source_key": row["source_key"],
        "source_packet": row["source_packet"],
        "source_family": row["source_family"],
        "matrix_model": row["matrix_model"],
        "matrix_shape": row["matrix_shape"],
        "compressed_variables": matrix_cols,
        "rank": row["rank"],
        "nullity": row["nullity"],
        "pivot_certificate_status": row["pivot_certificate_status"],
        "certificate_type": row["certificate_type"],
        "pivot_pattern": {
            "pattern_id": pattern_id,
            "structural_family": structural_family,
            "rref_pivot_blocks": matrix_cols,
            "private_pivot_blocks": matrix_cols,
            "pivot_rows_used": matrix_cols,
            "pivot_columns_used": matrix_cols,
            "row_type_total": row_type_total,
            "row_type_signature": row_type_signature,
            "row_type_counts": cert["pivot_row_type_counts"],
            "category_counts": category_counts,
            "pair_profile": pair_profile(pair_counts),
            "pair_pivot_counts": pair_counts,
            "single_row_type_schedule": len(cert["pivot_row_type_counts"]) == 1,
            "support_overlap_schedule": (
                category_counts["support_overlap_pivots"] == matrix_cols
            ),
            "generic_pairwise_schedule": (
                category_counts["generic_pairwise_pivots"] == matrix_cols
            ),
            "quotient_residual_schedule": (
                category_counts["quotient_fiber_pivots"]
                + category_counts["residual_pivots"]
                == matrix_cols
            ),
            "block_triangular_order_exists": False,
            "block_triangular_order_status": "NOT_PROVED",
            "pivot_rows_hash": cert["pivot_rows_hash"],
            "pivot_cols_hash": cert["pivot_cols_hash"],
            "pivot_pairs_hash": cert["pivot_pairs_hash"],
            "minor_hash": hash_payload(
                {
                    "pivot_rows_hash": cert["pivot_rows_hash"],
                    "pivot_cols_hash": cert["pivot_cols_hash"],
                    "pivot_pairs_hash": cert["pivot_pairs_hash"],
                    "source_matrix_metadata_hash": cert[
                        "source_matrix_metadata_hash"
                    ],
                }
            ),
        },
        "classification": pattern_id,
        "source_matrix_metadata_hash": row["source_matrix_metadata_hash"],
        "status": "PATTERN_PROFILED",
    }


def pattern_summaries(profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    all_families = sorted({profile["source_family"] for profile in profiles})
    for pattern_id in sorted({p["classification"] for p in profiles}):
        covered = [p for p in profiles if p["classification"] == pattern_id]
        families = sorted({p["source_family"] for p in covered})
        source_packets = sorted({p["source_packet"] for p in covered})
        row_type_counts: dict[str, int] = {}
        pair_counts: dict[str, int] = {}
        for profile in covered:
            add_counts(row_type_counts, profile["pivot_pattern"]["row_type_counts"])
            add_counts(pair_counts, profile["pivot_pattern"]["pair_pivot_counts"])
        out.append(
            {
                "pattern_id": pattern_id,
                "covered_count": len(covered),
                "families_covered": families,
                "source_packets_covered": source_packets,
                "uncovered_count": len(profiles) - len(covered),
                "global_coverage": families == all_families,
                "compressed_variable_range": [
                    min(p["compressed_variables"] for p in covered),
                    max(p["compressed_variables"] for p in covered),
                ],
                "aggregate_row_type_counts": dict(sorted(row_type_counts.items())),
                "aggregate_pair_pivot_counts": dict(sorted(pair_counts.items())),
                "candidate_theorem": {
                    "statement": candidate_statement(pattern_id),
                    "status": "CANDIDATE_THEOREM",
                    "proved": False,
                },
                "status": "CANDIDATE_PATTERN",
            }
        )
    out.append(
        {
            "pattern_id": "rref_pivot_minor_certificate",
            "covered_count": len(profiles),
            "families_covered": all_families,
            "source_packets_covered": sorted({p["source_packet"] for p in profiles}),
            "uncovered_count": 0,
            "global_coverage": True,
            "compressed_variable_range": [
                min(p["compressed_variables"] for p in profiles),
                max(p["compressed_variables"] for p in profiles),
            ],
            "aggregate_row_type_counts": aggregate_row_types(profiles),
            "aggregate_pair_pivot_counts": aggregate_pairs(profiles),
            "candidate_theorem": {
                "statement": (
                    "Each tested matrix has an explicit Sage-replayed RREF "
                    "pivot-minor certificate over GF(17^32)."
                ),
                "status": "COMPUTATIONAL_CERTIFICATE",
                "proved": True,
            },
            "status": "CERTIFICATE_PATTERN",
        }
    )
    return out


def candidate_statement(pattern_id: str) -> str:
    if pattern_id == "support_overlap_rref_pivot":
        return (
            "For the tested support-pattern RIM rows, the RREF pivot schedule "
            "uses support-overlap rows to cover every compressed variable."
        )
    if pattern_id == "generic_pairwise_rref_pivot":
        return (
            "For the tested balanced-clique pairwise rows, generic pairwise "
            "rows provide one RREF pivot for every compressed variable."
        )
    if pattern_id == "quotient_residual_rref_pivot":
        return (
            "For the tested two-level quotient-residual rows, quotient-fiber "
            "and residual rows jointly provide one RREF pivot for every "
            "compressed variable."
        )
    return "No candidate statement recorded."


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


def build_result(source: dict[str, Any]) -> dict[str, Any]:
    assert threshold_floor() == 6
    assert source["status"] == "M1_RIM_SUPPORT_PATTERN_PIVOT_REPLAY_COMPLETE"
    assert source["source_summary"]["total_certified_after"] == 34
    rows = source["certificates"]
    profiles = [matrix_profile(row) for row in rows]
    profiles.sort(key=lambda item: (item["source_packet"], item["compressed_variables"], item["candidate_id"]))
    patterns = pattern_summaries(profiles)
    support_profiles = [p for p in profiles if p["source_family"] == "support_pattern"]
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
        "construction_mode": "rim_pivot_pattern_theorem_audit",
        "source_replay": {
            "path": str(SOURCE_DATA),
            "record_hash": source["record_hash"],
            "source_matrices": source["source_summary"]["source_matrix_count"],
            "pivot_covered": source["source_summary"]["total_certified_after"],
            "status": source["source_summary"]["status"],
        },
        "profile_summary": {
            "source_matrices": len(profiles),
            "pivot_covered": len(profiles),
            "source_family_counts": aggregate_by(profiles, "source_family"),
            "source_packet_counts": aggregate_by(profiles, "source_packet"),
            "matrix_model_counts": aggregate_by(profiles, "matrix_model"),
            "aggregate_row_type_counts": aggregate_row_types(profiles),
            "aggregate_pair_pivot_counts": aggregate_pairs(profiles),
            "support_pattern_rows": len(support_profiles),
            "support_pattern_all_support_overlap": all(
                p["pivot_pattern"]["support_overlap_schedule"]
                for p in support_profiles
            ),
            "global_common_structural_pattern_found": False,
            "global_certificate_pattern_found": True,
            "status": "PIVOT_PROFILED",
        },
        "common_pattern_candidates": patterns,
        "matrix_profiles": profiles,
        "theorem_status": {
            "candidate_theorem_count": len(
                [p for p in patterns if p["status"] == "CANDIDATE_PATTERN"]
            ),
            "proved_theorem_count": 0,
            "common_pivot_pattern_theorem_proved": False,
            "support_overlap_schedule_candidate": True,
            "status": "CANDIDATE_THEOREM_ONLY",
        },
        "interpretation": {
            "a327_certificate_found": False,
            "candidate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "pivot_profiles_mined": True,
            "common_pivot_pattern_theorem_proved": False,
            "status": "AUDIT",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_rim_pivot_pattern_theorem.sage",
            "checks_source_replay_hash": True,
            "checks_profile_derivation": True,
            "reuses_existing_pivot_certificates": True,
            "recomputes_expensive_rank_gates": False,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": REQUIRED_NONCLAIMS,
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": "CANDIDATE_THEOREM_ONLY",
        },
        "status": "M1_RIM_PIVOT_PATTERN_THEOREM_AUDIT",
    }
    result["record_hash"] = hash_payload(
        {
            "source_replay": result["source_replay"],
            "profile_summary": result["profile_summary"],
            "common_pattern_candidates": result["common_pattern_candidates"],
            "matrix_profiles": result["matrix_profiles"],
            "theorem_status": result["theorem_status"],
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

    source = load_json(args.source)
    result = build_result(source)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output, result)
        print(f"WROTE {args.output}")
        print(f"source matrices: {result['profile_summary']['source_matrices']}")
        print(
            "pattern candidates: "
            f"{result['theorem_status']['candidate_theorem_count']}"
        )
        print(
            "global theorem proved: "
            f"{result['theorem_status']['common_pivot_pattern_theorem_proved']}"
        )
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
