#!/usr/bin/env python3
"""Verify the M1 interleaved-list threshold upward-push ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_interleaved_list_threshold_upward_push.json")
N = 512
K = 256
P = 17
FIELD_DEGREE = 32
TARGET_BITS = 128
GATE_NUMERATOR = 7
CERTIFIED_START = 384
PACKING_ROUTE_CUT_START = 383
PACKING_ROUTE_CUT_END = 373


def q_field() -> int:
    return P**FIELD_DEGREE


def threshold_floor() -> int:
    return q_field() // (2**TARGET_BITS)


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def multiplicative_order(base: int, modulus: int) -> int:
    if modulus == 1:
        return 1
    if math.gcd(base, modulus) != 1:
        raise ValueError("base and modulus must be coprime")
    value = 1
    for exponent in range(1, 10_000):
        value = (value * base) % modulus
        if value == 1:
            return exponent
    raise ValueError("order search exhausted")


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


def quotient_floor_row(fiber_size: int, quotient_subset_size: int) -> dict[str, Any]:
    quotient_size = N // fiber_size
    quotient_dimension = math.ceil(K / fiber_size)
    sigma = quotient_subset_size - quotient_dimension
    agreement = fiber_size * quotient_subset_size
    quotient_field_degree = multiplicative_order(P, quotient_size)
    if sigma < 0:
        lower_bound = 0
        denominator = None
    else:
        denominator = P ** (quotient_field_degree * sigma)
        lower_bound = ceil_div(math.comb(quotient_size, quotient_subset_size), denominator)
    return {
        "fiber_size": fiber_size,
        "quotient_size": quotient_size,
        "quotient_field_size_label": f"17^{quotient_field_degree}",
        "quotient_field_degree": quotient_field_degree,
        "quotient_subset_size": quotient_subset_size,
        "agreement": agreement,
        "quotient_dimension": quotient_dimension,
        "sigma": sigma,
        "subset_count": math.comb(quotient_size, quotient_subset_size),
        "pigeonhole_denominator": denominator,
        "lambda_lower": lower_bound,
        "clears_gate": lower_bound >= GATE_NUMERATOR,
        "construction": "quotient_fiber_prefix_list_floor",
    }


def best_row_for_fiber_size(fiber_size: int) -> dict[str, Any] | None:
    quotient_size = N // fiber_size
    quotient_dimension = math.ceil(K / fiber_size)
    best: dict[str, Any] | None = None
    for quotient_subset_size in range(quotient_dimension, quotient_size + 1):
        row = quotient_floor_row(fiber_size, quotient_subset_size)
        if row["clears_gate"] and (best is None or row["agreement"] > best["agreement"]):
            best = row
    return best


def quotient_scan_rows() -> list[dict[str, Any]]:
    rows = []
    for exponent in range(10):
        fiber_size = 2**exponent
        if N % fiber_size != 0:
            continue
        best = best_row_for_fiber_size(fiber_size)
        rows.append(
            {
                "fiber_size": fiber_size,
                "best_clearing_row": best,
                "clears_some_row": best is not None,
            }
        )
    return rows


def build_expected_record() -> dict[str, Any]:
    quotient_rows = quotient_scan_rows()
    clearing_rows = [
        row["best_clearing_row"]
        for row in quotient_rows
        if row["best_clearing_row"] is not None
    ]
    best = max(clearing_rows, key=lambda row: row["agreement"])
    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "field_denominator": str(q_field()),
        "field_denominator_label": "17^32",
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "known_certified_interval": {
            "from": CERTIFIED_START,
            "to": N,
            "lambda_mu": 1,
        },
        "packing_route_cut_interval": {
            "from": PACKING_ROUTE_CUT_END,
            "to": PACKING_ROUTE_CUT_START,
            "lambda_mu_upper_bound": GATE_NUMERATOR - 1,
            "endpoint_test": packing_gate_row(PACKING_ROUTE_CUT_END),
        },
        "quotient_scan_rows": quotient_rows,
        "best_clearing_row": best,
        "open_partial_interval": {
            "from": best["agreement"] + 1,
            "to": PACKING_ROUTE_CUT_END - 1,
            "status": "packing_permits_seven_but_no_lower_bound_yet",
        },
        "improves_previous_linear_overlap_clear_agreement": 292,
        "improvement_over_previous": best["agreement"] - 292,
        "status": "THRESHOLD_UPWARD_PUSH_QUOTIENT_CLEAR_AT_320",
        "non_claims": [
            "not_mca_n_bad",
            "not_protocol_soundness",
            "not_ordinary_list_decoding_failure",
            "not_exact_lambda_mu_at_320",
            "not_exact_delta_star_C",
        ],
    }
    result["record_hash"] = hash_payload(
        {
            "best": best,
            "partial": result["open_partial_interval"],
            "route_cut": result["packing_route_cut_interval"],
        }
    )
    return result


def load_record() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text())


def verify_record(record: dict[str, Any]) -> None:
    expected = build_expected_record()
    assert record == expected
    assert record["track"] == "INTERLEAVED_LIST"
    assert int(record["field_denominator"]) == 17**32
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert 6 * 2**128 < 17**32 < 7 * 2**128

    endpoint = record["packing_route_cut_interval"]["endpoint_test"]
    assert endpoint["agreement"] == 373
    assert endpoint["pair_overlap_lower_by_convexity"] == 5375
    assert endpoint["pair_overlap_budget_from_pairwise_bound"] == 5355
    assert endpoint["gate_witness_count_impossible"] is True

    best = record["best_clearing_row"]
    assert best["fiber_size"] == 32
    assert best["quotient_size"] == 16
    assert best["quotient_field_degree"] == 1
    assert best["quotient_field_size_label"] == "17^1"
    assert best["quotient_subset_size"] == 10
    assert best["agreement"] == 320
    assert best["quotient_dimension"] == 8
    assert best["sigma"] == 2
    assert best["subset_count"] == 8008
    assert best["pigeonhole_denominator"] == 289
    assert best["lambda_lower"] == 28
    assert best["clears_gate"] is True

    assert record["open_partial_interval"] == {
        "from": 321,
        "to": 372,
        "status": "packing_permits_seven_but_no_lower_bound_yet",
    }
    assert record["improvement_over_previous"] == 28


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    record = load_record()
    verify_record(record)
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("best quotient-fiber clearing row: a=320")
        print("open interval after upward push: 321 <= a <= 372")


if __name__ == "__main__":
    main()
