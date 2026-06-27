# M1 Interleaved-List Threshold Descent

Date: 2026-06-27

Status: PROVED LOWER BOUND / ROUTE CUT / PARTIAL INTERVAL / SEPARATE TRACK.

## Scope

This packet descends from the first uncovered interleaved-list agreement below
the high-agreement uniqueness range for

```text
C = RS[F_17^32,H,256],        |H| = 512.
```

It is only an `INTERLEAVED_LIST`-track packet.  It is not an MCA `N_bad`
statement and does not change the finite-slope MCA row.

The board denominator for this track is

```text
|F| = 17^32,
floor(17^32 / 2^128) = 6.
```

So a board-clearing interleaved-list lower bound needs

```text
L_lower >= 7.
```

## Replay: High-Agreement Range

The integrated high-agreement theorem gives

```text
Lambda_mu(C,a)=1
```

for every interleaving arity `mu >= 1` whenever

```text
2a-n >= k.
```

For `n=512` and `k=256`, this is exactly

```text
384 <= a <= 512.
```

No row in this range clears the interleaved-list gate.

## Packing Route Cut: 373 <= a <= 383

For distinct interleaved tuples at agreement `a`, choose one common agreement
support `S_i` for each tuple.  If two tuples are distinct, then some row
codeword differs.  Their common support intersection is therefore a zero set
of a nonzero degree-`<256` polynomial, so it has size at most `255`.

For seven hypothetical witnesses,

```text
sum_i |S_i| >= 7a,
sum_{i<j} |S_i cap S_j| <= binom(7,2)*255 = 5355.
```

If `m_h` is the number of supports containing `h in H`, then

```text
sum_h m_h >= 7a,
sum_h binom(m_h,2) = sum_{i<j} |S_i cap S_j|.
```

The scanner compares the pairwise budget `5355` with the convexity lower bound
on

```text
sum_h binom(m_h,2).
```

At `a=373`,

```text
7a = 2611 = 512*5 + 51,
sum_h binom(m_h,2) >= 461*binom(5,2) + 51*binom(6,2) = 5375,
```

which is larger than `5355`.  Thus seven witnesses are impossible at `a=373`,
and a fortiori at all larger agreements in this descent window.

For every

```text
373 <= a <= 383,
```

seven witnesses are impossible.  Thus

```text
Lambda_mu(C,a) <= 6        for 373 <= a <= 383.
```

In particular, `a=383`, `a=382`, and `a=373` cannot clear the list-track gate.

At `a=372`, this packing obstruction no longer rules out seven witnesses.
That is only a possibility statement, not a lower bound.

## Root-Pencil Lower Witness

A separate lower-bound construction uses scalar multiples of one root
polynomial.

Choose `A subset H` with

```text
|A| = k-1 = 255.
```

Let `P_A` be a nonzero degree-255 polynomial vanishing on `A`.  For distinct
scalars `lambda_j`, the codewords `lambda_j P_A` all agree on `A`, and they
are pairwise different on the complement `H \ A`, which has size `257`.

At agreement `a > 255`, each listed codeword needs

```text
b = a - 255
```

extra positions from this complement.  Disjoint blocks of size `b` therefore
give

```text
floor(257 / (a-255))
```

listed codewords.  Repeating these codewords diagonally in every row gives the
same lower bound for every interleaving arity `mu`.

This lower bound first reaches seven at

```text
a = 291,
```

since

```text
floor(257 / (291-255)) = floor(257/36) = 7.
```

Therefore the packet proves a separate interleaved-list lower-bound candidate

```text
Lambda_mu(C,291) >= 7.
```

This is not an MCA row and not a protocol statement.  It is a standard
interleaved-list lower bound over denominator `|F|=17^32`.

## Descent Ledger

The scanner records:

```text
384..512 : Lambda_mu = 1                         PROOF_RECORD
373..383 : Lambda_mu <= 6                        ROUTE_CUT
372..292 : packing permits 7, root-pencil < 7    PARTIAL
291      : root-pencil lower bound = 7           LOWER_ONLY
```

The phrase `LOWER_ONLY` is intentional: the exact value at `a=291` is not
claimed.  The lower bound is enough for the interleaved-list gate.

## Status Ledger

PROVED:

- high-agreement uniqueness for `384 <= a <= 512`;
- packing route cut `Lambda_mu(C,a) <= 6` for `373 <= a <= 383`;
- root-pencil lower bound `Lambda_mu(C,291) >= 7`;
- all counts use the interleaved-list denominator `|F|=17^32`.

PARTIAL:

- `372 <= a <= 292`: seven witnesses are not excluded by the packing test, but
  the root-pencil lower bound is below seven.

NOT CLAIMED:

- no MCA `N_bad`;
- no protocol soundness failure;
- no ordinary list-decoding failure beyond the stated predicate;
- no exact `Lambda_mu` values in the partial interval;
- no exact `delta*_C`.

## Validation

Run:

```bash
python3 experimental/scripts/scan_m1_interleaved_list_threshold_descent.py
python3 experimental/scripts/verify_m1_interleaved_list_threshold_descent.py
python3 experimental/scripts/verify_m1_interleaved_list_threshold_descent.py --json
python3 -m json.tool experimental/data/m1_interleaved_list_threshold_descent.json
```
