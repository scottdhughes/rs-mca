#!/usr/bin/env python3
"""Rank-aware v2 CP-SAT screen targeting structural defect for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "e472d07"
INPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_structural_rank_features.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_rankaware_v2_structural_defect.json")
LONG_REALIZATION_SCAN = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_long_front_realization.py")

TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
WITNESSES = tuple(range(1, 8))
PAIR_CAP = 255
PAIR7_LOWER = 142
S_VALUES = [8, 16, 32]
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the bounded rank-aware v2 structural-defect screen",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def load_long_realization() -> Any:
    spec = importlib.util.spec_from_file_location("long_realization_scan", LONG_REALIZATION_SCAN)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {LONG_REALIZATION_SCAN}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_ortools() -> tuple[Any, str]:
    try:
        from ortools.sat.python import cp_model  # type: ignore
        import ortools  # type: ignore

        return cp_model, str(ortools.__version__)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "OR-Tools is required. Run with "
            "/Users/scott/.venvs/rs-mca-ortools/bin/python "
            "experimental/scripts/scan_m1_a327_quotient_subgroup_rankaware_v2_structural_defect.py"
        ) from exc


def canonical_partition(blocks: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((tuple(sorted(block)) for block in blocks), key=lambda block: (block[0], len(block), block)))


def set_partitions(items: tuple[int, ...]) -> list[tuple[tuple[int, ...], ...]]:
    if not items:
        return [tuple()]
    first, rest = items[0], items[1:]
    out: set[tuple[tuple[int, ...], ...]] = set()
    for partition in set_partitions(rest):
        out.add(canonical_partition([(first,), *partition]))
        for idx, block in enumerate(partition):
            new_blocks = list(partition)
            new_blocks[idx] = tuple(sorted((first, *block)))
            out.add(canonical_partition(new_blocks))
    return sorted(out, key=lambda part: (len(part), [len(block) for block in part], part))


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def partition_pair_same(partition: tuple[tuple[int, ...], ...], pair: tuple[int, int]) -> bool:
    return any(pair[0] in block and pair[1] in block for block in partition)


def equation_cost(partition: tuple[tuple[int, ...], ...]) -> int:
    return sum(len(block) - 1 for block in partition)


def solve_model(s: int, time_limit: float, max_active_partitions: int, force_structural_defect: bool) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    quotient_length = DOMAIN_SIZE // s
    quotient_degree_bound = PAIR_CAP // s
    variable_count = 6 * (quotient_degree_bound + 1)
    partitions = set_partitions(WITNESSES)
    model = cp_model.CpModel()
    n_vars = []
    z_vars: list[list[Any]] = []
    active_vars = []
    for pidx, partition in enumerate(partitions):
        active = model.NewBoolVar(f"active_{pidx}")
        n = model.NewIntVar(0, quotient_length, f"n_{pidx}")
        model.Add(n > 0).OnlyEnforceIf(active)
        model.Add(n == 0).OnlyEnforceIf(active.Not())
        z_for_partition = []
        for bidx, _block in enumerate(partition):
            z = model.NewIntVar(0, DOMAIN_SIZE, f"z_{pidx}_{bidx}")
            model.Add(z <= s * n)
            z_for_partition.append(z)
        model.Add(sum(z_for_partition) == s * n)
        n_vars.append(n)
        z_vars.append(z_for_partition)
        active_vars.append(active)

    model.Add(sum(n_vars) == quotient_length)
    model.Add(sum(active_vars) <= max_active_partitions)

    for witness in WITNESSES:
        terms = []
        for partition, z_for_partition in zip(partitions, z_vars, strict=True):
            for block, z in zip(partition, z_for_partition, strict=True):
                if witness in block:
                    terms.append(z)
        model.Add(sum(terms) == TARGET_AGREEMENT)

    pair_equal_vars = {}
    selected_pair_vars = {}
    for pair in pairs():
        pair_equal = model.NewIntVar(0, quotient_length, f"pair_equal_{pair[0]}_{pair[1]}")
        selected_pair = model.NewIntVar(0, DOMAIN_SIZE, f"selected_pair_{pair[0]}_{pair[1]}")
        model.Add(
            pair_equal
            == sum(
                n
                for partition, n in zip(partitions, n_vars, strict=True)
                if partition_pair_same(partition, pair)
            )
        )
        selected_terms = []
        for partition, z_for_partition in zip(partitions, z_vars, strict=True):
            for block, z in zip(partition, z_for_partition, strict=True):
                if pair[0] in block and pair[1] in block:
                    selected_terms.append(z)
        model.Add(selected_pair == sum(selected_terms))
        model.Add(pair_equal <= quotient_degree_bound)
        if pair[1] == 7 and pair[0] <= 5:
            model.Add(selected_pair >= PAIR7_LOWER)
        pair_equal_vars[pair] = pair_equal
        selected_pair_vars[pair] = selected_pair

    eq_count = model.NewIntVar(0, quotient_length * 6, "equation_count")
    model.Add(eq_count == sum(equation_cost(partition) * n for partition, n in zip(partitions, n_vars, strict=True)))
    active_count = model.NewIntVar(0, max_active_partitions, "active_count")
    model.Add(active_count == sum(active_vars))
    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for idx in range(1, 6):
        model.Add(min_pair7 <= selected_pair_vars[(idx, 7)])
    max_pair_equal = model.NewIntVar(0, quotient_length, "max_pair_equal")
    for variable in pair_equal_vars.values():
        model.Add(max_pair_equal >= variable)

    if force_structural_defect:
        model.Add(eq_count <= variable_count - 1)
        model.Maximize(1000 * min_pair7 - 10 * max_pair_equal - active_count)
    else:
        model.Minimize(10000 * eq_count + 100 * max_pair_equal + active_count - min_pair7)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 0
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "s": s,
        "mode": "structural_defect_target" if force_structural_defect else "min_equation_fallback",
        "cp_sat_status": status_name,
        "feasible": feasible,
        "ortools_version": ortools_version,
        "quotient_length": quotient_length,
        "quotient_degree_bound": quotient_degree_bound,
        "variable_count": variable_count,
        "equation_count": None,
        "equation_gap_to_structural_defect": None,
        "active_partition_count": None,
        "support_vector": None,
        "pair7_counts": None,
        "max_pair_equal_h_count": None,
        "active_partitions": [],
        "best_failure_mode": "RANKAWARE_V2_CP_UNRESOLVED",
    }
    if not feasible:
        row["best_failure_mode"] = "RANKAWARE_V2_STRUCTURAL_DEFECT_NOT_FOUND" if force_structural_defect else "RANKAWARE_V2_CP_UNRESOLVED"
        return row

    support_vector = []
    for witness in WITNESSES:
        total = 0
        for partition, z_for_partition in zip(partitions, z_vars, strict=True):
            for block, z in zip(partition, z_for_partition, strict=True):
                if witness in block:
                    total += int(solver.Value(z))
        support_vector.append(total)
    selected_pair_counts = {
        f"{left}{right}": int(solver.Value(selected_pair_vars[(left, right)]))
        for left, right in pairs()
    }
    pair_equal_counts = {
        f"{left}{right}": int(solver.Value(pair_equal_vars[(left, right)]))
        for left, right in pairs()
    }
    active = []
    for partition, n, z_for_partition in zip(partitions, n_vars, z_vars, strict=True):
        n_value = int(solver.Value(n))
        if n_value == 0:
            continue
        active.append(
            {
                "quotient_fibers": n_value,
                "partition": [list(block) for block in partition],
                "selected_block_counts": [
                    {"block": list(block), "count": int(solver.Value(z))}
                    for block, z in zip(partition, z_for_partition, strict=True)
                    if int(solver.Value(z)) > 0
                ],
            }
        )
    active.sort(key=lambda item: (-int(item["quotient_fibers"]), item["partition"]))
    equation_count = int(solver.Value(eq_count))
    row.update(
        {
            "equation_count": equation_count,
            "equation_gap_to_structural_defect": equation_count - (variable_count - 1),
            "active_partition_count": int(solver.Value(active_count)),
            "support_vector": support_vector,
            "pair7_counts": [selected_pair_counts[f"{idx}7"] for idx in range(1, 6)],
            "selected_pair_counts": selected_pair_counts,
            "pair_equal_quotient_counts": pair_equal_counts,
            "pair_equal_h_counts": {key: s * value for key, value in pair_equal_counts.items()},
            "max_pair_equal_h_count": max(s * value for value in pair_equal_counts.values()),
            "active_partitions": active,
        }
    )
    row["best_failure_mode"] = (
        "RANKAWARE_V2_STRUCTURAL_DEFECT_TARGET"
        if equation_count < variable_count
        else "RANKAWARE_V2_MIN_EQUATION_FALLBACK"
    )
    return row


def build_record(time_limit: float, max_active_partitions: int) -> dict[str, Any]:
    previous = load_json(INPUT_DATA)
    long_realization = load_long_realization()
    results = []
    for s in S_VALUES:
        target = solve_model(s, time_limit, max_active_partitions, force_structural_defect=True)
        fallback = solve_model(s, time_limit, max_active_partitions, force_structural_defect=False)
        if fallback["feasible"]:
            coords = long_realization.expand_schedule(fallback)
            structural = long_realization.proxy_for_coordinates(coords, s)
            fallback["proxy_rank"] = structural["rank"]
            fallback["proxy_nullity"] = structural["nullity"]
            fallback["proxy_matrix_shape"] = structural["matrix_shape"]
        results.extend([target, fallback])
    targets = [row for row in results if row["best_failure_mode"] == "RANKAWARE_V2_STRUCTURAL_DEFECT_TARGET"]
    feasible_fallbacks = [row for row in results if row["mode"] == "min_equation_fallback" and row["feasible"]]
    best = min(
        feasible_fallbacks,
        key=lambda row: (
            row["equation_gap_to_structural_defect"],
            row["s"],
        ),
    ) if feasible_fallbacks else None
    proof_status = (
        "CANDIDATE / RANKAWARE_V2_STRUCTURAL_DEFECT_TARGET / PARTIAL / EXPERIMENTAL"
        if targets
        else "EXACT_EXTRACTION_NO_A327 / RANKAWARE_V2_NO_STRUCTURAL_DEFECT / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_structural_rank_features": {
            "proof_status": previous["proof_status"],
            "screens_tested": previous["structural_rank_features"]["screens_tested"],
            "structural_positive_screens": previous["structural_rank_features"]["structural_positive_screens"],
            "best_s": previous["structural_rank_features"]["best_s"],
            "best_structural_rank": previous["structural_rank_features"]["best_structural_rank"],
            "best_variable_count": previous["structural_rank_features"]["best_variable_count"],
            "failure_mode": previous["structural_rank_features"]["best_failure_mode"],
        },
        "rankaware_v2": {
            "s_values": S_VALUES,
            "time_limit_seconds": time_limit,
            "max_active_partitions": max_active_partitions,
            "models_tested": len(results),
            "structural_defect_targets_found": len(targets),
            "fallbacks_feasible": len(feasible_fallbacks),
            "best_s": None if best is None else best["s"],
            "best_equation_count": None if best is None else best["equation_count"],
            "best_variable_count": None if best is None else best["variable_count"],
            "best_equation_gap_to_structural_defect": None if best is None else best["equation_gap_to_structural_defect"],
            "best_proxy_rank": None if best is None else best.get("proxy_rank"),
            "best_proxy_nullity": None if best is None else best.get("proxy_nullity"),
            "best_failure_mode": (
                "RANKAWARE_V2_STRUCTURAL_DEFECT_TARGET"
                if targets
                else "RANKAWARE_V2_NO_STRUCTURAL_DEFECT"
            ),
        },
        "models": results,
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": REQUIRED_NONCLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--time-limit", type=float, default=30.0)
    parser.add_argument("--max-active-partitions", type=int, default=120)
    args = parser.parse_args()
    record = build_record(args.time_limit, args.max_active_partitions)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps({"proof_status": record["proof_status"], **record["rankaware_v2"]}, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_RANKAWARE_V2_STRUCTURAL_DEFECT_READY")


if __name__ == "__main__":
    main()
