# L1 High-Multiplicity Certificate Roadmap

- **Status:** PROVED / CONJECTURAL / AUDIT.
- **Agent/model:** Codex.
- **Date:** 2026-06-18.
- **Scope:** Follow-up roadmap for
  `experimental/l1_repaired_locator_theorem_package.md`. This note does not
  edit Papers A-D and does not assert a positive worst-case list-size theorem,
  MCA theorem, line-decoding theorem, or protocol-safety consequence.

## Purpose

The repaired locator package identifies the right uniform fiber problem:

\[
        \pi_a:\mathfrak X_a^{\mathrm{prim}}\longrightarrow V_n/V_k.
\]

For a coset \(b=[U]\in V_n/V_k\), write

\[
        F_a(b):=\pi_a^{-1}(b)
\]

and

\[
        L_s(b):=\sum_{a=s}^{n}|F_a(b)|.
\]

The remaining theorem gap is not another finite scanner. It is a
high-multiplicity certificate extraction statement:

> A large aperiodic fiber of \(\pi_a\) should force a bounded-complexity
> incidence/rank certificate, and every such certificate should either be one
> of the explicit quotient/folding structures or lie in a quantitatively small
> aperiodic exceptional class.

This note isolates the elementary reductions that are already proved and states
the missing certificate lemma precisely enough to guide the next proof attempt.

## Coordination Boundary

This note treats the quotient/folding constructions from PR #84, including its
arbitrary-word dilation/folding lift, as structured inputs. It does not rederive
monomial-prefix divisor counts, Fourier-prefix analysis, quotient-core floors,
or folding lower bounds.

The intended division is:

- **PR #84 lane:** explicit quotient/folding constructions, quotient-core
  floors, prefix/Fourier analysis.
- **This lane:** corrected arbitrary-word statement object, universal primitive
  incidence, exact syndrome correspondence, and extraction of certificates from
  high-multiplicity fibers.
- **PR #82 lane:** M1 Kummer/residue-line work.

## Reduction 1: Shell Concentration

**Status:** PROVED.

If

\[
        L_s(b)>n^B,
\]

then some \(a\in[s,n]\) satisfies

\[
        |F_a(b)|>\frac{n^B}{n-s+1}\ge n^{B-1}.
\]

Thus a cumulative \(n^B\) bound reduces, with one exponent of slack, to a
single exact agreement shell.

### Proof

There are \(n-s+1\) exact shells in the sum

\[
        L_s(b)=\sum_{a=s}^{n}|F_a(b)|.
\]

If every shell had size at most \(n^B/(n-s+1)\), then the cumulative sum would
be at most \(n^B\). Since \(n-s+1\le n\), the displayed lower bound follows.
\(\square\)

## Reduction 2: Locator Injectivity

**Status:** PROVED.

For fixed \(b\in V_n/V_k\) and \(a>k\), the map

\[
        (L,M,Q)\longmapsto L
\]

is injective on \(F_a(b)\).

### Proof

Given \(L\), the cofactor is forced:

\[
        M=\Omega_H/L.
\]

If \(Q_1\) and \(Q_2\) correspond to the same coset \(b\), then

\[
        [LQ_1]=[LQ_2]\quad\text{in }V_n/V_k,
\]

so

\[
        L(Q_1-Q_2)\in V_k.
\]

If \(Q_1\ne Q_2\), then \(L(Q_1-Q_2)\) is a nonzero polynomial of degree at
least \(\deg L=a>k\), impossible for an element of \(V_k\). Hence \(Q_1=Q_2\).
\(\square\)

Consequently, a high primitive-fiber multiplicity is a large family of
genuinely distinct maximal agreement locators. It is not gauge multiplicity or
redundant certificate multiplicity.

## Reduction 3: Pairwise Intersection And The Johnson Barrier

**Status:** PROVED.

Let \(t\) distinct elements of a fixed exact shell \(F_a(b)\) have maximal
agreement supports

\[
        A_i\subseteq H,\qquad |A_i|=a,\qquad 1\le i\le t.
\]

For distinct \(i,j\),

\[
        |A_i\cap A_j|\le k-1.
\]

Indeed, the corresponding degree-\(<k\) polynomials would otherwise agree on
at least \(k\) points and therefore be equal, contradicting distinct shell
elements.

Define incidence degrees

\[
        d_x:=|\{i:x\in A_i\}|.
\]

Then

\[
        \sum_{x\in H}d_x=ta
\]

and

\[
        \sum_{x\in H}\binom{d_x}{2}
        =
        \sum_{i<j}|A_i\cap A_j|
        \le
        \binom t2(k-1).
\]

Cauchy-Schwarz gives

\[
        \sum_x d_x^2\ge \frac{t^2a^2}{n}.
\]

Since

\[
        \sum_x\binom{d_x}{2}
        =
        \frac12\left(\sum_x d_x^2-\sum_x d_x\right),
\]

we obtain

\[
        \frac{t^2a^2/n-ta}{2}
        \le
        \frac{t(t-1)(k-1)}2.
\]

If \(a^2>n(k-1)\), this yields

\[
        t
        \le
        \frac{a-k+1}{a^2/n-k+1}.
\]

This proves that pairwise incidence controls the shell above the Johnson
barrier. It also proves why pairwise incidence cannot establish the desired
\(a=k+\sigma\) regime below that barrier: a higher-order certificate is
necessary.

## Missing Lemma 1: High-Multiplicity Extraction

**Status:** CONJECTURAL.

Fix a quotient/folding structured sub-incidence

\[
        \mathfrak X_{a,\mathrm{quot}}^{\mathrm{prim}}
        \subseteq
        \mathfrak X_a^{\mathrm{prim}}
\]

that contains the explicit structured families imported from #84. Let

\[
        F_a^{\mathrm{aper}}(b)
        =
        F_a(b)\setminus F_{a,\mathrm{quot}}(b).
\]

A useful high-multiplicity extraction lemma should say:

If

\[
        |F_a^{\mathrm{aper}}(b)|>n^{B-1},
\]

then there exists a controlled-size sublist whose agreement hypergraph:

1. satisfies the required partition-connectivity condition;
2. has an associated reduced intersection matrix that is symbolically full
   rank;
3. becomes rank deficient after specialization to the smooth subgroup
   evaluation set \(H\).

The random-RS RIM framework establishes the analogous
bad-list-to-connected-hypergraph-to-rank-defect mechanism for generic/random
evaluation sets. Here the problem is to adapt the extraction to the primitive
incidence setting and then classify why the fixed smooth subgroup
specialization loses rank.

## Missing Lemma 2: Classification And Counting

**Status:** CONJECTURAL.

Every extracted rank-defect certificate should fall into one of two classes:

\[
        \text{quotient/folding structured}
        \qquad\text{or}\qquad
        \text{aperiodic exceptional}.
\]

The structured class should import the explicit #84 quotient/folding families
instead of recreating them. The aperiodic exceptional class needs a
quantitative counting theorem controlling:

1. the number of certificate templates;
2. the number of primitive shell points extending each template;
3. the total contribution after summing over exact shells.

Certificate extraction alone does not prove an \(n^B\) theorem. It must be
paired with a certificate-counting or fiber-extension bound.

## Candidate Theorem Shape

**Status:** CONJECTURAL.

For fixed \(\rho,B,\epsilon,\gamma\), assume the generated-field entropy
reserve and quotient-profile margin from the repaired locator theorem package.
To prove a final exponent \(B\), one needs a small exponent reserve for the
sum over shells and for the structured quotient/folding term. For example, it
would be enough to prove the following with some \(\theta>0\). For every exact
shell \(a\ge s\), suppose:

1. quotient/folding structured fibers have total contribution across all
   shells at most \(n^{B-\theta}\);
2. every aperiodic fiber larger than \(n^{B-1-\theta}\) yields a controlled
   high-multiplicity certificate;
3. all controlled aperiodic certificates have total extension count at most
   \(n^{B-1-\theta}\) per shell.

Then

\[
        L_s(b)=\sum_{a=s}^{n}|F_a(b)|\le O(n^{B-\theta})+O(n^{B-\theta})
\]

and hence \(L_s(b)\le n^B\) for sufficiently large \(n\), after adjusting
constants. The displayed exponents are illustrative; the important point is
that the shell sum and the structured quotient/folding term both require
explicit budget room.

This is not yet a proof. It is the point at which the remaining work is
cleanly separated into:

- structured quotient/folding import;
- high-multiplicity extraction;
- aperiodic rank-defect classification;
- quantitative certificate counting.

## Why This Is The Next Attack Point

The repaired theorem package and verifier already settle the statement-level
and finite-identity issues. More scanning can find examples, but it does not
close the theorem gap. The gap is now the following precise implication:

\[
        \text{large aperiodic fiber of }\pi_a
        \quad\Longrightarrow\quad
        \text{controlled rank/incidence certificate}.
\]

This note is meant to keep that proof target explicit so future scripts or
proof notes do not drift back to raw support counts or pivot-gauge sections.

## Next Work

1. Define the first quotient/folding structured sub-incidence imported from
   #84 in the \(\mathfrak X_a^{\mathrm{prim}}\) notation.
2. Formalize the agreement hypergraph for primitive shell sublists and specify
   the exact partition-connectivity parameter needed from the RIM framework.
3. Prove a small bounded-\(t\) extraction lemma in toy regimes, or find the
   first obstruction to such extraction.
4. Only after the certificate target is precise, add a sparse-syndrome scanner
   that emits candidate high-multiplicity certificates rather than raw counts.
