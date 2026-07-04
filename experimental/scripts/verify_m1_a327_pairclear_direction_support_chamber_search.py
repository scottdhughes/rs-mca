#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear direction support chamber ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_direction_support_chamber_search.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_direction_support_chamber_search.md")
SCAN_PATH = Path("experimental/scripts/scan_m1_a327_pairclear_direction_support_chamber_search.py")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the base direction-support chamber front",
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
    require(record["source_commit"] == "a9acb86", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(
        record["proof_status"] == "CANDIDATE / CHAMBER_NINE_ROW_STABLE / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    previous = record["previous_module_syzygy"]
    require(previous["commit"] == "a9acb86", "wrong previous commit")
    require(previous["proof_status"] == "AUDIT / NINEROW_MODULE_SYZYGY_STABLE / PARTIAL / EXPERIMENTAL", "wrong previous status")
    require(previous["inactive_rank"] == 5, "wrong previous inactive rank")
    require(previous["inactive_right_kernel_nullity"] == 1, "wrong previous inactive nullity")
    require(previous["singleton_extensions_tested"] == 9, "wrong singleton extension count")
    require(previous["singleton_full_rank_count"] == 9, "wrong singleton full-rank count")
    require(previous["best_failure_mode"] == "NINEROW_MODULE_SINGLETON_EXTENSIONS_FULL_RANK", "wrong previous failure")

    target = record["target_system"]
    require(target["template_id"] == "ninerow_base_w1_c3_d1", "wrong target template")
    require(target["assignment_strategy"] == "fiber_round_robin", "wrong target assignment")
    require(target["basis_id"] == "basisaware_1_4_7_8_9_10", "wrong target basis")
    require(target["basis_class_indices"] == [1, 4, 7, 8, 9, 10], "wrong basis classes")
    require(target["basis_support_sizes"] == [179, 142, 105, 105, 74, 74], "wrong support sizes")
    require(target["coefficient_matrix_shape"] == [14, 6], "wrong coefficient matrix shape")
    require(target["row_classes"] == [0, 2, 3, 5, 6, 11, 12, 13, 14, 15, 16, 17, 18, 19], "wrong row classes")
    require(target["pair_projection_labels"] == [
        "P12", "P13", "P14", "P15", "P16", "P17",
        "P23", "P24", "P25", "P26", "P27",
        "P34", "P35", "P36", "P37",
        "P45", "P46", "P47",
        "P56", "P57",
        "P67",
    ], "wrong pair projection labels")
    require(target["pinned_direction"] == [0, 5, 0, 0, 0, 1], "wrong pinned direction")
    require(target["pinned_inactive_row_classes"] == [13, 16, 17, 18, 19], "wrong pinned inactive classes")
    require(target["pinned_active_row_classes"] == [0, 2, 3, 5, 6, 11, 12, 14, 15], "wrong pinned active classes")

    pinned = target["pinned_chamber"]
    require(pinned["zero_row_count"] == 5, "wrong pinned zero count")
    require(pinned["active_row_count"] == 9, "wrong pinned active count")
    require(pinned["inactive_rank"] == 5, "wrong pinned inactive rank")
    require(pinned["inactive_kernel_nullity"] == 1, "wrong pinned inactive nullity")
    require(pinned["zero_row_classes"] == [13, 16, 17, 18, 19], "wrong pinned zero classes")
    require(pinned["active_row_classes"] == [0, 2, 3, 5, 6, 11, 12, 14, 15], "wrong pinned active classes")
    require(pinned["exemplar_direction_projective"] == [0, 1, 0, 0, 0, 7], "wrong pinned projective direction")
    require(pinned["forced_pairs"] == [], "unexpected pinned forced pairs")
    require(all(int(value) % 17 for value in pinned["pair_projection_scalars"].values()), "zero pinned pair scalar")

    search = record["chamber_search"]
    require(search["field"] == "GF(17)", "wrong search field")
    require(search["full_projective_directions"] == 1508598, "wrong projective direction count")
    require(search["direction_limit"] is None, "search unexpectedly limited")
    require(search["directions_tested"] == 1508598, "wrong directions tested")
    require(search["pair_clear_directions"] == 360360, "wrong pair-clear direction count")
    require(search["distinct_pair_clear_chambers"] == 51, "wrong chamber count")
    require(search["pair_clear_nine_row_or_better_chambers"] == 1, "wrong nine-row chamber count")
    require(search["direct_support_reduced_directions"] == 0, "unexpected support-reduced directions")
    require(search["direct_support_reduced_chambers"] == 0, "unexpected support-reduced chambers")
    require(search["rank_slack_directions"] == 0, "unexpected rank-slack directions")
    require(search["rank_slack_chambers"] == 0, "unexpected rank-slack chambers")
    require(search["extension_chambers_tested"] == 50, "wrong extension chamber count")
    require(search["extension_tests"] == 571, "wrong extension tests")
    require(search["extension_pairclear_successes"] == 134, "wrong extension successes")
    require(search["support_reduced_extensions"] == 0, "unexpected support-reduced extensions")
    require(search["best_failure_mode"] == "CHAMBER_NINE_ROW_STABLE", "wrong failure mode")
    require(search["best_rank_slack_chamber"] is None, "rank-slack chamber should be absent")
    require(search["best_direct_support_reduced_chamber"] is None, "support-reduced chamber should be absent")
    require(search["best_support_reduced_extension"] is None, "support-reduced extension should be absent")
    require(search["best_nine_row_chamber"]["zero_row_classes"] == [13, 16, 17, 18, 19], "wrong best nine-row classes")
    require(search["best_nine_row_chamber"]["inactive_rank"] == 5, "wrong best nine-row rank")

    for phrase in [
        "CANDIDATE / CHAMBER_NINE_ROW_STABLE",
        "projective directions tested = 1508598",
        "pair-clear directions = 360360",
        "distinct pair-clear support chambers = 51",
        "direct support-reduced chambers = 0",
        "rank-slack chambers = 0",
        "support-reduced extensions = 0",
        "not an MCA row",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    for phrase in [
        "projective_directions",
        "rank_slack_chambers",
        "support_reduced_extensions",
        "global obstruction outside the base direction-support chamber front",
    ]:
        require(phrase in scan_text, f"scan missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "directions_tested": search["directions_tested"],
        "pair_clear_directions": search["pair_clear_directions"],
        "distinct_pair_clear_chambers": search["distinct_pair_clear_chambers"],
        "rank_slack_chambers": search["rank_slack_chambers"],
        "support_reduced_extensions": search["support_reduced_extensions"],
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
        print(f"PASS: M1 a=327 pair-clear direction support chamber search (status={result['proof_status']})")


if __name__ == "__main__":
    main()
