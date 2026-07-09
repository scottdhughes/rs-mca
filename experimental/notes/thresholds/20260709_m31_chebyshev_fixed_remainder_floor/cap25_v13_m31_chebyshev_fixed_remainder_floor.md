# CAP25 v13 M31 Chebyshev fixed-remainder floor

Status: `BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT`.

This note records a narrow hostile-audited computation for the deployed
Mersenne-31 list row in the CAP25 v13 finite-adjacent program. It does not prove
the adjacent safe row, does not give a counterpacket, and does not close
row-sharp Q. Its value is to replace a loose "M31 symmetry" intuition by one
exact Chebyshev fixed-remainder floor and the resulting residual target.

## Board anchor

The live finite goal remains the adjacent certificate

```text
U(a0 + 1) <= B* < L(a0).
```

For the Mersenne-31 list row:

```text
p        = 2^31 - 1
n        = 2^21
k        = 2^20
a+       = 1116023
w        = a+ - k = 67447
B*       = 2^24 - 1 = 16777215
avg_ceil = ceil(binomial(n, a+) / p^w) = 1993678
```

Thus the full max-fiber target has only

```text
log2(B* / avg_ceil) = 3.072998926581202 bits
```

of visible overhead.

## Domain correction

The Mersenne-31 row should not be treated as a multiplicative-root coset in
`F_p^*`. The usable finite symmetry is the Chebyshev / twin-coset structure of
the line-round row. Consequently, multiplicative mode-at-null or primitive
orbit heuristics are not theorem-facing inputs for this deployed row.

The relevant dyadic operation is the Chebyshev fold at scale `c=2^j`. For a
fixed remainder class inside one fold fiber, the induced quotient problem has
parameters

```text
N_c = n / c
f_c = floor(a+ / c)
r_c = a+ mod c
t_c = floor(w / c)
```

and, when `r_c > 0`, one quotient point is reserved by the fixed remainder
choice. The fixed-remainder lower floor used here is

```text
F_c = ceil(binomial(N_c - 1, f_c) / p^t_c).
```

This is a lower-floor / residual-target computation, not an upper ledger.

## Exact replay values

For the list row, the largest fixed-remainder dyadic floor among
`c=2^j`, `0 <= j <= 20`, is at `c=2048`:

```text
c     = 2048
N_c   = 1024
f_c   = 544
r_c   = 1911
t_c   = 32
F_c   = ceil(binomial(1023, 544) / p^32) = 6796405
```

This consumes about `40.51%` of the budget:

```text
B* - F_2048                  = 9980810
log2(B* / F_2048)            = 1.303659518930735 bits
log2((B* - F_2048)/avg_ceil) = 2.3237244851910264 bits
```

For comparison, the already printed Mersenne-31 MCA watch item is

```text
ceil(binomial(1024, 545) / p^32) = 12769758
B* - 12769758                    = 4007457
```

The hostile audit also replayed the naive dyadic fixed-remainder sum

```text
sum_{0 <= j <= 20} F_{2^j} = 16548620
B* - sum_j F_{2^j}          = 228595
```

This is not a counterpacket, because no theorem currently co-locates those
dyadic floors in one target fiber and no additivity/stacking theorem is being
claimed here. It is only a sharp warning that the finite margin is extremely
thin if a future chaining theorem exists.

### Follow-up 3x3 residual-flatness audit

A subsequent hostile audit of the chained-target residual made the warning
more precise. Removing only the selected `c=2048` floor leaves

```text
B* - F_2048 = 9980810.
```

The remaining printed dyadic floors sum to

```text
sum_{j != 11} F_{2^j} = 9752215
(B* - F_2048) - sum_{j != 11} F_{2^j} = 228595.
```

Thus the same `228595` gap remains after conditioning on the best floor. This
still does not prove a counterpacket: lower floors are not upper-ledger
payments, and the available Chebyshev tower structure points toward nested or
absorbed dyadic subfamilies rather than disjoint additive stacking.

The exact coarser tail above the best scale is tiny:

```text
sum_{c > 2048} F_c = 6880.
```

So the next live obstruction is not the coarser tower. It is the immediate
finer scale `c=1024`, where

```text
c     = 1024
N_c   = 2048
f_c   = 1089
r_c   = 887
t_c   = 65
F_c   = ceil(binomial(2047,1089) / p^65) = 1144150.
```

Inside the `c=1024` quotient, the already selected `c=2048` packet has the
paired form

```text
Q_pair(Y) = (Y - eta) P(T_2(Y)),    deg P = 544,    deg Q_pair = 1089.
```

The next theorem-facing target is therefore narrower than the original
chained-flatness slogan:

```text
CAP25-V13-M31-C1024-PAIRED-PREFIX-PRIMITIVE-Q.

Fix the c=2048 planted target. In the c=1024 quotient, bound the number of
degree-1089 split locators Q(Y) with the first 65 quotient-prefix coefficients
equal to the paired prefix induced by Q_pair(Y), excluding factor-through forms;
or exhibit a heavy non-factor-through paired-prefix fiber.
```

An equivalent incidence route is:

```text
M31-PLANTED-RESIDUAL-SHIFT-PAIR-INVERSE.

If the residual exceeds 9980810, force many planted-residual shift-pair
incidences in one distance stratum, then prove that the incidences enter a
paid cell or build an explicit counterpacket.
```

## Surviving lemma

The bankable local lemma is:

```text
CAP25-V13-M31-CHEBYSHEV-FIXED-REMAINDER-FLOOR.

In the Mersenne-31 list row, the c=2048 Chebyshev fixed-remainder quotient
floor contributes an exact lower floor of 6796405 to the corresponding planted
target condition, under the fixed-remainder convention above.
```

The exact arithmetic is replayed by
`m31_chebyshev_fixed_remainder_floor.py`.

## Nonclaims

This note does not claim:

- `U(1116023) <= B*`;
- row-sharp Q for the Mersenne-31 list row;
- a counterpacket to the Mersenne-31 list adjacent candidate;
- a proof that dyadic fixed-remainder floors stack additively;
- a finite safe-side certificate for any of the four deployed rows.

## Next exact target

The next theorem-facing obstruction is a planted-conditioned residual
flatness/chaining statement:

```text
CAP25-V13-CHEBYSHEV-CHAINED-TARGET-RESIDUAL-FLATNESS.

After conditioning on the c=2048 fixed-remainder planted floor in the
Mersenne-31 list row, prove that the remaining primitive residual target mass
is at most 9980810, or exhibit a co-located dyadic-chain counterpacket.
```

Equivalently, the residual family must fit inside only
`2.3237244851910264` bits above the identity average. This is now the sharper
M31-list finite audit target.

The 3x3 residual audit refines this broad target to the `c=1024`
paired-prefix primitive Q problem above. Any future use of the dyadic floors
must first prove co-location/additivity, or else work directly in that
paired-prefix quotient slice.
