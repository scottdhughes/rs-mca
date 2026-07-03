#!/usr/bin/env sage
"""Exact GF(17^32) audit for the mixed_rank6 low-rank M1 a=327 template."""

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
DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_exact_audit.json")


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


def exact_field_context():
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
    for _degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def row_basis(F, vectors, members):
    if len(members) <= 1:
        return []
    anchor = [F(value) for value in vectors[int(members[0]) - 1]]
    rows = []
    for witness in members[1:]:
        rows.append([F(value) - anchor[idx] for idx, value in enumerate(vectors[int(witness) - 1])])
    matrix = Matrix(F, rows)
    return [list(row) for row in matrix.row_space().basis()]


def build_matrix(F, powers, coordinate_classes, template_vectors, variable_count):
    entries = {}
    row_index = 0
    m = variable_count // K
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        members = [int(value) for value in coord["members"]]
        basis_rows = row_basis(F, template_vectors, members)
        for diff in basis_rows:
            for block in range(m):
                if diff[block] == 0:
                    continue
                start = block * K
                for degree in range(K):
                    entries[(row_index, start + degree)] = (
                        entries.get((row_index, start + degree), F(0))
                        + diff[block] * powers[degree][pos]
                    )
            row_index += 1
    return Matrix(F, row_index, variable_count, entries, sparse=True)


def pair_projection_coefficients(F, vector_row, template_vectors, pair):
    left, right = int(pair[0]), int(pair[1])
    m = len(template_vectors[0])
    diff = [F(template_vectors[left - 1][idx]) - F(template_vectors[right - 1][idx]) for idx in range(m)]
    coeffs = [F(0) for _ in range(K)]
    for block in range(m):
        start = block * K
        for degree in range(K):
            coeffs[degree] += diff[block] * vector_row[start + degree]
    return coeffs


def pair_projection_test(F, basis, template_vectors, exact_rank_limit=256):
    ranks = {}
    forced = []
    exact_ranks = len(basis) <= exact_rank_limit
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            rows = []
            has_nonzero = False
            for vector_row in basis:
                coeffs = pair_projection_coefficients(F, vector_row, template_vectors, [left, right])
                if any(value != 0 for value in coeffs):
                    has_nonzero = True
                if exact_ranks:
                    rows.append(coeffs)
            rank = int(Matrix(F, rows).rank()) if exact_ranks and rows else (1 if has_nonzero else 0)
            label = "P%s%s" % (left, right)
            ranks[label] = rank
            if rank == 0:
                forced.append([left, right])
    return {
        "forced_equal_pairs": forced,
        "min_projection_rank": min(ranks.values()) if ranks else None,
        "projection_rank_by_pair": ranks,
    }


def codeword_coefficients(F, vector_row, template_vectors):
    m = len(template_vectors[0])
    codewords = []
    for witness in range(LIST_SIZE):
        coeffs = [F(0) for _ in range(K)]
        for block in range(m):
            scalar = F(template_vectors[witness][block])
            start = block * K
            for degree in range(K):
                coeffs[degree] += scalar * vector_row[start + degree]
        codewords.append(coeffs)
    return codewords


def evaluate_candidate(F, powers, vector_row, coordinate_classes, template_vectors):
    coeffs = codeword_coefficients(F, vector_row, template_vectors)
    values = []
    for witness in range(LIST_SIZE):
        witness_values = []
        for pos in range(N):
            acc = F(0)
            for degree in range(K):
                acc += coeffs[witness][degree] * powers[degree][pos]
            witness_values.append(acc)
        values.append(witness_values)
    r_values = []
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        anchor = min(int(value) for value in coord["members"])
        r_values.append(values[anchor - 1][pos])
    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [hash_payload([str(value) for value in row]) for row in coeffs]
    return {
        "agreement_vector": agreements,
        "exact_max_min": min(agreements),
        "seven_distinct": len(set(codeword_hashes)) == LIST_SIZE,
        "received_word_hash": hash_payload([str(value) for value in r_values]),
        "codeword_hashes": codeword_hashes,
    }


def deterministic_candidates(F, basis, sample_limit):
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
    idx = 1
    while len(candidates) < sample_limit:
        acc = parent.zero()
        for basis_idx, row in enumerate(basis):
            acc += (alpha ** ((idx + 1) * (basis_idx + 1))) * row
        candidates.append(acc)
        idx += 1
    return candidates[:sample_limit]


def audit(sample_limit=24, rank_only=False):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    q, F, H = exact_field_context()
    powers = precompute_powers(F, H)
    proxy = record["proxy_candidate"]
    matrix = build_matrix(
        F,
        powers,
        record["coordinate_classes"],
        proxy["template_vectors"],
        int(proxy["variable_count"]),
    )
    rank = int(matrix.rank())
    nullity = int(matrix.ncols() - rank)
    record["exact_audit"].update(
        {
            "field": "GF(17^32)",
            "field_denominator": str(q),
            "H_order": len(H),
            "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
            "rank": rank,
            "nullity": nullity,
            "best_failure_mode": "LOWRANK_EXACT_NULLITY_POSITIVE" if nullity > 0 else "LOWRANK_EXACT_FULL_RANK",
        }
    )
    record["proof_status"] = (
        "CANDIDATE / LOWRANK_EXACT_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if nullity > 0
        else "EXACT_EXTRACTION_NO_A327 / LOWRANK_EXACT_FULL_RANK / PARTIAL / EXPERIMENTAL"
    )
    if nullity <= 0 or rank_only:
        return record

    basis = matrix.right_kernel().basis()
    projection = pair_projection_test(F, basis, proxy["template_vectors"])
    record["pair_projection_test"].update(projection)
    if projection["forced_equal_pairs"]:
        record["exact_audit"]["best_failure_mode"] = "LOWRANK_FORCED_PAIR_EQUALITY"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        return record
    record["exact_audit"]["best_failure_mode"] = "LOWRANK_PAIR_PROJECTIONS_CLEAR"
    record["proof_status"] = "CANDIDATE / LOWRANK_PAIR_PROJECTIONS_CLEAR / PARTIAL / EXPERIMENTAL"
    for vector_row in deterministic_candidates(F, basis, sample_limit):
        record["exact_audit"]["exact_vectors_constructed"] += 1
        evaluated = evaluate_candidate(F, powers, vector_row, record["coordinate_classes"], proxy["template_vectors"])
        if evaluated["seven_distinct"] and evaluated["exact_max_min"] >= TARGET_AGREEMENT:
            record["candidate"].update(
                {
                    "constructed": True,
                    "seven_distinct": True,
                    "agreement_vector": evaluated["agreement_vector"],
                    "received_word_hash": evaluated["received_word_hash"],
                    "codeword_hashes": evaluated["codeword_hashes"],
                }
            )
            record["exact_audit"]["best_failure_mode"] = "LOWRANK_EXACT_CANDIDATE"
            record["proof_status"] = "PROOF_RECORD / LOWRANK_EXACT_CANDIDATE / EXPERIMENTAL"
            return record
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--rank-only", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=24)
    args = parser.parse_args()
    record = audit(sample_limit=args.sample_limit, rank_only=args.rank_only)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        exact = record["exact_audit"]
        print("SAGE_AUDIT_M1_A327_LOWRANK_TEMPLATE_EXACT_AUDIT_OK")
        print("matrix_shape: %s" % exact["matrix_shape"])
        print("rank: %s" % exact["rank"])
        print("nullity: %s" % exact["nullity"])
        print("best_failure_mode: %s" % exact["best_failure_mode"])


if __name__ == "__main__":
    main()
