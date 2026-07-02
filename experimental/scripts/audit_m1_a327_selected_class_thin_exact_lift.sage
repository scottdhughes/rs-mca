#!/usr/bin/env sage
"""Exact GF(17^32) audit for selected-class thin M1 a=327 lifts."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
DATA_PATH = Path("experimental/data/m1_a327_selected_class_thin_exact_lift.json")


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    try:
        if hasattr(payload, "__float__"):
            return float(payload)
    except Exception:
        pass
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


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def build_matrix(F, powers, coordinate_classes, row_limit=None):
    ncols = LIST_SIZE * K + N
    entries = {}
    row_index = 0
    for coord in coordinate_classes:
        pos = int(coord["position"])
        for witness_one_based in coord["members"]:
            if row_limit is not None and row_index >= row_limit:
                return Matrix(F, row_index, ncols, entries, sparse=True)
            witness = int(witness_one_based) - 1
            start = witness * K
            for degree in range(K):
                entries[(row_index, start + degree)] = powers[degree][pos]
            entries[(row_index, LIST_SIZE * K + pos)] = -F(1)
            row_index += 1
    matrix = Matrix(F, row_index, ncols, entries, sparse=True)
    return matrix


def coeff_hash(vector_row, witness):
    start = witness * K
    return hash_payload([str(vector_row[start + degree]) for degree in range(K)])


def evaluate_vector(F, powers, vector_row):
    values = []
    for witness in range(LIST_SIZE):
        start = witness * K
        witness_values = []
        for pos in range(N):
            acc = F(0)
            for degree in range(K):
                acc += vector_row[start + degree] * powers[degree][pos]
            witness_values.append(acc)
        values.append(witness_values)
    r_values = [vector_row[LIST_SIZE * K + pos] for pos in range(N)]
    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [coeff_hash(vector_row, witness) for witness in range(LIST_SIZE)]
    return {
        "agreement_vector": agreements,
        "exact_max_min": min(agreements),
        "distinct_codewords": len(set(codeword_hashes)) == LIST_SIZE,
        "codeword_hashes": codeword_hashes,
        "received_word_hash": hash_payload([str(value) for value in r_values]),
    }


def sample_kernel_vectors(F, powers, matrix, sample_limit):
    if sample_limit <= 0:
        return []
    kernel = matrix.right_kernel()
    basis = list(kernel.basis())
    if not basis:
        return []
    samples = []
    candidates = []
    candidates.extend(basis[: min(len(basis), sample_limit)])
    if len(candidates) < sample_limit:
        acc = sum(basis, basis[0].parent().zero())
        candidates.append(acc)
    if len(candidates) < sample_limit:
        weighted = basis[0].parent().zero()
        for idx, row in enumerate(basis):
            weighted += F((idx % 16) + 1) * row
        candidates.append(weighted)
    seen = set()
    for idx, vector_row in enumerate(candidates):
        vector_hash = hash_payload([str(value) for value in vector_row[: min(64, len(vector_row))]])
        if vector_hash in seen:
            continue
        seen.add(vector_hash)
        evaluation = evaluate_vector(F, powers, vector_row)
        evaluation["sample_index"] = idx
        evaluation["vector_prefix_hash"] = vector_hash
        samples.append(evaluation)
        if len(samples) >= sample_limit:
            break
    return samples


def classify_exact(matrix_shape, rank, nullity, samples):
    if nullity <= 0:
        return "SELECTED_LIFT_LOW_NULLITY"
    if not samples:
        return "SELECTED_LIFT_RANK_ONLY"
    best = max(samples, key=lambda row: (row["distinct_codewords"], row["exact_max_min"]))
    if best["distinct_codewords"] and best["exact_max_min"] >= TARGET_AGREEMENT:
        return "SELECTED_LIFT_EXACT_CANDIDATE"
    if not best["distinct_codewords"]:
        return "SELECTED_LIFT_DEGENERATE"
    return "SELECTED_LIFT_LOW_AGREEMENT"


def prefix_rank_results(F, powers, coordinate_classes, row_limits):
    results = []
    for row_limit in row_limits:
        matrix = build_matrix(F, powers, coordinate_classes, row_limit=row_limit)
        rank = int(matrix.rank())
        nrows, ncols = int(matrix.nrows()), int(matrix.ncols())
        results.append(
            {
                "row_limit": int(row_limit),
                "matrix_shape": [nrows, ncols],
                "rank": rank,
                "nullity_in_prefix_projection": ncols - rank,
                "full_row_rank_prefix": rank == nrows,
            }
        )
    return results


def audit(sample_limit, row_limits, full):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    coordinate_classes = record["thin_hypergraph"]["best_coordinate_classes"]
    prefix_results = prefix_rank_results(F, powers, coordinate_classes, row_limits)
    if full:
        matrix = build_matrix(F, powers, coordinate_classes)
        rank = int(matrix.rank())
        nrows, ncols = int(matrix.nrows()), int(matrix.ncols())
        nullity = ncols - rank
        samples = sample_kernel_vectors(F, powers, matrix, sample_limit) if nullity > 0 else []
        best_sample = None if not samples else max(samples, key=lambda row: (row["distinct_codewords"], row["exact_max_min"]))
        matrix_shape = [nrows, ncols]
        failure_mode = classify_exact(matrix_shape, rank, nullity, samples)
    else:
        last = prefix_results[-1]
        rank = last["rank"]
        nrows, ncols = last["matrix_shape"]
        nullity = ncols - rank
        samples = []
        best_sample = None
        matrix_shape = [nrows, ncols]
        failure_mode = "SELECTED_LIFT_RANK_ONLY"

    exact_lift = {
        "systems_tested": 1,
        "timeouts": 0,
        "full_system_attempted": bool(full),
        "prefix_row_limits": [int(value) for value in row_limits],
        "prefix_rank_results": prefix_results,
        "matrix_shape": matrix_shape,
        "rank": rank,
        "nullity": nullity,
        "exact_vectors_constructed": len(samples),
        "seven_distinct_vectors": sum(1 for row in samples if row["distinct_codewords"]),
        "best_agreement_vector": None if best_sample is None else best_sample["agreement_vector"],
        "best_exact_max_min": None if best_sample is None else best_sample["exact_max_min"],
        "best_distinct_codewords": None if best_sample is None else best_sample["distinct_codewords"],
        "sample_limit": sample_limit,
        "sample_results": samples,
        "field": "GF(17^32)",
        "field_denominator": str(q),
        "H_order": len(H),
        "degree_bound": K,
        "best_failure_mode": failure_mode,
    }
    record["exact_lift"] = jsonable(exact_lift)
    if exact_lift["best_failure_mode"] == "SELECTED_LIFT_EXACT_CANDIDATE":
        record["proof_status"] = "PROOF_RECORD / CANDIDATE / SELECTED_LIFT_EXACT_CANDIDATE / EXPERIMENTAL"
    else:
        record["proof_status"] = "PROOF_RECORD / CANDIDATE / EXACT_EXTRACTION_NO_A327 / PARTIAL"
    return jsonable(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=6)
    parser.add_argument("--row-limits", default="128,256,512")
    parser.add_argument("--full", action="store_true")
    args = parser.parse_args()
    row_limits = [int(value) for value in args.row_limits.split(",") if value.strip()]
    record = audit(args.sample_limit, row_limits, args.full)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        exact = record["exact_lift"]
        print("SAGE_AUDIT_M1_A327_SELECTED_CLASS_THIN_EXACT_LIFT_OK")
        print("matrix_shape: %s" % exact["matrix_shape"])
        print("rank: %s" % exact["rank"])
        print("nullity: %s" % exact["nullity"])
        print("best_failure_mode: %s" % exact["best_failure_mode"])


if __name__ == "__main__":
    main()
