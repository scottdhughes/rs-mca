# M1 a327 value-class boundary exact audit

Status: ROUTE_CUT_TESTED_CANDIDATES / PARTIAL / EXPERIMENTAL

This note records a small exact `GF(17^32)` hardening pass for the
boundary-stressed value-class-first search over

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

The source boundary-search packet tested 200 value-class incidence designs:

```text
families:
  pair_boundary_45: 70
  quotient_fiber_45: 70
  boundary_residual_45: 60
all designs:
  support sizes = 327 for all seven witnesses
  max pair intersection = 255
  membership sizes = 4 and 5 only
proxy field = GF(12289)
proxy-positive candidates = 0
```

The proxy screen is useful for ranking but is not an exact `GF(17^32)` route
cut. This follow-up exact-audits five named candidates.

## Exact Audit Set

The exact audit covers:

```text
boundary_residual_45_c00_b5_200:
  top retained proxy-ranked candidate; lowest compressed-variable count.

quotient_fiber_45_c00_b5_064:
  best quotient_fiber_45 structural boundary candidate.

pair_boundary_45_c15_b5_064:
  best retained pair_boundary_45 candidate.

boundary_residual_45_c00_b5_096:
  boundary_residual_45 structural variant with different residual split.

pair_boundary_45_c00_b5_064:
  pair_boundary_45 anchor-clique high boundary-pressure variant.
```

For each selected candidate, the Sage audit uses the proxy field only to choose
a square set of pivot rows, then verifies the selected square minor over the
actual field `GF(17^32)`.

## Result

All five selected candidates have exact full-rank minor certificates over
`GF(17^32)`.

```text
exact-audited candidates: 5
exact field: GF(17^32)
certificate type: proxy-selected exact pivot minor
full-rank exact minors: 5
singular exact minors: 0
positive exact nullity: 0
```

The exact reduced nullities for the selected candidates are all zero:

```text
boundary_residual_45_c00_b5_200: exact minor rank 341, nullity 0
quotient_fiber_45_c00_b5_064:    exact minor rank 432, nullity 0
pair_boundary_45_c15_b5_064:     exact minor rank 346, nullity 0
boundary_residual_45_c00_b5_096: exact minor rank 410, nullity 0
pair_boundary_45_c00_b5_064:     exact minor rank 432, nullity 0
```

Thus these named retained/structural boundary candidates cannot yield an
`a=327` interleaved-list witness through their reduced value-class incidence
matrices.

This is not a global `a=327` obstruction. The broader value-class boundary
family and non-boundary constructive families remain open.

## Reproducibility

```text
python3 experimental/scripts/verify_m1_a327_valueclass_boundary_exact_audit.py
sage experimental/scripts/audit_m1_a327_valueclass_boundary_exact_audit.sage
```

The Sage audit also supports:

```text
sage experimental/scripts/audit_m1_a327_valueclass_boundary_exact_audit.sage --write-json
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
