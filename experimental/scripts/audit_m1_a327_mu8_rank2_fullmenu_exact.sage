#!/usr/bin/env sage
"""Exact interpolation audit for rank-2 mu_8 full-menu ablation candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


BASE_SCRIPT = Path("experimental/scripts/audit_m1_a327_mu8_rank2_cpsat_exact.sage")
SCHEDULE_INPUT = Path("experimental/data/m1_a327_mu8_rank2_fullmenu_schedule_candidates.json")
EXACT_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_fullmenu_exact_interpolation.json")
WITNESS_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_fullmenu_witness_audit.json")

ns = dict(globals())
ns["__name__"] = "rank2_fullmenu_base"
exec(compile(BASE_SCRIPT.read_text(), str(BASE_SCRIPT), "exec"), ns)

TARGET = ns["TARGET_AGREEMENT"]
NOT_CLAIMED = ns["NOT_CLAIMED"]


def jsonable(payload):
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    try:
        from numbers import Integral

        if isinstance(payload, Integral):
            return int(payload)
    except Exception:
        pass
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return str(payload)


def audit_exact(candidate_limit):
    with SCHEDULE_INPUT.open() as handle:
        schedule = json.load(handle)
    candidates = [row for row in schedule["candidates"] if row.get("guard_pass")][:candidate_limit]
    exact_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": "46a0755",
        "exact_interpolation": {
            "field": "GF(17^32)",
            "systems_tested": 0,
            "positive_nullity_systems": 0,
            "pair_visible_systems": 0,
            "best_nullity": 0,
            "best_failure_mode": (
                "MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE"
                if not candidates
                else "MU8_RANK2_CARRIER_EXACT_AUDIT_NOT_IMPLEMENTED_FOR_GUARD_CANDIDATE"
            ),
        },
        "systems": [],
        "proof_status": (
            "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE / PARTIAL / EXPERIMENTAL"
            if not candidates
            else "CANDIDATE / MU8_RANK2_CARRIER_EXACT_AUDIT_PENDING / PARTIAL / EXPERIMENTAL"
        ),
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    witness_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": "46a0755",
        "witness_audit": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "min_agreement": None,
            "status": "NO_EXACT_WITNESS_CONSTRUCTED",
        },
        "proof_status": "EXACT_EXTRACTION_NO_A327 / NO_EXACT_WITNESS_CONSTRUCTED / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    return exact_record, witness_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--candidate-limit", type=int, default=32)
    args = parser.parse_args()
    exact_record, witness_record = audit_exact(args.candidate_limit)
    if args.write_json:
        EXACT_OUTPUT.write_text(json.dumps(jsonable(exact_record), indent=2, sort_keys=True) + "\n")
        WITNESS_OUTPUT.write_text(json.dumps(jsonable(witness_record), indent=2, sort_keys=True) + "\n")
    summary = {
        "exact_status": exact_record["proof_status"],
        "witness_status": witness_record["proof_status"],
        "systems_tested": exact_record["exact_interpolation"]["systems_tested"],
        "best_nullity": exact_record["exact_interpolation"]["best_nullity"],
    }
    if args.json:
        print(json.dumps(jsonable(summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_MU8_RANK2_FULLMENU_EXACT_READY")


if __name__ == "__main__":
    main()
