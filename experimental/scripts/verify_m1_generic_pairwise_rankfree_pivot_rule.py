#!/usr/bin/env python3
"""Dependency-free verifier for the M1 generic-pairwise rank-free pivot audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_generic_pairwise_rankfree_pivot_rule.json")
SOURCE_DATA = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")
PATTERN_CLASS = "generic_pairwise_rref_pivot"

EXPECTED_RULES = [
    "anchored_pair_proxy_first",
    "compressed_variable_block_order",
    "incidence_greedy_matching_v1",
    "nonanchored_difference_first",
    "pair_boundary_pressure_asc",
    "pair_boundary_pressure_desc",
    "pair_label_lexicographic_order",
    "rref_profile_pair_quota_mimic",
]

EXPECTED_SOURCE_PACKET_COUNTS = {
    "pairwise_divisibility_nullvector_system": 6,
}

EXPECTED_SOURCE_FAMILY_COUNTS = {
    "balanced_clique": 6,
}

REQUIRED_NONCLAIMS = {
    "a=327 interleaved-list certificate",
    "global Lambda_mu(C,327) <= 6",
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond the stated interleaved-list predicate",
    "exact Lambda_mu",
    "exact delta*_C",
    "improvement over PR #133",
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def source_generic_profiles(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        row["source_key"]: row
        for row in source["matrix_profiles"]
        if row["classification"] == PATTERN_CLASS
    }


def aggregate_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        value = str(item[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def add_counts(dst: dict[str, int], src: dict[str, int]) -> None:
    for key, value in src.items():
        dst[key] = dst.get(key, 0) + int(value)


def aggregate_pairs(matrices: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for matrix in matrices:
        add_counts(out, matrix["rref_certificate"]["pair_pivot_counts"])
    return dict(sorted(out.items()))


def aggregate_rule_summary(matrices: list[dict[str, Any]]) -> dict[str, Any]:
    by_rule = {
        rule: {"tested": 0, "success": 0, "failed": 0}
        for rule in EXPECTED_RULES
    }
    by_class: dict[str, dict[str, int]] = {}
    total = 0
    success = 0
    best_failed = [-1, 1]
    best_failed_detail = None
    for matrix in matrices:
        ncols = matrix["matrix_shape"][1]
        for attempt in matrix["rankfree_rules"]:
            total += 1
            rule = attempt["rule"]
            rule_class = attempt["rule_class"]
            assert rule in by_rule
            by_rule[rule]["tested"] += 1
            by_class.setdefault(rule_class, {"tested": 0, "success": 0, "failed": 0})
            by_class[rule_class]["tested"] += 1
            if attempt["minor_nonzero"]:
                success += 1
                by_rule[rule]["success"] += 1
                by_class[rule_class]["success"] += 1
            else:
                by_rule[rule]["failed"] += 1
                by_class[rule_class]["failed"] += 1
                if attempt["minor_rank"] * best_failed[1] > best_failed[0] * ncols:
                    best_failed = [attempt["minor_rank"], ncols]
                    best_failed_detail = {
                        "candidate_id": matrix["candidate_id"],
                        "rule": rule,
                        "minor_rank": attempt["minor_rank"],
                        "selected_minor_size": ncols,
                    }
    return {
        "rules_tested": len(EXPECTED_RULES),
        "rule_names": EXPECTED_RULES,
        "rank_free_attempts": total,
        "rank_free_successes": success,
        "rank_free_failures": total - success,
        "success_by_rule": dict(sorted(by_rule.items())),
        "success_by_rule_class": dict(sorted(by_class.items())),
        "best_failed_minor_rank_ratio": best_failed,
        "best_failed_minor": best_failed_detail,
        "status": "RREF_DERIVED_PATTERN_ONLY" if success == 0 else "CANDIDATE_THEOREM",
    }


def validate_matrix(matrix: dict[str, Any], source_profile: dict[str, Any]) -> None:
    assert matrix["source_key"] == source_profile["source_key"]
    assert matrix["candidate_id"] == source_profile["candidate_id"]
    assert matrix["source_packet"] == source_profile["source_packet"]
    assert matrix["source_family"] == source_profile["source_family"] == "balanced_clique"
    assert matrix["pattern_class"] == PATTERN_CLASS
    assert matrix["matrix_shape"] == source_profile["matrix_shape"]
    assert matrix["rank"] == source_profile["rank"] == matrix["matrix_shape"][1]
    assert matrix["nullity"] == source_profile["nullity"] == 0
    assert matrix["rref_certificate_status"] == "CERTIFIED"
    assert matrix["route_cut_status"] == "ROUTE_CUT_CERTIFIED_CANDIDATE"
    assert matrix["best_rule_status"] == "RREF_DERIVED_ONLY"

    cert = matrix["rref_certificate"]
    source_pivot = source_profile["pivot_pattern"]
    assert cert["certificate_type"] == "RREF_PIVOT_MINOR"
    assert cert["minor_size"] == matrix["matrix_shape"][1]
    assert cert["minor_rank_full"] is True
    assert cert["determinant_nonzero"] is True
    assert cert["status"] == "CERTIFIED_FULL_RANK"
    assert cert["row_type_counts"] == {"balanced_or_generic_pairwise_row": cert["minor_size"]}
    assert cert["row_type_counts"] == source_pivot["row_type_counts"]
    assert cert["pair_pivot_counts"] == source_pivot["pair_pivot_counts"]
    for key in ["pivot_rows_hash", "pivot_cols_hash", "pivot_pairs_hash", "minor_hash"]:
        assert len(cert[key]) == 64
        assert cert[key] == source_pivot[key]

    attempts = matrix["rankfree_rules"]
    assert len(attempts) == len(EXPECTED_RULES)
    assert [attempt["rule"] for attempt in attempts] == EXPECTED_RULES
    assert matrix["rankfree_rule_successes"] == []
    for attempt in attempts:
        assert attempt["rule_class"] in {
            "DETERMINISTIC_COMBINATORIAL_RULE",
            "RREF_MIMIC_RULE",
        }
        assert attempt["uses_field_arithmetic"] is False
        assert attempt["rule_uses_field_arithmetic"] is False
        assert attempt["selected_minor_size"] == matrix["matrix_shape"][1]
        assert attempt["minor_nonzero"] is False
        assert attempt["minor_rank"] < matrix["matrix_shape"][1]
        assert attempt["status"] == "SINGULAR_MINOR"
        for key in ["pivot_rows_hash", "pivot_cols_hash", "pivot_pairs_hash"]:
            assert len(attempt[key]) == 64
        assert sum(attempt["pair_pivot_counts"].values()) == matrix["matrix_shape"][1]


def validate_record(record: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert record["n"] == 512
    assert record["k"] == 256
    assert record["denominator"] == "17^32"
    assert record["agreement"] == 327
    assert record["agreement_target"] == 327
    assert record["target_bits"] == 128
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert record["pattern_class"] == PATTERN_CLASS
    assert record["construction_mode"] == "generic_pairwise_rankfree_pivot_rule"
    assert record["status"] == "M1_GENERIC_PAIRWISE_RANKFREE_PIVOT_RULE_AUDIT"

    source_profiles = source_generic_profiles(source)
    matrices = record["matrices"]
    assert len(source_profiles) == 6
    assert record["matrix_count"] == len(matrices) == 6
    assert set(source_profiles) == {matrix["source_key"] for matrix in matrices}
    for matrix in matrices:
        validate_matrix(matrix, source_profiles[matrix["source_key"]])

    assert record["source_profile"] == {
        "path": str(SOURCE_DATA),
        "record_hash": source["record_hash"],
        "source_matrices": 34,
        "generic_pairwise_profiles": 6,
        "status": "CANDIDATE_THEOREM_ONLY",
    }
    assert record["source_family_counts"] == EXPECTED_SOURCE_FAMILY_COUNTS
    assert record["source_packet_counts"] == EXPECTED_SOURCE_PACKET_COUNTS
    assert record["source_family_counts"] == aggregate_by(matrices, "source_family")
    assert record["source_packet_counts"] == aggregate_by(matrices, "source_packet")
    assert record["aggregate_pair_pivot_counts"] == aggregate_pairs(matrices)
    assert record["rule_summary"] == aggregate_rule_summary(matrices)
    assert record["rule_summary"]["rank_free_attempts"] == 48
    assert record["rule_summary"]["rank_free_successes"] == 0
    assert record["rank_free_successes"] == 0
    assert record["rref_derived_certificates_replayed"] == 6
    assert record["theorem_assessment"] == {
        "target_statement": (
            "For the generic_pairwise_rref_pivot class, a metadata-only "
            "row schedule selects a full column-rank minor over GF(17^32)."
        ),
        "rankfree_rules_tested": EXPECTED_RULES,
        "rankfree_rule_attempts": 48,
        "rankfree_rule_successes": 0,
        "deterministic_schedule_proved": False,
        "reason_not_proved": (
            "All tested generic-pairwise metadata rules selected singular "
            "minors; the full-rank certificates remain RREF-derived."
        ),
        "status": "RREF_DERIVED_PATTERN_ONLY",
    }
    assert record["interpretation"] == {
        "a327_certificate_found": False,
        "candidate_found": False,
        "global_Lambda_mu_327_upper_bound": False,
        "generic_pairwise_candidates_certified_full_rank": True,
        "rankfree_rule_found": False,
        "deterministic_pivot_schedule_theorem_proved": False,
        "status": "AUDIT",
    }
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "RREF_DERIVED_PATTERN_ONLY",
    }
    assert record["repo_claim"]["mca_counted"] is False
    assert set(record["repo_claim"]["not_claimed"]) == REQUIRED_NONCLAIMS

    expected_hash = hash_payload(
        {
            "source_profile": record["source_profile"],
            "rule_summary": record["rule_summary"],
            "matrices": record["matrices"],
            "theorem_assessment": record["theorem_assessment"],
            "interpretation": record["interpretation"],
            "global": record["global_status"],
        }
    )
    assert record["record_hash"] == expected_hash
    return {
        "generic_pairwise_matrices": len(matrices),
        "rref_derived_certificates_replayed": record["rref_derived_certificates_replayed"],
        "rankfree_rule_attempts": record["rule_summary"]["rank_free_attempts"],
        "rankfree_rule_successes": record["rank_free_successes"],
        "deterministic_schedule_proved": record["theorem_assessment"][
            "deterministic_schedule_proved"
        ],
        "status": record["global_status"]["status"],
        "record_hash": record["record_hash"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default=DATA_PATH, type=Path)
    parser.add_argument("--source", default=SOURCE_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    summary = validate_record(load_json(args.data), load_json(args.source))
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("M1_GENERIC_PAIRWISE_RANKFREE_PIVOT_RULE_VERIFY_OK")
        print(f"generic-pairwise matrices: {summary['generic_pairwise_matrices']}")
        print(
            "rref-derived certificates replayed: "
            f"{summary['rref_derived_certificates_replayed']}"
        )
        print(f"rank-free attempts: {summary['rankfree_rule_attempts']}")
        print(f"rank-free successes: {summary['rankfree_rule_successes']}")
        print(
            "deterministic schedule proved: "
            f"{summary['deterministic_schedule_proved']}"
        )
        print(f"status: {summary['status']}")


if __name__ == "__main__":
    main()
