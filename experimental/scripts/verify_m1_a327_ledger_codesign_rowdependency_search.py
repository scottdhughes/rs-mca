#!/usr/bin/env python3
"""Verify the M1 a=327 ledger-codesign row-dependency search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_ledger_codesign_rowdependency_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_ledger_codesign_rowdependency_search.md")

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


def require_guard_profile(row: dict[str, Any], *, q_count: int) -> None:
    require(row["support_vector"] == [TARGET_AGREEMENT] * 7, "wrong support vector")
    require(row["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(row["max_pair_count"] == 253, "wrong max pair count")
    require(row["q_variable_count"] == q_count, "wrong q-variable count")
    require(row["q_variable_budget_ok"] is True, "profile below q-variable floor")
    require(row["functional_span_rank"] == 6, "wrong functional span rank")
    require(row["forced_functional_identities"] == 0, "unexpected forced identities")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET_AGREEMENT, "wrong target")
    require(record["source_commit"] == "af2492f", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / ROWDEP_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_ledger_codesign"]
    require(previous["systems_tested"] == 192, "wrong previous system count")
    require(previous["q_budget_profiles"] == 12, "wrong previous q-budget count")
    require(previous["best_q_variable_count"] == 771, "wrong previous q-variable count")
    require(previous["best_proxy_rank"] == 771, "wrong previous proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous proxy nullity")
    require(previous["failure_mode"] == "LCODESIGN_PROXY_FULL_RANK", "wrong previous failure")

    search = record["rowdependency_search"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["q_variable_floor"] == 350, "wrong q-variable floor")
    require(search["max_templates"] == 96, "wrong template limit")
    require(search["max_systems"] == 240, "wrong system limit")
    require(search["profile_candidate_limit"] == 40, "wrong profile candidate limit")
    require(search["basis_profiles_per_candidate"] == 4, "wrong basis profiles per candidate")
    require(search["profile_rank_limit"] == 12, "wrong proxy rank limit")
    require(search["structural_pass_systems"] == 240, "wrong structural pass count")
    require(search["basis_profiles_constructed"] == 160, "wrong basis profile count")
    require(search["dependency_positive_profiles"] == 160, "wrong dependency-positive count")
    require(search["dependency_q_budget_profiles"] == 18, "wrong dependency q-budget count")
    require(search["proxy_ranked_profiles"] == 12, "wrong proxy-ranked count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy-positive profile")
    require(search["best_dependency_score"] == 1954, "wrong best dependency score")
    require(search["best_dependency_q_variable_count"] == 802, "wrong dependency q count")
    require(search["best_q_variable_count"] == 771, "wrong best proxy q count")
    require(search["best_proxy_rank"] == 771, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_failure_mode"] == "ROWDEP_PROXY_FULL_RANK", "wrong best failure")
    require(search["profile_failure_counts"] == {"ROWDEP_PROXY_FULL_RANK": 12}, "wrong failure counts")

    dependency = record["best_dependency_profile"]
    require(dependency["template_id"] == "lcodesign_0002_basis_simple", "wrong dependency template")
    require(dependency["basis_id"] == "basisaware_1_4_7_8_9_10", "wrong dependency basis")
    require_guard_profile(dependency, q_count=802)
    require(dependency["dependency_score"] == 1954, "wrong dependency score")
    require(dependency["matrix_shape"] == [1043, 802], "wrong dependency matrix shape")
    require(dependency["nested_support_pairs"] == 4, "wrong dependency nested-support pairs")
    require(dependency["support_overlap_total"] == 1025, "wrong dependency overlap total")
    require(dependency["support_overlap_nonzero_pairs"] == 8, "wrong dependency overlap pair count")
    require(dependency["repeated_coordinate_pairs"] == 0, "unexpected dependency coordinate repeats")
    require(dependency["repeated_support_pairs"] == 0, "unexpected dependency support repeats")
    require(dependency["repeated_support_coordinate_pairs"] == 0, "unexpected dependency support-coordinate repeats")

    best = record["best_profile"]
    require(best["template_id"] == "lcodesign_0001_basis_simple", "wrong best template")
    require(best["basis_id"] == "basisaware_1_4_7_8_9_10", "wrong best basis")
    require_guard_profile(best, q_count=771)
    require(best["dependency_score"] == 1923, "wrong best dependency score")
    require(best["matrix_shape"] == [1012, 771], "wrong best matrix shape")
    require(best["proxy_matrix_shape"] == [1012, 771], "wrong best proxy matrix shape")
    require(best["proxy_rank"] == 771, "wrong best proxy rank")
    require(best["proxy_nullity"] == 0, "wrong best proxy nullity")
    require(best["nested_support_pairs"] == 2, "wrong best nested-support pairs")
    require(best["support_overlap_total"] == 1080, "wrong best overlap total")
    require(best["support_overlap_nonzero_pairs"] == 9, "wrong best overlap pair count")
    require(best["repeated_coordinate_pairs"] == 0, "unexpected best coordinate repeats")
    require(best["repeated_support_pairs"] == 0, "unexpected best support repeats")
    require(best["repeated_support_coordinate_pairs"] == 0, "unexpected best support-coordinate repeats")
    require(best["best_failure_mode"] == "ROWDEP_PROXY_FULL_RANK", "wrong best profile failure")
    require(best["chamber_sampled"] is False, "chamber should not be sampled")

    require(len(record["proxy_ranked_profiles"]) == 12, "wrong proxy-ranked profile list length")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "ROWDEP_PROXY_FULL_RANK",
        "structural-pass systems = 240",
        "dependency-positive profiles = 160",
        "dependency q-budget profiles = 18",
        "best dependency score = 1954",
        "proxy rank/nullity = 771 / 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "structural_pass_systems": search["structural_pass_systems"],
        "basis_profiles_constructed": search["basis_profiles_constructed"],
        "dependency_positive_profiles": search["dependency_positive_profiles"],
        "dependency_q_budget_profiles": search["dependency_q_budget_profiles"],
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
        print(f"PASS: M1 a=327 ledger-codesign row-dependency search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
