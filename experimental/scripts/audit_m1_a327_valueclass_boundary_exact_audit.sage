#!/usr/bin/env sage
"""Exact GF(17^32) pivot-minor audit for selected M1 a=327 boundary designs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_valueclass_boundary_search.py")
SOURCE_DATA_PATH = Path("experimental/data/m1_a327_valueclass_boundary_search.json")
DATA_PATH = Path("experimental/data/m1_a327_valueclass_boundary_exact_audit.json")

AUDIT_SELECTION = [
    {
        "candidate_id": "boundary_residual_45_c00_b5_200",
        "reason": "top retained proxy-ranked candidate; lowest compressed-variable count",
    },
    {
        "candidate_id": "quotient_fiber_45_c00_b5_064",
        "reason": "best quotient_fiber_45 structural boundary candidate",
    },
    {
        "candidate_id": "pair_boundary_45_c15_b5_064",
        "reason": "best retained pair_boundary_45 candidate",
    },
    {
        "candidate_id": "boundary_residual_45_c00_b5_096",
        "reason": "boundary_residual_45 structural variant with different residual split",
    },
    {
        "candidate_id": "pair_boundary_45_c00_b5_064",
        "reason": "pair_boundary_45 anchor-clique high boundary-pressure variant",
    },
]


def load_scanner():
    spec = importlib.util.spec_from_file_location("valueclass_boundary_scanner", SCANNER_PATH)
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


def field_context_exact():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


def field_context_proxy():
    F = GF(PROXY_PRIME)
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((PROXY_PRIME - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return F, H


def precompute_powers(F, H):
    powers = [[F(1) for _ in H]]
    for degree in range(1, K):
        previous = powers[-1]
        powers.append([previous[pos] * H[pos] for pos in range(N)])
    return powers


def bit(mask, idx):
    return bool(int(mask) & (1 << idx))


def locator_values(F, H, positions):
    roots = [H[pos] for pos in positions]
    position_set = set(positions)
    values = []
    for pos, point in enumerate(H):
        if pos in position_set:
            values.append(F(0))
            continue
        acc = F(1)
        for root in roots:
            acc *= point - root
        values.append(acc)
    return values


def reduced_rows(candidate, F, H, powers):
    masks = candidate["membership_masks"]
    anchor_zero_positions = {}
    locator_by_witness = {}
    dim_by_witness = {}
    offsets = {}
    total_vars = 0

    for witness in range(1, LIST_SIZE):
        zero_positions = [
            pos
            for pos, mask in enumerate(masks)
            if bit(mask, 0) and bit(mask, witness)
        ]
        anchor_zero_positions[str(witness)] = len(zero_positions)
        dim = max(0, K - len(zero_positions))
        dim_by_witness[witness] = dim
        offsets[witness] = total_vars
        total_vars += dim
        locator_by_witness[witness] = locator_values(F, H, zero_positions)

    rows = []
    row_type_counts = {}
    row_descriptors = []
    for left, right in itertools.combinations(range(1, LIST_SIZE), 2):
        for pos, mask in enumerate(masks):
            if not (bit(mask, left) and bit(mask, right)):
                continue
            row = [F(0)] * total_vars
            left_locator = locator_by_witness[left][pos]
            right_locator = locator_by_witness[right][pos]
            for degree in range(dim_by_witness[left]):
                row[offsets[left] + degree] = left_locator * powers[degree][pos]
            for degree in range(dim_by_witness[right]):
                row[offsets[right] + degree] -= right_locator * powers[degree][pos]
            if any(entry != 0 for entry in row):
                rows.append(row)
                pair_label = f"{left},{right}"
                row_type_counts[pair_label] = row_type_counts.get(pair_label, 0) + 1
                row_descriptors.append({"pair": pair_label, "coordinate": pos})

    metadata = {
        "anchor_zero_counts": anchor_zero_positions,
        "compressed_variables": total_vars,
        "remaining_equations": len(rows),
        "row_type_counts": dict(sorted(row_type_counts.items())),
        "row_descriptor_hash": hash_payload(row_descriptors),
    }
    return rows, metadata


def proxy_pivot_rows(candidate, proxy_F, proxy_H, proxy_powers):
    rows, metadata = reduced_rows(candidate, proxy_F, proxy_H, proxy_powers)
    total_vars = metadata["compressed_variables"]
    if total_vars == 0:
        return [], 0, metadata
    matrix = Matrix(proxy_F, rows, ncols=total_vars)
    pivot_rows = list(matrix.transpose().pivots())
    proxy_rank = len(pivot_rows)
    return pivot_rows[:total_vars], proxy_rank, metadata


def exact_minor_result(candidate, exact_F, exact_H, exact_powers, proxy_F, proxy_H, proxy_powers, selection_reason):
    pivot_rows, proxy_rank, proxy_metadata = proxy_pivot_rows(candidate, proxy_F, proxy_H, proxy_powers)
    exact_rows, exact_metadata = reduced_rows(candidate, exact_F, exact_H, exact_powers)
    total_vars = exact_metadata["compressed_variables"]
    assert total_vars == proxy_metadata["compressed_variables"]

    exact_minor_rank = None
    exact_nullity = None
    status = "DEFERRED_PROXY_NOT_FULL_COLUMN_RANK"
    if proxy_rank >= total_vars and len(pivot_rows) == total_vars:
        minor_rows = [exact_rows[row_idx] for row_idx in pivot_rows]
        minor = Matrix(exact_F, minor_rows, ncols=total_vars)
        exact_minor_rank = int(minor.rank())
        exact_nullity = int(total_vars - exact_minor_rank)
        status = "EXACT_MINOR_FULL_RANK" if exact_nullity == 0 else "EXACT_MINOR_SINGULAR"

    summary = candidate["summary"]
    return {
        "candidate_id": candidate["candidate_id"],
        "family": candidate["family"],
        "selection_reason": selection_reason,
        "support_sizes": summary["support_sizes"],
        "min_support_size": summary["min_support_size"],
        "max_pair_intersection": summary["max_pair_intersection"],
        "min_pair_intersection": summary["min_pair_intersection"],
        "pairs_at_255": summary["pairs_at_255"],
        "pairs_at_or_above_250": summary["pairs_at_or_above_250"],
        "pairs_at_or_above_245": summary["pairs_at_or_above_245"],
        "pair_boundary_score": summary["pair_boundary_score"],
        "membership_histogram": summary["membership_histogram"],
        "target_clique": candidate["target_clique"],
        "boundary_five_count": candidate["boundary_five_count"],
        "boundary_size": candidate["boundary_size"],
        "quotient_fiber_profile_hash": candidate["quotient_fiber_profile_hash"],
        "compressed_variables": total_vars,
        "remaining_equations": exact_metadata["remaining_equations"],
        "anchor_zero_counts": exact_metadata["anchor_zero_counts"],
        "row_type_counts": exact_metadata["row_type_counts"],
        "row_descriptor_hash": exact_metadata["row_descriptor_hash"],
        "proxy_pivot_rank": proxy_rank,
        "proxy_pivot_rows_count": len(pivot_rows),
        "proxy_pivot_rows_hash": hash_payload(pivot_rows),
        "exact_minor_rank": exact_minor_rank,
        "exact_nullity": exact_nullity,
        "non_diagonal_solution_found": False,
        "agreement_verified": False,
        "certificate_type": "PROXY_SELECTED_EXACT_MINOR_RANK",
        "status": status,
    }


def source_metadata():
    if not SOURCE_DATA_PATH.exists():
        return None
    with SOURCE_DATA_PATH.open() as handle:
        source = json.load(handle)
    return {
        "source_json": str(SOURCE_DATA_PATH),
        "source_candidate_count": source["candidate_count"],
        "source_candidate_design_hash": source["candidate_design_hash"],
        "source_proof_status": source["proof_status"],
        "source_proxy_positive_count": source["rank_gate"]["proxy_positive_count"],
        "source_retained_proxy_count": source["rank_gate"]["retained_proxy_count"],
    }


def exact_record():
    scanner = load_scanner()
    candidates = scanner.candidate_designs()
    by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    q, exact_F, exact_H = field_context_exact()
    exact_powers = precompute_powers(exact_F, exact_H)
    proxy_F, proxy_H = field_context_proxy()
    proxy_powers = precompute_powers(proxy_F, proxy_H)

    results = []
    for selection in AUDIT_SELECTION:
        candidate_id = selection["candidate_id"]
        if candidate_id not in by_id:
            raise KeyError(candidate_id)
        results.append(
            exact_minor_result(
                by_id[candidate_id],
                exact_F,
                exact_H,
                exact_powers,
                proxy_F,
                proxy_H,
                proxy_powers,
                selection["reason"],
            )
        )

    certified_count = sum(1 for row in results if row["status"] == "EXACT_MINOR_FULL_RANK")
    singular_count = sum(1 for row in results if row["status"] == "EXACT_MINOR_SINGULAR")
    proof_status = "CANDIDATE" if singular_count else "ROUTE_CUT_TESTED_CANDIDATES"
    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "valueclass_boundary_exact_audit",
        "source": source_metadata(),
        "candidate_count": len(candidates),
        "exact_audited_count": len(results),
        "selection": AUDIT_SELECTION,
        "proxy_field": "GF(12289)",
        "exact_field": "GF(17^32)",
        "field_denominator": str(q),
        "subgroup_order": len(exact_H),
        "degree_bound": K,
        "results": results,
        "result_hash": hash_payload(results),
        "exact_minor_full_rank_count": certified_count,
        "exact_minor_singular_count": singular_count,
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list certificate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "improvement over PR #133",
        ],
    }
    return jsonable(record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    args = parser.parse_args()

    record = exact_record()
    if record["proof_status"] == "ROUTE_CUT_TESTED_CANDIDATES":
        assert record["exact_minor_singular_count"] == 0

    if args.write_json:
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_VALUECLASS_BOUNDARY_EXACT_AUDIT_OK")
        print("exact_audited_count: %d" % record["exact_audited_count"])
        print("exact_minor_full_rank_count: %d" % record["exact_minor_full_rank_count"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
