#!/usr/bin/env python3
"""Verify the rank-3 mu_8 no-singleton-projective-key schedule audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_BROAD = Path("experimental/data/m1_a327_mu8_rank3_no_singleton_projective_key_schedule.json")
DEFAULT_FOCUSED = Path(
    "experimental/data/m1_a327_mu8_rank3_no_singleton_projective_key_blockkey001_schedule.json"
)
TARGET = 327
REQUIRED_TOTAL = 7 * TARGET
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def check_header(payload: dict[str, Any]) -> None:
    assert payload["track"] == "INTERLEAVED_LIST"
    assert payload["row"] == "RS[F_17^32,H,256]"
    assert payload["denominator"] == "17^32"
    assert payload["agreement_target"] == TARGET
    assert payload["mca_counted"] is False
    assert REQUIRED_NONCLAIMS.issubset(set(payload["not_claimed"]))


def check_no_singleton_flags(payload: dict[str, Any]) -> dict[str, Any]:
    check_header(payload)
    summary = payload["rank3_lowrow_schedule"]
    assert summary["forbid_singleton_projective_keys"] is True
    assert summary["forbid_core_subsets"] is True
    assert summary["support_pair_candidates"] == 0
    assert summary["best_min_support"] is None
    assert summary["best_total_incidence"] is None
    assert summary["best_pair_count_max"] is None
    assert payload["proof_status"].startswith(
        "EXACT_EXTRACTION_NO_A327 / MU8_RANK3_LOWROW_NO_SUPPORT_PAIR_PASS"
    )
    return summary


def verify(broad_path: Path, focused_path: Path) -> dict[str, Any]:
    broad = load_json(broad_path)
    focused = load_json(focused_path)
    broad_summary = check_no_singleton_flags(broad)
    focused_summary = check_no_singleton_flags(focused)

    assert broad_summary["subspaces_solved"] == 8
    assert broad_summary["best_singleton_key_forbid_constraints"] >= 500
    broad_candidates = broad["candidates"]
    assert len(broad_candidates) == 8
    statuses = {row["subspace_id"]: row["solver_status"] for row in broad_candidates}
    assert statuses["rank3_blockkey_001"] == "UNKNOWN"
    assert sum(1 for status in statuses.values() if status == "INFEASIBLE") == 7
    for row in broad_candidates:
        assert row["forbid_singleton_projective_keys"] is True
        assert row["support_pair_pass"] is False
        assert row["guard_pass"] is False
        assert row["singleton_key_forbid_constraints"] > 0

    assert focused_summary["subspaces_solved"] == 1
    assert focused_summary["best_singleton_key_forbid_constraints"] >= 600
    focused_candidates = focused["candidates"]
    assert len(focused_candidates) == 1
    focused_row = focused_candidates[0]
    assert focused_row["subspace_id"] == "rank3_blockkey_001"
    assert focused_row["solver_status"] == "INFEASIBLE"
    assert focused_row["support_pair_pass"] is False
    assert focused_row["guard_pass"] is False
    assert focused_row["forbid_singleton_projective_keys"] is True

    return {
        "status": "M1_A327_MU8_RANK3_NO_SINGLETON_PROJECTIVE_KEYS_VERIFY_PASS",
        "broad_path": str(broad_path),
        "focused_path": str(focused_path),
        "broad_subspaces_solved": broad_summary["subspaces_solved"],
        "broad_infeasible": sum(1 for status in statuses.values() if status == "INFEASIBLE"),
        "broad_unknown_resolved_by_focused": focused_row["subspace_id"],
        "focused_solver_status": focused_row["solver_status"],
        "support_pair_candidates": broad_summary["support_pair_candidates"],
        "required_selected_incidences": REQUIRED_TOTAL,
        "proof_status": broad["proof_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--broad", type=Path, default=DEFAULT_BROAD)
    parser.add_argument("--focused", type=Path, default=DEFAULT_FOCUSED)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(args.broad, args.focused)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])


if __name__ == "__main__":
    main()
