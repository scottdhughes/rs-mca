# Reduced-CRT incidence lemma for the `(3,1,3,(2,2,2))` frontier

**Status:** PROVED-LOCAL and cross-model GREEN; the frozen row refinement is
banked. The reduced-CRT algebra, pointwise core-agreement bridge, exact-system
exhaustivity, and exact-support disjointness argument are proved below under
explicit hypotheses. The old cross-model YELLOW is retained as audit history;
the fresh review and its upstream-context supplement both returned GREEN with
ledger authorization YES.

## Frozen statement

Let `k` be a field. Let `R,B_1,B_2,B_3 in k[X]` be monic and pairwise
coprime, with `deg R=1` and `deg B_i=2`. Put

\[
B=B_1B_2B_3=X^6+b_5X^5+\cdots+b_0.
\]

For distinct nonzero labels `c_1,c_2,c_3`, let `G` be the unique residue
class modulo `B` satisfying

\[
G\equiv c_iR^{-1}\pmod{B_i},\qquad \deg G<6,
\]

and write `G=g_5X^5+\cdots+g_0`. For

\[
F=X^3+f_2X^2+f_1X+f_0,
\]

let `K(F)` be the `X^3,X^4,X^5` coefficient vector of `FG mod B`. Then

\[
K(F)=M(f_0,f_1,f_2)^T+u,
\]

where

\[
M=\begin{pmatrix}
g_3&-b_3g_5+g_2&b_3b_5g_5-b_3g_4-b_2g_5+g_1\\
g_4&-b_4g_5+g_3&b_4b_5g_5-b_4g_4-b_3g_5+g_2\\
g_5&-b_5g_5+g_4&b_5^2g_5-b_5g_4-b_4g_5+g_3
\end{pmatrix}
\]

and

\[
u=\begin{pmatrix}
-b_3b_5^2g_5+b_3b_5g_4+b_3b_4g_5+b_2b_5g_5-b_3g_3-b_2g_4-b_1g_5+g_0\\
-b_4b_5^2g_5+b_4b_5g_4+b_4^2g_5+b_3b_5g_5-b_4g_3-b_3g_4-b_2g_5+g_1\\
-b_5^3g_5+b_5^2g_4+2b_4b_5g_5-b_5g_3-b_4g_4-b_3g_5+g_2
\end{pmatrix}.
\]

For the profile interpretation, impose the following additional hypotheses.
The evaluation blocks are pairwise disjoint. The core `C` consists of four
distinct `k`-points, `R=X-beta` locates the retained background agreement
`beta` and has no root in `C`, and the received word is zero on the core and
background. Choose the unique restored core point `h`, and put

\[
D=C\setminus\{h\},\qquad F=L_D,\qquad
H=L_C/F=X-h,\qquad V=FG\bmod B,\qquad W=RHV.
\]

Thus `F` is a split squarefree monic cubic with root set exactly `D`. These
hypotheses are part of the lemma; a nonsplit or repeated locator, a
core/background overlap, or nonzero received data on the core is outside its
scope.

For every restored core point `h`, substitute the actual locator

\[
F_h=L_{\rm core}/(X-h).
\]

Then the reduced-CRT incidence stratifies as follows.

1. `rank M=3`: at most one monic cubic `F` satisfies `K(F)=0` for the fixed
   cofactor-support pattern.
2. `rank M<3` and `rank[M|u]>rank M`: the affine system is empty.
3. `rank M<3` and `rank[M|u]=rank M`: every solution pair
   `V=FG mod B`, `deg V<=2`, has `deg gcd(F,V)>0`. If `F=L_D`, then there is
   an `alpha in D` with `(X-alpha) | gcd(F,V)`. This gives
   `W(alpha)=0=U(alpha)`, so the actual missed core is
   `D\setminus Z(V)` and has size at most two. Hence the compatible rank-drop
   stratum is empty in the exact `d=3` profile.

Consequently, for each fixed cofactor-support pattern the exact profile has at
most one codeword: full rank permits at most one monic cubic, affine
inconsistency permits none, and compatible rank drop migrates to `d<=2`.

## Proof

The displayed matrix is obtained by reducing the four basis elements
`G,XG,X^2G,X^3G` modulo `B` and selecting degrees three through five. This
also proves the affine identity `K(F)=M(f_0,f_1,f_2)^T+u`.

### Exhaustivity of the reduced system

Every exact target codeword is represented by this system. Indeed, let `P` be
its degree-`<5` explaining polynomial. Its unique core agreement `h` and
unique background agreement `beta` are distinct zeros because the received
word is zero on the core and background. With `H=X-h` and `R=X-beta`,

\[
P=RHV,\qquad \deg V\le2.
\]

For the exact two-point agreement set `S_i` in labelled petal `i`, let
`B_i=L_{S_i}`. On `S_i`, the received word is `c_iL_C=c_iHF`, while
`P=RHV`. Since the petals are disjoint from the core, `H` is nonzero there,
so

\[
RV-c_iF=0\quad\hbox{on }S_i.
\]

Therefore `B_i | (RV-c_iF)`, with quotient of degree at most one. This is
exactly the divided fixed-syndrome system. Conversely, its congruences give
the selected petal agreements. Thus the rank classification bounds every
exact-profile codeword, not merely candidates constructed from the system.

Assume `rank M<3` and the monic affine system is compatible. Compatibility
gives `rank[M|u]=rank M<=2`. Therefore the homogeneous space

\[
\mathcal U=\{F\in k[X]:\deg F\le3,\;\deg(FG\bmod B)\le2\}
\]

has dimension at least two. Choose independent `F_0,F_1 in U` and put
`V_i=F_iG mod B`, so `deg V_i<=2`. A nonzero `F_i` has nonzero `V_i`:
otherwise the CRT unit `G` would give `F_i=0 mod B`, impossible for a nonzero
polynomial of degree below six. Since

\[
B\mid F_0V_1-F_1V_0
\]

but

\[
\deg(F_0V_1-F_1V_0)\le3+2=5<6=\deg B,
\]

we have the polynomial identity `F_0V_1=F_1V_0`.

Let `g=gcd(V_0,V_1)` and write `V_i=gW_i`, with
`gcd(W_0,W_1)=1`. Unique factorization gives `F_i=AW_i` for one polynomial
`A`. Take `F_0` to be a monic cubic solution. If `W_0` were constant, then
`deg A=3`; the condition `deg F_1<=3` would force `W_1` to be constant too.
Then `(F_1,V_1)` would be a scalar multiple of `(F_0,V_0)`, contradicting
the choice of two independent kernel elements. Thus `deg W_0>0`, and
`gcd(F_0,V_0)` contains `W_0` as a nonconstant factor.

### Direct pointwise bridge

In the sunflower reconstruction, by definition,

\[
 D=C\setminus\{h\},\qquad F=L_D,\qquad H=L_C/F=X-h,
 \qquad W=RHV.
\]

Let `alpha in k` satisfy `(X-alpha) | gcd(F,V)`. Since `F=L_D` is split and
squarefree with root set exactly `D`, we have `alpha in D`; hence
`alpha != h`. Also `V(alpha)=0`, and therefore

\[
W(\alpha)=R(\alpha)H(\alpha)V(\alpha)=0=U(\alpha),
\]

where the last equality is the printed condition `U|_C=0`. This already gives
an additional core agreement. More precisely, `h` is an agreement because
`H(h)=0`. For `x in D`, distinctness of the core gives `H(x) != 0`, and
core/background disjointness gives `R(x) != 0`. Thus

\[
 W(x)=U(x)=0\quad\Longleftrightarrow\quad V(x)=0
 \qquad (x\in D).
\]

The core agreement set is exactly
`{h} union (D intersect Z(V))`, and the actual missed core is therefore

\[
 D\setminus Z(V).
\]

Because `gcd(F,V)` has positive degree and `F` is split squarefree, this set
has size at most two. The compatible rank-drop stratum cannot realize exact
`d=3`. This is a pointwise profile migration, not a periodicity or quotient
descent claim. The background-disjointness hypothesis is needed for the
displayed *exact* missed-core formula, not merely for the one-sided existence
of an extra zero.

### Exact-support disjointness

Fix the sunflower block partition. An exact codeword with

\[
(r,(a_i),d)=(1,(2,2,2),3)
\]

uniquely determines its one background agreement, its two agreement points in
each of the three labelled petals, and its one restored core point `h`: these
are simply the intersections of its exact agreement set with the disjoint
background, petal, and core blocks. Hence it has one and only one cofactor
support-pattern key. There are

\[
\binom21\binom42^3=432
\]

such keys. The restored point does not supply another factor of four: the
full-rank reduced map bounds *all* monic cubics, and therefore all four possible
core locators, by one for a fixed cofactor key. Once `F` is fixed, `V=FG mod B`
and `W=RHV` are fixed as well. Thus summing the per-key bound one over the 432
keys does not double-charge a codeword.

The pairwise-coprime locator and distinct nonzero label hypotheses construct
the CRT unit `G`. The kernel argument itself uses only that `G` is a unit
modulo `B`, `deg B=6`, `deg F<=3`, and `deg V<=2`. Split squarefreeness,
core/background disjointness, `h in C`, and `U|_C=0` enter only in the
pointwise bridge and exact missed-core formula.

## Exact certificates

- Sage derives `M,u`, checks the affine identity symbolically, replays all 432
  frozen `GF(19)` support patterns, and exhausts 18,900 normalized `GF(11)`
  charts. In `GF(11)`, all 60 actual-locator incidences on compatible rank
  drops satisfy the pointwise bridge and exact missed-core formula; there are
  zero bridge failures.
- The frozen `GF(19)` census has 408 `(rank M,rank[M|u])=(3,3)` patterns, 22
  `(2,3)` patterns, and two `(2,2)` patterns. All 38 monic cubics on the two
  compatible lines have nonconstant gcd with their reduced remainder. No
  actual split-core incidence occurs in this particular frozen layout.
- Python modular elimination, Singular, and Macaulay2 agree on two compatible
  migration controls, one affine-inconsistent control, and one full-rank
  control. Only resultant/discriminant/label-difference localization is used;
  generic saturation is not used.
- The Sage certificate prints the bridge hypotheses and catches mutations for
  core/background overlap, a nonsplit locator, a repeated-root locator,
  `alpha=h`, and a nonzero received core value.
- The Python ledger certificate uses the canonical background-plus-three-petal
  assignment key and catches a duplicated support-pattern assignment even when
  the textual pattern identifiers remain distinct.

The certificates are:

- `experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/certificate.json`
- `experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/cas_certificate.json`
- `experimental/data/certificates/l1-b9-frontier-31222-reduced-crt/ledger_certificate.json`

## Ledger consequence

For the 432 fixed cofactor-support patterns, the locally proved and freshly
reviewed lemma replaces the old charge

\[
432\cdot19^2=155{,}952
\]

by `432`. The exact finite all-profile bound changes from `1,503,967` to
`1,348,447`, and the unresolved bound from `668,803` to `513,283`. The new
largest unresolved profile is

\[
(\ell,d,r,t,(a_i))=(4,3,2,3,(2,2,1)),\qquad (G_2,G_R)=(4,4),
\]

with charge `155,952`. The fresh cross-model reviewer independently checked the
bridge, exact-system exhaustivity, canonical assignment, owner partition,
75-row replacement, arithmetic, and mutation suites and authorized this bank.

## Literature check

After the component factors were frozen, TheoremSearch returned Padé and
rational-interpolation uniqueness analogues, including Proposition 3.1 of
[Adukov--Ibryaeva](https://arxiv.org/abs/1112.5694) and Proposition 2.1 of
[Claeys--Wielonsky](https://arxiv.org/abs/1112.2887). Neither result is needed
for the proof above: the load-bearing step is the elementary degree gap plus
unique factorization. No literature theorem is imported into the certificate.

## Reproduction

```bash
/usr/local/bin/sage experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_lemma.sage
/usr/local/bin/sage experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_lemma.sage --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_cas.py
python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_cas.py --tamper-selftest
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_ledger.py
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_31222_reduced_crt_ledger.py --tamper-selftest
```

## Review gate and scope

The prior cross-model reviewer confirmed the kernel-dimension, degree-gap,
UFD, and zero-remainder steps but returned YELLOW because the pointwise bridge
and disjointness proof were absent. The fresh review in
`l1_b9_frontier_31222_reduced_crt_cross_model_review_v2.md` read the revised
packet and independently replayed the exact gates; a supplemental fresh pass
read the upstream reconstruction-collapse note in full. Both returned GREEN
with ledger authorization YES. This closes only the named local row. No
`m>2`, PR `#763`, Lean, commit, or GitHub action is authorized here.
