#!/usr/bin/env python3
"""Verifier for capacity-slack split selector."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_capacity_slack_split_selector.json")
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
    "NO_SPLIT_SAFE_COORDINATES",
    "SPLIT_SELECTOR_CAPACITY_LOSS",
    "SPLIT_SELECTOR_PAIR57_LOSS",
    "SPLIT_SELECTOR_PAIR27_37_STALLS",
    "SPLIT_SELECTOR_COLLAPSE_NOT_REDUCED",
    "SPLIT_SELECTOR_LOW_RESCHEDULE",
    "SPLIT_SELECTOR_EXACT_CANDIDATE",
    "SPLIT_SELECTOR_INCONSISTENT",
    "SPLIT_SELECTOR_TIMEOUT",
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
    require(record["source_commit"] == "395e7e0", "wrong source commit")
    require(record["construction_mode"] == "capacity_slack_split_selector", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["best_pair_B_values"] == [1024, 593, 592, 1024, 1024], "wrong baseline pair values")
    require(baseline["best_capacity_upper_bound"] == 315, "wrong baseline capacity")
    require(baseline["best_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong baseline collapse")
    require(
        baseline["failure_counts"] == {"SPLIT_CAPACITY_LOSS": 27, "SPLIT_DESTROYS_PAIR57": 18},
        "wrong baseline failure counts",
    )

    ledger = record["capacity_slack_ledger"]
    require(ledger["coordinates"] == 512, "wrong coordinate count")
    require(isinstance(ledger["coordinate_rows"], list), "coordinate rows missing")
    require(len(ledger["coordinate_rows"]) == 512, "coordinate row length mismatch")
    require(ledger["capacity_critical_count"] == 512, "wrong capacity-critical count")
    require(ledger["pair57_critical_count"] == 512, "wrong pair57-critical count")
    require(ledger["split_safe_count"] == 860, "wrong split-safe count")
    require(len(ledger["candidate_split_rows"]) == 96, "wrong retained candidate split row count")
    require(
        {row["split_safe_score"] for row in ledger["candidate_split_rows"]} == {0},
        "unexpected retained split-safe score range",
    )

    selector = record["split_selector"]
    require(selector["exact_field"] == "GF(17^32)", "wrong exact field")
    require(selector["base_system"] == "scalable_pairclass_overlap_all_extension96", "wrong base system")
    require(selector["split_location_budgets"] == [8, 16, 32], "wrong budgets")
    require(
        selector["selectors"] == ["greedy", "pair27_weighted", "pair37_weighted", "capacity_safe"],
        "wrong selectors",
    )
    require(selector["free_patterns"] == ["d2_first_free", "d2_first4_free", "d2_even_sparse"], "wrong free patterns")
    require(selector["systems_tested"] == 12, "wrong system count")
    require(selector["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(selector["timeouts"] == 0, "unexpected timeout count")
    require(selector["split_rows_tested"] == 12, "wrong split row count")
    require(selector["exact_vectors_constructed"] == 36, "wrong exact vector count")
    require(selector["capacity_preserving_vectors"] == 0, "wrong capacity-preserving count")
    require(selector["pair57_preserving_vectors"] == 36, "wrong pair57-preserving count")
    require(selector["pair27_37_improved_vectors"] == 36, "wrong pair27/37-improved count")
    require(selector["collapse_reduced_vectors"] == 36, "wrong collapse-reduced count")
    require(selector["best_pair_B_values"] == [1024, 593, 592, 1024, 1024], "wrong best pair values")
    require(selector["best_capacity_upper_bound"] == 315, "wrong best capacity")
    require(selector["best_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong best collapse")
    require(selector["best_exact_max_min"] is None, "unexpected exact max-min")
    require(selector["best_failure_mode"] == "SPLIT_SELECTOR_CAPACITY_LOSS", "wrong best failure")
    require(selector["failure_mode_counts"] == {"SPLIT_SELECTOR_CAPACITY_LOSS": 36}, "wrong failure counts")

    exact_candidate_count = 0
    vector_count = 0
    for result in selector["results"]:
        require(result["failure_mode"] in ALLOWED_FAILURES, f"bad result failure {result['failure_mode']}")
        for row in result.get("vector_results", []):
            vector_count += 1
            require(row["failure_mode"] in ALLOWED_FAILURES, f"bad vector failure {row['failure_mode']}")
            if row["failure_mode"] == "SPLIT_SELECTOR_EXACT_CANDIDATE":
                exact_candidate_count += 1
                require(row["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(vector_count == selector["exact_vectors_constructed"], "vector count mismatch")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "split_safe_count": ledger["split_safe_count"],
        "systems_tested": selector["systems_tested"],
        "exact_vectors_constructed": selector["exact_vectors_constructed"],
        "capacity_preserving_vectors": selector["capacity_preserving_vectors"],
        "pair57_preserving_vectors": selector["pair57_preserving_vectors"],
        "pair27_37_improved_vectors": selector["pair27_37_improved_vectors"],
        "best_pair_B_values": selector["best_pair_B_values"],
        "best_capacity_upper_bound": selector["best_capacity_upper_bound"],
        "best_collapse_pattern": selector["best_collapse_pattern"],
        "best_failure_mode": selector["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 capacity-slack split selector ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
