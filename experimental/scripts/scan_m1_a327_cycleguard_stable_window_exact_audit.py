#!/usr/bin/env python3
"""Prepare the M1 a=327 cycleguard basis-quotient exact audit ledger."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "c142977"
SOURCE_DATA = Path("experimental/data/m1_a327_cycleguard_exact_pairclear_chamber_realization.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_stable_window_exact_audit.json")

ROOT = Path(__file__).resolve().parents[2]
REALIZATION_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycleguard_exact_pairclear_chamber_realization.py"

P = 17
K = 256
TARGET_AGREEMENT = 327
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


realization_mod = load_module("cycleguard_chamber_realization", REALIZATION_SCRIPT)


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def functional_class_detail(classes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "class_index": int(row["class_index"]),
            "functional": [int(value) for value in row["functional"]],
            "support_size": int(row["support_size"]),
            "forced_identity": bool(row["forced_identity"]),
            "quotient_variables": int(row["quotient_variables"]),
            "positions": [int(pos) for pos in row["positions"]],
            "positions_hash": row["positions_hash"],
        }
        for row in classes
    ]


def basis_profile_payload(profile: dict[str, Any]) -> dict[str, Any]:
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": [int(idx) for idx in profile["basis_class_indices"]],
        "basis_functionals": [[int(value) for value in row] for row in profile["basis_functionals"]],
        "basis_support_sizes": [int(value) for value in profile["basis_support_sizes"]],
        "q_variable_count": int(profile["q_variable_count"]),
        "nonbasis_constraints": int(profile["nonbasis_constraints"]),
        "matrix_shape": [int(value) for value in profile["matrix_shape"]],
        "formal_nullity_lower_bound": int(profile["formal_nullity_lower_bound"]),
        "nonbasis_constraint_detail": [
            {
                "class_index": int(row["class_index"]),
                "support_size": int(row["support_size"]),
                "basis_coordinates": [int(value) % P for value in row["basis_coordinates"]],
            }
            for row in profile["nonbasis_constraint_detail"]
        ],
    }


def status_for(record: dict[str, Any]) -> tuple[str, str]:
    chamber = record["source_chamber"]
    profile = record["basis_profiles"][0] if record["basis_profiles"] else None
    if chamber["best_failure_mode"] != "CYCLEG_REALIZATION_BASIS_QUOTIENT_TARGET":
        return (
            "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_BAD_SOURCE_STATUS / PARTIAL / EXPERIMENTAL",
            "CYCLEG_EXACT_BAD_SOURCE_STATUS",
        )
    if profile is None:
        return (
            "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_NO_BASIS_PROFILE / PARTIAL / EXPERIMENTAL",
            "CYCLEG_EXACT_NO_BASIS_PROFILE",
        )
    return (
        "CANDIDATE / CYCLEG_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL",
        "CYCLEG_EXACT_AUDIT_PENDING",
    )


def build_record() -> dict[str, Any]:
    source_record = load_json(SOURCE_DATA)
    source_for_reconstruction = realization_mod.load_json(realization_mod.SOURCE_DATA)
    candidate, profile, _template_profile = realization_mod.reconstruct_target(source_for_reconstruction)
    classes = realization_mod.zstable.functional.functional_classes(candidate)
    functional_classes = functional_class_detail(classes)
    profile_payload = basis_profile_payload(profile)
    chamber = source_record["chamber_realization"]

    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "source_chamber": {
            "commit": SOURCE_COMMIT,
            "template_id": chamber["template_id"],
            "basis_id": chamber["basis_id"],
            "direction": chamber["best_chamber"]["direction"],
            "forced_pairs": chamber["forced_pairs"],
            "inactive_rank": chamber["inactive_rank"],
            "inactive_kernel_nullity": chamber["inactive_kernel_nullity"],
            "zero_class_union_size": chamber["zero_class_union_size"],
            "zero_row_window_dimension": chamber["zero_row_window_dimension"],
            "scalar_required_vanishing_union_size": chamber["scalar_required_vanishing_union_size"],
            "scalar_stable_window_dimension": chamber["scalar_stable_window_dimension"],
            "best_failure_mode": chamber["best_failure_mode"],
        },
        "survivor": {
            "template_id": candidate["template_id"],
            "template_family": candidate["template_family"],
            "template_dimension": int(candidate["template_dimension"]),
            "template_vectors": [[int(value) for value in row] for row in candidate["template_vectors"]],
            "assignment_strategy": candidate["assignment_strategy"],
            "assignment_seed": int(candidate["assignment_seed"]),
            "support_vector": [int(value) for value in candidate["support_vector"]],
            "pair7_counts": [int(value) for value in candidate["pair7_counts"]],
            "max_pair_count": int(candidate["max_pair_count"]),
            "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        },
        "coordinate_classes": candidate["coordinate_classes"],
        "functional_classes_detail": functional_classes,
        "basis_profiles": [profile_payload],
        "basis_quotient_audit": {
            "field": None,
            "field_denominator": None,
            "H_order": None,
            "best_basis_id": profile_payload["basis_id"],
            "best_basis_support_sizes": profile_payload["basis_support_sizes"],
            "best_q_variable_count": profile_payload["q_variable_count"],
            "best_matrix_shape": None,
            "best_rank": None,
            "best_nullity": None,
            "best_failure_mode": None,
        },
        "pair_projection_test": {
            "pairs_tested": 21,
            "forced_equal_pairs": [],
            "min_projection_rank": None,
            "projection_rank_by_pair": None,
        },
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": None,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "MCA/protocol consequence from this list-track proxy",
        ],
        "ledger_hashes": {
            "functional_classes_detail_hash": hash_payload(functional_classes),
            "basis_profiles_hash": hash_payload([profile_payload]),
            "coordinate_classes_hash": hash_payload(candidate["coordinate_classes"]),
            "template_vectors_hash": hash_payload(candidate["template_vectors"]),
        },
    }
    proof_status, failure = status_for(record)
    record["proof_status"] = proof_status
    record["basis_quotient_audit"]["best_failure_mode"] = failure
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        audit = record["basis_quotient_audit"]
        source = record["source_chamber"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "template_id": source["template_id"],
                    "basis_id": source["basis_id"],
                    "direction": source["direction"],
                    "forced_pairs": source["forced_pairs"],
                    "zero_row_window_dimension": source["zero_row_window_dimension"],
                    "scalar_required_vanishing_union_size": source["scalar_required_vanishing_union_size"],
                    "basis_q_variable_count": audit["best_q_variable_count"],
                    "basis_matrix_shape": record["basis_profiles"][0]["matrix_shape"],
                    "best_failure_mode": audit["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_CYCLEGUARD_STABLE_WINDOW_EXACT_AUDIT_READY")


if __name__ == "__main__":
    main()
