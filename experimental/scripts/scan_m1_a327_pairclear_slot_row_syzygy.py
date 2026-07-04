#!/usr/bin/env python3
"""Search pair-clear low-support slot directions for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "8ae0631"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_slot_kernel_row_reduction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_slot_row_syzygy.json")

ROOT = Path(__file__).resolve().parents[2]
ROWRED_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_slot_kernel_row_reduction.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR_CLEAR_SLOT = 5
BEST_ROWRED_MUTATION = "w1_c3_d1"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rowred = load_module("pairclear_slot_kernel_row_reduction", ROWRED_SCRIPT)
lowrank = rowred.lowrank
zstable = rowred.zstable
basisaware = rowred.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize(vectors: list[list[int]]) -> list[list[int]]:
    return [[int(value) % P for value in row] for row in vectors]


def best_rowreduction_vectors() -> list[list[int]]:
    vectors = rowred.best_pairclear_vectors()
    # BEST_ROWRED_MUTATION is w1_c3_d1 relative to the 984fc16 pair-clear base.
    vectors[0][3] = (vectors[0][3] + 1) % P
    return normalize(vectors)


def template_pairclear(vectors: list[list[int]]) -> bool:
    values = [int(row[PAIR_CLEAR_SLOT]) % P for row in vectors]
    return len(set(values)) == len(values)


def mutation_specs(max_mutations: int) -> list[dict[str, Any]]:
    base = rowred.p23.tvpair.base_spec()
    start = best_rowreduction_vectors()
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
                "template_id": f"pcsyzygy_{mutation_id}",
                "template_family": "pairclear_slot_row_syzygy",
                "vectors": normalized,
                "base_template_id": "pcslot_w1_c3_d1",
                "mutation_id": mutation_id,
            }
        )

    add("base_w1_c3_d1", [row[:] for row in start])

    for witness in range(1, 8):
        for col in range(PAIR_CLEAR_SLOT):
            for delta in (1, P - 1, 2, P - 2, 3, P - 3):
                vectors = [row[:] for row in start]
                vectors[witness - 1][col] = (vectors[witness - 1][col] + delta) % P
                add(f"w{witness}_c{col}_d{delta}", vectors)

    shear_pairs = [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 7),
        (2, 3),
        (2, 7),
        (3, 7),
        (4, 5),
        (4, 7),
        (5, 7),
        (6, 7),
    ]
    for i, j in shear_pairs:
        for col in range(PAIR_CLEAR_SLOT):
            for delta in (1, P - 1, 2, P - 2):
                vectors = [row[:] for row in start]
                vectors[i - 1][col] = (vectors[i - 1][col] + delta) % P
                vectors[j - 1][col] = (vectors[j - 1][col] - delta) % P
                add(f"P{i}{j}_shear_c{col}_d{delta}", vectors)

    return rows


def candidate_from_profile(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    candidate = lowrank.evaluate_candidate(profile, strategy, seed=seed)
    candidate["mutation_id"] = profile.get("mutation_id")
    candidate["base_template_id"] = profile.get("base_template_id")
    candidate["total_effective_cost"] = rowred.total_effective_cost_gf17(
        profile["template_vectors"],
        candidate["coordinate_classes"],
    )
    return candidate


def structural_status(candidate: dict[str, Any]) -> str:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "PCSYZ_SUPPORT_FAIL"
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return "PCSYZ_PAIR_GUARD_FAIL"
    row = zstable.candidate_structural_row(candidate)
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        return row["structural_status"].replace("JOINT_TEMPLATE", "PCSYZ")
    return "PCSYZ_STRUCTURAL_PASS"


def dot(row: list[int] | tuple[int, ...], vector: list[int] | tuple[int, ...]) -> int:
    return sum(int(row[idx]) * int(vector[idx]) for idx in range(TEMPLATE_DIM)) % P


def direction_vectors(anchor_slot: int, max_extra: int) -> list[list[int]]:
    vectors = []
    seen: set[tuple[int, ...]] = set()
    other = [idx for idx in range(TEMPLATE_DIM) if idx != anchor_slot]
    for extra_count in range(0, max_extra + 1):
        for coords in itertools.combinations(other, extra_count):
            if not coords:
                values_iter = [()]
            else:
                values_iter = itertools.product(range(1, P), repeat=extra_count)
            for values in values_iter:
                vector = [0] * TEMPLATE_DIM
                vector[anchor_slot] = 1
                for coord, value in zip(coords, values, strict=True):
                    vector[coord] = int(value) % P
                key = tuple(vector)
                if key in seen:
                    continue
                seen.add(key)
                vectors.append(vector)
    return vectors


def reconstruct_profile(candidate: dict[str, Any], basis_class_indices: list[int], basis_id: str) -> tuple[list[dict[str, Any]], dict[str, Any]] | None:
    classes = basisaware.functional.functional_classes(candidate)
    by_class = {int(row["class_index"]): idx for idx, row in enumerate(classes)}
    try:
        combo = tuple(by_class[int(class_index)] for class_index in basis_class_indices)
    except KeyError:
        return None
    profile = basisaware.profile_from_indices(classes, combo, basis_id)
    if profile is None:
        return None
    return classes, profile


def pair_projection_for_vector(candidate: dict[str, Any], profile: dict[str, Any], vector: list[int]) -> dict[str, Any]:
    scalars = zstable.zexp.pair_projection_scalars(candidate, profile, vector)
    forced = [label for label, value in scalars.items() if int(value) % P == 0]
    return {
        "forced_pair_count": len(forced),
        "forced_pairs": forced,
        "pair_projection_scalars": scalars,
    }


def direction_summary(candidate: dict[str, Any], summary: dict[str, Any], max_extra: int) -> dict[str, Any] | None:
    reconstructed = reconstruct_profile(candidate, summary["basis_class_indices"], summary["basis_id"])
    if reconstructed is None:
        return None
    _classes, profile = reconstructed
    matrix = zstable.coefficient_matrix(profile)
    anchor_slot = int(summary["proxy_kernel_slot"])
    best = None
    tested = 0
    pair_clear_count = 0
    kernel_count = 0
    for vector in direction_vectors(anchor_slot, max_extra=max_extra):
        tested += 1
        row_values = [dot(row, vector) for row in matrix]
        nonzero_indices = [idx for idx, value in enumerate(row_values) if value % P]
        pair_record = pair_projection_for_vector(candidate, profile, vector)
        if pair_record["forced_pair_count"] == 0:
            pair_clear_count += 1
            if not nonzero_indices:
                kernel_count += 1
        record = {
            "basis_id": profile["basis_id"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "anchor_slot": anchor_slot,
            "direction_vector": vector,
            "direction_weight": sum(1 for value in vector if value % P),
            "directions_tested": tested,
            "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
            "direction_nonzero_rows": len(nonzero_indices),
            "direction_nonzero_row_indices": nonzero_indices,
            "direction_nonzero_row_classes": [
                int(profile["nonbasis_constraint_detail"][idx]["class_index"]) for idx in nonzero_indices
            ],
            **pair_record,
        }
        key = (
            record["forced_pair_count"],
            record["direction_nonzero_rows"],
            record["direction_weight"],
            record["direction_vector"],
        )
        if best is None or key < best[0]:
            best = (key, record)
    if best is None:
        return None
    best_record = dict(best[1])
    best_record["directions_tested"] = tested
    best_record["pair_clear_directions"] = pair_clear_count
    best_record["pair_clear_direction_kernels"] = kernel_count
    failure = "PCSYZ_DIRECTION_PAIR_CLEAR_KERNEL"
    if best_record["forced_pair_count"] > 0:
        failure = "PCSYZ_DIRECTION_FORCED_PAIR"
    elif best_record["direction_nonzero_rows"] > 0:
        failure = "PCSYZ_DIRECTION_REDUCE_ROWS"
    best_record["best_failure_mode"] = failure
    return best_record


def direction_sort_key(summary: dict[str, Any]) -> tuple[Any, ...]:
    return (
        summary["forced_pair_count"],
        summary["direction_nonzero_rows"],
        summary["direction_weight"],
        summary["basis_id"],
        summary["anchor_slot"],
        summary["direction_vector"],
    )


def row_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    direction = row.get("best_direction") or {}
    profile = row.get("best_profile") or {}
    return (
        direction.get("forced_pair_count", 999),
        direction.get("direction_nonzero_rows", 999),
        profile.get("slot_nonzero_rows", 999),
        row.get("template_id", ""),
        row.get("assignment_strategy", ""),
    )


def analyze_candidate(candidate: dict[str, Any], top_classes: int, random_bases: int, direction_max_extra: int) -> dict[str, Any]:
    row = rowred.analyze_candidate(candidate, top_classes=top_classes, random_bases=random_bases)
    row["mutation_id"] = candidate.get("mutation_id")
    row["base_template_id"] = candidate.get("base_template_id")
    row["backward_structural_status"] = structural_status(candidate)
    row["direction_profiles_tested"] = 0
    row["direction_vectors_tested"] = 0
    row["pair_clear_direction_profiles"] = 0
    row["pair_clear_direction_kernel_profiles"] = 0
    row["row_reduced_direction_profiles"] = 0
    row["best_direction"] = None
    row["direction_summaries"] = []
    if row["backward_structural_status"] != "PCSYZ_STRUCTURAL_PASS":
        row["best_failure_mode"] = row["backward_structural_status"]
        return row

    direction_summaries = []
    for summary in row.get("profile_summaries", []):
        if int(summary.get("forced_pair_count", 999)) != 0:
            continue
        direction = direction_summary(candidate, summary, max_extra=direction_max_extra)
        if direction is None:
            continue
        row["direction_profiles_tested"] += 1
        row["direction_vectors_tested"] += direction["directions_tested"]
        direction_summaries.append(direction)

    direction_summaries.sort(key=direction_sort_key)
    row["direction_summaries"] = direction_summaries[:8]
    row["best_direction"] = row["direction_summaries"][0] if row["direction_summaries"] else None
    row["pair_clear_direction_profiles"] = sum(1 for item in direction_summaries if item["forced_pair_count"] == 0)
    row["pair_clear_direction_kernel_profiles"] = sum(
        1 for item in direction_summaries if item["forced_pair_count"] == 0 and item["direction_nonzero_rows"] == 0
    )
    row["row_reduced_direction_profiles"] = sum(
        1
        for item in direction_summaries
        if item["forced_pair_count"] == 0
        and row.get("best_profile") is not None
        and item["direction_nonzero_rows"] < int(row["best_profile"]["slot_nonzero_rows"])
    )

    if row["pair_clear_direction_kernel_profiles"]:
        row["best_failure_mode"] = "PCSYZ_DIRECTION_PAIR_CLEAR_KERNEL"
    elif row["row_reduced_direction_profiles"]:
        row["best_failure_mode"] = "PCSYZ_DIRECTION_REDUCE_ROWS"
    elif row["pair_clear_direction_profiles"]:
        row["best_failure_mode"] = "PCSYZ_DIRECTION_PAIR_CLEAR_NO_REDUCTION"
    elif row["direction_summaries"]:
        row["best_failure_mode"] = "PCSYZ_DIRECTION_FORCED_PAIR"
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
        "direction_profiles_tested",
        "direction_vectors_tested",
        "pair_clear_direction_profiles",
        "pair_clear_direction_kernel_profiles",
        "row_reduced_direction_profiles",
        "best_failure_mode",
        "best_profile",
        "best_direction",
        "direction_summaries",
    ]
    return {key: row.get(key) for key in keys}


def build_record(
    max_mutations: int,
    max_candidates: int,
    top_classes: int,
    random_bases: int,
    direction_max_extra: int,
) -> dict[str, Any]:
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
            candidates.append(candidate_from_profile(profile, strategy, seed=93000 + 97 * profile_index + strategy_index))

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
        if row["backward_structural_status"] == "PCSYZ_STRUCTURAL_PASS"
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
    analyzed = [
        analyze_candidate(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            direction_max_extra=direction_max_extra,
        )
        for candidate, _row in selected
    ]
    skipped_structural_pass = max(0, len(pass_rows) - len(selected))

    kernel_rows = [
        row
        for row in analyzed
        if row.get("best_direction") is not None
        and row["best_direction"]["forced_pair_count"] == 0
        and row["best_direction"]["direction_nonzero_rows"] == 0
    ]
    reduced_rows = [
        row
        for row in analyzed
        if row.get("best_direction") is not None
        and row["best_direction"]["forced_pair_count"] == 0
        and row.get("best_profile") is not None
        and row["best_direction"]["direction_nonzero_rows"] < row["best_profile"]["slot_nonzero_rows"]
    ]
    pair_clear_rows = [
        row
        for row in analyzed
        if row.get("best_direction") is not None
        and row["best_direction"]["forced_pair_count"] == 0
    ]
    if kernel_rows:
        best = min(kernel_rows, key=row_sort_key)
        proof_status = "CANDIDATE / PCSYZ_DIRECTION_PAIR_CLEAR_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "PCSYZ_DIRECTION_PAIR_CLEAR_KERNEL"
    elif reduced_rows:
        best = min(reduced_rows, key=row_sort_key)
        proof_status = "CANDIDATE / PCSYZ_DIRECTION_REDUCE_ROWS / PARTIAL / EXPERIMENTAL"
        failure = "PCSYZ_DIRECTION_REDUCE_ROWS"
    elif pair_clear_rows:
        best = min(pair_clear_rows, key=row_sort_key)
        proof_status = "CANDIDATE / PCSYZ_DIRECTION_PAIR_CLEAR_NO_REDUCTION / PARTIAL / EXPERIMENTAL"
        failure = "PCSYZ_DIRECTION_PAIR_CLEAR_NO_REDUCTION"
    elif analyzed:
        best = min(analyzed, key=row_sort_key)
        proof_status = "EXACT_EXTRACTION_NO_A327 / PCSYZ_DIRECTION_FORCED_PAIR / PARTIAL / EXPERIMENTAL"
        failure = "PCSYZ_DIRECTION_FORCED_PAIR"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / PCSYZ_NO_STRUCTURAL_PASS / PARTIAL / EXPERIMENTAL"
        failure = "PCSYZ_NO_STRUCTURAL_PASS"

    previous_search = previous["pairclear_slot_row_reduction"]
    best_direction = None if best is None else best.get("best_direction")
    best_profile = None if best is None else best.get("best_profile")
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_pairclear_slot_row_reduction": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_mutation_id": previous_search["best_mutation_id"],
            "pair_clear_slot_profiles": previous_search["pair_clear_slot_profiles"],
            "pair_clear_slot_kernel_profiles": previous_search["pair_clear_slot_kernel_profiles"],
            "best_forced_pair_count": previous_search["best_forced_pair_count"],
            "best_forced_pairs": previous_search["best_forced_pairs"],
            "best_slot_nonzero_rows": previous_search["best_slot_nonzero_rows"],
            "best_coefficient_nullity": previous_search["best_coefficient_nullity"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "pairclear_slot_row_syzygy": {
            "base_mutation_id": BEST_ROWRED_MUTATION,
            "mutations_generated": len(specs),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": len(candidates),
            "structural_pass_candidates": len(pass_rows),
            "structural_pass_candidates_analyzed": len(selected),
            "structural_pass_candidates_skipped": skipped_structural_pass,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "direction_max_extra": direction_max_extra,
            "basis_profiles_tested": sum(row["basis_profiles_tested"] for row in analyzed),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in analyzed),
            "pair_clear_slot_profiles": sum(row["pair_clear_slot_profiles"] for row in analyzed),
            "pair_clear_slot_kernel_profiles": sum(row["pair_clear_slot_kernel_profiles"] for row in analyzed),
            "direction_profiles_tested": sum(row["direction_profiles_tested"] for row in analyzed),
            "direction_vectors_tested": sum(row["direction_vectors_tested"] for row in analyzed),
            "pair_clear_direction_profiles": sum(row["pair_clear_direction_profiles"] for row in analyzed),
            "pair_clear_direction_kernel_profiles": sum(row["pair_clear_direction_kernel_profiles"] for row in analyzed),
            "row_reduced_direction_profiles": sum(row["row_reduced_direction_profiles"] for row in analyzed),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_unit_slot_nonzero_rows": None if best_profile is None else best_profile["slot_nonzero_rows"],
            "best_direction_nonzero_rows": None if best_direction is None else best_direction["direction_nonzero_rows"],
            "best_direction_forced_pair_count": None if best_direction is None else best_direction["forced_pair_count"],
            "best_direction_forced_pairs": None if best_direction is None else best_direction["forced_pairs"],
            "best_direction_vector": None if best_direction is None else best_direction["direction_vector"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in structural_rows)),
            "candidate_summaries": [candidate_summary(row) for row in analyzed],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "PAIRCLEAR_SLOT_ROW_SYZYGY",
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
    parser.add_argument("--max-candidates", type=int, default=24)
    parser.add_argument("--top-classes", type=int, default=14)
    parser.add_argument("--random-bases", type=int, default=0)
    parser.add_argument("--direction-max-extra", type=int, default=1)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        direction_max_extra=args.direction_max_extra,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["pairclear_slot_row_syzygy"]
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
                    "direction_profiles_tested": search["direction_profiles_tested"],
                    "direction_vectors_tested": search["direction_vectors_tested"],
                    "pair_clear_direction_profiles": search["pair_clear_direction_profiles"],
                    "pair_clear_direction_kernel_profiles": search["pair_clear_direction_kernel_profiles"],
                    "row_reduced_direction_profiles": search["row_reduced_direction_profiles"],
                    "best_mutation_id": search["best_mutation_id"],
                    "best_unit_slot_nonzero_rows": search["best_unit_slot_nonzero_rows"],
                    "best_direction_nonzero_rows": search["best_direction_nonzero_rows"],
                    "best_direction_forced_pair_count": search["best_direction_forced_pair_count"],
                    "best_direction_forced_pairs": search["best_direction_forced_pairs"],
                    "best_direction_vector": search["best_direction_vector"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_SLOT_ROW_SYZYGY_READY")


if __name__ == "__main__":
    main()
