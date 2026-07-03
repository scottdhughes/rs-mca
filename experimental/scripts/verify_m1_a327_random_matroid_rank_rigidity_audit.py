#!/usr/bin/env python3
"""Verify the M1 a=327 random-matroid rank-rigidity audit ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_random_matroid_rank_rigidity_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_random_matroid_rank_rigidity_audit.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "global rank rigidity outside the tested proxy front",
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
    require(record["source_commit"] == "f50b089", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    v3 = record["rank_feedback_v3"]
    require(v3["systems_tested"] == 96, "wrong v3 system count")
    require(v3["structural_pass_candidates"] == 84, "wrong v3 structural count")
    require(v3["proxy_candidates_tested"] == 8, "wrong v3 proxy candidate count")
    require(v3["proxy_basis_profiles_tested"] == 16, "wrong v3 profile count")
    require(v3["proxy_positive_candidates"] == 0, "unexpected v3 proxy-positive candidate")
    require(v3["best_template_id"] == "random_matroid_v3_seed_017_m6", "wrong v3 best")
    require(v3["best_proxy_rank"] == 1348, "wrong v3 best rank")
    require(v3["best_proxy_nullity"] == 0, "wrong v3 best nullity")

    audit = record["rank_rigidity_audit"]
    require(audit["proxy_profiles_audited"] == 16, "wrong profile audit count")
    require(audit["full_column_rank_profiles"] == 16, "wrong full-rank count")
    require(audit["proxy_positive_profiles"] == 0, "unexpected positive profile")
    require(audit["min_row_surplus"] == 241, "wrong min row surplus")
    require(audit["max_row_surplus"] == 241, "wrong max row surplus")
    require(audit["min_q_variable_count"] == 1348, "wrong min q count")
    require(audit["max_q_variable_count"] == 1475, "wrong max q count")
    require(audit["matrix_shape_counts"] == {
        "1589x1348": 4,
        "1629x1388": 4,
        "1672x1431": 4,
        "1716x1475": 4,
    }, "wrong matrix shape counts")
    require(audit["basis_counts"] == {
        "deterministic_random_basis_2": 4,
        "deterministic_random_basis_4": 4,
        "deterministic_random_basis_7": 8,
    }, "wrong basis counts")
    require(audit["best_failure_mode"] == "RANK_RIGIDITY_PROXY_FRONT_FULL_COLUMN_RANK", "wrong audit failure")
    for profile in audit["proxy_profiles"]:
        require(profile["proxy_rank"] == profile["q_variable_count"], "profile not full column rank")
        require(profile["proxy_nullity"] == 0, "profile has proxy nullity")
        require(profile["row_surplus"] == 241, "profile row surplus mismatch")

    for phrase in [
        "16 proxy basis profiles",
        "full column rank",
        "row surplus = 241",
        "not a global",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "proxy_profiles_audited": audit["proxy_profiles_audited"],
        "full_column_rank_profiles": audit["full_column_rank_profiles"],
        "proxy_positive_profiles": audit["proxy_positive_profiles"],
        "best_failure_mode": audit["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 random-matroid rank-rigidity audit (status={result['proof_status']})")


if __name__ == "__main__":
    main()
