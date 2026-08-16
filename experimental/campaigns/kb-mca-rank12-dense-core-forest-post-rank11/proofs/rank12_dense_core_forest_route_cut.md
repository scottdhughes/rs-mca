# Rank-twelve dense-core forest route cut

## 1. Setup

Put

\[
R=1,048,576,\qquad d=67,472,
\]

so every complete shortening row is

\[
(n_K,K,m_K)=(R+K,K,d+K).
\]

The KoalaBear budget and disjoint near-rational charge are

\[
B_*=274,980,728,111,395,087,\qquad N_{\rm near}=134,944.
\]

If affine error rank twelve were over budget, the reversible gauge and the
already-paid lower ranks would produce a post-near family \(Z_{11}\) with

\[
|Z_{11}|\ge L_0:=B_*-N_{\rm near}+1
=274,980,728,111,260,144                                      \tag{1}
\]

and explanation direction dimension at most eleven.

For a family of direction dimension at most \(s\), the parent stack gives one
frozen minimizing pair \(e_\gamma=(a_\gamma,b_\gamma)\), complete pair core

\[
H_\gamma=\{x:r_0(x)=a_\gamma(x),\ r_1(x)=b_\gamma(x)\},
\]

and support margin \(\theta_\gamma\) satisfying

\[
|H_\gamma|\ge d+K-\theta_\gamma,\qquad
\sum_\gamma\theta_\gamma\le C_s(K),                         \tag{2}
\]

where

\[
C_s(K)=\left\lfloor\max\left\{
\frac{(R+K)^{\underline{s+1}}}
     {(d+K)(d+1)^{\overline{s-1}}},
\frac{(R+s)^{\underline{s+1}}}
     {(d+1)^{\overline s}}
\right\}\right\rfloor.                                      \tag{3}
\]

The same complete-agreement shortening semantics as the parent are retained
throughout.

## 2. Coupled pair-type ceiling

For one pair type \(e\), define its deficiency

\[
\delta_e=\max\{1,m_K-|H_e|\}.                               \tag{4}
\]

Every record owned by \(e\) has \(\theta_\gamma\ge\delta_e\). Its exception
sets outside \(H_e\) are pairwise disjoint, since at one coordinate outside
the core the affine pair equation determines at most one finite slope.
Consequently one deficiency-\(\delta\) type owns at most

\[
c_\delta=
\left\lfloor\frac{R-d+\delta}{\delta}\right\rfloor.          \tag{5}
\]

### 2.1 Pair-core Plotkin prefix

Distinct pair types have

\[
|H_e\cap H_f|\le K-1.                                       \tag{6}
\]

Indeed, on the intersection both degree-\(<K\) endpoint differences vanish;
\(K\) common evaluation roots would make both differences zero.

Let \(N_t\) be the number of pair types with \(\delta_e\le t\), and put

\[
n=R+K,\quad h=d+K-t,\quad\lambda=K-1.
\]

Every associated core has size at least \(h\) and pairwise intersections at
most \(\lambda\). If \(N_t h\ge n/2\), Cauchy applied to coordinate
incidences gives

\[
N_t(h^2-\lambda n)\le n(h-\lambda).                         \tag{7}
\]

Thus, when \(h^2-\lambda n>0\),

\[
N_t\le
\max\left\{
\left\lceil\frac n{2h}\right\rceil-1,\
\left\lfloor\frac{n(h-\lambda)}
{h^2-\lambda n}\right\rfloor
\right\}.                                                   \tag{8}
\]

When the denominator is nonpositive, (8) contributes no bound.

### 2.2 Ordinary affine-pair prefix

The ordinary affine list theorem and sub-square interleaving collapse give

\[
N_t\le
Q_s(t):=
\left\lfloor
\frac{\binom{R+s}{s}}{\binom{d-t+s}{s}}
\right\rfloor                                               \tag{9}
\]

whenever \(Q_s(t)^2<p^6\). This is used only with the displayed strict
field guard.

Let \(G_t^{\rm raw}\) be the minimum of the available bounds (8) and (9), and
make it monotone by

\[
G_t=\max_{1\le u\le t}G_u^{\rm raw},\qquad G_0=0.            \tag{10}
\]

This enlarges the raw caps and is therefore safe.

### 2.3 Exact resource fill

Fix a cutoff \(J\). There are at most \(G_t-G_{t-1}\) new type slots of
exact deficiency \(t\), each with capacity \(c_t\) and per-record resource
cost at least \(t\). Since costs increase with \(t\), the integral optimum
fills these slots greedily in increasing \(t\), allowing a partial final
layer. Any remaining record has margin at least \(J+1\). This yields an
exact upper bound \(U_s(K,J)\).

Only the following nine cells are used:

\[
\begin{array}{c|r|r|r}
s&K&J&U_s(K,J)\\ \hline
11&4976&406&251872885956938780\\
10&4976&447&16183579359343472\\
9&4976&496&1039758346504303\\
8&4976&558&66805394184372\\
7&4976&637&4301754506033\\
6&4976&743&286886640300\\
5&4976&890&28821197274\\
4&4939&1110&1957361137\\
3&4423&3534&136821540.
\end{array}                                                 \tag{11}
\]

At the first eight cells, the ordinary pair cap is load-bearing. At the
rank-three cell, the Plotkin prefix sharpens the final prefix from \(4410\)
to \(3992\). Every ordinary cap used through its cutoff satisfies the
sextic-field guard.

## 3. Exact forest dynamic program

Complete-core incidence gives a coordinate contained in at least

\[
I_s(K,L)=
\left\lceil\frac{L(d+K)-C_s(K)}{R+K}\right\rceil             \tag{12}
\]

selected pair cores. Relative to one incident pair, the incident
pair-difference span is either:

- proper, yielding a source-bound child of direction dimension at most
  \(s-1\), load at least \(I_s(K,L)\), and row dimension \(K-1\); or
- full, making the coordinate global for the complete family and shortening
  the entire load to dimension \(K-1\) without a rank drop.

At \(K=s\), the full outcome is impossible because the full degree-\(<s\)
RS code contains the constant polynomial \(1\).

For target \(T\), define \(E_s(K;T)\) as the largest integer load which can
evade every selected cap in (11) and also evade producing a rank-at-most-two
descendant of load at least \(T\).

The base is

\[
E_2(K;T)=T-1.                                               \tag{13}
\]

Solving \(I_s(K,L)\le M\) for \(L\) gives

\[
P_s(K,M)=
\left\lfloor
\frac{M(R+K)+C_s(K)}{d+K}
\right\rfloor.                                              \tag{14}
\]

Therefore

\[
E_s(s;T)=
\min\{U_s(s),P_s(s,E_{s-1}(s-1;T))\},                       \tag{15}
\]

and for \(K>s\),

\[
E_s(K;T)=
\min\left\{
U_s(K),\
\max\left(
E_s(K-1;T),\
P_s(K,E_{s-1}(K-1;T))
\right)
\right\}.                                                   \tag{16}
\]

Here \(U_s(K)=+\infty\) except at the nine cells (11).

The maximum in (16) is load-bearing. The actual received line, not the
proof, determines whether the coordinate is full or proper.

## 4. Deployed computation

For

\[
T=9,342,183,
\]

the rank endpoint evasion ceilings at \(K=1,048,576\) are

\[
\begin{array}{c|r}
s&E_s(1,048,576;T)\\ \hline
2&9342182\\
3&136881788\\
4&1992326004\\
5&28985512639\\
6&421705605438\\
7&6135450719867\\
8&89267473921113\\
9&1298825246161540\\
10&18898180719798204\\
11&274980718357491817.
\end{array}                                                 \tag{17}
\]

Comparing the final entry with (1),

\[
L_0-E_{11}(1,048,576;T)=9,753,768,327>0.                    \tag{18}
\]

Thus every over-budget affine-error-rank-twelve line produces one
source-bound descendant with at least \(9,342,183\) distinct slopes and
direction dimension at most two.

The target is exact for this declared certificate class:

\[
E_{11}(1,048,576;9,342,184)
=274,980,748,327,713,549
=L_0+20,216,453,405.                                       \tag{19}
\]

Equation (19) is a method wall, not an actual RS construction.

## 5. Full-code rank-two calibration

This subsection is conditional on a descendant retaining rank two through
whole-family shortening to \(K=2\). It is not used in the route theorem.

At \(K=2\), split at margin cutoff \(1922\). Exact values are

\[
C_2(2)=253,241,283,\qquad
|Z_{\rm high}|\le131,690,
\]

so a \(9,342,183\)-slope family has at least

\[
9,210,493
\]

low records. Their cores have size at least \(65,552\), pairwise
intersection at most one, and (8) gives at most fifteen pair types.
Therefore one pair owns at least

\[
\left\lceil\frac{9,210,493}{15}\right\rceil=614,033         \tag{20}
\]

slopes.

A deficiency-two pair owns at most

\[
\left\lfloor\frac{981,104+2}{2}\right\rfloor=490,553,
\]

so the pair in (20) has deficiency one. Its exception sets are disjoint and
at least

\[
2\cdot614,033-981,105=246,961                               \tag{21}
\]

owned records have singleton exceptions.

These numbers identify the next owner problem but do not contradict local
constraints. Fifteen disjoint `m-1` cores fit in the endpoint universe, and
the low load can be distributed among fifteen locally legal singleton stars.

## 6. Boundary

The theorem is a direct, source-bound rank-twelve route cut. It does not pay
the resulting rank-two forest, sum different leaves, regenerate the active-v4
chronology, or close KoalaBear.

The first unproved implication is:

> Every source-bound rank-at-most-two descendant forest of load at least
> `9,342,183` either merges into one existing chronology owner or has an
> aggregate leaf/exception incidence bound below that load.

A per-star use of (20), a per-locator cancellation, or another single-path
descent is insufficient.
