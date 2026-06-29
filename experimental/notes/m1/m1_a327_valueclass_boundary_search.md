# M1 a327 value-class boundary search

Status: TESTED_DESIGNS_NO_PROXY_NULLITY / PARTIAL / EXPERIMENTAL

This note records a boundary-stressed value-class-first constructive search for
an `a=327` interleaved-list witness over

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

The search chooses received-word value classes first. At each coordinate
`h in H`, a membership set

```text
E_h subset {1,...,7}
```

records which witnesses should receive credit at that coordinate. The induced
support sets are

```text
S_i = {h : i in E_h}.
```

Every generated design has:

```text
|S_i| = 327 for every i,
max |S_i cap S_j| <= 255,
271 coordinates of membership size 4,
241 coordinates of membership size 5.
```

Unlike the first balanced value-class layer, this search deliberately pushes
selected pair intersections to the RS equality cap `255`.

## Candidate Families

The scanner generates 200 deterministic boundary-stressed incidence designs.

```text
pair_boundary_45:
  70 designs. A target witness triple shares 255 coordinates, with boundary
  positions spread through H.

quotient_fiber_45:
  70 designs. A target triple shares 7 full x -> x^32 quotient fibers plus
  31 residual coordinates.

boundary_residual_45:
  60 designs. A target triple shares 6 full quotient fibers plus 63 residual
  coordinates spread across additional fibers.
```

For every tested design:

```text
support sizes: all 327
max pair intersection: 255
pairs at 255: 3
membership sizes: 4 and 5 only
```

## Result

The Sage audit computes a reduced-rank proxy over `GF(12289)` for all 200
candidate designs and retains the top 20 by proxy/nullity and boundary-pressure
score.

```text
candidate designs: 200
families:
  pair_boundary_45: 70
  quotient_fiber_45: 70
  boundary_residual_45: 60
proxy field: GF(12289)
proxy-positive candidates: 0
retained proxy-ranked candidates: 20
best proxy-ranked candidate: boundary_residual_45_c00_b5_200
best compressed variables: 341
best remaining equations: 1218
best proxy rank: 341
best proxy nullity: 0
exact GF(17^32) extraction: not triggered
```

This is a local proxy-screen negative result for the named boundary-stressed
incidence layer. It does not prove the corresponding reduced matrices are full
rank over `GF(17^32)`, and it does not prove any global obstruction at
`a=327`.

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
`GF(17^32)`, followed by reconstruction of codewords and a received word.

## Reproducibility

```text
python3 experimental/scripts/scan_m1_a327_valueclass_boundary_search.py
python3 experimental/scripts/verify_m1_a327_valueclass_boundary_search.py
sage experimental/scripts/audit_m1_a327_valueclass_boundary_search.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_valueclass_boundary_search.sage --write-json
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
