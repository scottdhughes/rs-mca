---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
direct_statement: Every realized base-field boundary shallow family obeys an excess-weighted affine-span basis inequality; ranks at most four are impossible at the forced shallow cardinality. Separately, agreement-shortening and error-puncturing close the two endpoint rows of the fixed-G post-Johnson interval.
architecture: M31_BASE_FIELD_BOUNDARY_AFFINE_SPAN_SHORTENING_V1
parent_payload_sha256: 006cde59ee0a9fc23f8f13c3dc9955c26732bdee86b4af943f06fffeb5dd572e
atom_or_cell: Direct M31 boundary diagnostic and ordinary-LIST route cut; no v4 atom value or owner payment.
quantifier: Every reconstructed base-field boundary family of canonical shallow triples satisfying the common-unit theorem, and every received table in the fixed-G ordinary RS subclass at the two stated endpoints.
projection_and_unit: Distinct nonanchor codewords per received word. The affine-span inequality counts codewords by full-rank evaluation coordinate sets, not supports or locator labels.
claimed_bound: Exact route cuts only. The deployed row, ranks at least seven, and the residual deterministic fixed-G middle interval remain open. Ledger movement is zero.
status: PROVED_AFFINE_RANK4_AND_FIXED_G_ENDPOINT_ROUTE_CUTS_HIGH_RANK_OPEN
impact: ROUTE_CUT
falsifier: A reconstructed family violating the basis inequality; a shallow family of size 15775933 and affine rank at most four; an endpoint ordinary RS list exceeding the displayed cap; or any use of the toy census or route cuts as a global list bound.
replay: Standard-library big integers, an independent Sage integer replay, an exhaustive five-cell Sage census, hostile mutations, predecessor payload pins, and fresh proof review.
---

# M31 varying-G affine-span and fixed-G endpoint route cuts

## Status and exact scope

This packet advances both live branches of the Mersenne-31 boundary problem,
but closes neither one globally.

First, it proves an exact varying-`G` inequality for every *realized* shallow
family reconstructed by the common-unit CRT theorem.  The inequality excludes
affine ranks one through four, sharply localizes ranks five and six, and gives
weighted excess ceilings through rank ten.  Rank seven and above remain live;
rank eleven already escapes the uniform weighted cut over the whole shallow
range.

Second, it closes the two endpoint rows of the fixed-`G` ordinary
Reed--Solomon interval by one-coordinate peeling.  The exact unresolved
fixed-`G` interval therefore becomes

$$
72,860\le m\le 908,269,
\qquad
5,413\le d=m-w\le840,822.                         \tag{0.1}
$$

These are route cuts.  They do not prove
`#X(V)<=16,777,214`, do not fill a Grande Finale v4 atom, and do not change an
official endpoint or score.

## 1. Boundary family and inherited shallow reduction

The deployed integers are

$$
\begin{aligned}
p&=2^{31}-1=2,147,483,647,\\
n&=2,097,152, &K&=1,048,576,\\
a&=1,116,023, &R&=981,129,\\
w&=a-K=67,447, &B_*&=16,777,215.
\end{aligned}                                      \tag{1.1}
$$

Write the pinned evaluation domain as

$$
D=S_0\mathbin{\dot\cup}E_0,
\qquad |S_0|=a,\quad |E_0|=R,                      \tag{1.2}
$$

and let `A0` and `L0` be the respective split locators.  The sealed parent
packet proves that any forbidden boundary list has a subfamily of

$$
L=15,775,933                                      \tag{1.3}
$$

distinct nonanchor codewords with shallow excess

$$
0\le s_i\le366,886.                                \tag{1.4}
$$

For every member there are canonical polynomials

$$
G_i\mid A_0,\qquad
c_i={A_0\over G_i}b_i,\qquad
H_i=\gcd(L_0,G_i-b_iV),                            \tag{1.5}
$$

where `V` is one common unit modulo `L0`, `G_i` is monic and split on `S0`,
`H_i` is monic and split on `E0`,

$$
m_i=\deg G_i,qquad
\deg H_i=m_i+s_i,qquad
\deg b_i<m_i-w,                                   \tag{1.6}
$$

and the reconstructed received word `U` is zero on `S0` and nonzero on
`E0`.  The exact agreement support of `c_i` is

$$
(S_0\setminus Z(G_i))\mathbin{\dot\cup}Z(H_i),     \tag{1.7}
$$

of size `a+s_i`.

The common-unit theorem, including the individual denominator-unit gates,
is a dependency.  This packet does not replace those gates by pairwise
support conditions alone.

## 2. Varying-G affine-span basis inequality

Let

$$
W_c=\operatorname{span}_{\mathbf F_p}\{c_i:i\in I\},
\qquad r=\dim W_c,                                 \tag{2.1}
$$

and define

$$
g=\left|\bigcup_i Z(G_i)\right|,
\qquad
e=\left|E_0\cap\bigcap_i Z(b_i)\right|.            \tag{2.2}
$$

Here `g` is a union cardinality, not `sum_i deg(G_i)`, and `r` is linear
rank after adjoining the zero boundary anchor, not the number of distinct
locators.

### Theorem 2.1 (excess-weighted basis inequality)

Every reconstructed family above satisfies

$$
\boxed{
\sum_{i\in I}\binom{w+s_i+r+e}{r}
\le \binom{R+g-e}{r}.}                             \tag{2.3}
$$

It also satisfies

$$
g-e\ge w+r.                                        \tag{2.4}
$$

### Proof

Let `Z(W_c)` denote the common zero set of all polynomials in `W_c` on `D`.
At a point of `S0`, the squarefree factorization of `A0`, the divisibility
`G_i|A0`, and `gcd(G_i,b_i)=1` show

$$
c_i(x)=0\quad\Longleftrightarrow\quad x\notin Z(G_i).
$$

At a point of `E0`, both `A0` and `G_i` are nonzero, so

$$
c_i(x)=0\quad\Longleftrightarrow\quad b_i(x)=0.
$$

Consequently

$$
|Z(W_c)|=z=a-g+e.                                  \tag{2.5}
$$

If `f_1,...,f_r` is a basis of `W_c`, their common polynomial factor has
degree at least `z`.  Dividing by it leaves `r` independent polynomials of
degree less than `K-z`; hence `K-z>=r`.  This proves

$$
z\le K-r,                                          \tag{2.6}
$$

which is equivalent to (2.4).

For every `x` outside `Z(W_c)`, form the nonzero evaluation column

$$
v_x=(f_1(x),\ldots,f_r(x))\in\mathbf F_p^r.         \tag{2.7}
$$

If a `j`-dimensional subspace `Q` of `F_p^r` contains `t` such columns, its
annihilator gives `r-j` independent polynomials in `W_c` vanishing at those
`t` coordinates and at all `z` common zeros.  The same factor-dimension
argument gives

$$
t+z\le K-(r-j),
\qquad t\le K-r+j-z.                               \tag{2.8}
$$

By (1.7), `c_i` agrees with `U` at `a+s_i` coordinates.  Exactly `a-g` of
these are common-zero coordinates in `S0`; none of the `e` common zeros in
`E0` is an agreement because `U` is nonzero there.  Thus `c_i` has
`g+s_i` agreement columns outside `Z(W_c)`.

Choose an ordered column basis greedily from those agreement columns.  After
`j` independent choices, (2.8) leaves at least

$$
g+s_i-(K-r+j-z)=w+s_i+r+e-j                       \tag{2.9}
$$

choices for the next column.  Dividing the product over `j=0,...,r-1` by
`r!` shows that `c_i` owns at least

$$
\binom{w+s_i+r+e}{r}                               \tag{2.10}
$$

unordered full-rank coordinate sets.

A full-rank `r`-coordinate set owns at most one `c_i`: its agreement
equations with the fixed received word `U` uniquely determine the
coefficient vector of a polynomial in `W_c`.  The number of candidate
coordinate sets outside the common zero set is

$$
\binom{n-z}{r}=\binom{R+g-e}{r}.                   \tag{2.11}
$$

Double counting proves (2.3).  This last uniqueness step is why (2.3)
counts codewords rather than supports.  ∎

## 3. Exact affine-rank consequences

Set all `s_i=0`, take the weakest `e=0`, and maximize the right side at
`g=a`.  Then (2.3) gives

$$
L\le {\binom nr\over\binom{w+r}{r}}.               \tag{3.1}
$$

The exact floors for ranks one through four are

$$
31,\qquad966,\qquad30,058,\qquad934,551.           \tag{3.2}
$$

All are below (1.3), so every forbidden shallow family has

$$
\boxed{r\ge5}.                                     \tag{3.3}
$$

At rank five the first numerator-union size not excluded by the zero-excess
bound is

$$
g=874,886,                                         \tag{3.4}
$$

with adjacent caps

$$
15,775,899\quad\hbox{and}\quad15,775,941.          \tag{3.5}
$$

At rank six it is

$$
g=87,070,                                          \tag{3.6}
$$

with adjacent caps

$$
15,775,873\quad\hbox{and}\quad15,775,962.          \tag{3.7}
$$

Thus rank five requires `g>=874,886`, and rank six requires `g>=87,070`.
The zero-excess inequality alone permits every rank at least seven.

For additional localization, retain `s_i` and again use the weakest
`g=a,e=0`.  The function

$$
s\longmapsto\binom{w+s+r}{r}                       \tag{3.8}
$$

is discretely convex.  Among integer vectors with a fixed total excess, its
sum is minimized by entries differing by at most one.  Exact integer
optimization of (2.3) therefore gives

| rank `r` | base excess `q` | entries at `q+1` | maximum `sum_i s_i` |
|---:|---:|---:|---:|
| 5 | 8,763 | 3,950,411 | 138,248,451,290 |
| 6 | 64,972 | 8,496,922 | 1,025,002,415,798 |
| 7 | 129,040 | 11,542,946 | 2,035,737,937,266 |
| 8 | 196,716 | 3,995,011 | 3,103,382,431,039 |
| 9 | 265,094 | 1,499,656 | 4,182,106,682,358 |
| 10 | 332,335 | 3,785,452 | 5,242,898,479,007 |

At rank eleven, all `L` entries may equal the full shallow ceiling `366,886`
without violating this worst-case inequality.  Hence (2.3) is a genuine
route cut, not a closure of the high-rank component.

## 4. Incidence lemma used for endpoint peeling

### Lemma 4.1

Let `N` subsets of a `v`-point universe each have size `q0`, with pairwise
intersection at most `lambda`.  If

$$
\Delta=q_0^2-v\lambda>0,                           \tag{4.1}
$$

then

$$
N\le\left\lfloor
{v(q_0-\lambda)\over\Delta}
\right\rfloor.                                    \tag{4.2}
$$

### Proof

If `d_x` is the number of sets containing `x`, then

$$
Nq_0=\sum_xd_x,
\qquad
\sum_x\binom{d_x}{2}\le\lambda\binom N2.          \tag{4.3}
$$

Cauchy--Schwarz gives `sum_x d_x^2 >= N^2q_0^2/v`.
Substitution into (4.3), followed by rearrangement using `Delta>0`, gives
(4.2).  ∎

For an ordinary `RS(E0,d)` list, chosen agreement sets have pairwise
intersection at most `d-1`, since two distinct degree-less-than-`d`
polynomials agree in at most `d-1` positions.

## 5. Lower fixed-G endpoint

Take

$$
m=72,859,
\qquad d=m-w=5,412.                                \tag{5.1}
$$

For every listed polynomial `f`, choose exactly `m` agreement coordinates.
For a chosen agreement coordinate `x`, shorten by

$$
f_x(Y)={f(Y)-r(x)\over Y-x},
\qquad
r_x(y)={r(y)-r(x)\over y-x}.                       \tag{5.2}
$$

For fixed `x`, this map is injective and produces an
`RS(981128,5411)` list at agreement `72858`.  Lemma 4.1 has

$$
\lambda=5,410,qquad
\Delta=72,858^2-981,128\cdot5,410=385,684,         \tag{5.3}
$$

and gives the exact local cap

$$
\left\lfloor{981,128\cdot67,448\over385,684}\right\rfloor
=171,578                                           \tag{5.4}
$$

with remainder `231,992`.  Double counting selected pairs `(f,x)` gives

$$
L\cdot72,859\le981,129\cdot171,578,
$$

hence

$$
\boxed{L\le2,310,492}.                             \tag{5.5}
$$

The margin below `B_*-1=16,777,214` is `14,466,722`.

## 6. Upper fixed-G endpoint

Take

$$
m=908,270,
\qquad d=m-w=840,823.                              \tag{6.1}
$$

Split the list into the exact-agreement shell and the higher-agreement tail.
Every exact-shell word has exactly

$$
R-m=72,859                                         \tag{6.2}
$$

error coordinates.  Puncturing one selected error coordinate preserves all
`m` agreements and remains injective, because `R-1>=d`.  Lemma 4.1 for the
punctured `RS(981128,840823)` list again has `Delta=385,684` and local cap
`171,578`.  Error-incidence double counting therefore gives

$$
L_{\rm shell}\le2,310,492.                         \tag{6.3}
$$

For the tail at agreement at least `908,271`, the unpunctured incidence
denominator is

$$
908,271^2-981,129\cdot840,822=1,361,403,           \tag{6.4}
$$

and Lemma 4.1 gives

$$
L_{\rm tail}\le
\left\lfloor{981,129\cdot67,449\over1,361,403}\right\rfloor
=48,608.                                           \tag{6.5}
$$

Thus

$$
\boxed{L\le2,359,100},                             \tag{6.6}
$$

with margin `14,418,114` below the required cap.

The shell/tail split is load-bearing.  Error puncturing is asserted only on
the exact shell; applying it to a word with unknown extra agreements would
not supply the uniform error-incidence multiplicity used in (6.3).

## 7. Sharp stopping point of this peeling method

At the adjacent lower row `(m,d)=(72860,5413)`, shortening on `s` selected
agreement coordinates has

$$
\Delta_s=-1,290,548+840,821s.                      \tag{7.1}
$$

It first becomes positive at `s=2`.  Pulling the local bound back by

$$
L\binom ms\le\binom Rs J_s                        \tag{7.2}
$$

gives the exact ceilings

| `s` | ceiling |
|---:|---:|
| 2 | 30,682,450 |
| 3 | 131,171,396 |
| 4 | 1,049,845,524 |
| 5 | 10,057,621,549 |
| 6 | 105,113,431,231 |

For `7<=s<=d-1`, each factor in

$$
{\binom Rs\over\binom{72,860}s}
$$

exceeds `R/72860>13`, and `13^7=62,748,517>B_*-1`; the local incidence cap is
at least one.  For `s>=d`, the selected agreements already determine at most
one degree-less-than-`d` polynomial, but the same binomial pullback ratio is
still larger than the target.  Thus no larger `s` closes this row by the same
method.

At the adjacent upper exact shell `(m,d)=(908269,840822)`, puncturing `s`
of its `72860` error coordinates yields the identical denominator, local
cap, and pullback sequence throughout the shared incidence range; the same
ratio obstruction handles every larger `s`.  The method therefore stops
exactly at (0.1).
This is a sharpness statement for this peeling-plus-incidence route, not a
lower bound on the true list size.

## 8. Exhaustive toy varying-G control

The companion Sage scanner exhausts every legal split `G`, split shallow
`H`, coefficient vector `b`, and unit table `V` in five tiny cells.  It
separately computes abstract compatibility cliques, fixed-`G` cliques,
mixed-`G` cliques, and actual reconstructed codeword families.

| cell | abstract | fixed `G` | mixed `G` | realized |
|---|---:|---:|---:|---:|
| `GF(5),a=2,R=2,w=0,s=0` | 5 | 2 | 5 | 5 |
| `GF(5),a=3,R=2,w=1,s=0` | 1 | 1 | 0 | 1 |
| `GF(7),a=3,R=3,w=1,s=0` | 3 | 1 | 3 | 3 |
| `GF(7),a=3,R=3,w=1,s<=1` | 3 | 1 | 3 | 3 |
| `GF(7),a=4,R=2,w=0,s<=1` | 14 | 2 | 14 | 14 |

The final realized witness has 14 nonanchors, 15 codewords after the zero
anchor add-back, and ten distinct `G` locators.  This is exact toy evidence
that a fixed-`G` maximum is not a valid proxy for the varying-`G` census.
It is not deployed-scale evidence and proves no asymptotic growth law.

## 9. Ledger and successor

The ledger movement is exactly zero:

```text
U_paid     = 3730 (parent, unchanged)
U_Q        = null
U_list-int = null
U_ext      = null
U_new      = null
```

The varying-`G` residual is now forced into affine rank at least five.  Ranks
five and six carry the exact union/excess thresholds in Section 3; ranks
seven through ten carry only weighted-excess restrictions; rank eleven and
above is the primitive high-rank component.  The fixed-`G` subclass still
requires a uniform deterministic ordinary-RS theorem throughout (0.1).

The combined live terminal is

```text
UNPAID_HIGH_AFFINE_RANK_SPLIT_RATIONAL_INCIDENCE
```

The maximal successor theorem must couple high affine rank to the split
numerator/divisor geometry or route it to an exhaustive source-bound owner.
Another fixed-locator count, common-unit reconstruction, pairwise CRT lemma,
or Johnson moment cannot discharge that component.

## 10. Proof audit

### Statement audited

The implication from a reconstructed shallow common-unit boundary family to
the weighted basis inequality (2.3), together with the two one-coordinate
fixed-`G` endpoint bounds.

### Dependencies

- **PROVEN by sealed predecessors:** boundary-anchor reconstruction, exact
  support identity, shallow/deep split, individual unit gates, and pairwise
  CRT sufficiency below `p-1`.
- **PROVED here:** common-zero identity, polynomial-subspace root bound,
  evaluation-column flat bound, basis double count, incidence lemma, endpoint
  shortening/puncturing bounds, and exact method-stopping arithmetic.
- **PROVED COMPUTATIONALLY at toy scale only:** the five finite-field census
  rows in Section 8.
- **UNPROVEN:** the high-rank varying-`G` theorem, the deterministic fixed-`G`
  middle theorem, and the complete M31 row.

### Parameter dependence

Every numerical consequence is exact at (1.1), (1.3), and (1.4).  There are
no asymptotic constants and no hidden `T`, `Y`, `L_barI`, `lambda`, `I`, or
dyadic-level parameters.

### Layer-cake / dyadic summability

Not applicable.

### Moment / Markov / Chebyshev

No probabilistic moment, Markov, or Chebyshev inequality is used.
“Chebyshev” elsewhere in the M31 project refers to the pinned domain, not to
this proof.  Lemma 4.1 is a deterministic finite incidence second moment.

### Edge cases / notation

- Rank means linear rank of codewords with the zero anchor fixed.
- Common `E0` codeword zeros are nonagreements because the boundary received
  word is a unit there.
- The common-root dimension argument uses strict degree `<K`.
- Agreement shortening selects actual agreement coordinates separately for
  each word; error puncturing is restricted to an exact-agreement shell.
- `B_*-1=16,777,214` is the fixed-`G` nonanchor cap; it is not `B_*`.
- Convex excess ceilings use `g=a,e=0`, the weakest uniform specialization.

### Numerical evidence

All deployed integers are exact big-integer consequences of proved formulas
and are independently replayed by Python and Sage.  Only Section 8 is a
finite experimental census; its five cells total 40,010 explicit checks.

### Verdict

**GREEN locally / YELLOW globally — independently reviewed route cuts; global
row unresolved.**  A fresh proof audit found no blocking mathematical defect,
and the local affine-span and endpoint lemmas are bankable.  No global proof
or ledger payment is authorized by this packet.

### Remaining risks

- The high-affine-rank branch may contain a genuine primitive family.
- Rank five and six thresholds do not themselves provide owners.
- No uniform theorem currently controls all deterministic deployed
  puncturings in the fixed-`G` middle interval.
- Tiny mixed-`G` amplification cannot be extrapolated quantitatively.

### Maximal next action

Construct one source-bound high-rank dichotomy for the reconstructed shallow
family: either a rank-`r` component pays through its exact basis/excess
deficit and split-locator union, routes to a named quotient/periodic owner,
or emits an explicit primitive counterexample template.  In parallel, the
fixed-`G` middle must be attacked by a Chebyshev-specific higher-order
intersection theorem, not another Johnson calculation.
