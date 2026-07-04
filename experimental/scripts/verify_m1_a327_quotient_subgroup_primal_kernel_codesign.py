#!/usr/bin/env python3
"""Verify the M1 a=327 quotient-subgroup primal-kernel codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_primal_kernel_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_quotient_subgroup_primal_kernel_codesign.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong target")
    require(record["source_commit"] == "563f34a", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_rankaware_v2"]
    require(previous["structural_defect_targets_found"] == 0, "unexpected previous structural defect")
    require(previous["best_proxy_nullity"] == 0, "unexpected previous proxy nullity")

    search = record["primal_kernel_codesign"]
    require(search["order8_bucket_size"] == 64, "wrong order-8 bucket size")
    require(search["degree_in_X"] == 192, "wrong degree")
    require(search["best_failure_mode"].startswith("PRIMAL_KERNEL_"), "wrong failure label")

    root = record["root_geometry"]
    require(root["cp_sat_status"] in {"OPTIMAL", "FEASIBLE", "INFEASIBLE", "UNKNOWN"}, "bad root CP status")
    if root["feasible"]:
        require(root["support_vector"] == [327] * 7, "root support vector changed")
        require(min(root["pair7_counts"]) >= 142, "root pair7 guard failed")
        require(root["max_selected_pair_count"] <= 255, "root pair cap failed")
        require(len(root["root_triples_by_witness"]) == 6, "wrong root triple count")
        require(all(len(triple) == 3 for triple in root["root_triples_by_witness"]), "root triples not cubic")

    locator = record["locator_codesign"]
    if locator["attempted"]:
        require(locator["field"] == "GF(17)", "wrong locator field")
        require(locator["polynomial_family"] == "g_i(X)=c_i*prod_{r in R_i}(X^64-r)", "wrong family")
        require(len(locator["order8_domain"]) == 8, "wrong order-8 domain")
        require(locator["allocation_attempts"] >= 1, "missing locator attempts")
        require(len(locator["attempt_sample"]) >= 1, "missing locator attempt sample")
        for attempt in [*locator["attempt_sample"], locator["best"]]:
            require(attempt["degree_in_X"] == 192, "wrong attempt degree")
            if attempt["allocation_feasible"]:
                require(attempt["max_ambient_pair_count"] <= 255, "feasible allocation violates ambient pair cap")
                require(all(value == 327 for value in attempt["allocation_support_vector"]), "allocation support changed")
                require(min(attempt["allocation_pair7_counts"]) >= 142, "allocation pair7 guard failed")

    expected = (
        "CANDIDATE / PRIMAL_KERNEL_LOCATOR_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        if search["locator_candidate_constructed"]
        else "EXACT_EXTRACTION_NO_A327 / PRIMAL_KERNEL_CODESIGN_NO_ALLOCATION / PARTIAL / EXPERIMENTAL"
    )
    require(record["proof_status"] == expected, "wrong proof status")
    require(record["candidate"]["constructed"] is search["locator_candidate_constructed"], "candidate flag mismatch")

    for phrase in [
        "PRIMAL_KERNEL",
        "order-8",
        "dependency-engineered",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        **search,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 quotient-subgroup primal-kernel codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
