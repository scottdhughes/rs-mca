#!/usr/bin/env python3
"""Aggregate RIM pivot certificates for M1 a=327 route-cut matrices."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_quotient_residual_rim_pivot_certificates.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
TARGET_BITS = 128
FIELD_DENOMINATOR = P**FIELD_DEGREE

SOURCE_PACKETS = [
    {
        "packet": "pairwise_divisibility_nullvector_system",
        "path": Path("experimental/data/m1_a327_pairwise_divisibility_nullvector_system.json"),
        "matrix_model": "pairwise_divisibility",
    },
    {
        "packet": "two_level_pairwise_divisibility",
        "path": Path("experimental/data/m1_a327_two_level_pairwise_divisibility.json"),
        "matrix_model": "two_level_pairwise_divisibility",
    },
    {
        "packet": "constructive_rank_defect_support_design",
        "path": Path("experimental/data/m1_constructive_rank_defect_support_design.json"),
        "matrix_model": "support_design_reduced_intersection_matrix",
    },
    {
        "packet": "support_pattern_multiplicity_mutation_search",
        "path": Path("experimental/data/m1_support_pattern_multiplicity_mutation_search.json"),
        "matrix_model": "support_design_reduced_intersection_matrix",
    },
    {
        "packet": "support_pattern_surrogate_rank_feedback_search",
        "path": Path("experimental/data/m1_support_pattern_surrogate_rank_feedback_search.json"),
        "matrix_model": "support_design_reduced_intersection_matrix",
    },
]


# Filled from the Sage audit after source candidate identities are fixed.
PRECOMPUTED_PIVOT_CERTIFICATES: dict[str, dict[str, Any]] = {
    "two_level_pairwise_divisibility::common_six_fiber_residual_11": {
        "certificate_type": "RREF_PIVOT_MINOR",
        "minor_size": 6,
        "matrix_rows": 3825,
        "matrix_cols": 6,
        "rank": 6,
        "nullity": 0,
        "pivot_rows_hash": "0ccd87610e937eeb211aa990e4ed406b6dfd3c6b86d2f2454e007b9d1e448341",
        "pivot_cols_hash": "4e098021cf9ec15699efd082b803811ec67394af4b3ea324e86edbccc3cbeac3",
        "pivot_pairs_hash": "b9feeb7c7988405c37e927a5e7685c70754f7b7bf155c7d1b3d981d69909eef0",
        "pivot_row_type_counts": {"quotient_full_fiber_row": 1, "residual_or_partial_fiber_row": 5},
        "pivot_pair_counts": {"1,2": 2, "1,3": 1, "1,4": 1, "1,5": 1, "1,6": 1},
        "minor_rank": 6,
        "minor_rank_full": True,
        "minor_det_nonzero": True,
        "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1},
        "remaining_equations_by_pair": {
            "1,2": 255,
            "1,3": 255,
            "1,4": 255,
            "1,5": 255,
            "1,6": 255,
            "2,3": 255,
            "2,4": 255,
            "2,5": 255,
            "2,6": 255,
            "3,4": 255,
            "3,5": 255,
            "3,6": 255,
            "4,5": 255,
            "4,6": 255,
            "5,6": 255,
        },
        "source_matrix_metadata_hash": "9056354fcd9961ae40caff6fed0b2a31e185d392c4675627032972d0a0d89218",
        "status": "CERTIFIED_FULL_RANK",
    },
    "two_level_pairwise_divisibility::common_six_fiber_residual_10": {
        "certificate_type": "RREF_PIVOT_MINOR",
        "minor_size": 6,
        "matrix_rows": 3825,
        "matrix_cols": 6,
        "rank": 6,
        "nullity": 0,
        "pivot_rows_hash": "f396b70fb65886f54a5e2262918bddc58bb510d6b5d6b1e5a3cd101caf1d6da1",
        "pivot_cols_hash": "4e098021cf9ec15699efd082b803811ec67394af4b3ea324e86edbccc3cbeac3",
        "pivot_pairs_hash": "b9feeb7c7988405c37e927a5e7685c70754f7b7bf155c7d1b3d981d69909eef0",
        "pivot_row_type_counts": {"quotient_full_fiber_row": 1, "residual_or_partial_fiber_row": 5},
        "pivot_pair_counts": {"1,2": 2, "1,3": 1, "1,4": 1, "1,5": 1, "1,6": 1},
        "minor_rank": 6,
        "minor_rank_full": True,
        "minor_det_nonzero": True,
        "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1},
        "remaining_equations_by_pair": {
            "1,2": 255,
            "1,3": 255,
            "1,4": 255,
            "1,5": 255,
            "1,6": 255,
            "2,3": 255,
            "2,4": 255,
            "2,5": 255,
            "2,6": 255,
            "3,4": 255,
            "3,5": 255,
            "3,6": 255,
            "4,5": 255,
            "4,6": 255,
            "5,6": 255,
        },
        "source_matrix_metadata_hash": "81b914bb7bb33740bd367cbd9dd4510c204ff84c60040ef8f4486cfa57acf7a1",
        "status": "CERTIFIED_FULL_RANK",
    },
    "two_level_pairwise_divisibility::punctured_eight_fiber_11": {
        "certificate_type": "RREF_PIVOT_MINOR",
        "minor_size": 6,
        "matrix_rows": 3825,
        "matrix_cols": 6,
        "rank": 6,
        "nullity": 0,
        "pivot_rows_hash": "b467614b919254a1fed4c7fa757955aa2317ebd4d588dfe78014dd35f9d96bdc",
        "pivot_cols_hash": "4e098021cf9ec15699efd082b803811ec67394af4b3ea324e86edbccc3cbeac3",
        "pivot_pairs_hash": "b9feeb7c7988405c37e927a5e7685c70754f7b7bf155c7d1b3d981d69909eef0",
        "pivot_row_type_counts": {"quotient_full_fiber_row": 5, "residual_or_partial_fiber_row": 1},
        "pivot_pair_counts": {"1,2": 2, "1,3": 1, "1,4": 1, "1,5": 1, "1,6": 1},
        "minor_rank": 6,
        "minor_rank_full": True,
        "minor_det_nonzero": True,
        "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1},
        "remaining_equations_by_pair": {
            "1,2": 255,
            "1,3": 255,
            "1,4": 255,
            "1,5": 255,
            "1,6": 255,
            "2,3": 255,
            "2,4": 255,
            "2,5": 255,
            "2,6": 255,
            "3,4": 255,
            "3,5": 255,
            "3,6": 255,
            "4,5": 255,
            "4,6": 255,
            "5,6": 255,
        },
        "source_matrix_metadata_hash": "9c3fc8c7fae3f8e4c4c80ef0e4d4cf7d69ba1045e32e3ab127b8a11d13b5045b",
        "status": "CERTIFIED_FULL_RANK",
    },
    "two_level_pairwise_divisibility::punctured_eight_fiber_10": {
        "certificate_type": "RREF_PIVOT_MINOR",
        "minor_size": 6,
        "matrix_rows": 3825,
        "matrix_cols": 6,
        "rank": 6,
        "nullity": 0,
        "pivot_rows_hash": "8d6e092d43f0c07a5409348979bc03bb1b7bd310dc41ffae7b61b101e2438ba5",
        "pivot_cols_hash": "4e098021cf9ec15699efd082b803811ec67394af4b3ea324e86edbccc3cbeac3",
        "pivot_pairs_hash": "b9feeb7c7988405c37e927a5e7685c70754f7b7bf155c7d1b3d981d69909eef0",
        "pivot_row_type_counts": {"quotient_full_fiber_row": 5, "residual_or_partial_fiber_row": 1},
        "pivot_pair_counts": {"1,2": 2, "1,3": 1, "1,4": 1, "1,5": 1, "1,6": 1},
        "minor_rank": 6,
        "minor_rank_full": True,
        "minor_det_nonzero": True,
        "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1},
        "remaining_equations_by_pair": {
            "1,2": 255,
            "1,3": 255,
            "1,4": 255,
            "1,5": 255,
            "1,6": 255,
            "2,3": 255,
            "2,4": 255,
            "2,5": 255,
            "2,6": 255,
            "3,4": 255,
            "3,5": 255,
            "3,6": 255,
            "4,5": 255,
            "4,6": 255,
            "5,6": 255,
        },
        "source_matrix_metadata_hash": "2aebca19e0802ca2b313fe38314a2dd5ba6afbc031c3047324879df732812f87",
        "status": "CERTIFIED_FULL_RANK",
    },
    "two_level_pairwise_divisibility::seven_fibers_plus_residual_11": {
        "certificate_type": "RREF_PIVOT_MINOR",
        "minor_size": 6,
        "matrix_rows": 3825,
        "matrix_cols": 6,
        "rank": 6,
        "nullity": 0,
        "pivot_rows_hash": "8c22c7baabb9c6d5688bf3d6b053efe86b614799d88995ff29977caa3f8f2bad",
        "pivot_cols_hash": "4e098021cf9ec15699efd082b803811ec67394af4b3ea324e86edbccc3cbeac3",
        "pivot_pairs_hash": "b9feeb7c7988405c37e927a5e7685c70754f7b7bf155c7d1b3d981d69909eef0",
        "pivot_row_type_counts": {"quotient_full_fiber_row": 6},
        "pivot_pair_counts": {"1,2": 2, "1,3": 1, "1,4": 1, "1,5": 1, "1,6": 1},
        "minor_rank": 6,
        "minor_rank_full": True,
        "minor_det_nonzero": True,
        "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1},
        "remaining_equations_by_pair": {
            "1,2": 255,
            "1,3": 255,
            "1,4": 255,
            "1,5": 255,
            "1,6": 255,
            "2,3": 255,
            "2,4": 255,
            "2,5": 255,
            "2,6": 255,
            "3,4": 255,
            "3,5": 255,
            "3,6": 255,
            "4,5": 255,
            "4,6": 255,
            "5,6": 255,
        },
        "source_matrix_metadata_hash": "f9db6b1f9cf69186af308a2ece43f58cbbd43678e48e6851c8be14731df47652",
        "status": "CERTIFIED_FULL_RANK",
    },
    "two_level_pairwise_divisibility::seven_fibers_plus_residual_10": {
        "certificate_type": "RREF_PIVOT_MINOR",
        "minor_size": 6,
        "matrix_rows": 3825,
        "matrix_cols": 6,
        "rank": 6,
        "nullity": 0,
        "pivot_rows_hash": "62d246c9b94e5e6a0e51ba46a69ef7282c86d57a7dfd1fb21733904ea6128e52",
        "pivot_cols_hash": "4e098021cf9ec15699efd082b803811ec67394af4b3ea324e86edbccc3cbeac3",
        "pivot_pairs_hash": "b9feeb7c7988405c37e927a5e7685c70754f7b7bf155c7d1b3d981d69909eef0",
        "pivot_row_type_counts": {"quotient_full_fiber_row": 6},
        "pivot_pair_counts": {"1,2": 2, "1,3": 1, "1,4": 1, "1,5": 1, "1,6": 1},
        "minor_rank": 6,
        "minor_rank_full": True,
        "minor_det_nonzero": True,
        "compressed_dimensions_by_witness": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1, "6": 1},
        "remaining_equations_by_pair": {
            "1,2": 255,
            "1,3": 255,
            "1,4": 255,
            "1,5": 255,
            "1,6": 255,
            "2,3": 255,
            "2,4": 255,
            "2,5": 255,
            "2,6": 255,
            "3,4": 255,
            "3,5": 255,
            "3,6": 255,
            "4,5": 255,
            "4,6": 255,
            "5,6": 255,
        },
        "source_matrix_metadata_hash": "70ccf4ba113e0bcde2ac9b7ad41bae470792d27f319fd5b8eca93938bb99abef",
        "status": "CERTIFIED_FULL_RANK",
    },
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def source_candidates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCE_PACKETS:
        data = json.loads(source["path"].read_text())
        candidates = data.get("candidates", data.get("retained_candidates", []))
        for row in candidates:
            exact = row.get("sage_exact_rank") or row.get("exact_rank_gate")
            if exact is None:
                continue
            if exact.get("field_label") != "GF(17^32)":
                continue
            if exact.get("rank") != exact.get("compressed_variables"):
                continue
            if exact.get("nullity") != 0:
                continue
            candidate_id = row.get("candidate_id", row.get("tuple_id"))
            source_key = f"{source['packet']}::{candidate_id}"
            rows.append(
                {
                    "source_key": source_key,
                    "source_packet": source["packet"],
                    "candidate_id": candidate_id,
                    "matrix_model": source["matrix_model"],
                    "construction_family": row.get(
                        "construction_family",
                        row.get("family", row.get("mutation_family", "unknown")),
                    ),
                    "matrix_shape": [
                        exact.get("remaining_pairwise_equations"),
                        exact.get("compressed_variables"),
                    ],
                    "rank": exact.get("rank"),
                    "nullity": exact.get("nullity"),
                    "source_matrix_metadata_hash": exact.get("matrix_metadata_hash"),
                }
            )
    return rows


def certificate_for(row: dict[str, Any]) -> dict[str, Any]:
    cert = PRECOMPUTED_PIVOT_CERTIFICATES.get(row["source_key"])
    if cert is None:
        if (
            row["source_packet"] == "two_level_pairwise_divisibility"
            and row["matrix_shape"][1] > 64
        ):
            return {
                "certificate_type": "PIVOT_CERTIFICATE_PENDING_LARGE_MATRIX",
                "reason": (
                    "exact pivot-minor extraction deferred for compressed dimension above "
                    "first-pass limit"
                ),
                "compressed_variables": row["matrix_shape"][1],
                "pivot_column_limit": 64,
                "status": "PIVOT_EXTRACTION_DEFERRED",
            }
        return {
            "certificate_type": "SOURCE_REPLAY_PENDING",
            "reason": "source matrix replay not included in the first-pass pivot audit",
            "status": "SOURCE_REPLAY_PENDING",
        }
    return cert


def certified_rows() -> list[dict[str, Any]]:
    rows = []
    for row in source_candidates():
        cert = certificate_for(row)
        status = "CERTIFIED_FULL_RANK" if cert.get("minor_rank_full") is True else "PENDING"
        rows.append(
            {
                **row,
                "pivot_certificate": cert,
                "certificate_type": cert.get("certificate_type", "SAGE_PIVOT_CERTIFICATE_PENDING"),
                "status": status,
            }
        )
    return rows


def aggregate_by(rows: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        value = str(row[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def build_result() -> dict[str, Any]:
    rows = certified_rows()
    certified = [row for row in rows if row["status"] == "CERTIFIED_FULL_RANK"]
    pending = [row for row in rows if row["status"] != "CERTIFIED_FULL_RANK"]
    pivot_type_counts: dict[str, int] = {}
    for row in certified:
        profile = row["pivot_certificate"].get("pivot_row_type_counts", {})
        for row_type, count in profile.items():
            pivot_type_counts[row_type] = pivot_type_counts.get(row_type, 0) + count
    assert threshold_floor() == 6
    status = "PIVOT_CERTIFICATES_COMPLETE" if len(certified) == len(rows) else "PARTIAL"
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
        "construction_mode": "rim_pivot_certificate_audit",
        "source_summary": {
            "source_packet_count": len(SOURCE_PACKETS),
            "source_matrix_count": len(rows),
            "certified_full_rank_count": len(certified),
            "pending_certificate_count": len(pending),
            "source_packet_counts": aggregate_by(rows, "source_packet"),
            "matrix_model_counts": aggregate_by(rows, "matrix_model"),
            "exact_field": "GF(17^32)",
            "status": status,
        },
        "pivot_summary": {
            "certificate_type": "RREF_PIVOT_MINOR",
            "all_certified_minors_full_rank": len(certified) == len(rows),
            "pivot_row_type_counts": dict(sorted(pivot_type_counts.items())),
            "status": status,
        },
        "certificates": rows,
        "interpretation": {
            "full_rank_replaced_by_replayable_pivot_certificates": len(certified) == len(rows),
            "candidate_found": False,
            "a327_certificate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "status": status,
        },
        "open_layers": {
            "symbolic_pivot_pattern_theorem": True,
            "quotient_residual_designs_outside_sources": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_quotient_residual_rim_pivot_certificates.sage",
            "constructs_GF_17_32": True,
            "reconstructs_source_matrices": True,
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
            "status": status,
        },
        "status": "M1_QUOTIENT_RESIDUAL_RIM_PIVOT_CERTIFICATES_PARTIAL",
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
    parser.add_argument("--list-sources", action="store_true")
    args = parser.parse_args()

    if args.list_sources:
        print(json.dumps(source_candidates(), indent=2, sort_keys=True))
        return
    result = build_result()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output)
        print(f"WROTE {args.output}")
        print(f"source matrices: {result['source_summary']['source_matrix_count']}")
        print(f"certified: {result['source_summary']['certified_full_rank_count']}")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
