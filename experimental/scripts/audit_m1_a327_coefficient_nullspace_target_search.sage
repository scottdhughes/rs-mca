#!/usr/bin/env sage
"""Exact GF(17^32) capacity audit for selected coefficient-nullspace root tuples."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
TARGET_AGREEMENT = 327
TOP_LABELS_PER_WITNESS = 3
SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_coefficient_nullspace_target_search.py")
SCAN_DATA_PATH = Path("experimental/data/m1_a327_coefficient_nullspace_target_search.json")
DATA_PATH = Path("experimental/data/m1_a327_coefficient_nullspace_target_search_exact_audit.json")

EXACT_ROOT_TUPLES = {
    "all_pair_boundary_random_shuffle_0064",
    "all_pair_boundary_random_shuffle_0255",
    "all_pair_boundary_block",
    "quotient_residual_shift_00",
    "interval_shift_000_step_17",
    "random_255_tuple_000",
}


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
    return str(payload)


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_scanner():
    spec = importlib.util.spec_from_file_location("coefficient_nullspace_scanner", SCANNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def field_context_exact():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def locator_values(F, H, roots):
    root_points = [H[pos] for pos in roots]
    root_set = set(roots)
    values = []
    for pos, point in enumerate(H):
        if pos in root_set:
            values.append(F(0))
            continue
        acc = F(1)
        for root in root_points:
            acc *= point - root
        values.append(acc)
    return values


def top_base_constants(locator_values, limit=TOP_LABELS_PER_WITNESS):
    constants = []
    base = locator_values[0]
    for witness in range(1, DIFF_COUNT):
        labels = Counter()
        other = locator_values[witness]
        for pos in range(N):
            if base[pos] == 0 or other[pos] == 0:
                continue
            labels[base[pos] / other[pos]] += 1
        top = [label for label, _count in labels.most_common(limit)]
        while len(top) < limit:
            top.append(base[0].parent()(1))
        constants.append(top)
    return constants


def value_class_capacity(values):
    largest_histogram = {}
    total_capacity = 0
    for pos in range(N):
        buckets = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        largest = max(int(mask).bit_count() for mask in buckets.values())
        total_capacity += largest
        largest_histogram[str(largest)] = largest_histogram.get(str(largest), 0) + 1
    return {
        "capacity_total": total_capacity,
        "capacity_upper_bound": total_capacity // LIST_SIZE,
        "largest_class_histogram": dict(sorted(largest_histogram.items(), key=lambda item: int(item[0]))),
    }


def evaluate_constants(locator_values, constants):
    F = locator_values[0][0].parent()
    values = [[F(0) for _ in range(N)]]
    for constant, locator in zip(constants, locator_values):
        values.append([constant * locator[pos] for pos in range(N)])
    return value_class_capacity(values)


def audit_root_tuple(root_tuple, F, H):
    locators = [locator_values(F, H, roots) for roots in root_tuple["root_sets"]]
    constant_options = top_base_constants(locators)
    candidates = [[F(1)] * DIFF_COUNT]
    for combo in itertools.product(*constant_options):
        candidates.append([F(1)] + list(combo))

    seen = set()
    best = None
    tested = 0
    for constants in candidates:
        digest = hash_payload([str(constant) for constant in constants])
        if digest in seen:
            continue
        seen.add(digest)
        tested += 1
        result = evaluate_constants(locators, constants)
        row = {
            "constants_hash": digest,
            **result,
        }
        if best is None or (
            row["capacity_upper_bound"],
            row["capacity_total"],
            row["constants_hash"],
        ) > (
            best["capacity_upper_bound"],
            best["capacity_total"],
            best["constants_hash"],
        ):
            best = row

    return {
        "root_tuple_id": root_tuple["root_tuple_id"],
        "family": root_tuple["family"],
        "root_tuple_hash": root_tuple["root_tuple_hash"],
        "constant_candidates_tested": tested,
        "best": best,
        "status": "EXACT_CAPACITY_REACHES_A327" if best["capacity_upper_bound"] >= TARGET_AGREEMENT else "EXACT_CAPACITY_BELOW_A327",
    }


def exact_record():
    scanner = load_scanner()
    with SCAN_DATA_PATH.open() as handle:
        source = json.load(handle)
    q, F, H = field_context_exact()
    tuples = {root_tuple["root_tuple_id"]: root_tuple for root_tuple in scanner.root_tuples()}
    results = [audit_root_tuple(tuples[root_tuple_id], F, H) for root_tuple_id in sorted(EXACT_ROOT_TUPLES)]
    exact_candidate_count = sum(1 for row in results if row["status"] == "EXACT_CAPACITY_REACHES_A327")
    proof_status = "CANDIDATE" if exact_candidate_count else "ROUTE_CUT_TESTED_ROOT_SETS"
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "coefficient_nullspace_target_exact_capacity_audit",
            "source": {
                "source_json": str(SCAN_DATA_PATH),
                "source_result_hash": source["result_hash"],
                "source_proof_status": source["proof_status"],
                "source_proxy_candidate_count": source["proxy_candidate_count"],
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "degree_bound": K,
            "top_labels_per_witness": TOP_LABELS_PER_WITNESS,
            "exact_root_tuple_count": len(results),
            "results": results,
            "result_hash": hash_payload(results),
            "exact_candidate_count": exact_candidate_count,
            "proof_status": proof_status,
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list certificate",
                "global Lambda_mu(C,327) <= 6",
                "exact Lambda_mu",
                "exact delta*_C",
                "improvement over PR #133",
            ],
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()

    record = exact_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_COEFFICIENT_NULLSPACE_TARGET_SEARCH_OK")
        print("exact_root_tuple_count: %d" % record["exact_root_tuple_count"])
        print("exact_candidate_count: %d" % record["exact_candidate_count"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
