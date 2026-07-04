#!/usr/bin/env python3
"""Verify the M1 a=327 realization-aware ledger perturbation ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_realization_aware_ledger_perturbation.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_realization_aware_ledger_perturbation.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "synthetic rowspace edits",
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
    require(record["source_commit"] == "8a15096", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / LEDGERPERT_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )
    require(record["realization_status"] == "ACTUAL_TEMPLATE_ROWSPACES_ONLY", "wrong realization status")

    previous = record["previous_residual_slot_repair"]
    require(previous["commit"] == "8a15096", "wrong previous commit")
    require(previous["actual_zero_slot_profiles"] == 0, "unexpected previous zero slot")
    require(previous["best_failure_mode"] == "RESIDUAL_SLOT_INVARIANT_NONZERO", "wrong previous failure")

    search = record["ledger_perturbation_search"]
    require(
        search["kernel_basis"]
        == [
            [0, 1, -1, 0, 0, -1, 1, 0, 0, 0, 0],
            [0, 1, 0, -1, 0, -1, 0, 1, 0, 0, 0],
            [1, -1, 1, -1, 0, 0, 0, 0, -2, 1, 1],
        ],
        "wrong count-kernel basis",
    )
    require(search["max_abs_coeff"] == 6, "wrong coefficient bound")
    require(search["ledger_profiles_tested"] == 96, "wrong ledger count")
    require(search["systems_tested"] == 576, "wrong system count")
    require(search["structural_pass_candidates"] == 576, "wrong structural pass count")
    require(search["slot_profiles_tested"] == 127800, "wrong slot profile count")
    require(search["actual_zero_slot_profiles"] == 0, "unexpected actual zero slot")
    require(search["pair_projection_clear_actual_slots"] == 0, "unexpected pair-clear slot")
    require(search["proxy_positive_actual_slots"] == 0, "unexpected proxy-positive slot")
    require(search["best_template_id"] == "ledgerpert_base", "wrong best template")
    require(search["best_perturbation_id"] == "base", "wrong best perturbation")
    require(search["best_kernel_coefficients"] == [0, 0, 0], "wrong best coefficients")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best assignment")
    require(search["best_slot_nonzero_rows"] == 2, "wrong best residual count")
    require(search["best_forced_pair_count"] == 10, "wrong best forced-pair count")
    require(search["best_failure_mode"] == "LEDGERPERT_SLOT_NOT_KERNEL", "wrong best failure")

    candidate = record["best_candidate"]
    require(candidate["perturbation_id"] == "base", "wrong candidate perturbation")
    require(candidate["kernel_coefficients"] == [0, 0, 0], "wrong candidate coefficients")
    require(candidate["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(candidate["pair7_counts"] == [253, 253, 253, 253, 253], "pair7 mismatch")
    require(candidate["max_pair_count"] == 253, "max pair mismatch")
    require(candidate["functional_span_rank"] == 6, "functional span mismatch")
    require(candidate["forced_functional_identities"] == 0, "unexpected forced identity")
    require(candidate["best_profile"]["basis_id"] == "slot_union_142_6_8_10_12_15_16", "wrong best basis")
    require(candidate["best_profile"]["proxy_kernel_slot"] == 3, "wrong best slot")
    require(candidate["best_profile"]["slot_nonzero_rows"] == 2, "wrong profile residual count")
    require(candidate["best_profile"]["forced_pair_count"] == 10, "wrong profile forced-pair count")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "ledger profiles tested = 96",
        "actual zero-slot profiles = 0",
        "best slot nonzero rows = 2",
        "forced pair count = 10",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "ledger_profiles_tested": search["ledger_profiles_tested"],
        "actual_zero_slot_profiles": search["actual_zero_slot_profiles"],
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
        print(f"PASS: M1 a=327 realization-aware ledger perturbation (status={result['proof_status']})")


if __name__ == "__main__":
    main()
