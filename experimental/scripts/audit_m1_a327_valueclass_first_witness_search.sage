#!/usr/bin/env sage
"""Sage proxy-rank audit for the M1 a=327 value-class-first search."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_valueclass_first_witness_search.py")
DATA_PATH = Path("experimental/data/m1_a327_valueclass_first_witness_search.json")
PROXY_PRIME = 12289


def load_scanner():
    spec = importlib.util.spec_from_file_location("valueclass_scanner", SCANNER_PATH)
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


def field_context_proxy():
    F = GF(PROXY_PRIME)
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((PROXY_PRIME - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def bit(mask, idx):
    return bool(int(mask) & (1 << idx))


def locator_values(F, H, positions):
    roots = [H[pos] for pos in positions]
    position_set = set(positions)
    values = []
    for pos, point in enumerate(H):
        if pos in position_set:
            values.append(F(0))
            continue
        acc = F(1)
        for root in roots:
            acc *= point - root
        values.append(acc)
    return values


def reduced_rank_result(candidate, F, H, powers):
    masks = candidate["membership_masks"]
    anchor_zero_positions = {}
    locator_by_witness = {}
    dim_by_witness = {}
    offsets = {}
    total_vars = 0

    for witness in range(1, LIST_SIZE):
        zero_positions = [
            pos
            for pos, mask in enumerate(masks)
            if bit(mask, 0) and bit(mask, witness)
        ]
        anchor_zero_positions[str(witness)] = len(zero_positions)
        dim = max(0, K - len(zero_positions))
        dim_by_witness[witness] = dim
        offsets[witness] = total_vars
        total_vars += dim
        locator_by_witness[witness] = locator_values(F, H, zero_positions)

    rows = []
    row_type_counts = {}
    for left, right in itertools.combinations(range(1, LIST_SIZE), 2):
        for pos, mask in enumerate(masks):
            if not (bit(mask, left) and bit(mask, right)):
                continue
            row = [F(0)] * total_vars
            left_locator = locator_by_witness[left][pos]
            right_locator = locator_by_witness[right][pos]
            for degree in range(dim_by_witness[left]):
                row[offsets[left] + degree] = left_locator * powers[degree][pos]
            for degree in range(dim_by_witness[right]):
                row[offsets[right] + degree] -= right_locator * powers[degree][pos]
            if any(entry != 0 for entry in row):
                rows.append(row)
                row_type_counts[f"{left},{right}"] = row_type_counts.get(f"{left},{right}", 0) + 1

    if total_vars == 0:
        rank = 0
        nullity = 0
    else:
        M = Matrix(F, rows, ncols=total_vars)
        rank = int(M.rank())
        nullity = int(total_vars - rank)

    summary = candidate["summary"]
    return {
        "candidate_id": candidate["candidate_id"],
        "family": candidate["family"],
        "support_sizes": summary["support_sizes"],
        "min_support_size": summary["min_support_size"],
        "max_pair_intersection": summary["max_pair_intersection"],
        "pairs_at_cap": summary["pairs_at_cap"],
        "membership_histogram": summary["membership_histogram"],
        "anchor_zero_counts": anchor_zero_positions,
        "compressed_variables": total_vars,
        "remaining_equations": len(rows),
        "row_type_counts": dict(sorted(row_type_counts.items())),
        "proxy_rank": rank,
        "proxy_nullity": nullity,
        "exact_rank": None,
        "exact_nullity": None,
        "exact_status": "NOT_RUN_PROXY_FULL_RANK" if nullity == 0 else "EXACT_GF17_32_REQUIRED",
        "non_diagonal_solution_found": False,
        "agreement_verified": False,
        "status": "PROXY_POSITIVE_NULLITY" if nullity > 0 else "PROXY_FULL_RANK",
    }


def proxy_record():
    scanner = load_scanner()
    F, H = field_context_proxy()
    powers = precompute_powers(F, H)
    candidates = scanner.candidate_designs()
    results = [reduced_rank_result(candidate, F, H, powers) for candidate in candidates]
    record = scanner.build_record(rank_results=results)
    record["field_denominator"] = str(Integer(P) ** FIELD_DEGREE)
    record["subgroup_order"] = len(H)
    record["sage_audit"] = {
        "proxy_field": "GF(12289)",
        "exact_field": "GF(17^32)",
        "exact_trigger": "proxy_nullity > 0",
        "subgroup_order": len(H),
        "degree_bound": K,
        "candidate_design_hash": scanner.hash_payload(candidates),
        "proxy_rank_result_hash": hash_payload(results),
        "status": "SAGE_PROXY_REDUCED_RANK_GATE",
    }
    return jsonable(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()

    record = proxy_record()
    best = record["rank_gate"]["best"]
    if record["proof_status"] == "TESTED_DESIGNS_NO_PROXY_NULLITY":
        assert best["proxy_nullity"] == 0

    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_VALUECLASS_FIRST_WITNESS_SEARCH_OK")
        print("candidate_count: %d" % record["candidate_count"])
        print("best_proxy_nullity: %s" % best["proxy_nullity"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
