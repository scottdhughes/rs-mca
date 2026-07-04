#!/usr/bin/env python3
"""Rank-aware s=4 quotient schedule generator for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "7e21f1d"
INPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_label_rank_feedback.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_rank_aware_schedule_generator.json")
REALIZATION_SCAN = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_realization_search.py")
LABEL_SCAN = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_label_rank_feedback.py")

TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
WITNESSES = tuple(range(1, 8))
PAIR_CAP = 255
PAIR7_LOWER = 142
S_VALUE = 4
QUOTIENT_LENGTH = DOMAIN_SIZE // S_VALUE
QUOTIENT_DEGREE_BOUND = PAIR_CAP // S_VALUE
OBJECTIVES = ["pair7_slack", "min_equation_count", "min_pair_equal", "min_active_equation"]

REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the tested rank-aware quotient schedule generator",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
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
            "experimental/scripts/scan_m1_a327_quotient_subgroup_rank_aware_schedule_generator.py"
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


def solve_schedule(objective: str, time_limit: float, max_active_partitions: int) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    partitions = set_partitions(WITNESSES)
    model = cp_model.CpModel()
    n_vars = []
    z_vars: list[list[Any]] = []
    active_vars = []
    for pidx, partition in enumerate(partitions):
        active = model.NewBoolVar(f"active_{pidx}")
        n = model.NewIntVar(0, QUOTIENT_LENGTH, f"n_{pidx}")
        model.Add(n > 0).OnlyEnforceIf(active)
        model.Add(n == 0).OnlyEnforceIf(active.Not())
        z_for_partition = []
        for bidx, _block in enumerate(partition):
            z = model.NewIntVar(0, DOMAIN_SIZE, f"z_{pidx}_{bidx}")
            model.Add(z <= S_VALUE * n)
            z_for_partition.append(z)
        model.Add(sum(z_for_partition) == S_VALUE * n)
        n_vars.append(n)
        z_vars.append(z_for_partition)
        active_vars.append(active)

    model.Add(sum(n_vars) == QUOTIENT_LENGTH)
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
        pair_equal = model.NewIntVar(0, QUOTIENT_LENGTH, f"pair_equal_{pair[0]}_{pair[1]}")
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
        model.Add(pair_equal <= QUOTIENT_DEGREE_BOUND)
        if pair[1] == 7 and pair[0] <= 5:
            model.Add(selected_pair >= PAIR7_LOWER)
        pair_equal_vars[pair] = pair_equal
        selected_pair_vars[pair] = selected_pair

    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for idx in range(1, 6):
        model.Add(min_pair7 <= selected_pair_vars[(idx, 7)])
    max_pair_equal = model.NewIntVar(0, QUOTIENT_LENGTH, "max_pair_equal")
    for variable in pair_equal_vars.values():
        model.Add(max_pair_equal >= variable)
    eq_count = model.NewIntVar(0, QUOTIENT_LENGTH * 6, "equation_count")
    model.Add(eq_count == sum(equation_cost(partition) * n for partition, n in zip(partitions, n_vars, strict=True)))
    active_count = model.NewIntVar(0, max_active_partitions, "active_count")
    model.Add(active_count == sum(active_vars))

    if objective == "pair7_slack":
        model.Maximize(1000 * min_pair7 - 10 * max_pair_equal - eq_count)
    elif objective == "min_equation_count":
        model.Minimize(1000 * eq_count + 10 * max_pair_equal - min_pair7)
    elif objective == "min_pair_equal":
        model.Minimize(1000 * max_pair_equal + eq_count - min_pair7)
    elif objective == "min_active_equation":
        model.Minimize(1000 * active_count + eq_count + max_pair_equal)
    else:
        raise ValueError(f"unknown objective {objective}")

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 0
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "objective": objective,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "ortools_version": ortools_version,
        "equation_count": None,
        "active_partition_count": None,
        "support_vector": None,
        "pair7_counts": None,
        "max_pair_equal_quotient_count": None,
        "max_pair_equal_h_count": None,
        "active_partitions": [],
        "best_failure_mode": "RANK_AWARE_CP_UNRESOLVED",
    }
    if not feasible:
        row["best_failure_mode"] = "RANK_AWARE_CP_INFEASIBLE" if status_name == "INFEASIBLE" else "RANK_AWARE_CP_UNRESOLVED"
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
    pair_equal_quotient_counts = {
        f"{left}{right}": int(solver.Value(pair_equal_vars[(left, right)]))
        for left, right in pairs()
    }
    pair_equal_h_counts = {key: S_VALUE * value for key, value in pair_equal_quotient_counts.items()}
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
    pair7_counts = [selected_pair_counts[f"{idx}7"] for idx in range(1, 6)]
    row.update(
        {
            "equation_count": int(solver.Value(eq_count)),
            "active_partition_count": int(solver.Value(active_count)),
            "support_vector": support_vector,
            "pair7_counts": pair7_counts,
            "selected_pair_counts": selected_pair_counts,
            "pair_equal_quotient_counts": pair_equal_quotient_counts,
            "pair_equal_h_counts": pair_equal_h_counts,
            "max_pair_equal_quotient_count": max(pair_equal_quotient_counts.values()),
            "max_pair_equal_h_count": max(pair_equal_h_counts.values()),
            "active_partitions": active,
        }
    )
    if support_vector != [TARGET_AGREEMENT] * len(WITNESSES):
        row["best_failure_mode"] = "RANK_AWARE_SUPPORT_FAIL"
    elif max(pair_equal_h_counts.values()) > PAIR_CAP:
        row["best_failure_mode"] = "RANK_AWARE_PAIR_CAP_FAIL"
    elif min(pair7_counts) < PAIR7_LOWER:
        row["best_failure_mode"] = "RANK_AWARE_PAIR7_FAIL"
    else:
        row["best_failure_mode"] = "RANK_AWARE_CP_FEASIBLE"
    return row


def evaluate_schedule(schedule: dict[str, Any], realization_scan: Any, label_scan: Any, random_trials: int, seed: int) -> dict[str, Any]:
    coordinates = realization_scan.expand_schedule(schedule)
    payloads = label_scan.partition_payloads(coordinates)
    base_signature = label_scan.signature_for_coordinates(coordinates)
    best = None
    tested = 0
    positive = 0
    for label, signature in label_scan.candidate_signatures(base_signature, random_trials, seed):
        labelled = label_scan.rebuild_coordinates(signature, payloads)
        proxy = label_scan.proxy_for_coordinates(realization_scan, labelled)
        tested += 1
        if proxy["nullity"] > 0:
            positive += 1
        row = {
            "label": label,
            "proxy_rank": proxy["rank"],
            "proxy_nullity": proxy["nullity"],
            "matrix_shape": proxy["matrix_shape"],
            "best_failure_mode": proxy["best_failure_mode"],
        }
        if best is None or (row["proxy_rank"], -row["proxy_nullity"], row["label"]) < (
            best["proxy_rank"],
            -best["proxy_nullity"],
            best["label"],
        ):
            best = row
    assert best is not None
    return {
        "labellings_tested": tested,
        "proxy_positive_labellings": positive,
        "best_label": best["label"],
        "best_proxy_rank": best["proxy_rank"],
        "best_proxy_nullity": best["proxy_nullity"],
        "best_matrix_shape": best["matrix_shape"],
        "best_failure_mode": best["best_failure_mode"],
    }


def build_record(time_limit: float, max_active_partitions: int, random_trials: int, seed: int) -> dict[str, Any]:
    previous = load_json(INPUT_DATA)
    realization_scan = load_module(REALIZATION_SCAN, "quotient_realization_scan")
    label_scan = load_module(LABEL_SCAN, "quotient_label_scan")
    generated = []
    for objective in OBJECTIVES:
        schedule = solve_schedule(objective, time_limit, max_active_partitions)
        if schedule["feasible"]:
            schedule["proxy_label_feedback"] = evaluate_schedule(
                schedule,
                realization_scan,
                label_scan,
                random_trials=random_trials,
                seed=seed,
            )
        generated.append(schedule)
    feasible = [row for row in generated if row["feasible"]]
    positive = [
        row
        for row in feasible
        if row.get("proxy_label_feedback", {}).get("proxy_positive_labellings", 0) > 0
    ]
    best = None
    for row in feasible:
        feedback = row["proxy_label_feedback"]
        key = (
            feedback["best_proxy_rank"],
            -feedback["best_proxy_nullity"],
            row["equation_count"],
            row["active_partition_count"],
            row["objective"],
        )
        if best is None or key < best[0]:
            best = (key, row)
    best_row = None if best is None else best[1]
    proof_status = (
        "CANDIDATE / RANK_AWARE_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if positive
        else "EXACT_EXTRACTION_NO_A327 / RANK_AWARE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
    )
    if not feasible:
        proof_status = "PARTIAL / RANK_AWARE_CP_UNRESOLVED / EXPERIMENTAL"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_label_rank_feedback": {
            "proof_status": previous["proof_status"],
            "labellings_tested": previous["label_rank_feedback"]["labellings_tested"],
            "proxy_positive_labellings": previous["label_rank_feedback"]["proxy_positive_labellings"],
            "best_proxy_rank": previous["label_rank_feedback"]["best_proxy_rank"],
            "best_proxy_nullity": previous["label_rank_feedback"]["best_proxy_nullity"],
            "failure_mode": previous["label_rank_feedback"]["best_failure_mode"],
        },
        "rank_aware_schedule_generator": {
            "objectives": OBJECTIVES,
            "time_limit_seconds": time_limit,
            "max_active_partitions": max_active_partitions,
            "random_trials_per_schedule": random_trials,
            "seed": seed,
            "schedules_tested": len(generated),
            "cp_feasible_schedules": len(feasible),
            "proxy_positive_schedules": len(positive),
            "best_objective": None if best_row is None else best_row["objective"],
            "best_equation_count": None if best_row is None else best_row["equation_count"],
            "best_active_partition_count": None if best_row is None else best_row["active_partition_count"],
            "best_proxy_rank": None if best_row is None else best_row["proxy_label_feedback"]["best_proxy_rank"],
            "best_proxy_nullity": None if best_row is None else best_row["proxy_label_feedback"]["best_proxy_nullity"],
            "best_matrix_shape": None if best_row is None else best_row["proxy_label_feedback"]["best_matrix_shape"],
            "best_failure_mode": (
                "RANK_AWARE_PROXY_POSITIVE"
                if positive
                else ("RANK_AWARE_PROXY_FULL_RANK" if feasible else "RANK_AWARE_CP_UNRESOLVED")
            ),
        },
        "generated_schedules": generated,
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
    parser.add_argument("--time-limit", type=float, default=15.0)
    parser.add_argument("--max-active-partitions", type=int, default=80)
    parser.add_argument("--random-trials", type=int, default=16)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    record = build_record(args.time_limit, args.max_active_partitions, args.random_trials, args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps({"proof_status": record["proof_status"], **record["rank_aware_schedule_generator"]}, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_RANK_AWARE_SCHEDULE_GENERATOR_READY")


if __name__ == "__main__":
    main()
