#!/usr/bin/env python3
"""Verify the M1 a=327 prescribed Z_lambda-stable proxy audit ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_prescribed_zlambda_stable_proxy_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_prescribed_zlambda_stable_proxy_audit.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "realized exact template vectors for the prescribed coefficients",
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
    require(record["source_commit"] == "70b744e", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["realization_status"] == "SYNTHETIC_FUNCTIONAL_PROXY_TARGET", "wrong realization status")
    require(record["proof_status"] == "EXACT_EXTRACTION_NO_A327 / PZREL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL", "wrong proof status")

    candidate = record["input_candidate"]
    require(candidate["template_id"] == "single_outside_w6_v0", "wrong template")
    require(candidate["assignment_strategy"] == "signature_fiber_blocks", "wrong assignment")
    require(candidate["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "support mismatch")
    require(candidate["pair7_counts"] == [206, 206, 206, 206, 206], "pair7 mismatch")
    require(candidate["max_pair_count"] == 206, "max pair mismatch")

    profile = record["prescribed_profile"]
    require(profile["source_basis_id"] == "pzrel_union_85_14_15_16_17_18_19", "wrong source basis")
    require(profile["prescribed_kernel_id"] == "random_kernel_0", "wrong kernel id")
    require(profile["prescribed_kernel_vector"] == [1, 9, 4, 9, 13, 14], "wrong kernel vector")
    require(profile["basis_class_indices"] == [14, 15, 16, 17, 18, 19], "wrong basis indices")
    require(profile["basis_support_sizes"] == [29, 28, 21, 6, 1, 1], "wrong basis supports")
    require(profile["basis_zero_union_size"] == 85, "wrong basis union")
    require(profile["stable_common_multiplier_dimension"] == 171, "wrong stable dimension")
    require(profile["q_variable_count"] == 1450, "wrong q variable count")
    require(profile["coefficient_matrix_shape"] == [14, 6], "wrong coefficient shape")
    require(profile["coefficient_rank"] == 5, "wrong coefficient rank")
    require(profile["right_kernel_nullity"] == 1, "wrong right-kernel nullity")
    require(profile["right_kernel_verified"] is True, "right kernel not verified")
    require(profile["forced_pair_count"] == 0, "unexpected forced pair")
    require(profile["forced_pairs"] == [], "forced pair list nonempty")

    proxy = record["proxy_audit"]
    require(proxy["status"] == "PROXY_RANK_PASS", "proxy did not pass")
    require(proxy["timeout"] is False, "unexpected timeout")
    require(proxy["best_failure_mode"] == "PZREL_PROXY_FULL_RANK", "wrong proxy failure")
    result = proxy["proxy_result"]
    require(result["proxy_field"] == "GF(12289)", "wrong proxy field")
    require(result["proxy_matrix_shape"] == [1691, 1450], "wrong proxy shape")
    require(result["proxy_rank"] == 1450, "wrong proxy rank")
    require(result["proxy_nullity"] == 0, "wrong proxy nullity")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "proxy matrix shape = `1691 x 1450`",
        "proxy rank/nullity = `1450 / 0`",
        "basis-zero union size = 85",
        "stable common multiplier dimension = 171",
        "forced pair count = 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "realization_status": record["realization_status"],
        "proxy_rank": result["proxy_rank"],
        "proxy_nullity": result["proxy_nullity"],
        "best_failure_mode": proxy["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 prescribed Z_lambda-stable proxy audit (status={result['proof_status']})")


if __name__ == "__main__":
    main()
