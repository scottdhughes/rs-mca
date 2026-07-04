#!/usr/bin/env sage
"""Exact GF(17^32) audit for the cycleguard basis-quotient lift target."""

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
DATA_PATH = Path("experimental/data/m1_a327_cycleguard_stable_window_exact_audit.json")


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


def z_data(F, H, classes_by_index, basis_indices):
    R = PolynomialRing(F, "x")
    x = R.gen()
    out = {}
    for class_index in basis_indices:
        cls = classes_by_index[int(class_index)]
        poly = R(1)
        for pos in cls["positions"]:
            poly *= x - H[int(pos)]
        coeffs = [F(value) for value in poly.list()]
        coeffs.extend([F(0)] * (K - len(coeffs)))
        evals = [poly(value) for value in H]
        out[int(class_index)] = {
            "degree": int(poly.degree()),
            "coeffs": coeffs[:K],
            "evals": evals,
            "poly_hash": hash_payload([str(value) for value in coeffs[:K]]),
        }
    return out


def basis_blocks(classes_by_index, basis_indices):
    blocks = {}
    cursor = 0
    for slot, class_index in enumerate(basis_indices):
        support_size = int(classes_by_index[int(class_index)]["support_size"])
        q_degree = K - support_size
        if q_degree <= 0:
            raise RuntimeError("nonpositive q-degree for basis class %s" % class_index)
        blocks[int(class_index)] = {
            "basis_slot": slot,
            "start": cursor,
            "q_degree_bound": q_degree,
            "support_size": support_size,
        }
        cursor += q_degree
    return blocks, cursor


def build_basis_matrix(F, powers, record, profile):
    classes_by_index = {int(row["class_index"]): row for row in record["functional_classes_detail"]}
    basis_indices = [int(idx) for idx in profile["basis_class_indices"]]
    blocks, ncols = basis_blocks(classes_by_index, basis_indices)
    z = z_data(F, [powers[1][pos] for pos in range(N)], classes_by_index, basis_indices)
    entries = {}
    row_index = 0
    for constraint in profile["nonbasis_constraint_detail"]:
        cls = classes_by_index[int(constraint["class_index"])]
        coords = [F(value) for value in constraint["basis_coordinates"]]
        for pos in cls["positions"]:
            pos = int(pos)
            for basis_slot, class_index in enumerate(basis_indices):
                scalar = coords[basis_slot]
                if scalar == 0:
                    continue
                block = blocks[class_index]
                z_eval = z[class_index]["evals"][pos]
                if z_eval == 0:
                    continue
                start = block["start"]
                for degree in range(block["q_degree_bound"]):
                    entries[(row_index, start + degree)] = (
                        entries.get((row_index, start + degree), F(0))
                        + scalar * z_eval * powers[degree][pos]
                    )
            row_index += 1
    return Matrix(F, row_index, ncols, entries, sparse=True), blocks, z


def basis_value_coeffs(F, vector_row, class_index, block, z):
    coeffs = [F(0) for _ in range(K)]
    start = block["start"]
    z_coeffs = z[int(class_index)]["coeffs"]
    for q_degree in range(block["q_degree_bound"]):
        q_coeff = vector_row[start + q_degree]
        if q_coeff == 0:
            continue
        for z_degree, z_coeff in enumerate(z_coeffs):
            if q_degree + z_degree >= K:
                break
            coeffs[q_degree + z_degree] += q_coeff * z_coeff
    return coeffs


def all_basis_value_coeffs(F, vector_row, blocks, z):
    return {
        int(class_index): basis_value_coeffs(F, vector_row, int(class_index), block, z)
        for class_index, block in blocks.items()
    }


def reconstruct_a_coeffs(F, vector_row, record, profile, blocks, z):
    basis_indices = [int(idx) for idx in profile["basis_class_indices"]]
    basis_coeffs = all_basis_value_coeffs(F, vector_row, blocks, z)
    matrix = Matrix(F, [[F(value) for value in row] for row in profile["basis_functionals"]])
    a_coeffs = [[F(0) for _ in range(K)] for _ in range(len(profile["basis_functionals"]))]
    for degree in range(K):
        rhs = vector(F, [basis_coeffs[class_index][degree] for class_index in basis_indices])
        solution = matrix.solve_right(rhs)
        for component, value in enumerate(solution):
            a_coeffs[component][degree] = value
    return a_coeffs


def pair_projection_coeffs(F, vector_row, pair, record, profile, blocks, z):
    template = record["survivor"]["template_vectors"]
    left, right = int(pair[0]), int(pair[1])
    a_coeffs = reconstruct_a_coeffs(F, vector_row, record, profile, blocks, z)
    coeffs = [F(0) for _ in range(K)]
    for component in range(len(a_coeffs)):
        scalar = F(template[left - 1][component]) - F(template[right - 1][component])
        if scalar != 0:
            for degree in range(K):
                coeffs[degree] += scalar * a_coeffs[component][degree]
    return coeffs


def pair_projection_test(F, basis, record, profile, blocks, z, exact_rank_limit=128):
    projection_rank_by_pair = {}
    forced_equal_pairs = []
    exact_ranks = len(basis) <= exact_rank_limit
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            rows = []
            has_nonzero = False
            for vector_row in basis:
                coeffs = pair_projection_coeffs(F, vector_row, [left, right], record, profile, blocks, z)
                if any(value != 0 for value in coeffs):
                    has_nonzero = True
                if exact_ranks:
                    rows.append(coeffs)
            rank = int(Matrix(F, rows).rank()) if exact_ranks and rows else (1 if has_nonzero else 0)
            label = "P%s%s" % (left, right)
            projection_rank_by_pair[label] = rank
            if rank == 0:
                forced_equal_pairs.append([left, right])
    return {
        "pairs_tested": 21,
        "forced_equal_pairs": forced_equal_pairs,
        "min_projection_rank": min(projection_rank_by_pair.values()) if projection_rank_by_pair else None,
        "projection_rank_by_pair": projection_rank_by_pair,
    }


def codeword_coefficients(F, a_coeffs, template_vectors):
    codewords = []
    for witness in range(LIST_SIZE):
        coeffs = [F(0) for _ in range(K)]
        for component in range(len(a_coeffs)):
            scalar = F(template_vectors[witness][component])
            if scalar == 0:
                continue
            for degree in range(K):
                coeffs[degree] += scalar * a_coeffs[component][degree]
        codewords.append(coeffs)
    return codewords


def evaluate_candidate(F, powers, vector_row, record, profile, blocks, z):
    a_coeffs = reconstruct_a_coeffs(F, vector_row, record, profile, blocks, z)
    codewords = codeword_coefficients(F, a_coeffs, record["survivor"]["template_vectors"])
    values = []
    for witness in range(LIST_SIZE):
        witness_values = []
        for pos in range(N):
            acc = F(0)
            for degree in range(K):
                acc += codewords[witness][degree] * powers[degree][pos]
            witness_values.append(acc)
        values.append(witness_values)
    r_values = [None for _ in range(N)]
    raw_violations = 0
    for coord in sorted(record["coordinate_classes"], key=lambda row: int(row["position"])):
        pos = int(coord["position"])
        members = [int(value) for value in coord["members"]]
        anchor = min(members)
        r_values[pos] = values[anchor - 1][pos]
        for witness in members:
            if values[witness - 1][pos] != r_values[pos]:
                raw_violations += 1
    agreements = [
        sum(1 for pos in range(N) if values[witness][pos] == r_values[pos])
        for witness in range(LIST_SIZE)
    ]
    codeword_hashes = [hash_payload([str(value) for value in row]) for row in codewords]
    return {
        "agreement_vector": agreements,
        "exact_max_min": min(agreements),
        "seven_distinct": len(set(codeword_hashes)) == LIST_SIZE,
        "raw_row_violations": raw_violations,
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


def audit(sample_limit=16, rank_only=False):
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    q, F, H = exact_field_context()
    powers = precompute_powers(F, H)
    if not record["basis_profiles"]:
        record["basis_quotient_audit"]["best_failure_mode"] = "CYCLEG_EXACT_NO_BASIS_PROFILE"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_NO_BASIS_PROFILE / PARTIAL / EXPERIMENTAL"
        return record
    profile = record["basis_profiles"][0]
    matrix, blocks, z = build_basis_matrix(F, powers, record, profile)
    rank = int(matrix.rank())
    nullity = int(matrix.ncols() - rank)
    record["basis_quotient_audit"].update(
        {
            "best_basis_id": profile["basis_id"],
            "best_basis_support_sizes": profile["basis_support_sizes"],
            "best_q_variable_count": profile["q_variable_count"],
            "best_matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
            "best_rank": rank,
            "best_nullity": nullity,
            "field": "GF(17^32)",
            "field_denominator": str(q),
            "H_order": len(H),
            "best_failure_mode": "CYCLEG_EXACT_NULLITY_POSITIVE" if nullity > 0 else "CYCLEG_EXACT_NULLITY_ZERO",
        }
    )
    record["proof_status"] = (
        "CANDIDATE / CYCLEG_EXACT_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if nullity > 0
        else "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_NULLITY_ZERO / PARTIAL / EXPERIMENTAL"
    )
    if nullity <= 0 or rank_only:
        return record
    basis = matrix.right_kernel().basis()
    projection = pair_projection_test(F, basis, record, profile, blocks, z)
    record["pair_projection_test"].update(projection)
    if projection["forced_equal_pairs"]:
        record["basis_quotient_audit"]["best_failure_mode"] = "CYCLEG_EXACT_FORCED_PAIR_EQUALITY"
        record["proof_status"] = "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        return record
    record["basis_quotient_audit"]["best_failure_mode"] = "CYCLEG_EXACT_PAIR_PROJECTIONS_CLEAR"
    record["proof_status"] = "CANDIDATE / CYCLEG_EXACT_PAIR_PROJECTIONS_CLEAR / PARTIAL / EXPERIMENTAL"
    for vector_row in deterministic_candidates(F, basis, sample_limit):
        evaluated = evaluate_candidate(F, powers, vector_row, record, profile, blocks, z)
        if (
            evaluated["raw_row_violations"] == 0
            and evaluated["seven_distinct"]
            and evaluated["exact_max_min"] >= TARGET_AGREEMENT
        ):
            record["candidate"].update(
                {
                    "constructed": True,
                    "seven_distinct": True,
                    "agreement_vector": evaluated["agreement_vector"],
                    "received_word_hash": evaluated["received_word_hash"],
                    "codeword_hashes": evaluated["codeword_hashes"],
                }
            )
            record["basis_quotient_audit"]["best_failure_mode"] = "CYCLEG_EXACT_CANDIDATE"
            record["proof_status"] = "PROOF_RECORD / CYCLEG_EXACT_CANDIDATE / EXPERIMENTAL"
            return record
    record["basis_quotient_audit"]["best_failure_mode"] = "CYCLEG_EXACT_DEGENERATE_SAMPLE"
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--rank-only", action="store_true")
    parser.add_argument("--sample-limit", type=int, default=16)
    args = parser.parse_args()
    record = audit(sample_limit=args.sample_limit, rank_only=args.rank_only)
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        audit_row = record["basis_quotient_audit"]
        print("SAGE_AUDIT_M1_A327_CYCLEGUARD_STABLE_WINDOW_EXACT_AUDIT_OK")
        print("best_matrix_shape: %s" % audit_row["best_matrix_shape"])
        print("best_rank: %s" % audit_row["best_rank"])
        print("best_nullity: %s" % audit_row["best_nullity"])
        print("best_failure_mode: %s" % audit_row["best_failure_mode"])


if __name__ == "__main__":
    main()
