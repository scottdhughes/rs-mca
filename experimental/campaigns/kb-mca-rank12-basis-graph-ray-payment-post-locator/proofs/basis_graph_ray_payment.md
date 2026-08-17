# Basis-graph synchronization and payment of the rank-twelve large-locator interval

## 1. Inherited source-bound interface

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
family \(Z\) of

\[
|Z|=L_2=5{,}170{,}912
\]

distinct finite slopes. Each slope has one frozen exact size-\(m\) bad
support, one explanation, and one minimizing pair. All minimizing-pair
differences lie in one fixed two-dimensional Reed--Solomon direction code
\(C'\).

The exact parent at
`ed556ccb7527e1c54e58b8d151ccefd8539000ac` proves the following. If a
heavy complete-core coordinate gives a proper rank-two drop at ambient
\(K\), the resulting rank-at-most-one leaf has an **actual full common pair
core** \(C\) of degree

\[
c=|C|\ge c_{\min}(K)=K-\kappa(K),
\]

where \(\kappa(K)\) is obtained by exact inversion of the all-dimension
rank-one capacity. The floor is nondecreasing. In particular,

\[
c_{\min}(778{,}969)=718{,}959,
\qquad
c_{\min}(778{,}970)=718{,}960.               \tag{1}
\]

The repaired rank-one theorem gives the dimension-uniform cap

\[
\boxed{A_1=4{,}070{,}947}.                    \tag{2}
\]

Before selecting a proper drop, shorten every coordinate in the complete
pair core of the whole rank-two family. Thus no remaining coordinate is a
whole-family pair-core coordinate.

## 2. A chronology-disjoint support partition

Let a proper drop occur. Let

\[
W\le C',\qquad \dim W=1,
\]

be the direction space of the rank-one leaf, and let \(C\) be its actual
full common pair core. Every polynomial in \(W\) vanishes on \(C\). Because
whole-family pair-core coordinates have already been exhausted, evaluation
on \(C'\) is nonzero at every \(x\in C\). Hence

\[
\ker(\operatorname{ev}_x|_{C'})=W
\qquad(x\in C).                                  \tag{3}
\]

Fix one minimizing pair \(e_0=(a_0,b_0)\) in the leaf. For every selected
slope \(\gamma\), with minimizing pair
\(e_\gamma=(a_\gamma,b_\gamma)\), define

\[
p_\gamma=(a_\gamma-a_0)+\gamma(b_\gamma-b_0)\in C'. \tag{4}
\]

Translate the received pair by \(e_0\). This preserves each finite slope,
frozen support, scalar agreement, and same-support pair noncontainment.

Partition the original slopes using their frozen supports:

\[
Z=Z_{\mathrm{in}}\sqcup Z_{\mathrm{out}},
\]

where \(Z_{\mathrm{in}}\) consists of supports meeting \(C\), and
\(Z_{\mathrm{out}}\) consists of supports avoiding \(C\).

If \(S_\gamma\cap C\ne\varnothing\), then at a point of that intersection
the translated received scalar word and \(p_\gamma\) both vanish. By (3),
\(p_\gamma\in W\). Therefore \(Z_{\mathrm{in}}\) is one rank-one family,
and (2) gives

\[
\boxed{|Z_{\mathrm{in}}|\le4{,}070{,}947}.       \tag{5}
\]

This is a partition in original slope units, not a sum over overlapping
proper-drop leaves.

## 3. Omission sets and vector divided differences

If \(c>t\), the complement of \(C\) contains fewer than \(m\) coordinates,
so \(Z_{\mathrm{out}}=\varnothing\). Assume \(c\le t\), put

\[
r=t-c,
\qquad
X=D_K\setminus C,
\qquad |X|=n-c=m+r,
\]

and write every frozen support in \(Z_{\mathrm{out}}\) as

\[
S_\gamma=X\setminus E_\gamma,
\qquad |E_\gamma|=r.                              \tag{6}
\]

For three distinct slopes \(\alpha,\beta,\gamma\), define the vector second
divided difference

\[
q_{\alpha\beta\gamma}
=
\sum_{\delta\in\{\alpha,\beta,\gamma\}}
\frac{p_\delta}
{\prod_{\eta\in\{\alpha,\beta,\gamma\}\setminus\{\delta\}}
(\delta-\eta)}
\in C'.                                           \tag{7}
\]

At a coordinate contained in all three supports, the values of
\(p_\delta\) equal the translated received word, which is affine in the
slope. Therefore

\[
\operatorname{supp}(q_{\alpha\beta\gamma})\cap X
\subseteq E_\alpha\cup E_\beta\cup E_\gamma.     \tag{8}
\]

## 4. The quotient rank-three matroid

Choose a nonzero linear functional

\[
\ell:C'\longrightarrow\mathbb F,
\qquad \ker\ell=W,
\]

and put \(z_\gamma=\ell(p_\gamma)\). Associate to each selected slope the
column

\[
v_\gamma=(1,\gamma,z_\gamma)\in\mathbb F^3.     \tag{9}
\]

A triple \(B=\{\alpha,\beta,\gamma\}\) is a basis of the vector matroid of
these columns exactly when

\[
s_B:=\ell(q_B)\ne0.                              \tag{10}
\]

### 4.1 Nonbases contribute zero vector second difference

If \(s_B=0\), then \(q_B\in W\), so \(q_B\) vanishes on \(C\). By (8),

\[
\operatorname{wt}(q_B)\le3r.
\]

Every nonzero word in the shortened Reed--Solomon code has weight at least

\[
n-K+1=R+1=1{,}048{,}577.                         \tag{11}
\]

Consequently,

\[
3r<R+1\quad\Longrightarrow\quad q_B=0             \tag{12}
\]

for every nonbasis triple.

### 4.2 Adjacent bases require only four omission sets

For a basis \(B\), normalize

\[
\widehat q_B=q_B/s_B,
\qquad \ell(\widehat q_B)=1.                      \tag{13}
\]

If bases \(B,B'\) are adjacent, they share two slopes and
\(|B\cup B'|=4\). Their normalized difference belongs to \(W\):

\[
\widehat q_B-\widehat q_{B'}\in W.
\]

It therefore vanishes on \(C\). Outside \(C\), equations (8) for the two
bases show

\[
\operatorname{supp}(\widehat q_B-\widehat q_{B'})
\subseteq\bigcup_{\delta\in B\cup B'}E_\delta,
\]

and hence

\[
\operatorname{wt}(\widehat q_B-\widehat q_{B'})\le4r. \tag{14}
\]

Thus

\[
4r<R+1
\quad\Longrightarrow\quad
\widehat q_B=\widehat q_{B'}                     \tag{15}
\]

for adjacent bases.

### 4.3 Basis-graph connectivity synchronizes all bases

The basis graph of any matroid is connected. For completeness, let \(B\) and
\(B'\) be bases. If they differ, basis exchange gives
\(b\in B\setminus B'\) and \(e\in B'\setminus B\) such that
\(B-b+e\) is a basis. This exchange reduces \(|B\setminus B'|\); induction
produces a path of single exchanges from \(B\) to \(B'\).

Therefore (15) forces one common normalized vector \(Q\in C'\) with

\[
\widehat q_B=Q
\]

for every basis \(B\). By (12), every nonbasis triple has \(q_B=0\). Hence
for **every** triple,

\[
q_B\in\langle Q\rangle.                           \tag{16}
\]

Pass to \(C'/\langle Q\rangle\). All second divided differences vanish
there, so the image of \(p_\gamma\) is affine in \(\gamma\). Choosing two
reference slopes gives \(H_0,H_1\in C'\) and scalars \(c_\gamma\) such that

\[
\boxed{
 p_\gamma=H_0+\gamma H_1+c_\gamma Q
 \qquad(\gamma\in Z_{\mathrm{out}}).
}                                                   \tag{17}
\]

If the quotient matroid has rank at most two, (12) already says every vector
second difference is zero, and (17) holds with a zero correction parameter.
Thus the complete outside-core family is one affine correction ray.

## 5. Exact four-support threshold

The largest integer satisfying \(4r<R+1\) is

\[
r_{\max}=\left\lfloor\frac R4\right\rfloor
=262{,}144,
\]

because

\[
4r_{\max}=1{,}048{,}576<R+1.
\]

Equivalently, the actual common locator must satisfy

\[
c\ge t-r_{\max}=718{,}960.                        \tag{18}
\]

The parent floor first guarantees (18) at

\[
\boxed{K=778{,}970}.                               \tag{19}
\]

This improves the former six-support threshold \(K=858{,}619\) by
\(79{,}649\) ambient dimensions.

## 6. Universal-core-aware payment of the synchronized ray

Translate (17) by the fixed affine base \(H_0+\gamma H_1\). The parameter
point attached to \(\gamma\) is \((\gamma,c_\gamma)\), and its explanation
is \(c_\gamma Q\).

Let \(U\subseteq X\) be the coordinates at which the translated received
pair and \(Q\) all vanish. Put

\[
u=|U|,
\qquad M=m-u,
\qquad N=|X|-u=M+r.                                \tag{20}
\]

Since \(Q\ne0\) has degree less than \(K\),

\[
0\le u\le K-1,
\qquad D+1\le M\le K+D.                            \tag{21}
\]

Every selected support contains at least \(M\) nonuniversal coordinate
copies.

For \(Q(x)\ne0\), agreement is one affine graph line in the parameter
plane; equal graph lines form a weighted clone class. For \(Q(x)=0\) but
\(x\notin U\), agreement is one vertical line. A selected support must use
at least two nonuniversal parameter-line classes: universal coordinates plus
one graph clone would give a simultaneous codeword-pair explanation, while
all zero coordinates of \(Q\) together have size at most \(K-1<m\).

In the active interval,

\[
N\le K+D+r<2K,                                    \tag{22}
\]

so at most one graph clone has weight at least \(K\). Assign every selected
point on that graph to it. If its weight is \(w\), each assigned support
uses at least \(\max\{1,M-w\}\) outside coordinates. A fixed outside line
meets the graph once, so the graph owns at most

\[
\left\lfloor\frac{N-w}{\max\{1,M-w\}}\right\rfloor
\le r+1.                                           \tag{23}
\]

After removing those points, every parameter-line class in a residual
support has weight at most \(K-1\). The minimum number of heterogeneous
coordinate pairs in at least \(M\) copies is

\[
B_K(M)=
\begin{cases}
M-1,&M\le K-1,\\[1mm]
(K-1)(M-K+1),&M\ge K.
\end{cases}                                       \tag{24}
\]

Two distinct parameter lines meet at at most one point. Therefore

\[
|Z_{\mathrm{out}}|
\le r+1+
\max_{D+1\le M\le K+D}
\left\lfloor\frac{\binom{M+r}{2}}{B_K(M)}\right\rfloor. \tag{25}
\]

On \(D+1\le M\le K-1\), writing \(x=M-1\), the unfloored quotient has
second derivative

\[
\frac{r(r+1)}{x^3}\ge0.
\]

On \(K\le M\le K+D\), writing \(y=M-K+1\), its second derivative is

\[
\frac{(K+r-2)(K+r-1)}{(K-1)y^3}>0.
\]

Thus only

\[
M\in\{D+1,K-1,K,K+D\}                             \tag{26}
\]

need be checked.

The exact scan of all \(269{,}607\) cells in (19) through \(K=1{,}048{,}576\)
gives

\[
\boxed{|Z_{\mathrm{out}}|\le1{,}067{,}271}.       \tag{27}
\]

The unique maximum occurs at \(K=778{,}970\), where

\[
(c,r,k)=(718{,}960,262{,}144,60{,}010).
\]

The four endpoint values in (26) are

```text
M=D+1      1,067,271
M=K-1        957,882
M=K          957,883
M=K+D        262,156
```

## 7. Payment of the complete large-locator interval

The support partition is disjoint. Equations (5) and (27) yield

\[
|Z|
\le4{,}070{,}947+1{,}067{,}271
=5{,}138{,}218
<5{,}170{,}912.                                    \tag{28}
\]

The exact contradiction slack is

\[
\boxed{32{,}694}.                                  \tag{29}
\]

Therefore a proper rank-two drop is impossible for every

\[
\boxed{778{,}970\le K\le1{,}048{,}576}.           \tag{30}
\]

At every heavy coordinate the only remaining outcome is a whole-family pair
core. Hence all \(5{,}170{,}912\) slopes shorten intact through all
\(269{,}607\) top dimensions and reach

\[
\boxed{K\le778{,}969}.                             \tag{31}
\]

## 8. The conditional near-MDS interval

The ray accounting in Section 6 remains below \(L_2\) even after the strict
four-support inequality fails. Exact capacity inversion and ray optimization
show that for every

\[
774{,}075\le K\le778{,}969,                        \tag{32}
\]

the **synchronized** ray branch satisfies

\[
A_1+R_{\mathrm{ray}}(K)<L_2.
\]

The worst cell is \(K=774{,}075\):

```text
rank-one global cap       4,070,947
synchronized ray cap      1,099,960
-----------------------------------
total                     5,170,907
rank-two load             5,170,912
slack                             5
```

Thus a surviving proper drop in (32) must contain adjacent quotient bases
whose normalized second differences are unequal. Their difference is a
nonzero word \(P\in W\) supported in at most four omission sets. After
factoring the actual common-core locator and the complete outside zero
locator, the residual factor has degree at most

\[
\Delta(K)=4r-(R+1).                                \tag{33}
\]

Across (32), \(\Delta(K)\le22{,}063\). At the preceding cell
\(K=774{,}074\), the synchronized-ray total is \(L_2+1\); this is the exact
arithmetic wall of this conditional compiler.

## 9. The adjacent cubic terminal

At \(K=778{,}969\), the parent floor gives

\[
c=718{,}959,
\qquad r=262{,}145,
\qquad 4r=R+4.                                     \tag{34}
\]

If all normalized basis second differences coincide, the single-ray branch
has cap

\[
4{,}070{,}947+1{,}067{,}277
=5{,}138{,}224<L_2
\]

with slack \(32{,}688\). Hence any surviving proper drop emits a nonzero
basis-edge difference \(P\in W\) of weight

\[
R+1\le\operatorname{wt}(P)\le R+4.                \tag{35}
\]

The outside-core domain has size

\[
N=1{,}108{,}586,
\qquad k=K-c=60{,}010.
\]

Since \(P\) vanishes on \(C\), it has between \(60{,}006\) and \(60{,}009\)
zeros outside \(C\). Dividing by the common-core locator and the complete
outside zero locator leaves a polynomial factor of degree at most

\[
(k-1)-60{,}006=3.                                  \tag{36}
\]

Thus the exact adjacent terminal is

\[
\boxed{\texttt{CUBIC\_NEAR\_MDS\_BASIS\_EDGE}}.
\]

This is a structural terminal, not an unsafe certificate.

## 10. Scope

This packet pays the proper-drop branch only in (30), and proves the
conditional near-MDS route cut (32)--(36). It does not pay affine error rank
twelve, move an active-v4 ledger atom, or close KoalaBear.
