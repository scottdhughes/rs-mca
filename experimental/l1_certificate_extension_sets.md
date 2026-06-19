# L1 Certificate Extension Sets

- **Status:** PROVED / CONJECTURAL / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-19.
- **Scope:** Follow-up to
  `experimental/l1_slack_rim_extraction.md` and
  `experimental/l1_high_multiplicity_certificate_roadmap.md`. This note does
  not edit Papers A-D and does not assert a positive worst-case list-size
  theorem, MCA theorem, line-decoding theorem, or protocol-safety consequence.

## Purpose

The slack RIM extraction note proves that a repaired arbitrary-word list of
size

\[
        t_0=\left\lceil\frac{2(n-k)}{\sigma}\right\rceil
\]

already contains a certified sublist. To turn certificate counting into a list
bound, one more elementary bridge is needed: enough disjoint certified blocks
cover all but fewer than \(t_0\) listed codewords.

This note proves that bridge, defines point-level extension sets
\(E_U(c)\), and records the exact union-bound implication needed for the L1
program. The remaining open step is quantitative aperiodic extension counting
for certificates on the fixed smooth subgroup \(H\).

## Setup

Let \(H\subseteq\mathbb F_q\) have size \(n\), let

\[
        V_d:=\{f\in\mathbb F_q[X]:\deg f<d\},
\]

and fix \(U\in V_n\). For \(s=k+\sigma\), write

\[
        \mathcal L
        =
        \mathcal L_U(s)
        :=
        \{P\in V_k:|\{x\in H:P(x)=U(x)\}|\ge s\}.
\]

Put

\[
        D:=n-k,\qquad
        t_0:=\left\lceil\frac{2D}{\sigma}\right\rceil.
\]

A **certified block** is a sublist \(J\subseteq\mathcal L\) produced by
`experimental/l1_slack_rim_extraction.md`: it has

\[
        3\le |J|\le t_0
\]

and carries a weakly-partition-connected agreement hypergraph, a symbolically
full-rank RIM, a rank defect after specialization to \(H\), and the associated
deterministic GetCertificate data.

The exact representation of a certificate signature \(c\) can be refined later.
For this note, \(c\) records at least the finite combinatorial choices needed
to define the certificate witness incidence: arity \(t\), selected coordinate
labels in \(H\), agreement type at those certificate coordinates, selected RIM
minor/pivot data, nonvanishing guards, and the deterministic GetCertificate run
or refresh data.

## Certificate-Packing Lemma

**Lemma.** There exist pairwise disjoint certified sublists

\[
        J_1,\ldots,J_m\subseteq\mathcal L
\]

such that

\[
        3\le |J_i|\le t_0
\]

and

\[
        \left|
        \mathcal L\setminus\bigcup_{i=1}^{m}J_i
        \right|
        <t_0.
\]

Consequently,

\[
        \sum_i |J_i|
        \ge
        |\mathcal L|-(t_0-1).
\]

### Proof

Run the following greedy algorithm. Start with \(R_0=\mathcal L\). While
\(|R_j|\ge t_0\), choose any \(t_0\) distinct elements of \(R_j\). The slack RIM
extraction theorem applies to those \(t_0\) listed codewords and produces a
certified block \(J_{j+1}\subseteq R_j\) with \(3\le |J_{j+1}|\le t_0\). Set

\[
        R_{j+1}:=R_j\setminus J_{j+1}.
\]

The process terminates because each step removes at least three list elements.
The blocks are disjoint by construction. At termination, \(|R_m|<t_0\), so

\[
        \left|
        \mathcal L\setminus\bigcup_{i=1}^{m}J_i
        \right|
        =
        |R_m|
        <t_0.
\]

The final inequality follows from

\[
        \sum_i |J_i|
        =
        |\mathcal L|-|R_m|
        \ge
        |\mathcal L|-(t_0-1).
\]

\(\square\)

This lemma is independent of exact agreement shells. The selected certified
blocks may contain codewords with different exact agreement sizes.

## Point-Level Extension Sets

For a certificate signature \(c\), define the point-level extension set

\[
        E_U(c)
        :=
        \{P\in\mathcal L:
        P\text{ occurs in some certified block realizing }c\}.
\]

The packing lemma immediately gives

\[
        |\mathcal L|
        \le
        t_0-1+
        \left|\bigcup_c E_U(c)\right|
        \le
        t_0-1+\sum_c |E_U(c)|.
\]

Indeed, all elements in the certified blocks \(J_i\) lie in the union
\(\bigcup_cE_U(c)\), and fewer than \(t_0\) list elements remain outside the
packed blocks.

This is the sufficiency statement needed for certificate counting. It is not
enough to count certified tuples. One must count the list points that occur in
some tuple realizing a certificate, or use a summed extension-set bound that
dominates those points.

## Mixed-Shell Primitive Multi-Incidence

Return to the universal primitive incidence over

\[
        \mathcal B:=V_n/V_k.
\]

For each exact agreement size \(a\), write

\[
        \pi_a:\mathfrak X_a^{\mathrm{prim}}\longrightarrow\mathcal B
\]

for the primitive locator-cofactor projection from
`experimental/l1_repaired_locator_theorem_package.md`.

Since extraction works directly from the repaired list, do not impose shell
concentration. For \(t\ge3\), define the mixed-shell multi-incidence

\[
        \mathfrak X_{\ge s}^{(t)}
        :=
        \bigsqcup_{\mathbf a\in[s,n]^t}
        \left(
        \mathfrak X_{a_1}^{\mathrm{prim}}
        \times_{\mathcal B}\cdots\times_{\mathcal B}
        \mathfrak X_{a_t}^{\mathrm{prim}}
        \right)\setminus\Delta,
\]

where \(\Delta\) removes repeated listed codewords. A point of
\(\mathfrak X_{\ge s}^{(t)}\) is a \(t\)-tuple of distinct primitive listed
codewords over one coset \(b\in\mathcal B\), with exact agreement sizes allowed
to vary from vertex to vertex.

Let

\[
        \pi:\mathfrak X_{\ge s}^{(t)}\longrightarrow\mathcal B
\]

denote the common projection to the coset coordinate.

After choosing a representative \(U\) of \(b=[U]\), each vertex projection
recovers the associated listed polynomial

\[
        P_i=U-L_iQ_i\in V_k.
\]

Coset invariance from the repaired locator package shows that translating
\(U\) by an element of \(V_k\) translates all \(P_i\) by the same codeword and
does not change the relevant cardinality bounds.

## Certificate-Witness Incidence

For a certificate signature \(c\) of arity \(t=t(c)\), define a locally closed
witness incidence

\[
        \mathfrak W_c\subseteq\mathfrak X_{\ge s}^{(t)}
\]

by imposing the algebraic and open conditions encoded by \(c\):

1. the agreement-type constraints at the certificate coordinates;
2. the RIM minor vanishing conditions that make the specialized RIM singular;
3. the preceding nonvanishing conditions that make the deterministic
   certificate selection unambiguous;
4. the GetCertificate run or refresh data needed to identify the same
   certificate signature.

These are locally closed conditions: equalities encode vanishing of the relevant
polynomial evaluations and RIM minors, while inequalities encode distinct
coordinates, primitive-resultant conditions, nonzero pivots, and preceding
nonvanishing guards.

For \(b\in\mathcal B\), define the point-level extension set geometrically as
the union of vertex projections:

\[
        E_b(c)
        :=
        \bigcup_{i=1}^{t(c)}
        \rho_i\left(\mathfrak W_c\cap\pi^{-1}(b)\right),
\]

where \(\rho_i\) maps a witness tuple to its \(i\)-th listed codeword after
choosing a representative \(U\) of \(b\). Equivalently, for \(b=[U]\),
\(E_b(c)=E_U(c)\) up to the common coset translation by \(V_k\).

This definition is gauge-free. It counts list elements, not solver sections,
pivot gauges, or redundant tuple certificates.

## Exact List-Bound Implication

Suppose that for every coset \(b=[U]\) and every certificate \(c\), one has a
quotient/aperiodic split

\[
        E_b(c)
        \subseteq
        E_b^{\mathrm{quot}}(c)\cup E_b^{\mathrm{aper}}(c).
\]

Then the packing lemma gives the exact deterministic bound

\[
        |\mathcal L_U(k+\sigma)|
        \le
        t_0-1
        +
        \sum_c |E_b^{\mathrm{quot}}(c)|
        +
        \sum_c |E_b^{\mathrm{aper}}(c)|.
\]

Thus a positive L1 theorem follows from two independent budgets:

1. a structured quotient/folding budget. PR #84 supplies explicit
   quotient/folding templates, dilation symmetry, and structured lower-bound
   obstructions, but it does not by itself give a uniform arbitrary-word upper
   bound for all quotient extension sets;
2. a uniform aperiodic extension-counting bound, for example

\[
        \sum_c |E_b^{\mathrm{aper}}(c)|\le n^{B-\theta}.
\]

At the intended reserve \(\sigma\gtrsim n/\log n\), the packing remainder

\[
        t_0=O(\log n)
\]

is negligible compared with any fixed polynomial budget.

## Remaining Theorem Target

The exact remaining implication is

\[
        \text{small RIM certificate singular on }H
        \Longrightarrow
        \text{quotient/folding structure or bounded aperiodic extensions}.
\]

More concretely, for every extracted certificate \(c\), prove

\[
        E_b(c)
        \subseteq
        E_b^{\mathrm{quot}}(c)\cup E_b^{\mathrm{aper}}(c)
\]

where the quotient/folding term must be controlled by a separate structured
upper-budget theorem. PR #84 supplies the templates and lower-bound
obstructions that this branch should import; a complete arbitrary-word quotient
extension-set classification remains a separate requirement unless subsequently
proved. The aperiodic side then needs a uniform summed bound:

\[
        \sum_c |E_b^{\mathrm{aper}}(c)|\le n^{B-\theta}.
\]

This is the point where new algebraic geometry, finite-field incidence, or
fixed-domain RIM classification is needed. More raw scanning, additional pivot
gauges, or shell concentration will not by themselves prove this implication.

## Ledger

| Item | Status | Consequence |
|---|---|---|
| Certificate-packing lemma | PROVED | Covers all but fewer than \(t_0\) list elements by disjoint certified blocks. |
| Point-level extension sets \(E_U(c)\) | PROVED / AUDIT | Converts tuple certificates into list-element coverage. |
| Mixed-shell primitive multi-incidence | PROVED / AUDIT | Keeps extraction compatible with codewords from different exact shells. |
| Certificate-witness incidence \(\mathfrak W_c\) | AUDIT | Locally closed model for deterministic certificate signatures; exact implementation can be refined. |
| Union-bound list implication | PROVED | A summed extension-set bound directly yields a repaired list bound up to the \(t_0-1\) remainder. |
| Quotient/folding branch | AUDIT / CONJECTURAL | Should import #84 templates, dilation symmetry, and lower-bound obstructions; a full arbitrary-word quotient extension-set upper budget remains separate. |
| Aperiodic extension counting | CONJECTURAL | Main remaining quantitative L1 theorem target. |
| Positive worst-case list-size theorem | AUDIT | Not asserted here; requires the quotient and aperiodic budgets. |
