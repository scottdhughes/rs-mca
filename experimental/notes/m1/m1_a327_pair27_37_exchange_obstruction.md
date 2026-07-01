# M1 a=327 pair {2,7}/{3,7} exchange obstruction

Status: `EXACT_EXTRACTION_NO_A327 / PARTIAL / EXPERIMENTAL`

This packet follows `0639865`, where all tested post-`D2` pair-repair vectors
kept the stable exact geometry:

```text
D2 split retained
capacity >= 327
low six-class dominance
```

but none repaired the weak witness-7 pairs.

## Baseline

Post-`D2` pair-repair checkpoint:

```text
D2 split retained:                       78
capacity-preserving vectors:             78
low-collapse capacity-preserving:        78
best pair B values:                      [1024,514,513,1024,1024]
best capacity upper bound:               366
best failure mode:                       POST_D2_PAIR7_NOT_REPAIRED
```

The remaining weak pairs are:

```text
B({2,7}) = 514
B({3,7}) = 513
target    = 654
```

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is an exact `GF(17^32)` value-class audit. It is not a public certificate
and does not update any board row.

## Method

For the exact low-collapse, capacity-preserving post-`D2` vector pool, the
audit computes the Hall contribution landscape for:

```text
U27 = {2,7}
U37 = {3,7}
```

For a two-witness subset `U`, each coordinate contributes:

```text
2 if the two witnesses share a value class;
1 otherwise.
```

Thus:

```text
B(U) = 512 + number of coordinates where the pair shares a value class.
```

The audit reconstructs and analyzes all `78` exact vectors from `0639865`,
including the local repair-pin variants, and records:

```text
B({2,7}), B({3,7})
credit histograms
credit coordinates
quotient-fiber histograms
exchange-graph feasibility
```

## Result

Best retained exact value-class geometry:

```text
B({2,7}) = 514
B({3,7}) = 513
deficit({2,7}) = 140
deficit({3,7}) = 141
capacity upper bound = 366
```

Credit histograms:

```text
{2,7}: 510 coordinates contribute 1, 2 coordinates contribute 2
{3,7}: 511 coordinates contribute 1, 1 coordinate contributes 2
```

Credit coordinates:

```text
{2,7}: [0, 18]
{3,7}: [18]
```

So within the current exact tuple geometry there are only two coordinates
where witnesses `2` and `7` share a value, and only one coordinate where
witnesses `3` and `7` share a value.

The exchange graph is therefore infeasible:

```text
exchange_graph_feasible = false
```

No targeted repair rows are attempted in this packet, because the value-class
geometry itself does not contain enough pair-credit material to exchange into
a `B>=654` schedule.

## Interpretation

This is a stronger negative than another failed pin attempt.

The previous exact branch showed that local homogeneous pair pins do not repair
the weak pair values. This audit explains why the current codeword tuple
geometry cannot be fixed by rescheduler exchanges:

```text
there are not enough coordinates where {2,7} or {3,7} appears as a value class.
```

The obstruction is not selection among existing classes. The missing pair
classes must be created algebraically by a different exact perturbation.

## Status labels

`PROOF_RECORD / LOWER_BOUND` is reserved for a Sage-audited exact `GF(17^32)`
witness with seven distinct degree-`<256` codewords and one received word.

`EXACT_EXTRACTION_NO_A327` means the named exact diagnostic found no exact
`a>=327` witness and the current exchange graph is infeasible.

`PARTIAL` means other exact perturbation spaces and pair-Hall-guided nullspace
searches remain open.

## Failure labels

- `PAIR27_37_EXCHANGE_INFEASIBLE`: the current value-class geometry lacks
  enough available pair-credit coordinates.
- `PAIR27_37_REPAIR_INCONSISTENT`: a future exact target system with critical
  repair rows has no solution.
- `PAIR27_37_REPAIR_DROPS_CAPACITY`: repair works but capacity drops below
  `327`.
- `PAIR27_37_REPAIR_UNDOES_D2_SPLIT`: repair collapses `D2` again.
- `PAIR27_37_REPAIR_COLLAPSE_RETURNS`: six-class collapse returns.
- `PAIR27_37_REPAIR_LOW_RESCHEDULE`: pair values repair but exact max-min
  remains below `327`.
- `PAIR27_37_EXACT_CANDIDATE`: exact max-min reaches at least `327`.

## Non-claims

- No `a=327` interleaved-list certificate.
- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No public-row update.

## Next target

Do not keep trying to reschedule or exchange within the current exact tuple.
The next search should create pair-credit material directly, for example by a
pair-Hall-guided exact nullspace search that optimizes for many new
`P_2=P_7` and `P_3=P_7` coordinates while preserving the `D2` split and
capacity.
