#!/usr/bin/env sage
"""Proxy and exact rank audit for MILP-generated M1 a=327 value-class seeds."""

from __future__ import annotations

import argparse
import hashlib
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
SCAN_DATA_PATH = Path("experimental/data/m1_a327_valueclass_milp_incidence_seeds.json")
DATA_PATH = Path("experimental/data/m1_a327_valueclass_milp_incidence_seeds_rank_audit.json")

EXACT_SELECTION = {
    "all_sizes_max_pairs_at255_block",
    "all_sizes_max_pairs_at255_bit_reversal",
    "all_sizes_max_pairs_at255_fiber_round_robin",
    "all_sizes_min_anchor_variables_block",
    "sizes_3_7_max_pairs_at255_block",
    "sizes_3_7_max_pairs_at255_fiber_round_robin",
    "sizes_3_6_max_pairs_at255_block",
    "sizes_4_5_max_pairs_at255_block",
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


def proxy_rank_result(candidate, proxy_F, proxy_H, proxy_powers):
    rows, metadata = reduced_rows(candidate, proxy_F, proxy_H, proxy_powers)
    total_vars = metadata["compressed_variables"]
    if total_vars == 0:
        rank = 0
        pivots = []
    else:
        matrix = Matrix(proxy_F, rows, ncols=total_vars)
        rank = int(matrix.rank())
        pivots = list(matrix.transpose().pivots())
    return {
        "proxy_rank": rank,
        "proxy_nullity": int(total_vars - rank),
        "proxy_pivot_rows": pivots[:total_vars],
        "proxy_metadata": metadata,
    }


def exact_minor_result(candidate, proxy_result, exact_F, exact_H, exact_powers):
    exact_rows, exact_metadata = reduced_rows(candidate, exact_F, exact_H, exact_powers)
    total_vars = exact_metadata["compressed_variables"]
    exact_minor_rank = None
    exact_nullity = None
    status = "EXACT_NOT_SELECTED"
    if candidate["candidate_id"] in EXACT_SELECTION:
        pivot_rows = proxy_result["proxy_pivot_rows"]
        if proxy_result["proxy_rank"] >= total_vars and len(pivot_rows) == total_vars:
            minor_rows = [exact_rows[row_idx] for row_idx in pivot_rows]
            minor = Matrix(exact_F, minor_rows, ncols=total_vars)
            exact_minor_rank = int(minor.rank())
            exact_nullity = int(total_vars - exact_minor_rank)
            status = "EXACT_MINOR_FULL_RANK" if exact_nullity == 0 else "EXACT_MINOR_SINGULAR"
        else:
            status = "DEFERRED_PROXY_NOT_FULL_COLUMN_RANK"
    return {
        "exact_metadata": exact_metadata,
        "exact_minor_rank": exact_minor_rank,
        "exact_nullity": exact_nullity,
        "status": status,
    }


def audit_record():
    with SCAN_DATA_PATH.open() as handle:
        source = json.load(handle)
    candidates = source["candidates"]
    q, exact_F, exact_H = field_context_exact()
    exact_powers = precompute_powers(exact_F, exact_H)
    proxy_F, proxy_H = field_context_proxy()
    proxy_powers = precompute_powers(proxy_F, proxy_H)

    results = []
    for candidate in candidates:
        proxy_result = proxy_rank_result(candidate, proxy_F, proxy_H, proxy_powers)
        exact_result = exact_minor_result(candidate, proxy_result, exact_F, exact_H, exact_powers)
        summary = candidate["summary"]
        metadata = exact_result["exact_metadata"]
        results.append(
            {
                "candidate_id": candidate["candidate_id"],
                "profile_id": candidate["profile_id"],
                "embedding": candidate["embedding"],
                "support_sizes": summary["support_sizes"],
                "max_pair_intersection": summary["max_pair_intersection"],
                "min_pair_intersection": summary["min_pair_intersection"],
                "pairs_at_255": summary["pairs_at_255"],
                "pairs_at_or_above_250": summary["pairs_at_or_above_250"],
                "pairs_at_or_above_245": summary["pairs_at_or_above_245"],
                "pair_intersection_sum": summary["pair_intersection_sum"],
                "membership_histogram": summary["membership_histogram"],
                "anchor_compressed_variables": summary["anchor_compressed_variables"],
                "compressed_variables": metadata["compressed_variables"],
                "remaining_equations": metadata["remaining_equations"],
                "anchor_zero_counts": metadata["anchor_zero_counts"],
                "row_type_counts": metadata["row_type_counts"],
                "row_descriptor_hash": metadata["row_descriptor_hash"],
                "proxy_rank": proxy_result["proxy_rank"],
                "proxy_nullity": proxy_result["proxy_nullity"],
                "proxy_pivot_rows_count": len(proxy_result["proxy_pivot_rows"]),
                "proxy_pivot_rows_hash": hash_payload(proxy_result["proxy_pivot_rows"]),
                "exact_selected": candidate["candidate_id"] in EXACT_SELECTION,
                "exact_minor_rank": exact_result["exact_minor_rank"],
                "exact_nullity": exact_result["exact_nullity"],
                "non_diagonal_solution_found": False,
                "agreement_verified": False,
                "certificate_type": "PROXY_SELECTED_EXACT_MINOR_RANK",
                "status": exact_result["status"],
            }
        )

    proxy_positive_count = sum(1 for row in results if row["proxy_nullity"] > 0)
    exact_selected_count = sum(1 for row in results if row["exact_selected"])
    exact_full_rank_count = sum(1 for row in results if row["status"] == "EXACT_MINOR_FULL_RANK")
    exact_singular_count = sum(1 for row in results if row["status"] == "EXACT_MINOR_SINGULAR")
    proof_status = "CANDIDATE" if proxy_positive_count or exact_singular_count else "ROUTE_CUT_TESTED_CANDIDATES"
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "valueclass_milp_incidence_seed_rank_audit",
            "source": {
                "source_json": str(SCAN_DATA_PATH),
                "source_candidate_count": source["candidate_count"],
                "source_candidate_design_hash": source["candidate_design_hash"],
                "source_proof_status": source["proof_status"],
            },
            "candidate_count": len(candidates),
            "profile_count": len(source["profiles"]),
            "proxy_field": "GF(12289)",
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(exact_H),
            "degree_bound": K,
            "results": results,
            "result_hash": hash_payload(results),
            "proxy_positive_count": proxy_positive_count,
            "exact_selected_count": exact_selected_count,
            "exact_minor_full_rank_count": exact_full_rank_count,
            "exact_minor_singular_count": exact_singular_count,
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
        print("SAGE_AUDIT_M1_A327_VALUECLASS_MILP_INCIDENCE_SEEDS_OK")
        print("candidate_count: %d" % record["candidate_count"])
        print("proxy_positive_count: %d" % record["proxy_positive_count"])
        print("exact_selected_count: %d" % record["exact_selected_count"])
        print("exact_minor_full_rank_count: %d" % record["exact_minor_full_rank_count"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
