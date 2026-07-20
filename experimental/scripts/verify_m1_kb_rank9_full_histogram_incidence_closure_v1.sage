#!/usr/bin/env sage
"""Independent exact controls for the full-histogram incidence closure.

The deployed arithmetic is exact.  The finite-field/set-system examples are
toy controls for the moving-zero interface; they are not deployed selectors
and are not proof substitutes.
"""

from sage.all import GF, Integer, binomial, ceil


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


P = Integer(2_130_706_433)
N = Integer(2_097_152)
K = Integer(1_048_576)
A = Integer(1_116_048)
J = N - A
T = A - K
B_REMAINING = Integer(274_980_305_756_664_755)
C0 = binomial(T + 8, 8)
MU_ZERO = Integer(1_184_288_048_715_968_585_930_152_451_399_175)


def source_size(r):
    return T + r + 1


def carrier(r):
    return N - source_size(r)


def x_floor(r):
    return ceil((T - r + 1) / Integer(2))


def line_cap(r):
    x0 = x_floor(r)
    return 1 + J // x0 if x0 >= 1 else J + 1


def full_histogram_cap(r):
    return line_cap(r) * binomial(carrier(r), 8) // C0


expected = {
    67_467: (3, 327_035, 167_238_042_774_200_802),
    67_468: (3, 327_035, 167_237_360_939_443_806),
    67_469: (2, 490_553, 250_855_274_346_888_378),
    67_470: (2, 490_553, 250_854_251_601_007_573),
    67_471: (1, 981_105, 501_705_946_349_301_216),
    209_552: (-71_039, 981_105, 274_980_543_029_818_779),
    209_553: (-71_040, 981_105, 274_979_334_408_472_994),
}

for r, (want_x, want_j, want_cap) in expected.items():
    require(x_floor(r) == want_x, "x-floor endpoint drift")
    require(line_cap(r) == want_j, "line-cap endpoint drift")
    require(full_histogram_cap(r) == want_cap, "incidence-cap endpoint drift")

for r in range(67_467, 67_471):
    require(full_histogram_cap(r) <= B_REMAINING, "closed endpoint misses budget")
require(full_histogram_cap(67_471) > B_REMAINING, "x=1 route cut unexpectedly pays")
require(
    full_histogram_cap(67_471) - B_REMAINING
    == 226_725_640_592_636_461,
    "x=1 deficit drift",
)
require(full_histogram_cap(209_552) > B_REMAINING, "last route-cut layer unexpectedly pays")
require(full_histogram_cap(209_553) <= B_REMAINING, "upper paid restart misses budget")
require(
    B_REMAINING - full_histogram_cap(209_553) == 971_348_191_761,
    "upper paid margin drift",
)

# Enumerate a toy slack simplex and verify delta <= u <= r pointwise.
for r in range(0, 9):
    for h in range(r + 1):
        for u in range(r - h + 1):
            ell = r - h - u
            require(h + u + ell == r, "toy simplex identity failed")
            for delta in range(u + 1):
                require(0 <= delta <= u <= r, "toy full-histogram implication failed")

# Sharp toy moving-zero set systems over a genuine finite field.
F = GF(101)
points = list(F)[:7]

# j=5, x=1: J=j+1=6 is attained by six disjoint singleton moving sets.
j_toy = 5
x_one = 1
singleton_sets = [{points[i]} for i in range(6)]
require(len(singleton_sets) == 1 + j_toy // x_one, "x=1 line cap drift")
require(sum(len(S) for S in singleton_sets) == j_toy + x_one, "x=1 capacity drift")
require(len(set().union(*singleton_sets)) == 6, "x=1 disjointness drift")

# j=5, x=2: three disjoint pairs attain the cap; four pairs exceed capacity.
x_two = 2
pair_sets = [{points[0], points[1]}, {points[2], points[3]}, {points[4], points[5]}]
require(len(pair_sets) == 1 + j_toy // x_two, "x=2 line cap drift")
require(sum(len(S) for S in pair_sets) <= j_toy + x_two, "x=2 capacity drift")
require(4 * x_two > j_toy + x_two, "x=2 sharp-failure control drift")

r = Integer(67_471)
H = B_REMAINING + 1
N_V = carrier(r)
J_STAR = line_cap(r)
L = (H + J_STAR - 1) // J_STAR
bases_used = L * C0
ambient_bases = binomial(N_V, 8)
common_zero_size = N_V - (J + 1)
local_basis_capacity = binomial(common_zero_size, 8)
ambient_rank9 = binomial(N_V, 9)
weighted_rank9 = H * MU_ZERO

require(L == 280_276_123_103, "route-cut line count drift")
require(ambient_bases >= bases_used, "global abstract basis capacity failed")
require(local_basis_capacity >= C0, "local abstract basis capacity failed")
require(ambient_rank9 >= weighted_rank9, "rank-nine scalar capacity failed")
require(H <= P**6, "extension-field slope universe too small")
require((J_STAR - 1) * 1 == J, "x=1 moving-zero equality drift")

# The same all-zero-deficit relaxation remains feasible at the tight upper
# endpoint of the 142,082-layer gap.
r_last = Integer(209_552)
N_LAST = carrier(r_last)
s_last = source_size(r_last)
e_last = ceil(s_last / Integer(2))
u_last = e_last - 1
h_last = r_last - u_last
require((e_last, u_last, h_last) == (138_513, 138_512, 71_040), "upper slack profile drift")
require(h_last + u_last == r_last, "upper slack simplex drift")
require(1 >= x_floor(r_last), "upper chosen x misses floor")
require(
    binomial(N_LAST, 8) - bases_used
    == 2_577_700_250_714_186_088_081_437_187_324_862_173_900,
    "upper global basis margin drift",
)
require(
    binomial(N_LAST - (J + 1), 8) - C0
    == 6_090_483_505_083_391_560_362_880_461_341_367_491_591_320,
    "upper local basis margin drift",
)
require(
    binomial(N_LAST, 9) - H * MU_ZERO
    == 278_492_477_489_381_568_181_757_395_229_031_467_606_347_581_541_575,
    "upper rank-nine margin drift",
)

print("M1 KoalaBear full-histogram incidence Sage controls: PASS")
print("  paid ranges: 196..67,470 and 209,553..913,631")
print("  scalar route cut: 67,471..209,552 (142,082 layers)")
print("  toy controls are exact but not deployed selectors")
