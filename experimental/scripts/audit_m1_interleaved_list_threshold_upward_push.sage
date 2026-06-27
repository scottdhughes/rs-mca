#!/usr/bin/env sage
"""Sage audit for the M1 interleaved-list threshold upward push.

This independently verifies the quotient-fiber lower bound at agreement
a=320 for RS[F_17^32,H,256].
"""

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
TARGET_BITS = 128
FIBER_SIZE = 32
QUOTIENT_SIZE = 16
QUOTIENT_SUBSET_SIZE = 10
AGREEMENT = FIBER_SIZE * QUOTIENT_SUBSET_SIZE


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

    quotient_generator = subgroup_generator**FIBER_SIZE
    quotient_values = [quotient_generator**idx for idx in range(QUOTIENT_SIZE)]
    assert len(set(quotient_values)) == QUOTIENT_SIZE
    assert all(value**P == value for value in quotient_values)

    quotient_dimension = ceil(K / FIBER_SIZE)
    sigma = QUOTIENT_SUBSET_SIZE - quotient_dimension
    assert quotient_dimension == 8
    assert sigma == 2

    # Work with quotient locators in Y first:
    # L_A(Y)=prod_{y in A}(Y-y)=Y^10+lambda_9 Y^9+...+lambda_0.
    fibers = {}
    RY = PolynomialRing(field, "Y")
    Y = RY.gen()
    for indices in itertools.combinations(range(QUOTIENT_SIZE), QUOTIENT_SUBSET_SIZE):
        poly = RY(1)
        for idx in indices:
            poly *= Y - quotient_values[idx]
        coeffs = poly.list()
        key = (coeffs[8], coeffs[9])
        fibers.setdefault(key, []).append(indices)
    best_key, best_fiber = max(
        fibers.items(),
        key=lambda item: (len(item[1]), tuple(str(value) for value in item[0])),
    )
    assert len(best_fiber) >= 28

    RX = PolynomialRing(field, "X")
    X = RX.gen()
    h8, h9 = best_key
    received_poly = X**AGREEMENT + h8 * X**(FIBER_SIZE * 8) + h9 * X**(FIBER_SIZE * 9)

    witness_descriptors = []
    supports_payload = []
    for witness_index, indices in enumerate(best_fiber):
        locator = RX(1)
        active_quotient_values = {quotient_values[idx] for idx in indices}
        for idx in indices:
            locator *= X**FIBER_SIZE - quotient_values[idx]
        remainder = received_poly % locator
        assert remainder.degree() < K
        support = [
            pos
            for pos, point in enumerate(H)
            if point**FIBER_SIZE in active_quotient_values
        ]
        assert len(support) == AGREEMENT
        for pos in support:
            point = H[pos]
            assert remainder(point) == received_poly(point)
        supports_payload.append(support)
        witness_descriptors.append(
            {
                "witness": witness_index,
                "quotient_indices": list(indices),
                "agreement": len(support),
                "degree": remainder.degree(),
                "support_hash": hash_payload(support),
                "coefficient_hash": coeff_hash(remainder),
            }
        )

    coefficient_hashes = [descriptor["coefficient_hash"] for descriptor in witness_descriptors]
    assert len(set(coefficient_hashes)) == len(coefficient_hashes)
    support_hashes = [descriptor["support_hash"] for descriptor in witness_descriptors]
    assert len(set(support_hashes)) == len(support_hashes)

    result = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "field_denominator": str(q),
        "field_denominator_label": "17^32",
        "subgroup_order": len(H),
        "k": K,
        "quotient_map": "x -> x^32",
        "fiber_size": FIBER_SIZE,
        "quotient_size": QUOTIENT_SIZE,
        "quotient_subset_size": QUOTIENT_SUBSET_SIZE,
        "agreement": AGREEMENT,
        "target_bits": TARGET_BITS,
        "threshold_floor": int(q // (2**TARGET_BITS)),
        "minimum_to_clear": int(q // (2**TARGET_BITS) + 1),
        "lambda_lower_from_pigeonhole": len(best_fiber),
        "lambda_lower_from_verified_witnesses": len(witness_descriptors),
        "verified_witness_count": len(witness_descriptors),
        "clears_list_gate": len(witness_descriptors) > int(q // (2**TARGET_BITS)),
        "mca_counted": False,
        "quotient_key": [str(h8), str(h9)],
        "best_fiber_size": len(best_fiber),
        "expected_floor": ceil(binomial(QUOTIENT_SIZE, QUOTIENT_SUBSET_SIZE) / (P**sigma)),
        "witness_descriptors": witness_descriptors,
        "witness_descriptors_hash": hash_payload(witness_descriptors),
        "agreement_supports_hash": hash_payload(supports_payload),
        "status": "PROOF_RECORD_LOWER_BOUND_A320",
        "non_claims": [
            "not_mca_n_bad",
            "not_protocol_soundness",
            "not_ordinary_list_decoding_failure",
            "not_exact_lambda_mu_at_320",
            "not_exact_delta_star_C",
        ],
    }
    assert result["threshold_floor"] == 6
    assert result["minimum_to_clear"] == 7
    assert result["best_fiber_size"] >= result["expected_floor"] >= 28
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
        print("Sage reconstructed GF(17^32), subgroup order 512, and quotient x -> x^32")
        print("Lambda_mu(C,320) >= 28 by quotient-fiber pigeonhole")
        print(f"Verified {result['verified_witness_count']} explicit witnesses at agreement 320")
        print("MCA counted: false")
        print(f"witness_descriptors_hash: {result['witness_descriptors_hash']}")


if __name__ == "__main__":
    main()
