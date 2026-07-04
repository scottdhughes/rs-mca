#!/usr/bin/env python3
"""Verify the M1 a=327 quotient-subgroup realization-search ledger."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_realization_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_realization_search.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_quotient_subgroup_realization_search.py")

TARGET_AGREEMENT = 327
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def load_scan_module() -> Any:
    spec = importlib.util.spec_from_file_location("quotient_subgroup_realization_scan", SCAN_PATH)
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
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "7e21f1d", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_quotient_subgroup_primal_kernel_search"]
    require(previous["best_s"] == 4, "wrong previous best s")
    require(previous["best_pair7_counts"] == [252, 252, 252, 252, 252], "wrong previous pair7")
    require(previous["best_max_pair_equal_h_count"] == 252, "wrong previous pair cap")
    require(previous["failure_mode"] == "QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING", "wrong previous failure")

    schedule = record["schedule"]
    coordinates = schedule["coordinates"]
    require(schedule["s"] == 4, "wrong s")
    require(schedule["fiber_size"] == 4, "wrong fiber size")
    require(schedule["quotient_length"] == 128, "wrong quotient length")
    require(schedule["quotient_degree_bound"] == 63, "wrong degree bound")
    require(schedule["labelled_quotient_coordinates"] == 128, "wrong labelled count")
    require(len(coordinates) == 128, "coordinate ledger wrong length")
    require([coordinate["q_index"] for coordinate in coordinates] == list(range(128)), "q_index ledger is not deterministic")

    counts = scan.schedule_counts(coordinates)
    for key in [
        "support_vector",
        "selected_pair_counts",
        "pair_equal_quotient_counts",
        "pair_equal_h_counts",
        "pair7_counts",
        "max_pair_equal_quotient_count",
        "max_pair_equal_h_count",
    ]:
        require(counts[key] == schedule[key], f"schedule count mismatch: {key}")
    require(schedule["support_vector"] == [TARGET_AGREEMENT] * 7, "support target failed")
    require(max(schedule["pair_equal_h_counts"].values()) <= 255, "pair cap failed")
    require(min(schedule["pair7_counts"]) >= 142, "pair7 guard failed")

    proxy = record["proxy_realization"]
    recomputed_proxy = scan.proxy_realization(coordinates)
    for key in ["matrix_shape", "rank", "nullity", "best_failure_mode"]:
        require(recomputed_proxy[key] == proxy[key], f"proxy mismatch: {key}")
    require(proxy["proxy_field"] == "GF(257)", "wrong proxy field")
    require(proxy["variables"] == 384, "wrong variable count")
    require(proxy["matrix_shape"][1] == 384, "wrong matrix columns")

    expected_status = f"EXACT_EXTRACTION_NO_A327 / {proxy['best_failure_mode']} / PARTIAL / EXPERIMENTAL"
    if proxy["best_failure_mode"] == "QUOTIENT_REALIZATION_EXACT_CANDIDATE":
        expected_status = "CANDIDATE / QUOTIENT_REALIZATION_EXACT_CANDIDATE / PARTIAL / EXPERIMENTAL"
    require(record["proof_status"] == expected_status, "wrong proof status")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")
    require(record["exact_audit"]["run"] is False, "unexpected exact audit")

    for phrase in [
        "QUOTIENT_REALIZATION_PROXY_FULL_RANK",
        "s = 4",
        "quotient length = 128",
        "degree <= 63",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "support_vector": schedule["support_vector"],
        "pair7_counts": schedule["pair7_counts"],
        "max_pair_equal_h_count": schedule["max_pair_equal_h_count"],
        "proxy_matrix_shape": proxy["matrix_shape"],
        "proxy_rank": proxy["rank"],
        "proxy_nullity": proxy["nullity"],
        "best_failure_mode": proxy["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 quotient-subgroup realization search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
