# M1 a327 mu8 rank2 carrier generator

Status: EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_NO_GUARD_PASS / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, and not a global impossibility theorem.

## Model

The rank-2 carrier ansatz is:

```text
q(Y) = u F(Y) + v G(Y),   deg F, deg G < 32,
```

with `u,v in K^7`, `K=GF(17^32)`, and `Y=X^8`. The induced orbit codewords are:

```text
P_s(X) = sum_{r=1}^7 (u_r F(X^8) + v_r G(X^8)) zeta^(s*r) X^r,
         s=0,...,6.
```

For a fixed carrier plane, the exact Sage audit builds projective ratio menus
at each of the `64` quotient points. It then tries to select local ZERO,
RATIO, and FREE options satisfying the support and pair-cap guards before
building the `64`-variable rational interpolation system in the coefficients
of `F` and `G`.

## Result

The first deterministic carrier-plane front generated `64` pair-visible
planes. Sage built exact local menus over `GF(17^32)` for all `64` planes.
The schedule heuristic constructed one best schedule per plane, but the front
had no guard-passing schedule:

```text
planes audited = 64
constructed schedule attempts = 64
guard-passing schedules = 0
exact interpolation systems tested = 0
best min support = 286
best selected incidence total = 2032
```

So this commit does not reach the rational-interpolation rank gate. The
negative is local to this first deterministic plane library and greedy
schedule selector.

## Interpretation

The rank-2 carrier route remains live. The next generator should make the
partition design itself more constructive, rather than choosing one largest
local equality block per quotient/phase. The immediate target is a carrier
plane and local-option grammar that reaches:

```text
support_i >= 327 for all seven labels
pair_ij <= 255 for all 21 pairs
selected incidences >= 2289
```

before exact interpolation.

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
