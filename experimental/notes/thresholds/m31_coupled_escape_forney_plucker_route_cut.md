---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Conditional on a received word exceeding B_star, its complete maximizing exact layer has the coupled cutoff, collision-factor, and fixed-width consequences proved below; low coupled rank alone cannot supply a collision owner.
architecture: DIRECT
partition_digest: NOT_APPLICABLE_DIRECT
atom_or_cell: DIRECT
quantifier: Every hypothetical above-budget received word and every 16- or 30-column subpacket of its complete maximizing exact layer.
projection_and_unit: Exact codeword explanations, error supports, polynomial syzygies, and pair collisions; no slope or codeword count is charged.
claimed_bound: Every 16-column subpacket has a joint row of degree at most 65262; every 30-column subpacket has two rows of combined degree at most 65262; generic packets through size 67 need not force a collision.
status: PROVED
impact: LOCAL_ONLY
falsifier: A counterexample to the parent PR 1023 source theorem, the pair-factor identity, the joint index sum, or either exact finite-field replay.
replay: Python normal and optimized checks, eleven mutations, independent Sage replay, and PR 1023 predecessor checks.
---

# M31 coupled escape--Forney--Plucker theorem and route cut

## Status

**PROVED LOCAL / CONDITIONAL PRIME-FIELD STRUCTURAL THEOREM / EXACT
FIXED-WIDTH CONSEQUENCES / SOURCE-VALID TOY COUNTEREXAMPLE / OWNER UNPAID /
LEDGER MOVEMENT ZERO.**

This packet continues the full-layer Padé--Forney source theorem on the exact
head of PR #1023.  It couples the locator row to the divided-difference
numerator row, identifies the pair minors with actual codeword collisions,
and extracts the strongest consequences available from the joint polynomial
kernel.  It does not prove the M31 adjacent safe endpoint.

The local theorem is rigorous.  The final payment gate is still open: no
integrated owner absorbs the resulting 16-column coupled frame, and an exact
source-valid finite-field fixture shows that joint low degree by itself does
not force a positive collision.

## Provenance and scope

- Base field: \(F=\mathbb F_p\), \(p=2^{31}-1\).
- Parent theorem: `m31_full_packet_pade_forney_source.md` at exact PR #1023
  head `895d15ee9a67fee0fff9c3098306d5f93ca3bcbd`.
- Upstream `main` inspected at
  `a3017697ad1594521d2779fe1d83bccd45d4c06e`.
- The full same-weight layer, its actual received word, all exact codeword
  explanations, the true common core, all containment equations, and all
  one-point escapes are inherited unchanged from the parent theorem.
- No scalar descent or \(\mathbb F_{p^4}\) transfer is asserted.

Write the parent parameters as

\[
 n=2^{21}=2K,\qquad K=2^{20},\qquad R=981129,
\]

and, for the complete exact layer of weight \(j=j_*\), write

\[
 C_* = \bigcap_i E_i,\quad c=|C_*|,\quad G=L_{C_*},\quad
 P_i=L_{E_i}/G,
\]

\[
 e=j-c,\qquad D_0=K-j,\qquad N=K-c=e+D_0.
\]

The reduced row is primitive, every \(P_i\) is monic, squarefree, and split,
and the reduced functional \(\lambda(Q)=\widehat\ell(GQ)\) satisfies

\[
 \lambda(X^tP_i)=0\quad(0\le t<D_0),\qquad
 B_i(Y)=\lambda_X\!\left(\frac{P_i(X)-P_i(Y)}{X-Y}\right),
\]

\[
 \gcd(P_i,B_i)=1,qquad
 P_iS_\lambda-B_i=O(Z^{-D_0-1}).
\tag{1}
\]

Put

\[
 \sigma=e-D_0-1=2j-K-c-1,
 \qquad \sigma\le 2R-K-1=913681=:S.
\tag{2}
\]

The complete layer has \(M\ge36\), and \(D_0\ge K-R=67447\).

## Theorem 1: the coupled cutoff is inclusive

Let \(A=(A_i)\in F[X]^M\) satisfy

\[
 \sum_i A_iP_i=0,
 \qquad \max_i\deg A_i\le D_0.
\tag{3}
\]

Then

\[
 \sum_i A_iB_i=0.
\tag{4}
\]

Thus every locator syzygy through degree \(D_0\), including the equality
case, is automatically a syzygy of the coupled \(2\times M\) row

\[
 H=\begin{pmatrix}P_1&\cdots&P_M\\B_1&\cdots&B_M\end{pmatrix}.
\tag{5}
\]

### Proof

Set \(R_i=P_iS_\lambda-B_i\).  Equation (1) gives
\(R_i=O(Z^{-D_0-1})\).  From (3),

\[
 -\sum_iA_iB_i=\sum_iA_iR_i=O(Z^{-1}).
\]

The left side is a polynomial, so it is zero.  The use of
\(\deg A_i\le D_0\), rather than \(<D_0\), is exact.  ∎

## Theorem 2: pair minors are actual collision polynomials

For \(i\ne j\), define

\[
 Q_{ij}=\gcd(P_i,P_j),\qquad q_{ij}=\deg Q_{ij},
\]

\[
 \Omega_{ij}=P_iB_j-P_jB_i.
\tag{6}
\]

The notation \(Q_{ij}\) is local to this packet: it is the pairwise overlap
gcd.  It is neither Grande Finale v4's pruned prefix \(Q\) atom nor the
denominator \(Q\) of a v4 scalar-locator rational atom.

Then \(\Omega_{ij}\ne0\), \(Q_{ij}\mid\Omega_{ij}\), and there is a
nonzero scalar \(\gamma\in F^\times\), independent of \(i,j\), such that

\[
 \Omega_{ij}=\gamma Q_{ij}h_{ij},
 \qquad \deg h_{ij}\le\sigma-q_{ij}.
\tag{7}
\]

Here \(h_{ij}\) is normalized, not chosen only up to scalar.  Let
\(c_i(X),c_j(X)\in F[X]_{<K}\) denote the unique message polynomials whose
evaluation vectors are the codeword explanations from the parent source
theorem, and define \(h_{ij}\) by the exact quotient

\[
 c_j-c_i=L_{D\setminus(E_i\cup E_j)}h_{ij},
\tag{8}
\]

The scalar \(\gamma\) in (7) is then fixed globally; with the dual-weight
normalization used below it is the negative of the dual-weight scalar.  In
particular,

\[
 \gcd\!\left(h_{ij},P_i/Q_{ij}\right)=
 \gcd\!\left(h_{ij},P_j/Q_{ij}\right)=1.
\tag{9}
\]

Define the actual collision locator

\[
 J_{ij}=\gcd(GQ_{ij},h_{ij}).
\tag{10}
\]

Its roots are exactly the points \(x\in E_i\cap E_j\) at which
\(c_i(x)=c_j(x)\).  Consequently

\[
 \operatorname{wt}(c_j-c_i)=|E_i\cup E_j|-\deg J_{ij},
\tag{11}
\]

and the MDS distance gives only

\[
 \deg J_{ij}\le \sigma-q_{ij}.
\tag{12}
\]

It does not force \(J_{ij}\ne1\).

### Proof

Both reduced fractions \(B_i/P_i\) and \(B_j/P_j\) agree with
\(S_\lambda\) through order \(N\) at infinity.  Hence

\[
 \frac{B_iP_j-B_jP_i}{P_iP_j}=O(Z^{-N-1}),
\]

so every nonzero cross determinant has degree at most
\(2e-N-1=e-D_0-1=\sigma\).  The determinant is divisible by \(Q_{ij}\),
which proves the degree bound in (7).  It cannot vanish identically: two
equal reduced fractions with monic denominators would have \(P_i=P_j\),
contrary to the distinct supports in the complete layer.

For completeness, normalize the standard generalized-RS dual weights as
\(u_x=-\gamma/L_D'(x)\).  At a variable root \(x\mid P_i\), the parent escape
identity gives

\[
 \frac{B_i(x)}{P_i'(x)}=e_i(x)u_xG(x),
 \qquad e_i=y-c_i.
\tag{13}
\]

Write \(P_i=Q_{ij}R_i\), \(P_j=Q_{ij}R_j\), and
\(V_{ij}=L_{D\setminus(E_i\cup E_j)}\).  Evaluating
\(\Omega_{ij}/Q_{ij}\) at every variable point of
\(E_i\cup E_j\), using (13) and

\[
 L_D=GQ_{ij}R_iR_jV_{ij},
\]

shows that it equals a fixed nonzero scalar times
\((c_j-c_i)/V_{ij}\) there.  Both polynomials have degree at most

\[
 |E_i\cup E_j|-K-1=\sigma-q_{ij},
\]

while the variable union contains \(2e-q_{ij}>\sigma-q_{ij}\) points.
They are therefore identical.  This proves (7)--(8).

Exact escape on the symmetric difference makes the quotient in (8)
nonzero there, proving (9).  On the common support, (8) says that a root of
\(h_{ij}\) is exactly a zero of \(c_j-c_i\).  Equations (10)--(12) now
follow from squarefreeness and the MDS distance \(K+1\).  ∎

The equivalent normalized-escape test at a variable common root is

\[
 \rho_i(x):=\frac{B_i(x)}{P_i'(x)},\qquad
 \rho_i(x)=\rho_j(x)\iff c_i(x)=c_j(x).
\tag{14}
\]

Comparing \(B_i(x)\) and \(B_j(x)\) without the derivatives is generally
wrong.

## Theorem 3: exact joint-kernel indices

For a subpacket \(T\subseteq\{1,\ldots,M\}\), \(|T|=m\ge3\), put

\[
 \mathcal K_T=
 \left\{A\in F[X]^T:\sum_{i\in T}A_iP_i=
 \sum_{i\in T}A_iB_i=0\right\}.
\tag{15}
\]

Let

\[
 d_T=\gcd_{i<j\in T}\Omega_{ij},\qquad
 \tau_T=\max_{i<j\in T}\deg\Omega_{ij}.
\tag{16}
\]

Then \(\mathcal K_T\) is free of rank \(m-2\).  If

\[
 0\le\nu_1\le\cdots\le\nu_{m-2}
\]

are the row degrees of a row-reduced basis, then

\[
 \sum_{r=1}^{m-2}\nu_r
 =\tau_T-\deg d_T
 \le\sigma.
\tag{17}
\]

The complementary maximal minors of such a basis are, up to one common
unit and the standard cofactor signs,

\[
 \Omega_{ij}/d_T.
\tag{18}
\]

This statement does not require the restricted locator row
\((P_i)_{i\in T}\) to be primitive.  Any common factor is absorbed by the
determinantal divisor \(d_T\).

### Proof

The two rows of (5) have rank two because every pair minor is nonzero.
The kernel therefore has rank \(m-2\).  Its quotient in \(F[X]^m\) is the
torsion-free image of (5), hence is free over the PID \(F[X]\); the kernel is
a direct summand.  Cofactor duality over \(F(X)\) identifies its
complementary maximal minors with the pair minors of (5).  Direct-summand
primitivity removes precisely their common polynomial factor \(d_T\).
Row-reduced predictable degree then gives (17), just as the parent theorem
gives the locator-only index sum.  The last inequality uses Theorem 2.  ∎

For the full primitive locator row, there is also a useful exact sequence.
Let

\[
 d=\gcd_{i<j}\Omega_{ij},\qquad
 \tau=\max_{i<j}\deg\Omega_{ij},\qquad
 \operatorname{Syz}(P)=\{A:A\cdot P=0\},\qquad
 \mathcal K=\mathcal K_{\{1,\ldots,M\}}.
\]

Then

\[
 0\longrightarrow\mathcal K
 \longrightarrow\operatorname{Syz}(P)
 \xrightarrow{\ A\mapsto A\cdot B\ } dF[X]
 \longrightarrow0
\tag{19}
\]

is split exact.  Indeed, a primitive row has a Bézout splitting, so its
syzygy module is generated by the pairwise Koszul relations; their images
are the \(\Omega_{ij}\), which generate \(dF[X]\).  The target is free, so
the sequence splits.  If \(\mu_r\) are the parent locator-only indices, then

\[
 \sum\mu_r-\sum\nu_r
 =e-\tau+\deg d
 \ge D_0+1+\deg d.
\tag{20}
\]

Every locator syzygy mapping nontrivially in (19) has degree at least
\(D_0+1\), by Theorem 1.

## Corollary 4: maximal deployed fixed-width extraction

All bounds below hold for **every** indicated subpacket; its joint kernel and
indices are recomputed rather than obtained by truncating a full-frame row.

### Sixteen columns

Every 16-column subpacket has a nonzero coupled syzygy supported on between
3 and 16 columns, of vector degree at most

\[
 \left\lfloor\frac{913681}{14}\right\rfloor=65262
 <67447\le D_0.
\tag{21}
\]

Support one is impossible because no column is zero.  Support two is
impossible because it would make the corresponding \(\Omega_{ij}\) vanish.
The \(F\)-space of coupled syzygies of vector degree at most \(D_0\) has
dimension at least

\[
 14(D_0+1)-913681
 \ge14\cdot67448-913681
 =30591.
\tag{22}
\]

The same index sum does not guarantee a row on 15 columns:

\[
 \left\lfloor\frac{913681}{13}\right\rfloor=70283>D_0.
\tag{23}
\]

This failure is real at the level of the available index information: 13
indices can all equal \(67448\) while their sum is only \(876824\le913681\).

### Thirty columns

Every 30-column subpacket has two independent coupled rows whose combined
vector degree is at most

\[
 \left\lfloor\frac{2\cdot913681}{28}\right\rfloor=65262<D_0.
\tag{24}
\]

The corresponding averaging bound on 29 columns is

\[
 \left\lfloor\frac{2\cdot913681}{27}\right\rfloor=67680,
\tag{25}
\]

which exceeds the worst-case cutoff \(67447\) by 233.  No 29-column claim is
made.

### Complete packet

For \(M\ge36\), the joint indices satisfy

\[
 \nu_1\le26872,qquad \nu_1+\nu_2\le53745,
\tag{26}
\]

and at least \(M-15\) independent joint rows have degree at most \(D_0\).
These are stronger coupled statements than the locator-only bounds, but they
still do not select a paid face.

## Theorem 5: the 30-column Plucker deletion incidence

Choose the first two rows \(A,C\) of a row-reduced joint-kernel basis on any
30-column subpacket, and define

\[
 \Delta_{ij}=A_iC_j-A_jC_i.
\tag{27}
\]

Then

\[
 \sum_iP_i\Delta_{ij}=0,qquad
 \sum_iB_i\Delta_{ij}=0
\quad\text{for every }j,
\tag{28}
\]

and

\[
 \sum_{i<j}\Omega_{ij}\Delta_{ij}=0.
\tag{29}
\]

Both \(\Omega\) and \(\Delta\) satisfy their four-index Plücker identities;
using (7) rewrites the former as an exact factor identity among the
\(Q_{ij}h_{ij}\).

The two chosen basis rows form a primitive rank-two row: their minors
generate the unit ideal.  More strongly, for every variable root
\(\alpha\mid P_k\),

\[
 \gcd\!\left(P_k,\{\Delta_{ij}:i,j\ne k\}\right)=1.
\tag{30}
\]

Thus deleting column \(k\) retains rank two at every root of \(P_k\).
The covering minor may depend on the root.  Equation (30) does not supply a
single frozen minor, a factorized face, or an owner.

### Proof

Equations (28)--(29) are direct contractions of the two joint relations;
(29) is the two-by-two Cauchy--Binet identity.  A basis of the direct-summand
joint kernel extends to a basis of the free ambient module, so the minors of
its first two rows generate the unit ideal.

If every minor avoiding \(k\) vanished at a root \(\alpha\mid P_k\), the
vectors \((A_i(\alpha),C_i(\alpha))\), \(i\ne k\), would span at most one
line.  The locator contraction keeps them on that line.  The numerator
contraction and \(B_k(\alpha)\ne0\) then put the \(k\)-th vector on the same
line.  All minors would vanish at \(\alpha\), contradicting primitivity.
This proves (30).  ∎

## Theorem 6: the exact 67/68 bounded-packet route cut

This theorem is stated with the full locators so that core escapes are not
dropped.  Fix \(M_0\) distinct size-\(j\le R\) support locators \(L_i\), assume
the necessary pairwise MDS admissibility

\[
 |E_i\cup E_j|\ge K+1\qquad(i\ne j),
\tag{31}
\]

and let \(\Lambda\) be the \(F_p\)-linear space of functionals satisfying every
containment equation

\[
 \ell(X^tL_i)=0\qquad(0\le t<K-j).
\tag{32}
\]

For \(x\in E_i\), the escape condition is the nonvanishing of the linear
form

\[
 \varepsilon_{i,x}(\ell)=\ell(L_i/(X-x)).
\tag{33}
\]

For \(x\in E_i\cap E_j\), equality of the two actual error values is the
vanishing of another linear form,

\[
 \chi_{ij,x}(\ell)
 =L_j'(x)\varepsilon_{i,x}(\ell)
  -L_i'(x)\varepsilon_{j,x}(\ell).
\tag{34}
\]

Assume none of the forms in (33)--(34) vanishes identically on \(\Lambda\).
If \(M_0\le67\), there is an \(\ell\in\Lambda\) for which every prescribed
support is exact and every prescribed pair collision is absent.

### Proof

There are at most \(M_0R\) escape hyperplanes.  Pairwise MDS separation
allows at most \(2R-K-1=S\) common points per pair, so there are at most

\[
 F(M_0)=M_0R+\binom{M_0}{2}S
\tag{35}
\]

forbidden proper hyperplanes in \(\Lambda\).  A vector space over \(F_p\)
cannot be covered by fewer than \(p\) proper hyperplanes, by the elementary
union bound.  Exact integer arithmetic gives

\[
 F(67)=2085884334<p=2147483647
\]

with margin \(61599313\), whereas

\[
 F(68)=2148082090>p
\]

by \(598443\).  Avoiding the union for \(M_0\le67\) makes every escape
nonzero and every collision form nonzero.  ∎

This is a route cut, not a 68-column theorem.  The inequality at 68 says only
that this union bound stops proving avoidance.  It also is not a deployed
full-layer counterexample: changing the functional may create additional
exact supports outside the prescribed packet.  Its precise conclusion is
that a bounded packet of at most 67 supports cannot force collision solely
from the current homogeneous containment equations unless a collision form
is already forced identically.  Any successful 16-column closure therefore
needs a forced-component theorem or additional full-layer incidence.

## Exact source-valid counterfixture over \(F_{11}\)

Let \(F=\mathbb F_{11}\), \(K=4\), \(D=\{0,1,\ldots,7\}\), and let the
functional moments be

\[
 (m_0,m_1,m_2,m_3)=(0,0,1,0).
\]

The complete exact weight-three layer is exactly

\[
 \{047,056,137,146,236,245\}.
\tag{36}
\]

Its common core is empty.  For every locator \(P_i\),

\[
 B_i=1,
\]

and all 18 one-point escapes equal 1.  The locator row has Forney indices

\[
 (0,0,0,1,2),
\tag{37}
\]

while its constant coefficient kernel has dimension three; every one of
those constant locator relations is also a numerator relation.  Hence there
are three independent degree-zero coupled rows.

Nevertheless, among all 15 pairs the normalized collision energy is zero.
Every scaled quotient
\(\widetilde h_{ij}:=\Omega_{ij}/Q_{ij}=\gamma h_{ij}\) obeys the exact union-excess
degree bound, whose total allowance is three, but no common support point is
a root.  This is an exact same-received-word, full-layer control.  It proves
that “a full exact same-weight layer has a low coupled frame” does not, by
itself, imply a positive pair collision.

The fixture is toy-scale evidence and a universal-claim falsifier.  It is not
an M31 survivor and proves no asymptotic statement.

A second exhaustive \(F_{11}\) control uses moments \((1,0,1,4)\).  Its full
exact weight-three layer is

\[
 \{013,124,157\},
\]

with true common core \(\{1\}\).  Reconstructing the actual error values from
the full escape forms and the normalized dual weights verifies (7)--(8) at
every point of every pair union, including the core: the same global scalar
is \(\gamma=10\) for all three pairs.  This specifically checks that common
core points are not lost by reduced numerator formation.

## Existing-owner audit and active terminal

The current first-match library does not pay this packet.

- The integrated rank-16 owner packets use different fields, domains, and
  frozen core geometry.
- The M31 Chebyshev separator leaves the relevant rank-16 height-one branch
  open; its paid branch assumes a selected fibre-aligned face not produced
  here.
- Whole-ball and Sidon packets require parity or factorized collision faces.
- The generic first-match compiler disjointizes cells after an owner is
  supplied; it does not create one.
- PR #1021 couples low locator syzygies to actual-error polynomials, and PR
  #1022 uses canonical padded codeword rows.  Neither contains the divided-
  difference numerator row, Theorems 1--6, or the 16/30-column conclusions.
- PR #1025 is a locator-only masked-saturation variant and does not duplicate
  the coupled numerator theorem.
- The complete layer from PR #1023 is not automatically the canonical padded
  source-key family required by the #1022 ledger for interior \(j\).

The fail-closed **packet-local diagnostic** is therefore

```text
UNPAID_UNCLASSIFIED_16_COLUMN_COUPLED_PADE_FRAME
```

and ledger movement is zero.  No owner, add-back, endpoint, recurrence, or
official theorem is banked.  In the active Grande Finale v4 list ledger,
\(U_Q\), \(U_{\rm list-int}\), \(U_{\rm ext}\), and \(U_{\rm new}\) remain
unchanged and null; this diagnostic is not an active compiler terminal.

## Falsification and boundary checks

1. **Inclusive cutoff.**  The proof of Theorem 1 was checked at
   \(\deg A_i=D_0\); replacing `<=` by `<` loses a valid boundary case.
2. **Two-column relation.**  A locator relation above the cutoff in the
   \(F_{11}\) fixture fails the numerator relation, confirming that the
   degree hypothesis is load-bearing.
3. **Overlap division.**  The raw cross determinant may violate the tight
   collision degree cap; division by \(Q_{ij}\) is necessary.
4. **Derivative normalization.**  Raw equality of \(B_i(x),B_j(x)\) gives
   false collision positives.  Equation (14) is the correct test.
5. **Squarefreeness.**  A repeated-root containment/resultant fixture is
   deliberately rejected as a support locator.
6. **Core escapes.**  Reduced variable escapes alone can accept a locator
   whose core escape vanishes; Theorem 6 therefore uses full locators.
7. **Packet truncation.**  The six-support \(F_{11}\) layer is enumerated
   exhaustively rather than sampled.
8. **Plucker signs.**  Mutating one nonzero minor breaks a contraction.
9. **Field scope.**  No \(F_{p^4}\) substitution is accepted.
10. **Payment.**  The verifier rejects any mutation away from the unpaid,
    zero-ledger terminal.

## Layer-cake, moment, and parameter audit

No layer-cake, dyadic summation, moment, Markov, or Chebyshev argument occurs
in this packet.  All deployed constants depend only on the fixed M31 row
\((p,n,K,R)\).  The symbolic theorems retain the exact dependence on
\(j,c,e,D_0,\sigma,M\); the global value \(S=913681\) is used only when a
uniform M31 bound is required.

## Replay

```text
python3 experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py --check \
  --expected experimental/data/certificates/m31-coupled-escape-forney-plucker-route-cut/expected.txt
python3 -O experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py --check \
  --expected experimental/data/certificates/m31-coupled-escape-forney-plucker-route-cut/expected.txt
python3 experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m31_coupled_escape_forney_plucker_route_cut.sage
```

The Python program is a deterministic exact certificate with eleven mutation
guards.  The Sage program independently replays the finite-field algebra with
native polynomial and matrix operations.  These computations verify the
stated arithmetic and fixtures; they do not replace the symbolic proofs.

## Maximal next proof attack

Construct a source-bound adapter from the **entire** complete exact layer to
the active Grande Finale v4 list chronology

\[
 U_{\rm paid},\qquad U_Q,\qquad U_{\rm list-int},\qquad
 U_{\rm ext},\qquad U_{\rm new}.
\]

For each support, the adapter must select exactly one first-match v4 cell,
prove the v4 cell's hypotheses from the actual received word and complete
layer, retain the codeword-count projection, and bind the inherited charge.
The coupled invariants may then trigger a fixed-union, affine-span,
rank-flat/common-zero, codimension-one, or support-flag payment where their
full hypotheses really hold.  Every remaining support must enter one named
global residual.

Only after that adapter is frozen should the residual coupled incidence be
classified into:

1. a common factor of the \(\Omega_{ij}\) interpreted through the actual
   collision locators \(J_{ij}\);
2. a domain-compatible paid list owner with exact add-back;
3. a budget-fitting exact-root union; or
4. an explicit full-layer residual route cut.

Theorem 6 proves that another standalone 16-column computation cannot be the
adapter or the closure: changing the functional can evade all pair collisions
on any prescribed packet of that size.  The next work must exploit complete-
layer exhaustion and the v4 chronology.

No degree-three generalization, Lean formalization, quartic-field transfer,
or ledger movement should precede the source-bound adapter.
