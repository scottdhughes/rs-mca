#!/usr/bin/env sage
"""Independent Sage replay for the rank-nine syndrome-rank route cut.

The script has three deliberately separate layers.

1.  It recomputes the deployed KoalaBear cap using exact Sage integers and
    rationals.  This layer only checks arithmetic; it does not establish the
    adapter hypotheses (in particular, syndrome-line nondegeneracy or witness
    rank) for a deployed selector.
2.  It exhaustively checks the deterministic rank-reduction mechanism on a
    small RS[5,2,4] code over GF(7).
3.  On the same code it gives a counterexample to the false implication
    "the whole syndrome line has low-weight lifts => one common support".

The toy is finite-field evidence and a guardrail, not a deployed-field census
or a replacement for the local symbolic proof.
"""

from itertools import combinations, product
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def hamming_weight(word):
    return sum(1 for entry in word if entry != 0)


def syndrome_cap(E, E_plus, distance, witness_rank):
    """Floor(B_{E,E+} * gamma^{-(t-2)}) with exact arithmetic."""

    E = ZZ(E)
    E_plus = ZZ(E_plus)
    distance = ZZ(distance)
    witness_rank = ZZ(witness_rank)
    require(0 < E <= E_plus < distance, "invalid syndrome-cap radii")
    require(witness_rank >= 2, "witness rank below two")
    ball_factor = (E_plus + 1) // (E_plus - E + 1)
    gamma = QQ(distance - E) / distance
    cap = floor(QQ(ball_factor) / gamma ** (witness_rank - 2))
    return ZZ(ball_factor), gamma, ZZ(cap)


# -------------------------------------------------------------------------
# Exact deployed arithmetic.
# -------------------------------------------------------------------------

n = ZZ(2_097_152)
R = ZZ(1_048_576)
j = ZZ(981_104)
distance = R + 1
distance_gap = distance - j
B_remaining = ZZ(274_980_725_508_892_088)

require(distance_gap == 67_473, "deployed distance gap drift")

difference_rank = ZZ(9)
# The selected affine differences have rank s.  Adding any witness whose
# syndrome is not in the direction span gives witness-column rank t=s+1.
witness_rank = difference_rank + 1
exponent = witness_rank - 2
ball_factor, gamma, cap = syndrome_cap(j, j, distance, witness_rank)

numerator = ball_factor * distance ** exponent
denominator = distance_gap ** exponent
require(cap * denominator <= numerator,
        "syndrome cap is below its exact floor")
require((cap + 1) * denominator > numerator,
        "syndrome cap is above its exact floor")
require(cap == 3_337_935_545_766_696,
        "deployed rank-nine syndrome cap drift")
require(cap <= B_remaining,
        "deployed rank-nine cap does not fit the remaining budget")
require(B_remaining - cap == 271_642_789_963_125_392,
        "rank-nine remaining margin drift")

rank_rows = [
    {
        "difference_rank": difference_rank,
        "witness_rank": witness_rank,
        "exponent": exponent,
        "ball_factor": ball_factor,
        "gamma": str(gamma),
        "cap": cap,
        "fits_remaining_budget": True,
        "remaining_margin": B_remaining - cap,
    }
]


# -------------------------------------------------------------------------
# Exhaustive GF(7) RS[5,2,4] control.
# -------------------------------------------------------------------------

F = GF(7)
points = [F(i) for i in range(5)]
N_toy = ZZ(len(points))
H = matrix(
    F,
    3,
    N_toy,
    lambda row, column: points[column] ** row,
)

require(H.rank() == 3, "toy parity-check rank drift")
require(
    all(
        H.matrix_from_columns(list(columns)).rank() == 3
        for columns in combinations(range(N_toy), 3)
    ),
    "toy Vandermonde parity check is not MDS",
)

toy_code = H.right_kernel()
require(toy_code.dimension() == 2, "toy code dimension drift")
toy_nonzero_weights = [
    hamming_weight(word) for word in toy_code if word != 0
]
toy_distance = min(toy_nonzero_weights)
require(toy_distance == 4, "toy RS[5,2,4] distance drift")

E_toy = ZZ(2)
gamma_toy = QQ(toy_distance - E_toy) / toy_distance
require(gamma_toy == QQ(1) / 2, "toy gamma drift")

s0 = vector(F, [0, 1, 0])
s1 = vector(F, [0, 0, 1])
require(matrix(F, [s0, s1]).rank() == 2,
        "toy syndrome line is degenerate")


def enumerate_low_weight_lifts(target, radius):
    """Exhaust all vectors of weight at most radius with given syndrome."""

    lifts = []
    nonzero = list(F)[1:]
    for weight in range(radius + 1):
        for support in combinations(range(N_toy), weight):
            for coefficients in product(nonzero, repeat=weight):
                word = vector(F, N_toy)
                for coordinate, coefficient in zip(support, coefficients):
                    word[coordinate] = coefficient
                if H * word == target:
                    lifts.append(word)
    return lifts


def support_tuple(word):
    return tuple(i for i, entry in enumerate(word) if entry != 0)


slopes = list(F)
lifts_by_slope = {}
for alpha in slopes:
    target = s0 + alpha * s1
    lifts = enumerate_low_weight_lifts(target, E_toy)
    require(lifts, "toy syndrome point lacks a low-weight lift")
    require(all(hamming_weight(word) <= E_toy for word in lifts),
            "toy lift exceeds the radius")
    require(all(H * word == target for word in lifts),
            "toy lift has the wrong syndrome")
    lifts_by_slope[alpha] = sorted(
        lifts,
        key=lambda word: (support_tuple(word), tuple(ZZ(x) for x in word)),
    )

require(
    [len(lifts_by_slope[F(i)]) for i in range(7)]
    == [1, 1, 1, 2, 2, 2, 1],
    "toy low-weight lift census drift",
)

# Every alpha has a distinct-pair realization: for i != k and i+k=alpha,
# coefficients c and -c with c(i-k)=1 give syndrome (0,1,alpha).
pair_supports = {
    int(alpha): [support_tuple(word) for word in lifts_by_slope[alpha]]
    for alpha in slopes
}
require(
    pair_supports
    == {
        0: [(3, 4)],
        1: [(0, 1)],
        2: [(0, 2)],
        3: [(0, 3), (1, 2)],
        4: [(0, 4), (1, 3)],
        5: [(1, 4), (2, 3)],
        6: [(2, 4)],
    },
    "toy pair-support atlas drift",
)


# No support of size at most E_toy can simultaneously lift s0 and s1.  This
# is the exact common-support condition, tested by column-span containment.
syndrome_basis = matrix(
    F,
    3,
    2,
    lambda row, column: [s0, s1][column][row],
)
common_supports = []
for support_size in range(E_toy + 1):
    for support in combinations(range(N_toy), support_size):
        restricted = H.matrix_from_columns(list(support))
        if restricted.augment(syndrome_basis).rank() == restricted.rank():
            common_supports.append(support)

require(not common_supports,
        "a common support of size at most two unexpectedly exists")


# Choose the lexicographically first support lift at each slope.  The resulting
# witness matrix has rank four, so the local rank-reduction lemma takes two steps.
canonical_lifts = [lifts_by_slope[F(i)][0] for i in range(7)]
X = matrix(F, N_toy, 7,
           lambda row, column: canonical_lifts[column][row])
Y = matrix(F, 3, 7,
           lambda row, column: (s0 + F(column) * s1)[row])

require(H * X == Y, "toy witness syndrome matrix drift")
require(Y.rank() == 2, "toy syndrome matrix rank drift")
require(all(hamming_weight(X.column(i)) <= E_toy for i in range(7)),
        "toy witness column exceeds radius")
require(X.rank() == 4, "toy witness rank drift")


def largest_rank_reduced_subsets(column_indices, rank_bound):
    """Return every largest subset whose witness rank is at most rank_bound."""

    column_indices = tuple(column_indices)
    for size in range(len(column_indices), 0, -1):
        qualifying = []
        for subset in combinations(column_indices, size):
            if X.matrix_from_columns(list(subset)).rank() <= rank_bound:
                qualifying.append(subset)
        if qualifying:
            return qualifying
    raise RuntimeError("no nonempty rank-reduced subset")


first_reductions = largest_rank_reduced_subsets(range(7), 3)
J1 = first_reductions[0]
first_required = ceil(ZZ(7) * gamma_toy)
require(len(J1) == 5 >= first_required,
        "toy first rank-reduction size drift")
require(X.matrix_from_columns(list(J1)).rank() == 3,
        "toy first reduction rank drift")

second_reductions = largest_rank_reduced_subsets(J1, 2)
J2 = second_reductions[0]
second_required = ceil(ZZ(len(J1)) * gamma_toy)
iterated_required = ceil(ZZ(7) * gamma_toy ** 2)
require(len(J2) == 3 >= second_required,
        "toy second rank-reduction size drift")
require(len(J2) >= iterated_required,
        "toy iterated rank-reduction size drift")
require(X.matrix_from_columns(list(J2)).rank() == 2,
        "toy final witness rank drift")
require(J1 == (0, 1, 3, 4, 5), "toy first subset drift")
require(J2 == (0, 3, 4), "toy second subset drift")


# The final three columns lie on one affine lift line.  It contains exactly
# E+1 low-weight points, saturating the deterministic line-ball bound, even
# though the syndrome line has (separately chosen) low-weight lifts at all
# seven slopes.
lift_a = X.column(J2[0])
lift_b = (X.column(J2[1]) - lift_a) / F(J2[1] - J2[0])
require(lift_b != 0, "toy affine lift direction vanished")
require(H * lift_a == s0, "toy affine lift intercept syndrome drift")
require(H * lift_b == s1, "toy affine lift direction syndrome drift")
require(
    all(X.column(index) == lift_a + F(index) * lift_b for index in J2),
    "toy final witnesses are not affine in their slopes",
)

low_weight_affine_slopes = [
    ZZ(alpha)
    for alpha in slopes
    if hamming_weight(lift_a + alpha * lift_b) <= E_toy
]
toy_ball_factor, toy_gamma_check, toy_threshold_cap = syndrome_cap(
    E_toy, E_toy, toy_distance, X.rank()
)
require(toy_gamma_check == gamma_toy, "toy threshold gamma drift")
require(toy_ball_factor == 3, "toy line-ball factor drift")
require(low_weight_affine_slopes == [0, 3, 4],
        "toy affine lift low-weight slopes drift")
require(len(low_weight_affine_slopes) == toy_ball_factor,
        "toy affine lift does not saturate the line-ball bound")
require(
    ZZ(7) * gamma_toy ** (X.rank() - 2) <= toy_ball_factor,
    "toy deterministic rank-threshold inequality drift",
)
require(toy_threshold_cap == 12,
        "toy rank-threshold slope cap drift")


output = {
    "schema": (
        "rs-mca-m1-kb-branch3-rank9-syndrome-rank-reduction-v1-"
        "sage-control"
    ),
    "status": "PASS",
    "deployed_exact_arithmetic": {
        "n": n,
        "R": R,
        "E": j,
        "E_plus": j,
        "distance": distance,
        "distance_gap": distance_gap,
        "remaining_budget": B_remaining,
        "rank_rows": rank_rows,
    },
    "GF7_RS_5_2_4_control": {
        "field": "GF(7)",
        "length": N_toy,
        "dimension": toy_code.dimension(),
        "minimum_distance": toy_distance,
        "E": E_toy,
        "gamma": str(gamma_toy),
        "syndrome_line_size": len(slopes),
        "lift_counts_by_slope": [
            len(lifts_by_slope[F(i)]) for i in range(7)
        ],
        "pair_supports_by_slope": pair_supports,
        "common_supports_of_size_at_most_E": common_supports,
        "canonical_witness_rank": X.rank(),
        "first_rank_reduction": {
            "required_size": first_required,
            "chosen_slopes": list(J1),
            "size": len(J1),
            "rank": X.matrix_from_columns(list(J1)).rank(),
        },
        "second_rank_reduction": {
            "required_size": second_required,
            "iterated_required_size": iterated_required,
            "chosen_slopes": list(J2),
            "size": len(J2),
            "rank": X.matrix_from_columns(list(J2)).rank(),
        },
        "affine_lift_low_weight_slopes": low_weight_affine_slopes,
        "line_ball_factor": toy_ball_factor,
        "rank_threshold_slope_cap": toy_threshold_cap,
        "full_syndrome_line_has_low_weight_lifts": True,
        "full_syndrome_line_has_common_support": False,
    },
    "nonclaims": [
        "not a deployed-field census",
        "not a proof of deployed syndrome-line nondegeneracy",
        "not a proof that deployed affine rank nine gives witness rank ten",
        "not a replacement for the local symbolic proof",
        "not payment of the correlated-agreement or sparse-sigma branch",
    ],
}

print(json.dumps(output, sort_keys=True, default=int))
