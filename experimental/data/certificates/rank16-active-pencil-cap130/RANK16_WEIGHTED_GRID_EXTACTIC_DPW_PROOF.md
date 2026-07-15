# Rank-16 fixed-pair weighted-grid theorem

## Theorem

Let

\[
p=2{,}130{,}706{,}433,
\quad N=1{,}053{,}693,
\quad a=72{,}588,
\quad h=5{,}116.
\]

Fix a source-valid rank-16 saturated endpoint pair and one active pencil.  For
an integer core size \(0\le c\le553\), put

\[
d=h-c=5{,}116-c,
\qquad b=a-2h+c=62{,}356+c,
\qquad U=N-(2a-h)=913{,}633.
\]

Assume the frozen fixed-pair source facts: common neighbors form the simple
row--column grid, the exact endpoint budgets hold, complete actual tails on a
common row or column are disjoint, other pair intersections have size at most
\(d\), every tail coordinate is an affine parameter line, and all coordinate
copies in one primitive direction have total multiplicity at most \(d\).
Then the active-pencil occupancy is at most \(155\).

The proof is over the literal field \(\mathbf F_p\).  It uses no
Hirzebruch/BMY inequality and no characteristic-zero transfer.

## 1. Source-owned actual tails

Suppose, for contradiction, that the pencil contains at least 156 common
neighbors, and select any set \(S\) of exactly 156 of them.  Let \(P_0,P_1\)
be the endpoints.

The frozen saturation argument is about complete actual agreement sets, not
chosen representatives.  Every saturated endpoint--neighbor difference has
exactly \(h\) residual roots; the frozen selected-support intersection already
has size \(h\), so all those roots are actual received-word agreements.  If
\(A(P)\) is the complete residual agreement set of a neighbor \(P\), its two
endpoint blocks have size \(d\), meet in the common plane core of size \(c\),
and

\[
T_P:=A(P)\setminus(A(P_0)\cup A(P_1))
\]

satisfies

\[
|T_P|\ge a-2h+c=b.                                      \tag{1}
\]

The union of all selected tails is contained in the complement of the two
complete endpoint agreement sets.  Since those endpoint sets each have size
at least \(a\) and meet in exactly \(h\) coordinates,

\[
M:=\left|\bigcup_{P\in S}T_P\right|
 \le N-(2a-h)=U.                                         \tag{2}
\]

Thus

\[
\sum_{P\in S}|T_P|\ge156b.                              \tag{3}
\]

No support reselection appears in (1)--(3).

Let \(r,t\) be the numbers of occupied rows and columns of \(S\).  The exact
endpoint budget gives

\[
r,t\le R(c):=\left\lfloor\frac{72{,}588-c}{5{,}116-c}\right\rfloor-1.
                                                                    \tag{4}
\]

For the present range,

\[
R(c)=13\quad(0\le c\le296),
\qquad
R(c)=14\quad(297\le c\le553).                            \tag{5}
\]

Rows and columns meet in at most one point, so the grid graph is simple.  Its
row and column degrees are at most 14.  Since it contains the 156 selected
points, the only possible ordered pairs \((r,t)\) are

\[
(12,13),(12,14),(13,12),(13,13),(13,14),
(14,12),(14,13),(14,14),                                \tag{6}
\]

subject, of course, to \(r,t\le R(c)\).

A tail-coordinate line contains neither endpoint.  Hence it cannot equal a
row, a column, or the fixed endpoint line.  It meets each row and each column
at most once, and therefore contains at most

\[
s:=\min(r,t)                                             \tag{7}
\]

selected neighbors.

## 2. Balanced direction coloring

Projectively take the fixed endpoint line as the line at infinity.  Then a
primitive transverse direction is exactly the intersection point of its lines
with that fixed line.  For every such direction \(\nu\), let \(X_\nu\) be
the set of coordinate copies in that direction.  The source direction-fiber
bound is

\[
|X_\nu|\le d.                                            \tag{8}
\]

Color all \(M\) copies with colors \(1,\ldots,d\), injectively on every
\(X_\nu\), and with total color loads differing by at most one.  This coloring
exists by the following greedy rule.  Process the direction classes in any
order and assign the copies of the next class to distinct currently
least-loaded colors.  If the loads before a step are \(q\) and \(q+1\), then
either only some \(q\)-loads are raised, or every \(q\)-load is raised and
some \(q+1\)-loads are raised.  The new loads again differ by at most one.

Write \(e_j\) for the load of color \(j\).  From (2),

\[
e_j\le E(c):=\left\lceil\frac{U}{d}\right\rceil.         \tag{9}
\]

For \(0\le c\le553\),

\[
179\le E(c)\le201.                                       \tag{10}
\]

In one color no geometric line is repeated: two copies of the same line have
the same primitive direction and therefore receive different colors.  Thus a
color gives a reduced transverse line arrangement.  In fact it contains at
most one transverse line of each direction.

## 3. Exact Tjurina ledger in one color

Fix a color, suppress its index, and let its \(e\) transverse lines be joined
to the \(r\) endpoint-row lines, the \(t\) endpoint-column lines, and the fixed
endpoint line.  The resulting reduced projective arrangement has degree

\[
D=e+r+t+1\le201+14+14+1=230<p.                            \tag{11}
\]

Base extension from \(\mathbf F_p\) to its algebraic closure preserves all
lines and incidences, so work over that algebraic closure.

Let \(k_P\) be the number of this color's transverse lines through
\(P\in S\), and put

\[
I:=\sum_{P\in S}k_P.                                     \tag{12}
\]

For any reduced degree-\(D\) line arrangement, if \(m_x\) is the
multiplicity of a singular point, then

\[
\sum_x\binom{m_x}{2}=\binom D2.
\]

Because every \(m_x<D<p\), an ordinary \(m_x\)-fold point has local Tjurina
length \((m_x-1)^2\).  Therefore

\[
\tau=\binom D2+\sum_x\binom{m_x-1}{2}.                   \tag{13}
\]

At the two endpoints the multiplicities are \(r+1\) and \(t+1\).  At a
selected neighbor \(P\), the multiplicity is \(k_P+2\).  Dropping all other
nonnegative terms from (13) gives the exact lower ledger

\[
\tau\ge
 \binom D2+\binom r2+\binom t2
 +\sum_{P\in S}\binom{k_P+1}{2}.                         \tag{14}
\]

For fixed total \(I\), discrete convexity minimizes the last sum by balancing
the 156 integers \(k_P\).  If

\[
I=156q+u,\qquad 0\le u<156,
\]

then

\[
F(I):=(156-u)\binom{q+1}{2}+u\binom{q+2}{2}
 \le\sum_{P\in S}\binom{k_P+1}{2}.                      \tag{15}
\]

Also, by (7),

\[
I\le se.                                                  \tag{16}
\]

## 4. Characteristic-valid du Plessis--Wall bound

Let \(f\) define any reduced degree-\(D\) plane curve over an algebraically
closed field with characteristic not dividing \(D\).  Let \(\rho=\operatorname{mdr}(f)\)
be the least degree of a nonzero homogeneous relation among
\(f_x,f_y,f_z\), and let \(\tau\) be the gradient-scheme length.  Then

\[
\tau\le (D-1)(D-\rho-1)+\rho^2,                           \tag{17}
\]

and, for \(\alpha=2\rho+1-D>0\),

\[
\tau\le (D-1)(D-\rho-1)+\rho^2-\binom{\alpha+1}{2}.       \tag{18}
\]

Here is the characteristic-valid proof.  The gradient sequence is

\[
0\longrightarrow \mathcal E\longrightarrow\mathcal O^3
 \longrightarrow\mathcal I_\Sigma(D-1)\longrightarrow0,
\]

with

\[
c_1(\mathcal E)=1-D,
\qquad c_2(\mathcal E)=(D-1)^2-\tau.
\]

A minimal degree-\(\rho\) syzygy is a section of \(\mathcal E(\rho)\).  Its
coefficients have no common polynomial divisor, since division would give a
smaller syzygy, so its zero scheme \(Z\) is zero-dimensional and

\[
0\longrightarrow\mathcal O\longrightarrow\mathcal E(\rho)
 \longrightarrow\mathcal I_Z(2\rho+1-D)\longrightarrow0.
\]

Consequently

\[
\operatorname{length}Z
 =(D-1)(D-\rho-1)+\rho^2-\tau.                             \tag{19}
\]

Nonnegativity gives (17).  If \(\alpha>0\), minimality gives
\(H^0(\mathcal E(\rho-1))=0\).  Twisting the last sequence down once gives
\(H^0(\mathcal I_Z(\alpha-1))=0\), so restriction of degree-\(\alpha-1\)
forms to \(Z\) is injective.  Hence

\[
\operatorname{length}Z\ge h^0(\mathcal O(\alpha-1))
 =\binom{\alpha+1}{2},
\]

which gives (18).  This uses no characteristic-zero theorem.  In our
arrangements, (11) ensures that all required degrees are invertible.

Write the right side of (17)--(18), with the correction when applicable, as
\(\operatorname{DPW}(D,\rho)\).  Combining (14)--(15) gives

\[
F(I)\le \operatorname{DPW}(D,\rho)
 -\binom D2-\binom r2-\binom t2.                          \tag{20}
\]

The low-\(\rho\) branch of (20) alone is too weak; the following forcing lemma
is the load-bearing additional input.

## 5. Divisorial stripping

A degree-\(\rho\) Jacobian syzygy defines a projective vector field, a section
of \(T_{\mathbf P^2}(\rho-1)\), tangent to every arrangement line.  Let the
divisorial zero of this section have total degree \(z\), and suppose exactly
\(h_0\) distinct arrangement lines occur among its components.

Divide by the full zero divisor.  The resulting section has degree
\(\rho-z\), has only isolated zeros, and remains tangent to the arrangement
with those \(h_0\) lines deleted.  If \(\rho'\) is the mdr of the remaining
product, subtracting the cofactor divided by its invertible degree times the
Euler field gives

\[
\rho'\le\rho-z.                                           \tag{21}
\]

Conversely, multiply a minimal logarithmic field for the remaining arrangement
by the product of the \(h_0\) deleted line equations and again use the Euler
field to obtain a full Jacobian syzygy.  Thus

\[
\rho\le\rho'+h_0.                                        \tag{22}
\]

Since \(z\ge h_0\), (21)--(22) force

\[
z=h_0,
\qquad \rho'=\rho-h_0.                                   \tag{23}
\]

Thus the divisor is a reduced union of arrangement lines only.  After
stripping it, put

\[
q=\rho-h_0.                                               \tag{24}
\]

The remaining field is a section of \(T_{\mathbf P^2}(q-1)\) with isolated
zeros and is tangent to exactly \(D-h_0\) remaining arrangement lines.

## 6. Positive-characteristic extactic pencil lemma

**Lemma.**  Let \(K\) be algebraically closed of characteristic \(p\), let
\(0\le q<p\), and let a nonzero section of
\(T_{\mathbf P^2}(q-1)\) have isolated zeros.  If it is tangent to more than
\(3q\) distinct projective lines, all those lines form one pencil.

**Proof.**  Choose one invariant line as the line at infinity.  Tangency to
that line lets the affine field be represented as

\[
\delta=P(x,y)\partial_x+Q(x,y)\partial_y,
\qquad \deg P,\deg Q\le q.                                \tag{25}
\]

The isolated-zero hypothesis gives \(\gcd(P,Q)=1\).  If \(q=0\), then
\(P,Q\) are constant and every invariant line is parallel to their constant
direction, so the conclusion holds.  Assume \(q\ge1\), and define the first
line extactic polynomial

\[
\mathcal X=P\,\delta(Q)-Q\,\delta(P).                     \tag{26}
\]

It has degree at most \(3q-1\).  Every invariant affine line divides
\(\mathcal X\): modulo such a line, \(\delta\) is a scalar multiple of its
constant tangent direction, and because the line ideal is \(\delta\)-stable,
(26) vanishes modulo that ideal.  More than \(3q\) invariant projective lines
give more than \(3q-1\) affine invariant lines, so

\[
\mathcal X=0.                                             \tag{27}
\]

If \(Q/P\) is constant, coprimality makes \(P,Q\) constant and all invariant
lines are parallel, a pencil centered at infinity.  Otherwise put
\(R=Q/P\).  Equation (27) is \(\delta R=0\).

Let \(\lambda\) be transcendental over \(K\) and
\(G_\lambda=Q-\lambda P\).  From (27),

\[
P\,\delta(G_\lambda)=G_\lambda\,\delta(P).
\]

Since \(\gcd(P,G_\lambda)=1\), this gives
\(G_\lambda\mid\delta(G_\lambda)\).  Factor over an algebraic closure of
\(K(\lambda)\) as

\[
G_\lambda=\prod_i g_i^{m_i}.
\]

Every multiplicity satisfies \(1\le m_i\le\deg G_\lambda\le q<p\), so
\(m_i\ne0\) in \(K\).  Taking the \(g_i\)-adic valuation in
\(G_\lambda\mid\delta(G_\lambda)\) shows that
\(g_i\mid\delta(g_i)\): otherwise differentiating
\(g_i^{m_i}\) would have exact \(g_i\)-valuation \(m_i-1\).  Modulo
\(g_i\), one has \(Q=\lambda P\), and
\(\gcd(P,g_i)=1\), whence

\[
g_i\mid(\partial_x+\lambda\partial_y)g_i.                \tag{28}
\]

The derivative in (28) has smaller degree unless it is zero.  In coordinates
\(u=x\), \(v=y-\lambda x\), the operator is \(\partial_u\).  Its kernel in
characteristic \(p\) is \(K(\lambda)[u^p,v]\); since
\(\deg g_i\le q<p\), (28) forces
\(g_i\in K(\lambda)[v]\), and over the algebraic closure an irreducible such
\(g_i\) is linear.  Thus every component of a generic fiber is an affine line.

These generic component lines form an algebraic curve \(C\) in the dual
projective plane.  Through a general point of the original plane there is
exactly one such line: the point has one value of the first integral and lies
on one component of its support.  A general point \(x\) corresponds to
a dual line \(x^*\); by Bezout, the number of members of \(C\) through \(x\)
is \(\deg C\).  Hence \(\deg C=1\).  A line in the dual plane is precisely a
pencil of primal lines.  Finally, at a general point of any exceptional
invariant line, its tangent direction must equal the unique generic pencil
leaf direction, so that line also belongs to the same pencil.  This proves the
lemma. \(\square\)

## 7. The near-pencil incidence cap

Return to one color arrangement of degree \(D\) and mdr \(\rho\).  If

\[
3\rho<D,                                                  \tag{29}
\]

strip the \(h_0\) divisorial lines.  By (23)--(24), the remaining line count
and field degree obey

\[
(D-h_0)-3q=D-3\rho+2h_0>0.
\]

The extactic lemma makes all remaining lines a pencil.

Its center cannot lie on the fixed endpoint line.  At the first endpoint at
most \(r+1\le15\) arrangement lines occur; at the second at most
\(t+1\le15\); at any other point of the fixed line there are only the fixed
line and at most one transverse line, because a color has at most one line in
one primitive direction.  On the other hand, (29), \(h_0\le\rho\), and
\(D\ge12+13+1=26\) give

\[
D-h_0\ge D-\rho\ge18.
\]

Thus the pencil center is affine.  At an affine point at most one row line and
one column line pass, while the fixed endpoint line does not.  Therefore

\[
h_0\ge r+t-1,
\qquad \rho\ge r+t-1.                                    \tag{30}
\]

Let \(m\) be the number of surviving transverse lines in the pencil.  At most
two skeleton lines survive, so

\[
m\ge D-h_0-2=e-h_0+r+t-1
 \ge e-\rho+r+t-1.                                       \tag{31}
\]

The \(m\) pencil transverses have at most \(m+155\) incidences with \(S\): if
the center is selected, they contribute \(m\) copies of the center and at
most one copy of every other selected point; if it is not selected, each of
the 156 points lies on at most one pencil member.  Each of the remaining
\(e-m\) transverses has at most \(s\) selected points.  Hence

\[
\begin{aligned}
I&\le m+155+s(e-m)\\
 &\le e+155+(s-1)(\rho-r-t+1).                            \tag{32}
\end{aligned}
\]

Thus, for every possible mdr \(\rho\), (16), (20), and, on the branch
\(3\rho<D\), (30)--(32), give a finite exact upper bound for \(I\).

## 8. Exact finite profile functional

For integers \(e,r,t\), let \(D=e+r+t+1\), \(s=\min(r,t)\), and for each
\(0\le\rho<D\) let \(J(e,r,t,\rho)\) be the largest integer \(I\) satisfying

\[
0\le I\le se,                                             \tag{33}
\]

\[
F(I)\le \operatorname{DPW}(D,\rho)
      -\binom D2-\binom r2-\binom t2,                     \tag{34}
\]

and, if \(3\rho<D\), also

\[
\rho\ge r+t-1,
\qquad
I\le e+155+(s-1)(\rho-r-t+1).                            \tag{35}
\]

Define

\[
\Phi(E;r,t)=
 \max_{0\le e\le E}\max_{0\le\rho<e+r+t+1}J(e,r,t,\rho).\tag{36}
\]

Every color has \(I_j\le\Phi(E(c);r,t)\).  Therefore (3) and the \(d\)-color
partition would require

\[
156b\le\sum_{j=1}^d I_j
       \le d\,\Phi(E(c);r,t).                             \tag{37}
\]

The attached dependency-free integer scan evaluates (36) for every
\(c=0,\ldots,553\), every pair (6) allowed by (5), every
\(0\le e\le E(c)\), and every integer mdr \(0\le\rho<D\).  It proves the
strict reverse inequality in every row.

The smallest margin occurs at

\[
c=12,
\quad d=5104,
\quad b=62368,
\quad R=13,
\quad E=180,
\quad r=t=13.
\]

The worst color profile has \(e=180,D=207,\rho=69\).  Its DPW upper bound is

\[
(206)(137)+69^2=32983,
\]

while the fixed part of (14) is

\[
\binom{207}{2}+2\binom{13}{2}=21477.
\]

The residual budget is 11506, and

\[
F(1816)=11496\le11506<11508=F(1817).
\]

Hence \(\Phi=1816\), and

\[
\begin{aligned}
156b&=156\cdot62368=9{,}729{,}408,\\
d\Phi&=5104\cdot1816=9{,}268{,}864,\\
156b-d\Phi&=460{,}544>0.                                 \tag{38}
\end{aligned}
\]

This is the minimum over the complete scan.  Equation (37) is impossible.
Therefore the selected set of 156 neighbors cannot exist, and the active
pencil has occupancy at most 155 for every \(0\le c\le553\).

## 9. Exact `c=553/554` boundary

At \(c=553\),

\[
d=4563,
\quad b=62909,
\quad E=\left\lceil\frac{913633}{4563}\right\rceil=201.
\]

The worst profile is \(r=t=14,e=201,D=230,\rho=77\).  Here

\[
\operatorname{DPW}(230,77)=40737,
\]

\[
\binom{230}{2}+2\binom{14}{2}=26517,
\]

and the residual budget is 14220.  Since

\[
F(2029)=14210\le14220<14224=F(2030),
\]

one has \(\Phi=2029\), and

\[
\begin{aligned}
156b&=9{,}813{,}804,\\
d\Phi&=4563\cdot2029=9{,}258{,}327,\\
156b-d\Phi&=555{,}477.                                   \tag{39}
\end{aligned}
\]

For comparison, the frozen direction-pair relaxation has

\[
\begin{array}{c|r|r|r}
 c&\text{need}&\text{old capacity}&\text{capacity}-\text{need}\\ \hline
553&9{,}813{,}804&9{,}814{,}582&+778\\
554&9{,}813{,}960&9{,}813{,}232&-728.
\end{array}                                               \tag{40}
\]

The new argument also gives, consistently on the adjacent row \(c=554\),

\[
9{,}813{,}960-4562\cdot2029
 =9{,}813{,}960-9{,}256{,}298
 =557{,}662.                                               \tag{41}
\]

Thus there is no gap at the frozen \(553/554\) interface.

## 10. Audit ledger

1. **Actual agreement ownership.**  The proof uses complete actual tails
   \(T_P\), not arbitrarily chosen size-\(m\) supports.  Equations (1)--(3)
   survive every support choice.
2. **Positive characteristic.**  Every color arrangement has degree at most
   230, so all Euler divisions are valid in characteristic
   \(p=2{,}130{,}706{,}433\).  DPW is proved by vector bundles, and the
   extactic proof explicitly uses only \(q<p\).  No BMY/Hirzebruch transfer is
   used.
3. **Line repetitions.**  Same-direction copies get distinct colors; a
   geometric line has a unique direction.  Therefore each color is reduced.
   Tail lines avoid both endpoints and cannot equal a skeleton line.
4. **Direction coloring.**  The greedy least-load construction is injective
   in every direction class and produces loads differing by at most one.  No
   fictitious generic line is added.
5. **Load-bearing forcing.**  If the extactic/divisorial clause is deleted,
   the \(c=553,r=t=14,E=201\) color relaxation rises from 2029 to 2766 and
   gives total capacity 12,621,258, above the required 9,813,804.  The new
   forcing is therefore essential, not cosmetic.
6. **Finite verification.**  The primary Python replay uses only the standard
   library and exact integers.  Normal and optimized (`python -O`) runs are
   byte-identical.  An independent standard-library Ruby implementation
   reproduces the minimum and the \(c=553\) row.

Primary scan ledger SHA-256:

```text
683ac4da362766bf3d763845f7858723422f94e7e9fbceeda434f61dcd269135
```

Primary output:

```text
RANK16_WEIGHTED_GRID_EXTACTIC_DPW: PASS
field_p=2130706433 selected=156 cores=0..553
tail_universe=913633 max_balanced_color_lines=201
feasible_grid_pairs=[(12, 13), (12, 14), (13, 12), (13, 13), (13, 14), (14, 12), (14, 13), (14, 14)]
uniform_min=c12,d5104,b62368,R13,E180,color_cap1816,need9729408,total_cap9268864,margin460544
uniform_min_profile=(13, 13, (180, (69, 'DPW', 207, 32983, 21477, 11506, 1816, None)))
c553_new=need9813804,total_cap9258327,margin555477,profile(14, 14, (201, (77, 'DPW', 230, 40737, 26517, 14220, 2029, None)))
c553_old=need9813804,cap9814582,cap_minus_need778
c554_old=need9813960,cap9813232,cap_minus_need-728
c554_new_consistency=need9813960,total_cap9256298,margin557662
tamper_without_extactic=c553_color_cap2766,total_cap12621258,need9813804,closure=false
scan_sha256=683ac4da362766bf3d763845f7858723422f94e7e9fbceeda434f61dcd269135
```
