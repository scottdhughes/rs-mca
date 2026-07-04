#!/usr/bin/env python3
"""OR-Tools quotient-subgroup primal-kernel screen for M1 a=327."""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "cff22a0"
PREVIOUS_DATA = Path("experimental/data/m1_a327_collision_budget_rightkernel_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_primal_kernel_search.json")
ORTOOLS_PYTHON = Path("/Users/scott/.venvs/rs-mca-ortools/bin/python")

TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
WITNESSES = tuple(range(1, 8))
PAIR_CAP = 255
PAIR7_LOWER = 142
S_VALUES = [32, 16, 8, 4]

REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the tested quotient-subgroup count screen",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require_ortools() -> tuple[Any, str]:
    try:
        from ortools.sat.python import cp_model  # type: ignore
        import ortools  # type: ignore

        return cp_model, str(ortools.__version__)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "OR-Tools is required. Run with "
            f"{ORTOOLS_PYTHON} {Path(__file__).as_posix()} --write --json"
        ) from exc


def tools_status() -> dict[str, Any]:
    if not ORTOOLS_PYTHON.exists():
        return {
            "ortools_python": str(ORTOOLS_PYTHON),
            "ortools_available": False,
            "ortools_version": None,
            "cp_sat_smoke": False,
        }
    code = (
        "from ortools.sat.python import cp_model\n"
        "import ortools\n"
        "m=cp_model.CpModel(); x=m.NewBoolVar('x'); m.Add(x==1)\n"
        "s=cp_model.CpSolver(); status=s.Solve(m)\n"
        "print(ortools.__version__); print(int(status)); print(s.Value(x))\n"
    )
    try:
        completed = subprocess.run(
            [str(ORTOOLS_PYTHON), "-c", code],
            check=True,
            text=True,
            capture_output=True,
            timeout=20,
        )
        lines = completed.stdout.strip().splitlines()
        return {
            "ortools_python": str(ORTOOLS_PYTHON),
            "ortools_available": True,
            "ortools_version": lines[0] if lines else None,
            "cp_sat_smoke": len(lines) >= 3 and lines[-1] == "1",
        }
    except Exception as exc:  # pragma: no cover - diagnostic only
        return {
            "ortools_python": str(ORTOOLS_PYTHON),
            "ortools_available": False,
            "ortools_version": None,
            "cp_sat_smoke": False,
            "error": type(exc).__name__,
        }


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
    left, right = pair
    return any(left in block and right in block for block in partition)


def solve_count_model(s: int, time_limit: float, max_active_partitions: int) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    quotient_length = DOMAIN_SIZE // s
    quotient_degree_bound = PAIR_CAP // s
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

    pair_equal_exprs = {}
    selected_pair_exprs = {}
    for pair in pairs():
        eq_terms = [
            n
            for partition, n in zip(partitions, n_vars, strict=True)
            if partition_pair_same(partition, pair)
        ]
        selected_terms = []
        for partition, z_for_partition in zip(partitions, z_vars, strict=True):
            for block, z in zip(partition, z_for_partition, strict=True):
                if pair[0] in block and pair[1] in block:
                    selected_terms.append(z)
        pair_equal = model.NewIntVar(0, quotient_length, f"pair_equal_{pair[0]}_{pair[1]}")
        selected_pair = model.NewIntVar(0, DOMAIN_SIZE, f"selected_pair_{pair[0]}_{pair[1]}")
        model.Add(pair_equal == sum(eq_terms))
        model.Add(selected_pair == sum(selected_terms))
        model.Add(pair_equal <= quotient_degree_bound)
        if pair[1] == 7 and pair[0] <= 5:
            model.Add(selected_pair >= PAIR7_LOWER)
        pair_equal_exprs[pair] = pair_equal
        selected_pair_exprs[pair] = selected_pair

    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    pair7_terms = [selected_pair_exprs[(idx, 7)] for idx in range(1, 6)]
    for term in pair7_terms:
        model.Add(min_pair7 <= term)
    max_pair_equal = model.NewIntVar(0, quotient_length, "max_pair_equal")
    for term in pair_equal_exprs.values():
        model.Add(max_pair_equal >= term)

    # Prefer pair-to-7 slack, then fewer quotient equality collisions.
    model.Maximize(1000 * min_pair7 - max_pair_equal)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 0
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)

    row: dict[str, Any] = {
        "s": s,
        "quotient_length": quotient_length,
        "quotient_degree_bound": quotient_degree_bound,
        "fiber_size": s,
        "partition_count": len(partitions),
        "max_active_partitions": max_active_partitions,
        "ortools_version": ortools_version,
        "cp_sat_status": status_name,
        "cp_sat_objective": None,
        "feasible": feasible,
        "support_vector": None,
        "pair_equal_quotient_counts": None,
        "pair_equal_h_counts": None,
        "selected_pair_counts": None,
        "pair7_counts": None,
        "max_pair_equal_quotient_count": None,
        "max_pair_equal_h_count": None,
        "active_partition_count": None,
        "active_partitions": [],
        "best_failure_mode": None,
    }
    if not feasible:
        row["best_failure_mode"] = (
            "QUOTIENT_CP_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"}
            else "QUOTIENT_CP_UNRESOLVED"
        )
        return row

    support_vector = []
    for witness in WITNESSES:
        total = 0
        for partition, z_for_partition in zip(partitions, z_vars, strict=True):
            for block, z in zip(partition, z_for_partition, strict=True):
                if witness in block:
                    total += int(solver.Value(z))
        support_vector.append(total)

    pair_equal_counts = {
        f"{left}{right}": int(solver.Value(pair_equal_exprs[(left, right)]))
        for left, right in pairs()
    }
    pair_equal_h_counts = {key: s * value for key, value in pair_equal_counts.items()}
    selected_pair_counts = {
        f"{left}{right}": int(solver.Value(selected_pair_exprs[(left, right)]))
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

    pair7_counts = [selected_pair_counts[f"{idx}7"] for idx in range(1, 6)]
    row.update(
        {
            "cp_sat_objective": solver.ObjectiveValue(),
            "support_vector": support_vector,
            "pair_equal_quotient_counts": pair_equal_counts,
            "pair_equal_h_counts": pair_equal_h_counts,
            "selected_pair_counts": selected_pair_counts,
            "pair7_counts": pair7_counts,
            "max_pair_equal_quotient_count": max(pair_equal_counts.values()),
            "max_pair_equal_h_count": max(pair_equal_h_counts.values()),
            "active_partition_count": len(active),
            "active_partitions": active,
        }
    )
    if support_vector != [TARGET_AGREEMENT] * 7:
        row["best_failure_mode"] = "QUOTIENT_SUPPORT_FAIL"
    elif max(pair_equal_h_counts.values()) > PAIR_CAP:
        row["best_failure_mode"] = "QUOTIENT_PAIR_CAP_FAIL"
    elif min(pair7_counts) < PAIR7_LOWER:
        row["best_failure_mode"] = "QUOTIENT_PAIR7_GUARD_FAIL"
    else:
        row["best_failure_mode"] = "QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING"
    return row


def sort_screen(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        not bool(row["feasible"]),
        -(min(row["pair7_counts"]) if row["pair7_counts"] else -1),
        row["max_pair_equal_h_count"] if row["max_pair_equal_h_count"] is not None else 10**9,
        row["s"],
    )


def build_record(time_limit: float, max_active_partitions: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    screens = [solve_count_model(s, time_limit, max_active_partitions) for s in S_VALUES]
    feasible = [row for row in screens if row["feasible"]]
    best = sorted(screens, key=sort_screen)[0] if screens else None
    proof_status = (
        "CANDIDATE / QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING / PARTIAL / EXPERIMENTAL"
        if feasible
        else "EXACT_EXTRACTION_NO_A327 / QUOTIENT_CP_INFEASIBLE / PARTIAL / EXPERIMENTAL"
    )
    failure = (
        "QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING"
        if feasible
        else "QUOTIENT_CP_INFEASIBLE"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_collision_budget_rightkernel_codesign": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_constructed": previous["collision_budget_rightkernel_codesign"][
                "basis_profiles_constructed"
            ],
            "rightkernel_collision_budget_profiles": previous["collision_budget_rightkernel_codesign"][
                "rightkernel_collision_budget_profiles"
            ],
            "proxy_ranked_profiles": previous["collision_budget_rightkernel_codesign"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["collision_budget_rightkernel_codesign"]["proxy_positive_profiles"],
            "best_proxy_rank": previous["collision_budget_rightkernel_codesign"]["best_proxy_rank"],
            "best_proxy_nullity": previous["collision_budget_rightkernel_codesign"]["best_proxy_nullity"],
            "failure_mode": previous["collision_budget_rightkernel_codesign"]["best_failure_mode"],
        },
        "tools": tools_status(),
        "quotient_subgroup_primal_kernel_search": {
            "s_values": S_VALUES,
            "time_limit_seconds": time_limit,
            "max_active_partitions": max_active_partitions,
            "screens_tested": len(screens),
            "cp_feasible_screens": len(feasible),
            "best_s": None if best is None else best["s"],
            "best_pair7_counts": None if best is None else best["pair7_counts"],
            "best_max_pair_equal_h_count": None if best is None else best["max_pair_equal_h_count"],
            "best_active_partition_count": None if best is None else best["active_partition_count"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in screens)),
        },
        "screens": screens,
        "best_screen": best,
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
    parser.add_argument("--time-limit", type=float, default=10.0)
    parser.add_argument("--max-active-partitions", type=int, default=12)
    args = parser.parse_args()
    record = build_record(args.time_limit, args.max_active_partitions)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["quotient_subgroup_primal_kernel_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "screens_tested": search["screens_tested"],
                    "cp_feasible_screens": search["cp_feasible_screens"],
                    "best_s": search["best_s"],
                    "best_pair7_counts": search["best_pair7_counts"],
                    "best_max_pair_equal_h_count": search["best_max_pair_equal_h_count"],
                    "best_active_partition_count": search["best_active_partition_count"],
                    "best_failure_mode": search["best_failure_mode"],
                    "ortools_available": record["tools"]["ortools_available"],
                    "ortools_version": record["tools"]["ortools_version"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_PRIMAL_KERNEL_SEARCH_READY")


if __name__ == "__main__":
    main()
