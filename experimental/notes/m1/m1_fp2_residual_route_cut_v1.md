# M1 quadratic-parameter residual route cut v1

**Status:** PROVED SCALARIZATION / PROVED MASK-RELATIVE ROUTE CUT /
DECLARED CLASS EXHAUSTIVE / CLASS UNPAID / ROW OPEN.

This packet treats one row-uniform residual class at the KoalaBear MCA
agreement

\[
A=1{,}116{,}048.
\]

It does not sample received pairs.  For every admissible received pair it
classifies the complete degree-two parameter stratum relative to the frozen
earlier first-match assignments.  The class ends at an explicit scalarization
and incidence route cut `UNPAID_TOWER_DEGREE_2`; the earlier mask is retained
as a set-theoretic interface rather than falsely advertised as a locally
replayed equation atlas.  No value is assigned to \(U_2\), \(U_A\), or
\(U_Q\).

## Statement audited

Put

\[
B=\mathbb F_p\subset K=\mathbb F_{p^2}\subset F=\mathbb F_{p^6},
\qquad p=2{,}130{,}706{,}433,
\]

and let \(C_F=\operatorname{RS}_F(D,k)\), where
\(D\subset B^\times\), \(n=|D|=2{,}097{,}152\), and
\(k=1{,}048{,}576\).  For every received pair \((f,g)\in(F^D)^2\), let

\[
R_2(f,g)=
\operatorname{Bad}^{\mathrm{M1}}_{\mathrm{ap},>5}(f,g;A)
\cap(K\setminus B).
\]

If \(Z_r(f,g)\) is the actual slope projection assigned by branch \(r\), put

\[
Z_{<6}(f,g)=\bigcup_{r=1}^5 Z_r(f,g),
\qquad
\operatorname{Bad}_{\mathrm{ap},>5}^{\mathrm{M1}}
=\operatorname{Bad}_{\mathrm{ap}}^{\mathrm{M1}}\setminus Z_{<6}.
\]

Thus the subscript \(>5\) means the literal set-theoretic complement of the
actual slope projections assigned by the frozen first five branches.  It does
not assert that those branches are all paid, and it does not replace their
masks by a coarser support condition.  This packet binds that interface but
does not machine-encode the five predicates.  The field condition is exactly

\[
\gamma^{p^2}-\gamma=0,
\qquad
\gamma^p-\gamma\ne0.
\]

This is the smallest canonical extension-parameter class: the nonbase slopes
in \(F\) split disjointly according to minimal field degree \(2\), \(3\), or
\(6\).  Only the degree-two class is treated here.

## Lemma 1: exact quadratic-parameter scalarization

Choose a \(K\)-basis \(\beta_0,\beta_1,\beta_2\) of \(F\), and write

\[
f=\sum_{i=0}^2\beta_i f_i,
\qquad
g=\sum_{i=0}^2\beta_i g_i,
\qquad f_i,g_i\in K^D.
\]

For every \(\gamma\in K\), multiplication by \(\gamma\) is the diagonal
matrix \(\gamma I_3\) in this basis.  Hence

\[
\Psi_K(f+\gamma g)
=
(f_i+\gamma g_i)_{i=0}^2.
\]

Since \(D\subset B\subset K\), restriction of scalars gives

\[
\Psi_K(C_F)=C_K^3,
\qquad C_K=\operatorname{RS}_K(D,k).
\]

Consequently, for every support \(S\subseteq D\) with \(|S|=A\),

\[
(f+\gamma g)|_S\in C_F|_S
\quad\Longleftrightarrow\quad
(f_i+\gamma g_i)|_S\in C_K|_S
\quad(0\le i\le2).
\]

The pair-containment condition transfers coordinatewise as well.  Thus the
degree-two slope class is exactly a diagonal scalar line in the
three-interleaved code \(C_K^3\), with the same support and with the original
first-match mask retained symbolically as \(\gamma\notin Z_{<6}(f,g)\).

This is an exact retyping theorem, not a positive MCA estimate.  In
particular, \(\gamma\in K\) does not imply that the received pair, its
projective syndrome field, or its witness data descend to \(K\).

### Canonical three-leaf refinement

If a diagonal witness on \(S\) is noncontained, at least one coordinate pair
\((f_i,g_i)\) is noncontained on \(S\).  Assign the witness to the least such
index \(i\in\{0,1,2\}\).  This gives three disjoint, exhaustive
**witness-incidence** leaves.  On leaf \(i\), the same \(\gamma\) is scalar
MCA-bad for \((f_i,g_i)\) over \(K\), so

\[
R_2(f,g)
\subseteq
\bigcup_{i=0}^2
\left(
\operatorname{Bad}^{\mathrm{M1}}_{C_K}(f_i,g_i;A)
\cap(K\setminus B)
\right).
\]

The least-index assignment proves disjoint witness coverage; it does not make
the projected scalar bad-slope sets disjoint, and it does not preserve a paid
owner label from the original first-match ledger.  A future numeric bound must
deduplicate slopes within each received line and then take a supremum across
received lines.

## Lemma 2: exact fixed-support incidence

Let \(S\subseteq D\), \(|S|=A\), and put \(E=D\setminus S\).  Write
\(s(u)\) for the parity-check syndrome and let \(V_E(K)\) be the span over
\(K\) of the parity columns indexed by \(E\).  In the three-interleaved
syndrome space put

\[
\mathbf y_0=(s(f_0),s(f_1),s(f_2)),
\qquad
\mathbf y_1=(s(g_0),s(g_1),s(g_2)),
\qquad
W_E=V_E(K)^{\oplus3}.
\]

The exact support incidence is

\[
\mathbf y_0+\gamma\mathbf y_1\in W_E,
\qquad
\{\mathbf y_0,\mathbf y_1\}\not\subseteq W_E.
\]

Equivalently, after quotienting by \(W_E\),

\[
\overline{\mathbf y}_0+gamma\overline{\mathbf y}_1=0,
\qquad
(\overline{\mathbf y}_0,\overline{\mathbf y}_1)\ne(0,0).
\]

Therefore each fixed support contributes at most one slope.  In raw
interpolation coordinates this is a

```text
3A by (3k+1) = 3,348,144 by 3,145,729
```

affine system.  Eliminating the three degree-less-than-\(k\) polynomials
leaves

```text
3(A-k) = 202,416
```

affine syndrome equations in \([1,\gamma]\).  The two-column form does not
imply \(d_{\mathrm{eff}}\le1\): the unresolved operation is the exact union
over all surviving supports, not the solution count for one fixed support.

## Proposition 3: the existing routes do not pay this class

Put \(j=n-A=981{,}104\).  The currently available uniform gates fail at the
printed row:

\[
3j=2{,}943{,}312>1{,}048{,}576=n-k,
\]

so the deep MCA theorem does not apply;

\[
2j=1{,}962{,}208>1{,}048{,}576=n-k,
\]

so the half-distance conversion does not apply; and

\[
A^2=1{,}245{,}563{,}138{,}304
<2{,}199{,}021{,}158{,}400=(k-1)n,
\]

so the interleaved Johnson hypothesis does not apply.  The exact
restriction-of-scalars theorem supplies no additional band estimate.

The complete-absorption deficiency remains

\[
d=n+k-2A=913{,}632.
\]

Scalarization does not change it to \(d_{\mathrm{eff}}\le1\).  The previous
uniform-atlas audit proves that a bare complete-absorption binomial fits the
remaining budget in the declared compiler range only when
\(d_{\mathrm{eff}}\le1\).

Field membership alone also fails numerically.  Exact arithmetic gives

\[
|K\setminus B|=p^2-p
=4{,}539{,}909{,}901{,}496{,}877{,}056,
\]

while the current provisional remainder is

\[
B_{\mathrm{rem}}=274{,}980{,}725{,}509{,}241{,}614.
\]

The raw stratum exceeds the remainder by

\[
4{,}264{,}929{,}175{,}987{,}635{,}442,
\]

a factor between \(16\) and \(17\).  The coarse field polynomial

\[
\frac{Z^{p^2}-Z}{Z^p-Z}
\]

has exactly \(K\setminus B\) as its roots and the same nonfitting degree
\(p^2-p\).  Thus it is an exact root union, but not a budget-fitting one.

Even the hypothetical number of conjugate pairs is

\[
\frac{p^2-p}{2}
=2{,}269{,}954{,}950{,}748{,}438{,}528
>B_{\mathrm{rem}}.
\]

That division is not a valid fixed-line count in any event, as the following
control shows.

## Exact quadratic fixed-line control

Let

```text
B0 = F_7,
K0 = F_49 = F_7[a]/(a^2+1),
D0 = F_7^x = {1,2,3,4,5,6},
C0 = RS[K0,D0,3],
A0 = 5.
```

Define

```text
f = (-a,0,0,0,0,1),
g = ( 1,0,0,0,0,0).
```

Then

\[
\operatorname{Bad}^{\mathrm{M1}}(f,g;5)=\{a\}.
\]

Indeed, every five-support contains at least three of the four middle zero
coordinates.  A degree-less-than-three polynomial vanishing at those three
distinct base points is zero.  The only explained five-support is therefore
the first five coordinates at slope \(a\).  On that support neither \(f\) nor
\(g\) is itself explained.  Since \(a^7=-a\ne a\), the conjugate slope is not
bad for the same line.

The Python verifier enumerates all \(49\) slopes and all six five-supports;
Sage independently replays the same census.  This is a toy-scale falsifier of
automatic fixed-line Frobenius closure.  It has not been passed through the
deployed first five branches and is not evidence for the size of the deployed
residual.

Coefficientwise Frobenius gives only the between-pair covariance

\[
\operatorname{Bad}(f,g;A)^p
=
\operatorname{Bad}(f^p,g^p;A).
\]

It becomes a fixed-pair action only after proving an automorphism that
preserves the received pair and every first-match mask.  No such automorphism
is assumed here.

## Mask-relative exhaustive terminal decision

The three least-coordinate leaves have exact scalarization and syndrome
equations and cover the witness incidence over the declared set
\(R_2(f,g)\) for every received pair.  Their common post-5 mask remains the
external set-theoretic predicate \(\gamma\notin Z_{<6}(f,g)\); no local
branch-1--5 equation adapter is claimed.  Each currently has the terminal

```text
kind   = UNPAID_TOWER_DEGREE_2
reason = EXACT_ARITY3_DIAGONAL_RETYPE_NO_EXISTING_BAND_OWNER
charge = null
```

Here `TOWER_DEGREE_2` describes the parameter field only.  It does not assert
that the pair or witness descends.  The packet distinguishes:

```text
declared_post5_residual_class_complete = true
deployed_mask_replay_complete          = false
class_closed                           = false
row_complete                           = false
U_2                                    = null
U_Q                                    = null
U_A                                    = null
ledger_consequence                     = false
```

Thus the class terminates in an explicit route cut without being silently
forced into a paid owner.  A future refinement of any leaf must prove exactly
one of:

1. inclusion in a named paid owner, with a global-once charge;
2. a uniform complete-absorption injection with \(d_{\mathrm{eff}}\le1\);
3. a source-derived, within-line deduplicated exact-root union fitting the
   still-variable component reserve; or
4. a more refined equation-defined unpaid route cut.

For an eliminant \(E(Z)\), the exact proper-degree-two root polynomial can be
computed without enumerating \(K\) by taking the monic quotient

\[
H_E=
\frac{\gcd(E,Z^{p^2}-Z)}{\gcd(E,Z^p-Z)}.
\]

Multiple eliminants must be combined by a monic least common multiple, not by
summing their degrees.  Such an eliminant must also come with a consequence
certificate proving that it contains the full leaf.

## Dependencies

- **PROVEN:** the field partition and exact \(F/K\) restriction of scalars.
- **PROVEN:** the three least-noncontained-coordinate leaves are disjoint and
  exhaustive as witness-incidence leaves relative to the declared post-5
  residual.
- **PROVEN:** the fixed-support quotient incidence has at most one slope.
- **PROVEN:** the exact row arithmetic and the \(\mathbb F_{49}\) control.
- **PROVEN / INHERITED:** the current paid baseline and the
  \(d_{\mathrm{eff}}\le1\) bare-binomial budget wall.
- **UNPROVEN:** a paid scalar-\(K\) band owner, effective-deficiency collapse,
  or budget-fitting exact-root union.
- **OPEN:** \(U_Q\), \(U_A\), and the final KoalaBear inequality.

## Parameter dependence

The scalarization and fixed-support uniqueness are uniform in finite field
towers \(B\subset K\subset F\) with \([F:K]=3\) and evaluation domain in
\(B\).  The displayed budget and gate failures are exact and specific to the
printed KoalaBear row.  No asymptotic inference is made.

## Layer-cake / dyadic summability

Not applicable.

## Moment / Markov / Chebyshev

Not applicable.

## Edge cases and notation

- The slope field, projective syndrome field of the pair, and coefficient
  field of an eliminant are distinct objects.
- The earlier first-match mask is carried as the literal set difference
  \(\gamma\notin Z_{<6}(f,g)\); its five predicates are not machine-encoded in
  this packet.  Scalarization does not prove that a projected coordinate
  retains an earlier owner label.
- Exact-root deduplication occurs within one received line.  Across received
  lines the ledger takes a supremum or maximum, never a union or average.
- Infinity is outside \(R_2\); only finite slopes are classified.
- The symbols \(t=A-k=67{,}472\) and \(\tau=n-A=981{,}104\) are not
  interchangeable.
- A base-defined eliminant root set is Frobenius-stable; an arbitrary actual
  fixed-line bad set need not be.
- `null` is not zero.

## Numerical evidence

The deployed comparisons are exact integer arithmetic.  The
\(\mathbb F_{49}\) census is exhaustive toy-scale evidence backed by the
direct proof above.  No random or sampled atlas evidence is used.

## Verdict

**GREEN for the scalarization and mask-interface route cut; YELLOW for a
deployed equation atlas; RED as a payment or row closure.**

## Remaining risks

The coordinate union may overlap heavily or sparsely, and no current theorem
controls its within-line distinct-slope count in the deployed band.  A future
small eliminant could close this class without contradicting any route cut.
The component reserve remains unknown until \(U_Q\) and the rest of \(U_A\)
are separated disjointly.

## Minimal next action

Attack the row-uniform support-to-slope union in the exact two-column syndrome
system.  Freeze the original first-five-branch masks, classify its rank-one
and inconsistent components, and stop at the first compatible leaf that is
neither paid nor zero-dimensional.  Do not move to the degree-three or
full-degree extension strata until this degree-two class is refined.

## Replay

```bash
python3 experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py --check
python3 experimental/scripts/verify_m1_fp2_residual_route_cut_v1.py --tamper-selftest
/usr/local/bin/sage experimental/scripts/verify_m1_fp2_residual_route_cut_v1.sage
python3 experimental/scripts/verify_m1_extension_uniform_atlas_route_cut_v2.py --check
python3 experimental/scripts/verify_frontier_extension_fixed_line_audit_v1.py --check
python3 experimental/scripts/verify_kb_mca_1116048_base_slope_universe_v2.py --check
```
