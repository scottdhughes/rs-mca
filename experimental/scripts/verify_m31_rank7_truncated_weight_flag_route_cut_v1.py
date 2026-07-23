#!/usr/bin/env python3
"""Verify the M31 rank-seven truncated-weight/flag route cut.

This verifier proves and specializes a rank-uniform truncated generalized-
weight incidence inequality.  At rank seven it combines the exact affine-
fiber caps, common-zero Johnson compiler, and coset-free codimension-one
compiler.  The result pays the two rank-seven flanks and freezes the exact
primitive middle.  It does not close rank seven, any higher rank, or the
complete M31 LIST row.

All deployed gates use exact integer or rational arithmetic.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


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

RANK = 7
G_MIN = W + RANK
G_MAX = A
D6_MIN = N - K + 6
T0_TURN = 1_177_354

SCHEMA_ID = "m31-rank7-truncated-weight-flag-route-cut-summary-v1"
THEOREM_ID = "M31_RANK7_TRUNCATED_WEIGHT_FLAG_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_RANK7_TRUNCATED_WEIGHT_FLAG_V1"
STATUS = "PROVED_RANK7_TWO_FLANK_ROUTE_CUT_MIDDLE_OPEN"
TERMINAL_LOW = "UNPAID_RANK7_MIXED_G_NEAR_MDS_LOCATOR_INCIDENCE"
TERMINAL_MIDDLE = "UNPAID_RANK7_FIXED_G_ORDINARY_RS_MIDDLE_OR_MIXED_G"
PARENT_PAYLOAD = (
    "3e0a6102795f88aa8121229bc40bcc723aa7e5cc81bbcfd5b0013adf5d11caf9"
)


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def product(values: Any) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def falling(value: int, length: int) -> int:
    require(length >= 0, "falling length nonnegative")
    require(value >= length, "falling argument large enough")
    return product(value - offset for offset in range(length))


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0, "ceil numerator nonnegative")
    require(denominator > 0, "ceil denominator positive")
    return (numerator + denominator - 1) // denominator


def fraction_record(value: Fraction) -> dict[str, int]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "floor": value.numerator // value.denominator,
    }


def affine_fiber_cap(dimension: int) -> int:
    require(0 <= dimension <= RANK - 1, "affine fiber dimension")
    return comb((N - K) + dimension, dimension) // comb(
        W + dimension, dimension
    )


def raw_q6_cap(union_size: int, fiber_dimension: int) -> int:
    """Cap q_6 from a truncated independent-tuple/fiber inequality."""
    require(G_MIN <= union_size <= G_MAX, "legal rank-seven union")
    require(1 <= fiber_dimension <= RANK - 2, "q6-visible fiber dimension")
    tuple_length = RANK - fiber_dimension
    fixed = SHALLOW_SIZE * union_size * product(
        W + index for index in range(fiber_dimension + 1, RANK - 1)
    )
    numerator = affine_fiber_cap(fiber_dimension) * falling(
        R + union_size, tuple_length
    )
    return numerator // fixed - (W + RANK - 1)


def q6_envelope(union_size: int) -> tuple[int, int, int, int]:
    """Return (used cap, winning k, raw cap, strict-weight cap)."""
    raw_candidates = [
        (raw_q6_cap(union_size, fiber_dimension), fiber_dimension)
        for fiber_dimension in range(1, RANK - 1)
    ]
    raw_cap, winner = min(raw_candidates)
    strict_cap = union_size - W - RANK
    require(strict_cap >= 0, "strict generalized-weight cap nonnegative")
    return min(raw_cap, strict_cap), winner, raw_cap, strict_cap


def pi_profile(d6: int, layer_mismatch: int) -> int:
    require(d6 >= D6_MIN, "legal d6")
    require(layer_mismatch >= 0, "layer mismatch nonnegative")
    return (d6 - R + layer_mismatch) * product(
        W + index + layer_mismatch for index in range(1, 6)
    )


def old_support_term(d6: int) -> Fraction:
    return Fraction(falling(d6, 6), pi_profile(d6, 0))


def new_layer_term(d6: int, union_size: int) -> Fraction:
    layer = R + union_size - d6
    require(layer >= 1, "strict rank-seven support layer")
    return Fraction(
        falling(d6, 7),
        (W + 1) * pi_profile(d6, layer),
    )


def codimension_one_majorant(union_size: int, q6_cap: int) -> dict[str, Any]:
    d6_max = D6_MIN + q6_cap
    require(d6_max < R + union_size, "d6 below full support")

    # T0 decreases through T0_TURN and increases thereafter.  T1 is
    # increasing.  On the low interval use separate monotone maxima; on the
    # high interval both terms increase, so its right endpoint is exact.
    low_endpoint = min(T0_TURN, d6_max)
    low_majorant = old_support_term(D6_MIN) + new_layer_term(
        low_endpoint, union_size
    )
    candidates: list[tuple[str, Fraction]] = [("LOW_PIECE", low_majorant)]
    if d6_max >= T0_TURN:
        high_endpoint = old_support_term(d6_max) + new_layer_term(
            d6_max, union_size
        )
        candidates.append(("HIGH_ENDPOINT", high_endpoint))
    owner, bound = max(candidates, key=lambda item: item[1])
    return {
        "owner": owner,
        "d6_max": d6_max,
        "low_piece": low_majorant,
        "bound": bound,
    }


def common_zero_johnson(union_size: int, q1: int = 0) -> int | None:
    require(G_MIN <= union_size <= G_MAX, "Johnson union range")
    require(q1 >= 0, "q1 nonnegative")
    active_length = R + union_size
    alpha = union_size - W - 1 - q1
    require(alpha >= 0, "Johnson alpha nonnegative")
    denominator = union_size**2 - active_length * alpha
    if denominator <= 0:
        return None
    numerator = active_length * (W + 1 + q1)
    return numerator // denominator


def q1_johnson_payment_threshold(union_size: int) -> int:
    """Least q1 for which the exact Johnson floor is <= SHALLOW_TARGET."""
    active_length = R + union_size
    denominator_at_zero = union_size**2 - active_length * (
        union_size - W - 1
    )
    numerator_gap = (
        active_length * (W + 1) - SHALLOW_SIZE * denominator_at_zero
    )
    if numerator_gap < 0:
        return 0
    return numerator_gap // ((SHALLOW_SIZE - 1) * active_length) + 1


def fixed_g_johnson_cap(degree: int) -> int | None:
    """Ordinary RS cap for one fixed-G slice at zero excess."""
    require(W + 1 <= degree <= R, "fixed-G degree range")
    denominator = degree**2 - R * (degree - W - 1)
    if denominator <= 0:
        return None
    return R * (W + 1) // denominator


def truncated_weight_scan() -> dict[str, Any]:
    fiber_caps = {str(k): affine_fiber_cap(k) for k in range(0, RANK)}
    require(
        fiber_caps
        == {
            "0": 1,
            "1": 15,
            "2": 241,
            "3": 3_757,
            "4": 58_410,
            "5": 908_021,
            "6": 14_115_528,
        },
        "exact affine fiber caps",
    )

    winner_counts: dict[int, int] = {}
    transitions: list[dict[str, int]] = []
    previous_winner: int | None = None
    maximum_q6 = -1
    maximum_q6_points: list[int] = []
    minimum_interpolation_margin = 10**30

    for union_size in range(G_MIN, G_MAX + 1):
        cap, winner, raw_cap, strict_cap = q6_envelope(union_size)
        winner_counts[winner] = winner_counts.get(winner, 0) + 1
        if winner != previous_winner:
            transitions.append(
                {
                    "union_size": union_size,
                    "winning_fiber_dimension": winner,
                    "raw_q6_cap": raw_cap,
                }
            )
            previous_winner = winner

        if cap > maximum_q6:
            maximum_q6 = cap
            maximum_q6_points = [union_size]
        elif cap == maximum_q6:
            maximum_q6_points.append(union_size)

        d6_max = D6_MIN + cap
        margin = 5 * (W + 1) - (d6_max - R)
        minimum_interpolation_margin = min(minimum_interpolation_margin, margin)
        require(margin >= 0, "profile interpolation on every rank-seven cell")
        require(d6_max < R + union_size, "strict d6<d7 on every cell")

    require(
        transitions
        == [
            {
                "union_size": 67_454,
                "winning_fiber_dimension": 1,
                "raw_q6_cap": 837_776,
            },
            {
                "union_size": 76_877,
                "winning_fiber_dimension": 5,
                "raw_q6_cap": 770_616,
            },
        ],
        "exact fiber-owner transition",
    )
    require(
        winner_counts == {1: 9_423, 5: 1_039_147},
        "winner histogram",
    )
    require(maximum_q6 == 242_225, "global q6 cap")
    require(
        maximum_q6_points == [309_679, 309_680, 309_681],
        "q6 plateau",
    )
    require(minimum_interpolation_margin == 27_562, "interpolation margin")

    return {
        "rank_uniform_inequality": (
            "sum_i prod_{j=k+1}^r(d_j-R+eta+s_i) "
            "<= B_k*(d_r)_(r-k)"
        ),
        "affine_fiber_cap": (
            "B_k=floor(binomial(n-K+k,k)/binomial(w+k,k))"
        ),
        "fiber_caps": fiber_caps,
        "rank7_union_values_exhausted": G_MAX - G_MIN + 1,
        "winning_fiber_histogram": {
            str(key): value for key, value in sorted(winner_counts.items())
        },
        "winner_transitions": transitions,
        "maximum_q6": maximum_q6,
        "maximum_q6_unions": maximum_q6_points,
        "maximum_d6": D6_MIN + maximum_q6,
        "minimum_profile_interpolation_margin": minimum_interpolation_margin,
    }


def rank7_flank_scan() -> dict[str, Any]:
    johnson_paid: list[int] = []
    codim_paid: list[int] = []
    first_unpaid_johnson: tuple[int, int] | None = None
    last_unpaid_codim: tuple[int, int] | None = None
    first_paid_codim: tuple[int, int] | None = None
    threshold_records: dict[str, Any] = {}

    for union_size in range(G_MIN, G_MAX + 1):
        cap, _, _, _ = q6_envelope(union_size)
        codim = codimension_one_majorant(union_size, cap)
        codim_floor = codim["bound"].numerator // codim["bound"].denominator
        johnson_floor = common_zero_johnson(union_size)

        if johnson_floor is not None and johnson_floor <= SHALLOW_TARGET:
            johnson_paid.append(union_size)
        elif first_unpaid_johnson is None:
            denominator = union_size**2 - (R + union_size) * (
                union_size - W - 1
            )
            first_unpaid_johnson = (union_size, denominator)

        if codim_floor <= SHALLOW_TARGET:
            codim_paid.append(union_size)
            if first_paid_codim is None:
                first_paid_codim = (union_size, codim_floor)
        else:
            last_unpaid_codim = (union_size, codim_floor)

        if union_size in (72_427, 72_428, 354_998, 354_999):
            threshold_records[str(union_size)] = {
                "johnson_floor": johnson_floor,
                "q6_cap": cap,
                "codim_owner": codim["owner"],
                "codim_floor": codim_floor,
                "low_piece_floor": codim["low_piece"].numerator
                // codim["low_piece"].denominator,
            }

    require(johnson_paid == list(range(G_MIN, 72_428)), "Johnson paid prefix")
    require(first_unpaid_johnson == (72_428, -898_676), "Johnson transition")
    require(
        common_zero_johnson(72_427) == 4_735_771,
        "last Johnson cap",
    )
    require(codim_paid == list(range(354_999, G_MAX + 1)), "codim paid suffix")
    require(last_unpaid_codim == (354_998, 15_776_141), "last codim failure")
    require(first_paid_codim == (354_999, 15_775_924), "first codim payment")
    require(
        threshold_records["354998"]["low_piece_floor"] == 14_336_564,
        "last-unpaid low-piece majorant",
    )
    require(
        threshold_records["354999"]["low_piece_floor"] == 14_336_558,
        "first-paid low-piece majorant",
    )

    return {
        "common_zero_johnson_paid_range": [G_MIN, 72_427],
        "codimension_one_paid_range": [354_999, G_MAX],
        "primitive_rank7_union_range": [72_428, 354_998],
        "primitive_union_count": 354_998 - 72_428 + 1,
        "last_johnson_cap": 4_735_771,
        "last_codim_failure": 15_776_141,
        "last_codim_excess": 15_776_141 - SHALLOW_SIZE,
        "first_codim_payment": 15_775_924,
        "first_codim_margin": SHALLOW_TARGET - 15_775_924,
        "threshold_records": threshold_records,
    }


def primitive_owner_partition() -> dict[str, Any]:
    q1_thresholds = {
        str(g): q1_johnson_payment_threshold(g)
        for g in (72_428, 72_858, 72_859, 354_998)
    }
    require(
        q1_thresholds
        == {"72428": 1, "72858": 374, "72859": 375, "354998": 193_230},
        "q1 Johnson thresholds",
    )

    fixed_caps: dict[int, int] = {}
    for union_size in range(72_428, 72_859):
        values = [
            cap
            for degree in range(W + 1, union_size + 1)
            if (cap := fixed_g_johnson_cap(degree)) is not None
        ]
        require(values, "fixed-G Johnson values present")
        fixed_caps[union_size] = max(values)

    require(fixed_caps[72_428] == 183, "fixed-G cap at low sliver start")
    require(fixed_caps[72_858] == 174_019, "fixed-G cap before endpoint")
    require(
        all(
            fixed_caps[left] <= fixed_caps[right]
            for left, right in zip(range(72_428, 72_858), range(72_429, 72_859))
        ),
        "fixed-G caps monotone in low sliver",
    )

    endpoint_peeling_cap = 2_310_492
    locator_floors = {
        "72428": ceil_div(SHALLOW_SIZE, fixed_caps[72_428]),
        "72858": ceil_div(SHALLOW_SIZE, fixed_caps[72_858]),
        "72859": ceil_div(SHALLOW_SIZE, endpoint_peeling_cap),
    }
    require(
        locator_floors == {"72428": 86_208, "72858": 91, "72859": 7},
        "low-sliver locator floors",
    )

    return {
        "first_match_order": [
            "COMMON_ZERO_JOHNSON",
            "TRUNCATED_WEIGHT_CODIM_ONE",
            "FIXED_G_JOHNSON_OR_ENDPOINT_PEELING",
            TERMINAL_LOW,
            TERMINAL_MIDDLE,
        ],
        "johnson_q1_payment_thresholds": q1_thresholds,
        "low_mixed_g_sliver": [72_428, 72_859],
        "fixed_g_standard_johnson_range": [W + 1, 72_858],
        "fixed_g_endpoint_peeling_degree": 72_859,
        "fixed_g_endpoint_peeling_cap": endpoint_peeling_cap,
        "minimum_distinct_G_floors": locator_floors,
        "ordinary_rs_middle_overlap": {
            "union_range": [72_860, 354_998],
            "dimension_range": [5_413, 287_551],
            "full_parent_unresolved_dimension_range": [5_413, 840_822],
        },
        "residual_conditions": [
            "rank=7",
            "72428<=g<=354998",
            "0<=q1<=q6<=Q6(g)",
            "q1<qJ(g)",
            "codim_one_bound(g,q6)>=15775933",
        ],
    }


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    text = json.dumps(
        value,
        sort_keys=True,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return (text + "\n").encode("ascii")


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unsigned)).hexdigest()


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


def tamper_selftest() -> dict[str, Any]:
    expected = build_summary()
    paths_and_values = [
        (("row", "shallow_size"), SHALLOW_SIZE + 1),
        (("truncated_weight_compiler", "maximum_q6"), 242_226),
        (("truncated_weight_compiler", "maximum_d6"), 1_290_808),
        (("truncated_weight_compiler", "minimum_profile_interpolation_margin"), 27_561),
        (("rank7_flanks", "common_zero_johnson_paid_range"), [G_MIN, 72_428]),
        (("rank7_flanks", "codimension_one_paid_range"), [354_998, G_MAX]),
        (("rank7_flanks", "last_johnson_cap"), 4_735_772),
        (("rank7_flanks", "last_codim_failure"), 15_776_140),
        (("rank7_flanks", "first_codim_payment"), 15_775_925),
        (("owner_partition", "low_mixed_g_sliver"), [72_429, 72_859]),
        (("owner_partition", "fixed_g_endpoint_peeling_cap"), 2_310_491),
        (("owner_partition", "minimum_distinct_G_floors", "72428"), 86_207),
        (("impact", "rank7_closed"), True),
        (("impact", "ledger_movement"), 1),
        (("parent_payload_sha256",), "0" * 64),
    ]
    detected = 0
    for path, value in paths_and_values:
        mutant = copy.deepcopy(expected)
        cursor: Any = mutant
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        try:
            deep_exact(mutant, expected)
        except VerificationError:
            detected += 1
        else:
            raise VerificationError(f"mutation escaped: {'.'.join(path)}")
    require(detected == len(paths_and_values), "all primary mutations detected")
    return {
        "schema": "m31-rank7-truncated-weight-flag-primary-tamper-v1",
        "mutations": len(paths_and_values),
        "detected": detected,
        "all_detected": True,
        "base_payload_sha256": expected["payload_sha256"],
    }


def build_summary() -> dict[str, Any]:
    global CHECKS
    CHECKS = 0
    require((R, W) == (981_129, 67_447), "deployed radius and excess")
    require(SHALLOW_SIZE == 15_775_933, "shallow source size")
    require(G_MIN == 67_454, "rank-seven legal union floor")
    require(D6_MIN == 1_048_582, "rank-seven d6 floor")

    weights = truncated_weight_scan()
    flanks = rank7_flank_scan()
    owners = primitive_owner_partition()

    summary: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture": ARCHITECTURE_ID,
        "status": STATUS,
        "parent_payload_sha256": PARENT_PAYLOAD,
        "row": {
            "field_prime": P,
            "n": N,
            "K": K,
            "agreement": A,
            "R": R,
            "w": W,
            "B_star": B_STAR,
            "deep_cap": DEEP_CAP,
            "shallow_size": SHALLOW_SIZE,
            "shallow_target": SHALLOW_TARGET,
            "maximum_excess": S_MAX,
        },
        "truncated_weight_compiler": weights,
        "rank7_flanks": flanks,
        "owner_partition": owners,
        "terminals": [TERMINAL_LOW, TERMINAL_MIDDLE],
        "impact": {
            "rank7_closed": False,
            "rank8_and_above_closed": False,
            "row_closed": False,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
        },
        "nonclaims": [
            "No scalar or support profile is promoted to an actual codeword family.",
            "No fixed-G deterministic post-Johnson list theorem is claimed.",
            "No rank at least seven is globally excluded.",
            "No Grande Finale v4 atom receives a numerical payment.",
        ],
    }
    summary["checks"] = CHECKS + 2
    summary["payload_sha256"] = payload_sha256(summary)
    require(summary["payload_sha256"] == payload_sha256(summary), "payload seal")
    require(summary["checks"] == CHECKS + 1, "check counter sealed")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    try:
        summary = tamper_selftest() if args.tamper_selftest else build_summary()
        encoded = canonical_json(summary, pretty=args.pretty)
        if args.output is not None:
            args.output.write_bytes(encoded)
        if not args.check or args.output is None:
            sys.stdout.buffer.write(encoded)
        return 0
    except (VerificationError, AssertionError, ValueError) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
