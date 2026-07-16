# M1 KoalaBear branch-3 TDD excess and defect-span route cut v1

**Status:** PROVED LOCAL SHORTENING / PROVED COMPLETE-SELECTOR
DEFECT-SPAN BRIDGE / PROVED RANK-\(\le 3\) GLOBAL TERMINAL /
COUNTERCONTROL / FAIL-CLOSED ROUTE CUT / NO LEDGER MOVEMENT.

This packet attacks only the terminal
`UNPAID_HIGH_UNION_TRIPLE_DISTANCE_DEFECT` left by the branch-3
deep-owner packet at

\[
(n,k,A)=(2{,}097{,}152,1{,}048{,}576,1{,}116{,}048).
\]

It proves an exact shortening description for every nonzero
triple-distance defect (TDD), identifies the precise bridge from all TDD
residuals to the minimum affine rank over complete actual-witness
selectors, and records the largest intrinsic-rank terminal that fits the
remaining KoalaBear budget.  It also gives an exact \(e=1\) control showing
that low triple excess alone does not force the displayed local TDD supports
themselves to have pairwise common-GCD or cyclic-shift symmetry.

The result is a route cut, not a closure.  No TDD charge is banked and
branch 3 remains open.

## 1. Deployed row and predecessor state

Put

\[
R=n-k=1{,}048{,}576,\qquad
j=n-A=981{,}104,\qquad
t=A-k=67{,}472,
\]

and let

\[
d=R+1=1{,}048{,}577,\qquad
r_*=\left\lfloor\frac R3\right\rfloor=349{,}525,\qquad
L=r_*+1=349{,}526.
\]

The predecessor packet has already:

1. paid the intrinsic deep owner through error weight \(r_*\);
2. applied the one-global-carrier owner through carrier excess ten;
3. reduced a surviving family of more than fifteen slopes to a nonzero
   TDD supported on the union of three selected actual error supports.

Its exact ledger state is

\[
U_{\rm paid}=2{,}602{,}502{,}999,\qquad
B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\]

This packet starts from that state and leaves it unchanged.

## 2. TDD convention

Let \(F\) be a field, let \(D\subset F\) have \(n\) distinct points, and
let \(C=\operatorname{RS}_F(D,k)\).  Fix a received pair \(f,g:D\to F\).
For three distinct finite slopes \(\alpha,\beta,\gamma\), choose codewords
\(c_\alpha,c_\beta,c_\gamma\in C\), and put

\[
e_\eta=f+\eta g-c_\eta,\qquad
E_\eta=\operatorname{supp}(e_\eta).
\]

The triple-distance defect is

\[
\Delta_{\alpha\beta\gamma}
 =
(\beta-\gamma)c_\alpha
+(\gamma-\alpha)c_\beta
+(\alpha-\beta)c_\gamma.
\tag{2.1}
\]

The same affine combination of the received words vanishes, so

\[
\Delta_{\alpha\beta\gamma}
 =
-\bigl((\beta-\gamma)e_\alpha
+(\gamma-\alpha)e_\beta
+(\alpha-\beta)e_\gamma\bigr).
\tag{2.2}
\]

Consequently

\[
\operatorname{supp}\Delta_{\alpha\beta\gamma}
\subseteq
U:=E_\alpha\cup E_\beta\cup E_\gamma.
\tag{2.3}
\]

The TDD branch means \(\Delta_{\alpha\beta\gamma}\ne0\).  The RS minimum
distance then gives \(|U|\ge d=R+1\).  Define the **triple excess**

\[
e=|U|-(R+1),\qquad 0\le e\le k-1.
\tag{2.4}
\]

This is not the carrier excess.  The carrier excess of this same union is

\[
\kappa(U)=|U|-R=e+1.
\tag{2.5}
\]

In particular, the already-paid excess-ten carrier theorem can pay an
\(e\le9\) TDD only when this same \(U\) contains every support in the
complete retained selector.  A local triple union is not a global
carrier certificate.

## 3. Exact shortening and silent shell

For \(U\subseteq D\), define the complementary locator

\[
M_U(X)=\prod_{x\in D\setminus U}(X-x).
\tag{3.1}
\]

If \(|U|=R+1+e\), then

\[
\deg M_U=n-|U|=k-1-e.
\tag{3.2}
\]

Regard the nonzero TDD as its unique polynomial representative of degree
less than \(k\).  It vanishes on \(D\setminus U\), so

\[
\boxed{\quad
\Delta_{\alpha\beta\gamma}=M_UQ,\qquad \deg Q\le e.
\quad}
\tag{3.3}
\]

Conversely every \(M_UQ\) with \(\deg Q\le e\) is a codeword supported in
\(U\).  Therefore the shortened defect space

\[
\{c\in C:\operatorname{supp}c\subseteq U\}
\]

has dimension exactly \(e+1\).

Since \(M_U(x)\ne0\) for every \(x\in U\), the **silent shell**

\[
Z_{\rm sil}
=U\setminus\operatorname{supp}\Delta_{\alpha\beta\gamma}
\]

satisfies

\[
Z_{\rm sil}=U\cap Z(Q),\qquad |Z_{\rm sil}|\le e.
\tag{3.4}
\]

Thus \(e=0\) gives one projective defect direction for fixed \(U\) and no
silent points.  For general \(e\), the number of projective defect
directions over a field of size \(q\) is

\[
\frac{q^{e+1}-1}{q-1}.
\tag{3.5}
\]

Equation (3.5) is a diagnostic multiplicity, not a ledger payment.

## 4. Exact overlap consequences

Write

\[
a_\eta=|E_\eta|,\qquad
P=\sum_{\eta<\theta}|E_\eta\cap E_\theta|,\qquad
T=|E_\alpha\cap E_\beta\cap E_\gamma|.
\]

Coordinatewise membership counting gives

\[
\boxed{\quad
P-T=a_\alpha+a_\beta+a_\gamma-|U|.
\quad}
\tag{4.1}
\]

Hence

\[
\max_{\eta<\theta}|E_\eta\cap E_\theta|
\ge
\left\lceil
\frac{(a_\alpha+a_\beta+a_\gamma-R-1-e)_+}{3}
\right\rceil.
\tag{4.2}
\]

Every point of the silent shell lies in at least two of the three error
supports.  Indeed, at a point belonging to exactly one support, (2.2)
is a nonzero scalar multiple of the unique nonzero error value.

After the intrinsic deep-owner deletion every selected error has weight
at least \(L\).  Since \(3L=R+2\), (4.1) only forces:

\[
e=0\Longrightarrow P-T\ge1,\qquad
e\ge1\Longrightarrow P-T\ge0.
\tag{4.3}
\]

Even at \(e=0\), (4.3) gives only one pair-specific common point; it does
not give a common factor shared by the complete retained family.

## 5. Intrinsic selector rank and the defect-span bridge

Let \(\operatorname{Sel}(\Gamma)\) be the set of all complete selectors
choosing one actual noncontained witness for every slope in the retained set
\(\Gamma\).  For \(\sigma\in\operatorname{Sel}(\Gamma)\), let

\[
s(\sigma)
=
\dim\operatorname{span}_{F}\bigl\{
e^\sigma_\eta-e^\sigma_{\eta_0}:\eta\in\Gamma
\bigr\}
\]

which is independent of the anchor \(\eta_0\).  Define the intrinsic
selected-witness rank

\[
s_*(\Gamma)=\min_{\sigma\in\operatorname{Sel}(\Gamma)}s(\sigma).
\tag{5.1}
\]

Separately define the intrinsic global carrier excess

\[
\kappa_*(\Gamma)
=
\min_{\sigma\in\operatorname{Sel}(\Gamma)}
\max\left\{
0,
\left|\bigcup_{\eta\in\Gamma}E^\sigma_\eta\right|-R
\right\}.
\]

The carrier owner is applied existentially over complete selectors:
if \(\kappa_*(\Gamma)\le10\), choose a selector attaining that minimum and
pay the complete slope set.  On the complementary route
\(\kappa_*(\Gamma)\ge11\), every complete selector has union excess at least
eleven, including any selector attaining \(s_*(\Gamma)\).  The carrier-minimizing
and rank-minimizing selectors need not be the same.

This existential reapplication is necessary.  The predecessor TDD was
derived after fixing one selected family; high union for that family alone
does not imply high union for a newly chosen rank-minimizing selector.

The deployed field and code are finite and every retained slope has at least
one valid witness, so both minima are attained.  Fix one rank-minimizing
selector \(\sigma_*\) before choosing anchors or computing any residual rank.

The predecessor high-union CCL/TDD theorem is uniform over every complete
selector.  Therefore, on the route

\[
|\Gamma|>15,\qquad \kappa_*(\Gamma)\ge11,
\]

it is reapplied to \(\sigma_*\): that selector itself has high union and
contains a nonzero TDD.  No TDD is inherited from a different earlier
selection.

Suppress \(\sigma_*\) from the notation.  Let \(H\) be an RS parity check and
write

\[
He_\eta=y_0+\eta y_1,\qquad y_1\ne0.
\]

Here \(y_1\ne0\) follows from any retained transverse witness: if \(y_1=0\),
then \(He_\eta=y_0\in H(F^{E_\eta})\), so both \(y_0\) and \(y_1\) lie in
that support image, contradicting transversality.

Choose two anchors \(\alpha\ne\beta\).  There are unique codewords
\(p,q\in C\) satisfying

\[
p+\alpha q=c_\alpha,\qquad p+\beta q=c_\beta.
\]

Put

\[
a=f-p,\qquad b=g-q,\qquad
r_\eta=c_\eta-(p+\eta q).
\tag{5.2}
\]

Then

\[
r_\alpha=r_\beta=0,\qquad
e_\eta=a+\eta b-r_\eta,
\tag{5.3}
\]

and (2.1) becomes

\[
\Delta_{\alpha\beta\eta}=(\alpha-\beta)r_\eta.
\tag{5.4}
\]

Let

\[
\mathcal D
=\operatorname{span}\{e_\eta-e_\alpha:\eta\in\Gamma\},
\qquad
s=\dim\mathcal D,
\]

and

\[
\mathcal R=\operatorname{span}\{r_\eta:\eta\in\Gamma\}.
\]

Since

\[
e_\beta-e_\alpha=(\beta-\alpha)b,
\]

we have \(b\in\mathcal D\).  Equation (5.3) gives

\[
r_\eta=(\eta-\alpha)b-(e_\eta-e_\alpha)\in\mathcal D.
\]

Moreover \(Hb=y_1\ne0\), whereas every \(r_\eta\) is a codeword.  Therefore
the sum is direct:

\[
\boxed{\quad
\mathcal D=\langle b\rangle\oplus\mathcal R,\qquad
s_*(\Gamma)=s(\sigma_*)=1+\dim\mathcal R.
\quad}
\tag{5.5}
\]

This is a minimizing-complete-selector identity.  Computing affine rank on
only three TDD anchors does not certify the retained family.  An arbitrary
complete selector does not certify the exact value of \(s_*\); however, if
that selector has rank at most three, it already proves \(s_*\le3\) and gives
the payment below.

### Basis-carrier compression

Choose actual residuals

\[
r_{\gamma_2},\ldots,r_{\gamma_s}
\]

forming a basis of \(\mathcal R\), and define

\[
V=
E_\alpha\cup E_\beta\cup
\bigcup_{h=2}^{s}E_{\gamma_h}.
\tag{5.6}
\]

Solving (5.3) at the two anchors shows that \(a\) and \(b\) are supported
on \(E_\alpha\cup E_\beta\).  Each basis residual is supported in \(V\);
every other residual is their linear combination; and then every
\(e_\eta=a+\eta b-r_\eta\) is supported in \(V\).  Hence

\[
\boxed{\quad
V=\bigcup_{\eta\in\Gamma}E_\eta.
\quad}
\tag{5.7}
\]

Thus the chosen minimizing selector has a basis carrier consisting of
\(s_*+1\) actual supports.  The basis and the minimizing selector need not be
unique, so this carrier is not called canonical.  At the first unpaid
intrinsic affine layer \(s_*=4\), five slopes and three independent residual
codewords recover the complete union of that minimizing selector.

## 6. Rank-\(\le3\) global terminal

The KoalaBear MCA numerator counts distinct finite bad slopes.  Therefore one
actual transverse witness for every retained slope is the complete object
needed here; the rank need not include every explaining codeword at a fixed
slope.  Selector dependence is handled existentially for payment and by a
minimizing selector for the residual structure.  The rank must still cover
the entire retained slope set rather than only the three anchors of one TDD.

The selected-witness affine-core set-pair theorem applies to the complete
selector, because the predecessor supplies actual errors of weight at
most \(j\), minimum kernel distance \(d>j\), and the declared
transversality condition.  It gives

\[
|\Gamma|
\le
\binom{s+\max_\eta|E_\eta|}{s}
\le
\binom{s+j}{s}.
\tag{6.1}
\]

For the KoalaBear row,

\[
\binom{j+3}{3}
=157{,}397{,}034{,}144{,}292{,}985
<
B_{\rm rem},
\tag{6.2}
\]

Every post-deep selected error has weight at least \(L\).  Thus the smallest
rank-four cap available from this theorem is already

\[
\binom{L+4}{4}
=621{,}897{,}958{,}437{,}476{,}295{,}030
>
B_{\rm rem}.
\tag{6.3}
\]

At the maximal permitted weight, the still larger diagnostic value is

\[
\binom{j+4}{4}
=38{,}605{,}872{,}343{,}809{,}750{,}481{,}845.
\tag{6.4}
\]

Therefore the existence of any valid complete selector of rank at most three
is a single budget-fitting global terminal; equivalently
\(s_*(\Gamma)\le3\).  The same set-pair cap cannot pay rank four anywhere in
the post-deep weight range.  The rank-three charge must not be applied once
per triple or repeatedly on an unproved cover.

Combining (5.5) with (6.2), this terminal is exactly

```text
MINIMUM_COMPLETE_SELECTOR_TDD_DEFECT_SPAN_RANK <= 2
    -> PAID_SELECTED_AFFINE_CORE_RANK_LE_3.
```

Its complement is

```text
INTRINSIC_ACTUAL_AFFINE_RANK s_* >= 4
AND EVERY_MINIMIZING_SELECTOR_HAS_TDD_DEFECT_SPAN_RANK >= 3.
```

## 7. Exact \(e=1\) countercontrol

Low triple excess does not by itself force the displayed three TDD supports
to have common-GCD or cyclic-shift structure.  The deployed arithmetic has
the exact identity

\[
R+2=3L.
\tag{7.1}
\]

Choose \(U\subset D\) of size \(R+2\), partition it into three disjoint
\(L\)-sets

\[
U=E_0\sqcup E_1\sqcup E_a,
\]

and choose \(a\notin\{0,1\}\).  Put

\[
\Delta=M_U,\qquad c_0=c_1=0,\qquad c_a=-\Delta.
\]

Define \(f,g\) coordinatewise by

\[
\begin{array}{c|ccc}
 &E_0&E_1&E_a\cup(D\setminus U)\\ \hline
f&-\Delta/(1-a)&0&0\\
g& \Delta/(1-a)&-\Delta/a&0.
\end{array}
\tag{7.2}
\]

Then the errors at slopes \(0,1,a\) have supports exactly
\(E_0,E_1,E_a\), respectively, and

\[
\Delta_{0,1,a}=\Delta,\qquad
e=|U|-(R+1)=1,\qquad
\kappa(U)=2.
\tag{7.3}
\]

All three weights are \(L=r_*+1\).  No alternate witness of weight at
most \(r_*\) exists: the difference of such an error and the displayed
error would be a nonzero codeword of weight at most

\[
L+r_*=699{,}051<d.
\]

The three support locators are pairwise coprime.  If the evaluation
domain is indexed cyclically, the three sets may be chosen as consecutive
proper exponent intervals, each with trivial shift stabilizer.

The declared noncontainment condition can also be met.  For slopes \(0\)
and \(1\), take \(k\) common-zero points and one point in the opposite
nonzero block, then extend inside the error zero mask to size \(A\).  For
slope \(a\), take \(D\setminus U\), two points of \(E_0\), and one point
of \(E_1\).  Any codeword matching \(g\) there would have the form
\(M_Uh\) with \(\deg h\le1\); the two \(E_0\) values force
\(h=1/(1-a)\), while the \(E_1\) value forces \(h=-1/a\), a contradiction.
Again extend to size \(A\).

The cardinalities needed here are exact:

\[
|E_a\cup(D\setminus U)|=L+k-2\ge k,\qquad
|D\setminus E_\eta|=n-L\ge A.
\]

This is a route-control fixture, not a surviving branch-3 counterexample:
the complete three-slope family is itself paid by the global carrier
with \(\kappa=2\), and it is also below the predecessor small-family
threshold.  Other heavy witnesses for the same slopes are not classified.
Its purpose is only to reject any proposed lemma saying that small local
\(e\) forces the displayed TDD supports themselves to share a locator factor
or a nontrivial cyclic stabilizer.

## 8. Raw union enumeration does not pay

Let

\[
c=|D\setminus U|=k-1-e.
\]

A hypothetical one-key-per-union count has \(\binom nc\) keys.  In the
near-full-union tail,

\[
\sum_{c=0}^{2}\binom nc
=2{,}199{,}024{,}304{,}129
<
B_{\rm rem},
\tag{8.1}
\]

but

\[
\sum_{c=0}^{3}\binom nc
=1{,}537{,}228{,}672{,}810{,}876{,}929
>
B_{\rm rem}.
\tag{8.2}
\]

Thus even a one-key-per-union terminal could fit only for

\[
e\ge k-3=1{,}048{,}573.
\]

That is not a proved injection.  Worse, for every fixed \(U\) with
\(e\ge1\), the projective defect multiplicity (3.5) is at least
\(q_{\rm line}+1\), already vastly above \(B_{\rm rem}\).  At \(e=0\)
the projective multiplicity is one, but \(\binom n{R+1}\) is enormous.
Raw \((U,[Q])\) enumeration therefore never supplies the missing owner.

Any union terminal needs a new canonical slope injection or a proved
bounded multiplicity theorem.

## 9. Frozen fail-closed owner order

For the complete retained family, apply:

1. a named already-paid quotient, periodic, Johnson, or common-support
   owner;
2. one certified global carrier of excess at most ten;
3. the intrinsic complete-selector affine-core terminal \(s_*\le3\);
4. a future deduplicated TDD-root union only after an injection or bounded
   multiplicity theorem is proved;
5. otherwise emit
   `UNPAID_PRIMITIVE_INTRINSIC_RANK3_TDD_SPREAD`.

The packet explicitly forbids:

- transferring high-union status from one selector to another without first
  checking the intrinsic minimum \(\kappa_*\);
- paying a local \(e\le9\) triple as though its union were global;
- inferring intrinsic complete-selector rank from one triple or an arbitrary
  nonminimizing selector;
- charging the rank-\(\le3\) cap on arbitrarily many subfamilies;
- confusing triple excess \(e\) with carrier excess \(e+1\);
- counting support unions without defect multiplicity control; or
- forcing a compatible residual into an existing owner.

## 10. Verdict and next object

**Verdict:** GREEN for (3.3), (3.4), (4.1), (5.5), (5.7), and the
rank-\(\le3\) conditional terminal; RED for the claim that low TDD excess
alone closes the residual; YELLOW for branch 3 and the KoalaBear row.

No ledger change is justified:

\[
U_{\rm paid}=2{,}602{,}502{,}999,\qquad
B_{\rm rem}=274{,}980{,}725{,}508{,}892{,}088.
\]

The next exact object is the first unpaid intrinsic affine-rank stratum, not
a claim that every remaining received pair has rank exactly four:

```text
INTRINSIC_GLOBAL_CARRIER_EXCESS kappa_* AT_LEAST_11
AND INTRINSIC_ACTUAL_AFFINE_RANK s_* EXACTLY_4
AND ITS_TDD_DEFECT_SPAN_RANK EXACTLY_3
AND FIVE_ACTUAL_SUPPORTS_RECOVER_THAT_SELECTOR'S_COMPLETE_UNION.
```

It must route to an existing quotient/periodic owner, one global carrier,
a genuinely budget-fitting canonical injection, or remain an explicit
primitive rank-three TDD spread.

No \(m>2\), degree-three parameter class, \(U_Q/U_A\) extrapolation, Lean
formalization, or Paper-D theorem promotion is authorized by this packet.
