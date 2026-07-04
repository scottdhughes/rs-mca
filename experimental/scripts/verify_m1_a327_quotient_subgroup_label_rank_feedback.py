#!/usr/bin/env python3
"""Verify the M1 a=327 quotient-subgroup label rank-feedback ledger."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_label_rank_feedback.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_label_rank_feedback.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_label_rank_feedback.py")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def load_scan_module() -> Any:
    spec = importlib.util.spec_from_file_location("label_rank_feedback_scan", SCAN_PATH)
    require(spec is not None and spec.loader is not None, "failed to import scan module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    scan = load_scan_module()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "7e21f1d", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")

    previous = record["previous_quotient_subgroup_realization_search"]
    require(previous["proxy_matrix_shape"] == [495, 384], "wrong previous matrix shape")
    require(previous["proxy_rank"] == 384, "wrong previous rank")
    require(previous["proxy_nullity"] == 0, "wrong previous nullity")

    feedback = record["label_rank_feedback"]
    require(feedback["labellings_tested"] == len(record["tested_labellings"]), "wrong tested count")
    require(feedback["best_support_vector"] == [327] * 7, "best support changed")
    require(feedback["best_pair7_counts"] == [252] * 5, "best pair7 changed")
    require(feedback["best_max_pair_equal_h_count"] == 252, "best pair cap changed")
    require(feedback["best_matrix_shape"] == [495, 384], "best matrix shape changed")
    require(feedback["best_proxy_rank"] <= 384, "rank exceeds variable count")
    require(feedback["best_proxy_nullity"] == 384 - feedback["best_proxy_rank"], "bad nullity")

    recomputed = scan.build_record(feedback["random_trials_requested"], feedback["seed"])
    require(recomputed["label_rank_feedback"] == feedback, "rank-feedback recomputation mismatch")
    require(recomputed["proof_status"] == record["proof_status"], "proof status mismatch")

    expected_status = (
        "CANDIDATE / QUOTIENT_LABEL_RANK_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
        if feedback["proxy_positive_labellings"] > 0
        else "EXACT_EXTRACTION_NO_A327 / QUOTIENT_LABEL_RANK_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected_status, "wrong proof status")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "QUOTIENT_LABEL_RANK_PROXY_FULL_RANK",
        "labellings tested",
        "GF(257)",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        **feedback,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 quotient-subgroup label rank feedback (status={result['proof_status']})")


if __name__ == "__main__":
    main()
