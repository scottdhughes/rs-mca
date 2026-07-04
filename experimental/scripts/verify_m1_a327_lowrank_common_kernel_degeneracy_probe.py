#!/usr/bin/env python3
"""Verify the M1 a=327 low-rank common-kernel degeneracy probe."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_lowrank_common_kernel_degeneracy_probe.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_lowrank_common_kernel_degeneracy_probe.md")

TARGET_AGREEMENT = 327
PAIR_COUNT = 21
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "global obstruction outside the tested low-rank templates",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "fc61a75", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / LOWRANK_TEMPLATE_COMMON_KERNEL_DEGENERACY / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )
    probes = record["candidate_probes"]
    require(len(probes) == 2, "expected two candidate probes")
    require(record["probe"]["degenerate_candidates"] == 2, "not all candidates degenerate")
    for probe in probes:
        label = probe["source_label"]
        require(probe["template_dimension"] == 6, f"{label}: wrong template dimension")
        require(probe["functional_span_rank"] == 5, f"{label}: expected span rank 5")
        require(probe["common_kernel_dimension"] == 1, f"{label}: expected common kernel dimension 1")
        require(probe["proxy_rank"] == probe["expected_common_kernel_artifact_rank"], f"{label}: proxy rank mismatch")
        require(probe["proxy_nullity"] == probe["expected_common_kernel_artifact_nullity"], f"{label}: proxy nullity mismatch")
        require(probe["common_kernel_artifact_rank_match"] is True, f"{label}: artifact rank did not match")
        require(probe["cooccurrence_graph_connected"] is True, f"{label}: cooccurrence graph disconnected")
        require(len(probe["forced_equal_pairs_on_common_kernel"]) == PAIR_COUNT, f"{label}: not all pairs forced")
        require(probe["all_pairs_forced_on_common_kernel"] is True, f"{label}: all-pairs forced flag false")
        require(probe["degeneracy_detected"] is True, f"{label}: degeneracy not detected")
        require(probe["failure_mode"] == "LOWRANK_TEMPLATE_COMMON_KERNEL_DEGENERACY", f"{label}: wrong failure")
    for phrase in [
        "common-kernel degeneracy",
        "1280 / 256",
        "functional span rank is 5",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")
    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "candidates_tested": len(probes),
        "degenerate_candidates": record["probe"]["degenerate_candidates"],
        "failure_mode": record["probe"]["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 low-rank common-kernel degeneracy probe")


if __name__ == "__main__":
    main()
