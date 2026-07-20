# M1 KoalaBear bounded-slack effective-multiplier Frobenius owner v1

Status: **PROVED LOCAL / ALL FULL-OUTSIDE SLACK LAYERS \(1\le r\le195\)
CLOSED / EXACT \(r=196\) INHERITED-LEDGER ROUTE CUT / INDEPENDENT PROOF
AND ARTIFACT REVIEWS GREEN / KOALABEAR ROW OPEN**.

This packet replaces, rather than supplements, the four-anchor moving-cofactor
owner from the predecessor.  The replacement is one pair-global 392-anchor
source-Frobenius eliminant.  Its root cap is

\[
 196(p+1)=417{,}618{,}461{,}064.
\tag{0.1}
\]

It closes every full-outside coefficient-rank-two rich record with

\[
 1\le r=s-t-1\le195.
\tag{0.2}
\]

The same local algebra works through \(m=9{,}208\), but that larger charge
destroys the inherited rank-nine accounting gate.  Exact optimization shows
that \(m=195\) is the largest replacement preserving both the one-cut gate and
a nonnegative aggregate-excess allowance.  At \(r=196\), the one-cut gate
still exists but its allowance is negative.  This is an accounting route cut,
not a claim that the \(r=196\) algebra fails.

The paid terminal is

```text
PAID_PAIR_GLOBAL_SOURCE_FROBENIUS_EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_195
```

and the new local residual is

```text
UNPAID_FULL_OUTSIDE_SOURCE_SIZE_AT_LEAST_67669
```

Rank nine, \(U_Q\), residual \(U_A\), non-full-outside source load, and the
KoalaBear row remain open.

## 1. Frozen row and imported contracts

Fix

\[
 p=2{,}130{,}706{,}433,
 \qquad B=\mathbf F_p\subset F=\mathbf F_{p^6},
 \qquad D\subset B^\times,
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

Fix one received pair, its one SP3 translation, its source

\[
 \Sigma=\operatorname{supp}(\epsilon _0)
       \cup\operatorname{supp}(\epsilon _1),
 \qquad s=|\Sigma|,
\]

and the source pencil

\[
 S_a(Z)=\epsilon _0(a)+Z\epsilon _1(a)
 \qquad(a\in\Sigma).
\tag{1.2}
\]

The pair, translation, source, domain order, and polynomials \(S_a\) are
fixed before every selector.  Alternative translations are not unioned.

We import the exact post-C5/source-rational/common-twist contracts:

1. a qualifying record is full-outside, has coefficient rank two, and has a
   selected finite slope;
2. \(H=\gcd(P,Q)\) is the full monic gcd and
   \(P=H\bar P,\ Q=H\bar Q,\ \gcd(\bar P,\bar Q)=1\);
3. \(L_C\mid H\), where \(C\) is the forced outside-source set;
4. for every selected finite slope,
   \[
    \bar P+\eta\bar Q=L_{F_\eta}A_\eta,
    \qquad L_{F_\eta}\in B[X];
   \tag{1.3}
   \]
5. with
   \[
    r=s-t-1,
    \quad h=\deg H-|C|,
    \quad u=e-x,
    \quad \ell=k-1-\deg H-e,
   \tag{1.4}
   \]
   one has
   \[
    h+u+\ell=r,
    \qquad 0\le\delta_\eta\le u,
    \qquad \deg A_\eta\le u-\delta_\eta;
   \tag{1.5}
   \]
6. \(x\le49{,}055\) and the source-rational restart gives
   \[
    e\ge\left\lceil\frac{s}{2}\right\rceil.
   \tag{1.6}
   \]

All conclusions below are subset-stable: after any exact earlier deletion,
they apply to every complete selector rebuilt on the remaining slope set.

## 2. Uniform effective multiplier

Write

\[
 H=L_CG,
 \qquad \deg G=h,
\tag{2.1}
\]

and define, for each selected slope,

\[
 B_\eta=GA_\eta.
\tag{2.2}
\]

By (1.5),

\[
 \boxed{
 \deg B_\eta
 \le h+u-\delta_\eta
 =r-\ell-\delta_\eta
 \le r.}
\tag{2.3}
\]

Thus one degree-\(m\) owner covers every nonnegative profile
\((h,u,\ell)\) with \(h+u+\ell=r\le m\), including every allowed deficit.
For \(1\le r\le195\), the exact simplex contains

\[
 \sum_{r=1}^{195}\binom{r+2}{2}
 =\binom{198}{3}-1
 =1{,}274{,}195
\tag{2.4}
\]

profiles.  If deficits are retained as separate shapes, their number is

\[
 \sum_{r=1}^{195}\binom{r+3}{3}
 =\binom{199}{4}-1
 =63{,}391{,}250.
\tag{2.5}
\]

These counts are descriptive checks, not union factors in the slope ledger.

Because \(C,F_\eta,\Sigma\) are pairwise disjoint, their locator values are
nonzero on \(\Sigma\).  Source coupling and (1.3) give, for every
\(a\in\Sigma\),

\[
 S_a(\eta)=L_C(a)L_{F_\eta}(a)B_\eta(a).
\tag{2.6}
\]

The product \(L_C(a)L_{F_\eta}(a)\) lies in \(B^\times\).

Uniformly in \(r\),

\[
 e=x+u\le49{,}055+r,
 \qquad s=t+r+1,
\]

so every nonzero reduced pencil member has source support at least

\[
 s-e\ge t+1-49{,}055=18{,}418.
\tag{2.7}
\]

The smallest reduced-degree floor among all retained layers occurs at
\(r=1\):

\[
 e\ge\left\lceil\frac{67{,}474}{2}\right\rceil=33{,}737.
\tag{2.8}
\]

This corrects the tempting but false uniform value \(33{,}738\), which is
valid only starting at \(r=2\).

## 3. The source-Frobenius eliminant

For a fixed integer \(m\ge1\) and an ordered anchor set
\(T_0\subset\Sigma\) of size \(2(m+1)\), define

\[
 E_{T_0,m}(Z)=
 \det_{a\in T_0}
 \left[
  a^iS_a(Z)^p\ (0\le i\le m)
  \;\middle|\;
  a^iS_a(Z)\ (0\le i\le m)
 \right].
\tag{3.1}
\]

Let \(B_\eta(X)=\sum_{i=0}^m b_iX^i\), padding with zero coefficients.
Equation (2.6), together with the fact that its locator multiplier is in
\(B^\times\), gives

\[
 B_\eta(a)S_a(\eta)^p-B_\eta(a)^pS_a(\eta)=0.
\tag{3.2}
\]

Hence

\[
 (b_0,\ldots,b_m,-b_0^p,\ldots,-b_m^p)
\tag{3.3}
\]

is a nonzero kernel vector for (3.1) at \(Z=\eta\).  Therefore every selected
slope with \(\deg B_\eta\le m\) annihilates every determinant (3.1).

The first block contributes degree at most \((m+1)p\), and the second block
degree at most \(m+1\).  Thus

\[
 \deg E_{T_0,m}\le(m+1)(p+1).
\tag{3.4}
\]

For the deployed value \(m=195\), (3.1) has 392 anchors and

\[
 \deg E_{T_0,195}
 \le196(p+1)=417{,}618{,}461{,}064.
\tag{3.5}
\]

## 4. Nonvanishing by diagonal Krylov spaces

### Lemma 4.1

Under the frozen contracts, not every determinant \(E_{T_0,195}\) is the
zero polynomial.

### Proof

Assume every 392-anchor determinant vanishes identically.  Let \(M\) be the
diagonal operator with the distinct source coordinates as eigenvalues.  For a
pencil parameter \(y\), write

\[
 w_y=(S_a(y))_{a\in\Sigma},
 \qquad q_z=(S_a(z)^p)_{a\in\Sigma}.
\tag{4.1}
\]

Diagonal specialization of the two-parameter wedge produces monomials

\[
 Z^{ip+j},\qquad0\le i,j\le m+1.
\tag{4.2}
\]

They are distinct because \(p>m+1\).  Thus the assumed univariate identities
separate coefficientwise and imply that, for every \(y,z\),

\[
 K_{m+1}(M,w_y)\cap K_{m+1}(M,q_z)\ne\{0\},
\tag{4.3}
\]

where

\[
 K_{m+1}(M,v)=\langle v,Mv,\ldots,M^mv\rangle.
\]

Equation (2.7) implies that each \(w_y\) and \(q_z\) has support at least
\(18{,}418>m\).  A polynomial of degree at most \(m\) cannot annihilate such a
vector under the distinct diagonal eigenvalues, so every Krylov space in
(4.3) has dimension \(m+1\).

Fix \(z\) and distinct \(y_1,y_2\).  Choose nonzero polynomial pairs
\(f_i,g_i\), each of degree at most \(m\), such that

\[
 f_i(M)w_{y_i}=g_i(M)q_z\ne0
 \qquad(i=1,2).
\tag{4.4}
\]

Commutativity of polynomials in the same diagonal \(M\) gives

\[
 g_2(M)f_1(M)w_{y_1}
 =g_1(M)f_2(M)w_{y_2}.
\tag{4.5}
\]

The common vector is nonzero.  Indeed, it equals
\(g_1(M)g_2(M)q_z\); the multiplier has degree at most \(2m=390\), while
\(q_z\) has support at least \(18{,}418\).

Let \(A_1=g_2f_1\) and \(A_2=g_1f_2\).  Before cancelling the full gcd,
observe that \(H(a)\ne0\) for every \(a\in\Sigma\): otherwise
\(P(a)=Q(a)=0\), hence both translated source coordinates vanish at \(a\),
contrary to \(a\in\Sigma\).  Source coupling now turns (4.5) into

\[
 A_1(a)(\bar P+y_1\bar Q)(a)
 =A_2(a)(\bar P+y_2\bar Q)(a)
\tag{4.6}
\]

at every source point.  The difference has degree at most \(e+2m\), and

\[
 s-(e+2m)\ge18{,}418-390=18{,}028>0.
\tag{4.7}
\]

It is therefore the zero polynomial.  Rearranging gives

\[
 (A_1-A_2)\bar P+(y_1A_1-y_2A_2)\bar Q=0.
\tag{4.8}
\]

Neither coefficient in (4.8) is zero: either vanishing would, using
\(y_1\ne y_2\), contradict coefficient rank two and the nonzero common vector.
Since \(\gcd(\bar P,\bar Q)=1\), (4.8) forces

\[
 \deg\bar P,\deg\bar Q\le2m=390.
\tag{4.9}
\]

This contradicts the uniform floor \(e\ge33{,}737\) in (2.8).  Hence a
nonzero determinant exists.  \(\square\)

The proof uses diagonal Krylov commutativity.  It does **not** use a general
Segre/opposite-ruling classification; that shortcut is false for arbitrary
skew block pencils and is retained only as a Sage countercontrol.

## 5. Pair-global owner and exact restart

Order the 392-subsets of \(\Sigma\) lexicographically using the frozen domain
order.  If a qualifying record exists, Lemma 4.1 gives a first subset
\(T_\star\) for which \(E_{T_\star,195}\ne0\).  Define the intrinsic owner

\[
 \mathcal Z_{195}
 =\{\eta\in F:E_{T_\star,195}(\eta)=0\}.
\tag{5.1}
\]

If every 392-anchor source determinant is zero, take the owner to be empty;
otherwise use the first nonzero determinant whether or not a qualifying
selector record happens to exist.  Lemma 4.1 proves that a qualifying record
forces the second branch.  This construction depends only on the fixed
received pair, translation, source, and domain order.  It does not choose a
minor from a selector or record.

Every selected slope in every layer \(1\le r\le195\) lies in
\(\mathcal Z_{195}\), and

\[
 |\mathcal Z_{195}|\le196(p+1).
\tag{5.2}
\]

At the predecessor first-match slot, replace

```text
source_frobenius_moving_linear_cofactor
```

by

```text
source_frobenius_effective_multiplier_degree_at_most_195
```

on the exact incoming residual.  Delete only its intersection with
\(\mathcal Z_{195}\).  Then rebuild the complete selector, carriers, affine
ranks, deficit histograms, and all downstream gates.  The old four-anchor
owner is not retained as an additive charge.

## 6. Algebraic endpoint

The preceding proof works for a general fixed \(m\) whenever

\[
 2m<18{,}418,
 \qquad p>m+1,
 \qquad e>2m.
\tag{6.1}
\]

The last condition is automatic here from \(e\ge33{,}737\).  The sharp active
condition is therefore

\[
 m\le\left\lfloor\frac{18{,}418-1}{2}\right\rfloor=9{,}208.
\tag{6.2}
\]

At \(m=9{,}208\), the support/root margin is still two:

\[
 18{,}418-2m=2.
\tag{6.3}
\]

At \(m=9{,}209\), equality replaces strictness, so both the common-vector and
source-root arguments can fail.  This is a sharp route cut for this proof
mechanism under the current coarse support bound.

The algebraic endpoint owner would have cap

\[
 9{,}209(p+1)=19{,}621{,}675{,}550{,}706.
\tag{6.4}
\]

It is not banked below because the current ledger fails much earlier.

## 7. Exact ledger maximality and the \(r=196\) route cut

The predecessor already charges

\[
 2(p+1)=4{,}261{,}412{,}868
\tag{7.1}
\]

for the four-anchor slot.  Replacing it by (3.5) moves only

\[
 194(p+1)=413{,}357{,}048{,}196.
\tag{7.2}
\]

Thus

\[
 U_{\rm paid}:8{,}997{,}682{,}136
 \longrightarrow422{,}354{,}730{,}332,
\tag{7.3}
\]

\[
 B_{\rm remaining}:274{,}980{,}719{,}113{,}712{,}951
 \longrightarrow274{,}980{,}305{,}756{,}664{,}755.
\tag{7.4}
\]

Exact replay of the inherited \(D=18{,}014\) one-cut compiler gives

\[
 T_{18{,}014}=17{,}413{,}395{,}125{,}116,
\tag{7.5}
\]

\[
 E_{\max}=
 17{,}249{,}952{,}857{,}855{,}762{,}969{,}687{,}793{,}243,
 974{,}375{,}796{,}302{,}274,
\tag{7.6}
\]

with

\[
 K_{\rm remaining}=4{,}807{,}513,
 \qquad J_{\rm break}=21.
\tag{7.7}
\]

The Python optimizer exhausts every integer \(1\le m\le9{,}208\).  The owner
cap and \(U_{\rm paid}\) increase with \(m\), while the remaining budget,
one-cut tail target, and aggregate-excess allowance do not increase.  The
last \(m\) retaining a defined one-cut gate and \(E_{\max}\ge0\) is exactly

\[
 \boxed{m=195.}
\tag{7.8}
\]

At \(r=196\), the prospective owner data would be

\[
 \operatorname{cap}=197(p+1)=419{,}749{,}167{,}498,
\]

\[
 U_{\rm paid}=424{,}485{,}436{,}766,
 \qquad
 B_{\rm remaining}=274{,}980{,}303{,}625{,}958{,}321,
\tag{7.9}
\]

and the one-cut threshold still exists:

\[
 T_{18{,}014}=17{,}410{,}886{,}628{,}770.
\tag{7.10}
\]

But its inherited aggregate-excess allowance is

\[
 E_{\max}=
 -9{,}487{,}087{,}327{,}483{,}531{,}737{,}221{,}376{,}676,
 045{,}581{,}877{,}928{,}676<0.
\tag{7.11}
\]

Since aggregate excess is nonnegative by definition, (7.11) supplies no
paying threshold and no meaningful maximal-gcd break index.  Monotonicity
then excludes every \(196\le m\le7{,}136\) from the inherited gate; at
\(m=7{,}137\), even the one-cut helper ceases to have a useful threshold.
The algebraic theorem remains valid, but current incidence/accounting
hypotheses cannot use its larger charge.

This is the exact missing lemma:

> Prove a stronger rank-nine support-incidence or deficit-distribution bound
> that replaces the exhausted uniform-cap/aggregate-excess allowance.

Until such a lemma exists, \(r=196\) is the first unpaid layer and no larger
effective-multiplier owner is banked.

## 8. Revised residual and scope

After exact deletion and restart, every surviving qualifying full-outside
record has

\[
 r\ge196,
 \qquad s\ge t+197=67{,}669,
\tag{8.1}
\]

\[
 e\ge\left\lceil\frac{67{,}669}{2}\right\rceil=33{,}835,
 \qquad
 \deg H\le k-1-e\le1{,}014{,}740.
\tag{8.2}
\]

This packet does not:

- add the 392-anchor cap to the old four-anchor cap;
- union roots over minors, records, profiles, selectors, or translations;
- treat the necessary determinant condition as sufficient;
- claim that the degree-two Sage fixture constructs a degree-195 record;
- bank the algebraic \(m=9{,}208\) endpoint;
- interpret the negative value (7.11) as a usable threshold;
- pay non-full-outside source load;
- determine \(U_Q\), residual \(U_A\), the complete profile envelope, or the
  lower reserve;
- close rank nine or KoalaBear;
- authorize rank at least ten, Lean, or stable-paper promotion.

The global verdict remains **YELLOW**.

## 9. Exact controls and next action

The Python verifier:

1. replays the predecessor payload and source bindings;
2. exhausts all \(1{,}274{,}195\) slack triples through \(r=195\) without
   serializing them into the certificate;
3. checks all \(38{,}809\) diagonal exponents \(ip+j\);
4. exhausts the exact ledger optimizer on \(1\le m\le9{,}208\);
5. binds the \(m=195\), \(m=196\), \(m=7{,}136/7{,}137\), and
   \(m=9{,}208/9{,}209\) endpoints;
6. validates source hashes, canonical JSON, optimized-mode parity, and
   mutations.

The Sage control retains an exact \(\mathbf F_{13^2}/\mathbf F_{13}\)
degree-two specialization.  It verifies the Frobenius fingerprint, selected
roots, full three-step diagonal Krylov ranks, cross-multiplier commutativity,
root-count sharpness, and the false skew-block ruling shortcut.  Its deployed
integer assertions check the degree-195 and endpoint arithmetic.  It is not a
selector census or a substitute for the symbolic proof.

The maximal next mathematical action is not another effective-degree layer.
It is the rank-nine incidence/accounting lemma isolated by (7.11).  If no such
bound follows from the current selector hypotheses, (7.11) should remain the
banked route cut.
