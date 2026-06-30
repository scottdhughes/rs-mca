#!/usr/bin/env python3
"""Affine collapse-plus-quotient line search for the M1 a=327 proxy target."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np

import scan_m1_a327_balanced_target_milp_codeword_solver as balanced
import scan_m1_a327_collapse_subspace_quotient_solver as quotient
import scan_m1_a327_joint_target_codeword_solver as joint
import scan_m1_a327_proxy_positive_exact_extraction as proxy_exact
import scan_m1_a327_soft_collapse_penalty_target_solver as soft


SOURCE_DATA = Path("experimental/data/m1_a327_collapse_subspace_quotient_solver.json")
SOFT_DATA = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_collapse_quotient_line_search.json")

N = joint.N
K = joint.K
LIST_SIZE = joint.LIST_SIZE
VARIABLE_COUNT = joint.VARIABLE_COUNT
TARGET_AGREEMENT = joint.TARGET_AGREEMENT
PRIMARY_PRIME = joint.PROXY_PRIME
CONFIRMATION_PRIMES = [7681, 10753, 11777, 13313]
SOURCE_COMMIT = "8dbcb6b"
COLLAPSE_CLASS = [1, 3, 4, 5, 6, 7]

ANCHORS_PER_SYSTEM = 3
DIRECTIONS_PER_SYSTEM = 16
RETAINED_LINES_PER_SYSTEM = 16
CONFIRMATION_LINE_COUNT = 5
LAMBDA_VALUES = [
    1,
    2,
    3,
    4,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    109,
    113,
    127,
    131,
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


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def vector_values(powers: np.ndarray, vector: np.ndarray, p: int) -> list[list[int]]:
    values = [[0] * N]
    for witness in range(LIST_SIZE - 1):
        start = witness * K
        coeffs = vector[start:start + K] % p
        witness_values = (powers @ coeffs) % p
        values.append([int(value) for value in witness_values])
    return values


def combine_values(anchor_values: list[list[int]], direction_values: list[list[int]], scalar: int, p: int) -> list[list[int]]:
    return [
        [
            (int(anchor_values[witness][pos]) + scalar * int(direction_values[witness][pos])) % p
            for pos in range(N)
        ]
        for witness in range(LIST_SIZE)
    ]


def eval_values(
    values: list[list[int]],
    family: str,
    detail: str,
    anchor_dom: int | None = None,
    solve_assignment: bool = True,
) -> dict[str, Any]:
    capacity = joint.value_class_capacity(values)
    six_dom = soft.six_class_dominance(values)
    assignment = None
    if anchor_dom is not None and six_dom >= anchor_dom and capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        failure_mode = "LINE_COLLAPSE_PERSISTS"
    elif capacity["capacity_upper_bound"] >= TARGET_AGREEMENT and solve_assignment:
        assignment = joint.exact_assignment_max_min(values)
        if assignment is None or assignment["exact_max_min"] < TARGET_AGREEMENT:
            failure_mode = "LINE_LOW_RESCHEDULE"
        elif anchor_dom is not None and six_dom < anchor_dom:
            failure_mode = "LINE_PROXY_CANDIDATE"
        else:
            failure_mode = "LINE_COLLAPSE_PERSISTS"
    elif capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        failure_mode = "LINE_REDUCED_CAPACITY_UNSCHEDULED"
    else:
        failure_mode = "LINE_CAPACITY_LOSS"
    return {
        "sample_family": family,
        "sample_detail": detail,
        **capacity,
        "assignment": assignment,
        "six_class_dominance": six_dom,
        "failure_mode": failure_mode,
    }


def core_for_system(row: dict[str, Any], p: int) -> dict[str, Any]:
    source = quotient.source_for_row(row)
    selection = quotient.selected_soft_rows(source, row)
    if p == PRIMARY_PRIME:
        powers = joint.vandermonde_powers(joint.proxy_subgroup())
        rows = balanced.rows_for_selected(powers, selection["selected"])
    else:
        powers = proxy_exact.vandermonde_powers_modp(p)
        rows = proxy_exact.rows_for_selected_modp(powers, selection["selected"], p)
    echelon, pivots = quotient.echelon_modp(rows, p)
    null_basis, free_cols = quotient.nullspace_basis_matrix(echelon, pivots, VARIABLE_COUNT, p)
    collapse_basis, collapse_dim = collapse_basis_for_rows_modp(rows, p)
    return {
        "source": source,
        "selection": selection,
        "powers": powers,
        "rows": rows,
        "echelon": echelon,
        "pivots": pivots,
        "null_basis": null_basis,
        "free_cols": free_cols,
        "collapse_basis": collapse_basis,
        "collapse_dim": collapse_dim,
        "rank": len(pivots),
        "nullity": VARIABLE_COUNT - len(pivots),
    }


def collapse_basis_for_rows_modp(rows: np.ndarray, p: int) -> tuple[np.ndarray, int]:
    restricted = rows[:, :K] % p
    echelon, pivots = quotient.echelon_modp(restricted, p)
    small_basis, _free_cols = quotient.nullspace_basis_matrix(echelon, pivots, K, p)
    full_basis = np.zeros((small_basis.shape[0], VARIABLE_COUNT), dtype=np.int64)
    full_basis[:, :K] = small_basis
    return full_basis, small_basis.shape[0]


def anchor_candidates(core: dict[str, Any], p: int) -> list[dict[str, Any]]:
    basis = core["collapse_basis"]
    powers = core["powers"]
    vectors: list[tuple[str, np.ndarray]] = []
    if basis.shape[0]:
        weighted = np.zeros(VARIABLE_COUNT, dtype=np.int64)
        for idx, vector in enumerate(basis[: min(16, basis.shape[0])]):
            weighted = (weighted + (idx + 1) * vector) % p
        vectors.append(("weighted_first_16", weighted))
        for idx, vector in enumerate(basis[: min(8, basis.shape[0])]):
            vectors.append((f"basis_{idx}", vector % p))
    anchors = []
    seen = set()
    for anchor_id, vector in vectors:
        digest = hash_payload(vector.tolist())
        if digest in seen or not np.any(vector):
            continue
        seen.add(digest)
        values = vector_values(powers, vector, p)
        sample = eval_values(values, "collapse_anchor", anchor_id)
        sample["anchor_id"] = anchor_id
        sample["vector_hash"] = digest
        sample["_vector"] = vector
        sample["_values"] = values
        anchors.append(sample)
    anchors.sort(
        key=lambda row: (
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["anchor_id"],
        ),
        reverse=True,
    )
    return anchors[:ANCHORS_PER_SYSTEM]


def direction_block_activity(vector: np.ndarray) -> list[str]:
    blocks = []
    for block in range(LIST_SIZE - 1):
        start = block * K
        if np.any(vector[start:start + K] % PRIMARY_PRIME):
            blocks.append(f"D_{block + 2}")
    return blocks


def quotient_directions(core: dict[str, Any], p: int) -> list[dict[str, Any]]:
    powers = core["powers"]
    rows = []
    for idx, vector in enumerate(core["null_basis"]):
        if not np.any(vector[K:] % p):
            continue
        values = vector_values(powers, vector, p)
        sample = eval_values(values, "quotient_direction", f"basis_{idx}", solve_assignment=False)
        free_col = int(core["free_cols"][idx])
        blocks = direction_block_activity(vector)
        sample.update(
            {
                "basis_index": idx,
                "free_column": free_col,
                "free_block": f"D_{free_col // K + 2}",
                "active_blocks": blocks,
                "active_block_count": len(blocks),
                "vector_hash": hash_payload(vector.tolist()),
                "_vector": vector,
                "_values": values,
            }
        )
        rows.append(sample)
    rows.sort(
        key=lambda row: (
            row["capacity_upper_bound"],
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["active_block_count"],
            -row["six_class_dominance"],
            -row["basis_index"],
        ),
        reverse=True,
    )
    return rows[:DIRECTIONS_PER_SYSTEM]


def line_eval(anchor: dict[str, Any], direction: dict[str, Any], scalar: int, p: int, solve_assignment: bool = True) -> dict[str, Any]:
    values = combine_values(anchor["_values"], direction["_values"], scalar, p)
    sample = eval_values(
        values,
        "collapse_quotient_line",
        f"{anchor['anchor_id']}+{scalar}*{direction['basis_index']}",
        anchor["six_class_dominance"],
        solve_assignment=solve_assignment,
    )
    sample.update(
        {
            "anchor_id": anchor["anchor_id"],
            "anchor_hash": anchor["vector_hash"],
            "quotient_basis_index": direction["basis_index"],
            "quotient_free_column": direction["free_column"],
            "lambda": int(scalar),
            "line_hash": hash_payload([anchor["vector_hash"], direction["vector_hash"], int(scalar), p]),
        }
    )
    return sample


def best_line_for_direction(anchor: dict[str, Any], direction: dict[str, Any], p: int) -> dict[str, Any]:
    preliminary = [line_eval(anchor, direction, scalar % p, p, solve_assignment=False) for scalar in LAMBDA_VALUES if scalar % p]
    best_preliminary = max(
        preliminary,
        key=lambda row: (
            row["failure_mode"] == "LINE_REDUCED_CAPACITY_UNSCHEDULED",
            row["capacity_upper_bound"],
            -row["six_class_dominance"],
            row["capacity_total"],
        ),
    )
    if best_preliminary["failure_mode"] == "LINE_REDUCED_CAPACITY_UNSCHEDULED":
        best = line_eval(anchor, direction, int(best_preliminary["lambda"]) % p, p, solve_assignment=True)
    else:
        best = best_preliminary
    failure_counts: dict[str, int] = {}
    for sample in preliminary:
        failure_counts[sample["failure_mode"]] = failure_counts.get(sample["failure_mode"], 0) + 1
    if best_preliminary["failure_mode"] == "LINE_REDUCED_CAPACITY_UNSCHEDULED":
        failure_counts[best["failure_mode"]] = failure_counts.get(best["failure_mode"], 0) + 1
    return {
        **best,
        "lambda_values_tested": len(preliminary),
        "assignment_solves": int(best_preliminary["failure_mode"] == "LINE_REDUCED_CAPACITY_UNSCHEDULED"),
        "failure_mode_counts": dict(sorted(failure_counts.items())),
        "direction_capacity_upper_bound": direction["capacity_upper_bound"],
        "direction_failure_mode": direction["failure_mode"],
        "direction_active_blocks": direction["active_blocks"],
    }


def confirm_line(system_row: dict[str, Any], line: dict[str, Any], p: int) -> dict[str, Any]:
    core = core_for_system(system_row, p)
    anchors = {anchor["anchor_id"]: anchor for anchor in anchor_candidates(core, p)}
    anchor = anchors.get(line["anchor_id"])
    if anchor is None:
        return {"prime": p, "status": "ANCHOR_NOT_AVAILABLE"}
    try:
        q_idx = core["free_cols"].index(int(line["quotient_free_column"]))
    except ValueError:
        return {"prime": p, "status": "FREE_COLUMN_NOT_AVAILABLE"}
    q_vector = core["null_basis"][q_idx]
    if not np.any(q_vector[K:] % p):
        return {"prime": p, "status": "FREE_COLUMN_COLLAPSE_ONLY"}
    q_values = vector_values(core["powers"], q_vector, p)
    direction = {
        "basis_index": q_idx,
        "free_column": int(line["quotient_free_column"]),
        "vector_hash": hash_payload(q_vector.tolist()),
        "_values": q_values,
    }
    sample = line_eval(anchor, direction, int(line["lambda"]) % p, p, solve_assignment=False)
    return {
        "prime": p,
        "status": "REPLAYED",
        "capacity_upper_bound": sample["capacity_upper_bound"],
        "proxy_max_min": None if sample["assignment"] is None else sample["assignment"]["exact_max_min"],
        "six_class_dominance": sample["six_class_dominance"],
        "failure_mode": sample["failure_mode"],
        "confirmation_mode": "capacity_and_collapse_no_rescheduler",
    }


def analyze_system(row: dict[str, Any]) -> dict[str, Any]:
    core = core_for_system(row, PRIMARY_PRIME)
    anchors = anchor_candidates(core, PRIMARY_PRIME)
    directions = quotient_directions(core, PRIMARY_PRIME)
    line_rows = []
    for anchor in anchors:
        for direction in directions:
            line_rows.append(best_line_for_direction(anchor, direction, PRIMARY_PRIME))
    line_rows.sort(
        key=lambda line: (
            line["failure_mode"] == "LINE_PROXY_CANDIDATE",
            -1 if line["assignment"] is None else line["assignment"]["exact_max_min"],
            line["capacity_upper_bound"],
            -line["six_class_dominance"],
            line["capacity_total"],
        ),
        reverse=True,
    )
    retained_lines = line_rows[:RETAINED_LINES_PER_SYSTEM]
    top_for_confirm = retained_lines[:CONFIRMATION_LINE_COUNT]
    confirmations = [
        {
            "line_hash": line["line_hash"],
            "anchor_id": line["anchor_id"],
            "quotient_free_column": line["quotient_free_column"],
            "lambda": line["lambda"],
            "prime_results": [confirm_line(row, line, p) for p in CONFIRMATION_PRIMES],
        }
        for line in top_for_confirm
    ]
    failure_counts: dict[str, int] = {}
    lambda_failure_counts: dict[str, int] = {}
    for line in line_rows:
        failure_counts[line["failure_mode"]] = failure_counts.get(line["failure_mode"], 0) + 1
        for failure, count in line["failure_mode_counts"].items():
            lambda_failure_counts[failure] = lambda_failure_counts.get(failure, 0) + count
    best = retained_lines[0]
    return {
        "system_id": row["target_system_id"],
        "row_budget": row["row_budget"],
        "lambda_collapse_penalty": row["lambda_collapse_penalty"],
        "selection_objective": row["selection_objective"],
        "target_rows_hash": row["target_rows_hash"],
        "proxy_rank": core["rank"],
        "proxy_nullity": core["nullity"],
        "collapse_subspace_dimension": core["collapse_dim"],
        "quotient_dimension": core["nullity"] - core["collapse_dim"],
        "anchors_tested": len(anchors),
        "quotient_directions_tested": len(directions),
        "lambda_values_per_line": len(LAMBDA_VALUES),
        "lambda_values_tested": len(anchors) * len(directions) * len(LAMBDA_VALUES),
        "best": compact_line(best),
        "failure_mode_counts_by_line": dict(sorted(failure_counts.items())),
        "failure_mode_counts_by_lambda": dict(sorted(lambda_failure_counts.items())),
        "anchors": [compact_anchor(anchor) for anchor in anchors],
        "directions": [compact_direction(direction) for direction in directions[:16]],
        "retained_lines": [compact_line(line) for line in retained_lines],
        "multiprime_confirmation": confirmations,
    }


def compact_anchor(anchor: dict[str, Any]) -> dict[str, Any]:
    return {
        "anchor_id": anchor["anchor_id"],
        "capacity_upper_bound": anchor["capacity_upper_bound"],
        "proxy_max_min": None if anchor["assignment"] is None else anchor["assignment"]["exact_max_min"],
        "six_class_dominance": anchor["six_class_dominance"],
        "vector_hash": anchor["vector_hash"],
    }


def compact_direction(direction: dict[str, Any]) -> dict[str, Any]:
    return {
        "basis_index": direction["basis_index"],
        "free_column": direction["free_column"],
        "free_block": direction["free_block"],
        "active_blocks": direction["active_blocks"],
        "capacity_upper_bound": direction["capacity_upper_bound"],
        "proxy_max_min": None if direction["assignment"] is None else direction["assignment"]["exact_max_min"],
        "six_class_dominance": direction["six_class_dominance"],
        "failure_mode": direction["failure_mode"],
        "vector_hash": direction["vector_hash"],
    }


def compact_line(line: dict[str, Any]) -> dict[str, Any]:
    return {
        "line_hash": line["line_hash"],
        "anchor_id": line["anchor_id"],
        "quotient_basis_index": line["quotient_basis_index"],
        "quotient_free_column": line["quotient_free_column"],
        "lambda": line["lambda"],
        "capacity_upper_bound": line["capacity_upper_bound"],
        "proxy_max_min": None if line["assignment"] is None else line["assignment"]["exact_max_min"],
        "agreement_vector": None if line["assignment"] is None else line["assignment"]["agreement_vector"],
        "six_class_dominance": line["six_class_dominance"],
        "failure_mode": line["failure_mode"],
        "assignment_solves": line["assignment_solves"],
        "direction_capacity_upper_bound": line["direction_capacity_upper_bound"],
        "direction_failure_mode": line["direction_failure_mode"],
        "direction_active_blocks": line["direction_active_blocks"],
        "failure_mode_counts": line["failure_mode_counts"],
    }


def build_record() -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    soft_source = load_json(SOFT_DATA)
    soft_rows_by_id = {row["target_system_id"]: row for row in soft_source["retained_results"]}
    systems = [soft_rows_by_id[row["system_id"]] for row in source["systems"]]
    analyses = [analyze_system(row) for row in systems]
    best = max(
        analyses,
        key=lambda row: (
            row["best"]["failure_mode"] == "LINE_PROXY_CANDIDATE",
            -1 if row["best"]["proxy_max_min"] is None else row["best"]["proxy_max_min"],
            row["best"]["capacity_upper_bound"],
            -row["best"]["six_class_dominance"],
        ),
    )
    proxy_candidates = [
        line
        for row in analyses
        for line in row["retained_lines"]
        if line["failure_mode"] == "LINE_PROXY_CANDIDATE"
    ]
    failure_counts: dict[str, int] = {}
    for row in analyses:
        for failure, count in row["failure_mode_counts_by_lambda"].items():
            failure_counts[failure] = failure_counts.get(failure, 0) + count
    proof_status = "CANDIDATE" if proxy_candidates else "TESTED_QUOTIENT_LINES_NO_A327"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "collapse_subspace": {
            "systems_tested": source["proxy_systems"]["systems_tested"],
            "collapse_dimension": source["collapse_quotient"]["collapse_subspace_dimensions"][0],
            "quotient_dimension": source["collapse_quotient"]["quotient_dimensions"][0],
            "best_collapse_capacity": source["collapse_quotient"]["best_capacity_upper_bound"],
            "best_collapse_proxy_max_min": source["collapse_quotient"]["best_proxy_max_min"],
            "best_six_class_dominance": source["collapse_quotient"]["best_six_class_dominance"],
        },
        "construction_mode": "collapse_quotient_line_search",
        "line_search": {
            "anchors_tested": sum(row["anchors_tested"] for row in analyses),
            "quotient_directions_tested": sum(row["quotient_directions_tested"] for row in analyses),
            "lambda_values_tested": sum(row["lambda_values_tested"] for row in analyses),
            "proxy_line_candidates": len(proxy_candidates),
            "best_capacity_upper_bound": best["best"]["capacity_upper_bound"],
            "best_proxy_max_min": best["best"]["proxy_max_min"],
            "best_six_class_dominance": best["best"]["six_class_dominance"],
            "best_failure_mode": best["best"]["failure_mode"],
            "failure_mode_counts": dict(sorted(failure_counts.items())),
        },
        "systems": analyses,
        "best": best,
        "exact_audit": {
            "triggered": bool(proxy_candidates),
            "exact_vectors_constructed": 0,
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
