#!/usr/bin/env sage
"""Sage audit for full M1 a=327 RIM support-pattern pivot replay."""

from __future__ import annotations

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
from numbers import Integral

from sage.all import GF, Integer, matrix


DATA_PATH = Path("experimental/data/m1_rim_support_pattern_pivot_replay.json")
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
    module = load_module("base_pivot_audit", BASE_AUDIT_PATH)
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


def source_family(row):
    if row["source_packet"] == "two_level_pairwise_divisibility":
        return "two_level_quotient_residual"
    if row["source_packet"] == "pairwise_divisibility_nullvector_system":
        return "balanced_clique"
    return "support_pattern"


def compact_certificate(base, M, row_meta, row):
    raw = base.pivot_certificate(M, row_meta)
    row_types = raw["pivot_row_type_counts"]
    return {
        "certificate_type": "RREF_PIVOT",
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
        "pivot_minor_size": raw["minor_size"],
        "quotient_row_count": row_types.get("quotient_full_fiber_row", 0),
        "residual_row_count": row_types.get("residual_or_partial_fiber_row", 0),
        "generic_row_count": row_types.get("balanced_or_generic_pairwise_row", 0),
        "support_overlap_row_count": row_types.get("support_overlap_row", 0),
        "source_family": source_family(row),
        "source_matrix_metadata_hash": row["source_matrix_metadata_hash"],
        "pivot_certificate_status": "CERTIFIED",
        "status": "CERTIFIED_FULL_RANK",
    }


def source_candidate_map(base):
    out = {}
    for packet, path in base.SOURCE_SCANNERS.items():
        module = base.load_module(packet, path)
        for candidate in module.retained_candidates():
            out[(packet, candidate["candidate_id"])] = candidate
    return out


def compute_certificates():
    base = load_base_audit()
    scanner = base.load_module("base_pivot_scanner", BASE_SCANNER_PATH)
    source_rows = scanner.source_candidates()
    source_map = source_candidate_map(base)
    _q, F, H = base.field_context()
    rows = []
    for row in source_rows:
        M, row_meta, _witness_dims, _remaining_by_pair = base.reconstruct_matrix(
            F, H, row, source_map
        )
        cert = compact_certificate(base, M, row_meta, row)
        rows.append(
            {
                "source_key": row["source_key"],
                "source_packet": row["source_packet"],
                "candidate_id": row["candidate_id"],
                "pivot_certificate": cert,
            }
        )
    return jsonable(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--compute-only", action="store_true")
    args = parser.parse_args()

    computed = compute_certificates()
    if args.compute_only:
        print(json.dumps(computed, indent=2, sort_keys=True))
        return

    record = json.loads(DATA_PATH.read_text())
    by_key = {row["source_key"]: row for row in computed}
    assert len(record["certificates"]) == len(computed)
    for row in record["certificates"]:
        source_key = row["source_key"]
        assert source_key in by_key
        assert row["pivot_certificate"] == by_key[source_key]["pivot_certificate"]
        assert row["status"] == "CERTIFIED_FULL_RANK"
        assert row["pivot_certificate"]["minor_rank_full"] is True
        assert row["pivot_certificate"]["determinant_nonzero"] is True
        assert row["pivot_certificate"]["pivot_certificate_status"] == "CERTIFIED"
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "PIVOT_COVERAGE_COMPLETE",
    }
    if args.json:
        print(json.dumps(computed, indent=2, sort_keys=True))
    else:
        print("SAGE_AUDIT_M1_RIM_SUPPORT_PATTERN_PIVOT_REPLAY_OK")


if __name__ == "__main__":
    main()
