#!/usr/bin/env sage
"""Exact GF(17^32) rank batch and kernel classifier for mu_8 mutations."""

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
RANK_OUTPUT = Path("experimental/data/m1_a327_mu8_exact_rank_batch_64.json")
CLASS_OUTPUT = Path("experimental/data/m1_a327_mu8_kernel_classification.json")
WITNESS_OUTPUT = Path("experimental/data/m1_a327_mu8_exact_witness_audit.json")


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


def matrix_rows(F, omega, gamma, patterns):
    rows = []
    metadata = []
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
                for power in range(QUOTIENT_DEGREE_BOUND):
                    exponent = residue + MU_ORDER * power
                    row.append(root_factor * (rep ** exponent))
            rows.append(row)
            metadata.append({"qidx": qidx, "anchor": int(anchor), "selected": int(selected)})
    return rows, metadata


def matrix_hash(rows):
    return hash_payload([[str(value) for value in row] for row in rows])


def build_matrix(F, rows):
    return Matrix(F, rows)


def vector_to_coeffs(vector):
    coeffs = {}
    idx = 0
    for residue in range(1, MU_ORDER):
        for power in range(QUOTIENT_DEGREE_BOUND):
            coeffs[(residue, power)] = vector[idx]
            idx += 1
    return coeffs


def pair_map_vector(vector, gamma, left, right):
    F = gamma.parent()
    out = [F(0) for _ in range(DEGREE_BOUND)]
    idx = 0
    for residue in range(1, MU_ORDER):
        phase = gamma ** ((left - 1) * residue) - gamma ** ((right - 1) * residue)
        for power in range(QUOTIENT_DEGREE_BOUND):
            exponent = residue + MU_ORDER * power
            out[exponent] += phase * vector[idx]
            idx += 1
    return out


def pair_projection_zero(kernel_basis, gamma, left, right):
    for vec in kernel_basis:
        if any(value != 0 for value in pair_map_vector(vec, gamma, left, right)):
            return False
    return True


def classify_kernel(kernel_basis, gamma):
    forced_pairs = []
    projection_ranks = {}
    for left in range(1, 8):
        for right in range(left + 1, 8):
            label = "P%d%d" % (left, right)
            forced = pair_projection_zero(kernel_basis, gamma, left, right)
            projection_ranks[label] = 0 if forced else 1
            if forced:
                forced_pairs.append([left, right])
    if not forced_pairs:
        status = "MU8_KERNEL_PAIR_VISIBLE"
    elif len(forced_pairs) == 21:
        status = "MU8_KERNEL_COMMON_KERNEL_ONLY"
    else:
        status = "MU8_KERNEL_MIXED_PAIR_FORCED"
    return {
        "forced_equal_pairs": forced_pairs,
        "projection_rank_by_pair": projection_ranks,
        "status": status,
    }


def polynomial_vector_nonzero(values):
    return any(value != 0 for value in values)


def deterministic_avoidance(kernel_basis, gamma):
    if not kernel_basis:
        return None
    F = gamma.parent()
    x = None
    processed = []
    pair_maps = [(left, right) for left in range(1, 8) for right in range(left + 1, 8)]
    scalar_candidates = [F(i) for i in range(P)]
    z = F.gen()
    scalar_candidates.extend(z ** exp for exp in range(1, 96))
    for left, right in pair_maps:
        if x is not None and polynomial_vector_nonzero(pair_map_vector(x, gamma, left, right)):
            processed.append((left, right))
            continue
        y = None
        for basis_vec in kernel_basis:
            if polynomial_vector_nonzero(pair_map_vector(basis_vec, gamma, left, right)):
                y = basis_vec
                break
        if y is None:
            return None
        forbidden = {F(0)}
        if x is None:
            x = F(0) * y
        for prev_left, prev_right in processed:
            ux = pair_map_vector(x, gamma, prev_left, prev_right)
            uy = pair_map_vector(y, gamma, prev_left, prev_right)
            pivot = None
            for idx, value in enumerate(uy):
                if value != 0:
                    pivot = idx
                    break
            if pivot is None:
                continue
            a0 = -ux[pivot] / uy[pivot]
            if all(ux[idx] + a0 * uy[idx] == 0 for idx in range(len(ux))):
                forbidden.add(a0)
        chosen = None
        for value in scalar_candidates:
            if value not in forbidden:
                chosen = value
                break
        if chosen is None:
            return None
        x = x + chosen * y
        processed.append((left, right))
    return x


def p_eval(coeffs, x):
    F = x.parent()
    total = F(0)
    for (residue, power), coeff in coeffs.items():
        if coeff:
            total += coeff * (x ** (residue + MU_ORDER * power))
    return total


def verify_witness_vector(vector, omega, gamma, patterns):
    coeffs = vector_to_coeffs(vector)
    points = []
    received = []
    for qidx in range(QUOTIENT_ORDER):
        rep = omega ** qidx
        subset = patterns[qidx % len(patterns)]
        anchor = min(subset)
        common = p_eval(coeffs, (gamma ** anchor) * rep)
        for residue in range(MU_ORDER):
            points.append((gamma ** residue) * rep)
            received.append(common)
    agreements = []
    for shift in range(7):
        count = 0
        for point, value in zip(points, received, strict=True):
            if p_eval(coeffs, (gamma ** shift) * point) == value:
                count += 1
        agreements.append(count)
    pair_agreements = {}
    for left in range(7):
        for right in range(left + 1, 7):
            count = 0
            for point in points:
                if p_eval(coeffs, (gamma ** left) * point) == p_eval(coeffs, (gamma ** right) * point):
                    count += 1
            pair_agreements["P%d%d" % (left + 1, right + 1)] = count
    return {
        "constructed": True,
        "agreement_vector": agreements,
        "min_agreement": min(agreements),
        "pair_agreement_max": max(pair_agreements.values()),
        "pair_agreements": pair_agreements,
        "seven_distinct": all(value <= DEGREE_BOUND - 1 for value in pair_agreements.values()),
        "coeff_hash": hash_payload([[residue, power, str(value)] for (residue, power), value in sorted(coeffs.items()) if value]),
    }


def audit(limit=None):
    scan = load_scan()
    F = exact_field()
    gen = F.multiplicative_generator()
    omega = gen ** ((F.order() - 1) // H_ORDER)
    gamma = omega ** (H_ORDER // MU_ORDER)
    rank_rows = []
    classifications = []
    witness = None
    schedules = scan["candidate_schedules"]
    if limit is not None:
        schedules = schedules[:limit]
    for schedule in schedules:
        patterns = schedule["patterns"]
        rows, metadata = matrix_rows(F, omega, gamma, patterns)
        matrix = build_matrix(F, rows)
        rank = int(matrix.rank())
        nullity = int(matrix.ncols() - rank)
        row = {
            "candidate_id": schedule["candidate_id"],
            "source_schedule_id": schedule["source_schedule_id"],
            "move": schedule["move"],
            "patterns_hash": schedule["patterns_hash"],
            "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
            "rank": rank,
            "nullity": nullity,
            "canonical_matrix_hash": matrix_hash(rows),
            "row_metadata_hash": hash_payload(metadata),
            "pivot_column_count": rank,
            "minor_certificate_available": False,
            "status": "MU8_SELECTED_MUTATION_FULL_COLUMN_RANK" if nullity == 0 else "MU8_SELECTED_MUTATION_POSITIVE_NULLITY",
        }
        rank_rows.append(row)
        if nullity <= 0:
            continue
        kernel_basis = matrix.right_kernel().basis()
        classification = classify_kernel(kernel_basis, gamma)
        classification.update(
            {
                "candidate_id": schedule["candidate_id"],
                "kernel_nullity": len(kernel_basis),
                "patterns_hash": schedule["patterns_hash"],
            }
        )
        classifications.append(classification)
        if classification["status"] == "MU8_KERNEL_PAIR_VISIBLE" and witness is None:
            vector = deterministic_avoidance(kernel_basis, gamma)
            if vector is not None:
                candidate = verify_witness_vector(vector, omega, gamma, patterns)
                candidate["candidate_id"] = schedule["candidate_id"]
                witness = candidate
    rank_status = (
        "CANDIDATE / MU8_SELECTED_MUTATION_POSITIVE_NULLITY / PARTIAL / EXPERIMENTAL"
        if any(row["nullity"] > 0 for row in rank_rows)
        else "EXACT_EXTRACTION_NO_A327 / MU8_SELECTED_MUTATION_FULL_COLUMN_RANK / PARTIAL / EXPERIMENTAL"
    )
    if witness and witness["seven_distinct"] and witness["min_agreement"] >= TARGET_AGREEMENT:
        witness_status = "EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS"
    else:
        witness_status = "NO_EXACT_WITNESS_CONSTRUCTED"
    rank_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "01bc0e3",
        "rank_batch": {
            "field": "GF(17^32)",
            "schedules_planned": len(scan["candidate_schedules"]),
            "schedules_tested": len(rank_rows),
            "full_rank_schedules": sum(1 for row in rank_rows if row["nullity"] == 0),
            "positive_nullity_schedules": sum(1 for row in rank_rows if row["nullity"] > 0),
            "best_nullity": max([row["nullity"] for row in rank_rows], default=0),
            "best_failure_mode": "MU8_SELECTED_MUTATION_FULL_COLUMN_RANK" if all(row["nullity"] == 0 for row in rank_rows) else "MU8_SELECTED_MUTATION_POSITIVE_NULLITY",
        },
        "schedule_ranks": rank_rows,
        "proof_status": rank_status,
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
    class_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "01bc0e3",
        "kernel_classification": {
            "positive_nullity_schedules": len(classifications),
            "pair_visible_kernels": sum(1 for row in classifications if row["status"] == "MU8_KERNEL_PAIR_VISIBLE"),
            "pair_forced_kernels": sum(1 for row in classifications if row["status"] != "MU8_KERNEL_PAIR_VISIBLE"),
            "classifications": classifications,
        },
        "proof_status": "CANDIDATE / MU8_KERNEL_CLASSIFICATION / PARTIAL / EXPERIMENTAL" if classifications else "EXACT_EXTRACTION_NO_A327 / MU8_KERNEL_CLASSIFICATION_NOT_RUN_FULL_RANK / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": rank_record["not_claimed"],
    }
    witness_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "01bc0e3",
        "witness_audit": witness if witness is not None else {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "min_agreement": None,
            "status": witness_status,
        },
        "proof_status": "PROOF_RECORD / EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS / EXPERIMENTAL" if witness_status == "EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS" else "EXACT_EXTRACTION_NO_A327 / NO_EXACT_WITNESS_CONSTRUCTED / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": rank_record["not_claimed"],
    }
    return rank_record, class_record, witness_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    rank_record, class_record, witness_record = audit(limit=args.limit)
    if args.write_json:
        RANK_OUTPUT.write_text(json.dumps(jsonable(rank_record), indent=2, sort_keys=True) + "\n")
        CLASS_OUTPUT.write_text(json.dumps(jsonable(class_record), indent=2, sort_keys=True) + "\n")
        WITNESS_OUTPUT.write_text(json.dumps(jsonable(witness_record), indent=2, sort_keys=True) + "\n")
    summary = {
        "rank_status": rank_record["proof_status"],
        "classification_status": class_record["proof_status"],
        "witness_status": witness_record["proof_status"],
        "schedules_tested": rank_record["rank_batch"]["schedules_tested"],
        "full_rank_schedules": rank_record["rank_batch"]["full_rank_schedules"],
        "positive_nullity_schedules": rank_record["rank_batch"]["positive_nullity_schedules"],
        "best_nullity": rank_record["rank_batch"]["best_nullity"],
    }
    if args.json:
        print(json.dumps(jsonable(summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_MU8_EXACT_RANK_BATCH_READY")


if __name__ == "__main__":
    main()
