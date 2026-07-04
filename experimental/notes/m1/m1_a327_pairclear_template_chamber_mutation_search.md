# M1 a=327 pair-clear template chamber mutation search

Status:

CANDIDATE / TCHAMBER_NINE_ROW_STABLE_FRONT / PARTIAL / EXPERIMENTAL

This packet follows `12a54d9` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous checkpoint exhaustively scanned the base `14 x 6` projective
direction front and found:

```text
projective directions tested = 1508598
pair-clear directions = 360360
rank-slack chambers = 0
support-reduced extensions = 0
best failure = CHAMBER_NINE_ROW_STABLE
```

This branch moves one level upstream. It varies the template before rerunning
the same projective chamber score. The bounded front used:

```text
mutations generated = 24
candidate systems constructed = 72
structural-pass candidates = 72
structural-pass candidates analyzed = 8
basis profiles scored = 4
```

Each scored basis profile was scanned over all projective directions in
`GF(17)^6`.

## Result

The four full profile scans tested:

```text
directions tested = 6034392
pair-clear directions = 1441440
distinct pair-clear chambers = 218
```

The scored profiles were:

```text
ninerow_base_w1_c3_d1 / fiber_round_robin / basisaware_1_4_7_8_9_10
ninerow_w1_c0_d1      / fiber_round_robin / basisaware_1_4_7_8_9_10
ninerow_w1_c0_d13     / fiber_round_robin / basisaware_1_4_7_8_9_10
ninerow_w1_c0_d14     / fiber_round_robin / basisaware_1_4_7_8_9_10
```

Aggregate outcome:

```text
nine-row-or-better profiles = 1
direct support-reduced profiles = 0
rank-slack profiles = 0
support-reduced extension profiles = 0
failure counts:
  TCHAMBER_NINE_ROW_STABLE = 1
  TCHAMBER_LOWER_SUPPORT_ONLY = 3
```

The best profile remains the base chamber:

```text
template = ninerow_base_w1_c3_d1
basis = basisaware_1_4_7_8_9_10
zero row classes = [13,16,17,18,19]
zero row count = 5
inactive rank = 5
inactive kernel nullity = 1
active row classes = [0,2,3,5,6,11,12,14,15]
```

The three tested mutations did not preserve the nine-row chamber. They had
pair-clear directions, but only lower-support chambers and no rank slack.

## Interpretation

This is not a broad mutation theorem. It is a bounded front result:

- the base chamber remains locally best among the scored profiles;
- first-coordinate witness-1 mutations tested here do not create support
  reduction or inactive-rank slack;
- the current obstruction is still a nine-row, rank-5 inactive chamber.

The next search should not rescan these same four profiles. It should diversify
the template mutation family and basis selector enough to change the coefficient
arrangement more substantially.

## Non-claims

This packet does not claim:

- an `a=327` certificate
- Sage `GF(17^32)` exact lift
- MCA `N_bad`
- protocol soundness
- ordinary list decoding beyond the stated interleaved-list predicate
- global `Lambda_mu(C,327) <= 6`
- exact `Lambda_mu`
- exact `delta*_C`
- global obstruction outside the tested template-chamber mutation front

## Next Target

Move to a broader, more deliberately diverse mutation selector:

```text
m1-a327-pairclear-diverse-chamber-front
```

The selector should force coverage across:

```text
witness index
coordinate index
shear-pair mutations
basis class sets
assignment strategies
```

and then run the chamber score only on profiles whose cheap prefix/proxy scan
suggests either:

```text
>=5 zero rows with inactive rank <=4
```

or:

```text
>=6 zero rows
```

Use Python first. Macaulay2/Singular should remain reserved for small module
certificates after a promising chamber appears. Sage should still wait until a
pair-clear direction-kernel proxy target exists.
