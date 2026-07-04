#!/usr/bin/env python3
"""Search small row-block syzygies inside M1 a=327 collision-budget profiles."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "856d30a"
PREVIOUS_DATA = Path("experimental/data/m1_a327_ledger_codesign_collision_budget_codesign.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_collision_budget_syzygy_search.json")

ROOT = Path(__file__).resolve().parents[2]
CBUDGET_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_ledger_codesign_collision_budget_codesign.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
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
    "global obstruction outside the tested collision-budget syzygy front",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cbudget = load_module("ledger_codesign_collision_budget_codesign", CBUDGET_SCRIPT)
exactrow = cbudget.exactrow
rowdep = cbudget.rowdep
lcodesign = cbudget.lcodesign
pfcoll = cbudget.pfcoll


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def rank_mod_numpy(matrix: Any, prime: int = PROXY_PRIME) -> int:
    import numpy as np

    work = np.asarray(matrix, dtype=np.int64) % prime
    nrows, ncols = work.shape
    rank = 0
    for col in range(ncols):
        nonzero = np.flatnonzero(work[rank:, col] % prime)
        if nonzero.size == 0:
            continue
        pivot = rank + int(nonzero[0])
        if pivot != rank:
            work[[rank, pivot]] = work[[pivot, rank]]
        inv = pow(int(work[rank, col]), -1, prime)
        work[rank, :] = (work[rank, :] * inv) % prime
        if rank + 1 < nrows:
            below = np.flatnonzero(work[rank + 1 :, col] % prime) + rank + 1
            if below.size:
                factors = work[below, col].copy()
                work[below, :] = (work[below, :] - factors[:, None] * work[rank, :]) % prime
        rank += 1
        if rank == nrows:
            break
    return int(rank)


def proxy_matrix_with_metadata(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    h_values: list[int],
    powers: list[list[int]],
    prime: int = PROXY_PRIME,
) -> tuple[Any, list[dict[str, Any]]]:
    import numpy as np

    classes = pfcoll.feedback.zstable.functional.functional_classes(candidate)
    classes_by_index = {int(row["class_index"]): row for row in classes}
    positions_by_index = pfcoll.feedback.class_position_sets(classes)
    basis_indices = [int(idx) for idx in profile["basis_class_indices"]]
    blocks, ncols = pfcoll.feedback.basis_blocks(classes_by_index, basis_indices)
    powers_np = np.asarray(powers, dtype=np.int64)
    z_evals = {
        int(class_index): pfcoll.feedback.z_evals_for_support(positions_by_index[int(class_index)], h_values, prime)
        for class_index in basis_indices
    }
    nrows = sum(int(row["support_size"]) for row in profile["nonbasis_constraint_detail"])
    matrix = np.zeros((nrows, ncols), dtype=np.int64)
    metadata: list[dict[str, Any]] = []
    row_index = 0
    for constraint_order, constraint in enumerate(profile["nonbasis_constraint_detail"]):
        class_index = int(constraint["class_index"])
        coords = [int(value) % prime for value in constraint["basis_coordinates"]]
        support_hash = classes_by_index[class_index]["positions_hash"]
        for pos in positions_by_index[class_index]:
            for basis_slot, basis_class_index in enumerate(basis_indices):
                scalar = coords[basis_slot]
                if scalar == 0:
                    continue
                z_eval = z_evals[basis_class_index][pos]
                if z_eval == 0:
                    continue
                block = blocks[basis_class_index]
                start = block["start"]
                q_degree = block["q_degree_bound"]
                matrix[row_index, start : start + q_degree] = (
                    matrix[row_index, start : start + q_degree]
                    + scalar * z_eval * powers_np[:q_degree, pos]
                ) % prime
            metadata.append(
                {
                    "row_index": row_index,
                    "constraint_order": constraint_order,
                    "class_index": class_index,
                    "position": int(pos),
                    "support_hash": support_hash,
                    "basis_coordinates": coords,
                }
            )
            row_index += 1
    return matrix, metadata


def normalized_row_key(row: Any, prime: int = PROXY_PRIME) -> bytes:
    import numpy as np

    values = np.asarray(row, dtype=np.int64) % prime
    nonzero = np.flatnonzero(values)
    if nonzero.size == 0:
        return b"ZERO"
    pivot = int(nonzero[0])
    inv = pow(int(values[pivot]), -1, prime)
    normalized = (values * inv) % prime
    return normalized.astype(np.uint16).tobytes()


def row_block_metrics(matrix: Any, metadata: list[dict[str, Any]]) -> dict[str, Any]:
    import numpy as np

    nrows, ncols = matrix.shape
    zero_rows = int(np.sum(np.all(matrix % PROXY_PRIME == 0, axis=1)))
    projective_counts = Counter(normalized_row_key(matrix[idx, :]) for idx in range(nrows))
    projective_duplicate_groups = sum(1 for count in projective_counts.values() if count > 1)
    projective_duplicate_pairs = sum(count * (count - 1) // 2 for count in projective_counts.values() if count > 1)
    max_projective_multiplicity = max(projective_counts.values(), default=0)

    by_position: dict[int, list[int]] = defaultdict(list)
    by_support: dict[str, list[int]] = defaultdict(list)
    by_support_position: dict[tuple[str, int], list[int]] = defaultdict(list)
    for info in metadata:
        idx = int(info["row_index"])
        pos = int(info["position"])
        support_hash = str(info["support_hash"])
        by_position[pos].append(idx)
        by_support[support_hash].append(idx)
        by_support_position[(support_hash, pos)].append(idx)

    def lowrank_summary(groups: list[list[int]], max_size: int) -> tuple[int, int, int, int]:
        lowrank_groups = 0
        deficiency = 0
        tested = 0
        best_rank = 0
        for indices in groups:
            if len(indices) < 2:
                continue
            block_indices = indices[:max_size]
            block = matrix[block_indices, :]
            rank = rank_mod_numpy(block, PROXY_PRIME)
            tested += 1
            best_rank = max(best_rank, rank)
            if rank < len(block_indices):
                lowrank_groups += 1
                deficiency += len(block_indices) - rank
        return tested, lowrank_groups, deficiency, best_rank

    pos_tested, pos_lowrank, pos_def, pos_best_rank = lowrank_summary(
        [rows for rows in by_position.values() if len(rows) >= 3],
        4,
    )
    support_pos_tested, support_pos_lowrank, support_pos_def, support_pos_best_rank = lowrank_summary(
        [rows for rows in by_support_position.values() if len(rows) >= 2],
        4,
    )
    support_tested, support_lowrank, support_def, support_best_rank = lowrank_summary(
        [rows for rows in by_support.values() if len(rows) >= 3],
        4,
    )

    syzygy_score = (
        1000 * zero_rows
        + 500 * projective_duplicate_pairs
        + 200 * support_pos_def
        + 80 * pos_def
        + 50 * support_def
    )
    return {
        "row_block_rows": int(nrows),
        "row_block_cols": int(ncols),
        "zero_rows": zero_rows,
        "projective_duplicate_groups": projective_duplicate_groups,
        "projective_duplicate_pairs": projective_duplicate_pairs,
        "max_projective_multiplicity": int(max_projective_multiplicity),
        "position_blocks_tested": pos_tested,
        "position_lowrank_blocks": pos_lowrank,
        "position_lowrank_deficiency": pos_def,
        "position_best_rank": pos_best_rank,
        "support_position_blocks_tested": support_pos_tested,
        "support_position_lowrank_blocks": support_pos_lowrank,
        "support_position_lowrank_deficiency": support_pos_def,
        "support_position_best_rank": support_pos_best_rank,
        "support_blocks_tested": support_tested,
        "support_lowrank_blocks": support_lowrank,
        "support_lowrank_deficiency": support_def,
        "support_best_rank": support_best_rank,
        "syzygy_score": syzygy_score,
        "syzygy_positive": syzygy_score > 0,
    }


def syzygy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        not bool(row["syzygy_positive"]),
        -int(row["syzygy_score"]),
        -int(row["projective_duplicate_pairs"]),
        -int(row["support_position_lowrank_deficiency"]),
        -int(row["position_lowrank_deficiency"]),
        -int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        not bool(row["syzygy_positive"]),
        -int(row["syzygy_score"]),
        -int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def build_record(
    max_templates: int,
    max_systems: int,
    profile_candidate_limit: int,
    groups_per_candidate: int,
    syzygy_profile_limit: int,
    proxy_rank_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    front = rowdep.build_front(max_templates=max_templates, max_systems=max_systems)
    ordered_front = sorted(front, key=lambda item: lcodesign.structural_sort_key(item[1]))[:profile_candidate_limit]
    preferences = [
        "low_support_basis",
        "low_support_not_group_support",
        "mid_support_rank",
        "q_budget_then_span",
    ]
    h_values = pfcoll.feedback.proxy_h_values(PROXY_PRIME)
    powers = pfcoll.feedback.precompute_powers_mod(h_values, PROXY_PRIME)

    profile_rows: list[dict[str, Any]] = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    for candidate_order, (candidate, structural) in enumerate(ordered_front):
        for profile_order, (profile, meta) in enumerate(
            cbudget.collision_budget_profiles(candidate, candidate_order, groups_per_candidate, preferences)
        ):
            row = cbudget.profile_row(candidate, profile, candidate_order, profile_order, meta)
            row["source_system_order"] = structural["system_order"]
            if not row["collision_budget_success"]:
                continue
            profile_rows.append(row)
            source_profiles[(candidate_order, row["basis_id"])] = (candidate, profile)

    scored_rows = []
    for row in sorted(profile_rows, key=cbudget.collision_budget_sort_key)[:syzygy_profile_limit]:
        candidate, profile = source_profiles[(int(row["candidate_order"]), row["basis_id"])]
        matrix, metadata = proxy_matrix_with_metadata(candidate, profile, h_values, powers, PROXY_PRIME)
        scored_rows.append({**row, **row_block_metrics(matrix, metadata)})

    syzygy_positive = [row for row in scored_rows if row["syzygy_positive"]]
    rank_targets = sorted(syzygy_positive, key=syzygy_sort_key)[:proxy_rank_limit]
    proxy_rows = []
    for target in rank_targets:
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
                    "SYZYGY_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "SYZYGY_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best_scored = min(scored_rows, key=syzygy_sort_key) if scored_rows else None
    best_syzygy = min(syzygy_positive, key=syzygy_sort_key) if syzygy_positive else None
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

    failure = "SYZYGY_NO_SCORED_PROFILES"
    proof_status = "EXACT_EXTRACTION_NO_A327 / SYZYGY_NO_SCORED_PROFILES / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "SYZYGY_PROXY_POSITIVE" if positives else "SYZYGY_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / SYZYGY_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / SYZYGY_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )
    elif syzygy_positive:
        failure = "SYZYGY_PROXY_NOT_RUN"
        proof_status = "CANDIDATE / SYZYGY_PROXY_NOT_RUN / PARTIAL / EXPERIMENTAL"
    elif scored_rows:
        failure = "SYZYGY_NO_SMALL_ROW_BLOCK_DEPENDENCY"
        proof_status = "EXACT_EXTRACTION_NO_A327 / SYZYGY_NO_SMALL_ROW_BLOCK_DEPENDENCY / PARTIAL / EXPERIMENTAL"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_collision_budget_codesign": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "basis_profiles_constructed": previous["collision_budget_codesign"]["basis_profiles_constructed"],
            "collision_budget_profiles": previous["collision_budget_codesign"]["collision_budget_profiles"],
            "proxy_ranked_profiles": previous["collision_budget_codesign"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["collision_budget_codesign"]["proxy_positive_profiles"],
            "best_q_variable_count": previous["collision_budget_codesign"]["best_q_variable_count"],
            "best_proxy_rank": previous["collision_budget_codesign"]["best_proxy_rank"],
            "best_proxy_nullity": previous["collision_budget_codesign"]["best_proxy_nullity"],
            "failure_mode": previous["collision_budget_codesign"]["best_failure_mode"],
        },
        "collision_budget_syzygy_search": {
            "proxy_prime": PROXY_PRIME,
            "q_variable_floor": Q_VARIABLE_FLOOR,
            "max_templates": max_templates,
            "max_systems": max_systems,
            "profile_candidate_limit": profile_candidate_limit,
            "groups_per_candidate": groups_per_candidate,
            "syzygy_profile_limit": syzygy_profile_limit,
            "proxy_rank_limit": proxy_rank_limit,
            "collision_budget_profiles_reconstructed": len(profile_rows),
            "syzygy_profiles_scored": len(scored_rows),
            "syzygy_positive_profiles": len(syzygy_positive),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_syzygy_score": None if best_scored is None else best_scored["syzygy_score"],
            "best_projective_duplicate_pairs": None if best_scored is None else best_scored["projective_duplicate_pairs"],
            "best_position_lowrank_deficiency": None if best_scored is None else best_scored["position_lowrank_deficiency"],
            "best_support_position_lowrank_deficiency": (
                None if best_scored is None else best_scored["support_position_lowrank_deficiency"]
            ),
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_scored_profile": best_scored,
        "best_syzygy_profile": best_syzygy,
        "best_profile": best,
        "best_candidate": best_candidate,
        "proxy_ranked_profiles": sorted(proxy_rows, key=proxy_sort_key),
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
    parser.add_argument("--groups-per-candidate", type=int, default=8)
    parser.add_argument("--syzygy-profile-limit", type=int, default=80)
    parser.add_argument("--proxy-rank-limit", type=int, default=12)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_systems=args.max_systems,
        profile_candidate_limit=args.profile_candidate_limit,
        groups_per_candidate=args.groups_per_candidate,
        syzygy_profile_limit=args.syzygy_profile_limit,
        proxy_rank_limit=args.proxy_rank_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["collision_budget_syzygy_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "collision_budget_profiles_reconstructed": search["collision_budget_profiles_reconstructed"],
                    "syzygy_profiles_scored": search["syzygy_profiles_scored"],
                    "syzygy_positive_profiles": search["syzygy_positive_profiles"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_syzygy_score": search["best_syzygy_score"],
                    "best_projective_duplicate_pairs": search["best_projective_duplicate_pairs"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_COLLISION_BUDGET_SYZYGY_SEARCH_READY")


if __name__ == "__main__":
    main()
