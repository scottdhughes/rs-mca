#!/usr/bin/env sage
"""Independent Sage replay for the c=2048 occupancy/30-carrier packet."""

from collections import Counter, defaultdict
from itertools import combinations


CHECKS = 0


def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(label)


# Deployed exact arithmetic, independent of the Python verifier.
p = 2^31 - 1
n = 2^21
K = 2^20
A = 1116023
R = n - A
w = A - K
Bstar = p^4 // 2^100
c = 2048
N = n // c
S = 2 * R - K - 1
D0 = K - R

check((p, n, K) == (2147483647, 2097152, 1048576), "deployed base")
check((A, R, w, Bstar) == (1116023, 981129, 67447, 16777215),
      "deployed row")
check((N, R // c, R % c, A // c, A % c) ==
      (1024, 479, 137, 544, 1911), "Euclidean fiber data")
check((S, D0) == (913681, 67447), "coupled constants")


# Enumerate the deployed profile pairs from the partial-fiber inequalities.
profiles = []
for m in range(N + 1):
    for z in range(N - m + 1):
        h = N - m - z
        r_err = R - c * m
        r_agr = A - c * z
        if r_err < 0 or r_agr < 0 or r_err + r_agr != c * h:
            continue
        feasible = (h > 0 and h <= r_err <= h * (c - 1)
                    and h <= r_agr <= h * (c - 1))
        if feasible:
            profiles.append((479 - m, 544 - z, m, z, h, r_err, r_agr))

profiles.sort()
pairs = {(row[0], row[1]) for row in profiles}
expected = ({(0, v) for v in range(137)}
            | {(u, v) for u in range(1, 480) for v in range(545)})
check(pairs == expected, "exact deployed feasible set")
check(len(profiles) == 261192, "profile count")

faces = {(u, v) for u, v in pairs if u == 0 or v == 0}
bideep = {(u, v) for u, v in pairs if u >= 1 and v >= 1}
arms = {(u, v) for u, v in bideep if u <= 32 or v <= 32}
core = {(u, v) for u, v in bideep if u >= 33 and v >= 33}
check((len(faces), len(bideep), len(arms), len(core)) ==
      (616, 260576, 31712, 228864), "partition counts")
check(not (faces & bideep) and faces | bideep == pairs,
      "face/deep partition")
check(not (arms & core) and arms | core == bideep,
      "arm/core partition")
check((0, 136) in pairs and (0, 137) not in pairs,
      "sharp u=0 endpoint")
check(137 + 2048 * 32 == 65673 <= w < 67721 == 137 + 2048 * 33,
      "error visible-arm threshold")
check(1911 + 2048 * 32 == w < 69495 == 1911 + 2048 * 33,
      "agreement visible-arm threshold")


# Exact 30/29/65 aggregate coupled-index thresholds.
def partial(columns, rows):
    return floor(rows * S / (columns - 2))


check((partial(30, 1), partial(30, 2)) == (32631, 65262),
      "30-column partial sums")
check(partial(30, 2) < D0 < partial(29, 2) == 67680,
      "minimal 30-column transition")
check(min(m for m in range(4, 100) if partial(m, 2) < D0) == 30,
      "first aggregate two-row width")
check((partial(65, 1), partial(65, 2)) == (14502, 29005),
      "65-column partial sums")
check(29 * len(bideep) == 7556704, "bi-deep residual cap")
early = Bstar - 3730 - 7556704
check(early == 9216781 and early - 6796405 == 2420376,
      "conditional boundary budget")
check(3730 + 7556704 + early == Bstar, "boundary allocation identity")
check(64 * len(profiles) == 16716288 < Bstar, "raw 65 pigeonhole")
check(64 * len(bideep) == 16676864 < Bstar, "deep 65 pigeonhole")


# Exact GF(17)^* control with four complete x^4 fibers of size four.
F = GF(17)
RX = PolynomialRing(F, "X")
X = RX.gen()
RZ = PolynomialRing(F, "Z")
Z = RZ.gen()
trunc = RZ.quotient(Z^4, "zbar")
D = tuple(F(i) for i in range(1, 17))
phi = X^4
fiber_map = {
    value: tuple(point for point in D if point^4 == value)
    for value in set(point^4 for point in D)
}
fiber_map = dict(sorted(fiber_map.items(), key=lambda item: int(item[0])))
check([(int(value), tuple(int(point) for point in fiber))
       for value, fiber in fiber_map.items()] == [
           (1, (1, 4, 13, 16)),
           (4, (6, 7, 10, 11)),
           (13, (3, 5, 12, 14)),
           (16, (2, 8, 9, 15)),
       ], "toy complete fibers")


def reverse_polynomial(poly):
    degree = poly.degree()
    return sum(poly[degree - index] * Z^index for index in range(degree + 1))


histogram = Counter()
error_recovery_buckets = defaultdict(set)
agreement_recovery_buckets = defaultdict(set)
false_qr_buckets = defaultdict(list)

for support_tuple in combinations(D, 7):
    support = set(support_tuple)
    occupancy = {
        value: sum(point in support for point in fiber)
        for value, fiber in fiber_map.items()
    }
    m = sum(value == 4 for value in occupancy.values())
    z = sum(value == 0 for value in occupancy.values())
    u = 1 - m
    v = 2 - z
    histogram[(u, v)] += 1

    L = prod(X - point for point in support_tuple)
    prefix = tuple(int(L[7 - index]) for index in range(1, 4))
    full_error = tuple(value for value, count in occupancy.items() if count == 4)

    # Error-side visible face: fixed full-fiber quotient and prefix determine
    # the degree-three partial locator exactly by reciprocal unit division.
    if u == 0:
        full_points = set().union(*(set(fiber_map[value]) for value in full_error))
        remainder = tuple(sorted(support - full_points, key=int))
        B = prod(X^4 - value for value in full_error)
        P_R = prod(X - point for point in remainder)
        check(L == P_R * B and P_R.degree() == 3, "toy error factorization")
        recovered = trunc(reverse_polynomial(L)) / trunc(reverse_polynomial(B))
        check(recovered == trunc(reverse_polynomial(P_R)),
              "toy reciprocal error recovery")
        error_recovery_buckets[(tuple(map(int, full_error)), prefix)].add(
            tuple(map(int, remainder))
        )

    # Complementary agreement-side face, checked with its own locator prefix.
    agreement = set(D) - support
    if v == 0:
        full_agreement = tuple(
            value for value, fiber in fiber_map.items()
            if set(fiber).issubset(agreement)
        )
        full_points = set().union(*(set(fiber_map[value]) for value in full_agreement))
        remainder = tuple(sorted(agreement - full_points, key=int))
        L_A = prod(X - point for point in agreement)
        B_A = prod(X^4 - value for value in full_agreement)
        P_A = prod(X - point for point in remainder)
        prefix_A = tuple(int(L_A[9 - index]) for index in range(1, 4))
        check(L_A == P_A * B_A and P_A.degree() == 1,
              "toy agreement factorization")
        recovered_A = trunc(reverse_polynomial(L_A)) / trunc(reverse_polynomial(B_A))
        check(recovered_A == trunc(reverse_polynomial(P_A)),
              "toy reciprocal agreement recovery")
        agreement_recovery_buckets[(tuple(map(int, full_agreement)), prefix_A)].add(
            tuple(map(int, remainder))
        )

    # Guard against falsely extending QR2 to a bi-deep partial remainder.
    if (u, v) == (1, 1):
        false_qr_buckets[(tuple(map(int, full_error)), prefix)].append(
            tuple(sorted(map(int, support)))
        )

check(histogram == Counter({
    (0, 0): 48,
    (0, 1): 576,
    (0, 2): 256,
    (1, 1): 2496,
    (1, 2): 8064,
}), "toy profile histogram")
check(sum(histogram.values()) == binomial(16, 7) == 11440,
      "toy support exhaustion")
check(all(len(values) == 1 for values in error_recovery_buckets.values()),
      "toy error visible recovery injective")
check(all(len(values) == 1 for values in agreement_recovery_buckets.values()),
      "toy agreement visible recovery injective")

collision_key = ((), (12, 12, 14))
collision_pair = [
    (1, 2, 3, 4, 5, 8, 16),
    (1, 4, 6, 7, 10, 13, 15),
]
check(false_qr_buckets[collision_key][:2] == collision_pair,
      "toy bi-deep prefix collision")
check(collision_pair[0] != collision_pair[1],
      "toy collision has distinct partial labels")

print("M31 c=2048 occupancy / 30-carrier Sage replay: PASS")
print("atlas: 261192 = 616 + 260576; arms/core = 31712/228864")
print("Forney: width30=65262<67447<67680=width29")
print("GF(17): 11440 supports exhausted; visible recovery and false-QR guard PASS")
print("scope: exact target arithmetic + toy algebra; carrier owner remains OPEN")
print("checks=%s" % CHECKS)
