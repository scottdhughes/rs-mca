# M1 a327 mu8 rank2 full-menu carrier synthesis

Status: EXACT_EXTRACTION_NO_A327 / MU8_RANK2_CARRIER_FULL_MENU_SUPPORT_PAIR_INFEASIBLE / PARTIAL / EXPERIMENTAL.

This packet remains strictly INTERLEAVED_LIST work over `RS[F_17^32,H,256]`
with denominator `17^32` and `mca_counted=false`. It is not an MCA row, not
protocol soundness, and not a global `Lambda_mu(C,327) <= 6` theorem.

## What Changed

The previous CP-SAT scheduler used ratio width `4` and a hard interpolation
row-cost gate. This packet keeps width `4` but removes the hard row-slack gate:
row cost is now only a soft objective, and exact Sage interpolation remains
the only algebraic authority.

The scan also adds a first deterministic carrier-plane synthesis ledger. It
emits balanced GF(17)-seed carrier planes with forced pair identities filtered
out. These are seed planes for later exact menu scans, not proof records.

## Result

The width ablation solved `64` carrier planes at widths `4` and `8`:

```text
widths tested = [4, 8]
hard row-slack gate = false
best min support = 313
best selected incidence total = 2193
required min support = 327
required selected incidence total = 2289
guard-passing candidates = 0
```

The best candidate was pair-cap tight:

```text
max pair load = 255
```

No support/pair-passing schedule was produced, so no exact interpolation system
was tested.

## Interpretation

Removing the hard row-slack gate helps materially:

```text
291 -> 313 best min support
2041 -> 2193 best total incidence
```

but the bounded width-8 menu is still short by `14` on weakest support and
`96` selected incidences overall. This is a local-menu support/pair failure, not
an algebraic rank obstruction to rank-2 carriers.

The next step is to run real width expansion or adaptive ratio column
generation. The current data suggests the width-4 menu is close enough that
additional ratio signatures may matter.

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
