# M1 Interleaved-List Threshold Interval Sharpening

Date: 2026-06-27

Status: PROVED LOWER BOUND / ROUTE CUT / PARTIAL INTERVAL / SEPARATE TRACK.

## Scope

This packet sharpens the open interval left by the interleaved-list threshold
descent for

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

for every interleaving arity `mu >= 1` whenever

```text
2a - n >= k.
```

For `n=512` and `k=256`, this is exactly

```text
384 <= a <= 512.
```

The support-occupancy packing argument rules out seven witnesses for

```text
373 <= a <= 383.
```

Indeed, for seven hypothetical common-support witnesses with supports
`S_1,...,S_7`, each of size at least `a`, distinct codewords in an
`[512,256]` Reed-Solomon code agree on at most `255` positions.  Hence

```text
sum_{i<j} |S_i cap S_j| <= binom(7,2) * 255 = 5355.
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

contradicting the pairwise budget.  Therefore seven witnesses are impossible
at `a=373`, and a fortiori at larger agreements in this descent window.

At `a=372`, the same packing obstruction no longer rules out seven witnesses.

## New Lower Bound At a=292

The previous root-pencil lower bound first clears at `a=291`.  This packet
improves the first proved clearing row to

```text
a = 292.
```

Choose a common root set

```text
A subset H,        |A| = 254.
```

Let `P_A` be the degree-254 polynomial vanishing on `A`.  The complement
`H \ A` has size `258`.

Choose eight distinct complement points

```text
x1,x2,x3,x4,x5,x6,y12,y34 in H \ A
```

avoiding the finitely many residual-line coincidences described below.  Define
seven residual linear polynomials

```text
r0(X) = 0,
r1(X) = X - x1,
r2(X) = ((y12-x1)/(y12-x2)) * (X - x2),
r3(X) = X - x3,
r4(X) = ((y34-x3)/(y34-x4)) * (X - x4),
r5(X) = X - x5,
r6(X) = X - x6.
```

The exclusions ensure that these residuals are pairwise distinct.  Such a
choice is possible with large slack.  Choose the six star points first.  This
leaves `252` complement points.  For `y12`, the conditions that it be distinct,
that the displayed denominator be nonzero, and that `r2` avoid the already
chosen residuals exclude at most a fixed dozen values.  After `y12` is chosen,
the same argument excludes at most fourteen values for `y34`.  The verifier
records this conservative finite-exclusion budget.

Now define codewords

```text
P_i(X) = P_A(X) r_i(X),        0 <= i <= 6.
```

Each has degree at most

```text
254 + 1 = 255 < 256,
```

so each is a codeword of `C`.

All seven codewords agree on the common root set `A`.  In the complement,
use the following eight controlled overlap points:

```text
x1:  P_0 = P_1,
x2:  P_0 = P_2,
x3:  P_0 = P_3,
x4:  P_0 = P_4,
x5:  P_0 = P_5,
x6:  P_0 = P_6,
y12: P_1 = P_2,
y34: P_3 = P_4.
```

The resulting overlap counts by witness are

```text
[6,2,2,2,2,1,1].
```

Since `a=292`, each witness needs

```text
292 - 254 = 38
```

complement positions beyond the common root core.  Therefore the unique
positions needed by the seven witnesses are

```text
[32,36,36,36,36,37,37],
```

whose sum is `250`.  Together with the eight overlap points, this uses exactly

```text
250 + 8 = 258 = |H \ A|
```

complement points.

Define a received word by taking the common value on each controlled overlap
point and, on each unique block, the value of the assigned codeword.  Then every
`P_i` agrees with the received word on exactly

```text
254 + 38 = 292
```

positions.  Diagonal embedding gives the same lower bound for every
interleaving arity `mu`.

Thus

```text
Lambda_mu(C,292) >= 7.
```

This is a lower bound only; exact `Lambda_mu(C,292)` is not claimed.

## Sharpened Ledger

The scanner records:

```text
384..512 : Lambda_mu = 1                         PROOF_RECORD
373..383 : Lambda_mu <= 6                        ROUTE_CUT
372..293 : packing permits 7; no lower bound     PARTIAL
292      : linear-overlap lower bound = 7        LOWER_ONLY
```

The phrase `LOWER_ONLY` is intentional.  The lower bound is enough for the
interleaved-list gate, but the exact list size is not claimed.

## Status Ledger

PROVED:

- high-agreement uniqueness for `384 <= a <= 512`;
- packing route cut `Lambda_mu(C,a) <= 6` for `373 <= a <= 383`;
- linear-overlap lower bound `Lambda_mu(C,292) >= 7`;
- all counts use the interleaved-list denominator `|F|=17^32`.

PARTIAL:

- `372 <= a <= 293`: seven witnesses are not excluded by the packing test, but
  this packet does not construct them.

NOT CLAIMED:

- no MCA `N_bad`;
- no protocol soundness failure;
- no ordinary list-decoding failure beyond the stated predicate;
- no exact `Lambda_mu` values in the partial interval;
- no exact `Lambda_mu(C,292)`;
- no exact `delta*_C`.

## Validation

Run:

```bash
python3 experimental/scripts/scan_m1_interleaved_list_threshold_interval_sharpening.py
python3 experimental/scripts/verify_m1_interleaved_list_threshold_interval_sharpening.py
python3 experimental/scripts/verify_m1_interleaved_list_threshold_interval_sharpening.py --json
python3 -m json.tool experimental/data/m1_interleaved_list_threshold_interval_sharpening.json
```
