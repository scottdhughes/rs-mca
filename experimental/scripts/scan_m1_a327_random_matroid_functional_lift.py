#!/usr/bin/env python3
"""Prepare the M1 a=327 random-matroid functional-lift ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "68a0780"
REPAIR_DATA = Path("experimental/data/m1_a327_lowrank_template_forced_identity_repair.json")
SEARCH_DATA = Path("experimental/data/m1_a327_lowrank_template_selected_class_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_random_matroid_functional_lift.json")

P = 17
PROXY_PRIME = 12289
K = 256
N = 512
TARGET_AGREEMENT = 327
LIST_SIZE = 7
TEMPLATE_DIM = 6


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def rref(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> tuple[list[list[int]], list[int]]:
    matrix = [[value % prime for value in row] for row in rows if any(value % prime for value in row)]
    pivots: list[int] = []
    rank = 0
    for col in range(ncols):
        pivot = None
        for row in range(rank, len(matrix)):
            if matrix[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, prime)
        matrix[rank] = [(value * inv) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][col] % prime:
                continue
            factor = matrix[row][col] % prime
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[rank][idx]) % prime
                for idx in range(ncols)
            ]
        pivots.append(col)
        rank += 1
        if rank == len(matrix):
            break
    return matrix[:rank], pivots


def rank_mod_p(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> int:
    return len(rref(rows, ncols=ncols, prime=prime)[0])


def normalize_projective(row: list[int], prime: int = P) -> tuple[int, ...]:
    reduced = [value % prime for value in row]
    for value in reduced:
        if value:
            inv = pow(value, -1, prime)
            return tuple((entry * inv) % prime for entry in reduced)
    raise ValueError("zero row has no projective normalization")


def row_basis_mod_p(vectors: list[list[int]], members: list[int], prime: int = P) -> list[list[int]]:
    if len(members) <= 1:
        return []
    anchor = [value % prime for value in vectors[int(members[0]) - 1]]
    rows = []
    for witness in members[1:]:
        rows.append([(vectors[int(witness) - 1][idx] - anchor[idx]) % prime for idx in range(len(anchor))])
    basis, _pivots = rref(rows, ncols=len(anchor), prime=prime)
    return basis


def solve_coordinates(row: list[int], basis_rows: list[list[int]], prime: int = P) -> list[int] | None:
    d = len(basis_rows)
    if d == 0:
        return [] if not any(value % prime for value in row) else None
    matrix = []
    for col in range(TEMPLATE_DIM):
        matrix.append([basis_rows[idx][col] % prime for idx in range(d)] + [row[col] % prime])
    rank = 0
    pivots: list[int] = []
    for col in range(d):
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
                for idx in range(d + 1)
            ]
        pivots.append(col)
        rank += 1
    for row_idx in range(rank, len(matrix)):
        if all(matrix[row_idx][col] % prime == 0 for col in range(d)) and matrix[row_idx][d] % prime:
            return None
    solution = [0] * d
    for row_idx, pivot in enumerate(pivots):
        solution[pivot] = matrix[row_idx][d] % prime
    return solution


def nullspace_basis(rows: list[list[int]], ncols: int = TEMPLATE_DIM, prime: int = P) -> list[list[int]]:
    basis, pivots = rref(rows, ncols=ncols, prime=prime)
    pivot_set = set(pivots)
    free_cols = [col for col in range(ncols) if col not in pivot_set]
    result = []
    for free_col in free_cols:
        vector = [0] * ncols
        vector[free_col] = 1
        for basis_row, pivot in reversed(list(zip(basis, pivots, strict=True))):
            acc = 0
            for col in free_cols:
                acc = (acc + basis_row[col] * vector[col]) % prime
            vector[pivot] = (-acc) % prime
        result.append(vector)
    return result


def independent_greedy(rows: list[list[int]], order: list[int], target_rank: int) -> list[int]:
    selected: list[int] = []
    selected_rows: list[list[int]] = []
    current_rank = 0
    for idx in order:
        trial_rank = rank_mod_p(selected_rows + [rows[idx]])
        if trial_rank > current_rank:
            selected.append(idx)
            selected_rows.append(rows[idx])
            current_rank = trial_rank
        if current_rank == target_rank:
            break
    return selected if current_rank == target_rank else []


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def find_survivor(repair: dict[str, Any], search: dict[str, Any]) -> dict[str, Any]:
    best = repair["best_candidate"]
    for candidate in search["lowrank_template_search"]["candidates"]:
        if (
            candidate["template_id"] == best["template_id"]
            and candidate["assignment_strategy"] == best["assignment_strategy"]
            and candidate["coordinate_classes_hash"] == best["coordinate_classes_hash"]
        ):
            return candidate
    raise RuntimeError("could not find full survivor candidate")


def functional_classes(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    vectors = candidate["template_vectors"]
    positions_by_functional: dict[tuple[int, ...], set[int]] = defaultdict(set)
    compressed_rows = 0
    for coord in sorted(candidate["coordinate_classes"], key=lambda row: int(row["position"])):
        members = [int(value) for value in coord["members"]]
        for row in row_basis_mod_p(vectors, members):
            key = normalize_projective(row)
            positions_by_functional[key].add(int(coord["position"]))
            compressed_rows += 1
    if compressed_rows != int(candidate["total_effective_cost"]):
        raise RuntimeError(f"compressed row mismatch: {compressed_rows} != {candidate['total_effective_cost']}")
    classes = []
    for idx, (functional, positions_set) in enumerate(
        sorted(positions_by_functional.items(), key=lambda item: (-len(item[1]), item[0]))
    ):
        positions = sorted(positions_set)
        classes.append(
            {
                "class_index": idx,
                "functional": list(functional),
                "support_size": len(positions),
                "forced_identity": len(positions) > K - 1,
                "quotient_variables": max(0, K - len(positions)),
                "positions": positions,
                "positions_hash": hash_payload(positions),
            }
        )
    return classes


def basis_orders(classes: list[dict[str, Any]]) -> dict[str, list[int]]:
    rows = [row["functional"] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    orders: dict[str, list[int]] = {
        "max_support_basis": sorted(range(len(classes)), key=lambda idx: (-supports[idx], rows[idx])),
        "min_support_basis": sorted(range(len(classes)), key=lambda idx: (supports[idx], rows[idx])),
        "balanced_support_basis": sorted(
            range(len(classes)),
            key=lambda idx: (abs(supports[idx] - 64), -supports[idx], rows[idx]),
        ),
    }
    for seed in range(8):
        rng = random.Random(seed)
        order = list(range(len(classes)))
        rng.shuffle(order)
        orders[f"random_seeded_basis_{seed}"] = order
    return orders


def basis_profiles(classes: list[dict[str, Any]], functional_span_rank: int) -> list[dict[str, Any]]:
    rows = [row["functional"] for row in classes]
    supports = [int(row["support_size"]) for row in classes]
    profiles = []
    seen: set[tuple[int, ...]] = set()
    for basis_id, order in basis_orders(classes).items():
        selected = independent_greedy(rows, order, target_rank=functional_span_rank)
        key = tuple(selected)
        if len(selected) != functional_span_rank or key in seen:
            continue
        seen.add(key)
        basis_rows = [rows[idx] for idx in selected]
        q_variable_count = sum(K - supports[idx] for idx in selected)
        nonbasis_rows = 0
        nonbasis_constraints = []
        for idx, row in enumerate(rows):
            if idx in selected:
                continue
            coords = solve_coordinates(row, basis_rows)
            if coords is None:
                raise RuntimeError("basis did not span functional class")
            nonbasis_rows += supports[idx]
            nonbasis_constraints.append(
                {
                    "class_index": int(classes[idx]["class_index"]),
                    "support_size": supports[idx],
                    "basis_coordinates": coords,
                }
            )
        profiles.append(
            {
                "basis_id": basis_id,
                "basis_class_indices": [int(classes[idx]["class_index"]) for idx in selected],
                "basis_functionals": [classes[idx]["functional"] for idx in selected],
                "basis_support_sizes": [supports[idx] for idx in selected],
                "q_variable_count": q_variable_count,
                "nonbasis_constraints": len(nonbasis_constraints),
                "matrix_shape": [nonbasis_rows, q_variable_count],
                "formal_nullity_lower_bound": max(0, q_variable_count - nonbasis_rows),
                "nonbasis_constraint_detail": nonbasis_constraints,
            }
        )
    return sorted(
        profiles,
        key=lambda row: (
            row["formal_nullity_lower_bound"],
            -row["matrix_shape"][0],
            -row["q_variable_count"],
        ),
        reverse=True,
    )


def primitive_root_mod_prime(prime: int) -> int:
    factors = [2, 3]
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise RuntimeError(f"no primitive root found for {prime}")


def rank_mod_prime_matrix(matrix: list[list[int]], ncols: int, prime: int) -> int:
    rows = [[value % prime for value in row] for row in matrix if any(value % prime for value in row)]
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(rows)):
            if rows[row_idx][col] % prime:
                pivot = row_idx
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, prime)
        rows[rank] = [(value * inv) % prime for value in rows[rank]]
        for row_idx in range(len(rows)):
            if row_idx == rank or not rows[row_idx][col] % prime:
                continue
            factor = rows[row_idx][col] % prime
            rows[row_idx] = [
                (rows[row_idx][idx] - factor * rows[rank][idx]) % prime
                for idx in range(ncols)
            ]
        rank += 1
        if rank == len(rows) or rank == ncols:
            break
    return rank


def proxy_basis_rank(classes: list[dict[str, Any]], profile: dict[str, Any] | None) -> dict[str, Any]:
    if profile is None:
        return {
            "proxy_field": "GF(12289)",
            "proxy_matrix_shape": None,
            "proxy_rank": None,
            "proxy_nullity": None,
        }
    classes_by_index = {int(row["class_index"]): row for row in classes}
    generator = primitive_root_mod_prime(PROXY_PRIME)
    subgroup_generator = pow(generator, (PROXY_PRIME - 1) // N, PROXY_PRIME)
    H = [pow(subgroup_generator, idx, PROXY_PRIME) for idx in range(N)]
    powers = [[1] * N]
    for _degree in range(1, K):
        previous = powers[-1]
        powers.append([(previous[pos] * H[pos]) % PROXY_PRIME for pos in range(N)])
    z_eval = {}
    for class_index in profile["basis_class_indices"]:
        positions = classes_by_index[int(class_index)]["positions"]
        evals = []
        for value in H:
            acc = 1
            for pos in positions:
                acc = (acc * (value - H[int(pos)])) % PROXY_PRIME
            evals.append(acc)
        z_eval[int(class_index)] = evals
    blocks = {}
    cursor = 0
    for class_index in profile["basis_class_indices"]:
        q_degree = K - int(classes_by_index[int(class_index)]["support_size"])
        blocks[int(class_index)] = (cursor, q_degree)
        cursor += q_degree
    matrix = []
    for constraint in profile["nonbasis_constraint_detail"]:
        positions = classes_by_index[int(constraint["class_index"])]["positions"]
        coords = [int(value) % PROXY_PRIME for value in constraint["basis_coordinates"]]
        for pos in positions:
            pos = int(pos)
            row = [0] * cursor
            for slot, class_index in enumerate(profile["basis_class_indices"]):
                scalar = coords[slot]
                if not scalar:
                    continue
                class_index = int(class_index)
                z_value = z_eval[class_index][pos]
                if not z_value:
                    continue
                start, q_degree = blocks[class_index]
                for degree in range(q_degree):
                    row[start + degree] = (
                        row[start + degree] + scalar * z_value * powers[degree][pos]
                    ) % PROXY_PRIME
            matrix.append(row)
    rank = rank_mod_prime_matrix(matrix, ncols=cursor, prime=PROXY_PRIME)
    return {
        "proxy_field": "GF(12289)",
        "proxy_matrix_shape": [len(matrix), cursor],
        "proxy_rank": rank,
        "proxy_nullity": cursor - rank,
    }


def build_record(mark_exact_timeout: bool = False) -> dict[str, Any]:
    repair = load_json(REPAIR_DATA)
    search = load_json(SEARCH_DATA)
    survivor = find_survivor(repair, search)
    classes = functional_classes(survivor)
    functionals = [row["functional"] for row in classes]
    functional_span_rank = rank_mod_p(functionals)
    annihilator_basis = nullspace_basis(functionals)
    profiles = basis_profiles(classes, functional_span_rank=functional_span_rank)
    best = profiles[0] if profiles else None
    proxy_rank = proxy_basis_rank(classes, best)
    histogram = Counter(str(row["support_size"]) for row in classes)
    forced = [row for row in classes if row["forced_identity"]]
    proof_status = "CANDIDATE / RANDOM_MATROID_FUNC_LIFT_METADATA / PARTIAL / EXPERIMENTAL"
    failure = None
    if forced:
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANDOM_MATROID_FUNC_LIFT_FORCED_IDENTITY / PARTIAL / EXPERIMENTAL"
        failure = "RANDOM_MATROID_FUNC_LIFT_FORCED_IDENTITY"
    elif not profiles:
        proof_status = "EXACT_EXTRACTION_NO_A327 / RANDOM_MATROID_FUNC_LIFT_NO_BASIS / PARTIAL / EXPERIMENTAL"
        failure = "RANDOM_MATROID_FUNC_LIFT_NO_BASIS"
    elif proxy_rank["proxy_nullity"] == 0:
        proof_status = "CANDIDATE / RANDOM_MATROID_FUNC_LIFT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RANDOM_MATROID_FUNC_LIFT_PROXY_FULL_RANK"
    if mark_exact_timeout:
        proof_status = "CANDIDATE / RANDOM_MATROID_FUNC_LIFT_EXACT_TIMEOUT_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        failure = "RANDOM_MATROID_FUNC_LIFT_EXACT_TIMEOUT"
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "forced_identity_repair": {
            "commit": SOURCE_COMMIT,
            "best_template_id": repair["best_candidate"]["template_id"],
            "best_assignment_strategy": repair["best_candidate"]["assignment_strategy"],
            "saturation_pass_candidates": repair["forced_identity_repair"]["saturation_pass_candidates"],
            "sage_status": repair["sage_exact_check"]["status"],
            "forced_rank": repair["sage_exact_check"]["forced_rank"],
            "reduced_template_dimension": repair["sage_exact_check"]["reduced_template_dimension"],
            "forced_equal_pairs": repair["sage_exact_check"]["forced_equal_pairs"],
        },
        "survivor": {
            "template_id": survivor["template_id"],
            "template_family": survivor["template_family"],
            "template_dimension": survivor["template_dimension"],
            "assignment_strategy": survivor["assignment_strategy"],
            "template_vectors": survivor["template_vectors"],
            "support_vector": survivor["support_vector"],
            "pair_count_matrix": survivor["pair_count_matrix"],
            "pair7_counts": survivor["pair7_counts"],
            "max_pair_count": survivor["max_pair_count"],
            "selected_class_size_counts": survivor["selected_class_size_counts"],
            "effective_cost": survivor["total_effective_cost"],
            "variable_count": survivor["variable_count"],
            "proxy_field": "GF(12289)",
            "proxy_rank": survivor["proxy_rank"],
            "proxy_nullity": survivor["proxy_nullity"],
            "coordinate_classes_hash": survivor["coordinate_classes_hash"],
        },
        "coordinate_classes": survivor["coordinate_classes"],
        "functional_classes_detail": classes,
        "functional_lift": {
            "functional_classes": len(classes),
            "functional_span_rank": functional_span_rank,
            "annihilator_dimension": len(annihilator_basis),
            "annihilator_basis": annihilator_basis,
            "support_size_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
            "forced_functional_identities": len(forced),
            "basis_profiles_tested": len(profiles),
            "best_basis_id": None if best is None else best["basis_id"],
            "best_basis_support_sizes": None if best is None else best["basis_support_sizes"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_matrix_shape": None if best is None else best["matrix_shape"],
            "best_rank": None,
            "best_nullity": None,
            "proxy_field": proxy_rank["proxy_field"],
            "proxy_matrix_shape": proxy_rank["proxy_matrix_shape"],
            "proxy_rank": proxy_rank["proxy_rank"],
            "proxy_nullity": proxy_rank["proxy_nullity"],
            "exact_rank_attempted": bool(mark_exact_timeout),
            "exact_rank_timeout": bool(mark_exact_timeout),
            "best_failure_mode": failure,
        },
        "basis_profiles": profiles,
        "pair_projection_test": {
            "pairs_tested": 21,
            "forced_equal_pairs": [],
            "min_projection_rank": None,
            "projection_rank_by_pair": None,
        },
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
        ],
        "ledger_hashes": {
            "functional_classes_hash": hash_payload(classes),
            "basis_profiles_hash": hash_payload(profiles),
            "coordinate_classes_hash": hash_payload(survivor["coordinate_classes"]),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--mark-exact-timeout", action="store_true")
    args = parser.parse_args()
    record = build_record(mark_exact_timeout=args.mark_exact_timeout)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        lift = record["functional_lift"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "template_id": record["survivor"]["template_id"],
                    "assignment_strategy": record["survivor"]["assignment_strategy"],
                    "functional_classes": lift["functional_classes"],
                    "forced_functional_identities": lift["forced_functional_identities"],
                    "basis_profiles_tested": lift["basis_profiles_tested"],
                    "best_basis_id": lift["best_basis_id"],
                    "best_matrix_shape": lift["best_matrix_shape"],
                    "best_q_variable_count": lift["best_q_variable_count"],
                    "proxy_rank": lift["proxy_rank"],
                    "proxy_nullity": lift["proxy_nullity"],
                    "best_failure_mode": lift["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_RANDOM_MATROID_FUNCTIONAL_LIFT_READY")


if __name__ == "__main__":
    main()
