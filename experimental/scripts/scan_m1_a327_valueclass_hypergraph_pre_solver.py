#!/usr/bin/env python3
"""Discrete value-class hypergraph pre-solver for the M1 a=327 lane.

This deliberately works one abstraction layer above GF(17^32): coordinates are
assigned partitions of the seven witnesses, then Hall guards and split-probe
robustness are checked at the value-class level before any exact lift is tried.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from numbers import Integral
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_a327_valueclass_hypergraph_pre_solver.json")
SOURCE_LEDGER = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json")

N = 512
FIBER_COUNT = 16
FIBER_SIZE = 32
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
PAIR_COINCIDENCE_TARGET = PAIR_TARGET - N
CAPACITY_TOTAL_TARGET = LIST_SIZE * TARGET_AGREEMENT
SOURCE_COMMIT = "56fd7a9"

WITNESS_MASKS = [1 << idx for idx in range(LIST_SIZE)]
FRAGILE_1457 = (1 << 0) | (1 << 3) | (1 << 4) | (1 << 6)
SIX_CLASS_BASIN = (1 << 0) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5) | (1 << 6)
PAIR_INDICES = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6)]
PAIR_LABELS = ["B17", "B27", "B37", "B47", "B57"]

SPLIT_PROBES = {
    "split_4_from_157": [(1 << 3), (1 << 0) | (1 << 4) | (1 << 6)],
    "split_14_vs_57": [(1 << 0) | (1 << 3), (1 << 4) | (1 << 6)],
    "split_1_from_457": [(1 << 0), (1 << 3) | (1 << 4) | (1 << 6)],
    "split_15_vs_47": [(1 << 0) | (1 << 4), (1 << 3) | (1 << 6)],
    "split_17_vs_45": [(1 << 0) | (1 << 6), (1 << 3) | (1 << 4)],
}

PROFILE_SPECS = [
    {
        "profile_id": "user_low_collapse_patterns",
        "description": "Only 2+2+1+1+1, 3+2+1+1, 3+3+1, and 4+1+1+1 patterns.",
        "allowed_signatures": [(2, 2, 1, 1, 1), (3, 2, 1, 1), (3, 3, 1), (4, 1, 1, 1)],
        "max_block_size": 4,
        "fragile_1457_cap": 0,
    },
    {
        "profile_id": "no_fragile_max5",
        "description": "All partitions with max block <=5 and no block containing {1,4,5,7}.",
        "max_block_size": 5,
        "fragile_1457_cap": 0,
    },
    {
        "profile_id": "fragile_cap_16_max5",
        "description": "All max-5 partitions with at most 16 fragile {1,4,5,7} coordinates.",
        "max_block_size": 5,
        "fragile_1457_cap": 16,
    },
    {
        "profile_id": "fragile_cap_32_max5",
        "description": "All max-5 partitions with at most 32 fragile {1,4,5,7} coordinates.",
        "max_block_size": 5,
        "fragile_1457_cap": 32,
    },
    {
        "profile_id": "fragile_cap_64_max5",
        "description": "All max-5 partitions with at most 64 fragile {1,4,5,7} coordinates.",
        "max_block_size": 5,
        "fragile_1457_cap": 64,
    },
    {
        "profile_id": "all_max5_no_six",
        "description": "All partitions with max block <=5 and no explicit fragile cap.",
        "max_block_size": 5,
        "fragile_1457_cap": None,
    },
    {
        "profile_id": "size5_plus_balanced_splits",
        "description": "Max-5 partitions excluding block size signatures below 3+2+1+1.",
        "allowed_signatures": [(5, 1, 1), (4, 2, 1), (4, 1, 1, 1), (3, 3, 1), (3, 2, 2), (3, 2, 1, 1)],
        "max_block_size": 5,
        "fragile_1457_cap": 32,
    },
    {
        "profile_id": "pairblock_split_resilience",
        "description": "Emphasize 2+2 and 3+2 residual block signatures plus size-5 capacity buffers.",
        "allowed_signatures": [(5, 1, 1), (4, 2, 1), (3, 2, 2), (3, 2, 1, 1), (2, 2, 1, 1, 1)],
        "max_block_size": 5,
        "fragile_1457_cap": 32,
    },
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


def mask_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(LIST_SIZE) if mask & (1 << idx)]


def canonical(blocks: list[int]) -> tuple[int, ...]:
    return tuple(sorted((int(block) for block in blocks if block), key=lambda block: (-block.bit_count(), block)))


def set_partitions(n: int = LIST_SIZE) -> list[tuple[int, ...]]:
    parts: list[list[int]] = []

    def rec(item: int, blocks: list[int]) -> None:
        if item == n:
            parts.append(list(blocks))
            return
        bit = 1 << item
        for idx in range(len(blocks)):
            blocks[idx] |= bit
            rec(item + 1, blocks)
            blocks[idx] ^= bit
        blocks.append(bit)
        rec(item + 1, blocks)
        blocks.pop()

    rec(0, [])
    return sorted({canonical(blocks) for blocks in parts})


ALL_PARTITIONS = set_partitions()


def signature(partition: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted((block.bit_count() for block in partition), reverse=True))


def has_fragile_1457(partition: tuple[int, ...]) -> bool:
    return any((block & FRAGILE_1457) == FRAGILE_1457 for block in partition)


def has_six_class_basin(partition: tuple[int, ...]) -> bool:
    return any((block & SIX_CLASS_BASIN) == SIX_CLASS_BASIN for block in partition)


def max_block_size(partition: tuple[int, ...]) -> int:
    return max(block.bit_count() for block in partition)


def pair_same(partition: tuple[int, ...], pair: tuple[int, int]) -> int:
    left, right = pair
    pair_mask = (1 << left) | (1 << right)
    return int(any((block & pair_mask) == pair_mask for block in partition))


def refine_for_probe(partition: tuple[int, ...], groups: list[int]) -> tuple[int, ...]:
    # A split probe models splitting the residual [1,4,5,7] block. It should not
    # globally separate witness 7 from unrelated pair-support blocks like {2,7}.
    # Therefore it refines only blocks that actually contain the fragile class.
    refined: list[int] = []
    for block in partition:
        if (block & FRAGILE_1457) != FRAGILE_1457:
            refined.append(block)
            continue
        used = 0
        for group in groups:
            piece = block & group
            used |= piece
            if piece:
                refined.append(piece)
        outside = block & ~used
        if outside:
            refined.append(outside)
    return canonical(refined)


def partition_row(partition: tuple[int, ...]) -> dict[str, Any]:
    return {
        "blocks": [mask_members(block) for block in partition],
        "signature": list(signature(partition)),
        "max_block_size": max_block_size(partition),
        "pair_same": {
            label: pair_same(partition, pair)
            for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True)
        },
        "fragile_1457": has_fragile_1457(partition),
        "six_class_basin": has_six_class_basin(partition),
    }


def allowed_partitions(spec: dict[str, Any]) -> list[tuple[int, ...]]:
    allowed_signatures = None
    if "allowed_signatures" in spec:
        allowed_signatures = {tuple(sig) for sig in spec["allowed_signatures"]}
    out = []
    for partition in ALL_PARTITIONS:
        if max_block_size(partition) > spec.get("max_block_size", LIST_SIZE):
            continue
        if has_six_class_basin(partition):
            continue
        if allowed_signatures is not None and signature(partition) not in allowed_signatures:
            continue
        if spec.get("fragile_1457_cap") == 0 and has_fragile_1457(partition):
            continue
        out.append(partition)
    return out


def coefficient_rows(partitions: list[tuple[int, ...]]) -> dict[str, list[float]]:
    rows: dict[str, list[float]] = {
        "capacity": [max_block_size(partition) / LIST_SIZE for partition in partitions],
    }
    for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
        rows[label] = [float(pair_same(partition, pair)) for partition in partitions]
    for probe_name, groups in SPLIT_PROBES.items():
        probed = [refine_for_probe(partition, groups) for partition in partitions]
        rows[f"{probe_name}:capacity"] = [max_block_size(partition) / LIST_SIZE for partition in probed]
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            rows[f"{probe_name}:{label}"] = [float(pair_same(partition, pair)) for partition in probed]
    return rows


def solve_profile(spec: dict[str, Any]) -> dict[str, Any]:
    partitions = allowed_partitions(spec)
    if not partitions:
        return {
            "profile_id": spec["profile_id"],
            "description": spec["description"],
            "solver_status": "NO_ALLOWED_PARTITIONS",
            "allowed_partition_count": 0,
            "split_resilient": False,
            "failure_mode": "HYPERGRAPH_INFEASIBLE",
        }

    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover - environment fallback.
        return {
            "profile_id": spec["profile_id"],
            "description": spec["description"],
            "solver_status": "SCIPY_UNAVAILABLE",
            "solver_error": str(exc),
            "allowed_partition_count": len(partitions),
            "split_resilient": False,
            "failure_mode": "HYPERGRAPH_SOLVER_UNAVAILABLE",
        }

    rows = coefficient_rows(partitions)
    var_count = len(partitions) + 1
    t_idx = len(partitions)

    objective = np.zeros(var_count)
    objective[t_idx] = -1000.0
    for idx, partition in enumerate(partitions):
        objective[idx] += 0.01 * int(has_fragile_1457(partition))
        objective[idx] += 0.001 * max_block_size(partition)

    constraints = []
    lower = []
    upper = []

    row = np.zeros(var_count)
    row[: len(partitions)] = 1
    constraints.append(row)
    lower.append(N)
    upper.append(N)

    fragile_cap = spec.get("fragile_1457_cap")
    if fragile_cap is not None and fragile_cap > 0:
        row = np.zeros(var_count)
        row[: len(partitions)] = [1 if has_fragile_1457(partition) else 0 for partition in partitions]
        constraints.append(row)
        lower.append(0)
        upper.append(int(fragile_cap))

    guard_targets = {"capacity": TARGET_AGREEMENT}
    guard_targets.update({label: PAIR_COINCIDENCE_TARGET for label in PAIR_LABELS})
    for key, target in guard_targets.items():
        row = np.zeros(var_count)
        row[: len(partitions)] = rows[key]
        row[t_idx] = -1
        constraints.append(row)
        lower.append(float(target))
        upper.append(float("inf"))

    for probe_name in SPLIT_PROBES:
        for label, target in guard_targets.items():
            key = f"{probe_name}:{label}"
            row = np.zeros(var_count)
            row[: len(partitions)] = rows[key]
            row[t_idx] = -1
            constraints.append(row)
            lower.append(float(target))
            upper.append(float("inf"))

    bounds = Bounds(
        np.r_[np.zeros(len(partitions)), -N * np.ones(1)],
        np.r_[N * np.ones(len(partitions)), N * np.ones(1)],
    )
    integrality = np.r_[np.ones(len(partitions)), np.zeros(1)]
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=LinearConstraint(np.vstack(constraints), np.array(lower), np.array(upper)),
        options={"time_limit": 30},
    )

    if not result.success:
        return {
            "profile_id": spec["profile_id"],
            "description": spec["description"],
            "solver_status": "INFEASIBLE_OR_LIMIT",
            "solver_message": str(result.message),
            "allowed_partition_count": len(partitions),
            "split_resilient": False,
            "failure_mode": "HYPERGRAPH_INFEASIBLE",
        }

    counts = [int(round(value)) for value in result.x[: len(partitions)]]
    t_value = float(result.x[t_idx])
    used = [(partition, count) for partition, count in zip(partitions, counts, strict=True) if count]
    summary = evaluate_counts(used)
    summary["profile_id"] = spec["profile_id"]
    summary["description"] = spec["description"]
    summary["solver_status"] = "OPTIMAL_OR_FEASIBLE"
    summary["solver_message"] = str(result.message)
    summary["objective_value"] = float(result.fun)
    summary["max_min_margin"] = t_value
    summary["allowed_partition_count"] = len(partitions)
    summary["partition_count_hash"] = hash_payload([
        {"partition": [mask_members(block) for block in partition], "count": count}
        for partition, count in used
    ])
    summary["top_partition_counts"] = [
        {
            **partition_row(partition),
            "count": count,
        }
        for partition, count in sorted(used, key=lambda item: (-item[1], partition_row(item[0])["signature"]))[:12]
    ]
    summary["split_resilient"] = summary["best_robustness_score"] >= 0
    summary["failure_mode"] = classify_summary(summary)
    return summary


def evaluate_one(partitions: list[tuple[int, int]]) -> dict[str, Any]:
    capacity_total = sum(count * max_block_size(partition) for partition, count in partitions)
    pair_same_counts = [
        sum(count * pair_same(partition, pair) for partition, count in partitions)
        for pair in PAIR_INDICES
    ]
    pair_B_values = [N + count for count in pair_same_counts]
    fragile_count = sum(count for partition, count in partitions if has_fragile_1457(partition))
    six_class_count = sum(count for partition, count in partitions if has_six_class_basin(partition))
    return {
        "capacity_total": capacity_total,
        "capacity_upper_bound": capacity_total // LIST_SIZE,
        "pair_same_counts": pair_same_counts,
        "pair_B_values": pair_B_values,
        "guard_vector": {
            "capacity": capacity_total // LIST_SIZE,
            **{label: value for label, value in zip(PAIR_LABELS, pair_B_values, strict=True)},
        },
        "guard_margins": {
            "capacity": capacity_total // LIST_SIZE - TARGET_AGREEMENT,
            **{label: value - PAIR_TARGET for label, value in zip(PAIR_LABELS, pair_B_values, strict=True)},
        },
        "robustness_score": min(
            [capacity_total // LIST_SIZE - TARGET_AGREEMENT]
            + [value - PAIR_TARGET for value in pair_B_values]
        ),
        "fragile_1457_count": fragile_count,
        "six_class_basin_count": six_class_count,
    }


def evaluate_counts(used: list[tuple[tuple[int, ...], int]]) -> dict[str, Any]:
    pre = evaluate_one(used)
    probes = {}
    for name, groups in SPLIT_PROBES.items():
        refined = [(refine_for_probe(partition, groups), count) for partition, count in used]
        probes[name] = evaluate_one(refined)
    best_probe_name, best_probe = max(
        probes.items(),
        key=lambda item: (item[1]["robustness_score"], item[1]["capacity_upper_bound"]),
    )
    all_scores = [pre["robustness_score"]] + [row["robustness_score"] for row in probes.values()]
    return {
        "coordinate_count": N,
        "fiber_count": FIBER_COUNT,
        "fiber_size": FIBER_SIZE,
        "pre_split": pre,
        "split_probes": probes,
        "best_probe": {"split_family": best_probe_name, **best_probe},
        "best_robustness_score": min(all_scores),
    }


def classify_summary(summary: dict[str, Any]) -> str:
    if summary["best_robustness_score"] >= 0:
        return "HYPERGRAPH_SPLIT_RESILIENT"
    pre = summary["pre_split"]
    if pre["capacity_upper_bound"] < TARGET_AGREEMENT:
        return "HYPERGRAPH_CAPACITY_NOT_ROBUST"
    if pre["pair_B_values"][1] < PAIR_TARGET or pre["pair_B_values"][2] < PAIR_TARGET:
        return "HYPERGRAPH_GUARDS_FAIL"
    if pre["pair_B_values"][3] < PAIR_TARGET:
        return "HYPERGRAPH_B47_NOT_ROBUST"
    for probe in summary["split_probes"].values():
        if probe["capacity_upper_bound"] < TARGET_AGREEMENT:
            return "HYPERGRAPH_CAPACITY_NOT_ROBUST"
        if probe["pair_B_values"][3] < PAIR_TARGET:
            return "HYPERGRAPH_B47_NOT_ROBUST"
    return "HYPERGRAPH_GUARDS_FAIL"


def build_record(results: list[dict[str, Any]]) -> dict[str, Any]:
    source = json.loads(SOURCE_LEDGER.read_text())
    tested = len(results)
    best = max(
        results,
        key=lambda row: (
            row.get("best_robustness_score", -10**9),
            (row.get("pre_split") or {}).get("capacity_upper_bound", -1),
        ),
    ) if results else None
    split_resilient = [row for row in results if row.get("split_resilient")]
    feasible = [row for row in results if row.get("solver_status") == "OPTIMAL_OR_FEASIBLE"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "upstream_exact_scanner": {
            "systems_tested": source["exact_scanner"]["systems_tested"],
            "exact_vectors_constructed": source["exact_scanner"]["exact_vectors_constructed"],
            "split_resilient_skeletons": source["exact_scanner"]["split_resilient_skeletons"],
            "best_failure_mode": source["exact_scanner"]["best_failure_mode"],
            "best_robustness_score": source["exact_scanner"]["best_robustness_score"],
        },
        "hypergraph_search": {
            "coordinate_count": N,
            "fiber_count": FIBER_COUNT,
            "systems_tested": tested,
            "feasible_hypergraphs": len(feasible),
            "split_resilient_hypergraphs": len(split_resilient),
            "profile_count": len(PROFILE_SPECS),
            "best_guard_vector": None if best is None or "pre_split" not in best else best["pre_split"]["guard_vector"],
            "best_probe_guard_vector": None if best is None or "best_probe" not in best else best["best_probe"]["guard_vector"],
            "best_robustness_score": None if best is None else best.get("best_robustness_score"),
            "best_collapse_proxy": None if best is None or "pre_split" not in best else {
                "fragile_1457_count": best["pre_split"]["fragile_1457_count"],
                "six_class_basin_count": best["pre_split"]["six_class_basin_count"],
            },
            "best_failure_mode": None if best is None else best.get("failure_mode"),
            "failure_mode_counts": failure_counts(results),
            "profiles": results,
        },
        "proof_status": proof_status(split_resilient, tested),
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "exact GF(17^32) lift",
        ],
    }


def failure_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in rows:
        failure = row.get("failure_mode", "UNKNOWN")
        out[failure] = out.get(failure, 0) + 1
    return dict(sorted(out.items()))


def proof_status(split_resilient: list[dict[str, Any]], tested: int) -> str:
    if split_resilient:
        return "HYPERGRAPH_SEARCH / CANDIDATE / EXPERIMENTAL"
    if tested == len(PROFILE_SPECS):
        return "HYPERGRAPH_SEARCH / TESTED_NO_SPLIT_RESILIENT / EXPERIMENTAL"
    return "HYPERGRAPH_SEARCH / PARTIAL / EXPERIMENTAL"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    specs = PROFILE_SPECS if args.limit is None else PROFILE_SPECS[: args.limit]
    results = [solve_profile(spec) for spec in specs]
    record = build_record(results)
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
