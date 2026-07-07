# L1 residual excess W3 collapse-edge origin audit

- **Status:** EXPERIMENTAL / FINITE ARITHMETIC ORIGIN AUDIT.
- **Branch:** `scott/l1-w3-collapse-edge-lean-compact`.
- **Data:** `experimental/data/certificates/l1-residual-excess-classifier/w3_collapse_edge_origin_audit_combo012_sizes10_2_3.json`
- **Compact arithmetic data:** `experimental/data/certificates/l1-residual-excess-classifier/w3_collapse_edge_origin_arithmetic_compact_combo012_sizes10_2_3.json`
- **Compact dot data:** `experimental/data/certificates/l1-residual-excess-classifier/w3_collapse_edge_origin_dot_compact_combo012_sizes10_2_3.json`
- **Compact verifier:** `experimental/scripts/verify_l1_w3_collapse_edge_compact_packet.py`
- **Lean metadata checker:** `experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeOriginSummary.lean`
- **Lean dot checker:** `experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeOriginDot.lean`
- **Lean arithmetic checker:** `experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeOriginArithmetic.lean`

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

The companion Lean module `L1Threshold.CollapseEdgeOriginArithmetic` checks the
compact per-edge arithmetic packet:

```lean
L1Threshold.CollapseEdgeOriginArithmetic.edgeOriginArithmeticAllRowsOK
L1Threshold.CollapseEdgeOriginArithmetic.edgeOriginArithmeticRowCount
L1Threshold.CollapseEdgeOriginArithmetic.edgeOriginArithmeticCaseCounts
```

For each compact row, Lean verifies that the stored edge kind is certified by
the modular affine equation:

```text
intercept + shift * slope = 0 mod 137
```

This moves the stored edge-kind arithmetic classification into Lean while
keeping the raw 45k-line graph certificate and W3 reconstruction data out of the
compact packet.

The companion Lean module `L1Threshold.CollapseEdgeOriginDot` checks one layer
below that:

```lean
L1Threshold.CollapseEdgeOriginDot.edgeOriginDotAllRowsOK
L1Threshold.CollapseEdgeOriginDot.edgeOriginDotRowCount
L1Threshold.CollapseEdgeOriginDot.edgeOriginDotCaseCounts
```

For each compact row, Lean verifies:

```text
intercept = <v(a)-v(b), quotient_base> mod 137
slope     = <v(a)-v(b), seed_coords>   mod 137
```

using supplied four-coordinate endpoint evaluations and the stored quotient/seed
vectors.

## Scope

This is still not a Lean-certified symbolic W3 reconstruction.  The compact
Lean dot checker trusts the generated endpoint evaluation vectors, and the
Python finite-field arithmetic audit remains the layer that reconstructs those
endpoint evaluations from the W3 basis.

The audited chain is now:

1. raw W3 basis data and endpoint evaluations;
2. Python origin audit producing compact endpoint/dot rows;
3. Lean dot-product checker for `(intercept,slope)`;
4. Lean modular arithmetic checker for stored edge kinds;
5. Lean finite graph checker for active components and alternate contribution.

It does not prove a symbolic collapse-edge rule, does not cover all W3 generated
families, and does not prove the global L1 theorem.
