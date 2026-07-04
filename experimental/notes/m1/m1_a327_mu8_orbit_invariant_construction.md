# M1 a327 mu_8 orbit-invariant construction

Status: EXACT_EXTRACTION_NO_A327 / MU8_ORBIT_NULLITY_ZERO_FRONT / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, not exact `Lambda_mu`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Construction Model

The construction uses the order-8 subgroup `mu_8 <= H`. Write a candidate base
polynomial as:

```text
P(X) = sum_{t=1}^7 X^t g_t(X^8),  deg g_t < 32.
```

The invariant part `g_0(X^8)` is omitted in this first front because it cannot
separate the `mu_8` orbit codewords. This leaves:

```text
unknowns = 7 * 32 = 224
quotient cosets = 64
period-8 pattern classes = 8
target support per orbit codeword = 328
```

For each quotient coset, the selected pattern requires the values of `P` on a
subset of the eight `mu_8` positions to be equal. A pattern front with total
period size `41` gives support `8 * 41 = 328` for every orbit codeword.

## Result

The audit tested `29` deterministic period-8 schedules. Of these, `9` passed
the support and ambient pair-autocorrelation guards. Every guard-passing
schedule produced the same exact matrix shape over `GF(17^32)`:

```text
264 x 224
```

All `9` guard-passing exact matrices had full column rank:

```text
rank/nullity = 224/0
```

No exact orbit candidate was constructed in this first front.

## Interpretation

This does not kill the `mu_8` orbit-invariant idea. It says the first small
period-8 Sidon-complement schedule family is algebraically full rank over
`GF(17^32)`.

The construction remains attractive because the exact matrices are small enough
to audit directly in Sage. The next `mu_8` branch should widen the pattern
grammar and/or implement the block decomposition suggested by the symmetry, so
rank feedback can be used inside the schedule generator instead of testing only
hand-seeded Sidon fronts.

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
