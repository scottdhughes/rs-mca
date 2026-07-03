#!/usr/bin/env sage
"""Exact/proxy audit for M1 a=327 low-rank template selected-class designs."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
PROXY_PRIME = 12289
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_selected_class_search.json")


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


def proxy_field_context():
    F = GF(PROXY_PRIME)
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((PROXY_PRIME - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return F, H


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


def build_matrix(F, powers, candidate):
    vectors = candidate["template_vectors"]
    m = int(candidate["template_dimension"])
    entries = {}
    row_index = 0
    for coord in sorted(candidate["coordinate_classes"], key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        basis_rows = row_basis(F, vectors, [int(value) for value in coord["members"]])
        for coeffs in basis_rows:
            for block in range(m):
                if coeffs[block] == 0:
                    continue
                start = block * K
                for degree in range(K):
                    entries[(row_index, start + degree)] = (
                        entries.get((row_index, start + degree), F(0))
                        + coeffs[block] * powers[degree][pos]
                    )
            row_index += 1
    return Matrix(F, row_index, m * K, entries, sparse=True)


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
            start = block * K
            scalar = F(template_vectors[witness][block])
            for degree in range(K):
                coeffs[degree] += scalar * vector_row[start + degree]
        codewords.append(coeffs)
    return codewords


def evaluate_candidate(F, H, powers, vector_row, candidate):
    coeffs = codeword_coefficients(F, vector_row, candidate["template_vectors"])
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
    for coord in sorted(candidate["coordinate_classes"], key=lambda row: int(row["position"])):
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
        "codeword_hashes": codeword_hashes,
        "received_word_hash": hash_payload([str(value) for value in r_values]),
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


def rank_candidate(F, H, candidate):
    powers = precompute_powers(F, H)
    matrix = build_matrix(F, powers, candidate)
    rank = int(matrix.rank())
    nullity = int(matrix.ncols() - rank)
    return matrix, powers, rank, nullity


def audit(sample_limit=24, run_exact=False):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    candidates = record["lowrank_template_search"].get("candidates", [])
    if not candidates:
        record["exact_audit"]["best_failure_mode"] = "LOWRANK_TEMPLATE_SUPPORT_FAIL"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        return record

    Fp, Hp = proxy_field_context()
    audited = []
    for candidate in candidates:
        _matrix, _powers, rank, nullity = rank_candidate(Fp, Hp, candidate)
        row = dict(candidate)
        row["proxy_rank"] = rank
        row["proxy_nullity"] = nullity
        row["best_failure_mode"] = "LOWRANK_TEMPLATE_PROXY_POSITIVE" if nullity > 0 else "LOWRANK_TEMPLATE_PROXY_FULL_RANK"
        audited.append(row)

    best = max(
        audited,
        key=lambda row: (
            row["proxy_nullity"],
            row["cost_margin"],
            min(row["pair7_counts"]),
            -row["max_pair_count"],
            -row["template_dimension"],
        ),
    )
    positive = [row for row in audited if int(row["proxy_nullity"]) > 0]
    search = record["lowrank_template_search"]
    search["candidates"] = audited
    search["proxy_positive_candidates"] = len(positive)
    search["best_template_dimension"] = best["template_dimension"]
    search["best_effective_cost"] = best["total_effective_cost"]
    search["best_variable_count"] = best["variable_count"]
    search["best_proxy_rank"] = best["proxy_rank"]
    search["best_proxy_nullity"] = best["proxy_nullity"]
    search["best_failure_mode"] = best["best_failure_mode"]
    record["best_candidate"] = best

    if int(best["proxy_nullity"]) <= 0:
        record["exact_audit"].update({"run": False, "best_failure_mode": "LOWRANK_TEMPLATE_PROXY_FULL_RANK"})
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        return record
    if not run_exact:
        record["exact_audit"].update({"run": False, "best_failure_mode": "LOWRANK_TEMPLATE_PROXY_POSITIVE"})
        record["proof_status"] = "CANDIDATE / LOWRANK_TEMPLATE_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
        return record

    q, F, H = exact_field_context()
    matrix, powers, rank, nullity = rank_candidate(F, H, best)
    search["exact_audits"] = 1
    search["best_exact_nullity"] = nullity
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
    if nullity <= 0:
        record["exact_audit"]["best_failure_mode"] = "LOWRANK_TEMPLATE_EXACT_NULLITY_ZERO"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_EXACT_NULLITY_ZERO / PARTIAL / EXPERIMENTAL"
        return record

    basis = matrix.right_kernel().basis()
    projection = pair_projection_test(F, basis, best["template_vectors"])
    record["exact_audit"].update(projection)
    if projection["forced_equal_pairs"]:
        record["exact_audit"]["best_failure_mode"] = "LOWRANK_TEMPLATE_FORCED_PAIR_EQUALITY"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        return record

    for vector_row in deterministic_candidates(F, basis, sample_limit):
        evaluated = evaluate_candidate(F, H, powers, vector_row, best)
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
            record["exact_audit"]["best_failure_mode"] = "LOWRANK_TEMPLATE_EXACT_CANDIDATE"
            record["proof_status"] = "PROOF_RECORD / LOWRANK_TEMPLATE_EXACT_CANDIDATE / EXPERIMENTAL"
            return record

    record["exact_audit"]["best_failure_mode"] = "LOWRANK_TEMPLATE_FORCED_PAIR_EQUALITY"
    record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=24)
    parser.add_argument("--exact", action="store_true", help="continue from proxy-positive candidates to GF(17^32)")
    args = parser.parse_args()
    record = audit(sample_limit=args.sample_limit, run_exact=args.exact)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        exact = record["exact_audit"]
        search = record["lowrank_template_search"]
        print("SAGE_AUDIT_M1_A327_LOWRANK_TEMPLATE_SELECTED_CLASS_SEARCH_OK")
        print("proxy_positive_candidates: %s" % search["proxy_positive_candidates"])
        print("best_proxy_rank: %s" % search["best_proxy_rank"])
        print("best_proxy_nullity: %s" % search["best_proxy_nullity"])
        print("exact_run: %s" % exact["run"])
        print("best_failure_mode: %s" % (exact["best_failure_mode"] or search["best_failure_mode"]))


if __name__ == "__main__":
    main()
