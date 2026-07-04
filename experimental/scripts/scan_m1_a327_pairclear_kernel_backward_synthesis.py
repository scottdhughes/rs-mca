#!/usr/bin/env python3
"""Generate actual templates with a pair-clear slot kernel built in."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "81fceb2"
PREVIOUS_DATA = Path("experimental/data/m1_a327_prescribed_nonbasis_kernel_generator.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_kernel_backward_synthesis.json")

ROOT = Path(__file__).resolve().parents[2]
LOWRANK_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_lowrank_template_selected_class_search.py"
RAWARE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_realization_aware_proxy_slot_generator.py"

P = 17
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR_CLEAR_SLOT = 5


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lowrank = load_module("lowrank_template_selected_class_search", LOWRANK_SCRIPT)
raware = load_module("realization_aware_proxy_slot_generator", RAWARE_SCRIPT)
functional = raware.functional
zstable = raware.zstable
joint = raware.joint


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


PAIR_CLEAR_TEMPLATE_SPECS = [
    {
        "template_id": "pairclear_slot5_rank6_spine_a",
        "template_family": "pairclear_slot_rank6_spine",
        "vectors": [
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 2],
            [1, 1, 0, 0, 0, 3],
            [0, 0, 1, 0, 0, 4],
            [0, 0, 0, 1, 0, 5],
            [0, 0, 0, 0, 1, 6],
        ],
        "selected_class_sizes": [3, 4, 5, 6],
        "cost_weight": 4.0,
        "pair7_weight": 1.5,
        "assignment_strategies": ["fiber_block", "residue_block", "fiber_round_robin"],
    },
    {
        "template_id": "pairclear_slot5_rank6_spine_b",
        "template_family": "pairclear_slot_rank6_spine",
        "vectors": [
            [1, 0, 0, 0, 1, 0],
            [0, 1, 0, 0, 1, 1],
            [0, 0, 1, 0, 1, 2],
            [1, 1, 0, 0, 1, 3],
            [1, 0, 1, 0, 1, 4],
            [0, 1, 1, 0, 1, 5],
            [0, 0, 0, 1, 1, 6],
        ],
        "selected_class_sizes": [3, 4, 5, 6],
        "cost_weight": 4.0,
        "pair7_weight": 1.5,
        "assignment_strategies": ["fiber_block", "residue_block", "fiber_round_robin"],
    },
    {
        "template_id": "pairclear_slot5_rank5_plus_tail",
        "template_family": "pairclear_slot_rank5_plus_tail",
        "vectors": [
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1],
            [0, 1, 0, 0, 0, 2],
            [1, 1, 0, 0, 0, 3],
            [0, 0, 1, 0, 0, 4],
            [0, 0, 0, 1, 0, 5],
            [1, 1, 1, 1, 0, 6],
        ],
        "selected_class_sizes": [3, 4, 5, 6],
        "cost_weight": 4.0,
        "pair7_weight": 1.5,
        "assignment_strategies": ["fiber_block", "residue_block", "fiber_round_robin"],
    },
    {
        "template_id": "pairclear_slot5_pair7_guarded",
        "template_family": "pairclear_slot_pair7_guarded",
        "vectors": [
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1],
            [1, 1, 0, 0, 0, 2],
            [0, 0, 1, 0, 0, 3],
            [0, 0, 1, 1, 0, 4],
            [0, 0, 0, 1, 0, 5],
            [0, 0, 0, 0, 1, 6],
        ],
        "selected_class_sizes": [3, 4, 5, 6],
        "cost_weight": 4.0,
        "pair7_weight": 2.5,
        "assignment_strategies": ["pair7_block", "fiber_round_robin", "residue_block"],
    },
]


def template_pairclear(vectors: list[list[int]], slot: int = PAIR_CLEAR_SLOT) -> bool:
    values = [int(row[slot]) % P for row in vectors]
    return len(set(values)) == len(values)


def structural_status(candidate: dict[str, Any]) -> str:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "PKBS_SUPPORT_FAIL"
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return "PKBS_PAIR_GUARD_FAIL"
    if not template_pairclear(candidate["template_vectors"]):
        return "PKBS_SLOT_NOT_PAIR_CLEAR"
    row = zstable.candidate_structural_row(candidate)
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        return row["structural_status"].replace("JOINT_TEMPLATE", "PKBS")
    return "PKBS_STRUCTURAL_PASS"


def pairclear_slot_summary(
    candidate: dict[str, Any],
    classes: list[dict[str, Any]],
    profile: dict[str, Any],
    slot: int,
    run_proxy: bool,
) -> dict[str, Any]:
    summary = raware.actual_slot_summary(candidate, classes, profile, slot, run_proxy=run_proxy)
    if summary["forced_pair_count"] != 0:
        summary["best_failure_mode"] = "PKBS_SLOT_PAIR_CLEAR_BROKEN"
    elif summary["slot_nonzero_rows"] == 0 and summary["proxy_result"] and summary["proxy_result"]["proxy_nullity"] > 0:
        summary["best_failure_mode"] = "PKBS_PROXY_NULLITY_POSITIVE"
    elif summary["slot_nonzero_rows"] == 0:
        summary["best_failure_mode"] = "PKBS_ACTUAL_PAIR_CLEAR_SLOT_TARGET"
    else:
        summary["best_failure_mode"] = "PKBS_SLOT_NOT_KERNEL"
    return summary


def analyze_candidate(candidate: dict[str, Any], stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    row["pairclear_slot"] = PAIR_CLEAR_SLOT
    row["pairclear_slot_values"] = [int(vector[PAIR_CLEAR_SLOT]) % P for vector in candidate["template_vectors"]]
    row["pairclear_slot_distinct"] = template_pairclear(candidate["template_vectors"])
    row["stable_basis_combinations"] = 0
    row["stable_basis_profiles_tested"] = 0
    row["slot_profiles_tested"] = 0
    row["actual_zero_slot_profiles"] = 0
    row["pair_projection_clear_actual_slots"] = 0
    row["proxy_positive_actual_slots"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []

    status = structural_status(candidate)
    row["backward_structural_status"] = status
    if status != "PKBS_STRUCTURAL_PASS":
        row["best_failure_mode"] = status
        return row

    classes = functional.functional_classes(candidate)
    stable_total, profiles = raware.pslot.stable_profiles_for_candidate(classes, limit=stable_basis_limit)
    row["stable_basis_combinations"] = stable_total
    row["stable_basis_profiles_tested"] = len(profiles)
    summaries = [
        pairclear_slot_summary(candidate, classes, profile, slot=slot, run_proxy=run_proxy)
        for profile in profiles
        for slot in range(len(profile["basis_class_indices"]))
    ]
    row["slot_profiles_tested"] = len(summaries)
    row["actual_zero_slot_profiles"] = sum(1 for item in summaries if item["slot_nonzero_rows"] == 0)
    row["pair_projection_clear_actual_slots"] = sum(
        1 for item in summaries if item["slot_nonzero_rows"] == 0 and item["forced_pair_count"] == 0
    )
    row["proxy_positive_actual_slots"] = sum(1 for item in summaries if item["best_failure_mode"] == "PKBS_PROXY_NULLITY_POSITIVE")
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["best_failure_mode"] == "PKBS_PROXY_NULLITY_POSITIVE",
            item["best_failure_mode"] == "PKBS_ACTUAL_PAIR_CLEAR_SLOT_TARGET",
            -item["slot_nonzero_rows"],
            item["proxy_kernel_block_degree"],
            item["stable_common_multiplier_dimension"],
        ),
        reverse=True,
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_positive_actual_slots"]:
        row["best_failure_mode"] = "PKBS_PROXY_NULLITY_POSITIVE"
    elif row["pair_projection_clear_actual_slots"]:
        row["best_failure_mode"] = "PKBS_ACTUAL_PAIR_CLEAR_SLOT_TARGET"
    elif summaries:
        row["best_failure_mode"] = "PKBS_SLOT_NOT_KERNEL"
    else:
        row["best_failure_mode"] = "PKBS_NO_STABLE_BASIS"
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
        "pairclear_slot",
        "pairclear_slot_values",
        "pairclear_slot_distinct",
        "stable_basis_combinations",
        "stable_basis_profiles_tested",
        "slot_profiles_tested",
        "actual_zero_slot_profiles",
        "pair_projection_clear_actual_slots",
        "proxy_positive_actual_slots",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_candidates() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    profiles = [lowrank.solve_template_counts(spec) for spec in PAIR_CLEAR_TEMPLATE_SPECS]
    candidates = []
    for profile in profiles:
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for index, strategy in enumerate(profile["assignment_strategies"]):
            candidates.append(lowrank.evaluate_candidate(profile, strategy, seed=51000 + 37 * index))
    return profiles, candidates


def build_record(stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, candidates = build_candidates()
    rows = [analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=run_proxy) for candidate in candidates]
    proxy_positive = [row for row in rows if row["proxy_positive_actual_slots"] > 0]
    zero_slots = [row for row in rows if row["pair_projection_clear_actual_slots"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / PKBS_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "PKBS_PROXY_NULLITY_POSITIVE"
    elif zero_slots:
        best = max(zero_slots, key=lambda row: row["pair_projection_clear_actual_slots"])
        proof_status = "CANDIDATE / PKBS_ACTUAL_PAIR_CLEAR_SLOT_TARGET / PARTIAL / EXPERIMENTAL"
        failure = "PKBS_ACTUAL_PAIR_CLEAR_SLOT_TARGET"
    elif rows:
        best = min(
            rows,
            key=lambda row: (
                row["best_profile"]["slot_nonzero_rows"] if row.get("best_profile") else 999,
                -row["slot_profiles_tested"],
                row["template_id"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / PKBS_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "PKBS_SLOT_NOT_KERNEL"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / PKBS_NO_CANDIDATES / PARTIAL / EXPERIMENTAL"
        failure = "PKBS_NO_CANDIDATES"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_prescribed_nonbasis_kernel": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "near_pair_clear_kernel_profiles": previous["prescribed_nonbasis_kernel"]["near_pair_clear_kernel_profiles"],
            "best_failure_mode": previous["prescribed_nonbasis_kernel"]["best_failure_mode"],
        },
        "pairclear_backward_synthesis": {
            "template_specs_tested": len(PAIR_CLEAR_TEMPLATE_SPECS),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["backward_structural_status"] == "PKBS_STRUCTURAL_PASS"),
            "stable_basis_combinations": sum(row["stable_basis_combinations"] for row in rows),
            "stable_basis_profiles_tested": sum(row["stable_basis_profiles_tested"] for row in rows),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in rows),
            "actual_zero_slot_profiles": sum(row["actual_zero_slot_profiles"] for row in rows),
            "pair_projection_clear_actual_slots": sum(row["pair_projection_clear_actual_slots"] for row in rows),
            "proxy_positive_actual_slots": sum(row["proxy_positive_actual_slots"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_slot_nonzero_rows": None if best is None or best.get("best_profile") is None else best["best_profile"]["slot_nonzero_rows"],
            "best_forced_pair_count": None if best is None or best.get("best_profile") is None else best["best_profile"]["forced_pair_count"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "PAIR_CLEAR_SLOT_ACTUAL_TEMPLATES",
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
    parser.add_argument("--stable-basis-limit", type=int, default=128)
    parser.add_argument("--run-proxy", action="store_true")
    args = parser.parse_args()
    record = build_record(stable_basis_limit=args.stable_basis_limit, run_proxy=args.run_proxy)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["pairclear_backward_synthesis"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "actual_zero_slot_profiles": search["actual_zero_slot_profiles"],
                    "pair_projection_clear_actual_slots": search["pair_projection_clear_actual_slots"],
                    "proxy_positive_actual_slots": search["proxy_positive_actual_slots"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_KERNEL_BACKWARD_SYNTHESIS_READY")


if __name__ == "__main__":
    main()
