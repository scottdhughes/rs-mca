# Positive-characteristic boundary extactic exclusion

## Theorem

Let `k` be an algebraically closed field of characteristic `p`.  Let a
reduced arrangement of

```text
B=3q,                 2<=q<p
```

distinct projective lines have exact minimal Jacobian-syzygy degree `q>0`.
Assume that the corresponding degree-`q` minimal projective field has
isolated zeros and preserves the arrangement.  Then the field's zero scheme
consists precisely of the distinct arrangement intersection points, and
every such zero is reduced.  Consequently, if `R` is the number of distinct
arrangement intersection points, then

```text
R=q^2+q+1,            E=(q^2+q+1)-R=0.                 (1)
```

This is the equality case missing from the strict `B>3q` invariant-line
ramification exclusion.  It is characteristic-valid; the only place where
the characteristic enters is the explicit hypothesis `q<p`.

## 1. Every arrangement line has exactly `q+1` support points

Fix an arrangement line `L`.  The Euler subtraction and direct
multirestriction construction from the strict ramification theorem give:

1. a nonzero restriction of the projective field to `L`, a section of
   `O_L(q+1)`;
2. a nonzero degree-`q` logarithmic derivation of the rank-two
   multirestriction on `L`, whose total multiplicity is `M=B-1=3q-1`.

If `h_L` is the number of distinct intersections on `L`, the first item gives

```text
h_L<=q+1.                                                   (2)
```

Suppose `h_L<=q`.  The positive-characteristic rational-map lemma applies,
because

```text
M-h_L >= (3q-1)-q = 2q-1 > 2q-2.
```

It produces a point `P` on `L` whose multiplicity in the projective
arrangement is at least `2q`.  If an arrangement line `K` did not pass
through `P`, its intersections with those at least `2q` lines through `P`
would be at least `2q` distinct support points on `K`.  This contradicts
`h_K<=q+1`, since `q>=2`.  Thus the arrangement would be a pencil, whose
Jacobian-syzygy degree is zero.  That contradicts exact `mdr=q>0`.

Therefore every line satisfies

```text
h_L=q+1.                                                   (3)
```

The `q+1` distinct arrangement intersections are zeros of the nonzero
section of `O_L(q+1)`.  They exhaust its zero divisor.  In particular, each
is a simple zero of the restricted field and there is no further zero at a
smooth point of `L`.

## 2. The degree-`3q` extactic polynomial is nonzero

Choose one arrangement line as `z=0`.  Write the logarithmic homogeneous
derivation representing the projective field as

```text
theta=a partial_x+b partial_y+c partial_z,       deg(a,b,c)=q.
```

Tangency gives `c=z gamma`.  Replacing `theta` by the projectively equivalent

```text
delta=theta-gamma(x partial_x+y partial_y+z partial_z)
      =A partial_x+B partial_y
```

makes `delta(z)=0`.  Define

```text
Xi = det [ x          y          z
           A          B          0
           delta(A)   delta(B)   0 ]
   = z(A delta(B)-B delta(A)).                            (4)
```

It is homogeneous of degree

```text
1+q+(2q-1)=3q.
```

Every invariant arrangement line contributes its reduced linear factor to
`Xi`.  Indeed, make an invertible linear coordinate change putting that line
in the form `w=0`.  The three determinant columns transform by that same
coordinate change, so the determinant changes only by a nonzero scalar.
Tangency says `delta(w)=h w`, and then

```text
delta^2(w)=(delta(h)+h^2)w.
```

Thus the entire `w` column is divisible by `w`, and so `w|Xi`.  Since the
arrangement is reduced, the product of its distinct linear factors divides
`Xi`.

We claim `Xi` is not the zero polynomial.  Suppose otherwise and dehomogenize
on `z=1`, writing

```text
D=P partial_x+Q partial_y,       deg(P),deg(Q)<=q.
```

The isolated-zero hypothesis implies `gcd(P,Q)=1`; a common nonconstant
factor would homogenize to a divisorial zero.  Moreover
`max(deg P,deg Q)=q`: otherwise both homogeneous coefficients `A,B` would be
divisible by `z`, again giving a divisorial zero.  Equation `Xi=0` becomes

```text
P D(Q)-Q D(P)=0.                                         (5)
```

Over `k(t)`, put `R_t=Q-tP`, which has degree `q`.  From (5),

```text
P D(R_t)=R_t D(P).
```

Since `gcd(P,R_t)=1`, `R_t` divides `D(R_t)`.  Modulo `R_t` one has `Q=tP`,
and hence

```text
D(R_t) = P(partial_x+t partial_y)R_t       modulo R_t.
```

The same coprimality therefore says that `R_t` divides

```text
(partial_x+t partial_y)R_t.
```

The latter polynomial has degree smaller than `R_t`; hence it is zero.
With `u=y-tx` and `v=x`, the operator is `partial_v`.  Because
`deg R_t<=q<p`, its kernel in this degree contains no nonconstant `v^p`
term, and therefore

```text
R_t in k(t)[u].                                           (6)
```

The identity holds over `k(t)`, hence after specialization away from finitely
many exceptional values.  For infinitely many `t in k`, (6) factors over
the algebraically closed field `k` into affine lines
`y-tx=constant`.  Each factor is invariant, since
`D(y-tx-constant)=Q-tP=R_t` is divisible by that factor.  Thus the
projective field has infinitely many invariant projective lines.

The pairwise intersection of two distinct invariant lines is a zero of the
projective field.  Since the zero set is finite, an infinite subfamily must
pass through one fixed point `P_0`: fix one line and pigeonhole its
intersections with the others among the finite zero set.  Any invariant line
not through `P_0` would meet that infinite pencil in infinitely many distinct
zeros.  Hence every invariant line, including every arrangement line, passes
through `P_0`.  Again the arrangement is a pencil and has `mdr=0`, a
contradiction.  Therefore `Xi` is nonzero.

## 3. Equality of divisors and reduced zero scheme

Let `f` be the reduced product of the `B=3q` arrangement lines.  Section 2
shows

```text
f divides Xi,          deg f=deg Xi=3q,          Xi!=0,
```

so

```text
Xi=lambda f,          lambda in k^*.                        (7)
```

In particular, every arrangement factor occurs in `Xi` with multiplicity
exactly one.

At a zero of the projective field, the first two rows in (4) are dependent;
therefore every field zero lies on `Xi=0`, hence by (7) on the arrangement.
Section 1 excludes zeros at smooth arrangement points.

It remains to compute the local length at an arrangement intersection `P`.
Choose affine parameters `(u,v)` centered at `P` and write the local field
as

```text
X=F(u,v) partial_u+G(u,v) partial_v.
```

For a double point, put the two lines at `u=0` and `v=0`.  Tangency gives
`F in (u)` and `G in (v)`, so the Jacobian at the origin is diagonal:

```text
J_X(P) = [ F_u(P)       0
                 0 G_v(P) ].                            (8)
```

The restricted zero on `v=0` is simple exactly when `F_u(P)!=0`, and the
restricted zero on `u=0` is simple exactly when `G_v(P)!=0`.  Hence (8) is
invertible.

At a point incident to at least three lines, use `u=0`, `v=0`, and
`u-v=0` for three of them.  The first two tangency conditions again make
the linear part diagonal, say `(alpha u,beta v)`.  Tangency to `u-v=0`
forces `alpha=beta`.  Simplicity on either line forces this common scalar to
be nonzero.  Thus the Jacobian is again invertible.  By the formal inverse
function/local-parameter criterion, `(F,G)` is the maximal ideal in the
completed local ring, so the local zero-scheme length is exactly one in
both cases.

Finally, a degree-`q` projective field is a section of
`T_(P^2)(q-1)`.  Its isolated zero scheme has top-Chern length

```text
c_2(T_(P^2)(q-1))
 =3+3(q-1)+(q-1)^2
 =q^2+q+1.                                                (9)
```

Equations (7)--(9) prove (1).

## 4. `M=213` impact

The complete low-band scan has only three possible equality cells `B=3q`:

```text
(q,B)=(22,66), (23,69), (24,72).
```

After imposing the necessary support saturation (3), their exact-state
censuses are

```text
(22,66): 1,474 states, all with 30<=E<=47;
(23,69):   136 states, all with 30<=E<=38;
(24,72):     0 states.
```

The source translation is exact.  In the finite-state driver, the retained
arrangement support size is

```text
R_total=(M-n_14-n_15)+residual_points,
```

while

```text
point_cap=(q^2+q+1)-(M-n_14-n_15).
```

Therefore its recorded

```text
E=point_cap-residual_points=(q^2+q+1)-R_total
```

is precisely the geometric excess in (1), not a relaxation surrogate.
The theorem forces `E=0`, so all equality cells are excluded.  The relaxed
low-band residual drops from 5,639 profiles to 2,625 profiles in the nine
strictly sub-boundary cells `B<3q`.

## Replay

```text
ruby --disable-gems -w work/verify_rank15_poschar_boundary_extactic_exclusion.rb
```

The replay hash-locks the finite-state source, reruns all three equality
cells with the support-saturation condition, checks their complete excess
histograms, and verifies the degree and characteristic inequalities used in
the proof.

## Exact nonclaim

This theorem closes the `B=3q` equality cells only.  It does not exclude the
nine remaining cells with `B<3q`, where the extactic polynomial has a
positive-degree residual factor.
