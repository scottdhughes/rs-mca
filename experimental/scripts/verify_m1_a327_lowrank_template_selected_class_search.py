#!/usr/bin/env python3
"""Verify the M1 a=327 low-rank template selected-class ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_selected_class_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_lowrank_template_selected_class_search.md")

N = 512
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
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
    "LOWRANK_TEMPLATE_SUPPORT_FAIL",
    "LOWRANK_TEMPLATE_PAIR_CAP_FAIL",
    "LOWRANK_TEMPLATE_PAIR7_FAIL",
    "LOWRANK_TEMPLATE_COST_TOO_HIGH",
    "LOWRANK_TEMPLATE_PROXY_PENDING",
    "LOWRANK_TEMPLATE_PROXY_FULL_RANK",
    "LOWRANK_TEMPLATE_PROXY_POSITIVE",
    "LOWRANK_TEMPLATE_EXACT_NULLITY_ZERO",
    "LOWRANK_TEMPLATE_FORCED_PAIR_EQUALITY",
    "LOWRANK_TEMPLATE_EXACT_CANDIDATE",
    "LOWRANK_TEMPLATE_TIMEOUT",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def contains(mask: int, witness: int) -> bool:
    return bool(mask & (1 << (witness - 1)))


def verify_candidate(row: dict[str, Any]) -> None:
    require(row["best_failure_mode"] in ALLOWED_FAILURES, "bad candidate failure mode")
    m = int(row["template_dimension"])
    require(row["variable_count"] == K * m, "bad variable count")
    require(row["total_effective_cost"] >= 0, "bad effective cost")
    require(row["cost_margin"] == row["variable_count"] - row["total_effective_cost"], "bad cost margin")
    require(row["support_vector"] == [TARGET_AGREEMENT] * LIST_SIZE, "bad supports")
    require(max(row["pair_count_matrix"].values()) <= PAIR_CAP, "pair cap violated")
    require(row["max_pair_count"] == max(row["pair_count_matrix"].values()), "bad max pair")
    require(row["pair7_counts"] == [row["pair_count_matrix"][label] for label in PAIR7_PAIR_LABELS], "bad pair7")
    require(min(row["pair7_counts"]) >= PAIR7_LOWER, "pair7 too low")
    if row["proxy_rank"] is not None:
        require(row["proxy_rank"] + row["proxy_nullity"] == row["variable_count"], "bad proxy rank/nullity")
    coords = row["coordinate_classes"]
    require(len(coords) == N, "bad coordinate count")
    supports = [0] * LIST_SIZE
    pairs = {label: 0 for label in PAIR_LABELS}
    for coord in coords:
        mask = int(coord["mask"])
        members = {int(value) for value in coord["members"]}
        require(members == {idx for idx in range(1, LIST_SIZE + 1) if contains(mask, idx)}, "bad members")
        for witness in members:
            supports[witness - 1] += 1
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if pair[0] in members and pair[1] in members:
                pairs[label] += 1
    require(supports == row["support_vector"], "coordinate supports mismatch")
    require(pairs == row["pair_count_matrix"], "coordinate pairs mismatch")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "b41747d", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_rank_defect_search"]
    require(previous["failure_mode"] == "RANK_DEFECT_PROXY_FULL_RANK", "wrong previous failure")
    search = record["lowrank_template_search"]
    require(search["systems_tested"] == len(search["candidates"]), "bad candidate count")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad search failure")
    for candidate in search["candidates"]:
        verify_candidate(candidate)
    if record["best_candidate"] is not None:
        verify_candidate(record["best_candidate"])

    exact = record["exact_audit"]
    require(exact["best_failure_mode"] in ALLOWED_FAILURES, "bad exact failure")
    if exact["run"]:
        require(exact["rank"] + exact["nullity"] == search["best_variable_count"], "bad exact rank/nullity")

    candidate = record["candidate"]
    if candidate["constructed"]:
        require(candidate["seven_distinct"] is True, "constructed candidate not distinct")
        require(candidate["agreement_vector"] is not None, "missing agreement vector")
        require(min(candidate["agreement_vector"]) >= TARGET_AGREEMENT, "candidate agreement too low")

    for phrase in [
        "low-rank coefficient template",
        "affine rank",
        "proxy field",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "templates_tested": search["templates_tested"],
        "systems_tested": search["systems_tested"],
        "proxy_positive_candidates": search["proxy_positive_candidates"],
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
        print(f"PASS: M1 a=327 low-rank template selected-class search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
