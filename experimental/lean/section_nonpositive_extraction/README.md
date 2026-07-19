# Section-nonpositive degree-gate formalization

This standalone Lean 4.14 package formalizes the arithmetic engine of the
section-nonpositive rational-host reach map.  The canonical compiler source was
produced by PR #721 at `aa66634e` and integrated at `c23dcaa0`.  Its
counterexample consumer was produced by PR #730 at `539d8f0d` and integrated,
together with this package's former finite skeleton, at `9262f63c`.

## Theorem map

| Source statement | Lean declaration | Status |
| --- | --- | --- |
| Section-nonpositive predicate `a^2 <= n(k-1)` | `SectionNonpositive` | DEFINITION |
| Counterexample degree ceiling | `ceiling_violated` | PROVED arithmetic implication |
| Counterexample uniform denominator family | `family_obstruction` | PROVED arithmetic implication |
| Three counterexample parameter rows | `rows_are_valid` | PROVED finite regression |
| Compiler section 4.1, universal degree gate | `degree_gate` | PROVED in the exact printed regime |
| Former degree-gate check through `n=40` | `gateHoldsUpTo`, `degree_gate_n_le_40` | PROVED finite regression |
| Counterexample regime floor | `rowExistsAt`, `regime_floor_is_8` | PROVED finite regression |
| Polynomial/interpolation semantics and rational-host extraction | none | NOT FORMALIZED IN LEAN |
| Counterexample Theorems 1--3 beyond their arithmetic engine | none | NOT FORMALIZED IN LEAN |

## Statement boundary

`degree_gate` keeps the source's hypotheses `1 <= k < n` and
`k+1 <= a <= n`.  From `a^2 <= n(k-1)` it proves

```text
2a-k <= n-1.
```

The proof establishes the strict precursor `2a<n+k` by comparing squares and
using the positive gap

```text
4n(k-1) < (n+k)^2.
```

The source assumptions `k+1 <= a` and `a <= n` are algebraically redundant for
the square comparison, but remain visible so this declaration is an exact
compiler-regime wrapper.  No unrestricted natural-subtraction identity is used:
`1<=k` and `k<n` make the predecessor expressions exact, while `k+1<=a`
guarantees that the printed `2a-k` is nontruncated in the intended host range.

## Scope

This package proves only natural-number degree inequalities.  It does not
construct or extract a rational-host presentation, formalize polynomial or
interpolation semantics, prove the counterexample's presentation iff, build a
non-host family, count generic failures, instantiate a finite field/domain or
Reed--Solomon code, search denominators, build a first-match/ray compiler, pay a
profile, establish lower reserve, close a row, prove an MCA threshold, or make
a Proximity Prize claim.

Build with the pinned toolchain:

```text
lake build
```
