#!/usr/bin/env python3
"""Verify the M1 interleaved-list threshold descent atlas."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_interleaved_list_threshold_descent.json")
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
    extra_needed = agreement - ROOT_SET_SIZE
    if extra_needed <= 0:
        lower: int | str = "at_least_field_size"
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


def build_expected_record() -> dict[str, Any]:
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


def load_record() -> dict[str, Any]:
    return json.loads(DATA_PATH.read_text())


def row_by_agreement(rows: list[dict[str, Any]], agreement: int) -> dict[str, Any]:
    matches = [row for row in rows if row["agreement"] == agreement]
    assert len(matches) == 1
    return matches[0]


def verify_record(record: dict[str, Any]) -> None:
    expected = build_expected_record()
    assert record == expected

    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert int(record["field_denominator"]) == 17**32
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert 6 * 2**128 < 17**32 < 7 * 2**128

    certified = record["certified_agreements"]
    assert len(certified) == 129
    assert certified[0]["agreement"] == 512
    assert certified[-1]["agreement"] == 384
    for row in certified:
        assert row["lambda_exact"] == 1
        assert row["status"] == "PROOF_RECORD"
        assert row["clears_gate_proved"] is False

    descent = record["descent_agreements"]
    assert descent[0]["agreement"] == 383
    assert descent[-1]["agreement"] == 291
    assert record["first_possible_clear_agreement_by_packing"] == 372
    assert record["first_proved_clear_agreement_by_root_pencil"] == 291
    assert record["route_cut_interval_by_packing"] == {
        "descending_from": 383,
        "descending_to": 373,
        "status": "Lambda_mu_upper_bound_at_most_6",
    }
    assert record["open_partial_interval"] == {
        "descending_from": 372,
        "descending_to": 292,
        "status": "packing_permits_seven_but_root_pencil_lower_below_gate",
    }

    row383 = row_by_agreement(descent, 383)
    assert row383["status"] == "ROUTE_CUT"
    assert row383["lambda_lower"] == 2
    assert row383["lambda_upper"] == 6
    assert row383["clears_gate_proved"] is False
    assert row383["clears_gate_possible"] is False
    assert row383["packing_test"]["gate_witness_count_impossible"] is True

    row373 = row_by_agreement(descent, 373)
    assert row373["status"] == "ROUTE_CUT"
    assert row373["lambda_upper"] == 6
    assert row373["packing_test"]["total_support_incidence_lower"] == 2611
    assert row373["packing_test"]["pair_overlap_lower_by_convexity"] == 5375
    assert row373["packing_test"]["pair_overlap_budget_from_pairwise_bound"] == 5355

    row372 = row_by_agreement(descent, 372)
    assert row372["status"] == "PARTIAL"
    assert row372["lambda_lower"] == 2
    assert row372["lambda_upper"] is None
    assert row372["clears_gate_possible"] is True
    assert row372["clears_gate_proved"] is False
    assert row372["packing_test"]["total_support_incidence_lower"] == 2604
    assert row372["packing_test"]["pair_overlap_lower_by_convexity"] == 5340
    assert row372["packing_test"]["pair_overlap_budget_from_pairwise_bound"] == 5355

    row292 = row_by_agreement(descent, 292)
    assert row292["status"] == "PARTIAL"
    assert row292["lambda_lower"] == 6
    assert row292["clears_gate_proved"] is False

    row291 = row_by_agreement(descent, 291)
    assert row291["status"] == "LOWER_ONLY"
    assert row291["lambda_lower"] == 7
    assert row291["clears_gate_proved"] is True
    assert row291["clears_gate_possible"] is True
    assert row291["root_pencil_witness"]["extra_positions_needed_per_witness"] == 36
    assert row291["root_pencil_witness"]["complement_size"] == 257
    assert record["proved_clear_row"] == row291
    assert record["status"] == "THRESHOLD_DESCENT_LOWER_ONLY_CLEAR_AT_291"

    for row in descent:
        assert row["mca_counted"] is False
        if row["status"] == "ROUTE_CUT":
            assert row["lambda_upper"] == 6
            assert row["clears_gate_possible"] is False
        if row["status"] == "PARTIAL":
            assert row["lambda_lower"] <= 6
            assert row["clears_gate_possible"] is True
            assert row["clears_gate_proved"] is False


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
        print("packing route cut: 373 <= a <= 383")
        print("first packing-possible clear: a=372")
        print("first root-pencil proved clear: a=291")


if __name__ == "__main__":
    main()
