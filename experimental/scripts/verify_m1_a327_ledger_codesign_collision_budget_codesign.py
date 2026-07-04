#!/usr/bin/env python3
"""Verify the M1 a=327 ledger-codesign collision-budget codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_ledger_codesign_collision_budget_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_ledger_codesign_collision_budget_codesign.md")

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


def verify_profile(profile: dict[str, Any], *, proxy: bool) -> None:
    require(profile["profile_kind"] == "collision_budget", "wrong profile kind")
    require(profile["template_id"] == "lcodesign_0002_basis_simple", "wrong template")
    require(
        profile["basis_id"] == "collbudget_low_support_basis_support_0_11_6_7_10_5_2",
        "wrong basis",
    )
    require(profile["codesign_preference"] == "low_support_basis", "wrong preference")
    require(profile["forced_group_type"] == "support", "wrong forced group type")
    require(profile["forced_group_nonbasis_count"] == 2, "wrong forced group nonbasis count")
    require(profile["forced_group_class_indices"] == [8, 9], "wrong forced group classes")
    require(profile["support_vector"] == [TARGET_AGREEMENT] * 7, "wrong support vector")
    require(profile["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(profile["max_pair_count"] == 253, "wrong max pair count")
    require(profile["q_variable_count"] == 851, "wrong q-variable count")
    require(profile["q_variable_budget_ok"] is True, "profile below q budget")
    require(profile["collision_budget_success"] is True, "profile did not clear collision-budget gate")
    require(profile["matrix_shape"] == [1092, 851], "wrong matrix shape")
    require(profile["repeated_support_pairs"] == 1, "wrong support collision count")
    require(profile["repeated_coordinate_pairs"] == 0, "unexpected coordinate collision")
    require(profile["repeated_support_coordinate_pairs"] == 0, "unexpected support-coordinate collision")
    require(profile["nested_support_pairs"] == 2, "wrong nested support pairs")
    require(profile["support_overlap_total"] == 1055, "wrong support overlap total")
    require(profile["functional_classes"] == 12, "wrong functional class count")
    require(profile["functional_span_rank"] == 6, "wrong functional span")
    require(profile["forced_functional_identities"] == 0, "unexpected forced identities")
    if proxy:
        require(profile["proxy_matrix_shape"] == [1092, 851], "wrong proxy matrix")
        require(profile["proxy_rank"] == 851, "wrong proxy rank")
        require(profile["proxy_nullity"] == 0, "wrong proxy nullity")
        require(profile["best_failure_mode"] == "CBUDGET_PROXY_FULL_RANK", "wrong profile failure")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "2939690", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / CBUDGET_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_exact_rowcollision_search"]
    require(previous["structural_pass_systems"] == 360, "wrong previous structural count")
    require(previous["basis_profiles_constructed"] == 540, "wrong previous profile count")
    require(previous["exact_collision_profiles"] == 438, "wrong previous collision count")
    require(previous["exact_collision_q_budget_profiles"] == 0, "wrong previous collision-budget count")
    require(previous["best_exact_collision_q_variable_count"] == 271, "wrong previous q count")
    require(previous["failure_mode"] == "EXACT_ROWCOLLISION_Q_BUDGET_FAIL", "wrong previous failure")

    search = record["collision_budget_codesign"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["q_variable_floor"] == 350, "wrong q floor")
    require(search["max_templates"] == 128, "wrong max templates")
    require(search["max_systems"] == 360, "wrong max systems")
    require(search["profile_candidate_limit"] == 60, "wrong candidate limit")
    require(search["groups_per_candidate"] == 8, "wrong groups per candidate")
    require(
        search["preferences"]
        == ["low_support_basis", "low_support_not_group_support", "mid_support_rank", "q_budget_then_span"],
        "wrong preference list",
    )
    require(search["structural_pass_systems"] == 360, "wrong structural pass count")
    require(search["candidates_scanned"] == 60, "wrong candidate count")
    require(search["candidates_with_collision_groups"] == 60, "wrong collision candidate count")
    require(search["candidate_collision_group_counts"] == {"support": 60}, "wrong collision group counts")
    require(search["basis_profiles_constructed"] == 240, "wrong basis profile count")
    require(search["exact_collision_profiles"] == 240, "wrong exact-collision count")
    require(search["q_budget_profiles"] == 240, "wrong q-budget count")
    require(search["collision_budget_profiles"] == 240, "wrong collision-budget count")
    require(search["proxy_ranked_profiles"] == 12, "wrong proxy-ranked count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positive")
    require(search["best_success_q_variable_count"] == 851, "wrong success q count")
    require(search["best_success_repeated_support_pairs"] == 1, "wrong success support collision count")
    require(search["best_proxy_rank"] == 851, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_q_variable_count"] == 851, "wrong best q count")
    require(search["best_failure_mode"] == "CBUDGET_PROXY_FULL_RANK", "wrong best failure")
    require(search["profile_failure_counts"] == {"CBUDGET_PROXY_FULL_RANK": 12}, "wrong failure counts")

    verify_profile(record["best_success_profile"], proxy=False)
    verify_profile(record["best_profile"], proxy=True)
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "CBUDGET_PROXY_FULL_RANK",
        "collision-budget profiles = 240",
        "best q-variable count = 851",
        "proxy rank/nullity = 851 / 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_constructed": search["basis_profiles_constructed"],
        "collision_budget_profiles": search["collision_budget_profiles"],
        "proxy_ranked_profiles": search["proxy_ranked_profiles"],
        "proxy_positive_profiles": search["proxy_positive_profiles"],
        "best_q_variable_count": search["best_q_variable_count"],
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
        print(f"PASS: M1 a=327 ledger-codesign collision-budget codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
