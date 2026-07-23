#!/usr/bin/env sage
"""Independent Sage replay for the M31 rank-seven route cut."""

from itertools import combinations
import json


P = 2^31 - 1
N = 2^21
K = 2^20
A = 1116023
T = N - A
W = A - K
B_STAR = 2^24 - 1
DEEP_CAP = 1001282
L = B_STAR - DEEP_CAP
TARGET = L - 1
RANK = 7
G_MIN = W + RANK
G_MAX = A
D6_MIN = N - K + 6
D_TURN = 1177354

checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


def fall(x, r):
    out = ZZ(1)
    for i in range(r):
        out *= x - i
    return out


def prod(values):
    out = ZZ(1)
    for value in values:
        out *= value
    return out


def B(k):
    return ZZ(binomial((N-K)+k, k) // binomial(W+k, k))


def raw_q6(g, k):
    fixed = L*g*prod(W+j for j in range(k+1, 6))
    return B(k)*fall(T+g, 7-k) // fixed - (W+6)


def q6_envelope(g):
    raw, winner = min((raw_q6(g, k), k) for k in range(1, 6))
    strict = g-W-7
    return min(raw, strict), winner, raw, strict


def pi(d, b):
    return (d-T+b)*prod(W+i+b for i in range(1, 6))


def old(d):
    return QQ(fall(d, 6))/pi(d, 0)


def new(d, g):
    e = T+g-d
    require(e >= 1, "positive support layer")
    return QQ(fall(d, 7))/((W+1)*pi(d, e))


def codim_majorant(g, q):
    dmax = D6_MIN+q
    low_d = min(D_TURN, dmax)
    low = old(D6_MIN)+new(low_d, g)
    if dmax < D_TURN:
        return low, low, "LOW_PIECE"
    high = old(dmax)+new(dmax, g)
    if high >= low:
        return high, low, "HIGH_ENDPOINT"
    return low, low, "LOW_PIECE"


require((T, W, L) == (981129, 67447, 15775933), "deployed constants")
require([B(k) for k in range(7)] == [1,15,241,3757,58410,908021,14115528],
        "fiber caps")

transitions = []
last_winner = None
winner_counts = {}
qmax = -1
qmax_points = []
minimum_margin = 10^30
for g in range(G_MIN, G_MAX+1):
    q, winner, raw, strict = q6_envelope(g)
    winner_counts[winner] = winner_counts.get(winner, 0)+1
    if winner != last_winner:
        transitions.append((g, winner, raw))
        last_winner = winner
    if q > qmax:
        qmax = q
        qmax_points = [g]
    elif q == qmax:
        qmax_points.append(g)
    margin = 5*(W+1)-((D6_MIN+q)-T)
    minimum_margin = min(minimum_margin, margin)
    require(margin >= 0, "interpolation margin")

require(transitions == [(67454,1,837776),(76877,5,770616)], "winner transitions")
require(winner_counts == {1:9423,5:1039147}, "winner histogram")
require(qmax == 242225, "q6 maximum")
require(qmax_points == [309679,309680,309681], "q6 plateau")
require(minimum_margin == 27562, "minimum interpolation margin")

last_johnson_paid = None
first_nonpositive = None
last_codim_unpaid = None
first_codim_paid = None
records = {}
for g in range(G_MIN, G_MAX+1):
    denominator = g^2-(T+g)*(g-W-1)
    jcap = None if denominator <= 0 else (T+g)*(W+1)//denominator
    if jcap is not None and jcap <= TARGET:
        last_johnson_paid = (g, jcap)
    elif first_nonpositive is None:
        first_nonpositive = (g, denominator)

    q, _, _, _ = q6_envelope(g)
    value, low, owner = codim_majorant(g, q)
    floor_value = floor(value)
    if floor_value <= TARGET and first_codim_paid is None:
        first_codim_paid = (g, floor_value)
    if floor_value > TARGET:
        last_codim_unpaid = (g, floor_value)
    if g in [72427,72428,354998,354999]:
        records[g] = (jcap, q, floor(low), floor_value, owner)

require(last_johnson_paid == (72427,4735771), "Johnson transition paid")
require(first_nonpositive == (72428,-898676), "Johnson transition failed")
require(last_codim_unpaid == (354998,15776141), "last codim failure")
require(first_codim_paid == (354999,15775924), "first codim payment")
require(records[354998][2] == 14336564, "last low-piece majorant")
require(records[354999][2] == 14336558, "first low-piece majorant")

# Exact source-orientation control.  For RS(GF(11),11,7) and u(x)=x^7,
# every seven-subset gives one distinct degree-<7 codeword with exactly seven
# agreements.  The truncated-weight inequality is sharp for every k.
F = GF(11)
PR.<x> = PolynomialRing(F)
D = list(F)
u = x^7
words = []
for support in combinations(D, 7):
    locator = prod(x-alpha for alpha in support)
    c = u-locator
    require(c.degree() < 7, "toy codeword degree")
    agreements = sum(1 for alpha in D if c(alpha) == u(alpha))
    require(agreements == 7, "toy exact agreement")
    words.append(c)

require(len(words) == binomial(11,7) == 330, "toy list size")
require(len(set(words)) == 330, "toy words distinct")
rows = [vector(F, [c[i] for i in range(7)]) for c in words]
require(matrix(F, rows).rank() == 7, "toy codeword span rank seven")

toy_weights = [4+j for j in range(1,8)]
for k in range(7):
    left = 330*prod(toy_weights[j-1]-4 for j in range(k+1,8))
    toy_B = binomial(4+k,k)
    right = toy_B*fall(11,7-k)
    require(left == right, "toy truncated inequality equality k=%s" % k)

summary = {
    "schema": "m31-rank7-truncated-weight-flag-sage-v1",
    "checks": int(checks),
    "deployed": {
        "union_values": int(G_MAX-G_MIN+1),
        "fiber_caps": [int(B(k)) for k in range(7)],
        "winner_transitions": [[int(v) for v in row] for row in transitions],
        "maximum_q6": int(qmax),
        "maximum_q6_unions": [int(v) for v in qmax_points],
        "minimum_interpolation_margin": int(minimum_margin),
        "last_johnson_paid": [int(v) for v in last_johnson_paid],
        "first_johnson_nonpositive": [int(v) for v in first_nonpositive],
        "last_codim_unpaid": [int(v) for v in last_codim_unpaid],
        "first_codim_paid": [int(v) for v in first_codim_paid],
    },
    "toy_gf11": {
        "list_size": len(words),
        "span_rank": int(matrix(F, rows).rank()),
        "generalized_weights": [int(v) for v in toy_weights],
        "truncated_equalities": int(7),
        "scope": "EXACT_ORIENTATION_AND_SHARPNESS_CONTROL_ONLY",
    },
    "impact": {
        "rank7_closed": False,
        "row_closed": False,
        "ledger_movement": int(0),
    },
}

print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
