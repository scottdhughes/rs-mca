#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear diverse rank-slack kernel repair ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_diverse_rankslack_kernel_repair.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_diverse_rankslack_kernel_repair.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_diverse_rankslack_kernel_repair.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the audited rank-slack kernel front",
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

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "3228415", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / RANKSLACK_KERNEL_EIGHT_ROW_STABLE / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_five_row_module_audit"]
    require(previous["commit"] == "3228415", "wrong previous commit")
    require(previous["proof_status"] == "AUDIT / DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["target_template_id"] == "ninerow_w2_c0_d1", "wrong previous template")
    require(previous["target_mutation_id"] == "w2_c0_d1", "wrong previous mutation")
    require(previous["target_basis_id"] == "basisaware_0_1_2_3_4_6", "wrong previous basis")
    require(previous["active_row_count"] == 5, "wrong previous active count")
    require(previous["inactive_row_count"] == 8, "wrong previous inactive count")
    require(previous["rank_slack_rank"] == 4, "wrong previous rank-slack rank")
    require(previous["rank_slack_nullity"] == 2, "wrong previous rank-slack nullity")
    require(previous["best_failure_mode"] == "DIVERSE_FIVEROW_MODULE_SUPPORT_REDUCED", "wrong previous failure")

    kernel = record["rank_slack_kernel"]
    require(kernel["field"] == "GF(17)", "wrong field")
    require(kernel["basis"] == [[0, 0, 1, 1, 0, 0], [14, 3, 8, 0, 9, 1]], "wrong kernel basis")
    require(kernel["projective_basis"] == [[0, 0, 1, 1, 0, 0], [1, 16, 3, 0, 14, 11]], "wrong projective basis")
    require(kernel["base_zero_row_classes"] == [7, 8, 10, 12, 16, 17, 18], "wrong base zero classes")
    require(kernel["directions_tested"] == 18, "wrong direction count")
    require(kernel["pair_clear_directions"] == 10, "wrong pair-clear count")
    require(kernel["support_reduced_directions"] == 1, "wrong support-reduced count")
    require(kernel["nine_or_better_directions"] == 0, "unexpected nine-or-better direction")
    require(kernel["coefficient_kernel_directions"] == 0, "unexpected coefficient kernel")
    require(kernel["best_failure_mode"] == "RANKSLACK_KERNEL_EIGHT_ROW_STABLE", "wrong failure")
    require(len(kernel["all_direction_summaries"]) == 18, "wrong direction summary count")

    best = kernel["best_direction"]
    require(best["kernel_coefficients"] == [1, 2], "wrong best coefficients")
    require(best["direction"] == [11, 6, 0, 1, 1, 2], "wrong best direction")
    require(best["direction_projective"] == [1, 16, 0, 14, 14, 11], "wrong projective best direction")
    require(best["forced_pair_count"] == 0, "best direction has forced pairs")
    require(best["forced_pairs"] == [], "best forced pair list not empty")
    require(all(int(value) % 17 for value in best["pair_projection_scalars"].values()), "zero best pair scalar")
    require(best["zero_row_count"] == 8, "wrong best zero count")
    require(best["zero_row_classes"] == [7, 8, 10, 12, 15, 16, 17, 18], "wrong best zero classes")
    require(best["active_row_count"] == 5, "wrong best active count")
    require(best["active_row_classes"] == [5, 9, 11, 13, 14], "wrong best active classes")

    first = kernel["all_direction_summaries"][0]
    require(first["direction"] == [0, 0, 1, 1, 0, 0], "wrong first basis direction")
    require(first["zero_row_count"] == 10, "wrong first zero count")
    require(first["forced_pair_count"] == 11, "wrong first forced-pair count")

    for phrase in [
        "CANDIDATE / RANKSLACK_KERNEL_EIGHT_ROW_STABLE",
        "directions tested = 18",
        "pair-clear directions = 10",
        "support-reduced directions = 1",
        "nine-or-better directions = 0",
        "coefficient-kernel directions = 0",
        "has 10 zero rows but 11 forced pairs",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "projective_kernel_combinations",
        "RANKSLACK_KERNEL_NINE_ROW_REPAIR",
        "RANKSLACK_KERNEL_EIGHT_ROW_STABLE",
        "global obstruction outside the audited rank-slack kernel front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "directions_tested": kernel["directions_tested"],
        "pair_clear_directions": kernel["pair_clear_directions"],
        "support_reduced_directions": kernel["support_reduced_directions"],
        "nine_or_better_directions": kernel["nine_or_better_directions"],
        "best_zero_row_count": best["zero_row_count"],
        "best_active_row_count": best["active_row_count"],
        "best_failure_mode": kernel["best_failure_mode"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 pair-clear diverse rank-slack kernel repair (status={result['proof_status']})")


if __name__ == "__main__":
    main()
