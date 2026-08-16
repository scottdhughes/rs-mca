# Weighted parent-factor synchronization

## 1. Inherited exact envelope

Use the deployed KoalaBear row

```text
n = 2,097,152
K = 1,048,576
m = 1,116,048
w = 67,472
B* = 274,980,728,111,395,087
2w = 134,944.
```

Fix

\[
 \tau=1549,\qquad h=42447.
\]

The anchored rich-flat predecessor gives

\[
 A=m-\tau=1114499,\qquad
 c=2A-n=131846,\qquad
 q=h+1=42448.
\]

Its complete transverse envelope is

\[
 T_{\rm tr}=274871033266908609,
\]

so

\[
 B^*-T_{\rm tr}=109694844486478. \tag{1}
\]

If a line has at least \(B^*+1\) bad slopes, then its disjoint nontransverse
row-space packets carry total load at least

\[
 L=B^*+1-T_{\rm tr}
  =109694844486479. \tag{2}
\]

No density, expectation, or asymptotic inference occurs here.

## 2. Canonical immediate-parent routing

For a nontransverse represented row space \(U\), the predecessor supplies a
proper flat

\[
 F<U^\perp
\]

containing at least \(q\) labeled evaluation columns from the fixed actual
anchor-good support.

Choose once and deterministically an intermediate space \(W\) satisfying

\[
 U\subset W\subseteq F^\perp,\qquad \dim W=\dim U+1. \tag{3}
\]

For example, use the first vector in the frozen ambient basis order that
extends \(U\) inside \(F^\perp\).  Then

\[
 \dim W\in\{2,3\},
\]

and every polynomial in \(W\) vanishes on the selected \(q\)-set \(J_W\).

Route the entire disjoint \(U\)-packet to this \(W\), and merge packets with
the same parent before charging them.

Every pair assigned to \(W\) has both endpoint-difference rows in \(W\), so
all assigned pairs lie in

\[
 (a_0+W)\times(b_0+W). \tag{4}
\]

At the selected cutoff,

\[
 n-A=982653.
\]

The exact projected affine-list caps are

\[
 M_2=252,\qquad M_3=4023.
\]

The sextic field guard \(M_3^2<|\mathbb F|\) holds.  Thus a dimension-three
parent owns at most

\[
 R_3=(n-A)M_3=3953213019 \tag{5}
\]

assigned slopes.  This also dominates the dimension-two cap.

Combining (2) and (5), the number \(N\) of distinct merged parents satisfies

\[
 N\ge
 \left\lceil\frac{109694844486479}{3953213019}\right\rceil
 =27749. \tag{6}
\]

The preceding integer is sharp for this abstraction:

\[
 27748R_3<L\le27749R_3.
\]

## 3. Unweighted intersection moments

For each of the \(N\) parents, choose one canonical subset

\[
 J_i\subseteq J_{W_i},\qquad |J_i|=q.
\]

All \(J_i\) lie in the same actual anchor-good support \(G_0\), with

\[
 |G_0|\le m.
\]

Pad the universe by unused labels to size \(m\).  Put

\[
 d_x=\#\{i:x\in J_i\}.
\]

Then

\[
 \sum_x d_x=Nq=1177889552.
\]

Write

\[
 Nq=am+b,\qquad
 a=1055,\quad b=458912. \tag{7}
\]

For every \(k\ge2\),

\[
 \sum_{\substack{I\subseteq[N]\\|I|=k}}
 \left|\bigcap_{i\in I}J_i\right|
 =
 \sum_x\binom{d_x}{k}. \tag{8}
\]

The integer function \(d\mapsto\binom d k\) is discretely convex.  Subject to
(7), the right side of (8) is minimized by \(m-b\) degrees equal to \(a\)
and \(b\) degrees equal to \(a+1\).  Hence some \(k\)-set of parents has
intersection at least

\[
 I_k=
 \left\lceil
 \frac{(m-b)\binom ak+b\binom{a+1}k}
      {\binom Nk}
 \right\rceil. \tag{9}
\]

Exact evaluation gives

\[
 I_2=1614,\qquad
 I_3=62,\qquad
 I_4=3,\qquad
 I_5=1. \tag{10}
\]

If \(W_{i_1},\ldots,W_{i_k}\) are the selected parents, every polynomial in

\[
 V_k=W_{i_1}+\cdots+W_{i_k}
\]

vanishes on their common coordinates.  Since each parent has dimension at
most three,

\[
\begin{array}{c|c|c}
k&\dim V_k\text{ at most}&\text{common locator degree at least}\\ \hline
2&6&1614\\
3&9&62\\
4&10&3\\
5&10&1.
\end{array} \tag{11}
\]

The sum-space need not itself be represented by one minimizing pair.

## 4. Weighted synchronization

Let \(\lambda_i\) be the distinct-slope load assigned to parent \(W_i\).
The parent packets are disjoint and

\[
 \sum_i\lambda_i\ge L.
\]

For a fixed \(k\), double count pairs \((i,T)\) weighted by \(\lambda_i\),
where \(T\subseteq J_i\) and \(|T|=k\):

\[
 \sum_{\substack{T\subseteq G_0\\|T|=k}}
 \sum_{i:T\subseteq J_i}\lambda_i
 =
 \sum_i\lambda_i\binom qk
 \ge L\binom qk. \tag{12}
\]

Therefore some fixed \(k\)-coordinate set \(T\) is contained in parents
carrying total assigned load at least

\[
 \Lambda_k=
 \left\lceil
 \frac{L\binom qk}{\binom mk}
 \right\rceil. \tag{13}
\]

The exact values are

\[
\begin{array}{c|r}
k&\Lambda_k\\ \hline
1&4172156357758\\
2&158681059954\\
3&6035034641\\
4&229522148\\
5&8728902\\
6&331960\\
7&12625\\
8&481\\
9&19\\
10&1.
\end{array} \tag{14}
\]

Every parent counted in the inner sum of (12) lies in the common kernel

\[
 C'_T=\{P\in C':P(x)=0\ \text{for every }x\in T\}. \tag{15}
\]

Thus (14) is a source-level weighted common-factor concentration statement,
not merely an unweighted set intersection.

## 5. Exact next theorem

The strongest remaining joint is now localized:

> For one of the synchronized spaces or weighted kernel families in
> (11)--(15), either perform common-locator cancellation into one existing
> chronology owner, or prove a Sylvester/subresultant rank bound below the
> corresponding assigned slope load.

The factors may not be cancelled separately parent by parent.

## 6. Nonclaims

- Rank eleven is not paid.
- KoalaBear is not closed.
- No active-v4 atom moves.
- No claim is made that all \(27,749\) parents share one locator.
- No synchronized sum-space is declared represented or independently
  chargeable.
