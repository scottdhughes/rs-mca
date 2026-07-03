#!/usr/bin/env python3
"""Prescribe right-kernel coefficient relations for M1 a=327 selected-class proxies."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "6d58c96"
RIGHT_KERNEL_DATA = Path("experimental/data/m1_a327_right_kernel_engineered_rank_feedback.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_prescribed_right_kernel_selected_class_search.json")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_prescribed_right_kernel_selected_class_search.m2")

ROOT = Path(__file__).resolve().parents[2]
RIGHT_KERNEL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_right_kernel_engineered_rank_feedback.py"

TARGET_AGREEMENT = 327
PAIR7_LOWER = 142
PAIR_CAP = 255
P = 17


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


right_kernel = load_module("right_kernel_engineered_rank_feedback", RIGHT_KERNEL_SCRIPT)
functional = right_kernel.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def kernel_specs(max_random: int) -> list[dict[str, Any]]:
    kernels = [
        ("slot_6_kernel", [0, 0, 0, 0, 0, 1]),
        ("all_ones_kernel", [1, 1, 1, 1, 1, 1]),
        ("fibonacci_kernel", [1, 2, 3, 5, 8, 13]),
        ("alternating_kernel", [1, 16, 1, 16, 1, 16]),
        ("sparse_246_kernel", [0, 1, 0, 1, 0, 1]),
    ]
    for seed in range(max_random):
        rng = random.Random(31000 + seed)
        row = [rng.randrange(P) for _ in range(6)]
        while not any(row):
            row = [rng.randrange(P) for _ in range(6)]
        kernels.append((f"random_kernel_{seed}", row))
    out = []
    seen: set[tuple[int, ...]] = set()
    for kernel_id, vector in kernels:
        normalized = functional.normalize_projective(vector)
        if normalized in seen:
            continue
        seen.add(normalized)
        out.append({"kernel_id": kernel_id, "kernel_vector": list(normalized)})
    return out


def dot_mod(left: list[int], right: list[int]) -> int:
    return sum(int(a) * int(b) for a, b in zip(left, right, strict=True)) % P


def project_to_kernel(coords: list[int], kernel: list[int], salt: int) -> list[int]:
    row = [int(value) % P for value in coords]
    pivot = next((idx for idx, value in reversed(list(enumerate(kernel))) if int(value) % P), None)
    if pivot is None:
        raise RuntimeError("zero kernel")
    acc = sum(row[idx] * int(kernel[idx]) for idx in range(len(row)) if idx != pivot) % P
    row[pivot] = (-acc * pow(int(kernel[pivot]) % P, -1, P)) % P
    if any(row):
        return row
    # Avoid turning a nonbasis row into a vacuous constraint.
    free = [idx for idx in range(len(row)) if idx != pivot]
    idx = free[salt % len(free)]
    row[idx] = 1
    acc = int(kernel[idx]) % P
    row[pivot] = (-acc * pow(int(kernel[pivot]) % P, -1, P)) % P
    return row


def coefficient_rank(profile: dict[str, Any]) -> int:
    rows = [
        [int(value) % P for value in item["basis_coordinates"]]
        for item in profile["nonbasis_constraint_detail"]
    ]
    return right_kernel.rank_rows(rows, ncols=len(profile["basis_class_indices"]), prime=P)


def engineer_profile(profile: dict[str, Any], kernel: dict[str, Any]) -> dict[str, Any]:
    kernel_vector = [int(value) % P for value in kernel["kernel_vector"]]
    engineered_detail = []
    changed = 0
    for salt, item in enumerate(profile["nonbasis_constraint_detail"]):
        old = [int(value) % P for value in item["basis_coordinates"]]
        new = project_to_kernel(old, kernel_vector, salt)
        if new != old:
            changed += 1
        engineered_detail.append(
            {
                "class_index": int(item["class_index"]),
                "support_size": int(item["support_size"]),
                "basis_coordinates": new,
            }
        )
    engineered = {
        **profile,
        "basis_id": f"{profile['basis_id']}__{kernel['kernel_id']}",
        "source_basis_id": profile["basis_id"],
        "prescribed_kernel_id": kernel["kernel_id"],
        "prescribed_kernel_vector": kernel_vector,
        "nonbasis_constraint_detail": engineered_detail,
        "coordinate_rows_changed": changed,
    }
    rank = coefficient_rank(engineered)
    engineered["coefficient_rank"] = rank
    engineered["right_kernel_nullity"] = len(profile["basis_class_indices"]) - rank
    engineered["right_kernel_verified"] = all(
        dot_mod(item["basis_coordinates"], kernel_vector) == 0
        for item in engineered["nonbasis_constraint_detail"]
    )
    return engineered


def structural_status(row: dict[str, Any]) -> str:
    if row["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "PRESCRIBED_KERNEL_SUPPORT_FAIL"
    if row["max_pair_count"] > PAIR_CAP or min(row["pair7_counts"]) < PAIR7_LOWER:
        return "PRESCRIBED_KERNEL_PAIR_GUARD_FAIL"
    if row["forced_functional_identities"] > 0:
        return "PRESCRIBED_KERNEL_FORCED_IDENTITY"
    if row["functional_span_rank"] != 6:
        return "PRESCRIBED_KERNEL_LOW_FUNCTIONAL_SPAN"
    if row["annihilator_dimension"] != 0 or row["annihilator_diagonal"]:
        return "PRESCRIBED_KERNEL_DIAGONAL_ANNIHILATOR"
    return "PRESCRIBED_KERNEL_STRUCTURAL_PASS"


def proxy_engineered_profile(classes: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    result = functional.proxy_basis_rank(classes, profile)
    return {
        "basis_id": profile["basis_id"],
        "source_basis_id": profile["source_basis_id"],
        "prescribed_kernel_id": profile["prescribed_kernel_id"],
        "prescribed_kernel_vector": profile["prescribed_kernel_vector"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "q_variable_count": profile["q_variable_count"],
        "matrix_shape": result["proxy_matrix_shape"],
        "proxy_field": result["proxy_field"],
        "proxy_rank": result["proxy_rank"],
        "proxy_nullity": result["proxy_nullity"],
        "coefficient_rank": profile["coefficient_rank"],
        "right_kernel_nullity": profile["right_kernel_nullity"],
        "coordinate_rows_changed": profile["coordinate_rows_changed"],
    }


def analyze_candidate(
    candidate: dict[str, Any],
    kernels: list[dict[str, Any]],
    max_profiles: int,
    run_proxy: bool,
) -> dict[str, Any]:
    classes = functional.functional_classes(candidate)
    functionals = [row["functional"] for row in classes]
    span_rank = functional.rank_mod_p(functionals)
    annihilator = functional.nullspace_basis(functionals)
    ann = right_kernel.v3.annihilator_pair_ranks(candidate["template_vectors"], annihilator)
    forced = sum(1 for item in classes if item["forced_identity"])
    row = {
        "template_id": candidate["template_id"],
        "template_family": candidate["template_family"],
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "template_dimension": candidate["template_dimension"],
        "support_vector": candidate["support_vector"],
        "pair7_counts": candidate["pair7_counts"],
        "max_pair_count": candidate["max_pair_count"],
        "selected_class_size_counts": candidate["selected_class_size_counts"],
        "effective_cost": candidate["total_effective_cost"],
        "variable_count": candidate["variable_count"],
        "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        "functional_classes": len(classes),
        "functional_classes_hash": hash_payload(classes),
        "functional_span_rank": span_rank,
        "annihilator_dimension": len(annihilator),
        "forced_functional_identities": forced,
        **ann,
    }
    structural = structural_status(row)
    row["structural_status"] = structural
    base_profiles: list[dict[str, Any]] = []
    engineered_profiles: list[dict[str, Any]] = []
    if structural == "PRESCRIBED_KERNEL_STRUCTURAL_PASS":
        base_profiles = right_kernel.candidate_basis_profiles(classes, max_random_profiles=max_profiles)
        for profile in base_profiles[:max_profiles]:
            for kernel in kernels:
                engineered = engineer_profile(profile, kernel)
                if engineered["right_kernel_nullity"] > 0 and engineered["right_kernel_verified"]:
                    engineered_profiles.append(engineered)
    row["basis_profiles_tested"] = len(base_profiles)
    row["engineered_profiles_tested"] = len(engineered_profiles)
    row["right_kernel_positive_profiles"] = [
        {
            "basis_id": profile["basis_id"],
            "source_basis_id": profile["source_basis_id"],
            "prescribed_kernel_id": profile["prescribed_kernel_id"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "q_variable_count": profile["q_variable_count"],
            "matrix_shape": profile["matrix_shape"],
            "coefficient_rank": profile["coefficient_rank"],
            "right_kernel_nullity": profile["right_kernel_nullity"],
            "coordinate_rows_changed": profile["coordinate_rows_changed"],
        }
        for profile in engineered_profiles[:5]
    ]
    proxy_results = []
    if run_proxy and engineered_profiles:
        for profile in engineered_profiles[:max_profiles]:
            proxy_results.append(proxy_engineered_profile(classes, profile))
            if proxy_results[-1]["proxy_nullity"] and proxy_results[-1]["proxy_nullity"] > 0:
                break
    row["proxy_results"] = proxy_results
    row["best_proxy"] = None
    if proxy_results:
        row["best_proxy"] = max(
            proxy_results,
            key=lambda item: (
                item["proxy_nullity"],
                item["right_kernel_nullity"],
                -item["proxy_rank"],
                item["q_variable_count"],
            ),
        )
    if structural != "PRESCRIBED_KERNEL_STRUCTURAL_PASS":
        row["best_failure_mode"] = structural
    elif not engineered_profiles:
        row["best_failure_mode"] = "PRESCRIBED_KERNEL_COEFFICIENT_FAIL"
    elif not proxy_results:
        row["best_failure_mode"] = "PRESCRIBED_KERNEL_PROXY_PENDING"
    elif row["best_proxy"]["proxy_nullity"] > 0:
        row["best_failure_mode"] = "PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE"
    else:
        row["best_failure_mode"] = "PRESCRIBED_KERNEL_PROXY_FULL_RANK"
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "template_family",
        "assignment_strategy",
        "assignment_seed",
        "template_dimension",
        "support_vector",
        "pair7_counts",
        "max_pair_count",
        "selected_class_size_counts",
        "effective_cost",
        "variable_count",
        "coordinate_classes_hash",
        "functional_classes",
        "functional_span_rank",
        "annihilator_dimension",
        "forced_functional_identities",
        "basis_profiles_tested",
        "engineered_profiles_tested",
        "right_kernel_positive_profiles",
        "structural_status",
        "best_failure_mode",
    ]
    return {key: row[key] for key in keys} | {
        "best_proxy": row["best_proxy"],
        "proxy_results": row["proxy_results"],
    }


def m2_matrix_rows(matrix: list[list[int]]) -> str:
    return "{" + ",".join("{" + ",".join(f"{value}_R" for value in row) + "}" for row in matrix) + "}"


def write_m2_for_proxy(best_proxy: dict[str, Any], row: dict[str, Any], raw_candidates: list[dict[str, Any]], kernels: list[dict[str, Any]], max_profiles: int) -> None:
    candidate = next(candidate for candidate in raw_candidates if candidate["coordinate_classes_hash"] == row["coordinate_classes_hash"])
    classes = functional.functional_classes(candidate)
    profiles = right_kernel.candidate_basis_profiles(classes, max_random_profiles=max_profiles)
    kernel = next(item for item in kernels if item["kernel_id"] == best_proxy["prescribed_kernel_id"])
    source = next(
        profile
        for profile in profiles
        if profile["basis_id"] == best_proxy["source_basis_id"]
        and profile["basis_class_indices"] == best_proxy["basis_class_indices"]
    )
    engineered = engineer_profile(source, kernel)
    matrix = [
        [int(value) % P for value in item["basis_coordinates"]]
        for item in engineered["nonbasis_constraint_detail"]
    ]
    text = f"""-- Generated by scan_m1_a327_prescribed_right_kernel_selected_class_search.py
R = ZZ/17[x]
Coeff = matrix({m2_matrix_rows(matrix)})
print concatenate("M2_COEFF_ROWS=", toString numRows Coeff)
print concatenate("M2_COEFF_COLS=", toString numColumns Coeff)
print concatenate("M2_COEFF_RANK=", toString rank Coeff)
RightK = gens kernel Coeff
print concatenate("M2_RIGHT_KERNEL_GENS=", toString numColumns RightK)
LeftK = gens kernel transpose Coeff
print concatenate("M2_LEFT_SYZYGY_GENS=", toString numColumns LeftK)
print concatenate("M2_LEFT_SYZYGY_RANK=", toString rank LeftK)
"""
    M2_SCRIPT_PATH.write_text(text)


def run_m2() -> dict[str, Any]:
    proc = subprocess.run(
        ["M2", "--script", str(M2_SCRIPT_PATH)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    parsed: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        if line.startswith("M2_") and "=" in line:
            key, value = line.split("=", 1)
            parsed[key] = int(value)
    return {
        "command": ["M2", "--script", str(M2_SCRIPT_PATH)],
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "parsed": parsed,
    }


def build_record(max_templates: int, max_proxy_candidates: int, max_profiles: int, max_random_kernels: int, run_m2_flag: bool) -> dict[str, Any]:
    previous = load_json(RIGHT_KERNEL_DATA)
    kernels = kernel_specs(max_random=max_random_kernels)
    raw_candidates = right_kernel.build_candidates(max_templates=max_templates)
    cheap_rows = [
        analyze_candidate(candidate, kernels=kernels, max_profiles=max_profiles, run_proxy=False)
        for candidate in raw_candidates
    ]
    structural = [
        idx for idx, row in enumerate(cheap_rows)
        if row["structural_status"] == "PRESCRIBED_KERNEL_STRUCTURAL_PASS"
    ]
    structural = sorted(
        structural,
        key=lambda idx: (
            cheap_rows[idx]["engineered_profiles_tested"],
            cheap_rows[idx]["basis_profiles_tested"],
            -cheap_rows[idx]["effective_cost"],
            cheap_rows[idx]["template_id"],
        ),
        reverse=True,
    )
    proxy_indices = set(structural[:max_proxy_candidates])
    rows = [
        analyze_candidate(candidate, kernels=kernels, max_profiles=max_profiles, run_proxy=idx in proxy_indices)
        for idx, candidate in enumerate(raw_candidates)
    ]
    proxy_positive = [row for row in rows if row["best_failure_mode"] == "PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE"]
    proxy_ranked = [row for row in rows if row["proxy_results"]]
    right_kernel_positive = [row for row in rows if row["right_kernel_positive_profiles"]]
    if proxy_positive:
        best = max(
            proxy_positive,
            key=lambda row: (
                row["best_proxy"]["proxy_nullity"],
                row["best_proxy"]["right_kernel_nullity"],
                -row["best_proxy"]["proxy_rank"],
            ),
        )
        proof_status = "CANDIDATE / PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = max(
            proxy_ranked,
            key=lambda row: (
                row["best_proxy"]["right_kernel_nullity"],
                -row["best_proxy"]["proxy_rank"],
                row["best_proxy"]["q_variable_count"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / PRESCRIBED_KERNEL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "PRESCRIBED_KERNEL_PROXY_FULL_RANK"
    elif right_kernel_positive:
        best = max(right_kernel_positive, key=lambda row: len(row["right_kernel_positive_profiles"]))
        proof_status = "CANDIDATE / PRESCRIBED_KERNEL_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "PRESCRIBED_KERNEL_PROXY_PENDING"
    elif rows:
        best = max(rows, key=lambda row: (row["basis_profiles_tested"], row["functional_span_rank"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / PRESCRIBED_KERNEL_COEFFICIENT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "PRESCRIBED_KERNEL_COEFFICIENT_FAIL"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / PRESCRIBED_KERNEL_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "PRESCRIBED_KERNEL_SUPPORT_FAIL"

    m2_result = None
    if run_m2_flag and best is not None and best["best_proxy"] is not None:
        write_m2_for_proxy(best["best_proxy"], best, raw_candidates, kernels, max_profiles)
        m2_result = run_m2()

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_right_kernel_search": {
            "commit": SOURCE_COMMIT,
            "systems_tested": previous["right_kernel_search"]["systems_tested"],
            "coefficient_profiles_tested": previous["right_kernel_search"]["coefficient_profiles_tested"],
            "right_kernel_positive_candidates": previous["right_kernel_search"]["right_kernel_positive_candidates"],
            "best_failure_mode": previous["right_kernel_search"]["best_failure_mode"],
        },
        "prescribed_kernel_search": {
            "templates_tested": max_templates,
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "PRESCRIBED_KERNEL_STRUCTURAL_PASS"),
            "basis_profiles_tested": sum(row["basis_profiles_tested"] for row in rows),
            "engineered_profiles_tested": sum(row["engineered_profiles_tested"] for row in rows),
            "right_kernel_positive_candidates": len(right_kernel_positive),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_basis_profiles_tested": sum(len(row["proxy_results"]) for row in rows),
            "proxy_positive_candidates": len(proxy_positive),
            "kernel_ids_tested": [item["kernel_id"] for item in kernels],
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_proxy_rank": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "m2_right_kernel_check": m2_result,
        "realization_status": "SYNTHETIC_FUNCTIONAL_PROXY_TARGET",
        "realization_note": (
            "The selected-class support ledger is inherited from exact template candidates, "
            "but nonbasis coefficient rows are prescribed in basis coordinates. A later branch "
            "must realize these engineered functionals by actual template vectors before Sage exact audit."
        ),
        "exact_audit": {
            "run": False,
            "field": None,
            "H_order": None,
            "rank": None,
            "nullity": None,
            "best_failure_mode": None,
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
            "realized exact template vectors for the prescribed coefficients",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--run-m2", action="store_true")
    parser.add_argument("--max-templates", type=int, default=18)
    parser.add_argument("--max-proxy-candidates", type=int, default=12)
    parser.add_argument("--max-profiles-per-candidate", type=int, default=8)
    parser.add_argument("--max-random-kernels", type=int, default=4)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_proxy_candidates=args.max_proxy_candidates,
        max_profiles=args.max_profiles_per_candidate,
        max_random_kernels=args.max_random_kernels,
        run_m2_flag=args.run_m2,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["prescribed_kernel_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "engineered_profiles_tested": search["engineered_profiles_tested"],
                    "right_kernel_positive_candidates": search["right_kernel_positive_candidates"],
                    "proxy_candidates_tested": search["proxy_candidates_tested"],
                    "proxy_basis_profiles_tested": search["proxy_basis_profiles_tested"],
                    "proxy_positive_candidates": search["proxy_positive_candidates"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                    "realization_status": record["realization_status"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PRESCRIBED_RIGHT_KERNEL_SELECTED_CLASS_SEARCH_READY")


if __name__ == "__main__":
    main()
