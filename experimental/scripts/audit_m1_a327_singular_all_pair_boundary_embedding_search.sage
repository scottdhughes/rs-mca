#!/usr/bin/env sage
"""Exact GF(17^32) audit for selected all-pair-boundary embeddings."""

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
SCAN_DATA_PATH = Path("experimental/data/m1_a327_singular_all_pair_boundary_embedding_search.json")
DATA_PATH = Path("experimental/data/m1_a327_singular_all_pair_boundary_embedding_search_exact_audit.json")
SCANNER_PATH = Path("experimental/scripts/scan_m1_a327_singular_all_pair_boundary_embedding_search.py")

EXACT_SELECTION = {
    "all_pair_boundary_block",
    "all_pair_boundary_bit_reversal",
    "all_pair_boundary_fiber_round_robin",
    "all_pair_boundary_random_shuffle_0000",
    "all_pair_boundary_random_shuffle_0001",
    "all_pair_boundary_random_shuffle_0017",
    "all_pair_boundary_random_shuffle_0064",
    "all_pair_boundary_random_shuffle_0255",
    "all_pair_boundary_random_shuffle_0511",
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


def load_scanner():
    spec = importlib.util.spec_from_file_location("singular_all_pair_boundary_scanner", SCANNER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def field_context_exact():
    q = Integer(P) ** FIELD_DEGREE
    F = GF(q, name="z")
    generator = F.multiplicative_generator()
    subgroup_generator = generator ** ((q - 1) // N)
    H = [subgroup_generator**idx for idx in range(N)]
    assert len(set(H)) == N
    assert subgroup_generator**N == 1
    return q, F, H


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


def reduced_rows(candidate, F, H):
    masks = candidate["membership_masks"]
    locator_by_witness = {}
    anchor_zero_counts = {}
    for witness in range(1, LIST_SIZE):
        zero_positions = [
            pos
            for pos, mask in enumerate(masks)
            if bit(mask, 0) and bit(mask, witness)
        ]
        anchor_zero_counts[str(witness)] = len(zero_positions)
        locator_by_witness[witness] = locator_values(F, H, zero_positions)

    rows = []
    row_type_counts = {}
    row_descriptors = []
    for left, right in itertools.combinations(range(1, LIST_SIZE), 2):
        for pos, mask in enumerate(masks):
            if not (bit(mask, left) and bit(mask, right)):
                continue
            left_value = locator_by_witness[left][pos]
            right_value = locator_by_witness[right][pos]
            if left_value == 0 and right_value == 0:
                continue
            row = [F(0)] * (LIST_SIZE - 1)
            row[left - 1] = left_value
            row[right - 1] = -right_value
            rows.append(row)
            pair_label = f"{left},{right}"
            row_type_counts[pair_label] = row_type_counts.get(pair_label, 0) + 1
            row_descriptors.append({"pair": pair_label, "coordinate": pos})
    return rows, {
        "anchor_zero_counts": anchor_zero_counts,
        "compressed_variables": LIST_SIZE - 1,
        "remaining_equations": len(rows),
        "row_type_counts": dict(sorted(row_type_counts.items())),
        "row_descriptor_hash": hash_payload(row_descriptors),
    }


def exact_result(candidate, F, H):
    rows, metadata = reduced_rows(candidate, F, H)
    matrix = Matrix(F, rows, ncols=LIST_SIZE - 1)
    rank = int(matrix.rank())
    nullity = LIST_SIZE - 1 - rank
    pivots = list(matrix.transpose().pivots())
    return {
        "candidate_id": candidate["candidate_id"],
        "embedding_id": candidate["embedding_id"],
        "embedding_family": candidate["embedding_family"],
        "seed": candidate["seed"],
        "membership_mask_hash": candidate["membership_mask_hash"],
        "support_sizes": candidate["summary"]["support_sizes"],
        "membership_histogram": candidate["summary"]["membership_histogram"],
        "pairs_at_255": candidate["summary"]["pairs_at_255"],
        "proxy_rank": candidate["proxy_rank"],
        "proxy_nullity": candidate["proxy_nullity"],
        "compressed_variables": metadata["compressed_variables"],
        "remaining_equations": metadata["remaining_equations"],
        "anchor_zero_counts": metadata["anchor_zero_counts"],
        "row_type_counts": metadata["row_type_counts"],
        "row_descriptor_hash": metadata["row_descriptor_hash"],
        "exact_rank": rank,
        "exact_nullity": nullity,
        "exact_pivot_rows_count": len(pivots),
        "exact_pivot_rows_hash": hash_payload(pivots),
        "non_diagonal_solution_found": False,
        "agreement_verified": False,
        "status": "EXACT_FULL_RANK" if nullity == 0 else "EXACT_POSITIVE_NULLITY",
    }


def audit_record():
    with SCAN_DATA_PATH.open() as handle:
        source = json.load(handle)
    scanner = load_scanner()
    regenerated = []
    for candidate in scanner.candidate_embeddings():
        candidate_id = f"all_pair_boundary_{candidate['embedding_id']}"
        regenerated.append(
            {
                "candidate_id": candidate_id,
                "embedding_id": candidate["embedding_id"],
                "embedding_family": candidate["embedding_family"],
                "seed": candidate["seed"],
                "membership_masks": candidate["membership_masks"],
                "membership_mask_hash": scanner.hash_payload(candidate["membership_masks"]),
                "summary": scanner.summarize_masks(candidate["membership_masks"]),
            }
        )
    by_id = {candidate["candidate_id"]: candidate for candidate in regenerated}
    source_by_id = {candidate["candidate_id"]: candidate for candidate in source["results"]}
    q, F, H = field_context_exact()
    results = []
    for candidate_id in sorted(EXACT_SELECTION):
        if by_id[candidate_id]["membership_mask_hash"] != source_by_id[candidate_id]["membership_mask_hash"]:
            raise RuntimeError("regenerated membership mask hash mismatch for %s" % candidate_id)
        by_id[candidate_id]["proxy_rank"] = source_by_id[candidate_id]["proxy_rank"]
        by_id[candidate_id]["proxy_nullity"] = source_by_id[candidate_id]["proxy_nullity"]
        results.append(exact_result(by_id[candidate_id], F, H))

    full_rank_count = sum(1 for row in results if row["status"] == "EXACT_FULL_RANK")
    positive_nullity_count = sum(1 for row in results if row["status"] == "EXACT_POSITIVE_NULLITY")
    proof_status = "CANDIDATE" if positive_nullity_count else "ROUTE_CUT_TESTED_EMBEDDINGS"
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "singular_all_pair_boundary_embedding_exact_audit",
            "source": {
                "source_json": str(SCAN_DATA_PATH),
                "source_candidate_count": source["candidate_count"],
                "source_result_hash": source["result_hash"],
                "source_proof_status": source["proof_status"],
                "source_proxy_singular_count": source["proxy_singular_count"],
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": len(H),
            "degree_bound": K,
            "exact_audited_count": len(results),
            "results": results,
            "result_hash": hash_payload(results),
            "exact_full_rank_count": full_rank_count,
            "exact_positive_nullity_count": positive_nullity_count,
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
        print("SAGE_AUDIT_M1_A327_SINGULAR_ALL_PAIR_BOUNDARY_EMBEDDING_SEARCH_OK")
        print("exact_audited_count: %d" % record["exact_audited_count"])
        print("exact_full_rank_count: %d" % record["exact_full_rank_count"])
        print("exact_positive_nullity_count: %d" % record["exact_positive_nullity_count"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
