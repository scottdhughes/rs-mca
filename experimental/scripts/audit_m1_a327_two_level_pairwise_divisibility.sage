#!/usr/bin/env sage
"""Sage audit for the M1 a=327 two-level pairwise-divisibility search."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from numbers import Integral


DATA_PATH = Path("experimental/data/m1_a327_two_level_pairwise_divisibility.json")
SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_two_level_pairwise_divisibility.py")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7


def load_scanner():
    spec = importlib.util.spec_from_file_location("m1_a327_two_level_scanner", SCANNER_PATH)
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


def field_context(field_mode):
    if field_mode == "exact":
        q = Integer(P) ** FIELD_DEGREE
        F = GF(q, name="z")
        generator = F.multiplicative_generator()
        subgroup_generator = generator ** ((q - 1) // N)
        H = [subgroup_generator**idx for idx in range(N)]
        label = "GF(17^32)"
    elif field_mode == "surrogate":
        q = Integer(12289)
        F = GF(q)
        generator = F.multiplicative_generator()
        subgroup_generator = generator ** ((q - 1) // N)
        H = [subgroup_generator**idx for idx in range(N)]
        label = "GF(12289)_surrogate"
    else:
        raise ValueError("unknown field mode")
    assert len(set(H)) == N
    return q, F, H, label


def locator_values(F, H, vanish_positions):
    values = []
    roots = [H[pos] for pos in vanish_positions]
    for point in H:
        acc = F(1)
        for root in roots:
            acc *= point - root
        values.append(acc)
    return values


def build_compressed_matrix(F, H, pair_sets):
    witness_dims = {}
    witness_offsets = {}
    locator_eval = {}
    ambient_dimension = 0
    for witness in range(1, LIST_SIZE):
        vanish = pair_sets[(0, witness)]
        dim = K - len(vanish)
        if dim <= 0:
            return None
        witness_dims[str(witness)] = dim
        witness_offsets[witness] = ambient_dimension
        ambient_dimension += dim
        locator_eval[witness] = locator_values(F, H, vanish)

    rows = []
    remaining_equations_by_pair = {}
    for i in range(1, LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            positions = pair_sets[(i, j)]
            remaining_equations_by_pair[pair_label((i, j))] = len(positions)
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

    return {
        "rows": rows,
        "ambient_dimension": ambient_dimension,
        "witness_dims": witness_dims,
        "remaining_equations_by_pair": remaining_equations_by_pair,
    }


def rank_gate(pair_sets, field_mode):
    q, F, H, label = field_context(field_mode)
    compressed = build_compressed_matrix(F, H, pair_sets)
    if compressed is None:
        return {
            "field_mode": field_mode,
            "field_label": label,
            "field_size": str(q),
            "compressed_variables": 0,
            "rank": None,
            "nullity": None,
            "status": "ANCHOR_EQUALITY_TOO_LARGE",
        }
    M = matrix(F, compressed["rows"])
    rank = M.rank()
    nullity = compressed["ambient_dimension"] - rank
    return {
        "field_mode": field_mode,
        "field_label": label,
        "field_size": str(q),
        "compressed_variables": compressed["ambient_dimension"],
        "rank": rank,
        "nullity": nullity,
        "non_diagonal_solution_found": nullity > 0,
        "compressed_dimensions_by_witness": compressed["witness_dims"],
        "remaining_pairwise_equations": len(compressed["rows"]),
        "remaining_equations_by_pair": compressed["remaining_equations_by_pair"],
        "matrix_metadata_hash": sha256_payload(
            {
                "field_mode": field_mode,
                "witness_dims": compressed["witness_dims"],
                "remaining_equations_by_pair": compressed["remaining_equations_by_pair"],
                "pair_set_hash": sha256_payload({pair_label(pair): values for pair, values in pair_sets.items()}),
            }
        ),
        "status": "RANK_COMPUTED",
    }


def compute_rank_gates():
    scanner = load_scanner()
    rows = []
    for candidate in scanner.retained_candidates():
        pair_sets = candidate["pair_sets"]
        rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "pair_set_hash": candidate["pairwise_design"]["pair_set_hash"],
                "surrogate": rank_gate(pair_sets, "surrogate"),
                "exact": rank_gate(pair_sets, "exact"),
            }
        )
    return jsonable(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--compute-only", action="store_true")
    args = parser.parse_args()

    computed = compute_rank_gates()
    if args.compute_only:
        print(json.dumps(computed, indent=2, sort_keys=True))
        return

    record = json.loads(DATA_PATH.read_text())
    by_id = {row["candidate_id"]: row for row in computed}
    assert len(record["candidates"]) == len(computed)
    for row in record["candidates"]:
        candidate_id = row["candidate_id"]
        assert candidate_id in by_id
        assert row["pairwise_design"]["pair_set_hash"] == by_id[candidate_id]["pair_set_hash"]
        assert row["surrogate_rank_gate"] == by_id[candidate_id]["surrogate"]
        assert row["sage_exact_rank"] == by_id[candidate_id]["exact"]
        assert row["sage_exact_rank"]["nullity"] == 0
        assert row["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATE"
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "ROUTE_CUT_TESTED_CANDIDATES",
    }
    if args.json:
        print(json.dumps(computed, indent=2, sort_keys=True))
    else:
        print("SAGE_AUDIT_M1_A327_TWO_LEVEL_PAIRWISE_DIVISIBILITY_OK")


if __name__ == "__main__":
    main()
