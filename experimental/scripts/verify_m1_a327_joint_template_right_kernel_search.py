#!/usr/bin/env python3
"""Verify the M1 a=327 joint template/right-kernel search ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_joint_template_right_kernel_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_joint_template_right_kernel_search.md")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_joint_template_right_kernel_search.m2")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
ALLOWED_LABELS = {
    "JOINT_TEMPLATE_SUPPORT_FAIL",
    "JOINT_TEMPLATE_PAIR_GUARD_FAIL",
    "JOINT_TEMPLATE_FORCED_IDENTITY",
    "JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN",
    "JOINT_TEMPLATE_DIAGONAL_ANNIHILATOR",
    "JOINT_TEMPLATE_STRUCTURAL_PASS",
    "JOINT_TEMPLATE_COEFFICIENT_FULL_RANK",
    "JOINT_TEMPLATE_PROXY_PENDING",
    "JOINT_TEMPLATE_PROXY_FULL_RANK",
    "JOINT_TEMPLATE_PROXY_NULLITY_POSITIVE",
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
    m2_text = M2_SCRIPT_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "f63a23f", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_template_realization"]
    require(previous["linear_nullity"] == 7, "wrong previous nullity")
    require(previous["non_diagonal_kernel_dimension"] == 1, "wrong previous quotient dimension")
    require(previous["rowspace_valid_samples"] == 0, "unexpected previous valid sample")
    require(previous["best_failure_mode"] == "TEMPLATE_REALIZATION_ROWSPACE_FAIL", "wrong previous failure")

    search = record["joint_template_search"]
    require(search["templates_tested"] == 36, "wrong template count")
    require(search["systems_tested"] == 216, "wrong system count")
    require(search["structural_pass_candidates"] == 210, "wrong structural-pass count")
    require(search["right_kernel_positive_candidates"] == 6, "wrong right-kernel positive count")
    require(search["proxy_candidates_tested"] == 6, "wrong proxy candidate count")
    require(search["proxy_basis_profiles_tested"] == 42, "wrong proxy basis count")
    require(search["proxy_positive_candidates"] == 0, "unexpected proxy-positive")
    require(search["best_template_id"] == "single_outside_w7_v1", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(search["best_proxy_rank"] == 277, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 0, "wrong best proxy nullity")
    require(search["best_failure_mode"] == "JOINT_TEMPLATE_PROXY_FULL_RANK", "wrong best failure")
    require(search["failure_counts"] == {
        "JOINT_TEMPLATE_COEFFICIENT_FULL_RANK": 204,
        "JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN": 6,
        "JOINT_TEMPLATE_PROXY_FULL_RANK": 6,
    }, "failure counts mismatch")
    require(search["screen_counts"] == {
        "JOINT_TEMPLATE_LOW_FUNCTIONAL_SPAN": 6,
        "JOINT_TEMPLATE_STRUCTURAL_PASS": 210,
    }, "screen counts mismatch")
    require(set(search["failure_counts"]).issubset(ALLOWED_LABELS), "bad failure label")
    require(set(search["screen_counts"]).issubset(ALLOWED_LABELS), "bad screen label")

    best = record["best_candidate"]
    require(best["template_id"] == "single_outside_w7_v1", "best template mismatch")
    require(best["template_family"] == "single_outside_rank5_hyperplane", "best family mismatch")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "best strategy mismatch")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "best support mismatch")
    require(best["pair7_counts"] == [253, 253, 253, 253, 253], "best pair7 mismatch")
    require(best["max_pair_count"] == 253, "best max pair mismatch")
    require(best["selected_class_size_counts"] == {"3": 185, "4": 6, "5": 216, "6": 105}, "best size counts mismatch")
    require(best["functional_classes"] == 14, "best functional class mismatch")
    require(best["functional_span_rank"] == 6, "best span mismatch")
    require(best["annihilator_dimension"] == 0, "best annihilator mismatch")
    require(best["forced_functional_identities"] == 0, "best forced identities mismatch")
    require(best["basis_profiles_tested"] == 30, "best basis profile count mismatch")
    profile = best["right_kernel_profiles"][0]
    require(profile["basis_id"] == "max_support_basis", "wrong right-kernel basis")
    require(profile["basis_class_indices"] == [0, 1, 2, 3, 4, 5], "wrong basis classes")
    require(profile["basis_support_sizes"] == [253, 216, 216, 216, 179, 179], "wrong basis supports")
    require(profile["coefficient_rank"] == 5, "wrong coefficient rank")
    require(profile["right_kernel_nullity"] == 1, "wrong right-kernel nullity")
    require(profile["matrix_shape"] == [518, 277], "wrong coefficient/proxy shape")
    proxy = best["best_proxy"]
    require(proxy["basis_id"] == "max_support_basis", "wrong proxy basis")
    require(proxy["coefficient_rank"] == 5, "wrong proxy coefficient rank")
    require(proxy["right_kernel_nullity"] == 1, "wrong proxy right-kernel nullity")
    require(proxy["matrix_shape"] == [518, 277], "wrong proxy matrix shape")
    require(proxy["proxy_rank"] == 277, "wrong proxy rank")
    require(proxy["proxy_nullity"] == 0, "wrong proxy nullity")

    m2 = record["m2_right_kernel_check"]
    require(m2 is not None, "missing M2 check")
    require(m2["returncode"] == 0, "M2 did not pass")
    parsed = m2["parsed"]
    require(parsed["M2_COEFF_ROWS"] == 8, "M2 row mismatch")
    require(parsed["M2_COEFF_COLS"] == 6, "M2 column mismatch")
    require(parsed["M2_COEFF_RANK"] == 5, "M2 rank mismatch")
    require(parsed["M2_RIGHT_KERNEL_GENS"] == 1, "M2 right-kernel mismatch")
    require(parsed["M2_LEFT_SYZYGY_GENS"] == 3, "M2 left syzygy gens mismatch")
    require(parsed["M2_LEFT_SYZYGY_RANK"] == 3, "M2 left syzygy rank mismatch")
    require("Coeff = matrix" in m2_text, "M2 script missing matrix")
    require("M2_RIGHT_KERNEL_GENS" in m2_text, "M2 script missing right-kernel line")

    require(record["exact_audit"]["run"] is False, "unexpected exact audit")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 216",
        "right-kernel-positive candidates = 6",
        "proxy-positive candidates = 0",
        "coefficient rank/right-kernel nullity = 5 / 1",
        "proxy quotient rank/nullity = 277 / 0",
        "coefficient matrix = 8 x 6",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "systems_tested": search["systems_tested"],
        "right_kernel_positive_candidates": search["right_kernel_positive_candidates"],
        "proxy_positive_candidates": search["proxy_positive_candidates"],
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
        print(f"PASS: M1 a=327 joint template/right-kernel search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
