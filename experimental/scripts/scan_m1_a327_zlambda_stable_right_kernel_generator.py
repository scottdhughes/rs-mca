#!/usr/bin/env python3
"""Search actual-template right kernels that survive Z_lambda expansion gates."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "f47d995"
ZEXP_DATA = Path("experimental/data/m1_a327_zlambda_expansion_stability_audit.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_zlambda_stable_right_kernel_generator.json")

ROOT = Path(__file__).resolve().parents[2]
JOINT_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_joint_template_right_kernel_search.py"
ZEXP_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_zlambda_expansion_stability_audit.py"
REALIZATION_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_kernel_template_realization.py"

TARGET_AGREEMENT = 327
PAIR7_LOWER = 142
PAIR_CAP = 255
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
zexp = load_module("zlambda_expansion_stability_audit", ZEXP_SCRIPT)
realization = load_module("prescribed_kernel_template_realization", REALIZATION_SCRIPT)
functional = joint.functional


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def class_position_sets(classes: list[dict[str, Any]]) -> dict[int, set[int]]:
    return {
        int(row["class_index"]): {int(pos) for pos in row["positions"]}
        for row in classes
    }


def profile_union_size(profile: dict[str, Any], positions: dict[int, set[int]]) -> int:
    union: set[int] = set()
    for class_index in profile["basis_class_indices"]:
        union |= positions[int(class_index)]
    return len(union)


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix, strict=True)]


def inverse_matrix(matrix: list[list[int]], prime: int = P) -> list[list[int]] | None:
    n = len(matrix)
    work = [
        [int(value) % prime for value in row] + [1 if row_idx == col else 0 for col in range(n)]
        for row_idx, row in enumerate(matrix)
    ]
    rank = 0
    for col in range(n):
        pivot = None
        for row_idx in range(rank, n):
            if work[row_idx][col] % prime:
                pivot = row_idx
                break
        if pivot is None:
            return None
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, prime)
        work[rank] = [(value * inv) % prime for value in work[rank]]
        for row_idx in range(n):
            if row_idx == rank or not work[row_idx][col] % prime:
                continue
            factor = work[row_idx][col] % prime
            work[row_idx] = [
                (work[row_idx][idx] - factor * work[rank][idx]) % prime
                for idx in range(2 * n)
            ]
        rank += 1
    return [row[n:] for row in work]


def mat_vec(matrix: list[list[int]], vector: list[int], prime: int = P) -> list[int]:
    return [sum(row[idx] * int(vector[idx]) for idx in range(len(vector))) % prime for row in matrix]


def coefficient_matrix(profile: dict[str, Any]) -> list[list[int]]:
    return [
        [int(value) % P for value in item["basis_coordinates"]]
        for item in profile["nonbasis_constraint_detail"]
    ]


def pair_projection_record(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    matrix = coefficient_matrix(profile)
    kernel_basis = realization.nullspace(matrix, len(profile["basis_class_indices"]))
    records = []
    for vector in kernel_basis:
        scalars = zexp.pair_projection_scalars(candidate, profile, vector)
        forced = [label for label, value in scalars.items() if value == 0]
        records.append(
            {
                "kernel_vector": vector,
                "forced_pair_count": len(forced),
                "forced_pairs": forced,
                "pair_projection_scalars": scalars,
            }
        )
    best = min(records, key=lambda row: (row["forced_pair_count"], row["kernel_vector"])) if records else None
    return {
        "kernel_basis": kernel_basis,
        "best_forced_pair_count": None if best is None else best["forced_pair_count"],
        "best_forced_pairs": None if best is None else best["forced_pairs"],
        "best_pair_projection_scalars": None if best is None else best["pair_projection_scalars"],
    }


def summarize_profile(candidate: dict[str, Any], profile: dict[str, Any], positions: dict[int, set[int]], run_proxy: bool) -> dict[str, Any]:
    matrix = coefficient_matrix(profile)
    rank17 = joint.right_kernel.rank_rows(matrix, ncols=len(profile["basis_class_indices"]), prime=P)
    rank_proxy_coeff = functional.rank_mod_prime_matrix(matrix, ncols=len(profile["basis_class_indices"]), prime=PROXY_PRIME)
    union_size = profile_union_size(profile, positions)
    stable_dim = max(0, K - union_size)
    pair_record = pair_projection_record(candidate, profile) if rank17 < len(profile["basis_class_indices"]) else {
        "kernel_basis": [],
        "best_forced_pair_count": None,
        "best_forced_pairs": None,
        "best_pair_projection_scalars": None,
    }
    failure = "ZSTABLE_STABLE_LIFT_TARGET"
    if rank17 == len(profile["basis_class_indices"]):
        failure = "ZSTABLE_COEFFICIENT_FULL_RANK"
    elif stable_dim <= 0:
        failure = "ZSTABLE_BASIS_UNION_TOO_LARGE"
    elif pair_record["best_forced_pair_count"] and pair_record["best_forced_pair_count"] > 0:
        failure = "ZSTABLE_FORCED_PAIR_EQUALITY"
    proxy = None
    if run_proxy and failure == "ZSTABLE_STABLE_LIFT_TARGET":
        proxy_result = functional.proxy_basis_rank(functional.functional_classes(candidate), profile)
        proxy = {
            "matrix_shape": proxy_result["proxy_matrix_shape"],
            "proxy_field": proxy_result["proxy_field"],
            "proxy_rank": proxy_result["proxy_rank"],
            "proxy_nullity": proxy_result["proxy_nullity"],
        }
        if proxy["proxy_nullity"] > 0:
            failure = "ZSTABLE_PROXY_NULLITY_POSITIVE"
        else:
            failure = "ZSTABLE_PROXY_FULL_RANK"
    return {
        "basis_id": profile["basis_id"],
        "basis_class_indices": profile["basis_class_indices"],
        "basis_support_sizes": profile["basis_support_sizes"],
        "q_variable_count": profile["q_variable_count"],
        "coefficient_matrix_shape": [len(matrix), len(profile["basis_class_indices"])],
        "coefficient_rank_gf17": rank17,
        "coefficient_nullity_gf17": len(profile["basis_class_indices"]) - rank17,
        "coefficient_rank_gf12289": rank_proxy_coeff,
        "coefficient_nullity_gf12289": len(profile["basis_class_indices"]) - rank_proxy_coeff,
        "basis_zero_union_size": union_size,
        "stable_common_multiplier_dimension": stable_dim,
        "basis_zero_union_hash": hash_payload(sorted(set().union(*(positions[int(idx)] for idx in profile["basis_class_indices"])))),
        **pair_record,
        "proxy_result": proxy,
        "best_failure_mode": failure,
    }


def candidate_structural_row(candidate: dict[str, Any]) -> dict[str, Any]:
    classes = functional.functional_classes(candidate)
    functionals = [row["functional"] for row in classes]
    span_rank = functional.rank_mod_p(functionals)
    annihilator = functional.nullspace_basis(functionals)
    ann = joint.right_kernel.v3.annihilator_pair_ranks(candidate["template_vectors"], annihilator)
    forced = sum(1 for row in classes if row["forced_identity"])
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
    row["structural_status"] = joint.structural_status(row)
    return row


def profile_from_combo(classes: list[dict[str, Any]], combo: tuple[int, ...], basis_id: str) -> dict[str, Any] | None:
    if len(combo) != 6:
        return None
    rows = [[int(value) % P for value in row["functional"]] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    basis_rows = [rows[idx] for idx in combo]
    inv_transpose = inverse_matrix(transpose(basis_rows), prime=P)
    if inv_transpose is None:
        return None
    q_variable_count = sum(K - supports[idx] for idx in combo)
    nonbasis_rows = 0
    nonbasis_constraints = []
    combo_set = set(combo)
    for idx, row in enumerate(rows):
        if idx in combo_set:
            continue
        coords = mat_vec(inv_transpose, row, prime=P)
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
        "basis_class_indices": [int(classes[idx]["class_index"]) for idx in combo],
        "basis_functionals": [classes[idx]["functional"] for idx in combo],
        "basis_support_sizes": [supports[idx] for idx in combo],
        "q_variable_count": q_variable_count,
        "nonbasis_constraints": len(nonbasis_constraints),
        "matrix_shape": [nonbasis_rows, q_variable_count],
        "formal_nullity_lower_bound": max(0, q_variable_count - nonbasis_rows),
        "nonbasis_constraint_detail": nonbasis_constraints,
    }


def stability_basis_profiles(classes: list[dict[str, Any]], max_basis_combinations: int) -> tuple[int, list[dict[str, Any]]]:
    positions = class_position_sets(classes)
    combos = []
    for combo in itertools.combinations(range(len(classes)), 6):
        union_size = len(set().union(*(positions[int(classes[idx]["class_index"])] for idx in combo)))
        support_sum = sum(int(classes[idx]["support_size"]) for idx in combo)
        combos.append((union_size, -support_sum, combo))
    combos.sort()
    tested = 0
    profiles: list[dict[str, Any]] = []
    seen: set[tuple[int, ...]] = set()
    for union_size, _support_key, combo in combos[:max_basis_combinations]:
        profile = profile_from_combo(
            classes,
            tuple(combo),
            f"zstable_union_{union_size}_{'_'.join(str(classes[idx]['class_index']) for idx in combo)}",
        )
        tested += 1
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        profiles.append(profile)
    return tested, profiles


def mapped_structural_failure(status: str) -> str:
    return {
        "JOINT_TEMPLATE_SUPPORT_FAIL": "ZSTABLE_SUPPORT_FAIL",
        "JOINT_TEMPLATE_PAIR_GUARD_FAIL": "ZSTABLE_PAIR_GUARD_FAIL",
        "JOINT_TEMPLATE_FORCED_IDENTITY": "ZSTABLE_FORCED_IDENTITY",
        "JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN": "ZSTABLE_LOW_FUNCTIONAL_SPAN",
        "JOINT_TEMPLATE_DIAGONAL_ANNIHILATOR": "ZSTABLE_DIAGONAL_ANNIHILATOR",
    }.get(status, status)


def analyze_candidate(candidate: dict[str, Any], max_basis_combinations: int, run_proxy: bool) -> dict[str, Any]:
    row = candidate_structural_row(candidate)
    classes = functional.functional_classes(candidate)
    positions = class_position_sets(classes)
    row["basis_profiles_tested"] = 0
    row["coefficient_kernel_profiles"] = 0
    row["stable_basis_union_profiles"] = 0
    row["pair_projection_clear_profiles"] = 0
    row["proxy_results_tested"] = 0
    row["proxy_positive_profiles"] = 0
    row["best_profile"] = None
    row["profile_summaries"] = []
    if row["structural_status"] != "JOINT_TEMPLATE_STRUCTURAL_PASS":
        row["best_failure_mode"] = mapped_structural_failure(row["structural_status"])
        return row
    tested, profiles = stability_basis_profiles(classes, max_basis_combinations=max_basis_combinations)
    row["basis_profiles_tested"] = tested
    summaries = []
    for profile in profiles:
        matrix = coefficient_matrix(profile)
        rank17 = joint.right_kernel.rank_rows(matrix, ncols=6, prime=P)
        if rank17 == 6:
            continue
        # Expensive pair-projection and optional proxy only run after a right kernel exists.
        summary = summarize_profile(candidate, profile, positions, run_proxy=run_proxy)
        summaries.append(summary)
        if summary["best_failure_mode"] in {"ZSTABLE_PROXY_NULLITY_POSITIVE", "ZSTABLE_PROXY_FULL_RANK"}:
            row["proxy_results_tested"] += 1
        if summary["best_failure_mode"] == "ZSTABLE_PROXY_NULLITY_POSITIVE":
            row["proxy_positive_profiles"] += 1
            break
    row["profile_summaries"] = sorted(
        summaries,
        key=lambda item: (
            item["best_failure_mode"] == "ZSTABLE_PROXY_NULLITY_POSITIVE",
            item["best_failure_mode"] == "ZSTABLE_PROXY_FULL_RANK",
            item["stable_common_multiplier_dimension"],
            -(item["best_forced_pair_count"] if item["best_forced_pair_count"] is not None else 99),
            -item["basis_zero_union_size"],
            item["coefficient_nullity_gf17"],
        ),
        reverse=True,
    )[:8]
    row["coefficient_kernel_profiles"] = len(summaries)
    row["stable_basis_union_profiles"] = sum(1 for item in summaries if item["stable_common_multiplier_dimension"] > 0)
    row["pair_projection_clear_profiles"] = sum(
        1
        for item in summaries
        if item["stable_common_multiplier_dimension"] > 0 and item["best_forced_pair_count"] == 0
    )
    row["best_profile"] = row["profile_summaries"][0] if row["profile_summaries"] else None
    if row["proxy_positive_profiles"]:
        row["best_failure_mode"] = "ZSTABLE_PROXY_NULLITY_POSITIVE"
    elif any(item["best_failure_mode"] == "ZSTABLE_PROXY_FULL_RANK" for item in summaries):
        row["best_failure_mode"] = "ZSTABLE_PROXY_FULL_RANK"
    elif row["pair_projection_clear_profiles"]:
        row["best_failure_mode"] = "ZSTABLE_PROXY_PENDING"
    elif row["stable_basis_union_profiles"]:
        row["best_failure_mode"] = "ZSTABLE_FORCED_PAIR_EQUALITY"
    elif row["coefficient_kernel_profiles"]:
        row["best_failure_mode"] = "ZSTABLE_BASIS_UNION_TOO_LARGE"
    else:
        row["best_failure_mode"] = "ZSTABLE_COEFFICIENT_FULL_RANK"
    return row


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "template_family",
        "assignment_strategy",
        "assignment_seed",
        "support_vector",
        "pair7_counts",
        "max_pair_count",
        "selected_class_size_counts",
        "coordinate_classes_hash",
        "functional_classes",
        "functional_span_rank",
        "forced_functional_identities",
        "structural_status",
        "basis_profiles_tested",
        "coefficient_kernel_profiles",
        "stable_basis_union_profiles",
        "pair_projection_clear_profiles",
        "proxy_results_tested",
        "proxy_positive_profiles",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row[key] for key in keys}


def build_record(max_specs: int, max_basis_combinations: int, max_proxy_candidates: int) -> dict[str, Any]:
    previous = load_json(ZEXP_DATA)
    _profiles, raw_candidates = joint.build_candidates(max_specs=max_specs)
    cheap_rows = [
        analyze_candidate(candidate, max_basis_combinations=max_basis_combinations, run_proxy=False)
        for candidate in raw_candidates
    ]
    proxy_indices = [
        idx
        for idx, row in sorted(
            enumerate(cheap_rows),
            key=lambda item: (
                item[1]["pair_projection_clear_profiles"],
                item[1]["stable_basis_union_profiles"],
                item[1]["coefficient_kernel_profiles"],
                -(item[1]["best_profile"]["basis_zero_union_size"] if item[1]["best_profile"] else 10_000),
            ),
            reverse=True,
        )
        if row["pair_projection_clear_profiles"] > 0
    ][:max_proxy_candidates]
    rows = list(cheap_rows)
    proxy_index_set = set(proxy_indices)
    for idx in proxy_index_set:
        rows[idx] = analyze_candidate(
            raw_candidates[idx],
            max_basis_combinations=max_basis_combinations,
            run_proxy=True,
        )
    proxy_positive = [row for row in rows if row["proxy_positive_profiles"] > 0]
    proxy_ranked = [row for row in rows if row["proxy_results_tested"] > 0]
    pair_clear = [row for row in rows if row["pair_projection_clear_profiles"] > 0]
    stable_union = [row for row in rows if row["stable_basis_union_profiles"] > 0]
    coefficient_kernel = [row for row in rows if row["coefficient_kernel_profiles"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / ZSTABLE_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "ZSTABLE_PROXY_NULLITY_POSITIVE"
    elif proxy_ranked:
        best = min(proxy_ranked, key=lambda row: row["best_profile"]["proxy_result"]["proxy_rank"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZSTABLE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "ZSTABLE_PROXY_FULL_RANK"
    elif pair_clear:
        best = max(pair_clear, key=lambda row: row["pair_projection_clear_profiles"])
        proof_status = "CANDIDATE / ZSTABLE_PROXY_PENDING / PARTIAL / EXPERIMENTAL"
        failure = "ZSTABLE_PROXY_PENDING"
    elif stable_union:
        best = max(stable_union, key=lambda row: row["stable_basis_union_profiles"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZSTABLE_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL"
        failure = "ZSTABLE_FORCED_PAIR_EQUALITY"
    elif coefficient_kernel:
        best = min(coefficient_kernel, key=lambda row: row["best_profile"]["basis_zero_union_size"])
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZSTABLE_BASIS_UNION_TOO_LARGE / PARTIAL / EXPERIMENTAL"
        failure = "ZSTABLE_BASIS_UNION_TOO_LARGE"
    elif rows:
        best = max(rows, key=lambda row: (row["basis_profiles_tested"], row["functional_span_rank"]))
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZSTABLE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "ZSTABLE_COEFFICIENT_FULL_RANK"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / ZSTABLE_SUPPORT_FAIL / PARTIAL / EXPERIMENTAL"
        failure = "ZSTABLE_SUPPORT_FAIL"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_zlambda_audit": {
            "commit": SOURCE_COMMIT,
            "profiles_audited": previous["zlambda_expansion_audit"]["profiles_audited"],
            "stable_lift_targets": previous["zlambda_expansion_audit"]["stable_lift_targets"],
            "coefficient_kernel_profiles": previous["zlambda_expansion_audit"]["coefficient_kernel_profiles"],
            "best_basis_zero_union_size": previous["zlambda_expansion_audit"]["best_basis_zero_union_size"],
            "best_forced_pair_count": previous["zlambda_expansion_audit"]["best_forced_pair_count"],
            "best_failure_mode": previous["zlambda_expansion_audit"]["best_failure_mode"],
        },
        "zlambda_stable_generator": {
            "templates_tested": max_specs,
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "basis_profiles_tested": sum(row["basis_profiles_tested"] for row in rows),
            "coefficient_kernel_profiles": sum(row["coefficient_kernel_profiles"] for row in rows),
            "stable_basis_union_profiles": sum(row["stable_basis_union_profiles"] for row in rows),
            "pair_projection_clear_profiles": sum(row["pair_projection_clear_profiles"] for row in rows),
            "proxy_candidates_tested": len(proxy_ranked),
            "proxy_positive_candidates": len(proxy_positive),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_zero_union_size": None if best is None or best["best_profile"] is None else best["best_profile"]["basis_zero_union_size"],
            "best_stable_common_multiplier_dimension": None if best is None or best["best_profile"] is None else best["best_profile"]["stable_common_multiplier_dimension"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["best_forced_pair_count"],
            "best_proxy_rank": None if best is None or best["best_profile"] is None or best["best_profile"]["proxy_result"] is None else best["best_profile"]["proxy_result"]["proxy_rank"],
            "best_proxy_nullity": None if best is None or best["best_profile"] is None or best["best_profile"]["proxy_result"] is None else best["best_profile"]["proxy_result"]["proxy_nullity"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
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
    parser.add_argument("--max-specs", type=int, default=36)
    parser.add_argument("--max-basis-combinations", type=int, default=512)
    parser.add_argument("--max-proxy-candidates", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        max_specs=args.max_specs,
        max_basis_combinations=args.max_basis_combinations,
        max_proxy_candidates=args.max_proxy_candidates,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["zlambda_stable_generator"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_candidates": search["structural_pass_candidates"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "coefficient_kernel_profiles": search["coefficient_kernel_profiles"],
                    "stable_basis_union_profiles": search["stable_basis_union_profiles"],
                    "pair_projection_clear_profiles": search["pair_projection_clear_profiles"],
                    "proxy_candidates_tested": search["proxy_candidates_tested"],
                    "proxy_positive_candidates": search["proxy_positive_candidates"],
                    "best_template_id": search["best_template_id"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_basis_zero_union_size": search["best_basis_zero_union_size"],
                    "best_stable_common_multiplier_dimension": search["best_stable_common_multiplier_dimension"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
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
        print("M1_A327_ZLAMBDA_STABLE_RIGHT_KERNEL_GENERATOR_READY")


if __name__ == "__main__":
    main()
