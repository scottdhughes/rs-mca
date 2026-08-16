# Nested weighted pinning and span-dimension ladder

## 1. Exact deployed cell

Use

```text
n=2,097,152, K=1,048,576, m=1,116,048, w=67,472,
B*=274,980,728,111,395,087,
C_10=106,618,568,137,036,225,644.
```

Select

\[
 \tau=1937,\qquad h=36775.
\]

Then

\[
 A=m-\tau=1114111,\quad d=A-K=65535,\quad
 c=2A-n=131070,\quad q=h+1=36776.
\]

The anchored-rich-flat envelope gives

\[
 N_1=\left\lfloor\frac{m^{\underline 9}}{(c-h)^9}\right\rfloor
     =4557575472,
\]

\[
 N_2=\left\lfloor\frac{m^{\underline 8}}{(c-h)^8}\right\rfloor
     =385072738.
\]

The dimension-two pair-list cap is `255`, so one rank-two row-space packet
costs

\[
 R_2=(n-A)255=250675455.
\]

The exact transverse accounting is

\[
 T_{\rm tr}
 =134944+\left\lfloor\frac{C_{10}}{1938}\right\rfloor
 +(n-A)+8147918N_1+R_2N_2
 =188677776072813437.
\]

Hence every line with at least \(B^*+1\) bad slopes has nontransverse packet
load at least

\[
 L=B^*+1-T_{\rm tr}=86302952038581651. \tag{1}
\]

## 2. Immediate parents

For every nontransverse row-space packet, use the deterministic immediate
parent construction from the included factor-synchronization packet.  This
gives a dimension-two or dimension-three space \(W_i\), a selected actual
anchor-zero set

\[
 J_i,\qquad |J_i|=q,
\]

and a disjoint assigned-slope load \(\lambda_i\).  Equal parents are merged.
Thus

\[
 \sum_i\lambda_i\ge L. \tag{2}
\]

Every pair assigned to \(W_i\) has both endpoint-difference rows in \(W_i\).

## 3. Nested weighted flag lemma

Let \(I_0\) be the full parent index set, \(T_0=\varnothing\), and
\(L_0=\sum_i\lambda_i\).  Suppose \(T_j\) and

\[
 I_j=\{i:T_j\subseteq J_i\}
\]

have been chosen.  Since each \(J_i\) has size \(q\), double counting the
remaining coordinate incidences gives

\[
 \sum_{x\notin T_j}\sum_{\substack{i\in I_j\\x\in J_i}}\lambda_i
 =(q-j)\sum_{i\in I_j}\lambda_i. \tag{3}
\]

There are at most \(m-j\) available coordinates.  Hence some
\(x_{j+1}\notin T_j\) satisfies

\[
 \sum_{i\in I_j:x_{j+1}\in J_i}\lambda_i
 \ge
 \left\lceil
 \frac{q-j}{m-j}\sum_{i\in I_j}\lambda_i
 \right\rceil. \tag{4}
\]

Set \(T_{j+1}=T_j\cup\{x_{j+1}\}\) and restrict \(I_j\) accordingly.
Induction gives one nested chain

\[
 T_1\subset T_2\subset\cdots\subset T_{10},
 \qquad |T_k|=k, \tag{5}
\]

whose assigned loads are at least

\[
 L_k=
 \left\lceil L\frac{q^{\underline k}}{m^{\underline k}}\right\rceil.
 \tag{6}
\]

At the deployed values,

```text
k   L_k
1   2,843,853,816,476,423
2      93,708,171,878,891
3       3,087,708,134,499
4         101,738,094,101
5           3,352,119,806
6             110,444,488
7               3,638,792
8                 119,884
9                   3,950
10                    131
```

## 4. Nested direction spaces

Let

\[
 V_k=\sum_{i\in I_k}W_i.
\]

Then

\[
 V_{10}\le\cdots\le V_2\le V_1\le C', \tag{7}
\]

and every member of \(V_k\) vanishes on \(T_k\).  Every assigned pair in
\(I_k\) lies in

\[
 (a_0+V_k)\times(b_0+V_k). \tag{8}
\]

Put \(r_k=\dim V_k\).  For a direction space of dimension \(r\), the ordinary
affine Reed--Solomon endpoint cap at agreement \(A\) is

\[
 M_r=
 \left\lfloor
 \frac{\binom{n-K+r}{r}}{\binom{A-K+r}{r}}
 \right\rfloor. \tag{9}
\]

The exact values for \(1\le r\le10\) are

```text
r   M_r             (n-A)M_r
1   16                   15,728,656
2   255                 250,675,455
3   4,095             4,025,552,895
4   65,530           64,418,676,730
5   1,048,431     1,030,650,658,671
6   16,773,712   16,489,246,618,192
7   268,356,622 263,805,562,047,502
8   4,293,280,145 4,220,470,407,020,945
9   68,684,687,551 67,519,863,934,822,591
10  1,098,814,582,063 1,080,179,785,565,793,583
```

For every displayed \(r\), \(M_r^2<2130706433^6\).  The inherited
sub-square interleaving theorem therefore bounds the number of ordered pair
types in (8) by \(M_r\).  Each pair type owns at most \(n-A=983041\) slopes.
Consequently the assigned load of \(I_k\) is at most \((n-A)M_{r_k}\).

Comparing with (6) gives

\[
\begin{array}{c|c|c|c}
k&L_k&\text{largest excluded dimension}&\dim V_k\text{ at least}\\ \hline
1&2843853816476423&7&8\\
2&93708171878891&6&7\\
3&3087708134499&5&6\\
4&101738094101&4&5\\
5&3352119806&2&3\\
6&110444488&1&2.
\end{array} \tag{10}
\]

For \(7\le k\le10\), positive load leaves at least one immediate parent, so
\(\dim V_k\ge2\).

## 5. Additional abundance control

At this cell the dimension-three parent cap is

\[
 (n-A)M_3=4025552895.
\]

Thus the nontransverse load in (1) uses at least

\[
 \left\lceil\frac{L}{4025552895}\right\rceil=21438783
\]

distinct merged parents.  Applying the same convex degree-moment argument as
the included synchronization packet to their \(q\)-sets gives common
intersections of at least

```text
two parents      1,212 coordinates
three parents       40 coordinates
four parents         2 coordinates
five parents         1 coordinate
```

This abundance statement is supplementary; the nested weighted flag is the
stronger successor terminal.

## 6. Exact successor obligation

The nested flag is source-level but not yet a first-match owner.  The next
theorem must cancel one nested locator chain as a whole, or prove a structured
rank bound on the quotient family.  In particular, the \(T_1\)-family has
more than \(2.84\times10^{15}\) assigned slopes, common locator \(X-x_1\),
and direction dimension at least eight.

Independent cancellation of different parents or different pins remains
unauthorized.

## 7. Nonclaims

- Rank eleven is not paid.
- KoalaBear is not closed.
- No active-v4 atom moves.
- The spaces \(V_k\) need not be represented by individual minimizing pairs.
- The nested loads are not added to one another.
