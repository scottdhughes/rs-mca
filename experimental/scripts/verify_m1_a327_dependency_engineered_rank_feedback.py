#!/usr/bin/env python3
"""Verify the M1 a=327 dependency-engineered rank-feedback ledger."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_dependency_engineered_rank_feedback.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_dependency_engineered_rank_feedback.md")

TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_LABELS = {
    "DEPENDENCY_SUPPORT_FAIL",
    "DEPENDENCY_PAIR_GUARD_FAIL",
    "DEPENDENCY_FORCED_IDENTITY",
    "DEPENDENCY_LOW_FUNCTIONAL_SPAN",
    "DEPENDENCY_DIAGONAL_ANNIHILATOR",
    "DEPENDENCY_STRUCTURAL_PASS",
    "DEPENDENCY_PROXY_PENDING",
    "DEPENDENCY_PROXY_FULL_RANK",
    "DEPENDENCY_PROXY_NULLITY_POSITIVE",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify_coordinate_ledger(best: dict[str, Any]) -> None:
    coords = best["coordinate_classes"]
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
    require(supports == best["support_vector"], "support vector mismatch")
    require(supports == [TARGET_AGREEMENT] * 7, "support target mismatch")
    require(max(pair_counts.values()) == best["max_pair_count"], "max pair mismatch")
    require(best["pair7_counts"] == [pair_counts[label] for label in ["P17", "P27", "P37", "P47", "P57"]], "pair7 mismatch")
    require(best["selected_class_size_counts"] == dict(selected_sizes), "selected size mismatch")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "614bf1c", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_rank_feedback_v3"]
    require(previous["systems_tested"] == 96, "wrong v3 system count")
    require(previous["structural_pass_candidates"] == 84, "wrong v3 structural count")
    require(previous["proxy_basis_profiles_tested"] == 16, "wrong v3 proxy basis count")
    require(previous["proxy_positive_candidates"] == 0, "wrong v3 proxy-positive count")

    rigidity = record["previous_rank_rigidity_audit"]
    require(rigidity["proxy_profiles_audited"] == 16, "wrong rigidity profile count")
    require(rigidity["full_column_rank_profiles"] == 16, "wrong rigidity full-rank count")
    require(rigidity["row_surplus"] == 241, "wrong rigidity row surplus")

    search = record["dependency_engineered_search"]
    require(search["templates_tested"] == 18, "wrong template count")
    require(search["systems_tested"] == 108, "wrong system count")
    require(search["structural_pass_candidates"] == 96, "wrong structural-pass count")
    require(search["proxy_candidates_tested"] == 8, "wrong proxy candidate count")
    require(search["proxy_basis_profiles_tested"] == 24, "wrong proxy basis count")
    require(search["proxy_positive_candidates"] == 0, "unexpected proxy-positive candidate")
    require(search["best_template_id"] == "random_matroid_v3_seed_007_m6", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(search["best_functional_span_rank"] == 6, "wrong best span")
    require(search["best_proxy_rank"] == 1385, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_dependency_score"] == 1295, "wrong dependency score")
    require(search["best_failure_mode"] == "DEPENDENCY_PROXY_FULL_RANK", "wrong best failure")
    require(set(search["failure_counts"]).issubset(ALLOWED_LABELS), "bad failure label")
    require(set(search["screen_counts"]).issubset(ALLOWED_LABELS), "bad screen label")
    require(search["failure_counts"] == {
        "DEPENDENCY_LOW_FUNCTIONAL_SPAN": 12,
        "DEPENDENCY_PROXY_FULL_RANK": 8,
        "DEPENDENCY_PROXY_PENDING": 88,
    }, "failure counts mismatch")

    summaries = search["candidate_summaries"]
    require(len(summaries) == search["systems_tested"], "summary count mismatch")
    require(sum(1 for row in summaries if row["structural_status"] == "DEPENDENCY_STRUCTURAL_PASS") == 96, "summary structural count mismatch")
    require(sum(1 for row in summaries if row["proxy_results"]) == 8, "summary proxy count mismatch")

    best = record["best_candidate"]
    require(best["support_vector"] == [TARGET_AGREEMENT] * 7, "best support mismatch")
    require(best["pair7_counts"] == [233, 233, 233, 233, 233], "best pair7 mismatch")
    require(best["max_pair_count"] == 233, "best max pair mismatch")
    require(best["functional_span_rank"] == 6, "best span mismatch")
    require(best["annihilator_dimension"] == 0, "best annihilator mismatch")
    require(best["forced_functional_identities"] == 0, "best forced identity mismatch")
    metrics = best["support_dependency_metrics"]
    require(metrics["duplicate_support_groups"] == 14, "wrong duplicate support groups")
    require(metrics["duplicate_support_pairs"] == 51, "wrong duplicate support pairs")
    require(metrics["nested_support_pairs"] == 66, "wrong nested support pairs")
    require(metrics["support_overlap_total"] == 2347, "wrong support overlap")
    require(best["best_proxy"]["proxy_rank"] == 1385, "best proxy rank mismatch")
    require(best["best_proxy"]["proxy_nullity"] == 0, "best proxy nullity mismatch")
    verify_coordinate_ledger(best)

    require(record["exact_audit"]["run"] is False, "unexpected exact audit")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 108",
        "structural-pass candidates = 96",
        "proxy-ranked basis profiles = 24",
        "duplicate support groups = 14",
        "random_matroid_v3_seed_007_m6",
        "1385 / 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "proxy_candidates_tested": search["proxy_candidates_tested"],
        "proxy_basis_profiles_tested": search["proxy_basis_profiles_tested"],
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
        print(f"PASS: M1 a=327 dependency-engineered rank feedback (status={result['proof_status']})")


if __name__ == "__main__":
    main()
