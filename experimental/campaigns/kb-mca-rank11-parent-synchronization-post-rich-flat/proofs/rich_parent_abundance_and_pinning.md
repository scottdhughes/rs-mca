# Rich-parent abundance, synchronization, and weighted pinning

## 1. Inherited exact envelope

Use the KoalaBear row

```text
n=2,097,152, K=1,048,576, m=1,116,048,
w=67,472, B*=274,980,728,111,395,087.
```

At cutoff `tau=1547`, put

```text
A=m-tau=1,114,501,
d=A-K=65,925,
mu=n-A=982,651.
```

The anchored rich-flat predecessor proves that the near-rational add-back,
high-margin tail, anchor packet, and every `h=42452` transverse row-space
packet together contribute at most

\[
 T_0=274978720888758363. \tag{1}
\]

Thus an unsafe line, which has at least `B*+1` bad slopes, has a disjoint
nontransverse load

\[
 L_0=B^*+1-T_0=2007222636725. \tag{2}
\]

For each nontransverse rank-`r` row space `U`, `r in {1,2}`, the predecessor
produces a direction subspace `W` with

\[
 U\subsetneq W\le C'
\]

and at least

\[
 q=42453 \tag{3}
\]

actual anchor-good coordinates on which every polynomial in `W` vanishes.

## 2. Canonical exact-dimensional parents

Fix once and for all an ordered basis of `C'`, the induced row-reduced order
on its subspaces, and the deployed coordinate order.

For each nontransverse `U`:

1. choose the first predecessor witness flat and its common-zero labels;
2. choose the first subspace `P` satisfying
   \[
    U<P\le W,\qquad \dim P=\dim U+1;
   \]
3. choose the first `q` common-zero coordinates of `P`.

Assign the entire slope packet of `U` to `P`. If several `U` map to the same
`P`, merge their packets. The packets remain disjoint because the source
row-space packets were disjoint.

The resulting parent has dimension two when `rank(U)=1` and dimension three
when `rank(U)=2`. Every pair difference in the merged packet lies in `P`.
Moreover, `P` vanishes on every source witness set assigned to it, so its
canonical common-zero set `J_P` can be chosen with

\[
 J_P\subseteq G_0,\qquad |J_P|=q. \tag{4}
\]

## 3. Exact parent packet caps

For a direction dimension `r`, the ordinary affine list cap at this cutoff is

\[
 Q_r=\left\lfloor
 \frac{\binom{n-K+r}{r}}{\binom{d+r}{r}}
 \right\rfloor. \tag{5}
\]

The sextic line field satisfies `Q_r^2<|F|` for every dimension used below, so
the sub-square interleaving collapse bounds the ordered pair list by `Q_r`.
Every fixed pair owns at most `mu=n-A` slopes.

For dimensions two and three,

\[
 Q_2=252,\qquad Q_3=4023, \tag{6}
\]

and hence

\[
 R_2=\mu Q_2=247628052,\qquad
 R_3=\mu Q_3=3953204973. \tag{7}
\]

If `ell_P` is the assigned slope load of a parent, then

\[
 0<\ell_P\le R_{\dim P},
 \qquad
 \sum_P\ell_P\ge L_0. \tag{8}
\]

## 4. Parent abundance

Since `R_3>R_2`, (8) immediately gives

\[
 |\mathcal P_2|+|\mathcal P_3|
 \ge \left\lceil\frac{L_0}{R_3}\right\rceil
 =508. \tag{9}
\]

A fixed-dimension conclusion is only slightly weaker. If both parent classes
had at most `477` members, then

\[
 \sum_P\ell_P
 \le477(R_2+R_3)
 =2003797352925
 <L_0, \tag{10}
\]

where the shortfall is `3,425,283,800`. Therefore

\[
 \max\{|\mathcal P_2|,|\mathcal P_3|\}\ge478. \tag{11}
\]

## 5. Synchronizing the common-zero sets

Choose `N=478` parents from the class supplied by (11). Their canonical
sets `J_i` all have size `q` in the same anchor universe `G_0`, with
`|G_0|<=m`.

For a coordinate `x`, let `d_x` be the number of selected sets containing it.
For every integer `k>=1`,

\[
 \sum_{1\le i_1<\cdots<i_k\le N}
 |J_{i_1}\cap\cdots\cap J_{i_k}|
 =\sum_{x\in G_0}\binom{d_x}{k}. \tag{12}
\]

The right side is minimized, subject to
`sum_x d_x=Nq`, when the degrees differ by at most one. Padding `G_0` by
empty coordinates to size `m` can only weaken the result. Here

\[
 Nq=18m+203670. \tag{13}
\]

Consequently

\[
 \sum_x\binom{d_x}{k}
 \ge (m-203670)\binom{18}{k}
     +203670\binom{19}{k}. \tag{14}
\]

Dividing by `binom(478,k)` and taking ceilings yields

\[
\begin{array}{c|ccc}
 k&2&3&4\\ \hline
 \max |J_{i_1}\cap\cdots\cap J_{i_k}|&1530&53&2.
\end{array} \tag{15}
\]

In particular, two distinct parents of the selected fixed dimension have at
least `1530` common zeros. If their dimension is two, their sum has dimension
at least three; if their dimension is three, their sum has dimension at least
four. In either case every polynomial in the sum vanishes on the intersection.
Thus an unsafe line emits either

\[
 \dim V\ge3,\quad \deg\gcd(V)\ge1530, \tag{16a}
\]

or

\[
 \dim V\ge4,\quad \deg\gcd(V)\ge1530. \tag{16b}
\]

The distinction records whether the abundant parent class has dimension two
or three.

## 6. Weighted coordinate pinning

The abundance theorem ignores packet weights after (11). The full weighted
incidence identity gives a different and stronger dimension conclusion.
For a coordinate subset `T`, let

\[
 \Lambda_T=\sum_{P:T\subseteq J_P}\ell_P. \tag{17}
\]

For every `k<=q`, double counting `(assigned slope,T)` incidences gives

\[
 \sum_{T\in\binom{G_0}{k}}\Lambda_T
 =\sum_P\ell_P\binom{q}{k}
 \ge L_0\binom{q}{k}. \tag{18}
\]

Since `|G_0|<=m`, some `k`-set satisfies

\[
 \Lambda_T\ge
 \left\lceil
 \frac{L_0\binom qk}{\binom mk}
 \right\rceil. \tag{19}
\]

The exact first nine values are

```text
k=1   76,352,112,631
k=2    2,904,268,266
k=3      110,469,544
k=4        4,201,831
k=5          159,818
k=6            6,079
k=7              232
k=8                9
k=9                1
```

### One-coordinate dimension growth

Take the coordinate `x` supplied by (19) for `k=1`, and let

\[
 V_x=\sum_{P:x\in J_P}P. \tag{20}
\]

Every polynomial in `V_x` vanishes at `x`, and every assigned pair in the
pinned packets has both endpoint differences in `V_x`.

If `dim V_x<=4`, the same interleaved-list argument as in Section 3 gives

\[
 \Lambda_{\{x\}}
 \le \mu Q_4. \tag{21}
\]

Exact arithmetic gives

\[
 Q_4=63993,\qquad \mu Q_4=62882785443. \tag{22}
\]

But

\[
 76352112631-62882785443=13469327188>0. \tag{23}
\]

Therefore

\[
 \boxed{\dim V_x\ge5} \tag{24}
\]

and `X-x` divides every polynomial in `V_x`. The pinned packet load is at
least `76,352,112,631` distinct slopes.

### Two-coordinate dimension growth

For the two-set `T` supplied by (19),

\[
 \Lambda_T\ge2904268266>R_2=247628052. \tag{25}
\]

Hence the span of its parent spaces has dimension at least three, and every
polynomial in that span is divisible by the two-coordinate locator.

## 7. Exact residual and nonclaims

The packet proves abundance and synchronization, not a row payment. In
particular:

- the dimension-five pinned load remains below the unrestricted dimension-five
  pair-list ceiling;
- the synchronized parent sums are not assumed to own every nontransverse
  packet;
- no locator is cancelled independently in the active chronology;
- error rank eleven and KoalaBear remain open;
- active-v4 ledger movement is zero.

The strongest next step is a source-bound shortening owner for the pinned
`dim>=5` subfamily, or an aggregate Pluecker/Wronskian theorem using the
`478` same-dimensional parents.