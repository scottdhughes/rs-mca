# Hostile audit 1: rank-16 weighted-grid extactic/DPW theorem

## Verdict

```text
PASS, with exact scope:
in one source-owned fixed-pair active pencil, occupancy <=155
for every literal core 0<=c<=553.
```

No counterexample was found.  The proof is valid over the deployed field;
it does not use a characteristic-zero transfer.  Combined with the separately
frozen direction-pair payment for `554<=c<=832`, it supplies a local
per-active-pencil cap throughout the currently relevant core band.  It does
**not** prove the active-hyperplane cap `<=1417`, eliminate the rank-16 parent
state, activate a recurrence payment, or change the official score from
`0/2`.

The downloaded proof had one rendering byte `0x08` in place of the two
characters `\\b` in `\\binom` at equation (18).  The canonical work copy
changes only that byte-level typo; no mathematical text was changed.

## 1. Frozen source interface

The theorem consumes exactly the source facts already proved in
`RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md`:

1. saturated endpoint-neighbor intersections are complete actual received-word
   agreement sets, not selected representatives;
2. for a neighbor `P`, its complete tail
   `T_P=A(P)\(A(P_0) union A(P_1))` has
   `|T_P|>=62,356+c`;
3. the tail union is contained in an actual universe of size at most
   `913,633`;
4. common neighbors form a simple row-column graph, with row and column
   degrees at most 14 and
   `r,t<=floor((72,588-c)/(5,116-c))-1`;
5. tails of row-sharing or column-sharing neighbors are disjoint, while any
   other pair intersection is at most `d=5,116-c`;
6. every tail coordinate restricts to a nonconstant affine parameter line,
   and all coordinate copies with one primitive direction have total
   multiplicity at most `d`.

The apparent possibility of a constant coordinate section causes no gap: a
tail coordinate lies outside both endpoint agreement sets, so its agreement
equation cannot be the whole plane; an empty section contributes no tail.
The source proof uses complete agreement sets, so selecting 156 neighbors
does not introduce a support-reselection assumption.

For `0<=c<=553`, the row ceiling is 13 through `c=296` and 14 thereafter.
A simple grid containing 156 edges therefore has exactly one of the eight
ordered size pairs printed in the theorem.  A tail line is distinct from all
skeleton lines and meets each occupied row and column once at most, giving
the literal incidence cap `k_P`-sum `I<=min(r,t)e` in each color.

## 2. Direction coloring and reduced arrangements

Each primitive direction class has at most `d` coordinate copies.  Assigning
the copies of each class injectively to the `d` currently least-loaded colors
preserves the invariant that all color loads differ by at most one.  Hence

```text
e_j<=ceil(913,633/d)<=201.
```

Two copies of one geometric line have the same primitive direction and thus
receive different colors.  Tail lines cannot equal a row, column, or the
endpoint line because they contain neither endpoint.  Consequently every
color really is a reduced line arrangement of degree

```text
D=e+r+t+1<=230<p.
```

No fictitious line is added.  The proof only replaces an actual color load by
the uniform upper bound `E(c)` inside a monotone maximization.

## 3. Characteristic-valid DPW bundle calculation

Let `f` be a reduced degree-`D` plane curve with `p` not dividing `D`.  Euler
expresses `f` through its partials.  Locally on an affine chart, the gradient
scheme of the present reduced line arrangement is a zero-dimensional complete
intersection; thus the kernel bundle in

```text
0 -> E -> O^3 -> I_Sigma(D-1) -> 0
```

is locally free of rank two, with

```text
c1(E)=1-D,
c2(E)=(D-1)^2-tau.
```

A degree-`rho` minimal Jacobian relation has no common polynomial factor, so
its section of `E(rho)` has a zero-dimensional zero scheme `Z` and gives

```text
0 -> O -> E(rho) -> I_Z(2rho+1-D) -> 0.
```

Taking `c2` yields exactly

```text
length(Z)=(D-1)(D-rho-1)+rho^2-tau.
```

This proves the uncorrected bound by nonnegativity.  If
`alpha=2rho+1-D>0`, twist down once.  Minimality gives
`H0(E(rho-1))=0`, while `H0(O(-1))=H1(O(-1))=0`; hence
`H0(I_Z(alpha-1))=0`.  Restriction of degree-`alpha-1` forms to `Z` is
injective, so

```text
length(Z)>=h0(O(alpha-1))=binom(alpha+1,2).
```

This is precisely the correction used by the scan.  All local ordinary
multiple-point Tjurina lengths are `(m-1)^2`: here `m<D<p`, so the Euler
division by `m` is valid.  Thus the identity

```text
tau=binom(D,2)+sum_x binom(m_x-1,2)
```

and the marked-point lower ledger have no positive-characteristic defect.

## 4. Divisorial stripping equalities

Represent the minimal Jacobian syzygy by a projective logarithmic field of
degree `rho`, and write its full divisorial zero as a scalar divisor of degree
`z`.  Let `h0` be the number of distinct arrangement lines occurring in that
divisor.  After division, only those `h0` lines can lose tangency: every other
arrangement line is coprime to the scalar divisor.  The remaining field has
degree `rho-z`, isolated zeros, and is logarithmic for the product of the
`D-h0` surviving lines.

Because `0<D-h0<p`, subtracting its cofactor divided by `D-h0` times the
Euler field gives a nonzero Jacobian syzygy of the remaining product.  Hence

```text
rho'<=rho-z.
```

Conversely, multiplying a minimal remaining syzygy by the product of the
deleted lines produces a full logarithmic field; subtracting its cofactor
divided by `D` times Euler gives a nonzero full Jacobian syzygy.  Hence

```text
rho<=rho'+h0.
```

Since every deleted arrangement line contributes at least one to `z`, these
two inequalities force

```text
z=h0 and rho'=rho-h0.
```

Thus no non-arrangement component or repeated arrangement component is being
silently discarded, and the stripped field used by the extactic lemma really
has isolated zeros.

## 5. Extactic pencil lemma over the literal characteristic

Move one invariant line to infinity.  Tangency to it gives an affine field

```text
delta=P d/dx+Q d/dy,  deg(P),deg(Q)<=q,
```

and isolated zeros give `gcd(P,Q)=1`.  The first line-extactic polynomial

```text
X=P delta(Q)-Q delta(P)
```

has degree at most `3q-1`.  Every invariant affine line divides `X`.  More
than `3q` projective invariant lines leave at least `3q` affine invariant
lines, so `X=0`.

If `Q/P` is not constant, take the generic fiber
`G_lambda=Q-lambda P`.  Coprimality and `X=0` imply
`G_lambda | delta(G_lambda)`.  For an irreducible component `g` of
`G_lambda`, the generic multiplicity is at most `deg(G_lambda)<=q<p`; its
multiplicity is therefore nonzero in the field, and valuation gives
`g|delta(g)`.  Modulo `g`, this becomes

```text
g | (d/dx + lambda d/dy)g.
```

The derivative has smaller degree unless zero.  In coordinates
`u=x, v=y-lambda x`, the kernel is `K(lambda)[u^p,v]`; degree `<p` removes
all `u^p` terms.  Hence every generic irreducible component is a line
`v=constant`.  This is the exact point where `q<p` prevents an inseparable
counterexample.

The generic component lines form a reduced algebraic curve `C` in the dual
plane.  A general primal point has `P!=0`, determines the unique value
`lambda=Q/P`, and lies on exactly one component of that fiber.  Therefore
its dual line meets `C` in exactly one point.  Bezout for a general dual line
gives `deg(C)=1`, so `C` is a dual line and the generic components form one
primal pencil.  Equality of the polynomial line field on a dense open set
then forces every exceptional invariant line into the same pencil.  This
fills the only compressed step in the submitted generic-fiber/dual-curve
paragraph; no characteristic-zero foliation theorem is imported.

## 6. Near-pencil incidence signs

On the branch `3rho<D`, stripping leaves

```text
(D-h0)-3(rho-h0)=D-3rho+2h0>0,
```

so the surviving arrangement is a pencil.  Its center cannot be on the fixed
endpoint line.  At the endpoints at most 15 arrangement lines occur; at any
other point of that line there are the fixed line and at most one transverse
of that direction.  But `D-h0>=D-rho>=18` for the smallest possible
`D=26` on this branch.

An affine center contains at most one row and one column.  Therefore at least
`r+t-1` skeleton lines were stripped, so

```text
h0>=r+t-1 and rho>=r+t-1.
```

If `m` surviving transverse lines lie in the pencil, then

```text
m>=e-rho+r+t-1.
```

Their total incidence with the 156 grid points is at most `m+155`, whether
or not the center is selected.  Every other transverse has at most
`s=min(r,t)` incidences.  Because the coefficient of the lower bound for `m`
is negative after expansion, the safe substitution direction is

```text
I<=e+155+(s-1)(rho-r-t+1).
```

This reproduces exactly the branch constraint in both scans.

## 7. Exact replay and pins

The primary standard-library scan byte-matches under normal and optimized
Python.  The independent Ruby implementation byte-matches under normal and
warnings modes, with empty warning output.  Both reproduce the global
minimum

```text
c=12, color cap=1816, total margin=460,544,
```

and the endpoint

```text
c=553, color cap=2029, total margin=555,477.
```

Downloaded source pins:

```text
proof input
  b7cb50f722f99a1d013a78bb322bcd5aa8741485ba257f68a16ea7d3087d2160
primary verifier
  64a586f0b4b2bf2f502adad65ab369653fb569a83134d8a15a7831f7fe035d8b
primary output
  c77070bf2e3529a904fdba270a4f2fd636ed3a969e8341efe1662b3fc65c73a8
independent verifier
  d4f815be46b699577b5e6c8b91af2edc3dd6bb2a2ce41bca2e51f959500c3610
independent output
  b385c79b8e12a1f94f67c36d0f55d75998fdfc3166b479721421613c01c48408
```

Canonical work pins:

```text
proof after the one-byte rendering repair
  09fbf955ee629381a2f4b5f62fcbc0893852668a755c0df79d3daac9cbf9f59f
primary verifier
  64a586f0b4b2bf2f502adad65ab369653fb569a83134d8a15a7831f7fe035d8b
primary output
  c77070bf2e3529a904fdba270a4f2fd636ed3a969e8341efe1662b3fc65c73a8
independent verifier
  d4f815be46b699577b5e6c8b91af2edc3dd6bb2a2ce41bca2e51f959500c3610
independent output
  b385c79b8e12a1f94f67c36d0f55d75998fdfc3166b479721421613c01c48408
```

Frozen source pins:

```text
RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md
  4229a4859dd3ebec80e646428b8a0a7a1914b7f56638e386a7a7f33b5568080d
source verifier
  2c92befebb461824707a9d9906bc1ea0218079f967ab2058dfa36d895e6e2813
source output
  7232ca26d81a7c56930da46112914ef75220831a338a779a042b10d3ccf72467
```

Canonical replay:

```text
python3 work/verify_rank16_weighted_grid_extactic_dpw.py
python3 -O work/verify_rank16_weighted_grid_extactic_dpw.py
ruby --disable-gems work/verify_rank16_weighted_grid_extactic_dpw_independent.rb
ruby --disable-gems -w work/verify_rank16_weighted_grid_extactic_dpw_independent.rb
```

## Explicit nonclaims

- No active-hyperplane occupancy bound `<=1417` is proved.
- No fixed-pair common-neighbor aggregate is paid merely by this local cap.
- No rank-16 parent state or recurrence child is eliminated here.
- No claim is made for a core outside `0<=c<=553` by this theorem alone.
- No Grand List or Grand MCA official conclusion is proved.
