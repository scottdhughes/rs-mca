#!/usr/bin/env python3
"""Coefficient/nullspace-first proxy search for the M1 a=327 target."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from numbers import Integral
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import scan_m1_a327_singular_all_pair_boundary_embedding_search as allpair


OUTPUT_DATA = Path("experimental/data/m1_a327_coefficient_nullspace_target_search.json")

N = 512
K = 256
LIST_SIZE = 7
DIFF_COUNT = LIST_SIZE - 1
TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
TOP_LABELS_PER_WITNESS = 3
RETAINED_CANDIDATES = 32
RANDOM_ROOT_TUPLES = 24


def jsonable(payload: Any) -> Any:
    if payload is None or isinstance(payload, (str, bool, float)):
        return payload
    if isinstance(payload, Integral):
        return int(payload)
    if isinstance(payload, list):
        return [jsonable(item) for item in payload]
    if isinstance(payload, tuple):
        return [jsonable(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): jsonable(value) for key, value in payload.items()}
    return payload


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(jsonable(payload), sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def primitive_root_mod_prime(p: int) -> int:
    n = p - 1
    factors = []
    temp = n
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    for candidate in range(2, p):
        if all(pow(candidate, n // factor, p) != 1 for factor in factors):
            return candidate
    raise RuntimeError(f"no primitive root for {p}")


def proxy_subgroup() -> np.ndarray:
    generator = primitive_root_mod_prime(PROXY_PRIME)
    subgroup_generator = pow(generator, (PROXY_PRIME - 1) // N, PROXY_PRIME)
    return np.array([pow(subgroup_generator, idx, PROXY_PRIME) for idx in range(N)], dtype=np.int64)


def quotient_fibers() -> list[list[int]]:
    return [[residue + 16 * offset for offset in range(32)] for residue in range(16)]


def root_tuple_hash(root_sets: list[list[int]]) -> str:
    return hash_payload([sorted(root_set) for root_set in root_sets])


def locator_values_modp(H: np.ndarray, roots: list[int]) -> np.ndarray:
    values = np.ones(N, dtype=np.int64)
    for position in roots:
        values = (values * ((H - int(H[position])) % PROXY_PRIME)) % PROXY_PRIME
    values[roots] = 0
    return values


def quotient_residual_root_tuples() -> list[dict[str, Any]]:
    fibers = quotient_fibers()
    tuples = []
    for shift in range(6):
        root_sets = []
        for witness in range(DIFF_COUNT):
            full_fibers = [(shift + 2 * witness + offset) % 16 for offset in range(7)]
            residual_fiber = (shift + 2 * witness + 7) % 16
            residual = [pos for idx, pos in enumerate(fibers[residual_fiber]) if idx != (shift + witness) % 32]
            roots = sorted([pos for fiber in full_fibers for pos in fibers[fiber]] + residual)
            root_sets.append(roots)
        tuples.append(
            {
                "root_tuple_id": f"quotient_residual_shift_{shift:02d}",
                "family": "quotient_fiber_plus_residual",
                "root_sets": root_sets,
            }
        )
    return tuples


def interval_root_tuples() -> list[dict[str, Any]]:
    tuples = []
    for shift, step in [(0, 17), (3, 19), (11, 23), (29, 31), (47, 37), (83, 41)]:
        root_sets = []
        for witness in range(DIFF_COUNT):
            start = (shift + witness * step) % N
            root_sets.append(sorted((start + offset) % N for offset in range(255)))
        tuples.append(
            {
                "root_tuple_id": f"interval_shift_{shift:03d}_step_{step:02d}",
                "family": "cyclic_interval",
                "root_sets": root_sets,
            }
        )
    return tuples


def random_root_tuples() -> list[dict[str, Any]]:
    tuples = []
    for idx in range(RANDOM_ROOT_TUPLES):
        seed = 0xA327C0EF + 7919 * idx
        rng = random.Random(seed)
        root_sets = [sorted(rng.sample(range(N), 255)) for _ in range(DIFF_COUNT)]
        tuples.append(
            {
                "root_tuple_id": f"random_255_tuple_{idx:03d}",
                "family": "seeded_random_255",
                "seed": seed,
                "root_sets": root_sets,
            }
        )
    return tuples


def all_pair_boundary_root_tuples() -> list[dict[str, Any]]:
    selected_embeddings = {
        "block",
        "bit_reversal",
        "fiber_round_robin",
        "random_shuffle_0000",
        "random_shuffle_0001",
        "random_shuffle_0017",
        "random_shuffle_0064",
        "random_shuffle_0255",
        "random_shuffle_0511",
    }
    tuples = []
    for candidate in allpair.candidate_embeddings():
        if candidate["embedding_id"] not in selected_embeddings:
            continue
        root_sets = []
        masks = candidate["membership_masks"]
        for witness in range(1, LIST_SIZE):
            roots = [
                position
                for position, mask in enumerate(masks)
                if (mask & 1) and (mask & (1 << witness))
            ]
            root_sets.append(sorted(roots))
        tuples.append(
            {
                "root_tuple_id": f"all_pair_boundary_{candidate['embedding_id']}",
                "family": "all_pair_boundary_embedding_roots",
                "seed": candidate["seed"],
                "root_sets": root_sets,
            }
        )
    return tuples


def root_tuples() -> list[dict[str, Any]]:
    tuples = (
        quotient_residual_root_tuples()
        + interval_root_tuples()
        + random_root_tuples()
        + all_pair_boundary_root_tuples()
    )
    seen = set()
    unique = []
    for item in tuples:
        digest = root_tuple_hash(item["root_sets"])
        if digest in seen:
            continue
        seen.add(digest)
        item = dict(item)
        item["root_tuple_hash"] = digest
        unique.append(item)
    return unique


def top_base_constants(locator_values: list[np.ndarray], limit: int = TOP_LABELS_PER_WITNESS) -> list[list[int]]:
    constants = []
    base = locator_values[0]
    for witness in range(1, DIFF_COUNT):
        labels = Counter()
        other = locator_values[witness]
        for pos in range(N):
            if int(base[pos]) == 0 or int(other[pos]) == 0:
                continue
            label = (int(base[pos]) * pow(int(other[pos]), PROXY_PRIME - 2, PROXY_PRIME)) % PROXY_PRIME
            labels[label] += 1
        top = [label for label, _count in labels.most_common(limit)]
        while len(top) < limit:
            top.append(1)
        constants.append(top)
    return constants


def value_class_capacity(values: list[list[int]]) -> dict[str, Any]:
    largest_histogram: dict[str, int] = {}
    class_mask_histogram: dict[str, int] = {}
    total_capacity = 0
    for pos in range(N):
        buckets: dict[int, int] = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        masks = list(buckets.values())
        largest = max(mask.bit_count() for mask in masks)
        total_capacity += largest
        largest_histogram[str(largest)] = largest_histogram.get(str(largest), 0) + 1
        for mask in masks:
            class_mask_histogram[str(mask)] = class_mask_histogram.get(str(mask), 0) + 1
    return {
        "capacity_total": total_capacity,
        "capacity_upper_bound": total_capacity // LIST_SIZE,
        "largest_class_histogram": dict(sorted(largest_histogram.items(), key=lambda item: int(item[0]))),
        "class_mask_histogram_hash": hash_payload(class_mask_histogram),
    }


def exact_assignment_max_min(values: list[list[int]]) -> dict[str, Any]:
    classes_by_pos: list[list[int]] = []
    for pos in range(N):
        buckets: dict[int, int] = {}
        for witness in range(LIST_SIZE):
            value = values[witness][pos]
            buckets[value] = buckets.get(value, 0) | (1 << witness)
        classes_by_pos.append(sorted(set(buckets.values())))

    variable_offsets = []
    total_vars = 0
    for classes in classes_by_pos:
        variable_offsets.append(total_vars)
        total_vars += len(classes)

    # Binary-search feasibility for a common agreement floor.
    def feasible(floor: int) -> tuple[bool, list[int] | None]:
        objective = np.zeros(total_vars)
        integrality = np.ones(total_vars)
        bounds = Bounds(np.zeros(total_vars), np.ones(total_vars))
        rows = []
        lower = []
        upper = []
        for pos, classes in enumerate(classes_by_pos):
            row = np.zeros(total_vars)
            start = variable_offsets[pos]
            row[start : start + len(classes)] = 1
            rows.append(row)
            lower.append(1)
            upper.append(1)
        for witness in range(LIST_SIZE):
            row = np.zeros(total_vars)
            for pos, classes in enumerate(classes_by_pos):
                start = variable_offsets[pos]
                for idx, mask in enumerate(classes):
                    if mask & (1 << witness):
                        row[start + idx] = 1
            rows.append(row)
            lower.append(floor)
            upper.append(np.inf)
        constraints = LinearConstraint(np.vstack(rows), np.array(lower), np.array(upper))
        result = milp(objective, integrality=integrality, bounds=bounds, constraints=constraints, options={"time_limit": 15})
        if not result.success:
            return False, None
        chosen = []
        rounded = np.rint(result.x).astype(int)
        for pos, classes in enumerate(classes_by_pos):
            start = variable_offsets[pos]
            choice = next((idx for idx, value in enumerate(rounded[start : start + len(classes)]) if value), 0)
            chosen.append(classes[choice])
        return True, chosen

    lo, hi = 0, max(value_class_capacity(values)["capacity_upper_bound"], TARGET_AGREEMENT)
    best_masks = None
    while lo < hi:
        mid = (lo + hi + 1) // 2
        ok, masks = feasible(mid)
        if ok:
            lo = mid
            best_masks = masks
        else:
            hi = mid - 1
    agreement = [0] * LIST_SIZE
    if best_masks is not None:
        for mask in best_masks:
            for witness in range(LIST_SIZE):
                if mask & (1 << witness):
                    agreement[witness] += 1
    return {
        "exact_max_min": lo,
        "agreement_vector": agreement,
        "chosen_masks_hash": None if best_masks is None else hash_payload(best_masks),
    }


def evaluate_constants(root_tuple: dict[str, Any], locator_values: list[np.ndarray], constants: list[int]) -> dict[str, Any]:
    values = [[0] * N]
    for constant, locator in zip(constants, locator_values):
        values.append([int((constant * int(locator[pos])) % PROXY_PRIME) for pos in range(N)])
    capacity = value_class_capacity(values)
    exact = None
    if capacity["capacity_upper_bound"] >= TARGET_AGREEMENT:
        exact = exact_assignment_max_min(values)
    pair_equalities = 0
    for left, right in itertools.combinations(range(1, LIST_SIZE), 2):
        pair_equalities += sum(1 for pos in range(N) if values[left][pos] == values[right][pos])
    anchor_equalities = sum(sum(1 for pos in range(N) if values[witness][pos] == 0) for witness in range(1, LIST_SIZE))
    return {
        "root_tuple_id": root_tuple["root_tuple_id"],
        "family": root_tuple["family"],
        "root_tuple_hash": root_tuple["root_tuple_hash"],
        "constants": constants,
        "constants_hash": hash_payload(constants),
        "anchor_equalities": anchor_equalities,
        "nonanchor_pair_equalities": pair_equalities,
        **capacity,
        "assignment": exact,
        "status": (
            "PROXY_A327_ASSIGNMENT"
            if exact is not None and exact["exact_max_min"] >= TARGET_AGREEMENT
            else "CAPACITY_BELOW_A327"
        ),
    }


def evaluate_root_tuple(root_tuple: dict[str, Any], H: np.ndarray) -> list[dict[str, Any]]:
    locators = [locator_values_modp(H, roots) for roots in root_tuple["root_sets"]]
    constant_options = top_base_constants(locators)
    candidate_constants = [[1] * DIFF_COUNT]
    for combo in itertools.product(*constant_options):
        candidate_constants.append([1] + list(combo))
    seen = set()
    results = []
    for constants in candidate_constants:
        digest = hash_payload(constants)
        if digest in seen:
            continue
        seen.add(digest)
        results.append(evaluate_constants(root_tuple, locators, constants))
    return results


def build_record() -> dict[str, Any]:
    H = proxy_subgroup()
    tuples = root_tuples()
    all_results = []
    family_counts: dict[str, int] = {}
    for root_tuple in tuples:
        family_counts[root_tuple["family"]] = family_counts.get(root_tuple["family"], 0) + 1
        all_results.extend(evaluate_root_tuple(root_tuple, H))

    retained = sorted(
        all_results,
        key=lambda row: (
            row["capacity_upper_bound"],
            row["capacity_total"],
            row["nonanchor_pair_equalities"],
            row["anchor_equalities"],
            row["root_tuple_id"],
        ),
        reverse=True,
    )[:RETAINED_CANDIDATES]
    proxy_candidates = [row for row in all_results if row["status"] == "PROXY_A327_ASSIGNMENT"]
    best = retained[0]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "coefficient_nullspace_target_search",
        "model": {
            "anchor": "P_1 = 0",
            "differences": "D_i(X) = c_i L_i(X), deg L_i = 255",
            "proxy_field": "GF(12289)",
            "constants_per_root_tuple": "1 + product(top base locator-ratio labels)",
            "top_labels_per_witness": TOP_LABELS_PER_WITNESS,
        },
        "root_tuple_count": len(tuples),
        "root_tuple_family_counts": dict(sorted(family_counts.items())),
        "candidate_constant_count": len(all_results),
        "result_hash": hash_payload(all_results),
        "proxy_candidate_count": len(proxy_candidates),
        "best": best,
        "retained_count": len(retained),
        "retained_results": retained,
        "proof_status": "CANDIDATE" if proxy_candidates else "TESTED_ROOT_SETS_NO_PROXY_A327",
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list certificate over GF(17^32)",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "improvement over PR #133",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    record = build_record()
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(jsonable(record), indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(jsonable(record), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
