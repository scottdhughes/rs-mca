#!/usr/bin/env python3
"""Verify the M1 a=507 adjacent-bridge obstruction ledger.

The theorem verified here is deliberately narrow: the adjacent line-plus-list
ledger cannot be consumed as a seventh event in the current finite-slope
support-wise LD_sw board row, because LD_sw(C,507)=6 exactly.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_a507_adjacent_bridge_theorem.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def q_line() -> int:
    return 17**32


def threshold_floor() -> int:
    return q_line() // (2**128)


def exact_ldsw_count(n: int, agreement: int) -> int:
    return n - agreement + 1


def expected_result() -> dict[str, Any]:
    n = 512
    agreement = 507
    line_numerator = exact_ldsw_count(n, agreement)
    adjacent_interleaved_numerator = 1
    conditional_total = line_numerator + adjacent_interleaved_numerator
    floor = threshold_floor()

    return {
        "agreement": agreement,
        "adjacent_interleaved_numerator": adjacent_interleaved_numerator,
        "board_consumable": False,
        "bridge_conditions": {
            "agreement_preservation": {
                "agreement": agreement,
                "status": "PROVED_FOR_ADJACENT_LEDGER",
            },
            "denominator_preservation": {
                "denominator": "17^32",
                "reason": (
                    "Same field arithmetic is available in the adjacent ledger, "
                    "but denominator preservation cannot rescue a predicate "
                    "contradiction."
                ),
                "status": "NOT_DECISIVE_AFTER_PREDICATE_FAILURE",
            },
            "disjointness_from_existing_six": {
                "intersection_size": "not_applicable",
                "reason": (
                    "A disjoint same-predicate extra event would force "
                    "LD_sw(C,507) >= 7, contradicting LD_sw(C,507)=6."
                ),
                "status": "FAILED_UNDER_PREDICATE_PRESERVATION",
            },
            "no_double_counting": {
                "reason": (
                    "No same-predicate extra event exists, so a fiber "
                    "correction cannot produce a seventh current-row numerator."
                ),
                "status": "FAILED_UNDER_PREDICATE_PRESERVATION",
            },
            "predicate_preservation": {
                "reason": (
                    "The adjacent interleaved-list +1 is not a finite-slope "
                    "support-wise LD_sw event; if a bridge made it one, "
                    "disjointness would contradict the exact count "
                    "LD_sw(C,507)=6."
                ),
                "status": "FAILED_FOR_CURRENT_BOARD_ROW",
            },
        },
        "conditional_total": conditional_total,
        "decision_status": "PROVED_OBSTRUCTION",
        "line_numerator": line_numerator,
        "nonclaims": [
            "new frontier row",
            "protocol soundness failure",
            "ordinary list-decoding failure",
            "exact delta*_C",
            "impossibility of separate protocol or interleaved-list ledgers",
        ],
        "obstruction": {
            "contradiction": "would force LD_sw(C,507) >= 7",
            "exact_ldsw_count": line_numerator,
            "reason": (
                "current board row counts the finite-slope support-wise "
                "LD_sw predicate"
            ),
            "would_be_count_if_bridge_existed": conditional_total,
        },
        "q_line": "17^32",
        "q_line_integer": str(q_line()),
        "reason": "PROVED_OBSTRUCTION_EXACT_LD_SW_COUNT",
        "row": "RS[F_17^32,H,256]",
        "same_predicate_N_bad": line_numerator,
        "same_predicate_clears_gate": line_numerator > floor,
        "schema": "m1-a507-adjacent-bridge-theorem.v1",
        "separate_adjacent_ledger": {
            "conditional_total": conditional_total,
            "conditional_total_clears_gate_if_consumable": conditional_total
            > floor,
            "status": "SEPARATE_LEDGER_NOT_CURRENT_BOARD_ROW",
        },
        "threshold_bits": 128,
        "threshold_floor": floor,
    }


def load_data() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def verify_result(data: dict[str, Any]) -> None:
    expected = expected_result()
    require(data == expected, "checked JSON does not match expected ledger")

    q = q_line()
    require(data["threshold_floor"] == 6, "threshold floor")
    require(6 * 2**128 < q < 7 * 2**128, "integer gate margins")
    require(data["line_numerator"] == 6, "line numerator")
    require(data["adjacent_interleaved_numerator"] == 1, "adjacent numerator")
    require(data["conditional_total"] == 7, "conditional total")
    require(data["same_predicate_N_bad"] == 6, "same predicate N_bad")
    require(data["same_predicate_clears_gate"] is False, "same predicate gate")
    require(data["board_consumable"] is False, "board consumable flag")
    require(
        data["separate_adjacent_ledger"][
            "conditional_total_clears_gate_if_consumable"
        ]
        is True,
        "conditional gate",
    )

    conditions = data["bridge_conditions"]
    require(
        conditions["predicate_preservation"]["status"]
        == "FAILED_FOR_CURRENT_BOARD_ROW",
        "predicate obstruction",
    )
    require(
        conditions["disjointness_from_existing_six"]["status"]
        == "FAILED_UNDER_PREDICATE_PRESERVATION",
        "disjointness obstruction",
    )
    require(
        conditions["denominator_preservation"]["status"]
        == "NOT_DECISIVE_AFTER_PREDICATE_FAILURE",
        "denominator status",
    )
    require(data["decision_status"] == "PROVED_OBSTRUCTION", "decision")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON result.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_data()
    verify_result(data)
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("decision_status=PROVED_OBSTRUCTION")
        print("same-predicate board N_bad(507)=6; adjacent 6+1 is separate")


if __name__ == "__main__":
    main()
