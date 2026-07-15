# `c=0`, `g=X^a`: complete `f=28` residual-pencil payment

## Exact result

At the deployed constants

```text
B=32,768,
t=981,105=28B+63,601,
a=67,472=2B+1,936,
n=2,097,152,
```

consider the canonical stratum of supports having exactly 28 complete
quotient fibers

```text
C_y={x in H:x^B=y},       y in mu_64.
```

For the monomial first-hard modulus `g=X^a`, all
residual locators arising inside one projective residue ray lie in one
projective pencil.  If the ray contains two distinct residual supports, the
pencil has at most `30,833` deployed base roots and hence at most

```text
63
```

split members.  Combining this owner cap with the fixed-residual
three-invariant Hahn cap at weight 28 gives

```text
N_(f=28)(one projective residue ray)
 <=63*64*20,826,085
 =83,970,774,720
 <T=274,854,110,496,187,592.                           (1)
```

Together with the separately proved `f=29` cap, the complete top two
canonical strata obey

```text
N_(f in {28,29})(one projective residue ray)
 <=83,970,774,720+1,619,679,744
 =85,590,454,464
 <T,                                                       (2)

margin=274,854,024,905,733,128.
```

Equation (2) is valid even if one ray contains both `f=28` and `f=29`
locators: the canonical full-block count partitions the locators, so the two
independent caps may be added.  No cross-stratum ownership assertion is
needed.

Pinned inputs:

```text
work/C0_Q64_THREE_INVARIANT_HAHN_PAYMENT.md
sha256=99fa4b6c53657e3aecc52c19d7830f509955dc43cf18351c58232b35336d915b

work/verify_c0_q64_three_invariant_hahn_payment.rb
sha256=baf78eb9a8e297220bf69484f110bc108f88fb083d1e0693e05f570fa76722a5

work/verify_c0_q64_three_invariant_hahn_payment.expected.txt
sha256=28cd93bf4472d29537a267a7c84360f6f7c26eb9795aa4758e2a105383dcbba1

work/C0_Q64_F29_PROJECTIVE_RESIDUAL_OWNER_PAYMENT.md
sha256=704524424be7dc8b411a71011f8f8eb63ae88f9e7f4ebcfd100420e23c322ad5

work/verify_c0_q64_f29_projective_residual_owner_payment.rb
sha256=52c95bdcf544081281a2590e653320db7d59efd3ca193687160802bcb7dc5478

work/verify_c0_q64_f29_projective_residual_owner_payment.expected.txt
sha256=2d296032abd51cafafd7f46cb23bf4db0d1f8c99e7e015c20d26fe0a40c06543
```

## 1. Two-block normal form

Write a residual locator in the `f=28` stratum uniquely as

```text
A_i(X)=A_(i,0)(X)+X^B A_(i,1)(X),                     (3)

deg A_(i,0)<B,
deg A_(i,1)=m=63,601-B=30,833,
A_(i,1) monic.
```

The constant coefficient of `A_(i,0)` is nonzero because every residual
root lies in `H subset F_p^*`.  Write the quotient locator as

```text
Q_i(Y)=q_(i,0)+q_(i,1)Y+...,
q_(i,0)!=0,
lambda_i=q_(i,1)/q_(i,0).                             (4)
```

The complete locator is

```text
L_i=A_i Q_i(X^B).                                      (5)
```

Fix one member `i=0`.  Since all members lie in one projective residue ray
modulo `X^a`, choose `c_i!=0` with

```text
L_i == c_i L_0 modulo X^a.                             (6)
```

Because `a>2B`, equations (3)--(6) identify the complete coefficient blocks
of degrees `0..B-1` and `B..2B-1`.  Put

```text
s_i=c_i q_(0,0)/q_(i,0),
U=A_(0,0),
V=A_(0,1).
```

The first block of (6) gives

```text
A_(i,0)=s_i U.                                         (7)
```

The second block gives

```text
A_(i,1)+lambda_i A_(i,0)
 =s_i(V+lambda_0 U),
```

and hence

```text
A_i
 =s_i [ U+X^B V+(lambda_0-lambda_i)X^B U ].            (8)
```

Thus every residual locator is a monic representative of the projective
pencil

```text
P+theta D,
P=U+X^B V,
D=X^B U.                                               (9)
```

The two pencil generators are independent because `U(0)!=0`, while
`D(0)=0`.  Distinct residual supports give distinct parameters.

## 2. Base-root and split-member cap

If `deg U>m`, then (8) and `deg A_(i,1)=m` force

```text
lambda_i=lambda_0
```

for every member.  Monicity then forces `s_i=1`, so (7)--(8) give
`A_i=A_0`.  Therefore a pencil with at least two distinct residual supports
necessarily has

```text
deg U<=m=30,833.                                       (10)
```

Let `c` be the number of deployed roots common to the whole pencil.  At a
deployed root `x`, the direction in (9) vanishes only if `U(x)=0`, because
`x!=0`.  Hence

```text
c<=deg U<=30,833.                                      (11)
```

After deleting the `c` common roots, distinct split members of a pencil have
disjoint deployed root sets: a non-base point determines its unique pencil
parameter.  Every residual locator has degree

```text
r=63,601.
```

Thus a pencil of `M` residual supports uses at least

```text
c+M(r-c)
```

of the `n` deployed roots.  From (11),

```text
M<=max_(0<=c<=30,833) floor((n-c)/(r-c))
 =floor((2,097,152-30,833)/(63,601-30,833))
 =63.                                                   (12)
```

This proves the residual-owner cap.

## 3. Fixed-residual and cross-stratum composition

For each one of the at most 63 residual supports, the all-weight theorem at
`f=28` gives fixed-absolute-scalar cap

```text
20,826,085.
```

The quotient constant lies in `mu_64`, so a projective ray meets that fixed
residual image in at most 64 scalar cells.  Multiplication gives (1).

The `f=28` and `f=29` strata are disjoint by their canonical numbers of
complete `mu_B` cosets.  Therefore their proven ray caps add, regardless of
any congruence between a member of one stratum and a member of the other.
This proves (2).

## Scope and nonclaims

- The theorem is uniform over every residual-root distribution and every
  projective residue ray for the literal modulus `g=X^67,472`.
- It pays the complete `f=28` stratum and, after composition with the
  previous theorem, the union `f=28,29`.
- It does not pay `f<=27`.  At those weights the residual locator has at
  least three `B`-blocks, so (8)--(12) are not an exhaustive owner compiler.
- It does not treat arbitrary monic `g`, prove the uniform factor
  `4,224,290`, close `c=0`, or move the official score.

## Replay

```bash
ruby --disable-gems -w work/verify_c0_q64_f28_residual_pencil_payment.rb
```
