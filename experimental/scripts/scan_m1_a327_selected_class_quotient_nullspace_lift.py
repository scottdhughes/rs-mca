#!/usr/bin/env python3
"""Prepare the quotient-nullspace lift target for M1 a=327 selected classes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "9fcdb02"
SOURCE_DATA = Path("experimental/data/m1_a327_selected_class_thin_exact_lift.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_selected_class_quotient_nullspace_lift.json")

N = 512
LIST_SIZE = 7
K = 256
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
QUOTIENT_VARIABLES = (LIST_SIZE - 1) * K
PAIR7_PAIR_LABELS = ["P17", "P27", "P37", "P47", "P57"]
PAIR_INDICES = [(i, j) for i in range(LIST_SIZE) for j in range(i + 1, LIST_SIZE)]
PAIR_LABELS = [f"P{i + 1}{j + 1}" for i, j in PAIR_INDICES]


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def pair_counts(coordinate_classes: list[dict[str, Any]]) -> dict[str, int]:
    counts = {label: 0 for label in PAIR_LABELS}
    for row in coordinate_classes:
        members = {int(value) - 1 for value in row["members"]}
        for label, (left, right) in zip(PAIR_LABELS, PAIR_INDICES, strict=True):
            if left in members and right in members:
                counts[label] += 1
    return counts


def support_counts(coordinate_classes: list[dict[str, Any]]) -> list[int]:
    supports = [0] * LIST_SIZE
    for row in coordinate_classes:
        for witness in row["members"]:
            supports[int(witness) - 1] += 1
    return supports


def class_size_counts(coordinate_classes: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in coordinate_classes:
        key = str(int(row["size"]))
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: int(item[0])))


def anchored_classes(coordinate_classes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    anchored = []
    for row in coordinate_classes:
        members = [int(value) for value in row["members"]]
        anchor = min(members)
        anchored.append(
            {
                "position": int(row["position"]),
                "fiber": int(row["fiber"]),
                "members": members,
                "anchor": anchor,
                "equation_count": len(members) - 1,
            }
        )
    return anchored


def build_record() -> dict[str, Any]:
    source = load_source()
    thin = source["thin_hypergraph"]
    coordinate_classes = thin["best_coordinate_classes"]
    supports = support_counts(coordinate_classes)
    pairs = pair_counts(coordinate_classes)
    pair7_counts = [pairs[label] for label in PAIR7_PAIR_LABELS]
    selected_incidences = sum(int(row["size"]) for row in coordinate_classes)
    equations = selected_incidences - len(coordinate_classes)
    anchored = anchored_classes(coordinate_classes)

    record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "thin_selected_hypergraph": {
            "supports": supports,
            "selected_incidences": selected_incidences,
            "max_pair_count": max(pairs.values()),
            "pair_counts": pairs,
            "pair7_counts": pair7_counts,
            "pair_B_values": [N + value for value in pair7_counts],
            "selected_class_size_counts": class_size_counts(coordinate_classes),
            "coordinate_classes_hash": thin["best_coordinate_classes_hash"],
            "coordinate_classes": coordinate_classes,
            "anchored_classes_hash": hash_payload(anchored),
            "anchored_classes": anchored,
        },
        "quotient_system": {
            "variables": QUOTIENT_VARIABLES,
            "equations": equations,
            "matrix_shape": [equations, QUOTIENT_VARIABLES],
            "rank": None,
            "nullity": None,
            "field": None,
            "field_denominator": None,
            "H_order": None,
            "degree_bound": K,
            "full_system_attempted": False,
            "prefix_rank_results": [],
            "best_failure_mode": None,
        },
        "pair_projection_test": {
            "pairs_tested": 21,
            "forced_equal_pairs": [],
            "projection_results": [],
            "min_projection_rank": None,
        },
        "exact_candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "exact_max_min": None,
            "received_word_hash": None,
            "codeword_hashes": None,
            "vector_hash": None,
        },
        "proof_status": "CANDIDATE / EXACT_SOLVE_PENDING / PARTIAL / EXPERIMENTAL",
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
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        summary = {
            "status": record["proof_status"],
            "supports": record["thin_selected_hypergraph"]["supports"],
            "selected_incidences": record["thin_selected_hypergraph"]["selected_incidences"],
            "max_pair_count": record["thin_selected_hypergraph"]["max_pair_count"],
            "pair7_counts": record["thin_selected_hypergraph"]["pair7_counts"],
            "matrix_shape": record["quotient_system"]["matrix_shape"],
        }
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_SELECTED_CLASS_QUOTIENT_NULLSPACE_LIFT_READY")


if __name__ == "__main__":
    main()
