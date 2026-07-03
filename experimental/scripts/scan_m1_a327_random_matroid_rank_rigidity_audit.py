#!/usr/bin/env python3
"""Prepare a rank-rigidity audit for the M1 a=327 random-matroid proxy front."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "f50b089"
SOURCE_DATA = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v3.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_random_matroid_rank_rigidity_audit.json")

TARGET_AGREEMENT = 327


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def proxy_profile_rows(source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for candidate in source["rank_feedback_v3"]["candidate_summaries"]:
        for proxy in candidate["proxy_results"]:
            rows.append(
                {
                    "template_id": candidate["template_id"],
                    "assignment_strategy": candidate["assignment_strategy"],
                    "basis_id": proxy["basis_id"],
                    "matrix_shape": proxy["matrix_shape"],
                    "q_variable_count": proxy["q_variable_count"],
                    "proxy_rank": proxy["proxy_rank"],
                    "proxy_nullity": proxy["proxy_nullity"],
                    "row_surplus": proxy["matrix_shape"][0] - proxy["matrix_shape"][1],
                    "functional_classes": candidate["functional_classes"],
                    "functional_span_rank": candidate["functional_span_rank"],
                    "max_pair_count": candidate["max_pair_count"],
                    "pair7_counts": candidate["pair7_counts"],
                }
            )
    return rows


def build_record() -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    profiles = proxy_profile_rows(source)
    full_rank = [row for row in profiles if row["proxy_rank"] == row["q_variable_count"] and row["proxy_nullity"] == 0]
    positive = [row for row in profiles if row["proxy_nullity"] and row["proxy_nullity"] > 0]
    best = None
    if profiles:
        best = max(
            profiles,
            key=lambda row: (
                row["proxy_nullity"],
                -row["proxy_rank"],
                row["q_variable_count"],
                -row["row_surplus"],
            ),
        )
    row_surpluses = [row["row_surplus"] for row in profiles]
    q_variables = [row["q_variable_count"] for row in profiles]
    matrix_shapes = Counter(f"{row['matrix_shape'][0]}x{row['matrix_shape'][1]}" for row in profiles)
    basis_counts = Counter(row["basis_id"] for row in profiles)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "rank_feedback_v3": {
            "systems_tested": source["rank_feedback_v3"]["systems_tested"],
            "structural_pass_candidates": source["rank_feedback_v3"]["structural_pass_candidates"],
            "proxy_candidates_tested": source["rank_feedback_v3"]["proxy_candidates_tested"],
            "proxy_basis_profiles_tested": source["rank_feedback_v3"]["proxy_basis_profiles_tested"],
            "proxy_positive_candidates": source["rank_feedback_v3"]["proxy_positive_candidates"],
            "best_template_id": source["rank_feedback_v3"]["best_template_id"],
            "best_proxy_rank": source["rank_feedback_v3"]["best_proxy_rank"],
            "best_proxy_nullity": source["rank_feedback_v3"]["best_proxy_nullity"],
            "best_failure_mode": source["rank_feedback_v3"]["best_failure_mode"],
        },
        "rank_rigidity_audit": {
            "proxy_profiles_audited": len(profiles),
            "full_column_rank_profiles": len(full_rank),
            "proxy_positive_profiles": len(positive),
            "min_row_surplus": None if not row_surpluses else min(row_surpluses),
            "max_row_surplus": None if not row_surpluses else max(row_surpluses),
            "min_q_variable_count": None if not q_variables else min(q_variables),
            "max_q_variable_count": None if not q_variables else max(q_variables),
            "matrix_shape_counts": dict(sorted(matrix_shapes.items())),
            "basis_counts": dict(sorted(basis_counts.items())),
            "best_profile": best,
            "proxy_profiles": profiles,
            "best_failure_mode": "RANK_RIGIDITY_PROXY_FRONT_FULL_COLUMN_RANK"
            if profiles and len(full_rank) == len(profiles)
            else "RANK_RIGIDITY_PROXY_FRONT_MIXED",
        },
        "proof_status": "AUDIT / RANK_RIGIDITY_PROXY_FRONT / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "global rank rigidity outside the tested proxy front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        audit = record["rank_rigidity_audit"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "proxy_profiles_audited": audit["proxy_profiles_audited"],
                    "full_column_rank_profiles": audit["full_column_rank_profiles"],
                    "proxy_positive_profiles": audit["proxy_positive_profiles"],
                    "min_row_surplus": audit["min_row_surplus"],
                    "max_row_surplus": audit["max_row_surplus"],
                    "best_failure_mode": audit["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_RANDOM_MATROID_RANK_RIGIDITY_AUDIT_READY")


if __name__ == "__main__":
    main()
