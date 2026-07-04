#!/usr/bin/env python3
"""Verify the M1 a=327 residual-slot equation repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_residual_slot_equation_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_residual_slot_equation_repair.md")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "success or failure outside this residual slot profile",
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
    require(record["source_commit"] == "fae2021", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / RESIDUAL_SLOT_INVARIANT_NONZERO / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_nearmiss_repair"]
    require(previous["commit"] == "fae2021", "wrong previous commit")
    require(previous["best_template_id"] == "nearmiss_w7_c1_v9", "wrong previous template")
    require(previous["best_mutation_id"] == "w7_c1_v9", "wrong previous mutation")
    require(previous["best_assignment_strategy"] == "signature_fiber_blocks", "wrong previous assignment")
    require(previous["best_basis_id"] == "slot_union_142_6_8_10_12_15_16", "wrong previous basis")
    require(previous["best_slot"] == 3, "wrong previous slot")
    require(previous["best_slot_nonzero_rows"] == 2, "wrong previous residual count")
    require(previous["best_forced_pair_count"] == 10, "wrong previous forced-pair count")

    equations = record["residual_slot_equations"]
    require(equations["template_id"] == "nearmiss_w7_c1_v9", "wrong target template")
    require(equations["mutation_id"] == "w7_c1_v9", "wrong target mutation")
    require(equations["assignment_strategy"] == "signature_fiber_blocks", "wrong target assignment")
    require(equations["basis_id"] == "slot_union_142_6_8_10_12_15_16", "wrong target basis")
    require(equations["basis_class_indices"] == [6, 8, 10, 12, 15, 16], "wrong basis indices")
    require(equations["basis_support_sizes"] == [74, 74, 74, 37, 37, 31], "wrong basis supports")
    require(equations["slot"] == 3, "wrong slot")
    require(equations["coefficient_matrix_shape"] == [11, 6], "wrong coefficient shape")
    require(equations["residual_row_count"] == 2, "wrong residual row count")
    require(equations["best_failure_mode"] == "RESIDUAL_SLOT_INVARIANT_NONZERO", "wrong failure mode")

    rows = equations["residual_rows"]
    require([row["class_index"] for row in rows] == [1, 5], "wrong residual classes")
    require([row["slot_coefficient"] for row in rows] == [1, 1], "wrong residual coefficients")
    require(rows[0]["functional"] == [0, 0, 0, 1, 0, 0], "wrong class 1 functional")
    require(rows[1]["functional"] == [0, 0, 0, 1, 4, 8], "wrong class 5 functional")

    u_audit = equations["symbolic_u_audit"]
    require(u_audit["valid_parameter_pairs"] == 272, "wrong valid u-pair count")
    require(u_audit["singular_parameter_pairs"] == 17, "wrong singular u-pair count")
    require(u_audit["coordinate_solve_failures"] == 0, "unexpected coordinate solve failure")
    require(u_audit["class1_slot_values"] == [1], "class1 slot is not invariant")
    require(u_audit["class5_slot_values"] == [1], "class5 slot is not invariant")
    require(u_audit["zero_slot_solution_count"] == 0, "unexpected zero-slot solution")

    stable = record["exhaustive_stable_profile_audit"]
    require(stable["stable_basis_combinations"] == 326, "wrong stable combo count")
    require(stable["stable_basis_profiles_constructed"] == 122, "wrong stable profile count")
    require(stable["slot_profiles_tested"] == 732, "wrong slot profile count")
    require(stable["actual_zero_slot_profiles"] == 0, "unexpected zero-slot profile")
    require(stable["pair_projection_clear_actual_slots"] == 0, "unexpected pair-clear slot")
    require(stable["best_basis_id"] == "slot_union_142_6_8_10_12_15_16", "wrong best stable basis")
    require(stable["best_slot"] == 3, "wrong best stable slot")
    require(stable["best_slot_nonzero_rows"] == 2, "wrong best residual count")
    require(stable["best_forced_pair_count"] == 10, "wrong best forced-pair count")
    require(record["candidate"]["constructed"] is False, "unexpected exact candidate")

    for phrase in [
        "slot coefficient values = [1]",
        "actual zero-slot profiles = 0",
        "best slot nonzero rows = 2",
        "best forced pair count = 10",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "residual_row_count": equations["residual_row_count"],
        "actual_zero_slot_profiles": stable["actual_zero_slot_profiles"],
        "best_failure_mode": equations["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 residual-slot equation repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
