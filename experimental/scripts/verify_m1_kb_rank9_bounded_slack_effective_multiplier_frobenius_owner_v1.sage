"""Exact controls for the bounded-slack effective-multiplier owner.

The finite-field fixture remains a degree-two specialization of the general
source-Frobenius argument.  Exact integer checks bind the deployed degree-195
owner, the algebraic endpoint 9208, and the inherited-ledger cut at 196.  This
is not a deployed selector, a rank-nine census, or the symbolic proof.
"""

import json


SCHEMA = "rs-mca-m1-kb-rank9-bounded-slack-effective-multiplier-frobenius-owner-v1-sage"
SCALE = "EXACT_TOY_CONTROL_NOT_DEPLOYED_SELECTOR_CENSUS_PROOF_OR_LEDGER"

DEPLOYED_P = 2_130_706_433
DEPLOYED_M = 195
DEPLOYED_ANCHOR_SIZE = 392
DEPLOYED_CROSS_DEGREE = 390
DEPLOYED_SUPPORT_FLOOR = 18_418
DEPLOYED_E_FLOOR = 33_737
DEPLOYED_EXPONENT_COUNT = 38_809
DEPLOYED_OWNER_CAP = 417_618_461_064
DEPLOYED_LEDGER_INCREMENT = 413_357_048_196
DEPLOYED_PROFILE_COUNT = 1_274_195
DEPLOYED_DEFICIT_SHAPE_COUNT = 63_391_250
ALGEBRAIC_MAX_M = 9_208
FIRST_ALGEBRAIC_FAILURE_M = 9_209
M196_OWNER_CAP = 419_749_167_498
M196_E_MAX = -9_487_087_327_483_531_737_221_376_676_045_581_877_928_676


class ContractError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


require((DEPLOYED_M + 1)*(DEPLOYED_P + 1) == DEPLOYED_OWNER_CAP,
        "deployed owner cap drift")
require(DEPLOYED_OWNER_CAP - 2*(DEPLOYED_P + 1) == DEPLOYED_LEDGER_INCREMENT,
        "deployed ledger increment drift")
require(2*(DEPLOYED_M + 1) == DEPLOYED_ANCHOR_SIZE,
        "deployed anchor size drift")
require(2*DEPLOYED_M == DEPLOYED_CROSS_DEGREE,
        "deployed cross degree drift")
require(DEPLOYED_SUPPORT_FLOOR > DEPLOYED_CROSS_DEGREE,
        "deployed support guard failed")
require(DEPLOYED_E_FLOOR > DEPLOYED_CROSS_DEGREE,
        "deployed reduced-degree guard failed")
require((DEPLOYED_M + 2)^2 == DEPLOYED_EXPONENT_COUNT,
        "deployed exponent count drift")
require(binomial(198, 3) - 1 == DEPLOYED_PROFILE_COUNT,
        "deployed profile count drift")
require(binomial(199, 4) - 1 == DEPLOYED_DEFICIT_SHAPE_COUNT,
        "deployed deficit-shape count drift")
require((DEPLOYED_SUPPORT_FLOOR - 1)//2 == ALGEBRAIC_MAX_M,
        "algebraic endpoint drift")
require(2*ALGEBRAIC_MAX_M < DEPLOYED_SUPPORT_FLOOR,
        "algebraic maximum strictness drift")
require(2*FIRST_ALGEBRAIC_FAILURE_M == DEPLOYED_SUPPORT_FLOOR,
        "algebraic failure equality drift")
require(197*(DEPLOYED_P + 1) == M196_OWNER_CAP,
        "m196 owner cap drift")
require(M196_E_MAX < 0, "m196 aggregate-excess sign drift")


B = GF(13)
F.<zeta> = GF(13^2)
R.<X> = PolynomialRing(F)
S.<Z> = PolynomialRing(F)

source = [F(i) for i in [1, 2, 3, 4, 5, 6]]
moving = [F(i) for i in [7, 8, 9, 10, 11, 12]]

P = (
    (9*zeta + 12)*X^3
    + (6*zeta + 6)*X^2
    + (10*zeta + 7)*X
    + 4*zeta + 10
)
Q = (
    9*zeta*X^3
    + (5*zeta + 10)*X^2
    + (11*zeta + 11)*X
    + zeta + 8
)


def coefficient_frobenius(poly):
    return R([c^13 for c in poly.list()])


def six_anchor_minor(poly_p, poly_q):
    rows = []
    for a in source:
        value = F(poly_p(a)) + Z*F(poly_q(a))
        value_p = value^13
        rows.append(
            [
                value_p,
                a*value_p,
                a^2*value_p,
                value,
                a*value,
                a^2*value,
            ]
        )
    return matrix(S, rows).det()


def support_size(values):
    return sum(1 for value in values if value != 0)


def source_values(poly_p, poly_q, slope):
    return vector(F, [poly_p(a) + slope*poly_q(a) for a in source])


def krylov_rank(values):
    return matrix(
        F,
        [
            [source[i]^power * values[i] for power in range(3)]
            for i in range(len(source))
        ],
    ).rank()


def apply_polynomial(poly, values):
    return vector(
        F,
        [poly(source[i])*values[i] for i in range(len(source))],
    )


require(str(F.modulus()) == "x^2 + 12*x + 2", "GF(13^2) modulus drift")
require(P.degree() == Q.degree() == 3, "fixture degree drift")
require(gcd(P, Q) == 1, "fixture pencil not primitive")

selected = []
for root in moving:
    require(Q(root) != 0, "moving root is a Q pole")
    eta = -P(root)/Q(root)
    member = P + eta*Q
    quotient, remainder = member.quo_rem(X-root)
    require(remainder == 0, "moving-root division failed")
    require(quotient.degree() == 2, "effective multiplier is not quadratic")
    require(
        all(quotient(a) != 0 for a in B),
        "quadratic effective multiplier has a base root",
    )
    selected.append(
        {
            "moving_root": root,
            "eta": eta,
            "quotient": quotient,
            "source_support": support_size(
                [member(a) for a in source]
            ),
        }
    )

etas = [record["eta"] for record in selected]
require(len(set(etas)) == len(etas) == 6, "selected slopes not distinct")
require(all(eta^13 != eta for eta in etas), "selected slope lies in base field")

minor = six_anchor_minor(P, Q)
require(minor != 0, "six-anchor determinant vanished")
require(minor.degree() == 42 == 3*13 + 3, "six-anchor degree drift")
require(all(minor(eta) == 0 for eta in etas), "selected slope misses determinant")
minor_roots = minor.roots(multiplicities=False)
require(len(minor_roots) == 14, "six-anchor root count drift")

all_source_supports = [
    support_size(source_values(P, Q, eta))
    for eta in F
]
require(min(all_source_supports) == 5, "universal source support drift")
require(all(record["source_support"] == 6 for record in selected), "selected support drift")

all_u_ranks = [krylov_rank(source_values(P, Q, eta)) for eta in F]
all_v_ranks = [
    krylov_rank(
        vector(F, [value^13 for value in source_values(P, Q, eta)])
    )
    for eta in F
]
require(set(all_u_ranks) == {3}, "ordinary Krylov rank drift")
require(set(all_v_ranks) == {3}, "Frobenius Krylov rank drift")

fingerprint_checks = {}
degree_fixtures = [
    R(zeta + 1),
    X + zeta,
    X^2 + (zeta + 1)*X + zeta + 2,
]
for degree, multiplier in enumerate(degree_fixtures):
    conjugate = coefficient_frobenius(R(multiplier))
    ok = True
    for a in source:
        base_scalar = a
        value = base_scalar*multiplier(a)
        if multiplier(a)*value^13 - conjugate(a)*value != 0:
            ok = False
    fingerprint_checks[degree] = ok
    require(ok, "fingerprint fixture failed")

low_p = X^2 + 1
low_q = X + 1
require(gcd(low_p, low_q) == 1, "low-degree fixture not primitive")
low_minor = six_anchor_minor(low_p, low_q)
require(low_minor == 0, "low-degree all-minor countercontrol drift")

exponents = [i*13 + j for i in range(4) for j in range(4)]
require(len(exponents) == len(set(exponents)) == 16, "exponent separation drift")

q_vector = vector(F, [zeta + a for a in source])
g1 = X + zeta
g2 = X^2 + zeta*X + 1
w1 = apply_polynomial(g1, q_vector)
w2 = apply_polynomial(g2, q_vector)
common_1 = apply_polynomial(g2, w1)
common_2 = apply_polynomial(g1, w2)
common_direct = apply_polynomial(g1*g2, q_vector)
require(common_1 == common_2 == common_direct, "operator commutativity drift")
require(common_direct != 0, "common cross vector vanished")

support_four = vector(F, [1, 1, 1, 1, 0, 0])
four_annihilator = prod(X-a for a in source[:4])
require(
    apply_polynomial(four_annihilator, support_four) == 0,
    "support-four annihilator countercontrol drift",
)

root_count_boundary = prod(X-a for a in source)
require(root_count_boundary != 0, "root-count countercontrol vanished")
require(root_count_boundary.degree() == 6 == 2 + 4, "root-count boundary drift")
require(
    all(root_count_boundary(a) == 0 for a in source),
    "root-count equality countercontrol drift",
)

K5 = GF(5)
block_A = matrix(K5, [[0,3,3], [2,0,4], [2,1,0]])
block_B = matrix(K5, [[0,3,4], [2,0,1], [1,4,0]])
block_C = matrix(K5, [[0,4,1], [1,0,1], [4,4,0]])
block_D = matrix(K5, [[0,2,1], [3,0,2], [4,3,0]])
block_total = block_matrix([[block_A, block_B], [block_C, block_D]])
require(
    all(block.is_skew_symmetric() for block in [block_A, block_B, block_C, block_D]),
    "skew-block guardrail drift",
)
require(block_total.det() == K5(2), "skew-block total determinant drift")
require(
    all(
        (block_C + zz*block_D - yy*block_A - yy*zz*block_B).det() == 0
        for yy in K5
        for zz in K5
    ),
    "skew-block plane-incidence guardrail drift",
)

interface_checks = {
    "base_field_order": B.order() == 13,
    "extension_field_order": F.order() == 169,
    "extension_degree_two": F.degree() == 2,
    "pinned_modulus": str(F.modulus()) == "x^2 + 12*x + 2",
    "source_points_nonzero": all(a != 0 for a in source),
    "source_points_distinct": len(set(source)) == 6,
    "moving_points_distinct": len(set(moving)) == 6,
    "source_moving_disjoint": set(source).isdisjoint(set(moving)),
    "primitive_pencil": gcd(P, Q) == 1,
    "degree_three_pencil": P.degree() == Q.degree() == 3,
    "selected_fiber_count": len(selected) == 6,
    "selected_slopes_distinct": len(set(etas)) == 6,
    "selected_slopes_outside_base": all(eta^13 != eta for eta in etas),
    "selected_members_have_moving_root": all(
        (P + record["eta"]*Q)(record["moving_root"]) == 0
        for record in selected
    ),
    "selected_quotients_degree_two": all(
        record["quotient"].degree() == 2 for record in selected
    ),
    "selected_quotients_no_base_roots": all(
        all(record["quotient"](a) != 0 for a in B)
        for record in selected
    ),
    "selected_source_support_full": all(
        record["source_support"] == 6 for record in selected
    ),
    "universal_source_support_floor": min(all_source_supports) == 5,
    "all_U_Krylov_rank_three": set(all_u_ranks) == {3},
    "all_V_Krylov_rank_three": set(all_v_ranks) == {3},
    "six_anchor_minor_nonzero": minor != 0,
    "six_anchor_minor_degree": minor.degree() == 42,
    "selected_slopes_minor_roots": all(minor(eta) == 0 for eta in etas),
    "minor_root_count": len(minor_roots) == 14,
    "fingerprint_degree_zero": fingerprint_checks[0],
    "fingerprint_degree_one": fingerprint_checks[1],
    "fingerprint_degree_two": fingerprint_checks[2],
    "coefficient_frobenius": coefficient_frobenius(X+zeta) == X+zeta^13,
    "low_degree_all_minors_zero": low_minor == 0,
    "exponent_separation": len(set(exponents)) == 16,
    "operator_commutativity": common_1 == common_2 == common_direct,
    "common_cross_vector_nonzero": common_direct != 0,
    "support_four_annihilator_countercontrol": apply_polynomial(
        four_annihilator, support_four
    ) == 0,
    "root_count_strictness_countercontrol": (
        root_count_boundary.degree() == len(source)
        and all(root_count_boundary(a) == 0 for a in source)
    ),
    "skew_blocks_and_invertible_total": (
        block_total.det() == K5(2)
        and all(
            block.is_skew_symmetric()
            for block in [block_A, block_B, block_C, block_D]
        )
    ),
    "skew_incidence_countercontrol": all(
        (block_C + zz*block_D - yy*block_A - yy*zz*block_B).det() == 0
        for yy in K5
        for zz in K5
    ),
    "deployed_m_is_195": DEPLOYED_M == 195,
    "deployed_anchor_size_is_392": DEPLOYED_ANCHOR_SIZE == 392,
    "deployed_cross_degree_is_390": DEPLOYED_CROSS_DEGREE == 390,
    "deployed_support_guard_strict": DEPLOYED_SUPPORT_FLOOR > DEPLOYED_CROSS_DEGREE,
    "deployed_reduced_degree_guard_strict": DEPLOYED_E_FLOOR > DEPLOYED_CROSS_DEGREE,
    "deployed_exponent_count": DEPLOYED_EXPONENT_COUNT == (DEPLOYED_M + 2)^2,
    "deployed_owner_cap": DEPLOYED_OWNER_CAP == (DEPLOYED_M + 1)*(DEPLOYED_P + 1),
    "deployed_ledger_increment": DEPLOYED_LEDGER_INCREMENT == 194*(DEPLOYED_P + 1),
    "deployed_profile_count": DEPLOYED_PROFILE_COUNT == binomial(198, 3) - 1,
    "deployed_deficit_shape_count": DEPLOYED_DEFICIT_SHAPE_COUNT == binomial(199, 4) - 1,
    "algebraic_maximum_strict": 2*ALGEBRAIC_MAX_M < DEPLOYED_SUPPORT_FLOOR,
    "algebraic_next_fails_strictness": 2*FIRST_ALGEBRAIC_FAILURE_M == DEPLOYED_SUPPORT_FLOOR,
    "m196_owner_cap": M196_OWNER_CAP == 197*(DEPLOYED_P + 1),
    "m196_aggregate_excess_negative": M196_E_MAX < 0,
}

EXPECTED_INTERFACE_KEYS = set(interface_checks)
require(len(EXPECTED_INTERFACE_KEYS) == 50, "interface inventory drift")
require(all(interface_checks.values()), "an exact interface check failed")


def validate_interfaces(candidate):
    require(set(candidate) == EXPECTED_INTERFACE_KEYS, "interface-key drift")
    require(all(candidate.values()), "mutated interface accepted")


mutation_rejections = 0
for key in sorted(EXPECTED_INTERFACE_KEYS):
    candidate = dict(interface_checks)
    candidate[key] = False
    try:
        validate_interfaces(candidate)
    except ContractError:
        mutation_rejections += 1
    else:
        raise ContractError("interface mutation survived: " + key)
require(mutation_rejections == 50, "mutation rejection count drift")

control = {
    "schema": SCHEMA,
    "scale": SCALE,
    "toy_only": True,
    "base_field_order": int(B.order()),
    "extension_field_order": int(F.order()),
    "field_modulus": str(F.modulus()),
    "source_points": [int(a) for a in source],
    "moving_points": [int(a) for a in moving],
    "pencil_P": str(P),
    "pencil_Q": str(Q),
    "selected_fiber_count": len(selected),
    "selected_slopes": [str(eta) for eta in etas],
    "effective_multiplier_degree": 2,
    "selected_source_support": [
        record["source_support"] for record in selected
    ],
    "universal_source_support_minimum": min(all_source_supports),
    "six_anchor_minor_degree": int(minor.degree()),
    "six_anchor_minor_root_count": len(minor_roots),
    "selected_slopes_are_minor_roots": True,
    "ordinary_Krylov_space_count": len(all_u_ranks),
    "frobenius_Krylov_space_count": len(all_v_ranks),
    "ordinary_Krylov_rank_set": [int(value) for value in sorted(set(all_u_ranks))],
    "frobenius_Krylov_rank_set": [int(value) for value in sorted(set(all_v_ranks))],
    "fingerprint_degrees_checked": [0, 1, 2],
    "low_degree_all_minors_zero": True,
    "support_four_countercontrol": True,
    "root_count_strictness_countercontrol": True,
    "skew_block_total_determinant": int(block_total.det()),
    "skew_block_incidence_pairs_checked": 25,
    "skew_block_all_incidence_determinants_zero": True,
    "mutation_count": len(interface_checks),
    "mutation_rejections": mutation_rejections,
    "deployed_m": DEPLOYED_M,
    "deployed_anchor_size": DEPLOYED_ANCHOR_SIZE,
    "deployed_cross_degree": DEPLOYED_CROSS_DEGREE,
    "deployed_support_floor": DEPLOYED_SUPPORT_FLOOR,
    "deployed_reduced_degree_floor": DEPLOYED_E_FLOOR,
    "deployed_owner_cap": DEPLOYED_OWNER_CAP,
    "deployed_ledger_increment": DEPLOYED_LEDGER_INCREMENT,
    "deployed_profile_count": DEPLOYED_PROFILE_COUNT,
    "deployed_deficit_shape_count": DEPLOYED_DEFICIT_SHAPE_COUNT,
    "algebraic_max_m": ALGEBRAIC_MAX_M,
    "first_algebraic_failure_m": FIRST_ALGEBRAIC_FAILURE_M,
    "m196_owner_cap": M196_OWNER_CAP,
    "m196_aggregate_excess_max": M196_E_MAX,
    "complete_selector_constructed": False,
    "deployed_rank9_record_constructed": False,
}

print(
    "BOUNDED_SLACK_EFFECTIVE_MULTIPLIER_CONTROL="
    + json.dumps(control, sort_keys=True, separators=(",", ":"), default=int)
)
print(
    "BOUNDED_SLACK_EFFECTIVE_MULTIPLIER_MUTATIONS="
    + json.dumps(interface_checks, sort_keys=True, separators=(",", ":"), default=int)
)
print("SCALE=" + SCALE)
