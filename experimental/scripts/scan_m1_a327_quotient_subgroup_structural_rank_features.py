#!/usr/bin/env python3
"""Structural-rank diagnostics for feasible M1 a=327 quotient-subgroup fronts."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "e472d07"
INPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_long_cpsat_front.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_structural_rank_features.json")
LONG_REALIZATION_SCAN = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_long_front_realization.py")

TARGET_AGREEMENT = 327
DOMAIN_SIZE = 512
PAIR_CAP = 255
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the tested structural-rank diagnostics",
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


def partition_key(partition: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted((tuple(sorted(block)) for block in partition), key=lambda block: (block[0], len(block), block)))


def variable_support(witness: int, degree_bound: int) -> range | None:
    if witness == 7:
        return None
    start = (witness - 1) * (degree_bound + 1)
    return range(start, start + degree_bound + 1)


def row_supports_for_coordinates(coordinates: list[dict[str, Any]], s: int) -> list[tuple[int, ...]]:
    degree_bound = PAIR_CAP // s
    supports = []
    for coordinate in coordinates:
        for block in partition_key(coordinate["partition"]):
            if len(block) <= 1:
                continue
            anchor = block[0]
            anchor_support = variable_support(anchor, degree_bound)
            for witness in block[1:]:
                columns: set[int] = set()
                witness_support = variable_support(witness, degree_bound)
                if witness_support is not None:
                    columns.update(witness_support)
                if anchor_support is not None:
                    columns.update(anchor_support)
                supports.append(tuple(sorted(columns)))
    return supports


def hopcroft_karp(row_supports: list[tuple[int, ...]], variable_count: int) -> int:
    adjacency = [list(support) for support in row_supports]
    row_match = [-1] * len(adjacency)
    col_match = [-1] * variable_count
    distance = [0] * len(adjacency)

    def bfs() -> bool:
        queue: deque[int] = deque()
        found = False
        for row in range(len(adjacency)):
            if row_match[row] == -1:
                distance[row] = 0
                queue.append(row)
            else:
                distance[row] = -1
        while queue:
            row = queue.popleft()
            for col in adjacency[row]:
                matched_row = col_match[col]
                if matched_row == -1:
                    found = True
                elif distance[matched_row] == -1:
                    distance[matched_row] = distance[row] + 1
                    queue.append(matched_row)
        return found

    def dfs(row: int) -> bool:
        for col in adjacency[row]:
            matched_row = col_match[col]
            if matched_row == -1 or (distance[matched_row] == distance[row] + 1 and dfs(matched_row)):
                row_match[row] = col
                col_match[col] = row
                return True
        distance[row] = -1
        return False

    matching = 0
    while bfs():
        for row in range(len(adjacency)):
            if row_match[row] == -1 and dfs(row):
                matching += 1
    return matching


def residue_histogram(coordinates: list[dict[str, Any]], s: int) -> dict[str, dict[str, int]]:
    out = {}
    quotient_length = DOMAIN_SIZE // s
    for modulus in [2, 4, 8, 16, 32]:
        if quotient_length % modulus != 0:
            continue
        counts = Counter(int(coordinate["q_index"]) % modulus for coordinate in coordinates)
        out[str(modulus)] = {str(idx): counts[idx] for idx in range(modulus)}
    return out


def support_diversity(row_supports: list[tuple[int, ...]]) -> dict[str, Any]:
    counts = Counter(row_supports)
    multiplicities = sorted(counts.values(), reverse=True)
    return {
        "row_count": len(row_supports),
        "distinct_row_supports": len(counts),
        "max_row_support_multiplicity": multiplicities[0] if multiplicities else 0,
        "top_row_support_multiplicities": multiplicities[:10],
    }


def grouped_signature(coordinates: list[dict[str, Any]]) -> tuple[int, ...]:
    return tuple(int(coordinate["active_partition_index"]) for coordinate in coordinates)


def mutate_signatures(base_signature: tuple[int, ...], random_trials: int, seed: int) -> list[tuple[str, list[int]]]:
    counts = Counter(base_signature)
    grouped = list(base_signature)
    round_robin = []
    remaining = Counter(counts)
    previous = None
    while remaining:
        candidates = sorted(remaining, key=lambda key: (-remaining[key], key))
        chosen = candidates[0]
        if chosen == previous and len(candidates) > 1:
            chosen = candidates[1]
        round_robin.append(chosen)
        previous = chosen
        remaining[chosen] -= 1
        if remaining[chosen] == 0:
            del remaining[chosen]
    out = [("grouped_baseline", grouped), ("round_robin", round_robin)]
    rng = random.Random(seed)
    seen = {tuple(sig) for _, sig in out}
    for trial in range(random_trials):
        shuffled = list(base_signature)
        rng.shuffle(shuffled)
        key = tuple(shuffled)
        if key in seen:
            continue
        seen.add(key)
        out.append((f"random_seed_{seed}_{trial}", shuffled))
    return out


def rebuild_coordinates(signature: list[int], payloads: dict[int, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    cursors = {key: 0 for key in payloads}
    out = []
    for q_index, active_index in enumerate(signature):
        source = payloads[active_index][cursors[active_index]]
        cursors[active_index] += 1
        out.append(
            {
                "q_index": q_index,
                "active_partition_index": active_index,
                "local_partition_index": cursors[active_index] - 1,
                "partition": source["partition"],
                "selected_blocks": source["selected_blocks"],
            }
        )
    return out


def partition_payloads(coordinates: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for coordinate in coordinates:
        grouped[int(coordinate["active_partition_index"])].append(coordinate)
    for values in grouped.values():
        values.sort(key=lambda item: int(item["local_partition_index"]))
    return dict(grouped)


def diagnose_coordinates(label: str, coordinates: list[dict[str, Any]], s: int) -> dict[str, Any]:
    degree_bound = PAIR_CAP // s
    variable_count = 6 * (degree_bound + 1)
    row_supports = row_supports_for_coordinates(coordinates, s)
    matching = hopcroft_karp(row_supports, variable_count)
    diversity = support_diversity(row_supports)
    return {
        "label": label,
        "s": s,
        "quotient_length": DOMAIN_SIZE // s,
        "quotient_degree_bound": degree_bound,
        "variable_count": variable_count,
        "equation_count": len(row_supports),
        "structural_rank": matching,
        "structural_nullity_upper_bound": variable_count - matching,
        "full_column_matching": matching == variable_count,
        "row_support_diversity": diversity,
        "residue_histogram": residue_histogram(coordinates, s),
    }


def diagnose_screen(screen: dict[str, Any], long_realization: Any, random_trials: int, seed: int) -> dict[str, Any]:
    s = int(screen["s"])
    base_coordinates = long_realization.expand_schedule(screen)
    payloads = partition_payloads(base_coordinates)
    signature = grouped_signature(base_coordinates)
    diagnostics = []
    for label, mutated in mutate_signatures(signature, random_trials, seed + s):
        diagnostics.append(diagnose_coordinates(label, rebuild_coordinates(mutated, payloads), s))
    best = min(
        diagnostics,
        key=lambda row: (
            row["structural_rank"],
            row["equation_count"],
            row["row_support_diversity"]["distinct_row_supports"],
            row["label"],
        ),
    )
    return {
        "s": s,
        "quotient_length": screen["quotient_length"],
        "support_vector": screen["support_vector"],
        "pair7_counts": screen["pair7_counts"],
        "max_pair_equal_h_count": screen["max_pair_equal_h_count"],
        "labellings_tested": len(diagnostics),
        "structural_positive_labellings": sum(1 for row in diagnostics if not row["full_column_matching"]),
        "best_label": best["label"],
        "best_structural_rank": best["structural_rank"],
        "best_structural_nullity_upper_bound": best["structural_nullity_upper_bound"],
        "best_equation_count": best["equation_count"],
        "best_variable_count": best["variable_count"],
        "best_full_column_matching": best["full_column_matching"],
        "best_row_support_diversity": best["row_support_diversity"],
        "diagnostics": diagnostics,
    }


def build_record(random_trials: int, seed: int) -> dict[str, Any]:
    previous = load_json(INPUT_DATA)
    long_realization = load_long_realization()
    feasible = [screen for screen in previous["screens"] if screen["feasible"]]
    results = [diagnose_screen(screen, long_realization, random_trials, seed) for screen in feasible]
    structural_positive = [row for row in results if row["structural_positive_labellings"] > 0]
    best = min(
        results,
        key=lambda row: (
            row["best_structural_rank"],
            row["best_equation_count"],
            row["s"],
        ),
    )
    proof_status = (
        "CANDIDATE / STRUCTURAL_RANK_DEFECT_TARGET / PARTIAL / EXPERIMENTAL"
        if structural_positive
        else "EXACT_EXTRACTION_NO_A327 / STRUCTURAL_RANK_FULL_COLUMN_MATCHING / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_long_cpsat_front": {
            "proof_status": previous["proof_status"],
            "screens_tested": previous["long_cpsat_front"]["screens_tested"],
            "cp_feasible_screens": previous["long_cpsat_front"]["cp_feasible_screens"],
            "best_s": previous["long_cpsat_front"]["best_s"],
            "failure_mode": previous["long_cpsat_front"]["best_failure_mode"],
        },
        "structural_rank_features": {
            "random_trials_per_screen": random_trials,
            "seed": seed,
            "screens_tested": len(results),
            "structural_positive_screens": len(structural_positive),
            "best_s": best["s"],
            "best_label": best["best_label"],
            "best_structural_rank": best["best_structural_rank"],
            "best_structural_nullity_upper_bound": best["best_structural_nullity_upper_bound"],
            "best_equation_count": best["best_equation_count"],
            "best_variable_count": best["best_variable_count"],
            "best_full_column_matching": best["best_full_column_matching"],
            "best_failure_mode": (
                "STRUCTURAL_RANK_DEFECT_TARGET"
                if structural_positive
                else "STRUCTURAL_RANK_FULL_COLUMN_MATCHING"
            ),
        },
        "screen_diagnostics": results,
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
    parser.add_argument("--random-trials", type=int, default=16)
    parser.add_argument("--seed", type=int, default=3)
    args = parser.parse_args()
    record = build_record(args.random_trials, args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps({"proof_status": record["proof_status"], **record["structural_rank_features"]}, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_STRUCTURAL_RANK_FEATURES_READY")


if __name__ == "__main__":
    main()
