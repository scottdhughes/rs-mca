# M1 all-line Hankel aperiodic packet audit

Date: 2026-06-27

Source: distilled from PR #127 by AllenGrahamHart.

Status: AUDIT / PROOF PROGRAM / EXPERIMENTAL.  This is not the final M1
polynomial packing theorem.

## Claim being organized

The M1 target is to bound, after quotient-periodic and tangent/contained
classes are charged,

```text
#{ z : exists an aperiodic split locator T with slope z } <= n^B
```

uniformly over all received lines.  The useful contribution of PR #127 is not a
completed bound, but a cleaner finite object for attacking this target.

## Hankel-pencil object

Let `C = RS[F,D,k]`, `|D|=n`, and write

```text
r = n-k,        j+t = r,        a = k+t = n-j.
```

For a line `(f,g):D -> F^2`, let `u = Syn(f)` and `v = Syn(g)`.  A `j`-point
complement `T subset D` has monic locator vector `ell_T`.  The finite slope
`z` is explained on the support `D \ T` exactly when

```text
(H_{t,j}(u) + z H_{t,j}(v)) ell_T = 0.
```

The same support is noncontained exactly when

```text
H_{t,j}(v) ell_T != 0.
```

Thus, after deleting contained/tangent-core locators and charging
whole-fiber quotient-periodic locators, the residual M1 object is a slope image
of a split-locator incidence variety inside this Hankel pencil.

## Useful `t=2` reductions

For `t=2`, define

```text
a_T = H_{2,j}(u) ell_T,
b_T = H_{2,j}(v) ell_T        in F^2.
```

A complement contributes a finite noncontained bad slope iff

```text
b_T != 0,        det[a_T b_T] = 0.
```

The strict-overlap graph is the one-exchange graph on complements.  PR #127
records several useful reductions for this graph:

1. Same-slope one-exchange collisions lie in a full fixed-slope root slice.
2. Such root slices lift to a higher-slack Hankel core and should be charged
   separately from the residual aperiodic slope-image problem.
3. After root-slice peeling, remaining one-exchange edges are controlled by
   quadratic companion slices.
4. Residual triangles are top-packet triangles rather than star triangles.
5. Nontrivial residual top packets lie in a common lifted `t=1` Hankel kernel.

These statements are useful because they turn local collision multiplicity into
packet structure that can plausibly be charged by tangent, quotient, or
higher-slack ledgers.

## What is not proved here

This note does not prove the desired uniform bound

```text
#{ residual aperiodic slopes } <= n^B.
```

It also does not prove a corrected-reserve MCA theorem, protocol soundness
statement, or prize threshold.  The PR #127 verifier is large and incremental;
before merging it wholesale, the finite checks should be split into smaller
auditable scripts keyed to the reductions above.

## Suggested next steps

1. Extract a small verifier just for the `t=2` determinant gate and
   same-slope root-slice lemma.
2. Extract a second verifier for residual top packets and lifted `t=1` kernels.
3. State the first theorem target as a bounded-degree one-exchange graph lemma
   after quotient and root-slice charging.
4. Only after those are separately audited, decide whether any part belongs in
   `experimental/experiments.tex` as a theorem rather than a proof program.
