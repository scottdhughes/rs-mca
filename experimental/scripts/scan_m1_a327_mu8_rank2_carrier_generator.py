#!/usr/bin/env python3
"""Generate deterministic rank-2 mu_8 carrier planes for exact Sage audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path
from typing import Iterable


OUTPUT_DATA = Path("experimental/data/m1_a327_mu8_rank2_carrier_menu_scan.json")
SCHEDULE_OUTPUT = Path("experimental/data/m1_a327_mu8_rank2_carrier_schedule_candidates.json")

MODULUS = 17
ZETA = 2  # order 8 in GF(17)
RESIDUES = list(range(1, 8))
LABELS = list(range(7))
TARGET_AGREEMENT = 327

NOT_CLAIMED = [
    "MCA N_bad",
    "protocol soundness",
    "ordinary list decoding beyond stated interleaved-list predicate",
    "global Lambda_mu(C,327) <= 6",
    "exact Lambda_mu",
    "exact delta*_C",
]


def mod(value: int) -> int:
    return value % MODULUS


def inv(value: int) -> int:
    return pow(value % MODULUS, MODULUS - 2, MODULUS)


def normalize_vector(vector: Iterable[int]) -> tuple[int, ...]:
    values = [mod(value) for value in vector]
    for value in values:
        if value:
            scale = inv(value)
            return tuple(mod(scale * item) for item in values)
    return tuple(values)


def rref_key(rows: list[list[int]]) -> tuple[tuple[int, ...], ...]:
    matrix = [[mod(value) for value in row] for row in rows if any(mod(value) for value in row)]
    if not matrix:
        return tuple()
    r = 0
    pivots = []
    for c in range(len(matrix[0])):
        pivot = None
        for i in range(r, len(matrix)):
            if matrix[i][c]:
                pivot = i
                break
        if pivot is None:
            continue
        matrix[r], matrix[pivot] = matrix[pivot], matrix[r]
        scale = inv(matrix[r][c])
        matrix[r] = [mod(scale * value) for value in matrix[r]]
        for i in range(len(matrix)):
            if i != r and matrix[i][c]:
                factor = matrix[i][c]
                matrix[i] = [mod(matrix[i][j] - factor * matrix[r][j]) for j in range(len(matrix[i]))]
        pivots.append(c)
        r += 1
        if r == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:r])


def rank(rows: list[list[int]]) -> int:
    return len(rref_key(rows))


def hash_payload(payload: object) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def phase_power(base: int, exp: int) -> int:
    return pow(base % MODULUS, exp, MODULUS)


def vector_library() -> list[dict]:
    vectors: list[dict] = []

    def add(name: str, vector: Iterable[int], family: str) -> None:
        normalized = normalize_vector(vector)
        if any(normalized):
            vectors.append({"name": name, "family": family, "vector": list(normalized)})

    for idx in range(7):
        add(f"e{idx + 1}", [1 if j == idx else 0 for j in range(7)], "standard")
    add("all_ones", [1] * 7, "low_weight")
    add("odd_residues", [1 if residue % 2 else 0 for residue in RESIDUES], "residue_pattern")
    add("even_residues", [1 if residue % 2 == 0 else 0 for residue in RESIDUES], "residue_pattern")
    add("low_half", [1 if residue <= 4 else 0 for residue in RESIDUES], "residue_pattern")
    add("high_half", [1 if residue >= 4 else 0 for residue in RESIDUES], "residue_pattern")
    for shift in range(8):
        add(
            f"zeta_phase_{shift}",
            [phase_power(ZETA, shift * residue) for residue in RESIDUES],
            "zeta_phase",
        )
    for left, right in combinations(range(7), 2):
        vector = [0] * 7
        vector[left] = 1
        vector[right] = 1
        add(f"pair_{left + 1}_{right + 1}", vector, "low_weight_pair")
        vector = [0] * 7
        vector[left] = 1
        vector[right] = -1
        add(f"diff_{left + 1}_{right + 1}", vector, "low_weight_pair")
    deduped = []
    seen = set()
    for row in vectors:
        key = tuple(row["vector"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def forced_equal_pairs(u: list[int], v: list[int]) -> list[list[int]]:
    forced = []
    for left, right in combinations(LABELS, 2):
        diff = right - left
        ok = True
        for idx, residue in enumerate(RESIDUES):
            phase = (phase_power(ZETA, diff * residue) - 1) % MODULUS
            if phase and (u[idx] or v[idx]):
                ok = False
                break
        if ok:
            forced.append([left + 1, right + 1])
    return forced


def build_planes(limit: int) -> list[dict]:
    library = vector_library()
    planes = []
    seen = set()
    for left, right in combinations(library, 2):
        if rank([left["vector"], right["vector"]]) < 2:
            continue
        key = rref_key([left["vector"], right["vector"]])
        if key in seen:
            continue
        seen.add(key)
        forced = forced_equal_pairs(left["vector"], right["vector"])
        if forced:
            continue
        families = sorted({left["family"], right["family"]})
        score = (
            0 if "zeta_phase" in families else 1,
            0 if "standard" in families else 1,
            sum(1 for value in left["vector"] if value) + sum(1 for value in right["vector"] if value),
        )
        planes.append(
            {
                "plane_id": f"rank2_plane_{len(planes):04d}",
                "left_vector_id": left["name"],
                "right_vector_id": right["name"],
                "families": families,
                "u": left["vector"],
                "v": right["vector"],
                "gf17_rref_key": [list(row) for row in key],
                "forced_equal_pairs": forced,
                "score_tuple": list(score),
                "exact_menu_status": "PENDING_SAGE_AUDIT",
            }
        )
    planes.sort(key=lambda row: tuple(row["score_tuple"]))
    return planes[:limit]


def build_records(limit: int) -> tuple[dict, dict]:
    planes = build_planes(limit)
    menu_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "83c6f93",
        "rank2_carrier_generator": {
            "base_field_for_library": "GF(17)",
            "zeta_mod_17": ZETA,
            "planes_generated": len(planes),
            "planes_rejected_for_forced_pair": "filtered",
            "best_failure_mode": "MU8_RANK2_CARRIER_EXACT_MENU_PENDING",
        },
        "carrier_planes": planes,
        "proof_status": "CANDIDATE / MU8_RANK2_CARRIER_EXACT_MENU_PENDING / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    schedule_record = {
        "track": "INTERLEAVED_LIST",
        "row": "RS[F_17^32,H,256]",
        "denominator": "17^32",
        "agreement_target": TARGET_AGREEMENT,
        "source_commit": "83c6f93",
        "schedule_candidates": {
            "constructed": 0,
            "selected_for_exact_interpolation": 0,
            "best_failure_mode": "MU8_RANK2_CARRIER_SAGE_MENU_PENDING",
        },
        "candidates": [],
        "proof_status": "CANDIDATE / MU8_RANK2_CARRIER_SAGE_MENU_PENDING / PARTIAL / EXPERIMENTAL",
        "mca_counted": False,
        "not_claimed": NOT_CLAIMED,
    }
    return menu_record, schedule_record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--limit", type=int, default=64)
    args = parser.parse_args()
    menu_record, schedule_record = build_records(args.limit)
    if args.write:
        OUTPUT_DATA.write_text(json.dumps(menu_record, indent=2, sort_keys=True) + "\n")
        SCHEDULE_OUTPUT.write_text(json.dumps(schedule_record, indent=2, sort_keys=True) + "\n")
    summary = {
        "proof_status": menu_record["proof_status"],
        "planes_generated": menu_record["rank2_carrier_generator"]["planes_generated"],
        "schedule_status": schedule_record["proof_status"],
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    elif not args.write:
        print("M1_A327_MU8_RANK2_CARRIER_GENERATOR_READY")


if __name__ == "__main__":
    main()
