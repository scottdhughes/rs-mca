#!/usr/bin/env python3
"""Verify the M1 a=327 basis/kernel co-design ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_basis_kernel_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_basis_kernel_codesign.md")

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
    require(record["source_commit"] == "cfc4f6d", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "ACTUAL_TEMPLATE_ROWSPACES_ONLY", "wrong realization status")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / CODESIGN_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_basis_forcing"]
    require(previous["commit"] == "cfc4f6d", "wrong previous commit")
    require(previous["coefficient_kernel_profiles"] == 0, "unexpected previous coefficient kernel")
    require(previous["best_failure_mode"] == "BASISFORCE_COEFFICIENT_FULL_RANK", "wrong previous failure")

    search = record["basis_kernel_codesign"]
    require(search["max_specs"] == 36, "wrong max specs")
    require(search["systems_tested"] == 216, "wrong systems tested")
    require(search["structural_pass_candidates"] == 210, "wrong structural pass count")
    require(search["target_present_candidates"] == 144, "wrong target-present count")
    require(search["forced_basis_combinations"] == 257298, "wrong forced-basis combo count")
    require(search["forced_basis_profiles_tested"] == 4530, "wrong forced-basis profile count")
    require(search["coefficient_kernel_profiles"] == 0, "unexpected coefficient kernel")
    require(search["pair_projection_clear_profiles"] == 0, "unexpected pair-clear profile")
    require(search["proxy_results_tested"] == 0, "unexpected proxy result")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy-positive profile")
    require(search["best_template_id"] == "single_outside_w2_v3", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best assignment")
    require(search["best_target_mode"] is None, "unexpected target mode")
    require(search["best_forced_pair_count"] is None, "unexpected forced-pair count")
    require(search["best_coefficient_nullity"] is None, "unexpected coefficient nullity")
    require(search["best_failure_mode"] == "CODESIGN_COEFFICIENT_FULL_RANK", "wrong best failure")
    require(
        search["failure_counts"]
        == {
            "CODESIGN_COEFFICIENT_FULL_RANK": 132,
            "CODESIGN_LOW_FUNCTIONAL_SPAN": 6,
            "CODESIGN_NO_STABLE_TARGET_BASIS": 12,
            "CODESIGN_TARGET_FUNCTIONAL_MISSING": 66,
        },
        "wrong failure counts",
    )
    require(
        search["screen_counts"] == {"JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN": 6, "JOINT_TEMPLATE_STRUCTURAL_PASS": 210},
        "wrong screen counts",
    )

    best = record["best_candidate"]
    require(best["template_id"] == "single_outside_w2_v3", "wrong best candidate template")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "wrong best candidate assignment")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(best["pair7_counts"] == [225, 225, 225, 225, 225], "pair7 mismatch")
    require(best["max_pair_count"] == 225, "max pair mismatch")
    require(best["target_functional_present_modes"] == ["primary_e4"], "wrong target-present modes")
    require(best["target_functional_missing_modes"] == ["both_residuals"], "wrong target-missing modes")
    require(best["forced_basis_combinations"] == 973, "wrong best combo count")
    require(best["forced_basis_profiles_tested"] == 72, "wrong best profile count")
    require(best["coefficient_kernel_profiles"] == 0, "unexpected best coefficient kernel")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 216",
        "target-present candidates = 144",
        "forced basis profiles tested = 4530",
        "coefficient-kernel profiles = 0",
        "best failure = CODESIGN_COEFFICIENT_FULL_RANK",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "coefficient_kernel_profiles": search["coefficient_kernel_profiles"],
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
        print(f"PASS: M1 a=327 basis/kernel co-design (status={result['proof_status']})")


if __name__ == "__main__":
    main()
