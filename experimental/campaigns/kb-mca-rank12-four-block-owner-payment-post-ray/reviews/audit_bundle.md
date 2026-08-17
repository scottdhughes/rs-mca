# Independent audit bundle

## Verdict

**GREEN for the stated proper-drop payment on `K >= 662,480`.**

## Hostile checks performed

### Source and chronology

The proof partitions the already-frozen exact supports into supports meeting
or avoiding the actual full common pair core. No support is refrozen after the
partition, and no local locator payment is summed over overlapping slopes.
The rank-one part uses the global all-dimension cap rather than the smaller
capacity at the minimum locator floor; this avoids the monotonicity error that
a larger actual core can increase the effective rank-one capacity.

### Four-slope algebra

For four witness slopes, the vector-valued cubic interpolation has two
independent nonaffine coefficients. The four omission sets must cover the
shortened domain, or one coordinate annihilates the complete direction plane
and becomes a forbidden whole-family pair core.

On each clean block the agreement equation is linear in the correction
coefficients and slope. For any three blocks, the consistency determinant is
a degree-one polynomial in the slope. Its leading coefficient reduces to a
Vandermonde in the three distinct omitted-slope sums and is nonzero. The
unique root is the remaining base slope. Thus the proof has no hidden
identity-triplet owner.

### Fixed-pair owners

Two clean equations determine one affine codeword pair. Same-support pair
noncontainment forces at least one dirty coordinate outside its simultaneous
agreement set. Charging non-pair dirty coordinates gives the printed bound
`max(0,b_i+b_j+y-m+1)`.

### Correction rays

After cancelling the clean universal core and any further ray-universal
coordinates, the parameter conditions are weighted affine lines. If one graph
clone has weight at least the residual dimension, every selected point lies
on it and the count is at most `rho+1`. Otherwise heterogeneous coordinate
pairs charge injectively. These cases are mutually exclusive, so the proof
uses a maximum, not an invalid sum.

The endpoint quotients are convex on both legal agreement-threshold ranges.
In the dirty regime each candidate is decreasing and convex in the dirty
incidence variable. Majorization therefore reduces two active rays to the two
endpoint profiles used by the verifier.

### Dirty-incidence optimizer

The pair-owner objective is symmetric and convex in the four dirty incidence
counts with fixed sum and box constraints. It is Schur-convex, so its maximum
occurs at the maximally unequal vector. This yields the two displayed endpoint
profiles and, at the global dirty endpoint, the exact pair/triplet bound
`r+4 eta+9`.

## Exact independent replay

The separate audit reconstructs:

- all `386,098` cells including the adjacent wall;
- the common-locator inversion;
- all three regimes;
- the first-cell exact ray fractions;
- the unique global maximum at `K=662,480`;
- finite-field triplet controls over `GF(7)` and `GF(11)`.

Wolfram independently reproduced the two boundary totals:

```text
K=662,479: total 5,170,930, slack -18
K=662,480: total 5,170,907, slack   5
```

and confirmed that the triplet determinant is affine in the slope and that
the two endpoint functions have nonnegative second derivatives.

## Literature scope

A targeted primary-literature review covered current MCA and Reed--Solomon
shortening work, including Jo's 2026 beyond-Johnson theorem, Chojecki's
shortening bounds, Haboeck's MCA note, and current interleaving results. None
contains the source-bound four-block owner theorem used here. No external
numerical theorem is load-bearing.

## Remaining risk boundary

The five-unit slack is genuine but narrow. Any future source integration must
preserve the exact support partition, full-core convention, global rank-one
cap, and floor-after-summing rule for the two real ray envelopes. The adjacent
cell is not paid by this packet.
