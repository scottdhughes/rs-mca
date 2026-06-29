#!/usr/bin/env python3
"""Descriptor generator for the M1 a=327 random low-degree witness search.

The exact finite-field evaluation is done by the matching Sage audit.  This
dependency-free scanner records the deterministic candidate tuple families,
their seeds, and the status boundary for the first constructive search layer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


OUTPUT_DATA = Path("experimental/data/m1_a327_random_lowdegree_list_witness_search.json")

P = 17
FIELD_DEGREE = 32
N = 512
K = 256
LIST_SIZE = 7
TARGET_AGREEMENT = 327


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def lcg(seed: int) -> int:
    return (6364136223846793005 * seed + 1442695040888963407) & ((1 << 64) - 1)


def deterministic_sample(seed: int, universe_size: int, count: int) -> list[int]:
    if count > universe_size:
        raise ValueError("sample count exceeds universe size")
    values: list[int] = []
    seen: set[int] = set()
    state = seed & ((1 << 64) - 1)
    while len(values) < count:
        state = lcg(state)
        candidate = state % universe_size
        if candidate not in seen:
            seen.add(candidate)
            values.append(candidate)
    return values


def sparse_terms(seed: int, terms: int, max_degree: int) -> list[dict[str, int]]:
    degrees = deterministic_sample(seed ^ 0xA32751, max_degree + 1, terms)
    out: list[dict[str, int]] = []
    state = seed ^ 0xC0FFEE
    for degree in sorted(degrees):
        state = lcg(state)
        coeff = int(state % (P - 1)) + 1
        out.append({"degree": degree, "coeff_mod_17": coeff})
    return out


def random_sparse_descriptors() -> list[dict[str, Any]]:
    descriptors = []
    for tuple_index in range(24):
        seed = 0xA3270000 + tuple_index
        witnesses = []
        for witness in range(LIST_SIZE):
            witnesses.append(
                {
                    "witness": witness,
                    "terms": sparse_terms(seed + 97 * witness, terms=7, max_degree=K - 1),
                }
            )
        descriptors.append(
            {
                "candidate_id": f"random_sparse_subfield_{tuple_index:02d}",
                "family": "random_sparse_subfield",
                "seed": seed,
                "description": "Seven sparse degree<256 polynomials with GF(17) coefficients.",
                "witnesses": witnesses,
            }
        )
    return descriptors


def common_root_core_descriptors() -> list[dict[str, Any]]:
    descriptors = []
    root_sizes = [192, 224, 240, 248, 255]
    for root_size in root_sizes:
        residual_degree_bound = K - 1 - root_size
        for variant in range(6):
            seed = 0xBEEF0000 + 1000 * root_size + variant
            descriptors.append(
                {
                    "candidate_id": f"common_root_core_r{root_size}_{variant:02d}",
                    "family": "common_root_core",
                    "seed": seed,
                    "root_size": root_size,
                    "root_positions": deterministic_sample(seed, N, root_size),
                    "residual_degree_bound": residual_degree_bound,
                    "description": (
                        "Seven codewords share a common root-core locator and "
                        "use distinct low-degree residual factors."
                    ),
                    "residuals": [
                        sparse_terms(seed + 131 * witness, terms=min(5, residual_degree_bound + 1), max_degree=residual_degree_bound)
                        for witness in range(LIST_SIZE)
                    ],
                }
            )
    return descriptors


def monomial_orbit_descriptors() -> list[dict[str, Any]]:
    descriptors = []
    degrees = [1, 2, 3, 4, 8, 16, 32, 64, 128, 192, 255]
    for degree in degrees:
        for variant in range(4):
            seed = 0xD00D0000 + 1000 * degree + variant
            scale_seed = seed ^ 0x123456
            shift_seed = seed ^ 0x654321
            scales = []
            shifts = []
            state = scale_seed
            for witness in range(LIST_SIZE):
                state = lcg(state)
                scales.append(int(state % (P - 1)) + 1)
            state = shift_seed
            for witness in range(LIST_SIZE):
                state = lcg(state)
                shifts.append(int(state % P))
            descriptors.append(
                {
                    "candidate_id": f"monomial_orbit_d{degree}_{variant:02d}",
                    "family": "monomial_orbit",
                    "seed": seed,
                    "degree": degree,
                    "scales_mod_17": scales,
                    "shifts_mod_17": shifts,
                    "description": "Seven affine monomial codewords a_i X^d + b_i.",
                }
            )
    return descriptors


def clustered_root_core_descriptors() -> list[dict[str, Any]]:
    descriptors = []
    for variant in range(18):
        seed = 0xCAFE0000 + variant
        common_size = [160, 176, 192][variant % 3]
        residual_degree_bound = K - 1 - common_size
        descriptors.append(
            {
                "candidate_id": f"clustered_root_core_{variant:02d}",
                "family": "clustered_root_core",
                "seed": seed,
                "common_root_size": common_size,
                "common_root_positions": deterministic_sample(seed, N, common_size),
                "cluster_sizes": [4, 3],
                "residual_degree_bound": residual_degree_bound,
                "description": (
                    "Seven codewords share a common root core and split into "
                    "two residual clusters outside it."
                ),
                "cluster_residuals": [
                    sparse_terms(seed + 17, terms=min(5, residual_degree_bound + 1), max_degree=residual_degree_bound),
                    sparse_terms(seed + 43, terms=min(5, residual_degree_bound + 1), max_degree=residual_degree_bound),
                ],
                "witness_noise": [
                    sparse_terms(seed + 211 * witness, terms=min(3, residual_degree_bound + 1), max_degree=residual_degree_bound)
                    for witness in range(LIST_SIZE)
                ],
            }
        )
    return descriptors


def candidate_descriptors() -> list[dict[str, Any]]:
    candidates = []
    candidates.extend(random_sparse_descriptors())
    candidates.extend(common_root_core_descriptors())
    candidates.extend(monomial_orbit_descriptors())
    candidates.extend(clustered_root_core_descriptors())
    return candidates


def build_record(exact_results: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    candidates = candidate_descriptors()
    best = None
    status = "PARTIAL"
    if exact_results is not None:
        if len(exact_results) != len(candidates):
            raise ValueError("exact result count does not match descriptor count")
        best = max(exact_results, key=lambda row: row["capacity_upper_bound"])
        status = (
            "CANDIDATE"
            if best["capacity_upper_bound"] >= TARGET_AGREEMENT
            else "TESTED_TUPLES_NO_A327"
        )

    return {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "construction_mode": "random_lowdegree_list_witness_search",
        "candidate_families": {
            family: sum(1 for item in candidates if item["family"] == family)
            for family in sorted({item["family"] for item in candidates})
        },
        "candidate_count": len(candidates),
        "candidate_descriptor_hash": hash_payload(candidates),
        "exact_evaluation": {
            "status": "SAGE_EVALUATED" if exact_results is not None else "NOT_RUN",
            "result_count": 0 if exact_results is None else len(exact_results),
            "best": best,
            "results": [] if exact_results is None else exact_results,
        },
        "proof_status": status,
        "mca_counted": False,
        "not_claimed": [
            "MCA N_bad",
            "protocol soundness",
            "ordinary list decoding beyond the stated interleaved-list predicate",
            "a=327 interleaved-list certificate",
            "global Lambda_mu(C,327) <= 6",
            "exact Lambda_mu",
            "exact delta*_C",
            "improvement over PR #133",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print JSON record")
    parser.add_argument("--write", action="store_true", help=f"write {OUTPUT_DATA}")
    args = parser.parse_args()

    record = build_record()
    if args.write:
        OUTPUT_DATA.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_DATA.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    if args.json or not args.write:
        print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
