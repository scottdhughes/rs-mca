#!/usr/bin/env python3
"""Block-count quotient partition grammar search for M1 a=327 order-8 lifts."""

from __future__ import annotations

import argparse
import importlib.util
import json
from itertools import combinations
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "b8d5a7e"
PREVIOUS_DATA = Path("experimental/data/m1_a327_order8_narrow_partition_grammar_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_order8_block_count_partition_grammar_search.json")
PARTITION_FIRST_SCRIPT = Path("experimental/scripts/scan_m1_a327_order8_partition_first_interpolation_search.py")

TRACK = "INTERLEAVED_LIST"
ROW = "RS[F_17^32,H,256]"
DENOMINATOR = "17^32"
TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
ORDER8_LENGTH = 8
BUCKET_SIZE = 64
PAIR_CAP = 255
PAIR7_LOWER = 142
VARIABLE_COUNT = 24
WITNESSES = tuple(range(1, 8))
GUARDED_TO_7 = tuple(range(1, 6))
BASELINE = 7
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track block-count quotient grammar",
    "global obstruction outside the tested order-8 block-count quotient model",
]


def require_ortools() -> tuple[Any, str]:
    try:
        from ortools.sat.python import cp_model  # type: ignore
        import ortools  # type: ignore

        return cp_model, str(ortools.__version__)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "OR-Tools is required. Run with "
            "/Users/scott/.venvs/rs-mca-ortools/bin/python "
            "experimental/scripts/scan_m1_a327_order8_block_count_partition_grammar_search.py"
        ) from exc


def load_partition_first_module() -> Any:
    spec = importlib.util.spec_from_file_location("m1_a327_partition_first", PARTITION_FIRST_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {PARTITION_FIRST_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PF = load_partition_first_module()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def block_family(block_sizes: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [tuple(block) for size in block_sizes for block in combinations(WITNESSES, size)]


def solve_block_count_model(
    mode: str,
    block_sizes: tuple[int, ...],
    time_limit: float,
    seed: int,
) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    blocks = block_family(block_sizes)
    model = cp_model.CpModel()
    active: list[list[Any]] = []
    selected: list[list[Any]] = []

    for bucket in range(ORDER8_LENGTH):
        active_row = []
        selected_row = []
        for bidx, block in enumerate(blocks):
            on = model.NewBoolVar(f"active_q{bucket}_b{bidx}")
            count = model.NewIntVar(0, BUCKET_SIZE, f"count_q{bucket}_b{bidx}")
            model.Add(count <= BUCKET_SIZE * on)
            model.Add(count >= on)
            active_row.append(on)
            selected_row.append(count)
        model.Add(sum(selected_row) == BUCKET_SIZE)
        # Positive selected blocks in one quotient bucket must be disjoint;
        # they are the positive-count blocks of a single equality partition.
        for witness in WITNESSES:
            model.Add(sum(active_row[bidx] for bidx, block in enumerate(blocks) if witness in block) <= 1)
        active.append(active_row)
        selected.append(selected_row)

    for witness in WITNESSES:
        model.Add(
            sum(
                selected[bucket][bidx]
                for bucket in range(ORDER8_LENGTH)
                for bidx, block in enumerate(blocks)
                if witness in block
            )
            == TARGET_AGREEMENT
        )

    pair_selected = {}
    pair_ambient = {}
    for left, right in pairs():
        selected_var = model.NewIntVar(0, DOMAIN_SIZE, f"selected_pair_{left}_{right}")
        ambient_var = model.NewIntVar(0, ORDER8_LENGTH, f"ambient_pair_{left}_{right}")
        model.Add(
            selected_var
            == sum(
                selected[bucket][bidx]
                for bucket in range(ORDER8_LENGTH)
                for bidx, block in enumerate(blocks)
                if left in block and right in block
            )
        )
        model.Add(
            ambient_var
            == sum(
                active[bucket][bidx]
                for bucket in range(ORDER8_LENGTH)
                for bidx, block in enumerate(blocks)
                if left in block and right in block
            )
        )
        if mode in {"pair_cap", "ambient_pair_cap"}:
            model.Add(selected_var <= PAIR_CAP)
        if mode in {"pair7_guard", "pair_cap", "ambient_pair_cap"}:
            if right == BASELINE and left in GUARDED_TO_7:
                model.Add(selected_var >= PAIR7_LOWER)
        if mode == "ambient_pair_cap":
            model.Add(ambient_var <= 3)
        pair_selected[(left, right)] = selected_var
        pair_ambient[(left, right)] = ambient_var

    equation_count = model.NewIntVar(0, ORDER8_LENGTH * 6, "equation_count")
    model.Add(
        equation_count
        == sum(
            (len(block) - 1) * active[bucket][bidx]
            for bucket in range(ORDER8_LENGTH)
            for bidx, block in enumerate(blocks)
        )
    )
    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for witness in GUARDED_TO_7:
        model.Add(min_pair7 <= pair_selected[(witness, BASELINE)])
    max_selected_pair = model.NewIntVar(0, DOMAIN_SIZE, "max_selected_pair")
    max_ambient_pair = model.NewIntVar(0, ORDER8_LENGTH, "max_ambient_pair")
    for pair in pairs():
        model.Add(max_selected_pair >= pair_selected[pair])
        model.Add(max_ambient_pair >= pair_ambient[pair])
    if mode == "support_only":
        model.Minimize(equation_count)
    elif mode == "pair7_guard":
        model.Minimize(1000 * equation_count + max_selected_pair - min_pair7)
    else:
        model.Minimize(1000 * equation_count + 10 * max_ambient_pair + max_selected_pair - min_pair7)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "mode": mode,
        "ortools_version": ortools_version,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "time_limit_seconds": time_limit,
        "block_sizes": list(block_sizes),
        "block_count": len(blocks),
        "equation_count": None,
        "support_vector": None,
        "pair7_counts": None,
        "max_selected_pair_count": None,
        "max_ambient_pair_buckets": None,
        "selected_partitions": None,
        "selected_block_counts": None,
        "best_failure_mode": (
            "BLOCK_COUNT_SUPPORT_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "support_only"
            else "BLOCK_COUNT_PAIR7_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "pair7_guard"
            else "BLOCK_COUNT_PAIR_CAP_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "pair_cap"
            else "BLOCK_COUNT_AMBIENT_INFEASIBLE"
            if status_name in {"INFEASIBLE", "MODEL_INVALID"} and mode == "ambient_pair_cap"
            else "BLOCK_COUNT_CP_UNRESOLVED"
        ),
    }
    if not feasible:
        return row

    active_blocks_by_bucket: list[list[tuple[int, ...]]] = []
    selected_block_counts = []
    selected_partitions = []
    for bucket in range(ORDER8_LENGTH):
        bucket_blocks = [
            block
            for bidx, block in enumerate(blocks)
            if int(solver.Value(active[bucket][bidx])) > 0
        ]
        active_blocks_by_bucket.append(bucket_blocks)
        covered = {witness for block in bucket_blocks for witness in block}
        partition = [list(block) for block in bucket_blocks]
        partition.extend([witness] for witness in WITNESSES if witness not in covered)
        selected_partitions.append(sorted(partition, key=lambda block: (block[0], len(block), block)))
        selected_block_counts.append(
            [
                {"block": list(block), "count": int(solver.Value(selected[bucket][bidx]))}
                for bidx, block in enumerate(blocks)
                if int(solver.Value(active[bucket][bidx])) > 0
            ]
        )

    selected_pair_counts = {
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in pair_selected.items()
    }
    ambient_pair_bucket_counts = {
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in pair_ambient.items()
    }
    row.update(
        {
            "equation_count": int(solver.Value(equation_count)),
            "support_vector": [
                sum(
                    entry["count"]
                    for bucket_entries in selected_block_counts
                    for entry in bucket_entries
                    if witness in entry["block"]
                )
                for witness in WITNESSES
            ],
            "pair7_counts": [selected_pair_counts[f"{idx}7"] for idx in GUARDED_TO_7],
            "selected_pair_counts": selected_pair_counts,
            "ambient_pair_bucket_counts": ambient_pair_bucket_counts,
            "max_selected_pair_count": max(selected_pair_counts.values()),
            "max_ambient_pair_buckets": max(ambient_pair_bucket_counts.values()),
            "selected_partitions": selected_partitions,
            "selected_block_counts": selected_block_counts,
            "best_failure_mode": "BLOCK_COUNT_SCHEDULE_FEASIBLE",
        }
    )
    return row


def audit_schedule(schedule: dict[str, Any]) -> dict[str, Any]:
    audit = PF.interpolation_audit(schedule)
    if not audit["attempted"]:
        audit["best_failure_mode"] = "BLOCK_COUNT_NO_SCHEDULE"
    elif audit["candidate_constructed"]:
        audit["best_failure_mode"] = "BLOCK_COUNT_EXACT_CANDIDATE"
    elif audit["nullity"] == 0:
        audit["best_failure_mode"] = "BLOCK_COUNT_INTERPOLATION_NULLITY_ZERO"
    else:
        audit["best_failure_mode"] = "BLOCK_COUNT_FORCED_PAIR_EQUALITY"
    return audit


def build_record(time_limit: float, block_sizes: tuple[int, ...], seed: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    modes = ["support_only", "pair7_guard", "pair_cap", "ambient_pair_cap"]
    models = [solve_block_count_model(mode, block_sizes, time_limit, seed + idx) for idx, mode in enumerate(modes)]
    fully_constrained = models[-1]
    audit = audit_schedule(fully_constrained) if fully_constrained["feasible"] else {
        "attempted": False,
        "rank": None,
        "nullity": None,
        "forced_equal_pairs": [],
        "candidate_constructed": False,
        "best_failure_mode": "BLOCK_COUNT_NO_SCHEDULE",
    }
    candidate = bool(audit["candidate_constructed"])
    if candidate:
        proof_status = "CANDIDATE / BLOCK_COUNT_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
    elif fully_constrained["feasible"]:
        proof_status = "EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
    elif fully_constrained["cp_sat_status"] in {"INFEASIBLE", "MODEL_INVALID"}:
        proof_status = "EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_AMBIENT_INFEASIBLE / PARTIAL / EXPERIMENTAL"
    else:
        proof_status = "EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_CP_UNRESOLVED / PARTIAL / EXPERIMENTAL"

    return {
        "track": TRACK,
        "row": ROW,
        "denominator": DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_narrow_grammar": {
            "proof_status": previous["proof_status"],
            "models_tested": previous["narrow_grammar_search"]["models_tested"],
            "feasible_support_schedules": previous["narrow_grammar_search"]["feasible_support_schedules"],
            "best_failure_mode": previous["narrow_grammar_search"]["best_failure_mode"],
        },
        "block_count_search": {
            "block_sizes": list(block_sizes),
            "block_count": len(block_family(block_sizes)),
            "time_limit_seconds_per_model": time_limit,
            "models_tested": len(models),
            "support_only_feasible": models[0]["feasible"],
            "pair7_guard_feasible": models[1]["feasible"],
            "pair_cap_feasible": models[2]["feasible"],
            "ambient_pair_cap_feasible": fully_constrained["feasible"],
            "interpolation_audit_attempted": audit["attempted"],
            "exact_candidates": 1 if candidate else 0,
            "best_failure_mode": audit["best_failure_mode"] if fully_constrained["feasible"] else fully_constrained["best_failure_mode"],
        },
        "models": models,
        "interpolation_audit": audit,
        "candidate": {
            "constructed": candidate,
            "seven_distinct": candidate,
            "agreement_vector": fully_constrained["support_vector"] if candidate else None,
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
    parser.add_argument("--block-sizes", type=int, nargs="+", default=[1, 2, 3, 4, 5, 6, 7])
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    record = build_record(args.time_limit, tuple(args.block_sizes), args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {"proof_status": record["proof_status"], **record["block_count_search"]}
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_ORDER8_BLOCK_COUNT_PARTITION_GRAMMAR_SEARCH_READY")


if __name__ == "__main__":
    main()
