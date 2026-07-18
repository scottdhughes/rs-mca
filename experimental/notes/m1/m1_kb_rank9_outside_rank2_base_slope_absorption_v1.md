# M1 KoalaBear outside-rank-two base-slope absorption v1

Status: **PROVED EXISTING-OWNER ABSORPTION FOR THE PRINTED \(J=166\)
TEMPLATE / BROADER EXTENSION RESIDUAL OPEN**.

This packet audits the full-outside rank-two moving-root template printed in
`m1_kb_rank9_active_source_matroid_reindex_v1.md`, equations (6.9)--(6.11).
It corrects that template's routing terminal.  It does not pay the general
full-outside rank-two branch or prove the KoalaBear row safe.

## 1. Statement audited

The printed template has

\[
 D\subset \mathbf F_p^\times,
 \qquad W\subset D,
 \qquad P=L_CX,
 \qquad Q=-L_C,
\]

and its rich explaining polynomials are

\[
 P+\rho Q=L_C(X-\rho),\qquad \rho\in W.
\tag{1.1}
\]

The active-source packet selected 166 such slopes to expose the first point
where the ambient determinant cap can exceed the remaining budget.  The
question here is whether those 166 slope labels survive the already-frozen
first-match owners and therefore justify the terminal

```text
UNPAID_OUTSIDE_CARRIER_RANK2_MULTISELECTOR.
```

They do not.

## 2. Base-defined moving-root lemma

Let \(B=\mathbf F_p\subset F=\mathbf F_{p^6}\), let \(D\subset B\), and let
\(P,Q\in F[X]\).  Suppose the projective pencil descends to \(B\): for some
\(\lambda\in F^\times\),

\[
 \lambda P,\lambda Q\in B[X].
\tag{2.1}
\]

At a point \(x\in D\) which is not a common root of \(P,Q\), a finite
moving-root slope \(\eta\) is characterized by

\[
 P(x)+\eta Q(x)=0.
\tag{2.2}
\]

If \(Q(x)\ne0\), then

\[
 \eta=-\frac{\lambda P(x)}{\lambda Q(x)}\in B.
\tag{2.3}
\]

If \(Q(x)=0\), non-commonness gives \(P(x)\ne0\), so there is no finite
slope.  If \(P(x)=Q(x)=0\), the point belongs to the common gcd and does not
define a moving-root label; it must be deleted before the reduced rational
map is evaluated.  Thus every finite moving-root slope of a projectively
base-defined pencil on a base domain lies in \(B\).

This statement is projective.  A denominator zero is an infinity image, not
a finite slope.  Cancelling a common factor does not authorize reinserting
its deleted roots into the domain.

## 3. First-match absorption of the printed line

For (1.1), no scalar extension is even needed:

\[
 P,Q\in B[X],\qquad
 \eta_\rho=-P(\rho)/Q(\rho)=\rho\in W\subset D\subset B^\times.
\tag{3.1}
\]

The frozen first-match order places

```text
7. residual_base_slope_universe
8. sparse_sigma_or_sparse_support
```

after branches 1--6.  Therefore each displayed slope is either assigned to
an even earlier owner or, if still residual, to
`residual_base_slope_universe`.  No displayed slope reaches the sparse/rank-
nine branch.  After the mandatory post-owner selector rebuild, this printed
graph line has

\[
 J_{\mathrm{post\text{-}base}}=0.
\tag{3.2}
\]

Eight additional outlier records can change affine rank, the carrier, and
determinant data.  They cannot change the field membership of the 166 fixed
slope labels or resurrect them after first-match deletion.  They may create
other slopes; those must be classified from a rebuilt selector and are not
paid by this argument.

The corrected terminal for the printed line is

```text
PAID_BASE_SLOPE_UNIVERSE_BEFORE_SPARSE_SELECTOR
```

This is an ownership correction, not a new charge.  The global charge \(p\)
was already banked by the base-slope packet, so ledger movement here is zero.

## 4. Exact maximal-gcd residual normal form

The audit also identifies the first genuine extension-valued target.  If
\(\deg\gcd(P,Q)=k-2\) and the coefficient rank of \((P,Q)\) is two, then

\[
 P=G(aX+b),\qquad Q=G(cX+d),\qquad ad-bc\ne0.
\tag{4.1}
\]

After deleting the roots of \(G\), the projective moving-root map is the
Möbius transformation

\[
 \phi_M([X:Z])=[-(aX+bZ):cX+dZ],
 \qquad [M]\in\operatorname{PGL}_2(F).
\tag{4.2}
\]

The classifier is applied to this **gcd-reduced projective matrix**, up to
one common extension scalar.  Merely seeing a nonbase coefficient before
cancellation is insufficient: a nonbase common factor can cancel and leave a
base-defined reduced map.

Its image of \(\mathbf P^1(B)\) is a \(B\)-projective subline.  In what
follows, absorb the harmless base-field sign in the first row and let \(M\)
denote the actual homogeneous matrix of \(\phi_M\).  Let \(M^{(p)}\) denote
coefficientwise Frobenius and put

\[
 q_M(X,Z)=\det\!\left(M\binom{X}{Z},
                         M^{(p)}\binom{X}{Z}\right).
\tag{4.3}
\]

For \([X:Z]\in\mathbf P^1(B)\), the image \(M[X:Z]\) is a base projective
point exactly when \(q_M(X,Z)=0\).  If \([M]\) is nonstandard, meaning
\(M\notin F^\times M_2(B)\), then \(q_M\) is a nonzero homogeneous
quadratic and hence has at most two roots on \(\mathbf P^1(B)\).  Conversely,
if \(q_M\equiv0\), then every vector is an eigenvector of
\(M^{-1}M^{(p)}\); hence that matrix is scalar and projective Frobenius
descent gives \([M]\in\operatorname{PGL}_2(B)\).

Consequently a surviving maximal-gcd pencil has the exact dichotomy

```text
projectively base-defined  -> paid before sparse/rank nine;
nonstandard B-subline      -> at most two base points, extension part open.
```

The latter is the honest next terminal:

```text
UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2
```

If the common-gcd degree is below \(k-2\), the reduced quotient can have
degree greater than one.  Nothing here reduces it to a projective subline;
its separate terminal is

```text
UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP
```

## 5. Exact finite-field control

The companion Sage replay works over \(F=\mathbf F_{5^6}\) and
\(B=\mathbf F_5\).  It checks all 120 classes of
\(\operatorname{PGL}_2(B)\), a 625-matrix slice whose 580 invertible members
are genuinely nonbase, exact zero-, one-, and two-intersection examples, a
finite pole, common-factor deletion (including a common root at a pole),
rank-one degeneracies, and the zero matrix.  The nonbase invertible slice has
exact histogram

```text
intersection size 1:  80
intersection size 2: 500
```

and no intersection larger than two.  These are exact toy-scale controls for
the projective bookkeeping; the theorem in Sections 2 and 4 is the proof.

## 6. Dependencies and scope

### Proved inputs

- The MCA numerator counts distinct finite bad slopes, not witnesses,
  supports, or determinant charts.
- After branches 1--6, all remaining base-field slopes have the global-once
  owner `residual_base_slope_universe`.
- That owner precedes the sparse/rank-nine branch.
- The active-source template has \(W\subset D\subset B^\times\),
  \(P=L_CX\), and \(Q=-L_C\).

### Not proved here

- No global bound for slopes in \(F\setminus B\).
- No deployed complete-selector construction or payment for a nonstandard
  extension subline.
- No reduction of lower-gcd rational maps to the maximal-gcd subline case.
- No payment of the other source-load terminals in the predecessor packet.
- No value for \(U_Q\) or \(U_A\), and no safe KoalaBear row.

The current predecessor ledger is imported unchanged.  The older
base-slope packet has an earlier ledger snapshot; only its proved owner and
first-match position are consumed here.  Its historical paid total is not
substituted for the current stack's total.

## 7. Verification and verdict

Run the normal, optimized, mutation, Sage, and predecessor replays listed in
the certificate README.  The JSON certificate binds both predecessor
payloads, their notes and verifiers, this note, the exact Sage control, the
owner order, the 166-slope template, the zero ledger movement, and the two
honest extension terminals.

**Verdict:** GREEN for absorption of the printed \(J=166\) template;
YELLOW for the broader full-outside rank-two branch and the KoalaBear row.

The minimal next action is to rebuild the selector after base-slope deletion.
If a maximal-gcd extension pencil survives, freeze its nonstandard
\(B\)-subline incidence and classify it across the complete selector.  If
the gcd is smaller, freeze the first lower-degree rational map separately.
Do not return to the deleted base-defined graph line.
