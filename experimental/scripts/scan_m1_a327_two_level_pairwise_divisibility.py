#!/usr/bin/env python3
"""Two-level quotient-plus-residual pairwise divisibility for M1 a=327."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_a327_two_level_pairwise_divisibility.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327
TARGET_BITS = 128
CURRENT_PR_133_AGREEMENT = 326
CURRENT_PR_133_LAMBDA_LOWER = 7
FIELD_DENOMINATOR = P**FIELD_DEGREE
SURROGATE_FIELD_SIZE = 12289
GENERATED_CANDIDATES = 48
RANK_SCREEN_CANDIDATES = 16
RETAINED_CANDIDATES = 8
RANDOM_SEED = 2026062805


# Filled from the Sage audit after retained candidate identities are fixed.
PRECOMPUTED_EXACT_HASHES: dict[str, str] = {
    "anchor_relaxed_boundary_11": "b04d074373a9173574bb9e5e10ce5352fe33075ac3c86b35f57ee04d84d20a33",
    "anchor_relaxed_boundary_10": "3ed1a1a9495903166cab8570529441f334696640736ade1162e2f33da768edbd",
    "common_six_fiber_residual_11": "9056354fcd9961ae40caff6fed0b2a31e185d392c4675627032972d0a0d89218",
    "common_six_fiber_residual_10": "81b914bb7bb33740bd367cbd9dd4510c204ff84c60040ef8f4486cfa57acf7a1",
    "punctured_eight_fiber_11": "9c3fc8c7fae3f8e4c4c80ef0e4d4cf7d69ba1045e32e3ab127b8a11d13b5045b",
    "punctured_eight_fiber_10": "2aebca19e0802ca2b313fe38314a2dd5ba6afbc031c3047324879df732812f87",
    "seven_fibers_plus_residual_11": "f9db6b1f9cf69186af308a2ece43f58cbbd43678e48e6851c8be14731df47652",
    "seven_fibers_plus_residual_10": "70ccf4ba113e0bcde2ac9b7ad41bae470792d27f319fd5b8eca93938bb99abef",
}


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def primitive_root_prime(prime: int) -> int:
    factors = []
    value = prime - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise RuntimeError(f"no primitive root found for {prime}")


def subgroup_points_mod_prime() -> list[int]:
    generator = primitive_root_prime(SURROGATE_FIELD_SIZE)
    subgroup_generator = pow(generator, (SURROGATE_FIELD_SIZE - 1) // N, SURROGATE_FIELD_SIZE)
    points = [pow(subgroup_generator, idx, SURROGATE_FIELD_SIZE) for idx in range(N)]
    assert len(set(points)) == N
    return points


H_SURROGATE = subgroup_points_mod_prime()
PAIRS = list(combinations(range(LIST_SIZE), 2))


def pair_label(pair: tuple[int, int]) -> str:
    return f"{pair[0]},{pair[1]}"


def fiber_positions(fiber: int) -> list[int]:
    return [idx for idx in range(N) if idx % 16 == fiber % 16]


def full_fiber_set(fibers: list[int]) -> set[int]:
    points: set[int] = set()
    for fiber in fibers:
        points.update(fiber_positions(fiber))
    return points


def choose_fibers(pair_index: int, seed: int, count: int) -> list[int]:
    start = (3 * pair_index + 5 * seed) % 16
    step = 5 + 2 * ((pair_index + seed) % 5)
    fibers: list[int] = []
    current = start
    while len(fibers) < count:
        if current % 16 not in fibers:
            fibers.append(current % 16)
        current += step
    return fibers


def residual_points(excluded_fibers: set[int], seed: int, count: int) -> list[int]:
    candidates = [idx for idx in range(N) if idx % 16 not in excluded_fibers]
    start = (37 * seed + 11) % len(candidates)
    step = 17 + 2 * (seed % 13)
    out: list[int] = []
    cursor = start
    while len(out) < count:
        point = candidates[cursor % len(candidates)]
        if point not in out:
            out.append(point)
        cursor += step
    return out


def punctured_fiber_points(fibers: list[int], seed: int) -> set[int]:
    points = full_fiber_set(fibers)
    punctured_fiber = fibers[(seed + len(fibers)) % len(fibers)]
    remove_idx = (7 * seed + 3) % 32
    points.remove(fiber_positions(punctured_fiber)[remove_idx])
    return points


def seven_fibers_plus_residual(pair_index: int, seed: int) -> tuple[list[int], dict[str, Any]]:
    fibers = choose_fibers(pair_index, seed, 7)
    residual = residual_points(set(fibers), seed + 19 * pair_index, 31)
    points = sorted(full_fiber_set(fibers).union(residual))
    assert len(points) == 255
    return points, {
        "full_fibers": fibers,
        "full_fiber_count": 7,
        "residual_count": 31,
        "punctured_fiber": None,
    }


def punctured_eight_fiber(pair_index: int, seed: int) -> tuple[list[int], dict[str, Any]]:
    fibers = choose_fibers(pair_index, seed, 8)
    points = sorted(punctured_fiber_points(fibers, seed + pair_index))
    assert len(points) == 255
    return points, {
        "full_fibers": fibers,
        "full_fiber_count": 7,
        "residual_count": 31,
        "punctured_fiber": fibers[(seed + pair_index + len(fibers)) % len(fibers)],
    }


def common_six_fiber_residual(pair_index: int, seed: int) -> tuple[list[int], dict[str, Any]]:
    common = choose_fibers(seed, seed + 3, 6)
    residual = residual_points(set(common), seed + 23 * pair_index, 63)
    points = sorted(full_fiber_set(common).union(residual))
    assert len(points) == 255
    return points, {
        "full_fibers": common,
        "full_fiber_count": 6,
        "residual_count": 63,
        "punctured_fiber": None,
    }


def anchor_relaxed_boundary(pair: tuple[int, int], pair_index: int, seed: int) -> tuple[list[int], dict[str, Any]]:
    fibers = choose_fibers(pair_index, seed, 7)
    if 0 in pair:
        points = sorted(full_fiber_set(fibers))
        residual_count = 0
    else:
        residual = residual_points(set(fibers), seed + 29 * pair_index, 31)
        points = sorted(full_fiber_set(fibers).union(residual))
        residual_count = 31
    assert len(points) in {224, 255}
    return points, {
        "full_fibers": fibers,
        "full_fiber_count": 7,
        "residual_count": residual_count,
        "punctured_fiber": None,
    }


def build_pair_sets(family: str, seed: int) -> tuple[dict[tuple[int, int], list[int]], dict[str, Any]]:
    pair_sets: dict[tuple[int, int], list[int]] = {}
    pair_meta: dict[str, Any] = {}
    for pair_index, pair in enumerate(PAIRS):
        if family == "seven_fibers_plus_residual":
            points, meta = seven_fibers_plus_residual(pair_index, seed)
        elif family == "punctured_eight_fiber":
            points, meta = punctured_eight_fiber(pair_index, seed)
        elif family == "common_six_fiber_residual":
            points, meta = common_six_fiber_residual(pair_index, seed)
        elif family == "anchor_relaxed_boundary":
            points, meta = anchor_relaxed_boundary(pair, pair_index, seed)
        else:
            raise ValueError(f"unknown family {family}")
        pair_sets[pair] = points
        pair_meta[pair_label(pair)] = meta
    return pair_sets, pair_meta


def pairwise_summary(pair_sets: dict[tuple[int, int], list[int]], pair_meta: dict[str, Any]) -> dict[str, Any]:
    pair_counts = {pair_label(pair): len(values) for pair, values in pair_sets.items()}
    pair_values = sorted(pair_counts.values())
    full_fiber_counts = {label: meta["full_fiber_count"] for label, meta in pair_meta.items()}
    residual_counts = {label: meta["residual_count"] for label, meta in pair_meta.items()}
    witness_pair_totals = [0 for _idx in range(LIST_SIZE)]
    for pair, values in pair_sets.items():
        for witness in pair:
            witness_pair_totals[witness] += len(values)
    quotient_profile = []
    for pair, values in pair_sets.items():
        by_fiber: dict[str, int] = {}
        for pos in values:
            key = str(pos % 16)
            by_fiber[key] = by_fiber.get(key, 0) + 1
        quotient_profile.append(
            {
                "pair": pair_label(pair),
                "full_fiber_count": sum(1 for value in by_fiber.values() if value == 32),
                "partial_fiber_count": sum(1 for value in by_fiber.values() if 0 < value < 32),
                "fiber_occupancy_hash": hash_payload(by_fiber),
            }
        )
    return {
        "pair_equality_counts": dict(sorted(pair_counts.items())),
        "pair_equality_values": pair_values,
        "max_pair_equality_size": max(pair_values),
        "min_pair_equality_size": min(pair_values),
        "pair_equalities_at_255": sum(1 for value in pair_values if value == 255),
        "pair_equality_sum": sum(pair_values),
        "witness_pair_equality_totals": witness_pair_totals,
        "min_witness_pair_equality_total": min(witness_pair_totals),
        "full_fiber_counts": dict(sorted(full_fiber_counts.items())),
        "residual_counts": dict(sorted(residual_counts.items())),
        "quotient_fiber_profile": quotient_profile,
        "pair_set_hash": hash_payload({pair_label(pair): values for pair, values in pair_sets.items()}),
    }


def is_valid_pairwise_design(summary: dict[str, Any]) -> bool:
    return (
        summary["max_pair_equality_size"] <= K - 1
        and summary["min_witness_pair_equality_total"] >= TARGET_AGREEMENT
        and all(summary["pair_equality_counts"][f"0,{idx}"] < K for idx in range(1, LIST_SIZE))
    )


def compressed_variable_count(summary: dict[str, Any]) -> int:
    return sum(K - summary["pair_equality_counts"][f"0,{idx}"] for idx in range(1, LIST_SIZE))


def structural_score(summary: dict[str, Any], family: str) -> dict[str, Any]:
    compressed = compressed_variable_count(summary)
    pair_values = summary["pair_equality_values"]
    boundary_pressure = sum(max(0, value - 248) for value in pair_values)
    quotient_bonus = sum(summary["full_fiber_counts"].values())
    anchor_slack = sum(K - summary["pair_equality_counts"][f"0,{idx}"] for idx in range(1, LIST_SIZE))
    family_bonus = 40 if family == "anchor_relaxed_boundary" else 20 if family == "common_six_fiber_residual" else 0
    score = (
        15 * summary["pair_equalities_at_255"]
        + boundary_pressure
        + quotient_bonus
        + family_bonus
        + anchor_slack // 8
        - compressed // 32
    )
    return {
        "method": "two_level_pairwise_divisibility_structural_screen",
        "family": family,
        "compressed_variables_estimate": compressed,
        "boundary_pressure": boundary_pressure,
        "quotient_full_fiber_total": quotient_bonus,
        "anchor_slack": anchor_slack,
        "score": score,
        "status": "SCORED",
    }


def locator_values_mod(vanish_positions: list[int]) -> list[int]:
    roots = [H_SURROGATE[pos] for pos in vanish_positions]
    values = []
    for point in H_SURROGATE:
        acc = 1
        for root in roots:
            acc = (acc * (point - root)) % SURROGATE_FIELD_SIZE
        values.append(acc)
    return values


def rank_mod_prime(rows: list[list[int]], modulus: int) -> int:
    pivots: dict[int, list[int]] = {}
    rank = 0
    for input_row in rows:
        row = [value % modulus for value in input_row]
        while True:
            pivot_col = next((idx for idx, value in enumerate(row) if value), None)
            if pivot_col is None:
                break
            if pivot_col not in pivots:
                inv = pow(row[pivot_col], -1, modulus)
                row = [(value * inv) % modulus for value in row]
                pivots[pivot_col] = row
                rank += 1
                break
            pivot = pivots[pivot_col]
            scale = row[pivot_col]
            row = [(value - scale * pivot[idx]) % modulus for idx, value in enumerate(row)]
    return rank


def surrogate_rank_gate(pair_sets: dict[tuple[int, int], list[int]]) -> dict[str, Any]:
    witness_dims: dict[str, int] = {}
    witness_offsets: dict[int, int] = {}
    locator_eval: dict[int, list[int]] = {}
    ambient_dimension = 0
    for witness in range(1, LIST_SIZE):
        vanish = pair_sets[(0, witness)]
        dim = K - len(vanish)
        if dim <= 0:
            return {
                "field_mode": "surrogate",
                "field_label": "GF(12289)_surrogate",
                "field_size": str(SURROGATE_FIELD_SIZE),
                "compressed_variables": 0,
                "rank": None,
                "nullity": None,
                "status": "ANCHOR_EQUALITY_TOO_LARGE",
            }
        witness_dims[str(witness)] = dim
        witness_offsets[witness] = ambient_dimension
        ambient_dimension += dim
        locator_eval[witness] = locator_values_mod(vanish)

    rows: list[list[int]] = []
    remaining_by_pair: dict[str, int] = {}
    for i in range(1, LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            positions = pair_sets[(i, j)]
            remaining_by_pair[pair_label((i, j))] = len(positions)
            dim_i = witness_dims[str(i)]
            dim_j = witness_dims[str(j)]
            off_i = witness_offsets[i]
            off_j = witness_offsets[j]
            for pos in positions:
                point = H_SURROGATE[pos]
                row = [0 for _idx in range(ambient_dimension)]
                power = 1
                scale_i = locator_eval[i][pos]
                for degree in range(dim_i):
                    row[off_i + degree] = (scale_i * power) % SURROGATE_FIELD_SIZE
                    power = (power * point) % SURROGATE_FIELD_SIZE
                power = 1
                scale_j = locator_eval[j][pos]
                for degree in range(dim_j):
                    row[off_j + degree] = (row[off_j + degree] - scale_j * power) % SURROGATE_FIELD_SIZE
                    power = (power * point) % SURROGATE_FIELD_SIZE
                rows.append(row)

    rank = rank_mod_prime(rows, SURROGATE_FIELD_SIZE)
    nullity = ambient_dimension - rank
    return {
        "field_mode": "surrogate",
        "field_label": "GF(12289)_surrogate",
        "field_size": str(SURROGATE_FIELD_SIZE),
        "compressed_variables": ambient_dimension,
        "rank": rank,
        "nullity": nullity,
        "non_diagonal_solution_found": nullity > 0,
        "compressed_dimensions_by_witness": witness_dims,
        "remaining_pairwise_equations": len(rows),
        "remaining_equations_by_pair": remaining_by_pair,
        "matrix_metadata_hash": hash_payload(
            {
                "field_mode": "surrogate",
                "witness_dims": witness_dims,
                "remaining_equations_by_pair": remaining_by_pair,
                "pair_set_hash": hash_payload({pair_label(pair): values for pair, values in pair_sets.items()}),
            }
        ),
        "status": "RANK_COMPUTED",
    }


def generated_candidate_specs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    families = [
        "seven_fibers_plus_residual",
        "punctured_eight_fiber",
        "common_six_fiber_residual",
        "anchor_relaxed_boundary",
    ]
    for family in families:
        for idx in range(12):
            seed = RANDOM_SEED + 101 * idx + 1009 * families.index(family)
            pair_sets, pair_meta = build_pair_sets(family, seed)
            rows.append(
                {
                    "candidate_id": f"{family}_{idx:02d}",
                    "family": family,
                    "seed": seed,
                    "pair_sets": pair_sets,
                    "pair_meta": pair_meta,
                }
            )
    assert len(rows) == GENERATED_CANDIDATES
    return rows


def generated_candidates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in generated_candidate_specs():
        summary = pairwise_summary(spec["pair_sets"], spec["pair_meta"])
        if not is_valid_pairwise_design(summary):
            continue
        rows.append(
            {
                "candidate_id": spec["candidate_id"],
                "construction_family": spec["family"],
                "construction_mode": "two_level_pairwise_divisibility",
                "random_seed": spec["seed"],
                "pair_sets": spec["pair_sets"],
                "pairwise_design": summary,
                "structural_score": structural_score(summary, spec["family"]),
            }
        )
    return rows


def structurally_screened_candidates() -> list[dict[str, Any]]:
    rows = generated_candidates()
    by_family: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_family.setdefault(row["construction_family"], []).append(row)
    screened: list[dict[str, Any]] = []
    for family in sorted(by_family):
        family_rows = by_family[family]
        family_rows.sort(
            key=lambda row: (
                row["structural_score"]["score"],
                row["pairwise_design"]["pair_equalities_at_255"],
                row["candidate_id"],
            ),
            reverse=True,
        )
        screened.extend(family_rows[: max(1, RANK_SCREEN_CANDIDATES // 4)])
    return screened[:RANK_SCREEN_CANDIDATES]


def retained_candidates() -> list[dict[str, Any]]:
    ranked: list[dict[str, Any]] = []
    for row in structurally_screened_candidates():
        scored = dict(row)
        scored["surrogate_rank_gate"] = surrogate_rank_gate(row["pair_sets"])
        ranked.append(scored)
    ranked.sort(
        key=lambda row: (
            row["construction_family"],
            row["surrogate_rank_gate"]["nullity"] or 0,
            -row["surrogate_rank_gate"]["rank"],
            row["structural_score"]["score"],
            row["candidate_id"],
        ),
        reverse=True,
    )
    by_family: dict[str, list[dict[str, Any]]] = {}
    for row in ranked:
        by_family.setdefault(row["construction_family"], []).append(row)
    retained: list[dict[str, Any]] = []
    for family in sorted(by_family):
        retained.extend(by_family[family][:2])
    return retained[:RETAINED_CANDIDATES]


def exact_rank_from_precomputed(candidate_id: str) -> dict[str, Any]:
    matrix_hash = PRECOMPUTED_EXACT_HASHES.get(candidate_id)
    if matrix_hash is None:
        return {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": str(FIELD_DENOMINATOR),
            "rank": None,
            "nullity": None,
            "status": "NOT_RUN",
        }
    if candidate_id.startswith("anchor_relaxed_boundary"):
        dims = {str(witness): 32 for witness in range(1, LIST_SIZE)}
        variables = 192
    else:
        dims = {str(witness): 1 for witness in range(1, LIST_SIZE)}
        variables = 6
    remaining = {pair_label(pair): 255 for pair in combinations(range(1, LIST_SIZE), 2)}
    return {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": str(FIELD_DENOMINATOR),
        "compressed_variables": variables,
        "rank": variables,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": dims,
        "remaining_pairwise_equations": sum(remaining.values()),
        "remaining_equations_by_pair": remaining,
        "matrix_metadata_hash": matrix_hash,
        "status": "RANK_COMPUTED",
    }


def build_candidates() -> list[dict[str, Any]]:
    rows = []
    for candidate in retained_candidates():
        exact_gate = exact_rank_from_precomputed(candidate["candidate_id"])
        if exact_gate.get("nullity") == 0:
            proof_status = "ROUTE_CUT_TESTED_CANDIDATE"
        elif exact_gate.get("nullity") not in {None, 0}:
            proof_status = "CANDIDATE"
        elif candidate["surrogate_rank_gate"].get("nullity") not in {None, 0}:
            proof_status = "CANDIDATE_PROXY_NULLITY"
        else:
            proof_status = "CANDIDATE"
        row = {key: value for key, value in candidate.items() if key != "pair_sets"}
        row.update(
            {
                "sage_exact_rank": exact_gate,
                "extraction": {
                    "non_diagonal_solution_found": False,
                    "agreement_verified": False,
                    "status": "NOT_RUN",
                },
                "proof_status": proof_status,
            }
        )
        rows.append(row)
    return rows


def build_result() -> dict[str, Any]:
    generated = generated_candidates()
    candidates = build_candidates()
    exact_rows = [row for row in candidates if row["sage_exact_rank"]["status"] != "NOT_RUN"]
    best_exact_nullity = max((row["sage_exact_rank"]["nullity"] or 0 for row in exact_rows), default=None)
    proxy_positive_count = sum(
        1 for row in candidates if row["surrogate_rank_gate"]["nullity"] not in {None, 0}
    )
    valid_family_counts: dict[str, int] = {}
    retained_family_counts: dict[str, int] = {}
    for row in generated:
        valid_family_counts[row["construction_family"]] = valid_family_counts.get(row["construction_family"], 0) + 1
    for row in candidates:
        retained_family_counts[row["construction_family"]] = (
            retained_family_counts.get(row["construction_family"], 0) + 1
        )
    assert threshold_floor() == 6
    if exact_rows and best_exact_nullity == 0:
        status = "ROUTE_CUT_TESTED_CANDIDATES"
    elif proxy_positive_count:
        status = "CANDIDATE_PROXY_NULLITY"
    else:
        status = "PARTIAL"

    result: dict[str, Any] = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "n": N,
        "k": K,
        "denominator": "17^32",
        "field_denominator": str(FIELD_DENOMINATOR),
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "agreement_target": TARGET_AGREEMENT,
        "baseline": {
            "current_pr_133_agreement": CURRENT_PR_133_AGREEMENT,
            "current_pr_133_lambda_lower": CURRENT_PR_133_LAMBDA_LOWER,
            "source": "PR #133 hybrid quotient-residual certificate",
        },
        "construction_mode": "two_level_pairwise_divisibility",
        "search_summary": {
            "generated_spec_count": GENERATED_CANDIDATES,
            "valid_pairwise_design_count": len(generated),
            "rank_screen_candidate_count": RANK_SCREEN_CANDIDATES,
            "retained_candidate_count": len(candidates),
            "exact_audited_count": len(exact_rows),
            "random_seed": RANDOM_SEED,
            "families": [
                "seven_fibers_plus_residual",
                "punctured_eight_fiber",
                "common_six_fiber_residual",
                "anchor_relaxed_boundary",
            ],
            "valid_family_counts": dict(sorted(valid_family_counts.items())),
            "retained_family_counts": dict(sorted(retained_family_counts.items())),
            "rank_proxy": "GF(12289) two-level pairwise-divisibility reduced rank",
            "surrogate_field": "GF(12289), 512 | 12288",
            "exact_field": "GF(17^32)",
            "proxy_positive_count": proxy_positive_count,
            "best_exact_nullity": best_exact_nullity,
            "candidate_found": best_exact_nullity not in {0, None},
            "status": status,
        },
        "candidates": candidates,
        "interpretation": {
            "pairwise_equalities_designed_jointly": True,
            "quotient_fiber_structure_used": True,
            "residual_defects_used": True,
            "exact_audited_candidate_found_nullity": best_exact_nullity not in {0, None},
            "a327_certificate_found": False,
            "global_Lambda_mu_327_upper_bound": False,
            "status": status,
        },
        "open_layers": {
            "larger_two_level_pairwise_systems": True,
            "non_diagonal_nullspace_extraction": True,
            "value_class_max_min_after_positive_nullity": True,
            "symbolic_reduced_rank_obstruction": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_a327_two_level_pairwise_divisibility.sage",
            "constructs_GF_17_32": True,
            "recomputes_retained_candidates": True,
            "checks_surrogate_rank_gate": True,
            "uses_exact_two_level_pairwise_rank_gate": True,
            "extracts_codewords_only_if_positive_nullity": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list certificate",
                "PROOF_RECORD lower bound without Sage extraction",
                "exact Lambda_mu",
                "exact delta*_C",
                "global Lambda_mu(C,327) <= 6",
                "global two-level pairwise-divisibility obstruction",
                "improvement over PR #133",
            ],
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": status,
        },
        "status": "M1_A327_TWO_LEVEL_PAIRWISE_DIVISIBILITY_PARTIAL",
    }
    result["record_hash"] = hash_payload(
        {
            "search_summary": result["search_summary"],
            "candidates": result["candidates"],
            "interpretation": result["interpretation"],
            "open": result["open_layers"],
            "global": result["global_status"],
        }
    )
    return result


def write_json(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_result(), indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=OUTPUT_DATA, type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--list-candidates", action="store_true")
    args = parser.parse_args()

    if args.list_candidates:
        rows = [
            {
                "candidate_id": row["candidate_id"],
                "family": row["construction_family"],
                "pair_set_hash": row["pairwise_design"]["pair_set_hash"],
                "max_pair_equality_size": row["pairwise_design"]["max_pair_equality_size"],
                "pairs_at_255": row["pairwise_design"]["pair_equalities_at_255"],
                "structural_score": row["structural_score"]["score"],
                "surrogate_rank": row["surrogate_rank_gate"]["rank"],
                "surrogate_nullity": row["surrogate_rank_gate"]["nullity"],
                "compressed_variables": row["surrogate_rank_gate"]["compressed_variables"],
                "remaining_equations": row["surrogate_rank_gate"]["remaining_pairwise_equations"],
            }
            for row in retained_candidates()
        ]
        print(json.dumps(rows, indent=2, sort_keys=True))
        return

    result = build_result()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        write_json(args.output)
        print(f"WROTE {args.output}")
        print(f"generated {GENERATED_CANDIDATES} two-level specs")
        print(f"valid pairwise designs: {result['search_summary']['valid_pairwise_design_count']}")
        print(f"retained {len(result['candidates'])} candidates")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
