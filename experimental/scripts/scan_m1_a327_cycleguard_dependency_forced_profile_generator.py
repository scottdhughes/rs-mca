#!/usr/bin/env python3
"""Generate dependency-forced pre-chamber profiles for M1 a=327 cycleguard search."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "db1182b"
PREVIOUS_DATA = Path("experimental/data/m1_a327_cycleguard_dependency_aware_prechamber_screen.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_dependency_forced_profile_generator.json")

ROOT = Path(__file__).resolve().parents[2]
DEPENDENCY_SCREEN = ROOT / "experimental/scripts/scan_m1_a327_cycleguard_dependency_aware_prechamber_screen.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
P = 17
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dep = load_module("cycleguard_dependency_aware_prechamber", DEPENDENCY_SCREEN)
feedback = dep.feedback
p456 = dep.p456
functional = feedback.zstable.functional


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def normalize_projective(row: list[int]) -> tuple[int, ...]:
    reduced = [int(value) % P for value in row]
    for value in reduced:
        if value:
            inv = pow(value, -1, P)
            return tuple((entry * inv) % P for entry in reduced)
    return tuple(reduced)


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
            matrix[row_idx] = [(matrix[row_idx][idx] - factor * matrix[rank][idx]) % P for idx in range(ncols)]
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


def collision_groups(classes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_functional: dict[tuple[int, ...], list[int]] = defaultdict(list)
    by_support: dict[str, list[int]] = defaultdict(list)
    by_support_functional: dict[tuple[str, tuple[int, ...]], list[int]] = defaultdict(list)
    for idx, row in enumerate(classes):
        functional_key = normalize_projective([int(value) for value in row["functional"]])
        support_hash = row["positions_hash"]
        by_functional[functional_key].append(idx)
        by_support[support_hash].append(idx)
        by_support_functional[(support_hash, functional_key)].append(idx)

    out = []
    for group_type, groups in [
        ("support_coordinate", by_support_functional),
        ("coordinate", by_functional),
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


def forced_profile_rows(
    candidate: dict[str, Any],
    candidate_order: int,
    max_groups_per_candidate: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    classes = feedback.zstable.functional.functional_classes(candidate)
    groups = collision_groups(classes)
    rows = [[int(value) % P for value in row["functional"]] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    base_order = sorted(
        range(len(classes)),
        key=lambda idx: (-supports[idx], normalize_projective(rows[idx]), int(classes[idx]["class_index"])),
    )
    out: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen: set[tuple[int, ...]] = set()

    for group_order, group in enumerate(groups[:max_groups_per_candidate]):
        avoid = set(int(idx) for idx in group["class_offsets"])
        selected = extend_to_basis(classes, avoid=avoid, preferred=base_order)
        if selected is None:
            continue
        group_nonbasis = [idx for idx in group["class_offsets"] if idx not in set(selected)]
        if len(group_nonbasis) < 2:
            continue
        basis_id = (
            f"depforced_{group['group_type']}_{group_order}_"
            f"{'_'.join(str(classes[idx]['class_index']) for idx in selected)}"
        )
        profile = profile_from_selected(classes, selected, basis_id)
        if profile is None:
            continue
        key = tuple(profile["basis_class_indices"])
        if key in seen:
            continue
        seen.add(key)
        meta = {
            "candidate_order": candidate_order,
            "forced_group_order": group_order,
            "forced_group_type": group["group_type"],
            "forced_group_size": group["group_size"],
            "forced_group_class_indices": group["class_indices"],
            "forced_group_nonbasis_count": len(group_nonbasis),
            "candidate_collision_groups": len(groups),
            "candidate_support_coordinate_groups": sum(1 for item in groups if item["group_type"] == "support_coordinate"),
            "candidate_coordinate_groups": sum(1 for item in groups if item["group_type"] == "coordinate"),
            "candidate_support_groups": sum(1 for item in groups if item["group_type"] == "support"),
        }
        out.append((profile, meta))
    return out


def profile_summary(candidate: dict[str, Any], profile: dict[str, Any], meta: dict[str, Any]) -> dict[str, Any]:
    cheap = dep.prechamber.cheap_profile_row(
        candidate,
        profile,
        int(meta["candidate_order"]),
        int(meta["forced_group_order"]),
    )
    features = dep.dependency_features(candidate, profile)
    forced_dependency_score = (
        31 * int(features["support_coordinate_duplicate_excess"])
        + 23 * int(features["coordinate_duplicate_excess"])
        + 13 * int(features["support_duplicate_excess"])
        + 7 * int(meta["forced_group_nonbasis_count"])
        + int(features["dependency_score"])
    )
    return {
        **cheap,
        **features,
        **meta,
        "forced_dependency_score": forced_dependency_score,
    }


def forced_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["support_coordinate_duplicate_excess"]),
        -int(row["coordinate_duplicate_excess"]),
        -int(row["support_duplicate_excess"]),
        -int(row["forced_group_nonbasis_count"]),
        -int(row["forced_dependency_score"]),
        int(row["row_minus_col"]),
        int(row["matrix_shape"][0]),
        int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        -int(row["support_coordinate_duplicate_excess"]),
        -int(row["coordinate_duplicate_excess"]),
        -int(row["forced_dependency_score"]),
        int(row["row_minus_col"]),
        row["template_id"],
        row["basis_id"],
    )


def build_record(
    max_mutations: int,
    seed_offsets: int,
    max_candidates: int,
    max_diverse_candidates: int,
    max_groups_per_candidate: int,
    collect_profile_limit: int,
    rank_profile_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, screened, selected_candidates = p456.structural_candidates(
        max_mutations=max_mutations,
        seed_offsets=seed_offsets,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )

    forced_rows = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    candidates_with_collision_groups = 0
    candidate_group_counts: Counter[str] = Counter()
    for candidate_order, (candidate, _screen) in enumerate(selected_candidates):
        classes = feedback.zstable.functional.functional_classes(candidate)
        groups = collision_groups(classes)
        if groups:
            candidates_with_collision_groups += 1
            candidate_group_counts.update(item["group_type"] for item in groups)
        for profile, meta in forced_profile_rows(candidate, candidate_order, max_groups_per_candidate):
            row = profile_summary(candidate, profile, meta)
            key = (int(row["candidate_order"]), row["basis_id"])
            source_profiles[key] = (candidate, profile)
            forced_rows.append(row)
            if len(forced_rows) >= collect_profile_limit:
                break
        if len(forced_rows) >= collect_profile_limit:
            break

    h_values = feedback.proxy_h_values(PROXY_PRIME)
    powers = feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    targets = sorted(forced_rows, key=forced_sort_key)[:rank_profile_limit]
    proxy_rows = []
    for target in targets:
        candidate, profile = source_profiles[(int(target["candidate_order"]), target["basis_id"])]
        proxy = feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
        proxy_rows.append(
            {
                **target,
                "proxy_prime": proxy["proxy_prime"],
                "proxy_matrix_shape": proxy["matrix_shape"],
                "proxy_rank": proxy["proxy_rank"],
                "proxy_nullity": proxy["proxy_nullity"],
                "best_failure_mode": (
                    "CYCLEG_DEP_FORCED_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "CYCLEG_DEP_FORCED_PROXY_FULL_RANK"
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
            **feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
        }

    failure = "CYCLEG_DEP_FORCED_NO_COLLISION_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / CYCLEG_DEP_FORCED_NO_COLLISION_PROFILES / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "CYCLEG_DEP_FORCED_PROXY_POSITIVE" if positives else "CYCLEG_DEP_FORCED_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / CYCLEG_DEP_FORCED_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / CYCLEG_DEP_FORCED_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    best_forced = max(forced_rows, key=lambda row: int(row["forced_dependency_score"])) if forced_rows else None
    support_coordinate_profiles = [
        row for row in forced_rows if int(row["support_coordinate_duplicate_excess"]) > 0
    ]
    coordinate_collision_profiles = [
        row for row in forced_rows if int(row["coordinate_duplicate_excess"]) > 0
    ]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_dependency_screen": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_collected": previous["dependency_aware_prechamber_screen"]["basis_profiles_collected"],
            "proxy_ranked_profiles": previous["dependency_aware_prechamber_screen"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["dependency_aware_prechamber_screen"]["proxy_positive_profiles"],
            "best_proxy_rank": previous["dependency_aware_prechamber_screen"]["best_proxy_rank"],
            "best_proxy_nullity": previous["dependency_aware_prechamber_screen"]["best_proxy_nullity"],
            "best_dependency_score": previous["dependency_aware_prechamber_screen"]["best_dependency_score"],
            "failure_mode": previous["dependency_aware_prechamber_screen"]["best_failure_mode"],
        },
        "dependency_forced_profile_generator": {
            "proxy_prime": PROXY_PRIME,
            "max_mutations": max_mutations,
            "seed_offsets": seed_offsets,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "max_groups_per_candidate": max_groups_per_candidate,
            "collect_profile_limit": collect_profile_limit,
            "rank_profile_limit": rank_profile_limit,
            "mutations_generated": len(profiles),
            "structural_pass_candidates": sum(
                1 for _candidate, row in screened if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
            ),
            "selected_candidates": len(selected_candidates),
            "candidates_with_collision_groups": candidates_with_collision_groups,
            "candidate_collision_group_counts": dict(candidate_group_counts),
            "forced_profiles_constructed": len(forced_rows),
            "support_coordinate_collision_profiles": len(support_coordinate_profiles),
            "coordinate_collision_profiles": len(coordinate_collision_profiles),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_forced_dependency_score": None if best_forced is None else best_forced["forced_dependency_score"],
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
            "forced_group_type_histogram": dict(Counter(row["forced_group_type"] for row in forced_rows)),
        },
        "best_profile": best,
        "best_forced_profile": best_forced,
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
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "Sage GF(17^32) exact lift",
            "MCA/protocol consequence from this list-track proxy",
            "global obstruction outside the tested dependency-forced prechamber generator",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=646)
    parser.add_argument("--seed-offsets", type=int, default=3)
    parser.add_argument("--max-candidates", type=int, default=180)
    parser.add_argument("--max-diverse-candidates", type=int, default=80)
    parser.add_argument("--max-groups-per-candidate", type=int, default=8)
    parser.add_argument("--collect-profile-limit", type=int, default=96)
    parser.add_argument("--rank-profile-limit", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        seed_offsets=args.seed_offsets,
        max_candidates=args.max_candidates,
        max_diverse_candidates=args.max_diverse_candidates,
        max_groups_per_candidate=args.max_groups_per_candidate,
        collect_profile_limit=args.collect_profile_limit,
        rank_profile_limit=args.rank_profile_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["dependency_forced_profile_generator"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "forced_profiles_constructed": search["forced_profiles_constructed"],
                    "support_coordinate_collision_profiles": search["support_coordinate_collision_profiles"],
                    "coordinate_collision_profiles": search["coordinate_collision_profiles"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_forced_dependency_score": search["best_forced_dependency_score"],
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
        print("M1_A327_CYCLEGUARD_DEPENDENCY_FORCED_PROFILE_GENERATOR_READY")


if __name__ == "__main__":
    main()
