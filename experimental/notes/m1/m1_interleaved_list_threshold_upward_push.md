# M1 Interleaved-List Threshold Upward Push

Date: 2026-06-27

Status: PROOF RECORD / LOWER BOUND / ROUTE CUT / PARTIAL INTERVAL / SEPARATE TRACK.

## Scope

This packet pushes the interleaved-list lower-bound clearing agreement upward
for

```text
C = RS[F_17^32,H,256],        |H| = 512.
```

It is only an `INTERLEAVED_LIST`-track packet.  It is not an MCA `N_bad`
statement and does not change the finite-slope MCA row.

The list-track denominator is

```text
|F| = 17^32,
floor(17^32 / 2^128) = 6.
```

Thus a list-track lower bound clears the numerical gate once

```text
L_lower >= 7.
```

## Replayed Boundary

The high-agreement uniqueness theorem gives

```text
Lambda_mu(C,a)=1
```

for

```text
384 <= a <= 512.
```

The support-occupancy packing argument rules out seven witnesses for

```text
373 <= a <= 383.
```

At `a=373`,

```text
7a = 2611 = 512*5 + 51,
```

so convexity gives

```text
sum_h binom(m_h,2)
  >= 461*binom(5,2) + 51*binom(6,2)
  = 5375,
```

while seven distinct Reed-Solomon witnesses have pairwise support-overlap
budget at most

```text
binom(7,2) * 255 = 5355.
```

Thus seven witnesses are impossible at `a=373`, and a fortiori at larger
agreements below the uniqueness range.

## Quotient-Fiber Lower Bound At a=320

The new lower-bound construction uses the quotient map

```text
phi(x) = x^32
```

on `H`.  Since `|H|=512`, this map has fibers of size `32` and image size

```text
|Q| = 16.
```

The quotient image lies in `F_17`, because `17 == 1 mod 16`.  Put

```text
c = 32,
N_Q = 16,
m = 10,
a = cm = 320,
ceil(k/c) = ceil(256/32) = 8,
sigma_Q = m - ceil(k/c) = 2.
```

For each `10`-subset `A subset Q`, define

```text
L_A(X) = product_{y in A} (X^32 - y).
```

This locator has degree `320` and vanishes on a union of ten quotient fibers,
so its support size is `320`.

Write the quotient locator as

```text
prod_{y in A}(Y-y)
  = Y^10 + lambda_9(A)Y^9 + lambda_8(A)Y^8 + ... .
```

Record the high quotient coefficient pair

```text
(lambda_8(A), lambda_9(A)) in F_17^2.
```

There are

```text
binom(16,10) = 8008
```

quotient subsets and only

```text
17^2 = 289
```

possible high-coefficient pairs.  Hence some pair occurs at least

```text
ceil(8008/289) = 28
```

times.

For a heaviest pair `(h_8,h_9)`, set

```text
U(X) = X^320 + h_8 X^256 + h_9 X^288.
```

For every quotient subset in the fiber, reducing `U` modulo `L_A` cancels the
terms of degree at least `256`.  The remainder has degree `<256`, and it agrees
with `U` on the full fiber-union support of size `320`.

Distinct quotient supports give distinct remainders by the usual locator
argument: if two remainders were equal, then `U-P` would have degree at most
`320` and vanish on the union of two different `320`-point supports, which has
more than `320` points.

Therefore

```text
Lambda_mu(C,320) >= 28.
```

The standard base-list-to-interleaved embedding gives the same lower bound for
every interleaving arity `mu`.

## Sage Audit

The Sage audit independently constructs:

- `GF(17^32)`;
- a cyclic subgroup `H` of order `512`;
- the quotient image for `x -> x^32`;
- the heaviest high-coefficient fiber;
- every degree-`<256` codeword in that heaviest fiber;
- a received word with agreement `320` for each verified witness.

In the audited finite row, the heaviest fiber has size `32`, so the Sage audit
verifies `32` explicit witnesses.  The theorem statement keeps the conservative
pigeonhole lower bound `Lambda_mu(C,320) >= 28`.

The audit emits canonical support and coefficient hashes.

## Sharpened Ledger

The packet records:

```text
384..512 : Lambda_mu = 1                         PROOF_RECORD
373..383 : Lambda_mu <= 6                        ROUTE_CUT
321..372 : packing permits 7; no lower bound     PARTIAL
320      : quotient-fiber lower bound >= 28      LOWER_ONLY
```

The phrase `LOWER_ONLY` is intentional.  The lower bound is enough for the
interleaved-list gate, but the exact list size is not claimed.

## Status Ledger

PROVED:

- high-agreement uniqueness for `384 <= a <= 512`;
- packing route cut `Lambda_mu(C,a) <= 6` for `373 <= a <= 383`;
- quotient-fiber lower bound `Lambda_mu(C,320) >= 28`;
- all counts use the interleaved-list denominator `|F|=17^32`.

PARTIAL:

- `321 <= a <= 372`: seven witnesses are not excluded by the packing test, but
  this packet does not construct them.

NOT CLAIMED:

- no MCA `N_bad`;
- no protocol soundness failure;
- no ordinary list-decoding failure beyond the stated predicate;
- no exact `Lambda_mu(C,320)`;
- no exact `delta*_C`.

## Validation

Run:

```bash
python3 experimental/scripts/scan_m1_interleaved_list_threshold_upward_push.py
python3 experimental/scripts/verify_m1_interleaved_list_threshold_upward_push.py
python3 experimental/scripts/verify_m1_interleaved_list_threshold_upward_push.py --json
sage experimental/scripts/audit_m1_interleaved_list_threshold_upward_push.sage
sage experimental/scripts/audit_m1_interleaved_list_threshold_upward_push.sage --json
python3 -m json.tool experimental/data/m1_interleaved_list_threshold_upward_push.json
```
