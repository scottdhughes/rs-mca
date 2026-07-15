# Exact First Adjacent Reed--Solomon Threshold Correspondence

Status: **PROVED** for both target-dependent implications in (AD2).

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`thm:exact-first-adjacent-row` and equation (AD2).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Proposition-level characterization of the first safe agreement | `GrandeFinale.RSFirstAdjacentThreshold.IsFirstSafeMCA` |
| A first safe agreement is unique | `GrandeFinale.RSFirstAdjacentThreshold.isFirstSafeMCA_unique` |
| `M <= b` makes `k+1` the first safe agreement | `GrandeFinale.RSFirstAdjacentThreshold.firstAdjacent_isFirstSafeMCA` |
| `choose n (R-2) <= b < M` makes `k+2` the first safe agreement | `GrandeFinale.RSFirstAdjacentThreshold.secondAdjacent_isFirstSafeMCA` |
| Both implications under the common `R >= 2` and field gate | `GrandeFinale.RSFirstAdjacentThreshold.exactFirstAdjacent_AD2` |

The first implication uses AD1 to make the first grid point safe. For the
second, AD1 makes `k+1` unsafe, while the exact support-atlas bound at `k+2`
and binomial symmetry make `k+2` safe. There is no intermediate integer grid
point, so these certificates are the exact first-safe statements.

## Statement comparison

The Lean theorems quantify an arbitrary natural-number budget `b`. Substituting
`b = floor (epsilon * |F|)` gives the manuscript statement. This is a harmless
generalization because the proof uses only the two displayed integer
comparisons in (AD2).

## Scope boundaries

The module gives the proposition-level threshold equalities. It does not
formalize real-valued floor arithmetic for a particular `epsilon` or introduce
a second computable first-safe scan.

## Verification

```text
lake env lean GrandeFinale/RSFirstAdjacentThreshold.lean
```

The module prints the axioms of its principal results. No proof placeholder or
added axiom occurs.
