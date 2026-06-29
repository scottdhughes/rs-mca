#!/usr/bin/env python3
"""Extract tested rank-free rules for support-overlap pivot schedules."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import zlib
from pathlib import Path
from typing import Any


SOURCE_DATA = Path("experimental/data/m1_rim_pivot_pattern_theorem.json")
OUTPUT_DATA = Path("experimental/data/m1_support_overlap_rankfree_pivot_rule.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
TARGET_BITS = 128
FIELD_DENOMINATOR = P**FIELD_DEGREE

RANKFREE_RULE_RESULTS_ZLIB_B64 = """
eNrtvV2PXEdyLfpf+KyHjMjIyAi9+drjAwE+NjDH574YBpGfHsIaSSAl3zPH8H+/K4pdTapY3WST1aUamcLYJLurd+2uiIxYa+34
+Jf/fDHaD/PVbD+vl6/mi29f/PnV/1nzZf/xlx9me/2Xl29+er3afDn+Mr5/NV5mKfqyt+/bDwMverPw/zixpsqWXnzzYq6f1+s/
v/qh/fDzyx9+/OH/rtc/vvj259e/rG9e/Ln9/PrV/3n55k/tp/Xi23/JtdI35P+Kb7z64cfXL//U3vwJb+4tjdRqnn2MXNtslrTM
xDOrTCsllUm5pV6Mek9mrnPPlssQl5WZXxyv97r98O8v9y/ff398/x/w91c//+XFt+mbFz+9+o8ff345fvz+zfF9M1eXTLS4lDaX
G96P9qpV026zSBtrJWMj6832sJUGtbJ8i4zWO704XvSn9uo1rvzLDz+/efHtf76gb/jFt/wN/swvvtX4U1586/FnefEtxZ+KP//r
/Z++vyfyVFPbXjbj02oZ/6ZRfQk+H6lkIml6avhgVIutVdaSvnNvtVUbadzf0+sf/7+XP//lp/Xefb355aeffnz988sf/2O9/r79
FC/Bffh/vfcj9/exlasqa+7EPtoua8/e3WeeyqUVk4n7op36xpfyKqN2yY2VF489F+4jrBHXf/u3/Xqtl69/+X69bD//vP78U9zS
v/znneHu3Wa379+s9815+MAOn+/Rfr/6lOnuU6a7T5lPP+VvXvDd9zm+f/iz3P359vv57udyfP3w59uvy92/5e7f5ddWezZHur/q
GHXwWM19zK0ujffcyxtOy0iWCyUbTRbejtvMTdtI3LvY5FFTp/LinF3Hor039zRy2Wm00QpLrtnLmrOn2lnKwne3amojj5VzkeJ5
t51dUg67wohxpR9/fD1x6hFCDvbBv9bru2+/HN+3N7DSi7/7wz//4Y//87t//O5//fN3f/vyb//pf/4/3/3j3/zzP/3xu7/5h5d/
/N//8Ifj6395s9683K/W9/Nle/3q5z/9ef38aty7w5v1/Ro/I+y89Ys3r/7veutYb35uP/8S7/P3f/PdP/zh717+r+/+8X/873/4
mz++xFv+0x9f/Nc3n+Jg6TEH4484GJ84GD/gYHTnYHTiYPQbOpja6FbylAVPg9fk5TxFhy+tvcMzJlmqcxk7lV4S89CpMxNTpdb9
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
"""

REQUIRED_NONCLAIMS = [
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
]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rankfree_rule_results() -> list[dict[str, Any]]:
    packed = "".join(RANKFREE_RULE_RESULTS_ZLIB_B64.split())
    return json.loads(zlib.decompress(base64.b64decode(packed)).decode())


def add_counts(dst: dict[str, int], src: dict[str, int]) -> None:
    for key, value in src.items():
        dst[key] = dst.get(key, 0) + value


def aggregate_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        value = str(item[key])
        out[value] = out.get(value, 0) + 1
    return dict(sorted(out.items()))


def aggregate_pairs(schedules: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for schedule in schedules:
        add_counts(out, schedule["pivot_schedule"]["pair_pivot_counts"])
    return dict(sorted(out.items()))


def aggregate_rule_results(schedules: list[dict[str, Any]]) -> dict[str, Any]:
    by_rule: dict[str, dict[str, int]] = {}
    total = 0
    success = 0
    best_rank_ratio = None
    best_rank_fraction = -1.0
    for schedule in schedules:
        ncols = schedule["matrix_shape"][1]
        for attempt in schedule["rankfree_rules"]:
            total += 1
            rule = attempt["rule"]
            if rule not in by_rule:
                by_rule[rule] = {"tested": 0, "success": 0, "failed": 0}
            by_rule[rule]["tested"] += 1
            if attempt["minor_nonzero"]:
                success += 1
                by_rule[rule]["success"] += 1
            else:
                by_rule[rule]["failed"] += 1
            ratio = [attempt["minor_rank"], ncols]
            fraction = attempt["minor_rank"] / ncols if ncols else 0.0
            if fraction > best_rank_fraction:
                best_rank_fraction = fraction
                best_rank_ratio = ratio
    return {
        "rankfree_rules_tested": sorted(by_rule),
        "rankfree_rule_attempts": total,
        "rankfree_rule_successes": success,
        "rankfree_rule_failures": total - success,
        "rankfree_rule_success_by_rule": dict(sorted(by_rule.items())),
        "best_failed_minor_rank_ratio": best_rank_ratio,
    }


def result_by_source_key() -> dict[str, dict[str, Any]]:
    return {row["source_key"]: row for row in rankfree_rule_results()}


def matrix_schedule(profile: dict[str, Any], exact_result: dict[str, Any]) -> dict[str, Any]:
    pivot = profile["pivot_pattern"]
    cols = profile["compressed_variables"]
    assert profile["classification"] == "support_overlap_rref_pivot"
    assert pivot["support_overlap_schedule"] is True
    assert pivot["category_counts"]["support_overlap_pivots"] == cols
    assert exact_result["source_key"] == profile["source_key"]
    assert exact_result["matrix_shape"] == profile["matrix_shape"]
    assert exact_result["rank"] == profile["rank"] == cols
    assert exact_result["minor_rank_full"] is True
    assert exact_result["pivot_rows_hash"] == pivot["pivot_rows_hash"]
    assert exact_result["pivot_cols_hash"] == pivot["pivot_cols_hash"]
    assert exact_result["pivot_pairs_hash"] == pivot["pivot_pairs_hash"]
    assert exact_result["minor_hash"] == pivot["minor_hash"]
    rankfree_rules = exact_result["rankfree_rule_attempts"]
    best_rule_status = (
        "DETERMINISTIC_COMBINATORIAL_RULE"
        if any(rule["minor_nonzero"] for rule in rankfree_rules)
        else "RREF_DERIVED_ONLY"
    )
    return {
        "candidate_id": profile["candidate_id"],
        "source_key": profile["source_key"],
        "source_packet": profile["source_packet"],
        "source_family": profile["source_family"],
        "matrix_model": profile["matrix_model"],
        "matrix_shape": profile["matrix_shape"],
        "rank": profile["rank"],
        "nullity": profile["nullity"],
        "source_matrix_metadata_hash": profile["source_matrix_metadata_hash"],
        "pattern_class": "support_overlap_rref_pivot",
        "pivot_schedule": {
            "schedule_origin": "RREF_DERIVED_PATTERN",
            "schedule_status": "CERTIFIED_RREF_DERIVED",
            "covered_columns": cols,
            "pivot_rows_used": cols,
            "pivot_columns_used": cols,
            "rref_private_pivot_count": cols,
            "combinatorial_private_pivot_count": None,
            "support_overlap_pivot_count": cols,
            "support_overlap_pivot_fraction": "1",
            "block_triangular_order_exists": False,
            "block_triangular_order_status": "NOT_PROVED",
            "deterministic_combinatorial_schedule": False,
            "pivot_rows_hash": pivot["pivot_rows_hash"],
            "pivot_cols_hash": pivot["pivot_cols_hash"],
            "pivot_pairs_hash": pivot["pivot_pairs_hash"],
            "minor_hash": pivot["minor_hash"],
            "pair_pivot_counts": pivot["pair_pivot_counts"],
            "pair_profile": pivot["pair_profile"],
            "row_type_counts": pivot["row_type_counts"],
            "row_type_signature": pivot["row_type_signature"],
        },
        "rankfree_rules": rankfree_rules,
        "best_rule_status": best_rule_status,
        "route_cut_status": "ROUTE_CUT_CERTIFIED_CANDIDATE",
        "schedule_classification": "RREF_DERIVED_PATTERN",
        "status": "CERTIFIED_RREF_DERIVED",
    }


def build_result(source: dict[str, Any]) -> dict[str, Any]:
    assert threshold_floor() == 6
    assert source["status"] == "M1_RIM_PIVOT_PATTERN_THEOREM_AUDIT"
    assert source["theorem_status"]["support_overlap_schedule_candidate"] is True
    exact_by_key = result_by_source_key()
    profiles = [
        profile
        for profile in source["matrix_profiles"]
        if profile["classification"] == "support_overlap_rref_pivot"
    ]
    profiles.sort(key=lambda item: (item["compressed_variables"], item["candidate_id"]))
    assert set(exact_by_key) == {profile["source_key"] for profile in profiles}
    schedules = [matrix_schedule(profile, exact_by_key[profile["source_key"]]) for profile in profiles]
    assert len(schedules) == 20
    source_packets = aggregate_by(schedules, "source_packet")
    pair_counts = aggregate_pairs(schedules)
    rule_summary = aggregate_rule_results(schedules)
    covered_by_rankfree = sum(
        1 for schedule in schedules if schedule["best_rule_status"] != "RREF_DERIVED_ONLY"
    )
    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "denominator": "17^32",
        "field_denominator": str(FIELD_DENOMINATOR),
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "support_overlap_rankfree_pivot_rule",
        "source_profile": {
            "path": str(SOURCE_DATA),
            "record_hash": source["record_hash"],
            "source_matrices": source["profile_summary"]["source_matrices"],
            "support_overlap_profiles": len(schedules),
            "status": source["global_status"]["status"],
        },
        "schedule_summary": {
            "support_overlap_matrices": len(schedules),
            "source_packet_counts": source_packets,
            "compressed_variable_range": [
                min(item["matrix_shape"][1] for item in schedules),
                max(item["matrix_shape"][1] for item in schedules),
            ],
            "all_pivots_support_overlap": True,
            "all_schedules_rref_derived": True,
            "deterministic_combinatorial_schedule_found": covered_by_rankfree > 0,
            "covered_by_rankfree_rule": covered_by_rankfree,
            "covered_by_incidence_rule": 0,
            "still_rref_derived_only": len(schedules) - covered_by_rankfree,
            "block_triangular_order_proved": False,
            "route_cut_certified_candidates": len(schedules),
            "aggregate_pair_pivot_counts": pair_counts,
            "rankfree_rule_summary": rule_summary,
            "status": "RREF_DERIVED_PATTERN_ONLY",
        },
        "matrix_schedules": schedules,
        "theorem_assessment": {
            "target_statement": (
                "For every reduced matrix in the support_overlap_rref_pivot class, "
                "a deterministic support-overlap schedule selects a full "
                "column-rank minor over GF(17^32)."
            ),
            "tested_rows_support_rref_schedule": True,
            "rankfree_rules_tested": rule_summary["rankfree_rules_tested"],
            "rankfree_rule_attempts": rule_summary["rankfree_rule_attempts"],
            "rankfree_rule_successes": rule_summary["rankfree_rule_successes"],
            "deterministic_schedule_proved": False,
            "reason_not_proved": (
                "The certified schedules are extracted from Sage RREF pivot rows. "
                "The tested rank-free metadata rules all selected singular minors."
            ),
            "status": "RREF_DERIVED_PATTERN_ONLY",
        },
        "interpretation": {
            "a327_certificate_found": False,
            "candidate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "support_overlap_candidates_certified_full_rank": True,
            "rankfree_rule_found": covered_by_rankfree > 0,
            "deterministic_pivot_schedule_theorem_proved": False,
            "status": "AUDIT",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_support_overlap_rankfree_pivot_rule.sage",
            "checks_GF_17_32": True,
            "reconstructs_20_support_matrices": True,
            "recomputes_rref_schedule_hashes": True,
            "tests_rankfree_rule_minors": True,
            "verifies_selected_minors_full_rank": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": REQUIRED_NONCLAIMS,
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": "RREF_DERIVED_PATTERN_ONLY",
        },
        "status": "M1_SUPPORT_OVERLAP_RANKFREE_PIVOT_RULE_AUDIT",
    }
    result["record_hash"] = hash_payload(
        {
            "source_profile": result["source_profile"],
            "schedule_summary": result["schedule_summary"],
            "matrix_schedules": result["matrix_schedules"],
            "theorem_assessment": result["theorem_assessment"],
            "interpretation": result["interpretation"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path, result: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default=SOURCE_DATA, type=Path)
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_result(load_json(args.source))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output, result)
        print(f"WROTE {args.output}")
        print(
            "support-overlap matrices: "
            f"{result['schedule_summary']['support_overlap_matrices']}"
        )
        print(
            "rank-free successes: "
            f"{result['theorem_assessment']['rankfree_rule_successes']}"
        )
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
