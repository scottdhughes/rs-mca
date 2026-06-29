#!/usr/bin/env sage
"""Sage audit for the M1 a=327 random low-degree witness search."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_random_lowdegree_list_witness_search.py")
DATA_PATH = Path("experimental/data/m1_a327_random_lowdegree_list_witness_search.json")


def load_scanner():
    spec = importlib.util.spec_from_file_location("random_lowdegree_scanner", SCANNER_PATH)
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


def eval_terms(F, powers, terms):
    values = [F(0) for _ in range(N)]
    for term in terms:
        coeff = F(term["coeff_mod_17"])
        degree = int(term["degree"])
        row = powers[degree]
        for pos in range(N):
            values[pos] += coeff * row[pos]
    return values


def root_locator_values(F, H, positions):
    root_positions = {int(pos) for pos in positions}
    roots = [H[pos] for pos in root_positions]
    values = []
    zero = F(0)
    one = F(1)
    for pos, point in enumerate(H):
        if pos in root_positions:
            values.append(zero)
            continue
        acc = one
        for root in roots:
            acc *= point - root
        values.append(acc)
    return values


def max_term_degree(terms):
    return max(int(term["degree"]) for term in terms) if terms else -1


def build_value_rows(desc, F, H, powers):
    family = desc["family"]
    if family == "random_sparse_subfield":
        values = [eval_terms(F, powers, witness["terms"]) for witness in desc["witnesses"]]
        degrees = [max_term_degree(witness["terms"]) for witness in desc["witnesses"]]
        return values, degrees

    if family == "common_root_core":
        locator = root_locator_values(F, H, desc["root_positions"])
        values = []
        degrees = []
        for residual_terms in desc["residuals"]:
            residual = eval_terms(F, powers, residual_terms)
            values.append([locator[pos] * residual[pos] for pos in range(N)])
            degrees.append(int(desc["root_size"]) + max_term_degree(residual_terms))
        return values, degrees

    if family == "monomial_orbit":
        degree = int(desc["degree"])
        values = [
            [F(scale) * powers[degree][pos] + F(shift) for pos in range(N)]
            for scale, shift in zip(desc["scales_mod_17"], desc["shifts_mod_17"])
        ]
        return values, [degree for _ in range(LIST_SIZE)]

    if family == "clustered_root_core":
        locator = root_locator_values(F, H, desc["common_root_positions"])
        cluster_residuals = [
            eval_terms(F, powers, terms) for terms in desc["cluster_residuals"]
        ]
        values = []
        degrees = []
        for witness, noise_terms in enumerate(desc["witness_noise"]):
            cluster_index = 0 if witness < 4 else 1
            noise = eval_terms(F, powers, noise_terms)
            combined = [
                cluster_residuals[cluster_index][pos] + F(witness + 1) * noise[pos]
                for pos in range(N)
            ]
            values.append([locator[pos] * combined[pos] for pos in range(N)])
            degrees.append(
                int(desc["common_root_size"])
                + max(max_term_degree(desc["cluster_residuals"][cluster_index]), max_term_degree(noise_terms))
            )
        return values, degrees

    raise ValueError("unknown family %s" % family)


def value_class_rows(values):
    rows = []
    for pos in range(N):
        classes = {}
        for idx, witness_values in enumerate(values):
            value = witness_values[pos]
            classes.setdefault(value, 0)
            classes[value] = int(classes[value]) | (1 << idx)
        rows.append([int(mask) for mask in classes.values()])
    return rows


def capacity_upper_bound(class_rows):
    total = 0
    histogram = {}
    for masks in class_rows:
        largest = max(mask.bit_count() for mask in masks)
        total += largest
        histogram[str(largest)] = histogram.get(str(largest), 0) + 1
    return total // LIST_SIZE, total, dict(sorted(histogram.items(), key=lambda item: int(item[0])))


def evaluate_candidate(desc, F, H, powers):
    values, degrees = build_value_rows(desc, F, H, powers)
    assert len(values) == LIST_SIZE
    assert all(degree < K for degree in degrees)
    value_hashes = [hash_payload([str(value) for value in row]) for row in values]
    assert len(set(value_hashes)) == LIST_SIZE

    rows = value_class_rows(values)
    upper, total_capacity, largest_histogram = capacity_upper_bound(rows)
    return {
        "candidate_id": desc["candidate_id"],
        "family": desc["family"],
        "max_degree": max(degrees),
        "degree_vector": degrees,
        "distinct_codewords": True,
        "capacity_total": total_capacity,
        "capacity_upper_bound": upper,
        "largest_class_histogram": largest_histogram,
        "solver_status": "SKIPPED_BY_CAPACITY_UPPER_BOUND"
        if upper < TARGET_AGREEMENT
        else "CAPACITY_GATE_REQUIRES_ASSIGNMENT_SOLVER",
        "codeword_hash": hash_payload(value_hashes),
    }


def exact_record():
    scanner = load_scanner()
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    descriptors = scanner.candidate_descriptors()
    results = [evaluate_candidate(desc, F, H, powers) for desc in descriptors]
    record = scanner.build_record(exact_results=results)
    record["field_denominator"] = str(q)
    record["subgroup_order"] = len(H)
    record["sage_audit"] = {
        "gf": "GF(17^32)",
        "subgroup_order": len(H),
        "degree_bound": K,
        "candidate_descriptor_hash": scanner.hash_payload(descriptors),
        "candidate_result_hash": hash_payload(results),
        "status": "SAGE_EVALUATED_CAPACITY_GATE",
    }
    return jsonable(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()

    record = exact_record()
    best = record["exact_evaluation"]["best"]
    assert record["proof_status"] in {"TESTED_TUPLES_NO_A327", "CANDIDATE"}
    if record["proof_status"] == "TESTED_TUPLES_NO_A327":
        assert best["capacity_upper_bound"] < TARGET_AGREEMENT

    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_RANDOM_LOWDEGREE_LIST_WITNESS_SEARCH_OK")
        print("candidate_count: %d" % record["candidate_count"])
        print("best_capacity_upper_bound: %s" % best["capacity_upper_bound"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
