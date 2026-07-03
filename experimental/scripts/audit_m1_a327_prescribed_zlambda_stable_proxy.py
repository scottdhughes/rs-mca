#!/usr/bin/env python3
"""Single-case proxy-rank audit for the best prescribed Z_lambda-stable target."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import signal
import time
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "70b744e"
INPUT_DATA = Path("experimental/data/m1_a327_prescribed_zlambda_stable_relation_generator.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_prescribed_zlambda_stable_proxy_audit.json")

ROOT = Path(__file__).resolve().parents[2]
JOINT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py"
PZREL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_zlambda_stable_relation_generator.py"
PRESCRIBED_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_right_kernel_selected_class_search.py"

TARGET_AGREEMENT = 327
P = 17


class AuditTimeout(Exception):
    pass


def timeout_handler(_signum, _frame) -> None:
    raise AuditTimeout("proxy rank timed out")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


joint = load_module("joint_template_right_kernel_search", JOINT_SCRIPT)
pzrel = load_module("prescribed_zlambda_stable_relation_generator", PZREL_SCRIPT)
prescribed = load_module("prescribed_right_kernel_selected_class_search", PRESCRIBED_SCRIPT)
functional = joint.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def reconstruct_best(input_record: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    best = input_record["best_candidate"]
    best_profile = best["best_profile"]
    _profiles, raw_candidates = joint.build_candidates(max_specs=input_record["prescribed_stable_relation"]["templates_tested"])
    candidate = next(
        row for row in raw_candidates
        if row["coordinate_classes_hash"] == best["coordinate_classes_hash"]
    )
    classes = functional.functional_classes(candidate)
    _stable_total, profiles = pzrel.stable_profiles_for_candidate(classes, limit=128)
    source = next(profile for profile in profiles if profile["basis_id"] == best_profile["source_basis_id"])
    kernels = prescribed.kernel_specs(max_random=8)
    kernel = next(row for row in kernels if row["kernel_id"] == best_profile["prescribed_kernel_id"])
    engineered = prescribed.engineer_profile(source, kernel)
    return candidate, classes, engineered


def pair_projection_for_engineered(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    kernel = [int(value) % P for value in profile["prescribed_kernel_vector"]]
    return pzrel.pair_projection_for_kernel(candidate, profile, kernel)


def audit(max_seconds: int | None) -> dict[str, Any]:
    input_record = load_json(INPUT_DATA)
    candidate, classes, profile = reconstruct_best(input_record)
    positions = pzrel.zstable.class_position_sets(classes)
    union_size = pzrel.zstable.profile_union_size(profile, positions)
    pair_record = pair_projection_for_engineered(candidate, profile)
    coefficient_matrix = pzrel.zstable.coefficient_matrix(profile)
    coefficient_rank = joint.right_kernel.rank_rows(coefficient_matrix, ncols=6, prime=P)
    coefficient_hash = hash_payload(coefficient_matrix)
    start = time.monotonic()
    proxy_result = None
    status = "PROXY_NOT_RUN"
    timeout = False
    if max_seconds is not None and max_seconds > 0:
        old_handler = signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(max_seconds)
    else:
        old_handler = None
    try:
        proxy_result = functional.proxy_basis_rank(classes, profile)
        status = "PROXY_RANK_PASS"
    except AuditTimeout:
        timeout = True
        status = "PROXY_RANK_TIMEOUT"
    finally:
        if max_seconds is not None and max_seconds > 0:
            signal.alarm(0)
            if old_handler is not None:
                signal.signal(signal.SIGALRM, old_handler)
    runtime = time.monotonic() - start
    proof_status = "CANDIDATE / PZREL_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
    failure = status
    if proxy_result is not None:
        if proxy_result["proxy_nullity"] > 0:
            proof_status = "CANDIDATE / PZREL_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
            failure = "PZREL_PROXY_NULLITY_POSITIVE"
        else:
            proof_status = "EXACT_EXTRACTION_NO_A327 / PZREL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
            failure = "PZREL_PROXY_FULL_RANK"
    elif timeout:
        proof_status = "CANDIDATE / PZREL_PROXY_TIMEOUT / PARTIAL / EXPERIMENTAL"
        failure = "PZREL_PROXY_TIMEOUT"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "input_candidate": {
            "template_id": candidate["template_id"],
            "assignment_strategy": candidate["assignment_strategy"],
            "coordinate_classes_hash": candidate["coordinate_classes_hash"],
            "support_vector": candidate["support_vector"],
            "pair7_counts": candidate["pair7_counts"],
            "max_pair_count": candidate["max_pair_count"],
        },
        "prescribed_profile": {
            "source_basis_id": profile["source_basis_id"],
            "prescribed_kernel_id": profile["prescribed_kernel_id"],
            "prescribed_kernel_vector": profile["prescribed_kernel_vector"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "basis_zero_union_size": union_size,
            "stable_common_multiplier_dimension": 256 - union_size,
            "q_variable_count": profile["q_variable_count"],
            "coefficient_matrix_shape": [len(coefficient_matrix), 6],
            "coefficient_rank": coefficient_rank,
            "right_kernel_nullity": 6 - coefficient_rank,
            "right_kernel_verified": profile["right_kernel_verified"],
            "coefficient_matrix_hash": coefficient_hash,
            "forced_pair_count": pair_record["forced_pair_count"],
            "forced_pairs": pair_record["forced_pairs"],
            "pair_projection_scalars": pair_record["pair_projection_scalars"],
        },
        "proxy_audit": {
            "max_seconds": max_seconds,
            "runtime_seconds": runtime,
            "status": status,
            "timeout": timeout,
            "proxy_result": proxy_result,
            "best_failure_mode": failure,
        },
        "realization_status": "SYNTHETIC_FUNCTIONAL_PROXY_TARGET",
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
            "realized exact template vectors for the prescribed coefficients",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-seconds", type=int, default=300)
    args = parser.parse_args()
    record = audit(max_seconds=args.max_seconds)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        proxy = record["proxy_audit"]
        result = proxy["proxy_result"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "realization_status": record["realization_status"],
                    "status": proxy["status"],
                    "timeout": proxy["timeout"],
                    "runtime_seconds": proxy["runtime_seconds"],
                    "proxy_matrix_shape": None if result is None else result["proxy_matrix_shape"],
                    "proxy_rank": None if result is None else result["proxy_rank"],
                    "proxy_nullity": None if result is None else result["proxy_nullity"],
                    "best_failure_mode": proxy["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PRESCRIBED_ZLAMBDA_STABLE_PROXY_AUDIT_READY")


if __name__ == "__main__":
    main()
