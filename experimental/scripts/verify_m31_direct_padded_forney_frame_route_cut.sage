#!/usr/bin/env sage
"""Sage replay for M31 padded-frame cross-check and coloop elimination.

The deployed layer is exact integer arithmetic.  The finite-field layer uses
an existing source-realized F_31 Reed--Solomon fixture to recover the complete
Forney profile from truncated Macaulay kernels, constructs three exact low
syzygies, checks Pluecker complementary-gcd divisibility and every one-column
deletion, and replays the F_11 padding-order counterpacket.  These are exact
controls, not a deployed M31 enumeration.
"""

import json
from itertools import combinations
from pathlib import Path


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def ordered_prefix(total, count, prefix):
    q, r = divmod(total, count)
    return prefix * q + max(0, r - (count - prefix))


def polynomial_gcd(polynomials):
    result = polynomials[0]
    for polynomial in polynomials[1:]:
        result = gcd(result, polynomial)
    return result.monic()


def macaulay_matrix(polynomials, degree_bound):
    degree = polynomials[0].degree()
    field = polynomials[0].base_ring()
    if degree_bound == 0:
        return Matrix(field, degree, 0)
    output = Matrix(field, degree + degree_bound,
                    len(polynomials) * degree_bound)
    for index, polynomial in enumerate(polynomials):
        for shift in range(degree_bound):
            column = index * degree_bound + shift
            for exponent in range(degree + 1):
                output[exponent + shift, column] = polynomial[exponent]
    return output


def kernel_vector_to_polynomial_row(vector, count, degree_bound, ring):
    return [sum((vector[index * degree_bound + shift] * ring.gen()^shift
                 for shift in range(degree_bound)), ring.zero())
            for index in range(count)]


# ---------------------------------------------------------------- deployed
p = 2^31 - 1
n = 2^21
K = 2^20
a = 1116023
w = a - K
radius = n - a
budget = p^4 // 2^100
forbidden = budget + 1
forced_keys = 259881
safe_allowance = forced_keys - 1
small_total = radius - w - 1

check((p, n, K, a, w, radius) ==
      (2147483647, 2097152, 1048576, 1116023, 67447, 981129),
      "deployed constants")
check((budget, forbidden) == (16777215, 16777216), "deployed budget")
check(small_total == 913681, "common-syndrome small total")
check(divmod(small_total, 44) == (20765, 21), "small-total division")
prefixes = tuple(ordered_prefix(small_total, 44, k) for k in range(1, 5))
check(prefixes == (20765, 41530, 62295, 83060), "deployed prefix caps")
check(prefixes[2] < w < prefixes[3], "rank-three endpoint")
check(w - prefixes[2] == 5152, "rank-three margin")
check(44 - small_total // w == 31, "low-index count")

widths = {columns: ordered_prefix(small_total, columns - 2, 3)
          for columns in range(5, 47)}
minimum_width = min(columns for columns, value in widths.items() if value < w)
check(minimum_width == 43, "minimum packet width")
check((widths[42], widths[43], widths[46]) == (68526, 66852, 62295),
      "packet-width boundary")
resources, residual = divmod(safe_allowance, prefixes[2])
check((resources, residual) == (4, 10700), "root-union allowance")
check(5 * prefixes[2] - safe_allowance == 51595, "fifth resource excess")


# ------------------------------------- source-realized F31 syndrome/Forney
repo_root = Path(__file__).resolve().parents[2]
fixture_path = (repo_root /
                "experimental/data/certificates/rank16-left-kernel-forney/f31_fixture.json")
fixture = json.loads(fixture_path.read_text())
check(fixture["field"] == 31 and fixture["dimension"] == 15 and
      fixture["agreement"] == 16, "F31 fixture parameters")

F31 = GF(31)
R31.<X> = PolynomialRing(F31)
domain31 = [F31(value) for value in fixture["evaluation_set"]]
supports31 = [set(F31(value) for value in support)
              for support in fixture["supports"]]
toy_K = fixture["dimension"]
toy_a = fixture["agreement"]
toy_w = toy_a - toy_K
check(toy_w == 1 and len(supports31) == 16, "F31 fixture shape")
check(len(set().union(*supports31)) == 30, "F31 full union")

# y(x)=x^16 and c_T=x^16-Lambda_T are genuine distinct degree-<15 words
# agreeing exactly on T.
received31 = X^fixture["received_word_exponent"]
codewords31 = []
for support in supports31:
    locator = prod(X - point for point in support)
    codeword = received31 - locator
    check(codeword.degree() < toy_K, "F31 codeword degree")
    agreements = {point for point in domain31
                  if codeword(point) == received31(point)}
    check(agreements == support, "F31 exact agreement support")
    codewords31.append(codeword)
check(len(set(codewords31)) == len(codewords31), "F31 distinct codewords")

union31 = set().union(*supports31)
locators31 = [prod(X - point for point in union31 - support)
              for support in supports31]
degree31 = len(union31) - toy_a
check(degree31 == 14, "F31 primitive degree")
check(all(locator.is_monic() and locator.degree() == degree31
          for locator in locators31), "F31 equal-degree locators")
check(polynomial_gcd(locators31).degree() == 0, "F31 primitive row")

nullities = [0]
matrices = {}
for degree_bound in range(1, 4):
    matrix = macaulay_matrix(locators31, degree_bound)
    matrices[degree_bound] = matrix
    nullities.append(matrix.ncols() - matrix.rank())
check(nullities == [0, 2, 16, 31], "F31 Macaulay nullities")

profile = []
previous_cumulative = 0
for degree in range(3):
    cumulative = nullities[degree + 1] - nullities[degree]
    exact = cumulative - previous_cumulative
    check(exact >= 0, "F31 profile multiplicity")
    profile.extend([degree] * exact)
    previous_cumulative = cumulative
check(profile == [0, 0] + [1] * 12 + [2], "F31 Forney profile")
check(sum(profile) == degree31, "F31 Forney sum")
h31 = sum(max(0, index - toy_w) for index in profile)
check(h31 == 1 and max(profile) == toy_w + 1, "F31 common syndrome defect")

# Build the first three low rows: the two constant relations and one new
# degree-one relation.  Rank is checked over the fraction field by Sage.
constant_vectors = matrices[1].right_kernel().basis()
check(len(constant_vectors) == 2, "F31 constant syzygies")
rows31 = [kernel_vector_to_polynomial_row(kernel_vector, len(locators31), 1, R31)
          for kernel_vector in constant_vectors]
for kernel_vector in matrices[2].right_kernel().basis():
    candidate = kernel_vector_to_polynomial_row(
        kernel_vector, len(locators31), 2, R31
    )
    trial = Matrix(R31, rows31 + [candidate])
    if trial.rank() == 3:
        rows31.append(candidate)
        break
check(len(rows31) == 3, "F31 rank-three low frame found")
B31 = Matrix(R31, rows31)
row_degrees31 = tuple(max(entry.degree() if entry else -1 for entry in row)
                      for row in rows31)
check(row_degrees31 == (0, 0, 1), "F31 first-three degrees")
check(B31 * vector(R31, locators31) == vector(R31, [0, 0, 0]),
      "F31 exact syzygy equations")
check(B31.rank() == 3, "F31 syzygy rank")

# One-column deletion is injective on the exact syzygy row space.  In
# particular the last column can be distinguished and an anchor-only basis
# triple exists.
for deleted in range(len(locators31)):
    kept = [column for column in range(len(locators31)) if column != deleted]
    check(B31.matrix_from_columns(kept).rank() == 3,
          "F31 one-column deletion")

nonzero_minors = 0
old_anchor_minor = None
for columns in combinations(range(len(locators31)), 3):
    minor = B31.matrix_from_columns(columns).det()
    complement = [locators31[index] for index in range(len(locators31))
                  if index not in columns]
    common = polynomial_gcd(complement)
    check(minor % common == 0, "F31 Pluecker/gcd divisibility")
    if minor:
        nonzero_minors += 1
        check(minor.degree() <= sum(row_degrees31), "F31 minor degree")
        check(common.degree() <= minor.degree(), "F31 relative core degree")
        if max(columns) < len(locators31) - 1 and old_anchor_minor is None:
            old_anchor_minor = columns
check(nonzero_minors > 0, "F31 nonzero minor")
check(old_anchor_minor is not None, "F31 old-anchor basis minor")


# --------------------------------------------- F11 padding-order regression
F11 = GF(11)
R11.<Y> = PolynomialRing(F11)
domain11 = [F11(value) for value in range(9)]
c0 = R11.zero()
c1 = Y * (Y - 1) * (Y - 2)
received_values = [F11(value) for value in (0, 0, 0, 0, 0, 0, 10, 1, 6)]
agreements0 = {point for point, value in zip(domain11, received_values)
               if c0(point) == value}
agreements1 = {point for point, value in zip(domain11, received_values)
               if c1(point) == value}
check(agreements0 == set(F11(value) for value in (0, 1, 2, 3, 4, 5)),
      "F11 agreements c0")
check(agreements1 == set(F11(value) for value in (0, 1, 2, 6, 7, 8)),
      "F11 agreements c1")


def selected_locator(order, agreements, count):
    selected = []
    for point in order:
        if point in agreements:
            selected.append(point)
            if len(selected) == count:
                break
    roots = set(domain11) - set(selected)
    return prod(Y - point for point in roots)


cross_order = [F11(value) for value in (0, 1, 2, 3, 4, 5, 6, 7, 8)]
common_order = [F11(value) for value in (0, 1, 3, 4, 5, 6, 7, 8, 2)]
cross = [selected_locator(cross_order, agreements, 5)
         for agreements in (agreements0, agreements1)]
common = [selected_locator(common_order, agreements, 5)
          for agreements in (agreements0, agreements1)]
actual = [prod(Y - point for point in set(domain11) - agreements)
          for agreements in (agreements0, agreements1)]


def primitive_pair_index(pair):
    return pair[0].degree() - gcd(pair[0], pair[1]).degree()


check((primitive_pair_index(actual), primitive_pair_index(cross),
       primitive_pair_index(common)) == (3, 2, 3),
      "F11 actual/cross/common profiles")


print("Sage M31 padded-frame cross-check and coloop elimination: PASS")
print("deployed direct rank3: 62295 < 67447; margin 5152")
print("F31 source profile:", profile, "h=", h31,
      "low row degrees=", row_degrees31)
print("F31 nonzero minors:", nonzero_minors,
      "old-anchor basis:", old_anchor_minor)
print("F11 pair indices: actual=3, cross-padded=2, common-padded=3")
print("padded rank3: CONSUMED FROM PR #1021; rank-two coloop: ELIMINATED")
print("remaining: UNPAID_CANONICAL_LOCATOR_NUMERATOR_ESCAPE_OWNER_REFUND")
print("M31 row: OPEN; ledger movement: 0")
