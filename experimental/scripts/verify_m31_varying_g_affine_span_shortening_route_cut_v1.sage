#!/usr/bin/env sage
"""Independent Sage replay of the M31 affine-span/shortening arithmetic.

This file deliberately does not import the Python verifier.  It recomputes
the deployed binomial thresholds, endpoint incidence caps, and adjacent-row
shortening ceilings with Sage integers.
"""

import json


P = Integer(2)^31 - 1
N = Integer(2)^21
K = Integer(2)^20
A = Integer(1116023)
R = N - A
W = A - K
B = Integer(2)^24 - 1
TARGET = B - 1
L = Integer(15775933)
S_MAX = Integer(366886)


def require(condition, label):
    if not bool(condition):
        raise RuntimeError(label)


def incidence_cap(v, a, lam):
    delta = a*a - v*lam
    require(delta > 0, "positive incidence denominator")
    numerator = v*(a-lam)
    return {
        "delta": delta,
        "cap": numerator // delta,
        "remainder": numerator % delta,
    }


def zero_cap(rank, g):
    return binomial(R+g, rank) // binomial(W+rank, rank)


def first_g(rank):
    lo = W + rank
    hi = A
    while lo < hi:
        mid = (lo+hi)//2
        if zero_cap(rank, mid) >= L:
            hi = mid
        else:
            lo = mid+1
    return lo


def excess(rank):
    budget = binomial(N, rank)
    cost = lambda s: binomial(W+s+rank, rank)
    lo = Integer(0)
    hi = S_MAX
    while lo < hi:
        mid = (lo+hi+1)//2
        if L*cost(mid) <= budget:
            lo = mid
        else:
            hi = mid-1
    q = lo
    if q == S_MAX:
        u = Integer(0)
    else:
        u = min(L-1, (budget-L*cost(q)) // binomial(W+q+rank, rank-1))
    return q, u, L*q+u


def shorten(m, d, s):
    local = incidence_cap(R-s, m-s, d-s-1)
    pull = (binomial(R, s)*local["cap"]) // binomial(m, s)
    return local["delta"], local["cap"], pull


def puncture_errors(m, d, s):
    local = incidence_cap(R-s, m, d-1)
    pull = (binomial(R, s)*local["cap"]) // binomial(R-m, s)
    return local["delta"], local["cap"], pull


require((P, N, K, A, R, W, B) == (
    2147483647, 2097152, 1048576, 1116023, 981129, 67447, 16777215),
    "deployed parameters")

rank_caps = [zero_cap(r, A) for r in (1, 2, 3, 4)]
require(rank_caps == [31, 966, 30058, 934551], "rank caps")

g5 = first_g(5)
g6 = first_g(6)
require((g5, zero_cap(5, g5-1), zero_cap(5, g5)) ==
        (874886, 15775899, 15775941), "rank-five threshold")
require((g6, zero_cap(6, g6-1), zero_cap(6, g6)) ==
        (87070, 15775873, 15775962), "rank-six threshold")

excess_rows = [excess(r) for r in range(5, 12)]
require([row[0] for row in excess_rows[:6]] ==
        [8763, 64972, 129040, 196716, 265094, 332335], "excess bases")
require([row[1] for row in excess_rows[:6]] ==
        [3950411, 8496922, 11542946, 3995011, 1499656, 3785452],
        "excess one-step counts")
require([row[2] for row in excess_rows[:6]] == [
    138248451290, 1025002415798, 2035737937266,
    3103382431039, 4182106682358, 5242898479007],
    "excess ceilings")
require(excess_rows[-1][0] == S_MAX, "rank eleven no cut")

lower = incidence_cap(R-1, 72858, 5410)
require(lower == {"delta": 385684, "cap": 171578, "remainder": 231992},
        "lower endpoint local cap")
lower_cap = (R*lower["cap"]) // 72859
require(lower_cap == 2310492, "lower endpoint cap")

upper_shell = incidence_cap(R-1, 908270, 840822)
require(upper_shell == lower, "upper shell local cap")
shell_cap = (R*upper_shell["cap"]) // 72859
upper_tail = incidence_cap(R, 908271, 840822)
require(upper_tail["delta"] == 1361403 and upper_tail["cap"] == 48608,
        "upper endpoint tail")
require(shell_cap + upper_tail["cap"] == 2359100, "upper endpoint total")

lower_adjacent = [shorten(72860, 5413, s) for s in range(2, 7)]
upper_adjacent = [puncture_errors(908269, 840822, s) for s in range(2, 7)]
require(lower_adjacent == upper_adjacent, "adjacent symmetry")
require([row[2] for row in lower_adjacent] == [
    30682450, 131171396, 1049845524, 10057621549, 105113431231],
    "adjacent ceilings")
require(R > 13*72860 and 13^7 > TARGET, "large-s obstruction")

summary = {
    "schema": "m31-varying-g-affine-span-shortening-route-cut-sage-v1",
    "status": "EXACT_INDEPENDENT_ARITHMETIC_REPLAY",
    "rank_caps_1_4": rank_caps,
    "rank_5_threshold": [g5, zero_cap(5, g5-1), zero_cap(5, g5)],
    "rank_6_threshold": [g6, zero_cap(6, g6-1), zero_cap(6, g6)],
    "excess_rows_5_11": [list(row) for row in excess_rows],
    "fixed_G_new_interval_m": [72860, 908269],
    "lower_endpoint_cap": lower_cap,
    "upper_endpoint_cap": shell_cap + upper_tail["cap"],
    "adjacent_pullback_caps": [row[2] for row in lower_adjacent],
    "ledger_movement": 0,
    "row_closed": False,
    "terminal": "UNPAID_HIGH_AFFINE_RANK_SPLIT_RATIONAL_INCIDENCE",
}
print(json.dumps(summary, sort_keys=True, default=int))
