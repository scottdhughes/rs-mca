#!/usr/bin/env python3
"""Exact certificate for M31 syzygy-coloop elimination and locator route cut.

The hand proof establishes the polynomial-module and common-syndrome lemmas.
This stdlib-only verifier pins their deployed arithmetic, preserves the signed
source-key contract, and guards the remaining owner/refund route cut.  It does
not prove the M31 list bound or formalize polynomial-module theory.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable


P = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
CUTOFF = AGREEMENT - K
RADIUS = N - AGREEMENT
BUDGET = P**4 // 2**100
FORBIDDEN = BUDGET + 1

PACKET_COLUMNS = 46
FORNEY_INDICES = PACKET_COLUMNS - 1
EXCEPTIONAL_INDICES = 1
SMALL_INDICES = FORNEY_INDICES - EXCEPTIONAL_INDICES
SMALL_TOTAL_MAX = RADIUS - CUTOFF - 1
EXCEPTIONAL_INDEX_MIN = CUTOFF + 1

FORCED_SOURCE_KEYS = 259_881
SAFE_SIGNED_ALLOWANCE = FORCED_SOURCE_KEYS - 1

PR1008_HEAD = "bea91e5a6abbb5cdc33bace66c86ac93e18c2b8e"
PR1014_HEAD = "c7cbcf1cff1180b4aac0862ae3c3e665f6b29b21"
PR1021_HEAD = "8a6316f4969eca577825d2504d0ec7d0239b3cb4"

# Explicit balanced zero-sum block patterns for the support-only empty-core
# regression.  Every row has size 15 and sum 0 modulo 32.
EMPTY_CORE_ANCHORS = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 18, 22, 27, 28, 30, 31),
    (8, 9, 10, 12, 13, 14, 15, 16, 17, 19, 20, 23, 25, 26, 29),
    (0, 1, 2, 3, 4, 5, 11, 12, 14, 16, 21, 22, 24, 26, 31),
    (1, 6, 7, 9, 11, 13, 17, 19, 20, 21, 23, 25, 27, 28, 29),
    (0, 2, 3, 4, 6, 7, 9, 10, 15, 17, 18, 22, 24, 25, 30),
    (8, 10, 11, 13, 14, 16, 18, 19, 20, 23, 24, 26, 27, 28, 31),
    (0, 1, 3, 5, 6, 7, 12, 15, 18, 21, 22, 27, 28, 29, 30),
    (2, 4, 5, 8, 9, 10, 11, 12, 14, 15, 21, 23, 29, 30, 31),
    (0, 2, 6, 11, 13, 16, 17, 19, 20, 22, 24, 25, 26, 27, 28),
    (1, 3, 4, 5, 7, 8, 10, 12, 13, 17, 18, 21, 23, 24, 26),
    (0, 1, 4, 9, 14, 15, 16, 17, 19, 20, 25, 26, 29, 30, 31),
    (2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 20, 22, 23, 25, 29),
    (0, 2, 9, 10, 13, 14, 15, 16, 18, 19, 24, 27, 28, 30, 31),
    (1, 3, 4, 5, 6, 7, 8, 11, 17, 18, 19, 20, 21, 22, 30),
    (7, 11, 12, 13, 14, 15, 16, 18, 21, 24, 25, 26, 27, 28, 31),
    (0, 1, 2, 3, 4, 5, 10, 19, 21, 23, 24, 25, 28, 29, 30),
    (0, 6, 8, 12, 13, 14, 15, 16, 17, 20, 22, 23, 29, 30, 31),
    (1, 2, 3, 4, 5, 9, 10, 11, 13, 15, 16, 21, 26, 27, 29),
    (0, 6, 7, 9, 10, 12, 18, 19, 20, 22, 24, 25, 26, 27, 31),
    (1, 2, 3, 4, 8, 11, 14, 15, 17, 21, 22, 23, 24, 28, 31),
    (1, 5, 6, 7, 8, 13, 17, 19, 20, 23, 25, 26, 27, 29, 30),
    (0, 2, 4, 9, 10, 12, 13, 14, 16, 18, 19, 24, 25, 28, 30),
    (3, 5, 6, 7, 8, 9, 12, 15, 17, 20, 21, 22, 23, 27, 29),
    (0, 1, 11, 14, 16, 18, 20, 21, 22, 23, 26, 27, 28, 30, 31),
    (2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 16, 24, 25, 28, 31),
    (0, 7, 11, 12, 13, 14, 15, 16, 17, 18, 19, 26, 28, 29, 31),
    (1, 2, 3, 4, 5, 6, 10, 12, 13, 18, 19, 21, 23, 26, 29),
    (1, 2, 6, 8, 9, 11, 13, 15, 16, 17, 20, 24, 25, 27, 30),
    (0, 3, 4, 5, 7, 8, 15, 17, 18, 19, 22, 24, 26, 27, 29),
    (0, 1, 9, 11, 12, 13, 14, 20, 21, 22, 23, 25, 26, 28, 31),
    (2, 3, 4, 5, 6, 7, 9, 10, 15, 16, 18, 19, 20, 28, 30),
    (0, 8, 10, 12, 14, 17, 19, 21, 22, 24, 25, 26, 29, 30, 31),
    (1, 2, 3, 4, 5, 6, 11, 13, 20, 21, 23, 27, 28, 29, 31),
    (7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 22, 23, 24, 25, 30),
    (0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 16, 25, 26, 27),
    (5, 7, 8, 9, 14, 17, 18, 20, 21, 24, 27, 28, 29, 30, 31),
    (0, 1, 2, 3, 4, 8, 13, 15, 16, 17, 18, 20, 22, 23, 30),
    (5, 6, 12, 13, 15, 16, 19, 21, 22, 23, 24, 26, 27, 28, 31),
    (0, 1, 2, 3, 7, 10, 11, 14, 15, 21, 25, 27, 28, 29, 31),
    (4, 5, 6, 10, 11, 13, 18, 19, 20, 22, 23, 24, 25, 26, 30),
    (2, 3, 7, 8, 9, 10, 12, 14, 16, 17, 20, 22, 24, 29, 31),
    (0, 1, 4, 5, 6, 7, 9, 11, 12, 13, 17, 23, 26, 28, 30),
    (1, 8, 11, 13, 14, 15, 16, 17, 18, 19, 21, 22, 25, 27, 29),
    (0, 2, 3, 4, 5, 6, 7, 8, 9, 18, 24, 25, 26, 27, 28),
    (2, 10, 12, 14, 15, 16, 18, 19, 20, 22, 23, 27, 29, 30, 31),
)

ROOT = Path(__file__).resolve().parents[2]
PYTHON_PATH = ROOT / "experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.py"
SAGE_PATH = ROOT / "experimental/scripts/verify_m31_direct_padded_forney_frame_route_cut.sage"
NOTE_PATH = ROOT / "experimental/notes/thresholds/m31_direct_padded_forney_frame_route_cut.md"
README_PATH = ROOT / "experimental/data/certificates/m31-direct-padded-forney-frame-route-cut/README.md"
CERTIFICATE_PATH = ROOT / "experimental/data/certificates/m31-direct-padded-forney-frame-route-cut/manifest.json"

SOURCE_PATHS = (
    ROOT / "experimental/notes/thresholds/m31_canonical_popov_rank46_compiler.md",
    ROOT / "experimental/notes/l2/rank16_left_kernel_forney_route_cut.md",
    ROOT / "experimental/data/certificates/rank16-left-kernel-forney/f31_fixture.json",
    NOTE_PATH,
    PYTHON_PATH,
    SAGE_PATH,
    README_PATH,
)


class VerificationError(RuntimeError):
    """Raised when an exact gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(payload: Any) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    out.pop("certificate_sha256", None)
    out["certificate_sha256"] = hashlib.sha256(canonical_json(out)).hexdigest()
    return out


def ordered_prefix_max(total: int, ordered_count: int, prefix_count: int) -> int:
    """Largest first-k sum for a nondecreasing nonnegative n-tuple."""
    if not (0 <= prefix_count <= ordered_count and total >= 0 and ordered_count > 0):
        raise VerificationError("ordered-prefix domain")
    quotient, remainder = divmod(total, ordered_count)
    return prefix_count * quotient + max(0, remainder - (ordered_count - prefix_count))


@functools.cache
def exhaustive_optimizer_control() -> dict[str, Any]:
    """Small exhaustive verification of the exact prefix optimizer."""
    cases = 0
    digest = hashlib.sha256()
    for ordered_count in range(2, 7):
        for total in range(16):
            for prefix_count in range(1, ordered_count + 1):
                observed = -1
                for values in itertools.combinations_with_replacement(
                    range(total + 1), ordered_count
                ):
                    if sum(values) <= total:
                        observed = max(observed, sum(values[:prefix_count]))
                expected = ordered_prefix_max(total, ordered_count, prefix_count)
                require(observed == expected, "small exhaustive prefix optimizer")
                digest.update(
                    f"{ordered_count},{total},{prefix_count},{observed}\n".encode()
                )
                cases += 1
    return {"cases": cases, "rows_sha256": digest.hexdigest()}


@functools.cache
def deployed_total_scan() -> dict[str, Any]:
    """Exhaust every allowed small-index total and pin the worst endpoint."""
    digest = hashlib.sha256()
    maximum = -1
    first_cutoff_crossing: int | None = None
    previous = -1
    for total in range(SMALL_TOTAL_MAX + 1):
        value = ordered_prefix_max(total, SMALL_INDICES, 3)
        require(value >= previous, "prefix cap monotone in total")
        if value >= CUTOFF and first_cutoff_crossing is None:
            first_cutoff_crossing = total
        previous = value
        maximum = max(maximum, value)
        digest.update(f"{total},{value}\n".encode())
    require(first_cutoff_crossing is None, "all allowed totals clear cutoff")
    require(maximum == 62_295, "deployed total scan maximum")
    return {
        "first_total": 0,
        "last_total": SMALL_TOTAL_MAX,
        "rows_scanned": SMALL_TOTAL_MAX + 1,
        "rows_sha256": digest.hexdigest(),
        "maximum_rank3_prefix": maximum,
        "first_cutoff_crossing": first_cutoff_crossing,
    }


@functools.cache
def packet_width_scan() -> dict[str, Any]:
    rows = []
    digest = hashlib.sha256()
    minimum: int | None = None
    for columns in range(5, PACKET_COLUMNS + 1):
        small_count = columns - 2
        value = ordered_prefix_max(SMALL_TOTAL_MAX, small_count, 3)
        clears = value < CUTOFF
        if clears and minimum is None:
            minimum = columns
        row = {
            "columns": columns,
            "small_indices": small_count,
            "rank3_prefix": value,
            "clears_cutoff": clears,
        }
        rows.append(row)
        digest.update(f"{columns},{small_count},{value},{int(clears)}\n".encode())
    require(minimum == 43, "minimum packet width")
    by_columns = {row["columns"]: row for row in rows}
    require(by_columns[42]["rank3_prefix"] == 68_526, "width predecessor")
    require(by_columns[43]["rank3_prefix"] == 66_852, "width first pass")
    require(by_columns[46]["rank3_prefix"] == 62_295, "deployed width")
    return {
        "range": [5, PACKET_COLUMNS],
        "minimum_columns_certified": minimum,
        "predecessor": by_columns[42],
        "first_pass": by_columns[43],
        "deployed": by_columns[46],
        "rows_sha256": digest.hexdigest(),
    }


def f11_padding_regression() -> dict[str, Any]:
    actual0 = {6, 7, 8}
    actual1 = {3, 4, 5}
    cross0 = {5, 6, 7, 8}
    cross1 = {3, 4, 5, 8}
    common0 = {2, 6, 7, 8}
    common1 = {2, 3, 4, 5}

    def pair_index(left: set[int], right: set[int]) -> int:
        require(len(left) == len(right), "equal-degree pair")
        return len(left) - len(left & right)

    actual_index = pair_index(actual0, actual1)
    cross_index = pair_index(cross0, cross1)
    common_index = pair_index(common0, common1)
    require((actual_index, cross_index, common_index) == (3, 2, 3),
            "F11 direct padded profiles")
    return {
        "field": 11,
        "actual_error_pair_index": actual_index,
        "cross_order_direct_padded_index": cross_index,
        "common_order_direct_padded_index": common_index,
        "actual_error_frame_identical_across_orders": True,
        "direct_padded_profile_retains_order": True,
        "actual_error_row_transport_claimed": False,
    }


def direct_padded_frame() -> dict[str, Any]:
    require((PACKET_COLUMNS, FORNEY_INDICES, SMALL_INDICES) == (46, 45, 44),
            "frame dimensions")
    require(SMALL_TOTAL_MAX == 913_681, "small-index total")
    quotient, remainder = divmod(SMALL_TOTAL_MAX, SMALL_INDICES)
    require((quotient, remainder) == (20_765, 21), "small-index division")
    prefixes = {
        str(k): ordered_prefix_max(SMALL_TOTAL_MAX, SMALL_INDICES, k)
        for k in range(1, 5)
    }
    require(prefixes == {"1": 20_765, "2": 41_530, "3": 62_295, "4": 83_060},
            "deployed prefix caps")
    require(prefixes["3"] < CUTOFF < prefixes["4"], "rank-three endpoint")
    low_indices = SMALL_INDICES - SMALL_TOTAL_MAX // CUTOFF
    require(low_indices == 31, "low-index count")
    require(RADIUS - EXCEPTIONAL_INDEX_MIN == SMALL_TOTAL_MAX,
            "common-syndrome subtraction")

    return {
        "packet_columns": PACKET_COLUMNS,
        "forney_indices": FORNEY_INDICES,
        "primitive_equal_degree_total_max": RADIUS,
        "common_syndrome_defect_lower": 1,
        "exceptional_indices_lower": EXCEPTIONAL_INDICES,
        "exceptional_index_min": EXCEPTIONAL_INDEX_MIN,
        "small_indices": SMALL_INDICES,
        "small_index_total_max": SMALL_TOTAL_MAX,
        "ordered_partial_sum_max": prefixes,
        "rank3_minor_degree_max": prefixes["3"],
        "rank3_margin": CUTOFF - prefixes["3"],
        "rank4_certified_below_cutoff": False,
        "indices_strictly_below_cutoff_lower": low_indices,
        "module_identity": (
            "G=Lambda_(D\\U); E_i=W_i/G=Lambda_(U\\T_i); "
            "Syz(W_i)=Syz(E_i)"
        ),
        "ordered_selector_and_root_masks_preserved": True,
        "actual_error_to_padded_transport_used": False,
        "masked_diagonal_saturation_rank3_frame_consumed_from_pr1021": True,
        "single_column_deletion_injective_on_syzygy_space": True,
        "rank2_coloop_possible": False,
        "anchor_basis_size": 3,
        "complementary_family_size": 43,
        "distinguished_extra_retained": True,
        "relative_common_core_degree_max": prefixes["3"],
        "pluecker_intermediate_terminal": "UNPAID_CANONICAL_COMMON_CORE_OWNER_REFUND",
        "remaining_terminal": "UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND",
        "pluecker_divisibility": "gcd(E_k:k notin I) divides Delta_I",
        "relative_core_support": "U\\union_(k notin I)T_k",
    }


def signed_source_contract() -> dict[str, Any]:
    require(BUDGET == 16_777_215 and FORBIDDEN == 16_777_216, "budget")
    require((FORCED_SOURCE_KEYS, SAFE_SIGNED_ALLOWANCE) == (259_881, 259_880),
            "signed occupancy thresholds")
    return {
        "forbidden_implies_marked_keys_lower": FORCED_SOURCE_KEYS,
        "safe_signed_allowance": SAFE_SIGNED_ALLOWANCE,
        "all_marked_keys_receive_direct_frame": True,
        "source_key_selection_or_loss": False,
        "signed_occupancy_credits_preserved": True,
        "duplicate_source_key_assignment": False,
        "source_key": "(j,ordered_45_anchor_tuple,distinguished_extra_codeword)",
    }


def root_union_route_cut() -> dict[str, Any]:
    degree = ordered_prefix_max(SMALL_TOTAL_MAX, SMALL_INDICES, 3)
    independent, residual = divmod(SAFE_SIGNED_ALLOWANCE, degree)
    require((degree, independent, residual) == (62_295, 4, 10_700),
            "root-union allowance")
    fifth = (independent + 1) * degree
    require(fifth == 311_475, "fifth root resource")
    require(fifth - SAFE_SIGNED_ALLOWANCE == 51_595, "root-union excess")
    return {
        "optimistic_local_claim": "one marked key injects into one low minor root set",
        "minor_degree_max": degree,
        "independent_resources_fitting": independent,
        "residual_after_fitting": residual,
        "next_resource_total": fifth,
        "next_resource_excess": fifth - SAFE_SIGNED_ALLOWANCE,
        "independent_per_key_or_layer_root_unions_close_row": False,
        "required_new_input": (
            "cross-key global deduplication, a typed semantic owner with exact "
            "charge/refund, primitive-component elimination, or a stronger source theorem"
        ),
    }


@functools.cache
def support_only_empty_core_route_cut() -> dict[str, Any]:
    """Exact W-only counterfamily with empty complementary common cores."""
    block_count = 32
    block_size = 65_408
    fixed_pool = 9
    tag_pool = 4_087
    blocks_per_locator = 15

    require(fixed_pool + tag_pool + block_count * block_size == N,
            "empty-core domain partition")
    require((fixed_pool - 1) + 1 + blocks_per_locator * block_size == RADIUS,
            "empty-core locator size")
    require(1 + (tag_pool - 1) + (block_count - blocks_per_locator) * block_size ==
            AGREEMENT, "empty-core selected-agreement size")

    # Independent subset-sum DP.  Translation by one changes the color by 15,
    # a unit modulo 32, which is the theorem-side explanation for equality.
    dp = [[0] * block_count for _ in range(blocks_per_locator + 1)]
    dp[0][0] = 1
    for value in range(block_count):
        for chosen in range(min(blocks_per_locator, value + 1), 0, -1):
            for residue in range(block_count):
                dp[chosen][(residue + value) % block_count] += dp[chosen - 1][residue]
    color_counts = dp[blocks_per_locator]
    color_count = math.comb(block_count, blocks_per_locator) // block_count
    require(math.gcd(blocks_per_locator, block_count) == 1, "translation color unit")
    require(math.comb(block_count, blocks_per_locator) == 565_722_720,
            "zero-sum family numerator")
    require(color_count == 17_678_835, "zero-sum color size")
    require(color_counts == [color_count] * block_count, "subset-sum DP colors")
    require(color_count >= FORBIDDEN, "enough zero-sum supports")

    anchors = [set(row) for row in EMPTY_CORE_ANCHORS]
    require(len(anchors) == 45 and len(set(EMPTY_CORE_ANCHORS)) == 45,
            "empty-core anchor count")
    require(all(len(row) == blocks_per_locator for row in anchors),
            "empty-core anchor size")
    require(all(sum(row) % block_count == 0 for row in anchors),
            "empty-core anchor color")
    block_occurrences = [sum(block in row for row in anchors)
                         for block in range(block_count)]
    require((min(block_occurrences), max(block_occurrences)) == (20, 22),
            "empty-core balanced anchors")
    max_pair_blocks = max(
        len(left & right) for left, right in itertools.combinations(anchors, 2)
    )
    require(max_pair_blocks <= 13, "empty-core anchor pair overlap")
    fixed_omissions = [sum(index % fixed_pool == point for index in range(45))
                       for point in range(fixed_pool)]
    require(fixed_omissions == [5] * fixed_pool, "empty-core fixed omissions")
    anchor_tags = [index % tag_pool for index in range(45)]
    require(len(set(anchor_tags)) == 45, "empty-core anchor tags distinct")
    require(FORBIDDEN >= tag_pool and
            {index % tag_pool for index in range(tag_pool)} == set(range(tag_pool)),
            "retained consecutive tags cover tag pool")
    require(min(block_occurrences) > 0 and max(block_occurrences) < 45,
            "anchors use and omit every block")

    anchor_digest = hashlib.sha256(canonical_json(list(EMPTY_CORE_ANCHORS))).hexdigest()
    deletion_digest = hashlib.sha256()
    deletion_count = 0
    all_blocks = set(range(block_count))
    all_fixed = set(range(fixed_pool))
    for deleted in itertools.combinations(range(45), 3):
        deleted_set = set(deleted)
        retained = [index for index in range(45) if index not in deleted_set]
        common_blocks = set(all_blocks)
        common_fixed = set(all_fixed)
        common_tags: set[int] | None = None
        for index in retained:
            common_blocks &= anchors[index]
            common_fixed &= all_fixed - {index % fixed_pool}
            tag = {index % tag_pool}
            common_tags = tag if common_tags is None else common_tags & tag
        require(not common_blocks and not common_fixed and not common_tags,
                "every anchor-triple complement has empty gcd")
        deletion_digest.update(f"{deleted[0]},{deleted[1]},{deleted[2]}\n".encode())
        deletion_count += 1
    require(deletion_count == math.comb(45, 3) == 14_190,
            "empty-core deletion census")

    # Any two different color-zero block patterns meet in at most 13 blocks:
    # meeting in 14 would be one swap, and equality of colors would force the
    # removed and inserted labels to coincide modulo 32.
    locator_intersection_max = 13 * block_size + 8 + 1
    agreement_intersection_max = N - 2 * RADIUS + locator_intersection_max
    require(locator_intersection_max == 850_313, "locator overlap cap")
    require(agreement_intersection_max == 985_207, "agreement overlap cap")
    require((K - 1) - agreement_intersection_max == 63_368,
            "MDS overlap margin")

    high_layers = RADIUS - 614_160
    tail = FORBIDDEN - 45
    c_low = 3_730
    c_rows = 45 * (high_layers - 1)
    signed_xi = tail - c_low - c_rows
    require((high_layers, tail, c_rows, signed_xi) ==
            (366_969, 16_777_171, 16_513_560, 259_881),
            "empty-core signed occupancy")

    return {
        "role": "support-only route cut; not a same-received-word RS list",
        "partition": {
            "fixed_pool": fixed_pool,
            "tag_pool": tag_pool,
            "block_count": block_count,
            "block_size": block_size,
        },
        "zero_sum_block_family": {
            "subset_size": blocks_per_locator,
            "color_modulus": block_count,
            "color_zero_count": color_count,
            "all_color_counts": color_counts,
            "translation_color_step": blocks_per_locator,
        },
        "retained_supports": FORBIDDEN,
        "retained_order": (
            "45 explicit anchors in certificate order, then distinct remaining "
            "color-zero subsets in lexicographic order"
        ),
        "tag_index_interval": [0, FORBIDDEN - 1],
        "fixed_tag_period": fixed_pool,
        "variable_tag_period": tag_pool,
        "block_pattern_makes_support_map_injective": True,
        "locator_size": RADIUS,
        "selected_agreement_size": AGREEMENT,
        "pairwise_locator_intersection_max": locator_intersection_max,
        "pairwise_selected_agreement_intersection_max": agreement_intersection_max,
        "pairwise_MDS_margin": (K - 1) - agreement_intersection_max,
        "anchors": {
            "count": len(anchors),
            "rows": [list(row) for row in EMPTY_CORE_ANCHORS],
            "rows_sha256": anchor_digest,
            "block_occurrences": block_occurrences,
            "minimum_block_occurrence": min(block_occurrences),
            "maximum_block_occurrence": max(block_occurrences),
            "maximum_pair_block_intersection": max_pair_blocks,
            "fixed_point_omissions": fixed_omissions,
            "variable_tags_distinct": True,
        },
        "triple_deletion_census": {
            "triples": deletion_count,
            "rows_sha256": deletion_digest.hexdigest(),
            "remaining_42_anchor_locator_intersection_empty": True,
            "every_extra_and_every_anchor_basis_triple_relative_gcd_empty": True,
        },
        "global_locator_gcd_empty": True,
        "global_selected_agreement_core_empty": True,
        "coarse_direct_rank3_cap": ordered_prefix_max(RADIUS, 45, 3),
        "coarse_direct_rank3_below_cutoff": True,
        "signed_occupancy": {
            "tail": tail,
            "C_low": c_low,
            "sum_C_1_through_C_45": c_rows,
            "Xi_46": signed_xi,
        },
        "actual_same_received_word_RS_list": False,
        "semantic_C1_C8_owner_audited": False,
        "falsified_W_only_implication": (
            "canonical-size boundary masks + MDS pair overlap + low padded Forney/Pluecker + "
            "empty complementary gcd imply a paid add-back"
        ),
        "missing_invariant": (
            "simultaneous received-word/padded-pair relations and one-point escapes, "
            "or a typed semantic owner/refund"
        ),
    }


def build_payload() -> dict[str, Any]:
    payload = {
        "schema": "m31-exact-syzygy-coloop-locator-route-cut-v1",
        "artifact_kind": "M31_EXACT_SYZYGY_COLOOP_ELIMINATION_AND_LOCATOR_ROUTE_CUT",
        "dependencies": {
            "integrated_pr1008_rank46_source_head": PR1008_HEAD,
            "stacked_pr1021_masked_saturation_head": PR1021_HEAD,
        },
        "overlap_boundary": {
            "pr1014_counterpacket_provenance_head": PR1014_HEAD,
            "pr1021_62295_numerical_conclusion_consumed": True,
            "pr1021_proof_route": (
                "diagonal-saturation exact sequence, minimal-index monotonicity, "
                "and actual-error exceptional index"
            ),
            "independent_direct_padded_common_syndrome_crosscheck": True,
            "new_rank2_coloop_elimination": True,
            "new_empty_core_support_route_cut": True,
        },
        "deployed": {
            "p": P,
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "cutoff": CUTOFF,
            "radius": RADIUS,
            "budget": BUDGET,
            "forbidden_size": FORBIDDEN,
        },
        "optimizer_control": exhaustive_optimizer_control(),
        "deployed_total_scan": deployed_total_scan(),
        "packet_width_scan": packet_width_scan(),
        "direct_padded_frame": direct_padded_frame(),
        "f11_padding_regression": f11_padding_regression(),
        "signed_source_contract": signed_source_contract(),
        "root_union_route_cut": root_union_route_cut(),
        "support_only_empty_core_route_cut": support_only_empty_core_route_cut(),
        "semantic_terminals": [
            "UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND"
        ],
        "scope_guards": {
            "m31_list_row_closed": False,
            "ledger_movement": 0,
            "owner_charge": None,
            "U_Q": None,
            "U_A": None,
            "stable_tex_modified": False,
            "lean_used_for_discovery": False,
            "toy_controls_are_deployed_enumeration": False,
        },
        "source_sha256": {
            str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS
        },
    }
    return payload


def verify_payload(payload: dict[str, Any]) -> None:
    require(payload["schema"] == "m31-exact-syzygy-coloop-locator-route-cut-v1", "schema")
    require(payload["artifact_kind"] ==
            "M31_EXACT_SYZYGY_COLOOP_ELIMINATION_AND_LOCATOR_ROUTE_CUT",
            "artifact kind")
    dependencies = payload["dependencies"]
    require(dependencies == {
        "integrated_pr1008_rank46_source_head": PR1008_HEAD,
        "stacked_pr1021_masked_saturation_head": PR1021_HEAD,
    }, "dependency heads")
    require(payload["overlap_boundary"] == {
        "pr1014_counterpacket_provenance_head": PR1014_HEAD,
        "pr1021_62295_numerical_conclusion_consumed": True,
        "pr1021_proof_route": (
            "diagonal-saturation exact sequence, minimal-index monotonicity, "
            "and actual-error exceptional index"
        ),
        "independent_direct_padded_common_syndrome_crosscheck": True,
        "new_rank2_coloop_elimination": True,
        "new_empty_core_support_route_cut": True,
    }, "PR1021 overlap boundary")

    deployed = payload["deployed"]
    require((deployed["p"], deployed["n"], deployed["K"]) == (P, N, K),
            "field/code parameters")
    require((deployed["agreement"], deployed["cutoff"], deployed["radius"]) ==
            (AGREEMENT, CUTOFF, RADIUS), "agreement parameters")
    require((deployed["budget"], deployed["forbidden_size"]) == (BUDGET, FORBIDDEN),
            "budget parameters")

    require(payload["optimizer_control"] == exhaustive_optimizer_control(),
            "optimizer exhaustive control")
    require(payload["deployed_total_scan"] == deployed_total_scan(), "deployed total scan")
    require(payload["packet_width_scan"] == packet_width_scan(), "packet width scan")

    frame = payload["direct_padded_frame"]
    require((frame["packet_columns"], frame["forney_indices"], frame["small_indices"]) ==
            (46, 45, 44), "frame dimensions")
    require(frame["primitive_equal_degree_total_max"] == 981_129, "primitive total")
    require(frame["common_syndrome_defect_lower"] == 1, "common syndrome")
    require(frame["exceptional_index_min"] == 67_448, "exceptional index")
    require(frame["small_index_total_max"] == 913_681, "small total")
    require(frame["ordered_partial_sum_max"] ==
            {"1": 20_765, "2": 41_530, "3": 62_295, "4": 83_060},
            "prefix caps")
    require(frame["rank3_margin"] == 5_152, "rank3 margin")
    require(frame["rank4_certified_below_cutoff"] is False, "rank4 route cut")
    require(frame["indices_strictly_below_cutoff_lower"] == 31, "low indices")
    require(frame["ordered_selector_and_root_masks_preserved"] is True, "selector retained")
    require(frame["actual_error_to_padded_transport_used"] is False, "no false transport")
    require(frame["masked_diagonal_saturation_rank3_frame_consumed_from_pr1021"] is True,
            "masked rank3 frame consumed")
    require(frame["single_column_deletion_injective_on_syzygy_space"] is True,
            "deletion injective")
    require(frame["rank2_coloop_possible"] is False, "coloop eliminated")
    require((frame["anchor_basis_size"], frame["complementary_family_size"]) == (3, 43),
            "Pluecker family")
    require(frame["distinguished_extra_retained"] is True, "extra retained")
    require(frame["relative_common_core_degree_max"] == 62_295, "relative core cap")
    require(frame["pluecker_intermediate_terminal"] ==
            "UNPAID_CANONICAL_COMMON_CORE_OWNER_REFUND", "intermediate terminal")
    require(frame["remaining_terminal"] ==
            "UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND",
            "remaining terminal")

    f11 = payload["f11_padding_regression"]
    require((f11["actual_error_pair_index"], f11["cross_order_direct_padded_index"],
             f11["common_order_direct_padded_index"]) == (3, 2, 3), "F11 profiles")
    require(f11["direct_padded_profile_retains_order"] is True, "F11 order")
    require(f11["actual_error_row_transport_claimed"] is False, "F11 transport guard")

    source = payload["signed_source_contract"]
    require(source["forbidden_implies_marked_keys_lower"] == FORCED_SOURCE_KEYS,
            "marked source keys")
    require(source["safe_signed_allowance"] == SAFE_SIGNED_ALLOWANCE, "safe allowance")
    require(source["all_marked_keys_receive_direct_frame"] is True, "all keys framed")
    require(source["source_key_selection_or_loss"] is False, "no key loss")
    require(source["signed_occupancy_credits_preserved"] is True, "credits retained")
    require(source["duplicate_source_key_assignment"] is False, "no duplicate key")

    route = payload["root_union_route_cut"]
    require((route["minor_degree_max"], route["independent_resources_fitting"],
             route["residual_after_fitting"]) == (62_295, 4, 10_700),
            "root-union fit")
    require((route["next_resource_total"], route["next_resource_excess"]) ==
            (311_475, 51_595), "root-union failure")
    require(route["independent_per_key_or_layer_root_unions_close_row"] is False,
            "root-union route cut")

    empty_core = payload["support_only_empty_core_route_cut"]
    require(empty_core == support_only_empty_core_route_cut(),
            "support-only empty-core route cut")
    require(empty_core["zero_sum_block_family"]["color_zero_count"] == 17_678_835,
            "empty-core family size")
    require(empty_core["retained_supports"] == FORBIDDEN, "empty-core retained mass")
    require(empty_core["pairwise_selected_agreement_intersection_max"] == 985_207,
            "empty-core agreement overlap")
    require(empty_core["pairwise_MDS_margin"] == 63_368, "empty-core MDS margin")
    require(empty_core["anchors"]["maximum_block_occurrence"] == 22,
            "empty-core anchor balance")
    require(empty_core["triple_deletion_census"]["triples"] == 14_190,
            "empty-core deletion census")
    require(empty_core["triple_deletion_census"]
            ["every_extra_and_every_anchor_basis_triple_relative_gcd_empty"] is True,
            "empty-core universal complementary gcd")
    require(empty_core["global_locator_gcd_empty"] is True, "empty global locator gcd")
    require(empty_core["global_selected_agreement_core_empty"] is True,
            "empty global agreement core")
    require(empty_core["coarse_direct_rank3_cap"] == 65_406 and
            empty_core["coarse_direct_rank3_below_cutoff"] is True,
            "empty-core coarse padded frame")
    require(empty_core["signed_occupancy"]["Xi_46"] == FORCED_SOURCE_KEYS,
            "empty-core signed occupancy")
    require(empty_core["actual_same_received_word_RS_list"] is False,
            "empty-core source scope")
    require(empty_core["semantic_C1_C8_owner_audited"] is False,
            "empty-core semantic scope")

    require(payload["semantic_terminals"] ==
            ["UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND"],
            "terminal census")
    guards = payload["scope_guards"]
    require(guards["m31_list_row_closed"] is False, "row open")
    require(guards["ledger_movement"] == 0, "ledger movement")
    require(guards["owner_charge"] is None, "owner charge")
    require(guards["U_Q"] is None and guards["U_A"] is None, "open U atoms")
    require(guards["stable_tex_modified"] is False, "stable TeX guard")
    require(guards["lean_used_for_discovery"] is False, "Lean guard")
    require(guards["toy_controls_are_deployed_enumeration"] is False, "toy scope")

    hashes = payload["source_sha256"]
    expected_hashes = {
        str(path.relative_to(ROOT)): sha256_path(path) for path in SOURCE_PATHS
    }
    require(set(hashes) == set(expected_hashes), "source hash keys")
    require(hashes == expected_hashes, "live source hashes")

    claimed = payload.get("certificate_sha256")
    require(isinstance(claimed, str) and len(claimed) == 64, "certificate hash shape")
    unsealed = copy.deepcopy(payload)
    unsealed.pop("certificate_sha256", None)
    require(hashlib.sha256(canonical_json(unsealed)).hexdigest() == claimed,
            "certificate self hash")


def mutate_path(payload: dict[str, Any], path: tuple[str, ...], value: Any) -> dict[str, Any]:
    out = copy.deepcopy(payload)
    cursor: Any = out
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return seal(out)


def tamper_selftest(expected: dict[str, Any]) -> None:
    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("field", lambda d: mutate_path(d, ("deployed", "p"), P - 1)),
        ("dependency", lambda d: mutate_path(d, ("dependencies", "stacked_pr1021_masked_saturation_head"), "0" * 40)),
        ("overlap", lambda d: mutate_path(d, ("overlap_boundary", "pr1014_counterpacket_provenance_head"), "0" * 40)),
        ("scan", lambda d: mutate_path(d, ("deployed_total_scan", "maximum_rank3_prefix"), 62_296)),
        ("width", lambda d: mutate_path(d, ("packet_width_scan", "minimum_columns_certified"), 42)),
        ("syndrome", lambda d: mutate_path(d, ("direct_padded_frame", "common_syndrome_defect_lower"), 0)),
        ("exceptional", lambda d: mutate_path(d, ("direct_padded_frame", "exceptional_index_min"), CUTOFF)),
        ("small-total", lambda d: mutate_path(d, ("direct_padded_frame", "small_index_total_max"), SMALL_TOTAL_MAX + 1)),
        ("rank3", lambda d: mutate_path(d, ("direct_padded_frame", "ordered_partial_sum_max", "3"), 62_296)),
        ("rank4", lambda d: mutate_path(d, ("direct_padded_frame", "rank4_certified_below_cutoff"), True)),
        ("selector", lambda d: mutate_path(d, ("direct_padded_frame", "ordered_selector_and_root_masks_preserved"), False)),
        ("transport", lambda d: mutate_path(d, ("direct_padded_frame", "actual_error_to_padded_transport_used"), True)),
        ("masked", lambda d: mutate_path(d, ("direct_padded_frame", "masked_diagonal_saturation_rank3_frame_consumed_from_pr1021"), False)),
        ("deletion", lambda d: mutate_path(d, ("direct_padded_frame", "single_column_deletion_injective_on_syzygy_space"), False)),
        ("coloop", lambda d: mutate_path(d, ("direct_padded_frame", "rank2_coloop_possible"), True)),
        ("extra", lambda d: mutate_path(d, ("direct_padded_frame", "distinguished_extra_retained"), False)),
        ("core-cap", lambda d: mutate_path(d, ("direct_padded_frame", "relative_common_core_degree_max"), 62_296)),
        ("F11-order", lambda d: mutate_path(d, ("f11_padding_regression", "cross_order_direct_padded_index"), 3)),
        ("source-keys", lambda d: mutate_path(d, ("signed_source_contract", "forbidden_implies_marked_keys_lower"), FORCED_SOURCE_KEYS - 1)),
        ("credits", lambda d: mutate_path(d, ("signed_source_contract", "signed_occupancy_credits_preserved"), False)),
        ("duplicate", lambda d: mutate_path(d, ("signed_source_contract", "duplicate_source_key_assignment"), True)),
        ("root-count", lambda d: mutate_path(d, ("root_union_route_cut", "independent_resources_fitting"), 5)),
        ("root-close", lambda d: mutate_path(d, ("root_union_route_cut", "independent_per_key_or_layer_root_unions_close_row"), True)),
        ("empty-core-count", lambda d: mutate_path(d, ("support_only_empty_core_route_cut", "zero_sum_block_family", "color_zero_count"), 17_678_834)),
        ("empty-core-overlap", lambda d: mutate_path(d, ("support_only_empty_core_route_cut", "pairwise_selected_agreement_intersection_max"), K - 1)),
        ("empty-core-gcd", lambda d: mutate_path(d, ("support_only_empty_core_route_cut", "triple_deletion_census", "every_extra_and_every_anchor_basis_triple_relative_gcd_empty"), False)),
        ("empty-core-xi", lambda d: mutate_path(d, ("support_only_empty_core_route_cut", "signed_occupancy", "Xi_46"), SAFE_SIGNED_ALLOWANCE)),
        ("empty-core-source", lambda d: mutate_path(d, ("support_only_empty_core_route_cut", "actual_same_received_word_RS_list"), True)),
        ("terminal", lambda d: mutate_path(d, ("semantic_terminals",), ["UNPAID_RANK2_COLOOP"])),
        ("closure", lambda d: mutate_path(d, ("scope_guards", "m31_list_row_closed"), True)),
        ("ledger", lambda d: mutate_path(d, ("scope_guards", "ledger_movement"), 1)),
        ("owner", lambda d: mutate_path(d, ("scope_guards", "owner_charge"), 0)),
        ("source-hash", lambda d: mutate_path(
            d, ("source_sha256", str(NOTE_PATH.relative_to(ROOT))), "0" * 64
        )),
    ]
    rejected = 0
    for label, mutator in mutations:
        candidate = mutator(expected)
        try:
            verify_payload(candidate)
        except (VerificationError, KeyError, TypeError):
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {label}")
    require(rejected == len(mutations), "all mutations rejected")
    print(f"tamper-selftest: PASS ({rejected}/{len(mutations)})")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not (args.write or args.check or args.tamper_selftest):
        args.check = True

    expected = seal(build_payload())
    verify_payload(expected)

    if args.write:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_bytes(canonical_json(expected))
        print(f"wrote {CERTIFICATE_PATH.relative_to(ROOT)}")

    if args.check:
        require(CERTIFICATE_PATH.exists(), "certificate exists")
        actual = json.loads(CERTIFICATE_PATH.read_text())
        verify_payload(actual)
        require(actual == expected, "certificate equals regenerated payload")

    if args.tamper_selftest:
        tamper_selftest(expected)

    print("M31 exact-syzygy coloop elimination and locator route cut: PASS")
    print("direct padded rank3: 62295 < 67447; margin 5152")
    print("padded rank3: CONSUMED FROM PR #1021; rank-two coloop: ELIMINATED")
    print("remaining: UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND")
    print("M31 row: OPEN; ledger movement: 0")
    print(f"checks={CHECKS}")


if __name__ == "__main__":
    main()
