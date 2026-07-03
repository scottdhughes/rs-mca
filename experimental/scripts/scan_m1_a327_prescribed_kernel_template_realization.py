#!/usr/bin/env python3
"""Try to realize prescribed right-kernel functional rows by template vectors."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "42e00f2"
PRESCRIBED_DATA = Path("experimental/data/m1_a327_prescribed_right_kernel_selected_class_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_prescribed_kernel_template_realization.json")

ROOT = Path(__file__).resolve().parents[2]
PRESCRIBED_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_right_kernel_selected_class_search.py"

P = 17
TEMPLATE_DIM = 6
LIST_SIZE = 7
VARIABLES = LIST_SIZE * TEMPLATE_DIM


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prescribed = load_module("prescribed_right_kernel_selected_class_search", PRESCRIBED_SCRIPT)
right_kernel = prescribed.right_kernel
functional = prescribed.functional
lowrank = right_kernel.lowrank


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rref(rows: list[list[int]], ncols: int, prime: int = P) -> tuple[list[list[int]], list[int]]:
    matrix = [[int(value) % prime for value in row] for row in rows if any(int(value) % prime for value in row)]
    pivots: list[int] = []
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % prime:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % prime:
                continue
            factor = matrix[row_idx][col] % prime
            matrix[row_idx] = [
                (matrix[row_idx][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(matrix):
            break
    return matrix[:rank], pivots


def rank(rows: list[list[int]], ncols: int) -> int:
    return len(rref(rows, ncols=ncols)[0])


def nullspace(rows: list[list[int]], ncols: int) -> list[list[int]]:
    basis, pivots = rref(rows, ncols=ncols)
    pivot_set = set(pivots)
    free_cols = [col for col in range(ncols) if col not in pivot_set]
    out = []
    for free_col in free_cols:
        vector = [0] * ncols
        vector[free_col] = 1
        for basis_row, pivot in reversed(list(zip(basis, pivots, strict=True))):
            acc = 0
            for col in free_cols:
                acc = (acc + basis_row[col] * vector[col]) % P
            vector[pivot] = (-acc) % P
        out.append(vector)
    return out


def subspace_equal(left: list[list[int]], right: list[list[int]], ncols: int = TEMPLATE_DIM) -> bool:
    return rank(left, ncols) == rank(right, ncols) == rank(left + right, ncols)


def vector_to_template(vector: list[int]) -> list[list[int]]:
    return [
        [int(vector[witness * TEMPLATE_DIM + col]) % P for col in range(TEMPLATE_DIM)]
        for witness in range(LIST_SIZE)
    ]


def template_distinct(vectors: list[list[int]]) -> bool:
    return len({tuple(row) for row in vectors}) == LIST_SIZE


def diagonal_basis() -> list[list[int]]:
    basis = []
    for col in range(TEMPLATE_DIM):
        vector = [0] * VARIABLES
        for witness in range(LIST_SIZE):
            vector[witness * TEMPLATE_DIM + col] = 1
        basis.append(vector)
    return basis


def independent_extensions(base: list[list[int]], candidates: list[list[int]], ncols: int) -> list[list[int]]:
    current = [row[:] for row in base]
    current_rank = rank(current, ncols)
    out = []
    for candidate in candidates:
        trial_rank = rank(current + [candidate], ncols)
        if trial_rank > current_rank:
            out.append(candidate)
            current.append(candidate)
            current_rank = trial_rank
    return out


def class_key(row: list[int]) -> tuple[int, ...]:
    return tuple(functional.normalize_projective(row))


def reconstruct_best_target(record: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, list[int]], dict[str, Any]]:
    raw_candidates = right_kernel.build_candidates(max_templates=18)
    best = record["best_candidate"]
    candidate = next(
        item for item in raw_candidates
        if item["coordinate_classes_hash"] == best["coordinate_classes_hash"]
    )
    classes = functional.functional_classes(candidate)
    class_by_key = {tuple(row["functional"]): row for row in classes}
    profiles = right_kernel.candidate_basis_profiles(classes, max_random_profiles=8)
    proxy = best["best_proxy"]
    source = next(
        profile for profile in profiles
        if profile["basis_id"] == proxy["source_basis_id"]
        and profile["basis_class_indices"] == proxy["basis_class_indices"]
    )
    kernel = next(
        item for item in prescribed.kernel_specs(max_random=4)
        if item["kernel_id"] == proxy["prescribed_kernel_id"]
    )
    engineered = prescribed.engineer_profile(source, kernel)
    basis_functionals = {
        int(class_index): [int(value) % P for value in row]
        for class_index, row in zip(engineered["basis_class_indices"], engineered["basis_functionals"], strict=True)
    }
    prescribed_by_class: dict[str, list[int]] = {}
    for class_index, row in basis_functionals.items():
        prescribed_by_class[str(class_index)] = row
    for item in engineered["nonbasis_constraint_detail"]:
        acc = [0] * TEMPLATE_DIM
        for scalar, basis_row in zip(item["basis_coordinates"], engineered["basis_functionals"], strict=True):
            for col in range(TEMPLATE_DIM):
                acc[col] = (acc[col] + int(scalar) * int(basis_row[col])) % P
        prescribed_by_class[str(int(item["class_index"]))] = acc
    if set(prescribed_by_class) != {str(int(row["class_index"])) for row in classes}:
        raise RuntimeError("prescribed class map incomplete")
    return candidate, classes, prescribed_by_class, engineered


def coordinate_prescribed_rows(candidate: dict[str, Any], classes: list[dict[str, Any]], prescribed_by_class: dict[str, list[int]]) -> list[dict[str, Any]]:
    key_to_class = {tuple(row["functional"]): int(row["class_index"]) for row in classes}
    rows = []
    for coord in sorted(candidate["coordinate_classes"], key=lambda item: int(item["position"])):
        original_rows = functional.row_basis_mod_p(candidate["template_vectors"], [int(value) for value in coord["members"]])
        class_indices = []
        prescribed_rows = []
        for original in original_rows:
            idx = key_to_class[class_key(original)]
            class_indices.append(idx)
            prescribed_rows.append(prescribed_by_class[str(idx)])
        rows.append(
            {
                "position": int(coord["position"]),
                "members": [int(value) for value in coord["members"]],
                "original_class_indices": class_indices,
                "prescribed_rows": prescribed_rows,
                "prescribed_rank": rank(prescribed_rows, TEMPLATE_DIM),
            }
        )
    return rows


def build_realization_matrix(coord_rows: list[dict[str, Any]]) -> list[list[int]]:
    matrix = []
    for coord in coord_rows:
        members = coord["members"]
        anchor = members[0] - 1
        normals = nullspace(coord["prescribed_rows"], TEMPLATE_DIM)
        for witness_one_based in members[1:]:
            witness = witness_one_based - 1
            for normal in normals:
                row = [0] * VARIABLES
                for col, value in enumerate(normal):
                    row[witness * TEMPLATE_DIM + col] = (row[witness * TEMPLATE_DIM + col] + value) % P
                    row[anchor * TEMPLATE_DIM + col] = (row[anchor * TEMPLATE_DIM + col] - value) % P
                matrix.append(row)
    return matrix


def verify_template(candidate: dict[str, Any], coord_rows: list[dict[str, Any]], vectors: list[list[int]]) -> dict[str, Any]:
    failures = []
    realized_total_cost = 0
    realized_rank_histogram: dict[str, int] = {}
    for coord in coord_rows:
        realized_rows = functional.row_basis_mod_p(vectors, coord["members"])
        realized_total_cost += rank(realized_rows, TEMPLATE_DIM)
        realized_rank_histogram[str(rank(realized_rows, TEMPLATE_DIM))] = realized_rank_histogram.get(str(rank(realized_rows, TEMPLATE_DIM)), 0) + 1
        if not subspace_equal(realized_rows, coord["prescribed_rows"]):
            failures.append(coord["position"])
    realized_candidate = {
        **candidate,
        "template_vectors": vectors,
        "total_effective_cost": realized_total_cost,
        "variable_count": len(vectors[0]) * 256,
    }
    try:
        classes = functional.functional_classes(realized_candidate)
        class_count = len(classes)
        forced = sum(1 for row in classes if row["forced_identity"])
        span_rank = functional.rank_mod_p([row["functional"] for row in classes])
        annihilator = functional.nullspace_basis([row["functional"] for row in classes])
    except Exception as exc:
        class_count = None
        forced = None
        span_rank = None
        annihilator = []
        failures.append(f"class_rebuild_error:{exc}")
    return {
        "rowspace_failures": failures,
        "rowspace_ok": not failures,
        "seven_template_vectors_distinct": template_distinct(vectors),
        "realized_total_effective_cost": realized_total_cost,
        "realized_rank_histogram": realized_rank_histogram,
        "realized_functional_classes": class_count,
        "realized_forced_functional_identities": forced,
        "realized_functional_span_rank": span_rank,
        "realized_annihilator_dimension": len(annihilator),
        "template_vectors": vectors,
        "template_vectors_hash": hash_payload(vectors),
    }


def sample_solutions(kernel_basis: list[list[int]], candidate: dict[str, Any], coord_rows: list[dict[str, Any]], max_samples: int) -> list[dict[str, Any]]:
    samples = []
    raw_vectors = []
    non_diagonal = independent_extensions(diagonal_basis(), kernel_basis, VARIABLES)
    raw_vectors.extend(non_diagonal[:1])
    raw_vectors.extend(kernel_basis[: min(len(kernel_basis), max_samples)])
    rng = random.Random(42000)
    for _ in range(max_samples):
        if not kernel_basis:
            break
        coeffs = [rng.randrange(P) for _ in kernel_basis]
        if not any(coeffs):
            coeffs[rng.randrange(len(coeffs))] = 1
        vector = [0] * VARIABLES
        for scalar, basis_vec in zip(coeffs, kernel_basis, strict=True):
            for idx, value in enumerate(basis_vec):
                vector[idx] = (vector[idx] + scalar * value) % P
        raw_vectors.append(vector)
    seen: set[str] = set()
    for vector in raw_vectors:
        vectors = vector_to_template(vector)
        key = hash_payload(vectors)
        if key in seen:
            continue
        seen.add(key)
        samples.append(verify_template(candidate, coord_rows, vectors))
        if samples[-1]["rowspace_ok"] and samples[-1]["seven_template_vectors_distinct"]:
            break
    return samples


def build_record(max_samples: int) -> dict[str, Any]:
    source = load_json(PRESCRIBED_DATA)
    candidate, classes, prescribed_by_class, engineered = reconstruct_best_target(source)
    coord_rows = coordinate_prescribed_rows(candidate, classes, prescribed_by_class)
    matrix = build_realization_matrix(coord_rows)
    matrix_rank = rank(matrix, VARIABLES)
    kernel_basis = nullspace(matrix, VARIABLES)
    diagonal = diagonal_basis()
    diagonal_rank = rank(diagonal, VARIABLES)
    diagonal_in_kernel = all(
        all(sum(row[col] * basis_vec[col] for col in range(VARIABLES)) % P == 0 for row in matrix)
        for basis_vec in diagonal
    )
    non_diagonal = independent_extensions(diagonal, kernel_basis, VARIABLES) if diagonal_in_kernel else []
    non_diagonal_dimension = len(non_diagonal) if diagonal_in_kernel else None
    samples = sample_solutions(kernel_basis, candidate, coord_rows, max_samples=max_samples)
    successful = [
        row for row in samples
        if row["rowspace_ok"] and row["seven_template_vectors_distinct"]
    ]
    if successful:
        best = successful[0]
        proof_status = "CANDIDATE / TEMPLATE_REALIZATION_PROXY_TARGET / PARTIAL / EXPERIMENTAL"
        failure = "TEMPLATE_REALIZATION_PROXY_TARGET"
    elif samples and any(row["rowspace_ok"] for row in samples):
        best = next(row for row in samples if row["rowspace_ok"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / TEMPLATE_REALIZATION_DEGENERATE / PARTIAL / EXPERIMENTAL"
        failure = "TEMPLATE_REALIZATION_DEGENERATE"
    elif kernel_basis:
        best = samples[0] if samples else None
        proof_status = "EXACT_EXTRACTION_NO_A327 / TEMPLATE_REALIZATION_ROWSPACE_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "TEMPLATE_REALIZATION_ROWSPACE_FAIL"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / TEMPLATE_REALIZATION_LINEAR_INCONSISTENT / PARTIAL / EXPERIMENTAL"
        failure = "TEMPLATE_REALIZATION_LINEAR_INCONSISTENT"
    rank_histogram: dict[str, int] = {}
    for row in coord_rows:
        rank_histogram[str(row["prescribed_rank"])] = rank_histogram.get(str(row["prescribed_rank"]), 0) + 1
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": 327,
        "source_commit": SOURCE_COMMIT,
        "prescribed_kernel_proxy": {
            "commit": SOURCE_COMMIT,
            "best_template_id": source["prescribed_kernel_search"]["best_template_id"],
            "best_assignment_strategy": source["prescribed_kernel_search"]["best_assignment_strategy"],
            "proxy_rank": source["prescribed_kernel_search"]["best_proxy_rank"],
            "proxy_nullity": source["prescribed_kernel_search"]["best_proxy_nullity"],
            "realization_status": source["realization_status"],
        },
        "realization_target": {
            "template_id": candidate["template_id"],
            "assignment_strategy": candidate["assignment_strategy"],
            "coordinate_classes_hash": candidate["coordinate_classes_hash"],
            "source_basis_id": engineered["source_basis_id"],
            "prescribed_kernel_id": engineered["prescribed_kernel_id"],
            "prescribed_kernel_vector": engineered["prescribed_kernel_vector"],
            "coefficient_rank": engineered["coefficient_rank"],
            "right_kernel_nullity": engineered["right_kernel_nullity"],
            "coordinate_rows_changed": engineered["coordinate_rows_changed"],
            "prescribed_coordinate_rank_histogram": rank_histogram,
        },
        "template_realization": {
            "linear_matrix_shape": [len(matrix), VARIABLES],
            "linear_rank": matrix_rank,
            "linear_nullity": VARIABLES - matrix_rank,
            "kernel_basis_vectors": len(kernel_basis),
            "diagonal_rank": diagonal_rank,
            "diagonal_in_kernel": diagonal_in_kernel,
            "non_diagonal_kernel_dimension": non_diagonal_dimension,
            "non_diagonal_quotient_exhausted": bool(non_diagonal_dimension is not None and non_diagonal_dimension <= 1),
            "samples_tested": len(samples),
            "rowspace_valid_samples": sum(1 for row in samples if row["rowspace_ok"]),
            "seven_distinct_samples": sum(1 for row in samples if row["rowspace_ok"] and row["seven_template_vectors_distinct"]),
            "best_realized_total_effective_cost": None if best is None else best["realized_total_effective_cost"],
            "best_realized_functional_classes": None if best is None else best["realized_functional_classes"],
            "best_realized_functional_span_rank": None if best is None else best["realized_functional_span_rank"],
            "best_failure_mode": failure,
        },
        "best_sample": best,
        "sample_summaries": [
            {
                key: row[key]
                for key in [
                    "rowspace_ok",
                    "seven_template_vectors_distinct",
                    "realized_total_effective_cost",
                    "realized_functional_classes",
                    "realized_forced_functional_identities",
                    "realized_functional_span_rank",
                    "realized_annihilator_dimension",
                    "template_vectors_hash",
                ]
            }
            for row in samples
        ],
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
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-samples", type=int, default=128)
    args = parser.parse_args()
    record = build_record(max_samples=args.max_samples)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        realization = record["template_realization"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "linear_matrix_shape": realization["linear_matrix_shape"],
                    "linear_rank": realization["linear_rank"],
                    "linear_nullity": realization["linear_nullity"],
                    "samples_tested": realization["samples_tested"],
                    "rowspace_valid_samples": realization["rowspace_valid_samples"],
                    "seven_distinct_samples": realization["seven_distinct_samples"],
                    "best_realized_functional_span_rank": realization["best_realized_functional_span_rank"],
                    "best_failure_mode": realization["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PRESCRIBED_KERNEL_TEMPLATE_REALIZATION_READY")


if __name__ == "__main__":
    main()
