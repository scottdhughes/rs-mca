#!/usr/bin/env python3
"""Prescribed functional-collision realization scan for M1 a=327.

This branch keeps the selected-class coordinate ledger from the current
cycle-guarded endpoint fixed, then synthesizes actual GF(17) template vectors
with prescribed pair-difference collision patterns.  It tests whether those
realized templates, not synthetic functional rows, produce proxy nullity.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "af58bd0"
PREVIOUS_DATA = Path("experimental/data/m1_a327_cycleguard_functional_collision_template_synthesis.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_prescribed_functional_collision_realization.json")

ROOT = Path(__file__).resolve().parents[2]
FCOLL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycleguard_functional_collision_template_synthesis.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
P = 17
TEMPLATE_DIM = 6
VARIABLE_COUNT = TEMPLATE_DIM * 256

REQUIRED_NONCLAIMS = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
    "Sage GF(17^32) exact lift",
    "MCA/protocol consequence from this list-track proxy",
    "global obstruction outside the tested prescribed functional-collision realization front",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fcoll = load_module("cycleguard_functional_collision_template_synthesis", FCOLL_SCRIPT)
feedback = fcoll.feedback
p456 = fcoll.p456


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def size_histogram(coordinate_classes: list[dict[str, Any]]) -> dict[str, int]:
    return dict(Counter(str(int(row["size"])) for row in coordinate_classes))


def compact_vector(vector: list[int]) -> list[int]:
    return [int(value) % P for value in vector]


def rank_mod_p(rows: list[list[int]], ncols: int = TEMPLATE_DIM) -> int:
    matrix = [[int(value) % P for value in row] for row in rows if any(int(value) % P for value in row)]
    rank = 0
    for col in range(ncols):
        pivot = None
        for row_idx in range(rank, len(matrix)):
            if matrix[row_idx][col] % P:
                pivot = row_idx
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col], -1, P)
        matrix[rank] = [(value * inv) % P for value in matrix[rank]]
        for row_idx in range(rank + 1, len(matrix)):
            if not matrix[row_idx][col] % P:
                continue
            factor = matrix[row_idx][col] % P
            matrix[row_idx] = [(matrix[row_idx][idx] - factor * matrix[rank][idx]) % P for idx in range(ncols)]
        rank += 1
        if rank == ncols:
            break
    return rank


def normalize_projective(row: list[int]) -> tuple[int, ...] | None:
    values = [int(value) % P for value in row]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return tuple((entry * inv) % P for entry in values)
    return None


def vector_rank(vectors: list[list[int]]) -> int:
    return rank_mod_p(vectors, ncols=TEMPLATE_DIM)


def template_equal_pairs(vectors: list[list[int]]) -> list[str]:
    out = []
    keys = [tuple(compact_vector(row)) for row in vectors]
    for left in range(7):
        for right in range(left + 1, 7):
            if keys[left] == keys[right]:
                out.append(f"P{left + 1}{right + 1}")
    return out


def pairdiff_metrics(vectors: list[list[int]]) -> dict[str, Any]:
    groups: dict[tuple[int, ...], list[str]] = {}
    for left in range(7):
        for right in range(left + 1, 7):
            diff = [(vectors[right][idx] - vectors[left][idx]) % P for idx in range(TEMPLATE_DIM)]
            key = normalize_projective(diff)
            if key is None:
                groups.setdefault(tuple([0] * TEMPLATE_DIM), []).append(f"P{left + 1}{right + 1}")
            else:
                groups.setdefault(key, []).append(f"P{left + 1}{right + 1}")
    collisions = [pairs for pairs in groups.values() if len(pairs) > 1]
    return {
        "pairdiff_groups": len(groups),
        "pairdiff_collision_groups": len(collisions),
        "pairdiff_collision_excess": sum(len(pairs) - 1 for pairs in collisions),
        "largest_pairdiff_collision_group": max((len(pairs) for pairs in collisions), default=1),
        "pairdiff_collision_pairs": collisions[:8],
    }


def add(u: list[int], v: list[int], scalar: int = 1) -> list[int]:
    return [(u[idx] + scalar * v[idx]) % P for idx in range(TEMPLATE_DIM)]


def e(idx: int) -> list[int]:
    return [1 if col == idx else 0 for col in range(TEMPLATE_DIM)]


BASE_SHAPES: list[tuple[str, list[list[int]]]] = [
    (
        "basis_simple",
        [e(0), e(1), e(2), e(3), e(4), e(5), [0, 0, 0, 0, 0, 0]],
    ),
    (
        "one_parallel_pairdiff",
        [e(5), add(e(5), e(0)), e(1), add(e(1), e(0)), e(2), e(3), e(4)],
    ),
    (
        "two_parallel_pairdiff",
        [e(4), add(e(4), e(0)), e(5), add(e(5), e(0)), e(1), e(2), e(3)],
    ),
    (
        "parallelogram_quad",
        [e(5), add(e(5), e(0)), add(e(5), e(1)), add(add(e(5), e(0)), e(1)), e(2), e(3), e(4)],
    ),
    (
        "triangle_plus_basis",
        [e(0), e(1), add(e(0), e(1)), e(2), e(3), e(4), e(5)],
    ),
]


def permute_vectors(vectors: list[list[int]], permutation: list[int]) -> list[list[int]]:
    return [compact_vector(vectors[idx]) for idx in permutation]


def scale_coordinates(vectors: list[list[int]], scalars: list[int]) -> list[list[int]]:
    return [[(value * scalars[col]) % P for col, value in enumerate(row)] for row in vectors]


def shear_coordinates(vectors: list[list[int]], source: int, target: int, scalar: int) -> list[list[int]]:
    out = []
    for row in vectors:
        new = list(row)
        new[target] = (new[target] + scalar * new[source]) % P
        out.append(new)
    return out


def random_rank6_template(seed: int, relation_pairs: int) -> list[list[int]]:
    rng = random.Random(seed)
    vectors = [[rng.randrange(P) for _ in range(TEMPLATE_DIM)] for _ in range(7)]
    # Force one or two prescribed equal pair differences while keeping actual
    # vector rows otherwise random.  The structural screen below rejects
    # degenerate templates.
    if relation_pairs >= 1:
        vectors[3] = add(vectors[2], [(vectors[1][idx] - vectors[0][idx]) % P for idx in range(TEMPLATE_DIM)])
    if relation_pairs >= 2:
        vectors[5] = add(vectors[4], [(vectors[1][idx] - vectors[0][idx]) % P for idx in range(TEMPLATE_DIM)])
    return [compact_vector(row) for row in vectors]


def template_specs(max_templates: int) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    permutations = [
        list(range(7)),
        [6, 0, 1, 2, 3, 4, 5],
        [0, 2, 4, 6, 1, 3, 5],
        [1, 3, 5, 0, 2, 4, 6],
        [2, 3, 6, 0, 1, 4, 5],
        [4, 0, 5, 1, 6, 2, 3],
    ]
    scalar_sets = [
        [1, 1, 1, 1, 1, 1],
        [1, 2, 3, 5, 8, 13],
        [1, 4, 9, 16, 8, 2],
    ]
    for shape_id, vectors in BASE_SHAPES:
        for perm_id, permutation in enumerate(permutations):
            for scalar_id, scalars in enumerate(scalar_sets):
                base = scale_coordinates(permute_vectors(vectors, permutation), scalars)
                specs.append(
                    {
                        "template_family": "prescribed_pairdiff_collision",
                        "shape_id": shape_id,
                        "permutation_id": perm_id,
                        "coordinate_scalars_id": scalar_id,
                        "vectors": base,
                    }
                )
                for source, target, scalar in [(0, 5, 1), (1, 4, 2), (2, 3, 4)]:
                    specs.append(
                        {
                            "template_family": "prescribed_pairdiff_collision_shear",
                            "shape_id": shape_id,
                            "permutation_id": perm_id,
                            "coordinate_scalars_id": scalar_id,
                            "shear": [source, target, scalar],
                            "vectors": shear_coordinates(base, source, target, scalar),
                        }
                    )
                if len(specs) >= max_templates:
                    return specs[:max_templates]
    seed = 0
    while len(specs) < max_templates:
        relation_pairs = 1 + (seed % 2)
        specs.append(
            {
                "template_family": "random_prescribed_pairdiff_collision",
                "shape_id": f"random_seed_{seed}_relations_{relation_pairs}",
                "seed": seed,
                "relation_pairs": relation_pairs,
                "vectors": random_rank6_template(seed, relation_pairs),
            }
        )
        seed += 1
    return specs[:max_templates]


def candidate_from_spec(source: dict[str, Any], spec: dict[str, Any], order: int) -> dict[str, Any]:
    vectors = [compact_vector(row) for row in spec["vectors"]]
    coordinate_classes = source["coordinate_classes"]
    candidate = {
        "template_id": f"pfcoll_{order:04d}_{spec['shape_id']}",
        "template_family": spec["template_family"],
        "template_dimension": TEMPLATE_DIM,
        "template_vectors": vectors,
        "assignment_strategy": source["assignment_strategy"],
        "assignment_seed": int(source["assignment_seed"]),
        "coordinate_classes": coordinate_classes,
        "coordinate_classes_hash": source["coordinate_classes_hash"],
        "support_vector": [int(value) for value in source["support_vector"]],
        "pair7_counts": [int(value) for value in source["pair7_counts"]],
        "max_pair_count": int(source["max_pair_count"]),
        "selected_class_size_counts": size_histogram(coordinate_classes),
        "variable_count": VARIABLE_COUNT,
        "prescribed_template_spec": {key: value for key, value in spec.items() if key != "vectors"},
    }
    candidate["total_effective_cost"] = fcoll.recompute_total_effective_cost(candidate)
    return candidate


def candidate_metrics(candidate: dict[str, Any], order: int) -> dict[str, Any]:
    metrics = fcoll.functional_metrics(candidate)
    structural = p456.tchamber.candidate_screen_row(candidate)
    pairdiff = pairdiff_metrics(candidate["template_vectors"])
    equal_pairs = template_equal_pairs(candidate["template_vectors"])
    status = structural["backward_structural_status"]
    if equal_pairs and status == "TCHAMBER_STRUCTURAL_PASS":
        status = "PFCOLL_TEMPLATE_EQUAL_PAIR"
    realized = (
        status == "TCHAMBER_STRUCTURAL_PASS"
        and metrics["functional_span_rank"] == TEMPLATE_DIM
        and metrics["forced_functional_identities"] == 0
        and metrics["functional_classes"] <= 18
        and metrics["raw_collision_excess"] >= 1759
    )
    return {
        "candidate_order": order,
        "template_id": candidate["template_id"],
        "template_family": candidate["template_family"],
        "shape_id": candidate["prescribed_template_spec"].get("shape_id"),
        "support_vector": candidate["support_vector"],
        "pair7_counts": candidate["pair7_counts"],
        "max_pair_count": candidate["max_pair_count"],
        "total_effective_cost": candidate["total_effective_cost"],
        "template_vector_rank": vector_rank(candidate["template_vectors"]),
        "template_equal_pairs": equal_pairs,
        "structural_status": status,
        "prescribed_collision_realized": realized,
        **pairdiff,
        **metrics,
    }


def candidate_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    structural_priority = 0 if row["structural_status"] == "TCHAMBER_STRUCTURAL_PASS" else 1
    return (
        structural_priority,
        0 if row["prescribed_collision_realized"] else 1,
        -int(row["pairdiff_collision_excess"]),
        -int(row["raw_collision_excess"]),
        int(row["functional_classes"]),
        -int(row["functional_span_rank"]),
        int(row["max_functional_support"]),
        row["template_id"],
    )


def profile_row(candidate: dict[str, Any], profile: dict[str, Any], candidate_order: int, profile_order: int) -> dict[str, Any]:
    row = fcoll.profile_row(candidate, profile, candidate_order, profile_order)
    metrics = fcoll.functional_metrics(candidate)
    pairdiff = pairdiff_metrics(candidate["template_vectors"])
    row.update(
        {
            "prescribed_collision_realized": True,
            "pairdiff_collision_excess": pairdiff["pairdiff_collision_excess"],
            "pairdiff_collision_groups": pairdiff["pairdiff_collision_groups"],
            "raw_functional_rows": metrics["raw_functional_rows"],
            "functional_classes": metrics["functional_classes"],
            "raw_collision_excess": metrics["raw_collision_excess"],
            "max_raw_collision_multiplicity": metrics["max_raw_collision_multiplicity"],
            "max_functional_support": metrics["max_functional_support"],
            "functional_span_rank": metrics["functional_span_rank"],
            "forced_functional_identities": metrics["forced_functional_identities"],
        }
    )
    return row


def profile_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["pairdiff_collision_excess"]),
        -int(row["raw_collision_excess"]),
        int(row["row_minus_col"]),
        int(row["matrix_shape"][0]),
        int(row["q_variable_count"]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        -int(row["pairdiff_collision_excess"]),
        -int(row["raw_collision_excess"]),
        int(row["row_minus_col"]),
        row["template_id"],
        row["basis_id"],
    )


def build_record(max_templates: int, profile_candidate_limit: int, basis_profiles_per_candidate: int, profile_rank_limit: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    source = previous["best_candidate"]

    candidate_rows = []
    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for order, spec in enumerate(template_specs(max_templates)):
        candidate = candidate_from_spec(source, spec, order)
        row = candidate_metrics(candidate, order)
        candidate_rows.append(row)
        if row["prescribed_collision_realized"]:
            candidates.append((candidate, row))

    profile_rows = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    profile_front = sorted(candidates, key=lambda item: candidate_sort_key(item[1]))[:profile_candidate_limit]
    for profile_candidate_order, (candidate, candidate_row) in enumerate(profile_front):
        for profile_order, profile in enumerate(
            p456.tchamber.basis_profiles(
                candidate,
                top_classes=26,
                random_bases=96,
                limit=basis_profiles_per_candidate,
            )
        ):
            row = profile_row(candidate, profile, int(candidate_row["candidate_order"]), profile_order)
            row["profile_candidate_order"] = profile_candidate_order
            profile_rows.append(row)
            source_profiles[(int(row["candidate_order"]), row["basis_id"])] = (candidate, profile)

    h_values = feedback.proxy_h_values(PROXY_PRIME)
    powers = feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    proxy_rows = []
    for target in sorted(profile_rows, key=profile_sort_key)[:profile_rank_limit]:
        candidate, profile = source_profiles[(int(target["candidate_order"]), target["basis_id"])]
        proxy = feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
        proxy_rows.append(
            {
                **target,
                "proxy_prime": proxy["proxy_prime"],
                "proxy_matrix_shape": proxy["matrix_shape"],
                "proxy_rank": proxy["proxy_rank"],
                "proxy_nullity": proxy["proxy_nullity"],
                "best_failure_mode": (
                    "PFCOLL_REALIZATION_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "PFCOLL_REALIZATION_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best_profile = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    best_candidate = None
    if best_profile is not None:
        candidate, _profile = source_profiles[(int(best_profile["candidate_order"]), best_profile["basis_id"])]
        best_candidate = {
            **feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
            "template_vectors": candidate["template_vectors"],
            "prescribed_template_spec": candidate["prescribed_template_spec"],
            "selected_class_size_counts": candidate["selected_class_size_counts"],
            "total_effective_cost": candidate["total_effective_cost"],
        }

    failure = "PFCOLL_REALIZATION_NO_REALIZED_COLLISION"
    proof_status = "EXACT_EXTRACTION_NO_A327 / PFCOLL_REALIZATION_NO_REALIZED_COLLISION / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "PFCOLL_REALIZATION_PROXY_POSITIVE" if positives else "PFCOLL_REALIZATION_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / PFCOLL_REALIZATION_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / PFCOLL_REALIZATION_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    best_realized = min(candidate_rows, key=candidate_sort_key) if candidate_rows else None
    status_counts = Counter(row["structural_status"] for row in candidate_rows)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_functional_collision_template_synthesis": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_template_id": previous["best_profile"]["template_id"],
            "best_basis_id": previous["best_profile"]["basis_id"],
            "best_proxy_rank": previous["functional_collision_template_synthesis"]["best_proxy_rank"],
            "best_proxy_nullity": previous["functional_collision_template_synthesis"]["best_proxy_nullity"],
            "proxy_positive_profiles": previous["functional_collision_template_synthesis"]["proxy_positive_profiles"],
            "failure_mode": previous["functional_collision_template_synthesis"]["best_failure_mode"],
        },
        "prescribed_functional_collision_realization": {
            "proxy_prime": PROXY_PRIME,
            "max_templates": max_templates,
            "profile_candidate_limit": profile_candidate_limit,
            "basis_profiles_per_candidate": basis_profiles_per_candidate,
            "profile_rank_limit": profile_rank_limit,
            "templates_tested": len(candidate_rows),
            "structural_pass_templates": sum(1 for row in candidate_rows if row["structural_status"] == "TCHAMBER_STRUCTURAL_PASS"),
            "prescribed_collision_realized_templates": len(candidates),
            "template_status_counts": dict(status_counts),
            "basis_profiles_constructed": len(profile_rows),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_realized_pairdiff_collision_excess": None if best_realized is None else best_realized["pairdiff_collision_excess"],
            "best_realized_functional_classes": None if best_realized is None else best_realized["functional_classes"],
            "best_proxy_rank": None if best_profile is None else best_profile["proxy_rank"],
            "best_proxy_nullity": None if best_profile is None else best_profile["proxy_nullity"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_realized_template": best_realized,
        "best_profile": best_profile,
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
    parser.add_argument("--max-templates", type=int, default=180)
    parser.add_argument("--profile-candidate-limit", type=int, default=24)
    parser.add_argument("--basis-profiles-per-candidate", type=int, default=2)
    parser.add_argument("--profile-rank-limit", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        profile_candidate_limit=args.profile_candidate_limit,
        basis_profiles_per_candidate=args.basis_profiles_per_candidate,
        profile_rank_limit=args.profile_rank_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["prescribed_functional_collision_realization"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "templates_tested": search["templates_tested"],
                    "structural_pass_templates": search["structural_pass_templates"],
                    "prescribed_collision_realized_templates": search["prescribed_collision_realized_templates"],
                    "basis_profiles_constructed": search["basis_profiles_constructed"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_realized_pairdiff_collision_excess": search["best_realized_pairdiff_collision_excess"],
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
        print("M1_A327_PRESCRIBED_FUNCTIONAL_COLLISION_REALIZATION_READY")


if __name__ == "__main__":
    main()
