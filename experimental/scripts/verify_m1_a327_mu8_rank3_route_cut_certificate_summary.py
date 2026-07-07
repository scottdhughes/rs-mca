#!/usr/bin/env python3
"""Verify the compact M1 a=327 mu8 rank-3 route-cut certificate summary."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TARGET = 327
REQUIRED_TOTAL = 7 * TARGET
PAIR_CAP = 255
DEFAULT_INPUT = Path(
    "experimental/data/m1_a327_mu8_rank3_route_cut_certificate_summary.json"
)
REQUIRED_NONCLAIMS = {
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def check_header(record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET, "wrong target")
    require(record["mca_counted"] is False, "MCA counted")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")


def check_hash_artifacts(record: dict[str, Any]) -> None:
    artifacts = record["hash_addressed_artifacts"]
    require(len(artifacts) >= 9, "too few hash-addressed artifacts")
    seen_paths = set()
    for artifact in artifacts:
        path = artifact["path"]
        require(path not in seen_paths, f"duplicate artifact path: {path}")
        seen_paths.add(path)
        require(artifact["included_in_this_pr"] is False, f"artifact should be external: {path}")
        require(SHA256_RE.match(artifact["sha256"]) is not None, f"bad sha256: {path}")
        require(artifact["line_count"] > 0, f"missing line count: {path}")
        require(artifact["byte_count"] > 0, f"missing byte count: {path}")
    archive = record["large_raw_schedule_archive"]
    require(archive["path"] in seen_paths, "large archive is not hash-addressed")
    require(archive["line_count"] == 73753, "large archive line count changed")
    require(archive["sha256"] == "b9eea14d9db3ac34fd626dbcc8276a5fe8a70c8b133189acfcab5897395c637a", "large archive hash changed")


def check_generic_core_nogoods(record: dict[str, Any]) -> None:
    generic = record["generic_core_nogoods"]
    require(generic["status"] == "MU8_RANK3_GENERIC_CORE_NOGOODS_READY", "wrong generic status")
    require(generic["pressure_files_scanned"] == 30, "pressure file count changed")
    require(generic["pressure_systems_scanned"] == 79, "pressure system count changed")
    require(generic["eligible_dependency_free_full_rank_systems"] == 56, "eligible system count changed")
    require(generic["unique_core_nogoods"] == 54, "unique no-good count changed")
    require(generic["singleton_projective_core_nogoods"] == 54, "singleton no-good count changed")
    require(generic["duplicate_cores_removed"] == 2, "duplicate count changed")
    plane_total = sum(row["unique_core_nogoods"] for row in generic["planes"].values())
    require(plane_total == generic["unique_core_nogoods"], "plane no-good count mismatch")


def check_guarded_run(record: dict[str, Any]) -> None:
    guarded = record["guarded_core_nogood_run"]
    require(guarded["schedule_status"] == "MU8_RANK3_LOWROW_SUPPORT_PAIR_PASS", "wrong guarded schedule status")
    require(guarded["support_pair_candidates"] == 2, "guarded support/pair count changed")
    require(guarded["best_min_support"] >= TARGET, "guarded support below target")
    require(guarded["best_total_incidence"] >= REQUIRED_TOTAL, "guarded incidence below target")
    require(guarded["best_pair_count_max"] <= PAIR_CAP, "guarded pair cap failed")
    require(guarded["best_max_selected_projective_key_support"] == 1, "guarded key support changed")
    require(guarded["exact_status"] == "MU8_RANK3_PROJECTIVE_INTERPOLATION_FULL_RANK", "wrong guarded exact status")
    require(guarded["exact_field"] == "GF(17^32)", "wrong exact field")
    require(guarded["exact_systems_tested"] == 2, "guarded exact systems changed")
    require(guarded["exact_positive_nullity_systems"] == 0, "guarded positive nullity appeared")
    require(guarded["exact_best_nullity"] == 0, "guarded best nullity changed")
    require(all(shape == [152, 96] for shape in guarded["exact_matrix_shapes"]), "guarded matrix shape changed")
    require(guarded["row_pressure_status"] == "MU8_RANK3_ROW_DEPENDENCY_FULL_RANK", "wrong pressure status")
    require(guarded["row_pressure_positive_nullity_systems"] == 0, "pressure positive nullity appeared")
    require(guarded["witness_constructed"] is False, "unexpected witness")


def check_singleton_forbid(record: dict[str, Any]) -> None:
    singleton = record["singleton_projective_key_forbid_run"]
    require(singleton["status"] == "MU8_RANK3_LOWROW_NO_SUPPORT_PAIR_PASS", "wrong singleton status")
    require(singleton["forbid_core_subsets"] is True, "core subsets not forbidden")
    require(singleton["forbid_singleton_projective_keys"] is True, "singleton keys not forbidden")
    require(singleton["broad_subspaces_solved"] == 8, "broad subspace count changed")
    require(singleton["broad_support_pair_candidates"] == 0, "broad support/pair candidates appeared")
    require(singleton["broad_solver_status_counts"] == {"INFEASIBLE": 7, "UNKNOWN": 1}, "broad solver statuses changed")
    require(singleton["focused_subspace"] == "rank3_blockkey_001", "focused subspace changed")
    require(singleton["focused_solver_status"] == "INFEASIBLE", "focused solver status changed")
    require(singleton["focused_support_pair_candidates"] == 0, "focused support/pair candidate appeared")
    require(singleton["focused_singleton_key_forbid_constraints"] == 613, "focused constraint count changed")


def check_archive_summary(record: dict[str, Any]) -> None:
    archive = record["large_raw_schedule_archive"]
    require(archive["status"] == "ARCHIVED_SEPARATELY", "archive status changed")
    require(archive["support_pair_candidates"] == 1, "archive support/pair count changed")
    require(archive["best_min_support"] >= TARGET, "archive support below target")
    require(archive["best_total_incidence"] >= REQUIRED_TOTAL, "archive incidence below target")
    require(archive["best_pair_count_max"] <= PAIR_CAP, "archive pair cap failed")
    require(archive["max_selected_projective_key_support"] == 1, "archive projective key support changed")
    exact = archive["exact_interpolation"]
    require(exact["field"] == "GF(17^32)", "archive exact field changed")
    require(exact["systems_tested"] == 1, "archive exact system count changed")
    require(exact["matrix_shape"] == [155, 96], "archive matrix shape changed")
    require(exact["rank"] == 96 and exact["nullity"] == 0, "archive rank/nullity changed")
    pressure = archive["row_dependency_pressure"]
    require(pressure["systems_tested"] == 1, "archive pressure count changed")
    require(pressure["rank"] == 96 and pressure["nullity"] == 0, "archive pressure rank/nullity changed")
    require(pressure["critical_group_count"] == 0, "archive critical group count changed")


def verify(path: Path) -> dict[str, Any]:
    record = load_json(path)
    check_header(record)
    check_hash_artifacts(record)
    check_generic_core_nogoods(record)
    check_guarded_run(record)
    check_singleton_forbid(record)
    check_archive_summary(record)
    require(record["summary"]["exact_a327_witness_passes"] == 0, "unexpected exact witness")
    require(record["summary"]["board_ready"] is False, "summary claims board readiness")
    return {
        "status": "M1_A327_MU8_RANK3_ROUTE_CUT_CERTIFICATE_SUMMARY_VERIFY_PASS",
        "path": str(path),
        "unique_core_nogoods": record["generic_core_nogoods"]["unique_core_nogoods"],
        "guarded_support_pair_candidates": record["guarded_core_nogood_run"]["support_pair_candidates"],
        "singleton_forbid_support_pair_candidates": record["singleton_projective_key_forbid_run"]["focused_support_pair_candidates"],
        "archived_raw_schedule_lines": record["large_raw_schedule_archive"]["line_count"],
        "exact_a327_witness_passes": record["summary"]["exact_a327_witness_passes"],
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
