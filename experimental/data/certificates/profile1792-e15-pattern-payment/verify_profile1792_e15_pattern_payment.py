#!/usr/bin/env python3
"""Exact nested-pattern payment for 110 Profile1792 residual cells."""

from collections import defaultdict
from math import comb


T = 274_854_110_496_187_592
U_DYADIC = 57_121_027_290_597_096
OLD_CAP = 121_502_836_610_262
TOTAL_PROFILES = 1_792


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


# A state is (leaf weight, all-one counts at sizes 2,4,...,2^height).
# Ordered children retain the literal 64-leaf fiber patterns.
states: dict[tuple[int, tuple[int, ...]], int] = {(0, ()): 1, (1, ()): 1}
for height in range(1, 7):
    size = 1 << height
    nxt: defaultdict[tuple[int, tuple[int, ...]], int] = defaultdict(int)
    for (left_weight, left_counts), left_number in states.items():
        for (right_weight, right_counts), right_number in states.items():
            weight = left_weight + right_weight
            counts = tuple(
                a + b for a, b in zip(left_counts, right_counts)
            ) + (int(weight == size),)
            nxt[(weight, counts)] += left_number * right_number
    states = dict(nxt)

check(
    sum(number for (weight, _), number in states.items() if weight == 32)
    == comb(64, 32),
    "64-leaf weight-32 census",
)

rows: list[tuple[tuple[int, int, int, int, int, int], int]] = []
for (weight, counts), number in states.items():
    if weight != 32:
        continue
    e16, e17, e18, e19, e20, _e21 = counts
    if e16 <= 15 and e17 <= 7 and e18 <= 3 and e19 <= 1 and e20 == 0:
        rows.append(((32, e16, e17, e18, e19, e20), number))

check(len(rows) == 166, "residual e15=32 profile count")
check(
    sum(number for _, number in rows) == comb(64, 32) - 601_080_390,
    "residual e15=32 pattern total",
)

paid = [(profile, number) for profile, number in rows if number <= OLD_CAP]
unpaid = [(profile, number) for profile, number in rows if number > OLD_CAP]

check(len(paid) == 110, "paid profile count")
check(len(unpaid) == 56, "unpaid e15=32 profile count")

paid_total = sum(number for _, number in paid)
check(paid_total == 904_093_061_906_432, "paid exact aggregate")

saving = len(paid) * OLD_CAP - paid_total
check(saving == 12_461_218_965_222_388, "uniform-budget saving")

remaining_profiles = TOTAL_PROFILES - len(paid)
check(remaining_profiles == 1_682, "remaining profile count")

new_cap, closing_margin = divmod(T - U_DYADIC - paid_total, remaining_profiles)
check(new_cap == 128_911_409_122_285, "relaxed remaining-profile cap")
check(closing_margin == 694, "new closing margin")
check(
    U_DYADIC + paid_total + remaining_profiles * new_cap
    == T - closing_margin,
    "closing ledger",
)

largest_profile, largest_count = max(rows, key=lambda item: item[1])
smallest_unpaid_profile, smallest_unpaid_count = min(
    unpaid, key=lambda item: item[1]
)
check(largest_profile == (32, 8, 1, 0, 0, 0), "largest profile label")
check(largest_count == 247_029_899_691_294_720, "largest pattern count")
check(
    smallest_unpaid_profile == (32, 13, 3, 0, 0, 0),
    "smallest unpaid profile label",
)
check(
    smallest_unpaid_count == 170_870_483_976_192,
    "smallest unpaid pattern count",
)

print("PROFILE1792_E15_32_PATTERN_PAYMENT: PASS")
print(f"residual_e15_32_profiles={len(rows)}")
print(f"paid_profiles={len(paid)} unpaid_e15_32_profiles={len(unpaid)}")
print(f"paid_exact_aggregate={paid_total}")
print(f"uniform_budget_saving={saving}")
print(f"remaining_all_profiles={remaining_profiles}")
print(f"relaxed_uniform_cap={new_cap}")
print(f"closing_margin={closing_margin}")
print(f"largest_profile={largest_profile} count={largest_count}")
print(
    f"smallest_unpaid_profile={smallest_unpaid_profile} "
    f"count={smallest_unpaid_count}"
)
