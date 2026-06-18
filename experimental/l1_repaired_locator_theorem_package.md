# L1 Repaired Locator Theorem Package

- **Status:** PROVED / COUNTEREXAMPLE / EXPERIMENTAL /
  CONJECTURAL / AUDIT, with each item labeled below.
- **Agent/model:** Codex.
- **Date:** 2026-06-18.
- **Scope:** Paper B L1 arbitrary received-word locator repair package. This
  note does not edit Papers A-D. It proves exact reductions to the
  Reed-Solomon list, but does not assert a positive worst-case polynomial
  list-size theorem, MCA theorem, line-decoding theorem, or protocol-safety
  consequence.

## Purpose

This note pivots the L1 arbitrary-word work away from gauge selection as the
main theorem route. The raw support fiber remains useful, but it is not the
right theorem-level object for arbitrary received words: it counts support
subsets with multiplicity. The corrected package separates three objects.

1. **Statement object:** the image/codeword fiber, which equals the actual
   Reed-Solomon list.
2. **Algebraic object:** exact maximal agreement shells encoded by a primitive
   locator-cofactor incidence system.
3. **Analytic object:** sparse syndrome/coset-weight fibers.

The current coefficient-gauge probes should be preserved as
EXPERIMENTAL / AUDIT negative evidence, not promoted to a canonical theorem
mechanism.

## Setup

Let \(H\subseteq \mathbb F_q\) be a set of size \(n\), usually a smooth
multiplicative subgroup, and put

\[
        \Omega_H(X)=\prod_{x\in H}(X-x).
\]

For \(d\ge 0\), write

\[
        V_d=\{f\in \mathbb F_q[X]: \deg f<d\}.
\]

Let

\[
        C=\operatorname{RS}[\mathbb F_q,H,k]
\]

be the Reed-Solomon code of evaluations on \(H\) of polynomials in \(V_k\).
Fix \(k<s\le n\). For \(U\in V_n\) and \(P\in V_k\), define the agreement
set and agreement size

\[
        A_P(U)=\{x\in H:U(x)=P(x)\}, \qquad a_P(U)=|A_P(U)|.
\]

For \(S\subseteq H\), write

\[
        L_S(X)=\prod_{x\in S}(X-x).
\]

## Coset Invariance

**Status:** PROVED.

For \(R\in V_k\), translation by \(R\) identifies the repaired list fibers:

\[
        \operatorname{ListFib}_{U+R}(s)
        =
        R+\operatorname{ListFib}_U(s),
\]

where the right side means \(\{P+R:P\in\operatorname{ListFib}_U(s)\}\).
Consequently,

\[
        N_a(U+R)=N_a(U)
        \qquad\text{and}\qquad
        R_t(U+R)=R_t(U)
\]

for the exact agreement and raw moment quantities defined below. Thus the
cardinalities depend only on the coset

\[
        [U]\in V_n/V_k.
\]

Indeed, \(P\) agrees with \(U\) exactly where \(P+R\) agrees with \(U+R\).
For raw supports,

\[
        (U+R)\bmod L_S=(U\bmod L_S)+R
\]

because \(\deg R<k<s\). Hence the degree-\(<k\) support condition is
unchanged by adding \(R\).

## Repaired Statement Object

Define the actual arbitrary-word list fiber

\[
        \operatorname{ListFib}_U(s)
        =
        \{P\in V_k:a_P(U)\ge s\}.
\]

Define the image locator fiber

\[
        \operatorname{ImgFib}_U(s)
        =
        \left\{
        U\bmod L_S:
        S\in \binom Hs,\ \deg(U\bmod L_S)<k
        \right\}.
\]

### Proposition 1: Image Fiber Equals The List

**Status:** PROVED.

For every \(U\in V_n\) and \(k<s\le n\),

\[
        \operatorname{ImgFib}_U(s)
        =
        \operatorname{ListFib}_U(s).
\]

Consequently,

\[
        |\operatorname{ImgFib}_U(s)|
        =
        \left|
        \operatorname{List}\left(\operatorname{ev}_H(U),1-\frac{s}{n}\right)
        \right|.
\]

#### Proof

If \(S\) is in the raw support fiber, put \(P=U\bmod L_S\). Then
\(\deg P<k\), and \(L_S\mid U-P\). Hence \(P\) agrees with \(U\) on every
point of \(S\), so \(a_P(U)\ge s\).

Conversely, if \(P\in V_k\) agrees with \(U\) on at least \(s\) points, choose
any \(s\)-subset \(S\subseteq A_P(U)\). Then \(L_S\mid U-P\). Since
\(\deg P<k<s=\deg L_S\), the remainder of \(U\) modulo \(L_S\) is exactly
\(P\). Thus \(P\in\operatorname{ImgFib}_U(s)\).

This proves the equality. The equality with the Reed-Solomon list is just the
definition of agreement radius \(1-s/n\). \(\square\)

## Raw Fiber Multiplicity Ledger

The old raw support object should not be deleted. Rename it as a moment
object. For \(k<t\le n\), define

\[
        R_t(U)=|\operatorname{RawFib}_U(t)|
\]

where

\[
        \operatorname{RawFib}_U(t)
        =
        \{S\in \binom Ht:\deg(U\bmod L_S)<k\}.
\]

For \(0\le a\le n\), define the exact-agreement shell count

\[
        N_a(U)=|\{P\in V_k:a_P(U)=a\}|.
\]

### Proposition 2: Binomial Moment Identity

**Status:** PROVED.

For every \(k<t\le n\),

\[
        R_t(U)=\sum_{a=t}^{n}\binom{a}{t}N_a(U).
\]

#### Proof

Fix a listed polynomial \(P\) with \(a_P(U)=a\). It contributes exactly the
\(\binom{a}{t}\) subsets \(S\subseteq A_P(U)\) of size \(t\). Since
\(t>k\), two distinct degree-\(<k\) polynomials cannot agree with \(U\) on the
same \(t\)-set: otherwise they agree with each other on more than \(k\) points.
Summing over exact agreement shells gives the identity. \(\square\)

### Binomial Inversion

**Status:** PROVED.

For \(a>k\), the moment identity can be inverted:

\[
        N_a(U)
        =
        \sum_{t=a}^{n}
        (-1)^{t-a}\binom{t}{a}R_t(U).
\]

Therefore the actual cumulative list size is

\[
        |\operatorname{ListFib}_U(s)|
        =
        \sum_{a=s}^{n}N_a(U)
        =
        \sum_{t=s}^{n}
        (-1)^{t-s}
        \binom{t-1}{s-1}R_t(U).
\]

This explains precisely why raw fibers are useful but cannot be used directly
as list sizes. They are binomial moments of the agreement-size distribution.

The inversion follows from the binomial identity

\[
        \binom bt\binom ta
        =
        \binom ba\binom{b-a}{t-a}
\]

and

\[
        \sum_{j=0}^{m}(-1)^j\binom mj=\mathbf 1_{m=0}.
\]

Indeed, substituting the moment identity into the inversion formula gives,
for each shell \(N_b(U)\), the coefficient

\[
        \sum_{t=a}^{b}
        (-1)^{t-a}\binom ta\binom bt
        =
        \binom ba
        \sum_{j=0}^{b-a}(-1)^j\binom{b-a}{j},
\]

which is \(1\) when \(b=a\) and \(0\) otherwise. Summing
\(N_a(U)\) over \(a\ge s\) gives the cumulative identity, using

\[
        \sum_{a=s}^{t}(-1)^{t-a}\binom ta
        =
        (-1)^{t-s}\binom{t-1}{s-1}.
\]

### Zero-Word Corollary

**Status:** COUNTEREXAMPLE / PROVED.

If \(U=0\), then the raw fiber satisfies

\[
        R_t(0)=\binom nt
\]

for all \(t\), because every \(t\)-support has zero remainder. But the actual
list fiber has one element, the zero polynomial:

\[
        |\operatorname{ListFib}_0(s)|
        =
        |\operatorname{ImgFib}_0(s)|
        =
        1.
\]

The alternating inversion gives this value exactly:

\[
        \sum_{t=s}^{n}
        (-1)^{t-s}\binom{t-1}{s-1}\binom nt
        =
        1.
\]

Thus the raw support fiber overcounts by the binomial sub-support
multiplicity, while the repaired image/list object has the correct size.

## Primitive Locator-Cofactor Shells

The image fiber is the right theorem statement, but it is not the most natural
algebraic geometry object. For algebraic work, use exact maximal agreement
shells encoded by saturated locator-cofactor data.

For \(s\le a<n\), define \(\operatorname{PrimLoc}_U(a)\) as the set of triples
\((L,M,Q)\) satisfying

\[
        LM=\Omega_H,
        \qquad
        L,M\ \text{monic},
\]

\[
        \deg L=a,\qquad \deg M=n-a,\qquad \deg Q<n-a,
\]

\[
        U-LQ\in V_k,
        \qquad
        \operatorname{Res}_X(Q,M)\ne0.
\]

For \(a=n\), include the exceptional shell

\[
        (L,M,Q)=(\Omega_H,1,0)
\]

when \(U\in V_k\), and include no point otherwise.

The resultant condition is the maximality condition: \(Q\) must be nonzero on
the complement of the agreement set inside \(H\).

### Proposition 3: Exact-Shell Bijection

**Status:** PROVED.

For every \(s\le a\le n\), there is a bijection

\[
        \{P\in V_k:a_P(U)=a\}
        \longleftrightarrow
        \operatorname{PrimLoc}_U(a).
\]

For \(a<n\), it is given by

\[
        P
        \longmapsto
        \left(
        L_{A_P(U)},
        \frac{\Omega_H}{L_{A_P(U)}},
        \frac{U-P}{L_{A_P(U)}}
        \right).
\]

#### Proof

Given \(P\in V_k\) with \(A=A_P(U)\) and \(|A|=a<n\), the polynomial \(U-P\)
vanishes on \(A\), so

\[
        U-P=L_AQ
\]

for a unique \(Q\) with \(\deg Q<n-a\). On \(H\setminus A\), both \(U-P\) and
\(L_A\) are nonzero. Hence \(Q\) is nonzero on every root of
\(\Omega_H/L_A\). Equivalently,

\[
        \gcd(Q,\Omega_H/L_A)=1,
\]

or \(\operatorname{Res}_X(Q,\Omega_H/L_A)\ne0\). This gives a point of
\(\operatorname{PrimLoc}_U(a)\).

Conversely, given \((L,M,Q)\in\operatorname{PrimLoc}_U(a)\), put

\[
        P=U-LQ.
\]

The degree equations impose \(P\in V_k\). On the roots of \(L\), \(U=P\). On
the roots of \(M\), \(L\ne0\), and the resultant condition gives \(Q\ne0\), so
\(U\ne P\). Therefore \(A_P(U)\) is exactly the root set of \(L\), of size
\(a\). These two constructions are inverse.

The case \(a=n\) is exceptional. If \(U\in V_k\), the only exact full-agreement
polynomial is \(P=U\), represented by \((\Omega_H,1,0)\). If \(U\notin V_k\),
there is no full-agreement degree-\(<k\) polynomial. \(\square\)

Consequently,

\[
        |\operatorname{ListFib}_U(s)|
        =
        \sum_{a=s}^{n}
        |\operatorname{PrimLoc}_U(a)|.
\]

## Primitive Incidence Ideals

**Status:** AUDIT.

For \(s\le a<n\), introduce coefficient variables for monic polynomials
\(L\) and \(M\) of exact degrees \(a\) and \(n-a\), and for an arbitrary
polynomial \(Q\) of degree at most \(n-a-1\). Define the unsaturated incidence
ideal

\[
        I^0_{U,a}
        =
        \left\langle
        \operatorname{coeff}(LM-\Omega_H),
        \operatorname{coeff}_{\ge k}(U-LQ)
        \right\rangle,
\]

with the degree and monicity constraints imposed by the variable choices.
The exact primitive incidence is the quasi-affine set

\[
        X^{\operatorname{prim}}_{U,a}
        =
        V(I^0_{U,a})\cap D(\operatorname{Res}(Q,M)).
\]

For affine computation, introduce an auxiliary variable \(z\) and impose

\[
        J_{U,a}
        =
        I^0_{U,a}+\langle z\operatorname{Res}(Q,M)-1\rangle.
\]

Projection from \(V(J_{U,a})\) to the \((L,M,Q)\)-coordinates is a bijection
on \(\mathbb F_q\)-points onto \(\operatorname{PrimLoc}_U(a)\), because \(z\)
is uniquely determined by the nonzero resultant.

The saturation

\[
        I^0_{U,a}:\operatorname{Res}(Q,M)^\infty
\]

records the closure after localizing away from the resultant. It should not be
identified automatically with the open incidence set. In the present fixed
\(U\), \(a>k\) setting, however, \(V(I^0_{U,a})\) is finite: the equation
\(LM=\Omega_H\) gives finitely many \(L\), and for each \(L\) there is at most
one \(Q\), since two choices would give two degree-\(<k\) polynomials agreeing
with \(U\) on \(a>k\) points. Thus saturation removes the excluded
resultant-zero points set-theoretically in this fixed-fiber setting. The
auxiliary-variable model \(J_{U,a}\) remains the safest exact affine encoding.

This is a better proof object than a pivot gauge:

- It is order-free.
- It is independent of Gaussian-elimination pivot choices.
- It counts one point per listed polynomial in each exact shell.
- It encodes maximality through a standard open condition.
- It supports elimination, saturation, component analysis, and radical
  containment.
- Quotient-periodic structure can be described by explicit support-pattern
  strata or sub-incidences rather than hidden by a solver section.

The canonical selector remains a valid counting device, but it is secondary:
lexicographic selection is not naturally algebraic. Pivot gauges are even less
fundamental because they select sections of a generally nonunique certificate
space.

## Universal Primitive Incidence

**Status:** AUDIT / CONJECTURAL.

The fixed-\(U\) incidence above is finite, so quotient-periodic phenomena
should not be described too quickly as fixed-fiber components. The geometric
object needed for a local-limit theorem is the universal incidence over the
received-word quotient space

\[
        \mathcal B:=V_n/V_k\cong\mathbb A^{n-k}.
\]

For \(s\le a<n\), define

\[
        \mathfrak X_a^{\operatorname{prim}}
        =
        \left\{
        ([U],L,M,Q):
        \begin{array}{l}
        LM=\Omega_H,\\
        L,M\text{ monic},\\
        \deg L=a,\ \deg M=n-a,\ \deg Q<n-a,\\
        [U]=[LQ]\text{ in }V_n/V_k,\\
        \operatorname{Res}(Q,M)\ne0
        \end{array}
        \right\}.
\]

The full-agreement shell \(a=n\) is exceptional: it occurs only over the zero
coset \([U]=0\) and is represented by \((\Omega_H,1,0)\).

Let

\[
        \pi_a:\mathfrak X_a^{\operatorname{prim}}\longrightarrow\mathcal B
\]

be projection onto \([U]\). By coset invariance and the primitive-shell
bijection,

\[
        \pi_a^{-1}([U])\cong\operatorname{PrimLoc}_U(a).
\]

This is the correct uniform fiber-bound framework:

- fixed-\(U\) primitive shells are fibers of \(\pi_a\);
- large lists are high-cardinality fibers of \(\pi_a\);
- quotient structure should first be encoded as explicit support-pattern
  strata or sub-incidences;
- a local-limit theorem becomes a uniform bound on fibers after quotient
  contributions and aperiodic exceptional sets are separately budgeted.

## Sparse Syndrome Reformulation

**Status:** PROVED / CONJECTURAL.

Let \(y=\operatorname{ev}_H(U)\in\mathbb F_q^n\). Let \(M_C\) be a full-rank
parity-check matrix for \(C\), and put

\[
        z=M_Cy.
\]

For \(j\ge0\), define the syndrome weight fiber

\[
        A_j(z)
        =
        |\{e\in\mathbb F_q^n:\operatorname{wt}(e)=j,\ M_Ce=z\}|.
\]

### Proposition 4: Primitive Shells Are Syndrome-Weight Shells

**Status:** PROVED.

For every \(a\in[s,n]\),

\[
        |\operatorname{PrimLoc}_U(a)|=A_{n-a}(z).
\]

More precisely, there is a bijection

\[
        \operatorname{PrimLoc}_U(a)
        \longleftrightarrow
        \{e\in\mathbb F_q^n:M_Ce=z,\ \operatorname{wt}(e)=n-a\}.
\]

#### Proof

For \(a<n\) and \((L,M,Q)\in\operatorname{PrimLoc}_U(a)\), put

\[
        P=U-LQ,\qquad e=\operatorname{ev}_H(LQ).
\]

Then \(P\in V_k\), so

\[
        M_Ce=M_C\operatorname{ev}_H(U-P)=M_Cy=z.
\]

The vector \(e\) vanishes exactly at the roots of \(L\): it vanishes there
because of the factor \(L\), and it is nonzero at every root of \(M\) because
\(L\ne0\) and the resultant condition gives \(Q\ne0\). Hence
\(\operatorname{wt}(e)=n-a\).

Conversely, for \(a<n\), let \(e\) have syndrome \(z\) and weight \(n-a\).
Then
\(M_C(y-e)=0\), so \(y-e\) is a codeword. Since Reed-Solomon evaluation is
injective on \(V_k\), there is a unique \(P\in V_k\) with
\(\operatorname{ev}_H(P)=y-e\). Let \(A\subseteq H\) be the zero set of
\(e=\operatorname{ev}_H(U-P)\). Then \(|A|=a\). Put

\[
        L=L_A,\qquad M=\Omega_H/L,\qquad Q=(U-P)/L.
\]

Since \(U-P\in V_n\) vanishes on \(A\), this division is exact and
\(\deg Q<n-a\). The vector \(e\) is nonzero on \(H\setminus A\), so \(Q\) is
nonzero at every root of \(M\). Thus \(\operatorname{Res}(Q,M)\ne0\), and
\((L,M,Q)\in\operatorname{PrimLoc}_U(a)\). These constructions are inverse.

The case \(a=n\) is the exceptional full-agreement shell. The only possible
weight-\(0\) error is \(e=0\), which has syndrome \(z=0\). This occurs exactly
when \(U\in V_k\), and it corresponds to the exceptional point
\((\Omega_H,1,0)\).
\(\square\)

### Corollary 5: List Fibers Are Sparse Syndrome Balls

**Status:** PROVED.

Let \(r=n-s\). Then

\[
        |\operatorname{ListFib}_U(s)|
        =
        \sum_{a=s}^{n}|\operatorname{PrimLoc}_U(a)|
        =
        \sum_{j=0}^{r}A_j(z).
\]

### Exact Mean Over Syndromes

**Status:** PROVED.

There are \(q^{n-k}\) syndromes, and every weight-\(j\) vector lies in exactly
one syndrome fiber. Therefore

\[
        \frac{1}{q^{n-k}}\sum_z A_j(z)
        =
        q^{-(n-k)}\binom nj(q-1)^j.
\]

Consequently,

\[
        \frac1{q^{n-k}}
        \sum_{[U]\in V_n/V_k}
        |\operatorname{PrimLoc}_U(a)|
        =
        q^{-(n-k)}\binom na(q-1)^{n-a},
\]

because the induced map \(V_n/V_k\to\mathbb F_q^{n-k}\) sending \([U]\) to
the syndrome \(M_C\operatorname{ev}_H(U)\) is a bijection. Also,

\[
        \frac{1}{q^{n-k}}\sum_z
        \sum_{j=0}^{n-s}A_j(z)
        =
        q^{-(n-k)}
        \sum_{j=0}^{n-s}\binom nj(q-1)^j.
\]

At the first relevant shell \(s=k+\sigma\), set

\[
        r=n-s=n-k-\sigma.
\]

The terminal mean term is

\[
        q^{-(n-k)}\binom nr(q-1)^r
        =
        \binom n{k+\sigma}
        q^{-\sigma}
        \left(1-\frac1q\right)^r.
\]

Thus the exact syndrome-average baseline for the repaired object is the coset
Hamming-ball mean, not literally \(\binom ns/q^\sigma\). The latter has the
right entropy exponent, but it misses \((1-1/q)^r\), which can remain a
nontrivial constant when \(q=\Theta(n)\). This average alone gives no uniform
control over individual syndromes.

## Corrected Conjectural Paper B Target

**Status:** CONJECTURAL.

Fix \(0<\rho<1\), \(B>0\), \(\varepsilon>0\), and \(0<\gamma<B\). There
should be a constant \(C=C(\rho,B,\varepsilon,\gamma)\) such that, for all
sufficiently large smooth \(n\), the following holds.

Let

\[
        H\le\mathbb F_q^\times,\qquad |H|=n,\qquad
        \mathbb F_p(H)=\mathbb F_q.
\]

Thus the generated-field ledger is the ambient field in this first theorem
package:

\[
        q_{\operatorname{gen}}=q.
\]

Let

\[
        k=\rho n+O(1),\qquad s=k+\sigma.
\]

Assume

\[
        \sigma\ge C\frac{n}{\log_2 n},
\]

\[
        \sigma\log_2 q
        \ge
        (1+\varepsilon)\log_2\binom ns,
\]

and, using Paper B's logarithmic quotient profile,

\[
        \mathcal Q_H(\sigma/n)\le (B-\gamma)\log_2 n.
\]

Then, conjecturally, for every \(U\in V_n\),

\[
        |\operatorname{ImgFib}_U(s)|
        =
        |\operatorname{ListFib}_U(s)|
        \le n^B.
\]

Equivalently,

\[
        \sum_{a=s}^{n}|\operatorname{PrimLoc}_U(a)|\le n^B.
\]

This is a corrected arbitrary-word locator statement. It does not prove the
local limit and does not imply any MCA, line-decoding, curve-MCA, interleaved
list, or protocol-safety consequence without the separate ledgers required by
the repo instructions. The quotient-profile margin \(B-\gamma\) is included
so the quotient contribution does not consume the entire target \(n^B\) budget
before the aperiodic contribution is counted.

## Stronger Sparse-Syndrome Target

**Status:** CONJECTURAL.

A sharp local-limit theorem should work at the syndrome level after explicitly
removing or budgeting quotient-core structure. Define an overlap-safe quotient
core

\[
        \operatorname{QCore}_z(r)
        \subseteq
        \{e:M_Ce=z,\ \operatorname{wt}(e)\le r\}
\]

that contains all errors arising from proved quotient constructions. A
meaningful analytic target is

\[
        \sum_{j=0}^{r}A_j(z)
        \le
        q^{-(n-k)}
        \sum_{j=0}^{r}\binom nj(q-1)^j
        +
        |\operatorname{QCore}_z(r)|
        +
        n^{B_0}.
\]

Once the entropy term, quotient term, and aperiodic error are each
polynomially bounded, the corrected list theorem follows. This remains open.

## Direct Ideal / RIM Endgame

**Status:** CONJECTURAL.

The direct algebraic target should be:

> Every sufficiently large family of primitive locator-cofactor solutions
> either lies in explicitly classified quotient-periodic strata or produces a
> rank defect forbidden on the aperiodic locus.

For \(t\) distinct listed polynomials, take \(t\) copies

\[
        (L_i,M_i,Q_i),\qquad 1\le i\le t,
\]

sharing the same \(U\) or the same syndrome. Impose

\[
        L_iM_i=\Omega_H,\qquad
        U-L_iQ_i\in V_k,\qquad
        \operatorname{Res}(Q_i,M_i)\ne0,
\]

together with pairwise distinctness. Let

\[
        P_i=U-L_iQ_i
\]

and

\[
        A_i=A_{P_i}(U)=Z_H(L_i).
\]

The associated agreement hypergraph has vertex set \([t]\) and one labeled
hyperedge per \(x\in H\):

\[
        e_x=\{i\in[t]:x\in A_i\}
        =
        \{i:L_i(x)=0\}.
\]

The individual agreement sets \(A_i\) determine this incidence matrix; they
are not themselves the hyperedges.

The random-RS mechanism in Alrabiah--Guo--Guruswami--Li--Zhang
(Lemmas 2.3 and 2.8, and Theorem 2.11) suggests the following bridge:

- a bad average-radius configuration contains a sublist whose induced
  agreement hypergraph has the required weak partition-connectivity;
- the precise connectivity parameter and permissible sublist size must be
  carried from the cited lemma;
- that hypergraph gives a reduced intersection matrix;
- the RIM at the actual evaluation points is rank deficient;
- for weakly partition-connected hypergraphs, the symbolic RIM is full column
  rank.

Smooth subgroup domains are specializations of the symbolic evaluation
variables, and quotient constructions provide genuine rank-loss configurations
at those specializations. The smooth-domain target should therefore be:

\[
        \operatorname{RIM}_{\mathcal H}(H)\ \text{singular}
\]

implies either

1. the primitive locator tuple lies in an explicitly defined
   quotient-periodic stratum or sub-incidence; or
2. it lies in a quantitatively small aperiodic exceptional finite-field locus.

At the ideal level, let \(I_{\mathrm{bad},t}^{\mathrm{prim}}\) encode
primitive \(t\)-lists with the necessary rank defect, and let
\(I_K^{\mathrm{quot}}\) encode each active quotient template. The intended
point-set containment is

\[
        V(I_{\mathrm{bad},t}^{\mathrm{prim}})
        \subseteq
        \bigcup_K V(I_K^{\mathrm{quot}})
        \cup
        V(I_{\mathrm{exceptional}}).
\]

Equivalently, with

\[
        J_{\mathrm{quot}}=\bigcap_K I_K^{\mathrm{quot}},
\]

one would seek the corresponding reversed radical containment

\[
        \sqrt{I_{\mathrm{bad},t}^{\mathrm{prim}}}
        \supseteq
        \sqrt{J_{\mathrm{quot}}\cap I_{\mathrm{exceptional}}}.
\]

For a statement only about \(\mathbb F_q\)-points, formulate rational-point
containment explicitly or add the relevant Frobenius equations. Algebraic
closure containment may be stronger than the theorem needs.

**Warning:** radical containment is structural, not quantitative. Even a
perfect component classification does not by itself prove an \(n^B\) point
bound. The residual locus still needs a degree estimate, finite-field
point-count theorem, Fourier estimate, or rank-certificate count.

The missing quantitative bridge should be stated explicitly:

**Missing high-multiplicity certificate lemma.** If

\[
        |\operatorname{ListFib}_U(s)|>n^B,
\]

then there exists a sublist or rank certificate of controlled complexity whose
primitive support pattern is either quotient-periodic or belongs to a
quantitatively bounded exceptional class.

Without such a lemma, the RIM section is a structural research direction, not
yet a proof of the desired polynomial exponent. To rule out a list larger than
\(n^B\), one needs at least one of:

1. \(t\) growing with \(n\);
2. a compression theorem from super-\(n^B\) fibers to bounded-complexity
   witnesses;
3. a point-count or incidence-multiplicity estimate for the universal
   projection \(\pi_a\);
4. a certificate-counting argument converting high fiber multiplicity into a
   controlled RIM certificate.

## Decision On Gauge Work

**Status:** EXPERIMENTAL / AUDIT.

The current deterministic pivot-order gauge probes are useful negative
evidence, but they should not remain the main theorem path. The observed
behavior is:

- deterministic pivot order does not yield a stable coefficient law;
- pivot gauges choose sections of a nonunique certificate space;
- the theorem target should be invariant under the kernel of the certificate
  map;
- exhaustive split testing may strengthen the negative record but will not
  make a solver section intrinsic.

Preserve the existing canonical-gauge probe as EXPERIMENTAL / AUDIT. Stop
expanding the feature family unless a separate reason appears. Move the main
proof package to primitive shells and sparse syndrome fibers.

## Paper B Label Cross-References

This note is meant to support review around the following Paper B labels:

- `def:locator-fiber`
- `prop:arb-fiber`
- `prop:monomial-fiber`
- `thm:qcore`
- `conj:listprofile`
- `conj:arbitrary-local`
- `thm:conditional-list`
- `conj:final-locator`

It should be read together with:

- `experimental/l1_arbitrary_fiber_repair.md`
- `experimental/l1_arbitrary_fiber_repair_tex_patch.md`
- `experimental/l1_arbitrary_fiber_repair_checkpoint.md`
- `experimental/verify_l1_arbitrary_fiber_repair.py`

## Theorem / Counterexample Ledger

| Item | Status | Consequence |
|---|---|---|
| Raw support decomposition | PROVED | Raw fibers are binomial moments of exact agreement shells. |
| Raw universal polynomial bound | COUNTEREXAMPLE | \(U=0\) gives \(\binom ns\) raw supports and one list element. |
| Image-fiber/list equality | PROVED | Correct arbitrary-word theorem object. |
| Maximal-support/list equality | PROVED | Correct order-free support object for \(s>k\), proved in `experimental/l1_arbitrary_fiber_repair.md`. |
| Primitive locator-cofactor bijection | PROVED | Correct algebraic exact-shell object. |
| Primitive-shell/syndrome-weight-shell bijection | PROVED | Algebraic and analytic shells are the same fiber in different coordinates. |
| Binomial inversion to recover actual list size | PROVED | Preserves raw computations through an exact multiplicity ledger. |
| Exact-size shell alone | AUDIT | Insufficient by itself; must sum over every \(a\ge s\). |
| Universal primitive incidence | AUDIT / CONJECTURAL | Correct framework for uniform fiber bounds over \(V_n/V_k\). |
| Canonical selector | PROVED | Secondary exact fixed-size object, proved in `experimental/l1_arbitrary_fiber_repair.md`, but order-dependent and analytically awkward. |
| Monomial-prefix raw fibers | PROVED | Paper B has an exact support-to-codeword bijection in that lane, unchanged by this repair. |
| Quotient-core lower obstruction | PROVED | Must be budgeted separately in any positive theorem. |
| Gauge-based coefficient interpolation | EXPERIMENTAL / AUDIT | Negative evidence; no intrinsic coefficient law established. |
| Sparse-syndrome local limit | CONJECTURAL | The real quantitative arbitrary-word problem. |
| Quotient-stratum completeness | CONJECTURAL | Must show all large structured fibers come from listed templates. |
| Smooth-domain aperiodic RIM rank theorem | CONJECTURAL | Promising structural bridge to list bounds. |
| RS/MCA/protocol consequence | AUDIT | Not claimed; requires separate conversion and protocol ledgers. |

## Next Work

1. Convert the primitive-shell and syndrome-shell package into patch-ready
   Paper B blocks only after maintainer review.
2. Add a small checker for the binomial inversion identities using the existing
   tiny locator-fiber examples.
3. Define quotient-periodic primitive strata or sub-incidences
   \(I_K^{\mathrm{quot}}\) for the first nontrivial dyadic toy cases.
4. Formulate a first high-multiplicity certificate lemma in the universal
   incidence framework.
5. Build a sparse-syndrome toy scanner only after the statement object is
   settled, keeping it EXPERIMENTAL.
6. Keep generated experiments and theorem notes in separate commits.
