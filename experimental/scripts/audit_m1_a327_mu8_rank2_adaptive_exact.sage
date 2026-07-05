#!/usr/bin/env sage
"""Exact interpolation audit for adaptive rank-2 mu_8 schedules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


BASE_SCRIPT = Path("experimental/scripts/audit_m1_a327_mu8_rank2_cpsat_exact.sage")
ADAPTIVE_SCHEDULE_INPUT = Path("experimental/data/m1_a327_mu8_rank2_adaptive_schedule_candidates.json")
NEAR_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_adaptive_near_front_exact.json")
EXACT_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_adaptive_exact_interpolation.json")
WITNESS_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_adaptive_witness_audit.json")
SOURCE_COMMIT = "14684a5"

ns = dict(globals())
ns["__name__"] = "rank2_adaptive_base"
exec(compile(BASE_SCRIPT.read_text(), str(BASE_SCRIPT), "exec"), ns)

TARGET_AGREEMENT = ns["TARGET_AGREEMENT"]
NOT_CLAIMED = ns["NOT_CLAIMED"]
BASE_NS = ns["ns"]


def ratio_line_metadata(candidate):
    counts = {}
    for choice in candidate.get("chosen_options", []):
        if choice.get("kind") == "RATIO" and choice.get("ratio_key"):
            key = str(choice["ratio_key"])
            counts[key] = counts.get(key, 0) + 1
    histogram = {
        str(size): sum(1 for value in counts.values() if value == size)
        for size in sorted(set(counts.values()))
    }
    forced = sorted(key for key, value in counts.items() if value >= 32)
    return {
        "ratio_line_support_histogram": histogram,
        "max_ratio_line_support": max(counts.values(), default=0),
        "forced_global_ratio_lines": forced,
        "rank_one_collapse_risk": bool(forced),
    }


def mapped_kernel_status(status):
    if status == "MU8_RANK2_CARRIER_PAIR_VISIBLE":
        return "MU8_RANK2_KERNEL_PAIR_VISIBLE"
    if status in ("MU8_RANK2_CARRIER_PAIR_FORCED", "MU8_RANK2_CARRIER_MIXED_PAIR_FORCED"):
        return "MU8_RANK2_KERNEL_PAIR_FORCED"
    return status


def audit_candidate(candidate, menu_record, F, omega, gamma, support_required):
    plane = ns["lookup_plane"](menu_record, candidate["plane_id"])
    u = BASE_NS["vector_from_ints"](F, plane["u"])
    v = BASE_NS["vector_from_ints"](F, plane["v"])
    rows, metadata = ns["interpolation_rows_for_candidate"](F, omega, plane, candidate)
    matrix = Matrix(F, rows) if rows else Matrix(F, 0, 64)
    rank = int(matrix.rank())
    nullity = int(matrix.ncols() - rank)
    forced_pairs = []
    kernel_status = None
    witness = None
    status = "MU8_RANK2_ADAPTIVE_NEAR_FRONT_DIAGNOSTIC"
    if support_required:
        status = "MU8_RANK2_SUPPORT_PAIR_PASS_INTERPOLATION_FULL_RANK"
    if nullity > 0:
        kernel_basis = matrix.right_kernel().basis()
        raw_kernel_status, forced_pairs = BASE_NS["classify_kernel"](kernel_basis, u, v, gamma)
        kernel_status = mapped_kernel_status(raw_kernel_status)
        if support_required:
            status = "MU8_RANK2_SUPPORT_PAIR_PASS_INTERPOLATION_NULLITY"
            if kernel_status == "MU8_RANK2_KERNEL_PAIR_FORCED":
                status = "MU8_RANK2_KERNEL_PAIR_FORCED"
            elif kernel_status == "MU8_RANK2_KERNEL_PAIR_VISIBLE":
                status = "MU8_RANK2_KERNEL_PAIR_VISIBLE"
                vec = BASE_NS["deterministic_avoidance"](kernel_basis, u, v, gamma)
                if vec is not None:
                    witness = BASE_NS["verify_witness"](
                        vec,
                        ns["convert_candidate_for_witness"](candidate),
                        u,
                        v,
                        omega,
                        gamma,
                    )
                    witness["candidate_id"] = candidate["candidate_id"]
                    witness["plane_id"] = candidate["plane_id"]
    ratio_meta = ratio_line_metadata(candidate)
    row = {
        "candidate_id": candidate["candidate_id"],
        "plane_id": candidate["plane_id"],
        "near_front": bool(candidate.get("near_front")),
        "support_pair_pass": bool(candidate.get("support_pair_pass")),
        "min_support": candidate.get("min_support"),
        "selected_incidence_total": candidate.get("selected_incidence_total"),
        "pair_count_max": candidate.get("pair_count_max"),
        "row_cost": candidate.get("row_cost"),
        "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
        "rank": rank,
        "nullity": nullity,
        "kernel_status": kernel_status,
        "forced_equal_pairs": forced_pairs,
        "row_metadata_hash": BASE_NS["hash_payload"](metadata),
        "status": status,
    }
    row.update(ratio_meta)
    return row, witness


def build_empty_witness():
    return {
        "constructed": False,
        "seven_distinct": False,
        "agreement_vector": None,
        "min_agreement": None,
        "status": "NO_EXACT_WITNESS_CONSTRUCTED",
    }


def audit(candidate_limit, near_limit):
    with ADAPTIVE_SCHEDULE_INPUT.open() as handle:
        schedule_record = json.load(handle)
    ratio_limit = int(schedule_record["adaptive_schedule_candidates"].get("menu_ratio_limit", 32))
    plane_limit = int(schedule_record["adaptive_schedule_candidates"].get("plane_limit", 64))
    candidates = schedule_record.get("candidates", [])
    support_candidates = []
    near_candidates = []
    seen_support = set()
    seen_near = set()
    for row in candidates:
        key = row.get("candidate_id")
        if row.get("support_pair_pass") and key not in seen_support and len(support_candidates) < candidate_limit:
            seen_support.add(key)
            support_candidates.append(row)
        elif row.get("near_front") and not row.get("support_pair_pass") and key not in seen_near and len(near_candidates) < near_limit:
            seen_near.add(key)
            near_candidates.append(row)
    menu_record = ns["build_menu_record"](plane_limit=plane_limit, ratio_limit=ratio_limit)
    F, omega, gamma = ns["exact_context"]()
    near_rows = []
    exact_rows = []
    witness = None
    for candidate in near_candidates:
        row, _ = audit_candidate(candidate, menu_record, F, omega, gamma, support_required=False)
        near_rows.append(row)
    for candidate in support_candidates:
        row, candidate_witness = audit_candidate(candidate, menu_record, F, omega, gamma, support_required=True)
        exact_rows.append(row)
        if witness is None and candidate_witness is not None:
            witness = candidate_witness
    near_positive = [row for row in near_rows if row["nullity"] > 0]
    exact_positive = [row for row in exact_rows if row["nullity"] > 0]
    near_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "near_front_exact": {
            "field": "GF(17^32)",
            "systems_tested": len(near_rows),
            "positive_nullity_systems": len(near_positive),
            "best_nullity": max([row["nullity"] for row in near_rows], default=0),
            "diagnostic_only": True,
            "best_failure_mode": (
                "MU8_RANK2_ADAPTIVE_NEAR_FRONT_DIAGNOSTIC"
                if near_rows
                else "MU8_RANK2_ADAPTIVE_NO_NEAR_FRONT_CANDIDATE"
            ),
        },
        "systems": near_rows,
        "proof_status": (
            "CANDIDATE / MU8_RANK2_ADAPTIVE_NEAR_FRONT_DIAGNOSTIC / PARTIAL / EXPERIMENTAL"
            if near_rows
            else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_ADAPTIVE_NO_NEAR_FRONT_CANDIDATE / PARTIAL / EXPERIMENTAL"
        ),
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    exact_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "exact_interpolation": {
            "field": "GF(17^32)",
            "systems_tested": len(exact_rows),
            "positive_nullity_systems": len(exact_positive),
            "pair_visible_systems": sum(1 for row in exact_rows if row["status"] == "MU8_RANK2_KERNEL_PAIR_VISIBLE"),
            "best_nullity": max([row["nullity"] for row in exact_rows], default=0),
            "best_failure_mode": (
                "MU8_RANK2_SUPPORT_PAIR_PASS_INTERPOLATION_NULLITY"
                if exact_positive
                else "MU8_RANK2_SUPPORT_PAIR_PASS_INTERPOLATION_FULL_RANK"
                if exact_rows
                else "MU8_RANK2_ADAPTIVE_NO_SUPPORT_PAIR_CANDIDATE"
            ),
        },
        "systems": exact_rows,
        "proof_status": (
            "CANDIDATE / MU8_RANK2_SUPPORT_PAIR_PASS_INTERPOLATION_NULLITY / PARTIAL / EXPERIMENTAL"
            if exact_positive
            else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_SUPPORT_PAIR_PASS_INTERPOLATION_FULL_RANK / PARTIAL / EXPERIMENTAL"
            if exact_rows
            else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_ADAPTIVE_NO_SUPPORT_PAIR_CANDIDATE / PARTIAL / EXPERIMENTAL"
        ),
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    witness_pass = (
        witness is not None
        and witness["seven_distinct"]
        and witness["raw_selected_class_rows_ok"]
        and witness["min_agreement"] >= TARGET_AGREEMENT
    )
    witness_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "witness_audit": witness if witness is not None else build_empty_witness(),
        "proof_status": (
            "PROOF_RECORD / EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS / EXPERIMENTAL"
            if witness_pass
            else "EXACT_EXTRACTION_NO_A327 / NO_EXACT_WITNESS_CONSTRUCTED / PARTIAL / EXPERIMENTAL"
        ),
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    return near_record, exact_record, witness_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--candidate-limit", type=int, default=32)
    parser.add_argument("--near-limit", type=int, default=16)
    args = parser.parse_args()
    near_record, exact_record, witness_record = audit(args.candidate_limit, args.near_limit)
    if args.write_json:
        NEAR_OUTPUT.write_text(json.dumps(BASE_NS["jsonable"](near_record), indent=2, sort_keys=True) + "\n")
        EXACT_OUTPUT.write_text(json.dumps(BASE_NS["jsonable"](exact_record), indent=2, sort_keys=True) + "\n")
        WITNESS_OUTPUT.write_text(json.dumps(BASE_NS["jsonable"](witness_record), indent=2, sort_keys=True) + "\n")
    summary = {
        "near_status": near_record["proof_status"],
        "exact_status": exact_record["proof_status"],
        "witness_status": witness_record["proof_status"],
        "near_systems_tested": near_record["near_front_exact"]["systems_tested"],
        "support_pair_systems_tested": exact_record["exact_interpolation"]["systems_tested"],
        "near_best_nullity": near_record["near_front_exact"]["best_nullity"],
        "exact_best_nullity": exact_record["exact_interpolation"]["best_nullity"],
    }
    if args.json:
        print(json.dumps(BASE_NS["jsonable"](summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_MU8_RANK2_ADAPTIVE_EXACT_READY")


if __name__ == "__main__":
    main()
