# M1 KoalaBear branch-3 deep-owner extension and CCL/TDD cut v1

**Status:** PROVED DEEP-OWNER EXTENSION /
EXACT SHARED-ENVELOPE ACCOUNTING DELTA /
PROVED COMMON-CODE-LINE OR TRIPLE-DISTANCE-DEFECT DICHOTOMY /
BRANCH 3 AND ROW OPEN.

This packet makes one bankable improvement to the KoalaBear M1 upper ledger at

\[
A=1{,}116{,}048
\]

and replaces the broad branch-3 fallback by a sharper named residual.

First, every branch-3 slope admitting an actual noncontained witness whose
nonzero error support has size at most

\[
r_*=\left\lfloor\frac{n-k}{3}\right\rfloor=349{,}525
\]

lifts to the exact deep-MCA owner.  Together with the already-paid branch-2
rank-drop cell, this enlarged owner has the global upper cap
\(r_*+1=349{,}526\).
The predecessor already charged \(67{,}472\), so the new ledger delta is

\[
349{,}526-67{,}472=282{,}054.
\]

Second, choose one actual witness for every surviving heavier branch-3 slope.
Apply the integrated global-carrier owner first.  If the selected support union
has excess at most ten over \(R\), it is a certified budget-fitting
alternative.  Otherwise either the retained family has at most \(15\) slopes
or some triple has a nonzero triple-distance defect, supported on the union of
its three actual error supports, so that union has size at least
\(R+1=1{,}048{,}577\).

The last terminal is named `UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT`.  This
packet does not pay it and therefore does not close branch 3 or the KoalaBear
row.

## Statement audited

Let

\[
C=\operatorname{RS}_F(D,k),\qquad |D|=n,
\]

and let \(f,g:D\to F\) be one received pair.  Put

\[
R=n-k,\qquad j=n-A,\qquad t=A-k=R-j.
\]

For KoalaBear,

\[
\begin{aligned}
n&=2{,}097{,}152, &
k&=1{,}048{,}576,\\
R&=1{,}048{,}576, &
A&=1{,}116{,}048,\\
j&=981{,}104, &
t&=67{,}472.
\end{aligned}
\tag{1}
\]

For every finite MCA-bad slope \(\gamma\), a declared exact-\(A\)
noncontained witness consists of a set \(S_\gamma\subseteq D\), a codeword
\(c_\gamma\in C\), and

\[
|S_\gamma|=A,\qquad
y_\gamma=f+\gamma g=c_\gamma\quad\hbox{on }S_\gamma,
\]

while the received pair is not simultaneously explained on \(S_\gamma\).
Define

\[
e_\gamma=y_\gamma-c_\gamma,\qquad
E_\gamma=\operatorname{supp}(e_\gamma).
\tag{2}
\]

Then

\[
E_\gamma\subseteq D\setminus S_\gamma,\qquad |E_\gamma|\le j.
\tag{3}
\]

The predecessor proves the field-native identity

\[
\operatorname{rank}_F M_A(\gamma)=\min\{t,|E_\gamma|\}.
\tag{4}
\]

Thus every full-row-rank branch-3 survivor has

\[
t\le |E_\gamma|\le j
\tag{5}
\]

for every declared actual witness.

## The extended deep owner

Set

\[
r_*=\left\lfloor\frac R3\right\rfloor=349{,}525,\qquad
A_*=n-r_*=1{,}747{,}627.
\tag{6}
\]

The exact gate is

\[
3r_*=1{,}048{,}575\le R=1{,}048{,}576.
\tag{7}
\]

Suppose a branch-3 slope has one declared witness (2) with
\(|E_\gamma|\le r_*\).  Enlarge its witness support to the full agreement set

\[
S_\gamma^*=D\setminus E_\gamma.
\tag{8}
\]

By (3),

\[
S_\gamma\subseteq S_\gamma^*,\qquad
|S_\gamma^*|\ge n-r_*=A_*.
\tag{9}
\]

The same codeword \(c_\gamma\) explains the point on \(S_\gamma^*\).
Noncontainment persists upward: a simultaneous explanation of \(f,g\) on
\(S_\gamma^*\) would restrict to one on \(S_\gamma\), contradicting the
declared witness.  Therefore \(\gamma\) is MCA-bad at agreement \(A_*\).  If
an exact-size witness convention is used, choose any \(A_*\)-point subset of
\(S_\gamma^*\) containing \(S_\gamma\); such a subset exists by (9), and the
same restriction argument preserves noncontainment.

Paper D's `thm:deep-mca`, equivalently the exact numerator
`cor:exact-deep-numerator` in the thresholds file, gives

\[
\#\{\hbox{finite MCA-bad slopes at agreement }A_*\}
\le r_*+1=349{,}526.
\tag{10}
\]

The literal branch-2 rank-drop slopes also lie in this same envelope because
their actual error weight is at most

\[
t-1=67{,}471\le r_*.
\]

Consequently the union of:

1. the already-paid literal branch-2 cell; and
2. the literal branch-3 slopes for which a witness with
   \(|E_\gamma|\le r_*\) exists

has one global upper cap \(349{,}526\).  This is a composite owner extension,
not a
claim that branch 3 alone has cap \(282{,}054\).  Since the ledger already
allocated \(67{,}472\) to branch 2, the exact accounting increment used to
raise the chosen shared envelope to (10) is

\[
\Delta U_{\rm deep}
=349{,}526-67{,}472
=282{,}054.
\tag{11}
\]

This use is monotone under all earlier first-match deletions.

## The heavy residual

Remove the extended deep owner.  Intrinsically, a surviving slope has no
declared exact-\(A\) noncontained witness with actual error weight at most
\(r_*\).  Hence every valid selected witness on the residual satisfies

\[
r_*+1\le |E_\gamma|\le j.
\tag{12}
\]

Let \(Z\) be the surviving finite-slope set for one fixed received pair, and
choose one declared witness (2) for each \(\gamma\in Z\).  The theorem below is
valid for every such selection.

Put

\[
U_{\rm sel}=\bigcup_{\gamma\in Z}E_\gamma,\qquad
\kappa_{\rm sel}=\max\{0,|U_{\rm sel}|-R\}.
\tag{13}
\]

The integrated carrier packet is the first-match owner:

```text
kappa_sel <= 10
    -> CERTIFIED_LOW_EXCESS_COMMON_CARRIER.
```

It applies to the one selected global union, with the independent-union owner
at \(\kappa_{\rm sel}=0\) and the agreement-weighted transverse-secant owner
for \(1\le\kappa_{\rm sel}\le10\).  No cap is banked here because the TDD
alternative below can occur for other received pairs.

It remains to classify a genuinely high selected union:

\[
\kappa_{\rm sel}\ge11,\qquad |U_{\rm sel}|\ge R+11.
\tag{14}
\]

For three distinct slopes \(\gamma_i,\gamma_j,\gamma_k\), define

\[
\Delta_{ijk}
=
(\gamma_j-\gamma_k)c_i
+(\gamma_k-\gamma_i)c_j
+(\gamma_i-\gamma_j)c_k.
\tag{15}
\]

Because \(C\) is linear, \(\Delta_{ijk}\in C\).  The same affine combination
of the received words \(f+\gamma g\) vanishes, so

\[
\Delta_{ijk}
=-
\bigl(
(\gamma_j-\gamma_k)e_i
+(\gamma_k-\gamma_i)e_j
+(\gamma_i-\gamma_j)e_k
\bigr).
\tag{16}
\]

Therefore

\[
\operatorname{supp}(\Delta_{ijk})
\subseteq E_i\cup E_j\cup E_k.
\tag{17}
\]

If some \(\Delta_{ijk}\ne0\), the RS minimum distance gives

\[
|E_i\cup E_j\cup E_k|
\ge\operatorname{wt}(\Delta_{ijk})
\ge R+1
=1{,}048{,}577.
\tag{18}
\]

This is the terminal `UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT`.

## The common-code-line alternative

Suppose every defect (15) vanishes.  If \(|Z|\le1\), the family is already
small.  Otherwise fix two distinct slopes \(\gamma_1,\gamma_2\) and set

\[
q=\frac{c_2-c_1}{\gamma_2-\gamma_1},
\qquad
p=c_1-\gamma_1q.
\tag{19}
\]

Then \(p,q\in C\), and \(\Delta_{12i}=0\) gives

\[
c_i=p+\gamma_iq
\qquad(\gamma_i\in Z).
\tag{20}
\]

Put

\[
a=f-p,\qquad b=g-q,\qquad
W=\operatorname{supp}(a)\cup\operatorname{supp}(b),\qquad w=|W|.
\tag{21}
\]

Now

\[
e_i=a+\gamma_i b.
\tag{22}
\]

At any \(x\in W\), the affine function
\(\gamma\mapsto a(x)+\gamma b(x)\) is nonzero and therefore vanishes at at most
one finite slope.  Across \(m=|Z|\) distinct slopes, at least \(m-1\) of the
values at each \(x\in W\) are nonzero.  Using (3),

\[
(m-1)w
\le\sum_{i=1}^m|E_i|
\le mj,
\]

so

\[
w\le\left\lfloor\frac{mj}{m-1}\right\rfloor.
\tag{23}
\]

For \(m\ge2\), every point of \(W\) is nonzero for all but at most one selected
slope, so it belongs to at least one \(E_i\).  Hence

\[
W=U_{\rm sel}.
\tag{24}
\]

The smallest integer \(m\) for which (23) forces \(w\le R\) is

\[
m_0
=\left\lceil\frac{R}{R-j}\right\rceil
=\left\lceil\frac{R}{t}\right\rceil
=16.
\tag{25}
\]

Indeed,

\[
\left\lfloor\frac{16j}{15}\right\rfloor
=1{,}046{,}510<R,
\tag{26}
\]

whereas

\[
\left\lfloor\frac{15j}{14}\right\rfloor
=1{,}051{,}182>R.
\tag{27}
\]

Thus:

- if \(m\le15\), the high-union family has the trivial constant cap \(15\);
- if \(m\ge16\), equations (24) and (26) give
  \(|U_{\rm sel}|=|W|<R\), contradicting the high-union condition (14).

Therefore a high selected union with at least \(16\) slopes cannot have all
triple defects zero.  Some TDD (18) must occur.

For completeness, when the common-code-line alternative occurs before the
high-union restriction, each declared witness has transverse syndrome
incidence:

\[
s(f)+\gamma s(g)\in V_{E_\gamma},
\qquad
\{s(f),s(g)\}\not\subseteq V_{E_\gamma}.
\tag{28}
\]

The second assertion follows because simultaneous containment would explain
the pair on \(D\setminus E_\gamma\supseteq S_\gamma\).  The
independent-union ray theorem therefore applies to the carrier \(W\), with
\(|E_\gamma|\le j<R\), and gives

\[
|Z|\le j+1=981{,}105.
\tag{29}
\]

Hence the selected-family first-match classifier terminates exactly as

```text
CERTIFIED_LOW_EXCESS_COMMON_CARRIER
CERTIFIED_HIGH_UNION_SMALL_FAMILY_15
UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT
```

The first two are theorem-owned, budget-fitting alternatives but are not
separately added to \(U_{\rm paid}\) in this packet.  The third is an explicit
high-union primitive route cut, not an owner.

## Ledger effect

The predecessor ledger is

\[
U_{\rm paid,before}=2{,}602{,}220{,}945,
\qquad
B_{\rm remaining,before}=274{,}980{,}725{,}509{,}174{,}142.
\]

After the composite deep-owner extension (11),

\[
\begin{aligned}
U_{\rm paid,after}
&=2{,}602{,}502{,}999,\\
B_{\rm remaining,after}
&=274{,}980{,}725{,}508{,}892{,}088.
\end{aligned}
\tag{30}
\]

The exact primitive multiplier remains

\[
K_{\rm rem}=4{,}807{,}520.
\]

No carrier or small-family charge is banked separately: these are pair-level
alternatives to the unpaid TDD case, not additive global cells.  The packet
banks only the exact deep-owner extension.

\(U_2\), \(U_Q\), and \(U_A\) remain null.  Branches 4--5, the high-union TDD
residual, the field-full quadratic support union, and the complete row
inequality remain open.

## Reproducibility

```bash
python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py --write
python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_deep_ccl_tdd_v1.py --tamper-selftest

python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py --tamper-selftest
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --check
python3 experimental/scripts/verify_m1_kb_branch3_low_excess_carrier_cut_v1.py --tamper-selftest
```

The new verifier checks source hashes and theorem anchors, exact KoalaBear
arithmetic, the composite-owner delta, the exact \(15/16\) carrier threshold,
the CCL/TDD identities, two finite-field controls, schema/hash integrity, and
mutation rejection.

## Audit summary

- **Proof status:** GREEN for the deep-owner extension, exact shared-envelope
  accounting delta, and selected-family CCL/TDD dichotomy.  YELLOW for branch
  3 and the complete row.
- **Parameter dependence:** the witness lift and CCL/TDD proof are uniform for
  RS rows with \(j<R\); the printed threshold \(16\), charges, and ledger are
  KoalaBear-specific.
- **Layer-cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** exact integer arithmetic and exact finite-field
  controls only; neither is promoted into proof.

## Edge cases and nonclaims

- The error support is the actual nonzero support tied to a declared
  noncontained witness, not a padded co-support.
- Membership in the extended deep owner is intrinsic existence of one valid
  witness with \(|E_\gamma|\le r_*\).
- After deleting that owner, every valid witness has weight at least \(r_*+1\).
- Slopes are finite and distinct; the point at infinity is not included.
- The composite increment \(282{,}054\) is not a stand-alone branch-3 cap.
- The ambient deep-MCA cap \(349{,}526\) is sharp by the tangent floor, but
  sharpness for the literal post-first-match composite subset is not proved.
- The selected global union is tested against the integrated excess-\(10\)
  owner before the small/TDD split.
- A TDD is defined by \(\Delta_{ijk}\ne0\); the large triple union is its
  minimum-distance consequence.
- Failure to exhibit a CCL certificate does not itself prove a TDD.  The
  theorem proves the high-union dichotomy only after the actual decoded
  codewords are supplied.
- This packet does not pay
  `UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT`.
- This packet does not close branch 3, determine \(U_2,U_Q,U_A\), begin
  degree-three work, or prove the KoalaBear row safe.

## Minimal next action

Attack one object only:

```text
UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT
```

Use the three actual error supports and the nonzero RS codeword
\(\Delta_{ijk}\) to test, in first-match order, periodic/quotient ownership,
the integrated affine-core rank-\(\le3\) set-pair bound, and a deduplicated
minimum-distance support-union count.  Stop if a genuinely primitive TDD
component survives.
