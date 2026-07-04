#!/usr/bin/env sage
"""Exact audit for M1 a=327 mu_8 orbit-invariant construction seeds."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
H_ORDER = 512
MU_ORDER = 8
QUOTIENT_ORDER = 64
DEGREE_BOUND = 256
TARGET_AGREEMENT = 327
OUTPUT_DATA = Path("experimental/data/m1_a327_mu8_orbit_invariant_construction.json")


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


def complement(subset):
    used = set(int(value) % MU_ORDER for value in subset)
    return sorted(value for value in range(MU_ORDER) if value not in used)


def rotate(subset, shift):
    return sorted(((int(value) + int(shift)) % MU_ORDER for value in subset))


def autocorrelation(subset):
    values = {}
    S = set(subset)
    for shift in range(1, MU_ORDER):
        values[shift] = sum(1 for value in S if ((value + shift) % MU_ORDER) in S)
    return values


def schedule_autocorrelation(patterns):
    totals = {shift: 0 for shift in range(1, MU_ORDER)}
    for subset in patterns:
        corr = autocorrelation(subset)
        for shift, value in corr.items():
            totals[shift] += value
    return totals


def pattern_seeds():
    # Seven size-5 complements of Sidon-like triples and one size-6 complement.
    sidon_triples = [
        [0, 1, 3],
        [0, 1, 4],
        [0, 1, 5],
        [0, 2, 3],
        [0, 2, 5],
        [0, 3, 4],
        [0, 3, 5],
    ]
    six_holes = [[0, step] for step in range(1, 5)]
    schedules = []
    for seed_idx, triple in enumerate(sidon_triples):
        five_base = complement(triple)
        for hole in six_holes:
            patterns = [rotate(five_base, shift) for shift in range(7)] + [complement(hole)]
            schedules.append(
                {
                    "schedule_id": "sidon_rot_%02d_hole_%d%d" % (seed_idx, hole[0], hole[1]),
                    "patterns": patterns,
                    "description": "seven rotated size-5 complements plus one size-6 complement",
                }
            )
    # A fixed reference seed from the review.
    patterns = [complement([0, 1, 3]) for _ in range(7)] + [complement([0, 1])]
    schedules.insert(
        0,
        {
            "schedule_id": "review_fixed_sidon_013_hole_01",
            "patterns": patterns,
            "description": "review reference: seven fixed complements of {0,1,3} plus complement of {0,1}",
        },
    )
    deduped = []
    seen = set()
    for row in schedules:
        key = tuple(tuple(pattern) for pattern in row["patterns"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def vector_to_coeffs(vector):
    coeffs = {}
    idx = 0
    for residue in range(1, MU_ORDER):
        for power in range(32):
            coeffs[(residue, power)] = vector[idx]
            idx += 1
    return coeffs


def p_eval(coeffs, x):
    total = x.parent()(0)
    for (residue, power), coeff in coeffs.items():
        if coeff:
            total += coeff * (x ** (residue + MU_ORDER * power))
    return total


def shift_nonzero(coeffs, gamma, shift):
    for (residue, power), coeff in coeffs.items():
        exponent = residue + MU_ORDER * power
        if coeff and (gamma ** (shift * exponent) - 1) != 0:
            return True
    return False


def coeff_hash(coeffs):
    payload = [
        [residue, power, str(value)]
        for (residue, power), value in sorted(coeffs.items())
        if value
    ]
    return hash_payload(payload)


def candidate_from_kernel(kernel_basis, gamma):
    if not kernel_basis:
        return None
    F = gamma.parent()
    field_candidates = [F(0), F(1)]
    z = F.gen()
    for exp in range(1, 96):
        field_candidates.append(z ** exp)
    for alpha in field_candidates:
        vector = None
        for idx, basis_vec in enumerate(kernel_basis):
            scale = alpha ** idx
            if vector is None:
                vector = scale * basis_vec
            else:
                vector += scale * basis_vec
        coeffs = vector_to_coeffs(vector)
        if all(shift_nonzero(coeffs, gamma, shift) for shift in range(1, MU_ORDER)):
            return coeffs
    return None


def build_matrix(F, omega, gamma, patterns):
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
                root_factor = gamma ** (selected * residue) - gamma ** (anchor * residue)
                for power in range(32):
                    exponent = residue + MU_ORDER * power
                    row.append(root_factor * (rep ** exponent))
            rows.append(row)
    return Matrix(F, rows)


def verify_candidate(F, omega, gamma, patterns, coeffs):
    points = []
    received = []
    selected_counts = [0 for _ in range(MU_ORDER)]
    for qidx in range(QUOTIENT_ORDER):
        rep = omega ** qidx
        subset = patterns[qidx % len(patterns)]
        anchor = min(subset)
        common = p_eval(coeffs, (gamma ** anchor) * rep)
        for residue in range(MU_ORDER):
            point = (gamma ** residue) * rep
            points.append(point)
            received.append(common)
            for codeword_shift in range(MU_ORDER):
                if (residue + codeword_shift) % MU_ORDER in subset:
                    selected_counts[codeword_shift] += 1
    agreements = [0 for _ in range(MU_ORDER)]
    for shift in range(MU_ORDER):
        for point, value in zip(points, received, strict=True):
            if p_eval(coeffs, (gamma ** shift) * point) == value:
                agreements[shift] += 1
    pair_agreements = {}
    for left in range(MU_ORDER):
        for right in range(left + 1, MU_ORDER):
            count = 0
            for point in points:
                if p_eval(coeffs, (gamma ** left) * point) == p_eval(coeffs, (gamma ** right) * point):
                    count += 1
            pair_agreements["P%d%d" % (left + 1, right + 1)] = count
    distinct = all(value <= DEGREE_BOUND - 1 for value in pair_agreements.values())
    return {
        "selected_counts": selected_counts,
        "agreement_vector": agreements,
        "min_agreement": min(agreements),
        "pair_agreement_max": max(pair_agreements.values()),
        "pair_agreements": pair_agreements,
        "eight_distinct": distinct,
        "coeff_hash": coeff_hash(coeffs),
    }


def audit():
    F = exact_field()
    gen = F.multiplicative_generator()
    omega = gen ** ((F.order() - 1) // H_ORDER)
    gamma = omega ** (H_ORDER // MU_ORDER)
    assert omega.multiplicative_order() == H_ORDER
    assert gamma.multiplicative_order() == MU_ORDER
    schedule_results = []
    best = None
    for schedule in pattern_seeds():
        patterns = schedule["patterns"]
        support_total = sum(len(pattern) for pattern in patterns) * (QUOTIENT_ORDER // len(patterns))
        corr = schedule_autocorrelation(patterns)
        ambient_pair_bound = max(corr.values()) * (QUOTIENT_ORDER // len(patterns))
        if support_total < TARGET_AGREEMENT or ambient_pair_bound > DEGREE_BOUND - 1:
            schedule_results.append(
                {
                    "schedule_id": schedule["schedule_id"],
                    "patterns": patterns,
                    "support_per_codeword": support_total,
                    "autocorrelation_by_shift": corr,
                    "ambient_pair_bound": ambient_pair_bound,
                    "status": "MU8_SCHEDULE_GUARD_FAIL",
                }
            )
            continue
        matrix = build_matrix(F, omega, gamma, patterns)
        rank = int(matrix.rank())
        nullity = int(matrix.ncols() - rank)
        candidate = None
        status = "MU8_ORBIT_NULLITY_ZERO"
        if nullity > 0:
            coeffs = candidate_from_kernel(matrix.right_kernel().basis(), gamma)
            if coeffs is None:
                status = "MU8_ORBIT_DEGENERATE_KERNEL"
            else:
                candidate = verify_candidate(F, omega, gamma, patterns, coeffs)
                status = (
                    "MU8_ORBIT_EXACT_CANDIDATE"
                    if candidate["eight_distinct"] and candidate["min_agreement"] >= TARGET_AGREEMENT
                    else "MU8_ORBIT_LOW_AGREEMENT_OR_COLLAPSE"
                )
        row = {
            "schedule_id": schedule["schedule_id"],
            "description": schedule["description"],
            "patterns": patterns,
            "pattern_size_sum": sum(len(pattern) for pattern in patterns),
            "support_per_codeword": support_total,
            "autocorrelation_by_shift": corr,
            "ambient_pair_bound": ambient_pair_bound,
            "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
            "rank": rank,
            "nullity": nullity,
            "candidate": candidate,
            "status": status,
        }
        schedule_results.append(row)
        if best is None or (row["nullity"], -row["rank"]) > (best["nullity"], -best["rank"]):
            best = row
        if status == "MU8_ORBIT_EXACT_CANDIDATE":
            best = row
            break
    exact_candidate = None
    if best and best.get("candidate") and best["status"] == "MU8_ORBIT_EXACT_CANDIDATE":
        exact_candidate = best["candidate"]
    proof_status = (
        "PROOF_RECORD / MU8_ORBIT_EXACT_CANDIDATE / EXPERIMENTAL"
        if exact_candidate
        else "EXACT_EXTRACTION_NO_A327 / MU8_ORBIT_NULLITY_ZERO_FRONT / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "2e551d7",
        "mu8_orbit_model": {
            "field": "GF(17^32)",
            "H_order": H_ORDER,
            "mu_order": MU_ORDER,
            "quotient_order": QUOTIENT_ORDER,
            "degree_bound": DEGREE_BOUND,
            "unknowns": 224,
            "target_support_per_codeword": 328,
            "P_form": "sum_{t=1}^7 X^t g_t(X^8), deg g_t < 32",
        },
        "search": {
            "schedules_tested": len(schedule_results),
            "guard_passing_schedules": sum(1 for row in schedule_results if row["status"] != "MU8_SCHEDULE_GUARD_FAIL"),
            "positive_nullity_schedules": sum(1 for row in schedule_results if row.get("nullity", 0) > 0),
            "exact_candidates": sum(1 for row in schedule_results if row["status"] == "MU8_ORBIT_EXACT_CANDIDATE"),
            "best_schedule_id": None if best is None else best["schedule_id"],
            "best_rank": None if best is None else best["rank"],
            "best_nullity": None if best is None else best["nullity"],
            "best_failure_mode": None if best is None else best["status"],
        },
        "schedule_results": schedule_results,
        "exact_candidate": exact_candidate,
        "proof_status": proof_status,
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
    args = parser.parse_args()
    record = audit()
    if args.write_json:
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        "schedules_tested": record["search"]["schedules_tested"],
        "guard_passing_schedules": record["search"]["guard_passing_schedules"],
        "positive_nullity_schedules": record["search"]["positive_nullity_schedules"],
        "exact_candidates": record["search"]["exact_candidates"],
        "best_schedule_id": record["search"]["best_schedule_id"],
        "best_rank": record["search"]["best_rank"],
        "best_nullity": record["search"]["best_nullity"],
        "best_failure_mode": record["search"]["best_failure_mode"],
    }
    if args.json:
        print(json.dumps(jsonable(summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_MU8_ORBIT_INVARIANT_CONSTRUCTION_READY")


if __name__ == "__main__":
    main()
