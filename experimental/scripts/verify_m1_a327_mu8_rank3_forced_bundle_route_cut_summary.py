#!/usr/bin/env python3
"""Verify the compact M1 a327 mu8 rank3 forced-bundle route-cut summary."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("experimental/data/m1_a327_mu8_rank3_forced_bundle_route_cut_summary.json")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


EXPECTED_ARTIFACTS = {
    "experimental/data/m1_a327_mu8_rank3_forced_bundle_anchor_file.json": (
        842,
        13336,
        "ffa66c290e942d5ea1aa5f537292b6719a988b97ba4d07dcfb1c6e0cd6227f1b",
    ),
    "experimental/data/m1_a327_mu8_rank3_forced_bundle_schedule.json": (
        4387,
        84926,
        "91248069ebc497bda4b70b072f82ab6b52ea1e888224d8e99a6626ef2edc1f51",
    ),
    "experimental/data/m1_a327_mu8_rank3_forced_bundle_exact_interpolation.json": (
        46,
        1344,
        "7ffd96e855c3e688d78fe05c2a37484354f5a64c28d76e390cd6d23eca2a456a",
    ),
    "experimental/data/m1_a327_mu8_rank3_forced_bundle_singleton_replacement_targets.json": (
        2049,
        53022,
        "4b931a7f5242f9505b8a625d6adefbe55c6e5195cf4fd708e9c1999cc39b88f2",
    ),
    "experimental/data/m1_a327_mu8_rank3_forced_bundle_singleton_shared_point_probe.json": (
        1171,
        20946,
        "5efcee4f65c4ae322e58656542e929f5b33da0e5ae2199ce1a8ee625371e26e0",
    ),
    "experimental/data/m1_a327_mu8_rank3_forced_bundle_singleton_projective_line_probe.json": (
        4726,
        83205,
        "cd45e61178fbb82c67924c7b5108eef969f97c4cb405993fde59059952627ba2",
    ),
    "experimental/data/m1_a327_mu8_rank3_forced_bundle_projective_line_bundle_plan.json": (
        68,
        2326,
        "bf6bd4824a10331a0fb06137b1d8f48b6aa9f2575e18c05213f7843337b60d2d",
    ),
}


def fail(message: str) -> None:
    raise SystemExit(f"VERIFY_FAIL: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_artifacts(record: dict[str, Any], check_hashes: bool) -> None:
    artifacts = record["source_artifacts"]
    require(len(artifacts) == len(EXPECTED_ARTIFACTS), "wrong artifact count")
    by_path = {item["path"]: item for item in artifacts}
    require(set(by_path) == set(EXPECTED_ARTIFACTS), "artifact path set changed")
    for path, (line_count, byte_count, sha256) in EXPECTED_ARTIFACTS.items():
        item = by_path[path]
        require(item["line_count"] == line_count, f"line count changed for {path}")
        require(item["byte_count"] == byte_count, f"byte count changed for {path}")
        require(item["sha256"] == sha256, f"sha256 changed for {path}")
        require(SHA256_RE.match(item["sha256"]) is not None, f"bad sha256 shape for {path}")
        if check_hashes:
            file_path = Path(path)
            require(file_path.exists(), f"source artifact missing: {path}")
            require(sha256_file(file_path) == sha256, f"source artifact hash mismatch: {path}")


def verify(record: dict[str, Any], check_hashes: bool) -> dict[str, Any]:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == 327, "wrong target")
    require(record["mca_counted"] is False, "MCA counted")
    require(
        record["proof_status"]
        == "EXACT_EXTRACTION_NO_A327 / MU8_RANK3_FORCED_BUNDLE_SINGLETON_BOUNDARY_ROUTE_CUT / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )
    check_artifacts(record, check_hashes=check_hashes)

    anchor = record["forced_bundle_anchor"]
    require(anchor["forced_anchor_count"] == 12, "forced anchor count changed")
    require(anchor["forced_selected_incidence"] == 336, "forced incidence changed")
    require(anchor["forced_support_vector"] == [48] * 7, "forced support vector changed")
    require(anchor["forced_pair_count_max"] == 48, "forced pair max changed")
    require(anchor["residual_selected_incidence_need"] == 1953, "residual incidence changed")
    require(anchor["source_schedule_support_pair_pass"] is True, "source schedule no longer passes")

    scheduler = record["forced_bundle_scheduler"]
    require(scheduler["support_pair_candidates"] == 1, "support/pair candidate count changed")
    require(scheduler["strict_support_pair_candidates"] == 0, "strict candidate count changed")
    require(scheduler["best_min_support"] == 327, "best min support changed")
    require(scheduler["best_total_incidence"] == 2294, "best total incidence changed")
    require(scheduler["best_pair_count_max"] == 255, "best pair max changed")
    require(scheduler["best_row_cost"] == 148, "best row cost changed")
    require(scheduler["best_support_vector"] == [328, 328, 327, 330, 327, 327, 327], "support vector changed")
    require(scheduler["best_nonforced_repeated_projective_key_count"] == 0, "nonforced repeat count changed")
    require(scheduler["best_nonforced_singleton_projective_key_count"] == 29, "singleton escape count changed")

    exact = record["exact_interpolation"]
    require(exact["field"] == "GF(17^32)", "wrong exact field")
    require(exact["systems_tested"] == 1, "exact system count changed")
    require(exact["positive_nullity_systems"] == 0, "positive nullity appeared")
    require(exact["pair_visible_systems"] == 0, "pair-visible system appeared")
    require(exact["matrix_shape"] == [148, 96], "exact matrix shape changed")
    require(exact["rank"] == 96, "exact rank changed")
    require(exact["nullity"] == 0, "exact nullity changed")

    targets = record["singleton_replacement_targets"]
    require(targets["singleton_signature_groups"] == 12, "singleton group count changed")
    require(targets["singleton_projective_rows"] == 29, "singleton row count changed")
    require(targets["best_target_group_count"] == 8, "best target count changed")
    require(targets["best_target_group_incidence"] == 168, "best target incidence changed")
    require(targets["best_target_group_support_vector"] == [24] * 7, "best target support changed")
    require(targets["best_target_group_qidxs"] == [21, 28, 32, 38, 43, 46, 48, 49], "best qidxs changed")

    shared = record["singleton_shared_point_probe"]
    require(shared["nontrivial_shared_point_groups"] == 0, "shared-point groups appeared")
    require(shared["best_nontrivial_matrix_shape"] == [104, 3], "shared-point matrix shape changed")
    require(shared["best_nontrivial_rank"] == 3, "shared-point rank changed")
    require(shared["best_nontrivial_nullity"] == 0, "shared-point nullity changed")

    line = record["singleton_projective_line_probe"]
    require(line["nontrivial_projective_line_groups"] == 2, "line group count changed")
    require(line["best_nontrivial_line_target_count"] == 2, "best line target count changed")
    require(line["best_nontrivial_line_target_selected_incidence"] == 54, "best line incidence changed")

    bundle = record["projective_line_bundle_plan"]
    require(bundle["line_positive_groups"] == 2, "bundle line-positive count changed")
    require(bundle["material_bundles"] == 0, "material bundle appeared")
    require(bundle["best_line_target_count"] == 4, "bundle target count changed")
    require(bundle["best_line_target_selected_incidence"] == 96, "bundle incidence changed")
    require(bundle["best_remaining_singleton_rows"] == 25, "remaining singleton rows changed")
    require(bundle["best_max_line_support"] == 2, "max line support changed")
    require(bundle["degree32_repeated_line_threshold"] == 32, "degree threshold changed")

    candidate = record["candidate"]
    require(candidate["constructed"] is False, "candidate unexpectedly constructed")
    require(candidate["seven_distinct"] is False, "seven distinct unexpectedly true")
    require(candidate["agreement_vector"] is None, "agreement vector unexpectedly present")
    require(candidate["exact_a327_witness_passes"] == 0, "exact witness pass count changed")

    return {
        "status": "M1_A327_MU8_RANK3_FORCED_BUNDLE_ROUTE_CUT_SUMMARY_VERIFY_PASS",
        "path": str(DEFAULT_INPUT),
        "source_artifacts": len(record["source_artifacts"]),
        "support_pair_candidates": scheduler["support_pair_candidates"],
        "strict_support_pair_candidates": scheduler["strict_support_pair_candidates"],
        "exact_rank": exact["rank"],
        "exact_nullity": exact["nullity"],
        "singleton_escape_rows": scheduler["best_nonforced_singleton_projective_key_count"],
        "shared_point_nontrivial_groups": shared["nontrivial_shared_point_groups"],
        "line_bundle_material_bundles": bundle["material_bundles"],
        "exact_a327_witness_passes": candidate["exact_a327_witness_passes"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check-source-hashes", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = load_json(args.input)
    summary = verify(record, check_hashes=args.check_source_hashes)
    summary["path"] = str(args.input)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(summary["status"])


if __name__ == "__main__":
    main()
