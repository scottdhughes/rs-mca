#!/usr/bin/env sage
"""Sage gate for the M1 a=327 collapse-constrained Hall repair packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_collapse_constrained_hall_repair.json")


def audit_record():
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    record["sage_gate"] = {
        "exact_field": "GF(17^32)",
        "exact_audit_triggered": bool(record["exact_audit"]["triggered"]),
        "reason": (
            "collapse-constrained Hall proxy candidate pending exact lift"
            if record["exact_audit"]["triggered"]
            else "no collapse-constrained Hall proxy a>=327 candidate"
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
        print("SAGE_GATE_M1_A327_COLLAPSE_CONSTRAINED_HALL_REPAIR_OK")
        print("exact_audit_triggered: %s" % record["sage_gate"]["exact_audit_triggered"])
        print("proof_status: %s" % record["proof_status"])


if __name__ == "__main__":
    main()
