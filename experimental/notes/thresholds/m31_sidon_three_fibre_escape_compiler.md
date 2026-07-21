# M31 Sidon source wall, three-fibre compression, and escape compiler

## Status

**PROVED exact same-weight rank extraction / PROVED sharp support-only
source-selection wall / PROVED conditional three-fibre compression / PROVED
conditional escape-killed-versus-actual-survivor dichotomy / GLOBAL M31
ACTIVATION AND ADD-BACK OPEN / LEDGER MOVEMENT ZERO.**

This packet is stacked on PR #1003 at
`f8d29402790331aeca5697ab6da9716406d38043`.  It attacks the largest open
gate in that packet: whether an above-budget exact-support family must
activate one of the 137 factorized Pluecker cells.  The answer is split.

* Every forbidden-size exact list has a same-weight packet of at least 36
  supports, with a large exact locator-kernel lower bound.
* Cardinality, boundary weight, pairwise MDS packing, the exact `K+2`
  shadow, and every independently completed coordinate-shortened local line
  still do **not** force a factorized parity four-face.  An exact Sidon
  countermodel proves this sharply.
* Conditional on a selected rank-drop face, its Pluecker data define a
  separable rational map having three almost-complete fibres in the actual
  Chebyshev evaluation domain.
* The one-point escapes of that face have an exact algebraic dichotomy.  A
  listed pair of low-degree Pluecker quotients vanishes at a locator root and
  kills the face, or all escapes are simultaneously realizable by an actual
  syndrome hyperplane.  In particular, every `tau=0` rank-drop face is
  escape-compatible.

These are closure-oriented reductions and route cuts.  They do not select a
factorized face from the 36-support packet, count all exact supports in a
hyperplane, or supply a disjoint global add-back.  All completion atoms
therefore remain null.

## 1. Exact deployed object

Throughout,

```text
p       = 2^31-1          = 2,147,483,647,
n       = 2^21            = 2,097,152,
K       = 2^20            = 1,048,576,
a       = 1,116,023,
sigma   = a-K             = 67,447,
R       = n-a             = 981,129,
B*      = floor(p^4/2^100)= 16,777,215,
L       = B*+1            = 16,777,216.
```

Let `D` be the `n`-point M31 Chebyshev evaluation set, let
`C=RS_Fp(D,K)`, and put `V=C^perp`.  For an error support `E subset D`,

```text
W_E={v in V : supp(v) subset D\E}.
```

For a nonzero syndrome hyperplane `H`, the exact-support indicator is

```text
z_H(E)=1  iff
W_E subset H
and W_(E\{x}) not subset H for every x in E.              (1.1)
```

The direct closure target remains

```text
max_H sum_(E subset D, |E|<=R) z_H(E) <= B*.              (1.2)
```

No statement below replaces the whole-ball objective (1.2) by a boundary
shell or by a pseudo-family.

## 2. A uniform same-weight packet from every forbidden list

Two distinct exact errors for the same received word differ by a nonzero
codeword.  Their support union therefore has size at least the MDS distance

```text
n-K+1=K+1=1,048,577.                                      (2.1)
```

Consequently each weight `1<=j<=K/2=524,288` contains at most one exact
error.  Weight zero is absent for a nonzero syndrome.  A family of size at
least `L` therefore leaves at least

```text
L-524,288=16,252,928                                      (2.2)
```

supports in the `R-K/2=456,841` layers
`j=524,289,...,R`.  Pigeonholing gives one weight with at least

```text
ceil(16,252,928/456,841)=36                               (2.3)
```

exact supports.  This selection changes no support, so it retains every
containment and every one-point escape in (1.1).

For `m` distinct supports of that common weight, the equal-degree locator
map at `D_j=K-j` has `mD_j` columns and a `K`-dimensional target.  Because
all selected flats lie in the same nonzero hyperplane, its image has rank at
most `K-1`.  Hence

```text
dim ker Theta_(E_1,...,E_m) >= m(K-j)-(K-1).              (2.4)
```

For any 16 selected supports this is

```text
30,577+16(R-j),                                           (2.5)
```

and for all 36 it is

```text
1,379,517+36(R-j).                                       (2.6)
```

This is a genuine whole-ball-to-equal-weight rank theorem.  It does not
produce even one parity four-face or the six equal Venn cells used by PR
#1003.

## 3. A sharp Sidon wall against support-only face selection

This use of “Sidon” is unrelated to the C9 `N=20` quantitative primitive-leaf
counterexample in `experimental/notes/audits/sidon_direct_payment.md`.  Here
the Sidon object is a forbidden-size subset of a 48-dimensional binary
support code, used only to remove distinct zero-XOR parity quartets.

The factorized face in PR #1003 is an even-parity quartet: the XOR of its
four binary incidence vectors is zero.  The linear binary pseudo-family in
PR #1001 contains many such quartets, so it did not test whether the already
frozen support/local-line invariants force one.  The following exact
replacement does.

Start with the binary simplex code

```text
[2^12-1,12,2^11]_2=[4095,12,2048]_2.
```

Repeat every coordinate 33 times and take four direct-sum copies.  Padding
with zero coordinates gives

```text
[4*33*4095+440589,48,33*2048]_2
   =[981129,48,67584]_2.                                  (3.1)
```

Identify its message space with
`F_(2^24) x F_(2^24)` and retain only

```text
S={(x,x^3):x in F_(2^24)}.                                (3.2)
```

This set is Sidon in the additive group.  Indeed, suppose two unordered
pairs of distinct field elements obey

```text
x+y=u+v=s,
x^3+y^3=u^3+v^3.                                         (3.3)
```

Because the two entries within either pair are distinct, `s!=0`.  In
characteristic two,

```text
x^3+y^3=s^3+xy*s,
```

so (3.3) gives `xy=uv`.  The two pairs are the roots of the same monic
quadratic and hence coincide.  Thus (3.2) has exactly `2^24=L` points and no
four distinct points summing to zero.

Embed the `R` binary coordinates into `R` disjoint pairs among the `n`
evaluation positions.  A codeword chooses one point from every pair; call
the resulting error transversal `E_x` and its agreement complement `S_x`.
There are

```text
n-2R=134,894                                               (3.4)
```

unused evaluation points.  For distinct labels,

```text
|S_x|=a,
|S_x intersect S_y|=a-d(x,y)
                   <=a-67,584=K-137<K.                   (3.5)
```

Hence the exact `K+2` shadow argument and all independently completed
coordinate-shortened `K+2` local-line laws of PR #1001 replay verbatim: they
use only the number and common size of the agreement blocks and the strict
intersection bound in (3.5).  In particular their first two selected-shell
totals remain

```text
N_(K+1)=L binom(a,K+1),
N_(K+2)=binom(n,K+2)
        +L[p binom(a,K+2)-(K-1)binom(a,K+1)].             (3.6)
```

On the other hand, an even-parity quartet of transversals would give four
distinct message labels with XOR zero, contradicting the Sidon property.
Thus this forbidden-size model has no factorized parity four-face.

The construction in this section is **not** one common syndrome hyperplane
and does not claim to be an exact received-word list.  It proves the sharp
route cut:

```text
cardinality + boundary weight + pairwise MDS packing
+ exact K+2 shadow + independently completed local lines
do not imply a factorized parity four-face.                (3.7)
```

Any valid activation theorem must use a genuinely joint invariant, such as
common-hyperplane containment together with the one-point escape quotients.

## 4. The conditional 137-cell Pluecker data

Now condition on one selected boundary factorized face.  Let the six monic,
pairwise-coprime split locators

```text
A0,A1,B0,B1,C0,C1
```

have common degree

```text
r=33*1024=33,792,
```

and define

```text
P00=A0 B0 C0,   P10=A1 B0 C1,
P01=A0 B1 C1,   P11=A1 B1 C0.                            (4.1)
```

PR #1003 proves that every rank drop of `Theta_sigma` has a unique

```text
0<=tau<=136,
mu1+mu2=r+tau,
mu3=2r-tau,
h=dim coker Theta_sigma=137-tau.                          (4.2)
```

Choose the two low syzygy rows `S,T`.  Their six Pluecker minors factor as

```text
Delta13=A0 qA0,   Delta02=A1 qA1,
Delta23=B0 qB0,   Delta01=B1 qB1,
Delta12=C0 qC0,   Delta03=C1 qC1,                        (4.3)
```

where all six `q` are nonzero, primitive as a family, and have degree at
most `tau`.  The quadratic Pluecker identity is

```text
B0 B1 qB0 qB1-A0 A1 qA0 qA1+C0 C1 qC0 qC1=0.            (4.4)
```

## 5. A uniform almost-complete three-fibre map

Put

```text
MA=A0 A1 qA0 qA1,
MB=B0 B1 qB0 qB1,
MC=C0 C1 qC0 qC1.                                        (5.1)
```

Equation (4.4) says `MA=MB+MC`.  Let

```text
g=gcd(MA,MC),
NA=MA/g, NB=MB/g, NC=MC/g,
lambda=NA/NC.                                            (5.2)
```

The three reduced polynomials are pairwise coprime: any further common
factor of two would, using `NA=NB+NC`, be a further common factor of all
three, contradicting the definition of `g`.  The rational map
`lambda:P^1->P^1` is nonconstant: otherwise two nonzero pairwise-coprime
members of (5.2) would be constants, contradicting their surviving locator
roots below.

Only roots of `qC0 qC1`, of total degree at most `2tau`, can cancel roots of
`A0 A1` from the zero fibre.  The same argument, cyclically, applies to the
other two locator pairs.  Therefore each of the fibres over
`0,1,infinity` contains at least

```text
2r-2tau                                                    (5.3)
```

distinct points of the actual evaluation domain `D`.  After additionally
discarding locator roots at which the fibre's own two `q` factors vanish,
each fibre still has at least

```text
2r-4tau                                                    (5.4)
```

simple `D`-points.  The degree `d=deg(lambda)` satisfies

```text
2r-2tau <= d <= 2r+2tau.                                  (5.5)
```

The lower bound follows from (5.3); the upper bound follows directly from
(5.1)--(5.2).  Across all three fibres, at most `6tau` of the six locator
sets can disappear by cancellation.

At the worst deployed cell `tau=136`, these uniform bounds are

```text
67,312 <= d <= 67,856,
at least 67,312 distinct D-points in each special fibre,
at least 67,040 simple D-points in each special fibre,
at most 816 of the 202,752 locator roots cancelled.        (5.6)
```

Since `d<p`, the nonconstant map is separable.  Thus every one of the 137
rank-drop cells produces an almost-complete three-fibre rational map on the
literal M31 Chebyshev domain.  This is not yet an invariant power/Chebyshev
quotient: no theorem here says that `lambda` factors through a declared
fold, preserves received values, or pays a global list owner.

## 6. Exact one-point escape classes

Let `E_core` be the common error core of the four supports and write

```text
e=3r=101,376,
c=|E_core|=R-e=879,753,
W_core=W_(E_core),
I=sum_(i in {00,10,01,11}) W_(E_i),
Q=W_core/I.                                               (6.1)
```

After removing the common locator and harmless nonzero GRS multiplier, the
quotient `Q` is the cokernel of `Theta_sigma`, so `dim Q=h=137-tau`.

For a variable point `alpha` in `E_i\E_core`, equivalently a root of
`P_i`, the one-point extension

```text
W_(E_i\{alpha})/W_(E_i)
```

is represented in `Q` by

```text
P_i/(X-alpha).                                            (6.2)
```

The class (6.2) vanishes if and only if

```text
e_i belongs to rowspan{S(alpha),T(alpha)}.                (6.3)
```

For the forward implication, a representation of (6.2) through
`Theta_sigma`, multiplied by `X-alpha`, gives a syzygy of degree at most
`sigma` whose value at `alpha` is `-e_i`.  Every such syzygy is generated by
the two low rows: the third Forney index is `mu3>sigma`, and the
predictable-degree property forbids cancellation of a nonzero third-row
coefficient below that degree.  Conversely, a
constant combination of `S,T` taking the value `e_i` has degree
`<=mu2<sigma`; subtracting `e_i` and dividing every coordinate by
`X-alpha` gives a representation of (6.2), up to an irrelevant sign.

At every locator root the evaluated two-row frame has rank two.  This uses
the **unimodularity of the actual Forney frame**, not merely primitivity of
the six quotient polynomials.  Since the primitive row `(P_i)` has a
Bezout section, its syzygy module splits off from `F_p[X]^4`.  The rows
`S,T` are part of a basis of that free summand, so their span is itself a
rank-two direct summand.  Equivalently, the six `2 x 2` minors of `(S;T)`
generate the unit ideal and cannot vanish simultaneously at any `alpha`.
Hence (6.3) is equivalent to vanishing of the three complementary Pluecker
minors.

This distinction is load-bearing.  The condition
`gcd(qA0,qA1,qB0,qB1,qC0,qC1)=1` by itself does not imply pointwise rank two;
a quotient-only search must retain the unimodular-frame saturation gate.

Substituting (4.3) gives exactly the following twelve collision tests:

| support | locator point | the two additional quotients that must vanish |
|---|---|---|
| `00` | `A0` | `qB0,qC0` |
| `00` | `B0` | `qA0,qC0` |
| `00` | `C0` | `qA0,qB0` |
| `10` | `A1` | `qB0,qC1` |
| `10` | `B0` | `qA1,qC1` |
| `10` | `C1` | `qA1,qB0` |
| `01` | `A0` | `qB1,qC1` |
| `01` | `B1` | `qA0,qC1` |
| `01` | `C1` | `qA0,qB1` |
| `11` | `A1` | `qB1,qC0` |
| `11` | `B1` | `qA1,qC0` |
| `11` | `C0` | `qA1,qB1` |

For example, the first row means

```text
alpha in Z(A0) intersect Z(qB0) intersect Z(qC0).         (6.4)
```

Each support has at most `3tau` such forced incidences.  In the `tau=0`
cell every `q` is a nonzero constant, so all twelve collision sets are
empty.

## 7. Escape-killed or an actual common center

If one collision in the table occurs, its escape generator already lies in
`I`.  Every hyperplane containing all four `W_(E_i)` therefore also contains
that one-point extension, contrary to (1.1).  The face has terminal

```text
ESCAPE_KILLED.                                             (7.1)
```

Suppose instead that all twelve collision sets are empty.  Every variable
escape line then lies outside `I`.  A point removed from the common core has
an extension generator outside `W_core` (evaluate the cancelled locator at
that core point), and hence outside `I` automatically.  Thus every one of
the at most

```text
4R=3,924,516                                               (7.2)
```

escape lines is nonzero in `V/I`.

The annihilator has exact dimension

```text
dim Ann(I)=c+h=879,890-tau.                               (7.3)
```

Indeed `dim V=K`, the MDS shortening formula gives
`dim W_core=K-c`, and `dim(W_core/I)=h`; hence
`dim I=K-c-h` and (7.3) follows.

For each escape line, the functionals in `Ann(I)` that also vanish on that
line form one proper hyperplane.  The union bound leaves at least

```text
p^(c+h-1)(p-4R)                                           (7.4)
```

functionals avoiding all escape hyperplanes.  This is positive because

```text
p-4R=2,143,559,131.                                      (7.5)
```

The syndrome-to-functional map is surjective, so any surviving functional
gives an actual received-word center for which all four supports are exact.
The other terminal is therefore

```text
ACTUAL_HYPERPLANE_SURVIVOR.                               (7.6)
```

Duplicate escape hyperplanes only strengthen the union bound.  There is no
unspoken compatibility assumption in (7.4).

Combining (7.1) and (7.6), every conditionally selected rank-drop cell has
an exact terminal.  This does **not** bound the size of the full list: four
actual survivors are far below `L`, and no theorem selects a collision-bearing
face from an above-budget family.

## 8. Literal-Chebyshev, exact-source toy falsifier

Domain compatibility and exact one-point escape together do not eliminate
the low-rank branch.  Over `F_31`, let

```text
D=Z(T_8), C=RS_F31(D,4).
```

The standard degree-eight Chebyshev polynomial has roots

```text
2,5,10,11,20,21,26,29.
```

Exhausting all `8P6=20,160` ordered, pairwise-distinct singleton factor
sextuples gives

```text
rank Theta_1 = 4: 19,440,
rank Theta_1 = 3:    720.                                (8.1)
```

For every one of the 720 rank-three sextuples, the unique projective
left-kernel functional is nonzero on all twelve one-point escape directions
`P_i/(X-alpha)`.  Dividing by the 24 vertex relabellings leaves 30 unordered
source-valid faces.  Exhausting the exact six-element `PGL_2` stabilizer of
`D` finds no nonidentity stabilizer of any of the 30 support faces (and hence
none of a face together with its syndrome).  Every support has
odd size three, so none is a union of fibres for a nontrivial dyadic fold of
the eight-point domain.  All 30 are therefore primitive under these toy
owners.

One explicit sextuple is

```text
(a0,a1,b0,b1,c0,c1)=(2,5,10,20,11,29),
(qA0,qA1,qB0,qB1,qC0,qC1)=(4,25,13,23,19,14).            (8.2)
```

In the displayed root order, an actual center and four degree-less-than-four
explanations are

```text
y=(28,0,21,25,0,0,0,0),
c00=0,
c10=30+23X+11X^2+4X^3,
c01=12+26X+2X^2+25X^3,
c11=29+17X+4X^2+13X^3.                                   (8.3)
```

Their exact error supports are the four parity supports.  An exhaustive
scan of all `31^4` codewords shows that the complete radius-three list around
this center has size five: the sole additional support is `{5,21,26}`, with
explanation

```text
22+27X+29X^2+26X^3.                                      (8.4)
```

There are no exact supports of weights zero, one, or two.

These are exact toy-scale controls, not sampled evidence.  They prove no
deployed M31 survivor, but they refute every field-uniform lemma asserting
that Chebyshev membership, exact source validity, escape, and the declared
symmetry/quotient owners jointly eliminate all low-`tau` cells.  A deployed
argument must use the large-`r` geometry, a genuinely global source
invariant, or a disjoint add-back.

## 9. What the maximal attack resolved and what remains

The packet proves three sharp facts about the global activation problem.

1. Every forbidden list yields a large, exact, same-weight rank packet.
2. All currently frozen support-only and independently completed local-line
   invariants permit a Sidon extremizer with no parity face.
3. Once a rank-drop parity face is selected, its remaining structure is no
   longer vague: it is simultaneously an almost-complete three-fibre map and
   one of two exact escape terminals.  Generic escape does not pay the
   `tau=0` cell; it realizes it.

The missing theorem is consequently an escape-aware common-hyperplane
activation theorem on the actual same-weight packet.  It must prove one of

```text
EXACT_WHOLE_BALL_BOUND_LE_BUDGET,
SOURCE_VALID_COLLISION_BEARING_FACE,
GLOBALLY_DISJOINT_PAID_OWNER,
EXPLICIT_PRIMITIVE_GENERAL_RANK_SOURCE.                   (9.1)
```

It cannot be obtained from cardinality, distance, scalar shells, or local
line completion alone.  Enumerating the 137 cells without first proving
activation would classify a conditional object and would not close (1.2).

The almost-complete three-fibre statement is a precise second possible
attack: prove that no primitive reduced map (5.2) with the stated literal
Chebyshev fibres exists, or classify every such map into a declared uniform
quotient owner while preserving all received data.  A mere support
automorphism is insufficient.

## 10. Ledger impact, nonclaims, and replay

```text
prime-field M31 list row closed:    false
quartic-field M31 list row closed:  false
U_paid:                             null
U_Q:                                null
U_list-int:                         null
U_new:                              null
ledger movement:                    0
prize claim:                        false
```

No asymptotic parameter, layer-cake sum, moment estimate, Markov inequality,
or Chebyshev concentration bound occurs here.  All deployed arithmetic is
exact.  The `GF(2^6)` and `GF(31)` enumerations are toy-scale
falsifiers or replays only; the Sidon proof, three-fibre bounds, and escape
dichotomy are symbolic finite-field arguments.

Replay from the repository root:

```text
python3 experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --check
python3 -O experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --check
python3 experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.py --tamper-selftest
sage experimental/scripts/verify_m31_sidon_three_fibre_escape_compiler.sage
```

The manifest hash-binds this note, both verifiers, the certificate README,
and the inherited PR #1001/#1003 sources.  Every closing field is fail-closed.
