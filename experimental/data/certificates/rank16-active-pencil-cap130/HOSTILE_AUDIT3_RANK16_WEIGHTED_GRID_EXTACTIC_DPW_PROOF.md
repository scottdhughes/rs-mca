# Hostile audit 3: rank-16 weighted-grid extactic/DPW theorem

## Verdict

```text
ACCEPT_LOCAL
one fixed source-owned active pencil has occupancy <=155 for c=0..553
composed with the frozen source payment: occupancy <=155 for c=0..832
no active-hyperplane cap, rank-16 payment, recurrence payment, or score change
```

This audit read the downloaded proof and both verifier implementations in
full, checked the literal source anchors before execution, replayed the
independent Ruby exhaustion with warnings enabled, and replayed the frozen
source/impact audit.  The host's `/usr/bin/python3` is an Xcode stub, so the
primary Python source was inspected line by line and compared with its frozen
output; the independent Ruby program is a complete reimplementation of the
finite scan, not a sample.

## 1. Source and weighted-to-reduced interface

The proof consumes exactly the frozen facts in
`RANK16_FIXED_PAIR_ACTIVE_PENCIL_GRID_TAIL_CUT.md`: complete actual tails have
size at least `62,356+c`, their union has size at most `913,633`, occupied
rows and columns obey the endpoint budget and degree-14 cap, and one primitive
tail direction owns at most `d=5,116-c` coordinate copies.

Coloring each primitive-direction class injectively among `d` colors and
always using least-loaded colors preserves a load spread of at most one.
Thus each color has at most `ceil(913,633/d)<=201` coordinate lines.  A
geometric affine line has one direction, so injectivity removes every line
repetition inside a color.  A tail line contains neither endpoint and hence
cannot be a row, column, or endpoint line.  The resulting arrangement is
therefore genuinely reduced, of degree at most `201+14+14+1=230`.

The color incidences sum exactly to the complete actual-tail incidences.  No
generic line, chosen-support replacement, extension-field denominator, or
unowned root enters this conversion.

## 2. Characteristic and Jacobian checks

All arrangement degrees and local multiplicities are below the literal
prime `p=2,130,706,433`.  Euler division by the arrangement degree, a local
ordinary-point multiplicity, or a remaining arrangement degree is therefore
legal.  The local Tjurina contribution is `(m-1)^2`, and

```text
tau >= C(D,2)+C(r,2)+C(t,2)+sum_P C(k_P+1,2)
```

has the correct signs and counts the two endpoint singularities and all 156
marked grid points without overlap.

The du Plessis--Wall inequality is proved through the gradient kernel bundle.
For a minimal degree-`rho` relation, the zero length is

```text
(D-1)(D-rho-1)+rho^2-tau.
```

When `2rho+1-D>0`, twisting down and minimality give the printed triangular
correction.  This proof is characteristic-valid and uses no Hirzebruch/BMY
transfer.

Dividing the complete divisorial zero and comparing minimal syzygy degrees in
both directions forces `z=h_0` and exact remaining `mdr=rho-h_0`.  Hence no
non-arrangement divisor or repeated arrangement component is discarded.

## 3. Extactic and near-pencil checks

For the stripped isolated-zero degree-`q` field, the affine extactic
polynomial has degree at most `3q-1`.  More than `3q` projective invariant
lines force it to vanish.  In a generic fiber, every factor has multiplicity
at most `q<p`; valuation and the degree-`<p` kernel of the directional
derivative force each generic irreducible component to be a line.  The
reduced dual family meets a general dual line once, so it has degree one and
is a pencil.  This closes the inseparability branch explicitly.

On `3rho<D`, the surviving pencil has at least `D-rho>=18` lines.  Its center
cannot lie on the endpoint line, whose arrangement multiplicities are at
most 15 at an endpoint and 2 elsewhere.  An affine center forces deletion of
at least `r+t-1` skeleton lines.  The resulting incidence inequality

```text
I <= e+155+(min(r,t)-1)(rho-r-t+1)
```

uses the lower bound on surviving pencil transverses in the correct direction.

## 4. Replay and exact scope map

The independent replay prints

```text
RANK16_WEIGHTED_GRID_EXTACTIC_DPW_INDEPENDENT: PASS
uniform minimum: c=12, margin=460,544
c=553 margin=555,477
```

The new theorem's interval is `c=0..553`.  The previously accepted local
interval after the `c=551` hostile audit is `c=551..832`.  Their exact overlap
is the three cores `c=551,552,553`; the strict new extension is `c=0..550`;
their union is `c=0..832`.

For the frozen surviving common-neighbor mass, the uniform cap 155 forces

```text
3,036,018,092,461 active pencils.
```

The unchanged projective incidence compiler would close if every active
hyperplane owned at most `1,424` pencils, while `1,425` already fails.  This
is only a weaker missing input: no theorem here proves `Q<=1,424`, so the
rank-16 parent and official score remain unchanged.

## Pins

```text
downloaded proof       b7cb50f722f99a1d013a78bb322bcd5aa8741485ba257f68a16ea7d3087d2160
canonical proof        09fbf955ee629381a2f4b5f62fcbc0893852668a755c0df79d3daac9cbf9f59f
primary verifier       64a586f0b4b2bf2f502adad65ab369653fb569a83134d8a15a7831f7fe035d8b
primary output         c77070bf2e3529a904fdba270a4f2fd636ed3a969e8341efe1662b3fc65c73a8
independent verifier   d4f815be46b699577b5e6c8b91af2edc3dd6bb2a2ce41bca2e51f959500c3610
independent output     b385c79b8e12a1f94f67c36d0f55d75998fdfc3166b479721421613c01c48408
frozen source theorem  4229a4859dd3ebec80e646428b8a0a7a1914b7f56638e386a7a7f33b5568080d
```
