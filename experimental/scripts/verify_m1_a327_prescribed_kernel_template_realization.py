#!/usr/bin/env python3
"""Verify the M1 a=327 prescribed-kernel template-realization ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_prescribed_kernel_template_realization.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_prescribed_kernel_template_realization.md")

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
    require(record["source_commit"] == "42e00f2", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")

    proxy = record["prescribed_kernel_proxy"]
    require(proxy["commit"] == "42e00f2", "wrong proxy commit")
    require(proxy["best_template_id"] == "random_matroid_v3_seed_010_m6", "wrong proxy template")
    require(proxy["best_assignment_strategy"] == "signature_fiber_blocks", "wrong proxy strategy")
    require(proxy["proxy_rank"] == 687, "wrong proxy rank")
    require(proxy["proxy_nullity"] == 166, "wrong proxy nullity")
    require(proxy["realization_status"] == "SYNTHETIC_FUNCTIONAL_PROXY_TARGET", "wrong proxy realization status")

    target = record["realization_target"]
    require(target["template_id"] == "random_matroid_v3_seed_010_m6", "wrong target template")
    require(target["assignment_strategy"] == "signature_fiber_blocks", "wrong target strategy")
    require(target["source_basis_id"] == "max_support_basis", "wrong target basis")
    require(target["prescribed_kernel_id"] == "slot_6_kernel", "wrong kernel id")
    require(target["prescribed_kernel_vector"] == [0, 0, 0, 0, 0, 1], "wrong kernel vector")
    require(target["coefficient_rank"] == 5, "wrong coefficient rank")
    require(target["right_kernel_nullity"] == 1, "wrong right-kernel nullity")
    require(target["coordinate_rows_changed"] == 33, "wrong changed-row count")
    require(target["prescribed_coordinate_rank_histogram"] == {"2": 87, "3": 97, "4": 328}, "wrong prescribed rank histogram")

    realization = record["template_realization"]
    require(realization["linear_matrix_shape"] == [4193, 42], "wrong linear shape")
    require(realization["linear_rank"] == 35, "wrong linear rank")
    require(realization["linear_nullity"] == 7, "wrong linear nullity")
    require(realization["diagonal_rank"] == 6, "wrong diagonal rank")
    require(realization["diagonal_in_kernel"] is True, "diagonal not in kernel")
    require(realization["non_diagonal_kernel_dimension"] == 1, "wrong non-diagonal dimension")
    require(realization["non_diagonal_quotient_exhausted"] is True, "quotient not exhausted")
    require(realization["samples_tested"] == 263, "wrong sample count")
    require(realization["rowspace_valid_samples"] == 0, "unexpected rowspace-valid sample")
    require(realization["seven_distinct_samples"] == 0, "unexpected seven-distinct valid sample")
    require(realization["best_realized_total_effective_cost"] == 1687, "wrong realized cost")
    require(realization["best_realized_functional_classes"] == 33, "wrong realized class count")
    require(realization["best_realized_functional_span_rank"] == 5, "wrong realized span")
    require(realization["best_failure_mode"] == "TEMPLATE_REALIZATION_ROWSPACE_FAIL", "wrong failure mode")

    best = record["best_sample"]
    require(best["rowspace_ok"] is False, "best sample unexpectedly rowspace-valid")
    require(best["seven_template_vectors_distinct"] is True, "best sample not template-distinct")
    require(best["realized_total_effective_cost"] == 1687, "best realized cost mismatch")
    require(best["realized_rank_histogram"] == {"2": 87, "3": 187, "4": 238}, "wrong realized rank histogram")
    require(best["realized_functional_classes"] == 33, "best class count mismatch")
    require(best["realized_forced_functional_identities"] == 0, "unexpected forced identity")
    require(best["realized_functional_span_rank"] == 5, "best span mismatch")
    require(best["realized_annihilator_dimension"] == 1, "best annihilator mismatch")
    require(len(best["rowspace_failures"]) == 90, "wrong rowspace failure count")

    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")
    for phrase in [
        "linear matrix = 4193 x 42",
        "non-diagonal kernel dimension = 1",
        "rowspace-valid samples = 0",
        "best realized functional span rank = 5",
        "rowspace failures in representative = 90",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "linear_nullity": realization["linear_nullity"],
        "non_diagonal_kernel_dimension": realization["non_diagonal_kernel_dimension"],
        "rowspace_valid_samples": realization["rowspace_valid_samples"],
        "best_realized_functional_span_rank": realization["best_realized_functional_span_rank"],
        "best_failure_mode": realization["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 prescribed-kernel template realization (status={result['proof_status']})")


if __name__ == "__main__":
    main()
