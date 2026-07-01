# M1 full-overlap low-tail completion and projection wall

**Status:** PROVED / ROUTE_CUT / AUDIT.

**Paper-B location:** M1 residue-line packing; `def:residue`,
`lem:denom`, `thm:normalform`, `thm:closure`, `conj:B`.

This note records a local residue-line fact that survived the
`M1-FULL-OVERLAP-LOW-TAIL-COMPLETION-OR-PADE-GRAVER-ATOM` audit.  It is not a
leaderboard result, not a Paper-A no-slack example, and not a proof of
`conj:B`.  Its purpose is to separate a proved low-tail completion identity
from the remaining projection-to-Graver wall.

## Setup

Let `F` be a field, let `D` be a finite set of evaluation points, and let
`P_h=F[T]_<h`.  Let `E,B in F[T]` with `E(x) != 0` for all active
`x in D`.  Write

```text
f(x)=B(x)/E(x).
```

For a finite set of vertices `Gamma`, suppose that for each `i in Gamma`
there are a slope `z_i in F`, a low-tail polynomial `R_i in P_h`, and a
support `S_i subset D` such that

```text
Q_i = z_i B + E R_i,
Q_i(x) = w(x)  for all x in S_i,
```

for one common word `w`.  For an edge `e=(i,j)`, let

```text
O_ij = S_i cap S_j
```

be the full overlap, and let `A_ij subset O_ij` be any selected row set.

## Full-overlap completion

On every full-overlap row `x in O_ij`,

```text
R_i(x)-R_j(x) = (z_j-z_i) f(x).
```

Indeed, both witnesses equal `w(x)` on `O_ij`, so

```text
0 = Q_i(x)-Q_j(x)
  = (z_i-z_j)B(x)+E(x)(R_i(x)-R_j(x)).
```

Since `E(x) != 0`, division by `E(x)` gives the identity.  Thus the transition

```text
tau_ij(x) = (z_j-z_i)f(x)
```

is the vertex coboundary `R_i-R_j` on every full overlap, and therefore on
every selected sub-overlap.

Consequently, every honest dual cocycle for the selected or full
`P_h` vertex-coboundary complex annihilates `tau`.  In particular, if

```text
d_A : direct_sum_i P_h -> direct_sum_ij F^{A_ij}
```

is the selected-row coboundary map, and if a functional `lambda_A` satisfies
`d_A^* lambda_A=0`, then

```text
lambda_A(tau_A)=0.
```

This is the higher-tail analogue of the `h=1` active-row completion identity:
genuine support-wise low-tail witnesses do not create nonzero holonomy on an
honest completed coboundary complex.

## Omitted-row extension

The route becomes subtler when a functional is only a projected or partial
functional.  Put

```text
M_ij = O_ij \ A_ij.
```

Let `d_M` denote the omitted-row coboundary map.  A selected functional
`lambda_A` extends to a full-overlap cocycle precisely when there is a
functional `mu_M` on omitted rows such that

```text
d_A^* lambda_A + d_M^* mu_M = 0.
```

Equivalently,

```text
d_A^* lambda_A in -im(d_M^*).
```

In that case the selected value is paid by omitted rows:

```text
lambda_A(tau_A) = -mu_M(tau_M).
```

If no such extension exists, finite-dimensional duality gives
`H in ker(d_M)` with

```text
lambda_A(d_A H) != 0.
```

On a single edge this says that a nonzero polynomial in `P_h` vanishes on the
omitted rows but is visible on selected rows.  For distinct evaluation points,
this forces fewer than `h` omitted rows on that edge.  Thus a nonzero selected
projection is not automatically a Pade--Graver atom; it can instead be a
vertex-boundary projection defect.

## Slope-weighted moment gate

For a selected-row functional

```text
lambda_e = sum_{x in A_e} alpha_{e,x} ev_{e,x},       e=(i,j),
```

define the slope-weighted functional on functions over `D` by

```text
Theta_lambda(P)
  = sum_{e=(i,j)} sum_{x in A_e} alpha_{e,x}(z_j-z_i)P(x).
```

Then

```text
lambda_A(tau_A) = Theta_lambda(f).
```

If

```text
Theta_lambda(P_h)=0
```

and `Theta_lambda(f) != 0`, then a support-minimal subfunctional gives a
Vandermonde/Pade--Graver atom:

```text
mu(P_h)=0,
mu(f) != 0.
```

For distinct rows, such a support-minimal atom has at least `h+1` support
points, and at exactly `h+1` points it is the usual divided-difference
functional.

If instead `Theta_lambda(P_h) != 0`, the obstruction is not a Pade--Graver
atom.  It is a low-tail projection defect.

## Small route cut

The following `F_5` packet shows why the unqualified implication

```text
nonzero projected holonomy => local P_h Pade--Graver atom
```

is false.

Take

```text
D={0,1,2},   h=2,   P_h=F_5[T]_<2,
E=1+T(T-1)(T-2),   B=T.
```

Then `E=1` on `D`, so `f=B/E=T` on all rows of `D`, and hence `f in P_h` on
all active rows.  Let the slopes be

```text
z_1=0, z_2=1, z_3=2
```

and let

```text
S_1={0,2},   S_2={0,1},   S_3={1,2},
w(0)=0, w(1)=1, w(2)=0.
```

The low-tail witnesses are

```text
R_1=0,   R_2=0,   R_3=-3T+2.
```

They satisfy `Q_i=z_iB+ER_i=w` on `S_i`.  On the selected one-row overlaps

```text
A_12={0},   A_23={1},   A_31={2},
```

the sum of the three selected evaluations annihilates constants but has
nonzero value on the transition:

```text
lambda(tau)=2 in F_5.
```

However, since `f=T in P_h` on all of `D`, no functional `mu` with
`mu(P_h)=0` can satisfy `mu(f) != 0`.  The packet is therefore a projection
defect, not a local `P_h` Pade--Graver atom.

This does not contradict full-overlap completion.  It only cuts the
unqualified extraction slogan.

## Fixed-pencil alternative

On a connected nonzero-slope full-overlap component, suppose every completed
overlap has at least `h` distinct rows.  If `f` agrees on the union of overlap
rows with some `P in P_h`, then

```text
R_i-R_j = (z_j-z_i)P
```

as polynomials on every edge.  Hence

```text
R_i + z_i P = R_j + z_j P
```

throughout the component, so

```text
R_i = C - z_i P
```

for one `C in P_h`.  Thus an `h`-rich connected component with no distributed
atom collapses to a fixed-pencil branch.

## Remaining wall

The next exact target is

```text
M1-PROJECTION-TO-GRAVER-SATURATION-OR-VERTEX-BOUNDARY-DEFECT.
```

For a selected/projected functional with `lambda_A(tau_A) != 0`, prove a
trichotomy:

```text
1. full-overlap completion:
   lambda_A extends to a full cocycle, so omitted rows pay the selected value;

2. Graver saturation:
   Theta_lambda(P_h)=0 and Theta_lambda(f)!=0, so a support-minimal
   Vandermonde/Pade--Graver atom exists;

3. vertex-boundary projection defect:
   Theta_lambda(P_h)!=0 or d_A^*lambda_A is not absorbable by omitted rows,
   exposing an explicit low-tail projection-defect branch.
```

This is the current Paper-B-native obstruction.  It should be attacked before
claiming any residue-line packing payment from projected holonomy.
