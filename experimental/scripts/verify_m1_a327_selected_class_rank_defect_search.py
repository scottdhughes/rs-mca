#!/usr/bin/env python3
"""Verify the M1 a=327 selected-class rank-defect search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_selected_class_rank_defect_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_selected_class_rank_defect_search.md")

N = 512
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
VARIABLES = (LIST_SIZE - 1) * K
QUOTIENT_EQUATIONS = LIST_SIZE * TARGET_AGREEMENT - N
PAIR_INDICES = [(i, j) for i in range(1, LIST_SIZE + 1) for j in range(i + 1, LIST_SIZE + 1)]
PAIR_LABELS = [f"P{i}{j}" for i, j in PAIR_INDICES]
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]
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
    "RANK_DEFECT_RS_CAP_FAIL",
    "RANK_DEFECT_SUPPORT_FAIL",
    "RANK_DEFECT_PAIR7_FAIL",
    "RANK_DEFECT_PROXY_FULL_RANK",
    "RANK_DEFECT_PROXY_PENDING",
    "RANK_DEFECT_PROXY_POSITIVE",
    "RANK_DEFECT_EXACT_NULLITY_ZERO",
    "RANK_DEFECT_FORCED_PAIR_EQUALITY",
    "RANK_DEFECT_EXACT_CANDIDATE",
    "RANK_DEFECT_TIMEOUT",
    "RANK_DEFECT_COUNT_TARGET",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def contains(mask: int, witness: int) -> bool:
    return bool(mask & (1 << (witness - 1)))


def verify_candidate(row: dict[str, Any], require_coordinates: bool) -> None:
    require(row["best_failure_mode"] in ALLOWED_FAILURES, "bad candidate failure mode")
    require(row["supports"] == [TARGET_AGREEMENT] * LIST_SIZE, "bad supports")
    require(max(row["pair_counts"].values()) <= PAIR_CAP, "pair cap violated")
    require(row["max_pair_count"] == max(row["pair_counts"].values()), "bad max pair")
    require(row["pair7_counts"] == [row["pair_counts"][label] for label in PAIR7_PAIR_LABELS], "bad pair7")
    require(min(row["pair7_counts"]) >= PAIR7_LOWER, "pair7 too low")
    require(row["matrix_shape"] == [QUOTIENT_EQUATIONS, VARIABLES], "bad proxy matrix shape")
    if row["proxy_rank"] is not None:
        require(row["proxy_rank"] + row["proxy_nullity"] == VARIABLES, "bad proxy rank/nullity")
    if require_coordinates:
        coords = row["coordinate_classes"]
        require(len(coords) == N, "bad coordinate count")
        supports = [0] * LIST_SIZE
        pair_counts = {label: 0 for label in PAIR_LABELS}
        equations = 0
        for coord in coords:
            mask = int(coord["mask"])
            members = {int(value) for value in coord["members"]}
            require(members == {idx for idx in range(1, LIST_SIZE + 1) if contains(mask, idx)}, "bad members")
            equations += len(members) - 1
            for witness in members:
                supports[witness - 1] += 1
            for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
                if pair[0] in members and pair[1] in members:
                    pair_counts[label] += 1
        require(supports == row["supports"], "coordinate supports mismatch")
        require(pair_counts == row["pair_counts"], "coordinate pair counts mismatch")
        require(equations == QUOTIENT_EQUATIONS, "coordinate equation count mismatch")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "7e7439a", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    target = record["rank_defect_target"]
    require(target["variables"] == VARIABLES, "bad variable count")
    require(target["selected_incidences"] == LIST_SIZE * TARGET_AGREEMENT, "bad selected incidence count")
    require(target["quotient_equations"] == QUOTIENT_EQUATIONS, "bad quotient equation count")
    require(target["rank_threshold_for_lift"] == VARIABLES - 1, "bad rank threshold")
    require(target["required_row_dependencies_for_nullity"] == QUOTIENT_EQUATIONS - (VARIABLES - 1), "bad dependency count")

    search = record["search"]
    require(search["systems_tested"] == len(search["candidates"]), "bad candidate count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad search failure")
    for row in search["candidates"]:
        verify_candidate(row, require_coordinates=True)
    if record["best_candidate"] is not None:
        verify_candidate(record["best_candidate"], require_coordinates=True)

    exact = record["exact_audit"]
    require(exact["best_failure_mode"] in ALLOWED_FAILURES, "bad exact failure")
    if exact["run"]:
        require(exact["matrix_shape"] == [QUOTIENT_EQUATIONS, VARIABLES], "bad exact matrix shape")
        require(exact["rank"] + exact["nullity"] == VARIABLES, "bad exact rank/nullity")

    candidate = record["candidate"]
    if candidate["constructed"]:
        require(candidate["seven_distinct"] is True, "constructed candidate is not distinct")
        require(candidate["agreement_vector"] is not None, "missing agreement vector")
        require(min(candidate["agreement_vector"]) >= TARGET_AGREEMENT, "candidate agreement too low")

    for phrase in [
        "rank defect",
        "1536 variables",
        "1777 equations",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "proxy_rank_defect_candidates": search["proxy_rank_defect_candidates"],
        "best_proxy_rank": search["best_proxy_rank"],
        "best_proxy_nullity": search["best_proxy_nullity"],
        "best_failure_mode": exact["best_failure_mode"] or search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 selected-class rank-defect search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
