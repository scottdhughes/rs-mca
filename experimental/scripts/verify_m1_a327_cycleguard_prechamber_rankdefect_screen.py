#!/usr/bin/env python3
"""Verify the M1 a=327 cycleguard pre-chamber rank-defect screen ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_cycleguard_prechamber_rankdefect_screen.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_cycleguard_prechamber_rankdefect_screen.md")

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
    require(record["source_commit"] == "f220bb6", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / CYCLEG_PRECHAMBER_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_generation_search"]
    require(previous["basis_profiles_scored"] == 636, "wrong previous score count")
    require(previous["proxy_ranked_profiles"] == 8, "wrong previous ranked count")
    require(previous["proxy_positive_profiles"] == 0, "wrong previous positive count")
    require(previous["best_proxy_rank"] == 678, "wrong previous rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous nullity")
    require(previous["failure_mode"] == "CYCLEG_RANKGEN_PROXY_FULL_RANK", "wrong previous failure")

    search = record["prechamber_rankdefect_screen"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["basis_profiles_collected"] == 96, "wrong collected count")
    require(search["proxy_ranked_profiles"] == 8, "wrong ranked count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positives")
    require(search["best_proxy_rank"] == 345, "wrong best rank")
    require(search["best_proxy_nullity"] == 0, "wrong best nullity")
    require(search["best_failure_mode"] == "CYCLEG_PRECHAMBER_PROXY_FULL_RANK", "wrong failure")
    require(search["cheap_shape_histogram"] == {"241": 96}, "wrong shape histogram")
    require(search["profile_failure_counts"] == {"CYCLEG_PRECHAMBER_PROXY_FULL_RANK": 8}, "wrong failure counts")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P12_shear_c0_d16", "wrong best template")
    require(best["basis_id"] == "basisaware_0_1_2_3_4_5", "wrong best basis")
    require(best["proxy_matrix_shape"] == [586, 345], "wrong best matrix")
    require(best["proxy_rank"] == 345, "wrong best proxy rank")
    require(best["proxy_nullity"] == 0, "wrong best proxy nullity")
    require(best["chamber_sampled"] is False, "chamber should not be sampled")

    require(len(record["proxy_ranked_profiles"]) == 8, "wrong ranked profile length")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "CYCLEG_PRECHAMBER_PROXY_FULL_RANK",
        "basis profiles collected = 96",
        "proxy rank/nullity = 345 / 0",
        "chamber_sampled = false",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "basis_profiles_collected": search["basis_profiles_collected"],
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
        print(f"PASS: M1 a=327 cycleguard pre-chamber screen (status={result['proof_status']})")


if __name__ == "__main__":
    main()
