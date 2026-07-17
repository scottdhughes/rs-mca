# M1 KoalaBear branch-3--5 slope-projection contract v1

**Status:** PROVED SOURCE-STATUS AND QUANTIFIER CONTRACT / PROVED Q0
SUPPORT-MEMBERSHIP ADAPTER / GLOBAL MASK REPLAY OPEN / NO LEDGER MOVEMENT.

This packet repairs the executable-status boundary for the KoalaBear MCA row

\[
 (n,k,A)=(2^{21},2^{20},1{,}116{,}048).
\]

It does not prove a new slope bound.  It proves which predicates may be used
when defining the residual passed to the open rank-nine split-locator count.
The main conclusion is fail-closed:

> Branch 2 now has a proved field-native envelope and owner, but branches
> 3--5 do not form a complete executable first-match projector.  In
> particular, a residual described as "after branches 3--5" is not a
> source-bound object.  Later algebra may instead work on a declared monotone
> superset, such as the full-row-rank branch-3 successor envelope, provided it
> pays that whole superset.

The packet supersedes only the *current-status interpretation* of the older
post-C5 mask inventory.  It does not rewrite that historical artifact.

## 1. Exact row and first-match semantics

Put

\[
 R=n-k=1{,}048{,}576,
 \qquad j=n-A=981{,}104,
 \qquad t=A-k=67{,}472.
\]

For one received pair \((f,g)\), let \(\mathcal W_A(f,g)\) be the set of all
exact-\(A\) noncontained witnesses \((\gamma,S,c)\).  If \(\mathcal C\) is a
witness predicate, write

\[
 Z(\mathcal C)=
 \{\gamma:\text{some witness over }\gamma\text{ satisfies }\mathcal C\}.
\tag{1.1}
\]

For ordered witness cells \(\mathcal C_1,\ldots,\mathcal C_s\), the actual
first-match slope sets are

\[
 Z_i^\circ=Z(\mathcal C_i)\setminus\bigcup_{h<i}Z(\mathcal C_h).
\tag{1.2}
\]

Thus ownership is existential at the slope-projection level.  One must not
choose a witness first and classify only that witness.  Equivalently, after
removing an existential witness owner, **every** witness over a surviving
slope fails its predicate.

This is the finite-row specialization of the witness-exhaustive first-match
definition in `experimental/asymptotic_rs_mca_frontiers.tex`.

The certificate binds these statements semantically, not only by note-file
fingerprints.  It strictly parses the predecessor JSON certificates, verifies
their internal payload hashes where present, checks the exact schemas and
load-bearing status/quantifier/ledger fields, and records both certificate and
verifier hashes.  The older Q0 ledger has no payload-hash field, so this packet
binds its exact file hash and validates its conditional status, row, descent
gate, terminal rungs, terminal cost, and branch-4 deduction flag.

## 2. Branches 1 and 2: exact status refresh

The older post-C5 inventory recorded branch 2 as `UNBOUND_SOURCE_SYMBOL`.
That entry predates the two field-native Hankel packets and is no longer the
current local status.

For

\[
 M_A(\gamma)=H_{t,j}(\operatorname{Syn}(f+\gamma g)),
\]

the proved branch-2 envelope is

\[
 Z_{2,\mathrm{env}}(f,g)=
 \{\gamma\in\operatorname{Bad}_A(f,g):
       \operatorname{rank}_F M_A(\gamma)<t\}.
\tag{2.1}
\]

The actual-error-support factorization proves

\[
 \operatorname{rank}_F M_A(\gamma)
 =\min(t,|E_\gamma|),
\]

and the deep-MCA owner gives the sharp global charge

\[
 |Z_{2,\mathrm{env}}(f,g)|\le t=67{,}472.
\tag{2.2}
\]

The finite-pivot failure locus is empty relative to actual noncontained
incidences.  Consequently the safe successor envelope

\[
 Z_{3,\mathrm{pre}}(f,g)
 =\operatorname{Bad}_A(f,g)\setminus Z_{2,\mathrm{env}}(f,g)
\tag{2.3}
\]

is exact and every member has full ambient-\(F\) row rank.

This does **not** make the literal branch-2 first-match set

\[
 (\operatorname{Bad}_A\setminus Z_1)\cap Z_{2,\mathrm{env}}
\]

machine-exact, because branch 1 still has no source-bound slope projector
\(Z_1\).  The envelope payment (2.2) and the successor (2.3) are nevertheless
safe: they intentionally absorb any overlap with the incomplete earlier
interface.  Later upper bounds are monotone under deleting genuine earlier
owners.

## 3. Branch 3: load-bearing quantifiers

Let

\[
 r_* = \left\lfloor\frac R3\right\rfloor=349{,}525.
\]

The proved deep extension is the existential slope cell

\[
 Z_{3,\mathrm{deep}}=
 \{\gamma\in Z_{3,\mathrm{pre}}:
   \exists\text{ valid exact-}A\text{ witness with }|E_\gamma|\le r_*\}.
\tag{3.1}
\]

Together with branch 2 it lies in one deep-MCA envelope of size at most
\(r_*+1=349{,}526\).  Since branch 2 already contributed \(67{,}472\), the
banked incremental charge is

\[
 349{,}526-67{,}472=282{,}054.
\tag{3.2}
\]

On the complement of (3.1), every valid witness has
\(|E_\gamma|\ge r_*+1\).  Replacing this universal conclusion by failure of
one chosen witness is invalid.

For a retained slope family \(\Gamma\), let \(\operatorname{Sel}(\Gamma)\)
be the finite set of complete actual-witness selectors and define

\[
 \kappa_*(\Gamma)=
 \min_{\sigma\in\operatorname{Sel}(\Gamma)}
 \max\left(0,
   \left|\bigcup_{\gamma\in\Gamma}E^\sigma_\gamma\right|-R\right).
\tag{3.3}
\]

The low-excess common-carrier owner is eligible exactly when **there exists**
a complete selector with \(\kappa\le10\).  Its complementary route
\(\kappa_*\ge11\) means **every** complete selector has excess at least 11.
An unsuccessful supplied selector does not certify this complement.
Likewise, a list of supplied selectors certifies the universal complement only
when a separate certificate says that list exhausts the complete-selector
universe.  The predecessor explicitly has no deployed complete-selector
inventory.  The Python helper therefore treats its small list as a named
`TOY_EXHAUSTIVE_SELECTOR_LIST`; it is a quantifier control, not a deployed
enumerator.

The subsequent intrinsic-rank and sparse-sigma packets operate only after
these quantifiers are fixed.  Their tangent/chosen-minor split is a proved
local partition for one complete rank-nine selector, but its regular
split-locator terminal remains open and its local cap has not been promoted
to a global first-match payment.

## 4. Branch 4: exact Q0 support membership

Write the cyclic domain as

\[
 D_n=\langle\omega\rangle,
 \qquad n=2^{21},
\]

and identify a co-support \(T\subseteq D_n\) with its exponent set in
\(\mathbb Z/n\mathbb Z\).  For a dyadic divisor \(c\mid n\), put

\[
 n_c=n/c,
 \qquad j_c=\lfloor j/c\rfloor,
 \qquad r_c=j-cj_c.
\]

The fibers of \(\pi_c(x)=x^c\) are

\[
 \mathcal F_{c,u}=\{u+vn_c:0\le v<c\},
 \qquad 0\le u<n_c.
\]

The source-bound Q0 membership predicate is

\[
 T=P\sqcup\bigcup_{u\in Q}\mathcal F_{c,u},
 \qquad |Q|=j_c,\qquad |P|=r_c.
\tag{4.1}
\]

Because \(|T|=cj_c+r_c\) and \(r_c<c\), (4.1) is executable without a
choice: \(Q\) is exactly the set of completely occupied \(c\)-fibers, and
\(P\) is the leftover.  Thus Q0 membership is equivalent to

```text
number of complete c-fibers in T == floor(j/c)
and number of leftover points == j mod c.
```

Raw membership and branch-4 route eligibility are different.  When \(c>j\),
one has \(j_c=0\), \(Q=\varnothing\), and \(P=T\), so every size-\(j\)
co-support satisfies (4.1) tautologically.  Such a zero-core decomposition is
not quotient structure and must not make every slope branch-4 eligible.
Accordingly the executable branch-4 filter is

\[
 \text{Q0 membership at }c
 \quad\text{and}\quad j_c\ge1.
\tag{4.2}
\]

The deployed zero-core rungs \(c=1048576,2097152\) are diagnostics for the
pure planted-tail gap, not branch-4 slope masks.

The predicate is applied to the padded size-\(j\) **co-support**
\(T=D\setminus S\), not to the actual nonzero error support.

For a fixed ordered dyadic list, a slope enters the branch-4 Q0 route at rung
\(c\) when some witness over that slope satisfies (4.1)--(4.2).  If different
witnesses, or one witness, qualify at several positive-core rungs, the first
rung in the frozen order owns the slope's **Q0 route assignment**.  This is
not by itself a paid owner.  The first-match decision is again made after
projecting witnesses to slopes.

The current rung theorem proves:

- descent with an open lower-rung max-fiber obligation for
  \(c=2,4,\ldots,32768\);
- descent plus a terminal raw union bound for
  \(c=65536,131072\), with total
  \[
  \binom{32}{14}+\binom{16}{7}
  =471{,}435{,}600+11{,}440
  =471{,}447{,}040;
  \]
- an open positive-core quotient/planted-tail route for
  \(c=262144,524288\), where \(r_c>w\);
- tautological zero-core diagnostics, outside branch-4 eligibility, for
  \(c=1048576,2097152\).

The terminal raw union bound is proved **inside one fixed top-prefix profile
target**: the Q0 injection is stated within \(\Phi_w^{-1}(z)\).  Membership
alone does not transport that cost across different targets and does not
instantiate a new global slope payment.  The current verifier for the older
ledger emits rung arithmetic rather than accepting a witness and returning
its first eligible rung.  The adapter in this packet supplies the missing
support-membership and positive-core route filter; it does not prove the
lower-rung or planted-tail payments, or re-bank the imported terminal cost.

Support periodicity alone is not invariant quotient descent.  The received
data and explaining polynomial must descend through the same fibers before a
quotient owner may be invoked.

## 5. Branch 5 remains source-unbound

The label `planted_prefix_structured` is not an executable predicate.  A
valid branch-5 owner would have to declare, for each plant size \(b\), a
source-bound algebraic family \(\mathcal P_b\), prove membership of the plant
locator, state the residual prefix map and scale, and bound the projection to
distinct slopes.  Arbitrary \(b\)-subsets are explicitly excluded by the
generic planted-payment theorem.

No such deployed family/census/projection packet currently exists.  Therefore
branch 5 is frozen as

```text
UNBOUND_SOURCE_FAMILY
```

and its complement may not be asserted.  In particular, neither
`not periodic` nor `not positive-core Q0` means `not planted`.  The
tautological zero-core Q0 decompositions belong to this unbound pure-planted
gap rather than supplying a branch-4 owner.

## 6. Executable fail-closed policy

The machine contract is:

```text
input: all exact-A noncontained witnesses for each finite slope

branch 2 envelope:
    Bad_A and ambient-F rank(M_A(gamma)) < t

branch 3 deep projection:
    exists witness over gamma with actual error weight <= r_*

branch 3 low-excess family gate:
    exists complete selector of the entire retained family with kappa <= 10
complement:
    every complete selector has kappa >= 11, requiring a certified
    exhaustive complete-selector universe

branch 4 Q0 projection, in frozen dyadic order:
    exists witness over gamma whose size-j co-support satisfies (4.1)
    and whose quotient core is nonempty: floor(j/c) >= 1

zero-core Q0 diagnostic:
    floor(j/c) = 0 is tautological and is not branch-4 eligibility

terminal Q0 payment:
    requires one fixed top-prefix profile target; membership alone does not pay

branch 5:
    UNBOUND_SOURCE_FAMILY

downstream exact complement after branches 3--5:
    FORBIDDEN_UNTIL_ALL_PRIOR_SLOPE_PROJECTIONS_ARE_SOURCE_BOUND
```

The exact small cyclic control uses \(n=16,j=7\).  One co-support qualifies
simultaneously at \(c=2\) and \(c=4\); the slope-projection classifier assigns
it to \(c=2\).  A second co-support qualifies only at \(c=4\).  A separate
witness-family control checks that a slope with one heavy and one light
witness is removed by the existential deep cell, and that one low-excess
complete selector pays a family even if another selector has excess 12.  The
independent Sage replay constructs \(D=\mathbb F_{17}^*\), checks the exponent
fibres against \(x\mapsto x^c\), and verifies
\(L_T(X)=L_P(X)L_Q(X^c)\) for every positive control.  It also checks that
every co-support has tautological raw membership at \(c=8,16>j\), while
neither zero-core rung is eligible for the branch-4 route.

## 7. Ledger and verdict

This packet changes no charge:

\[
 U_{\rm paid}=2{,}602{,}502{,}999,
 \qquad
 B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\]

Both \(U_Q\) and \(U_A\) remain `null`, not zero.

- **GREEN:** branch-2 envelope/successor status, branch-3 quantifier contract,
  exact Q0 co-support membership, the positive-core branch-4 filter, frozen
  rung ordering, fixed-prefix payment guard, and fail-closed complement policy.
- **RED:** a claim that branches 1--5 now form a complete executable paid
  first-match replay.
- **YELLOW:** the KoalaBear row and the regular rank-nine split-locator count.

No layer-cake, moment, Markov, or Chebyshev argument is used.  All printed
deployed arithmetic is exact.  The \(n=16\) controls test semantics only and
are not evidence for the deployed slope count.

## 8. Minimal next action

Use this contract in one of two legitimate ways:

1. prove a row-uniform bound on the entire declared branch-3/rank-nine
   successor envelope, so incomplete later masks are irrelevant by
   monotonicity; or
2. supply a source-bound branch-5 algebraic plant family and distinct-slope
   payment before passing its complement to the regular locator algebra.

Do not describe a local full-projective/GM control as a deployed residual, do
not select one witness before first-match projection, and do not move the
ledger from this contract alone.
