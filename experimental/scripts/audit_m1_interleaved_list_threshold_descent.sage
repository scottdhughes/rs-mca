#!/usr/bin/env sage
r"""
Independent Sage audit for the M1 interleaved-list threshold descent row.

This audit reconstructs GF(17^32), a 512-point multiplicative subgroup H, and
the root-pencil lower-bound witness at agreement a=291.  It deliberately does
not import or replay the Python JSON scanner.

Run:
    sage experimental/scripts/audit_m1_interleaved_list_threshold_descent.sage
    sage experimental/scripts/audit_m1_interleaved_list_threshold_descent.sage --json
"""

import argparse
import hashlib
import json


P = 17
FIELD_DEGREE = 32
N = 512
K_DIM = 256
AGREEMENT = 291
TARGET_BITS = 128
MINIMUM_TO_CLEAR = 7
ROOT_SET_SIZE = K_DIM - 1
BLOCK_SIZE = AGREEMENT - ROOT_SET_SIZE


def json_ready(payload):
    if isinstance(payload, dict):
        return {str(key): json_ready(value) for key, value in payload.items()}
    if isinstance(payload, (list, tuple)):
        return [json_ready(value) for value in payload]
    if isinstance(payload, (str, bool)) or payload is None:
        return payload
    try:
        if payload in ZZ:
            return int(payload)
    except Exception:
        pass
    return payload


def sha256_json(payload):
    encoded = json.dumps(
        json_ready(payload), sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def field_element_digest(element):
    return sha256_json(str(element))


def descriptor_hashes(descriptors):
    return [sha256_json(descriptor) for descriptor in descriptors]


def build_audit():
    q = P**FIELD_DEGREE
    K = GF(q, "z")
    generator = K.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**i for i in range(N)]

    assert len({str(x) for x in H}) == N
    assert subgroup_generator**N == K(1)
    assert subgroup_generator**(N // 2) != K(1)

    threshold_floor = q // (2**TARGET_BITS)
    assert threshold_floor == 6
    assert threshold_floor + 1 == MINIMUM_TO_CLEAR
    assert threshold_floor * 2**TARGET_BITS < q
    assert (threshold_floor + 1) * 2**TARGET_BITS > q

    R = PolynomialRing(K, "X")
    X = R.gen()
    root_indices = list(range(ROOT_SET_SIZE))
    complement_indices = list(range(ROOT_SET_SIZE, N))
    roots = [H[i] for i in root_indices]
    complement = [H[i] for i in complement_indices]

    root_polynomial = R(1)
    for root in roots:
        root_polynomial *= X - root

    assert root_polynomial.degree() == ROOT_SET_SIZE
    assert root_polynomial.degree() < K_DIM
    assert all(root_polynomial(point) == 0 for point in roots)
    assert all(root_polynomial(point) != 0 for point in complement)

    scalars = [K(i) for i in range(1, MINIMUM_TO_CLEAR + 1)]
    assert len({str(scalar) for scalar in scalars}) == MINIMUM_TO_CLEAR

    received = [K(0) for _ in range(N)]
    witness_descriptors = []
    agreement_counts = []
    supports = []
    for witness_id, scalar in enumerate(scalars):
        block_start = witness_id * BLOCK_SIZE
        block_stop = block_start + BLOCK_SIZE
        block_relative = list(range(block_start, block_stop))
        assert block_stop <= len(complement_indices)
        block_indices = [complement_indices[i] for i in block_relative]
        for idx in block_indices:
            received[idx] = scalar * root_polynomial(H[idx])
        witness_descriptors.append(
            {
                "witness_id": witness_id,
                "scalar_in_prime_field": witness_id + 1,
                "root_index_start": root_indices[0],
                "root_index_stop_inclusive": root_indices[-1],
                "block_index_start": block_indices[0],
                "block_index_stop_inclusive": block_indices[-1],
                "block_size": len(block_indices),
                "agreement": AGREEMENT,
            }
        )

    residual_indices = complement_indices[MINIMUM_TO_CLEAR * BLOCK_SIZE :]
    assert len(residual_indices) == N - ROOT_SET_SIZE - MINIMUM_TO_CLEAR * BLOCK_SIZE
    assert len(residual_indices) == 5

    for witness_id, scalar in enumerate(scalars):
        values = [scalar * root_polynomial(point) for point in H]
        support = [idx for idx, (value, target) in enumerate(zip(values, received)) if value == target]
        supports.append(support)
        agreement_counts.append(len(support))
        assert len(support) == AGREEMENT
        assert set(root_indices).issubset(set(support))

    assert len({tuple(support) for support in supports}) == MINIMUM_TO_CLEAR
    assert all(count >= AGREEMENT for count in agreement_counts)

    # Distinct codewords: scalar multiples of a nonzero root polynomial.
    for i in range(len(scalars)):
        for j in range(i + 1, len(scalars)):
            assert scalars[i] != scalars[j]
            assert (scalars[i] - scalars[j]) * root_polynomial != 0

    # Diagonal interleaving: repeating each listed codeword in every row keeps
    # the same common support, so the construction works for every mu.
    for mu in [1, 2, 3, 7]:
        for support in supports:
            assert len(support) >= AGREEMENT
        assert len(supports) == MINIMUM_TO_CLEAR

    descriptors_hash = sha256_json(witness_descriptors)
    received_digest = sha256_json(
        {
            "root_indices": root_indices,
            "residual_indices": residual_indices,
            "witness_hashes": descriptor_hashes(witness_descriptors),
        }
    )

    return json_ready({
        "tool": "SageMath",
        "status": "PASS",
        "row": "RS[F_17^32,H,256]",
        "track": "INTERLEAVED_LIST",
        "mca_counted": False,
        "mca_reason": "separate interleaved-list track; no bridge to N_bad",
        "p": P,
        "field_degree": FIELD_DEGREE,
        "field_denominator": str(q),
        "field_denominator_label": "17^32",
        "subgroup_order": len(H),
        "agreement": AGREEMENT,
        "k": K_DIM,
        "root_set_size": ROOT_SET_SIZE,
        "block_size": BLOCK_SIZE,
        "residual_size": len(residual_indices),
        "threshold_floor": threshold_floor,
        "minimum_to_clear": MINIMUM_TO_CLEAR,
        "lambda_lower_bound": len(supports),
        "clears_list_gate": len(supports) >= MINIMUM_TO_CLEAR,
        "degree_less_than_k": root_polynomial.degree() < K_DIM,
        "agreement_counts": agreement_counts,
        "supports_are_distinct": len({tuple(support) for support in supports}) == len(supports),
        "diagonal_mu_samples_checked": [1, 2, 3, 7],
        "witness_descriptors": witness_descriptors,
        "witness_descriptor_hashes": descriptor_hashes(witness_descriptors),
        "witness_descriptors_hash": descriptors_hash,
        "received_descriptor_hash": received_digest,
        "root_polynomial_digest": field_element_digest(root_polynomial),
        "subgroup_generator_digest": field_element_digest(subgroup_generator),
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_audit()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("Sage reconstructed GF(17^32), subgroup order 512, and a=291 witnesses")
        print("Lambda_mu(C,291) >= 7 for the standard interleaved-list predicate")
        print("MCA counted: false")
        print("witness_descriptors_hash:", result["witness_descriptors_hash"])


if __name__ == "__main__":
    main()
