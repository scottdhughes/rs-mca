#!/usr/bin/env python3
"""Try to realize the proxy-slot functional target by template vectors."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "ce5589c"
PROXY_SLOT_DATA = Path("experimental/data/m1_a327_proxy_slot_kernel_generator.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_proxy_slot_template_realization.json")

ROOT = Path(__file__).resolve().parents[2]
PROXY_SLOT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_proxy_slot_kernel_generator.py"
REALIZATION_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_kernel_template_realization.py"

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


pslot = load_module("proxy_slot_kernel_generator", PROXY_SLOT_SCRIPT)
realization = load_module("prescribed_kernel_template_realization", REALIZATION_SCRIPT)
joint = pslot.joint
functional = pslot.functional


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def reconstruct_proxy_slot_target(
    source: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, list[int]], dict[str, Any]]:
    best = source["best_candidate"]
    profile = best["best_profile"]
    _profiles, raw_candidates = joint.build_candidates(max_specs=36)
    candidate = next(
        item for item in raw_candidates if item["coordinate_classes_hash"] == best["coordinate_classes_hash"]
    )
    classes = functional.functional_classes(candidate)
    _stable_total, stable_profiles = pslot.stable_profiles_for_candidate(classes, limit=128)
    source_profile = next(
        item for item in stable_profiles
        if item["basis_id"] == profile["source_basis_id"]
        and item["basis_class_indices"] == profile["basis_class_indices"]
    )
    engineered = pslot.slot_engineered_profile(source_profile, profile["proxy_kernel_slot"])

    prescribed_by_class: dict[str, list[int]] = {}
    for class_index, row in zip(engineered["basis_class_indices"], engineered["basis_functionals"], strict=True):
        prescribed_by_class[str(int(class_index))] = [int(value) % P for value in row]
    for item in engineered["nonbasis_constraint_detail"]:
        acc = [0] * TEMPLATE_DIM
        for scalar, basis_row in zip(item["basis_coordinates"], engineered["basis_functionals"], strict=True):
            for col in range(TEMPLATE_DIM):
                acc[col] = (acc[col] + int(scalar) * int(basis_row[col])) % P
        prescribed_by_class[str(int(item["class_index"]))] = acc
    class_ids = {str(int(row["class_index"])) for row in classes}
    if set(prescribed_by_class) != class_ids:
        missing = sorted(class_ids - set(prescribed_by_class))
        extra = sorted(set(prescribed_by_class) - class_ids)
        raise RuntimeError(f"prescribed class map mismatch missing={missing} extra={extra}")
    return candidate, classes, prescribed_by_class, engineered


def build_record(max_samples: int) -> dict[str, Any]:
    source = load_json(PROXY_SLOT_DATA)
    candidate, classes, prescribed_by_class, engineered = reconstruct_proxy_slot_target(source)
    coord_rows = realization.coordinate_prescribed_rows(candidate, classes, prescribed_by_class)
    matrix = realization.build_realization_matrix(coord_rows)
    matrix_rank = realization.rank(matrix, VARIABLES)
    kernel_basis = realization.nullspace(matrix, VARIABLES)
    diagonal = realization.diagonal_basis()
    diagonal_rank = realization.rank(diagonal, VARIABLES)
    diagonal_in_kernel = all(
        all(sum(row[col] * basis_vec[col] for col in range(VARIABLES)) % P == 0 for row in matrix)
        for basis_vec in diagonal
    )
    non_diagonal = realization.independent_extensions(diagonal, kernel_basis, VARIABLES) if diagonal_in_kernel else []
    non_diagonal_dimension = len(non_diagonal) if diagonal_in_kernel else None
    samples = realization.sample_solutions(kernel_basis, candidate, coord_rows, max_samples=max_samples)
    rowspace_success = [
        row for row in samples
        if row["rowspace_ok"] and row["seven_template_vectors_distinct"]
    ]
    if rowspace_success:
        best = rowspace_success[0]
        proof_status = "CANDIDATE / TEMPLATE_REALIZATION_PROXY_SLOT_TARGET / PARTIAL / EXPERIMENTAL"
        failure = "TEMPLATE_REALIZATION_PROXY_SLOT_TARGET"
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
        rank_key = str(row["prescribed_rank"])
        rank_histogram[rank_key] = rank_histogram.get(rank_key, 0) + 1

    source_profile = source["best_candidate"]["best_profile"]
    proxy = source["proxy_audit"]["proxy_result"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": 327,
        "source_commit": SOURCE_COMMIT,
        "proxy_slot_target": {
            "commit": SOURCE_COMMIT,
            "template_id": source["best_candidate"]["template_id"],
            "assignment_strategy": source["best_candidate"]["assignment_strategy"],
            "coordinate_classes_hash": source["best_candidate"]["coordinate_classes_hash"],
            "support_vector": source["best_candidate"]["support_vector"],
            "pair7_counts": source["best_candidate"]["pair7_counts"],
            "max_pair_count": source["best_candidate"]["max_pair_count"],
            "source_basis_id": source_profile["source_basis_id"],
            "engineered_basis_id": source_profile["basis_id"],
            "proxy_kernel_slot": source_profile["proxy_kernel_slot"],
            "basis_zero_union_size": source_profile["basis_zero_union_size"],
            "guaranteed_proxy_nullity_lower_bound": source_profile["guaranteed_proxy_nullity_lower_bound"],
            "proxy_rank": proxy["proxy_rank"],
            "proxy_nullity": proxy["proxy_nullity"],
            "realization_status": source["realization_status"],
        },
        "realization_target": {
            "functional_classes": len(classes),
            "basis_class_indices": engineered["basis_class_indices"],
            "basis_support_sizes": engineered["basis_support_sizes"],
            "q_variable_count": engineered["q_variable_count"],
            "coefficient_matrix_shape": source_profile["coefficient_matrix_shape"],
            "coefficient_rank": source_profile["coefficient_rank"],
            "right_kernel_nullity": source_profile["right_kernel_nullity"],
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
            "seven_distinct_samples": sum(
                1 for row in samples if row["rowspace_ok"] and row["seven_template_vectors_distinct"]
            ),
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
            "MCA/protocol consequence from this list-track proxy",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-samples", type=int, default=256)
    args = parser.parse_args()
    record = build_record(max_samples=args.max_samples)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        realization_record = record["template_realization"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "linear_matrix_shape": realization_record["linear_matrix_shape"],
                    "linear_rank": realization_record["linear_rank"],
                    "linear_nullity": realization_record["linear_nullity"],
                    "samples_tested": realization_record["samples_tested"],
                    "rowspace_valid_samples": realization_record["rowspace_valid_samples"],
                    "seven_distinct_samples": realization_record["seven_distinct_samples"],
                    "best_realized_functional_span_rank": realization_record["best_realized_functional_span_rank"],
                    "best_failure_mode": realization_record["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PROXY_SLOT_TEMPLATE_REALIZATION_READY")


if __name__ == "__main__":
    main()
