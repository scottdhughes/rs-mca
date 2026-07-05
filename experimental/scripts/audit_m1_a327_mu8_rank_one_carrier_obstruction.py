#!/usr/bin/env python3
"""Record the incidence obstruction for rank-one mu_8 carriers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


OUTPUT_DATA = Path("experimental/data/m1_a327_mu8_rank_one_carrier_obstruction.json")

FIELD_DENOMINATOR = "17^32"
H_ORDER = 512
MU_ORDER = 8
QUOTIENT_DEGREE_BOUND = 32
PAIR_COUNT = 21
PAIR_FACTOR_DEGREE_BOUND = 7
LIST_SIZE = 7
TARGET_AGREEMENT = 327

NOT_CLAIMED = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
]


def build_record() -> dict:
    quotient_roots_max = QUOTIENT_DEGREE_BOUND - 1
    common_zero_coordinates_max = MU_ORDER * quotient_roots_max
    outside_pair_equalities_max = PAIR_COUNT * PAIR_FACTOR_DEGREE_BOUND
    selected_incidence_ceiling = (
        H_ORDER
        + (LIST_SIZE - 1) * common_zero_coordinates_max
        + outside_pair_equalities_max
    )
    required_selected_incidences = LIST_SIZE * TARGET_AGREEMENT
    contradiction = selected_incidence_ceiling < required_selected_incidences
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": FIELD_DENOMINATOR,
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "83c6f93",
        "rank_one_mu8_carrier_obstruction": {
            "ansatz": "q(Y)=u*f(Y), deg(f)<32",
            "pair_visible_required": True,
            "quotient_roots_max": quotient_roots_max,
            "common_zero_coordinates_max": common_zero_coordinates_max,
            "outside_pair_equalities_max": outside_pair_equalities_max,
            "selected_incidence_ceiling": selected_incidence_ceiling,
            "required_selected_incidences": required_selected_incidences,
            "strict_gap": required_selected_incidences - selected_incidence_ceiling,
            "contradiction": contradiction,
            "status": "MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION",
        },
        "proof_status": (
            "CONSTRUCTION_FAIL / MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION "
            "/ PARTIAL / EXPERIMENTAL"
        ),
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write_json:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        "selected_incidence_ceiling": record["rank_one_mu8_carrier_obstruction"][
            "selected_incidence_ceiling"
        ],
        "required_selected_incidences": record["rank_one_mu8_carrier_obstruction"][
            "required_selected_incidences"
        ],
        "strict_gap": record["rank_one_mu8_carrier_obstruction"]["strict_gap"],
        "status": record["rank_one_mu8_carrier_obstruction"]["status"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write_json:
        print("M1_A327_MU8_RANK_ONE_CARRIER_OBSTRUCTION_READY")


if __name__ == "__main__":
    main()
