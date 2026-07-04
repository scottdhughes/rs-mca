#!/usr/bin/env python3
"""Search pair-clear direction support chambers for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable


SOURCE_COMMIT = "a9acb86"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_nine_row_module_syzygy.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_direction_support_chamber_search.json")

ROOT = Path(__file__).resolve().parents[2]
MODULE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_nine_row_module_syzygy.py"

P = 17
TEMPLATE_DIM = 6
TARGET_AGREEMENT = 327
PINNED_DIRECTION = [0, 5, 0, 0, 0, 1]
PINNED_INACTIVE_CLASSES = [13, 16, 17, 18, 19]
PINNED_ACTIVE_CLASSES = [0, 2, 3, 5, 6, 11, 12, 14, 15]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


module_syzygy = load_module("pairclear_nine_row_module_syzygy", MODULE_SCRIPT)
zstable = module_syzygy.zstable


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def dot(row: list[int] | tuple[int, ...], vector: list[int] | tuple[int, ...]) -> int:
    return sum(int(row[idx]) * int(vector[idx]) for idx in range(TEMPLATE_DIM)) % P


def normalize_projective(vector: list[int]) -> list[int]:
    values = [int(value) % P for value in vector]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return [(entry * inv) % P for entry in values]
    return values


def rank_rows(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> int:
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
        if rank == ncols:
            break
    return rank


def rref(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> tuple[list[list[int]], list[int]]:
    matrix = [[int(value) % P for value in row] for row in rows if any(int(value) % P for value in row)]
    pivots: list[int] = []
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
        pivots.append(col)
        rank += 1
        if rank == len(matrix) or rank == ncols:
            break
    return matrix[:rank], pivots


def nullspace_basis(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> list[list[int]]:
    basis, pivots = rref(rows, ncols=ncols)
    pivot_set = set(pivots)
    free_cols = [col for col in range(ncols) if col not in pivot_set]
    result = []
    for free_col in free_cols:
        vector = [0] * ncols
        vector[free_col] = 1
        for basis_row, pivot in reversed(list(zip(basis, pivots, strict=True))):
            vector[pivot] = (-sum(basis_row[col] * vector[col] for col in free_cols)) % P
        result.append(vector)
    return result


def projective_directions(dim: int = TEMPLATE_DIM) -> Iterable[list[int]]:
    """Yield one normalized representative of each projective GF(17) direction."""
    for first in range(dim):
        suffix_len = dim - first - 1
        for encoded in range(P**suffix_len):
            vector = [0] * dim
            vector[first] = 1
            value = encoded
            for idx in range(first + 1, dim):
                vector[idx] = value % P
                value //= P
            yield vector


def all_projective_count(dim: int = TEMPLATE_DIM) -> int:
    return (P**dim - 1) // (P - 1)


def linear_image_rows(linear_forms: list[list[int]], vector: list[int]) -> list[int]:
    return [dot(row, vector) for row in linear_forms]


def pair_projection_matrix(candidate: dict[str, Any], profile: dict[str, Any]) -> tuple[list[str], list[list[int]]]:
    labels = sorted(zstable.zexp.pair_projection_scalars(candidate, profile, [1, 0, 0, 0, 0, 0]).keys())
    rows: list[list[int]] = []
    for label in labels:
        coeffs = []
        for col in range(TEMPLATE_DIM):
            basis = [0] * TEMPLATE_DIM
            basis[col] = 1
            coeffs.append(int(zstable.zexp.pair_projection_scalars(candidate, profile, basis)[label]) % P)
        rows.append(coeffs)
    return labels, rows


def chamber_record(
    zero_indices: tuple[int, ...],
    matrix: list[list[int]],
    row_classes: list[int],
    exemplar: list[int],
) -> dict[str, Any]:
    rows = [matrix[idx] for idx in zero_indices]
    rank = rank_rows(rows)
    return {
        "zero_row_count": len(zero_indices),
        "active_row_count": len(matrix) - len(zero_indices),
        "inactive_rank": rank,
        "inactive_kernel_nullity": TEMPLATE_DIM - rank,
        "zero_row_indices": list(zero_indices),
        "zero_row_classes": [row_classes[idx] for idx in zero_indices],
        "active_row_indices": [idx for idx in range(len(matrix)) if idx not in set(zero_indices)],
        "active_row_classes": [row_classes[idx] for idx in range(len(matrix)) if idx not in set(zero_indices)],
        "exemplar_direction": exemplar,
        "exemplar_direction_projective": normalize_projective(exemplar),
        "exemplar_weight": sum(1 for value in exemplar if value % P),
    }


def chamber_sort_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -record["zero_row_count"],
        record["inactive_rank"],
        -record["inactive_kernel_nullity"],
        record["active_row_count"],
        record["exemplar_weight"],
        record["exemplar_direction_projective"],
    )


def rank_slack_sort_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -record["zero_row_count"],
        record["inactive_rank"],
        record["active_row_count"],
        record["exemplar_weight"],
        record["exemplar_direction_projective"],
    )


def pair_clear_vector_in_subspace(pair_rows: list[list[int]], basis: list[list[int]]) -> list[int] | None:
    if not basis:
        return None
    dim = len(basis)
    for coeffs in projective_directions(dim):
        vector = [0] * TEMPLATE_DIM
        for coeff, basis_vector in zip(coeffs, basis, strict=True):
            if not coeff:
                continue
            vector = [(vector[idx] + coeff * basis_vector[idx]) % P for idx in range(TEMPLATE_DIM)]
        if all(value % P for value in linear_image_rows(pair_rows, vector)):
            return normalize_projective(vector)
    return None


def extension_record(
    chamber: dict[str, Any],
    active_idx: int,
    matrix: list[list[int]],
    row_classes: list[int],
    pair_rows: list[list[int]],
) -> dict[str, Any] | None:
    extended_zero_indices = tuple(sorted(chamber["zero_row_indices"] + [active_idx]))
    rows = [matrix[idx] for idx in extended_zero_indices]
    rank = rank_rows(rows)
    nullity = TEMPLATE_DIM - rank
    if nullity <= 0:
        return None
    basis = nullspace_basis(rows)
    direction = pair_clear_vector_in_subspace(pair_rows, basis)
    if direction is None:
        return None
    return {
        "added_active_row_index": active_idx,
        "added_active_row_class": row_classes[active_idx],
        "zero_row_count": len(extended_zero_indices),
        "active_row_count": len(matrix) - len(extended_zero_indices),
        "inactive_rank": rank,
        "inactive_kernel_nullity": nullity,
        "zero_row_indices": list(extended_zero_indices),
        "zero_row_classes": [row_classes[idx] for idx in extended_zero_indices],
        "active_row_indices": [idx for idx in range(len(matrix)) if idx not in set(extended_zero_indices)],
        "active_row_classes": [row_classes[idx] for idx in range(len(matrix)) if idx not in set(extended_zero_indices)],
        "pair_clear_direction": direction,
        "pair_clear_direction_weight": sum(1 for value in direction if value % P),
    }


def extension_sort_key(record: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -record["zero_row_count"],
        record["inactive_rank"],
        record["active_row_count"],
        record["pair_clear_direction_weight"],
        record["pair_clear_direction"],
    )


def build_record(direction_limit: int | None, extension_chamber_limit: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    candidate, profile = module_syzygy.reconstruct_candidate()
    matrix = [[int(value) % P for value in row] for row in zstable.coefficient_matrix(profile)]
    row_classes = [int(row["class_index"]) for row in profile["nonbasis_constraint_detail"]]
    pair_labels, pair_rows = pair_projection_matrix(candidate, profile)

    pinned_pair_values = dict(zip(pair_labels, linear_image_rows(pair_rows, PINNED_DIRECTION), strict=True))
    pinned_zero_indices = tuple(idx for idx, row in enumerate(matrix) if dot(row, PINNED_DIRECTION) == 0)
    pinned_record = chamber_record(pinned_zero_indices, matrix, row_classes, PINNED_DIRECTION)
    pinned_record["pair_projection_scalars"] = pinned_pair_values
    pinned_record["forced_pairs"] = [label for label, value in pinned_pair_values.items() if not value % P]

    chamber_exemplars: dict[tuple[int, ...], list[int]] = {}
    directions_tested = 0
    pair_clear_directions = 0
    support_reduced_directions = 0
    rank_slack_directions = 0

    for vector in projective_directions(TEMPLATE_DIM):
        if direction_limit is not None and directions_tested >= direction_limit:
            break
        directions_tested += 1
        pair_values = linear_image_rows(pair_rows, vector)
        if any(value % P == 0 for value in pair_values):
            continue
        pair_clear_directions += 1
        row_values = linear_image_rows(matrix, vector)
        zero_indices = tuple(idx for idx, value in enumerate(row_values) if value % P == 0)
        if len(zero_indices) >= 6:
            support_reduced_directions += 1
        if len(zero_indices) >= 5 and rank_rows([matrix[idx] for idx in zero_indices]) <= 4:
            rank_slack_directions += 1
        old = chamber_exemplars.get(zero_indices)
        if old is None or (sum(1 for value in vector if value % P), vector) < (sum(1 for value in old if value % P), old):
            chamber_exemplars[zero_indices] = vector

    chambers = [
        chamber_record(zero_indices, matrix, row_classes, exemplar)
        for zero_indices, exemplar in chamber_exemplars.items()
    ]
    pair_clear_support_reduced = [row for row in chambers if row["zero_row_count"] >= 6]
    rank_slack_chambers = [row for row in chambers if row["zero_row_count"] >= 5 and row["inactive_rank"] <= 4]
    pair_clear_nine_row_chambers = [row for row in chambers if row["zero_row_count"] >= 5]

    extension_inputs = sorted(
        [row for row in chambers if row["inactive_rank"] <= 4],
        key=lambda row: (-row["zero_row_count"], row["inactive_rank"], row["active_row_count"]),
    )[:extension_chamber_limit]
    extension_tests = 0
    extensions: list[dict[str, Any]] = []
    for chamber in extension_inputs:
        zero_set = set(chamber["zero_row_indices"])
        for active_idx in range(len(matrix)):
            if active_idx in zero_set:
                continue
            extension_tests += 1
            record = extension_record(chamber, active_idx, matrix, row_classes, pair_rows)
            if record is not None:
                extensions.append(record)
    support_reduced_extensions = [row for row in extensions if row["zero_row_count"] >= 6]

    best_chamber = min(chambers, key=chamber_sort_key) if chambers else None
    best_nine_row_chamber = min(pair_clear_nine_row_chambers, key=chamber_sort_key) if pair_clear_nine_row_chambers else None
    best_rank_slack = min(rank_slack_chambers, key=rank_slack_sort_key) if rank_slack_chambers else None
    best_support_reduced = min(pair_clear_support_reduced, key=chamber_sort_key) if pair_clear_support_reduced else None
    best_extension = min(extensions, key=extension_sort_key) if extensions else None
    best_support_reduced_extension = min(support_reduced_extensions, key=extension_sort_key) if support_reduced_extensions else None

    proof_status = "EXACT_EXTRACTION_NO_A327 / CHAMBER_NO_RANK_SLACK_FRONT / PARTIAL / EXPERIMENTAL"
    failure = "CHAMBER_NO_RANK_SLACK_FRONT"
    if best_support_reduced is not None:
        proof_status = "CANDIDATE / CHAMBER_DIRECT_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL"
        failure = "CHAMBER_DIRECT_SUPPORT_REDUCED"
    elif best_support_reduced_extension is not None:
        proof_status = "CANDIDATE / CHAMBER_EXTENSION_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL"
        failure = "CHAMBER_EXTENSION_SUPPORT_REDUCED"
    elif best_rank_slack is not None:
        proof_status = "CANDIDATE / CHAMBER_RANK_SLACK_FOUND / PARTIAL / EXPERIMENTAL"
        failure = "CHAMBER_RANK_SLACK_FOUND"
    elif best_nine_row_chamber is not None:
        proof_status = "CANDIDATE / CHAMBER_NINE_ROW_STABLE / PARTIAL / EXPERIMENTAL"
        failure = "CHAMBER_NINE_ROW_STABLE"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_module_syzygy": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "inactive_rank": previous["module_syzygy"]["inactive_matrix"]["rank"],
            "inactive_right_kernel_nullity": previous["module_syzygy"]["inactive_matrix"]["right_kernel_nullity"],
            "singleton_extensions_tested": previous["module_syzygy"]["singleton_extensions_tested"],
            "singleton_full_rank_count": previous["module_syzygy"]["singleton_full_rank_count"],
            "best_failure_mode": previous["module_syzygy"]["best_failure_mode"],
        },
        "target_system": {
            "template_id": candidate["template_id"],
            "assignment_strategy": candidate["assignment_strategy"],
            "basis_id": profile["basis_id"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "coefficient_matrix_shape": [len(matrix), TEMPLATE_DIM],
            "row_classes": row_classes,
            "pair_projection_labels": pair_labels,
            "pinned_direction": PINNED_DIRECTION,
            "pinned_inactive_row_classes": PINNED_INACTIVE_CLASSES,
            "pinned_active_row_classes": PINNED_ACTIVE_CLASSES,
            "pinned_chamber": pinned_record,
        },
        "chamber_search": {
            "field": "GF(17)",
            "full_projective_directions": all_projective_count(TEMPLATE_DIM),
            "direction_limit": direction_limit,
            "directions_tested": directions_tested,
            "pair_clear_directions": pair_clear_directions,
            "distinct_pair_clear_chambers": len(chambers),
            "pair_clear_nine_row_or_better_chambers": len(pair_clear_nine_row_chambers),
            "direct_support_reduced_directions": support_reduced_directions,
            "direct_support_reduced_chambers": len(pair_clear_support_reduced),
            "rank_slack_directions": rank_slack_directions,
            "rank_slack_chambers": len(rank_slack_chambers),
            "extension_chambers_tested": len(extension_inputs),
            "extension_tests": extension_tests,
            "extension_pairclear_successes": len(extensions),
            "support_reduced_extensions": len(support_reduced_extensions),
            "best_chamber": best_chamber,
            "best_nine_row_chamber": best_nine_row_chamber,
            "best_rank_slack_chamber": best_rank_slack,
            "best_direct_support_reduced_chamber": best_support_reduced,
            "best_extension": best_extension,
            "best_support_reduced_extension": best_support_reduced_extension,
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
            "global obstruction outside the base direction-support chamber front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--direction-limit", type=int, default=None)
    parser.add_argument("--extension-chamber-limit", type=int, default=200)
    args = parser.parse_args()
    record = build_record(
        direction_limit=args.direction_limit,
        extension_chamber_limit=args.extension_chamber_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["chamber_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "directions_tested": search["directions_tested"],
                    "pair_clear_directions": search["pair_clear_directions"],
                    "distinct_pair_clear_chambers": search["distinct_pair_clear_chambers"],
                    "pair_clear_nine_row_or_better_chambers": search["pair_clear_nine_row_or_better_chambers"],
                    "direct_support_reduced_chambers": search["direct_support_reduced_chambers"],
                    "rank_slack_chambers": search["rank_slack_chambers"],
                    "extension_pairclear_successes": search["extension_pairclear_successes"],
                    "support_reduced_extensions": search["support_reduced_extensions"],
                    "best_failure_mode": search["best_failure_mode"],
                    "best_nine_row_zero_count": None
                    if search["best_nine_row_chamber"] is None
                    else search["best_nine_row_chamber"]["zero_row_count"],
                    "best_nine_row_inactive_rank": None
                    if search["best_nine_row_chamber"] is None
                    else search["best_nine_row_chamber"]["inactive_rank"],
                    "best_rank_slack_zero_count": None
                    if search["best_rank_slack_chamber"] is None
                    else search["best_rank_slack_chamber"]["zero_row_count"],
                    "best_rank_slack_inactive_rank": None
                    if search["best_rank_slack_chamber"] is None
                    else search["best_rank_slack_chamber"]["inactive_rank"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_DIRECTION_SUPPORT_CHAMBER_SEARCH_READY")


if __name__ == "__main__":
    main()
