#!/usr/bin/env python3
"""Verify the M1 a=327 low-rank functional-basis extraction ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_lowrank_functional_basis_extraction.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_lowrank_functional_basis_extraction.md")

TARGET_AGREEMENT = 327
PAIR_LABELS = [f"P{i}{j}" for i in range(1, 8) for j in range(i + 1, 8)]
ALL_PAIRS = [[i, j] for i in range(1, 8) for j in range(i + 1, 8)]
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    None,
    "FUNC_BASIS_FORCED_SPAN_COLLAPSES",
    "FUNC_BASIS_PAIR_FORCED_BY_FORCED_IDENTITIES",
    "FUNC_BASIS_NO_INDEPENDENT_BASIS",
    "FUNC_BASIS_MATRIX_TIMEOUT",
    "FUNC_BASIS_NULLITY_ZERO",
    "FUNC_BASIS_FORCED_PAIR_EQUALITY",
    "FUNC_BASIS_RAW_ROW_VIOLATION",
    "FUNC_BASIS_DEGENERATE_SAMPLE",
    "FUNC_BASIS_EXACT_CANDIDATE",
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
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "edf8a8c", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    baseline = record["functional_divisibility_baseline"]
    require(baseline["template_id"] == "mixed_rank6", "wrong template")
    require(baseline["template_dimension"] == 6, "wrong template dimension")
    require(baseline["functional_classes"] == 15, "wrong functional class count")
    require(baseline["forced_functional_identities"] == 2, "wrong baseline forced count")
    require(baseline["quotient_variables"] == 2327, "wrong baseline quotient count")
    require(baseline["matrix_shape"] == [3840, 3863], "wrong baseline matrix shape")
    require(baseline["formal_nullity_lower_bound"] == 23, "wrong baseline nullity lower bound")

    reduction = record["forced_identity_reduction"]
    require(reduction["forced_rank"] == 5, "wrong forced rank")
    require(reduction["reduced_template_dimension"] == 1, "wrong reduced template dimension")
    require(reduction["remaining_functional_classes"] == 0, "unexpected remaining functionals")
    require(reduction["zero_projected_functionals"] == 15, "wrong zero-projected count")
    require(reduction["pure_q_kernel_impossible"] is True, "pure-Q injectivity not recorded")
    require(len(reduction["forced_kernel_basis"]) == 1, "wrong forced kernel dimension")

    basis = record["basis_quotient_system"]
    require(basis["bases_tested"] == 0, "unexpected bases tested")
    require(basis["best_failure_mode"] in ALLOWED_FAILURES, "bad basis failure")
    require(basis["best_failure_mode"] == "FUNC_BASIS_PAIR_FORCED_BY_FORCED_IDENTITIES", "wrong failure mode")

    projection = record["pair_projection_test"]
    require(projection["pairs_tested"] == 21, "wrong pair count")
    require(projection["forced_equal_pairs"] == ALL_PAIRS, "not all pairs forced equal")
    require(projection["min_projection_rank"] == 0, "bad min projection rank")
    require(set(projection["projection_rank_by_pair"]) == set(PAIR_LABELS), "bad pair projection labels")
    require(all(value == 0 for value in projection["projection_rank_by_pair"].values()), "unexpected nonzero pair projection")

    candidate = record["candidate"]
    require(candidate["constructed"] is False, "unexpected candidate")
    sage = record["sage_exact_check"]
    require(sage["field"] == "GF(17^32)", "wrong Sage check field")
    if sage["run"]:
        require(sage["forced_rank"] == 5, "Sage forced rank mismatch")
        require(sage["forced_kernel_dimension"] == 1, "Sage forced kernel dimension mismatch")
        require(sage["forced_equal_pairs"] == 21, "Sage forced pair count mismatch")
        require(sage["status"] == "PASS", "Sage exact check did not pass")

    for phrase in [
        "forced-identity saturation",
        "forced rank = 5",
        "all 21 witness pairs",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "forced_rank": reduction["forced_rank"],
        "reduced_template_dimension": reduction["reduced_template_dimension"],
        "forced_equal_pairs": len(projection["forced_equal_pairs"]),
        "best_failure_mode": basis["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 functional-basis extraction (status={result['proof_status']})")


if __name__ == "__main__":
    main()
