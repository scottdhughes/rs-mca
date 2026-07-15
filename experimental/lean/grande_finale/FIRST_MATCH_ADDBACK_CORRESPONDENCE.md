# First-Match and Weighted Add-Back Correspondence

Status: **PROVED** for the exact finite first-match, union, overlap, and
weighted add-back statements listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`lem:first-match-bound`, `prop:first-match-sum-detail`,
`lem:exact-profile-addback`, and `lem:profile-summation`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Assign each slope to the least-index cell containing it | `GrandeFinale.FirstMatchAddBack.firstMatchCell` |
| First-match cells are disjoint and retain the original union | `GrandeFinale.FirstMatchAddBack.firstMatchCell_pairwiseDisjoint`, `GrandeFinale.FirstMatchAddBack.biUnion_firstMatchCell_eq` |
| First-match cardinalities sum exactly to the distinct union size | `GrandeFinale.FirstMatchAddBack.sum_card_firstMatchCell_eq` |
| Exact per-line first-match budget sum | `GrandeFinale.FirstMatchAddBack.firstMatch_union_card_le_sum_budget` |
| Finite family-size-times-budget union bound | `GrandeFinale.FirstMatchAddBack.profileUnion_card_le_family_mul_budget` |
| Maximum full-slice overlap and its mass bound | `GrandeFinale.FirstMatchAddBack.overlapMultiplicity`, `GrandeFinale.FirstMatchAddBack.sum_slice_card_le_overlap_mul_union_card` |
| A nonempty partition has overlap multiplicity one | `GrandeFinale.FirstMatchAddBack.overlapMultiplicity_eq_one_of_pairwiseDisjoint` |
| Exact weighted add-back (AB1) | `GrandeFinale.FirstMatchAddBack.weightedProfileAddBack_ab1` |
| Common-target coverage rewrite (AB2) | `GrandeFinale.FirstMatchAddBack.weightedProfileAddBack_ab2` |
| Uniform coverage and overlap bound (AB3) | `GrandeFinale.FirstMatchAddBack.weightedProfileAddBack_ab3` |

## Statement comparison

The ordered first-match construction is generic over a finite linearly ordered
index set and arbitrary finite slope sets. It proves the disjoint-union
identity before applying any cell budgets.

For weighted add-back, the manuscript's nonempty full slice and image map are
represented by their exact cardinal consequences `0 < L_lambda` and
`L_lambda <= M_lambda`. The budget and loss factors are allowed to be real,
which includes the manuscript's integer counts after coercion. AB2 uses the
literal coverage factor `A/L_lambda`. AB3 defines `mu` as the maximum number
of full slices containing a support and proves
`sum M_lambda <= mu * |union Omega_lambda|` by finite incidence counting.

## Scope boundaries

The module does not construct a witness-exhaustive atlas or certify individual
cell budgets. It also does not replace the asymptotic notation in
`lem:profile-summation` with a separate sequence-level interface. Instead,
`profileUnion_card_le_family_mul_budget` proves its exact finite input:
`|union E_i| <= |I| * B`. Maximization over received lines is already
provided by `ExactProfileCompiler.profileCompiler_max_bound`.

## Verification

```text
lake env lean GrandeFinale/FirstMatchAddBack.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
