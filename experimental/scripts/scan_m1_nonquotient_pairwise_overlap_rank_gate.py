#!/usr/bin/env python3
"""Emit the M1 non-quotient pairwise-overlap rank-gate checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_nonquotient_pairwise_overlap_rank_gate.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_BITS = 128
TARGET_AGREEMENT = 327
LIST_SIZE = 7
CURRENT_PR_133_AGREEMENT = 326
CURRENT_PR_133_LAMBDA_LOWER = 7

FIELD_DENOMINATOR = P**FIELD_DEGREE

SUPPORT_DESIGN = {
    "witness_support_sizes": [327, 327, 327, 327, 327, 327, 327],
    "pair_intersection_min": 142,
    "pair_intersection_max": 254,
    "pair_intersection_values": [
        142,
        142,
        142,
        142,
        148,
        149,
        149,
        175,
        175,
        180,
        181,
        182,
        188,
        215,
        220,
        246,
        246,
        253,
        253,
        254,
        254,
    ],
    "pair_intersections": {
        "0,1": 182,
        "0,2": 175,
        "0,3": 148,
        "0,4": 175,
        "0,5": 220,
        "0,6": 254,
        "1,2": 253,
        "1,3": 246,
        "1,4": 149,
        "1,5": 142,
        "1,6": 181,
        "2,3": 253,
        "2,4": 188,
        "2,5": 142,
        "2,6": 142,
        "3,4": 215,
        "3,5": 149,
        "3,6": 142,
        "4,5": 246,
        "4,6": 180,
        "5,6": 254,
    },
    "multiplicity_histogram": {"4": 271, "5": 241},
}

PAIRWISE_OVERLAP_RANK_GATE = {
    "field_denominator": str(FIELD_DENOMINATOR),
    "field_denominator_label": "17^32",
    "subgroup_order": N,
    "difference_variables": 6 * K,
    "compressed_variables": 382,
    "diagonal_vanish_equations": 1154,
    "remaining_pairwise_equations": 2882,
    "total_pairwise_overlap_equations": 4036,
    "vanish_intersections_with_anchor": {
        "1": 182,
        "2": 175,
        "3": 148,
        "4": 175,
        "5": 220,
        "6": 254,
    },
    "compressed_dimensions_by_witness": {
        "1": 74,
        "2": 81,
        "3": 108,
        "4": 81,
        "5": 36,
        "6": 2,
    },
    "remaining_equations_by_pair": {
        "1,2": 253,
        "1,3": 246,
        "1,4": 149,
        "1,5": 142,
        "1,6": 181,
        "2,3": 253,
        "2,4": 188,
        "2,5": 142,
        "2,6": 142,
        "3,4": 215,
        "3,5": 149,
        "3,6": 142,
        "4,5": 246,
        "4,6": 180,
        "5,6": 254,
    },
    "matrix_hash": "8ac5f55f37637dc3324f80ae4afd1240c58a760db1df84911e8ffb4f4bec34df",
    "rank": 382,
    "nullity": 0,
    "non_diagonal_solution_found": False,
    "explicit_witness_extracted": False,
    "status": "RANK_COMPUTED",
}


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def build_result() -> dict[str, Any]:
    assert threshold_floor() == 6
    assert SUPPORT_DESIGN["pair_intersection_max"] <= K - 1
    assert sum(SUPPORT_DESIGN["witness_support_sizes"]) == LIST_SIZE * TARGET_AGREEMENT
    assert sum(SUPPORT_DESIGN["pair_intersections"].values()) == 4036
    assert PAIRWISE_OVERLAP_RANK_GATE["compressed_variables"] == sum(
        PAIRWISE_OVERLAP_RANK_GATE["compressed_dimensions_by_witness"].values()
    )
    assert PAIRWISE_OVERLAP_RANK_GATE["rank"] == PAIRWISE_OVERLAP_RANK_GATE["compressed_variables"]
    assert PAIRWISE_OVERLAP_RANK_GATE["nullity"] == 0

    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "field_denominator": str(FIELD_DENOMINATOR),
        "field_denominator_label": "17^32",
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "target_agreement": TARGET_AGREEMENT,
        "baseline": {
            "current_pr_133_agreement": CURRENT_PR_133_AGREEMENT,
            "current_pr_133_lambda_lower": CURRENT_PR_133_LAMBDA_LOWER,
            "source": "PR #133 hybrid quotient-residual certificate",
        },
        "support_design": SUPPORT_DESIGN,
        "pairwise_overlap_rank_gate": PAIRWISE_OVERLAP_RANK_GATE,
        "interpretation": {
            "support_packing_blocks_a327": False,
            "pairwise_overlap_rank_decided": True,
            "support_design_interpolable": False,
            "candidate_found": False,
            "status": "ROUTE_CUT_SUPPORT_DESIGN",
        },
        "open_layers": {
            "rank_friendly_support_designs": True,
            "multi_core_nonquotient_families": True,
            "non_quotient_randomized_support_search": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_nonquotient_pairwise_overlap_rank_gate.sage",
            "recomputes_support_design": True,
            "constructs_GF_17_32": True,
            "uses_reduced_difference_system": True,
            "rank_mode": "compressed_pairwise_overlap",
            "optional_modes": ["--no-rank", "--rank-only", "--sample-nullspace", "--extract-witness"],
        },
        "repo_claim": {
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
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": "ROUTE_CUT_SUPPORT_DESIGN",
        },
        "status": "M1_NONQUOTIENT_PAIRWISE_OVERLAP_RANK_GATE_ROUTE_CUT",
    }
    result["record_hash"] = hash_payload(
        {
            "support_design": result["support_design"],
            "pairwise_overlap_rank_gate": result["pairwise_overlap_rank_gate"],
            "interpretation": result["interpretation"],
            "open": result["open_layers"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_result(), indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_result()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output)
        print(f"WROTE {args.output}")
        print("pairwise-overlap rank gate: rank 382 / nullity 0")
        print("status: ROUTE_CUT_SUPPORT_DESIGN")


if __name__ == "__main__":
    main()
