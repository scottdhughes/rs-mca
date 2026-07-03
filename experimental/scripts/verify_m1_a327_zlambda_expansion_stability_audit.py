#!/usr/bin/env python3
"""Verify the M1 a=327 Z_lambda expansion-stability audit ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_zlambda_expansion_stability_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_zlambda_expansion_stability_audit.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
}
ALLOWED_FAILURES = {
    "ZEXP_COEFFICIENT_FULL_RANK",
    "ZEXP_BASIS_UNION_TOO_LARGE",
    "ZEXP_FORCED_PAIR_EQUALITY",
    "ZEXP_STABLE_LIFT_TARGET",
    "ZEXP_NO_RIGHT_KERNEL_PROFILES",
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
    require(record["agreement_target"] == 327, "wrong target")
    require(record["source_commit"] == "b3d6a79", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / ZEXP_EXPANSION_UNSTABLE / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["joint_template_search"]
    require(previous["systems_tested"] == 216, "wrong previous systems")
    require(previous["right_kernel_positive_candidates"] == 6, "wrong previous right-kernel positives")
    require(previous["proxy_positive_candidates"] == 0, "wrong previous proxy positives")
    require(previous["best_proxy_rank"] == 277, "wrong previous best proxy rank")
    require(previous["best_proxy_nullity"] == 0, "wrong previous best proxy nullity")
    require(previous["best_failure_mode"] == "JOINT_TEMPLATE_PROXY_FULL_RANK", "wrong previous failure")

    audit = record["zlambda_expansion_audit"]
    require(audit["profiles_audited"] == 30, "wrong audited profile count")
    require(audit["stable_lift_targets"] == 0, "unexpected stable lift target")
    require(audit["coefficient_kernel_profiles"] == 30, "wrong GF17 kernel count")
    require(audit["proxy_characteristic_kernel_profiles"] == 6, "wrong GF12289 kernel count")
    require(audit["best_template_id"] == "single_outside_w7_v1", "wrong best template")
    require(audit["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(audit["best_basis_id"] == "max_support_basis", "wrong best basis")
    require(audit["best_basis_zero_union_size"] == 327, "wrong best union size")
    require(audit["best_stable_common_multiplier_dimension"] == 0, "wrong stable multiplier dimension")
    require(audit["best_forced_pair_count"] == 15, "wrong forced-pair count")
    require(audit["best_failure_mode"] == "ZEXP_BASIS_UNION_TOO_LARGE", "wrong best failure")
    require(audit["failure_counts"] == {"ZEXP_BASIS_UNION_TOO_LARGE": 30}, "failure counts mismatch")
    require(set(audit["failure_counts"]).issubset(ALLOWED_FAILURES), "bad failure label")
    require(len(audit["profile_summaries"]) == 30, "profile summary count mismatch")

    best = record["best_profile"]
    require(best["template_id"] == "single_outside_w7_v1", "best template mismatch")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "best strategy mismatch")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "best support mismatch")
    require(best["pair7_counts"] == [253, 253, 253, 253, 253], "best pair7 mismatch")
    require(best["max_pair_count"] == 253, "best max pair mismatch")
    require(best["functional_classes"] == 14, "best functional class count mismatch")
    require(best["functional_span_rank"] == 6, "best span rank mismatch")
    profile = best["profile_audit"]
    require(profile["basis_id"] == "max_support_basis", "wrong profile basis")
    require(profile["basis_class_indices"] == [0, 1, 2, 3, 4, 5], "wrong basis indices")
    require(profile["basis_support_sizes"] == [253, 216, 216, 216, 179, 179], "wrong basis supports")
    require(profile["coefficient_matrix_shape"] == [8, 6], "wrong coefficient matrix shape")
    require(profile["coefficient_rank_gf17"] == 5, "wrong GF17 coefficient rank")
    require(profile["coefficient_nullity_gf17"] == 1, "wrong GF17 coefficient nullity")
    require(profile["coefficient_rank_gf12289"] == 5, "wrong GF12289 coefficient rank")
    require(profile["coefficient_nullity_gf12289"] == 1, "wrong GF12289 coefficient nullity")
    require(profile["kernel_basis"] == [[1, 1, 1, 1, 1, 1]], "wrong kernel basis")
    require(profile["basis_zero_union_size"] == 327, "wrong basis union size")
    require(profile["basis_zero_intersection_size"] == 0, "wrong basis intersection size")
    require(profile["stable_common_multiplier_dimension"] == 0, "wrong stable dimension")
    require(profile["best_forced_pair_count"] == 15, "wrong best forced-pair count")
    require(
        profile["best_forced_pairs"]
        == [
            "P23",
            "P24",
            "P25",
            "P26",
            "P27",
            "P34",
            "P35",
            "P36",
            "P37",
            "P45",
            "P46",
            "P47",
            "P56",
            "P57",
            "P67",
        ],
        "wrong forced-pair list",
    )
    require(record["candidate"]["constructed"] is False, "unexpected constructed candidate")

    for phrase in [
        "profiles audited = 30",
        "stable lift targets = 0",
        "coefficient-kernel profiles over GF(17) = 30",
        "basis-zero union size = 327",
        "stable common multiplier dimension = 0",
        "forced pair count = 15",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "profiles_audited": audit["profiles_audited"],
        "stable_lift_targets": audit["stable_lift_targets"],
        "coefficient_kernel_profiles": audit["coefficient_kernel_profiles"],
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
        print(f"PASS: M1 a=327 Z_lambda expansion audit (status={result['proof_status']})")


if __name__ == "__main__":
    main()
