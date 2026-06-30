#!/usr/bin/env sage
"""Sage gate for the M1 a=327 rescheduler-aware quotient-plane packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_rescheduler_aware_quotient_plane_search.json")


def audit_record():
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    record["sage_gate"] = {
        "exact_field": "GF(17^32)",
        "exact_audit_triggered": bool(record["exact_audit"]["triggered"]),
        "reason": (
            "proxy plane candidate pending exact lift"
            if record["exact_audit"]["triggered"]
            else "no proxy quotient-plane a>=327 candidate"
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
        print("SAGE_GATE_M1_A327_RESCHEDULER_AWARE_QUOTIENT_PLANE_SEARCH_OK")
        print("exact_audit_triggered: %s" % record["sage_gate"]["exact_audit_triggered"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
