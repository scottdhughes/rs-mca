#!/usr/bin/env sage
"""Independent Sage replay for the M31 65-column fixed-anchor route cut."""

from itertools import combinations


checks = 0


def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


p = 2**31 - 1
n = 2**21
K = 2**20
A = 1_116_023
R = n - A
w = A - K
Bstar = p**4 // 2**100
target_field_size = p**4
Upaid = 3_730
c = 2_048
fibers = n // c
profiles = 137 + 479 * 545
S = 2 * R - K - 1

check((p, n, K, A, R, w, Bstar) ==
      (2_147_483_647, 2_097_152, 1_048_576, 1_116_023,
       981_129, 67_447, 16_777_215), "deployed constants")
check((c, fibers, profiles, S) == (2_048, 1_024, 261_192, 913_681),
      "atlas and index constants")

boundary_cap = 64 * profiles
total_cap = Upaid + boundary_cap
check(boundary_cap == 16_716_288, "boundary cap")
check(total_cap == 16_720_018, "paid plus boundary cap")
check(Bstar - total_cap == 57_197, "boundary slack")
check((Bstar - Upaid + 1 + profiles - 1) // profiles == 65,
      "65-column trigger")

combined_allowance = 9_216_781
check(35 * profiles == 9_141_720, "combined 35-cap")
check(combined_allowance - 35 * profiles == 75_061,
      "combined gate slack")
check((combined_allowance + 1 + profiles - 1) // profiles == 36,
      "combined width-36 trigger")

rank36 = 34
q36, b36 = divmod(S, rank36)
check((q36, b36) == (26_872, 33), "width-36 division")
prefix36 = [
    m * q36 + max(0, m - (rank36 - b36))
    for m in (1, 2)
]
check(prefix36 == [26_872, 53_745], "width-36 prefix")
check(rank36 - S // (w + 1) == 21, "width-36 low rows")
check(rank36 * (w + 1) - S == 1_379_551,
      "width-36 syzygy dimension")
check([(36 - m) * (w + 1 - prefix36[m - 1])
       for m in (1, 2)] == [1_420_160, 465_902],
      "width-36 anchor incidences")

# Sharp cumulative-index optimizer.
rank = 63
q, b = divmod(S, rank)
check((q, b) == (14_502, 55), "index Euclidean division")


def sharp_prefix(m):
    candidates = []
    for t in (q, q + 1):
        candidates.append(min(m * t, S - (rank - m) * t))
    balanced = m * q + max(0, m - (rank - b))
    check(max(candidates) == balanced, "sharp prefix optimizer m=%s" % m)
    return balanced


prefix = [sharp_prefix(m) for m in range(1, 6)]
check(prefix == [14_502, 29_004, 43_506, 58_008, 72_510],
      "sharp prefix values")
check(all(x < w + 1 for x in prefix[:4]) and prefix[4] > w + 1,
      "four-step anchor ladder")
check(S // 14 == 65_262 < w, "fifty low rows")
sharp_50 = [0] * 50 + [w + 1] * 13
check(sum(sharp_50) == 876_824 <= S, "fifty-first not forced")
check(rank * (w + 1) - S == 3_335_543, "syzygy dimension")

degrees = prefix[:4]
incidences = [(65 - m) * (w + 1 - degrees[m - 1])
              for m in range(1, 5)]
check(incidences == [3_388_544, 2_421_972, 1_484_404, 575_840],
      "fixed-anchor incidences")

# Independent full source-floor census.
activated36 = []
activated = []
for u in range(480):
    vmax = 136 if u == 0 else 544
    for v in range(vmax + 1):
        h = u + v + 1
        rerr = 137 + c * u
        ragr = 1_911 + c * v
        check(rerr + ragr == c * h, "profile color sum")
        check(h <= rerr <= h * (c - 1), "error feasibility")
        check(h <= ragr <= h * (c - 1), "agreement feasibility")
        f = 544 - v
        available = 1_024 - h
        t = min(32, f)
        check(ragr + c * f == A, "source agreement size")
        candidates = binomial(available, f)
        floor = (candidates + p**t - 1) // p**t
        if t < f:
            check(ragr + c * (f - t - 1) == K - 137,
                  "source degree gate")
        else:
            check(floor == 1, "full-prefix singleton")
        if floor >= 36:
            activated36.append((u, v, ZZ(floor)))
        if floor >= 65:
            activated.append((u, v, ZZ(floor)))

faces36 = [row for row in activated36 if row[0] == 0 or row[1] == 0]
bideep36 = [row for row in activated36 if row[0] >= 1 and row[1] >= 1]
faces = [row for row in activated if row[0] == 0 or row[1] == 0]
bideep = [row for row in activated if row[0] >= 1 and row[1] >= 1]
check((len(activated36), len(faces36), len(bideep36)) == (172, 35, 137),
      "floor-36 census")
check((len(activated), len(faces), len(bideep)) == (156, 34, 122),
      "floor-65 census")
check(max(activated, key=lambda row: row[2]) == (0, 0, 6_796_405),
      "global source maximum")
check(max(bideep, key=lambda row: row[2]) == (1, 1, 1_693_898),
      "bi-deep source maximum")

frontier = []
for u in sorted(set(row[0] for row in bideep)):
    row = max((row for row in bideep if row[0] == u),
              key=lambda item: item[1])
    frontier.append(row)
check(frontier == [
    (1, 16, 120), (2, 15, 108), (3, 14, 97), (4, 13, 87),
    (5, 12, 78), (6, 11, 69), (7, 9, 115), (8, 8, 102),
    (9, 7, 89), (10, 6, 78), (11, 5, 68), (12, 3, 109),
    (13, 2, 94), (14, 1, 81),
], "floor-65 frontier")

# Proper-hyperplane collision-avoidance arithmetic.
def forbidden(width):
    return width * R + binomial(width, 2) * S


check(forbidden(65) == 1_964_229_865, "65 forbidden hyperplanes")
check(target_field_size - forbidden(65) ==
      21_267_647_892_944_572_736_998_860_267_723_701_016,
      "65 target-field avoidance margin")
check(forbidden(36) == 610_939_674, "36 forbidden hyperplanes")
check(target_field_size - forbidden(36) ==
      21_267_647_892_944_572_736_998_860_269_076_991_207,
      "36 target-field avoidance margin")
check(forbidden(Bstar + 1) == 128_589_177_894_085_853_184,
      "budget-width forbidden hyperplanes")
check(target_field_size - forbidden(Bstar + 1) ==
      21_267_647_892_944_572_608_409_682_375_602_077_697,
      "budget-width avoidance margin")

lo, hi = 0, 10**17
while lo + 1 < hi:
    mid = (lo + hi) // 2
    if forbidden(mid) < target_field_size:
        lo = mid
    else:
        hi = mid
check((lo, hi) == (6_823_032_369_902_110, 6_823_032_369_902_111),
      "target-field union-bound endpoint")

# Polynomial-module control for the fixed-minor bridge.  The four band rows
# are a primitive direct-summand frame because columns 1..4 form the identity.
# The lexicographically first nonzero four-minor is X^4, while another minor
# is the unit.  This checks that a basis-relative nonunit anchor can coexist
# with global primitivity and that its exceptional roots are degree-bounded.
F = GF(17)
PR.<X> = PolynomialRing(F)
Band = matrix(PR, 4, 8)
for i in range(4):
    Band[i, i] = X
    Band[i, i + 1] = 1

minors = {}
for cols in combinations(range(8), 4):
    minors[cols] = Band.matrix_from_columns(cols).det()
nonzero = [(cols, value) for cols, value in minors.items() if value != 0]
check(nonzero, "nonzero band minors")
lex_cols, lex_anchor = nonzero[0]
check(lex_cols == (0, 1, 2, 3) and lex_anchor == X**4,
      "lexicographic polynomial anchor")
check(minors[(1, 2, 3, 4)] == 1, "primitive unit minor")
minor_gcd = PR.zero()
for _cols, value in nonzero:
    minor_gcd = gcd(minor_gcd, value)
check(minor_gcd == 1, "minor gcd one")

toy_locator = prod(X - a for a in (F(0), F(1), F(2), F(3), F(4), F(5)))
toy_roots = [a for a in F if toy_locator(a) == 0]
exceptional = [a for a in toy_roots if lex_anchor(a) == 0]
check(len(toy_roots) == 6 and len(exceptional) == 1 <= lex_anchor.degree(),
      "anchor exceptional-root bound")

print("M31 c=2048 65-column fixed-anchor Sage replay")
print("profiles=261192 floor36=172 floor65=156 faces65=34 bideep65=122")
print("index_prefix=%s low_rows=50 syzygy_dim=3335543" % prefix[:4])
print("anchor_incidences=%s" % incidences)
print("target_field_collision_endpoint=%s" % lo)
print("checks=%s" % checks)
print("PASS")
