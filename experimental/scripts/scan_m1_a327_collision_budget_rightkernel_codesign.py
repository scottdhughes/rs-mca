#!/usr/bin/env python3
"""Codesign collision-budget profiles with coefficient right kernels for M1 a=327.

The default pass reuses the 240 committed collision-budget profiles from the
previous front. Exhaustive basis enumeration is available as an explicit mode,
but it is heavier because local profile feature extraction is not cheap.
"""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "0108539"
PREVIOUS_DATA = Path("experimental/data/m1_a327_collision_budget_syzygy_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_collision_budget_rightkernel_codesign.json")

ROOT = Path(__file__).resolve().parents[2]
SYZYGY_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_collision_budget_syzygy_search.py"
ORTOOLS_PYTHON = Path("/Users/scott/.venvs/rs-mca-ortools/bin/python")

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
P = 17
TEMPLATE_DIM = 6
Q_VARIABLE_FLOOR = 350

REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested collision-budget right-kernel front",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


syzygy = load_module("collision_budget_syzygy_search", SYZYGY_SCRIPT)
cbudget = syzygy.cbudget
exactrow = cbudget.exactrow
rowdep = cbudget.rowdep
lcodesign = cbudget.lcodesign
pfcoll = cbudget.pfcoll


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_rows(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> int:
    matrix = [[int(value) % prime for value in row] for row in rows if any(int(value) % prime for value in row)]
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % prime:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % prime:
                continue
            factor = matrix[row_idx][col] % prime
            matrix[row_idx] = [
                (matrix[row_idx][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        rank += 1
        if rank == len(matrix) or rank == ncols:
            break
    return rank


def rref_rows(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> tuple[list[list[int]], list[int]]:
    matrix = [[int(value) % prime for value in row] for row in rows if any(int(value) % prime for value in row)]
    rank = 0
    pivots: list[int] = []
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % prime:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row_idx in range(len(matrix)):
            if row_idx == rank or not matrix[row_idx][col] % prime:
                continue
            factor = matrix[row_idx][col] % prime
            matrix[row_idx] = [
                (matrix[row_idx][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(matrix) or rank == ncols:
            break
    return matrix[:rank], pivots


def nullspace_basis(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> list[list[int]]:
    rref, pivots = rref_rows(rows, ncols=ncols, prime=prime)
    pivot_set = set(pivots)
    free_cols = [idx for idx in range(ncols) if idx not in pivot_set]
    basis: list[list[int]] = []
    for free in free_cols:
        vec = [0] * ncols
        vec[free] = 1
        for row, pivot in zip(rref, pivots, strict=True):
            vec[pivot] = (-row[free]) % prime
        basis.append(vec)
    return basis


def normalize_projective(row: list[int], prime: int = P) -> tuple[int, ...]:
    values = [int(value) % prime for value in row]
    for value in values:
        if value:
            inv = pow(value, -1, prime)
            return tuple((entry * inv) % prime for entry in values)
    return tuple(values)


def coefficient_rightkernel_metrics(profile: dict[str, Any]) -> dict[str, Any]:
    rows = [
        [int(value) % P for value in item["basis_coordinates"]]
        for item in profile["nonbasis_constraint_detail"]
    ]
    rank = rank_rows(rows, ncols=len(profile["basis_class_indices"]), prime=P)
    kernel = nullspace_basis(rows, ncols=len(profile["basis_class_indices"]), prime=P)
    projective_kernel = [list(normalize_projective(row, P)) for row in kernel if any(row)]
    return {
        "coefficient_row_count": len(rows),
        "coefficient_rank": rank,
        "coefficient_right_kernel_nullity": len(profile["basis_class_indices"]) - rank,
        "coefficient_right_kernel_basis": projective_kernel,
        "coefficient_right_kernel_projective_first": projective_kernel[0] if projective_kernel else None,
    }


def tools_status() -> dict[str, Any]:
    if not ORTOOLS_PYTHON.exists():
        return {
            "ortools_python": str(ORTOOLS_PYTHON),
            "ortools_available": False,
            "ortools_version": None,
            "cp_sat_smoke": False,
            "used_for": "not_available",
        }
    code = (
        "from ortools.sat.python import cp_model\n"
        "import ortools\n"
        "m=cp_model.CpModel(); x=m.NewBoolVar('x'); m.Add(x==1)\n"
        "s=cp_model.CpSolver(); status=s.Solve(m)\n"
        "print(ortools.__version__); print(int(status)); print(s.Value(x))\n"
    )
    try:
        completed = subprocess.run(
            [str(ORTOOLS_PYTHON), "-c", code],
            check=True,
            text=True,
            capture_output=True,
            timeout=20,
        )
        lines = completed.stdout.strip().splitlines()
        return {
            "ortools_python": str(ORTOOLS_PYTHON),
            "ortools_available": True,
            "ortools_version": lines[0] if lines else None,
            "cp_sat_smoke": len(lines) >= 3 and lines[-1] == "1",
            "used_for": "available_for_next_cp_sat_allocation; not_required_for_current_committed_profile_enumeration",
        }
    except Exception as exc:  # pragma: no cover - diagnostic only
        return {
            "ortools_python": str(ORTOOLS_PYTHON),
            "ortools_available": False,
            "ortools_version": None,
            "cp_sat_smoke": False,
            "used_for": f"smoke_failed:{type(exc).__name__}",
        }


def exhaustive_basis_profiles(candidate: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    classes = pfcoll.feedback.zstable.functional.functional_classes(candidate)
    out: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for combo_order, selected in enumerate(itertools.combinations(range(len(classes)), TEMPLATE_DIM)):
        basis_id = "rkcodesign_basis_" + "_".join(str(classes[idx]["class_index"]) for idx in selected)
        profile = exactrow.profile_from_selected(classes, list(selected), basis_id)
        if profile is None:
            continue
        out.append(
            (
                profile,
                {
                    "basis_search": "exhaustive_rank6_functional_classes",
                    "basis_combo_order": combo_order,
                    "basis_combo_count": None,
                    "functional_class_count": len(classes),
                },
            )
        )
    total = len(out)
    return [(profile, {**meta, "basis_combo_count": total}) for profile, meta in out]


def committed_collision_budget_profiles(
    candidate: dict[str, Any],
    candidate_order: int,
    groups_per_candidate: int,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    preferences = [
        "low_support_basis",
        "low_support_not_group_support",
        "mid_support_rank",
        "q_budget_then_span",
    ]
    return cbudget.collision_budget_profiles(candidate, candidate_order, groups_per_candidate, preferences)


def rightkernel_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        not bool(row["rightkernel_collision_budget_success"]),
        -int(row["coefficient_right_kernel_nullity"]),
        -int(row["q_variable_count"]),
        -int(row["repeated_support_coordinate_pairs"]),
        -int(row["repeated_support_pairs"]),
        -int(row["repeated_coordinate_pairs"]),
        int(row["row_surplus"]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        not bool(row["rightkernel_collision_budget_success"]),
        -int(row["coefficient_right_kernel_nullity"]),
        -int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def compact_row(row: dict[str, Any] | None) -> dict[str, Any] | None:
    if row is None:
        return None
    keys = [
        "template_id",
        "candidate_order",
        "source_system_order",
        "basis_id",
        "basis_class_indices",
        "basis_support_sizes",
        "q_variable_count",
        "matrix_shape",
        "support_vector",
        "pair7_counts",
        "max_pair_count",
        "functional_span_rank",
        "forced_functional_identities",
        "exact_collision_positive",
        "collision_budget_success",
        "coefficient_row_count",
        "coefficient_rank",
        "coefficient_right_kernel_nullity",
        "coefficient_right_kernel_projective_first",
        "rightkernel_collision_budget_success",
        "proxy_prime",
        "proxy_matrix_shape",
        "proxy_rank",
        "proxy_nullity",
        "best_failure_mode",
        "repeated_support_coordinate_pairs",
        "repeated_support_pairs",
        "repeated_coordinate_pairs",
        "row_surplus",
    ]
    return {key: row.get(key) for key in keys if key in row}


def build_record(
    max_templates: int,
    max_systems: int,
    profile_candidate_limit: int,
    proxy_rank_limit: int,
    groups_per_candidate: int,
    basis_mode: str,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    front = rowdep.build_front(max_templates=max_templates, max_systems=max_systems)
    ordered_front = sorted(front, key=lambda item: lcodesign.structural_sort_key(item[1]))[:profile_candidate_limit]

    profile_rows: list[dict[str, Any]] = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    combo_counts: Counter[int] = Counter()
    rank_counts: Counter[int] = Counter()
    kernel_nullity_counts: Counter[int] = Counter()

    for candidate_order, (candidate, structural) in enumerate(ordered_front):
        if basis_mode == "exhaustive":
            profiles = exhaustive_basis_profiles(candidate)
        elif basis_mode == "committed_collision_budget":
            profiles = committed_collision_budget_profiles(candidate, candidate_order, groups_per_candidate)
        else:
            raise ValueError(f"unknown basis mode {basis_mode}")
        combo_counts[len(pfcoll.feedback.zstable.functional.functional_classes(candidate))] += len(profiles)
        for profile_order, (profile, meta) in enumerate(profiles):
            row = cbudget.profile_row(candidate, profile, candidate_order, profile_order, meta)
            row["source_system_order"] = structural["system_order"]
            metrics = coefficient_rightkernel_metrics(profile)
            row.update(metrics)
            rank_counts[int(metrics["coefficient_rank"])] += 1
            kernel_nullity_counts[int(metrics["coefficient_right_kernel_nullity"])] += 1
            row["rightkernel_collision_budget_success"] = bool(
                row["collision_budget_success"] and int(row["coefficient_right_kernel_nullity"]) > 0
            )
            profile_rows.append(row)
            source_profiles[(candidate_order, row["basis_id"])] = (candidate, profile)

    collision_budget_profiles = [row for row in profile_rows if row["collision_budget_success"]]
    rightkernel_profiles = [row for row in profile_rows if row["rightkernel_collision_budget_success"]]
    targets = sorted(rightkernel_profiles, key=rightkernel_sort_key)[:proxy_rank_limit]

    h_values = pfcoll.feedback.proxy_h_values(PROXY_PRIME)
    powers = pfcoll.feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    proxy_rows = []
    for target in targets:
        candidate, profile = source_profiles[(int(target["candidate_order"]), target["basis_id"])]
        proxy = pfcoll.feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
        proxy_rows.append(
            {
                **target,
                "proxy_prime": proxy["proxy_prime"],
                "proxy_matrix_shape": proxy["matrix_shape"],
                "proxy_rank": proxy["proxy_rank"],
                "proxy_nullity": proxy["proxy_nullity"],
                "best_failure_mode": (
                    "RKERNEL_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "RKERNEL_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best_rightkernel = min(rightkernel_profiles, key=rightkernel_sort_key) if rightkernel_profiles else None
    best_collision_budget = min(collision_budget_profiles, key=rightkernel_sort_key) if collision_budget_profiles else None
    best = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    best_candidate = None
    if best is not None:
        candidate, _profile = source_profiles[(int(best["candidate_order"]), best["basis_id"])]
        best_candidate = {
            **pfcoll.feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
            "template_vectors": candidate["template_vectors"],
            "selected_count_hash": candidate["selected_count_hash"],
            "selected_class_size_counts": candidate["selected_class_size_counts"],
            "total_effective_cost": candidate["total_effective_cost"],
        }

    failure = "RKERNEL_NO_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / RKERNEL_NO_PROFILES / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "RKERNEL_PROXY_POSITIVE" if positives else "RKERNEL_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / RKERNEL_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / RKERNEL_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )
    elif rightkernel_profiles:
        failure = "RKERNEL_PROXY_NOT_RUN"
        proof_status = "CANDIDATE / RKERNEL_PROXY_NOT_RUN / PARTIAL / EXPERIMENTAL"
    elif collision_budget_profiles:
        failure = "RKERNEL_COEFFICIENT_FULL_RANK"
        proof_status = "EXACT_EXTRACTION_NO_A327 / RKERNEL_COEFFICIENT_FULL_RANK / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_collision_budget_syzygy_search": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "collision_budget_profiles_reconstructed": previous["collision_budget_syzygy_search"][
                "collision_budget_profiles_reconstructed"
            ],
            "syzygy_profiles_scored": previous["collision_budget_syzygy_search"]["syzygy_profiles_scored"],
            "syzygy_positive_profiles": previous["collision_budget_syzygy_search"]["syzygy_positive_profiles"],
            "proxy_ranked_profiles": previous["collision_budget_syzygy_search"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["collision_budget_syzygy_search"]["proxy_positive_profiles"],
            "best_failure_mode": previous["collision_budget_syzygy_search"]["best_failure_mode"],
        },
        "tools": tools_status(),
        "collision_budget_rightkernel_codesign": {
            "proxy_prime": PROXY_PRIME,
            "coefficient_prime": P,
            "q_variable_floor": Q_VARIABLE_FLOOR,
            "max_templates": max_templates,
            "max_systems": max_systems,
            "profile_candidate_limit": profile_candidate_limit,
            "groups_per_candidate": groups_per_candidate,
            "basis_mode": basis_mode,
            "proxy_rank_limit": proxy_rank_limit,
            "structural_pass_systems": len(front),
            "candidates_scanned": len(ordered_front),
            "basis_profiles_constructed": len(profile_rows),
            "functional_class_combo_profile_counts": dict(combo_counts),
            "coefficient_rank_counts": dict(rank_counts),
            "coefficient_kernel_nullity_counts": dict(kernel_nullity_counts),
            "collision_budget_profiles": len(collision_budget_profiles),
            "rightkernel_collision_budget_profiles": len(rightkernel_profiles),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_rightkernel_q_variable_count": None if best_rightkernel is None else best_rightkernel["q_variable_count"],
            "best_rightkernel_coefficient_nullity": (
                None if best_rightkernel is None else best_rightkernel["coefficient_right_kernel_nullity"]
            ),
            "best_collision_budget_q_variable_count": (
                None if best_collision_budget is None else best_collision_budget["q_variable_count"]
            ),
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_rightkernel_profile": compact_row(best_rightkernel),
        "best_collision_budget_profile": compact_row(best_collision_budget),
        "best_profile": compact_row(best),
        "best_candidate": best_candidate,
        "proxy_ranked_profiles": [compact_row(row) | {
            "proxy_prime": row["proxy_prime"],
            "proxy_matrix_shape": row["proxy_matrix_shape"],
            "proxy_rank": row["proxy_rank"],
            "proxy_nullity": row["proxy_nullity"],
            "best_failure_mode": row["best_failure_mode"],
        } for row in sorted(proxy_rows, key=proxy_sort_key)],
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": REQUIRED_NONCLAIMS,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-templates", type=int, default=128)
    parser.add_argument("--max-systems", type=int, default=360)
    parser.add_argument("--profile-candidate-limit", type=int, default=60)
    parser.add_argument("--proxy-rank-limit", type=int, default=12)
    parser.add_argument("--groups-per-candidate", type=int, default=8)
    parser.add_argument(
        "--basis-mode",
        choices=["committed_collision_budget", "exhaustive"],
        default="committed_collision_budget",
    )
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_systems=args.max_systems,
        profile_candidate_limit=args.profile_candidate_limit,
        proxy_rank_limit=args.proxy_rank_limit,
        groups_per_candidate=args.groups_per_candidate,
        basis_mode=args.basis_mode,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["collision_budget_rightkernel_codesign"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "basis_profiles_constructed": search["basis_profiles_constructed"],
                    "collision_budget_profiles": search["collision_budget_profiles"],
                    "rightkernel_collision_budget_profiles": search["rightkernel_collision_budget_profiles"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_rightkernel_q_variable_count": search["best_rightkernel_q_variable_count"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                    "ortools_available": record["tools"]["ortools_available"],
                    "ortools_version": record["tools"]["ortools_version"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_COLLISION_BUDGET_RIGHTKERNEL_CODESIGN_READY")


if __name__ == "__main__":
    main()
