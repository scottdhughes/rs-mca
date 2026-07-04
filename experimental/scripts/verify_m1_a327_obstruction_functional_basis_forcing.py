#!/usr/bin/env python3
"""Verify the M1 a=327 obstruction-functional basis forcing ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_obstruction_functional_basis_forcing.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_obstruction_functional_basis_forcing.md")

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
    require(record["source_commit"] == "abb1956", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "ACTUAL_TEMPLATE_ROWSPACES_ONLY", "wrong realization status")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / BASISFORCE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_ledger_perturbation"]
    require(previous["commit"] == "abb1956", "wrong previous commit")
    require(previous["actual_zero_slot_profiles"] == 0, "unexpected previous zero slot")
    require(previous["best_failure_mode"] == "LEDGERPERT_SLOT_NOT_KERNEL", "wrong previous failure")

    search = record["basis_forcing_search"]
    require(search["target_functionals"]["primary_e4"] == [0, 0, 0, 1, 0, 0], "wrong primary target")
    require(search["target_functionals"]["secondary_residual"] == [0, 0, 0, 1, 4, 8], "wrong secondary target")
    require(search["target_modes"] == ["primary_e4", "both_residuals"], "wrong target modes")
    require(search["max_abs_coeff"] == 6, "wrong coefficient bound")
    require(search["ledger_profiles_tested"] == 96, "wrong ledger count")
    require(search["systems_tested"] == 576, "wrong system count")
    require(search["structural_pass_candidates"] == 576, "wrong structural count")
    require(search["forced_basis_combinations"] == 4608, "wrong forced-basis combo count")
    require(search["forced_basis_profiles_tested"] == 576, "wrong forced-basis profile count")
    require(search["coefficient_kernel_profiles"] == 0, "unexpected coefficient kernel")
    require(search["pair_projection_clear_profiles"] == 0, "unexpected pair-clear profile")
    require(search["proxy_results_tested"] == 0, "unexpected proxy result")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy-positive profile")
    require(search["best_template_id"] == "ledgerpert_base", "wrong best template")
    require(search["best_perturbation_id"] == "base", "wrong best perturbation")
    require(search["best_kernel_coefficients"] == [0, 0, 0], "wrong best coefficients")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best assignment")
    require(search["best_target_mode"] is None, "unexpected best target mode")
    require(search["best_forced_pair_count"] is None, "unexpected forced-pair count")
    require(search["best_coefficient_nullity"] is None, "unexpected coefficient nullity")
    require(search["best_failure_mode"] == "BASISFORCE_COEFFICIENT_FULL_RANK", "wrong best failure")
    require(search["failure_counts"] == {"BASISFORCE_COEFFICIENT_FULL_RANK": 576}, "wrong failure counts")

    best = record["best_candidate"]
    require(best["perturbation_id"] == "base", "wrong best perturbation row")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(best["pair7_counts"] == [253, 253, 253, 253, 253], "pair7 mismatch")
    require(best["functional_span_rank"] == 6, "span mismatch")
    require(best["forced_functional_identities"] == 0, "unexpected forced identity")
    require(best["coefficient_kernel_profiles"] == 0, "unexpected best coefficient kernel")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 576",
        "forced basis profiles tested = 576",
        "coefficient-kernel profiles = 0",
        "best failure = BASISFORCE_COEFFICIENT_FULL_RANK",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "forced_basis_profiles_tested": search["forced_basis_profiles_tested"],
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
        print(f"PASS: M1 a=327 obstruction-functional basis forcing (status={result['proof_status']})")


if __name__ == "__main__":
    main()
