#!/usr/bin/env python3
"""Search basis-aware pair-clear coefficient kernels for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "a1bb7cf"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_kernel_backward_synthesis.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_basis_aware_pairclear_kernel_synthesis.json")

ROOT = Path(__file__).resolve().parents[2]
PKBS_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_kernel_backward_synthesis.py"

P = 17
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pkbs = load_module("pairclear_kernel_backward_synthesis", PKBS_SCRIPT)
lowrank = pkbs.lowrank
raware = pkbs.raware
functional = pkbs.functional
zstable = pkbs.zstable
joint = pkbs.joint


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_rows(rows: list[list[int]], ncols: int = 6) -> int:
    return joint.right_kernel.rank_rows(rows, ncols=ncols, prime=P)


def profile_from_indices(classes: list[dict[str, Any]], selected: tuple[int, ...], basis_id: str) -> dict[str, Any] | None:
    return zstable.profile_from_combo(classes, selected, basis_id)


def candidate_basis_combos(classes: list[dict[str, Any]], top_classes: int, random_bases: int) -> tuple[int, list[tuple[int, ...]]]:
    rows = [row["functional"] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    order = sorted(range(len(classes)), key=lambda idx: (-supports[idx], rows[idx]))
    front = order[: min(top_classes, len(order))]
    combos: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()

    for combo in itertools.combinations(front, 6):
        selected_rows = [rows[idx] for idx in combo]
        if rank_rows(selected_rows) != 6:
            continue
        key = tuple(combo)
        seen.add(key)
        combos.append(key)

    for seed in range(random_bases):
        rng = random.Random(73000 + seed)
        shuffled = list(range(len(classes)))
        rng.shuffle(shuffled)
        selected: list[int] = []
        selected_rows: list[list[int]] = []
        current_rank = 0
        for idx in shuffled:
            trial_rank = rank_rows(selected_rows + [rows[idx]])
            if trial_rank > current_rank:
                selected.append(idx)
                selected_rows.append(rows[idx])
                current_rank = trial_rank
            if current_rank == 6:
                break
        if len(selected) == 6:
            key = tuple(selected)
            if key not in seen:
                seen.add(key)
                combos.append(key)
    return len(combos), combos


def basis_slot_summary(candidate: dict[str, Any], classes: list[dict[str, Any]], profile: dict[str, Any], slot: int) -> dict[str, Any]:
    pair_record = raware.pslot.pair_projection_for_slot(candidate, profile, slot)
    matrix = zstable.coefficient_matrix(profile)
    slot_nonzero_rows = sum(1 for row in matrix if int(row[slot]) % P)
    coefficient_rank = rank_rows(matrix)
    union_positions = zstable.profile_union_size(profile, zstable.class_position_sets(classes))
    failure = "BAPK_PAIR_CLEAR_SLOT_KERNEL"
    if pair_record["forced_pair_count"] > 0:
        failure = "BAPK_SLOT_PAIR_CLEAR_BROKEN"
    elif slot_nonzero_rows > 0:
        failure = "BAPK_PAIR_CLEAR_SLOT_NOT_KERNEL"
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "basis_zero_union_size": union_positions,
        "stable_common_multiplier_dimension": K - union_positions,
        "q_variable_count": profile["q_variable_count"],
        "proxy_kernel_slot": slot,
        "proxy_kernel_vector": [1 if idx == slot else 0 for idx in range(6)],
        "proxy_kernel_block_degree": K - int(profile["basis_support_sizes"][slot]),
        "coefficient_matrix_shape": [len(matrix), 6],
        "coefficient_rank": coefficient_rank,
        "coefficient_nullity": 6 - coefficient_rank,
        "slot_nonzero_rows": slot_nonzero_rows,
        **pair_record,
        "best_failure_mode": failure,
    }


def structural_status(candidate: dict[str, Any]) -> str:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "BAPK_SUPPORT_FAIL"
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return "BAPK_PAIR_GUARD_FAIL"
    row = zstable.candidate_structural_row(candidate)
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        return row["structural_status"].replace("JOINT_TEMPLATE", "BAPK")
    return "BAPK_STRUCTURAL_PASS"


def analyze_candidate(candidate: dict[str, Any], top_classes: int, random_bases: int) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    row["backward_structural_status"] = structural_status(candidate)
    row["basis_combos_tested"] = 0
    row["basis_profiles_tested"] = 0
    row["slot_profiles_tested"] = 0
    row["pair_clear_slot_profiles"] = 0
    row["pair_clear_slot_kernel_profiles"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["backward_structural_status"] != "BAPK_STRUCTURAL_PASS":
        row["best_failure_mode"] = row["backward_structural_status"]
        return row

    classes = functional.functional_classes(candidate)
    combo_count, combos = candidate_basis_combos(classes, top_classes=top_classes, random_bases=random_bases)
    row["basis_combos_tested"] = combo_count
    summaries = []
    profile_seen: set[tuple[int, ...]] = set()
    for combo in combos:
        profile = profile_from_indices(
            classes,
            combo,
            f"basisaware_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
        )
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in profile_seen:
            continue
        profile_seen.add(key)
        row["basis_profiles_tested"] += 1
        for slot in range(6):
            summaries.append(basis_slot_summary(candidate, classes, profile, slot))

    row["slot_profiles_tested"] = len(summaries)
    row["pair_clear_slot_profiles"] = sum(1 for item in summaries if item["forced_pair_count"] == 0)
    row["pair_clear_slot_kernel_profiles"] = sum(
        1 for item in summaries if item["forced_pair_count"] == 0 and item["slot_nonzero_rows"] == 0
    )
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["forced_pair_count"],
            item["slot_nonzero_rows"],
            item["coefficient_matrix_shape"][0],
            -item["proxy_kernel_block_degree"],
            item["basis_zero_union_size"],
        ),
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["pair_clear_slot_kernel_profiles"]:
        row["best_failure_mode"] = "BAPK_PAIR_CLEAR_SLOT_KERNEL"
    elif row["pair_clear_slot_profiles"]:
        row["best_failure_mode"] = "BAPK_PAIR_CLEAR_SLOT_NOT_KERNEL"
    elif summaries:
        row["best_failure_mode"] = "BAPK_SLOT_PAIR_CLEAR_BROKEN"
    else:
        row["best_failure_mode"] = "BAPK_NO_BASIS_PROFILE"
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
        "pair_clear_slot_profiles",
        "pair_clear_slot_kernel_profiles",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_candidates() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return pkbs.build_candidates()


def build_record(top_classes: int, random_bases: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, candidates = build_candidates()
    rows = [analyze_candidate(candidate, top_classes=top_classes, random_bases=random_bases) for candidate in candidates]
    exact = [row for row in rows if row["pair_clear_slot_kernel_profiles"] > 0]
    pair_clear = [row for row in rows if row["pair_clear_slot_profiles"] > 0]
    if exact:
        best = max(exact, key=lambda row: row["pair_clear_slot_kernel_profiles"])
        proof_status = "CANDIDATE / BAPK_PAIR_CLEAR_SLOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "BAPK_PAIR_CLEAR_SLOT_KERNEL"
    elif pair_clear:
        best = min(
            pair_clear,
            key=lambda row: (
                row["best_profile"]["slot_nonzero_rows"] if row["best_profile"] else 999,
                row["best_profile"]["forced_pair_count"] if row["best_profile"] else 999,
                row["template_id"],
            ),
        )
        proof_status = "CANDIDATE / BAPK_PAIR_CLEAR_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "BAPK_PAIR_CLEAR_SLOT_NOT_KERNEL"
    elif rows:
        best = min(
            rows,
            key=lambda row: (
                row["best_profile"]["forced_pair_count"] if row.get("best_profile") else 999,
                row["best_profile"]["slot_nonzero_rows"] if row.get("best_profile") else 999,
                row["template_id"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / BAPK_SLOT_PAIR_CLEAR_BROKEN / PARTIAL / EXPERIMENTAL"
        failure = "BAPK_SLOT_PAIR_CLEAR_BROKEN"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / BAPK_NO_CANDIDATES / PARTIAL / EXPERIMENTAL"
        failure = "BAPK_NO_CANDIDATES"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_pairclear_backward_synthesis": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "slot_profiles_tested": previous["pairclear_backward_synthesis"]["slot_profiles_tested"],
            "pair_projection_clear_actual_slots": previous["pairclear_backward_synthesis"]["pair_projection_clear_actual_slots"],
            "best_failure_mode": previous["pairclear_backward_synthesis"]["best_failure_mode"],
        },
        "basis_aware_pairclear_synthesis": {
            "template_specs_tested": len(pkbs.PAIR_CLEAR_TEMPLATE_SPECS),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "systems_tested": len(rows),
            "top_classes": top_classes,
            "random_bases": random_bases,
            "structural_pass_candidates": sum(1 for row in rows if row["backward_structural_status"] == "BAPK_STRUCTURAL_PASS"),
            "basis_combos_tested": sum(row["basis_combos_tested"] for row in rows),
            "basis_profiles_tested": sum(row["basis_profiles_tested"] for row in rows),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in rows),
            "pair_clear_slot_profiles": sum(row["pair_clear_slot_profiles"] for row in rows),
            "pair_clear_slot_kernel_profiles": sum(row["pair_clear_slot_kernel_profiles"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_forced_pair_count": None if best is None or best.get("best_profile") is None else best["best_profile"]["forced_pair_count"],
            "best_slot_nonzero_rows": None if best is None or best.get("best_profile") is None else best["best_profile"]["slot_nonzero_rows"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "BASIS_AWARE_PAIR_CLEAR_SEARCH",
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
    parser.add_argument("--top-classes", type=int, default=14)
    parser.add_argument("--random-bases", type=int, default=64)
    args = parser.parse_args()
    record = build_record(top_classes=args.top_classes, random_bases=args.random_bases)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["basis_aware_pairclear_synthesis"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "pair_clear_slot_profiles": search["pair_clear_slot_profiles"],
                    "pair_clear_slot_kernel_profiles": search["pair_clear_slot_kernel_profiles"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_BASIS_AWARE_PAIRCLEAR_KERNEL_SYNTHESIS_READY")


if __name__ == "__main__":
    main()
