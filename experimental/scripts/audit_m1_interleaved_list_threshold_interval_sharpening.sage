#!/usr/bin/env sage
"""Sage audit for the M1 interleaved-list threshold interval sharpening.

This independently builds explicit finite-field witnesses for
Lambda_mu(C,292) >= 7 in the row RS[F_17^32,H,256].
"""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_BITS = 128
AGREEMENT = 292
WITNESS_COUNT = 7
COMMON_ROOT_SIZE = K - 2


def encode_field_element(value) -> str:
    return str(value)


def hash_payload(payload) -> str:
    encoded = json.dumps(
        jsonable(payload), sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


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


def poly_eval(coeffs, x):
    total = x.parent()(0)
    power = x.parent()(1)
    for coeff in coeffs:
        total += coeff * power
        power *= x
    return total


def poly_mul_linear(poly, root):
    field = root.parent()
    out = [field(0)] * (len(poly) + 1)
    for idx, coeff in enumerate(poly):
        out[idx] -= coeff * root
        out[idx + 1] += coeff
    return out


def root_polynomial(points, field):
    poly = [field(1)]
    for point in points:
        poly = poly_mul_linear(poly, point)
    return poly


def scalar_mul(poly, scalar):
    return [scalar * coeff for coeff in poly]


def poly_add(left, right):
    field = left[0].parent() if left else right[0].parent()
    width = max(len(left), len(right))
    out = [field(0)] * width
    for idx, coeff in enumerate(left):
        out[idx] += coeff
    for idx, coeff in enumerate(right):
        out[idx] += coeff
    return out


def poly_mul(left, right, field):
    out = [field(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def build_audit():
    q = P**FIELD_DEGREE
    field = GF(q, name="z")
    z = field.gen()
    generator = field.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1

    common_roots = H[:COMMON_ROOT_SIZE]
    complement = H[COMMON_ROOT_SIZE:]
    assert len(complement) == N - COMMON_ROOT_SIZE == 258

    # Eight controlled overlap points.  The first six define star overlaps with
    # witness 0; y12 and y34 add two off-star overlaps.
    x1, x2, x3, x4, x5, x6, y12, y34 = complement[:8]
    unique_pool = complement[8:]
    assert len(unique_pool) == 250

    root_poly = root_polynomial(common_roots, field)
    assert len(root_poly) - 1 == COMMON_ROOT_SIZE

    residuals = [
        [field(0)],
        [-x1, field(1)],
        [-(y12 - x1) * x2 / (y12 - x2), (y12 - x1) / (y12 - x2)],
        [-x3, field(1)],
        [-(y34 - x3) * x4 / (y34 - x4), (y34 - x3) / (y34 - x4)],
        [-x5, field(1)],
        [-x6, field(1)],
    ]
    residuals = [trim(poly) for poly in residuals]
    assert len({tuple(poly) for poly in residuals}) == WITNESS_COUNT

    codewords = [trim(poly_mul(root_poly, residual, field)) for residual in residuals]
    assert len({tuple(poly) for poly in codewords}) == WITNESS_COUNT
    assert max(len(poly) - 1 for poly in codewords) == K - 1
    assert all(len(poly) - 1 < K for poly in codewords)

    supports = [set(range(COMMON_ROOT_SIZE)) for _ in range(WITNESS_COUNT)]
    controlled = [
        (COMMON_ROOT_SIZE + 0, [0, 1]),
        (COMMON_ROOT_SIZE + 1, [0, 2]),
        (COMMON_ROOT_SIZE + 2, [0, 3]),
        (COMMON_ROOT_SIZE + 3, [0, 4]),
        (COMMON_ROOT_SIZE + 4, [0, 5]),
        (COMMON_ROOT_SIZE + 5, [0, 6]),
        (COMMON_ROOT_SIZE + 6, [1, 2]),
        (COMMON_ROOT_SIZE + 7, [3, 4]),
    ]

    received = {}
    for pos in range(COMMON_ROOT_SIZE):
        received[pos] = field(0)
    for pos, active in controlled:
        values = [poly_eval(codewords[idx], H[pos]) for idx in active]
        assert len(set(values)) == 1
        received[pos] = values[0]
        for idx in active:
            supports[idx].add(pos)

    unique_needed = [AGREEMENT - len(support) for support in supports]
    assert unique_needed == [32, 36, 36, 36, 36, 37, 37]
    cursor = 0
    for idx, needed in enumerate(unique_needed):
        block = list(range(COMMON_ROOT_SIZE + 8 + cursor, COMMON_ROOT_SIZE + 8 + cursor + needed))
        cursor += needed
        for pos in block:
            value = poly_eval(codewords[idx], H[pos])
            received[pos] = value
            supports[idx].add(pos)
    assert cursor == len(unique_pool) == 250
    assert len(received) == N

    # Fill any unassigned position defensively.  In this construction all
    # complement points are assigned by the controlled+unique support partition.
    for pos in range(N):
        received.setdefault(pos, field(0))

    agreements = []
    agreement_hash_payload = []
    for idx, codeword in enumerate(codewords):
        agree = [
            pos
            for pos, point in enumerate(H)
            if poly_eval(codeword, point) == received[pos]
        ]
        assert set(agree) == supports[idx]
        assert len(agree) == AGREEMENT
        agreements.append(len(agree))
        agreement_hash_payload.append(agree)

    support_intersections = []
    for i in range(WITNESS_COUNT):
        for j in range(i + 1, WITNESS_COUNT):
            support_intersections.append(
                {
                    "i": i,
                    "j": j,
                    "intersection_size": len(supports[i] & supports[j]),
                }
            )
            assert len(supports[i] & supports[j]) <= K - 1

    witness_descriptors = [
        {
            "witness": idx,
            "degree": int(len(codeword) - 1),
            "agreement": int(agreements[idx]),
            "support_hash": hash_payload([int(pos) for pos in sorted(supports[idx])]),
            "coefficient_hash": hash_payload([encode_field_element(c) for c in codeword]),
        }
        for idx, codeword in enumerate(codewords)
    ]

    result = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "field_denominator": str(q),
        "field_denominator_label": "17^32",
        "subgroup_order": len(H),
        "k": K,
        "agreement": AGREEMENT,
        "target_bits": TARGET_BITS,
        "threshold_floor": int(q // (2**TARGET_BITS)),
        "minimum_to_clear": int(q // (2**TARGET_BITS) + 1),
        "lambda_lower": WITNESS_COUNT,
        "clears_list_gate": WITNESS_COUNT > int(q // (2**TARGET_BITS)),
        "mca_counted": False,
        "common_root_size": COMMON_ROOT_SIZE,
        "controlled_overlap_point_count": len(controlled),
        "unique_pool_size": len(unique_pool),
        "unique_needed_by_witness": [int(value) for value in unique_needed],
        "agreements": [int(value) for value in agreements],
        "witness_descriptors": witness_descriptors,
        "witness_descriptors_hash": hash_payload(witness_descriptors),
        "agreement_supports_hash": hash_payload(agreement_hash_payload),
        "support_intersections": support_intersections,
        "status": "PROOF_RECORD_LOWER_BOUND_A292",
        "non_claims": [
            "not_mca_n_bad",
            "not_protocol_soundness",
            "not_ordinary_list_decoding_failure",
            "not_exact_lambda_mu_at_292",
            "not_exact_delta_star_C",
        ],
    }
    assert result["threshold_floor"] == 6
    assert result["minimum_to_clear"] == 7
    assert result["clears_list_gate"] is True
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_audit()
    if args.json:
        print(json.dumps(jsonable(result), indent=2, sort_keys=True))
    else:
        print("PASS")
        print("Sage reconstructed GF(17^32), subgroup order 512, and a=292 witnesses")
        print("Lambda_mu(C,292) >= 7 for the standard interleaved-list predicate")
        print("MCA counted: false")
        print(f"witness_descriptors_hash: {result['witness_descriptors_hash']}")


if __name__ == "__main__":
    main()
