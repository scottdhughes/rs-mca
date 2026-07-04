#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear diverse five-row module audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_diverse_five_row_module_audit.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_diverse_five_row_module_audit.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_diverse_five_row_module_audit.py")
M2_SCRIPT_PATH = Path("experimental/scripts/m2_m1_a327_pairclear_diverse_five_row_module_audit.m2")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the audited five-row module front",
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
    scan_text = SCAN_PATH.read_text()
    m2_text = M2_SCRIPT_PATH.read_text()

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "e7dada7", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "AUDIT / DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_diverse_chamber_front"]
    require(previous["commit"] == "e7dada7", "wrong previous commit")
    require(previous["proof_status"] == "CANDIDATE / DCHAMBER_DIRECT_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["sampled_profiles"] == 48, "wrong previous sampled profiles")
    require(previous["full_profiles_scanned"] == 4, "wrong previous full profiles")
    require(previous["full_direct_support_reduced_profiles"] == 4, "wrong previous support reduction")
    require(previous["best_template_id"] == "ninerow_w2_c0_d1", "wrong previous best template")
    require(previous["best_mutation_id"] == "w2_c0_d1", "wrong previous best mutation")
    require(previous["best_basis_id"] == "basisaware_0_1_2_3_4_6", "wrong previous best basis")
    require(previous["best_failure_mode"] == "DCHAMBER_DIRECT_SUPPORT_REDUCED", "wrong previous failure")

    target = record["target_system"]
    require(target["template_id"] == "ninerow_w2_c0_d1", "wrong target template")
    require(target["mutation_id"] == "w2_c0_d1", "wrong target mutation")
    require(target["profile_index"] == 41, "wrong profile index")
    require(target["assignment_strategy"] == "fiber_round_robin", "wrong assignment")
    require(target["assignment_seed"] == 109978, "wrong assignment seed")
    require(target["basis_id"] == "basisaware_0_1_2_3_4_6", "wrong basis")
    require(target["basis_class_indices"] == [0, 1, 2, 3, 4, 6], "wrong basis classes")
    require(target["basis_support_sizes"] == [216, 216, 179, 148, 142, 111], "wrong support sizes")
    require(target["direction"] == [1, 16, 0, 14, 14, 11], "wrong direction")
    require(target["direction_projective"] == [1, 16, 0, 14, 14, 11], "wrong projective direction")
    require(target["forced_pairs"] == [], "unexpected forced pairs")
    require(all(int(value) % 17 for value in target["pair_projection_scalars"].values()), "zero pair scalar")
    require(target["row_classes"] == [5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18], "wrong row classes")
    require(target["row_values"] == [1, 0, 0, 15, 0, 13, 0, 4, 16, 0, 0, 0, 0], "wrong row values")
    require(target["active_row_indices"] == [0, 3, 5, 7, 8], "wrong active indices")
    require(target["active_row_classes"] == [5, 9, 11, 13, 14], "wrong active classes")
    require(target["inactive_row_indices"] == [1, 2, 4, 6, 9, 10, 11, 12], "wrong inactive indices")
    require(target["inactive_row_classes"] == [7, 8, 10, 12, 15, 16, 17, 18], "wrong inactive classes")

    module = record["module_audit"]
    require(module["field"] == "GF(17)", "wrong module field")
    full = module["full_matrix"]
    require(full["shape"] == [13, 6], "wrong full shape")
    require(full["rank"] == 6, "wrong full rank")
    require(full["right_kernel_nullity"] == 0, "wrong full nullity")
    require(full["left_syzygy_dimension"] == 7, "wrong full syzygy")
    active = module["active_matrix"]
    require(active["shape"] == [5, 6], "wrong active shape")
    require(active["rank"] == 5, "wrong active rank")
    require(active["right_kernel_nullity"] == 1, "wrong active nullity")
    inactive = module["inactive_matrix"]
    require(inactive["shape"] == [8, 6], "wrong inactive shape")
    require(inactive["rank"] == 5, "wrong inactive rank")
    require(inactive["right_kernel_nullity"] == 1, "wrong inactive nullity")
    require(inactive["left_syzygy_dimension"] == 3, "wrong inactive syzygy")
    require(inactive["right_kernel_basis"] == [[14, 3, 0, 9, 9, 1]], "wrong inactive kernel")
    require(module["inactive_kernel_projective_basis"] == [[1, 16, 0, 14, 14, 11]], "wrong projective inactive kernel")
    require(module["direction_spans_inactive_kernel"] is True, "direction not in inactive kernel")
    require(module["singleton_extensions_tested"] == 5, "wrong singleton count")
    require(module["singleton_full_rank_count"] == 5, "wrong singleton full-rank count")
    for row in module["singleton_extensions"]:
        require(row["full_rank"] is True, "singleton not full rank")
        require(row["rank_inactive_plus_row"] == 6, "singleton rank mismatch")
        require(row["right_kernel_nullity"] == 0, "singleton nullity mismatch")
    require(module["pair_extensions_tested"] == 10, "wrong pair extension count")
    require(module["pair_full_rank_count"] == 10, "wrong pair full-rank count")
    for row in module["pair_extensions"]:
        require(row["full_rank"] is True, "pair extension not full rank")
        require(row["rank_inactive_plus_rows"] == 6, "pair extension rank mismatch")
        require(row["right_kernel_nullity"] == 0, "pair extension nullity mismatch")
    rank_slack = module["rank_slack_chamber"]
    require(rank_slack["zero_row_classes"] == [7, 8, 10, 12, 16, 17, 18], "wrong rank-slack classes")
    require(rank_slack["matrix"]["shape"] == [7, 6], "wrong rank-slack shape")
    require(rank_slack["matrix"]["rank"] == 4, "wrong rank-slack rank")
    require(rank_slack["matrix"]["right_kernel_nullity"] == 2, "wrong rank-slack nullity")
    require(rank_slack["kernel_projective_basis"] == [[0, 0, 1, 1, 0, 0], [1, 16, 3, 0, 14, 11]], "wrong rank-slack kernel basis")
    require(module["best_failure_mode"] == "DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED", "wrong module failure")

    m2 = record["macaulay2"]["result"]
    require(m2["returncode"] == 0, "Macaulay2 failed")
    parsed = m2["parsed"]
    expected = {
        "M2_FULL_ROWS": 13,
        "M2_FULL_COLS": 6,
        "M2_FULL_RANK": 6,
        "M2_FULL_RIGHT_KERNEL_GENS": 0,
        "M2_FULL_LEFT_SYZYGY_GENS": 7,
        "M2_FULL_LEFT_SYZYGY_RANK": 7,
        "M2_ACTIVE_ROWS": 5,
        "M2_ACTIVE_COLS": 6,
        "M2_ACTIVE_RANK": 5,
        "M2_ACTIVE_RIGHT_KERNEL_GENS": 1,
        "M2_ACTIVE_LEFT_SYZYGY_GENS": 0,
        "M2_ACTIVE_LEFT_SYZYGY_RANK": 0,
        "M2_INACTIVE_ROWS": 8,
        "M2_INACTIVE_COLS": 6,
        "M2_INACTIVE_RANK": 5,
        "M2_INACTIVE_RIGHT_KERNEL_GENS": 1,
        "M2_INACTIVE_LEFT_SYZYGY_GENS": 3,
        "M2_INACTIVE_LEFT_SYZYGY_RANK": 3,
        "M2_RANKSLACK_ROWS": 7,
        "M2_RANKSLACK_COLS": 6,
        "M2_RANKSLACK_RANK": 4,
        "M2_RANKSLACK_RIGHT_KERNEL_GENS": 2,
        "M2_RANKSLACK_LEFT_SYZYGY_GENS": 3,
        "M2_RANKSLACK_LEFT_SYZYGY_RANK": 3,
    }
    for key, value in expected.items():
        require(parsed[key] == value, f"M2 mismatch for {key}")
    for idx in range(5):
        require(parsed[f"M2_EXT{idx}_RANK"] == 6, f"M2 extension {idx} not full rank")
    for phrase in ["FULL = matrix", "INACTIVE = matrix", "RANKSLACK = matrix", "M2_RANKSLACK_RIGHT_KERNEL_GENS"]:
        require(phrase in m2_text, f"M2 script missing phrase: {phrase}")

    for phrase in [
        "AUDIT / DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED",
        "full matrix shape = [13,6]",
        "inactive matrix shape = [8,6]",
        "inactive kernel projective basis = [[1,16,0,14,14,11]]",
        "singleton extensions tested = 5",
        "pair full-rank count = 10",
        "rank-slack right-kernel nullity = 2",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "TARGET_MUTATION_ID = \"w2_c0_d1\"",
        "TARGET_DIRECTION = [1, 16, 0, 14, 14, 11]",
        "rank_slack_chamber",
        "global obstruction outside the audited five-row module front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "full_rank": full["rank"],
        "inactive_rank": inactive["rank"],
        "inactive_right_kernel_nullity": inactive["right_kernel_nullity"],
        "active_row_count": active["shape"][0],
        "singleton_full_rank_count": module["singleton_full_rank_count"],
        "rank_slack_nullity": rank_slack["matrix"]["right_kernel_nullity"],
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
        print(f"PASS: M1 a=327 pair-clear diverse five-row module audit (status={result['proof_status']})")


if __name__ == "__main__":
    main()
