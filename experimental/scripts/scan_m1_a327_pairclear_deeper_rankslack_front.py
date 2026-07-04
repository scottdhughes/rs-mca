#!/usr/bin/env python3
"""Search for deeper pair-clear rank-slack chambers for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "ced3433"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_diverse_rankslack_kernel_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_deeper_rankslack_front.json")

ROOT = Path(__file__).resolve().parents[2]
DIVERSE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_diverse_chamber_front.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


diverse = load_module("pairclear_diverse_chamber_front", DIVERSE_SCRIPT)
tchamber = diverse.tchamber
chamber = diverse.chamber
ninerow = diverse.ninerow
lowrank = diverse.lowrank


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def deep_rank_slack_chambers(score: dict[str, Any], prefix: str = "sample") -> list[dict[str, Any]]:
    rows = []
    for key in [
        f"best_{prefix}_direct_support_reduced_chamber",
        f"best_{prefix}_rank_slack_chamber",
        f"best_{prefix}_nine_row_chamber",
        f"best_{prefix}_chamber",
    ]:
        value = score.get(key)
        if value and value.get("zero_row_count", 0) >= 8 and value.get("inactive_rank", 99) <= 4:
            rows.append(value)
    return rows


def full_deep_rank_slack_chambers(score: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for key in [
        "best_direct_support_reduced_chamber",
        "best_rank_slack_chamber",
        "best_nine_row_chamber",
        "best_chamber",
    ]:
        value = score.get(key)
        if value and value.get("zero_row_count", 0) >= 8 and value.get("inactive_rank", 99) <= 4:
            rows.append(value)
    return rows


def deep_sample_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    deep = deep_rank_slack_chambers(row, prefix="sample")
    best_deep = max(
        deep,
        key=lambda item: (
            item["zero_row_count"],
            -item["inactive_rank"],
            item["inactive_kernel_nullity"],
            -item["active_row_count"],
        ),
        default=None,
    )
    best_any = (
        row.get("best_sample_direct_support_reduced_chamber")
        or row.get("best_sample_rank_slack_chamber")
        or row.get("best_sample_nine_row_chamber")
        or row.get("best_sample_chamber")
        or {}
    )
    return (
        0 if best_deep else 1,
        -(best_deep or best_any).get("zero_row_count", 0),
        (best_deep or best_any).get("inactive_rank", 99),
        -(best_deep or best_any).get("inactive_kernel_nullity", 0),
        -row["pair_clear_directions"],
        row["template_id"],
        row["basis_id"],
    )


def full_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    deep = full_deep_rank_slack_chambers(row)
    best_deep = max(
        deep,
        key=lambda item: (
            item["zero_row_count"],
            -item["inactive_rank"],
            item["inactive_kernel_nullity"],
            -item["active_row_count"],
        ),
        default=None,
    )
    best_any = (
        row.get("best_direct_support_reduced_chamber")
        or row.get("best_rank_slack_chamber")
        or row.get("best_nine_row_chamber")
        or row.get("best_chamber")
        or {}
    )
    return (
        0 if best_deep else 1,
        -(best_deep or best_any).get("zero_row_count", 0),
        (best_deep or best_any).get("inactive_rank", 99),
        -(best_deep or best_any).get("inactive_kernel_nullity", 0),
        -row["pair_clear_directions"],
        row["template_id"],
        row["basis_id"],
    )


def compact_sample(row: dict[str, Any]) -> dict[str, Any]:
    out = diverse.compact_sample(row)
    deep = deep_rank_slack_chambers(row, prefix="sample")
    out["sample_deep_rank_slack_chambers"] = len(deep)
    out["best_sample_deep_rank_slack_chamber"] = min(
        deep,
        key=lambda item: (-item["zero_row_count"], item["inactive_rank"], item["active_row_count"]),
        default=None,
    )
    return out


def compact_full(row: dict[str, Any]) -> dict[str, Any]:
    out = diverse.compact_full(row)
    deep = full_deep_rank_slack_chambers(row)
    out["deep_rank_slack_chambers"] = len(deep)
    out["best_deep_rank_slack_chamber"] = min(
        deep,
        key=lambda item: (-item["zero_row_count"], item["inactive_rank"], item["active_row_count"]),
        default=None,
    )
    return out


def build_record(
    max_mutations: int,
    max_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
    sample_directions: int,
    full_profiles: int,
    extension_chamber_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    specs = ninerow.mutation_specs(max_mutations=max_mutations)
    profiles = []
    for spec in specs:
        profile = lowrank.solve_template_counts(spec)
        profile["mutation_id"] = spec.get("mutation_id")
        profile["base_template_id"] = spec.get("base_template_id")
        profiles.append(profile)

    candidates = []
    for profile_index, profile in enumerate(profiles):
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for strategy_index, strategy in enumerate(profile["assignment_strategies"]):
            candidates.append(diverse.candidate_from_profile(profile, strategy, seed=107000 + 97 * profile_index + strategy_index))

    screened = [(candidate, tchamber.candidate_screen_row(candidate)) for candidate in candidates]
    structural_pass = [
        (candidate, row)
        for candidate, row in screened
        if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
    ]
    structural_pass.sort(key=tchamber.candidate_sort_key)
    selected_candidates = diverse.diverse_candidates(structural_pass, max_candidates)
    directions = diverse.sampled_projective_directions(sample_directions, seed=327777)

    sampled = []
    profile_lookup: dict[tuple[str, str, int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    for candidate, _row in selected_candidates:
        profiles_for_candidate = tchamber.basis_profiles(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            limit=max_basis_profiles,
        )
        for profile in profiles_for_candidate:
            score = diverse.cheap_score_profile(candidate, profile, directions)
            sampled.append(score)
            profile_lookup[
                (
                    score["template_id"],
                    score["assignment_strategy"],
                    score["assignment_seed"],
                    score["basis_id"],
                )
            ] = (candidate, profile)

    full_inputs = sorted(sampled, key=deep_sample_sort_key)[:full_profiles]
    full_scores = []
    for row in full_inputs:
        key = (row["template_id"], row["assignment_strategy"], row["assignment_seed"], row["basis_id"])
        candidate, profile = profile_lookup[key]
        full_scores.append(
            tchamber.score_profile(
                candidate,
                profile,
                direction_limit=None,
                extension_chamber_limit=extension_chamber_limit,
            )
        )

    best_full = min(full_scores, key=full_sort_key) if full_scores else None
    best_sample = min(sampled, key=deep_sample_sort_key) if sampled else None
    full_deep = [row for row in full_scores if full_deep_rank_slack_chambers(row)]
    sample_deep = [row for row in sampled if deep_rank_slack_chambers(row, prefix="sample")]

    failure = "DEEP_RANKSLACK_NO_SCORED_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / DEEP_RANKSLACK_NO_SCORED_PROFILES / PARTIAL / EXPERIMENTAL"
    if full_deep:
        failure = "DEEP_RANKSLACK_FOUND"
        proof_status = "CANDIDATE / DEEP_RANKSLACK_FOUND / PARTIAL / EXPERIMENTAL"
    elif best_full and best_full.get("direct_support_reduced_chambers", 0) > 0:
        failure = "DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY"
        proof_status = "CANDIDATE / DEEP_RANKSLACK_SUPPORT_REDUCED_ONLY / PARTIAL / EXPERIMENTAL"
    elif sample_deep:
        failure = "DEEP_RANKSLACK_SAMPLE_ONLY"
        proof_status = "CANDIDATE / DEEP_RANKSLACK_SAMPLE_ONLY / PARTIAL / EXPERIMENTAL"
    elif best_full:
        failure = best_full["best_failure_mode"].replace("TCHAMBER", "DEEP_RANKSLACK")
        proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    previous_kernel = previous["rank_slack_kernel"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_rank_slack_kernel_repair": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "directions_tested": previous_kernel["directions_tested"],
            "pair_clear_directions": previous_kernel["pair_clear_directions"],
            "support_reduced_directions": previous_kernel["support_reduced_directions"],
            "nine_or_better_directions": previous_kernel["nine_or_better_directions"],
            "coefficient_kernel_directions": previous_kernel["coefficient_kernel_directions"],
            "best_failure_mode": previous_kernel["best_failure_mode"],
        },
        "deeper_rank_slack_front": {
            "max_mutations": max_mutations,
            "max_candidates": max_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "sample_directions": len(directions),
            "full_profiles": full_profiles,
            "extension_chamber_limit": extension_chamber_limit,
            "deep_target": "zero_row_count >= 8 and inactive_rank <= 4",
            "mutations_generated": len(specs),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": len(candidates),
            "structural_pass_candidates": len(structural_pass),
            "diverse_candidates_selected": len(selected_candidates),
            "sampled_profiles": len(sampled),
            "sample_deep_rank_slack_profiles": len(sample_deep),
            "sample_pair_clear_directions": sum(row["pair_clear_directions"] for row in sampled),
            "full_profiles_scanned": len(full_scores),
            "full_deep_rank_slack_profiles": len(full_deep),
            "full_directions_tested": sum(row["directions_tested"] for row in full_scores),
            "full_pair_clear_directions": sum(row["pair_clear_directions"] for row in full_scores),
            "full_direct_support_reduced_profiles": sum(1 for row in full_scores if row["direct_support_reduced_chambers"] > 0),
            "full_rank_slack_profiles": sum(1 for row in full_scores if row["rank_slack_chambers"] > 0),
            "full_support_reduced_extension_profiles": sum(1 for row in full_scores if row["support_reduced_extensions"] > 0),
            "best_template_id": None if best_full is None else best_full["template_id"],
            "best_mutation_id": None if best_full is None else best_full.get("mutation_id"),
            "best_assignment_strategy": None if best_full is None else best_full["assignment_strategy"],
            "best_basis_id": None if best_full is None else best_full["basis_id"],
            "best_failure_mode": failure,
            "sample_failure_counts": dict(Counter(row["best_failure_mode"] for row in sampled)),
            "full_failure_counts": dict(Counter(row["best_failure_mode"] for row in full_scores)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in screened)),
            "sampled_profile_summaries": [compact_sample(row) for row in sorted(sampled, key=deep_sample_sort_key)[:20]],
            "full_profile_summaries": [compact_full(row) for row in sorted(full_scores, key=full_sort_key)],
        },
        "best_sample_profile": None if best_sample is None else compact_sample(best_sample),
        "best_full_profile": None if best_full is None else compact_full(best_full),
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
            "global obstruction outside the tested deeper rank-slack front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=160)
    parser.add_argument("--max-candidates", type=int, default=36)
    parser.add_argument("--top-classes", type=int, default=16)
    parser.add_argument("--random-bases", type=int, default=32)
    parser.add_argument("--max-basis-profiles", type=int, default=3)
    parser.add_argument("--sample-directions", type=int, default=75000)
    parser.add_argument("--full-profiles", type=int, default=4)
    parser.add_argument("--extension-chamber-limit", type=int, default=100)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
        sample_directions=args.sample_directions,
        full_profiles=args.full_profiles,
        extension_chamber_limit=args.extension_chamber_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["deeper_rank_slack_front"]
        best = record["best_full_profile"]
        deep = None if best is None else best.get("best_deep_rank_slack_chamber")
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "mutations_generated": search["mutations_generated"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "sampled_profiles": search["sampled_profiles"],
                    "sample_deep_rank_slack_profiles": search["sample_deep_rank_slack_profiles"],
                    "full_profiles_scanned": search["full_profiles_scanned"],
                    "full_deep_rank_slack_profiles": search["full_deep_rank_slack_profiles"],
                    "full_direct_support_reduced_profiles": search["full_direct_support_reduced_profiles"],
                    "best_template_id": search["best_template_id"],
                    "best_mutation_id": search["best_mutation_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_deep_zero_count": None if deep is None else deep["zero_row_count"],
                    "best_deep_inactive_rank": None if deep is None else deep["inactive_rank"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_DEEPER_RANKSLACK_FRONT_READY")


if __name__ == "__main__":
    main()
