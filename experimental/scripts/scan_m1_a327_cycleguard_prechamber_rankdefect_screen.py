#!/usr/bin/env python3
"""Pre-chamber basis-quotient rank-defect screen for M1 a=327 cycleguard search."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "f220bb6"
PREVIOUS_DATA = Path("experimental/data/m1_a327_cycleguard_rankdefect_generation_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_prechamber_rankdefect_screen.json")

ROOT = Path(__file__).resolve().parents[2]
GENERATION_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycleguard_rankdefect_generation_search.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generation = load_module("cycleguard_rankdefect_generation", GENERATION_SCRIPT)
feedback = generation.feedback
p456 = generation.p456
tchamber = generation.tchamber


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def cheap_profile_row(candidate: dict[str, Any], profile: dict[str, Any], candidate_order: int, profile_order: int) -> dict[str, Any]:
    rows, cols = [int(value) for value in profile["matrix_shape"]]
    return {
        "candidate_order": candidate_order,
        "profile_order": profile_order,
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": int(candidate["assignment_seed"]),
        "basis_id": profile["basis_id"],
        "basis_class_indices": [int(value) for value in profile["basis_class_indices"]],
        "basis_support_sizes": [int(value) for value in profile["basis_support_sizes"]],
        "q_variable_count": int(profile["q_variable_count"]),
        "matrix_shape": [rows, cols],
        "row_minus_col": rows - cols,
        "formal_nullity_lower_bound": int(profile["formal_nullity_lower_bound"]),
        "support_vector": [int(value) for value in candidate["support_vector"]],
        "pair7_counts": [int(value) for value in candidate["pair7_counts"]],
        "max_pair_count": int(candidate["max_pair_count"]),
    }


def cheap_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["formal_nullity_lower_bound"]),
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
    cheap: dict[str, Any],
    h_values: list[int],
    powers: list[list[int]],
) -> dict[str, Any]:
    proxy = feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
    return {
        **cheap,
        "proxy_prime": proxy["proxy_prime"],
        "proxy_matrix_shape": proxy["matrix_shape"],
        "proxy_rank": proxy["proxy_rank"],
        "proxy_nullity": proxy["proxy_nullity"],
        "best_failure_mode": (
            "CYCLEG_PRECHAMBER_PROXY_POSITIVE"
            if int(proxy["proxy_nullity"]) > 0
            else "CYCLEG_PRECHAMBER_PROXY_FULL_RANK"
        ),
        "chamber_sampled": False,
        "exact_pairclear_rank_slack_chamber": None,
    }


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        int(row["row_minus_col"]),
        int(row["proxy_matrix_shape"][0]),
        int(row["proxy_matrix_shape"][1]),
        row["template_id"],
        row["basis_id"],
    )


def find_source_pair(
    selected_candidates: list[tuple[dict[str, Any], dict[str, Any]]],
    cheap: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    candidate, _screen = selected_candidates[int(cheap["candidate_order"])]
    profiles = list(
        tchamber.basis_profiles(
            candidate,
            top_classes=26,
            random_bases=96,
            limit=max(int(cheap["profile_order"]) + 1, 1),
        )
    )
    profile = profiles[int(cheap["profile_order"])]
    if candidate["template_id"] != cheap["template_id"] or profile["basis_id"] != cheap["basis_id"]:
        raise RuntimeError("source profile reconstruction mismatch")
    return candidate, profile


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

    cheap_rows: list[dict[str, Any]] = []
    for candidate_order, (candidate, _screen) in enumerate(selected_candidates):
        for profile_order, profile in enumerate(
            tchamber.basis_profiles(
                candidate,
                top_classes=top_classes,
                random_bases=random_bases,
                limit=max_basis_profiles,
            )
        ):
            cheap_rows.append(cheap_profile_row(candidate, profile, candidate_order, profile_order))
            if len(cheap_rows) >= collect_profile_limit:
                break
        if len(cheap_rows) >= collect_profile_limit:
            break

    h_values = feedback.proxy_h_values(PROXY_PRIME)
    powers = feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    ranked_targets = sorted(cheap_rows, key=cheap_sort_key)[:rank_profile_limit]
    proxy_rows = []
    for cheap in ranked_targets:
        candidate, profile = find_source_pair(selected_candidates, cheap)
        proxy_rows.append(proxy_row(candidate, profile, cheap, h_values, powers))

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    failure = "CYCLEG_PRECHAMBER_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / CYCLEG_PRECHAMBER_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "CYCLEG_PRECHAMBER_PROXY_POSITIVE" if positives else "CYCLEG_PRECHAMBER_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / CYCLEG_PRECHAMBER_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / CYCLEG_PRECHAMBER_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    best_candidate = None
    if best is not None:
        candidate, _screen = selected_candidates[int(best["candidate_order"])]
        best_candidate = {
            **feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
        }

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_generation_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_scored": previous["rankdefect_generation_search"]["basis_profiles_scored"],
            "proxy_ranked_profiles": previous["rankdefect_generation_search"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["rankdefect_generation_search"]["proxy_positive_profiles"],
            "best_proxy_rank": previous["rankdefect_generation_search"]["best_proxy_rank"],
            "best_proxy_nullity": previous["rankdefect_generation_search"]["best_proxy_nullity"],
            "failure_mode": previous["rankdefect_generation_search"]["best_failure_mode"],
        },
        "prechamber_rankdefect_screen": {
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
            "basis_profiles_collected": len(cheap_rows),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
            "cheap_shape_histogram": dict(Counter(str(row["row_minus_col"]) for row in cheap_rows)),
        },
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
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "Sage GF(17^32) exact lift",
            "MCA/protocol consequence from this list-track proxy",
            "global obstruction outside the tested cycle-guarded prechamber rank-defect screen",
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
        search = record["prechamber_rankdefect_screen"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "basis_profiles_collected": search["basis_profiles_collected"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
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
        print("M1_A327_CYCLEGUARD_PRECHAMBER_RANKDEFECT_SCREEN_READY")


if __name__ == "__main__":
    main()
