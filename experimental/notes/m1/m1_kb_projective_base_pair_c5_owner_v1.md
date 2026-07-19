# M1 KoalaBear projective-base-pair C5 owner v1

Status: **PROVED JOINT \(\mathbf F_p\)-PROJECTIVE-PAIR OWNER AND
FULL-OUTSIDE SPLIT-MAXIMAL-GCD ABSORPTION / GENERAL MAXIMAL-GCD,
FIELD-FULL, AND LOWER-GCD ROUTES OPEN**.

This packet turns one previously unpriced C5 coverage cell into a deployed
KoalaBear distinct-slope owner.  It also closes the apparent nonstandard
subline obtained by changing the two coefficient coordinates of the
full-outside **split** maximal-gcd source \(G=L_C\) from the predecessor
packet.  It does not pay
proper-field strata of degree two or three, field-full local sublines,
lower-gcd rational maps, or the complete rank-nine residual.

## 1. Statement audited

Let

\[
 B=\mathbf F_p\subset F=\mathbf F_{p^6},\qquad D\subset B,
\]

and fix one received pair \(R=[r_0\ r_1]\).  Write \(Y_R=HR\) for its
global syndrome matrix and \(F_{\rm proj}(R)\) for the intrinsic field of
definition of its syndrome plane.  Let \(Z_a(R)\subset F\) be the set of
distinct finite exact-witness slopes.  Delete the actual first-match slope
projections of KoalaBear branches 1--5 and call the remainder

\[
 Z_{>5}(R)=Z_a(R)\setminus Z_{1:5}(R).
\tag{1.1}
\]

The new first-match cell is

\[
 \mathcal O_{C5,B}(R)=
 \begin{cases}
 Z_{>5}(R),&\operatorname{rank}Y_R>0
                 \text{ and }F_{\rm proj}(R)=B,\\
 \varnothing,&\text{otherwise}.
 \end{cases}
\tag{1.2}

It is inserted immediately after branches 1--5 and before the residual
extension-valued and base-slope buckets.  Importantly, (1.2) takes **all**
remaining finite slopes of a base-projective pair.  It is not restricted to
the extension-valued points of a displayed nonstandard subline.

## 2. Joint C5/base owner lemma

For every fixed received pair \(R\),

\[
 \#\mathcal O_{C5,B}(R)
 +\#\mathcal O_{\rm base}(R)\le p+1,
\tag{2.1}
\]

where \(\mathcal O_{\rm base}\) is the already-banked later
`residual_base_slope_universe` first-match cell under the new order.

### Proof

If \(\operatorname{rank}Y_R=0\), both received words are codewords and the
support-wise noncontained exact-witness fiber is empty.

Suppose \(F_{\rm proj}(R)=B\) and the rank is positive.  Projective syndrome
descent gives one \(A\in\operatorname{PGL}_2(F)\), depending on \(R\) but not
on a support, such that

\[
 \widehat Z_a(R)\subset A\mathbf P^1(B).
\tag{2.2}
\]

The right side has exactly \(p+1\) projective points.  Hence its intersection
with the source finite chart has at most \(p+1\) points.  Canonical C5
coverage is witness-exhaustive on the minimal-field stratum
\(F_{\rm proj}(R)=B\), after whatever realized earlier cells were removed.
Thus (1.2) contains every remaining slope and every later owner, including
the base-slope owner, is empty.  This proves (2.1) in this case.

If \(F_{\rm proj}(R)\ne B\), the new C5 cell is empty by definition.  The
later residual base-slope owner is a subset of \(B\), so it has at most \(p\)
finite slopes.  This proves (2.1) in the other case.

The two cases are pair-global minimal-field strata.  Therefore their caps
combine by a maximum,

\[
 \max\{p+1,p\}=p+1,
\tag{2.3}
\]

not by the sum \(2p+1\).  Earlier first-match deletions only shrink both
sets, so the argument does not require branches 1--5 to be executable from
this packet. \(\square\)

The older paid block used the uniform cap \(p\) for
`residual_base_slope_universe`.  Equation (2.1) replaces that block by the
joint cap \(p+1\); it does not add a second \(p+1\) charge.  Equivalently,
the pair-global \(F_{\rm proj}=B\) stratum is deleted before the still-open
\(U_A\) residual is defined.

## 3. Full-outside split maximal-gcd absorption

The predecessor's full-outside branch has a source support
\(\Sigma\subset D\) and a source pair which is zero off \(\Sigma\).  Restrict
now to the split maximal-gcd subcell

\[
 c_L=k-2,
\tag{3.1}
\]

so the \(k-2\) common roots are the distinct domain points
\(C\subset D\subset B\).  Coefficient rank two then gives

\[
 P=G(aX+b),\qquad Q=G(cX+d),\qquad ad-bc\ne0,
\tag{3.2}
\]

with monic common factor \(G=L_C\in B[X]\).  Define the base-valued pair

\[
 R_B=\bigl(\mathbf 1_\Sigma GX,\ \mathbf 1_\Sigma G\bigr)\in(B^D)^2.
\tag{3.3}
\]

Up to the harmless row/sign convention, the full source pair is

\[
 R_\epsilon=R_B
 \begin{pmatrix}a&c\\ b&d\end{pmatrix}.
\tag{3.4}

The matrix is invertible.  Therefore projective reparametrization sends the
source pair back to \(R_B\); restoring the two explaining codewords is a
codeword gauge.  The intrinsic syndrome field theorem gives

\[
 F_{\rm proj}(R)=B.
\tag{3.5}

The transverse source-syndrome hypothesis supplies positive rank (indeed
rank two), so the empty rank-zero exception does not occur.  Consequently
canonical C5 owns the entire remaining witness fiber of this pair.  A
nonstandard image \(A\mathbf P^1(B)\) in the original affine coordinates is
not a post-C5 primitive component; it is simply the projective image of the
base pair.

Thus the predecessor terminal

```text
UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2
```

is corrected, for this full-outside split-maximal-gcd source subcell, to

```text
PAID_PAIR_PROJECTIVE_BASE_SUBLINE_C5.
```

This conclusion is pair-global.  A support-dependent \(B\)-subline inside a
pair with \(F_{\rm proj}(R)=F\) need not descend: source values outside the
local plant can generate the full field, and different supports can produce
different sublines.  Such components remain

```text
UNPAID_NONSTANDARD_SUBLINE_FULL_PAIR_FIELD.
```

Nor does the degree statement
\(\deg\gcd(P,Q)=k-2\) by itself imply (3.1): the gcd can have non-domain or
nonbase roots, and a nonbase common factor need not be removable by one
projective change of the two pair coordinates.  The general maximal-gcd
terminal therefore remains open outside the split subcell:

```text
UNPAID_EXTENSION_SUBLINE_OUTSIDE_CARRIER_RANK2.
```

Together with the field-full local-subline case, the refined fail-closed
terminal is

```text
UNPAID_FULL_PROJECTIVE_OR_NONSPLIT_MAXIMAL_GCD_SUBLINE_OUTSIDE_CARRIER_RANK2.
```

If the common gcd has degree below \(k-2\), the reduced map has degree larger
than one in general and (3.3)--(3.4) do not follow.  Its terminal remains

```text
UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP.
```

## 4. Exact deployed ledger movement

For KoalaBear,

\[
 p=2{,}130{,}706{,}433.
\]

The existing base block charged \(p\).  Replacing it by (2.3) moves the
ledger by exactly one:

\[
\begin{aligned}
 U_{\rm paid}&:2{,}603{,}484{,}103
                   \longrightarrow2{,}603{,}484{,}104,\\
 B_{\rm remaining}&:274{,}980{,}725{,}507{,}910{,}984
                   \longrightarrow274{,}980{,}725{,}507{,}910{,}983.
\end{aligned}
\tag{4.1}
\]

The exact rank-nine one-cut replay at \(D=18{,}014\) gives

\[
 T_{18{,}014}:17{,}907{,}571{,}352{,}523
 \longrightarrow17{,}907{,}571{,}352{,}522,
\tag{4.2}
\]

and

\[
 E_{\max}=5{,}284{,}472{,}953{,}546{,}090{,}246{,}987{,}229{,}221,
 937{,}957{,}984{,}923{,}412{,}724.
\tag{4.3}
\]

The decrease in \(E_{\max}\) is exactly

\[
 \binom{67{,}480}{8}
 =10{,}658{,}592{,}438{,}443{,}717{,}273{,}371{,}372,
 062{,}592{,}575,
\tag{4.4}
\]

and \(K_{\rm remaining}=4{,}807{,}520\) is unchanged.  The row remains
open because \(U_Q\), the redefined residual \(U_A\), and the nonzero
rank-nine source-load tails are not paid.

## 5. Exact finite-field control

The companion Sage replay uses the repetition code over
\(B=\mathbf F_5\subset F=\mathbf F_{5^6}\).  It constructs a positive-rank
base pair whose six projective directions all have exact two-point
support-wise noncontained witnesses.  An invertible nonbase change of pair
coordinates produces a nonstandard \(B\)-subline with all \(p+1=6\) points
finite: one base slope and five extension slopes.  The syndrome-plane RREF
is nevertheless Frobenius-fixed, and the inverse coordinate change returns
the base pair.  Thus the \(p+1\) finite-chart cap is sharp and raw extension
coordinates do not imply a post-C5 component.

This is an exact toy-scale edge control.  Sections 2 and 3 contain the
symbolic proof and the deployed payment.

The same replay also protects the scope over
\(\mathbf F_{11}\subset\mathbf F_{11^2}\).  For the
\([9,3,7]\) RS code it takes \(G=X-\xi\), where
\(\xi\notin\mathbf F_{11}\), and \(P=GX,\ Q=-G\).  Here
\(\deg\gcd(P,Q)=k-2\) but \(c_L=0\).  Six exact weight-five witnesses survive,
the source syndrome rank is two, and its RREF has nonbase entries, so
\(F_{\rm proj}=\mathbf F_{11^2}\).  This is an exact countercontrol to
dropping the split-locator hypothesis; it is not a counterexample to the
joint owner, whose \(F_{\rm proj}=B\) premise fails.

## 6. Dependencies and scope

### Proved inputs

- The intrinsic projective syndrome field and projective subline confinement.
- Canonical proper-field C5 witness exhaustion after realized earlier cells.
- The KoalaBear numerator counts distinct finite slopes per received pair.
- The global `residual_base_slope_universe` owner has cap \(p\).
- The current deployed ledger and exact one-cut compiler from the tangent
  owner packet.
- The predecessor full-outside source equations and, on the additional
  \(c_L=k-2\) subcell, the split locator \(G=L_C\in B[X]\).

### Not proved here

- No payment for \(F_{\rm proj}=\mathbf F_{p^2}\) or
  \(\mathbf F_{p^3}\).
- No payment for a local nonstandard subline inside a field-full received
  pair.
- No absorption of a maximal-degree gcd whose full common factor is not
  proved to equal a base-domain locator.
- No reduction of lower-gcd rational maps to projective lines.
- No complete post-owner selector, source-load tail, value of \(U_Q\), or
  value of the remaining \(U_A\).
- No KoalaBear row closure, rank-at-least-ten work, Lean formalization, or
  stable-paper promotion.

## 7. Verdict

The joint \(F_{\rm proj}=B\) C5/base owner and its exact \(+1\) ledger
replacement are proved.  The full-outside split-maximal-gcd coefficient
deformation is absorbed by this owner.  The next honest route cuts are the
nonsplit/nonbase-gcd, pair-field-full, and lower-gcd residuals, not another
coefficient deformation of the same \(G=L_C\) base source.
