#!/usr/bin/env python3
"""Replay the source-audit form of the finite Role 10 owner-prefix lemma.

Python standard library only. The source A-order is the recursive ordered
state-pair order used by verify_rank16_integer_subcore_owner.py. Exact-F order
is ordinary lexicographic combination order.
"""

from __future__ import annotations

import argparse
import hashlib
import runpy
from collections import defaultdict
from functools import cache
from math import comb
from pathlib import Path


P = 2_130_706_433
N = 2_097_152
K = 1_048_576
M = 1_116_047
B = 32_768
T = 274_854_110_496_187_592

PROFILE_1 = (31, 14, 7, 0, 0, 0)
PROFILE_2 = (31, 15, 6, 2, 1, 0)
PROFILE_3 = (31, 15, 6, 3, 1, 0)
SOURCE_A_RANK = 14_646
C_A = 5_812_512

INHERITED_COMPILER = Path(
    "experimental/scripts/verify_rank16_integer_subcore_owner.py"
)
INHERITED_COMPILER_SHA256 = (
    "fc61a8cbf29abd9ecd4fc9e076576bf2fdea2f276fc4261ba91815f3afe8b571"
)
PR890_HEAD = "a5b98c75d0e3732e9659d8fd220c821329e572e4"
PR890_PATCH_SHA256 = (
    "d967f805d1e70074eced0599a0e70e261d3317047e10ec78e419059156642307"
)


class VerificationError(RuntimeError):
    """Raised when a replay obligation fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def profile_target(
    profile: tuple[int, int, int, int, int, int],
) -> tuple[int, tuple[int, ...]]:
    return profile[0], profile[1:] + (0,)


@cache
def inherited_owner_subtotal() -> int:
    """Rebuild the inherited owner subtotal from its pinned source compiler."""
    repository_root = Path(__file__).resolve().parents[2]
    compiler_path = repository_root / INHERITED_COMPILER
    source = compiler_path.read_bytes()
    require(
        hashlib.sha256(source).hexdigest() == INHERITED_COMPILER_SHA256,
        "pinned inherited compiler hash",
    )
    namespace = runpy.run_path(str(compiler_path))
    values = namespace["replay"]()
    subtotal = int(values["new_paid"])
    require(subtotal == 274_847_747_040_605_072, "inherited owner subtotal")
    return subtotal


@cache
def subtree_states(height: int) -> dict[tuple[int, tuple[int, ...]], int]:
    if height == 0:
        return {(0, ()): 1, (1, ()): 1}

    size = 1 << height
    result: defaultdict[tuple[int, tuple[int, ...]], int] = defaultdict(int)
    children = subtree_states(height - 1)
    for (left_weight, left_counts), left_number in children.items():
        for (right_weight, right_counts), right_number in children.items():
            weight = left_weight + right_weight
            counts = tuple(
                left + right for left, right in zip(left_counts, right_counts)
            ) + (int(weight == size),)
            result[(weight, counts)] += left_number * right_number
    return dict(result)


def combine_states(
    left: tuple[int, tuple[int, ...]],
    right: tuple[int, tuple[int, ...]],
    height: int,
) -> tuple[int, tuple[int, ...]]:
    weight = left[0] + right[0]
    counts = tuple(a + b for a, b in zip(left[1], right[1])) + (
        int(weight == 1 << height),
    )
    return weight, counts


def unrank_source_pattern(
    height: int,
    target: tuple[int, tuple[int, ...]],
    rank: int,
) -> int:
    """Unrank in recursive ordered state-pair, then child-rank order."""
    require(1 <= rank <= subtree_states(height)[target], "source pattern rank")
    if height == 0:
        return target[0]

    children = subtree_states(height - 1)
    for left in sorted(children):
        for right in sorted(children):
            if combine_states(left, right, height) != target:
                continue
            block = children[left] * children[right]
            if rank > block:
                rank -= block
                continue
            left_rank, offset = divmod(rank - 1, children[right])
            left_mask = unrank_source_pattern(height - 1, left, left_rank + 1)
            right_mask = unrank_source_pattern(height - 1, right, offset + 1)
            return left_mask | (right_mask << (1 << (height - 1)))
    raise VerificationError("unreachable source pattern rank")


def selected(mask: int) -> tuple[int, ...]:
    return tuple(index for index in range(64) if mask >> index & 1)


def fixed_state(height: int, offset: int, mask: int) -> tuple[int, tuple[int, ...]]:
    if height == 0:
        return (int(bool(mask >> offset & 1)), ())
    half = 1 << (height - 1)
    left = fixed_state(height - 1, offset, mask)
    right = fixed_state(height - 1, offset + half, mask)
    return combine_states(left, right, height)


def prefix_completion_states(
    height: int,
    offset: int,
    known_until: int,
    mask: int,
) -> dict[tuple[int, tuple[int, ...]], int]:
    """Count states after fixing the contiguous prefix [0, known_until)."""
    end = offset + (1 << height)
    if end <= known_until:
        return {fixed_state(height, offset, mask): 1}
    if offset >= known_until:
        return subtree_states(height)

    half = 1 << (height - 1)
    left = prefix_completion_states(height - 1, offset, known_until, mask)
    right = prefix_completion_states(
        height - 1, offset + half, known_until, mask
    )
    result: defaultdict[tuple[int, tuple[int, ...]], int] = defaultdict(int)
    for left_state, left_number in left.items():
        for right_state, right_number in right.items():
            state = combine_states(left_state, right_state, height)
            result[state] += left_number * right_number
    return dict(result)


def profile_lexicographic_rank(
    target: tuple[int, tuple[int, ...]],
    choice: tuple[int, ...],
) -> int:
    """One-based lexicographic rank among patterns with the exact target state."""
    rank = 1
    prefix_mask = 0
    previous = -1
    for value in choice:
        for candidate in range(previous + 1, value):
            trial_mask = prefix_mask | (1 << candidate)
            states = prefix_completion_states(6, 0, candidate + 1, trial_mask)
            rank += states.get(target, 0)
        prefix_mask |= 1 << value
        previous = value
    return rank


@cache
def congruence_cover_lower_bound(
    q: int,
    residue: int,
    universe: int,
    block_size: int,
    strength: int,
) -> int:
    require(0 < residue < q, "nonzero residue")
    require(0 <= strength <= block_size <= universe, "cover parameters")
    if strength == 0:
        return residue

    previous = congruence_cover_lower_bound(
        q, residue, universe - 1, block_size - 1, strength - 1
    )
    lower = (universe * previous + block_size - 1) // block_size
    target = residue * comb(universe, strength) % q
    coefficient = comb(block_size, strength) % q
    candidate = lower
    while coefficient * candidate % q != target:
        candidate += 1
    return candidate


def minimum_pair_collisions(universe: int, incidences: int) -> int:
    quotient, remainder = divmod(incidences, universe)
    return universe * comb(quotient, 2) + remainder * quotient


def first_at_least_with_congruence(
    lower: int,
    constant: int,
    modulus: int,
) -> int:
    candidate = lower
    while (constant - candidate) % modulus:
        candidate += 1
    return candidate


def replay(mutation: str = "none") -> dict[str, object]:
    agreement_residual = M - 31 * B
    intersection_cap = K - 1 - 31 * B
    require(agreement_residual == 100_239, "agreement residual")
    require(intersection_cap == 32_767, "intersection cap")

    core25_universe = 8 * B
    core25_forced = minimum_pair_collisions(
        core25_universe, 12 * agreement_residual
    )
    core25_allowed = comb(12, 2) * intersection_cap
    if mutation == "cap25":
        core25_allowed += 30_000
    require(core25_forced > core25_allowed, "fixed-25 cap 11")

    core26_universe = 7 * B
    core26_forced = minimum_pair_collisions(
        core26_universe, 6 * agreement_residual
    )
    core26_allowed = comb(6, 2) * intersection_cap
    if mutation == "cap26":
        core26_allowed += 24_000
    require(core26_forced > core26_allowed, "fixed-26 cap 5")

    l52 = congruence_cover_lower_bound(5, 2, 33, 23, 20)
    l31 = congruence_cover_lower_bound(3, 1, 33, 24, 22)
    if mutation == "recurrence":
        l52 += 1
    require(l52 == 647_885, "L_5,2(33,23,20)")
    require(l31 == 721_232, "L_3,1(33,24,22)")

    delta27_lower = (3 * comb(33, 10) + 6 * l52 + 299) // 300
    delta27 = first_at_least_with_congruence(
        delta27_lower, 11 * comb(33, 8), 351
    )
    cap27 = (11 * comb(33, 8) - delta27) // 351
    require(delta27 == 938_574, "fixed-27 exact-A deficit")
    require(cap27 == 432_442, "fixed-27 exact-A cap")

    delta26_lower = (comb(33, 9) + 2 * l31 + 24) // 25
    delta26 = first_at_least_with_congruence(
        delta26_lower, 11 * comb(33, 8), 26
    )
    cap26 = (11 * comb(33, 8) - delta26) // 26
    require(delta26 == 1_600_404, "fixed-26 exact-A deficit")
    require(cap26 == C_A, "fixed-26 exact-A cap")

    target = profile_target(PROFILE_3)
    source_mask = unrank_source_pattern(6, target, SOURCE_A_RANK)
    source_pattern = selected(source_mask)
    source_lex_rank = profile_lexicographic_rank(target, source_pattern)
    expected_lex_rank = 592_047 + int(mutation == "a-rank-order")
    require(source_lex_rank == expected_lex_rank, "source/lex A-order separation")

    profile_counts = {
        profile: subtree_states(6)[profile_target(profile)]
        for profile in (PROFILE_1, PROFILE_2, PROFILE_3)
    }
    require(profile_counts[PROFILE_1] == 6_684_672, "profile 1 census")
    require(profile_counts[PROFILE_2] == 7_833_600, "profile 2 census")
    require(profile_counts[PROFILE_3] == 783_360, "profile 3 census")

    inherited_paid = inherited_owner_subtotal()
    if mutation == "owner-total":
        inherited_paid += 1
    pre_f_paid = (
        inherited_paid
        + profile_counts[PROFILE_1] * cap27
        + profile_counts[PROFILE_2] * cap27
        + 14_645 * cap26
        + 15
    )
    n_f, n_f_remainder = divmod(T - 1 - pre_f_paid, 5)
    require(n_f_remainder == 0, "integral exact-F prefix")
    require(n_f == 4_152_808, "derived exact-F prefix")

    q_f_numerator = 5 * n_f - 3 * C_A + 1
    q_f, q_f_remainder = divmod(q_f_numerator, 5)
    require(q_f_remainder == 0, "integral terminal exact-F rank")
    require(q_f == 665_301, "derived terminal exact-F rank")

    exact_f_bucket_count = comb(33, 26)
    if mutation == "rank-domain":
        exact_f_bucket_count = n_f
    require(n_f + 1 <= exact_f_bucket_count, "R0 exact-F domain")
    require(q_f + 1 <= exact_f_bucket_count, "R3 exact-F domain")

    owner_stages = (
        profile_counts[PROFILE_1] * cap27,
        profile_counts[PROFILE_2] * cap27,
        14_645 * cap26,
        n_f * 5,
        15,
    )
    appended_paid = sum(owner_stages)
    owner_total = inherited_paid + appended_paid
    require(appended_paid == 6_363_455_582_519, "appended owner subtotal")
    require(owner_total == T - 1, "owner total T-1")

    residual_q_f = q_f + int(mutation == "residual-identity")
    residual_floor = 3 * C_A + 5 * residual_q_f - 1
    require(residual_floor == 5 * n_f, "same-word residual identity")

    vacancy_margin_through_665300 = 5 * n_f - (3 * C_A + 5 * (q_f - 1))
    allowance_margin_through_665301 = (
        5 * n_f + 1 - (3 * C_A + 5 * q_f)
    )
    overflow_at_665302 = 3 * C_A + 5 * (q_f + 1) - (5 * n_f + 1)
    require(vacancy_margin_through_665300 == 4, "665300 vacancy margin")
    require(allowance_margin_through_665301 == 0, "665301 allowance margin")
    require(overflow_at_665302 == 5, "665302 overflow")

    return {
        "agreement_residual": agreement_residual,
        "intersection_cap": intersection_cap,
        "core25_margin": core25_forced - core25_allowed,
        "core26_margin": core26_forced - core26_allowed,
        "L_5_2_33_23_20": l52,
        "L_3_1_33_24_22": l31,
        "fixed27_deficit": delta27,
        "fixed27_cap": cap27,
        "fixed26_deficit": delta26,
        "fixed26_cap": cap26,
        "source_A_rank": SOURCE_A_RANK,
        "ordinary_lex_rank": source_lex_rank,
        "profile_1_patterns": profile_counts[PROFILE_1],
        "profile_2_patterns": profile_counts[PROFILE_2],
        "profile_3_patterns": profile_counts[PROFILE_3],
        "inherited_compiler_sha256": INHERITED_COMPILER_SHA256,
        "pr890_head": PR890_HEAD,
        "pr890_patch_sha256": PR890_PATCH_SHA256,
        "inherited_paid": inherited_owner_subtotal(),
        "derived_exact_F_prefix": n_f,
        "derived_terminal_exact_F_rank": q_f,
        "exact_F_bucket_count": exact_f_bucket_count,
        "source_pattern": source_pattern,
        "appended_paid": appended_paid,
        "owner_total": owner_total,
        "residual_floor": residual_floor,
        "vacancy_margin_through_665300": vacancy_margin_through_665300,
        "allowance_margin_through_665301": allowance_margin_through_665301,
        "overflow_at_665302": overflow_at_665302,
        "next_payment_wall": (14_649, q_f + 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        default="none",
        choices=(
            "none",
            "a-rank-order",
            "rank-domain",
            "cap25",
            "cap26",
            "recurrence",
            "owner-total",
            "residual-identity",
        ),
    )
    parser.add_argument("--self-test-mutations", action="store_true")
    args = parser.parse_args()
    if args.self_test_mutations:
        mutations = (
            "a-rank-order",
            "rank-domain",
            "cap25",
            "cap26",
            "recurrence",
            "owner-total",
            "residual-identity",
        )
        for mutation in mutations:
            try:
                replay(mutation)
            except VerificationError:
                print(f"MUTATION_CAUGHT={mutation}")
            else:
                raise VerificationError(f"mutation survived: {mutation}")
        print("ALL_MUTATIONS_CAUGHT")
        return
    values = replay(args.mutation)

    print("R31_ROLE10_SOURCE_OWNER_PREFIX_REPLAY")
    for key, value in values.items():
        print(f"{key}={value}")
    print("ALL_CHECKS_PASSED")


if __name__ == "__main__":
    main()
