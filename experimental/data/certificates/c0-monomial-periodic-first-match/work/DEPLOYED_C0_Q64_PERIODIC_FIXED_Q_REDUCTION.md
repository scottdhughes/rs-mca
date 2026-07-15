# Deployed `c=0` periodic obstruction: exact `mu_64` reduction

## The literal block scale

Put

```text
B=2^15=32,768,       H=mu_(2^21),       H/mu_B=mu_64,
t=981,105=29B+30,833,
a=67,472.
```

The crucial numerical window is

```text
2B=65,536 < a=67,472 <3B=98,304.                     (1)
```

Fix a residual support `R_0` of size `30,833` inside one `mu_B` coset and
write its locator as `A_0(X)`.  For a 29-subset `S` of the quotient
`mu_64`, disjoint from the residual coset, put

```text
Q_S(Y)=product_(y in S)(Y-y),
L_S(X)=A_0(X) Q_S(X^B).                               (2)
```

Every `L_S` is a monic locator of exactly `t` distinct roots in `H`.
Because `A_0(0)!=0`, (1) makes the following equivalence exact:

```text
L_S == L_T (mod X^a)
 iff Q_S == Q_T (mod Y^3).                            (3)
```

Indeed, the least nonzero coefficient of `Q_S-Q_T` at `Y^j` produces a
nonzero term of degree `jB` after (2).  It is invisible modulo `X^a` exactly
when `j>=3`.

Thus the entire periodic fixed-residual lane reduces to the finite map

```text
{S subset mu_64: |S|=29}
  -> (c_0(S),c_1(S),c_2(S)) in F_p^3,                 (4)
```

where `c_i` are the three low coefficients of `Q_S`.

If

```text
P_S=product_(y in S)y,
U_S=sum_(y in S)y^(-1),
V_S=sum_(y in S)y^(-2),
```

then, since `p` is odd,

```text
c_0=-P_S,
c_1=P_S U_S,
c_2=-P_S (U_S^2-V_S)/2.                              (5)
```

Consequently (4) is equivalently the explicit subset map

```text
S -> (P_S,U_S,V_S) in mu_64 x F_p x F_p.             (6)
```

This answers the reduction question completely.  It does not by itself
bound the maximum fiber of (6).

There is no hidden subgroup-index loss in this finite quotient.  Truncated
units split, via the degree-two logarithm, as

```text
(F_p[Y]/Y^3)^* = F_p^* x F_p^2,
log(1-rY)=(-r,-r^2/2).
```

For fixed cardinality, ratios against the factor at `y=1` have scalar
projection generating `mu_64` and logarithmic vectors

```text
(u-1,(u^2-1)/2),       u=y^(-1).
```

The vectors from any two distinct nontrivial `u` are independent: their
determinant is a nonzero Vandermonde product.  Raising ratios to the 64th
power kills the scalar component and exposes the full `p`-primary span.
Therefore the effective group of (6) is exactly

```text
mu_64 x F_p^2.                                         (6a)
```

The obstruction below is genuine nonuniformity inside a fully generated
effective group, not a ray-class index artifact.

## A literal fixed-scalar family of size 405

Partition `mu_64` into its sixteen `mu_4` cosets

```text
C_j={zeta^(j+16k):0<=k<4},       j in Z/16Z.
```

Keep the quotient point `1=zeta^0` as a singleton, reserve the other three
points of `C_0` so one of their `mu_B` cosets can contain `R_0`, and choose
seven complete blocks `C_j` with `j in {1,...,15}`.  The quotient support is

```text
S_J={1} union union_(j in J) C_j,       |J|=7,        (7)
```

and has size `1+7*4=29`.

Every complete `mu_4` coset has zero inverse first and second power sums.
Its product has exponent `4j+32 mod 64`.  Therefore all sets (7) with one
fixed value of

```text
sum_(j in J) j (mod 16)                               (8)
```

have exactly the same triple (6).  Direct enumeration of the
`binom(15,7)=6,435` block choices gives residue-fiber sizes between 400 and
405, with maximum

```text
405.                                                   (9)
```

This is not just a quotient toy.  Take the binary complete intersection

```text
g=X^a,       h=L_(S_0)
```

for one member `S_0` of a 405-family.  Since none of the locators contains
the root zero, `gcd(g,h)=1`, and

```text
deg g+deg h-2=a+t-2=K-1.
```

Equation (3) gives, for every member of the family,

```text
L_S=h+gW_S.                                            (10)
```

Thus all 405 split locators lie in the same deployed binary-apolar top shell
with the **same scalar `q=1`**.  They are exact because that scalar is
nonzero.  Here `D_0=gcd(g,X^n-Z^n)=1`, so no deletion or jet subtlety is
being hidden.

This explicitly kills fixed-`q` uniqueness, any cap below 405, and any claim
that the `a+1` swap improvement makes sparse generators harmless.

## Does it threaten the required `1.29e8` ceiling?

No conclusion at that scale follows from this construction.  Numerically,

```text
T/(p-1)=128,996,705.678592...,
(T/(p-1))/405=318,510.384392... .                     (11)
```

So the explicit periodic family is 18.281 bits below the sufficient
fixed-scalar ceiling.

Conversely, the generic consequence of the three coefficients is much too
weak to prove the ceiling.  If two 29-subsets have one value under (4), then
after cancelling their common quotient roots their disjoint tail locators
are congruent modulo `Y^3`.  Monicity forces Johnson swap at least four.
The resulting sharp packing bound is only

```text
max fiber(4)
 <=floor(binom(64,26)/binom(29,26))
 =164,629,954,331,472,                                (12)
```

which is `1,276,233.788...` times the target in (11).

Therefore this sparse/periodic lane is now a finite, auditable `mu_64`
problem, but it is not closed:

```text
405 <= max fiber of (6) <=164,629,954,331,472.
```

The lower endpoint is a genuine deployed fixed-`q` construction; the upper
endpoint is only three-coefficient packing.  Excluding a target violation
requires an actual maximum-fiber theorem or exact computation for (6), not
another use of the minimum-swap bound.
