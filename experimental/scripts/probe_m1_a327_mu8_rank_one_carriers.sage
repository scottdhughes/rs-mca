#!/usr/bin/env sage
"""Probe rank-one carrier lines for M1 a=327 mu_8 schedules."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
H_ORDER = 512
MU_ORDER = 8
QUOTIENT_ORDER = 64
QUOTIENT_DEGREE_BOUND = 32
DEGREE_BOUND = 256
TARGET_AGREEMENT = 327

SCAN_DATA = Path("experimental/data/m1_a327_mu8_block_rank_feedback_scan.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_mu8_rank_one_carrier_probe.json")


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
    return str(payload)


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def exact_field():
    return GF(Integer(P) ** FIELD_DEGREE, name="z")


def load_scan():
    with SCAN_DATA.open() as handle:
        return json.load(handle)


def point_functional_rows(F, omega, gamma, patterns, qidx):
    rep = omega ** qidx
    subset = patterns[qidx % len(patterns)]
    anchor = min(subset)
    rows = []
    for selected in subset:
        if selected == anchor:
            continue
        rows.append([
            (gamma ** (selected * residue) - gamma ** (anchor * residue)) * (rep ** residue)
            for residue in range(1, MU_ORDER)
        ])
    return rows


def all_matrix_rows(F, omega, gamma, patterns):
    rows = []
    for qidx in range(QUOTIENT_ORDER):
        rep = omega ** qidx
        subset = patterns[qidx % len(patterns)]
        anchor = min(subset)
        for selected in subset:
            if selected == anchor:
                continue
            row = []
            for residue in range(1, MU_ORDER):
                factor = (gamma ** (selected * residue) - gamma ** (anchor * residue)) * (rep ** residue)
                for power in range(QUOTIENT_DEGREE_BOUND):
                    y = rep ** MU_ORDER
                    row.append(factor * (y ** power))
            rows.append(row)
    return rows


def subspace_key(subspace):
    mat = subspace.basis_matrix().echelon_form()
    return hash_payload([[str(value) for value in row] for row in mat.rows()])


def odd_residue_support(vector):
    return any(vector[residue - 1] != 0 for residue in [1, 3, 5, 7])


def carrier_coverage(vector, allowed_subspaces):
    count = 0
    for subspace in allowed_subspaces:
        if vector in subspace:
            count += 1
    return count


def vector_support(vector):
    return [idx + 1 for idx, value in enumerate(vector) if value != 0]


def candidate_vectors_from_subspace(subspace, max_vectors):
    basis = list(subspace.basis())
    vectors = []
    for vec in basis:
        vectors.append(vec)
    for left in range(len(basis)):
        for right in range(left + 1, len(basis)):
            vectors.append(basis[left] + basis[right])
            vectors.append(basis[left] - basis[right])
            if len(vectors) >= max_vectors:
                return vectors
    if len(basis) >= 3 and len(vectors) < max_vectors:
        vectors.append(basis[0] + basis[1] + basis[2])
    return vectors[:max_vectors]


def enumerate_intersections(F, allowed_subspaces, max_subspaces):
    V = VectorSpace(F, MU_ORDER - 1)
    subspaces = {subspace_key(V): V}
    for allowed in allowed_subspaces:
        additions = {}
        for subspace in list(subspaces.values()):
            intersection = subspace.intersection(allowed)
            if intersection.dimension() <= 0:
                continue
            additions[subspace_key(intersection)] = intersection
        subspaces.update(additions)
        if len(subspaces) > max_subspaces:
            # Keep the smallest-dimensional spaces first; lines are the useful carriers.
            ordered = sorted(subspaces.values(), key=lambda row: (row.dimension(), subspace_key(row)))
            subspaces = {subspace_key(row): row for row in ordered[:max_subspaces]}
    return list(subspaces.values())


def construct_vector_from_carrier(F, omega, gamma, patterns, carrier):
    bad = []
    allowed_subspaces = allowed_subspaces_for_schedule(F, omega, gamma, patterns)
    for qidx, subspace in enumerate(allowed_subspaces):
        if carrier not in subspace:
            bad.append(qidx)
    R = PolynomialRing(F, "Y")
    Y = R.gen()
    poly = R(1)
    for qidx in bad:
        rep = omega ** qidx
        poly *= (Y - rep ** MU_ORDER)
    if poly.degree() >= QUOTIENT_DEGREE_BOUND:
        return None
    coeffs = [F(0) for _ in range(QUOTIENT_DEGREE_BOUND)]
    for power, coeff in enumerate(poly.list()):
        coeffs[power] = coeff
    vector = []
    for residue in range(1, MU_ORDER):
        for power in range(QUOTIENT_DEGREE_BOUND):
            vector.append(carrier[residue - 1] * coeffs[power])
    return vector, bad


def p_eval(coeffs, x):
    F = x.parent()
    total = F(0)
    idx = 0
    for residue in range(1, MU_ORDER):
        for power in range(QUOTIENT_DEGREE_BOUND):
            coeff = coeffs[idx]
            if coeff:
                total += coeff * (x ** (residue + MU_ORDER * power))
            idx += 1
    return total


def verify_witness_vector(vector, omega, gamma, patterns):
    points = []
    received = []
    for qidx in range(QUOTIENT_ORDER):
        rep = omega ** qidx
        subset = patterns[qidx % len(patterns)]
        anchor = min(subset)
        common = p_eval(vector, (gamma ** anchor) * rep)
        for residue in range(MU_ORDER):
            points.append((gamma ** residue) * rep)
            received.append(common)
    agreements = []
    for shift in range(7):
        count = 0
        for point, value in zip(points, received, strict=True):
            if p_eval(vector, (gamma ** shift) * point) == value:
                count += 1
        agreements.append(count)
    pair_agreements = {}
    for left in range(7):
        for right in range(left + 1, 7):
            count = 0
            for point in points:
                if p_eval(vector, (gamma ** left) * point) == p_eval(vector, (gamma ** right) * point):
                    count += 1
            pair_agreements["P%d%d" % (left + 1, right + 1)] = count
    return {
        "agreement_vector": agreements,
        "min_agreement": min(agreements),
        "pair_agreement_max": max(pair_agreements.values()),
        "pair_agreements": pair_agreements,
        "seven_distinct": all(value <= DEGREE_BOUND - 1 for value in pair_agreements.values()),
    }


def allowed_subspaces_for_schedule(F, omega, gamma, patterns):
    V = VectorSpace(F, MU_ORDER - 1)
    subspaces = []
    for qidx in range(QUOTIENT_ORDER):
        rows = point_functional_rows(F, omega, gamma, patterns, qidx)
        matrix = Matrix(F, rows)
        subspaces.append(V.subspace(matrix.right_kernel().basis()))
    return subspaces


def probe_schedule(F, omega, gamma, schedule, max_subspaces, max_vectors):
    patterns = schedule["patterns"]
    allowed_subspaces = allowed_subspaces_for_schedule(F, omega, gamma, patterns)
    common = allowed_subspaces[0]
    for subspace in allowed_subspaces[1:]:
        common = common.intersection(subspace)
    candidates = enumerate_intersections(F, allowed_subspaces, max_subspaces=max_subspaces)
    best = None
    best_pair_visible = None
    for subspace in candidates:
        for vector in candidate_vectors_from_subspace(subspace, max_vectors=max_vectors):
            if vector.is_zero():
                continue
            coverage = carrier_coverage(vector, allowed_subspaces)
            row = {
                "coverage": int(coverage),
                "bad_count": int(QUOTIENT_ORDER - coverage),
                "residue_support": vector_support(vector),
                "odd_residue_support": odd_residue_support(vector),
                "carrier_hash": hash_payload([str(value) for value in vector]),
            }
            if best is None or (row["coverage"], row["odd_residue_support"], -len(row["residue_support"])) > (
                best["coverage"],
                best["odd_residue_support"],
                -len(best["residue_support"]),
            ):
                best = row
            if row["odd_residue_support"] and (best_pair_visible is None or row["coverage"] > best_pair_visible["coverage"]):
                best_pair_visible = row
                best_pair_visible_vector = vector
    constructed = None
    if best_pair_visible is not None and best_pair_visible["coverage"] >= 33:
        carrier_vec = None
        # Re-find the vector from its hash to avoid retaining every candidate in JSON.
        target_hash = best_pair_visible["carrier_hash"]
        for subspace in candidates:
            for vector in candidate_vectors_from_subspace(subspace, max_vectors=max_vectors):
                if hash_payload([str(value) for value in vector]) == target_hash:
                    carrier_vec = vector
                    break
            if carrier_vec is not None:
                break
        built = construct_vector_from_carrier(F, omega, gamma, patterns, carrier_vec)
        if built is not None:
            qvector, bad = built
            matrix = Matrix(F, all_matrix_rows(F, omega, gamma, patterns))
            mv = matrix * vector(F, qvector)
            verified = all(value == 0 for value in mv)
            witness = verify_witness_vector(qvector, omega, gamma, patterns)
            constructed = {
                "bad_quotient_points": bad,
                "bad_count": len(bad),
                "kernel_vector_verified_by_matrix": bool(verified),
                "witness_audit": witness,
            }
    status = "MU8_RANK_ONE_NO_PAIR_VISIBLE_CARRIER"
    if best_pair_visible is not None and best_pair_visible["coverage"] >= 33:
        status = "MU8_RANK_ONE_PAIR_VISIBLE_CARRIER_FOUND"
    return {
        "candidate_id": schedule["candidate_id"],
        "source_schedule_id": schedule["source_schedule_id"],
        "patterns_hash": schedule["patterns_hash"],
        "common_kernel_dimension": int(common.dimension()),
        "subspaces_enumerated": len(candidates),
        "best_carrier_coverage": None if best is None else best["coverage"],
        "best_bad_count": None if best is None else best["bad_count"],
        "best_pair_visible_carrier_coverage": None if best_pair_visible is None else best_pair_visible["coverage"],
        "best_pair_visible_bad_count": None if best_pair_visible is None else best_pair_visible["bad_count"],
        "carrier_residue_support": None if best_pair_visible is None else best_pair_visible["residue_support"],
        "odd_residue_support": False if best_pair_visible is None else best_pair_visible["odd_residue_support"],
        "constructs_degree_lt_32_scalar": bool(best_pair_visible is not None and best_pair_visible["bad_count"] <= 31),
        "constructed": constructed,
        "status": status,
    }


def audit(limit, max_subspaces, max_vectors):
    scan = load_scan()
    F = exact_field()
    gen = F.multiplicative_generator()
    omega = gen ** ((F.order() - 1) // H_ORDER)
    gamma = omega ** (H_ORDER // MU_ORDER)
    schedules = scan["candidate_schedules"][:limit]
    rows = [probe_schedule(F, omega, gamma, schedule, max_subspaces=max_subspaces, max_vectors=max_vectors) for schedule in schedules]
    found = [row for row in rows if row["status"] == "MU8_RANK_ONE_PAIR_VISIBLE_CARRIER_FOUND"]
    witness_rows = [
        row for row in found
        if row["constructed"]
        and row["constructed"]["kernel_vector_verified_by_matrix"]
        and row["constructed"]["witness_audit"]["seven_distinct"]
        and row["constructed"]["witness_audit"]["min_agreement"] >= TARGET_AGREEMENT
    ]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "01bc0e3",
        "rank_one_carrier_probe": {
            "field": "GF(17^32)",
            "schedules_planned": len(scan["candidate_schedules"]),
            "schedules_tested": len(rows),
            "max_subspaces": max_subspaces,
            "max_vectors_per_subspace": max_vectors,
            "pair_visible_carriers_found": len(found),
            "exact_witnesses_found": len(witness_rows),
            "best_pair_visible_carrier_coverage": max([row["best_pair_visible_carrier_coverage"] or 0 for row in rows], default=0),
            "best_failure_mode": "MU8_RANK_ONE_PAIR_VISIBLE_CARRIER_FOUND" if found else "MU8_RANK_ONE_NO_PAIR_VISIBLE_CARRIER",
        },
        "schedule_probes": rows,
        "proof_status": (
            "PROOF_RECORD / EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS / EXPERIMENTAL"
            if witness_rows
            else (
                "CANDIDATE / MU8_RANK_ONE_PAIR_VISIBLE_CARRIER_FOUND / PARTIAL / EXPERIMENTAL"
                if found
                else "EXACT_EXTRACTION_NO_A327 / MU8_RANK_ONE_NO_PAIR_VISIBLE_CARRIER / PARTIAL / EXPERIMENTAL"
            )
        ),
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=64)
    parser.add_argument("--max-subspaces", type=int, default=2048)
    parser.add_argument("--max-vectors", type=int, default=32)
    args = parser.parse_args()
    record = audit(limit=args.limit, max_subspaces=args.max_subspaces, max_vectors=args.max_vectors)
    if args.write_json:
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        "schedules_tested": record["rank_one_carrier_probe"]["schedules_tested"],
        "pair_visible_carriers_found": record["rank_one_carrier_probe"]["pair_visible_carriers_found"],
        "exact_witnesses_found": record["rank_one_carrier_probe"]["exact_witnesses_found"],
        "best_pair_visible_carrier_coverage": record["rank_one_carrier_probe"]["best_pair_visible_carrier_coverage"],
        "best_failure_mode": record["rank_one_carrier_probe"]["best_failure_mode"],
    }
    if args.json:
        print(json.dumps(jsonable(summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_PROBE_M1_A327_MU8_RANK_ONE_CARRIERS_READY")


if __name__ == "__main__":
    main()
