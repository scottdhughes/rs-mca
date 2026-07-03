#!/usr/bin/env python3
"""Verify the M1 a=327 prescribed right-kernel selected-class proxy ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_prescribed_right_kernel_selected_class_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_prescribed_right_kernel_selected_class_search.md")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_prescribed_right_kernel_selected_class_search.m2")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "realized exact template vectors for the prescribed coefficients",
}
ALLOWED_LABELS = {
    "PRESCRIBED_KERNEL_SUPPORT_FAIL",
    "PRESCRIBED_KERNEL_PAIR_GUARD_FAIL",
    "PRESCRIBED_KERNEL_FORCED_IDENTITY",
    "PRESCRIBED_KERNEL_LOW_FUNCTIONAL_SPAN",
    "PRESCRIBED_KERNEL_DIAGONAL_ANNIHILATOR",
    "PRESCRIBED_KERNEL_STRUCTURAL_PASS",
    "PRESCRIBED_KERNEL_COEFFICIENT_FAIL",
    "PRESCRIBED_KERNEL_PROXY_PENDING",
    "PRESCRIBED_KERNEL_PROXY_FULL_RANK",
    "PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE",
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
    require(record["source_commit"] == "6d58c96", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    previous = record["previous_right_kernel_search"]
    require(previous["systems_tested"] == 108, "wrong previous system count")
    require(previous["coefficient_profiles_tested"] == 3276, "wrong previous profile count")
    require(previous["right_kernel_positive_candidates"] == 0, "unexpected previous positive")
    require(previous["best_failure_mode"] == "RIGHT_KERNEL_COEFFICIENT_FULL_RANK", "wrong previous failure")

    search = record["prescribed_kernel_search"]
    require(search["templates_tested"] == 18, "wrong template count")
    require(search["systems_tested"] == 108, "wrong system count")
    require(search["structural_pass_candidates"] == 96, "wrong structural-pass count")
    require(search["engineered_profiles_tested"] == 6912, "wrong engineered profile count")
    require(search["right_kernel_positive_candidates"] == 96, "wrong right-kernel positive count")
    require(search["proxy_candidates_tested"] == 12, "wrong proxy candidate count")
    require(search["proxy_basis_profiles_tested"] == 12, "wrong proxy profile count")
    require(search["proxy_positive_candidates"] == 12, "wrong proxy-positive count")
    require(search["best_template_id"] == "random_matroid_v3_seed_010_m6", "wrong best template")
    require(search["best_assignment_strategy"] == "signature_fiber_blocks", "wrong best strategy")
    require(search["best_proxy_rank"] == 687, "wrong best proxy rank")
    require(search["best_proxy_nullity"] == 166, "wrong best proxy nullity")
    require(search["best_failure_mode"] == "PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE", "wrong best failure")
    require(search["failure_counts"] == {
        "PRESCRIBED_KERNEL_LOW_FUNCTIONAL_SPAN": 12,
        "PRESCRIBED_KERNEL_PROXY_NULLITY_POSITIVE": 12,
        "PRESCRIBED_KERNEL_PROXY_PENDING": 84,
    }, "failure counts mismatch")
    require(search["screen_counts"] == {
        "PRESCRIBED_KERNEL_LOW_FUNCTIONAL_SPAN": 12,
        "PRESCRIBED_KERNEL_STRUCTURAL_PASS": 96,
    }, "screen counts mismatch")
    require(set(search["failure_counts"]).issubset(ALLOWED_LABELS), "bad failure label")
    require(set(search["screen_counts"]).issubset(ALLOWED_LABELS), "bad screen label")

    best = record["best_candidate"]
    require(best["template_id"] == "random_matroid_v3_seed_010_m6", "best template mismatch")
    require(best["assignment_strategy"] == "signature_fiber_blocks", "best strategy mismatch")
    require(best["support_vector"] == [327, 327, 327, 327, 327, 327, 327], "best support mismatch")
    require(best["pair7_counts"] == [233, 233, 233, 233, 233], "best pair7 mismatch")
    require(best["max_pair_count"] == 233, "best max pair mismatch")
    require(best["functional_classes"] == 45, "best functional class mismatch")
    require(best["functional_span_rank"] == 6, "best span mismatch")
    require(best["annihilator_dimension"] == 0, "best annihilator mismatch")
    require(best["forced_functional_identities"] == 0, "best forced identity mismatch")
    require(best["engineered_profiles_tested"] == 72, "best engineered profile count mismatch")
    proxy = best["best_proxy"]
    require(proxy["basis_id"] == "max_support_basis__slot_6_kernel", "wrong best basis")
    require(proxy["source_basis_id"] == "max_support_basis", "wrong source basis")
    require(proxy["prescribed_kernel_id"] == "slot_6_kernel", "wrong kernel")
    require(proxy["prescribed_kernel_vector"] == [0, 0, 0, 0, 0, 1], "wrong kernel vector")
    require(proxy["basis_class_indices"] == [0, 1, 2, 3, 4, 5], "wrong basis classes")
    require(proxy["basis_support_sizes"] == [230, 91, 91, 91, 90, 90], "wrong basis support sizes")
    require(proxy["coefficient_rank"] == 5, "wrong coefficient rank")
    require(proxy["right_kernel_nullity"] == 1, "wrong right-kernel nullity")
    require(proxy["matrix_shape"] == [1094, 853], "wrong proxy matrix shape")
    require(proxy["proxy_rank"] == 687, "wrong proxy rank")
    require(proxy["proxy_nullity"] == 166, "wrong proxy nullity")

    m2 = record["m2_right_kernel_check"]
    require(m2 is not None, "M2 check missing")
    require(m2["returncode"] == 0, "M2 did not pass")
    parsed = m2["parsed"]
    require(parsed["M2_COEFF_ROWS"] == 39, "M2 row mismatch")
    require(parsed["M2_COEFF_COLS"] == 6, "M2 column mismatch")
    require(parsed["M2_COEFF_RANK"] == 5, "M2 rank mismatch")
    require(parsed["M2_RIGHT_KERNEL_GENS"] == 1, "M2 right-kernel mismatch")
    require(parsed["M2_LEFT_SYZYGY_GENS"] == 34, "M2 left syzygy gens mismatch")
    require(parsed["M2_LEFT_SYZYGY_RANK"] == 34, "M2 left syzygy rank mismatch")
    require("Coeff = matrix" in m2_text, "M2 script missing matrix")
    require("M2_RIGHT_KERNEL_GENS" in m2_text, "M2 script missing right kernel line")

    require(record["realization_status"] == "SYNTHETIC_FUNCTIONAL_PROXY_TARGET", "wrong realization status")
    require(record["exact_audit"]["run"] is False, "unexpected exact audit")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "systems tested = 108",
        "engineered profiles tested = 6912",
        "proxy-positive candidates = 12",
        "coefficient rank/right-kernel nullity = 5 / 1",
        "proxy quotient rank/nullity = 687 / 166",
        "Sage exact-lift target",
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
        "realization_status": record["realization_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 prescribed right-kernel selected-class search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
