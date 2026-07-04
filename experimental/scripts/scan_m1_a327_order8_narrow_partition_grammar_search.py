#!/usr/bin/env python3
"""Seeded narrow partition-grammar search for M1 a=327 order-8 quotient lifts."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from itertools import combinations
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "43a18ee"
PREVIOUS_DATA = Path("experimental/data/m1_a327_order8_partition_first_interpolation_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_order8_narrow_partition_grammar_search.json")
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
    "MCA/protocol consequence from this list-track narrow partition grammar",
    "global obstruction outside the tested order-8 narrow partition grammar",
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
            "experimental/scripts/scan_m1_a327_order8_narrow_partition_grammar_search.py"
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


def canonical_partition(blocks: list[tuple[int, ...]]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((tuple(sorted(block)) for block in blocks), key=lambda block: (block[0], len(block), block)))


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def equation_cost(partition: tuple[tuple[int, ...], ...]) -> int:
    return sum(len(block) - 1 for block in partition)


def same_block(partition: tuple[tuple[int, ...], ...], left: int, right: int) -> bool:
    return any(left in block and right in block for block in partition)


def with_residual_merge(
    zero_block: tuple[int, ...], residual: tuple[int, ...], merge_blocks: list[tuple[int, ...]]
) -> tuple[tuple[int, ...], ...]:
    used = {item for block in merge_blocks for item in block}
    blocks = [zero_block, *merge_blocks]
    blocks.extend((item,) for item in residual if item not in used)
    return canonical_partition(blocks)


def local_partitions(zero_members: tuple[int, ...], residual_mode: str) -> list[tuple[tuple[int, ...], ...]]:
    zero_block = tuple(sorted((BASELINE, *zero_members)))
    residual = tuple(witness for witness in WITNESSES if witness not in zero_block)
    out: set[tuple[tuple[int, ...], ...]] = {with_residual_merge(zero_block, residual, [])}
    if residual_mode.startswith("bounded"):
        max_residual_cost = int(residual_mode.removeprefix("bounded"))
        for residual_partition in PF.set_partitions(residual):
            if equation_cost(residual_partition) <= max_residual_cost:
                out.add(canonical_partition([zero_block, *residual_partition]))
        return sorted(out, key=lambda partition: (equation_cost(partition), len(partition), partition))
    if residual_mode in {"pairs", "mixed", "two_pairs"}:
        for pair in combinations(residual, 2):
            out.add(with_residual_merge(zero_block, residual, [tuple(pair)]))
    if residual_mode in {"triples", "mixed"}:
        for triple in combinations(residual, 3):
            out.add(with_residual_merge(zero_block, residual, [tuple(triple)]))
    if residual_mode in {"two_pairs", "mixed"}:
        residual_pairs = [tuple(pair) for pair in combinations(residual, 2)]
        for first, second in combinations(residual_pairs, 2):
            if set(first).isdisjoint(second):
                out.add(with_residual_merge(zero_block, residual, [first, second]))
    return sorted(out, key=lambda partition: (equation_cost(partition), len(partition), partition))


def root_pattern_key(pattern: dict[int, tuple[int, ...]]) -> tuple[tuple[int, tuple[int, ...]], ...]:
    return tuple((witness, tuple(pattern[witness])) for witness in GUARDED_TO_7)


def zero_members_by_bucket(pattern: dict[int, tuple[int, ...]]) -> list[tuple[int, ...]]:
    buckets: list[list[int]] = [[] for _ in range(ORDER8_LENGTH)]
    for witness, roots in pattern.items():
        for bucket in roots:
            buckets[bucket].append(witness)
    return [tuple(sorted(bucket)) for bucket in buckets]


def root_pattern_stats(pattern: dict[int, tuple[int, ...]]) -> dict[str, Any]:
    zero_members = zero_members_by_bucket(pattern)
    bucket_loads = [len(members) for members in zero_members]
    pair_bucket_counts = {
        f"{left}{right}": sum(1 for members in zero_members if left in members and right in members)
        for left, right in combinations(GUARDED_TO_7, 2)
    }
    return {
        "bucket_guard_loads": bucket_loads,
        "max_bucket_guard_load": max(bucket_loads),
        "min_bucket_guard_load": min(bucket_loads),
        "guard_pair_root_bucket_counts": pair_bucket_counts,
        "max_guard_pair_root_buckets": max(pair_bucket_counts.values()) if pair_bucket_counts else 0,
    }


def generated_root_patterns(limit: int, seed: int) -> list[dict[int, tuple[int, ...]]]:
    combos = [tuple(combo) for combo in combinations(range(ORDER8_LENGTH), 3)]
    seen: set[tuple[tuple[int, tuple[int, ...]], ...]] = set()
    patterns: list[dict[int, tuple[int, ...]]] = []

    for shared_roots in combinations(range(ORDER8_LENGTH), 3):
        pattern = {witness: tuple(shared_roots) for witness in GUARDED_TO_7}
        key = root_pattern_key(pattern)
        if key not in seen:
            seen.add(key)
            patterns.append(pattern)

    offsets = [(0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 2, 5), (0, 1, 4), (0, 3, 6)]
    for base in offsets:
        for multiplier in (1, 3, 5, 7):
            for shift_step in (1, 2, 3):
                pattern = {}
                for witness in GUARDED_TO_7:
                    roots = tuple(sorted(((multiplier * item + shift_step * (witness - 1)) % ORDER8_LENGTH) for item in base))
                    pattern[witness] = roots
                key = root_pattern_key(pattern)
                if key not in seen:
                    seen.add(key)
                    patterns.append(pattern)

    rng = random.Random(seed)
    attempts = 0
    while len(patterns) < limit and attempts < 10000:
        attempts += 1
        pattern = {witness: tuple(sorted(rng.sample(range(ORDER8_LENGTH), 3))) for witness in GUARDED_TO_7}
        stats = root_pattern_stats(pattern)
        # Keep some concentration: pair-to-7 support needs zero-block mass in multi-guard buckets.
        if stats["max_bucket_guard_load"] < 3:
            continue
        key = root_pattern_key(pattern)
        if key in seen:
            continue
        seen.add(key)
        patterns.append(pattern)

    return sorted(patterns[:limit], key=lambda pat: (-root_pattern_stats(pat)["max_bucket_guard_load"], root_pattern_key(pat)))


def solve_seeded_pattern(
    pattern_index: int,
    root_pattern: dict[int, tuple[int, ...]],
    residual_mode: str,
    time_limit: float,
    max_equation_count: int | None,
    seed: int,
) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    zero_members = zero_members_by_bucket(root_pattern)
    partitions_by_bucket = [local_partitions(members, residual_mode) for members in zero_members]
    model = cp_model.CpModel()

    choose: list[list[Any]] = []
    selected: list[list[list[Any]]] = []
    for bucket, partitions in enumerate(partitions_by_bucket):
        choose_row = []
        selected_row = []
        for pidx, partition in enumerate(partitions):
            chosen = model.NewBoolVar(f"choose_q{bucket}_p{pidx}")
            choose_row.append(chosen)
            block_counts = []
            for bidx, _block in enumerate(partition):
                count = model.NewIntVar(0, BUCKET_SIZE, f"sel_q{bucket}_p{pidx}_b{bidx}")
                model.Add(count <= BUCKET_SIZE * chosen)
                block_counts.append(count)
            selected_row.append(block_counts)
        model.Add(sum(choose_row) == 1)
        model.Add(sum(count for block_counts in selected_row for count in block_counts) == BUCKET_SIZE)
        choose.append(choose_row)
        selected.append(selected_row)

    for witness in WITNESSES:
        model.Add(
            sum(
                selected[bucket][pidx][bidx]
                for bucket, partitions in enumerate(partitions_by_bucket)
                for pidx, partition in enumerate(partitions)
                for bidx, block in enumerate(partition)
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
                selected[bucket][pidx][bidx]
                for bucket, partitions in enumerate(partitions_by_bucket)
                for pidx, partition in enumerate(partitions)
                for bidx, block in enumerate(partition)
                if left in block and right in block
            )
        )
        model.Add(
            ambient_var
            == sum(
                choose[bucket][pidx]
                for bucket, partitions in enumerate(partitions_by_bucket)
                for pidx, partition in enumerate(partitions)
                if same_block(partition, left, right)
            )
        )
        model.Add(selected_var <= PAIR_CAP)
        model.Add(ambient_var <= 3)
        if right == BASELINE and left in GUARDED_TO_7:
            model.Add(selected_var >= PAIR7_LOWER)
            model.Add(ambient_var == 3)
        pair_selected[(left, right)] = selected_var
        pair_ambient[(left, right)] = ambient_var

    equation_count = model.NewIntVar(0, ORDER8_LENGTH * 6, "equation_count")
    model.Add(
        equation_count
        == sum(
            equation_cost(partition) * choose[bucket][pidx]
            for bucket, partitions in enumerate(partitions_by_bucket)
            for pidx, partition in enumerate(partitions)
        )
    )
    if max_equation_count is not None:
        model.Add(equation_count <= max_equation_count)

    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for witness in GUARDED_TO_7:
        model.Add(min_pair7 <= pair_selected[(witness, BASELINE)])
    max_ambient = model.NewIntVar(0, 3, "max_ambient")
    for variable in pair_ambient.values():
        model.Add(max_ambient >= variable)
    model.Minimize(1000 * equation_count + 25 * max_ambient - min_pair7)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed + pattern_index
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "pattern_index": pattern_index,
        "residual_mode": residual_mode,
        "root_buckets_by_witness": {str(witness): list(root_pattern[witness]) for witness in GUARDED_TO_7},
        "root_pattern_stats": root_pattern_stats(root_pattern),
        "ortools_version": ortools_version,
        "time_limit_seconds": time_limit,
        "max_equation_count": max_equation_count,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "local_partition_counts": [len(partitions) for partitions in partitions_by_bucket],
        "equation_count": None,
        "support_vector": None,
        "pair7_counts": None,
        "max_ambient_pair_buckets": None,
        "selected_partitions": None,
        "selected_block_counts": None,
        "best_failure_mode": "NARROW_GRAMMAR_SUPPORT_INFEASIBLE"
        if status_name in {"INFEASIBLE", "MODEL_INVALID"}
        else "NARROW_GRAMMAR_CP_UNRESOLVED",
    }
    if not feasible:
        return row

    selected_partitions = []
    selected_block_counts = []
    for bucket, partitions in enumerate(partitions_by_bucket):
        pidx = next(idx for idx, variable in enumerate(choose[bucket]) if solver.Value(variable))
        partition = partitions[pidx]
        selected_partitions.append([list(block) for block in partition])
        selected_block_counts.append(
            [
                {"block": list(block), "count": int(solver.Value(selected[bucket][pidx][bidx]))}
                for bidx, block in enumerate(partition)
                if int(solver.Value(selected[bucket][pidx][bidx])) > 0
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
            "max_ambient_pair_buckets": max(ambient_pair_bucket_counts.values()),
            "selected_partitions": selected_partitions,
            "selected_block_counts": selected_block_counts,
            "best_failure_mode": "NARROW_GRAMMAR_SCHEDULE_FEASIBLE",
        }
    )
    return row


def audit_schedule(schedule: dict[str, Any]) -> dict[str, Any]:
    audit = PF.interpolation_audit(schedule)
    if not audit["attempted"]:
        audit["best_failure_mode"] = "NARROW_GRAMMAR_NO_SCHEDULE"
    elif audit["candidate_constructed"]:
        audit["best_failure_mode"] = "NARROW_GRAMMAR_EXACT_CANDIDATE"
    elif audit["nullity"] == 0:
        audit["best_failure_mode"] = "NARROW_GRAMMAR_INTERPOLATION_NULLITY_ZERO"
    else:
        audit["best_failure_mode"] = "NARROW_GRAMMAR_FORCED_PAIR_EQUALITY"
    return audit


def build_record(
    root_patterns: int,
    time_limit: float,
    seed: int,
    residual_modes: list[str],
    max_equation_count: int | None,
    stop_after_feasible: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    patterns = generated_root_patterns(root_patterns, seed)
    results: list[dict[str, Any]] = []
    feasible_results: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    best_audit: dict[str, Any] | None = None
    best_schedule: dict[str, Any] | None = None

    for pattern_index, pattern in enumerate(patterns):
        for residual_mode in residual_modes:
            result = solve_seeded_pattern(
                pattern_index=pattern_index,
                root_pattern=pattern,
                residual_mode=residual_mode,
                time_limit=time_limit,
                max_equation_count=max_equation_count,
                seed=seed,
            )
            results.append(result)
            if not result["feasible"]:
                continue
            feasible_results.append(result)
            audit = audit_schedule(result)
            audits.append({"pattern_index": pattern_index, "residual_mode": residual_mode, **audit})
            if best_audit is None or (
                (audit["candidate_constructed"], audit["nullity"] or -1, -(audit["rank"] or 999))
                > (
                    best_audit["candidate_constructed"],
                    best_audit["nullity"] or -1,
                    -(best_audit["rank"] or 999),
                )
            ):
                best_audit = audit
                best_schedule = result
            if audit["candidate_constructed"] or (
                stop_after_feasible and len(feasible_results) >= stop_after_feasible
            ):
                break
        if best_audit and best_audit["candidate_constructed"]:
            break
        if stop_after_feasible and len(feasible_results) >= stop_after_feasible:
            break

    if best_audit is None:
        best_audit = {
            "attempted": False,
            "rank": None,
            "nullity": None,
            "forced_equal_pairs": [],
            "candidate_constructed": False,
            "best_failure_mode": "NARROW_GRAMMAR_NO_SUPPORT_SCHEDULE",
        }
    candidate = bool(best_audit["candidate_constructed"])
    if candidate:
        proof_status = "CANDIDATE / NARROW_GRAMMAR_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
    elif feasible_results:
        proof_status = "EXACT_EXTRACTION_NO_A327 / NARROW_GRAMMAR_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
    else:
        proof_status = "EXACT_EXTRACTION_NO_A327 / NARROW_GRAMMAR_NO_SUPPORT_SCHEDULE / PARTIAL / EXPERIMENTAL"

    search_summary = {
        "root_patterns_requested": root_patterns,
        "root_patterns_generated": len(patterns),
        "residual_modes": residual_modes,
        "time_limit_seconds_per_model": time_limit,
        "max_equation_count": max_equation_count,
        "models_tested": len(results),
        "feasible_support_schedules": len(feasible_results),
        "interpolation_audits": len(audits),
        "exact_candidates": 1 if candidate else 0,
        "best_equation_count": best_schedule["equation_count"] if best_schedule else None,
        "best_interpolation_rank": best_audit["rank"],
        "best_interpolation_nullity": best_audit["nullity"],
        "best_failure_mode": best_audit["best_failure_mode"],
    }
    return {
        "track": TRACK,
        "row": ROW,
        "denominator": DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_partition_first": {
            "proof_status": previous["proof_status"],
            "structural_defect_target_feasible": previous["partition_first_search"][
                "structural_defect_target_feasible"
            ],
            "support_feasibility_feasible": previous["partition_first_search"]["support_feasibility_feasible"],
            "best_failure_mode": previous["partition_first_search"]["best_failure_mode"],
        },
        "narrow_grammar_search": search_summary,
        "models": results,
        "interpolation_audits": audits,
        "best_schedule": best_schedule,
        "interpolation_audit": best_audit,
        "candidate": {
            "constructed": candidate,
            "seven_distinct": candidate,
            "agreement_vector": best_schedule["support_vector"] if candidate and best_schedule else None,
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
    parser.add_argument("--root-patterns", type=int, default=64)
    parser.add_argument("--time-limit", type=float, default=5.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--residual-modes", nargs="+", default=["bounded3", "bounded4", "mixed"])
    parser.add_argument("--max-equation-count", type=int, default=30)
    parser.add_argument("--no-equation-cap", action="store_true")
    parser.add_argument("--stop-after-feasible", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        root_patterns=args.root_patterns,
        time_limit=args.time_limit,
        seed=args.seed,
        residual_modes=args.residual_modes,
        max_equation_count=None if args.no_equation_cap else args.max_equation_count,
        stop_after_feasible=args.stop_after_feasible,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {"proof_status": record["proof_status"], **record["narrow_grammar_search"]}
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_ORDER8_NARROW_PARTITION_GRAMMAR_SEARCH_READY")


if __name__ == "__main__":
    main()
