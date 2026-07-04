# M1 a=327 cycleguard exact pair-clear chamber realization

Status:

CANDIDATE / CYCLEG_REALIZATION_STABLE_WINDOW / PARTIAL / EXPERIMENTAL

This packet follows `0fc5a00` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The cycle-guarded template front found exact pair-clear and rank slack together.
This branch reconstructs the best chamber directly from its mutation spec and
assignment seed, then audits what the chamber actually gives before any heavy
`GF(17^32)` exact lift.

The source front was:

```text
commit = 0fc5a00
basis profiles tested = 876
exact pair-clear profiles = 291
exact pair-clear rank-slack profiles = 80
best template = ninerow_P57_shear_c1_d1
best basis = basisaware_0_1_2_3_4_5
```

## Reconstruction

The target chamber reconstructs directly from:

```text
mutation = P57_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 179986
seed offset = 0
basis = basisaware_0_1_2_3_4_5
basis class indices = [0,1,2,3,4,5]
basis support sizes = [216,142,142,105,105,74]
coefficient matrix shape = [19,6]
```

The reconstructed candidate has:

```text
support vector = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
selected class size counts = {3:185,4:43,5:142,6:142}
functional classes = 25
functional span rank = 6
forced functional identities = 0
annihilator dimension = 0
```

## Best Chamber

The best direction is:

```text
direction = [1,4,0,0,10,0]
forced pairs = []
cycle forced count = 0
cycle pairs cleared = [P14,P16,P17,P45,P46,P47,P56,P57,P67]
```

It creates the inactive row set:

```text
zero row classes = [7,8,9,13,17,19,21,23]
zero row count = 8
inactive rank = 4
inactive kernel nullity = 2
```

The zero-class support union is:

```text
zero class union size = 253
stable window dimension = 3
```

This is the key improvement over the previous local pair-clear repair basin:
the chamber clears all pair projections, preserves rank slack, and leaves a
small positive degree window for a common zero set.

## Rank-Slack Subspace

The inactive-row nullspace basis is:

```text
[0,0,1,0,0,0]
[12,14,0,0,1,0]
```

Among the 18 projective directions in this two-dimensional subspace:

```text
pair-clear directions = 11
```

So the exact pair-clear property is not a single isolated direction inside the
rank-slack chamber.

## Interpretation

This is a proxy/chamber realization checkpoint. It does not construct seven
degree-<256 codewords over `GF(17^32)`. It says the best cycle-guarded front
can be reconstructed cheaply and has the three necessary proxy features that
were not coexisting in the local repair basin:

```text
exact pair-clear
rank slack
positive zero-union window
```

The next branch should turn this chamber into an exact lift target. The first
step should be a Sage audit of the chamber-induced divisibility/stable-window
system, not another broad mutation scan.

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
- global obstruction outside the tested cycle-guarded chamber

## Next Target

Create:

```text
m1-a327-cycleguard-stable-window-exact-audit
```

The audit should use the reconstructed chamber, its zero classes, and the
3-dimensional stable window to build an exact `GF(17^32)` lift target. Only if
Sage verifies seven distinct degree-<256 codewords and one received word on `H`
with agreement at least 327 for all seven should this become a proof-record PR.
