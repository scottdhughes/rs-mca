# Section-nonpositive degree-gate formalization

## Claim

In the canonical compiler regime `1 <= k < n` and `k+1 <= a <= n`, the gate

```text
a^2 <= n(k-1)
```

implies the exact integer degree room `2a-k <= n-1`.

## Status

PROVED.

## Source audit and repair boundary

The source is section 4.1 of
`experimental/notes/thresholds/canonical_reduced_rational_host_compiler.md`,
produced by PR #721 at `aa66634e` and integrated at `c23dcaa0`.  The source
derives `2a<n+k` by a discriminant comparison and then uses integrality.

The consumer is Theorem 3 of
`experimental/notes/thresholds/section_nonpositive_extraction_counterexample.md`,
produced by PR #730 at `539d8f0d` and integrated at `9262f63c`.  Its Lean
package previously supplied only `degree_gate_n_le_40`; the note separately
exhausted the claim through `n=64`.  Neither finite check proved the universal
statement in Lean.

The new theorem keeps all printed regime hypotheses.  The assumptions
`k+1<=a` and `a<=n` are logically unused by the square comparison, but are not
silently removed from the source wrapper.  The proof avoids false unrestricted
Nat subtraction: `1<=k` controls `k-1`, `k<n` controls `n-1`, and `k+1<=a`
guarantees that the printed `2a-k` is nontruncated in the source regime.

## Lean correspondence

`SectionNonpositiveExtraction.degree_gate` is in
`experimental/lean/section_nonpositive_extraction/SectionNonpositiveExtraction.lean`.
The package README is the complete source-statement to Lean-name status map.
The existing Boolean census and theorem retain their exact types as a finite
regression.

## Proof outline

Scaling section-nonpositivity gives `4a^2 <= 4n(k-1)`.  Writing
`k=p+1` and `n=k+q+1` reduces the exact gap

```text
4n(k-1) < (n+k)^2
```

to normalized natural-number arithmetic.  If `n+k <= 2a`, monotonicity of
multiplication would reverse that strict gap.  Thus `2a<n+k`, and integrality
gives the printed degree room.  The proof uses only core Lean tactics and APIs.

## Validation

From `experimental/lean/section_nonpositive_extraction`:

```bash
lake clean
lake build
```

From the repository root:

```bash
python3 experimental/scripts/verify_section_nonpositive_degree_gate.py --check
python3 experimental/scripts/verify_section_nonpositive_degree_gate.py --tamper-selftest --check
```

## Scope and nonclaims

This formalizes only the universal arithmetic degree gate.  It does not prove
rational-host extraction or presentation, polynomial/interpolation semantics,
the counterexample's Theorem-1 iff, a non-host family or generic-failure count,
field/domain/RS instantiation, denominator enumeration, first-match or ray
compilation, profile payment, lower reserve, row closure, an MCA threshold, or
a Proximity Prize claim.
