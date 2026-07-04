# M1 a=327 pair-clear nine-row module syzygy

Status:

AUDIT / NINEROW_MODULE_SYZYGY_STABLE / PARTIAL / EXPERIMENTAL

This packet follows `66742fe` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The previous checkpoint stabilized the pinned pair-clear direction:

```text
basis = basisaware_1_4_7_8_9_10
direction vector = [0,5,0,0,0,1]
active row classes = [0,2,3,5,6,11,12,14,15]
inactive row classes = [13,16,17,18,19]
```

This branch exports that coefficient system over `GF(17)` and audits it as a
small module/syzygy problem. It checks:

```text
full 14 x 6 coefficient matrix
active 9 x 6 row matrix
inactive 5 x 6 row matrix
inactive + one active row, for all nine active rows
```

The Python audit is the primary ledger. Macaulay2 independently checks the same
small matrices. No Sage `GF(17^32)` exact lift is attempted.

## Result

Python over `GF(17)` gives:

```text
full matrix shape = [14,6]
full matrix rank = 6
full right-kernel nullity = 0
full left-syzygy dimension = 8

active matrix shape = [9,6]
active matrix rank = 6
active right-kernel nullity = 0
active left-syzygy dimension = 3

inactive matrix shape = [5,6]
inactive matrix rank = 5
inactive right-kernel nullity = 1
inactive left-syzygy dimension = 0
inactive right-kernel basis = [[0,5,0,0,0,1]]
```

The pinned direction spans the inactive kernel:

```text
pinned direction = [0,5,0,0,0,1]
projective pinned direction = [0,1,0,0,0,7]
inactive kernel projective basis = [[0,1,0,0,0,7]]
```

Every active row destroys that one-dimensional inactive kernel:

```text
singleton extensions tested = 9
singleton full-rank count = 9
```

Equivalently, for each active row class:

```text
[0,2,3,5,6,11,12,14,15]
```

the matrix formed by the five inactive rows plus that active row has rank 6.

Macaulay2 confirms the same ranks:

```text
M2 full rank = 6
M2 active rank = 6
M2 inactive rank = 5
M2 inactive right-kernel generators = 1
M2 active right-kernel generators = 0
M2 full right-kernel generators = 0
M2 extension ranks = 6 for all 9 singleton extensions
```

## Interpretation

This is a clean local module certificate for the pinned nine-row direction.
The five inactive rows cut out exactly the projective direction
`[0,5,0,0,0,1]`; each of the nine active rows is independent of that inactive
row span and therefore cannot be additionally killed while keeping the inactive
rows killed.

So the tested chamber has no direction that preserves the five inactive zeros
and removes even one of the nine active rows. This explains why the previous
local direction scan stayed at nine rows.

This is still not a global obstruction. It does not rule out:

- a different basis
- a different projective direction with different inactive rows
- a different template family
- an exact `a=327` witness outside this local front

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
- global obstruction outside the pinned nine-row module front

## Next Target

Move to:

```text
m1-a327-pairclear-direction-support-chamber-search
```

The next constructive branch should not try to kill an active row inside this
same inactive chamber. Instead, search for a different pair-clear direction
whose inactive row set has:

```text
inactive rank <= 4
```

or whose inactive kernel has dimension at least 2, giving room to impose extra
active-row zeros while preserving pair-clear projections. Use Python for the
rank/chamber search. Macaulay2/Singular remain useful only for small pinned
module checks. Sage should wait until a pair-clear direction-kernel proxy target
exists.
