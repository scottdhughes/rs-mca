#!/usr/bin/env python3
"""Verify the M1 non-quotient pairwise-overlap rank-gate checkpoint."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DATA_PATH = Path("experimental/data/m1_nonquotient_pairwise_overlap_rank_gate.json")


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def verify_record(record: dict[str, Any]) -> None:
    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert record["n"] == 512
    assert record["k"] == 256
    assert int(record["field_denominator"]) == 17**32
    assert record["field_denominator_label"] == "17^32"
    assert record["target_bits"] == 128
    assert record["threshold_floor"] == 6
    assert record["minimum_to_clear"] == 7
    assert 6 * 2**128 < 17**32 < 7 * 2**128
    assert record["target_agreement"] == 327
    assert record["baseline"] == {
        "current_pr_133_agreement": 326,
        "current_pr_133_lambda_lower": 7,
        "source": "PR #133 hybrid quotient-residual certificate",
    }

    support = record["support_design"]
    assert support["witness_support_sizes"] == [327] * 7
    assert sum(support["witness_support_sizes"]) == 7 * 327
    assert support["pair_intersection_min"] == 142
    assert support["pair_intersection_max"] == 254
    assert support["pair_intersection_max"] <= 255
    assert len(support["pair_intersection_values"]) == 21
    assert sorted(support["pair_intersections"].values()) == support["pair_intersection_values"]
    assert sum(support["pair_intersections"].values()) == 4036
    assert support["multiplicity_histogram"] == {"4": 271, "5": 241}
    assert 271 * 4 + 241 * 5 == 7 * 327

    gate = record["pairwise_overlap_rank_gate"]
    assert gate["field_denominator"] == str(17**32)
    assert gate["field_denominator_label"] == "17^32"
    assert gate["subgroup_order"] == 512
    assert gate["difference_variables"] == 6 * 256
    assert gate["compressed_variables"] == 382
    assert gate["diagonal_vanish_equations"] == 1154
    assert gate["remaining_pairwise_equations"] == 2882
    assert gate["total_pairwise_overlap_equations"] == 4036
    assert gate["diagonal_vanish_equations"] + gate["remaining_pairwise_equations"] == 4036
    assert gate["vanish_intersections_with_anchor"] == {
        "1": 182,
        "2": 175,
        "3": 148,
        "4": 175,
        "5": 220,
        "6": 254,
    }
    assert gate["compressed_dimensions_by_witness"] == {
        "1": 74,
        "2": 81,
        "3": 108,
        "4": 81,
        "5": 36,
        "6": 2,
    }
    assert sum(gate["compressed_dimensions_by_witness"].values()) == gate["compressed_variables"]
    assert gate["remaining_equations_by_pair"] == {
        key: value
        for key, value in support["pair_intersections"].items()
        if not key.startswith("0,")
    }
    assert sum(gate["remaining_equations_by_pair"].values()) == gate["remaining_pairwise_equations"]
    assert gate["matrix_hash"] == "8ac5f55f37637dc3324f80ae4afd1240c58a760db1df84911e8ffb4f4bec34df"
    assert gate["rank"] == 382
    assert gate["rank"] == gate["compressed_variables"]
    assert gate["nullity"] == 0
    assert gate["non_diagonal_solution_found"] is False
    assert gate["explicit_witness_extracted"] is False
    assert gate["status"] == "RANK_COMPUTED"

    assert record["interpretation"] == {
        "support_packing_blocks_a327": False,
        "pairwise_overlap_rank_decided": True,
        "support_design_interpolable": False,
        "candidate_found": False,
        "status": "ROUTE_CUT_SUPPORT_DESIGN",
    }
    assert record["open_layers"] == {
        "rank_friendly_support_designs": True,
        "multi_core_nonquotient_families": True,
        "non_quotient_randomized_support_search": True,
        "global_Lambda_mu_327_upper_bound": True,
        "status": "PARTIAL",
    }
    assert record["sage_audit"]["uses_reduced_difference_system"] is True
    assert record["repo_claim"]["mca_counted"] is False
    assert "global Lambda_mu(C,327) <= 6" in record["repo_claim"]["not_claimed"]
    assert "improvement over PR #133" in record["repo_claim"]["not_claimed"]
    assert record["global_status"] == {
        "candidate_found": False,
        "improves_pr_133": False,
        "status": "ROUTE_CUT_SUPPORT_DESIGN",
    }
    assert record["status"] == "M1_NONQUOTIENT_PAIRWISE_OVERLAP_RANK_GATE_ROUTE_CUT"

    expected_hash = hash_payload(
        {
            "support_design": record["support_design"],
            "pairwise_overlap_rank_gate": record["pairwise_overlap_rank_gate"],
            "interpretation": record["interpretation"],
            "open": record["open_layers"],
            "global": record["global_status"],
        }
    )
    assert record["record_hash"] == expected_hash


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    record = json.loads(DATA_PATH.read_text())
    verify_record(record)
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print("PASS")
        print("rank 382 on 382 compressed variables")
        print("support design route cut; no a=327 candidate claimed")


if __name__ == "__main__":
    main()
