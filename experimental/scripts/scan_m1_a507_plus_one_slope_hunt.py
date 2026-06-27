#!/usr/bin/env python3
"""Run the a=507 plus-one slope hunt ledger.

This is a theorem-driven scanner, not an F_17^32 enumerator.  It replays the
integrated high-agreement tangent-star formulas, records same-predicate
exclusion labels, and keeps the adjacent line-plus-list term bridge-needed
instead of counting it as a support-wise bad slope.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_VERSION = "m1-a507-plus-one-slope-hunt.v1"
DEFAULT_OUTPUT = Path("experimental/data/m1_a507_plus_one_slope_hunt.json")
AGREEMENTS = (506, 507, 508, 509, 510)
A_TARGET = 507


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def run_git(args: list[str]) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except Exception:
        return "UNAVAILABLE"
    return proc.stdout.strip()


def exact_start(n: int, k: int) -> int:
    return (2 * n + k + 2) // 3


def reduced_fraction(numerator: int, denominator: int) -> str:
    divisor = math.gcd(numerator, denominator)
    numerator //= divisor
    denominator //= divisor
    if denominator == 1:
        return str(numerator)
    return f"{numerator}/{denominator}"


def ld_sw(n: int, agreement: int) -> int:
    return n - agreement + 1


def existing_slope_labels(agreement: int, count: int) -> list[str]:
    return [
        f"a{agreement}_finite_tangent_slope_{index:03d}"
        for index in range(count)
    ]


def board_replay_rows(n: int, budget_floor: int) -> list[dict[str, Any]]:
    rows = []
    for agreement in AGREEMENTS:
        count = ld_sw(n, agreement)
        rows.append(
            {
                "agreement": agreement,
                "closed_distance": n - agreement,
                "closed_radius": reduced_fraction(n - agreement, n),
                "N_bad": count,
                "clears_gate": count > budget_floor,
                "status": (
                    "PROOF_RECORD_UNSAFE"
                    if count > budget_floor
                    else (
                        "PROOF_RECORD_SAFE_GATE"
                        if agreement == A_TARGET
                        else "PROOF_RECORD_SAFE"
                    )
                ),
            }
        )
    return rows


def searched_families(n: int, k: int) -> list[dict[str, Any]]:
    exact_from = exact_start(n, k)
    return [
        {
            "family": "finite_slope_supportwise_tangent_star",
            "status": "ROUTE_CUT",
            "same_predicate": True,
            "classification_scope": "same_predicate_exclusion_only",
            "reason": "exact tangent-star upper bound gives LD_sw(C,507)=6",
            "extra_same_predicate_slopes": 0,
            "source": "experimental/data/tangent-star/tangent_star_no_nontangent_summary.md",
        },
        {
            "family": "tangent_floor_refinement",
            "status": "ROUTE_CUT",
            "same_predicate": True,
            "classification_scope": "same_predicate_exclusion_only",
            "reason": "moving-root floor is already exact for a>=427",
            "extra_same_predicate_slopes": 0,
            "source": "experimental/data/tangent/tangent_staircase_summary.md",
        },
        {
            "family": "projective_slope_or_no_loss_CA",
            "status": "ROUTE_CUT",
            "same_predicate": False,
            "classification_scope": "not_exhaustive_outside_LD_sw_predicate",
            "reason": "if recast as a same-predicate finite support-wise slope, the exact LD_sw(C,507)=6 bound excludes a seventh counted event",
            "extra_same_predicate_slopes": 0,
            "source": "experimental/data/adjacent-ledgers/high_agreement_adjacent_ledgers_summary.md",
        },
        {
            "family": "quotient_core_refinement_same_predicate",
            "status": "ROUTE_CUT",
            "same_predicate": True,
            "classification_scope": "same_predicate_exclusion_only",
            "reason": "any same-predicate a=507 event is counted by LD_sw and is excluded by the exact upper bound",
            "extra_same_predicate_slopes": 0,
            "source": "experimental/SUMMARY.md",
        },
        {
            "family": "two_ended_locator_variant_same_predicate",
            "status": "ROUTE_CUT",
            "same_predicate": True,
            "classification_scope": "same_predicate_exclusion_only",
            "reason": "same-predicate locator outputs at a=507 would contradict LD_sw(C,507)=6",
            "extra_same_predicate_slopes": 0,
            "source": "experimental/notes/m1/m1_cycle120_standalone_ldsw_proof.md",
        },
        {
            "family": "slope_symmetry_frobenius_dilation",
            "status": "ROUTE_CUT",
            "same_predicate": True,
            "classification_scope": "same_predicate_exclusion_only",
            "reason": "symmetry images inside the same row and predicate are still finite support-wise slopes and are included in LD_sw(C,507)",
            "extra_same_predicate_slopes": 0,
            "source": "experimental/data/tangent-star/tangent_star_no_nontangent_summary.md",
        },
        {
            "family": "adjacent_line_plus_interleaved_list",
            "status": "BRIDGE_NEEDED",
            "same_predicate": False,
            "classification_scope": "bridge_target_not_counted_in_LD_sw",
            "reason": "line numerator 6 plus interleaved-list numerator 1 gives a conditional coding-ledger total 7, not a seventh support-wise slope",
            "extra_same_predicate_slopes": 0,
            "source": "experimental/data/adjacent-ledgers/high_agreement_adjacent_ledgers_summary.md",
            "conditional_total_numerator": 7,
        },
    ]


def bridge_candidate(q_line: int, q_label: str, existing: list[str]) -> dict[str, Any]:
    candidate = {
        "agreement": A_TARGET,
        "slope_id": "adjacent_interleaved_unique_list_term_not_a_slope",
        "predicate_family": "adjacent_line_plus_interleaved_list",
        "is_existing_slope": False,
        "disjoint_from_existing_six": True,
        "denominator": q_label,
        "denominator_integer": str(q_line),
        "counted_in_N_bad": False,
        "proof_status": "BRIDGE_NEEDED",
        "bridge_needed": (
            "This is an interleaved-list coding-ledger term, not a finite "
            "support-wise bad slope."
        ),
        "existing_slope_hash": sha256_obj(existing),
    }
    candidate["retained_event_hash"] = sha256_obj(candidate)
    candidate["support_template_hash"] = sha256_obj(
        {
            "agreement": A_TARGET,
            "line_numerator": 6,
            "interleaved_list_numerator": 1,
            "conditional_total": 7,
        }
    )
    candidate["slope_list_hash"] = sha256_obj(existing)
    return candidate


def build_report() -> dict[str, Any]:
    p = 17
    field_degree = 32
    q_line = p**field_degree
    q_label = "17^32"
    n = 512
    k = 256
    threshold_bits = 128
    threshold_den = 2**threshold_bits
    budget_floor = q_line // threshold_den
    exact_from = exact_start(n, k)
    old_count = ld_sw(n, A_TARGET)
    existing = existing_slope_labels(A_TARGET, old_count)
    bridge = bridge_candidate(q_line, q_label, existing)
    extra_valid = 0
    new_count = old_count + extra_valid
    adjacent_line = old_count
    adjacent_list = 1
    adjacent_total = adjacent_line + adjacent_list

    script_path = Path(__file__).resolve()
    return {
        "schema": "m1-a507-plus-one-slope-hunt.v1",
        "script_version": SCRIPT_VERSION,
        "generated_at_utc": _dt.datetime.now(_dt.UTC).isoformat(),
        "repository": {
            "git_head_before_write": run_git(["rev-parse", "HEAD"]),
            "git_branch": run_git(["branch", "--show-current"]),
            "git_status_short_before_write": run_git(["status", "--short"]),
        },
        "runtime": {
            "python": sys.version,
            "platform": platform.platform(),
        },
        "script_sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
        "parameters": {
            "row": "RS[F_17^32,H,256]",
            "field_base": p,
            "field_degree": field_degree,
            "q_line": q_label,
            "q_line_integer": str(q_line),
            "n": n,
            "k": k,
            "rate": reduced_fraction(k, n),
            "target_agreement": A_TARGET,
            "threshold_bits": threshold_bits,
            "threshold_floor": budget_floor,
            "exact_staircase_start": exact_from,
        },
        "source_records": [
            "experimental/data/tangent/tangent_staircase_summary.md",
            "experimental/data/tangent/verify_tangent_staircase.py",
            "experimental/data/tangent-star/tangent_star_no_nontangent_summary.md",
            "experimental/data/tangent-star/verify_tangent_star_threshold.py",
            "experimental/data/adjacent-ledgers/high_agreement_adjacent_ledgers_summary.md",
            "experimental/data/adjacent-ledgers/verify_high_agreement_adjacent_ledgers.py",
        ],
        "integer_gate": {
            "inequality": "2^128 * N_bad > 17^32",
            "threshold_floor": budget_floor,
            "six_is_safe": 6 * threshold_den < q_line,
            "seven_is_unsafe": 7 * threshold_den > q_line,
        },
        "board_replay_rows": board_replay_rows(n, budget_floor),
        "existing_a507_slopes": existing,
        "existing_a507_slope_hash": sha256_obj(existing),
        "searched_families": searched_families(n, k),
        "candidate_events": [bridge],
        "plus_one_result": {
            "status": "ROUTE_CUT",
            "route_cut_scope": "same_denominator_same_finite_slope_supportwise_LD_sw_predicate_only",
            "N_bad_507_old": old_count,
            "extra_valid_same_predicate_count": extra_valid,
            "N_bad_507_new": new_count,
            "threshold_floor": budget_floor,
            "clears_gate": new_count > budget_floor,
            "same_predicate_frontier_moved": False,
        },
        "adjacent_bridge_ledger": {
            "status": "BRIDGE_NEEDED",
            "line_numerator": adjacent_line,
            "interleaved_list_numerator": adjacent_list,
            "conditional_total_numerator": adjacent_total,
            "conditional_total_clears_gate": adjacent_total > budget_floor,
            "counted_in_N_bad": False,
        },
        "nonclaims": [
            "ordinary list decoding",
            "protocol soundness failure",
            "efficient attack",
            "exact delta*_C",
            "new finite-slope support-wise frontier at a=507",
            "combining different event semantics without a bridge",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {args.output}")
    print(f"STATUS {report['plus_one_result']['status']}")
    print(f"N_BAD_507_NEW {report['plus_one_result']['N_bad_507_new']}")
    print(
        "ADJACENT_CONDITIONAL_TOTAL "
        f"{report['adjacent_bridge_ledger']['conditional_total_numerator']}"
    )


if __name__ == "__main__":
    main()
