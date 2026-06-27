#!/usr/bin/env sage
"""Sage audit for the M1 hybrid quotient-residual certificate."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from numbers import Integral


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
FIBER_SIZE = 32
QUOTIENT_SIZE = 16
QUOTIENT_SUBSET_SIZE = 10
TARGET_BITS = 128
PRIMITIVE_ROOT_MOD_17 = 3
SELECTED_QUOTIENT_INDICES = [
    [1, 2, 4, 5, 8, 9, 10, 11, 12, 15],
    [1, 2, 5, 6, 7, 8, 9, 12, 14, 15],
    [1, 3, 4, 6, 7, 10, 11, 12, 13, 14],
    [1, 3, 5, 7, 8, 9, 10, 12, 13, 14],
    [2, 3, 4, 5, 6, 9, 11, 12, 14, 15],
    [2, 4, 5, 7, 8, 11, 12, 13, 14, 15],
    [2, 4, 6, 8, 9, 10, 11, 13, 14, 15],
]
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


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def hash_payload(payload) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def coeff_hash(poly) -> str:
    return hash_payload([str(coeff) for coeff in poly.list()])


def build_audit():
    q = P**FIELD_DEGREE
    field = GF(q, name="z")
    generator = field.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1

    quotient_values = [field(PRIMITIVE_ROOT_MOD_17) ** idx for idx in range(QUOTIENT_SIZE)]
    assert len(set(quotient_values)) == QUOTIENT_SIZE
    assert all(value**P == value for value in quotient_values)

    RX = PolynomialRing(field, "X")
    X = RX.gen()
    received_quotient_word = X**(FIBER_SIZE * QUOTIENT_SUBSET_SIZE)
    codewords = []
    descriptors = []
    for witness_index, indices in enumerate(SELECTED_QUOTIENT_INDICES):
        locator = RX(1)
        for idx in indices:
            locator *= X**FIBER_SIZE - quotient_values[idx]
        remainder = received_quotient_word % locator
        assert remainder.degree() < K
        codewords.append(remainder)
        descriptors.append(
            {
                "witness": witness_index,
                "quotient_indices": indices,
                "degree": int(remainder.degree()),
                "coefficient_hash": coeff_hash(remainder),
            }
        )

    # Build an explicit received word on H.  Within each quotient fiber, assign
    # the first scheduled block of points to the first value, then continue.
    received_values = {}
    for qidx, schedule in SCHEDULE_BY_QUOTIENT.items():
        active_points = [
            point for point in H if point**FIBER_SIZE == quotient_values[qidx]
        ]
        assert len(active_points) == FIBER_SIZE
        cursor = 0
        for value, multiplicity in schedule.items():
            for point in active_points[cursor : cursor + multiplicity]:
                received_values[point] = field(value)
            cursor += multiplicity
        assert cursor == FIBER_SIZE
    assert len(received_values) == N

    agreement_counts = []
    agreement_hash_payload = []
    for witness_index, codeword in enumerate(codewords):
        support_positions = []
        for pos, point in enumerate(H):
            if codeword(point) == received_values[point]:
                support_positions.append(pos)
        agreement_counts.append(len(support_positions))
        agreement_hash_payload.append(support_positions)
    assert agreement_counts == [327, 327, 327, 326, 326, 326, 327]
    assert min(agreement_counts) == 326

    result = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "field_denominator": str(q),
        "field_denominator_label": "17^32",
        "subgroup_order": len(H),
        "k": K,
        "quotient_core": "x -> x^32",
        "selected_witness_count": len(codewords),
        "candidate_agreement": min(agreement_counts),
        "agreement_counts": agreement_counts,
        "lambda_lower": len(codewords),
        "threshold_floor": int(q // (2**TARGET_BITS)),
        "minimum_to_clear": int(q // (2**TARGET_BITS) + 1),
        "clears_list_gate": len(codewords) > int(q // (2**TARGET_BITS)),
        "mca_counted": False,
        "witness_descriptors": descriptors,
        "witness_descriptors_hash": hash_payload(descriptors),
        "received_word_hash": hash_payload(
            {
                "schedule_by_quotient": SCHEDULE_BY_QUOTIENT,
                "primitive_root_mod_17": PRIMITIVE_ROOT_MOD_17,
            }
        ),
        "agreement_supports_hash": hash_payload(agreement_hash_payload),
        "status": "SAGE_AUDIT_HYBRID_QUOTIENT_RESIDUAL_CLEAR_AT_A326",
        "non_claims": [
            "not_mca_n_bad",
            "not_protocol_soundness",
            "not_ordinary_list_decoding_failure",
            "not_exact_lambda_mu_at_326",
            "not_exact_delta_star_C",
        ],
    }
    assert result["threshold_floor"] == 6
    assert result["minimum_to_clear"] == 7
    assert result["clears_list_gate"] is True
    return jsonable(result)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_audit()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("Sage reconstructed GF(17^32), H, seven codewords, and the received word")
        print("hybrid quotient-residual row clears at a=326")
        print(f"agreement_counts: {result['agreement_counts']}")
        print(f"witness_descriptors_hash: {result['witness_descriptors_hash']}")


if __name__ == "__main__":
    main()
