---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: A fixed 1911-point remainder in one complete T_2048 fiber and 544 moving complete fibers produce one deployed base-field received word whose complete quartic-field ball is boundary-only and contains at least 6,796,405 codewords. Under the declared first-match rule routing fixed-R quotient/remainder profiles by C1, every codeword in the certified structured subfamily is removed by or at C1 and therefore contributes zero to the post-C1 primitive-Q residual. Before first-match pruning it refutes every flat raw-tail baseline b>=28; the largest compatible baseline b=27 does not obtain a two-row below-cutoff consequence from the current aggregate Forney theorem.
architecture: M31_CHEBYSHEV_FIXED_REMAINDER_C1_BOUNDARY_SOURCE_ROUTE_CUT_V1
atom_or_cell: Exact realized boundary source removed by or at C1_QUOTIENT_REMAINDER; no numerical C1 upper payment, no U_Q payment, and no atom movement.
quantifier: The polynomial-fold lemma is field-generic under its displayed complete-fiber hypotheses; the numerical specialization is one existential received word in the deployed M31 list code.
projection_and_unit: Distinct codewords per received word. The structured floor is a certified subfamily of the complete boundary prefix fiber, not its exact total cardinality.
claimed_bound: M_R>=6,796,405 and T46>=6,796,360 for one deployed exact-boundary center; the proposed raw T46<=259,880 cap fails by 6,536,480. The moving-cutoff optimizer makes b=27 the largest flat raw baseline compatible with this source, but its 28-column aggregate Forney data certify only the first ordered partial degree below 67,447, not a two-row minor.
status: PROVED
impact: PROVED_C1_BOUNDARY_SOURCE_AND_RAW_ARCHITECTURE_ROUTE_CUT
falsifier: Any universal raw T46<=259880 theorem; any flat raw-baseline compiler with b>=28; or any claim that the current aggregate Forney index sum gives a two-row below-cutoff minor on the source-compatible 28-column packet.
replay: Standard-library Python normal/optimized checks and mutations, independent Sage finite-field replay, exact big-integer optimizer, strict schema/hash gates, and predecessor/source replays.
---

# M31 Chebyshev fixed-remainder exact C1 boundary source and raw route cut

## 1. Result

This packet adds the missing symbolic bridge behind the checked-in
`c=2048` fixed-remainder arithmetic.  It proves that the floor

\[
 \left\lceil\frac{\binom{1023}{544}}{p^{32}}\right\rceil
 =6{,}796{,}405
\tag{1.1}
\]

is realized by distinct codewords around one actual received word for the
deployed code over \(\mathbb F_{p^4}\).  The complete ball around that word is
one exact-agreement boundary prefix fiber; it has no interior codewords and
no extension-only codewords.

This is a lower source, not an upper payment.  Under the declared owner order,
the fixed-remainder structured subfamily is removed by or at C1
quotient/remainder; it is not a primitive Q parent.
It leaves the M31 list row open, but cuts two unqualified raw closure
architectures:

1. the raw bound \(T_{46}\le259880\) is false by at least \(6{,}536{,}480\);
2. no flat raw baseline simultaneously survives this source and obtains a
   two-row below-cutoff consequence from the current aggregate coupled-Forney
   theorem.

The correct successor for this route is

```text
M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL.
```

## 2. Fixed-remainder polynomial-fold theorem

Let \(\mathbb B\subseteq\mathbb F\) be finite fields, let
\(D\subseteq\mathbb B\), and let \(\phi\in\mathbb B[X]\) be monic of
degree \(c\).  Assume the restriction

\[
 \phi:D\longrightarrow Q:=\phi(D)
\]

has complete fibers of size \(c\).  Put \(N=|Q|\).  Fix
\(\beta_0\in Q\), a set

\[
 R_0\subseteq\phi^{-1}(\beta_0),
 \qquad |R_0|=r<c,
\]

and integers \(0\le t<f\le N-1\).  For every
\(E\in\binom{Q\setminus\{\beta_0\}}f\), write

\[
 P_{R_0}(X)=\prod_{x\in R_0}(X-x),
 \qquad
 V_E(Y)=\prod_{b\in E}(Y-b),
\]

and

\[
 L_E(X)=P_{R_0}(X)V_E(\phi(X)).
\tag{2.1}
\]

The roots of \(L_E\) in \(D\) are exactly

\[
 A_E=R_0\sqcup\phi^{-1}(E),
 \qquad |A_E|=A:=r+cf.
\tag{2.2}
\]

### Theorem 2.1 (fixed-remainder polynomial-fold exact boundary list)

Assume \(1\le K<A\le|D|\) and

\[
 r+c(f-t-1)<K.
\tag{2.3}
\]

Then there is a received word \(U\in\mathbb B^D\) and at least

\[
 \left\lceil
  \frac{\binom{N-1}{f}}{|\mathbb B|^t}
 \right\rceil
\tag{2.4}
\]

distinct codewords of \(\operatorname{RS}_{\mathbb F}(D,K)\) agreeing with
\(U\) on exactly \(A\) coordinates.  Moreover:

1. the structured agreement supports are precisely the sets (2.2);
2. the complete radius-\((|D|-A)\) list around \(U\) is the full depth-
   \((A-K)\) global locator-prefix fiber;
3. every codeword in that complete \(\mathbb F\)-list is defined over
   \(\mathbb B\); and
4. every member of the complete list has exact agreement \(A\), not merely
   agreement at least \(A\).

#### Proof

Bucket the \(f\)-sets \(E\) by the first \(t\) nonleading coefficients of
the monic degree-\(f\) polynomial \(V_E\).  These coefficients lie in
\(\mathbb B^t\), so one bucket has size at least (2.4).

For two members \(E,E'\) of one bucket,

\[
 \deg(V_E-V_{E'})\le f-t-1.
\]

Equation (2.1) therefore gives

\[
 \deg(L_E-L_{E'})
 \le r+c(f-t-1)<K.
\tag{2.5}
\]

All locators in the bucket consequently have the same coefficients in
degrees \(K,K+1,\ldots,A\).  Let \(U(X)\) be this common high-degree part,
with lower coefficients set to zero.  It is monic of degree \(A\) and belongs
to \(\mathbb B[X]\).  For each bucket member put

\[
 c_E(X)=U(X)-L_E(X).
\tag{2.6}
\]

By (2.5), \(\deg c_E<K\).  Equation (2.6) shows that its agreement set with
\(U|_D\) is exactly the root set (2.2).  The codewords are distinct: equality
of two evaluations would give equality of two degree-less-than-\(K<|D|\)
polynomials, hence equality of their locators and root sets, and then
uniqueness of the complete-fiber-plus-fixed-remainder decomposition gives
\(E=E'\).

The exact locator-prefix/list bijection identifies the complete list with the
full depth-\((A-K)\) prefix fiber.  Finally, for any
\(c\in\mathbb F[X]_{<K}\), the polynomial \(U-c\) is monic of degree \(A\).
If it has at least \(A\) roots in \(D\), it has exactly \(A\) and equals the
monic locator of those roots, which lies in \(\mathbb B[X]\).  Thus
\(c=U-L_S\in\mathbb B[X]\), proving both target-field descent and exact
boundary agreement.  \(\square\)

## 3. Deployed Chebyshev specialization

Put

```text
p       = 2^31-1          = 2,147,483,647,
n       = 2^21            = 2,097,152,
K       = 2^20            = 1,048,576,
A       = 1,116,023,
R       = n-A             = 981,129,
w       = A-K             = 67,447,
B*      = floor(p^4/2^100)= 16,777,215.
```

The deployed standard-position M31 twin-coset \(x\)-domain
\(D\subseteq\mathbb F_p\) has complete \(2048\)-point fibers under
\(T_{2048}\).  Its leading coefficient is \(2^{2047}\in\mathbb F_p^\times\);
divide by it to obtain a monic map \(\phi\) with the same fibers.  Then

\[
 c=2048,
 \quad N=1024,
 \quad r=1911,
 \quad f=544,
 \quad t=32.
\tag{3.1}
\]

The identities

\[
 1911+2048\cdot544=1{,}116{,}023=A,
\]

\[
 32\cdot2048+1911=67{,}447=w
\tag{3.2}
\]

and the strict degree gate

\[
 1911+2048(544-32-1)
 =1{,}048{,}439
 =K-137<K
\tag{3.3}
\]

verify every hypothesis of Theorem 2.1.  It follows that one
\(U\in\mathbb F_p^D\) has

\[
 M_R(U)
 =|\mathcal L_R(U)|
 \ge6{,}796{,}405.
\tag{3.4}
\]

The equality in (3.4) is between the complete list and its sole boundary
layer, not between the complete list and the displayed lower floor.  The
actual value of \(M_R(U)\) may be larger than \(6{,}796{,}405\).

### 3.1 Exact C1 owner classification and upstream correction

The structured bucket fixes the same remainder \(R_0\) for every \(E\).
Since

\[
 |R_0|=1911<2048,
 \qquad 1911\le w=67447,
\]

the exact quotient--remainder normal form QR2 identifies it as one fixed-
remainder quotient-prefix fiber.  The same classification is visible on the
error supports.  Put

\[
 E'=Q\setminus(E\sqcup\{\beta_0\}),
 \qquad
 R'=\phi^{-1}(\beta_0)\setminus R_0.
\]

Then

\[
 D\setminus A_E=\phi^{-1}(E')\sqcup R',
\]

with

\[
 |E'|=1024-1-544=479,
 \qquad |R'|=2048-1911=137,
\]

and exactly

\[
 479\cdot2048+137=981129=R.
\tag{3.5}
\]

Both descriptions are fixed-(R), complete-fiber-plus-remainder profiles
satisfying the QR2 hypotheses.  The agreement bucket is a single depth-(w)
QR2 quotient-prefix fiber; the complement description is the corresponding
(s=11) fixed-(R) C1 profile.  Under the declared first-match convention,
every codeword in the certified structured subfamily is removed by or at
`C1_QUOTIENT_REMAINDER`, so that subfamily contributes zero to the post-C1
primitive-Q residual.

This corrects the packet's initial Q-parent framing after the upstream audit
of [PR #1032](https://github.com/przchojecki/rs-mca/pull/1032), exact head
`a843a8f7930054617ef1d94169a4a9d3422cb909`, which independently classifies
all fixed-remainder dyadic scales and includes \(c=2048\).  The new content
here is the received-word/codeword realization and the raw architecture cut;
PR #1032 explicitly makes no such realization claim.  QR2 does **not** show
that every arbitrary support in the complete global prefix fiber is removed
by or at C1 under the declared first-match convention,
and neither packet supplies the missing numerical C1 upper payment.

## 4. Exact chronology specialization

For this degree-\(A\) center,

\[
 N_{\rm low}=0,
 \qquad M_j=0\quad(j<R),
\tag{4.1}
\]

so the source-adapter occupancy quantities are

\[
 T_{46}=M_R-45,
 \qquad
 \Delta_{46}=3730+45(366969-1)=16{,}517{,}290,
\tag{4.2}
\]

and

\[
 \Xi_{46}=M_R-16{,}517{,}335.
\tag{4.3}
\]

Equation (3.4) gives

\[
 T_{46}\ge6{,}796{,}360
 =259{,}880+6{,}536{,}480.
\tag{4.4}
\]

Thus the raw theorem \(T_{46}\le259880\) is false.  In contrast, the signed
target

\[
 \Xi_{46}\le259880
\]

is, on this center, exactly

\[
 M_R\le16{,}777{,}215=B^*.
\tag{4.5}
\]

These are pre-first-match raw occupancy quantities.  Under the declared
first-match convention, the displayed lower floor comes from a structured
family removed by or at C1, so it is not a lower
bound on the post-C1 primitive-Q residual and none of (4.2)--(4.4) is a ledger
payment.  The complete list is still the full global boundary-prefix fiber,
but its arbitrary non-fixed-remainder supports are not classified here.  The
active v4 ledger has no negative-refund atom, so (4.2) cannot be entered as a
negative charge.

## 5. Sharp flat-baseline optimizer

Within the current moving-cutoff compiler, the source also cuts every flat
raw-tail baseline at least 28, even if its low-weight cutoff is optimized.

For a cutoff \(J\), let \(P(J)\) be the exact integer packing cap for all
weights at most \(J\), obtained from the balanced pair-incidence inequality.
For a flat baseline \(b\), put

\[
 S_b(J)=B^*-P(J)-b(R-J).
\tag{5.1}
\]

A proposed raw-tail theorem

\[
 \sum_{j>J}(M_j-b)_+\le S_b(J)
\tag{5.2}
\]

must accommodate the actual center above, for which its left side is at least
\(6{,}796{,}405-b\).

The exact scan covers all 89,955 cutoffs from \(K/2\) through the last
positive-denominator row and reproduces the frozen source digest
`bed6d505...1815763`.  Its transition is:

| baseline \(b\) | first optimal \(J\) | \(P(J)\) | best safe raw cap | source floor | margin |
|---:|---:|---:|---:|---:|---:|
| 27 | 614134 | 2835 | 6865515 | 6796378 | +69137 |
| 28 | 614137 | 2916 | 6498523 | 6796377 | -297854 |
| 29 | 614139 | 2972 | 6131533 | 6796376 | -664843 |
| 45 | 614160 | 3730 | 259880 | 6796360 | -6536480 |

For each fixed \(J\), the compatibility margin decreases strictly with \(b\)
because \(R-J-1>0\).  Therefore the failure at \(b=28\) proves that every
\(b\ge28\) is incompatible.  Baseline 27 is the largest not refuted by this
source.  Compatibility is not a proof of (5.2).

## 6. Aggregate Forney route cut

The coupled joint-kernel theorem applies to every \(m\)-column subpacket of
the complete boundary layer.  Its \(m-2\) ordered indices have total at most

\[
 S=2R-K-1=913681,
 \qquad D_0\ge K-R=67447.
\tag{6.1}
\]

For the source-compatible baseline \(b=27\), a marked packet has \(m=28\)
columns and 26 joint indices.  Exact ordered balancing gives

\[
 \nu_1\le35141<67447,
 \qquad
 \nu_1+\nu_2\le70282>67447.
\tag{6.2}
\]

Thus the aggregate theorem certifies one ordered partial degree below the
source cutoff, but it does not certify a two-row minor there.  Baseline 28
still gives only

\[
 \nu_1+\nu_2\le67680>67447.
\]

Two-row control first appears at baseline 29, with 30 columns and

\[
 \nu_1+\nu_2\le65262<67447,
\tag{6.3}
\]

but every baseline at least 28 is already refuted by Section 5.  Hence no
flat raw-tail baseline simultaneously

1. survives the exact \(c=2048\) boundary source; and
2. obtains a two-row below-cutoff consequence from the current aggregate
   Forney theorem.

This cuts the **unqualified flat raw tail plus aggregate Forney**
architecture.  It does not cut a chronology-correct C1 payment, signed
cross-weight refunds, stronger geometry at baseline 27, or a direct row-sharp
Q theorem.

## 7. Nonclaims and next maximal target

This packet does not claim:

- that \(6{,}796{,}405\) is the exact complete-list size;
- an M31 counterexample or an above-budget received word;
- a row-sharp Q upper bound;
- a numerical upper payment for the C1 quotient/remainder cell;
- that every codeword in the complete global prefix fiber is removed by or at
  C1 under the declared first-match convention;
- a payment of the variable-remainder/orientation residual;
- an integer value for \(U_Q\), \(U_{\rm list-int}\), \(U_{\rm ext}\), or
  high \(U_{\rm new}\);
- an arbitrary-boundary-to-Q adapter;
- that the adverse abstract Forney index distribution is geometrically
  realized;
- any additive stacking of different Chebyshev scales;
- an endpoint, official score, stable-paper theorem, or Lean change.

The maximal surviving attack is now a joint owner/residual problem.  First,
obtain a numerical codeword payment for the C1 quotient/remainder cell that
accommodates this \(6{,}796{,}405\)-member realized source.  In parallel,
exhaust the `M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL`: the remainder must
vary with the complete-fiber choice, have total partial occupancy at least the
fold degree, or carry a transversal/local-coset orientation not covered by
the fixed-\(R\) theorem.  Under the same declared first-match convention, a
fixed-remainder \(c=1024\) paired-prefix family is also removed by or at C1
and is not the next primitive-Q target.  Every genuine residual
component must receive a chronology-valid payment, a budget-fitting
attained-image bound, or an explicit primitive route cut.

## 8. Replay and provenance

The companion Python verifier recomputes the exact binomial floor, the full
moving-cutoff scan, all baseline transitions, the ordered Forney bounds, and
an exhaustive `GF(17)` fixed-remainder prefix fiber.  The Sage verifier
independently reconstructs the finite-field locators, received word,
codewords, exact supports, and deployed big integers.  The manifest binds the
domain theorem, exact prefix-list theorem, fixed-remainder arithmetic source,
v4 chronology/admissibility sources, rank-46 optimizer, and immediate
predecessor.

All computations are finite and exact.  There is no analytic layer-cake,
dyadic summability, moment, Markov, or probabilistic Chebyshev step;
“Chebyshev” denotes the folding polynomial.
