# Common-core shortening and the near-k cover obstruction

**Status:** PROVED route cut, with a pre-atlas RS realization.

This note closes one proposed escape from the large-kernel balanced-core wall.
It does not prove that a positive-rate high-kernel residual survives the full
first-match atlas.  It proves that, if such an actual-slope residual survives,
subexponentially many cells cannot pay it merely by regaining almost all of the
code dimension as a common agreement core.

## 1. Setup

Let

\[
 C=\operatorname{RS}_{\mathbb F}(D,k),\qquad |D|=n,\qquad R=n-k,
\]

and fix exact agreement

\[
 a=k+w+1,\qquad 0\leq w\leq R-1,
 \qquad t=n-a=R-w-1.
\]

For a nonempty family \(\mathcal F\) of exact-\(a\) agreement supports, put

\[
 C_{\mathcal F}=\bigcap_{S\in\mathcal F}S,
 \quad c=|C_{\mathcal F}|,
 \quad U=\bigcup_{S\in\mathcal F}(D\setminus S)=D\setminus C_{\mathcal F}.
\]

The residual kernel parameter is

\[
 \kappa(\mathcal F)=\dim\ker H_U=\max\{0,k-c\}.
\]

All slope sets below are actual finite slopes of the RS syndrome line, after
the noncommonness condition and the stated first-match deletions.  They are not
formal locator parameters.

## 2. Exact theorem

### Theorem 2.1 (mass, shortening, and cover obstruction)

The following statements hold.

1. **Mass-kernel inequality.**

   \[
   |\mathcal F|
      \leq {n-c\choose t}
      \leq {R+\kappa(\mathcal F)\choose t}.
      \tag{2.1}
   \]

   If one witness support is selected for every slope in an actual noncommon
   slope set \(Z\), then the selected supports are distinct and

   \[
   |Z|\leq {R+\kappa(\mathcal F)\choose t}.
   \tag{2.2}
   \]

2. **Slope-preserving common-core shortening.**  Fix \(0\leq s\leq k\), and
   suppose every support in one cell contains a fixed set

   \[
   K\subseteq D,\qquad |K|=k-s.
   \]

   Write \(Q_K(X)=\prod_{x\in K}(X-x)\).  For \(j=0,1\), let \(g_j\) be the
   polynomial of degree less than \(|K|\) interpolating \(r_j\) on \(K\), and
   define on \(D'=D\setminus K\)

   \[
   \widetilde r_j(x)=\frac{r_j(x)-g_j(x)}{Q_K(x)}.
   \tag{2.3}
   \]

   The map

   \[
   (\gamma,S,h)\longmapsto
   \left(\gamma,S\setminus K,
   \frac{h-g_0-\gamma g_1}{Q_K}\right)
   \tag{2.4}
   \]

   is a bijection from exact-\(a\), noncommon witnesses containing \(K\) to
   exact-\((w+s+1)\), noncommon witnesses for

   \[
   \operatorname{RS}_{\mathbb F}(D',s),
   \qquad |D'|=R+s,
   \qquad R'=R.
   \tag{2.5}
   \]

   It preserves the slope, the error support, and the depth-\(w\) locator
   prefix.  If the cell's full common core is \(C_i\supseteq K\), its shortened
   error union has

   \[
   \kappa_i'=\max\{0,s-|C_i\setminus K|\}\leq s.
   \tag{2.6}
   \]

3. **Exact cell capacities.**  A cell with a fixed common core of size at
   least \(k-s\) has at most

   \[
   B_{\rm supp}(R,w,s)={R+s\choose w+s+1}
   \tag{2.7}
   \]

   exact supports, and its actual first-match slope set has size at most

   \[
   B_{\rm cell}(R,w,s)=
   \min\left\{
     {R+s\choose w+s+1},
     {R+s\choose s+1}
   \right\}.
   \tag{2.8}
   \]

4. **First-match cover lower bound.**  Let \(Z_{\rm res}\) be partitioned into
   actual first-match slope sets \(Z_1^\circ,\ldots,Z_P^\circ\), and suppose
   each nonempty cell has a fixed common core of size at least \(k-s\).  Then

   \[
   P\geq
   \left\lceil\frac{|Z_{\rm res}|}{B_{\rm cell}(R,w,s)}\right\rceil.
   \tag{2.9}
   \]

   A partition of a specified support family \(\mathcal F_{\rm res}\) obeys

   \[
   P\geq
   \left\lceil\frac{|\mathcal F_{\rm res}|}
   {B_{\rm supp}(R,w,s)}\right\rceil.
   \tag{2.10}
   \]

   Here \(P\) counts nonempty realized profiles, including every realized core
   parameter.  It is not the number of abstract profile-type names.

5. **Asymptotic consequence.**  If

   \[
   s_n=o(n/\log n),\qquad w_n=O(n/\log n),
   \tag{2.11}
   \]

   then \(B_{\rm supp}=e^{o(n)}\) and \(B_{\rm cell}=e^{o(n)}\).  Consequently,
   for every fixed \(\beta>0\),

   \[
   |Z_{{\rm res},n}|\geq \exp(\beta n-o(n))
   \quad\Longrightarrow\quad
   P_n\geq \exp(\beta n-o(n)).
   \tag{2.12}
   \]

Thus an \(e^{o(n)}\) decomposition into cells that each regain a
\(k-o(n/\log n)\) common core cannot pay a positive-rate actual-slope
residual.

## 3. Proof

For (2.1), the error-support map \(S\mapsto D\setminus S\) injects
\(\mathcal F\) into the \(t\)-subsets of \(D\setminus C_{\mathcal F}\).
The MDS rank identity gives

\[
 \kappa(\mathcal F)=\max\{0,n-c-R\}=\max\{0,k-c\}.
\]

If \(c\leq k\), then \(n-c=R+\kappa\).  If \(c>k\), then
\(n-c<R=R+\kappa\), and monotonicity in the upper binomial argument proves
the second inequality.  A fixed exact support cannot carry two distinct
noncommon slopes: subtracting two explanations on that support explains
\(r_1\), and then \(r_0\), on the same support.  This proves (2.2).

For (2.4), \(h-g_0-\gamma g_1\) vanishes on \(K\), hence is divisible by
\(Q_K\), and its quotient has degree less than \(s\).  For every
\(x\in D'\),

\[
 \widetilde r_0(x)+\gamma\widetilde r_1(x)-\widetilde h(x)
 =\frac{r_0(x)+\gamma r_1(x)-h(x)}{Q_K(x)}.
 \tag{3.1}
\]

This proves exact agreement and preserves the error support.  The inverse is

\[
 \widetilde h\longmapsto g_0+\gamma g_1+Q_K\widetilde h.
\]

The same division applied separately to putative explanations of \(r_0\) and
\(r_1\) proves preservation of noncommonness.  Locator factorization gives

\[
 Q_S=Q_KQ_{S\setminus K},
 \qquad
 \deg(Q_S-Q_T)\leq k
 \Longleftrightarrow
 \deg(Q_{S\setminus K}-Q_{T\setminus K})\leq s,
 \tag{3.2}
\]

which is exactly preservation of the first \(w\) nonleading locator
coefficients.  Equations (2.5) and (2.6) now follow from the MDS identity.

After shortening, supports have size \(w+s+1\) in a domain of size \(R+s\),
proving (2.7).  For the slope bound, let \(U_i\) be the union of shortened
error supports.  If \(\kappa_i'\geq1\), the proved field-independent
higher-dimensional transverse-secant theorem gives

\[
 |Z_i^\circ|\leq {R+\kappa_i'\choose \kappa_i'+1}
 \leq {R+s\choose s+1}.
\]

If \(\kappa_i'=0\), the bounded residual-kernel ray compiler gives
\(|Z_i^\circ|\leq t+1\leq R\leq {R+s\choose s+1}\).  Combining this with
support injection proves (2.8).

First-match deletion makes the sets \(Z_i^\circ\) disjoint, so

\[
 |Z_{\rm res}|=\sum_i|Z_i^\circ|\leq P B_{\rm cell}.
\]

This proves (2.9), and the support version proves (2.10).

Finally, use \({N\choose r}\leq(eN/r)^r\), with
\(r=w+s+1\) for the support term and \(r=s+1\) for the secant term.  Under
(2.11), both logarithms are \(o(n)\).  Substitution in (2.9) proves (2.12).

## 4. Pre-atlas RS realization

The existing theorem `thm:aperiodic-ray-obstruction` supplies smooth
multiplicative rows with a complete depth-\(w_n\) prefix fiber
\(\mathcal F_n\), an actual received line, and an exact support-slope-witness
bijection satisfying

\[
 |\mathcal F_n|=|Z_n|
 \geq \exp((\log 2-\eta)n-o(n)).
 \tag{4.1}
\]

Let \(C_n=\bigcap_{S\in\mathcal F_n}S\) and
\(k_n'=k_n-|C_n|\).  A nonsingleton prefix fiber cannot have
\(|C_n|>k_n\): otherwise \(Q_S-Q_T\) would be divisible by a polynomial of
degree greater than \(k_n\), contradicting equality of the depth-\(w_n\)
prefix.  If \(k_n'=o(n)\), (2.1), taken in the complementary binomial
parameter, would give \(|\mathcal F_n|=e^{o(n)}\), contradicting (4.1).
Hence \(k_n'=\Theta(n)\).

Shortening by the full core \(C_n\) preserves all slopes and witnesses and
leaves empty common core, so the residual kernel is \(k_n'=\Theta(n)\).  If
the shortened locators lay in one projective pencil, the proved split-pencil
moving-root bound, with root gcd one, would give at most \(n\) parameters.
This contradicts (4.1).  The shortened family is therefore genuinely
higher-dimensional before the full first-match atlas is imposed.  Applying
(2.9) shows that every uniform \(s_n=o(n/\log n)\) near-core refinement of
this pre-atlas line requires exponentially many realized cells.

## 5. Exact remaining wall and nonclaims

This theorem eliminates only the following proposed A2 mechanism:

> cover a positive-rate high-kernel residual with \(e^{o(n)}\) realized cells,
> each regaining a common core of size \(k-o(n/\log n)\), and sum the
> subexponential transverse-secant payments.

It does **not** prove that the aperiodic line retains a positive-rate slope set
after quotient, planted, tangent, extension, rank, saturation, curve, and
pencil first-match removals.  It therefore does not prove A2 false, does not
prove A4, and does not close the asymptotic frontier.

The exact next target is a survivor-or-payment theorem for one named
high-kernel residual: either prove that the earlier atlas cells reduce its
actual slope projection to \(e^{o(n)}\), or exhibit a positive-rate primitive
survivor and pay it by an image-scale MI+MA or direct signed-Sidon theorem.

There is no finite deployed-row movement.  No CAP25 or M31 residual currently
supplies the realized balanced-core slope census required by (2.9), and no
adjacent inequality \(U(a_0+1)\leq B^*<L(a_0)\) is proved here.
