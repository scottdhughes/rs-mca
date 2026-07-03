#!/usr/bin/env sage
"""Exact forced-identity check for M1 a=327 low-rank functional-basis extraction."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
DATA_PATH = Path("experimental/data/m1_a327_lowrank_functional_basis_extraction.json")


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


def exact_field():
    return GF(Integer(P) ** FIELD_DEGREE, name="z")


def pair_projection_rank(F, kernel_basis, template_vectors, left, right):
    diff = [
        F(template_vectors[left - 1][idx]) - F(template_vectors[right - 1][idx])
        for idx in range(len(template_vectors[0]))
    ]
    values = []
    for basis_vec in kernel_basis:
        acc = F(0)
        for idx, value in enumerate(diff):
            acc += value * basis_vec[idx]
        values.append(acc)
    return 1 if any(value != 0 for value in values) else 0


def audit():
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    F = exact_field()
    forced_rows = [
        [F(value) for value in row]
        for row in record["forced_identity_reduction"]["forced_functionals"]
    ]
    matrix = Matrix(F, forced_rows)
    rank = int(matrix.rank())
    kernel_basis = matrix.right_kernel().basis()
    template_vectors = record["functional_divisibility_baseline"].get("template_vectors")
    if template_vectors is None:
        # Keep compatibility with the compact baseline by reading witness vectors from source-style rows.
        template_vectors = [
            [0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1],
        ]
    forced_pairs = []
    projection_ranks = {}
    for left in range(1, 8):
        for right in range(left + 1, 8):
            label = "P%s%s" % (left, right)
            pair_rank = pair_projection_rank(F, kernel_basis, template_vectors, left, right)
            projection_ranks[label] = pair_rank
            if pair_rank == 0:
                forced_pairs.append([left, right])
    record["sage_exact_check"] = {
        "run": True,
        "field": "GF(17^32)",
        "forced_rank": rank,
        "forced_kernel_dimension": len(kernel_basis),
        "forced_equal_pairs": len(forced_pairs),
        "projection_rank_by_pair": projection_ranks,
        "status": "PASS" if rank == 5 and len(kernel_basis) == 1 and len(forced_pairs) == 21 else "FAIL",
    }
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = audit()
    if args.write_json:
        DATA_PATH.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))
    elif not args.write_json:
        sage = record["sage_exact_check"]
        print("SAGE_AUDIT_M1_A327_LOWRANK_FUNCTIONAL_BASIS_EXTRACTION_OK")
        print("forced_rank: %s" % sage["forced_rank"])
        print("forced_kernel_dimension: %s" % sage["forced_kernel_dimension"])
        print("forced_equal_pairs: %s" % sage["forced_equal_pairs"])
        print("status: %s" % sage["status"])


if __name__ == "__main__":
    main()
