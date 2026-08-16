# Paying KoalaBear affine error rank eleven by global-core descent

## 1. Exact inherited interface

Write

\[
 R=n-K=1{,}048{,}576,
 \qquad d=m-K=67{,}472,
\]

so every complete shortening used below has parameters

\[
 (n_K,K,m_K)=(R+K,K,d+K).
\]

The deployed bad-slope budget and intrinsic near-rational charge are

\[
 B_*=274{,}980{,}728{,}111{,}395{,}087,
 \qquad N_{\rm near}=134{,}944.
\]

Suppose, for contradiction, that an affine-error-rank-eleven line is over
budget.  After removing the disjoint near-rational family and applying the
reversible rank gauge from the predecessor stack, there is a selected
post-near family `Z_10` with

\[
 |Z_{10}|\ge L_{10}:=B_*-N_{\rm near}+1
 =274{,}980{,}728{,}111{,}260{,}144,              \tag{1}
\]

whose explanations lie in one affine translate `c_0+C'` of a
Reed--Solomon direction code with

\[
 s:=\dim C'\le10.
\]

The lower-rank branches are already paid.  It is therefore enough to treat
`s=10`; if a later subfamily has smaller actual dimension, we skip directly
to that rank.

For every selected slope `gamma`, retain one exact size-`m_K` support
`S_gamma`, one explanation `h_gamma`, and one minimizing direction
`b_gamma in C'`.  Put

\[
 a_\gamma=h_\gamma-\gamma b_\gamma
\]

and define the complete minimizing-pair core

\[
 H_\gamma=
 \{x:r_0(x)=a_\gamma(x),\ r_1(x)=b_\gamma(x)\}.
\]

If `theta_gamma` is the selected support margin, then

\[
 S_\gamma\setminus H_\gamma
\]

has size at most `theta_gamma`, so

\[
 |H_\gamma|\ge d+K-\theta_\gamma.                  \tag{2}
\]

The pointwise support-margin theorem gives, for a direction space of
dimension at most `s`,

\[
 \sum_{\gamma\in Z_s}\theta_\gamma\le C_s(K),       \tag{3}
\]

where

\[
 C_s(K)=\left\lfloor\max\left\{
 \frac{(R+K)^{\underline{s+1}}}
      {(d+K)(d+1)^{\overline{s-1}}},
 \frac{(R+s)^{\underline{s+1}}}
      {(d+1)^{\overline{s}}}
 \right\}\right\rfloor.                            \tag{4}
\]

Both endpoint resources increase with the affine rank, since their
successive ratios are respectively

\[
 \frac{R+K-s-1}{d+s}>1,
 \qquad
 \frac{R+s+1}{d+s+1}>1.
\]

Thus (4) is valid uniformly when the actual direction dimension is below
`s`.

## 2. Complete-core incidence

Summing (2) and using (3),

\[
 \sum_{x\in D_K}
 \#\{\gamma:x\in H_\gamma\}
 =\sum_\gamma |H_\gamma|
 \ge |Z_s|(d+K)-C_s(K).
\]

Consequently some actual coordinate `x` lies in at least

\[
 I_s(K,L):=
 \left\lceil
 \frac{L(d+K)-C_s(K)}{R+K}
 \right\rceil                                      \tag{5}
\]

complete pair cores whenever `|Z_s|>=L`.

Fix one incident minimizing pair `e_0=(a_0,b_0)` and let

\[
 U_x=\operatorname{span}\{
 a_\gamma-a_0,\ b_\gamma-b_0:
 x\in H_\gamma
 \}\le C'.                                          \tag{6}
\]

Every generator in (6) vanishes at `x`.

### Lemma 2.1: dimension drop or global pair core

Exactly one of the following useful outcomes holds.

1. `dim U_x<s`.  After subtracting the codeword pair `(a_0,b_0)`, every
   incident explanation lies in `U_x` and vanishes at `x`.  Locator division
   and deletion of `x` produce at least `I_s(K,L)` bad slopes in row
   `(R+K-1,K-1,d+K-1)` with direction dimension at most `s-1`.
2. `U_x=C'`.  Since every word of `U_x` vanishes at `x`, every word of `C'`
   vanishes there.  For any selected pair `(a,b)`, both differences
   `a-a_0` and `b-b_0` lie in `C'`, so `(a(x),b(x))=(a_0(x),b_0(x))`.
   The base pair is incident and equals the received pair at `x`; therefore
   **every selected minimizing pair equals the received pair at `x`**.
   The coordinate is a whole-family pair-core coordinate.  Locator division
   shortens the complete selected family, preserves all `L` slopes, and
   preserves direction dimension `s`.

#### Proof

Only the shortening semantics require care.  Let `A_gamma` be the complete
scalar agreement domain of the selected explanation.  It contains the frozen
bad support, and hence is itself pair-noncontained.  In either case above,
`x in A_gamma` for every slope being shortened.  Interpolate the received
pair at `x`, subtract that codeword pair, divide every received word and
explanation by `X-x`, and delete `x`.

If a codeword pair simultaneously explained the shortened received pair on
`A_gamma\setminus{x}`, multiplying by `X-x` and adding the interpolating pair
would explain the original received pair on all of `A_gamma`, a
contradiction.  Thus each slope remains support-wise MCA-bad.

The next-stage exact-support interface is also preserved.  In an RS row of
dimension `K'`, let `A` be pair-noncontained with `|A|>=m'>K'`.  If every
`m'`-subset of `A` were pair-contained, adjacent `m'`-subsets would have
intersection size `m'-1>=K'`; uniqueness of degree-`<K'` interpolation would
force their explaining pairs to coincide.  The graph of `m'`-subsets under
single-coordinate swaps is connected, so one pair would explain all of `A`, a
contradiction.  Hence `A` contains an exact size-`m'` pair-noncontained
support.

The same locator lift shows that post-near status is preserved: a shortened
distance at most `d` would lift to an original distance at most `d`.  Division
is injective on any direction space vanishing at `x`, so its dimension is
preserved.  This proves both alternatives.  ∎

When `K=s`, the second alternative is impossible: an `s`-dimensional subcode
of the `s`-dimensional degree-`<s` Reed--Solomon code is the whole code and
contains the constant polynomial `1`, which does not vanish at any deployed
coordinate.

## 3. Delayed dimension descent is worst

Starting with a rank-`s` family of load `L_s`, apply Lemma 2.1 repeatedly.
Whole-family coordinates may be removed until a proper-span coordinate is
encountered.  The next-rank load is at least `I_s(K,L_s)` at the dimension
where the drop occurs.

For the deployed row and the loads below, exact integer evaluation proves

\[
 I_s(K,L_s)\ge I_s(s,L_s)
 \qquad(s\le K\le1{,}048{,}576),                    \tag{7}
\]

for every `2<=s<=10`.  No floating-point comparison is used.  The verifier
updates

\[
 (R+K)^{\underline{s+1}}
\]

by the exact recurrence

\[
 P_s(K+1)=P_s(K)\frac{R+K+1}{R+K-s}
\]

and checks all deployed cells.  There are no strict decreases, and the unique
first minimum is always `K=s`.

Thus the weakest possible recursion is

\[
 L_{s-1}:=I_s(s,L_s)
 =\left\lceil
 \frac{L_s(d+s)-C_s(s)}{R+s}
 \right\rceil.                                      \tag{8}
\]

Exact evaluation gives

\[
\begin{array}{c|r|r}
s&C_s(s)&L_{s-1}\\ \hline
10&861057176799343503&17695628624859819\\
9&55413538236037195&1138737729126327\\
8&3566101912297072&73278302796469\\
7&229490967859328&4715427489703\\
6&14768331186162&303431536894\\
5&950366735057&19525148223\\
4&61156835934&1256382675\\
3&3935435218&80843204\\
2&253241283&5201865.
\end{array}                                         \tag{9}
\]

Therefore an unsafe rank-eleven family would force at least

\[
 L_1=5{,}201{,}865                                 \tag{10}
\]

distinct bad slopes in the final row

\[
 (n_1,K_1,m_1)=(1{,}048{,}577,1,67{,}473).          \tag{11}
\]

## 4. Weighted affine-line endpoint

At `K_1=1`, codewords are constants.  Represent each coordinate `x` by the
affine graph line

\[
 \ell_x:\quad \lambda=r_0(x)+\gamma r_1(x)
\]

in the `(gamma,lambda)` plane.  Merge identical lines into clone classes and
retain their original coordinate multiplicities.  A selected slope and its
constant explanation give a point `P_gamma` incident to weighted line mass at
least

\[
 m_1=67{,}473.
\]

Pair noncontainment means that the complete agreement domain contains at
least two distinct clone lines.  Choose an exact `m_1`-coordinate sub-support
retaining two classes.

Put

\[
 q=\frac{m_1-1}{2}=33{,}736.
\]

### 4.1 No dominant clone class

Suppose every clone class contributes at most `q` coordinates to the chosen
support.  The number of unordered coordinate pairs drawn from different clone
classes is at least

\[
 q(q+1)=1{,}138{,}151{,}432.                         \tag{12}
\]

Indeed, this is a conservative lower bound for every positive composition of
`2q+1` with parts at most `q`.  A pair of distinct affine graph lines meets in
at most one finite point.  Cross-pairs charged by distinct selected points are
therefore disjoint, and

\[
 L_{\rm low}
 \le\left\lfloor
 \frac{\binom{1{,}048{,}577}{2}}{q(q+1)}
 \right\rfloor
 =483.                                               \tag{13}
\]

### 4.2 A dominant clone class

Now suppose one clone class contributes more than `q` support coordinates.
It is unique; charge the point to that dominant graph line.

Let the globally distinct clone lines capable of dominating be
`ell_1,...,ell_t`, with full coordinate weights `w_i`.  Necessarily
`w_i>=q+1`, so

\[
 t\le\left\lfloor\frac{n_1}{q+1}\right\rfloor=31.   \tag{14}
\]

Define the effective outside deficiency

\[
 a_i=\max\{1,m_1-\min(w_i,m_1-1)\},
 \qquad 1\le a_i\le q,                               \tag{15}
\]

and the relaxed outside weight

\[
 W_0=n_1-\sum_{i=1}^t(m_1-a_i)
    =n_1-tm_1+\sum_i a_i.                            \tag{16}
\]

Every point charged to `ell_i` requires at least `a_i` support coordinates
from other clone lines.  At most `t-1` such points can meet another dominant
line, one for each other line.  All remaining charged points use only
non-dominant lines, whose total weight is at most `W_0`.  Hence

\[
 N_i\le t-1+\left\lfloor\frac{W_0}{a_i}\right\rfloor
\]

and

\[
 L_{\rm high}
 \le t(t-1)+W_0\sum_{i=1}^t\frac1{a_i}.             \tag{17}
\]

It remains to optimize (17).  Hold all variables except `a_i` fixed and put

\[
 C_0=n_1-tm_1+\sum_{j\ne i}a_j,
 \qquad Q_0=\sum_{j\ne i}\frac1{a_j}.
\]

The variable part is

\[
 f(a)=(C_0+a)(Q_0+1/a).
\]

If `C_0>=0`, then `f''(a)=2C_0/a^3>=0`, so the maximum on `[1,q]` is at an
endpoint.  If `C_0<0`, then

\[
 f'(a)=Q_0-C_0/a^2>0,
\]

so moving to `a=q` increases the value and preserves feasibility.  Iterating
shows that a maximizer has every

\[
 a_i\in\{1,q\}.                                     \tag{18}
\]

The remaining exact enumeration has only

\[
 \sum_{t=1}^{31}(t+1)=527
\]

formal endpoint rows, of which 271 are feasible.  Its maximum is

\[
 t=8,\qquad a_1=\cdots=a_8=1,
 \qquad W_0=508{,}801,
\]

and (17) gives

\[
 L_{\rm high}\le8\cdot7+508{,}801\cdot8
 =4{,}070{,}464.                                    \tag{19}
\]

Combining the disjoint low- and high-dominant cases,

\[
 |Z_1|\le483+4{,}070{,}464
 =4{,}070{,}947.                                    \tag{20}
\]

This contradicts (10), with exact slack

\[
 5{,}201{,}865-4{,}070{,}947
 =1{,}130{,}918.                                    \tag{21}
\]

## 5. Conclusion and boundary

No over-budget post-near affine-error-rank-eleven family exists.  Restoring
the disjoint near-rational charge `134,944` proves that the complete affine
error rank eleven branch fits `B_*`.

This is a direct branch payment.  It does not regenerate the active-v4
first-match chronology, move a ledger atom, pay affine error rank twelve, or
close the KoalaBear row.
