---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The complete c=2048 partial-occupancy atlas has 261192 profiles, of which 260576 are bi-deep.  Hence either the bi-deep exact-boundary layer has at most 7556704 codewords, or one profile contains a 30-codeword subpacket and the field-generic coupled Padé--Forney theorem supplies two independent rows of combined degree at most 65262<67447.
architecture: DIRECT_TARGET_FIELD_BOUNDARY_REDUCTION
partition_digest: CERTIFICATE_BOUND
atom_or_cell: C1_BOUNDARY / M31_VARIABLE_REMAINDER_ORIENTATION_RESIDUAL
quantifier: Every received word over F_(p^4) and its complete exact error-weight R layer.
projection_and_unit: Exact codewords and their unique exact error supports; no slope projection and no numerical owner payment.
claimed_bound: bi-deep residual <=7556704 OR an exact same-profile 30-column coupled two-row carrier exists
status: PROVED
impact: ROUTE_CUT
falsifier: A feasible c=2048 occupancy profile outside the atlas, a bi-deep family of more than 7556704 codewords with no 30-member profile, or failure of the target-field 30-column coupled-index conclusion.
replay: Python normal/optimized certificate and mutations, plus independent Sage finite-field replay.
---

# M31 `c=2048` partial-occupancy atlas and 30-carrier reduction

## Status

```text
PROVED TARGET-FIELD EXACT-BOUNDARY REDUCTION
route_terminal = M31_C2048_BIDEEP_30COLUMN_OWNER
ledger_movement = 0
row_closed = false
```

This packet exhausts the variable-remainder occupancy profiles at the most
important deployed Chebyshev scale.  It converts a large bi-deep boundary
residual into one precise algebraic object: a 30-codeword same-profile
coupled Padé--Forney frame.  It does not classify or pay that frame.

The conclusion is stronger than another isolated fixed-width calculation.
It says that the entire `c=2048` bi-deep boundary residual is already below
`7,556,704` unless the 30-column object occurs.

## 1. Deployed row and scope

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

The deployed code is

\[
 \operatorname{RS}_{\mathbb F_{p^4}}(D,K),
 \qquad D\subseteq\mathbb F_p.
\]

Fix an arbitrary received word over \(\mathbb F_{p^4}\).  This note concerns
its complete exact layer of error weight \(R\).  Because
\(R<K+1=d_{\min}\), two listed codewords cannot have the same exact error
support.  Counts of supports below are therefore counts of codewords.

Let the deployed `T_2048` map partition \(D\) into

\[
 N=n/2048=1024
\]

complete fibers, each of size \(c=2048\).  Only this fixed partition is used
in the occupancy atlas.

## 2. Exact occupancy atlas

For an exact error support \(S\subseteq D\), \(|S|=R\), define

* \(m\): number of fibers contained in \(S\);
* \(z\): number of fibers disjoint from \(S\);
* \(h=N-m-z\): number of partial fibers.

Write

\[
 u=479-m,
 \qquad v=544-z.
\tag{2.1}
\]

The error and agreement points in the partial fibers are respectively

\[
 r_{\rm err}=R-cm=137+2048u,
 \qquad
 r_{\rm agr}=A-cz=1911+2048v,
\tag{2.2}
\]

and

\[
 h=u+v+1,
 \qquad r_{\rm err}+r_{\rm agr}=2048h.
\tag{2.3}
\]

### Theorem 2.1 (complete profile classification)

The feasible profiles are exactly

\[
 \{(0,v):0\le v\le136\}
 \;\sqcup\;
 \{(u,v):1\le u\le479,\ 0\le v\le544\}.
\tag{2.4}
\]

Consequently there are exactly

\[
 137+479\cdot545=261192
\tag{2.5}
\]

profiles.

### Proof

The size constraints imply \(m\le\lfloor R/c\rfloor=479\) and
\(z\le\lfloor A/c\rfloor=544\), so \(u,v\ge0\).  In every partial fiber
both colors occur.  Thus a triple is feasible exactly when

\[
 h\le r_{\rm err}\le h(c-1)
 \quad\text{and}\quad
 h\le r_{\rm agr}\le h(c-1).
\tag{2.6}
\]

Using (2.2)--(2.3), the four slacks are

\[
\begin{aligned}
 r_{\rm err}-h&=136+2047u-v,\\
 h(c-1)-r_{\rm err}&=1910+2047v-u,\\
 r_{\rm agr}-h&=1910+2047v-u,\\
 h(c-1)-r_{\rm agr}&=136+2047u-v.
\end{aligned}
\tag{2.7}
\]

If \(u=0\), these inequalities are equivalent to \(0\le v\le136\).
If \(u\ge1\), they hold throughout
\(1\le u\le479\), \(0\le v\le544\).  Conversely, whenever (2.6) holds,
write \(r_{\rm err}\) as a sum of \(h\) integers in
\([1,c-1]\); selecting that many points in the \(h\) partial fibers
constructs a support.  This proves both necessity and sufficiency. \(\square\)

## 3. Frozen C1-shaped face, arm, and core partition

The two Euclidean-remainder, or **C1-shaped**, faces are

\[
 u=0
 \quad\text{or}\quad
 v=0.
\tag{3.1}
\]

On the first face the error orientation has `479` complete fibers and a
remainder of size `137<2048`; on the second face the complementary agreement
orientation has `544` complete fibers and a remainder of size `1911<2048`.
For each individual support its remainder is fixed while the corresponding
QR profile is evaluated.

For a canonical locator-prefix center \(U_z\), the exact prefix-list
bijection proves that the whole boundary list is precisely the prefix fiber,
and every codeword and support is base-field-valued.  Adding one codeword to
the center and to every explanation preserves all exact supports and the
coupled syndrome data.  This supplies the missing codeword projection for
canonical centers and their codeword translates.  Actual C1 routing then
still uses the declared owner order and must accept the chosen error or
complementary-agreement orientation; this paragraph does not prove that both
orientations are active owner predicates.

There is no proved converse saying that an arbitrary quartic-field received
word is such a translate.  Accordingly, for a general received word the two
sets in (3.1) are only C1-shaped occupancy faces.  Their actual routing by or
at C1 remains conditional on the missing boundary-to-prefix adapter and on
the declared first-match order.  This packet infers no numerical C1 payment.

There are exactly

\[
 137+479=616
\tag{3.2}
\]

face profiles.  The bi-deep residual is

\[
 1\le u\le479,
 \qquad 1\le v\le544,
\tag{3.3}
\]

and has

\[
 479\cdot544=260576
\tag{3.4}
\]

profiles.

The relevant locator prefix has depth \(w=67447\).  In the error orientation,
the partial-error locator is
visible through that depth exactly for \(u\le32\), since

\[
 137+2048\cdot32=65673\le67447
 <67721=137+2048\cdot33.
\tag{3.5}
\]

Using the complementary locator and its own prefix, the partial-agreement
locator is visible exactly for
\(v\le32\), with

\[
 1911+2048\cdot32=67447
 <69495=1911+2048\cdot33.
\tag{3.6}
\]

Thus the two visible arms inside the bi-deep residual contain

\[
 32\cdot544+479\cdot32-32^2=31712
\tag{3.7}
\]

profiles, while the double-strict core \(u,v\ge33\) contains

\[
 447\cdot512=228864.
\tag{3.8}
\]

### Lemma 3.1 (fixed-quotient recovery on a visible arm)

Let
\[
 \phi(X)=2^{-2047}T_{2048}(X)
\]
be the monic normalization of the deployed fold; it has the same fibers.
For a quotient set \(E\), put
\[
 V_E(Y)=\prod_{b\in E}(Y-b).
\]
Let a support have complete-fiber quotient set \(E\), partial remainder
\(R_0\), and locator

\[
 L=P_{R_0}(V_E\circ\phi).
\]

Fix the global depth-\(w\) locator prefix and fix \(E\).  If
\(|R_0|\le w\), then \(R_0\) is uniquely determined.

### Proof

For reciprocal polynomials,

\[
 L^\vee=P_{R_0}^\vee B_E,
 \qquad B_E=(V_E\circ\phi)^\vee.
\]

The constant coefficient of \(B_E\) is one.  It is therefore a unit modulo
\(Z^{w+1}\).  Division recovers
\(P_{R_0}^\vee\bmod Z^{w+1}\); because
\(\deg P_{R_0}\le w\), this is the entire monic locator and hence its root
set. \(\square\)

This lemma does not bound the number of quotient sets \(E\), does not assign
an owner, and gives no recovery when both \(u,v\ge33\).

## 4. Exact 30-carrier dichotomy

Let \(M_{u,v}(y)\) be the number of exact-boundary codewords of the fixed
received word whose supports have profile \((u,v)\).  Put

\[
 M_{\rm deep}(y)=
 \sum_{u=1}^{479}\sum_{v=1}^{544}M_{u,v}(y).
\]

### Lemma 4.1 (field-generic arbitrary-subpacket kernel)

Let \(\mathbb K\) be any field containing the deployed evaluation domain.
Take the complete exact error-weight \(j\) layer of one received word over
\(\mathbb K\), divide the common core \(C_j\) of the **entire** layer, and
write its reduced locator and divided-difference numerator columns as
\((P_i,B_i)\).  For every selected subpacket \(T\) of cardinality
\(q=|T|\ge3\), its joint kernel

\[
 \left\{(A_i)_{i\in T}:
   \sum_{i\in T}A_iP_i=\sum_{i\in T}A_iB_i=0\right\}
\]

is free of rank \(q-2\).  If
\(0\le\nu_1\le\cdots\le\nu_{q-2}\) are its row-reduced indices, then

\[
 \sum_{r=1}^{q-2}\nu_r
 \le 2j-K-|C_j|-1.
\tag{4.1}
\]

### Proof

The target-field source adapter proves over an arbitrary \(\mathbb K\) that
the shortened-dual functional, containment equations, one-point escapes,
divided-difference identities, and pair-minor formula survive unchanged.
For distinct columns every pair minor

\[
 \Omega_{ij}=P_iB_j-P_jB_i
\]

is nonzero and has degree at most
\(\sigma=2j-K-|C_j|-1\).  Hence the two-row polynomial matrix restricted to
\(T\) has rank two.  Over the PID \(\mathbb K[X]\), its kernel is a direct
summand of rank \(q-2\).  If
\(d_T=\gcd_{i<j\in T}\Omega_{ij}\) and
\(\tau_T=\max_{i<j\in T}\deg\Omega_{ij}\), cofactor duality and predictable
degree give

\[
 \sum_r\nu_r=\tau_T-\deg d_T\le\sigma.
\]

This repeats the arbitrary-subpacket proof over \(\mathbb K[X]\); it does not
truncate a 46-column frame. \(\square\)

### Theorem 4.2 (bi-deep occupancy or 30-column carrier)

For every target-field received word, exactly one of the following
alternatives is forced:

1. \(M_{u,v}(y)\le29\) for every bi-deep profile, and hence
   \[
   M_{\rm deep}(y)\le29\cdot260576=7556704;
   \tag{4.2}
   \]
2. some fixed bi-deep profile contains 30 distinct exact-boundary codewords.
   On any selected 30 of them, the coupled locator--numerator kernel has two
   independent rows whose combined vector degree is at most
   \[
   \left\lfloor\frac{2(2R-K-1)}{30-2}\right\rfloor
   =65262
   <67447=K-R.
   \tag{4.3}
   \]
   In particular, the two rows have a nonzero two-by-two minor of degree
   below the exact boundary cutoff.

### Proof

The first alternative is immediate by summing the 260576 profile caps.  If
it fails, pigeonhole gives a profile with at least 30 codewords.

For the second conclusion, apply Lemma 4.1 over
\(\mathbb K=\mathbb F_{p^4}\) after dividing the true common core of the
complete exact weight-\(R\) layer.  Recompute the kernel on the selected
\(q=30\) columns.  Its \(28\) nondecreasing joint
indices have total at most

\[
 S=2R-K-1=913681.
\]

The sum of the first two is at most \(\lfloor2S/28\rfloor=65262\).
The joint kernel is a direct summand of rank 28, so its first two
row-reduced basis rows are independent and some two-by-two minor is nonzero.
Its degree is at most the sum of their row degrees.  This proves (4.3).
\(\square\)

The threshold is sharp for the presently known aggregate index information:

\[
 \left\lfloor\frac{2S}{29-2}\right\rfloor
 =67680>67447,
\tag{4.4}
\]

whereas 30 columns give (4.3).  This is an information-theoretic statement
about the inherited index-sum bound; it does not assert that the adverse
29-column index sequence is geometrically realized.

## 5. Exact budget calibration

The banked low-weight payment is `3730`.  Suppose a future fixed, disjoint,
non-oracular first-match compiler proves both of the following:

1. it assigns the C1-shaped faces through a valid boundary-to-prefix adapter;
2. after applying its declared algebraic carrier-owner predicates, the
   unowned bi-deep residual has at most 29 codewords in every profile.

Then the remaining residual is at most (4.2).  Let
\(U_{\rm face+carrier}\) denote the combined charge of the face owners and
all carrier owners.  A sufficient exact boundary-only
target is

\[
 U_{\rm face+carrier}
 \le16777215-3730-7556704=9216781.
\tag{5.1}
\]

Carrier codewords are not silently deleted: their entire disjoint charge is
included in \(U_{\rm face+carrier}\).  The existence of one 30-subpacket in
Theorem 4.2 is only the trigger for the next algebraic classification; it is
not itself an admissible owner or pruning rule.

The fixed-remainder source from the predecessor packet lies on
\((u,v)=(0,0)\) and has at least `6,796,405` codewords.  Therefore the
conditional early allowance (5.1) is not refuted by that source; its exact
slack is

\[
 9216781-6796405=2420376.
\tag{5.2}
\]

This is a conditional combined-owner target, not a proved payment.  It also
budgets only the low cell and the exact boundary layer.  The high interior
weights, extension atom,
and the other v4 chronology terms remain open.

For scale, the complete raw atlas satisfies

\[
 64\cdot261192=16716288<B_*,
\tag{5.3}
\]

and the bi-deep atlas satisfies

\[
 64\cdot260576=16676864<B_*.
\tag{5.4}
\]

Thus more than \(B_*\) boundary codewords force 65 codewords in one raw
profile; more than \(B_*\) bi-deep codewords force 65 in one bi-deep
profile.  On 65 columns the same aggregate theorem gives

\[
 \nu_1\le14502,
 \qquad \nu_1+\nu_2\le29005<67447.
\tag{5.5}
\]

## 6. What is proved and what remains open

This packet proves:

1. an exhaustive, row-uniform `c=2048` occupancy atlas;
2. the exact C1-face / bi-deep / visible-arm / double-core counts;
3. fixed-quotient recovery on the visible arms;
4. a target-field dichotomy reducing every oversized bi-deep boundary
   residual to one same-profile 30-column coupled frame;
5. the exact boundary-only numerical target left after that reduction.

It does **not** prove:

* a numerical payment for C1 or for the early face union;
* that the 30-column carrier has a paid periodic, quotient, Johnson, or B11
  owner;
* an admissible first-match rule based on enumerating the received-word list;
* that the visible-arm recovery bounds the number of quotient sets;
* a bound for high interior weights;
* a value for \(U_Q\), \(U_{\rm list,int}\), \(U_{\rm ext}\), or high
  \(U_{\rm new}\);
* any ledger movement, endpoint, score, stable-paper, or Lean change.

The exact successor obligation is the named terminal

```text
M31_C2048_BIDEEP_30COLUMN_OWNER
```

Classify the same-profile 30-column coupled frame using the partial-fiber
incidence equations.  Turn the classification into a fixed, non-oracular,
codeword-disjoint owner rule and prove that its residual has at most 29
codewords per profile.  Every component must terminate in a chronology-valid
paid owner, an attained-image bound that fits the remaining budget, or an
explicit primitive route cut.  A generic fixed-width computation with no
profile incidence is insufficient.

## 7. Replay and dependence

The Python certificate independently enumerates every feasible occupancy
pair from the fiber inequalities, checks all partitions and integer budgets,
and rejects semantic mutations.  The Sage replay uses exact finite-field
polynomials to check the reciprocal recovery lemma and exhausts a toy
complete-fiber support atlas independently.

Load-bearing sources are the active v4 source adapter, its target-field
Lemma 2.1, the coupled Padé--Forney subpacket theorem, the exact
quotient--remainder normal form, and predecessor #1039.  PR #1032 at exact
head `a843a8f7930054617ef1d94169a4a9d3422cb909` is a logical chronology
dependency only; it is not mechanical ancestry and its fixed-remainder C1
rule is not converted into a numerical payment here.

There is no analytic layer-cake, dyadic summability, moment, Markov, or
probabilistic Chebyshev step.  `Chebyshev` denotes the deployed polynomial
fold.
