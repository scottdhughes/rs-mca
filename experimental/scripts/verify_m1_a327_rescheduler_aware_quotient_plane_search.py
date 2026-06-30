#!/usr/bin/env python3
"""Verifier for the M1 a=327 rescheduler-aware quotient-plane search."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_rescheduler_aware_quotient_plane_search.json")
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
    "PLANE_CAPACITY_LOSS",
    "PLANE_COLLAPSE_RETURNS",
    "PLANE_REDUCED_CAPACITY_UNSCHEDULED",
    "PLANE_LOW_RESCHEDULE",
    "PLANE_BALANCE_IMPROVES",
    "PLANE_PROXY_CANDIDATE",
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
    require(record["source_commit"] == "ad3d73a", "wrong source commit")
    require(record["construction_mode"] == "rescheduler_aware_quotient_plane_search", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")
    baseline = record["line_baseline"]
    require(baseline["best_capacity_upper_bound"] == 403, "wrong line capacity baseline")
    require(baseline["best_proxy_max_min"] == 259, "wrong line max-min baseline")
    require(baseline["best_six_class_dominance"] == 2, "wrong line dominance baseline")
    lines = record["lines"]
    search = record["plane_search"]
    require(search["lines_tested"] == len(lines) > 0, "bad lines count")
    require(search["second_directions_tested"] == sum(row["second_directions_tested"] for row in lines), "bad direction count")
    require(search["lambda_mu_pairs_tested"] == sum(row["lambda_mu_pairs_tested"] for row in lines), "bad pair count")
    require(search["assignment_solves"] == sum(row["assignment_solves"] for row in lines), "bad assignment count")
    candidate_count = 0
    for row in lines:
        require(row["lambda_mu_pairs_tested"] == row["second_directions_tested"] * row["mu_values_per_direction"], "bad row pair count")
        for plane in row["retained_planes"]:
            require(plane["failure_mode"] in ALLOWED_FAILURES, f"bad plane failure {plane['failure_mode']}")
            if plane["failure_mode"] == "PLANE_PROXY_CANDIDATE":
                candidate_count += 1
                require(plane["proxy_max_min"] is not None and plane["proxy_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(record["proof_status"] in {"CANDIDATE", "TESTED_QUOTIENT_PLANES_NO_A327"}, "bad proof status")
    if record["proof_status"] == "TESTED_QUOTIENT_PLANES_NO_A327":
        require(candidate_count == 0, "negative status with retained candidate")
    if search["proxy_plane_candidates"] > 0:
        require(record["exact_audit"]["triggered"] is True, "candidate should trigger exact audit flag")
    return {
        "status": "PASS",
        "lines_tested": search["lines_tested"],
        "second_directions_tested": search["second_directions_tested"],
        "lambda_mu_pairs_tested": search["lambda_mu_pairs_tested"],
        "assignment_solves": search["assignment_solves"],
        "proxy_plane_candidates": search["proxy_plane_candidates"],
        "best_capacity_upper_bound": search["best_capacity_upper_bound"],
        "best_proxy_max_min": search["best_proxy_max_min"],
        "best_six_class_dominance": search["best_six_class_dominance"],
        "best_failure_mode": search["best_failure_mode"],
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
            "PASS: M1 a=327 rescheduler-aware quotient-plane search "
            f"({result['lambda_mu_pairs_tested']} plane evaluations)"
        )


if __name__ == "__main__":
    main()
