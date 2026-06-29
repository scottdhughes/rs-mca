# M1 a327 RIM obstruction summary

Status: AUDIT / COMPUTATIONAL_CERTIFICATE / ROUTE_CUT / PARTIAL /
EXPERIMENTAL

This note summarizes the focused reduced-intersection-matrix audit packet for
the M1 interleaved-list workstream over

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains the PR #133 record:

```text
Lambda_mu(C,326) >= 7.
```

This packet does not improve that row. It is strictly an `INTERLEAVED_LIST`
audit over denominator `17^32`, not an MCA `N_bad` row, and it does not claim
protocol soundness, ordinary list decoding beyond the stated predicate, exact
`Lambda_mu`, exact `delta*_C`, an `a=327` certificate, or a global upper bound
at `a=327`.

## Scope

The included files consolidate the mature RIM obstruction and pivot-certificate
lane:

```text
nonquotient pairwise overlap rank gate
base quotient-residual RIM pivot certificates
34/34 RIM support-pattern pivot replay
pivot-pattern mining over three source classes
support-overlap rank-free rule audit
generic-pairwise rank-free rule audit
quotient-residual rank-free rule audit
```

The route-cut meaning is local: each exact full-rank reduced matrix in this
packet cannot produce an `a=327` interleaved-list witness through that tested
support/RIM model. The packet does not prove
`Lambda_mu(C,327) <= 6` globally.

## Rank Gate

The nonquotient support design passes the basic packing test:

```text
7 supports
support size = 327
max pair intersection = 254
```

Its reduced pairwise-overlap rank gate is full rank over `GF(17^32)`:

```text
matrix shape: 2882 x 382
rank:         382
nullity:       0
```

Thus that support design cannot produce a non-diagonal interpolation solution.

## Pivot Coverage

The pivot replay packet certifies all prior exact full-rank `a=327` reduced
matrices in this local lane:

```text
source matrices:      34
pivot certified:      34
certificate type:     Sage-replayed RREF pivot minor over GF(17^32)
```

The 34 matrices split as:

```text
support_overlap_rref_pivot:    20
generic_pairwise_rref_pivot:    6
quotient_residual_rref_pivot:   8
```

The aggregate pivot row profile is:

```text
support_overlap_row:             1901
balanced_or_generic_pairwise_row: 1226
quotient_full_fiber_row:           383
residual_or_partial_fiber_row:      37
```

This is a replayable computational certificate. It is not yet a deterministic
combinatorial full-rank theorem.

## Rank-Free Rule Audits

The support-overlap class remains RREF-derived only:

```text
matrices:                    20
rank-free metadata attempts: 160
rank-free successes:           0
```

The generic-pairwise class also remains RREF-derived only:

```text
matrices:                   6
rank-free attempts:        48
rank-free successes:        0
```

The quotient-residual class has a narrow RREF-mimic partial success:

```text
matrices:                       8
rank-free attempts:            88
total successes:                2
deterministic-rule successes:   0
RREF-mimic successes:           2
large-matrix successes:         0
```

The two successes are both from the `rref_profile_type_pair_quota_mimic` rule
on small 6-column quotient-residual matrices. The two 192-column anchor-relaxed
matrices remain RREF-derived.

## Conclusion

This packet gives a focused local obstruction audit:

```text
AUDIT / COMPUTATIONAL_CERTIFICATE / ROUTE_CUT / PARTIAL
```

It records that the tested `a=327` support/RIM candidates are blocked by
certified full-rank reduced matrices, and that the tested rank-free metadata
rules do not yet yield a deterministic pivot theorem.

## Not Claimed

```text
MCA N_bad
protocol soundness
ordinary list decoding beyond the stated interleaved-list predicate
a=327 interleaved-list certificate
global Lambda_mu(C,327) <= 6
global RIM full-rank theorem
deterministic combinatorial pivot schedule
exact Lambda_mu
exact delta*_C
improvement over PR #133
```
