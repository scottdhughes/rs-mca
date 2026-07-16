# M1 KoalaBear branch-2 Hankel pivot adapter v1

**Status:** PROVED PAPER-D IMPLICIT FINITE-PIVOT ADAPTER / PROVED PIVOT
FAILURE EMPTY ON ACTUAL NONCONTAINED INCIDENCES / EXACT TWO-ROOT ROUTE CUT /
RANK POLICY, LEGACY BRIDGE, BRANCH 2, AND ROW OPEN.

This packet refines the source-interface audit at the KoalaBear MCA row

\[
A=1{,}116{,}048.
\]

The predecessor correctly left the combined branch
`rank_drop_or_pivot_failure` open.  Its machine label
`UNBOUND_SOURCE_SYMBOL`, however, is too broad for the finite-pivot half:
Paper D already supplies a canonical, field-native support-to-Hankel adapter.
What remains unbound is the deployed **rank-drop policy**, its owner, and the
identification of the field-native Hankel pivot with the older cyclotomic
symbol \(\operatorname{red}_p B_0(S)\).

This packet makes only that finite-pivot subgate executable.  It assigns no
charge, changes no ledger value, and does not claim that KoalaBear branch 2 is
complete.

## Statement audited

Let

\[
B=\mathbb F_p\subset K=\mathbb F_{p^2}\subset F=\mathbb F_{p^6},
\qquad D\subset B,
\]

and let \(C=\operatorname{RS}_F(D,k)\).  For an agreement support
\(S\subset D\) of size \(A\), put

\[
T=D\setminus S,\qquad
j=|T|=n-A,\qquad
r=n-k,\qquad
t=r-j=A-k.
\]

Write the co-support locator in ascending coefficient order:

\[
L_T(X)=\prod_{x\in T}(X-x)
      =\sum_{b=0}^{j}\ell_bX^b,
\qquad
\boldsymbol\ell_T=(\ell_0,\ldots,\ell_j)^t,
\qquad \ell_j=1.
\]

Use the full-domain dual weights

\[
\lambda_x=
\left(\prod_{\substack{y\in D\\y\ne x}}(x-y)\right)^{-1}
\]

and weighted syndrome

\[
\operatorname{Syn}(Y)_m
=\sum_{x\in D}\lambda_xx^mY(x),
\qquad 0\le m<r.
\]

For \(w\in F^r\), define the implicit quotient map

\[
\Phi_T^F(w)=H_{t,j}(w)\boldsymbol\ell_T,
\qquad
H_{t,j}(w)_{h,b}=w_{h+b}.
\]

Paper D proves

\[
\ker\Phi_T^F=W_T(F),
\]

where \(W_T(F)\) is the span of the parity-check columns indexed by \(T\).
Hence

\[
F^r/W_T(F)\overset{\sim}{\longrightarrow}F^t
\]

is a canonical support-wise quotient-coordinate map.

For a received pair \(f,g:D\to F\), put

\[
A_T=\Phi_T^F(\operatorname{Syn}_F(f)),
\qquad
B_T=\Phi_T^F(\operatorname{Syn}_F(g)).
\]

Then a finite slope \(\gamma\in F\) is explained on \(S\) and is
support-wise noncontained there if and only if

\[
A_T+\gamma B_T=0,
\qquad
B_T\ne0.
\]

This is the exact field-native branch-2 pivot interface.

## Canonical finite-pivot partition

On an actual finite support-wise noncontained incidence, define

\[
h_*(T)=\min\{h:0\le h<t,\ (B_T)_h\ne0\}.
\]

The chart with label \(h_*\) is cut out by

\[
(B_T)_h=0\quad(h<h_*),
\qquad
(B_T)_{h_*}\ne0,
\]

together with

\[
(A_T)_m(B_T)_{h_*}-(A_T)_{h_*}(B_T)_m=0
\quad(0\le m<t).
\]

Its unique finite root is

\[
\gamma=-\frac{(A_T)_{h_*}}{(B_T)_{h_*}}.
\]

The labels \(h=0,\ldots,t-1\) are disjoint and exhaustive on the actual
finite noncontained incidence locus.

The residual pivot-failure locus is empty **relative to that locus**.  Indeed,
if \(B_T=0\) and \(A_T+\gamma B_T=0\), then \(A_T=0\), so \(f\) and \(g\) are
both explained on \(S\).  That case is contained, not a noncontained
branch-2 witness.  If \(B_T=0\) and \(A_T\ne0\), the affine incidence is
inconsistent.

This does not make the predecessor branch-1 bucket a complete paid projector.
It only proves that after contained and inconsistent cases are removed, every
actual finite noncontained incidence has a canonical pivot.

## Exact scalar replay over \(K\)

Choose a \(K\)-basis

\[
(\beta_0,\beta_1,\beta_2)
\]

of \(F\), and write

\[
f=\sum_{i=0}^2\beta_if_i,
\qquad
g=\sum_{i=0}^2\beta_ig_i.
\]

Because \(D\), the dual weights, and the locator coefficients lie in
\(B\subset K\),

\[
A_T=\sum_{i=0}^2\beta_i a_{i,T},
\qquad
B_T=\sum_{i=0}^2\beta_i b_{i,T},
\]

where

\[
a_{i,T}=\Phi_T^K(\operatorname{Syn}_K(f_i)),
\qquad
b_{i,T}=\Phi_T^K(\operatorname{Syn}_K(g_i)).
\]

For \(\gamma\in K\),

\[
A_T+\gamma B_T=0
\quad\Longleftrightarrow\quad
a_{i,T}+\gamma b_{i,T}=0
\quad(0\le i\le2).
\]

Similarly,

\[
B_T\ne0
\quad\Longleftrightarrow\quad
(b_{0,T},b_{1,T},b_{2,T})\ne0.
\]

The ambient row \(h_*\) is basis-independent.  A scalar replay must therefore
scan \(h\) first and the basis coordinate \(i\) second.  After choosing

\[
c_*=\min\{i:(b_{i,T})_{h_*}\ne0\},
\]

one may recover

\[
\gamma=-\frac{(a_{c_*,T})_{h_*}}{(b_{c_*,T})_{h_*}}
\]

and impose the scalar cross equations

\[
(b_{c_*,T})_{h_*}(a_{i,T})_m
-(a_{c_*,T})_{h_*}(b_{i,T})_m=0
\]

for every \(i\in\{0,1,2\}\) and \(0\le m<t\), together with

\[
\gamma^{p^2}=\gamma,
\qquad
\gamma^p\ne\gamma
\]

for the proper quadratic parameter class.

A flattened component-major “first coordinate” is not canonical and can
select the wrong ambient row.

## Rank-policy guardrail

The ambient Hankel matrix has shape

\[
t\times(j+1).
\]

The three coordinate recurrences may be stacked into a

\[
3t\times(j+1)
\]

matrix only because actual locator vectors are \(K\)-valued.  This is an exact
zero-incidence replay on the common \(K\)-valued locator slice; it is not the
full restriction of scalars of the ambient matrix, which would have
\(3(j+1)\) columns.

Ambient and scalar-stack rank strata are therefore not interchangeable.  For
example, if \(\beta\in F\setminus K\), then

\[
\begin{bmatrix}1&\beta\end{bmatrix}
\]

has \(F\)-rank \(1\), while its coefficient stack over \(K\) has rank \(2\).
No `rank_drop` predicate or owner is inferred from the scalar replay.

## KoalaBear dimensions

At the printed row,

\[
\begin{aligned}
n&=2{,}097{,}152,\\
k=r&=1{,}048{,}576,\\
j&=n-A=981{,}104,\\
t&=A-k=67{,}472,\\
j+1&=981{,}105.
\end{aligned}
\]

Thus the canonical ambient matrix has shape

\[
67{,}472\times981{,}105
\]

and contains

\[
66{,}197{,}116{,}560
\]

entries.  It must remain implicit.  Its kernel dimension is at least

\[
981{,}105-67{,}472=913{,}633.
\]

The three-coordinate stack has \(202{,}416\) rows and kernel dimension at
least \(778{,}689\) on the common locator slice.  Kernel nonemptiness is not a
paid owner and does not define the missing rank policy.

The depth is \(t=67{,}472\), not the predecessor prefix quantity
\(w=t-1=67{,}471\).  A valid \(B_T\) may have its sole nonzero entry at
row \(t-1\).

## Exact controls

### Prime-field convention and non-first-pivot control

The Python verifier exhausts all \(15\) size-four supports and all \(17\)
slopes for

\[
\mathbb F_{17},\quad D=\{0,1,2,3,4,5\},\quad k=2.
\]

It checks direct interpolation against the weighted Hankel recurrence.  For

\[
g(x)=x^2,\qquad f(x)=-3x^2,
\]

and

\[
S=\{0,1,2,3\},\qquad T=\{4,5\},
\]

the exact data are

\[
\lambda=(16,5,7,10,12,1),
\quad
\boldsymbol\ell_T=(3,8,1),
\quad
A_T=(0,14),
\quad
B_T=(0,1).
\]

The canonical pivot is \(h_*=1\) and the recovered slope is \(3\).  This
control catches omitted dual weights, reversed locator coefficients,
agreement/co-support reversal, and a non-first deterministic pivot.

A second exact control modifies two degree-less-than-two codewords only on
\(T=\{4,5\}\).  On \(S=\{0,1,2,3\}\) it obtains

\[
A_T=B_T=(0,0)
\]

and directly checks simultaneous explanation and affine incidence.  Thus the
\(B_T=0\) contained branch is exercised positively as well as proved from the
Paper-D equivalence.

### Exact two-support / two-root route cut

The Sage replay works over

\[
\mathbb F_7\subset\mathbb F_{7^2}\subset\mathbb F_{7^6}
\]

with

\[
D=\{0,1,2,3,4,5\},\quad k=2,\quad j=t=2.
\]

It constructs one received pair with:

- global syndrome rank \(2\);
- full projective syndrome field \(\mathbb F_{7^6}\), certified by
  \(\operatorname{rank}[Y\mid Y^{(7^e)}]=3\) for \(e=1,2,3\);
- exactly two size-two co-support roots,
  \[
  T_1=\{0,1\}\mapsto\eta,\qquad
  T_2=\{2,4\}\mapsto\eta+1,
  \]
  with \(\eta,\eta+1\in\mathbb F_{7^2}\setminus\mathbb F_7\);
- least pivots \(0\) and \(1\), respectively;
- direct degree-less-than-two codeword explanations and support-wise
  noncontainment.

Therefore

```text
branch-1 incidence
+ field-native deterministic pivots
+ rank two
+ full projective syndrome field
```

does not imply a global one-root support union.

This is a route cut, not a deployed asymptotic lower bound: the construction
is not proved to survive the still-undefined rank policy or KoalaBear branches
3--5.

## Legacy cyclotomic bridge

The older first-match packet assumes a surviving row

\[
\operatorname{red}_p B_0(S)\ne0
\]

for a cyclotomic \(\mathcal O\)-valued affine row packet.  This packet uses the
Paper-D field-native symbol

\[
(B_T)_h.
\]

No theorem currently identifies these two objects, supplies the required
cyclotomic lift, or proves that their rank/pivot strata agree.  The legacy
bridge remains explicitly false/unproved in the certificate.

## Dependencies

- **PROVEN / IMPORTED:** the weighted support-locator syndrome recurrence.
- **PROVEN / IMPORTED:** the exact affine and projective support-image map.
- **PROVEN / IMPORTED:** exact \(F/K\) restriction of scalars on a base-field
  evaluation domain.
- **PROVEN HERE:** the executable implicit finite-pivot adapter and disjoint
  least-ambient-row partition.
- **PROVEN HERE:** pivot failure has zero actual finite noncontained witnesses.
- **PROVEN HERE:** the exact prime-field convention control and exact
  two-support/two-root route cut.
- **UNPROVEN:** the deployed rank-drop predicate and paid owner.
- **UNPROVEN:** the bridge to \(\operatorname{red}_p B_0(S)\).
- **UNPROVEN:** complete executable projectors for KoalaBear branches 3--5.
- **OPEN:** the field-full rank-two support union, \(U_2\), \(U_Q\), \(U_A\),
  and the final row inequality.

## Parameter dependence

The support-locator and scalar replay statements are uniform over finite field
towers \(B\subset K\subset F\) with \([F:K]=3\) and \(D\subset B\).  The
printed dimensions, entry counts, and ledger values are specific to the
KoalaBear row.  No asymptotic inference is made from either exact toy control.

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.

## Edge cases and notation

- \(S\) is the agreement support; the locator is built from
  \(T=D\setminus S\).
- Locator coefficients are ascending and include the monic top coefficient.
- The syndrome uses full-domain dual weights.
- The canonical pivot label is the ambient row \(h\), not a support ID or a
  flattened scalar coordinate.
- \(B_T=0\), \(A_T=0\) is contained; \(B_T=0\), \(A_T\ne0\) is inconsistent.
- Ambient cross equations alone do not prove that the recovered root lies in
  \(K\).
- A deterministic support-wise root does not by itself bound the deduplicated
  union across supports.
- `null` is not zero.

## Numerical evidence

The integer dimensions are exact.  The \(\mathbb F_{17}\) census and
\(\mathbb F_{7^6}\) construction are exhaustive finite controls, not sampled
evidence and not an asymptotic slope count.

## Verdict

**YELLOW — GREEN for the Paper-D finite-pivot adapter and its exact scalar
replay; RED/OPEN for the rank-drop half, legacy cyclotomic bridge, ledger
payment, and complete KoalaBear row.**

The packet is PR-worthy as a narrow source correction and executable route
cut.  It is not PR-worthy as a closure or ledger improvement.

## Remaining risks

The term `rank_drop` still lacks a row-specific matrix, threshold, first-match
semantics, and named owner.  Because the ambient and scalar-stack rank strata
can differ, that policy cannot be reconstructed by dimension counting.

The two-root control proves that a global one-root shortcut is false at the
current level of hypotheses.  It does not show that two roots survive the
eventual rank policy or later owner projectors.

## Minimal next action

Freeze one exact rank-drop predicate for the field-native Hankel pencil,
including:

1. the matrix whose rank is tested;
2. the threshold and chart order;
3. the named paid owner for every rank-drop component; and
4. whether the legacy cyclotomic row is proved equivalent or is formally
   retired from this branch.

Only after that statement is fixed should representative minors be factored.
Do not move to degree three, charge branch 2, or alter \(U_2,U_Q,U_A\).
