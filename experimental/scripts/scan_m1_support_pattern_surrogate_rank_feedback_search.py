#!/usr/bin/env python3
"""Emit the M1 support-pattern surrogate-rank feedback search checkpoint."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_support_pattern_surrogate_rank_feedback_search.json")
MULTIPLICITY_SCANNER_PATH = Path(
    "experimental/scripts/scan_m1_support_pattern_multiplicity_mutation_search.py"
)

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
PREFILTER_LIMIT = 12
RETAINED_CANDIDATES = 6


# Filled from the Sage audit after retained candidate identities are fixed.
# The scanner remains dependency-free; Sage is the exact GF(17^32) source.
PRECOMPUTED_EXACT_RANKS: dict[str, dict[str, Any]] = {
    "multiplicity_spread_cyclic_45_balanced_r2_seed_202607755": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 59,
        "rank": 59,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 8, "2": 11, "3": 3, "4": 12, "5": 17, "6": 8},
        "remaining_pairwise_equations": 3651,
        "remaining_equations_by_pair": {
            "1,2": 241,
            "1,3": 241,
            "1,4": 239,
            "1,5": 242,
            "1,6": 233,
            "2,3": 253,
            "2,4": 240,
            "2,5": 246,
            "2,6": 236,
            "3,4": 250,
            "3,5": 247,
            "3,6": 243,
            "4,5": 245,
            "4,6": 240,
            "5,6": 255,
        },
        "matrix_metadata_hash": "ef3e6ba7351f521a7f57a5cfd2e7ca490b6faec6814c9761924e6f15d315ab7f",
        "status": "RANK_COMPUTED",
    },
    "multiplicity_spread_cyclic_3456_balanced_r0_seed_202608129": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 67,
        "rank": 67,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 13, "2": 11, "3": 14, "4": 8, "5": 14, "6": 7},
        "remaining_pairwise_equations": 3625,
        "remaining_equations_by_pair": {
            "1,2": 243,
            "1,3": 239,
            "1,4": 238,
            "1,5": 242,
            "1,6": 234,
            "2,3": 248,
            "2,4": 243,
            "2,5": 241,
            "2,6": 239,
            "3,4": 246,
            "3,5": 246,
            "3,6": 238,
            "4,5": 248,
            "4,6": 232,
            "5,6": 248,
        },
        "matrix_metadata_hash": "a858176036f34179779eb07cf0605179660a69b4f0951d2318478088af96c744",
        "status": "RANK_COMPUTED",
    },
    "multiplicity_spread_cyclic_45_balanced_r0_seed_202607721": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 69,
        "rank": 69,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 4, "2": 17, "3": 16, "4": 18, "5": 12, "6": 2},
        "remaining_pairwise_equations": 3618,
        "remaining_equations_by_pair": {
            "1,2": 248,
            "1,3": 237,
            "1,4": 232,
            "1,5": 247,
            "1,6": 235,
            "2,3": 252,
            "2,4": 233,
            "2,5": 242,
            "2,6": 246,
            "3,4": 250,
            "3,5": 237,
            "3,6": 239,
            "4,5": 238,
            "4,6": 236,
            "5,6": 246,
        },
        "matrix_metadata_hash": "ed8fa6c7bfa985c95a78c7b6711670142cbd4ded1082b184ee9f3b166e90f8e6",
        "status": "RANK_COMPUTED",
    },
    "multiplicity_spread_cyclic_45_balanced_r1_seed_202607738": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 77,
        "rank": 77,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 5, "2": 19, "3": 8, "4": 25, "5": 10, "6": 10},
        "remaining_pairwise_equations": 3631,
        "remaining_equations_by_pair": {
            "1,2": 249,
            "1,3": 244,
            "1,4": 237,
            "1,5": 249,
            "1,6": 241,
            "2,3": 242,
            "2,4": 226,
            "2,5": 247,
            "2,6": 238,
            "3,4": 241,
            "3,5": 247,
            "3,6": 237,
            "4,5": 243,
            "4,6": 236,
            "5,6": 254,
        },
        "matrix_metadata_hash": "d6d73d38ace5fb9f4229132dffe98baca875d2395134a0d44f6cdfbca4cbd7fe",
        "status": "RANK_COMPUTED",
    },
    "multiplicity_spread_cyclic_3456_balanced_r2_seed_202608163": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 87,
        "rank": 87,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 2, "2": 20, "3": 15, "4": 20, "5": 20, "6": 10},
        "remaining_pairwise_equations": 3597,
        "remaining_equations_by_pair": {
            "1,2": 245,
            "1,3": 240,
            "1,4": 239,
            "1,5": 235,
            "1,6": 241,
            "2,3": 242,
            "2,4": 231,
            "2,5": 238,
            "2,6": 234,
            "3,4": 252,
            "3,5": 241,
            "3,6": 242,
            "4,5": 241,
            "4,6": 234,
            "5,6": 242,
        },
        "matrix_metadata_hash": "261e4f24e6488c49c87649aba3abd9eef1a9400530c9f8b729f5d2a2ab47035d",
        "status": "RANK_COMPUTED",
    },
    "multiplicity_spread_cyclic_3456_balanced_r1_seed_202608146": {
        "field_mode": "exact",
        "field_label": "GF(17^32)",
        "field_size": "2367911594760467245844106297320951247361",
        "compressed_variables": 101,
        "rank": 101,
        "nullity": 0,
        "non_diagonal_solution_found": False,
        "compressed_dimensions_by_witness": {"1": 8, "2": 20, "3": 19, "4": 24, "5": 22, "6": 8},
        "remaining_pairwise_equations": 3648,
        "remaining_equations_by_pair": {
            "1,2": 254,
            "1,3": 246,
            "1,4": 244,
            "1,5": 239,
            "1,6": 237,
            "2,3": 252,
            "2,4": 241,
            "2,5": 236,
            "2,6": 237,
            "3,4": 242,
            "3,5": 241,
            "3,6": 237,
            "4,5": 255,
            "4,6": 240,
            "5,6": 247,
        },
        "matrix_metadata_hash": "def98ed532024ed996bde92f432273d812fdf4b7a7a0df53023f33d45c6d6c85",
        "status": "RANK_COMPUTED",
    },
}


def load_multiplicity_scanner():
    spec = importlib.util.spec_from_file_location(
        "m1_multiplicity_scanner", MULTIPLICITY_SCANNER_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


mult = load_multiplicity_scanner()
base = mult.base


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


def surrogate_points() -> list[int]:
    root = primitive_root_prime(SURROGATE_FIELD_SIZE)
    subgroup_generator = pow(root, (SURROGATE_FIELD_SIZE - 1) // N, SURROGATE_FIELD_SIZE)
    points = [pow(subgroup_generator, idx, SURROGATE_FIELD_SIZE) for idx in range(N)]
    assert len(set(points)) == N
    return points


SURROGATE_H = surrogate_points()


def support_positions(memberships: list[list[int]]) -> list[list[int]]:
    supports = [[] for _idx in range(LIST_SIZE)]
    for pos, members in enumerate(memberships):
        for member in members:
            supports[member].append(pos)
    return supports


def intersection_positions(supports: list[list[int]]) -> dict[tuple[int, int], list[int]]:
    intersections = {}
    for i in range(LIST_SIZE):
        set_i = set(supports[i])
        for j in range(i + 1, LIST_SIZE):
            intersections[(i, j)] = sorted(set_i.intersection(supports[j]))
    return intersections


def locator_values_mod(points: list[int], vanish_positions: list[int]) -> list[int]:
    roots = [points[pos] for pos in vanish_positions]
    values = []
    prime = SURROGATE_FIELD_SIZE
    for point in points:
        acc = 1
        for root in roots:
            acc = (acc * (point - root)) % prime
        values.append(acc)
    return values


def pair_label(pair: tuple[int, int]) -> str:
    return f"{pair[0]},{pair[1]}"


def dense_rank_mod(rows: list[list[int]], ncols: int, prime: int) -> int:
    rank = 0
    pivot_col = 0
    rows = [row[:] for row in rows if any(value % prime for value in row)]
    while rank < len(rows) and pivot_col < ncols:
        pivot = None
        for idx in range(rank, len(rows)):
            if rows[idx][pivot_col] % prime:
                pivot = idx
                break
        if pivot is None:
            pivot_col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][pivot_col] % prime, prime - 2, prime)
        rows[rank] = [(value * inv) % prime for value in rows[rank]]
        pivot_row = rows[rank]
        for idx in range(len(rows)):
            if idx == rank:
                continue
            factor = rows[idx][pivot_col] % prime
            if factor:
                rows[idx] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(rows[idx], pivot_row)
                ]
        rank += 1
        pivot_col += 1
    return rank


def surrogate_rank_gate(memberships: list[list[int]]) -> dict[str, Any]:
    supports = support_positions(memberships)
    intersections = intersection_positions(supports)
    witness_dims: dict[str, int] = {}
    witness_offsets: dict[int, int] = {}
    locator_eval: dict[int, list[int]] = {}
    ambient_dimension = 0
    for witness in range(1, LIST_SIZE):
        vanish = intersections[(0, witness)]
        dim = K - len(vanish)
        if dim <= 0:
            return {
                "field_mode": "surrogate",
                "field_label": "GF(12289)_surrogate",
                "field_size": str(SURROGATE_FIELD_SIZE),
                "compressed_variables": 0,
                "rank": None,
                "nullity": None,
                "status": "ANCHOR_INTERSECTION_TOO_LARGE",
            }
        witness_dims[str(witness)] = dim
        witness_offsets[witness] = ambient_dimension
        ambient_dimension += dim
        locator_eval[witness] = locator_values_mod(SURROGATE_H, vanish)

    rows: list[list[int]] = []
    remaining_equations_by_pair: dict[str, int] = {}
    prime = SURROGATE_FIELD_SIZE
    for i in range(1, LIST_SIZE):
        for j in range(i + 1, LIST_SIZE):
            positions = intersections[(i, j)]
            remaining_equations_by_pair[pair_label((i, j))] = len(positions)
            dim_i = witness_dims[str(i)]
            dim_j = witness_dims[str(j)]
            off_i = witness_offsets[i]
            off_j = witness_offsets[j]
            for pos in positions:
                point = SURROGATE_H[pos]
                powers_i = [1]
                for _degree in range(1, dim_i):
                    powers_i.append((powers_i[-1] * point) % prime)
                powers_j = [1]
                for _degree in range(1, dim_j):
                    powers_j.append((powers_j[-1] * point) % prime)
                row = [0 for _idx in range(ambient_dimension)]
                scale_i = locator_eval[i][pos]
                scale_j = locator_eval[j][pos]
                for degree, value in enumerate(powers_i):
                    row[off_i + degree] = (scale_i * value) % prime
                for degree, value in enumerate(powers_j):
                    row[off_j + degree] = (-scale_j * value) % prime
                rows.append(row)

    rank = dense_rank_mod(rows, ambient_dimension, prime)
    nullity = ambient_dimension - rank
    return {
        "field_mode": "surrogate",
        "field_label": "GF(12289)_surrogate",
        "field_size": str(prime),
        "compressed_variables": ambient_dimension,
        "rank": rank,
        "nullity": nullity,
        "non_diagonal_solution_found": nullity > 0,
        "compressed_dimensions_by_witness": witness_dims,
        "remaining_pairwise_equations": len(rows),
        "remaining_equations_by_pair": remaining_equations_by_pair,
        "matrix_metadata_hash": base.hash_payload(
            {
                "field_mode": "surrogate",
                "witness_dims": witness_dims,
                "remaining_equations_by_pair": remaining_equations_by_pair,
                "support_hash": base.hash_payload([sorted(members) for members in memberships]),
            }
        ),
        "status": "RANK_COMPUTED",
    }


def generated_candidate_specs() -> list[dict[str, Any]]:
    seeds = [
        "cyclic_45_interval_high_overlap",
        "cyclic_45_balanced",
        "cyclic_3456_near_boundary",
        "cyclic_3456_balanced",
    ]
    objectives = [
        ("multiplicity_spread", False),
        ("pair_boundary", False),
        ("anchor_compression", False),
        ("mixed_boundary_spread", False),
    ]
    specs = []
    counter = 202607500
    for seed_name in seeds:
        for objective, restrict_same_fiber in objectives:
            for repeat in range(3):
                counter += 17
                specs.append(
                    {
                        "seed_name": seed_name,
                        "objective": objective,
                        "repeat": repeat,
                        "random_seed": counter,
                        "steps": 900,
                        "restrict_same_fiber": restrict_same_fiber,
                    }
                )
    return specs


def generated_candidates() -> list[dict[str, Any]]:
    rows = []
    for spec in generated_candidate_specs():
        seed_memberships = base.seed_memberships(spec["seed_name"])
        memberships, accepted, attempted_valid = mult.mutate(
            seed_memberships,
            objective=spec["objective"],
            seed=spec["random_seed"],
            steps=spec["steps"],
            restrict_same_fiber=spec["restrict_same_fiber"],
        )
        summary = base.support_summary(memberships)
        profile = base.quotient_fiber_profile(memberships)
        row_proxy = base.row_pattern_proxy(summary, profile, "pair_boundary")
        score, _summary, _profile = mult.proxy_score(memberships, spec["objective"])
        candidate_id = (
            f"{spec['objective']}_{spec['seed_name']}_"
            f"r{spec['repeat']}_seed_{spec['random_seed']}"
        )
        rows.append(
            {
                "candidate_id": candidate_id,
                "mutation_family": "surrogate_rank_feedback_pair_replacement_membership_hypergraph",
                "seed_design": spec["seed_name"],
                "search_objective": spec["objective"],
                "random_seed": spec["random_seed"],
                "repeat": spec["repeat"],
                "mutation_steps": spec["steps"],
                "valid_mutation_attempts": attempted_valid,
                "accepted_mutations": accepted,
                "restrict_same_quotient_fiber": spec["restrict_same_fiber"],
                "memberships": memberships,
                "support_design": summary,
                "quotient_fiber_profile": profile,
                "pre_rank_proxy": {
                    "method": "multiplicity_pair_boundary_prefilter",
                    "proxy_score": score,
                    "compressed_variables": row_proxy["compressed_variables"],
                    "multiplicity_spread_score": mult.multiplicity_spread_score(summary),
                    "repeated_fiber_pattern_score": row_proxy["repeated_fiber_pattern_score"],
                    "pairs_at_255": summary["pair_intersections_at_255"],
                    "status": "SCORED",
                },
            }
        )
    rows.sort(
        key=lambda row: (
            row["pre_rank_proxy"]["proxy_score"],
            row["support_design"]["pair_intersections_at_255"],
            row["pre_rank_proxy"]["multiplicity_spread_score"],
            -row["pre_rank_proxy"]["compressed_variables"],
            row["candidate_id"],
        ),
        reverse=True,
    )
    return rows


def retained_candidates() -> list[dict[str, Any]]:
    prefiltered = generated_candidates()[:PREFILTER_LIMIT]
    ranked = []
    for row in prefiltered:
        gate = surrogate_rank_gate(row["memberships"])
        row = dict(row)
        row["surrogate_rank_gate"] = gate
        row["rank_feedback"] = {
            "method": "exact_GF_12289_rank_feedback_after_prefilter",
            "prefilter_limit": PREFILTER_LIMIT,
            "surrogate_nullity": gate["nullity"],
            "surrogate_rank": gate["rank"],
            "compressed_variables": gate["compressed_variables"],
            "rank_defect_found": gate["nullity"] not in {None, 0},
            "status": "SCORED",
        }
        ranked.append(row)
    ranked.sort(
        key=lambda row: (
            row["rank_feedback"]["surrogate_nullity"] or 0,
            -row["rank_feedback"]["surrogate_rank"],
            -row["rank_feedback"]["compressed_variables"],
            row["support_design"]["pair_intersections_at_255"],
            row["pre_rank_proxy"]["proxy_score"],
            row["candidate_id"],
        ),
        reverse=True,
    )
    return ranked[:RETAINED_CANDIDATES]


def exact_rank_from_precomputed(candidate_id: str) -> dict[str, Any]:
    computed = PRECOMPUTED_EXACT_RANKS.get(candidate_id)
    if computed is None:
        return {
            "field_mode": "exact",
            "field_label": "GF(17^32)",
            "field_size": str(FIELD_DENOMINATOR),
            "rank": None,
            "nullity": None,
            "status": "NOT_RUN",
        }
    return computed


def build_candidates() -> list[dict[str, Any]]:
    rows = []
    for candidate in retained_candidates():
        exact_gate = exact_rank_from_precomputed(candidate["candidate_id"])
        proof_status = (
            "ROUTE_CUT_TESTED_CANDIDATE"
            if exact_gate.get("nullity") == 0
            else "CANDIDATE_PROXY_NULLITY"
            if candidate["surrogate_rank_gate"].get("nullity") not in {None, 0}
            else "CANDIDATE"
        )
        row = {key: value for key, value in candidate.items() if key != "memberships"}
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


def threshold_floor() -> int:
    return FIELD_DENOMINATOR // (2**TARGET_BITS)


def build_result() -> dict[str, Any]:
    candidates = build_candidates()
    exact_rows = [row for row in candidates if row["sage_exact_rank"]["status"] != "NOT_RUN"]
    best_exact_nullity = max(
        (row["sage_exact_rank"]["nullity"] or 0 for row in exact_rows),
        default=None,
    )
    proxy_positive_count = sum(
        1 for row in candidates if row["surrogate_rank_gate"]["nullity"] not in {None, 0}
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
        "field_denominator": str(FIELD_DENOMINATOR),
        "field_denominator_label": "17^32",
        "target_bits": TARGET_BITS,
        "threshold_floor": threshold_floor(),
        "minimum_to_clear": threshold_floor() + 1,
        "target_agreement": TARGET_AGREEMENT,
        "baseline": {
            "current_pr_133_agreement": CURRENT_PR_133_AGREEMENT,
            "current_pr_133_lambda_lower": CURRENT_PR_133_LAMBDA_LOWER,
            "source": "PR #133 hybrid quotient-residual certificate",
        },
        "search_summary": {
            "generated_candidate_count": len(generated_candidate_specs()),
            "prefiltered_for_surrogate_rank_count": PREFILTER_LIMIT,
            "retained_candidate_count": len(candidates),
            "exact_audited_count": len(exact_rows),
            "candidate_family": "surrogate-rank-feedback multiplicity-changing pair replacements",
            "rank_proxy": "actual GF(12289) reduced rank after multiplicity/pair-boundary prefilter",
            "surrogate_field": "GF(12289), 512 | 12288",
            "exact_field": "GF(17^32)",
            "proxy_positive_count": proxy_positive_count,
            "best_exact_nullity": best_exact_nullity,
            "status": status,
        },
        "candidates": candidates,
        "interpretation": {
            "support_packing_blocks_a327": False,
            "surrogate_rank_feedback_found_proxy_nullity": proxy_positive_count > 0,
            "exact_audited_candidate_found_nullity": best_exact_nullity not in {0, None},
            "candidate_found": False,
            "status": status,
        },
        "open_layers": {
            "larger_stochastic_beam": True,
            "constructive_rank_defect_objective": True,
            "positive_exact_nullity_candidate": best_exact_nullity not in {0, None},
            "non_diagonal_nullspace_extraction": True,
            "global_support_pattern_rank_nullity_classification": True,
            "global_Lambda_mu_327_upper_bound": True,
            "status": "PARTIAL",
        },
        "sage_audit": {
            "script": "experimental/scripts/audit_m1_support_pattern_surrogate_rank_feedback_search.sage",
            "recomputes_retained_candidates": True,
            "constructs_GF_17_32": True,
            "checks_python_surrogate_rank_gate": True,
            "uses_exact_rank_gate": True,
        },
        "repo_claim": {
            "mca_counted": False,
            "not_claimed": [
                "MCA N_bad",
                "protocol soundness",
                "ordinary list decoding beyond the stated interleaved-list predicate",
                "a=327 interleaved-list certificate",
                "global Lambda_mu(C,327) <= 6",
                "global support-pattern rank-nullity classification",
                "exact Lambda_mu",
                "exact delta*_C",
                "improvement over PR #133",
            ],
        },
        "global_status": {
            "candidate_found": False,
            "improves_pr_133": False,
            "status": status,
        },
        "status": "M1_SUPPORT_PATTERN_SURROGATE_RANK_FEEDBACK_SEARCH_ROUTE_CUT_PARTIAL",
    }
    result["record_hash"] = base.hash_payload(
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
                "prefilter_score": row["pre_rank_proxy"]["proxy_score"],
                "support_hash": row["support_design"]["support_hash"],
                "multiplicity_histogram": row["support_design"]["multiplicity_histogram"],
                "pair_max": row["support_design"]["pair_intersection_max"],
                "pairs_at_255": row["support_design"]["pair_intersections_at_255"],
                "surrogate_rank": row["surrogate_rank_gate"]["rank"],
                "surrogate_nullity": row["surrogate_rank_gate"]["nullity"],
                "compressed_variables": row["surrogate_rank_gate"]["compressed_variables"],
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
        print(f"generated {len(generated_candidate_specs())} support-pattern mutations")
        print(f"ranked {PREFILTER_LIMIT} candidates by actual GF(12289) surrogate rank")
        print(f"retained {len(result['candidates'])} rank-feedback candidates")
        print(f"status: {result['global_status']['status']}")


if __name__ == "__main__":
    main()
