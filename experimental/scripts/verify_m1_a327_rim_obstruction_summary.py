#!/usr/bin/env python3
"""Dependency-free verifier for the M1 a=327 RIM obstruction summary."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_rim_obstruction_summary.json")

SOURCE_FILES = {
    "rank_gate": Path("experimental/data/m1_nonquotient_pairwise_overlap_rank_gate.json"),
    "pivot_replay": Path("experimental/data/m1_rim_support_pattern_pivot_replay.json"),
    "pivot_patterns": Path("experimental/data/m1_rim_pivot_pattern_theorem.json"),
    "support_overlap_rankfree": Path("experimental/data/m1_support_overlap_rankfree_pivot_rule.json"),
    "generic_pairwise_rankfree": Path("experimental/data/m1_generic_pairwise_rankfree_pivot_rule.json"),
    "quotient_residual_rankfree": Path("experimental/data/m1_quotient_residual_rankfree_pivot_rule.json"),
}

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "global RIM full-rank theorem",
    "deterministic combinatorial pivot schedule",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify() -> dict[str, Any]:
    summary = load_json(DATA_PATH)
    sources = {key: load_json(path) for key, path in SOURCE_FILES.items()}

    require(summary["track"] == "INTERLEAVED_LIST", "wrong track")
    require(summary["denominator"] == "17^32", "wrong denominator")
    require(summary["agreement_target"] == 327, "wrong target agreement")
    require(summary["baseline"]["current_pr_133_agreement"] == 326, "wrong baseline agreement")
    require(summary["baseline"]["current_pr_133_lambda_lower"] == 7, "wrong baseline lambda")
    require(summary["repo_claim"]["mca_counted"] is False, "MCA counted unexpectedly")
    require(summary["repo_claim"]["improves_pr_133"] is False, "PR #133 improvement claimed")
    require(
        REQUIRED_NONCLAIMS.issubset(set(summary["repo_claim"]["not_claimed"])),
        "missing non-claims",
    )

    rank_gate = sources["rank_gate"]["pairwise_overlap_rank_gate"]
    support_design = sources["rank_gate"]["support_design"]
    support_sizes = support_design["witness_support_sizes"]
    require(summary["rank_gate"]["support_count"] == len(support_sizes), "support count mismatch")
    require(
        all(size == summary["rank_gate"]["support_size"] for size in support_sizes),
        "support size mismatch",
    )
    require(
        summary["rank_gate"]["max_pair_intersection"] == support_design["pair_intersection_max"],
        "max pair intersection mismatch",
    )
    require(
        summary["rank_gate"]["matrix_shape"]
        == [rank_gate["remaining_pairwise_equations"], rank_gate["compressed_variables"]],
        "rank-gate matrix shape mismatch",
    )
    require(summary["rank_gate"]["rank"] == rank_gate["rank"], "rank-gate rank mismatch")
    require(summary["rank_gate"]["nullity"] == rank_gate["nullity"], "rank-gate nullity mismatch")
    require(rank_gate["non_diagonal_solution_found"] is False, "rank gate found non-diagonal solution")

    replay_summary = sources["pivot_replay"]["pivot_summary"]
    pattern_summary = sources["pivot_patterns"]["profile_summary"]
    require(replay_summary["all_source_matrices_certified"] is True, "not all source matrices certified")
    require(summary["pivot_coverage"]["source_matrices"] == pattern_summary["source_matrices"], "source count mismatch")
    require(summary["pivot_coverage"]["pivot_certified"] == pattern_summary["pivot_covered"], "pivot count mismatch")
    require(
        summary["pivot_coverage"]["pattern_classes"]["support_overlap_rref_pivot"]
        == pattern_summary["source_family_counts"]["support_pattern"],
        "support-overlap class count mismatch",
    )
    require(
        summary["pivot_coverage"]["pattern_classes"]["generic_pairwise_rref_pivot"]
        == pattern_summary["source_family_counts"]["balanced_clique"],
        "generic-pairwise class count mismatch",
    )
    require(
        summary["pivot_coverage"]["pattern_classes"]["quotient_residual_rref_pivot"]
        == pattern_summary["source_family_counts"]["two_level_quotient_residual"],
        "quotient-residual class count mismatch",
    )
    require(
        summary["pivot_coverage"]["aggregate_row_type_counts"]
        == pattern_summary["aggregate_row_type_counts"],
        "aggregate row type counts mismatch",
    )
    require(
        summary["pivot_coverage"]["common_structural_pattern_found"]
        == pattern_summary["global_common_structural_pattern_found"],
        "structural pattern flag mismatch",
    )

    support_rankfree = sources["support_overlap_rankfree"]["schedule_summary"]
    support_rules = support_rankfree["rankfree_rule_summary"]
    require(summary["rank_free_audits"]["support_overlap"]["matrices"] == support_rankfree["support_overlap_matrices"], "support-overlap matrix count mismatch")
    require(summary["rank_free_audits"]["support_overlap"]["attempts"] == support_rules["rankfree_rule_attempts"], "support-overlap attempt count mismatch")
    require(summary["rank_free_audits"]["support_overlap"]["successes"] == support_rules["rankfree_rule_successes"], "support-overlap success count mismatch")

    generic_rules = sources["generic_pairwise_rankfree"]["rule_summary"]
    require(summary["rank_free_audits"]["generic_pairwise"]["matrices"] == sources["generic_pairwise_rankfree"]["matrix_count"], "generic matrix count mismatch")
    require(summary["rank_free_audits"]["generic_pairwise"]["attempts"] == generic_rules["rank_free_attempts"], "generic attempt count mismatch")
    require(summary["rank_free_audits"]["generic_pairwise"]["successes"] == generic_rules["rank_free_successes"], "generic success count mismatch")
    require(
        summary["rank_free_audits"]["generic_pairwise"]["deterministic_rule_successes"]
        == generic_rules["success_by_rule_class"]["DETERMINISTIC_COMBINATORIAL_RULE"]["success"],
        "generic deterministic success mismatch",
    )

    quotient_rules = sources["quotient_residual_rankfree"]["rule_summary"]
    require(summary["rank_free_audits"]["quotient_residual"]["matrices"] == sources["quotient_residual_rankfree"]["matrix_count"], "quotient matrix count mismatch")
    require(summary["rank_free_audits"]["quotient_residual"]["attempts"] == quotient_rules["rank_free_attempts"], "quotient attempt count mismatch")
    require(summary["rank_free_audits"]["quotient_residual"]["successes"] == quotient_rules["rank_free_successes"], "quotient success count mismatch")
    require(summary["rank_free_audits"]["quotient_residual"]["deterministic_rule_successes"] == quotient_rules["deterministic_rule_successes"], "quotient deterministic success mismatch")
    require(summary["rank_free_audits"]["quotient_residual"]["rref_mimic_successes"] == quotient_rules["rref_mimic_rule_successes"], "quotient RREF mimic success mismatch")
    require(summary["rank_free_audits"]["quotient_residual"]["large_matrix_successes"] == quotient_rules["large_matrix_rank_free_successes"], "quotient large-matrix success mismatch")

    return {
        "status": "PASS",
        "track": summary["track"],
        "agreement_target": summary["agreement_target"],
        "pivot_certified": summary["pivot_coverage"]["pivot_certified"],
        "rank_free_successes": {
            key: value["successes"]
            for key, value in summary["rank_free_audits"].items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable result")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "PASS: M1 a=327 RIM obstruction summary matches source JSON "
            f"(pivot_certified={result['pivot_certified']})"
        )


if __name__ == "__main__":
    main()
