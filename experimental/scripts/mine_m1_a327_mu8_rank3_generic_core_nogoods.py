#!/usr/bin/env python3
"""Mine dependency-free rank-3 mu_8 pivot cores as CP-SAT no-goods."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


TARGET = 327
SOURCE_COMMIT = "95a2245"
DEFAULT_OUTPUT = Path("experimental/data/m1_a327_mu8_rank3_generic_core_nogoods.json")
NOT_CLAIMED = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def tracked_pressure_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "experimental/data/*rank3*row_dependency_pressure*.json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line) for line in proc.stdout.splitlines() if line.strip()]


def core_signature(core_group_ids: list[str]) -> str:
    body = "\n".join(sorted(str(group_id) for group_id in core_group_ids))
    return hashlib.sha256(body.encode()).hexdigest()[:24]


def dependency_last_core(system: dict[str, Any]) -> dict[str, Any] | None:
    for core in system.get("pivot_cores", []):
        if core.get("mode") == "dependency_last":
            return core
    return None


def is_dependency_free_full_rank(system: dict[str, Any], core: dict[str, Any]) -> bool:
    matrix_shape = system.get("matrix_shape") or []
    if len(matrix_shape) != 2:
        return False
    cols = int(matrix_shape[1])
    return (
        int(system.get("rank", -1)) == cols
        and int(system.get("nullity", -1)) == 0
        and int(core.get("core_rank", -1)) == cols
        and int(core.get("dependency_groups_in_core", -1)) == 0
        and int(core.get("dependency_rows_in_core", -1)) == 0
        and bool(core.get("core_group_ids"))
    )


def build_record(paths: list[Path]) -> dict[str, Any]:
    files = []
    systems = []
    seen: set[tuple[str, str]] = set()
    by_plane: dict[str, Counter[str]] = defaultdict(Counter)
    pressure_systems_scanned = 0
    eligible_systems = 0
    duplicate_cores = 0
    singleton_projective_cores = 0

    for path in paths:
        payload = load_json(path)
        file_systems = payload.get("systems", [])
        file_eligible = 0
        file_unique = 0
        for system in file_systems:
            pressure_systems_scanned += 1
            core = dependency_last_core(system)
            if not core or not is_dependency_free_full_rank(system, core):
                continue
            eligible_systems += 1
            file_eligible += 1
            signature = core_signature(core.get("core_group_ids", []))
            plane_id = str(system.get("plane_id") or system.get("subspace_id") or "UNKNOWN")
            dedupe_key = (plane_id, signature)
            if dedupe_key in seen:
                duplicate_cores += 1
                continue
            seen.add(dedupe_key)
            file_unique += 1
            hist = core.get("core_group_histograms", {})
            singleton_projective = int(hist.get("max_projective_key_support", 0)) <= 1
            if singleton_projective:
                singleton_projective_cores += 1
            by_plane[plane_id]["unique_core_nogoods"] += 1
            by_plane[plane_id]["singleton_projective_cores"] += int(singleton_projective)
            systems.append(
                {
                    "path": str(path),
                    "candidate_id": system.get("candidate_id"),
                    "plane_id": system.get("plane_id"),
                    "subspace_id": system.get("subspace_id"),
                    "matrix_shape": system.get("matrix_shape"),
                    "rank": system.get("rank"),
                    "nullity": system.get("nullity"),
                    "min_support": system.get("min_support"),
                    "pair_count_max": system.get("pair_count_max"),
                    "selected_incidence_total": system.get("selected_incidence_total"),
                    "core_signature": signature,
                    "dependency_last_dependency_free": True,
                    "dependency_last_singleton_projective": singleton_projective,
                    "pivot_cores": [
                        {
                            "mode": "dependency_last",
                            "core_rank": core.get("core_rank"),
                            "core_row_count": core.get("core_row_count"),
                            "core_group_count": core.get("core_group_count"),
                            "dependency_groups_in_core": core.get("dependency_groups_in_core"),
                            "dependency_rows_in_core": core.get("dependency_rows_in_core"),
                            "core_group_histograms": hist,
                            "core_group_ids": core.get("core_group_ids", []),
                        }
                    ],
                }
            )
        files.append(
            {
                "path": str(path),
                "systems": len(file_systems),
                "eligible_dependency_free_cores": file_eligible,
                "unique_core_nogoods": file_unique,
            }
        )

    systems.sort(key=lambda row: (str(row.get("plane_id")), str(row.get("candidate_id")), row["core_signature"]))
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET,
        "source_commit": SOURCE_COMMIT,
        "generic_core_nogoods": {
            "pressure_files_scanned": len(paths),
            "pressure_systems_scanned": pressure_systems_scanned,
            "eligible_dependency_free_full_rank_systems": eligible_systems,
            "unique_core_nogoods": len(systems),
            "duplicate_cores_removed": duplicate_cores,
            "singleton_projective_core_nogoods": singleton_projective_cores,
            "planes": {
                plane_id: dict(counts)
                for plane_id, counts in sorted(by_plane.items())
            },
            "best_failure_mode": "MU8_RANK3_GENERIC_CORE_NOGOODS_READY",
        },
        "files": files,
        "systems": systems,
        "proof_status": "EXACT_EXTRACTION_NO_A327 / MU8_RANK3_GENERIC_CORE_NOGOODS / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", help="Pressure ledger to mine. Defaults to tracked rank3 pressure ledgers.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    paths = args.input if args.input else tracked_pressure_files()
    record = build_record(paths)
    if args.write:
        write_json(args.output, record)
    summary = {
        "proof_status": record["proof_status"],
        "pressure_files_scanned": record["generic_core_nogoods"]["pressure_files_scanned"],
        "pressure_systems_scanned": record["generic_core_nogoods"]["pressure_systems_scanned"],
        "eligible_dependency_free_full_rank_systems": record["generic_core_nogoods"]["eligible_dependency_free_full_rank_systems"],
        "unique_core_nogoods": record["generic_core_nogoods"]["unique_core_nogoods"],
        "singleton_projective_core_nogoods": record["generic_core_nogoods"]["singleton_projective_core_nogoods"],
        "best_failure_mode": record["generic_core_nogoods"]["best_failure_mode"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_RANK3_GENERIC_CORE_NOGOODS_READY")


if __name__ == "__main__":
    main()
