#!/usr/bin/env python3
"""Verify the rank-3 mu_8 generic-core no-good packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("experimental/data/m1_a327_mu8_rank3_generic_core_nogoods.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def parse_group_id(group_id: str) -> tuple[int, str]:
    qidx_raw, option_id = str(group_id).split(":", 1)
    return int(qidx_raw), option_id


def verify(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    assert payload["track"] == "INTERLEAVED_LIST"
    assert payload["row"] == "RS[F_17^32,H,256]"
    assert payload["denominator"] == "17^32"
    assert payload["agreement_target"] == 327
    assert payload["mca_counted"] is False
    assert "MCA N_bad" in payload["not_claimed"]
    assert payload["proof_status"].startswith("EXACT_EXTRACTION_NO_A327 / MU8_RANK3_GENERIC_CORE_NOGOODS")
    summary = payload["generic_core_nogoods"]
    systems = payload["systems"]
    assert systems, "expected at least one no-good system"
    assert summary["unique_core_nogoods"] == len(systems)
    assert summary["eligible_dependency_free_full_rank_systems"] >= len(systems)
    seen: set[tuple[str, str]] = set()
    singleton_count = 0
    for system in systems:
        plane_id = str(system.get("plane_id") or system.get("subspace_id") or "UNKNOWN")
        signature = str(system["core_signature"])
        assert (plane_id, signature) not in seen
        seen.add((plane_id, signature))
        shape = system["matrix_shape"]
        assert len(shape) == 2
        cols = int(shape[1])
        assert int(system["rank"]) == cols
        assert int(system["nullity"]) == 0
        assert system["dependency_last_dependency_free"] is True
        cores = system["pivot_cores"]
        assert len(cores) == 1
        core = cores[0]
        assert core["mode"] == "dependency_last"
        assert int(core["core_rank"]) == cols
        assert int(core["dependency_groups_in_core"]) == 0
        assert int(core["dependency_rows_in_core"]) == 0
        group_ids = core["core_group_ids"]
        assert group_ids
        parsed = [parse_group_id(group_id) for group_id in group_ids]
        assert len(set(parsed)) == len(parsed)
        hist = core.get("core_group_histograms", {})
        if int(hist.get("max_projective_key_support", 0)) <= 1:
            singleton_count += 1
    assert singleton_count == summary["singleton_projective_core_nogoods"]
    return {
        "status": "M1_A327_MU8_RANK3_GENERIC_CORE_NOGOODS_VERIFY_PASS",
        "path": str(path),
        "proof_status": payload["proof_status"],
        "unique_core_nogoods": len(systems),
        "singleton_projective_core_nogoods": singleton_count,
        "eligible_dependency_free_full_rank_systems": summary["eligible_dependency_free_full_rank_systems"],
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
