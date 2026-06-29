# M1 a327 value-class-first witness search

Status: TESTED_DESIGNS_NO_PROXY_NULLITY / PARTIAL / EXPERIMENTAL

This note records the first value-class-first constructive search for an
`a=327` interleaved-list witness over

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` search packet, not an MCA `N_bad` row, and it does not claim
protocol soundness, ordinary list decoding beyond the stated predicate, exact
`Lambda_mu`, exact `delta*_C`, an `a=327` certificate, or a global upper bound
at `a=327`.

## Model

Instead of guessing seven codewords first, this search chooses received-word
value classes first. At each coordinate `h in H`, a membership set

```text
E_h subset {1,...,7}
```

records which witnesses should receive credit at that coordinate. The induced
support sets are

```text
S_i = {h : i in E_h}.
```

The first layer uses the exact total incidence required by `a=327`:

```text
7 * 327 = 2289
```

distributed as:

```text
241 coordinates of membership size 5
271 coordinates of membership size 4
```

so the average coordinate multiplicity is `2289 / 512`.

## Result

This checkpoint tests the first deterministic balanced 4/5 incidence layer.

```text
candidate designs: 14
families:
  balanced_45_regular: 6
  quotient_fiber_balanced: 4
  anti_anchor_balanced: 4
support sizes: all 327
max pair intersections: 193..198
proxy field: GF(12289)
proxy nullities: all 0
best proxy-ranked candidate: quotient_fiber_balanced_03
best compressed variables: 374
best remaining equations: 1350
exact GF(17^32) extraction: not triggered
```

This is a local proxy-screen negative result for the named incidence layer. It
does not prove the corresponding reduced matrices are full rank over
`GF(17^32)`, and it does not prove any global obstruction at `a=327`.

## Proxy Rank Gate

For each incidence design, the Sage audit anchors `P_1=0` and writes

```text
D_i = P_i - P_1,  i=2,...,7.
```

Pairwise value-class requirements become the reduced interpolation system:

```text
D_i(h)=0          when 1 and i both lie in E_h,
D_i(h)=D_j(h)    when i and j both lie in E_h.
```

The audit compresses the anchor-zero constraints by factoring the corresponding
locator roots out of each `D_i`, then computes a reduced-rank proxy over
`GF(12289)`, whose multiplicative group contains a subgroup of order `512`.

This proxy rank gate is a search screen, not a proof over `GF(17^32)`. If
positive proxy nullity appears, the next step is exact rank/extraction over
`GF(17^32)`, followed by reconstruction of codewords and a received word. If
all tested designs have proxy nullity zero, the result is only a local
proxy-screen negative result for this first incidence layer.

## Candidate Families

The scanner generates deterministic value-class incidence designs:

```text
balanced_45_regular:
  balanced 4/5-uniform incidence designs.

quotient_fiber_balanced:
  4/5 memberships distributed evenly inside quotient-fiber-sized blocks.

anti_anchor_balanced:
  balanced designs that reduce reliance on anchor-containing classes.
```

All candidates satisfy:

```text
|S_i| = 327 for every witness i,
max |S_i cap S_j| <= 255.
```

## Reproducibility

```text
python3 experimental/scripts/scan_m1_a327_valueclass_first_witness_search.py
python3 experimental/scripts/verify_m1_a327_valueclass_first_witness_search.py
sage experimental/scripts/audit_m1_a327_valueclass_first_witness_search.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_valueclass_first_witness_search.sage --write-json
```

to regenerate the proxy rank-gate JSON. Exact `GF(17^32)` extraction is only
triggered by a positive proxy-nullity candidate.

## Not Claimed

```text
MCA N_bad
protocol soundness
ordinary list decoding beyond the stated interleaved-list predicate
a=327 interleaved-list certificate
global Lambda_mu(C,327) <= 6
exact Lambda_mu
exact delta*_C
improvement over PR #133
```
