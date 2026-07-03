#!/usr/bin/env python3
"""Prescribe Z_lambda-stable right-kernel relations before proxy quotient rank."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "9cc5e91"
PREVIOUS_DATA = Path("experimental/data/m1_a327_zlambda_stable_basis_relation_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_prescribed_zlambda_stable_relation_generator.json")

ROOT = Path(__file__).resolve().parents[2]
JOINT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py"
ZREL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_zlambda_stable_basis_relation_search.py"
ZSTABLE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_zlambda_stable_right_kernel_generator.py"
PRESCRIBED_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_right_kernel_selected_class_search.py"

TARGET_AGREEMENT = 327
P = 17
K = 256


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


joint = load_module("joint_template_right_kernel_search", JOINT_SCRIPT)
zrel = load_module("zlambda_stable_basis_relation_search", ZREL_SCRIPT)
zstable = load_module("zlambda_stable_right_kernel_generator", ZSTABLE_SCRIPT)
prescribed = load_module("prescribed_right_kernel_selected_class_search", PRESCRIBED_SCRIPT)
functional = joint.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def pair_projection_for_kernel(candidate: dict[str, Any], profile: dict[str, Any], kernel: list[int]) -> dict[str, Any]:
    scalars = {}
    basis_rows = profile["basis_functionals"]
    for left in range(1, 8):
        for right in range(left + 1, 8):
            diff = [
                (int(candidate["template_vectors"][left - 1][idx]) - int(candidate["template_vectors"][right - 1][idx])) % P
                for idx in range(len(candidate["template_vectors"][0]))
            ]
            coords = functional.solve_coordinates(diff, basis_rows)
            if coords is None:
                raise RuntimeError(f"pair P{left}{right} not in basis span")
            scalars[f"P{left}{right}"] = sum(int(coords[idx]) * int(kernel[idx]) for idx in range(len(coords))) % P
    forced = [label for label, value in scalars.items() if value == 0]
    return {
        "forced_pair_count": len(forced),
        "forced_pairs": forced,
        "pair_projection_scalars": scalars,
    }


def stable_profiles_for_candidate(classes: list[dict[str, Any]], limit: int) -> tuple[int, list[dict[str, Any]]]:
    stable_total, front = zrel.stable_combo_front(classes, limit=limit)
    profiles = []
    seen: set[tuple[int, ...]] = set()
    for union_size, combo in front:
        profile = zstable.profile_from_combo(
            classes,
            combo,
            f"pzrel_union_{union_size}_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        profiles.append(profile)
    return stable_total, profiles


def engineered_stable_profile(
    candidate: dict[str, Any],
    classes: list[dict[str, Any]],
    profile: dict[str, Any],
    kernel: dict[str, Any],
    run_proxy: bool,
) -> dict[str, Any]:
    kernel_vector = [int(value) % P for value in kernel["kernel_vector"]]
    pair_record = pair_projection_for_kernel(candidate, profile, kernel_vector)
    engineered = prescribed.engineer_profile(profile, kernel)
    positions = zstable.class_position_sets(classes)
    union_size = zstable.profile_union_size(profile, positions)
    failure = "PZREL_STABLE_RELATION_TARGET"
    if pair_record["forced_pair_count"] > 0:
        failure = "PZREL_FORCED_PAIR_EQUALITY"
    proxy = None
    if run_proxy and failure == "PZREL_STABLE_RELATION_TARGET":
        result = functional.proxy_basis_rank(classes, engineered)
        proxy = {
            "matrix_shape": result["proxy_matrix_shape"],
            "proxy_field": result["proxy_field"],
            "proxy_rank": result["proxy_rank"],
            "proxy_nullity": result["proxy_nullity"],
        }
        if proxy["proxy_nullity"] > 0:
            failure = "PZREL_PROXY_NULLITY_POSITIVE"
        else:
            failure = "PZREL_PROXY_FULL_RANK"
    return {
        "basis_id": engineered["basis_id"],
        "source_basis_id": engineered["source_basis_id"],
        "prescribed_kernel_id": engineered["prescribed_kernel_id"],
        "prescribed_kernel_vector": engineered["prescribed_kernel_vector"],
        "basis_class_indices": engineered["basis_class_indices"],
        "basis_support_sizes": engineered["basis_support_sizes"],
        "q_variable_count": engineered["q_variable_count"],
        "coefficient_matrix_shape": [len(engineered["nonbasis_constraint_detail"]), 6],
        "coefficient_rank": engineered["coefficient_rank"],
        "right_kernel_nullity": engineered["right_kernel_nullity"],
        "right_kernel_verified": engineered["right_kernel_verified"],
        "coordinate_rows_changed": engineered["coordinate_rows_changed"],
        "basis_zero_union_size": union_size,
        "stable_common_multiplier_dimension": K - union_size,
        **pair_record,
        "proxy_result": proxy,
        "best_failure_mode": failure,
    }


def analyze_candidate(
    candidate: dict[str, Any],
    kernels: list[dict[str, Any]],
    stable_basis_limit: int,
    profile_limit: int,
    run_proxy: bool,
) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    classes = functional.functional_classes(candidate)
    row["stable_basis_combinations"] = 0
    row["stable_basis_profiles_tested"] = 0
    row["engineered_profiles_tested"] = 0
    row["pair_projection_clear_profiles"] = 0
    row["proxy_results_tested"] = 0
    row["proxy_positive_profiles"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = zstable.mapped_structural_failure(row["structural_status"]).replace("ZSTABLE", "PZREL")
        return row

    stable_total, profiles = stable_profiles_for_candidate(classes, limit=stable_basis_limit)
    row["stable_basis_combinations"] = stable_total
    row["stable_basis_profiles_tested"] = len(profiles)
    summaries = []
    for profile in profiles[:profile_limit]:
        for kernel in kernels:
            summary = engineered_stable_profile(candidate, classes, profile, kernel, run_proxy=run_proxy)
            summaries.append(summary)
            if summary["best_failure_mode"] in {"PZREL_PROXY_NULLITY_POSITIVE", "PZREL_PROXY_FULL_RANK"}:
                row["proxy_results_tested"] += 1
            if summary["best_failure_mode"] == "PZREL_PROXY_NULLITY_POSITIVE":
                row["proxy_positive_profiles"] += 1
                break
        if row["proxy_positive_profiles"]:
            break

    row["engineered_profiles_tested"] = len(summaries)
    row["pair_projection_clear_profiles"] = sum(
        1 for item in summaries if item["best_failure_mode"] in {"PZREL_STABLE_RELATION_TARGET", "PZREL_PROXY_FULL_RANK", "PZREL_PROXY_NULLITY_POSITIVE"}
    )
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["best_failure_mode"] == "PZREL_PROXY_NULLITY_POSITIVE",
            item["best_failure_mode"] == "PZREL_PROXY_FULL_RANK",
            item["best_failure_mode"] == "PZREL_STABLE_RELATION_TARGET",
            -item["forced_pair_count"],
            item["right_kernel_nullity"],
            item["stable_common_multiplier_dimension"],
        ),
        reverse=True,
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_positive_profiles"]:
        row["best_failure_mode"] = "PZREL_PROXY_NULLITY_POSITIVE"
    elif any(item["best_failure_mode"] == "PZREL_PROXY_FULL_RANK" for item in summaries):
        row["best_failure_mode"] = "PZREL_PROXY_FULL_RANK"
    elif row["pair_projection_clear_profiles"]:
        row["best_failure_mode"] = "PZREL_PROXY_PENDING"
    elif summaries:
        row["best_failure_mode"] = "PZREL_FORCED_PAIR_EQUALITY"
    else:
        row["best_failure_mode"] = "PZREL_NO_STABLE_BASIS"
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
        "stable_basis_combinations",
        "stable_basis_profiles_tested",
        "engineered_profiles_tested",
        "pair_projection_clear_profiles",
        "proxy_results_tested",
        "proxy_positive_profiles",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row[key] for key in keys}


def build_record(max_specs: int, stable_basis_limit: int, profile_limit: int, max_random_kernels: int, max_proxy_candidates: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    kernels = prescribed.kernel_specs(max_random=max_random_kernels)
    _profiles, raw_candidates = joint.build_candidates(max_specs=max_specs)
    cheap_rows = [
        analyze_candidate(
            candidate,
            kernels=kernels,
            stable_basis_limit=stable_basis_limit,
            profile_limit=profile_limit,
            run_proxy=False,
        )
        for candidate in raw_candidates
    ]
    proxy_indices = [
        idx
        for idx, row in sorted(
            enumerate(cheap_rows),
            key=lambda item: (
                item[1]["pair_projection_clear_profiles"],
                item[1]["engineered_profiles_tested"],
                item[1]["stable_basis_profiles_tested"],
            ),
            reverse=True,
        )
        if row["pair_projection_clear_profiles"] > 0
    ][:max_proxy_candidates]
    rows = list(cheap_rows)
    for idx in proxy_indices:
        rows[idx] = analyze_candidate(
            raw_candidates[idx],
            kernels=kernels,
            stable_basis_limit=stable_basis_limit,
            profile_limit=profile_limit,
            run_proxy=True,
        )

    proxy_positive = [row for row in rows if row["proxy_positive_profiles"] > 0]
    proxy_ranked = [row for row in rows if row["proxy_results_tested"] > 0]
    pair_clear = [row for row in rows if row["pair_projection_clear_profiles"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / PZREL_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "PZREL_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = min(proxy_ranked, key=lambda row: row["best_profile"]["proxy_result"]["proxy_rank"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / PZREL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "PZREL_PROXY_FULL_RANK"
    elif pair_clear:
        best = max(pair_clear, key=lambda row: row["pair_projection_clear_profiles"])
        proof_status = "CANDIDATE / PZREL_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "PZREL_PROXY_PENDING"
    elif rows:
        best = max(rows, key=lambda row: (row["engineered_profiles_tested"], row["stable_basis_profiles_tested"], row["functional_span_rank"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / PZREL_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        failure = "PZREL_FORCED_PAIR_EQUALITY"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / PZREL_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "PZREL_SUPPORT_FAIL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_stable_basis_relation_search": {
            "commit": SOURCE_COMMIT,
            "systems_tested": previous["stable_basis_relation_search"]["systems_tested"],
            "stable_basis_profiles_tested": previous["stable_basis_relation_search"]["stable_basis_profiles_tested"],
            "stable_coefficient_kernel_profiles": previous["stable_basis_relation_search"]["stable_coefficient_kernel_profiles"],
            "best_failure_mode": previous["stable_basis_relation_search"]["best_failure_mode"],
        },
        "prescribed_stable_relation": {
            "templates_tested": max_specs,
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "stable_basis_combinations": sum(row["stable_basis_combinations"] for row in rows),
            "stable_basis_profiles_tested": sum(row["stable_basis_profiles_tested"] for row in rows),
            "engineered_profiles_tested": sum(row["engineered_profiles_tested"] for row in rows),
            "pair_projection_clear_profiles": sum(row["pair_projection_clear_profiles"] for row in rows),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_positive_candidates": len(proxy_positive),
            "kernel_ids_tested": [row["kernel_id"] for row in kernels],
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_zero_union_size": None if best is None or best["best_profile"] is None else best["best_profile"]["basis_zero_union_size"],
            "best_stable_common_multiplier_dimension": None if best is None or best["best_profile"] is None else best["best_profile"]["stable_common_multiplier_dimension"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["forced_pair_count"],
            "best_proxy_rank": None if best is None or best["best_profile"] is None or best["best_profile"]["proxy_result"] is None else best["best_profile"]["proxy_result"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_profile"] is None or best["best_profile"]["proxy_result"] is None else best["best_profile"]["proxy_result"]["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "SYNTHETIC_FUNCTIONAL_PROXY_TARGET",
        "realization_note": (
            "Stable basis supports and selected-class ledgers come from actual template candidates, "
            "but nonbasis coordinates are projected into a prescribed right-kernel hyperplane. "
            "Actual template-vector realization remains a separate gate."
        ),
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
            "realized exact template vectors for the prescribed coefficients",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-specs", type=int, default=36)
    parser.add_argument("--stable-basis-limit", type=int, default=128)
    parser.add_argument("--profile-limit", type=int, default=16)
    parser.add_argument("--max-random-kernels", type=int, default=8)
    parser.add_argument("--max-proxy-candidates", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        max_specs=args.max_specs,
        stable_basis_limit=args.stable_basis_limit,
        profile_limit=args.profile_limit,
        max_random_kernels=args.max_random_kernels,
        max_proxy_candidates=args.max_proxy_candidates,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["prescribed_stable_relation"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "realization_status": record["realization_status"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "engineered_profiles_tested": search["engineered_profiles_tested"],
                    "pair_projection_clear_profiles": search["pair_projection_clear_profiles"],
                    "proxy_candidates_tested": search["proxy_candidates_tested"],
                    "proxy_positive_candidates": search["proxy_positive_candidates"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_basis_zero_union_size": search["best_basis_zero_union_size"],
                    "best_stable_common_multiplier_dimension": search["best_stable_common_multiplier_dimension"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
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
        print("M1_A327_PRESCRIBED_ZLAMBDA_STABLE_RELATION_GENERATOR_READY")


if __name__ == "__main__":
    main()
