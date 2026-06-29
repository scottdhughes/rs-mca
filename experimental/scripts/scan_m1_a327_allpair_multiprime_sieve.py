#!/usr/bin/env python3
"""Multi-prime proxy sieve for all-pair-boundary a=327 embeddings."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_singular_all_pair_boundary_embedding_search as allpair


OUTPUT_DATA = Path("experimental/data/m1_a327_allpair_multiprime_sieve.json")

N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
COLUMNS = LIST_SIZE - 1
PAIR_CAP = K - 1

# Generated with PARI/GP:
# v=[]; n=1; while(#v<23, n=nextprime(n+1); if(n%512==1, v=concat(v,[n]))); print(v)
MULTIPRIME_PROXY_PRIMES = [
    7681,
    10753,
    11777,
    12289,
    13313,
    15361,
    17921,
    18433,
    19457,
    23041,
    25601,
    26113,
    32257,
    36353,
    37889,
    39937,
    40961,
    45569,
    50177,
    51713,
    58369,
    59393,
    61441,
]


def jsonable(payload: Any) -> Any:
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


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def factor_distinct(n: int) -> list[int]:
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors


def primitive_root_mod_prime(p: int) -> int:
    n = p - 1
    factors = factor_distinct(n)
    for candidate in range(2, p):
        if all(pow(candidate, n // factor, p) != 1 for factor in factors):
            return candidate
    raise RuntimeError(f"no primitive root for {p}")


def proxy_subgroup(p: int) -> np.ndarray:
    if (p - 1) % N != 0:
        raise ValueError(f"proxy prime {p} does not have 512-subgroup")
    generator = primitive_root_mod_prime(p)
    subgroup_generator = pow(generator, (p - 1) // N, p)
    return np.array([pow(subgroup_generator, idx, p) for idx in range(N)], dtype=np.int64)


def bit(mask: int, idx: int) -> bool:
    return bool(int(mask) & (1 << idx))


def embedding_structure(masks: list[int]) -> dict[str, Any]:
    anchor_roots: dict[int, list[int]] = {}
    pair_positions: dict[tuple[int, int], list[int]] = {}
    for witness in range(1, LIST_SIZE):
        anchor_roots[witness] = [
            pos for pos, mask in enumerate(masks) if bit(mask, 0) and bit(mask, witness)
        ]
    for left in range(1, LIST_SIZE):
        for right in range(left + 1, LIST_SIZE):
            pair_positions[(left, right)] = [
                pos for pos, mask in enumerate(masks) if bit(mask, left) and bit(mask, right)
            ]
    return {"anchor_roots": anchor_roots, "pair_positions": pair_positions}


def locator_values_modp(H: np.ndarray, roots: list[int], p: int) -> np.ndarray:
    values = np.ones(N, dtype=np.int64)
    for position in roots:
        values = (values * ((H - int(H[position])) % p)) % p
    values[roots] = 0
    return values


def modular_rank(rows: list[list[int]], columns: int, p: int) -> tuple[int, list[int]]:
    basis: dict[int, list[int]] = {}
    pivot_rows = []
    for row_idx, row in enumerate(rows):
        vec = [int(value) % p for value in row]
        while True:
            pivot = next((idx for idx, value in enumerate(vec) if value % p), None)
            if pivot is None:
                break
            if pivot not in basis:
                inv = pow(vec[pivot], p - 2, p)
                basis[pivot] = [(value * inv) % p for value in vec]
                pivot_rows.append(row_idx)
                break
            factor = vec[pivot]
            base = basis[pivot]
            vec = [(left - factor * right) % p for left, right in zip(vec, base)]
        if len(basis) == columns:
            break
    return len(basis), pivot_rows


def modular_null_vector(rows: list[list[int]], columns: int, p: int) -> list[int] | None:
    matrix = [[int(value) % p for value in row] for row in rows]
    pivot_cols: list[int] = []
    row = 0
    for col in range(columns):
        pivot = next((idx for idx in range(row, len(matrix)) if matrix[idx][col] % p), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        inv = pow(matrix[row][col], p - 2, p)
        matrix[row] = [(value * inv) % p for value in matrix[row]]
        for idx in range(len(matrix)):
            if idx == row:
                continue
            factor = matrix[idx][col]
            if factor:
                matrix[idx] = [
                    (left - factor * right) % p
                    for left, right in zip(matrix[idx], matrix[row])
                ]
        pivot_cols.append(col)
        row += 1
        if row == len(matrix):
            break
    free_cols = [col for col in range(columns) if col not in pivot_cols]
    if not free_cols:
        return None
    free_col = free_cols[0]
    vector = [0] * columns
    vector[free_col] = 1
    for row_idx in range(len(pivot_cols) - 1, -1, -1):
        col = pivot_cols[row_idx]
        total = 0
        for other in free_cols:
            total = (total + matrix[row_idx][other] * vector[other]) % p
        vector[col] = (-total) % p
    return vector


def value_class_capacity(values: list[list[int]]) -> dict[str, Any]:
    largest_histogram: dict[str, int] = {}
    total_capacity = 0
    for pos in range(N):
        buckets: dict[int, int] = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        largest = max(mask.bit_count() for mask in buckets.values())
        total_capacity += largest
        largest_histogram[str(largest)] = largest_histogram.get(str(largest), 0) + 1
    return {
        "capacity_total": total_capacity,
        "capacity_upper_bound": total_capacity // LIST_SIZE,
        "largest_class_histogram": dict(sorted(largest_histogram.items(), key=lambda item: int(item[0]))),
    }


def rank_rows_for_prime(structure: dict[str, Any], p: int, H: np.ndarray) -> tuple[list[list[int]], dict[int, np.ndarray]]:
    locators = {
        witness: locator_values_modp(H, roots, p)
        for witness, roots in structure["anchor_roots"].items()
    }
    rows = []
    for left in range(1, LIST_SIZE):
        for right in range(left + 1, LIST_SIZE):
            for pos in structure["pair_positions"][(left, right)]:
                left_value = int(locators[left][pos])
                right_value = int(locators[right][pos])
                if left_value == 0 and right_value == 0:
                    continue
                row = [0] * COLUMNS
                row[left - 1] = left_value
                row[right - 1] = (-right_value) % p
                rows.append(row)
    return rows, locators


def capacity_from_kernel(locators: dict[int, np.ndarray], kernel: list[int], p: int) -> dict[str, Any]:
    values = [[0] * N]
    for witness in range(1, LIST_SIZE):
        constant = int(kernel[witness - 1]) % p
        values.append([int((constant * int(locators[witness][pos])) % p) for pos in range(N)])
    return value_class_capacity(values)


def prime_record_for_embedding(structure: dict[str, Any], p: int, H: np.ndarray) -> dict[str, Any]:
    rows, locators = rank_rows_for_prime(structure, p, H)
    rank, pivot_rows = modular_rank(rows, COLUMNS, p)
    nullity = COLUMNS - rank
    record: dict[str, Any] = {
        "prime": p,
        "rank": rank,
        "nullity": nullity,
        "remaining_equations": len(rows),
        "pivot_rows_count": len(pivot_rows),
        "pivot_rows_hash": hash_payload(pivot_rows),
        "status": "PROXY_SINGULAR" if nullity else "PROXY_FULL_RANK",
    }
    if nullity:
        kernel = modular_null_vector(rows, COLUMNS, p)
        if kernel is None:
            raise RuntimeError("rank/nullity mismatch")
        capacity = capacity_from_kernel(locators, kernel, p)
        record.update(
            {
                "kernel_hash": hash_payload(kernel),
                "kernel_capacity": capacity,
                "capacity_status": (
                    "PROXY_KERNEL_CAPACITY_REACHES_A327"
                    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT
                    else "PROXY_KERNEL_CAPACITY_BELOW_A327"
                ),
            }
        )
    return record


def candidate_records() -> list[dict[str, Any]]:
    records = []
    for candidate in allpair.candidate_embeddings():
        masks = candidate["membership_masks"]
        summary = allpair.summarize_masks(masks)
        if summary["support_sizes"] != [TARGET_AGREEMENT] * LIST_SIZE:
            raise RuntimeError("support size mismatch")
        if summary["pairs_at_255"] != 21:
            raise RuntimeError("all-pair boundary profile lost")
        records.append(
            {
                "candidate_id": f"all_pair_boundary_{candidate['embedding_id']}",
                "embedding_id": candidate["embedding_id"],
                "embedding_family": candidate["embedding_family"],
                "seed": candidate["seed"],
                "membership_masks": masks,
                "membership_mask_hash": allpair.hash_payload(masks),
                "summary": allpair.compact_summary(summary),
            }
        )
    return records


def evaluate_candidate(candidate: dict[str, Any], subgroups: dict[int, np.ndarray]) -> dict[str, Any]:
    structure = embedding_structure(candidate["membership_masks"])
    prime_records = [
        prime_record_for_embedding(structure, prime, subgroups[prime])
        for prime in MULTIPRIME_PROXY_PRIMES
    ]
    rank_histogram: dict[str, int] = {}
    singular_records = []
    capacity_anomalies = []
    for record in prime_records:
        rank_histogram[str(record["rank"])] = rank_histogram.get(str(record["rank"]), 0) + 1
        if record["nullity"]:
            singular_records.append(record)
            if record["kernel_capacity"]["capacity_upper_bound"] >= TARGET_AGREEMENT:
                capacity_anomalies.append(record)
    min_rank = min(record["rank"] for record in prime_records)
    max_nullity = max(record["nullity"] for record in prime_records)
    status = (
        "MULTIPRIME_PROXY_ANOMALY"
        if singular_records or capacity_anomalies
        else "MULTIPRIME_PROXY_FULL_RANK"
    )
    prime_rank_profile = [
        (record["prime"], record["rank"], record["nullity"], record["remaining_equations"])
        for record in prime_records
    ]
    prime_pivot_profile = [
        (record["prime"], record["pivot_rows_hash"])
        for record in prime_records
    ]
    return {
        "candidate_id": candidate["candidate_id"],
        "embedding_id": candidate["embedding_id"],
        "embedding_family": candidate["embedding_family"],
        "seed": candidate["seed"],
        "membership_mask_hash": candidate["membership_mask_hash"],
        "summary": candidate["summary"],
        "rank_histogram": dict(sorted(rank_histogram.items(), key=lambda item: int(item[0]))),
        "min_rank": min_rank,
        "max_nullity": max_nullity,
        "singular_prime_count": len(singular_records),
        "capacity_anomaly_count": len(capacity_anomalies),
        "prime_rank_profile_hash": hash_payload(prime_rank_profile),
        "prime_pivot_profile_hash": hash_payload(prime_pivot_profile),
        "anomaly_prime_records": [
            {
                "prime": record["prime"],
                "rank": record["rank"],
                "nullity": record["nullity"],
                "remaining_equations": record["remaining_equations"],
                "pivot_rows_hash": record["pivot_rows_hash"],
                **(
                    {
                        "kernel_hash": record["kernel_hash"],
                        "kernel_capacity_upper_bound": record["kernel_capacity"]["capacity_upper_bound"],
                        "kernel_capacity_total": record["kernel_capacity"]["capacity_total"],
                        "capacity_status": record["capacity_status"],
                    }
                    if record["nullity"]
                    else {}
                ),
            }
            for record in singular_records
        ],
        "status": status,
    }


def build_record() -> dict[str, Any]:
    candidates = candidate_records()
    subgroups = {prime: proxy_subgroup(prime) for prime in MULTIPRIME_PROXY_PRIMES}
    results = [evaluate_candidate(candidate, subgroups) for candidate in candidates]
    anomalies = [row for row in results if row["status"] == "MULTIPRIME_PROXY_ANOMALY"]
    best = sorted(
        results,
        key=lambda row: (
            row["max_nullity"],
            -row["min_rank"],
            row["singular_prime_count"],
            row["capacity_anomaly_count"],
            row["candidate_id"],
        ),
        reverse=True,
    )[0]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "allpair_multiprime_sieve",
        "source": {
            "source_scanner": "experimental/scripts/scan_m1_a327_singular_all_pair_boundary_embedding_search.py",
            "source_profile_json": str(allpair.SOURCE_DATA_PATH),
        },
        "prime_source": "PARI/GP first primes p == 1 mod 512",
        "proxy_primes": MULTIPRIME_PROXY_PRIMES,
        "proxy_prime_count": len(MULTIPRIME_PROXY_PRIMES),
        "candidate_count": len(results),
        "rank_evaluation_count": len(results) * len(MULTIPRIME_PROXY_PRIMES),
        "deterministic_embedding_count": 3,
        "random_embedding_count": allpair.RANDOM_EMBEDDINGS,
        "candidate_records_include_membership_masks": False,
        "results": [
            {
                key: value
                for key, value in row.items()
                if key != "membership_masks"
            }
            for row in results
        ],
        "result_hash": hash_payload(results),
        "anomaly_count": len(anomalies),
        "rank_anomaly_count": sum(1 for row in anomalies if row["singular_prime_count"]),
        "capacity_anomaly_count": sum(1 for row in anomalies if row["capacity_anomaly_count"]),
        "exact_audit_triggers": [row["candidate_id"] for row in anomalies],
        "best": best,
        "proof_status": (
            "CANDIDATE"
            if anomalies
            else "TESTED_EMBEDDINGS_NO_MULTIPRIME_PROXY_ANOMALY"
        ),
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
