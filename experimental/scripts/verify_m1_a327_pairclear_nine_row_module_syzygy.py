#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear nine-row module/syzygy ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_nine_row_module_syzygy.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_nine_row_module_syzygy.md")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_pairclear_nine_row_module_syzygy.m2")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the pinned nine-row module front",
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
    require(record["source_commit"] == "66742fe", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "AUDIT / NINEROW_MODULE_SYZYGY_STABLE / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_nine_row_repair"]
    require(previous["commit"] == "66742fe", "wrong previous commit")
    require(previous["proof_status"] == "CANDIDATE / NINEROW_FIXED_DIRECTION_STABLE / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["best_mutation_id"] == "base_w1_c3_d1", "wrong previous mutation")
    require(previous["best_fixed_direction_nonzero_rows"] == 9, "wrong previous row count")
    require(previous["best_fixed_direction_forced_pair_count"] == 0, "wrong previous forced-pair count")
    require(previous["row_reduced_directions"] == 0, "unexpected previous row reduction")
    require(previous["pair_clear_direction_kernels"] == 0, "unexpected previous kernel")
    require(previous["best_failure_mode"] == "NINEROW_FIXED_DIRECTION_STABLE", "wrong previous failure")

    target = record["target_system"]
    require(target["template_id"] == "ninerow_base_w1_c3_d1", "wrong target template")
    require(target["assignment_strategy"] == "fiber_round_robin", "wrong target assignment")
    require(target["basis_id"] == "basisaware_1_4_7_8_9_10", "wrong target basis")
    require(target["basis_class_indices"] == [1, 4, 7, 8, 9, 10], "wrong basis classes")
    require(target["basis_support_sizes"] == [179, 142, 105, 105, 74, 74], "wrong support sizes")
    require(target["pinned_direction"] == [0, 5, 0, 0, 0, 1], "wrong pinned direction")
    require(target["pinned_direction_projective"] == [0, 1, 0, 0, 0, 7], "wrong projective direction")
    require(target["forced_pairs"] == [], "unexpected forced pairs")
    require(all(int(value) % 17 for value in target["pair_projection_scalars"].values()), "zero pair scalar")
    require(target["full_row_classes"] == [0, 2, 3, 5, 6, 11, 12, 13, 14, 15, 16, 17, 18, 19], "wrong full classes")
    require(target["active_row_indices"] == [0, 1, 2, 3, 4, 5, 6, 8, 9], "wrong active indices")
    require(target["active_row_classes"] == [0, 2, 3, 5, 6, 11, 12, 14, 15], "wrong active classes")
    require(target["inactive_row_indices"] == [7, 10, 11, 12, 13], "wrong inactive indices")
    require(target["inactive_row_classes"] == [13, 16, 17, 18, 19], "wrong inactive classes")
    require(target["row_values"] == [8, 10, 14, 8, 3, 9, 2, 0, 15, 9, 0, 0, 0, 0], "wrong row values")

    module = record["module_syzygy"]
    require(module["field"] == "GF(17)", "wrong module field")
    full = module["full_matrix"]
    require(full["shape"] == [14, 6], "wrong full shape")
    require(full["rank"] == 6, "wrong full rank")
    require(full["right_kernel_nullity"] == 0, "wrong full right nullity")
    require(full["left_syzygy_dimension"] == 8, "wrong full left syzygy")
    active = module["active_matrix"]
    require(active["shape"] == [9, 6], "wrong active shape")
    require(active["rank"] == 6, "wrong active rank")
    require(active["right_kernel_nullity"] == 0, "wrong active right nullity")
    require(active["left_syzygy_dimension"] == 3, "wrong active left syzygy")
    inactive = module["inactive_matrix"]
    require(inactive["shape"] == [5, 6], "wrong inactive shape")
    require(inactive["rank"] == 5, "wrong inactive rank")
    require(inactive["right_kernel_nullity"] == 1, "wrong inactive right nullity")
    require(inactive["left_syzygy_dimension"] == 0, "wrong inactive left syzygy")
    require(inactive["right_kernel_basis"] == [[0, 5, 0, 0, 0, 1]], "wrong inactive kernel basis")
    require(module["inactive_kernel_projective_basis"] == [[0, 1, 0, 0, 0, 7]], "wrong inactive projective basis")
    require(module["pinned_direction_spans_inactive_kernel"] is True, "pinned direction does not span inactive kernel")
    require(module["singleton_extensions_tested"] == 9, "wrong singleton count")
    require(module["singleton_full_rank_count"] == 9, "not all singleton extensions full rank")
    for row in module["singleton_extensions"]:
        require(row["full_rank"] is True, "singleton not full rank")
        require(row["rank_inactive_plus_row"] == 6, "singleton rank mismatch")
        require(row["right_kernel_nullity"] == 0, "singleton right nullity mismatch")
    require(module["best_failure_mode"] == "NINEROW_MODULE_SINGLETON_EXTENSIONS_FULL_RANK", "wrong module failure")

    m2 = record["macaulay2"]["result"]
    require(m2["returncode"] == 0, "Macaulay2 did not pass")
    parsed = m2["parsed"]
    expected = {
        "M2_FULL_ROWS": 14,
        "M2_FULL_COLS": 6,
        "M2_FULL_RANK": 6,
        "M2_FULL_RIGHT_KERNEL_GENS": 0,
        "M2_FULL_LEFT_SYZYGY_GENS": 8,
        "M2_FULL_LEFT_SYZYGY_RANK": 8,
        "M2_ACTIVE_ROWS": 9,
        "M2_ACTIVE_COLS": 6,
        "M2_ACTIVE_RANK": 6,
        "M2_ACTIVE_RIGHT_KERNEL_GENS": 0,
        "M2_ACTIVE_LEFT_SYZYGY_GENS": 3,
        "M2_ACTIVE_LEFT_SYZYGY_RANK": 3,
        "M2_INACTIVE_ROWS": 5,
        "M2_INACTIVE_COLS": 6,
        "M2_INACTIVE_RANK": 5,
        "M2_INACTIVE_RIGHT_KERNEL_GENS": 1,
        "M2_INACTIVE_LEFT_SYZYGY_GENS": 0,
        "M2_INACTIVE_LEFT_SYZYGY_RANK": 0,
    }
    for key, value in expected.items():
        require(parsed[key] == value, f"M2 mismatch for {key}")
    for idx in range(9):
        require(parsed[f"M2_EXT{idx}_RANK"] == 6, f"M2 extension {idx} not full rank")
    require("FULL = matrix" in m2_text, "M2 script missing full matrix")
    require("INACTIVE = matrix" in m2_text, "M2 script missing inactive matrix")
    require("M2_INACTIVE_RIGHT_KERNEL_GENS" in m2_text, "M2 script missing inactive kernel print")

    for phrase in [
        "AUDIT / NINEROW_MODULE_SYZYGY_STABLE",
        "inactive right-kernel basis = [[0,5,0,0,0,1]]",
        "singleton extensions tested = 9",
        "singleton full-rank count = 9",
        "Macaulay2",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "inactive_rank": inactive["rank"],
        "inactive_right_kernel_nullity": inactive["right_kernel_nullity"],
        "singleton_full_rank_count": module["singleton_full_rank_count"],
        "best_failure_mode": module["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 pair-clear nine-row module syzygy (status={result['proof_status']})")


if __name__ == "__main__":
    main()
