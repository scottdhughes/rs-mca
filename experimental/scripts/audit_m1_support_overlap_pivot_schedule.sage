#!/usr/bin/env sage
"""Sage audit for the M1 support-overlap RREF pivot-schedule packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
from numbers import Integral

from sage.all import GF, Integer, matrix


DATA_PATH = Path("experimental/data/m1_support_overlap_pivot_schedule.json")
BASE_AUDIT_PATH = Path("experimental/scripts/audit_m1_quotient_residual_rim_pivot_certificates.sage")
BASE_SCANNER_PATH = Path("experimental/scripts/scan_m1_quotient_residual_rim_pivot_certificates.py")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        loader = importlib.machinery.SourceFileLoader(name, str(path))
        spec = importlib.util.spec_from_loader(name, loader)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_base_audit():
    module = load_module("base_pivot_audit_support_overlap", BASE_AUDIT_PATH)
    module.Integer = Integer
    module.GF = GF
    module.matrix = matrix
    return module


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def source_candidate_map(base):
    out = {}
    for packet, path in base.SOURCE_SCANNERS.items():
        module = base.load_module("support_overlap_" + packet, path)
        for candidate in module.retained_candidates():
            out[(packet, candidate["candidate_id"])] = candidate
    return out


def compact_certificate(base, M, row_meta, row):
    raw = base.pivot_certificate(M, row_meta)
    row_types = raw["pivot_row_type_counts"]
    assert row_types == {"support_overlap_row": raw["matrix_cols"]}
    return {
        "matrix_rows": raw["matrix_rows"],
        "matrix_cols": raw["matrix_cols"],
        "rank": raw["rank"],
        "nullity": raw["nullity"],
        "minor_size": raw["minor_size"],
        "minor_rank": raw["minor_rank"],
        "minor_rank_full": raw["minor_rank_full"],
        "determinant_nonzero": raw["minor_det_nonzero"],
        "pivot_rows_hash": raw["pivot_rows_hash"],
        "pivot_cols_hash": raw["pivot_cols_hash"],
        "pivot_pairs_hash": raw["pivot_pairs_hash"],
        "pivot_row_type_counts": raw["pivot_row_type_counts"],
        "pivot_pair_counts": raw["pivot_pair_counts"],
        "source_matrix_metadata_hash": row["source_matrix_metadata_hash"],
    }


def expected_minor_hash(cert):
    return hash_payload(
        {
            "pivot_rows_hash": cert["pivot_rows_hash"],
            "pivot_cols_hash": cert["pivot_cols_hash"],
            "pivot_pairs_hash": cert["pivot_pairs_hash"],
            "source_matrix_metadata_hash": cert["source_matrix_metadata_hash"],
        }
    )


def source_rows_by_key(base):
    scanner = base.load_module("base_pivot_scanner_support_overlap", BASE_SCANNER_PATH)
    return {
        row["source_key"]: row
        for row in scanner.source_candidates()
        if row["matrix_model"] == "support_design_reduced_intersection_matrix"
    }


def compute_support_schedules(record):
    base = load_base_audit()
    source_map = source_candidate_map(base)
    source_rows = source_rows_by_key(base)
    _q, F, H = base.field_context()
    rows = []
    for schedule in record["matrix_schedules"]:
        source_key = schedule["source_key"]
        assert source_key in source_rows
        source_row = source_rows[source_key]
        M, row_meta, _witness_dims, _remaining_by_pair = base.reconstruct_matrix(
            F, H, source_row, source_map
        )
        cert = compact_certificate(base, M, row_meta, source_row)
        rows.append(
            {
                "source_key": source_key,
                "candidate_id": source_row["candidate_id"],
                "matrix_shape": [cert["matrix_rows"], cert["matrix_cols"]],
                "rank": cert["rank"],
                "nullity": cert["nullity"],
                "minor_rank_full": cert["minor_rank_full"],
                "determinant_nonzero": cert["determinant_nonzero"],
                "pivot_rows_hash": cert["pivot_rows_hash"],
                "pivot_cols_hash": cert["pivot_cols_hash"],
                "pivot_pairs_hash": cert["pivot_pairs_hash"],
                "minor_hash": expected_minor_hash(cert),
                "pivot_pair_counts": cert["pivot_pair_counts"],
                "pivot_row_type_counts": cert["pivot_row_type_counts"],
                "status": "CERTIFIED_RREF_DERIVED",
            }
        )
    return jsonable(rows)


def validate_record(record, computed):
    by_key = {row["source_key"]: row for row in computed}
    assert len(by_key) == 20
    assert record["schedule_summary"]["support_overlap_matrices"] == 20
    assert record["theorem_assessment"]["deterministic_schedule_proved"] is False
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "RREF_DERIVED_PATTERN_ONLY",
    }
    for schedule in record["matrix_schedules"]:
        source_key = schedule["source_key"]
        assert source_key in by_key
        computed_row = by_key[source_key]
        pivot = schedule["pivot_schedule"]
        assert schedule["matrix_shape"] == computed_row["matrix_shape"]
        assert schedule["rank"] == computed_row["rank"] == schedule["matrix_shape"][1]
        assert schedule["nullity"] == computed_row["nullity"] == 0
        assert computed_row["minor_rank_full"] is True
        assert computed_row["determinant_nonzero"] is True
        assert pivot["pivot_rows_hash"] == computed_row["pivot_rows_hash"]
        assert pivot["pivot_cols_hash"] == computed_row["pivot_cols_hash"]
        assert pivot["pivot_pairs_hash"] == computed_row["pivot_pairs_hash"]
        assert pivot["minor_hash"] == computed_row["minor_hash"]
        assert pivot["pair_pivot_counts"] == computed_row["pivot_pair_counts"]
        assert pivot["row_type_counts"] == computed_row["pivot_row_type_counts"]
        assert pivot["support_overlap_pivot_count"] == schedule["matrix_shape"][1]
        assert pivot["deterministic_combinatorial_schedule"] is False

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--compute-only", action="store_true")
    args = parser.parse_args()

    record = json.loads(DATA_PATH.read_text())
    computed = compute_support_schedules(record)
    if args.compute_only:
        print(json.dumps(computed, indent=2, sort_keys=True))
        return
    validate_record(record, computed)
    if args.json:
        print(json.dumps(computed, indent=2, sort_keys=True))
    else:
        print("SAGE_AUDIT_M1_SUPPORT_OVERLAP_PIVOT_SCHEDULE_OK")


if __name__ == "__main__":
    main()
