# One-deeper locator prefix to anti-host MCA line

**Status:** PROVED / ROUTE CUT.

## Purpose

The canonical reduced rational-host compiler is exact after a received
direction already has a rational-host presentation. It does not show that all
slope-rich section-nonpositive lines have one. This note gives an explicit
source-valid family of received lines that simultaneously has:

1. many distinct exact-agreement MCA slopes;
2. support-wise nontriviality and occupancy one;
3. no rational-host presentation throughout the canonical degree range.

The result is a lower sharpness theorem for the non-host remainder. It does
not prove that these slopes survive every earlier first-match owner.

## Finite compiler

Let \(B\) be a finite field, let \(D\subseteq B\) have size \(n\), and fix

\[
1\le k<m<n,\qquad s=m-k\ge 1.
\]

For an \(m\)-subset \(S\subseteq D\), write

\[
Q_S(X)=\prod_{x\in S}(X-x)
      =X^m+c_1(S)X^{m-1}+\cdots+c_m(S)
\]

and define the depth-\(s\) locator-prefix map

\[
\Phi_s(S)=(c_1(S),\ldots,c_s(S)).
\]

Fix \(z\in B^s\) and a family
\(\mathcal G\subseteq\Phi_s^{-1}(z)\) of size \(N\).

### Theorem (one-deeper prefix-to-anti-host line)

Let \(F/B\) be a finite extension satisfying

\[
|F|>
\max\left\{
n+(k-1)\binom N2,\;
1+(n-m)N
\right\}.                                                   \tag{1}
\]

For \(C=RS_F(D,k)\), there is a received pair
\(r=(r_0,r_1)\) and an injection

\[
S\longmapsto(\gamma_S,S,h_S)
\]

from \(\mathcal G\) into the exact-\(m\) support-wise MCA witness
incidence such that:

1. the \(\gamma_S\) are \(N\) distinct finite slopes;
2. the agreement set of \(r_0+\gamma_S r_1\) with \(h_S\) is exactly \(S\);
3. \(r_1\) has no degree-\(<k\) explanation on \(S\), so the witness is
   support-wise nontrivial;
4. every displayed explanation pair has retained-support occupancy one.

For every nonempty challenge set \(\Gamma\subseteq F\), translating the base
point of the line gives

\[
B^{\mathrm{MCA}}_{C,\Gamma}(m)
\ge
\left\lceil\frac{N|\Gamma|}{|F|}\right\rceil.                \tag{2}
\]

For the full-field challenge, the lower bound is \(N\).

Moreover, the direction \(r_1\) has no presentation on \(D\) of the form

\[
r_1(x)=c(x)-\frac{T(x)}{L(x)}                               \tag{3}
\]

with

\[
\deg c<k,\quad
1\le d:=\deg L\le n-m-2,\quad
\deg T<d,\quad
L(x)\ne0\quad(x\in D).                                      \tag{4}
\]

No monicity, coprimality, or reducedness assumption is needed for this
exclusion.

## Construction and proof

Put

\[
U_z(X)=X^m+\sum_{i=1}^{s}z_iX^{m-i}
\]

and, for \(S\in\mathcal G\), define

\[
P_S(X)=U_z(X)-Q_S(X).
\]

The leading coefficient and the next \(s=m-k\) coefficients cancel, so

\[
\deg P_S\le m-s-1=k-1.                                      \tag{5}
\]

For distinct \(S,T\), the polynomial
\(P_S-P_T=Q_T-Q_S\) is nonzero and has degree at most \(k-1\).
The first term in (1) therefore permits a point

\[
\alpha\in F\setminus D
\]

that is not a root of any \(P_S-P_T\). Set

\[
\gamma_S=P_S(\alpha).
\]

These slopes are pairwise distinct.

The second term in (1) permits a nonzero \(\theta\in F\) such that

\[
\frac1{x-\alpha}+\theta\gamma_S\ne0
\qquad
(S\in\mathcal G,\;x\in D\setminus S).                       \tag{6}
\]

Define on \(D\)

\[
r_0(x)=\frac{U_z(x)}{x-\alpha},
\qquad
r_1(x)=\theta U_z(x)-\frac1{x-\alpha},                      \tag{7}
\]

and define

\[
h_S(X)=
\frac{P_S(X)-P_S(\alpha)}{X-\alpha}
+\theta\gamma_SP_S(X).                                      \tag{8}
\]

The quotient in (8) is a polynomial of degree at most \(k-2\); the second
term has degree at most \(k-1\). Thus \(\deg h_S<k\). Direct substitution
gives the exact identity

\[
r_0+\gamma_Sr_1-h_S
=Q_S(X)\left(\frac1{X-\alpha}+\theta\gamma_S\right).         \tag{9}
\]

The first factor vanishes on \(D\) exactly at \(S\), and (6) keeps the
second factor nonzero on \(D\setminus S\). This proves exact agreement and
occupancy one.

If a polynomial \(G\), \(\deg G<k\), explained \(r_1\) on \(S\), then

\[
(X-\alpha)(G-\theta P_S)+1
\]

would have degree at most \(k\) and at least \(m\ge k+1\) roots. It would be
zero, but its value at \(\alpha\) is 1. This proves support-wise
nontriviality.

For the anti-host assertion, suppose (3)-(4) held and put

\[
A=cL-T,\qquad \deg A\le k+d-1.
\]

Equality on \(D\) implies that

\[
H(X)=
L(X)\bigl(\theta(X-\alpha)U_z(X)-1\bigr)
-(X-\alpha)A(X)
\]

vanishes on all \(n\) domain points. Its first summand has degree exactly
\(m+d+1\), while the second has degree at most \(k+d\). Hence \(H\ne0\) and

\[
\deg H=m+d+1\le n-1,
\]

contradicting its \(n\) distinct roots.

Finally, translating \(r_0\) to \(r_0+\delta r_1\) translates the slope set
to \(Z-\delta\). The identity

\[
\sum_{\delta\in F}|(Z-\delta)\cap\Gamma|=N|\Gamma|
\]

proves (2).

## Section-nonpositive consequence

At agreement \(a=m\), define

\[
J=m^2-n(k-1).
\]

Since \(s=m-k\),

\[
J=n(s+1)-m(n-m).
\]

If \(J\le0\), then

\[
s+1\le\frac{m(n-m)}n<n-m,
\]

and integrality gives \(s\le n-m-2\). Therefore the anti-host exclusion
contains every degree

\[
1\le d\le s=a-k
\]

used by the canonical reduced rational-host compiler.

## Realized-image scale

For the full support slice
\(\Omega=\binom Dm\), let

\[
L_s=|\Phi_s(\Omega)|.
\]

A largest prefix fiber has

\[
N\ge\frac{|\Omega|}{L_s}
 \ge \binom nm |B|^{-s}.                                   \tag{10}
\]

Thus the construction reaches the actual depth-\(s\) average fiber scale,
not merely a polynomial lower bound.

As a concrete asymptotic family, let

\[
B_r=\mathbb F_{2^r},\quad
D_r=B_r^\times,\quad
n_r=2^r-1,\quad
m_r=2^{r-1}-1,
\]

fix \(0<\eta<\log 2\), and put

\[
s_r=\left\lfloor\frac{\eta n_r}{\log|B_r|}\right\rfloor,
\qquad
k_r=m_r-s_r.
\]

For all sufficiently large \(r\), (1) can be met by an extension
\(F_r/B_r\) with \(\log|F_r|=O(n_r)\). A largest prefix fiber gives

\[
N_r\ge
\binom{n_r}{m_r}|B_r|^{-s_r}
\ge
\frac{\exp((\log2-\eta)n_r)}{n_r+1}.                        \tag{11}
\]

Also \(J_r<0\) eventually. Since

\[
\gcd(m_r,n_r)=1,
\]

every support in this family has trivial multiplicative stabilizer. If
\(\overline N_{\mathrm{id},r}\) denotes the identity-profile average with
depth \(s_r-1\), then

\[
N_r\ge |B_r|^{-1}\overline N_{\mathrm{id},r}.               \tag{12}
\]

Because \(\log|B_r|=o(n_r)\), this is the same exponential scale as the
identity profile.

Consequently, no field-independent polynomial bound, and no absolute
\(\exp(o(n))\) bound, can cover the entire \(J\le0\) non-host complement.
Any valid upper theorem must pay that complement at its realized image scale
or route these witnesses to named earlier owners.

## Verification

The script
experimental/scripts/verify_one_deeper_prefix_anti_host_compiler.py gives a
deterministic exact instance over \(\mathbb F_{101}\) with

~~~text
n=8, k=3, m=4, s=1, J=0, N=8.
~~~

It reconstructs the largest prefix fiber, chooses the separating pole and
twist, verifies all exact agreement sets and support-wise nontriviality,
checks challenge-set translation averaging, and exhausts every admissible
monic rational denominator of degree 1 or 2. The latter is the complete
anti-host range \(d\le n-m-2\) in this instance.

## Relation to current work

The integrated aperiodic prefix obstruction has many exact slopes, but its
direction is itself a degree-one rational host. Pending PR #730 proves that
rational-host extraction fails generically; it does not construct a non-host
line carrying many exact MCA slopes. This theorem supplies that separate
bridge. It should be cited as a slope-rich anti-host compiler, not as
ownership of the generic non-host stratum.

## Nonclaims

This theorem does not prove that its slopes survive quotient, Chebyshev,
planted, remainder, signed-minority, rational-host, or other earlier
first-match owners. It does not place the line in the final primitive
residual, refute the correctly normalized profile-envelope upper statement,
or exclude a broader owner that first subtracts the line-determined prefix
word. It does not rule out punctured or profile-local hosts, prove MI/MA,
Sidon payment, residual-ray closure, a complete atlas, a target comparison,
an unsafe reserve, a deployed finite crossing, Grand MCA, or Grand List.

The official score remains 0/2. The exact next target is a
section-nonpositive primitive-residual payment that either routes every slope
of this construction to an earlier named owner or pays the retained non-host
cell at its realized depth-\(s\) image scale.
