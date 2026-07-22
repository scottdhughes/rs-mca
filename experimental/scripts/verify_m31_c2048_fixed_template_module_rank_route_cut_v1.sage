#!/usr/bin/env sage
"""Independent Sage replay for the M31 fixed-template module-rank cut."""


P = 2^31 - 1
N = 2^21
K = 2^20
A = 1116023
C = 2048
B_STAR = P^4 // 2^100
BOUNDARY_TARGET = 9216781
U_PAID = 3730


def require(condition, label):
    if not condition:
        raise AssertionError(label)


# Exact determinant-valuation saturation fixtures.  The selected square minor
# is diagonal, so the sum of point nullities equals its degree ell*D.
F = GF(101)
R.<T> = PolynomialRing(F)
for D in range(1, 5):
    for ell in range(1, 5):
        diagonal = [prod(T - F(3 + 7*j + t) for t in range(D))
                    for j in range(ell)]
        matrix = Matrix(R, ell, ell, lambda i, j: diagonal[i] if i == j else 0)
        determinant = matrix.det()
        require(determinant != 0, "nonzero selected minor")
        require(determinant.degree() == ell*D, "minor degree saturation")
        nullity_sum = 0
        valuation_sum = 0
        for b in F:
            evaluated = Matrix(F, ell, ell,
                               [entry(b) for entry in matrix.list()])
            nullity = ell - evaluated.rank()
            valuation = determinant.valuation(T - b)
            require(nullity <= valuation, "point nullity <= determinant valuation")
            nullity_sum += nullity
            valuation_sum += valuation
        require(nullity_sum == ell*D, "summed nullity saturation")
        require(valuation_sum == determinant.degree(), "root valuation degree")


# A genuine route-cut fixture: two F-linearly independent polynomial columns
# can have only rank one over F(T).  Rank drop is therefore nonempty and cannot
# silently be identified with payment.
column_1 = vector(R, [1, T, 0])
column_2 = vector(R, [T, T^2, 0])
deficient = Matrix(R, 3, 2, lambda i, j: [column_1, column_2][j][i])
require(deficient.rank() == 1, "F(T)-rank-deficient fixture")
require(column_1 != column_2, "distinct polynomial columns")
for a in F:
    for b in F:
        if a != 0 or b != 0:
            require(a*column_1 + b*column_2 != 0,
                    "columns F-linearly independent")

# The exact one-unit failure mechanism: W=Span_F{e_0,T e_0} has nullity one
# at every field label although its F(T)-rank is one.  Taking D=50 gives
# 101 point incidences against the invalid full-rank ceiling 2D=100.
deficient_nullity_sum = 0
for b in F:
    evaluated = Matrix(F, 1, 2, [1, b])
    deficient_nullity_sum += 2 - evaluated.rank()
require(deficient_nullity_sum == 101 > 2*50,
        "rank-deficient strong-design one-unit failure")


# Independent all-profile relaxed-Singleton census.
histogram = {}
profile_count = 0
threshold_sum = 0
equality_profiles = []
source_violations = []
row_digest_input = []
for u in range(480):
    vmax = 136 if u == 0 else 544
    for v in range(vmax + 1):
        profile_count += 1
        h = u + v + 1
        r = 1911 + C*v
        f = 544 - v
        M = 1023 - u - v
        require(r + C*f == A, "profile agreement decomposition")
        require(M == 1024 - h, "available quotient labels")
        if v >= 512:
            require(r >= K, "fixed-template uniqueness")
            D = -1
            d = K - r
            L = 1
            slack = 0
            equality = 0
        else:
            D = 511 - v
            d = K - r
            require(d == C*D + 137, "module dimension")
            require(M - D == 512 - u and M > D,
                    "evaluation injectivity")
            L = None
            for candidate in range(1, C + 1):
                left = (candidate + 1)*f*(C + 1 - candidate)
                right = M*(C + 1 - candidate) + candidate*d
                if left >= right:
                    L = candidate
                    slack = left - right
                    equality = ZZ(left == right)
                    break
            require(L is not None, "threshold exists")
            require(d - 1 - D*(C + 1 - L) == 136 + D*(L - 1),
                    "design comparison identity")
        histogram[L] = histogram.get(L, 0) + 1
        threshold_sum += L
        if equality:
            equality_profiles.append([u, v, L])
        t = min(32, f)
        source_floor = (binomial(M, f) + P^t - 1) // P^t
        if source_floor > L:
            source_violations.append([u, v, L, source_floor])

expected_histogram = {
    1:32703, 2:16896, 3:16657, 4:16486, 5:16349, 6:16227,
    7:16092, 8:15957, 9:15833, 10:15705, 11:15574,
    12:15447, 13:15314, 14:15184, 15:13886, 16:6170, 17:712,
}
expected_equality = [
    [31,365,14], [91,400,12], [223,239,8], [285,266,6],
]
require(profile_count == 261192, "profile count")
require(histogram == expected_histogram, "threshold histogram")
require(threshold_sum == 1988814, "threshold sum")
require(max(histogram) == 17, "maximum threshold")
require(equality_profiles == expected_equality, "equality profiles")
require(len(source_violations) == 193, "rank-one source violation count")
require(sum(1 for row in source_violations if row[2] == 17) == 176,
        "rank-one threshold-17 source count")
require(sum(1 for row in source_violations if row[2] == 16) == 17,
        "rank-one threshold-16 source count")
require(max(source_violations, key=lambda row: row[3]) ==
        [0, 0, 17, 6796405], "largest rank-one source")
require(next(row for row in source_violations if row[:2] == [1, 1]) ==
        [1, 1, 17, 1693898], "largest bideep rank-one source")
require(BOUNDARY_TARGET - threshold_sum == 7227967,
        "conditional boundary target margin")
require(U_PAID + threshold_sum == 1992544,
        "conditional low-plus-profile total")
require(B_STAR - U_PAID - threshold_sum == 14784671,
        "conditional B-star margin")

print("M31 c=2048 fixed-template module-rank Sage replay")
print("determinant valuation: PASS")
print("F-linear independent / F(T)-rank-drop fixture: PASS")
print("profiles=%d threshold_sum=%d max=%d equality=%d source_violations=%d" %
      (profile_count, threshold_sum, max(histogram), len(equality_profiles),
       len(source_violations)))
