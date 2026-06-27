#!/usr/bin/env python3
"""Emit the M1 interleaved-list threshold descent atlas.

The atlas separates three facts for the active F_17^32 row:

* high-agreement uniqueness gives Lambda_mu(C,a)=1 for a>=384;
* support-occupancy packing rules out seven witnesses for 373<=a<=383;
* a root-pencil construction proves seven witnesses by a=291.

It does not claim exact Lambda_mu values in the open interval.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


N = 512
K = 256
P = 17
FIELD_DEGREE = 32
TARGET_BITS = 128
CERTIFIED_START = 384
DESCENT_START = 383
GATE_NUMERATOR = 7
ROOT_SET_SIZE = K - 1
COMPLEMENT_SIZE = N - ROOT_SET_SIZE


def q_field() -> int:
    return P**FIELD_DEGREE


def threshold_floor() -> int:
    return q_field() // (2**TARGET_BITS)


def uniqueness_start(n: int, k: int) -> int:
    return (n + k + 1) // 2


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def minimum_pair_intersections(universe_size: int, total_incidence: int) -> int:
    """Minimum sum_x binom(c_x,2) when sum_x c_x=total_incidence."""

    quotient, remainder = divmod(total_incidence, universe_size)
    return (
        remainder * math.comb(quotient + 1, 2)
        + (universe_size - remainder) * math.comb(quotient, 2)
    )


def packing_gate_row(agreement: int, witness_count: int = GATE_NUMERATOR) -> dict[str, Any]:
    """Return the agreement-support packing test for `witness_count` supports."""

    support_intersection_upper = K - 1
    total_incidence_lower = witness_count * agreement
    pair_overlap_lower = minimum_pair_intersections(N, total_incidence_lower)
    pair_overlap_budget = math.comb(witness_count, 2) * support_intersection_upper
    impossible = pair_overlap_lower > pair_overlap_budget
    return {
        "hypothetical_witness_count": witness_count,
        "agreement": agreement,
        "support_size_lower": agreement,
        "pair_support_intersection_upper_by_mds": support_intersection_upper,
        "total_support_incidence_lower": total_incidence_lower,
        "pair_overlap_lower_by_convexity": pair_overlap_lower,
        "pair_overlap_budget_from_pairwise_bound": pair_overlap_budget,
        "gate_witness_count_impossible": impossible,
    }


def root_pencil_lower_bound(agreement: int) -> dict[str, Any]:
    """Root-pencil lower bound from scalar multiples of one root polynomial."""

    extra_needed = agreement - ROOT_SET_SIZE
    if extra_needed <= 0:
        lower = "at_least_field_size"
        clears = True
    else:
        lower = COMPLEMENT_SIZE // extra_needed
        clears = lower >= GATE_NUMERATOR
    return {
        "construction": "root_pencil_scalar_multiples",
        "root_set_size": ROOT_SET_SIZE,
        "root_polynomial_degree": ROOT_SET_SIZE,
        "degree_less_than_k": ROOT_SET_SIZE < K,
        "complement_size": COMPLEMENT_SIZE,
        "extra_positions_needed_per_witness": extra_needed,
        "lambda_mu_lower_bound": lower,
        "clears_gate": clears,
    }


def classify_descent_row(agreement: int) -> dict[str, Any]:
    packing = packing_gate_row(agreement)
    lower = root_pencil_lower_bound(agreement)
    lower_value = lower["lambda_mu_lower_bound"]
    lower_numeric = lower_value if isinstance(lower_value, int) else GATE_NUMERATOR
    if packing["gate_witness_count_impossible"]:
        status = "ROUTE_CUT"
        clears_gate_possible = False
        lambda_upper = GATE_NUMERATOR - 1
    elif lower["clears_gate"]:
        status = "LOWER_ONLY"
        clears_gate_possible = True
        lambda_upper = None
    else:
        status = "PARTIAL"
        clears_gate_possible = True
        lambda_upper = None
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "field_denominator": "17^32",
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": GATE_NUMERATOR,
        "agreement": agreement,
        "radius_closed": f"{N-agreement}/{N}",
        "lambda_lower": lower_value,
        "lambda_upper": lambda_upper,
        "packing_upper": lambda_upper,
        "root_pencil_lower": lower_value,
        "gap": None if lambda_upper is None else lambda_upper - lower_numeric,
        "clears_gate_proved": lower["clears_gate"],
        "clears_gate_possible": clears_gate_possible,
        "status": status,
        "mca_counted": False,
        "mca_reason": "separate interleaved-list track; no bridge to N_bad",
        "predicate": "standard Lambda_mu(C,a) interleaved-list predicate",
        "packing_test": packing,
        "root_pencil_witness": lower,
    }


def certified_rows() -> list[dict[str, Any]]:
    return [
        {
            "agreement": a,
            "radius_closed": f"{N-a}/{N}",
            "lambda_lower": 1,
            "lambda_upper": 1,
            "lambda_exact": 1,
            "clears_gate_proved": False,
            "clears_gate_possible": False,
            "status": "PROOF_RECORD",
            "predicate_status": "PROOF_RECORD_UNIQUENESS",
        }
        for a in range(N, CERTIFIED_START - 1, -1)
    ]


def descent_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    agreement = DESCENT_START
    while agreement > ROOT_SET_SIZE:
        row = classify_descent_row(agreement)
        rows.append(row)
        if row["clears_gate_proved"]:
            break
        agreement -= 1
    return rows


def build_result() -> dict[str, Any]:
    high_rows = certified_rows()
    down_rows = descent_rows()
    first_possible = next(
        row["agreement"] for row in down_rows if row["clears_gate_possible"]
    )
    first_proved = next(
        row["agreement"] for row in down_rows if row["clears_gate_proved"]
    )
    route_cut_rows = [
        row["agreement"] for row in down_rows if row["status"] == "ROUTE_CUT"
    ]
    partial_rows = [
        row["agreement"] for row in down_rows if row["status"] == "PARTIAL"
    ]
    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "field_denominator": str(q_field()),
        "field_denominator_label": "17^32",
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": GATE_NUMERATOR,
        "known_certified_interval": {
            "from": uniqueness_start(N, K),
            "to": N,
            "lambda_mu": 1,
            "row_count": len(high_rows),
        },
        "descent_start": DESCENT_START,
        "first_possible_clear_agreement_by_packing": first_possible,
        "first_proved_clear_agreement_by_root_pencil": first_proved,
        "route_cut_interval_by_packing": {
            "descending_from": max(route_cut_rows),
            "descending_to": min(route_cut_rows),
            "status": "Lambda_mu_upper_bound_at_most_6",
        },
        "open_partial_interval": {
            "descending_from": max(partial_rows),
            "descending_to": min(partial_rows),
            "status": "packing_permits_seven_but_root_pencil_lower_below_gate",
        },
        "proved_clear_row": next(
            row for row in down_rows if row["agreement"] == first_proved
        ),
        "certified_agreements": high_rows,
        "descent_agreements": down_rows,
        "status": "THRESHOLD_DESCENT_LOWER_ONLY_CLEAR_AT_291",
        "non_claims": [
            "not_mca_n_bad",
            "not_protocol_soundness",
            "not_ordinary_list_decoding_failure",
            "not_exact_lambda_values_in_partial_interval",
            "not_exact_delta_star_C",
        ],
    }
    result["record_hash"] = hash_payload(
        {
            "first_possible": first_possible,
            "first_proved": first_proved,
            "route_cut_interval": result["route_cut_interval_by_packing"],
            "partial_interval": result["open_partial_interval"],
            "proved_clear_hash": hash_payload(result["proved_clear_row"]),
        }
    )
    return result


def write_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_result(), indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default="experimental/data/m1_interleaved_list_threshold_descent.json",
        type=Path,
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_result()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output)
        print(f"WROTE {args.output}")
        print("packing route cut: 373 <= a <= 383")
        print("first packing-possible clear: a=372")
        print("first root-pencil proved clear: a=291")


if __name__ == "__main__":
    main()
