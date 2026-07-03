#!/usr/bin/env python3
"""Rank-feedback v3 search around random-matroid M1 a=327 templates."""

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


SOURCE_COMMIT = "2dcae46"
SOURCE_DATA = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v2.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v3.json")

ROOT = Path(__file__).resolve().parents[2]
LOWRANK_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_lowrank_template_selected_class_search.py"
FUNCTIONAL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_random_matroid_functional_lift.py"

TARGET_AGREEMENT = 327
PAIR7_LOWER = 142
PAIR_CAP = 255
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


def shear_vectors(base_vectors: list[list[int]], seed: int) -> list[list[int]]:
    rng = random.Random(seed)
    out = normalize_vectors(base_vectors)
    left = rng.randrange(TEMPLATE_DIM)
    right = rng.randrange(TEMPLATE_DIM)
    while right == left:
        right = rng.randrange(TEMPLATE_DIM)
    scale = rng.randrange(1, 17)
    for row in out:
        row[left] = (row[left] + scale * row[right]) % 17
    for _ in range(3):
        row_idx = rng.randrange(len(out))
        col = rng.randrange(TEMPLATE_DIM)
        out[row_idx][col] = (out[row_idx][col] + rng.randrange(1, 17)) % 17
    return out


def template_specs(source: dict[str, Any], max_templates: int) -> list[dict[str, Any]]:
    base_row = next(
        (
            row
            for row in source["rank_feedback_search"]["candidates"]
            if row["template_id"] == "random_matroid_seeded_0_m6"
        ),
        source["best_candidate"],
    )
    base_vectors = normalize_vectors(base_row["template_vectors"])
    v2_vectors = normalize_vectors(source["best_candidate"]["template_vectors"])
    specs: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(template_id: str, family: str, vectors: list[list[int]], selected_sizes: list[int], cost: float, pair7: float) -> None:
        nonlocal specs
        if len(specs) >= max_templates:
            return
        vectors = normalize_vectors(vectors)
        key = hash_payload(vectors + [selected_sizes])
        if key in seen:
            return
        seen.add(key)
        specs.append(
            {
                "template_id": template_id,
                "template_family": family,
                "vectors": vectors,
                "selected_class_sizes": selected_sizes,
                "cost_weight": cost,
                "pair7_weight": pair7,
                "assignment_strategies": ["sorted_block", "fiber_round_robin", "residue_block", "fiber_block"],
            }
        )

    add("random_matroid_seeded_0_m6", "random_matroid_rank_feedback_v3", base_vectors, [3, 4, 5], 5.0, 1.0)
    add("random_matroid_v2_best_seed_1_m6", "random_matroid_rank_feedback_v3", v2_vectors, [3, 4, 5], 5.0, 1.0)

    seeds = list(range(101, 101 + max_templates * 3))
    for idx, seed in enumerate(seeds, start=1):
        parent = base_vectors if idx % 2 else v2_vectors
        if idx % 3 == 0:
            vectors = shear_vectors(parent, seed)
            family = "random_matroid_shear_feedback_v3"
        else:
            vectors = mutate_vectors(parent, seed=seed, weight=1 + (idx % 5))
            family = "random_matroid_mutation_feedback_v3"
        selected_sizes = [3, 4, 5, 6] if idx % 4 == 0 else [3, 4, 5]
        add(
            f"random_matroid_v3_seed_{idx:03d}_m6",
            family,
            vectors,
            selected_sizes,
            cost=4.0 + (idx % 4),
            pair7=1.0 + 0.5 * (idx % 3),
        )
        if len(specs) >= max_templates:
            break
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


def profile_from_order(classes: list[dict[str, Any]], order: list[int], basis_id: str, span_rank: int) -> dict[str, Any] | None:
    rows = [row["functional"] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    selected = functional.independent_greedy(rows, order, target_rank=span_rank)
    if len(selected) != span_rank:
        return None
    basis_rows = [rows[idx] for idx in selected]
    q_variable_count = sum(256 - supports[idx] for idx in selected)
    nonbasis_rows = 0
    nonbasis_constraints = []
    for idx, row in enumerate(rows):
        if idx in selected:
            continue
        coords = functional.solve_coordinates(row, basis_rows)
        if coords is None:
            return None
        nonbasis_rows += supports[idx]
        nonbasis_constraints.append(
            {
                "class_index": int(classes[idx]["class_index"]),
                "support_size": supports[idx],
                "basis_coordinates": coords,
            }
        )
    return {
        "basis_id": basis_id,
        "basis_class_indices": [int(classes[idx]["class_index"]) for idx in selected],
        "basis_functionals": [classes[idx]["functional"] for idx in selected],
        "basis_support_sizes": [supports[idx] for idx in selected],
        "q_variable_count": q_variable_count,
        "nonbasis_constraints": len(nonbasis_constraints),
        "matrix_shape": [nonbasis_rows, q_variable_count],
        "formal_nullity_lower_bound": max(0, q_variable_count - nonbasis_rows),
        "nonbasis_constraint_detail": nonbasis_constraints,
    }


def basis_profiles_v3(classes: list[dict[str, Any]], span_rank: int, random_bases: int) -> list[dict[str, Any]]:
    rows = [row["functional"] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    hamming = [sum(1 for value in row if int(value) % 17) for row in rows]
    orders: dict[str, list[int]] = {
        "max_support_basis": sorted(range(len(classes)), key=lambda idx: (-supports[idx], rows[idx])),
        "min_q_variable_basis": sorted(range(len(classes)), key=lambda idx: (256 - supports[idx], rows[idx])),
        "balanced_support_basis": sorted(range(len(classes)), key=lambda idx: (abs(supports[idx] - 128), -supports[idx], rows[idx])),
        "dependency_weighted_basis": sorted(range(len(classes)), key=lambda idx: (-supports[idx] * max(1, hamming[idx]), hamming[idx], rows[idx])),
    }
    for seed in range(random_bases):
        rng = random.Random(9000 + seed)
        order = list(range(len(classes)))
        rng.shuffle(order)
        orders[f"deterministic_random_basis_{seed}"] = order

    profiles = []
    seen: set[tuple[int, ...]] = set()
    for basis_id, order in orders.items():
        profile = profile_from_order(classes, order, basis_id, span_rank)
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        profiles.append(profile)
    return sorted(
        profiles,
        key=lambda row: (
            row["formal_nullity_lower_bound"],
            row["q_variable_count"],
            -row["matrix_shape"][0],
        ),
        reverse=True,
    )


def structural_status(row: dict[str, Any]) -> str:
    if row["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "RANK_FEEDBACK_SUPPORT_FAIL"
    if row["max_pair_count"] > PAIR_CAP or min(row["pair7_counts"]) < PAIR7_LOWER:
        return "RANK_FEEDBACK_PAIR_GUARD_FAIL"
    if row["forced_functional_identities"] > 0:
        return "RANK_FEEDBACK_FORCED_IDENTITY"
    if row["functional_span_rank"] != 6:
        return "RANK_FEEDBACK_LOW_FUNCTIONAL_SPAN"
    if row["annihilator_dimension"] != 0 or row["annihilator_diagonal"]:
        return "RANK_FEEDBACK_DIAGONAL_ANNIHILATOR"
    return "RANK_FEEDBACK_STRUCTURAL_PASS"


def proxy_status(proxy_results: list[dict[str, Any]], structural: str) -> str:
    if structural != "RANK_FEEDBACK_STRUCTURAL_PASS":
        return structural
    if not proxy_results:
        return "RANK_FEEDBACK_PROXY_PENDING"
    if any(row["proxy_nullity"] and row["proxy_nullity"] > 0 for row in proxy_results):
        return "RANK_FEEDBACK_PROXY_NULLITY_POSITIVE"
    return "RANK_FEEDBACK_PROXY_FULL_RANK"


def proxy_profile(classes: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    result = functional.proxy_basis_rank(classes, profile)
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "q_variable_count": profile["q_variable_count"],
        "matrix_shape": result["proxy_matrix_shape"],
        "proxy_field": result["proxy_field"],
        "proxy_rank": result["proxy_rank"],
        "proxy_nullity": result["proxy_nullity"],
    }


def analyze_candidate(candidate: dict[str, Any], max_bases: int, run_proxy: bool) -> dict[str, Any]:
    classes = functional.functional_classes(candidate)
    functionals = [row["functional"] for row in classes]
    span_rank = functional.rank_mod_p(functionals)
    annihilator = functional.nullspace_basis(functionals)
    ann = annihilator_pair_ranks(candidate["template_vectors"], annihilator)
    forced = sum(1 for item in classes if item["forced_identity"])
    profiles = basis_profiles_v3(classes, span_rank=span_rank, random_bases=12)
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
        "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        "functional_classes": len(classes),
        "functional_classes_hash": hash_payload(classes),
        "functional_span_rank": span_rank,
        "annihilator_dimension": len(annihilator),
        "annihilator_basis": annihilator,
        "forced_functional_identities": forced,
        "basis_profiles_tested": len(profiles),
        **ann,
    }
    structural = structural_status(row)
    row["structural_status"] = structural
    proxy_results = []
    if run_proxy and structural == "RANK_FEEDBACK_STRUCTURAL_PASS":
        for profile in profiles[:max_bases]:
            proxy_results.append(proxy_profile(classes, profile))
            if proxy_results[-1]["proxy_nullity"] and proxy_results[-1]["proxy_nullity"] > 0:
                break
    row["proxy_results"] = proxy_results
    row["best_proxy"] = None
    if proxy_results:
        row["best_proxy"] = max(proxy_results, key=lambda item: (item["proxy_nullity"], -item["proxy_rank"], item["q_variable_count"]))
    row["best_failure_mode"] = proxy_status(proxy_results, structural)
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in [
            "template_id",
            "template_family",
            "assignment_strategy",
            "assignment_seed",
            "template_dimension",
            "support_vector",
            "pair7_counts",
            "max_pair_count",
            "selected_class_size_counts",
            "effective_cost",
            "variable_count",
            "coordinate_classes_hash",
            "functional_classes",
            "functional_span_rank",
            "annihilator_dimension",
            "forced_functional_identities",
            "basis_profiles_tested",
            "structural_status",
            "best_failure_mode",
        ]
    } | {
        "best_proxy": row["best_proxy"],
        "proxy_results": row["proxy_results"],
    }


def build_record(max_templates: int, max_proxy_candidates: int, max_bases_per_candidate: int) -> dict[str, Any]:
    source = load_json(SOURCE_DATA)
    specs = template_specs(source, max_templates=max_templates)
    profiles = []
    raw_candidates = []
    for spec_index, spec in enumerate(specs):
        profile = lowrank.solve_template_counts(spec)
        profiles.append(profile)
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for strategy_index, strategy in enumerate(profile["assignment_strategies"]):
            raw_candidates.append(lowrank.evaluate_candidate(profile, strategy, seed=7000 + spec_index * 101 + strategy_index * 17))

    cheap_rows = [analyze_candidate(candidate, max_bases=max_bases_per_candidate, run_proxy=False) for candidate in raw_candidates]
    structural_indices = [
        idx for idx, row in enumerate(cheap_rows) if row["structural_status"] == "RANK_FEEDBACK_STRUCTURAL_PASS"
    ]
    structural_indices = sorted(
        structural_indices,
        key=lambda idx: (
            -cheap_rows[idx]["basis_profiles_tested"],
            cheap_rows[idx]["effective_cost"],
            cheap_rows[idx]["functional_classes"],
            cheap_rows[idx]["template_id"],
        ),
    )
    proxy_indices = set(structural_indices[:max_proxy_candidates])
    rows = [
        analyze_candidate(candidate, max_bases=max_bases_per_candidate, run_proxy=idx in proxy_indices)
        for idx, candidate in enumerate(raw_candidates)
    ]

    proxy_positive = [row for row in rows if row["best_failure_mode"] == "RANK_FEEDBACK_PROXY_NULLITY_POSITIVE"]
    proxy_ranked = [row for row in rows if row["proxy_results"]]
    if proxy_positive:
        best = max(
            proxy_positive,
            key=lambda row: (
                row["best_proxy"]["proxy_nullity"],
                -row["best_proxy"]["proxy_rank"],
                row["functional_classes"],
            ),
        )
        proof_status = "CANDIDATE / RANK_FEEDBACK_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "RANK_FEEDBACK_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = max(
            proxy_ranked,
            key=lambda row: (
                row["functional_span_rank"],
                -(row["best_proxy"]["proxy_rank"] if row["best_proxy"] else 10**9),
                row["best_proxy"]["q_variable_count"] if row["best_proxy"] else -1,
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RANK_FEEDBACK_PROXY_FULL_RANK"
    elif rows:
        best = max(rows, key=lambda row: (row["functional_span_rank"], -row["forced_functional_identities"], row["template_id"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "RANK_FEEDBACK_PROXY_PENDING"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "RANK_FEEDBACK_SUPPORT_FAIL"

    best_full = None
    if best is not None:
        for candidate in raw_candidates:
            if candidate["coordinate_classes_hash"] == best["coordinate_classes_hash"]:
                best_full = candidate
                break

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_rank_feedback_v2": {
            "commit": SOURCE_COMMIT,
            "templates_tested": source["rank_feedback_search"]["templates_tested"],
            "systems_tested": source["rank_feedback_search"]["systems_tested"],
            "proxy_cases_tested": source["rank_feedback_search"]["proxy_cases_tested"],
            "proxy_positive_candidates": source["rank_feedback_search"]["proxy_positive_candidates"],
            "best_template_id": source["rank_feedback_search"]["best_template_id"],
            "best_functional_span_rank": source["rank_feedback_search"]["best_functional_span_rank"],
            "best_proxy_rank": source["rank_feedback_search"]["best_proxy_rank"],
            "best_proxy_nullity": source["rank_feedback_search"]["best_proxy_nullity"],
            "best_failure_mode": source["rank_feedback_search"]["best_failure_mode"],
        },
        "rank_feedback_v3": {
            "templates_tested": len(specs),
            "profiles_constructed": len(profiles),
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "RANK_FEEDBACK_STRUCTURAL_PASS"),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_basis_profiles_tested": sum(len(row["proxy_results"]) for row in rows),
            "proxy_positive_candidates": len(proxy_positive),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_functional_span_rank": None if best is None else best["functional_span_rank"],
            "best_proxy_rank": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "profiles": profiles,
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best) | {"coordinate_classes": None if best_full is None else best_full["coordinate_classes"]},
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
    parser.add_argument("--max-templates", type=int, default=36)
    parser.add_argument("--max-proxy-candidates", type=int, default=16)
    parser.add_argument("--max-bases-per-candidate", type=int, default=5)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_proxy_candidates=args.max_proxy_candidates,
        max_bases_per_candidate=args.max_bases_per_candidate,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["rank_feedback_v3"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "templates_tested": search["templates_tested"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "proxy_candidates_tested": search["proxy_candidates_tested"],
                    "proxy_basis_profiles_tested": search["proxy_basis_profiles_tested"],
                    "proxy_positive_candidates": search["proxy_positive_candidates"],
                    "best_template_id": search["best_template_id"],
                    "best_functional_span_rank": search["best_functional_span_rank"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                    "screen_counts": search["screen_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_RANDOM_MATROID_RANK_FEEDBACK_V3_READY")


if __name__ == "__main__":
    main()
