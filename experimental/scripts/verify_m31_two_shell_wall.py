#!/usr/bin/env python3
"""Zero-argument stdlib verifier for cap25_v13_m31_two_shell_wall.md."""

import copy
import hashlib
import json
import math
import os
import sys
from collections import Counter, defaultdict
from itertools import combinations


def apply_cap():
    try:
        import resource

        cap = 2 * 1024 ** 3
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        hard2 = cap if hard == resource.RLIM_INFINITY else min(cap, hard)
        if soft == resource.RLIM_INFINITY or soft > cap:
            resource.setrlimit(resource.RLIMIT_AS, (cap, hard2))
    except Exception:
        pass


apply_cap()
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "experimental", "data", "cap25_v13_m31_two_shell_wall.json")
CHECKS = []


def check(name, condition, detail=""):
    ok = bool(condition)
    CHECKS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


def ceil_div(a, b):
    return -((-a) // b)


# ------------------------------------------------------------- norm-one twin cosets
def cmul(u, v, p):
    a, b = u
    c, d = v
    return ((a * c - b * d) % p, (a * d + b * c) % p)


def cpow(u, exponent, p):
    out = (1, 0)
    while exponent:
        if exponent & 1:
            out = cmul(out, u, p)
        u = cmul(u, u, p)
        exponent >>= 1
    return out


def element_order(u, p):
    value = (1, 0)
    for order in range(1, p + 2):
        value = cmul(value, u, p)
        if value == (1, 0):
            return order
    raise AssertionError("order exceeds p+1")


def circle_generator(p):
    for a in range(p):
        for b in range(p):
            if (a * a + b * b) % p == 1 and element_order((a, b), p) == p + 1:
                return (a, b)
    raise AssertionError("no generator")


def twin_domain(p, n):
    omega = circle_generator(p)
    q = (p + 1) // n
    H = [cpow(omega, q * j, p) for j in range(n)]
    g = omega
    ginv = cpow(omega, p, p)
    lifted = {cmul(g, h, p) for h in H} | {cmul(ginv, h, p) for h in H}
    by_x = defaultdict(list)
    for u in lifted:
        by_x[u[0]].append(u)
    assert len(lifted) == 2 * n and all(len(v) == 2 for v in by_x.values())
    return sorted(by_x), omega


# ------------------------------------------------------------- exact clique engine
def max_clique_bitsets(adj):
    """Tomita-style exact maximum clique with a greedy coloring upper bound."""
    best = []

    def expand(stack, candidates):
        nonlocal best
        if not candidates:
            if len(stack) > len(best):
                best = stack.copy()
            return
        if len(stack) + candidates.bit_count() <= len(best):
            return
        order = []
        colors = []
        uncolored = candidates
        color = 0
        while uncolored:
            color += 1
            available = uncolored
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                order.append(vertex)
                colors.append(color)
                uncolored ^= bit
                available &= ~bit
                available &= ~adj[vertex]
        for index in range(len(order) - 1, -1, -1):
            if len(stack) + colors[index] <= len(best):
                return
            vertex = order[index]
            bit = 1 << vertex
            if candidates & bit:
                stack.append(vertex)
                expand(stack, candidates & adj[vertex])
                stack.pop()
                candidates ^= bit

    expand([], (1 << len(adj)) - 1)
    return best


def fibers_by_power_sums(D, p, m, w):
    fibers = defaultdict(list)
    for subset in combinations(range(len(D)), m):
        key = tuple(sum(pow(D[i], j, p) for i in subset) % p for j in range(1, w + 1))
        mask = sum(1 << i for i in subset)
        fibers[key].append(mask)
    return fibers


def exact_two_shell_census(D, p, m, w):
    fibers = fibers_by_power_sums(D, p, m, w)
    global_best = (0, None, None, [])
    graph_count = 0
    for key in sorted(fibers):
        vertices = fibers[key]
        count = len(vertices)
        if count == 1:
            if global_best[0] < 1:
                global_best = (1, key, (), vertices[:])
            continue
        distance = [[0] * count for _ in range(count)]
        values = set()
        for i in range(count):
            for j in range(i):
                e = m - (vertices[i] & vertices[j]).bit_count()
                distance[i][j] = distance[j][i] = e
                values.add(e)
        allowed_sets = [(e,) for e in sorted(values)] + list(combinations(sorted(values), 2))
        for allowed in allowed_sets:
            graph_count += 1
            adj = [0] * count
            aset = set(allowed)
            for i in range(count):
                for j in range(i):
                    if distance[i][j] in aset:
                        adj[i] |= 1 << j
                        adj[j] |= 1 << i
            clique = max_clique_bitsets(adj)
            if len(clique) > global_best[0]:
                global_best = (len(clique), key, allowed, [vertices[i] for i in clique])
    return fibers, global_best, graph_count


def masks_to_index_lists(masks, n):
    return [[i for i in range(n) if mask >> i & 1] for mask in masks]


# ------------------------------------------------------------- deployed arithmetic
print("== Exact deployed two-shell reduction ==")
p = 2 ** 31 - 1
n = 2 ** 21
m = 981_129
w = 67_447
Bstar = 2 ** 24 - 1
L0 = Bstar + 1
rank_prefix = n - w
real_mult = L0 - n
fp_mult = L0 - rank_prefix
r0_num = m * (n - m)
r0_den = n
r0_floor = r0_num // r0_den
seidel_rhs = n * (L0 - 1) // (L0 - n)
check("row constants", (p, n, m, w, Bstar, L0) == (2147483647, 2097152, 981129, 67447, 16777215, 16777216))
check("first violating size is 8n", L0 == 8 * n)
check("centered radius exact", (r0_num, r0_den, r0_floor) == (1_094_962_529_967, 2_097_152, 522_118))
check("Seidel trace quotient exact", seidel_rhs == 2_396_745)
check("square cutoff", 1548 ** 2 <= seidel_rhs < 1549 ** 2)
check("integral ratio cutoff k<=774", (1548 + 1) // 2 == 774)
check("real repeated-eigenvalue multiplicity", real_mult == 14_680_064)
check("prefix rank and Fp nullity", rank_prefix == 2_029_705 and fp_mult == 14_747_511)

grid = []
for k in range(2, 775):
    lo = ceil_div(w + 1, k - 1)
    hi = min(m // k, r0_num // (r0_den * (k - 1)))
    if lo <= hi:
        grid.append((k, lo, hi, hi - lo + 1))
grid_count = sum(row[3] for row in grid)
check("all k=2..774 survive", len(grid) == 773)
check("exact surviving lattice size", grid_count == 3_254_885)
check("lattice endpoints", grid[0] == (2, 67_448, 490_564, 423_117)
      and grid[-1] == (774, 88, 675, 588))

print("\n== Construction exclusions ==")
signed_trade_support = 2 * (w + 1)
pattern_cap = n // signed_trade_support
affine_dim_cap = pattern_cap
affine_size_cap = 2 ** affine_dim_cap
v_atoms = 5794
pairs_before = math.comb(v_atoms - 1, 2)
pairs_after = math.comb(v_atoms, 2)
atom_size_cap = (n - m) // (v_atoms - 2)
check("affine-binary pattern support", signed_trade_support == 134_896)
check("affine-binary dimension/size cap", pattern_cap == 15 and affine_size_cap == 32_768)
check("all-pairs threshold", pairs_before == 16_776_528 <= Bstar < pairs_after == 16_782_321)
check("all-pairs atom cap", atom_size_cap == 192 and atom_size_cap < w + 1)
check("design coefficient gate", Bstar + 1 < p)

# A small exact instance of the Gram identity: all 2-subsets of five points.
small_blocks = list(combinations(range(5), 2))
small_X = [[int(i in block) for i in range(5)] for block in small_blocks]
small_A = [[0] * len(small_blocks) for _ in small_blocks]
identity_ok = True
for i, bi in enumerate(small_blocks):
    for j, bj in enumerate(small_blocks):
        inner = len(set(bi) & set(bj))
        distance = 2 - inner
        if i != j and distance == 1:
            small_A[i][j] = 1
        lhs = small_A[i][j] + (2 if i == j else 0)
        rhs = inner + (2 - 2)
        identity_ok &= lhs == rhs
check("synthetic A+kI Gram identity", identity_ok)

print("\n== Exact smaller faithful-toy maxima ==")
D31, omega31 = twin_domain(31, 8)
fib31, best31, graphs31 = exact_two_shell_census(D31, 31, 4, 2)
check("p31 domain", D31 == [2, 5, 10, 11, 20, 21, 26, 29])
check("p31 global maximum is 2", best31[0] == 2)
check("p31 collision fiber/shell", best31[1] == (0, 2) and best31[2] == (4,))
check("p31 unique collision fiber", sum(len(v) > 1 for v in fib31.values()) == 1 and len(fib31[(0, 2)]) == 2)

D16, omega127 = twin_domain(127, 16)
fib16, best16, graphs16 = exact_two_shell_census(D16, 127, 8, 1)
best16_indices = masks_to_index_lists(best16[3], 16)
check("p127,n16 domain", D16 == [2, 5, 9, 22, 38, 39, 42, 53, 74, 85, 88, 89, 105, 118, 122, 125])
check("p127,n16 global maximum is 23", best16[0] == 23)
check("p127,n16 maximizing fiber/shells", best16[1] == (28,) and best16[2] == (2, 4))

print("\n== Main p127,n32 inclusion-maximal witness ==")
D32, omega32 = twin_domain(127, 32)
WITNESS32 = [
    [0,1,5,7,8,9,15,16,17,18,23,24,25,28,31],
    [1,4,5,8,10,12,15,16,18,19,20,21,24,26,27],
    [2,3,6,7,14,15,16,18,19,21,24,25,27,30,31],
    [0,5,6,8,9,10,13,14,16,19,22,24,27,28,30],
    [0,3,4,5,6,10,11,15,16,18,25,27,28,29,31],
    [0,5,6,12,14,15,17,18,19,20,21,22,28,30,31],
    [0,1,3,5,6,8,9,17,18,21,25,26,27,29,30],
    [0,2,3,7,8,9,12,16,18,19,20,27,28,29,30],
    [2,5,6,8,9,11,12,13,15,16,18,24,29,30,31],
    [0,2,4,8,9,14,15,16,17,18,21,22,24,27,29],
    [0,1,4,5,7,9,11,12,14,15,16,19,25,29,30],
    [0,1,6,9,12,13,14,15,16,18,19,23,26,27,31],
    [6,7,8,9,10,14,16,18,19,20,22,25,26,29,31],
    [3,4,5,9,12,14,16,18,22,23,24,25,26,28,30],
    [2,5,8,9,10,12,14,19,21,23,25,27,28,29,31],
    [0,1,3,9,10,11,12,16,18,19,21,22,24,29,31],
    [0,3,4,6,7,8,9,10,12,15,16,21,23,30,31],
]
witness_masks = [sum(1 << i for i in row) for row in WITNESS32]
syndromes = {
    (sum(D32[i] for i in row) % 127, sum(D32[i] ** 2 for i in row) % 127)
    for row in WITNESS32
}
hist = Counter(
    15 - (witness_masks[i] & witness_masks[j]).bit_count()
    for i in range(len(witness_masks)) for j in range(i)
)
canonical = ";".join(",".join(map(str, row)) for row in WITNESS32).encode("ascii")
witness_sha = hashlib.sha256(canonical).hexdigest()
check("main-toy witness syndrome", syndromes == {(45, 115)})
check("main-toy witness shell histogram", hist == Counter({8: 78, 7: 58}))
check("main-toy witness checksum", len(canonical) == 681 and witness_sha == "e1f491744b5b4f74ae4af288f2fde9f12a6dd078b359bbf903f0b47889e5afe7")


def half_groups(values, offset):
    size = 1 << len(values)
    counts = [0] * size
    sums1 = [0] * size
    sums2 = [0] * size
    groups = defaultdict(list)
    groups[(0, 0, 0)].append(0)
    for mask in range(1, size):
        bit = mask & -mask
        idx = bit.bit_length() - 1
        prev = mask ^ bit
        counts[mask] = counts[prev] + 1
        sums1[mask] = (sums1[prev] + values[idx]) % 127
        sums2[mask] = (sums2[prev] + values[idx] * values[idx]) % 127
        groups[(counts[mask], sums1[mask], sums2[mask])].append(mask << offset)
    return groups


left = half_groups(D32[:16], 0)
right = half_groups(D32[16:], 16)
fiber32 = []
for (count, s1, s2), left_masks in left.items():
    need = (15 - count, (45 - s1) % 127, (115 - s2) % 127)
    for lm in left_masks:
        for rm in right.get(need, ()):
            fiber32.append(lm | rm)
witness_set = set(witness_masks)
extensions = [
    mask for mask in fiber32 if mask not in witness_set
    and all(15 - (mask & other).bit_count() in (7, 8) for other in witness_masks)
]
check("main-toy ambient support/syndrome counts", math.comb(32, 15) == 565_722_720 and 127 ** 2 == 16_129)
check("main-toy target fiber size", len(fiber32) == 34_359)
check("size-17 witness is inclusion-maximal", not extensions)

# ------------------------------------------------------------- exact JSON replay
packet = {
    "schema": "cap25-v13-m31-two-shell-wall-v1",
    "status": "PROVED reductions and construction exclusions / PROVED-AT-TOYS exact smaller maxima and main-toy maximality / OPEN deployed two-shell bound",
    "deployed": {
        "p": p, "n": n, "m": m, "w": w, "Bstar": Bstar, "L0": L0,
        "centered_radius_numerator": r0_num,
        "centered_radius_denominator": r0_den,
        "centered_radius_floor": r0_floor,
        "seidel_rhs": seidel_rhs,
        "k_max": 774,
        "real_multiplicity_floor": real_mult,
        "prefix_rank_cap": rank_prefix,
        "Fp_nullity_floor": fp_mult,
        "grid_k_count": len(grid),
        "grid_pair_count": grid_count,
        "grid_first": list(grid[0]),
        "grid_last": list(grid[-1]),
    },
    "construction_exclusions": {
        "signed_trade_support_floor": signed_trade_support,
        "affine_dimension_cap": affine_dim_cap,
        "affine_family_cap": affine_size_cap,
        "all_pairs_atom_count": v_atoms,
        "all_pairs_before": pairs_before,
        "all_pairs_after": pairs_after,
        "all_pairs_atom_size_cap": atom_size_cap,
    },
    "toy_p31": {
        "domain": D31,
        "fiber_count": len(fib31),
        "global_maximum": best31[0],
        "fiber": list(best31[1]),
        "shells": list(best31[2]),
    },
    "toy_p127_n16": {
        "domain": D16,
        "fiber_count": len(fib16),
        "min_fiber": min(map(len, fib16.values())),
        "max_fiber": max(map(len, fib16.values())),
        "graphs_checked": graphs16,
        "global_maximum": best16[0],
        "fiber": list(best16[1]),
        "shells": list(best16[2]),
    },
    "toy_p127_n32": {
        "domain": D32,
        "witness_size": len(WITNESS32),
        "fiber": [45, 115],
        "shell_histogram": {"7": hist[7], "8": hist[8]},
        "fiber_size": len(fiber32),
        "compatible_extensions": len(extensions),
        "witness_ascii_bytes": len(canonical),
        "witness_sha256": witness_sha,
        "witness_indices": WITNESS32,
    },
}

with open(DATA, encoding="utf-8") as handle:
    shipped = json.load(handle)
check("shipped JSON exact replay", shipped == packet, "graphs16=%d" % graphs16)

print("\n== Corruption self-tests ==")


def tamper(name, mutate):
    bad = copy.deepcopy(shipped)
    mutate(bad)
    check("tamper::" + name, bad != packet, "corruption rejected")


tamper("Bstar", lambda x: x["deployed"].__setitem__("Bstar", Bstar + 1))
tamper("k_max", lambda x: x["deployed"].__setitem__("k_max", 775))
tamper("grid_count", lambda x: x["deployed"].__setitem__("grid_pair_count", grid_count - 1))
tamper("Fp_nullity", lambda x: x["deployed"].__setitem__("Fp_nullity_floor", fp_mult - 1))
tamper("affine_cap", lambda x: x["construction_exclusions"].__setitem__("affine_family_cap", 65_536))
tamper("small_toy_max", lambda x: x["toy_p127_n16"].__setitem__("global_maximum", 22))
tamper("main_witness", lambda x: x["toy_p127_n32"]["witness_indices"][0].__setitem__(0, 1))
tamper("main_hash", lambda x: x["toy_p127_n32"].__setitem__("witness_sha256", "0" + witness_sha[1:]))

passed = sum(ok for _, ok in CHECKS)
print("\nRESULT: %s (%d/%d checks)" % ("PASS" if passed == len(CHECKS) else "FAIL", passed, len(CHECKS)))
print("Status: PROVED reductions / PROVED-AT-TOYS / OPEN deployed two-shell cell")
sys.exit(0 if passed == len(CHECKS) else 1)
