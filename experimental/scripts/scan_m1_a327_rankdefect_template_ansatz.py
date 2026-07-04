#!/usr/bin/env python3
"""Generate rank-defect-oriented template ansatzes for M1 a=327."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "d7b67e4"
PREVIOUS_DATA = Path("experimental/data/m1_a327_basis_kernel_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_rankdefect_template_ansatz.json")

ROOT = Path(__file__).resolve().parents[2]
CODESIGN_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_basis_kernel_codesign.py"

P = 17
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


codesign = load_module("basis_kernel_codesign", CODESIGN_SCRIPT)
joint = codesign.joint
lowrank = joint.lowrank
dependency = joint.dependency


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def dot(left: list[int], right: list[int]) -> int:
    return sum(int(a) * int(b) for a, b in zip(left, right, strict=True)) % P


def rank_rows(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> int:
    return joint.right_kernel.rank_rows(rows, ncols=ncols, prime=P)


def hyperplane_basis(relation: list[int]) -> list[list[int]]:
    pivot = next(idx for idx, value in enumerate(relation) if value % P)
    inv = pow(relation[pivot] % P, -1, P)
    basis = []
    for free in range(TEMPLATE_DIM):
        if free == pivot:
            continue
        row = [0] * TEMPLATE_DIM
        row[free] = 1
        row[pivot] = (-relation[free] * inv) % P
        basis.append(row)
    return basis


def outside_vector(relation: list[int], seed: int) -> list[int]:
    rng = random.Random(93000 + seed)
    for _attempt in range(1000):
        row = [rng.randrange(P) for _ in range(TEMPLATE_DIM)]
        if dot(relation, row):
            return row
    raise RuntimeError("could not find outside vector")


def normalize(vectors: list[list[int]]) -> list[list[int]]:
    return [[int(value) % P for value in row] for row in vectors]


def ansatz_specs(max_specs: int) -> list[dict[str, Any]]:
    relation_vectors = [
        [0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1],
        [1, 2, 3, 5, 8, 13],
        [0, 0, 0, 1, 1, 1],
        [1, 0, 0, 1, 0, 1],
        [0, 1, 0, 1, 1, 0],
        [0, 0, 1, 1, 0, 1],
    ]
    specs = []
    seen: set[str] = set()

    def add(template_id: str, family: str, vectors: list[list[int]], cost: float, pair7: float) -> None:
        if len(specs) >= max_specs:
            return
        vectors = normalize(vectors)
        if rank_rows([[vectors[idx][col] - vectors[0][col] for col in range(TEMPLATE_DIM)] for idx in range(1, 7)]) < 6:
            return
        key = hash_payload(vectors)
        if key in seen:
            return
        seen.add(key)
        specs.append(
            {
                "template_id": template_id,
                "template_family": family,
                "vectors": vectors,
                "selected_class_sizes": [3, 4, 5, 6],
                "cost_weight": cost,
                "pair7_weight": pair7,
                "assignment_strategies": [
                    "signature_fiber_blocks",
                    "signature_residue_blocks",
                    "pair7_signature_blocks",
                    "dependency_twin_interleave",
                    "fiber_factor_packed",
                    "seeded_dependency_shuffle",
                ],
            }
        )

    for rel_idx, relation in enumerate(relation_vectors):
        basis = hyperplane_basis(relation)
        basis_sum = [sum(row[col] for row in basis) % P for col in range(TEMPLATE_DIM)]
        for outside_witness in range(1, 8):
            outside = outside_vector(relation, 100 * rel_idx + outside_witness)
            vectors = [[0] * TEMPLATE_DIM]
            vectors.extend(basis[:5])
            vectors.append(basis_sum)
            vectors[outside_witness - 1] = outside
            add(
                f"rankdefect_hyperplane_r{rel_idx}_out{outside_witness}",
                "rankdefect_hyperplane_plus_outside",
                vectors,
                3.5 + (rel_idx % 3),
                1.0 + (outside_witness == 7),
            )
        for seed in range(3):
            rng = random.Random(94000 + 101 * rel_idx + seed)
            outside = outside_vector(relation, 1000 + 100 * rel_idx + seed)
            vectors = [[0] * TEMPLATE_DIM]
            for idx in range(5):
                combo = [0] * TEMPLATE_DIM
                for basis_row in basis:
                    scale = rng.randrange(P)
                    combo = [(value + scale * basis_row[col]) % P for col, value in enumerate(combo)]
                vectors.append(combo)
            vectors.append([sum(row[col] for row in vectors[1:]) % P for col in range(TEMPLATE_DIM)])
            vectors[6] = outside
            add(
                f"rankdefect_random_hyperplane_r{rel_idx}_seed{seed}",
                "rankdefect_random_hyperplane_plus_outside",
                vectors,
                4.0 + (seed % 2),
                1.5,
            )
    return specs[:max_specs]


def build_candidates(max_specs: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    specs = ansatz_specs(max_specs)
    profiles = []
    candidates = []
    for spec_index, spec in enumerate(specs):
        profile = lowrank.solve_template_counts(spec)
        profiles.append(profile)
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for strategy_index, strategy in enumerate(spec["assignment_strategies"]):
            candidates.append(
                dependency.evaluate_dependency_candidate(
                    profile,
                    strategy,
                    seed=95000 + spec_index * 137 + strategy_index * 19,
                )
            )
    return profiles, candidates


def analyze_candidate(candidate: dict[str, Any], stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    row = codesign.analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=run_proxy)
    row["best_failure_mode"] = row["best_failure_mode"].replace("CODESIGN", "RANKDEFECT")
    for profile in row.get("profile_summaries", []):
        profile["best_failure_mode"] = profile["best_failure_mode"].replace("CODESIGN", "RANKDEFECT")
    if row.get("best_profile") is not None:
        row["best_profile"]["best_failure_mode"] = row["best_profile"]["best_failure_mode"].replace("CODESIGN", "RANKDEFECT")
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    return codesign.candidate_summary(row)


def build_record(max_specs: int, stable_basis_limit: int, max_proxy_candidates: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, candidates = build_candidates(max_specs=max_specs)
    cheap_rows = [analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=False) for candidate in candidates]
    proxy_indices = [
        idx
        for idx, row in sorted(
            enumerate(cheap_rows),
            key=lambda item: (
                item[1]["pair_projection_clear_profiles"],
                item[1]["coefficient_kernel_profiles"],
                item[1]["forced_basis_profiles_tested"],
            ),
            reverse=True,
        )
        if row["pair_projection_clear_profiles"] > 0
    ][:max_proxy_candidates]
    proxy_index_set = set(proxy_indices)
    rows = [
        analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=idx in proxy_index_set)
        for idx, candidate in enumerate(candidates)
    ]
    proxy_positive = [row for row in rows if row["proxy_positive_profiles"] > 0]
    proxy_ranked = [row for row in rows if row["proxy_results_tested"] > 0]
    pair_clear = [row for row in rows if row["pair_projection_clear_profiles"] > 0]
    coefficient_kernel = [row for row in rows if row["coefficient_kernel_profiles"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / RANKDEFECT_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "RANKDEFECT_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = min(proxy_ranked, key=lambda row: row["best_profile"]["proxy_result"]["proxy_rank"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANKDEFECT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RANKDEFECT_PROXY_FULL_RANK"
    elif pair_clear:
        best = max(pair_clear, key=lambda row: row["pair_projection_clear_profiles"])
        proof_status = "CANDIDATE / RANKDEFECT_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "RANKDEFECT_PROXY_PENDING"
    elif coefficient_kernel:
        best = min(
            coefficient_kernel,
            key=lambda row: (
                row["best_profile"]["best_forced_pair_count"] if row["best_profile"] else 99,
                -row["coefficient_kernel_profiles"],
                row["template_id"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANKDEFECT_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        failure = "RANKDEFECT_FORCED_PAIR_EQUALITY"
    elif rows:
        best = max(rows, key=lambda row: (row["forced_basis_profiles_tested"], row["functional_span_rank"], row["template_id"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANKDEFECT_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RANKDEFECT_COEFFICIENT_FULL_RANK"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANKDEFECT_NO_CANDIDATES / PARTIAL / EXPERIMENTAL"
        failure = "RANKDEFECT_NO_CANDIDATES"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_basis_kernel_codesign": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "systems_tested": previous["basis_kernel_codesign"]["systems_tested"],
            "coefficient_kernel_profiles": previous["basis_kernel_codesign"]["coefficient_kernel_profiles"],
            "best_failure_mode": previous["basis_kernel_codesign"]["best_failure_mode"],
        },
        "rankdefect_template_ansatz": {
            "templates_generated": len(profiles),
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "target_present_candidates": sum(1 for row in rows if row["target_functional_present_modes"]),
            "forced_basis_combinations": sum(row["forced_basis_combinations"] for row in rows),
            "forced_basis_profiles_tested": sum(row["forced_basis_profiles_tested"] for row in rows),
            "coefficient_kernel_profiles": sum(row["coefficient_kernel_profiles"] for row in rows),
            "pair_projection_clear_profiles": sum(row["pair_projection_clear_profiles"] for row in rows),
            "proxy_results_tested": sum(row["proxy_results_tested"] for row in rows),
            "proxy_positive_profiles": sum(row["proxy_positive_profiles"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_target_mode": None if best is None or best["best_profile"] is None else best["best_profile"]["target_mode"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["best_forced_pair_count"],
            "best_coefficient_nullity": None if best is None or best["best_profile"] is None else best["best_profile"]["coefficient_nullity_gf17"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "profiles": profiles,
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "ACTUAL_TEMPLATE_ROWSPACES_ONLY",
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
            "Sage GF(17^32) exact lift",
            "synthetic rowspace edits",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-specs", type=int, default=64)
    parser.add_argument("--stable-basis-limit", type=int, default=96)
    parser.add_argument("--max-proxy-candidates", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        max_specs=args.max_specs,
        stable_basis_limit=args.stable_basis_limit,
        max_proxy_candidates=args.max_proxy_candidates,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["rankdefect_template_ansatz"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "templates_generated": search["templates_generated"],
                    "systems_tested": search["systems_tested"],
                    "target_present_candidates": search["target_present_candidates"],
                    "forced_basis_profiles_tested": search["forced_basis_profiles_tested"],
                    "coefficient_kernel_profiles": search["coefficient_kernel_profiles"],
                    "pair_projection_clear_profiles": search["pair_projection_clear_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_target_mode": search["best_target_mode"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_coefficient_nullity": search["best_coefficient_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_RANKDEFECT_TEMPLATE_ANSATZ_READY")


if __name__ == "__main__":
    main()
