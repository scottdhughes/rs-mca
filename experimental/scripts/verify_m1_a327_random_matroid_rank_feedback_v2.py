#!/usr/bin/env python3
"""Verify the M1 a=327 random-matroid rank-feedback v2 ledger."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_random_matroid_rank_feedback_v2.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_random_matroid_rank_feedback_v2.md")

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
    "RANK_FEEDBACK_FORCED_IDENTITY",
    "RANK_FEEDBACK_LOW_FUNCTIONAL_SPAN",
    "RANK_FEEDBACK_DIAGONAL_ANNIHILATOR",
    "RANK_FEEDBACK_PROXY_FULL_RANK",
    "RANK_FEEDBACK_PROXY_NULLITY_POSITIVE",
    "RANK_FEEDBACK_FORCED_PAIR_EQUALITY",
    "RANK_FEEDBACK_EXACT_CANDIDATE",
    "RANK_FEEDBACK_PROXY_NOT_RUN",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify_candidate(candidate: dict[str, Any]) -> None:
    require(candidate["support_vector"] == [TARGET_AGREEMENT] * 7, "candidate support mismatch")
    require(candidate["pair7_counts"] == [204, 204, 204, 204, 204], "candidate pair7 mismatch")
    require(candidate["max_pair_count"] <= 255, "candidate pair cap violated")
    require(candidate["forced_functional_identities"] == 0, "best candidate has forced identity")
    require(candidate["functional_span_rank"] == 6, "best candidate does not repair span rank")
    require(candidate["annihilator_dimension"] == 0, "best candidate has annihilator")
    require(candidate["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(candidate["proxy_rank"] == candidate["best_q_variable_count"], "best proxy is not full rank")
    require(candidate["proxy_nullity"] == 0, "unexpected proxy nullity")
    require(candidate["best_failure_mode"] == "RANK_FEEDBACK_PROXY_FULL_RANK", "wrong best failure")


def verify_coordinate_ledger(candidate: dict[str, Any]) -> None:
    coords = candidate["coordinate_classes"]
    require(len(coords) == 512, "bad coordinate count")
    supports = [0] * 7
    pair_counts = {f"P{i}{j}": 0 for i in range(1, 8) for j in range(i + 1, 8)}
    selected_sizes = Counter()
    for coord in coords:
        members = [int(value) for value in coord["members"]]
        selected_sizes[str(len(members))] += 1
        for witness in members:
            supports[witness - 1] += 1
        for left in range(1, 8):
            for right in range(left + 1, 8):
                if left in members and right in members:
                    pair_counts[f"P{left}{right}"] += 1
    require(supports == candidate["support_vector"], "support ledger mismatch")
    require(max(pair_counts.values()) == candidate["max_pair_count"], "pair max mismatch")
    require(candidate["pair7_counts"] == [pair_counts[label] for label in ["P17", "P27", "P37", "P47", "P57"]], "pair7 ledger mismatch")
    require(candidate["selected_class_size_counts"] == dict(selected_sizes), "class size ledger mismatch")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "3d6bfd4", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_functional_lift"]
    require(previous["template_id"] == "random_matroid_seeded_0_m6", "wrong source template")
    require(previous["functional_classes"] == 35, "wrong source functional count")
    require(previous["functional_span_rank"] == 5, "wrong source span rank")
    require(previous["best_matrix_shape"] == [1211, 714], "wrong source matrix shape")
    require(previous["proxy_rank"] == 714, "wrong source proxy rank")
    require(previous["proxy_nullity"] == 0, "wrong source proxy nullity")
    require(previous["best_failure_mode"] == "RANDOM_MATROID_FUNC_LIFT_EXACT_TIMEOUT", "wrong source failure")

    search = record["rank_feedback_search"]
    require(search["templates_tested"] == 7, "wrong template count")
    require(search["systems_tested"] == 14, "wrong system count")
    require(search["proxy_cases_tested"] == 6, "wrong proxy case count")
    require(search["proxy_positive_candidates"] == 0, "unexpected proxy-positive candidate")
    require(search["best_template_id"] == "random_matroid_feedback_seed_1_m6", "wrong best template")
    require(search["best_assignment_strategy"] == "sorted_block", "wrong best assignment")
    require(search["best_functional_span_rank"] == 6, "wrong best span rank")
    require(search["best_proxy_rank"] == 1086, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_failure_mode"] == "RANK_FEEDBACK_PROXY_FULL_RANK", "wrong search failure")
    require(set(search["failure_counts"]).issubset(ALLOWED_FAILURES), "unexpected failure label")

    candidates = search["candidates"]
    require(len(candidates) == search["systems_tested"], "candidate count mismatch")
    require(sum(1 for row in candidates if row["proxy_rank"] is not None) == search["proxy_cases_tested"], "proxy count mismatch")
    require(sum(1 for row in candidates if row["best_failure_mode"] == "RANK_FEEDBACK_PROXY_FULL_RANK") == 6, "full-rank count mismatch")
    require(sum(1 for row in candidates if row["best_failure_mode"] == "RANK_FEEDBACK_DIAGONAL_ANNIHILATOR") == 4, "diagonal count mismatch")
    require(sum(1 for row in candidates if row["best_failure_mode"] == "RANK_FEEDBACK_PROXY_NOT_RUN") == 4, "not-run count mismatch")

    best = record["best_candidate"]
    verify_candidate(best)
    verify_coordinate_ledger(best)
    require(record["exact_audit"]["run"] is False, "unexpected exact audit")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "random_matroid_feedback_seed_1_m6",
        "functional span rank = 6",
        "1086 / 0",
        "GF(12289)",
        "RANK_FEEDBACK_PROXY_NOT_RUN",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "proxy_cases_tested": search["proxy_cases_tested"],
        "proxy_positive_candidates": search["proxy_positive_candidates"],
        "best_template_id": search["best_template_id"],
        "best_proxy_rank": search["best_proxy_rank"],
        "best_proxy_nullity": search["best_proxy_nullity"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 random-matroid rank-feedback v2 (status={result['proof_status']})")


if __name__ == "__main__":
    main()
