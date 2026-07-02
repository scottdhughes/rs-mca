#!/usr/bin/env sage
"""Exact GF(17^32) tree-divisibility audit for M1 a=327 selected classes."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
DATA_PATH = Path("experimental/data/m1_a327_selected_class_tree_divisibility_lift.json")
SOURCE_QUOTIENT_DATA = Path("experimental/data/m1_a327_selected_class_quotient_nullspace_lift.json")


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


def pair_label(left, right):
    left, right = sorted((int(left), int(right)))
    return "P%s%s" % (left, right)


def parse_pair_label(label):
    return int(label[1]), int(label[2])


def orient_tree(edges):
    adjacency = {node: [] for node in range(1, LIST_SIZE + 1)}
    for left, right in edges:
        left = int(left)
        right = int(right)
        adjacency[left].append(right)
        adjacency[right].append(left)
    parent = {1: None}
    edge_parent_child = {}
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for neighbor in adjacency[node]:
            if neighbor in parent:
                continue
            parent[neighbor] = node
            edge_parent_child[pair_label(node, neighbor)] = [node, neighbor]
            queue.append(neighbor)
    if len(parent) != LIST_SIZE:
        raise RuntimeError("tree is not connected")
    path_coeffs = {1: {}}
    for node in range(2, LIST_SIZE + 1):
        chain = []
        current = node
        while current != 1:
            previous = parent[current]
            label = pair_label(previous, current)
            chain.append(label)
            current = previous
        coeffs = {}
        for label in chain:
            coeffs[label] = coeffs.get(label, 0) + 1
        path_coeffs[node] = coeffs
    return edge_parent_child, path_coeffs


def pair_path_coeffs(path_coeffs, left, right):
    coeffs = {}
    for label, value in path_coeffs[int(left)].items():
        coeffs[label] = coeffs.get(label, 0) + value
    for label, value in path_coeffs[int(right)].items():
        coeffs[label] = coeffs.get(label, 0) - value
    return {label: value for label, value in coeffs.items() if value}


def tree_variable_blocks(tree_edges, pair_counts):
    blocks = {}
    cursor = 0
    for edge in tree_edges:
        label = pair_label(edge[0], edge[1])
        qdeg = K - int(pair_counts[label])
        if qdeg <= 0:
            raise RuntimeError("nonpositive quotient degree for %s" % label)
        blocks[label] = {
            "start": cursor,
            "q_degree_bound": qdeg,
            "pair_count": int(pair_counts[label]),
        }
        cursor += qdeg
    return blocks, cursor


def z_data(F, H, pair_sets, tree_labels):
    R = PolynomialRing(F, "x")
    x = R.gen()
    out = {}
    for label in tree_labels:
        poly = R(1)
        for pos in pair_sets[label]:
            poly *= x - H[int(pos)]
        coeffs = [F(value) for value in poly.list()]
        evals = [poly(value) for value in H]
        out[label] = {
            "degree": int(poly.degree()),
            "coeffs": coeffs,
            "evals": evals,
            "poly_hash": hash_payload([str(value) for value in coeffs]),
        }
    return out


def build_tree_matrix(F, powers, pair_sets, tree_spec, pair_counts):
    tree_edges = tree_spec["edges"]
    tree_labels = tree_spec["edge_labels"]
    blocks, ncols = tree_variable_blocks(tree_edges, pair_counts)
    _orientation, path_coeffs = orient_tree(tree_edges)
    z = z_data(F, [powers[1][pos] for pos in range(N)], pair_sets, tree_labels)

    entries = {}
    row_index = 0
    for non_tree_label in tree_spec["non_tree_edge_labels"]:
        left, right = parse_pair_label(non_tree_label)
        path = pair_path_coeffs(path_coeffs, left, right)
        for pos in pair_sets[non_tree_label]:
            pos = int(pos)
            for label, sign_int in path.items():
                block = blocks[label]
                z_eval = z[label]["evals"][pos]
                if z_eval == 0:
                    continue
                sign = F(sign_int)
                start = block["start"]
                for degree in range(block["q_degree_bound"]):
                    entries[(row_index, start + degree)] = entries.get((row_index, start + degree), F(0)) + sign * z_eval * powers[degree][pos]
            row_index += 1
    return Matrix(F, row_index, ncols, entries, sparse=True), blocks, path_coeffs, z


def edge_polynomial_coeffs(F, vector_row, label, block, z):
    coeffs = [F(0) for _ in range(K)]
    start = block["start"]
    z_coeffs = z[label]["coeffs"]
    for q_degree in range(block["q_degree_bound"]):
        q_coeff = vector_row[start + q_degree]
        if q_coeff == 0:
            continue
        for z_degree, z_coeff in enumerate(z_coeffs):
            coeffs[q_degree + z_degree] += q_coeff * z_coeff
    return coeffs


def pair_polynomial_coeffs(F, vector_row, pair, blocks, path_coeffs, z):
    left, right = pair
    path = pair_path_coeffs(path_coeffs, left, right)
    coeffs = [F(0) for _ in range(K)]
    for label, sign_int in path.items():
        sign = F(sign_int)
        edge_coeffs = edge_polynomial_coeffs(F, vector_row, label, blocks[label], z)
        for degree in range(K):
            coeffs[degree] += sign * edge_coeffs[degree]
    return coeffs


def pair_projection_test(F, basis, blocks, path_coeffs, z, exact_rank_limit=256):
    projection_rank_by_pair = {}
    projection_results = []
    forced_equal_pairs = []
    exact_ranks = len(basis) <= exact_rank_limit
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            label = pair_label(left, right)
            rows = []
            has_nonzero = False
            for vector_row in basis:
                coeffs = pair_polynomial_coeffs(F, vector_row, [left, right], blocks, path_coeffs, z)
                if any(value != 0 for value in coeffs):
                    has_nonzero = True
                if exact_ranks:
                    rows.append(coeffs)
            rank = int(Matrix(F, rows).rank()) if exact_ranks and rows else (1 if has_nonzero else 0)
            forced_equal = rank == 0
            projection_rank_by_pair[label] = rank
            if forced_equal:
                forced_equal_pairs.append([left, right])
            projection_results.append(
                {
                    "pair": [left, right],
                    "pair_label": label,
                    "projection_rank": rank,
                    "projection_rank_exact": bool(exact_ranks),
                    "forced_equal": forced_equal,
                }
            )
    return {
        "pairs_tested": 21,
        "forced_equal_pairs": forced_equal_pairs,
        "min_projection_rank": min(projection_rank_by_pair.values()) if projection_rank_by_pair else None,
        "projection_rank_by_pair": projection_rank_by_pair,
        "projection_results": projection_results,
    }


def codeword_coefficients(F, vector_row, blocks, path_coeffs, z):
    edge_coeff_cache = {
        label: edge_polynomial_coeffs(F, vector_row, label, block, z)
        for label, block in blocks.items()
    }
    codewords = [[F(0) for _ in range(K)] for _ in range(LIST_SIZE)]
    for witness in range(2, LIST_SIZE + 1):
        for label, sign_int in path_coeffs[witness].items():
            sign = F(sign_int)
            edge_coeffs = edge_coeff_cache[label]
            for degree in range(K):
                codewords[witness - 1][degree] += sign * edge_coeffs[degree]
    return codewords


def evaluate_candidate(F, powers, vector_row, blocks, path_coeffs, z, coordinate_classes):
    coeffs = codeword_coefficients(F, vector_row, blocks, path_coeffs, z)
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
    for row in coordinate_classes:
        pos = int(row["position"])
        anchor = min(int(value) for value in row["members"])
        r_values.append(values[anchor - 1][pos])
    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [hash_payload([str(value) for value in row]) for row in coeffs]
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


def deterministic_candidates(F, basis, sample_limit):
    if not basis or sample_limit <= 0:
        return []
    parent = basis[0].parent()
    generator = F.multiplicative_generator()
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
            acc += (generator ** ((idx + 1) * (basis_idx + 1))) * row
        candidates.append(acc)
        idx += 1
    return candidates[:sample_limit]


def construct_candidate(F, powers, basis, blocks, path_coeffs, z, coordinate_classes, sample_limit):
    samples = []
    seen = set()
    for sample_index, vector_row in enumerate(deterministic_candidates(F, basis, sample_limit)):
        vector_hash = hash_payload([str(value) for value in vector_row[: min(128, len(vector_row))]])
        if vector_hash in seen:
            continue
        seen.add(vector_hash)
        evaluation = evaluate_candidate(F, powers, vector_row, blocks, path_coeffs, z, coordinate_classes)
        evaluation["sample_index"] = sample_index
        evaluation["vector_hash"] = vector_hash
        samples.append(evaluation)
        if evaluation["seven_distinct"] and evaluation["exact_max_min"] >= TARGET_AGREEMENT:
            return evaluation, samples
    best = None if not samples else max(samples, key=lambda row: (row["seven_distinct"], row["exact_max_min"]))
    return best, samples


def classify(nullity, projection, candidate):
    if nullity <= 0:
        return "TREE_DIVISIBILITY_NULLITY_ZERO"
    if projection["forced_equal_pairs"]:
        return "TREE_DIVISIBILITY_FORCED_PAIR_EQUALITY"
    if candidate is None:
        return "TREE_DIVISIBILITY_DEGENERATE_SAMPLE"
    if candidate["seven_distinct"] and candidate["exact_max_min"] >= TARGET_AGREEMENT:
        return "TREE_DIVISIBILITY_EXACT_CANDIDATE"
    return "TREE_DIVISIBILITY_DEGENERATE_SAMPLE"


def audit(tree_name, sample_limit):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    with SOURCE_QUOTIENT_DATA.open() as handle:
        source = json.load(handle)
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    trees = record["tree_divisibility"]["trees_tested"]
    if tree_name is None:
        tree_name = record["tree_divisibility"]["best_tree_name"]
    tree_spec = next(row for row in trees if row["tree_name"] == tree_name)
    pair_sets = record["thin_selected_hypergraph"]["pair_sets"]
    pair_counts = record["thin_selected_hypergraph"]["pair_counts"]
    matrix, blocks, path_coeffs, z = build_tree_matrix(F, powers, pair_sets, tree_spec, pair_counts)
    rank = int(matrix.rank())
    nrows, ncols = int(matrix.nrows()), int(matrix.ncols())
    nullity = ncols - rank
    basis = list(matrix.right_kernel().basis()) if nullity > 0 else []
    projection = {
        "pairs_tested": 21,
        "forced_equal_pairs": [],
        "min_projection_rank": None,
        "projection_rank_by_pair": None,
        "projection_results": [],
    }
    candidate = {
        "constructed": False,
        "seven_distinct": False,
        "agreement_vector": None,
        "received_word_hash": None,
        "codeword_hashes": None,
        "vector_hash": None,
        "sample_results": [],
    }
    best_sample = None
    if basis:
        projection = pair_projection_test(F, basis, blocks, path_coeffs, z)
        if not projection["forced_equal_pairs"]:
            coordinate_classes = source["thin_selected_hypergraph"]["coordinate_classes"]
            best_sample, samples = construct_candidate(
                F, powers, basis, blocks, path_coeffs, z, coordinate_classes, sample_limit
            )
            if best_sample is not None:
                candidate = {
                    "constructed": True,
                    "seven_distinct": bool(best_sample["seven_distinct"]),
                    "agreement_vector": best_sample["agreement_vector"],
                    "received_word_hash": best_sample["received_word_hash"],
                    "codeword_hashes": best_sample["codeword_hashes"],
                    "vector_hash": best_sample["vector_hash"],
                    "exact_max_min": best_sample["exact_max_min"],
                    "pair_equalities": best_sample["pair_equalities"],
                    "sample_results": samples,
                }
    failure_mode = classify(nullity, projection, best_sample)
    record["tree_divisibility"].update(
        {
            "best_tree_name": tree_spec["tree_name"],
            "best_tree_edges": tree_spec["edges"],
            "best_tree_edge_labels": tree_spec["edge_labels"],
            "tree_variable_count": ncols,
            "non_tree_equation_count": nrows,
            "matrix_shape": [nrows, ncols],
            "rank": rank,
            "nullity": nullity,
            "best_failure_mode": failure_mode,
            "field": "GF(17^32)",
            "field_denominator": str(q),
            "H_order": len(H),
            "tree_variable_blocks": blocks,
            "tree_z_hashes": {label: z[label]["poly_hash"] for label in z},
            "sample_limit": sample_limit,
        }
    )
    record["pair_projection_test"] = jsonable(projection)
    record["exact_candidate"] = jsonable(candidate)
    if failure_mode == "TREE_DIVISIBILITY_EXACT_CANDIDATE":
        record["proof_status"] = "PROOF_RECORD / TREE_DIVISIBILITY_EXACT_CANDIDATE / EXPERIMENTAL"
    else:
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / %s / PARTIAL / EXPERIMENTAL" % failure_mode
    return jsonable(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tree-name")
    parser.add_argument("--sample-limit", type=int, default=128)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = audit(args.tree_name, args.sample_limit)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        tree = record["tree_divisibility"]
        print("SAGE_AUDIT_M1_A327_SELECTED_CLASS_TREE_DIVISIBILITY_LIFT_OK")
        print("tree_name: %s" % tree["best_tree_name"])
        print("matrix_shape: %s" % tree["matrix_shape"])
        print("rank: %s" % tree["rank"])
        print("nullity: %s" % tree["nullity"])
        print("best_failure_mode: %s" % tree["best_failure_mode"])


if __name__ == "__main__":
    main()
