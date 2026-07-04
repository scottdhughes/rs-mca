#!/usr/bin/env python3
"""Verify the M1 a=327 cycleguard basis-quotient exact audit ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_cycleguard_stable_window_exact_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_cycleguard_stable_window_exact_audit.md")

TARGET_AGREEMENT = 327
PAIR_LABELS = [f"P{i}{j}" for i in range(1, 8) for j in range(i + 1, 8)]
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_STATUSES = {
    "CANDIDATE / CYCLEG_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL",
    "CANDIDATE / CYCLEG_EXACT_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL",
    "CANDIDATE / CYCLEG_EXACT_PAIR_PROJECTIONS_CLEAR / PARTIAL / EXPERIMENTAL",
    "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_BAD_SOURCE_STATUS / PARTIAL / EXPERIMENTAL",
    "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_NO_BASIS_PROFILE / PARTIAL / EXPERIMENTAL",
    "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_NULLITY_ZERO / PARTIAL / EXPERIMENTAL",
    "EXACT_EXTRACTION_NO_A327 / CYCLEG_EXACT_FORCED_PAIR_EQUALITY / PARTIAL / EXPERIMENTAL",
    "PROOF_RECORD / CYCLEG_EXACT_CANDIDATE / EXPERIMENTAL",
}
ALLOWED_FAILURES = {
    "CYCLEG_EXACT_AUDIT_PENDING",
    "CYCLEG_EXACT_BAD_SOURCE_STATUS",
    "CYCLEG_EXACT_NO_BASIS_PROFILE",
    "CYCLEG_EXACT_NULLITY_POSITIVE",
    "CYCLEG_EXACT_NULLITY_ZERO",
    "CYCLEG_EXACT_FORCED_PAIR_EQUALITY",
    "CYCLEG_EXACT_PAIR_PROJECTIONS_CLEAR",
    "CYCLEG_EXACT_DEGENERATE_SAMPLE",
    "CYCLEG_EXACT_CANDIDATE",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong agreement target")
    require(record["source_commit"] == "c142977", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["proof_status"] in ALLOWED_STATUSES, "bad proof status")

    source = record["source_chamber"]
    require(source["template_id"] == "ninerow_P57_shear_c1_d1", "wrong template")
    require(source["basis_id"] == "basisaware_0_1_2_3_4_5", "wrong basis")
    require(source["direction"] == [1, 4, 0, 0, 10, 0], "wrong chamber direction")
    require(source["forced_pairs"] == [], "source chamber has forced pairs")
    require(source["inactive_rank"] == 4, "wrong inactive rank")
    require(source["inactive_kernel_nullity"] == 2, "wrong inactive nullity")
    require(source["zero_class_union_size"] == 253, "wrong zero union")
    require(source["zero_row_window_dimension"] == 3, "wrong zero-row window")
    require(source["scalar_required_vanishing_union_size"] == 512, "wrong scalar required union")
    require(source["scalar_stable_window_dimension"] == 0, "wrong scalar stable window")
    require(source["best_failure_mode"] == "CYCLEG_REALIZATION_BASIS_QUOTIENT_TARGET", "wrong source failure")

    survivor = record["survivor"]
    require(survivor["template_dimension"] == 6, "wrong template dimension")
    require(len(survivor["template_vectors"]) == 7, "wrong template vector count")
    require(survivor["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "wrong support vector")
    require(survivor["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(survivor["max_pair_count"] == 253, "wrong max pair count")

    require(len(record["coordinate_classes"]) == 512, "wrong coordinate count")
    require(len(record["functional_classes_detail"]) == 25, "wrong functional class count")
    basis_profiles = record["basis_profiles"]
    require(len(basis_profiles) == 1, "wrong basis profile count")
    profile = basis_profiles[0]
    require(profile["basis_class_indices"] == [0, 1, 2, 3, 4, 5], "wrong basis classes")
    require(profile["basis_support_sizes"] == [216, 142, 142, 105, 105, 74], "wrong basis supports")
    require(profile["q_variable_count"] == 752, "wrong q variable count")
    require(profile["matrix_shape"] == [993, 752], "wrong planned matrix shape")
    require(profile["nonbasis_constraints"] == 19, "wrong nonbasis count")

    audit = record["basis_quotient_audit"]
    require(audit["best_failure_mode"] in ALLOWED_FAILURES, "bad audit failure")
    require(audit["best_basis_id"] == "basisaware_0_1_2_3_4_5", "audit basis mismatch")
    require(audit["best_q_variable_count"] == 752, "audit q variable mismatch")
    if audit["best_matrix_shape"] is not None:
        require(audit["best_matrix_shape"] == [993, 752], "exact matrix shape mismatch")
        require(audit["field"] == "GF(17^32)", "wrong exact field")
        require(audit["field_denominator"] == str(17**32), "wrong field denominator")
        require(audit["H_order"] == 512, "wrong H order")
        require(isinstance(audit["best_rank"], int), "rank missing")
        require(isinstance(audit["best_nullity"], int), "nullity missing")
        require(audit["best_rank"] + audit["best_nullity"] == 752, "rank/nullity mismatch")

    projection = record["pair_projection_test"]
    require(projection["pairs_tested"] == 21, "wrong pair count")
    if projection["projection_rank_by_pair"] is not None:
        require(set(projection["projection_rank_by_pair"]) == set(PAIR_LABELS), "bad projection labels")
        require(projection["min_projection_rank"] is not None, "missing min projection rank")

    candidate = record["candidate"]
    if candidate["constructed"]:
        require(record["proof_status"] == "PROOF_RECORD / CYCLEG_EXACT_CANDIDATE / EXPERIMENTAL", "candidate without proof status")
        require(candidate["seven_distinct"] is True, "candidate not seven-distinct")
        require(min(candidate["agreement_vector"]) >= TARGET_AGREEMENT, "candidate below target")
        require(len(candidate["codeword_hashes"]) == 7, "wrong codeword hash count")
    else:
        require(candidate["seven_distinct"] is False, "unexpected distinct flag")

    for phrase in [
        "CYCLEG_EXACT_NULLITY_ZERO",
        "basis-quotient functional-divisibility",
        "matrix shape = 993 x 752",
        "rank = 752",
        "nullity = 0",
        "scalar stable-window dimension = 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_id": source["basis_id"],
        "matrix_shape": audit["best_matrix_shape"] or profile["matrix_shape"],
        "rank": audit["best_rank"],
        "nullity": audit["best_nullity"],
        "best_failure_mode": audit["best_failure_mode"],
        "candidate_constructed": candidate["constructed"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 cycleguard exact audit (status={result['proof_status']})")


if __name__ == "__main__":
    main()
