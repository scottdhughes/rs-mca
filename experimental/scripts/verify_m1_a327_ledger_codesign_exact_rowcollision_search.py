#!/usr/bin/env python3
"""Verify the M1 a=327 ledger-codesign exact row-collision search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_ledger_codesign_exact_rowcollision_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_ledger_codesign_exact_rowcollision_search.md")

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


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "b74ba9e", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / EXACT_ROWCOLLISION_Q_BUDGET_FAIL / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_rowdependency_search"]
    require(previous["structural_pass_systems"] == 240, "wrong previous structural count")
    require(previous["basis_profiles_constructed"] == 160, "wrong previous profile count")
    require(previous["dependency_q_budget_profiles"] == 18, "wrong previous dependency q count")
    require(previous["proxy_ranked_profiles"] == 12, "wrong previous ranked count")
    require(previous["proxy_positive_profiles"] == 0, "unexpected previous proxy positive")
    require(previous["best_proxy_rank"] == 771, "wrong previous proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous proxy nullity")
    require(previous["failure_mode"] == "ROWDEP_PROXY_FULL_RANK", "wrong previous failure")

    search = record["exact_rowcollision_search"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["q_variable_floor"] == 350, "wrong q-variable floor")
    require(search["max_templates"] == 128, "wrong template limit")
    require(search["max_systems"] == 360, "wrong system limit")
    require(search["profile_candidate_limit"] == 60, "wrong candidate limit")
    require(search["natural_basis_profiles_per_candidate"] == 8, "wrong natural profile count")
    require(search["natural_random_bases"] == 512, "wrong random basis count")
    require(search["forced_groups_per_candidate"] == 8, "wrong forced group limit")
    require(search["profile_rank_limit"] == 12, "wrong rank limit")
    require(search["structural_pass_systems"] == 360, "wrong structural pass count")
    require(search["candidates_scanned"] == 60, "wrong candidate count")
    require(search["candidates_with_collision_groups"] == 60, "wrong collision candidate count")
    require(search["candidate_collision_group_counts"] == {"support": 60}, "wrong candidate collision groups")
    require(search["basis_profiles_constructed"] == 540, "wrong basis profile count")
    require(search["natural_profiles_constructed"] == 480, "wrong natural profile count")
    require(search["forced_profiles_constructed"] == 60, "wrong forced profile count")
    require(search["q_budget_profiles"] == 36, "wrong q-budget profile count")
    require(search["exact_collision_profiles"] == 438, "wrong exact-collision count")
    require(search["exact_collision_q_budget_profiles"] == 0, "unexpected exact-collision q-budget profile")
    require(search["proxy_ranked_profiles"] == 0, "unexpected proxy rank")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positive")
    require(search["best_exact_collision_score"] == -91, "wrong best collision score")
    require(search["best_exact_collision_q_variable_count"] == 271, "wrong best collision q count")
    require(search["best_q_budget_collision_score"] is None, "unexpected q-budget collision score")
    require(search["best_failure_mode"] == "EXACT_ROWCOLLISION_Q_BUDGET_FAIL", "wrong best failure")

    collision = record["best_exact_collision_profile"]
    require(collision["profile_kind"] == "natural", "wrong collision profile kind")
    require(collision["template_id"] == "lcodesign_0003_basis_simple", "wrong collision template")
    require(collision["basis_id"] == "basisaware_0_1_2_3_4_6", "wrong collision basis")
    require(collision["support_vector"] == [TARGET_AGREEMENT] * 7, "wrong collision support")
    require(collision["pair7_counts"] == [253, 253, 253, 253, 253], "wrong collision pair7 counts")
    require(collision["max_pair_count"] == 253, "wrong collision max pair")
    require(collision["q_variable_count"] == 271, "wrong collision q count")
    require(collision["q_variable_budget_ok"] is False, "collision profile unexpectedly clears q budget")
    require(collision["matrix_shape"] == [512, 271], "wrong collision matrix shape")
    require(collision["repeated_support_pairs"] == 1, "wrong repeated support pairs")
    require(collision["repeated_coordinate_pairs"] == 0, "unexpected repeated coordinates")
    require(collision["repeated_support_coordinate_pairs"] == 0, "unexpected support-coordinate repeats")
    require(collision["nested_support_pairs"] == 1, "wrong nested support pairs")
    require(collision["support_overlap_total"] == 148, "wrong support overlap total")
    require(collision["functional_classes"] == 12, "wrong functional class count")
    require(collision["functional_span_rank"] == 6, "wrong functional span")
    require(collision["forced_functional_identities"] == 0, "unexpected forced identities")

    require(record["best_collision_q_budget_profile"] is None, "unexpected q-budget collision profile")
    require(record["best_profile"] is None, "unexpected proxy-ranked best profile")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "EXACT_ROWCOLLISION_Q_BUDGET_FAIL",
        "structural-pass systems = 360",
        "exact-collision profiles = 438",
        "exact-collision q-budget profiles = 0",
        "best exact-collision q-variable count = 271",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "structural_pass_systems": search["structural_pass_systems"],
        "basis_profiles_constructed": search["basis_profiles_constructed"],
        "exact_collision_profiles": search["exact_collision_profiles"],
        "exact_collision_q_budget_profiles": search["exact_collision_q_budget_profiles"],
        "q_budget_profiles": search["q_budget_profiles"],
        "best_exact_collision_q_variable_count": search["best_exact_collision_q_variable_count"],
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
        print(f"PASS: M1 a=327 ledger-codesign exact row-collision search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
