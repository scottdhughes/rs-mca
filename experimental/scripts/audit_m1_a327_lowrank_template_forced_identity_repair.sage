#!/usr/bin/env sage
"""Exact forced-identity sanity check for the low-rank repair survivor."""

from __future__ import annotations

import argparse
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
DATA_PATH = Path("experimental/data/m1_a327_lowrank_template_forced_identity_repair.json")


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


def audit():
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    F = exact_field()
    best = record["best_candidate"]
    forced = best["saturation"]["forced_functionals"]
    m = int(best["template_dimension"])
    matrix = Matrix(F, [[F(value) for value in row] for row in forced], ncols=m) if forced else Matrix(F, 0, m)
    rank = int(matrix.rank())
    kernel = matrix.right_kernel().basis()
    forced_pairs = []
    for left in range(1, 8):
        for right in range(left + 1, 8):
            diff = [
                F(best["template_vectors"][left - 1][idx]) - F(best["template_vectors"][right - 1][idx])
                for idx in range(m)
            ]
            values = []
            for basis_vec in kernel:
                acc = F(0)
                for idx, value in enumerate(diff):
                    acc += value * basis_vec[idx]
                values.append(acc)
            if not any(values):
                forced_pairs.append([left, right])
    record["sage_exact_check"] = {
        "run": True,
        "field": "GF(17^32)",
        "best_template_id": best["template_id"],
        "forced_rank": rank,
        "reduced_template_dimension": m - rank,
        "forced_equal_pairs": len(forced_pairs),
        "status": "PASS" if rank == 0 and m - rank == 6 and not forced_pairs else "FAIL",
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
        print("SAGE_AUDIT_M1_A327_LOWRANK_TEMPLATE_FORCED_IDENTITY_REPAIR_OK")
        print("best_template_id: %s" % sage["best_template_id"])
        print("forced_rank: %s" % sage["forced_rank"])
        print("reduced_template_dimension: %s" % sage["reduced_template_dimension"])
        print("forced_equal_pairs: %s" % sage["forced_equal_pairs"])
        print("status: %s" % sage["status"])


if __name__ == "__main__":
    main()
