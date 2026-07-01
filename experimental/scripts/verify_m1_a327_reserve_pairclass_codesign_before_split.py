#!/usr/bin/env python3
"""Verifier for reserve/pairclass co-design before split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_reserve_pairclass_codesign_before_split.json")
TARGET_AGREEMENT = 327
PAIR_TARGET = 2 * TARGET_AGREEMENT
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_FAILURES = {
    "RESERVE_NOT_CREATED",
    "RESERVE_NOT_POSTSPLIT_SURVIVING",
    "PAIRCLASS_NOT_CREATED",
    "PAIR57_GUARD_LOSS",
    "COLLAPSE_RETURNS",
    "LOW_RESCHEDULE",
    "EXACT_CANDIDATE",
    "CODESIGN_INCONSISTENT",
    "CODESIGN_TIMEOUT",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "c7eed3e", "wrong source commit")
    require(record["construction_mode"] == "reserve_pairclass_codesign_before_split", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["best_pre_split_capacity"] == 393, "wrong baseline pre capacity")
    require(baseline["best_post_split_capacity"] == 322, "wrong baseline post capacity")
    require(baseline["best_post_split_pair_B_values"] == [1024, 608, 608, 1024, 1024], "wrong baseline pairs")
    require(baseline["post_capacity_deficit"] == 5, "wrong capacity deficit")
    require(baseline["post_B27_deficit"] == 46, "wrong B27 deficit")
    require(baseline["post_B37_deficit"] == 46, "wrong B37 deficit")
    require(baseline["best_failure"] == "BUFFER_NOT_CREATED", "wrong baseline failure")

    search = record["codesign_search"]
    require(search["systems_tested"] == 20, "wrong system count")
    require(search["timeouts"] == 14, "wrong timeout count")
    require(search["exact_vectors_constructed"] == 12, "wrong exact vector count")
    require(search["pre_split_vectors"] == 6, "wrong pre-split vector count")
    require(search["post_split_vectors"] == 6, "wrong post-split vector count")
    require(search["postsplit_capacity_preserving_vectors"] == 1, "wrong post-split capacity-preserving count")
    require(search["postsplit_pairclass_repaired_vectors"] == 0, "unexpected post-split pairclass repair")
    require(search["postsplit_pair57_preserving_vectors"] == 6, "wrong post-split pair57 count")
    require(search["collapse_reduced_vectors"] == 6, "wrong collapse-reduced count")
    require(search["best_pre_split_capacity"] == 402, "wrong best pre-split capacity")
    require(search["best_post_split_capacity"] == 329, "wrong best post-split capacity")
    require(search["best_post_split_pair_B_values"] == [1024, 641, 640, 1024, 1024], "wrong best post-split pair values")
    require(search["best_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong best collapse pattern")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["row_extension_sizes"] == [64, 96, 128, 160], "wrong row extension sizes")
    require(
        search["row_families"]
        == [
            "pair27_37_plus_capacity",
            "pair27_37_plus_57_guard",
            "quotient_fiber_buffer",
            "mixed_buffer_pairclass",
            "postsplit_survivor_rows",
        ],
        "wrong row families",
    )
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(search["best_failure_mode"] == "RESERVE_NOT_CREATED", "wrong best failure")
    require(search["failure_mode_counts"] == {"CODESIGN_TIMEOUT": 14, "RESERVE_NOT_CREATED": 6}, "wrong failure counts")
    require(len(search["results"]) == search["systems_tested"], "wrong result length")

    exact_candidate_count = 0
    for result in search["results"]:
        failure = result["failure_mode"]
        require(failure in ALLOWED_FAILURES, f"bad result failure {failure}")
        post = result.get("post_split")
        if failure == "CODESIGN_TIMEOUT":
            require(result.get("pre_split") is None and post is None, "timeout should not have vectors")
        elif failure != "CODESIGN_INCONSISTENT":
            require(result.get("pre_split") is not None and post is not None, "completed case missing vectors")
        if failure == "EXACT_CANDIDATE":
            exact_candidate_count += 1
            require(post is not None and post.get("exact_max_min", -1) >= TARGET_AGREEMENT, "candidate below target")
            require(post["pair_B_values"][1] >= PAIR_TARGET and post["pair_B_values"][2] >= PAIR_TARGET, "candidate pair deficit")
            require(post["pair_B_values"][4] >= PAIR_TARGET, "candidate pair57 deficit")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "timeouts": search["timeouts"],
        "exact_vectors_constructed": search["exact_vectors_constructed"],
        "postsplit_capacity_preserving_vectors": search["postsplit_capacity_preserving_vectors"],
        "postsplit_pairclass_repaired_vectors": search["postsplit_pairclass_repaired_vectors"],
        "best_pre_split_capacity": search["best_pre_split_capacity"],
        "best_post_split_capacity": search["best_post_split_capacity"],
        "best_post_split_pair_B_values": search["best_post_split_pair_B_values"],
        "best_collapse_pattern": search["best_collapse_pattern"],
        "best_failure_mode": search["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 reserve/pairclass co-design ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
