#!/usr/bin/env python3
"""Right-kernel-engineered proxy search for M1 a=327 random-matroid templates."""

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


SOURCE_COMMIT = "e237ab6"
V2_DATA = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v2.json")
DEPENDENCY_DATA = Path("experimental/data/m1_a327_dependency_engineered_rank_feedback.json")
SYZYGY_DATA = Path("experimental/data/m1_a327_random_matroid_syzygy_rigidity_proxy.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_right_kernel_engineered_rank_feedback.json")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_right_kernel_engineered_rank_feedback.m2")

ROOT = Path(__file__).resolve().parents[2]
DEPENDENCY_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_dependency_engineered_rank_feedback.py"

TARGET_AGREEMENT = 327
PAIR7_LOWER = 142
PAIR_CAP = 255
PROXY_PRIME = 12289


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dependency = load_module("dependency_engineered_rank_feedback", DEPENDENCY_SCRIPT)
v3 = dependency.v3
lowrank = dependency.lowrank
functional = dependency.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_rows(rows: list[list[int]], ncols: int, prime: int = 17) -> int:
    matrix = [[int(value) % prime for value in row] for row in rows if any(int(value) % prime for value in row)]
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
        rank += 1
        if rank == len(matrix) or rank == ncols:
            break
    return rank


def profile_from_selected(classes: list[dict[str, Any]], selected: list[int], basis_id: str) -> dict[str, Any] | None:
    rows = [row["functional"] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    if len(selected) != 6 or rank_rows([rows[idx] for idx in selected], ncols=6, prime=17) != 6:
        return None
    basis_rows = [rows[idx] for idx in selected]
    q_variable_count = sum(256 - supports[idx] for idx in selected)
    nonbasis_rows = 0
    nonbasis_constraints = []
    for idx, row in enumerate(rows):
        if idx in selected:
            continue
        coords = functional.solve_coordinates(row, basis_rows)
        if coords is None:
            return None
        nonbasis_rows += supports[idx]
        nonbasis_constraints.append(
            {
                "class_index": int(classes[idx]["class_index"]),
                "support_size": supports[idx],
                "basis_coordinates": coords,
            }
        )
    return {
        "basis_id": basis_id,
        "basis_class_indices": [int(classes[idx]["class_index"]) for idx in selected],
        "basis_functionals": [classes[idx]["functional"] for idx in selected],
        "basis_support_sizes": [supports[idx] for idx in selected],
        "q_variable_count": q_variable_count,
        "nonbasis_constraints": len(nonbasis_constraints),
        "matrix_shape": [nonbasis_rows, q_variable_count],
        "formal_nullity_lower_bound": max(0, q_variable_count - nonbasis_rows),
        "nonbasis_constraint_detail": nonbasis_constraints,
    }


def extend_to_basis(rows: list[list[int]], forced: list[int], order: list[int]) -> list[int] | None:
    selected: list[int] = []
    selected_rows: list[list[int]] = []
    current_rank = 0
    for idx in forced + [item for item in order if item not in forced]:
        if idx in selected:
            continue
        trial_rank = rank_rows(selected_rows + [rows[idx]], ncols=6, prime=17)
        if trial_rank > current_rank:
            selected.append(idx)
            selected_rows.append(rows[idx])
            current_rank = trial_rank
        if current_rank == 6:
            return selected
    return None


def coefficient_rank(profile: dict[str, Any]) -> int:
    rows = [
        [int(value) % 17 for value in item["basis_coordinates"]]
        for item in profile["nonbasis_constraint_detail"]
    ]
    return rank_rows(rows, ncols=len(profile["basis_class_indices"]), prime=17)


def profile_dependency_score(profile: dict[str, Any]) -> dict[str, int]:
    groups = Counter(tuple(int(value) for value in row["basis_coordinates"]) for row in profile["nonbasis_constraint_detail"])
    repeated_groups = sum(1 for value in groups.values() if value > 1)
    repeated_pairs = sum(value * (value - 1) // 2 for value in groups.values() if value > 1)
    repeated_weight = 0
    for key, value in groups.items():
        if value <= 1:
            continue
        repeated_weight += sum(
            int(row["support_size"])
            for row in profile["nonbasis_constraint_detail"]
            if tuple(int(coord) for coord in row["basis_coordinates"]) == key
        )
    return {
        "repeated_coordinate_groups": repeated_groups,
        "repeated_coordinate_pairs": repeated_pairs,
        "repeated_coordinate_weight": repeated_weight,
        "row_surplus": profile["matrix_shape"][0] - profile["q_variable_count"],
        "basis_support_sum": sum(profile["basis_support_sizes"]),
        "dependency_score": 20 * repeated_pairs + repeated_weight + sum(profile["basis_support_sizes"]),
    }


def candidate_basis_profiles(classes: list[dict[str, Any]], max_random_profiles: int) -> list[dict[str, Any]]:
    rows = [row["functional"] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    base_profiles = dependency.dependency_basis_profiles(classes, span_rank=6, random_bases=12)
    profiles: list[dict[str, Any]] = []
    seen: set[tuple[int, ...]] = set()

    def add(profile: dict[str, Any] | None) -> None:
        if profile is None:
            return
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            return
        seen.add(key)
        cr = coefficient_rank(profile)
        metrics = profile_dependency_score(profile)
        profiles.append(
            profile
            | {
                "coefficient_rank": cr,
                "right_kernel_nullity": len(profile["basis_class_indices"]) - cr,
                "right_kernel_metrics": metrics,
            }
        )

    for profile in base_profiles:
        add(profile)

    full_order = sorted(range(len(classes)), key=lambda idx: (-supports[idx], rows[idx]))
    for idx in range(len(classes)):
        complement = [rows[j] for j in range(len(classes)) if j != idx]
        if rank_rows(complement, ncols=6, prime=17) <= 5:
            add(profile_from_selected(classes, extend_to_basis(rows, [idx], full_order) or [], f"essential_single_{idx}"))

    # Pair removals catch cases where no single class is individually essential.
    high_support = sorted(range(len(classes)), key=lambda idx: (-supports[idx], rows[idx]))[:24]
    for left_pos, left in enumerate(high_support):
        for right in high_support[left_pos + 1 :]:
            forced = [left, right]
            if rank_rows([rows[idx] for idx in forced], ncols=6, prime=17) != len(forced):
                continue
            complement = [rows[j] for j in range(len(classes)) if j not in forced]
            if rank_rows(complement, ncols=6, prime=17) <= 5:
                add(
                    profile_from_selected(
                        classes,
                        extend_to_basis(rows, forced, full_order) or [],
                        f"essential_pair_{left}_{right}",
                    )
                )

    for seed in range(max_random_profiles):
        rng = random.Random(17000 + seed)
        order = list(range(len(classes)))
        rng.shuffle(order)
        selected = extend_to_basis(rows, [], order)
        add(profile_from_selected(classes, selected or [], f"right_kernel_random_basis_{seed}"))

    return sorted(
        profiles,
        key=lambda row: (
            row["right_kernel_nullity"],
            row["right_kernel_metrics"]["dependency_score"],
            -row["coefficient_rank"],
            row["q_variable_count"],
        ),
        reverse=True,
    )


def structural_status(row: dict[str, Any]) -> str:
    if row["support_vector"] != [TARGET_AGREEMENT] * 7:
        return "RIGHT_KERNEL_SUPPORT_FAIL"
    if row["max_pair_count"] > PAIR_CAP or min(row["pair7_counts"]) < PAIR7_LOWER:
        return "RIGHT_KERNEL_PAIR_GUARD_FAIL"
    if row["forced_functional_identities"] > 0:
        return "RIGHT_KERNEL_FORCED_IDENTITY"
    if row["functional_span_rank"] != 6:
        return "RIGHT_KERNEL_LOW_FUNCTIONAL_SPAN"
    if row["annihilator_dimension"] != 0 or row["annihilator_diagonal"]:
        return "RIGHT_KERNEL_DIAGONAL_ANNIHILATOR"
    return "RIGHT_KERNEL_STRUCTURAL_PASS"


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
    ann = dependency.v3.annihilator_pair_ranks(candidate["template_vectors"], annihilator)
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
        "annihilator_basis": annihilator,
        "forced_functional_identities": forced,
        **ann,
    }
    structural = structural_status(row)
    row["structural_status"] = structural
    profiles: list[dict[str, Any]] = []
    if structural == "RIGHT_KERNEL_STRUCTURAL_PASS":
        profiles = candidate_basis_profiles(classes, max_random_profiles=max_profiles)
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
                item["right_kernel_metrics"]["dependency_score"],
                -item["proxy_rank"],
            ),
        )
    if structural != "RIGHT_KERNEL_STRUCTURAL_PASS":
        row["best_failure_mode"] = structural
    elif not right_kernel_profiles:
        row["best_failure_mode"] = "RIGHT_KERNEL_COEFFICIENT_FULL_RANK"
    elif not proxy_results:
        row["best_failure_mode"] = "RIGHT_KERNEL_PROXY_PENDING"
    elif row["best_proxy"]["proxy_nullity"] > 0:
        row["best_failure_mode"] = "RIGHT_KERNEL_PROXY_NULLITY_POSITIVE"
    else:
        row["best_failure_mode"] = "RIGHT_KERNEL_PROXY_FULL_RANK"
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in [
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
    } | {
        "best_proxy": row["best_proxy"],
        "proxy_results": row["proxy_results"],
    }


def build_candidates(max_templates: int) -> list[dict[str, Any]]:
    v2 = load_json(V2_DATA)
    specs = dependency.v3.template_specs(v2, max_templates=max_templates)
    strategies = [
        "signature_fiber_blocks",
        "signature_residue_blocks",
        "pair7_signature_blocks",
        "dependency_twin_interleave",
        "fiber_factor_packed",
        "seeded_dependency_shuffle",
    ]
    raw_candidates = []
    for spec_index, spec in enumerate(specs):
        profile = dependency.lowrank.solve_template_counts(spec)
        if profile.get("solver_status") != "OPTIMAL_OR_FEASIBLE":
            continue
        for strategy_index, strategy in enumerate(strategies):
            raw_candidates.append(
                dependency.evaluate_dependency_candidate(
                    profile,
                    strategy,
                    seed=23000 + spec_index * 137 + strategy_index * 19,
                )
            )
    return raw_candidates


def m2_matrix_rows(matrix: list[list[int]]) -> str:
    return "{" + ",".join("{" + ",".join(f"{value}_R" for value in row) + "}" for row in matrix) + "}"


def write_m2_for_profile(profile: dict[str, Any]) -> None:
    matrix = [
        [int(value) % 17 for value in row["basis_coordinates"]]
        for row in profile["nonbasis_constraint_detail"]
    ]
    text = f"""-- Generated by scan_m1_a327_right_kernel_engineered_rank_feedback.py
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


def build_record(max_templates: int, max_coefficient_candidates: int, max_profiles_per_candidate: int, run_m2_flag: bool) -> dict[str, Any]:
    dependency_record = load_json(DEPENDENCY_DATA)
    syzygy_record = load_json(SYZYGY_DATA)
    raw_candidates = build_candidates(max_templates=max_templates)
    cheap_rows = [analyze_candidate(candidate, max_profiles=max_profiles_per_candidate, run_proxy=False) for candidate in raw_candidates]
    structural = [idx for idx, row in enumerate(cheap_rows) if row["structural_status"] == "RIGHT_KERNEL_STRUCTURAL_PASS"]
    structural = sorted(
        structural,
        key=lambda idx: (
            len(cheap_rows[idx]["right_kernel_profiles"]),
            cheap_rows[idx]["basis_profiles_tested"],
            -cheap_rows[idx]["effective_cost"],
            cheap_rows[idx]["template_id"],
        ),
        reverse=True,
    )
    proxy_indices = set(structural[:max_coefficient_candidates])
    rows = [
        analyze_candidate(candidate, max_profiles=max_profiles_per_candidate, run_proxy=idx in proxy_indices)
        for idx, candidate in enumerate(raw_candidates)
    ]
    right_kernel_positive = [row for row in rows if row["right_kernel_profiles"]]
    proxy_positive = [row for row in rows if row["best_failure_mode"] == "RIGHT_KERNEL_PROXY_NULLITY_POSITIVE"]
    proxy_ranked = [row for row in rows if row["proxy_results"]]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_proxy"]["proxy_nullity"])
        proof_status = "CANDIDATE / RIGHT_KERNEL_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "RIGHT_KERNEL_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = max(
            proxy_ranked,
            key=lambda row: (
                row["best_proxy"]["right_kernel_nullity"],
                row["best_proxy"]["right_kernel_metrics"]["dependency_score"],
                -row["best_proxy"]["proxy_rank"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / RIGHT_KERNEL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RIGHT_KERNEL_PROXY_FULL_RANK"
    elif right_kernel_positive:
        best = max(right_kernel_positive, key=lambda row: len(row["right_kernel_profiles"]))
        proof_status = "CANDIDATE / RIGHT_KERNEL_COEFFICIENT_POSITIVE_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "RIGHT_KERNEL_PROXY_PENDING"
    elif rows:
        best = max(rows, key=lambda row: (row["basis_profiles_tested"], row["functional_span_rank"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / RIGHT_KERNEL_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RIGHT_KERNEL_COEFFICIENT_FULL_RANK"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / RIGHT_KERNEL_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "RIGHT_KERNEL_SUPPORT_FAIL"

    m2_result = None
    if run_m2_flag and best is not None and best["right_kernel_profiles"]:
        # Reconstruct the first right-kernel-positive profile for M2 verification.
        best_candidate = next(candidate for candidate in raw_candidates if candidate["coordinate_classes_hash"] == best["coordinate_classes_hash"])
        classes = functional.functional_classes(best_candidate)
        profiles = candidate_basis_profiles(classes, max_random_profiles=max_profiles_per_candidate)
        target = best["right_kernel_profiles"][0]
        profile = next(
            item
            for item in profiles
            if item["basis_id"] == target["basis_id"] and item["basis_class_indices"] == target["basis_class_indices"]
        )
        write_m2_for_profile(profile)
        m2_result = run_m2()

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "dependency_engineered": {
            "commit": "c3bb743",
            "systems_tested": dependency_record["dependency_engineered_search"]["systems_tested"],
            "proxy_positive_candidates": dependency_record["dependency_engineered_search"]["proxy_positive_candidates"],
            "best_template_id": dependency_record["dependency_engineered_search"]["best_template_id"],
            "best_proxy_rank": dependency_record["dependency_engineered_search"]["best_proxy_rank"],
            "best_proxy_nullity": dependency_record["dependency_engineered_search"]["best_proxy_nullity"],
        },
        "syzygy_proxy": {
            "commit": SOURCE_COMMIT,
            "coefficient_matrix_shape": syzygy_record["syzygy_proxy"]["coefficient_matrix_shape"],
            "coefficient_rank": syzygy_record["syzygy_proxy"]["coefficient_rank_python"],
            "right_kernel_nullity": syzygy_record["syzygy_proxy"]["right_kernel_nullity_python"],
            "left_syzygy_dimension": syzygy_record["syzygy_proxy"]["left_syzygy_dimension_python"],
            "best_failure_mode": syzygy_record["syzygy_proxy"]["best_failure_mode"],
        },
        "right_kernel_search": {
            "templates_tested": max_templates,
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "RIGHT_KERNEL_STRUCTURAL_PASS"),
            "coefficient_profiles_tested": sum(row["basis_profiles_tested"] for row in rows),
            "right_kernel_positive_candidates": len(right_kernel_positive),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_basis_profiles_tested": sum(len(row["proxy_results"]) for row in rows),
            "proxy_positive_candidates": len(proxy_positive),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_functional_span_rank": None if best is None else best["functional_span_rank"],
            "best_proxy_rank": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_proxy"] is None else best["best_proxy"]["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
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
    parser.add_argument("--max-templates", type=int, default=18)
    parser.add_argument("--max-coefficient-candidates", type=int, default=12)
    parser.add_argument("--max-profiles-per-candidate", type=int, default=20)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_coefficient_candidates=args.max_coefficient_candidates,
        max_profiles_per_candidate=args.max_profiles_per_candidate,
        run_m2_flag=args.run_m2,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["right_kernel_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "templates_tested": search["templates_tested"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "coefficient_profiles_tested": search["coefficient_profiles_tested"],
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
        print("M1_A327_RIGHT_KERNEL_ENGINEERED_RANK_FEEDBACK_READY")


if __name__ == "__main__":
    main()
