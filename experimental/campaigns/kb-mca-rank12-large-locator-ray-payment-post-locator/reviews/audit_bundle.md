# Independent mathematics audit

## Verdict

**GREEN for the stated large-locator proper-drop payment.**

The audit explicitly rejects a stronger but invalid intermediate accounting:
one may not cap the rank-one part by the capacity at the minimum locator
floor.  If the actual core is larger, the effective residual dimension is
smaller and the rank-one capacity can increase.  The final proof instead uses
the proved all-dimension maximum `4,070,947`.

## Load-bearing checks

1. **Source-bound partition.**  The partition by the already-frozen exact
   support meeting or avoiding the actual full common core is disjoint in
   original slope units.
2. **Kernel promotion.**  A support meeting the core gives one zero of its
   pair-difference polynomial.  Since whole-family core coordinates have been
   exhausted, the evaluation kernel in the two-dimensional direction code is
   exactly the one-dimensional leaf direction.
3. **Six-support synchronization.**  A second divided difference is supported
   in three omission sets.  After quotienting by the leaf direction, the
   difference of two such objects is supported in six omission sets and lies
   in the leaf direction.  The strict inequality `6r<R+1` forces equality by
   Reed--Solomon minimum distance.
4. **Universal coordinates.**  The ray payment retains an arbitrary universal
   set `U`.  It uses only `u<=K-1`, since `U` lies in the zero set of the
   nonzero ray direction `Q`; no support is assumed to contain every universal
   coordinate.
5. **At least two line classes.**  All `Q`-zero coordinates together have
   fewer than `m` copies.  Universal coordinates plus one graph clone class
   are simultaneously explained by a global codeword pair, so an MCA-bad
   exact support must contain at least two nonuniversal parameter-line
   classes.
6. **Large clone.**  The nonuniversal support universe has size `N=M+r<2K`, so
   at most one graph clone has weight at least `K`.  Complete-agreement
   outside-coordinate injection bounds that clone by `r+1` points.
7. **Residual cross-pairs.**  After removing the large graph, every class has
   weight at most `K-1`.  The exact heterogeneous-pair floor is `M-1` below
   `K`, and `(K-1)(M-K+1)` above it.  A heterogeneous coordinate pair lies on
   at most one point of the affine parameter plane.
8. **Optimization.**  The two rational pieces have nonnegative second
   derivative, so the floor maximum is attained at one of four included
   endpoints.  The primary and independent implementations agree on every
   deployed cell.
9. **Final composition.**  `4,070,947+796,620=4,867,567<5,170,912`, leaving
   exact slack `303,345`.

## Scope

The proof pays only proper drops for `K>=858,619`.  It does not classify the
adjacent `K=858,618` near-minimum-weight case, pay affine error rank twelve,
or move an active-v4 ledger atom.

# Certificate and custody review

## Verdict

**GREEN.**

- Exact parent: `ed556ccb7527e1c54e58b8d151ccefd8539000ac`.
- Parent canonical payload:
  `edef5ffa88a495a0a659a62a3ce891372b59458350ef4eab5b35f75ed5f37baa`.
- The primary verifier reconstructs the parent capacity strip, all `189,958`
  ambient cells, four ray endpoints per cell, finite controls, and all stated
  selected cells.
- The independent audit recomputes rank-one capacities by direct `Fraction`
  maximization rather than the primary endpoint shortcut.
- Eight hostile semantic mutations are rejected.
- Claims and nonclaims are frozen in `result.json` and mirrored in the
  manifest.

No mutable network response, floating-point comparison, external executable,
or literature theorem is load-bearing.

# Targeted literature sweep

The closest current primary sources reviewed were:

- Sunghyeon Jo, *Reed--Solomon Mutual Correlated Agreement Beyond the
  Johnson Radius*, IACR ePrint 2026/1432.
- Przemek Chojecki, *Shortening Bounds for Reed--Solomon MCA*, IACR ePrint
  2026/1463.
- Ulrich Haboeck, *A note on mutual correlated agreement for Reed--Solomon
  codes*, IACR ePrint 2025/2110.
- Sunghyeon Jo, *Interleaving Stability for Mutual Correlated Agreement and
  Curve Decodability*, IACR ePrint 2026/891.

These works provide context for deterministic MCA, shortening, and affine-line
agreement, but none states the source-bound six-omission synchronization or
the universal-core-aware affine-ray bound proved here.  No external theorem is
load-bearing; the proof uses only elementary Reed--Solomon minimum distance,
affine-line intersection, and exact convex optimization.

# Wolfram exact replay

Wolfram Language independently reproduced the selected cells:

```text
K=858619: incident=2510746, k=52277, core=806342,
ray endpoints={609591,796619,796620,174773}, ray=796620.

K=858625: incident=2510755, k=52276, core=806349,
ray endpoints={609559,796606,796607,174766}.

K=900000: incident=2567239, k=49453, core=850547,
ray=720584.

K=991011: incident=2683421, k=43644, core=947367,
ray=563554.

K=1048576: incident=2751700, k=40231, core=1008345,
ray endpoints={33737,524288,524289,9}.
```

It also returned the exact second derivatives

\[
\frac{r(r+1)}{x^3},
\qquad
\frac{(K+r-2)(K+r-1)}{(K-1)y^3},
\]

which certify convexity on the two optimization intervals.  The load-bearing
all-cell scan remains the two independent integer Python implementations.
