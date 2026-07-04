#!/usr/bin/env python3
"""Template-vector mutation scan for M1 a=327 cycleguard functional collisions."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "f2b56ec"
PREVIOUS_DATA = Path("experimental/data/m1_a327_cycleguard_dependency_forced_profile_generator.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_cycleguard_functional_collision_template_synthesis.json")

ROOT = Path(__file__).resolve().parents[2]
FORCED_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_cycleguard_dependency_forced_profile_generator.py"

TARGET_AGREEMENT = 327
PROXY_PRIME = 12289
P = 17
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


forced = load_module("cycleguard_dependency_forced_profile_generator", FORCED_SCRIPT)
dep = forced.dep
feedback = forced.feedback
p456 = forced.p456


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def vector_key(vector: list[int]) -> tuple[int, ...]:
    return tuple(int(value) % P for value in vector)


def template_equal_pairs(vectors: list[list[int]]) -> list[str]:
    pairs = []
    for left in range(7):
        for right in range(left + 1, 7):
            if vector_key(vectors[left]) == vector_key(vectors[right]):
                pairs.append(f"P{left + 1}{right + 1}")
    return pairs


def normalized_row(row: list[int]) -> tuple[int, ...] | None:
    values = [int(value) % P for value in row]
    for value in values:
        if value:
            inv = pow(value, -1, P)
            return tuple((entry * inv) % P for entry in values)
    return None


def raw_functional_rows(candidate: dict[str, Any]) -> list[tuple[int, ...]]:
    out = []
    vectors = candidate["template_vectors"]
    for coord in candidate["coordinate_classes"]:
        members = [int(value) for value in coord["members"]]
        for row in feedback.zstable.functional.row_basis_mod_p(vectors, members):
            key = normalized_row(row)
            if key is not None:
                out.append(key)
    return out


def functional_metrics(candidate: dict[str, Any]) -> dict[str, Any]:
    raw_rows = raw_functional_rows(candidate)
    classes = feedback.zstable.functional.functional_classes(candidate)
    supports = [int(row["support_size"]) for row in classes]
    support_hash_counts = Counter(row["positions_hash"] for row in classes)
    raw_counts = Counter(raw_rows)
    return {
        "raw_functional_rows": len(raw_rows),
        "functional_classes": len(classes),
        "raw_collision_excess": len(raw_rows) - len(classes),
        "raw_collision_groups": sum(1 for value in raw_counts.values() if value > 1),
        "max_raw_collision_multiplicity": max(raw_counts.values()) if raw_counts else 0,
        "forced_functional_identities": sum(1 for row in classes if row["forced_identity"]),
        "max_functional_support": max(supports) if supports else 0,
        "support_duplicate_groups": sum(1 for value in support_hash_counts.values() if value > 1),
        "support_duplicate_excess": sum(value - 1 for value in support_hash_counts.values() if value > 1),
        "functional_span_rank": feedback.zstable.functional.rank_mod_p([row["functional"] for row in classes]),
    }


def recompute_total_effective_cost(candidate: dict[str, Any]) -> int:
    return p456.ninerow.syzygy.rowred.total_effective_cost_gf17(
        candidate["template_vectors"],
        candidate["coordinate_classes"],
    )


def mutation_specs(limit: int) -> list[dict[str, Any]]:
    specs = []
    deltas = [1, 2, 4, 8, 16]
    for witness in range(7):
        for coord in range(TEMPLATE_DIM):
            for delta in deltas:
                specs.append(
                    {
                        "mutation_family": "single_entry_delta",
                        "witness": witness,
                        "coordinate": coord,
                        "delta": delta,
                    }
                )
                if len(specs) >= limit:
                    return specs
    for target in range(7):
        for source in range(7):
            if target == source:
                continue
            for scalar in [1, 2, 4, 8]:
                specs.append(
                    {
                        "mutation_family": "witness_shear",
                        "target": target,
                        "source": source,
                        "scalar": scalar,
                    }
                )
                if len(specs) >= limit:
                    return specs
    return specs


def apply_mutation(base: dict[str, Any], spec: dict[str, Any], base_order: int, mutation_order: int) -> dict[str, Any]:
    candidate = copy.deepcopy(base)
    vectors = [[int(value) % P for value in row] for row in candidate["template_vectors"]]
    if spec["mutation_family"] == "single_entry_delta":
        witness = int(spec["witness"])
        coord = int(spec["coordinate"])
        vectors[witness][coord] = (vectors[witness][coord] + int(spec["delta"])) % P
    elif spec["mutation_family"] == "witness_shear":
        target = int(spec["target"])
        source = int(spec["source"])
        scalar = int(spec["scalar"])
        vectors[target] = [
            (vectors[target][idx] + scalar * vectors[source][idx]) % P
            for idx in range(TEMPLATE_DIM)
        ]
    else:
        raise ValueError(f"unknown mutation family {spec['mutation_family']}")
    candidate["template_vectors"] = vectors
    mutation_id = (
        f"fcoll_b{base_order}_m{mutation_order}_"
        f"{spec['mutation_family']}"
    )
    candidate["template_id"] = f"{base['template_id']}__{mutation_id}"
    candidate["mutation_id"] = mutation_id
    candidate["base_mutation_id"] = base.get("mutation_id")
    candidate["base_template_id"] = base.get("template_id")
    candidate["functional_collision_mutation"] = spec
    candidate["total_effective_cost"] = recompute_total_effective_cost(candidate)
    return candidate


def candidate_row(
    candidate: dict[str, Any],
    base_order: int,
    mutation_order: int,
    spec: dict[str, Any],
) -> dict[str, Any]:
    metrics = functional_metrics(candidate)
    structural = p456.tchamber.candidate_screen_row(candidate)
    equal_pairs = template_equal_pairs(candidate["template_vectors"])
    status = structural["backward_structural_status"]
    if equal_pairs and status == "TCHAMBER_STRUCTURAL_PASS":
        status = "FCOLL_TEMPLATE_PAIR_COLLISION"
    return {
        "base_order": base_order,
        "mutation_order": mutation_order,
        "template_id": candidate["template_id"],
        "base_template_id": candidate.get("base_template_id"),
        "base_mutation_id": candidate.get("base_mutation_id"),
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": int(candidate["assignment_seed"]),
        "mutation_spec": spec,
        "support_vector": [int(value) for value in candidate["support_vector"]],
        "pair7_counts": [int(value) for value in candidate["pair7_counts"]],
        "max_pair_count": int(candidate["max_pair_count"]),
        "total_effective_cost": int(candidate["total_effective_cost"]),
        "template_equal_pairs": equal_pairs,
        "structural_status": status,
        "raw_functional_rows": metrics["raw_functional_rows"],
        "functional_classes": metrics["functional_classes"],
        "raw_collision_excess": metrics["raw_collision_excess"],
        "raw_collision_groups": metrics["raw_collision_groups"],
        "max_raw_collision_multiplicity": metrics["max_raw_collision_multiplicity"],
        "forced_functional_identities": metrics["forced_functional_identities"],
        "functional_span_rank": metrics["functional_span_rank"],
        "max_functional_support": metrics["max_functional_support"],
        "support_duplicate_groups": metrics["support_duplicate_groups"],
        "support_duplicate_excess": metrics["support_duplicate_excess"],
    }


def candidate_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    structural_priority = 0 if row["structural_status"] == "TCHAMBER_STRUCTURAL_PASS" else 1
    return (
        structural_priority,
        -int(row["raw_collision_excess"]),
        -int(row["support_duplicate_excess"]),
        int(row["functional_classes"]),
        int(row["max_functional_support"]),
        int(row["total_effective_cost"]),
        row["template_id"],
    )


def profile_row(candidate: dict[str, Any], profile: dict[str, Any], candidate_order: int, profile_order: int) -> dict[str, Any]:
    row = dep.profile_row(candidate, profile, candidate_order, profile_order)
    metrics = functional_metrics(candidate)
    row.update(
        {
            "raw_functional_rows": metrics["raw_functional_rows"],
            "functional_classes": metrics["functional_classes"],
            "raw_collision_excess": metrics["raw_collision_excess"],
            "raw_collision_groups": metrics["raw_collision_groups"],
            "max_raw_collision_multiplicity": metrics["max_raw_collision_multiplicity"],
            "max_functional_support": metrics["max_functional_support"],
            "functional_span_rank": metrics["functional_span_rank"],
            "forced_functional_identities": metrics["forced_functional_identities"],
        }
    )
    return row


def profile_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["raw_collision_excess"]),
        -int(row["support_duplicate_excess"]),
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
        -int(row["raw_collision_excess"]),
        -int(row["support_duplicate_excess"]),
        int(row["row_minus_col"]),
        row["template_id"],
        row["basis_id"],
    )


def build_record(
    max_mutations: int,
    seed_offsets: int,
    max_candidates: int,
    max_diverse_candidates: int,
    base_candidate_limit: int,
    mutations_per_candidate: int,
    profile_candidate_limit: int,
    basis_profiles_per_candidate: int,
    profile_rank_limit: int,
) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    profiles, screened, selected_candidates = p456.structural_candidates(
        max_mutations=max_mutations,
        seed_offsets=seed_offsets,
        max_candidates=max_candidates,
        max_diverse_candidates=max_diverse_candidates,
    )
    specs = mutation_specs(mutations_per_candidate)
    mutation_rows = []
    mutated_candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    source_candidates: dict[int, dict[str, Any]] = {}
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}

    for base_order, (base, _screen) in enumerate(selected_candidates[:base_candidate_limit]):
        for mutation_order, spec in enumerate(specs):
            mutated = apply_mutation(base, spec, base_order, mutation_order)
            row = candidate_row(mutated, base_order, mutation_order, spec)
            mutation_rows.append(row)
            if row["structural_status"] != "TCHAMBER_STRUCTURAL_PASS":
                continue
            mutated_candidates.append((mutated, row))

    profile_rows = []
    profile_front = sorted(mutated_candidates, key=lambda item: candidate_sort_key(item[1]))[:profile_candidate_limit]
    for candidate_order, (candidate, _mutation_row) in enumerate(profile_front):
        source_candidates[candidate_order] = candidate
        for profile_order, profile in enumerate(
            p456.tchamber.basis_profiles(
                candidate,
                top_classes=26,
                random_bases=96,
                limit=basis_profiles_per_candidate,
            )
        ):
            row = profile_row(candidate, profile, candidate_order, profile_order)
            profile_rows.append(row)
            source_profiles[(candidate_order, row["basis_id"])] = (candidate, profile)

    h_values = feedback.proxy_h_values(PROXY_PRIME)
    powers = feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    targets = sorted(profile_rows, key=profile_sort_key)[:profile_rank_limit]
    proxy_rows = []
    for target in targets:
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
                    "FCOLL_TEMPLATE_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "FCOLL_TEMPLATE_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    best_candidate = None
    if best is not None:
        candidate, _profile = source_profiles[(int(best["candidate_order"]), best["basis_id"])]
        best_candidate = {
            **feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
            "functional_collision_mutation": candidate["functional_collision_mutation"],
            "base_mutation_id": candidate.get("base_mutation_id"),
        }

    failure = "FCOLL_TEMPLATE_NO_STRUCTURAL_PASS_MUTATIONS"
    proof_status = "EXACT_EXTRACTION_NO_A327 / FCOLL_TEMPLATE_NO_STRUCTURAL_PASS_MUTATIONS / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "FCOLL_TEMPLATE_PROXY_POSITIVE" if positives else "FCOLL_TEMPLATE_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / FCOLL_TEMPLATE_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / FCOLL_TEMPLATE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    best_mutation = min(mutation_rows, key=candidate_sort_key) if mutation_rows else None
    status_counts = Counter(row["structural_status"] for row in mutation_rows)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_dependency_forced_generator": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "forced_profiles_constructed": previous["dependency_forced_profile_generator"]["forced_profiles_constructed"],
            "support_coordinate_collision_profiles": previous["dependency_forced_profile_generator"]["support_coordinate_collision_profiles"],
            "coordinate_collision_profiles": previous["dependency_forced_profile_generator"]["coordinate_collision_profiles"],
            "proxy_ranked_profiles": previous["dependency_forced_profile_generator"]["proxy_ranked_profiles"],
            "proxy_positive_profiles": previous["dependency_forced_profile_generator"]["proxy_positive_profiles"],
            "best_proxy_rank": previous["dependency_forced_profile_generator"]["best_proxy_rank"],
            "best_proxy_nullity": previous["dependency_forced_profile_generator"]["best_proxy_nullity"],
            "failure_mode": previous["dependency_forced_profile_generator"]["best_failure_mode"],
        },
        "functional_collision_template_synthesis": {
            "proxy_prime": PROXY_PRIME,
            "max_mutations": max_mutations,
            "seed_offsets": seed_offsets,
            "max_candidates": max_candidates,
            "max_diverse_candidates": max_diverse_candidates,
            "base_candidate_limit": base_candidate_limit,
            "mutations_per_candidate": mutations_per_candidate,
            "profile_candidate_limit": profile_candidate_limit,
            "basis_profiles_per_candidate": basis_profiles_per_candidate,
            "profile_rank_limit": profile_rank_limit,
            "mutations_tested": len(mutation_rows),
            "structural_pass_mutations": len(mutated_candidates),
            "mutation_status_counts": dict(status_counts),
            "basis_profiles_constructed": len(profile_rows),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_mutation_raw_collision_excess": None if best_mutation is None else best_mutation["raw_collision_excess"],
            "best_mutation_functional_classes": None if best_mutation is None else best_mutation["functional_classes"],
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_mutation": best_mutation,
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
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond stated interleaved-list predicate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "Sage GF(17^32) exact lift",
            "MCA/protocol consequence from this list-track proxy",
            "global obstruction outside the tested functional-collision template synthesis front",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-mutations", type=int, default=646)
    parser.add_argument("--seed-offsets", type=int, default=3)
    parser.add_argument("--max-candidates", type=int, default=180)
    parser.add_argument("--max-diverse-candidates", type=int, default=80)
    parser.add_argument("--base-candidate-limit", type=int, default=4)
    parser.add_argument("--mutations-per-candidate", type=int, default=24)
    parser.add_argument("--profile-candidate-limit", type=int, default=16)
    parser.add_argument("--basis-profiles-per-candidate", type=int, default=2)
    parser.add_argument("--profile-rank-limit", type=int, default=8)
    args = parser.parse_args()
    record = build_record(
        max_mutations=args.max_mutations,
        seed_offsets=args.seed_offsets,
        max_candidates=args.max_candidates,
        max_diverse_candidates=args.max_diverse_candidates,
        base_candidate_limit=args.base_candidate_limit,
        mutations_per_candidate=args.mutations_per_candidate,
        profile_candidate_limit=args.profile_candidate_limit,
        basis_profiles_per_candidate=args.basis_profiles_per_candidate,
        profile_rank_limit=args.profile_rank_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["functional_collision_template_synthesis"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "mutations_tested": search["mutations_tested"],
                    "structural_pass_mutations": search["structural_pass_mutations"],
                    "basis_profiles_constructed": search["basis_profiles_constructed"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_mutation_raw_collision_excess": search["best_mutation_raw_collision_excess"],
                    "best_mutation_functional_classes": search["best_mutation_functional_classes"],
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
        print("M1_A327_CYCLEGUARD_FUNCTIONAL_COLLISION_TEMPLATE_SYNTHESIS_READY")


if __name__ == "__main__":
    main()
