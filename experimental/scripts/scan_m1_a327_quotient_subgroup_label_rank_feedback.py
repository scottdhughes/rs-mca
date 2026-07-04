#!/usr/bin/env python3
"""Rank-feedback labelling search for the M1 a=327 s=4 quotient schedule."""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np


SOURCE_COMMIT = "7e21f1d"
INPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_realization_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_quotient_subgroup_label_rank_feedback.json")
REALIZATION_SCAN = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_realization_search.py")

TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PROXY_PRIME = 257
QUOTIENT_LENGTH = 128
REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track quotient-subgroup proxy",
    "global obstruction outside the tested quotient-coordinate labellings",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def load_realization_scan() -> Any:
    spec = importlib.util.spec_from_file_location("quotient_realization_scan", REALIZATION_SCAN)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load realization scan module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def numpy_rank_mod(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    rows = np.array(matrix, dtype=np.int64) % prime
    rank = 0
    row_count, column_count = rows.shape
    for column in range(column_count):
        pivots = np.nonzero(rows[rank:, column] % prime)[0]
        if pivots.size == 0:
            continue
        pivot = rank + int(pivots[0])
        if pivot != rank:
            rows[[rank, pivot]] = rows[[pivot, rank]]
        inverse = pow(int(rows[rank, column]), -1, prime)
        rows[rank, :] = (rows[rank, :] * inverse) % prime
        factors = rows[:, column].copy() % prime
        mask = factors != 0
        mask[rank] = False
        if mask.any():
            rows[mask, :] = (rows[mask, :] - factors[mask, None] * rows[rank, :]) % prime
        rank += 1
        if rank == row_count:
            break
    return rank


def signature_for_coordinates(coordinates: list[dict[str, Any]]) -> tuple[int, ...]:
    return tuple(int(coordinate["active_partition_index"]) for coordinate in coordinates)


def partition_payloads(coordinates: list[dict[str, Any]]) -> dict[int, list[dict[str, Any]]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for coordinate in coordinates:
        grouped[int(coordinate["active_partition_index"])].append(coordinate)
    for values in grouped.values():
        values.sort(key=lambda item: int(item["local_partition_index"]))
    return dict(grouped)


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
    for active_index, values in payloads.items():
        if cursors[active_index] != len(values):
            raise ValueError(f"unused payloads for partition {active_index}")
    return out


def round_robin_signature(counts: Counter[int]) -> list[int]:
    remaining = Counter(counts)
    out: list[int] = []
    previous: int | None = None
    while remaining:
        candidates = sorted(remaining, key=lambda key: (-remaining[key], key))
        chosen = candidates[0]
        if chosen == previous and len(candidates) > 1:
            chosen = candidates[1]
        out.append(chosen)
        previous = chosen
        remaining[chosen] -= 1
        if remaining[chosen] == 0:
            del remaining[chosen]
    return out


def residue_spread_signature(counts: Counter[int], stride: int) -> list[int]:
    multiset = []
    for key, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        multiset.extend([key] * count)
    out: list[int | None] = [None] * len(multiset)
    position = 0
    for value in multiset:
        while out[position] is not None:
            position = (position + 1) % len(out)
        out[position] = value
        position = (position + stride) % len(out)
    return [int(value) for value in out]


def candidate_signatures(base_signature: tuple[int, ...], random_trials: int, seed: int) -> list[tuple[str, list[int]]]:
    counts = Counter(base_signature)
    out: list[tuple[str, list[int]]] = [
        ("grouped_baseline", list(base_signature)),
        ("round_robin", round_robin_signature(counts)),
    ]
    for stride in [3, 5, 7, 11, 17, 31]:
        out.append((f"residue_spread_stride_{stride}", residue_spread_signature(counts, stride)))
    rng = random.Random(seed)
    base_values = list(base_signature)
    seen = {tuple(values) for _, values in out}
    for trial in range(random_trials):
        shuffled = base_values[:]
        rng.shuffle(shuffled)
        key = tuple(shuffled)
        if key in seen:
            continue
        seen.add(key)
        out.append((f"random_seed_{seed}_{trial}", shuffled))
    return out


def proxy_for_coordinates(scan: Any, coordinates: list[dict[str, Any]]) -> dict[str, Any]:
    rows, row_counts = scan.build_proxy_rows(coordinates, PROXY_PRIME)
    rank = numpy_rank_mod(rows, PROXY_PRIME)
    nullity = scan.QUOTIENT_VARIABLES - rank
    return {
        "proxy_field": f"GF({PROXY_PRIME})",
        "matrix_shape": [len(rows), scan.QUOTIENT_VARIABLES],
        "row_counts": row_counts,
        "rank": rank,
        "nullity": nullity,
        "best_failure_mode": (
            "QUOTIENT_LABEL_RANK_PROXY_POSITIVE" if nullity > 0 else "QUOTIENT_LABEL_RANK_PROXY_FULL_RANK"
        ),
    }


def build_record(random_trials: int, seed: int) -> dict[str, Any]:
    scan = load_realization_scan()
    previous = load_json(INPUT_DATA)
    base_coordinates = previous["schedule"]["coordinates"]
    payloads = partition_payloads(base_coordinates)
    base_signature = signature_for_coordinates(base_coordinates)
    tested = []
    best: dict[str, Any] | None = None
    for label, signature in candidate_signatures(base_signature, random_trials, seed):
        coordinates = rebuild_coordinates(signature, payloads)
        counts = scan.schedule_counts(coordinates)
        proxy = proxy_for_coordinates(scan, coordinates)
        row = {
            "label": label,
            "signature_prefix": signature[:32],
            "support_vector": counts["support_vector"],
            "pair7_counts": counts["pair7_counts"],
            "max_pair_equal_h_count": counts["max_pair_equal_h_count"],
            "proxy_rank": proxy["rank"],
            "proxy_nullity": proxy["nullity"],
            "matrix_shape": proxy["matrix_shape"],
            "best_failure_mode": proxy["best_failure_mode"],
        }
        tested.append(row)
        if best is None or (row["proxy_rank"], -row["proxy_nullity"], label) < (
            best["proxy_rank"],
            -best["proxy_nullity"],
            best["label"],
        ):
            best = row
    assert best is not None
    positive = [row for row in tested if row["proxy_nullity"] > 0]
    proof_status = (
        "CANDIDATE / QUOTIENT_LABEL_RANK_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if positive
        else "EXACT_EXTRACTION_NO_A327 / QUOTIENT_LABEL_RANK_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_quotient_subgroup_realization_search": {
            "proof_status": previous["proof_status"],
            "proxy_matrix_shape": previous["proxy_realization"]["matrix_shape"],
            "proxy_rank": previous["proxy_realization"]["rank"],
            "proxy_nullity": previous["proxy_realization"]["nullity"],
            "failure_mode": previous["proxy_realization"]["best_failure_mode"],
        },
        "label_rank_feedback": {
            "random_trials_requested": random_trials,
            "seed": seed,
            "labellings_tested": len(tested),
            "proxy_positive_labellings": len(positive),
            "best_label": best["label"],
            "best_proxy_rank": best["proxy_rank"],
            "best_proxy_nullity": best["proxy_nullity"],
            "best_matrix_shape": best["matrix_shape"],
            "best_support_vector": best["support_vector"],
            "best_pair7_counts": best["pair7_counts"],
            "best_max_pair_equal_h_count": best["max_pair_equal_h_count"],
            "best_failure_mode": best["best_failure_mode"],
        },
        "tested_labellings": tested,
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
    parser.add_argument("--random-trials", type=int, default=64)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    record = build_record(args.random_trials, args.seed)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps({"proof_status": record["proof_status"], **record["label_rank_feedback"]}, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_QUOTIENT_SUBGROUP_LABEL_RANK_FEEDBACK_READY")


if __name__ == "__main__":
    main()
