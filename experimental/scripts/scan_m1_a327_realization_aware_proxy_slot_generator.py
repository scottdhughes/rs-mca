#!/usr/bin/env python3
"""Search actual-template proxy-slot kernels without synthetic rowspace edits."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "8032816"
PREVIOUS_DATA = Path("experimental/data/m1_a327_proxy_slot_template_realization.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_realization_aware_proxy_slot_generator.json")

ROOT = Path(__file__).resolve().parents[2]
PROXY_SLOT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_proxy_slot_kernel_generator.py"

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


pslot = load_module("proxy_slot_kernel_generator", PROXY_SLOT_SCRIPT)
joint = pslot.joint
zstable = pslot.zstable
functional = pslot.functional


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def actual_slot_summary(
    candidate: dict[str, Any],
    classes: list[dict[str, Any]],
    profile: dict[str, Any],
    slot: int,
    run_proxy: bool,
) -> dict[str, Any]:
    positions = zstable.class_position_sets(classes)
    matrix = zstable.coefficient_matrix(profile)
    slot_nonzero_rows = sum(1 for row in matrix if int(row[slot]) % P)
    pair_record = pslot.pair_projection_for_slot(candidate, profile, slot)
    union_size = zstable.profile_union_size(profile, positions)
    q_degree = K - int(profile["basis_support_sizes"][slot])
    coefficient_rank = joint.right_kernel.rank_rows(matrix, ncols=6, prime=P)
    failure = "RAWARE_ACTUAL_PROXY_SLOT_TARGET"
    if slot_nonzero_rows:
        failure = "RAWARE_SLOT_NOT_KERNEL"
    elif pair_record["forced_pair_count"] > 0:
        failure = "RAWARE_FORCED_PAIR_EQUALITY"
    proxy = None
    if run_proxy and failure == "RAWARE_ACTUAL_PROXY_SLOT_TARGET":
        proxy_result = functional.proxy_basis_rank(classes, profile)
        proxy = {
            "proxy_field": proxy_result["proxy_field"],
            "proxy_matrix_shape": proxy_result["proxy_matrix_shape"],
            "proxy_rank": proxy_result["proxy_rank"],
            "proxy_nullity": proxy_result["proxy_nullity"],
        }
        if proxy["proxy_nullity"] > 0:
            failure = "RAWARE_PROXY_NULLITY_POSITIVE"
        else:
            failure = "RAWARE_PROXY_FULL_RANK"
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "proxy_kernel_slot": slot,
        "proxy_kernel_vector": [1 if idx == slot else 0 for idx in range(6)],
        "basis_zero_union_size": union_size,
        "stable_common_multiplier_dimension": K - union_size,
        "q_variable_count": profile["q_variable_count"],
        "proxy_kernel_block_degree": q_degree,
        "coefficient_matrix_shape": [len(matrix), 6],
        "coefficient_rank": coefficient_rank,
        "coefficient_nullity": 6 - coefficient_rank,
        "slot_nonzero_rows": slot_nonzero_rows,
        "actual_template_realized": True,
        **pair_record,
        "proxy_result": proxy,
        "best_failure_mode": failure,
    }


def analyze_candidate(candidate: dict[str, Any], stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    classes = functional.functional_classes(candidate)
    row["stable_basis_combinations"] = 0
    row["stable_basis_profiles_tested"] = 0
    row["slot_profiles_tested"] = 0
    row["actual_zero_slot_profiles"] = 0
    row["pair_projection_clear_actual_slots"] = 0
    row["proxy_positive_actual_slots"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = zstable.mapped_structural_failure(row["structural_status"]).replace("ZSTABLE", "RAWARE")
        return row

    stable_total, profiles = pslot.stable_profiles_for_candidate(classes, limit=stable_basis_limit)
    row["stable_basis_combinations"] = stable_total
    row["stable_basis_profiles_tested"] = len(profiles)
    summaries = []
    for profile in profiles:
        for slot in range(6):
            summaries.append(actual_slot_summary(candidate, classes, profile, slot, run_proxy=run_proxy))
    row["slot_profiles_tested"] = len(summaries)
    row["actual_zero_slot_profiles"] = sum(1 for item in summaries if item["slot_nonzero_rows"] == 0)
    row["pair_projection_clear_actual_slots"] = sum(
        1 for item in summaries if item["slot_nonzero_rows"] == 0 and item["forced_pair_count"] == 0
    )
    row["proxy_positive_actual_slots"] = sum(1 for item in summaries if item["best_failure_mode"] == "RAWARE_PROXY_NULLITY_POSITIVE")
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["best_failure_mode"] == "RAWARE_PROXY_NULLITY_POSITIVE",
            item["best_failure_mode"] == "RAWARE_ACTUAL_PROXY_SLOT_TARGET",
            -item["slot_nonzero_rows"],
            item["proxy_kernel_block_degree"],
            -item["forced_pair_count"],
            item["stable_common_multiplier_dimension"],
        ),
        reverse=True,
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_positive_actual_slots"]:
        row["best_failure_mode"] = "RAWARE_PROXY_NULLITY_POSITIVE"
    elif row["pair_projection_clear_actual_slots"]:
        row["best_failure_mode"] = "RAWARE_ACTUAL_PROXY_SLOT_TARGET"
    elif row["actual_zero_slot_profiles"]:
        row["best_failure_mode"] = "RAWARE_FORCED_PAIR_EQUALITY"
    elif summaries:
        row["best_failure_mode"] = "RAWARE_SLOT_NOT_KERNEL"
    else:
        row["best_failure_mode"] = "RAWARE_NO_STABLE_BASIS"
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
        "slot_profiles_tested",
        "actual_zero_slot_profiles",
        "pair_projection_clear_actual_slots",
        "proxy_positive_actual_slots",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row[key] for key in keys}


def build_record(max_specs: int, stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    _profiles, raw_candidates = joint.build_candidates(max_specs=max_specs)
    rows = [analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=run_proxy) for candidate in raw_candidates]
    proxy_positive = [row for row in rows if row["proxy_positive_actual_slots"] > 0]
    zero_slots = [row for row in rows if row["actual_zero_slot_profiles"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / RAWARE_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "RAWARE_PROXY_NULLITY_POSITIVE"
    elif zero_slots:
        best = max(zero_slots, key=lambda row: row["pair_projection_clear_actual_slots"])
        proof_status = "CANDIDATE / RAWARE_ACTUAL_PROXY_SLOT_TARGET / PARTIAL / EXPERIMENTAL"
        failure = "RAWARE_ACTUAL_PROXY_SLOT_TARGET"
    elif rows:
        best = min(
            rows,
            key=lambda row: (
                row["best_profile"]["slot_nonzero_rows"] if row["best_profile"] else 999,
                -row["slot_profiles_tested"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / RAWARE_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "RAWARE_SLOT_NOT_KERNEL"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / RAWARE_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "RAWARE_SUPPORT_FAIL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_template_realization": {
            "commit": SOURCE_COMMIT,
            "target_template_id": previous["proxy_slot_target"]["template_id"],
            "proxy_rank": previous["proxy_slot_target"]["proxy_rank"],
            "proxy_nullity": previous["proxy_slot_target"]["proxy_nullity"],
            "linear_rank": previous["template_realization"]["linear_rank"],
            "linear_nullity": previous["template_realization"]["linear_nullity"],
            "rowspace_valid_samples": previous["template_realization"]["rowspace_valid_samples"],
            "best_failure_mode": previous["template_realization"]["best_failure_mode"],
        },
        "realization_aware_search": {
            "templates_tested": max_specs,
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "stable_basis_combinations": sum(row["stable_basis_combinations"] for row in rows),
            "stable_basis_profiles_tested": sum(row["stable_basis_profiles_tested"] for row in rows),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in rows),
            "actual_zero_slot_profiles": sum(row["actual_zero_slot_profiles"] for row in rows),
            "pair_projection_clear_actual_slots": sum(row["pair_projection_clear_actual_slots"] for row in rows),
            "proxy_positive_actual_slots": sum(row["proxy_positive_actual_slots"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_slot_nonzero_rows": None if best is None or best["best_profile"] is None else best["best_profile"]["slot_nonzero_rows"],
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
    parser.add_argument("--stable-basis-limit", type=int, default=128)
    parser.add_argument("--run-proxy", action="store_true")
    args = parser.parse_args()
    record = build_record(max_specs=args.max_specs, stable_basis_limit=args.stable_basis_limit, run_proxy=args.run_proxy)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["realization_aware_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "actual_zero_slot_profiles": search["actual_zero_slot_profiles"],
                    "pair_projection_clear_actual_slots": search["pair_projection_clear_actual_slots"],
                    "proxy_positive_actual_slots": search["proxy_positive_actual_slots"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_REALIZATION_AWARE_PROXY_SLOT_GENERATOR_READY")


if __name__ == "__main__":
    main()
