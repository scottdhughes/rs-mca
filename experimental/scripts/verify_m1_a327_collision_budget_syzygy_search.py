#!/usr/bin/env python3
"""Verify the M1 a=327 collision-budget syzygy search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_collision_budget_syzygy_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_collision_budget_syzygy_search.md")

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
    require(record["source_commit"] == "856d30a", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / SYZYGY_NO_SMALL_ROW_BLOCK_DEPENDENCY / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_collision_budget_codesign"]
    require(previous["basis_profiles_constructed"] == 240, "wrong previous profile count")
    require(previous["collision_budget_profiles"] == 240, "wrong previous collision-budget count")
    require(previous["proxy_ranked_profiles"] == 12, "wrong previous proxy-ranked count")
    require(previous["proxy_positive_profiles"] == 0, "unexpected previous proxy positive")
    require(previous["best_q_variable_count"] == 851, "wrong previous q count")
    require(previous["best_proxy_rank"] == 851, "wrong previous proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous proxy nullity")
    require(previous["failure_mode"] == "CBUDGET_PROXY_FULL_RANK", "wrong previous failure")

    search = record["collision_budget_syzygy_search"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["q_variable_floor"] == 350, "wrong q floor")
    require(search["max_templates"] == 128, "wrong max templates")
    require(search["max_systems"] == 360, "wrong max systems")
    require(search["profile_candidate_limit"] == 60, "wrong candidate limit")
    require(search["groups_per_candidate"] == 8, "wrong groups per candidate")
    require(search["syzygy_profile_limit"] == 240, "wrong syzygy profile limit")
    require(search["proxy_rank_limit"] == 12, "wrong proxy rank limit")
    require(search["collision_budget_profiles_reconstructed"] == 240, "wrong reconstructed count")
    require(search["syzygy_profiles_scored"] == 240, "wrong scored count")
    require(search["syzygy_positive_profiles"] == 0, "unexpected syzygy positive")
    require(search["proxy_ranked_profiles"] == 0, "unexpected proxy rank")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positive")
    require(search["best_syzygy_score"] == 0, "wrong best syzygy score")
    require(search["best_projective_duplicate_pairs"] == 0, "wrong duplicate pair count")
    require(search["best_position_lowrank_deficiency"] == 0, "wrong position deficiency")
    require(search["best_support_position_lowrank_deficiency"] == 0, "wrong support-position deficiency")
    require(search["best_proxy_rank"] is None, "unexpected best proxy rank")
    require(search["best_proxy_nullity"] is None, "unexpected best proxy nullity")
    require(search["best_q_variable_count"] is None, "unexpected best proxy q count")
    require(search["best_failure_mode"] == "SYZYGY_NO_SMALL_ROW_BLOCK_DEPENDENCY", "wrong failure")

    best = record["best_scored_profile"]
    require(best["template_id"] == "lcodesign_0002_basis_simple", "wrong best template")
    require(best["basis_id"] == "collbudget_low_support_basis_support_0_11_6_7_10_5_2", "wrong best basis")
    require(best["q_variable_count"] == 851, "wrong best q")
    require(best["matrix_shape"] == [1092, 851], "wrong matrix shape")
    require(best["row_block_rows"] == 1092, "wrong row block rows")
    require(best["row_block_cols"] == 851, "wrong row block cols")
    require(best["collision_budget_success"] is True, "best not collision-budget")
    require(best["repeated_support_pairs"] == 1, "wrong support collision count")
    require(best["syzygy_score"] == 0, "wrong best profile syzygy score")
    require(best["syzygy_positive"] is False, "best profile syzygy positive unexpectedly")
    require(best["zero_rows"] == 0, "unexpected zero rows")
    require(best["projective_duplicate_pairs"] == 0, "unexpected projective duplicate rows")
    require(best["max_projective_multiplicity"] == 1, "unexpected projective multiplicity")
    require(best["position_blocks_tested"] == 216, "wrong position block count")
    require(best["position_lowrank_blocks"] == 0, "unexpected position low-rank blocks")
    require(best["support_position_blocks_tested"] == 74, "wrong support-position block count")
    require(best["support_position_lowrank_blocks"] == 0, "unexpected support-position low-rank blocks")
    require(best["support_blocks_tested"] == 5, "wrong support block count")
    require(best["support_lowrank_blocks"] == 0, "unexpected support low-rank blocks")

    require(record["best_syzygy_profile"] is None, "unexpected syzygy profile")
    require(record["best_profile"] is None, "unexpected proxy profile")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "SYZYGY_NO_SMALL_ROW_BLOCK_DEPENDENCY",
        "syzygy profiles scored = 240",
        "syzygy-positive profiles = 0",
        "projective duplicate pairs = 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "collision_budget_profiles_reconstructed": search["collision_budget_profiles_reconstructed"],
        "syzygy_profiles_scored": search["syzygy_profiles_scored"],
        "syzygy_positive_profiles": search["syzygy_positive_profiles"],
        "proxy_ranked_profiles": search["proxy_ranked_profiles"],
        "best_syzygy_score": search["best_syzygy_score"],
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
        print(f"PASS: M1 a=327 collision-budget syzygy search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
