# Reed--Solomon Support-Hyperplane Correspondence

Status: **PROVED** for the exact syndrome-hyperplane family listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially the
`(R-1)`-support hyperplanes in the lower-bound proof of
`thm:exact-first-adjacent-row` (AD1).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| The syndrome image of errors supported on `E` is the span of the columns indexed by `E` | `GrandeFinale.RSSupportHyperplanes.syndromeSpan_parityCheck_eq_supportColumnSpan` |
| An at-most-`R` support span has dimension `|E|` | `GrandeFinale.RSSupportHyperplanes.supportColumnSpan_finrank` |
| Every exact `(R-1)` support span is a functional kernel | `GrandeFinale.RSSupportHyperplanes.exists_supportFunctional` |
| Distinct exact supports have distinct syndrome spans | `GrandeFinale.RSSupportHyperplanes.syndromeSpan_injective_of_card_eq` |
| The exact supports admit an injective family of nonzero functional kernels | `GrandeFinale.RSSupportHyperplanes.exists_distinct_supportHyperplanes` |

For distinct supports `E,E'` of size `R-1`, their union contains an
`R`-element subset. If the two support spans were equal, all `R` corresponding
columns would lie in one proper `(R-1)`-dimensional span, contradicting the
weighted Vandermonde independence theorem.

## Scope boundaries

This module supplies the distinct syndrome-hyperplane family used by the AD1
finite-avoidance construction. It does not prove the exact support upper bound,
compose the family with the separating-line theorem, or derive the final AD1
equality and AD2 implications.

## Verification

```text
lake env lean GrandeFinale/RSSupportHyperplanes.lean
```

The module prints the axioms of its principal results. No `sorry`, `admit`,
`native_decide`, or added axiom occurs.
