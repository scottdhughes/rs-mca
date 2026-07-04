#!/usr/bin/env python3
"""Focused repair search for the best actual-template proxy-slot near miss."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "e8ce88b"
PREVIOUS_DATA = Path("experimental/data/m1_a327_realization_aware_proxy_slot_generator.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_realized_slot_nearmiss_repair.json")

ROOT = Path(__file__).resolve().parents[2]
RAWARE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_realization_aware_proxy_slot_generator.py"

TARGET_AGREEMENT = 327
P = 17
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


raware = load_module("realization_aware_proxy_slot_generator", RAWARE_SCRIPT)
joint = raware.joint
dependency = joint.dependency
functional = raware.functional
pslot = raware.pslot
zstable = raware.zstable


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_cost_for_mask(vectors: list[list[int]], mask: int) -> int:
    members = dependency.mask_members(mask)
    return len(functional.row_basis_mod_p(vectors, members))


def total_effective_cost(vectors: list[list[int]], selected_counts: list[dict[str, Any]]) -> int:
    return sum(rank_cost_for_mask(vectors, int(row["mask"])) * int(row["count"]) for row in selected_counts)


def near_miss_base_profile() -> dict[str, Any]:
    spec = next(item for item in joint.template_specs(36) if item["template_id"] == "single_outside_w7_v3")
    profile = dependency.lowrank.solve_template_counts(spec)
    if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
        raise RuntimeError("near-miss base profile did not solve")
    return profile


def mutation_profiles(base_profile: dict[str, Any], max_mutations: int) -> list[dict[str, Any]]:
    base_vectors = [[int(value) % P for value in row] for row in base_profile["template_vectors"]]
    rows: list[dict[str, Any]] = []

    def add(mutation_id: str, vectors: list[list[int]]) -> None:
        if len(rows) >= max_mutations:
            return
        cost = total_effective_cost(vectors, base_profile["selected_counts"])
        rows.append(
            {
                **base_profile,
                "template_id": f"nearmiss_{mutation_id}",
                "template_family": "single_outside_w7_v3_nearmiss_repair",
                "template_vectors": vectors,
                "total_effective_cost": cost,
                "variable_count": TEMPLATE_DIM * 256,
                "mutation_id": mutation_id,
                "base_template_id": base_profile["template_id"],
            }
        )

    add("base", [row[:] for row in base_vectors])
    for col in range(TEMPLATE_DIM):
        original = base_vectors[6][col]
        for value in range(P):
            if value == original:
                continue
            vectors = [row[:] for row in base_vectors]
            vectors[6][col] = value
            add(f"w7_c{col}_v{value}", vectors)
    focus = [row[:] for row in base_vectors]
    focus[6][1] = 9
    for col in range(TEMPLATE_DIM):
        if col == 1:
            continue
        original = focus[6][col]
        for value in range(P):
            if value == original:
                continue
            vectors = [row[:] for row in focus]
            vectors[6][col] = value
            add(f"w7_c1_v9_c{col}_v{value}", vectors)
    return rows


def candidate_structural_pass(candidate: dict[str, Any]) -> bool:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return False
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return False
    return True


def analyze_candidate(candidate: dict[str, Any], stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    row["mutation_id"] = candidate.get("mutation_id")
    row["base_template_id"] = candidate.get("base_template_id")
    row["stable_basis_combinations"] = 0
    row["stable_basis_profiles_tested"] = 0
    row["slot_profiles_tested"] = 0
    row["actual_zero_slot_profiles"] = 0
    row["pair_projection_clear_actual_slots"] = 0
    row["proxy_positive_actual_slots"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = zstable.mapped_structural_failure(row["structural_status"]).replace("ZSTABLE", "NREPAIR")
        return row

    classes = functional.functional_classes(candidate)
    stable_total, profiles = pslot.stable_profiles_for_candidate(classes, limit=stable_basis_limit)
    row["stable_basis_combinations"] = stable_total
    row["stable_basis_profiles_tested"] = len(profiles)
    summaries = []
    for profile in profiles:
        for slot in range(6):
            summaries.append(raware.actual_slot_summary(candidate, classes, profile, slot, run_proxy=run_proxy))
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
            -item["forced_pair_count"],
            item["proxy_kernel_block_degree"],
            item["stable_common_multiplier_dimension"],
        ),
        reverse=True,
    )[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_positive_actual_slots"]:
        row["best_failure_mode"] = "NREPAIR_PROXY_NULLITY_POSITIVE"
    elif row["pair_projection_clear_actual_slots"]:
        row["best_failure_mode"] = "NREPAIR_ACTUAL_PROXY_SLOT_TARGET"
    elif row["actual_zero_slot_profiles"]:
        row["best_failure_mode"] = "NREPAIR_FORCED_PAIR_EQUALITY"
    elif summaries:
        row["best_failure_mode"] = "NREPAIR_SLOT_NOT_KERNEL"
    else:
        row["best_failure_mode"] = "NREPAIR_NO_STABLE_BASIS"
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "template_family",
        "mutation_id",
        "base_template_id",
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
        "effective_cost",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_record(max_mutations: int, stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    base_profile = near_miss_base_profile()
    mutation_rows = mutation_profiles(base_profile, max_mutations=max_mutations)
    strategies = [
        "signature_fiber_blocks",
        "signature_residue_blocks",
        "pair7_signature_blocks",
        "dependency_twin_interleave",
        "fiber_factor_packed",
        "seeded_dependency_shuffle",
    ]
    candidates = []
    for mutation_index, profile in enumerate(mutation_rows):
        for strategy_index, strategy in enumerate(strategies):
            candidate = dependency.evaluate_dependency_candidate(
                profile,
                strategy,
                seed=71000 + mutation_index * 137 + strategy_index * 19,
            )
            candidate["mutation_id"] = profile["mutation_id"]
            candidate["base_template_id"] = profile["base_template_id"]
            candidates.append(candidate)
    rows = [analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=run_proxy) for candidate in candidates]
    proxy_positive = [row for row in rows if row["proxy_positive_actual_slots"] > 0]
    zero_slots = [row for row in rows if row["actual_zero_slot_profiles"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / NREPAIR_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "NREPAIR_PROXY_NULLITY_POSITIVE"
    elif zero_slots:
        best = max(zero_slots, key=lambda row: row["pair_projection_clear_actual_slots"])
        proof_status = "CANDIDATE / NREPAIR_ACTUAL_PROXY_SLOT_TARGET / PARTIAL / EXPERIMENTAL"
        failure = "NREPAIR_ACTUAL_PROXY_SLOT_TARGET"
    elif rows:
        best = min(
            rows,
            key=lambda row: (
                row["best_profile"]["slot_nonzero_rows"] if row["best_profile"] else 999,
                row["best_profile"]["forced_pair_count"] if row["best_profile"] else 999,
                row["effective_cost"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / NREPAIR_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "NREPAIR_SLOT_NOT_KERNEL"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / NREPAIR_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "NREPAIR_SUPPORT_FAIL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_realization_aware": {
            "commit": SOURCE_COMMIT,
            "best_template_id": previous["realization_aware_search"]["best_template_id"],
            "best_assignment_strategy": previous["realization_aware_search"]["best_assignment_strategy"],
            "best_slot_nonzero_rows": previous["realization_aware_search"]["best_slot_nonzero_rows"],
            "actual_zero_slot_profiles": previous["realization_aware_search"]["actual_zero_slot_profiles"],
            "best_failure_mode": previous["realization_aware_search"]["best_failure_mode"],
        },
        "nearmiss_repair_search": {
            "mutation_profiles_tested": len(mutation_rows),
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "stable_basis_combinations": sum(row["stable_basis_combinations"] for row in rows),
            "stable_basis_profiles_tested": sum(row["stable_basis_profiles_tested"] for row in rows),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in rows),
            "actual_zero_slot_profiles": sum(row["actual_zero_slot_profiles"] for row in rows),
            "pair_projection_clear_actual_slots": sum(row["pair_projection_clear_actual_slots"] for row in rows),
            "proxy_positive_actual_slots": sum(row["proxy_positive_actual_slots"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best["mutation_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_slot_nonzero_rows": None if best is None or best["best_profile"] is None else best["best_profile"]["slot_nonzero_rows"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["forced_pair_count"],
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
    parser.add_argument("--max-mutations", type=int, default=177)
    parser.add_argument("--stable-basis-limit", type=int, default=64)
    parser.add_argument("--run-proxy", action="store_true")
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        stable_basis_limit=args.stable_basis_limit,
        run_proxy=args.run_proxy,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["nearmiss_repair_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "mutation_profiles_tested": search["mutation_profiles_tested"],
                    "systems_tested": search["systems_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "actual_zero_slot_profiles": search["actual_zero_slot_profiles"],
                    "pair_projection_clear_actual_slots": search["pair_projection_clear_actual_slots"],
                    "proxy_positive_actual_slots": search["proxy_positive_actual_slots"],
                    "best_mutation_id": search["best_mutation_id"],
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
        print("M1_A327_REALIZED_SLOT_NEARMISS_REPAIR_READY")


if __name__ == "__main__":
    main()
