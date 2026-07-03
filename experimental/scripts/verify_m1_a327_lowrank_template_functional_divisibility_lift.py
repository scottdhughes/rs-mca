#!/usr/bin/env python3
"""Verify the M1 a=327 low-rank functional-divisibility ledger."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_functional_divisibility_lift.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_lowrank_template_functional_divisibility_lift.md")

N = 512
K = 256
LIST_SIZE = 7
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
    "FUNC_DIV_TOO_MANY_FUNCTIONALS",
    "FUNC_DIV_FORCED_FUNCTIONAL_IDENTITY",
    "FUNC_DIV_MATRIX_TIMEOUT",
    "FUNC_DIV_NULLITY_ZERO",
    "FUNC_DIV_FORCED_PAIR_EQUALITY",
    "FUNC_DIV_DEGENERATE_SAMPLE",
    "FUNC_DIV_RAW_ROW_VIOLATION",
    "FUNC_DIV_EXACT_CANDIDATE",
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
    raw_rows = 0
    for coord in coords:
        mask = int(coord["mask"])
        members = {int(value) for value in coord["members"]}
        require(members == {idx for idx in range(1, LIST_SIZE + 1) if contains(mask, idx)}, "bad coordinate members")
        raw_rows += len(members) - 1
        for witness in members:
            supports[witness - 1] += 1
        for label, pair in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if pair[0] in members and pair[1] in members:
                pair_counts[label] += 1
    require(raw_rows == proxy["raw_selected_class_rows"], "bad raw row count")
    require(supports == proxy["support_vector"], "support vector mismatch")
    require(pair_counts == proxy["pair_count_matrix"], "pair count mismatch")
    require(proxy["pair7_counts"] == [pair_counts[label] for label in PAIR7_PAIR_LABELS], "pair7 mismatch")
    require(max(pair_counts.values()) <= PAIR_CAP, "pair cap violated")
    require(min(proxy["pair7_counts"]) >= PAIR7_LOWER, "pair7 too low")


def verify_functional_ledger(record: dict[str, Any]) -> None:
    func = record["functional_divisibility"]
    classes = record["functional_classes_detail"]
    proxy = record["proxy_candidate"]
    require(len(classes) == func["functional_classes"], "functional class count mismatch")
    histogram = Counter(str(row["support_size"]) for row in classes)
    require(dict(sorted(histogram.items(), key=lambda item: int(item[0]))) == func["support_size_histogram"], "histogram mismatch")
    forced = [row for row in classes if row["support_size"] > K - 1]
    require(len(forced) == func["forced_functional_identities"], "forced identity mismatch")
    quotient_variables = sum(max(0, K - int(row["support_size"])) for row in classes)
    require(quotient_variables == func["quotient_variable_count"], "quotient variable mismatch")
    require(func["matrix_shape"] == [K * len(classes), proxy["variable_count"] + quotient_variables], "matrix shape mismatch")
    require(func["formal_nullity_lower_bound"] == max(0, func["matrix_shape"][1] - func["matrix_shape"][0]), "bad formal nullity bound")
    require(func["best_failure_mode"] in ALLOWED_FAILURES, "bad functional failure")
    if func["rank"] is not None:
        require(func["rank"] + func["nullity"] == func["matrix_shape"][1], "bad rank/nullity")
    support_row_sum = sum(int(row["support_size"]) for row in classes)
    require(support_row_sum <= proxy["compressed_basis_rows"], "support row accounting too large")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "64e2fdf", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    proxy = record["proxy_candidate"]
    require(proxy["template_id"] == "mixed_rank6", "wrong template")
    require(proxy["template_dimension"] == 6, "wrong template dimension")
    require(proxy["compressed_matrix_shape"] == [1533, 1536], "wrong compressed matrix shape")
    require(proxy["raw_selected_class_rows"] == 1777, "wrong raw selected-class rows")
    require(proxy["compressed_basis_rows"] == 1533, "wrong compressed row count")
    require(proxy["variable_count"] == 1536, "wrong variable count")
    require(proxy["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(proxy["proxy_rank"] == 1280, "wrong proxy rank")
    require(proxy["proxy_nullity"] == 256, "wrong proxy nullity")
    verify_coordinate_ledgers(record)
    verify_functional_ledger(record)

    candidate = record["candidate"]
    if candidate["constructed"]:
        require(candidate["seven_distinct"] is True, "candidate not seven distinct")
        require(candidate["agreement_vector"] is not None, "missing agreement vector")
        require(min(candidate["agreement_vector"]) >= TARGET_AGREEMENT, "agreement too low")
        require(record["functional_divisibility"]["best_failure_mode"] == "FUNC_DIV_EXACT_CANDIDATE", "bad candidate failure mode")

    for phrase in [
        "functional-divisibility",
        "mixed_rank6",
        "GF(17^32)",
        "raw selected-class",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    func = record["functional_divisibility"]
    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "functional_classes": func["functional_classes"],
        "matrix_shape": func["matrix_shape"],
        "rank": func["rank"],
        "nullity": func["nullity"],
        "best_failure_mode": func["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 functional-divisibility lift (status={result['proof_status']})")


if __name__ == "__main__":
    main()
