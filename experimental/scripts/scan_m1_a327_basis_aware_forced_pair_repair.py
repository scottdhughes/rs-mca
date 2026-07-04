#!/usr/bin/env python3
"""Target the remaining basis-aware forced pairs for M1 a=327."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


SOURCE_COMMIT = "37d9718"
PREVIOUS_DATA = Path("experimental/data/m1_a327_basis_aware_pairclear_kernel_synthesis.json")
OUTPUT_DATA = Path("experimental/data/m1_a327_basis_aware_forced_pair_repair.json")

ROOT = Path(__file__).resolve().parents[2]
BASIS_AWARE_SCRIPT = ROOT / "experimental/scripts/scan_m1_a327_basis_aware_pairclear_kernel_synthesis.py"

TARGET_FORCED_PAIRS = ["P12", "P17", "P27", "P46"]
DEFAULT_TOP_CLASSES = 32
DEFAULT_RANDOM_BASES = 1024


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


basisaware = load_module("basis_aware_pairclear_kernel_synthesis", BASIS_AWARE_SCRIPT)


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        return json.load(handle)


def forced_pair_delta(previous_pairs: list[str], current_pairs: list[str]) -> dict[str, Any]:
    previous_set = set(previous_pairs)
    current_set = set(current_pairs)
    target_set = set(TARGET_FORCED_PAIRS)
    return {
        "target_forced_pairs": TARGET_FORCED_PAIRS,
        "previous_forced_pairs": previous_pairs,
        "current_forced_pairs": current_pairs,
        "target_pairs_repaired": sorted(target_set - current_set),
        "target_pairs_remaining": sorted(target_set & current_set),
        "new_forced_pairs_introduced": sorted(current_set - target_set),
        "forced_pair_count_delta": len(current_set) - len(previous_set),
    }


def build_record(top_classes: int, random_bases: int) -> dict[str, Any]:
    previous = load_json(PREVIOUS_DATA)
    expanded = basisaware.build_record(top_classes=top_classes, random_bases=random_bases)
    previous_profile = previous["best_candidate"]["best_profile"]
    current_profile = expanded["best_candidate"]["best_profile"]
    delta = forced_pair_delta(previous_profile["forced_pairs"], current_profile["forced_pairs"])

    if current_profile["forced_pair_count"] == 0:
        proof_status = "CANDIDATE / BAFPAIR_PAIR_CLEAR_SLOT / PARTIAL / EXPERIMENTAL"
        failure = "BAFPAIR_PAIR_CLEAR_SLOT"
    elif current_profile["forced_pair_count"] < previous_profile["forced_pair_count"]:
        proof_status = "EXACT_EXTRACTION_NO_A327 / BAFPAIR_PARTIAL_FORCED_PAIR_REPAIR / PARTIAL / EXPERIMENTAL"
        failure = "BAFPAIR_PARTIAL_FORCED_PAIR_REPAIR"
    else:
        proof_status = "EXACT_EXTRACTION_NO_A327 / BAFPAIR_NO_FORCED_PAIR_IMPROVEMENT / PARTIAL / EXPERIMENTAL"
        failure = "BAFPAIR_NO_FORCED_PAIR_IMPROVEMENT"

    search = expanded["basis_aware_pairclear_synthesis"]
    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": 327,
        "source_commit": SOURCE_COMMIT,
        "previous_basis_aware_pairclear": {
            "commit": SOURCE_COMMIT,
            "proof_status": previous["proof_status"],
            "best_forced_pair_count": previous_profile["forced_pair_count"],
            "best_forced_pairs": previous_profile["forced_pairs"],
            "best_failure_mode": previous["basis_aware_pairclear_synthesis"]["best_failure_mode"],
        },
        "forced_pair_repair": {
            "top_classes": top_classes,
            "random_bases": random_bases,
            "systems_tested": search["systems_tested"],
            "structural_pass_candidates": search["structural_pass_candidates"],
            "basis_profiles_tested": search["basis_profiles_tested"],
            "slot_profiles_tested": search["slot_profiles_tested"],
            "pair_clear_slot_profiles": search["pair_clear_slot_profiles"],
            "pair_clear_slot_kernel_profiles": search["pair_clear_slot_kernel_profiles"],
            "best_template_id": search["best_template_id"],
            "best_assignment_strategy": search["best_assignment_strategy"],
            "best_forced_pair_count": current_profile["forced_pair_count"],
            "best_slot_nonzero_rows": current_profile["slot_nonzero_rows"],
            "best_failure_mode": failure,
            **delta,
            "failure_counts": search["failure_counts"],
            "screen_counts": search["screen_counts"],
            "candidate_summaries": search["candidate_summaries"],
        },
        "best_candidate": expanded["best_candidate"],
        "realization_status": "BASIS_AWARE_FORCED_PAIR_REPAIR",
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
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--top-classes", type=int, default=DEFAULT_TOP_CLASSES)
    parser.add_argument("--random-bases", type=int, default=DEFAULT_RANDOM_BASES)
    args = parser.parse_args()
    record = build_record(top_classes=args.top_classes, random_bases=args.random_bases)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json:
        search = record["forced_pair_repair"]
        print(
            json.dumps(
                {
                    "proof_status": record["proof_status"],
                    "systems_tested": search["systems_tested"],
                    "basis_profiles_tested": search["basis_profiles_tested"],
                    "slot_profiles_tested": search["slot_profiles_tested"],
                    "previous_forced_pairs": search["previous_forced_pairs"],
                    "current_forced_pairs": search["current_forced_pairs"],
                    "target_pairs_repaired": search["target_pairs_repaired"],
                    "target_pairs_remaining": search["target_pairs_remaining"],
                    "new_forced_pairs_introduced": search["new_forced_pairs_introduced"],
                    "best_forced_pair_count": search["best_forced_pair_count"],
                    "best_slot_nonzero_rows": search["best_slot_nonzero_rows"],
                    "best_failure_mode": search["best_failure_mode"],
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif not args.write:
        print("M1_A327_BASIS_AWARE_FORCED_PAIR_REPAIR_READY")


if __name__ == "__main__":
    main()
