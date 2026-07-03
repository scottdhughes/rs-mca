#!/usr/bin/env python3
"""Verify the M1 a=327 low-rank template exact-audit ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_exact_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_lowrank_template_exact_audit.md")

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
    "LOWRANK_EXACT_TIMEOUT",
    "LOWRANK_EXACT_FULL_RANK",
    "LOWRANK_EXACT_NULLITY_POSITIVE",
    "LOWRANK_FORCED_PAIR_EQUALITY",
    "LOWRANK_PAIR_PROJECTIONS_CLEAR",
    "LOWRANK_EXACT_CANDIDATE",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def contains(mask: int, witness: int) -> bool:
    return bool(mask & (1 << (witness - 1)))


def verify_coordinate_ledgers(record: dict[str, Any]) -> None:
    coords = record["coordinate_classes"]
    proxy = record["proxy_candidate"]
    require(len(coords) == N, "bad coordinate count")
    supports = [0] * LIST_SIZE
    pair_counts = {label: 0 for label in PAIR_LABELS}
    row_count = 0
    for coord in coords:
        mask = int(coord["mask"])
        members = {int(value) for value in coord["members"]}
        require(members == {idx for idx in range(1, LIST_SIZE + 1) if contains(mask, idx)}, "bad coordinate members")
        row_count += len(members) - 1
        for witness in members:
            supports[witness - 1] += 1
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if pair[0] in members and pair[1] in members:
                pair_counts[label] += 1
    require(supports == proxy["support_vector"], "support vector mismatch")
    require(pair_counts == proxy["pair_count_matrix"], "pair count mismatch")
    require(proxy["pair7_counts"] == [pair_counts[label] for label in PAIR7_PAIR_LABELS], "pair7 mismatch")
    require(max(pair_counts.values()) <= PAIR_CAP, "pair cap violated")
    require(min(proxy["pair7_counts"]) >= PAIR7_LOWER, "pair7 too low")
    require(row_count == len(record["row_specs"]), "row spec count mismatch")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "e56f3ad", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    proxy = record["proxy_candidate"]
    require(proxy["template_id"] == "mixed_rank6", "wrong template")
    require(proxy["template_dimension"] == 6, "wrong template dimension")
    require(proxy["effective_cost"] == 1533, "wrong effective cost")
    require(proxy["variable_count"] == 1536, "wrong variable count")
    require(proxy["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(proxy["proxy_rank"] == 1280, "wrong proxy rank")
    require(proxy["proxy_nullity"] == 256, "wrong proxy nullity")
    require(proxy["raw_row_count"] >= proxy["basis_row_count"], "bad row count compression")
    require(proxy["basis_row_count"] == proxy["effective_cost"], "basis row count mismatch")
    verify_coordinate_ledgers(record)

    exact = record["exact_audit"]
    require(exact["best_failure_mode"] in ALLOWED_FAILURES, "bad exact failure")
    if exact["rank"] is not None:
        require(exact["matrix_shape"] is not None, "missing matrix shape")
        require(exact["matrix_shape"][0] == proxy["basis_row_count"], "unexpected exact row count")
        require(exact["rank"] + exact["nullity"] == proxy["variable_count"], "bad rank/nullity")
    projection = record["pair_projection_test"]
    require(projection["pairs_tested"] == 21, "bad projection pair count")
    if projection["projection_rank_by_pair"] is not None:
        require(set(projection["projection_rank_by_pair"]) == set(PAIR_LABELS), "bad projection labels")

    candidate = record["candidate"]
    if candidate["constructed"]:
        require(candidate["seven_distinct"] is True, "candidate not seven distinct")
        require(candidate["agreement_vector"] is not None, "missing agreement vector")
        require(min(candidate["agreement_vector"]) >= TARGET_AGREEMENT, "agreement too low")

    for phrase in [
        "mixed_rank6",
        "GF(17^32)",
        "pair-projection",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "template_id": proxy["template_id"],
        "proxy_rank": proxy["proxy_rank"],
        "proxy_nullity": proxy["proxy_nullity"],
        "exact_rank": exact["rank"],
        "exact_nullity": exact["nullity"],
        "best_failure_mode": exact["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 low-rank template exact audit (status={result['proof_status']})")


if __name__ == "__main__":
    main()
