#!/usr/bin/env python3
"""Verify the M1 a=327 pair-clear cyclic tail/mixed obstruction ledger."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a327_pairclear_cyclic_tail_mixed_obstruction.json")
NOTE_PATH = Path("experimental/notes/m1/m1_a327_pairclear_cyclic_tail_mixed_obstruction.md")
TAIL_DATA = Path("experimental/data/m1_a327_pairclear_tailpair_projection_repair.json")
P456_DATA = Path("experimental/data/m1_a327_pairclear_p45_p46_p56_codesign.json")
P46P67_DATA = Path("experimental/data/m1_a327_pairclear_p46_p67_tradeoff_repair.json")

REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested rank-slack pair-clear front",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify_tail(record: dict[str, Any], source: dict[str, Any]) -> None:
    section = record["tailpair_projection_repair"]
    search = source["tailpair_projection_repair"]
    best = source["best_profile"]
    info = best["tailpair_projection"]
    require(section["basis_profiles_tested"] == search["basis_profiles_tested"] == 2856, "tail basis count mismatch")
    require(section["target_rows_present_profiles"] == search["target_rows_present_profiles"] == 2024, "tail target-present mismatch")
    require(section["extended_rank_slack_profiles"] == search["extended_rank_slack_profiles"] == 112, "tail rank-slack mismatch")
    require(section["tail_candidates"] == search["tail_candidates"] == 112, "tail candidate mismatch")
    require(section["deep_rank_slack_repair_profiles"] == search["deep_rank_slack_repair_profiles"] == 0, "tail deep repair mismatch")
    require(section["best_template_id"] == best["template_id"] == "ninerow_P17_shear_c1_d1", "tail template mismatch")
    require(section["best_basis_id"] == best["basis_id"] == "targetaware_0_1_2_3_4_13", "tail basis mismatch")
    require(section["best_direction"] == info["direction"] == [0, 0, 1, 1, 2, 0], "tail direction mismatch")
    require(section["best_forced_pairs"] == info["forced_pairs"] == ["P45", "P46", "P56"], "tail forced pairs mismatch")
    require(section["best_failure_mode"] == search["best_failure_mode"] == "TAILPAIR_FORCED_PROJECTIONS_REMAIN", "tail failure mismatch")


def verify_p456(record: dict[str, Any], source: dict[str, Any]) -> None:
    section = record["p45_p46_p56_codesign"]
    search = source["p45_p46_p56_codesign"]
    best = source["best_profile"]
    info = best["extended_codesign_direction"]
    require(section["basis_profiles_tested"] == search["basis_profiles_tested"] == 6850, "P456 basis count mismatch")
    require(section["target_rows_present_profiles"] == search["target_rows_present_profiles"] == 5010, "P456 target-present mismatch")
    require(section["extended_rank_slack_profiles"] == search["extended_rank_slack_profiles"] == 320, "P456 rank-slack mismatch")
    require(section["exact_pairclear_profiles"] == search["exact_pairclear_profiles"] == 0, "P456 exact mismatch")
    require(section["target_repaired_profiles"] == search["target_repaired_profiles"] == 0, "P456 repaired mismatch")
    require(section["near_repair_profiles"] == search["near_repair_profiles"] == 0, "P456 near mismatch")
    require(section["best_template_id"] == best["template_id"] == "ninerow_W57_c13_pm1", "P456 template mismatch")
    require(section["best_basis_id"] == best["basis_id"] == "targetaware_0_1_2_3_4_10", "P456 basis mismatch")
    require(section["best_direction"] == info["direction"] == [0, 0, 0, 1, 0, 2], "P456 direction mismatch")
    require(section["best_forced_pairs"] == info["forced_pairs"] == ["P14", "P16", "P17", "P46", "P47", "P67"], "P456 forced pairs mismatch")
    require(section["best_target_pairs_cleared"] == info["target_pairs_cleared"] == ["P45", "P56"], "P456 target clearance mismatch")
    require(section["best_preserve_pairs_cleared"] == info["preserve_pairs_cleared"] == ["P57"], "P456 preserve clearance mismatch")
    require(section["best_failure_mode"] == search["best_failure_mode"] == "P456_FORCED_PROJECTIONS_REMAIN", "P456 failure mismatch")


def verify_p46p67(record: dict[str, Any], source: dict[str, Any]) -> None:
    section = record["p46_p67_tradeoff_repair"]
    search = source["p46_p67_tradeoff_repair"]
    best = source["best_profile"]
    info = best["extended_tradeoff_direction"]
    require(section["basis_profiles_tested"] == search["basis_profiles_tested"] == 6850, "P46/P67 basis count mismatch")
    require(section["target_rows_present_profiles"] == search["target_rows_present_profiles"] == 5010, "P46/P67 target-present mismatch")
    require(section["extended_rank_slack_profiles"] == search["extended_rank_slack_profiles"] == 320, "P46/P67 rank-slack mismatch")
    require(section["exact_pairclear_profiles"] == search["exact_pairclear_profiles"] == 0, "P46/P67 exact mismatch")
    require(section["tradeoff_repaired_profiles"] == search["tradeoff_repaired_profiles"] == 0, "P46/P67 repair mismatch")
    require(section["clean_tradeoff_repaired_profiles"] == search["clean_tradeoff_repaired_profiles"] == 0, "P46/P67 clean mismatch")
    require(section["near_repair_profiles"] == search["near_repair_profiles"] == 0, "P46/P67 near mismatch")
    require(section["best_template_id"] == best["template_id"] == "ninerow_P14_shear_c1_d1", "P46/P67 template mismatch")
    require(section["best_basis_id"] == best["basis_id"] == "targetaware_0_1_2_3_4_13", "P46/P67 basis mismatch")
    require(section["best_direction"] == info["direction"] == [0, 1, 1, 2, 0, 0], "P46/P67 direction mismatch")
    require(section["best_forced_pairs"] == info["forced_pairs"] == ["P56", "P57", "P67"], "P46/P67 forced pairs mismatch")
    require(section["best_repair_pairs_cleared"] == info["repair_pairs_cleared"] == ["P46"], "P46/P67 repair clearance mismatch")
    require(section["best_preserve_pairs_cleared"] == info["preserve_pairs_cleared"] == ["P45"], "P46/P67 preserve clearance mismatch")
    require(section["best_spillover_pairs_cleared"] == info["spillover_pairs_cleared"] == ["P14", "P16", "P17", "P47"], "P46/P67 spillover clearance mismatch")
    require(section["best_failure_mode"] == search["best_failure_mode"] == "P46P67_FORCED_PROJECTIONS_REMAIN", "P46/P67 failure mismatch")


def verify() -> dict[str, Any]:
    record = load_json(DATA_PATH)
    note_text = NOTE_PATH.read_text()
    tail = load_json(TAIL_DATA)
    p456 = load_json(P456_DATA)
    p46p67 = load_json(P46P67_DATA)

    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["source_commit"] == "75dc8b8", "wrong source commit")
    require(record["mca_counted"] is False, "MCA counted unexpectedly")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")
    require(record["proof_status"] == "AUDIT / ROUTE_CUT_LOCAL_PAIRCLEAR_FRONT / EXPERIMENTAL", "wrong proof status")
    require(record["cycle_scope"]["extended_zero_classes"] == [6, 7, 8, 14, 17, 18, 19, 20], "wrong zero classes")
    require(record["cycle_scope"]["extended_rank_guard"] == "<=4", "wrong rank guard")
    require(record["cycle_scope"]["kernel_dimension"] == 2, "wrong kernel dimension")

    verify_tail(record, tail)
    verify_p456(record, p456)
    verify_p46p67(record, p46p67)

    diagnosis = record["cycle_diagnosis"]
    require(diagnosis["tail_front"] == ["P56", "P57", "P67"], "wrong tail front")
    require(diagnosis["mixed_front"] == ["P14", "P16", "P17", "P46", "P47", "P67"], "wrong mixed front")
    require(diagnosis["p456_front"] == ["P45", "P46", "P56"], "wrong P456 front")
    require(
        diagnosis["observed_cycle"]
        == [
            ["P56", "P57", "P67"],
            ["P45", "P46", "P56"],
            ["P14", "P16", "P17", "P46", "P47", "P67"],
            ["P56", "P57", "P67"],
        ],
        "wrong observed cycle",
    )
    require("No tested nullity-2 rank-slack kernel direction" in diagnosis["route_cut"], "route cut too broad or missing")

    for phrase in [
        "AUDIT / ROUTE_CUT_LOCAL_PAIRCLEAR_FRONT / EXPERIMENTAL",
        "extended zero classes = [6,7,8,14,17,18,19,20]",
        "basis profiles tested = 2856",
        "basis profiles tested = 6850",
        "[P56,P57,P67]",
        "[P45,P46,P56]",
        "[P14,P16,P17,P46,P47,P67]",
        "No tested nullity-2 rank-slack kernel direction",
        "not an MCA row",
        "Do not rerank the same nullity-2 kernels again",
    ]:
        require(phrase in note_text, f"note missing phrase: {phrase}")

    return {
        "status": "PASS",
        "proof_status": record["proof_status"],
        "tail_forced_pairs": record["tailpair_projection_repair"]["best_forced_pairs"],
        "mixed_forced_pairs": record["p45_p46_p56_codesign"]["best_forced_pairs"],
        "return_forced_pairs": record["p46_p67_tradeoff_repair"]["best_forced_pairs"],
        "route_cut": record["cycle_diagnosis"]["route_cut"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"PASS: M1 a=327 pair-clear cyclic tail/mixed obstruction (status={result['proof_status']})")


if __name__ == "__main__":
    main()
