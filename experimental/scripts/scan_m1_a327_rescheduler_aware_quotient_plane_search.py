#!/usr/bin/env python3
"""Rescheduler-aware quotient-plane search for the M1 a=327 proxy target."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_collapse_quotient_line_search as line
import scan_m1_a327_joint_target_codeword_solver as joint


SOURCE_DATA = Path("experimental/data/m1_a327_collapse_quotient_line_search.json")
SOFT_DATA = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_rescheduler_aware_quotient_plane_search.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PRIMARY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "ad3d73a"
LOW_COLLAPSE_THRESHOLD = 20
LINE_COUNT = 10
SECOND_DIRECTIONS_PER_LINE = 32
MU_VALUES = line.LAMBDA_VALUES
ASSIGNMENT_SOLVES_PER_LINE = 8


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


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def soft_row_by_id() -> dict[str, dict[str, Any]]:
    soft = load_json(SOFT_DATA)
    return {row["target_system_id"]: row for row in soft["retained_results"]}


def candidate_lines(source: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for system in source["systems"]:
        for candidate in system["retained_lines"]:
            if candidate["capacity_upper_bound"] < TARGET_AGREEMENT:
                continue
            if candidate["six_class_dominance"] > LOW_COLLAPSE_THRESHOLD:
                continue
            if candidate["proxy_max_min"] is None:
                continue
            rows.append(
                {
                    "system_id": system["system_id"],
                    **candidate,
                }
            )
    rows.sort(
        key=lambda row: (
            row["proxy_max_min"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["line_hash"],
        ),
        reverse=True,
    )
    return rows[:LINE_COUNT]


def vector_for_basis(core: dict[str, Any], basis_index: int) -> np.ndarray:
    return core["null_basis"][int(basis_index)] % PRIMARY_PRIME


def weak_witness_blocks(agreement_vector: list[int] | None) -> set[str]:
    if not agreement_vector:
        return {f"D_{idx}" for idx in range(2, 8)}
    min_value = min(agreement_vector)
    weak = {
        f"D_{idx + 1}"
        for idx, value in enumerate(agreement_vector)
        if value <= min_value + 1 and idx + 1 >= 2
    }
    return weak or {f"D_{idx}" for idx in range(2, 8)}


def direction_block_activity(vector: np.ndarray) -> list[str]:
    return line.direction_block_activity(vector)


def add_values(base_values: list[list[int]], direction_values: list[list[int]], scalar: int, p: int) -> list[list[int]]:
    return [
        [
            (int(base_values[witness][pos]) + scalar * int(direction_values[witness][pos])) % p
            for pos in range(line.N)
        ]
        for witness in range(line.LIST_SIZE)
    ]


def capacity_collapse_screen(values: list[list[int]]) -> dict[str, Any]:
    capacity = joint.value_class_capacity(values)
    six_dom = line.soft.six_class_dominance(values)
    if capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        failure_mode = "PLANE_CAPACITY_LOSS"
    elif six_dom > LOW_COLLAPSE_THRESHOLD:
        failure_mode = "PLANE_COLLAPSE_RETURNS"
    else:
        failure_mode = "PLANE_REDUCED_CAPACITY_UNSCHEDULED"
    return {
        **capacity,
        "six_class_dominance": six_dom,
        "failure_mode": failure_mode,
    }


def classify_solved(sample: dict[str, Any], baseline_max_min: int | None) -> str:
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "PLANE_CAPACITY_LOSS"
    if sample["six_class_dominance"] > LOW_COLLAPSE_THRESHOLD:
        return "PLANE_COLLAPSE_RETURNS"
    assignment = sample.get("assignment")
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "PLANE_PROXY_CANDIDATE"
    if assignment is not None and baseline_max_min is not None and assignment["exact_max_min"] > baseline_max_min:
        return "PLANE_BALANCE_IMPROVES"
    return "PLANE_LOW_RESCHEDULE"


def quotient_direction_pool(core: dict[str, Any], line_row: dict[str, Any]) -> list[dict[str, Any]]:
    weak_blocks = weak_witness_blocks(line_row["agreement_vector"])
    q1 = int(line_row["quotient_basis_index"])
    rows = []
    for idx, vector in enumerate(core["null_basis"]):
        if idx == q1 or not np.any(vector[line.K:] % PRIMARY_PRIME):
            continue
        blocks = direction_block_activity(vector)
        active_weak = len(set(blocks).intersection(weak_blocks))
        if active_weak == 0 and len(rows) > 4 * SECOND_DIRECTIONS_PER_LINE:
            continue
        values = line.vector_values(core["powers"], vector, PRIMARY_PRIME)
        screen = capacity_collapse_screen(values)
        free_column = int(core["free_cols"][idx])
        rows.append(
            {
                "basis_index": idx,
                "free_column": free_column,
                "free_block": f"D_{free_column // line.K + 2}",
                "active_blocks": blocks,
                "active_weak_blocks": active_weak,
                "direction_capacity_upper_bound": screen["capacity_upper_bound"],
                "direction_six_class_dominance": screen["six_class_dominance"],
                "direction_failure_mode": screen["failure_mode"],
                "vector_hash": hash_payload(vector.tolist()),
                "_vector": vector,
                "_values": values,
            }
        )
    rows.sort(
        key=lambda row: (
            row["active_weak_blocks"],
            row["direction_capacity_upper_bound"],
            -row["direction_six_class_dominance"],
            len(row["active_blocks"]),
            -row["basis_index"],
        ),
        reverse=True,
    )
    return rows[:SECOND_DIRECTIONS_PER_LINE]


def evaluate_plane_for_direction(
    base_line_values: list[list[int]],
    line_row: dict[str, Any],
    direction: dict[str, Any],
) -> dict[str, Any]:
    prelim = []
    for mu in MU_VALUES:
        values = add_values(base_line_values, direction["_values"], int(mu) % PRIMARY_PRIME, PRIMARY_PRIME)
        sample = capacity_collapse_screen(values)
        sample.update(
            {
                "mu": int(mu),
                "second_basis_index": direction["basis_index"],
                "second_free_column": direction["free_column"],
            }
        )
        prelim.append(sample)

    prelim.sort(
        key=lambda row: (
            row["failure_mode"] == "PLANE_REDUCED_CAPACITY_UNSCHEDULED",
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["capacity_total"],
        ),
        reverse=True,
    )
    best_pre = prelim[0]
    failure_counts: dict[str, int] = {}
    for row in prelim:
        failure_counts[row["failure_mode"]] = failure_counts.get(row["failure_mode"], 0) + 1

    solved = None
    if best_pre["failure_mode"] == "PLANE_REDUCED_CAPACITY_UNSCHEDULED":
        values = add_values(base_line_values, direction["_values"], int(best_pre["mu"]) % PRIMARY_PRIME, PRIMARY_PRIME)
        solved = {
            **best_pre,
            "assignment": joint.exact_assignment_max_min(values),
        }
        solved["failure_mode"] = classify_solved(solved, line_row["proxy_max_min"])
        failure_counts[solved["failure_mode"]] = failure_counts.get(solved["failure_mode"], 0) + 1
    best = solved if solved is not None else best_pre
    best.update(
        {
            "line_hash": line_row["line_hash"],
            "anchor_id": line_row["anchor_id"],
            "lambda": line_row["lambda"],
            "second_direction_hash": direction["vector_hash"],
            "second_active_blocks": direction["active_blocks"],
            "second_active_weak_blocks": direction["active_weak_blocks"],
            "direction_capacity_upper_bound": direction["direction_capacity_upper_bound"],
            "direction_failure_mode": direction["direction_failure_mode"],
            "assignment_solves": int(solved is not None),
            "failure_mode_counts": dict(sorted(failure_counts.items())),
            "plane_hash": hash_payload([line_row["line_hash"], direction["vector_hash"], best["mu"]]),
        }
    )
    return best


def analyze_line(system_row: dict[str, Any], line_row: dict[str, Any]) -> dict[str, Any]:
    core = line.core_for_system(system_row, PRIMARY_PRIME)
    anchors = {anchor["anchor_id"]: anchor for anchor in line.anchor_candidates(core, PRIMARY_PRIME)}
    anchor = anchors[line_row["anchor_id"]]
    q1 = vector_for_basis(core, int(line_row["quotient_basis_index"]))
    q1_values = line.vector_values(core["powers"], q1, PRIMARY_PRIME)
    base_line_values = line.combine_values(anchor["_values"], q1_values, int(line_row["lambda"]), PRIMARY_PRIME)
    directions = quotient_direction_pool(core, line_row)
    plane_rows = [evaluate_plane_for_direction(base_line_values, line_row, direction) for direction in directions]
    plane_rows.sort(
        key=lambda row: (
            row["failure_mode"] == "PLANE_PROXY_CANDIDATE",
            row["failure_mode"] == "PLANE_BALANCE_IMPROVES",
            -1 if row.get("assignment") is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
        ),
        reverse=True,
    )
    failure_counts: dict[str, int] = {}
    for row in plane_rows:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    best = plane_rows[0]
    return {
        "line_hash": line_row["line_hash"],
        "system_id": line_row["system_id"],
        "line_capacity_upper_bound": line_row["capacity_upper_bound"],
        "line_proxy_max_min": line_row["proxy_max_min"],
        "line_six_class_dominance": line_row["six_class_dominance"],
        "line_agreement_vector": line_row["agreement_vector"],
        "weak_blocks": sorted(weak_witness_blocks(line_row["agreement_vector"])),
        "second_directions_tested": len(directions),
        "mu_values_per_direction": len(MU_VALUES),
        "lambda_mu_pairs_tested": len(directions) * len(MU_VALUES),
        "assignment_solves": sum(row["assignment_solves"] for row in plane_rows),
        "best": compact_plane(best),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "retained_planes": [compact_plane(row) for row in plane_rows[:12]],
    }


def compact_plane(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "plane_hash": row["plane_hash"],
        "line_hash": row["line_hash"],
        "mu": row["mu"],
        "second_basis_index": row["second_basis_index"],
        "second_free_column": row["second_free_column"],
        "second_active_blocks": row["second_active_blocks"],
        "second_active_weak_blocks": row["second_active_weak_blocks"],
        "capacity_upper_bound": row["capacity_upper_bound"],
        "proxy_max_min": None if row.get("assignment") is None else row["assignment"]["exact_max_min"],
        "agreement_vector": None if row.get("assignment") is None else row["assignment"]["agreement_vector"],
        "six_class_dominance": row["six_class_dominance"],
        "failure_mode": row["failure_mode"],
        "assignment_solves": row["assignment_solves"],
        "direction_capacity_upper_bound": row["direction_capacity_upper_bound"],
        "direction_failure_mode": row["direction_failure_mode"],
    }


def build_record() -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    soft_rows = soft_row_by_id()
    lines = candidate_lines(source)
    analyses = []
    for line_row in lines:
        analyses.append(analyze_line(soft_rows[line_row["system_id"]], line_row))
    best = max(
        analyses,
        key=lambda row: (
            row["best"]["failure_mode"] == "PLANE_PROXY_CANDIDATE",
            row["best"]["failure_mode"] == "PLANE_BALANCE_IMPROVES",
            -1 if row["best"]["proxy_max_min"] is None else row["best"]["proxy_max_min"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance"],
        ),
    )
    failure_counts: dict[str, int] = {}
    for row in analyses:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    proxy_candidates = [
        row for row in analyses
        if row["best"]["failure_mode"] == "PLANE_PROXY_CANDIDATE"
    ]
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_QUOTIENT_PLANES_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "line_baseline": {
            "best_capacity_upper_bound": source["line_search"]["best_capacity_upper_bound"],
            "best_proxy_max_min": source["line_search"]["best_proxy_max_min"],
            "best_six_class_dominance": source["line_search"]["best_six_class_dominance"],
            "failure_mode": source["line_search"]["best_failure_mode"],
        },
        "construction_mode": "rescheduler_aware_quotient_plane_search",
        "plane_search": {
            "lines_tested": len(analyses),
            "second_directions_tested": sum(row["second_directions_tested"] for row in analyses),
            "lambda_mu_pairs_tested": sum(row["lambda_mu_pairs_tested"] for row in analyses),
            "assignment_solves": sum(row["assignment_solves"] for row in analyses),
            "proxy_plane_candidates": len(proxy_candidates),
            "best_capacity_upper_bound": best["best"]["capacity_upper_bound"],
            "best_proxy_max_min": best["best"]["proxy_max_min"],
            "best_six_class_dominance": best["best"]["six_class_dominance"],
            "best_agreement_vector": best["best"]["agreement_vector"],
            "best_failure_mode": best["best"]["failure_mode"],
            "failure_mode_counts": dict(sorted(failure_counts.items())),
        },
        "lines": analyses,
        "best": best,
        "exact_audit": {
            "triggered": bool(proxy_candidates),
            "best_exact_max_min": None,
        },
        "result_hash": hash_payload(analyses),
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "GF(17^32) proof record",
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
