# M1 a=327 pair-clear direction nine-row repair

Status:

CANDIDATE / NINEROW_FIXED_DIRECTION_STABLE / PARTIAL / EXPERIMENTAL

This packet follows `402d88c` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous pair-clear row-syzygy checkpoint found the pinned direction:

```text
basis = basisaware_1_4_7_8_9_10
direction vector = [0,5,0,0,0,1]
forced pair count = 0
direction nonzero rows = 9
direction nonzero row classes = [0,2,3,5,6,11,12,14,15]
```

This branch targets that nine-row system directly. For each local mutation that
passes structural guards and contains the target basis, it checks:

```text
fixed direction = [0,5,0,0,0,1]
local anchored directions with up to two extra nonzero coordinates
```

The objective is to preserve pair-clear behavior and reduce the active support
below nine rows, or find an actual direction kernel. No Sage `GF(17^32)` exact
lift is attempted.

## Result

The bounded nine-row repair pass used:

```text
mutations generated = 72
candidate systems constructed = 216
structural-pass candidates = 210
structural-pass candidates analyzed = 36
structural-pass candidates skipped = 174
direction max extra coordinates = 2
target basis profiles present = 27
directions tested = 71307
pair-clear directions = 2883
row-reduced directions = 0
pair-clear direction-kernel profiles = 0
fixed-direction pair-clear profiles = 3
fixed-direction row-reduced profiles = 0
fixed-direction kernel profiles = 0
```

The best row remains the original pinned system:

```text
template = ninerow_base_w1_c3_d1
mutation = base_w1_c3_d1
assignment = fiber_round_robin
basis = basisaware_1_4_7_8_9_10
direction vector = [0,5,0,0,0,1]
forced pair count = 0
forced pairs = none
direction nonzero rows = 9
direction nonzero row classes = [0,2,3,5,6,11,12,14,15]
```

The tested front did not produce:

```text
direction_nonzero_rows <= 8
direction_nonzero_rows = 0
```

The local direction search also returned the same best vector:

```text
best local direction vector = [0,5,0,0,0,1]
best local direction nonzero rows = 9
```

## Interpretation

This is a local stability result for the pinned nine-row pair-clear direction.
The pair-clear property remains available, but this bounded mutation and local
direction front does not move the row support below nine.

So the obstruction has sharpened again:

```text
not pair projection
not coordinate-unit slot support
now a stable nine-row pair-clear direction system
```

This is not a global obstruction and not a proof that no `a=327` witness exists.
It only says that this pinned nine-row repair front did not find a smaller
support direction or kernel.

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
- failure outside this bounded nine-row front

## Next Target

Move to:

```text
m1-a327-pairclear-nine-row-module-syzygy
```

The next step should stop widening local mutation first and model the pinned
nine-row system algebraically:

```text
basis = [1,4,7,8,9,10]
direction = [0,5,0,0,0,1]
active row classes = [0,2,3,5,6,11,12,14,15]
```

Use Python to export the row system over `GF(17)`. Then use Macaulay2 or
Singular only if the exported equations become a small module/syzygy or
rank-minor problem. Sage should still wait until a pair-clear direction-kernel
proxy target exists.
