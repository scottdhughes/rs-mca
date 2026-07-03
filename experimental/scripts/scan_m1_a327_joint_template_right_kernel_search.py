#!/usr/bin/env python3
"""Joint template/right-kernel proxy search for M1 a=327 selected classes."""

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


SOURCE_COMMIT = "f63a23f"
REALIZATION_DATA = Path("experimental/data/m1_a327_prescribed_kernel_template_realization.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_joint_template_right_kernel_search.json")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_joint_template_right_kernel_search.m2")

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
dependency = right_kernel.dependency
lowrank = right_kernel.lowrank
functional = right_kernel.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize(vectors: list[list[int]]) -> list[list[int]]:
    return [[int(value) % P for value in row] for row in vectors]


def standard_hyperplane_points() -> list[list[int]]:
    return [
        [0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 0],
    ]


def single_outside_template(outside_witness: int, base_variant: int) -> list[list[int]]:
    vectors = standard_hyperplane_points()
    idx = outside_witness - 1
    if base_variant == 0:
        vectors[idx][5] = 1
    elif base_variant == 1:
        vectors[idx] = [0, 0, 0, 0, 0, 1]
    elif base_variant == 2:
        vectors[idx] = [1, 1, 1, 1, 1, 1]
    else:
        rng = random.Random(51000 + 37 * outside_witness + base_variant)
        vectors[idx] = [rng.randrange(P) for _ in range(5)] + [1]
    return normalize(vectors)


def paired_outside_template(left: int, right: int) -> list[list[int]]:
    vectors = standard_hyperplane_points()
    vectors[left - 1][5] = 1
    vectors[right - 1][5] = 1
    return normalize(vectors)


def sheared_outside_template(seed: int) -> list[list[int]]:
    rng = random.Random(52000 + seed)
    vectors = single_outside_template(6 if seed % 2 == 0 else 5, seed % 4)
    for row in vectors:
        for _ in range(2):
            left = rng.randrange(5)
            right = rng.randrange(5)
            if left != right:
                row[left] = (row[left] + rng.randrange(1, P) * row[right]) % P
    return normalize(vectors)


def template_specs(max_specs: int) -> list[dict[str, Any]]:
    specs = []
    seen: set[str] = set()

    def add(template_id: str, family: str, vectors: list[list[int]], sizes: list[int], cost: float, pair7: float) -> None:
        if len(specs) >= max_specs:
            return
        vectors = normalize(vectors)
        key = hash_payload({"vectors": vectors, "sizes": sizes})
        if key in seen:
            return
        seen.add(key)
        specs.append(
            {
                "template_id": template_id,
                "template_family": family,
                "vectors": vectors,
                "selected_class_sizes": sizes,
                "cost_weight": cost,
                "pair7_weight": pair7,
                "assignment_strategies": [
                    "signature_fiber_blocks",
                    "signature_residue_blocks",
                    "pair7_signature_blocks",
                    "dependency_twin_interleave",
                    "fiber_factor_packed",
                    "seeded_dependency_shuffle",
                ],
            }
        )

    for outside in [6, 5, 4, 1, 2, 3, 7]:
        for variant in range(4):
            add(
                f"single_outside_w{outside}_v{variant}",
                "single_outside_rank5_hyperplane",
                single_outside_template(outside, variant),
                [3, 4, 5, 6] if variant % 2 else [3, 4, 5],
                3.5 + variant,
                1.0 + (outside == 7),
            )
    for left, right in [(5, 6), (4, 6), (6, 7), (1, 6), (2, 6), (3, 6)]:
        add(
            f"paired_outside_w{left}_{right}",
            "paired_outside_rank5_hyperplane",
            paired_outside_template(left, right),
            [3, 4, 5, 6],
            4.0,
            1.5,
        )
    for seed in range(max_specs):
        add(
            f"sheared_outside_seed_{seed:03d}",
            "sheared_outside_rank5_hyperplane",
            sheared_outside_template(seed),
            [3, 4, 5, 6] if seed % 3 == 0 else [3, 4, 5],
            4.0 + (seed % 4),
            1.0 + 0.5 * (seed % 3),
        )
    return specs


def structural_status(row: dict[str, Any]) -> str:
    if row["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "JOINT_TEMPLATE_SUPPORT_FAIL"
    if row["max_pair_count"] > PAIR_CAP or min(row["pair7_counts"]) < PAIR7_LOWER:
        return "JOINT_TEMPLATE_PAIR_GUARD_FAIL"
    if row["forced_functional_identities"] > 0:
        return "JOINT_TEMPLATE_FORCED_IDENTITY"
    if row["functional_span_rank"] != 6:
        return "JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN"
    if row["annihilator_dimension"] != 0 or row["annihilator_diagonal"]:
        return "JOINT_TEMPLATE_DIAGONAL_ANNIHILATOR"
    return "JOINT_TEMPLATE_STRUCTURAL_PASS"


def proxy_profile(classes: list[dict[str, Any]], profile: dict[str, Any]) -> dict[str, Any]:
    result = functional.proxy_basis_rank(classes, profile)
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "q_variable_count": profile["q_variable_count"],
        "matrix_shape": result["proxy_matrix_shape"],
        "proxy_field": result["proxy_field"],
        "proxy_rank": result["proxy_rank"],
        "proxy_nullity": result["proxy_nullity"],
        "coefficient_rank": profile["coefficient_rank"],
        "right_kernel_nullity": profile["right_kernel_nullity"],
        "right_kernel_metrics": profile["right_kernel_metrics"],
    }


def analyze_candidate(candidate: dict[str, Any], max_profiles: int, run_proxy: bool) -> dict[str, Any]:
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
        "template_vectors": candidate["template_vectors"],
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
    profiles: list[dict[str, Any]] = []
    if structural == "JOINT_TEMPLATE_STRUCTURAL_PASS":
        profiles = right_kernel.candidate_basis_profiles(classes, max_random_profiles=max_profiles)
    right_kernel_profiles = [profile for profile in profiles if profile["right_kernel_nullity"] > 0]
    row["basis_profiles_tested"] = len(profiles)
    row["right_kernel_profiles"] = [
        {
            "basis_id": profile["basis_id"],
            "basis_class_indices": profile["basis_class_indices"],
            "basis_support_sizes": profile["basis_support_sizes"],
            "q_variable_count": profile["q_variable_count"],
            "matrix_shape": profile["matrix_shape"],
            "coefficient_rank": profile["coefficient_rank"],
            "right_kernel_nullity": profile["right_kernel_nullity"],
            "right_kernel_metrics": profile["right_kernel_metrics"],
        }
        for profile in right_kernel_profiles[:5]
    ]
    proxy_results = []
    if run_proxy and right_kernel_profiles:
        for profile in right_kernel_profiles[:max_profiles]:
            proxy_results.append(proxy_profile(classes, profile))
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
    if structural != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = structural
    elif not right_kernel_profiles:
        row["best_failure_mode"] = "JOINT_TEMPLATE_COEFFICIENT_FULL_RANK"
    elif not proxy_results:
        row["best_failure_mode"] = "JOINT_TEMPLATE_PROXY_PENDING"
    elif row["best_proxy"]["proxy_nullity"] > 0:
        row["best_failure_mode"] = "JOINT_TEMPLATE_PROXY_NULLITY_POSITIVE"
    else:
        row["best_failure_mode"] = "JOINT_TEMPLATE_PROXY_FULL_RANK"
    return row


def build_candidates(max_specs: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    specs = template_specs(max_specs)
    profiles = []
    candidates = []
    for spec_index, spec in enumerate(specs):
        profile = lowrank.solve_template_counts(spec)
        profiles.append(profile)
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for strategy_index, strategy in enumerate(spec["assignment_strategies"]):
            candidates.append(
                dependency.evaluate_dependency_candidate(
                    profile,
                    strategy,
                    seed=61000 + 101 * spec_index + 17 * strategy_index,
                )
            )
    return profiles, candidates


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
        "right_kernel_profiles",
        "structural_status",
        "best_failure_mode",
    ]
    return {key: row[key] for key in keys} | {
        "best_proxy": row["best_proxy"],
        "proxy_results": row["proxy_results"],
    }


def m2_matrix_rows(matrix: list[list[int]]) -> str:
    return "{" + ",".join("{" + ",".join(f"{value}_R" for value in row) + "}" for row in matrix) + "}"


def write_m2_for_best(best: dict[str, Any], raw_candidates: list[dict[str, Any]], max_profiles: int) -> None:
    candidate = next(item for item in raw_candidates if item["coordinate_classes_hash"] == best["coordinate_classes_hash"])
    classes = functional.functional_classes(candidate)
    profiles = right_kernel.candidate_basis_profiles(classes, max_random_profiles=max_profiles)
    target = best["right_kernel_profiles"][0]
    profile = next(
        item
        for item in profiles
        if item["basis_id"] == target["basis_id"] and item["basis_class_indices"] == target["basis_class_indices"]
    )
    matrix = [
        [int(value) % P for value in item["basis_coordinates"]]
        for item in profile["nonbasis_constraint_detail"]
    ]
    text = f"""-- Generated by scan_m1_a327_joint_template_right_kernel_search.py
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


def build_record(max_specs: int, max_proxy_candidates: int, max_profiles: int, run_m2_flag: bool) -> dict[str, Any]:
    previous = load_json(REALIZATION_DATA)
    profiles, raw_candidates = build_candidates(max_specs=max_specs)
    cheap_rows = [analyze_candidate(candidate, max_profiles=max_profiles, run_proxy=False) for candidate in raw_candidates]
    structural = [
        idx for idx, row in enumerate(cheap_rows)
        if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"
    ]
    structural = sorted(
        structural,
        key=lambda idx: (
            len(cheap_rows[idx]["right_kernel_profiles"]),
            cheap_rows[idx]["basis_profiles_tested"],
            cheap_rows[idx]["functional_classes"],
            cheap_rows[idx]["template_id"],
        ),
        reverse=True,
    )
    proxy_indices = set(structural[:max_proxy_candidates])
    rows = [
        analyze_candidate(candidate, max_profiles=max_profiles, run_proxy=idx in proxy_indices)
        for idx, candidate in enumerate(raw_candidates)
    ]
    proxy_positive = [row for row in rows if row["best_failure_mode"] == "JOINT_TEMPLATE_PROXY_NULLITY_POSITIVE"]
    proxy_ranked = [row for row in rows if row["proxy_results"]]
    right_kernel_positive = [row for row in rows if row["right_kernel_profiles"]]
    if proxy_positive:
        best = max(
            proxy_positive,
            key=lambda row: (
                row["best_proxy"]["proxy_nullity"],
                row["best_proxy"]["right_kernel_nullity"],
                -row["best_proxy"]["proxy_rank"],
            ),
        )
        proof_status = "CANDIDATE / JOINT_TEMPLATE_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "JOINT_TEMPLATE_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = max(
            proxy_ranked,
            key=lambda row: (
                row["best_proxy"]["right_kernel_nullity"],
                -row["best_proxy"]["proxy_rank"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / JOINT_TEMPLATE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "JOINT_TEMPLATE_PROXY_FULL_RANK"
    elif right_kernel_positive:
        best = max(right_kernel_positive, key=lambda row: len(row["right_kernel_profiles"]))
        proof_status = "CANDIDATE / JOINT_TEMPLATE_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "JOINT_TEMPLATE_PROXY_PENDING"
    elif rows:
        best = max(rows, key=lambda row: (row["functional_span_rank"], row["basis_profiles_tested"], row["template_id"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / JOINT_TEMPLATE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "JOINT_TEMPLATE_COEFFICIENT_FULL_RANK"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / JOINT_TEMPLATE_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "JOINT_TEMPLATE_SUPPORT_FAIL"
    m2_result = None
    if run_m2_flag and best is not None and best["right_kernel_profiles"]:
        write_m2_for_best(best, raw_candidates, max_profiles)
        m2_result = run_m2()
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_template_realization": {
            "commit": SOURCE_COMMIT,
            "linear_nullity": previous["template_realization"]["linear_nullity"],
            "non_diagonal_kernel_dimension": previous["template_realization"]["non_diagonal_kernel_dimension"],
            "rowspace_valid_samples": previous["template_realization"]["rowspace_valid_samples"],
            "best_failure_mode": previous["template_realization"]["best_failure_mode"],
        },
        "joint_template_search": {
            "templates_tested": len(profiles),
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "right_kernel_positive_candidates": len(right_kernel_positive),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_basis_profiles_tested": sum(len(row["proxy_results"]) for row in rows),
            "proxy_positive_candidates": len(proxy_positive),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_proxy_rank": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "profiles": profiles,
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "m2_right_kernel_check": m2_result,
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
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--run-m2", action="store_true")
    parser.add_argument("--max-specs", type=int, default=36)
    parser.add_argument("--max-proxy-candidates", type=int, default=12)
    parser.add_argument("--max-profiles-per-candidate", type=int, default=16)
    args = parser.parse_args()
    record = build_record(
        max_specs=args.max_specs,
        max_proxy_candidates=args.max_proxy_candidates,
        max_profiles=args.max_profiles_per_candidate,
        run_m2_flag=args.run_m2,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["joint_template_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
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
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_JOINT_TEMPLATE_RIGHT_KERNEL_SEARCH_READY")


if __name__ == "__main__":
    main()
