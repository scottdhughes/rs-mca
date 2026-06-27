#!/usr/bin/env python3
"""Emit the M1 interleaved-list threshold interval-sharpening ledger.

This packet sharpens the open interval left by the threshold-descent
certificate.  It keeps the track separation explicit: all counts are for the
standard interleaved-list predicate, not MCA N_bad.
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
GATE_NUMERATOR = 7
CERTIFIED_START = 384
DESCENT_START = 383
COMMON_ROOT_SIZE = K - 2
LINEAR_OVERLAP_AGREEMENT = 292
ROOT_PENCIL_ROOT_SIZE = K - 1


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
    quotient, remainder = divmod(total_incidence, universe_size)
    return (
        remainder * math.comb(quotient + 1, 2)
        + (universe_size - remainder) * math.comb(quotient, 2)
    )


def packing_gate_row(agreement: int, witness_count: int = GATE_NUMERATOR) -> dict[str, Any]:
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
    complement_size = N - ROOT_PENCIL_ROOT_SIZE
    extra_needed = agreement - ROOT_PENCIL_ROOT_SIZE
    if extra_needed <= 0:
        lower: int | str = "at_least_field_size"
        clears = True
    else:
        lower = complement_size // extra_needed
        clears = lower >= GATE_NUMERATOR
    return {
        "construction": "root_pencil_scalar_multiples",
        "root_set_size": ROOT_PENCIL_ROOT_SIZE,
        "root_polynomial_degree": ROOT_PENCIL_ROOT_SIZE,
        "degree_less_than_k": ROOT_PENCIL_ROOT_SIZE < K,
        "complement_size": complement_size,
        "extra_positions_needed_per_witness": extra_needed,
        "lambda_mu_lower_bound": lower,
        "clears_gate": clears,
    }


def linear_overlap_witness() -> dict[str, Any]:
    """Seven witnesses at a=292 from a 254-root core and linear residuals."""

    agreement = LINEAR_OVERLAP_AGREEMENT
    complement_size = N - COMMON_ROOT_SIZE
    extra_needed = agreement - COMMON_ROOT_SIZE
    overlap_points = [
        {"point_label": "x1", "active_witnesses": [0, 1]},
        {"point_label": "x2", "active_witnesses": [0, 2]},
        {"point_label": "x3", "active_witnesses": [0, 3]},
        {"point_label": "x4", "active_witnesses": [0, 4]},
        {"point_label": "x5", "active_witnesses": [0, 5]},
        {"point_label": "x6", "active_witnesses": [0, 6]},
        {"point_label": "y12", "active_witnesses": [1, 2]},
        {"point_label": "y34", "active_witnesses": [3, 4]},
    ]
    overlap_count_by_witness = [0] * GATE_NUMERATOR
    for point in overlap_points:
        for witness in point["active_witnesses"]:
            overlap_count_by_witness[witness] += 1
    unique_needed_by_witness = [
        extra_needed - overlap_count for overlap_count in overlap_count_by_witness
    ]
    unique_total = sum(unique_needed_by_witness)
    used_complement_points = len(overlap_points) + unique_total
    residuals = [
        {"witness": 0, "residual": "0"},
        {"witness": 1, "residual": "X - x1"},
        {"witness": 2, "residual": "((y12-x1)/(y12-x2))*(X - x2)"},
        {"witness": 3, "residual": "X - x3"},
        {"witness": 4, "residual": "((y34-x3)/(y34-x4))*(X - x4)"},
        {"witness": 5, "residual": "X - x5"},
        {"witness": 6, "residual": "X - x6"},
    ]
    return {
        "construction": "common_254_root_core_with_controlled_linear_overlaps",
        "agreement": agreement,
        "common_root_size": COMMON_ROOT_SIZE,
        "common_root_polynomial_degree": COMMON_ROOT_SIZE,
        "residual_degree": 1,
        "codeword_degree_bound": COMMON_ROOT_SIZE + 1,
        "degree_less_than_k": COMMON_ROOT_SIZE + 1 < K,
        "complement_size": complement_size,
        "extra_positions_needed_per_witness": extra_needed,
        "overlap_points": overlap_points,
        "overlap_point_count": len(overlap_points),
        "overlap_count_by_witness": overlap_count_by_witness,
        "unique_needed_by_witness": unique_needed_by_witness,
        "unique_total": unique_total,
        "used_complement_points": used_complement_points,
        "uses_all_complement_points": used_complement_points == complement_size,
        "lambda_mu_lower_bound": GATE_NUMERATOR,
        "clears_gate": True,
        "residuals": residuals,
        "generic_choice_budget": {
            "complement_points": complement_size,
            "star_points_chosen_first": 6,
            "available_after_star_points": complement_size - 6,
            "forbidden_y12_upper_bound": 12,
            "forbidden_y34_upper_bound_after_y12": 14,
            "capacity_ok": complement_size - 6 > 12 and complement_size - 7 > 14,
        },
        "generic_choice_status": "finite-exclusion choice has ample complement capacity",
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


def classify_interval_row(agreement: int) -> dict[str, Any]:
    packing = packing_gate_row(agreement)
    root_pencil = root_pencil_lower_bound(agreement)
    linear = linear_overlap_witness() if agreement == LINEAR_OVERLAP_AGREEMENT else None
    if packing["gate_witness_count_impossible"]:
        status = "ROUTE_CUT"
        lambda_upper = GATE_NUMERATOR - 1
        lambda_lower = root_pencil["lambda_mu_lower_bound"]
        clears_possible = False
        clears_proved = False
        construction = root_pencil
    elif linear is not None:
        status = "LOWER_ONLY"
        lambda_upper = None
        lambda_lower = linear["lambda_mu_lower_bound"]
        clears_possible = True
        clears_proved = True
        construction = linear
    else:
        status = "PARTIAL"
        lambda_upper = None
        lambda_lower = root_pencil["lambda_mu_lower_bound"]
        clears_possible = True
        clears_proved = False
        construction = root_pencil
    lower_numeric = lambda_lower if isinstance(lambda_lower, int) else GATE_NUMERATOR
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "field_denominator": "17^32",
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": GATE_NUMERATOR,
        "agreement": agreement,
        "radius_closed": f"{N-agreement}/{N}",
        "lambda_lower": lambda_lower,
        "lambda_upper": lambda_upper,
        "packing_upper": lambda_upper,
        "root_pencil_lower": root_pencil["lambda_mu_lower_bound"],
        "gap": None if lambda_upper is None else lambda_upper - lower_numeric,
        "clears_gate_proved": clears_proved,
        "clears_gate_possible": clears_possible,
        "status": status,
        "mca_counted": False,
        "mca_reason": "separate interleaved-list track; no bridge to N_bad",
        "predicate": "standard Lambda_mu(C,a) interleaved-list predicate",
        "packing_test": packing,
        "construction": construction,
    }


def interval_rows() -> list[dict[str, Any]]:
    return [
        classify_interval_row(agreement)
        for agreement in range(DESCENT_START, LINEAR_OVERLAP_AGREEMENT - 1, -1)
    ]


def build_result() -> dict[str, Any]:
    high_rows = certified_rows()
    rows = interval_rows()
    route_cut_rows = [row["agreement"] for row in rows if row["status"] == "ROUTE_CUT"]
    partial_rows = [row["agreement"] for row in rows if row["status"] == "PARTIAL"]
    lower_rows = [row for row in rows if row["clears_gate_proved"]]
    first_possible = next(row["agreement"] for row in rows if row["clears_gate_possible"])
    first_proved = max(row["agreement"] for row in lower_rows)
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
        "first_proved_clear_agreement_by_linear_overlap": first_proved,
        "route_cut_interval_by_packing": {
            "descending_from": max(route_cut_rows),
            "descending_to": min(route_cut_rows),
            "status": "Lambda_mu_upper_bound_at_most_6",
        },
        "open_partial_interval": {
            "descending_from": max(partial_rows),
            "descending_to": min(partial_rows),
            "status": "packing_permits_seven_but_no_lower_bound_yet",
        },
        "proved_clear_row": next(
            row for row in rows if row["agreement"] == first_proved
        ),
        "prior_root_pencil_clear_agreement": 291,
        "improves_prior_root_pencil_clear_by": first_proved - 291,
        "certified_agreements": high_rows,
        "interval_agreements": rows,
        "status": "THRESHOLD_INTERVAL_SHARPENED_LOWER_ONLY_CLEAR_AT_292",
        "non_claims": [
            "not_mca_n_bad",
            "not_protocol_soundness",
            "not_ordinary_list_decoding_failure",
            "not_exact_lambda_values_in_partial_interval",
            "not_exact_lambda_mu_at_292",
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
        default="experimental/data/m1_interleaved_list_threshold_interval_sharpening.json",
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
        print("open interval after sharpening: 293 <= a <= 372")
        print("first proved clear: a=292")


if __name__ == "__main__":
    main()
