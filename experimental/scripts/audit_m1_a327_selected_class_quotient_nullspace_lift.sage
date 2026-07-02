#!/usr/bin/env sage
"""Exact GF(17^32) quotient-nullspace audit for M1 a=327 selected classes."""

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
DATA_PATH = Path("experimental/data/m1_a327_selected_class_quotient_nullspace_lift.json")


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


def block_start(witness_one_based):
    """Return quotient block start for witness 2..7."""
    return (int(witness_one_based) - 2) * K


def add_witness_terms(entries, row_index, witness_one_based, scalar, powers, pos):
    if int(witness_one_based) == 1:
        return
    start = block_start(witness_one_based)
    for degree in range(K):
        entries[(row_index, start + degree)] = entries.get((row_index, start + degree), 0) + scalar * powers[degree][pos]


def build_quotient_matrix(F, powers, anchored_classes, row_limit=None):
    ncols = (LIST_SIZE - 1) * K
    entries = {}
    row_index = 0
    for coord in anchored_classes:
        pos = int(coord["position"])
        anchor = int(coord["anchor"])
        for witness in coord["members"]:
            witness = int(witness)
            if witness == anchor:
                continue
            if row_limit is not None and row_index >= row_limit:
                return Matrix(F, row_index, ncols, entries, sparse=True)
            add_witness_terms(entries, row_index, witness, F(1), powers, pos)
            add_witness_terms(entries, row_index, anchor, -F(1), powers, pos)
            row_index += 1
    return Matrix(F, row_index, ncols, entries, sparse=True)


def prefix_rank_results(F, powers, anchored_classes, row_limits):
    results = []
    for row_limit in row_limits:
        matrix = build_quotient_matrix(F, powers, anchored_classes, row_limit=row_limit)
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


def projection_coefficients(vector_row, pair):
    left, right = int(pair[0]), int(pair[1])
    coeffs = [vector_row.parent().base_ring()(0) for _ in range(K)]
    if left != 1:
        start = block_start(left)
        for degree in range(K):
            coeffs[degree] += vector_row[start + degree]
    if right != 1:
        start = block_start(right)
        for degree in range(K):
            coeffs[degree] -= vector_row[start + degree]
    return coeffs


def pair_projection_test(F, basis, exact_rank_limit=256):
    pairs = [(left, right) for left in range(1, LIST_SIZE + 1) for right in range(left + 1, LIST_SIZE + 1)]
    results = []
    forced_equal_pairs = []
    min_projection_rank = None
    exact_ranks = len(basis) <= exact_rank_limit
    for pair in pairs:
        projected_rows = []
        has_nonzero = False
        for row in basis:
            coeffs = projection_coefficients(row, pair)
            if any(value != 0 for value in coeffs):
                has_nonzero = True
            if exact_ranks:
                projected_rows.append(coeffs)
        if exact_ranks:
            rank = int(Matrix(F, projected_rows).rank()) if projected_rows else 0
        else:
            rank = 1 if has_nonzero else 0
        forced_equal = rank == 0
        if forced_equal:
            forced_equal_pairs.append([pair[0], pair[1]])
        min_projection_rank = rank if min_projection_rank is None else min(min_projection_rank, rank)
        results.append(
            {
                "pair": [pair[0], pair[1]],
                "projection_rank": rank,
                "projection_rank_exact": bool(exact_ranks),
                "forced_equal": forced_equal,
            }
        )
    return {
        "pairs_tested": len(pairs),
        "forced_equal_pairs": forced_equal_pairs,
        "projection_results": results,
        "min_projection_rank": min_projection_rank,
    }


def coeff_hash(vector_row, witness_one_based):
    if witness_one_based == 1:
        return hash_payload(["0"] * K)
    start = block_start(witness_one_based)
    return hash_payload([str(vector_row[start + degree]) for degree in range(K)])


def evaluate_differences(F, powers, vector_row, anchored_classes):
    values = []
    zero_values = [F(0) for _ in range(N)]
    values.append(zero_values)
    for witness in range(2, LIST_SIZE + 1):
        start = block_start(witness)
        witness_values = []
        for pos in range(N):
            acc = F(0)
            for degree in range(K):
                acc += vector_row[start + degree] * powers[degree][pos]
            witness_values.append(acc)
        values.append(witness_values)

    r_values = []
    for coord in anchored_classes:
        pos = int(coord["position"])
        anchor = int(coord["anchor"])
        r_values.append(values[anchor - 1][pos])

    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [coeff_hash(vector_row, witness) for witness in range(1, LIST_SIZE + 1)]
    pair_equalities = []
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            if codeword_hashes[left - 1] == codeword_hashes[right - 1]:
                pair_equalities.append([left, right])
    return {
        "agreement_vector": agreements,
        "exact_max_min": min(agreements),
        "seven_distinct": len(set(codeword_hashes)) == LIST_SIZE,
        "pair_equalities": pair_equalities,
        "codeword_hashes": codeword_hashes,
        "received_word_hash": hash_payload([str(value) for value in r_values]),
    }


def deterministic_kernel_candidates(F, basis, sample_limit):
    if not basis or sample_limit <= 0:
        return []
    parent = basis[0].parent()
    alpha = F.multiplicative_generator()
    candidates = []
    candidates.extend(basis[: min(len(basis), sample_limit)])
    if len(candidates) < sample_limit:
        acc = parent.zero()
        for row in basis:
            acc += row
        candidates.append(acc)
    sample_idx = 1
    while len(candidates) < sample_limit:
        acc = parent.zero()
        for idx, row in enumerate(basis):
            coeff = alpha ** ((sample_idx + 1) * (idx + 1))
            acc += coeff * row
        candidates.append(acc)
        sample_idx += 1
    return candidates[:sample_limit]


def construct_candidate(F, powers, basis, anchored_classes, sample_limit):
    samples = []
    seen = set()
    for idx, vector_row in enumerate(deterministic_kernel_candidates(F, basis, sample_limit)):
        vector_hash = hash_payload([str(value) for value in vector_row[: min(128, len(vector_row))]])
        if vector_hash in seen:
            continue
        seen.add(vector_hash)
        evaluation = evaluate_differences(F, powers, vector_row, anchored_classes)
        evaluation["sample_index"] = idx
        evaluation["vector_hash"] = vector_hash
        samples.append(evaluation)
        if evaluation["seven_distinct"] and evaluation["exact_max_min"] >= TARGET_AGREEMENT:
            return evaluation, samples
    best = None if not samples else max(samples, key=lambda row: (row["seven_distinct"], row["exact_max_min"]))
    return best, samples


def classify(nullity, projection, candidate):
    if nullity <= 0:
        return "QUOTIENT_NULLITY_ZERO"
    if projection["forced_equal_pairs"]:
        return "QUOTIENT_LIFT_FORCED_PAIR_EQUALITY"
    if candidate is None:
        return "QUOTIENT_RANK_ONLY"
    if not candidate["seven_distinct"]:
        return "QUOTIENT_LIFT_DEGENERATE"
    if candidate["exact_max_min"] < TARGET_AGREEMENT:
        return "QUOTIENT_LIFT_DISTINCT_BUT_SUPPORT_LOSS"
    return "QUOTIENT_LIFT_EXACT_CANDIDATE"


def audit(row_limits, full, sample_limit):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    anchored_classes = record["thin_selected_hypergraph"]["anchored_classes"]
    prefix_results = prefix_rank_results(F, powers, anchored_classes, row_limits)

    projection = {
        "pairs_tested": 21,
        "forced_equal_pairs": [],
        "projection_results": [],
        "min_projection_rank": None,
    }
    candidate = {
        "constructed": False,
        "seven_distinct": False,
        "agreement_vector": None,
        "exact_max_min": None,
        "received_word_hash": None,
        "codeword_hashes": None,
        "vector_hash": None,
        "sample_results": [],
    }

    if full:
        matrix = build_quotient_matrix(F, powers, anchored_classes)
        rank = int(matrix.rank())
        nrows, ncols = int(matrix.nrows()), int(matrix.ncols())
        nullity = ncols - rank
        basis = list(matrix.right_kernel().basis()) if nullity > 0 else []
        projection = pair_projection_test(F, basis) if basis else projection
        best_sample = None
        samples = []
        if basis and not projection["forced_equal_pairs"]:
            best_sample, samples = construct_candidate(F, powers, basis, anchored_classes, sample_limit)
        if best_sample is not None:
            candidate = {
                "constructed": True,
                "seven_distinct": bool(best_sample["seven_distinct"]),
                "agreement_vector": best_sample["agreement_vector"],
                "exact_max_min": best_sample["exact_max_min"],
                "received_word_hash": best_sample["received_word_hash"],
                "codeword_hashes": best_sample["codeword_hashes"],
                "vector_hash": best_sample["vector_hash"],
                "pair_equalities": best_sample["pair_equalities"],
                "sample_results": samples,
            }
        failure_mode = classify(nullity, projection, best_sample)
        matrix_shape = [nrows, ncols]
    else:
        last = prefix_results[-1]
        _prefix_rank = last["rank"]
        _prefix_nrows, ncols = last["matrix_shape"]
        rank = None
        nullity = None
        matrix_shape = [record["thin_selected_hypergraph"]["selected_incidences"] - N, ncols]
        failure_mode = "QUOTIENT_RANK_ONLY"

    record["quotient_system"].update(
        {
            "variables": (LIST_SIZE - 1) * K,
            "equations": record["thin_selected_hypergraph"]["selected_incidences"] - N,
            "matrix_shape": matrix_shape,
            "rank": rank,
            "nullity": nullity,
            "field": "GF(17^32)",
            "field_denominator": str(q),
            "H_order": len(H),
            "degree_bound": K,
            "full_system_attempted": bool(full),
            "prefix_row_limits": [int(value) for value in row_limits],
            "prefix_rank_results": prefix_results,
            "sample_limit": sample_limit,
            "best_failure_mode": failure_mode,
        }
    )
    record["pair_projection_test"] = jsonable(projection)
    record["exact_candidate"] = jsonable(candidate)
    if failure_mode == "QUOTIENT_LIFT_EXACT_CANDIDATE":
        record["proof_status"] = "PROOF_RECORD / QUOTIENT_LIFT_EXACT_CANDIDATE / EXPERIMENTAL"
    elif full:
        record["proof_status"] = "CANDIDATE / QUOTIENT_AUDIT / PARTIAL / EXPERIMENTAL"
    else:
        record["proof_status"] = "CANDIDATE / PREFIX_RANK_AUDIT / PARTIAL / EXPERIMENTAL"
    return jsonable(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--row-limits", default="128,256,512")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=64)
    args = parser.parse_args()
    row_limits = [int(value) for value in args.row_limits.split(",") if value.strip()]
    record = audit(row_limits=row_limits, full=args.full, sample_limit=args.sample_limit)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        quotient = record["quotient_system"]
        print("SAGE_AUDIT_M1_A327_SELECTED_CLASS_QUOTIENT_NULLSPACE_LIFT_OK")
        print("matrix_shape: %s" % quotient["matrix_shape"])
        print("rank: %s" % quotient["rank"])
        print("nullity: %s" % quotient["nullity"])
        print("best_failure_mode: %s" % quotient["best_failure_mode"])


if __name__ == "__main__":
    main()
