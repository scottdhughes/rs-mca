#!/usr/bin/env python3
"""Perturb the selected-count ledger around the realized-slot near miss."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import sympy as sp


SOURCE_COMMIT = "8a15096"
PREVIOUS_DATA = Path("experimental/data/m1_a327_residual_slot_equation_repair.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_realization_aware_ledger_perturbation.json")

ROOT = Path(__file__).resolve().parents[2]
NREPAIR_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_realized_slot_nearmiss_repair.py"

P = 17
TARGET_AGREEMENT = 327
PAIR_CAP = 255
PAIR7_LOWER = 142
TEMPLATE_DIM = 6


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


nrepair = load_module("realized_slot_nearmiss_repair", NREPAIR_SCRIPT)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def mask_contains(mask: int, witness: int) -> int:
    return 1 if mask & (1 << (witness - 1)) else 0


def pair_same(mask: int, left: int, right: int) -> int:
    return mask_contains(mask, left) * mask_contains(mask, right)


def count_kernel_basis(selected_counts: list[dict[str, Any]]) -> list[list[int]]:
    masks = [int(row["mask"]) for row in selected_counts]
    rows = [[1] * len(masks)]
    for witness in range(1, 8):
        rows.append([mask_contains(mask, witness) for mask in masks])
    kernel = sp.Matrix(rows).nullspace()
    basis = []
    for vector in kernel:
        denominator = sp.ilcm(*[entry.q for entry in vector])
        ints = [int(entry * denominator) for entry in vector]
        gcd = 0
        for value in ints:
            gcd = math.gcd(gcd, abs(value))
        basis.append([value // gcd for value in ints])
    return basis


def selected_count_summary(selected_counts: list[dict[str, Any]]) -> dict[str, Any]:
    masks = [int(row["mask"]) for row in selected_counts]
    counts = [int(row["count"]) for row in selected_counts]
    supports = [
        sum(count * mask_contains(mask, witness) for mask, count in zip(masks, counts, strict=True))
        for witness in range(1, 8)
    ]
    pair_counts = {}
    pair7 = []
    for left in range(1, 8):
        for right in range(left + 1, 8):
            value = sum(count * pair_same(mask, left, right) for mask, count in zip(masks, counts, strict=True))
            label = f"P{left}{right}"
            pair_counts[label] = value
            if right == 7 and left <= 5:
                pair7.append(value)
    return {
        "coordinate_count": sum(counts),
        "support_vector": supports,
        "pair_count_matrix": pair_counts,
        "pair7_counts": pair7,
        "max_pair_count": max(pair_counts.values()),
        "selected_class_size_counts": dict(Counter(str(mask.bit_count()) for mask, count in zip(masks, counts, strict=True) for _ in range(count))),
    }


def near_miss_profile() -> dict[str, Any]:
    base = nrepair.near_miss_base_profile()
    vectors = [[int(value) % P for value in row] for row in base["template_vectors"]]
    vectors[6][1] = 9
    return {
        **base,
        "template_id": "ledgerpert_w7_c1_v9_base",
        "template_family": "single_outside_w7_v3_ledger_perturbation",
        "template_vectors": vectors,
        "mutation_id": "w7_c1_v9",
        "base_template_id": base["template_id"],
    }


def with_counts(base_profile: dict[str, Any], counts: list[int], perturbation_id: str, coeffs: list[int]) -> dict[str, Any]:
    selected_counts = []
    for source, count in zip(base_profile["selected_counts"], counts, strict=True):
        if count <= 0:
            continue
        selected_counts.append(
            {
                "mask": int(source["mask"]),
                "members": source["members"],
                "size": int(source["size"]),
                "affine_rank_cost": nrepair.rank_cost_for_mask(base_profile["template_vectors"], int(source["mask"])),
                "count": int(count),
            }
        )
    return {
        **base_profile,
        "template_id": f"ledgerpert_{perturbation_id}",
        "selected_counts": selected_counts,
        "selected_count_hash": nrepair.joint.hash_payload(selected_counts),
        "total_effective_cost": nrepair.total_effective_cost(base_profile["template_vectors"], selected_counts),
        "variable_count": TEMPLATE_DIM * 256,
        "perturbation_id": perturbation_id,
        "kernel_coefficients": coeffs,
    }


def perturbation_profiles(max_abs_coeff: int, max_profiles: int) -> tuple[list[list[int]], list[dict[str, Any]]]:
    base = near_miss_profile()
    base_counts = [int(row["count"]) for row in base["selected_counts"]]
    basis = count_kernel_basis(base["selected_counts"])
    profiles = []
    seen: set[tuple[int, ...]] = set()
    coefficient_vectors = list(itertools.product(range(-max_abs_coeff, max_abs_coeff + 1), repeat=len(basis)))
    coefficient_vectors.sort(key=lambda coeffs: (sum(abs(value) for value in coeffs), coeffs))
    for coeffs_tuple in coefficient_vectors:
        coeffs = [int(value) for value in coeffs_tuple]
        if not any(coeffs):
            perturbation_id = "base"
        else:
            perturbation_id = "k_" + "_".join(str(value).replace("-", "m") for value in coeffs)
        counts = base_counts[:]
        for scale, direction in zip(coeffs, basis, strict=True):
            for idx, value in enumerate(direction):
                counts[idx] += scale * value
        key = tuple(counts)
        if key in seen or any(value < 0 for value in counts):
            continue
        seen.add(key)
        profile = with_counts(base, counts, perturbation_id, coeffs)
        summary = selected_count_summary(profile["selected_counts"])
        if summary["coordinate_count"] != 512 or summary["support_vector"] != [TARGET_AGREEMENT] * 7:
            continue
        if summary["max_pair_count"] > PAIR_CAP or min(summary["pair7_counts"]) < PAIR7_LOWER:
            continue
        profile["count_summary"] = summary
        profiles.append(profile)
        if len(profiles) >= max_profiles:
            break
    return basis, profiles


def analyze_profile(profile: dict[str, Any], stable_basis_limit: int, run_proxy: bool) -> list[dict[str, Any]]:
    strategies = [
        "signature_fiber_blocks",
        "signature_residue_blocks",
        "pair7_signature_blocks",
        "dependency_twin_interleave",
        "fiber_factor_packed",
        "seeded_dependency_shuffle",
    ]
    rows = []
    for strategy_index, strategy in enumerate(strategies):
        candidate = nrepair.dependency.evaluate_dependency_candidate(
            profile,
            strategy,
            seed=81000 + 101 * len(rows) + 17 * strategy_index,
        )
        candidate["perturbation_id"] = profile["perturbation_id"]
        candidate["kernel_coefficients"] = profile["kernel_coefficients"]
        row = nrepair.analyze_candidate(candidate, stable_basis_limit=stable_basis_limit, run_proxy=run_proxy)
        row["perturbation_id"] = profile["perturbation_id"]
        row["kernel_coefficients"] = profile["kernel_coefficients"]
        row["count_summary"] = profile["count_summary"]
        rows.append(row)
    return rows


def candidate_summary(row: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "template_id",
        "template_family",
        "perturbation_id",
        "kernel_coefficients",
        "assignment_strategy",
        "assignment_seed",
        "support_vector",
        "pair7_counts",
        "max_pair_count",
        "selected_class_size_counts",
        "coordinate_classes_hash",
        "functional_classes",
        "functional_span_rank",
        "forced_functional_identities",
        "structural_status",
        "stable_basis_combinations",
        "stable_basis_profiles_tested",
        "slot_profiles_tested",
        "actual_zero_slot_profiles",
        "pair_projection_clear_actual_slots",
        "proxy_positive_actual_slots",
        "effective_cost",
        "best_failure_mode",
        "best_profile",
    ]
    return {key: row.get(key) for key in keys}


def build_record(max_abs_coeff: int, max_profiles: int, stable_basis_limit: int, run_proxy: bool) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    kernel_basis, profiles = perturbation_profiles(max_abs_coeff=max_abs_coeff, max_profiles=max_profiles)
    rows = []
    for profile in profiles:
        rows.extend(analyze_profile(profile, stable_basis_limit=stable_basis_limit, run_proxy=run_proxy))

    proxy_positive = [row for row in rows if row["proxy_positive_actual_slots"] > 0]
    zero_slots = [row for row in rows if row["actual_zero_slot_profiles"] > 0]
    if proxy_positive:
        best = max(proxy_positive, key=lambda row: row["best_profile"]["proxy_result"]["proxy_nullity"])
        proof_status = "CANDIDATE / LEDGERPERT_PROXY_NULLITY_POSITIVE / PARTIAL / EXPERIMENTAL"
        failure = "LEDGERPERT_PROXY_NULLITY_POSITIVE"
    elif zero_slots:
        best = max(zero_slots, key=lambda row: row["pair_projection_clear_actual_slots"])
        proof_status = "CANDIDATE / LEDGERPERT_ACTUAL_ZERO_SLOT / PARTIAL / EXPERIMENTAL"
        failure = "LEDGERPERT_ACTUAL_ZERO_SLOT"
    elif rows:
        best = min(
            rows,
            key=lambda row: (
                row["best_profile"]["slot_nonzero_rows"] if row["best_profile"] else 999,
                row["best_profile"]["forced_pair_count"] if row["best_profile"] else 999,
                row["effective_cost"],
            ),
        )
        proof_status = "EXACT_EXTRACTION_NO_A327 / LEDGERPERT_SLOT_NOT_KERNEL / PARTIAL / EXPERIMENTAL"
        failure = "LEDGERPERT_SLOT_NOT_KERNEL"
    else:
        best = None
        proof_status = "EXACT_EXTRACTION_NO_A327 / LEDGERPERT_NO_FEASIBLE_LEDGER / PARTIAL / EXPERIMENTAL"
        failure = "LEDGERPERT_NO_FEASIBLE_LEDGER"

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": SOURCE_COMMIT,
        "previous_residual_slot_repair": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_failure_mode": previous["residual_slot_equations"]["best_failure_mode"],
            "actual_zero_slot_profiles": previous["exhaustive_stable_profile_audit"]["actual_zero_slot_profiles"],
        },
        "ledger_perturbation_search": {
            "kernel_basis": kernel_basis,
            "max_abs_coeff": max_abs_coeff,
            "ledger_profiles_tested": len(profiles),
            "systems_tested": len(rows),
            "structural_pass_candidates": sum(1 for row in rows if row["structural_status"] == "JOINT_TEMPLATE_STRUCTURAL_PASS"),
            "stable_basis_combinations": sum(row["stable_basis_combinations"] for row in rows),
            "stable_basis_profiles_tested": sum(row["stable_basis_profiles_tested"] for row in rows),
            "slot_profiles_tested": sum(row["slot_profiles_tested"] for row in rows),
            "actual_zero_slot_profiles": sum(row["actual_zero_slot_profiles"] for row in rows),
            "pair_projection_clear_actual_slots": sum(row["pair_projection_clear_actual_slots"] for row in rows),
            "proxy_positive_actual_slots": sum(row["proxy_positive_actual_slots"] for row in rows),
            "best_template_id": None if best is None else best["template_id"],
            "best_perturbation_id": None if best is None else best["perturbation_id"],
            "best_kernel_coefficients": None if best is None else best["kernel_coefficients"],
            "best_assignment_strategy": None if best is None else best["assignment_strategy"],
            "best_slot_nonzero_rows": None if best is None or best["best_profile"] is None else best["best_profile"]["slot_nonzero_rows"],
            "best_forced_pair_count": None if best is None or best["best_profile"] is None else best["best_profile"]["forced_pair_count"],
            "best_failure_mode": failure,
            "failure_counts": dict(Counter(row["best_failure_mode"] for row in rows)),
            "screen_counts": dict(Counter(row["structural_status"] for row in rows)),
            "candidate_summaries": [candidate_summary(row) for row in rows],
        },
        "best_candidate": None if best is None else candidate_summary(best),
        "realization_status": "ACTUAL_TEMPLATE_ROWSPACES_ONLY",
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
            "synthetic rowspace edits",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--max-abs-coeff", type=int, default=6)
    parser.add_argument("--max-profiles", type=int, default=96)
    parser.add_argument("--stable-basis-limit", type=int, default=96)
    parser.add_argument("--run-proxy", action="store_true")
    args = parser.parse_args()
    record = build_record(
        max_abs_coeff=args.max_abs_coeff,
        max_profiles=args.max_profiles,
        stable_basis_limit=args.stable_basis_limit,
        run_proxy=args.run_proxy,
    )
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["ledger_perturbation_search"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "ledger_profiles_tested": search["ledger_profiles_tested"],
                    "systems_tested": search["systems_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "actual_zero_slot_profiles": search["actual_zero_slot_profiles"],
                    "pair_projection_clear_actual_slots": search["pair_projection_clear_actual_slots"],
                    "proxy_positive_actual_slots": search["proxy_positive_actual_slots"],
                    "best_perturbation_id": search["best_perturbation_id"],
                    "best_kernel_coefficients": search["best_kernel_coefficients"],
                    "best_assignment_strategy": search["best_assignment_strategy"],
                    "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_failure_mode": search["best_failure_mode"],
                    "failure_counts": search["failure_counts"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_REALIZATION_AWARE_LEDGER_PERTURBATION_READY")


if __name__ == "__main__":
    main()
