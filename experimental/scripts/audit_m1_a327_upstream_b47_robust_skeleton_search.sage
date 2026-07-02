#!/usr/bin/env sage
"""Sage-side JSON audit for the upstream B47 robust-skeleton ledger.

This is intentionally not an exact witness audit. The packet is an upstream
ledger seeded from already-recorded exact results, so the Sage-side check only
replays the machine-readable counts and non-claim boundary.
"""

import json
from pathlib import Path


DATA_PATH = Path("experimental/data/m1_a327_upstream_b47_robust_skeleton_search.json")


def main():
    record = json.loads(DATA_PATH.read_text())
    assert record["track"] == "INTERLEAVED_LIST"
    assert record["row"] == "RS[F_17^32,H,256]"
    assert record["denominator"] == "17^32"
    assert record["mca_counted"] is False
    search = record["upstream_b47_search"]
    assert search["systems_tested"] == 0
    assert search["exact_vectors_constructed"] == 0
    assert search["split_probe_vectors"] == 30
    assert search["split_resilient_skeletons"] == 0
    assert search["best_failure_mode"] == "UPSTREAM_B47_NOT_ROBUST"
    print("PASS: upstream B47 robust-skeleton JSON audit")


if __name__ == "__main__":
    main()
