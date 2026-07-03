#!/usr/bin/env python3
"""Verify the M1 a=327 Z_lambda stable-basis relation-search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_zlambda_stable_basis_relation_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_zlambda_stable_basis_relation_search.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
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
    require(record["source_commit"] == "06d5270", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / ZREL_STABLE_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_zlambda_stable_generator"]
    require(previous["systems_tested"] == 216, "wrong previous systems")
    require(previous["basis_profiles_tested"] == 13440, "wrong previous basis profiles")
    require(previous["coefficient_kernel_profiles"] == 30, "wrong previous coefficient kernels")
    require(previous["stable_basis_union_profiles"] == 0, "unexpected previous stable union")
    require(previous["best_failure_mode"] == "ZSTABLE_BASIS_UNION_TOO_LARGE", "wrong previous failure")

    search = record["stable_basis_relation_search"]
    require(search["templates_tested"] == 36, "wrong template count")
    require(search["systems_tested"] == 216, "wrong system count")
    require(search["structural_pass_candidates"] == 210, "wrong structural-pass count")
    require(search["stable_basis_combinations"] == 23663322, "wrong stable combination count")
    require(search["stable_basis_profiles_tested"] == 12312, "wrong stable profile count")
    require(search["stable_coefficient_kernel_profiles"] == 0, "unexpected stable coefficient kernel")
    require(search["pair_projection_clear_profiles"] == 0, "unexpected pair-clear profile")
    require(search["proxy_candidates_tested"] == 0, "unexpected proxy candidate")
    require(search["proxy_positive_candidates"] == 0, "unexpected proxy positive")
    require(search["best_template_id"] == "single_outside_w7_v0", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(search["best_basis_zero_union_size"] is None, "unexpected best union")
    require(search["best_stable_common_multiplier_dimension"] is None, "unexpected stable dimension")
    require(search["best_forced_pair_count"] is None, "unexpected forced-pair count")
    require(search["best_proxy_rank"] is None, "unexpected proxy rank")
    require(search["best_proxy_nullity"] is None, "unexpected proxy nullity")
    require(search["best_failure_mode"] == "ZREL_STABLE_COEFFICIENT_FULL_RANK", "wrong best failure")
    require(search["failure_counts"] == {"ZREL_LOW_FUNCTIONAL_SPAN": 6, "ZREL_STABLE_COEFFICIENT_FULL_RANK": 210}, "failure counts mismatch")
    require(search["screen_counts"] == {"JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN": 6, "JOINT_TEMPLATE_STRUCTURAL_PASS": 210}, "screen counts mismatch")
    require(len(search["candidate_summaries"]) == 216, "candidate count mismatch")

    best = record["best_candidate"]
    require(best["template_id"] == "single_outside_w7_v0", "best template mismatch")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "best strategy mismatch")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "best support mismatch")
    require(best["pair7_counts"] == [233, 233, 233, 233, 233], "best pair7 mismatch")
    require(best["max_pair_count"] == 233, "best max pair mismatch")
    require(best["functional_classes"] == 17, "best functional class mismatch")
    require(best["functional_span_rank"] == 6, "best span mismatch")
    require(best["stable_basis_combinations"] == 515, "best stable combinations mismatch")
    require(best["stable_basis_profiles_tested"] == 95, "best stable profile count mismatch")
    require(best["stable_coefficient_kernel_profiles"] == 0, "unexpected best stable kernel")
    require(best["best_failure_mode"] == "ZREL_STABLE_COEFFICIENT_FULL_RANK", "best failure mismatch")
    require(best["best_profile"] is None, "unexpected best profile")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 216",
        "stable basis combinations = 23,663,322",
        "stable basis profiles tested = 12,312",
        "stable coefficient-kernel profiles = 0",
        "pair-projection-clear profiles = 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "stable_basis_profiles_tested": search["stable_basis_profiles_tested"],
        "stable_coefficient_kernel_profiles": search["stable_coefficient_kernel_profiles"],
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
        print(f"PASS: M1 a=327 Z_lambda stable-basis relation search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
