---
workboard_item: M1
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: For one received word, one c=2048 occupancy profile, and one fixed partial agreement template, the complete exact-boundary family is an interleaved quotient-RS packing. If v>=512 it has at most one codeword; if v<=511 its size is at most floor(binomial(1023-u-v,512-v)/binomial(544-v,512-v)). Exact locator w-jets and normalized cofactor w-jets are in fiber-preserving bijection. One deployed fixed template realizes at least 15 distinct such targets, and two same-profile codewords can have different partial templates.
architecture: M31_C2048_FIXED_TEMPLATE_INTERLEAVED_QUOTIENT_ROUTE_CUT_V1
partition_digest: CERTIFICATE_BOUND; no ledger atom assigned
atom_or_cell: HIGH_BOUNDARY_EXACT_CODEWORD / U_new
quantifier: Every target-field received word at the deployed exact boundary for the upper theorem; the two route-cut constructions are symbolic base-field constructions and hence also target-field constructions.
projection_and_unit: Distinct exact-boundary codewords, fixed partial agreement templates, full-fiber quotient supports, and depth-w normalized cofactor reciprocal jets.
claimed_bound: The fixed-template cap above, 25767 budget-fitting occupancy profiles under that cap, a 15-target fixed-template source, and a two-template same-profile source. The legal global expression remains a sum over profiles, templates, and attained cofactor jets.
status: PROVED LOCAL THEOREMS / GLOBAL OWNER OPEN
impact: FIXED_TEMPLATE_INTERLEAVED_BOUND / ATTAINED-TARGET ROUTE CUT
falsifier: A fixed-template family violating the packing cap; failure of the reciprocal congruence or jet bijection; coincident targets in the 15-target construction; extra agreements in either construction; or a chronology-valid reduction of the global sum that this packet wrongly excludes.
replay: Python exact profile census, arithmetic, canonical certificate, and semantic mutations; independent Sage polynomial and finite-field fixtures.
---

# M31 `c=2048` fixed-template interleaved quotient route cut

## Status

```text
PROVED fixed-template interleaved quotient-RS cap
PROVED locator-jet / normalized-cofactor-jet equivalence
PROVED at least 15 attained targets in one fixed template
PROVED same profile does not force one partial template
UNPROVEN complete profile/template/target sum
ledger movement = 0
M31 LIST row closed = false
```

This packet performs the source-bound reduction requested by the 65-column
route cut.  It uses the whole exact-boundary family attached to a fixed
partial template, rather than selecting another small carrier.  The result is
an exact interleaved Reed--Solomon packing theorem and an exact description of
the target that has to be summed.

The theorem does not pay the row.  Most fixed-template caps are still above
the LIST budget, different templates occur around one received word, and even
one fixed template can attain many distinct cofactor targets.  The correct
successor is therefore a theorem for the complete attained-image sum, not a
maximum-prefix-fiber estimate.

## 1. Deployed constants and support coordinates

Put

\[
 p=2^{31}-1,
 \quad n=2^{21}=2097152,
 \quad K=2^{20}=1048576,
\]
\[
 A=1116023,
 \quad R=n-A=981129,
 \quad w=A-K=67447,
 \quad c=2048,
 \quad N=n/c=1024,
\]
\[
 B_*=\left\lfloor\frac{p^4}{2^{100}}\right\rfloor=16777215.
\tag{1.1}
\]

Let \(\phi\in\mathbb F_p[X]\) be the deployed monic Chebyshev fold.  Its
restriction to the evaluation domain has \(N\) complete fibers of size
\(c\), with quotient-label set \(Q\).

For an occupancy profile \((u,v)\), set

\[
 h=u+v+1,
 \qquad r=1911+2048v,
 \qquad f=544-v,
 \qquad M=1023-u-v.
\tag{1.2}
\]

Thus \(h\) is the number of partial fibers, \(r\) is the number of
agreement points in them, \(f\) is the number of full agreement fibers, and
\(M=N-h\) quotient labels remain available after the partial labels are
removed.  In particular

\[
 r+cf=A.
\tag{1.3}
\]

Fix the partial-fiber labels \(H_0\subset Q\), \(|H_0|=h\), and fix an
actual partial agreement template

\[
 P_0\subset\phi^{-1}(H_0),
 \qquad |P_0|=r,
\]

meeting every fiber over \(H_0\) nontrivially but not completely.  Write
\(L_0=L_{P_0}\).  Every support in this fixed-template class has the form

\[
 S_E=P_0\sqcup\phi^{-1}(E),
 \qquad E\in\binom{Q\setminus H_0}{f}.
\tag{1.4}
\]

## 2. Fixed-template interleaved quotient theorem

### Theorem 2.1

Let \(Y\in\mathbb F_{p^4}[X]_{<n}\) be one received polynomial.  Let
\(\mathcal L(Y;P_0)\) be the set of distinct degree-less-than-\(K\)
codeword polynomials whose exact agreement support with \(Y\) has the form
(1.4).

If \(v\ge512\), then

\[
 |\mathcal L(Y;P_0)|\le1.
\tag{2.1}
\]

If \(v\le511\), put

\[
 \kappa=512-v.
\tag{2.2}
\]

Then

\[
 \boxed{
 |\mathcal L(Y;P_0)|
 \le
 \left\lfloor
 \frac{\binom{M}{\kappa}}{\binom{f}{\kappa}}
 \right\rfloor .}
\tag{2.3}
\]

The theorem is field-generic: the same proof works over every coefficient
field containing the base field.

### Proof

If \(v\ge512\), then \(r\ge K\).  Two codewords in the family both agree
with \(Y\) on \(P_0\), so their difference has at least \(K\) distinct
roots and degree less than \(K\).  It is zero.  This proves (2.1).

Now suppose \(v\le511\), so \(r<K\).  Let \(C_0\) be the remainder of
\(Y\) on division by \(L_0\).  Every family member \(C_i\) is congruent to
\(Y\), hence to \(C_0\), modulo \(L_0\).  Define

\[
 q_i=\frac{C_i-C_0}{L_0},
 \qquad
 \widetilde Y=\frac{Y-C_0}{L_0}.
\tag{2.4}
\]

The exact agreement on the full fibers over \(E_i\) gives

\[
 \widetilde Y-q_i=V_{E_i}(\phi)H_i,
 \qquad
 V_{E_i}(T)=\prod_{b\in E_i}(T-b).
\tag{2.5}
\]

Indeed, for each \(b\in E_i\), the monic degree-\(2048\) polynomial
\(\phi(X)-b\) has precisely the 2,048 distinct points of the complete fiber
as its roots.  It therefore divides \(\widetilde Y-q_i\); the factors for
distinct labels are coprime, so their product \(V_{E_i}(\phi)\) divides it.

Because \(\phi\) is monic of degree \(c\),
\(1,X,\ldots,X^{c-1}\) is a basis of \(\mathbb F_{p^4}[X]\) over
\(\mathbb F_{p^4}[\phi]\).  Hence uniquely

\[
 q_i(X)=\sum_{a=0}^{2047}X^a q_{i,a}(\phi(X)).
\tag{2.6}
\]

The degree headroom is

\[
 K-r=2048(511-v)+137.
\tag{2.7}
\]

The triangular leading degrees \(a+2048j\) in (2.6) therefore give

\[
 \deg q_{i,a}\le511-v\quad(0\le a\le136),
\tag{2.8}
\]
\[
 \deg q_{i,a}\le510-v\quad(137\le a\le2047).
\tag{2.9}
\]

At \(v=511\), the last 1,911 components are zero.  Decomposing (2.5) in
the same free basis shows that \(V_{E_i}\) divides every scalar component
of \(\widetilde Y-q_i\).  Thus on every common label
\(b\in E_i\cap E_j\), all components of \(q_i-q_j\) vanish.

If \(C_i\ne C_j\), then \(q_i\ne q_j\), so at least one scalar component
is a nonzero polynomial of degree at most \(511-v\).  Consequently

\[
 |E_i\cap E_j|\le511-v=\kappa-1.
\tag{2.10}
\]

Every \(E_i\) contains \(\binom f\kappa\) subsets of size \(\kappa\),
and (2.10) says no such subset can belong to two different \(E_i\).  All
of them lie in the \(M\)-element set \(Q\setminus H_0\), which contains
\(\binom M\kappa\) such subsets.  Double counting proves (2.3).
\(\square\)

### Exact deployed census

Scanning all 261,192 feasible profiles gives:

```text
fixed-template cap <= B*:                 25,767 profiles
  v>=512 uniqueness profiles:             15,807
  additional budget-fitting profiles:      9,960
fixed-template cap > B*:                 235,425 profiles
fixed-template cap <= 1:                  16,422 profiles
fixed-template cap <= 15:                 17,763 profiles
fixed-template cap <= 36:                 18,105 profiles
fixed-template cap <= 65:                 18,388 profiles
```

The largest budget-fitting cap is \(16,769,604\), attained at profiles
\((472,161)\) and \((128,505)\).  The smallest cap above budget is
\(16,808,455\), attained at \((224,504)\) and \((471,257)\).  The face
\((0,0)\) has the
255-digit cap

\[
\begin{split}
&431740767214703188879316377498800092884434688802708891775670954559170283736794298076501087440929776468830378661824689539133900550726656117368329822580973095992598875401404711523153496477591190494411907262059922361682951457977842456177675714658631053353130.
\end{split}
\tag{2.11}
\]

Thus Theorem 2.1 fits the full-row budget individually for every fixed
template in 25,767 profile shapes.  It is not a first-match payment or a
uniform budget-fitting theorem, and it does not by itself control how many
partial templates occur around one word.

## 3. Exact cofactor-jet bridge

For a polynomial \(F\) of degree \(d\), write

\[
 F^\vee(Z)=Z^dF(Z^{-1}).
\]

Coefficients beyond the actual degree are zero-padded whenever jets are
compared.

### Theorem 3.1

Assume one received polynomial \(Y\) has a nonempty exact-boundary family.
Then \(\deg Y\ge A\).  Write

\[
 \deg Y=A+s,
 \qquad \gamma=\operatorname{lc}(Y).
\tag{3.1}
\]

For every exact-boundary codeword \(C\), write uniquely

\[
 Y-C=L_SH,
 \qquad \overline H=\gamma^{-1}H.
\tag{3.2}
\]

Then \(\overline H\) is monic of degree \(s\), and

\[
 L_S^\vee\overline H^\vee
 \equiv
 \gamma^{-1}Y^\vee
 \pmod{Z^{w+s+1}}.
\tag{3.3}
\]

In particular, modulo \(Z^{w+1}\), inversion followed by multiplication by
the fixed unit \(\gamma^{-1}Y^\vee\) gives a bijection between the attained
depth-\(w\) locator reciprocal jets and the attained depth-\(w\)
normalized-cofactor reciprocal jets.  Every fiber cardinality is preserved.

### Proof

The polynomial \(Y-C\) is nonzero and divisible by the degree-\(A\)
locator, so \(\deg Y\ge A\).  Since \(\deg C<K\le A\), its leading term
cannot cancel that of \(Y\).  Thus \(H\) has degree \(s\), leading
coefficient \(\gamma\), and \(\overline H\) is monic.

Taking reciprocals in (3.2), with the common ambient degree \(A+s\), gives

\[
 L_S^\vee\overline H^\vee
 =\gamma^{-1}Y^\vee
  -\gamma^{-1}Z^{A+s-\deg C}C^\vee.
\]

Because \(\deg C\le K-1\), the final term is divisible by

\[
 Z^{A+s-K+1}=Z^{w+s+1},
\]

which proves (3.3).  All three displayed reciprocal polynomials have
constant coefficient one after normalization.  They are therefore units in
the truncated power-series ring.  A locator jet determines the cofactor jet
by division, and conversely, proving the bijection and fiber preservation.
\(\square\)

### Corollary 3.2 (fixed-template quotient coordinates)

For fixed \(P_0\),

\[
 L_{S_E}^\vee=L_0^\vee\bigl(V_E(\phi)\bigr)^\vee.
\tag{3.4}
\]

Cancel the fixed unit \(L_0^\vee\) modulo \(Z^{w+1}\).  The triangular
reciprocal identity for a monic degree-2048 fold then shows that equality of
two locator depth-\(w\) jets is equivalent to equality of the first

\[
 \min(\lfloor w/2048\rfloor,f)=\min(32,f)
\tag{3.5}
\]

coefficients of \(V_E\).  The same equivalence holds for normalized
cofactor jets by Theorem 3.1.

This uses fixed-unit cancellation followed by the QR5 triangular argument.
It does not invoke the full QR2 theorem for a general \(P_0\), because
\(r=1911+2048v\) can be at least \(2048\).  QR2 applies directly in the
special profile \((0,0)\), where \(r=1911<2048\).

## 4. A fixed template with at least 15 attained targets

The previous section identifies the correct target.  The next construction
shows that even one fixed template need not coalesce to one, four, or any
other bound below 15 targets.

Fix \(\beta_0\in Q\) and a set

\[
 P_0\subset\phi^{-1}(\beta_0),
 \qquad |P_0|=1911.
\tag{4.1}
\]

Partition \(Q\setminus\{\beta_0\}\) into \(J\sqcup U\), with
\(|J|=511\) and \(|U|=512\).  There exist 15 pairwise disjoint sets
\(B_i\subset U\), each of size 33, whose field sums are pairwise distinct.
Indeed, after \(i<15\) blocks have been removed, at least
\(512-33i\ge50\) points remain.  Fix 32 of them and vary the last point.
This produces at least 18 distinct sums at the final step, more than the 14
previously forbidden sums.  The same inequality is stronger at earlier
steps.  The blocks use 495 labels and leave 17 unused.

Choose distinct nonzero scalars \(a_1,\ldots,a_{15}\in\mathbb F_p\).
There is a unique polynomial \(G(T)\) of degree at most 512 on the 513
labels \(Q\setminus J\), prescribed by

\[
 G|_{B_i}=a_i,
 \qquad
 G(\beta_0)=0,
 \qquad
 G=0\text{ on the 17 unused labels}.
\tag{4.2}
\]

Put

\[
 V_J(T)=\prod_{b\in J}(T-b),
 \qquad W(T)=V_J(T)G(T),
 \qquad q_i(T)=a_iV_J(T),
\tag{4.3}
\]
\[
 Y=L_0W(\phi),
 \qquad C_i=L_0q_i(\phi),
 \qquad E_i=J\sqcup B_i.
\tag{4.4}
\]

Then

\[
 \deg C_i=1911+2048\cdot511=1048439=K-137,
\tag{4.5}
\]
\[
 \deg Y\le1911+2048\cdot1023=2097015=n-137.
\tag{4.6}
\]

Moreover \(W-q_i\) vanishes on exactly the quotient labels \(E_i\): it
vanishes on \(J\), equals zero on \(B_i\), is nonzero on every other block
because the \(a_i\) are distinct, and is nonzero at \(\beta_0\) and the
unused labels because \(a_i\ne0\).  Hence \(C_i\) has exact agreement set

\[
 S_i=P_0\sqcup\phi^{-1}(E_i),
 \qquad |S_i|=1911+544\cdot2048=A.
\tag{4.7}
\]

Factoring \(W-q_i=V_{E_i}h_i\) gives

\[
 \deg h_i\le479,
 \qquad \deg h_i(\phi)\le980992=R-137.
\tag{4.8}
\]

The first nonleading coefficient of \(V_{E_i}\) is
\(-\sum_{b\in J}b-\sum_{b\in B_i}b\), so the 15 quotient targets are
pairwise distinct.  QR2 applies here because \(|P_0|=1911<2048\) and
\(w\ge1911\); Theorem 3.1 then makes the 15 locator and normalized-cofactor
targets pairwise distinct as well.

This proves at least 15 attained targets among the displayed codewords.  It
does not claim that these are all targets or all codewords in the ball.

## 5. Same profile does not imply one partial template

The fixed-template theorem cannot be applied globally by assuming that all
members of one profile share \(P_0\).

Choose distinct quotient labels \(\beta_1,\beta_2\).  Partition the other
1,022 labels as

\[
 J\sqcup A_1\sqcup A_2,
 \qquad |J|=66,
 \qquad |A_1|=|A_2|=478.
\tag{5.1}
\]

Choose

\[
 P_i\subset\phi^{-1}(\beta_i),
 \qquad |P_i|=1911,
\]

and put

\[
 E_i=J\sqcup A_i,
 \qquad S_i=P_i\sqcup\phi^{-1}(E_i).
\tag{5.2}
\]

Both supports have profile \((0,0)\), but their partial templates differ.
Their intersection is

\[
 I=S_1\cap S_2=\phi^{-1}(J),
 \qquad |I|=66\cdot2048=135168<K.
\tag{5.3}
\]

Let \(g=L_I\), a degree-less-than-\(K\) codeword polynomial.  Define a
received word by \(Y=0\) on \(S_1\), \(Y=g\) on \(S_2\), and on every
point outside \(S_1\cup S_2\) choose a value different from both \(0\) and
\(g\).  The definitions agree on \(I\), where \(g=0\).  Since the target
field has more than two elements, the outside choice is possible.

The codewords \(0\) and \(g\) then have exact agreement sets \(S_1\) and
\(S_2\), respectively.  This is a two-codeword construction, not a budget
violation, but it proves that same-profile pigeonhole does not supply a
common partial template.

## 6. The legal global decomposition and remaining owner

For one received word, complete-support factorization assigns every exact
boundary codeword uniquely to:

1. one occupancy profile \((u,v)\);
2. one exact partial agreement template \(P_0\); and
3. one attained normalized cofactor depth-\(w\) jet \(\eta\).

Therefore the exact boundary mass is the disjoint sum

\[
 M_\partial(Y)=
 \sum_{(u,v)}
 \sum_{P_0}
 \sum_{\eta\in\operatorname{AttCofJet}(Y;u,v,P_0)}
 N_Y(u,v,P_0,\eta).
\tag{6.1}
\]

For each fixed \((u,v,P_0)\), Theorem 2.1 bounds the sum over \(\eta\).
It does not bound the number of simultaneously attained templates, and the
15-target construction rules out any universal target-count replacement
below 15 for the innermost sum.  The two-template construction rules out
deleting the middle sum.

The new exact terminal inside
`HIGH_BOUNDARY_EXACT_CODEWORD` / \(U_{\rm new}\) is

```text
UNPAID_ATTAINED_COFACTOR_JET_SUM_OWNER
```

A closing successor must do at least one of the following, in the declared
v4 chronology:

* bound (6.1), together with \(U_{\rm paid}\), by \(B_*\);
* route a disjoint part of (6.1) into the existing row-sharp quotient atom
  with an exact codeword payment;
* classify the varying-template residual into a chronology-valid paid owner;
* or prove a new explicit primitive route cut for the surviving attained
  cofactor-jet incidence.

A maximum-prefix-fiber bound alone, a standalone fixed-width carrier, or a
source-specific canonical center cannot replace (6.1).

## 7. Scope, dependence, and nonclaims

This packet proves no numerical movement of \(U_Q\), \(U_{\rm list,int}\),
\(U_{\rm ext}\), or \(U_{\rm new}\).  It does not pay the combined
9,216,781 boundary allowance, high interior, or the complete M31 row.  The
15-target construction does not assert that its complete ball is
boundary-only.  The fixed-template cap is an upper theorem, while both
displayed constructions are exact lower witnesses; neither is promoted from
toy-scale evidence.

There is no layer-cake, dyadic summability, moment, Markov, or probabilistic
Chebyshev argument.  `Chebyshev` refers only to the deployed polynomial fold.

The load-bearing sources are the exact quotient--remainder reciprocal normal
form, the deployed Chebyshev complete-fiber theorem, the exhaustive occupancy
atlas and arbitrary-word source adapter, the multiprefix fixed-template
source, and the immediate 65-column predecessor.  The certificate seals
those sources and independently replays the arithmetic and finite-field
fixtures.
