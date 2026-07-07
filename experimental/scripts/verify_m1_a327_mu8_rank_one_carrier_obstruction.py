#!/usr/bin/env python3
"""Verify the rank-one mu_8 carrier incidence obstruction packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("experimental/data/m1_a327_mu8_rank_one_carrier_obstruction.json")


def fail(message: str) -> None:
    raise SystemExit(f"VERIFY_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify(record: dict[str, Any]) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong agreement target")
    require(record["mca_counted"] is False, "MCA counted")
    require(
        record["proof_status"]
        == "CONSTRUCTION_FAIL / MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )

    obstruction = record["rank_one_mu8_carrier_obstruction"]
    quotient_roots_max = 32 - 1
    common_zero_coordinates_max = 8 * quotient_roots_max
    outside_pair_equalities_max = 21 * 7
    selected_incidence_ceiling = 512 + 6 * common_zero_coordinates_max + outside_pair_equalities_max
    required_selected_incidences = 7 * 327
    strict_gap = required_selected_incidences - selected_incidence_ceiling

    require(obstruction["ansatz"] == "q(Y)=u*f(Y), deg(f)<32", "wrong ansatz")
    require(obstruction["pair_visible_required"] is True, "pair-visible guard missing")
    require(obstruction["quotient_roots_max"] == quotient_roots_max, "wrong quotient root bound")
    require(
        obstruction["common_zero_coordinates_max"] == common_zero_coordinates_max,
        "wrong common-zero coordinate bound",
    )
    require(
        obstruction["outside_pair_equalities_max"] == outside_pair_equalities_max,
        "wrong outside pair-equality bound",
    )
    require(
        obstruction["selected_incidence_ceiling"] == selected_incidence_ceiling,
        "wrong selected incidence ceiling",
    )
    require(
        obstruction["required_selected_incidences"] == required_selected_incidences,
        "wrong required selected incidence count",
    )
    require(obstruction["strict_gap"] == strict_gap, "wrong strict gap")
    require(obstruction["contradiction"] is True, "contradiction not recorded")
    require(selected_incidence_ceiling < required_selected_incidences, "incidence ceiling does not contradict target")
    require(obstruction["status"] == "MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION", "wrong obstruction status")

    return {
        "status": "M1_A327_MU8_RANK_ONE_CARRIER_OBSTRUCTION_VERIFY_PASS",
        "path": str(DEFAULT_INPUT),
        "common_zero_coordinates_max": common_zero_coordinates_max,
        "outside_pair_equalities_max": outside_pair_equalities_max,
        "selected_incidence_ceiling": selected_incidence_ceiling,
        "required_selected_incidences": required_selected_incidences,
        "strict_gap": strict_gap,
        "mca_counted": record["mca_counted"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    summary = verify(load_json(args.input))
    summary["path"] = str(args.input)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(summary["status"])


if __name__ == "__main__":
    main()
