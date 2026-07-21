# M31 literal packet activation route cut and the forced rank-36 Forney frame

## Status

**PROVED literal same-weight actual-hyperplane packets of sizes 230 and 36
with no parity quartet / PROVED uniform rank-36 low-Forney-frame theorem for
every forbidden list / ARBITRARY-PACKET PARITY ACTIVATION REFUTED / GLOBAL
M31 LIST ROW OPEN / LEDGER MOVEMENT ZERO.**

This packet is stacked on PR #1004 at
`aab74d5f882412cba3f37346b40c394086da1068`.  It closes the precise
activation question left there: can one discard the rest of an exact list,
retain an arbitrary bounded same-weight packet in its literal syndrome
hyperplane, and force one of PR #1004's factorized parity four-faces?  No.

The negative statement is literal rather than a pseudo-family obstruction.
The inherited identity-prefix theorem gives an actual M31 received word with
at least `1,993,678` exact boundary supports.  A sharp elementary greedy
extraction retains 230 of them with no four distinct incidence vectors of
zero XOR.  An independent Chebyshev-fibre construction gives a completely
explicit 36-label packet inside another actual syndrome hyperplane and
replays every one-point escape.

There is nevertheless a strong positive replacement.  Every forbidden list
still gives a 36-support equal-weight packet whose primitive locator row has
at least 21 minimal syzygies below the shifted-locator cutoff.  Its two
smallest rows have combined degree at most `53,745`, strictly below the
cutoff `67,447`.  Thus the correct forced local object is a growing-rank
Grassmann/Pluecker frame, not a four-face.

Nothing here bounds the full list in either constructed hyperplane, charges a
whole forbidden layer, or supplies the global add-back.  No completion atom
moves.

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

Let `D=Z_Fp(T_n)` be the standard-position M31 Chebyshev domain, let
`C=RS_Fp(D,K)`, and put `V=C^perp`.  For an error support `E subset D`, set

```text
W_E={v in V:supp(v) subset D\E}.
```

For a nonzero syndrome hyperplane `H`, the exact-support condition is

```text
W_E subset H,
W_(E\{x}) not subset H for every x in E.                 (1.1)
```

The whole-ball target remains

```text
max_H sum_(E subset D, |E|<=R) 1[(1.1)] <= B*.           (1.2)
```

Integrated scalar descent identifies this prime-field target with the
deployed quartic-field predicate.  The present packet does not prove (1.2).

## 2. An actual 1,993,678-support boundary source

The identity-prefix lemma in `tex/cs25_cap_v13_2.tex` applies to every
`D subset F_p`.  Send each `a`-subset `M subset D` to the first `sigma`
coefficients of its monic locator

```text
Lambda_M(X)=product_(alpha in M)(X-alpha).
```

One prefix fibre has size at least

```text
ceil(binomial(n,a)/p^sigma)=1,993,678.                   (2.1)
```

For its common prefix `z`, the inherited construction gives a received word
`U_z` and, for every `M` in the fibre, a polynomial `c_M` of degree `<K`
such that

```text
U_z-c_M=Lambda_M on D.                                  (2.2)
```

Equation (2.2) is stronger than agreement on at least `a` positions:
`Lambda_M` has exactly the roots `M` inside `D`.  Hence the exact error
support is

```text
E_M=D\M,             |E_M|=R.                           (2.3)
```

The locators, codewords, and supports are pairwise distinct.  Because the
list has more than one member, `U_z` has nonzero syndrome.  Its kernel is
therefore one literal projective syndrome hyperplane, so its complete set of
dual projective points satisfies every global projective-line equation of
the integrated lift theorem.

This is a theorem-level actual center at the adjacent safe agreement.  The
*certified lower subfamily* `1,993,678` is below `B*`; no upper bound on the
full list around `U_z` is proved here.  Its budget status is therefore
`UNKNOWN`, and this packet does not claim a counterexample to the M31 bound.

## 3. A 230-support parity-free subpacket

We use the following elementary extraction lemma.

**Binary Sidon extraction.**  Let `A` be a set of distinct vectors over
`F_2`.  If

```text
|A| > (q-1)+binomial(q-1,3),                             (3.1)
```

then `A` has a `q`-element subset in which all unordered pair sums are
distinct.

Indeed, suppose `r` vectors have been chosen.  A new vector is forbidden if
it is already chosen or equals the XOR of three distinct chosen vectors.
There are at most

```text
r+binomial(r,3)
```

such values.  Any other choice creates no collision between a new pair sum
and an old pair sum.  Induction proves the lemma.

At the M31 value from (2.1),

```text
229+binomial(229,3)=1,975,583 < 1,993,678.               (3.2)
```

Thus the actual boundary family contains 230 supports whose 26,335
unordered pair XORs are distinct.  Equivalently, no four distinct selected
support incidence vectors have XOR zero.  Complementing all four incidence
vectors changes no fourfold XOR, so the conclusion is identical for the
agreement supports and the error supports.

PR #1004's factorized face is an even-parity quartet.  It is therefore absent
from this 230-support packet.  Nevertheless the packet consists of exact
same-weight supports in one actual M31 syndrome hyperplane and automatically
inherits every global projective-line closure law and every literal locator
identity.

The same greedy estimate does not certify 231:

```text
230+binomial(230,3)=2,001,690 > 1,993,678.               (3.3)
```

This sharpens the route cut.  Any proof that first replaces its source list
by an arbitrary packet of at most 230 supports and then forgets the ambient
list mass cannot force a parity four-face, even if it retains the fact that
the packet is literal and lies in a globally line-closed hyperplane.  A valid
activation theorem may still select a *special* packet using the entire
forbidden family; (3.2) does not address such a mass-sensitive selection.

## 4. An independent explicit 36-support Chebyshev control

There is also a closed-form deployed construction, independent of the
prefix pigeonhole.  Put

```text
s=2^17=131,072,       Y=T_s(X).
```

The identity `T_n=T_16 o T_s` partitions `D` into 16 complete `s`-point
fibres.  Use 12 fibres as variable labels and reserve the other four.  Set

```text
e=4s=524,288,
c=R-e=456,841.
```

Choose a common `c`-point error core `C_0` in the four reserve fibres.  This
is possible because `4s=524,288>c`.  For a four-subset `S` of the 12 variable
labels define

```text
E_S=C_0 union union_(lambda in S) Y^(-1)(lambda).         (4.1)
```

Then `|E_S|=c+4s=R`.  The certificate pins 36 four-subsets for which all 630
pair XORs are distinct.  Any two distinct members use at least five variable
fibres in their union, so

```text
|E_S union E_T| >= c+5s=1,112,201 > K+1.                (4.2)
```

Let `L_0` be the common-core locator and, up to harmless nonzero scalars,
write the variable locator as

```text
P_S=q_S(Y),          q_S(Y)=product_(lambda in S)(Y-lambda).
```

Every shortened space in (4.1) is contained in

```text
I=L_0 * sum_(k=0)^4 Y^k F_p[X]_<sigma.                  (4.3)
```

Because `sigma<s`, the five bands in (4.3) are independent and have total
dimension `5sigma=337,235<K`.

Here (4.3) is literal under the standard weighted-dual identification

```text
F_p[X]_<K  -> V,       R |-> (u_x R(x))_(x in D).
```

It gives

```text
W_(C_0)=L_0 F_p[X]_<K-c,
K-c=4s+sigma=591,735.                                  (4.4)
```

Division by `L_0` therefore identifies `W_(C_0)` with
`F_p[X]_<K-c`.  Evaluation on the `c<K` core points has kernel
`W_(C_0)` and is onto by interpolation, so it also identifies

```text
V/W_(C_0) ~= F_p^(C_0).                                 (4.5)
```

The one-point escapes can be separated simultaneously.  Regard `F_p[X]` as
the free `F_p[Y]`-module with basis `1,X,...,X^(s-1)`, after normalizing `Y`
to be monic.  After the division in (4.4), let `psi` extract the coefficient of
`Y^3 X^(s-1)`.  It kills every `q_S(Y)A(X)` with `deg A<sigma`.  If
`alpha` is a variable point in the fibre labelled `lambda in S`, then

```text
q_S(Y)/(X-alpha)
 =q_(S\{lambda})(Y) * (Y-lambda)/(X-alpha),              (4.6)
```

and `psi` of (4.6) is the nonzero leading coefficient of the normalized
`Y`.  Thus every variable escape avoids `I`.

To extend `psi` from `W_(C_0)` to all of `V`, use the `c` quotient
coordinates in (4.5).  At a fixed `x in C_0`, the escape
from `E_S` has nonzero `x`-coordinate

```text
L_0'(x) q_S(Y(x)) !=0,                                  (4.7)
```

because core and variable fibres are disjoint.  Each of the 36 supports
forbids only one value of that extension coordinate.  Since `36<p`, choose
every coordinate outside its forbidden set.  The resulting functional on
`V` vanishes on every `W_(E_S)` and is nonzero on every one-point escape.
Surjectivity of the syndrome map gives one actual M31 received word realizing
all 36 exact supports.

The construction could use all `binomial(12,4)=495` supports because
`495<p`; the pinned Sidon 36-subpacket is used only to remove every parity
quartet.  Again, the complete 495-support family may contain special faces.
The theorem is a route cut against arbitrary-packet activation, not against
mass-sensitive selection.

## 5. What every forbidden list really forces

Now start from a hypothetical exact list of size at least `L=B*+1`.  PR
#1004 proves that it contains `M>=36` exact error supports of one weight

```text
K/2 < j <= R.                                            (5.1)
```

Select any 36 and let

```text
C_0=intersection_i E_i,       c=|C_0|,
S_i=D\E_i,                    m=n-j,
U=union_i S_i=D\C_0,
e=|U|-m=j-c,
D_0=m-K=K-j.                                             (5.2)
```

Inside `U`, the complement locator of `S_i` is the reduced error locator
of `E_i\C_0`; call it `P_i`.  The row `(P_1,...,P_36)` is primitive and all
entries have degree `e`.  Let

```text
mu_1 <= ... <= mu_35
```

be its Forney indices.  The general shortened-dual/Forney theorem already
proved in `experimental/notes/l2/rank16_left_kernel_forney_route_cut.md`
gives

```text
sum_(i=1)^35 mu_i=e.                                     (5.3)
```

The common received-word syndrome is nonzero on the reduced shortened dual
quotient.  Equivalently, the truncated locator map at degree bound `D_0` is
not surjective.  Its predictable-degree formula therefore forces

```text
mu_35 >= D_0+1.                                          (5.4)
```

Combining (5.2)--(5.4),

```text
sum_(i=1)^34 mu_i
 <= e-D_0-1
  = 2j-K-c-1
 <= 2R-K-1
  = 913,681.                                             (5.5)
```

Several uniform conclusions follow immediately.  Since the first 34
indices are ordered,

```text
mu_1 <= floor(913,681/34)=26,872,                        (5.6)

mu_1+mu_2 <= floor(2*913,681/34)
            =floor(913,681/17)
            =53,745.                                    (5.7)
```

Meanwhile

```text
D_0=K-j >= K-R=67,447,                                  (5.8)
```

so (5.7) is strictly below the shifted-locator cutoff.  Also at most

```text
floor(913,681/67,447)=13
```

of the first 34 indices can be at least `D_0`.  Together with the exceptional
largest index, at least

```text
35-(13+1)=21                                             (5.9)
```

minimal syzygy rows have degree `<D_0`.

In particular, the two smallest rows form an independent `2 x 36` polynomial
frame.  Every `2 x 2` Pluecker minor has degree at most `53,745<D_0`, and at
least one minor is nonzero.  A row supported on only two columns is
impossible: it would give a relation between two reduced locators below
`D_0`, contradicting the pairwise MDS separation.  Thus every forbidden
list activates a nontrivial bounded-degree general-rank source.

For an actual layer multiplicity `M_j>=36`, the same proof retains the mass
and improves (5.7) to

```text
mu_1+mu_2
 <= floor(2(2j-K-c-1)/(M_j-2)).                         (5.10)
```

Equation (5.10), rather than the constant 36 extraction, is the
multiplicity-sensitive local input a closure proof should preserve.

## 6. Exact route cut and next proof object

The packet proves the following dichotomy of proof strategies.

```text
arbitrary bounded packet + literal hyperplane + all line closure
  DOES NOT force a factorized parity face inside the retained packet;

forbidden whole list
  DOES force a low-degree growing-rank Forney/Pluecker frame.
```

The maximal remaining attack is therefore a mass-preserving first-match
compiler.  It must retain every layer multiplicity `M_j`, mark the common
core, and route the full shifted-Popov frame to exactly one of:

1. a common-GCD, quotient, or fixed-dimensional owner with a disjoint
   support charge;
2. a primitive growing-dimensional frame with an exact root/incidence bound
   that fits `B*`; or
3. an explicit unpaid route cut.

The complete-quadrilateral six-section consequence of PR #1004 remains a
useful conditional terminal after a special four-face is selected.  Generic
Riemann--Hurwitz, Mason, Belyi, and Ritt arguments do not perform that source
selection and do not replace (5.10).

## 7. Exact nonclaims

- The constructed centers are not claimed to have full list size `>B*`.
- A forbidden family is not claimed to contain the particular 230- or
  36-support packet constructed here.
- The full 1,993,678- or 495-support family is not claimed parity-free.
- Global projective-line closure is not claimed to determine a bounded
  packet; the actual centers merely satisfy it automatically.
- The 21 low syzygies are not classified, paid, or proved sparse.
- No common-core division is counted without a marked-core add-back.
- No `U_Q`, `U_A`, interior, boundary, or whole-ball atom is banked.
- No prime-field or quartic-field M31 list theorem, MCA theorem, official
  radius, or prize solution is claimed.
- No stable-paper TeX is changed.

## 8. Replay

```bash
python3 experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --check
python3 -O experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --check
python3 experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.py --tamper-selftest
HOME=/tmp/rs-mca-sage-home /usr/local/bin/sage experimental/scripts/verify_m31_actual_hyperplane_packet_activation_route_cut.sage
git diff --check
```

The Python certificate checks every deployed integer, the exact prefix
average, the greedy thresholds, the explicit Sidon packet, the fibre/module
degree bands, and all Forney bounds.  The Sage replay independently verifies
the field-native `T_16` split, quotient-polynomial rank, deployed integers,
and a faithful literal small Chebyshev hyperplane model.  Neither verifier
promotes its toy control to the deployed proof.
