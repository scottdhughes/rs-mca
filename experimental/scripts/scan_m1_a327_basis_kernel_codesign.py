#!/usr/bin/env python3
"""Co-design obstruction-functional basis inclusion with coefficient rank defect."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "cfc4f6d"
PREVIOUS_DATA = Path("experimental/data/m1_a327_obstruction_functional_basis_forcing.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_basis_kernel_codesign.json")

ROOT = Path(__file__).resolve().parents[2]
JOINT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py"
BASIS_FORCE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_obstruction_functional_basis_forcing.py"

P = 17
PROXY_PRIME = 12289
K = 256
TARGET_AGREEMENT = 327
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


joint = load_module("joint_template_right_kernel_search", JOINT_SCRIPT)
basis_force = load_module("obstruction_functional_basis_forcing", BASIS_FORCE_SCRIPT)
zstable = basis_force.zstable
functional = basis_force.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def stable_forced_combos(
    classes: list[dict[str, Any]],
    target_mode: str,
    limit: int,
) -> tuple[int, list[tuple[int, tuple[int, ...]]], list[int]]:
    targets = basis_force.TARGET_MODES[target_mode]
    by_functional = {
        basis_force.normalize(row["functional"]): idx
        for idx, row in enumerate(classes)
    }
    required = []
    for target in targets:
        if target not in by_functional:
            return 0, [], []
        required.append(by_functional[target])
    required_set = set(required)
    positions = zstable.class_position_sets(classes)
    rows = []
    stable_total = 0
    remaining = [idx for idx in range(len(classes)) if idx not in required_set]
    needed = TEMPLATE_DIM - len(required)
    for extra in itertools.combinations(remaining, needed):
        combo = tuple(sorted(tuple(required) + tuple(extra)))
        union_size = len(set().union(*(positions[int(classes[idx]["class_index"])] for idx in combo)))
        if union_size > K - 1:
            continue
        stable_total += 1
        support_sum = sum(int(classes[idx]["support_size"]) for idx in combo)
        rows.append((union_size, -support_sum, combo))
    rows.sort()
    return stable_total, [(union_size, combo) for union_size, _support_sum, combo in rows[:limit]], required


def summarize_codesign_profile(
    candidate: dict[str, Any],
    classes: list[dict[str, Any]],
    profile: dict[str, Any],
    target_mode: str,
    run_proxy: bool,
) -> dict[str, Any]:
    positions = zstable.class_position_sets(classes)
    matrix = zstable.coefficient_matrix(profile)
    rank17 = joint.right_kernel.rank_rows(matrix, ncols=TEMPLATE_DIM, prime=P)
    rank_proxy_coeff = functional.rank_mod_prime_matrix(matrix, ncols=TEMPLATE_DIM, prime=PROXY_PRIME)
    union_size = zstable.profile_union_size(profile, positions)
    pair_record = (
        zstable.pair_projection_record(candidate, profile)
        if rank17 < TEMPLATE_DIM
        else {
            "kernel_basis": [],
            "best_forced_pair_count": None,
            "best_forced_pairs": None,
            "best_pair_projection_scalars": None,
        }
    )
    failure = "CODESIGN_STABLE_RELATION_TARGET"
    if rank17 == TEMPLATE_DIM:
        failure = "CODESIGN_COEFFICIENT_FULL_RANK"
    elif pair_record["best_forced_pair_count"] and pair_record["best_forced_pair_count"] > 0:
        failure = "CODESIGN_FORCED_PAIR_EQUALITY"
    proxy = None
    if run_proxy and failure == "CODESIGN_STABLE_RELATION_TARGET":
        proxy_result = functional.proxy_basis_rank(classes, profile)
        proxy = {
            "matrix_shape": proxy_result["proxy_matrix_shape"],
            "proxy_field": proxy_result["proxy_field"],
            "proxy_rank": proxy_result["proxy_rank"],
            "proxy_nullity": proxy_result["proxy_nullity"],
        }
        failure = "CODESIGN_PROXY_NULLITY_POSITIVE" if proxy["proxy_nullity"] > 0 else "CODESIGN_PROXY_FULL_RANK"
    return {
        "basis_id": profile["basis_id"],
        "target_mode": target_mode,
        "basis_class_indices": profile["basis_class_indices"],
        "basis_functionals": profile["basis_functionals"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "q_variable_count": profile["q_variable_count"],
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "coefficient_rank_gf17": rank17,
        "coefficient_nullity_gf17": TEMPLATE_DIM - rank17,
        "coefficient_rank_gf12289": rank_proxy_coeff,
        "coefficient_nullity_gf12289": TEMPLATE_DIM - rank_proxy_coeff,
        "basis_zero_union_size": union_size,
        "stable_common_multiplier_dimension": K - union_size,
        "basis_zero_union_hash": hash_payload(sorted(set().union(*(positions[int(idx)] for idx in profile["basis_class_indices"])))),
        **pair_record,
        "proxy_result": proxy,
        "best_failure_mode": failure,
    }


def analyze_candidate(candidate: dict[str, Any], stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    row["forced_basis_modes_tested"] = 0
    row["target_functional_present_modes"] = []
    row["target_functional_missing_modes"] = []
    row["forced_basis_combinations"] = 0
    row["forced_basis_profiles_tested"] = 0
    row["coefficient_kernel_profiles"] = 0
    row["pair_projection_clear_profiles"] = 0
    row["proxy_results_tested"] = 0
    row["proxy_positive_profiles"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = zstable.mapped_structural_failure(row["structural_status"]).replace("ZSTABLE", "CODESIGN")
        return row

    classes = functional.functional_classes(candidate)
    summaries = []
    for target_mode in basis_force.TARGET_MODES:
        stable_total, front, required = stable_forced_combos(classes, target_mode=target_mode, limit=stable_basis_limit)
        row["forced_basis_modes_tested"] += 1
        row["forced_basis_combinations"] += stable_total
        if not required:
            row["target_functional_missing_modes"].append(target_mode)
            continue
        row["target_functional_present_modes"].append(target_mode)
        for union_size, combo in front:
            profile = zstable.profile_from_combo(
                classes,
                combo,
                f"codesign_{target_mode}_union_{union_size}_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
            )
            if profile is None:
                continue
            row["forced_basis_profiles_tested"] += 1
            summary = summarize_codesign_profile(candidate, classes, profile, target_mode=target_mode, run_proxy=run_proxy)
            if summary["coefficient_nullity_gf17"] <= 0:
                continue
            summaries.append(summary)
            if summary["best_failure_mode"] in {"CODESIGN_PROXY_NULLITY_POSITIVE", "CODESIGN_PROXY_FULL_RANK"}:
                row["proxy_results_tested"] += 1
            if summary["best_failure_mode"] == "CODESIGN_PROXY_NULLITY_POSITIVE":
                row["proxy_positive_profiles"] += 1
                break
    row["coefficient_kernel_profiles"] = len(summaries)
    row["pair_projection_clear_profiles"] = sum(
        1
        for item in summaries
        if item["best_failure_mode"] in {"CODESIGN_STABLE_RELATION_TARGET", "CODESIGN_PROXY_FULL_RANK", "CODESIGN_PROXY_NULLITY_POSITIVE"}
    )
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["best_failure_mode"] == "CODESIGN_PROXY_NULLITY_POSITIVE",
            item["best_failure_mode"] == "CODESIGN_PROXY_FULL_RANK",
            item["best_failure_mode"] == "CODESIGN_STABLE_RELATION_TARGET",
            item["coefficient_nullity_gf17"],
            -(item["best_forced_pair_count"] if item["best_forced_pair_count"] is not None else 99),
            item["stable_common_multiplier_dimension"],
            -item["basis_zero_union_size"],
        ),
        reverse=True,
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_positive_profiles"]:
        row["best_failure_mode"] = "CODESIGN_PROXY_NULLITY_POSITIVE"
    elif any(item["best_failure_mode"] == "CODESIGN_PROXY_FULL_RANK" for item in summaries):
        row["best_failure_mode"] = "CODESIGN_PROXY_FULL_RANK"
    elif row["pair_projection_clear_profiles"]:
        row["best_failure_mode"] = "CODESIGN_PROXY_PENDING"
    elif row["coefficient_kernel_profiles"]:
        row["best_failure_mode"] = "CODESIGN_FORCED_PAIR_EQUALITY"
    elif row["forced_basis_profiles_tested"]:
        row["best_failure_mode"] = "CODESIGN_COEFFICIENT_FULL_RANK"
    elif row["target_functional_present_modes"]:
        row["best_failure_mode"] = "CODESIGN_NO_STABLE_TARGET_BASIS"
    elif row["target_functional_missing_modes"]:
        row["best_failure_mode"] = "CODESIGN_TARGET_FUNCTIONAL_MISSING"
    else:
        row["best_failure_mode"] = "CODESIGN_NO_TARGET_MODES"
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "template_family",
        "assignment_strategy",
        "assignment_seed",
        "support_vector",
        "pair7_counts",
        "max_pair_count",
        "selected_class_size_counts",
        "coordinate_classes_hash",
        "functional_classes",
        "functional_span_rank",
        "forced_functional_identities",
        "structural_status",
        "forced_basis_modes_tested",
        "target_functional_present_modes",
        "target_functional_missing_modes",
        "forced_basis_combinations",
        "forced_basis_profiles_tested",
        "coefficient_kernel_profiles",
        "pair_projection_clear_profiles",
        "proxy_results_tested",
        "proxy_positive_profiles",
        "effective_cost",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_record(max_specs: int, stable_basis_limit: int, max_proxy_candidates: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    _profiles, candidates = joint.build_candidates(max_specs=max_specs)
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
        proof_status = "CANDIDATE / CODESIGN_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "CODESIGN_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = min(proxy_ranked, key=lambda row: row["best_profile"]["proxy_result"]["proxy_rank"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / CODESIGN_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "CODESIGN_PROXY_FULL_RANK"
    elif pair_clear:
        best = max(pair_clear, key=lambda row: row["pair_projection_clear_profiles"])
        proof_status = "CANDIDATE / CODESIGN_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "CODESIGN_PROXY_PENDING"
    elif coefficient_kernel:
        best = min(
            coefficient_kernel,
            key=lambda row: (
                row["best_profile"]["best_forced_pair_count"] if row["best_profile"] else 99,
                -row["coefficient_kernel_profiles"],
                row["template_id"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / CODESIGN_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        failure = "CODESIGN_FORCED_PAIR_EQUALITY"
    elif rows:
        best = max(rows, key=lambda row: (row["forced_basis_profiles_tested"], row["functional_span_rank"], row["template_id"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / CODESIGN_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "CODESIGN_COEFFICIENT_FULL_RANK"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / CODESIGN_NO_CANDIDATES / PARTIAL / EXPERIMENTAL"
        failure = "CODESIGN_NO_CANDIDATES"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_basis_forcing": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "forced_basis_profiles_tested": previous["basis_forcing_search"]["forced_basis_profiles_tested"],
            "coefficient_kernel_profiles": previous["basis_forcing_search"]["coefficient_kernel_profiles"],
            "best_failure_mode": previous["basis_forcing_search"]["best_failure_mode"],
        },
        "basis_kernel_codesign": {
            "max_specs": max_specs,
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
    parser.add_argument("--max-specs", type=int, default=36)
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
        search = record["basis_kernel_codesign"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
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
        print("M1_A327_BASIS_KERNEL_CODESIGN_READY")


if __name__ == "__main__":
    main()
