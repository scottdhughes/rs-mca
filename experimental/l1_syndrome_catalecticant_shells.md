# L1 Syndrome Catalecticant Shells

- **Status:** PROVED / CONJECTURAL / EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-19.
- **Scope:** Follow-up to the repaired locator, slack RIM extraction, and
  certificate extension-set notes. This note does not edit Papers A-D and does
  not assert a positive worst-case list-size theorem, MCA theorem,
  line-decoding theorem, or protocol-safety consequence.

## Purpose

The repaired primitive shell

\[
        \operatorname{PrimLoc}_U(a)
\]

has a canonical syndrome-coordinate representation. It is the set of split
error locators lying in a syndrome-dependent Hankel, or catalecticant, linear
section, with a nonzero-amplitude guard. This gives an exact arbitrary-word
analogue of divisor formulations used in quotient/folding constructions while
remaining safe for the zero word.

The result below turns the exact shell problem into:

> uniformly count \(H\)-split divisors of \(\Omega_H\) in a syndrome Hankel
> section, after removing quotient-periodic templates and imposing the
> recovered-amplitude nonvanishing guard.

## Setup

Let \(H\subseteq\mathbb F_q\) have size \(n\), set

\[
        \Omega_H(X):=\prod_{x\in H}(X-x),
\]

and let

\[
        D:=n-k.
\]

For \(x\in H\), define the standard parity-check weight

\[
        v_x:=\frac{1}{\Omega_H'(x)}.
\]

If \(H=\mu_n\subseteq\mathbb F_q^\times\), then
\(\Omega_H(X)=X^n-1\), so

\[
        v_x=\frac{x}{n}.
\]

For a received word \(y=\operatorname{ev}_H(U)\), define syndrome moments

\[
        s_m(U):=\sum_{x\in H} v_x U(x)x^m,
        \qquad 0\le m<D.
\]

These are exactly the generalized RS parity-check syndromes in moment form.

## Weighted Moment Parity Check

**Proposition.** If \(P\in V_k\), then

\[
        \sum_{x\in H} v_xP(x)x^m=0,
        \qquad 0\le m<D.
\]

Consequently, the syndrome moments \(s_m(U)\) depend only on the coset
\([U]\in V_n/V_k\).

### Proof

For \(0\le m<D=n-k\), the polynomial \(P(X)X^m\) has degree at most

\[
        (k-1)+(D-1)=n-2.
\]

The Lagrange coefficient identity says that for every polynomial \(F\) of
degree \(<n-1\),

\[
        \sum_{x\in H}\frac{F(x)}{\Omega_H'(x)}=0.
\]

Apply this with \(F(X)=P(X)X^m\). If \(U\) is replaced by \(U+P\) with
\(P\in V_k\), all displayed moments are unchanged. \(\square\)

## Necessity: Error Locators Satisfy Hankel Recurrences

Fix an exact agreement size \(a>k\), and put

\[
        j:=n-a,\qquad
        \tau:=D-j=a-k.
\]

Thus \(j\) is the exact error-support size, and \(\tau\) is the shell reserve.
Let \(P\in V_k\) agree with \(U\) on exactly \(a\) points, and let

\[
        E:=\{x\in H:U(x)\ne P(x)\}.
\]

Then \(|E|=j\). Define the monic error locator

\[
        M_E(T)
        =
        \prod_{x\in E}(T-x)
        =
        T^j+m_{j-1}T^{j-1}+\cdots+m_0.
\]

Let

\[
        e_x:=U(x)-P(x),
        \qquad
        w_x:=v_xe_x.
\]

Then

\[
        s_m(U)=\sum_{x\in E} w_xx^m,
        \qquad 0\le m<D.
\]

Since \(M_E(x)=0\) for \(x\in E\), for \(0\le r<D-j=\tau\),

\[
        s_{r+j}+\sum_{i=0}^{j-1}m_is_{r+i}
        =
        \sum_{x\in E}w_xx^rM_E(x)
        =
        0.
\]

Equivalently,

\[
        \mathsf H_j(s)
        \begin{pmatrix}
        m_0\\
        \vdots\\
        m_{j-1}\\
        1
        \end{pmatrix}
        =
        0,
\]

where

\[
        \mathsf H_j(s)=
        \begin{pmatrix}
        s_0&s_1&\cdots&s_j\\
        s_1&s_2&\cdots&s_{j+1}\\
        \vdots&\vdots&&\vdots\\
        s_{\tau-1}&s_\tau&\cdots&s_{D-1}
        \end{pmatrix}.
\]

For \(j=0\), this says precisely that all syndrome moments vanish.

## Converse: Vandermonde Amplitude Recovery

Let \(M\mid\Omega_H\) be monic of degree \(j\), and let

\[
        E=Z_H(M)=\{x_1,\ldots,x_j\}.
\]

Assume \(M\) satisfies the displayed Hankel recurrences. If \(j>0\), recover
scaled amplitudes \(w_{x_i}\) from

\[
        \begin{pmatrix}
        s_0\\
        s_1\\
        \vdots\\
        s_{j-1}
        \end{pmatrix}
        =
        \begin{pmatrix}
        1&\cdots&1\\
        x_1&\cdots&x_j\\
        \vdots&&\vdots\\
        x_1^{j-1}&\cdots&x_j^{j-1}
        \end{pmatrix}
        \begin{pmatrix}
        w_{x_1}\\
        \vdots\\
        w_{x_j}
        \end{pmatrix}.
\]

The Vandermonde matrix is invertible because the \(x_i\) are distinct. Impose
the primitive amplitude guard

\[
        w_x\ne0\qquad\text{for every }x\in E.
\]

For \(j=0\), the guard is vacuous and the recurrences require the zero
syndrome.

Define an error vector

\[
        e_x=
        \begin{cases}
        w_x/v_x,&x\in E,\\
        0,&x\notin E.
        \end{cases}
\]

The first \(j\) moments match by construction, and the recurrence for \(M\)
extends the match through all moments \(0\le m<D\). Hence \(e\) has the same
syndrome moments as \(U\). Therefore \(y-e\) has zero syndrome, so
\(y-e\in\operatorname{RS}[\mathbb F_q,H,k]\), and there is a unique
\(P\in V_k\) with \(\operatorname{ev}_H(P)=y-e\). The nonzero-amplitude guard
ensures the exact error support is \(E\), so \(P\) agrees with \(U\) on exactly
\(a=n-j\) points.

## Exact Primitive Syndrome-Locator Bijection

Combining the two directions gives a canonical bijection

\[
\operatorname{PrimLoc}_U(a)
\longleftrightarrow
\left\{
\begin{array}{c}
M\mid\Omega_H,\ M\text{ monic},\ \deg M=j,\\
\mathsf H_j(s)(m_0,\ldots,m_{j-1},1)^T=0,\\
w_x(M,s)\ne0\text{ for every }x\in Z_H(M)
\end{array}
\right\}.
\]

The locator \(M\) here is the complement locator from the primitive triple
\((L,M,Q)\). Thus this does not introduce a competing object. It gives the
existing primitive exact shell a canonical syndrome-coordinate section.

Equivalently, this is the same shell as the weight-\(j\) syndrome shell:

\[
        |\operatorname{PrimLoc}_U(a)|
        =
        |\{e:\operatorname{wt}(e)=j,\ M_Ce=M_Cy\}|.
\]

The new point is the divisor-linear-section representation of those same
errors.

## Zero-Syndrome Corollary

If

\[
        s_0=\cdots=s_{D-1}=0,
\]

then every divisor \(M\mid\Omega_H\) satisfies the recurrence equations.
However, Vandermonde recovery gives \(w_x=0\) at every root of every positive
degree \(M\). The primitive amplitude guard rejects all \(j>0\) candidates.
Only \(j=0\) remains.

Thus the syndrome-locator shell reproduces the repaired zero-word behavior:

\[
        |\operatorname{ListFib}_0(s)|=1,
\]

and does not revert to the raw-support overcount.

## Entropy Location And Local-Limit Target

At the first shell

\[
        a=k+\sigma,\qquad j=D-\sigma,
\]

the recurrence system has exactly

\[
        D-j=\sigma
\]

linear equations. The finite candidate universe is the set of monic degree-\(j\)
divisors of \(\Omega_H\), hence has size

\[
        \binom nj=\binom n{k+\sigma}.
\]

A random codimension-\(\sigma\) linear section would have heuristic scale

\[
        \frac{\binom n{k+\sigma}}{q^\sigma}.
\]

This is the generated-field entropy-reserve scale in Paper B, now located on a
concrete divisor-in-Hankel-section object.

The corrected local-limit target is therefore:

> Uniformly count aperiodic \(H\)-split divisors of \(\Omega_H\) lying in the
> syndrome Hankel section, subject to the recovered-amplitude nonvanishing
> guard, after separately budgeting quotient/folding templates.

This target is CONJECTURAL. It is not proved here.

## Quotient-Periodic Versus Aperiodic Divisors

A quotient-periodic divisor is one whose root set has a nontrivial permitted
subgroup-coset structure. In the cleanest cyclic case, this includes locators
of the form

\[
        M(T)=\widetilde M(T^d),
\]

or equivalently root sets that are unions of fibers of \(T\mapsto T^d\) on
\(H\).

The aperiodic part consists of \(H\)-split divisors with trivial permitted
subgroup stabilizer after the quotient/folding templates have been removed.
PR #84 supplies explicit quotient/folding templates, dilation symmetry, and
structured lower-bound obstructions. A uniform arbitrary-word upper bound for
all quotient extension sets remains a separate theorem requirement.

## Ledger

| Item | Status | Consequence |
|---|---|---|
| Weighted syndrome moment parity check | PROVED | Moments are the standard GRS parity checks. |
| Coset invariance of moments | PROVED | The object depends on \([U]\in V_n/V_k\). |
| Locator recurrence necessity | PROVED | Every primitive exact shell point gives a Hankel recurrence. |
| Vandermonde converse with amplitude guard | PROVED | Every guarded split divisor in the section gives an exact shell codeword. |
| Primitive shell / syndrome shell / guarded divisor shell equality | PROVED | Gives a canonical syndrome-locator section for exact shells. |
| Zero-syndrome guard | PROVED | Rejects all positive-degree divisors when the syndrome is zero. |
| Quotient-periodic divisor split | AUDIT / CONJECTURAL | Templates are known inputs, but full arbitrary-word quotient budgeting remains separate. |
| Aperiodic divisor-in-section local limit | CONJECTURAL | Main quantitative target after quotient structures are budgeted. |
| Positive worst-case list-size theorem | AUDIT | Not asserted here. |

## Companion Verifier

The script `experimental/verify_l1_syndrome_catalecticant_shells.py` checks
tiny prime-field cases by comparing four independently constructed finite
objects as canonical scaled-error atoms:

\[
        \text{exact RS shell}
        =
        \text{primitive support shell}
        =
        \text{weight-}j\text{ syndrome shell}
        =
        \text{guarded Hankel-divisor shell}.
\]

The verifier is EXPERIMENTAL / AUDIT evidence only.
