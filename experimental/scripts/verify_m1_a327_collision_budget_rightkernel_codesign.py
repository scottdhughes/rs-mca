#!/usr/bin/env python3
"""Verify the M1 a=327 collision-budget right-kernel codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_collision_budget_rightkernel_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_collision_budget_rightkernel_codesign.md")

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
    require(record["source_commit"] == "0108539", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / RKERNEL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_collision_budget_syzygy_search"]
    require(previous["collision_budget_profiles_reconstructed"] == 240, "wrong previous profile count")
    require(previous["syzygy_profiles_scored"] == 240, "wrong previous syzygy count")
    require(previous["syzygy_positive_profiles"] == 0, "unexpected previous syzygy positive")
    require(previous["proxy_ranked_profiles"] == 0, "unexpected previous proxy ranked")
    require(previous["proxy_positive_profiles"] == 0, "unexpected previous proxy positive")
    require(previous["best_failure_mode"] == "SYZYGY_NO_SMALL_ROW_BLOCK_DEPENDENCY", "wrong previous failure")

    tools = record["tools"]
    require(tools["ortools_available"] is True, "OR-Tools unavailable")
    require(tools["ortools_version"] == "9.15.6755", "wrong OR-Tools version")
    require(tools["cp_sat_smoke"] is True, "CP-SAT smoke failed")

    search = record["collision_budget_rightkernel_codesign"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["coefficient_prime"] == 17, "wrong coefficient prime")
    require(search["q_variable_floor"] == 350, "wrong q floor")
    require(search["max_templates"] == 128, "wrong max templates")
    require(search["max_systems"] == 360, "wrong max systems")
    require(search["profile_candidate_limit"] == 60, "wrong candidate limit")
    require(search["groups_per_candidate"] == 8, "wrong groups per candidate")
    require(search["basis_mode"] == "committed_collision_budget", "wrong basis mode")
    require(search["proxy_rank_limit"] == 12, "wrong proxy rank limit")
    require(search["structural_pass_systems"] == 360, "wrong structural pass systems")
    require(search["candidates_scanned"] == 60, "wrong candidates scanned")
    require(search["basis_profiles_constructed"] == 240, "wrong profile count")
    require(search["functional_class_combo_profile_counts"] == {"11": 192, "12": 48}, "wrong class profile counts")
    require(search["coefficient_rank_counts"] == {"5": 192, "6": 48}, "wrong coefficient rank counts")
    require(search["coefficient_kernel_nullity_counts"] == {"0": 48, "1": 192}, "wrong nullity counts")
    require(search["collision_budget_profiles"] == 240, "wrong collision-budget count")
    require(search["rightkernel_collision_budget_profiles"] == 192, "wrong right-kernel profile count")
    require(search["proxy_ranked_profiles"] == 12, "wrong proxy ranked count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positive")
    require(search["best_rightkernel_q_variable_count"] == 666, "wrong best rightkernel q count")
    require(search["best_rightkernel_coefficient_nullity"] == 1, "wrong best coefficient nullity")
    require(search["best_collision_budget_q_variable_count"] == 666, "wrong best collision budget q count")
    require(search["best_proxy_rank"] == 666, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_q_variable_count"] == 666, "wrong best q count")
    require(search["best_failure_mode"] == "RKERNEL_PROXY_FULL_RANK", "wrong failure mode")
    require(search["profile_failure_counts"] == {"RKERNEL_PROXY_FULL_RANK": 12}, "wrong profile failure counts")

    best = record["best_rightkernel_profile"]
    require(best["template_id"] == "lcodesign_0000_basis_simple", "wrong best template")
    require(best["basis_id"] == "collbudget_low_support_basis_support_0_6_7_10_5_2_3", "wrong best basis")
    require(best["basis_support_sizes"] == [74, 74, 74, 142, 253, 253], "wrong best support sizes")
    require(best["q_variable_count"] == 666, "wrong best q")
    require(best["matrix_shape"] == [907, 666], "wrong best matrix shape")
    require(best["coefficient_rank"] == 5, "wrong best coefficient rank")
    require(best["coefficient_right_kernel_nullity"] == 1, "wrong best coefficient nullity")
    require(best["coefficient_right_kernel_projective_first"] == [1, 1, 1, 16, 16, 16], "wrong kernel")
    require(best["rightkernel_collision_budget_success"] is True, "best not right-kernel collision-budget")

    require(record["best_profile"]["proxy_rank"] == 666, "best profile proxy rank missing")
    require(record["best_profile"]["proxy_nullity"] == 0, "best profile proxy nullity missing")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "RKERNEL_PROXY_FULL_RANK",
        "right-kernel collision-budget profiles = 192",
        "coefficient kernel nullity counts = {0: 48, 1: 192}",
        "best coefficient kernel = [1,1,1,16,16,16]",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_constructed": search["basis_profiles_constructed"],
        "rightkernel_collision_budget_profiles": search["rightkernel_collision_budget_profiles"],
        "proxy_ranked_profiles": search["proxy_ranked_profiles"],
        "proxy_positive_profiles": search["proxy_positive_profiles"],
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
        print(f"PASS: M1 a=327 collision-budget right-kernel codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
