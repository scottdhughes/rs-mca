#!/usr/bin/env sage
"""Independent Sage replay of the rank-nine GM--MDS fixed-domain gate.

This CONTROL_ONLY_J10 script reconstructs the exact GF(127) eleven-locator intersection
failure, specialization exception, and full-rank control, plus the transparent
GF(11) three-quadratic exception.  It does not read the Python certificate
and is not a deployed-scale polynomial/rank executor.
"""

from itertools import combinations


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def gm_violations(supports, degree):
    answer = []
    minimum_slack = None
    for size in range(1, len(supports) + 1):
        for indices in combinations(range(len(supports)), size):
            common = set(supports[indices[0]])
            for index in indices[1:]:
                common.intersection_update(supports[index])
            bound = degree + 1 - size
            slack = bound - len(common)
            minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
            if slack < 0:
                answer.append((indices, tuple(sorted(common)), bound, -slack))
    require(minimum_slack is not None, "empty GM scan")
    return answer, minimum_slack


def locator_matrix(field, supports):
    RX = PolynomialRing(field, "X")
    X = RX.gen()
    degree = len(supports[0])
    polynomials = [prod(X - field(point) for point in support) for support in supports]
    require(all(polynomial.is_monic() for polynomial in polynomials),
            "a locator is not monic")
    require(all(polynomial.degree() == degree for polynomial in polynomials),
            "locator degree drift")
    matrix_rows = matrix(
        field,
        [[polynomial[coefficient] for coefficient in range(degree + 1)]
         for polynomial in polynomials],
    )
    return RX, X, polynomials, matrix_rows


def normalized_left_relation(matrix_rows):
    kernel = matrix_rows.left_kernel()
    require(kernel.dimension() > 0, "left kernel is trivial")
    relation = kernel.basis()[0]
    first = next(value for value in relation if value != 0)
    relation = relation / first
    require(relation * matrix_rows == 0, "left relation failed")
    return relation


# -------------------------------------------------------------------------
# Deployed arithmetic and the missing-input guard.
# -------------------------------------------------------------------------

p_kb = ZZ(2 ** 31 - 2 ** 24 + 1)
q_kb = p_kb ** 6
n_kb = ZZ(2 ** 21)
k_kb = ZZ(2 ** 20)
A_kb = ZZ(1_116_048)
R_kb = n_kb - k_kb
j_kb = n_kb - A_kb
K_lovett_kb = j_kb + 1

require(p_kb.is_prime(), "KoalaBear base modulus is not prime")
require((R_kb, j_kb, K_lovett_kb) == (1_048_576, 981_104, 981_105),
        "deployed dimensions drift")
require(p_kb >= n_kb + K_lovett_kb - 1,
        "deployed field-size inequality drift")
require(q_kb == p_kb ** 6, "extension degree drift")

actual_retained_11_tuple_supplied = False
deployed_scale_executor_implemented = False
require(not actual_retained_11_tuple_supplied,
        "this replay must not invent a deployed support tuple")
require(not deployed_scale_executor_implemented,
        "this control must not claim a deployed-scale executor")


# -------------------------------------------------------------------------
# Same-shape GF(127) fixed-domain specialization exception.
# -------------------------------------------------------------------------

F = GF(127)
core8 = set(range(4, 12))
exception_supports = [
    tuple(sorted(core8 | {1, 126})),
    tuple(sorted(core8 | {2, 125})),
    tuple(sorted(core8 | {3, 124})),
]
used = set().union(*(set(support) for support in exception_supports))
remainder = [point for point in range(127) if point not in used]
exception_supports += [
    tuple(remainder[10 * block : 10 * (block + 1)])
    for block in range(8)
]
exception_domain = set().union(*(set(support) for support in exception_supports))

require(len(exception_supports) == 11, "exception locator count drift")
require(all(len(support) == 10 for support in exception_supports),
        "exception locator degree drift")
require(len(exception_domain) == 94, "exception domain size drift")
require(127 >= len(exception_domain) + 11 - 1,
        "exception left the GM--MDS field-size envelope")

violations, minimum_slack = gm_violations(exception_supports, 10)
require(len(violations) == 0 and minimum_slack >= 0,
        "exception is not GM--MDS admissible")
RX, X, exception_polynomials, exception_matrix = locator_matrix(F, exception_supports)
require(exception_matrix.rank() == 10, "exception coefficient rank drift")
relation = normalized_left_relation(exception_matrix)
require(list(map(ZZ, relation)) == [1, 100, 26] + [0] * 8,
        "exception normalized relation drift")
require(F(47) * exception_polynomials[0]
        + exception_polynomials[1]
        + F(79) * exception_polynomials[2] == 0,
        "declared exception relation failed")


# -------------------------------------------------------------------------
# Same-shape GF(127) GM intersection failure.
# -------------------------------------------------------------------------

core9 = set(range(4, 13))
failure_supports = [
    tuple(sorted(core9 | {1})),
    tuple(sorted(core9 | {2})),
    tuple(sorted(core9 | {3})),
]
used_failure = set().union(*(set(support) for support in failure_supports))
remainder_failure = [point for point in range(127) if point not in used_failure]
failure_supports += [
    tuple(remainder_failure[10 * block : 10 * (block + 1)])
    for block in range(8)
]
failure_domain = set().union(*(set(support) for support in failure_supports))

require(len(failure_domain) == 92, "failure domain size drift")
require(127 >= len(failure_domain) + 11 - 1,
        "failure left the GM--MDS field-size envelope")
failure_violations, failure_minimum_slack = gm_violations(failure_supports, 10)
require(failure_minimum_slack == -1, "failure minimum slack drift")
require(failure_violations[0][0] == (0, 1, 2),
        "first failed subfamily drift")
require(failure_violations[0][1] == tuple(range(4, 13)),
        "failed common core drift")
require(failure_violations[0][2:] == (8, 1),
        "failed bound/excess drift")
pair_johnson_distances = [
    10 - len(set(failure_supports[left]) & set(failure_supports[right]))
    for left, right in combinations((0, 1, 2), 2)
]
require(pair_johnson_distances == [1, 1, 1],
        "failure Johnson distances drift")
_, _, failure_polynomials, failure_matrix = locator_matrix(F, failure_supports)
require(failure_matrix.matrix_from_rows([0, 1, 2]).rank() == 2,
        "common-core subfamily did not force dependence")


# -------------------------------------------------------------------------
# Same-shape GF(127) full-rank control.
# -------------------------------------------------------------------------

full_rank_supports = [
    tuple(range(10 * block, 10 * (block + 1)))
    for block in range(11)
]
full_rank_domain = set().union(*(set(support) for support in full_rank_supports))
require(len(full_rank_domain) == 110, "full-rank domain size drift")
require(127 >= len(full_rank_domain) + 11 - 1,
        "full-rank control left field-size envelope")
full_violations, full_minimum_slack = gm_violations(full_rank_supports, 10)
require(len(full_violations) == 0 and full_minimum_slack == 0,
        "full-rank control lost GM admissibility")
_, _, full_polynomials, full_matrix = locator_matrix(F, full_rank_supports)
require(full_matrix.rank() == 11 and full_matrix.det() != 0,
        "full-rank locator matrix drift")


# -------------------------------------------------------------------------
# Transparent GF(11) specialization exception inside the size envelope.
# -------------------------------------------------------------------------

F11 = GF(11)
small_supports = [(1, 10), (2, 9), (3, 8)]
small_domain = set().union(*(set(support) for support in small_supports))
require(11 >= len(small_domain) + 3 - 1,
        "small control left field-size envelope")
small_violations, small_slack = gm_violations(small_supports, 2)
require(len(small_violations) == 0 and small_slack == 0,
        "small control lost GM admissibility")
RX11, X11, small_polynomials, small_matrix = locator_matrix(F11, small_supports)
require(small_matrix.rank() == 2, "small specialization rank drift")
small_relation = normalized_left_relation(small_matrix)
require(list(map(ZZ, small_relation)) == [1, 5, 5],
        "small normalized relation drift")
require(F11(9) * small_polynomials[0]
        + small_polynomials[1]
        + small_polynomials[2] == 0,
        "small transparent relation failed")


print("PASS independent Sage rank-nine GM--MDS fixed-domain gate v1")
print("  deployed: p=%s q=p^6 n=%s j=%s; actual 11-tuple missing" %
      (p_kb, n_kb, j_kb))
print("  GF(127): failure/common-core, admissible rank-10 exception, rank-11 control")
print("  GF(11): admissible three-quadratic rank-2 exception")
print("  CONTROL_ONLY_J10; deployed executor not implemented")
print("  no owner payment; no ledger movement")
