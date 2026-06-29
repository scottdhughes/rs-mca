#!/usr/bin/env sage
"""Sage audit for the M1 quotient-residual rank-free pivot-rule packet."""

from __future__ import annotations

import argparse
import hashlib
import importlib.machinery
import importlib.util
import json
from pathlib import Path
from numbers import Integral

from sage.all import GF, Integer, matrix


DATA_PATH = Path("experimental/data/m1_quotient_residual_rankfree_pivot_rule.json")
BASE_AUDIT_PATH = Path("experimental/scripts/audit_m1_quotient_residual_rim_pivot_certificates.sage")
BASE_SCANNER_PATH = Path("experimental/scripts/scan_m1_quotient_residual_rim_pivot_certificates.py")
SOURCE_PROFILE_PATH = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")


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
    module = load_module("base_pivot_audit_quotient_residual", BASE_AUDIT_PATH)
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
        module = base.load_module("quotient_residual_" + packet, path)
        for candidate in module.retained_candidates():
            out[(packet, candidate["candidate_id"])] = candidate
    return out


def source_rows_by_key(base):
    scanner = base.load_module("base_pivot_scanner_quotient_residual", BASE_SCANNER_PATH)
    return {
        row["source_key"]: row
        for row in scanner.source_candidates()
        if row["source_packet"] == "two_level_pairwise_divisibility"
    }


def source_profiles_by_key():
    source = json.loads(SOURCE_PROFILE_PATH.read_text())
    return {
        row["source_key"]: row
        for row in source["matrix_profiles"]
        if row["classification"] == "quotient_residual_rref_pivot"
    }


def compact_certificate(base, M, row_meta, row):
    raw = base.pivot_certificate(M, row_meta)
    row_types = raw["pivot_row_type_counts"]
    assert set(row_types).issubset(
        {"quotient_full_fiber_row", "residual_or_partial_fiber_row"}
    )
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


def pair_tuple(pair_label):
    return tuple(int(part) for part in pair_label.split(","))


def row_position(meta):
    return int(meta["position"])


def row_fiber(meta):
    return row_position(meta) % 16


def row_type(meta):
    return meta["row_type"]


def block_offsets(witness_dims):
    offsets = {}
    cursor = 0
    for witness in sorted(int(key) for key in witness_dims):
        dim = int(witness_dims[str(witness)])
        offsets[witness] = (cursor, cursor + dim)
        cursor += dim
    return offsets


def row_block_score(meta, offsets):
    i, j = pair_tuple(meta["pair"])
    i0, i1 = offsets[i]
    j0, j1 = offsets[j]
    return min(i0, j0), max(i1 - i0, j1 - j0)


def first_n(ordering, ncols):
    rows = [idx for idx, _meta in ordering[:ncols]]
    assert len(rows) == ncols
    return rows


def rref_profile_rows(indexed, ncols, pivot_pair_counts):
    rows = []
    used = set()
    by_pair = {}
    for idx, meta in indexed:
        by_pair.setdefault(meta["pair"], []).append((idx, meta))
    for pair, quota in sorted(pivot_pair_counts.items(), key=lambda item: pair_tuple(item[0])):
        chosen = by_pair.get(pair, [])[:quota]
        rows.extend(idx for idx, _meta in chosen)
        used.update(idx for idx, _meta in chosen)
    if len(rows) < ncols:
        for idx, _meta in sorted(indexed, key=lambda item: (row_position(item[1]), pair_tuple(item[1]["pair"]))):
            if idx not in used:
                rows.append(idx)
                used.add(idx)
                if len(rows) == ncols:
                    break
    assert len(rows) == ncols
    return rows


def rref_profile_type_pair_rows(indexed, ncols, pivot_pair_counts, pivot_row_type_counts):
    rows = []
    used = set()
    remaining_type = dict(pivot_row_type_counts)
    by_pair = {}
    for idx, meta in indexed:
        by_pair.setdefault(meta["pair"], []).append((idx, meta))
    type_order = ["quotient_full_fiber_row", "residual_or_partial_fiber_row"]
    for pair, quota in sorted(pivot_pair_counts.items(), key=lambda item: pair_tuple(item[0])):
        candidates = by_pair.get(pair, [])
        local = []
        for wanted_type in type_order:
            for idx, meta in candidates:
                if idx in used or row_type(meta) != wanted_type:
                    continue
                if remaining_type.get(wanted_type, 0) <= 0:
                    continue
                local.append(idx)
                used.add(idx)
                remaining_type[wanted_type] -= 1
                if len(local) == quota:
                    break
            if len(local) == quota:
                break
        if len(local) < quota:
            for idx, _meta in candidates:
                if idx not in used:
                    local.append(idx)
                    used.add(idx)
                    if len(local) == quota:
                        break
        rows.extend(local)
    if len(rows) < ncols:
        for idx, _meta in sorted(
            indexed,
            key=lambda item: (row_type(item[1]), row_fiber(item[1]), row_position(item[1])),
        ):
            if idx not in used:
                rows.append(idx)
                used.add(idx)
                if len(rows) == ncols:
                    break
    assert len(rows) == ncols
    return rows


def schedule_rules(row_meta, ncols, witness_dims, pivot_pair_counts, pivot_row_type_counts):
    indexed = list(enumerate(row_meta))
    pair_sizes = {}
    fiber_sizes = {}
    row_type_sizes = {}
    witness_loads = {}
    for _idx, meta in indexed:
        pair = meta["pair"]
        pair_sizes[pair] = pair_sizes.get(pair, 0) + 1
        fiber = row_fiber(meta)
        fiber_sizes[fiber] = fiber_sizes.get(fiber, 0) + 1
        row_type_sizes[row_type(meta)] = row_type_sizes.get(row_type(meta), 0) + 1
        for witness in pair_tuple(pair):
            witness_loads[witness] = witness_loads.get(witness, 0) + 1
    offsets = block_offsets(witness_dims)
    pair_boundary_key = lambda item: (
        -pair_sizes[item[1]["pair"]],
        pair_tuple(item[1]["pair"]),
        row_position(item[1]),
    )
    pair_boundary_asc_key = lambda item: (
        pair_sizes[item[1]["pair"]],
        pair_tuple(item[1]["pair"]),
        row_position(item[1]),
    )
    incidence_key = lambda item: (
        witness_loads[pair_tuple(item[1]["pair"])[0]]
        + witness_loads[pair_tuple(item[1]["pair"])[1]],
        pair_sizes[item[1]["pair"]],
        pair_tuple(item[1]["pair"]),
        row_position(item[1]),
    )
    rules = {
        "pair_label_coordinate_order": first_n(
            sorted(indexed, key=lambda item: (pair_tuple(item[1]["pair"]), row_position(item[1]))),
            ncols,
        ),
        "pair_boundary_pressure_desc": first_n(sorted(indexed, key=pair_boundary_key), ncols),
        "pair_boundary_pressure_asc": first_n(sorted(indexed, key=pair_boundary_asc_key), ncols),
        "quotient_full_fiber_first": first_n(
            sorted(
                indexed,
                key=lambda item: (
                    0 if row_type(item[1]) == "quotient_full_fiber_row" else 1,
                    row_fiber(item[1]),
                    pair_tuple(item[1]["pair"]),
                    row_position(item[1]),
                ),
            ),
            ncols,
        ),
        "residual_partial_fiber_first": first_n(
            sorted(
                indexed,
                key=lambda item: (
                    0 if row_type(item[1]) == "residual_or_partial_fiber_row" else 1,
                    row_fiber(item[1]),
                    pair_tuple(item[1]["pair"]),
                    row_position(item[1]),
                ),
            ),
            ncols,
        ),
        "fiber_coordinate_order": first_n(
            sorted(
                indexed,
                key=lambda item: (
                    row_fiber(item[1]),
                    row_position(item[1]),
                    row_type(item[1]),
                    pair_tuple(item[1]["pair"]),
                ),
            ),
            ncols,
        ),
        "row_type_pair_order": first_n(
            sorted(
                indexed,
                key=lambda item: (
                    row_type(item[1]),
                    pair_tuple(item[1]["pair"]),
                    row_position(item[1]),
                ),
            ),
            ncols,
        ),
        "quotient_residual_balanced_order": first_n(
            sorted(
                indexed,
                key=lambda item: (
                    abs(
                        row_type_sizes.get(row_type(item[1]), 0)
                        - pivot_row_type_counts.get(row_type(item[1]), 0)
                    ),
                    row_type(item[1]),
                    row_fiber(item[1]),
                    pair_tuple(item[1]["pair"]),
                    row_position(item[1]),
                ),
            ),
            ncols,
        ),
        "compressed_variable_block_order": first_n(
            sorted(
                indexed,
                key=lambda item: (
                    row_block_score(item[1], offsets),
                    pair_tuple(item[1]["pair"]),
                    row_position(item[1]),
                ),
            ),
            ncols,
        ),
        "incidence_greedy_matching_v1": first_n(sorted(indexed, key=incidence_key), ncols),
        "rref_profile_type_pair_quota_mimic": rref_profile_type_pair_rows(
            indexed, ncols, pivot_pair_counts, pivot_row_type_counts
        ),
    }
    return rules


def rule_attempts(base, M, row_meta, witness_dims, pivot_pair_counts, pivot_row_type_counts):
    ncols = M.ncols()
    cols = list(range(ncols))
    out = []
    for rule, rows in sorted(
        schedule_rules(
            row_meta, ncols, witness_dims, pivot_pair_counts, pivot_row_type_counts
        ).items()
    ):
        assert len(rows) == ncols
        minor = M.matrix_from_rows_and_columns(rows, cols)
        minor_rank = minor.rank()
        selected_meta = [row_meta[idx] for idx in rows]
        pair_counts = {}
        for meta in selected_meta:
            pair = meta["pair"]
            pair_counts[pair] = pair_counts.get(pair, 0) + 1
        rule_class = (
            "RREF_MIMIC_RULE"
            if rule == "rref_profile_type_pair_quota_mimic"
            else "DETERMINISTIC_COMBINATORIAL_RULE"
        )
        out.append(
            {
                "rule": rule,
                "rule_class": rule_class,
                "uses_field_arithmetic": False,
                "rule_uses_field_arithmetic": False,
                "selected_minor_size": ncols,
                "minor_rank": minor_rank,
                "minor_nonzero": minor_rank == ncols,
                "pivot_rows_hash": base.sha256_payload(rows),
                "pivot_cols_hash": base.sha256_payload(cols),
                "pivot_pairs_hash": base.sha256_payload(pair_counts),
                "pair_pivot_counts": dict(sorted(pair_counts.items())),
                "status": "SUCCESS" if minor_rank == ncols else "SINGULAR_MINOR",
            }
        )
    return out


def compute_quotient_residual_rows(record=None):
    base = load_base_audit()
    source_map = source_candidate_map(base)
    source_rows = source_rows_by_key(base)
    source_profiles = source_profiles_by_key()
    _q, F, H = base.field_context()
    keys = sorted(source_profiles)
    rows = []
    for source_key in keys:
        assert source_key in source_rows
        source_row = source_rows[source_key]
        M, row_meta, witness_dims, remaining_by_pair = base.reconstruct_matrix(
            F, H, source_row, source_map
        )
        cert = compact_certificate(base, M, row_meta, source_row)
        profile = source_profiles[source_key]
        rows.append(
            {
                "source_key": source_key,
                "candidate_id": source_row["candidate_id"],
                "source_packet": source_row["source_packet"],
                "source_family": profile["source_family"],
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
                "compressed_dimensions_by_witness": witness_dims,
                "remaining_equations_by_pair": remaining_by_pair,
                "rankfree_rule_attempts": rule_attempts(
                    base,
                    M,
                    row_meta,
                witness_dims,
                profile["pivot_pattern"]["pair_pivot_counts"],
                profile["pivot_pattern"]["row_type_counts"],
            ),
            "status": "CERTIFIED_RREF_DERIVED",
        }
        )
    return jsonable(rows)


def validate_record(record, computed):
    by_key = {row["source_key"]: row for row in computed}
    assert len(by_key) == 8
    assert record["matrix_count"] == 8
    assert record["rule_summary"]["rules_tested"] == 11
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": record["rule_summary"]["status"],
    }
    for matrix_record in record["matrices"]:
        source_key = matrix_record["source_key"]
        assert source_key in by_key
        computed_row = by_key[source_key]
        pivot = matrix_record["rref_certificate"]
        assert matrix_record["matrix_shape"] == computed_row["matrix_shape"]
        assert matrix_record["rank"] == computed_row["rank"] == matrix_record["matrix_shape"][1]
        assert matrix_record["nullity"] == computed_row["nullity"] == 0
        assert computed_row["minor_rank_full"] is True
        assert computed_row["determinant_nonzero"] is True
        assert pivot["pivot_rows_hash"] == computed_row["pivot_rows_hash"]
        assert pivot["pivot_cols_hash"] == computed_row["pivot_cols_hash"]
        assert pivot["pivot_pairs_hash"] == computed_row["pivot_pairs_hash"]
        assert pivot["minor_hash"] == computed_row["minor_hash"]
        assert pivot["pair_pivot_counts"] == computed_row["pivot_pair_counts"]
        assert pivot["row_type_counts"] == computed_row["pivot_row_type_counts"]
        assert matrix_record["rankfree_rules"] == computed_row["rankfree_rule_attempts"]
        for attempt in matrix_record["rankfree_rules"]:
            assert attempt["uses_field_arithmetic"] is False
            assert attempt["rule_uses_field_arithmetic"] is False
            assert attempt["minor_nonzero"] == (attempt["minor_rank"] == matrix_record["matrix_shape"][1])
    expected_hash = hash_payload(
        {
            "source_profile": record["source_profile"],
            "rule_summary": record["rule_summary"],
            "matrices": record["matrices"],
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

    if args.compute_only:
        print(json.dumps(compute_quotient_residual_rows(), indent=2, sort_keys=True))
        return
    record = json.loads(DATA_PATH.read_text())
    computed = compute_quotient_residual_rows(record)
    validate_record(record, computed)
    if args.json:
        print(json.dumps(computed, indent=2, sort_keys=True))
    else:
        print("SAGE_AUDIT_M1_QUOTIENT_RESIDUAL_RANKFREE_PIVOT_RULE_OK")


if __name__ == "__main__":
    main()
