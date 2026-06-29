#!/usr/bin/env sage
"""Exact GF(17^32) audit wrapper for the balanced MILP target/codeword solver."""

from __future__ import annotations

import argparse
import hashlib
import json
from numbers import Integral
from pathlib import Path


P = 17
FIELD_DEGREE = 32
N = 512
K = 256
TARGET_AGREEMENT = 327
SCAN_DATA_PATH = Path("experimental/data/m1_a327_balanced_target_milp_codeword_solver.json")
DATA_PATH = Path("experimental/data/m1_a327_balanced_target_milp_codeword_solver_exact_audit.json")


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


def audit_record():
    with SCAN_DATA_PATH.open() as handle:
        source = json.load(handle)

    triggers = source["exact_audit_triggers"]
    if triggers:
        raise RuntimeError(
            "balanced target solver found proxy a>=327 triggers; "
            "implement explicit exact extraction before writing audit JSON"
        )

    q = Integer(P) ** FIELD_DEGREE
    return jsonable(
        {
            "track": "INTERLEAVED_LIST",
            "row": "RS[F_17^32,H,256]",
            "denominator": "17^32",
            "agreement_target": TARGET_AGREEMENT,
            "construction_mode": "balanced_target_milp_codeword_solver_exact_audit",
            "source": {
                "source_json": str(SCAN_DATA_PATH),
                "source_result_hash": source["result_hash"],
                "source_proof_status": source["proof_status"],
                "source_target_system_count": source["target_system_count"],
                "source_codeword_tuple_sample_count": source["codeword_tuple_sample_count"],
                "source_proxy_candidate_system_count": source["proxy_candidate_system_count"],
            },
            "exact_field": "GF(17^32)",
            "field_denominator": str(q),
            "subgroup_order": N,
            "degree_bound": K,
            "exact_trigger_count": len(triggers),
            "exact_audited_count": 0,
            "results": [],
            "result_hash": hash_payload([]),
            "proof_status": "NO_EXACT_AUDIT_TRIGGERED",
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
    if not args.json:
        print("SAGE_AUDIT_M1_A327_BALANCED_TARGET_MILP_CODEWORD_SOLVER_OK")
        print(f"exact_trigger_count: {record['exact_trigger_count']}")
        print(f"proof_status: {record['proof_status']}")


if __name__ == "__main__":
    main()
