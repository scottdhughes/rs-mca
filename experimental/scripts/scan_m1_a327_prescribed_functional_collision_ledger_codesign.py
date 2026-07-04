#!/usr/bin/env python3
"""Codesign selected-class ledgers and actual functional-collision templates."""

from __future__ import annotations

import argparse
import importlib.util
import json
from collections import Counter
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "e6fb874"
PREVIOUS_DATA = Path("experimental/data/m1_a327_prescribed_functional_collision_realization.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_prescribed_functional_collision_ledger_codesign.json")

ROOT = Path(__file__).resolve().parents[2]
PFCOLL_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_prescribed_functional_collision_realization.py"
LOWRANK_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_lowrank_template_selected_class_search.py"
DEPENG_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_dependency_engineered_rank_feedback.py"

TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
PROXY_PRIME = 12289
TEMPLATE_DIM = 6
VARIABLE_COUNT = TEMPLATE_DIM * 256
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
    "global obstruction outside the tested prescribed functional-collision ledger-codesign front",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


pfcoll = load_module("prescribed_functional_collision_realization", PFCOLL_SCRIPT)
lowrank = load_module("lowrank_template_selected_class_search", LOWRANK_SCRIPT)
depeng = load_module("dependency_engineered_rank_feedback", DEPENG_SCRIPT)

feedback = pfcoll.feedback
p456 = pfcoll.p456


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def hash_payload(payload: Any) -> str:
    return lowrank.hash_payload(payload)


def actual_template_specs(max_templates: int) -> list[dict[str, Any]]:
    specs = []
    seen: set[str] = set()

    for order, spec in enumerate(pfcoll.template_specs(max_templates * 2)):
        vectors = [[int(value) % 17 for value in row] for row in spec["vectors"]]
        key = hash_payload(vectors)
        if key in seen:
            continue
        seen.add(key)
        metrics = pfcoll.pairdiff_metrics(vectors)
        specs.append(
            {
                "template_id": f"lcodesign_{len(specs):04d}_{spec['shape_id']}",
                "template_family": f"ledger_codesign_{spec['template_family']}",
                "template_dimension": TEMPLATE_DIM,
                "vectors": vectors,
                "selected_class_sizes": [3, 4, 5, 6],
                "cost_weight": 2.0,
                "pair7_weight": 2.0,
                "assignment_strategies": [
                    "fiber_round_robin",
                    "pair7_block",
                    "fiber_block",
                    "residue_block",
                    "signature_fiber_blocks",
                    "pair7_signature_blocks",
                ],
                "source_template_spec": {key: value for key, value in spec.items() if key != "vectors"},
                "pairdiff_collision_excess": metrics["pairdiff_collision_excess"],
                "pairdiff_collision_groups": metrics["pairdiff_collision_groups"],
            }
        )
        if len(specs) >= max_templates:
            break

    for base in lowrank.TEMPLATE_SPECS:
        if len(base["vectors"][0]) != TEMPLATE_DIM:
            continue
        vectors = [[int(value) % 17 for value in row] for row in base["vectors"]]
        key = hash_payload(vectors)
        if key in seen:
            continue
        seen.add(key)
        metrics = pfcoll.pairdiff_metrics(vectors)
        specs.append(
            {
                "template_id": f"lcodesign_{len(specs):04d}_{base['template_id']}",
                "template_family": f"ledger_codesign_{base['template_family']}",
                "template_dimension": TEMPLATE_DIM,
                "vectors": vectors,
                "selected_class_sizes": [3, 4, 5, 6],
                "cost_weight": 2.0,
                "pair7_weight": 2.0,
                "assignment_strategies": [
                    "fiber_round_robin",
                    "pair7_block",
                    "fiber_block",
                    "residue_block",
                    "signature_fiber_blocks",
                    "pair7_signature_blocks",
                ],
                "source_template_spec": {"source": "lowrank_template_selected_class_search", "template_id": base["template_id"]},
                "pairdiff_collision_excess": metrics["pairdiff_collision_excess"],
                "pairdiff_collision_groups": metrics["pairdiff_collision_groups"],
            }
        )
        if len(specs) >= max_templates:
            break
    return specs[:max_templates]


def assign_codesign_coordinates(profile: dict[str, Any], strategy: str, seed: int) -> list[dict[str, Any]]:
    if strategy in {"signature_fiber_blocks", "pair7_signature_blocks"}:
        return depeng.assign_dependency_coordinates(profile, strategy, seed)
    return lowrank.assign_coordinates(profile["selected_counts"], strategy, seed)


def evaluate_codesign_candidate(profile: dict[str, Any], strategy: str, seed: int) -> dict[str, Any]:
    coordinates = assign_codesign_coordinates(profile, strategy, seed)
    pairs = lowrank.pair_counts(coordinates)
    pair7 = [pairs[label] for label in lowrank.PAIR7_PAIR_LABELS]
    candidate = {
        "template_id": profile["template_id"],
        "template_family": profile["template_family"],
        "template_dimension": profile["template_dimension"],
        "template_vectors": profile["template_vectors"],
        "assignment_strategy": strategy,
        "assignment_seed": seed,
        "support_vector": lowrank.support_counts(coordinates),
        "pair_count_matrix": pairs,
        "max_pair_count": max(pairs.values()),
        "pair7_counts": pair7,
        "selected_class_size_counts": lowrank.size_histogram(coordinates),
        "total_effective_cost": profile["total_effective_cost"],
        "variable_count": profile["variable_count"],
        "cost_margin": profile["variable_count"] - profile["total_effective_cost"],
        "coordinate_classes_hash": hash_payload(coordinates),
        "quotient_fiber_histogram": lowrank.fiber_histogram(coordinates),
        "coordinate_classes": coordinates,
        "selected_count_hash": profile["selected_count_hash"],
        "source_template_spec": profile.get("source_template_spec"),
        "pairdiff_collision_excess": profile.get("pairdiff_collision_excess", 0),
        "pairdiff_collision_groups": profile.get("pairdiff_collision_groups", 0),
    }
    candidate["total_effective_cost"] = pfcoll.fcoll.recompute_total_effective_cost(candidate)
    return candidate


def structural_row(candidate: dict[str, Any], profile: dict[str, Any], system_order: int) -> dict[str, Any]:
    metrics = pfcoll.fcoll.functional_metrics(candidate)
    screen = p456.tchamber.candidate_screen_row(candidate)
    equal_pairs = pfcoll.template_equal_pairs(candidate["template_vectors"])
    status = screen["backward_structural_status"]
    if equal_pairs and status == "TCHAMBER_STRUCTURAL_PASS":
        status = "LCODESIGN_TEMPLATE_EQUAL_PAIR"
    if candidate["support_vector"] != [TARGET_AGREEMENT] * 7:
        status = "LCODESIGN_SUPPORT_FAIL"
    elif candidate["max_pair_count"] > PAIR_CAP or min(candidate["pair7_counts"]) < PAIR7_LOWER:
        status = "LCODESIGN_PAIR_GUARD_FAIL"
    return {
        "system_order": system_order,
        "template_id": candidate["template_id"],
        "template_family": candidate["template_family"],
        "assignment_strategy": candidate["assignment_strategy"],
        "assignment_seed": candidate["assignment_seed"],
        "support_vector": candidate["support_vector"],
        "pair7_counts": candidate["pair7_counts"],
        "max_pair_count": candidate["max_pair_count"],
        "selected_class_size_counts": candidate["selected_class_size_counts"],
        "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        "selected_count_hash": candidate["selected_count_hash"],
        "solver_total_effective_cost": profile["total_effective_cost"],
        "total_effective_cost": candidate["total_effective_cost"],
        "cost_margin": VARIABLE_COUNT - candidate["total_effective_cost"],
        "template_equal_pairs": equal_pairs,
        "structural_status": status,
        "functional_classes": metrics["functional_classes"],
        "functional_span_rank": metrics["functional_span_rank"],
        "forced_functional_identities": metrics["forced_functional_identities"],
        "raw_collision_excess": metrics["raw_collision_excess"],
        "max_functional_support": metrics["max_functional_support"],
        "pairdiff_collision_excess": candidate["pairdiff_collision_excess"],
        "pairdiff_collision_groups": candidate["pairdiff_collision_groups"],
    }


def structural_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    status_priority = 0 if row["structural_status"] == "TCHAMBER_STRUCTURAL_PASS" else 1
    return (
        status_priority,
        -int(row["cost_margin"]),
        -int(row["raw_collision_excess"]),
        int(row["functional_classes"]),
        -int(row["functional_span_rank"]),
        row["template_id"],
        row["assignment_strategy"],
    )


def profile_row(candidate: dict[str, Any], profile: dict[str, Any], candidate_order: int, profile_order: int) -> dict[str, Any]:
    row = pfcoll.profile_row(candidate, profile, candidate_order, profile_order)
    metrics = pfcoll.fcoll.functional_metrics(candidate)
    row.update(
        {
            "functional_classes": metrics["functional_classes"],
            "functional_span_rank": metrics["functional_span_rank"],
            "forced_functional_identities": metrics["forced_functional_identities"],
            "raw_collision_excess": metrics["raw_collision_excess"],
            "max_functional_support": metrics["max_functional_support"],
            "pairdiff_collision_excess": candidate["pairdiff_collision_excess"],
            "pairdiff_collision_groups": candidate["pairdiff_collision_groups"],
            "selected_count_hash": candidate["selected_count_hash"],
            "coordinate_classes_hash": candidate["coordinate_classes_hash"],
        }
    )
    return row


def profile_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    q_shortfall = max(0, Q_VARIABLE_FLOOR - int(row["q_variable_count"]))
    return (
        q_shortfall,
        -int(row["q_variable_count"]),
        int(row["row_minus_col"]),
        -int(row["raw_collision_excess"]),
        int(row["matrix_shape"][0]),
        row["template_id"],
        row["basis_id"],
    )


def proxy_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        -int(row["proxy_nullity"]),
        int(row["proxy_rank"]),
        max(0, Q_VARIABLE_FLOOR - int(row["q_variable_count"])),
        -int(row["q_variable_count"]),
        int(row["row_minus_col"]),
        row["template_id"],
        row["basis_id"],
    )


def build_record(max_templates: int, max_systems: int, profile_candidate_limit: int, basis_profiles_per_candidate: int, profile_rank_limit: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    specs = actual_template_specs(max_templates)
    solved_profiles = []
    for spec in specs:
        solved = lowrank.solve_template_counts(spec)
        if solved.get("solver_status") == "OPTIMAL_OR_FEASIBLE":
            solved["source_template_spec"] = spec["source_template_spec"]
            solved["pairdiff_collision_excess"] = spec["pairdiff_collision_excess"]
            solved["pairdiff_collision_groups"] = spec["pairdiff_collision_groups"]
            solved_profiles.append(solved)

    candidates: list[tuple[dict[str, Any], dict[str, Any]]] = []
    structural_rows = []
    system_order = 0
    for profile_order, profile in enumerate(solved_profiles):
        for strategy_order, strategy in enumerate(profile["assignment_strategies"]):
            if system_order >= max_systems:
                break
            candidate = evaluate_codesign_candidate(profile, strategy, seed=73100 + 37 * profile_order + strategy_order)
            row = structural_row(candidate, profile, system_order)
            structural_rows.append(row)
            if row["structural_status"] == "TCHAMBER_STRUCTURAL_PASS":
                candidates.append((candidate, row))
            system_order += 1
        if system_order >= max_systems:
            break

    profile_rows = []
    source_profiles: dict[tuple[int, str], tuple[dict[str, Any], dict[str, Any]]] = {}
    for candidate_order, (candidate, row) in enumerate(sorted(candidates, key=lambda item: structural_sort_key(item[1]))[:profile_candidate_limit]):
        for profile_order, profile in enumerate(
            p456.tchamber.basis_profiles(
                candidate,
                top_classes=32,
                random_bases=128,
                limit=basis_profiles_per_candidate,
            )
        ):
            out = profile_row(candidate, profile, candidate_order, profile_order)
            out["source_system_order"] = row["system_order"]
            out["profile_candidate_order"] = candidate_order
            profile_rows.append(out)
            source_profiles[(candidate_order, out["basis_id"])] = (candidate, profile)

    h_values = pfcoll.feedback.proxy_h_values(PROXY_PRIME)
    powers = pfcoll.feedback.precompute_powers_mod(h_values, PROXY_PRIME)
    ranked_targets = sorted(profile_rows, key=profile_sort_key)[:profile_rank_limit]
    proxy_rows = []
    for target in ranked_targets:
        candidate, profile = source_profiles[(int(target["profile_candidate_order"]), target["basis_id"])]
        proxy = pfcoll.feedback.proxy_basis_quotient_rank(candidate, profile, h_values, powers, PROXY_PRIME)
        q_budget_ok = int(target["q_variable_count"]) >= Q_VARIABLE_FLOOR
        proxy_rows.append(
            {
                **target,
                "q_variable_floor": Q_VARIABLE_FLOOR,
                "q_variable_budget_ok": q_budget_ok,
                "proxy_prime": proxy["proxy_prime"],
                "proxy_matrix_shape": proxy["matrix_shape"],
                "proxy_rank": proxy["proxy_rank"],
                "proxy_nullity": proxy["proxy_nullity"],
                "best_failure_mode": (
                    "LCODESIGN_PROXY_POSITIVE"
                    if int(proxy["proxy_nullity"]) > 0
                    else "LCODESIGN_PROXY_FULL_RANK"
                ),
                "chamber_sampled": False,
                "exact_pairclear_rank_slack_chamber": None,
            }
        )

    positives = [row for row in proxy_rows if int(row["proxy_nullity"]) > 0]
    best = min(proxy_rows, key=proxy_sort_key) if proxy_rows else None
    best_candidate = None
    if best is not None:
        candidate, _profile = source_profiles[(int(best["profile_candidate_order"]), best["basis_id"])]
        best_candidate = {
            **pfcoll.feedback.compact_candidate(candidate),
            "coordinate_classes": candidate["coordinate_classes"],
            "template_vectors": candidate["template_vectors"],
            "selected_count_hash": candidate["selected_count_hash"],
            "selected_class_size_counts": candidate["selected_class_size_counts"],
            "total_effective_cost": candidate["total_effective_cost"],
        }

    failure = "LCODESIGN_NO_STRUCTURAL_PASS"
    proof_status = "EXACT_EXTRACTION_NO_A327 / LCODESIGN_NO_STRUCTURAL_PASS / PARTIAL / EXPERIMENTAL"
    if proxy_rows:
        failure = "LCODESIGN_PROXY_POSITIVE" if positives else "LCODESIGN_PROXY_FULL_RANK"
        proof_status = (
            "CANDIDATE / LCODESIGN_PROXY_POSITIVE / PARTIAL / EXPERIMENTAL"
            if positives
            else "EXACT_EXTRACTION_NO_A327 / LCODESIGN_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL"
        )

    best_structural = min(structural_rows, key=structural_sort_key) if structural_rows else None
    status_counts = Counter(row["structural_status"] for row in structural_rows)
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_prescribed_functional_collision_realization": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "templates_tested": previous["prescribed_functional_collision_realization"]["templates_tested"],
            "prescribed_collision_realized_templates": previous["prescribed_functional_collision_realization"]["prescribed_collision_realized_templates"],
            "best_proxy_rank": previous["prescribed_functional_collision_realization"]["best_proxy_rank"],
            "best_proxy_nullity": previous["prescribed_functional_collision_realization"]["best_proxy_nullity"],
            "best_q_variable_count": previous["best_profile"]["q_variable_count"],
            "failure_mode": previous["prescribed_functional_collision_realization"]["best_failure_mode"],
        },
        "prescribed_functional_collision_ledger_codesign": {
            "proxy_prime": PROXY_PRIME,
            "q_variable_floor": Q_VARIABLE_FLOOR,
            "max_templates": max_templates,
            "max_systems": max_systems,
            "profile_candidate_limit": profile_candidate_limit,
            "basis_profiles_per_candidate": basis_profiles_per_candidate,
            "profile_rank_limit": profile_rank_limit,
            "template_specs_tested": len(specs),
            "milp_feasible_templates": len(solved_profiles),
            "systems_tested": len(structural_rows),
            "structural_pass_systems": len(candidates),
            "system_status_counts": dict(status_counts),
            "basis_profiles_constructed": len(profile_rows),
            "q_budget_profiles": sum(1 for row in profile_rows if int(row["q_variable_count"]) >= Q_VARIABLE_FLOOR),
            "proxy_ranked_profiles": len(proxy_rows),
            "proxy_positive_profiles": len(positives),
            "best_structural_cost_margin": None if best_structural is None else best_structural["cost_margin"],
            "best_structural_functional_classes": None if best_structural is None else best_structural["functional_classes"],
            "best_proxy_rank": None if best is None else best["proxy_rank"],
            "best_proxy_nullity": None if best is None else best["proxy_nullity"],
            "best_q_variable_count": None if best is None else best["q_variable_count"],
            "best_failure_mode": failure,
            "profile_failure_counts": dict(Counter(row["best_failure_mode"] for row in proxy_rows)),
        },
        "best_structural_system": best_structural,
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
    parser.add_argument("--max-templates", type=int, default=96)
    parser.add_argument("--max-systems", type=int, default=192)
    parser.add_argument("--profile-candidate-limit", type=int, default=32)
    parser.add_argument("--basis-profiles-per-candidate", type=int, default=3)
    parser.add_argument("--profile-rank-limit", type=int, default=10)
    args = parser.parse_args()
    record = build_record(
        max_templates=args.max_templates,
        max_systems=args.max_systems,
        profile_candidate_limit=args.profile_candidate_limit,
        basis_profiles_per_candidate=args.basis_profiles_per_candidate,
        profile_rank_limit=args.profile_rank_limit,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["prescribed_functional_collision_ledger_codesign"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "template_specs_tested": search["template_specs_tested"],
                    "milp_feasible_templates": search["milp_feasible_templates"],
                    "systems_tested": search["systems_tested"],
                    "structural_pass_systems": search["structural_pass_systems"],
                    "basis_profiles_constructed": search["basis_profiles_constructed"],
                    "q_budget_profiles": search["q_budget_profiles"],
                    "proxy_ranked_profiles": search["proxy_ranked_profiles"],
                    "proxy_positive_profiles": search["proxy_positive_profiles"],
                    "best_q_variable_count": search["best_q_variable_count"],
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
        print("M1_A327_PRESCRIBED_FUNCTIONAL_COLLISION_LEDGER_CODESIGN_READY")


if __name__ == "__main__":
    main()
