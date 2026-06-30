#!/usr/bin/env python3
"""Collision-tangent quotient-plane search for the M1 a=327 proxy target."""

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
OUTPUT_DATA = Path("experimental/data/m1_a327_collision_tangent_quotient_plane_search.json")

TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PRIMARY_PRIME = joint.PROXY_PRIME
SOURCE_COMMIT = "84d5194"
LOW_COLLAPSE_THRESHOLD = 20
LINE_COUNT = 5
PROTECTION_BUDGETS = [260, 280, 300, 320]
TANGENT_DIRECTIONS_PER_SPACE = 16
MAX_TANGENT_BASIS_CANDIDATES = 96
MU_VALUES = line.LAMBDA_VALUES
PREVIEW_MU_VALUES = [1, 2, 3, 5, 7, 11, 17, 31]
ASSIGNMENT_SOLVES_PER_SPACE = 4


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
            rows.append({"system_id": system["system_id"], **candidate})
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


def add_values(base_values: list[list[int]], direction_values: list[list[int]], scalar: int, p: int) -> list[list[int]]:
    return [
        [
            (int(base_values[witness][pos]) + scalar * int(direction_values[witness][pos])) % p
            for pos in range(line.N)
        ]
        for witness in range(line.LIST_SIZE)
    ]


def dominant_class_entries(values: list[list[int]]) -> list[dict[str, Any]]:
    entries = []
    for pos in range(line.N):
        buckets: dict[int, int] = {}
        for witness in range(line.LIST_SIZE):
            value = int(values[witness][pos])
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        largest = max(buckets.values(), key=lambda mask: (mask.bit_count(), mask))
        entries.append(
            {
                "pos": pos,
                "mask": int(largest),
                "members": joint.members(int(largest)),
                "size": int(largest).bit_count(),
                "fiber": pos % 16,
            }
        )
    return entries


def protected_classes(values: list[list[int]], budget: int) -> dict[str, Any]:
    entries = dominant_class_entries(values)
    remaining = list(range(len(entries)))
    credits = [0] * line.LIST_SIZE
    selected: list[dict[str, Any]] = []
    while min(credits) < budget and remaining:
        deficits = [max(0, budget - credit) for credit in credits]
        best_idx = max(
            remaining,
            key=lambda idx: (
                sum(deficits[witness] for witness in entries[idx]["members"]),
                entries[idx]["size"],
                -entries[idx]["fiber"],
                -entries[idx]["pos"],
            ),
        )
        if sum(deficits[witness] for witness in entries[best_idx]["members"]) <= 0:
            break
        remaining.remove(best_idx)
        chosen = entries[best_idx]
        selected.append(chosen)
        for witness in chosen["members"]:
            credits[witness] += 1
    constraints = sum(max(0, entry["size"] - 1) for entry in selected)
    return {
        "budget": budget,
        "protected_classes": selected,
        "protected_class_count": len(selected),
        "protected_pair_constraints": constraints,
        "protected_credit_vector": credits,
        "protected_min_credit": min(credits),
        "protected_mask_histogram": histogram(str(entry["mask"]) for entry in selected),
        "protected_size_histogram": histogram(str(entry["size"]) for entry in selected),
        "protected_fiber_histogram": histogram(str(entry["fiber"]) for entry in selected),
    }


def histogram(items: Any) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        out[str(item)] = out.get(str(item), 0) + 1
    return dict(sorted(out.items(), key=lambda row: row[0]))


def vector_for_basis(core: dict[str, Any], basis_index: int) -> np.ndarray:
    return core["null_basis"][int(basis_index)] % PRIMARY_PRIME


def tangent_constraint_row(core: dict[str, Any], left: int, right: int, pos: int) -> np.ndarray:
    powers = core["powers"][pos]
    basis = core["null_basis"]
    row = np.zeros(basis.shape[0], dtype=np.int64)
    if left != 0:
        left_start = (left - 1) * line.K
        row = (row + basis[:, left_start:left_start + line.K] @ powers) % PRIMARY_PRIME
    if right != 0:
        right_start = (right - 1) * line.K
        row = (row - basis[:, right_start:right_start + line.K] @ powers) % PRIMARY_PRIME
    return row % PRIMARY_PRIME


def tangent_space_for(core: dict[str, Any], protected: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for entry in protected["protected_classes"]:
        members = entry["members"]
        if len(members) < 2:
            continue
        left = members[0]
        for right in members[1:]:
            rows.append(tangent_constraint_row(core, left, right, int(entry["pos"])))
    if not rows:
        return {
            "constraint_rank": 0,
            "tangent_dimension": core["null_basis"].shape[0],
            "coefficient_basis": np.identity(core["null_basis"].shape[0], dtype=np.int64),
        }
    matrix = np.vstack(rows) % PRIMARY_PRIME
    echelon, pivots = line.quotient.echelon_modp(matrix, PRIMARY_PRIME)
    coeff_basis, _free_cols = line.quotient.nullspace_basis_matrix(echelon, pivots, core["null_basis"].shape[0], PRIMARY_PRIME)
    return {
        "constraint_rank": len(pivots),
        "tangent_dimension": coeff_basis.shape[0],
        "coefficient_basis": coeff_basis,
    }


def direction_block_activity(vector: np.ndarray) -> list[str]:
    return line.direction_block_activity(vector)


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


def basis_candidate_indices(size: int) -> list[int]:
    if size <= MAX_TANGENT_BASIS_CANDIDATES:
        return list(range(size))
    chosen = set(range(min(32, size)))
    for idx in np.linspace(0, size - 1, MAX_TANGENT_BASIS_CANDIDATES - len(chosen), dtype=int):
        chosen.add(int(idx))
    return sorted(chosen)[:MAX_TANGENT_BASIS_CANDIDATES]


def capacity_collapse_screen(values: list[list[int]]) -> dict[str, Any]:
    capacity = joint.value_class_capacity(values)
    six_dom = line.soft.six_class_dominance(values)
    if capacity["capacity_upper_bound"] < TARGET_AGREEMENT:
        failure_mode = "TANGENT_CAPACITY_LOSS"
    elif six_dom > LOW_COLLAPSE_THRESHOLD:
        failure_mode = "TANGENT_COLLAPSE_RETURNS"
    else:
        failure_mode = "TANGENT_REDUCED_CAPACITY_UNSCHEDULED"
    return {**capacity, "six_class_dominance": six_dom, "failure_mode": failure_mode}


def classify_solved(sample: dict[str, Any], baseline_max_min: int | None) -> str:
    if sample["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "TANGENT_CAPACITY_LOSS"
    if sample["six_class_dominance"] > LOW_COLLAPSE_THRESHOLD:
        return "TANGENT_COLLAPSE_RETURNS"
    assignment = sample.get("assignment")
    if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT:
        return "TANGENT_PROXY_CANDIDATE"
    if assignment is not None and baseline_max_min is not None and assignment["exact_max_min"] > baseline_max_min:
        return "TANGENT_BALANCE_IMPROVES"
    return "TANGENT_LOW_RESCHEDULE"


def direction_preview(
    base_line_values: list[list[int]],
    direction_values: list[list[int]],
) -> dict[str, Any]:
    samples = []
    for mu in PREVIEW_MU_VALUES:
        values = add_values(base_line_values, direction_values, int(mu) % PRIMARY_PRIME, PRIMARY_PRIME)
        sample = capacity_collapse_screen(values)
        sample["mu"] = int(mu)
        samples.append(sample)
    return max(
        samples,
        key=lambda row: (
            row["failure_mode"] == "TANGENT_REDUCED_CAPACITY_UNSCHEDULED",
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["capacity_total"],
        ),
    )


def tangent_direction_pool(
    core: dict[str, Any],
    tangent: dict[str, Any],
    base_line_values: list[list[int]],
    q1_hash: str,
    weak_blocks: set[str],
) -> list[dict[str, Any]]:
    coeff_basis = tangent["coefficient_basis"]
    rows = []
    for basis_idx in basis_candidate_indices(coeff_basis.shape[0]):
        coeff = coeff_basis[basis_idx]
        vector = (coeff @ core["null_basis"]) % PRIMARY_PRIME
        if not np.any(vector[line.K:] % PRIMARY_PRIME):
            continue
        digest = hash_payload(vector.tolist())
        if digest == q1_hash:
            continue
        values = line.vector_values(core["powers"], vector, PRIMARY_PRIME)
        preview = direction_preview(base_line_values, values)
        blocks = direction_block_activity(vector)
        active_weak = len(set(blocks).intersection(weak_blocks))
        rows.append(
            {
                "tangent_basis_index": int(basis_idx),
                "active_blocks": blocks,
                "active_weak_blocks": active_weak,
                "preview_capacity_upper_bound": preview["capacity_upper_bound"],
                "preview_six_class_dominance": preview["six_class_dominance"],
                "preview_failure_mode": preview["failure_mode"],
                "preview_mu": preview["mu"],
                "vector_hash": digest,
                "_values": values,
            }
        )
    rows.sort(
        key=lambda row: (
            row["preview_failure_mode"] == "TANGENT_REDUCED_CAPACITY_UNSCHEDULED",
            row["preview_capacity_upper_bound"],
            row["active_weak_blocks"],
            -row["preview_six_class_dominance"],
            len(row["active_blocks"]),
            -row["tangent_basis_index"],
        ),
        reverse=True,
    )
    return rows[:TANGENT_DIRECTIONS_PER_SPACE]


def prelim_for_direction(
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
                "tangent_basis_index": direction["tangent_basis_index"],
            }
        )
        prelim.append(sample)
    best = max(
        prelim,
        key=lambda row: (
            row["failure_mode"] == "TANGENT_REDUCED_CAPACITY_UNSCHEDULED",
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["capacity_total"],
        ),
    )
    failure_counts: dict[str, int] = {}
    for row in prelim:
        failure_counts[row["failure_mode"]] = failure_counts.get(row["failure_mode"], 0) + 1
    best.update(
        {
            "line_hash": line_row["line_hash"],
            "anchor_id": line_row["anchor_id"],
            "lambda": line_row["lambda"],
            "second_direction_hash": direction["vector_hash"],
            "second_active_blocks": direction["active_blocks"],
            "second_active_weak_blocks": direction["active_weak_blocks"],
            "preview_capacity_upper_bound": direction["preview_capacity_upper_bound"],
            "preview_failure_mode": direction["preview_failure_mode"],
            "assignment_solves": 0,
            "failure_mode_counts": dict(sorted(failure_counts.items())),
            "plane_hash": hash_payload([line_row["line_hash"], direction["vector_hash"], best["mu"]]),
        }
    )
    return best


def solve_prelim(
    base_line_values: list[list[int]],
    direction_values: list[list[int]],
    sample: dict[str, Any],
    line_row: dict[str, Any],
) -> dict[str, Any]:
    values = add_values(base_line_values, direction_values, int(sample["mu"]) % PRIMARY_PRIME, PRIMARY_PRIME)
    solved = {**sample, "assignment": joint.exact_assignment_max_min(values), "assignment_solves": 1}
    solved["failure_mode"] = classify_solved(solved, line_row["proxy_max_min"])
    solved["failure_mode_counts"] = {
        **sample["failure_mode_counts"],
        solved["failure_mode"]: sample["failure_mode_counts"].get(solved["failure_mode"], 0) + 1,
    }
    return solved


def compact_tangent_plane(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "plane_hash": row["plane_hash"],
        "line_hash": row["line_hash"],
        "mu": row["mu"],
        "tangent_basis_index": row["tangent_basis_index"],
        "second_active_blocks": row["second_active_blocks"],
        "second_active_weak_blocks": row["second_active_weak_blocks"],
        "capacity_upper_bound": row["capacity_upper_bound"],
        "proxy_max_min": None if row.get("assignment") is None else row["assignment"]["exact_max_min"],
        "agreement_vector": None if row.get("assignment") is None else row["assignment"]["agreement_vector"],
        "six_class_dominance": row["six_class_dominance"],
        "failure_mode": row["failure_mode"],
        "assignment_solves": row["assignment_solves"],
        "preview_capacity_upper_bound": row["preview_capacity_upper_bound"],
        "preview_failure_mode": row["preview_failure_mode"],
    }


def analyze_tangent_space(
    core: dict[str, Any],
    line_row: dict[str, Any],
    base_line_values: list[list[int]],
    q1_hash: str,
    budget: int,
) -> dict[str, Any]:
    protected = protected_classes(base_line_values, budget)
    tangent = tangent_space_for(core, protected)
    if tangent["tangent_dimension"] == 0:
        return {
            "budget": budget,
            "protected_class_count": protected["protected_class_count"],
            "protected_pair_constraints": protected["protected_pair_constraints"],
            "protected_min_credit": protected["protected_min_credit"],
            "protected_credit_vector": protected["protected_credit_vector"],
            "protected_size_histogram": protected["protected_size_histogram"],
            "constraint_rank": tangent["constraint_rank"],
            "tangent_dimension": 0,
            "tangent_directions_tested": 0,
            "mu_values_tested": 0,
            "assignment_solves": 0,
            "best": {"failure_mode": "TANGENT_SPACE_ZERO", "capacity_upper_bound": None, "proxy_max_min": None, "six_class_dominance": None},
            "failure_mode_counts": {"TANGENT_SPACE_ZERO": 1},
            "retained_planes": [],
        }

    weak_blocks = weak_witness_blocks(line_row["agreement_vector"])
    directions = tangent_direction_pool(core, tangent, base_line_values, q1_hash, weak_blocks)
    prelim_rows = [prelim_for_direction(base_line_values, line_row, direction) for direction in directions]
    prelim_rows.sort(
        key=lambda row: (
            row["failure_mode"] == "TANGENT_REDUCED_CAPACITY_UNSCHEDULED",
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["capacity_total"],
        ),
        reverse=True,
    )
    direction_by_hash = {direction["vector_hash"]: direction for direction in directions}
    solved_rows = []
    solves = 0
    for row in prelim_rows:
        if row["failure_mode"] != "TANGENT_REDUCED_CAPACITY_UNSCHEDULED":
            solved_rows.append(row)
            continue
        if solves >= ASSIGNMENT_SOLVES_PER_SPACE:
            solved_rows.append(row)
            continue
        direction = direction_by_hash[row["second_direction_hash"]]
        solved_rows.append(solve_prelim(base_line_values, direction["_values"], row, line_row))
        solves += 1
    solved_rows.sort(
        key=lambda row: (
            row["failure_mode"] == "TANGENT_PROXY_CANDIDATE",
            row["failure_mode"] == "TANGENT_BALANCE_IMPROVES",
            -1 if row.get("assignment") is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"] if row["capacity_upper_bound"] is not None else -1,
            -1 * (row["six_class_dominance"] if row["six_class_dominance"] is not None else 9999),
        ),
        reverse=True,
    )
    failure_counts: dict[str, int] = {}
    for row in solved_rows:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    return {
        "budget": budget,
        "protected_class_count": protected["protected_class_count"],
        "protected_pair_constraints": protected["protected_pair_constraints"],
        "protected_min_credit": protected["protected_min_credit"],
        "protected_credit_vector": protected["protected_credit_vector"],
        "protected_size_histogram": protected["protected_size_histogram"],
        "constraint_rank": tangent["constraint_rank"],
        "tangent_dimension": tangent["tangent_dimension"],
        "tangent_directions_tested": len(directions),
        "mu_values_tested": len(directions) * len(MU_VALUES),
        "assignment_solves": solves,
        "best": compact_tangent_plane(solved_rows[0]) if solved_rows else {"failure_mode": "TANGENT_SPACE_ZERO"},
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "retained_planes": [compact_tangent_plane(row) for row in solved_rows[:8]],
    }


def analyze_line(system_row: dict[str, Any], line_row: dict[str, Any]) -> dict[str, Any]:
    core = line.core_for_system(system_row, PRIMARY_PRIME)
    anchors = {anchor["anchor_id"]: anchor for anchor in line.anchor_candidates(core, PRIMARY_PRIME)}
    anchor = anchors[line_row["anchor_id"]]
    q1 = vector_for_basis(core, int(line_row["quotient_basis_index"]))
    q1_hash = hash_payload(q1.tolist())
    q1_values = line.vector_values(core["powers"], q1, PRIMARY_PRIME)
    base_line_values = line.combine_values(anchor["_values"], q1_values, int(line_row["lambda"]), PRIMARY_PRIME)
    spaces = [
        analyze_tangent_space(core, line_row, base_line_values, q1_hash, budget)
        for budget in PROTECTION_BUDGETS
    ]
    best = max(
        spaces,
        key=lambda space: (
            space["best"]["failure_mode"] == "TANGENT_PROXY_CANDIDATE",
            space["best"]["failure_mode"] == "TANGENT_BALANCE_IMPROVES",
            -1 if space["best"].get("proxy_max_min") is None else space["best"]["proxy_max_min"],
            -1 if space["best"].get("capacity_upper_bound") is None else space["best"]["capacity_upper_bound"],
            -9999 if space["best"].get("six_class_dominance") is None else -space["best"]["six_class_dominance"],
        ),
    )
    failure_counts: dict[str, int] = {}
    for space in spaces:
        for failure, count in space["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    return {
        "line_hash": line_row["line_hash"],
        "system_id": line_row["system_id"],
        "line_capacity_upper_bound": line_row["capacity_upper_bound"],
        "line_proxy_max_min": line_row["proxy_max_min"],
        "line_six_class_dominance": line_row["six_class_dominance"],
        "line_agreement_vector": line_row["agreement_vector"],
        "protection_budgets": PROTECTION_BUDGETS,
        "tangent_spaces_built": len(spaces),
        "tangent_directions_tested": sum(space["tangent_directions_tested"] for space in spaces),
        "mu_values_tested": sum(space["mu_values_tested"] for space in spaces),
        "assignment_solves": sum(space["assignment_solves"] for space in spaces),
        "best": best["best"],
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "tangent_spaces": spaces,
    }


def build_record() -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    soft_rows = soft_row_by_id()
    lines = candidate_lines(source)
    analyses = [analyze_line(soft_rows[line_row["system_id"]], line_row) for line_row in lines]
    best = max(
        analyses,
        key=lambda row: (
            row["best"]["failure_mode"] == "TANGENT_PROXY_CANDIDATE",
            row["best"]["failure_mode"] == "TANGENT_BALANCE_IMPROVES",
            -1 if row["best"].get("proxy_max_min") is None else row["best"]["proxy_max_min"],
            -1 if row["best"].get("capacity_upper_bound") is None else row["best"]["capacity_upper_bound"],
            -9999 if row["best"].get("six_class_dominance") is None else -row["best"]["six_class_dominance"],
        ),
    )
    failure_counts: dict[str, int] = {}
    for row in analyses:
        for failure, count in row["failure_mode_counts"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    proxy_candidates = [row for row in analyses if row["best"]["failure_mode"] == "TANGENT_PROXY_CANDIDATE"]
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_TANGENT_PLANES_NO_A327"
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
        "construction_mode": "collision_tangent_quotient_plane_search",
        "tangent_search": {
            "line_candidates_tested": len(analyses),
            "protection_budgets": PROTECTION_BUDGETS,
            "tangent_spaces_built": sum(row["tangent_spaces_built"] for row in analyses),
            "tangent_directions_tested": sum(row["tangent_directions_tested"] for row in analyses),
            "mu_values_tested": sum(row["mu_values_tested"] for row in analyses),
            "assignment_solves": sum(row["assignment_solves"] for row in analyses),
            "proxy_candidates": len(proxy_candidates),
            "best_capacity_upper_bound": best["best"].get("capacity_upper_bound"),
            "best_proxy_max_min": best["best"].get("proxy_max_min"),
            "best_six_class_dominance": best["best"].get("six_class_dominance"),
            "best_agreement_vector": best["best"].get("agreement_vector"),
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
