# M1 a327 quotient-subgroup primal-kernel search

Status:

CANDIDATE / QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING / PARTIAL / EXPERIMENTAL

This packet follows `cff22a0` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The collision-budget right-kernel branch showed that shallow coefficient-level
right kernels are common but do not survive proxy expansion:

```text
right-kernel collision-budget profiles = 192
proxy ranked profiles = 12
proxy positive profiles = 0
best failure = RKERNEL_PROXY_FULL_RANK
```

So this branch moves to a native RS right-kernel model. Instead of prescribing a
random reduced q-vector, use quotient-subgroup codeword differences:

```text
g_i(X) = P_i(X^s),  i=1,...,6
```

for:

```text
s = 32, 16, 8, 4
```

If `deg(P_i-P_j) <= floor(255/s)`, then the lifted pair agreement on `H` is at
most `255`, so the RS pair cap is visible at the quotient level.

## Count Model

For a fixed `s`, the quotient length is `512/s`. At each quotient coordinate,
the seven quotient values induce a partition of the witnesses. The received
word may choose different blocks on the `s` coordinates inside the fiber.

The OR-Tools CP-SAT model chooses:

- how many quotient fibers use each witness partition;
- how many coordinates inside those fibers select each block.

It enforces:

```text
support vector = [327,327,327,327,327,327,327]
pair equality on H <= 255 for every pair
pair-to-7 selected counts >= 142
```

The run used:

```text
OR-Tools = 9.15.6755
time limit = 20 seconds per s-value
max active partitions = 80
```

## Result

The screen tested all four requested values:

```text
s = 32: unresolved under time limit
s = 16: unresolved under time limit
s = 8:  unresolved under time limit
s = 4:  feasible, OPTIMAL
```

Best screen:

```text
best s = 4
quotient length = 128
quotient degree bound = 63
support vector = [327,327,327,327,327,327,327]
pair7 counts = [252,252,252,252,252]
max pair equality on H = 252
max quotient pair equality count = 63
active partition count = 22
status = QUOTIENT_CP_FEASIBLE_REALIZATION_PENDING
```

The `s=4` count schedule therefore clears the support and pair-cap layer. It is
not yet an exact RS witness, because no quotient polynomials `P_i` have been
constructed to realize the recorded quotient partitions.

## Interpretation

This is the first positive signal after the coefficient-kernel front:

```text
native quotient-subgroup support allocation: feasible
exact quotient-polynomial realization: pending
Sage GF(17^32) witness: not attempted
```

The feasible `s=4` schedule is tight but plausible:

```text
max pair equality on H = 252 < 255
quotient pair count = 63
degree bound for P_i-P_j = 63
```

So the next obstruction is no longer support/pair budgeting. It is quotient
partition realization by seven degree-`<=63` quotient polynomials.

The unresolved `s=32`, `s=16`, and `s=8` screens are not negative results. They
only failed to produce a schedule within the bounded CP-SAT run.

## Next Step

Move to:

```text
m1-a327-quotient-subgroup-realization-search
```

Start from the `s=4` feasible count schedule and try to realize the active
quotient partitions by seven quotient polynomials:

```text
P_1,...,P_7 in F[Y] with degree <= 63
```

on a quotient domain of length `128`.

The realization branch should:

1. expand the 22 active partition types into 128 labelled quotient coordinates;
2. build equality constraints `P_i(y)=P_j(y)` for pairs in the same block;
3. keep pair equality sets at or below 63 quotient points;
4. solve first over proxy fields compatible with a length-128 subgroup;
5. if proxy realization succeeds, run Sage over `GF(17^32)`;
6. lift via `f_i(X)=P_i(X^4)` and verify directly on `H`.

Board-moving only if Sage verifies:

```text
GF(17^32)
H order = 512
seven distinct degree<256 codewords
one received word on H
agreement >=327 for all seven
denominator |F| = 17^32
mca_counted = false
```

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track quotient-subgroup proxy;
- global obstruction outside the tested quotient-subgroup count screen.
