#!/usr/bin/env sage
"""Exact GF(17^32) audit for selected-class rank-defect candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path


P = 17
PROXY_PRIME = 12289
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
VARIABLES = (LIST_SIZE - 1) * K
QUOTIENT_EQUATIONS = LIST_SIZE * TARGET_AGREEMENT - N
DATA_PATH = Path("experimental/data/m1_a327_selected_class_rank_defect_search.json")


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


def proxy_field_context():
    F = GF(PROXY_PRIME)
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((PROXY_PRIME - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for _degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def block_start(witness_one_based):
    return (int(witness_one_based) - 2) * K


def build_quotient_matrix(F, powers, coordinate_classes):
    entries = {}
    row_index = 0
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        members = [int(value) for value in coord["members"]]
        anchor = min(members)
        for witness in members:
            if witness == anchor:
                continue
            if witness != 1:
                start = block_start(witness)
                for degree in range(K):
                    key = (row_index, start + degree)
                    entries[key] = entries.get(key, F(0)) + powers[degree][pos]
            if anchor != 1:
                start = block_start(anchor)
                for degree in range(K):
                    key = (row_index, start + degree)
                    entries[key] = entries.get(key, F(0)) - powers[degree][pos]
            row_index += 1
    return Matrix(F, row_index, VARIABLES, entries, sparse=True)


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
    results = {}
    forced_equal_pairs = []
    exact_ranks = len(basis) <= exact_rank_limit
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            rows = []
            has_nonzero = False
            for vector_row in basis:
                coeffs = projection_coefficients(vector_row, [left, right])
                if any(value != 0 for value in coeffs):
                    has_nonzero = True
                if exact_ranks:
                    rows.append(coeffs)
            rank = int(Matrix(F, rows).rank()) if exact_ranks and rows else (1 if has_nonzero else 0)
            label = "P%s%s" % (left, right)
            results[label] = rank
            if rank == 0:
                forced_equal_pairs.append([left, right])
    return {
        "forced_equal_pairs": forced_equal_pairs,
        "min_projection_rank": min(results.values()) if results else None,
        "projection_rank_by_pair": results,
    }


def coeff_hash(vector_row, witness_one_based):
    if int(witness_one_based) == 1:
        return hash_payload(["0"] * K)
    start = block_start(witness_one_based)
    return hash_payload([str(vector_row[start + degree]) for degree in range(K)])


def evaluate_candidate(F, powers, vector_row, coordinate_classes):
    values = [[F(0) for _ in range(N)]]
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
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        anchor = min(int(value) for value in coord["members"])
        r_values.append(values[anchor - 1][pos])
    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [coeff_hash(vector_row, witness) for witness in range(1, LIST_SIZE + 1)]
    return {
        "agreement_vector": agreements,
        "exact_max_min": min(agreements),
        "seven_distinct": len(set(codeword_hashes)) == LIST_SIZE,
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
            acc += (alpha ** ((sample_idx + 1) * (idx + 1))) * row
        candidates.append(acc)
        sample_idx += 1
    return candidates[:sample_limit]


def rank_candidate_over_field(F, H, coordinate_classes):
    powers = precompute_powers(F, H)
    matrix = build_quotient_matrix(F, powers, coordinate_classes)
    rank = int(matrix.rank())
    return matrix, powers, rank, int(matrix.ncols() - rank)


def audit(sample_limit=24):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    candidates = record["search"].get("candidates", [])
    if not candidates:
        record["exact_audit"]["best_failure_mode"] = "RANK_DEFECT_SUPPORT_FAIL"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / RANK_DEFECT_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        return record

    Fp, Hp = proxy_field_context()
    audited = []
    for candidate in candidates:
        _matrix, _powers, rank, nullity = rank_candidate_over_field(Fp, Hp, candidate["coordinate_classes"])
        updated = dict(candidate)
        updated["proxy_rank"] = rank
        updated["proxy_nullity"] = nullity
        updated["best_failure_mode"] = "RANK_DEFECT_PROXY_POSITIVE" if nullity > 0 else "RANK_DEFECT_PROXY_FULL_RANK"
        audited.append(updated)

    best = max(
        audited,
        key=lambda row: (
            row["proxy_nullity"],
            min(row["pair7_counts"]),
            -row["max_pair_count"],
            row["profile_id"],
            row["assignment_strategy"],
        ),
    )
    proxy_positive = [row for row in audited if int(row["proxy_nullity"]) > 0]
    record["search"]["candidates"] = audited
    record["best_candidate"] = best
    record["search"]["proxy_rank_defect_candidates"] = len(proxy_positive)
    record["search"]["best_proxy_rank"] = best["proxy_rank"]
    record["search"]["best_proxy_nullity"] = best["proxy_nullity"]
    record["search"]["best_failure_mode"] = best["best_failure_mode"]

    if int(best["proxy_nullity"]) <= 0:
        record["exact_audit"].update(
            {
                "run": False,
                "best_failure_mode": "RANK_DEFECT_PROXY_FULL_RANK",
            }
        )
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / RANK_DEFECT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        return record

    q, F, H = field_context()
    matrix, powers, rank, nullity = rank_candidate_over_field(F, H, best["coordinate_classes"])
    record["search"]["exact_rank_audits"] = 1
    record["search"]["best_exact_rank"] = rank
    record["search"]["best_exact_nullity"] = nullity
    record["search"]["positive_exact_nullity"] = 1 if nullity > 0 else 0
    record["exact_audit"].update(
        {
            "run": True,
            "field": "GF(17^32)",
            "field_denominator": str(q),
            "H_order": len(H),
            "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
            "rank": rank,
            "nullity": nullity,
        }
    )
    if nullity == 0:
        record["exact_audit"]["best_failure_mode"] = "RANK_DEFECT_EXACT_NULLITY_ZERO"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / RANK_DEFECT_EXACT_NULLITY_ZERO / PARTIAL / EXPERIMENTAL"
        return record

    basis = matrix.right_kernel().basis()
    projection = pair_projection_test(F, basis)
    record["exact_audit"].update(projection)
    if projection["forced_equal_pairs"]:
        record["exact_audit"]["best_failure_mode"] = "RANK_DEFECT_FORCED_PAIR_EQUALITY"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / RANK_DEFECT_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        return record

    for vector_row in deterministic_kernel_candidates(F, basis, sample_limit):
        candidate = evaluate_candidate(F, powers, vector_row, best["coordinate_classes"])
        if candidate["seven_distinct"] and candidate["exact_max_min"] >= TARGET_AGREEMENT:
            record["candidate"].update(
                {
                    "constructed": True,
                    "seven_distinct": True,
                    "agreement_vector": candidate["agreement_vector"],
                    "received_word_hash": candidate["received_word_hash"],
                    "codeword_hashes": candidate["codeword_hashes"],
                }
            )
            record["exact_audit"]["best_failure_mode"] = "RANK_DEFECT_EXACT_CANDIDATE"
            record["proof_status"] = "PROOF_RECORD / RANK_DEFECT_EXACT_CANDIDATE / EXPERIMENTAL"
            return record

    record["exact_audit"]["best_failure_mode"] = "RANK_DEFECT_FORCED_PAIR_EQUALITY"
    record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / RANK_DEFECT_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=24)
    args = parser.parse_args()
    record = audit(sample_limit=args.sample_limit)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        exact = record["exact_audit"]
        print("SAGE_AUDIT_M1_A327_SELECTED_CLASS_RANK_DEFECT_SEARCH_OK")
        print("run: %s" % exact["run"])
        print("rank: %s" % exact["rank"])
        print("nullity: %s" % exact["nullity"])
        print("best_failure_mode: %s" % exact["best_failure_mode"])


if __name__ == "__main__":
    main()
