#!/usr/bin/env python3
"""Verify the M31 varying-G marked-basis rank-five route cut.

The verifier certifies exact consequences of the first-pivot, colored,
cross-block, affine-line, and balanced pair-incidence inequalities for the
base-field boundary shallow family.  It proves no global M31 LIST bound and
moves no Grande Finale v4 ledger atom.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from math import comb
from pathlib import Path
from typing import Any, Callable


P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
DEEP_CAP = 1_001_282
SHALLOW_SIZE = B_STAR - DEEP_CAP
SHALLOW_TARGET = SHALLOW_SIZE - 1
S_MAX = 366_886
M0 = W + 1

SCHEMA_ID = "m31-varying-g-first-pivot-basis-route-cut-summary-v1"
THEOREM_ID = "M31_VARYING_G_FIRST_PIVOT_BASIS_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_FIRST_PIVOT_BASIS_V1"
ARTIFACT_KIND = "EXACT_MARKED_BASIS_AND_AGGREGATE_ROUTE_CUT"
STATUS = "PROVED_MARKED_BASIS_RANK5_CUT_RANK6_WINDOW_OPEN"
TERMINAL = "UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE"
PARENT_PAYLOAD = "78a6b51d69736b574d258df9e20d84155b8be86e51db942bc6c02a710ee7866d"

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "experimental/data/schemas/m31_varying_g_first_pivot_basis_route_cut_v1.schema.json"
DEFAULT_MANIFEST = ROOT / "experimental/data/certificates/m31-varying-g-first-pivot-basis-route-cut-v1/manifest.json"
README_PATH = ROOT / "experimental/data/certificates/m31-varying-g-first-pivot-basis-route-cut-v1/README.md"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_varying_g_first_pivot_basis_route_cut_v1.md"
PRIMARY_PATH = Path(__file__).resolve()
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_v1.sage"
PACKET_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_first_pivot_basis_route_cut_packet_v1.py"
PARENT_MANIFEST_PATH = ROOT / "experimental/data/certificates/m31-varying-g-affine-span-shortening-route-cut-v1/manifest.json"
PARENT_NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_varying_g_affine_span_shortening_route_cut_v1.md"
PARENT_PACKET_PATH = ROOT / "experimental/scripts/verify_m31_varying_g_affine_span_shortening_route_cut_packet_v1.py"


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            indent=2 if pretty else None,
            separators=None if pretty else (",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON encoding") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_sha256(result)
    return result


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"JSON exists: {path}")
    try:
        value = json.loads(path.read_text(encoding="ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"valid ASCII JSON: {path}") from exc
    require(type(value) is dict, f"JSON object: {path}")
    return value


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def falling(value: int, length: int) -> int:
    require(length >= 0, "falling length nonnegative")
    require(value >= length, "falling argument large enough")
    result = 1
    for offset in range(length):
        result *= value - offset
    return result


def first_pivot_cap(rank: int, union_size: int, common_e: int = 0) -> int:
    require(rank >= 1, "positive rank")
    require(W + rank + common_e <= union_size <= A, "legal union")
    numerator = falling(R + union_size - common_e, rank)
    denominator = union_size * falling(W + rank + common_e - 1, rank - 1)
    return numerator // denominator


def endpoint_rank_cap(rank: int) -> dict[str, int | str]:
    low_g = W + rank
    low = first_pivot_cap(rank, low_g)
    high = first_pivot_cap(rank, A)
    if low >= high:
        maximum, endpoint = low, "LOW"
    else:
        maximum, endpoint = high, "HIGH"
    return {
        "rank": rank,
        "low_union": low_g,
        "low_cap": low,
        "high_union": A,
        "high_cap": high,
        "maximum_cap": maximum,
        "maximizing_endpoint": endpoint,
    }


def first_pivot_rank6_threshold() -> dict[str, int]:
    rank = 6
    lo = max(W + rank, R // (rank - 1))
    hi = A
    require(first_pivot_cap(rank, hi) >= SHALLOW_SIZE, "rank6 reaches target")
    while lo < hi:
        mid = (lo + hi) // 2
        if first_pivot_cap(rank, mid) >= SHALLOW_SIZE:
            hi = mid
        else:
            lo = mid + 1
    return {
        "first_union_not_excluded": lo,
        "predecessor_cap": first_pivot_cap(rank, lo - 1),
        "threshold_cap": first_pivot_cap(rank, lo),
    }


def affine_line_cap(union_size: int) -> int:
    effective_n = R + union_size
    numerator = 15 * effective_n * comb(effective_n - 1, 4)
    denominator = union_size * comb(W + 5, 4)
    return numerator // denominator


def affine_line_rank6_threshold() -> dict[str, int]:
    survivors = [
        union_size
        for union_size in range(W + 6, A + 1)
        if affine_line_cap(union_size) >= SHALLOW_SIZE
    ]
    require(survivors, "line cap has survivors")
    lo = survivors[0]
    require(survivors == list(range(lo, A + 1)), "line survivors form one suffix")
    return {
        "first_union_not_excluded": lo,
        "predecessor_cap": affine_line_cap(lo - 1),
        "threshold_cap": affine_line_cap(lo),
    }


def cross_min_product(union_size: int) -> int:
    require(union_size > R, "cross uniform product requires g>R")
    return min((union_size - M0) * M0, (union_size - R) * R)


def cross_block_cap(union_size: int) -> int:
    effective_n = R + union_size
    numerator = union_size * R * comb(effective_n - 2, 4)
    denominator = cross_min_product(union_size) * comb(W + 4, 4)
    return numerator // denominator


def cross_block_rank6_threshold() -> dict[str, int]:
    open_unions = [
        union_size
        for union_size in range(R + 1, A + 1)
        if cross_block_cap(union_size) >= SHALLOW_SIZE
    ]
    require(open_unions, "cross cap has survivors")
    require(open_unions == list(range(R + 1, open_unions[-1] + 1)),
            "cross survivors form one prefix")
    first_closed = open_unions[-1] + 1
    require(first_closed <= A, "cross cap eventually closes")
    return {
        "last_union_not_excluded": first_closed - 1,
        "last_cap": cross_block_cap(first_closed - 1),
        "first_closed_union": first_closed,
        "first_closed_cap": cross_block_cap(first_closed),
        "high_endpoint_cap": cross_block_cap(A),
    }


def balanced_ceiling(
    budget: int,
    weight: Callable[[int], int],
    *,
    include_histogram: bool = False,
) -> dict[str, int | bool]:
    if SHALLOW_SIZE * weight(0) > budget:
        return {
            "feasible": False,
            "base_excess_q": -1,
            "entries_raised_to_q_plus_1": 0,
            "total_excess_ceiling": -1,
            "uniform_cut": True,
        }
    if SHALLOW_SIZE * weight(S_MAX) <= budget:
        return {
            "feasible": True,
            "base_excess_q": S_MAX,
            "entries_raised_to_q_plus_1": 0,
            "total_excess_ceiling": SHALLOW_SIZE * S_MAX,
            "uniform_cut": False,
        }
    lo, hi = 0, S_MAX
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if SHALLOW_SIZE * weight(mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    q = lo
    marginal = weight(q + 1) - weight(q)
    require(marginal > 0, "positive discrete marginal")
    raised = (budget - SHALLOW_SIZE * weight(q)) // marginal
    require(0 <= raised < SHALLOW_SIZE, "balanced raised range")
    result: dict[str, int | bool] = {
        "feasible": True,
        "base_excess_q": q,
        "entries_raised_to_q_plus_1": raised,
        "total_excess_ceiling": SHALLOW_SIZE * q + raised,
        "uniform_cut": True,
    }
    if include_histogram:
        result["entries_at_q"] = SHALLOW_SIZE - raised
    return result


def rank6_line_excess(union_size: int) -> dict[str, int | bool]:
    effective_n = R + union_size
    budget = 15 * effective_n * comb(effective_n - 1, 4)
    return balanced_ceiling(
        budget,
        lambda excess: (union_size + excess) * comb(W + excess + 5, 4),
        include_histogram=True,
    )


def rank6_cross_excess(union_size: int) -> dict[str, int | bool]:
    if union_size <= R:
        return {
            "feasible": True,
            "base_excess_q": S_MAX,
            "entries_raised_to_q_plus_1": 0,
            "total_excess_ceiling": SHALLOW_SIZE * S_MAX,
            "uniform_cut": False,
        }
    require(union_size < R + M0, "active rank6 cross branch")
    budget = union_size * R * comb(R + union_size - 2, 4)
    return balanced_ceiling(
        budget,
        lambda excess: (
            (union_size - R + excess)
            * R
            * comb(W + excess + 4, 4)
        ),
        include_histogram=True,
    )


def rank6_combined_excess() -> dict[str, int]:
    best = (-1, -1, -1, -1)
    for union_size in range(781_458, 1_033_228):
        line = int(rank6_line_excess(union_size)["total_excess_ceiling"])
        cross = int(rank6_cross_excess(union_size)["total_excess_ceiling"])
        value = min(line, cross)
        if value > best[0]:
            best = (value, union_size, line, cross)
    require(best == (96_161_189_784, 1_009_364, 96_161_189_784, 96_162_018_632),
            "rank6 combined excess maximum")
    line_detail = rank6_line_excess(best[1])
    cross_detail = rank6_cross_excess(best[1])
    require(line_detail["base_excess_q"] == 6_095, "rank6 line base excess")
    require(cross_detail["base_excess_q"] == 6_095, "rank6 cross base excess")
    require(line_detail["entries_raised_to_q_plus_1"] == 6_878_149,
            "rank6 line raised count")
    require(cross_detail["entries_raised_to_q_plus_1"] == 7_706_997,
            "rank6 cross raised count")
    return {
        "total_excess_ceiling": best[0],
        "maximizing_union": best[1],
        "line_ceiling": best[2],
        "cross_ceiling": best[3],
        "base_excess_q": int(line_detail["base_excess_q"]),
        "line_entries_raised": int(line_detail["entries_raised_to_q_plus_1"]),
        "cross_entries_raised": int(cross_detail["entries_raised_to_q_plus_1"]),
    }


def first_pivot_cost(rank: int, union_size: int, excess: int) -> int:
    return (union_size + excess) * comb(W + excess + rank - 1, rank - 1)


def first_pivot_budget(rank: int, union_size: int) -> int:
    effective_n = R + union_size
    return effective_n * comb(effective_n - 1, rank - 1)


def first_pivot_excess_sweep(rank: int) -> dict[str, int | bool]:
    require(7 <= rank <= 12, "high-rank sweep range")
    q = 0
    best = (-1, -1, -1, -1)
    first_full = None
    for union_size in range(W + rank, A + 1):
        budget = first_pivot_budget(rank, union_size)
        weight = lambda excess, g=union_size: first_pivot_cost(rank, g, excess)
        while q > 0 and SHALLOW_SIZE * weight(q) > budget:
            q -= 1
        while q < S_MAX and SHALLOW_SIZE * weight(q + 1) <= budget:
            q += 1
        if SHALLOW_SIZE * weight(q) > budget:
            continue
        if q == S_MAX:
            total, raised = SHALLOW_SIZE * S_MAX, 0
            if first_full is None:
                first_full = union_size
        else:
            marginal = weight(q + 1) - weight(q)
            raised = min(SHALLOW_SIZE - 1, (budget - SHALLOW_SIZE * weight(q)) // marginal)
            total = SHALLOW_SIZE * q + raised
        if total > best[0]:
            best = (total, union_size, q, raised)
    require(best[0] >= 0, "high-rank sweep feasible")
    return {
        "rank": rank,
        "total_excess_ceiling": best[0],
        "maximizing_union": best[1],
        "base_excess_q": best[2],
        "entries_raised_to_q_plus_1": best[3],
        "uniform_cut": best[0] < SHALLOW_SIZE * S_MAX,
        "first_union_permitting_full_shallow_ceiling": first_full if first_full is not None else -1,
    }


def pair_minimum(total: int, universe: int) -> int:
    require(total >= 0 and universe > 0, "pair minimum parameters")
    q, remainder = divmod(total, universe)
    return universe * comb(q, 2) + remainder * q


def scalar_profile() -> dict[str, Any]:
    rank = 6
    union_size = 900_000
    degree = 899_999
    effective_n = R + union_size
    total_m = SHALLOW_SIZE * degree
    q1 = comb(W + 5, 5)
    q2 = comb(W + 4, 4)
    pair_rhs = (SHALLOW_SIZE - 1) * total_m - comb(SHALLOW_SIZE, 2) * (W + 1)
    slacks = {
        "predecessor_basis": comb(effective_n, 6) - SHALLOW_SIZE * comb(W + 6, 6),
        "marked_E": R * comb(effective_n - 1, 5) - SHALLOW_SIZE * degree * q1,
        "marked_S": union_size * comb(effective_n - 1, 5)
        - SHALLOW_SIZE * (union_size - degree) * q1,
        "first_pivot_total": effective_n * comb(effective_n - 1, 5)
        - SHALLOW_SIZE * union_size * q1,
        "cross_block": union_size * R * comb(effective_n - 2, 4)
        - SHALLOW_SIZE * (union_size - degree) * degree * q2,
        "affine_line": 15 * effective_n * comb(effective_n - 1, 4)
        - SHALLOW_SIZE * union_size * comb(W + 5, 4),
        "exact_pair_incidence": pair_rhs
        - pair_minimum(total_m, union_size)
        - pair_minimum(total_m, R),
        "cauchy_moment_times_aR": (
            (2 * SHALLOW_SIZE * total_m
             - SHALLOW_SIZE * (SHALLOW_SIZE - 1) * (W + 1))
            * A * R
            - total_m * total_m * (A + R)
        ),
    }
    require(total_m == 14_198_323_924_067, "scalar profile total degree")
    require(slacks == {
        "predecessor_basis": 59_479_200_309_177_922_870_036_052_970_569_240,
        "marked_E": 27_407_153_349_842_619_929_030_408_431_302_720,
        "marked_S": 176_664_888_061_209_174_836_992_414_341_886_680,
        "first_pivot_total": 204_072_041_411_051_794_766_022_822_773_189_400,
        "cross_block": 460_698_629_600_585_299_877_979_611_070_709_550,
        "affine_line": 2_476_896_532_094_258_299_896_800_951_250,
        "exact_pair_incidence": 867_885_585_529_651_763,
        "cauchy_moment_times_aR": 49_374_815_466_171_856_144_854_090_456_850,
    }, "scalar profile exact slacks")
    require(all(value >= 0 for value in slacks.values()), "scalar profile feasible")
    return {
        "rank": rank,
        "g": union_size,
        "e": 0,
        "all_excess": 0,
        "all_degrees": degree,
        "M": total_m,
        "slacks": slacks,
        "realized_polynomial_family": False,
    }


def source_bindings() -> list[dict[str, str]]:
    specifications = (
        ("packet_schema", SCHEMA_PATH),
        ("primary_exact_replay", PRIMARY_PATH),
        ("independent_sage_replay", SAGE_PATH),
        ("packet_verifier", PACKET_PATH),
        ("theorem_note", NOTE_PATH),
        ("packet_readme", README_PATH),
        ("parent_manifest", PARENT_MANIFEST_PATH),
        ("parent_note", PARENT_NOTE_PATH),
    )
    return [
        {
            "binding_id": f"M31_FIRST_PIVOT::{role}",
            "role": role,
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": sha256_path(path),
        }
        for role, path in specifications
    ]


def build_payload() -> dict[str, Any]:
    require(N == A + R, "domain partition")
    require(W == A - K, "anchor deficit")
    require(SHALLOW_SIZE == 15_775_933, "shallow family size")
    require(SHALLOW_TARGET == 15_775_932, "shallow target")
    require(N - K + 1 == 1_048_577, "affine line numerator")
    require((N - K + 1) // (W + 1) == 15, "affine line multiplicity")
    require(R // (W + 1) == 14, "projective ray multiplicity")
    require((SHALLOW_SIZE + 13) // 14 == 1_126_853, "projective direction floor")

    parent = load_json(PARENT_MANIFEST_PATH)
    require(parent.get("payload_sha256") == PARENT_PAYLOAD, "parent payload pin")

    rank_caps = [endpoint_rank_cap(rank) for rank in range(1, 6)]
    require([row["maximum_cap"] for row in rank_caps]
            == [15, 241, 3_757, 58_410, 1_756_141],
            "rank1-5 maximum caps")
    require(all(int(row["maximum_cap"]) < SHALLOW_SIZE for row in rank_caps),
            "rank1-5 excluded")

    first_pivot_threshold = first_pivot_rank6_threshold()
    require(first_pivot_threshold == {
        "first_union_not_excluded": 520_449,
        "predecessor_cap": 15_775_901,
        "threshold_cap": 15_775_934,
    }, "first-pivot rank6 threshold")

    line_threshold = affine_line_rank6_threshold()
    require(line_threshold == {
        "first_union_not_excluded": 781_458,
        "predecessor_cap": 15_775_916,
        "threshold_cap": 15_775_941,
    }, "affine-line rank6 threshold")

    cross_threshold = cross_block_rank6_threshold()
    require(cross_threshold == {
        "last_union_not_excluded": 1_033_227,
        "last_cap": 15_776_172,
        "first_closed_union": 1_033_228,
        "first_closed_cap": 15_775_916,
        "high_endpoint_cap": 14_468_798,
    }, "cross-block rank6 threshold")

    rank6_excess = rank6_combined_excess()
    high_excess = [first_pivot_excess_sweep(rank) for rank in range(7, 13)]
    require(
        [row["total_excess_ceiling"] for row in high_excess[:5]]
        == [
            1_230_614_224_136,
            2_269_797_172_033,
            3_348_220_234_408,
            4_424_565_157_287,
            5_474_137_140_842,
        ],
        "rank7-11 excess ceilings",
    )
    require(
        [row["base_excess_q"] for row in high_excess[:5]]
        == [78_005, 143_877, 212_235, 280_462, 346_992],
        "rank7-11 balanced bases",
    )
    require(high_excess[-1]["uniform_cut"] is False, "rank12 full range open")
    require(high_excess[-1]["first_union_permitting_full_shallow_ceiling"] == 909_846,
            "rank12 first full union")
    rank12_before = (
        first_pivot_budget(12, 909_845)
        // first_pivot_cost(12, 909_845, S_MAX)
    )
    rank12_at = (
        first_pivot_budget(12, 909_846)
        // first_pivot_cost(12, 909_846, S_MAX)
    )
    require((rank12_before, rank12_at) == (15_775_932, 15_776_019),
            "rank12 adjacent full caps")

    profile = scalar_profile()

    payload: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture_id": ARCHITECTURE_ID,
        "artifact_kind": ARTIFACT_KIND,
        "status": STATUS,
        "terminal": TERMINAL,
        "row_contract": {
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "agreement": A,
            "budget": B_STAR,
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "quantifier": "EVERY_RECONSTRUCTED_BASE_FIELD_BOUNDARY_SHALLOW_SUBFAMILY",
        },
        "deployed_parameters": {
            "p": P,
            "n": N,
            "K": K,
            "a": A,
            "R": R,
            "w": W,
            "B_star": B_STAR,
            "deep_cap": DEEP_CAP,
            "shallow_size": SHALLOW_SIZE,
            "shallow_target": SHALLOW_TARGET,
            "shallow_excess_range": [0, S_MAX],
        },
        "marked_basis_theorem": {
            "rank_definition": "r=dim_Fp span{c_i}",
            "common_zero_count": "z=a-g+e",
            "first_pivot": "sum_i (g+s_i)*(w+s_i+r+e-1)_(r-1) <= (R+g-e)_r",
            "marked_E": "sum_i (m_i+s_i)*C(w+s_i+r+e-1,r-1) <= (R-e)*C(R+g-e-1,r-1)",
            "marked_S": "sum_i (g-m_i)*C(w+s_i+r+e-1,r-1) <= g*C(R+g-e-1,r-1)",
            "cross_block": "sum_i (g-m_i)*(m_i+s_i)*C(w+s_i+r+e-2,r-2) <= g*(R-e)*C(R+g-e-2,r-2)",
            "affine_line": "sum_i (g+s_i)*C(w+s_i+r+e-1,r-2) <= 15*(R+g-e)*C(R+g-e-1,r-2)",
            "affine_line_multiplicity": 15,
            "projective_ray_multiplicity": 14,
            "minimum_projective_directions": 1_126_853,
            "ordered_full_rank_tuple_owns_at_most_one_codeword": True,
        },
        "rank_consequences": {
            "rank_1_through_5_excluded": True,
            "worst_case_zero_excess_caps": rank_caps,
            "rank6_first_pivot_threshold": first_pivot_threshold,
            "rank6_affine_line_threshold": line_threshold,
            "rank6_cross_block_threshold": cross_threshold,
            "rank6_surviving_union_interval": [781_458, 1_033_227],
            "rank6_combined_excess": rank6_excess,
            "rank7_through_12_first_pivot_excess": high_excess,
            "rank12_adjacent_full_caps": [rank12_before, rank12_at],
        },
        "balanced_pair_incidence": {
            "definition": "pi(T,v)=v*C(q,2)+rho*q for T=q*v+rho and 0<=rho<v",
            "gate": "pi(M,g)+pi(M+S,R-e) <= (L-1)*M-C(L,2)*(w+1)",
            "degree_range": "L*(w+e+1)<=M<=min(L*g,L*(R-e)-S)",
            "individual_gate": "2*e+s_i<=R-w-1",
        },
        "aggregate_route_cut": profile,
        "toy_sharpness": {
            "scope": "EXACT_TINY_FIELD_CONTROL_ONLY",
            "field": 17,
            "n": 14,
            "K": 12,
            "w": 0,
            "R": 2,
            "family_size": 90,
            "rank": 12,
            "g": 12,
            "e": 0,
            "distinct_G": 78,
            "max_fixed_G": 2,
            "Wronskian_pairs": 4_005,
            "basis_capacity": 91,
            "first_pivot_slack": 479_001_600,
            "marked_E_slack": 0,
            "canonical_family_sha256": "2ed7462c2a4041ca893b39e194c1e6331751171c4cb982cd9625501ce05a10b9",
            "deployed_bound_proved": False,
        },
        "dependency_contract": {
            "stacked_on_parent": True,
            "parent_payload_sha256": PARENT_PAYLOAD,
        },
        "ledger_state": {
            "movement_from_this_packet": 0,
            "official_endpoint_or_score_movement": 0,
            "row_closed": False,
            "route_cut_not_payment": True,
        },
        "nonclaims": {
            "complete_M31_list_bound_proved": False,
            "rank6_paid": False,
            "scalar_profile_realized": False,
            "toy_family_is_deployed_evidence": False,
            "fixed_syndrome_secant_theorem_proved": False,
            "stable_paper_modified": False,
        },
        "source_bindings": source_bindings(),
    }
    return seal(payload)


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema") == SCHEMA_ID, "schema id")
    require(payload.get("theorem_id") == THEOREM_ID, "theorem id")
    require(payload.get("architecture_id") == ARCHITECTURE_ID, "architecture id")
    require(payload.get("artifact_kind") == ARTIFACT_KIND, "artifact kind")
    require(payload.get("status") == STATUS, "status")
    require(payload.get("terminal") == TERMINAL, "terminal")
    require(payload.get("payload_sha256") == payload_sha256(payload), "payload seal")
    require(payload["rank_consequences"]["rank_1_through_5_excluded"] is True,
            "rank1-5 status")
    require(payload["rank_consequences"]["rank6_surviving_union_interval"]
            == [781_458, 1_033_227], "rank6 interval")
    require(payload["rank_consequences"]["rank6_combined_excess"] == {
        "total_excess_ceiling": 96_161_189_784,
        "maximizing_union": 1_009_364,
        "line_ceiling": 96_161_189_784,
        "cross_ceiling": 96_162_018_632,
        "base_excess_q": 6_095,
        "line_entries_raised": 6_878_149,
        "cross_entries_raised": 7_706_997,
    }, "rank6 excess envelope")
    require(payload["marked_basis_theorem"]["affine_line_multiplicity"] == 15,
            "affine-line multiplicity")
    require(payload["marked_basis_theorem"]["projective_ray_multiplicity"] == 14,
            "projective-ray multiplicity")
    require(payload["marked_basis_theorem"]["minimum_projective_directions"]
            == 1_126_853, "projective direction count")
    deep_exact(payload["aggregate_route_cut"], scalar_profile(),
               "aggregate_route_cut")
    require(payload["toy_sharpness"]["deployed_bound_proved"] is False,
            "toy scope")
    require(payload["toy_sharpness"]["canonical_family_sha256"]
            == "2ed7462c2a4041ca893b39e194c1e6331751171c4cb982cd9625501ce05a10b9",
            "toy family digest")
    require(payload["dependency_contract"]["parent_payload_sha256"] == PARENT_PAYLOAD,
            "parent dependency pin")
    require(payload["ledger_state"]["movement_from_this_packet"] == 0,
            "zero ledger movement")
    require(payload["ledger_state"]["row_closed"] is False, "row open")
    require(payload["nonclaims"]["rank6_paid"] is False, "rank6 unpaid")
    bindings = payload.get("source_bindings")
    require(type(bindings) is list and len(bindings) == 8, "source binding count")
    seen: set[str] = set()
    for binding in bindings:
        require(type(binding) is dict, "source binding object")
        require(set(binding) == {"binding_id", "role", "path", "sha256"},
                "source binding keys")
        path_text = binding["path"]
        require(type(path_text) is str and not path_text.startswith("/"),
                "relative source path")
        require(".." not in Path(path_text).parts, "no source traversal")
        require(path_text not in seen, "source path unique")
        seen.add(path_text)
        path = ROOT / path_text
        require(path.is_file(), f"bound source exists: {path_text}")
        require(sha256_bytes(path.read_bytes()) == binding["sha256"],
                f"fresh source hash: {path_text}")


def validate_schema_top_level(payload: dict[str, Any]) -> None:
    schema = load_json(SCHEMA_PATH)
    require(schema.get("additionalProperties") is False, "closed schema")
    properties = schema.get("properties")
    required = schema.get("required")
    require(type(properties) is dict and type(required) is list, "schema shape")
    require(set(payload) == set(properties) == set(required), "schema exact keys")
    for key, specification in properties.items():
        if isinstance(specification, dict) and "const" in specification:
            require(payload[key] == specification["const"], f"schema const {key}")


def tamper_selftest(payload: dict[str, Any]) -> dict[str, Any]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("status", lambda x: x.__setitem__("status", "SAFE")),
        ("rank5", lambda x: x["rank_consequences"].__setitem__("rank_1_through_5_excluded", False)),
        ("rank6-low", lambda x: x["rank_consequences"]["rank6_surviving_union_interval"].__setitem__(0, 781_457)),
        ("rank6-high", lambda x: x["rank_consequences"]["rank6_surviving_union_interval"].__setitem__(1, 1_033_228)),
        ("rank6-excess", lambda x: x["rank_consequences"]["rank6_combined_excess"].__setitem__("total_excess_ceiling", 96_161_189_785)),
        ("obsolete-cross-envelope", lambda x: x["rank_consequences"].__setitem__("rank6_combined_excess", {
            "total_excess_ceiling": 98_858_386_539,
            "maximizing_union": 1_015_559,
            "line_ceiling": 98_858_386_539,
            "cross_ceiling": 98_859_091_194,
            "base_excess_q": 6_266,
            "line_entries_raised": 6_390_361,
            "cross_entries_raised": 7_095_016,
        })),
        ("rank6-line-histogram", lambda x: x["rank_consequences"]["rank6_combined_excess"].__setitem__("line_entries_raised", 6_878_150)),
        ("line-multiplicity", lambda x: x["marked_basis_theorem"].__setitem__("affine_line_multiplicity", 16)),
        ("ray-multiplicity", lambda x: x["marked_basis_theorem"].__setitem__("projective_ray_multiplicity", 15)),
        ("scalar-realized", lambda x: x["aggregate_route_cut"].__setitem__("realized_polynomial_family", True)),
        ("scalar-M-transcription", lambda x: x["aggregate_route_cut"].__setitem__("M", 14_198_324_019_067)),
        ("scalar-Cauchy-transcription", lambda x: x["aggregate_route_cut"]["slacks"].__setitem__("cauchy_moment_times_aR", 49_374_815_466_156_145_844_854_090_456_850)),
        ("toy-deployed", lambda x: x["toy_sharpness"].__setitem__("deployed_bound_proved", True)),
        ("toy-hash", lambda x: x["toy_sharpness"].__setitem__("canonical_family_sha256", "0" * 64)),
        ("ledger", lambda x: x["ledger_state"].__setitem__("movement_from_this_packet", 1)),
        ("row", lambda x: x["ledger_state"].__setitem__("row_closed", True)),
        ("parent", lambda x: x["dependency_contract"].__setitem__("parent_payload_sha256", "0" * 64)),
        ("source", lambda x: x["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("seal", lambda x: x.__setitem__("payload_sha256", "0" * 64)),
    ]
    detected: list[str] = []
    for name, mutate in mutations:
        changed = copy.deepcopy(payload)
        mutate(changed)
        if name != "seal":
            changed = seal(changed)
        try:
            validate_payload(changed)
        except (VerificationError, KeyError, TypeError, IndexError):
            detected.append(name)
    require(len(detected) == len(mutations), "all mutations detected")
    return {"count": len(mutations), "detected": detected}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()

    payload = build_payload()
    validate_payload(payload)
    validate_schema_top_level(payload)

    if args.tamper_selftest:
        result = tamper_selftest(payload)
        result["status"] = STATUS
        print(canonical_json(result, pretty=True).decode("ascii"), end="")
        return

    if args.write_manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_bytes(canonical_json(payload))

    if args.check:
        committed = load_json(args.manifest)
        deep_exact(committed, payload)
        require(args.manifest.read_bytes() == canonical_json(committed),
                "manifest canonical bytes")

    print(canonical_json(payload).decode("ascii"), end="")


if __name__ == "__main__":
    try:
        main()
    except VerificationError as exc:
        print(f"verification failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
