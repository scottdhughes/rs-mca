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


def check_evidence_tracking(record: dict[str, Any]) -> dict[str, int]:
    tracking = record["evidence_tracking"]
    hashes = record["evidence_hashes_sha256"]
    tracked = tracking["tracked_files"]
    untracked = tracking["untracked_files"]
    missing = tracking["missing_files"]

    require(tracking["evidence_files_hashed"] == len(hashes), "evidence hash count mismatch")
    require(tracking["tracked_count"] == len(tracked), "tracked evidence count mismatch")
    require(tracking["untracked_count"] == len(untracked), "untracked evidence count mismatch")
    require(tracking["missing_count"] == len(missing), "missing evidence count mismatch")
    require(tracking["tracked_count"] + tracking["untracked_count"] == len(hashes), "tracked/untracked split mismatch")
    require(tracking["missing_count"] == 0, "triage references missing evidence")
    require(set(tracked).isdisjoint(set(untracked)), "tracked and untracked evidence overlap")
    require(set(tracked).union(set(untracked)) == set(hashes), "tracking paths do not match hashed evidence")
    require(tracking["untracked_count"] == 0, "triage still depends on untracked evidence")
    require(tracking["tracked_count"] == len(hashes), "not all hashed evidence is tracked")
    require(tracking["self_contained_for_public_pr"] is True, "public PR self-contained flag should be true")
    return {
        "tracked_count": tracking["tracked_count"],
        "untracked_count": tracking["untracked_count"],
        "missing_count": tracking["missing_count"],
    }


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

    non_singleton = rank3["non_singleton_synthesized_dependency"]
    require(non_singleton["present"] is True, "rank-3 non-singleton synthesized summary missing")
    require(non_singleton["header_ok"] is True, "rank-3 non-singleton header failed")
    require(non_singleton["anchors"] == 35, "rank-3 non-singleton anchor count changed")
    require(non_singleton["carriers_emitted"] == 6, "rank-3 synthesized carrier count changed")
    require(non_singleton["support_pair_candidates"] == 2, "rank-3 non-singleton support/pair count changed")
    require(non_singleton["best_min_support"] >= TARGET, "rank-3 non-singleton support below target")
    require(non_singleton["best_total_incidence"] >= REQUIRED_TOTAL, "rank-3 non-singleton total below target")
    require(non_singleton["best_pair_count_max"] <= 255, "rank-3 non-singleton pair cap failed")
    require(non_singleton["exact_best_nullity"] == 0, "rank-3 non-singleton exact nullity changed")
    require(non_singleton["depmin2_support_pair_candidates"] == 1, "rank-3 depmin2 support/pair count changed")
    require(non_singleton["depmin2_best_min_support"] >= TARGET, "rank-3 depmin2 support below target")
    require(non_singleton["depmin2_best_total_incidence"] >= REQUIRED_TOTAL, "rank-3 depmin2 total below target")
    require(non_singleton["depmin2_pair_count_max"] <= 255, "rank-3 depmin2 pair cap failed")
    require(non_singleton["depmin2_exact_best_nullity"] == 0, "rank-3 depmin2 exact nullity changed")
    require(non_singleton["depmin3_support_pair_candidates"] == 0, "rank-3 depmin3 unexpectedly passed")
    require(non_singleton["depmin3_best_min_support"] == 323, "rank-3 depmin3 boundary changed")
    require(non_singleton["depmin3_best_total_incidence"] == 2266, "rank-3 depmin3 total changed")
    require(non_singleton["depmin3_selected_incidence_gap"] == 23, "rank-3 depmin3 gap changed")
    require(non_singleton["depmin4_support_pair_candidates"] == 0, "rank-3 depmin4 unexpectedly passed")
    require(non_singleton["depmin4_best_min_support"] == 311, "rank-3 depmin4 boundary changed")
    require(non_singleton["depmin4_best_total_incidence"] == 2182, "rank-3 depmin4 total changed")
    require(non_singleton["depmin4_selected_incidence_gap"] == 107, "rank-3 depmin4 gap changed")

    blocked = rank3["singleton_blocked_current"]
    support_first = blocked["support_first"]
    require(support_first["present"] is True, "rank-3 singleton-blocked support-first missing")
    require(support_first["header_ok"] is True, "rank-3 singleton-blocked support-first header failed")
    require(support_first["support_pair_candidates"] >= 1, "rank-3 singleton-blocked should pass support/pair")
    require(support_first["best_support_pair_min_support"] >= TARGET, "rank-3 singleton-blocked support below target")
    require(support_first["best_support_pair_total_incidence"] >= REQUIRED_TOTAL, "rank-3 singleton-blocked total below target")
    require(support_first["best_support_pair_pair_count_max"] <= 255, "rank-3 singleton-blocked pair cap failed")

    blocked_exact = blocked["exact"]
    require(blocked_exact["present"] is True, "rank-3 singleton-blocked exact missing")
    require(blocked_exact["header_ok"] is True, "rank-3 singleton-blocked exact header failed")
    require(blocked_exact["systems_tested"] == 1, "rank-3 singleton-blocked exact systems changed")
    require(blocked_exact["best_nullity"] == 0, "rank-3 singleton-blocked exact nullity changed")
    require(blocked_exact["positive_nullity_systems"] == 0, "rank-3 singleton-blocked positive nullity")

    blocked_pressure = blocked["row_pressure"]
    require(blocked_pressure["present"] is True, "rank-3 singleton-blocked row pressure missing")
    require(blocked_pressure["header_ok"] is True, "rank-3 singleton-blocked row pressure header failed")
    require(blocked_pressure["systems_tested"] == 1, "rank-3 singleton-blocked row pressure systems changed")
    require(blocked_pressure["best_nullity"] == 0, "rank-3 singleton-blocked pressure nullity changed")
    require(blocked_pressure["positive_nullity_systems"] == 0, "rank-3 singleton-blocked pressure positive nullity")
    require(blocked_pressure["first_system_matrix_shape"] == [155, 96], "rank-3 singleton-blocked pressure shape changed")
    require(blocked_pressure["first_system_rank"] == 96, "rank-3 singleton-blocked pressure rank changed")
    require(blocked_pressure["first_system_nullity"] == 0, "rank-3 singleton-blocked pressure nullity mismatch")
    require(blocked_pressure["rank_drop_histogram"] == {"0": 64}, "rank-3 singleton-blocked rank-drop histogram changed")
    require(blocked_pressure["greedy_core_row_count"] == 96, "rank-3 singleton-blocked greedy core rows changed")
    require(blocked_pressure["greedy_core_rank"] == 96, "rank-3 singleton-blocked greedy core rank changed")

    repeat = blocked["repeat_pressure"]
    require(repeat["present"] is True, "rank-3 singleton-blocked repeat pressure missing")
    require(repeat["header_ok"] is True, "rank-3 singleton-blocked repeat pressure header failed")
    require(repeat["support_pair_candidates"] == 0, "rank-3 singleton-blocked repeat pressure unexpectedly passed")
    require(repeat["near_front_candidates"] == 0, "rank-3 singleton-blocked repeat pressure unexpectedly near-front")
    require(repeat["min_projective_key_count"] == 2, "rank-3 singleton-blocked repeat min key count changed")
    require(repeat["best_paircap_min_support"] == 296, "rank-3 singleton-blocked repeat paircap support changed")
    require(repeat["best_paircap_total_incidence"] == 2072, "rank-3 singleton-blocked repeat paircap total changed")
    require(repeat["best_paircap_pair_count_max"] == 255, "rank-3 singleton-blocked repeat paircap max changed")

    core_smoke = rank3["core_dependency_smoke"]
    require(core_smoke["present"] is True, "rank-3 core-dependency smoke missing")
    require(core_smoke["header_ok"] is True, "rank-3 core-dependency smoke header failed")
    require(core_smoke["anchor_targets"] == 128, "rank-3 core-dependency anchor count changed")
    require(core_smoke["replacement_rows"] == 72, "rank-3 core-dependency replacement rows changed")
    require(core_smoke["support_pair_replacements"] == 72, "rank-3 core-dependency support/pair replacements changed")
    require(core_smoke["carriers_emitted"] == 2, "rank-3 core-dependency carrier count changed")
    require(core_smoke["support_pair_candidates"] == 1, "rank-3 core-dependency support/pair count changed")
    require(core_smoke["best_support_pair_min_support"] >= TARGET, "rank-3 core-dependency support below target")
    require(core_smoke["best_support_pair_total_incidence"] >= REQUIRED_TOTAL, "rank-3 core-dependency total below target")
    require(core_smoke["best_support_pair_pair_count_max"] <= 255, "rank-3 core-dependency pair cap failed")
    require(core_smoke["exact_best_nullity"] == 0, "rank-3 core-dependency exact nullity changed")
    require(core_smoke["exact_positive_nullity_systems"] == 0, "rank-3 core-dependency positive nullity")
    require(core_smoke["row_pressure_best_nullity"] == 0, "rank-3 core-dependency row pressure nullity changed")
    require(core_smoke["witness_constructed"] is False, "rank-3 core-dependency unexpectedly constructed witness")

    core_nogoods = rank3["generic_core_nogoods"]
    require(core_nogoods["nogoods_present"] is True, "rank-3 generic core no-goods missing")
    require(core_nogoods["schedule_present"] is True, "rank-3 core-no-good schedule missing")
    require(core_nogoods["pressure_present"] is True, "rank-3 core-no-good pressure missing")
    nogoods = core_nogoods["nogoods"]
    require(nogoods["header_ok"] is True, "rank-3 generic core no-good header failed")
    require(nogoods["pressure_files_scanned"] >= 30, "rank-3 no-good pressure file count changed")
    require(nogoods["pressure_systems_scanned"] >= 79, "rank-3 no-good pressure system count changed")
    require(
        nogoods["eligible_dependency_free_full_rank_systems"] >= 56,
        "rank-3 no-good eligible system count changed",
    )
    require(nogoods["unique_core_nogoods"] >= 54, "rank-3 unique no-good count changed")
    require(
        nogoods["singleton_projective_core_nogoods"] >= 54,
        "rank-3 singleton no-good count changed",
    )
    guarded = core_nogoods["guarded_schedule"]
    require(guarded["header_ok"] is True, "rank-3 guarded no-good schedule header failed")
    require(guarded["forbid_core_subsets"] is True, "rank-3 guarded schedule did not forbid core subsets")
    require(guarded["support_pair_candidates"] >= 2, "rank-3 guarded schedule lost support/pair")
    require(guarded["best_min_support"] >= TARGET, "rank-3 guarded schedule support below target")
    require(guarded["best_total_incidence"] >= REQUIRED_TOTAL, "rank-3 guarded schedule total below target")
    require(guarded["best_pair_count_max"] <= 255, "rank-3 guarded schedule pair cap failed")
    require(guarded["best_core_nogood_constraints"] >= 1, "rank-3 guarded schedule did not hit no-good")
    require(
        guarded["best_max_selected_projective_key_support"] <= 1,
        "rank-3 guarded schedule unexpectedly left singleton-projective regime",
    )
    core_exact = core_nogoods["exact"]
    require(core_exact["present"] is True, "rank-3 core-no-good exact missing")
    require(core_exact["header_ok"] is True, "rank-3 core-no-good exact header failed")
    require(core_exact["systems_tested"] == 2, "rank-3 core-no-good exact systems changed")
    require(core_exact["best_nullity"] == 0, "rank-3 core-no-good exact nullity changed")
    require(core_exact["positive_nullity_systems"] == 0, "rank-3 core-no-good positive nullity")
    require(core_exact["pair_visible_systems"] == 0, "rank-3 core-no-good pair-visible system")
    followup = core_nogoods["followup_pressure"]
    require(followup["header_ok"] is True, "rank-3 core-no-good pressure header failed")
    require(followup["systems_tested"] == 2, "rank-3 core-no-good pressure systems changed")
    require(followup["best_nullity"] == 0, "rank-3 core-no-good pressure nullity changed")
    require(followup["positive_nullity_systems"] == 0, "rank-3 core-no-good pressure positive nullity")
    require(followup["dependency_free_pivot_cores"] >= 1, "rank-3 core-no-good did not find fresh generic core")
    require(
        followup["singleton_projective_systems"] == 2,
        "rank-3 core-no-good pressure left singleton-projective regime",
    )
    return {
        "exact_systems_tested": exact["systems_tested_total"],
        "row_pressure_systems_tested": pressure["systems_tested_total"],
        "singleton22_candidates": singleton["22"]["support_pair_candidates"],
        "non_singleton_support_pair_candidates": non_singleton["support_pair_candidates"],
        "depmin2_support_pair_candidates": non_singleton["depmin2_support_pair_candidates"],
        "depmin3_support_total": [
            non_singleton["depmin3_best_min_support"],
            non_singleton["depmin3_best_total_incidence"],
        ],
        "singleton_blocked_support_pair_candidates": support_first["support_pair_candidates"],
        "singleton_blocked_repeat_paircap_front": [
            repeat["best_paircap_min_support"],
            repeat["best_paircap_total_incidence"],
        ],
        "core_dependency_smoke": [
            core_smoke["carriers_emitted"],
            core_smoke["support_pair_candidates"],
            core_smoke["exact_best_nullity"],
        ],
        "generic_core_nogoods": [
            nogoods["unique_core_nogoods"],
            guarded["support_pair_candidates"],
            core_exact["best_nullity"],
            followup["dependency_free_pivot_cores"],
        ],
    }


def verify(path: Path) -> dict[str, Any]:
    record = load_json(path)
    check_header(record)
    check_evidence_hashes(record)
    evidence_tracking = check_evidence_tracking(record)

    public = record["public_packet_triage"]
    require(public["board_ready"] is False, "packet should not be board-ready")
    require(public["exact_a327_witness"] is False, "packet unexpectedly claims exact witness")
    require(public["recommended_public_action"] == "open_narrow_route_cut_pr_if_desired", "wrong public action")
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
        "evidence_tracking": evidence_tracking,
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
