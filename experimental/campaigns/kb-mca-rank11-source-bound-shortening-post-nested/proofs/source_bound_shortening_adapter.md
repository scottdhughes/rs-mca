# Source-bound locator shortening for the nested pinned-span ladder

## 1. Complete-agreement shortening lemma

Let

\[
 C=\operatorname{RS}_{\mathbb F}(D,K),\qquad |D|=n,
\]

and let `r=(r_0,r_1)` be a received pair.  Fix a finite slope `gamma`, a
codeword `c_gamma`, and its complete scalar agreement domain

\[
 A_\gamma=\{x\in D:r_0(x)+\gamma r_1(x)=c_\gamma(x)\}.
\]

Assume `|A_gamma|>=m`, no pair in `C^2` simultaneously explains the received
pair on `A_gamma`, and `T subset A_gamma` with `|T|=k<K`.

Choose a codeword pair `(p_0,p_1)` satisfying

\[
 p_i(x)=r_i(x)\qquad(x\in T,\ i=0,1).
\]

Such a pair exists by interpolation.  Put

\[
 L_T(X)=\prod_{x\in T}(X-x),\qquad D'=D\setminus T,
\]

and define the shortened received words on `D'` by

\[
 r_i'(x)=\frac{r_i(x)-p_i(x)}{L_T(x)}.
\]

Since `c_gamma-p_0-gamma p_1` vanishes at every point of `T`, define

\[
 c_\gamma'=\frac{c_\gamma-p_0-\gamma p_1}{L_T}
 \in\mathbb F[X]_{<K-k}.
\]

Then `r_0'+gamma r_1'=c_gamma'` on
`A_gamma'=A_gamma\setminus T`, whose size is at least `m-k`.

Suppose a shortened pair `(u,v)`, with degrees `<K-k`, simultaneously
explained the shortened received pair on `A_gamma'`.  The lifted pair

\[
 (p_0+L_Tu,\ p_1+L_Tv)
\]

has degree `<K`, agrees with the received pair on `A_gamma'`, and agrees on
`T` by interpolation.  It therefore explains the received pair on all of
`A_gamma`, contradicting pair noncontainment.  Hence the slope remains
support-wise MCA-bad in `RS_F(D',K-k)` at agreement `m-k`.

## 2. Why the complete agreement domain is essential

It is false that one may simply swap a pinned coordinate into an arbitrary
exact size-`m` bad support.

Over `GF(5)`, take `D={0,1,2,3}`, `K=2`, `m=3`,

```text
r_0=(0,0,0,0),
r_1=(0,0,1,0),
gamma=0,
c_gamma=0.
```

The scalar explanation agrees on all of `D`.  The support `{0,1,2}` is
pair-noncontained: an affine polynomial vanishing at 0 and 1 is zero and
cannot take value 1 at 2.  But replacing 2 by the pinned coordinate 3 gives
`{0,1,3}`, on which the pair `(0,0)` simultaneously explains the received
pair.

The complete scalar agreement domain `D` is nevertheless pair-noncontained,
and shortening at `{3}` retains the bad domain `{0,1,2}`.  This is exactly the
mechanism used above.

## 3. Pair-direction compatibility

Suppose each slope has a designated pair
`e_gamma=(a_gamma,b_gamma)` with

\[
 c_\gamma=a_\gamma+\gamma b_\gamma
\]

and that the pair agrees individually with the received pair on `T`.  Then

\[
 a_\gamma'=\frac{a_\gamma-p_0}{L_T},\qquad
 b_\gamma'=\frac{b_\gamma-p_1}{L_T}
\]

are degree-`<K-k` codewords and
`c_gamma'=a_gamma'+gamma b_gamma'`.

If a direction space `V` vanishes on `T`, locator division defines an
injective linear map

\[
 V\longrightarrow\mathbb F[X]_{<K-k},\qquad f\mapsto f/L_T.
\]

Thus direction dimensions and all pair-difference containments are preserved.

## 4. Application to the nested pinned-span packet

The parent packet supplies

\[
 T_1\subset\cdots\subset T_{10}\subset G_0
\]

and nested parent-direction spans

\[
 V_{10}\le\cdots\le V_1\le C'.
\]

Every assigned minimizing pair agrees individually with the actual received
pair on the appropriate `T_k`.  Choose one polynomial pair `(p_0,p_1)` of
degree `<10` interpolating the received pair on `T_10`; the same pair works
for every prefix.

For each `k`, write

\[
 L_k(X)=\prod_{x\in T_k}(X-x)
\]

and apply the lemma to the complete agreement domain of every assigned slope.
The result is an actual support-wise MCA-bad family in the shortened row

\[
 (n_k,K_k,m_k)=(n-k,K-k,m-k).
\]

The quotient direction space

\[
 \widetilde V_k=V_k/L_k
\]

has the same dimension as `V_k`.  If
`T_{k+1}=T_k union {x_{k+1}}`, then

\[
 (X-x_{k+1})\widetilde V_{k+1}\le\widetilde V_k.
\]

Thus the ten outputs form one compatible quotient ladder rather than ten
unrelated shortened certificates.

## 5. Deployed table

```text
k   n_k      K_k      m_k      bad slopes at least        dim at least
1   2097151  1048575  1116047  2,843,853,816,476,423      8
2   2097150  1048574  1116046     93,708,171,878,891      7
3   2097149  1048573  1116045      3,087,708,134,499      6
4   2097148  1048572  1116044        101,738,094,101      5
5   2097147  1048571  1116043          3,352,119,806      3
6   2097146  1048570  1116042            110,444,488      2
7   2097145  1048569  1116041              3,638,792      2
8   2097144  1048568  1116040                119,884      2
9   2097143  1048567  1116039                  3,950      2
10  2097142  1048566  1116038                    131      2
```

For every `k`,

```text
n_k-K_k = 1,048,576,
m_k-K_k =    67,472,
n_k-m_k =   981,104.
```

## 6. Exact theorem boundary

The adapter proves that the nested pins are legitimate source-level
shortening coordinates.  It does not improve the invariant row gaps and
therefore does not, by itself, pay affine error rank eleven.

The next theorem must exploit the compatible quotient relation, the enormous
first four slope loads, or the lower direction dimensions using the
relative-order-32, correction-space, Wronskian, or Sylvester/subresultant
machinery.  The ten loads may not be summed because the slope families are
nested.
