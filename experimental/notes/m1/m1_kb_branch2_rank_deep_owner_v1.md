# M1 KoalaBear branch-2 rank/deep owner v1

**Status:** PROVED FIELD-NATIVE RANK-DROP POLICY / PROVED DEEP-MCA
OWNER WITH SHARP CHARGE / PROVED DEPLOYED BRANCH-2 CLOSURE / LEGACY
CYCLOTOMIC BRIDGE RETIRED AS NOT REQUIRED / PARTIAL UPPER LEDGER.

This packet closes the local `rank_drop_or_pivot_failure` branch at the
KoalaBear MCA candidate agreement

\[
A=1{,}116{,}048.
\]

It uses the field-native Hankel pencil supplied by Paper D and the finite-pivot
adapter of the predecessor packet.  It does not identify that pencil with the
older cyclotomic \(\mathcal O\)-valued row packet.  The older bridge is instead
retired from deployed branch 2 because the current base-slope-universe ledger
no longer uses it.

The resulting charge is one global distinct-slope charge

\[
67{,}472.
\]

The complete KoalaBear row remains open.  In particular this packet does not
close branches 3--5, the field-full quadratic support union, \(U_2\), \(U_Q\),
or \(U_A\).

## Statement audited

Let

\[
C=\operatorname{RS}_{F}(D,k),\qquad |D|=n,
\]

and let \(f,g:D\to F\) be one received pair.  At agreement \(A\), put

\[
R=n-k,\qquad j=n-A,\qquad t=A-k=R-j.
\]

For a finite slope \(\gamma\in F\), define the ambient field-native Hankel
matrix

\[
M_A(\gamma)
 =
H_{t,j}\bigl(\operatorname{Syn}(f+\gamma g)\bigr)
 =
H_{t,j}(\operatorname{Syn}(f))
 +\gamma H_{t,j}(\operatorname{Syn}(g)).
\]

The deployed rank-drop predicate is

\[
\operatorname{rank}_{F}M_A(\gamma)<t.
\]

It is the failure of full **row** rank of the
\(t\times(j+1)\) ambient matrix.  It is not:

- the overdetermined Paper-D predicate
  \(\operatorname{rank}<j+1\), which is automatic here because
  \(t<j+1\);
- the rank of the three-coordinate \(F/\mathbb F_{p^2}\) scalar stack; or
- a raw algebraic rank-drop condition divorced from an actual MCA-bad
  incidence.

For the bad-slope set \(Z_A(f,g)\), define the safe branch-2 rank envelope

\[
Z_{2,\mathrm{env}}(f,g)
 =
\left\{
\gamma\in Z_A(f,g):
\operatorname{rank}_{F}M_A(\gamma)<t
\right\}.
\]

If \(Z_1(f,g)\) denotes the earlier literal first-match cell, then the literal
branch-2 rank residual is

\[
Z_{2,\mathrm{fm}}(f,g)
=
\bigl(Z_A(f,g)\setminus Z_1(f,g)\bigr)
\cap Z_{2,\mathrm{env}}(f,g)
\subseteq Z_{2,\mathrm{env}}(f,g).
\]

The theorem proved here is the stronger envelope bound

\[
|Z_{2,\mathrm{env}}(f,g)|\le t
\]

for every received pair.  At the KoalaBear row this gives

\[
|Z_{2,\mathrm{env}}(f,g)|\le67{,}472.
\]

Consequently the same charge pays the disjoint literal first-match residual.
The envelope bound is sharp, so this owner cannot be uniformly lowered without
using additional information from branch 1.

## Exact support and actual error support

The exact-support reduction in
`experimental/rs_mca_thresholds.tex` says that every threshold-\(A\)
MCA-bad slope has an exact witness

\[
(\gamma,S,c),\qquad |S|=A,
\]

where \(c\in C\) explains \(f+\gamma g\) on \(S\), while the pair
\((f,g)\) is not simultaneously explained on \(S\).

Put

\[
y_\gamma=f+\gamma g,\qquad
e_\gamma=y_\gamma-c,
\qquad
E_\gamma=\operatorname{supp}(e_\gamma),
\qquad
s_\gamma=|E_\gamma|.
\]

Since \(e_\gamma\) vanishes on \(S\),

\[
E_\gamma\subseteq D\setminus S,
\qquad
s_\gamma\le j.
\]

The set \(D\setminus S\) is the chosen degree-\(j\) co-support.  It may contain
points where the actual error amplitude is zero.  Rank is controlled by
\(E_\gamma\), not by the padded co-support.

## Exact rank factorization

Use the Paper-D dual weights

\[
\lambda_x
=
\left(\prod_{\substack{y\in D\\y\ne x}}(x-y)\right)^{-1}
\]

and put

\[
w_x=\lambda_x e_\gamma(x)\ne0
\qquad(x\in E_\gamma).
\]

Let \(V_m(E)\) be the \(|E|\times m\) Vandermonde evaluation matrix

\[
V_m(E)_{x,a}=x^a,
\qquad x\in E,\quad0\le a<m.
\]

The \((a,b)\)-entry of the Hankel matrix is

\[
\begin{aligned}
M_A(\gamma)_{a,b}
&=\operatorname{Syn}(e_\gamma)_{a+b}\\
&=\sum_{x\in E_\gamma}w_xx^{a+b}.
\end{aligned}
\]

Therefore

\[
M_A(\gamma)
=
V_t(E_\gamma)^{\mathsf T}
\operatorname{diag}(w_x:x\in E_\gamma)
V_{j+1}(E_\gamma).
\tag{1}
\]

Because \(s_\gamma\le j\), the right Vandermonde matrix has row rank
\(s_\gamma\), so it maps \(F^{j+1}\) onto \(F^{E_\gamma}\).  The diagonal
map is invertible.  The left Vandermonde matrix has rank
\(\min(t,s_\gamma)\).  Hence

\[
\operatorname{rank}_{F}M_A(\gamma)
=\min(t,s_\gamma).
\tag{2}
\]

In particular,

\[
\operatorname{rank}_{F}M_A(\gamma)<t
\quad\Longleftrightarrow\quad
s_\gamma\le t-1.
\tag{3}
\]

This argument applies only after an actual explaining codeword has supplied
the nonzero amplitudes \(w_x\).  A received pair lying entirely in
\(C^{\equiv2}\) has \(M_A(\gamma)=0\) for every slope, but has no MCA-bad
slope.  Thus the raw algebraic rank-drop locus is not the counted object.

## Lift to the deep agreement

Set

\[
r_0=t-1,
\qquad
A_{\mathrm{deep}}=n-r_0=n-t+1.
\]

If \(\gamma\in Z_{2,\mathrm{env}}(f,g)\), equation (3) gives

\[
|E_\gamma|\le r_0.
\]

Enlarge the original exact witness support to the full agreement set

\[
S_\gamma^*=D\setminus E_\gamma.
\]

Then

\[
|S_\gamma^*|
=n-|E_\gamma|
\ge n-r_0
=A_{\mathrm{deep}},
\]

and the same codeword \(c\) explains \(y_\gamma\) on \(S_\gamma^*\).
Moreover \(S\subseteq S_\gamma^*\).  Noncontainment persists upward:
if \(f\) and \(g\) were simultaneously explained on \(S_\gamma^*\), their
restrictions would simultaneously explain the pair on \(S\), contradicting
the original witness.

Thus every \(\gamma\in Z_{2,\mathrm{env}}(f,g)\) is MCA-bad at agreement
\(A_{\mathrm{deep}}\).

Paper D's deep-MCA theorem gives, whenever

\[
3r_0\le n-k,
\]

at most \(r_0+1\) MCA-bad finite slopes at agreement \(n-r_0\).  Therefore

\[
|Z_{2,\mathrm{env}}(f,g)|
\le r_0+1
=t.
\tag{4}
\]

No separate tangent-case bridge is required: the full-agreement lift makes
the rank-drop slopes honest deep-radius MCA-bad slopes before the deep theorem
is applied.

## KoalaBear arithmetic

For

\[
\begin{aligned}
p&=2{,}130{,}706{,}433,\\
n&=2{,}097{,}152,\\
k&=1{,}048{,}576,\\
A&=1{,}116{,}048,
\end{aligned}
\]

one has

\[
\begin{aligned}
j&=981{,}104,\\
t&=67{,}472,\\
r_0&=67{,}471,\\
A_{\mathrm{deep}}&=2{,}029{,}681.
\end{aligned}
\]

The load-bearing gate is

\[
3r_0
=202{,}413
\le1{,}048{,}576
=n-k.
\]

The current paid baseline imported from the base-slope-universe packet is

\[
U_{\mathrm{paid,before}}
=2{,}602{,}153{,}473.
\]

Adding branch 2 globally once gives

\[
\begin{aligned}
U_{\mathrm{paid,after}}
&=2{,}602{,}220{,}945,\\
B_{\mathrm{remaining}}
&=274{,}980{,}725{,}509{,}174{,}142.
\end{aligned}
\]

The exact primitive multiplier remains

\[
K_{\mathrm{rem}}=4{,}807{,}520.
\]

The complete safe inequality remains undecided because later first-match
owners and \(U_2,U_Q,U_A\) are still open.

## Sharpness of the charge

The universal tangent-floor construction at the derived deep agreement
(`experimental/rs_mca_thresholds.tex`,
`prop:universal-tangent-floor`) shows that \(t\), rather than \(t-1\), is the
correct uniform envelope charge.

Choose \(t\) distinct coordinates \(x_1,\ldots,x_t\) and \(t\) distinct
slopes \(\gamma_1,\ldots,\gamma_t\).  Modulo a codeword-pair translation,
define

\[
g(x_i)=1,\qquad f(x_i)=-\gamma_i,
\]

and let both words vanish away from those coordinates.  For slope
\(\gamma_i\), the line error is supported on the other \(t-1\) coordinates.
It is MCA-bad at agreement \(n-(t-1)\), hence also at the lower agreement
\(A\), and equation (2) gives Hankel rank \(t-1<t\).

Thus one received pair can contribute \(t\) distinct slopes to the safe
branch-2 envelope.

## First-match integration

The frozen branch order begins

```text
1. contained or noncontained failure
2. rank-drop or pivot failure
3. tangent / common-line / residue-line
```

Writing \(Z_1\) for the prior literal first-match cell, the deployed branch-2
rank policy is:

```text
Z_2_env = Bad_A(f,g) intersect {gamma : rank_F M_A(gamma) < t}.
Z_2_fm  = (Bad_A(f,g) minus Z_1) intersect Z_2_env.
```

The proved envelope bound pays the disjoint literal cell \(Z_{2,\mathrm{fm}}\)
by assigning it to

```text
DEEP_MCA_RANK_DROP
```

with one global charge \(t\).  On the complement, the predecessor proves that
every actual finite support-wise noncontained incidence has a least nonzero
field-native Hankel pivot.  Hence:

- rank drop is paid by `DEEP_MCA_RANK_DROP`;
- pivot failure contributes zero actual bad slopes;
- full-row-rank, pivot-success slopes survive to branch 3.

This closes branch 2 relative to the bad-slope first-match universe.  It does
not make branch 1 or branches 3--5 executable, and it does not close the global
mask replay.

## Legacy cyclotomic bridge retirement

The predecessor left open a possible identification between

\[
(B_T)_h
\]

and the older cyclotomic symbol

\[
\operatorname{red}_p B_0(S).
\]

No such identification is proved here.

The current deployed base-slope packet replaced the old generated-collision
charge \(t p\) by the global residual-base-slope-universe charge \(p\).  It
explicitly requires no cyclotomic lift or affine-row adapter and retains the
old generated-collision lemma only as an optional refinement.

Therefore the cyclotomic identification is marked

```text
RETIRED_NOT_REQUIRED_FOR_DEPLOYED_BRANCH2
```

This is a branch-local dependency retirement, not a proof of equivalence and
not a claim that the older optional lemma is invalid.

## Exact controls

The Python verifier and independent Sage replay use

\[
\mathbb F_7,\qquad n=7,\qquad k=1,\qquad A=4,
\qquad j=t=3,\qquad r_0=2.
\]

They construct the sharp tangent-floor pair on three coordinates with slopes
\(0,1,2\).  Exhaustive support enumeration checks:

- exactly those three slopes are MCA-bad at agreement \(A=4\);
- all three have actual error weight \(2\);
- all three have ambient Hankel rank \(2<t=3\);
- each padded exact-\(A\) co-support has one zero-amplitude point;
- the same three slopes are MCA-bad at the lifted agreement \(5\);
- a contained codeword pair has rank zero for every slope but contributes no
  bad slope.

The control is exact toy-scale evidence and a mutation guardrail.  The
deployed theorem is the symbolic argument above.

## Dependencies

- **PROVEN / IMPORTED:** exact reduction from threshold-\(A\) witnesses to
  exact-\(A\) witnesses.
- **PROVEN / IMPORTED:** Paper-D weighted syndrome and field-native Hankel
  pencil.
- **PROVEN HERE:** the actual-error-support factorization (1) and exact rank
  identity (2).
- **PROVEN HERE:** the upward full-agreement lift of rank-drop witnesses.
- **PROVEN / IMPORTED:** Paper-D deep-MCA bound.
- **PROVEN / IMPORTED:** the predecessor's empty finite pivot-failure locus.
- **PROVEN HERE:** a safe branch-2 rank envelope, its literal first-match
  subset, and the sharp global envelope charge.
- **PROVEN HERE:** deployed branch-local retirement of the legacy bridge.
- **OPEN:** complete branch-1 and branches-3--5 projectors, field-full
  quadratic support-union payment, \(U_2,U_Q,U_A\), and the row inequality.

## Parameter dependence

The rank factorization and witness lift are uniform over finite fields and
Reed--Solomon evaluation domains with distinct points.  The deep charge is
uniform whenever \(3(t-1)\le n-k\).  The printed dimensions and ledger
arithmetic are KoalaBear-specific.

No hidden dependence on a support selector occurs: \(M_A(\gamma)\) depends
only on the received pair, the slope, and the fixed agreement \(A\).

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.

## Edge cases and notation

- \(T=D\setminus S\) is the padded co-support of size \(j\).
- \(E_\gamma\subseteq T\) is the actual nonzero error support.
- Zero amplitudes in \(T\setminus E_\gamma\) are omitted from the diagonal
  factorization.
- The empty error support gives rank zero, but is charged only when the slope
  is actually MCA-bad.
- Rank is ambient \(F\)-rank and the threshold is \(t\).
- The literal first-match rank cell subtracts branch 1 and is a subset of the
  safe rank-drop envelope bounded here.
- The charge counts distinct finite slopes globally once, not supports,
  witnesses, pivots, or charts.
- The derived deep agreement is \(n-t+1\), not \(n-t\).
- `null` remains different from zero.

## Numerical evidence

All deployed arithmetic is exact big-integer arithmetic.  The
\(\mathbb F_7\) census is exhaustive at toy scale.  It validates conventions,
padding, incidence scoping, and sharpness; it is not used as asymptotic
evidence.

## Verdict

**GREEN for the field-native rank-drop predicate, exact rank-to-weight bridge,
deep-MCA owner, sharp \(67{,}472\) charge, empty pivot-failure complement, and
deployed branch-2 closure.**

**YELLOW for the complete KoalaBear upper ledger and final row.**

## Remaining risks

The next global mask remains branch 3.  A tangent/common-line theorem used
there must operate only on full-row-rank branch-2 survivors and must not
recharge the deep rank-drop slopes.

The exact field-full quadratic support union remains open.  No value is
assigned to \(U_2,U_Q,U_A\).

## Minimal next action

Build one executable branch-3 tangent/common-line/residue-line projector on
the full-row-rank envelope complement

\[
Z_A(f,g)\setminus Z_{2,\mathrm{env}}(f,g).
\]

It must terminate every slope in a named paid owner or an explicit primitive
route cut.  Do not move to degree three, alter \(U_2,U_Q,U_A\), or claim the
complete row safe.
