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

Both print with no axioms in the local `lake build` audit.

## Scope

This Lean certificate does not reconstruct the underlying `GF(137)` arithmetic.
It only certifies the finite graph implication after the raw edge rules have
been generated.  The compact PR records the raw source hash in the origin-audit
summary, but does not include the 45k-line raw edge-rule JSON.

This is not a symbolic W3 lemma, not a global L1 theorem, and not MCA/protocol
evidence.
