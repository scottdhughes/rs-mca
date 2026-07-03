#!/usr/bin/env sage
"""Audit the connected-subtree counting obstruction for M1 a=327."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_connected_subtree_selected_class_construction.json")

N = 512
LIST_SIZE = 7
TARGET_AGREEMENT = 327
PAIR_CAP = 255


def audit():
    with DATA_PATH.open() as handle:
        record = json.load(handle)
    obstruction = record["connected_subtree_design"]["counting_obstruction"]
    selected_lower = LIST_SIZE * TARGET_AGREEMENT
    edge_lower = selected_lower - N
    edge_upper = (LIST_SIZE - 1) * PAIR_CAP
    assert obstruction["support_selected_incidence_lower"] == selected_lower
    assert obstruction["tree_edge_incidence_lower"] == edge_lower
    assert obstruction["tree_edge_incidence_upper_from_pair_cap"] == edge_upper
    assert edge_lower > edge_upper
    record["exact_construction"].update(
        {
            "audit_run": True,
            "degree_bound_ok": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "best_failure_mode": "CONNECTED_SUBTREE_GLOBAL_COUNT_OBSTRUCTION",
        }
    )
    record["proof_status"] = (
        "CONSTRUCTION_FAIL / CONNECTED_SUBTREE_GLOBAL_COUNT_OBSTRUCTION / "
        "PARTIAL / EXPERIMENTAL"
    )
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = audit()
    if args.write_json:
        DATA_PATH.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(record, indent=2, sort_keys=True))
    elif not args.write_json:
        obstruction = record["connected_subtree_design"]["counting_obstruction"]
        print("SAGE_AUDIT_M1_A327_CONNECTED_SUBTREE_SELECTED_CLASS_CONSTRUCTION_OK")
        print("tree_edge_incidence_lower: %s" % obstruction["tree_edge_incidence_lower"])
        print("tree_edge_incidence_upper: %s" % obstruction["tree_edge_incidence_upper_from_pair_cap"])
        print("best_failure_mode: %s" % record["exact_construction"]["best_failure_mode"])


if __name__ == "__main__":
    main()
