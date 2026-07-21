---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: The target-field canonical Popov pair and the exact-error Pade pair have the same polynomial right kernel; their monic gcd recovers the discarded-agreement mask exactly. Every forced rank-46 key therefore has a direct simultaneous canonical rank-three frame. A target-field deformation dichotomy and an exhaustive GF(17) complete-layer witness cut off collision forcing from selected-family cardinality or four-root overlap coalescence alone.
architecture: GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1
partition_digest: 816f0702925f9734d230ffdfbf51a9d77aab2e1546918c722e1cc90227feafcc
atom_or_cell: U_new diagnostic refinement UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND; U_paid remains 3730 and U_Q, U_list-int, U_ext, and high U_new remain null
quantifier: Every received word over F_(p^4) and every marked key forced by a hypothetical forbidden list; the deformation lemma is conditional on proper collision forms; the GF(17) witness is an exact field-uniform falsifier, not a deployed survivor.
projection_and_unit: Distinct target-field codewords per received word; canonical padding roots, actual error roots, and collision-root resources remain typed and are not charged as owners.
claimed_bound: Every forced marked key has three simultaneous canonical locator-numerator syzygies of combined degree at most 62295<67447; the distinguished-column coloop is impossible; and the padding is recovered exactly. No additional atom value is proved. The target-field dichotomy isolates identically forced collision components, while the GF(17) model refutes a universal four-root transversal for the natural key collision unions.
status: PROVED
impact: ROUTE_CUT
falsifier: Failure of the product, interpolation, monic-gcd, right-kernel, diagonal-saturation, inclusive-cutoff, or direct-frame identities; failure of the exact target-field hyperplane count; or any claimed completeness, collision, or set-packing property of the sealed GF(17) witness.
replay: Python normal and optimized checks, hostile semantic mutations, independent Sage finite-field replay, predecessor replays, live source hashes, and fresh proof audits.
---

# M31 canonical masked Padé bridge and global route cuts

## Status

**PROVED TARGET-FIELD POPOV–PADÉ KERNEL BRIDGE / PROVED EXACT MASK
RECOVERY / PROVED SIMULTANEOUS CANONICAL RANK-THREE FRAME ON EVERY
GLOBAL KEY / PROVED NO-COLOOP / PROVED CONDITIONAL TARGET-FIELD
DEFORMATION DICHOTOMY / EXACT GF(17) FIVE-UNION FALSIFIER / LEDGER
MOVEMENT ZERO / M31 LIST ROW OPEN.**

This packet closes the algebraic padding/source compatibility wall.  It
does not close the row.  For an actual error locator $L$, discarded-agreement
padding locator $Q$, and canonical locator $W=LQ$, the source-computable
divided-difference numerator satisfies

\[
  \mathcal B_{\widehat\ell}(W)=Q\mathcal B_{\widehat\ell}(L),
  \qquad
  Q=\gcd\!\left(W,\mathcal B_{\widehat\ell}(W)\right).
\tag{0.1}
\]

With the standard weighted-dual normalization, the canonical interpolation
numerator $N=Wc$ also satisfies

\[
  N=\mathsf YW+\gamma^{-1}\Lambda_D\mathcal B_{\widehat\ell}(W).
\tag{0.2}
\]

Thus the canonical Popov pair $(W,N)$ and the masked Padé pair
$(W,\mathcal B(W))$ have exactly the same polynomial right kernel.  The
bridge respects, rather than evades, the known diagonal-saturation
obstruction: at an interior weight a reduced actual-error relation transports
back only when its coordinates are divisible by their individual padding
locators.

Two exact route cuts show what is still missing.

1. Over the deployed target field, either some collision form vanishes
   identically on the common containment space, or the entire forbidden-size
   selected family can be deformed to another received word while retaining
   all selected exact supports and eliminating all selected-selected
   collision roots.  The former branch is not yet a paid owner; the latter
   may create additional list members.
2. Over $\mathbb F_{17}$, an exhaustive complete exact layer has 92 genuine
   canonical keys and five pairwise disjoint nonempty natural collision-root
   unions.  Hence the displayed local coupled data do not force a
   four-point transversal for those unions.

The exact fail-closed terminal is

    UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND

## 1. Deployed contract and inherited source

Fix

\[
\begin{aligned}
 p&=2^{31}-1=2\,147\,483\,647,\\
 n&=2^{21}=2\,097\,152,\\
 K&=2^{20}=1\,048\,576,\\
 a&=1\,116\,023,\\
 R&=n-a=981\,129,\\
 w&=a-K=K-R=67\,447,\\
 B_*&=\left\lfloor p^4/2^{100}\right\rfloor=16\,777\,215,\\
 L_*&=B_*+1=2^{24}=16\,777\,216.
\end{aligned}
\tag{1.1}
\]

Let $\mathbb K=\mathbb F_{p^4}$, let
$D=(x_1,\ldots,x_n)\subset\mathbb F_p$ be the fixed ordered M31 evaluation
domain, and put

\[
  \Lambda_D(X)=\prod_{x\in D}(X-x).
\]

For a received word $y\in\mathbb K^D$, let $\mathsf Y\in\mathbb K[X]_{<n}$
be its interpolation polynomial.  Choose the standard dual weights

\[
  u_x=-\frac{\gamma}{\Lambda_D'(x)},
  \qquad \gamma\in\mathbb K^\times,
\tag{1.2}
\]

and define

\[
  \widehat\ell(f)=\sum_{x\in D}y(x)u_xf(x),
  \qquad f\in\mathbb K[X]_{<K}.
\tag{1.3}
\]

For $A\in\mathbb K[X]_{<K}$, define its divided-difference numerator by

\[
  \mathcal B_{\widehat\ell}(A)(Z)
  =\widehat\ell_X\!\left(
      \frac{A(X)-A(Z)}{X-Z}
    \right).
\tag{1.4}
\]

The predecessor source theorem proves the following directly over
$\mathbb K$.  If $c\in\mathbb K[X]_{<K}$ is a listed codeword with exact
error set $E$, $j=|E|\le R$, and monic locator

\[
  L=L_E=\prod_{\alpha\in E}(X-\alpha),
\]

then

\[
  \widehat\ell(HL)=0\quad\text{for every }\deg H<K-j,
\tag{1.5}
\]

and every one-point escape is nonzero:

\[
  \mathcal B_{\widehat\ell}(L)(\alpha)
  =\widehat\ell\!\left(\frac{L(X)}{X-\alpha}\right)\ne0
  \quad(\alpha\in E).
\tag{1.6}
\]

Let $T$ be the first $a$ agreement points of $c$ in the fixed domain order.
The discarded agreement set and its locator are

\[
  P=(D\setminus E)\setminus T,
  \qquad Q=L_P,
  \qquad \deg Q=R-j.
\tag{1.7}
\]

Then

\[
  W=LQ=L_{D\setminus T}
\tag{1.8}
\]

is monic, squarefree, $D$-split, and has degree $R$.  The roots of $L$ and
$Q$ are disjoint.  The first-$a$ rule makes $c\mapsto W$ injective.

## 2. Exact canonical masked bridge

### Theorem 2.1

For every listed codeword and the objects above:

\[
  \widehat\ell(X^tW)=0
  \qquad(0\le t<w);
\tag{2.1}
\]

\[
  \boxed{\mathcal B_{\widehat\ell}(W)
  =Q\mathcal B_{\widehat\ell}(L);}
\tag{2.2}
\]

\[
  \boxed{
  \gcd\!\left(W,\mathcal B_{\widehat\ell}(W)\right)=Q,
  \qquad
  L=\frac{W}{\gcd(W,\mathcal B_{\widehat\ell}(W))}.}
\tag{2.3}
\]

All gcds in this note are monic.  Consequently the actual error weight is
visible in the canonical pair:

\[
  j=R-\deg\gcd\!\left(W,\mathcal B_{\widehat\ell}(W)\right).
\tag{2.4}
\]

If $N=Wc$ is the canonical interpolation numerator, then

\[
  \boxed{
  c=\mathsf Y+\gamma^{-1}\frac{\Lambda_D}{W}
       \mathcal B_{\widehat\ell}(W),}
\tag{2.5}
\]

\[
  \boxed{
  N=\mathsf YW+\gamma^{-1}\Lambda_D
       \mathcal B_{\widehat\ell}(W).}
\tag{2.6}
\]

For any family indexed by $i$, put

\[
 H_B=
 \begin{pmatrix}
 W_1&\cdots&W_m\\
 \mathcal B(W_1)&\cdots&\mathcal B(W_m)
 \end{pmatrix},
 \qquad
 H_N=
 \begin{pmatrix}
 W_1&\cdots&W_m\\
 N_1&\cdots&N_m
 \end{pmatrix}.
\tag{2.7}
\]

Then

\[
 H_N=
 \begin{pmatrix}
 1&0\\
 \mathsf Y&\gamma^{-1}\Lambda_D
 \end{pmatrix}H_B,
 \qquad
 \boxed{\ker_{\mathbb K[X]}H_N=\ker_{\mathbb K[X]}H_B.}
\tag{2.8}
\]

The left matrix in (2.8) is injective over $\mathbb K[X]$ because its
determinant is the nonzero polynomial $\gamma^{-1}\Lambda_D$.  It is not
claimed to be unimodular, and (2.8) is an equality of right kernels rather
than row modules.

Finally, any polynomials $A_i$ satisfying

\[
  \sum_iA_iW_i=0,
  \qquad
  \max_i\deg A_i\le w,
\tag{2.9}
\]

also satisfy

\[
  \sum_iA_i\mathcal B(W_i)=0,
  \qquad
  \sum_iA_iN_i=0.
\tag{2.10}
\]

The cutoff in (2.9) is inclusive even though the recurrence in (2.1) is
strict.

### Proof

For $0\le t<w$,

\[
  \deg(X^tQ)\le(w-1)+(R-j)=K-j-1.
\]

Equation (1.5) therefore gives (2.1).

The polynomial product rule is

\[
\frac{L(X)Q(X)-L(Z)Q(Z)}{X-Z}
=
Q(Z)\frac{L(X)-L(Z)}{X-Z}
+
L(X)\frac{Q(X)-Q(Z)}{X-Z}.
\tag{2.11}
\]

If $Q=1$, the last term is zero.  Otherwise its multiplier of $L(X)$ has
$X$-degree at most $R-j-1<K-j$, so (1.5) kills it coefficientwise.
Applying $\widehat\ell_X$ proves (2.2).  Equation (1.6) gives
$\gcd(L,\mathcal B(L))=1$.  Since $L$ and $Q$ are disjoint, taking the
monic gcd of $LQ$ and $Q\mathcal B(L)$ proves (2.3) and (2.4).

To prove the interpolation identity, put $V=\Lambda_D/L$.  Orthogonality of
the standard dual weights gives, for every $f$ of degree less than $K$,

\[
 \widehat\ell(f)
 =\sum_{x\in D}(y(x)-c(x))u_xf(x).
\tag{2.12}
\]

At every $\alpha\in E$,

\[
\begin{aligned}
 \mathcal B(L)(\alpha)
 &= (y(\alpha)-c(\alpha))u_\alpha L'(\alpha)\\
 &= -\gamma\,
    \frac{y(\alpha)-c(\alpha)}{V(\alpha)}.
\end{aligned}
\tag{2.13}
\]

Both $\mathcal B(L)$ and $-\gamma(\mathsf Y-c)/V$ have degree less than
$j$ and agree at all $j$ roots of $L$.  For $j=0$ both are zero.  Hence

\[
  \mathcal B(L)=-\gamma\,\frac{\mathsf Y-c}{\Lambda_D/L}.
\tag{2.14}
\]

Substitute (2.2) and $W=LQ$ into (2.14) to obtain (2.5) and (2.6).
Equation (2.8) follows immediately.

For the inclusive cutoff, use the divided-difference identity directly:

\[
 \sum_iA_i(Z)\mathcal B(W_i)(Z)
 =
 \widehat\ell_X\!\left[
 \sum_i
 \frac{A_i(Z)-A_i(X)}{X-Z}W_i(X)
 \right].
\tag{2.15}
\]

Every displayed multiplier of $W_i(X)$ has $X$-degree at most $w-1$.
Equation (2.1) kills the right side.  This proves the first equality in
(2.10), including $\deg A_i=w$; (2.6) proves the second.  $\square$

### Canonical fiber predicate

Conversely, let $W$ be a monic degree-$R$ divisor of $\Lambda_D$ satisfying
(2.1).  The exact containment theorem gives a unique codeword whose error
support lies in $Z(W)$.  At a root $\alpha$ of $W$,

\[
  \mathcal B(W)(\alpha)
  =\widehat\ell\!\left(\frac{W(X)}{X-\alpha}\right).
\tag{2.16}
\]

Thus the actual error roots are exactly the roots of
$W/\gcd(W,\mathcal B(W))$, while the gcd roots are agreements.  If every
gcd root occurs after the last point of $D\setminus Z(W)$ in the fixed
ordering, then $D\setminus Z(W)$ is exactly the first $a$ agreement set.
This supplies a fixed, source-bound canonical masked zero-fiber predicate.

It also yields the exact source classification, with the predecessor cutoff
$J_0=614\,160$:

\[
\begin{array}{c|c}
\text{source class}&\deg Q\\ \hline
j=R\ \text{(boundary)}&0\\
J_0<j<R\ \text{(high interior)}&1\le\deg Q\le366\,968\\
j\le J_0\ \text{(banked low predicate)}&\deg Q\ge366\,969.
\end{array}
\tag{2.17}
\]

This is an algebraic classification.  Boundary does not automatically mean
the v4 $U_Q$ atom, and high interior is not automatically paid by
$U_{\rm list-int}$.

## 3. Fixed-layer saturation and collision typing

Fix one complete exact-weight layer.  Write

\[
  G=\gcd_iL_i,\qquad L_i=GP_i,\qquad
  \lambda(A)=\widehat\ell(GA),
\]

and set

\[
  C_G=\mathcal B_{\widehat\ell}(G),
  \qquad B_i^{\mathrm{red}}=\mathcal B_\lambda(P_i).
\]

The product expansion gives

\[
  \mathcal B_{\widehat\ell}(GP_i)
  =P_iC_G+B_i^{\mathrm{red}}.
\tag{3.1}
\]

Let $H_L$ have columns $(L_i,\mathcal B(L_i))^T$, let $H_{\rm red}$ have
columns $(P_i,B_i^{\rm red})^T$, and put
$\Delta_Q=\operatorname{diag}(Q_i)$.  Then

\[
 H_L=
 \begin{pmatrix}
 G&0\\ C_G&1
 \end{pmatrix}H_{\rm red},
 \qquad
 H_B=H_L\Delta_Q.
\tag{3.2}
\]

Both left multipliers are injective over the polynomial ring, so

\[
\boxed{
 \ker H_N=\ker H_B
 =\Delta_Q^{-1}\ker H_{\rm red}\cap\mathbb K[X]^m.}
\tag{3.3}
\]

Equivalently,

\[
\boxed{
 \Delta_Q(\ker H_B)
 =\ker H_{\rm red}\cap
   \bigoplus_iQ_i\mathbb K[X].}
\tag{3.4}
\]

At the boundary $Q_i=1$, the bridge is integral in both directions.  In the
interior, a reduced row transports back precisely when its $i$th coordinate
is divisible by $Q_i$.  This is the exact diagonal-saturation law.  It does
not identify the full reduced and padded kernels and does not contradict the
padding counterexample in #1014.

For two codewords in the layer, define

\[
 \Omega^W_{ik}
 =W_i\mathcal B(W_k)-W_k\mathcal B(W_i).
\]

If $Q^{\rm err}_{ik}=\gcd(P_i,P_k)$ and

\[
 c_k-c_i=L_{D\setminus(E_i\cup E_k)}h_{ik},
\]

then the target-field collision theorem and (3.1) give

\[
\boxed{
 \Omega^W_{ik}
 =\gamma Q_iQ_kGQ^{\rm err}_{ik}h_{ik}.}
\tag{3.5}
\]

The actual collision locator is

\[
  J_{ik}=\gcd(GQ^{\rm err}_{ik},h_{ik}),
\tag{3.6}
\]

not the entire factor on the right of (3.5).  Common actual-error core,
pair overlap, padding, and codeword collision remain distinct typed objects.
If a packet-wide common factor is first removed from the locator row, one
must divide (3.5) accordingly; both padding factors need not remain visibly
present in that reduced minor.

## 4. Simultaneous canonical rank-three frame

Fix one 46-column marked key forced by the source adapter.  Its columns are
45 canonical anchors and one distinguished excess codeword from a complete
high exact-weight layer.  Put

\[
  G_W=\gcd(W_1,\ldots,W_{46}),
  \qquad P_i^W=W_i/G_W,
  \qquad e=R-\deg G_W.
\]

The row $(P_i^W)$ is primitive, monic, and equal-degree.  Let its ordered
Forney indices be

\[
  0\le\lambda_1\le\cdots\le\lambda_{45}.
\]

The primitive equal-degree identity gives

\[
  \sum_{r=1}^{45}\lambda_r=e\le R.
\tag{4.1}
\]

At least one index is at least $w+1$.  Otherwise a full minimal basis would
have degree at most $w$, and Theorem 2.1 would make every basis row annihilate
both $(W_i)$ and $(\mathcal B(W_i))$.  Over $\mathbb K(X)$ this would force
all reduced fractions

\[
  \frac{\mathcal B(W_i)}{W_i}
  =\frac{\mathcal B(L_i)}{L_i}
\tag{4.2}
\]

to be equal.  The right fractions are reduced by (1.6), their monic
denominators have the same positive degree, and the 46 exact supports are
distinct.  This is impossible.  Therefore

\[
  \lambda_{45}\ge w+1=67\,448,
\]

and

\[
  \sum_{r=1}^{44}\lambda_r
  \le R-(w+1)=913\,681.
\tag{4.3}
\]

Exact integer balancing of the nondecreasing sequence gives

\[
\boxed{
 \lambda_1\le20\,765,\qquad
 \lambda_1+\lambda_2\le41\,530,\qquad
 \lambda_1+\lambda_2+\lambda_3\le62\,295<67\,447.}
\tag{4.4}
\]

The first three rows are therefore three independent simultaneous relations

\[
 \sum_iA_iW_i
 =\sum_iA_i\mathcal B(W_i)
 =\sum_iA_iN_i=0.
\tag{4.5}
\]

Deleting the distinguished column is injective on their
$\mathbb K(X)$-span: a kernel vector would be a locator syzygy supported on
one nonzero column, hence zero.  Rank three survives on the 45 anchors, so
the distinguished-coloop alternative is impossible.

Choosing a basis triple $I$ among the anchors, the complementary primitive
locator core obeys

\[
  \gcd(P_k^W:k\notin I)\mid\Delta_I,
  \qquad
  \deg\Delta_I\le62\,295,
\tag{4.6}
\]

where $\Delta_I$ is the corresponding $3\times3$ coefficient minor.
Equations (2.3), (3.5), and (4.5) now expose the padding, error, and collision
types on every forced key.  They do not supply a disjoint global owner or an
occupancy refund.

The numerical arithmetic in this section overlaps the prime-field sibling
#1022 and is reproved here so that this packet does not depend on that open
branch.  The new source-bound content is the target-field
$(W,N)\leftrightarrow(W,\mathcal B(W))$ kernel bridge, exact mask recovery,
diagonal saturation, and collision typing.

## 5. Target-field deformation dichotomy

Let $\mathcal S=(E_1,\ldots,E_{L_*})$ be any selected family of
$L_*=2^{24}$ distinct compatible exact supports of weights at most $R$.
Let $\mathscr L$ be their common containment-functional space:

\[
 \mathscr L=
 \left\{
 \ell:
 \ell(X^tL_{E_i})=0
 \text{ for all }i,\ 0\le t<K-|E_i|
 \right\}.
\tag{5.1}
\]

The original functional lies in $\mathscr L$.  For $x\in E_i$, the escape
form

\[
  \varepsilon_{i,x}(\ell)
  =\ell\!\left(\frac{L_{E_i}}{X-x}\right)
\tag{5.2}
\]

is linear and nonzero on $\mathscr L$, because the original exact functional
witnesses it.

For $x\in E_i\cap E_k$, define the collision form

\[
 \chi_{ik,x}(\ell)
 =L_{E_k}'(x)\varepsilon_{i,x}(\ell)
  -L_{E_i}'(x)\varepsilon_{k,x}(\ell).
\tag{5.3}
\]

After reconstruction, $\chi_{ik,x}(\ell)=0$ exactly when the two codewords
agree at their common error point $x$.  Properness of (5.3) on
$\mathscr L$ is an additional branch hypothesis; it is not implied by the
original functional when that functional already has a collision.

Pairwise MDS separation gives

\[
 |E_i\cap E_k|\le2R-K-1=913\,681.
\tag{5.4}
\]

The total number of escape and collision hyperplanes is therefore at most

\[
\begin{aligned}
 H
 &=
 L_*R+\binom{L_*}{2}(2R-K-1)\\
 &=128\,589\,177\,894\,085\,853\,184\\
 &<2^{67}=147\,573\,952\,589\,676\,412\,928\\
 &<p^4
 =21\,267\,647\,892\,944\,572\,736\,998\,860\,269\,687\,930\,881.
\end{aligned}
\tag{5.5}
\]

The exact margin below $2^{67}$ is

\[
  18\,984\,774\,695\,590\,559\,744.
\tag{5.6}
\]

A vector space over $\mathbb F_{p^4}$ cannot be covered by fewer than $p^4$
proper linear hyperplanes.  Hence exactly one of the following branches
holds:

1. some collision form (5.3) vanishes identically on $\mathscr L$; or
2. another functional in $\mathscr L$ avoids every escape and collision
   hyperplane.

In branch 2 every selected support remains exact for the received word
induced by the new functional, and no two selected codewords collide at a
common error point.  The induced received word may have additional exact
supports.  Thus this branch need not preserve complete-layer membership,
lexicographic anchors, common cores, collisions involving new codewords, or
the v4 first-match chronology.

This is a sharp route dichotomy, not a payment.  A collision-based closure
must exhibit an identically forced component and then classify it, or use
complete-list/cross-weight structure that the deformation does not preserve.
Selected-family cardinality and the local Padé identities alone cannot force
a collision owner.

## 6. Exhaustive GF(17) four-root-transversal falsifier

Work over $F=\mathbb F_{17}$ with

\[
 D=(0,1,\ldots,13),\quad n=14=2K,\quad K=7,\quad
 R=j=6,\quad a=8,\quad w=K-R=1.
\tag{6.1}
\]

Define

\[
 \ell\!\left(\sum_{r=0}^{6}q_rX^r\right)
 =4q_0+q_2+3q_3+4q_4+10q_5+8q_6.
\tag{6.2}
\]

With $u_x=1/\Lambda_D'(x)$, the received word

\[
 y=(4,3,11,5,13,6,9,0,0,0,0,0,0,0)
\tag{6.3}
\]

realizes (6.2) exactly.  For a six-subset $E\subset D$, put
$P_E=\prod_{x\in E}(X-x)$.  Exhausting all
$\binom{14}{6}=3003$ supports proves that the complete exact weight-six
layer is

\[
 \mathcal E=
 \left\{
 E:
 \ell(P_E)=0,\quad
 \ell(P_E/(X-x))\ne0\ \text{for every }x\in E
 \right\},
\tag{6.4}
\]

with

\[
 |\mathcal E|=137,
 \qquad
 \bigcap_{E\in\mathcal E}E=\varnothing.
\tag{6.5}
\]

The replay reconstructs all 137 degree-$<7$ codewords, checks all eight
agreements and six nonzero errors, and proves that the codewords are
distinct for this one received word.

Order $\mathcal E$ lexicographically by incidence vectors with $0<1$.  Freeze
the first 45 supports as anchors and use each of the remaining 92 supports
as one distinguished extra.  Since $j=R$, every $Q=1$.  Each key has the
coupled row

\[
 \left(P_E,\,
 \mathcal B_\ell(P_E)\right).
\tag{6.6}
\]

The exact replay proves:

- all 92 rows have rank two;
- all $92\binom{46}{2}=95\,220$ pair minors are nonzero;
- every key has at least 40 independent constant coupled relations; and
- all collision-factor and normalized-escape identities hold.

For an extra support $E_*$, define the natural anchor-collision union

\[
 \mathcal J(E_*)=
 \left\{
 x\in E_*:
 \exists\text{ anchor }E_i\ni x
 \text{ with }c_{E_i}(x)=c_{E_*}(x)
 \right\}.
\tag{6.7}
\]

An exact 14-bit set-packing computation over all 92 nonempty sets
$\mathcal J(E_*)$ has optimum five.  One attaining family is

\[
\begin{array}{c|c|c}
\text{global layer index}&E_*&\mathcal J(E_*)\\ \hline
93 &(0,3,6,7,9,13)&(9,13)\\
107&(0,2,4,7,9,10)&(4,7)\\
112&(0,2,3,7,12,13)&(2,3,12)\\
122&(0,1,4,8,10,12)&(8,10)\\
125&(0,1,4,5,6,7)&(5,6).
\end{array}
\tag{6.8}
\]

These five unions are pairwise disjoint and nonempty.  Exhaustive enumeration
of every subset of the 14-point domain gives the stronger exact transversal
number

\[
 \tau\!\left(\{\mathcal J(E_*):E_*\text{ is an extra}\}\right)=6.
\tag{6.9}
\]

There are exactly four minimum root transversals:

\[
\begin{aligned}
 &(3,5,6,7,8,9),\\
 &(3,5,7,8,9,13),\\
 &(3,6,7,8,9,12),\\
 &(6,7,8,9,11,12).
\end{aligned}
\tag{6.10}
\]

Thus no set of even five domain points meets every natural key collision
union.  Equivalently, the following parameter-uniform implication is false:

    complete exact same-weight layer for one received word
    + canonical shared 45 anchors
    + exact escapes and MDS separation
    + rank-two coupled rows
    + at least three low joint relations on every key
    + actual pair-collision factorization

      implies either disjoint packing number at most four
      or a four-point transversal for every natural
      anchor-extra collision-root union.

This does not refute arbitrary grouping into four polynomials, a non-root
owner, a larger eliminant, an M31-specific domain theorem, or a
chronology-valid refund.  It is an exact universal-claim falsifier, not
evidence for or against existence of a deployed M31 survivor.

The certificate also exhausts the weight-five exact layer of the same
received word.  Its four supports have nontrivial degree-one canonical
padding.  This independent fixture checks (2.2)–(2.8), monic gcd recovery,
both pair-minor padding factors, and equality of the two polynomial right
kernels through multiplier widths one to six.  It is a guard for the
load-bearing bridge, not an additional theorem.

## 7. Consequence for the v4 residual

The first-match status remains

    U_paid     = 3730       BANKED by #1029
    U_Q        = null
    U_list-int = null
    U_ext      = null
    U_new      = null       high residual unpaid

The positive theorem removes the old unspecified algebraic padding bridge
and the distinguished-coloop branch.  It also supplies an exact
source-bound boundary/interior classifier and makes the canonical Popov,
masked Padé, actual-error, and reduced common-core rows compatible.

Neither route cut supplies a v4 atom:

- an identically forced collision form is an algebraic component, not a
  named owner;
- the deformation branch can change the complete list;
- a five-set packing blocks only the stated four-root-transversal inference;
- mask recovery is classification, not payment; and
- no signed occupancy credit has been refunded.

The exact diagnostic terminal is therefore

    UNPAID_CANONICAL_MASKED_COLLISION_OWNER_REFUND

A closing theorem must now do at least one of the following:

1. classify every identically forced collision component and route it to
   disjoint chronology-valid owners with exact charges and refunds;
2. prove an M31-domain/cross-weight complete-list incidence theorem robust to
   both route cuts;
3. eliminate the remaining primitive masked component by a new global
   eliminant; or
4. directly bound the complete distinguished-codeword projection by
   $259\,880$.

Another standalone fixed-width locator, gcd, Plücker, or local-rank
calculation cannot provide one of these conclusions by itself.

## 8. Provenance, falsification, and replay

This packet is stacked on #1029, whose ancestors are the exact full-layer
source theorem #1023 and coupled actual-error theorem #1028.  It reads the
active Grande Finale v4 LIST chronology without assigning any new atom.

The diagonal-saturation law agrees with #1014.  The rank-three/no-coloop
arithmetic overlaps #1022 but is reproduced here over the target field and
is not imported as an ancestry dependency.  No open upstream PR supplies the
combined target-field Popov–Padé bridge, exact mask classifier, deformation
dichotomy, and exhaustive complete-layer regression.

The verifier fails closed under mutations of:

- the strict recurrence or inclusive syzygy endpoints;
- the product, interpolation, gcd, right-kernel, or saturation identities;
- the distinction between padding, error overlap, and collision;
- the $62\,295<67\,447$ frame arithmetic or no-coloop conclusion;
- the exact hyperplane count, field comparison, or conditional branch scope;
- the GF(17) field, received word, complete layer, ordering, support count,
  pair minors, collision identities, or set-packing optimum;
- any claim of M31 counterexample, ledger payment, or row closure; and
- any bound-source hash or payload seal.

The certificate README records the exact normal Python, optimized Python,
mutation, Sage, predecessor, schema, and hash-replay commands.  There is no
analytic layer-cake, Markov, Chebyshev, or probabilistic moment argument.
All displayed finite arithmetic is exact.

## 9. Nonclaims

- The M31 list row is not closed.
- No forbidden deployed received word is constructed.
- No integer is assigned to $U_Q$, $U_{\rm list-int}$, $U_{\rm ext}$, or
  high $U_{\rm new}$.
- The canonical and reduced row modules are not claimed equal.
- Interior divisibility is not automatic.
- An identically forced component is not automatically a paid owner.
- The deformed selected family need not remain the complete list.
- The GF(17) witness does not refute arbitrary four-polynomial or non-root
  owners.
- No stable-paper theorem, endpoint, official score, or Lean claim changes.
