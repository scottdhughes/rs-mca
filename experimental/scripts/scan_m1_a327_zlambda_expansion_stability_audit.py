#!/usr/bin/env python3
"""Audit whether coefficient right kernels survive Z_lambda quotient expansion."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "b3d6a79"
JOINT_DATA = Path("experimental/data/m1_a327_joint_template_right_kernel_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_zlambda_expansion_stability_audit.json")

ROOT = Path(__file__).resolve().parents[2]
JOINT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py"
REALIZATION_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_kernel_template_realization.py"

P = 17
PROXY_PRIME = 12289
K = 256


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


joint = load_module("joint_template_right_kernel_search", JOINT_SCRIPT)
realization = load_module("prescribed_kernel_template_realization", REALIZATION_SCRIPT)
functional = joint.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def coefficient_matrix(profile: dict[str, Any]) -> list[list[int]]:
    return [
        [int(value) % P for value in item["basis_coordinates"]]
        for item in profile["nonbasis_constraint_detail"]
    ]


def profile_by_id(classes: list[dict[str, Any]], profile_summary: dict[str, Any], max_profiles: int) -> dict[str, Any]:
    profiles = joint.right_kernel.candidate_basis_profiles(classes, max_random_profiles=max_profiles)
    return next(
        profile
        for profile in profiles
        if profile["basis_id"] == profile_summary["basis_id"]
        and profile["basis_class_indices"] == profile_summary["basis_class_indices"]
    )


def class_by_index(classes: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {int(row["class_index"]): row for row in classes}


def pair_projection_scalars(candidate: dict[str, Any], profile: dict[str, Any], kernel_vector: list[int]) -> dict[str, int]:
    out: dict[str, int] = {}
    basis_rows = profile["basis_functionals"]
    for left in range(1, 8):
        for right in range(left + 1, 8):
            diff = [
                (int(candidate["template_vectors"][left - 1][idx]) - int(candidate["template_vectors"][right - 1][idx])) % P
                for idx in range(len(candidate["template_vectors"][0]))
            ]
            coords = functional.solve_coordinates(diff, basis_rows)
            if coords is None:
                raise RuntimeError(f"pair P{left}{right} not in basis span")
            out[f"P{left}{right}"] = sum(int(coords[idx]) * int(kernel_vector[idx]) for idx in range(len(coords))) % P
    return out


def audit_profile(candidate: dict[str, Any], classes: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    matrix = coefficient_matrix(profile)
    rank17 = joint.right_kernel.rank_rows(matrix, ncols=6, prime=P)
    rank_proxy_coeff = functional.rank_mod_prime_matrix(matrix, ncols=6, prime=PROXY_PRIME)
    kernel_basis = realization.nullspace(matrix, 6)
    by_index = class_by_index(classes)
    basis_position_sets = [
        set(int(pos) for pos in by_index[int(class_index)]["positions"])
        for class_index in profile["basis_class_indices"]
    ]
    union_positions: set[int] = set()
    intersection_positions = set(range(512))
    for positions in basis_position_sets:
        union_positions |= positions
        intersection_positions &= positions
    basis_support_sizes = [len(item) for item in basis_position_sets]
    kernel_records = []
    for kernel_vector in kernel_basis:
        scalars = pair_projection_scalars(candidate, profile, kernel_vector)
        forced_pairs = [label for label, value in scalars.items() if value == 0]
        kernel_records.append(
            {
                "kernel_vector": kernel_vector,
                "forced_pair_count": len(forced_pairs),
                "forced_pairs": forced_pairs,
                "pair_projection_scalars": scalars,
            }
        )
    best_kernel = min(
        kernel_records,
        key=lambda row: (row["forced_pair_count"], row["kernel_vector"]),
    ) if kernel_records else None
    union_size = len(union_positions)
    stable_common_multiplier_dimension = max(0, K - union_size)
    if rank17 == 6:
        failure = "ZEXP_COEFFICIENT_FULL_RANK"
    elif stable_common_multiplier_dimension <= 0:
        failure = "ZEXP_BASIS_UNION_TOO_LARGE"
    elif best_kernel is not None and best_kernel["forced_pair_count"] > 0:
        failure = "ZEXP_FORCED_PAIR_EQUALITY"
    else:
        failure = "ZEXP_STABLE_LIFT_TARGET"
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": basis_support_sizes,
        "coefficient_matrix_shape": [len(matrix), 6],
        "coefficient_rank_gf17": rank17,
        "coefficient_nullity_gf17": 6 - rank17,
        "coefficient_rank_gf12289": rank_proxy_coeff,
        "coefficient_nullity_gf12289": 6 - rank_proxy_coeff,
        "kernel_basis": kernel_basis,
        "basis_zero_union_size": union_size,
        "basis_zero_intersection_size": len(intersection_positions),
        "stable_common_multiplier_dimension": stable_common_multiplier_dimension,
        "basis_zero_union_hash": hash_payload(sorted(union_positions)),
        "kernel_records": kernel_records,
        "best_forced_pair_count": None if best_kernel is None else best_kernel["forced_pair_count"],
        "best_forced_pairs": None if best_kernel is None else best_kernel["forced_pairs"],
        "best_failure_mode": failure,
    }


def build_record(max_profiles: int) -> dict[str, Any]:
    source = load_json(JOINT_DATA)
    _profiles, raw_candidates = joint.build_candidates(max_specs=36)
    audited = []
    for summary in source["joint_template_search"]["candidate_summaries"]:
        if not summary["right_kernel_profiles"]:
            continue
        candidate = next(
            row for row in raw_candidates
            if row["coordinate_classes_hash"] == summary["coordinate_classes_hash"]
        )
        classes = functional.functional_classes(candidate)
        for profile_summary in summary["right_kernel_profiles"][:max_profiles]:
            profile = profile_by_id(classes, profile_summary, max_profiles=16)
            audited.append(
                {
                    "template_id": summary["template_id"],
                    "template_family": summary["template_family"],
                    "assignment_strategy": summary["assignment_strategy"],
                    "coordinate_classes_hash": summary["coordinate_classes_hash"],
                    "support_vector": summary["support_vector"],
                    "pair7_counts": summary["pair7_counts"],
                    "max_pair_count": summary["max_pair_count"],
                    "functional_classes": summary["functional_classes"],
                    "functional_span_rank": summary["functional_span_rank"],
                    "profile_audit": audit_profile(candidate, classes, profile),
                }
            )
    stable_targets = [
        row for row in audited
        if row["profile_audit"]["best_failure_mode"] == "ZEXP_STABLE_LIFT_TARGET"
    ]
    if stable_targets:
        best = max(
            stable_targets,
            key=lambda row: (
                row["profile_audit"]["stable_common_multiplier_dimension"],
                -row["profile_audit"]["best_forced_pair_count"],
            ),
        )
        proof_status = "CANDIDATE / ZEXP_STABLE_LIFT_TARGET / PARTIAL / EXPERIMENTAL"
        failure = "ZEXP_STABLE_LIFT_TARGET"
    elif audited:
        best = max(
            audited,
            key=lambda row: (
                row["profile_audit"]["stable_common_multiplier_dimension"],
                -(row["profile_audit"]["best_forced_pair_count"] or 99),
                -row["profile_audit"]["basis_zero_union_size"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZEXP_EXPANSION_UNSTABLE / PARTIAL / EXPERIMENTAL"
        failure = best["profile_audit"]["best_failure_mode"]
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZEXP_NO_RIGHT_KERNEL_PROFILES / PARTIAL / EXPERIMENTAL"
        failure = "ZEXP_NO_RIGHT_KERNEL_PROFILES"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": 327,
        "source_commit": SOURCE_COMMIT,
        "joint_template_search": {
            "commit": SOURCE_COMMIT,
            "systems_tested": source["joint_template_search"]["systems_tested"],
            "right_kernel_positive_candidates": source["joint_template_search"]["right_kernel_positive_candidates"],
            "proxy_positive_candidates": source["joint_template_search"]["proxy_positive_candidates"],
            "best_proxy_rank": source["joint_template_search"]["best_proxy_rank"],
            "best_proxy_nullity": source["joint_template_search"]["best_proxy_nullity"],
            "best_failure_mode": source["joint_template_search"]["best_failure_mode"],
        },
        "zlambda_expansion_audit": {
            "profiles_audited": len(audited),
            "stable_lift_targets": len(stable_targets),
            "coefficient_kernel_profiles": sum(
                1 for row in audited if row["profile_audit"]["coefficient_nullity_gf17"] > 0
            ),
            "proxy_characteristic_kernel_profiles": sum(
                1 for row in audited if row["profile_audit"]["coefficient_nullity_gf12289"] > 0
            ),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_id": None if best is None else best["profile_audit"]["basis_id"],
            "best_basis_zero_union_size": None if best is None else best["profile_audit"]["basis_zero_union_size"],
            "best_stable_common_multiplier_dimension": None if best is None else best["profile_audit"]["stable_common_multiplier_dimension"],
            "best_forced_pair_count": None if best is None else best["profile_audit"]["best_forced_pair_count"],
            "best_failure_mode": failure,
            "failure_counts": dict(
                sorted(
                    {
                        label: sum(1 for row in audited if row["profile_audit"]["best_failure_mode"] == label)
                        for label in {row["profile_audit"]["best_failure_mode"] for row in audited}
                    }.items()
                )
            ),
            "profile_summaries": audited,
        },
        "best_profile": best,
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
    parser.add_argument("--max-profiles-per-candidate", type=int, default=8)
    args = parser.parse_args()
    record = build_record(max_profiles=args.max_profiles_per_candidate)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        audit = record["zlambda_expansion_audit"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "profiles_audited": audit["profiles_audited"],
                    "stable_lift_targets": audit["stable_lift_targets"],
                    "coefficient_kernel_profiles": audit["coefficient_kernel_profiles"],
                    "proxy_characteristic_kernel_profiles": audit["proxy_characteristic_kernel_profiles"],
                    "best_template_id": audit["best_template_id"],
                    "best_assignment_strategy": audit["best_assignment_strategy"],
                    "best_basis_id": audit["best_basis_id"],
                    "best_basis_zero_union_size": audit["best_basis_zero_union_size"],
                    "best_stable_common_multiplier_dimension": audit["best_stable_common_multiplier_dimension"],
                    "best_forced_pair_count": audit["best_forced_pair_count"],
                    "best_failure_mode": audit["best_failure_mode"],
                    "failure_counts": audit["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_ZLAMBDA_EXPANSION_STABILITY_AUDIT_READY")


if __name__ == "__main__":
    main()
