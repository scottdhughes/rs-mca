#!/usr/bin/env python3
"""Verify the M1 hybrid quotient-residual certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_interleaved_list_hybrid_quotient_residual.json")
P = 17
N = 512
K = 256
FIELD_DEGREE = 32
TARGET_BITS = 128
FIBER_SIZE = 32
QUOTIENT_SIZE = 16
QUOTIENT_SUBSET_SIZE = 10
GATE_NUMERATOR = 7
PRIMITIVE_ROOT_MOD_17 = 3
SELECTED_WITNESS_IDS = (23, 24, 26, 28, 29, 30, 31)


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def quotient_values() -> list[int]:
    return [pow(PRIMITIVE_ROOT_MOD_17, idx, P) for idx in range(QUOTIENT_SIZE)]


def multiply_by_linear(poly: list[int], root: int) -> list[int]:
    result = [0] * (len(poly) + 1)
    for idx, coeff in enumerate(poly):
        result[idx] = (result[idx] - coeff * root) % P
        result[idx + 1] = (result[idx + 1] + coeff) % P
    return result


def quotient_locator(indices: tuple[int, ...]) -> list[int]:
    values = quotient_values()
    poly = [1]
    for idx in indices:
        poly = multiply_by_linear(poly, values[idx])
    return poly


def eval_poly(poly: list[int], value: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % P
        power = (power * value) % P
    return total


def quotient_witnesses() -> list[dict[str, Any]]:
    witnesses = []
    for indices in itertools.combinations(range(QUOTIENT_SIZE), QUOTIENT_SUBSET_SIZE):
        locator = quotient_locator(indices)
        if locator[9] % P != 0 or locator[8] % P != 0:
            continue
        witnesses.append(
            {
                "witness_id": len(witnesses),
                "quotient_indices": list(indices),
                "remainder_coefficients_low_to_high": [
                    (-locator[idx]) % P for idx in range(8)
                ],
            }
        )
    return witnesses


def value_class_masks(witnesses: list[dict[str, Any]]) -> list[list[int]]:
    classes = []
    for qvalue in quotient_values():
        by_value: dict[int, int] = {}
        for witness in witnesses:
            value = eval_poly(witness["remainder_coefficients_low_to_high"], qvalue)
            by_value[value] = by_value.get(value, 0) | (1 << witness["witness_id"])
        classes.append(list(by_value.values()))
    return classes


def selected_schedule_counts(
    witnesses: list[dict[str, Any]], schedule: dict[str, dict[str, int]]
) -> list[int]:
    selected = list(SELECTED_WITNESS_IDS)
    selected_index = {witness_id: idx for idx, witness_id in enumerate(selected)}
    values = quotient_values()
    counts = [0] * len(selected)
    for qidx_text, value_schedule in schedule.items():
        qvalue = values[int(qidx_text)]
        for value_text, multiplicity in value_schedule.items():
            value = int(value_text)
            for witness_id in selected:
                witness = witnesses[witness_id]
                witness_value = eval_poly(
                    witness["remainder_coefficients_low_to_high"], qvalue
                )
                if witness_value == value:
                    counts[selected_index[witness_id]] += multiplicity
    return counts


def max_total_agreement_upper(classes: list[list[int]]) -> tuple[int, tuple[int, ...]]:
    best_total = -1
    best_subset: tuple[int, ...] | None = None
    for subset in itertools.combinations(range(32), GATE_NUMERATOR):
        mask = sum(1 << witness_id for witness_id in subset)
        quotient_total = 0
        for class_masks in classes:
            quotient_total += max((class_mask & mask).bit_count() for class_mask in class_masks)
        total = FIBER_SIZE * quotient_total
        if total > best_total:
            best_total = total
            best_subset = subset
    assert best_subset is not None
    return best_total, best_subset


def verify_record(record: dict[str, Any]) -> None:
    witnesses = quotient_witnesses()
    assert len(witnesses) == 32
    classes = value_class_masks(witnesses)

    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert int(record["field_denominator"]) == 17**32
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert 6 * 2**128 < 17**32 < 7 * 2**128

    core = record["quotient_core"]
    assert core["map"] == "x -> x^32"
    assert core["fiber_size"] == 32
    assert core["quotient_size"] == 16
    assert core["base_agreement"] == 320
    assert core["available_witnesses"] == 32

    cert = record["hybrid_certificate"]
    assert cert["selected_witness_ids"] == [23, 24, 26, 28, 29, 30, 31]
    assert cert["selected_quotient_indices"] == [
        witnesses[witness_id]["quotient_indices"] for witness_id in SELECTED_WITNESS_IDS
    ]
    recomputed_counts = selected_schedule_counts(
        witnesses, cert["schedule_by_quotient_value"]
    )
    assert recomputed_counts == cert["agreement_counts"]
    assert cert["agreement_counts"] == [327, 327, 327, 326, 326, 326, 327]
    assert cert["candidate_agreement"] == 326
    assert cert["lambda_lower"] == 7
    assert cert["clears_gate"] is True
    assert cert["mca_counted"] is False
    for schedule in cert["schedule_by_quotient_value"].values():
        assert sum(schedule.values()) == 32

    max_total, max_total_subset = max_total_agreement_upper(classes)
    upper = record["quotient_packet_upper_bound"]
    assert max_total == upper["max_total_agreement_over_any_7_witnesses"]
    assert list(max_total_subset) == upper["max_total_subset"]
    assert upper["max_total_agreement_over_any_7_witnesses"] == 2304
    assert upper["upper_bound_for_min_agreement"] == 329
    assert upper["rules_out_agreement_at_least"] == 330
    assert upper["route_cut_interval_within_this_packet"] == {"from": 330, "to": 372}

    assert record["open_interval_after_hybrid"] == {
        "from": 327,
        "to": 329,
        "status": "open_within_this_quotient_packet",
    }
    assert "not_mca_n_bad" in record["non_claims"]
    assert "not_exhausting_non_quotient_or_other_hybrid_families" in record["non_claims"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    record = json.loads(DATA_PATH.read_text())
    verify_record(record)
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("hybrid quotient-residual row clears at a=326")
        print("same quotient packet cannot reach a>=330")


if __name__ == "__main__":
    main()
