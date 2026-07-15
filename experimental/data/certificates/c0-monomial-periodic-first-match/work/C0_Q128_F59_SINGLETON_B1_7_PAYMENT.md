# `c=0`, `g=X^a`: the `q=128`, `f=59`, singleton-occupancy `b<=7` payment

## Exact result

Put

```text
p=2,130,706,433,
n=2,097,152,
t=981,105,
a=67,472,
B=16,384,
t=59B+14,449,
a=4B+1,936.
```

For a support having exactly 59 complete `q=128` fibers, write its unique
locator as

```text
L(X)=A(X)Q_S(X^B),
deg A=14,449<B,
Q_S(Y)=product_(y in S)(Y-y),
S subset mu_128, |S|=59.                              (1)
```

Inside one projective residue ray modulo `X^a`, the monic residual locator
`A` is fixed.  After fixing the constant coefficient of `Q_S`, the first
four inverse power sums of `S` are fixed.  Pair `mu_128` by `x<->-x`, and
let `b` be the number of singleton pairs in `S`.  Since `|S|=59`, write

```text
b+2d=59,
```

where `d` is the number of double pairs.  Then the union of the four cells

```text
(b,d)=(1,29),(3,28),(5,27),(7,26)                    (2)
```

has, in one projective residue ray, at most

```text
128*(
      1*25,307,496
     +42*20,826,085
     +34,137*14,641,173
     +12,598,400*10,193,410)
=16,501,934,370,530,176
<T=274,854,110,496,187,592.                           (3)
```

The exact margin is

```text
258,352,176,125,657,416.                              (4)
```

The already treated coarse `q=64` strata have an exact relation to (2):
`b=1` is coarse `f=29`, `b=3` is coarse `f=28`, `b=5` is the first
coarse `f=27` cell, and `b=7` is coarse `f=26`.  Therefore, under a
coarse-first first-match rule which has already deleted `f=29,28`, the
genuinely new disjoint contribution is only `b=5,7`, and its cap is

```text
128*(34,137*14,641,173+12,598,400*10,193,410)
=16,501,819,170,137,728<T.                            (5)
```

No overlapping `b=1,3` payment is added in (5).

Pinned input:

```text
work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md
sha256=99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b

work/verify_c0_q64_three_invariant_hahn_payment.rb
sha256=baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5

work/verify_c0_q64_three_invariant_hahn_payment.expected.txt
sha256=28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1
```

No live return or live PR is consumed.

## 1. Projective ownership and the four normalized invariants

Write

```text
Q_S(Y)=q_0+q_1Y+...+Y^59,       q_0!=0.
```

Reduction of (1) modulo `X^B` is exactly `q_0 A`.  If `L,L'` lie in one
projective residue ray, then

```text
q_0 A = c q'_0 A'                              mod X^B. (6)
```

Both `A,A'` are monic of degree `14,449<B`, so (6) is an equality of
polynomials and fixes `A=A'` after comparison of leading coefficients.
Because `A(0)!=0`, it is a unit in `F_p[X]/(X^a)`, and may be cancelled from
the projective congruence.  Since

```text
4B<a<5B,
```

the normalized coefficients

```text
q_j/q_0,       1<=j<=4                               (7)
```

are fixed throughout the ray.  Explicitly,

```text
Q_S(Y)/q_0
 =product_(y in S)(1-Y/y)
 =sum_(j=0)^59 (-1)^j e_j(S^(-1))Y^j.                (8)
```

Thus (7) fixes `e_1,...,e_4` of the inverse roots.  Newton's identities
fix the inverse power sums

```text
p_k(S)=sum_(y in S)y^(-k),       1<=k<=4.             (9)
```

The distinction between a projective ray and an absolute scalar cell is
load-bearing here.  The constant coefficient is

```text
q_0=(-1)^59 product_(y in S)y in mu_128.              (10)
```

It is not fixed by (7), but it has only 128 possible values.  We first
count one fixed value of (10), and multiply by 128 only at the end.

## 2. The antipodal decomposition

For each double pair `{x,-x}` put `z=x^2 in mu_64`; let `D` be the set of
its `d` labels.  Let `T_sing` be the set of the `b` singleton roots.  It
contains no antipodal pair.  The odd inverse power sums in (9) receive no
contribution from the double pairs, hence every support in one absolute
scalar cell satisfies

```text
sum_(x in T_sing)x^(-1)=constant,
sum_(x in T_sing)x^(-3)=constant.                    (11)
```

For a fixed singleton set, the remaining even sums and product give

```text
product_(z in D)z=constant,
sum_(z in D)z^(-1)=constant,
sum_(z in D)z^(-2)=constant.                         (12)
```

Signs such as `product {x,-x}=-z` only alter the fixed constant in (12).
The forbidden pair labels touched by `T_sing` may be restored to the
ambient `mu_64`; this only enlarges a fiber.  Therefore the accepted
all-weight `q=64` Hahn theorem bounds the number of possible `D` by

```text
d=29: 25,307,496,
d=28: 20,826,085,
d=27: 14,641,173,
d=26: 10,193,410.                                    (13)
```

## 3. Exact two-odd-moment singleton certificate

Invert the singleton roots, so a candidate is a `b`-subset `U` of
`mu_128`, with no antipodal pair, and with fixed

```text
sum_(u in U)u,       sum_(u in U)u^3.                 (14)
```

Any `(b-2)`-subset `W` of `U` determines the two omitted roots.  Indeed,
if they are `u,v`, (14) determines

```text
s=u+v,       h=u^3+v^3.
```

The case `s=0` is impossible because it would give the antipodal pair
`v=-u`.  Since `p` is not three, the identity

```text
u^3+v^3=s^3-3uvs
```

therefore determines `uv=(s^3-h)/(3s)`.  The unordered pair `{u,v}` is
the root set of `Z^2-sZ+uv`, and is unique.  Consequently the
`(b-2)`-subset certificates belonging to distinct singleton sets are
disjoint, and

```text
H_b<=floor(C(128,b-2)/C(b,2)).                        (15)
```

At the four values in (2), this gives exactly

```text
H_1=1,
H_3=floor(C(128,1)/3)=42,
H_5=floor(C(128,3)/10)=34,137,
H_7=floor(C(128,5)/21)=12,598,400.                   (16)
```

Multiplying (13) and (16), summing the disjoint occupancy cells, and then
paying the 128 possible constants (10) proves (3).  Deleting `b=1,3`
before summation proves the first-match form (5).

## 4. Exact coarse `q=64` relation

A double antipodal pair of complete `q=128` fibers is one complete
`q=64` fiber.  A singleton contributes one complete child but not its
antipodal child.  The original residual has only 14,449 roots, fewer than
one `q=128` fiber, so it cannot complete a missing child.  Hence the coarse
full-fiber count is exactly `d` and the coarse residual degree is

```text
14,449+b*16,384.
```

For `b=1,3,5,7` these degrees are respectively

```text
30,833, 63,601, 96,369, 129,137,
```

which proves the claimed `q64 f=29,28,27,26` routing without overlap.

## Scope and nonclaims

- This is uniform over every distribution of the fixed 14,449-root
  residual and every projective residue ray for `g=X^67,472`.
- It pays all `q128 f=59` supports with singleton occupancy `b<=7`.
- Under the explicit coarse-first rule, only `b=5,7` is new; the theorem
  does not add `b=1,3` twice.
- It does **not** pay the still-open `b>=9` part of `q128 f=59`.
- It does not pay `q128 f=54..58`, general monic `g`, all of `c=0`, or an
  official question.

## Replay

```bash
ruby --disable-gems -w work/verify_c0_q128_f59_singleton_b1_7_payment.rb
```
