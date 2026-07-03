#!/usr/bin/env python3
"""Dependency-engineered proxy search for M1 a=327 random-matroid templates."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "614bf1c"
V2_DATA = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v2.json")
V3_DATA = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v3.json")
RIGIDITY_DATA = Path("experimental/data/m1_a327_random_matroid_rank_rigidity_audit.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_dependency_engineered_rank_feedback.json")

ROOT = Path(__file__).resolve().parents[2]
V3_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_random_matroid_rank_feedback_v3.py"

TARGET_AGREEMENT = 327
PAIR7_LOWER = 142
PAIR_CAP = 255
FIBER_COUNT = 16
N = 512


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


v3 = load_module("random_matroid_rank_feedback_v3", V3_SCRIPT)
lowrank = v3.lowrank
functional = v3.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def mask_members(mask: int) -> list[int]:
    return [idx + 1 for idx in range(7) if mask & (1 << idx)]


def contains(mask: int, witness_one_based: int) -> bool:
    return bool(mask & (1 << (witness_one_based - 1)))


def expanded_masks(counts: list[dict[str, Any]]) -> list[int]:
    masks: list[int] = []
    for row in counts:
        masks.extend([int(row["mask"])] * int(row["count"]))
    if len(masks) != N:
        raise RuntimeError("bad coordinate count")
    return masks


def mask_signature(vectors: list[list[int]], mask: int) -> tuple[tuple[int, ...], ...]:
    rows = []
    for row in functional.row_basis_mod_p(vectors, mask_members(mask)):
        rows.append(tuple(functional.normalize_projective(row)))
    return tuple(sorted(rows))


def dependency_ordered_masks(profile: dict[str, Any], strategy: str, seed: int) -> list[int]:
    masks = expanded_masks(profile["selected_counts"])
    vectors = profile["template_vectors"]
    rng = random.Random(seed)
    sig_cache = {mask: mask_signature(vectors, mask) for mask in set(masks)}
    if strategy == "signature_fiber_blocks":
        masks.sort(key=lambda mask: (sig_cache[mask], mask.bit_count(), mask))
    elif strategy == "signature_residue_blocks":
        masks.sort(key=lambda mask: (mask.bit_count(), sig_cache[mask], mask))
    elif strategy == "pair7_signature_blocks":
        masks.sort(key=lambda mask: (not contains(mask, 7), sig_cache[mask], mask.bit_count(), mask))
    elif strategy == "dependency_twin_interleave":
        groups: dict[tuple[tuple[int, ...], ...], list[int]] = defaultdict(list)
        for mask in masks:
            groups[sig_cache[mask]].append(mask)
        keys = sorted(groups, key=lambda key: (-len(groups[key]), key))
        out = []
        while any(groups.values()):
            for key in keys:
                if groups[key]:
                    out.append(groups[key].pop())
        masks = out
    elif strategy == "fiber_factor_packed":
        masks.sort(key=lambda mask: (sig_cache[mask], not contains(mask, 7), -mask.bit_count(), mask))
    elif strategy == "seeded_dependency_shuffle":
        masks.sort(key=lambda mask: (sig_cache[mask], mask))
        chunks = [masks[start : start + FIBER_COUNT] for start in range(0, len(masks), FIBER_COUNT)]
        for chunk in chunks:
            rng.shuffle(chunk)
        masks = [mask for chunk in chunks for mask in chunk]
    else:
        raise ValueError(f"unknown dependency strategy: {strategy}")
    return masks


def dependency_positions(strategy: str, seed: int) -> list[int]:
    if strategy in {"signature_fiber_blocks", "fiber_factor_packed"}:
        return [fiber + FIBER_COUNT * idx for fiber in range(FIBER_COUNT) for idx in range(N // FIBER_COUNT)]
    if strategy == "signature_residue_blocks":
        return [pos for residue in range(32) for pos in range(residue, N, 32)]
    if strategy == "dependency_twin_interleave":
        return [idx + 32 * block for idx in range(32) for block in range(16)]
    if strategy == "pair7_signature_blocks":
        return list(range(N))
    if strategy == "seeded_dependency_shuffle":
        rng = random.Random(seed)
        positions = [fiber + FIBER_COUNT * idx for fiber in range(FIBER_COUNT) for idx in range(N // FIBER_COUNT)]
        fiber_blocks = [positions[start : start + 32] for start in range(0, len(positions), 32)]
        for block in fiber_blocks:
            rng.shuffle(block)
        return [pos for block in fiber_blocks for pos in block]
    raise ValueError(f"unknown dependency strategy: {strategy}")


def assign_dependency_coordinates(profile: dict[str, Any], strategy: str, seed: int) -> list[dict[str, Any]]:
    masks = dependency_ordered_masks(profile, strategy, seed)
    positions = dependency_positions(strategy, seed)
    coordinates = [None] * N
    for mask, position in zip(masks, positions, strict=True):
        coordinates[position] = {
            "position": position,
            "fiber": position % FIBER_COUNT,
            "mask": mask,
            "members": mask_members(mask),
            "size": mask.bit_count(),
        }
    return [row for row in coordinates if row is not None]


def evaluate_dependency_candidate(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    coordinates = assign_dependency_coordinates(profile, strategy, seed)
    pairs = lowrank.pair_counts(coordinates)
    pair7 = [pairs[label] for label in lowrank.PAIR7_PAIR_LABELS]
    return {
        "template_id": profile["template_id"],
        "template_family": profile["template_family"],
        "template_dimension": profile["template_dimension"],
        "template_vectors": profile["template_vectors"],
        "assignment_strategy": strategy,
        "assignment_seed": seed,
        "support_vector": lowrank.support_counts(coordinates),
        "pair_count_matrix": pairs,
        "max_pair_count": max(pairs.values()),
        "pair7_counts": pair7,
        "selected_class_size_counts": lowrank.size_histogram(coordinates),
        "total_effective_cost": profile["total_effective_cost"],
        "variable_count": profile["variable_count"],
        "cost_margin": profile["variable_count"] - profile["total_effective_cost"],
        "coordinate_classes_hash": hash_payload(coordinates),
        "quotient_fiber_histogram": lowrank.fiber_histogram(coordinates),
        "coordinate_classes": coordinates,
        "proxy_prime": v3.PROXY_PRIME,
        "proxy_rank": None,
        "proxy_nullity": None,
        "best_failure_mode": "DEPENDENCY_ENGINEERED_PROXY_PENDING",
    }


def support_dependency_metrics(classes: list[dict[str, Any]]) -> dict[str, Any]:
    support_sets = [set(int(pos) for pos in row["positions"]) for row in classes]
    support_hashes = [row["positions_hash"] for row in classes]
    hash_counts = Counter(support_hashes)
    duplicate_groups = {key: value for key, value in hash_counts.items() if value > 1}
    duplicate_pairs = sum(value * (value - 1) // 2 for value in duplicate_groups.values())
    nested_pairs = 0
    overlap_total = 0
    for left in range(len(support_sets)):
        for right in range(left + 1, len(support_sets)):
            a = support_sets[left]
            b = support_sets[right]
            if a and b and (a <= b or b <= a):
                nested_pairs += 1
            overlap_total += len(a & b)
    return {
        "duplicate_support_groups": len(duplicate_groups),
        "duplicate_support_pairs": duplicate_pairs,
        "nested_support_pairs": nested_pairs,
        "support_overlap_total": overlap_total,
        "support_size_histogram": dict(Counter(str(len(item)) for item in support_sets)),
    }


def profile_dependency_score(classes: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    groups = Counter()
    weighted_groups = Counter()
    for row in profile["nonbasis_constraint_detail"]:
        key = tuple(int(value) for value in row["basis_coordinates"])
        groups[key] += 1
        weighted_groups[key] += int(row["support_size"])
    repeated_coordinate_groups = sum(1 for value in groups.values() if value > 1)
    repeated_coordinate_pairs = sum(value * (value - 1) // 2 for value in groups.values() if value > 1)
    repeated_coordinate_weight = sum(value for key, value in weighted_groups.items() if groups[key] > 1)
    basis_support_sum = sum(profile["basis_support_sizes"])
    row_surplus = profile["matrix_shape"][0] - profile["matrix_shape"][1]
    score = (
        20 * repeated_coordinate_pairs
        + repeated_coordinate_weight
        + basis_support_sum
        - row_surplus
        + profile["q_variable_count"]
    )
    return {
        "dependency_score": score,
        "repeated_coordinate_groups": repeated_coordinate_groups,
        "repeated_coordinate_pairs": repeated_coordinate_pairs,
        "repeated_coordinate_weight": repeated_coordinate_weight,
        "basis_support_sum": basis_support_sum,
        "row_surplus": row_surplus,
    }


def dependency_basis_profiles(classes: list[dict[str, Any]], span_rank: int, random_bases: int) -> list[dict[str, Any]]:
    base = v3.basis_profiles_v3(classes, span_rank=span_rank, random_bases=random_bases)
    enriched = []
    seen: set[tuple[int, ...]] = set()
    for profile in base:
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        metrics = profile_dependency_score(classes, profile)
        enriched.append(profile | {"dependency_metrics": metrics})
    return sorted(
        enriched,
        key=lambda row: (
            row["dependency_metrics"]["dependency_score"],
            row["dependency_metrics"]["repeated_coordinate_pairs"],
            row["formal_nullity_lower_bound"],
            row["q_variable_count"],
        ),
        reverse=True,
    )


def structural_status(row: dict[str, Any]) -> str:
    if row["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "DEPENDENCY_SUPPORT_FAIL"
    if row["max_pair_count"] > PAIR_CAP or min(row["pair7_counts"]) < PAIR7_LOWER:
        return "DEPENDENCY_PAIR_GUARD_FAIL"
    if row["forced_functional_identities"] > 0:
        return "DEPENDENCY_FORCED_IDENTITY"
    if row["functional_span_rank"] != 6:
        return "DEPENDENCY_LOW_FUNCTIONAL_SPAN"
    if row["annihilator_dimension"] != 0 or row["annihilator_diagonal"]:
        return "DEPENDENCY_DIAGONAL_ANNIHILATOR"
    return "DEPENDENCY_STRUCTURAL_PASS"


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
        "dependency_metrics": profile["dependency_metrics"],
    }


def analyze_candidate(candidate: dict[str, Any], max_bases: int, run_proxy: bool) -> dict[str, Any]:
    classes = functional.functional_classes(candidate)
    functionals = [row["functional"] for row in classes]
    span_rank = functional.rank_mod_p(functionals)
    annihilator = functional.nullspace_basis(functionals)
    ann = v3.annihilator_pair_ranks(candidate["template_vectors"], annihilator)
    forced = sum(1 for item in classes if item["forced_identity"])
    profiles = dependency_basis_profiles(classes, span_rank=span_rank, random_bases=16)
    support_metrics = support_dependency_metrics(classes)
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
        "support_dependency_metrics": support_metrics,
        **ann,
    }
    structural = structural_status(row)
    row["structural_status"] = structural
    proxy_results = []
    if run_proxy and structural == "DEPENDENCY_STRUCTURAL_PASS":
        for profile in profiles[:max_bases]:
            proxy_results.append(proxy_profile(classes, profile))
            if proxy_results[-1]["proxy_nullity"] and proxy_results[-1]["proxy_nullity"] > 0:
                break
    row["proxy_results"] = proxy_results
    row["best_proxy"] = None
    if proxy_results:
        row["best_proxy"] = max(
            proxy_results,
            key=lambda item: (
                item["proxy_nullity"],
                item["dependency_metrics"]["dependency_score"],
                -item["proxy_rank"],
                item["q_variable_count"],
            ),
        )
    if structural != "DEPENDENCY_STRUCTURAL_PASS":
        row["best_failure_mode"] = structural
    elif not proxy_results:
        row["best_failure_mode"] = "DEPENDENCY_PROXY_PENDING"
    elif row["best_proxy"]["proxy_nullity"] > 0:
        row["best_failure_mode"] = "DEPENDENCY_PROXY_NULLITY_POSITIVE"
    else:
        row["best_failure_mode"] = "DEPENDENCY_PROXY_FULL_RANK"
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
            "support_dependency_metrics",
            "structural_status",
            "best_failure_mode",
        ]
    } | {
        "best_proxy": row["best_proxy"],
        "proxy_results": row["proxy_results"],
    }


def build_record(max_templates: int, max_proxy_candidates: int, max_bases_per_candidate: int) -> dict[str, Any]:
    v2 = load_json(V2_DATA)
    v3_data = load_json(V3_DATA)
    rigidity = load_json(RIGIDITY_DATA)
    specs = v3.template_specs(v2, max_templates=max_templates)
    strategies = [
        "signature_fiber_blocks",
        "signature_residue_blocks",
        "pair7_signature_blocks",
        "dependency_twin_interleave",
        "fiber_factor_packed",
        "seeded_dependency_shuffle",
    ]
    profiles = []
    raw_candidates = []
    for spec_index, spec in enumerate(specs):
        profile = lowrank.solve_template_counts(spec)
        profiles.append(profile)
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for strategy_index, strategy in enumerate(strategies):
            raw_candidates.append(
                evaluate_dependency_candidate(
                    profile,
                    strategy,
                    seed=11000 + spec_index * 137 + strategy_index * 19,
                )
            )

    cheap_rows = [analyze_candidate(candidate, max_bases=max_bases_per_candidate, run_proxy=False) for candidate in raw_candidates]
    structural_indices = [
        idx for idx, row in enumerate(cheap_rows) if row["structural_status"] == "DEPENDENCY_STRUCTURAL_PASS"
    ]
    structural_indices = sorted(
        structural_indices,
        key=lambda idx: (
            cheap_rows[idx]["support_dependency_metrics"]["duplicate_support_pairs"],
            cheap_rows[idx]["support_dependency_metrics"]["nested_support_pairs"],
            cheap_rows[idx]["support_dependency_metrics"]["support_overlap_total"],
            -cheap_rows[idx]["effective_cost"],
            cheap_rows[idx]["template_id"],
        ),
        reverse=True,
    )
    proxy_indices = set(structural_indices[:max_proxy_candidates])
    rows = [
        analyze_candidate(candidate, max_bases=max_bases_per_candidate, run_proxy=idx in proxy_indices)
        for idx, candidate in enumerate(raw_candidates)
    ]
    proxy_positive = [row for row in rows if row["best_failure_mode"] == "DEPENDENCY_PROXY_NULLITY_POSITIVE"]
    proxy_ranked = [row for row in rows if row["proxy_results"]]
    if proxy_positive:
        best = max(
            proxy_positive,
            key=lambda row: (
                row["best_proxy"]["proxy_nullity"],
                row["best_proxy"]["dependency_metrics"]["dependency_score"],
                -row["best_proxy"]["proxy_rank"],
            ),
        )
        proof_status = "CANDIDATE / DEPENDENCY_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "DEPENDENCY_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = max(
            proxy_ranked,
            key=lambda row: (
                row["best_proxy"]["dependency_metrics"]["dependency_score"],
                -row["best_proxy"]["proxy_rank"],
                row["support_dependency_metrics"]["support_overlap_total"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / DEPENDENCY_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "DEPENDENCY_PROXY_FULL_RANK"
    elif rows:
        best = max(
            rows,
            key=lambda row: (
                row["support_dependency_metrics"]["duplicate_support_pairs"],
                row["support_dependency_metrics"]["nested_support_pairs"],
                row["functional_span_rank"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / DEPENDENCY_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "DEPENDENCY_PROXY_PENDING"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / DEPENDENCY_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "DEPENDENCY_SUPPORT_FAIL"

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
        "previous_rank_feedback_v3": {
            "commit": "f50b089",
            "systems_tested": v3_data["rank_feedback_v3"]["systems_tested"],
            "structural_pass_candidates": v3_data["rank_feedback_v3"]["structural_pass_candidates"],
            "proxy_candidates_tested": v3_data["rank_feedback_v3"]["proxy_candidates_tested"],
            "proxy_basis_profiles_tested": v3_data["rank_feedback_v3"]["proxy_basis_profiles_tested"],
            "proxy_positive_candidates": v3_data["rank_feedback_v3"]["proxy_positive_candidates"],
            "best_template_id": v3_data["rank_feedback_v3"]["best_template_id"],
            "best_proxy_rank": v3_data["rank_feedback_v3"]["best_proxy_rank"],
            "best_proxy_nullity": v3_data["rank_feedback_v3"]["best_proxy_nullity"],
        },
        "previous_rank_rigidity_audit": {
            "commit": SOURCE_COMMIT,
            "proxy_profiles_audited": rigidity["rank_rigidity_audit"]["proxy_profiles_audited"],
            "full_column_rank_profiles": rigidity["rank_rigidity_audit"]["full_column_rank_profiles"],
            "row_surplus": rigidity["rank_rigidity_audit"]["min_row_surplus"],
            "best_failure_mode": rigidity["rank_rigidity_audit"]["best_failure_mode"],
        },
        "dependency_engineered_search": {
            "templates_tested": len(specs),
            "profiles_constructed": len(profiles),
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "DEPENDENCY_STRUCTURAL_PASS"),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_basis_profiles_tested": sum(len(row["proxy_results"]) for row in rows),
            "proxy_positive_candidates": len(proxy_positive),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_functional_span_rank": None if best is None else best["functional_span_rank"],
            "best_proxy_rank": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_nullity"],
            "best_dependency_score": None if best is None or best["best_proxy"] is None else best["best_proxy"]["dependency_metrics"]["dependency_score"],
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
    parser.add_argument("--max-templates", type=int, default=18)
    parser.add_argument("--max-proxy-candidates", type=int, default=8)
    parser.add_argument("--max-bases-per-candidate", type=int, default=3)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_proxy_candidates=args.max_proxy_candidates,
        max_bases_per_candidate=args.max_bases_per_candidate,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["dependency_engineered_search"]
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
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_functional_span_rank": search["best_functional_span_rank"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_dependency_score": search["best_dependency_score"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                    "screen_counts": search["screen_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_DEPENDENCY_ENGINEERED_RANK_FEEDBACK_READY")


if __name__ == "__main__":
    main()
