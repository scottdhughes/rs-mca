#!/usr/bin/env sage
"""Independent Sage replay for the M31 multiprefix/carrier packet."""

from itertools import combinations


checks = 0


def check(condition, label):
    global checks
    checks += 1
    if not condition:
        raise RuntimeError(label)


def ceil_div(a, b):
    check(a >= 0 and b > 0, "ceil-div domain")
    return (a + b - 1) // b


# Deployed exact arithmetic and independent activation census.
p = 2^31 - 1
n = 2^21
K = 2^20
A = 1116023
RADIUS = n - A
w = A - K
c = 2048
N = n // c

check(p == 2147483647, "deployed prime")
check(RADIUS == 981129 and w == 67447, "deployed row")
check(N == 1024 and w // c == 32, "deployed fold")
check(p^4 // 2^100 == 16777215, "deployed budget")

activated = []
bideep = []
threshold_activations = []
profile_count = 0
for u in range(480):
    vmax = 136 if u == 0 else 544
    for v in range(vmax + 1):
        profile_count += 1
        h = u + v + 1
        f = 544 - v
        r = 1911 + c*v
        available = 1023 - u - v
        check(r + c*f == A, "profile agreement identity")
        check(h <= r <= h*(c-1), "profile partial feasibility")
        check(f <= available, "profile quotient availability")
        t = min(32, f)
        floor_uv = ceil_div(ZZ(binomial(available, f)), ZZ(p)^t)
        if t < f:
            check(r + c*(f-t-1) == 1048439 < K,
                  "uniform fixed-template degree")
        else:
            check(floor_uv == 1, "full coefficient floor")
        if floor_uv >= 30:
            activated.append((u, v, floor_uv))
            if u >= 1 and v >= 1:
                bideep.append((u, v, floor_uv))
        if u >= 1 and v >= 1:
            index_sum_upper = 2*RADIUS - K - 1 - (137 + c*u)
            q_min = next(q for q in range(4, N + 1)
                         if 2*index_sum_upper // (q-2) < w)
            if floor_uv >= q_min:
                threshold_activations.append((u, v, floor_uv, q_min))

check(profile_count == 261192, "profile count")
check(len(activated) == 177, "activated count")
check(len(bideep) == 141, "activated bi-deep count")
check(len(threshold_activations) == 142,
      "optimized source-threshold activation count")
check({q: len([x for x in threshold_activations if x[3] == q])
       for q in set(x[3] for x in threshold_activations)} == {29: 124, 30: 18},
      "optimized threshold histogram")
check(not any(x[2] < 29 for x in threshold_activations),
      "no lower-floor optimized activation")
check([x[:3] for x in threshold_activations if x[2] == 29]
      == [(8, 10, 29)],
      "extra twenty-nine-column source")
check(max(activated, key=lambda row: row[2]) == (0, 0, 6796405),
      "global fixed-template maximum")
check(max(bideep, key=lambda row: row[2]) == (1, 1, 1693898),
      "bi-deep fixed-template maximum")

vmax_expected = [18, 17, 15, 14, 13, 12, 11, 9, 8, 7, 6, 5, 3, 2, 1]
last_floor_expected = [33, 30, 51, 46, 41, 37, 33, 54, 48, 42,
                       37, 32, 51, 44, 38]
for u, vmax, last_floor in zip(range(1, 16), vmax_expected,
                                last_floor_expected):
    row = [(v, floor_uv) for uu, v, floor_uv in bideep if uu == u]
    check(row[-1] == (vmax, last_floor), "activation staircase")

S = 2*RADIUS - K - 1
g11 = 137 + c
check(S == 913681 and g11 == 2185, "source divisor arithmetic")
check(2*(S-g11)//28 == 65106 < w, "source 30-column sharpening")
check(2*(S-g11)//27 == 67518 > w, "u=1 29-column noncertificate")
check(2*(S-(137+2*c))//27 == 67366 < w,
      "source 29-column sharpening")


# Exact GF(17) fixed-multipartial source.
F = GF(17)
PR = PolynomialRing(F, 'X')
X = PR.gen()
D = [F(x) for x in range(1, 17)]
phi = X^2
Q = sorted(set(phi(x) for x in D), key=lambda x: Integer(x))
partial = [F(1), F(2), F(3)]
partial_labels = set(phi(x) for x in partial)
available = [b for b in Q if b not in partial_labels]


def locator(points):
    return prod(X-x for x in points)


LP = locator(partial)
U = LP * phi^3
toy_supports = []
toy_codewords = []
for E in combinations(available, 3):
    support = set(partial)
    support.update(x for x in D if phi(x) in E)
    L = locator(sorted(support, key=lambda x: Integer(x)))
    codeword = U - L
    check(codeword.degree() < 8, "toy source codeword degree")
    agreements = {x for x in D if U(x) == codeword(x)}
    check(agreements == support, "toy source exact support")
    toy_supports.append(tuple(sorted(Integer(x) for x in support)))
    toy_codewords.append(tuple(Integer(a) for a in codeword.list()))

check(len(toy_supports) == 10, "toy source count")
check(len(set(toy_supports)) == 10, "toy source supports distinct")
check(len(set(toy_codewords)) == 10, "toy source codewords distinct")
check(all(len(support) == 9 for support in toy_supports),
      "toy source boundary agreement")
check(U.degree() == 9 and 9 >= 8, "toy boundary-only degree gate")


# Same-remainder, different-prefix arbitrary-word obstruction over GF(17).
S1 = {F(x) for x in [1, 2, 3, 4, 9, 13, 14, 15, 16]}
S2 = {F(x) for x in [1, 5, 6, 7, 9, 10, 11, 12, 16]}
I = S1.intersection(S2)
outside = set(D).difference(S1.union(S2))
g = locator(sorted(I, key=lambda x: Integer(x)))
check(g == X^3 + 8*X^2 + 16*X + 9, "toy bridge polynomial")
check(g.degree() == 3 < 7, "toy bridge is codeword")
check(outside == {F(8)}, "toy outside remainder")

y = {}
for x in D:
    if x in S1:
        y[x] = F(0)
    elif x in S2:
        y[x] = g(x)
    else:
        y[x] = F(1)
        check(y[x] != 0 and y[x] != g(x), "toy outside avoidance")

check({x for x in D if y[x] == 0} == S1, "toy exact zero codeword")
check({x for x in D if y[x] == g(x)} == S2, "toy exact bridge codeword")


def prefix(points, width):
    L = locator(sorted(points, key=lambda x: Integer(x)))
    degree = L.degree()
    return tuple(Integer(L[degree-i]) for i in range(1, width+1))


agreement_prefixes = (prefix(S1, 2), prefix(S2, 2))
error_prefixes = (prefix(set(D)-S1, 2), prefix(set(D)-S2, 2))
check(agreement_prefixes == ((8, 4), (8, 8)),
      "toy agreement multiprefix")
check(error_prefixes == ((9, 9), (9, 5)), "toy error multiprefix")

# Interpolate the arbitrary received word and replay Y-P=L_S H exactly.
Y = PR.lagrange_polynomial([(x, y[x]) for x in D])
check(Y.degree() < 16, "toy received interpolant")
for codeword, support in [(PR(0), S1), (g, S2)]:
    L = locator(sorted(support, key=lambda x: Integer(x)))
    quotient, remainder = (Y-codeword).quo_rem(L)
    check(remainder == 0, "toy Pade divisibility")
    check(quotient.degree() <= 6, "toy H degree")
    check(all(quotient(x) != 0 for x in set(D)-support),
          "toy H exactness outside support")


# Deployed symbolic obstruction arithmetic.
check(65 + 479 + 479 + 1 == 1024, "deployed quotient partition")
check(1911 + 137 == 2048, "deployed partial-fiber split")
check(65*2048 + 1911 == 135031 < K, "deployed bridge degree")
check(544 == 65 + 479 and 479 == RADIUS//2048,
      "deployed orientation sizes")
check(p % 2 == 1 and p > 2, "deployed unequal-sum swap gate")

print("PASS: Sage independent multiprefix/carrier replay")
print("profiles=261192 floor30=177 bideep_floor30=141 source_threshold_certified=142")
print("floor_1_1=1693898 source_30_bound=65106 source_29_bound=67366")
print("toy_source_codewords=10 toy_prefixes=%s/%s" %
      (agreement_prefixes, error_prefixes))
print("checks=%s" % checks)
