# M1 a=327 cycle-guarded template front search

Status:

CANDIDATE / CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK / PARTIAL / EXPERIMENTAL

This packet follows `a63ab87` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The local rank-slack basis-exchange and support-augmentation fronts kept
returning to the cyclic forced-pair patterns:

```text
P56/P57/P67
P45/P46/P56
P14/P16/P17/P46/P47/P67
```

This branch moves the cyclic pair-clear obstruction upstream. Instead of
repairing a selected rank-slack profile after the fact, it samples directions
inside higher-level template/basis profiles and rejects directions that force
any pair in:

```text
[P14,P16,P17,P45,P46,P47,P56,P57,P67]
```

The scan is intentionally a bounded front search, not an exact lift.

## Search

The banked bounded sweep used:

```text
mutations generated = 646
seed offsets = 3
candidate systems constructed = 5814
structural pass candidates = 5328
selected candidates = 219
basis profiles tested = 876
directions sampled per profile = 2048
```

It found:

```text
cycle-clear profiles = 453
cycle-clear rank-slack profiles = 203
exact pair-clear profiles = 291
exact pair-clear rank-slack profiles = 80
```

Failure/status counts:

```text
CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_RANKSLACK = 80
CYCLEG_TEMPLATE_EXACT_PAIRCLEAR_ONLY = 211
CYCLEG_TEMPLATE_CYCLE_CLEAR_RANKSLACK = 73
CYCLEG_TEMPLATE_CYCLE_CLEAR_ONLY = 89
CYCLEG_TEMPLATE_NO_CYCLE_CLEAR_DIRECTION = 423
```

## Best Profile

The best profile is:

```text
template = ninerow_P57_shear_c1_d1
mutation = P57_shear_c1_d1
assignment = fiber_round_robin
assignment seed = 179986
basis = basisaware_0_1_2_3_4_5
basis class indices = [0,1,2,3,4,5]
basis support sizes = [216,142,142,105,105,74]
coefficient matrix shape = [19,6]
```

Its best sampled exact pair-clear rank-slack direction is:

```text
direction = [1,4,0,0,10,0]
direction weight = 3
forced pairs = []
cycle pairs cleared = [P14,P16,P17,P45,P46,P47,P56,P57,P67]
zero row classes = [7,8,9,13,17,19,21,23]
zero row count = 8
inactive rank = 4
inactive kernel nullity = 2
```

So the cyclic pair-clear obstruction can be avoided at the high-level template
front while also creating rank slack in the inactive rows. This is the first
front after the support-augmentation route cut where exact pair-clear and
rank slack appear together in the sampled template direction.

## Interpretation

This is a constructive front signal, not a proof row. It shows that making the
cycle pairs a generation-time guard changes the search behavior: the scan finds
sampled directions clearing every pair projection, including all cyclic tail,
P456, and mixed-front pairs, and it finds 80 profiles where exact pair-clear and
rank slack coexist.

The remaining issue is downstream realization/lift. The next branch should not
re-enter the old local pair-clear repair basin. It should reconstruct the best
exact pair-clear rank-slack chamber and determine whether the proxy chamber can
be realized as a selected-class/low-rank template target before any heavy
`GF(17^32)` lift.

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
- global obstruction outside the tested cycle-guarded template front

## Next Target

Create a focused branch for the best exact-pair-clear chamber:

```text
m1-a327-cycleguard-exact-pairclear-chamber-realization
```

The objective should be to reconstruct the best profile, enforce the direction
`[1,4,0,0,10,0]`, and determine whether the resulting exact pair-clear
rank-slack chamber can be realized as a useful selected-class/low-rank template
target before any heavy `GF(17^32)` lift.
