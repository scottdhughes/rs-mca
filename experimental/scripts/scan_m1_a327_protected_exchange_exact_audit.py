#!/usr/bin/env python3
"""Candidate ledger for exact audit of protected-exchange proxy hits."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_hall_guided_target_mutation as guided
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_witness7_pair_protected_local_exchange as protected


SOURCE_DATA_PATH = Path("experimental/data/m1_a327_witness7_pair_protected_local_exchange.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_protected_exchange_exact_audit.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PROXY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "c9f2e4c"


def jsonable(payload: object) -> object:
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
    if hasattr(payload, "tolist"):
        return jsonable(payload.tolist())
    return payload


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def source_record() -> dict[str, Any]:
    return load_json(SOURCE_DATA_PATH)


def proxy_candidate_rows(record: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    record = source_record() if record is None else record
    rows = []
    seen = set()
    for row in record["retained_results"]:
        best = row["best"]
        if best["failure_mode"] != "PROTECTED_EXCHANGE_PROXY_CANDIDATE":
            continue
        key = row["target_system_id"]
        if key in seen:
            continue
        seen.add(key)
        rows.append(row)
    rows.sort(
        key=lambda row: (
            row["best"]["proxy_max_min"],
            row["best"]["min_pair7_B"],
            row["best"]["capacity_upper_bound"],
            row["target_system_id"],
        ),
        reverse=True,
    )
    return rows


def reconstruct_candidate(row: dict[str, Any]) -> dict[str, Any]:
    stage1_row = None
    for candidate in protected.retained_stage1_bases():
        if candidate["best"]["value_class_hash"] == row["stage1_value_class_hash"]:
            stage1_row = candidate
            break
    if stage1_row is None:
        raise RuntimeError("stage-1 base not found for protected-exchange candidate")
    base, values, original_selected = protected.reconstruct_stage1_state(stage1_row)
    selection = protected.select_exchange_rows(
        values,
        base,
        original_selected,
        int(row["exchange_budget"]),
        row["exchange_move"],
    )
    target_hash = guided.hash_payload([(coord["position"], coord["mask"]) for coord in selection["selected"]])
    if target_hash != row["target_rows_hash"]:
        raise RuntimeError("protected-exchange target row reconstruction hash mismatch")

    powers = joint.vandermonde_powers(joint.proxy_subgroup())
    matrix = balanced.rows_for_selected(powers, selection["selected"])
    rref, pivots = joint.rref_modp(matrix, PROXY_PRIME)
    seed = int(
        guided.hash_payload([base["stage1_value_class_hash"], row["exchange_budget"], row["exchange_move"], protected.SOURCE_COMMIT])[:12],
        16,
    )
    vectors = balanced.sample_nullspace_vectors(rref, pivots, seed, protected.SAMPLES_PER_SYSTEM)
    sample_index = int(row["best"]["sample_index"])
    vector = vectors[sample_index]
    if guided.hash_payload(vector.tolist()) != row["best"]["vector_hash"]:
        raise RuntimeError("protected-exchange proxy vector reconstruction hash mismatch")
    return {
        "base": base,
        "selection": selection,
        "selected": selection["selected"],
        "pivots": pivots,
        "proxy_vector": vector,
        "proxy_matrix_shape": [int(matrix.shape[0]), int(matrix.shape[1])],
        "proxy_rank": len(pivots),
        "proxy_nullity": joint.VARIABLE_COUNT - len(pivots),
    }


def candidate_ledger(row: dict[str, Any]) -> dict[str, Any]:
    best = row["best"]
    return {
        "candidate_id": row["target_system_id"],
        "exchange_budget": row["exchange_budget"],
        "exchange_move": row["exchange_move"],
        "proxy_field": row["proxy_field"],
        "proxy_rank": row["rank"],
        "proxy_nullity": row["nullity"],
        "target_row_count": row["target_row_count"],
        "target_rows_hash": row["target_rows_hash"],
        "proxy_codeword_tuple_hash": best["vector_hash"],
        "proxy_value_class_hash": best["value_class_hash"],
        "proxy_max_min": best["proxy_max_min"],
        "proxy_agreement_vector": best["agreement_vector"],
        "capacity_upper_bound": best["capacity_upper_bound"],
        "pair_B_values": best["pair7_B_values"],
        "pair_deficit_to_654": best["pair7_deficits_to_654"],
        "added_six_class_dominance": best["six_class_dominance_added_by_repair"],
        "protected_stage1_rows_preserved": row["protected_rows_preserved"],
        "sample_index": best["sample_index"],
    }


def build_record(exact_audit: dict[str, Any] | None = None) -> dict[str, Any]:
    source = source_record()
    candidates = [candidate_ledger(row) for row in proxy_candidate_rows(source)]
    best = candidates[0] if candidates else None
    exact_audit = exact_audit or {
        "candidates_tested": 0,
        "row_schedules_tested": 0,
        "free_schedules_tested": 0,
        "exact_vectors_constructed": 0,
        "nondegenerate_vectors": 0,
        "best_exact_max_min": None,
        "best_exact_agreement_vector": None,
        "best_capacity_upper_bound": None,
        "best_pair_B_values": None,
        "best_failure_mode": "EXACT_AUDIT_PENDING" if candidates else "NO_PROXY_CANDIDATES",
        "results": [],
    }
    proof_status = "CANDIDATE"
    if exact_audit["best_failure_mode"] == "EXACT_CANDIDATE_A327":
        proof_status = "PROOF_RECORD"
    elif exact_audit["candidates_tested"] > 0 and exact_audit["best_exact_max_min"] is not None:
        proof_status = "EXACT_AUDIT_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "construction_mode": "protected_exchange_exact_audit",
        "proxy_candidates": {
            "count": len(candidates),
            "best_candidate_id": None if best is None else best["candidate_id"],
            "best_proxy_max_min": None if best is None else best["proxy_max_min"],
            "best_proxy_agreement_vector": None if best is None else best["proxy_agreement_vector"],
            "best_pair_B_values": None if best is None else best["pair_B_values"],
            "added_six_class_dominance": None if best is None else best["added_six_class_dominance"],
            "candidates": candidates,
        },
        "exact_audit": exact_audit,
        "proof_status": proof_status,
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
