#!/usr/bin/env python3
"""Filter low-rank template candidates by forced-identity saturation."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "ff3c0da"
SOURCE_DATA = Path("experimental/data/m1_a327_lowrank_template_selected_class_search.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_lowrank_template_forced_identity_repair.json")

P = 17
K = 256
TARGET_AGREEMENT = 327
LIST_SIZE = 7


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def rref(rows: list[list[int]], ncols: int, prime: int = P) -> tuple[list[list[int]], list[int]]:
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


def nullspace_basis(rows: list[list[int]], ncols: int, prime: int = P) -> list[list[int]]:
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


def rank_mod_p(rows: list[list[int]], ncols: int, prime: int = P) -> int:
    return len(rref(rows, ncols=ncols, prime=prime)[0])


def normalize_projective(row: list[int], prime: int = P) -> tuple[int, ...]:
    reduced = [value % prime for value in row]
    for value in reduced:
        if value:
            inv = pow(value, -1, prime)
            return tuple((entry * inv) % prime for entry in reduced)
    raise ValueError("zero row has no projective normalization")


def reduce_mod_span(row: list[int], basis: list[list[int]], pivots: list[int], prime: int = P) -> tuple[int, ...]:
    reduced = [value % prime for value in row]
    for basis_row, pivot in zip(basis, pivots, strict=True):
        factor = reduced[pivot] % prime
        if not factor:
            continue
        reduced = [(reduced[idx] - factor * basis_row[idx]) % prime for idx in range(len(reduced))]
    return tuple(reduced)


def row_basis_mod_p(vectors: list[list[int]], members: list[int], prime: int = P) -> list[list[int]]:
    if len(members) <= 1:
        return []
    anchor = [value % prime for value in vectors[int(members[0]) - 1]]
    rows = []
    for witness in members[1:]:
        rows.append([(vectors[int(witness) - 1][idx] - anchor[idx]) % prime for idx in range(len(anchor))])
    basis, _pivots = rref(rows, ncols=len(anchor), prime=prime)
    return basis


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
                "positions": positions,
                "positions_hash": hash_payload(positions),
            }
        )
    return classes


def saturate(candidate: dict[str, Any]) -> dict[str, Any]:
    classes = functional_classes(candidate)
    m = int(candidate["template_dimension"])
    forced_rows = [row["functional"] for row in classes if row["forced_identity"]]
    changed = True
    iterations = []
    while changed:
        changed = False
        basis, pivots = rref(forced_rows, ncols=m)
        projected: dict[tuple[int, ...], set[int]] = defaultdict(set)
        zero_projected = 0
        for row in classes:
            remainder = reduce_mod_span(row["functional"], basis, pivots)
            if not any(remainder):
                zero_projected += 1
                continue
            key = normalize_projective(list(remainder))
            projected[key].update(int(pos) for pos in row["positions"])
        new_forced = []
        for key, positions in projected.items():
            if len(positions) > K - 1:
                new_forced.append(list(key))
        current_rank = len(basis)
        for row in new_forced:
            trial_rank = rank_mod_p(forced_rows + [row], ncols=m)
            if trial_rank > current_rank:
                forced_rows.append(row)
                current_rank = trial_rank
                changed = True
        iterations.append(
            {
                "forced_rank": len(rref(forced_rows, ncols=m)[0]),
                "projected_classes": len(projected),
                "zero_projected_functionals": zero_projected,
                "new_forced_candidates": len(new_forced),
            }
        )
    basis, pivots = rref(forced_rows, ncols=m)
    projected: dict[tuple[int, ...], set[int]] = defaultdict(set)
    zero_projected = 0
    for row in classes:
        remainder = reduce_mod_span(row["functional"], basis, pivots)
        if not any(remainder):
            zero_projected += 1
            continue
        key = normalize_projective(list(remainder))
        projected[key].update(int(pos) for pos in row["positions"])
    projected_classes = []
    for idx, (functional, positions_set) in enumerate(
        sorted(projected.items(), key=lambda item: (-len(item[1]), item[0]))
    ):
        positions = sorted(positions_set)
        projected_classes.append(
            {
                "class_index": idx,
                "functional": list(functional),
                "support_size": len(positions),
                "forced_identity": len(positions) > K - 1,
                "positions_hash": hash_payload(positions),
            }
        )
    kernel = nullspace_basis(forced_rows, ncols=m)
    pair_ranks = {}
    forced_pairs = []
    for left in range(1, LIST_SIZE + 1):
        for right in range(left + 1, LIST_SIZE + 1):
            diff = [
                (int(candidate["template_vectors"][left - 1][idx]) - int(candidate["template_vectors"][right - 1][idx])) % P
                for idx in range(m)
            ]
            values = [
                sum(diff[idx] * basis_vec[idx] for idx in range(m)) % P
                for basis_vec in kernel
            ]
            rank = 1 if any(values) else 0
            label = f"P{left}{right}"
            pair_ranks[label] = rank
            if rank == 0:
                forced_pairs.append([left, right])
    histogram = Counter(str(row["support_size"]) for row in classes)
    projected_histogram = Counter(str(row["support_size"]) for row in projected_classes)
    return {
        "functional_classes": len(classes),
        "support_size_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "initial_forced_identities": sum(1 for row in classes if row["forced_identity"]),
        "forced_rank": len(basis),
        "forced_functionals": basis,
        "reduced_template_dimension": m - len(basis),
        "remaining_functional_classes": len(projected_classes),
        "projected_support_size_histogram": dict(sorted(projected_histogram.items(), key=lambda item: int(item[0]))),
        "zero_projected_functionals": zero_projected,
        "saturation_iterations": iterations,
        "forced_equal_pairs": forced_pairs,
        "min_pair_projection_rank": min(pair_ranks.values()) if pair_ranks else None,
        "pair_projection_rank_by_pair": pair_ranks,
    }


def classify(candidate: dict[str, Any], saturation: dict[str, Any]) -> str:
    if not candidate.get("proxy_nullity"):
        return "LOWRANK_REPAIR_PROXY_NOT_POSITIVE"
    if saturation["reduced_template_dimension"] <= 0:
        return "LOWRANK_REPAIR_FORCED_SPAN_COLLAPSES"
    if saturation["reduced_template_dimension"] < 2:
        return "LOWRANK_REPAIR_REDUCED_DIM_TOO_SMALL"
    if saturation["forced_equal_pairs"]:
        return "LOWRANK_REPAIR_FORCED_PAIR_EQUALITY"
    return "LOWRANK_REPAIR_SATURATION_PASS"


def load_source() -> dict[str, Any]:
    with SOURCE_DATA.open() as handle:
        return json.load(handle)


def build_record() -> dict[str, Any]:
    source = load_source()
    candidates = []
    for candidate in source["lowrank_template_search"]["candidates"]:
        sat = saturate(candidate)
        failure = classify(candidate, sat)
        row = {
            "template_id": candidate["template_id"],
            "template_family": candidate["template_family"],
            "template_dimension": candidate["template_dimension"],
            "template_vectors": candidate["template_vectors"],
            "assignment_strategy": candidate["assignment_strategy"],
            "effective_cost": candidate["total_effective_cost"],
            "variable_count": candidate["variable_count"],
            "proxy_rank": candidate["proxy_rank"],
            "proxy_nullity": candidate["proxy_nullity"],
            "support_vector": candidate["support_vector"],
            "pair7_counts": candidate["pair7_counts"],
            "max_pair_count": candidate["max_pair_count"],
            "coordinate_classes_hash": candidate["coordinate_classes_hash"],
            "saturation": sat,
            "best_failure_mode": failure,
        }
        candidates.append(row)
    passing = [row for row in candidates if row["best_failure_mode"] == "LOWRANK_REPAIR_SATURATION_PASS"]
    best = None
    if passing:
        best = max(
            passing,
            key=lambda row: (
                row["saturation"]["reduced_template_dimension"],
                row["proxy_nullity"],
                -len(row["saturation"]["forced_equal_pairs"]),
                -row["effective_cost"],
            ),
        )
    elif candidates:
        best = max(
            candidates,
            key=lambda row: (
                row["proxy_nullity"] or 0,
                row["saturation"]["reduced_template_dimension"],
                -len(row["saturation"]["forced_equal_pairs"]),
            ),
        )
    failure = "LOWRANK_REPAIR_SATURATION_PASS" if passing else "LOWRANK_REPAIR_NO_SURVIVOR"
    proof_status = (
        "CANDIDATE / LOWRANK_REPAIR_SATURATION_PASS / PARTIAL / EXPERIMENTAL"
        if passing
        else "EXACT_EXTRACTION_NO_A327 / LOWRANK_REPAIR_NO_SURVIVOR / PARTIAL / EXPERIMENTAL"
    )
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_lowrank_search": {
            "systems_tested": source["lowrank_template_search"]["systems_tested"],
            "proxy_positive_candidates": source["lowrank_template_search"]["proxy_positive_candidates"],
            "best_proxy_rank": source["lowrank_template_search"]["best_proxy_rank"],
            "best_proxy_nullity": source["lowrank_template_search"]["best_proxy_nullity"],
            "best_failure_mode": source["lowrank_template_search"]["best_failure_mode"],
        },
        "forced_identity_repair": {
            "candidates_tested": len(candidates),
            "proxy_positive_candidates": sum(1 for row in candidates if row["proxy_nullity"] and row["proxy_nullity"] > 0),
            "saturation_pass_candidates": len(passing),
            "best_template_id": None if best is None else best["template_id"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_reduced_template_dimension": None if best is None else best["saturation"]["reduced_template_dimension"],
            "best_forced_equal_pair_count": None if best is None else len(best["saturation"]["forced_equal_pairs"]),
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in candidates)),
            "candidates": candidates,
        },
        "best_candidate": best,
        "sage_exact_check": {
            "run": False,
            "field": "GF(17^32)",
            "best_template_id": None if best is None else best["template_id"],
            "forced_rank": None,
            "reduced_template_dimension": None,
            "forced_equal_pairs": None,
            "status": "NOT_RUN",
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
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["forced_identity_repair"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "candidates_tested": search["candidates_tested"],
                    "proxy_positive_candidates": search["proxy_positive_candidates"],
                    "saturation_pass_candidates": search["saturation_pass_candidates"],
                    "best_template_id": search["best_template_id"],
                    "best_reduced_template_dimension": search["best_reduced_template_dimension"],
                    "best_forced_equal_pair_count": search["best_forced_equal_pair_count"],
                    "failure_counts": search["failure_counts"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_LOWRANK_TEMPLATE_FORCED_IDENTITY_REPAIR_READY")


if __name__ == "__main__":
    main()
