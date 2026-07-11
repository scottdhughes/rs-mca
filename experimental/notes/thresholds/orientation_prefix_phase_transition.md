# Antipodal orientation prefixes have a critical depth scale

- **Status:** PROVED-SPECIAL / COARSE PHASE BRACKET / ROUTE MAP.
- **Track:** asymptotic hard input A / unsaturated orientation projection.
- **Verifier:**
  `python3 experimental/scripts/verify_orientation_prefix_phase_transition.py`.
- **Promotion gate:** experimental only. No statement in this packet is
  promoted to the frontiers TeX.

## Exact theorem

For \(r\ge2\), put

\[
q=3^r,\qquad B=\mathbb F_q,\qquad N=q-1=2a,\qquad D=B^\times.
\]

Fix a generator \(g\) of \(D\), use \(g^0,\ldots,g^{a-1}\) as representatives
of the antipodal pairs, and write every orientation uniquely as

\[
S_\epsilon=\{\epsilon_i g^i:0\le i<a\},
\qquad \epsilon_i\in\mathbb F_3^\times=\{1,-1\}.
\]

Put
\(\mathcal O_r=\{S_\epsilon:
\epsilon\in(\mathbb F_3^\times)^a\}\).

Let \(C_\epsilon(T)=\prod_i(1-\epsilon_i g^iT)\), and let
\(\Phi_u(S_\epsilon)\) be its first \(u\) nonconstant coefficients. For
\(0\le u\le a-2\), define

\[
E_{r,u}=\{m\in\{1,3,\ldots,N-1\}:
          [3^jm]_N>u\text{ for every }0\le j<r\},
\tag{1}
\]

where \([\cdot]_N\) is represented in \(\{1,\ldots,N-1\}\). Then, for every
\(z\in B^u\), the orientation-prefix fiber satisfies

\[
\boxed{\quad
 |\mathcal O_r\cap\Phi_u^{-1}(z)|\le2^{|E_{r,u}|}.
\quad}
\tag{2}
\]

Put

\[
L=\left\lceil\log_3\frac q{u+1}\right\rceil.
\tag{3}
\]

Whenever \(2L\le r\),

\[
|E_{r,u}|
 \le \frac q2\exp\!\left(-\frac{r}{2\cdot3^L}\right)
 \le \frac q2\exp\!\left(-\frac{r(u+1)}{6q}\right).
\tag{4}
\]

Consequently, for every sequence \(u=u_r\) with

\[
\frac{ru}{a}\longrightarrow\infty
\qquad
\left(u=\omega(a/r)=\omega(N/\log|B|)\right),
\tag{5}
\]

one has

\[
\max_z|\mathcal O_r\cap\Phi_u^{-1}(z)|=\exp(o(a)),
\qquad
\log|\Phi_u(\mathcal O_r)|=a\log2-o(a).
\tag{6}
\]

At fixed critical scale, let \(c>0\), put
\(u_r=\lfloor ca/r\rfloor\), and write
\(M_r(u)=\max_z|\mathcal O_r\cap\Phi_u^{-1}(z)|\). Then
\[
\max\!\left\{0,\log2-\frac c2\log3\right\}
\le\liminf_{r\to\infty}\frac{\log M_r(u_r)}a
\le\limsup_{r\to\infty}\frac{\log M_r(u_r)}a
\le e^{-c/12}\log2.
\tag{CW}
\]

For every fixed finite \(c\), the upper endpoint in (CW) is positive; (CW)
does **not** assert subexponential fibers. The subexponential conclusion (6)
uses the different quantifier order \(ru/a\to\infty\), equivalently a
critical-scale multiplier tending to infinity.

There is also a finite high-depth bound. Let \(d_u\) be the smallest odd
integer strictly larger than \(u\). If \(d_u>a/2\), then

\[
\max_z|\mathcal O_r\cap\Phi_u^{-1}(z)|
\le
\left\lfloor\frac{2d_u}{2d_u-a}\right\rfloor.
\tag{7}
\]

Thus \(u\ge\lfloor a/2\rfloor\) gives an \(O(a)\) bound,
\(u\ge(1/2+\eta)a\) gives \(O_\eta(1)\), and the largest legal depth
\(u=a-2\) gives at most two orientations per prefix.

## 1. Equal locator prefixes force moment constraints without division

Write

\[
C_\epsilon(T)=1+c_1T+\cdots+c_aT^a,\qquad
P_m(\epsilon)=\sum_i(\epsilon_i g^i)^m.
\]

Newton's identity is

\[
P_m+c_1P_{m-1}+\cdots+c_{m-1}P_1+m c_m=0.
\tag{8}
\]

If two locator prefixes agree through \(u\), induction in (8) shows that
their power sums agree through \(u\). This direction never divides by \(m\),
so it remains valid when \(3\mid m\).

This one-way implication is essential. The reverse Newton-coordinate change
is not invertible at the coordinates \(c_{3j}\) in characteristic three.
This packet therefore does not consume the frontiers theorem that assumes
\(R<\operatorname{char}B\), and it does not identify locator-prefix fibers
with ordinary-moment fibers.

For odd \(m\), \(\epsilon_i^m=\epsilon_i\). Hence, for
\(\delta_i=\epsilon_i-\epsilon_i'\in\mathbb F_3\),

\[
\widehat\delta(m)
 :=\sum_{i=0}^{a-1}\delta_i g^{im}=0
\quad\text{for every odd }m\le u.
\tag{9}
\]

## 2. Frobenius turns the missing frequencies into a small code

Because \(\delta_i\in\mathbb F_3\),

\[
\widehat\delta(3m)=\widehat\delta(m)^3.
\tag{10}
\]

Thus every zero in (9) propagates around its full multiplication-by-three
orbit modulo \(N\). The only Fourier coordinates that may remain nonzero are
the frequencies in \(E_{r,u}\).

The square matrix with rows indexed by all odd \(m=2j+1\) and columns
\(0\le i<a\) has entries

\[
g^{i(2j+1)}=g^i(g^{2i})^j.
\]

After removing the nonzero column factors \(g^i\), it is the Vandermonde
matrix on the \(a\) distinct nodes \(g^{2i}\). Hence the full odd-frequency
Fourier transform is injective.

Let one missing Frobenius orbit have length \(\ell\). Equation (10) says
that the whole orbit is determined by one seed \(y\), while orbit closure
forces \(y^{3^\ell}=y\). There are at most \(3^\ell\) possible seeds.
Multiplying over the missing orbits shows that the \(\mathbb F_3\)-linear
space \(V\) of allowable difference vectors has
\(\dim_{\mathbb F_3}V\le\sum\ell=|E_{r,u}|\).

For a nonempty prefix fiber, fix one orientation \(\epsilon_0\). The fiber
lies in the affine coset \(\epsilon_0+V\). If \(d=\dim V\), choose \(d\)
original coordinate positions on which projection is injective on \(V\)
(for example, pivot columns of a generator matrix). Projection remains
injective on \(\epsilon_0+V\), while an orientation has only two possible
signs at each selected position. The fiber therefore has at most
\(2^d\le2^{|E_{r,u}|}\) elements. This proves (2).

Equivalently, the necessary moment constraints define a Frobenius-cyclic
Fourier code over \(\mathbb F_3\), and one locator-prefix fiber lies in one
affine coset of that code. Ordinary moments give an upper container only;
the characteristic-three locator coordinates can cut the coset further.

## 3. Missing frequencies are ternary necklaces without a zero run

Represent a residue modulo \(3^r-1\) by its cyclic \(r\)-digit ternary word.
Multiplication by three rotates the digits. If the word has a cyclic run of
\(L\) zeros, rotate that run into the leading positions. The resulting
integer is strictly smaller than \(3^{r-L}\). From (3),

\[
3^{r-L}\le u+1,
\]

so that rotation lies at most \(u\). Every member of \(E_{r,u}\) must
therefore avoid a cyclic run \(0^L\).

For a uniformly random **labelled** ternary cyclic word, let \(A_i\) be the
event that the \(L\) digits beginning at \(i\) are all zero. Then

\[
\mu=\sum_i\Pr(A_i)=r3^{-L}.
\]

When \(2L\le r\), the ordered dependency sum satisfies

\[
\Delta
 =\sum_{i\sim j,\ i\ne j}\Pr(A_i\cap A_j)
 =2r\sum_{s=1}^{L-1}3^{-(L+s)}
 =\mu\bigl(1-3^{-(L-1)}\bigr)
 <\mu.
\]

The dependency-graph form of Janson's inequality gives

\[
\Pr\!\left(\bigcap_iA_i^c\right)
\le\exp(-\mu+\Delta/2)
<\exp(-\mu/2).
\]

Let \(\mathcal A\) be the set of **labelled** cyclic ternary words avoiding
\(0^L\); the Janson bound above counts \(|\mathcal A|\). Since \(L\ge1\),
the all-zero word is absent. Swap the first nonzero digit \(1\leftrightarrow2\).
This is a fixed-point-free involution of \(\mathcal A\): it preserves the
zero pattern and reverses integer parity because every power of three is odd.
Thus exactly \(|\mathcal A|/2\) avoiders are odd. The odd standard word
representatives are precisely the odd residues \(1,3,\ldots,N-1\), and
\(E_{r,u}\) is a subset of them. Therefore
\[
|E_{r,u}|\le\frac q2\exp(-\mu/2),
\]
which proves the first inequality in (4). Since \(3^L<3q/(u+1)\), the second
follows.

Under (5), condition \(2L\le r\) holds eventually. Moreover, for \(r\ge2\),
\(a/q\ge4/9\), so with \(t_r=ru/a\),

\[
\frac{|E_{r,u}|}{a}
\le\frac q{2a}\exp\!\left(-\frac{2t_r}{27}\right)=o(1).
\tag{11}
\]

Equations (2) and (11) prove (6).

For fixed \(c>0\), put \(u_r=\lfloor ca/r\rfloor\). This depth is eventually
legal, and \(L=O(\log r)\), so \(2L\le r\). In the second bound of (4),
\[
\frac q{2a}\longrightarrow1,
\qquad
\frac{r(u_r+1)}{6q}\longrightarrow\frac c{12}.
\]
Together with (2), this proves the upper side of (CW). PR #634 gives
\[
M_r(u_r)\ge
\left\lceil\frac{2^a}{q^{\lceil u_r/2\rceil}}\right\rceil.
\]
Since \(r\lceil u_r/2\rceil/a\to c/2\), this gives the lower side of (CW),
including the zero floor when the printed exponential lower bound is
vacuous.

In the fixed-linear specialization \(u\ge\delta a\),
\[
|E_{r,u}|\le \frac q2\exp(-2\delta r/27)
 =O_\delta(a^{\beta_\delta})
\quad\text{for some }\beta_\delta<1.
\]

## 4. A separate Hamming/Plotkin bound controls high depth

Take two distinct orientations in one prefix fiber and let \(J\) be the set
of flipped antipodal pairs, \(h=|J|\). Factor their common roots:

\[
C_\epsilon(T)-C_{\epsilon'}(T)
 =A(T)\bigl(B(T)-B(-T)\bigr),
\qquad A(0)=1,\quad\deg B=h.
\tag{12}
\]

The two residual root sets are disjoint negatives of one another, so
\(B(T)-B(-T)\ne0\). Its first nonzero term has odd degree, and its degree is
at most \(h\). Prefix agreement through \(u\), together with \(A(0)=1\),
forces that first odd degree to exceed \(u\). Therefore

\[
h\ge d_u.
\tag{13}
\]

Every prefix fiber is consequently a binary code of length \(a\) and minimum
distance at least \(d_u\). When \(d_u>a/2\), the binary Plotkin bound gives
(7). This argument is independent of the Fourier/zero-run estimate.

At the largest legal depth \(u=a-2\), one has \(d_u\in\{a-1,a\}\).
Translate a putative binary prefix code so that one word is zero. Every other
word then has weight at least \(a-1\), hence at most one zero. Two distinct
nonzero words of that form have mutual distance at most two, below
\(a-1\ge3\). Thus the endpoint fiber has at most two orientations, including
the small row \(r=2,a=4\) where the unrounded Plotkin expression alone gives
only three.

## 5. The resulting phase diagram

PR #631 already supplies the general profilewise pigeonhole and
fixed-prefix separating-pole transport at every legal depth, and applies it
to smooth power-map orientations at growing shallow depth. It proves no
uniform upper bound on every prefix fiber. PR #634 strengthens the lower side
on the present antipodal orientation family by exploiting its
half-dimensional locator-prefix image:

- if \(ru/a\to0\), some prefix fiber has size
  \(\exp(a\log2-o(a))\);
- at its highlighted \(u=\Theta(a/r)\), some prefix fiber has a fixed positive
  exponential rate;
- for every fixed \(c>0\), (CW) gives explicit lower and upper exponential
  rates at \(u=\lfloor ca/r\rfloor\);
- by (6), if \(ru/a\to\infty\), every prefix fiber is subexponential.

Thus \(a/r=\Theta(N/\log|B|)\) is the correct coarse transition scale for
this mechanism. PR #631's growing-shallow floor and PR #634's sharper
antipodal floor lie on the lower side; (CW) gives an explicit but nonmatching
fixed-critical-scale rate bracket, and (6) supplies the supercritical upper
side. The remaining exact problem is the maximum intersection of
\((\mathbb F_3^\times)^a\) with an affine coset of the Frobenius-cyclic
Fourier code, further cut by the characteristic-three locator coordinates.

PR #636 places the PR #634 mechanism in qualitative
effective-image-collapse geography: the half-dimensional image cap is a
collapse-trigger candidate rather than an occupancy-saturation conclusion.
From PR #634 alone, exact orientation image size, asymptotic uniformity of
prefix fibers, \(Q_{\rm img}=1\), exact \(G_1\), and one received line
realizing all of \(\mathcal O_r\) are not proved. None is used here. The
present theorem proves only restricted maximum-fiber and image-entropy
bounds; no C7 projection-degree payment follows.

PR #631 supplies the general slope transport used here, and PR #634 gives
the antipodal specialization. For each fixed \(z\), one chooses a
\(z\)-dependent extension and pole that separate the complete all-support
prefix fiber; under the full-field challenge, the resulting orientation
subcell has exactly as many distinct slopes as that fixed orientation fiber.
In the supercritical regime, (2) and (11) bound this number by
\(\exp(o(a))\). This does not give one line valid across prefixes, and says
nothing about nonorientation supports or other atlas cells.

## Hypothesis audit

| Item | Required here | Supplied |
| --- | --- | --- |
| field row | \(q=3^r\), \(r\ge2\) | stated in the theorem |
| antipodal coordinates | one representative from each \(\{x,-x\}\) | \(g^0,\ldots,g^{a-1}\) |
| legal locator depth | \(0\le u\le a-2\) | stated; inherited only for the optional pole corollary |
| Newton step | equal elementary prefixes imply equal moments | proved from (8), without division |
| Fourier step | odd-frequency matrix injective | explicit Vandermonde factorization |
| Frobenius step | difference coordinates lie in \(\mathbb F_3\) | \(\epsilon_i-\epsilon_i'\in\mathbb F_3\) |
| zero-run step | \(2L\le r\) | printed on the finite bound; automatic only asymptotically under (5) |
| parity-halving step | labelled cyclic words; \(L\ge1\) | first-nonzero-digit involution preserves zero runs and flips parity |
| Plotkin step | binary words and \(d_u>a/2\) | orientations are signs; condition printed |
| route geography | pre-atlas restricted support family | no primitive, payment, or envelope claim |

The theorem does **not** use the characteristic-\(>R\) Newton equivalence in
the frontiers TeX. It uses ordinary power sums only as necessary consequences
of elementary-prefix equality. It also does not assume that all allowable
Fourier seeds come from orientations or from locator-prefix fibers.

## Ledger effect and next wall

This packet closes the linear- and supercritical-depth item named by PR #634
for the restricted antipodal orientation class. It proves neither C7 payment
nor survival past the effective-image-collapse router. The paste-ready
experimental ledger entry is:

> Antipodal orientation prefixes have a coarse phase bracket at
> \(u\asymp N/\log|B|\). At fixed \(u=\lfloor ca/r\rfloor\), the normalized
> maximum-fiber rate lies between
> \(\max\{0,\log2-(c/2)\log3\}\) and \(e^{-c/12}\log2\). Along sequences
> with \(ru/a\to\infty\), every fiber is subexponential. The result is
> pre-atlas and restricted to \(\mathcal O_r\); no C7 payment or primitive
> conclusion.

The highest-value remaining atom in this line is to close the explicit gap
in (CW). In particular, once
\(c\ge2\log2/\log3\), the available lower rate is zero while the upper rate
remains positive for every fixed \(c\). Determine whether the true rate
vanishes at a finite \(c\) or stays positive, by controlling the sign-cube
intersection with the affine Frobenius-cyclic code and the additional
locator cuts; only then compare the witnesses exhaustively with the
collapse cell.

## Nonclaims

- No arbitrary-support, augmented-atlas, or post-C7 primitive theorem is
  claimed.
- No full-image certificate, profile-envelope, collapse payment, or global
  hard-input-A conclusion is claimed.
- No base-valued or bounded-extension received line is constructed.
- No converse from ordinary moments to locator prefixes is used.
- No exact formula for \(|\Phi_u(\mathcal O_r)|\) or for the critical-window
  maximum fiber is claimed.
- No fixed \(c\) is claimed to give subexponential fibers. That conclusion
  requires the different quantifier order \(ru/a\to\infty\) in (5).
- No uniformity, \(Q_{\rm img}=1\), exact \(G_1\), subexponential
  prefix-profile census, or global unrefined orientation-cell slope bound is
  claimed.
- No single received line works simultaneously across prefixes; the pole and
  extension used by the optional slope corollary may depend on \(z\).
- The Frobenius-cyclic Fourier coset is only an upper container for a locator
  fiber, not an exact parametrization.
- No finite M31 or KoalaBear survivor count, deployed inequality, target
  reserve, C9/Sidon, PTE, or Lean result changes.
- No paper TeX is changed.
