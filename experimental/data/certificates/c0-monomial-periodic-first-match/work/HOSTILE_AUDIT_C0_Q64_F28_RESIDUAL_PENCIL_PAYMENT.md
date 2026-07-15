# Hostile audit: complete canonical `q64,f=28` residual-pencil payment

## Verdict

```text
TWO-BLOCK COEFFICIENT COMPILER: PASS
RESIDUAL PROJECTIVE-PENCIL NORMAL FORM: PASS
DISTINCT-FAMILY DEGREE CUT deg U<=30,833: PASS
BASE-ROOT AND UNIQUE-NONBASE-PARAMETER ARGUMENT: PASS
RESIDUAL OWNER CAP 63: PASS
FIXED-RESIDUAL HAHN/64-SCALAR COMPOSITION: PASS
CANONICAL f=28 PLUS f=29 DISJOINT ADDITION: PASS
f<=27 / CROSS-SCALE ADDITION / GENERAL g / UNIFORM c=0: NOT PROVED
```

Accepted pins:

```text
work/C0_Q64_F28_RESIDUAL_PENCIL_PAYMENT.md
9c0142793a738513f8a83801ff2536cd2a463b8f377a34be716ca5744b1f4709

work/verify_c0_q64_f28_residual_pencil_payment.rb
c080aa36fe5af048eeb087975a6b88d42cb15b04ed056c39901b3bdaed148e51

work/verify_c0_q64_f28_residual_pencil_payment.expected.txt
aea77f11333714650f33e253fd0f0f7f5c63335dcb34bec7f03c4709d819b7c3.
```

The claimant replay byte-matches its expected output.

## 1. Two-block equations

At `f=28`, the canonical residual degree is

```text
r=63,601=B+m,       B=32,768,       m=30,833.
```

Every residual locator has the unique decomposition

```text
A_i=A_(i,0)+X^B A_(i,1),
deg A_(i,0)<B,       deg A_(i,1)=m,
```

with `A_(i,1)` monic.  Write the first two quotient coefficients as
`q_(i,0)` and `q_(i,1)`, with `lambda_i=q_(i,1)/q_(i,0)`.

Because

```text
a=2B+1,936,
```

projective proportionality modulo `X^a` exposes both complete coefficient
blocks below `X^(2B)`.  Relative to a fixed member zero, block zero gives

```text
A_(i,0)=s_i U,
s_i=c_i q_(0,0)/q_(i,0).
```

Block one gives exactly

```text
A_(i,1)=s_i[V+(lambda_0-lambda_i)U].
```

There is no sign or scalar loss: direct substitution gives

```text
q_(i,0)A_(i,1)+q_(i,1)A_(i,0)
=c_i(q_(0,0)V+q_(0,1)U).
```

Thus

```text
A_i=s_i(P+theta_i D),
P=U+X^B V,       D=X^B U,
theta_i=lambda_0-lambda_i.
```

Since `U(0)` is nonzero and `D(0)=0`, the two generators are independent.
For any admissible parameter whose polynomial has degree `r`, monic
normalization is unique; hence distinct residual supports have distinct
parameters.

## 2. Degree cut and base-root bound

The polynomial `V` is monic of degree `m`.  If `deg U>m`, the formula for
`A_(i,1)` can have degree at most `m` only when
`lambda_i=lambda_0`.  Then `A_i=s_iA_0`, and monicity forces `s_i=1`.
Therefore a family containing two distinct residual supports necessarily has

```text
deg U<=m=30,833.
```

If a deployed point is a root of two distinct pencil members, subtracting
their equations forces `D(x)=0`; substituting back forces `P(x)=0`.  It is
therefore a base root common to every pencil member.  Since deployed points
are nonzero and `D=X^B U`, all base roots are roots of `U`.  Thus their
number `c` satisfies

```text
c<=deg U<=30,833.
```

At every nonbase point with `D(x)!=0`, the equation
`P(x)+theta D(x)=0` determines one unique parameter.  A point with
`D(x)=0,P(x)!=0` belongs to no member.  Hence, after deleting the `c` base
roots, the deployed residual-root sets of distinct members are disjoint.

## 3. Exact residual-owner cap

For `M` residual supports, their union has size

```text
c+M(63,601-c)<=2,097,152.
```

The independent verifier checks every integer `c=0,...,30,833` and obtains

```text
max floor((2,097,152-c)/(63,601-c))=63.
```

The maximum is attained precisely throughout the integer interval
`30,802,...,30,833`.  This verifies the endpoint calculation rather than
assuming monotonicity after flooring.

## 4. Fixed-residual and scalar-cell composition

For each of the at most 63 residual supports, the independently audited
all-weight theorem gives absolute-cell cap

```text
20,826,085
```

at weight 28.  After the common residual is canceled, the quotient constant
lies in `mu_64`; therefore a fixed-residual periodic image meets a projective
ray in at most 64 scalar cells.  Multiplying the three independent factors
is legitimate and gives

```text
N_f28(ray)<=63*64*20,826,085
           =83,970,774,720.
```

The projective-ray scalar is already incorporated by the 64-cell payment;
there is no further `p-1` multiplier.

## 5. Canonical addition with `f=29`

The `f=28` and `f=29` populations are disjoint because the canonical label
is the exact number of complete `mu_32768` quotient fibers in the support.
A support with 29 complete fibers is not counted in the canonical f28
population, even though it admits a noncanonical representation obtained by
moving a full fiber into a residual.  Consequently the two caps add without
any cross-stratum ownership assertion:

```text
83,970,774,720+1,619,679,744=85,590,454,464<T,
margin=274,854,024,905,733,128.
```

This disjointness is internal to the fixed q64 scale.  The union can overlap
periodic descriptions at q32 or another scale and cannot be added to those
without an explicit first-match partition.

## Scope and nonclaims

The theorem pays the complete canonical `q64,f=28,g=X^a` stratum and its
disjoint q64 union with the accepted canonical f29 stratum.  For `f<=27`,
the residual has at least three B-blocks and the printed two-block pencil is
not exhaustive.  The result does not treat cross-scale addition, arbitrary
monic `g`, the complete c0 branch, or an official question.

## Independent replay

```text
work/audit_c0_q64_f28_residual_pencil_payment.rb
work/audit_c0_q64_f28_residual_pencil_payment.expected.txt
```

The audit also substitutes deterministic independent scalar choices into
the two-block identities and checks the complete integer base-root range.
