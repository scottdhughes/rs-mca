# M1 KoalaBear rank-nine GM--MDS fixed-domain gate v1

- **Status:** PROVED universal support/rank trichotomy / PROVED exact
  specialization countercontrol / deployed input and executor missing / no
  ledger movement.
- **Target:** the regular split-locator terminal left by
  `m1_kb_branch3_rank9_sparse_chart_boundary_v1.md` after the generic
  rank-to-locator-span shortcut was refuted.
- **Companion checks:**
  `verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.py` and
  `verify_m1_kb_rank9_gm_mds_fixed_domain_gate_v1.sage`.

This packet proves one fail-closed gate.  Given a **declared** eleven-tuple
of retained monic degree-`j`, `D`-split locators, it either emits a large
common-core witness, certifies their exact fixed-domain independence, or
emits an exact specialization dependence.  It does not supply an actual
retained KoalaBear 11-tuple and therefore makes no owner payment.

The local gate is GREEN.  Its application to the deployed KoalaBear
first-match residual is YELLOW because the required supports and their
first-match provenance have not been produced.

**Implementation boundary:** the committed Python and Sage programs are
`CONTROL_ONLY` exact replays at `j=10`.  Their sequential locator builder is
quadratic in `j`, so a deployed-scale executor is not implemented.  The
KoalaBear rank test requires a fast product-tree/NTT coefficient backend or a
streamed exact nonzero-minor certificate.

## 1. Deployed interface

At the open KoalaBear MCA row,

\[
 p=2^{31}-2^{24}+1,
 \qquad q=p^6,
 \qquad (n,k,A)=(2^{21},2^{20},1{,}116{,}048),
\]

and hence

\[
 R=n-k=1{,}048{,}576,
 \qquad j=n-A=981{,}104.
\]

The sparse chart-boundary predecessor leaves the terminal

```text
REGULAR_HIGH_EXCESS_SPLIT_LOCATOR_ROUTE
```

with one monic, squarefree, `D`-split degree-`j` locator for each selected
regular slope.  It explicitly leaves later owner masks pending.  The next
rank-only locator-span shortcut is false by the parametric counterexample in
`m1_rank9_regular_locator_span_shortcut_refuted_v1.md`.

After the earlier base-slope owner has been applied, genuinely unresolved
regular slopes are extension-valued.  That field split does not supply their
supports.  The input required here is one declared tuple

\[
 (T_1,\ldots,T_{11}),\qquad T_i\subseteq D,\quad |T_i|=j,
\tag{1.1}
\]

together with the record that these locators survive the earlier deployed
first-match owners.

The base-field assertion used below is not inferred from splitness.  The
deployed source `experimental/cap25_cap_v13_raw.tex`, subsection *Proved base
cases of the identity-scale collision problem*, states that the KoalaBear
domain is a coset of the order-`2^21` subgroup of `F_p^times`.  Thus
`D subset F_p`.

## 2. Deployed 11-locator GM--MDS/fixed-domain trichotomy

Put

\[
 L_{T_i}(X)=\prod_{x\in T_i}(X-x),
 \qquad K=j+1.
\]

For every nonempty (I\subseteq[11]), test

\[
 \boxed{
 |I|+\left|\bigcap_{i\in I}T_i\right|\le K.
 }
\tag{2.1}
\]

Exactly one of the following fail-closed outcomes occurs.

### 2.1 Intersection failure

If (2.1) fails for (I), put

\[
 r=|I|,
 \qquad W=\bigcap_{i\in I}T_i,
 \qquad c=|W|.
\]

Then

\[
 c\ge j+2-r.
\tag{2.2}
\]

For every (i\in I),

\[
 L_{T_i}=L_W L_{T_i\setminus W},
 \qquad \deg L_{T_i\setminus W}=j-c\le r-2.
\tag{2.3}
\]

Thus the (r) locators lie in the space

\[
 L_W\,F[X]_{\le j-c},
\]

whose dimension is at most (r-1).  They are dependent over every field and
for every distinct-point specialization.  Moreover,

\[
 |T_i\setminus W|\le r-2,
 \qquad
 d_J(T_i,T_{i'})
 =j-|T_i\cap T_{i'}|
 \le r-2.
\tag{2.4}
\]

The exact terminal is

```text
JOHNSON_COMMON_CORE_CANDIDATE_NOT_PAID
```

Equation (2.4) is a geometric Johnson/common-core candidate, not an existing
owner assignment.  It does not prove the alignment hypothesis of the
deployed Johnson owner, does not bound the global carrier of the complete
selector, and implies neither cyclic periodicity nor invariant quotient
descent.

### 2.2 Intersection success and exact rank eleven

If every inequality (2.1) holds, compute the rank over `F_p` of the eleven
coefficient rows

\[
 \ell_{T_i}=([X^0]L_{T_i},\ldots,[X^j]L_{T_i}).
\tag{2.5}
\]

Because the bound deployed source gives `D subset F_p`, this is also the
rank after scalar extension to `F_(p^6)`.  For a declared
tuple alone, rank eleven gives only the support-level terminal

```text
FIXED_DOMAIN_LOCATOR_INDEPENDENCE_CERTIFIED_FOR_DECLARED_TUPLE
```

Only after the certificate also verifies retained-slope and first-match
provenance may this be promoted to

```text
DEPLOYED_LOCATOR_INDEPENDENCE_CERTIFIED_AFTER_PROVENANCE
```

Either terminal is only a local independence certificate.  A later counting
argument must still show what it pays.

### 2.3 Intersection success and exact rank below eleven

If every inequality (2.1) holds but the rank in (2.5) is below eleven, emit a
nonzero relation

\[
 \sum_{i=1}^{11}c_iL_{T_i}=0.
\tag{2.6}
\]

The exact terminal is

```text
FIXED_DOMAIN_GM_SPECIALIZATION_EXCEPTION
```

This is an explicit unpaid component.  It must not be forced into a Johnson,
periodic, or quotient owner.

## 3. The imported generic theorem and its exact scope

For a binary support (T_i), let (v_i\in\{0,1\}^{|D|}) be its indicator.
In Shachar Lovett, *MDS matrices over small fields: A proof of the GM--MDS
conjecture*, [arXiv:1803.02523](https://arxiv.org/abs/1803.02523), Definition
1.4 gives Property (V(K)), and Theorem 1.7 proves formal-root independence
under Property (V^*(K)).

Here (|v_i|=j=K-1), so each (v_i) contributes the single polynomial
(L_{T_i}).  For nonempty (I), Property (V(K)) is exactly

\[
 \sum_{i\in I}(K-|v_i|)
 +\left|\bigwedge_{i\in I}v_i\right|
 =|I|+\left|\bigcap_{i\in I}T_i\right|
 \le K.
\tag{3.1}
\]

All vectors are binary, so (V^*(K)) applies.  Consequently (2.1) proves
that the locator polynomials are independent over the **formal-root field**.
Equivalently, some coefficient minor is a nonzero polynomial in formal
evaluation points.

This does not say that the same minor is nonzero at every fixed collection
of distinct field points.  The numerical field-size condition also does not
repair that quantifier.  At KoalaBear,

\[
 p\ge n+K-1,
\]

but an exact rank or nonzero minor at the deployed subgroup is still
mandatory.

## 4. Exact same-shape specialization exception

The fixed-domain caveat already occurs with the same

\[
 11\text{ locators},\qquad j=10,
\]

shape and inside the usual GM--MDS field-size envelope.

Work over (F=\mathbb F_{127}), and set

\[
 C=\{4,5,6,7,8,9,10,11\}.
\]

Take

\[
 T_1=C\cup\{1,-1\},\quad
 T_2=C\cup\{2,-2\},\quad
 T_3=C\cup\{3,-3\},
\tag{4.1}
\]

and eight further pairwise-disjoint ten-point supports, each disjoint from
the first three.  The verifier freezes an explicit choice.  The union has
size (94), and

\[
 127\ge94+11-1.
\]

All (2^{11}-1=2047) inequalities (2.1) hold.  Nevertheless, if

\[
 Q=L_C,
\]

then

\[
 L_{T_1}=Q(X^2-1),\quad
 L_{T_2}=Q(X^2-4),\quad
 L_{T_3}=Q(X^2-9),
\]

and in (mathbb F_{127}[X]),

\[
 47L_{T_1}+L_{T_2}+79L_{T_3}=0.
\tag{4.2}
\]

Indeed (47+1+79=127) and
(47+4+79\cdot9=762=6\cdot127).  The complete eleven-row coefficient
matrix has exact rank ten.  Therefore GM--MDS admissibility alone cannot
replace the fixed-domain test.

For transparency the certificate also includes a three-quadratic control
over (mathbb F_{11}): the disjoint supports

\[
 \{1,-1\},\quad\{2,-2\},\quad\{3,-3\}
\]

satisfy every GM--MDS inequality and the field-size bound
(11\ge6+3-1), but

\[
 9(X^2-1)+(X^2-4)+(X^2-9)=0.
\tag{4.3}
\]

## 5. Exact common-core and full-rank controls

The certificate independently freezes two more eleven-locator controls over
(mathbb F_{127}).

1. Three distinct locators share a nine-root core and have distinct
   one-point petals.  Pair inequalities are tight, the first triple
   inequality fails, the exact Johnson distance is one, and the classifier
   emits only `JOHNSON_COMMON_CORE_CANDIDATE_NOT_PAID`.
2. Eleven pairwise-disjoint ten-point supports have coefficient rank eleven,
   and the control classifier emits
   `FIXED_DOMAIN_LOCATOR_INDEPENDENCE_CERTIFIED_FOR_DECLARED_TUPLE`.

Sage independently reconstructs all three same-shape controls, enumerates
all (2047) intersection inequalities, and checks the ranks and null
relations.

## 6. Owner and ledger consequences

This trichotomy closes the proposed *generic GM--MDS shortcut*, not the
KoalaBear row:

- intersection failure gives a named common-core candidate but no paid
  owner;
- intersection success gives only generic independence until the deployed
  coefficient rank is checked;
- a fixed specialization relation is a legitimate primitive terminal;
- no statement here produces or exhausts the actual retained supports.

Therefore

\[
 \Delta U_{\rm paid}=0,
 \qquad
 \Delta B_{\rm rem}=0.
\]

There is no ledger movement.

## 7. Audit record

- **Statement audited:** the implication from eleven regular split locators
  to generic independence, fixed-domain independence, or an existing paid
  owner.
- **Dependencies:** Lovett's Property (V^*(K)) theorem for the formal-root
  branch; direct factor-space dimension for a failed inequality; exact
  finite-field row reduction for specialization.
- **Parameter dependence:** exact in `j`, the declared eleven supports,
  and the fixed domain; no hidden `T`, `Y`, `L`, `lambda`, or asymptotic
  constant.
- **Layer-cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** the controls are exact finite-field identities,
  not a deployed census or asymptotic proof.
- **Implementation scale:** `CONTROL_ONLY_J10`; the deployed executor is not
  implemented.
- **Local verdict:** GREEN.
- **Deployed owner/payment verdict:** YELLOW -- required retained supports,
  first-match provenance, and a deployed-scale executor are missing.

## 8. Minimal next action

Produce one exact retained record

```text
(gamma_i, T_i, regular-chart witness, first-match exclusions), i=1,...,11
```

for extension-valued KoalaBear survivors.  Run the 2,047 intersection
tests.  In parallel, implement a fast product-tree/NTT or streamed-minor
backend at `j=981104`.  If the intersections all pass, certify one
nonzero fixed-domain evaluation or coefficient minor with that backend; if
one fails, run the actual Johnson owner predicate on the emitted common core.
Stop on a specialization exception or on a Johnson candidate that fails the
deployed owner hypotheses.

Do not resume generic locator-span bounds, attack rank at least ten, move the
ledger, or promote this packet to a stable theorem before that input exists.
