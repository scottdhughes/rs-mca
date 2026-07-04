#!/usr/bin/env python3
"""Codesign exact support collisions with q-budget on the M1 a=327 ledger front."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "2939690"
PREVIOUS_DATA = Path("experimental/data/m1_a327_ledger_codesign_exact_rowcollision_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_ledger_codesign_collision_budget_codesign.json")

ROOT = Path(__file__).resolve().parents[2]
EXACT_ROWCOLLISION_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_ledger_codesign_exact_rowcollision_search.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
P = 17
TEMPLATE_DIM = 6
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
    "global obstruction outside the tested ledger-codesign collision-budget front",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


exactrow = load_module("ledger_codesign_exact_rowcollision_search", EXACT_ROWCOLLISION_SCRIPT)
rowdep = exactrow.rowdep
lcodesign = exactrow.lcodesign
pfcoll = exactrow.pfcoll


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def hamming(row: list[int]) -> int:
    return sum(1 for value in row if int(value) % P)


def preference_order(classes: list[dict[str, Any]], group: dict[str, Any], preference: str) -> list[int]:
    rows = [[int(value) % P for value in row["functional"]] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    avoid = set(int(idx) for idx in group["class_offsets"])
    base = [idx for idx in range(len(classes)) if idx not in avoid]
    support_hashes = {idx: classes[idx]["positions_hash"] for idx in range(len(classes))}
    group_support_hashes = {support_hashes[idx] for idx in avoid}

    if preference == "low_support_basis":
        return sorted(base, key=lambda idx: (supports[idx], -hamming(rows[idx]), exactrow.normalize_projective(rows[idx])))
    if preference == "low_support_not_group_support":
        return sorted(
            base,
            key=lambda idx: (
                support_hashes[idx] in group_support_hashes,
                supports[idx],
                -hamming(rows[idx]),
                exactrow.normalize_projective(rows[idx]),
            ),
        )
    if preference == "mid_support_rank":
        return sorted(base, key=lambda idx: (abs(supports[idx] - 128), supports[idx], -hamming(rows[idx])))
    if preference == "q_budget_then_span":
        return sorted(base, key=lambda idx: (supports[idx], exactrow.normalize_projective(rows[idx]), int(classes[idx]["class_index"])))
    raise ValueError(f"unknown preference {preference}")


def extend_to_basis_ordered(classes: list[dict[str, Any]], avoid: set[int], order: list[int]) -> list[int] | None:
    rows = [[int(value) % P for value in row["functional"]] for row in classes]
    selected: list[int] = []
    selected_rows: list[list[int]] = []
    current_rank = 0
    tail = [idx for idx in range(len(classes)) if idx not in set(order)]
    for idx in order + tail:
        if idx in selected:
            continue
        trial = selected_rows + [rows[idx]]
        trial_rank = exactrow.rank_rows(trial)
        if trial_rank <= current_rank:
            continue
        selected.append(idx)
        selected_rows.append(rows[idx])
        current_rank = trial_rank
        if current_rank == TEMPLATE_DIM:
            return selected
    return None


def collision_budget_profiles(
    candidate: dict[str, Any],
    candidate_order: int,
    groups_per_candidate: int,
    preferences: list[str],
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    classes = pfcoll.feedback.zstable.functional.functional_classes(candidate)
    groups = exactrow.candidate_collision_groups(classes)
    out: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen: set[tuple[str, tuple[int, ...]]] = set()
    for group_order, group in enumerate(groups[:groups_per_candidate]):
        avoid = set(int(idx) for idx in group["class_offsets"])
        for preference in preferences:
            order = preference_order(classes, group, preference)
            selected = extend_to_basis_ordered(classes, avoid=avoid, order=order)
            if selected is None:
                continue
            nonbasis_count = sum(1 for idx in group["class_offsets"] if idx not in set(selected))
            if nonbasis_count < 2:
                continue
            key = (preference, tuple(selected))
            if key in seen:
                continue
            seen.add(key)
            basis_id = (
                f"collbudget_{preference}_{group['group_type']}_{group_order}_"
                f"{'_'.join(str(classes[idx]['class_index']) for idx in selected)}"
            )
            profile = exactrow.profile_from_selected(classes, selected, basis_id)
            if profile is None:
                continue
            out.append(
                (
                    profile,
                    {
                        "codesign_preference": preference,
                        "forced_group_order": group_order,
                        "forced_group_type": group["group_type"],
                        "forced_group_size": group["group_size"],
                        "forced_group_nonbasis_count": nonbasis_count,
                        "forced_group_class_indices": group["class_indices"],
                        "candidate_collision_groups": len(groups),
                        "candidate_support_coordinate_groups": sum(
                            1 for item in groups if item["group_type"] == "support_coordinate"
                        ),
                        "candidate_coordinate_groups": sum(1 for item in groups if item["group_type"] == "coordinate"),
                        "candidate_support_groups": sum(1 for item in groups if item["group_type"] == "support"),
                    },
                )
            )
    return out


def profile_row(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    candidate_order: int,
    profile_order: int,
    extra: dict[str, Any],
) -> dict[str, Any]:
    row = exactrow.profile_row(candidate, profile, candidate_order, profile_order, "collision_budget", extra)
    row["collision_budget_success"] = bool(row["exact_collision_positive"] and row["q_variable_budget_ok"])
    row["collision_budget_score"] = (
        1000 * int(row["collision_budget_success"])
        + 150 * int(row["repeated_support_coordinate_pairs"])
        + 80 * int(row["repeated_support_pairs"])
        + 80 * int(row["repeated_coordinate_pairs"])
        + int(row["q_variable_count"])
        - max(0, Q_VARIABLE_FLOOR - int(row["q_variable_count"])) * 3
    )
    return row


def collision_budget_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        not bool(row["collision_budget_success"]),
        -int(row["repeated_support_coordinate_pairs"]),
        -int(row["repeated_support_pairs"]),
        -int(row["repeated_coordinate_pairs"]),
        -int(row["q_variable_count"]),
        -int(row["collision_budget_score"]),
        int(row["row_surplus"]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        not bool(row["collision_budget_success"]),
        -int(row["repeated_support_coordinate_pairs"]),
        -int(row["repeated_support_pairs"]),
        -int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def build_record(
    max_templates: int,
    max_systems: int,
    profile_candidate_limit: int,
    groups_per_candidate: int,
    profile_rank_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    front = rowdep.build_front(max_templates=max_templates, max_systems=max_systems)
    ordered_front = sorted(front, key=lambda item: lcodesign.structural_sort_key(item[1]))[:profile_candidate_limit]
    preferences = [
        "low_support_basis",
        "low_support_not_group_support",
        "mid_support_rank",
        "q_budget_then_span",
    ]

    profile_rows: list[dict[str, Any]] = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    candidate_collision_counter: Counter[str] = Counter()
    candidates_with_collision_groups = 0
    for candidate_order, (candidate, structural) in enumerate(ordered_front):
        classes = pfcoll.feedback.zstable.functional.functional_classes(candidate)
        groups = exactrow.candidate_collision_groups(classes)
        if groups:
            candidates_with_collision_groups += 1
            candidate_collision_counter.update(item["group_type"] for item in groups)
        for profile_order, (profile, meta) in enumerate(
            collision_budget_profiles(candidate, candidate_order, groups_per_candidate, preferences)
        ):
            row = profile_row(candidate, profile, candidate_order, profile_order, meta)
            row["source_system_order"] = structural["system_order"]
            profile_rows.append(row)
            source_profiles[(candidate_order, row["basis_id"])] = (candidate, profile)

    successes = [row for row in profile_rows if row["collision_budget_success"]]
    targets = sorted(successes, key=collision_budget_sort_key)[:profile_rank_limit]

    h_values = pfcoll.feedback.proxy_h_values(PROXY_PRIME)
    powers = pfcoll.feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    proxy_rows = []
    for target in targets:
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
                    "CBUDGET_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "CBUDGET_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    q_budget_profiles = [row for row in profile_rows if int(row["q_variable_count"]) >= Q_VARIABLE_FLOOR]
    collision_profiles = [row for row in profile_rows if row["exact_collision_positive"]]
    best_success = min(successes, key=collision_budget_sort_key) if successes else None
    best_any = min(profile_rows, key=collision_budget_sort_key) if profile_rows else None
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

    failure = "CBUDGET_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / CBUDGET_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if successes and proxy_rows:
        failure = "CBUDGET_PROXY_POSITIVE" if positives else "CBUDGET_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / CBUDGET_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / CBUDGET_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )
    elif successes:
        failure = "CBUDGET_PROXY_NOT_RUN"
        proof_status = "CANDIDATE / CBUDGET_PROXY_NOT_RUN / PARTIAL / EXPERIMENTAL"
    elif collision_profiles and q_budget_profiles:
        failure = "CBUDGET_COLLISION_BUDGET_NOT_COINCIDENT"
        proof_status = "EXACT_EXTRACTION_NO_A327 / CBUDGET_COLLISION_BUDGET_NOT_COINCIDENT / PARTIAL / EXPERIMENTAL"
    elif collision_profiles:
        failure = "CBUDGET_Q_BUDGET_FAIL"
        proof_status = "EXACT_EXTRACTION_NO_A327 / CBUDGET_Q_BUDGET_FAIL / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_exact_rowcollision_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "structural_pass_systems": previous["exact_rowcollision_search"]["structural_pass_systems"],
            "basis_profiles_constructed": previous["exact_rowcollision_search"]["basis_profiles_constructed"],
            "exact_collision_profiles": previous["exact_rowcollision_search"]["exact_collision_profiles"],
            "exact_collision_q_budget_profiles": previous["exact_rowcollision_search"]["exact_collision_q_budget_profiles"],
            "best_exact_collision_q_variable_count": previous["exact_rowcollision_search"]["best_exact_collision_q_variable_count"],
            "failure_mode": previous["exact_rowcollision_search"]["best_failure_mode"],
        },
        "collision_budget_codesign": {
            "proxy_prime": PROXY_PRIME,
            "q_variable_floor": Q_VARIABLE_FLOOR,
            "max_templates": max_templates,
            "max_systems": max_systems,
            "profile_candidate_limit": profile_candidate_limit,
            "groups_per_candidate": groups_per_candidate,
            "preferences": preferences,
            "profile_rank_limit": profile_rank_limit,
            "structural_pass_systems": len(front),
            "candidates_scanned": len(ordered_front),
            "candidates_with_collision_groups": candidates_with_collision_groups,
            "candidate_collision_group_counts": dict(candidate_collision_counter),
            "basis_profiles_constructed": len(profile_rows),
            "exact_collision_profiles": len(collision_profiles),
            "q_budget_profiles": len(q_budget_profiles),
            "collision_budget_profiles": len(successes),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_success_q_variable_count": None if best_success is None else best_success["q_variable_count"],
            "best_success_repeated_support_pairs": None if best_success is None else best_success["repeated_support_pairs"],
            "best_any_q_variable_count": None if best_any is None else best_any["q_variable_count"],
            "best_any_repeated_support_pairs": None if best_any is None else best_any["repeated_support_pairs"],
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_success_profile": best_success,
        "best_profile": best,
        "best_any_profile": best_any,
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-templates", type=int, default=128)
    parser.add_argument("--max-systems", type=int, default=360)
    parser.add_argument("--profile-candidate-limit", type=int, default=60)
    parser.add_argument("--groups-per-candidate", type=int, default=8)
    parser.add_argument("--profile-rank-limit", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_systems=args.max_systems,
        profile_candidate_limit=args.profile_candidate_limit,
        groups_per_candidate=args.groups_per_candidate,
        profile_rank_limit=args.profile_rank_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["collision_budget_codesign"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "structural_pass_systems": search["structural_pass_systems"],
                    "candidates_scanned": search["candidates_scanned"],
                    "basis_profiles_constructed": search["basis_profiles_constructed"],
                    "exact_collision_profiles": search["exact_collision_profiles"],
                    "q_budget_profiles": search["q_budget_profiles"],
                    "collision_budget_profiles": search["collision_budget_profiles"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_success_q_variable_count": search["best_success_q_variable_count"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LEDGER_CODESIGN_COLLISION_BUDGET_CODESIGN_READY")


if __name__ == "__main__":
    main()
