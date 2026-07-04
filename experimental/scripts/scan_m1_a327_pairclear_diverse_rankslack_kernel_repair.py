#!/usr/bin/env python3
"""Search the 2D rank-slack kernel from the diverse five-row chamber."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "3228415"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_diverse_five_row_module_audit.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_diverse_rankslack_kernel_repair.json")

ROOT = Path(__file__).resolve().parents[2]
AUDIT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_diverse_five_row_module_audit.py"

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


audit = load_module("pairclear_diverse_five_row_module_audit", AUDIT_SCRIPT)
zstable = audit.zstable


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize_projective(vector: list[int]) -> list[int]:
    values = [int(value) % P for value in vector]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return [(entry * inv) % P for entry in values]
    return values


def dot(row: list[int] | tuple[int, ...], vector: list[int] | tuple[int, ...]) -> int:
    return sum(int(row[idx]) * int(vector[idx]) for idx in range(TEMPLATE_DIM)) % P


def projective_kernel_combinations(basis: list[list[int]]) -> list[dict[str, Any]]:
    rows = []
    for coeffs in [[1, t] for t in range(P)] + [[0, 1]]:
        vector = [0] * TEMPLATE_DIM
        for coeff, basis_vector in zip(coeffs, basis, strict=True):
            for idx, value in enumerate(basis_vector):
                vector[idx] = (vector[idx] + coeff * int(value)) % P
        rows.append(
            {
                "coefficients": coeffs,
                "direction": vector,
                "direction_projective": normalize_projective(vector),
            }
        )
    return rows


def direction_record(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    matrix: list[list[int]],
    row_classes: list[int],
    coeffs: list[int],
    vector: list[int],
) -> dict[str, Any]:
    row_values = [dot(row, vector) for row in matrix]
    zero_indices = [idx for idx, value in enumerate(row_values) if not value % P]
    active_indices = [idx for idx, value in enumerate(row_values) if value % P]
    scalars = zstable.zexp.pair_projection_scalars(candidate, profile, vector)
    forced = [pair for pair, value in scalars.items() if int(value) % P == 0]
    return {
        "kernel_coefficients": coeffs,
        "direction": vector,
        "direction_projective": normalize_projective(vector),
        "direction_weight": sum(1 for value in vector if value % P),
        "row_values": row_values,
        "zero_row_count": len(zero_indices),
        "zero_row_indices": zero_indices,
        "zero_row_classes": [row_classes[idx] for idx in zero_indices],
        "active_row_count": len(active_indices),
        "active_row_indices": active_indices,
        "active_row_classes": [row_classes[idx] for idx in active_indices],
        "forced_pair_count": len(forced),
        "forced_pairs": forced,
        "pair_projection_scalars": scalars,
    }


def direction_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["forced_pair_count"],
        -row["zero_row_count"],
        row["active_row_count"],
        row["direction_weight"],
        row["direction_projective"],
    )


def build_record() -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    candidate, profile, _profile_index = audit.reconstruct_target()
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    rank_slack = previous["module_audit"]["rank_slack_chamber"]
    kernel_basis = rank_slack["matrix"]["right_kernel_basis"]
    directions = [
        direction_record(candidate, profile, matrix, row_classes, item["coefficients"], item["direction"])
        for item in projective_kernel_combinations(kernel_basis)
    ]
    pair_clear = [row for row in directions if row["forced_pair_count"] == 0]
    support_reduced = [row for row in pair_clear if row["zero_row_count"] >= 8]
    nine_or_better = [row for row in pair_clear if row["zero_row_count"] >= 9]
    kernels = [row for row in pair_clear if row["active_row_count"] == 0]
    best = min(pair_clear, key=direction_sort_key) if pair_clear else min(directions, key=direction_sort_key)

    failure = "RANKSLACK_KERNEL_FORCED_PAIR"
    proof_status = "EXACT_EXTRACTION_NO_A327 / RANKSLACK_KERNEL_FORCED_PAIR / PARTIAL / EXPERIMENTAL"
    if kernels:
        failure = "RANKSLACK_KERNEL_COEFFICIENT_KERNEL"
        proof_status = "CANDIDATE / RANKSLACK_KERNEL_COEFFICIENT_KERNEL / PARTIAL / EXPERIMENTAL"
        best = min(kernels, key=direction_sort_key)
    elif nine_or_better:
        failure = "RANKSLACK_KERNEL_NINE_ROW_REPAIR"
        proof_status = "CANDIDATE / RANKSLACK_KERNEL_NINE_ROW_REPAIR / PARTIAL / EXPERIMENTAL"
        best = min(nine_or_better, key=direction_sort_key)
    elif support_reduced:
        failure = "RANKSLACK_KERNEL_EIGHT_ROW_STABLE"
        proof_status = "CANDIDATE / RANKSLACK_KERNEL_EIGHT_ROW_STABLE / PARTIAL / EXPERIMENTAL"
        best = min(support_reduced, key=direction_sort_key)
    elif pair_clear:
        failure = "RANKSLACK_KERNEL_LOWER_SUPPORT_ONLY"
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANKSLACK_KERNEL_LOWER_SUPPORT_ONLY / PARTIAL / EXPERIMENTAL"

    previous_audit = previous["module_audit"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_five_row_module_audit": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "target_template_id": previous["target_system"]["template_id"],
            "target_mutation_id": previous["target_system"]["mutation_id"],
            "target_basis_id": previous["target_system"]["basis_id"],
            "active_row_count": previous_audit["active_matrix"]["shape"][0],
            "inactive_row_count": previous_audit["inactive_matrix"]["shape"][0],
            "rank_slack_rank": previous_audit["rank_slack_chamber"]["matrix"]["rank"],
            "rank_slack_nullity": previous_audit["rank_slack_chamber"]["matrix"]["right_kernel_nullity"],
            "best_failure_mode": previous_audit["best_failure_mode"],
        },
        "rank_slack_kernel": {
            "field": "GF(17)",
            "basis": kernel_basis,
            "projective_basis": rank_slack["kernel_projective_basis"],
            "base_zero_row_indices": rank_slack["zero_row_indices"],
            "base_zero_row_classes": rank_slack["zero_row_classes"],
            "directions_tested": len(directions),
            "pair_clear_directions": len(pair_clear),
            "support_reduced_directions": len(support_reduced),
            "nine_or_better_directions": len(nine_or_better),
            "coefficient_kernel_directions": len(kernels),
            "best_direction": best,
            "all_direction_summaries": directions,
            "best_failure_mode": failure,
        },
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
            "global obstruction outside the audited rank-slack kernel front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        kernel = record["rank_slack_kernel"]
        best = kernel["best_direction"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "directions_tested": kernel["directions_tested"],
                    "pair_clear_directions": kernel["pair_clear_directions"],
                    "support_reduced_directions": kernel["support_reduced_directions"],
                    "nine_or_better_directions": kernel["nine_or_better_directions"],
                    "coefficient_kernel_directions": kernel["coefficient_kernel_directions"],
                    "best_zero_row_count": best["zero_row_count"],
                    "best_active_row_count": best["active_row_count"],
                    "best_forced_pair_count": best["forced_pair_count"],
                    "best_failure_mode": kernel["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_DIVERSE_RANKSLACK_KERNEL_REPAIR_READY")


if __name__ == "__main__":
    main()
