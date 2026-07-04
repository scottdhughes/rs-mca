#!/usr/bin/env python3
"""Verify the M1 a=327 basis-aware pair-clear kernel synthesis ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_basis_aware_pairclear_kernel_synthesis.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_basis_aware_pairclear_kernel_synthesis.md")

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
    require(record["source_commit"] == "a1bb7cf", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "BASIS_AWARE_PAIR_CLEAR_SEARCH", "wrong realization status")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / BAPK_SLOT_PAIR_CLEAR_BROKEN / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_pairclear_backward_synthesis"]
    require(previous["commit"] == "a1bb7cf", "wrong previous commit")
    require(previous["slot_profiles_tested"] == 738, "wrong previous slot profile count")
    require(previous["pair_projection_clear_actual_slots"] == 0, "unexpected previous pair-clear slot")
    require(previous["best_failure_mode"] == "PKBS_SLOT_NOT_KERNEL", "wrong previous failure")

    search = record["basis_aware_pairclear_synthesis"]
    require(search["template_specs_tested"] == 4, "wrong template spec count")
    require(search["milp_profiles_constructed"] == 4, "wrong MILP profile count")
    require(search["systems_tested"] == 12, "wrong systems tested")
    require(search["top_classes"] == 14, "wrong top class count")
    require(search["random_bases"] == 64, "wrong random basis count")
    require(search["structural_pass_candidates"] == 3, "wrong structural pass count")
    require(search["basis_profiles_tested"] == 2976, "wrong basis profile count")
    require(search["slot_profiles_tested"] == 17856, "wrong slot profile count")
    require(search["pair_clear_slot_profiles"] == 0, "unexpected pair-clear slot")
    require(search["pair_clear_slot_kernel_profiles"] == 0, "unexpected pair-clear slot kernel")
    require(search["best_template_id"] == "pairclear_slot5_pair7_guarded", "wrong best template")
    require(search["best_assignment_strategy"] == "pair7_block", "wrong best assignment")
    require(search["best_forced_pair_count"] == 4, "wrong best forced-pair count")
    require(search["best_slot_nonzero_rows"] == 8, "wrong best slot-nonzero count")
    require(search["best_failure_mode"] == "BAPK_SLOT_PAIR_CLEAR_BROKEN", "wrong best failure")
    require(
        search["failure_counts"]
        == {
            "BAPK_FORCED_IDENTITY": 6,
            "BAPK_LOW_FUNCTIONAL_SPAN": 3,
            "BAPK_SLOT_PAIR_CLEAR_BROKEN": 3,
        },
        "wrong failure counts",
    )
    require(
        search["screen_counts"]
        == {
            "BAPK_FORCED_IDENTITY": 6,
            "BAPK_LOW_FUNCTIONAL_SPAN": 3,
            "BAPK_STRUCTURAL_PASS": 3,
        },
        "wrong screen counts",
    )

    best = record["best_candidate"]
    require(best["template_id"] == "pairclear_slot5_pair7_guarded", "wrong best candidate template")
    require(best["assignment_strategy"] == "pair7_block", "wrong best candidate assignment")
    require(best["pair_clear_slot_profiles"] == 0, "unexpected best pair-clear slot")
    require(best["pair_clear_slot_kernel_profiles"] == 0, "unexpected best pair-clear kernel")

    profile = best["best_profile"]
    require(profile["basis_id"] == "basisaware_5_8_13_12_14_16", "wrong best basis")
    require(profile["coefficient_matrix_shape"] == [11, 6], "wrong coefficient matrix shape")
    require(profile["coefficient_rank"] == 6, "wrong coefficient rank")
    require(profile["coefficient_nullity"] == 0, "wrong coefficient nullity")
    require(profile["proxy_kernel_slot"] == 4, "wrong best stable-basis slot")
    require(profile["slot_nonzero_rows"] == 8, "wrong slot nonzero count")
    require(profile["forced_pair_count"] == 4, "wrong profile forced-pair count")
    require(profile["forced_pairs"] == ["P12", "P17", "P27", "P46"], "wrong forced pairs")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "basis profiles tested = 2976",
        "slot profiles tested = 17856",
        "pair-clear slot profiles = 0",
        "forced pair count = 4",
        "P12, P17, P27, P46",
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
        print(f"PASS: M1 a=327 basis-aware pair-clear kernel synthesis (status={result['proof_status']})")


if __name__ == "__main__":
    main()
