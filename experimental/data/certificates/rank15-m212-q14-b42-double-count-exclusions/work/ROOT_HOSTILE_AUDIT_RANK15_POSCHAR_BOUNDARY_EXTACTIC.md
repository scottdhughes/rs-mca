# Root hostile audit: positive-characteristic boundary extactic exclusion

## Verdict

`ACCEPT`, with high confidence, for the frozen theorem

```text
work/RANK15_POSCHAR_BOUNDARY_EXTACTIC_EXCLUSION.md
SHA-256 1c5a2840aac0bfe4426b50ef10d6abde8a09724a7982967208214f2b695101c6
```

and frozen replay

```text
work/verify_rank15_poschar_boundary_extactic_exclusion.rb
SHA-256 d35fc042b2aabf08f40691d58433350ff68f773c6dbdeb159032633620d817f8.
```

This audit is independent of the theorem author's derivation.  It checks the
proof object, not merely the printed census.

## 1. Restriction and saturation

For an arrangement line `L`, Euler subtraction produces a nonzero degree-`q`
rank-two multirestriction derivation with total multiplicity `3q-1`, while the
projective field restricts to a nonzero section of `O_L(q+1)`.  Hence
`h_L<=q+1`.  If `h_L<=q`, the separable rational-map lemma gives an
arrangement point of multiplicity at least `2q`.  A line outside that pencil
would then have at least `2q>q+1` distinct intersections.  Thus all lines
would form a pencil, contradicting exact positive `mdr=q`.  Consequently
every line has exactly `q+1` support points, all simple as zeros of the
restricted section.

The `+1` between the Ziegler multiplicity and the projective arrangement
multiplicity is used correctly.

## 2. Extactic determinant

After putting one invariant line at `z=0`, the Euler-equivalent homogeneous
derivation has the form

```text
delta=A partial_x+B partial_y,       deg A=deg B=q.
```

The determinant

```text
Xi=det[(x,y,z);(A,B,0);(delta A,delta B,0)]
```

has degree `1+q+(2q-1)=3q`.  A linear coordinate change acts on all three
rows by the same invertible matrix, so the determinant is covariant up to a
unit.  If an invariant line is `w=0`, then

```text
delta(w)=h w,
delta^2(w)=(delta(h)+h^2)w,
```

and its reduced factor divides `Xi`.  Adding an Euler multiple to the chosen
homogeneous representative changes the determinant rows only by combinations
of the first two rows, so the divisor is projectively well defined for the
argument used here.

## 3. The zero-determinant branch

If `Xi=0`, dehomogenization gives coprime `P,Q` of maximum degree exactly
`q`; otherwise the field has a divisorial zero in the affine chart or along
`z=0`.  Over `k(t)`, `R_t=Q-tP` has degree `q` and is coprime to `P`.  The
identity

```text
P D(Q)-Q D(P)=0
```

implies

```text
R_t | (partial_x+t partial_y)R_t.
```

The second polynomial has smaller degree, so it vanishes.  In coordinates
`u=y-tx`, `v=x`, its operator is `partial_v`.  Since `q<p`, no nonconstant
`v^p` term occurs, and `R_t` belongs to `k(t)[u]`.  Away from finitely many
specializations this yields invariant affine lines of infinitely many
slopes.  Intersections of distinct invariant lines are field zeros.  Finiteness
of the isolated zero set therefore forces all invariant lines into one
pencil, again contradicting exact positive `mdr`.  No characteristic-zero
separability or analytic theorem is imported in this step.

Thus `Xi` is nonzero.  The reduced arrangement product `f` has the same
degree `3q`, so `Xi=lambda f` and every arrangement factor occurs exactly
once.

## 4. Zero scheme

At a projective field zero the coordinate row and derivation row of the
extactic matrix are dependent, so the zero lies on `Xi=f`.  Saturation
excludes zeros at smooth points of the arrangement.

At a double intersection, tangency diagonalizes the local Jacobian and the
two simple restricted zeros make both diagonal entries nonzero.  At a point
on at least three lines, tangency to three directions forces the diagonal
linearization to be a nonzero scalar.  Hence every arrangement intersection
is a reduced local zero of length one.  This is an ambient two-variable
Jacobian argument, not an unsupported inference from one restriction.

The isolated zero length of a section of `T_(P^2)(q-1)` is

```text
c2=3+3(q-1)+(q-1)^2=q^2+q+1.
```

Therefore the number of distinct arrangement intersections equals this
length and the exact geometric excess is zero.

## 5. Source and replay scope

The finite driver records

```text
R_total=(213-n14-n15)+R_residual,
E=(q^2+q+1)-R_total.
```

Thus its `E` is the theorem's geometric excess.  The frozen replay reports

```text
(q,B)=(22,66): 1474 U=0 states, all E=30..47;
(q,B)=(23,69):  136 U=0 states, all E=30..38;
(q,B)=(24,72):    0 U=0 states.
```

Every equality state is therefore excluded.  This audit makes no claim on
the nine cells with `B<3q`, where the extactic determinant has a residual
factor of degree `1..6`.
