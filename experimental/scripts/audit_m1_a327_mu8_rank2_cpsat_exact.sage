#!/usr/bin/env sage
"""Exact menu builder and interpolation audit for rank-2 mu_8 CP-SAT schedules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


BASE_SCRIPT = Path("experimental/scripts/audit_m1_a327_mu8_rank2_carrier_exact.sage")
MENU_INPUT = Path("experimental/data/m1_a327_mu8_rank2_carrier_menu_scan.json")
CPSAT_MENU_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_cpsat_menu.json")
CPSAT_SCHEDULE_INPUT = Path("experimental/data/m1_a327_mu8_rank2_cpsat_schedule_candidates.json")
EXACT_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_cpsat_exact_interpolation.json")
WITNESS_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_cpsat_witness_audit.json")

ns = dict(globals())
ns["__name__"] = "rank2_base"
exec(compile(BASE_SCRIPT.read_text(), str(BASE_SCRIPT), "exec"), ns)

P = ns["P"]
FIELD_DEGREE = ns["FIELD_DEGREE"]
H_ORDER = ns["H_ORDER"]
MU_ORDER = ns["MU_ORDER"]
QUOTIENT_ORDER = ns["QUOTIENT_ORDER"]
QUOTIENT_DEGREE_BOUND = ns["QUOTIENT_DEGREE_BOUND"]
TARGET_AGREEMENT = ns["TARGET_AGREEMENT"]
PAIR_CAP = ns["PAIR_CAP"]
NOT_CLAIMED = ns["NOT_CLAIMED"]
PAIR_LABELS = ns["PAIR_LABELS"]


def element_coeffs(value):
    poly = value.polynomial()
    return [int(poly[i]) if i <= poly.degree() else 0 for i in range(FIELD_DEGREE)]


def ratio_key(ratio):
    return ns["ratio_key"](ratio)


def partition_labels(values):
    return ns["partition_labels"](values)


def exact_context():
    F = ns["exact_field"]()
    gen = F.multiplicative_generator()
    omega = gen ** ((F.order() - 1) // H_ORDER)
    gamma = omega ** (H_ORDER // MU_ORDER)
    return F, omega, gamma


def phase_partitions_for_ratio(u, v, ratio, rep, gamma):
    parts = []
    for phase in range(MU_ORDER):
        values = [
            ns["value_for_label"](u, v, ratio, rep, gamma, phase, label)
            for label in range(7)
        ]
        parts.append(partition_labels(values))
    return parts


def build_plane_menus(F, omega, gamma, plane, ratio_limit):
    u = ns["vector_from_ints"](F, plane["u"])
    v = ns["vector_from_ints"](F, plane["v"])
    qrows = []
    for qidx in range(QUOTIENT_ORDER):
        rep = omega ** qidx
        options = []
        options.append(
            {
                "option_id": "ZERO_ALL",
                "kind": "ZERO",
                "row_cost": 2,
                "ratio_key": None,
                "phase_blocks": [[list(range(7))] for _ in range(MU_ORDER)],
            }
        )
        options.append(
            {
                "option_id": "FREE_SINGLETONS",
                "kind": "FREE",
                "row_cost": 0,
                "ratio_key": None,
                "phase_blocks": [[ [label] for label in range(7) ] for _ in range(MU_ORDER)],
            }
        )
        ratios = ns["ratio_candidates_for_qidx"](u, v, rep, gamma, ratio_limit)
        seen = set()
        for idx, ratio in enumerate(ratios):
            key = ratio_key(ratio)
            if key in seen:
                continue
            seen.add(key)
            options.append(
                {
                    "option_id": "RATIO_%03d" % idx,
                    "kind": "RATIO",
                    "row_cost": 1,
                    "ratio_key": key,
                    "ratio_coeffs": [element_coeffs(ratio[0]), element_coeffs(ratio[1])],
                    "phase_blocks": phase_partitions_for_ratio(u, v, ratio, rep, gamma),
                }
            )
        qrows.append({"qidx": qidx, "options": options})
    return qrows


def build_menu_record(plane_limit, ratio_limit):
    with MENU_INPUT.open() as handle:
        menu = json.load(handle)
    F, omega, gamma = exact_context()
    planes = []
    for plane in menu["carrier_planes"][:plane_limit]:
        planes.append(
            {
                "plane_id": plane["plane_id"],
                "u": plane["u"],
                "v": plane["v"],
                "left_vector_id": plane["left_vector_id"],
                "right_vector_id": plane["right_vector_id"],
                "quotient_points": build_plane_menus(F, omega, gamma, plane, ratio_limit),
            }
        )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "ddc7fe9",
        "menu": {
            "field": "GF(17^32)",
            "planes": len(planes),
            "quotient_points": QUOTIENT_ORDER,
            "ratio_limit": ratio_limit,
        },
        "planes": planes,
        "proof_status": "CANDIDATE / MU8_RANK2_CPSAT_MENU_READY / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }


def lookup_plane(menu_record, plane_id):
    for plane in menu_record["planes"]:
        if plane["plane_id"] == plane_id:
            return plane
    raise KeyError(plane_id)


def lookup_option(plane, qidx, option_id):
    for option in plane["quotient_points"][qidx]["options"]:
        if option["option_id"] == option_id:
            return option
    raise KeyError((plane["plane_id"], qidx, option_id))


def coeffs_to_element(F, coeffs):
    z = F.gen()
    total = F(0)
    for idx, coeff in enumerate(coeffs):
        if coeff:
            total += F(Integer(coeff)) * (z ** idx)
    return total


def ratio_from_option(F, option):
    if option["kind"] != "RATIO":
        return None
    return (
        coeffs_to_element(F, option["ratio_coeffs"][0]),
        coeffs_to_element(F, option["ratio_coeffs"][1]),
    )


def interpolation_rows_for_candidate(F, omega, plane, candidate):
    rows = []
    metadata = []
    for choice in candidate["chosen_options"]:
        qidx = int(choice["qidx"])
        option = lookup_option(plane, qidx, choice["option_id"])
        y = omega ** (MU_ORDER * qidx)
        powers = [y ** power for power in range(QUOTIENT_DEGREE_BOUND)]
        if option["kind"] == "ZERO":
            rows.append(powers + [F(0) for _ in range(QUOTIENT_DEGREE_BOUND)])
            rows.append([F(0) for _ in range(QUOTIENT_DEGREE_BOUND)] + powers)
            metadata.extend([{"qidx": qidx, "kind": "ZERO_F"}, {"qidx": qidx, "kind": "ZERO_G"}])
        elif option["kind"] == "RATIO":
            a, b = ratio_from_option(F, option)
            rows.append([b * value for value in powers] + [-a * value for value in powers])
            metadata.append({"qidx": qidx, "kind": "RATIO", "ratio_key": option["ratio_key"]})
    return rows, metadata


def convert_candidate_for_witness(candidate):
    converted = {"choices": []}
    for choice in candidate["chosen_options"]:
        converted["choices"].append(
            {
                "blocks_by_phase": choice["selected_blocks_by_phase"],
                "kind": choice["kind"],
            }
        )
    return converted


def audit_exact(candidate_limit):
    with CPSAT_SCHEDULE_INPUT.open() as handle:
        schedule_record = json.load(handle)
    ratio_limit = int(schedule_record["cpsat_scheduler"].get("ratio_limit", 4))
    plane_limit = int(schedule_record["cpsat_scheduler"].get("planes_solved", 64))
    guard_candidates = [row for row in schedule_record["candidates"] if row.get("guard_pass")][:candidate_limit]
    if guard_candidates:
        menu_record = build_menu_record(plane_limit=plane_limit, ratio_limit=ratio_limit)
    elif CPSAT_MENU_OUTPUT.exists():
        with CPSAT_MENU_OUTPUT.open() as handle:
            menu_record = json.load(handle)
    else:
        menu_record = build_menu_record(plane_limit=plane_limit, ratio_limit=ratio_limit)
    F, omega, gamma = exact_context()
    exact_rows = []
    witness = None
    for candidate in guard_candidates:
        plane = lookup_plane(menu_record, candidate["plane_id"])
        u = ns["vector_from_ints"](F, plane["u"])
        v = ns["vector_from_ints"](F, plane["v"])
        rows, metadata = interpolation_rows_for_candidate(F, omega, plane, candidate)
        matrix = Matrix(F, rows) if rows else Matrix(F, 0, 64)
        rank = int(matrix.rank())
        nullity = int(matrix.ncols() - rank)
        status = "MU8_RANK2_CARRIER_INTERPOLATION_FULL_RANK"
        forced_pairs = []
        if nullity > 0:
            kernel_basis = matrix.right_kernel().basis()
            status, forced_pairs = ns["classify_kernel"](kernel_basis, u, v, gamma)
            if status == "MU8_RANK2_CARRIER_PAIR_VISIBLE" and witness is None:
                vec = ns["deterministic_avoidance"](kernel_basis, u, v, gamma)
                if vec is not None:
                    audit_row = ns["verify_witness"](
                        vec,
                        convert_candidate_for_witness(candidate),
                        u,
                        v,
                        omega,
                        gamma,
                    )
                    audit_row["candidate_id"] = candidate["candidate_id"]
                    audit_row["plane_id"] = candidate["plane_id"]
                    witness = audit_row
        exact_rows.append(
            {
                "candidate_id": candidate["candidate_id"],
                "plane_id": candidate["plane_id"],
                "matrix_shape": [int(matrix.nrows()), int(matrix.ncols())],
                "rank": rank,
                "nullity": nullity,
                "forced_equal_pairs": forced_pairs,
                "row_metadata_hash": ns["hash_payload"](metadata),
                "status": status,
            }
        )
    exact_positive = [row for row in exact_rows if row["nullity"] > 0]
    exact_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "ddc7fe9",
        "exact_interpolation": {
            "field": "GF(17^32)",
            "systems_tested": len(exact_rows),
            "positive_nullity_systems": len(exact_positive),
            "pair_visible_systems": sum(1 for row in exact_rows if row["status"] == "MU8_RANK2_CARRIER_PAIR_VISIBLE"),
            "best_nullity": max([row["nullity"] for row in exact_rows], default=0),
            "best_failure_mode": (
                "MU8_RANK2_CARRIER_INTERPOLATION_NULLITY"
                if exact_positive
                else "MU8_RANK2_CARRIER_INTERPOLATION_FULL_RANK"
                if exact_rows
                else "MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE"
            ),
        },
        "systems": exact_rows,
        "proof_status": (
            "CANDIDATE / MU8_RANK2_CARRIER_INTERPOLATION_NULLITY / PARTIAL / EXPERIMENTAL"
            if exact_positive
            else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_INTERPOLATION_FULL_RANK / PARTIAL / EXPERIMENTAL"
            if exact_rows
            else "EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_EXACT_CANDIDATE / PARTIAL / EXPERIMENTAL"
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
        "source_commit": "ddc7fe9",
        "witness_audit": witness if witness is not None else {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "min_agreement": None,
            "status": "NO_EXACT_WITNESS_CONSTRUCTED",
        },
        "proof_status": (
            "PROOF_RECORD / EXACT_A327_INTERLEAVED_LIST_WITNESS_PASS / EXPERIMENTAL"
            if witness_pass
            else "EXACT_EXTRACTION_NO_A327 / NO_EXACT_WITNESS_CONSTRUCTED / PARTIAL / EXPERIMENTAL"
        ),
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    return exact_record, witness_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-menu-json", action="store_true")
    parser.add_argument("--write-json", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--plane-limit", type=int, default=64)
    parser.add_argument("--ratio-limit", type=int, default=12)
    parser.add_argument("--candidate-limit", type=int, default=32)
    args = parser.parse_args()
    if args.build_menu_json:
        record = build_menu_record(args.plane_limit, args.ratio_limit)
        CPSAT_MENU_OUTPUT.write_text(json.dumps(ns["jsonable"](record), indent=2, sort_keys=True) + "\n")
        summary = {
            "proof_status": record["proof_status"],
            "planes": record["menu"]["planes"],
            "ratio_limit": record["menu"]["ratio_limit"],
        }
        if args.json:
            print(json.dumps(summary, indent=2, sort_keys=True))
        return
    exact_record, witness_record = audit_exact(args.candidate_limit)
    if args.write_json:
        EXACT_OUTPUT.write_text(json.dumps(ns["jsonable"](exact_record), indent=2, sort_keys=True) + "\n")
        WITNESS_OUTPUT.write_text(json.dumps(ns["jsonable"](witness_record), indent=2, sort_keys=True) + "\n")
    summary = {
        "exact_status": exact_record["proof_status"],
        "witness_status": witness_record["proof_status"],
        "systems_tested": exact_record["exact_interpolation"]["systems_tested"],
        "best_nullity": exact_record["exact_interpolation"]["best_nullity"],
    }
    if args.json:
        print(json.dumps(ns["jsonable"](summary), indent=2, sort_keys=True))
    elif not args.write_json:
        print("SAGE_AUDIT_M1_A327_MU8_RANK2_CPSAT_EXACT_READY")


if __name__ == "__main__":
    main()
