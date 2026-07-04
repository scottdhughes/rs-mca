#!/usr/bin/env python3
"""Tail-pair projection repair search for M1 a=327 pair-clear row-span kernels."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "8184509"
PREVIOUS_DATA = Path("experimental/data/m1_a327_pairclear_rowspan_dependence_mutation.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_pairclear_tailpair_projection_repair.json")

ROOT = Path(__file__).resolve().parents[2]
ROWSPAN_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_pairclear_rowspan_dependence_mutation.py"

TARGET_TAIL_PAIRS = ["P56", "P57", "P67"]
TARGET_AGREEMENT = 327


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rowspan = load_module("pairclear_rowspan_dependence_mutation", ROWSPAN_SCRIPT)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def forced_pair_info(row: dict[str, Any]) -> dict[str, Any]:
    best = row.get("extended_best_subspace_direction") or {}
    forced_pairs = list(best.get("forced_pairs") or [])
    return {
        "forced_pair_count": int(best.get("forced_pair_count", 99)),
        "forced_pairs": forced_pairs,
        "tail_forced_count": sum(1 for pair in forced_pairs if pair in TARGET_TAIL_PAIRS),
        "tail_pairs_cleared": [pair for pair in TARGET_TAIL_PAIRS if pair not in forced_pairs],
        "direction": best.get("direction"),
        "direction_weight": best.get("direction_weight"),
    }


def tail_score_key(row: dict[str, Any]) -> tuple[Any, ...]:
    info = forced_pair_info(row)
    extended_rank_slack = bool(row.get("extended_rank_slack"))
    return (
        0 if row.get("deep_rank_slack_repair") else 1,
        0 if extended_rank_slack else 1,
        info["forced_pair_count"],
        info["tail_forced_count"],
        row.get("extended_rank", 99),
        row.get("base_rank", 99),
        info["direction_weight"] if info["direction_weight"] is not None else 99,
        row["template_id"],
        row["basis_id"],
    )


def compact_profile(row: dict[str, Any]) -> dict[str, Any]:
    base = rowspan.compact_profile(row)
    base["tailpair_projection"] = forced_pair_info(row)
    return base


def build_record(
    max_mutations: int,
    max_candidates: int,
    max_diverse_candidates: int,
    top_classes: int,
    random_bases: int,
    max_basis_profiles: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    previous_search = previous["rowspan_dependence_mutation"]
    profiles, screened, selected_candidates = rowspan.structural_candidates(
        max_mutations=max_mutations,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )

    analyzed = []
    basis_profiles_tested = 0
    for candidate, _screen in selected_candidates:
        for profile in rowspan.target_aware_basis_profiles(
            candidate,
            top_classes=top_classes,
            random_bases=random_bases,
            max_basis_profiles=max_basis_profiles,
        ):
            basis_profiles_tested += 1
            analyzed.append(rowspan.analyze_profile(candidate, profile))

    target_present = [row for row in analyzed if row["target_rows_present"]]
    extended_rank_slack = [row for row in target_present if row.get("extended_rank_slack")]
    extended_pair_clear = [row for row in target_present if row.get("extended_pair_clear")]
    deep = [row for row in analyzed if row.get("deep_rank_slack_repair")]
    tail_candidates = [row for row in extended_rank_slack if row.get("extended_best_subspace_direction")]
    best = min(tail_candidates or analyzed, key=tail_score_key) if analyzed else None

    forced_counts = Counter()
    forced_patterns = Counter()
    tail_forced_counts = Counter()
    for row in tail_candidates:
        info = forced_pair_info(row)
        forced_counts[str(info["forced_pair_count"])] += 1
        forced_patterns[",".join(info["forced_pairs"])] += 1
        tail_forced_counts[str(info["tail_forced_count"])] += 1

    failure = "TAILPAIR_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / TAILPAIR_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if best:
        info = forced_pair_info(best)
        if best.get("deep_rank_slack_repair"):
            failure = "TAILPAIR_EXACT_PAIRCLEAR_REPAIRED"
            proof_status = "CANDIDATE / TAILPAIR_EXACT_PAIRCLEAR_REPAIRED / PARTIAL / EXPERIMENTAL"
        elif best.get("extended_rank_slack") and info["forced_pair_count"] <= 1:
            failure = "TAILPAIR_NEAR_REPAIR"
            proof_status = "CANDIDATE / TAILPAIR_NEAR_REPAIR / PARTIAL / EXPERIMENTAL"
        elif best.get("extended_rank_slack"):
            failure = "TAILPAIR_FORCED_PROJECTIONS_REMAIN"
            proof_status = "EXACT_EXTRACTION_NO_A327 / TAILPAIR_FORCED_PROJECTIONS_REMAIN / PARTIAL / EXPERIMENTAL"
        else:
            failure = best["best_failure_mode"].replace("ROWSPAN", "TAILPAIR")
            proof_status = f"EXACT_EXTRACTION_NO_A327 / {failure} / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_rowspan_dependence_mutation": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "extended_rank_slack_profiles": previous_search["extended_rank_slack_profiles"],
            "extended_rank_slack_pair_clear_profiles": previous_search["extended_rank_slack_pair_clear_profiles"],
            "best_failure_mode": previous_search["best_failure_mode"],
        },
        "tailpair_projection_repair": {
            "target_tail_pairs": TARGET_TAIL_PAIRS,
            "max_mutations": max_mutations,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "top_classes": top_classes,
            "random_bases": random_bases,
            "max_basis_profiles": max_basis_profiles,
            "mutations_generated": len(profiles),
            "milp_profiles_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE"),
            "candidate_systems_constructed": sum(1 for profile in profiles if profile.get("solver_status") == "OPTIMAL_OR_FEASIBLE") * 3,
            "structural_pass_candidates": sum(
                1 for _candidate, row in screened if row["backward_structural_status"] == "TCHAMBER_STRUCTURAL_PASS"
            ),
            "selected_candidates": len(selected_candidates),
            "basis_profiles_tested": basis_profiles_tested,
            "target_rows_present_profiles": len(target_present),
            "extended_rank_slack_profiles": len(extended_rank_slack),
            "extended_pair_clear_profiles": len(extended_pair_clear),
            "deep_rank_slack_repair_profiles": len(deep),
            "tail_candidates": len(tail_candidates),
            "forced_pair_count_histogram": dict(forced_counts),
            "tail_forced_count_histogram": dict(tail_forced_counts),
            "forced_pair_pattern_counts": dict(forced_patterns.most_common(12)),
            "best_template_id": None if best is None else best["template_id"],
            "best_mutation_id": None if best is None else best.get("mutation_id"),
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_basis_id": None if best is None else best["basis_id"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in analyzed)),
            "screen_counts": dict(Counter(row["backward_structural_status"] for _candidate, row in screened)),
        },
        "best_profile": None if best is None else compact_profile(best),
        "profile_summaries": [compact_profile(row) for row in sorted(tail_candidates or analyzed, key=tail_score_key)[:40]],
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
            "global obstruction outside the tested tail-pair projection repair front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=640)
    parser.add_argument("--max-candidates", type=int, default=260)
    parser.add_argument("--max-diverse-candidates", type=int, default=120)
    parser.add_argument("--top-classes", type=int, default=24)
    parser.add_argument("--random-bases", type=int, default=96)
    parser.add_argument("--max-basis-profiles", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        max_candidates=args.max_candidates,
        max_diverse_candidates=args.max_diverse_candidates,
        top_classes=args.top_classes,
        random_bases=args.random_bases,
        max_basis_profiles=args.max_basis_profiles,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["tailpair_projection_repair"]
        best = record["best_profile"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "extended_rank_slack_profiles": search["extended_rank_slack_profiles"],
                    "extended_pair_clear_profiles": search["extended_pair_clear_profiles"],
                    "tail_candidates": search["tail_candidates"],
                    "forced_pair_count_histogram": search["forced_pair_count_histogram"],
                    "tail_forced_count_histogram": search["tail_forced_count_histogram"],
                    "best_template_id": search["best_template_id"],
                    "best_basis_id": search["best_basis_id"],
                    "best_forced_pairs": None if best is None else best["tailpair_projection"]["forced_pairs"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_PAIRCLEAR_TAILPAIR_PROJECTION_REPAIR_READY")


if __name__ == "__main__":
    main()
