#!/usr/bin/env sage
"""Sage pivot-certificate audit for M1 a=327 reduced-intersection matrices."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from numbers import Integral


DATA_PATH = Path("experimental/data/m1_quotient_residual_rim_pivot_certificates.json")
SCANNER_PATH = Path("experimental/scripts/scan_m1_quotient_residual_rim_pivot_certificates.py")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7

SOURCE_SCANNERS = {
    "pairwise_divisibility_nullvector_system": Path(
        "experimental/scripts/scan_m1_a327_pairwise_divisibility_nullvector_system.py"
    ),
    "two_level_pairwise_divisibility": Path(
        "experimental/scripts/scan_m1_a327_two_level_pairwise_divisibility.py"
    ),
    "constructive_rank_defect_support_design": Path(
        "experimental/scripts/scan_m1_constructive_rank_defect_support_design.py"
    ),
    "support_pattern_multiplicity_mutation_search": Path(
        "experimental/scripts/scan_m1_support_pattern_multiplicity_mutation_search.py"
    ),
    "support_pattern_surrogate_rank_feedback_search": Path(
        "experimental/scripts/scan_m1_support_pattern_surrogate_rank_feedback_search.py"
    ),
}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
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


def sha256_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def pair_label(pair):
    return "%d,%d" % (pair[0], pair[1])


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    return q, F, H


def locator_values(F, H, vanish_positions):
    roots = [H[pos] for pos in vanish_positions]
    values = []
    for point in H:
        acc = F(1)
        for root in roots:
            acc *= point - root
        values.append(acc)
    return values


def support_positions(memberships):
    supports = [[] for _idx in range(LIST_SIZE)]
    for pos, members in enumerate(memberships):
        for member in members:
            supports[member].append(pos)
    return supports


def intersection_positions(supports):
    intersections = {}
    for i in range(LIST_SIZE):
        set_i = set(supports[i])
        for j in range(i + 1, LIST_SIZE):
            intersections[(i, j)] = sorted(set_i.intersection(supports[j]))
    return intersections


def pair_positions_from_partitions(partitions):
    positions = {}
    for i in range(LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            positions[(i, j)] = []
    for pos, partition in enumerate(partitions):
        for block in partition:
            for idx_i in range(len(block)):
                for idx_j in range(idx_i + 1, len(block)):
                    i = block[idx_i]
                    j = block[idx_j]
                    if i > j:
                        i, j = j, i
                    positions[(i, j)].append(pos)
    return positions


def row_type_for_pairset(pair_sets, pair, pos):
    by_fiber = {}
    for point in pair_sets[pair]:
        fiber = point % 16
        by_fiber[fiber] = by_fiber.get(fiber, 0) + 1
    occupancy = by_fiber.get(pos % 16, 0)
    if occupancy == 32:
        return "quotient_full_fiber_row"
    if occupancy > 0:
        return "residual_or_partial_fiber_row"
    return "unexpected_pairset_row"


def build_matrix_from_pair_sets(F, H, pair_sets, row_type_mode):
    witness_dims = {}
    witness_offsets = {}
    locator_eval = {}
    ambient_dimension = 0
    for witness in range(1, LIST_SIZE):
        vanish = pair_sets[(0, witness)]
        dim = K - len(vanish)
        if dim <= 0:
            raise ValueError("anchor equality too large")
        witness_dims[str(witness)] = dim
        witness_offsets[witness] = ambient_dimension
        ambient_dimension += dim
        locator_eval[witness] = locator_values(F, H, vanish)

    rows = []
    row_meta = []
    remaining_by_pair = {}
    for i in range(1, LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            pair = (i, j)
            positions = pair_sets[pair]
            remaining_by_pair[pair_label(pair)] = len(positions)
            dim_i = witness_dims[str(i)]
            dim_j = witness_dims[str(j)]
            off_i = witness_offsets[i]
            off_j = witness_offsets[j]
            for pos in positions:
                point = H[pos]
                row = [F(0) for _idx in range(ambient_dimension)]
                power = F(1)
                scale_i = locator_eval[i][pos]
                for degree in range(dim_i):
                    row[off_i + degree] = scale_i * power
                    power *= point
                power = F(1)
                scale_j = locator_eval[j][pos]
                for degree in range(dim_j):
                    row[off_j + degree] -= scale_j * power
                    power *= point
                rows.append(row)
                if row_type_mode == "two_level":
                    row_type = row_type_for_pairset(pair_sets, pair, pos)
                else:
                    row_type = "balanced_or_generic_pairwise_row"
                row_meta.append({"pair": pair_label(pair), "position": pos, "row_type": row_type})
    return matrix(F, rows), row_meta, witness_dims, remaining_by_pair


def build_matrix_from_memberships(F, H, memberships):
    supports = support_positions(memberships)
    intersections = intersection_positions(supports)
    witness_dims = {}
    witness_offsets = {}
    locator_eval = {}
    ambient_dimension = 0
    for witness in range(1, LIST_SIZE):
        vanish = intersections[(0, witness)]
        dim = K - len(vanish)
        if dim <= 0:
            raise ValueError("anchor intersection too large")
        witness_dims[str(witness)] = dim
        witness_offsets[witness] = ambient_dimension
        ambient_dimension += dim
        locator_eval[witness] = locator_values(F, H, vanish)

    rows = []
    row_meta = []
    remaining_by_pair = {}
    for i in range(1, LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            pair = (i, j)
            positions = intersections[pair]
            remaining_by_pair[pair_label(pair)] = len(positions)
            dim_i = witness_dims[str(i)]
            dim_j = witness_dims[str(j)]
            off_i = witness_offsets[i]
            off_j = witness_offsets[j]
            for pos in positions:
                point = H[pos]
                row = [F(0) for _idx in range(ambient_dimension)]
                power = F(1)
                scale_i = locator_eval[i][pos]
                for degree in range(dim_i):
                    row[off_i + degree] = scale_i * power
                    power *= point
                power = F(1)
                scale_j = locator_eval[j][pos]
                for degree in range(dim_j):
                    row[off_j + degree] -= scale_j * power
                    power *= point
                rows.append(row)
                row_meta.append({"pair": pair_label(pair), "position": pos, "row_type": "support_overlap_row"})
    return matrix(F, rows), row_meta, witness_dims, remaining_by_pair


SUPPORTED_RECONSTRUCTION_PACKETS = {
    "two_level_pairwise_divisibility",
}
PIVOT_COLUMN_LIMIT = 64


def source_candidate_map():
    modules = {
        name: load_module(name, path)
        for name, path in SOURCE_SCANNERS.items()
        if name in SUPPORTED_RECONSTRUCTION_PACKETS
    }
    out = {}
    for packet, module in modules.items():
        for candidate in module.retained_candidates():
            candidate_id = candidate["candidate_id"]
            out[(packet, candidate_id)] = candidate
    return out


def reconstruct_matrix(F, H, row, source_map):
    key = (row["source_packet"], row["candidate_id"])
    candidate = source_map[key]
    packet = row["source_packet"]
    if packet == "pairwise_divisibility_nullvector_system":
        scanner = load_module("pairwise_scanner_for_pivot", SOURCE_SCANNERS[packet])
        pair_sets = scanner.pair_positions(candidate["equality_partitions"])
        return build_matrix_from_pair_sets(F, H, pair_sets, "generic")
    if packet == "two_level_pairwise_divisibility":
        return build_matrix_from_pair_sets(F, H, candidate["pair_sets"], "two_level")
    return build_matrix_from_memberships(F, H, candidate["memberships"])


def pivot_certificate(M, row_meta):
    rank = M.rank()
    ncols = M.ncols()
    assert rank == ncols
    pivot_rows = list(M.transpose().pivots())
    assert len(pivot_rows) >= ncols
    pivot_rows = pivot_rows[:ncols]
    pivot_cols = list(range(ncols))
    minor = M.matrix_from_rows_and_columns(pivot_rows, pivot_cols)
    minor_rank = minor.rank()
    row_type_counts = {}
    pair_counts = {}
    for row_idx in pivot_rows:
        meta = row_meta[row_idx]
        row_type = meta["row_type"]
        pair = meta["pair"]
        row_type_counts[row_type] = row_type_counts.get(row_type, 0) + 1
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    return {
        "certificate_type": "RREF_PIVOT_MINOR",
        "minor_size": ncols,
        "matrix_rows": M.nrows(),
        "matrix_cols": ncols,
        "rank": rank,
        "nullity": ncols - rank,
        "pivot_rows_hash": sha256_payload(pivot_rows),
        "pivot_cols_hash": sha256_payload(pivot_cols),
        "pivot_pairs_hash": sha256_payload(pair_counts),
        "pivot_row_type_counts": dict(sorted(row_type_counts.items())),
        "pivot_pair_counts": dict(sorted(pair_counts.items())),
        "minor_rank": minor_rank,
        "minor_rank_full": minor_rank == ncols,
        "minor_det_nonzero": minor_rank == ncols,
        "status": "CERTIFIED_FULL_RANK",
    }


def compute_certificates():
    scanner = load_module("pivot_scanner", SCANNER_PATH)
    source_rows = scanner.source_candidates()
    source_map = source_candidate_map()
    _q, F, H = field_context()
    rows = []
    for row in source_rows:
        if row["source_packet"] not in SUPPORTED_RECONSTRUCTION_PACKETS:
            rows.append(
                {
                    "source_key": row["source_key"],
                    "source_packet": row["source_packet"],
                    "candidate_id": row["candidate_id"],
                    "pivot_certificate": {
                        "certificate_type": "SOURCE_REPLAY_PENDING",
                        "reason": "source matrix replay not included in the first-pass pivot audit",
                        "status": "SOURCE_REPLAY_PENDING",
                    },
                }
            )
            continue
        if row["matrix_shape"][1] > PIVOT_COLUMN_LIMIT:
            rows.append(
                {
                    "source_key": row["source_key"],
                    "source_packet": row["source_packet"],
                    "candidate_id": row["candidate_id"],
                    "pivot_certificate": {
                        "certificate_type": "PIVOT_CERTIFICATE_PENDING_LARGE_MATRIX",
                        "reason": "exact pivot-minor extraction deferred for compressed dimension above first-pass limit",
                        "compressed_variables": row["matrix_shape"][1],
                        "pivot_column_limit": PIVOT_COLUMN_LIMIT,
                        "status": "PIVOT_EXTRACTION_DEFERRED",
                    },
                }
            )
            continue
        M, row_meta, witness_dims, remaining_by_pair = reconstruct_matrix(F, H, row, source_map)
        cert = pivot_certificate(M, row_meta)
        cert["compressed_dimensions_by_witness"] = witness_dims
        cert["remaining_equations_by_pair"] = remaining_by_pair
        cert["source_matrix_metadata_hash"] = row["source_matrix_metadata_hash"]
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
        if row["status"] == "CERTIFIED_FULL_RANK":
            assert row["pivot_certificate"]["minor_rank_full"] is True
        else:
            assert row["status"] == "PENDING"
            assert row["pivot_certificate"]["status"] in {
                "SOURCE_REPLAY_PENDING",
                "PIVOT_EXTRACTION_DEFERRED",
            }
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "PARTIAL",
    }
    if args.json:
        print(json.dumps(computed, indent=2, sort_keys=True))
    else:
        print("SAGE_AUDIT_M1_QUOTIENT_RESIDUAL_RIM_PIVOT_CERTIFICATES_OK")


if __name__ == "__main__":
    main()
