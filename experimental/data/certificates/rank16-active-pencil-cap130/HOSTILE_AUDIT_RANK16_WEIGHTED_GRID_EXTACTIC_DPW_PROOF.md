# Hostile audit: rank-16 weighted-grid extactic/DPW theorem

## Verdict

```text
PASS AS A SOURCE-VALID LOCAL THEOREM
ACTIVE-PENCIL OCCUPANCY <=155 FOR c=0..553
COMPOSED WITH THE FROZEN SOURCE: <=155 FOR c=0..832
NO ACTIVE-HYPERPLANE CAP, RANK-16 STATE PAYMENT, OR SCORE MOVEMENT
```

The return is not an R18 projective-ray answer.  It answers the independent
prompt

```text
work/sol_pro_prompts/ROLE1_WEIGHTED_GRID_ARRANGEMENT.md
```

and proves the exact local lemma requested there.  Its arithmetic was replayed
by the attached independent Ruby implementation over every core
`c=0,...,553`; the minimum contradiction margin is `460,544`, at `c=12`, and
the `c=553` margin is `555,477`.

## Frozen objects

```text
work/RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md
sha256 4229a4859dd3ebec80e646428b8a0a7a1914b7f56638e386a7a7f33b5568080d

work/verify_rank16_fixed_pair_active_pencil_grid_tail_cut.rb
sha256 2c92befebb461824707a9d9906bc1ea0218079f967ab2058dfa36d895e6e2813

work/RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT_OUTPUT.txt
sha256 7232ca26d81a7c56930da46112914ef75220831a338a779a042b10d3ccf72467

work/sol_pro_prompts/ROLE1_WEIGHTED_GRID_ARRANGEMENT.md
sha256 546639f510da27c7fee631e6ec27db7d280d509579c7344e69c0e61399c74992

/Users/danielcabezas/Downloads/RANK16_WEIGHTED_GRID_EXTACTIC_DPW_PROOF.md
sha256 b7cb50f722f99a1d013a78bb322bcd5aa8741485ba257f68a16ea7d3087d2160

/Users/danielcabezas/Downloads/verify_rank16_weighted_grid_extactic_dpw.py
sha256 64a586f0b4b2bf2f502adad65ab369653fb569a83134d8a15a7831f7fe035d8b

/Users/danielcabezas/Downloads/verify_rank16_weighted_grid_extactic_dpw.out
sha256 c77070bf2e3529a904fdba270a4f2fd636ed3a969e8341efe1662b3fc65c73a8

/Users/danielcabezas/Downloads/verify_rank16_weighted_grid_extactic_dpw_independent.rb
sha256 d4f815be46b699577b5e6c8b91af2edc3dd6bb2a2ce41bca2e51f959500c3610

/Users/danielcabezas/Downloads/verify_rank16_weighted_grid_extactic_dpw_independent.out
sha256 b385c79b8e12a1f94f67c36d0f55d75998fdfc3166b479721421613c01c48408
```

The independent Ruby replay is byte-identical to its supplied expected
output.  The host's `/usr/bin/python3` is an Xcode developer-tools stub, so
the primary Python program was source-inspected but not used as the independent
runtime.  The Ruby program is not a spot check: it exhausts all 554 cores,
every feasible row/column profile, every color size through 201, and every
integer mdr.

## 1. Source ownership is exact

The proof consumes precisely the facts printed in the frozen source theorem,
not an enlargement of the Sol-Pro prompt:

1. Complete actual agreement tails satisfy
   `|T_P|>=62,356+c`; their union has size at most `913,633`.
2. The common-neighbor plane is a simple bipartite row--column grid, with
   `r,t<=R(c)` and row/column degree at most `14`.
3. A tail-coordinate agreement line avoids both endpoints, so it meets any
   row and any column at most once.
4. All coordinate lines in one primitive direction have total coordinate
   weight at most `d=5,116-c`.
5. The frozen theorem already proves the same `155` cap for `c=554..832`.

The new proof uses complete actual tails throughout.  It does not reselect
size-`m` supports, replace a weighted direction by a generic line, or import
an unowned root.

## 2. Balanced direction coloring is valid

Each primitive direction class has at most `d` coordinate copies.  Assigning
one copy to each of `d` colors injectively within every direction, while
always choosing currently least-loaded colors, preserves a load difference
of at most one after every class.  Hence every color has at most

```text
E(c)=ceil(913,633/(5,116-c))<=201
```

transverse lines.  A geometric line has one primitive direction, so no line
is repeated inside a color.  Summing the color incidences recovers every
actual tail incidence exactly.

## 3. The Tjurina and DPW ledgers are characteristic-valid

After adjoining the `r` row lines, `t` column lines, and the endpoint line,
one color has degree

```text
D=e+r+t+1<=230<p=2,130,706,433.
```

Every singularity is an ordinary `m`-fold line-arrangement point with
`m<D<p`.  Euler division is therefore legal and its local Tjurina length is
`(m-1)^2`.  This gives

```text
tau >= C(D,2)+C(r,2)+C(t,2)+sum_P C(k_P+1,2).
```

The submitted du Plessis--Wall bound does not invoke a characteristic-zero
surface theorem.  For the gradient kernel bundle `E`, a minimal degree-`rho`
syzygy gives

```text
0 -> O -> E(rho) -> I_Z(2rho+1-D) -> 0,
length(Z)=(D-1)(D-rho-1)+rho^2-tau.
```

Nonnegativity proves the ordinary bound.  When `alpha=2rho+1-D>0`, minimality
forces `H^0(I_Z(alpha-1))=0`, so restriction of degree-`alpha-1` forms to `Z`
is injective and `length(Z)>=C(alpha+1,2)`.  This proves the corrected bound
in arbitrary characteristic under the already verified degree gate.

## 4. Divisorial stripping is sound

A minimal Jacobian syzygy gives a projective logarithmic vector field of
degree `rho`.  If its zero divisor has degree `z` and contains `h_0` distinct
arrangement lines, division leaves an isolated-zero field of degree
`rho-z`, tangent to the arrangement with those `h_0` lines removed.  Euler
subtraction gives

```text
mdr(remaining)<=rho-z.
```

Conversely, multiplying a minimal logarithmic field for the remaining
arrangement by the product of the deleted line equations and applying Euler
subtraction gives

```text
rho<=mdr(remaining)+h_0.
```

Since `z>=h_0`, the two inequalities force

```text
z=h_0,  mdr(remaining)=rho-h_0.
```

Thus no untracked non-arrangement divisor, repeated deleted line, or hidden
degree loss survives the stripping step.

## 5. The positive-characteristic extactic lemma passes

For an isolated-zero degree-`q` field tangent to an invariant line at
infinity, write the affine field as

```text
delta=P d/dx+Q d/dy,  deg(P),deg(Q)<=q,  gcd(P,Q)=1.
```

Every invariant affine line divides

```text
X=P delta(Q)-Q delta(P),  deg(X)<=3q-1.
```

More than `3q` invariant projective lines therefore force `X=0`.  If `Q/P`
is nonconstant, the generic fiber `G_lambda=Q-lambda P` satisfies
`G_lambda|delta(G_lambda)`.  For every irreducible factor `g_i`, its
multiplicity is at most `q<p`, so valuation gives

```text
g_i | (d/dx+lambda d/dy)g_i.
```

The derivative has lower degree unless zero.  In coordinates
`u=x, v=y-lambda x`, the kernel of `d/du` is `K(lambda)[u^p,v]`; the gate
`deg(g_i)<=q<p` therefore makes every generic component a line.  The reduced
dual family meets the dual line of a general primal point once: that point
has the unique value `lambda=Q/P` and lies on one reduced generic component.
Bezout makes the reduced dual family degree one, hence a pencil.  An
exceptional invariant line has the same direction as the unique pencil leaf
at a general point on it and therefore is that leaf.  This closes the only
positive-characteristic separability hazard; all relevant degrees are below
`p`.

## 6. Near-pencil incidence and finite scan

On the branch `3rho<D`, divisorial stripping plus the extactic lemma makes
the remaining lines a pencil.  Its center cannot lie on the endpoint line:
the surviving pencil has at least `D-rho>=18` lines, whereas endpoint-line
multiplicities are at most `15` at either endpoint and at most `2` elsewhere.
An affine center forces deletion of at least `r+t-1` skeleton lines.  If `I`
is the marked incidence total in the color, this yields

```text
I <= e+155+(min(r,t)-1)(rho-r-t+1).
```

The independent exact scan combines this with DPW and the balanced Tjurina
floor.  It verifies a strict contradiction for every allowed profile.  The
worst two audit rows are

```text
c=12:  need=9,729,408, cap=9,268,864, margin=460,544;
c=553: need=9,813,804, cap=9,258,327, margin=555,477.
```

Deleting the extactic/divisorial branch reopens `c=553`, so this part is
correctly identified as load-bearing.

## 7. Exact compiler impact

The new theorem composes with the frozen `c=554..832` result to give at most
`155` common neighbors in every surviving active pencil, `c=0..832`.  It
subsumes the separate accepted `c=552` and `c=553` local payments.

For the frozen surviving common-neighbor mass,

```text
470,582,804,331,383
  =3,036,018,092,460*155+83,
```

so it forces at least

```text
3,036,018,092,461 active pencils.
```

In the existing projective-incidence compiler this relaxes the still-missing
uniform active-hyperplane input from `Q<=1,046` to the exact new threshold

```text
Q<=1,424.
```

Indeed

```text
floor(1,424 Theta_14/Theta_13)=3,034,125,960,592 < 3,036,018,092,461,
floor(1,425 Theta_14/Theta_13)=3,036,256,667,025 >=3,036,018,092,461.
```

No theorem in the return proves `Q<=1,424`.  Therefore it removes no rank-16
parent state, does not compile either official question, and leaves the
official score at `0/2`.

## Replay

```text
ruby --disable-gems -w \
  work/verify_hostile_audit_rank16_weighted_grid_extactic_dpw.rb
```
