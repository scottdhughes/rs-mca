# CAP25 v13 raw: a star-determinant rank gap removes four M31 two-shell rows

**Status:** `PROVED` for the theorem and exact four-row certificate below;
`OPEN` for the remaining `3,101,276` two-shell rows, all cells with three or
more shells, and the complete deployed M31 upper ledger.

**Base:** continues
`experimental/notes/thresholds/cap25_v13_m31_rank_inertia_anchor_cut.md`.

**Verifier:**

```text
python3 experimental/scripts/verify_m31_star_determinant_rank_gap.py
```

The verifier uses only the Python standard library. It regenerates the full
`3,254,885`-row grid and the integrated `153,605`-row exclusion union before
applying the new predicate. The exact replay certificate is
`experimental/data/cap25_v13_m31_star_determinant_rank_gap.json`; the verifier
checks every row, boundary value, count, and hash and includes two tamper
tests.

## 1. Exact setting

Use the deployed M31 constants

```text
p  = 2^31-1 = 2147483647,
N  = 2^21   = 2097152,
m  = 981129,
w  = 67447,
d0 = N-w    = 2029705,
B* = 2^24-1,
L  = B*+1   = 16777216,
R  = m(N-m) = 1094962529967.
```

It is enough to exclude an `L`-member subfamily of a family larger than
`B*`. On a two-shell row write

```text
e1=(kappa-1)t,  e2=kappa*t,  lambda=kappa-1.
```

Let `X` be the `L x N` binary incidence matrix and let `A` join two supports
when their distance is `e2`. Put

```text
S=A-lambda*I,  c=m-e1.
```

Entrywise one has the exact integer identity

```text
t*S = c*J-X*X^T.                                          (1)
```

Indeed, the right side is `-e1` on the diagonal, `t` on an
`e2`-edge, and zero on an `e1`-pair.

All rows of `X` have one M31 prefix syndrome. Their differences lie in the
kernel of the weight-plus-power-sum Vandermonde matrix, so

```text
rank_Fp(X) <= N-w=d0,   rank_Fp(S) <= d0.                 (2)
```

Centering (1) gives

```text
t*S = (R/N-e1)*J-C,                                      (3)
```

where `C=X*X^T-(m^2/N)J` is positive semidefinite. The grid has
`e1<=floor(R/N)`. Thus

```text
n_+(S) <= 1.                                              (4)
```

No regularity, integral spectrum, or modular-to-real rank equality is used.

## 2. Exact maximum-degree cap

Fix a vertex and let its `e2`-neighborhood have size `h`. If `a_h` is the
average degree inside that neighborhood, the anchored difference vectors
give

```text
|sum z_U|^2 = t*h^2*(kappa+1+(lambda-a_h)/h),
|sum z_U|^2 >= N*h^2*kappa^2*t^2/R.                       (5)
```

Dropping `a_h>=0` yields

```text
h*C0(kappa,t) <= R*lambda,
C0(kappa,t)=N*kappa^2*t-R*(kappa+1).                      (6)
```

When `C0>0`, every graph degree is therefore at most

```text
u(kappa,t)=floor(R*(kappa-1)/C0(kappa,t)).                (7)
```

## 3. Variable-rank cubic obstruction

Suppose temporarily that `rank_Q(S)<=d`, where `d0<=d<=N`, and put

```text
q_d=L-d,
T_{kappa,d}(x)
  =(d-1)^2*(q_d*(kappa-1)^3+x^3)
   -(q_d*(kappa-1)+x)^3.                                 (8)
```

Then `A` has at least `q_d` copies of `lambda`. By (4), at most one of its
remaining eigenvalues exceeds `lambda`. Write the spectrum as

```text
lambda (q_d times), rho, x_1,...,x_{d-1},  x_i<=lambda.
```

The trace equation and `x_i>=-rho` give

```text
rho >= q_d*lambda/(d-2).                                 (9)
```

Set `a=(q_d*lambda+rho)/(d-1)`. On the range (9), `a<=rho` and
`lambda<2a`. Hence

```text
x_i^3 <= 3*a^2*x_i+2*a^3
```

because the difference factors as `(2a-x_i)(a+x_i)^2`. Summing and using
`tr(A^3)>=0` gives

```text
T_{kappa,d}(rho) >= 0.                                   (10)
```

Moreover,

```text
T'_{kappa,d}(x)
  =3*((d-2)x-q_d*lambda)*(d*x+q_d*lambda),                (11)
```

so `T` is nondecreasing on the range (9). Since `rho<=Delta(A)<=u`, either

```text
u < ceil(q_d*lambda/(d-2))
```

or

```text
T_{kappa,d}(u)<0                                          (12)
```

forces `rank_Q(S)>d`.

Applying (12) successively from `d=d0` identifies exactly ten integrated
survivors with a certified real-rank floor `r0>d0`:

| kappa | t | e1 | e2 | u | r0 | g=r0-d0 |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 391732 | 391732 | 783464 | 913 | 2032856 | 3151 |
| 2 | 391733 | 391733 | 783466 | 907 | 2049267 | 19562 |
| 2 | 391734 | 391734 | 783468 | 900 | 2068679 | 38974 |
| 2 | 391735 | 391735 | 783470 | 894 | 2085550 | 55845 |
| 3 | 232117 | 464234 | 696351 | 1807 | 2058936 | 29231 |
| 4 | 163198 | 489594 | 652792 | 2729 | 2041947 | 12242 |
| 6 | 101539 | 507695 | 609234 | 4561 | 2035032 | 5327 |
| 8 | 73432 | 514024 | 587456 | 6316 | 2062308 | 32603 |
| 14 | 39961 | 519493 | 559454 | 11831 | 2040825 | 11120 |
| 15 | 37131 | 519834 | 556965 | 12737 | 2041622 | 11917 |

The ten-row hash is

```text
c18ab71c6450c9b22360c16c91944e98c5d5dedf50723a9fb133e254c69a4b15
```

These are rank-gap certificates, not yet ten exclusions.

## 4. Full-rank star determinant

Let `r=rank_Q(S)`. A symmetric rational matrix has a nonsingular principal
submatrix of order its rank; choose such an integer principal block `B` of
`S`. By (2),

```text
rank_Fp(B)<=d0.
```

The Smith normal form therefore gives

```text
p^(r-d0) divides det(B).                                  (13)
```

For one of the ten rows, `r>=r0`, so

```text
|det(B)| >= p^g,  g=r0-d0.                               (14)
```

Now specialize to `kappa=2`, hence `lambda=1`. By principal-submatrix
interlacing and (4), `B` has at most one positive eigenvalue. Since `B` is
nonsingular and `tr(B)=-r`, either all its eigenvalues are negative, when
`|det(B)|<=1`, or its positive eigenvalue `beta` satisfies `beta<=u-1`.
Writing the other eigenvalues as `-a_i`, AM-GM gives

```text
|det(B)|
 <= beta*((r+beta)/(r-1))^(r-1)
 <= (u-1)*(1+u/(r-1))^(r-1)
 <  (u-1)*3^u.                                           (15)
```

Let

```text
b(u)=min{b in Z: u-1<2^b}=bit_length(u-1).
```

Since `3^u<2^(2u)` and `p>2^30`, (14)-(15) are incompatible whenever

```text
b(u)+2u < 30g.                                           (16)
```

Condition (16) holds on exactly the first four rows of the table:

| t | u | r0 | g | b(u)+2u | 30g |
|---:|---:|---:|---:|---:|---:|
| 391732 | 913 | 2032856 | 3151 | 1836 | 94530 |
| 391733 | 907 | 2049267 | 19562 | 1824 | 586860 |
| 391734 | 900 | 2068679 | 38974 | 1810 | 1169220 |
| 391735 | 894 | 2085550 | 55845 | 1798 | 1675350 |

Thus no `L`-member M31-prefix two-shell realization exists on

```text
(2,391732,391732,783464),
(2,391733,391733,783466),
(2,391734,391734,783468),
(2,391735,391735,783470).                                 (17)
```

The tuple order is `(kappa,t,e1,e2)`. The four-row hash is

```text
2809ec4892d507367920dcfd2480375a619033f61751aafe96efc6bebfbe473d
```

## 5. Exact ledger delta

The verifier reproduces the integrated union before adding (17):

```text
base grid                         3254885
integrated exclusions             153605
integrated residual              3101280
new exclusions                         4
new exclusion union               153609
new residual                     3101276
```

The new union and residual hashes are

```text
new union:
2f57a0a5379a4222869d4e6ab79aad39d7b352df6c0227996ab2da7ec10483a4

new residual:
40925c2c5a3c3928a42f6d92775de87608c7e260bf3c3ff7eda36b5e02193956
```

## 6. Nonclaims and remaining wall

- This packet does not exclude the other six rank-gap rows. A stronger
  componentwise `p`-adic determinant bound is needed there.
- It does not exclude the remaining `3,101,276` two-shell rows.
- It does not handle three-or-more-shell cells or add sizes of different
  cells.
- It does not prove a complete first-match upper ledger.
- It does not prove `U(a0+1)<=B*` and does not solve the deployed M31 row.
- It has no asymptotic effect.

The next exact target is a componentwise valuation bound for the six
remaining low-`kappa` rank-gap rows. If `B=A_S-lambda I` is any nonsingular
induced star block with maximum degree at most `u` and `n_+(B)<=1`, prove

```text
v_p(det(B))<g
```

for the six triples

```text
(lambda,u,g) =
(2,1807,29231), (3,2729,12242), (5,4561,5327),
(7,6316,32603), (13,11831,11120), (14,12737,11917).
```
