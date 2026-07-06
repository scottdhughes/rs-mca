#!/usr/bin/env python3
"""Verify the rank-3 mu_8 core-no-good low-row smoke audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_SCHEDULE = Path("experimental/data/m1_a327_mu8_rank3_core_nogood_lowrow_schedule.json")
DEFAULT_EXACT = Path("experimental/data/m1_a327_mu8_rank3_core_nogood_exact_interpolation.json")
DEFAULT_WITNESS = Path("experimental/data/m1_a327_mu8_rank3_core_nogood_witness_audit.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify(schedule_path: Path, exact_path: Path, witness_path: Path) -> dict[str, Any]:
    schedule = load_json(schedule_path)
    exact = load_json(exact_path)
    witness = load_json(witness_path)
    for payload in (schedule, exact, witness):
        assert payload["track"] == "INTERLEAVED_LIST"
        assert payload["row"] == "RS[F_17^32,H,256]"
        assert payload["denominator"] == "17^32"
        assert payload["agreement_target"] == 327
        assert payload["mca_counted"] is False
        assert "MCA N_bad" in payload["not_claimed"]
    sched = schedule["rank3_lowrow_schedule"]
    assert sched["forbid_core_subsets"] is True
    assert sched["support_pair_candidates"] >= 1
    assert sched["best_core_nogood_constraints"] >= 1
    support_pair = [row for row in schedule["candidates"] if row.get("support_pair_pass")]
    assert support_pair
    for row in support_pair:
        assert min(row["support_vector"]) >= 327
        assert row["selected_incidence_total"] >= 7 * 327
        assert row["pair_count_max"] <= 255
        assert row["core_nogood_constraints"] >= 1
    audit = exact["exact_interpolation"]
    assert audit["systems_tested"] == len(support_pair[: audit["systems_tested"]])
    assert audit["positive_nullity_systems"] == 0
    assert audit["pair_visible_systems"] == 0
    assert audit["best_nullity"] == 0
    assert exact["proof_status"].startswith("EXACT_EXTRACTION_NO_A327 / MU8_RANK3_PROJECTIVE_INTERPOLATION_FULL_RANK")
    for system in exact["systems"]:
        shape = system["matrix_shape"]
        assert len(shape) == 2
        assert int(system["rank"]) == int(shape[1])
        assert int(system["nullity"]) == 0
        assert system["status"] == "MU8_RANK3_PROJECTIVE_INTERPOLATION_FULL_RANK"
    assert witness["witness_audit"]["status"] == "NO_EXACT_WITNESS_CONSTRUCTED"
    assert witness["proof_status"].startswith("EXACT_EXTRACTION_NO_A327")
    return {
        "status": "M1_A327_MU8_RANK3_CORE_NOGOOD_LOWROW_VERIFY_PASS",
        "schedule_path": str(schedule_path),
        "exact_path": str(exact_path),
        "support_pair_candidates": sched["support_pair_candidates"],
        "best_min_support": sched["best_min_support"],
        "best_total_incidence": sched["best_total_incidence"],
        "best_core_nogood_constraints": sched["best_core_nogood_constraints"],
        "systems_tested": audit["systems_tested"],
        "positive_nullity_systems": audit["positive_nullity_systems"],
        "proof_status": exact["proof_status"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--schedule", type=Path, default=DEFAULT_SCHEDULE)
    parser.add_argument("--exact", type=Path, default=DEFAULT_EXACT)
    parser.add_argument("--witness", type=Path, default=DEFAULT_WITNESS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(args.schedule, args.exact, args.witness)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])


if __name__ == "__main__":
    main()
