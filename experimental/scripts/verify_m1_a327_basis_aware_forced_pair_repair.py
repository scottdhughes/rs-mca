#!/usr/bin/env python3
"""Verify the M1 a=327 basis-aware forced-pair repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_basis_aware_forced_pair_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_basis_aware_forced_pair_repair.md")

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
    require(record["source_commit"] == "37d9718", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "BASIS_AWARE_FORCED_PAIR_REPAIR", "wrong realization status")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / BAFPAIR_PARTIAL_FORCED_PAIR_REPAIR / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_basis_aware_pairclear"]
    require(previous["commit"] == "37d9718", "wrong previous commit")
    require(previous["best_forced_pair_count"] == 4, "wrong previous forced-pair count")
    require(previous["best_forced_pairs"] == ["P12", "P17", "P27", "P46"], "wrong previous forced pairs")
    require(previous["best_failure_mode"] == "BAPK_SLOT_PAIR_CLEAR_BROKEN", "wrong previous failure")

    search = record["forced_pair_repair"]
    require(search["top_classes"] == 32, "wrong top class count")
    require(search["random_bases"] == 1024, "wrong random basis count")
    require(search["systems_tested"] == 12, "wrong systems tested")
    require(search["structural_pass_candidates"] == 3, "wrong structural pass count")
    require(search["basis_profiles_tested"] == 16437, "wrong basis profile count")
    require(search["slot_profiles_tested"] == 98622, "wrong slot profile count")
    require(search["pair_clear_slot_profiles"] == 0, "unexpected pair-clear slot")
    require(search["pair_clear_slot_kernel_profiles"] == 0, "unexpected pair-clear slot kernel")
    require(search["best_template_id"] == "pairclear_slot5_pair7_guarded", "wrong best template")
    require(search["best_assignment_strategy"] == "pair7_block", "wrong best assignment")
    require(search["best_forced_pair_count"] == 3, "wrong best forced-pair count")
    require(search["best_slot_nonzero_rows"] == 11, "wrong best slot-nonzero count")
    require(search["target_pairs_repaired"] == ["P17", "P27"], "wrong repaired target pairs")
    require(search["target_pairs_remaining"] == ["P12", "P46"], "wrong remaining target pairs")
    require(search["new_forced_pairs_introduced"] == ["P57"], "wrong introduced forced pairs")
    require(search["forced_pair_count_delta"] == -1, "wrong forced-pair delta")
    require(search["best_failure_mode"] == "BAFPAIR_PARTIAL_FORCED_PAIR_REPAIR", "wrong best failure")

    best = record["best_candidate"]
    require(best["template_id"] == "pairclear_slot5_pair7_guarded", "wrong best candidate template")
    require(best["assignment_strategy"] == "pair7_block", "wrong best candidate assignment")
    profile = best["best_profile"]
    require(profile["basis_id"] == "basisaware_6_7_8_14_15_16", "wrong best basis")
    require(profile["coefficient_matrix_shape"] == [11, 6], "wrong coefficient shape")
    require(profile["coefficient_rank"] == 6, "wrong coefficient rank")
    require(profile["coefficient_nullity"] == 0, "wrong coefficient nullity")
    require(profile["proxy_kernel_slot"] == 5, "wrong proxy kernel slot")
    require(profile["slot_nonzero_rows"] == 11, "wrong slot nonzero count")
    require(profile["forced_pair_count"] == 3, "wrong profile forced-pair count")
    require(profile["forced_pairs"] == ["P12", "P46", "P57"], "wrong profile forced pairs")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "basis profiles tested = 16437",
        "slot profiles tested = 98622",
        "target pairs repaired = P17,P27",
        "target pairs remaining = P12,P46",
        "new forced pair introduced = P57",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "best_forced_pair_count": search["best_forced_pair_count"],
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
        print(f"PASS: M1 a=327 basis-aware forced-pair repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
