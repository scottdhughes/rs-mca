# `c=0` fixed-residual `q=64` periodic lanes: exact three-invariant Hahn payment

## Status

```text
COMPLETE PAYMENT OF EVERY FIXED-RESIDUAL q64 FULL-BLOCK PERIODIC LANE
NOT A SUM OVER RESIDUAL SUPPORTS
NOT A UNIFORM c=0 PROJECTIVE-RESIDUE FLATNESS THEOREM
NOT AN OFFICIAL PAYMENT
```

Put `B=32,768`.  If a degree-`t` support has a fixed residual part `R` and
`f` variable complete `mu_B` cosets, then

```text
0<=f<=floor(t/B)=29.
```

Because the locator of `R` has nonzero constant coefficient, it is a unit
modulo `X^a`.  Canceling it in the periodic congruence leaves the exact
finite map

```text
S in binom(Omega_R,f) subseteq binom(mu_64,f)
  |-> (P_S,U_S,V_S)
     in mu_64 x F_p x F_p,

P_S=product_(y in S)y,
U_S=sum_(y in S)y^(-1),
V_S=sum_(y in S)y^(-2).
```

Here `Omega_R` deletes every quotient coset already touched by `R`.
Embedding it in the full `mu_64` only enlarges every fiber.

This note proves exact weight-specific fiber caps whose maximum is

```text
max_(0<=f<=29) max_(P,U,V)
 #{S in binom(mu_64,f): (P_S,U_S,V_S)=(P,U,V)}
 <=25,307,496.                                         (1)
```

The prior sufficient fixed-scalar ceiling was

```text
floor(T/(p-1))=128,996,705.
```

Thus (1) pays every scalar cell in every fixed-residual full-block lane.
Paying all `p-1` nonzero scalar cells is already sufficient:

```text
(p-1)*25,307,496
 =53,922,844,505,014,272
 <T=274,854,110,496,187,592,

margin=220,931,265,991,173,320.                        (2)
```

There is also a sharper narrow-lane overcount.  The constant coefficient of
the quotient locator is `-P_S in mu_64`; therefore one projective residue
ray meets a fixed-residual periodic image in at most 64 scalar cells.  Hence

```text
64*25,307,496=1,619,679,744<T.                         (2a)
```

The source and finite-classification pins are

```text
work/DEPLOYED_C0_Q64_PERIODIC_FIXED_Q_REDUCTION.md
sha256=8b2d84ffb344bbb0a78c904358645322f5159c20c152760ea7cd97354228fc69

work/PROFILE1792_MU64_SHORT_TRADES_SQL_OUTPUT.txt
sha256=58780e11b9c45d507e1daacbcb5be2548b82228bfe38e3e5c4e2d9f412211416

work/HOSTILE_AUDIT3_MU64_DISTANCE7_GAP_ORBIT_CENSUS.md
sha256=3542ad6a7f394fe7a0bae5d45c12598a045768997497448145976fff64e2b43a

work/PROFILE1792_MU64_SIZE8_TRADE_CLASSIFICATION.md
sha256=143341369f91a8965960d943a520ea0eb410b1ac5b82e7d447968dac9ebfa19e

work/PROFILE1792_MU64_SIZE9_TRADE_CENSUS.md
sha256=ebe4101c29d00cb4354b1cce6291b4640a4e457b69827c012dbdda292c5a7690

work/mu64_size9_two_moment_records_compact.analysis.json
sha256=3686fa22df3d93e85bb660f81667182e45ed2ec9c3cdf4b1aa8e3685eaf959b5
```

No live return or live PR is consumed.

## 1. Exact distance translation

Let `E,F` be two distinct `f`-subsets in one fiber and put

```text
A=E\F,       B=F\E,       |A|=|B|=s.
```

Canceling their common elements gives

```text
product_(a in A)a = product_(b in B)b,
sum_(a in A)a^(-1)=sum_(b in B)b^(-1),
sum_(a in A)a^(-2)=sum_(b in B)b^(-2).                 (3)
```

Inversion permutes `mu_64`.  In odd characteristic, equality of the first
two power sums is equivalent to equality of the first two elementary
symmetric functions.  Therefore the inverse wings in (3) are a disjoint
equal-`(e_1,e_2)` trade, with equal product as an additional constraint.

The complete deployed finite classifications give:

- no disjoint equal-two-moment trade for `s=1,2,3`;
- for `s=4`, both wings are distinct full `mu_4` cosets;
- no disjoint equal-two-moment trade for `s=5,6,7`;
- for `s=8`, each wing is a union of two full `mu_4` cosets;
- for `s=9`, there are exactly 55 rotation-orbit representatives and every
  literal wing belongs to exactly one of the 3,520 two-moment trades.

Distinct `mu_4` cosets have distinct products, so (3) deletes the `s=4`
trades.  Hence every fiber code has minimum Johnson distance at least eight.

## 2. Pointwise distance-eight caps

Label the sixteen `mu_4` cosets by `Z/16Z`.  The product of the coset with
label `i` has exponent `4i+32 modulo 64`.  At distance eight, the size-eight
classification and (3) say that a pair of full selected cosets `{i,j}` can
be exchanged for a pair of full empty cosets `{k,l}` exactly when

```text
i+j == k+l modulo 16.                                  (4)
```

A weight-`f` subset contains at most `floor(f/4)` full cosets and its
complement contains at most `floor((64-f)/4)` full cosets.  Enlarging either
label set only adds solutions of (4).  The verifier exhausts the maximal
disjoint full/empty label sets for all `8<=f<=29`: 606,060 states in total.
The pointwise `A_8` caps, in weight order `8..29`, are

```text
7,6,6,6,18,16,16,16,32,28,28,28,46,40,40,40,59,52,52,52,72,72.
```

In particular

```text
A_8<=72.                                               (5)
```

## 3. The pointwise distance-nine cap

For each of the 55 accepted size-nine two-moment trade-orbit
representatives, the replay recomputes the exponent sum of both wings.
Exactly one orbit also has equal product.  Product equality is preserved by
rotation, and each size-nine two-moment wing lies in exactly one accepted
trade.  Thus the complete full-three-invariant distance-nine trade universe
has 64 literal unordered pairs.  For every weight under consideration,

```text
A_9<=64.                                               (6)
```

This deliberately pays the whole literal trade universe rather than
claiming that only one trade can cross a fixed support.

## 4. Exact Hahn certificates

For each `8<=f<=29`, normalize the Hahn polynomials of `J(64,f)` by

```text
H_j(i)=sum_(q=0)^j
 (-1)^q binom(j,q)binom(65-j,q)binom(i,q)
 /[binom(f,q)binom(64-f,q)],

H_j(0)=1.
```

The verifier constructs

```text
F_f(i)=1+sum_(j=1)^m c_(f,j) H_j(i)                   (7)
```

from the following zero sets:

```text
f : zero set
8 : empty
9,10 : 9
11 : 10,11
12 : 10,12
13,14 : 10,12,13
15 : 10,12,13,15
16,17 : 10,12,13,15,16
18 : 10,12,13,15,16,18
19 : 10,12,13,15,16,19
20,21 : 10,12,13,15,16,18,19
22 : 10,12,13,15,16,18,19,22
23 : 10,12,13,15,16,18,19,21,22
24,25 : 10,12,13,15,16,18,19,20,21
26 : 10,12,13,15,16,18,19,20,21,26
27 : 10,12,13,15,16,18,19,21,22,27
28 : 10,12,13,15,16,18,19,21,22,26,27
29 : 10,12,13,15,16,18,19,20,21,24,25.               (8)
```

All coefficients are positive.  Their complete canonical rational stream
has digest

```text
6b9fdd32619e2fd8ae53b05ac16de82e6c532bc18afecbeafda3fc66187d1d20.
```

Exact evaluation gives

```text
F_f(i)<=0 for every 10<=i<=f.                          (9)
```

For a weight-`f` fiber code of size `M`, let `A_i` be its average Johnson
distance distribution, so `A_0=1` and `sum_i A_i=M`.  Delsarte positivity
and (5)--(9) give

```text
M<=F_f(0)+A_8 max(F_f(8),0)+A_9 max(F_f(9),0).         (10)
```

For weights `0..7`, the cap is one because maximum Johnson distance is below
eight.  For weights `0..29`, the exact integer caps are

```text
1,1,1,1,1,1,1,1,
8,11,26,91,220,516,1091,3093,10217,20908,57196,145025,
296899,614503,1241710,2465809,3954000,6287643,10193410,
14641173,20826085,25307496.                            (11)
```

The last is the maximum.  Its exact rational predecessor is

```text
7162373179063296/283013891=25,307,496.9350... .        (12)
```

This proves (1), and (2)--(2a) follow by exact integer arithmetic.

## Scope and nonclaims

For the original 29-full-block construction this theorem replaces the old
upper endpoint `164,629,954,331,472` by `25,307,496`.  More generally, it
pays every fixed residual support and every possible count zero through 29
of variable full blocks.  It consumes the actual product and two moment
values; it is not a support-only Hahn argument.

It does **not** sum over different residual supports.  It does not bound all
degree-`t` split locators modulo an arbitrary monic `g` of degree 67,472, or
cover general factorization strata.  It therefore does not prove the uniform
factor `4,224,290`, the complete `c=0` theorem, any `c>0` theorem, or an
official score.

## Replay

```bash
ruby --disable-gems -w work/verify_c0_q64_three_invariant_hahn_payment.rb
```
