# M1 a327 value-class high-overlap beam

Status: TESTED_DESIGNS_NO_PROXY_NULLITY / PARTIAL / EXPERIMENTAL

This note records a high-overlap value-class-first beam search for an `a=327`
interleaved-list witness over

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

The search starts from boundary value-class designs and applies
degree-preserving two-coordinate mutations. Every mutation preserves:

```text
|S_i| = 327 for every i,
max |S_i cap S_j| <= 255.
```

Unlike the previous boundary layer, the beam allows membership sizes

```text
3, 4, 5, 6
```

instead of only 4 and 5. The beam score rewards:

```text
pairs at 255,
pairs in 250..255,
pairs in 245..255,
membership-size diversity,
low-rank-friendly overlap concentration.
```

## Search Layer

The scanner uses eight boundary-search seed designs and runs eight mutation
trajectories from each seed.

```text
seed candidates: 8
trajectories per seed: 8
mutation steps per trajectory: 5000
candidate designs: 64
allowed membership sizes: 3,4,5,6
```

The generated candidates are substantially more overlap-concentrated than the
prior boundary layer:

```text
max pairs at 255: 9
max pairs at or above 250: 9
max pairs at or above 245: 9
```

Some retained candidates also have much smaller reduced systems than the prior
boundary templates. The best proxy-ranked candidate has:

```text
candidate: high_overlap_from_boundary_residual_45_c00_b5_200_t00
compressed variables: 165
remaining equations: 674
membership histogram: {3: 226, 4: 39, 5: 27, 6: 220}
proxy rank: 165
proxy nullity: 0
```

## Result

The Sage audit computes a reduced-rank proxy over `GF(12289)` for all 64
candidate designs and retains the top 20 by proxy/nullity and overlap score.

```text
proxy field: GF(12289)
proxy-positive candidates: 0
retained proxy-ranked candidates: 20
best proxy rank/nullity: 165 / 0
exact GF(17^32) extraction: not triggered
```

This is a local proxy-screen negative result for the named high-overlap beam
layer. It does not prove the corresponding reduced matrices are full rank over
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
`GF(17^32)`, followed by reconstruction of codewords and a received word.

## Reproducibility

```text
python3 experimental/scripts/scan_m1_a327_valueclass_high_overlap_beam.py
python3 experimental/scripts/verify_m1_a327_valueclass_high_overlap_beam.py
sage experimental/scripts/audit_m1_a327_valueclass_high_overlap_beam.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_valueclass_high_overlap_beam.sage --write-json
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
