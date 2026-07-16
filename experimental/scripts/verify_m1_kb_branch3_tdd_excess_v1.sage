#!/usr/bin/env sage
"""Independent Sage replay for the branch-3 TDD excess route cut.

This is a finite-field control, not a deployed-field enumeration.  It checks:

* shortened RS spaces on unions of excess e=0,1,2 have dimension e+1;
* the exact e=1 disjoint-support construction over GF(17);
* the TDD factorization and silent-shell statement in that construction;
* full selected-error affine rank and residual-codeword rank differ by one;
* every selected support is transverse to the two syndrome directions.
"""

import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


F = GF(17)
Rpoly.<X> = PolynomialRing(F)
D = [F(i) for i in range(8)]
n = 8
k = 4
R = n - k
d = R + 1


def evaluate(poly):
    return vector(F, [poly(x) for x in D])


def support(vector_value):
    return [i for i, value in enumerate(vector_value) if value != 0]


shortened = []
for excess in range(3):
    union_size = R + 1 + excess
    U_indices = list(range(union_size))
    complement = [D[i] for i in range(union_size, n)]
    M_U = prod(X - point for point in complement)
    basis = [evaluate(M_U * X^power) for power in range(excess + 1)]
    rank = matrix(F, basis).rank()
    require(M_U.degree() == k - 1 - excess, "locator degree drift")
    require(
        all((M_U * X^power).degree() < k for power in range(excess + 1)),
        "shortened basis left the RS degree range",
    )
    require(rank == excess + 1, "shortened dimension is not e+1")
    require(
        all(
            all(vector_value[i] == 0 for i in range(union_size, n))
            for vector_value in basis
        ),
        "shortened basis leaks outside U",
    )
    shortened.append(
        {
            "excess": int(excess),
            "union_size": int(union_size),
            "locator_degree": int(M_U.degree()),
            "shortened_dimension": int(rank),
        }
    )


# Exact e=1 fixture: R+2=6=3*2.
E0 = {0, 1}
E1 = {2, 3}
Ea = {4, 5}
U = E0 | E1 | Ea
a_slope = F(2)
M_U = prod(X - D[i] for i in range(n) if i not in U)
Delta = evaluate(M_U)
zero = vector(F, [0] * n)
c0 = zero
c1 = zero
ca = -Delta

f = vector(F, [0] * n)
g = vector(F, [0] * n)
for i in E0:
    f[i] = -Delta[i] / (1 - a_slope)
    g[i] = Delta[i] / (1 - a_slope)
for i in E1:
    g[i] = -Delta[i] / a_slope

e0 = f - c0
e1 = f + g - c1
ea = f + a_slope * g - ca
tdd = (1 - a_slope) * c0 + a_slope * c1 - ca

require(set(support(e0)) == E0, "slope-zero support drift")
require(set(support(e1)) == E1, "slope-one support drift")
require(set(support(ea)) == Ea, "slope-a support drift")
require(tdd == Delta and tdd != zero, "TDD identity drift")
require(set(support(tdd)) == U, "e=1 fixture acquired a silent shell")
require(M_U.degree() == k - 2, "e=1 locator degree drift")
require(len(U) - (R + 1) == 1, "triple excess drift")
require(len(U) - R == 2, "carrier excess drift")
require(2 + 1 < d, "toy deep-owner uniqueness inequality drift")


# Parity check for the [8,4,5] evaluation code.
generator = matrix(F, [[point^power for point in D] for power in range(k)])
H = generator.right_kernel().basis_matrix()
require(H.nrows() == R and H.ncols() == n, "parity-check shape drift")
require(generator * H.transpose() == 0, "parity-check orthogonality drift")

y0 = H * f
y1 = H * g
require(y1 != 0, "syndrome direction vanished")


def column_span_rank(indices, extra_columns=()):
    columns = [H.column(i) for i in sorted(indices)] + list(extra_columns)
    if not columns:
        return 0
    return matrix(F, columns).transpose().rank()


transverse = []
for label, indices in (("0", E0), ("1", E1), ("2", Ea)):
    base_rank = column_span_rank(indices)
    with_both = column_span_rank(indices, (y0, y1))
    is_transverse = with_both > base_rank
    require(is_transverse, "selected support is not transverse")
    transverse.append(
        {
            "slope": label,
            "support_rank": int(base_rank),
            "rank_with_both_syndromes": int(with_both),
            "transverse": bool(is_transverse),
        }
    )


# Anchor slopes 0 and 1 give p=q=0.  The sole nonzero residual is ca.
selected_differences = matrix(F, [e1 - e0, ea - e0])
affine_rank = selected_differences.rank()
residual_rank = matrix(F, [ca]).rank()
require(affine_rank == 2, "selected affine rank drift")
require(residual_rank == 1, "residual-codeword rank drift")
require(affine_rank == residual_rank + 1, "rank bridge drift")

summary = {
    "schema": "rs-mca-m1-kb-branch3-tdd-excess-v1-sage-control",
    "field": int(17),
    "code": {
        "n": int(n),
        "k": int(k),
        "R": int(R),
        "minimum_distance": int(d),
    },
    "shortened_spaces": shortened,
    "e1_fixture": {
        "slopes": [int(0), int(1), int(2)],
        "support_weights": [int(len(E0)), int(len(E1)), int(len(Ea))],
        "pairwise_disjoint": True,
        "triple_excess": int(len(U) - (R + 1)),
        "carrier_excess": int(len(U) - R),
        "silent_shell_size": int(len(U - set(support(tdd)))),
        "selected_affine_rank": int(affine_rank),
        "residual_codeword_rank": int(residual_rank),
        "rank_bridge": bool(affine_rank == residual_rank + 1),
        "transversality": transverse,
    },
}

print(json.dumps(summary, sort_keys=True, default=int))
