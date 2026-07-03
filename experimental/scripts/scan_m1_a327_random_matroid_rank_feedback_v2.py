#!/usr/bin/env python3
"""Rank-feedback search around the random-matroid M1 a=327 functional lift."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np


SOURCE_COMMIT = "3d6bfd4"
SOURCE_DATA = Path("experimental/data/m1_a327_random_matroid_functional_lift.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v2.json")

ROOT = Path(__file__).resolve().parents[2]
LOWRANK_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_lowrank_template_selected_class_search.py"
FUNCTIONAL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_random_matroid_functional_lift.py"

TARGET_AGREEMENT = 327
PAIR7_LOWER = 142
PROXY_PRIME = 12289
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lowrank = load_module("lowrank_selected_class", LOWRANK_SCRIPT)
functional = load_module("random_matroid_functional", FUNCTIONAL_SCRIPT)


def fast_rank_mod_prime_matrix(matrix: list[list[int]], ncols: int, prime: int) -> int:
    rows = [row for row in matrix if any(value % prime for value in row)]
    if not rows:
        return 0
    array = np.asarray(rows, dtype=np.int64) % prime
    rank = 0
    nrows = array.shape[0]
    for col in range(ncols):
        candidates = np.flatnonzero(array[rank:, col] % prime)
        if candidates.size == 0:
            continue
        pivot = rank + int(candidates[0])
        if pivot != rank:
            array[[rank, pivot]] = array[[pivot, rank]]
        inv = pow(int(array[rank, col]), -1, prime)
        array[rank, :] = (array[rank, :] * inv) % prime
        if rank + 1 < nrows:
            lower = array[rank + 1 :, col] % prime
            nonzero = np.flatnonzero(lower)
            if nonzero.size:
                rows_to_clear = rank + 1 + nonzero
                factors = array[rows_to_clear, col].copy() % prime
                array[rows_to_clear, :] = (
                    array[rows_to_clear, :] - factors[:, None] * array[rank, :]
                ) % prime
        rank += 1
        if rank == nrows or rank == ncols:
            break
    return int(rank)


functional.rank_mod_prime_matrix = fast_rank_mod_prime_matrix


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize_vectors(vectors: list[list[int]]) -> list[list[int]]:
    return [[int(value) % 17 for value in row] for row in vectors]


def mutate_vectors(base_vectors: list[list[int]], seed: int, weight: int) -> list[list[int]]:
    rng = random.Random(seed)
    out = normalize_vectors(base_vectors)
    for row_idx in range(len(out)):
        for _ in range(weight):
            col = rng.randrange(TEMPLATE_DIM)
            out[row_idx][col] = (out[row_idx][col] + rng.randrange(1, 17)) % 17
    return out


def candidate_specs(base_vectors: list[list[int]]) -> list[dict[str, Any]]:
    specs = [
        {
            "template_id": "random_matroid_seeded_0_m6",
            "template_family": "random_matroid_rank_feedback",
            "vectors": normalize_vectors(base_vectors),
            "selected_class_sizes": [3, 4, 5],
            "cost_weight": 5.0,
            "pair7_weight": 1.0,
            "assignment_strategies": ["sorted_block", "fiber_round_robin"],
        }
    ]
    for idx, seed in enumerate([11, 17, 23, 29, 37, 43], start=1):
        specs.append(
            {
                "template_id": f"random_matroid_feedback_seed_{idx}_m6",
                "template_family": "random_matroid_rank_feedback",
                "vectors": mutate_vectors(base_vectors, seed=seed, weight=2 if idx <= 3 else 3),
                "selected_class_sizes": [3, 4, 5],
                "cost_weight": 5.0,
                "pair7_weight": 1.0,
                "assignment_strategies": ["sorted_block", "fiber_round_robin"],
            }
        )
    return specs


def annihilator_pair_ranks(template_vectors: list[list[int]], annihilator_basis: list[list[int]]) -> dict[str, Any]:
    ranks = {}
    forced_pairs = []
    if not annihilator_basis:
        return {
            "annihilator_pair_rank_by_pair": {f"P{i}{j}": None for i in range(1, 8) for j in range(i + 1, 8)},
            "annihilator_forced_equal_pairs": [],
            "annihilator_diagonal": False,
        }
    for left in range(1, 8):
        for right in range(left + 1, 8):
            diff = [
                (int(template_vectors[left - 1][idx]) - int(template_vectors[right - 1][idx])) % 17
                for idx in range(TEMPLATE_DIM)
            ]
            values = [
                sum(diff[idx] * basis_vec[idx] for idx in range(TEMPLATE_DIM)) % 17
                for basis_vec in annihilator_basis
            ]
            rank = 1 if any(values) else 0
            label = f"P{left}{right}"
            ranks[label] = rank
            if rank == 0:
                forced_pairs.append([left, right])
    return {
        "annihilator_pair_rank_by_pair": ranks,
        "annihilator_forced_equal_pairs": forced_pairs,
        "annihilator_diagonal": len(forced_pairs) == 21,
    }


def classify(row: dict[str, Any]) -> str:
    if row["forced_functional_identities"] > 0:
        return "RANK_FEEDBACK_FORCED_IDENTITY"
    if row["functional_span_rank"] < 5:
        return "RANK_FEEDBACK_LOW_FUNCTIONAL_SPAN"
    if row["annihilator_diagonal"]:
        return "RANK_FEEDBACK_DIAGONAL_ANNIHILATOR"
    if row["proxy_nullity"] is None:
        return "RANK_FEEDBACK_PROXY_NOT_RUN"
    if row["proxy_nullity"] > 0:
        return "RANK_FEEDBACK_PROXY_NULLITY_POSITIVE"
    return "RANK_FEEDBACK_PROXY_FULL_RANK"


def analyze_candidate(candidate: dict[str, Any], proxy_budget: bool) -> dict[str, Any]:
    classes = functional.functional_classes(candidate)
    functionals = [row["functional"] for row in classes]
    span_rank = functional.rank_mod_p(functionals)
    annihilator = functional.nullspace_basis(functionals)
    basis_profiles = functional.basis_profiles(classes, functional_span_rank=span_rank)
    best_profile = basis_profiles[0] if basis_profiles else None
    proxy = {
        "proxy_field": "GF(12289)",
        "proxy_matrix_shape": None,
        "proxy_rank": None,
        "proxy_nullity": None,
    }
    if proxy_budget and best_profile is not None and not any(row["forced_identity"] for row in classes):
        proxy = functional.proxy_basis_rank(classes, best_profile)
    ann = annihilator_pair_ranks(candidate["template_vectors"], annihilator)
    row = {
        "template_id": candidate["template_id"],
        "template_family": candidate["template_family"],
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "template_dimension": candidate["template_dimension"],
        "template_vectors": candidate["template_vectors"],
        "support_vector": candidate["support_vector"],
        "pair7_counts": candidate["pair7_counts"],
        "max_pair_count": candidate["max_pair_count"],
        "selected_class_size_counts": candidate["selected_class_size_counts"],
        "effective_cost": candidate["total_effective_cost"],
        "variable_count": candidate["variable_count"],
        "source_proxy_rank": candidate["proxy_rank"],
        "source_proxy_nullity": candidate["proxy_nullity"],
        "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        "coordinate_classes": candidate["coordinate_classes"],
        "functional_classes": len(classes),
        "functional_classes_hash": hash_payload(classes),
        "functional_span_rank": span_rank,
        "annihilator_dimension": len(annihilator),
        "annihilator_basis": annihilator,
        "forced_functional_identities": sum(1 for item in classes if item["forced_identity"]),
        "basis_profiles_tested": len(basis_profiles),
        "best_basis_id": None if best_profile is None else best_profile["basis_id"],
        "best_basis_support_sizes": None if best_profile is None else best_profile["basis_support_sizes"],
        "best_matrix_shape": proxy["proxy_matrix_shape"],
        "best_q_variable_count": None if best_profile is None else best_profile["q_variable_count"],
        "proxy_field": proxy["proxy_field"],
        "proxy_rank": proxy["proxy_rank"],
        "proxy_nullity": proxy["proxy_nullity"],
        **ann,
    }
    row["best_failure_mode"] = classify(row)
    return row


def build_record(max_proxy_cases: int) -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    base_vectors = source["survivor"]["template_vectors"]
    profiles = []
    candidates = []
    for spec in candidate_specs(base_vectors):
        profile = lowrank.solve_template_counts(spec)
        profiles.append(profile)
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for index, strategy in enumerate(profile["assignment_strategies"]):
            candidates.append(lowrank.evaluate_candidate(profile, strategy, seed=4100 + index * 37))

    # Analyze cheap structure for all candidates, but proxy-rank only the best small set.
    cheap_rows = []
    for candidate in candidates:
        cheap_rows.append(analyze_candidate(candidate, proxy_budget=False))
    proxy_order = sorted(
        range(len(cheap_rows)),
        key=lambda idx: (
            cheap_rows[idx]["forced_functional_identities"],
            -cheap_rows[idx]["functional_span_rank"],
            cheap_rows[idx]["annihilator_diagonal"],
            cheap_rows[idx]["effective_cost"],
        ),
    )
    proxy_indices = set(proxy_order[:max_proxy_cases])
    rows = []
    for idx, candidate in enumerate(candidates):
        rows.append(analyze_candidate(candidate, proxy_budget=idx in proxy_indices))

    proxy_positive = [row for row in rows if row["best_failure_mode"] == "RANK_FEEDBACK_PROXY_NULLITY_POSITIVE"]
    if proxy_positive:
        best = max(
            proxy_positive,
            key=lambda row: (
                row["proxy_nullity"],
                row["functional_span_rank"],
                -len(row["annihilator_forced_equal_pairs"]),
            ),
        )
        proof_status = "CANDIDATE / RANK_FEEDBACK_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "RANK_FEEDBACK_PROXY_NULLITY_POSITIVE"
    elif rows:
        best = max(
            rows,
            key=lambda row: (
                row["proxy_nullity"] or -1,
                row["functional_span_rank"],
                -row["forced_functional_identities"],
                -len(row["annihilator_forced_equal_pairs"]),
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RANK_FEEDBACK_PROXY_FULL_RANK"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "RANK_FEEDBACK_SUPPORT_FAIL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_functional_lift": {
            "template_id": source["survivor"]["template_id"],
            "functional_classes": source["functional_lift"]["functional_classes"],
            "functional_span_rank": source["functional_lift"]["functional_span_rank"],
            "best_matrix_shape": source["functional_lift"]["best_matrix_shape"],
            "proxy_rank": source["functional_lift"]["proxy_rank"],
            "proxy_nullity": source["functional_lift"]["proxy_nullity"],
            "best_failure_mode": source["functional_lift"]["best_failure_mode"],
        },
        "rank_feedback_search": {
            "templates_tested": len(profiles),
            "systems_tested": len(rows),
            "proxy_cases_tested": sum(1 for row in rows if row["proxy_rank"] is not None),
            "proxy_positive_candidates": len(proxy_positive),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_functional_span_rank": None if best is None else best["functional_span_rank"],
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "profiles": profiles,
            "candidates": rows,
        },
        "best_candidate": best,
        "exact_audit": {
            "run": False,
            "field": None,
            "H_order": None,
            "rank": None,
            "nullity": None,
            "best_failure_mode": None,
        },
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-proxy-cases", type=int, default=6)
    args = parser.parse_args()
    record = build_record(max_proxy_cases=args.max_proxy_cases)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["rank_feedback_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "templates_tested": search["templates_tested"],
                    "systems_tested": search["systems_tested"],
                    "proxy_cases_tested": search["proxy_cases_tested"],
                    "proxy_positive_candidates": search["proxy_positive_candidates"],
                    "best_template_id": search["best_template_id"],
                    "best_functional_span_rank": search["best_functional_span_rank"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_RANDOM_MATROID_RANK_FEEDBACK_V2_READY")


if __name__ == "__main__":
    main()
