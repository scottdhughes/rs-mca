#!/usr/bin/env python3
"""Verify M1 a=327 order-8 block-count partition grammar search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_order8_block_count_partition_grammar_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_order8_block_count_partition_grammar_search.md")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict:
    record = load_json(DATA_PATH)
    note = NOTE_PATH.read_text()
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong target")
    require(record["source_commit"] == "b8d5a7e", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    for claim in ["MCA N_bad", "protocol soundness", "Sage GF(17^32) exact lift"]:
        require(claim in record["not_claimed"], f"missing nonclaim: {claim}")

    previous = record["previous_narrow_grammar"]
    require(previous["feasible_support_schedules"] == 0, "previous support schedule count changed")

    search = record["block_count_search"]
    require(search["block_sizes"] == [1, 2, 3, 4, 5, 6, 7], "unexpected block sizes")
    require(search["models_tested"] == 4, "wrong diagnostic model count")
    require(search["support_only_feasible"] is True, "support-only model should be feasible")
    require(search["pair7_guard_feasible"] is True, "pair7 model should be feasible")
    require(search["best_failure_mode"].startswith("BLOCK_COUNT_"), "bad failure label")

    for model in record["models"]:
        if not model["feasible"]:
            continue
        require(model["support_vector"] == [327] * 7, "support vector changed")
        require(model["equation_count"] is not None, "missing equation count")
        if model["mode"] in {"pair7_guard", "pair_cap", "ambient_pair_cap"}:
            require(min(model["pair7_counts"]) >= 142, "pair7 guard failed")
        if model["mode"] in {"pair_cap", "ambient_pair_cap"}:
            require(max(model["selected_pair_counts"].values()) <= 255, "selected pair cap failed")
        if model["mode"] == "ambient_pair_cap":
            require(model["max_ambient_pair_buckets"] <= 3, "ambient pair cap failed")

    audit = record["interpolation_audit"]
    if audit["attempted"]:
        require(audit["matrix_shape"][1] == 24, "wrong interpolation variable count")
        require(audit["rank"] + audit["nullity"] == 24, "rank/nullity mismatch")

    if search["exact_candidates"]:
        expected = "CANDIDATE / BLOCK_COUNT_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
    elif search["ambient_pair_cap_feasible"]:
        expected = "EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_INTERPOLATION_NO_CANDIDATE / PARTIAL / EXPERIMENTAL"
    elif record["models"][-1]["cp_sat_status"] in {"INFEASIBLE", "MODEL_INVALID"}:
        expected = "EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_AMBIENT_INFEASIBLE / PARTIAL / EXPERIMENTAL"
    else:
        expected = "EXACT_EXTRACTION_NO_A327 / BLOCK_COUNT_CP_UNRESOLVED / PARTIAL / EXPERIMENTAL"
    require(record["proof_status"] == expected, "wrong proof status")
    for phrase in ["BLOCK_COUNT", "selected blocks", "degree-3 interpolation", "not an MCA row"]:
        require(phrase in note, f"note missing phrase: {phrase}")
    return {"status": "PASS", "proof_status": record["proof_status"], **search}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 order-8 block-count partition grammar search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
