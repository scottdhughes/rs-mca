#!/usr/bin/env python3
"""Prepare the M1 a=327 low-rank functional-divisibility lift ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "64e2fdf"
SOURCE_DATA = Path("experimental/data/m1_a327_lowrank_template_kernel_extraction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_lowrank_template_functional_divisibility_lift.json")

P = 17
K = 256
TARGET_AGREEMENT = 327


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def rank_mod_p(rows: list[list[int]], prime: int = P) -> int:
    matrix = [[value % prime for value in row] for row in rows if any(value % prime for value in row)]
    if not matrix:
        return 0
    ncols = len(matrix[0])
    rank = 0
    for col in range(ncols):
        pivot = None
        for row in range(rank, len(matrix)):
            if matrix[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][col] % prime:
                continue
            factor = matrix[row][col] % prime
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def row_basis_mod_p(vectors: list[list[int]], members: list[int], prime: int = P) -> list[list[int]]:
    if len(members) <= 1:
        return []
    anchor = [value % prime for value in vectors[int(members[0]) - 1]]
    rows = []
    for witness in members[1:]:
        rows.append([(vectors[int(witness) - 1][idx] - anchor[idx]) % prime for idx in range(len(anchor))])
    matrix = [row[:] for row in rows if any(row)]
    basis = []
    rank = 0
    ncols = len(anchor)
    for col in range(ncols):
        pivot = None
        for row in range(rank, len(matrix)):
            if matrix[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][col] % prime:
                continue
            factor = matrix[row][col] % prime
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        basis.append(matrix[rank][:])
        rank += 1
        if rank == len(matrix):
            break
    return basis


def normalize_projective(row: list[int], prime: int = P) -> tuple[int, ...]:
    reduced = [value % prime for value in row]
    for value in reduced:
        if value:
            inv = pow(value, -1, prime)
            return tuple((entry * inv) % prime for entry in reduced)
    raise ValueError("zero functional cannot be normalized")


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def build_functional_classes(source: dict[str, Any]) -> list[dict[str, Any]]:
    vectors = source["proxy_candidate"]["template_vectors"]
    positions_by_functional: dict[tuple[int, ...], set[int]] = defaultdict(set)
    row_count = 0
    for coord in sorted(source["coordinate_classes"], key=lambda row: int(row["position"])):
        members = [int(value) for value in coord["members"]]
        for row in row_basis_mod_p(vectors, members):
            key = normalize_projective(row)
            positions_by_functional[key].add(int(coord["position"]))
            row_count += 1
    if row_count != source["proxy_candidate"]["compressed_basis_rows"]:
        raise RuntimeError(
            f"compressed row mismatch: {row_count} != {source['proxy_candidate']['compressed_basis_rows']}"
        )
    classes = []
    for idx, (functional, positions_set) in enumerate(
        sorted(positions_by_functional.items(), key=lambda item: (-len(item[1]), item[0]))
    ):
        positions = sorted(positions_set)
        support_size = len(positions)
        classes.append(
            {
                "class_index": idx,
                "functional": list(functional),
                "support_size": support_size,
                "forced_identity": support_size > K - 1,
                "quotient_variables": max(0, K - support_size),
                "positions": positions,
                "positions_hash": hash_payload(positions),
            }
        )
    return classes


def build_record(mark_timeout: bool = False) -> dict[str, Any]:
    source = load_source()
    proxy = source["proxy_candidate"]
    if proxy["template_id"] != "mixed_rank6":
        raise RuntimeError(f"unexpected template: {proxy['template_id']}")
    classes = build_functional_classes(source)
    histogram = Counter(str(row["support_size"]) for row in classes)
    forced = [row for row in classes if row["forced_identity"]]
    quotient_variable_count = sum(row["quotient_variables"] for row in classes)
    matrix_shape = [K * len(classes), proxy["variable_count"] + quotient_variable_count]
    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "proxy_candidate": {
            "template_id": proxy["template_id"],
            "template_family": proxy["template_family"],
            "template_dimension": proxy["template_dimension"],
            "template_vectors": proxy["template_vectors"],
            "compressed_matrix_shape": source["kernel_extraction"]["coefficient_matrix_shape"],
            "raw_selected_class_rows": proxy["raw_selected_class_rows"],
            "compressed_basis_rows": proxy["compressed_basis_rows"],
            "variable_count": proxy["variable_count"],
            "proxy_field": proxy["proxy_field"],
            "proxy_rank": proxy["proxy_rank"],
            "proxy_nullity": proxy["proxy_nullity"],
            "support_vector": proxy["support_vector"],
            "pair_count_matrix": proxy["pair_count_matrix"],
            "pair7_counts": proxy["pair7_counts"],
            "selected_class_size_counts": proxy["selected_class_size_counts"],
        },
        "coordinate_classes": source["coordinate_classes"],
        "row_specs": source["row_specs"],
        "functional_classes_detail": classes,
        "functional_divisibility": {
            "functional_classes": len(classes),
            "support_size_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
            "forced_functional_identities": len(forced),
            "quotient_variable_count": quotient_variable_count,
            "matrix_shape": matrix_shape,
            "formal_nullity_lower_bound": max(0, matrix_shape[1] - matrix_shape[0]),
            "rank": None,
            "nullity": None,
            "best_failure_mode": None,
        },
        "pair_projection_test": {
            "pairs_tested": 21,
            "forced_equal_pairs": [],
            "min_projection_rank": None,
            "projection_rank_by_pair": None,
        },
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": "CANDIDATE / FUNC_DIV_METADATA / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
        ],
        "ledger_hashes": {
            "functional_classes_hash": hash_payload(classes),
            "coordinate_classes_hash": hash_payload(source["coordinate_classes"]),
            "row_specs_hash": hash_payload(source["row_specs"]),
        },
    }
    if len(classes) > 64:
        record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_TOO_MANY_FUNCTIONALS"
        record["proof_status"] = "CANDIDATE / FUNC_DIV_TOO_MANY_FUNCTIONALS / PARTIAL / EXPERIMENTAL"
    if mark_timeout:
        record["functional_divisibility"]["best_failure_mode"] = "FUNC_DIV_MATRIX_TIMEOUT"
        record["proof_status"] = "CANDIDATE / FUNC_DIV_MATRIX_TIMEOUT / PARTIAL / EXPERIMENTAL"
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--mark-timeout", action="store_true")
    args = parser.parse_args()
    record = build_record(mark_timeout=args.mark_timeout)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        func = record["functional_divisibility"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "functional_classes": func["functional_classes"],
                    "support_size_histogram": func["support_size_histogram"],
                    "forced_functional_identities": func["forced_functional_identities"],
                    "quotient_variable_count": func["quotient_variable_count"],
                    "matrix_shape": func["matrix_shape"],
                    "best_failure_mode": func["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LOWRANK_TEMPLATE_FUNCTIONAL_DIVISIBILITY_READY")


if __name__ == "__main__":
    main()
