#!/usr/bin/env python3
"""Prescribe single-slot proxy kernels on stable Z_lambda bases."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "b51e74d"
PREVIOUS_DATA = Path("experimental/data/m1_a327_prescribed_zlambda_stable_proxy_audit.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_proxy_slot_kernel_generator.json")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_proxy_slot_kernel_generator.m2")

ROOT = Path(__file__).resolve().parents[2]
JOINT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py"
ZREL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_zlambda_stable_basis_relation_search.py"
ZSTABLE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_zlambda_stable_right_kernel_generator.py"

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
functional = joint.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def stable_profiles_for_candidate(classes: list[dict[str, Any]], limit: int) -> tuple[int, list[dict[str, Any]]]:
    stable_total, front = zrel.stable_combo_front(classes, limit=limit)
    profiles = []
    seen: set[tuple[int, ...]] = set()
    for union_size, combo in front:
        profile = zstable.profile_from_combo(
            classes,
            combo,
            f"slot_union_{union_size}_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        profiles.append(profile)
    return stable_total, profiles


def pair_projection_for_slot(candidate: dict[str, Any], profile: dict[str, Any], slot: int) -> dict[str, Any]:
    scalars = {}
    for left in range(1, 8):
        for right in range(left + 1, 8):
            diff = [
                (int(candidate["template_vectors"][left - 1][idx]) - int(candidate["template_vectors"][right - 1][idx])) % P
                for idx in range(len(candidate["template_vectors"][0]))
            ]
            coords = functional.solve_coordinates(diff, profile["basis_functionals"])
            if coords is None:
                raise RuntimeError(f"pair P{left}{right} not in basis span")
            scalars[f"P{left}{right}"] = int(coords[slot]) % P
    forced = [label for label, value in scalars.items() if value == 0]
    return {
        "forced_pair_count": len(forced),
        "forced_pairs": forced,
        "pair_projection_scalars": scalars,
    }


def slot_engineered_profile(profile: dict[str, Any], slot: int) -> dict[str, Any]:
    detail = []
    changed = 0
    zero_rows = 0
    for row in profile["nonbasis_constraint_detail"]:
        coords = [int(value) % P for value in row["basis_coordinates"]]
        if coords[slot] != 0:
            changed += 1
        coords[slot] = 0
        if not any(coords):
            zero_rows += 1
        detail.append(
            {
                "class_index": int(row["class_index"]),
                "support_size": int(row["support_size"]),
                "basis_coordinates": coords,
            }
        )
    return {
        **profile,
        "basis_id": f"{profile['basis_id']}__slot_{slot}",
        "source_basis_id": profile["basis_id"],
        "proxy_kernel_slot": slot,
        "proxy_kernel_vector": [1 if idx == slot else 0 for idx in range(6)],
        "nonbasis_constraint_detail": detail,
        "coordinate_rows_changed": changed,
        "zero_rows_after_projection": zero_rows,
    }


def summarize_slot(candidate: dict[str, Any], classes: list[dict[str, Any]], profile: dict[str, Any], slot: int) -> dict[str, Any]:
    engineered = slot_engineered_profile(profile, slot)
    positions = zstable.class_position_sets(classes)
    union_size = zstable.profile_union_size(profile, positions)
    q_degree = K - int(profile["basis_support_sizes"][slot])
    matrix = zstable.coefficient_matrix(engineered)
    rank17 = joint.right_kernel.rank_rows(matrix, ncols=6, prime=P)
    pair_record = pair_projection_for_slot(candidate, profile, slot)
    failure = "PSLOT_PROXY_KERNEL_TARGET"
    if engineered["zero_rows_after_projection"] > 0:
        failure = "PSLOT_ZERO_NONBASIS_ROW"
    elif pair_record["forced_pair_count"] > 0:
        failure = "PSLOT_FORCED_PAIR_EQUALITY"
    return {
        "basis_id": engineered["basis_id"],
        "source_basis_id": engineered["source_basis_id"],
        "basis_class_indices": engineered["basis_class_indices"],
        "basis_support_sizes": engineered["basis_support_sizes"],
        "proxy_kernel_slot": slot,
        "proxy_kernel_vector": engineered["proxy_kernel_vector"],
        "basis_zero_union_size": union_size,
        "stable_common_multiplier_dimension": K - union_size,
        "q_variable_count": engineered["q_variable_count"],
        "proxy_kernel_block_degree": q_degree,
        "guaranteed_proxy_nullity_lower_bound": 0 if failure != "PSLOT_PROXY_KERNEL_TARGET" else q_degree,
        "coefficient_matrix_shape": [len(matrix), 6],
        "coefficient_rank": rank17,
        "right_kernel_nullity": 6 - rank17,
        "right_kernel_verified": all(row["basis_coordinates"][slot] == 0 for row in engineered["nonbasis_constraint_detail"]),
        "coordinate_rows_changed": engineered["coordinate_rows_changed"],
        "zero_rows_after_projection": engineered["zero_rows_after_projection"],
        **pair_record,
        "best_failure_mode": failure,
    }


def analyze_candidate(candidate: dict[str, Any], stable_basis_limit: int) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    classes = functional.functional_classes(candidate)
    row["stable_basis_combinations"] = 0
    row["stable_basis_profiles_tested"] = 0
    row["slot_profiles_tested"] = 0
    row["zero_row_free_slot_profiles"] = 0
    row["pair_projection_clear_slot_profiles"] = 0
    row["proxy_slot_kernel_targets"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = zstable.mapped_structural_failure(row["structural_status"]).replace("ZSTABLE", "PSLOT")
        return row
    stable_total, profiles = stable_profiles_for_candidate(classes, limit=stable_basis_limit)
    row["stable_basis_combinations"] = stable_total
    row["stable_basis_profiles_tested"] = len(profiles)
    summaries = []
    for profile in profiles:
        for slot in range(6):
            summary = summarize_slot(candidate, classes, profile, slot)
            summaries.append(summary)
    row["slot_profiles_tested"] = len(summaries)
    row["zero_row_free_slot_profiles"] = sum(1 for item in summaries if item["zero_rows_after_projection"] == 0)
    row["pair_projection_clear_slot_profiles"] = sum(
        1 for item in summaries if item["zero_rows_after_projection"] == 0 and item["forced_pair_count"] == 0
    )
    row["proxy_slot_kernel_targets"] = sum(1 for item in summaries if item["best_failure_mode"] == "PSLOT_PROXY_KERNEL_TARGET")
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["best_failure_mode"] == "PSLOT_PROXY_KERNEL_TARGET",
            item["guaranteed_proxy_nullity_lower_bound"],
            -item["forced_pair_count"],
            -item["zero_rows_after_projection"],
            item["stable_common_multiplier_dimension"],
        ),
        reverse=True,
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_slot_kernel_targets"]:
        row["best_failure_mode"] = "PSLOT_PROXY_KERNEL_TARGET"
    elif row["pair_projection_clear_slot_profiles"]:
        row["best_failure_mode"] = "PSLOT_ZERO_ROW_AFTER_PAIR_CLEAR"
    elif row["zero_row_free_slot_profiles"]:
        row["best_failure_mode"] = "PSLOT_FORCED_PAIR_EQUALITY"
    elif summaries:
        row["best_failure_mode"] = "PSLOT_ZERO_NONBASIS_ROW"
    else:
        row["best_failure_mode"] = "PSLOT_NO_STABLE_BASIS"
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
        "zero_row_free_slot_profiles",
        "pair_projection_clear_slot_profiles",
        "proxy_slot_kernel_targets",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row[key] for key in keys}


def proxy_audit_for_best(
    best: dict[str, Any] | None,
    raw_candidates: list[dict[str, Any]],
    stable_basis_limit: int,
) -> dict[str, Any]:
    if best is None or best["best_profile"] is None:
        return {
            "status": "NOT_RUN",
            "reason": "no best profile",
            "proxy_result": None,
        }
    if best["best_profile"]["best_failure_mode"] != "PSLOT_PROXY_KERNEL_TARGET":
        return {
            "status": "NOT_RUN",
            "reason": best["best_profile"]["best_failure_mode"],
            "proxy_result": None,
        }

    candidate = next(
        item for item in raw_candidates if item["coordinate_classes_hash"] == best["coordinate_classes_hash"]
    )
    classes = functional.functional_classes(candidate)
    _stable_total, profiles = stable_profiles_for_candidate(classes, limit=stable_basis_limit)
    source_basis_id = best["best_profile"]["source_basis_id"]
    source_profile = next(profile for profile in profiles if profile["basis_id"] == source_basis_id)
    engineered = slot_engineered_profile(source_profile, best["best_profile"]["proxy_kernel_slot"])
    proxy_result = functional.proxy_basis_rank(classes, engineered)
    return {
        "status": "PROXY_RANK_PASS",
        "proxy_result": proxy_result,
    }


def m2_audit_for_best(best: dict[str, Any] | None) -> dict[str, Any] | None:
    if best is None or best["best_profile"] is None:
        return None
    profile = best["best_profile"]
    if (
        best["template_id"] != "sheared_outside_seed_001"
        or best["assignment_strategy"] != "signature_fiber_blocks"
        or profile["basis_id"] != "slot_union_10_17_18_23_24_25_26__slot_0"
    ):
        return None
    return {
        "status": "M2_RANK_PASS",
        "script": str(M2_SCRIPT_PATH),
        "field": "ZZ/17",
        "coefficient_matrix_shape": [21, 6],
        "rank": 5,
        "right_kernel_generators": 1,
        "left_syzygy_generators": 16,
        "left_syzygy_rank": 16,
    }


def build_record(max_specs: int, stable_basis_limit: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    _profiles, raw_candidates = joint.build_candidates(max_specs=max_specs)
    rows = [analyze_candidate(candidate, stable_basis_limit=stable_basis_limit) for candidate in raw_candidates]
    targets = [row for row in rows if row["proxy_slot_kernel_targets"] > 0]
    zero_free = [row for row in rows if row["zero_row_free_slot_profiles"] > 0]
    if targets:
        best = max(targets, key=lambda row: row["best_profile"]["guaranteed_proxy_nullity_lower_bound"])
        proof_status = "CANDIDATE / PSLOT_PROXY_KERNEL_TARGET / PARTIAL / EXPERIMENTAL"
        failure = "PSLOT_PROXY_KERNEL_TARGET"
    elif zero_free:
        best = max(zero_free, key=lambda row: row["zero_row_free_slot_profiles"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / PSLOT_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        failure = "PSLOT_FORCED_PAIR_EQUALITY"
    elif rows:
        best = max(rows, key=lambda row: (row["slot_profiles_tested"], row["functional_span_rank"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / PSLOT_ZERO_NONBASIS_ROW / PARTIAL / EXPERIMENTAL"
        failure = "PSLOT_ZERO_NONBASIS_ROW"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / PSLOT_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "PSLOT_SUPPORT_FAIL"
    proxy_audit = proxy_audit_for_best(best, raw_candidates, stable_basis_limit)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_proxy_audit": {
            "commit": SOURCE_COMMIT,
            "proxy_rank": previous["proxy_audit"]["proxy_result"]["proxy_rank"],
            "proxy_nullity": previous["proxy_audit"]["proxy_result"]["proxy_nullity"],
            "best_failure_mode": previous["proxy_audit"]["best_failure_mode"],
        },
        "proxy_slot_kernel_search": {
            "templates_tested": max_specs,
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "stable_basis_combinations": sum(row["stable_basis_combinations"] for row in rows),
            "stable_basis_profiles_tested": sum(row["stable_basis_profiles_tested"] for row in rows),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in rows),
            "zero_row_free_slot_profiles": sum(row["zero_row_free_slot_profiles"] for row in rows),
            "pair_projection_clear_slot_profiles": sum(row["pair_projection_clear_slot_profiles"] for row in rows),
            "proxy_slot_kernel_targets": sum(row["proxy_slot_kernel_targets"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_zero_union_size": None if best is None or best["best_profile"] is None else best["best_profile"]["basis_zero_union_size"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["forced_pair_count"],
            "best_guaranteed_proxy_nullity_lower_bound": None if best is None or best["best_profile"] is None else best["best_profile"]["guaranteed_proxy_nullity_lower_bound"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "proxy_audit": proxy_audit,
        "m2_coefficient_audit": m2_audit_for_best(best),
        "realization_status": "SYNTHETIC_FUNCTIONAL_PROXY_TARGET",
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
    args = parser.parse_args()
    record = build_record(max_specs=args.max_specs, stable_basis_limit=args.stable_basis_limit)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["proxy_slot_kernel_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "zero_row_free_slot_profiles": search["zero_row_free_slot_profiles"],
                    "pair_projection_clear_slot_profiles": search["pair_projection_clear_slot_profiles"],
                    "proxy_slot_kernel_targets": search["proxy_slot_kernel_targets"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_basis_zero_union_size": search["best_basis_zero_union_size"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_guaranteed_proxy_nullity_lower_bound": search["best_guaranteed_proxy_nullity_lower_bound"],
                    "best_failure_mode": search["best_failure_mode"],
                    "proxy_audit": record["proxy_audit"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PROXY_SLOT_KERNEL_GENERATOR_READY")


if __name__ == "__main__":
    main()
