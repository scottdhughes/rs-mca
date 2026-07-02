#!/usr/bin/env python3
"""RS-feasible selected-class hypergraph pre-solver for M1 a=327.

This is a discrete pre-lift model. A coordinate chooses only the received-word
class C_h, not a full value-class partition. The model enforces the Reed-Solomon
pairwise co-occurrence cap needed for seven distinct degree-<256 codewords.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from numbers import Integral
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_a327_rs_feasible_valueclass_hypergraph_pre_solver.json")
SOURCE_LEDGER = Path("experimental/data/m1_a327_valueclass_hypergraph_pre_solver.json")

SOURCE_COMMIT = "e4e966a"
N = 512
FIBER_COUNT = 16
FIBER_SIZE = 32
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
PAIR7_LOWER = PAIR_TARGET - N
PAIR_CAP = 255
PREFERRED_PAIR_CAP = 220

WITNESS_MASKS = [1 << idx for idx in range(LIST_SIZE)]
FRAGILE_1457 = (1 << 0) | (1 << 3) | (1 << 4) | (1 << 6)
SEVEN_BIT = 1 << 6
PAIR_INDICES = list(itertools.combinations(range(LIST_SIZE), 2))
PAIR_LABELS = [f"P{left + 1}{right + 1}" for left, right in PAIR_INDICES]
PAIR7_INDICES = [(idx, 6) for idx in range(5)]
PAIR7_LABELS = ["B17", "B27", "B37", "B47", "B57"]

SPLIT_PROBES = {
    "split_4_from_157": [(1 << 3), (1 << 0) | (1 << 4) | (1 << 6)],
    "split_14_vs_57": [(1 << 0) | (1 << 3), (1 << 4) | (1 << 6)],
    "split_1_from_457": [(1 << 0), (1 << 3) | (1 << 4) | (1 << 6)],
    "split_15_vs_47": [(1 << 0) | (1 << 4), (1 << 3) | (1 << 6)],
    "split_17_vs_45": [(1 << 0) | (1 << 6), (1 << 3) | (1 << 4)],
}

PROFILE_SPECS = [
    {
        "profile_id": "selected_4_5_paircap255",
        "description": "Selected classes of size 4 or 5, hard RS pair cap 255.",
        "selected_class_sizes": [4, 5],
        "pair_cap": 255,
    },
    {
        "profile_id": "selected_4_5_paircap220",
        "description": "Selected classes of size 4 or 5, preferred pair cap 220 made hard.",
        "selected_class_sizes": [4, 5],
        "pair_cap": 220,
    },
    {
        "profile_id": "selected_4_5_paircap200",
        "description": "Selected classes of size 4 or 5, tighter pair cap 200.",
        "selected_class_sizes": [4, 5],
        "pair_cap": 200,
    },
    {
        "profile_id": "selected_3_4_5_paircap220",
        "description": "Selected classes of size 3, 4, or 5, preferred pair cap 220.",
        "selected_class_sizes": [3, 4, 5],
        "pair_cap": 220,
    },
    {
        "profile_id": "selected_3_4_5_paircap200",
        "description": "Selected classes of size 3, 4, or 5, tighter pair cap 200.",
        "selected_class_sizes": [3, 4, 5],
        "pair_cap": 200,
    },
]

LEGACY_E4E966A_BEST = [
    (331, ((1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 6), (1 << 4) | (1 << 5))),
    (181, ((1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 6), (1 << 0) | (1 << 5))),
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


def subset_masks(sizes: list[int]) -> list[int]:
    masks: list[int] = []
    for size in sizes:
        for combo in itertools.combinations(range(LIST_SIZE), size):
            mask = 0
            for idx in combo:
                mask |= 1 << idx
            masks.append(mask)
    return sorted(set(masks), key=lambda value: (value.bit_count(), value))


def contains(mask: int, idx: int) -> int:
    return int(bool(mask & (1 << idx)))


def pair_same(mask: int, pair: tuple[int, int]) -> int:
    left, right = pair
    return int(bool(mask & (1 << left)) and bool(mask & (1 << right)))


def probe_selected_class(mask: int, groups: list[int]) -> int:
    if (mask & FRAGILE_1457) != FRAGILE_1457:
        return mask
    outside = mask & ~FRAGILE_1457
    for group in groups:
        if group & SEVEN_BIT:
            return outside | (mask & group)
    best_piece = max((mask & group for group in groups), key=lambda piece: (piece.bit_count(), piece))
    return outside | best_piece


def selected_class_row(mask: int) -> dict[str, Any]:
    return {
        "members": mask_members(mask),
        "size": mask.bit_count(),
        "contains_fragile_1457": (mask & FRAGILE_1457) == FRAGILE_1457,
        "contains_7": bool(mask & SEVEN_BIT),
    }


def coefficient_rows(classes: list[int]) -> dict[str, list[int]]:
    rows: dict[str, list[int]] = {}
    for idx in range(LIST_SIZE):
        rows[f"support_{idx + 1}"] = [contains(mask, idx) for mask in classes]
    for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
        rows[f"pair_{label}"] = [pair_same(mask, pair) for mask in classes]
    for probe_name, groups in SPLIT_PROBES.items():
        probed = [probe_selected_class(mask, groups) for mask in classes]
        for idx in range(LIST_SIZE):
            rows[f"{probe_name}:support_{idx + 1}"] = [contains(mask, idx) for mask in probed]
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            rows[f"{probe_name}:pair_{label}"] = [pair_same(mask, pair) for mask in probed]
    return rows


def solve_profile(spec: dict[str, Any]) -> dict[str, Any]:
    classes = subset_masks(spec["selected_class_sizes"])
    try:
        import numpy as np
        from scipy.optimize import Bounds, LinearConstraint, milp
    except Exception as exc:  # pragma: no cover - environment fallback.
        return {
            "profile_id": spec["profile_id"],
            "description": spec["description"],
            "solver_status": "SCIPY_UNAVAILABLE",
            "solver_error": str(exc),
            "allowed_selected_class_count": len(classes),
            "rs_feasible": False,
            "split_resilient": False,
            "failure_mode": "RS_HYPERGRAPH_SOLVER_UNAVAILABLE",
        }

    rows = coefficient_rows(classes)
    var_count = len(classes) + 1
    t_idx = len(classes)
    pair_cap = int(spec["pair_cap"])

    objective = np.zeros(var_count)
    objective[t_idx] = -1000.0
    for idx, mask in enumerate(classes):
        objective[idx] += 0.01 * int((mask & FRAGILE_1457) == FRAGILE_1457)
        objective[idx] += 0.001 * mask.bit_count()

    constraints = []
    lower = []
    upper = []

    row = np.zeros(var_count)
    row[: len(classes)] = 1
    constraints.append(row)
    lower.append(N)
    upper.append(N)

    states = ["pre_split", *SPLIT_PROBES.keys()]
    for state in states:
        prefix = "" if state == "pre_split" else f"{state}:"
        for idx in range(LIST_SIZE):
            row = np.zeros(var_count)
            row[: len(classes)] = rows[f"{prefix}support_{idx + 1}"]
            row[t_idx] = -1
            constraints.append(row)
            lower.append(TARGET_AGREEMENT)
            upper.append(float("inf"))
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            row = np.zeros(var_count)
            row[: len(classes)] = rows[f"{prefix}pair_{label}"]
            row[t_idx] = 1
            constraints.append(row)
            lower.append(float("-inf"))
            upper.append(pair_cap)
        for pair, label in zip(PAIR7_INDICES, PAIR7_LABELS, strict=True):
            pair_label = f"P{pair[0] + 1}{pair[1] + 1}"
            row = np.zeros(var_count)
            row[: len(classes)] = rows[f"{prefix}pair_{pair_label}"]
            row[t_idx] = -1
            constraints.append(row)
            lower.append(PAIR7_LOWER)
            upper.append(float("inf"))

    bounds = Bounds(
        np.r_[np.zeros(len(classes)), -N * np.ones(1)],
        np.r_[N * np.ones(len(classes)), N * np.ones(1)],
    )
    integrality = np.r_[np.ones(len(classes)), np.zeros(1)]
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
            "selected_class_sizes": spec["selected_class_sizes"],
            "pair_cap": pair_cap,
            "solver_status": "INFEASIBLE_OR_LIMIT",
            "solver_message": str(result.message),
            "allowed_selected_class_count": len(classes),
            "rs_feasible": False,
            "split_resilient": False,
            "failure_mode": "RS_HYPERGRAPH_SUPPORT_FAIL",
        }

    counts = [int(round(value)) for value in result.x[: len(classes)]]
    used = [(mask, count) for mask, count in zip(classes, counts, strict=True) if count]
    summary = evaluate_counts(used, pair_cap)
    summary.update(
        {
            "profile_id": spec["profile_id"],
            "description": spec["description"],
            "selected_class_sizes": spec["selected_class_sizes"],
            "pair_cap": pair_cap,
            "solver_status": "OPTIMAL_OR_FEASIBLE",
            "solver_message": str(result.message),
            "objective_value": float(result.fun),
            "max_min_margin": float(result.x[t_idx]),
            "allowed_selected_class_count": len(classes),
            "selected_count_hash": hash_payload([
                {"selected_class": mask_members(mask), "count": count}
                for mask, count in used
            ]),
            "top_selected_class_counts": [
                {**selected_class_row(mask), "count": count}
                for mask, count in sorted(used, key=lambda item: (-item[1], item[0]))[:12]
            ],
        }
    )
    summary["rs_feasible"] = summary["pre_split"]["rs_pair_cap_pass"]
    summary["split_resilient"] = summary["best_robustness_score"] >= 0
    summary["failure_mode"] = classify_summary(summary)
    return summary


def evaluate_state(used: list[tuple[int, int]], pair_cap: int) -> dict[str, Any]:
    support_counts = [sum(count * contains(mask, idx) for mask, count in used) for idx in range(LIST_SIZE)]
    pair_counts = {
        label: sum(count * pair_same(mask, pair) for mask, count in used)
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True)
    }
    pair7_counts = {
        label: pair_counts[f"P{pair[0] + 1}{pair[1] + 1}"]
        for pair, label in zip(PAIR7_INDICES, PAIR7_LABELS, strict=True)
    }
    pair_B_values = [N + pair7_counts[label] for label in PAIR7_LABELS]
    max_pair_label, max_pair_count = max(pair_counts.items(), key=lambda item: item[1])
    support_margins = [value - TARGET_AGREEMENT for value in support_counts]
    pair_cap_margins = {label: pair_cap - value for label, value in pair_counts.items()}
    pair7_margins = {label: value - PAIR7_LOWER for label, value in pair7_counts.items()}
    robustness_score = min(
        support_margins
        + list(pair_cap_margins.values())
        + list(pair7_margins.values())
    )
    selected_class_size_counts: dict[str, int] = {}
    fragile_count = 0
    for mask, count in used:
        selected_class_size_counts[str(mask.bit_count())] = selected_class_size_counts.get(str(mask.bit_count()), 0) + count
        if (mask & FRAGILE_1457) == FRAGILE_1457:
            fragile_count += count
    return {
        "support_counts": support_counts,
        "support_margins": support_margins,
        "pair_counts": pair_counts,
        "pair_cap": pair_cap,
        "pair_cap_margins": pair_cap_margins,
        "pair7_counts": pair7_counts,
        "pair7_margins": pair7_margins,
        "pair_B_values": pair_B_values,
        "max_pair_count": max_pair_count,
        "max_pair_label": max_pair_label,
        "rs_pair_cap_pass": max_pair_count <= pair_cap,
        "selected_class_size_counts": dict(sorted(selected_class_size_counts.items())),
        "fragile_1457_selected_count": fragile_count,
        "robustness_score": robustness_score,
    }


def evaluate_counts(used: list[tuple[int, int]], pair_cap: int) -> dict[str, Any]:
    pre = evaluate_state(used, pair_cap)
    probes = {}
    for name, groups in SPLIT_PROBES.items():
        probed = [(probe_selected_class(mask, groups), count) for mask, count in used]
        probes[name] = evaluate_state(probed, pair_cap)
    all_scores = [pre["robustness_score"]] + [row["robustness_score"] for row in probes.values()]
    return {
        "coordinate_count": N,
        "fiber_count": FIBER_COUNT,
        "fiber_size": FIBER_SIZE,
        "pre_split": pre,
        "split_probes": probes,
        "best_robustness_score": min(all_scores),
    }


def classify_summary(summary: dict[str, Any]) -> str:
    states = [summary["pre_split"], *summary["split_probes"].values()]
    if summary["best_robustness_score"] >= 0:
        return "RS_HYPERGRAPH_FEASIBLE"
    for state in states:
        if min(state["support_margins"]) < 0:
            return "RS_HYPERGRAPH_SUPPORT_FAIL"
        if min(state["pair_cap_margins"].values()) < 0:
            return "RS_HYPERGRAPH_PAIR_CAP_FAIL"
        if min(state["pair7_margins"].values()) < 0:
            return "RS_HYPERGRAPH_PAIR7_GUARD_FAIL"
    return "RS_HYPERGRAPH_SPLIT_NOT_ROBUST"


def legacy_pair_cap_audit() -> dict[str, Any]:
    pair_counts = {label: 0 for label in PAIR_LABELS}
    for count, partition in LEGACY_E4E966A_BEST:
        for block in partition:
            for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
                pair_counts[label] += count * pair_same(block, pair)
    max_label, max_count = max(pair_counts.items(), key=lambda item: item[1])
    violations = {label: value for label, value in pair_counts.items() if value > PAIR_CAP}
    return {
        "source_commit": "e4e966a",
        "candidate_profile_id": "no_fragile_max5",
        "partition_count_hash": "63dde975f2148cbc507780378f927211e84fcdc7f944eeabcebc16610a3c97bc",
        "pair_cap": PAIR_CAP,
        "pair_counts": pair_counts,
        "max_pair_label": max_label,
        "max_pair_count": max_count,
        "violating_pairs": violations,
        "rs_pair_cap_pass": False,
        "failure_mode": "RS_HYPERGRAPH_PAIR_CAP_FAIL",
    }


def build_record(results: list[dict[str, Any]]) -> dict[str, Any]:
    source = json.loads(SOURCE_LEDGER.read_text())
    candidate = source["hypergraph_search"]
    feasible = [row for row in results if row.get("failure_mode") == "RS_HYPERGRAPH_FEASIBLE"]
    best = max(
        results,
        key=lambda row: (
            row.get("best_robustness_score", -10**9),
            -((row.get("pre_split") or {}).get("max_pair_count", 10**9)),
        ),
    ) if results else None
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "legacy_e4e966a_pair_cap_audit": legacy_pair_cap_audit(),
        "source_hypergraph_candidate": {
            "systems_tested": candidate["systems_tested"],
            "split_resilient_hypergraphs": candidate["split_resilient_hypergraphs"],
            "best_robustness_score": candidate["best_robustness_score"],
            "best_guard_vector": candidate["best_guard_vector"],
            "best_failure_mode": candidate["best_failure_mode"],
        },
        "rs_feasibility": {
            "coordinate_count": N,
            "fiber_count": FIBER_COUNT,
            "selected_class_sizes_tested": sorted({size for spec in PROFILE_SPECS for size in spec["selected_class_sizes"]}),
            "support_target": TARGET_AGREEMENT,
            "pair_cap": PAIR_CAP,
            "preferred_pair_cap": PREFERRED_PAIR_CAP,
            "pair7_lower": PAIR7_LOWER,
        },
        "search_result": {
            "systems_tested": len(results),
            "rs_feasible_hypergraphs": len(feasible),
            "split_resilient_hypergraphs": len(feasible),
            "best_supports": None if best is None or "pre_split" not in best else best["pre_split"]["support_counts"],
            "best_pair_counts": None if best is None or "pre_split" not in best else best["pre_split"]["pair_counts"],
            "best_max_pair_count": None if best is None or "pre_split" not in best else best["pre_split"]["max_pair_count"],
            "best_pair7_counts": None if best is None or "pre_split" not in best else best["pre_split"]["pair7_counts"],
            "best_pair_B_values": None if best is None or "pre_split" not in best else best["pre_split"]["pair_B_values"],
            "best_robustness_score": None if best is None else best.get("best_robustness_score"),
            "best_failure_mode": None if best is None else best.get("failure_mode"),
            "failure_mode_counts": failure_counts(results),
            "profiles": results,
        },
        "proof_status": proof_status(feasible, len(results)),
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


def proof_status(feasible: list[dict[str, Any]], tested: int) -> str:
    if feasible:
        return "RS_HYPERGRAPH_SEARCH / CANDIDATE / EXPERIMENTAL"
    if tested == len(PROFILE_SPECS):
        return "RS_HYPERGRAPH_SEARCH / TESTED_NO_RS_FEASIBLE / EXPERIMENTAL"
    return "RS_HYPERGRAPH_SEARCH / PARTIAL / EXPERIMENTAL"


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
