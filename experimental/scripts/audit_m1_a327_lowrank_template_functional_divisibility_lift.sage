#!/usr/bin/env sage
"""Functional-divisibility lift for the mixed_rank6 M1 a=327 template."""

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
DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_functional_divisibility_lift.json")


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


def vanishing_coefficients(F, H, positions):
    coeffs = [F(1)]
    for pos in positions:
        root = H[int(pos)]
        updated = [F(0) for _ in range(len(coeffs) + 1)]
        for idx, value in enumerate(coeffs):
            updated[idx] -= root * value
            updated[idx + 1] += value
        coeffs = updated
    return coeffs


def build_functional_matrix(F, H, record):
    proxy = record["proxy_candidate"]
    m = int(proxy["template_dimension"])
    a_vars = int(proxy["variable_count"])
    q_offsets = {}
    total_vars = a_vars
    for row in record["functional_classes_detail"]:
        q_dim = int(row["quotient_variables"])
        if q_dim > 0:
            q_offsets[int(row["class_index"])] = total_vars
            total_vars += q_dim
    entries = {}
    row_index = 0
    for func_row in record["functional_classes_detail"]:
        functional = [F(value) for value in func_row["functional"]]
        positions = [int(value) for value in func_row["positions"]]
        q_dim = int(func_row["quotient_variables"])
        z_coeffs = vanishing_coefficients(F, H, positions) if q_dim > 0 else []
        q_offset = q_offsets.get(int(func_row["class_index"]))
        for degree in range(K):
            for block in range(m):
                if functional[block] != 0:
                    entries[(row_index, block * K + degree)] = (
                        entries.get((row_index, block * K + degree), F(0))
                        + functional[block]
                    )
            if q_dim > 0:
                for z_degree, z_coeff in enumerate(z_coeffs):
                    q_degree = degree - z_degree
                    if 0 <= q_degree < q_dim:
                        col = q_offset + q_degree
                        entries[(row_index, col)] = entries.get((row_index, col), F(0)) - z_coeff
            row_index += 1
    return Matrix(F, row_index, total_vars, entries, sparse=True)


def component_values_from_coefficients(F, powers, vector_row, m):
    values = []
    for block in range(m):
        block_values = []
        start = block * K
        for pos in range(N):
            acc = F(0)
            for degree in range(K):
                acc += vector_row[start + degree] * powers[degree][pos]
            block_values.append(acc)
        values.append(block_values)
    return values


def raw_row_violations(F, component_values, row_specs):
    violations = 0
    for spec in row_specs:
        pos = int(spec["position"])
        diff = [F(value) for value in spec["template_difference"]]
        acc = F(0)
        for block, scalar in enumerate(diff):
            if scalar != 0:
                acc += scalar * component_values[block][pos]
        if acc != 0:
            violations += 1
    return violations


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


def pair_projection_test(F, basis, template_vectors, a_vars, exact_rank_limit=256):
    ranks = {}
    forced = []
    exact_ranks = len(basis) <= exact_rank_limit
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            rows = []
            has_nonzero = False
            for vector_row in basis:
                coeffs = pair_projection_coefficients(F, vector_row[:a_vars], template_vectors, [left, right])
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


def audit(run_rank=False, sample_limit=24):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    _q, F, H = exact_field_context()
    powers = precompute_powers(F, H)
    matrix = build_functional_matrix(F, H, record)
    record["functional_divisibility"]["matrix_shape"] = [int(matrix.nrows()), int(matrix.ncols())]
    if not run_rank:
        return record
    rank = int(matrix.rank())
    nullity = int(matrix.ncols() - rank)
    record["functional_divisibility"]["rank"] = rank
    record["functional_divisibility"]["nullity"] = nullity
    if nullity <= 0:
        record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_NULLITY_ZERO"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / FUNC_DIV_NULLITY_ZERO / PARTIAL / EXPERIMENTAL"
        return record
    basis = matrix.right_kernel().basis()
    proxy = record["proxy_candidate"]
    a_vars = int(proxy["variable_count"])
    projection = pair_projection_test(F, basis, proxy["template_vectors"], a_vars)
    record["pair_projection_test"].update(projection)
    if projection["forced_equal_pairs"]:
        record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_FORCED_PAIR_EQUALITY"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / FUNC_DIV_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        return record
    for vector_row in deterministic_candidates(F, basis, sample_limit):
        a_part = vector_row[:a_vars]
        component_values = component_values_from_coefficients(F, powers, a_part, int(proxy["template_dimension"]))
        violations = raw_row_violations(F, component_values, record["row_specs"])
        if violations:
            record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_RAW_ROW_VIOLATION"
            record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / FUNC_DIV_RAW_ROW_VIOLATION / PARTIAL / EXPERIMENTAL"
            continue
        evaluated = evaluate_candidate(F, powers, a_part, record["coordinate_classes"], proxy["template_vectors"])
        if not evaluated["seven_distinct"]:
            record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_DEGENERATE_SAMPLE"
            record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / FUNC_DIV_DEGENERATE_SAMPLE / PARTIAL / EXPERIMENTAL"
            continue
        if evaluated["exact_max_min"] >= TARGET_AGREEMENT:
            record["candidate"].update(
                {
                    "constructed": True,
                    "seven_distinct": True,
                    "agreement_vector": evaluated["agreement_vector"],
                    "received_word_hash": evaluated["received_word_hash"],
                    "codeword_hashes": evaluated["codeword_hashes"],
                }
            )
            record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_EXACT_CANDIDATE"
            record["proof_status"] = "PROOF_RECORD / FUNC_DIV_EXACT_CANDIDATE / EXPERIMENTAL"
            return record
    if record["functional_divisibility"]["best_failure_mode"] is None:
        record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_DEGENERATE_SAMPLE"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / FUNC_DIV_DEGENERATE_SAMPLE / PARTIAL / EXPERIMENTAL"
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--rank", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=24)
    args = parser.parse_args()
    record = audit(run_rank=args.rank, sample_limit=args.sample_limit)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        func = record["functional_divisibility"]
        print("SAGE_AUDIT_M1_A327_FUNCTIONAL_DIVISIBILITY_OK")
        print("functional_classes: %s" % func["functional_classes"])
        print("matrix_shape: %s" % func["matrix_shape"])
        print("rank: %s" % func["rank"])
        print("nullity: %s" % func["nullity"])
        print("best_failure_mode: %s" % func["best_failure_mode"])


if __name__ == "__main__":
    main()
