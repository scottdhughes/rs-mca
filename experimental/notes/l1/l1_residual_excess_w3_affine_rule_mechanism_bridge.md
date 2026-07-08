# L1 residual excess W3 affine-rule mechanism bridge

- **Status:** EXPERIMENTAL / FINITE BRIDGE CERTIFICATE.
- **Lean module:** `experimental/lean/l1_threshold_ledger/L1Threshold/CollapseEdgeAffineRuleBridge.lean`

## Purpose

This packet names the finite proof chain that is now available after the W3
edge-origin, graph-mechanism, and structural-wrapper packets were integrated:

```text
affine dot rows
  -> modular edge-rule arithmetic
  -> stored atShift edge rules with zero mismatches
  -> rule-active matching/triangle mechanism
  -> alternate contribution <= 1 for the six dangerous cases
```

The bridge is proof-facing glue. It does not add a new symbolic W3 theorem and
does not reconstruct the W3 basis polynomials.

## Lean surface

The module exposes four layer checks:

- `affineOriginRowsCertified`:
  compact dot rows and modular arithmetic rows are Lean-checked, with `6528`
  rows in each certificate.
- `storedRulePacketCertified`:
  the origin summary has zero mismatches, audits `6528` edge rules, and has the
  two-family six-shift shape.
- `ruleMechanismCertified`:
  active edges recomputed from stored `always / never / atShift` rules force
  matching-only non-survivor alternate cosets and the unique coset-37 triangle.
- `dangerousContributionCertified`:
  the finite structural wrapper gives alternate contribution `<= 1`, in fact
  exactly `[1,1,1,1,1,1]`, across the six dangerous cases.

The combined theorem is:

- `affineRulesToAlternateCollapseBridge`.

## Scope

This is a finite bridge certificate over the stored W3 packet. Its hypotheses
are the integrated compact certificates, not a symbolic description of all W3
blocks. It supports the next mathematical target:

> derive, without six-case enumeration, why the two quotient-family triples
> force the same stored `atShift` rule pattern.

It does not claim a global L1 theorem or any MCA/protocol consequence.
