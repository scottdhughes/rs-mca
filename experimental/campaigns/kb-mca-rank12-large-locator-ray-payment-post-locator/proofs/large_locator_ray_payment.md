# Paying the large-locator proper-drop interval in affine error rank twelve

## 1. Exact inherited interface

Work in a shortened KoalaBear row

\[
(n,K,m)=(R+K,K,D+K),
\qquad R=1{,}048{,}576,
\qquad D=67{,}472,
\]

and put

\[
t=n-m=R-D=981{,}104.
\]

The repaired predecessor stack supplies a post-near rank-two explanation
family `Z` of

\[
|Z|=L_2=5{,}170{,}912
\]

distinct finite slopes.  Each slope has one frozen exact size-`m` bad
support, one explanation, and one minimizing pair.  All pair differences lie
in a fixed two-dimensional Reed--Solomon direction code `C'`.

The exact parent at
`ed556ccb7527e1c54e58b8d151ccefd8539000ac` proves the following
source-bound statement.  If a heavy complete-core coordinate gives a proper
rank-two drop at ambient dimension `K`, the resulting rank-at-most-one leaf
has a full common pair-core locator of degree at least

\[
c_{\min}(K)=K-\kappa(K),
\]

where `kappa(K)` is obtained by exact inversion of the all-dimension rank-one
capacity.  The floor is nondecreasing.  In particular,

\[
c_{\min}(858{,}618)=806{,}341,
\qquad
c_{\min}(858{,}619)=806{,}342.                    \tag{1}
\]

The repaired rank-one theorem also gives the dimension-uniform bound

\[
\boxed{A_1=4{,}070{,}947}.                         \tag{2}
\]

A crucial scope point is that (2), rather than the smaller capacity at
`kappa(K)`, must be used for an actual common core larger than the minimum:
a larger core lowers the effective dimension, and the rank-one capacity may
increase.  The proof below keeps that variable and uses the global maximum.

Before a proper drop is selected, repeatedly shorten every coordinate in the
complete minimizing-pair core of the whole rank-two family.  Hence no
remaining coordinate is a whole-family pair core.

## 2. One rank-one family and one exceptional family

Let a proper drop occur, and let `C` be the **actual full common pair core**
of the resulting rank-one leaf.  Write

\[
c=|C|,
\qquad W\le C',
\qquad \dim W=1.
\]

Every polynomial in `W` vanishes on `C`.  Since the whole-family pair core
has already been exhausted, evaluation on `C'` is nonzero at every
`x in C`; therefore

\[
\ker(\operatorname{ev}_x|_{C'})=W
\qquad(x\in C).                                    \tag{3}
\]

Fix one minimizing pair `e_0=(a_0,b_0)` in the leaf.  For an arbitrary
selected slope `gamma`, with minimizing pair
`e_gamma=(a_gamma,b_gamma)`, put

\[
p_\gamma=(a_\gamma-a_0)+\gamma(b_\gamma-b_0)\in C'. \tag{4}
\]

Translate the received pair by `e_0`.  This preserves each finite slope,
selected support, scalar agreement, and same-support pair noncontainment.

Partition the slopes by their already-frozen exact supports:

\[
Z=Z_{\rm in}\sqcup Z_{\rm out},
\]

where `Z_in` consists of supports meeting `C`, and `Z_out` consists of
supports avoiding `C`.

If `S_gamma` meets `C` at `x`, then the translated received scalar word and
`p_gamma` both vanish at `x`.  Equation (3) gives

\[
p_\gamma\in W.
\]

Thus `Z_in` is one rank-one explanation family, and by (2)

\[
\boxed{|Z_{\rm in}|\le4{,}070{,}947}.              \tag{5}
\]

No dimension-specific capacity at the minimum locator floor is used.

## 3. Six-support synchronization of the exceptional family

If `c>t`, the complement of `C` has fewer than `m` coordinates, so
`Z_out` is empty.  Assume `c<=t` and put

\[
r=t-c.
\]

Let

\[
X=D_K\setminus C,
\qquad |X|=n-c=m+r.
\]

Each support in `Z_out` is an `m`-subset of `X`; write its omitted `r`-set
as `E_gamma=X\setminus S_gamma`.

For three distinct slopes define their second divided difference

\[
q_{\alpha\beta\gamma}
=[p_\alpha,p_\beta,p_\gamma]\in C'.                \tag{6}
\]

At a coordinate in all three supports, the values in (4) equal the translated
received scalar word and are affine in the slope.  Therefore

\[
\operatorname{supp}(q_{\alpha\beta\gamma})\cap X
\subseteq E_\alpha\cup E_\beta\cup E_\gamma.       \tag{7}
\]

Suppose

\[
6r<R+1.                                             \tag{8}
\]

A nonzero second difference in `W` would vanish on `C` and, by (7), have
weight at most `3r<R+1`, contradicting the Reed--Solomon minimum weight

\[
n-K+1=R+1=1{,}048{,}577.
\]

For two nonzero second differences, choose a scalar making their difference
lie in the one-dimensional space `W`.  That difference vanishes on `C` and
is supported in at most six omission sets, hence has weight at most `6r`.
By (8) it is zero.  Consequently all nonzero second divided differences are
proportional to one nonzero `Q in C'`.

Interpolating two reference explanations gives a codeword pair
`H_0,H_1 in C'` such that every exceptional explanation has the form

\[
\boxed{
 p_\gamma=H_0+\gamma H_1+c_\gamma Q.
}                                                     \tag{9}
\]

If fewer than three exceptional slopes occur, (9) follows directly.  Thus
`Z_out` is one correction ray whose base is affine in the slope.

The largest integer satisfying (8) is

\[
r_{\max}=\left\lfloor\frac R6\right\rfloor
=174{,}762,
\]

because

\[
6r_{\max}=1{,}048{,}572<R+1,
\qquad
6(r_{\max}+1)=R+2.                                  \tag{10}
\]

By (1), every proper drop at `K>=858,619` lies in this range.

## 4. Universal-core-aware payment of the affine correction ray

Translate (9) by the fixed codeword pair `(H_0,H_1)`.  The parameter point
attached to a slope is now `(gamma,c_gamma)`, and its explanation is
`c_gamma Q`.

Only coordinates in `X` can occur in the frozen exceptional supports.  Let
`U` be the set of coordinates in `X` at which both the translated received
pair and `Q` vanish.  These coordinates agree for every parameter pair.  Put

\[
u=|U|,
\qquad M=m-u,
\qquad N=|X|-u=M+r.                                  \tag{11}
\]

Since `Q` is nonzero of degree `<K`,

\[
0\le u\le K-1,
\qquad D+1\le M\le K+D.                             \tag{12}
\]

Every selected support contains at least `M` nonuniversal coordinate copies.

### 4.1 Parameter-line arrangement

For `Q(x)\ne0`, agreement is the graph line

\[
c=f_x(\gamma)
:=\frac{r'_0(x)+\gamma r'_1(x)}{Q(x)}.
\]

The function `f_x` is affine in `gamma`.  Coordinates with the same `f_x`
form one graph clone class.  For `Q(x)=0` but `x\notin U`, agreement occurs
on one vertical parameter line.  The total weight of all vertical
coordinates is at most `K-1-u`.

Every graph clone class is itself a global affine codeword-pair block:
if `f(\gamma)=a+b\gamma`, then adding back `(H_0,H_1)` gives the pair

\[
(H_0+aQ,\ H_1+bQ).
\]

A selected support must use at least two nonuniversal parameter-line classes.
Indeed, all zeros of `Q` together have fewer than `m` coordinates, so a graph
coordinate is necessary; and universal coordinates together with one graph
clone class are simultaneously explained by the displayed codeword pair.

### 4.2 At most one large clone line

In the range (10),

\[
N\le m+r=K+D+r<2K,                                  \tag{13}
\]

because `D+r<=242,234<K`.  Hence at most one graph clone class has weight at
least `K`.

Assign every selected parameter point lying on that large graph to it.  If
its weight is `w`, its complete scalar agreement domain must use at least

\[
\max\{1,M-w\}
\]

nonuniversal coordinates outside the clone class: the `1` is forced by
same-support pair noncontainment.  Along one graph, an outside coordinate can
serve at most one parameter point.  Thus the number assigned to the large
clone is at most

\[
\left\lfloor
\frac{N-w}{\max\{1,M-w\}}
\right\rfloor
\le r+1.                                             \tag{14}
\]

### 4.3 Heterogeneous-pair charge for the residual points

After removing the large-graph points, every parameter-line class meeting a
residual support has weight at most `K-1`.  A residual exact support contains
at least `M` nonuniversal copies and at least two classes.

The minimum number of unordered coordinate pairs drawn from distinct classes
is

\[
B_K(M)=
\begin{cases}
M-1,&M\le K-1,\\[1mm]
(K-1)(M-K+1),&M\ge K.
\end{cases}                                         \tag{15}
\]

For `M<=K-1`, the extremal composition is `(M-1,1)`.  For `M>=K`, note that
`M<2(K-1)` throughout this window; the extremal composition is
`(K-1,M-K+1)`.  The bound is nondecreasing if more than `M` nonuniversal
copies are present.

Two distinct affine parameter lines meet in at most one parameter point.
Therefore a heterogeneous coordinate pair can be charged by at most one
selected slope, and the residual contribution is bounded by

\[
\left\lfloor
\frac{\binom{M+r}{2}}{B_K(M)}
\right\rfloor.                                      \tag{16}
\]

Combining (14)--(16),

\[
|Z_{\rm out}|
\le r+1+
\max_{D+1\le M\le K+D}
\left\lfloor
\frac{\binom{M+r}{2}}{B_K(M)}
\right\rfloor.                                      \tag{17}
\]

### 4.4 Four-endpoint optimization

On `D+1<=M<=K-1`, put `x=M-1`.  Before the floor, the quotient in (17) is

\[
\frac{(x+r+1)(x+r)}{2x},
\]

whose second derivative is

\[
\frac{r(r+1)}{x^3}\ge0.
\]

On `K<=M<=K+D`, put `y=M-K+1`.  The quotient is

\[
\frac{(K-1+r+y)(K-2+r+y)}{2(K-1)y},
\]

with second derivative

\[
\frac{(K+r-2)(K+r-1)}{(K-1)y^3}>0.
\]

Hence the exact maximum after the floor occurs among only

\[
M\in\{D+1,K-1,K,K+D\}.                              \tag{18}
\]

The exact scan over every parent locator-floor cell
`858,619<=K<=1,048,576` gives

\[
\boxed{|Z_{\rm out}|\le796{,}620}.                  \tag{19}
\]

The maximum is unique at `K=858,619`, at the minimum parent locator floor
`c=806,342`, with `r=174,762` and endpoint `M=K`.  If the actual common core
is larger, `r` is smaller; every expression in (17) is nondecreasing in `r`,
so (19) remains valid.

At the first cell the four exact endpoint values are

```text
M=D+1      609,591
M=K-1      796,619
M=K        796,620
M=K+D      174,773
```

## 5. Elimination of the complete large-locator interval

The support partition is disjoint in original slope units.  Equations (5)
and (19) therefore give, for every proper rank-two drop at
`K>=858,619`,

\[
|Z|
\le4{,}070{,}947+796{,}620
=4{,}867{,}567
<5{,}170{,}912.                                      \tag{20}
\]

The exact contradiction slack is

\[
\boxed{303{,}345}.                                  \tag{21}
\]

Thus a proper drop is impossible throughout all

\[
858{,}619\le K\le1{,}048{,}576.
\]

At each heavy coordinate the only remaining outcome is a whole-family pair
core, so all `5,170,912` slopes shorten together through the complete top
interval and reach

\[
\boxed{K\le858{,}618}.                              \tag{22}
\]

At the adjacent cell `K=858,618`, the parent floor is only `806,341`, so
`r=174,763` and the six-omission support bound is

\[
6r=1{,}048{,}578=R+2,
\]

one coordinate above the Reed--Solomon minimum weight.  This is the exact
wall of the synchronization argument, not an unsafe certificate.

## 6. Scope and next theorem

This is a direct payment of the **proper-drop branch** in the displayed top
ambient interval.  It does not pay affine error rank twelve, move an active-v4
ledger atom, or close KoalaBear.

The next exact joint is the adjacent near-minimum-weight cell at `K=858,618`.
A nonzero difference of two second divided differences can then lie in `W`
with weight `R+1` or `R+2`.  The strongest successor is to classify that
near-MDS obstruction using its six omission sets and the full source-bound
common core.  Either it synchronizes to one ray after all, or its
`K-1`/`K-2` zero set yields a new named locator owner.
