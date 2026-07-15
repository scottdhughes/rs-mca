# The minimum-double `q=14,B=42` boundary cell is impossible over the deployed field

## Theorem

Work over the deployed field

```text
p=2,130,706,433.
```

Assume the source-realized `M=212` rank-15 reduction produces a reduced
arrangement of `B=42` individually `F_p`-rational projective lines with exact
minimal Jacobian-syzygy degree `q=14`, isolated field zeros, and the exact
boundary data

```text
U=E=0,
R=q^2+q+1=211,
D=39 arrangement double points.
```

Then the arrangement does not exist.

This pays the complete minimum-double subcell of both exact aggregate rows

```text
(square,n14,n15,P,R_res,I_res)
(31150,2,0,1,1,2),
(31152,0,1,0,0,0).
```

It does not exclude the same two aggregate rows when `D>=44`.

## 1. The boundary theorem fixes the incidence moments

The characteristic-valid boundary extactic theorem makes every field zero a
reduced arrangement intersection and every arrangement line contains exactly
`q+1=15` distinct intersections.  Hence, if `n_k` is the number of
intersection points incident with exactly `k` of the 42 lines,

```text
sum n_k=211,
sum k n_k=42*15=630,
sum C(k,2)n_k=C(42,2)=861.                         (1)
```

Put `x=k-2` at the 172 non-double points.  From (1) and `n_2=39`,

```text
sum x=208,
sum x^2=676.                                           (2)
```

All 172 values have `x>=1`; write `y=x-1`.  Then

```text
sum y=36,                 sum y^2=432=12*36.            (3)
```

The rank-15 marked-point cap gives `k<=15`, hence `0<=y<=12`.  Since
`y^2<=12y`, equality in (3) forces every `y` to be zero or 12.  Therefore

```text
n_2=39,                 n_3=169,                 n_15=3. (4)
```

## 2. Three centers and 39 leaves

For one arrangement line let `d,t,h` be its numbers of double, triple, and
15-fold intersections.  The 15 support points and the other 41 lines give

```text
d+t+h=15,
d+2t+14h=41.
```

Thus `t+13h=26` and `d=12h-11`.  Nonnegativity forces exactly two line
types:

```text
h=1: (d,t,h)=(1,13,1),
h=2: (d,t,h)=(13,0,2).                                  (5)
```

Counting incidences with the three 15-fold points gives exactly three lines
of the second type and 39 of the first.  Call them centers and leaves.

Let `e_CC,e_CL,e_LL` count double edges of center-center, center-leaf, and
leaf-leaf type.  The double degrees in (5) give

```text
39=2e_CC+e_CL,
39=e_CL+2e_LL,
```

so `e_CC=e_LL`.  A leaf-leaf double edge would be an isolated two-vertex
component of the double graph.  Each of those two saturated lines has 14
other simple radial intersections.  If `r` and `r^{-1}` are their reciprocal
double-point connection residues, the two line-residue equations give

```text
r=1-14=-13,             r^{-1}=1-14=-13.
```

This would force `169=1`, i.e. `168=0` in `F_p`, impossible.  Hence
`e_LL=e_CC=0`.  The double graph is exactly three disjoint stars `K_(1,13)`.

The three centers cannot be concurrent.  If they met at one 15-fold point,
their remaining three center--15-fold incidences would have to lie at the
other two 15-fold points; one of those points would contain two centers,
making that pair meet twice.  Thus the centers form a triangle, and every
15-fold vertex contains two centers and thirteen leaves.  Each leaf is
double with the opposite center.  The 169 triple points consequently form a
`(3,13)` net: every pair of leaves from two different vertex pencils meets a
unique leaf from the third pencil.

## 3. A rational `(3,13)` net forces `13 | p-1`

Move the three pencil vertices to the coordinate vertices.  Because every
line is individually `F_p`-rational, the three leaf classes can be written
with nonzero slope sets `A,B,C subset F_p^*`, each of size 13.  Triple
concurrence says

```text
B A^(-1) subset C.
```

All three sets have size 13.  Fix `a_0 in A`.  For every `a in A`, the set
`B/a` has size 13 and lies in `C`, hence `B/a=C=B/a_0`.  Therefore every
element of `A/a_0` stabilizes `C` under multiplication.  The stabilizer

```text
H={h in F_p^*: hC=C}
```

contains 13 elements.  Multiplication acts freely on `F_p^*`, so every
`H`-orbit in `C` has size `|H|`; hence `|H|` divides `|C|=13`.  It follows
that `|H|=13`, and therefore `13` divides `p-1`.

But

```text
p-1=2,130,706,432 == 10 (mod 13).
```

This contradiction proves the theorem.

## Scope

The proof is source-valid over the literal field because it uses individual
`F_p`-rationality of the arrangement lines, not merely an arrangement over
the algebraic closure.  It pays exactly the `D=39` subcell.  The exact moment
ledger has no rows at `D=40,41,42,43`; the next unresolved double count is
`D=44`.

