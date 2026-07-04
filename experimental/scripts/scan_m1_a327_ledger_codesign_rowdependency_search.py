#!/usr/bin/env python3
"""Row-dependency search on the M1 a=327 ledger-codesign front."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "af2492f"
PREVIOUS_DATA = Path("experimental/data/m1_a327_prescribed_functional_collision_ledger_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_ledger_codesign_rowdependency_search.json")

ROOT = Path(__file__).resolve().parents[2]
LCODESIGN_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_functional_collision_ledger_codesign.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
Q_VARIABLE_FLOOR = 350

REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested ledger-codesign rowdependency front",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lcodesign = load_module("prescribed_functional_collision_ledger_codesign", LCODESIGN_SCRIPT)
pfcoll = lcodesign.pfcoll
lowrank = lcodesign.lowrank
p456 = lcodesign.p456


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def positions_for_class(classes_by_index: dict[int, dict[str, Any]], class_index: int) -> set[int]:
    return {int(pos) for pos in classes_by_index[int(class_index)]["positions"]}


def dependency_metrics(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    classes = pfcoll.feedback.zstable.functional.functional_classes(candidate)
    classes_by_index = {int(row["class_index"]): row for row in classes}

    coord_groups: Counter[tuple[int, ...]] = Counter()
    support_groups: Counter[str] = Counter()
    support_coord_groups: Counter[tuple[tuple[int, ...], str]] = Counter()
    support_sets: list[set[int]] = []

    for row in profile["nonbasis_constraint_detail"]:
        class_index = int(row["class_index"])
        coords = tuple(int(value) % 17 for value in row["basis_coordinates"])
        support_hash = classes_by_index[class_index]["positions_hash"]
        coord_groups[coords] += 1
        support_groups[support_hash] += 1
        support_coord_groups[(coords, support_hash)] += 1
        support_sets.append(positions_for_class(classes_by_index, class_index))

    repeated_coordinate_groups = sum(1 for value in coord_groups.values() if value > 1)
    repeated_coordinate_pairs = sum(value * (value - 1) // 2 for value in coord_groups.values() if value > 1)
    repeated_support_groups = sum(1 for value in support_groups.values() if value > 1)
    repeated_support_pairs = sum(value * (value - 1) // 2 for value in support_groups.values() if value > 1)
    repeated_support_coordinate_groups = sum(1 for value in support_coord_groups.values() if value > 1)
    repeated_support_coordinate_pairs = sum(
        value * (value - 1) // 2 for value in support_coord_groups.values() if value > 1
    )

    nested_support_pairs = 0
    support_overlap_total = 0
    support_overlap_nonzero_pairs = 0
    for left in range(len(support_sets)):
        for right in range(left + 1, len(support_sets)):
            a = support_sets[left]
            b = support_sets[right]
            overlap = len(a & b)
            support_overlap_total += overlap
            if overlap:
                support_overlap_nonzero_pairs += 1
            if a and b and (a <= b or b <= a):
                nested_support_pairs += 1

    row_surplus = int(profile["matrix_shape"][0]) - int(profile["q_variable_count"])
    score = (
        200 * repeated_support_coordinate_pairs
        + 80 * repeated_coordinate_pairs
        + 40 * repeated_support_pairs
        + 12 * nested_support_pairs
        + support_overlap_total
        + 2 * int(profile["q_variable_count"])
        - 3 * row_surplus
    )
    dependency_positive = (
        repeated_support_coordinate_pairs > 0
        or repeated_coordinate_pairs > 0
        or repeated_support_pairs > 0
        or nested_support_pairs > 0
        or support_overlap_total > 0
    )
    return {
        "dependency_positive": dependency_positive,
        "dependency_score": score,
        "repeated_coordinate_groups": repeated_coordinate_groups,
        "repeated_coordinate_pairs": repeated_coordinate_pairs,
        "repeated_support_groups": repeated_support_groups,
        "repeated_support_pairs": repeated_support_pairs,
        "repeated_support_coordinate_groups": repeated_support_coordinate_groups,
        "repeated_support_coordinate_pairs": repeated_support_coordinate_pairs,
        "nested_support_pairs": nested_support_pairs,
        "support_overlap_total": support_overlap_total,
        "support_overlap_nonzero_pairs": support_overlap_nonzero_pairs,
        "row_surplus": row_surplus,
    }


def profile_row(candidate: dict[str, Any], profile: dict[str, Any], candidate_order: int, profile_order: int) -> dict[str, Any]:
    row = lcodesign.profile_row(candidate, profile, candidate_order, profile_order)
    metrics = dependency_metrics(candidate, profile)
    row.update(metrics)
    row["q_variable_floor"] = Q_VARIABLE_FLOOR
    row["q_variable_budget_ok"] = int(row["q_variable_count"]) >= Q_VARIABLE_FLOOR
    return row


def profile_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    q_shortfall = max(0, Q_VARIABLE_FLOOR - int(row["q_variable_count"]))
    return (
        not bool(row["dependency_positive"]),
        q_shortfall,
        -int(row["dependency_score"]),
        -int(row["q_variable_count"]),
        int(row["row_surplus"]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        not bool(row["dependency_positive"]),
        max(0, Q_VARIABLE_FLOOR - int(row["q_variable_count"])),
        -int(row["dependency_score"]),
        -int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def build_front(max_templates: int, max_systems: int) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    specs = lcodesign.actual_template_specs(max_templates)
    solved_profiles = []
    for spec in specs:
        solved = lowrank.solve_template_counts(spec)
        if solved.get("solver_status") == "OPTIMAL_OR_FEASIBLE":
            solved["source_template_spec"] = spec["source_template_spec"]
            solved["pairdiff_collision_excess"] = spec["pairdiff_collision_excess"]
            solved["pairdiff_collision_groups"] = spec["pairdiff_collision_groups"]
            solved_profiles.append(solved)

    out: list[tuple[dict[str, Any], dict[str, Any]]] = []
    system_order = 0
    for profile_order, profile in enumerate(solved_profiles):
        for strategy_order, strategy in enumerate(profile["assignment_strategies"]):
            if system_order >= max_systems:
                return out
            candidate = lcodesign.evaluate_codesign_candidate(
                profile,
                strategy,
                seed=88100 + 43 * profile_order + strategy_order,
            )
            row = lcodesign.structural_row(candidate, profile, system_order)
            if row["structural_status"] == "TCHAMBER_STRUCTURAL_PASS":
                out.append((candidate, row))
            system_order += 1
    return out


def build_record(
    max_templates: int,
    max_systems: int,
    profile_candidate_limit: int,
    basis_profiles_per_candidate: int,
    profile_rank_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    front = build_front(max_templates=max_templates, max_systems=max_systems)
    structural_rows = [row for _candidate, row in front]
    ordered_front = sorted(front, key=lambda item: lcodesign.structural_sort_key(item[1]))[:profile_candidate_limit]

    profile_rows = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    for candidate_order, (candidate, structural) in enumerate(ordered_front):
        for profile_order, profile in enumerate(
            p456.tchamber.basis_profiles(
                candidate,
                top_classes=32,
                random_bases=192,
                limit=basis_profiles_per_candidate,
            )
        ):
            row = profile_row(candidate, profile, candidate_order, profile_order)
            row["source_system_order"] = structural["system_order"]
            profile_rows.append(row)
            source_profiles[(candidate_order, row["basis_id"])] = (candidate, profile)

    dependency_profiles = [
        row for row in profile_rows
        if row["dependency_positive"] and int(row["q_variable_count"]) >= Q_VARIABLE_FLOOR
    ]
    rank_targets = sorted(dependency_profiles, key=profile_sort_key)[:profile_rank_limit]

    h_values = pfcoll.feedback.proxy_h_values(PROXY_PRIME)
    powers = pfcoll.feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    proxy_rows = []
    for target in rank_targets:
        candidate, profile = source_profiles[(int(target["candidate_order"]), target["basis_id"])]
        proxy = pfcoll.feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
        proxy_rows.append(
            {
                **target,
                "proxy_prime": proxy["proxy_prime"],
                "proxy_matrix_shape": proxy["matrix_shape"],
                "proxy_rank": proxy["proxy_rank"],
                "proxy_nullity": proxy["proxy_nullity"],
                "best_failure_mode": (
                    "ROWDEP_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "ROWDEP_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    best_candidate = None
    if best is not None:
        candidate, _profile = source_profiles[(int(best["candidate_order"]), best["basis_id"])]
        best_candidate = {
            **pfcoll.feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
            "template_vectors": candidate["template_vectors"],
            "selected_count_hash": candidate["selected_count_hash"],
            "selected_class_size_counts": candidate["selected_class_size_counts"],
            "total_effective_cost": candidate["total_effective_cost"],
        }

    failure = "ROWDEP_NO_DEPENDENCY_Q_BUDGET_PROFILE"
    proof_status = "EXACT_EXTRACTION_NO_A327 / ROWDEP_NO_DEPENDENCY_Q_BUDGET_PROFILE / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "ROWDEP_PROXY_POSITIVE" if positives else "ROWDEP_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / ROWDEP_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / ROWDEP_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    best_dependency = max(profile_rows, key=lambda row: int(row["dependency_score"])) if profile_rows else None
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_ledger_codesign": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "systems_tested": previous["prescribed_functional_collision_ledger_codesign"]["systems_tested"],
            "q_budget_profiles": previous["prescribed_functional_collision_ledger_codesign"]["q_budget_profiles"],
            "best_q_variable_count": previous["prescribed_functional_collision_ledger_codesign"]["best_q_variable_count"],
            "best_proxy_rank": previous["prescribed_functional_collision_ledger_codesign"]["best_proxy_rank"],
            "best_proxy_nullity": previous["prescribed_functional_collision_ledger_codesign"]["best_proxy_nullity"],
            "failure_mode": previous["prescribed_functional_collision_ledger_codesign"]["best_failure_mode"],
        },
        "rowdependency_search": {
            "proxy_prime": PROXY_PRIME,
            "q_variable_floor": Q_VARIABLE_FLOOR,
            "max_templates": max_templates,
            "max_systems": max_systems,
            "profile_candidate_limit": profile_candidate_limit,
            "basis_profiles_per_candidate": basis_profiles_per_candidate,
            "profile_rank_limit": profile_rank_limit,
            "structural_pass_systems": len(front),
            "basis_profiles_constructed": len(profile_rows),
            "dependency_positive_profiles": sum(1 for row in profile_rows if row["dependency_positive"]),
            "dependency_q_budget_profiles": len(dependency_profiles),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_dependency_score": None if best_dependency is None else best_dependency["dependency_score"],
            "best_dependency_q_variable_count": None if best_dependency is None else best_dependency["q_variable_count"],
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_dependency_profile": best_dependency,
        "best_profile": best,
        "best_candidate": best_candidate,
        "proxy_ranked_profiles": sorted(proxy_rows, key=proxy_sort_key),
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": REQUIRED_NONCLAIMS,
    }


REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested ledger-codesign rowdependency front",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-templates", type=int, default=96)
    parser.add_argument("--max-systems", type=int, default=240)
    parser.add_argument("--profile-candidate-limit", type=int, default=40)
    parser.add_argument("--basis-profiles-per-candidate", type=int, default=4)
    parser.add_argument("--profile-rank-limit", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_systems=args.max_systems,
        profile_candidate_limit=args.profile_candidate_limit,
        basis_profiles_per_candidate=args.basis_profiles_per_candidate,
        profile_rank_limit=args.profile_rank_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["rowdependency_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "structural_pass_systems": search["structural_pass_systems"],
                    "basis_profiles_constructed": search["basis_profiles_constructed"],
                    "dependency_positive_profiles": search["dependency_positive_profiles"],
                    "dependency_q_budget_profiles": search["dependency_q_budget_profiles"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_dependency_score": search["best_dependency_score"],
                    "best_q_variable_count": search["best_q_variable_count"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_template_id": None if record["best_profile"] is None else record["best_profile"]["template_id"],
                    "best_basis_id": None if record["best_profile"] is None else record["best_profile"]["basis_id"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LEDGER_CODESIGN_ROWDEPENDENCY_SEARCH_READY")


if __name__ == "__main__":
    main()
