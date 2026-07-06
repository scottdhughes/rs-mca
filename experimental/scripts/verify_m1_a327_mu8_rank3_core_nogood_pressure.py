#!/usr/bin/env python3
"""Verify the rank-3 mu_8 core-no-good pressure follow-up audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("experimental/data/m1_a327_mu8_rank3_core_nogood_row_dependency_pressure.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def verify(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    assert payload["track"] == "INTERLEAVED_LIST"
    assert payload["row"] == "RS[F_17^32,H,256]"
    assert payload["denominator"] == "17^32"
    assert payload["agreement_target"] == 327
    assert payload["mca_counted"] is False
    assert "MCA N_bad" in payload["not_claimed"]
    assert payload["proof_status"].startswith(
        "EXACT_EXTRACTION_NO_A327 / MU8_RANK3_ROW_DEPENDENCY_FULL_RANK"
    )
    summary = payload["row_dependency_pressure"]
    systems = payload["systems"]
    assert summary["systems_tested"] == len(systems)
    assert summary["positive_nullity_systems"] == 0
    assert summary["best_nullity"] == 0
    assert summary["pivot_core_enabled"] is True

    dependency_free_core_count = 0
    dependency_bearing_core_count = 0
    singleton_projective_systems = 0
    for system in systems:
        shape = system["matrix_shape"]
        assert len(shape) == 2
        cols = int(shape[1])
        assert int(system["rank"]) == cols
        assert int(system["nullity"]) == 0
        assert str(system["status"]).startswith("MU8_RANK3_ROW_DEPENDENCY_FULL_RANK")
        assert int(system["min_support"]) >= 327
        assert int(system["selected_incidence_total"]) >= 7 * 327
        assert int(system["pair_count_max"]) <= 255
        hist = system.get("selected_group_histograms", {})
        if int(hist.get("max_projective_key_support", 0)) <= 1:
            singleton_projective_systems += 1
        assert system["rank_drop_histogram"].get("0") == system["tested_group_count"]
        assert int(system["critical_group_count"]) == 0
        assert int(system["removable_group_count"]) == int(system["tested_group_count"])
        pivot_cores = system["pivot_cores"]
        assert pivot_cores
        for core in pivot_cores:
            assert int(core["core_rank"]) == cols
            assert int(core["core_row_count"]) == cols
            if int(core["dependency_groups_in_core"]) == 0:
                dependency_free_core_count += 1
            else:
                dependency_bearing_core_count += 1

    assert singleton_projective_systems >= 1
    assert dependency_free_core_count >= 1
    return {
        "status": "M1_A327_MU8_RANK3_CORE_NOGOOD_PRESSURE_VERIFY_PASS",
        "path": str(path),
        "proof_status": payload["proof_status"],
        "systems_tested": len(systems),
        "positive_nullity_systems": summary["positive_nullity_systems"],
        "dependency_free_pivot_cores": dependency_free_core_count,
        "dependency_bearing_pivot_cores": dependency_bearing_core_count,
        "singleton_projective_systems": singleton_projective_systems,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = verify(args.input)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])


if __name__ == "__main__":
    main()
