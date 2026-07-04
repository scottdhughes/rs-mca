#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear kernel backward-synthesis ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_kernel_backward_synthesis.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_kernel_backward_synthesis.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
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
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "81fceb2", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "PAIR_CLEAR_SLOT_ACTUAL_TEMPLATES", "wrong realization status")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / PKBS_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_prescribed_nonbasis_kernel"]
    require(previous["commit"] == "81fceb2", "wrong previous commit")
    require(previous["near_pair_clear_kernel_profiles"] == 0, "unexpected previous near pair-clear kernel")
    require(previous["best_failure_mode"] == "PNK_NEAR_KERNEL_FORCED_PAIR", "wrong previous failure")

    search = record["pairclear_backward_synthesis"]
    require(search["template_specs_tested"] == 4, "wrong template spec count")
    require(search["milp_profiles_constructed"] == 4, "wrong MILP profile count")
    require(search["systems_tested"] == 12, "wrong systems tested")
    require(search["structural_pass_candidates"] == 3, "wrong structural-pass count")
    require(search["stable_basis_profiles_tested"] == 123, "wrong stable-basis profile count")
    require(search["slot_profiles_tested"] == 738, "wrong slot profile count")
    require(search["actual_zero_slot_profiles"] == 0, "unexpected zero-slot profile")
    require(search["pair_projection_clear_actual_slots"] == 0, "unexpected pair-clear actual slot")
    require(search["proxy_positive_actual_slots"] == 0, "unexpected proxy-positive slot")
    require(search["best_template_id"] == "pairclear_slot5_pair7_guarded", "wrong best template")
    require(search["best_assignment_strategy"] == "pair7_block", "wrong best assignment")
    require(search["best_slot_nonzero_rows"] == 3, "wrong best slot-nonzero count")
    require(search["best_forced_pair_count"] == 11, "wrong best forced-pair count")
    require(search["best_failure_mode"] == "PKBS_SLOT_NOT_KERNEL", "wrong best failure")
    require(
        search["failure_counts"]
        == {
            "PKBS_FORCED_IDENTITY": 6,
            "PKBS_LOW_FUNCTIONAL_SPAN": 3,
            "PKBS_SLOT_NOT_KERNEL": 3,
        },
        "wrong failure counts",
    )
    require(
        search["screen_counts"]
        == {
            "PKBS_FORCED_IDENTITY": 6,
            "PKBS_LOW_FUNCTIONAL_SPAN": 3,
            "PKBS_STRUCTURAL_PASS": 3,
        },
        "wrong screen counts",
    )

    best = record["best_candidate"]
    require(best["template_id"] == "pairclear_slot5_pair7_guarded", "wrong best candidate template")
    require(best["assignment_strategy"] == "pair7_block", "wrong best candidate assignment")
    require(best["pairclear_slot"] == 5, "wrong pair-clear template slot")
    require(best["pairclear_slot_distinct"] is True, "template slot not pair-clear")
    require(best["actual_zero_slot_profiles"] == 0, "unexpected best zero-slot profile")
    require(best["pair_projection_clear_actual_slots"] == 0, "unexpected best pair-clear slot")

    profile = best["best_profile"]
    require(profile["basis_id"] == "slot_union_179_3_6_12_13_14_16", "wrong best basis")
    require(profile["coefficient_matrix_shape"] == [11, 6], "wrong coefficient matrix shape")
    require(profile["coefficient_rank"] == 6, "wrong coefficient rank")
    require(profile["coefficient_nullity"] == 0, "wrong coefficient nullity")
    require(profile["proxy_kernel_slot"] == 2, "wrong best stable-basis slot")
    require(profile["slot_nonzero_rows"] == 3, "wrong slot nonzero count")
    require(profile["forced_pair_count"] == 11, "wrong profile forced-pair count")
    require(
        profile["forced_pairs"] == ["P13", "P24", "P25", "P26", "P27", "P45", "P46", "P47", "P56", "P57", "P67"],
        "wrong forced pairs",
    )
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "template specs tested = 4",
        "systems tested = 12",
        "slot profiles tested = 738",
        "pair-projection-clear actual slots = 0",
        "forced pair count = 11",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "slot_profiles_tested": search["slot_profiles_tested"],
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
        print(f"PASS: M1 a=327 pair-clear kernel backward synthesis (status={result['proof_status']})")


if __name__ == "__main__":
    main()
