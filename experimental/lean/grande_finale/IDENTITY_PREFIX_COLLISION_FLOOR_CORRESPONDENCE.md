# Identity-Prefix Collision-Aware Floor Correspondence

Status: **PROVED** for the exact finite identity-prefix MCA floor in equation
(4.3) and its proper-challenge ceiling transfer.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`thm:collision-aware-pole`, equation `eq:collision-aware-pole` (4.2), and
`cor:identity-prefix-floor`, equation `eq:identity-prefix-floor` (4.3).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Pigeonhole list size `L_m` | `GrandeFinale.IdentityPrefixCollisionFloor.identityPrefixListFloor` |
| Collision-aware distinct-slope function `M(L)` | `GrandeFinale.IdentityPrefixCollisionFloor.collisionAwareFloor` |
| Exact identity-prefix full-field floor (4.3) | `GrandeFinale.IdentityPrefixCollisionFloor.identityPrefix_collisionAware_floor` |
| Proper-challenge ceiling applied to (4.3) | `GrandeFinale.IdentityPrefixCollisionFloor.identityPrefix_collisionAware_challenge_floor` |

## Statement comparison

Let `D` be a finite subset of the finite field `F`, let `k + 1 <= m <= |D|`,
and assume `|F| > |D|`.  Lean defines the source quantities literally as

```text
L_m = choose |D| m ⌈/⌉ |F|^(m-k-1),
M(L) = L * (|F|-|D|) ⌈/⌉
  ((|F|-|D|) + k * (L-1)).
```

The coefficient-prefix depth is `m - (k + 1) = m - k - 1`.  The pigeonhole
theorem supplies a complete prefix list of cardinality at least `L_m`.  Lean
then selects a sublist of cardinality exactly `L_m`; every selected polynomial
still has natural degree at most `k` and agrees with the received word on at
least `m` evaluation points.  Applying the existing polynomial-family
collision-aware pole theorem gives

```text
M(L_m) <= B_MCA (rsEval domainEval k) m,
```

which is the exact agreement-indexed numerator form of equation (4.3).
Selecting an exact-size sublist avoids relying on an unproved monotonicity
claim for the displayed ceiling expression.

The challenge corollary applies the finite translate-intersection compiler to
the full-field inequality and proves

```text
ceilDiv (Gamma.card * M(L_m)) |F|
  <= B_MCA_challenge (rsEval domainEval k) m Gamma
```

for every finite challenge set `Gamma`.

## Scope boundaries

The source corollary is same-field: the evaluation domain, prefix list, line,
and MCA numerator all live over `F`.  The hypotheses `m <= |D|` and
`|D| < |F|` make explicit the ambient context used by the source and ensure
that `L_m` is positive and an off-domain pole exists.

The challenge corollary maximizes over received lines after the exact shear
step; it does not claim that one fixed unshifted line meets every challenge
set.  Neither theorem proves a row-sharp Q bound or an asymptotic threshold
comparison.

## Verification

```text
lake env lean GrandeFinale/IdentityPrefixCollisionFloor.lean
```

The module prints the axioms of both principal results.  The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
