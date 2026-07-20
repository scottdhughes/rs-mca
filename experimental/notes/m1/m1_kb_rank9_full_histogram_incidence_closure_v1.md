# M1 KoalaBear full-histogram incidence closure v1

Status: **PROVED LOCAL / FULL-HISTOGRAM TWO-RANGE CLOSURE / EXACT
142,082-LAYER \(x_0\le1\) SCALAR ROUTE CUT / INDEPENDENT REVIEW PENDING /
KOALABEAR ROW OPEN**.

This packet is a zero-ledger successor to the full-outside carrier-incidence
splice.  The predecessor fixed the imported M2b cutoff at \(D=18{,}014\) and
isolated the interval

\[
 67{,}467\le r\le236{,}097.
\tag{0.1}
\]

The first four layers of (0.1) do not require another M2b cutoff.  The
imported MDS row-basis floor applies to every selected slope and increases
with its nonnegative deficit.  Replaying the predecessor incidence argument
on the complete selected set gives

\[
 |\Gamma|\le
 \left\lfloor
  \frac{J_*(r)\binom{n-(t+r+1)}8}{\binom{t+8}8}
 \right\rfloor.
\tag{0.2}
\]

This is at most the remaining budget for

\[
 196\le r\le67{,}470
 \quad\text{or}\quad
 209{,}553\le r\le913{,}631.
\tag{0.3}
\]

Relative to the predecessor, this closes four layers at the lower endpoint
and 26,545 layers at the upper endpoint.  At \(r=67{,}471\), the moving-zero
floor jumps to \(x_0=1\).  For every integer through \(r=209{,}552\), an exact
abstract packing with \(B_{\rm rem}+1\) zero-deficit slopes satisfies every
scalar inequality used here and in the predecessor.  Thus the new residual is
a sharp determinant/source-packing route, not another cutoff-optimization
problem.

The paid terminal is

```text
PAID_FULL_OUTSIDE_FULL_HISTOGRAM_CARRIER_INCIDENCE
```

and the new local residual is

```text
UNPAID_FULL_OUTSIDE_X1_DETERMINANT_SOURCE_PACKING_SLACK_67471_TO_209552
```

No owner is charged.  Rank nine, non-full-outside source load, \(U_Q\),
residual \(U_A\), and the KoalaBear row remain open.

## 1. Frozen row and predecessor contracts

Fix the KoalaBear row

\[
 p=2{,}130{,}706{,}433,
 \qquad B=\mathbf F_p\subset F=\mathbf F_{p^6},
\]

\[
 n=2^{21}=2{,}097{,}152,
 \quad k=2^{20}=1{,}048{,}576,
 \quad A=1{,}116{,}048,
\]

\[
 j=n-A=981{,}104,
 \qquad t=A-k=67{,}472.
\tag{1.1}
\]

Work after the exact degree-195 owner deletion and the predecessor's
mandatory complete-selector restart.  Fix one received pair, its translated
source \(\Sigma\), one rebuilt complete affine-rank-nine selector, and the
full-outside coefficient-rank-two rich-pencil component of that selector.
Write

\[
 s=|\Sigma|=t+r+1,
 \qquad
 N_V=|V|\le n-s.
\tag{1.2}
\]

For every contributing graph line \(L\), import

\[
 x_L=|W_L|-j,
 \qquad
 h_L+u_L+\ell_L=r,
\tag{1.3}
\]

where \(h_L,u_L,\ell_L\ge0\).  Every selected finite slope \(\eta\) on
that line has deficit \(\delta_{\eta,L}\) satisfying

\[
 0\le\delta_{\eta,L}\le u_L.
\tag{1.4}
\]

The source-rational restart and the slack simplex give

\[
 x_L\ge x_0(r):=
 \left\lceil\frac{t-r+1}{2}\right\rceil.
\tag{1.5}
\]

The moving-zero theorem gives, for every selected slope set on \(L\),

\[
 J_Lx_L+
 \sum_{\eta\in\Gamma_L}\delta_{\eta,L}
 \le j+x_L.
\tag{1.6}
\]

Every selected slope has

\[
 \delta_\eta=j-|E_\eta|\ge0.
\]

The imported MDS row-flat theorem supplies at least

\[
 \binom{t+8+\delta_\eta}{8}
 \ge C_0:=\binom{t+8}{8}
 =10{,}658{,}592{,}438{,}443{,}717{,}273{,}371{,}372{,}062{,}592{,}575
\tag{1.7}
\]

independent eight-row bases in its actual zero mask.  This lower bound is for
every selected slope; it does not require that the slope lie on a rich line.

The fixed-basis affine-line lemma and the canonical rank-nine basis atlas are
imported with their same-selector provenance.  The predecessor printed the
atlas for one cutoff subset, but its proof is subset-uniform: restriction to
an independent eight-row basis forces every selected graph point containing
that basis onto one unique affine graph line.  Section 3 replays this argument
for the complete selected set.  The rich bases are partitioned by their unique
graph lines.  No selector, basis, graph line, or source datum from before an
exact deletion is reused.

The inherited ledger is

\[
 U_{\rm paid}=422{,}354{,}730{,}332,
 \qquad
 B_{\rm rem}=274{,}980{,}305{,}756{,}664{,}755.
\tag{1.8}
\]

## 2. Rich-line occupancy

### Lemma 2.1 (contributing-line deficits lie below the source slack)

For every contributing line and every selected slope on that line,

\[
 \boxed{0\le\delta_{\eta,L}\le r.}
\tag{2.1}
\]

#### Proof

Equations (1.3)--(1.4) and nonnegativity give

\[
 \delta_{\eta,L}\le u_L
 \le h_L+u_L+\ell_L=r.
\]

This is pointwise in the rebuilt selector and does not average over source
sizes or graph lines. \(\square\)

Lemma 2.1 is deliberately line-scoped.  A selected slope of multiplicity at
most twenty need not lie on a contributing rich line.  The complete-selector
lower double count in Section 3 uses the all-slope MDS bound (1.7), not a
coverage assertion for rich lines.

### Lemma 2.2 (uniform total line multiplicity)

Every contributing graph line satisfies

\[
J_L\le J_*(r):=
\begin{cases}
1+\left\lfloor j/x_0(r)\right\rfloor,&x_0(r)\ge1,\\[3pt]
j+1,&x_0(r)\le0.
\end{cases}
\tag{2.2}
\]

#### Proof

Discarding the nonnegative deficit sum in (1.6) gives

\[
 (J_L-1)x_L\le j.
\]

If \(x_0(r)\ge1\), then \(x_L\ge x_0(r)\) and

\[
J_L\le1+\left\lfloor\frac j{x_L}\right\rfloor
\le1+\left\lfloor\frac j{x_0(r)}\right\rfloor.
\]

If \(x_0(r)\le0\), split on the actual integer \(x_L\).  For \(x_L\ge1\),
the same calculation gives \(J_L\le j+1\).  For \(x_L\le0\), the imported
nonempty-moving-set inequality \(x_L+\delta_{\eta,L}\ge1\), summed over the
selected slopes and combined with (1.6), gives

\[
 J_L\le j+x_L\le j<j+1.
\]

\(\square\)

## 3. Total-selector incidence bound

Let \(m_B\) be the fixed-basis multiplicity for the full selected slope set.
By the all-slope MDS lower bound (1.7),

\[
 |\Gamma|C_0
 \le\sum_{B\in\binom V8}m_B.
\tag{3.1}
\]

For completeness, the atlas identity does not require a numerical cutoff.
Fix an independent eight-subset \(B\subseteq V\).  Restriction

\[
 \rho_B:K_0\longrightarrow F^B
\]

is an isomorphism.  For every selected error whose zero mask contains \(B\),
the zero equations uniquely force

\[
 w_\eta|_B=-u|_B-\eta v|_B.
\]

Hence all of its graph points lie on one unique affine graph line.  Conversely,
every independent basis in the common-zero set of a graph line has exactly
the selected slopes of that line.  Thus the rich bases are partitioned by
their unique lines for the full set \(\Gamma\), exactly as in the imported
cutoff proof.  The atlas identity and unique-line partition therefore give

\[
 \begin{aligned}
 \sum_Bm_B
 &\le20\binom{N_V}{8}
   +\sum_{L:J_L\ge21}\beta_L(J_L-20)\\
 &\le20\binom{N_V}{8}
   +(J_*(r)-20)\sum_L\beta_L\\
 &\le J_*(r)\binom{N_V}{8}.
 \end{aligned}
\tag{3.2}
\]

Combining (3.1)--(3.2) proves

\[
 \boxed{
 |\Gamma|\le
 \left\lfloor
  \frac{J_*(r)\binom{N_V}{8}}{C_0}
 \right\rfloor.}
\tag{3.3}
\]

The right side is increasing in \(N_V\), so the full-outside carrier bound
in (1.2) permits the uniform replacement

\[
 N_V\longmapsto N_V^{\max}(r):=n-(t+r+1).
\tag{3.4}
\]

This is the claimed bound (0.2).

## 4. Exact two-range closure

At the predecessor's first unpaid boundary and the next three integers, the
exact values are

\[
\begin{array}{c|r|r|r|r}
r&x_0(r)&J_*(r)&\text{full-histogram cap}&B_{\rm rem}-\text{cap}\\ \hline
67{,}467&3&327{,}035&167{,}238{,}042{,}774{,}200{,}802
 &107{,}742{,}262{,}982{,}463{,}953\\
67{,}468&3&327{,}035&167{,}237{,}360{,}939{,}443{,}806
 &107{,}742{,}944{,}817{,}220{,}949\\
67{,}469&2&490{,}553&250{,}855{,}274{,}346{,}888{,}378
 &24{,}125{,}031{,}409{,}776{,}377\\
67{,}470&2&490{,}553&250{,}854{,}251{,}601{,}007{,}573
 &24{,}126{,}054{,}155{,}657{,}182
\end{array}
\tag{4.1}
\]

Every margin is positive.  At the upper transition, where the uniform line
cap is \(j+1\), exact evaluation gives

\[
\begin{array}{c|r|r|r}
r&N_V^{\max}&\text{full-histogram cap}&B_{\rm rem}-\text{cap}\\ \hline
209{,}552&1{,}820{,}127&274{,}980{,}543{,}029{,}818{,}779
 &-237{,}273{,}154{,}024\\
209{,}553&1{,}820{,}126&274{,}979{,}334{,}408{,}472{,}994
 &971{,}348{,}191{,}761
\end{array}
\tag{4.2}
\]

For \(r\ge67{,}472\), \(J_*(r)=j+1\) is constant and
\(N_V^{\max}(r)\) decreases strictly.  Hence the full-histogram cap decreases
strictly.  Therefore (3.3), (4.1), and (4.2) prove

\[
 \boxed{|\Gamma|\le B_{\rm rem}
 \quad\text{for}\quad
 196\le r\le67{,}470
 \quad\text{or}\quad
 209{,}553\le r\le913{,}631.}
\tag{4.3}
\]

These layers are paid directly by the complete-selector count.  They are not
separate charges, and they are not summed over \(r\): a fixed translated
source determines one value of \(r\).

## 5. Sharp scalar route cut on \(67{,}471\le r\le209{,}552\)

At the next integer,

\[
 s=134{,}944,
 \quad N_V^{\max}=1{,}962{,}208,
 \quad x_0=1,
 \quad J_*=j+1=981{,}105.
\tag{5.1}
\]

The total-selector cap is

\[
 501{,}705{,}946{,}349{,}301{,}216,
\tag{5.2}
\]

which misses the budget by

\[
 \boxed{226{,}725{,}640{,}592{,}636{,}461.}
\tag{5.3}
\]

This failure cannot be repaired by choosing another scalar M2b cutoff.  Put

\[
 H=B_{\rm rem}+1=274{,}980{,}305{,}756{,}664{,}756
\tag{5.4}
\]

and distribute these abstract zero-deficit slopes among

\[
 L=\left\lceil\frac H{J_*}\right\rceil
 =280{,}276{,}123{,}103
\tag{5.5}
\]

abstract graph-line blocks.  Give each block \(C_0\) disjoint abstract bases.
The global basis capacity has margin

\[
 \binom{1{,}962{,}208}{8}-LC_0
 =2{,}463{,}116{,}790{,}168{,}985{,}034{,}614{,}201{,}267,
 312{,}489{,}378{,}894{,}656{,}291>0.
\tag{5.6}
\]

At the first endpoint, choose on every block

\[
 x=1,
 \quad e=\left\lceil\frac s2\right\rceil=67{,}472,
 \quad u=67{,}471,
 \quad h=\ell=0,
 \quad\delta_\eta=0.
\tag{5.7}
\]

Then the slack simplex and source floor hold with equality, the degree-195
owner does not apply, and the moving-zero inequality is sharp:

\[
 (J_*-1)x=j.
\tag{5.8}
\]

Each line has enough common-zero coordinates to carry its bases.  The exact
margin is

\[
 \binom{981{,}103}{8}-C_0
 =21{,}290{,}404{,}433{,}608{,}922{,}511{,}447{,}759,
 768{,}398{,}167{,}865{,}425{,}920>0.
\tag{5.9}
\]

Finally, every item has the cheapest M2b multiplicity \(\mu_0\), and

\[
 \binom{1{,}962{,}208}{9}-H\mu_0
 =862{,}666{,}766{,}649{,}480{,}960{,}575{,}314{,}819,
 776{,}481{,}566{,}949{,}948{,}488{,}656{,}500>0.
\tag{5.10}
\]

The same construction works at every integer through \(r=209{,}552\).  Keep
\(x=1\) and \(\delta_\eta=0\), put

\[
 e=\left\lceil\frac{t+r+1}{2}\right\rceil,
 \qquad u=e-1,
 \qquad h=r-u,
 \qquad\ell=0.
\tag{5.11}
\]

Then \(h,u\ge0\), \(h+u=r\), and \(x\ge x_0(r)\).  The line count in
(5.5) is unchanged, while all three ambient capacities decrease with \(r\).
Their exact margins at the tight upper endpoint remain positive:

\[
 \binom{1{,}820{,}127}{8}-LC_0
 =2{,}577{,}700{,}250{,}714{,}186{,}088{,}081{,}437{,}187,
 324{,}862{,}173{,}900>0,
\tag{5.12}
\]

\[
 \binom{839{,}022}{8}-C_0
 =6{,}090{,}483{,}505{,}083{,}391{,}560{,}362{,}880{,}461,
 341{,}367{,}491{,}591{,}320>0,
\tag{5.13}
\]

\[
 \binom{1{,}820{,}127}{9}-H\mu_0
 =278{,}492{,}477{,}489{,}381{,}568{,}181{,}757{,}395,
 229{,}031{,}467{,}606{,}347{,}581{,}541{,}575>0.
\tag{5.14}
\]

Because every deficit is zero, it remains in the low bin for every admissible
nonnegative cutoff.  Thus no fixed, maximal, or source-adaptive scalar
low/high split can exclude any integer in this residual interval.

This construction is deliberately an exact relaxation.  It does not build
graph points, determinant rows, Reed--Solomon polynomials, a complete
selector, or a KoalaBear counterexample.  It proves that the next useful
lemma must read deployed determinant/source coupling or supply a disjoint
named owner.

## 6. Ledger and revised residual

No new root owner is introduced, so

\[
 U_{\rm paid}:422{,}354{,}730{,}332
 \longrightarrow422{,}354{,}730{,}332,
\tag{6.1}
\]

\[
 B_{\rm rem}:274{,}980{,}305{,}756{,}664{,}755
 \longrightarrow274{,}980{,}305{,}756{,}664{,}755.
\tag{6.2}
\]

The full-outside slack partition becomes

- \(r=0\): earlier C5 boundary;
- \(1\le r\le195\): degree-195 source-Frobenius owner;
- \(196\le r\le67{,}470\): full-histogram carrier incidence;
- \(67{,}471\le r\le209{,}552\): unpaid \(x_0\le1\) determinant/source
  packing;
- \(209{,}553\le r\le913{,}631\): full-histogram carrier incidence.

## 7. Audit status and nonclaims

- **PROVED:** Lemmas 2.1--2.2, the total-selector incidence bound (3.3),
  the exact two-range payment (4.3), and the 142,082-layer scalar route cut.
- **IMPORTED/REPLAYED:** the degree-195 deletion and restart, source-rational
  floor, slack simplex, moving-zero equations, canonical basis atlas,
  full-outside carrier shrink, M2b multiplicity, and inherited ledger.
- **EXACT CONTROL:** Python big-integer endpoints, source bindings, JSON
  certificate, normal/optimized mutation tests, and Sage set-system controls.
- **UNPROVEN:** a deployed determinant/source theorem at \(x_0\le1\),
  non-full-outside source load, complete rank-nine payment, \(U_Q\), residual
  \(U_A\), and KoalaBear.
- **Parameter dependence:** Sections 1 and 4--6 use the exact KoalaBear row;
  Sections 2--3 are uniform under the printed same-selector hypotheses.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.
- **Numerical evidence:** all deployed arithmetic is exact.  Sage controls
  are toy-scale implication tests, not a deployed census or proof substitute.

This packet does not:

- introduce or charge a new owner;
- sum over source sizes, selectors, graph lines, or received pairs;
- replace a scalar relaxation by a deployed selector;
- reuse pre-deletion source, basis, line, or carrier data;
- close non-full-outside load, \(U_Q\), residual \(U_A\), rank nine, or
  KoalaBear;
- authorize rank at least ten, Lean, or stable-paper promotion.

The global verdict remains **YELLOW**.

## 8. Maximal next action

Freeze the first surviving integer

\[
 r=67{,}471,
 \qquad x_0=1.
\]

On its same-selector canonical graph lines, prove one of:

1. a determinant/source packing inequality that forbids the disjoint-basis
   scalar relaxation of Section 5;
2. a first-match executable owner for every compatible packed component; or
3. an explicit deployed primitive component with its support, regular-chart,
   source, and polynomial equations.

Stop immediately if a compatible primitive component survives.  Another
cutoff optimization, support-histogram moment, or broad random sweep cannot
close this boundary.
