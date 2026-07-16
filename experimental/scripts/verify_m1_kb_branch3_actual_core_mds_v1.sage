#!/usr/bin/env sage
"""Independent Sage control for the branch-3 actual-core MDS splice.

This replay checks the deployed big-integer rank ladder and a tiny GF(17)
weighted-Vandermonde row-basis model.  It is not a deployed-field census and
does not prove that any deployed selector has a particular intrinsic rank.
"""

from itertools import combinations
import json
import math


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ceil_div(numerator, denominator):
    require(numerator >= 0 and denominator > 0, "invalid ceiling division")
    return (numerator + denominator - 1) // denominator


# Exact deployed arithmetic.
n = 2_097_152
R_deployed = 1_048_576
j = 981_104
Delta0 = R_deployed - j
U_paid = 2_602_502_999
B_remaining = 274_980_725_508_892_088
B_star = U_paid + B_remaining

rank_rows = []
for s in range(4, 10):
    r = s - 1
    multiplicity_binomial = math.comb(Delta0 + r, r)
    mu = ceil_div(multiplicity_binomial, s)
    cap = math.comb(n, s) // mu
    rank_rows.append(
        {
            "s": s,
            "r": r,
            "mu": mu,
            "cap": cap,
            "fits": cap <= B_remaining,
        }
    )

require([row["fits"] for row in rank_rows] == [True] * 5 + [False],
        "deployed uniform rank boundary drift")
require(rank_rows[0]["mu"] == 12_799_651_012_707,
        "rank-four multiplicity drift")
require(rank_rows[0]["cap"] == 62_966_423_050,
        "rank-four cap drift")
require(rank_rows[4]["cap"] == 58_747_334_643_050_472,
        "rank-eight cap drift")
require(B_star - (U_paid + rank_rows[4]["cap"])
        == 216_233_390_865_841_616,
        "rank-eight margin drift")
require(rank_rows[5]["cap"] == 1_825_750_153_566_470_657,
        "rank-nine worst cap drift")


def rank9_mu(extension_factor):
    return ceil_div(extension_factor * math.comb(Delta0 + 8, 8), 9)


def rank9_cap(carrier_size, extension_factor):
    return math.comb(carrier_size, 9) // rank9_mu(extension_factor)


def largest_paid_carrier(extension_factor):
    lower = R_deployed + 11
    upper = n
    if rank9_cap(upper, extension_factor) <= B_remaining:
        return upper
    while lower < upper:
        middle = (lower + upper + 1) // 2
        if rank9_cap(middle, extension_factor) <= B_remaining:
            lower = middle
        else:
            upper = middle - 1
    return lower


rank9_boundaries = [largest_paid_carrier(ell) for ell in range(1, 8)]
require(
    rank9_boundaries
    == [1_699_344, 1_835_392, 1_919_971, 1_982_333,
        2_032_097, 2_073_683, 2_097_152],
    "rank-nine joint boundary drift",
)
for ell, maximum in enumerate(rank9_boundaries[:6], start=1):
    require(rank9_cap(maximum, ell) <= B_remaining,
            "rank-nine paid endpoint drift")
    require(rank9_cap(maximum + 1, ell) > B_remaining,
            "rank-nine first-unpaid endpoint drift")
require(rank9_cap(n, 7) <= B_remaining,
        "extension factor seven no longer pays full domain")


# Tiny GF(17) MDS row-basis control.
F = GF(17)
N_toy = 7
R_toy = 4
kappa_toy = N_toy - R_toy
points = [F(i) for i in range(N_toy)]
H = matrix(F, R_toy, N_toy,
           lambda row, column: points[column] ** row)

require(H.rank() == R_toy, "toy parity-check rank drift")
require(
    all(H.matrix_from_columns(list(cols)).rank() == R_toy
        for cols in combinations(range(N_toy), R_toy)),
    "toy parity check is not MDS",
)

K0_space = H.right_kernel()
G = K0_space.basis_matrix()
require(K0_space.dimension() == kappa_toy == 3,
        "toy kernel dimension drift")

minimum_weight = min(
    sum(1 for entry in word if entry != 0)
    for word in K0_space
    if word != 0
)
require(minimum_weight == R_toy + 1 == 5,
        "toy kernel distance drift")

# Add a nonkernel direction to obtain r=3, s=4.
v = vector(F, [1] + [0] * (N_toy - 1))
y1 = H * v
require(y1 != 0, "toy source direction vanished")
D = matrix(F, list(G.rows()) + [v])
r_toy = G.rank()
s_toy = D.rank()
require((r_toy, s_toy) == (3, 4), "toy actual-core rank drift")

q_toy = 6
mask = None
for candidate in combinations(range(N_toy), q_toy):
    if D.matrix_from_columns(list(candidate)).rank() == s_toy:
        mask = list(candidate)
        break
require(mask is not None, "no toy injective mask found")

k0_bases = [
    list(cols)
    for cols in combinations(mask, r_toy)
    if G.matrix_from_columns(list(cols)).rank() == r_toy
]
d_bases = [
    list(cols)
    for cols in combinations(mask, s_toy)
    if D.matrix_from_columns(list(cols)).rank() == s_toy
]

row_basis_floor = math.comb(q_toy - kappa_toy + r_toy, r_toy)
source_minimum_lift = 1  # v itself has weight one and y1 is nonzero.
ell_toy = max(1, source_minimum_lift + q_toy - N_toy)
mu_toy = ceil_div(ell_toy * row_basis_floor, s_toy)

require(len(k0_bases) >= row_basis_floor,
        "toy K0 row-basis floor drift")
require(len(d_bases) >= mu_toy,
        "toy D row-basis multiplicity drift")

extension_pairs = 0
minimum_extensions = None
for basis in k0_bases:
    G_B = G.matrix_from_columns(basis)
    coefficients = G_B.transpose().solve_right(vector(F, [v[i] for i in basis]))
    k_B = coefficients * G
    z_B = v - k_B
    extensions = [
        x for x in mask
        if x not in basis
        and z_B[x] != 0
        and D.matrix_from_columns(basis + [x]).rank() == s_toy
    ]
    require(len(extensions) >= ell_toy,
            "toy extension-factor mechanism drift")
    extension_pairs += len(extensions)
    minimum_extensions = (
        len(extensions)
        if minimum_extensions is None
        else min(minimum_extensions, len(extensions))
    )

require(extension_pairs >= ell_toy * len(k0_bases),
        "toy extension-pair total drift")
require(len(d_bases) * s_toy >= extension_pairs,
        "toy at-most-s deletion multiplicity drift")

output = {
    "schema": "rs-mca-m1-kb-branch3-actual-core-mds-v1-sage-control",
    "status": "PASS",
    "deployed_exact_arithmetic": {
        "rank_rows": rank_rows,
        "rank9_largest_paid_carriers_ell_1_to_7": rank9_boundaries,
        "rank9_ell7_full_domain_cap": rank9_cap(n, 7),
    },
    "GF17_mds_control": {
        "N": N_toy,
        "R": R_toy,
        "kappa": kappa_toy,
        "kernel_dimension": K0_space.dimension(),
        "kernel_minimum_distance": minimum_weight,
        "r": r_toy,
        "s": s_toy,
        "q": q_toy,
        "ell": ell_toy,
        "row_basis_floor": row_basis_floor,
        "K0_basis_count": len(k0_bases),
        "D_basis_count": len(d_bases),
        "mu_floor": mu_toy,
        "extension_pairs": extension_pairs,
        "minimum_extensions_per_K0_basis": minimum_extensions,
    },
    "nonclaims": [
        "not a deployed-field census",
        "not a proof of deployed selector rank",
        "not a replacement for the imported theorem",
    ],
}

print(json.dumps(output, sort_keys=True, default=int))
