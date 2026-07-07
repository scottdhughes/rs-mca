# L1 residual excess W3 collapse-edge Lean checker

- **Status:** EXPERIMENTAL / FINITE LEAN CERTIFICATE.
- **Branch:** `scott/l1-w3-collapse-edge-lean-compact`.
- **Lean file:** `experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeCertificate.lean`
- **Compact origin audit:** `experimental/data/certificates/l1-residual-excess-classifier/w3_collapse_edge_origin_audit_combo012_sizes10_2_3.json`

## Certified finite statement

The Lean checker imports the stored finite graph rules for the six dangerous
`(missing,stray)=(2,1)` cases.  For each case it verifies:

1. each edge rule is activated at the certified shift;
2. the stored active-edge list matches the activated rules as a finite edge set;
3. the stored connected components form a partition of the points;
4. every listed component is connected using active edges;
5. no active edge crosses between listed components;
6. the head antecedent is `(missing,stray)=(2,1)`;
7. the only alternate component of size at least three is the coset-37 triple
   `[17,36,130]`;
8. the alternate contribution is at most `1`.

The main theorem is:

```lean
L1Threshold.CollapseEdgeCertificate.collapseEdgeAllCasesOk
```

The contribution-only theorem is:

```lean
L1Threshold.CollapseEdgeCertificate.collapseEdgeAllCaseContributionsLeOne
```

The pattern-exposing theorems are:

```lean
L1Threshold.CollapseEdgeCertificate.collapseEdgeShiftsAreTwoTriples
L1Threshold.CollapseEdgeCertificate.collapseEdgeAllActualSurvivorsSame
L1Threshold.CollapseEdgeCertificate.collapseEdgeAllAlternateContributionsExact
```

They record that the six certified shifts are
`[67,103,111,17,20,121]`, that every case has the same unique alternate
survivor `cosetW = 37`, component `[17,36,130]`, and that every certified
alternate contribution is exactly `1`.

These print with no axioms in the local `lake build` audit.

The one-line compact-packet aggregate theorem is:

```lean
L1Threshold.CollapseEdgeCompactPacket.compactPacketOK
```

It combines the finite graph checker, the compact origin-summary checker, the
compact dot-product origin checker, and the compact modular edge-origin
arithmetic checker.

## Scope

This Lean certificate does not reconstruct the underlying `GF(137)` arithmetic.
It only certifies the finite graph implication after the raw edge rules have
been generated.  A companion Lean module,
`L1Threshold.CollapseEdgeOriginSummary`, checks the compact origin-audit
metadata/count summary, but it also does not replay the omitted per-edge affine
arithmetic.  A second companion module,
`L1Threshold.CollapseEdgeOriginArithmetic`, checks the compact per-edge modular
classification rows `(intercept,slope)` over modulus `137`.  A third companion
module, `L1Threshold.CollapseEdgeOriginDot`, checks that those intercept/slope
values are dot products of supplied endpoint evaluations against the quotient
and seed vectors.
`L1Threshold.CollapseEdgeCompactPacket` combines these finite checks into a
single reviewer-facing gate.  The compact packet records the raw source hash in
the origin-audit summary, but does not include the 45k-line raw edge-rule JSON.

This is not a symbolic W3 lemma, not a global L1 theorem, and not MCA/protocol
evidence.
