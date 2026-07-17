# M1 rank-nine regular locator-span shortcut refuted v1

- **Status:** PROVED parametric counterexample / generic local route cut / no
  ledger movement / deployed KoalaBear residual remains OPEN.
- **Target:** the proposed implication from a rank-minimizing
  \((s_*,t)=(9,10)\) selector, intrinsic carrier excess
  \(\kappa_*=11\), transversality, and regular residual (6.1) to a bounded
  locator span or a bounded union of bounded-dimensional locator spaces.
- **Predecessor:**
  `experimental/notes/m1/m1_kb_branch3_rank9_sparse_chart_boundary_v1.md`.
- **Companion verifiers:**
  `experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.py`
  and
  `experimental/scripts/verify_m1_rank9_regular_locator_span_shortcut_refuted_v1.sage`.

For every integer \(j\ge10\) the construction below gives a finite-field
Reed--Solomon instance and an explicitly declared retained slope family
\(\Gamma\) whose unique complete noncontained selector satisfies

```text
s_*=9
t=10
kappa_*=11
all regular residual (6.1) gates
```

but

\[
  \operatorname{rank}\{\ell_O\}=j+1.
\tag{0.1}
\]

Thus no locator-span bound depending only on
\((s_*,t,\kappa_*)=(9,10,11)\) follows from the generic local hypotheses.
More strongly, a cover by \(B\) vector subspaces of dimension at most \(C\)
requires

\[
  BC\ge j+1.
\tag{0.2}
\]

The exact terminal is

```text
GENERIC_LOCAL_RANK_TO_LOCATOR_SPAN_SHORTCUT_REFUTED
```

This does **not** assert that \(\Gamma\) is the full bad-slope set.  It does
not instantiate the KoalaBear domain or execute its periodic, quotient,
Johnson, or B11 first-match masks.  Full-bad-family exhaustion and deployed
first-match survival are extra hypotheses and may be load-bearing.

## 1. Statement audited

The predecessor's regular residual retains, at every selected slope
\(\gamma\), a monic squarefree \(D\)-split degree-\(j\) locator \(L_O\) with
coefficient vector \(\ell_O\) satisfying

\[
  \Delta(\gamma)\ne0,\qquad
  M(\gamma)\ell_O=0,\qquad
  H_2\ell_O\ne0.
\tag{1.1}
\]

On the explicitly declared retained family \(\Gamma\), the selector is
complete, rank-minimizing, transverse, has affine-difference rank \(s_*=9\),
raw witness rank \(t=10\), and lies after the intrinsic low-carrier
alternative \(\kappa_*\le10\).  The audited shortcut asserted that these
conditions, without any exhaustion or deployed first-match premise on
\(\Gamma\), force one bounded-dimensional locator space or a bounded number
of such spaces.  The construction below disproves both versions.

## 2. Exact \(j=10\) control

Let

\[
  F_0=\mathbb F_2[u]/(u^{23}+u^5+1).
\tag{2.1}
\]

The class \(u\) has multiplicative order \(2^{23}-1\).  Put

\[
  a=0,\qquad b=1,\qquad
  r_i=u^{2^i},\qquad
  z_i=(1-r_i)^{-1}\quad(0\le i<22).
\tag{2.2}
\]

Set \(B=\{z_0,\ldots,z_{21}\}\), \(D=\{a,b\}\sqcup B\), and

\[
  C=\operatorname{RS}_{F_0}(D,13)=[24,13,12]_{F_0}.
\tag{2.3}
\]

Thus

\[
  n=24,\quad k=13,\quad R=11,\quad j=10,\quad A=n-j=14.
\tag{2.4}
\]

Use the sparse pair

\[
  \epsilon_1=1_a,\qquad
  \epsilon_2=1_b,\qquad
  v_\gamma=\epsilon_1+\gamma\epsilon_2.
\tag{2.5}
\]

Freeze these five eleven-point cores, written as index subsets of \(B\):

```text
C1=(3,5,6,7,9,11,13,16,17,20,21)
C2=(0,2,3,6,7,8,9,10,12,13,19)
C3=(1,2,4,6,7,8,10,15,17,20,21)
C4=(2,3,5,9,11,12,13,14,19,20,21)
C5=(0,1,2,5,6,12,14,15,18,20,21)
```

Their common intersection is empty and every pair has symmetric difference
at least eight.  For \(C_i\) and \(z\in B\setminus C_i\), put

\[
  Z=C_i\cup\{z\},\qquad
  p_Z(X)=\prod_{x\in Z}(X-x),\qquad
  q_Z(X)=\frac{p_Z(X)}{p_Z(a)},
\tag{2.6}
\]

\[
  \gamma_Z=q_Z(b),\qquad
  e_Z=v_{\gamma_Z}-\operatorname{ev}_D(q_Z),\qquad
  O_Z=B\setminus Z.
\tag{2.7}
\]

There are \(5\cdot11=55\) distinct root sets.

## 3. Slope injectivity and unique witnesses

For each \(z_i\), characteristic two and (2.2) give

\[
  \frac{b-z_i}{a-z_i}=r_i.
\tag{3.1}
\]

Consequently

\[
  \gamma_Z
  =\frac{p_Z(b)}{p_Z(a)}
  =\prod_{z_i\in Z}r_i
  =u^{\sum_{z_i\in Z}2^i}.
\tag{3.2}
\]

Binary subset sums are distinct and their maximum
\(2^{22}-1\) is below \(2^{23}-1\).  Hence all subset products are distinct;
in particular the 646,646 twelve-subset products and the 55 slopes are
distinct.  Every selected slope is nonzero.

The polynomial \(q_Z\) agrees with \(v_{\gamma_Z}\) at \(a,b\), vanishes
exactly on \(Z\), and is nonzero on \(O_Z\).  Therefore

\[
  \operatorname{supp}(e_Z)=O_Z,\qquad |O_Z|=10.
\tag{3.3}
\]

This is the unique noncontained radius-ten witness at its slope.  Indeed, a
nonzero degree-at-most-twelve polynomial \(c\) with
\(\operatorname{wt}(v_\gamma-\operatorname{ev}(c))\le10\) has at least
fourteen agreements.  If \(z_B\) is its number of roots on \(B\) and \(u_E\)
its agreements on \(E=\{a,b\}\), then

\[
  z_B\le12,\qquad u_E\le2,\qquad z_B+u_E\ge14,
\]

so \((z_B,u_E)=(12,2)\).  The roots and normalization at \(a\) determine
\(q_Z\), while (3.2) determines the unique \(Z\) at \(\gamma\).  The zero
codeword gives the contained weight-two error \(v_\gamma\); every padded
size-\(j\) support contains \(b\), so it fails \(H_2\ell_O\ne0\).

Thus the explicitly declared retained 55-slope family \(\Gamma\) has one
complete noncontained selector.  It is automatically rank-minimizing, and its
carrier minimum is the carrier excess computed below.  The ambient instance
has additional bad slopes; no full-bad-set exhaustion is claimed or needed
for the precisely scoped generic-local implication being refuted.

## 4. Exact ranks and carrier

For fixed \(C_i\), all \(q_{C_i\cup\{z\}}\) lie in

\[
  p_{C_i}(X)F_0[X]_{\le1}.
\tag{4.1}
\]

The ten polynomials obtained from two moving roots in each pencil are
independent.  In coefficient columns \(0,\ldots,9\), their determinant is

\[
 u^{22}+u^{16}+u^{15}+u^{14}+u^{12}+u^{11}+u^{10}
 +u^7+u^6+u^5+u^2+1\ne0.
\tag{4.2}
\]

Thus the five pencil spaces have direct-sum dimension ten.  Evaluation on
\(B\) is injective for degree-at-most-twelve polynomials, and
\(e_Z|_B=-q_Z|_B\).  Hence

\[
  \dim\operatorname{span}\{e_Z\}=10.
\tag{4.3}
\]

Every \(q_Z(a)=1\).  The differences lie in the kernel of evaluation at
\(a\), and nine basis differences are independent.  Therefore

\[
  s_*=\dim\operatorname{span}\{e_Z-e_{Z_0}\}=9.
\tag{4.4}
\]

The five cores have empty common intersection, so

\[
  \bigcup_Z O_Z=B.
\tag{4.5}
\]

The same ten basis supports already recover this union.  Consequently

\[
  N_V=22=R+11,\qquad
  \nu=11,\qquad
  \kappa_*=11.
\tag{4.6}
\]

This control is not paid by the \(\kappa_*\le10\) carrier owner.

## 5. Regular residual and transversality

Use the generalized Reed--Solomon weights

\[
  \lambda_x=
  \left(\prod_{y\in D\setminus\{x\}}(x-y)\right)^{-1}
\tag{5.1}
\]

and syndrome rows \(0,\ldots,R-1\).  Since \(R-j=1\), the closed-ball
Pad\'e--Hankel matrix has one row.  Freeze coefficient column one.  Because
\(a=0\), \(b=1\), and \(v_\gamma\) is supported on \(\{a,b\}\),

\[
  \Delta(\gamma)=\lambda_b\gamma\ne0.
\tag{5.2}
\]

Let \(L_{O_Z}(X)=\prod_{x\in O_Z}(X-x)\).  The evaluations of
\(v_{\gamma_Z}L_{O_Z}\) and \(q_ZL_{O_Z}\) agree on \(D\), while the latter
has degree \(12+j=n-2\).  The standard weighted degree-\(\le n-2\) identity
therefore gives

\[
  M(\gamma_Z)\ell_{O_Z}=0.
\tag{5.3}
\]

Also \(b\notin O_Z\), so

\[
  H_2\ell_{O_Z}=\lambda_bL_{O_Z}(b)\ne0.
\tag{5.4}
\]

The parity columns indexed by \(O_Z\) have rank \(j\); adjoining the column at
\(b\) raises the rank to \(j+1\).  Thus \(y_1\notin H(F^{O_Z})\), proving
transversality.  Every locator is monic, squarefree, degree \(j\), and
\(D\)-split.  All regular residual (1.1) gates hold.

## 6. Parametric obstruction

Fix \(j>10\).  Retain \(F_0\), the first 22 ratios and points, and the five
cores.  Introduce \(j-10\) new ratio variables.  For every two distinct
twelve-subsets \(I,J\) of the enlarged ratio set, impose

\[
  \prod_{i\in I}r_i-\prod_{i\in J}r_i\ne0,
\tag{6.1}
\]

together with nonzero, nonunit, and distinctness conditions for the new
ratios.  Each left side is a nonzero Laurent polynomial over \(F_0\): unequal
new-variable exponent vectors give different monomials; equal vectors leave
different old products by the binary injection.

The finite product of these Laurent polynomials is nonzero.  The algebraic
closure of \(F_0\) is infinite, so a tuple exists outside their finite union
of zero hypersurfaces.  Its finitely many coordinates lie in one finite
extension \(F/F_0\).  Mapping each new ratio \(r\) to \(z=(1-r)^{-1}\) yields
\(|B|=j+12\) distinct points with injective twelve-subset products.

Repeat Sections 2--5.  The row is

\[
  n=j+14,\qquad k=13,\qquad R=j+1,\qquad A=14,
\tag{6.2}
\]

and there are \(5(j+1)\) distinct slopes.  Scalar extension preserves (4.2),
so

\[
  (s_*,t)=(9,10).
\tag{6.3}
\]

The ten old basis supports contain every new point and still cover the first
22 points.  Hence

\[
  N_V=j+12=R+11,\qquad \kappa_*=11.
\tag{6.4}
\]

Uniqueness, rank-minimality, transversality, and regularity are unchanged.

For one core \(C\), let \(Q=B\setminus C\), so \(|Q|=j+1\).  Its supports are
\(Q\setminus\{z\}\), and its locators are

\[
  L_z(X)=\prod_{x\in Q\setminus\{z\}}(X-x)\qquad(z\in Q).
\tag{6.5}
\]

Evaluation on \(Q\) is diagonal up to nonzero scalars:
\(L_z(w)=0\) for \(w\ne z\), while \(L_z(z)\ne0\).  These locators form a
Lagrange basis of \(F[X]_{\le j}\), proving (0.1).  A \(C\)-dimensional vector
subspace contains at most \(C\) members of this independent family, proving
(0.2).  A cover by \(B\) projective subspaces of dimension at most \(c\)
similarly requires \(B(c+1)\ge j+1\).

## 7. Dependencies and literature check

- **PROVED:** exact \(j=10\) field arithmetic, all 55 witnesses, rank triple
  \((9,10,11)\), unique selector, carrier equality, fixed-chart regularity,
  and transversality.  Python and Sage replay these independently.
- **PROVED:** parametric finite-extension existence, scalar extension of
  (4.2), carrier identities, and Lagrange-basis locator rank.
- **IMPORTED:** the exact closed-ball Pad\'e--Hankel convention and predecessor
  definitions of \(s_*\), \(\kappa_*\), transversality, and the regular route.
- **UNVERIFIED / outside scope:** survival under the actual KoalaBear
  periodic, quotient, Johnson, and B11 masks, and equality of the declared
  \(\Gamma\) with a full bad-slope family.

A targeted TheoremSearch query and an independent web/paper search found no
primary-source theorem with the audited cross-locator conclusion.  This
negative search is context only; the proof does not depend on an
absence-of-literature claim.  The load-bearing distinctions were checked
against:

- Rosenkilde, [Power decoding Reed--Solomon codes up to the Johnson
  radius](https://arxiv.org/abs/1505.02111), Lemmas 2.1--2.2 and 7.3--7.4:
  the key equations form a simultaneous Hermite--Pad\'e module for one
  received word, not an \(F\)-linear span bound across varying slope matrices.
- Wu, [New list decoding algorithms for Reed--Solomon and BCH
  codes](https://arxiv.org/abs/cs/0703105), Section IV.A, Lemma 3 and Theorem
  1: the two-generator object is an \(F[X]\)-module with polynomial
  multipliers, not a two-dimensional \(F\)-vector space of locators.
- Lovett, [MDS matrices over small
  fields](https://arxiv.org/abs/1803.02523), Definition 1.4 and Theorem 1.7:
  GM--MDS independence depends on every support intersection, not just the
  carrier union or \(\nu\), and points toward full locator independence.
- Brakensiek--Gopi--Makam, [Generic Reed--Solomon codes achieve list-decoding
  capacity](https://arxiv.org/abs/2206.05256), Definitions 1.9--1.11 and
  Theorems 1.12--1.13: higher-order MDS results are domain and
  support-intersection statements, not consequences of the rank triple.

Both searches therefore point to actual support intersections and
fixed-domain determinants, not to a rank-only shortcut.

## 8. Audit verdict and ledger

- **Parameter dependence:** \(s_*=9\), \(t=10\), and \(\kappa_*=11\) are
  fixed; locator rank \(j+1\) is unbounded.  No hidden
  \(T,Y,\mathcal L,\mathcal L_{\bar I},\lambda,I\), or asymptotic constant
  appears.
- **Layer-cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Edge cases / notation:** \(j\ge10\), full weight removes padding
  ambiguity, the zero-codeword witness is rejected, and every slope is
  nonzero.
- **Numerical evidence:** the \(j=10\) result is an exact computer-assisted
  certificate, not statistical evidence and not a deployed-domain census.
- **Generic local verdict:** **RED** -- constant-span and fixed bounded-union
  implications from the stated local hypotheses are false when they impose no
  full-bad-family exhaustion or deployed first-match condition on \(\Gamma\).
- **KoalaBear owner-strengthened verdict:** **YELLOW** -- the deployed domain
  and actual first-match masks remain unresolved.

The ledger is unchanged:

\[
  U_{\rm paid}=2{,}602{,}502{,}999,\qquad
  B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\tag{8.1}
\]

There is no ledger movement.

## 9. Minimal next action

Bank this route cut and stop pursuing any locator-span or bounded-cover lemma
whose constants depend only on \(s_*,t,\kappa_*\) and regularity.  The next
closure attempt must use a deployed-domain or executable first-match owner
hypothesis in a load-bearing way.  Test GM--MDS intersection conditions and
fixed-domain locator determinants on actual retained supports; do not increase
the generic rank bound and do not start rank at least ten.
