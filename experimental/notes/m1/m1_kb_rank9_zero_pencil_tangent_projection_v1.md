# M1 KoalaBear rank-nine zero-pencil tangent projection v1

## Status

**PROVED source-bound projection lemma for one fixed sparse translation;
YELLOW global first-match payment.  No ledger movement.**

This note isolates the zero-codeword case left inside the canonical
rank-nine rich-pencil atlas.  It proves that this case is not a new primitive
rich-pencil component: every eligible zero-pencil slope is already in the
sparse-tangent slope image of the same translated received pair.

The resulting cap is local to one fixed SP3 translation.  The existing
`SPARSE_TANGENT_RANK9_CONDITIONAL_CAP` has not yet been promoted to a globally
deduplicated first-match owner, so this note does not bank the cap or delete a
term from the deployed ledger.

## 1. Frozen row and translation

The deployed row is

\[
 p=2{,}130{,}706{,}433,\qquad F=\mathbb F_{p^6},
 \qquad |D|=n=2^{21},
\]

\[
 k=2^{20},\qquad A=1{,}116{,}048,
 \qquad R=n-k=1{,}048{,}576,
\]

\[
 j=n-A=981{,}104,\qquad t=A-k=67{,}472.
\tag{1.1}
\]

Fix one source-bound SP3 translation

\[
 (\epsilon_0,\epsilon_1),\qquad
 \Sigma=\operatorname{supp}(\epsilon_0)\cup
        \operatorname{supp}(\epsilon_1),\qquad |\Sigma|\le j.
\tag{1.2}
\]

The indices here match the rich-pencil note.  They correspond to the pair
called \((\epsilon_1,\epsilon_2)\) in the sparse Pad\'e--Hankel note.

For a finite slope \(\eta\), an eligible translated witness consists of an
agreement support \(S_\eta\subseteq D\), \(|S_\eta|\ge A\), and a translated
explaining codeword.  The support-wise noncontainment gate says that no pair
of codewords explains \(\epsilon_0\) and \(\epsilon_1\) simultaneously on
\(S_\eta\).

## 2. Zero-pencil slope image

Let \(Z_0(\epsilon_0,\epsilon_1)\) be the slope projection, existential over
all eligible supports and witnesses for this one fixed translation, of the
case in which the translated explaining codeword is zero:

\[
 (\epsilon_0+\eta\epsilon_1)|_{S_\eta}=0.
\tag{2.1}
\]

This definition is made before choosing a residual selector.  If a canonical
rich graph line later has code polynomials

\[
 P_L=Q_L=0,
\tag{2.2}
\]

then every selected slope on that line lies in \(Z_0\).

Define the fixed tangent image

\[
 \mathcal T(\epsilon_0,\epsilon_1)
 =\left\{-\frac{\epsilon_0(x)}{\epsilon_1(x)}:
 x\in\Sigma,\ \epsilon_1(x)\ne0\right\}.
\tag{2.3}
\]

### Theorem 2.1 (zero-pencil tangent projection)

For one fixed translation satisfying (1.2),

\[
 \boxed{
 Z_0(\epsilon_0,\epsilon_1)
 \subseteq \mathcal T(\epsilon_0,\epsilon_1),
 \qquad
 |Z_0(\epsilon_0,\epsilon_1)|
 \le |\mathcal T(\epsilon_0,\epsilon_1)|
 \le |\Sigma|\le j.}
\tag{2.4}
\]

For this fixed pair there is at most one zero-codeword word pencil in the
canonical graph-line atlas.

### Proof

Fix \(\eta\in Z_0(\epsilon_0,\epsilon_1)\) and one eligible witness support
\(S_\eta\).  If

\[
 \epsilon_0(x)=\epsilon_1(x)=0
 \qquad(x\in S_\eta),
\tag{2.5}
\]

then the zero codeword pair explains both translated received words on
\(S_\eta\).  That contradicts support-wise noncontainment.  Hence some
\(x\in S_\eta\) has

\[
 (\epsilon_0(x),\epsilon_1(x))\ne(0,0).
\tag{2.6}
\]

Equation (2.1) gives

\[
 \epsilon_0(x)+\eta\epsilon_1(x)=0.
\tag{2.7}
\]

If \(\epsilon_1(x)=0\), then (2.7) also gives \(\epsilon_0(x)=0\), contrary
to (2.6).  Therefore \(\epsilon_1(x)\ne0\), \(x\in\Sigma\), and

\[
 \eta=-\epsilon_0(x)/\epsilon_1(x)
 \in\mathcal T(\epsilon_0,\epsilon_1).
\]

This proves the inclusion.  The two cardinality bounds follow because the
map in (2.3) has domain contained in \(\Sigma\), and \(|\Sigma|\le j\).

Finally, (2.2) fixes the word pencil to

\[
 (a_L,b_L)=(\epsilon_0,\epsilon_1).
\]

The coordinates of a word in the chosen basis of \(K_0\) are unique, so its
canonical graph line is unique.  Thus at most one zero pencil occurs for the
fixed translation and selector. \(\square\)

## 3. Exact first-match consequence

The theorem is slope-projected before a residual selector is built.  The
correct local integration is:

```text
fix one source-bound SP3 translation (epsilon_0, epsilon_1)
form the existential zero-codeword-witness slope image Z_0
    over all eligible witnesses
route Z_0 to SPARSE_TANGENT_RANK9_CONDITIONAL_CAP
delete Z_0 at slope level
rebuild a complete selector on the retained slopes
if its intrinsic rank drops, invoke the already-declared lower-rank route
otherwise every contributing rich line has (P_L,Q_L) != (0,0)
```

It is not valid to delete only one supplied zero-pencil witness: first match
is existential over every eligible witness at a slope.  It is also not valid
to retain a previously computed rank-nine selector after slope deletion
without recomputing its rank.

The local tangent count is

\[
 |Z_0|\le j=981{,}104.
\tag{3.1}
\]

This is a slope count, not a direct bound on the determinant-weighted atlas
term \(\beta_L(J_L-20)\).  The zero-pencil slopes must actually be projected
out before the nonzero rich-line incidence sum is formed.

## 4. Exact executable control

The companion Python checker uses the toy row

\[
 F=\mathbb F_{11},\quad n=9,\quad k=1,\quad A=3,\quad j=6.
\]

One fixed sparse pair has support \(\Sigma=\{0,1,2,3,4,5\}\).  Three points
have tangent ratio one and three have tangent ratio two.  The checker
reconstructs both zero-codeword agreement supports, verifies full toy RS
noncontainment by exact linear algebra, derives the tangent image from the raw
pair, and obtains

\[
 Z_0=\{1,2\}\subseteq\mathcal T=\{1,2\},
 \qquad 2\le6=j.
\tag{4.1}
\]

This is an exact logical control for Theorem 2.1.  It is not a rank-nine or
KoalaBear census and supplies no deployed numerical evidence.

## 5. Owner and ledger status

The owner audit is:

- contained/noncontained failure is not payment; noncontainment is the
  hypothesis forcing tangency;
- periodic, quotient, planted-prefix, extension-valued, and coefficient-shadow
  predicates do not follow from \(P_L=Q_L=0\);
- base-valued slopes remain covered by the earlier base-slope owner, in its
  own first-match position;
- the correct new classification is the existing
  `SPARSE_TANGENT_RANK9_CONDITIONAL_CAP`, not `UNPAID_PRIMITIVE`;
- global source-family deduplication and selector rebuilding remain open.

Therefore

\[
 U_{\rm paid}=2{,}602{,}502{,}999,
 \qquad
 B_{\rm remaining}=274{,}980{,}725{,}508{,}892{,}088
\tag{5.1}
\]

remain unchanged.  The result does not determine \(U_Q\) or \(U_A\).

## 6. Audit status and nonclaims

- **PROVED:** Theorem 2.1 for one fixed source-bound sparse translation;
  uniqueness of its zero word pencil; exact toy logical replay.
- **UNPROVEN:** globally deduplicated tangent payment; a source-bound complete
  selector after deletion; the determinant-weighted nonzero plant-load bound;
  rank at least ten; \(U_Q\); \(U_A\); complete profile comparison; lower
  reserve.
- **Parameter dependence:** the projection proof is field-uniform.  Only the
  last cap in (2.4) uses the deployed row through \(|\Sigma|\le j\).
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** (4.1) is exact toy-scale control only.
- **Global verdict:** YELLOW.  The local projection lemma is GREEN; its global
  first-match payment is open.

This packet does not:

- infer tangency from \(W_L=\Sigma\) without noncontainment;
- replace existential slope projection by one chosen witness;
- convert the \(j\)-slope cap directly into an atlas-excess charge;
- assume rank nine survives slope deletion;
- promote the tangent cap to a paid global owner;
- move the deployed ledger or close the KoalaBear row;
- authorize rank at least ten, Lean, or stable-paper promotion.

## 7. Minimal next action

Bank the fixed-translation tangent projection in the global source-family
first-match compiler: bind one SP3 translation per source family, deduplicate
its image after earlier owners, and rebuild the residual selector.  Only then
form the nonzero rich-line load

\[
 \mathcal E_{20}^{\rm nz}
 =\sum_{L:(P_L,Q_L)\ne(0,0)}\beta_L(J_L-20)
\]

and attack its exact source-point allocation.  If global projection cannot be
made source-bound, retain the zero-pencil term explicitly; do not set it to
zero by convention.
