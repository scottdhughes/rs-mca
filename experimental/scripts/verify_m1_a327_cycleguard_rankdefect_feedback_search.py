#!/usr/bin/env python3
"""Verify the M1 a=327 cycleguard rank-defect feedback ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_cycleguard_rankdefect_feedback_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_cycleguard_rankdefect_feedback_search.md")

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
    require(record["source_commit"] == "cf761a0", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / CYCLEG_RANKDEFECT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_exact_audit"]
    require(previous["matrix_shape"] == [993, 752], "wrong previous matrix")
    require(previous["rank"] == 752, "wrong previous rank")
    require(previous["nullity"] == 0, "wrong previous nullity")
    require(previous["failure_mode"] == "CYCLEG_EXACT_NULLITY_ZERO", "wrong previous failure")

    search = record["rankdefect_feedback_search"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["front_checkpoint_commit"] == "0fc5a00", "wrong front checkpoint")
    require(search["front_source_commit"] == "a63ab87", "wrong front source")
    require(search["front_basis_profiles_tested"] == 876, "wrong front basis count")
    require(search["front_exact_pairclear_rank_slack_profiles"] == 80, "wrong front rank-slack count")
    require(search["exact_pairclear_rank_slack_summaries"] == 40, "wrong summary count")
    require(search["proxy_ranked_profiles"] == 40, "wrong ranked count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positives")
    require(search["best_proxy_rank"] == 536, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_failure_mode"] == "CYCLEG_RANKDEFECT_PROXY_FULL_RANK", "wrong failure mode")
    require(search["profile_failure_counts"] == {"CYCLEG_RANKDEFECT_PROXY_FULL_RANK": 40}, "wrong failure counts")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P24_shear_c0_d1", "wrong best template")
    require(best["basis_id"] == "basisaware_0_1_2_3_4_7", "wrong best basis")
    require(best["proxy_matrix_shape"] == [777, 536], "wrong best matrix")
    require(best["proxy_rank"] == 536, "wrong best rank")
    require(best["proxy_nullity"] == 0, "wrong best nullity")
    require(best["best_chamber_forced_pairs"] == [], "best chamber forced pairs")
    require(best["best_chamber_inactive_rank"] == 4, "wrong chamber inactive rank")

    require(len(record["ranked_profiles"]) == 40, "wrong ranked profile rows")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "CYCLEG_RANKDEFECT_PROXY_FULL_RANK",
        "40 banked exact pair-clear rank-slack summaries",
        "proxy rank/nullity = 536 / 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "proxy_ranked_profiles": search["proxy_ranked_profiles"],
        "proxy_positive_profiles": search["proxy_positive_profiles"],
        "best_template_id": best["template_id"],
        "best_basis_id": best["basis_id"],
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
        print(f"PASS: M1 a=327 cycleguard rank-defect feedback (status={result['proof_status']})")


if __name__ == "__main__":
    main()
