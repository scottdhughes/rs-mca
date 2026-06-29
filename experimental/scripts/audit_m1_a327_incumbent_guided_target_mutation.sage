#!/usr/bin/env sage
"""Exact GF(17^32) lift audit for incumbent-guided proxy target-mutation hits."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from numbers import Integral
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
VARIABLE_COUNT = DIFF_COUNT * K
TARGET_AGREEMENT = 327

SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_incumbent_guided_target_mutation.py")
SCAN_DATA_PATH = Path("experimental/data/m1_a327_incumbent_guided_target_mutation.json")
DATA_PATH = Path("experimental/data/m1_a327_incumbent_guided_target_mutation_exact_audit.json")

EXACT_SELECTION_LIMIT = 3
EXACT_LIFT_SAMPLES_PER_SYSTEM = 4


def load_scanner():
    script_dir = str(SCANNER_PATH.parent.resolve())
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location("incumbent_guided_scanner", SCANNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


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


def hash_payload(payload):
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def field_context():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def reconstruct_selected(scanner, result_row):
    parent = scanner.load_parent()
    incumbents = {
        row["target_system_id"]: row
        for row in parent["retained_results"]
        if row["best"]["assignment"] is not None
    }
    incumbent = incumbents[result_row["base_target_system_id"]]
    sources = scanner.source_by_candidate_id()
    source = sources[scanner.parse_source_id(incumbent["target_system_id"])]
    base_selection = scanner.reconstruct_selected(
        source,
        incumbent["row_budget"],
        incumbent["selection_objective"],
    )
    coords = scanner.balanced.candidate_coordinates(source["membership_masks"])
    deficit = [
        TARGET_AGREEMENT - value
        for value in incumbent["best"]["assignment"]["agreement_vector"]
    ]
    selected_info = scanner.mutate_selected(
        coords,
        base_selection["selected"],
        result_row["row_budget"],
        result_row["mutation_profile"],
        deficit,
        result_row["mutation_round"],
    )
    if selected_info["mutation_hash"] != result_row["mutation_hash"]:
        raise RuntimeError("mutation hash mismatch for %s" % result_row["mutated_system_id"])
    return source, incumbent, selected_info


def proxy_vectors_for_row(scanner, result_row):
    source, incumbent, selected_info = reconstruct_selected(scanner, result_row)
    H = scanner.joint.proxy_subgroup()
    powers = scanner.joint.vandermonde_powers(H)
    rows = scanner.rows_for_selected(powers, selected_info["selected"])
    echelon, pivots = scanner.echelon_modp(rows, scanner.PROXY_PRIME)
    seed = int(
        scanner.hash_payload([incumbent["target_system_id"], selected_info["mutation_hash"]])[:12],
        16,
    )
    vectors = scanner.balanced.sample_nullspace_vectors(
        echelon,
        pivots,
        seed,
        scanner.SAMPLES_PER_SYSTEM,
    )
    retained_candidate_hashes = [
        sample["vector_hash"]
        for sample in result_row["retained_sample_results"]
        if sample["assignment"] is not None
        and sample["assignment"]["exact_max_min"] >= TARGET_AGREEMENT
    ]
    vector_by_hash = {
        scanner.hash_payload(vector.tolist()): vector
        for vector in vectors
    }
    selected_hashes = [digest for digest in retained_candidate_hashes if digest in vector_by_hash]
    if len(selected_hashes) < EXACT_LIFT_SAMPLES_PER_SYSTEM:
        ordered = sorted(
            vector_by_hash,
            key=lambda digest: (digest not in set(selected_hashes), digest),
        )
        for digest in ordered:
            if digest not in selected_hashes:
                selected_hashes.append(digest)
            if len(selected_hashes) >= EXACT_LIFT_SAMPLES_PER_SYSTEM:
                break
    return {
        "source": source,
        "incumbent": incumbent,
        "selected_info": selected_info,
        "proxy_rank": len(pivots),
        "proxy_nullity": VARIABLE_COUNT - len(pivots),
        "proxy_pivot_columns_hash": scanner.hash_payload(pivots),
        "vectors": [
            {
                "proxy_vector_hash": digest,
                "vector": vector_by_hash[digest],
                "was_proxy_candidate": digest in set(retained_candidate_hashes),
            }
            for digest in selected_hashes[:EXACT_LIFT_SAMPLES_PER_SYSTEM]
        ],
    }


def evaluate_lifted_vector(F, powers, vector):
    values = [[F(0) for _ in range(N)]]
    coefficients_mod17 = [int(value) % P for value in vector.tolist()]
    for witness in range(DIFF_COUNT):
        start = witness * K
        witness_values = [F(0) for _ in range(N)]
        for degree in range(K):
            coeff = coefficients_mod17[start + degree]
            if coeff == 0:
                continue
            scalar = F(coeff)
            power_row = powers[degree]
            for pos in range(N):
                witness_values[pos] += scalar * power_row[pos]
        values.append(witness_values)
    return values, coefficients_mod17


def class_masks_by_position(values):
    rows = []
    for pos in range(N):
        buckets = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = int(buckets.get(value, 0)) | (1 << witness)
        rows.append(sorted(set(int(mask) for mask in buckets.values())))
    return rows


def capacity_from_class_masks(class_rows):
    total = 0
    histogram = {}
    for masks in class_rows:
        largest = max(int(mask).bit_count() for mask in masks)
        total += largest
        histogram[str(largest)] = histogram.get(str(largest), 0) + 1
    return {
        "capacity_total": total,
        "capacity_upper_bound": total // LIST_SIZE,
        "largest_class_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
    }


def assignment_max_min(class_rows):
    offsets = []
    total_vars = 0
    for classes in class_rows:
        offsets.append(total_vars)
        total_vars += len(classes)

    def feasible(floor):
        objective = np.zeros(total_vars)
        bounds = Bounds(np.zeros(total_vars), np.ones(total_vars))
        integrality = np.ones(total_vars)
        rows = []
        lower = []
        upper = []
        for pos, classes in enumerate(class_rows):
            row = np.zeros(total_vars)
            row[offsets[pos] : offsets[pos] + len(classes)] = 1
            rows.append(row)
            lower.append(1)
            upper.append(1)
        for witness in range(LIST_SIZE):
            row = np.zeros(total_vars)
            for pos, classes in enumerate(class_rows):
                for idx, mask in enumerate(classes):
                    if int(mask) & (1 << witness):
                        row[offsets[pos] + idx] = 1
            rows.append(row)
            lower.append(floor)
            upper.append(np.inf)
        result = milp(
            objective,
            integrality=integrality,
            bounds=bounds,
            constraints=LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper)),
            options={"time_limit": 20},
        )
        if not result.success:
            return False, None
        rounded = np.rint(result.x).astype(int)
        chosen = []
        for pos, classes in enumerate(class_rows):
            start = offsets[pos]
            choice = next(
                (idx for idx, value in enumerate(rounded[start : start + len(classes)]) if value),
                0,
            )
            chosen.append(int(classes[choice]))
        return True, chosen

    cap = capacity_from_class_masks(class_rows)["capacity_upper_bound"]
    lo, hi = 0, max(cap, TARGET_AGREEMENT)
    best_masks = None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok, masks = feasible(mid)
        if ok:
            lo = mid
            best_masks = masks
        else:
            hi = mid - 1
    agreement = [0] * LIST_SIZE
    if best_masks is not None:
        for mask in best_masks:
            for witness in range(LIST_SIZE):
                if int(mask) & (1 << witness):
                    agreement[witness] += 1
    return {
        "exact_max_min": int(lo),
        "agreement_vector": agreement,
        "chosen_masks_hash": None if best_masks is None else hash_payload(best_masks),
    }


def value_hashes(values):
    return [hash_payload([str(value) for value in row]) for row in values]


def audit_vector(F, powers, vector_entry):
    values, coefficients_mod17 = evaluate_lifted_vector(F, powers, vector_entry["vector"])
    codeword_hashes = value_hashes(values)
    distinct = len(set(codeword_hashes)) == LIST_SIZE
    class_rows = class_masks_by_position(values)
    capacity = capacity_from_class_masks(class_rows)
    assignment = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        assignment = assignment_max_min(class_rows)
    exact_hit = distinct and assignment is not None and assignment["exact_max_min"] >= TARGET_AGREEMENT
    status = "EXACT_LIFT_A327_ASSIGNMENT" if exact_hit else (
        "EXACT_LIFT_DEGENERATE_CODEWORDS"
        if not distinct
        else "EXACT_LIFT_HIGH_CAPACITY_IMBALANCED"
        if assignment is not None
        else "EXACT_LIFT_LOW_CAPACITY"
    )
    row = {
        "proxy_vector_hash": vector_entry["proxy_vector_hash"],
        "was_proxy_candidate": vector_entry["was_proxy_candidate"],
        "coefficients_mod17_hash": hash_payload(coefficients_mod17),
        "codeword_value_hash": hash_payload(codeword_hashes),
        "distinct_codewords": distinct,
        **capacity,
        "assignment": assignment,
        "status": status,
    }
    if exact_hit:
        row["coefficients_mod17"] = coefficients_mod17
    return row


def audit_system(scanner, result_row, F, powers):
    proxy = proxy_vectors_for_row(scanner, result_row)
    samples = [audit_vector(F, powers, entry) for entry in proxy["vectors"]]
    best = max(
        samples,
        key=lambda row: (
            -1 if row["assignment"] is None else row["assignment"]["exact_max_min"],
            row["capacity_upper_bound"],
            row["capacity_total"],
            row["proxy_vector_hash"],
        ),
    )
    return {
        "mutated_system_id": result_row["mutated_system_id"],
        "source_candidate_id": result_row["source_candidate_id"],
        "mutation_profile": result_row["mutation_profile"],
        "mutation_round": result_row["mutation_round"],
        "row_budget": result_row["row_budget"],
        "proxy_best_max_min": result_row["best"]["assignment"]["exact_max_min"],
        "proxy_best_agreement_vector": result_row["best"]["assignment"]["agreement_vector"],
        "proxy_best_capacity_upper_bound": result_row["best"]["capacity_upper_bound"],
        "target_coordinate_count": result_row["target_coordinate_count"],
        "target_row_count": result_row["target_row_count"],
        "proxy_rank": proxy["proxy_rank"],
        "proxy_nullity": proxy["proxy_nullity"],
        "proxy_pivot_columns_hash": proxy["proxy_pivot_columns_hash"],
        "exact_lift_sample_count": len(samples),
        "exact_lift_a327_sample_count": sum(1 for row in samples if row["status"] == "EXACT_LIFT_A327_ASSIGNMENT"),
        "best_exact_lift_sample": best,
        "sample_results": samples,
    }


def selected_proxy_rows(scan_record):
    rows = [
        row
        for row in scan_record["retained_results"]
        if row["best"]["assignment"] is not None
        and row["best"]["assignment"]["exact_max_min"] >= TARGET_AGREEMENT
    ]
    rows.sort(
        key=lambda row: (
            row["best"]["assignment"]["exact_max_min"],
            row["best"]["capacity_upper_bound"],
            row["proxy_candidate_count"],
            row["mutated_system_id"],
        ),
        reverse=True,
    )
    return rows[:EXACT_SELECTION_LIMIT]


def audit_record():
    scanner = load_scanner()
    with SCAN_DATA_PATH.open() as handle:
        scan_record = json.load(handle)
    q, F, H = field_context()
    powers = precompute_powers(F, H)
    selected_rows = selected_proxy_rows(scan_record)
    results = [audit_system(scanner, row, F, powers) for row in selected_rows]
    exact_hit_count = sum(row["exact_lift_a327_sample_count"] for row in results)
    best = None
    if results:
        best = max(
            results,
            key=lambda row: (
                -1
                if row["best_exact_lift_sample"]["assignment"] is None
                else row["best_exact_lift_sample"]["assignment"]["exact_max_min"],
                row["best_exact_lift_sample"]["capacity_upper_bound"],
                row["mutated_system_id"],
            ),
        )
    proof_status = "CANDIDATE_EXACT_LIFT" if exact_hit_count else "EXACT_LIFTED_PROXY_CANDIDATES_NO_A327"
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "incumbent_guided_target_mutation_exact_lift_audit",
            "source": {
                "source_json": str(SCAN_DATA_PATH),
                "source_result_hash": scan_record["result_hash"],
                "source_proof_status": scan_record["proof_status"],
                "source_proxy_candidate_system_count": scan_record["proxy_candidate_system_count"],
                "source_exact_trigger_count": len(scan_record["exact_audit_triggers"]),
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "degree_bound": K,
            "selection_limit": EXACT_SELECTION_LIMIT,
            "exact_lift_samples_per_system": EXACT_LIFT_SAMPLES_PER_SYSTEM,
            "exact_lift_audited_system_count": len(results),
            "exact_lift_a327_sample_count": exact_hit_count,
            "exact_nullspace_extraction_status": "NOT_RUN_EXACT_GF1732_RREF_TOO_SLOW_FOR_THIS_PACKET",
            "best": best,
            "results": results,
            "result_hash": hash_payload(results),
            "proof_status": proof_status,
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list proof record",
                "global Lambda_mu(C,327) <= 6",
                "exact Lambda_mu",
                "exact delta*_C",
                "improvement over PR #133",
                "full GF(17^32) nullspace extraction for the proxy target systems",
            ],
        }
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()

    record = audit_record()
    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_INCUMBENT_GUIDED_TARGET_MUTATION_OK")
        print("exact_lift_audited_system_count: %d" % record["exact_lift_audited_system_count"])
        print("exact_lift_a327_sample_count: %d" % record["exact_lift_a327_sample_count"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
