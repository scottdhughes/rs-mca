# M1 a327 mu8 exact rank batch

Status: EXACT_EXTRACTION_NO_A327 / MU8_SELECTED_MUTATION_FULL_COLUMN_RANK / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Exact Rank Batch

The batch audits the `64` selected schedule mutations from the `mu_8` rank
feedback queue. For each schedule, it rebuilds the canonical active
`mu_8` quotient matrix over `GF(17^32)`:

```text
matrix shape = 264 x 224
```

All `64` selected mutations have full column rank:

```text
rank/nullity = 224/0
```

Therefore none of these fixed schedules has a nonzero active
`mu_8` orbit-polynomial kernel. Kernel classification is empty because no
positive-nullity schedule was found.

## Rank-One Carrier Probe

The rank-one carrier probe searches for a direction `u in K^7` with:

```text
coverage(u) = #{y : u in A_y} >= 33
odd residue support
```

Such a carrier would construct a degree `<32` scalar polynomial by vanishing on
the bad quotient points and would give a direct pair-visible kernel vector.

Across the same `64` schedules:

```text
pair-visible carriers found = 0
best pair-visible carrier coverage = 1
```

So the explicit rank-one carrier construction does not occur in this selected
mutation front.

## Interpretation

This is a narrow route cut for the selected `64` `mu_8` mutations, not a global
obstruction to `mu_8` orbit-invariant constructions. The useful result is that
the current mutation queue is algebraically full rank over the exact field, and
the simplest rank-one carrier mechanism is absent.

The next `mu_8` search should change the generator objective. Instead of
mutating only support/autocorrelation shape, it should optimize directly for:

- repeated quotient functional classes below threshold `32`;
- nontrivial common allowed directions with high coverage;
- structural rank deficiency before exact rank;
- pair-visible residue support.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- impossibility of other `mu_8` orbit-invariant schedules.
