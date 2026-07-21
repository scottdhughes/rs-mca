#!/usr/bin/env sage
"""Independent Sage replay for the M31 fixed-remainder C1 boundary source."""

from itertools import combinations


CHECKS = 0


def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise RuntimeError(label)


def ceil_div(numerator, denominator):
    check(denominator > 0, "positive denominator")
    return (numerator + denominator - 1) // denominator


# Deployed exact arithmetic, independently of the Python verifier.
p = 2^31 - 1
n = 2^21
K = 2^20
A = 1116023
radius = n - A
Bstar = p^4 // 2^100
c = 2048
Nq = n // c
r = 1911
f = 544
t = 32
floor_value = ceil_div(binomial(Nq - 1, f), p^t)
degree_upper = r + c * (f - t - 1)

check(p == 2147483647, "Mersenne prime")
check((n, K, A, radius) == (2097152, 1048576, 1116023, 981129),
      "deployed row")
check(Bstar == 16777215, "deployed budget")
check(Nq == 1024, "quotient size")
check(r + c * f == A, "agreement decomposition")
check(c * t + r == A - K == 67447, "prefix decomposition")
check(degree_upper == 1048439 and K - degree_upper == 137,
      "strict degree gate")
check(floor_value == 6796405, "fixed-remainder floor")
check((2^2047) % p != 0, "Chebyshev leading coefficient invertible")
check(floor_value - 45 == 6796360, "T46 floor")
check(floor_value - 45 - 259880 == 6536480, "raw T46 route cut")
check(3730 + 45 * (366969 - 1) == 16517290, "boundary deficit")
check(16517335 + 259880 == Bstar, "signed target is Q budget")
check(Nq - 1 - f == 479, "C1 complement complete fibers")
check(c - r == 137, "C1 complement remainder")
check(479 * c + 137 == radius, "C1 complement identity")
check(r <= A - K and 137 <= A - K, "agreement/complement QR2 visibility")


# Exhaustive GF(17) polynomial-fold control.
F = GF(17)
RX = PolynomialRing(F, "X")
X = RX.gen()
RY = PolynomialRing(F, "Y")
Y = RY.gen()
D = tuple(F(i) for i in range(1, 17))
phi = X^2
Q = tuple(sorted(set(phi(x) for x in D), key=lambda value: int(value)))
b0 = F(1)
R0 = (F(1),)
toy_f = 3
toy_t = 1
toy_K = 4
toy_A = 7

check(Q == tuple(F(i) for i in (1, 2, 4, 8, 9, 13, 15, 16)),
      "toy quotient image")
check(tuple(x for x in D if phi(x) == b0) == (F(1), F(16)),
      "toy complete reserved fiber")

P_R0 = prod(X - point for point in R0)
buckets = {}
for E in combinations(tuple(value for value in Q if value != b0), toy_f):
    V = prod(Y - value for value in E)
    prefix = (int(V[toy_f - 1]),)
    composed = RX(V(phi))
    locator_polynomial = P_R0 * composed
    support = tuple(x for x in D if locator_polynomial(x) == 0)
    check(locator_polynomial.is_monic() and locator_polynomial.degree() == toy_A,
          "toy monic support locator")
    check(len(support) == toy_A, "toy exact locator roots")
    buckets.setdefault(prefix, []).append((E, support, locator_polynomial))

heavy_prefix = min(buckets, key=lambda key: (-len(buckets[key]), key))
heavy = buckets[heavy_prefix]
check(len(buckets) == 16, "toy attained quotient prefixes")
check(heavy_prefix == (1,) and len(heavy) == 3, "toy heavy bucket")
check(len(heavy) == ceil_div(binomial(7, 3), 17), "toy exact floor")

L0 = heavy[0][2]
global_prefix = tuple(int(L0[toy_A - index]) for index in range(1, toy_A - toy_K + 1))
check(global_prefix == (16, 1, 16), "toy global prefix")
U = sum(L0[degree] * X^degree for degree in range(toy_K, toy_A + 1))
codewords = []
structured_supports = set()
for E, support, L in heavy:
    check(tuple(int(L[toy_A - index]) for index in range(1, toy_A - toy_K + 1))
          == global_prefix, "toy common monomial prefix")
    codeword = U - L
    check(codeword.degree() < toy_K, "toy codeword degree")
    agreements = tuple(x for x in D if codeword(x) == U(x))
    check(agreements == support and len(agreements) == toy_A,
          "toy exact agreement")
    codewords.append(codeword)
    structured_supports.add(tuple(int(x) for x in support))
check(len(set(codewords)) == 3, "toy codeword injection")

full_prefix_fiber = []
for support in combinations(D, toy_A):
    L = prod(X - point for point in support)
    prefix = tuple(int(L[toy_A - index]) for index in range(1, toy_A - toy_K + 1))
    if prefix == global_prefix:
        full_prefix_fiber.append(tuple(int(x) for x in support))
check(len(full_prefix_fiber) == 3, "toy complete global prefix fiber")
check(set(full_prefix_fiber) == structured_supports,
      "toy structured bucket equals complete fiber")

# The constructed list remains base-field-valued after target-field extension.
Fext = GF(17^2, "z")
RXext = PolynomialRing(Fext, "X")
Xext = RXext.gen()
for codeword in codewords:
    lifted = RXext([Fext(int(coefficient)) for coefficient in codeword.list()])
    check(lifted.degree() < toy_K, "toy extension lift")
    check(all(coefficient in Fext.prime_subfield() for coefficient in lifted),
          "toy codeword remains in base field")


# Independent moving-cutoff optimizer and baseline transition.
def balanced_pair_lower(member_count, set_size):
    quotient, remainder = divmod(member_count * set_size, n)
    return n * quotient * (quotient - 1) // 2 + remainder * quotient


def feasible(member_count, set_size):
    return balanced_pair_lower(member_count, set_size) <= binomial(member_count, 2) * (K - 1)


caps = {}
cap = 1
for cutoff in range(K // 2, radius):
    set_size = n - cutoff
    if set_size^2 <= n * (K - 1):
        break
    check(feasible(cap, set_size), "Sage moving cap feasible")
    while feasible(cap + 1, set_size):
        cap += 1
    check(not feasible(cap + 1, set_size), "Sage moving first exclusion")
    caps[cutoff] = cap
check(len(caps) == 89955 and max(caps) == 614242,
      "Sage optimizer domain")


def baseline_row(baseline):
    rows = []
    for cutoff, low_cap in caps.items():
        safe = Bstar - low_cap - baseline * (radius - cutoff)
        rows.append((safe, cutoff, low_cap))
    best = max(row[0] for row in rows)
    ties = [(cutoff, low_cap) for safe, cutoff, low_cap in rows if safe == best]
    return best, ties


b27, ties27 = baseline_row(27)
b28, ties28 = baseline_row(28)
b29, ties29 = baseline_row(29)
b45, ties45 = baseline_row(45)
check((b27, ties27[0]) == (6865515, (614134, 2835)), "Sage baseline27")
check((b28, ties28[0]) == (6498523, (614137, 2916)), "Sage baseline28")
check((b29, ties29[0]) == (6131533, (614139, 2972)), "Sage baseline29")
check((b45, ties45[0]) == (259880, (614160, 3730)), "Sage baseline45")
check(b27 - (floor_value - 27) == 69137, "Sage baseline27 headroom")
check(b28 - (floor_value - 28) == -297854, "Sage baseline28 route cut")
check(b29 - (floor_value - 29) == -664843, "Sage baseline29 route cut")


def ordered_prefix_max(total, count, prefix_count):
    quotient, remainder = divmod(total, count)
    return prefix_count * quotient + max(0, remainder - (count - prefix_count))


S = 2 * radius - K - 1
check(S == 913681, "Sage joint index sum")
check(ordered_prefix_max(S, 26, 1) == 35141, "Sage rank28 first sum")
check(ordered_prefix_max(S, 26, 2) == 70282, "Sage rank28 two sum")
check(ordered_prefix_max(S, 27, 2) == 67680, "Sage rank29 two sum")
check(ordered_prefix_max(S, 28, 2) == 65262, "Sage rank30 two sum")
check(35141 < 67447 < 70282, "Sage rank28 cutoff")
check(67680 > 67447 > 65262, "Sage two-row transition")

print("M31 Chebyshev fixed-remainder C1 boundary-source independent Sage replay: PASS")
print("deployed: floor=6796405 T46_floor=6796360 degree_headroom=137")
print("route: agreement=(544,1911) complement=(479,137) -> removed by/at C1 under declared order")
print("toy: structured=3 complete_prefix_fiber=3 exact_boundary=True")
print("optimizer: b27_margin=69137 b28_margin=-297854 b29_margin=-664843")
print("Forney: p1_28=35141 p2_28=70282 p2_29=67680 p2_30=65262")
print("scope: C1 numerical payment and variable-R residual OPEN; ledger movement 0")
print("checks=%s" % CHECKS)
