# Degree-three Johnson prefix for complete pair cores

## 1. Finite Johnson positivity

Let `X` be the set of all `h`-subsets of an `n`-set. For `0<=r<=h` and `i=1,2,3`, put `j=h-r` and

\[
q_i(r)=\frac{1}{h^{\underline i}(n-h)^{\underline i}}
\sum_{t=0}^i(-1)^t\binom it
(j^{\underline t})^2
r^{\underline{i-t}}(n-2h+r)^{\underline{i-t}}. \tag{1}
\]

The degree-`i` inclusion matrix, after orthogonal projection away from the lower inclusion spaces, has a positive-semidefinite Gram matrix whose entry at two `h`-sets depends only on their intersection size and is `q_i(r)` after normalization. Consequently, for any nonempty family `F` of `M` such sets, and its ordered inner distribution

\[
a_r=M^{-1}|\{(A,B)\in F^2:A\ne B,\ |A\cap B|=r\}|,
\]

we have

\[
a_r\ge0,\qquad \sum_ra_r=M-1,\qquad
1+\sum_ra_rq_i(r)\ge0\quad(i=1,2,3). \tag{2}
\]

This is the degree-three Johnson/Delsarte positivity statement. Formula (1) is checked directly in the exact verifier; no floating-point eigenvalue is used.

## 2. Exact dual certificate

Use

\[
(n,h,\lambda)=(1{,}052{,}933,67{,}701,4{,}356).
\]

Define

\[
\begin{aligned}
y_1&=\frac{783407435505036310}{1777114341209059},\\
y_2&=\frac{894939334590448235317}{3356227749370360},\\
y_3&=\frac{16360924804832711925677}{27945375053210112}.
\end{aligned} \tag{3}
\]

All three numbers are positive. Exact substitution gives equality in

\[
-\sum_{i=1}^3y_iq_i(r)\ge1 \tag{4}
\]

at

\[
r=3104,\quad3105,\quad4356.
\]

The verifier checks (4), as an exact rational inequality, at every integer `0<=r<=4356`. Its minimum is exactly one and occurs only at those three intersection sizes.

Multiplying (2) by the nonnegative `y_i` and summing yields

\[
M-1=\sum_ra_r
\le-\sum_i y_i\sum_ra_rq_i(r)
\le\sum_i y_i.
\]

Hence

\[
M\le1+y_1+y_2+y_3
=\frac{5562693924555713011364059}{101940091296780800}
<54{,}568{,}752,
\]

and therefore

\[
\boxed{M\le54{,}568{,}751}. \tag{5}
\]

## 3. Application to minimizing-pair cores

At ambient shortened dimension `K=4357`, take deficiency cutoff `T=4128`. Then

\[
n=R+K=1{,}052{,}933,\qquad
h=d+K-T=67{,}701,\qquad
\lambda=K-1=4{,}356.
\]

For each distinct minimizing-pair type of deficiency at most `T`, choose one canonical `h`-subset of its complete pair core. Distinct pair types have complete-core intersection at most `K-1`, because at least one endpoint difference is a nonzero polynomial of degree `<K`. Thus (5) applies.

The former ordinary affine pair-list prefix at this cell is

\[
\left\lfloor\frac{\binom{R+11}{11}}{\binom{d-T+11}{11}}\right\rfloor
=25{,}551{,}333{,}830{,}332.
\]

The exact degree-three prefix is `54,568,751`.

Using the conservative fixed-pair multiplicity `R-d+1=981,105` and the pointwise rank-eleven resource, the resulting one-threshold slope ceiling is

\[
54{,}568{,}751\cdot981{,}105+
\left\lfloor\frac{C_{11}(4357)}{4129}\right\rfloor
=3{,}293{,}927{,}023{,}491{,}665. \tag{6}
\]

Equation (6) is a local ambient-cell cap, not a complete rank-12 payment.
