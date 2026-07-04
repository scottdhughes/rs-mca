#!/usr/bin/env python3
"""Target the remaining three basis-aware pair-projection zeros for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "0aa9daa"
PREVIOUS_DATA = Path("experimental/data/m1_a327_basis_aware_forced_pair_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_basis_aware_three_pair_projection_repair.json")

ROOT = Path(__file__).resolve().parents[2]
BASIS_AWARE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_basis_aware_pairclear_kernel_synthesis.py"

TARGET_FORCED_PAIRS = ["P12", "P46", "P57"]
DEFAULT_TOP_CLASSES = 32
DEFAULT_RANDOM_BASES = 0


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


basisaware = load_module("basis_aware_pairclear_kernel_synthesis", BASIS_AWARE_SCRIPT)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def target_metrics(summary: dict[str, Any]) -> dict[str, Any]:
    forced = set(summary["forced_pairs"])
    target = set(TARGET_FORCED_PAIRS)
    return {
        "target_forced_pairs": sorted(forced & target),
        "target_forced_pair_count": len(forced & target),
        "target_pairs_repaired": sorted(target - forced),
        "new_forced_pairs_introduced": sorted(forced - target),
    }


def target_sort_key(summary: dict[str, Any]) -> tuple[Any, ...]:
    return (
        summary["target_forced_pair_count"],
        summary["forced_pair_count"],
        summary["slot_nonzero_rows"],
        summary["coefficient_matrix_shape"][0],
        -summary["proxy_kernel_block_degree"],
        summary["basis_zero_union_size"],
        summary["basis_id"],
        summary["proxy_kernel_slot"],
    )


def structural_status(candidate: dict[str, Any]) -> str:
    return basisaware.structural_status(candidate)


def analyze_candidate(candidate: dict[str, Any], top_classes: int, random_bases: int) -> dict[str, Any]:
    row = basisaware.zstable.candidate_structural_row(candidate)
    row["backward_structural_status"] = structural_status(candidate)
    row["basis_combos_tested"] = 0
    row["basis_profiles_tested"] = 0
    row["slot_profiles_tested"] = 0
    row["target_clear_slot_profiles"] = 0
    row["target_clear_slot_kernel_profiles"] = 0
    row["pair_clear_slot_profiles"] = 0
    row["pair_clear_slot_kernel_profiles"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["backward_structural_status"] != "BAPK_STRUCTURAL_PASS":
        row["best_failure_mode"] = row["backward_structural_status"].replace("BAPK", "BATHREE")
        return row

    classes = basisaware.functional.functional_classes(candidate)
    combo_count, combos = basisaware.candidate_basis_combos(
        classes,
        top_classes=top_classes,
        random_bases=random_bases,
    )
    row["basis_combos_tested"] = combo_count
    summaries: list[dict[str, Any]] = []
    profile_seen: set[tuple[int, ...]] = set()
    for combo in combos:
        profile = basisaware.profile_from_indices(
            classes,
            combo,
            f"threepair_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in profile_seen:
            continue
        profile_seen.add(key)
        row["basis_profiles_tested"] += 1
        for slot in range(6):
            summary = basisaware.basis_slot_summary(candidate, classes, profile, slot)
            summary.update(target_metrics(summary))
            if summary["forced_pair_count"] == 0 and summary["slot_nonzero_rows"] == 0:
                summary["best_failure_mode"] = "BATHREE_PAIR_CLEAR_SLOT_KERNEL"
            elif summary["forced_pair_count"] == 0:
                summary["best_failure_mode"] = "BATHREE_PAIR_CLEAR_SLOT"
            elif summary["target_forced_pair_count"] == 0 and summary["slot_nonzero_rows"] == 0:
                summary["best_failure_mode"] = "BATHREE_TARGET_CLEAR_SLOT_KERNEL_NEW_FORCED"
            elif summary["target_forced_pair_count"] == 0:
                summary["best_failure_mode"] = "BATHREE_TARGET_CLEAR_NEW_FORCED"
            elif summary["target_forced_pair_count"] < len(TARGET_FORCED_PAIRS):
                summary["best_failure_mode"] = "BATHREE_PARTIAL_TARGET_REPAIR"
            else:
                summary["best_failure_mode"] = "BATHREE_TARGET_NOT_REPAIRED"
            summaries.append(summary)

    row["slot_profiles_tested"] = len(summaries)
    row["target_clear_slot_profiles"] = sum(1 for item in summaries if item["target_forced_pair_count"] == 0)
    row["target_clear_slot_kernel_profiles"] = sum(
        1 for item in summaries if item["target_forced_pair_count"] == 0 and item["slot_nonzero_rows"] == 0
    )
    row["pair_clear_slot_profiles"] = sum(1 for item in summaries if item["forced_pair_count"] == 0)
    row["pair_clear_slot_kernel_profiles"] = sum(
        1 for item in summaries if item["forced_pair_count"] == 0 and item["slot_nonzero_rows"] == 0
    )
    row["profile_summaries"] = sorted(summaries, key=target_sort_key)[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["pair_clear_slot_kernel_profiles"]:
        row["best_failure_mode"] = "BATHREE_PAIR_CLEAR_SLOT_KERNEL"
    elif row["pair_clear_slot_profiles"]:
        row["best_failure_mode"] = "BATHREE_PAIR_CLEAR_SLOT"
    elif row["target_clear_slot_kernel_profiles"]:
        row["best_failure_mode"] = "BATHREE_TARGET_CLEAR_SLOT_KERNEL_NEW_FORCED"
    elif row["target_clear_slot_profiles"]:
        row["best_failure_mode"] = "BATHREE_TARGET_CLEAR_NEW_FORCED"
    elif summaries and row["best_profile"]["target_forced_pair_count"] < len(TARGET_FORCED_PAIRS):
        row["best_failure_mode"] = "BATHREE_PARTIAL_TARGET_REPAIR"
    elif summaries:
        row["best_failure_mode"] = "BATHREE_TARGET_NOT_REPAIRED"
    else:
        row["best_failure_mode"] = "BATHREE_NO_BASIS_PROFILE"
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
        "backward_structural_status",
        "basis_combos_tested",
        "basis_profiles_tested",
        "slot_profiles_tested",
        "target_clear_slot_profiles",
        "target_clear_slot_kernel_profiles",
        "pair_clear_slot_profiles",
        "pair_clear_slot_kernel_profiles",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_record(top_classes: int, random_bases: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    _profiles, candidates = basisaware.build_candidates()
    rows = [analyze_candidate(candidate, top_classes=top_classes, random_bases=random_bases) for candidate in candidates]

    pair_clear_kernel = [row for row in rows if row["pair_clear_slot_kernel_profiles"] > 0]
    pair_clear = [row for row in rows if row["pair_clear_slot_profiles"] > 0]
    target_clear_kernel = [row for row in rows if row["target_clear_slot_kernel_profiles"] > 0]
    target_clear = [row for row in rows if row["target_clear_slot_profiles"] > 0]
    if pair_clear_kernel:
        best = max(pair_clear_kernel, key=lambda row: row["pair_clear_slot_kernel_profiles"])
        proof_status = "CANDIDATE / BATHREE_PAIR_CLEAR_SLOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "BATHREE_PAIR_CLEAR_SLOT_KERNEL"
    elif pair_clear:
        best = min(pair_clear, key=lambda row: target_sort_key(row["best_profile"]))
        proof_status = "CANDIDATE / BATHREE_PAIR_CLEAR_SLOT / PARTIAL / EXPERIMENTAL"
        failure = "BATHREE_PAIR_CLEAR_SLOT"
    elif target_clear_kernel:
        best = min(target_clear_kernel, key=lambda row: target_sort_key(row["best_profile"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / BATHREE_TARGET_CLEAR_SLOT_KERNEL_NEW_FORCED / PARTIAL / EXPERIMENTAL"
        failure = "BATHREE_TARGET_CLEAR_SLOT_KERNEL_NEW_FORCED"
    elif target_clear:
        best = min(target_clear, key=lambda row: target_sort_key(row["best_profile"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / BATHREE_TARGET_CLEAR_NEW_FORCED / PARTIAL / EXPERIMENTAL"
        failure = "BATHREE_TARGET_CLEAR_NEW_FORCED"
    elif rows:
        best = min(
            rows,
            key=lambda row: target_sort_key(row["best_profile"]) if row.get("best_profile") else (99, 99, 99, 99, 0, 99, "", 99),
        )
        best_target_count = best["best_profile"]["target_forced_pair_count"] if best.get("best_profile") else 99
        if best_target_count < len(TARGET_FORCED_PAIRS):
            proof_status = "EXACT_EXTRACTION_NO_A327 / BATHREE_PARTIAL_TARGET_REPAIR / PARTIAL / EXPERIMENTAL"
            failure = "BATHREE_PARTIAL_TARGET_REPAIR"
        else:
            proof_status = "EXACT_EXTRACTION_NO_A327 / BATHREE_TARGET_NOT_REPAIRED / PARTIAL / EXPERIMENTAL"
            failure = "BATHREE_TARGET_NOT_REPAIRED"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / BATHREE_NO_CANDIDATES / PARTIAL / EXPERIMENTAL"
        failure = "BATHREE_NO_CANDIDATES"

    previous_search = previous["forced_pair_repair"]
    previous_profile = previous["best_candidate"]["best_profile"]
    best_profile = None if best is None else best["best_profile"]
    current_forced = [] if best_profile is None else best_profile["forced_pairs"]
    target = set(TARGET_FORCED_PAIRS)
    current_forced_set = set(current_forced)
    search = {
        "top_classes": top_classes,
        "random_bases": random_bases,
        "exhaustive_basis_front": top_classes >= max((row.get("functional_classes") or 0) for row in rows),
        "systems_tested": len(rows),
        "structural_pass_candidates": sum(row["backward_structural_status"] == "BAPK_STRUCTURAL_PASS" for row in rows),
        "basis_profiles_tested": sum(row["basis_profiles_tested"] for row in rows),
        "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in rows),
        "target_clear_slot_profiles": sum(row["target_clear_slot_profiles"] for row in rows),
        "target_clear_slot_kernel_profiles": sum(row["target_clear_slot_kernel_profiles"] for row in rows),
        "pair_clear_slot_profiles": sum(row["pair_clear_slot_profiles"] for row in rows),
        "pair_clear_slot_kernel_profiles": sum(row["pair_clear_slot_kernel_profiles"] for row in rows),
        "best_template_id": None if best is None else best["template_id"],
        "best_assignment_strategy": None if best is None else best["assignment_strategy"],
        "best_target_forced_pair_count": None if best_profile is None else best_profile["target_forced_pair_count"],
        "best_forced_pair_count": None if best_profile is None else best_profile["forced_pair_count"],
        "best_slot_nonzero_rows": None if best_profile is None else best_profile["slot_nonzero_rows"],
        "best_failure_mode": failure,
        "target_forced_pairs": TARGET_FORCED_PAIRS,
        "previous_forced_pairs": previous_profile["forced_pairs"],
        "current_forced_pairs": current_forced,
        "target_pairs_repaired": sorted(target - current_forced_set),
        "target_pairs_remaining": sorted(target & current_forced_set),
        "new_forced_pairs_introduced": sorted(current_forced_set - target),
        "target_forced_pair_count_delta": (None if best_profile is None else best_profile["target_forced_pair_count"] - len(TARGET_FORCED_PAIRS)),
        "forced_pair_count_delta_from_previous": (None if best_profile is None else len(current_forced) - len(previous_profile["forced_pairs"])),
        "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
        "screen_counts": dict(Counter(row["backward_structural_status"] for row in rows)),
        "candidate_summaries": [candidate_summary(row) for row in rows],
    }

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": 327,
        "source_commit": SOURCE_COMMIT,
        "previous_basis_aware_forced_pair_repair": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "systems_tested": previous_search["systems_tested"],
            "basis_profiles_tested": previous_search["basis_profiles_tested"],
            "slot_profiles_tested": previous_search["slot_profiles_tested"],
            "best_forced_pair_count": previous_profile["forced_pair_count"],
            "best_forced_pairs": previous_profile["forced_pairs"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "three_pair_projection_repair": search,
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "BASIS_AWARE_THREE_PAIR_PROJECTION_REPAIR",
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
            "MCA/protocol consequence from this list-track proxy",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--top-classes", type=int, default=DEFAULT_TOP_CLASSES)
    parser.add_argument("--random-bases", type=int, default=DEFAULT_RANDOM_BASES)
    args = parser.parse_args()
    record = build_record(top_classes=args.top_classes, random_bases=args.random_bases)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["three_pair_projection_repair"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "exhaustive_basis_front": search["exhaustive_basis_front"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "target_clear_slot_profiles": search["target_clear_slot_profiles"],
                    "pair_clear_slot_profiles": search["pair_clear_slot_profiles"],
                    "previous_forced_pairs": search["previous_forced_pairs"],
                    "current_forced_pairs": search["current_forced_pairs"],
                    "target_pairs_repaired": search["target_pairs_repaired"],
                    "target_pairs_remaining": search["target_pairs_remaining"],
                    "new_forced_pairs_introduced": search["new_forced_pairs_introduced"],
                    "best_target_forced_pair_count": search["best_target_forced_pair_count"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_BASIS_AWARE_THREE_PAIR_PROJECTION_REPAIR_READY")


if __name__ == "__main__":
    main()
