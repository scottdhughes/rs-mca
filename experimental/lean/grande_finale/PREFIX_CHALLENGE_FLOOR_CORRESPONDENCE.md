# Prefix Proper-Challenge Floor Correspondence

Status: **PROVED** for the finite scalar-extension prefix-fiber floor after
restriction to an arbitrary extension-field challenge set.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially the
coefficient-prefix construction, equation (4.6),
`cor:exact-prefix-ray-realization`, and the proper-challenge averaging step in
equation (13.3).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Every explicit simple-pole bad-slope set is bounded by the full MCA numerator | `GrandeFinale.PrefixChallengeFloor.badSlopeSet_card_le_B_MCA` |
| Exact proper-challenge floor from a prescribed coefficient fiber | `GrandeFinale.PrefixChallengeFloor.extensionPrefix_challenge_floor` |
| Largest-fiber prefix floor with literal nested ceilings | `GrandeFinale.PrefixChallengeFloor.heavy_extensionPrefix_challenge_floor` |

## Statement comparison

Let `B` be a finite base field, `F` a finite field with an `Algebra B F`
structure, and `D` a finite evaluation subset of `B`.  For `0 < K <= m`, the
coefficient-prefix pigeonhole theorem selects a prefix fiber of size at least

`D.card.choose m ⌈/⌉ (Fintype.card B) ^ (m - K)`.

The scalar-extension list--line theorem realizes the chosen fiber as exactly
the bad slopes of an extension-field simple-pole line.  That explicit line is
bounded by the full MCA numerator.  The translate-intersection compiler then
retains the natural ceiling fraction `Gamma.card / Fintype.card F` for every
finite challenge set `Gamma`.

Under the uniform strict field-size budget

`D.card + (K - 1) * (D.card.choose m).choose 2 < Fintype.card F`,

the exported heavy-fiber theorem therefore proves the literal nested-ceiling
bound

```text
(Gamma.card *
    (D.card.choose m ⌈/⌉ (Fintype.card B) ^ (m - K))) ⌈/⌉
    Fintype.card F
  <= B_MCA_challenge (rsEval extensionEval (K - 1)) m Gamma.
```

The prescribed-fiber theorem keeps the sharper equation-(4.6) budget measured
using the actual complete list size.  The heavy-fiber theorem derives its
uniform budget by bounding that list by all `m`-subsets of `D` and applying
monotonicity of `Nat.choose`.

## Scope boundaries

The result is an exact finite theorem.  It retains both natural-number
ceilings and accepts an arbitrary finite challenge set, including a proper
subset of `F`.  The challenge numerator maximizes over received lines after
the translate/shear step; the theorem does not claim that the original
unshifted pole line itself meets every fixed challenge set.

The uniform equation-(4.6) hypothesis is sufficient and may be stronger than
the prescribed-fiber budget.  The theorem does not discharge the frontiers
paper's later asymptotic parameter translation, row-sharp Q input, or adjacent
threshold comparison, so it is not by itself the full asymptotic
`prop:simple-pole-lower` conclusion.

## Verification

```text
lake env lean GrandeFinale/PrefixChallengeFloor.lean
```

The module prints the axioms of its three principal results.  The audit reports
only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
