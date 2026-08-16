---
workboard_item: K4
row: KoalaBear MCA
object: MCA
target_epsilon: 2^-128
agreement: 1116048
B_star: 274980728111395087
unit: distinct bad affine slopes per received line
parent_commit: 42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08
status: PROVED_SOURCE_BOUND_SHORTENING_ADAPTER
active_v4_ledger_movement: 0
---

# Contract

This packet is a direct successor to the nested pinned-span router at exact
parent `42e15d1bc6d8c2f1b73936bea157f6fcfafbfb08`.  It closes the first semantic gap left by that packet:
the pinned coordinates are promoted from coefficient-space common zeros to
actual support-wise MCA shortening data.

For each certified prefix `T_k`, one fixed degree-`<10` interpolation pair is
subtracted from the received pair.  The locator of `T_k` is then divided out
of every selected explanation and minimizing pair, and the coordinates in
`T_k` are deleted.  The resulting family is an actual support-wise MCA-bad
family for

```text
(n_k,K_k,m_k)=(2097152-k,1048576-k,1116048-k).
```

The map preserves each finite affine slope, every complete agreement-domain
witness after deleting `T_k`, same-domain pair noncontainment, and the
dimension of the pinned direction span.  The ten certified loads and
dimension floors are therefore retained in ten genuine shortened rows.

## Crucial support convention

The proof uses the complete scalar agreement domain of each explanation, not
an arbitrary replacement of coordinates inside an exact size-`m` witness.
A shipped `GF(5)` counterexample shows that replacing one coordinate in an
exact bad support can make that new support pair-contained.  The complete
agreement domain remains pair-noncontained, and any shortened pair
explanation lifts to a pair explanation on that complete original domain.

## Exact impact

- source-bound shortening ladder: proved;
- compatible quotient-direction ladder: proved;
- all three gaps `n-K`, `m-K`, and `n-m`: preserved exactly;
- active-v4 ledger movement: `0`;
- affine error rank eleven paid: no;
- KoalaBear closed: no.
