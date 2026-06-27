#!/usr/bin/env python3
"""Verify the M1 a=507 plus-one slope hunt report."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


REPORT_PATH = Path("experimental/data/m1_a507_plus_one_slope_hunt.json")
AGREEMENTS = (506, 507, 508, 509, 510)
A_TARGET = 507
SOURCE_RECORDS = {
    "experimental/data/tangent/tangent_staircase_summary.md",
    "experimental/data/tangent/verify_tangent_staircase.py",
    "experimental/data/tangent-star/tangent_star_no_nontangent_summary.md",
    "experimental/data/tangent-star/verify_tangent_star_threshold.py",
    "experimental/data/adjacent-ledgers/high_agreement_adjacent_ledgers_summary.md",
    "experimental/data/adjacent-ledgers/verify_high_agreement_adjacent_ledgers.py",
}
REQUIRED_NONCLAIMS = {
    "ordinary list decoding",
    "protocol soundness failure",
    "efficient attack",
    "exact delta*_C",
    "new finite-slope support-wise frontier at a=507",
}


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_obj(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()


def reduced_fraction(numerator: int, denominator: int) -> str:
    divisor = math.gcd(numerator, denominator)
    numerator //= divisor
    denominator //= divisor
    if denominator == 1:
        return str(numerator)
    return f"{numerator}/{denominator}"


def exact_start(n: int, k: int) -> int:
    return (2 * n + k + 2) // 3


def ld_sw(n: int, agreement: int) -> int:
    return n - agreement + 1


def existing_slope_labels(agreement: int, count: int) -> list[str]:
    return [
        f"a{agreement}_finite_tangent_slope_{index:03d}"
        for index in range(count)
    ]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify_parameters(report: dict[str, Any]) -> dict[str, Any]:
    params = report["parameters"]
    q = 17**32
    n = 512
    k = 256
    threshold_den = 2**128
    threshold_floor = q // threshold_den
    start = exact_start(n, k)

    require(report["schema"] == "m1-a507-plus-one-slope-hunt.v1", "schema")
    require(params["row"] == "RS[F_17^32,H,256]", "row")
    require(params["field_base"] == 17, "field base")
    require(params["field_degree"] == 32, "field degree")
    require(params["q_line"] == "17^32", "q_line")
    require(int(params["q_line_integer"]) == q, "q_line integer")
    require(params["n"] == n, "n")
    require(params["k"] == k, "k")
    require(params["rate"] == "1/2", "rate")
    require(params["target_agreement"] == A_TARGET, "target agreement")
    require(params["threshold_bits"] == 128, "threshold bits")
    require(params["threshold_floor"] == threshold_floor == 6, "threshold floor")
    require(params["exact_staircase_start"] == start == 427, "exact start")
    require(6 * threshold_den < q < 7 * threshold_den, "integer gate margins")
    return {"q": q, "n": n, "k": k, "threshold_floor": threshold_floor}


def verify_board_replay(report: dict[str, Any], context: dict[str, Any]) -> list[dict[str, Any]]:
    rows = report["board_replay_rows"]
    require([row["agreement"] for row in rows] == list(AGREEMENTS), "replay rows")
    checked = []
    for row in rows:
        agreement = row["agreement"]
        expected = ld_sw(context["n"], agreement)
        require(row["N_bad"] == expected, f"N_bad replay at {agreement}")
        require(row["closed_distance"] == context["n"] - agreement, "closed distance")
        require(
            row["closed_radius"]
            == reduced_fraction(context["n"] - agreement, context["n"]),
            "closed radius",
        )
        require(
            row["clears_gate"] == (expected > context["threshold_floor"]),
            "gate bool",
        )
        checked.append(
            {
                "agreement": agreement,
                "N_bad": expected,
                "clears_gate": row["clears_gate"],
                "status": row["status"],
            }
        )
    require(checked[0]["N_bad"] == 7 and checked[0]["clears_gate"], "a=506")
    require(checked[1]["N_bad"] == 6 and not checked[1]["clears_gate"], "a=507")
    return checked


def verify_families(report: dict[str, Any]) -> list[dict[str, Any]]:
    families = report["searched_families"]
    names = {family["family"] for family in families}
    required = {
        "finite_slope_supportwise_tangent_star",
        "tangent_floor_refinement",
        "projective_slope_or_no_loss_CA",
        "quotient_core_refinement_same_predicate",
        "two_ended_locator_variant_same_predicate",
        "slope_symmetry_frobenius_dilation",
        "adjacent_line_plus_interleaved_list",
    }
    require(required <= names, "searched family coverage")
    for family in families:
        require(family["extra_same_predicate_slopes"] == 0, "family extra count")
        if family["family"] == "adjacent_line_plus_interleaved_list":
            require(family["status"] == "BRIDGE_NEEDED", "adjacent status")
            require(
                family["classification_scope"] == "bridge_target_not_counted_in_LD_sw",
                "adjacent classification scope",
            )
            require(family["conditional_total_numerator"] == 7, "adjacent total")
        elif family["family"] == "projective_slope_or_no_loss_CA":
            require(family["status"] == "ROUTE_CUT", "projective/CA status")
            require(
                family["classification_scope"]
                == "not_exhaustive_outside_LD_sw_predicate",
                "projective/CA classification scope",
            )
        else:
            require(family["status"] == "ROUTE_CUT", "route cut family")
            require(
                family["classification_scope"] == "same_predicate_exclusion_only",
                "same-predicate classification scope",
            )
    return families


def verify_candidates(report: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    existing = existing_slope_labels(A_TARGET, 6)
    require(report["existing_a507_slopes"] == existing, "existing slopes")
    require(report["existing_a507_slope_hash"] == sha256_obj(existing), "existing hash")
    events = report["candidate_events"]
    require(len(events) == 1, "candidate event count")
    event = events[0]
    require(event["agreement"] == A_TARGET, "candidate agreement")
    require(event["denominator"] == "17^32", "candidate denominator")
    require(int(event["denominator_integer"]) == context["q"], "candidate q")
    require(event["is_existing_slope"] is False, "candidate existing")
    require(event["disjoint_from_existing_six"] is True, "candidate disjoint")
    require(event["counted_in_N_bad"] is False, "candidate not counted")
    require(event["proof_status"] == "BRIDGE_NEEDED", "candidate bridge status")
    require(event["slope_list_hash"] == sha256_obj(existing), "candidate slope hash")

    counted_proof_records = [
        candidate
        for candidate in events
        if candidate["counted_in_N_bad"]
        and candidate["proof_status"] == "PROOF_RECORD"
    ]
    require(counted_proof_records == [], "no counted proof-record plus-one")
    return {
        "candidate_count": len(events),
        "counted_proof_record_extra_count": len(counted_proof_records),
        "bridge_needed_count": sum(
            1 for candidate in events if candidate["proof_status"] == "BRIDGE_NEEDED"
        ),
    }


def verify_result(report: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    result = report["plus_one_result"]
    require(result["status"] == "ROUTE_CUT", "result status")
    require(
        result["route_cut_scope"]
        == "same_denominator_same_finite_slope_supportwise_LD_sw_predicate_only",
        "route cut scope",
    )
    require(result["N_bad_507_old"] == 6, "old N_bad")
    require(result["extra_valid_same_predicate_count"] == 0, "extra valid")
    require(result["N_bad_507_new"] == 6, "new N_bad")
    require(result["threshold_floor"] == context["threshold_floor"], "floor")
    require(result["clears_gate"] is False, "gate remains safe")
    require(result["same_predicate_frontier_moved"] is False, "frontier not moved")

    adjacent = report["adjacent_bridge_ledger"]
    require(adjacent["status"] == "BRIDGE_NEEDED", "adjacent status")
    require(adjacent["line_numerator"] == 6, "adjacent line")
    require(adjacent["interleaved_list_numerator"] == 1, "adjacent list")
    require(adjacent["conditional_total_numerator"] == 7, "adjacent total")
    require(adjacent["conditional_total_clears_gate"] is True, "adjacent clears")
    require(adjacent["counted_in_N_bad"] is False, "adjacent not counted")
    return {"plus_one_result": result, "adjacent_bridge_ledger": adjacent}


def verify_metadata(report: dict[str, Any]) -> dict[str, Any]:
    require(set(report["source_records"]) == SOURCE_RECORDS, "source records")
    require(REQUIRED_NONCLAIMS <= set(report["nonclaims"]), "nonclaims")
    require(report["script_version"].startswith("m1-a507-plus-one"), "script version")
    return {
        "source_records": sorted(report["source_records"]),
        "nonclaims_checked": sorted(REQUIRED_NONCLAIMS),
    }


def verify_report(path: Path) -> dict[str, Any]:
    report = json.loads(path.read_text(encoding="utf-8"))
    context = verify_parameters(report)
    replay = verify_board_replay(report, context)
    families = verify_families(report)
    candidates = verify_candidates(report, context)
    result = verify_result(report, context)
    metadata = verify_metadata(report)
    return {
        "status": "PASS",
        "report": str(path),
        "parameters": {
            "q_line": "17^32",
            "q_line_integer": str(context["q"]),
            "n": context["n"],
            "k": context["k"],
            "threshold_floor": context["threshold_floor"],
            "target_agreement": A_TARGET,
        },
        "board_replay": replay,
        "families_checked": len(families),
        "candidates": candidates,
        "result": result,
        "metadata": metadata,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = verify_report(args.report)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("a=507 same-predicate N_bad remains 6")
        print("adjacent line-plus-list total is 7 but BRIDGE_NEEDED")


if __name__ == "__main__":
    main()
