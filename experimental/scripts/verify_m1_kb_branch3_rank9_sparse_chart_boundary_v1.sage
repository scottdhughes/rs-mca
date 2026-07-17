#!/usr/bin/env sage
"""Independent Sage control for the sparse chart-boundary route cut.

The script has two layers.

1. It recomputes the deployed KoalaBear dimensions and the conditional
   ``j + (R-j) = R`` arithmetic using exact Sage integers.
2. It reconstructs an exact GF(11) RS[8,3,6] sparse pair.  Its bad-slope
   atlas contains tangent slopes, a non-tangent root of one fixed chosen
   maximal minor at which the full matrix still has maximal row rank, and
   regular-chart non-tangent slopes.

The finite example is a guardrail, not a deployed-field census and not a
replacement for the symbolic proof.
"""

from itertools import combinations
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# -------------------------------------------------------------------------
# Exact deployed arithmetic.
# -------------------------------------------------------------------------

p = ZZ(2_130_706_433)
extension_degree = ZZ(6)
q_line = p ** extension_degree
n = ZZ(2_097_152)
k = ZZ(1_048_576)
A = ZZ(1_116_048)
R = n - k
j = n - A
matrix_rows = R - j
matrix_columns = j + 1
h = 2 * j - R - 1
kernel_dimension = matrix_columns - matrix_rows
support_floor = matrix_rows + 1
tangent_cap = j
chart_boundary_cap = matrix_rows
conditional_union_cap = tangent_cap + chart_boundary_cap
B_star = (q_line - 1) // (ZZ(2) ** 128)
U_paid = ZZ(2_602_502_999)
B_remaining = B_star - U_paid

require(R == 1_048_576, "deployed redundancy drift")
require(j == 981_104, "deployed radius drift")
require(matrix_rows == 67_472, "deployed Hankel row count drift")
require(matrix_columns == 981_105, "deployed Hankel column count drift")
require(h == 913_631, "deployed residual excess drift")
require(kernel_dimension == 913_633 == h + 2,
        "deployed regular-kernel dimension drift")
require(support_floor == 67_473,
        "deployed non-tangent support floor drift")
require(conditional_union_cap == R,
        "deployed conditional two-cell cap drift")
require(B_remaining == 274_980_725_508_892_088,
        "deployed remaining-budget drift")


# -------------------------------------------------------------------------
# Exact GF(11) RS[8,3,6] Padé--Hankel control.
# -------------------------------------------------------------------------

F = GF(11)
D = [F(i) for i in range(8)]
n_toy = ZZ(len(D))
k_toy = ZZ(3)
m_toy = n_toy - k_toy
r_toy = ZZ(3)
rows_toy = m_toy - r_toy
columns_toy = r_toy + 1
h_toy = 2 * r_toy - m_toy - 1

require(len(set(D)) == n_toy, "toy evaluation points are not distinct")
require((m_toy, r_toy, rows_toy, columns_toy, h_toy) == (5, 3, 2, 4, 0),
        "toy dimensions drift")

lambdas = []
for x in D:
    derivative_value = F(1)
    for y in D:
        if y != x:
            derivative_value *= x - y
    require(derivative_value != 0, "toy syndrome weight denominator vanished")
    lambdas.append(1 / derivative_value)


def syndrome(word):
    return vector(
        F,
        [
            sum(lambdas[i] * D[i] ** a * word[i] for i in range(n_toy))
            for a in range(m_toy)
        ],
    )


def hankel(word):
    syn = syndrome(word)
    return matrix(
        F,
        rows_toy,
        columns_toy,
        lambda a, b: syn[a + b],
    )


RX = PolynomialRing(F, "X")
X = RX.gen()


def locator_vector(T):
    locator = prod(X - D[i] for i in T)
    require(locator.is_monic(), "toy locator is not monic")
    require(locator.degree() == r_toy, "toy locator degree drift")
    return vector(F, [locator[i] for i in range(r_toy + 1)])


support_E = (0, 1, 2)
epsilon_1 = vector(F, [10, 1, 3, 0, 0, 0, 0, 0])
epsilon_2 = vector(F, [1, 1, 9, 0, 0, 0, 0, 0])
actual_support = tuple(
    i for i in range(n_toy) if epsilon_1[i] != 0 or epsilon_2[i] != 0
)
require(actual_support == support_E, "toy actual sparse support drift")
require(all(epsilon_2[i] != 0 for i in support_E),
        "toy active-coordinate pattern drift")

H_1 = hankel(epsilon_1)
H_2 = hankel(epsilon_2)
require(
    H_1.list() == [F(x) for x in [0, 1, 4, 10, 1, 4, 10, 0]],
    "toy H_1 drift",
)
require(
    H_2.list() == [F(x) for x in [2, 7, 5, 1, 7, 5, 1, 4]],
    "toy H_2 drift",
)

all_T = list(combinations(range(n_toy), r_toy))
ell_by_T = {T: locator_vector(T) for T in all_T}


def is_tangent(gamma):
    v_gamma = epsilon_1 + gamma * epsilon_2
    return any(v_gamma[i] == 0 for i in support_E)


def witnesses(gamma):
    M_gamma = H_1 + gamma * H_2
    return [
        T
        for T in all_T
        if M_gamma * ell_by_T[T] == 0 and H_2 * ell_by_T[T] != 0
    ]


tangent_slopes = [gamma for gamma in F if is_tangent(gamma)]
require([ZZ(gamma) for gamma in tangent_slopes] == [1, 7, 10],
        "toy tangent atlas drift")
require(len(tangent_slopes) == len(support_E) == r_toy,
        "toy tangent cap is not saturated")

bad_atlas = []
for gamma in F:
    witness_list = witnesses(gamma)
    if witness_list:
        bad_atlas.append(
            {
                "gamma": gamma,
                "tangent": is_tangent(gamma),
                "rank": (H_1 + gamma * H_2).rank(),
                "witnesses": witness_list,
            }
        )

require(
    [ZZ(entry["gamma"]) for entry in bad_atlas] == [1, 2, 3, 5, 6, 7, 10],
    "toy bad-slope atlas drift",
)
require(
    [ZZ(entry["gamma"]) for entry in bad_atlas if entry["tangent"]]
    == [1, 7, 10],
    "toy tangent bad-slope partition drift",
)

non_tangent_bad = [entry for entry in bad_atlas if not entry["tangent"]]
require(
    [ZZ(entry["gamma"]) for entry in non_tangent_bad] == [2, 3, 5, 6],
    "toy non-tangent bad-slope partition drift",
)
require(all(entry["rank"] == rows_toy for entry in non_tangent_bad),
        "toy non-tangent bad matrix lost full row rank")

# Freeze one anchor and one column set for the whole sparse pair.  The anchor
# is an actual non-tangent bad slope, and the selected minor is nonzero there.
gamma_0 = F(2)
chosen_columns = (0, 1)
M_0 = H_1 + gamma_0 * H_2
require(witnesses(gamma_0), "toy anchor is not bad")
require(not is_tangent(gamma_0), "toy anchor is tangent")
require(M_0.matrix_from_columns(chosen_columns).det() != 0,
        "toy chosen minor vanishes at its anchor")

Rz = PolynomialRing(F, "z")
z = Rz.gen()
M_z = H_1.change_ring(Rz) + z * H_2.change_ring(Rz)
Delta = M_z.matrix_from_columns(chosen_columns).det()
require(Delta != 0, "toy chosen minor is the zero polynomial")
require(Delta == 5 * z ** 2 + 5 * z + 10,
        "toy chosen-minor polynomial drift")
require(Delta.degree() == rows_toy,
        "toy chosen-minor degree does not saturate the row bound")

minor_roots = [gamma for gamma in F if Delta(gamma) == 0]
require([ZZ(gamma) for gamma in minor_roots] == [4, 6],
        "toy chosen-minor root set drift")
require(len(minor_roots) == rows_toy,
        "toy chosen-minor root cap is not saturated")

boundary_bad = [
    entry for entry in non_tangent_bad if Delta(entry["gamma"]) == 0
]
regular_bad = [
    entry for entry in non_tangent_bad if Delta(entry["gamma"]) != 0
]
require([ZZ(entry["gamma"]) for entry in boundary_bad] == [6],
        "toy chart-boundary bad set drift")
require([ZZ(entry["gamma"]) for entry in regular_bad] == [2, 3, 5],
        "toy regular-chart bad set drift")

# The load-bearing guardrail: gamma=6 is a root of the chosen minor but the
# full matrix still has maximal row rank through another minor.
gamma_boundary = F(6)
M_boundary = H_1 + gamma_boundary * H_2
require(Delta(gamma_boundary) == 0,
        "toy chart-boundary slope no longer kills the chosen minor")
require(M_boundary.rank() == rows_toy,
        "toy chart-boundary slope became a global rank drop")
alternate_columns = (0, 2)
require(M_boundary.matrix_from_columns(alternate_columns).det() != 0,
        "toy alternate maximal minor vanished")

# Every recorded witness is a D-split squarefree locator of size r and passes
# the same-support noncontainment gate exactly.
for entry in bad_atlas:
    gamma = entry["gamma"]
    M_gamma = H_1 + gamma * H_2
    for T in entry["witnesses"]:
        require(len(T) == r_toy == len(set(T)), "toy witness support drift")
        require(set(T).issubset(set(range(n_toy))), "toy witness leaves D")
        ell_T = ell_by_T[T]
        require(M_gamma * ell_T == 0, "toy locator kernel equation failed")
        require(H_2 * ell_T != 0, "toy noncontainment gate failed")

tangent_bad_set = {
    entry["gamma"] for entry in bad_atlas if entry["tangent"]
}
boundary_bad_set = {entry["gamma"] for entry in boundary_bad}
regular_bad_set = {entry["gamma"] for entry in regular_bad}
require(not (tangent_bad_set & boundary_bad_set),
        "toy tangent/boundary cells overlap")
require(not (tangent_bad_set & regular_bad_set),
        "toy tangent/regular cells overlap")
require(not (boundary_bad_set & regular_bad_set),
        "toy boundary/regular cells overlap")
require(
    tangent_bad_set | boundary_bad_set | regular_bad_set
    == {entry["gamma"] for entry in bad_atlas},
    "toy first-match cells do not exhaust the bad atlas",
)


output = {
    "schema": "rs-mca-m1-kb-branch3-rank9-sparse-chart-boundary-v1-sage-control",
    "status": "PASS",
    "deployed_exact_arithmetic": {
        "p": p,
        "extension_degree": extension_degree,
        "q_line": q_line,
        "n": n,
        "k": k,
        "A": A,
        "R": R,
        "j": j,
        "matrix_rows": matrix_rows,
        "matrix_columns": matrix_columns,
        "residual_excess_h": h,
        "regular_kernel_dimension": kernel_dimension,
        "non_tangent_support_floor": support_floor,
        "tangent_conditional_cap": tangent_cap,
        "chart_boundary_conditional_cap": chart_boundary_cap,
        "two_cell_conditional_union_cap": conditional_union_cap,
        "U_paid": U_paid,
        "B_remaining": B_remaining,
        "ledger_movement": 0,
    },
    "GF11_RS_8_3_6_control": {
        "field": "GF(11)",
        "evaluation_domain": [ZZ(x) for x in D],
        "n": n_toy,
        "k": k_toy,
        "redundancy": m_toy,
        "radius": r_toy,
        "matrix_rows": rows_toy,
        "matrix_columns": columns_toy,
        "residual_excess_h": h_toy,
        "actual_sparse_support": list(support_E),
        "epsilon_1": [ZZ(x) for x in epsilon_1],
        "epsilon_2": [ZZ(x) for x in epsilon_2],
        "tangent_slopes": [ZZ(x) for x in tangent_slopes],
        "bad_slopes": [ZZ(entry["gamma"]) for entry in bad_atlas],
        "non_tangent_bad_slopes": [
            ZZ(entry["gamma"]) for entry in non_tangent_bad
        ],
        "chosen_anchor": ZZ(gamma_0),
        "chosen_columns": list(chosen_columns),
        "chosen_minor": str(Delta),
        "chosen_minor_degree": Delta.degree(),
        "chosen_minor_roots": [ZZ(x) for x in minor_roots],
        "chart_boundary_bad_slopes": [
            ZZ(entry["gamma"]) for entry in boundary_bad
        ],
        "regular_chart_bad_slopes": [
            ZZ(entry["gamma"]) for entry in regular_bad
        ],
        "boundary_full_matrix_rank": M_boundary.rank(),
        "boundary_alternate_columns": list(alternate_columns),
        "boundary_alternate_minor_nonzero": True,
        "same_support_noncontainment_checked": True,
        "cells_disjoint_and_exhaustive": True,
    },
    "nonclaims": [
        "not a deployed-field census",
        "not a proof of the symbolic tangent or chosen-minor bounds",
        "not a bound on the regular split-locator chart",
        "not global first-match aggregation",
        "not ledger movement",
        "not rank-nine, branch-3, or KoalaBear-row closure",
    ],
}

print(json.dumps(output, sort_keys=True, default=int))
