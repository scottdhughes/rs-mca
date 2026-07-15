# Exact Finite Profile Compiler Correspondence

Status: **PROVED** for the finite implications behind (FC1) and (FC2), from
the explicit structural and counting hypotheses listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`thm:exact-finite-profile-compiler`.

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Bipartite incidence double count | `GrandeFinale.ExactProfileCompiler.incidence_double_count` |
| Residual moment normalized by the full support-slice mean | `GrandeFinale.ExactProfileCompiler.residualMoment` |
| Exact residual moment-root bound on each fiber | `GrandeFinale.ExactProfileCompiler.fiber_le_barN_mul_momentRoot` |
| Support-pair count is at most residual mass times the largest fiber | `GrandeFinale.ExactProfileCompiler.pairCount_le_total_mul_max` |
| Literal natural-number floor in (FC1) | `GrandeFinale.ExactProfileCompiler.primitiveCell_slope_card_le_floor` |
| Available moment/direct budget, using the minimum when both occur | `GrandeFinale.ExactProfileCompiler.mergedBudget`, `GrandeFinale.ExactProfileCompiler.PrimitiveCellBudget.actual_le_merged` |
| Per-line first-match sum in (FC2) | `GrandeFinale.ExactProfileCompiler.profileCompiler_line_bound` |
| Maximum of the per-line bounds | `GrandeFinale.ExactProfileCompiler.profileCompiler_max_bound` |

## Statement comparison

For (FC1), the Lean theorem takes finite bad-slope, support-pair, and syndrome
sets together with the incidence relation and fiber counts. It assumes the
exact identities
`|P| = sum_s Q(s)^2` and `sum_s Q(s) = W`, a selected largest fiber,
and the displayed lower and upper incidence degrees. Its supplied positive
`barN` is the manuscript's full support-slice mean `M/L`; the residual
moment is normalized by that value even though the residual counts need not
sum to `M`. The conclusion is the literal floor

`floor(((J * W) / H) * barN * (L * Gamma)^(1/q))`.

For (FC2), `PrimitiveCellBudget` records whether the moment budget, direct
budget, or both have been certified. The per-line theorem sums those exact
budgets from a supplied closed first-match inequality, and the final theorem
takes a finite supremum over received lines.

## Scope boundaries

The module does not construct a witness-exhaustive atlas, derive the
support-pair identity from Reed--Solomon witnesses, or produce the certified
incidence relation and its degrees. Those are explicit inputs, as they are in
the source theorem. The challenge-set intersection, adjacent unsafe/safe
comparison, and final threshold conclusion remain factored through the
existing challenge and threshold results rather than being duplicated here.

## Verification

```text
lake env lean GrandeFinale/ExactProfileCompiler.lean
```

The module prints the axioms of its principal results. The audit reports only
Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
