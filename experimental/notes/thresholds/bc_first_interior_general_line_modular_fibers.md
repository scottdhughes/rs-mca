# First-interior general-line BC: exact modular-locator normal form

## Claim

At the first interior interpolation-lattice profile

```text
d1 = w+2,                 d2 = omega-1,
m = K+w,                  omega = n-m,
```

an arbitrary balanced-core chart has an exact normal form that eliminates the
raw `A` coordinate and exposes more structure.  No dimension or complexity
shrink is claimed.  Every valid census element is encoded by a monic degree-`m`
divisor `V | Lambda_D` and a degree-`<K` polynomial `c` satisfying two
determinant-derived divisibilities.  The small multiplier `B` has degree at
most one.

For a fixed nonzero `B`, the first divisibility is an affine fiber of a linear
map into

```text
P_{<=m+1} / (W1 P_{<K}),
```

whose dimension and rank are exact.  When `W1` is constant, its algebraic shape
matches the depth-`(w+1)` Q decomposition of the planted packet
`cap25_v13_bc_l4_interior_chart_to_q.md`; identifying it with that base-field
packet still requires the packet's field and confinement hypotheses.  When
`W1` is nonconstant, the fiber has both high-coefficient and
remainder-mod-`W1` constraints and is not an ordinary prefix fiber.  This
packet names that remaining object a **modular-locator fiber**.

The result turns the general first-interior chart into a named
higher-dimensional residual.  It does **not** prove a row-sharp bound for that
residual and therefore does not close `prob:saturated-bc` or a deployed upper
ledger.

## Status

- `PROVED`: the exact two-divisibility normal form, determinant gluing law,
  fixed-`B` rank formula, planted-shape specialization, and the `B=0`
  at-most-one-word-ray branch.
- `EXPERIMENTAL`: the exact `F_97 / mu_16` general-line preflight and its
  rank-two minimal-denominator fixture, which the audit routes through
  slice-local common-`D`-GCD cells before first match.
- `PROVED-SPECIAL`: the follow-up
  `bc_first_interior_f97_two_cell_certificate.md` factors those two cells,
  enumerates both residual planes, and proves the exact three-slope budget for
  the pinned retained subincidence.
- `OPEN GAP`: a row-sharp bound for the modular-locator fibers and a
  witness-exhaustive first-match classification of arbitrary lines.

The Lean module

```text
experimental/lean/grande_finale/GrandeFinale/BCFirstInteriorGeneralLine.lean
```

proves the determinant identities and records numerical rank/compiler target
shapes explicitly labelled `UNPROVED STATEMENT TARGETS`.  Those numerical
placeholders do not formalize the polynomial quotient map, its rank theorem,
or the coding-theoretic compiler.

## Parameters and field ledger

Let `F` be a field, let `D subset F` contain `n` distinct points, and put

```text
Lambda_D(X) = product_(x in D) (X-x).
```

Fix `C = RS_F(D,K)`, a received word `U`, agreement size `m=K+w`, and
`omega=n-m`.  Let

```text
g1=(W1,N1),  g2=(W2,N2)
```

be a shifted weak-Popov basis of the interpolation lattice `M_U`, with
`W1 != 0` and first interior profile

```text
d1=w+2 <= d2=omega-1=n-K+1-d1,
W1 N2-W2 N1=gamma Lambda_D,       gamma in F^*.
```

All coefficient-space ranks below are over the field in which this basis and
the multiplier cell are defined.  If that field is an extension `F` of a base
field `B`, an `|F|`-fiber statement cannot be charged to an `|B|` ledger without
a separate confinement or transfer theorem.  The toy experiment has `F=B=F_97`
and therefore cannot audit that extension-field step.

## 1. Exact first-interior normal form (`PROVED`)

### Theorem 1 (two-divisibility normal form)

A census element has the unique weak-Popov representation

```text
(W,N) = A g1+B g2,
W monic,  deg W=omega,  W|Lambda_D,  N=Wc,  deg c<K.
```

Predictable degrees give

```text
deg A <= omega-w-2,        deg B <= 1.                 (1)
```

Put

```text
V=Lambda_D/W.
```

Then `V` is monic, `D`-split, and has degree `m`, and

```text
W1 c-N1 = gamma B V,                                  (2)
N2-W2 c = gamma A V.                                  (3)
```

Conversely, let `V` be any monic degree-`m` divisor of `Lambda_D`, and let
`c` have degree `<K`.  If

```text
V | (W1 c-N1),              V | (N2-W2 c),             (4)
```

then

```text
B=(W1 c-N1)/(gamma V),
A=(N2-W2 c)/(gamma V)                                (5)
```

satisfy (1), and

```text
A W1+B W2=Lambda_D/V,
A N1+B N2=c Lambda_D/V.                               (6)
```

Thus (4)--(6) give an exact bijective normal form for the census chart.

### Proof

For a census element, multiply `N=Wc` by `W1` and subtract `N1W`.  The `A`
terms cancel, while the determinant evaluates the `B` terms:

```text
W(W1c-N1)
 = W1(AN1+BN2)-N1(AW1+BW2)
 = B(W1N2-W2N1)
 = gamma B W V.
```

Cancel the nonzero polynomial `W` to obtain (2).  The symmetric calculation
gives (3).

For the converse, the two quotients in (5) exist.  Since
`deg(W1c-N1)<=m+1`, division by the degree-`m` polynomial `V` gives
`deg B<=1`.  Since `d2=omega-1`, both `N2` and `W2c` have degree at most
`K+omega-2`; division by `V`, of degree `K+w`, gives
`deg A<=omega-w-2`.  Finally,

```text
W1(N2-W2c)+W2(W1c-N1)=gamma Lambda_D,
```

so substitution of (5) gives the first identity in (6).  The same expansion
with `N1,N2` gives the second.  The resulting `W=Lambda_D/V` is monic and
`D`-split, and `N=Wc` has the required shifted-degree cap.  Uniqueness follows
from the uniqueness of both the weak-Popov coordinates and `V=Lambda_D/W`.

### Gluing law

The first divisibility in (4) is the low-parameter modular fiber.  It does not,
by itself, always imply the second divisibility.  If

```text
G=gcd(V,W1),
```

then the determinant identity implies automatically only

```text
V/G | (N2-W2c).
```

The remaining condition is exactly

```text
G | (N2-W2c).                                           (7)
```

Here `Lambda_D` is squarefree because the points of `D` are distinct.  Hence
its divisor `V` is squarefree and `gcd(G,V/G)=1`; this is the step that makes
the remaining condition exactly (7), rather than merely necessary.

In particular, the first divisibility implies the second whenever
`gcd(V,W1)=1`.  Equation (7) is the load-bearing gluing condition on supports
meeting roots of `W1`; dropping it would turn a necessary modular-fiber
overcount into a false exact parametrization.

## 2. Fixed-multiplier modular fibers (`PROVED`)

Write `P_{<=r}` for the `F`-vector space of polynomials of degree at most `r`.
For a fixed nonzero polynomial `B` of degree `b<=1`, define

```text
L_B : P_{<=m} -> P_{<=m+1}/(W1 P_{<K}),
      V |-> B V mod W1 P_{<K}.                          (8)
```

Multiplication by the nonzero scalar `gamma` does not change its rank.  The
first condition in (4) places `V` in the affine fiber

```text
L_B(V)=[-N1/gamma].                                     (9)
```

The exact census is the subset of (9) cut out by `V|Lambda_D`, monicity,
degree `m`, and the gluing condition (7).

### Theorem 2 (exact ranks)

Assume `K>=3`, `W1!=0`, and `w+2<=omega-1`.  Put

```text
d=deg W1,      b=deg B,      e=deg gcd(B,W1),
0<=d<=w+2,     0<=b<=1.
```

Then

```text
dim P_{<=m+1}/(W1 P_{<K}) = w+2,                        (10)

rank L_B = max(d,w+1+b)-e.                              (11)
```

On the affine space of monic degree-`m` polynomials, the direction space is
`P_{<=m-1}`, and the restricted rank is

```text
rank_monic L_B = max(d,w+b)-e.                          (12)
```

Consequently every nonempty fixed-`B` monic fiber in (9) has codimension
exactly the number in (12).

### Proof

The subspace `W1 P_{<K}` has dimension `K` inside the `(m+2)`-dimensional
space `P_{<=m+1}`, proving (10).  Put `g=gcd(B,W1)`, write

```text
B=g B0,       W1=g W10,       gcd(B0,W10)=1.
```

The kernel of (8) consists of the `V` for which `BV=W1c` with `deg c<K`.
Coprimality forces

```text
V=W10 H,       c=B0 H.
```

For `V in P_{<=m}`, the degree of `H` is at most

```text
min(m-d+e, K-1-b+e).
```

Thus the kernel dimension is
`1+min(m-d+e,K-1-b+e)`.  Subtracting it from `m+1`, and using `m=K+w`,
gives (11).  On the monic direction space `P_{<=m-1}`, the kernel dimension is
`1+min(m-1-d+e,K-1-b+e)`, which gives (12).  The assumptions ensure the
displayed degree bounds are nonnegative.

## 3. Structural branches at `d1=w+2`

### 3.1 `B=0`: at most one word-ray per received word (`PROVED`)

If `B=0`, equation (2) gives `N1=W1c`.  Every valid element is

```text
(W,N)=A(W1,N1)=A W1(1,c),
```

so all raw support representatives belong to the same codeword ray `c`.
They may have a large saturation multiplicity, but they contribute at most one
deduplicated ray for the word.  When normalized `W1` is `D`-split of degree
`w+2`, the raw multiplicity is `binom(n-w-2,m)`; this is precisely why the
support census and the LineRay count must not be conflated.

This is a per-word statement.  It does not bound how many slopes of one
received line have `B=0`, so no line-level first-match payment follows here.

### 3.2 Strict numerator-leading case: mixed depth `w+1` (`PROVED`)

Suppose

```text
d=deg W1<=w+1.
```

Since the shifted row degree is `w+2`, necessarily `deg N1=m+1`.  A constant
`B` cannot produce a degree-`omega` locator: both `AW1` and `BW2` would have
degree at most `omega-1`.  Hence every full-degree element has linear `B`.
Because `V` is monic, (2) fixes the leading coefficient of `B`, leaving one
affine parameter.

For a linear `B` coprime to `W1`, (12) gives

```text
rank_monic L_B=w+1.                                    (13)
```

Equivalently, after the automatic degree-`m+1` cancellation, the condition

```text
N1+gamma B V in W1 P_{<K}
```

consists of

```text
w-d+1 high-coefficient equations  +  d remainder equations = w+1.  (14)
```

For `d=0`, there is no remainder condition and (14) is exactly the ordinary
depth-`(w+1)` prefix recursion of the planted packet.  For `d>0`, it is a
genuine mixed head-plus-remainder fiber.  No theorem in the repository turns
those arbitrary modular conditions into ordinary Q with a row-affordable
loss.

### 3.3 Full denominator degree: modular depth `w+2` (`PROVED`)

If

```text
d=deg W1=w+2,
```

then every fixed nonzero `B` coprime to `W1` has

```text
rank_monic L_B=w+2.                                    (15)
```

Linear, constant, and zero multipliers can occur,
depending on the top coefficient of `c`.  The nonzero fixed-`B` conditions are
degree-`(w+2)` modular fibers.  Allowing the two coefficients of a linear `B`
again leaves nominal effective depth `w`, but that dimension balance is not a
split-locator count.

### 3.4 Common factor of `B` and `W1`: slice-local fixed `D`-root (`PROVED`)

The only possible nonconstant gcd has degree one.  If `B` and `W1` share the
root `alpha` and the fiber (9) is nonempty, (2) gives `N1(alpha)=0`.  The
determinant identity then gives `Lambda_D(alpha)=0`, so `alpha in D`.  Moreover

```text
(A W1+B W2)(alpha)=0
```

for every `A` in that fixed-`B` slice.  The one-rank loss in (11)--(12) is
therefore a genuine slice-local fixed-domain-root/common-GCD locus, not an
unexplained generic rank drop.  This is a classification for the fixed-`B`
slice; paying all such slices in a line ledger still requires the explicit
first-match common-GCD owner.

## 4. Named residual input and its conditional payment

For fixed `B` and a monic divisor `V` for which the quotient exists, define

```text
c_(B,V)=(N1+gamma B V)/W1,       G_V=gcd(V,W1).
```

Define the glued modular-locator fiber, with the full basis and field data
understood, by

```text
MLFib_B(W1,N1,W2,N2,gamma,Lambda_D,K,m)
 = {monic V: deg V=m, V|Lambda_D,
      c_(B,V) exists with deg c_(B,V)<K,
      gcd(V,W1) | (N2-W2 c_(B,V))}.                     (16)
```

The exact raw census coordinates satisfy

```text
Cen(U;m)=sum_(deg B<=1) |MLFib_B|.                      (16a)
```

The coordinates are disjoint because `B` and `V=Lambda_D/W` are unique.  Ray
deduplication is different: all `B=0` coordinates give at most one word-ray,
and distinct nonzero `(B,V)` coordinates can also collide to one ray.  Hence

```text
|Ray(U;m)| <= 1+sum_(0!=B, deg B<=1) |MLFib_B|.         (16b)
```

After the slice-local `gcd(B,W1)!=1` loci have been assigned to the earlier
common-GCD first-match owner, the following remains a logically sufficient
fixed-word input over a coefficient field of size `s`:

```text
|MLFib_B| <= R_B binom(n,m) s^(-rank_monic L_B)          (17)
```

It must hold uniformly over the remaining nonzero multipliers with
`gcd(B,W1)=1`.  The exact rank exponent does not make `R_B` small.  The
follow-up packet
`bc_first_interior_modular_subset_product.md` proves that on a root-free
chart one sufficient Fourier choice is

```text
R_B^Fourier := kappa(W1) (1+A_(W1,h)),                  (17a)
```

where `A_(W1,h)` is an explicit nontrivial mixed character mass.  Moreover,
if `binom(n,m)s^(-rank_monic L_B)<1`, every nonempty integer fiber forces any
admissible `R_B` to be at least the reciprocal of that scale.  This occurs in
the full-denominator slice of both deployed rows and already forces 26.24 and
41.26 optimistic bits respectively.

Consequently, naively adding separately rounded estimates over at most `s` or
`s^2` multiplier slices can leave a dominant slice-count term.  The exact
rank identities identify the nominal exponent only; they do not prove the
previously claimed fixed-word dimension balance.  For `d=0`, the character
object specializes to ordinary Q.  For `d>0`, it is a genuinely mixed
truncated-locator/quotient-algebra subset-product problem.

A useful finite compiler therefore needs a mixed character theorem, an
aggregate occupancy bound across multipliers, ray deduplication, or a direct
slope-image bound.  In every case (16b)--(17) remain fixed-word statements;
line-level payment still requires the first-match slope projection and
uniformity along the received line.

## 5. Deployed dimensions (`AUDIT`)

For the two active MCA rows, the general first-interior coefficient caps are:

| row | `omega` | `w` | `(d1,d2)` | `deg A` cap | `deg B` cap | raw coefficient dimension |
|---|---:|---:|---:|---:|---:|---:|
| KoalaBear MCA | 981104 | 67471 | (67473, 981103) | 913631 | 1 | 913634 |
| Mersenne-31 MCA | 981128 | 67447 | (67449, 981127) | 913679 | 1 | 913682 |

The normal form replaces the misleading impression of an unstructured
`913k`-dimensional `A` search by an at-most two-parameter union of exact modular
locator fibers.  This is a structural elimination, not a proved dimension or
complexity shrink; it does not shrink the field ledger or prove (17).

## 6. Exact `F_97 / mu_16` preflight (`EXPERIMENTAL`)

The stdlib-only script

```text
experimental/scripts/experiment_bc_first_interior_general_line.py
```

uses the two first-interior toy rows

```text
F=F_97, D=mu_16, (K,m,w,d1)=(4,6,2,4) and (5,7,2,4).
```

It enumerates every support, solves its affine slope equations, recomputes the
shifted weak-Popov profile at all 97 slopes, deduplicates to `(slope,codeword)`
LineRay pairs, checks saturation, recovers `A,B`, and verifies (2)--(3), (9),
and the fixed-`B` ranks exactly.

The non-sparse polynomial controls exercise the constant-`W1` planted/Q shape:
their retained cases have `deg W1=0`, linear coprime `B`, full rank `4=w+2`,
and monic-direction rank `3=w+1`.

The deterministic row-B fixture exercises the full-denominator side:

```text
d1 histogram over slopes       {4: 3, 6: 94}
raw supports / LineRay / slopes 126 / 105 / 68
common supports                 0
retained d1=4 LineRay/slopes    4 / 3
fixed-B full/direction ranks    4 / 4
gcd(B,W1) degree               0 in all four retained pairs
minimal-denominator affine rank 2
minimal-denominator projective dimension 2
error-locator transversal gcd degrees {1,2}; zero-gcd transversals 0
common gcd across all four error locators degree 0
```

The selected minimal denominators have affine rank and projective dimension
two and are pairwise coprime; the rank statement therefore rules out
containment in one projective minimal-denominator pencil.  First-match
common-GCD concerns the degree-`omega` error locators, however.  There are two
one-per-slope transversals: their common `D`-root sets have indices `{15}` and
`{10,13}` respectively, so every transversal has a positive common-GCD.  The
four retained locators together have trivial gcd, but they are coverable by
two fixed-root cells.  The fixture is therefore routed by common-GCD before it
can become a residual witness.

The follow-up verifier enumerates all `9507` points of each residual
projective plane and, independently, all `6435` and `3432` split-divisor
candidates.  Each plane contains exactly three claimed split locators, the
two cells cover all four retained `LineRay`s, and ordered first match assigns
slope parts `{0,1,2}` and the empty set.  Hence the exact pinned slope budget
is `3`.

It refutes only the pre-common-GCD simplification that every general
first-interior line automatically has a rank-one minimal-denominator core.  It
does not refute `prob:saturated-bc`, which explicitly permits paid
decompositions or a named residual with its own slope bound.

### Honest first-match scope

The preflight exactly removes common size-`m` supports and cyclic-periodic
support representatives.  The separate two-cell certificate is
witness-exhaustive for this retained four-`LineRay` subincidence: it diagnoses
the selected error-locator common-GCD transversals and proves their exact
ordered first-match budget.  Neither script implements a witness-exhaustive
tangent classifier for arbitrary lines, and `q=p` makes extension/subfield
confinement inapplicable.  Before that fixture-specific certificate, the
preflight's retained class is therefore

```text
PRE_FIRST_MATCH_CANDIDATE_WITH_COMMON_GCD_ROUTING,
```

not a certified deployed post-first-match witness.

## 7. Replay

```sh
python3 experimental/scripts/experiment_bc_first_interior_general_line.py --max-attempts 1
```

The pinned seed is `20260715`; the fixture is found on the first deterministic
denominator-triple attempt.  A successful run ends with

```text
RESULT: EXPERIMENTAL RANK>=2 PRE-FIRST-MATCH FIXTURE; COMMON-GCD ROUTING PRESENT
```

## Ledger impact

- **Balanced-core residual ray compiler:** sharpened from an unstructured
  high-dimensional coefficient family to the exact modular-locator residual
  (16).
- **Q:** the planted `W1=1` chart still reduces to depth-`(w+1)` Q; the general
  nonconstant-`W1` chart does not.
- **Finite adjacent rows:** no row moves; (17) remains open and field-ledger
  transfer is not supplied.
- **First-match atlas:** the toy fixture is an adversarial example for the
  pre-excision single-pencil simplification and is then routed by fixed-root
  common-GCD cells; it is not an atlas counterexample.

## Nonclaims

- No bound on the complete `LineRay` census is proved.
- No deployed `U(a0+1)<=B*` inequality is proved.
- No base-to-extension or extension-to-base transfer is asserted.
- No tangent, quotient, extension, or complete common-GCD atlas classifier is
  inferred from the toy.
- No claim is made that affine rank two alone defeats a valid pencil
  decomposition with a bounded number of paid pieces.
