#!/usr/bin/env python3
"""Verify the compact M1 a327 mu8 rank-2 selected-front summary."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("experimental/data/m1_a327_mu8_rank2_selected_front_route_cut_summary.json")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_ARTIFACTS = {
    "experimental/data/m1_a327_mu8_rank2_carrier_menu_scan.json": (
        3482,
        51681,
        "6903bb376ba01c40ba1f54fa3fe032e8f7693450868447ecec8e887cb4f8bcb5",
    ),
    "experimental/data/m1_a327_mu8_rank2_carrier_schedule_candidates.json": (
        68728,
        1132539,
        "2b7f0fa241f4cc8a600cda8a358f529ecb78be0e8df4ffd012957060831d9efe",
    ),
    "experimental/data/m1_a327_mu8_rank2_cpsat_schedule_candidates.json": (
        3390,
        75049,
        "3097ac25f30ba77bbb229d63c19b5b14526cd97edd9e07b993ddf593505accdd",
    ),
    "experimental/data/m1_a327_mu8_rank2_width_ablation.json": (
        51,
        1454,
        "d6e6964a74da96aaad071bba34a91578084494fee4b06d8d8b8744026892e474",
    ),
    "experimental/data/m1_a327_mu8_rank2_fullmenu_schedule_candidates.json": (
        3714,
        72034,
        "a8ac78992e43029705a3ec8f750ce940b15ac260579328c1e0905046f664f00a",
    ),
    "experimental/data/m1_a327_mu8_rank2_adaptive_ratio_columns.json": (
        8725,
        205884,
        "1a3fdd0af70ec936c06cb73ec09ab4b4208bd7409bc70bea0c4cbdad239e975f",
    ),
    "experimental/data/m1_a327_mu8_rank2_adaptive_schedule_candidates.json": (
        3957,
        75626,
        "e3a28f36611b816af66017d0a074e0e76bed0f702c50544c97a96bb4ba41b485",
    ),
    "experimental/data/m1_a327_mu8_rank2_adaptive_near_front_exact.json": (
        55,
        1549,
        "dbeb3da88abe2bb080e550821e837f2eaac0d7a4ac795e393dc4baa81f335d26",
    ),
    "experimental/data/m1_a327_mu8_rank2_adaptive_exact_interpolation.json": (
        26,
        768,
        "ff3bd9c7af28a8f75f6aa0ff0a8ec7d26e26f0a8e36f97ce7fcdf2da4481ce71",
    ),
    "experimental/data/m1_a327_mu8_rank2_adaptive_witness_audit.json": (
        24,
        674,
        "820958b85f6bdd79edbee0ca7eab7ca5db8768bee91f72d0449efcab84f35ff5",
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
    require(len(artifacts) == len(EXPECTED_ARTIFACTS), "wrong source artifact count")
    by_path = {artifact["path"]: artifact for artifact in artifacts}
    require(set(by_path) == set(EXPECTED_ARTIFACTS), "source artifact paths changed")
    for path, (line_count, byte_count, sha256) in EXPECTED_ARTIFACTS.items():
        artifact = by_path[path]
        require(artifact["line_count"] == line_count, f"line count changed for {path}")
        require(artifact["byte_count"] == byte_count, f"byte count changed for {path}")
        require(artifact["sha256"] == sha256, f"sha256 changed for {path}")
        require(SHA256_RE.match(artifact["sha256"]) is not None, f"bad sha256 shape for {path}")
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
        == "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_SELECTED_FRONT_NO_SUPPORT_PAIR_PASS / PARTIAL / EXPERIMENTAL",
        "wrong proof status",
    )
    check_artifacts(record, check_hashes=check_hashes)

    model = record["rank2_model"]
    require(model["interpolation_variables"] == 64, "wrong interpolation variable count")
    require(model["quotient_points"] == 64, "wrong quotient point count")
    require(model["field"] == "GF(17^32)", "wrong exact field")

    expected_fronts = [
        ("greedy carrier schedule", 286, 2032, 41, 257),
        ("CP-SAT width-4 with row-cap gate", 291, 2041, 36, 248),
        ("full-menu width ablation", 313, 2193, 14, 96),
        ("adaptive ratio-column selected front", 314, 2202, 13, 87),
    ]
    fronts = record["frontier_progression"]
    require(len(fronts) == len(expected_fronts), "wrong frontier count")
    for front, (name, min_support, incidence, support_gap, incidence_gap) in zip(fronts, expected_fronts, strict=True):
        require(front["front"] == name, f"wrong front name: {name}")
        require(front["best_min_support"] == min_support, f"min support changed for {name}")
        require(front["best_selected_incidence_total"] == incidence, f"incidence changed for {name}")
        require(front["min_support_gap"] == support_gap, f"support gap changed for {name}")
        require(front["selected_incidence_gap"] == incidence_gap, f"incidence gap changed for {name}")
        require(front["guard_passing"] == 0 if "guard_passing" in front else front["support_pair_candidates"] == 0, f"guard pass appeared for {name}")

    adaptive = fronts[-1]
    require(adaptive["support_pair_candidates"] == 0, "adaptive support/pair candidate appeared")
    require(adaptive["near_front_candidates"] == 1, "adaptive near-front count changed")
    require(adaptive["best_support_vector"] == [314, 315, 317, 314, 314, 314, 314], "adaptive support vector changed")
    require(adaptive["best_pair_count_max"] == 255, "adaptive pair max changed")
    require(adaptive["best_row_cost"] == 92, "adaptive row cost changed")

    near = record["adaptive_near_front_exact_diagnostic"]
    require(near["diagnostic_only"] is True, "near-front should be diagnostic only")
    require(near["support_pair_pass"] is False, "near-front unexpectedly support/pair passing")
    require(near["matrix_shape"] == [92, 64], "near-front matrix shape changed")
    require(near["rank"] == 64, "near-front rank changed")
    require(near["nullity"] == 0, "near-front nullity changed")
    require(near["positive_nullity_systems"] == 0, "near-front positive nullity appeared")
    require(near["forced_equal_pairs"] == [], "forced equal pairs changed")
    require(near["forced_global_ratio_lines"] == [], "forced global ratio lines changed")
    require(near["max_ratio_line_support"] == 4, "max ratio-line support changed")
    require(near["rank_one_collapse_risk"] is False, "rank-one collapse risk changed")

    exact = record["support_pair_exact_interpolation"]
    require(exact["systems_tested"] == 0, "support/pair exact system unexpectedly tested")
    require(exact["positive_nullity_systems"] == 0, "support/pair positive nullity appeared")
    require(exact["pair_visible_systems"] == 0, "support/pair pair-visible system appeared")

    witness = record["witness_audit"]
    require(witness["constructed"] is False, "witness unexpectedly constructed")
    require(witness["seven_distinct"] is False, "seven distinct unexpectedly true")
    require(witness["agreement_vector"] is None, "agreement vector unexpectedly present")
    require(witness["status"] == "NO_EXACT_WITNESS_CONSTRUCTED", "wrong witness status")

    candidate = record["candidate"]
    require(candidate["exact_a327_witness_passes"] == 0, "exact witness pass count changed")

    return {
        "status": "M1_A327_MU8_RANK2_SELECTED_FRONT_ROUTE_CUT_SUMMARY_VERIFY_PASS",
        "path": str(DEFAULT_INPUT),
        "source_artifacts": len(record["source_artifacts"]),
        "best_min_support": adaptive["best_min_support"],
        "best_selected_incidence_total": adaptive["best_selected_incidence_total"],
        "best_support_gap": adaptive["min_support_gap"],
        "best_incidence_gap": adaptive["selected_incidence_gap"],
        "support_pair_candidates": adaptive["support_pair_candidates"],
        "near_front_exact_rank": near["rank"],
        "near_front_exact_nullity": near["nullity"],
        "exact_a327_witness_passes": candidate["exact_a327_witness_passes"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--check-source-hashes", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    summary = verify(load_json(args.input), check_hashes=args.check_source_hashes)
    summary["path"] = str(args.input)
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(summary["status"])


if __name__ == "__main__":
    main()
