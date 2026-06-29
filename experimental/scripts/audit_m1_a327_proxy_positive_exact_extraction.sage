#!/usr/bin/env sage
"""Exact GF(17^32) prefix-rank audit for proxy-positive extraction systems."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
VARIABLE_COUNT = DIFF_COUNT * K
TARGET_AGREEMENT = 327

SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_proxy_positive_exact_extraction.py")
SOURCE_DATA_PATH = Path("experimental/data/m1_a327_proxy_positive_exact_extraction.json")
DATA_PATH = Path("experimental/data/m1_a327_proxy_positive_exact_extraction_exact_audit.json")

AUDIT_SYSTEM_LIMIT = 1
PREFIX_ROW_COUNTS = [16, 32]


def load_scanner():
    script_dir = str(SCANNER_PATH.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location("proxy_positive_extraction_scanner", SCANNER_PATH)
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


def members(mask):
    return [idx for idx in range(LIST_SIZE) if int(mask) & (1 << idx)]


def constraint_rows_for_coordinate(F, powers, mask, pos):
    bits = members(mask)
    rows = []
    if 0 in bits:
        for witness in bits:
            if witness == 0:
                continue
            row = [F(0)] * VARIABLE_COUNT
            start = (witness - 1) * K
            for degree in range(K):
                row[start + degree] = powers[degree][pos]
            rows.append(row)
        return rows
    if len(bits) < 2:
        return rows
    left = bits[0]
    left_start = (left - 1) * K
    for witness in bits[1:]:
        row = [F(0)] * VARIABLE_COUNT
        right_start = (witness - 1) * K
        for degree in range(K):
            row[left_start + degree] = powers[degree][pos]
            row[right_start + degree] = -powers[degree][pos]
        rows.append(row)
    return rows


def rows_for_selected(F, powers, selected):
    rows = []
    for coord in selected:
        rows.extend(constraint_rows_for_coordinate(F, powers, coord["mask"], coord["position"]))
    if not rows:
        raise RuntimeError("empty exact target row set")
    return rows


def exact_prefix_audit(scanner, system, F, powers):
    source_record = scanner.load_source()
    source_by_id = {row["mutated_system_id"]: row for row in scanner.proxy_positive_rows(source_record)}
    source_row = source_by_id[system["system_id"]]
    _source, _base, selected_info = scanner.reconstruct_selected(source_row)
    exact_rows = rows_for_selected(F, powers, selected_info["selected"])
    prefix_results = []
    for row_count in PREFIX_ROW_COUNTS:
        used = min(row_count, len(exact_rows))
        matrix = Matrix(F, exact_rows[:used], ncols=VARIABLE_COUNT)
        rank = int(matrix.rank())
        prefix_results.append(
            {
                "rows": used,
                "rank": rank,
                "nullity_in_prefix_projection": int(VARIABLE_COUNT - rank),
                "full_row_rank_prefix": rank == used,
            }
        )
    return {
        "system_id": system["system_id"],
        "source_candidate_id": system["source_candidate_id"],
        "row_budget": system["row_budget"],
        "target_row_count": system["target_row_count"],
        "source_proxy_best_max_min": system["source_proxy_best_max_min"],
        "source_proxy_best_agreement": system["source_proxy_best_agreement"],
        "multi_prime_candidate_prime_count": system["multi_prime_candidate_prime_count"],
        "rank_drop_primes_vs_12289": system["rank_drop_primes_vs_12289"],
        "exact_prefix_rank_growth": prefix_results,
        "prefix_rank_drop_found": any(not row["full_row_rank_prefix"] for row in prefix_results),
        "full_exact_nullspace_extraction": "NOT_RUN",
        "status": "EXACT_PREFIX_ROWS_FULL_RANK"
        if all(row["full_row_rank_prefix"] for row in prefix_results)
        else "EXACT_PREFIX_RANK_DROP",
    }


def source_metadata(source):
    return {
        "source_json": str(SOURCE_DATA_PATH),
        "source_result_hash": source["result_hash"],
        "source_proof_status": source["proof_status"],
        "source_proxy_positive_systems": source["proxy_positive_systems"],
        "source_proxy_candidate_samples": source["proxy_candidate_samples"],
        "source_multi_prime_robust_system_count": source["multi_prime_robust_system_count"],
    }


def audit_record():
    scanner = load_scanner()
    with SOURCE_DATA_PATH.open() as handle:
        source = json.load(handle)
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    systems = sorted(
        source["systems"],
        key=lambda row: (
            row["multi_prime_candidate_prime_count"],
            row["source_proxy_best_max_min"],
            row["best_prime_fingerprint"]["best"]["capacity_upper_bound"],
            row["system_id"],
        ),
        reverse=True,
    )[:AUDIT_SYSTEM_LIMIT]
    results = [exact_prefix_audit(scanner, system, F, powers) for system in systems]
    prefix_drop_count = sum(1 for row in results if row["prefix_rank_drop_found"])
    proof_status = "EXACT_PREFIX_RANK_DROP_CANDIDATE" if prefix_drop_count else "EXACT_PREFIX_ROWS_FULL_RANK"
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "proxy_positive_exact_extraction_prefix_rank_audit",
            "source": source_metadata(source),
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "degree_bound": K,
            "audit_system_limit": AUDIT_SYSTEM_LIMIT,
            "prefix_row_counts": PREFIX_ROW_COUNTS,
            "exact_audited_system_count": len(results),
            "prefix_rank_drop_count": prefix_drop_count,
            "results": results,
            "result_hash": hash_payload(results),
            "proof_status": proof_status,
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list proof record",
                "global Lambda_mu(C,327) <= 6",
                "exact Lambda_mu",
                "exact delta*_C",
                "improvement over PR #133",
                "full GF(17^32) nullspace extraction",
            ],
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()

    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_PROXY_POSITIVE_EXACT_EXTRACTION_OK")
        print("exact_audited_system_count: %d" % record["exact_audited_system_count"])
        print("prefix_rank_drop_count: %d" % record["prefix_rank_drop_count"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
