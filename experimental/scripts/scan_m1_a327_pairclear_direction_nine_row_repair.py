#!/usr/bin/env python3
"""Repair the pinned nine-row pair-clear direction for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "402d88c"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_slot_row_syzygy.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_direction_nine_row_repair.json")

ROOT = Path(__file__).resolve().parents[2]
SYZYGY_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_slot_row_syzygy.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PAIR_CLEAR_SLOT = 5
TARGET_BASIS_CLASS_INDICES = [1, 4, 7, 8, 9, 10]
PINNED_DIRECTION = [0, 5, 0, 0, 0, 1]
PREVIOUS_ACTIVE_CLASSES = [0, 2, 3, 5, 6, 11, 12, 14, 15]
BASE_MUTATION_ID = "base_w1_c3_d1"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


syzygy = load_module("pairclear_slot_row_syzygy", SYZYGY_SCRIPT)
lowrank = syzygy.lowrank
zstable = syzygy.zstable
basisaware = syzygy.basisaware


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize(vectors: list[list[int]]) -> list[list[int]]:
    return [[int(value) % P for value in row] for row in vectors]


def base_vectors() -> list[list[int]]:
    return syzygy.best_rowreduction_vectors()


def template_pairclear(vectors: list[list[int]]) -> bool:
    values = [int(row[PAIR_CLEAR_SLOT]) % P for row in vectors]
    return len(set(values)) == len(values)


def mutation_specs(max_mutations: int) -> list[dict[str, Any]]:
    base = syzygy.rowred.p23.tvpair.base_spec()
    start = base_vectors()
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
                "template_id": f"ninerow_{mutation_id}",
                "template_family": "pairclear_direction_nine_row_repair",
                "vectors": normalized,
                "base_template_id": "pcsyzygy_base_w1_c3_d1",
                "mutation_id": mutation_id,
            }
        )

    add(BASE_MUTATION_ID, [row[:] for row in start])

    for witness in range(1, 8):
        for col in range(PAIR_CLEAR_SLOT):
            for delta in (1, P - 1, 2, P - 2, 3, P - 3, 4, P - 4):
                vectors = [row[:] for row in start]
                vectors[witness - 1][col] = (vectors[witness - 1][col] + delta) % P
                add(f"w{witness}_c{col}_d{delta}", vectors)

    shear_pairs = [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 7),
        (2, 3),
        (2, 4),
        (2, 7),
        (3, 4),
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

    # A small second-order front near the row-reduction mutation that created
    # the nine-row direction. Keep this after first-order moves so bounded runs
    # remain deterministic and easy to reproduce.
    for witness_a, witness_b in itertools.combinations(range(1, 8), 2):
        for col_a, col_b in ((3, 0), (3, 1), (3, 2), (2, 3), (1, 3)):
            vectors = [row[:] for row in start]
            vectors[witness_a - 1][col_a] = (vectors[witness_a - 1][col_a] + 1) % P
            vectors[witness_b - 1][col_b] = (vectors[witness_b - 1][col_b] - 1) % P
            add(f"W{witness_a}{witness_b}_c{col_a}{col_b}_pm1", vectors)
    return rows


def candidate_from_profile(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    candidate = lowrank.evaluate_candidate(profile, strategy, seed=seed)
    candidate["mutation_id"] = profile.get("mutation_id")
    candidate["base_template_id"] = profile.get("base_template_id")
    candidate["total_effective_cost"] = syzygy.rowred.total_effective_cost_gf17(
        profile["template_vectors"],
        candidate["coordinate_classes"],
    )
    return candidate


def structural_status(candidate: dict[str, Any]) -> str:
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "NINEROW_SUPPORT_FAIL"
    if candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        return "NINEROW_PAIR_GUARD_FAIL"
    row = zstable.candidate_structural_row(candidate)
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        return row["structural_status"].replace("JOINT_TEMPLATE", "NINEROW")
    return "NINEROW_STRUCTURAL_PASS"


def reconstruct_target_profile(candidate: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]] | None:
    classes = basisaware.functional.functional_classes(candidate)
    by_class = {int(row["class_index"]): idx for idx, row in enumerate(classes)}
    try:
        combo = tuple(by_class[int(class_index)] for class_index in TARGET_BASIS_CLASS_INDICES)
    except KeyError:
        return None
    profile = basisaware.profile_from_indices(
        classes,
        combo,
        "basisaware_" + "_".join(str(item) for item in TARGET_BASIS_CLASS_INDICES),
    )
    if profile is None:
        return None
    return classes, profile


def dot(row: list[int] | tuple[int, ...], vector: list[int] | tuple[int, ...]) -> int:
    return sum(int(row[idx]) * int(vector[idx]) for idx in range(TEMPLATE_DIM)) % P


def direction_record(candidate: dict[str, Any], profile: dict[str, Any], vector: list[int], label: str) -> dict[str, Any]:
    matrix = zstable.coefficient_matrix(profile)
    row_values = [dot(row, vector) for row in matrix]
    nonzero_indices = [idx for idx, value in enumerate(row_values) if value % P]
    scalars = zstable.zexp.pair_projection_scalars(candidate, profile, vector)
    forced = [pair for pair, value in scalars.items() if int(value) % P == 0]
    row_classes = [int(profile["nonbasis_constraint_detail"][idx]["class_index"]) for idx in nonzero_indices]
    previous = set(PREVIOUS_ACTIVE_CLASSES)
    current = set(row_classes)
    return {
        "direction_label": label,
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "direction_vector": [int(value) % P for value in vector],
        "direction_weight": sum(1 for value in vector if int(value) % P),
        "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
        "direction_nonzero_rows": len(nonzero_indices),
        "direction_nonzero_row_indices": nonzero_indices,
        "direction_nonzero_row_classes": row_classes,
        "previous_active_rows_retained": len(previous & current),
        "previous_active_rows_removed": sorted(previous - current),
        "new_active_rows_introduced": sorted(current - previous),
        "forced_pair_count": len(forced),
        "forced_pairs": forced,
        "pair_projection_scalars": scalars,
    }


def local_directions(max_extra: int) -> list[list[int]]:
    return syzygy.direction_vectors(anchor_slot=PAIR_CLEAR_SLOT, max_extra=max_extra)


def best_local_direction(candidate: dict[str, Any], profile: dict[str, Any], max_extra: int) -> dict[str, Any]:
    best = None
    tested = 0
    pair_clear_count = 0
    kernel_count = 0
    row_reduced_count = 0
    for vector in local_directions(max_extra):
        tested += 1
        record = direction_record(candidate, profile, vector, "local")
        if record["forced_pair_count"] == 0:
            pair_clear_count += 1
            if record["direction_nonzero_rows"] == 0:
                kernel_count += 1
            if record["direction_nonzero_rows"] < len(PREVIOUS_ACTIVE_CLASSES):
                row_reduced_count += 1
        key = (
            record["forced_pair_count"],
            record["direction_nonzero_rows"],
            record["direction_weight"],
            record["previous_active_rows_retained"],
            record["direction_vector"],
        )
        if best is None or key < best[0]:
            best = (key, record)
    if best is None:
        return {
            "directions_tested": tested,
            "pair_clear_directions": pair_clear_count,
            "pair_clear_direction_kernels": kernel_count,
            "row_reduced_directions": row_reduced_count,
        }
    out = dict(best[1])
    out["directions_tested"] = tested
    out["pair_clear_directions"] = pair_clear_count
    out["pair_clear_direction_kernels"] = kernel_count
    out["row_reduced_directions"] = row_reduced_count
    return out


def analyze_candidate(candidate: dict[str, Any], direction_max_extra: int) -> dict[str, Any]:
    row = zstable.candidate_structural_row(candidate)
    row["mutation_id"] = candidate.get("mutation_id")
    row["base_template_id"] = candidate.get("base_template_id")
    row["backward_structural_status"] = structural_status(candidate)
    row["target_basis_present"] = False
    row["fixed_direction"] = None
    row["best_local_direction"] = None
    row["directions_tested"] = 0
    row["pair_clear_directions"] = 0
    row["row_reduced_directions"] = 0
    row["pair_clear_direction_kernels"] = 0
    if row["backward_structural_status"] != "NINEROW_STRUCTURAL_PASS":
        row["best_failure_mode"] = row["backward_structural_status"]
        return row

    reconstructed = reconstruct_target_profile(candidate)
    if reconstructed is None:
        row["best_failure_mode"] = "NINEROW_TARGET_BASIS_MISSING"
        return row
    _classes, profile = reconstructed
    row["target_basis_present"] = True
    row["fixed_direction"] = direction_record(candidate, profile, PINNED_DIRECTION, "pinned")
    local = best_local_direction(candidate, profile, max_extra=direction_max_extra)
    row["best_local_direction"] = local
    row["directions_tested"] = local.get("directions_tested", 0)
    row["pair_clear_directions"] = local.get("pair_clear_directions", 0)
    row["row_reduced_directions"] = local.get("row_reduced_directions", 0)
    row["pair_clear_direction_kernels"] = local.get("pair_clear_direction_kernels", 0)

    fixed = row["fixed_direction"]
    if fixed["forced_pair_count"] == 0 and fixed["direction_nonzero_rows"] == 0:
        row["best_failure_mode"] = "NINEROW_FIXED_DIRECTION_KERNEL"
    elif local.get("forced_pair_count") == 0 and local.get("direction_nonzero_rows") == 0:
        row["best_failure_mode"] = "NINEROW_LOCAL_DIRECTION_KERNEL"
    elif fixed["forced_pair_count"] == 0 and fixed["direction_nonzero_rows"] < len(PREVIOUS_ACTIVE_CLASSES):
        row["best_failure_mode"] = "NINEROW_FIXED_DIRECTION_REDUCE_ROWS"
    elif local.get("forced_pair_count") == 0 and local.get("direction_nonzero_rows", 999) < len(PREVIOUS_ACTIVE_CLASSES):
        row["best_failure_mode"] = "NINEROW_LOCAL_DIRECTION_REDUCE_ROWS"
    elif fixed["forced_pair_count"] == 0:
        row["best_failure_mode"] = "NINEROW_FIXED_DIRECTION_STABLE"
    elif local.get("forced_pair_count") == 0:
        row["best_failure_mode"] = "NINEROW_LOCAL_DIRECTION_STABLE"
    else:
        row["best_failure_mode"] = "NINEROW_DIRECTION_FORCED_PAIR"
    return row


def record_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    fixed = row.get("fixed_direction") or {}
    local = row.get("best_local_direction") or {}
    best_forced = min(fixed.get("forced_pair_count", 999), local.get("forced_pair_count", 999))
    best_rows = min(fixed.get("direction_nonzero_rows", 999), local.get("direction_nonzero_rows", 999))
    fixed_rows = fixed.get("direction_nonzero_rows", 999)
    return (
        best_forced,
        best_rows,
        fixed.get("forced_pair_count", 999),
        fixed_rows,
        row.get("template_id", ""),
        row.get("assignment_strategy", ""),
    )


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
        "target_basis_present",
        "directions_tested",
        "pair_clear_directions",
        "row_reduced_directions",
        "pair_clear_direction_kernels",
        "best_failure_mode",
        "fixed_direction",
        "best_local_direction",
    ]
    return {key: row.get(key) for key in keys}


def build_record(max_mutations: int, max_candidates: int, direction_max_extra: int) -> dict[str, Any]:
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
            candidates.append(candidate_from_profile(profile, strategy, seed=104000 + 97 * profile_index + strategy_index))

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
        if row["backward_structural_status"] == "NINEROW_STRUCTURAL_PASS"
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
    analyzed = [analyze_candidate(candidate, direction_max_extra=direction_max_extra) for candidate, _row in selected]
    skipped_structural_pass = max(0, len(pass_rows) - len(selected))

    fixed_kernels = [
        row
        for row in analyzed
        if row.get("fixed_direction")
        and row["fixed_direction"]["forced_pair_count"] == 0
        and row["fixed_direction"]["direction_nonzero_rows"] == 0
    ]
    local_kernels = [
        row
        for row in analyzed
        if row.get("best_local_direction")
        and row["best_local_direction"].get("forced_pair_count") == 0
        and row["best_local_direction"].get("direction_nonzero_rows") == 0
    ]
    fixed_reduced = [
        row
        for row in analyzed
        if row.get("fixed_direction")
        and row["fixed_direction"]["forced_pair_count"] == 0
        and row["fixed_direction"]["direction_nonzero_rows"] < len(PREVIOUS_ACTIVE_CLASSES)
    ]
    local_reduced = [
        row
        for row in analyzed
        if row.get("best_local_direction")
        and row["best_local_direction"].get("forced_pair_count") == 0
        and row["best_local_direction"].get("direction_nonzero_rows", 999) < len(PREVIOUS_ACTIVE_CLASSES)
    ]
    fixed_stable = [
        row
        for row in analyzed
        if row.get("fixed_direction")
        and row["fixed_direction"]["forced_pair_count"] == 0
        and row["fixed_direction"]["direction_nonzero_rows"] == len(PREVIOUS_ACTIVE_CLASSES)
    ]

    if fixed_kernels:
        best = min(fixed_kernels, key=record_sort_key)
        proof_status = "CANDIDATE / NINEROW_FIXED_DIRECTION_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "NINEROW_FIXED_DIRECTION_KERNEL"
    elif local_kernels:
        best = min(local_kernels, key=record_sort_key)
        proof_status = "CANDIDATE / NINEROW_LOCAL_DIRECTION_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "NINEROW_LOCAL_DIRECTION_KERNEL"
    elif fixed_reduced:
        best = min(fixed_reduced, key=record_sort_key)
        proof_status = "CANDIDATE / NINEROW_FIXED_DIRECTION_REDUCE_ROWS / PARTIAL / EXPERIMENTAL"
        failure = "NINEROW_FIXED_DIRECTION_REDUCE_ROWS"
    elif local_reduced:
        best = min(local_reduced, key=record_sort_key)
        proof_status = "CANDIDATE / NINEROW_LOCAL_DIRECTION_REDUCE_ROWS / PARTIAL / EXPERIMENTAL"
        failure = "NINEROW_LOCAL_DIRECTION_REDUCE_ROWS"
    elif fixed_stable:
        best = min(fixed_stable, key=record_sort_key)
        proof_status = "CANDIDATE / NINEROW_FIXED_DIRECTION_STABLE / PARTIAL / EXPERIMENTAL"
        failure = "NINEROW_FIXED_DIRECTION_STABLE"
    elif analyzed:
        best = min(analyzed, key=record_sort_key)
        proof_status = "EXACT_EXTRACTION_NO_A327 / NINEROW_DIRECTION_FORCED_PAIR / PARTIAL / EXPERIMENTAL"
        failure = "NINEROW_DIRECTION_FORCED_PAIR"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / NINEROW_NO_STRUCTURAL_PASS / PARTIAL / EXPERIMENTAL"
        failure = "NINEROW_NO_STRUCTURAL_PASS"

    previous_search = previous["pairclear_slot_row_syzygy"]
    best_fixed = None if best is None else best.get("fixed_direction")
    best_local = None if best is None else best.get("best_local_direction")
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_pairclear_slot_row_syzygy": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_mutation_id": previous_search["best_mutation_id"],
            "best_direction_vector": previous_search["best_direction_vector"],
            "best_direction_nonzero_rows": previous_search["best_direction_nonzero_rows"],
            "best_direction_forced_pair_count": previous_search["best_direction_forced_pair_count"],
            "best_direction_forced_pairs": previous_search["best_direction_forced_pairs"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "target_nine_row_system": {
            "target_basis_class_indices": TARGET_BASIS_CLASS_INDICES,
            "pinned_direction": PINNED_DIRECTION,
            "previous_active_row_classes": PREVIOUS_ACTIVE_CLASSES,
        },
        "nine_row_repair": {
            "base_mutation_id": BASE_MUTATION_ID,
            "mutations_generated": len(specs),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": len(candidates),
            "structural_pass_candidates": len(pass_rows),
            "structural_pass_candidates_analyzed": len(selected),
            "structural_pass_candidates_skipped": skipped_structural_pass,
            "direction_max_extra": direction_max_extra,
            "target_basis_profiles_present": sum(1 for row in analyzed if row.get("target_basis_present")),
            "directions_tested": sum(row.get("directions_tested", 0) for row in analyzed),
            "pair_clear_directions": sum(row.get("pair_clear_directions", 0) for row in analyzed),
            "row_reduced_directions": sum(row.get("row_reduced_directions", 0) for row in analyzed),
            "pair_clear_direction_kernels": sum(row.get("pair_clear_direction_kernels", 0) for row in analyzed),
            "fixed_direction_pair_clear_profiles": sum(
                1
                for row in analyzed
                if row.get("fixed_direction") and row["fixed_direction"]["forced_pair_count"] == 0
            ),
            "fixed_direction_row_reduced_profiles": sum(
                1
                for row in analyzed
                if row.get("fixed_direction")
                and row["fixed_direction"]["forced_pair_count"] == 0
                and row["fixed_direction"]["direction_nonzero_rows"] < len(PREVIOUS_ACTIVE_CLASSES)
            ),
            "fixed_direction_kernel_profiles": len(fixed_kernels),
            "local_direction_row_reduced_profiles": len(local_reduced),
            "local_direction_kernel_profiles": len(local_kernels),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_fixed_direction_nonzero_rows": None if best_fixed is None else best_fixed["direction_nonzero_rows"],
            "best_fixed_direction_forced_pair_count": None if best_fixed is None else best_fixed["forced_pair_count"],
            "best_local_direction_nonzero_rows": None if best_local is None else best_local.get("direction_nonzero_rows"),
            "best_local_direction_forced_pair_count": None if best_local is None else best_local.get("forced_pair_count"),
            "best_local_direction_vector": None if best_local is None else best_local.get("direction_vector"),
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in structural_rows)),
            "candidate_summaries": [candidate_summary(row) for row in analyzed],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "PAIRCLEAR_DIRECTION_NINE_ROW_REPAIR",
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
    parser.add_argument("--max-mutations", type=int, default=72)
    parser.add_argument("--max-candidates", type=int, default=36)
    parser.add_argument("--direction-max-extra", type=int, default=2)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        direction_max_extra=args.direction_max_extra,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["nine_row_repair"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "mutations_generated": search["mutations_generated"],
                    "candidate_systems_constructed": search["candidate_systems_constructed"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "structural_pass_candidates_analyzed": search["structural_pass_candidates_analyzed"],
                    "target_basis_profiles_present": search["target_basis_profiles_present"],
                    "directions_tested": search["directions_tested"],
                    "pair_clear_directions": search["pair_clear_directions"],
                    "row_reduced_directions": search["row_reduced_directions"],
                    "pair_clear_direction_kernels": search["pair_clear_direction_kernels"],
                    "fixed_direction_pair_clear_profiles": search["fixed_direction_pair_clear_profiles"],
                    "fixed_direction_row_reduced_profiles": search["fixed_direction_row_reduced_profiles"],
                    "best_mutation_id": search["best_mutation_id"],
                    "best_fixed_direction_nonzero_rows": search["best_fixed_direction_nonzero_rows"],
                    "best_fixed_direction_forced_pair_count": search["best_fixed_direction_forced_pair_count"],
                    "best_local_direction_nonzero_rows": search["best_local_direction_nonzero_rows"],
                    "best_local_direction_forced_pair_count": search["best_local_direction_forced_pair_count"],
                    "best_local_direction_vector": search["best_local_direction_vector"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_DIRECTION_NINE_ROW_REPAIR_READY")


if __name__ == "__main__":
    main()
