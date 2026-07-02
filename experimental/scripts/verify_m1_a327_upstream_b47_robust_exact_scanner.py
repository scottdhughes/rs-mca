#!/usr/bin/env python3
"""Verify the M1 a=327 upstream B47-robust exact scanner ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_upstream_b47_robust_exact_scanner.json")
LEDGER_PATH = Path("experimental/data/m1_a327_upstream_b47_robust_skeleton_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_upstream_b47_robust_exact_scanner.md")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
SYSTEMS_PLANNED = 24
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "global obstruction outside the tested basin",
}
ALLOWED_FAILURES = {
    "UPSTREAM_B47_NOT_ROBUST",
    "UPSTREAM_CAPACITY_NOT_ROBUST",
    "UPSTREAM_PAIR27_37_NOT_ROBUST",
    "UPSTREAM_PAIR57_NOT_ROBUST",
    "UPSTREAM_COLLAPSE_UNCHANGED",
    "UPSTREAM_COLLAPSE_RETURNS",
    "UPSTREAM_SPLIT_RESILIENT_SKELETON",
    "UPSTREAM_LOW_RESCHEDULE",
    "UPSTREAM_EXACT_CANDIDATE",
    "UPSTREAM_TIMEOUT",
    "UPSTREAM_INCONSISTENT",
    "UPSTREAM_EXACT_SCANNER_PENDING",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(record: dict[str, Any], ledger: dict[str, Any], note_text: str) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "0500d07", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    source = record["upstream_b47_ledger"]
    ledger_search = ledger["upstream_b47_search"]
    require(source["source_skeletons_analyzed"] == ledger_search["source_skeletons_analyzed"], "source count mismatch")
    require(source["split_probe_vectors"] == ledger_search["split_probe_vectors"], "source probe mismatch")
    require(source["split_resilient_skeletons"] == 0, "source ledger should have no resilient skeleton")
    require(source["best_failure_mode"] == "UPSTREAM_B47_NOT_ROBUST", "wrong source failure")

    scan = record["exact_scanner"]
    require(scan["systems_planned"] == SYSTEMS_PLANNED, "wrong planned system count")
    require(0 <= scan["systems_tested"] <= SYSTEMS_PLANNED, "bad tested count")
    require(0 <= scan["timeouts"] <= scan["systems_tested"], "bad timeout count")
    require(0 <= scan["exact_vectors_constructed"] <= scan["systems_tested"], "bad exact vector count")
    require(scan["split_probe_vectors"] >= 0, "bad probe count")
    require(scan["split_resilient_skeletons"] <= scan["systems_tested"], "too many resilient skeletons")
    require(scan["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure mode")
    require(len(scan["candidate_families"]) == 6, "wrong family count")
    require(scan["budgets"] == [1, 2, 4, 8], "wrong budgets")
    require(scan["split_probe_families"] == ["split_4_from_157", "split_14_vs_57", "split_1_from_457"], "wrong probes")

    result_count = len(scan.get("results", []))
    require(result_count == scan["systems_tested"], "result count mismatch")
    for result in scan.get("results", []):
        require(result["failure_mode"] in ALLOWED_FAILURES, "bad case failure")
        if result.get("pre_split") is not None:
            pairs = result["pre_split"]["pair_B_values"]
            require(len(pairs) == 5, "bad pre-split pair vector")
        for probe in result.get("probe_results", []):
            if probe.get("pair_B_values") is not None:
                pairs = probe["pair_B_values"]
                require(len(pairs) == 5, "bad probe pair vector")
                if probe.get("failure_mode") == "UPSTREAM_EXACT_CANDIDATE":
                    require(probe.get("exact_max_min", -1) >= TARGET_AGREEMENT, "candidate below target")
                    require(probe.get("distinct_codewords") is True, "candidate not distinct")
                    require(probe["capacity_upper_bound"] >= TARGET_AGREEMENT, "candidate low capacity")
                    require(pairs[1] >= PAIR_TARGET and pairs[2] >= PAIR_TARGET, "candidate B27/B37 low")
                    require(pairs[3] >= PAIR_TARGET and pairs[4] >= PAIR_TARGET, "candidate B47/B57 low")

    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if scan["systems_tested"] < SYSTEMS_PLANNED:
        require(record["proof_status"] == "PARTIAL", "partial run should be PARTIAL")

    for phrase in [
        "not an MCA row",
        "not a protocol claim",
        "not a public-board update",
        "not a global obstruction theorem",
        "split-resilient before claiming progress",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": scan["systems_tested"],
        "exact_vectors_constructed": scan["exact_vectors_constructed"],
        "split_probe_vectors": scan["split_probe_vectors"],
        "split_resilient_skeletons": scan["split_resilient_skeletons"],
        "best_pre_split_capacity": scan["best_pre_split_capacity"],
        "best_pre_split_pair_B_values": scan["best_pre_split_pair_B_values"],
        "best_probe_split_capacity": scan["best_probe_split_capacity"],
        "best_probe_split_pair_B_values": scan["best_probe_split_pair_B_values"],
        "best_robustness_score": scan["best_robustness_score"],
        "best_failure_mode": scan["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH), load_json(LEDGER_PATH), NOTE_PATH.read_text())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 upstream B47 exact scanner ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
