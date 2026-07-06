#!/usr/bin/env python3
"""Verify the compact M1 a=327 mu8 public-packet triage ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


DEFAULT_INPUT = Path("experimental/data/m1_a327_mu8_public_packet_triage.json")
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def check_header(record: dict[str, Any]) -> None:
    require(record["track"] == "INTERLEAVED_LIST", "wrong track")
    require(record["row"] == "RS[F_17^32,H,256]", "wrong row")
    require(record["denominator"] == "17^32", "wrong denominator")
    require(record["agreement_target"] == TARGET, "wrong agreement target")
    require(record["mca_counted"] is False, "MCA was counted")
    require(REQUIRED_NONCLAIMS.issubset(set(record["not_claimed"])), "missing nonclaims")


def check_evidence_hashes(record: dict[str, Any]) -> None:
    hashes = record["evidence_hashes_sha256"]
    require(hashes, "missing evidence hashes")
    for raw_path, expected in hashes.items():
        path = Path(raw_path)
        require(path.exists(), f"hashed evidence missing: {path}")
        require(sha256_file(path) == expected, f"hash mismatch for {path}")


def check_rank_one(record: dict[str, Any]) -> dict[str, Any]:
    rank_one = record["rank_one_mu8"]["obstruction"]
    require(rank_one["status"] == "MU8_RANK_ONE_CARRIER_INCIDENCE_OBSTRUCTION", "wrong rank-one status")
    require(rank_one["pair_visible_required"] is True, "rank-one obstruction missing pair-visible hypothesis")
    require(rank_one["quotient_roots_max"] == 31, "rank-one quotient root bound changed")
    require(rank_one["common_zero_coordinates_max"] == 248, "rank-one common-zero bound changed")
    require(rank_one["outside_pair_equalities_max"] == 147, "rank-one outside-pair bound changed")
    require(rank_one["required_selected_incidences"] == REQUIRED_TOTAL, "rank-one required total mismatch")
    expected_ceiling = 512 + 6 * rank_one["common_zero_coordinates_max"] + rank_one["outside_pair_equalities_max"]
    require(rank_one["selected_incidence_ceiling"] == expected_ceiling, "rank-one ceiling arithmetic mismatch")
    require(rank_one["selected_incidence_ceiling"] == 2147, "rank-one ceiling changed")
    require(rank_one["strict_gap"] == REQUIRED_TOTAL - expected_ceiling, "rank-one gap mismatch")
    require(rank_one["contradiction"] is True, "rank-one contradiction not recorded")
    require(expected_ceiling < REQUIRED_TOTAL, "rank-one ceiling does not contradict a=327")
    return {
        "selected_incidence_ceiling": expected_ceiling,
        "required_selected_incidences": REQUIRED_TOTAL,
        "strict_gap": REQUIRED_TOTAL - expected_ceiling,
    }


def check_rank2(record: dict[str, Any]) -> dict[str, Any]:
    rank2 = record["rank2_mu8"]
    sweep = rank2["adaptive_sweep"]
    best = sweep["best"]
    require(sweep["adaptive_ledgers_scanned"] > 0, "rank-2 sweep scanned no ledgers")
    require(sweep["support_pair_passing_ledgers"] == 0, "rank-2 sweep found support/pair pass")
    require(best["best_min_support"] < TARGET, "rank-2 best support unexpectedly reaches target")
    require(best["best_total_incidence"] < REQUIRED_TOTAL, "rank-2 best total unexpectedly reaches target")
    require(best["support_pair_candidates"] == 0, "rank-2 best has support/pair candidates")
    require(best["selected_incidence_gap"] == REQUIRED_TOTAL - best["best_total_incidence"], "rank-2 best gap mismatch")
    require(best["support_gap"] == TARGET - best["best_min_support"], "rank-2 best support gap mismatch")

    exact = rank2["exact_sweep"]
    require(exact["exact_ledgers_scanned"] > 0, "rank-2 exact sweep scanned no ledgers")
    require(exact["systems_tested_total"] > 0, "rank-2 exact/near-front diagnostics missing")
    require(exact["positive_nullity_systems_total"] == 0, "rank-2 exact sweep found positive nullity")
    require(exact["pair_visible_systems_total"] == 0, "rank-2 exact sweep found pair-visible system")
    require(exact["max_best_nullity"] == 0, "rank-2 exact max nullity changed")
    require(exact["all_tested_systems_full_rank"] is True, "rank-2 tested systems are not all full-rank")
    return {
        "adaptive_ledgers_scanned": sweep["adaptive_ledgers_scanned"],
        "best_min_support": best["best_min_support"],
        "best_total_incidence": best["best_total_incidence"],
        "exact_systems_tested": exact["systems_tested_total"],
    }


def check_rank3(record: dict[str, Any]) -> dict[str, Any]:
    rank3 = record["rank3_mu8"]
    singleton = rank3["singleton_boundary"]
    require(singleton["22"]["support_pair_candidates"] > 0, "rank-3 singleton-22 should pass support/pair")
    require(singleton["22"]["best_min_support"] >= TARGET, "rank-3 singleton-22 support changed")
    require(singleton["22"]["best_total_incidence"] >= REQUIRED_TOTAL, "rank-3 singleton-22 total changed")
    require(singleton["21"]["support_pair_candidates"] == 0, "rank-3 singleton-21 unexpectedly passes")

    singleton_exact = rank3["singleton22_exact_and_pressure"]["exact"]
    require(singleton_exact["best_nullity"] == 0, "rank-3 singleton-22 exact nullity changed")
    require(singleton_exact["positive_nullity_systems"] == 0, "rank-3 singleton-22 positive nullity")

    exact = rank3["exact_sweep"]
    require(exact["exact_ledgers_scanned"] > 0, "rank-3 exact sweep scanned no ledgers")
    require(exact["systems_tested_total"] > 0, "rank-3 exact systems missing")
    require(exact["positive_nullity_systems_total"] == 0, "rank-3 exact sweep found positive nullity")
    require(exact["pair_visible_systems_total"] == 0, "rank-3 exact sweep found pair-visible system")
    require(exact["max_best_nullity"] == 0, "rank-3 max nullity changed")
    require(exact["all_tested_systems_full_rank"] is True, "rank-3 exact systems are not all full-rank")

    pressure = rank3["row_pressure_sweep"]
    require(pressure["pressure_ledgers_scanned"] > 0, "rank-3 pressure sweep scanned no ledgers")
    require(pressure["systems_tested_total"] > 0, "rank-3 pressure systems missing")
    require(pressure["positive_nullity_systems_total"] == 0, "rank-3 pressure sweep found positive nullity")
    require(pressure["all_tested_cores_full_rank"] is True, "rank-3 pressure systems are not all full-rank")
    return {
        "exact_systems_tested": exact["systems_tested_total"],
        "row_pressure_systems_tested": pressure["systems_tested_total"],
        "singleton22_candidates": singleton["22"]["support_pair_candidates"],
    }


def verify(path: Path) -> dict[str, Any]:
    record = load_json(path)
    check_header(record)
    check_evidence_hashes(record)

    public = record["public_packet_triage"]
    require(public["board_ready"] is False, "packet should not be board-ready")
    require(public["exact_a327_witness"] is False, "packet unexpectedly claims exact witness")
    require(public["recommended_public_action"] == "do_not_open_board_pr_yet", "wrong public action")
    require(public["route_cut_candidate"] is True, "route-cut candidate not recorded")

    witness = record["witness_sweep"]
    require(witness["witness_ledgers_scanned"] > 0, "no witness ledgers scanned")
    require(witness["exact_a327_witness_passes"] == 0, "exact witness pass found")
    require(witness["pass_paths"] == [], "witness pass paths should be empty")

    return {
        "status": "M1_A327_MU8_PUBLIC_PACKET_TRIAGE_VERIFY_PASS",
        "path": str(path),
        "rank_one": check_rank_one(record),
        "rank2": check_rank2(record),
        "rank3": check_rank3(record),
        "witness_ledgers_scanned": witness["witness_ledgers_scanned"],
        "proof_status": record["proof_status"],
        "public_action": public["recommended_public_action"],
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
