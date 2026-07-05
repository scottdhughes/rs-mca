# M1 a327 mu8 rank2 CP-SAT partition scheduler

Status: EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_PLANE_SUPPORT_PAIR_SLACK_INFEASIBLE / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, and not a global `Lambda_mu(C,327) <= 6` theorem.

## Scheduler

The scheduler replaces the greedy largest-block selector with an OR-Tools
CP-SAT model over exact local menus. Sage first builds local ZERO, FREE, and
RATIO options for each carrier plane and quotient point over `GF(17^32)`.
The Python scheduler then chooses:

```text
z[y,rho] in {0,1}
x[y,rho,t,B] in {0,1}
```

subject to one option per quotient point, one selected equality block per
phase, support constraints, pair caps, and interpolation-row cap `63`.

The objective maximizes the weakest label support, then selected incidence,
then pair slack and interpolation slack.

## Result

The bounded CP-SAT front used:

```text
carrier planes solved = 64
ratio options per quotient point = 4
interpolation row cap = 63
```

It did not find a guard-passing schedule:

```text
guard-passing schedules = 0
best min support = 291
best selected incidence total = 2041
required min support = 327
required selected incidence total = 2289
```

Therefore no exact interpolation system was tested in this packet.

## Interpretation

This is a stronger scheduler-level negative than the greedy front, but it is
still local to the first `64` carrier planes, the bounded exact ratio menu, and
the interpolation-row slack guard. It does not cut rank-2 carriers globally.

The next rank-2 step should expand the local grammar or design carrier planes
around support balance before exact interpolation, rather than tuning the
64-variable interpolation rank.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- impossibility of rank-2 `mu_8` carrier constructions.
