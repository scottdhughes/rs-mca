---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: For every feasible c=2048 occupancy profile there exists a separate fixed-multipartial exact-boundary source.  The certified floors prove that 141 bi-deep profiles realize at least 30 codewords; 18 require width 30 for the present below-cutoff theorem, 123 already admit width 29, and one additional floor-29 profile gives 124 width-29 and 142 profiles certified by the source-threshold criterion.  Profile (1,1) has floor 1693898.  Separately, one deployed arbitrary received word has two exact fixed-remainder (0,0) face codewords whose actual monic agreement and error locators have distinct prefixes, refuting their identification with one locator-prefix target by a common translation or any operation that leaves those supports literally fixed.
architecture: M31_C2048_MULTIPREFIX_30CARRIER_ACTIVATION_ROUTE_CUT_V1
partition_digest: CERTIFICATE_BOUND; no ledger atom assigned
atom_or_cell: C1_BOUNDARY / M31_C2048_BIDEEP_30COLUMN_OWNER
quantifier: Exact symbolic deployed constructions over F_p, hence also over F_(p^4); the fixed-template source theorem applies separately to every feasible c=2048 occupancy profile.
projection_and_unit: Distinct exact-boundary codewords per received word and their monic agreement/error locators; no slope projection.
claimed_bound: 1693898 codewords in one actual (1,1) bi-deep profile; the exact certified-floor sufficient-criterion histogram is 124 at q=29 plus 18 at q=30; literal support-preserving identification of the constructed pair's actual monic locator prefixes is impossible.
status: PROVED
impact: NEW_BIDEEP_PROFILE_FLOOR / ROUTE COUNTEREXAMPLE
falsifier: Failure of the fixed-template degree gate or exact-support construction, a profile-census mismatch, equality of either asserted locator prefix, or a support-preserving common translation that changes a monic locator.
replay: Python exact census, canonical certificate and mutations; independent Sage finite-field constructions.
---

# M31 `c=2048` multiprefix and 30-carrier activation route cut

## Status

```text
PROVED EXACT DEPLOYED SOURCES AND ROUTE CUTS
(1,1) 30-carrier terminal genuinely populated = true
literal common monic-locator-prefix identification = false
ledger movement = 0
row closed = false
```

This packet attacks both gates left by the exhaustive occupancy atlas.  It
does not pay either gate.  Instead it proves that two tempting eliminations
are unavailable:

1. the bi-deep residual cannot be closed by a universal cap of 29 codewords
   per profile, because one actual deployed base-field word has at least
   `1,693,898` codewords in profile `(u,v)=(1,1)`;
2. the constructed C1-shaped face pair cannot be identified with one common
   actual-monic-locator-prefix fiber by a common translation or an operation
   leaving its supports literally fixed, even
   when the two codewords have the same fixed remainder in both orientations.

The corrected target is a fixed-syndrome, multiprefix, partial-template
incidence/payment.  The result is a route cut and a new profile-level source
floor, not an upper bound or ledger payment.

## 1. Deployed row

Put

\[
 p=2^{31}-1,
 \quad n=2^{21}=2097152,
 \quad K=2^{20}=1048576,
\]
\[
 A=1116023,
 \quad R=n-A=981129,
 \quad w=A-K=67447,
\]
\[
 B_*=\left\lfloor\frac{p^4}{2^{100}}\right\rfloor=16777215.
\tag{1.1}
\]

Let \(D\subseteq\mathbb F_p\) be the deployed domain and let the monic
normalization \(\phi\) of \(T_{2048}\) split it into \(N=1024\) complete
fibers of size \(c=2048\).  Every construction below is over
\(\mathbb F_p\), and therefore remains a construction for the deployed code
over \(\mathbb F_{p^4}\).

## 2. Fixed-multipartial-template polynomial-fold source

The fixed-remainder source used only one partial fiber.  The same polynomial
argument works with an arbitrary fixed collection of partial fibers.

### Theorem 2.1 (fixed multipartial template)

Let \(\mathbb B\) be a finite field, let \(D\subseteq\mathbb B\), fix
\(0<K\le A\le |D|\), and suppose a monic degree-\(c\) polynomial
\(\phi\in\mathbb B[X]\) maps \(D\) onto \(Q\) with
complete fibers of size \(c\).  Fix distinct partial-fiber labels
\(H_0\subseteq Q\), \(|H_0|=h\), and a set

\[
 P\subseteq\phi^{-1}(H_0)
\]

meeting every fiber over \(H_0\) in between one and \(c-1\) points.  Put
\(r=|P|\).  Fix \(f\le |Q|-h\), and suppose

\[
 A=r+cf,
 \qquad 0\le t\le f.
\tag{2.1}
\]

For \(E\in\binom{Q\setminus H_0}{f}\), write

\[
 V_E(Y)=\prod_{b\in E}(Y-b)
       =Y^f+v_1(E)Y^{f-1}+\cdots+v_f(E)
\]

and bucket the sets \(E\) by
\((v_1(E),\ldots,v_t(E))\).  If \(t<f\), assume

\[
 r+c(f-t-1)<K.
\tag{2.2}
\]

Then one received word for \(\operatorname{RS}_{\mathbb B}(D,K)\) has at
least

\[
 \left\lceil
   \binom{|Q|-h}{f}|\mathbb B|^{-t}
 \right\rceil
\tag{2.3}
\]

distinct codewords at exact agreement \(A\).  Its complete radius-
\((|D|-A)\) ball is boundary-only.  When \(t=f\), the coefficient map is
injective and (2.3) is interpreted one bucket at a time; the construction
still gives one exact-boundary codeword.

### Proof

Choose a nonempty coefficient bucket \(\eta=(\eta_1,\ldots,\eta_t)\) of
maximum size and put

\[
 U_{P,\eta}(X)=L_P(X)
 \left(
   \phi(X)^f+\sum_{i=1}^t\eta_i\phi(X)^{f-i}
 \right).
\tag{2.4}
\]

For every \(E\) in that bucket, the locator

\[
 L_E(X)=L_P(X)V_E(\phi(X))
\tag{2.5}
\]

has simple roots exactly

\[
 S_E=P\sqcup\phi^{-1}(E).
\]

The first \(t\) quotient coefficients cancel in
\(U_{P,\eta}-L_E\).  Hence, if \(t<f\),

\[
 \deg(U_{P,\eta}-L_E)
 \le r+c(f-t-1)<K.
\tag{2.6}
\]

If \(t=f\), equality of all coefficients fixes \(E\), and the difference is
zero.  Thus

\[
 c_E=(U_{P,\eta}-L_E)|_D
\]

is a codeword.  The received word \(U_{P,\eta}|_D\) differs from it by the
locator \(L_E\), so its agreement set is exactly \(S_E\).  Different
quotient sets give different locators and therefore different degree-
less-than-\(K\) polynomials; evaluation is injective because
\(K\le |D|\), so the codewords are distinct.
Pigeonhole gives (2.3).

Finally \(U_{P,\eta}\) is monic of degree \(A\).  Subtracting any
degree-less-than-\(K\) polynomial leaves a nonzero degree-\(A\) polynomial,
which has at most \(A\) roots.  No codeword has more than \(A\) agreements.
\(\square\)

If a literal canonical high-part center is desired, subtract the degree-
less-than-\(K\) truncation of \(U_{P,\eta}\) from both the center and every
explaining codeword.  This common codeword translation leaves every support,
locator, and the identity \(Y-P=L_S\) unchanged.

This theorem fixes the entire partial template \(P\); it does not claim that
an arbitrary 30-codeword frame has a common partial template.

## 3. Exact deployed profile census and carrier activation

For the occupancy parameters of the predecessor packet,

\[
 h=u+v+1,
 \qquad f=z=544-v,
 \qquad r=1911+2048v,
\tag{3.1}
\]

and the available quotient-label count is

\[
 N-h=1023-u-v.
\tag{3.2}
\]

Every feasible profile supplies a partial template \(P\): the feasibility
inequalities are exactly the assertion that \(r\) is a sum of \(h\)
integers in \([1,2047]\).

For \(f>32\), take \(t=32\).  The degree bound is uniform:

\[
 r+2048(f-33)
 =A-33\cdot2048
 =1048439
 =K-137<K.
\tag{3.3}
\]

For \(f\le32\), take \(t=f\); the full coefficient vector determines
\(E\) and the certified floor is one.  Thus every feasible profile has the
following exactly computed certified lower bound

\[
 \boxed{
 L_{u,v}=
 \left\lceil
   \binom{1023-u-v}{544-v}
   p^{-\min(32,544-v)}
 \right\rceil .}
\tag{3.4}
\]

The deployed target-field ball has the same stronger property.  View the
base-field center \(U_{P,\eta}\) over \(\mathbb F_{p^4}\).  If a target-field
codeword \(P\) has at least \(A\) agreements, then \(U_{P,\eta}-P\) is monic
of degree \(A\) and has exactly \(A\) distinct roots in \(D\).  It therefore
equals their monic locator \(L_S\in\mathbb F_p[X]\), so
\(P=U_{P,\eta}-L_S\in\mathbb F_p[X]\).  Hence the complete deployed target-
field ball is boundary-only and all of its codewords are base-field-valued.

The quantifiers in (3.4) are

\[
 \text{for every feasible }(u,v)\text{ there exists a separately constructed }
 y_{u,v}.
\]

They are not a statement about every received word, and the different profile
floors are not simultaneously attained by one common word.

The complete exact-integer census gives:

```text
profiles with L_(u,v) >= 30:          177
  C1-shaped face profiles:             36
  bi-deep profiles:                   141

largest bi-deep certified floor:
  (u,v)=(1,1)
  h=3, f=543, r=3959
  L_(1,1)=1,693,898
```

The exact bi-deep staircase is

\[
\begin{array}{c|rrrrrrrrrrrrrrr}
u&1&2&3&4&5&6&7&8&9&10&11&12&13&14&15\\ \hline
\max v&18&17&15&14&13&12&11&9&8&7&6&5&3&2&1
\end{array}
\tag{3.5}
\]

and no bi-deep profile with \(u\ge16\) has floor at least 30.  At the last
entry of each row of (3.5), the floors are respectively

\[
 33,30,51,46,41,37,33,54,48,42,37,32,51,44,38.
\tag{3.6}
\]

The face \((0,0)\) specializes exactly to the predecessor floor
\(6{,}796{,}405\).

### Corollary 3.1 (the 30-carrier terminal is nonempty)

There is an actual deployed base-field received word with at least
`1,693,898` exact-boundary codewords in the single bi-deep profile `(1,1)`.
The error supports in this source share the fixed partial-error set

\[
 T=\phi^{-1}(H_0)\setminus P,
 \qquad |T|=137+2048u.
\tag{3.7}
\]

This fixed core survives in the determinantal divisor after the predecessor's
complete-layer core is divided.  More precisely, if the complete-layer core
is \(C_R\), then every reduced selected locator contains
\(T\setminus C_R\), so the gcd of the selected pair minors has degree at
least \(|T|-|C_R\cap T|\).  Lemma 4.1 of the predecessor therefore sharpens
on this source to

\[
 \sum\nu_i
 \le 2R-K-|C_R|-1-(|T|-|C_R\cap T|)
 \le913681-|T|.
\tag{3.8}
\]

For \((u,v)=(1,1)\), selecting any 30 and applying (3.8) gives two
independent coupled rows with combined degree at most

\[
 \left\lfloor\frac{2(913681-2185)}{28}\right\rfloor
 =65106<67447.
\tag{3.9}
\]

Among the 141 bi-deep profiles with floor at least 30, the 18 profiles with
\(u=1\) require 30 columns under the present degree information.  Their
corresponding 29-column upper is \(67518>67447\), so the current theorem does
not certify 29 there.  The remaining 123 profiles have \(u\ge2\), so 29
selected columns already give

\[
 \left\lfloor\frac{2(913681-(137+2048u))}{27}\right\rfloor
 \le67366<67447.
\tag{3.10}
\]

There is one further activation at the variable threshold:

\[
 L_{8,10}=29.
\tag{3.11}
\]

Since \(u=8\), (3.10) applies to all 29 members.  More exhaustively, define

\[
 q_{\min}(u)=\min\left\{q\ge4:
 \left\lfloor\frac{2(913681-(137+2048u))}{q-2}\right\rfloor<67447
 \right\}.
\tag{3.12}
\]

An exact scan of every bi-deep profile satisfying \(L_{u,v}\ge q_{\min}(u)\)
has histogram

\[
 \#\{q_{\min}=29\}=124,
 \qquad
 \#\{q_{\min}=30\}=18,
\tag{3.13}
\]

with no profile certified by this criterion having floor below 29.  Thus 141 profiles literally
realize at least 30 source codewords; among them 18 use \(q=30\) and 123 use
\(q=29\), while (3.11) supplies the one additional \(q=29\) source.  The 142
count is an exact census of this sufficient criterion and certifies at least
those 142 separate source constructions.  It does not prove that no other
profile can contain a carrier, is not a uniform arbitrary-word carrier theorem,
and still identifies no paid owner.

Therefore `M31_C2048_BIDEEP_30COLUMN_OWNER` cannot be discharged by proving
that the 30-column configuration is empty, nor by a universal profile cap of
29.  A chronology-valid owner, attained-image payment, or finer primitive
dichotomy is genuinely necessary.  The sharper 29-column source carrier for
\(u\ge2\) is a source-specific consequence of (3.7), not the unsupported
generic 29-column claim excluded by the predecessor.

## 4. A deployed fixed-remainder multiprefix obstruction

We next refute the proposed common-prefix normalization for arbitrary words
without changing profile or remainder data.

Fix one quotient label \(\beta_0\) and split its complete fiber as

\[
 \phi^{-1}(\beta_0)=A_0\sqcup T_0,
 \qquad |A_0|=1911,
 \qquad |T_0|=137.
\tag{4.1}
\]

Inside the remaining 1023 quotient labels choose \(J\) of size 65 and
partition the other 958 labels into \(P,Q\), each of size 479, with

\[
 \sum_{b\in P}b\ne\sum_{b\in Q}b.
\tag{4.2}
\]

Such a partition exists.  If an initial partition has equal sums, swapping
distinct \(a\in P\), \(b\in Q\) changes their difference by
\(2(b-a)\ne0\), since the characteristic is odd.

Define agreement supports

\[
 S_1=\phi^{-1}(J\cup P)\sqcup A_0,
 \qquad
 S_2=\phi^{-1}(J\cup Q)\sqcup A_0.
\tag{4.3}
\]

Their error complements are

\[
 E_1=\phi^{-1}(Q)\sqcup T_0,
 \qquad
 E_2=\phi^{-1}(P)\sqcup T_0.
\tag{4.4}
\]

Thus both codewords have profile \((u,v)=(0,0)\), with the same fixed
agreement remainder \(A_0\) and the same fixed error remainder \(T_0\).
Their intersection is

\[
 I=S_1\cap S_2=\phi^{-1}(J)\sqcup A_0,
 \qquad |I|=65\cdot2048+1911=135031<K.
\tag{4.5}
\]

Put \(g=L_I\), a degree-less-than-\(K\) codeword polynomial.  Define one
base-field received word by

\[
 y(x)=
 \begin{cases}
  0,&x\in S_1,\\
  g(x),&x\in S_2,
 \end{cases}
\tag{4.6}
\]

which is consistent on \(I\), and for \(x\in T_0\) choose
\(y(x)\notin\{0,g(x)\}\).  This is possible because \(g(x)\ne0\) on
\(T_0\) and \(p>2\).  The codewords \(0\) and \(g\) then have exact
agreement sets \(S_1\) and \(S_2\), respectively.

The first quotient coefficient is the negative sum of the selected quotient
labels.  By (4.2), the quotient prefixes of \(J\cup P\) and \(J\cup Q\)
differ.  QR2, with \(w\ge1911\) and quotient depth
\(\lfloor w/2048\rfloor=32\), therefore gives

\[
 \operatorname{pref}_w(L_{S_1})
 \ne
 \operatorname{pref}_w(L_{S_2}).
\tag{4.7}
\]

The same argument applied to (4.4), using \(w\ge137\), shows that their
error-locator prefixes differ as well.

Adding one common codeword to the received word and both explanations leaves
the agreement and error supports unchanged.  More generally, an operation
that leaves those supports literally fixed also leaves their actual monic
locators and prefixes unchanged.  Hence this pair cannot be identified with
one common actual-monic-locator-prefix fiber by such an operation.

This does not rule out a coarser attained target, a non-support-preserving
bijection proved by some new theorem, or a bound that also controls the number
of attained targets.  It does rule out the direct actual-locator common-prefix
identification.  A maximum-prefix-fiber bound alone, without a target-count or
coalescing theorem, cannot replace the sum over attained prefixes.

## 5. Exact arbitrary-word replacement

Let \(Y\in\mathbb F[X]_{<n}\) be the interpolation polynomial of an
arbitrary received word.  An exact-boundary codeword \(P\), with agreement
set \(S\) of size \(A\), is equivalent to

\[
 Y-P=L_SH,
\tag{5.1}
\]

where

\[
 \deg P<K,
 \qquad \deg H\le R-1,
 \qquad H(x)\ne0\quad(x\in D\setminus S).
\tag{5.2}
\]

Indeed, divisibility by \(L_S\) is exactly agreement on \(S\), the degree
bound follows from \(\deg Y<n\), and the last condition excludes additional
agreements.  Conversely (5.1)--(5.2) give exactly the prescribed agreement
set.  Translating the received word and every explanation by one codeword
does not change \(Y-P\), and therefore leaves the pair \((L_S,H)\)
unchanged.

Canonical prefix centers are the special stratum \(H=1\).  Re-centering
each prefix class separately around its own canonical polynomial preserves
the supports inside that class, but loses the common received word and does
not preserve predicates depending on \(H\), the Padé numerator, or the
first-match chronology.

The raw C1-shaped face count before first-match ownership is therefore the
fixed-syndrome multiprefix incidence

\[
 M_{\rm C1}(y)=\sum_z N_y^{\rm C1}(z),
\tag{5.3}
\]

coupled through

\[
 L_{S_1}H_1-L_{S_2}H_2=P_2-P_1,
 \qquad \deg(P_2-P_1)<K.
\tag{5.4}
\]

It is not enough to bound \(\max_zN_y^{\rm C1}(z)\) alone; a declared disjoint
first-match payment must also control or coalesce the attained targets.  The
conditional `9,216,781` allowance is for the combined face-plus-carrier charge,
not for (5.3) in isolation.

## 6. Consequences and remaining target

This packet proves:

1. a fixed-template exact-boundary source theorem for every feasible
   `c=2048` occupancy profile;
2. the exact 177-profile certified-floor-at-least-30 census and the exact
   142-profile sufficient-criterion census, including 18 width-30 and 124
   common-core-sharpened width-29 source profiles;
3. an actual `(1,1)` source of at least `1,693,898` codewords with the
   sharpened two-row bound `65106`;
4. a deployed fixed-remainder pair refuting literal identification of its
   actual monic locator prefixes by a common translation or operation that
   leaves the supports fixed;
5. the exact arbitrary-word \((L_S,H)\) representation and its translation
   invariance.

It does **not** prove:

* a C1 numerical payment;
* a 30-column carrier owner;
* that every 30-column carrier shares one partial template;
* a bound for the sum over attained prefix targets;
* a universal arbitrary-word carrier theorem, a global numerator floor, or a
  counterexample to the deployed M31 row;
* a replacement of the active v4 partition or its global terminals;
* a value for \(U_Q\), \(U_{\rm list,int}\), \(U_{\rm ext}\), or high
  \(U_{\rm new}\);
* a boundary or full-row closure.

The packet-local maximal `c=2048` exact-boundary diagnostic subterminal inside
`HIGH_BOUNDARY_EXACT_CODEWORD` / \(U_{\rm new}\) is

```text
M31_C2048_FIXED_SYNDROME_MULTIPREFIX_FACE_CARRIER_OWNER
```

It must classify actual same-profile 30-column frames using the simultaneous
data \((L_{S_i},H_i)\), route common-template quotient families without
double charging, and bound the complete sum over attained prefix targets.
Each component must end in a chronology-valid paid owner, a budget-fitting
attained-image bound, or an explicit primitive route cut.

The conditional boundary allowance `9,216,781`, all five v4 atoms, the global
M1 terminals, and every high-interior obligation remain unchanged.  No atom
moves.

## 7. Replay and dependence

The standard-library verifier recomputes all deployed constants, every
profile floor, the activation staircase, the symbolic construction gates,
the fixed-remainder obstruction counts, source hashes, and semantic
mutations.  The Sage replay independently constructs two finite-field
fixtures: a fixed-multipartial exact-boundary source and a same-remainder
multiprefix arbitrary-word obstruction.

Load-bearing local sources are the deployed Chebyshev domain and exact-prefix
theorem, QR2, the target-field source adapter, the fixed-remainder source, and
the predecessor occupancy/30-carrier packet.  Open PR #1032 is a logical
chronology cross-check only.  Upstream `main` was unchanged at
`32a41660e3088eeeb15a16645330856794302ff0` when this packet was prepared.

There is no analytic layer-cake, dyadic summability, moment, Markov, or
probabilistic Chebyshev step.  `Chebyshev` denotes the deployed polynomial
fold.
