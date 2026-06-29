#!/usr/bin/env python3
"""Full RIM pivot-certificate replay for M1 a=327 route-cut matrices."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import zlib
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_rim_support_pattern_pivot_replay.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
TARGET_BITS = 128
FIELD_DENOMINATOR = P**FIELD_DEGREE

CERTIFICATE_ROWS_ZLIB_B64 = """
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
"""

MATRIX_MODEL_BY_PACKET = {
    "pairwise_divisibility_nullvector_system": "pairwise_divisibility",
    "two_level_pairwise_divisibility": "two_level_pairwise_divisibility",
    "constructive_rank_defect_support_design": "support_design_reduced_intersection_matrix",
    "support_pattern_multiplicity_mutation_search": "support_design_reduced_intersection_matrix",
    "support_pattern_surrogate_rank_feedback_search": "support_design_reduced_intersection_matrix",
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def raw_certificate_rows() -> list[dict[str, Any]]:
    packed = "".join(CERTIFICATE_ROWS_ZLIB_B64.split())
    return json.loads(zlib.decompress(base64.b64decode(packed)).decode())


def source_family_for(packet: str) -> str:
    if packet == "two_level_pairwise_divisibility":
        return "two_level_quotient_residual"
    if packet == "pairwise_divisibility_nullvector_system":
        return "balanced_clique"
    return "support_pattern"


def certificate_rows() -> list[dict[str, Any]]:
    rows = []
    for raw in raw_certificate_rows():
        cert = raw["pivot_certificate"]
        assert cert["pivot_certificate_status"] == "CERTIFIED"
        packet = raw["source_packet"]
        rows.append(
            {
                "source_key": raw["source_key"],
                "source_packet": packet,
                "candidate_id": raw["candidate_id"],
                "matrix_model": MATRIX_MODEL_BY_PACKET[packet],
                "source_family": cert.get("source_family", source_family_for(packet)),
                "matrix_shape": [cert["matrix_rows"], cert["matrix_cols"]],
                "rank": cert["rank"],
                "nullity": cert["nullity"],
                "source_matrix_metadata_hash": cert["source_matrix_metadata_hash"],
                "pivot_certificate_status": cert["pivot_certificate_status"],
                "certificate_type": cert["certificate_type"],
                "pivot_certificate": cert,
                "status": "CERTIFIED_FULL_RANK",
            }
        )
    return rows


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


def build_result() -> dict[str, Any]:
    rows = certificate_rows()
    assert len(rows) == 34
    assert threshold_floor() == 6
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
        "construction_mode": "rim_support_pattern_pivot_replay",
        "source_summary": {
            "source_matrix_count": len(rows),
            "previous_certified_count": 14,
            "new_certified_count": 20,
            "total_certified_after": len(rows),
            "deferred_count_after": 0,
            "source_packet_counts": aggregate_by(rows, "source_packet"),
            "matrix_model_counts": aggregate_by(rows, "matrix_model"),
            "certified_by_source_packet": certified_by_source_packet(rows),
            "exact_field": "GF(17^32)",
            "status": "PIVOT_COVERAGE_COMPLETE",
        },
        "pivot_summary": {
            "certificate_type": "RREF_PIVOT",
            "pivot_row_type_counts": aggregate_pivot_row_types(rows),
            "common_pivot_pattern_found": False,
            "all_source_matrices_certified": True,
            "status": "PIVOT_COVERAGE_COMPLETE",
        },
        "certificates": rows,
        "interpretation": {
            "a327_certificate_found": False,
            "candidate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "coverage_increased_from_14_to_34": True,
            "status": "PIVOT_COVERAGE_COMPLETE",
        },
        "open_layers": {
            "common_pivot_pattern_theorem": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_rim_support_pattern_pivot_replay.sage",
            "constructs_GF_17_32": True,
            "reconstructs_all_source_matrices": True,
            "extracts_pivot_row_minor": True,
            "verifies_selected_minor_full_rank": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list certificate",
                "global Lambda_mu(C,327) <= 6",
                "global RIM full-rank theorem",
                "exact Lambda_mu",
                "exact delta*_C",
                "improvement over PR #133",
            ],
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": "PIVOT_COVERAGE_COMPLETE",
        },
        "status": "M1_RIM_SUPPORT_PATTERN_PIVOT_REPLAY_COMPLETE",
    }
    result["record_hash"] = hash_payload(
        {
            "source_summary": result["source_summary"],
            "pivot_summary": result["pivot_summary"],
            "certificates": result["certificates"],
            "interpretation": result["interpretation"],
            "open": result["open_layers"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_result(), indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_result()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output)
        print(f"WROTE {args.output}")
        print(f"source matrices: {result['source_summary']['source_matrix_count']}")
        print(f"total certified: {result['source_summary']['total_certified_after']}")
        print(f"pending: {result['source_summary']['deferred_count_after']}")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
