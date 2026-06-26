# Tangent-star barrier: no seventh non-tangent slope past agreement 506

## Status

PROVED / NEW-LOCAL finite MDS theorem, under the finite-slope support-wise MCA convention.

This note addresses the follow-up target: decide whether a non-tangent mechanism can survive past agreement `507` for

```text
C = RS[F_17^32, H, 256],  |H| = 512.
```

## Main theorem

Let `C` be an MDS linear code of length `n` and dimension `k`. For agreement `a`, let

```text
LD_sw(C,a)
```

be the maximum number of finite support-wise noncontained bad slopes at agreement at least `a`.

For every `k+1 <= a <= n`, the moving-root tangent construction gives

```text
LD_sw(C,a) >= n-a+1.
```

If additionally

```text
3a - 2n >= k,
```

then this is optimal:

```text
LD_sw(C,a) = n-a+1.
```

Moreover, equality forces a tangent-star structure: an extremal line has a common code-line support `S0` of size `a-1`, and every bad slope is obtained by moving one residual root outside `S0`. Thus in the exact range there is no separate non-tangent branch that can add more bad slopes.

## Application to the current row

For

```text
n = 512, k = 256,
```

the exact range starts at

```text
a >= ceil((2n+k)/3) = 427.
```

Therefore, for every `a >= 427`,

```text
LD_sw(C,a) = 513-a.
```

In particular:

```text
LD_sw(C,506) = 7,
LD_sw(C,507) = 6.
```

Since

```text
6 * 2^128 < 17^32 < 7 * 2^128,
```

agreement `507` is within the `2^-128` finite-slope MCA budget, while agreement `506` is already outside it.

On the integer Hamming-radius grid:

```text
radius 5  is safe,
radius 6  is unsafe.
```

In normalized radius:

```text
5/512 is safe on the closed grid,
6/512 is the first unsafe closed radius.
```

With a real supremum convention, the safe radius approaches `6/512` from below but does not include it.

## What this settles

For the `F_17^32`, `n=512`, `k=256` row, no non-tangent finite-slope support-wise MCA mechanism can add a seventh bad slope at agreement `a >= 507`.

## What this does not settle

This does not prove a CA, curve-MCA, projective-slope, interleaved-list, ordinary-list, SNARK, or protocol theorem. Those require separate conversion and field-ledger checks.
