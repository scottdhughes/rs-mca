# M1 rank-nine t=2 source-compatible cyclic control v1

- **Status:** PROVED exact toy source-compatibility controls / PROVED exact
  two-slope deep exits and complete-selector post-deep low-carrier exits /
  deployed row OPEN / no ledger movement.
- **Scope:** two cyclic extension-field rows testing the three-coordinate
  source compatibility absent from the earlier \(t=1\) control.
- **Predecessors:**
  `m1_kb_branch3_rank9_cyclic_rich_pencil_control_v1.md`,
  `m1_kb_branch3_rank9_rich_pencil_atlas_v1.md`,
  `m1_kb_branch3_deep_ccl_tdd_v1.md`,
  `m1_kb_branch3_low_excess_carrier_cut_v1.md`, and
  `m1_kb_branch3_5_mask_contract_v1.md`.
- **Companion checks:**
  `verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.sage` and
  `verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py`.

The earlier cyclic control showed that a hostile 21-slope rich pencil and
eight transverse directions can occur inside a selected affine-rank-nine
family, while a different complete selector routes the residual received
pair to the already-proved low-excess carrier owner.  That row had
\(t=A-k=1\) and a two-coordinate source.

This packet raises the source codimension by one.  It constructs exact
\(t=2\), three-coordinate source lines and proves the missing compatibility
equation.  The smallest row is

\[
 (n,k,R,j,A,t)=(35,13,22,20,15,2).
\]

It has an exact 21-plus-8 rank-nine family and an exhaustive 839-slope
**post-deep nonzero-locator** frontier.  Two additional zero-polynomial
slopes have actual error weight two and enter the extended deep owner.  Thus
the full support-wise noncontained finite frontier has all \(841\) slopes.
All post-deep locator errors avoid the three source coordinates, so every
selector in that ansatz has carrier excess at most ten.  The complete
post-deep lexicographic selector has excess seven.

The smallest row in the same ansatz that can even display carrier excess
eleven is

\[
 (n,k,R,j,A,t)=(36,14,22,20,16,2).
\]

It has a selected rank-nine family of excess eleven.  That selected family is
again incomplete: a fixed-root exhaustive inventory covers all 287 post-deep
nonzero-locator slopes and supplies a complete selector of excess five.  Its
two additional zero-polynomial slopes enter the same deep owner, giving all
\(289\) finite slopes.  Thus both toy received pairs split exactly into two
deep slopes and a post-deep part paid at or before low carrier.  Neither is a
deployed rank-nine residual.

## 1. Three-coordinate source normal form

Let \(D=\langle\omega\rangle\subset F^\times\) be a cyclic domain.  Write

\[
 a=D_0,\qquad b=D_1,\qquad c=D_2,
 \qquad \Sigma=\{a,b,c\},
\]

and let \(B=D\setminus\Sigma\), identified with exponent indices
\(3,\ldots,n-1\).  Fix a root core \(C\subset B\) of size \(k-2\), and put

\[
 G(X)=\prod_{i\in C}(X-D_i),\qquad
 Q_0=G/G(a),\qquad Q_1=Q_0(X-a).
\tag{1.1}
\]

For \(x\in B\setminus C\), define

\[
 q_x(X)
 =\frac{G(X)(X-x)}{G(a)(a-x)}
 =Q_0(X)+\frac1{a-x}Q_1(X).
\tag{1.2}
\]

Thus the one-moving-root locators form an affine polynomial pencil with fixed
GCD \(G\).  Restrict \(Q_0,Q_1\) to \(\Sigma\) and extend by zero on \(B\).
This gives an exact three-coordinate source line.

For the canonical slope coordinate

\[
 \eta=q_x(b),
\]

eliminate \(s=(a-x)^{-1}\) from (1.2).  Since \(Q_1(b)\ne0\), put

\[
 \beta=\frac{Q_1(c)}{Q_1(b)},\qquad
 \alpha=Q_0(c)-\beta Q_0(b).
\tag{1.3}
\]

The received pair is

\[
 \epsilon_0=(1,0,\alpha)\text{ on }(a,b,c),\qquad
 \epsilon_1=(0,1,\beta)\text{ on }(a,b,c),
\tag{1.4}
\]

and zero on \(B\).  Every rich-pencil word satisfies

\[
 q_x(a)=1,\qquad q_x(b)=\eta,\qquad
 q_x(c)=\alpha+\beta\eta.
\tag{1.5}
\]

### Proposition 1.1 -- exact nonzero-witness classification

Let \(A=k+2\), and let \(q\) be a nonzero polynomial of degree at most
\(k-1\).  If \(\operatorname{ev}_D(q)\) agrees with
\(\epsilon_0+\eta\epsilon_1\) at \(A\) points, then it agrees at all three
points of \(\Sigma\), has exactly \(k-1\) roots in \(B\), and has no other
agreement.  Consequently every noncontained witness with nonzero explaining
polynomial is uniquely indexed by a \((k-1)\)-set \(S\subset B\):

\[
 P_S(X)=\prod_{i\in S}(X-D_i),\qquad
 q_S=P_S/P_S(a),
\tag{1.6}
\]

subject to the exact compatibility equation

\[
 \boxed{q_S(c)=\alpha+\beta q_S(b).}
\tag{1.7}
\]

Its slope and actual error are

\[
 \eta_S=q_S(b),\qquad
 e_S=\epsilon_0+\eta_S\epsilon_1-\operatorname{ev}_D(q_S),
\tag{1.8}
\]

and

\[
 Z(e_S)=\Sigma\sqcup S,
 \qquad E_S=\operatorname{supp}(e_S)=B\setminus S,
 \qquad |E_S|=j=20.
\tag{1.9}
\]

**Proof.**  Away from the three source coordinates, agreement means
\(q(x)=0\).  A nonzero polynomial of degree at most \(k-1\) has at most
\(k-1\) such roots.  Since

\[
 A=(k-1)+3,
\]

all three source coordinates and exactly \(k-1\) roots are forced.  The
agreement at \(a\) normalizes \(q=q_S\); the agreements at \(b,c\) are exactly
(1.7).  Because \(a,b,c\notin S\), all three locator values are nonzero, and
there are no further zeros.  The zero polynomial agrees throughout \(B\), but
it is not covered by the nonzero-polynomial root count and must be classified
separately.
\(\square\)

Equation (1.7) is the new \(t=2\) compatibility gate.  A support mask alone
does not certify it.

### Proposition 1.2 -- uniform noncontainment for nonzero locators

Every compatible locator in Proposition 1.1 is support-wise noncontained.
Indeed, on

\[
 T_S=\Sigma\sqcup S,
\tag{1.10}
\]

an explaining polynomial for \(\epsilon_0\) would vanish on the \(k\)
distinct points \(S\sqcup\{b\}\), while having value one at \(a\).  A
polynomial of degree strictly less than \(k\) with those \(k\) roots is zero,
which is impossible at \(a\).  This proof is uniform in \(S\); it applies to
all compatible supports counted by the meet-in-the-middle inventories, not
only to the displayed 29-support subfamilies.  The Sage replay also checks
directly on every displayed support that the restricted RS generator has
rank \(k\) and gains rank on adjoining \(\epsilon_0|_{T_S}\).

### Proposition 1.3 -- the two exact deep exceptions

Put

\[
 \eta_0=0,
 \qquad
 \eta_c=-\alpha/\beta.
\tag{1.11}
\]

At \(\eta_0\), the zero polynomial agrees with \(y_{\eta_0}=\epsilon_0\)
on \(\{b\}\sqcup B\).  Choose the exact-size support

\[
 T_0=\{b\}\sqcup\{D_3,\ldots,D_{A+1}\}.
\tag{1.12}
\]

It has \(A\) points because its \(B\)-part has \(A-1=k+1\) points.  If a
degree-less-than-\(k\) polynomial explained \(\epsilon_1\) on \(T_0\), it
would vanish on those \(k+1\) points of \(B\) but equal one at \(b\), a
contradiction.  Hence this zero-polynomial witness is noncontained.  Its
actual error support is \(\{a,c\}\), and its weight is two.

At \(\eta_c\), the zero polynomial agrees on \(\{c\}\sqcup B\).  On

\[
 T_c=\{c\}\sqcup\{D_3,\ldots,D_{A+1}\},
\tag{1.13}
\]

an \(\epsilon_1\) explainer would again vanish on \(k+1\) points of \(B\)
but have value \(\beta\ne0\) at \(c\).  This witness is noncontained, with
actual support \(\{a,b\}\) and weight two.

These are the exact deep exceptions.  For any other slope, all three sparse
coordinates of \(y_\eta\) are nonzero, so the zero polynomial's agreement
set is exactly \(B\), where both \(\epsilon_0\) and \(\epsilon_1\) vanish;
that witness is contained.  Any nonzero RS codeword has MDS weight at least

\[
 R+1=23.
\]

Since \(\operatorname{wt}(y_\eta)\le3\), every error arising from a nonzero
codeword has weight at least

\[
 (R+1)-3=20>
 r_*:=\left\lfloor\frac R3\right\rfloor=7.
\tag{1.14}
\]

For each special slope, the displayed exact-\(A\) witness support lies inside
the full agreement set \(D\setminus E\).  If both sources were explainable on
that larger set, their restrictions would explain them on the displayed
support, contradicting the restricted-generator test.  Noncontainment
therefore persists upward exactly as required by the extended-deep bridge.
Thus exactly \(\eta_0,\eta_c\) enter the proved owner
`DEEP_MCA_BRANCH2_BRANCH3_WEIGHT_EXTENSION`.  The MITM inventories below
attain every other slope, so the exact finite frontier partitions as

\[
 |F|=2+(|F|-2):
 \quad\text{two deep zero-polynomial slopes plus the post-deep
 nonzero-locator frontier}.
\tag{1.15}
\]

## 2. Exact Hankel and transversality checks

For the cyclic domain, the dual weights are

\[
 \lambda_x=
 \left(\prod_{y\in D\setminus\{x\}}(x-y)\right)^{-1}
 =x/n.
\tag{2.1}
\]

For every declared selected nonzero-locator witness, the companion Sage
replay constructs the full \(R\times n\) weighted RS parity-check matrix, the
actual error, and the \(2\times21\) Hankel matrix

\[
 M_A(\eta)_{r,s}=\operatorname{Syn}(e_\eta)_{r+s},
 \qquad 0\le r<2,\quad0\le s\le20.
\tag{2.2}
\]

Every selected nonzero-locator actual support has size 20, so the proved
factorization gives

\[
 \operatorname{rank}M_A(\eta)=\min(2,20)=2.
\tag{2.3}
\]

The direct replay independently obtains rank two in every case.  If \(H_E\)
is the restriction to a selected nonzero-locator actual support, then both
rows have the exact tuple

\[
 \bigl(\operatorname{rank}H_E,
       \operatorname{rank}[H_E\mid y_0],
       \operatorname{rank}[H_E\mid y_1]\bigr)
 =(20,21,21).
\tag{2.4}
\]

Thus each selected incidence is transverse.  Moreover the two source
syndromes together with their Frobenius conjugates have rank four in both
rows.  These controls are not silently descending to the base field.

For each of the two special zero-polynomial witnesses, the replay separately
checks the exact \(A\)-point support, the full agreement set, actual error
support and weight two, restricted-generator ranks \((k,k+1)\) for the
\(\epsilon_1\) noncontainment test, Hankel rank two, and the deep inequality
\(2\le r_*=7\).  It also checks directly that every nonspecial zero-word
agreement set is \(B\), and that the MDS lower bound for a nonzero-codeword
error is \(20>7\).

## 3. The order-35 control

Use

\[
 F=\mathbb F_{29}[u]/(u^2+24u+2),\qquad |u|=840,
\]

\[
 \omega=u^{24}=26+16u,\qquad |\omega|=35.
\tag{3.1}
\]

The row is

\[
 (n,k,R,j,A,t)=(35,13,22,20,15,2).
\tag{3.2}
\]

Take

\[
 C=(3,4,5,6,7,8,9,10,11,12,13).
\tag{3.3}
\]

The canonical source coefficients are

\[
 \alpha=28+28u,\qquad \beta=2+23u.
\tag{3.4}
\]

The 21 root sets \(C\sqcup\{x\}\), \(x=14,\ldots,34\), form the rich
pencil.  Add these eight source-compatible 12-root sets:

~~~text
(3,4,8,9,11,12,14,16,19,20,28,30)
(7,14,16,19,20,23,24,27,29,30,31,32)
(4,7,9,11,12,15,21,23,29,30,32,33)
(4,6,7,16,19,22,24,28,29,30,31,34)
(4,5,7,11,12,13,17,18,20,28,30,31)
(4,5,7,11,12,22,23,27,28,30,33,34)
(3,7,10,13,18,19,22,24,30,31,33,34)
(4,5,6,7,10,11,17,18,25,26,27,33)
~~~

Exact linear algebra gives

\[
 \text{affine rank}=9,\qquad
 \text{raw rank}=10,\qquad
 \deg\gcd(q_x:x\text{ rich})=11.
\tag{3.5}
\]

The selected 29 slopes are distinct.  The selected carrier is all 32 points
of \(B\), hence its excess is ten.  The rich line itself has

\[
 (J_L,M_L,x_L)=(21,21,1).
\tag{3.6}
\]

This is a local rank-nine control.  It is not a complete selector.

### 3.1 Exhaustive 839-slope post-deep inventory

For \(i\in B\), define

\[
 r_i^{(b)}=\frac{b-D_i}{a-D_i},\qquad
 r_i^{(c)}=\frac{c-D_i}{a-D_i}.
\tag{3.7}
\]

For a 12-set \(S\), equation (1.7) becomes

\[
 \prod_{i\in S}r_i^{(c)}
 =\alpha+\beta\prod_{i\in S}r_i^{(b)}.
\tag{3.8}
\]

The exact verifier splits \(B\) into two 16-point halves.  It enumerates only
\(2^{16}\) product states on each side, grouped by cardinality, and evaluates
the exact affine incidence in bounded chunks.  It does not materialize the

\[
 \binom{32}{12}=225{,}792{,}840
\]

root sets.  The result is

\[
 268{,}998\text{ compatible root sets},
 \qquad839\text{ distinct slopes},
\tag{3.9}
\]

with 259 through 390 witnesses per slope.  The inventory hash is

~~~text
24150857548e5bc9ee199e1d088bdcfb458191579db247a65ed311e5dfbc590e
~~~

Both \(q_S(b)\) and \(q_S(c)\) are nonzero.  Hence the two slopes omitted
from the nonzero-locator inventory are \(0\) and

\[
 -\alpha/\beta=12+15u.
\]

The exact inventory attains every other field element, so 839 is the full
**post-deep nonzero-locator** frontier, not a sample.  Proposition 1.3 supplies
noncontained zero-polynomial witnesses at both omitted slopes; consequently
the full finite frontier has \(839+2=841\) slopes.

The lexicographically first witness at each slope has common root intersection

\[
 \{3,4,5\}.
\]

Its complete post-deep selector carrier therefore has size 29 and excess
seven.  More strongly, without using lexicographic choices, (1.9) gives

\[
 E_S\subseteq B,
 \qquad |B|-R=32-22=10.
\tag{3.10}
\]

Thus **every selector in the post-deep nonzero-locator ansatz** has excess at
most ten.  The exact low-carrier cap at the displayed post-deep lex selector
is

\[
 B_7=
 \left\lfloor
 \frac{\binom{29}{8}}{\binom87}
 \right\rfloor
 =536{,}518>839.
\tag{3.11}
\]

The worst structural excess-ten cap is also finite and larger than the exact
frontier:

\[
 B_{10}=
 \left\lfloor
 \frac{\binom{32}{11}}{\binom{11}{10}}
 \right\rfloor
 =11{,}729{,}498>839.
\tag{3.12}
\]

Therefore the 839 post-deep slopes are routed at or before the existing
low-carrier owner.  Together with the two slopes already removed by the deep
owner, this pays the full 841-slope toy frontier.  The 29-slope rank-nine
family cannot define a later residual.

## 4. The minimal post-deep high-carrier-capable row

Within the post-deep nonzero-locator, three-source, one-moving-root ansatz, a
degree-\((k-1)\) rich locator has a core of size \(k-2\).  The number of
available moving roots is

\[
 |B|-(k-2)=(n-3)-(k-2)=R-1.
\]

Thus a 21-slope rich pencil forces

\[
 R\ge22.
\tag{4.1}
\]

All actual errors lie in \(B\), so the maximum possible carrier excess is

\[
 |B|-R=(n-3)-R=k-3.
\tag{4.2}
\]

To make excess eleven possible one needs \(k\ge14\).  Equalities in
(4.1)--(4.2) give the smallest row

\[
 (n,k,R,j,A,t)=(36,14,22,20,16,2).
\tag{4.3}
\]

Use

\[
 F=\mathbb F_{17}[u]/(u^2+16u+3),\qquad |u|=288,
\]

\[
 \omega=u^8=12+16u,\qquad |\omega|=36,
\tag{4.4}
\]

and core

\[
 C=(3,4,5,6,7,8,9,10,11,12,13,14).
\tag{4.5}
\]

The canonical source coefficients are

\[
 \alpha=13+7u,\qquad \beta=5+14u.
\tag{4.6}
\]

The 21 one-moving-root sets and the following eight 13-root sets give a
source-compatible rank-nine local control:

~~~text
(4,6,7,10,12,13,14,17,18,19,21,22,34)
(6,7,11,13,15,18,21,22,24,26,27,30,34)
(7,8,12,13,15,17,18,19,21,23,30,32,35)
(6,7,8,9,10,13,15,16,18,19,20,22,31)
(3,6,18,21,23,24,25,26,27,30,32,33,35)
(5,8,9,13,19,21,22,24,25,26,29,31,32)
(5,6,10,12,13,18,23,25,26,31,32,33,34)
(3,6,11,15,17,19,20,22,23,29,31,33,35)
~~~

Exact replay gives

\[
 \text{affine/raw rank}=9/10,
 \qquad\deg\gcd=12,
 \qquad N_V=33,
 \qquad\nu=11.
\tag{4.7}
\]

This is the desired local high-carrier geometry.  It is still not a complete
selector.

### 4.1 Exhaustive fixed-root post-deep selector

Require the root \(D_3\) in every locator and choose the remaining 12 roots
from the other 32 nonsource coordinates.  The same two-half exact inventory
represents all

\[
 \binom{32}{12}=225{,}792{,}840
\]

such locators.  It finds

\[
 780{,}907\text{ compatible fixed-root locators},
 \qquad287\text{ slopes},
\tag{4.8}
\]

with 2,571 through 2,833 witnesses per slope.  Its inventory hash is

~~~text
ceeef4c9024450f0c935a0ae0aaf6b4dab693a7605f404f65f1655eac8ae0452
~~~

Again the two slopes omitted from the nonzero-locator inventory are zero and

\[
 -\alpha/\beta=1+15u.
\]

The fixed-root subinventory attains every other field element.  It therefore
already projects onto the **full post-deep nonzero-locator** frontier;
supports without the fixed root cannot add a post-deep slope.  Proposition
1.3 supplies the two deep zero-polynomial slopes, so the full finite frontier
has \(287+2=289\) slopes.

The lexicographically first fixed-root witnesses have common root intersection

\[
 \{3,4,5,6,7,8\}.
\tag{4.9}
\]

Their complete post-deep carrier has size 27 and excess five.  The exact cap
is

\[
 B_5=
 \left\lfloor
 \frac{\binom{27}{6}}{\binom65}
 \right\rfloor
 =49{,}335>287.
\tag{4.10}
\]

Thus all 287 post-deep slopes exit at or before the low-carrier owner.  The
other two slopes exit through the earlier deep owner.  The selected
excess-eleven rank-nine subfamily is an exact local control, but it is not a
first-match residual.

## 5. Quantifiers and first-match conclusion

The two objects must not be conflated:

~~~text
EXISTS a selected 29-slope family with affine rank nine
DOES NOT IMPLY
the complete post-deep family has a rank-nine residual.
~~~

For each row, the full finite frontier first partitions into exactly two deep
zero-polynomial slopes and the \(q-2\) nonzero-locator slopes.  The extended
deep owner is existential over valid noncontained witnesses, so its weight-two
witnesses remove the former pair.  For \(n=35\), the carrier cutoff is
structural for every selector in the remaining nonzero-locator ansatz.  For
\(n=36\), the exhaustive fixed-root inventory explicitly constructs one
complete selector for the remaining 287 slopes with excess five.  The
low-carrier owner is existential over complete selectors, so either
post-deep certificate is sufficient.  An earlier periodic, quotient, or other
first-match deletion can only shrink the slope set; both owner applications
are monotone under that deletion.  The safe conclusion is therefore
**deep or at-or-before low carrier**, not a claim that every slope's literal
first owner has otherwise been computed.

## 6. Scope and verdict

- **GREEN:** the source equation (1.7), nonzero-witness classification and
  uniform noncontainment, the two exact zero-polynomial deep exceptions in
  each row, both local rank-nine constructions, both exact post-deep slope
  inventories, the \(n=35\) post-deep ansatz excess-ten cut, the \(n=36\)
  post-deep complete excess-five selector, and the deep-or-at-or-before-low-
  carrier conclusion.
- **YELLOW:** any extrapolation to the KoalaBear domain or the deployed
  rank-nine aggregate.
- **RED:** promoting either 29-slope family to a complete selector, or moving
  the deployed ledger from these toy controls.

This packet does not instantiate the KoalaBear field or domain, prove a
deployed complete-selector inventory, close deployed rank nine, determine
\(U_Q\) or \(U_A\), move \(U_{\rm paid}\) or \(B_{\rm rem}\), authorize Lean,
or promote a theorem to the stable paper.

No layer-cake, moment, Markov, or Chebyshev argument is used.  All arithmetic
is exact finite-field or integer arithmetic at toy scale; it is not
asymptotic evidence.

## 7. Replay

~~~bash
HOME=/tmp/sage-home /usr/local/bin/sage \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.sage

python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --check
python3 -B \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --tamper-selftest
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --check
python3 -B -O \
  experimental/scripts/verify_m1_kb_branch3_rank9_t2_source_compatible_control_v1.py \
  --tamper-selftest
~~~
