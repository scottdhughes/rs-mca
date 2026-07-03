#!/usr/bin/env python3
"""Prepare the exact GF(17^32) audit target for the low-rank M1 a=327 template."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "e56f3ad"
SOURCE_DATA = Path("experimental/data/m1_a327_lowrank_template_selected_class_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_lowrank_template_exact_audit.json")

TARGET_AGREEMENT = 327


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def rank_mod_prime(rows: list[list[int]], prime: int = 17) -> int:
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


def build_record(mark_exact_timeout: bool = False) -> dict[str, Any]:
    source = load_source()
    best = source["best_candidate"]
    if best is None:
        raise RuntimeError("missing low-rank proxy-positive best candidate")
    if best["template_id"] != "mixed_rank6":
        raise RuntimeError(f"unexpected best template: {best['template_id']}")
    coordinate_classes = best["coordinate_classes"]
    template_vectors = best["template_vectors"]
    row_specs = []
    basis_row_count = 0
    for coord in sorted(coordinate_classes, key=lambda row: int(row["position"])):
        members = [int(value) for value in coord["members"]]
        anchor = min(members)
        coord_rows = []
        for witness in members:
            if witness == anchor:
                continue
            diff = [
                int(template_vectors[witness - 1][idx]) - int(template_vectors[anchor - 1][idx])
                for idx in range(best["template_dimension"])
            ]
            coord_rows.append(diff)
            row_specs.append(
                {
                    "position": int(coord["position"]),
                    "anchor": anchor,
                    "witness": witness,
                    "template_difference": diff,
                }
            )
        basis_row_count += rank_mod_prime(coord_rows)
    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "proxy_candidate": {
            "template_id": best["template_id"],
            "template_family": best["template_family"],
            "template_dimension": best["template_dimension"],
            "template_vectors": template_vectors,
            "effective_cost": best["total_effective_cost"],
            "variable_count": best["variable_count"],
            "proxy_field": "GF(12289)",
            "proxy_rank": best["proxy_rank"],
            "proxy_nullity": best["proxy_nullity"],
            "support_vector": best["support_vector"],
            "pair_count_matrix": best["pair_count_matrix"],
            "pair7_counts": best["pair7_counts"],
            "selected_class_size_counts": best["selected_class_size_counts"],
            "coordinate_classes_hash": best["coordinate_classes_hash"],
            "row_specs_hash": hash_payload(row_specs),
            "raw_row_count": len(row_specs),
            "basis_row_count": basis_row_count,
        },
        "coordinate_classes": coordinate_classes,
        "row_specs": row_specs,
        "exact_audit": {
            "field": "GF(17^32)",
            "H_order": None,
            "matrix_shape": None,
            "rank": None,
            "nullity": None,
            "exact_vectors_constructed": 0,
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
        "proof_status": "CANDIDATE / LOWRANK_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
        ],
    }
    if mark_exact_timeout:
        record["exact_audit"]["best_failure_mode"] = "LOWRANK_EXACT_TIMEOUT"
        record["proof_status"] = "CANDIDATE / LOWRANK_EXACT_TIMEOUT / PARTIAL / EXPERIMENTAL"
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--mark-exact-timeout", action="store_true")
    args = parser.parse_args()
    record = build_record(mark_exact_timeout=args.mark_exact_timeout)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        proxy = record["proxy_candidate"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "template_id": proxy["template_id"],
                    "template_dimension": proxy["template_dimension"],
                    "effective_cost": proxy["effective_cost"],
                    "variable_count": proxy["variable_count"],
                    "proxy_rank": proxy["proxy_rank"],
                    "proxy_nullity": proxy["proxy_nullity"],
                    "raw_row_count": proxy["raw_row_count"],
                    "basis_row_count": proxy["basis_row_count"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LOWRANK_TEMPLATE_EXACT_AUDIT_READY")


if __name__ == "__main__":
    main()
