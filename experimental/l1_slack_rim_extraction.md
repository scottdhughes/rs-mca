# L1 Slack RIM Extraction

- **Status:** PROVED / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-18.
- **Scope:** Follow-up to
  `experimental/l1_repaired_locator_theorem_package.md` and
  `experimental/l1_high_multiplicity_certificate_roadmap.md`. This note does
  not edit Papers A-D and does not assert a positive worst-case list-size
  theorem, MCA theorem, line-decoding theorem, or protocol-safety consequence.

## Purpose

The high-multiplicity roadmap left certificate extraction as a conjectural
step. For the repaired arbitrary-word list object, the published
agreement-hypergraph / reduced-intersection-matrix (RIM) machinery gives the
needed extraction immediately, with slack.

This note records that import precisely. The result is a compression theorem:
if the repaired list already contains

\[
        t_0=\left\lceil\frac{2(n-k)}{\sigma}\right\rceil
\]

codewords at agreement threshold \(s=k+\sigma\), then a sublist of size at
most \(t_0\) yields a weakly-partition-connected agreement hypergraph and a
rank-defective RIM certificate on the smooth subgroup evaluation set.

The remaining open L1 work is not extraction. It is classification and
quantitative extension-counting for the extracted certificates on the fixed
smooth subgroup.

## Imported Agreement-Hypergraph / RIM Facts

This note imports the deterministic part of the
Alrabiah--Guo--Guruswami--Li--Zhang agreement-hypergraph/RIM framework:

1. **Minimal-subset extraction.** If an agreement hypergraph on a vertex set
   \(I\) has enough crossing weight, then some nontrivial induced subhypergraph
   is \(K\)-weakly-partition-connected.
2. **Symbolic RIM rank.** A \(K\)-weakly-partition-connected agreement
   hypergraph has a reduced intersection matrix that is symbolically full
   column rank.
3. **Specialized rank defect.** For an actual bad list of degree-\(<k\)
   polynomials, the RIM specialized to the evaluation points has a nonzero
   kernel supplied by coefficient vectors of polynomial differences.
4. **GetCertificate.** A symbolically full-rank RIM that becomes singular
   after specialization has a deterministic coordinate certificate. With slack
   parameter \(\delta\), the certificate length is
   \(r=\lfloor\delta/2\rfloor\), and for a fixed hypergraph the number of
   certificate coordinate sequences is bounded by
   \(\binom nr 2^{tr}\).

The status here is therefore PROVED / AUDIT: the new argument below is
elementary after importing those published RIM implications. This note does
not reprove the imported RIM theorems and does not import the random-evaluation
probability estimate.

## Setup

Let \(H\subseteq\mathbb F_q\) be an evaluation set of size \(n\), let

\[
        V_d:=\{f\in\mathbb F_q[X]:\deg f<d\},
\]

and fix \(U\in V_n\). For \(P\in V_k\), write

\[
        A_P(U):=\{x\in H: P(x)=U(x)\}.
\]

For \(s=k+\sigma\), the repaired arbitrary-word list is

\[
        \mathcal L_U(s)
        :=
        \{P\in V_k: |A_P(U)|\ge s\}.
\]

Put

\[
        D:=n-k,\qquad
        t_0:=\left\lceil\frac{2D}{\sigma}\right\rceil,
        \qquad
        \delta:=\left\lfloor\frac{\sigma}{2}\right\rfloor.
\]

We assume \(1\le\sigma\le D\) and \(t_0\ge3\). This is the intended
positive-reserve regime. If \(t_0<3\), the statement below should be replaced
by the trivial finite-size case analysis; it is not the logarithmic-size RIM
certificate regime targeted here.

For \(P_1,\ldots,P_t\in\mathcal L_U(s)\), define the agreement hypergraph on
vertex set \([t]\) by one labeled hyperedge for every \(x\in H\):

\[
        e_x:=\{i\in[t]: P_i(x)=U(x)\}.
\]

For a hyperedge \(e\), set \(w(e):=\max\{|e|-1,0\}\), and define total weight

\[
        W:=\sum_{x\in H}w(e_x).
\]

The precise definition of \(K\)-weak partition connectivity is the imported
RIM definition: every nontrivial partition of the vertex set has crossing
weight at least \(K\) times the partition deficit.

## The Slack Extraction Theorem

**Theorem.** Assume the setup above. If

\[
        |\mathcal L_U(s)|\ge t_0,
\]

then there exists a sublist

\[
        \{P_i:i\in J\}\subseteq\mathcal L_U(s)
\]

of size

\[
        3\le |J|\le t_0
\]

whose induced agreement hypergraph is
\((k+\delta)\)-weakly-partition-connected. Its reduced intersection matrix is
symbolically full column rank and becomes rank deficient after specializing
the symbolic variables to the evaluation points in \(H\).

### Proof

Choose distinct

\[
        P_1,\ldots,P_{t_0}\in\mathcal L_U(s).
\]

Since each \(P_i\) agrees with \(U\) on at least \(k+\sigma\) points,

\[
        \sum_{x\in H}|e_x|
        =
        \sum_{i=1}^{t_0}|A_{P_i}(U)|
        \ge
        t_0(k+\sigma).
\]

Also \(w(e)\ge |e|-1\) for every nonempty \(e\), while empty edges contribute
zero to both sides after summing with the crude subtraction by \(n\). Hence

\[
        W
        =
        \sum_{x\in H}\max\{|e_x|-1,0\}
        \ge
        \sum_{x\in H}|e_x|-n.
\]

Therefore

\[
        W
        \ge
        t_0(k+\sigma)-n
        =
        k(t_0-1)+(t_0\sigma-D).
\]

Since \(t_0=\lceil2D/\sigma\rceil\),

\[
        t_0\sigma-D\ge D
\]

and

\[
        (t_0-1)\frac{\sigma}{2}<D.
\]

Thus

\[
        t_0\sigma-D
        >
        (t_0-1)\frac{\sigma}{2}
        \ge
        (t_0-1)\left\lfloor\frac{\sigma}{2}\right\rfloor
        =
        (t_0-1)\delta.
\]

Consequently

\[
        W\ge (k+\delta)(t_0-1).
\]

The imported minimal-subset extraction lemma now gives a nontrivial subset
\(J\subseteq[t_0]\) whose induced agreement hypergraph is
\((k+\delta)\)-weakly-partition-connected.

The subset cannot have size two. If \(J=\{i,j\}\), weak partition connectivity
for the two-part partition forces at least \(k+\delta\) coordinates at which
both \(P_i\) and \(P_j\) agree with \(U\). Hence \(P_i-P_j\) has at least
\(k+\delta\ge k\) roots in \(H\). Since \(\deg(P_i-P_j)<k\), this forces
\(P_i=P_j\), contradicting the choice of distinct list elements.

Therefore \(3\le |J|\le t_0\).

For this sublist, the imported symbolic RIM theorem gives full column rank
over the symbolic coordinate variables. The specialized rank defect is the
standard RIM defect from an actual list: fixing one vertex \(j_0\in J\), the
coefficient vectors of the nonzero degree-\(<k\) differences
\(P_i-P_{j_0}\) satisfy the specialized RIM equations at the evaluation points
of \(H\). Thus the RIM becomes rank deficient after specialization to \(H\).
\(\square\)

## Sharper Slack Parameter

The proof gives a sharper parameter for any chosen \(t\ge2\). If

\[
        P_1,\ldots,P_t\in\mathcal L_U(k+\sigma),
\]

then the same weight calculation gives

\[
        W
        \ge
        k(t-1)+(t\sigma-D).
\]

Define

\[
        \delta_t
        :=
        \left\lfloor
        \frac{t\sigma-D}{t-1}
        \right\rfloor.
\]

Whenever \(\delta_t\ge0\), the minimal-subset extraction gives an induced
sublist whose agreement hypergraph is \((k+\delta_t)\)-weakly-partition-
connected. For \(t=t_0\), the inequalities above imply

\[
        \delta_{t_0}\ge \left\lfloor\frac{\sigma}{2}\right\rfloor.
\]

This is why the logarithmic-size certificate is the right target. A
\(t=3\)-only analysis would need roughly \(3\sigma\gtrsim D\), which is a much
larger slack regime than the intended \(\sigma\asymp n/\log n\) reserve.

## Deterministic Certificate Corollary

For the extracted sublist of size \(t\), apply the imported deterministic
GetCertificate theorem to its RIM. With

\[
        r=\left\lfloor\frac{\delta_t}{2}\right\rfloor,
\]

the rank defect on \(H\) has a coordinate certificate of length \(r\). For a
fixed agreement hypergraph, the number of possible certificate coordinate
sequences is bounded by

\[
        \binom nr\,2^{tr}.
\]

At the intended reserve \(\sigma\gtrsim n/\log n\), the extracted list size is

\[
        t=O\!\left(\frac{n-k}{\sigma}\right)=O(\log n),
\]

and \(r=\Theta(\sigma)\). Thus \(tr=O(n)\). This is a deterministic
compression statement. It is not yet a polynomial list-size theorem.

## What Does Not Transfer From Random RS

The random-RS proof fixes a hypergraph and bounds the probability that a random
evaluation sequence makes the RIM singular. That probabilistic step does not
apply directly here. In this project, \(H\) is a fixed smooth subgroup, and the
objects varying are primitive locator tuples, agreement hypergraphs, and
certificates.

The transferable part is therefore:

\[
        \text{large repaired list}
        \Longrightarrow
        \text{small RIM certificate singular on }H.
\]

The non-transferable part is:

\[
        \text{random evaluation probability bound}.
\]

The remaining theorem frontier is a fixed-domain classification/counting
statement.

## Remaining Frontier: Extension Counting

For every extracted certificate \(c\), define

\[
        E(c):=
        \{\text{primitive list tuples extending }c\}.
\]

The next required theorem should prove a dichotomy

\[
        E(c)
        \subseteq
        E_{\mathrm{quot}}(c)\cup E_{\mathrm{aper}}(c),
\]

where \(E_{\mathrm{quot}}(c)\) is controlled by the explicit quotient/folding
structures imported from PR #84, and the aperiodic part satisfies a quantitative
extension-counting bound such as

\[
        \sum_c |E_{\mathrm{aper}}(c)|\le n^{B-\theta}
\]

or the corresponding shell-budgeted version from
`experimental/l1_high_multiplicity_certificate_roadmap.md`.

This note closes the extraction gap. It does not close the quotient/aperiodic
classification or point-counting gap.

## Ledger Update

| Item | Status | Consequence |
|---|---|---|
| Repaired arbitrary-word list object | PROVED / AUDIT | Imported from `l1_repaired_locator_theorem_package.md`. |
| Slack RIM extraction from \(|\mathcal L_U(k+\sigma)|\ge t_0\) | PROVED / AUDIT | Follows from elementary weight counting plus imported agreement-hypergraph/RIM lemmas. |
| Sublist size \(3\le t\le t_0\) | PROVED | Size two is impossible for distinct degree-\(<k\) codewords with \(k+\delta\) common agreement points. |
| Specialized RIM rank defect | PROVED / AUDIT | Imported deterministic RIM implication from actual listed polynomials. |
| Symbolic full column rank | PROVED / AUDIT | Imported weak-partition-connectivity RIM theorem. |
| Deterministic certificate compression | PROVED / AUDIT | Imported GetCertificate step; no random-evaluation probability estimate is used. |
| Quotient/folding classification | CONJECTURAL / AUDIT | Should import structured families from PR #84 rather than rederive them. |
| Aperiodic extension-counting bound | CONJECTURAL | Remaining quantitative L1 frontier. |
| Positive worst-case list-size theorem | AUDIT | Not asserted here; requires classification and quantitative extension counting. |
