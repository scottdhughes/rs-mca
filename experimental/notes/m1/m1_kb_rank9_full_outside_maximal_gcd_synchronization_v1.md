# M1 KoalaBear full-outside maximal-gcd synchronization v1

Status: **PROVED CONDITIONAL THREE-POINT SYNCHRONIZATION / DEPLOYED
COMPLETE-SELECTOR PROVENANCE OPEN / NO LEDGER MOVEMENT**.

This packet closes the local algebra of the full-outside, rank-two,
maximal-gcd terminal without repeating the false generic
full-projective/GM emptiness route.  For one fixed source-bound complete
selector, all contributing maximal-gcd graph lines have one common reduced
Möbius map.  Their selected finite slopes therefore lie in one common
\(\mathbf F_p\)-projective subline and have deduplicated cardinality at most
\(p+1\).

The current artifacts do not construct or enumerate the required deployed
complete selector.  Consequently the local lemma is proved, but its
prospective \(p+1\) owner is **not** charged to the KoalaBear ledger.

## 1. Exact statement

Fix the KoalaBear row

\[
 p=2{,}130{,}706{,}433,\qquad
 B=\mathbf F_p\subset F=\mathbf F_{p^6},\qquad D\subset B,
\]

\[
 n=2^{21},\quad k=2^{20},\quad
 A=1{,}116{,}048,\quad j=n-A=981{,}104,
 \quad t=A-k=67{,}472.
\tag{1.1}
\]

Work inside one fixed post-owner, source-bound complete selector for one
received pair.  The selector has carrier \(V\), sparse source pair
\((\epsilon _0,\epsilon _1)\), and

\[
 \Sigma=\operatorname{supp}(\epsilon _0)
       \cup\operatorname{supp}(\epsilon _1).
\tag{1.2}
\]

Restrict to the full-outside subcell

\[
 \Sigma\cap V=\varnothing.
\tag{1.3}
\]

For each contributing rich graph line \(L\), let \(P_L,Q_L\) be its
polynomial lifts.  Assume coefficient rank two and the **full**, monic gcd

\[
 H_L=\gcd(P_L,Q_L),\qquad \deg H_L=k-2.
\tag{1.4}
\]

The distinction between \(H_L\) and the forced domain locator
\(G_L=L_{C_L}\) is essential: the latter can have smaller degree.  From
(1.4), write

\[
 P_L=H_L(U_{L,1}X+U_{L,0}),\qquad
 Q_L=H_L(V_{L,1}X+V_{L,0}),
\tag{1.5}
\]

with

\[
 U_{L,1}V_{L,0}-U_{L,0}V_{L,1}\ne0.
\tag{1.6}
\]

Define the reduced projective map

\[
 \phi_L([X:Z])=
 [-(U_{L,1}X+U_{L,0}Z):V_{L,1}X+V_{L,0}Z]
 \in\mathbf P^1(F).
\tag{1.7}
\]

Here and below, "contributing rich graph line" includes the imported
same-selector contract:

- \(\beta_L>0\) and \(J_L\ge21\);
- \(a_L=\epsilon_0-\operatorname{ev}(P_L)\) and
  \(b_L=\epsilon_1-\operatorname{ev}(Q_L)\), with the graph words extended
  by zero outside \(V\); and
- for every selected \(\eta\in\Gamma_L\), transversality gives a point in
  \(F_{\eta,L}=\{x\in W_L:a_L(x)+\eta b_L(x)=0\}\).

### Theorem 1.1 (full-outside maximal-gcd synchronization)

Under (1.1)--(1.7) and the printed contributing-line contract, every
maximal-gcd line in this one selector has the same map
\(\phi_L=\phi\).  Every selected projective slope on those lines belongs to

\[
 \phi\bigl(\mathbf P^1(B)\bigr).
\tag{1.8}
\]

Therefore the distinct finite selected slopes satisfy

\[
 \boxed{
 \left|\bigcup_L\Gamma_L^{\rm fin}\right|
 \le p+1=2{,}130{,}706{,}434.}
\tag{1.9}
\]

The union in (1.9) is taken before counting.  Lines, supports, witnesses,
charts, and determinant bases are not counted.

## 2. Three-point synchronization

For every \(h\in\Sigma\), full-outside source coupling gives

\[
 P_L(h)=\epsilon _0(h),\qquad
 Q_L(h)=\epsilon _1(h).
\tag{2.1}
\]

The pair on the right is nonzero by the definition of \(\Sigma\).  Hence
\(H_L(h)\ne0\).  Cancelling it projectively in (1.5) yields

\[
 \phi_L([h:1])
 =[-\epsilon _0(h):\epsilon _1(h)].
\tag{2.2}
\]

The full-outside rank-two floor from the active-source reindex is

\[
 |\Sigma|\ge t-x_L+2.
\tag{2.3}
\]

Every contributing rich line has

\[
 x_L\le\left\lfloor\frac j{20}\right\rfloor=49{,}055,
\]

so

\[
 |\Sigma|\ge
 67{,}472-49{,}055+2=18{,}419>2.
\tag{2.4}
\]

Thus any two maps \(\phi_L,\phi_{L'}\) agree on at least three distinct
projective inputs \([h:1]\).  Two elements of \(\operatorname{PGL}_2(F)\)
that agree on three distinct points are equal.  This proves the first
assertion of Theorem 1.1.

Notice what is not asserted.  The source labels in (2.2) need not lie in
\(\mathbf P^1(B)\), and the pair-global intrinsic projective syndrome field
may be all of \(F\).  The base-field objects are the inputs \([h:1]\), not
necessarily their images.

## 3. Moving-root bridge

The subline cap also needs every counted slope to be represented by a base
domain input.  This is not automatic from the quotient degree.

For \(\eta\in\Gamma_L\), the rich-pencil atlas defines

\[
 F_{\eta,L}
 =\{x\in W_L:a_L(x)+\eta b_L(x)=0\}.
\tag{3.1}
\]

Contributing lines have \(\beta_L>0\).  The imported transversality
argument proves

\[
 F_{\eta,L}\ne\varnothing
\qquad(\eta\in\Gamma_L).
\tag{3.2}
\]

Choose \(x\in F_{\eta,L}\).  Since \(W_L\subset V\subset D\subset B\)
and \(\Sigma\cap V=\varnothing\), the source pair vanishes at \(x\).
The source equations

\[
 a_L=\epsilon _0-\operatorname{ev}(P_L),\qquad
 b_L=\epsilon _1-\operatorname{ev}(Q_L)
\tag{3.3}
\]

turn (3.1) into

\[
 P_L(x)+\eta Q_L(x)=0.
\tag{3.4}
\]

Moreover \(x\in W_L\) means \(a_L(x),b_L(x)\) are not both zero; by
full-outside vanishing, \(P_L(x),Q_L(x)\) are not both zero.  Thus \(x\)
is not a common root and (3.4) gives

\[
 [\eta:1]=\phi_L([x:1])
\tag{3.5}
\]

for finite \(\eta\), with the analogous projective statement for infinity.
Since \(x\in B\) and all \(\phi_L\) are the common \(\phi\), (1.8) follows.
The image of \(\mathbf P^1(B)\) has exactly \(p+1\) projective points;
discarding projective infinity cannot increase the finite count.  This proves
(1.9).

Without (3.2), an arbitrary selected label need not be an image of a base
domain point and the \(p+1\) conclusion would be false.  The moving-root
bridge is therefore a load-bearing hypothesis, not a bookkeeping detail.

## 4. What the lemma closes

The proof permits all of the following:

- a nonsplit or nonbase common factor \(H_L\);
- a field-full pair-global projective syndrome plane;
- a nonstandard image \(\phi(\mathbf P^1(B))\);
- a pole of \(\phi\) at a base point.

It uses neither projective descent nor generic GM emptiness.  Upstream's
full-projective GM control already refutes that shortcut.

The theorem does **not** cover \(\deg\gcd(P_L,Q_L)<k-2\).  The reduced map
then has degree greater than one in general, and the separate terminal

```text
UNPAID_EXTENSION_LOWER_GCD_RATIONAL_MAP
```

remains open.

## 5. Deployed provenance route cut

The current deployed source-incidence contract reports:

```text
complete global first-match replay                  false
deployed complete-selector inventory                false
paying selector for every deployed source family    false
deployed rich-pencil selector constructed           false
deployed rich-pencil census                         false
full deployed producer validator                    false
```

There is no terminal-record artifact on which to check the hypotheses of
Theorem 1.1 record by record.  In particular, the existing \(J=166\)
maximal-gcd template has \(\beta_L=0\), no eight-outlier rank-nine binding,
and no regular first-match binding.  The exact toy controls are not deployed
selectors.

Accordingly, the former algebraic terminal is refined only conditionally.
The live deployed subterminal is

```text
UNBOUND_COMPLETE_SELECTOR_MAXIMAL_GCD_PROVENANCE
```

inside the enclosing terminal

```text
UNBOUND_DEPLOYED_SOURCE_INCIDENCE.
```

The charge becomes available only after one of the frozen Routes S, U, or C
is supplied:

1. a source-bound paying complete selector for every eligible source family;
2. a uniform theorem producing such a selector; or
3. an exhaustive deployed source-family census with a verified selector for
   every family.

The eventual owner must also intersect the synchronized union with the
current residual slope set, delete it exactly once, and restart/restrict the
downstream selector.  Until then, first-match disjointness is unproved.

## 6. Ledger and prospective arithmetic

The current banked ledger remains

\[
 U_{\rm paid}=2{,}603{,}484{,}104,
 \qquad
 B_{\rm remaining}=274{,}980{,}725{,}507{,}910{,}983.
\tag{6.1}
\]

Thus this packet has ledger movement zero.  The prospective, unbanked owner
would have cap

\[
 p+1=2{,}130{,}706{,}434
\]

and would give

\[
 U_{\rm paid}^{\rm prospective}=4{,}734{,}190{,}538,
\qquad
 B_{\rm remaining}^{\rm prospective}
 =274{,}980{,}723{,}377{,}204{,}549.
\tag{6.2}
\]

The exact one-cut replay would then give

\[
 T_{18{,}014}^{\rm prospective}=17{,}905{,}062{,}856{,}176,
\tag{6.3}
\]

\[
 E_{\max}^{\rm prospective}
 =5{,}257{,}735{,}913{,}360{,}750{,}952{,}280{,}320{,}052,
 017{,}938{,}027{,}249{,}181{,}774,
\tag{6.4}
\]

and \(K_{\rm remaining}=4{,}807{,}520\).  These values are printed to make
the value of the missing provenance theorem exact.  They are not part of the
banked ledger.

The values of \(U_Q\) and residual \(U_A\) remain unknown.

## 7. Exact control

The companion Sage replay works over
\(\mathbf F_5\subset\mathbf F_{5^6}\).  It constructs two distinct
nonbase degree-four common factors which agree at three source points and
uses one nonstandard reduced Möbius map with a base-point pole.  It checks:

- exact equality of the two source pairs at the three anchors;
- exact full gcd degree \(k_{\rm toy}-2=4\);
- equality of the gcd-reduced maps;
- a common six-point projective \(\mathbf F_5\)-subline;
- five finite images and one projective infinity image.

A countercontrol gives two distinct Möbius maps which agree at exactly two
base projective points.  Their two sublines have union size ten, exceeding
\(p+1=6\).  This proves that the third anchor is essential in the toy model.

These are exact toy-scale controls for the projective bookkeeping.  They do
not supply deployed selector provenance or prove the KoalaBear payment.

## 8. Dependencies, verdict, and next gate

### Proved inputs

- the canonical rich-pencil atlas and its moving-zero transversality floor;
- the fixed same-selector source equations;
- rank-one exclusion and the source-size floor on the full-outside cell;
- the current C5/base owner and exact deployed ledger;
- Möbius three-point rigidity.

### Unproved deployed inputs

- a source-bound complete-selector inventory or uniform replacement;
- an actual eight-outlier rank-nine and regular first-match binding;
- owner-order intersection, exact deletion, and downstream restart;
- lower-gcd rational-map payment, \(U_Q\), and residual \(U_A\).

**Verdict:** GREEN for Theorem 1.1 under its printed hypotheses.  YELLOW for
the deployed payment and the KoalaBear row.

The minimal next action is Route U: prove uniformly that every eligible
source family admits one complete selector whose full-outside maximal-gcd
records satisfy the frozen source contract.  If a compatible selector violates
that contract, print the first exact record and preserve it as a primitive
route cut.  Do not charge (1.9) merely by setting a Boolean readiness flag.
