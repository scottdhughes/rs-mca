#!/usr/bin/env python3
"""Verify the M1 a=327 random-matroid functional-lift ledger."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_random_matroid_functional_lift.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_random_matroid_functional_lift.md")

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
    None,
    "RANDOM_MATROID_FUNC_LIFT_FORCED_IDENTITY",
    "RANDOM_MATROID_FUNC_LIFT_NO_BASIS",
    "RANDOM_MATROID_FUNC_LIFT_PROXY_FULL_RANK",
    "RANDOM_MATROID_FUNC_LIFT_EXACT_TIMEOUT",
    "RANDOM_MATROID_FUNC_LIFT_NULLITY_ZERO",
    "RANDOM_MATROID_FUNC_LIFT_NULLITY_POSITIVE",
    "RANDOM_MATROID_FUNC_LIFT_FORCED_PAIR_EQUALITY",
    "RANDOM_MATROID_FUNC_LIFT_PAIR_PROJECTIONS_CLEAR",
    "RANDOM_MATROID_FUNC_LIFT_DEGENERATE_SAMPLE",
    "RANDOM_MATROID_FUNC_LIFT_EXACT_CANDIDATE",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify_coordinate_ledger(record: dict[str, Any]) -> None:
    coords = record["coordinate_classes"]
    survivor = record["survivor"]
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
    require(supports == survivor["support_vector"], "support vector mismatch")
    require(pair_counts == survivor["pair_count_matrix"], "pair count mismatch")
    require(survivor["selected_class_size_counts"] == dict(selected_sizes), "selected size mismatch")
    require(max(pair_counts.values()) == survivor["max_pair_count"], "max pair mismatch")
    require(survivor["pair7_counts"] == [pair_counts[label] for label in ["P17", "P27", "P37", "P47", "P57"]], "pair7 mismatch")


def verify_functional_ledger(record: dict[str, Any]) -> None:
    lift = record["functional_lift"]
    classes = record["functional_classes_detail"]
    require(len(classes) == lift["functional_classes"], "functional class count mismatch")
    require(len(classes) == 35, "wrong functional class count")
    histogram = Counter(str(row["support_size"]) for row in classes)
    require(dict(sorted(histogram.items(), key=lambda item: int(item[0]))) == lift["support_size_histogram"], "histogram mismatch")
    require(lift["forced_functional_identities"] == 0, "unexpected forced identity")
    require(lift["functional_span_rank"] == 5, "wrong functional span rank")
    require(lift["annihilator_dimension"] == 1, "wrong annihilator dimension")
    require(lift["basis_profiles_tested"] == 11, "wrong basis profile count")
    require(lift["best_basis_id"] == "max_support_basis", "wrong best basis")
    require(lift["best_matrix_shape"] == [1211, 714], "wrong best matrix shape")
    require(lift["best_q_variable_count"] == 714, "wrong q variable count")
    require(lift["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(lift["proxy_matrix_shape"] == [1211, 714], "wrong proxy shape")
    require(lift["proxy_rank"] == 714, "wrong proxy rank")
    require(lift["proxy_nullity"] == 0, "wrong proxy nullity")
    require(lift["exact_rank_attempted"] is True, "exact rank attempt not recorded")
    require(lift["exact_rank_timeout"] is True, "exact timeout not recorded")
    require(lift["best_failure_mode"] in ALLOWED_FAILURES, "bad failure label")
    require(lift["best_failure_mode"] == "RANDOM_MATROID_FUNC_LIFT_EXACT_TIMEOUT", "wrong failure label")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "68a0780", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    repair = record["forced_identity_repair"]
    require(repair["best_template_id"] == "random_matroid_seeded_0_m6", "wrong repair survivor")
    require(repair["sage_status"] == "PASS", "repair Sage status did not pass")
    require(repair["forced_rank"] == 0, "wrong repair forced rank")
    require(repair["reduced_template_dimension"] == 6, "wrong repair dimension")
    require(repair["forced_equal_pairs"] == 0, "wrong repair forced pair count")

    survivor = record["survivor"]
    require(survivor["template_id"] == "random_matroid_seeded_0_m6", "wrong survivor")
    require(survivor["assignment_strategy"] == "sorted_block", "wrong assignment")
    require(survivor["support_vector"] == [TARGET_AGREEMENT] * 7, "wrong support vector")
    require(survivor["pair7_counts"] == [204, 204, 204, 204, 204], "wrong pair7 counts")
    require(survivor["max_pair_count"] == 204, "wrong max pair")
    require(survivor["proxy_rank"] == 1280, "wrong source proxy rank")
    require(survivor["proxy_nullity"] == 256, "wrong source proxy nullity")
    verify_coordinate_ledger(record)
    verify_functional_ledger(record)

    candidate = record["candidate"]
    require(candidate["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "random_matroid_seeded_0_m6",
        "functional-divisibility",
        "1211 x 714",
        "GF(12289)",
        "GF(17^32)",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    lift = record["functional_lift"]
    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "template_id": survivor["template_id"],
        "functional_classes": lift["functional_classes"],
        "functional_span_rank": lift["functional_span_rank"],
        "proxy_rank": lift["proxy_rank"],
        "proxy_nullity": lift["proxy_nullity"],
        "best_failure_mode": lift["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 random-matroid functional lift (status={result['proof_status']})")


if __name__ == "__main__":
    main()
