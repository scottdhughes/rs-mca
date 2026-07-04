#!/usr/bin/env sage
"""Sage audit scaffold for the M1 a=327 quotient-subgroup realization search."""

import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_quotient_subgroup_realization_search.json")


def main():
    record = json.loads(DATA_PATH.read_text())
    candidate = record["candidate"]
    if not candidate["constructed"]:
        print(
            json.dumps(
                {
                    "status": "NOT_RUN",
                    "reason": "no exact quotient-polynomial candidate is present in the ledger",
                    "proof_status": record["proof_status"],
                    "proxy_failure_mode": record["proxy_realization"]["best_failure_mode"],
                    "field": "GF(17^32)",
                    "H_order": int(512),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    raise NotImplementedError("Exact candidate replay is intentionally gated until candidate data exists.")


if __name__ == "__main__":
    main()
