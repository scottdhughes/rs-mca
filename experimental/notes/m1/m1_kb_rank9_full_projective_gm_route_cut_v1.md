# M1 rank-nine full-projective GM compatibility route cut v1

- **Status:** PROVED exact finite compatibility control / generic local
  emptiness shortcut refuted / no owner classification / no ledger movement.
- **Scope:** a declared proper retained family in one exact Reed--Solomon row;
  not the deployed KoalaBear row or domain.
- **Predecessors:**
  `m1_rank9_regular_locator_span_shortcut_refuted_v1.md` and
  `m1_kb_rank9_gm_mds_fixed_domain_gate_v1.md`.
- **Companion replays:**
  `verify_m1_kb_rank9_full_projective_gm_route_cut_v1.py` and
  `verify_m1_kb_rank9_full_projective_gm_route_cut_v1.sage`.

This packet closes one more proposed generic shortcut.  Full projective
syndrome field, full-degree extension slopes, the local rank-nine geometry,
and a GM--MDS-admissible fixed-domain rank-eleven locator tuple can all coexist
in one exact RS instance.  Those hypotheses therefore do not force emptiness,
a failed GM inequality, fixed-domain rank drop, or selector rank above nine.

The result is deliberately weaker than an owner or payment theorem.  The
declared family is a proper subfamily of the full bad-slope set, the deployed
first-match masks are not run, and no assertion is made that an existing owner
does or does not cover the control.

## 1. Exact field tower and row

Let

\[
 F=\mathbb F_2[\alpha]/
 (\alpha^{138}+\alpha^8+\alpha^7+\alpha+1),
 \qquad q_0=2^{23}.
\]

Put

\[
 v=\alpha^{(2^{138}-1)/(2^{23}-1)}.
\]

The exact verifier checks that \(v\) has order \(2^{23}-1\).  Hence

\[
 B=\{0\}\cup\langle v\rangle\cong\mathbb F_{2^{23}}
 \subset F,
 \qquad [F:B]=6.
\]

It also checks

\[
 \alpha^{q_0^e}\ne\alpha\quad(e=1,2,3),
 \qquad \alpha^{q_0^6}=\alpha.
\tag{1.1}
\]

Take

\[
 a=0,qquad b=1,qquad
 z_i=(1-v^{2^i})^{-1}\quad(0\le i<22),qquad c=v,
\]

and write \(\mathcal B=\{z_0,\ldots,z_{21}\}\).  The twenty-five
evaluation points

\[
 D=\{a,b\}\sqcup\mathcal B\sqcup\{c\}
\tag{1.2}
\]

are distinct and lie in \(B\).  Work with

\[
 C=\operatorname{RS}_F(D,13),
 \]

so

\[
 (n,k,R,j,A)=(25,13,12,11,14),
 \qquad R-j=1.
\tag{1.3}
\]

## 2. Extension of the five-pencil selector

Retain the five eleven-point cores from the locator-span counterexample.  For
each core, adjoining each of the eleven points outside it gives fifty-five
distinct twelve-point root sets \(Z\subset\mathcal B\).  Define

\[
 q_Z(X)=
 \frac{\prod_{z\in Z}(X-z)}{\prod_{z\in Z}(a-z)}\in B[X],
 \qquad
 \gamma_Z=q_Z(b)\in B^\times.
\tag{2.1}
\]

The binary exponents satisfy

\[
 \sum_{i=0}^{21}2^i=2^{22}-1<2^{23}-1.
\]

Consequently the products attached to all \(\binom{22}{12}=646{,}646\)
twelve-subsets are distinct; in particular the fifty-five \(\gamma_Z\) are
distinct.

Let \(1_x\) denote the word supported at coordinate \(x\), and put

\[
 f_0=1_a+\alpha1_c,
 \qquad g_0=1_b,
 \qquad f=f_0+\alpha g_0,
 \qquad g=g_0,
 \qquad \eta_Z=\gamma_Z+\alpha.
\tag{2.2}
\]

Characteristic two gives

\[
 f+\eta_Zg=f_0+\gamma_Zg_0.
\tag{2.3}
\]

Thus this word has values \(1,\gamma_Z,\alpha\) at \(a,b,c\),
respectively, and vanishes on \(\mathcal B\).  The polynomial \(q_Z\)
agrees on

\[
 \{a,b\}\cup Z,
\]

which has size fourteen.  Its discrepancy support is exactly

\[
 T_Z=\{c\}\cup(\mathcal B\setminus Z),
 \qquad |T_Z|=11,
\tag{2.4}
\]

because \(q_Z(c)\in B\) while \(\alpha\notin B\).

Every \(\eta_Z\) has degree six over \(B\): membership in any proper
intermediate field of degrees one, two, or three would put
\(\alpha=\eta_Z+\gamma_Z\) in the same field, contradicting (1.1).

## 3. Exact uniqueness and noncontainment

Fix \(Z\), and suppose a nonzero polynomial \(P\), \(\deg P\le12\),
agrees with \(f+\eta_Zg\) at at least fourteen points.  Let

\[
 r=|\{x\in\mathcal B:P(x)=0\}|,
 \qquad
 s=|\{x\in\{a,b,c\}:P(x)=(f+\eta_Zg)(x)\}|.
\]

Then

\[
 r+s\ge14,qquad r\le12,qquad s\le3.
\tag{3.1}
\]

Before using the base-field separation, the only possibilities are

\[
 (r,s)=(11,3),(12,2),(12,3).
\tag{3.2}
\]

No possibility in which \(c\) is an agreement can occur.

- If \(s=2\), then \(r=12\) and
  \(P=\lambda L_W\) for a base-field root product \(L_W\).  The other
  sparse agreement is at \(a\) or \(b\), with a nonzero value in \(B\),
  so \(\lambda\in B\).  Hence \(P(c)\in B\), contrary to
  \(P(c)=\alpha\).
- If \(s=3\) and \(r=12\), the same argument applies.  If \(r=11\), write
  \[
  P=L_W(uX+w).
  \]
  The equations \(P(a)=1\) and \(P(b)=\gamma_Z\), with nonzero
  base-field values of \(L_W(a),L_W(b)\), uniquely give \(u,w\in B\).
  Again \(P(c)\in B\), a contradiction.  Degree below twelve is included
  by allowing \(u=0\).

Therefore \(c\) is not an agreement.  Equations (3.1)--(3.2) force twelve
roots in \(\mathcal B\) and agreements exactly at \(a,b\).  Normalizing at
\(a\) gives \(P=q_W\) for a twelve-subset \(W\), while agreement at \(b\)
gives \(\gamma_W=\gamma_Z\).  The subset-product injection forces
\(W=Z\).

The zero polynomial is separate.  Its discrepancy support is exactly
\(\{a,b,c\}\), and \(\operatorname{supp}(g)=\{b\}\) is contained in that
support.  Hence \(Hg=h_b\) lies in the span of its support columns: the
zero-codeword witness is same-support contained and is rejected by the MCA
noncontainment gate.  Equivalently, every size-\(j\) padding \(T\) of its
discrepancy support contains \(b\), so
\(H_2\ell_T=\lambda_bL_T(b)=0\).  Both formulations are checked explicitly
in the exact replays.

Finally, if \(h_x\) is the weighted RS parity column at \(x\), then the
twelve columns indexed by \(T_Z\cup\{b\}\) are independent because
\(R=12\).  Thus

\[
 h_b\notin\operatorname{span}_F\{h_x:x\in T_Z\},
\tag{3.3}
\]

which proves support-wise noncontainment for \(q_Z\).  The fifty-five chosen
witnesses are therefore the unique noncontained complete selector on the
**declared** family \(\Gamma=\{\eta_Z\}\).

## 4. Full projective syndrome field

Let \(H\) be the weighted RS parity check.  Since all parity columns are
base-valued,

\[
 \operatorname{span}_F\{Hf,Hg\}
 =\operatorname{span}_F\{h_b,h_a+\alpha h_c\}.
\tag{4.1}
\]

This space has rank two.  Its coefficientwise \(q_0^e\)-Frobenius image
contains

\[
 h_a+\alpha^{q_0^e}h_c.
\]

The three columns \(h_a,h_b,h_c\) are independent, and (1.1) therefore
gives

\[
 \operatorname{rank}_F[Y\mid Y^{(q_0^e)}]=3
 \qquad(e=1,2,3),
\tag{4.2}
\]

where \(Y=[Hf\ Hg]\).

The Python and Sage replays also apply the same test to every proper
absolute subfield of \(F=\mathbb F_{2^{138}}\).  The proper divisor degrees
are

\[
 1,2,3,6,23,46,69,
\]

and in every case the augmented Frobenius rank is exactly three.  Thus no
incomparable proper subfield is missed by checking only the intermediate
fields over \(B\).  By the intrinsic projective-syndrome-field criterion,
consequently

\[
 F_{\rm proj}(f,g)=F.
\tag{4.3}
\]

This test is applied to the global syndrome pair, not a support quotient.

## 5. Preserved rank-nine and regular-locator geometry

Restricting the new error vectors to the old twenty-four coordinates recovers
the exact five-pencil errors.  Hence their raw and affine ranks are at least
ten and nine.  On the new coordinate, affine differences are evaluations of
the old polynomial differences at \(c\), hence a linear functional of their
old evaluation vectors.  The affine rank remains nine, and the raw family is
one vector plus that affine space, so its raw rank is ten.

The new locators are

\[
 L_{T_Z}(X)=(X-c)L_{\mathcal B\setminus Z}(X).
\tag{5.1}
\]

Multiplication by \(X-c\) is injective, so the locator-vector rank remains
eleven.  The ten frozen basis supports recover

\[
 V=\mathcal B\cup\{c\},
 \qquad |V|=23,
 \qquad |V|-R=11.
\tag{5.2}
\]

Since \(R-j=1\), the exact recurrence is a one-row Pad\'e--Hankel chart.
The verifier checks, for every declared slope,

\[
 M(\eta_Z)\ell_{T_Z}=0,
 \qquad H_2\ell_{T_Z}\ne0,
\tag{5.3}
\]

as well as full weight, transversality, nontangency, squarefreeness, and
base-field splitting.  This is local regular-chart compatibility, not
deployed first-match provenance.

## 6. GM--MDS representative

For the zero-based indices

\[
 (0,1,2,11,12,22,23,33,34,44,45),
\tag{6.1}
\]

the verifier enumerates all \(2^{11}-1=2047\) nonempty subsets and checks

\[
 |I|+\left|\bigcap_{i\in I}T_i\right|\le j+1=12.
\tag{6.2}
\]

The minimum slack, by \(|I|=1,\ldots,11\), is

\[
 (0,0,0,2,1,2,2,2,1,1,0).
\tag{6.3}
\]

All locator coefficients lie in \(B\), and their exact coefficient matrix has
rank eleven.  Thus one and the same control has

\[
 (\text{affine witness rank},\text{raw witness rank},
   \text{locator rank})=(9,10,11),
\tag{6.4}
\]

full projective syndrome field, degree-six slopes, and a GM-admissible
fixed-domain rank-eleven representative.

## 7. Exact conclusion and classifier semantics

The positive local terminal is

```text
FULL_PROJECTIVE_GM_DECLARED_FAMILY_COMPATIBILITY_CERTIFIED
```

and the only route cut is

```text
GENERIC_FULL_PROJECTIVE_OR_GM_EMPTINESS_SHORTCUT_REFUTED
```

In particular, the terminal is **not** `UNPAID_PRIMITIVE`.  The control proves
compatibility, not noncoverage by the existing owner catalogue.  The close
within-pencil supports may intersect a Johnson-type cell, and no owner mask is
executed here.

The following implication is false at the generic local level:

```text
base-domain
+ full-degree extension slopes
+ full projective syndrome field
+ regular transverse rank-nine declared selector
+ GM-admissible fixed-domain rank-eleven representative
=> emptiness, GM failure, specialization rank drop, or selector rank > 9.
```

The packet does not address a strengthened implication whose antecedent also
contains full retained-family exhaustion, deployed KoalaBear subgroup
geometry, and executable first-match survival.

Therefore

\[
 \Delta U_{\rm paid}=0,
 \qquad \Delta B_{\rm rem}=0.
\tag{7.1}
\]

## 8. Audit record

- **Dependencies:** the five-pencil construction and its rank witnesses are
  imported from the locator-span packet; the declared-tuple GM interface and
  the intrinsic projective-field criterion are imported from their named
  local sources.  The scalar extension, extra coordinate, twist, uniqueness
  proof, projective-field check, and simultaneous compatibility are proved
  here.
- **Parameter dependence:** exact at
  \((n,k,R,j,A)=(25,13,12,11,14)\) over
  \(\mathbb F_{2^{23}}\subset\mathbb F_{2^{138}}\).  There is no asymptotic
  claim and no hidden \(T,Y,L,\lambda\), or analytic constant.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** all controls are exact finite-field identities, not
  random evidence or a deployed census.
- **Local verdict:** GREEN for compatibility and the generic emptiness route
  cut.
- **Deployed payment verdict:** YELLOW.

This packet does **not**:

- instantiate the KoalaBear field, scale, or subgroup domain;
- assert that the declared fifty-five slopes exhaust the bad-slope set;
- prove survival of the deployed first-match order;
- execute periodic, quotient, planted, tangent, Johnson, B11, C5-payment, or
  sparse-sigma masks;
- classify the control as paid or unpaid by an existing owner;
- assert that all fifty-five supports jointly satisfy the GM inequalities;
- convert one eleven-support tuple into a complete-family slope count;
- move the ledger or close rank nine, branch 3, sparse sigma, or KoalaBear;
- attack intrinsic rank at least ten;
- authorize Lean or stable-paper promotion.

## 9. Minimal next action

Freeze a uniform deployed statement before building another local rank backend.
For every received pair reaching the regular rank-nine residual, it must bind
one complete retained selector to the actual first-match order and either:

1. produce a named paid owner/cap for that same selector; or
2. give a theorem converting a support/locator partition into a disjoint bound
   for every slope in the complete retained family.

The deployed subgroup geometry, complete-family exhaustion, and first-match
survival must be load-bearing.  A further toy certificate of one independent
locator tuple cannot move the ledger.
