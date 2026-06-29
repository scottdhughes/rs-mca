# M1 a327 value-class high-overlap exact audit

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records a small exact `GF(17^32)` hardening pass for the
high-overlap value-class-first beam over

```text
C = RS[F_17^32,H,256],    |H| = 512.
```

The current board-facing interleaved-list packet remains:

```text
Lambda_mu(C,326) >= 7.
```

This checkpoint does not improve that row. It is strictly an
`INTERLEAVED_LIST` audit packet, not an MCA `N_bad` row, and it does not claim
protocol soundness, ordinary list decoding beyond the stated predicate, exact
`Lambda_mu`, exact `delta*_C`, an `a=327` certificate, or a global upper bound
at `a=327`.

## Source Packet

The source high-overlap beam tested 64 value-class incidence designs:

```text
seed boundary candidates: 8
mutation trajectories per seed: 8
membership sizes allowed: 3,4,5,6
support sizes = 327 for all seven witnesses
pair cap <= 255
max pairs at 255: 9
max pairs at or above 250: 9
proxy field = GF(12289)
proxy-positive candidates = 0
```

The proxy screen is useful for ranking but is not an exact `GF(17^32)` route
cut. This follow-up exact-audits six retained or structurally notable
candidates.

## Exact Audit Set

The exact audit covers:

```text
high_overlap_from_boundary_residual_45_c00_b5_200_t00:
  best proxy-ranked candidate; lowest compressed-variable count.

high_overlap_from_boundary_residual_45_c00_b5_200_t04:
  second low-variable retained candidate with distinct histogram.

high_overlap_from_boundary_residual_45_c00_b5_096_t04:
  low-variable residual-split variant.

high_overlap_from_quotient_fiber_45_c15_b5_064_t07:
  best quotient-fiber high-overlap retained candidate with nine capped pairs.

high_overlap_from_quotient_fiber_45_c15_b5_064_t03:
  quotient-fiber high-overlap candidate with structurally novel histogram.

high_overlap_from_pair_boundary_45_c15_b5_064_t00:
  best pair-boundary high-overlap retained candidate with nine capped pairs.
```

For each selected candidate, the Sage audit uses the proxy field only to choose
a square set of pivot rows, then verifies the selected square minor over the
actual field `GF(17^32)`.

## Result

All six selected candidates have exact full-rank minor certificates over
`GF(17^32)`.

```text
exact-audited candidates: 6
exact field: GF(17^32)
certificate type: proxy-selected exact pivot minor
full-rank exact minors: 6
singular exact minors: 0
positive exact nullity: 0
```

The exact reduced nullities for the selected candidates are all zero:

```text
high_overlap_from_boundary_residual_45_c00_b5_200_t00: exact minor rank 165, nullity 0
high_overlap_from_boundary_residual_45_c00_b5_200_t04: exact minor rank 165, nullity 0
high_overlap_from_boundary_residual_45_c00_b5_096_t04: exact minor rank 168, nullity 0
high_overlap_from_quotient_fiber_45_c15_b5_064_t07:    exact minor rank 284, nullity 0
high_overlap_from_quotient_fiber_45_c15_b5_064_t03:    exact minor rank 285, nullity 0
high_overlap_from_pair_boundary_45_c15_b5_064_t00:     exact minor rank 296, nullity 0
```

Thus these named retained/structural high-overlap value-class candidates cannot
yield an `a=327` interleaved-list witness through their reduced value-class
incidence matrices.

This is not a global `a=327` obstruction. The broader high-overlap
value-class design space and non-value-class constructive families remain open.

## Reproducibility

```text
python3 experimental/scripts/verify_m1_a327_valueclass_high_overlap_exact_audit.py
sage experimental/scripts/audit_m1_a327_valueclass_high_overlap_exact_audit.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_valueclass_high_overlap_exact_audit.sage --write-json
```

to regenerate the exact audit JSON.

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
