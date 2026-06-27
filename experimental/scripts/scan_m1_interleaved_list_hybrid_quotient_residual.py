#!/usr/bin/env python3
"""Emit the M1 hybrid quotient-residual interleaved-list certificate.

The construction starts from the 32 quotient-fiber witnesses for the
`x -> x^32` packet and schedules received-word values inside quotient fibers.
It proves a list-track lower bound at agreement 326.  It does not count as MCA
`N_bad`.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any


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
SCHEDULE_BY_QUOTIENT = {
    0: {0: 7, 11: 7, 7: 6, 14: 6, 2: 6},
    1: {8: 32},
    2: {13: 32},
    3: {2: 32},
    4: {16: 32},
    5: {9: 32},
    6: {4: 32},
    7: {15: 32},
    8: {1: 32},
    9: {8: 32},
    10: {13: 32},
    11: {2: 32},
    12: {16: 32},
    13: {9: 32},
    14: {4: 32},
    15: {15: 32},
}


def q_field() -> int:
    return P**FIELD_DEGREE


def threshold_floor() -> int:
    return q_field() // (2**TARGET_BITS)


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def json_schedule() -> dict[str, dict[str, int]]:
    return {
        str(qidx): {str(value): multiplicity for value, multiplicity in schedule.items()}
        for qidx, schedule in SCHEDULE_BY_QUOTIENT.items()
    }


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
        # The received quotient word is Y^10.  Since the Y^9 and Y^8
        # coefficients vanish, Y^10 - L_A(Y) has quotient degree at most 7.
        remainder = [(-locator[idx]) % P for idx in range(8)]
        witnesses.append(
            {
                "witness_id": len(witnesses),
                "quotient_indices": list(indices),
                "remainder_coefficients_low_to_high": remainder,
            }
        )
    return witnesses


def value_class_masks(witnesses: list[dict[str, Any]]) -> tuple[list[list[int]], list[int]]:
    values = quotient_values()
    classes: list[list[int]] = []
    u_masks: list[int] = []
    for qidx, qvalue in enumerate(values):
        by_value: dict[int, int] = {}
        for witness in witnesses:
            value = eval_poly(witness["remainder_coefficients_low_to_high"], qvalue)
            by_value[value] = by_value.get(value, 0) | (1 << witness["witness_id"])
        classes.append(list(by_value.values()))
        u_value = pow(qvalue, QUOTIENT_SUBSET_SIZE, P)
        u_masks.append(by_value[u_value])
    return classes, u_masks


def selected_schedule_counts(witnesses: list[dict[str, Any]]) -> list[int]:
    selected = list(SELECTED_WITNESS_IDS)
    selected_index = {witness_id: idx for idx, witness_id in enumerate(selected)}
    values = quotient_values()
    counts = [0] * len(selected)
    for qidx, schedule in SCHEDULE_BY_QUOTIENT.items():
        qvalue = values[qidx]
        for value, multiplicity in schedule.items():
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
    for subset in itertools.combinations(range(len(quotient_witnesses())), GATE_NUMERATOR):
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


def build_result() -> dict[str, Any]:
    witnesses = quotient_witnesses()
    assert len(witnesses) == 32
    classes, _u_masks = value_class_masks(witnesses)
    counts = selected_schedule_counts(witnesses)
    candidate_agreement = min(counts)
    max_total, max_total_subset = max_total_agreement_upper(classes)
    upper_for_min_agreement = max_total // GATE_NUMERATOR
    assert candidate_agreement == 326
    assert upper_for_min_agreement == 329
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
        "quotient_core": {
            "map": "x -> x^32",
            "fiber_size": FIBER_SIZE,
            "quotient_size": QUOTIENT_SIZE,
            "base_agreement": FIBER_SIZE * QUOTIENT_SUBSET_SIZE,
            "quotient_subset_size": QUOTIENT_SUBSET_SIZE,
            "available_witnesses": len(witnesses),
        },
        "hybrid_certificate": {
            "selected_witness_ids": list(SELECTED_WITNESS_IDS),
            "selected_quotient_indices": [
                witnesses[witness_id]["quotient_indices"]
                for witness_id in SELECTED_WITNESS_IDS
            ],
            "schedule_by_quotient_value": json_schedule(),
            "agreement_counts": counts,
            "candidate_agreement": candidate_agreement,
            "lambda_lower": GATE_NUMERATOR,
            "clears_gate": candidate_agreement >= 321
            and GATE_NUMERATOR > threshold_floor(),
            "received_word_hash": hash_payload(json_schedule()),
            "witness_set_hash": hash_payload(
                [
                    witnesses[witness_id]["quotient_indices"]
                    for witness_id in SELECTED_WITNESS_IDS
                ]
            ),
            "construction": "hybrid_quotient_residual_value_class_schedule",
            "mca_counted": False,
        },
        "quotient_packet_upper_bound": {
            "max_total_agreement_over_any_7_witnesses": max_total,
            "max_total_subset": list(max_total_subset),
            "upper_bound_for_min_agreement": upper_for_min_agreement,
            "rules_out_agreement_at_least": upper_for_min_agreement + 1,
            "route_cut_interval_within_this_packet": {
                "from": upper_for_min_agreement + 1,
                "to": 372,
            },
        },
        "open_interval_after_hybrid": {
            "from": candidate_agreement + 1,
            "to": upper_for_min_agreement,
            "status": "open_within_this_quotient_packet",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_interleaved_list_hybrid_quotient_residual.sage",
            "explicit_received_word_and_witnesses": True,
        },
        "status": "HYBRID_QUOTIENT_RESIDUAL_CLEAR_AT_A326",
        "non_claims": [
            "not_mca_n_bad",
            "not_protocol_soundness",
            "not_ordinary_list_decoding_failure",
            "not_exact_lambda_mu_at_326",
            "not_exact_delta_star_C",
            "not_exhausting_non_quotient_or_other_hybrid_families",
        ],
    }
    result["record_hash"] = hash_payload(
        {
            "hybrid": result["hybrid_certificate"],
            "upper": result["quotient_packet_upper_bound"],
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
        default="experimental/data/m1_interleaved_list_hybrid_quotient_residual.json",
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
        print("hybrid quotient-residual row: a=326, lambda_lower=7")
        print("same quotient packet cannot reach a>=330 by total value-class upper bound")


if __name__ == "__main__":
    main()
