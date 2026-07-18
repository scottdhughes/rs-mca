# M1 KoalaBear rank-nine projective source-load disintegration v1

## Status

**PROVED exact post-tangent source-load disintegration, positive source-plant
floor, and projective rank dichotomy. PROVED local route cut:
the tangent slope payment and an unreduced degree bound do not pay the
remaining determinant load. YELLOW deployed source-fiber incidence theorem;
no ledger movement.**

This packet starts only after the global tangent owner has been charged and a
fresh residual selector has been built. It turns the determinant-weighted
nonzero atlas into an exact rational load on the fixed sparse source support.
The source fibers split into finite and projective-infinity charts and,
independently, coefficient rank one and two.

The split is not a payment. Deleting the one zero-codeword slope of a rank-one
finite polynomial pencil does not delete the positive weight carried by its
other rich slopes. Rank two gives a reduced exact-root bound, but no weighted
aggregate theorem is currently bound. The live deployed terminal is

~~~text
UNBOUND_POST_TANGENT_SOURCE_LOAD
~~~

If a future source-bound rebuilt selector exhibits an actual surviving
component with no owner, its fail-closed terminal is

~~~text
UNPAID_PRIMITIVE_PROJECTIVE_SOURCE_FIBER
~~~

The exact controls here are generic-local and do not themselves exhibit that
deployed component.

## 1. Frozen post-tangent row

The row is

\[
 p=2{,}130{,}706{,}433,\qquad F=\mathbf F_{p^6},\qquad
 n=2^{21},\qquad k=2^{20},
\]

\[
 A=1{,}116{,}048,\qquad R=n-k=1{,}048{,}576,
 \qquad j=n-A=981{,}104,\qquad t=A-k=67{,}472.
\tag{1.1}
\]

After the tangent owner, the exact ledger is

\[
 U_{\rm paid}=2{,}603{,}484{,}103,\qquad
 B_{\rm rem}=274{,}980{,}725{,}507{,}910{,}984.
\tag{1.2}
\]

The rebuilt one-cut target is

\[
 H_{18{,}014}\le17{,}907{,}571{,}352{,}523,
\]

with sufficient excess gate

\[
 E_{\max}'=
 5{,}284{,}472{,}953{,}556{,}748{,}839{,}425{,}672{,}939{,}211{,}329{,}356{,}986{,}005{,}299.
\tag{1.3}
\]

Fix the one SP3 translation used by the tangent owner,

\[
 (\epsilon_0,\epsilon_1),\qquad
 \Sigma=\operatorname{supp}(\epsilon_0)\cup
        \operatorname{supp}(\epsilon_1),\qquad |\Sigma|\le j.
\tag{1.4}
\]

All objects below must come from one complete selector rebuilt after tangent
deletion, one restriction map, and one kernel basis. No pre-deletion carrier,
rank, source distance, deficit histogram, graph line, or determinant mass may
be reused.

## 2. Nonzero rich lines and their plants

For every contributing graph line of the rebuilt low-deficit atlas, use

\[
 e_\eta=a_L+\eta b_L,\qquad
 Z_L=\{x\in V:a_L(x)=b_L(x)=0\},
\]

\[
 W_L=V\setminus Z_L,\qquad M_L=|W_L|=j+x_L,
\tag{2.1}
\]

and

\[
 w_L=\mathfrak b_L(J_L-20),\qquad
 \mathfrak b_L>0,\quad J_L\ge21.
\tag{2.2}
\]

Here \(\mathfrak b_L\) is the determinant-basis mass called \(\beta_L\) in
the predecessor; the new notation avoids collision with the graph direction.
The source coupling is pointwise:

\[
 a_L=\epsilon_0-\operatorname{ev}(P_L),\qquad
 b_L=\epsilon_1-\operatorname{ev}(Q_L),\qquad
 \deg P_L,\deg Q_L\le k-1.
\tag{2.3}
\]

The tangent packet removes the zero pencil, so

\[
 (P_L,Q_L)\ne(0,0).
\tag{2.4}
\]

Extend \(a_L,b_L\) by zero outside \(V\). Their full-domain common-zero set is
\(D\setminus W_L\), of size

\[
 |D\setminus W_L|=n-(j+x_L)=A-x_L.
\tag{2.5}
\]

Define the source plant and its size by

\[
 S_L=(D\setminus W_L)\cap\Sigma,\qquad s_L=|S_L|,
\tag{2.6}
\]

and the outside-source common roots by

\[
 C_L=(D\setminus W_L)\setminus\Sigma,\qquad c_L=|C_L|.
\tag{2.7}
\]

### Lemma 2.1 (positive plant)

Every residual nonzero rich line satisfies

\[
 \boxed{s_L=A-x_L-c_L\ge t-x_L+1\ge18{,}418.}
\tag{2.8}
\]

Moreover \(G_L=L_{C_L}\) divides \(\gcd(P_L,Q_L)\) and
\(\deg G_L=c_L\).

#### Proof

Every common-zero point outside \(\Sigma\) is a common domain root of
\(P_L,Q_L\). Since the domain points are distinct, \(G_L\) has degree exactly
\(c_L\). At least one of \(P_L,Q_L\) is nonzero, so \(c_L\le k-1\).
Subtracting \(c_L\) from (2.5) yields
\[
 s_L=A-x_L-c_L\ge A-x_L-(k-1)=t-x_L+1.
\]
The rich-line moving-zero inequality gives
\(x_L\le\lfloor j/20\rfloor=49{,}055\), whence
\[
 t-x_L+1\ge67{,}472-49{,}055+1=18{,}418.
\]
Thus every contributing line has a nonempty plant. \(\square\)

No lower bound such as \(x_L\ge1\) follows from support-wise nontriviality.
That condition is imposed on the selected witness support. A different
\(A\)-subset of the common-zero set may be simultaneously explained without
contradicting the selected witness. The packet uses only the imported upper
bound \(x_L\le49{,}055\).

## 3. Exact source-load disintegration

For \(h\in\Sigma\), define

\[
 \lambda_{L,h}=
 \begin{cases}
  w_L/s_L,&h\in S_L,\\
  0,&h\notin S_L,
 \end{cases}
\tag{3.1}
\]

and

\[
 \Lambda_h=\sum_L\lambda_{L,h}.
\tag{3.2}
\]

All loads lie in \(\mathbf Q_{\ge0}\). The division by \(s_L\) is
load-bearing: the unnormalized incidence sum would count line \(L\) exactly
\(s_L\) times.

### Theorem 3.1 (exact post-tangent source-load identity)

For every source-bound same-selector rebuilt nonzero atlas,

\[
 \boxed{
 \mathcal E_{20}^{\rm nz}
 =\sum_L w_L
 =\sum_{h\in\Sigma}\Lambda_h.}
\tag{3.3}
\]

#### Proof

The tangent owner removes every zero pencil, so the canonical atlas identity
is a sum over precisely the nonzero lines in (2.2). Lemma 2.1 gives \(s_L>0\).
Therefore
\[
 \sum_{h\in\Sigma}\Lambda_h
 =\sum_L\sum_{h\in S_L}\frac{w_L}{s_L}
 =\sum_Ls_L\frac{w_L}{s_L}
 =\sum_Lw_L.
\]
The predecessor atlas identity identifies the last sum with
\(\mathcal E_{20}^{\rm nz}\). \(\square\)

A pointwise sufficient target is now explicit:

\[
 \Lambda_h\le\frac{E_{\max}'}j\quad(h\in\Sigma)
 \quad\Longrightarrow\quad
 \mathcal E_{20}^{\rm nz}\le E_{\max}'.
\tag{3.4}
\]

Exact division gives

\[
 E_{\max}'=
 981{,}104\cdot
 5{,}386{,}251{,}563{,}092{,}953{,}284{,}693{,}236{,}332{,}958{,}921{,}130{,}671
 +164{,}515.
\tag{3.5}
\]

The implication in (3.4) is proved here. No estimate establishing its
pointwise antecedent is proved.

## 4. Finite and infinity source fibers

For \(h\in\Sigma\), define

\[
 \vartheta(h)=
 \begin{cases}
  -\epsilon_0(h)/\epsilon_1(h),&\epsilon_1(h)\ne0,\\
  \infty,&\epsilon_1(h)=0.
 \end{cases}
\tag{4.1}
\]

Write \(\Sigma_\theta=\{h:\vartheta(h)=\theta\}\), including
\(\Sigma_\infty\). If \(h\in S_L\), then

\[
 P_L(h)=\epsilon_0(h),\qquad Q_L(h)=\epsilon_1(h).
\tag{4.2}
\]

Consequently, on a finite fiber,

\[
 P_L(h)+\theta Q_L(h)=0,
 \qquad h\in S_L\cap\Sigma_\theta,
\tag{4.3}
\]

while at infinity

\[
 Q_L(h)=0,\qquad P_L(h)\ne0,
 \qquad h\in S_L\cap\Sigma_\infty.
\tag{4.4}
\]

Thus

\[
 \mathcal E_{20}^{\rm nz}
 =\sum_{\theta\in F\cup\{\infty\}}
   \sum_{h\in\Sigma_\theta}\Lambda_h.
\tag{4.5}
\]

No finite \(\theta\) with \(\Sigma_\theta\ne\varnothing\) lies in the
residual slope set: if it was incoming, the tangent owner assigned it; if it
was not incoming, it incurred no tangent-stage charge and may instead have
been earlier-owned or not bad. In either case, absence of that field element
does not remove the source fiber or the weights of other slopes on a rich line.

## 5. Polynomial-pair rank dichotomy

Because of (2.4), the coefficient matrix with rows \(P_L,Q_L\) has rank one
or two.

### Lemma 5.1 (rank one)

If the rank is one, write

\[
 (P_L,Q_L)=(rH,sH),\qquad H\ne0,\quad[r:s]\in\mathbf P^1(F).
\tag{5.1}
\]

Then every \(h\in S_L\) lies in the single source fiber
\([-\epsilon_0(h):\epsilon_1(h)]=[-r:s]\).

If \(s\ne0\), the unique finite slope

\[
 \eta_0=-r/s
\tag{5.2}
\]

makes \(P_L+\eta_0Q_L=0\). It equals \(\vartheta(h)\) for every planted
point and lies in the fixed tangent image, hence is absent from the residual
slope set. It is tangent-owned only if it belonged to the incoming cell.
Nevertheless
\(w_L=\mathfrak b_L(J_L-20)>0\) is formed from the remaining selected slopes;
deleting \(\eta_0\) does not pay that weight.

If \(s=0\), then \(Q_L=0\), every planted point is in \(\Sigma_\infty\), and
there is no finite zero-codeword slope.

#### Proof

For \(h\in S_L\), (4.2) is nonzero because \(h\in\Sigma\). Equation (5.1)
therefore has \(H(h)\ne0\), and projectivization gives the common fiber. The
remaining claims follow from \(P_L+\eta Q_L=(r+\eta s)H\). \(\square\)

### Lemma 5.2 (rank two)

Factor the forced outside roots:

\[
 P_L=G_L\widetilde P_L,\qquad Q_L=G_L\widetilde Q_L.
\tag{5.3}
\]

The reduced pair still has rank two. For finite \(\theta\),
\(\widetilde P_L+\theta\widetilde Q_L\) is nonzero; at infinity,
\(\widetilde Q_L\ne0\). Their degrees are at most \(k-1-c_L\). Hence

\[
 \boxed{
 |S_L\cap\Sigma_\theta|
 \le d_L^{\rm proj}:=k-1-c_L=s_L+x_L-t-1}
 \quad(\theta\in F\cup\{\infty\}).
\tag{5.4}
\]

In particular, \(d_L^{\rm proj}=0\) excludes rank two, while
\(d_L^{\rm proj}=1\) makes the projective source label injective on the plant
of a rank-two line. The unreduced bound \(k-1\) would be vacuous because

\[
 k-1=1{,}048{,}575>j=981{,}104.
\tag{5.5}
\]

Thus removing the forced common-root factor is essential.

#### Proof

Multiplication by nonzero \(G_L\) preserves coefficient rank. An identically
zero reduced combination would make the two rows dependent. Since all roots
of \(G_L\) lie outside \(\Sigma\), division loses no plant point. Apply the
ordinary root bound to (4.3)--(4.4), then use
\(c_L=A-x_L-s_L\) to obtain (5.4). \(\square\)

The exact split has four logical cells: finite/rank one, infinity/rank one,
finite/rank two, and infinity/rank two. None is paid by the current contracts.

## 6. Same-selector incidence interlock

Let \(r_1,\ldots,r_8\) be the chosen basis of \(K_0\), and write the graph
line as \(z_\eta=\alpha_L+\eta\boldsymbol\beta_L\). Put

\[
 g_h=(r_1(h),\ldots,r_8(h)).
\]

At a plant point,

\[
 g_h\alpha_L=-u(h),\qquad
 g_h\boldsymbol\beta_L=-v(h).
\tag{6.1}
\]

For finite \(\theta=\vartheta(h)\), projective incidence alone is

\[
 u(h)+\theta v(h)
 +g_h(\alpha_L+\theta\boldsymbol\beta_L)=0,
\tag{6.2}
\]

while exact source incidence also imposes the second affine equation in
(6.1). In the ambient line-parameter space these two equations have rank two
when \(g_h\ne0\); on an actual algebraic component their restrictions can
have rank two, one, or zero. A restricted rank drop needs an owner or an exact
count. It cannot be declared paid from the ambient calculation.

If \(h\in\Sigma\setminus V\), the zero extensions give
\(g_h=u(h)=v(h)=0\). Such a source point is a universal plant point for every
graph line and is a genuine rank-zero concentration edge case. A point in
\(D\setminus(V\cup\Sigma)\) is instead an outside-source common zero and
belongs to \(C_L\), not \(S_L\).

## 7. Exact controls and route cut

The Python checker reconstructs four deterministic controls over
\(\mathbf F_{11}\). The two rank-one controls use

\[
 (n,k,A,j,t)=(9,2,3,6,1),\qquad x_L=1,\qquad
 \mathfrak b_L=1,\quad J_L=3,\quad C=2,\quad w_L=1.
\]

The two rank-two controls instead use

\[
 (n,k,A,j,t)=(10,3,4,6,1),\qquad x_L=1,qquad
 c_L=1,\quad \mathfrak b_L=3,\quad J_L=3,\quad C=2,\quad w_L=3.
\]

The finite-only rank-two control has \(P=X(X-2)\), \(Q=X-2\). The mixed-chart
rank-two control has \(P=X-2\), \(Q=(X-2)(X-1)\). Both exact replays genuinely
divide the forced outside-source factor \(G=X-2\). The resulting reduced cap
is \(d_L^{\rm proj}=1\), whereas the unreduced degree is two.

For every selected slope it recomputes the error support and verifies exact
support-wise RS noncontainment in that fixture. The fixture value \(x_L=1\)
is not promoted to a general lower bound. The checker then reconstructs the common-zero set,
source polynomials, tangent image, plant, coefficient rank, rational loads,
and projective fibers.

The cases are:

1. rank one finite: zero-codeword slope \(10\) is in the tangent image and
   absent from the selected residual slopes, while those slopes still carry
   load one;
2. rank one infinity: \(Q_L=0\), the plant lies at infinity, and the line
   still carries load one;
3. rank two: after removing one forced outside-source common root,
   \(d_L^{\rm proj}=1\), and the plant splits injectively between finite
   fibers \(0\) and \(10\), each receiving load \(3/2\).
4. rank two with infinity: the same forced-factor and injective-cap checks
   hold, and the plant splits between finite fiber \(1\) and infinity, each
   receiving load \(3/2\).

The independent Sage companion reconstructs the same controls directly.
They are exact generic-local implication tests, not affine-rank-nine or
deployed-field selectors.

The controls prove a narrow route cut: source-load disintegration, tangent
deletion, support-wise noncontainment, source coupling, and the rank split do
not by themselves imply zero load or an owner. They do not prove that an
actual deployed primitive component exists.

## 8. Current terminal and next gate

No fresh deployed post-tangent selector/source inventory or row-uniform paying
theorem is currently bound. Therefore the live terminal remains

~~~text
UNBOUND_POST_TANGENT_SOURCE_LOAD
~~~

The next theorem must do at least one of the following on rebuilt same-selector
records:

- prove the pointwise bound (3.4), possibly after a disjoint rank/fiber split;
- route every heavy rank-one fiber without charging its tangent slope twice;
- use \(d_L^{\rm proj}=s_L+x_L-t-1\), then strengthen its larger values with
  the eight outlier directions, regular locator equations, or another owner;
- exhibit an actual compatible component and emit the primitive terminal with
  its equations.

No ledger value moves, and \(U_Q,U_A\) remain null.

## 9. Audit status and nonclaims

- **PROVED:** Lemma 2.1, Theorem 3.1, the projective partition, reduced
  rank-two root bound, and rank dichotomy.
- **EXACT CONTROL:** four \(\mathbf F_{11}\) generic-local noncontainment and
  source-coupling fixtures.
- **IMPORTED/REPLAYED:** canonical atlas identity, same-selector manifest,
  zero-pencil projection, tangent owner, and selector restart.
- **UNPROVEN:** deployed rebuilt source inventory; paying projective-fiber
  bound; complete rank-nine payment; \(U_Q\); \(U_A\); complete profile and
  lower-reserve comparisons.
- **Parameter dependence:** the algebra is field-uniform under the printed
  same-selector hypotheses. The \(18{,}418\) floor and pointwise target use the
  exact KoalaBear row.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** exact toy-scale logical controls only.
- **Global verdict:** YELLOW. The reduction is GREEN; deployed payment and row
  closure remain open.

This packet does not:

- infer \(x_L\ge1\) from support-wise nontriviality on another support;
- use raw, unnormalized source incidences as the identity;
- union different SP3 translations or mix selectors;
- treat infinity as empty;
- charge a rank-one line to its already-paid tangent slope;
- discard \(G_L\) and use the vacuous unreduced degree bound;
- turn toy controls into deployed primitive components;
- move the ledger or determine \(U_Q,U_A\);
- begin rank at least ten, Lean, or stable-paper promotion.

## 10. Minimal next action

On an actual rebuilt selector, compute the four finite/infinity and rank-one/
rank-two load cells. Apply the exact \(d_L^{\rm proj}\) cut first. If a heavy
cell survives all executable owners, freeze its support, regular-chart, and
polynomial equations and emit the primitive terminal; do not infer it from
these toy controls.
