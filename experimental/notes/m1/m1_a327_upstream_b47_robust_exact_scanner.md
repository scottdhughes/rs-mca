# M1 a=327 upstream B47-robust exact scanner

Status: `PARTIAL / EXPERIMENTAL`

This packet starts the exact-field upstream search requested after
`0500d07`. The goal is to construct new repaired skeleton candidates and score
them by split resilience before treating them as progress.

## Scope

Track: `INTERLEAVED_LIST`

Row: `RS[F_17^32,H,256]`

Denominator: `|F| = 17^32`

This is not an MCA row, not a protocol claim, not a public-board update, and
not a global obstruction theorem.

## Source route cut

The prior exact lineage was banked in the local-basin conservation note. Its
failure mode was concentrated in the repaired skeleton

```text
capacity      = 333
B values      = [1024,657,656,1024,1024]
collapse      = [[1,4,5,7],[6],[3],[2]]
```

and the full compensated split v2 grid found no tested vector preserving
capacity and all pair guards after splitting the residual `[1,4,5,7]` class.

## Scanner design

This branch uses the Sage-native repaired-skeleton cache and exact residual
append solver. Each candidate system is exact over `GF(17^32)` and is built by
adding upstream skeleton constraints before split probes are applied.

The exact case runner is batched one Sage process at a time so a slow residual
solve records as an execution fact rather than blocking the full scan.

Candidate families:

```text
alt_14_57
alt_15_47
alt_17_45
alt_145_7
b47_guard
triple_237_b47_guard
```

Budgets:

```text
1, 2, 4, 8
```

Split probes:

```text
split_4_from_157
split_14_vs_57
split_1_from_457
```

The robustness score is:

```text
min(capacity - 327,
    B27 - 654,
    B37 - 654,
    B47 - 654,
    B57 - 654)
```

The intended rule is: split-resilient before claiming progress.

## Success criteria

Board-moving success still requires all of:

```text
exact max-min >= 327
seven distinct degree<256 codewords
one received word on H
Sage audit over GF(17^32)
H order = 512
denominator |F| = 17^32
mca_counted = false
```

Strong local progress is any exact candidate skeleton whose split probes
preserve:

```text
capacity >= 327
B27 >= 654
B37 >= 654
B47 >= 654
B57 >= 654
```

with residual collapse not concentrated in `[1,4,5,7]`.

## Non-claims

- No `a=327` interleaved-list certificate.
- No MCA `N_bad` claim.
- No protocol soundness claim.
- No ordinary list-decoding theorem beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6` theorem.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
- No global obstruction outside the tested basin.
