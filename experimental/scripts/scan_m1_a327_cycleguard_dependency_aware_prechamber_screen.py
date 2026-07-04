#!/usr/bin/env python3
"""Dependency-aware pre-chamber screen for M1 a=327 cycleguard rank defect."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "31d5b30"
PREVIOUS_DATA = Path("experimental/data/m1_a327_cycleguard_prechamber_rankdefect_screen.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_dependency_aware_prechamber_screen.json")

ROOT = Path(__file__).resolve().parents[2]
PRECHAMBER_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycleguard_prechamber_rankdefect_screen.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
P = 17


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


prechamber = load_module("cycleguard_prechamber_rankdefect", PRECHAMBER_SCRIPT)
feedback = prechamber.feedback
p456 = prechamber.p456
tchamber = prechamber.tchamber


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


def dependency_features(candidate: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    classes = feedback.zstable.functional.functional_classes(candidate)
    by_index = {int(row["class_index"]): row for row in classes}
    support_hashes = []
    coord_rows = []
    support_coord_pairs = []
    for row in profile["nonbasis_constraint_detail"]:
        class_index = int(row["class_index"])
        support_hash = by_index[class_index]["positions_hash"]
        coord = normalize_projective([int(value) for value in row["basis_coordinates"]])
        support_hashes.append(support_hash)
        coord_rows.append(coord)
        support_coord_pairs.append((support_hash, coord))

    support_counts = Counter(support_hashes)
    coord_counts = Counter(coord_rows)
    pair_counts = Counter(support_coord_pairs)
    support_duplicate_excess = sum(count - 1 for count in support_counts.values() if count > 1)
    coord_duplicate_excess = sum(count - 1 for count in coord_counts.values() if count > 1)
    pair_duplicate_excess = sum(count - 1 for count in pair_counts.values() if count > 1)
    repeated_support_rows = sum(count for count in support_counts.values() if count > 1)
    repeated_coord_rows = sum(count for count in coord_counts.values() if count > 1)
    repeated_pair_rows = sum(count for count in pair_counts.values() if count > 1)
    rows, cols = [int(value) for value in profile["matrix_shape"]]
    dependency_score = (
        13 * pair_duplicate_excess
        + 8 * support_duplicate_excess
        + 5 * coord_duplicate_excess
        + repeated_pair_rows
        + repeated_support_rows
        + repeated_coord_rows
    )
    return {
        "dependency_score": dependency_score,
        "support_collision_groups": sum(1 for count in support_counts.values() if count > 1),
        "support_duplicate_excess": support_duplicate_excess,
        "repeated_support_rows": repeated_support_rows,
        "coordinate_collision_groups": sum(1 for count in coord_counts.values() if count > 1),
        "coordinate_duplicate_excess": coord_duplicate_excess,
        "repeated_coordinate_rows": repeated_coord_rows,
        "support_coordinate_collision_groups": sum(1 for count in pair_counts.values() if count > 1),
        "support_coordinate_duplicate_excess": pair_duplicate_excess,
        "repeated_support_coordinate_rows": repeated_pair_rows,
        "unique_support_hashes": len(support_counts),
        "unique_coordinate_rows": len(coord_counts),
        "unique_support_coordinate_pairs": len(pair_counts),
        "row_minus_col": rows - cols,
    }


def profile_row(candidate: dict[str, Any], profile: dict[str, Any], candidate_order: int, profile_order: int) -> dict[str, Any]:
    cheap = prechamber.cheap_profile_row(candidate, profile, candidate_order, profile_order)
    return {**cheap, **dependency_features(candidate, profile)}


def dependency_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["dependency_score"]),
        -int(row["support_coordinate_duplicate_excess"]),
        -int(row["support_duplicate_excess"]),
        -int(row["coordinate_duplicate_excess"]),
        int(row["row_minus_col"]),
        int(row["matrix_shape"][0]),
        int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
        int(row["assignment_seed"]),
    )


def proxy_row(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    row: dict[str, Any],
    h_values: list[int],
    powers: list[list[int]],
) -> dict[str, Any]:
    proxy = feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
    return {
        **row,
        "proxy_prime": proxy["proxy_prime"],
        "proxy_matrix_shape": proxy["matrix_shape"],
        "proxy_rank": proxy["proxy_rank"],
        "proxy_nullity": proxy["proxy_nullity"],
        "best_failure_mode": (
            "CYCLEG_DEP_PRECHAMBER_PROXY_POSITIVE"
            if int(proxy["proxy_nullity"]) > 0
            else "CYCLEG_DEP_PRECHAMBER_PROXY_FULL_RANK"
        ),
        "chamber_sampled": False,
        "exact_pairclear_rank_slack_chamber": None,
    }


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        -int(row["dependency_score"]),
        int(row["row_minus_col"]),
        int(row["proxy_matrix_shape"][0]),
        int(row["proxy_matrix_shape"][1]),
        row["template_id"],
        row["basis_id"],
    )


def build_record(
    max_mutations: int,
    seed_offsets: int,
    max_candidates: int,
    max_diverse_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
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
    collected: list[dict[str, Any]] = []
    for candidate_order, (candidate, _screen) in enumerate(selected_candidates):
        for profile_order, profile in enumerate(
            tchamber.basis_profiles(
                candidate,
                top_classes=top_classes,
                random_bases=random_bases,
                limit=max_basis_profiles,
            )
        ):
            collected.append(profile_row(candidate, profile, candidate_order, profile_order))
            if len(collected) >= collect_profile_limit:
                break
        if len(collected) >= collect_profile_limit:
            break

    h_values = feedback.proxy_h_values(PROXY_PRIME)
    powers = feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    targets = sorted(collected, key=dependency_sort_key)[:rank_profile_limit]
    proxy_rows = []
    for target in targets:
        candidate, profile = prechamber.find_source_pair(selected_candidates, target)
        proxy_rows.append(proxy_row(candidate, profile, target, h_values, powers))

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    best_candidate = None
    if best is not None:
        candidate, _screen = selected_candidates[int(best["candidate_order"])]
        best_candidate = {
            **feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
        }

    failure = "CYCLEG_DEP_PRECHAMBER_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / CYCLEG_DEP_PRECHAMBER_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "CYCLEG_DEP_PRECHAMBER_PROXY_POSITIVE" if positives else "CYCLEG_DEP_PRECHAMBER_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / CYCLEG_DEP_PRECHAMBER_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / CYCLEG_DEP_PRECHAMBER_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    best_collected = max(collected, key=lambda row: int(row["dependency_score"])) if collected else None
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_prechamber_screen": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_collected": previous["prechamber_rankdefect_screen"]["basis_profiles_collected"],
            "proxy_ranked_profiles": previous["prechamber_rankdefect_screen"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["prechamber_rankdefect_screen"]["proxy_positive_profiles"],
            "best_proxy_rank": previous["prechamber_rankdefect_screen"]["best_proxy_rank"],
            "best_proxy_nullity": previous["prechamber_rankdefect_screen"]["best_proxy_nullity"],
            "failure_mode": previous["prechamber_rankdefect_screen"]["best_failure_mode"],
        },
        "dependency_aware_prechamber_screen": {
            "proxy_prime": PROXY_PRIME,
            "max_mutations": max_mutations,
            "seed_offsets": seed_offsets,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "collect_profile_limit": collect_profile_limit,
            "rank_profile_limit": rank_profile_limit,
            "mutations_generated": len(profiles),
            "structural_pass_candidates": sum(
                1 for _candidate, row in screened if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
            ),
            "selected_candidates": len(selected_candidates),
            "basis_profiles_collected": len(collected),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_dependency_score": None if best_collected is None else best_collected["dependency_score"],
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
            "dependency_score_histogram": dict(Counter(str(row["dependency_score"]) for row in collected)),
        },
        "best_profile": best,
        "best_dependency_profile": best_collected,
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
            "global obstruction outside the tested dependency-aware prechamber screen",
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
    parser.add_argument("--top-classes", type=int, default=26)
    parser.add_argument("--random-bases", type=int, default=96)
    parser.add_argument("--max-basis-profiles", type=int, default=4)
    parser.add_argument("--collect-profile-limit", type=int, default=96)
    parser.add_argument("--rank-profile-limit", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        seed_offsets=args.seed_offsets,
        max_candidates=args.max_candidates,
        max_diverse_candidates=args.max_diverse_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
        collect_profile_limit=args.collect_profile_limit,
        rank_profile_limit=args.rank_profile_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["dependency_aware_prechamber_screen"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "basis_profiles_collected": search["basis_profiles_collected"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_dependency_score": search["best_dependency_score"],
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
        print("M1_A327_CYCLEGUARD_DEPENDENCY_AWARE_PRECHAMBER_SCREEN_READY")


if __name__ == "__main__":
    main()
