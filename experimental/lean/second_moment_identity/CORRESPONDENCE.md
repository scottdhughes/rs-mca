# Statement correspondence

Source:
`experimental/notes/thresholds/cap25_v13_bc_l4_curve_second_moment.md`

Independent verifier:
`experimental/scripts/verify_bc_l4_curve_second_moment.py`

## C1: curve second moment

The source identity
`M2 = sum_s N(theta(s))^2` equals the number of ordered valid pairs with a
common curve parameter.

- `orderedPairs_length` proves that a finite fiber of size `q` contributes
  exactly `q^2` ordered pairs.
- `curveSecondMoment_eq_orderedPairs` sums this equality over explicit finite
  fiber enumerations.
- `square_eq_diagonal_add_offDiagonal` and
  `secondMoment_diagonal_offDiagonal` split the result into the diagonal
  mass and the off-diagonal `q(q-1)` shift-pair ledger.

The Lean statement uses an explicit list of fibers. Instantiating it with the
source curve fibers requires only a duplicate-free enumeration of each finite
fiber; the theorem does not assume the field-specific curve construction.

## Cauchy--Schwarz conversion

- `twice_mul_le_sq_add_sq` is the elementary two-variable inequality.
- `cauchySchwarz` proves
  `(sum q)^2 <= (# fibers) * sum q^2` for every natural fiber table.
- `mass_le_of_secondMoment_ceiling` converts a cleared upper bound
  `(# fibers) * M2 <= B^2` into `sum q <= B`.
- `sumSq_le_max_mul_sum` retains the complementary max-fiber bound from the
  original toy module.

No real square root or rounding convention is hidden in these declarations.

## C2: p-fold average and twists

- `pFold_average_identity` proves the exact combinatorial heart of
  `sum_y S(y) = p * total`: each bucket contribution occurs exactly `p`
  times.
- `curveSum_twist` proves equality of a twisted curve sum from termwise
  equivariance and weight invariance.
- `curveSum_orbit_constancy` adds stability of the finite parameter
  enumeration and obtains orbit constancy.

These are abstract compilers. The field-specific preimage census,
root-of-unity action, and Lagrange checks remain independently verified by the
source script.

## L4 fixture and numerical ceilings

Namespace `SecondMomentIdentity.L4` kernel-checks the exact integer fixture:
`n=131072`, `k=65537`, `m=69753`, `p=2130706433`, `w=4216`,
`depth=4217`, `eMin=4218`, `eMax=61319`, dominant index `32632`,
and `57102` eligible strata. It also checks the exact mini-row average and
the cleared row-A/row-B Cauchy--Schwarz inequalities.

The large binomial integers, rational ratio crossing, logarithmic bracket,
top-stratum ceiling, twist-amplified bounds, and packing cross-check are
computed by the companion verifier. Their decimal logarithms are not promoted
to kernel theorems.

## Explicit nonclaims

This package does not prove a residual equidistribution law, local central
limit theorem, asymptotic rate, global optimality statement, or improvement of
the unconditional L4 numerical bound. The measured residual behavior in the
source note remains experimental.
