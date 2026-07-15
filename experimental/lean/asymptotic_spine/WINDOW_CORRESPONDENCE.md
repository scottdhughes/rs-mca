# Window-uniformity statement correspondence

Source:
`experimental/notes/audits/asymptotic_window_uniformity.md`

Verifier:
`experimental/scripts/verify_asymptotic_window_uniformity.py`

Lean modules:
`AsymptoticSpine/Window.lean` and
`AsymptoticSpine/WindowCells.lean`.

## Lemma W and Lemma B

`Window.lean` already proves:

- bounded local rate implies a linear window-variation bound;
- the reference-scale decomposition combines binomial and subfield rates;
- finite `LittleO` constant multiplication and addition;
- pointwise bounded-complexity budget aggregation;
- the single-cell discharge principle;
- the four-part U0/U1/U2/U3 cleared aggregation.

The analytic facts that supply the finite step rates—Stirling, the entropy MVT
bound on an interior interval, bounded base size, and source-specific binomial
ratio estimates—are hypotheses, not hidden axioms.

## C1--C8 finite aggregation

`WindowCells.lean` names the eight established cells with
`EstablishedCell` and the duplicate-free list `establishedCells`.

A `WindowPayment` records exactly the two source-side inputs for one cell:

1. its window value is at most a local ratio times its center value;
2. its center value is paid by a multiplier times the center reference scale.

`WindowPayment.windowPaid` composes those facts with the reference slide.
`finiteFamily_windowPaid` sums any finite family, and
`c1_c8_windowPaid` specializes this to the exact C1--C8 list.
`littleO_listSum` and `c1_c8_rates_littleO` prove that finitely many
cellwise `o(n)` rates still give a single `o(n)` rate.

This proves the arithmetic aggregation once the audited per-cell ratio/payment
facts are supplied. It does not rederive the algebro-geometric C1--C8 cell
counts.

## Activation and first-match handoff

The source activation remark says a contribution leaving one first-match cell
is reassigned to another, so the total paid slopes do not jump.

- `activationBefore` and `activationAfter` model moving an explicit list of
  assigned slopes from one leaf to the next.
- `activation_flatten_perm`,
  `activation_handoff_preserves_assignedCount`, and
  `activation_handoff_preserves_budgetSum` prove exact conservation.
- `firstMatch_handoff_common_cap` composes conserved printed budgets with the
  existing `firstMatch_le_sum_budgets` theorem on both sides of a threshold.
- `uncovered_activation_falsifier` shows that adding an unassigned slope
  changes the paid count; conservation is load-bearing.

The handoff theorem concerns already-assigned first-match leaves or printed
caps. Identifying a concrete source cell's departing and arriving slopes
remains source-specific data.

## Explicit nonclaims

No theorem here proves C9 routing, the primitive-Q atom, frontier interiority,
Stirling/MVT bounds, or the real asymptotic frontier. The C1--C8 formula audit
and the large exact numerical window checks remain in the source note and
verifier. Windowing is proved conditional on the same single-agreement
payments; those payments themselves are not reproved.
