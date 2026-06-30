#!/usr/bin/env python3
"""Verifier for the M1 a=327 collapse-quotient line-search packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_collapse_quotient_line_search.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "LINE_COLLAPSE_PERSISTS",
    "LINE_CAPACITY_LOSS",
    "LINE_LOW_RESCHEDULE",
    "LINE_PROXY_CANDIDATE",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "8dbcb6b", "wrong source commit")
    require(record["construction_mode"] == "collapse_quotient_line_search", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    collapse = record["collapse_subspace"]
    require(collapse["collapse_dimension"] == 103, "unexpected collapse dimension")
    require(collapse["quotient_dimension"] == 793, "unexpected quotient dimension")
    systems = record["systems"]
    require(len(systems) == collapse["systems_tested"] > 0, "bad system count")
    line_search = record["line_search"]
    require(line_search["anchors_tested"] == sum(row["anchors_tested"] for row in systems), "bad anchor count")
    require(line_search["quotient_directions_tested"] == sum(row["quotient_directions_tested"] for row in systems), "bad direction count")
    require(line_search["lambda_values_tested"] == sum(row["lambda_values_tested"] for row in systems), "bad lambda count")
    candidate_count = 0
    for row in systems:
        require(row["proxy_rank"] + row["proxy_nullity"] == 1536, "bad rank/nullity")
        require(row["quotient_dimension"] == row["proxy_nullity"] - row["collapse_subspace_dimension"], "bad quotient dimension")
        require(row["anchors_tested"] > 0, "no anchors tested")
        require(row["quotient_directions_tested"] > 0, "no directions tested")
        require(row["lambda_values_tested"] == row["anchors_tested"] * row["quotient_directions_tested"] * row["lambda_values_per_line"], "bad row lambda count")
        for line in row["retained_lines"]:
            require(line["failure_mode"] in ALLOWED_FAILURES, f"bad line failure {line['failure_mode']}")
            if line["failure_mode"] == "LINE_PROXY_CANDIDATE":
                candidate_count += 1
                require(line["proxy_max_min"] is not None and line["proxy_max_min"] >= TARGET_AGREEMENT, "candidate below target")
        for confirmation in row["multiprime_confirmation"]:
            require(len(confirmation["prime_results"]) == 4, "bad confirmation prime count")
    require(record["proof_status"] in {"CANDIDATE", "TESTED_QUOTIENT_LINES_NO_A327"}, "bad proof status")
    if record["proof_status"] == "TESTED_QUOTIENT_LINES_NO_A327":
        require(candidate_count == 0, "negative status with retained line candidate")
    if record["line_search"]["proxy_line_candidates"] > 0:
        require(record["exact_audit"]["triggered"] is True, "candidate should trigger exact audit flag")
    return {
        "status": "PASS",
        "systems_tested": len(systems),
        "anchors_tested": line_search["anchors_tested"],
        "quotient_directions_tested": line_search["quotient_directions_tested"],
        "lambda_values_tested": line_search["lambda_values_tested"],
        "proxy_line_candidates": line_search["proxy_line_candidates"],
        "best_capacity_upper_bound": line_search["best_capacity_upper_bound"],
        "best_proxy_max_min": line_search["best_proxy_max_min"],
        "best_six_class_dominance": line_search["best_six_class_dominance"],
        "best_failure_mode": line_search["best_failure_mode"],
        "proof_status": record["proof_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "PASS: M1 a=327 collapse quotient line search "
            f"({result['lambda_values_tested']} lambda evaluations)"
        )


if __name__ == "__main__":
    main()
