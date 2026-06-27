# M1 Interleaved-List Threshold Descent Sage Audit

Date: 2026-06-27

Status: PROOF_RECORD / LOWER_BOUND / INDEPENDENT SAGE AUDIT.

## Scope

This audit independently hardens the first clearing row from
`experimental/notes/m1/m1_interleaved_list_threshold_descent.md`.

The row is:

```text
C = RS[F_17^32,H,256],        |H| = 512,
agreement a = 291,
track = INTERLEAVED_LIST.
```

The audit checks only the standard interleaved-list predicate.  It does not
count an MCA `N_bad` event and does not prove a protocol soundness statement.

## What Sage Checks

The Sage script

```text
experimental/scripts/audit_m1_interleaved_list_threshold_descent.sage
```

does not import the Python scanner JSON.  It reconstructs the finite-field and
witness data directly:

- constructs `GF(17^32)`;
- constructs a multiplicative subgroup `H` of order `512`;
- recomputes `|F|=17^32`;
- recomputes `floor(|F|/2^128)=6`, so the list-track numerator needed to clear
  is `7`;
- constructs a root set `A subset H` of size `255`;
- builds the nonzero degree-255 root polynomial `P_A`;
- partitions the 257-point complement into seven disjoint blocks of size `36`
  plus a residual block of size `5`;
- forms seven scalar multiples `lambda_j P_A`;
- constructs one received word for which each scalar multiple agrees on exactly
  `255+36=291` points;
- verifies the seven witnesses are distinct;
- verifies diagonal repetition works for sampled `mu in {1,2,3,7}`, with the
  proof reason applying to every `mu`;
- emits canonical witness descriptor hashes.

## Result

The audit verifies:

```text
Lambda_mu(C,291) >= 7
```

for the standard interleaved-list predicate, for every interleaving arity `mu`
by diagonal repetition.

Since

```text
floor(17^32 / 2^128)=6,
```

this lower bound clears the interleaved-list track's numerical gate.

## Status Discipline

PROOF_RECORD / LOWER_BOUND:

- `Lambda_mu(C,291) >= 7`;
- denominator `|F|=17^32`;
- predicate is the standard interleaved-list predicate.

ROUTE_CUT inherited from the Python descent packet:

- `384..512` has `Lambda_mu=1`;
- `373..383` has `Lambda_mu <= 6` and cannot clear.

PARTIAL:

- `372..292` remains unresolved for exact `Lambda_mu` and for a stronger
  lower-bound construction.

NOT CLAIMED:

- no MCA `N_bad` row;
- no protocol soundness failure;
- no ordinary list-decoding theorem beyond the stated predicate;
- no exact value of `Lambda_mu(C,291)`;
- no exact `delta*_C`.

## Validation

Run:

```bash
sage experimental/scripts/audit_m1_interleaved_list_threshold_descent.sage
sage experimental/scripts/audit_m1_interleaved_list_threshold_descent.sage --json
```
