# Two-level centered support-flag router

## 1. Frozen record interface

Use the KoalaBear row

```text
n=2097152, K=1048576, m=1116048, w=m-K=67472,
B*=274980728111395087, 2w=134944.
```

After the reversible error-rank gauge, let `C'` be the fixed explanation
direction code, with `s=dim C'<=10`.  For every selected post-near slope,
freeze one actual minimizing pair

```text
e=(a_e,b_e) in (c_0+C') x C'
```

once and before any margin cutoff.  Write

```text
H_e={x:r_0(x)=a_e(x), r_1(x)=b_e(x)}
```

for its complete pair core.

The parent nonuniform-margin theorem gives

```text
sum_gamma theta_gamma <= C_10,
C_10=106618568137036225644.                         (1)
```

For a record assigned to `e` with `theta_gamma<=tau<w+1`, truncation is
inactive and its exact size-`m` support meets `H_e` in `m-theta_gamma`
coordinates.  Hence

```text
|H_e| >= m-theta_gamma.                             (2)
```

## 2. Dense center pair

Apply the parent weighted minimizing-pair theorem to the same frozen pair
selection at cutoff `1795`.  Exact replay gives one actual pair `e_*` with
weighted load `360132809` and at least

```text
ceil(360132809/1795)=200632
```

owned records.  The fixed-pair capacity at core deficiency five is only
`351431811`, below the forced weight, whereas deficiency four has capacity
`439536384`.  Thus

```text
|H_*| >= m-4=1116044.                               (3)
```

Fix any subset

```text
G_* subset H_*, |G_*|=H0=1116044.                  (4)
```

This makes the later count independent of whether the complete center core is
larger.

## 3. Low-margin pair-difference subcodes

Set

```text
tau=1936,
A=m-tau=1114112,
h=H0+A-n=133004.                                    (5)
```

Let `L` be the records with `theta_gamma<=tau`.  Every pair type appearing in
`L` satisfies `|H_e|>=A`.  Therefore

```text
|G_* intersect H_e| >= H0+A-n=h.                   (6)
```

For a noncenter pair type define

```text
U_e=span{a_e-a_*, b_e-b_*} <= C'.                  (7)
```

The pair types are distinct, so `dim U_e` is one or two.  Every word in `U_e`
vanishes on `G_* intersect H_e`; hence `U_e` has at least `h` common zeros in
`G_*`.

For a subcode `V<=C'`, write

```text
Z_*(V)={x in G_*:v(x)=0 for every v in V}.          (8)
```

Fix the two support thresholds

```text
Z2=117731, Z3=23354.                                (9)
```

The target terminal is:

> an actual noncenter low pair `e` and a three-dimensional subcode
> `W<=C'` such that `U_e<=W` and `|Z_*(W)|>=Z3`.

We prove the slope bound under the negation of this terminal.

## 4. Canonical container assignment

Fix an order on the subspaces of `C'` induced by the chosen basis.

- If `dim U_e=2`, assign `e` to the two-plane `V_e=U_e`; it has at least
  `h>Z2` common zeros.
- If `dim U_e=1` and some two-plane `V` containing `U_e` has at least `Z2`
  common zeros, assign `e` to the first such `V`.
- Otherwise assign `e` to the terminal line `U_e`.

This is a disjoint assignment of pair types.  Under the negation of the target
terminal, no assigned line or plane is contained in a three-dimensional
subcode having `Z3` common zeros.

## 5. Counting terminal lines

Let `U` be a terminal line and put `A_U=U^perp<=(C')^*`, of dimension `s-1`.
For `x in Z_*(U)`, the evaluation normal `ell_x` lies in `A_U`.
There are at least `h` such coordinate normals.

Any hyperplane `B<A_U` is the annihilator of a two-plane `V>U`.  Since `U`
is terminal, at most `Z2-1` of the selected coordinate normals lie in `B`.
Any subspace of `A_U` of codimension at least two is contained in the
annihilator of a three-dimensional subcode containing `U`; under the target
negation it contains at most `Z3-1` selected normals.

Choose an ordered basis of `A_U` from coordinate normals.  For the first
`s-2` choices, the current span has codimension at least two and there are at
least

```text
c13=h-Z3+1=109651                                    (10)
```

choices.  For the final choice, there are at least

```text
c12=h-Z2+1=15274.                                    (11)
```

Thus every terminal line owns at least

```text
c12*c13^(s-2)
```

ordered coordinate bases.  There are at most `H0 falling (s-1)` ordered
coordinate tuples globally, and a basis determines its span `A_U` and hence
`U`.  Therefore

```text
N1(s) <= floor(H0 falling (s-1)/(c12*c13^(s-2))).   (12)
```

## 6. Counting two-plane containers

Let `V` be an assigned two-plane and put `A_V=V^perp`, of dimension `s-2`.
At least `Z2` coordinate normals lie in `A_V`.  Every proper subspace of
`A_V` is contained in a hyperplane, which is the annihilator of a
three-dimensional subcode containing `V`.  Under the target negation it
contains at most `Z3-1` selected normals.

Every one of the `s-2` ordered basis choices therefore has at least

```text
c23=Z2-Z3+1=94378                                    (13)
```

options.  Hence

```text
N2(s) <= floor(H0 falling (s-2)/c23^(s-2)).          (14)
```

Repeated evaluation directions and zero normals are included: coordinates,
not distinct projective normals, are counted.  The finite exhaustive controls
verify this multiplicity-sensitive point.

## 7. Pair types and slopes inside a container

All pairs assigned to a fixed `r`-dimensional container (`r=1` or `2`) lie in
two affine copies of the same `r`-dimensional Reed--Solomon direction code and
have common pair agreement at least `A`.  The parent ordinary affine-span
bound and sub-square interleaving collapse give

```text
Q_r=floor(C(n-K+r,r)/C(A-K+r,r)).                    (15)
```

Here

```text
Q1=15, Q2=255, Q2^2=65025<2130706433^6.             (16)
```

A fixed pair core of size at least `A` owns at most

```text
P=n-A=983040                                         (17)
```

distinct slopes by the same-support exception-coordinate injection.  The
center pair is reserved once separately.  Consequently, for `3<=s<=10`,

```text
|L| <= (N1(s)Q1+N2(s)Q2)P+P.                        (18)
```

For `s<=2`, the direct `Q2*P+P` bound is stronger.  Exact evaluation shows
that the right side of (18) is increasing through `s=10`; at that endpoint,

```text
N1=8415196932,
N2=382360905,
|L|<=219935524214538240.                             (19)
```

## 8. High margin and exact row total

By (1), the high-margin records satisfy

```text
|H|<=floor(C_10/(tau+1))
    =55043143075392992.                              (20)
```

Adding (19), (20), and the disjoint near-rational charge gives

```text
|Z_bad| <= 134944
          +55043143075392992
          +219935524214538240
        =274978667290066176
        <274980728111395087=B*.                      (21)
```

The slack is `2060821328911`.

We have proved the contrapositive: an over-budget line forces an actual low
pair `e` and a three-dimensional `W<=C'` with `U_e<=W` and
`|Z_*(W)|>=23354`.

## 9. Exact adjacent wall

Keep `tau=1936` and replace `Z3` by `23355`.  Exhaustively scan every legal
integer `Z2`.  The unique best value remains `117731`, but the resulting
numbers are

```text
low  =219952702956503040,
total=274995846032030976,
over =15117920635889.                                (22)
```

Thus `23354` is the exact adjacent common-zero threshold for this declared
profile.  This is a method wall, not a counterexample to a stronger
support-flag or chronology theorem.

## 10. Nonclaims

The forced three-dimensional subcode is not asserted to own a specified
number of slopes, to be unique, or to be an active-v4 owner.  No common
locator is cancelled across unrelated pair edges.  Rank eleven and the
KoalaBear row remain open.
