#!/usr/bin/env python3
"""Preserve pair-clear slots while reducing slot-kernel rows for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "984fc16"
PREVIOUS_DATA = Path("experimental/data/m1_a327_p23_slot_kernel_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_slot_kernel_row_reduction.json")

ROOT = Path(__file__).resolve().parents[2]
P23_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_p23_slot_kernel_codesign.py"

P = 17
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR_CLEAR_SLOT = 5
BEST_PREVIOUS_MUTATION = "w2_c1_d1"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p23 = load_module("p23_slot_kernel_codesign", P23_SCRIPT)
lowrank = p23.lowrank
zstable = p23.zstable
basisaware = p23.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize(vectors: list[list[int]]) -> list[list[int]]:
    return [[int(value) % P for value in row] for row in vectors]


def best_pairclear_vectors() -> list[list[int]]:
    vectors = p23.best_previous_vectors()
    # BEST_PREVIOUS_MUTATION is w2_c1_d1 in p23 coordinates.
    vectors[1][1] = (vectors[1][1] + 1) % P
    return normalize(vectors)


def template_pairclear(vectors: list[list[int]]) -> bool:
    values = [int(row[PAIR_CLEAR_SLOT]) % P for row in vectors]
    return len(set(values)) == len(values)


def mutation_specs(max_mutations: int) -> list[dict[str, Any]]:
    base = p23.tvpair.base_spec()
    start = best_pairclear_vectors()
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
                "template_id": f"pcslot_{mutation_id}",
                "template_family": "pairclear_slot_kernel_row_reduction",
                "vectors": normalized,
                "base_template_id": "p23slot_w2_c1_d1",
                "mutation_id": mutation_id,
            }
        )

    add("base_w2_c1_d1", [row[:] for row in start])

    # Single-coordinate nudges around the pair-clear template.
    for witness in range(1, 8):
        for col in range(PAIR_CLEAR_SLOT):
            for delta in (1, P - 1, 2, P - 2):
                vectors = [row[:] for row in start]
                vectors[witness - 1][col] = (vectors[witness - 1][col] + delta) % P
                add(f"w{witness}_c{col}_d{delta}", vectors)

    # Two-row shears that often change stable-basis coordinates without
    # disturbing the raw pair-clear slot.
    shear_pairs = [(1, 2), (2, 3), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
    for i, j in shear_pairs:
        for col in range(PAIR_CLEAR_SLOT):
            vectors = [row[:] for row in start]
            vectors[i - 1][col] = (vectors[i - 1][col] + 1) % P
            vectors[j - 1][col] = (vectors[j - 1][col] - 1) % P
            add(f"P{i}{j}_shear_c{col}", vectors)
    return rows


def structural_status(candidate: dict[str, Any]) -> str:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "PCSLOT_SUPPORT_FAIL"
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return "PCSLOT_PAIR_GUARD_FAIL"
    row = zstable.candidate_structural_row(candidate)
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        return row["structural_status"].replace("JOINT_TEMPLATE", "PCSLOT")
    return "PCSLOT_STRUCTURAL_PASS"


def candidate_from_profile(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    candidate = lowrank.evaluate_candidate(profile, strategy, seed=seed)
    candidate["mutation_id"] = profile.get("mutation_id")
    candidate["base_template_id"] = profile.get("base_template_id")
    candidate["total_effective_cost"] = total_effective_cost_gf17(
        profile["template_vectors"],
        candidate["coordinate_classes"],
    )
    return candidate


def rank_rows_mod17(rows: list[list[int]], ncols: int = 6) -> int:
    matrix = [[int(value) % P for value in row] for row in rows if any(int(value) % P for value in row)]
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % P:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, P)
        matrix[rank] = [(value * inv) % P for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % P:
                continue
            factor = matrix[row_idx][col] % P
            matrix[row_idx] = [(matrix[row_idx][idx] - factor * matrix[rank][idx]) % P for idx in range(ncols)]
        rank += 1
    return rank


def affine_rank_gf17(vectors: list[list[int]], members: list[int]) -> int:
    if len(members) <= 1:
        return 0
    anchor = vectors[members[0] - 1]
    rows = []
    for witness in members[1:]:
        rows.append([(int(value) - int(anchor[idx])) % P for idx, value in enumerate(vectors[witness - 1])])
    return rank_rows_mod17(rows, ncols=len(anchor))


def total_effective_cost_gf17(vectors: list[list[int]], coordinates: list[dict[str, Any]]) -> int:
    return sum(affine_rank_gf17(vectors, row["members"]) for row in coordinates)


def profile_sort_key(summary: dict[str, Any]) -> tuple[Any, ...]:
    return (
        summary["forced_pair_count"],
        summary["slot_nonzero_rows"],
        -summary["coefficient_nullity"],
        summary["coefficient_matrix_shape"][0],
        -summary["proxy_kernel_block_degree"],
        summary["basis_id"],
        summary["proxy_kernel_slot"],
    )


def row_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    profile = row.get("best_profile") or {}
    return (
        profile.get("forced_pair_count", 999),
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
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["backward_structural_status"] != "PCSLOT_STRUCTURAL_PASS":
        row["best_failure_mode"] = row["backward_structural_status"]
        return row

    detail = basisaware.analyze_candidate(candidate, top_classes=top_classes, random_bases=random_bases)
    summaries = [dict(summary) for summary in detail["profile_summaries"]]
    summaries.sort(key=profile_sort_key)
    row.update(
        {
            "basis_combos_tested": detail["basis_combos_tested"],
            "basis_profiles_tested": detail["basis_profiles_tested"],
            "slot_profiles_tested": detail["slot_profiles_tested"],
            "pair_clear_slot_profiles": detail["pair_clear_slot_profiles"],
            "pair_clear_slot_kernel_profiles": detail["pair_clear_slot_kernel_profiles"],
            "best_profile": summaries[0] if summaries else None,
            "profile_summaries": summaries[:8],
        }
    )
    if row["pair_clear_slot_kernel_profiles"]:
        row["best_failure_mode"] = "PCSLOT_PAIR_CLEAR_SLOT_KERNEL"
    elif row["pair_clear_slot_profiles"]:
        row["best_failure_mode"] = "PCSLOT_PAIR_CLEAR_SLOT_REDUCE_ROWS"
    elif row["best_profile"] is not None:
        row["best_failure_mode"] = "PCSLOT_PAIR_CLEAR_LOST"
    else:
        row["best_failure_mode"] = "PCSLOT_NO_BASIS_PROFILE"
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
            candidates.append(candidate_from_profile(profile, strategy, seed=83000 + 97 * profile_index + strategy_index))

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
        if row["backward_structural_status"] == "PCSLOT_STRUCTURAL_PASS"
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
    if pair_clear_kernel:
        best = min(pair_clear_kernel, key=row_sort_key)
        proof_status = "CANDIDATE / PCSLOT_PAIR_CLEAR_SLOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "PCSLOT_PAIR_CLEAR_SLOT_KERNEL"
    elif pair_clear:
        best = min(pair_clear, key=row_sort_key)
        proof_status = "CANDIDATE / PCSLOT_PAIR_CLEAR_SLOT_REDUCE_ROWS / PARTIAL / EXPERIMENTAL"
        failure = "PCSLOT_PAIR_CLEAR_SLOT_REDUCE_ROWS"
    elif analyzed:
        best = min(analyzed, key=row_sort_key)
        proof_status = "EXACT_EXTRACTION_NO_A327 / PCSLOT_PAIR_CLEAR_LOST / PARTIAL / EXPERIMENTAL"
        failure = "PCSLOT_PAIR_CLEAR_LOST"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / PCSLOT_NO_STRUCTURAL_PASS / PARTIAL / EXPERIMENTAL"
        failure = "PCSLOT_NO_STRUCTURAL_PASS"

    previous_search = previous["p23_slot_codesign"]
    best_profile = None if best is None else best.get("best_profile")
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_p23_slot_codesign": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_mutation_id": previous_search["best_mutation_id"],
            "pair_clear_slot_profiles": previous_search["pair_clear_slot_profiles"],
            "best_forced_pair_count": previous_search["best_forced_pair_count"],
            "best_forced_pairs": previous_search["best_forced_pairs"],
            "best_slot_nonzero_rows": previous_search["best_slot_nonzero_rows"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "pairclear_slot_row_reduction": {
            "base_mutation_id": BEST_PREVIOUS_MUTATION,
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
        "realization_status": "PAIRCLEAR_SLOT_KERNEL_ROW_REDUCTION",
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
    parser.add_argument("--max-mutations", type=int, default=48)
    parser.add_argument("--max-candidates", type=int, default=48)
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
        search = record["pairclear_slot_row_reduction"]
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
                    "pair_clear_slot_kernel_profiles": search["pair_clear_slot_kernel_profiles"],
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
        print("M1_A327_PAIRCLEAR_SLOT_KERNEL_ROW_REDUCTION_READY")


if __name__ == "__main__":
    main()
