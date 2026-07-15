# Deployed `mu_64`: complete size-nine two-moment trade census

## Theorem and exact scope

For the deployed field and 64th root

```text
p=2,130,706,433,
zeta=1,548,376,985,
ord_p(zeta)=64,
```

the complete rotation-orbit census of nine-subsets of `mu_64` contains
exactly **55** disjoint aligned pairs with equal first and second elementary
symmetric moments.  Thus disjoint deployed-`mu_64` size-nine two-moment
trades exist.  Any payment route whose premise is “there are no disjoint
size-nine trades” is false.

Expanding the 55 representatives by all 64 rotations gives exactly 3,520
trades and 7,040 distinct wings.  Every wing lies in exactly one trade.

This theorem is a deployed-field finite classification.  It does not say
that every abstract size-nine trade has this form; it does not by itself
classify distance-nine graphs after adjoining other points; and it does not
pay a Profile 1792 row, another profile, a recurrence parent, or either
official question.

## 1. Exhaustive orbit generation

There are

```text
binom(64,9)/64 = 430,321,633
```

rotation orbits.  Because the subset size nine is odd while every
nonidentity rotation of the cyclic 64-set has even cycle lengths, no
nonidentity rotation fixes a nine-subset.  Hence the action is free and the
displayed quotient is exact.

The generator emits one canonical cyclic-gap necklace per orbit.  It also
checks its necklace generator against Burnside counts in 60 smaller test
cases.  The generated compact table has dtype `(key:uint64, mask:uint64)`,
16 bytes per record, and contains all 430,321,633 expected records.

No generated record has zero first moment, so neither tagged zero branch is
used in this run.

## 2. Complete invariant grouping and alignment

For a nine-set with moments `(s,e_2)` and `s!=0`, the compact rotation
invariant is

```text
(s^64, e_2/s^2).
```

Equality of these two quantities is complete for rotation alignment:
`(s'/s)^64=1`, so `s'/s` is a unique power of the deployed primitive 64th
root, and the ratio coordinate then aligns `e_2` as well.

Stable sorting of all records gives

```text
key groups                 429,075,424
repeated groups                119,174
candidate records             1,365,383
maximum group order                 105
aligned pair comparisons       7,166,305.
```

Every candidate moment is recomputed literally after alignment.  The group
histogram is

```text
order 2:      55 groups
order 11: 69,888 groups
order 12: 43,680 groups
order 13:  5,460 groups
order 14:     90 groups
order 105:     1 group.
```

Exactly the 55 order-two groups contain a disjoint aligned pair; the other
7,166,250 comparisons intersect.

## 3. Witness and rotation audit

The analysis JSON retains all 55 witnesses because the witness cap is 100.
The fast Ruby replay independently checks for every witness:

1. both masks have weight nine and are disjoint;
2. their first and second moments agree exactly in `F_p`;
3. the stored moments and invariant key are exact;
4. the ordered binary trade stream has the frozen SHA-256 digest below.

It then expands every witness through all 64 rotations.  There are 3,520
distinct unordered trade pairs and 7,040 distinct wing masks, and the trade
degree of every wing is one.  Thus neither a rotational stabilizer nor an
overlap between two trade orbits is hidden in the representative count.

## 4. Frozen artifacts and digests

```text
census script
  c2579102dddcfab1325a1a6b9a0de0a9cb4a7747541a0c9f1af98727c987ff5d
generation metadata
  871827e1c01530bccf3ae93ba31d1a9b32c703fb382a4d8154d90e98767d24b7
analysis JSON
  3686fa22df3d93e85bb660f81667182e45ed2ec9c3cdf4b1aa8e3685eaf959b5
6.4-GiB compact record table
  b3625474bf62f907cc03ae6f1befd3329fe48cebd4805f4d5462940757ab4f79
sorted `(key,mask)` record stream
  c9139ecb8a42266275a7a08427490db67c58c02896799b33437a0228a113e483
ordered disjoint-trade stream
  28815b3d7d27b3e939e9d65b7ad74caf97f515feaaec1fa04a8e78c7e9bea953
```

The sorted-stream digest is stronger than a raw `.npy` digest for replay
comparisons across harmless container-header differences.  The raw table
digest is retained as a byte-level freeze of this run.

## Replay

Fast literal replay of every returned witness and its rotations:

```bash
ruby work/verify_mu64_size9_trade_witnesses.rb
```

Full regeneration and exhaustive sort, using the already provisioned pinned
workspace runtime:

```bash
/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  work/census_mu64_size9_two_moment_trades_compact.py --batch-size 1000000 --generate-only
/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -B \
  work/census_mu64_size9_two_moment_trades_compact.py --analyze-only
```

The completed run used 868.922 seconds for generation and 743.704 seconds
for analysis.  The full replay needs roughly 6.4 GiB for the compact record
table plus transient memory for the stable key sort.
