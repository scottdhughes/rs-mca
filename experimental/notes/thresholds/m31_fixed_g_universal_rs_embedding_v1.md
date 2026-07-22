---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Every base-field ordinary RS list of at most B_star distinct degree-less-than-d polynomials on an R-point boundary subset E0, at agreement at least m=d+w, embeds after one common constant translation as distinct nonanchors sharing one G in a base-field M31 boundary list viewed inside the ambient code. At size B_star this is an exact counterexample equivalence between the ordinary RS instance and the base-field fixed-G boundary subclass.
architecture: M31_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_V1
parent_payload_sha256: 006cde59ee0a9fc23f8f13c3dc9955c26732bdee86b4af943f06fffeb5dd572e
atom_or_cell: Direct threshold-equivalent fixed-G boundary diagnostic; no v4 atom value, owner transport, or signed-Xi payment.
quantifier: Every R-subset E0 of the deployed evaluation domain D, its complement S0, every 1<=d<=R-w, every received table r:E0->F_p, and every family of at most B_star distinct f_i in F_p[X] of degree less than d with agreement at least d+w.
projection_and_unit: Ordinary base-field RS codewords become distinct M31 nonanchor codewords around one received word; one zero anchor is added. The construction is internal to F_p and hence valid over the ambient F_{p^4} code.
claimed_bound: Exact embedding and route cut only. The ordinary RS upper B_star-1, the global split-rational incidence upper, and the M31 row remain unproved. Ledger movement is zero.
status: PROVED_FIXED_G_UNIVERSAL_BASE_FIELD_RS_EMBEDDING_ORDINARY_LIST_BOUND_OPEN
impact: ROUTE_CUT / EXACT_COUNTEREXAMPLE_ADAPTER
falsifier: An input ordinary RS list satisfying the declared size, degree, and agreement gates for which every allowed constant leaves fewer than m common nonzero S0 coordinates; a constructed fixed-G boundary pair violating a canonical gate or exact support identity; or any use of this adapter as an upper bound or v4 payment.
replay: Independent Python big-integer and finite-table checks, Sage polynomial reconstruction, proof-critical mutations, parent payload pin, and fresh proof review.
---

# M31 fixed-G universal base-field RS embedding

## Status

This note removes both restrictions left in the fixed-G observation of the
parent packet.  The ordinary received word need not be nowhere zero, and the
message polynomials need not initially be coprime to a split numerator.
One common constant translation makes the received word nowhere zero and
leaves enough coordinates of S_0 simultaneously nonzero for every message.
Choosing G on those coordinates then embeds the entire ordinary list into
one fixed-G boundary slice.

The result is an exact counterexample adapter, not an upper bound.  It proves
that the M31 row contains a full ordinary base-field Reed--Solomon
list-decoding problem as a subclass.  The M31 LIST row, the global
split-rational incidence theorem, and every unfilled v4 atom remain open.

## 1. Deployed parameters and ordinary-list input

Let

$$
p=2^{31}-1=2,147,483,647,
\qquad
D=S_0\mathbin{\dot\cup}E_0,
$$

with

$$
|S_0|=a=1,116,023,
\qquad
|E_0|=R=981,129,
$$

and

$$
K=1,048,576,
\qquad
w=a-K=67,447,
\qquad
B_*=2^{24}-1=16,777,215.
$$

Fix

$$
1\le d\le R-w,
\qquad
m=d+w\le R.                                         (1.1)
$$

Let r:E_0\to F_p be an arbitrary received table, and let

$$
f_1,\ldots,f_L\in F_p[X],
\qquad
\deg(f_i)<d,                                         (1.2)
$$

be distinct, where L\ge1.  The deployed consequence uses L\le B_*.  Assume
each f_i agrees with r on at least m coordinates of E_0.  No nonvanishing or
coprimality hypothesis is imposed.

Only R-subsets E_0 of the deployed domain D are asserted.  This note does
not claim the same adapter for evaluation sets outside D, nor does it turn a
random-puncture or generic-evaluation theorem into a uniform theorem on D.

## 2. Constant-translation avoidance lemma

### Lemma 2.1

Let F be a finite field of size q, let S and E be disjoint finite subsets of
F with |S|=A and |E|=N, and let r:E\to F be arbitrary.  Given L polynomial
functions f_i on S, suppose q>N.  There is a constant kappa in F such that

$$
r(x)+kappa\ne0\quad(x\in E),                         (2.1)
$$

and the bad set

$$
B_kappa=
\{y\in S:\text{ some }i\text{ has }f_i(y)+kappa=0\}
$$

satisfies

$$
|B_kappa|
\le
\left\lfloor
\frac{LA}{q-|r(E)|}
\right\rfloor
\le
\left\lfloor\frac{LA}{q-N}\right\rfloor.           (2.2)
$$

### Proof

Let

$$
C=F\setminus\{-r(x):x\in E\}.
$$

Then |C|\ge q-N.  For each kappa in C, bound the size of B_kappa by the number
of incidences (i,y) for which f_i(y)+kappa=0.  Summing over kappa in C gives

$$
\sum_{kappa\in C}|B_kappa|
\le
\sum_{kappa\in C}\sum_{i=1}^L\sum_{y\in S}
\mathbf 1_{f_i(y)+kappa=0}
\le LA,                                              (2.3)
$$

because a fixed pair (i,y) names at most the one constant
kappa=-f_i(y).  Some kappa in C therefore satisfies

$$
|B_kappa|
\le\left\lfloor LA/|C|\right\rfloor
\le\left\lfloor LA/(q-N)\right\rfloor.
$$

Membership in C gives (2.1).

The proof uses incidences only as an upper bound on bad points.  Replacing
the union B_kappa by the incidence count in the conclusion would reverse the
needed implication and is not permitted.

## 3. Exact deployed margin

At L=B_* the conservative allowed-constant count is

$$
p-R=2,146,502,518.                                  (3.1)
$$

Moreover

$$
B_*a=18,723,757,815,945
$$

and exact division gives

$$
18,723,757,815,945
=8,722(2,146,502,518)+1,962,853,949.                 (3.2)
$$

Consequently Lemma 2.1 supplies one kappa with at most 8,722 bad S_0
coordinates.  The simultaneous good set has size at least

$$
a-8,722=1,107,301
=R+126,172.                                         (3.3)
$$

Thus for every L\le B_* and every w+1\le m\le R there are at least m
coordinates of S_0 on which every f_i+kappa is nonzero.

The same uniform conclusion holds well beyond the deployed budget.  Since

$$
a-R=134,894,
$$

the largest L for which the conservative bound still guarantees m good
points uniformly for every w+1\le m\le R is

$$
L_{\max}
=\left\lfloor
\frac{(a-R+1)(p-R)-1}{a}
\right\rfloor
=259,450,259.                                       (3.4)
$$

Indeed the bad-point floors at L_{\max} and L_{\max}+1 are respectively
134,894 and 134,895.  The row uses only the much smaller L=B_*.

## 4. Universal fixed-G construction

### Theorem 4.1

Under (1.1)-(1.2), put

$$
q_r=p-|r(E_0)|\ge p-R.                              (4.0a)
$$

Suppose more generally that

$$
a-\left\lfloor\frac{La}{q_r}\right\rfloor\ge m.    (4.0)
$$

Then every ordinary list of size L embeds into one fixed-G base-field
boundary slice of the M31 code.  In particular this holds for every
L\le B_* and, by the conservative inequality q_r\ge p-R, uniformly over all
w+1\le m\le R for every L\le L_{\max}.

### Proof

Choose kappa by Lemma 2.1.  By (4.0), choose a set Z contained in
S_0 minus B_kappa with |Z|=m and put

$$
G=L_Z=\prod_{z\in Z}(X-z).                           (4.1)
$$

For every i set

$$
b_i=f_i+kappa,
\qquad
\widetilde r=r+kappa.                               (4.2)
$$

Then \deg(b_i)<d=m-w, the b_i remain distinct, and

$$
gcd(b_i,G)=1                                        (4.3)
$$

because b_i is nonzero at every root of G.  In particular no b_i is the
zero polynomial.  Also \widetilde r is nowhere zero on E_0.

Since G has no roots on E_0, define the nonzero table

$$
V(x)=G(x)/\widetilde r(x),\qquad x\in E_0,           (4.4)
$$

and interpolate it modulo the squarefree locator L_0=L_{E_0}.  This gives a
unit V in F_p[X]/(L_0).  For each i and x in E_0,

$$
G(x)-b_i(x)V(x)
=\frac{G(x)}{r(x)+kappa}\,(r(x)-f_i(x)).             (4.5)
$$

Therefore the full gcd

$$
H_i=gcd(L_0,G-b_iV)                                 (4.6)
$$

is exactly the locator of the ordinary agreement set of f_i and r, and

$$
\deg(H_i)\ge m.                                     (4.7)
$$

At every root of H_i one has

$$
b_i(x)=f_i(x)+kappa=r(x)+kappa\ne0,
$$

so gcd(b_i,H_i)=1 as well.  Thus the individual denominator-unit gate and,
by the realized common V, all pairwise Wronskian gates from the parent
packet hold automatically.

Equations (4.1), (4.3), \deg(b_i)<m-w, and (4.6)-(4.7) are all canonical
fixed-G boundary gates.

For completeness, let A_0=L_{S_0}, choose the unique degree-less-than-R
representative H_0=V^{-1} modulo L_0, and set

$$
U=A_0H_0,
\qquad
C_i=(A_0/G)b_i.                                     (4.8)
$$

Since \deg(A_0)=a and \deg(H_0)<R, one has \deg(U)<a+R=n.

The zero codeword agrees with U exactly on S_0.  The agreement support of
C_i is exactly

$$
(S_0\setminus Z)\mathbin{\dot\cup}Z(H_i),           (4.9)
$$

and its error support is exactly

$$
Z\mathbin{\dot\cup}(E_0\setminus Z(H_i)).           (4.9a)
$$

so it has size at least

$$
a-m+\deg(H_i)\ge a.                                 (4.10)
$$

Each C_i lies in the deployed dimension-K code because

$$
\deg(C_i)
<(a-m)+d
=a-w
=K.                                                 (4.11)
$$

If C_i=C_j, cancellation of the nonzero polynomial A_0/G gives b_i=b_j,
hence f_i=f_j.  Each C_i is nonzero because b_i is nonzero, so the L
nonanchors are distinct from one another and from the zero anchor.  All constructed
coefficients lie in F_p, so they also define codewords and a received word
over the ambient field F_{p^4}.

## 5. Exact threshold equivalence

### Corollary 5.1

Fix L and m satisfying the witness-independent deployed gate

$$
a-\left\lfloor\frac{La}{p-R}\right\rfloor\ge m.     (5.0)
$$

The following are equivalent.

1. For some R-subset E_0 of D and some 1\le d\le R-w, an ordinary base-field
   RS(E_0,d) ball contains at least L distinct codewords at agreement at
   least m=d+w.

2. A base-field M31 boundary ball, viewed inside the ambient F_{p^4} code,
   contains the zero anchor and at least L distinct nonanchors sharing one
   locator G.

At L=B_*, either condition supplies B_*+1 codewords in one deployed M31 ball
and refutes the claimed upper B_*.

### Proof

For 1 implies 2, select L ordinary codewords and apply Theorem 4.1.  For 2
implies 1, use the fixed-G table

$$
r_{G,V}(x)=G(x)/V(x),\qquad x\in E_0.
$$

The exact identity

$$
\deg(\gcd(L_0,G-b_iV))
=\operatorname{agr}_{E_0}(b_i,r_{G,V})               (5.1)
$$

turns the L canonical nonanchors into L distinct ordinary RS codewords
of degree less than d=m-w and agreement at least m.  Evaluation is
injective here because d<R=|E_0|.

This is an equivalence only for the fixed-G boundary subclass.  A general
M31 counterexample may use many G locators, so an ordinary-list upper does
not by itself exhaust the whole global split-rational residual.

### Corollary 5.2: necessary ordinary-list theorem

M31 row safety implies, uniformly for every R-subset E_0 of D and every
1\le d\le R-w,

$$
\max_r
\#\{f\in F_p[X]:\deg(f)<d,\ \operatorname{agr}_{E_0}(f,r)\ge d+w\}
\le B_*-1=16,777,214.                               (5.2)
$$

The field in (5.2) is F_p and the evaluation set is a boundary subset of the
fixed deployed domain D.  It is not an assertion about every evaluation set
in F_p or about arbitrary F_{p^4}-valued received words.

Define the exact ordinary obstruction

$$
M_{\mathrm{ord}}=
\max_{\substack{E_0\subset D,\ |E_0|=R\\
1\le d\le R-w\\ r:E_0\to F_p}}
\#\{f\in F_p[X]:\deg(f)<d,\ \operatorname{agr}_{E_0}(f,r)\ge d+w\}.
                                                               (5.3)
$$

The construction proves the direct lower comparison

$$
B_{\mathcal C}^{\mathrm{list}}(a)
\ge1+\min(M_{\mathrm{ord}},B_*).                    (5.4)
$$

Thus M_{\mathrm{ord}}\ge B_* is already a direct row counterexample, while
M31 row safety forces M_{\mathrm{ord}}\le B_*-1.  The converse of the latter implication is not
claimed because a global M31 list may mix G locators.

## 6. Route cut and proof audit

The construction shows that neither of the two apparent fixed-G filters can
be used as a generic source of savings:

- nowhere-zero received data is obtained by one common translation;
- a split G with gcd(b_i,G)=1 for every list member is obtained from the
  same translation and the exact 126,172-coordinate reserve.

Thus the fixed-G branch already contains the full ordinary base-field RS
list problem in (5.2).  Any M31 closure must prove that uniform ordinary
list bound, exploit interactions between different G locators without
assuming they occur, use a source-bound CA/owner bridge, or refute the row.

The parent Johnson denominator

$$
m^2-R(d-1)
$$

is nonpositive for 72,859\le m\le908,270.  The new adapter proves that this is
not an artifact of the nowhere-zero or gcd filters: arbitrary ordinary
received words and lists enter the same fixed-G branch.

On the two positive-denominator wings the inherited fixed-G Johnson cap is
at most 174,019, strictly below B_*.  Consequently any ordinary list that
could refute the row through (5.4) must lie in the exact middle interval

$$
72,859\le m\le908,270,
\qquad
5,412\le d\le840,823.                               (6.1)
$$

Ledger movement and official endpoint movement are zero.  In particular,
the adapter does not prove (5.2), does not pay U_{\mathrm{list-int}}, and does not
close the global pairwise split-rational census.

Statement audited:

The implication chain from an arbitrary ordinary base-field RS list on a
deployed boundary subset to an actual fixed-G boundary list in the ambient
M31 code, and the reverse fixed-G identification at threshold B_*.

Dependencies:

- PROVED: the parent fixed-G agreement identity and exact boundary-list
  reconstruction.
- PROVED HERE: constant-translation avoidance, simultaneous coprimality,
  removal of received-word zeros, and threshold counterexample equivalence.
- UNPROVEN: the ordinary list upper (5.2), the global split-rational
  incidence upper, every new v4 atom payment, and M31 row safety.

Parameter dependence:

Every deployed margin uses exactly

$$
(p,a,R,K,w,B_*)
=(2147483647,1116023,981129,1048576,67447,16777215).
$$

Layer-cake and dyadic summability:

Not applicable.

Moment, Markov, and Chebyshev:

No moment or probabilistic inequality is used.  Lemma 2.1 is a finite exact
averaging argument over constants; its integer floor is retained.

Numerical evidence:

Small-field exhaustive controls may falsify the algebra and off-by-one
gates.  They are not evidence for the unproved deployed ordinary-list upper.

Literature search:

After (5.2) was frozen, targeted TheoremSearch and outside searches returned
Johnson-radius theorems, folded/subcode results, and existence or random-
puncturing results.  None had the required quantifier over every R-subset
E_0 of the fixed deployed domain, so no external list theorem is imported
into this proof or promoted into a bound.

Verdict:

YELLOW.  The universal fixed-G embedding is GREEN; the necessary ordinary
RS upper, the global M31 residual, and the row remain open.

## 7. Maximal successor

Attack (5.2) as the exact necessary theorem, uniformly over every R-subset
E_0 of the deployed domain and every 1\le d\le R-w.  A direct proof must go
beyond the Johnson-negative middle interval and cannot rely on random
puncturing, generic evaluation points, nowhere-zero centers, or the
split-numerator coprimality filter without an explicit uniform transfer.

In parallel, the only architecture-level escape is a source-bound CA-to-list
or cross-G aggregation theorem that actually exhausts the direct boundary
census.  Another fixed-G rank calculation cannot remove the ordinary RS
subproblem proved here.
