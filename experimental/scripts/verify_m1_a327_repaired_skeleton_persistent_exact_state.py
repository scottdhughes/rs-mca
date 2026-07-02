#!/usr/bin/env python3
"""Verifier for repaired-skeleton persistent exact state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_repaired_skeleton_persistent_exact_state.json")
TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
REQUIRED_HASHES = {
    "base_vector_hash",
    "base_codeword_value_hash",
    "base_value_class_hash",
    "failed_split_vector_hash",
    "failed_split_codeword_value_hash",
    "failed_split_value_class_hash",
    "fixed_specs_hash",
    "failed_split_specs_hash",
    "coordinate_ledger_hash",
    "result_hash",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def require_hash(value: Any, name: str) -> None:
    require(isinstance(value, str) and len(value) == 64, f"bad hash for {name}")


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "7a02b97", "wrong source commit")
    require(record["construction_mode"] == "repaired_skeleton_persistent_exact_state", "wrong mode")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing non-claims")

    baseline = record["baseline"]
    require(baseline["source_skeleton_commit"] == "2dfd1d9", "wrong source skeleton commit")
    require(baseline["source_skeleton_capacity"] == 333, "wrong source skeleton capacity")
    require(baseline["source_skeleton_pair_B_values"] == [1024, 657, 656, 1024, 1024], "wrong source pairs")
    require(baseline["source_skeleton_collapse_pattern"] == [[1, 4, 5, 7], [6], [3], [2]], "wrong source collapse")
    require(baseline["failed_split_commit"] == "7a02b97", "wrong failed split commit")
    require(baseline["failed_split_family"] == "split_4_from_157", "wrong failed split family")
    require(baseline["failed_split_capacity"] == 315, "wrong failed split capacity")
    require(baseline["failed_split_pair_B_values"] == [1024, 593, 592, 512, 1024], "wrong failed split pairs")
    require(baseline["failed_split_collapse_pattern"] == [[1, 5, 6, 7], [4], [3], [2]], "wrong failed split collapse")
    require(baseline["failed_split_failure_mode"] == "REPAIRED_SPLIT_CAPACITY_LOSS", "wrong failed split mode")

    replay = record["exact_state_replay"]
    require(replay["exact_field"] == "GF(17^32)", "wrong exact field")
    require(replay["H_order"] == 512, "wrong H order")
    require(replay["replay_status"] == "PASS", "replay did not pass")
    require(replay["source_skeleton"]["capacity"] == 333, "bad replay source capacity")
    require(replay["source_skeleton"]["pair_B_values"] == [1024, 657, 656, 1024, 1024], "bad replay source pairs")
    require(replay["failed_split"]["capacity"] == 315, "bad replay failed split capacity")
    require(replay["failed_split"]["pair_B_values"] == [1024, 593, 592, 512, 1024], "bad replay failed split pairs")
    require(replay["failed_split"]["failure_mode"] == "REPAIRED_SPLIT_CAPACITY_LOSS", "bad replay failed mode")

    hashes = replay["state_hashes"]
    require(REQUIRED_HASHES.issubset(hashes.keys()), "missing state hash")
    for key in REQUIRED_HASHES:
        require_hash(hashes[key], key)

    row_state = replay["row_state"]
    require(row_state["fixed_specs_count"] > 0, "empty fixed specs")
    require(row_state["failed_split_specs_count"] == 1, "wrong split spec count")
    require(row_state["pivot_columns_persisted"] is False, "unexpected pivot persistence claim")
    require(row_state["free_columns_persisted"] is False, "unexpected free persistence claim")

    ledger = replay["coordinate_ledger"]
    require(ledger["coordinates"] == 512, "wrong coordinate count")
    require_hash(ledger["ledger_hash"], "ledger_hash")
    require(len(ledger["rows"]) == 512, "wrong ledger rows")
    sample = ledger["rows"][0]
    for key in [
        "coordinate",
        "quotient_fiber",
        "capacity_before",
        "capacity_after",
        "B27_before",
        "B27_after",
        "B37_before",
        "B37_after",
        "B47_before",
        "B47_after",
        "B57_before",
        "B57_after",
        "split_damage_score",
        "replacement_priority_score",
    ]:
        require(key in sample, f"missing ledger key {key}")

    require(record["proof_status"] == "EXACT_STATE_REPLAY", "wrong proof status")
    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "replay_status": replay["replay_status"],
        "coordinate_rows": ledger["coordinates"],
        "source_capacity": replay["source_skeleton"]["capacity"],
        "failed_split_capacity": replay["failed_split"]["capacity"],
        "failed_split_pair_B_values": replay["failed_split"]["pair_B_values"],
        "result_hash": hashes["result_hash"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(load_json(DATA_PATH))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS: M1 a=327 repaired-skeleton persistent exact state")


if __name__ == "__main__":
    main()
