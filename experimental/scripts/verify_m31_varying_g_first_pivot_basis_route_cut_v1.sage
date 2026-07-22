#!/usr/bin/env sage
"""Independent Sage replay for the M31 first-pivot basis route cut.

This verifier does not import the primary Python implementation.  It
recomputes the deployed integer thresholds and excess envelopes, then
constructs and audits the exact GF(17) rank-twelve split-rational family.
The finite-field family is a toy sharpness control, not a deployed bound.
"""

import hashlib
import json
from itertools import combinations, product


# Deployed Mersenne-31 row.
P = Integer(2)^31 - 1
N = Integer(2)^21
K = Integer(2)^20
A = Integer(1116023)
R = N - A
W = A - K
B_STAR = Integer(2)^24 - 1
DEEP_CAP = Integer(1001282)
L = B_STAR - DEEP_CAP
S_MAX = Integer(366886)
M0 = W + 1

CHECKS = 0


def require(condition, label):
    global CHECKS
    CHECKS += 1
    if not bool(condition):
        raise RuntimeError(label)


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
        default=int,
    )


def falling(value, length):
    value = Integer(value)
    length = Integer(length)
    require(length >= 0 and value >= length, "legal falling factorial")
    answer = Integer(1)
    for offset in range(int(length)):
        answer *= value - offset
    return answer


def choose4(value):
    value = Integer(value)
    require(value >= 4, "legal fourth binomial")
    return value * (value-1) * (value-2) * (value-3) // 24


def first_pivot_cap(rank, union_size, common_e=0):
    rank = Integer(rank)
    union_size = Integer(union_size)
    common_e = Integer(common_e)
    numerator = falling(R + union_size - common_e, rank)
    denominator = union_size * falling(W + rank + common_e - 1, rank-1)
    return numerator // denominator


def endpoint_rank_cap(rank):
    low_g = W + rank
    low = first_pivot_cap(rank, low_g)
    high = first_pivot_cap(rank, A)
    if low >= high:
        maximum, endpoint = low, "LOW"
    else:
        maximum, endpoint = high, "HIGH"
    return {
        "rank": int(rank),
        "low_union": int(low_g),
        "low_cap": int(low),
        "high_union": int(A),
        "high_cap": int(high),
        "maximum_cap": int(maximum),
        "maximizing_endpoint": endpoint,
    }


def first_true(lo, hi, predicate, label):
    lo = Integer(lo)
    hi = Integer(hi)
    require(lo <= hi and predicate(hi), label + " endpoint")
    while lo < hi:
        middle = (lo + hi) // 2
        if predicate(middle):
            hi = middle
        else:
            lo = middle + 1
    return lo


def affine_line_cap(union_size):
    union_size = Integer(union_size)
    effective_n = R + union_size
    numerator = 15 * effective_n * binomial(effective_n-1, 4)
    denominator = union_size * binomial(W+5, 4)
    return numerator // denominator


def cross_min_product(union_size):
    union_size = Integer(union_size)
    require(union_size > R, "cross product active branch")
    return min((union_size-M0)*M0, (union_size-R)*R)


def cross_block_cap(union_size):
    union_size = Integer(union_size)
    effective_n = R + union_size
    numerator = union_size * R * binomial(effective_n-2, 4)
    denominator = cross_min_product(union_size) * binomial(W+4, 4)
    return numerator // denominator


def deployed_thresholds():
    rank_caps = [endpoint_rank_cap(rank) for rank in range(1, 6)]
    require(rank_caps == [
        {"rank": 1, "low_union": 67448, "low_cap": 15,
         "high_union": 1116023, "high_cap": 1,
         "maximum_cap": 15, "maximizing_endpoint": "LOW"},
        {"rank": 2, "low_union": 67449, "low_cap": 241,
         "high_union": 1116023, "high_cap": 58,
         "maximum_cap": 241, "maximizing_endpoint": "LOW"},
        {"rank": 3, "low_union": 67450, "low_cap": 3757,
         "high_union": 1116023, "high_cap": 1816,
         "maximum_cap": 3757, "maximizing_endpoint": "LOW"},
        {"rank": 4, "low_union": 67451, "low_cap": 58410,
         "high_union": 1116023, "high_cap": 56483,
         "maximum_cap": 58410, "maximizing_endpoint": "LOW"},
        {"rank": 5, "low_union": 67452, "low_cap": 908021,
         "high_union": 1116023, "high_cap": 1756141,
         "maximum_cap": 1756141, "maximizing_endpoint": "HIGH"},
    ], "full rank one through five endpoint rows")
    require(all(row["maximum_cap"] < L for row in rank_caps),
            "rank one through five excluded")

    first_g = first_true(
        max(W+6, R//5), A,
        lambda g: first_pivot_cap(6, g) >= L,
        "rank-six first-pivot threshold",
    )
    first_threshold = {
        "first_union_not_excluded": int(first_g),
        "predecessor_cap": int(first_pivot_cap(6, first_g-1)),
        "threshold_cap": int(first_pivot_cap(6, first_g)),
    }
    require(first_threshold == {
        "first_union_not_excluded": 520449,
        "predecessor_cap": 15775901,
        "threshold_cap": 15775934,
    }, "rank-six first-pivot values")

    line_g = first_true(
        200000, A,
        lambda g: affine_line_cap(g) >= L,
        "rank-six affine-line threshold",
    )
    line_threshold = {
        "first_union_not_excluded": int(line_g),
        "predecessor_cap": int(affine_line_cap(line_g-1)),
        "threshold_cap": int(affine_line_cap(line_g)),
    }
    require(line_threshold == {
        "first_union_not_excluded": 781458,
        "predecessor_cap": 15775916,
        "threshold_cap": 15775941,
    }, "rank-six affine-line values")

    first_closed = first_true(
        R+1, R+M0,
        lambda g: cross_block_cap(g) < L,
        "rank-six cross-block threshold",
    )
    cross_threshold = {
        "last_union_not_excluded": int(first_closed-1),
        "last_cap": int(cross_block_cap(first_closed-1)),
        "first_closed_union": int(first_closed),
        "first_closed_cap": int(cross_block_cap(first_closed)),
        "high_endpoint_cap": int(cross_block_cap(A)),
    }
    require(cross_threshold == {
        "last_union_not_excluded": 1033227,
        "last_cap": 15776172,
        "first_closed_union": 1033228,
        "first_closed_cap": 15775916,
        "high_endpoint_cap": 14468798,
    }, "rank-six cross-block values")

    return {
        "rank_1_through_5": rank_caps,
        "rank6_first_pivot": first_threshold,
        "rank6_affine_line": line_threshold,
        "rank6_cross_block": cross_threshold,
        "rank6_surviving_union_interval": [781458, 1033227],
    }


def find_base_excess(budget, weight):
    if L*weight(0) > budget:
        return Integer(-1)
    if L*weight(S_MAX) <= budget:
        return S_MAX
    lo = Integer(0)
    hi = S_MAX
    while lo < hi:
        middle = (lo+hi+1)//2
        if L*weight(middle) <= budget:
            lo = middle
        else:
            hi = middle-1
    return lo


def adjust_base_excess(budget, weight, base):
    if L*weight(0) > budget:
        return Integer(-1)
    base = min(max(Integer(base), Integer(0)), S_MAX)
    while base > 0 and L*weight(base) > budget:
        base -= 1
    while base < S_MAX and L*weight(base+1) <= budget:
        base += 1
    return base


def balanced_total(budget, weight, base):
    base = adjust_base_excess(budget, weight, base)
    if base < 0:
        return Integer(-1), base, Integer(0)
    require(L*weight(base) <= budget, "balanced base feasible")
    if base == S_MAX:
        return L*S_MAX, base, Integer(0)
    require(L*weight(base+1) > budget, "balanced base maximal")
    marginal = weight(base+1)-weight(base)
    require(marginal > 0, "balanced marginal positive")
    raised = (budget-L*weight(base)) // marginal
    require(0 <= raised < L, "balanced raised range")
    return L*base+raised, base, raised


def rank6_combined_excess():
    lower = Integer(781458)
    upper = Integer(1033227)
    line_cache = {}
    cross_cache = {}

    def line_weight(g, excess):
        excess = Integer(excess)
        key = int(excess)
        if key not in line_cache:
            line_cache[key] = binomial(W+excess+5, 4)
        return (g+excess)*line_cache[key]

    def cross_weight(g, excess):
        excess = Integer(excess)
        key = int(excess)
        if key not in cross_cache:
            cross_cache[key] = binomial(W+excess+4, 4)
        # Exact endpoint m=R-s from m+s<=R on the active g>R branch.
        return (g-R+excess)*R*cross_cache[key]

    line_q = Integer(0)
    cross_q = S_MAX
    best = None
    for g_int in range(int(lower), int(upper)+1):
        g = Integer(g_int)
        effective_n = R+g
        line_budget = 15*effective_n*choose4(effective_n-1)
        lw = lambda s, gg=g: line_weight(gg, s)
        if g == lower:
            line_q = find_base_excess(line_budget, lw)
        line_total, line_q, line_raised = balanced_total(
            line_budget, lw, line_q)

        if g <= R:
            cross_total = L*S_MAX
            cross_raised = Integer(0)
        else:
            cross_budget = g*R*choose4(effective_n-2)
            cw = lambda s, gg=g: cross_weight(gg, s)
            if g == R+1:
                cross_q = find_base_excess(cross_budget, cw)
            cross_total, cross_q, cross_raised = balanced_total(
                cross_budget, cw, cross_q)

        combined = min(line_total, cross_total)
        row = (
            combined, g, line_total, cross_total,
            line_q, line_raised, cross_q, cross_raised,
        )
        if best is None or combined > best[0]:
            best = row

    expected = (
        Integer(96161189784), Integer(1009364),
        Integer(96161189784), Integer(96162018632),
        Integer(6095), Integer(6878149),
        Integer(6095), Integer(7706997),
    )
    require(best == expected, "corrected rank-six combined excess maximum")
    return {
        "total_excess_ceiling": int(best[0]),
        "maximizing_union": int(best[1]),
        "line_ceiling": int(best[2]),
        "cross_ceiling": int(best[3]),
        "line_base_excess": int(best[4]),
        "line_entries_raised": int(best[5]),
        "cross_base_excess": int(best[6]),
        "cross_entries_raised": int(best[7]),
        "union_values_exhausted": int(upper-lower+1),
        "cross_endpoint": "m=R-s",
    }


def high_rank_excess(rank):
    rank = Integer(rank)
    require(7 <= rank <= 12, "high-rank excess range")
    first_g = W+rank
    last_g = A
    coefficient_cache = {}

    def coefficient(excess):
        key = int(excess)
        if key not in coefficient_cache:
            coefficient_cache[key] = binomial(W+excess+rank-1, rank-1)
        return coefficient_cache[key]

    def weight(g, excess):
        excess = Integer(excess)
        return (g+excess)*coefficient(excess)

    effective_n = R+first_g
    budget = rank*binomial(effective_n, rank)
    q = find_base_excess(budget, lambda s: weight(first_g, s))
    best = None
    first_full = None
    for g_int in range(int(first_g), int(last_g)+1):
        g = Integer(g_int)
        if g != first_g:
            # rank*C(n,r), updated from n-1 to n.
            previous_n = R+g-1
            budget = budget*(previous_n+1)//(previous_n+1-rank)
        total, q, raised = balanced_total(
            budget, lambda s, gg=g: weight(gg, s), q)
        if q == S_MAX and first_full is None:
            first_full = g
        row = (total, g, q, raised)
        if best is None or total > best[0]:
            best = row

    return {
        "rank": int(rank),
        "total_excess_ceiling": int(best[0]),
        "maximizing_union": int(best[1]),
        "base_excess_q": int(best[2]),
        "entries_raised_to_q_plus_1": int(best[3]),
        "uniform_cut": bool(best[0] < L*S_MAX),
        "first_union_permitting_full_shallow_ceiling": (
            int(first_full) if first_full is not None else -1),
        "union_values_exhausted": int(last_g-first_g+1),
    }


def deployed_excess_sweeps():
    rank6 = rank6_combined_excess()
    high = [high_rank_excess(rank) for rank in range(7, 13)]
    require(high == [
        {"rank": 7, "total_excess_ceiling": 1230614224136,
         "maximizing_union": 1116023, "base_excess_q": 78005,
         "entries_raised_to_q_plus_1": 12570471, "uniform_cut": True,
         "first_union_permitting_full_shallow_ceiling": -1,
         "union_values_exhausted": 1048570},
        {"rank": 8, "total_excess_ceiling": 2269797172033,
         "maximizing_union": 1116023, "base_excess_q": 143877,
         "entries_raised_to_q_plus_1": 3259792, "uniform_cut": True,
         "first_union_permitting_full_shallow_ceiling": -1,
         "union_values_exhausted": 1048569},
        {"rank": 9, "total_excess_ceiling": 3348220234408,
         "maximizing_union": 1116023, "base_excess_q": 212235,
         "entries_raised_to_q_plus_1": 15094153, "uniform_cut": True,
         "first_union_permitting_full_shallow_ceiling": -1,
         "union_values_exhausted": 1048568},
        {"rank": 10, "total_excess_ceiling": 4424565157287,
         "maximizing_union": 1116023, "base_excess_q": 280462,
         "entries_raised_to_q_plus_1": 15436241, "uniform_cut": True,
         "first_union_permitting_full_shallow_ceiling": -1,
         "union_values_exhausted": 1048567},
        {"rank": 11, "total_excess_ceiling": 5474137140842,
         "maximizing_union": 1116023, "base_excess_q": 346992,
         "entries_raised_to_q_plus_1": 14597306, "uniform_cut": True,
         "first_union_permitting_full_shallow_ceiling": -1,
         "union_values_exhausted": 1048566},
        {"rank": 12, "total_excess_ceiling": 5787968954638,
         "maximizing_union": 909846, "base_excess_q": 366886,
         "entries_raised_to_q_plus_1": 0, "uniform_cut": False,
         "first_union_permitting_full_shallow_ceiling": 909846,
         "union_values_exhausted": 1048565},
    ], "full rank seven through twelve excess rows")
    require(not high[-1]["uniform_cut"], "rank twelve full range open")
    require(high[-1]["first_union_permitting_full_shallow_ceiling"] == 909846,
            "rank twelve first full union")
    before = (
        (R+909845)*binomial(R+909844, 11)
        // ((909845+S_MAX)*binomial(W+S_MAX+11, 11))
    )
    at = (
        (R+909846)*binomial(R+909845, 11)
        // ((909846+S_MAX)*binomial(W+S_MAX+11, 11))
    )
    require((before, at) == (15775932, 15776019),
            "rank twelve adjacent full caps")
    return {
        "rank6_combined": rank6,
        "rank7_through_12": high,
        "rank12_adjacent_full_caps": [int(before), int(at)],
    }


def pair_minimum(total, universe):
    quotient, remainder = divmod(Integer(total), Integer(universe))
    return universe*binomial(quotient, 2)+remainder*quotient


def scalar_profile():
    rank = Integer(6)
    g = Integer(900000)
    degree = Integer(899999)
    effective_n = R+g
    total_m = L*degree
    q1 = binomial(W+5, 5)
    q2 = binomial(W+4, 4)
    pair_rhs = (L-1)*total_m-binomial(L, 2)*(W+1)
    slacks = {
        "predecessor_basis": binomial(effective_n, 6)-L*binomial(W+6, 6),
        "marked_E": R*binomial(effective_n-1, 5)-total_m*q1,
        "marked_S": g*binomial(effective_n-1, 5)-L*(g-degree)*q1,
        "first_pivot_total": (
            effective_n*binomial(effective_n-1, 5)-L*g*q1),
        "cross_block": (
            g*R*binomial(effective_n-2, 4)
            - L*(g-degree)*degree*q2),
        "affine_line": (
            15*effective_n*binomial(effective_n-1, 4)
            - L*g*binomial(W+5, 4)),
        "exact_pair_incidence": (
            pair_rhs-pair_minimum(total_m, g)-pair_minimum(total_m, R)),
        "cauchy_moment_times_aR": (
            (2*L*total_m-L*(L-1)*(W+1))*A*R
            - total_m*total_m*(A+R)),
    }
    expected = {
        "predecessor_basis": Integer(59479200309177922870036052970569240),
        "marked_E": Integer(27407153349842619929030408431302720),
        "marked_S": Integer(176664888061209174836992414341886680),
        "first_pivot_total": Integer(204072041411051794766022822773189400),
        "cross_block": Integer(460698629600585299877979611070709550),
        "affine_line": Integer(2476896532094258299896800951250),
        "exact_pair_incidence": Integer(867885585529651763),
        "cauchy_moment_times_aR": Integer(49374815466171856144854090456850),
    }
    require(total_m == 14198323924067, "scalar profile degree total")
    require(slacks == expected, "scalar profile exact slacks")
    require(all(value >= 0 for value in slacks.values()),
            "scalar profile feasible")
    return {
        "rank": int(rank),
        "g": int(g),
        "e": 0,
        "all_excess": 0,
        "all_degrees": int(degree),
        "M": int(total_m),
        "slacks": {key: int(value) for key, value in slacks.items()},
        "realized_polynomial_family": False,
    }


def toy_replay():
    q = Integer(17)
    a = Integer(12)
    toy_R = Integer(2)
    toy_K = a
    toy_w = Integer(0)
    field = GF(q)
    ring = PolynomialRing(field, "X")
    X = ring.gen()
    s_points = tuple(field(i) for i in range(int(a)))
    e_points = (field(12), field(13))

    def locator(roots):
        answer = ring.one()
        for root in roots:
            answer *= X-root
        return answer

    def lagrange_basis(index):
        numerator = ring.one()
        denominator = field.one()
        xi = s_points[index]
        for j, xj in enumerate(s_points):
            if j == index:
                continue
            numerator *= X-xj
            denominator *= xi-xj
        return numerator/denominator

    lagrange = tuple(lagrange_basis(i) for i in range(int(a)))
    require(all(lagrange[i](s_points[j]) == (1 if i == j else 0)
                for i in range(int(a)) for j in range(int(a))),
            "toy Lagrange basis")
    a0 = locator(s_points)
    l0 = locator(e_points)

    def construct(u_values):
        members = []
        for i in range(int(a)):
            ell = lagrange[i]
            for h_index in range(2):
                scalar = u_values[h_index]/ell(e_points[h_index])
                c = scalar*ell
                other = 1-h_index
                if c(e_points[other]) == u_values[other]:
                    continue
                members.append({
                    "c": c,
                    "G_roots": (s_points[i],),
                    "H_roots": (e_points[h_index],),
                })
        for i in range(int(a)):
            for j in range(i+1, int(a)):
                matrix_values = matrix(field, [
                    [lagrange[i](e_points[0]), lagrange[j](e_points[0])],
                    [lagrange[i](e_points[1]), lagrange[j](e_points[1])],
                ])
                require(matrix_values.det() != 0, "toy MDS two-by-two minor")
                alpha, beta = matrix_values.solve_right(vector(field, u_values))
                if alpha == 0 or beta == 0:
                    continue
                c = alpha*lagrange[i]+beta*lagrange[j]
                require(tuple(c(y) for y in e_points) == tuple(u_values),
                        "toy pair interpolation")
                members.append({
                    "c": c,
                    "G_roots": (s_points[i], s_points[j]),
                    "H_roots": e_points,
                })
        require(len({member["c"] for member in members}) == len(members),
                "toy codewords distinct")
        return members

    u_values = (field(1), field(6))
    family = construct(u_values)
    require(len(family) == 90, "toy good-ratio family size")
    v_values = tuple(a0(y)/u for y, u in zip(e_points, u_values))
    V = (v_values[0]
         + (v_values[1]-v_values[0])/(e_points[1]-e_points[0])
         * (X-e_points[0]))
    require(V == 14+14*X, "toy common unit polynomial")
    require(all(V(y) != 0 for y in e_points), "toy common unit gate")

    canonical = []
    for member in family:
        G = locator(member["G_roots"])
        H = locator(member["H_roots"])
        cofactor, remainder = a0.quo_rem(G)
        require(remainder == 0, "toy split G divides A0")
        b, remainder = member["c"].quo_rem(cofactor)
        require(remainder == 0, "toy reconstructed numerator")
        member["G"] = G
        member["H"] = H
        member["b"] = b
        member["m"] = Integer(len(member["G_roots"]))
        member["s"] = Integer(len(member["H_roots"]))-member["m"]
        require(member["c"] == cofactor*b, "toy rational reconstruction")
        require(member["c"].degree() < toy_K, "toy code degree")
        require(b != 0 and b.degree() < member["m"]-toy_w,
                "toy numerator degree")
        require(gcd(G, b) == 1 and gcd(H, b) == 1,
                "toy individual coprimality")
        require(gcd(l0, G-b*V) == H, "toy exact full gcd")
        require(member["s"] == 0, "toy zero excess")
        s_nonzeros = tuple(x for x in s_points if member["c"](x) != 0)
        e_agreements = tuple(y for index, y in enumerate(e_points)
                             if member["c"](y) == u_values[index])
        require(s_nonzeros == member["G_roots"], "toy exact G support")
        require(e_agreements == member["H_roots"], "toy exact H support")
        canonical.append({
            "G": tuple(int(x) for x in member["G_roots"]),
            "H": tuple(int(x) for x in member["H_roots"]),
            "b": tuple(int(x) for x in b.list()),
            "c": tuple(int(x) for x in member["c"].list()),
        })

    digest = hashlib.sha256(canonical_json(canonical).encode("ascii")).hexdigest()
    require(digest ==
            "2ed7462c2a4041ca893b39e194c1e6331751171c4cb982cd9625501ce05a10b9",
            "toy canonical family digest")

    wronskian_pairs = 0
    for left, right in combinations(family, 2):
        wronskian = left["G"]*right["b"]-right["G"]*left["b"]
        require(wronskian != 0, "toy nonzero Wronskian")
        left_h = set(left["H_roots"])
        right_h = set(right["H_roots"])
        require(all(wronskian(y) == 0 for y in left_h.intersection(right_h)),
                "toy Wronskian intersection zeros")
        require(all(wronskian(y) != 0
                    for y in left_h.symmetric_difference(right_h)),
                "toy Wronskian symmetric-difference units")
        wronskian_pairs += 1
    require(wronskian_pairs == binomial(90, 2) == 4005,
            "toy all Wronskian pairs")

    coefficient_rows = [
        [member["c"][index] for index in range(int(toy_K))]
        for member in family
    ]
    span_rank = matrix(field, coefficient_rows).rank()
    require(span_rank == 12, "toy full coefficient rank")
    union_roots = set().union(*[set(member["G_roots"]) for member in family])
    common_e = sum(all(member["b"](y) == 0 for member in family)
                   for y in e_points)
    require(len(union_roots) == 12 and common_e == 0, "toy g and e")

    g = Integer(len(union_roots))
    rank = Integer(span_rank)
    degree_sum = sum(member["m"] for member in family)
    m_histogram = {
        str(m): sum(member["m"] == m for member in family)
        for m in (1, 2)
    }
    b_degree_histogram = {}
    for member in family:
        key = str(int(member["b"].degree()))
        b_degree_histogram[key] = b_degree_histogram.get(key, 0)+1
    require(m_histogram == {"1": 24, "2": 66}, "toy degree histogram")
    require(degree_sum == 156, "toy degree sum")

    g_keys = [tuple(int(x) for x in member["G_roots"]) for member in family]
    distinct_g = len(set(g_keys))
    max_fixed_g = max(g_keys.count(key) for key in set(g_keys))
    require((distinct_g, max_fixed_g) == (78, 2), "toy locator counts")

    basis_lhs = sum(binomial(toy_w+member["s"]+rank+common_e, rank)
                    for member in family)
    basis_rhs = binomial(toy_R+g-common_e, rank)
    first_factor = falling(toy_w+rank+common_e-1, rank-1)
    ambient_factor = falling(toy_R+g-common_e-1, rank-1)
    first_lhs = sum((g+member["s"])*first_factor for member in family)
    first_rhs = falling(toy_R+g-common_e, rank)
    marked_e_lhs = sum((member["m"]+member["s"])*first_factor
                        for member in family)
    marked_e_rhs = (toy_R-common_e)*ambient_factor
    marked_s_lhs = sum((g-member["m"])*first_factor for member in family)
    marked_s_rhs = g*ambient_factor
    cross_lhs = sum(
        (g-member["m"])*(member["m"]+member["s"])
        * binomial(toy_w+member["s"]+rank+common_e-2, rank-2)
        for member in family)
    cross_rhs = (g*(toy_R-common_e)
                 * binomial(toy_R+g-common_e-2, rank-2))

    inequalities = {
        "basis": {
            "lhs": int(basis_lhs), "rhs": int(basis_rhs),
            "slack": int(basis_rhs-basis_lhs),
        },
        "first_pivot_ordered": {
            "lhs": int(first_lhs), "rhs": int(first_rhs),
            "slack": int(first_rhs-first_lhs),
        },
        "marked_E_ordered": {
            "lhs": int(marked_e_lhs), "rhs": int(marked_e_rhs),
            "slack": int(marked_e_rhs-marked_e_lhs),
        },
        "marked_S_ordered": {
            "lhs": int(marked_s_lhs), "rhs": int(marked_s_rhs),
            "slack": int(marked_s_rhs-marked_s_lhs),
        },
        "cross_block": {
            "lhs": int(cross_lhs), "rhs": int(cross_rhs),
            "slack": int(cross_rhs-cross_lhs),
        },
    }
    require(inequalities == {
        "basis": {"lhs": 90, "rhs": 91, "slack": 1},
        "first_pivot_ordered": {
            "lhs": 43110144000, "rhs": 43589145600,
            "slack": 479001600,
        },
        "marked_E_ordered": {
            "lhs": 6227020800, "rhs": 6227020800, "slack": 0,
        },
        "marked_S_ordered": {
            "lhs": 36883123200, "rhs": 37362124800,
            "slack": 479001600,
        },
        "cross_block": {"lhs": 1584, "rhs": 1584, "slack": 0},
    }, "toy basis and colored slacks")

    ratios = tuple(lagrange[i](e_points[1])/lagrange[i](e_points[0])
                   for i in range(int(a)))
    require(len(set(ratios)) == 12 and field(6) not in ratios,
            "toy distinct bad ratios and good witness ratio")
    size_histogram = {}
    for u1_int, u2_int in product(range(1, 17), repeat=2):
        trial = construct((field(u1_int), field(u2_int)))
        key = str(len(trial))
        size_histogram[key] = size_histogram.get(key, 0)+1
    require(size_histogram == {"77": 192, "90": 64},
            "toy exhaustive received-table histogram")

    bad_ratio = ratios[0]
    bad_family = construct((field(1), bad_ratio))
    bad_rank = matrix(field, [
        [member["c"][index] for index in range(int(toy_K))]
        for member in bad_family
    ]).rank()
    bad_union = set().union(*[set(member["G_roots"])
                              for member in bad_family])
    require((len(bad_family), bad_rank, len(bad_union)) == (77, 11, 11),
            "toy bad-ratio mutation detected")

    return {
        "field": 17,
        "S0": [int(x) for x in s_points],
        "E0": [int(x) for x in e_points],
        "n": 14,
        "K": 12,
        "R": 2,
        "w": 0,
        "U_E0": [1, 6],
        "V_coefficients": [int(x) for x in V.list()],
        "family_size": len(family),
        "rank": int(span_rank),
        "g": len(union_roots),
        "e": int(common_e),
        "m_histogram": m_histogram,
        "b_degree_histogram": b_degree_histogram,
        "degree_sum": int(degree_sum),
        "distinct_G": distinct_g,
        "max_fixed_G": max_fixed_g,
        "Wronskian_pairs": wronskian_pairs,
        "canonical_family_sha256": digest,
        "inequalities": inequalities,
        "basis_capacity": int(basis_rhs),
        "first_pivot_slack": int(first_rhs-first_lhs),
        "marked_E_slack": int(marked_e_rhs-marked_e_lhs),
        "received_tables_exhausted": 256,
        "received_table_size_histogram": size_histogram,
        "bad_ratio_removed": len(family)-len(bad_family),
        "bad_ratio_mutation": {
            "ratio": int(bad_ratio),
            "lost_index": 0,
            "family_size": len(bad_family),
            "members_removed": len(family)-len(bad_family),
            "rank": int(bad_rank),
            "g": len(bad_union),
            "detected": True,
        },
    }


require((P, N, K, A, R, W, B_STAR, DEEP_CAP, L, S_MAX) == (
    2147483647, 2097152, 1048576, 1116023, 981129, 67447,
    16777215, 1001282, 15775933, 366886,
), "deployed parameters")
require((N-K+1)//(W+1) == 15, "deployed affine-line multiplicity")
require(R//(W+1) == 14, "deployed projective-ray multiplicity")
require((L+13)//14 == 1126853, "deployed projective direction floor")

thresholds = deployed_thresholds()
excess = deployed_excess_sweeps()
profile = scalar_profile()
toy = toy_replay()

summary = {
    "schema": "m31-varying-g-first-pivot-basis-route-cut-sage-v1",
    "status": "EXACT_INDEPENDENT_SAGE_CONTROL",
    "terminal": "UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE",
    "deployed_parameters": {
        "p": int(P), "n": int(N), "K": int(K), "a": int(A),
        "R": int(R), "w": int(W), "B_star": int(B_STAR),
        "deep_cap": int(DEEP_CAP), "shallow_size": int(L),
        "shallow_excess_max": int(S_MAX),
        "affine_line_multiplicity": 15,
        "projective_ray_multiplicity": 14,
        "minimum_projective_directions": 1126853,
    },
    "deployed_thresholds": thresholds,
    "deployed_excess_sweeps": excess,
    "rank_caps_1_5": [row["maximum_cap"]
                       for row in thresholds["rank_1_through_5"]],
    "rank6_surviving_union_interval":
        thresholds["rank6_surviving_union_interval"],
    "rank6_combined_excess":
        excess["rank6_combined"]["total_excess_ceiling"],
    "aggregate_route_cut": profile,
    "toy_sharpness": toy,
    "scope": {
        "integer_only": True,
        "deployed_union_ranges_exhausted": True,
        "toy_received_tables_exhausted": True,
        "toy_family_is_deployed_evidence": False,
        "ledger_movement": 0,
        "row_closed": False,
    },
    "ledger_movement": 0,
    "row_closed": False,
}
summary["checks"] = int(CHECKS)
print(canonical_json(summary))
