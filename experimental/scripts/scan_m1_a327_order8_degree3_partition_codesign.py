#!/usr/bin/env python3
"""Order-8 degree-3 partition-first primal-kernel codesign for M1 a=327."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "4e6fb16"
PREVIOUS_DATA = Path("experimental/data/m1_a327_quotient_subgroup_primal_kernel_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_order8_degree3_partition_codesign.json")

TRACK = "INTERLEAVED_LIST"
ROW = "RS[F_17^32,H,256]"
DENOMINATOR = "17^32"
TARGET_AGREEMENT = 327
FIELD_PRIME = 17
DOMAIN_SIZE = 512
ORDER8_LENGTH = 8
BUCKET_SIZE = 64
PAIR_CAP = 255
PAIR7_LOWER = 142
WITNESSES = tuple(range(1, 8))
BASELINE = 7
NONBASELINE = tuple(range(1, 7))
GUARDED_TO_7 = tuple(range(1, 6))
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track order-8 quotient construction",
    "global obstruction outside the tested order-8 degree-3 partition codesign family",
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
            "experimental/scripts/scan_m1_a327_order8_degree3_partition_codesign.py"
        ) from exc


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def order_mod(value: int, prime: int) -> int:
    current = value % prime
    order = 1
    while current != 1:
        current = (current * value) % prime
        order += 1
    return order


def order8_domain() -> list[int]:
    generator = next(value for value in range(2, FIELD_PRIME) if order_mod(value, FIELD_PRIME) == ORDER8_LENGTH)
    return [pow(generator, idx, FIELD_PRIME) for idx in range(ORDER8_LENGTH)]


def eval_coefficients(coefficients: tuple[int, int, int, int], domain: list[int]) -> tuple[int, ...]:
    values = []
    for point in domain:
        powers = [1, point, (point * point) % FIELD_PRIME, (point * point * point) % FIELD_PRIME]
        values.append(sum(coeff * power for coeff, power in zip(coefficients, powers, strict=True)) % FIELD_PRIME)
    return tuple(values)


def all_degree3_words(domain: list[int]) -> list[dict[str, Any]]:
    out = []
    for coefficients in product(range(FIELD_PRIME), repeat=4):
        values = eval_coefficients(coefficients, domain)
        zero_count = sum(1 for value in values if value == 0)
        degree = 0
        for idx, coeff in enumerate(coefficients):
            if coeff % FIELD_PRIME:
                degree = idx
        out.append(
            {
                "coefficients": list(coefficients),
                "values": values,
                "zero_count": zero_count,
                "degree": degree,
                "nonzero": any(coefficients),
            }
        )
    return out


def locator_words(words: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [word for word in words if word["nonzero"] and word["zero_count"] == 3]


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def partitions_from_values(values_by_witness: list[tuple[int, ...]]) -> list[list[list[int]]]:
    partitions = []
    for bucket in range(ORDER8_LENGTH):
        classes: dict[int, list[int]] = {0: [BASELINE]}
        for witness, values in enumerate(values_by_witness, start=1):
            classes.setdefault(int(values[bucket]), []).append(witness)
        partitions.append(
            sorted((sorted(block) for block in classes.values()), key=lambda block: (block[0], len(block), block))
        )
    return partitions


def ambient_pair_counts(partitions: list[list[list[int]]]) -> dict[str, int]:
    out = {}
    for left, right in pairs():
        buckets = sum(any(left in block and right in block for block in partition) for partition in partitions)
        out[f"{left}{right}"] = buckets * BUCKET_SIZE
    return out


def solve_selected_allocation(partitions: list[list[list[int]]], time_limit: float) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    model = cp_model.CpModel()
    selected = []
    for bucket, partition in enumerate(partitions):
        row = []
        for block_idx, _block in enumerate(partition):
            row.append(model.NewIntVar(0, BUCKET_SIZE, f"selected_q{bucket}_b{block_idx}"))
        model.Add(sum(row) == BUCKET_SIZE)
        selected.append(row)

    for witness in WITNESSES:
        model.Add(
            sum(
                selected[bucket][block_idx]
                for bucket, partition in enumerate(partitions)
                for block_idx, block in enumerate(partition)
                if witness in block
            )
            == TARGET_AGREEMENT
        )

    pair_count_vars = {}
    for left, right in pairs():
        variable = model.NewIntVar(0, DOMAIN_SIZE, f"pair_{left}_{right}")
        model.Add(
            variable
            == sum(
                selected[bucket][block_idx]
                for bucket, partition in enumerate(partitions)
                for block_idx, block in enumerate(partition)
                if left in block and right in block
            )
        )
        model.Add(variable <= PAIR_CAP)
        if right == BASELINE and left in GUARDED_TO_7:
            model.Add(variable >= PAIR7_LOWER)
        pair_count_vars[(left, right)] = variable

    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for witness in GUARDED_TO_7:
        model.Add(min_pair7 <= pair_count_vars[(witness, BASELINE)])
    max_pair = model.NewIntVar(0, PAIR_CAP, "max_pair")
    for variable in pair_count_vars.values():
        model.Add(max_pair >= variable)
    model.Maximize(1000 * min_pair7 - max_pair)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 0
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "ortools_version": ortools_version,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "support_vector": None,
        "pair7_counts": None,
        "selected_pair_counts": None,
        "best_failure_mode": "ORDER8_PARTITION_ALLOCATION_INFEASIBLE"
        if status_name in {"INFEASIBLE", "MODEL_INVALID"}
        else "ORDER8_PARTITION_ALLOCATION_UNRESOLVED",
    }
    if not feasible:
        return row
    support_vector = []
    for witness in WITNESSES:
        support_vector.append(
            sum(
                int(solver.Value(selected[bucket][block_idx]))
                for bucket, partition in enumerate(partitions)
                for block_idx, block in enumerate(partition)
                if witness in block
            )
        )
    selected_pair_counts = {
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in pair_count_vars.items()
    }
    row.update(
        {
            "support_vector": support_vector,
            "pair7_counts": [selected_pair_counts[f"{idx}7"] for idx in GUARDED_TO_7],
            "selected_pair_counts": selected_pair_counts,
            "best_failure_mode": "ORDER8_PARTITION_ALLOCATION_FEASIBLE",
        }
    )
    return row


def partition_score(partitions: list[list[list[int]]], ambient_pairs: dict[str, int]) -> tuple[int, int, int, int]:
    large_block_score = sum(max(len(block) for block in partition) for partition in partitions)
    pair7_buckets = sum(ambient_pairs[f"{idx}7"] // BUCKET_SIZE for idx in GUARDED_TO_7)
    split_blocks = sum(sum(1 for block in partition if len(block) >= 3) for partition in partitions)
    max_pair = max(ambient_pairs.values())
    return (pair7_buckets, large_block_score, split_blocks, -max_pair)


def compact_candidate(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "label": row["label"],
        "family": row["family"],
        "coefficients_by_witness": row["coefficients_by_witness"],
        "zero_counts_by_witness": row["zero_counts_by_witness"],
        "distinct_quotient_codewords": row["distinct_quotient_codewords"],
        "max_ambient_pair_count": row["max_ambient_pair_count"],
        "partition_size_histogram": row["partition_size_histogram"],
        "allocation_status": row["allocation"]["cp_sat_status"],
        "allocation_feasible": row["allocation"]["feasible"],
        "allocation_support_vector": row["allocation"]["support_vector"],
        "allocation_pair7_counts": row["allocation"]["pair7_counts"],
        "best_failure_mode": row["best_failure_mode"],
    }


def evaluate_candidate(
    label: str,
    family: str,
    chosen_words: list[dict[str, Any]],
    allocation_time_limit: float,
) -> dict[str, Any]:
    values = [word["values"] for word in chosen_words]
    partitions = partitions_from_values(values)
    ambient_pairs = ambient_pair_counts(partitions)
    partition_histogram = Counter(tuple(sorted(len(block) for block in partition)) for partition in partitions)
    distinct = len({tuple(word["values"]) for word in chosen_words} | {tuple([0] * ORDER8_LENGTH)}) == 7
    max_ambient_pair = max(ambient_pairs.values())
    if not distinct:
        allocation = {
            "cp_sat_status": "NOT_RUN",
            "feasible": False,
            "support_vector": None,
            "pair7_counts": None,
            "selected_pair_counts": None,
            "best_failure_mode": "ORDER8_DEGREE3_DUPLICATE_CODEWORD",
        }
    elif max_ambient_pair > PAIR_CAP:
        allocation = {
            "cp_sat_status": "NOT_RUN",
            "feasible": False,
            "support_vector": None,
            "pair7_counts": None,
            "selected_pair_counts": None,
            "best_failure_mode": "ORDER8_DEGREE3_AMBIENT_PAIR_CAP_FAIL",
        }
    else:
        allocation = solve_selected_allocation(partitions, allocation_time_limit)
    exact_candidate = distinct and allocation["feasible"] and max(ambient_pairs.values()) <= PAIR_CAP
    return {
        "label": label,
        "family": family,
        "coefficients_by_witness": [word["coefficients"] for word in chosen_words],
        "zero_counts_by_witness": [word["zero_count"] for word in chosen_words],
        "distinct_quotient_codewords": distinct,
        "max_ambient_pair_count": max_ambient_pair,
        "ambient_pair_counts": ambient_pairs,
        "partition_size_histogram": {"|".join(map(str, key)): value for key, value in partition_histogram.items()},
        "score": list(partition_score(partitions, ambient_pairs)),
        "allocation": allocation,
        "best_failure_mode": "ORDER8_DEGREE3_EXACT_CANDIDATE"
        if exact_candidate
        else allocation["best_failure_mode"],
    }


def seeded_candidates(words: list[dict[str, Any]], rng: random.Random, trials: int) -> list[tuple[str, str, list[dict[str, Any]]]]:
    locators = locator_words(words)
    arbitrary = [word for word in words if word["nonzero"]]
    candidates = []

    # Deterministic seed: rotate through low-index locators and simple constants for witness 6.
    for offset in range(8):
        chosen = [locators[(offset + 7 * idx) % len(locators)] for idx in range(5)]
        chosen.append(arbitrary[(offset + 1) % len(arbitrary)])
        candidates.append((f"deterministic_locator5_general6_{offset}", "locator5_general6", chosen))

    for trial in range(trials):
        chosen = [rng.choice(locators) for _ in range(5)]
        chosen.append(rng.choice(arbitrary))
        candidates.append((f"random_locator5_general6_{trial}", "locator5_general6", chosen))

    return candidates


def build_record(candidate_trials: int, allocation_time_limit: float, seed: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    domain = order8_domain()
    words = all_degree3_words(domain)
    rng = random.Random(seed)
    attempts = []
    feasible = []
    for label, family, chosen_words in seeded_candidates(words, rng, candidate_trials):
        row = evaluate_candidate(label, family, chosen_words, allocation_time_limit)
        attempts.append(row)
        if row["best_failure_mode"] == "ORDER8_DEGREE3_EXACT_CANDIDATE":
            feasible.append(row)

    best = min(
        attempts,
        key=lambda row: (
            row["best_failure_mode"] != "ORDER8_DEGREE3_EXACT_CANDIDATE",
            -int(row["allocation"]["feasible"]),
            not row["distinct_quotient_codewords"],
            row["max_ambient_pair_count"] > PAIR_CAP,
            -row["score"][0],
            -row["score"][1],
            row["max_ambient_pair_count"],
            row["label"],
        ),
    )
    proof_status = (
        "CANDIDATE / ORDER8_DEGREE3_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        if feasible
        else "EXACT_EXTRACTION_NO_A327 / ORDER8_DEGREE3_NO_ALLOCATION / PARTIAL / EXPERIMENTAL"
    )
    sample = [compact_candidate(row) for row in attempts[:25]]
    if best not in attempts[:25]:
        sample.append(compact_candidate(best))
    return {
        "track": TRACK,
        "row": ROW,
        "denominator": DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_primal_kernel_codesign": {
            "proof_status": previous["proof_status"],
            "locator_allocation_attempts": previous["primal_kernel_codesign"]["locator_allocation_attempts"],
            "locator_feasible_allocations": previous["primal_kernel_codesign"]["locator_feasible_allocations"],
            "failure_mode": previous["primal_kernel_codesign"]["best_failure_mode"],
        },
        "order8_degree3_codesign": {
            "field": "GF(17)",
            "order8_domain": domain,
            "degree_in_X": 192,
            "candidate_trials": candidate_trials,
            "allocation_time_limit_seconds": allocation_time_limit,
            "seed": seed,
            "candidates_tested": len(attempts),
            "feasible_allocations": sum(1 for row in attempts if row["allocation"]["feasible"]),
            "exact_candidates": len(feasible),
            "best_failure_mode": best["best_failure_mode"],
            "best_label": best["label"],
            "best_score": best["score"],
            "best_max_ambient_pair_count": best["max_ambient_pair_count"],
        },
        "attempt_sample_limit": 25,
        "attempt_sample": sample,
        "best_candidate": compact_candidate(best),
        "candidate": {
            "constructed": bool(feasible),
            "seven_distinct": None if not feasible else feasible[0]["distinct_quotient_codewords"],
            "agreement_vector": None if not feasible else feasible[0]["allocation"]["support_vector"],
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
    parser.add_argument("--candidate-trials", type=int, default=2000)
    parser.add_argument("--allocation-time-limit", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    record = build_record(args.candidate_trials, args.allocation_time_limit, args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        **record["order8_degree3_codesign"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_ORDER8_DEGREE3_PARTITION_CODESIGN_READY")


if __name__ == "__main__":
    main()
