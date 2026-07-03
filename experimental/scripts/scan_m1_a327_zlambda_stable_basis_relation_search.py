#!/usr/bin/env python3
"""Search stable-basis right-kernel relations before proxy quotient rank."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "06d5270"
PREVIOUS_DATA = Path("experimental/data/m1_a327_zlambda_stable_right_kernel_generator.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_zlambda_stable_basis_relation_search.json")

ROOT = Path(__file__).resolve().parents[2]
JOINT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py"
ZSTABLE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_zlambda_stable_right_kernel_generator.py"

TARGET_AGREEMENT = 327
P = 17
PROXY_PRIME = 12289
K = 256


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


joint = load_module("joint_template_right_kernel_search", JOINT_SCRIPT)
zstable = load_module("zlambda_stable_right_kernel_generator", ZSTABLE_SCRIPT)
functional = joint.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def stable_combo_front(classes: list[dict[str, Any]], limit: int) -> tuple[int, list[tuple[int, tuple[int, ...]]]]:
    positions = zstable.class_position_sets(classes)
    rows = []
    stable_total = 0
    for combo in itertools.combinations(range(len(classes)), 6):
        union_size = len(set().union(*(positions[int(classes[idx]["class_index"])] for idx in combo)))
        if union_size > K - 1:
            continue
        stable_total += 1
        support_sum = sum(int(classes[idx]["support_size"]) for idx in combo)
        rows.append((union_size, -support_sum, combo))
    rows.sort()
    return stable_total, [(union_size, combo) for union_size, _support_sum, combo in rows[:limit]]


def summarize_relation_profile(candidate: dict[str, Any], classes: list[dict[str, Any]], profile: dict[str, Any], run_proxy: bool) -> dict[str, Any]:
    positions = zstable.class_position_sets(classes)
    matrix = zstable.coefficient_matrix(profile)
    rank17 = joint.right_kernel.rank_rows(matrix, ncols=6, prime=P)
    rank_proxy_coeff = functional.rank_mod_prime_matrix(matrix, ncols=6, prime=PROXY_PRIME)
    union_size = zstable.profile_union_size(profile, positions)
    pair_record = (
        zstable.pair_projection_record(candidate, profile)
        if rank17 < 6
        else {
            "kernel_basis": [],
            "best_forced_pair_count": None,
            "best_forced_pairs": None,
            "best_pair_projection_scalars": None,
        }
    )
    failure = "ZREL_STABLE_RELATION_TARGET"
    if rank17 == 6:
        failure = "ZREL_STABLE_COEFFICIENT_FULL_RANK"
    elif pair_record["best_forced_pair_count"] and pair_record["best_forced_pair_count"] > 0:
        failure = "ZREL_FORCED_PAIR_EQUALITY"
    proxy = None
    if run_proxy and failure == "ZREL_STABLE_RELATION_TARGET":
        proxy_result = functional.proxy_basis_rank(classes, profile)
        proxy = {
            "matrix_shape": proxy_result["proxy_matrix_shape"],
            "proxy_field": proxy_result["proxy_field"],
            "proxy_rank": proxy_result["proxy_rank"],
            "proxy_nullity": proxy_result["proxy_nullity"],
        }
        if proxy["proxy_nullity"] > 0:
            failure = "ZREL_PROXY_NULLITY_POSITIVE"
        else:
            failure = "ZREL_PROXY_FULL_RANK"
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "q_variable_count": profile["q_variable_count"],
        "coefficient_matrix_shape": [len(matrix), 6],
        "coefficient_rank_gf17": rank17,
        "coefficient_nullity_gf17": 6 - rank17,
        "coefficient_rank_gf12289": rank_proxy_coeff,
        "coefficient_nullity_gf12289": 6 - rank_proxy_coeff,
        "basis_zero_union_size": union_size,
        "stable_common_multiplier_dimension": K - union_size,
        "basis_zero_union_hash": hash_payload(sorted(set().union(*(positions[int(idx)] for idx in profile["basis_class_indices"])))),
        **pair_record,
        "proxy_result": proxy,
        "best_failure_mode": failure,
    }


def analyze_candidate(candidate: dict[str, Any], stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    classes = functional.functional_classes(candidate)
    row["stable_basis_combinations"] = 0
    row["stable_basis_profiles_tested"] = 0
    row["stable_coefficient_kernel_profiles"] = 0
    row["pair_projection_clear_profiles"] = 0
    row["proxy_results_tested"] = 0
    row["proxy_positive_profiles"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = zstable.mapped_structural_failure(row["structural_status"]).replace("ZSTABLE", "ZREL")
        return row

    stable_total, front = stable_combo_front(classes, limit=stable_basis_limit)
    row["stable_basis_combinations"] = stable_total
    summaries = []
    valid_profiles = 0
    for union_size, combo in front:
        profile = zstable.profile_from_combo(
            classes,
            combo,
            f"zrel_union_{union_size}_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
        )
        if profile is None:
            continue
        valid_profiles += 1
        summary = summarize_relation_profile(candidate, classes, profile, run_proxy=run_proxy)
        if summary["coefficient_nullity_gf17"] <= 0:
            continue
        summaries.append(summary)
        if summary["best_failure_mode"] in {"ZREL_PROXY_NULLITY_POSITIVE", "ZREL_PROXY_FULL_RANK"}:
            row["proxy_results_tested"] += 1
        if summary["best_failure_mode"] == "ZREL_PROXY_NULLITY_POSITIVE":
            row["proxy_positive_profiles"] += 1
            break
    row["stable_basis_profiles_tested"] = valid_profiles
    row["stable_coefficient_kernel_profiles"] = len(summaries)
    row["pair_projection_clear_profiles"] = sum(
        1 for item in summaries if item["best_failure_mode"] in {"ZREL_STABLE_RELATION_TARGET", "ZREL_PROXY_FULL_RANK", "ZREL_PROXY_NULLITY_POSITIVE"}
    )
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["best_failure_mode"] == "ZREL_PROXY_NULLITY_POSITIVE",
            item["best_failure_mode"] == "ZREL_PROXY_FULL_RANK",
            item["best_failure_mode"] == "ZREL_STABLE_RELATION_TARGET",
            item["stable_common_multiplier_dimension"],
            -(item["best_forced_pair_count"] if item["best_forced_pair_count"] is not None else 99),
            item["coefficient_nullity_gf17"],
        ),
        reverse=True,
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_positive_profiles"]:
        row["best_failure_mode"] = "ZREL_PROXY_NULLITY_POSITIVE"
    elif any(item["best_failure_mode"] == "ZREL_PROXY_FULL_RANK" for item in summaries):
        row["best_failure_mode"] = "ZREL_PROXY_FULL_RANK"
    elif row["pair_projection_clear_profiles"]:
        row["best_failure_mode"] = "ZREL_PROXY_PENDING"
    elif row["stable_coefficient_kernel_profiles"]:
        row["best_failure_mode"] = "ZREL_FORCED_PAIR_EQUALITY"
    else:
        row["best_failure_mode"] = "ZREL_STABLE_COEFFICIENT_FULL_RANK"
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
        "stable_coefficient_kernel_profiles",
        "pair_projection_clear_profiles",
        "proxy_results_tested",
        "proxy_positive_profiles",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row[key] for key in keys}


def build_record(max_specs: int, stable_basis_limit: int, max_proxy_candidates: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    _profiles, raw_candidates = joint.build_candidates(max_specs=max_specs)
    cheap_rows = [analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=False) for candidate in raw_candidates]
    proxy_indices = [
        idx
        for idx, row in sorted(
            enumerate(cheap_rows),
            key=lambda item: (
                item[1]["pair_projection_clear_profiles"],
                item[1]["stable_coefficient_kernel_profiles"],
                item[1]["stable_basis_profiles_tested"],
            ),
            reverse=True,
        )
        if row["pair_projection_clear_profiles"] > 0
    ][:max_proxy_candidates]
    rows = list(cheap_rows)
    for idx in proxy_indices:
        rows[idx] = analyze_candidate(raw_candidates[idx], stable_basis_limit=stable_basis_limit, run_proxy=True)

    proxy_positive = [row for row in rows if row["proxy_positive_profiles"] > 0]
    proxy_ranked = [row for row in rows if row["proxy_results_tested"] > 0]
    pair_clear = [row for row in rows if row["pair_projection_clear_profiles"] > 0]
    coefficient_kernel = [row for row in rows if row["stable_coefficient_kernel_profiles"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / ZREL_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "ZREL_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = min(proxy_ranked, key=lambda row: row["best_profile"]["proxy_result"]["proxy_rank"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZREL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "ZREL_PROXY_FULL_RANK"
    elif pair_clear:
        best = max(pair_clear, key=lambda row: row["pair_projection_clear_profiles"])
        proof_status = "CANDIDATE / ZREL_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "ZREL_PROXY_PENDING"
    elif coefficient_kernel:
        best = max(coefficient_kernel, key=lambda row: row["stable_coefficient_kernel_profiles"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZREL_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        failure = "ZREL_FORCED_PAIR_EQUALITY"
    elif rows:
        best = max(rows, key=lambda row: (row["stable_basis_profiles_tested"], row["functional_span_rank"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZREL_STABLE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "ZREL_STABLE_COEFFICIENT_FULL_RANK"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZREL_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "ZREL_SUPPORT_FAIL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_zlambda_stable_generator": {
            "commit": SOURCE_COMMIT,
            "systems_tested": previous["zlambda_stable_generator"]["systems_tested"],
            "basis_profiles_tested": previous["zlambda_stable_generator"]["basis_profiles_tested"],
            "coefficient_kernel_profiles": previous["zlambda_stable_generator"]["coefficient_kernel_profiles"],
            "stable_basis_union_profiles": previous["zlambda_stable_generator"]["stable_basis_union_profiles"],
            "best_failure_mode": previous["zlambda_stable_generator"]["best_failure_mode"],
        },
        "stable_basis_relation_search": {
            "templates_tested": max_specs,
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "stable_basis_combinations": sum(row["stable_basis_combinations"] for row in rows),
            "stable_basis_profiles_tested": sum(row["stable_basis_profiles_tested"] for row in rows),
            "stable_coefficient_kernel_profiles": sum(row["stable_coefficient_kernel_profiles"] for row in rows),
            "pair_projection_clear_profiles": sum(row["pair_projection_clear_profiles"] for row in rows),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_positive_candidates": len(proxy_positive),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_zero_union_size": None if best is None or best["best_profile"] is None else best["best_profile"]["basis_zero_union_size"],
            "best_stable_common_multiplier_dimension": None if best is None or best["best_profile"] is None else best["best_profile"]["stable_common_multiplier_dimension"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["best_forced_pair_count"],
            "best_proxy_rank": None if best is None or best["best_profile"] is None or best["best_profile"]["proxy_result"] is None else best["best_profile"]["proxy_result"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_profile"] is None or best["best_profile"]["proxy_result"] is None else best["best_profile"]["proxy_result"]["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
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
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-specs", type=int, default=36)
    parser.add_argument("--stable-basis-limit", type=int, default=512)
    parser.add_argument("--max-proxy-candidates", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        max_specs=args.max_specs,
        stable_basis_limit=args.stable_basis_limit,
        max_proxy_candidates=args.max_proxy_candidates,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["stable_basis_relation_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "stable_basis_combinations": search["stable_basis_combinations"],
                    "stable_basis_profiles_tested": search["stable_basis_profiles_tested"],
                    "stable_coefficient_kernel_profiles": search["stable_coefficient_kernel_profiles"],
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
        print("M1_A327_ZLAMBDA_STABLE_BASIS_RELATION_SEARCH_READY")


if __name__ == "__main__":
    main()
