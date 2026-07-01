#!/usr/bin/env python3
"""Verifier for high-buffer pairclass before split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_high_buffer_pairclass_before_split.json")
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
    "BUFFER_NOT_CREATED",
    "BUFFER_CREATES_COLLAPSE",
    "BUFFER_KILLS_PAIR27_37",
    "SPLIT_CONSUMES_BUFFER",
    "SPLIT_PAIR57_LOSS",
    "SPLIT_LOW_RESCHEDULE",
    "HIGH_BUFFER_EXACT_CANDIDATE",
    "BUFFER_INCONSISTENT",
    "HIGH_BUFFER_TIMEOUT",
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
    require(record["source_commit"] == "0f2655a", "wrong source commit")
    require(record["construction_mode"] == "high_buffer_pairclass_before_split", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["local_basin_baseline"]
    require(baseline["pre_split_pair_B_values"] == [1024, 577, 576, 1024, 1024], "wrong pre-split pairs")
    require(baseline["pre_split_capacity"] == 384, "wrong pre-split capacity")
    require(baseline["post_split_pair_B_values"] == [1024, 593, 592, 1024, 1024], "wrong post-split pairs")
    require(baseline["post_split_capacity"] == 315, "wrong post-split capacity")
    require(baseline["capacity_loss"] == 69, "wrong capacity loss")
    require(baseline["best_failure"] == "COMP_SPLIT_CAPACITY_NOT_RESTORED", "wrong source failure")

    search = record["high_buffer_search"]
    require(search["exact_field"] == "GF(17^32)", "wrong exact field")
    require(search["base_system"] == "scalable_pairclass_overlap_all_extension96", "wrong base system")
    require(search["buffer_rows"] == [32, 64, 96, 128], "wrong buffer rows")
    require(
        search["buffer_families"]
        == [
            "pair57_buffer",
            "all_capacity_buffer",
            "pair27_37_plus_capacity",
            "quotient_fiber_buffer",
            "mixed_buffer",
        ],
        "wrong buffer families",
    )
    require(search["systems_tested"] == 20, "wrong system count")
    require(search["timeouts"] == 9, "wrong timeout count")
    require(search["pre_split_vectors"] == 11, "wrong pre-split vector count")
    require(search["post_split_vectors"] == 11, "wrong post-split vector count")
    require(search["capacity_buffer_vectors"] == 0, "unexpected capacity buffer vector")
    require(search["post_split_capacity_preserving_vectors"] == 0, "unexpected post-split capacity-preserving vector")
    require(search["best_pre_split_capacity"] == 393, "wrong best pre-split capacity")
    require(search["best_post_split_capacity"] == 322, "wrong best post-split capacity")
    require(search["best_pair_B_values"] == [1024, 608, 608, 1024, 1024], "wrong best post-split pair values")
    require(search["best_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong best collapse pattern")
    require(search["best_exact_max_min"] is None, "unexpected exact max-min")
    require(search["best_failure_mode"] in ALLOWED_FAILURES, "bad best failure")
    require(search["best_failure_mode"] == "BUFFER_NOT_CREATED", "wrong best failure")
    require(search["failure_mode_counts"] == {"BUFFER_NOT_CREATED": 11, "HIGH_BUFFER_TIMEOUT": 9}, "wrong failure counts")
    require(len(search["results"]) == search["systems_tested"], "wrong result length")

    exact_candidate_count = 0
    for result in search["results"]:
        require(result["failure_mode"] in ALLOWED_FAILURES, f"bad result failure {result['failure_mode']}")
        post = result.get("post_split")
        if result["failure_mode"] == "HIGH_BUFFER_TIMEOUT":
            require(result.get("pre_split") is None and post is None, "timeout should not have vectors")
        else:
            require(result.get("pre_split") is not None and post is not None, "completed case missing vectors")
        if post and result["failure_mode"] == "HIGH_BUFFER_EXACT_CANDIDATE":
            exact_candidate_count += 1
            require(post["exact_max_min"] >= TARGET_AGREEMENT, "candidate below target")
    require(record["proof_status"] in {"PROOF_RECORD", "CANDIDATE", "EXACT_EXTRACTION_NO_A327", "PARTIAL"}, "bad status")
    if record["proof_status"] == "EXACT_EXTRACTION_NO_A327":
        require(exact_candidate_count == 0, "negative status with exact candidate")
    if exact_candidate_count:
        require(record["proof_status"] == "PROOF_RECORD", "exact candidate should be proof record")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "pre_split_vectors": search["pre_split_vectors"],
        "post_split_vectors": search["post_split_vectors"],
        "capacity_buffer_vectors": search["capacity_buffer_vectors"],
        "post_split_capacity_preserving_vectors": search["post_split_capacity_preserving_vectors"],
        "best_pre_split_capacity": search["best_pre_split_capacity"],
        "best_post_split_capacity": search["best_post_split_capacity"],
        "best_pair_B_values": search["best_pair_B_values"],
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
        print(f"PASS: M1 a=327 high-buffer pairclass ({result['systems_tested']} systems)")


if __name__ == "__main__":
    main()
