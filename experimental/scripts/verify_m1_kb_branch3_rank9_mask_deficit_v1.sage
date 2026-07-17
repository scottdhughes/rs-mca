#!/usr/bin/env sage
"""Independent Sage control for the rank-nine mask-deficit packet.

The script independently recomputes the deployed exact one-cut thresholds and
checks a tiny GF(17) weighted-Vandermonde row-basis model.  The toy model is not
an actual syndrome-line family and does not establish deployed realizability.
"""

from itertools import combinations
from fractions import Fraction
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceil_div(numerator, denominator):
    numerator = ZZ(numerator)
    denominator = ZZ(denominator)
    require(numerator >= 0 and denominator > 0, "invalid ceiling division")
    return (numerator + denominator - 1) // denominator


# Deployed exact arithmetic, independently expressed with Sage Integer/binomial.
n = ZZ(2_097_152)
R = ZZ(1_048_576)
j = ZZ(981_104)
L = ZZ(349_526)
Delta0 = R - j
Delta_max = j - L
s = ZZ(9)
r = ZZ(8)
B = ZZ(274_980_725_508_892_088)
m = B + 1
C = binomial(n, s)


def mu(d, delta):
    ell = max(ZZ(1), ZZ(d) - j + ZZ(delta))
    return ceil_div(ell * binomial(Delta0 + r + delta, r), s)


def one_cut(d, cutoff):
    mu0 = mu(d, 0)
    mu_high = mu(d, cutoff + 1)
    gain = mu_high - mu0
    gap = C + 1 - m * mu0
    required_high = ceil_div(gap, gain)
    T = m - required_high
    return {
        "D": ZZ(cutoff),
        "mu0": mu0,
        "mu_high": mu_high,
        "gain": gain,
        "required_high": required_high,
        "T_star": T,
        "good_weight": T * mu0 + required_high * mu_high,
        "bad_weight": (T + 1) * mu0 + (required_high - 1) * mu_high,
    }


def first_useful_cutoff(d):
    lower = ZZ(0)
    upper = Delta_max - 1
    require(m * mu(d, upper + 1) > C, "no deployed useful cutoff")
    while lower < upper:
        middle = (lower + upper) // 2
        if m * mu(d, middle + 1) > C:
            upper = middle
        else:
            lower = middle + 1
    return lower


distance_cases = [ZZ(1)] + [j + b for b in range(1, 7)]
frontier = []
for d in distance_cases:
    cutoff = first_useful_cutoff(d)
    gate = one_cut(d, cutoff)
    require(gate["good_weight"] > C, "good one-cut weight does not exclude m")
    require(gate["bad_weight"] <= C, "one-cut sharp bad profile not feasible")
    if cutoff > 0:
        require(one_cut(d, cutoff - 1)["T_star"] < 0,
                "first useful cutoff is not minimal")
    frontier.append(
        {
            "d": d,
            "d_minus_j": d - j,
            "coarse_ell": max(ZZ(1), d - j),
            **gate,
        }
    )

require(
    [row["D"] for row in frontier] == [18_014, 5, 4, 3, 2, 1, 0],
    "deployed first-useful cutoff drift",
)
require(
    [row["T_star"] for row in frontier]
    == [
        17_907_572_507_584,
        16_733_545_009_172_851,
        20_034_624_384_082_026,
        24_986_249_357_852_538,
        33_238_965_528_645_962,
        49_744_409_690_947_096,
        99_260_765_817_180_096,
    ],
    "deployed T-star frontier drift",
)
require(one_cut(1, 18_013)["T_star"] == -12_386_728_892_028,
        "universal previous-cut boundary drift")
require(mu(1, 0) == 1_184_288_048_715_968_585_930_152_451_399_175,
        "universal mu0 drift")
require(mu(1, 18_015) == 7_863_582_775_712_820_188_422_356_536_857_430,
        "universal high multiplicity drift")

universal_anchors = []
for cutoff in [18_014, 20_000, 50_000, 100_000, Delta_max - 1]:
    gate = one_cut(1, cutoff)
    require(gate["T_star"] >= 0, "universal anchor has negative T-star")
    universal_anchors.append(gate)


# Tiny GF(17) MDS row-basis control.
F = GF(17)
N_toy = 8
R_toy = 6
kappa_toy = N_toy - R_toy
j_toy = 5
s_toy = 2
r_toy = 1
d_toy = 1
points = [F(i) for i in range(N_toy)]
H = matrix(F, R_toy, N_toy,
           lambda row, column: points[column] ** row)

require(H.rank() == R_toy, "toy parity-check rank drift")
require(
    all(H.matrix_from_columns(list(cols)).rank() == R_toy
        for cols in combinations(range(N_toy), R_toy)),
    "toy parity check is not MDS",
)

K = H.right_kernel()
require(K.dimension() == kappa_toy == 2, "toy kernel dimension drift")
minimum_weight = min(
    sum(1 for entry in word if entry != 0)
    for word in K
    if word != 0
)
require(minimum_weight == R_toy + 1 == 7, "toy kernel distance drift")

G = matrix(F, [K.basis()[0]])
v = vector(F, [1] + [0] * (N_toy - 1))
y1 = H * v
D_space = matrix(F, list(G.rows()) + [v])
require(y1 != 0, "toy source direction vanished")
require(G.rank() == r_toy, "toy K0 rank drift")
require(D_space.rank() == s_toy, "toy affine-direction rank drift")


def toy_mu(delta):
    a = N_toy - j_toy + delta
    ell = max(1, d_toy + a - N_toy)
    return ceil_div(
        ell * binomial(a - kappa_toy + r_toy, r_toy),
        s_toy,
    )


toy_mus = [toy_mu(0), toy_mu(1)]
require(toy_mus == [1, 2], "toy multiplicity formula drift")

minimum_basis_counts = []
for delta in [0, 1]:
    mask_size = N_toy - j_toy + delta
    basis_counts = []
    for mask in combinations(range(N_toy), mask_size):
        columns = list(mask)
        if D_space.matrix_from_columns(columns).rank() != s_toy:
            continue
        basis_count = sum(
            1
            for basis in combinations(columns, s_toy)
            if D_space.matrix_from_columns(list(basis)).rank() == s_toy
        )
        basis_counts.append(basis_count)
    require(basis_counts, "no toy injective masks")
    minimum_basis_counts.append(min(basis_counts))

require(minimum_basis_counts == [1, 2], "toy row-basis minima drift")

toy_budget = binomial(N_toy, s_toy)
toy_m = 15
toy_good_low = 1
toy_good_weight = toy_good_low * toy_mus[0] + (toy_m - toy_good_low) * toy_mus[1]
toy_bad_low = 2
toy_bad_weight = toy_bad_low * toy_mus[0] + (toy_m - toy_bad_low) * toy_mus[1]
require(toy_budget == 28, "toy ambient budget drift")
require(toy_good_weight == 29 > toy_budget, "toy good boundary drift")
require(toy_bad_weight == 28 == toy_budget, "toy sharp bad boundary drift")

toy_set_pair_all_zero = Fraction(
    int(toy_m), int(binomial(j_toy + s_toy, s_toy))
)
toy_set_pair_bad = (
    Fraction(int(toy_bad_low), int(binomial(j_toy + s_toy, s_toy)))
    + Fraction(
        int(toy_m - toy_bad_low),
        int(binomial(j_toy + s_toy - 1, s_toy)),
    )
)
require(
    toy_set_pair_all_zero.numerator <= toy_set_pair_all_zero.denominator,
    "toy all-zero set-pair gate failed",
)
require(
    toy_set_pair_bad.numerator <= toy_set_pair_bad.denominator,
    "toy sharp bad set-pair gate failed",
)
require(2 <= 2 * j_toy - d_toy, "toy pairwise deficit gate failed")

output = {
    "schema": "rs-mca-m1-kb-branch3-rank9-mask-deficit-v1-sage-control",
    "status": "PASS",
    "deployed_exact_arithmetic": {
        "Delta0": Delta0,
        "Delta_max": Delta_max,
        "universal_previous_T_star": one_cut(1, 18_013)["T_star"],
        "distance_frontier": frontier,
        "universal_anchor_curve": universal_anchors,
    },
    "GF17_mds_control": {
        "N": N_toy,
        "R": R_toy,
        "kappa": kappa_toy,
        "kernel_minimum_distance": minimum_weight,
        "s": s_toy,
        "r": r_toy,
        "j": j_toy,
        "d": d_toy,
        "deficit_multiplicities": toy_mus,
        "injective_mask_minimum_D_basis_counts": minimum_basis_counts,
        "ambient_budget": toy_budget,
        "test_size": toy_m,
        "good_low_cap": toy_good_low,
        "good_weight": toy_good_weight,
        "sharp_bad_low_count": toy_bad_low,
        "sharp_bad_weight": toy_bad_weight,
        "set_pair_all_zero": str(toy_set_pair_all_zero),
        "set_pair_sharp_bad": str(toy_set_pair_bad),
        "pairwise_gate": True,
    },
    "nonclaims": [
        "not a deployed-field census",
        "not an actual syndrome-line family",
        "not a proof of a deployed cumulative deficit-tail lemma",
        "not a replacement for the imported theorem",
    ],
}

print(json.dumps(output, sort_keys=True, default=int))
