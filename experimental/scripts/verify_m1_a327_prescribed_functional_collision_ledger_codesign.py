#!/usr/bin/env python3
"""Verify the M1 a=327 prescribed functional-collision ledger-codesign ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_prescribed_functional_collision_ledger_codesign.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_prescribed_functional_collision_ledger_codesign.md")

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
    require(record["source_commit"] == "e6fb874", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / LCODESIGN_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_prescribed_functional_collision_realization"]
    require(previous["best_proxy_rank"] == 129, "wrong previous proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous proxy nullity")
    require(previous["best_q_variable_count"] == 129, "wrong previous q variable count")
    require(previous["failure_mode"] == "PFCOLL_REALIZATION_PROXY_FULL_RANK", "wrong previous failure")

    search = record["prescribed_functional_collision_ledger_codesign"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["q_variable_floor"] == 350, "wrong q floor")
    require(search["template_specs_tested"] == 96, "wrong template spec count")
    require(search["milp_feasible_templates"] == 96, "wrong feasible template count")
    require(search["systems_tested"] == 192, "wrong system count")
    require(search["structural_pass_systems"] == 192, "wrong structural pass count")
    require(search["system_status_counts"] == {"TCHAMBER_STRUCTURAL_PASS": 192}, "wrong system status counts")
    require(search["basis_profiles_constructed"] == 96, "wrong basis profile count")
    require(search["q_budget_profiles"] == 12, "wrong q-budget profile count")
    require(search["proxy_ranked_profiles"] == 10, "wrong ranked profile count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positives")
    require(search["best_structural_functional_classes"] == 11, "wrong best structural class count")
    require(search["best_q_variable_count"] == 771, "wrong best q variable count")
    require(search["best_proxy_rank"] == 771, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_failure_mode"] == "LCODESIGN_PROXY_FULL_RANK", "wrong best failure")
    require(search["profile_failure_counts"] == {"LCODESIGN_PROXY_FULL_RANK": 10}, "wrong profile failures")

    structural = record["best_structural_system"]
    require(structural["structural_status"] == "TCHAMBER_STRUCTURAL_PASS", "best structural system failed")
    require(structural["support_vector"] == [TARGET_AGREEMENT] * 7, "wrong support vector")
    require(structural["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(structural["max_pair_count"] == 253, "wrong pair cap")
    require(structural["functional_classes"] == 11, "wrong structural class count")
    require(structural["functional_span_rank"] == 6, "wrong span rank")
    require(structural["forced_functional_identities"] == 0, "unexpected forced identities")
    require(structural["template_equal_pairs"] == [], "unexpected equal template pairs")

    best = record["best_profile"]
    require(best["template_id"] == "lcodesign_0001_basis_simple", "wrong best template")
    require(best["basis_id"] == "basisaware_1_4_7_8_9_10", "wrong best basis")
    require(best["q_variable_count"] == 771, "wrong best q variable count")
    require(best["q_variable_budget_ok"] is True, "best profile below q budget")
    require(best["proxy_matrix_shape"] == [1012, 771], "wrong proxy matrix")
    require(best["proxy_rank"] == 771, "wrong proxy rank")
    require(best["proxy_nullity"] == 0, "wrong proxy nullity")
    require(best["functional_classes"] == 11, "wrong profile class count")
    require(best["raw_collision_excess"] == 1766, "wrong raw collision excess")
    require(best["chamber_sampled"] is False, "chamber should not be sampled")

    require(len(record["proxy_ranked_profiles"]) == 10, "wrong ranked profile length")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "LCODESIGN_PROXY_FULL_RANK",
        "systems tested = 192",
        "q-budget profiles = 12",
        "best q-variable count = 771",
        "proxy rank/nullity = 771 / 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "structural_pass_systems": search["structural_pass_systems"],
        "q_budget_profiles": search["q_budget_profiles"],
        "proxy_ranked_profiles": search["proxy_ranked_profiles"],
        "proxy_positive_profiles": search["proxy_positive_profiles"],
        "best_template_id": best["template_id"],
        "best_basis_id": best["basis_id"],
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
        print(f"PASS: M1 a=327 prescribed functional-collision ledger-codesign (status={result['proof_status']})")


if __name__ == "__main__":
    main()
