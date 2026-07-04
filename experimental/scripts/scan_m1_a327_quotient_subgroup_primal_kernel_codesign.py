#!/usr/bin/env python3
"""Dependency-engineered quotient-subgroup primal-kernel codesign for M1 a=327."""

from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "563f34a"
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_primal_kernel_codesign.json")
PREVIOUS_DATA = Path("experimental/data/m1_a327_quotient_subgroup_rankaware_v2_structural_defect.json")

TRACK = "INTERLEAVED_LIST"
ROW = "RS[F_17^32,H,256]"
DENOMINATOR = "17^32"
TARGET_AGREEMENT = 327
FIELD_PRIME = 17
DOMAIN_SIZE = 512
ORDER8_BUCKET_SIZE = 64
ORDER8_LENGTH = 8
PAIR_CAP = 255
PAIR7_LOWER = 142
WITNESSES = tuple(range(1, 8))
NONBASELINE = tuple(range(1, 7))
BASELINE = 7
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup construction",
    "global obstruction outside the tested order-8 primal-kernel codesign family",
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
            "experimental/scripts/scan_m1_a327_quotient_subgroup_primal_kernel_codesign.py"
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


def root_triples() -> list[tuple[int, int, int]]:
    return list(combinations(range(ORDER8_LENGTH), 3))


def pairs() -> list[tuple[int, int]]:
    return [(left, right) for left in WITNESSES for right in WITNESSES if left < right]


def solve_root_geometry(time_limit: float) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    triples = root_triples()
    model = cp_model.CpModel()

    choose = []
    for witness in NONBASELINE:
        row = [model.NewBoolVar(f"choose_w{witness}_r{idx}") for idx, _triple in enumerate(triples)]
        model.Add(sum(row) == 1)
        choose.append(row)

    root = [
        [model.NewBoolVar(f"root_w{witness}_q{bucket}") for bucket in range(ORDER8_LENGTH)]
        for witness in NONBASELINE
    ]
    for witness_idx, _witness in enumerate(NONBASELINE):
        for bucket in range(ORDER8_LENGTH):
            model.Add(
                root[witness_idx][bucket]
                == sum(
                    choose[witness_idx][triple_idx]
                    for triple_idx, triple in enumerate(triples)
                    if bucket in triple
                )
            )

    zero_selected = [model.NewIntVar(0, ORDER8_BUCKET_SIZE, f"zero_selected_q{bucket}") for bucket in range(ORDER8_LENGTH)]
    zero_for_witness = [
        [model.NewIntVar(0, ORDER8_BUCKET_SIZE, f"zero_w{witness}_q{bucket}") for bucket in range(ORDER8_LENGTH)]
        for witness in NONBASELINE
    ]
    singleton = [
        [model.NewIntVar(0, ORDER8_BUCKET_SIZE, f"singleton_w{witness}_q{bucket}") for bucket in range(ORDER8_LENGTH)]
        for witness in NONBASELINE
    ]

    for witness_idx, _witness in enumerate(NONBASELINE):
        for bucket in range(ORDER8_LENGTH):
            model.Add(zero_for_witness[witness_idx][bucket] == zero_selected[bucket]).OnlyEnforceIf(
                root[witness_idx][bucket]
            )
            model.Add(zero_for_witness[witness_idx][bucket] == 0).OnlyEnforceIf(root[witness_idx][bucket].Not())
            model.Add(singleton[witness_idx][bucket] == 0).OnlyEnforceIf(root[witness_idx][bucket])

    for bucket in range(ORDER8_LENGTH):
        model.Add(
            zero_selected[bucket] + sum(singleton[witness_idx][bucket] for witness_idx in range(len(NONBASELINE)))
            == ORDER8_BUCKET_SIZE
        )

    model.Add(sum(zero_selected) == TARGET_AGREEMENT)
    for witness_idx, _witness in enumerate(NONBASELINE):
        model.Add(
            sum(zero_for_witness[witness_idx][bucket] + singleton[witness_idx][bucket] for bucket in range(ORDER8_LENGTH))
            == TARGET_AGREEMENT
        )
        if witness_idx < 5:
            model.Add(sum(zero_for_witness[witness_idx]) >= PAIR7_LOWER)

    selected_pair_terms: dict[tuple[int, int], list[Any]] = {}
    for left_idx, right_idx in combinations(range(len(NONBASELINE)), 2):
        terms = []
        for bucket in range(ORDER8_LENGTH):
            both_root = model.NewBoolVar(f"both_w{left_idx + 1}_{right_idx + 1}_q{bucket}")
            model.AddBoolAnd([root[left_idx][bucket], root[right_idx][bucket]]).OnlyEnforceIf(both_root)
            model.AddBoolOr([root[left_idx][bucket].Not(), root[right_idx][bucket].Not()]).OnlyEnforceIf(
                both_root.Not()
            )
            term = model.NewIntVar(0, ORDER8_BUCKET_SIZE, f"pairzero_w{left_idx + 1}_{right_idx + 1}_q{bucket}")
            model.Add(term == zero_selected[bucket]).OnlyEnforceIf(both_root)
            model.Add(term == 0).OnlyEnforceIf(both_root.Not())
            terms.append(term)
        selected_pair_terms[(left_idx + 1, right_idx + 1)] = terms
        model.Add(sum(terms) <= PAIR_CAP)

    min_pair7 = model.NewIntVar(0, TARGET_AGREEMENT, "min_pair7")
    for witness_idx in range(5):
        model.Add(min_pair7 <= sum(zero_for_witness[witness_idx]))
    max_pair = model.NewIntVar(0, PAIR_CAP, "max_pair")
    for terms in selected_pair_terms.values():
        model.Add(max_pair >= sum(terms))
    model.Maximize(1000 * min_pair7 - max_pair)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = 0
    status = solver.Solve(model)
    status_name = solver.StatusName(status)
    feasible = status in (cp_model.OPTIMAL, cp_model.FEASIBLE)
    row: dict[str, Any] = {
        "model": "root_bucket_zero_singleton",
        "ortools_version": ortools_version,
        "cp_sat_status": status_name,
        "feasible": feasible,
        "root_triples_by_witness": None,
        "zero_selected_by_bucket": None,
        "support_vector": None,
        "pair7_counts": None,
        "max_selected_pair_count": None,
        "best_failure_mode": "PRIMAL_KERNEL_ROOT_GEOMETRY_INFEASIBLE"
        if status_name in {"INFEASIBLE", "MODEL_INVALID"}
        else "PRIMAL_KERNEL_ROOT_GEOMETRY_UNRESOLVED",
    }
    if not feasible:
        return row

    chosen_triples = []
    for witness_idx in range(len(NONBASELINE)):
        chosen = next(idx for idx, variable in enumerate(choose[witness_idx]) if solver.Value(variable))
        chosen_triples.append(list(triples[chosen]))
    zero_counts = [int(solver.Value(variable)) for variable in zero_selected]
    support_vector = []
    for witness_idx in range(len(NONBASELINE)):
        support_vector.append(
            sum(
                int(solver.Value(zero_for_witness[witness_idx][bucket]))
                + int(solver.Value(singleton[witness_idx][bucket]))
                for bucket in range(ORDER8_LENGTH)
            )
        )
    support_vector.append(sum(zero_counts))
    pair7_counts = [
        sum(int(solver.Value(zero_for_witness[witness_idx][bucket])) for bucket in range(ORDER8_LENGTH))
        for witness_idx in range(5)
    ]
    selected_pair_counts = {
        f"{left}{right}": sum(int(solver.Value(term)) for term in terms)
        for (left, right), terms in selected_pair_terms.items()
    }
    row.update(
        {
            "root_triples_by_witness": chosen_triples,
            "zero_selected_by_bucket": zero_counts,
            "support_vector": support_vector,
            "pair7_counts": pair7_counts,
            "selected_pair_counts": selected_pair_counts,
            "max_selected_pair_count": max(selected_pair_counts.values()) if selected_pair_counts else 0,
            "best_failure_mode": "PRIMAL_KERNEL_ROOT_GEOMETRY_FEASIBLE",
        }
    )
    return row


def locator_values(root_indices: list[int], scalar: int, domain: list[int]) -> list[int]:
    roots = [domain[idx] for idx in root_indices]
    values = []
    for value in domain:
        out = scalar % FIELD_PRIME
        for root in roots:
            out = (out * ((value - root) % FIELD_PRIME)) % FIELD_PRIME
        values.append(out)
    return values


def value_partitions(values_by_witness: list[list[int]]) -> list[list[list[int]]]:
    partitions = []
    for bucket in range(ORDER8_LENGTH):
        classes: dict[int, list[int]] = {0: [BASELINE]}
        for witness_idx, values in enumerate(values_by_witness, start=1):
            classes.setdefault(values[bucket], []).append(witness_idx)
        partition = sorted((sorted(block) for block in classes.values()), key=lambda block: (block[0], len(block), block))
        partitions.append(partition)
    return partitions


def solve_selected_allocation(partitions: list[list[list[int]]], time_limit: float) -> dict[str, Any]:
    cp_model, ortools_version = require_ortools()
    model = cp_model.CpModel()
    selected = []
    for bucket, partition in enumerate(partitions):
        row = []
        for block_idx, _block in enumerate(partition):
            row.append(model.NewIntVar(0, ORDER8_BUCKET_SIZE, f"selected_q{bucket}_b{block_idx}"))
        model.Add(sum(row) == ORDER8_BUCKET_SIZE)
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

    pair_counts = {}
    for left, right in pairs():
        count = model.NewIntVar(0, DOMAIN_SIZE, f"pair_{left}_{right}")
        model.Add(
            count
            == sum(
                selected[bucket][block_idx]
                for bucket, partition in enumerate(partitions)
                for block_idx, block in enumerate(partition)
                if left in block and right in block
            )
        )
        model.Add(count <= PAIR_CAP)
        if right == BASELINE and left <= 5:
            model.Add(count >= PAIR7_LOWER)
        pair_counts[(left, right)] = count

    min_pair7 = model.NewIntVar(0, DOMAIN_SIZE, "min_pair7")
    for witness in range(1, 6):
        model.Add(min_pair7 <= pair_counts[(witness, BASELINE)])
    max_pair = model.NewIntVar(0, PAIR_CAP, "max_pair")
    for variable in pair_counts.values():
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
        "selected_block_counts_by_bucket": None,
        "best_failure_mode": "PRIMAL_KERNEL_SELECTED_ALLOCATION_INFEASIBLE"
        if status_name in {"INFEASIBLE", "MODEL_INVALID"}
        else "PRIMAL_KERNEL_SELECTED_ALLOCATION_UNRESOLVED",
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
        f"{left}{right}": int(solver.Value(variable)) for (left, right), variable in pair_counts.items()
    }
    row.update(
        {
            "support_vector": support_vector,
            "pair7_counts": [selected_pair_counts[f"{idx}7"] for idx in range(1, 6)],
            "selected_pair_counts": selected_pair_counts,
            "selected_block_counts_by_bucket": [
                [
                    {"block": partition[block_idx], "count": int(solver.Value(selected[bucket][block_idx]))}
                    for block_idx in range(len(partition))
                    if int(solver.Value(selected[bucket][block_idx])) > 0
                ]
                for bucket, partition in enumerate(partitions)
            ],
            "best_failure_mode": "PRIMAL_KERNEL_SELECTED_ALLOCATION_FEASIBLE",
        }
    )
    return row


def ambient_pair_counts(partitions: list[list[list[int]]]) -> dict[str, int]:
    out = {}
    for left, right in pairs():
        buckets = sum(any(left in block and right in block for block in partition) for partition in partitions)
        out[f"{left}{right}"] = buckets * ORDER8_BUCKET_SIZE
    return out


def locator_attempt(
    label: str,
    roots_by_witness: list[list[int]],
    scalars: list[int],
    domain: list[int],
    time_limit: float,
) -> dict[str, Any]:
    values = [
        locator_values(root_indices, scalar, domain)
        for root_indices, scalar in zip(roots_by_witness, scalars, strict=True)
    ]
    distinct_values = len({tuple(row) for row in values} | {tuple([0] * ORDER8_LENGTH)}) == 7
    partitions = value_partitions(values)
    ambient_pairs = ambient_pair_counts(partitions)
    partition_histogram = Counter(tuple(sorted(len(block) for block in partition)) for partition in partitions)
    allocation = solve_selected_allocation(partitions, time_limit)
    return {
        "label": label,
        "root_triples_by_witness": roots_by_witness,
        "scalars": scalars,
        "distinct_quotient_codewords": distinct_values,
        "degree_in_X": 192,
        "ambient_pair_counts": ambient_pairs,
        "max_ambient_pair_count": max(ambient_pairs.values()),
        "partition_size_histogram": {"|".join(map(str, key)): value for key, value in partition_histogram.items()},
        "partitions_by_bucket": partitions,
        "allocation": allocation,
        "best_failure_mode": (
            "PRIMAL_KERNEL_LOCATOR_EXACT_CANDIDATE"
            if distinct_values and allocation["feasible"] and max(ambient_pairs.values()) <= PAIR_CAP
            else allocation["best_failure_mode"]
        ),
    }


def instantiate_locator_candidate(
    root_geometry: dict[str, Any],
    allocation_time_limit: float,
    random_trials: int,
    seed: int,
) -> dict[str, Any]:
    domain = order8_domain()
    attempts = []
    if root_geometry["feasible"]:
        roots_by_witness = root_geometry["root_triples_by_witness"]
        for label, scalars in [
            ("root_geometry_scalars_1_2_3_4_5_6", [1, 2, 3, 4, 5, 6]),
            ("root_geometry_scalars_all_1", [1, 1, 1, 1, 1, 1]),
            ("root_geometry_scalars_odd", [1, 3, 5, 7, 9, 11]),
        ]:
            attempts.append(locator_attempt(label, roots_by_witness, scalars, domain, allocation_time_limit))

    rng = random.Random(seed)
    triples = [list(triple) for triple in root_triples()]
    seen = {
        (
            tuple(tuple(root) for root in attempt["root_triples_by_witness"]),
            tuple(attempt["scalars"]),
        )
        for attempt in attempts
    }
    for trial in range(random_trials):
        roots_by_witness = [rng.choice(triples) for _ in NONBASELINE]
        scalars = [rng.randrange(1, FIELD_PRIME) for _ in NONBASELINE]
        key = (tuple(tuple(root) for root in roots_by_witness), tuple(scalars))
        if key in seen:
            continue
        seen.add(key)
        attempts.append(
            locator_attempt(f"random_locator_seed_{seed}_{trial}", roots_by_witness, scalars, domain, allocation_time_limit)
        )

    if not attempts:
        return {
            "attempted": False,
            "random_trials": random_trials,
            "best_failure_mode": "PRIMAL_KERNEL_LOCATOR_NOT_ATTEMPTED",
        }
    best = min(
        attempts,
        key=lambda row: (
            row["best_failure_mode"] != "PRIMAL_KERNEL_LOCATOR_EXACT_CANDIDATE",
            -int(row["allocation"]["feasible"]),
            row["max_ambient_pair_count"],
            row["scalars"],
        ),
    )
    def compact_attempt(attempt: dict[str, Any]) -> dict[str, Any]:
        allocation = attempt["allocation"]
        return {
            "label": attempt["label"],
            "root_triples_by_witness": attempt["root_triples_by_witness"],
            "scalars": attempt["scalars"],
            "distinct_quotient_codewords": attempt["distinct_quotient_codewords"],
            "degree_in_X": attempt["degree_in_X"],
            "max_ambient_pair_count": attempt["max_ambient_pair_count"],
            "partition_size_histogram": attempt["partition_size_histogram"],
            "allocation_status": allocation["cp_sat_status"],
            "allocation_feasible": allocation["feasible"],
            "allocation_support_vector": allocation["support_vector"],
            "allocation_pair7_counts": allocation["pair7_counts"],
            "best_failure_mode": attempt["best_failure_mode"],
        }

    sample = [compact_attempt(attempt) for attempt in attempts[:25]]
    if best not in attempts[:25]:
        sample.append(compact_attempt(best))
    return {
        "attempted": True,
        "field": "GF(17)",
        "order8_domain": domain,
        "polynomial_family": "g_i(X)=c_i*prod_{r in R_i}(X^64-r)",
        "random_trials": random_trials,
        "allocation_attempts": len(attempts),
        "feasible_allocations": sum(1 for attempt in attempts if attempt["allocation"]["feasible"]),
        "attempt_sample_limit": 25,
        "attempt_sample": sample,
        "best_scalars": best["scalars"],
        "best_failure_mode": best["best_failure_mode"],
        "candidate_constructed": best["best_failure_mode"] == "PRIMAL_KERNEL_LOCATOR_EXACT_CANDIDATE",
        "best": compact_attempt(best),
    }


def build_record(root_time_limit: float, allocation_time_limit: float, locator_trials: int, seed: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    root_geometry = solve_root_geometry(root_time_limit)
    locator = instantiate_locator_candidate(root_geometry, allocation_time_limit, locator_trials, seed)
    candidate_constructed = bool(locator.get("candidate_constructed"))
    if candidate_constructed:
        proof_status = "CANDIDATE / PRIMAL_KERNEL_LOCATOR_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        best_failure = "PRIMAL_KERNEL_LOCATOR_EXACT_CANDIDATE"
    else:
        proof_status = "EXACT_EXTRACTION_NO_A327 / PRIMAL_KERNEL_CODESIGN_NO_ALLOCATION / PARTIAL / EXPERIMENTAL"
        best_failure = locator.get("best_failure_mode", root_geometry["best_failure_mode"])
    return {
        "track": TRACK,
        "row": ROW,
        "denominator": DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_rankaware_v2": {
            "proof_status": previous["proof_status"],
            "models_tested": previous["rankaware_v2"]["models_tested"],
            "structural_defect_targets_found": previous["rankaware_v2"]["structural_defect_targets_found"],
            "best_proxy_rank": previous["rankaware_v2"]["best_proxy_rank"],
            "best_proxy_nullity": previous["rankaware_v2"]["best_proxy_nullity"],
            "failure_mode": previous["rankaware_v2"]["best_failure_mode"],
        },
        "primal_kernel_codesign": {
            "root_time_limit_seconds": root_time_limit,
            "allocation_time_limit_seconds": allocation_time_limit,
            "locator_random_trials": locator_trials,
            "seed": seed,
            "order8_bucket_size": ORDER8_BUCKET_SIZE,
            "degree_in_X": 192,
            "root_geometry_feasible": root_geometry["feasible"],
            "locator_allocation_attempts": locator.get("allocation_attempts", 0),
            "locator_feasible_allocations": locator.get("feasible_allocations", 0),
            "locator_candidate_constructed": candidate_constructed,
            "best_failure_mode": best_failure,
        },
        "root_geometry": root_geometry,
        "locator_codesign": locator,
        "candidate": {
            "constructed": candidate_constructed,
            "seven_distinct": None if not candidate_constructed else locator["best"]["distinct_quotient_codewords"],
            "agreement_vector": None
            if not candidate_constructed
            else locator["best"]["allocation_support_vector"],
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
    parser.add_argument("--time-limit", type=float, default=20.0)
    parser.add_argument("--allocation-time-limit", type=float, default=0.1)
    parser.add_argument("--locator-trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    record = build_record(args.time_limit, args.allocation_time_limit, args.locator_trials, args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        **record["primal_kernel_codesign"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_PRIMAL_KERNEL_CODESIGN_READY")


if __name__ == "__main__":
    main()
