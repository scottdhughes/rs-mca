#!/usr/bin/env python3
"""Verifier for the M1 a=327 pair {2,7}/{3,7} exchange audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pair27_37_exchange_obstruction.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
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
    require(record["source_commit"] == "0639865", "wrong source commit")
    require(record["construction_mode"] == "pair27_37_exchange_obstruction", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["d2_split_retained"] == 78, "wrong baseline D2 retained count")
    require(baseline["capacity_preserving_vectors"] == 78, "wrong baseline capacity count")
    require(baseline["low_collapse_capacity_preserving_vectors"] == 78, "wrong baseline low-collapse count")
    require(baseline["best_pair_B_values"] == [1024, 514, 513, 1024, 1024], "wrong baseline pair values")
    require(baseline["best_capacity_upper_bound"] == 366, "wrong baseline capacity")
    require(baseline["best_failure_mode"] == "POST_D2_PAIR7_NOT_REPAIRED", "wrong baseline failure")

    diag = record["pair27_37_diagnostic"]
    require(diag["exact_field"] == "GF(17^32)", "wrong exact field")
    require(diag["vectors_analyzed"] == 78, "wrong vector analysis count")
    require(diag["B27"] == 514, "wrong B27")
    require(diag["B37"] == 513, "wrong B37")
    require(diag["deficit27"] == PAIR_TARGET - 514, "wrong deficit27")
    require(diag["deficit37"] == PAIR_TARGET - 513, "wrong deficit37")
    require(diag["pair27_credit_histogram"] == {"1": 510, "2": 2}, "wrong pair27 histogram")
    require(diag["pair37_credit_histogram"] == {"1": 511, "2": 1}, "wrong pair37 histogram")
    require(diag["critical_coordinates"] == 2, "wrong critical coordinate count")
    require(diag["pair27_credit_coordinates"] == [0, 18], "wrong pair27 credit coordinates")
    require(diag["pair37_credit_coordinates"] == [18], "wrong pair37 credit coordinates")
    require(diag["exchange_graph_feasible"] is False, "exchange graph unexpectedly feasible")
    require(len(diag["retained_vectors"]) == 6, "wrong retained vector count")
    best = diag["best_vector"]
    require(best["capacity_upper_bound"] == 366, "wrong best diagnostic capacity")
    require(best["B27"] == 514 and best["B37"] == 513, "wrong best diagnostic pair values")
    require(best["failure_mode"] == "PAIR27_37_EXCHANGE_INFEASIBLE", "wrong best diagnostic failure")

    repair = record["targeted_repair"]
    require(repair["repair_sets_tested"] == 0, "unexpected repair sets tested")
    require(repair["exact_vectors_constructed"] == 0, "unexpected repair vectors")
    require(repair["B27_repaired_vectors"] == 0, "unexpected B27 repair")
    require(repair["B37_repaired_vectors"] == 0, "unexpected B37 repair")
    require(repair["full_pair_repaired_vectors"] == 0, "unexpected full pair repair")
    require(repair["best_pair_B_values"] == [1024, 514, 513, 1024, 1024], "wrong repair best pair values")
    require(repair["best_failure_mode"] == "PAIR27_37_EXCHANGE_INFEASIBLE", "wrong repair failure")
    require(record["proof_status"] == "EXACT_EXTRACTION_NO_A327", "wrong proof status")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "vectors_analyzed": diag["vectors_analyzed"],
        "B27": diag["B27"],
        "B37": diag["B37"],
        "deficit27": diag["deficit27"],
        "deficit37": diag["deficit37"],
        "critical_coordinates": diag["critical_coordinates"],
        "exchange_graph_feasible": diag["exchange_graph_feasible"],
        "best_failure_mode": repair["best_failure_mode"],
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
            "PASS: M1 a=327 pair27/37 exchange obstruction "
            f"({result['vectors_analyzed']} vectors)"
        )


if __name__ == "__main__":
    main()
