#!/usr/bin/env python3
"""Degree-1 residual nullspace proxy search for the M1 a=327 target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import scan_m1_a327_coefficient_nullspace_target_search as scalar_search


OUTPUT_DATA = Path("experimental/data/m1_a327_degree1_residual_nullspace_search.json")

N = 512
K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
TOP_LABELS_PER_WITNESS = 2
RETAINED_CANDIDATES = 40

ROOT_TUPLE_LIMIT_BY_FAMILY = {
    "all_pair_boundary_embedding_roots": 8,
    "quotient_fiber_plus_residual": 6,
    "cyclic_interval": 6,
    "seeded_random_255": 8,
}

DROP_MODES = ["first", "middle", "last", "witness_index"]


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


def proxy_subgroup() -> np.ndarray:
    return scalar_search.proxy_subgroup()


def select_root_tuples() -> list[dict[str, Any]]:
    counts: dict[str, int] = {}
    selected = []
    for root_tuple in scalar_search.root_tuples():
        family = root_tuple["family"]
        if counts.get(family, 0) >= ROOT_TUPLE_LIMIT_BY_FAMILY.get(family, 0):
            continue
        selected.append(root_tuple)
        counts[family] = counts.get(family, 0) + 1
    return selected


def drop_root(root_set: list[int], witness_index: int, mode: str) -> tuple[list[int], int]:
    roots = sorted(root_set)
    if len(roots) != 255:
        raise ValueError("expected 255 roots")
    if mode == "first":
        idx = 0
    elif mode == "middle":
        idx = len(roots) // 2
    elif mode == "last":
        idx = len(roots) - 1
    elif mode == "witness_index":
        idx = (37 * witness_index + 19) % len(roots)
    else:
        raise ValueError(f"unknown drop mode: {mode}")
    dropped = roots[idx]
    return roots[:idx] + roots[idx + 1 :], dropped


def root_tuple_254(root_tuple: dict[str, Any], drop_mode: str) -> dict[str, Any]:
    roots_254 = []
    dropped = []
    for witness_index, root_set in enumerate(root_tuple["root_sets"]):
        roots, dropped_position = drop_root(root_set, witness_index, drop_mode)
        roots_254.append(roots)
        dropped.append(dropped_position)
    return {
        "root_tuple_id": f"{root_tuple['root_tuple_id']}_drop_{drop_mode}",
        "source_root_tuple_id": root_tuple["root_tuple_id"],
        "family": root_tuple["family"],
        "drop_mode": drop_mode,
        "roots_254": roots_254,
        "dropped_positions": dropped,
        "root_tuple_hash": hash_payload(roots_254),
    }


def locator_values_modp(H: np.ndarray, roots: list[int]) -> np.ndarray:
    values = np.ones(N, dtype=np.int64)
    for position in roots:
        values = (values * ((H - int(H[position])) % PROXY_PRIME)) % PROXY_PRIME
    values[roots] = 0
    return values


def residual_specs(dropped_positions: list[int]) -> list[dict[str, Any]]:
    specs = [
        {"residual_id": "constant_one", "mode": "constant", "positions": []},
        {"residual_id": "common_x", "mode": "x", "positions": []},
    ]
    for position in [0, 1, 16, 32, 255, 511]:
        specs.append(
            {
                "residual_id": f"common_root_{position:03d}",
                "mode": "common_root",
                "positions": [position] * DIFF_COUNT,
            }
        )
    specs.append(
        {
            "residual_id": "restore_dropped_roots",
            "mode": "witness_roots",
            "positions": dropped_positions,
        }
    )
    for base, step in [(0, 17), (3, 31), (11, 47), (23, 61)]:
        specs.append(
            {
                "residual_id": f"witness_shift_base_{base:03d}_step_{step:02d}",
                "mode": "witness_roots",
                "positions": [(base + (idx + 1) * step) % N for idx in range(DIFF_COUNT)],
            }
        )
    return specs


def residual_values(H: np.ndarray, spec: dict[str, Any]) -> list[np.ndarray]:
    values = []
    for witness in range(DIFF_COUNT):
        if spec["mode"] == "constant":
            values.append(np.ones(N, dtype=np.int64))
        elif spec["mode"] == "x":
            values.append(H.copy())
        elif spec["mode"] in {"common_root", "witness_roots"}:
            root_value = int(H[spec["positions"][witness]])
            values.append((H - root_value) % PROXY_PRIME)
        else:
            raise ValueError(f"unknown residual mode: {spec['mode']}")
    return values


def top_base_constants(base_values: list[np.ndarray], limit: int = TOP_LABELS_PER_WITNESS) -> list[list[int]]:
    constants = []
    base = base_values[0]
    for witness in range(1, DIFF_COUNT):
        labels = Counter()
        other = base_values[witness]
        for pos in range(N):
            if int(base[pos]) == 0 or int(other[pos]) == 0:
                continue
            label = (int(base[pos]) * pow(int(other[pos]), PROXY_PRIME - 2, PROXY_PRIME)) % PROXY_PRIME
            labels[label] += 1
        top = [label for label, _count in labels.most_common(limit)]
        while len(top) < limit:
            top.append(1)
        constants.append(top)
    return constants


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


def exact_assignment_max_min(values: list[list[int]]) -> dict[str, Any]:
    classes_by_pos = []
    for pos in range(N):
        buckets: dict[int, int] = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        classes_by_pos.append(sorted(set(buckets.values())))

    offsets = []
    total_vars = 0
    for classes in classes_by_pos:
        offsets.append(total_vars)
        total_vars += len(classes)

    def feasible(floor: int) -> tuple[bool, list[int] | None]:
        objective = np.zeros(total_vars)
        bounds = Bounds(np.zeros(total_vars), np.ones(total_vars))
        integrality = np.ones(total_vars)
        rows = []
        lower = []
        upper = []
        for pos, classes in enumerate(classes_by_pos):
            row = np.zeros(total_vars)
            row[offsets[pos] : offsets[pos] + len(classes)] = 1
            rows.append(row)
            lower.append(1)
            upper.append(1)
        for witness in range(LIST_SIZE):
            row = np.zeros(total_vars)
            for pos, classes in enumerate(classes_by_pos):
                for idx, mask in enumerate(classes):
                    if mask & (1 << witness):
                        row[offsets[pos] + idx] = 1
            rows.append(row)
            lower.append(floor)
            upper.append(np.inf)
        result = milp(
            objective,
            integrality=integrality,
            bounds=bounds,
            constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
            options={"time_limit": 15},
        )
        if not result.success:
            return False, None
        rounded = np.rint(result.x).astype(int)
        chosen = []
        for pos, classes in enumerate(classes_by_pos):
            start = offsets[pos]
            choice = next((idx for idx, value in enumerate(rounded[start : start + len(classes)]) if value), 0)
            chosen.append(classes[choice])
        return True, chosen

    capacity = value_class_capacity(values)["capacity_upper_bound"]
    lo, hi = 0, max(capacity, TARGET_AGREEMENT)
    best_masks = None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok, masks = feasible(mid)
        if ok:
            lo = mid
            best_masks = masks
        else:
            hi = mid - 1
    agreement = [0] * LIST_SIZE
    if best_masks:
        for mask in best_masks:
            for witness in range(LIST_SIZE):
                if mask & (1 << witness):
                    agreement[witness] += 1
    return {
        "exact_max_min": lo,
        "agreement_vector": agreement,
        "chosen_masks_hash": None if best_masks is None else hash_payload(best_masks),
    }


def evaluate_candidate(root_tuple: dict[str, Any], residual_spec: dict[str, Any], base_values: list[np.ndarray], constants: list[int]) -> dict[str, Any]:
    values = [[0] * N]
    for constant, base in zip(constants, base_values):
        values.append([int((constant * int(base[pos])) % PROXY_PRIME) for pos in range(N)])
    capacity = value_class_capacity(values)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = exact_assignment_max_min(values)
    return {
        "root_tuple_id": root_tuple["root_tuple_id"],
        "source_root_tuple_id": root_tuple["source_root_tuple_id"],
        "family": root_tuple["family"],
        "drop_mode": root_tuple["drop_mode"],
        "root_tuple_hash": root_tuple["root_tuple_hash"],
        "residual_id": residual_spec["residual_id"],
        "residual_mode": residual_spec["mode"],
        "residual_positions_hash": hash_payload(residual_spec["positions"]),
        "constants": constants,
        "constants_hash": hash_payload(constants),
        **capacity,
        "assignment": assignment,
        "status": (
            "PROXY_A327_ASSIGNMENT"
            if assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT
            else "CAPACITY_BELOW_A327"
        ),
    }


def evaluate_root_tuple(root_tuple: dict[str, Any], H: np.ndarray) -> list[dict[str, Any]]:
    locators = [locator_values_modp(H, roots) for roots in root_tuple["roots_254"]]
    results = []
    for residual_spec in residual_specs(root_tuple["dropped_positions"]):
        residuals = residual_values(H, residual_spec)
        base_values = [(locator * residual) % PROXY_PRIME for locator, residual in zip(locators, residuals)]
        constant_options = top_base_constants(base_values)
        candidate_constants = [[1] * DIFF_COUNT]
        for combo in itertools.product(*constant_options):
            candidate_constants.append([1] + list(combo))
        seen = set()
        for constants in candidate_constants:
            digest = hash_payload((residual_spec["residual_id"], constants))
            if digest in seen:
                continue
            seen.add(digest)
            results.append(evaluate_candidate(root_tuple, residual_spec, base_values, constants))
    return results


def build_record() -> dict[str, Any]:
    H = proxy_subgroup()
    base_tuples = select_root_tuples()
    root_254 = [root_tuple_254(root_tuple, drop_mode) for root_tuple in base_tuples for drop_mode in DROP_MODES]
    all_results = []
    for root_tuple in root_254:
        all_results.extend(evaluate_root_tuple(root_tuple, H))
    retained = sorted(
        all_results,
        key=lambda row: (
            row["capacity_upper_bound"],
            row["capacity_total"],
            row["root_tuple_id"],
            row["residual_id"],
        ),
        reverse=True,
    )[:RETAINED_CANDIDATES]
    proxy_candidates = [row for row in all_results if row["status"] == "PROXY_A327_ASSIGNMENT"]
    family_counts: dict[str, int] = {}
    for root_tuple in root_254:
        family_counts[root_tuple["family"]] = family_counts.get(root_tuple["family"], 0) + 1
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "degree1_residual_nullspace_search",
        "model": {
            "anchor": "P_1 = 0",
            "differences": "D_i(X) = c_i L_i(X) R_i(X), deg L_i = 254, deg R_i <= 1",
            "proxy_field": "GF(12289)",
            "top_labels_per_witness": TOP_LABELS_PER_WITNESS,
        },
        "source_root_tuple_count": len(base_tuples),
        "root_tuple_count": len(root_254),
        "root_tuple_family_counts": dict(sorted(family_counts.items())),
        "drop_modes": DROP_MODES,
        "residual_pattern_count_per_root_tuple": len(residual_specs([0] * DIFF_COUNT)),
        "candidate_constant_count": len(all_results),
        "result_hash": hash_payload(all_results),
        "proxy_candidate_count": len(proxy_candidates),
        "best": retained[0],
        "retained_count": len(retained),
        "retained_results": retained,
        "proof_status": "CANDIDATE" if proxy_candidates else "TESTED_DEGREE1_RESIDUALS_NO_PROXY_A327",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list certificate over GF(17^32)",
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
