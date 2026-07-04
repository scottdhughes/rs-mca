#!/usr/bin/env python3
"""Search cycle-guarded chambers with basis-quotient proxy rank defect."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "cf761a0"
FRONT_CHECKPOINT_COMMIT = "0fc5a00"
PREVIOUS_DATA = Path("experimental/data/m1_a327_cycleguard_stable_window_exact_audit.json")
FRONT_DATA = Path("experimental/data/m1_a327_cycle_guarded_template_front_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_rankdefect_feedback_search.json")

ROOT = Path(__file__).resolve().parents[2]
CYCLEG_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycle_guarded_template_front_search.py"

P = 17
N = 512
K = 256
TARGET_AGREEMENT = 327
TEMPLATE_DIM = 6
PROXY_PRIME = 12289  # 12289 - 1 is divisible by 512.


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cycleg = load_module("cycle_guarded_template_front_search", CYCLEG_SCRIPT)
p456 = cycleg.p456
tchamber = cycleg.tchamber
zstable = cycleg.zstable


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def factorize(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root_mod_prime(prime: int) -> int:
    factors = sorted(set(factorize(prime - 1)))
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise RuntimeError("primitive root not found")


def proxy_h_values(prime: int = PROXY_PRIME) -> list[int]:
    generator = primitive_root_mod_prime(prime)
    root = pow(generator, (prime - 1) // N, prime)
    return [pow(root, idx, prime) for idx in range(N)]


def precompute_powers_mod(h_values: list[int], prime: int = PROXY_PRIME) -> list[list[int]]:
    powers = [[1 for _ in range(N)]]
    for _degree in range(1, K):
        previous = powers[-1]
        powers.append([(previous[pos] * h_values[pos]) % prime for pos in range(N)])
    return powers


def z_evals_for_support(support: list[int], h_values: list[int], prime: int = PROXY_PRIME) -> list[int]:
    roots = [h_values[int(pos)] for pos in support]
    out = []
    for value in h_values:
        acc = 1
        for root in roots:
            acc = (acc * (value - root)) % prime
        out.append(acc)
    return out


def modular_rank_sparse(rows: list[dict[int, int]], ncols: int, prime: int) -> int:
    basis: dict[int, dict[int, int]] = {}
    rank = 0
    for raw in rows:
        row = dict(raw)
        while row:
            pivot = min(row)
            if pivot not in basis:
                inv = pow(row[pivot], prime - 2, prime)
                basis[pivot] = {col: (value * inv) % prime for col, value in row.items()}
                rank += 1
                break
            factor = row[pivot]
            pivot_row = basis[pivot]
            for col, value in pivot_row.items():
                new_value = (row.get(col, 0) - factor * value) % prime
                if new_value:
                    row[col] = new_value
                elif col in row:
                    del row[col]
        if rank == ncols:
            break
    return rank


def modular_rank_dense_numpy(matrix: Any, prime: int) -> int:
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


def class_position_sets(classes: list[dict[str, Any]]) -> dict[int, list[int]]:
    return {
        int(row["class_index"]): [int(pos) for pos in row["positions"]]
        for row in classes
    }


def basis_blocks(classes_by_index: dict[int, dict[str, Any]], basis_indices: list[int]) -> tuple[dict[int, dict[str, int]], int]:
    blocks: dict[int, dict[str, int]] = {}
    cursor = 0
    for slot, class_index in enumerate(basis_indices):
        support_size = int(classes_by_index[int(class_index)]["support_size"])
        q_degree = K - support_size
        if q_degree <= 0:
            raise RuntimeError(f"nonpositive q-degree for basis class {class_index}")
        blocks[int(class_index)] = {
            "basis_slot": slot,
            "start": cursor,
            "q_degree_bound": q_degree,
            "support_size": support_size,
        }
        cursor += q_degree
    return blocks, cursor


def proxy_basis_quotient_rank(
    candidate: dict[str, Any],
    profile: dict[str, Any],
    h_values: list[int],
    powers: list[list[int]],
    prime: int = PROXY_PRIME,
) -> dict[str, Any]:
    import numpy as np

    classes = zstable.functional.functional_classes(candidate)
    classes_by_index = {int(row["class_index"]): row for row in classes}
    positions_by_index = class_position_sets(classes)
    basis_indices = [int(idx) for idx in profile["basis_class_indices"]]
    blocks, ncols = basis_blocks(classes_by_index, basis_indices)
    powers_np = np.asarray(powers, dtype=np.int64)
    z_evals = {
        int(class_index): z_evals_for_support(positions_by_index[int(class_index)], h_values, prime)
        for class_index in basis_indices
    }

    nrows = sum(int(row["support_size"]) for row in profile["nonbasis_constraint_detail"])
    matrix = np.zeros((nrows, ncols), dtype=np.int64)
    row_index = 0
    for constraint in profile["nonbasis_constraint_detail"]:
        class_index = int(constraint["class_index"])
        coords = [int(value) % prime for value in constraint["basis_coordinates"]]
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
            row_index += 1

    rank = modular_rank_dense_numpy(matrix, prime)
    nullity = ncols - rank
    return {
        "proxy_prime": prime,
        "matrix_shape": [int(nrows), ncols],
        "proxy_rank": rank,
        "proxy_nullity": nullity,
        "proxy_failure_mode": (
            "CYCLEG_RANKDEFECT_PROXY_POSITIVE"
            if nullity > 0
            else "CYCLEG_RANKDEFECT_PROXY_FULL_RANK"
        ),
    }


def compact_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": int(candidate["assignment_seed"]),
        "template_family": candidate["template_family"],
        "template_dimension": int(candidate["template_dimension"]),
        "support_vector": [int(value) for value in candidate["support_vector"]],
        "pair7_counts": [int(value) for value in candidate["pair7_counts"]],
        "max_pair_count": int(candidate["max_pair_count"]),
        "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        "template_vectors_hash": hash_payload(candidate["template_vectors"]),
    }


def reconstruct_summary(summary: dict[str, Any], front: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    target_mutation = summary["mutation_id"]
    specs = p456.ninerow.mutation_specs(max_mutations=front["cycle_guarded_template_front"]["max_mutations"])
    spec = next((row for row in specs if row.get("mutation_id") == target_mutation), None)
    if spec is None:
        raise RuntimeError(f"could not find mutation spec {target_mutation}")
    template_profile = p456.lowrank.solve_template_counts(spec)
    candidate = p456.diverse.candidate_from_profile(
        template_profile,
        summary["assignment_strategy"],
        seed=int(summary["assignment_seed"]),
    )
    candidate["mutation_id"] = spec.get("mutation_id")
    candidate["base_template_id"] = spec.get("base_template_id")
    profile = None
    for basis_profile in tchamber.basis_profiles(
        candidate,
        top_classes=front["cycle_guarded_template_front"]["top_classes"],
        random_bases=front["cycle_guarded_template_front"]["random_bases"],
        limit=front["cycle_guarded_template_front"]["max_basis_profiles"],
    ):
        if basis_profile["basis_id"] == summary["basis_id"]:
            profile = basis_profile
            break
    if profile is None:
        raise RuntimeError(f"could not reconstruct basis profile {summary['basis_id']}")
    if [int(value) for value in profile["basis_class_indices"]] != [int(value) for value in summary["basis_class_indices"]]:
        raise RuntimeError("basis class reconstruction mismatch")
    return candidate, profile


def compact_profile(candidate: dict[str, Any], profile: dict[str, Any], summary: dict[str, Any], proxy: dict[str, Any]) -> dict[str, Any]:
    chamber_row = (
        summary.get("best_exact_pairclear_rank_slack_chamber")
        or summary.get("best_exact_pairclear_chamber")
        or summary.get("best_cycle_clear_rank_slack_chamber")
        or summary.get("best_cycle_clear_chamber")
    )
    return {
        "template_id": candidate["template_id"],
        "mutation_id": candidate.get("mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": int(candidate["assignment_seed"]),
        "basis_id": profile["basis_id"],
        "basis_class_indices": [int(idx) for idx in profile["basis_class_indices"]],
        "basis_support_sizes": [int(value) for value in profile["basis_support_sizes"]],
        "q_variable_count": int(profile["q_variable_count"]),
        "planned_matrix_shape": [int(value) for value in profile["matrix_shape"]],
        "exact_pairclear_rank_slack_chamber": summary.get("best_exact_pairclear_rank_slack_chamber"),
        "best_chamber_direction": None if chamber_row is None else chamber_row.get("direction"),
        "best_chamber_zero_row_count": None if chamber_row is None else chamber_row.get("zero_row_count"),
        "best_chamber_inactive_rank": None if chamber_row is None else chamber_row.get("inactive_rank"),
        "best_chamber_forced_pairs": None if chamber_row is None else chamber_row.get("forced_pairs"),
        "proxy_prime": proxy["proxy_prime"],
        "proxy_matrix_shape": proxy["matrix_shape"],
        "proxy_rank": proxy["proxy_rank"],
        "proxy_nullity": proxy["proxy_nullity"],
        "best_failure_mode": proxy["proxy_failure_mode"],
    }


def profile_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        -int(row["best_chamber_zero_row_count"] or 0),
        int(row["best_chamber_inactive_rank"] or 99),
        row["template_id"],
        row["basis_id"],
    )


def build_record(
    rank_profile_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    front = load_json(FRONT_DATA)
    h_values = proxy_h_values(PROXY_PRIME)
    powers = precompute_powers_mod(h_values, PROXY_PRIME)

    summaries = [
        row
        for row in front["profile_summaries"]
        if row.get("best_failure_mode") == "CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK"
    ]
    rank_targets = summaries[:rank_profile_limit]
    ranked = []
    reconstructed = []
    for summary in rank_targets:
        candidate, profile = reconstruct_summary(summary, front)
        proxy = proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
        ranked.append(compact_profile(candidate, profile, summary, proxy))
        reconstructed.append((candidate, profile, summary))

    positives = [row for row in ranked if int(row["proxy_nullity"]) > 0]
    best = min(ranked, key=profile_sort_key) if ranked else None
    best_full_candidate = None
    if best is not None:
        for candidate, profile, _summary in reconstructed:
            if (
                candidate["template_id"] == best["template_id"]
                and profile["basis_id"] == best["basis_id"]
                and int(candidate["assignment_seed"]) == int(best["assignment_seed"])
            ):
                best_full_candidate = candidate
                break

    failure = "CYCLEG_RANKDEFECT_NO_EXACT_PAIRCLEAR_RANKSLACK"
    proof_status = "EXACT_EXTRACTION_NO_A327 / CYCLEG_RANKDEFECT_NO_EXACT_PAIRCLEAR_RANKSLACK / PARTIAL / EXPERIMENTAL"
    if ranked:
        failure = "CYCLEG_RANKDEFECT_PROXY_POSITIVE" if positives else "CYCLEG_RANKDEFECT_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / CYCLEG_RANKDEFECT_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / CYCLEG_RANKDEFECT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_exact_audit": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "matrix_shape": previous["basis_quotient_audit"]["best_matrix_shape"],
            "rank": previous["basis_quotient_audit"]["best_rank"],
            "nullity": previous["basis_quotient_audit"]["best_nullity"],
            "failure_mode": previous["basis_quotient_audit"]["best_failure_mode"],
        },
        "rankdefect_feedback_search": {
            "proxy_prime": PROXY_PRIME,
            "front_checkpoint_commit": FRONT_CHECKPOINT_COMMIT,
            "front_source_commit": front["source_commit"],
            "front_profile_summaries": len(front["profile_summaries"]),
            "rank_profile_limit": rank_profile_limit,
            "front_basis_profiles_tested": front["cycle_guarded_template_front"]["basis_profiles_tested"],
            "front_exact_pairclear_rank_slack_profiles": front["cycle_guarded_template_front"]["exact_pairclear_rank_slack_profiles"],
            "exact_pairclear_rank_slack_summaries": len(summaries),
            "proxy_ranked_profiles": len(ranked),
            "proxy_positive_profiles": len(positives),
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in ranked)),
        },
        "best_profile": best,
        "best_candidate": None if best_full_candidate is None else {
            **compact_candidate(best_full_candidate),
            "coordinate_classes": best_full_candidate["coordinate_classes"],
        },
        "ranked_profiles": sorted(ranked, key=profile_sort_key)[:40],
        "candidate": {
            "constructed": False,
            "seven_distinct": False,
            "agreement_vector": None,
            "received_word_hash": None,
            "codeword_hashes": None,
        },
        "proof_status": proof_status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "Sage GF(17^32) exact lift",
            "MCA/protocol consequence from this list-track proxy",
            "global obstruction outside the tested cycle-guarded rank-defect feedback front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--rank-profile-limit", type=int, default=40)
    args = parser.parse_args()
    record = build_record(
        rank_profile_limit=args.rank_profile_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["rankdefect_feedback_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "front_basis_profiles_tested": search["front_basis_profiles_tested"],
                    "front_exact_pairclear_rank_slack_profiles": search["front_exact_pairclear_rank_slack_profiles"],
                    "exact_pairclear_rank_slack_summaries": search["exact_pairclear_rank_slack_summaries"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_proxy_rank": search["best_proxy_rank"],
                    "best_proxy_nullity": search["best_proxy_nullity"],
                    "best_template_id": None if record["best_profile"] is None else record["best_profile"]["template_id"],
                    "best_basis_id": None if record["best_profile"] is None else record["best_profile"]["basis_id"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_CYCLEGUARD_RANKDEFECT_FEEDBACK_SEARCH_READY")


if __name__ == "__main__":
    main()
