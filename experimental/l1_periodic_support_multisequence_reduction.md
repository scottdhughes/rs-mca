# L1 Periodic Support Multisequence Reduction

- **Status:** PROVED / CONJECTURAL / EXPERIMENTAL / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-19.
- **Scope:** Follow-up to
  `experimental/l1_determinantal_support_criterion.md`. This note does not
  edit Papers A-D and does not assert a positive worst-case list-size theorem,
  MCA theorem, line-decoding theorem, or protocol-safety consequence.

## Purpose

The determinantal support criterion isolates quotient-periodic patterns as
structured subincidences of the universal determinantal family. This note gives
the exact arbitrary-word reduction for periodic error supports.

The result is stronger than a folding-source injection. It exhausts all
primitive shell supports invariant under a subgroup \(K_d\): the original
syndrome recurrence system is equivalent to one common quotient locator
annihilating \(d\) decimated syndrome sequences, with a primitive guard given
by inverse orbit Fourier transform.

## Setup

Assume

\[
        H=\mu_n\subseteq\mathbb F_q^\times,
\]

and let \(d\mid n\). Put

\[
        K_d:=\mu_d\le H.
\]

Let \(\mathbf s=(s_0,\ldots,s_{D-1})\) be a syndrome vector, and let
\(E\subseteq H\) have size \(j\). Its monic error locator is

\[
        M_E(T)=\prod_{x\in E}(T-x)
        =
        T^j+\sum_{i=0}^{j-1}m_iT^i.
\]

## Stabilizer-Locator Equivalence

**Proposition.** For \(E\subseteq H\), the following are equivalent:

1. \(K_dE=E\);
2. \(d\mid j\) and \(E\) is a union of \(K_d\)-cosets;
3. \(M_E(T)=\widetilde M_E(T^d)\) for a unique monic divisor
   \(\widetilde M_E(Z)\mid Z^{n/d}-1\) of degree \(j/d\);
4. in the locator coefficients, \(m_i=0\) whenever \(d\nmid i\).

### Proof

The action of \(K_d\) on \(H=\mu_n\) is free by multiplication, so
\(K_dE=E\) if and only if \(E\) is a union of \(K_d\)-orbits, equivalently
\(K_d\)-cosets. Thus \(d\mid |E|=j\).

If \(E\) is such a union, the image

\[
        \widetilde E:=E/K_d=\{x^d:x\in E\}\subseteq H^d=\mu_{n/d}
\]

has size \(j/d\), and

\[
        M_E(T)
        =
        \prod_{y\in\widetilde E}(T^d-y)
        =
        \widetilde M_E(T^d),
\]

where \(\widetilde M_E(Z)=\prod_{y\in\widetilde E}(Z-y)\). Conversely, a
locator of the form \(\widetilde M(T^d)\) has root set that is a union of
\(K_d\)-cosets. The coefficient sparsity condition is exactly the statement
that only powers \(T^{dh}\) occur. \(\square\)

Thus the \(K_d\)-periodic locus is coordinate-linear in locator-coefficient
space.

## Decimated-Syndrome Theorem

Assume \(j=dj'\), and write

\[
        \widetilde M(Z)=Z^{j'}+\sum_{h=0}^{j'-1}\widetilde m_hZ^h.
\]

The original locator recurrences for \(M(T)=\widetilde M(T^d)\) are

\[
        s_{r+dj'}+\sum_{h=0}^{j'-1}\widetilde m_hs_{r+dh}=0,
        \qquad
        0\le r<D-dj'.
\]

For \(0\le c<d\), define the decimated sequence

\[
        s^{(c)}_t:=s_{c+dt}.
\]

Then \(M(T)=\widetilde M(T^d)\) satisfies the full original syndrome system if
and only if the same quotient locator \(\widetilde M\) annihilates every
decimated sequence:

\[
        s^{(c)}_{t+j'}
        +
        \sum_{h=0}^{j'-1}\widetilde m_hs^{(c)}_{t+h}
        =
        0
\]

for every pair \((c,t)\) with

\[
        0\le c<d,\qquad 0\le c+dt<D-j.
\]

### Proof

Every integer \(r\) with \(0\le r<D-dj'\) has a unique expression
\(r=c+dt\) with \(0\le c<d\). Substituting \(j=dj'\) and
\(m_{dh}=\widetilde m_h\), while all other \(m_i\) vanish, rewrites the
original recurrence at \(r\) as the displayed decimated recurrence at
\((c,t)\). \(\square\)

The periodic arbitrary-word shell is therefore a common split-locator problem
for \(d\) interleaved syndrome sequences on the quotient domain \(H^d\). It is
not merely a single folded RS list.

## Orbit Fourier Amplitudes

Let \(E\) be \(K_d\)-periodic, and let scaled amplitudes \(w_x\) be supported
on \(E\). For a quotient point

\[
        y=x^d\in\widetilde E:=E/K_d,
\]

define orbit Fourier amplitudes

\[
        A_{y,c}:=\sum_{\kappa\in K_d}w_{\kappa x}(\kappa x)^c,
        \qquad 0\le c<d.
\]

Then

\[
        s_{c+dt}
        =
        \sum_{y\in\widetilde E} A_{y,c}y^t.
\]

Indeed,

\[
        \sum_{\kappa\in K_d}w_{\kappa x}(\kappa x)^{c+dt}
        =
        \left(
        \sum_{\kappa\in K_d}w_{\kappa x}(\kappa x)^c
        \right)
        (x^d)^t,
\]

because \(\kappa^d=1\).

Since \(d\mid q-1\), \(d\) is invertible in \(\mathbb F_q\). Fourier inversion
on \(K_d\) gives

\[
        w_{\kappa x}
        =
        \frac1d
        \sum_{c=0}^{d-1}A_{y,c}(\kappa x)^{-c}.
\]

Thus nonzero quotient Fourier amplitudes are not enough. The primitive guard is
the inverse-DFT open condition

\[
        \frac1d
        \sum_{c=0}^{d-1}A_{y,c}(\kappa x)^{-c}
        \ne0
\]

for every \(y=x^d\in\widetilde E\) and every \(\kappa\in K_d\).

## Exact Periodic-Shell Bijection

Let \(\operatorname{PerShell}_{j,d}(\mathbf s)\) be the primitive degree-\(j\)
shell supports invariant under \(K_d\). Then there is a canonical bijection

\[
\operatorname{PerShell}_{j,d}(\mathbf s)
\longleftrightarrow
\left\{
\begin{array}{c}
\widetilde E\subseteq H^d,\quad |\widetilde E|=j/d,\\
\widetilde M_{\widetilde E}
\text{ annihilates every decimated }
\mathbf s^{(c)},\\
\text{the inverse-DFT primitive guard holds}
\end{array}
\right\}.
\]

The raw candidate universe drops from

\[
        \binom nj
\]

to

\[
        \binom{n/d}{j/d}.
\]

The recurrence system still contains the same \(D-j\) scalar equations, now
distributed across the \(d\) residue sequences.

## Exact Stabilizer Mobius Ledger

Let \(P_d(\mathbf s)\) count primitive supports whose stabilizer contains
\(K_d\), and let \(Q_d(\mathbf s)\) count primitive supports whose stabilizer is
exactly \(K_d\). In the cyclic group \(H\),

\[
        P_d(\mathbf s)
        =
        \sum_{\substack{e:\ d\mid e\\ e\mid\gcd(n,j)}}Q_e(\mathbf s).
\]

Therefore

\[
        Q_d(\mathbf s)
        =
        \sum_{\substack{e:\ d\mid e\\ e\mid\gcd(n,j)}}
        \mu(e/d)P_e(\mathbf s).
\]

In particular, the exact aperiodic shell count is

\[
        Q_1(\mathbf s)
        =
        \sum_{e\mid\gcd(n,j)}\mu(e)P_e(\mathbf s).
\]

This gives an overlap-safe stabilizer ledger for removing quotient-periodic
templates.

## Remaining Frontier

After this reduction, the arbitrary-word periodic side is an exact
multisequence quotient-support problem. The remaining aperiodic target is

\[
        \text{uniformly count exact-stabilizer-}1
        \text{ supports satisfying the determinantal system}.
\]

This note does not prove that count.

## Ledger

| Item | Status | Consequence |
|---|---|---|
| \(K_dE=E\) iff \(E\) is a union of \(K_d\)-cosets | PROVED | Periodic supports are quotient supports. |
| \(K_d\)-periodic support iff \(M_E(T)=\widetilde M_E(T^d)\) | PROVED | Periodicity is coordinate-linear in locator coefficients. |
| Original recurrences iff all decimated recurrences | PROVED | Periodic arbitrary-word shells are common multisequence quotient-locator problems. |
| Orbit Fourier moment decomposition | PROVED | Decimated syndromes share quotient support with different amplitude columns. |
| Inverse-DFT primitive guard | PROVED | Primitive nonvanishing is an orbit-coordinate open condition. |
| Exact-stabilizer Mobius ledger | PROVED | Gives an overlap-safe periodic/aperiodic decomposition. |
| Exact-stabilizer-1 aperiodic count | CONJECTURAL | Main remaining quantitative target. |
| Positive worst-case list-size theorem | AUDIT | Not asserted here. |

## Companion Verifier

The script
`experimental/verify_l1_periodic_support_multisequence_reduction.py` checks
tiny cyclic prime-field cases for:

1. support invariance iff the locator lies in \(T^d\);
2. locator coefficient sparsity;
3. original recurrence system iff all decimated recurrence systems;
4. orbit Fourier moment decomposition;
5. inverse-DFT amplitude recovery and primitive guard equivalence;
6. direct exact-stabilizer counts versus Mobius inversion.

The verifier is EXPERIMENTAL / AUDIT evidence only.
