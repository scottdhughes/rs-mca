#!/usr/bin/env python3
"""Verify the M1 a=327 prescribed functional-collision realization ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_prescribed_functional_collision_realization.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_prescribed_functional_collision_realization.md")

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
    require(record["source_commit"] == "af58bd0", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / PFCOLL_REALIZATION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_functional_collision_template_synthesis"]
    require(previous["best_proxy_rank"] == 851, "wrong previous proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous proxy nullity")
    require(previous["proxy_positive_profiles"] == 0, "wrong previous positive count")
    require(previous["failure_mode"] == "FCOLL_TEMPLATE_PROXY_FULL_RANK", "wrong previous failure")

    search = record["prescribed_functional_collision_realization"]
    require(search["proxy_prime"] == 12289, "wrong proxy prime")
    require(search["templates_tested"] == 180, "wrong template count")
    require(search["structural_pass_templates"] == 72, "wrong structural pass count")
    require(search["prescribed_collision_realized_templates"] == 72, "wrong realized template count")
    require(search["template_status_counts"] == {"TCHAMBER_FORCED_IDENTITY": 108, "TCHAMBER_STRUCTURAL_PASS": 72}, "wrong status counts")
    require(search["basis_profiles_constructed"] == 48, "wrong basis profile count")
    require(search["proxy_ranked_profiles"] == 8, "wrong ranked profile count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positives")
    require(search["best_realized_functional_classes"] == 11, "wrong best class count")
    require(search["best_proxy_rank"] == 129, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_failure_mode"] == "PFCOLL_REALIZATION_PROXY_FULL_RANK", "wrong best failure")
    require(search["profile_failure_counts"] == {"PFCOLL_REALIZATION_PROXY_FULL_RANK": 8}, "wrong profile failures")

    realized = record["best_realized_template"]
    require(realized["template_id"] == "pfcoll_0000_basis_simple", "wrong best realized template")
    require(realized["support_vector"] == [TARGET_AGREEMENT] * 7, "wrong support vector")
    require(realized["pair7_counts"] == [253, 253, 253, 253, 253], "wrong pair7 counts")
    require(realized["max_pair_count"] == 253, "wrong pair cap")
    require(realized["structural_status"] == "TCHAMBER_STRUCTURAL_PASS", "best template not structural pass")
    require(realized["prescribed_collision_realized"] is True, "best template not realized")
    require(realized["functional_classes"] == 11, "wrong realized class count")
    require(realized["raw_collision_excess"] == 1766, "wrong raw collision excess")
    require(realized["forced_functional_identities"] == 0, "unexpected forced identities")
    require(realized["functional_span_rank"] == 6, "wrong functional span")
    require(realized["template_equal_pairs"] == [], "unexpected equal template pairs")

    best = record["best_profile"]
    require(best["template_id"] == "pfcoll_0000_basis_simple", "wrong best profile template")
    require(best["basis_id"] == "basisaware_0_1_2_3_4_5", "wrong best basis")
    require(best["proxy_matrix_shape"] == [370, 129], "wrong proxy matrix shape")
    require(best["proxy_rank"] == 129, "wrong proxy rank")
    require(best["proxy_nullity"] == 0, "wrong proxy nullity")
    require(best["functional_classes"] == 11, "wrong profile class count")
    require(best["raw_collision_excess"] == 1766, "wrong profile collision excess")
    require(best["chamber_sampled"] is False, "chamber should not be sampled")

    require(len(record["proxy_ranked_profiles"]) == 8, "wrong ranked profile length")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "PFCOLL_REALIZATION_PROXY_FULL_RANK",
        "templates tested = 180",
        "prescribed collision realized templates = 72",
        "functional classes = 11",
        "proxy rank/nullity = 129 / 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "templates_tested": search["templates_tested"],
        "prescribed_collision_realized_templates": search["prescribed_collision_realized_templates"],
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
        print(f"PASS: M1 a=327 prescribed functional-collision realization (status={result['proof_status']})")


if __name__ == "__main__":
    main()
