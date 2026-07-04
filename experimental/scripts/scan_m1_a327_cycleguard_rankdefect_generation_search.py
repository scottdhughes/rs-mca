#!/usr/bin/env python3
"""Generate cycle-guarded chambers with live basis-quotient rank feedback."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "639c399"
PREVIOUS_DATA = Path("experimental/data/m1_a327_cycleguard_rankdefect_feedback_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_rankdefect_generation_search.json")

ROOT = Path(__file__).resolve().parents[2]
FEEDBACK_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycleguard_rankdefect_feedback_search.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


feedback = load_module("cycleguard_rankdefect_feedback", FEEDBACK_SCRIPT)
cycleg = feedback.cycleg
p456 = feedback.p456
tchamber = feedback.tchamber
diverse = cycleg.diverse


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def live_profile_summary(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    scored: dict[str, Any],
    proxy: dict[str, Any],
) -> dict[str, Any]:
    row = feedback.compact_profile(candidate, profile, scored, proxy)
    row["generation_failure_mode"] = scored["best_failure_mode"]
    row["cycle_clear_directions"] = int(scored["cycle_clear_directions"])
    row["exact_pairclear_directions"] = int(scored["exact_pairclear_directions"])
    row["exact_pairclear_rank_slack_directions"] = int(scored["exact_pairclear_rank_slack_directions"])
    return row


def build_record(
    max_mutations: int,
    seed_offsets: int,
    max_candidates: int,
    max_diverse_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
    sample_directions: int,
    rank_profile_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, screened, selected_candidates = p456.structural_candidates(
        max_mutations=max_mutations,
        seed_offsets=seed_offsets,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )
    directions = diverse.sampled_projective_directions(sample_directions)
    h_values = feedback.proxy_h_values(PROXY_PRIME)
    powers = feedback.precompute_powers_mod(h_values, PROXY_PRIME)

    basis_profiles_scored = 0
    exact_pairclear_rank_slack_seen = 0
    ranked_profiles = []
    generation_failures: Counter[str] = Counter()
    stopped_reason = "EXHAUSTED_GENERATION_FRONT"

    for candidate, _screen in selected_candidates:
        for profile in tchamber.basis_profiles(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            limit=max_basis_profiles,
        ):
            basis_profiles_scored += 1
            scored = cycleg.guarded_score_profile(candidate, profile, directions)
            generation_failures[scored["best_failure_mode"]] += 1
            if scored.get("best_exact_pairclear_rank_slack_chamber") is None:
                continue
            exact_pairclear_rank_slack_seen += 1
            proxy = feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
            ranked_profiles.append(live_profile_summary(candidate, profile, scored, proxy))
            if len(ranked_profiles) >= rank_profile_limit:
                stopped_reason = "RANK_PROFILE_LIMIT_REACHED"
                break
        if stopped_reason == "RANK_PROFILE_LIMIT_REACHED":
            break

    positives = [row for row in ranked_profiles if int(row["proxy_nullity"]) > 0]
    best = min(ranked_profiles, key=feedback.profile_sort_key) if ranked_profiles else None
    best_full_candidate = None
    if best is not None:
        for candidate, _screen in selected_candidates:
            if (
                candidate["template_id"] == best["template_id"]
                and int(candidate["assignment_seed"]) == int(best["assignment_seed"])
                and candidate["assignment_strategy"] == best["assignment_strategy"]
            ):
                best_full_candidate = candidate
                break

    failure = "CYCLEG_RANKGEN_NO_EXACT_PAIRCLEAR_RANKSLACK"
    proof_status = "EXACT_EXTRACTION_NO_A327 / CYCLEG_RANKGEN_NO_EXACT_PAIRCLEAR_RANKSLACK / PARTIAL / EXPERIMENTAL"
    if ranked_profiles:
        failure = "CYCLEG_RANKGEN_PROXY_POSITIVE" if positives else "CYCLEG_RANKGEN_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / CYCLEG_RANKGEN_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / CYCLEG_RANKGEN_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_feedback_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "proxy_ranked_profiles": previous["rankdefect_feedback_search"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["rankdefect_feedback_search"]["proxy_positive_profiles"],
            "best_proxy_rank": previous["rankdefect_feedback_search"]["best_proxy_rank"],
            "best_proxy_nullity": previous["rankdefect_feedback_search"]["best_proxy_nullity"],
            "failure_mode": previous["rankdefect_feedback_search"]["best_failure_mode"],
        },
        "rankdefect_generation_search": {
            "proxy_prime": PROXY_PRIME,
            "max_mutations": max_mutations,
            "seed_offsets": seed_offsets,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "sample_directions": sample_directions,
            "rank_profile_limit": rank_profile_limit,
            "mutations_generated": len(profiles),
            "structural_pass_candidates": sum(
                1 for _candidate, row in screened if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
            ),
            "selected_candidates": len(selected_candidates),
            "basis_profiles_scored": basis_profiles_scored,
            "exact_pairclear_rank_slack_seen": exact_pairclear_rank_slack_seen,
            "proxy_ranked_profiles": len(ranked_profiles),
            "proxy_positive_profiles": len(positives),
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_failure_mode": failure,
            "stopped_reason": stopped_reason,
            "generation_failure_counts": dict(generation_failures),
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in ranked_profiles)),
        },
        "best_profile": best,
        "best_candidate": None if best_full_candidate is None else {
            **feedback.compact_candidate(best_full_candidate),
            "coordinate_classes": best_full_candidate["coordinate_classes"],
        },
        "ranked_profiles": sorted(ranked_profiles, key=feedback.profile_sort_key),
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
            "global obstruction outside the tested cycle-guarded rank-defect generation front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=646)
    parser.add_argument("--seed-offsets", type=int, default=3)
    parser.add_argument("--max-candidates", type=int, default=520)
    parser.add_argument("--max-diverse-candidates", type=int, default=180)
    parser.add_argument("--top-classes", type=int, default=26)
    parser.add_argument("--random-bases", type=int, default=96)
    parser.add_argument("--max-basis-profiles", type=int, default=8)
    parser.add_argument("--sample-directions", type=int, default=2048)
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
        sample_directions=args.sample_directions,
        rank_profile_limit=args.rank_profile_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["rankdefect_generation_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "basis_profiles_scored": search["basis_profiles_scored"],
                    "exact_pairclear_rank_slack_seen": search["exact_pairclear_rank_slack_seen"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_template_id": None if record["best_profile"] is None else record["best_profile"]["template_id"],
                    "best_basis_id": None if record["best_profile"] is None else record["best_profile"]["basis_id"],
                    "best_failure_mode": search["best_failure_mode"],
                    "stopped_reason": search["stopped_reason"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_CYCLEGUARD_RANKDEFECT_GENERATION_SEARCH_READY")


if __name__ == "__main__":
    main()
