#!/usr/bin/env sage
"""Independent Sage replay for the M31 rank-six closure packet."""

from itertools import product
import json


P = Integer(2)^31 - 1
N = Integer(2)^21
K = Integer(2)^20
A = Integer(1116023)
RADIUS = N - A
W = A - K
L = Integer(15775933)
G_MIN = Integer(781458)
G_MAX = Integer(1033227)
LINE_MULTIPLICITY = Integer(15)


class VerificationError(RuntimeError):
    pass


checks = 0


def require(condition, label):
    global checks
    checks += 1
    if not bool(condition):
        raise VerificationError(label)


def falling(value, length):
    value = Integer(value)
    length = Integer(length)
    require(length >= 0 and value >= length, "legal falling factorial")
    answer = Integer(1)
    for offset in range(int(length)):
        answer *= value - offset
    return answer


def q5_capacity(union_size):
    union_size = Integer(union_size)
    numerator = LINE_MULTIPLICITY * falling(RADIUS + union_size, 5)
    denominator = L * union_size * (W + 2) * (W + 3) * (W + 4)
    return numerator // denominator - (W + 5)


def pi_profile(d5, eta, layer_mismatch):
    answer = Integer(d5 - RADIUS + eta + layer_mismatch)
    for index in range(1, 5):
        answer *= W + index + eta + layer_mismatch
    return answer


def old_term(d5, eta=0):
    return falling(d5, 5) / pi_profile(d5, eta, 0)


def new_term(d5, union_size, eta=0):
    d6 = RADIUS + union_size - eta
    layer = d6 - d5
    require(layer >= 1, "positive support layer")
    return falling(d5, 6) / ((W + 1 + eta) * pi_profile(d5, eta, layer))


require(P == 2147483647, "M31 prime")
require(N == 2 * K, "half rate")
require(RADIUS + W == K, "R+w identity")

capacities = [q5_capacity(g) for g in srange(G_MIN, G_MAX + 1)]
require(all(capacities[index] <= capacities[index + 1]
            for index in range(len(capacities) - 1)),
        "full q5 capacity sweep monotone")
require(capacities[-1] == 32004, "q5 maximum")

base = L * G_MAX * (W + 2) * (W + 3) * (W + 4)
rhs = LINE_MULTIPLICITY * falling(RADIUS + G_MAX, 5)
q5_cap_slack = rhs - base * (W + 5 + 32004)
q5_next_slack = rhs - base * (W + 5 + 32005)
require(q5_cap_slack == 2961522295037039379410352000, "q5 cap slack")
require(q5_next_slack == -2040396785852186139127420050, "q5 next slack")

d_min = N - K + 5
d_max = d_min + 32004
require((d_min, d_max) == (1048581, 1080585), "d5 interval")
interpolation_margin = 4 * (W + 1) - (d_max - RADIUS)
require(interpolation_margin == 170336, "profile interpolation margin")

old_values = [old_term(d) for d in srange(d_min, d_max + 1)]
require(all(old_values[index] >= old_values[index + 1]
            for index in range(len(old_values) - 1)),
        "old resource exhaustive monotonicity")
new_d_values = [new_term(d, G_MIN) for d in srange(d_min, d_max + 1)]
require(all(new_d_values[index] <= new_d_values[index + 1]
            for index in range(len(new_d_values) - 1)),
        "new resource exhaustive d monotonicity")
new_g_values = [new_term(d_max, g) for g in srange(G_MIN, G_MAX + 1)]
require(all(new_g_values[index] >= new_g_values[index + 1]
            for index in range(len(new_g_values) - 1)),
        "new resource exhaustive g monotonicity")

old_max = old_values[0]
new_max = new_d_values[-1]
mixed = old_max + new_max
require(floor(old_max) == 908021, "old resource floor")
require(floor(new_max) == 95, "new resource floor")
require(floor(mixed) == 908116, "mixed floor")
require(L - floor(mixed) == 14867817, "rank-six contradiction gap")


# Literal GF(7) Reed--Solomon source control.
F = GF(7)
PR = PolynomialRing(F, "X")
X = PR.gen()
domain = list(F)
received = vector(F, [point^6 for point in domain])
listed = []
for coefficients in product(F, repeat=6):
    polynomial = sum(coefficients[index] * X^index for index in range(6))
    evaluation = vector(F, [polynomial(point) for point in domain])
    agreement = sum(1 for left, right in zip(received, evaluation) if left == right)
    if agreement >= 6:
        listed.append((tuple(coefficients), polynomial, evaluation))

require(len(listed) == 7, "GF7 whole list size")
anchor = vector(F, listed[0][0])
differences = [vector(F, row[0]) - anchor for row in listed[1:]]
require(matrix(F, differences).rank() == 6, "GF7 affine span rank")

# V=<X,...,X^5> has support D\{0}; every word outside it is nonzero at 0.
v_basis = [X^degree for degree in range(1, 6)]
v_support = {
    index
    for polynomial in v_basis
    for index, point in enumerate(domain)
    if polynomial(point) != 0
}
full_basis = [X^degree for degree in range(6)]
full_support = {
    index
    for polynomial in full_basis
    for index, point in enumerate(domain)
    if polynomial(point) != 0
}
require(len(v_support) == 6 and len(full_support) == 7, "GF7 d5/d6")
require(0 not in v_support and 0 in full_support, "GF7 support layer")
require(all(polynomial(0) == 0 for polynomial in v_basis), "GF7 V vanishes on layer")
require(PR(1)(0) != 0, "GF7 extender nonzero on layer")

toy_pi0 = Integer(5) * Integer(1) * 2 * 3 * 4
toy_pi1 = Integer(6) * Integer(2) * 3 * 4 * 5
toy_old = falling(6, 5) / toy_pi0
toy_new = falling(6, 6) / toy_pi1
require((toy_old, toy_new, toy_old + toy_new) == (6, 1, 7),
        "GF7 sharp compiler resources")

coefficient_set = {tuple(row[0]) for row in listed}
maximum_line_multiplicity = 0
for left_index in range(len(listed)):
    for right_index in range(left_index + 1, len(listed)):
        left = vector(F, listed[left_index][0])
        direction = vector(F, listed[right_index][0]) - left
        multiplicity = sum(
            1 for scalar in F if tuple(left + scalar * direction) in coefficient_set
        )
        maximum_line_multiplicity = max(maximum_line_multiplicity, multiplicity)
require(maximum_line_multiplicity == 2, "GF7 affine-line multiplicity")

toy_marked_left = Integer(6) * 6 * 2 * 3 * 4 * 5
toy_marked_right = Integer(2) * falling(7, 5)
require((toy_marked_left, toy_marked_right) == (4320, 5040),
        "GF7 generalized marked-line inequality")


def rational_record(value):
    return {
        "numerator": int(value.numerator()),
        "denominator": int(value.denominator()),
        "floor": int(floor(value)),
    }


summary = {
    "schema": "m31-rank6-generalized-weight-codim1-closure-sage-v1",
    "status": "EXACT_INDEPENDENT_SAGE_CONTROL",
    "theorem_id": "M31_RANK6_GENERALIZED_WEIGHT_CODIM_ONE_CLOSURE_V1",
    "deployed": {
        "union_values_exhausted": int(G_MAX - G_MIN + 1),
        "q5_ceiling": int(capacities[-1]),
        "q5_cap_slack": int(q5_cap_slack),
        "q5_successor_slack": int(q5_next_slack),
        "d5_range": [int(d_min), int(d_max)],
        "profile_interpolation_margin": int(interpolation_margin),
        "d5_values_exhausted": int(d_max - d_min + 1),
        "g_values_exhausted": int(G_MAX - G_MIN + 1),
        "old_support_maximum": rational_record(old_max),
        "new_layer_maximum": rational_record(new_max),
        "mixed_majorant": rational_record(mixed),
        "whole_chart_upper": int(floor(mixed)),
        "contradiction_gap": int(L - floor(mixed)),
    },
    "toy_GF7": {
        "scope": "EXACT_GF7_CONTROL_ONLY",
        "whole_list_size": len(listed),
        "affine_span_rank": int(matrix(F, differences).rank()),
        "d5": len(v_support),
        "d6": len(full_support),
        "support_layer": len(full_support - v_support),
        "support_saturated": True,
        "compiler_old_resource": int(toy_old),
        "compiler_new_resource": int(toy_new),
        "compiler_bound": int(toy_old + toy_new),
        "maximum_affine_line_multiplicity": int(maximum_line_multiplicity),
        "marked_line_left": int(toy_marked_left),
        "marked_line_right": int(toy_marked_right),
        "deployed_evidence": False,
    },
    "checks": int(checks),
}

print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
