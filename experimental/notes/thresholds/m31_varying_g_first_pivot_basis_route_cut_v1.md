---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Every realized base-field boundary shallow family obeys first-pivot, colored, cross-block, and affine-line evaluation-basis inequalities. They exclude affine ranks at most five and force every rank-six survivor into the numerator-union interval 781458 through 1033227.
architecture: M31_BASE_FIELD_BOUNDARY_FIRST_PIVOT_BASIS_V1
parent_payload_sha256: 78a6b51d69736b574d258df9e20d84155b8be86e51db942bc6c02a710ee7866d
atom_or_cell: Direct M31 boundary diagnostic; no v4 atom value or owner payment.
quantifier: Every subfamily of reconstructed base-field boundary shallow triples satisfying the common-unit theorem.
projection_and_unit: Distinct nonanchor codewords per received word. An ordered full-rank evaluation-coordinate tuple determines at most one codeword coefficient vector.
claimed_bound: Affine ranks one through five are impossible at shallow cardinality 15775933. Rank six forces 781458<=g<=1033227. The deployed row and every rank at least six remain open. Ledger movement is zero.
status: PROVED_MARKED_BASIS_RANK5_CUT_RANK6_WINDOW_OPEN
terminal: UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE
impact: ROUTE_CUT
falsifier: A reconstructed family violating a marked-basis inequality; a shallow family of size 15775933 and affine rank at most five; a rank-six family outside 781458<=g<=1033227; or use of the abstract scalar profile as a realized family.
replay: Standard-library exhaustive big-integer optimization over every legal g, independent Sage arithmetic and exhaustive toy-family replay, hostile mutations, predecessor payload pins, and fresh proof review.
---

# M31 varying-`G` first-pivot basis route cut

## Status and exact scope

This packet strengthens the realized-codeword basis inequality in the parent
packet.  The first agreement coordinate of an ordered basis can be chosen
freely.  Only the later coordinates need the evaluation-flat cap.  The exact
result is

$$
\boxed{
\sum_{i\in I}(g+s_i)
 (w+s_i+r+e-1)_{\underline{r-1}}
 \le (R+g-e)_{\underline r}.}                       \tag{0.1}
$$

Here $(x)_{\underline k}=x(x-1)\cdots(x-k+1)$ and
$(x)_{\underline0}=1$.  The theorem excludes affine rank five in addition
to the four ranks already removed by the parent.  At the forced shallow
cardinality it gives

$$
\boxed{r\ge6},                                      \tag{0.2}
$$

and rank six requires

$$
\boxed{781,458\le g\le1,033,227}.                   \tag{0.3}
$$

The old rank-six floor was $87,070$.

This is a genuine route cut but not a row closure.  An exact abstract scalar
profile inside this interval satisfies all marked-basis refinements, the
exact balanced pair-incidence gate, and the inherited global split-support
second moment.  It is not asserted to come from polynomials or supports.
Thus the present enumerated aggregate gates do not close rank six.  The
maximal next target is a structural split-rational incidence theorem that
distinguishes realized families from the scalar profile.

Ledger movement and official endpoint movement are both zero.

## 1. Inherited boundary family

The deployed integers are

$$
\begin{aligned}
p&=2^{31}-1=2,147,483,647,\\
n&=2,097,152, &K&=1,048,576,\\
a&=1,116,023, &R&=981,129,\\
w&=a-K=67,447, &B_*&=16,777,215.
\end{aligned}                                      \tag{1.1}
$$

The sealed predecessor proves that a forbidden boundary list has a family
of

$$
L=15,775,933                                        \tag{1.2}
$$

distinct nonanchor codewords with $0\le s_i\le366,886$.  For each member,

$$
c_i={A_0\over G_i}b_i,
\qquad
H_i=\gcd(L_0,G_i-b_iV),                             \tag{1.3}
$$

where

$$
m_i=\deg G_i,
\qquad
\deg H_i=m_i+s_i,
\qquad
\deg b_i<m_i-w.                                    \tag{1.4}
$$

Put

$$
W_c=\operatorname{span}_{\mathbf F_p}\{c_i:i\in I\},
\qquad r=\dim W_c,                                  \tag{1.5}
$$

and

$$
g=\left|\bigcup_iZ(G_i)\right|,
\qquad
e=\left|E_0\cap\bigcap_iZ(b_i)\right|.             \tag{1.6}
$$

The common-zero set of $W_c$ on the deployed domain has size

$$
z=a-g+e,                                            \tag{1.7}
$$

and the parent proves

$$
z\le K-r,
\qquad g-e\ge w+r.                                 \tag{1.8}
$$

If $v_x\in\mathbf F_p^r$ is the evaluation column at a coordinate outside
the common-zero set, then every $j$-dimensional column flat contains at most

$$
K-r+j-z                                             \tag{1.9}
$$

such columns.

## 2. First-pivot and colored basis inequalities

### Theorem 2.1 (first-pivot basis inequality)

Every reconstructed subfamily above obeys (0.1).

It also obeys the two stronger colored inequalities

$$
\sum_i(m_i+s_i)
 (w+s_i+r+e-1)_{\underline{r-1}}
\le
(R-e)(R+g-e-1)_{\underline{r-1}},                  \tag{2.1}
$$

and

$$
\sum_i(g-m_i)
 (w+s_i+r+e-1)_{\underline{r-1}}
\le
g(R+g-e-1)_{\underline{r-1}}.                      \tag{2.2}
$$

Adding (2.1) and (2.2) gives (0.1).

For $r\ge2$, it further obeys the cross-block inequality

$$
\sum_i(g-m_i)(m_i+s_i)
\binom{w+s_i+r+e-2}{r-2}
\le
g(R-e)\binom{R+g-e-2}{r-2}.                        \tag{2.2a}
$$

### Proof

Fix $i$.  Outside the common-zero set, $c_i$ has exactly

$$
g+s_i                                               \tag{2.3}
$$

agreement coordinates: $g-m_i$ lie in $S_0$ and $m_i+s_i$ lie in $E_0$.
Every corresponding evaluation column is nonzero.

Choose the first coordinate of an ordered evaluation basis freely from
these $g+s_i$ agreement coordinates.  Once $j\ge1$ independent columns have
been chosen, their span has dimension $j$.  By (1.9), at most
$K-r+j-z$ of all available columns lie in that span.  Hence at least

$$
\begin{aligned}
g+s_i-(K-r+j-z)
 &=g+s_i-K+r-j+a-g+e\\
 &=w+s_i+r+e-j                                      \tag{2.4}
\end{aligned}
$$

agreement columns extend the independent tuple.  Thus $c_i$ owns at least

$$
(g+s_i)(w+s_i+r+e-1)_{\underline{r-1}}              \tag{2.5}
$$

ordered full-rank agreement tuples.

One ordered full-rank $r$-tuple can belong to at most one listed codeword:
the fixed received values on those coordinates uniquely determine the
coefficient vector in $W_c$.  There are at most

$$
(n-z)_{\underline r}=(R+g-e)_{\underline r}         \tag{2.6}
$$

ordered coordinate tuples outside the common-zero set.  Summing (2.5)
proves (0.1).

For (2.1), require the freely chosen first coordinate to lie in $E_0$.
Every $H_i$ root is outside the common-zero set: the individual unit gate
$\gcd(b_i,H_i)=1$ forbids $b_i$ from vanishing there.  Codeword $i$ has
$m_i+s_i$ such first choices, and the ambient first coordinate has only
$R-e$ choices.  The same extension argument proves (2.1).

For (2.2), require the first coordinate to lie in $S_0$.  The available
choices for codeword $i$ are exactly
$\bigl(\bigcup_jZ(G_j)\bigr)\setminus Z(G_i)$, of size $g-m_i$; the ambient
first coordinate has $g$ choices.  This proves (2.2).  Their left sides add
because $(m_i+s_i)+(g-m_i)=g+s_i$, and their right sides add because
$(R-e)+g=R+g-e$.  ∎

For (2.2a), first mark one coordinate in each block.  A column from the
$S_0$-agreement block and a column from the $E_0$-agreement block are
automatically independent: the coefficient vector of $c_i$ pairs to zero
with the first and to the nonzero value $U(y)$ with the second.  There are
$(g-m_i)(m_i+s_i)$ marked independent pairs.  Starting at dimension two,
the same flat-cap argument supplies
$\binom{w+s_i+r+e-2}{r-2}$ unordered extensions.  Globally there are at
most $g(R-e)\binom{R+g-e-2}{r-2}$ choices of a marked cross-block pair and
the remaining coordinates.  Full rank again makes the owner unique.
This proves (2.2a).  ∎

### Corollary 2.2 (line and projective-ray multiplicities)

Every affine coefficient line contains at most

$$
\left\lfloor{n-K+1\over w+1}\right\rfloor=15        \tag{2.2b}
$$

listed codewords.  Indeed, write its members as $c_t=c_0+tv$.  Coordinates
where $v=0$ and $c_0=U$ are common agreements and number at most $K-1$;
every other coordinate agrees for at most one value of $t$.  If the line
contains $M$ listed words, then

$$
Ma\le n+(M-1)(K-1),
$$

which is (2.2b).

For $r\ge2$, consequently, counting owned independent
$(r-1)$-coordinate agreement sets gives

$$
\sum_i(g+s_i)\binom{w+s_i+r+e-1}{r-2}
\le
15(R+g-e)\binom{R+g-e-1}{r-2}.                     \tag{2.2c}
$$

The first coordinate is again free, the remaining $r-2$ independent
choices use the flat cap, and each independent $(r-1)$-set defines an
affine coefficient line with at most fifteen listed points.

Every projective coefficient direction contains at most

$$
\left\lfloor {R\over w+1}\right\rfloor=14.          \tag{2.2d}
$$

If $c_j=\lambda c_i$ with $\lambda\ne1$, then
$H_i\cap H_j=\varnothing$: at a common root both codewords equal the same
nonzero received value, forcing $\lambda=1$.  Since
$|H_i|=m_i+s_i\ge w+1$, disjointness inside $E_0$ proves (2.2d).
Thus a forbidden shallow family uses at least

$$
\left\lceil {15,775,933\over14}\right\rceil
=1,126,853                                          \tag{2.2e}
$$

distinct projective codeword directions.  It cannot be routed to a bounded
collection of scalar pencils without a separate multiplicity theorem.

### Comparison with the predecessor

The predecessor used the flat cap also at dimension zero and obtained the
smaller first factor $w+s_i+r+e$.  By (1.8),

$$
g+s_i\ge w+s_i+r+e,                                \tag{2.7}
$$

so (0.1) implies the old basis inequality.  Equality in the improvement is
possible only at the common-root boundary $g-e=w+r$.

## 3. Exact deployed rank consequences

Positive $e$ only decreases the right side of (0.1) and increases every
falling-factor term.  It is therefore weakest at $e=0$.  With all $s_i=0$,
(0.1) gives

$$
L\le
\left\lfloor
{(R+g)_{\underline r}
 \over g(w+r-1)_{\underline{r-1}}}
\right\rfloor.                                     \tag{3.1}
$$

For fixed $r$, the ratio in (3.1) decreases and then increases with $g$.
Indeed

$$
{(R+g+1)_{\underline r}/(g+1)
 \over (R+g)_{\underline r}/g}
\ge1
\quad\Longleftrightarrow\quad
(r-1)(g+1)\ge R.                                   \tag{3.2}
$$

Hence its maximum on $w+r\le g\le a$ occurs at an endpoint.  The exact
uniform caps are

| rank $r$ | maximum zero-excess cap | maximizing endpoint |
|---:|---:|---:|
| 1 | 15 | $g=w+1$ |
| 2 | 241 | $g=w+2$ |
| 3 | 3,757 | $g=w+3$ |
| 4 | 58,410 | $g=w+4$ |
| 5 | 1,756,141 | $g=a$ |

All are below $L=15,775,933$, proving (0.2).

At rank six the low endpoint has cap $14,115,528$.  On the increasing
branch the adjacent exact values are

$$
\begin{array}{c|r}
g&\text{cap in (3.1)}\\ \hline
520,448&15,775,901,\\
520,449&15,775,934.
\end{array}                                        \tag{3.3}
$$

The affine-line inequality (2.2c) is stronger.  At rank six and zero excess
it gives

$$
L\le
\left\lfloor
{15(R+g)\binom{R+g-1}{4}
 \over g\binom{w+5}{4}}
\right\rfloor.                                     \tag{3.4}
$$

Positive $s_i,e$ only strengthen this bound.  Its adjacent exact caps are

$$
\begin{array}{c|r}
g&\text{cap in (3.4)}\\ \hline
781,457&15,775,916,\\
781,458&15,775,941.
\end{array}                                        \tag{3.5}
$$

This proves the lower half of (0.3).

The cross-block inequality gives the complementary upper cut.  For $g>R$,
every legal $m_i$ lies in $[w+1,R]$, and concavity gives

$$
(g-m_i)(m_i+s_i)\ge
\min\{(g-w-1)(w+1),(g-R)R\}.                        \tag{3.6}
$$

Positive $s_i,e$ again strengthen the resulting uniform inequality: the
extension binomial grows, while the ambient $E_0$ block and total coordinate
universe shrink.  Exact substitution in (2.2a) gives

$$
\begin{array}{c|r}
g&\text{rank-six cross-block cap}\\ \hline
1,033,227&15,776,172,\\
1,033,228&15,775,916.
\end{array}                                        \tag{3.7}
$$

The cap decreases through $g=R+w+1=1,048,577$.  It then increases, but at
$g=a$ is still only $14,468,798$.  This proves the upper half of (0.3).

Rank seven is not excluded even at the low endpoint; its zero-excess
first-pivot cap there is $219,428,099$.

## 4. Exact all-`g` excess optimizer

For fixed $r,g$ and $e=0$, write

$$
C_{r,g}(s)
=(g+s)(w+s+r-1)_{\underline{r-1}}.                 \tag{4.1}
$$

This is a product of $r$ positive affine functions of $s$, so it is
discretely convex.  At fixed total excess, the sum of the costs is minimized
when all entries differ by at most one.  The verifier exhausts every integer

$$
w+r\le g\le a                                      \tag{4.2}
$$

and solves the balanced integer allocation against
$(R+g)_{\underline r}$.  No floating point or asymptotic estimate is used.
The exact uniform ceilings are:

| rank | maximizing $g$ | base excess $q$ | entries at $q+1$ | maximum $\sum_i s_i$ |
|---:|---:|---:|---:|---:|
| 6 | 1,009,364 | 6,095 | 6,878,149 | 96,161,189,784 |
| 7 | 1,116,023 | 78,005 | 12,570,471 | 1,230,614,224,136 |
| 8 | 1,116,023 | 143,877 | 3,259,792 | 2,269,797,172,033 |
| 9 | 1,116,023 | 212,235 | 15,094,153 | 3,348,220,234,408 |
| 10 | 1,116,023 | 280,462 | 15,436,241 | 4,424,565,157,287 |
| 11 | 1,116,023 | 346,992 | 14,597,306 | 5,474,137,140,842 |

For rank six the optimizer takes the minimum of the affine-line envelope
with cost

$$
(g+s)\binom{w+s+5}{4}                              \tag{4.2a}
$$

and the cross-block envelope from (2.2a), over the rigorously restricted
interval (0.3).  The cross-block cost is discretely convex throughout the
only active part $R<g\le1,033,227<R+w+1$; below $R$ it is vacuous.  More
precisely, the degree gates give $w+e+1\le m_i\le R-e-s_i$.  The lower- and
upper-endpoint values of the concave product $(g-m_i)(m_i+s_i)$ differ by

$$
(R-w-1-2e-s_i)(R+w+1-g)\ge0,                      \tag{4.2b}
$$

by $2e+s_i\le R-w-1$ and $g<R+w+1$.  Its exact minimum is therefore
$(g-R+e+s_i)(R-e)$.  Relative to $e=0$, that endpoint cost increases by
$e(2R-g-s_i-e)$; this is positive on the deployed range because
$s_i\le366,886$, $2e+s_i\le913,681$, and $g\le1,116,023$.  The extension
binomial also increases while the ambient budget decreases, so $e=0$ is the
weakest case.  There the cost is $(g-R+s_i)R$.  The other rows use the
first-pivot cost (4.1) over the complete legal union range.  Thus the new
rank-six ceiling is more than ten times smaller than the predecessor's
$1,025,002,415,798$ ceiling.

At rank twelve the full shallow ceiling is permitted.  Its first union size
is exactly

$$
g=909,846,                                           \tag{4.3}
$$

with adjacent all-full caps

$$
15,775,932\quad\hbox{and}\quad15,776,019.           \tag{4.4}
$$

Thus the first-pivot theorem moves the uncut full-range branch from rank
eleven to rank twelve.

## 5. Exact rank-six aggregate route cut

The parent used Cauchy--Schwarz to lower-bound summed pair incidences.  That
relaxation can be made exact at the scalar level.  For $T=qv+\rho$, with
$0\le\rho<v$, define

$$
\pi(T,v)=v\binom q2+\rho q.                         \tag{5.1}
$$

This is the exact minimum of $\sum_x\binom{d_x}{2}$ over $v$ points with
total incidence $T$.

### Lemma 5.1 (balanced pair-incidence gate)

Put $M=\sum_i m_i$ and $S=\sum_i s_i$.  Every reconstructed family
satisfies

$$
\boxed{
\pi(M,g)+\pi(M+S,R-e)
\le (L-1)M-\binom L2(w+1),}                         \tag{5.2}
$$

as well as

$$
L(w+e+1)\le M\le\min\{Lg,L(R-e)-S\},               \tag{5.3}
$$

and $2e+s_i\le R-w-1=913,681$ for every $i$.

To prove (5.2), balance the $M$ numerator-root incidences on their actual
$g$-point union and the $M+S$ denominator-root incidences on the
$R-e$ available $E_0$ points, then sum the inherited pairwise Wronskian
root bound.  For (5.3), each nonzero $b_i$ vanishes at the $e$ common
roots, so $e\le\deg b_i<m_i-w$; also $m_i\le g$ and
$m_i+s_i\le R-e$.

Even (5.2) together with all marked-basis inequalities does not close rank
six.  Consider the scalar profile

$$
r=6,\qquad g=900,000,\qquad e=0,\qquad s_i=0,
\qquad m_i=899,999\quad(1\le i\le L).               \tag{5.4}
$$

Thus

$$
M=14,198,323,924,067.                               \tag{5.5}
$$

Exact integer substitution gives the following nonnegative slacks:

| necessary aggregate inequality | exact slack |
|---|---:|
| predecessor basis inequality | 59,479,200,309,177,922,870,036,052,970,569,240 |
| $E_0$-marked inequality (2.1) | 27,407,153,349,842,619,929,030,408,431,302,720 |
| $S_0$-marked inequality (2.2) | 176,664,888,061,209,174,836,992,414,341,886,680 |
| first-pivot total (0.1) | 204,072,041,411,051,794,766,022,822,773,189,400 |
| cross-block inequality (2.2a) | 460,698,629,600,585,299,877,979,611,070,709,550 |
| affine-line inequality (2.2c) | 2,476,896,532,094,258,299,896,800,951,250 |
| exact pair-incidence gate (5.2) | 867,885,585,529,651,763 |
| inherited Cauchy moment after multiplication by $aR$ | 49,374,815,466,171,856,144,854,090,456,850 |

The verifier also exhausts every integer $g$ in (0.3).  Combining the exact
balanced affine-line and cross-block envelopes gives

$$
\boxed{\sum_i s_i\le96,161,189,784}.                \tag{5.6}
$$

The maximum occurs at $g=1,009,364$: the affine-line ceiling is
$96,161,189,784$ and the cross-block ceiling is $96,162,018,632$.
Both balanced profiles have base excess $6,095$; the line profile raises
$6,878,149$ entries and the cross-block profile raises $7,706,997$ entries.

Profile (5.4) is an **abstract scalar feasibility certificate only**.  It
supplies no evaluation columns, split locators, Wronskians, common unit,
received word, or Reed--Solomon codewords.  It proves the route cut:

> The first-pivot, colored, cross-block, and affine-line inequalities, exact
> balanced pair incidences, degree ranges, and the inherited global
> split-support second moment do not by themselves exclude rank six.

Consequently this packet does not force the profile into a paid owner and
does not move a ledger atom.

## 6. Generic basis-extension route cut

Appending arbitrary agreement coordinates to an owned basis cannot improve
(0.1) without a new structural restriction.  If $t\ge r$, an owned basis
extends to at most

$$
\binom{R+g-e-r}{t-r}                                \tag{6.1}
$$

ambient $t$-sets, and

$$
\binom{R+g-e}{r}
\binom{R+g-e-r}{t-r}
=
\binom{R+g-e}{t}\binom tr.                         \tag{6.2}
$$

Thus every uncolored supersets-of-bases inequality obtained only by extending
the bases counted in Theorem 2.1 is already implied by the $r$-basis bound.
A successor must control which colored extensions actually occur, prove
additional low-dimensional concentration, or exploit the split-rational
equations themselves.

### Exact sharpness control

The independent Sage replay constructs a realized boundary family over
$\mathbf F_{17}$ with

$$
(n,K,a,R,w,L,r,g,e)=(14,12,12,2,0,90,12,12,0).    \tag{6.3}
$$

Let $S=\{0,\ldots,11\}$, $E=\{12,13\}$, and let $\ell_i$ be the
$S$-Lagrange basis.  The received word vanishes on $S$ and has values
$(1,6)$ on $E$.  For each $i$ and $y\in E$, the replay includes the unique
multiple of $\ell_i$ agreeing at $y$; for each $i<j$, it includes the unique
linear combination of $\ell_i,\ell_j$ agreeing at both points of $E$.
The chosen ratio avoids every singleton degeneracy.  This gives

$$
2a+\binom a2=90=\binom{14}{12}-1                \tag{6.4}
$$

distinct nonanchor codewords.  Their span has rank twelve, their locator
union has size twelve, and their degree histogram is 24 members of degree
one and 66 of degree two.  There are 78 distinct numerator locators, no
fixed-locator slice has more than two members, and all 4,005 Wronskian pairs
pass the exact split-rational compatibility test.  The first-pivot slack is
$12!=479,001,600$, while the $E_0$-marked inequality is an equality.  The
missing one of the 91 evaluation bases is exactly the excluded zero anchor.

The canonical family digest is

```text
2ed7462c2a4041ca893b39e194c1e6331751171c4cb982cd9625501ce05a10b9
```

This is an exact toy-scale falsification control, not deployed M31 evidence.
It shows that realizability alone cannot supply a uniform saving from the
marked-basis theorem.  At positive $w$, the genuinely additional condition
is that every error support represent one fixed Reed--Solomon syndrome.
That fixed-syndrome secant incidence is the declared unpaid terminal:
`UNPAID_RANK6_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE`.

## 7. Architecture and proof audit

The exact v4 values remain

$$
U_{\rm paid}=3,730,
\qquad
U_Q=U_{\rm list-int}=U_{\rm ext}=U_{\rm new}=\text{null}. \tag{7.1}
$$

This packet has

$$
\text{ledger movement}=0,
\qquad
\text{official endpoint movement}=0.               \tag{7.2}
$$

### Statement audited

The implication from the inherited evaluation-flat cap and agreement-block
split to the first-pivot, colored, cross-block, affine-line, and projective
ray inequalities, and their exact deployed specialization.

### Dependencies

- **PROVEN by sealed predecessors:** base-field boundary reconstruction,
  shallow-family cardinality, exact support identity, individual unit gates,
  common-zero identity, and the evaluation-flat cap.
- **PROVED here:** first-pivot, colored, cross-block, affine-line, and
  projective-ray inequalities; exact balanced pair incidences; ranks at most
  five excluded; the two-sided rank-six union interval; exhaustive exact
  excess envelopes; and the aggregate rank-six route cut.
- **COMPUTATIONAL CONTROL:** exhaustive tiny boundary families verify the
  inequalities; they do not prove a deployed incidence bound.
- **UNPROVEN:** every realized rank-six-or-higher split-rational upper, every
  source-bound owner exhaustion for this residual, and the M31 LIST row.

### Parameter dependence

All constants are exact functions of

$$
(p,n,K,a,R,w,L)=(2147483647,2097152,1048576,
1116023,981129,67447,15775933).                     \tag{7.3}
$$

There are no asymptotic constants and no hidden $T,Y,\mathcal L,
\mathcal L_{\bar I},\lambda,I$, or dyadic-level parameters.

### Layer-cake / moments

Layer-cake and dyadic summability are not used.  The moments in Section 5 are
deterministic split-support incidence inequalities; there is no Markov,
probabilistic Chebyshev, or moment optimization.

### Edge cases and notation

- Rank is the linear span rank after the zero boundary anchor is fixed.
- The first-pivot falling product is $1$ at rank one.
- A root of $H_i$ cannot be a common `E0` codeword zero because
  $\gcd(b_i,H_i)=1$.
- Positive $e$ strengthens both sides in the closing direction.
- The scalar profile in Section 5 is not a polynomial or support witness.
- The full shallow range first becomes uncut at rank twelve, not rank eleven.

### Numerical evidence

All deployed thresholds are exact integer specializations of proved
inequalities.  The all-`g` scan covers every one of the legal union sizes;
it is a finite arithmetic optimization, not sampled evidence.  The finite
field replay is toy-scale and is used only as a falsification control.

### Verdict

**GREEN locally / YELLOW globally.**  The first-pivot theorem and its exact
rank consequences are bankable after independent review.  The rank-six
scalar profile is a rigorous route cut on aggregate methods, not a realized
counterexample.  No global proof is authorized.

## 8. Maximal next action

Attack the realized rank-six component in the finite window

$$
781,458\le g\le1,033,227                            \tag{8.1}
$$

with the colored first-pivot theorem frozen.  The successor must classify
low-dimensional concentration of the `E0` evaluation columns or derive a
split-rational/Wronskian incidence inequality that is false for the scalar
profile (5.4)--(5.5).  Every exceptional component must terminate in a
source-certified paid owner with a proved chart multiplicity, or remain an
explicit unpaid primitive component.  Another uncolored
supersets-of-bases count is already cut by Section 6.  The current
first/second incidence gates and inherited global split-support moment also
do not close the scalar relaxation.  Any stronger moment or owner theorem
must print a new realized-family hypothesis that fails for profile (5.4).
