# Eleven-grid-transversal exclusion of the `q=14`, `B=42`, `D=59` cell

## Theorem

Under the literal `M=212`, `q=14`, `B=42`, `U=E=0` boundary hypotheses,
the reduced arrangement cannot have exactly 59 double points.

Together with the audited `D=39,44..58` theorems, the next moment-feasible
double-count wall is `D=60`.

## 1. Exact profile reduction

Use weight `w=k-3` at every point of multiplicity `k>=4`.  The boundary
moments and line equations are

```text
sum w c_w=D-3,
sum w^2 c_w=471-D,
d_L=sum_(P high on L)w_P-11,
t_L=26-sum_(P high on L)w_P-s_L.                    (1)
```

The exact disjoint-group packing gate from the preceding theorem leaves, out
of 958 moment profiles at `D=59`, exactly

```text
[4^18,5^2,14^2,15],
[4^3,5^10,12,15^2],
[4^20,5,13,15^2].                                    (2)
```

In the first row the three heavy points have total incidence 43, so at most
two lines contain no heavy point.  Both multiplicity-5 points would have to
lie on both lines, impossible.  In the second row the heavy incidence is 42,
so at most three lines contain no heavy point.  Every multiplicity-5 point
must lie on at least two of them, but the three line pairs have at most three
intersection points, not ten.  Only the third row remains.

## 2. The rigid third skeleton

Write the high points as

```text
P_1,...,P_20: multiplicity 4, weight 1;
Q:            multiplicity 5, weight 2;
A:            multiplicity 13, weight 10;
B,C:          multiplicity 15, weight 12.             (3)
```

No line contains all three heavy points by the support inequality in (1).
If `x,y,z` lines contain two, one, zero heavy points, then

```text
2x+y=43,
x+y+z=42,
x<=3.
```

The point `Q` needs at least two no-heavy lines.  Hence `z>=2`, so equality
forces

```text
x=3, z=2.                                               (4)
```

All three heavy-pair lines occur.  Call the two no-heavy lines `L,M`.
The five lines through `Q` are `L,M` and three separate connectors to
`A,B,C`; a heavy-pair line through `Q` would consume two heavy partners in
one line and leave too few distinct lines.

Every `P_i` lies on at least one of `L,M`.  It cannot lie on both because
those lines already meet at `Q`.  Its remaining three lines are therefore
separate connectors to `A,B,C`.  Thus `L,M` partition the twenty `P` points.
If `p` lie on one of them, (1) gives

```text
d=p-9>=0,
t=23-2p>=0,
```

so `9<=p<=11`.

After its two heavy-pair sides, `A` has exactly 11 remaining lines.  The line
`AQ` contains no `P_i`, since every pair `Q,P_i` already lies on `L` or `M`.
Any other line through `A` contains at most one point of each of `L,M`.
The remaining ten `A`-lines must cover all twenty `P_i`; hence the split is

```text
10+10,                                                   (5)
```

and each of those ten lines pairs one point of `L` with one point of `M`.

The complete arrangement is therefore

```text
three heavy-pair sides;
11 A-low lines (AQ and ten A-P-P lines);
13 B-low lines;
13 C-low lines;
the two no-heavy lines L,M,                               (6)
```

for 42 lines.

## 3. Eleven complete 13-grid transversals

The side `BC` has high-point weight `12+12=24`, so (1) gives

```text
d_BC=13, t_BC=0.
```

At `B` and `C` it meets 28 of the other arrangement lines.  The remaining
13 are exactly the 11 `A`-low lines and `L,M`.  Since every arrangement line
has 15 distinct support points, their intersections with `BC` are 13
distinct doubles.

Every `A`-low line has double degree one by (1), so it spends its sole double
at `BC`.  The line `AQ` has `Q` plus twelve triples.  Each paired `A-P-P`
line has its two `P` grid points plus eleven triples.

Let `X` be the 13 low lines through `B` and `Y` the 13 low lines through
`C`.  On any `A`-low line, distinct members of `X` meet at `B`, which is not
on that line, and likewise for `Y`.  Its displayed high grid points and
remaining triples therefore pair all 13 members of `X` bijectively with all
13 members of `Y`.  Hence all eleven `A`-low lines are complete transversals
of the same `13 x 13` pencil grid.

The source transport makes every line individually `F_p`-rational.  Move
`A,B,C` to the coordinate triangle over `F_p` and parameterize the two low
pencils by sets `U,V subset F_p^*`, each of size 13.  If the eleven distinct
transversal slopes are `m_1,...,m_11`, then

```text
U=m_i V,              1<=i<=11.                         (7)
```

Thus the stabilizer `H={h:hV=V}` contains the eleven distinct ratios
`m_i/m_1`.  Multiplication acts freely on `F_p^*`, so `|H|` divides
`|V|=13`.  Since `|H|>=11`, one has `|H|=13`, forcing `13 | (p-1)`.

But for the deployed prime `p=2,130,706,433`, `(p-1) mod 13=10`.  This
contradiction excludes the last row of (2) and proves the theorem.

## Scope

The theorem pays only `D=59` in the two aggregate `q=14,B=42,U=E=0` rows.
It does not pay `D>=60` and makes no recurrence claim by itself.

