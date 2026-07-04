#!/usr/bin/env python3
"""Exact row-collision search on the M1 a=327 ledger-codesign front."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "b74ba9e"
PREVIOUS_DATA = Path("experimental/data/m1_a327_ledger_codesign_rowdependency_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_ledger_codesign_exact_rowcollision_search.json")

ROOT = Path(__file__).resolve().parents[2]
ROWDEP_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_ledger_codesign_rowdependency_search.py"

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
    "global obstruction outside the tested ledger-codesign exact-rowcollision front",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rowdep = load_module("ledger_codesign_rowdependency_search", ROWDEP_SCRIPT)
lcodesign = rowdep.lcodesign
pfcoll = rowdep.pfcoll
lowrank = rowdep.lowrank
p456 = rowdep.p456
functional = pfcoll.feedback.zstable.functional


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize_projective(row: list[int]) -> tuple[int, ...]:
    values = [int(value) % P for value in row]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return tuple((entry * inv) % P for entry in values)
    return tuple(values)


def rank_rows(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> int:
    matrix = [[int(value) % P for value in row] for row in rows if any(int(value) % P for value in row)]
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % P:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, P)
        matrix[rank] = [(value * inv) % P for value in matrix[rank]]
        for row_idx in range(rank + 1, len(matrix)):
            if not matrix[row_idx][col] % P:
                continue
            factor = matrix[row_idx][col] % P
            matrix[row_idx] = [
                (matrix[row_idx][idx] - factor * matrix[rank][idx]) % P
                for idx in range(ncols)
            ]
        rank += 1
        if rank == ncols:
            break
    return rank


def profile_from_selected(classes: list[dict[str, Any]], selected: list[int], basis_id: str) -> dict[str, Any] | None:
    rows = [[int(value) % P for value in row["functional"]] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    if len(selected) != TEMPLATE_DIM:
        return None
    if rank_rows([rows[idx] for idx in selected]) != TEMPLATE_DIM:
        return None
    basis_rows = [rows[idx] for idx in selected]
    nonbasis_constraints = []
    nonbasis_rows = 0
    selected_set = set(selected)
    for idx, row in enumerate(rows):
        if idx in selected_set:
            continue
        coords = functional.solve_coordinates(row, basis_rows)
        if coords is None:
            return None
        nonbasis_rows += supports[idx]
        nonbasis_constraints.append(
            {
                "class_index": int(classes[idx]["class_index"]),
                "support_size": supports[idx],
                "basis_coordinates": [int(value) % P for value in coords],
            }
        )
    q_variable_count = sum(256 - supports[idx] for idx in selected)
    return {
        "basis_id": basis_id,
        "basis_class_indices": [int(classes[idx]["class_index"]) for idx in selected],
        "basis_functionals": [rows[idx] for idx in selected],
        "basis_support_sizes": [supports[idx] for idx in selected],
        "q_variable_count": q_variable_count,
        "nonbasis_constraints": len(nonbasis_constraints),
        "matrix_shape": [nonbasis_rows, q_variable_count],
        "formal_nullity_lower_bound": max(0, q_variable_count - nonbasis_rows),
        "nonbasis_constraint_detail": nonbasis_constraints,
    }


def extend_to_basis(classes: list[dict[str, Any]], avoid: set[int], preferred: list[int]) -> list[int] | None:
    rows = [[int(value) % P for value in row["functional"]] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    front = [idx for idx in preferred if idx not in avoid]
    rest = sorted(
        [idx for idx in range(len(classes)) if idx not in set(front) and idx not in avoid],
        key=lambda idx: (-supports[idx], normalize_projective(rows[idx]), int(classes[idx]["class_index"])),
    )
    tail = sorted(
        list(avoid),
        key=lambda idx: (-supports[idx], normalize_projective(rows[idx]), int(classes[idx]["class_index"])),
    )
    selected: list[int] = []
    selected_rows: list[list[int]] = []
    current_rank = 0
    for idx in front + rest + tail:
        if idx in selected:
            continue
        trial = selected_rows + [rows[idx]]
        trial_rank = rank_rows(trial)
        if trial_rank <= current_rank:
            continue
        selected.append(idx)
        selected_rows.append(rows[idx])
        current_rank = trial_rank
        if current_rank == TEMPLATE_DIM:
            return selected
    return None


def candidate_collision_groups(classes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_coordinate: dict[tuple[int, ...], list[int]] = defaultdict(list)
    by_support: dict[str, list[int]] = defaultdict(list)
    by_support_coordinate: dict[tuple[str, tuple[int, ...]], list[int]] = defaultdict(list)
    for idx, row in enumerate(classes):
        coord = normalize_projective([int(value) for value in row["functional"]])
        support_hash = row["positions_hash"]
        by_coordinate[coord].append(idx)
        by_support[support_hash].append(idx)
        by_support_coordinate[(support_hash, coord)].append(idx)

    out = []
    for group_type, groups in [
        ("support_coordinate", by_support_coordinate),
        ("coordinate", by_coordinate),
        ("support", by_support),
    ]:
        for key, indices in groups.items():
            if len(indices) < 2:
                continue
            out.append(
                {
                    "group_type": group_type,
                    "group_key": json.dumps(key, sort_keys=True),
                    "class_offsets": indices,
                    "class_indices": [int(classes[idx]["class_index"]) for idx in indices],
                    "group_size": len(indices),
                    "support_sizes": [int(classes[idx]["support_size"]) for idx in indices],
                }
            )
    return sorted(
        out,
        key=lambda row: (
            {"support_coordinate": 0, "coordinate": 1, "support": 2}[row["group_type"]],
            -int(row["group_size"]),
            [-int(value) for value in row["support_sizes"]],
            row["class_indices"],
        ),
    )


def collision_metrics(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    metrics = rowdep.dependency_metrics(candidate, profile)
    exact_coordinate_pairs = int(metrics["repeated_coordinate_pairs"])
    exact_support_pairs = int(metrics["repeated_support_pairs"])
    exact_support_coordinate_pairs = int(metrics["repeated_support_coordinate_pairs"])
    exact_collision_positive = (
        exact_coordinate_pairs > 0
        or exact_support_pairs > 0
        or exact_support_coordinate_pairs > 0
    )
    exact_collision_score = (
        500 * exact_support_coordinate_pairs
        + 200 * exact_coordinate_pairs
        + 120 * exact_support_pairs
        + int(profile["q_variable_count"])
        - 2 * (int(profile["matrix_shape"][0]) - int(profile["q_variable_count"]))
    )
    return {
        **metrics,
        "exact_collision_positive": exact_collision_positive,
        "exact_collision_score": exact_collision_score,
    }


def profile_row(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    candidate_order: int,
    profile_order: int,
    profile_kind: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row = lcodesign.profile_row(candidate, profile, candidate_order, profile_order)
    row.update(collision_metrics(candidate, profile))
    row["profile_kind"] = profile_kind
    row["q_variable_floor"] = Q_VARIABLE_FLOOR
    row["q_variable_budget_ok"] = int(row["q_variable_count"]) >= Q_VARIABLE_FLOOR
    if extra:
        row.update(extra)
    return row


def exact_collision_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    q_shortfall = max(0, Q_VARIABLE_FLOOR - int(row["q_variable_count"]))
    return (
        not bool(row["exact_collision_positive"]),
        q_shortfall,
        -int(row["repeated_support_coordinate_pairs"]),
        -int(row["repeated_coordinate_pairs"]),
        -int(row["repeated_support_pairs"]),
        -int(row["exact_collision_score"]),
        -int(row["q_variable_count"]),
        int(row["row_surplus"]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        not bool(row["exact_collision_positive"]),
        -int(row["repeated_support_coordinate_pairs"]),
        -int(row["repeated_coordinate_pairs"]),
        -int(row["repeated_support_pairs"]),
        -int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def build_forced_profiles(
    candidate: dict[str, Any],
    candidate_order: int,
    max_groups_per_candidate: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    classes = pfcoll.feedback.zstable.functional.functional_classes(candidate)
    groups = candidate_collision_groups(classes)
    rows = [[int(value) % P for value in row["functional"]] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    preferred = sorted(
        range(len(classes)),
        key=lambda idx: (-supports[idx], normalize_projective(rows[idx]), int(classes[idx]["class_index"])),
    )
    out: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen: set[tuple[int, ...]] = set()
    for group_order, group in enumerate(groups[:max_groups_per_candidate]):
        avoid = set(int(idx) for idx in group["class_offsets"])
        selected = extend_to_basis(classes, avoid=avoid, preferred=preferred)
        if selected is None:
            continue
        nonbasis_count = sum(1 for idx in group["class_offsets"] if idx not in set(selected))
        if nonbasis_count < 2:
            continue
        basis_id = (
            f"exactrow_{group['group_type']}_{group_order}_"
            f"{'_'.join(str(classes[idx]['class_index']) for idx in selected)}"
        )
        profile = profile_from_selected(classes, selected, basis_id)
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        out.append(
            (
                profile,
                {
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


def build_record(
    max_templates: int,
    max_systems: int,
    profile_candidate_limit: int,
    natural_basis_profiles_per_candidate: int,
    natural_random_bases: int,
    forced_groups_per_candidate: int,
    profile_rank_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    front = rowdep.build_front(max_templates=max_templates, max_systems=max_systems)
    ordered_front = sorted(front, key=lambda item: lcodesign.structural_sort_key(item[1]))[:profile_candidate_limit]

    profile_rows: list[dict[str, Any]] = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    candidate_collision_counter: Counter[str] = Counter()
    candidates_with_collision_groups = 0
    forced_profiles_constructed = 0

    for candidate_order, (candidate, structural) in enumerate(ordered_front):
        classes = pfcoll.feedback.zstable.functional.functional_classes(candidate)
        groups = candidate_collision_groups(classes)
        if groups:
            candidates_with_collision_groups += 1
            candidate_collision_counter.update(item["group_type"] for item in groups)

        natural_profiles = p456.tchamber.basis_profiles(
            candidate,
            top_classes=48,
            random_bases=natural_random_bases,
            limit=natural_basis_profiles_per_candidate,
        )
        for profile_order, profile in enumerate(natural_profiles):
            row = profile_row(candidate, profile, candidate_order, profile_order, "natural")
            row["source_system_order"] = structural["system_order"]
            profile_rows.append(row)
            source_profiles[(candidate_order, row["basis_id"])] = (candidate, profile)

        forced = build_forced_profiles(candidate, candidate_order, forced_groups_per_candidate)
        for forced_order, (profile, meta) in enumerate(forced):
            forced_profiles_constructed += 1
            row = profile_row(
                candidate,
                profile,
                candidate_order,
                natural_basis_profiles_per_candidate + forced_order,
                "forced",
                meta,
            )
            row["source_system_order"] = structural["system_order"]
            profile_rows.append(row)
            source_profiles[(candidate_order, row["basis_id"])] = (candidate, profile)

    exact_collision_q_budget_profiles = [
        row for row in profile_rows
        if row["exact_collision_positive"] and int(row["q_variable_count"]) >= Q_VARIABLE_FLOOR
    ]
    rank_targets = sorted(exact_collision_q_budget_profiles, key=exact_collision_sort_key)[:profile_rank_limit]

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
                    "EXACT_ROWCOLLISION_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "EXACT_ROWCOLLISION_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    exact_positive = [row for row in profile_rows if row["exact_collision_positive"]]
    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    best_exact_collision = min(exact_positive, key=exact_collision_sort_key) if exact_positive else None
    best_collision_q_budget = (
        min(exact_collision_q_budget_profiles, key=exact_collision_sort_key)
        if exact_collision_q_budget_profiles
        else None
    )
    best_any = min(profile_rows, key=exact_collision_sort_key) if profile_rows else None
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

    failure = "EXACT_ROWCOLLISION_NOT_FOUND"
    proof_status = "EXACT_EXTRACTION_NO_A327 / EXACT_ROWCOLLISION_NOT_FOUND / PARTIAL / EXPERIMENTAL"
    if exact_positive and not exact_collision_q_budget_profiles:
        failure = "EXACT_ROWCOLLISION_Q_BUDGET_FAIL"
        proof_status = "EXACT_EXTRACTION_NO_A327 / EXACT_ROWCOLLISION_Q_BUDGET_FAIL / PARTIAL / EXPERIMENTAL"
    elif proxy_rows:
        failure = "EXACT_ROWCOLLISION_PROXY_POSITIVE" if positives else "EXACT_ROWCOLLISION_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / EXACT_ROWCOLLISION_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / EXACT_ROWCOLLISION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    q_budget = [row for row in profile_rows if int(row["q_variable_count"]) >= Q_VARIABLE_FLOOR]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_rowdependency_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "structural_pass_systems": previous["rowdependency_search"]["structural_pass_systems"],
            "basis_profiles_constructed": previous["rowdependency_search"]["basis_profiles_constructed"],
            "dependency_q_budget_profiles": previous["rowdependency_search"]["dependency_q_budget_profiles"],
            "proxy_ranked_profiles": previous["rowdependency_search"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["rowdependency_search"]["proxy_positive_profiles"],
            "best_proxy_rank": previous["rowdependency_search"]["best_proxy_rank"],
            "best_proxy_nullity": previous["rowdependency_search"]["best_proxy_nullity"],
            "failure_mode": previous["rowdependency_search"]["best_failure_mode"],
        },
        "exact_rowcollision_search": {
            "proxy_prime": PROXY_PRIME,
            "q_variable_floor": Q_VARIABLE_FLOOR,
            "max_templates": max_templates,
            "max_systems": max_systems,
            "profile_candidate_limit": profile_candidate_limit,
            "natural_basis_profiles_per_candidate": natural_basis_profiles_per_candidate,
            "natural_random_bases": natural_random_bases,
            "forced_groups_per_candidate": forced_groups_per_candidate,
            "profile_rank_limit": profile_rank_limit,
            "structural_pass_systems": len(front),
            "candidates_scanned": len(ordered_front),
            "candidates_with_collision_groups": candidates_with_collision_groups,
            "candidate_collision_group_counts": dict(candidate_collision_counter),
            "basis_profiles_constructed": len(profile_rows),
            "natural_profiles_constructed": sum(1 for row in profile_rows if row["profile_kind"] == "natural"),
            "forced_profiles_constructed": forced_profiles_constructed,
            "q_budget_profiles": len(q_budget),
            "exact_collision_profiles": len(exact_positive),
            "exact_collision_q_budget_profiles": len(exact_collision_q_budget_profiles),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_exact_collision_score": (
                None if best_exact_collision is None else best_exact_collision["exact_collision_score"]
            ),
            "best_exact_collision_q_variable_count": (
                None if best_exact_collision is None else best_exact_collision["q_variable_count"]
            ),
            "best_q_budget_collision_score": (
                None if best_collision_q_budget is None else best_collision_q_budget["exact_collision_score"]
            ),
            "best_q_budget_collision_q_variable_count": (
                None if best_collision_q_budget is None else best_collision_q_budget["q_variable_count"]
            ),
            "best_any_q_variable_count": None if best_any is None else best_any["q_variable_count"],
            "best_any_repeated_coordinate_pairs": None if best_any is None else best_any["repeated_coordinate_pairs"],
            "best_any_repeated_support_pairs": None if best_any is None else best_any["repeated_support_pairs"],
            "best_any_repeated_support_coordinate_pairs": (
                None if best_any is None else best_any["repeated_support_coordinate_pairs"]
            ),
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_exact_collision_profile": best_exact_collision,
        "best_collision_q_budget_profile": best_collision_q_budget,
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
    parser.add_argument("--natural-basis-profiles-per-candidate", type=int, default=8)
    parser.add_argument("--natural-random-bases", type=int, default=512)
    parser.add_argument("--forced-groups-per-candidate", type=int, default=8)
    parser.add_argument("--profile-rank-limit", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_systems=args.max_systems,
        profile_candidate_limit=args.profile_candidate_limit,
        natural_basis_profiles_per_candidate=args.natural_basis_profiles_per_candidate,
        natural_random_bases=args.natural_random_bases,
        forced_groups_per_candidate=args.forced_groups_per_candidate,
        profile_rank_limit=args.profile_rank_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["exact_rowcollision_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "structural_pass_systems": search["structural_pass_systems"],
                    "candidates_scanned": search["candidates_scanned"],
                    "candidates_with_collision_groups": search["candidates_with_collision_groups"],
                    "basis_profiles_constructed": search["basis_profiles_constructed"],
                    "forced_profiles_constructed": search["forced_profiles_constructed"],
                    "q_budget_profiles": search["q_budget_profiles"],
                    "exact_collision_profiles": search["exact_collision_profiles"],
                    "exact_collision_q_budget_profiles": search["exact_collision_q_budget_profiles"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_q_variable_count": search["best_q_variable_count"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LEDGER_CODESIGN_EXACT_ROWCOLLISION_SEARCH_READY")


if __name__ == "__main__":
    main()
