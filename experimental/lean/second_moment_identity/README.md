# Curve second-moment identity

This stdlib-only Lean package formalizes the finite combinatorial core of
`experimental/notes/thresholds/cap25_v13_bc_l4_curve_second_moment.md`.

The principal results are:

- `curveSecondMoment_eq_orderedPairs`: the sum of squared fiber sizes is the
  exact length of the common-fiber ordered-pair enumeration;
- `secondMoment_diagonal_offDiagonal`: the pair ledger splits into diagonal
  mass and `q(q-1)` off-diagonal pairs;
- `cauchySchwarz` and `mass_le_of_secondMoment_ceiling`: a general
  natural-number Cauchy--Schwarz inequality and its denominator-cleared
  square-root compiler;
- `pFold_average_identity`: exact total mass for a p-to-one cover;
- `curveSum_twist` and `curveSum_orbit_constancy`: abstract equivariance
  and orbit-constancy compilers;
- `L4.fixture`, `L4.dominantE_in_range`, and the remaining `L4`
  declarations: exact integer fixture and cleared arithmetic pins used by the
  companion verifier.

Build with:

```sh
lake build
```

Then run the independent source checks from the repository root:

```sh
python3 experimental/scripts/verify_bc_l4_curve_second_moment.py
python3 experimental/scripts/verify_bc_l4_curve_second_moment.py --tamper-selftest
```

## Proof boundary

The finite list theorems, pair enumerations, p-fold identity, twist compilers,
and integer gates are kernel-checked and unconditional. The companion Python
verifier independently computes the deployed large-binomial and logarithmic
L4 ceilings, exhaustively checks its finite-field toy rows, and tests every
pinned observable.

This package does not turn floating-point logarithmic output into a Lean
theorem. It does not assert the source note's measured residual law, a local
limit, worst-case residual equidistribution, or an asymptotic improvement.
See `CORRESPONDENCE.md` for the exact statement map.
