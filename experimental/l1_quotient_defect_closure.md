# L1 Quotient Defect Closure

- **Status:** PROVED / COUNTEREXAMPLE / CONJECTURAL / EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-19.
- **Scope:** Follow-up to
  `experimental/l1_periodic_support_multisequence_reduction.md`. This note
  does not edit Papers A-D and does not assert a positive worst-case list-size
  theorem, MCA theorem, line-decoding theorem, or protocol-safety consequence.

## Purpose

The periodic-support multisequence note gives an exact stabilizer ledger for
periodic primitive supports. Its exact-stabilizer-one bucket is not, however,
the right analytic definition of "quotient-free." A support can have trivial
stabilizer while being only one point away from a quotient-periodic support.

This note repairs the target class. It proves that low-defect perturbations of
quotient-periodic supports must be treated as structured exceptions. The
genuinely unresolved local-limit problem is the robustly aperiodic class after
low-defect quotient closures have been separately budgeted.

## Setup

Assume

\[
        H=\mu_n\subseteq\mathbb F_q^\times,\qquad D:=n-k.
\]

For an error support \(E\subseteq H\) of size \(j\), let

\[
        \mathbf s=(s_0,\ldots,s_{D-1}),\qquad
        s_m=\sum_{x\in E}w_xx^m,\qquad w_x\ne0,
\]

be the primitive syndrome-moment representation from
`experimental/l1_syndrome_catalecticant_shells.md`. Put

\[
        \tau:=D-j.
\]

The first shell \(a=k+\sigma\) has \(j=D-\sigma\) and \(\tau=\sigma\).

## Primitive Hankel Full-Row Rank

Let

\[
        \mathsf H_j(\mathbf s)
        =
        (s_{r+i})_{\substack{0\le r<\tau\\0\le i\le j}}
\]

be the \(\tau\times(j+1)\) Hankel/catalecticant matrix.

**Proposition.** If \(j\ge\tau\), then

\[
        \operatorname{rank}\mathsf H_j(\mathbf s)=\tau.
\]

### Proof

Suppose \(\lambda=(\lambda_0,\ldots,\lambda_{\tau-1})\) is in the left
kernel. Define

\[
        \Lambda(T)=\sum_{r=0}^{\tau-1}\lambda_rT^r.
\]

For every \(0\le i\le j\),

\[
        0=\sum_{r=0}^{\tau-1}\lambda_rs_{r+i}
        =
        \sum_{x\in E}w_x\Lambda(x)x^i.
\]

Using \(i=0,\ldots,j-1\), the \(j\times j\) Vandermonde matrix on the distinct
points of \(E\) is invertible, so

\[
        w_x\Lambda(x)=0\qquad(x\in E).
\]

All \(w_x\) are nonzero, hence \(\Lambda\) vanishes on \(j\) points. Since
\(\deg\Lambda<\tau\le j\), this forces \(\Lambda=0\), and therefore
\(\lambda=0\). The rows are independent. \(\square\)

If \(j<\tau\), then \(2j<D\). In that regime a fixed syndrome has at most one
weight-\(j\) error vector: two such errors with the same syndrome differ by a
codeword of the Reed-Solomon code and have difference weight at most
\(2j<D+1\), contradicting the minimum distance \(D+1\) unless they are equal.

Thus whenever an exact primitive shell can contain multiple points, its
Hankel locator equations have actual row rank \(\tau\), not merely expected
generic rank. At the first shell this gives actual row rank \(\sigma\).
This rank statement does not by itself count how many \(H\)-split divisors lie
in the section.

## One-Defect Quotient Lift

Let \(d>1\), \(d\mid n\), and \(d\mid k\). Put

\[
        K_d=\mu_d,\qquad H'=H^d,\qquad n'=\frac nd,\qquad k'=\frac kd.
\]

Let \(V\) be a quotient received word on \(H'\), and let

\[
        \mathcal W=\{W\in V_{k'}:\ |A_W(V)|=a'\}
\]

be an exact quotient shell.

**Theorem.** There is an arbitrary received word \(U\in V_n\) for which at
least

\[
        \frac{a'}{n'}|\mathcal W|
\]

distinct lifted codewords have agreement size \(da'-1\) and error supports
with trivial stabilizer in \(H\).

### Proof

Counting incidences between quotient codewords and their agreement points,

\[
        \sum_{y\in H'}|\{W\in\mathcal W:\ y\in A_W(V)\}|=a'|\mathcal W|.
\]

Choose \(y_0\in H'\) contained in at least
\((a'/n')|\mathcal W|\) of those agreement sets, and call the corresponding
subfamily \(\mathcal W_0\). Pick \(x_0\in H\) with \(x_0^d=y_0\).

Lift

\[
        U_0(X)=V(X^d),\qquad P_W(X)=W(X^d).
\]

Since \(\deg W<k'\), one has \(\deg P_W<dk'=k\). Let
\(\ell_{x_0}\in V_n\) be the Lagrange delta polynomial on \(H\), so

\[
        \ell_{x_0}(x_0)=1,\qquad
        \ell_{x_0}(x)=0\quad(x\in H,\ x\ne x_0).
\]

For any \(\eta\ne0\), set

\[
        U(X)=U_0(X)+\eta\ell_{x_0}(X).
\]

For \(W\in\mathcal W_0\), the lifted codeword \(P_W\) agrees with \(U\)
exactly on

\[
        \pi_d^{-1}(A_W(V))\setminus\{x_0\},
\]

where \(\pi_d(x)=x^d\). Hence its agreement size is \(da'-1\), and its error
support is

\[
        E_W=\pi_d^{-1}(H'\setminus A_W(V))\cup\{x_0\}.
\]

Every \(K_d\)-coset is full or empty in \(E_W\), except the coset
\(x_0K_d\), which contains exactly one error point. If \(hE_W=E_W\), then
\(h\) must preserve the unique partially occupied \(K_d\)-coset, so
\(h\in K_d\). It must also preserve the singleton \(\{x_0\}\), hence
\(hx_0=x_0\) and \(h=1\). Thus \(\operatorname{Stab}_H(E_W)=\{1\}\).

The lift \(W\mapsto W(X^d)\) is injective, so the displayed count of distinct
lifted codewords follows. \(\square\)

The reserve transforms as

\[
        (da'-1)-k=d(a'-k')-1.
\]

If the quotient family is a threshold list rather than an exact shell,
pigeonholing by exact agreement size loses at most another factor \(n'\).
Thus a large quotient list remains large after only polynomial loss.

**Counterexample consequence.** Exact stabilizer one does not imply
quotient-free or random-like behavior. It can contain a one-coordinate defect
of a quotient-periodic lifted family.

## Quotient Defect

For \(d\mid n\), define the full \(K_d\)-coset core of a support \(E\) by

\[
        E_d^{\mathrm{full}}
        =
        \bigcup\{xK_d:\ xK_d\subseteq E\}.
\]

Define the \(d\)-boundary and defect by

\[
        \partial_dE:=E\setminus E_d^{\mathrm{full}},\qquad
        \beta_d(E):=|\partial_dE|.
\]

Then \(\beta_d(E)=0\) means \(E\) is exactly \(K_d\)-periodic, while
\(\beta_d(E)=1\) includes the one-defect lift above. Exact stabilizer one only
says every nontrivial \(d\) has some defect; it does not say that the defect
is large.

## Exact Defect Stripping

Fix \(d\mid n\). Let

\[
        B:=\partial_dE,\qquad \beta:=|B|.
\]

Write the boundary locator as

\[
        B_E(T)=\prod_{b\in B}(T-b)=\sum_{u=0}^{\beta}b_uT^u,
        \qquad b_\beta=1.
\]

Because \(E_d^{\mathrm{full}}\) is a union of \(K_d\)-cosets, its locator has
the form \(\widetilde M(T^d)\). Therefore

\[
        M_E(T)=B_E(T)\widetilde M(T^d).
\]

Define the boundary-filtered syndrome by

\[
        t_r:=\sum_{u=0}^{\beta}b_us_{r+u},
        \qquad 0\le r<D-\beta.
\]

Then

\[
\begin{aligned}
        t_r
        &=
        \sum_{u=0}^{\beta}b_u\sum_{x\in E}w_xx^{r+u}  \\
        &=
        \sum_{x\in E}w_xB_E(x)x^r
        =
        \sum_{x\in E_d^{\mathrm{full}}}w_xB_E(x)x^r.
\end{aligned}
\]

Boundary points disappear because \(B_E(x)=0\) on \(B\). On the full core,
\(B_E(x)\ne0\), so the transformed amplitudes

\[
        w'_x:=w_xB_E(x)
\]

remain nonzero. Thus \(\mathbf t=\mathcal T_B\mathbf s\) is a primitive
syndrome for the exactly periodic core \(E_d^{\mathrm{full}}\).

The reserve is preserved. If

\[
        |E|=\beta+dj',
\]

then the filtered syndrome length is \(D-\beta\), and

\[
        (D-\beta)-dj'=D-|E|=\tau.
\]

Thus boundary stripping loses no reserve; it converts a low-defect support
into the periodic multisequence setting of
`experimental/l1_periodic_support_multisequence_reduction.md`.

## Low-Defect Quotient Union Bound

Let \(\mathcal S_j(\mathbf s)\) denote the guarded degree-\(j\) support shell
from the syndrome-catalecticant and determinantal notes. For a fixed \(d\mid n\)
and defect \(\beta\), defect stripping gives the upper-bound template

\[
|\{E\in\mathcal S_j(\mathbf s):\ \beta_d(E)=\beta\}|
\le
\sum_{\substack{B\subseteq H\\ |B|=\beta}}
P_{d,j-\beta}(\mathcal T_B\mathbf s),
\]

where \(P_{d,j-\beta}\) counts primitive periodic quotient multisequence
supports of size \(j-\beta\) for the filtered syndrome. Terms with
divisibility failures, incompatible boundary/core intersections, or other
empty incidence conditions may be omitted. Keeping them only enlarges the
right-hand side, so this is an overlap-safe union bound.

Each defect level carries an additional support-choice cost

\[
        \log_2\binom n\beta,
\]

which must be charged to the quotient ledger. Exact periodicity is only the
\(\beta=0\) term.

## Robustly Aperiodic Target

For thresholds \(\mathbf R=(R_d)_{d\mid n,\ d>1}\), call a support robustly
aperiodic when

\[
        \beta_d(E)>R_d\qquad\text{for every nontrivial }d\mid n.
\]

Define

\[
\mathcal S_j^{\mathrm{rob}}(\mathbf s;\mathbf R)
=
\{E\in\mathcal S_j(\mathbf s):\ \beta_d(E)>R_d\text{ for all }d>1\}.
\]

Then

\[
\mathcal S_j(\mathbf s)
\subseteq
\mathcal S_j^{\mathrm{rob}}(\mathbf s;\mathbf R)
\cup
\bigcup_{\substack{d\mid n\\ d>1}}
\bigcup_{\beta\le R_d}
\{E:\ \beta_d(E)=\beta\}.
\]

The low-defect part is controlled only after summing the quotient multisequence
budgets above over boundary choices. The unresolved local-limit claim should
apply to the robustly aperiodic part, not to the exact-stabilizer-one part.

The exact syndrome-average scale for the full degree-\(j\) shell is

\[
        \mu_j=q^{-D}\binom nj(q-1)^j.
\]

At \(j=D-\sigma\), this is

\[
        \mu_j=
        \binom njq^{-\sigma}\left(1-\frac1q\right)^j.
\]

A corrected conjectural analytic target is therefore:

\[
        |\mathcal S_j^{\mathrm{rob}}(\mathbf s;\mathbf R)|
        \le
        \mu_j+n^{B_0},
\]

uniformly in the syndrome, after the low-defect quotient budget has separately
been shown polynomial. This is CONJECTURAL.

## Revised L1 Frontier

The stabilizer Mobius ledger from
`experimental/l1_periodic_support_multisequence_reduction.md` remains exact
and useful, but it is only a stabilizer ledger. It should not be read as a
complete analytic quotient-free decomposition.

The corrected route is:

\[
        \text{large robustly aperiodic shell}
        \Longrightarrow
        \text{RIM certificate}
        \Longrightarrow
        \text{many low-defect quotient patterns or a bounded exception}.
\]

The final open problem is now sharper: prove a uniform robustly aperiodic
determinantal point count after charging the low-defect quotient closures to
the quotient ledger.

## Ledger

| Item | Status | Consequence |
|---|---|---|
| Primitive Hankel full-row rank for \(j\ge\tau\) | PROVED | Multiple-point shells have actual locator row rank \(\tau\). |
| \(j<\tau\) uniqueness of a fixed syndrome shell | PROVED | Below the half-distance threshold a shell cannot have multiple points. |
| One-defect quotient lift | PROVED | Quotient-periodic lists can create trivial-stabilizer supports after one coordinate defect. |
| Exact stabilizer one as quotient-free class | COUNTEREXAMPLE | Too coarse for the analytic generic remainder. |
| Full-coset core and boundary factorization | PROVED | Low-defect supports factor as boundary times a quotient locator. |
| Boundary-syndrome filtering | PROVED | Removes the boundary and preserves nonzero amplitudes on the periodic core. |
| Reserve preservation under defect stripping | PROVED | Low-defect reduction loses no \(\tau=D-j\) reserve. |
| Low-defect quotient union bound | PROVED | Gives an overlap-safe structured exception budget. |
| Robustly aperiodic local limit | CONJECTURAL | New quantitative L1 target after low-defect closures are removed. |
| Positive worst-case list-size theorem | AUDIT | Not asserted here. |
