#!/usr/bin/env python3
"""Co-design P23 repair and slot-kernel pressure for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "ae37b1a"
PREVIOUS_DATA = Path("experimental/data/m1_a327_template_vector_pairprojection_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_p23_slot_kernel_codesign.json")

ROOT = Path(__file__).resolve().parents[2]
TVPAIR_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_template_vector_pairprojection_repair.py"

P = 17
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR_CLEAR_SLOT = 5
TARGET_PAIR = "P23"
BEST_PREVIOUS_MUTATION = "w1_c0_d16"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tvpair = load_module("template_vector_pairprojection_repair", TVPAIR_SCRIPT)
lowrank = tvpair.lowrank
zstable = tvpair.zstable
basisaware = tvpair.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize(vectors: list[list[int]]) -> list[list[int]]:
    return [[int(value) % P for value in row] for row in vectors]


def best_previous_vectors() -> list[list[int]]:
    base = normalize(tvpair.base_spec()["vectors"])
    # BEST_PREVIOUS_MUTATION is w1_c0_d16: add -1 to witness 1, coordinate 0.
    base[0][0] = (base[0][0] - 1) % P
    return base


def template_pairclear(vectors: list[list[int]]) -> bool:
    values = [int(row[PAIR_CLEAR_SLOT]) % P for row in vectors]
    return len(set(values)) == len(values)


def mutation_specs(max_mutations: int) -> list[dict[str, Any]]:
    base = tvpair.base_spec()
    start = best_previous_vectors()
    rows: list[dict[str, Any]] = []
    seen: set[tuple[tuple[int, ...], ...]] = set()

    def add(mutation_id: str, vectors: list[list[int]]) -> None:
        if len(rows) >= max_mutations:
            return
        normalized = normalize(vectors)
        key = tuple(tuple(row) for row in normalized)
        if key in seen or not template_pairclear(normalized):
            return
        seen.add(key)
        rows.append(
            {
                **base,
                "template_id": f"p23slot_{mutation_id}",
                "template_family": "pairclear_slot_pair7_guarded_p23_slot_codesign",
                "vectors": normalized,
                "base_template_id": "tvpair_w1_c0_d16",
                "mutation_id": mutation_id,
            }
        )

    add("base_w1_c0_d16", [row[:] for row in start])

    # Directly disturb the remaining forced pair P23.
    for witness in (2, 3):
        row_index = witness - 1
        for col in range(PAIR_CLEAR_SLOT):
            for delta in (1, P - 1, 2, P - 2, 3, P - 3):
                vectors = [row[:] for row in start]
                vectors[row_index][col] = (vectors[row_index][col] + delta) % P
                add(f"w{witness}_c{col}_d{delta}", vectors)

    # Split P23 symmetrically in coefficient coordinates.
    for col in range(PAIR_CLEAR_SLOT):
        for delta in (1, P - 1, 2, P - 2):
            vectors = [row[:] for row in start]
            vectors[1][col] = (vectors[1][col] + delta) % P
            vectors[2][col] = (vectors[2][col] - delta) % P
            add(f"P23_split_c{col}_d{delta}", vectors)

    # Repair against rows that often reintroduced forced pairs in the previous front.
    for witness in (1, 2, 3, 4, 7):
        for col in (0, 1, 2):
            vectors = [row[:] for row in start]
            vectors[witness - 1][col] = (vectors[witness - 1][col] + 1) % P
            vectors[(witness % 7)][col] = (vectors[(witness % 7)][col] - 1) % P
            add(f"cycle_w{witness}_c{col}", vectors)
    return rows


def structural_status(candidate: dict[str, Any]) -> str:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "P23SLOT_SUPPORT_FAIL"
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return "P23SLOT_PAIR_GUARD_FAIL"
    row = zstable.candidate_structural_row(candidate)
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        return row["structural_status"].replace("JOINT_TEMPLATE", "P23SLOT")
    return "P23SLOT_STRUCTURAL_PASS"


def candidate_from_profile(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    candidate = lowrank.evaluate_candidate(profile, strategy, seed=seed)
    candidate["mutation_id"] = profile.get("mutation_id")
    candidate["base_template_id"] = profile.get("base_template_id")
    return candidate


def score_key(row: dict[str, Any]) -> tuple[Any, ...]:
    profile = row.get("best_profile") or {}
    forced_pairs = set(profile.get("forced_pairs") or [])
    return (
        profile.get("forced_pair_count", 999),
        int(TARGET_PAIR in forced_pairs),
        profile.get("slot_nonzero_rows", 999),
        -profile.get("coefficient_nullity", 0),
        profile.get("coefficient_matrix_shape", [999, 999])[0],
        row.get("template_id", ""),
    )


def analyze_candidate(candidate: dict[str, Any], top_classes: int, random_bases: int) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    row["mutation_id"] = candidate.get("mutation_id")
    row["base_template_id"] = candidate.get("base_template_id")
    row["backward_structural_status"] = structural_status(candidate)
    row["basis_profiles_tested"] = 0
    row["slot_profiles_tested"] = 0
    row["pair_clear_slot_profiles"] = 0
    row["pair_clear_slot_kernel_profiles"] = 0
    row["p23_clear_slot_profiles"] = 0
    row["p23_clear_slot_kernel_profiles"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["backward_structural_status"] != "P23SLOT_STRUCTURAL_PASS":
        row["best_failure_mode"] = row["backward_structural_status"]
        return row

    detail = basisaware.analyze_candidate(candidate, top_classes=top_classes, random_bases=random_bases)
    summaries = []
    for summary in detail["profile_summaries"]:
        summary = dict(summary)
        summary["p23_forced"] = TARGET_PAIR in summary["forced_pairs"]
        if summary["forced_pair_count"] == 0 and summary["slot_nonzero_rows"] == 0:
            summary["best_failure_mode"] = "P23SLOT_PAIR_CLEAR_SLOT_KERNEL"
        elif summary["forced_pair_count"] == 0:
            summary["best_failure_mode"] = "P23SLOT_PAIR_CLEAR_SLOT"
        elif not summary["p23_forced"] and summary["slot_nonzero_rows"] == 0:
            summary["best_failure_mode"] = "P23SLOT_P23_CLEAR_SLOT_KERNEL_NEW_FORCED"
        elif not summary["p23_forced"]:
            summary["best_failure_mode"] = "P23SLOT_P23_CLEAR_NEW_FORCED"
        else:
            summary["best_failure_mode"] = "P23SLOT_P23_STILL_FORCED"
        summaries.append(summary)

    row.update(
        {
            "basis_combos_tested": detail["basis_combos_tested"],
            "basis_profiles_tested": detail["basis_profiles_tested"],
            "slot_profiles_tested": detail["slot_profiles_tested"],
            "pair_clear_slot_profiles": detail["pair_clear_slot_profiles"],
            "pair_clear_slot_kernel_profiles": detail["pair_clear_slot_kernel_profiles"],
        }
    )
    # Re-score the retained top summaries for P23/slot-kernel pressure.
    summaries.sort(
        key=lambda item: (
            item["forced_pair_count"],
            int(item["p23_forced"]),
            item["slot_nonzero_rows"],
            -item["coefficient_nullity"],
            item["coefficient_matrix_shape"][0],
            item["basis_id"],
        )
    )
    row["profile_summaries"] = summaries[:8]
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    row["p23_clear_slot_profiles"] = sum(1 for item in detail["profile_summaries"] if TARGET_PAIR not in item["forced_pairs"])
    row["p23_clear_slot_kernel_profiles"] = sum(
        1 for item in detail["profile_summaries"] if TARGET_PAIR not in item["forced_pairs"] and item["slot_nonzero_rows"] == 0
    )
    if row["pair_clear_slot_kernel_profiles"]:
        row["best_failure_mode"] = "P23SLOT_PAIR_CLEAR_SLOT_KERNEL"
    elif row["pair_clear_slot_profiles"]:
        row["best_failure_mode"] = "P23SLOT_PAIR_CLEAR_SLOT"
    elif row["best_profile"] and TARGET_PAIR not in row["best_profile"]["forced_pairs"] and row["best_profile"]["slot_nonzero_rows"] == 0:
        row["best_failure_mode"] = "P23SLOT_P23_CLEAR_SLOT_KERNEL_NEW_FORCED"
    elif row["best_profile"] and TARGET_PAIR not in row["best_profile"]["forced_pairs"]:
        row["best_failure_mode"] = "P23SLOT_P23_CLEAR_NEW_FORCED"
    elif row["best_profile"]:
        row["best_failure_mode"] = "P23SLOT_P23_STILL_FORCED"
    else:
        row["best_failure_mode"] = "P23SLOT_NO_BASIS_PROFILE"
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
        "backward_structural_status",
        "basis_profiles_tested",
        "slot_profiles_tested",
        "pair_clear_slot_profiles",
        "pair_clear_slot_kernel_profiles",
        "p23_clear_slot_profiles",
        "p23_clear_slot_kernel_profiles",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_record(max_mutations: int, max_candidates: int, top_classes: int, random_bases: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    specs = mutation_specs(max_mutations=max_mutations)
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
            candidates.append(candidate_from_profile(profile, strategy, seed=72000 + 97 * profile_index + strategy_index))

    structural_rows = []
    for candidate in candidates:
        row = zstable.candidate_structural_row(candidate)
        row["mutation_id"] = candidate.get("mutation_id")
        row["base_template_id"] = candidate.get("base_template_id")
        row["backward_structural_status"] = structural_status(candidate)
        structural_rows.append((candidate, row))

    pass_rows = [
        (candidate, row)
        for candidate, row in structural_rows
        if row["backward_structural_status"] == "P23SLOT_STRUCTURAL_PASS"
    ]
    pass_rows.sort(
        key=lambda item: (
            item[1]["forced_functional_identities"],
            -item[1]["functional_span_rank"],
            item[0]["total_effective_cost"],
            -min(item[0]["pair7_counts"]),
            item[0]["max_pair_count"],
            item[0]["mutation_id"],
            item[0]["assignment_strategy"],
        )
    )
    selected = pass_rows[:max_candidates]
    analyzed = [analyze_candidate(candidate, top_classes=top_classes, random_bases=random_bases) for candidate, _row in selected]
    skipped_structural_pass = max(0, len(pass_rows) - len(selected))

    pair_clear_kernel = [row for row in analyzed if row["pair_clear_slot_kernel_profiles"] > 0]
    pair_clear = [row for row in analyzed if row["pair_clear_slot_profiles"] > 0]
    p23_clear_kernel = [
        row for row in analyzed if row.get("best_profile") and TARGET_PAIR not in row["best_profile"]["forced_pairs"] and row["best_profile"]["slot_nonzero_rows"] == 0
    ]
    p23_clear = [row for row in analyzed if row.get("best_profile") and TARGET_PAIR not in row["best_profile"]["forced_pairs"]]
    if pair_clear_kernel:
        best = max(pair_clear_kernel, key=lambda row: row["pair_clear_slot_kernel_profiles"])
        proof_status = "CANDIDATE / P23SLOT_PAIR_CLEAR_SLOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "P23SLOT_PAIR_CLEAR_SLOT_KERNEL"
    elif pair_clear:
        best = min(pair_clear, key=score_key)
        proof_status = "CANDIDATE / P23SLOT_PAIR_CLEAR_SLOT / PARTIAL / EXPERIMENTAL"
        failure = "P23SLOT_PAIR_CLEAR_SLOT"
    elif p23_clear_kernel:
        best = min(p23_clear_kernel, key=score_key)
        proof_status = "EXACT_EXTRACTION_NO_A327 / P23SLOT_P23_CLEAR_SLOT_KERNEL_NEW_FORCED / PARTIAL / EXPERIMENTAL"
        failure = "P23SLOT_P23_CLEAR_SLOT_KERNEL_NEW_FORCED"
    elif p23_clear:
        best = min(p23_clear, key=score_key)
        proof_status = "EXACT_EXTRACTION_NO_A327 / P23SLOT_P23_CLEAR_NEW_FORCED / PARTIAL / EXPERIMENTAL"
        failure = "P23SLOT_P23_CLEAR_NEW_FORCED"
    elif analyzed:
        best = min(analyzed, key=score_key)
        proof_status = "EXACT_EXTRACTION_NO_A327 / P23SLOT_P23_STILL_FORCED / PARTIAL / EXPERIMENTAL"
        failure = "P23SLOT_P23_STILL_FORCED"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / P23SLOT_NO_STRUCTURAL_PASS / PARTIAL / EXPERIMENTAL"
        failure = "P23SLOT_NO_STRUCTURAL_PASS"

    previous_search = previous["template_vector_repair"]
    best_profile = None if best is None else best.get("best_profile")
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_template_vector_repair": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_mutation_id": previous_search["best_mutation_id"],
            "best_forced_pair_count": previous_search["best_forced_pair_count"],
            "best_forced_pairs": previous_search["best_forced_pairs"],
            "best_slot_nonzero_rows": previous_search["best_slot_nonzero_rows"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "p23_slot_codesign": {
            "base_mutation_id": BEST_PREVIOUS_MUTATION,
            "target_pair": TARGET_PAIR,
            "mutations_generated": len(specs),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": len(candidates),
            "structural_pass_candidates": len(pass_rows),
            "structural_pass_candidates_analyzed": len(selected),
            "structural_pass_candidates_skipped": skipped_structural_pass,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "basis_profiles_tested": sum(row["basis_profiles_tested"] for row in analyzed),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in analyzed),
            "p23_clear_best_profiles": sum(
                1 for row in analyzed if row.get("best_profile") and TARGET_PAIR not in row["best_profile"]["forced_pairs"]
            ),
            "p23_clear_slot_kernel_best_profiles": sum(
                1
                for row in analyzed
                if row.get("best_profile")
                and TARGET_PAIR not in row["best_profile"]["forced_pairs"]
                and row["best_profile"]["slot_nonzero_rows"] == 0
            ),
            "pair_clear_slot_profiles": sum(row["pair_clear_slot_profiles"] for row in analyzed),
            "pair_clear_slot_kernel_profiles": sum(row["pair_clear_slot_kernel_profiles"] for row in analyzed),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_forced_pair_count": None if best_profile is None else best_profile["forced_pair_count"],
            "best_forced_pairs": None if best_profile is None else best_profile["forced_pairs"],
            "best_slot_nonzero_rows": None if best_profile is None else best_profile["slot_nonzero_rows"],
            "best_coefficient_nullity": None if best_profile is None else best_profile["coefficient_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in structural_rows)),
            "candidate_summaries": [candidate_summary(row) for row in analyzed],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "P23_SLOT_KERNEL_CODESIGN",
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
    parser.add_argument("--max-mutations", type=int, default=36)
    parser.add_argument("--max-candidates", type=int, default=24)
    parser.add_argument("--top-classes", type=int, default=14)
    parser.add_argument("--random-bases", type=int, default=0)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["p23_slot_codesign"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "mutations_generated": search["mutations_generated"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "structural_pass_candidates_analyzed": search["structural_pass_candidates_analyzed"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "pair_clear_slot_profiles": search["pair_clear_slot_profiles"],
                    "best_mutation_id": search["best_mutation_id"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_forced_pairs": search["best_forced_pairs"],
                    "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
                    "best_coefficient_nullity": search["best_coefficient_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_P23_SLOT_KERNEL_CODESIGN_READY")


if __name__ == "__main__":
    main()
