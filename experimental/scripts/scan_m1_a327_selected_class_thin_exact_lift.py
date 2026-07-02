#!/usr/bin/env python3
"""Thin selected-class hypergraph targets for exact M1 a=327 lifting."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import sys
from numbers import Integral
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "2e134d7"
SOURCE_DATA = Path("experimental/data/m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.json")
SOURCE_SCANNER = Path("experimental/scripts/scan_m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.py")
OUTPUT_DATA = Path("experimental/data/m1_a327_selected_class_thin_exact_lift.json")

N = 512
FIBER_COUNT = 16
FIBER_SIZE = 32
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR7_LABELS = ["B17", "B27", "B37", "B47", "B57"]
PAIR_INDICES = [(i, j) for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)]
PAIR_LABELS = [f"P{i + 1}{j + 1}" for i, j in PAIR_INDICES]
PAIR7_INDICES = [(idx, 6) for idx in range(5)]
SOURCE_PROFILE_ID = "selected_4_5_paircap255"

THIN_STRATEGIES = [
    {"strategy": "balanced_support_thin", "seed": 0, "pair7_weight": 0.25, "max_pair_weight": 1.0},
    {"strategy": "pair7_preserving_thin", "seed": 1, "pair7_weight": 2.0, "max_pair_weight": 1.0},
    {"strategy": "fiber_balanced_thin", "seed": 2, "pair7_weight": 0.5, "max_pair_weight": 1.0},
    {"strategy": "max_pair_minimizing_thin", "seed": 3, "pair7_weight": 0.0, "max_pair_weight": 2.0},
    {"strategy": "random_seeded_thin_0", "seed": 101, "pair7_weight": 0.75, "max_pair_weight": 1.0},
    {"strategy": "random_seeded_thin_1", "seed": 202, "pair7_weight": 0.75, "max_pair_weight": 1.0},
    {"strategy": "random_seeded_thin_2", "seed": 303, "pair7_weight": 0.75, "max_pair_weight": 1.0},
]


def load_source_scanner():
    script_dir = str(SOURCE_SCANNER.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location("rs_feasible_valueclass_scanner", SOURCE_SCANNER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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


def mask_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(LIST_SIZE) if mask & (1 << idx)]


def contains(mask: int, idx: int) -> int:
    return int(bool(mask & (1 << idx)))


def pair_same(mask: int, pair: tuple[int, int]) -> int:
    left, right = pair
    return int(bool(mask & (1 << left)) and bool(mask & (1 << right)))


def submasks(mask: int) -> list[int]:
    bits = [idx for idx in range(LIST_SIZE) if mask & (1 << idx)]
    out = []
    for size in range(3, len(bits) + 1):
        for combo in __import__("itertools").combinations(bits, size):
            submask = 0
            for idx in combo:
                submask |= 1 << idx
            out.append(submask)
    return sorted(set(out), key=lambda value: (value.bit_count(), value))


def source_selected_counts() -> tuple[list[tuple[int, int]], dict[str, Any]]:
    scanner = load_source_scanner()
    spec = next(row for row in scanner.PROFILE_SPECS if row["profile_id"] == SOURCE_PROFILE_ID)
    classes = scanner.subset_masks(spec["selected_class_sizes"])
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(f"scipy unavailable: {exc}") from exc

    rows = scanner.coefficient_rows(classes)
    var_count = len(classes) + 1
    t_idx = len(classes)
    objective = np.zeros(var_count)
    objective[t_idx] = -1000.0
    for idx, mask in enumerate(classes):
        objective[idx] += 0.01 * int((mask & scanner.FRAGILE_1457) == scanner.FRAGILE_1457)
        objective[idx] += 0.001 * mask.bit_count()

    constraints = []
    lower = []
    upper = []
    row = np.zeros(var_count)
    row[: len(classes)] = 1
    constraints.append(row)
    lower.append(N)
    upper.append(N)
    states = ["pre_split", *scanner.SPLIT_PROBES.keys()]
    for state in states:
        prefix = "" if state == "pre_split" else f"{state}:"
        for idx in range(LIST_SIZE):
            row = np.zeros(var_count)
            row[: len(classes)] = rows[f"{prefix}support_{idx + 1}"]
            row[t_idx] = -1
            constraints.append(row)
            lower.append(TARGET_AGREEMENT)
            upper.append(float("inf"))
        for label, pair in zip(scanner.PAIR_LABELS, scanner.PAIR_INDICES, strict=True):
            row = np.zeros(var_count)
            row[: len(classes)] = rows[f"{prefix}pair_{label}"]
            row[t_idx] = 1
            constraints.append(row)
            lower.append(float("-inf"))
            upper.append(PAIR_CAP)
        for pair in PAIR7_INDICES:
            pair_label = f"P{pair[0] + 1}{pair[1] + 1}"
            row = np.zeros(var_count)
            row[: len(classes)] = rows[f"{prefix}pair_{pair_label}"]
            row[t_idx] = -1
            constraints.append(row)
            lower.append(PAIR7_LOWER)
            upper.append(float("inf"))

    result = milp(
        objective,
        integrality=np.r_[np.ones(len(classes)), np.zeros(1)],
        bounds=Bounds(np.r_[np.zeros(len(classes)), -N], np.r_[N * np.ones(len(classes)), N]),
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 30},
    )
    if not result.success:
        raise RuntimeError(f"source MILP failed: {result.message}")
    counts = [int(round(value)) for value in result.x[: len(classes)]]
    used = [(mask, count) for mask, count in zip(classes, counts, strict=True) if count]
    summary = scanner.evaluate_counts(used, PAIR_CAP)
    summary["selected_count_hash"] = hash_payload([
        {"selected_class": mask_members(mask), "count": count} for mask, count in used
    ])
    return used, summary


def transition_list(source_counts: list[tuple[int, int]]) -> list[dict[str, Any]]:
    out = []
    for source_idx, (source_mask, source_count) in enumerate(source_counts):
        for target_mask in submasks(source_mask):
            out.append(
                {
                    "source_idx": source_idx,
                    "source_mask": source_mask,
                    "source_count": source_count,
                    "target_mask": target_mask,
                    "removed_incidence_count": source_mask.bit_count() - target_mask.bit_count(),
                }
            )
    return out


def solve_thin(source_counts: list[tuple[int, int]], strategy: dict[str, Any]) -> dict[str, Any]:
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover
        return {
            "strategy": strategy["strategy"],
            "solver_status": "SCIPY_UNAVAILABLE",
            "solver_error": str(exc),
            "failure_mode": "THIN_SUPPORT_FAIL",
        }

    transitions = transition_list(source_counts)
    rng = random.Random(int(strategy["seed"]))
    var_count = len(transitions) + 2
    max_pair_idx = len(transitions)
    min_pair7_idx = len(transitions) + 1
    objective = np.zeros(var_count)
    objective[max_pair_idx] = float(strategy["max_pair_weight"])
    objective[min_pair7_idx] = -float(strategy["pair7_weight"])
    for idx, transition in enumerate(transitions):
        objective[idx] = 0.0001 * transition["target_mask"].bit_count() + 0.00001 * rng.random()

    constraints = []
    lower = []
    upper = []

    for source_idx, (_source_mask, source_count) in enumerate(source_counts):
        row = np.zeros(var_count)
        for idx, transition in enumerate(transitions):
            if transition["source_idx"] == source_idx:
                row[idx] = 1
        constraints.append(row)
        lower.append(source_count)
        upper.append(source_count)

    for witness in range(LIST_SIZE):
        row = np.zeros(var_count)
        for idx, transition in enumerate(transitions):
            row[idx] = contains(transition["target_mask"], witness)
        constraints.append(row)
        lower.append(TARGET_AGREEMENT)
        upper.append(TARGET_AGREEMENT)

    for pair in PAIR_INDICES:
        row = np.zeros(var_count)
        for idx, transition in enumerate(transitions):
            row[idx] = pair_same(transition["target_mask"], pair)
        row[max_pair_idx] = -1
        constraints.append(row)
        lower.append(float("-inf"))
        upper.append(0)

        cap_row = np.zeros(var_count)
        for idx, transition in enumerate(transitions):
            cap_row[idx] = pair_same(transition["target_mask"], pair)
        constraints.append(cap_row)
        lower.append(float("-inf"))
        upper.append(PAIR_CAP)

    for pair in PAIR7_INDICES:
        row = np.zeros(var_count)
        for idx, transition in enumerate(transitions):
            row[idx] = pair_same(transition["target_mask"], pair)
        row[min_pair7_idx] = -1
        constraints.append(row)
        lower.append(0)
        upper.append(float("inf"))

        guard_row = np.zeros(var_count)
        for idx, transition in enumerate(transitions):
            guard_row[idx] = pair_same(transition["target_mask"], pair)
        constraints.append(guard_row)
        lower.append(PAIR7_LOWER)
        upper.append(float("inf"))

    result = milp(
        objective,
        integrality=np.r_[np.ones(len(transitions)), np.zeros(2)],
        bounds=Bounds(
            np.r_[np.zeros(len(transitions)), np.zeros(2)],
            np.r_[N * np.ones(len(transitions)), N * np.ones(2)],
        ),
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 30},
    )
    if not result.success:
        return {
            "strategy": strategy["strategy"],
            "solver_status": "INFEASIBLE_OR_LIMIT",
            "solver_message": str(result.message),
            "failure_mode": "THIN_SUPPORT_FAIL",
        }

    counts: dict[int, int] = {}
    transition_rows = []
    for transition, value in zip(transitions, result.x[: len(transitions)], strict=True):
        count = int(round(value))
        if count <= 0:
            continue
        mask = transition["target_mask"]
        counts[mask] = counts.get(mask, 0) + count
        transition_rows.append(
            {
                "source_class": mask_members(transition["source_mask"]),
                "target_class": mask_members(mask),
                "count": count,
            }
        )
    selected_counts = sorted(counts.items(), key=lambda item: (item[0].bit_count(), item[0]))
    summary = evaluate_selected_counts(selected_counts)
    summary.update(
        {
            "strategy": strategy["strategy"],
            "solver_status": "OPTIMAL_OR_FEASIBLE",
            "solver_message": str(result.message),
            "objective_value": float(result.fun),
            "thin_count_hash": hash_payload([
                {"selected_class": mask_members(mask), "count": count}
                for mask, count in selected_counts
            ]),
            "transition_hash": hash_payload(transition_rows),
            "top_selected_class_counts": [
                {"members": mask_members(mask), "size": mask.bit_count(), "count": count}
                for mask, count in sorted(selected_counts, key=lambda item: (-item[1], item[0]))[:16]
            ],
        }
    )
    summary["failure_mode"] = classify_thin(summary)
    return summary


def evaluate_selected_counts(selected_counts: list[tuple[int, int]]) -> dict[str, Any]:
    supports = [sum(count * contains(mask, idx) for mask, count in selected_counts) for idx in range(LIST_SIZE)]
    pair_counts = {
        label: sum(count * pair_same(mask, pair) for mask, count in selected_counts)
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True)
    }
    pair7_counts = {
        label: pair_counts[f"P{pair[0] + 1}{pair[1] + 1}"]
        for pair, label in zip(PAIR7_INDICES, PAIR7_LABELS, strict=True)
    }
    size_counts: dict[str, int] = {}
    for mask, count in selected_counts:
        size_counts[str(mask.bit_count())] = size_counts.get(str(mask.bit_count()), 0) + count
    max_pair_label, max_pair_count = max(pair_counts.items(), key=lambda item: item[1])
    selected_incidence_count = sum(count * mask.bit_count() for mask, count in selected_counts)
    pair_b_values = [N + pair7_counts[label] for label in PAIR7_LABELS]
    return {
        "supports": supports,
        "support_exact": supports == [TARGET_AGREEMENT] * LIST_SIZE,
        "pair_counts": pair_counts,
        "max_pair_label": max_pair_label,
        "max_pair_count": max_pair_count,
        "pair_cap_pass": max_pair_count <= PAIR_CAP,
        "pair7_counts": pair7_counts,
        "pair7_counts_vector": [pair7_counts[label] for label in PAIR7_LABELS],
        "pair7_guard_pass": min(pair7_counts.values()) >= PAIR7_LOWER,
        "pair_B_values": pair_b_values,
        "selected_class_size_counts": dict(sorted(size_counts.items())),
        "selected_incidence_count": selected_incidence_count,
        "coordinate_count": sum(count for _mask, count in selected_counts),
        "selected_counts": [
            {"mask": mask, "members": mask_members(mask), "count": count}
            for mask, count in selected_counts
        ],
        "coordinate_classes": coordinate_classes(selected_counts),
    }


def coordinate_classes(selected_counts: list[tuple[int, int]]) -> list[dict[str, Any]]:
    expanded = []
    for mask, count in selected_counts:
        expanded.extend([mask] * count)
    expanded.sort(key=lambda mask: (hash_payload(mask_members(mask)), mask))
    positions = list(range(N))
    positions.sort(key=lambda pos: (pos % FIBER_COUNT, pos // FIBER_COUNT))
    rows = []
    for position, mask in zip(positions, expanded, strict=True):
        rows.append(
            {
                "position": position,
                "fiber": position % FIBER_COUNT,
                "mask": mask,
                "members": mask_members(mask),
                "size": mask.bit_count(),
            }
        )
    return sorted(rows, key=lambda row: row["position"])


def classify_thin(row: dict[str, Any]) -> str:
    if not row["support_exact"]:
        return "THIN_SUPPORT_FAIL"
    if not row["pair_cap_pass"]:
        return "THIN_PAIR_CAP_FAIL"
    if not row["pair7_guard_pass"]:
        return "THIN_PAIR7_GUARD_FAIL"
    return "THIN_LIFT_TARGET"


def best_thin(candidates: list[dict[str, Any]]) -> dict[str, Any] | None:
    valid = [row for row in candidates if row.get("failure_mode") == "THIN_LIFT_TARGET"]
    pool = valid or candidates
    if not pool:
        return None
    return max(
        pool,
        key=lambda row: (
            row.get("failure_mode") == "THIN_LIFT_TARGET",
            -row.get("max_pair_count", 10**9),
            min(row.get("pair7_counts", {"B17": -1}).values()) if row.get("pair7_counts") else -1,
            row.get("selected_incidence_count", -1),
        ),
    )


def build_record(thin_candidates: list[dict[str, Any]], source_summary: dict[str, Any]) -> dict[str, Any]:
    source_record = json.loads(SOURCE_DATA.read_text())
    best = best_thin(thin_candidates)
    target_count = sum(1 for row in thin_candidates if row.get("failure_mode") == "THIN_LIFT_TARGET")
    best_hash = None if best is None else best.get("thin_count_hash")
    stored_candidates = []
    for candidate in thin_candidates:
        row = dict(candidate)
        coordinate_classes = row.get("coordinate_classes")
        if coordinate_classes is not None:
            row["coordinate_classes_hash"] = hash_payload(coordinate_classes)
        if row.get("thin_count_hash") != best_hash:
            row.pop("coordinate_classes", None)
            row["coordinate_classes_omitted"] = True
        stored_candidates.append(row)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "source_hypergraph": {
            "supports": source_summary["pre_split"]["support_counts"],
            "max_pair_count": source_summary["pre_split"]["max_pair_count"],
            "pair7_counts": [source_summary["pre_split"]["pair7_counts"][label] for label in PAIR7_LABELS],
            "pair_B_values": source_summary["pre_split"]["pair_B_values"],
            "robustness_score": source_summary["best_robustness_score"],
            "selected_class_size_counts": source_summary["pre_split"]["selected_class_size_counts"],
            "source_selected_count_hash": source_summary["selected_count_hash"],
            "source_proof_status": source_record["proof_status"],
        },
        "thin_hypergraph": {
            "strategies_tested": [row["strategy"] for row in thin_candidates],
            "candidates_constructed": len(thin_candidates),
            "lift_targets": target_count,
            "best_strategy": None if best is None else best.get("strategy"),
            "best_supports": None if best is None else best.get("supports"),
            "best_pair7_counts": None if best is None else best.get("pair7_counts_vector"),
            "best_max_pair_count": None if best is None else best.get("max_pair_count"),
            "best_selected_incidence_count": None if best is None else best.get("selected_incidence_count"),
            "best_selected_class_size_counts": None if best is None else best.get("selected_class_size_counts"),
            "best_thin_count_hash": None if best is None else best.get("thin_count_hash"),
            "best_coordinate_classes": None if best is None else best.get("coordinate_classes"),
            "best_coordinate_classes_hash": None if best is None else hash_payload(best.get("coordinate_classes")),
            "best_failure_mode": None if best is None else best.get("failure_mode"),
            "candidates": stored_candidates,
        },
        "exact_lift": {
            "systems_tested": 0,
            "timeouts": 0,
            "matrix_shape": None,
            "rank": None,
            "nullity": None,
            "exact_vectors_constructed": 0,
            "seven_distinct_vectors": 0,
            "best_agreement_vector": None,
            "best_failure_mode": None,
        },
        "proof_status": "PROOF_RECORD / CANDIDATE / EXACT_EXTRACTION_NO_A327 / PARTIAL",
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
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    source_counts, source_summary = source_selected_counts()
    strategies = THIN_STRATEGIES if args.limit is None else THIN_STRATEGIES[: args.limit]
    thin_candidates = [solve_thin(source_counts, strategy) for strategy in strategies]
    record = build_record(thin_candidates, source_summary)
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
