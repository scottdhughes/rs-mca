#!/usr/bin/env python3
"""Generate mu_8 rank-feedback schedule mutations for exact follow-up."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "dd07a87"
ORBIT_DATA = Path("experimental/data/m1_a327_mu8_orbit_invariant_construction.json")
BLOCK_DATA = Path("experimental/data/m1_a327_mu8_block_decomposition_audit.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_mu8_block_rank_feedback_scan.json")

MU_ORDER = 8
TARGET_SUPPORT = 328
PAIR_CAP = 255


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def autocorrelation(subset: list[int]) -> dict[int, int]:
    support = set(subset)
    return {
        shift: sum(1 for value in support if ((value + shift) % MU_ORDER) in support)
        for shift in range(1, MU_ORDER)
    }


def schedule_autocorrelation(patterns: list[list[int]]) -> dict[int, int]:
    totals = {shift: 0 for shift in range(1, MU_ORDER)}
    for pattern in patterns:
        corr = autocorrelation(pattern)
        for shift, value in corr.items():
            totals[shift] += value
    return totals


def normalize_patterns(patterns: list[list[int]]) -> list[list[int]]:
    return [sorted({int(value) % MU_ORDER for value in pattern}) for pattern in patterns]


def affine_relabel(patterns: list[list[int]], scale: int, shift: int) -> list[list[int]]:
    return normalize_patterns([
        [((scale * value + shift) % MU_ORDER) for value in pattern]
        for pattern in patterns
    ])


def rotate_pattern(pattern: list[int], shift: int) -> list[int]:
    return sorted(((value + shift) % MU_ORDER for value in pattern))


def guard_metrics(patterns: list[list[int]]) -> dict[str, Any]:
    support = sum(len(pattern) for pattern in patterns) * (64 // len(patterns))
    corr = schedule_autocorrelation(patterns)
    ambient = max(corr.values()) * (64 // len(patterns))
    return {
        "support_per_codeword": support,
        "autocorrelation_by_shift": {str(key): value for key, value in corr.items()},
        "ambient_pair_bound": ambient,
        "guard_pass": support >= TARGET_SUPPORT and ambient <= PAIR_CAP,
    }


def mutate(patterns: list[list[int]]) -> list[dict[str, Any]]:
    result = []
    # Affine relabels preserve many orbit symmetries but test label placement.
    for scale in [1, 3, 5, 7]:
        for shift in range(MU_ORDER):
            if scale == 1 and shift == 0:
                continue
            result.append({"move": f"affine_a{scale}_b{shift}", "patterns": affine_relabel(patterns, scale, shift)})
    # Rotate a single pattern; this keeps pattern sizes and total support fixed.
    for idx in range(len(patterns)):
        for shift in range(1, MU_ORDER):
            trial = [pattern[:] for pattern in patterns]
            trial[idx] = rotate_pattern(trial[idx], shift)
            result.append({"move": f"rotate_pattern_{idx}_by_{shift}", "patterns": normalize_patterns(trial)})
    # Single in/out swaps inside one pattern.
    for idx, pattern in enumerate(patterns):
        present = set(pattern)
        missing = [value for value in range(MU_ORDER) if value not in present]
        for old in sorted(present):
            for new in missing:
                trial = [row[:] for row in patterns]
                updated = sorted((present - {old}) | {new})
                trial[idx] = updated
                result.append({"move": f"swap_pattern_{idx}_{old}_to_{new}", "patterns": normalize_patterns(trial)})
    return result


def candidate_score(patterns: list[list[int]], metrics: dict[str, Any]) -> tuple[int, int, int, int]:
    sizes = Counter(len(pattern) for pattern in patterns)
    diversity = len({tuple(pattern) for pattern in patterns})
    autocorr_values = [int(value) for value in metrics["autocorrelation_by_shift"].values()]
    slack = PAIR_CAP - int(metrics["ambient_pair_bound"])
    balance = max(autocorr_values) - min(autocorr_values)
    # Lower tuple is better.
    return (balance, -diversity, -slack, -sizes.get(5, 0))


def build_record(limit: int) -> dict[str, Any]:
    orbit = load_json(ORBIT_DATA)
    block = load_json(BLOCK_DATA)
    guard_schedules = [
        row for row in orbit["schedule_results"]
        if row["status"] != "MU8_SCHEDULE_GUARD_FAIL"
    ]
    seen = set()
    candidates = []
    for source in guard_schedules:
        for mutation in mutate(source["patterns"]):
            patterns = mutation["patterns"]
            key = hash_payload(patterns)
            if key in seen:
                continue
            seen.add(key)
            metrics = guard_metrics(patterns)
            if not metrics["guard_pass"]:
                continue
            candidates.append(
                {
                    "candidate_id": f"mu8_mut_{len(candidates):05d}",
                    "source_schedule_id": source["schedule_id"],
                    "move": mutation["move"],
                    "patterns": patterns,
                    "patterns_hash": key,
                    "support_per_codeword": metrics["support_per_codeword"],
                    "ambient_pair_bound": metrics["ambient_pair_bound"],
                    "autocorrelation_by_shift": metrics["autocorrelation_by_shift"],
                    "score_tuple": list(candidate_score(patterns, metrics)),
                    "exact_rank_status": "NOT_RUN",
                }
            )
    candidates.sort(key=lambda row: tuple(row["score_tuple"]))
    selected = candidates[:limit]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": 327,
        "source_commit": SOURCE_COMMIT,
        "source_artifacts": {
            "mu8_orbit_front": str(ORBIT_DATA),
            "mu8_block_audit": str(BLOCK_DATA),
        },
        "rank_feedback_basis": {
            "guard_schedules": len(guard_schedules),
            "block_audit_reproduction_pass": block["block_audit"]["canonical_reproduction_pass"],
            "equivariance_certified_schedules": block["block_audit"]["equivariance_certified_schedules"],
            "positive_full_nullity_schedules": block["block_audit"]["positive_full_nullity_schedules"],
            "positive_residue_subset_schedules": block["block_audit"]["positive_residue_subset_schedules"],
        },
        "mutation_front": {
            "raw_guard_passing_mutations": len(candidates),
            "selected_for_exact_followup": len(selected),
            "moves": dict(Counter(row["move"].split("_")[0] for row in candidates)),
            "best_ambient_pair_bound": None if not selected else selected[0]["ambient_pair_bound"],
            "best_score_tuple": None if not selected else selected[0]["score_tuple"],
            "best_failure_mode": "MU8_RANK_FEEDBACK_EXACT_RANK_PENDING",
        },
        "candidate_schedules": selected,
        "proof_status": "CANDIDATE / MU8_RANK_FEEDBACK_EXACT_RANK_PENDING / PARTIAL / EXPERIMENTAL",
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
    parser.add_argument("--limit", type=int, default=64)
    args = parser.parse_args()
    record = build_record(limit=args.limit)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        "raw_guard_passing_mutations": record["mutation_front"]["raw_guard_passing_mutations"],
        "selected_for_exact_followup": record["mutation_front"]["selected_for_exact_followup"],
        "best_ambient_pair_bound": record["mutation_front"]["best_ambient_pair_bound"],
        "best_score_tuple": record["mutation_front"]["best_score_tuple"],
        "best_failure_mode": record["mutation_front"]["best_failure_mode"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_BLOCK_RANK_FEEDBACK_SCAN_READY")


if __name__ == "__main__":
    main()
