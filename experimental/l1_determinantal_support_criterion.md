# L1 Determinantal Support Criterion

- **Status:** PROVED / CONJECTURAL / EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-19.
- **Scope:** Follow-up to
  `experimental/l1_syndrome_catalecticant_shells.md`. This note does not edit
  Papers A-D and does not assert a positive worst-case list-size theorem, MCA
  theorem, line-decoding theorem, or protocol-safety consequence.

## Purpose

The syndrome-catalecticant shell note represents primitive exact shells as
guarded \(H\)-split divisors in a syndrome Hankel section. This note rewrites
the same condition as explicit generalized Vandermonde determinants on support
points.

For a support \(E=\{x_1,\ldots,x_j\}\subseteq H\), the recurrence equations are
equivalent to vanishing of minors

\[
        F_r(E;s)=0.
\]

Cramer minors encode the nonzero-amplitude guard. Thus the aperiodic counting
problem becomes a point-counting problem on an explicit quasi-affine
determinantal system on \(H^j/S_j\), after quotient-periodic components are
removed.

## Setup

Assume \(H\subseteq\mathbb F_q^\times\) is a multiplicative evaluation domain
of size \(n\), and let

\[
        D:=n-k.
\]

For a received word \(U\), let

\[
        s_m:=\sum_{x\in H}v_xU(x)x^m,\qquad 0\le m<D,
\]

be the weighted syndrome moments from
`experimental/l1_syndrome_catalecticant_shells.md`.

Fix an error-support size \(j\le D\). For

\[
        E=\{x_1,\ldots,x_j\}\subseteq H,
\]

write

\[
        M_E(T)=\prod_{\ell=1}^j(T-x_\ell)
        =
        T^j+m_{j-1}T^{j-1}+\cdots+m_0.
\]

The shell reserve is

\[
        \tau:=D-j.
\]

For the first shell \(a=k+\sigma\), one has \(j=D-\sigma\) and
\(\tau=\sigma\).

## Generalized Vandermonde Minors

For \(0\le r<\tau\), define

\[
F_r(E;s)=
\det
\begin{pmatrix}
x_1^r&\cdots&x_j^r&s_r\\
x_1^{r+1}&\cdots&x_j^{r+1}&s_{r+1}\\
\vdots&&\vdots&\vdots\\
x_1^{r+j}&\cdots&x_j^{r+j}&s_{r+j}
\end{pmatrix}.
\]

For \(j=0\), interpret this as the one-by-one determinant

\[
        F_r(\varnothing;s)=s_r.
\]

For \(j>0\), the first \(j\) rows and first \(j\) columns form

\[
        V_r(E):=(x_\ell^{r+h})_{0\le h<j,\ 1\le\ell\le j}.
\]

Because \(H\subseteq\mathbb F_q^\times\) and the \(x_\ell\) are distinct,

\[
        \det V_r(E)=
        \left(\prod_{\ell=1}^j x_\ell^r\right)
        \prod_{\ell<m}(x_m-x_\ell)\ne0.
\]

Thus the determinant \(F_r(E;s)\) vanishes exactly when the last column segment
\((s_r,\ldots,s_{r+j})^T\) lies in the span of the \(j\) support columns.

## Equivalence With Locator Recurrences

**Proposition.** For \(j>0\) and \(0\le r<\tau\),

\[
        F_r(E;s)=0
\]

if and only if

\[
        s_{r+j}+\sum_{i=0}^{j-1}m_is_{r+i}=0.
\]

For \(j=0\), the condition is \(s_r=0\).

### Proof

For \(j=0\), both conditions are the same.

Assume \(j>0\). Since \(V_r(E)\) is invertible, the first \(j\) equations

\[
        s_{r+h}=\sum_{\ell=1}^j w_\ell x_\ell^{r+h},
        \qquad 0\le h<j,
\]

recover unique amplitudes \(w_\ell\). The determinant \(F_r(E;s)\) vanishes
exactly when the same amplitudes also satisfy

\[
        s_{r+j}=\sum_{\ell=1}^j w_\ell x_\ell^{r+j}.
\]

If this holds, then

\[
        s_{r+j}+\sum_{i=0}^{j-1}m_is_{r+i}
        =
        \sum_{\ell=1}^j
        w_\ell x_\ell^r
        \left(x_\ell^j+\sum_{i=0}^{j-1}m_ix_\ell^i\right)
        =
        \sum_{\ell=1}^j w_\ell x_\ell^rM_E(x_\ell)
        =
        0.
\]

Conversely, if the recurrence holds, the same displayed identity and
\(M_E(x_\ell)=0\) show that the predicted value
\(\sum_\ell w_\ell x_\ell^{r+j}\) equals \(s_{r+j}\). Hence the last column is
in the support-column span, and \(F_r(E;s)=0\). \(\square\)

Consequently, a support \(E\) satisfies all syndrome-locator recurrences if
and only if

\[
        F_r(E;s)=0,\qquad 0\le r<\tau.
\]

## Cramer Minors And The Amplitude Guard

Let

\[
        V_0(E)=(x_\ell^h)_{0\le h<j,\ 1\le\ell\le j}.
\]

For \(1\le\ell\le j\), define \(C_\ell(E;s)\) by replacing the \(\ell\)-th
column of \(V_0(E)\) with

\[
        (s_0,\ldots,s_{j-1})^T
\]

and taking the determinant.

Since \(\det V_0(E)\ne0\), Cramer's rule gives

\[
        w_{x_\ell}=\frac{C_\ell(E;s)}{\det V_0(E)}.
\]

Thus the primitive nonzero-amplitude guard is exactly

\[
        C_\ell(E;s)\ne0,\qquad 1\le\ell\le j.
\]

Equivalently,

\[
        \prod_{\ell=1}^j C_\ell(E;s)\ne0.
\]

For \(j=0\), this guard is vacuous.

## Quasi-Affine Support System

Let \(\operatorname{Conf}_j(H)\subseteq H^j\) be the ordered configuration
space of distinct support points. Define

\[
        \mathcal D_j(s)
        =
        \left\{
        (x_1,\ldots,x_j)\in\operatorname{Conf}_j(H):
        F_r(E;s)=0\ \forall\,0\le r<\tau,\quad
        \prod_{\ell=1}^jC_\ell(E;s)\ne0
        \right\}.
\]

This is a quasi-affine determinantal system: closed generalized Vandermonde
minor equations plus open Cramer nonvanishing conditions. It is invariant under
the symmetric group \(S_j\), up to the expected sign changes in determinants,
and its quotient by \(S_j\) is precisely the guarded split-divisor shell from
`experimental/l1_syndrome_catalecticant_shells.md`.

Thus

\[
        \operatorname{PrimLoc}_U(n-j)
        \cong
        \mathcal D_j(s)/S_j.
\]

## Quotient-Periodic And Aperiodic Components

The determinant formulation gives a concrete ambient space for classification.
Quotient-periodic supports are those whose unordered support set is a union of
permitted subgroup-coset fibers, for example fibers of \(x\mapsto x^d\) in the
cyclic case. These should be isolated as structured strata or components inside
\(\mathcal D_j(s)/S_j\).

The aperiodic problem is the remaining point count:

> uniformly bound aperiodic points of the quasi-affine determinantal system
> \(\mathcal D_j(s)/S_j\), after quotient/folding templates have been removed.

PR #84 supplies quotient/folding templates, dilation symmetry, and structured
lower-bound obstructions. It should be imported as structured input, not treated
as a complete arbitrary-word upper bound.

## Ledger

| Item | Status | Consequence |
|---|---|---|
| Nonzero generalized Vandermonde denominator | PROVED | Multiplicative domains make \(V_r(E)\) invertible for distinct support points. |
| \(F_r(E;s)=0\) iff locator recurrence \(r\) holds | PROVED | Replaces Hankel recurrences by explicit support determinants. |
| Cramer minors encode nonzero amplitudes | PROVED | The primitive guard is a quasi-affine open condition. |
| Guarded split-divisor shell equals \(\mathcal D_j(s)/S_j\) | PROVED / AUDIT | Same object as the primitive shell from #89, in support coordinates. |
| Quotient-periodic support strata | AUDIT / CONJECTURAL | Templates are structured inputs; full upper-budget classification remains open. |
| Aperiodic determinantal point count | CONJECTURAL | Main quantitative target. |
| Positive worst-case list-size theorem | AUDIT | Not asserted here. |

## Companion Verifier

The script `experimental/verify_l1_determinantal_support_criterion.py` checks
tiny prime-field cases by comparing:

1. generalized Vandermonde minor vanishing;
2. locator recurrence vanishing;
3. Cramer-minor nonvanishing;
4. the guarded Hankel-divisor shell from
   `experimental/verify_l1_syndrome_catalecticant_shells.py`.

The verifier is EXPERIMENTAL / AUDIT evidence only.
