# Four-block owner payment for affine error rank twelve

## 1. Inherited source-bound interface

Work in a shortened KoalaBear row

\[
(n,K,m)=(R+K,K,D+K),
\qquad R=1{,}048{,}576,
\qquad D=67{,}472,
\]

and write

\[
t=n-m=R-D=981{,}104.
\]

The repaired predecessor stack supplies one post-near rank-two explanation
family \(Z\) of

\[
|Z|=L_2=5{,}170{,}912
\]

distinct finite slopes. Each slope has a frozen exact size-\(m\) bad support,
one explanation, and one minimizing pair. All scalar pair-difference
explanations lie in a fixed two-dimensional Reed--Solomon direction code
\(C'\).

The exact common-locator parent proves that a proper rank-two drop at ambient
dimension \(K\) produces a rank-at-most-one leaf with a full source-bound
common pair core of degree

\[
c\ge c_{\min}(K)=K-\kappa(K).
\]

The rank-one leaf may be enlarged by other slopes whose frozen supports meet
that core. Because the enlarged family can have additional scalar-universal
coordinates, the only uniform cap available without a further source theorem
is the global all-dimension maximum

\[
\boxed{A_1=4{,}070{,}947}.                 \tag{1}
\]

We use that maximum, not the smaller capacity at \(\kappa(K)\).

Before selecting a proper drop, shorten every coordinate in the complete
pair core of the entire rank-two family. Hence no remaining coordinate is a
whole-family pair core.

Fix an actual proper-drop leaf, let \(C\) be its **full** common pair core,
put \(c=|C|\), and let \(W<C'\) be its one-dimensional direction space.
Fix one pair \(e_0\) in the leaf and translate the received pair by \(e_0\).
For an arbitrary original slope \(\gamma\), define the translated scalar
explanation

\[
p_\gamma=(a_\gamma-a_0)+\gamma(b_\gamma-b_0)\in C'.  \tag{2}
\]

Partition the original slope family according to its frozen support:

\[
Z=Z_{\rm in}\sqcup Z_{\rm out},
\]

where \(Z_{\rm in}\) consists of supports meeting \(C\). At a core
coordinate the evaluation kernel of \(C'\) equals \(W\), since evaluation is
nonzero on \(C'\) and \(W\) is one-dimensional. Thus every
\(\gamma\in Z_{\rm in}\) has \(p_\gamma\in W\), so

\[
|Z_{\rm in}|\le A_1.                                  \tag{3}
\]

It remains to pay \(Z_{\rm out}\) below the residual budget

\[
L_2-A_1=1{,}099{,}965.                                \tag{4}
\]

Put

\[
r=t-c,
\qquad
X=D_K\setminus C,
\qquad
|X|=m+r.
\]

Every frozen support in \(Z_{\rm out}\) is an \(m\)-subset of \(X\), so its
omission set has size \(r\).

## 2. Four slopes witness every genuinely two-dimensional residual

Suppose the exceptional explanations do not lie in one affine correction
ray. Modulo vector-valued affine functions of the slope, their residual rank
is then two. Consequently there are four distinct slopes
\(\gamma_1,\ldots,\gamma_4\) for which

\[
1,\quad Z,\quad f(Z),\quad g(Z)
\]

are linearly independent on those four evaluation points, where \(f,g\) are
coefficient functions in a basis of \(C'\). Equivalently, their vector-valued
interpolant has the form

\[
H(Z)=H_0+ZH_1+Z^2Q_2+Z^3Q_3,              \tag{5}
\]

with \(Q_2,Q_3\) a basis of \(C'\).

Let \(E_i\subset X\) be the size-\(r\) omission set of the frozen support at
\(\gamma_i\). These four omission sets cover \(X\). Otherwise some
coordinate lies in all four supports, so both independent second divided
differences vanish there. Evaluation would annihilate all of \(C'\); two of
the supported slopes then force the translated received pair itself to
vanish, producing a whole-family pair core, contrary to the prior shortening.

Thus

\[
X=E_1\cup E_2\cup E_3\cup E_4.             \tag{6}
\]

Define the clean blocks and dirty set

\[
B_i=E_i\setminus\bigcup_{j\ne i}E_j,
\qquad
Y=X\setminus\bigsqcup_i B_i.
\]

Write

\[
b_i=|B_i|,
\qquad y=|Y|,
\qquad d_i=|E_i\cap Y|,
\]

and set

\[
\delta=4r-|X|=3r-m.
\]

Then

\[
b_i=r-d_i,
\qquad
\sum_i d_i=y+\delta,
\qquad
\left\lceil\frac\delta3\right\rceil\le y\le\delta. \tag{7}
\]

The last inequality follows because every dirty coordinate is omitted at
least twice and at most four times.

## 3. Clean blocks are projective fibers

For \(i\in\{1,2,3,4\}\), let

\[
s_i=\sum_{j\ne i}\gamma_j,
\qquad
u_i=\sum_{j<k\atop j,k\ne i}\gamma_j\gamma_k,
\qquad
v_i=\prod_{j\ne i}\gamma_j.
\]

At a coordinate in \(B_i\), the other three base explanations agree with the
received affine line. Their second divided difference is therefore zero:

\[
Q_2+s_iQ_3=0.                                      \tag{8}
\]

Moreover \(Q_3\ne0\) on \(B_i\). If both \(Q_2,Q_3\) vanished, evaluation
would annihilate \(C'\), again producing a whole-family pair core.

Subtract the affine part \(H_0+ZH_1\). Expanding the cubic interpolation
identity on \(B_i\) gives the received residual

\[
(v_i-\nu_i Z)Q_3.                                  \tag{9}
\]

Every arbitrary exceptional explanation can be written uniquely as

\[
H_0+\gamma H_1+aQ_2+bQ_3.
\]

By (8)--(9), it agrees on **all** of \(B_i\), or on none of it, according as

\[
\boxed{b-s_i a=v_i-\nu_i\gamma}.                   \tag{10}
\]

Let \(T_\gamma\) be the set of block equations (10) satisfied by the slope.
This algebraic set is defined even when a clean block happens to be empty.

### Triplet rigidity

Any three equations (10) have exactly one slope solution: the omitted base
slope. Indeed, their consistency determinant is affine in \(\gamma\). Its
coefficient is the determinant of the three rows \((-s_i,1,-\nu_i)\).
If \(S=\sum_j\gamma_j\) and \(E_2=\sum_{j<k}\gamma_j\gamma_k\), then

\[
\nu_i=s_i^2-Ss_i+E_2.
\]

The coefficient is therefore, up to a nonzero sign, the Vandermonde product
of the three distinct \(s_i\)'s. It cannot vanish. The omitted base slope is
one root, hence the unique root.

Consequently

\[
\#\{\gamma:|T_\gamma|\ge3\}\le4.                  \tag{11}
\]

There is no identity-triplet branch.

## 4. Canonical owner bounds

Assign each exceptional slope by \(|T_\gamma|\), breaking ties
lexicographically. The resulting slope classes are disjoint.

### Two clean blocks: one fixed pair

For \(T_\gamma=\{i,j\}\), the two equations determine affine functions
\(a(\gamma),b(\gamma)\), hence one fixed codeword pair. The common clean
agreement has size \(b_i+b_j\). Since no other clean equation holds, all
additional support coordinates lie in \(Y\).

If \(h=m-b_i-b_j\), the class is empty when \(h>y\). Otherwise let \(u\)
be the number of dirty coordinates on which the fixed pair itself agrees.
Same-support pair noncontainment gives \(u\le h-1\). Every other dirty
coordinate determines at most one finite slope, and each selected slope needs
at least \(h-u\) such coordinates. Hence

\[
N_{ij}\le
\max\{0,b_i+b_j+y-m+1\}.                           \tag{12}
\]

### One clean block: one correction ray

For \(T_\gamma=\{i\}\), equation (10) defines one affine correction ray in
direction \(Q_2+s_iQ_3\), with \(B_i\) as a universal core. After cancelling
that core, the row parameters are

\[
k_i=K-b_i,
\qquad
M_i=m-b_i,
\qquad
N_i=y,
\qquad
\rho_i=N_i-M_i=b_i+y-m.                             \tag{13}
\]

The class is empty when \(\rho_i<0\).

We use the following universal-core-aware ray envelope. For a shortened row
with dimension \(k\), gap \(D\), and outside excess \(\rho<k\), cancel all
further ray-universal coordinates. If the remaining agreement threshold is
\(M\), then \(D+1\le M\le k+D\) and the nonuniversal domain has size
\(M+\rho\).

If a graph clone has weight at least \(k\), the inequality
\(D+\rho<k\) gives total nonuniversal weight below \(2k\), so there is at
most one such graph. Its complement has fewer than \(M\) coordinates; hence
all selected points lie on that graph and there are at most \(\rho+1\) of
them. If no large graph exists, every selected support contributes at least

\[
B_k(M)=
\begin{cases}
M-1,&M\le k-1,\\
(k-1)(M-k+1),&M\ge k
\end{cases}
\]

heterogeneous coordinate pairs. Distinct parameter lines meet at at most one
point. Thus the large-clone and residual alternatives are mutually exclusive,
not additive.

Define the real envelope

\[
\overline{\mathcal R}(k,\rho)=\max\left\{
\rho+1,
\frac{(D+1+\rho)(D+\rho)}{2D},
\frac{(k-1+\rho)(k-2+\rho)}{2(k-2)},
\frac{(k+\rho)(k-1+\rho)}{2(k-1)},
\frac{(k+D+\rho)(k+D-1+\rho)}{2(k-1)(D+1)}
\right\}.                                           \tag{14}
\]

Convexity of the two \(M\)-ranges shows that the four endpoint values in
(14), together with the large-clone alternative, dominate every legal
\(M\). The integer ray count is at most
\(\lfloor\overline{\mathcal R}(k,\rho)\rfloor\).

There are no \(|T_\gamma|=0\) slopes in the range used below: even the full
dirty set has size less than \(m\).

## 5. Three exact regimes

### 5.1 Four-support ray regime: \(\delta<0\)

If \(4r<|X|=m+r\), four omission sets cannot cover \(X\). Thus a genuinely
two-dimensional residual is impossible and the whole exceptional family is
one correction ray. The exact integer version of (14), maximized at
\(M\in\{D+1,K-1,K,K+D\}\), pays this regime.

### 5.2 Clean four-block regime: \(\delta\ge0\), \(\eta:=2r-m<0\)

No one-block owner can reach \(m\) agreements. The symmetric convex function

\[
\sum_{i<j}(y+\delta-r+1-d_i-d_j)_+
\]

is maximized at an endpoint incidence profile. Maximizing also over
\(y\le\delta\) gives

\[
\sum_{i<j}N_{ij}\le\max\{0,2\delta-r+1\}.          \tag{15}
\]

Together with (11),

\[
|Z_{\rm out}|\le4+\max\{0,2\delta-r+1\}.           \tag{16}
\]

### 5.3 Dirty four-block regime: \(\eta\ge0\), \(4\eta<r\)

Here \(m=2r-\eta\) and \(\delta=r+\eta\). For fixed \(y\), the pair-owner
objective is convex on

\[
0\le d_i\le r,
\qquad
\sum_i d_i=y+r+\eta.
\]

Its endpoint profile is

\[
(0,0,y+\eta,r)
\quad(y\le r-\eta),
\]

or

\[
(0,y-r+\eta,r,r)
\quad(y\ge r-\eta).
\]

The resulting bound is nondecreasing in \(y\), so the maximum occurs at
\(y=\delta=r+\eta\), with profile

\[
(d_1,d_2,d_3,d_4)=(0,2\eta,r,r).                    \tag{17}
\]

At (17), the six two-block caps sum to

\[
r+4\eta+5.
\]

Adding the four triplet slopes gives

\[
r+4\eta+9.                                         \tag{18}
\]

A one-block ray is active only when

\[
d_i\le H:=y+\eta-r.
\]

The condition \(4\eta<r\) implies that at most two rays are active. If their
incidences are \(d_1,d_2\), then \(d_1+d_2\ge H\).
For fixed \(K,r,H\), every candidate in (14), under

\[
k=K-r+d,
\qquad
\rho=H-d,
\]

is decreasing and convex in \(d\). Therefore

\[
\mathcal R(d_1)+\mathcal R(d_2)
\le
\left\lfloor
\overline{\mathcal R}(K-r,H)
+
\overline{\mathcal R}(K-r+H,0)
\right\rfloor.                                      \tag{19}
\]

Both endpoint envelopes are nondecreasing in \(H\), and \(H\le2\eta\).
Combining (18)--(19),

\[
\boxed{
|Z_{\rm out}|\le
r+4\eta+9+
\left\lfloor
\overline{\mathcal R}(K-r,2\eta)
+
\overline{\mathcal R}(K-r+2\eta,0)
\right\rfloor.
}                                                     \tag{20}
\]

## 6. Deployed scan and exact boundary

The common-locator floor is reconstructed by exact inversion of the repaired
rank-one capacity at every ambient dimension. Across

\[
662{,}480\le K\le1{,}048{,}576,
\]

the three regimes above give a maximum exceptional cap of

\[
\boxed{1{,}099{,}960},
\]
attained uniquely at \(K=662{,}480\).

At that first cell,

\[
\begin{aligned}
K&=662{,}480,&
\kappa(K)&=75{,}757,&
c&=586{,}723,\\
r&=394{,}381,&
\eta&=58{,}810,&
\delta&=453{,}191.
\end{aligned}
\]

The pair/triplet part is

\[
r+4\eta+9=629{,}630.
\]

The two real ray envelopes are

\[
\overline{\mathcal R}(268{,}099,117{,}620)
=\\frac{24{,}796{,}460{,}207}{89{,}366},
\]

and

\[
\overline{\mathcal R}(385{,}719,0)
=\\frac{385{,}719}{2}.
\]

Their sum has floor \(470{,}330\). Hence

\[
|Z_{\rm out}|\le629{,}630+470{,}330=1{,}099{,}960.
\]

Using (3),

\[
|Z|
\le4{,}070{,}947+1{,}099{,}960
=5{,}170{,}907
<5{,}170{,}912,
\]
with exact slack

\[
\boxed{5}.                                           \tag{21}
\]

Thus a proper rank-two drop is impossible for every

\[
\boxed{K\ge662{,}480}.                               \tag{22}
\]

At each heavy coordinate the only remaining outcome is whole-family
shortening. All \(5{,}170{,}912\) slopes therefore shorten intact through the
complete interval and reach

\[
\boxed{K\le662{,}479}.                               \tag{23}
\]

At the adjacent cell \(K=662{,}479\), the same floor-safe compiler gives

\[
|Z_{\rm out}|\le1{,}099{,}983,
\qquad
A_1+|Z_{\rm out}|\le5{,}170{,}930,
\]
which is above the load by \(18\). This is an exact method wall, not an unsafe
certificate.

## 7. Scope

This theorem pays the complete proper-drop branch for the displayed ambient
interval. It does not pay affine error rank twelve, move an active-v4 ledger
atom, or close KoalaBear.

The strongest next target is the adjacent \(18\)-slope deficit at
\(K=662{,}479\). The extremal relaxed profile has two active one-block rays
and one dominant two-block owner. Any improvement must couple those owners;
an independent per-owner sharpening is unlikely to be sufficient.
