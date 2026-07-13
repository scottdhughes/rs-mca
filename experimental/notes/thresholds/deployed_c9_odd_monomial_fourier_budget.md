# Deployed C9 full-slice odd-monomial Fourier budget

## Status and publication gate

**PROVED / EXACT FINITE FULL-SLICE CERTIFICATE / PRZ-GATED.**  This note is
based on
`origin/main@fe93bb59dff3d022f66a097208e17c27e1e0deb4`.  It certifies one
object only: the absolute Fourier budget of the odd single-monomial modes on
the complete fixed-composition 16-block slice at the deployed row below.  It
also certifies that the same absolute Gauss-period plus uniform cycle-index
method is already nonpaying at the quadratic mode.

The novelty decision is deliberately narrow:

```text
exact q=2^17 fixed-composition 16-block instantiation only.
```

The product Fourier identity, signed complementation, the two-block Plotkin
cap, the monomial Gauss-period mechanism, and the cycle-index coefficient
majorant are supporting known machinery.  They are not claimed as new here.

This package is a narrow experimental PRZ candidate, not a publication
authorization.  Publication must be refused if the result is framed as a C9
payment, a first-match theorem, an arbitrary weighted-circle theorem, payment
of even or multimonomial modes, a global max-fiber theorem, or official score
movement.  Subject to a fresh overlap check, there is no additional
mathematical refusal reason for publishing the exact finite certificate under
the title and scope above; the remaining editorial question is whether this
fixed instance is substantial enough for a standalone PR.

## Exact object

Put

\[
 p=2,130,706,433,\qquad q=131,072=2^{17},\qquad w=67,471,
\]

and let \(H\leq\mathbb F_p^\times\) have order \(q\).  The verifier checks

\[
 p\text{ is prime},\qquad p-1=2^{24}\cdot127=16,256q.
\]

Take 16 labeled \(H\)-cosets, arranged in eight negative/positive pairs.  On
each negative block use a complemented minority of size
\(t_-=60,000\); its original occupancy is \(q-t_-=71,072\).  On each
positive block use a support of size \(t_+=51,566\).  Thus

\[
 n=16q=2,097,152,\qquad
 m=8(q-t_-)+8t_+=981,104.
\]

For \(S\subseteq\mathbb F_p\), write

\[
 \Phi_w(S)=\left(\sum_{x\in S}x,\ldots,\sum_{x\in S}x^w\right).
\]

For every \(H\)-coset \(C=\theta H\) and \(1\leq d\leq w<q\),
\(\sum_{x\in C}x^d=0\): the geometric sum over \(H\) can be nonzero only
when \(q\mid d\).  Therefore complementing a dense block replaces its
moment vector by its negative and introduces no fixed offset.

The complete complemented slice is

\[
 \Omega=\prod_{j=1}^8
 \binom{C_j^-}{t_-}\times\binom{C_j^+}{t_+},
 \qquad
 M=|\Omega|=
 \left[\binom q{t_-}\binom q{t_+}\right]^8,
\]

with signed boundary map

\[
 \Psi(U)=\sum_{j=1}^8
 \left(\Phi_w(U_j^+)-\Phi_w(U_j^-)\right)
 \in\mathbb F_p^w.
\]

Fix a nontrivial additive character \(\psi\) of \(\mathbb F_p\), and define

\[
 \widehat\Omega(\alpha)
 =\sum_{U\in\Omega}\psi\!\left(\alpha\cdot\Psi(U)\right),
 \qquad \alpha\in\mathbb F_p^w.
\]

This is the Fourier transform of the complete product slice.  No transform of
an arbitrarily first-match-deleted subset is used.

## Exact theorem

Let \(e_d\) be the \(d\)-th coordinate vector and put

\[
 \mathcal O
 =\{ae_d:a\in\mathbb F_p^\times,\ 1\leq d\leq w,\ d\text{ odd}\}.
\]

There are exactly

\[
 |\mathcal O|=33,736(p-1)=71,881,512,189,952                 \tag{D1}
\]

such modes.  Set

\[
 \Lambda=\lceil\sqrt p\rceil=46,160,
 \quad
 C_- = \binom{\Lambda+t_--1}{t_-},
 \quad
 C_+ = \binom{\Lambda+t_+-1}{t_+},
\]

and

\[
 R_{\rm odd}=C_-^8C_+^8,
 \qquad S_{\rm odd}=|\mathcal O|R_{\rm odd}.
\]

Then every \(\alpha\in\mathcal O\) satisfies

\[
 |\widehat\Omega(\alpha)|\leq R_{\rm odd},
\]

and therefore

\[
 \frac1{p^w}\sum_{\alpha\in\mathcal O}
 |\widehat\Omega(\alpha)|
 \leq\frac{S_{\rm odd}}{p^w}<2^{-472028},                 \tag{D2}
\]

\[
 \frac1M\sum_{\alpha\in\mathcal O}
 |\widehat\Omega(\alpha)|
 \leq\frac{S_{\rm odd}}M<2^{-438163},                   \tag{D3}
\]

\[
 \frac M{p^w}<2^{-33865},                                \tag{D4}
\]

and, even after an intentionally excessive labeled-profile multiplier,

\[
 \frac{16!}{p^w}
 \left(M+\sum_{\alpha\in\mathcal O}
 |\widehat\Omega(\alpha)|\right)
 \leq\frac{16!(M+S_{\rm odd})}{p^w}<2^{-33820}.          \tag{D5}
\]

The exponents in (D2)--(D5) are the maximal strict binary exponents for the
displayed certificate numerators.  The verifier checks the two sides of each
floor exactly:

\[
\begin{aligned}
 S_{\rm odd}2^{472028}&<p^w\leq S_{\rm odd}2^{472029},\\
 S_{\rm odd}2^{438163}&<M\leq S_{\rm odd}2^{438164},\\
 M2^{33865}&<p^w\leq M2^{33866},\\
 16!(M+S_{\rm odd})2^{33820}
 &<p^w\leq16!(M+S_{\rm odd})2^{33821}.
\end{aligned}
\]

Thus the odd coordinate axes are paid in the complete full-slice absolute
Fourier ledger, and nowhere else.

## Proof

### 1. Odd powers and Gauss periods

Because \(q\) is a power of two, every odd \(d\) satisfies
\(\gcd(d,q)=1\).  Hence \(x\mapsto x^d\) permutes \(H\) and maps each
\(H\)-coset onto another \(H\)-coset.  Let

\[
 s=\frac{p-1}{q}=16,256.
\]

Expanding a coset indicator in the \(s\) multiplicative characters trivial
on \(H\), using the trivial Gauss sum \(-1\) and modulus \(\sqrt p\) for
each nontrivial Gauss sum, gives, for every \(b\ne0\),

\[
 \left|\sum_{x\in\theta H}\psi(bx)\right|
 \leq\frac{1+(s-1)\sqrt p}{s}<\sqrt p<\Lambda.           \tag{1}
\]

The verifier checks (1) without floating point.  In particular,

\[
 (s\Lambda-1)^2-(s-1)^2p=79,620,071,001,856>0.
\]

For every cycle length \(1\leq r\leq t_-\), which covers both block sizes,
the coefficient \(r(\mathord\pm a)\theta^d\) is nonzero modulo \(p\), because
\(t_-<p\).  Thus (1) applies to every cycle used below.

### 2. Fixed-weight cycle majorant and product slice

For one block of size \(q\), the fixed-weight character coefficient is the
elementary symmetric coefficient of the \(q\) phase values.  The standard
Newton/cycle-index majorant gives

\[
 |e_t|\leq[u^t](1-u)^{-\Lambda}
 =\binom{\Lambda+t-1}{t}.
\]

The complete slice is a direct product.  Its signed block factors therefore
multiply exactly; signs and coset scalars only replace the nonzero additive
coefficient in (1).  Applying the block bound eight times at \(t_-\) and
eight times at \(t_+\) gives
\(|\widehat\Omega(\alpha)|\leq C_-^8C_+^8\).  Summing over the exact count
(D1) gives \(S_{\rm odd}\), and the four exact integer comparisons printed
above prove (D2)--(D5).

## Quadratic-method route cut

For the quadratic mode \(ae_2\), the power map \(x\mapsto x^2\) has kernel
two on \(H\).  Its image \(H^2\) has index \(2s\) in
\(\mathbb F_p^\times\), and

\[
 \sum_{x\in\theta H}\psi(bx^2)
 =2\sum_{y\in\theta^2H^2}\psi(by).
\]

The same absolute period argument therefore supplies only

\[
 \Lambda_2=2\Lambda=92,320.
\]

For both deployed block sizes, its cycle-index majorant is already larger
than the zero-character block coefficient:

\[
 \binom{\Lambda_2+t_--1}{t_-}>\binom q{t_-},\qquad
 \binom{\Lambda_2+t_+-1}{t_+}>\binom q{t_+}.             \tag{Q1}
\]

More precisely, the verifier checks by exact shifts that

\[
 \left\lfloor\log_2
 \frac{\binom{\Lambda_2+t_--1}{t_-}}{\binom q{t_-}}
 \right\rfloor=16,937,
 \qquad
 \left\lfloor\log_2
 \frac{\binom{\Lambda_2+t_+-1}{t_+}}{\binom q{t_+}}
 \right\rfloor=8,701.
\]

Consequently the pointwise absolute Gauss-period bound followed by the
uniform cycle-index majorant cannot produce a nontrivial quadratic
coefficient estimate at this row.  This is a method route cut.  It is not a
lower bound on the actual quadratic coefficient and not evidence that the
coefficient is large.

## Supporting known machinery

The following inputs are used only as prior machinery.

1. `experimental/notes/thresholds/signed_local_minority_fixed_composition.md`
   supplies signed complementation and the block-centered Plotkin theorem.
   Applied to one negative/positive pair, its already-proved formula has

   \[
   B_{\rm pair}
   =60,000(131,072-60,000)+51,566(131,072-51,566)
   =8,364,126,396,
   \]

   while \((w+1)q=8,843,689,984\).  The gap is \(479,563,588\), and

   \[
   18(479,563,588)\leq8,843,689,984
   <19(479,563,588).
   \]

   Hence the known two-block theorem gives cap 18.  This arithmetic is
   replayed here as a supporting check; no new pair-cap theorem is claimed,
   and cap 18 does not give a global cap \(18^8\).

2. `experimental/asymptotic_rs_mca_frontiers.tex`, theorem
   `thm:prefix-flatness-power-sum`, supplies the fixed-weight Fourier and
   cycle-index mechanism.  This note instantiates it only on the complete
   product slice.

3. `experimental/notes/roadmaps/b2_conjq_partial_results.md`, Round (f),
   already records the deployed odd-monomial permutation/Gauss-period
   mechanism.  The present novelty is not that mechanism; it is the exact
   \(q=2^{17}\), \((t_-,t_+)=(60,000,51,566)\), 8+8 block budget and its
   exact D2--D5 margins.

## Overlap audit through PR #739

The overlap check was refreshed on 2026-07-13 against
`origin/main@fe93bb59dff3d022f66a097208e17c27e1e0deb4` and the live PR set
through #739.  PR #736 and PR #738 are pay-per-bit ledger audits, PR #737 is an
all-LineRay affine-core statement package, and PR #739 is a Sidon-paired
staircase-concentration route cut; none has theorem or file overlap with this
certificate.

- The integrated signed local-minority note contains the underlying signed
  and Plotkin machinery, but not this odd-mode certificate.
- Open #726 proves general unweighted constant-Weil cycle flatness under its
  own hypotheses.  It explicitly does not supply this deployed 16-block
  instantiation.
- Open #723, #728, and #729 concern first-match masks or pruned signed
  packets.  They do not prove full-slice odd-axis Fourier cancellation, and
  this note does not use them to claim first-match survival.
- #724, #725, #727, and #730--#736 contain no duplicate of the exact row,
  D2--D5 margins, or quadratic majorant comparison above.
- #737 concerns all-pair affine cores and has no Fourier certificate or
  deployed-row arithmetic in common with this packet.
- #738 audits the conditional 86-bit branch row by row and contains neither
  the fixed-composition Fourier object nor the D2--D5 certificate.
- #739 concerns depth-one Sidon-paired fiber concentration and does not contain
  this deployed fixed-composition Fourier calculation.

The result remains true if any of those open PRs merge because its claim is
the fixed finite full-slice arithmetic only.

## Remaining wall

At the analytic full-slice layer, every even single-monomial mode and every
multimonomial mode remains unpaid.  A complete payment still needs an
aggregate estimate over that complementary dual, strong enough to control the
global eight-pair convolution or the equivalent complete-slice max fiber.
The pair cap 18 does not control additive representation multiplicity among
the eight pair images.

Beyond that analytic wall, the source still needs a valid first-match owner,
the exact weighted-circle identification if a circle chart is claimed, an
independent RC/direct-ray payment, and image-scale profile add-back.  None of
those obligations is moved by (D2)--(D5).

## Required nonclaims

- No C9 or hard-input-2 payment is proved.
- No first-match Fourier factorization or survival is proved.
- No arbitrary weighted-circle theorem is proved.
- No even-mode or multimonomial payment is proved.
- No global max-fiber bound is proved.
- No Q-to-RC implication is proved.
- No image-scale add-back is proved.
- No official score moves; it remains `0/2`.
- Odd axes are paid only in the complete full-slice absolute Fourier ledger.
- No stable paper TeX is edited.

## Reproducibility

The machine-readable certificate is

```text
experimental/data/certificates/deployed-c9-odd-monomial-fourier-budget/deployed_c9_odd_monomial_fourier_budget.json
```

The matching unproved Lean statement target is

```text
experimental/lean/grande_finale/GrandeFinale/DeployedC9OddMonomialFourierBudget.lean
```

It records the exact arithmetic brackets, the pointwise-to-aggregate odd-mode
compiler, and the quadratic-method route cut without claiming a Lean proof.

The stdlib-only verifier is

```text
experimental/scripts/verify_deployed_c9_odd_monomial_fourier_budget.py
```

Run:

```bash
python3 experimental/scripts/verify_deployed_c9_odd_monomial_fourier_budget.py --check
python3 -O experimental/scripts/verify_deployed_c9_odd_monomial_fourier_budget.py --check
python3 experimental/scripts/verify_deployed_c9_odd_monomial_fourier_budget.py --tamper-selftest
python3 -m py_compile experimental/scripts/verify_deployed_c9_odd_monomial_fourier_budget.py
python3 experimental/scripts/verify_signed_local_minority_fixed_composition.py --check
```

The normal `--check` output is preserved byte-for-byte at

```text
experimental/data/certificates/deployed-c9-odd-monomial-fourier-budget/verifier_output.txt
```
