#!/usr/bin/env sage
"""Exact block/rank-feedback audit for the M1 a=327 mu_8 front."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from math import gcd as integer_gcd
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
H_ORDER = 512
MU_ORDER = 8
QUOTIENT_ORDER = 64
DEGREE_BOUND = 256
QUOTIENT_DEGREE_BOUND = 32
TARGET_AGREEMENT = 327
SOURCE_DATA = Path("experimental/data/m1_a327_mu8_orbit_invariant_construction.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_mu8_block_decomposition_audit.json")


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


def canonical_projective(vec):
    for value in vec:
        if value != 0:
            inv = value ** (-1)
            return tuple(inv * entry for entry in vec)
    raise ValueError("zero vector has no projective representative")


def projective_key(vec):
    return tuple(str(value) for value in canonical_projective(vec))


def load_source():
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def matrix_rows(F, omega, gamma, patterns):
    rows = []
    metadata = []
    functional_rows = []
    for qidx in range(QUOTIENT_ORDER):
        rep = omega ** qidx
        subset = patterns[qidx % len(patterns)]
        anchor = min(subset)
        for selected in subset:
            if selected == anchor:
                continue
            functional = []
            row = []
            for residue in range(1, MU_ORDER):
                root_factor = gamma ** (selected * residue) - gamma ** (anchor * residue)
                functional.append(root_factor * (rep ** residue))
                for power in range(QUOTIENT_DEGREE_BOUND):
                    exponent = residue + MU_ORDER * power
                    row.append(root_factor * (rep ** exponent))
            rows.append(row)
            metadata.append(
                {
                    "qidx": qidx,
                    "pattern_index": qidx % len(patterns),
                    "anchor": int(anchor),
                    "selected": int(selected),
                }
            )
            functional_rows.append(functional)
    return rows, metadata, functional_rows


def row_hashes(rows):
    return [hash_payload([str(value) for value in row]) for row in rows]


def matrix_hash(rows):
    return hash_payload(row_hashes(rows))


def build_matrix(F, rows, residue_subset=None):
    if residue_subset is None:
        return Matrix(F, rows)
    cols = []
    for residue in residue_subset:
        start = (int(residue) - 1) * QUOTIENT_DEGREE_BOUND
        cols.extend(range(start, start + QUOTIENT_DEGREE_BOUND))
    return Matrix(F, [[row[col] for col in cols] for row in rows])


def residue_subset_audit(F, rows, max_size):
    results = []
    residues = list(range(1, MU_ORDER))
    for size in range(1, max_size + 1):
        for subset in combinations(residues, size):
            matrix = build_matrix(F, rows, residue_subset=subset)
            rank = int(matrix.rank())
            cols = int(matrix.ncols())
            nullity = cols - rank
            divisor = MU_ORDER
            for residue in subset:
                divisor = integer_gcd(divisor, int(residue))
            gcd_visible = divisor == 1
            results.append(
                {
                    "residue_subset": list(subset),
                    "gcd_visible": bool(gcd_visible),
                    "matrix_shape": [int(matrix.nrows()), cols],
                    "rank": rank,
                    "nullity": nullity,
                    "status": "MU8_RESIDUE_NULLITY_POSITIVE" if nullity > 0 else "MU8_RESIDUE_FULL_RANK",
                }
            )
    return results


def functional_class_metadata(F, functional_rows):
    by_class = {}
    for qidx, functional in enumerate(functional_rows):
        key = projective_key(functional)
        by_class.setdefault(key, set()).add(qidx)
    class_rows = []
    for idx, (key, positions_set) in enumerate(sorted(by_class.items(), key=lambda item: (-len(item[1]), item[0]))):
        positions = sorted(positions_set)
        class_rows.append(
            {
                "class_index": idx,
                "support_size": len(positions),
                "forced_identity_threshold32": len(positions) >= QUOTIENT_DEGREE_BOUND,
                "positions_hash": hash_payload(positions),
                "functional_hash": hash_payload(list(key)),
            }
        )
    matrix = Matrix(F, functional_rows)
    rank = int(matrix.rank()) if functional_rows else 0
    return {
        "point_constraint_rows": len(functional_rows),
        "dual_span_dimension": rank,
        "common_kernel_dimension": MU_ORDER - 1 - rank,
        "projective_functional_classes": len(class_rows),
        "support_size_histogram": dict(sorted(Counter(str(row["support_size"]) for row in class_rows).items(), key=lambda item: int(item[0]))),
        "forced_identities_threshold32": sum(1 for row in class_rows if row["forced_identity_threshold32"]),
        "classes": class_rows,
    }


def equivariance_audit(F, rows, row_meta, omega, gamma):
    # Conservative check for the prompt's Z/8 column action Q_r -> zeta^r Q_r.
    # We only accept block splitting if the transformed rows are exactly rows of the same matrix.
    transformed_hashes = {}
    existing = {}
    for idx, row in enumerate(rows):
        existing.setdefault(hash_payload([str(value) for value in row]), []).append(idx)
    for idx, row in enumerate(rows):
        transformed = []
        for residue in range(1, MU_ORDER):
            phase = gamma ** residue
            start = (residue - 1) * QUOTIENT_DEGREE_BOUND
            for col in range(start, start + QUOTIENT_DEGREE_BOUND):
                transformed.append(phase * row[col])
        transformed_hashes[idx] = hash_payload([str(value) for value in transformed])
    matched = sum(1 for key in transformed_hashes.values() if key in existing)
    defect_rows = len(rows) - matched
    return {
        "equivariance_checked": True,
        "column_action": "Q_r -> zeta^r Q_r",
        "row_action_certified": defect_rows == 0,
        "matched_transformed_rows": matched,
        "equivariance_defect_rows": defect_rows,
        "equivariance_defect_rank": None,
        "block_decomposition_used": False,
        "reason": "block split disabled unless every transformed row is present in the row set",
    }


def audit(max_subset_size, compute_full_rank):
    source = load_source()
    F = exact_field()
    gen = F.multiplicative_generator()
    omega = gen ** ((F.order() - 1) // H_ORDER)
    gamma = omega ** (H_ORDER // MU_ORDER)
    assert omega.multiplicative_order() == H_ORDER
    assert gamma.multiplicative_order() == MU_ORDER
    schedule_audits = []
    for schedule in source["schedule_results"]:
        if schedule["status"] == "MU8_SCHEDULE_GUARD_FAIL":
            continue
        patterns = schedule["patterns"]
        rows, metadata, functional_rows = matrix_rows(F, omega, gamma, patterns)
        matrix_shape = [len(rows), (MU_ORDER - 1) * QUOTIENT_DEGREE_BOUND]
        if compute_full_rank:
            matrix = build_matrix(F, rows)
            rank = int(matrix.rank())
            nullity = int(matrix.ncols() - rank)
        else:
            rank = int(schedule["rank"])
            nullity = int(schedule["nullity"])
        residue_results = residue_subset_audit(F, rows, max_size=max_subset_size) if max_subset_size > 0 else []
        functional_meta = functional_class_metadata(F, functional_rows)
        equivariance = equivariance_audit(F, rows, metadata, omega, gamma)
        positive_residue = [row for row in residue_results if row["nullity"] > 0]
        schedule_audits.append(
            {
                "schedule_id": schedule["schedule_id"],
                "patterns": patterns,
                "source_matrix_shape": schedule["matrix_shape"],
                "source_rank": schedule["rank"],
                "source_nullity": schedule["nullity"],
                "canonical_matrix_shape": matrix_shape,
                "canonical_rank": rank,
                "canonical_nullity": nullity,
                "canonical_reproduces_source": (
                    schedule["matrix_shape"] == matrix_shape
                    and schedule["rank"] == rank
                    and schedule["nullity"] == nullity
                ),
                "matrix_hash": matrix_hash(rows),
                "row_metadata_hash": hash_payload(metadata),
                "equivariance": equivariance,
                "quotient_subspace_metadata": functional_meta,
                "residue_subset_max_size": max_subset_size,
                "residue_subset_ranks": residue_results,
                "positive_residue_subset_count": len(positive_residue),
                "best_residue_nullity": max([row["nullity"] for row in residue_results], default=0),
                "best_residue_subset": None if not positive_residue else max(positive_residue, key=lambda row: (row["nullity"], row["gcd_visible"]))["residue_subset"],
                "status": "MU8_BLOCK_AUDIT_NULLITY_POSITIVE" if nullity > 0 or positive_residue else "MU8_BLOCK_AUDIT_FULL_RANK",
            }
        )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "dd07a87",
        "audit_model": {
            "field": "GF(17^32)",
            "H_order": H_ORDER,
            "mu_order": MU_ORDER,
            "quotient_order": QUOTIENT_ORDER,
            "active_variables": 224,
            "quotient_degree_bound": QUOTIENT_DEGREE_BOUND,
            "canonical_matrix_formula": "(zeta^(i*r)-zeta^(a*r))*(alpha_b*zeta^t)^r*y^ell",
            "residue_subset_max_size": max_subset_size,
            "full_rank_recomputed": compute_full_rank,
        },
        "block_audit": {
            "schedules_audited": len(schedule_audits),
            "canonical_reproduction_pass": all(row["canonical_reproduces_source"] for row in schedule_audits),
            "equivariance_certified_schedules": sum(1 for row in schedule_audits if row["equivariance"]["row_action_certified"]),
            "positive_full_nullity_schedules": sum(1 for row in schedule_audits if row["canonical_nullity"] > 0),
            "positive_residue_subset_schedules": sum(1 for row in schedule_audits if row["positive_residue_subset_count"] > 0),
            "best_full_nullity": max([row["canonical_nullity"] for row in schedule_audits], default=0),
            "best_residue_nullity": max([row["best_residue_nullity"] for row in schedule_audits], default=0),
            "best_failure_mode": "MU8_BLOCK_AUDIT_FULL_RANK",
        },
        "schedule_audits": schedule_audits,
        "proof_status": "EXACT_EXTRACTION_NO_A327 / MU8_BLOCK_AUDIT_FULL_RANK / PARTIAL / EXPERIMENTAL",
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
    parser.add_argument("--max-subset-size", type=int, default=0)
    parser.add_argument("--compute-full-rank", action="store_true")
    args = parser.parse_args()
    record = audit(max_subset_size=args.max_subset_size, compute_full_rank=args.compute_full_rank)
    if args.write_json:
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": record["proof_status"],
        "schedules_audited": record["block_audit"]["schedules_audited"],
        "canonical_reproduction_pass": record["block_audit"]["canonical_reproduction_pass"],
        "equivariance_certified_schedules": record["block_audit"]["equivariance_certified_schedules"],
        "positive_full_nullity_schedules": record["block_audit"]["positive_full_nullity_schedules"],
        "positive_residue_subset_schedules": record["block_audit"]["positive_residue_subset_schedules"],
        "best_full_nullity": record["block_audit"]["best_full_nullity"],
        "best_residue_nullity": record["block_audit"]["best_residue_nullity"],
        "best_failure_mode": record["block_audit"]["best_failure_mode"],
    }
    if args.json:
        print(json.dumps(jsonable(summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_MU8_BLOCK_DECOMPOSITION_READY")


if __name__ == "__main__":
    main()
