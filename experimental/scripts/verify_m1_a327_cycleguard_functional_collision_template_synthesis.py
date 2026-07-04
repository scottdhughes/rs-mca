#!/usr/bin/env python3
"""Verify the M1 a=327 functional-collision template synthesis ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_cycleguard_functional_collision_template_synthesis.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_cycleguard_functional_collision_template_synthesis.md")

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
    require(record["source_commit"] == "f2b56ec", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / FCOLL_TEMPLATE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_dependency_forced_generator"]
    require(previous["forced_profiles_constructed"] == 96, "wrong previous forced count")
    require(previous["support_coordinate_collision_profiles"] == 0, "wrong previous support-coordinate collisions")
    require(previous["coordinate_collision_profiles"] == 0, "wrong previous coordinate collisions")
    require(previous["proxy_ranked_profiles"] == 8, "wrong previous ranked count")
    require(previous["proxy_positive_profiles"] == 0, "wrong previous positives")
    require(previous["best_proxy_rank"] == 678, "wrong previous rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous nullity")
    require(previous["failure_mode"] == "CYCLEG_DEP_FORCED_PROXY_FULL_RANK", "wrong previous failure")

    search = record["functional_collision_template_synthesis"]
    require(search["mutations_tested"] == 96, "wrong mutation count")
    require(search["structural_pass_mutations"] == 88, "wrong structural pass count")
    require(search["mutation_status_counts"] == {"TCHAMBER_LOW_FUNCTIONAL_SPAN": 8, "TCHAMBER_STRUCTURAL_PASS": 88}, "wrong status counts")
    require(search["basis_profiles_constructed"] == 32, "wrong basis profile count")
    require(search["proxy_ranked_profiles"] == 8, "wrong ranked count")
    require(search["proxy_positive_profiles"] == 0, "unexpected proxy positives")
    require(search["best_mutation_raw_collision_excess"] == 1759, "wrong best raw collision excess")
    require(search["best_mutation_functional_classes"] == 18, "wrong best class count")
    require(search["best_proxy_rank"] == 851, "wrong best rank")
    require(search["best_proxy_nullity"] == 0, "wrong best nullity")
    require(search["best_failure_mode"] == "FCOLL_TEMPLATE_PROXY_FULL_RANK", "wrong failure")
    require(search["profile_failure_counts"] == {"FCOLL_TEMPLATE_PROXY_FULL_RANK": 8}, "wrong profile failures")

    mutation = record["best_mutation"]
    require(mutation["structural_status"] == "TCHAMBER_STRUCTURAL_PASS", "best mutation not structural pass")
    require(mutation["raw_functional_rows"] == 1777, "wrong raw rows")
    require(mutation["functional_classes"] == 18, "wrong mutation class count")
    require(mutation["raw_collision_excess"] == 1759, "wrong mutation collision excess")
    require(mutation["forced_functional_identities"] == 0, "unexpected forced identities")
    require(mutation["functional_span_rank"] == 6, "wrong span rank")
    require(mutation["template_equal_pairs"] == [], "unexpected equal template pairs")

    best = record["best_profile"]
    require(best["template_id"] == "ninerow_P12_shear_c0_d1__fcoll_b0_m1_single_entry_delta", "wrong best template")
    require(best["basis_id"] == "basisaware_1_4_7_8_9_10", "wrong best basis")
    require(best["proxy_matrix_shape"] == [1092, 851], "wrong best matrix")
    require(best["proxy_rank"] == 851, "wrong best rank")
    require(best["proxy_nullity"] == 0, "wrong best nullity")
    require(best["raw_collision_excess"] == 1759, "wrong profile raw collision excess")
    require(best["functional_classes"] == 18, "wrong profile class count")
    require(best["chamber_sampled"] is False, "chamber should not be sampled")

    require(len(record["proxy_ranked_profiles"]) == 8, "wrong ranked profile length")
    require(record["candidate"]["constructed"] is False, "unexpected candidate")

    for phrase in [
        "FCOLL_TEMPLATE_PROXY_FULL_RANK",
        "mutations tested = 96",
        "structural-pass mutations = 88",
        "proxy rank/nullity = 851 / 0",
        "raw functional rows/classes = 1777 / 18",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "mutations_tested": search["mutations_tested"],
        "structural_pass_mutations": search["structural_pass_mutations"],
        "basis_profiles_constructed": search["basis_profiles_constructed"],
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
        print(f"PASS: M1 a=327 functional-collision template synthesis (status={result['proof_status']})")


if __name__ == "__main__":
    main()
