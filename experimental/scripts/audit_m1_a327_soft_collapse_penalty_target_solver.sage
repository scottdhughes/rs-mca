#!/usr/bin/env sage
"""Sage gate for the M1 a=327 soft collapse-penalty target solver packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_soft_collapse_penalty_target_solver.json")


def audit_record():
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    # This packet is a proxy target-selection search. Exact GF(17^32)
    # reconstruction is intentionally gated on a collapse-reduced proxy
    # candidate, and no exact witness is claimed here.
    reduced = int(record["soft_collapse_search"]["collapse_reduced_proxy_candidates"])
    record["sage_gate"] = {
        "exact_field": "GF(17^32)",
        "exact_audit_triggered": bool(reduced),
        "reason": (
            "collapse-reduced proxy candidate needs exact lift"
            if reduced
            else "no collapse-reduced proxy a>=327 candidate"
        ),
    }
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = audit_record()
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print("SAGE_GATE_M1_A327_SOFT_COLLAPSE_PENALTY_TARGET_SOLVER_OK")
        print("exact_audit_triggered: %s" % record["sage_gate"]["exact_audit_triggered"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
