# L1 residual excess W3 collapse-edge origin audit

- **Status:** EXPERIMENTAL / FINITE ARITHMETIC ORIGIN AUDIT.
- **Branch:** `scott/l1-w3-collapse-edge-lean-compact`.
- **Data:** `experimental/data/certificates/l1-residual-excess-classifier/w3_collapse_edge_origin_audit_combo012_sizes10_2_3.json`
- **Compact verifier:** `experimental/scripts/verify_l1_w3_collapse_edge_compact_packet.py`
- **Lean metadata checker:** `experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeOriginSummary.lean`

## Purpose

The Lean checker certifies only the finite graph implication.  This audit
bridges one layer down by checking that every stored edge rule in the finite
certificate comes from the affine seed-shift equality equation over `F_137`.

For points `a,b` in one coset and quotient-line member `q + t s`, the edge
condition is:

```text
<v(a)-v(b), q> + t <v(a)-v(b), s> = 0  in F_137.
```

The audit recomputes:

```text
intercept = <v(a)-v(b), q>
slope     = <v(a)-v(b), s>
```

and classifies each edge as:

```text
always    if slope = 0 and intercept = 0
never     if slope = 0 and intercept != 0
at_shift  if slope != 0, with shift = -intercept / slope
```

## Result

The compact summary records:

```text
case_count         = 6
edge_rules_audited = 6528
mismatch_count     = 0
status             = L1_W3_COLLAPSE_EDGE_ORIGIN_CERTIFIED
```

So the stored finite edge rules agree with the reconstructed `F_137` affine
classification for the two quotient-line cases and three dangerous shifts in
each line.  The raw 45k-line edge-rule JSON is not part of this compact PR; it
is identified by SHA-256 in the summary:

```text
1aab9da15bf074232122898bd9958fe2f2240eacdbc138af5638851be99a889d
```

The companion Lean module `L1Threshold.CollapseEdgeOriginSummary` checks the
compact metadata/count statement:

```lean
L1Threshold.CollapseEdgeOriginSummary.originSummaryAllCasesOK
L1Threshold.CollapseEdgeOriginSummary.originSummaryEdgeRulesAudited
L1Threshold.CollapseEdgeOriginSummary.originSummaryTwoFamilies
```

These Lean theorems certify the six-case/two-family shape, the `6528` audited
edge-rule count, zero mismatches, and the repeated eight-coset rule-count
pattern present in the compact summary.

## Scope

This is still not a Lean-certified per-edge `GF(137)` reconstruction.  The
per-edge arithmetic audit is Python finite-field arithmetic that sits between:

1. the raw generated edge-rule certificate; and
2. the Lean finite graph checker.

It does not prove a symbolic collapse-edge rule, does not cover all W3 generated
families, and does not prove the global L1 theorem.
