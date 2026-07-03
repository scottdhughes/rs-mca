#!/usr/bin/env python3
"""Prepare the M1 a=327 low-rank template kernel-extraction ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "c5f1caa"
SOURCE_DATA = Path("experimental/data/m1_a327_lowrank_template_exact_audit.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_lowrank_template_kernel_extraction.json")

TARGET_AGREEMENT = 327


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def build_record(mark_square_timeout: bool = False, mark_eval_timeout: bool = False) -> dict[str, Any]:
    source = load_source()
    proxy = source["proxy_candidate"]
    if proxy["template_id"] != "mixed_rank6":
        raise RuntimeError(f"unexpected template: {proxy['template_id']}")
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
            "raw_selected_class_rows": proxy["raw_row_count"],
            "compressed_basis_rows": proxy["basis_row_count"],
            "variable_count": proxy["variable_count"],
            "proxy_field": proxy["proxy_field"],
            "proxy_rank": proxy["proxy_rank"],
            "proxy_nullity": proxy["proxy_nullity"],
            "support_vector": proxy["support_vector"],
            "pair_count_matrix": proxy["pair_count_matrix"],
            "pair7_counts": proxy["pair7_counts"],
            "selected_class_size_counts": proxy["selected_class_size_counts"],
            "coordinate_classes_hash": proxy["coordinate_classes_hash"],
            "row_specs_hash": proxy["row_specs_hash"],
        },
        "coordinate_classes": source["coordinate_classes"],
        "row_specs": source["row_specs"],
        "kernel_extraction": {
            "strategies_tested": [],
            "square_solves_tested": 0,
            "eval_sparse_solves_tested": 0,
            "exact_vectors_constructed": 0,
            "raw_rows_checked": 0,
            "raw_row_violations": None,
            "coefficient_matrix_shape": None,
            "eval_sparse_matrix_shape": None,
            "trial_results": [],
            "best_failure_mode": None,
        },
        "pair_projection_test": {
            "pairs_tested": 21,
            "forced_equal_pairs": [],
            "seven_distinct_vectors": 0,
        },
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": "CANDIDATE / LOWRANK_KERNEL_EXTRACTION_PENDING / PARTIAL / EXPERIMENTAL",
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
            "coordinate_classes_hash": hash_payload(source["coordinate_classes"]),
            "row_specs_hash": hash_payload(source["row_specs"]),
        },
    }
    if mark_square_timeout:
        record["kernel_extraction"]["strategies_tested"].append("square_free_column_solve")
        record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_SQUARE_SOLVE_TIMEOUT"
        record["proof_status"] = "CANDIDATE / LOWRANK_KERNEL_SQUARE_SOLVE_TIMEOUT / PARTIAL / EXPERIMENTAL"
    if mark_eval_timeout:
        record["kernel_extraction"]["strategies_tested"].append("eval_sparse_solve")
        record["kernel_extraction"]["best_failure_mode"] = "LOWRANK_KERNEL_EVAL_SPARSE_TIMEOUT"
        record["proof_status"] = "CANDIDATE / LOWRANK_KERNEL_EVAL_SPARSE_TIMEOUT / PARTIAL / EXPERIMENTAL"
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--mark-square-timeout", action="store_true")
    parser.add_argument("--mark-eval-timeout", action="store_true")
    args = parser.parse_args()
    record = build_record(
        mark_square_timeout=args.mark_square_timeout,
        mark_eval_timeout=args.mark_eval_timeout,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        proxy = record["proxy_candidate"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "template_id": proxy["template_id"],
                    "compressed_basis_rows": proxy["compressed_basis_rows"],
                    "variable_count": proxy["variable_count"],
                    "proxy_rank": proxy["proxy_rank"],
                    "proxy_nullity": proxy["proxy_nullity"],
                    "best_failure_mode": record["kernel_extraction"]["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LOWRANK_TEMPLATE_KERNEL_EXTRACTION_READY")


if __name__ == "__main__":
    main()
