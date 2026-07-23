---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
architecture: M31_BASE_FIELD_BOUNDARY_RANK7_TRUNCATED_WEIGHT_FLAG_V1
parent_payload_sha256: 3e0a6102795f88aa8121229bc40bcc723aa7e5cc81bbcfd5b0013adf5d11caf9
atom_or_cell: Direct M31 boundary rank-seven diagnostic; no v4 atom value or owner payment.
direct_statement: Every reconstructed base-field boundary shallow family of affine codeword-span rank seven is excluded when its numerator-root union satisfies g<=72427 or g>=354999. Every survivor lies in 72428<=g<=354998 and satisfies explicit q1/q6 compiler-failure gates.
quantifier: Every subfamily of reconstructed base-field boundary shallow triples satisfying the common-unit theorem and the sealed rank-six predecessor.
projection_and_unit: Distinct actual base-field codewords per received word. Independent coordinate tuples and generalized-weight profiles are incidence witnesses only; every paid flank bounds the whole affine codeword chart.
claimed_bound: The common-zero Johnson compiler pays 67454<=g<=72427 and the truncated-weight codimension-one compiler pays 354999<=g<=1116023. The remaining rank-seven union interval has 282571 integer values and splits into an unpaid mixed-G near-MDS sliver and an unpaid fixed-G ordinary-RS-middle-or-mixed-G component.
status: PROVED_RANK7_TWO_FLANK_ROUTE_CUT_MIDDLE_OPEN
terminal: UNPAID_RANK7_MIXED_G_NEAR_MDS_LOCATOR_INCIDENCE / UNPAID_RANK7_FIXED_G_ORDINARY_RS_MIDDLE_OR_MIXED_G
impact: ROUTE_CUT
ledger_mode: DIRECT
partition_digest: DIRECT_ROUTE_NOT_APPLICABLE
falsifier: A reconstructed rank-seven family violating the truncated generalized-weight inequality; failure of an affine-fiber cap; failure of support saturation or the codimension-one parameter map; a surviving family outside 72428<=g<=354998; or promotion of a scalar weight profile to codewords.
replay: Exact Python big-integer and rational exhaustion over all 1048570 rank-seven union sizes, optimized parity, mutation tests, independent Sage arithmetic, predecessor replay, and fresh proof review.
---

# M31 rank-seven truncated-weight/flag route cut

## Status and exact scope

This packet takes the first complete stratum after the rank-six closure.  It
proves one rank-uniform theorem and then exhausts rank seven exactly.

For every `k<r`, independent agreement coordinates may be truncated before a
full basis is reached.  The residual coefficient fiber is an affine
`k`-flat, whose whole list is bounded by the already-proved affine-span
compiler.  Retaining the generalized Hamming weights before truncation gives
the all-rank inequality

$$
 \boxed{
 \sum_{i\in I}\prod_{j=k+1}^{r}
 (d_j-R+\eta+s_i)
 \le B_k(d_r)_{\underline{r-k}},
 }
 \qquad
 B_k=\left\lfloor
 {\binom{n-K+k}{k}\over\binom{w+k}{k}}
 \right\rfloor .                                  \tag{0.1}
$$

At rank seven, (0.1), common-zero Johnson, and the coset-free
codimension-one compiler prove

$$
 \boxed{g\le72,427\quad\hbox{or}\quad g\ge354,999
        \Longrightarrow |I|\le15,775,932.}         \tag{0.2}
$$

Consequently every surviving rank-seven family lies in the exact interval

$$
 \boxed{72,428\le g\le354,998.}                    \tag{0.3}
$$

The interval contains 282,571 integer union sizes.  It is not paid.  Its
lower 432 values require many moving locators after existing fixed-`G`
owners are removed; the rest contains the universal deterministic
post-Johnson ordinary-RS obstruction.  Rank eight and above also remain
open.  Thus this is a route cut, not rank-seven or row closure, and ledger
movement is zero.

## 1. Source-bound shallow family

The deployed integers are

$$
\begin{aligned}
p&=2^{31}-1=2,147,483,647, & n&=2,097,152,\\
K&=1,048,576, & a&=1,116,023,\\
R&=n-a=981,129, & w&=a-K=67,447,\\
B_*&=16,777,215.&&
\end{aligned}                                      \tag{1.1}
$$

The deep owner contributes at most 1,001,282.  Therefore a forbidden
boundary list supplies

$$
 L=15,775,933                                      \tag{1.2}
$$

distinct actual shallow nonanchor codewords for one received word, with
excesses `0<=s_i<=366886`.  The sealed predecessor at payload
`3e0a6102795f88aa8121229bc40bcc723aa7e5cc81bbcfd5b0013adf5d11caf9`
excludes ranks one through six.

Assume henceforth that

$$
 W_c=\operatorname{span}_{\mathbf F_p}\{c_i:i\in I\},
 \qquad \dim W_c=r\ge7.                            \tag{1.3}
$$

Let `g` be the numerator-root union size and let `eta` be the common
`E0` mismatch count.  The common-zero identity gives

$$
 d_r(W_c)=R+g-\eta.                                \tag{1.4}
$$

Write the generalized weights as

$$
 d_j=(n-K)+j+q_j,
 \qquad0\le q_1\le\cdots\le q_{r-1}.              \tag{1.5}
$$

Every object counted below is an actual codeword.  Tuple and weight counts
are used only to upper-bound whole affine codeword fibers.

## 2. Rank-uniform truncated generalized-weight compiler

### Theorem 2.1

For every integer `0<=k<r`, the shallow family satisfies (0.1).

### Proof

Represent evaluation on `W_c` by columns in `W_c^*`.  Zero columns are
exactly the common-zero coordinates.  A listed codeword `c_i` has

$$
 d_r-R+\eta+s_i=g+s_i                              \tag{2.1}
$$

agreement columns outside that common-zero set.

Suppose `t` independent agreement columns have been chosen.  Their span
annihilates an `(r-t)`-dimensional subcode.  That subcode has support at
least `d_{r-t}`, so at most `d_r-d_{r-t}` active columns lie in the old
span.  The number of extending agreement columns is therefore at least

$$
 d_{r-t}-R+\eta+s_i.                               \tag{2.2}
$$

Stop after `r-k` independent columns.  Multiplication of (2.1)--(2.2)
shows that word `i` owns at least

$$
 \prod_{j=k+1}^{r}(d_j-R+\eta+s_i)                 \tag{2.3}
$$

ordered independent tuples.

A fixed tuple cuts the affine coefficient space in an affine `k`-flat.
The proved recursive affine-span list compiler bounds the complete list in
that fiber by

$$
 B_k=\left\lfloor
 {\binom{n-K+k}{k}\over\binom{w+k}{k}}
 \right\rfloor.                                   \tag{2.4}
$$

There are at most `(d_r)_(r-k)` ordered active tuples.  Double counting
gives (0.1).  No affine coset is summed separately, and there is no field-
size factor.  \(\square\)

For rank seven the exact fiber caps are

| `k` | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| `B_k` | 1 | 15 | 241 | 3,757 | 58,410 | 908,021 | 14,115,528 |

The cases used to control `q_6` have `1<=k<=5`.  Dropping positive excess,
common mismatch, and lower `q_j` only in the weakening direction gives

$$
 q_6\le
 \min_{1\le k\le5}
 \left\{
 \left\lfloor
 {B_k(R+g)_{\underline{7-k}}
  \over
  Lg\prod_{j=k+1}^{5}(w+j)}
 \right\rfloor-(w+6)
 \right\}.                                        \tag{2.5}
$$

Strict generalized-weight growth independently gives

$$
 q_6\le g-w-7.                                    \tag{2.6}
$$

The verifier exhausts every integer `67454<=g<=1116023`.  Among the raw
caps in (2.5), `k=1` wins exactly through `g=76876`, and `k=5` wins from
`g=76877` onward; `k=2,3,4` never win.  After taking (2.6),

$$
 \boxed{q_6\le242,225},                            \tag{2.7}
$$

with equality possible in the scalar envelope only at
`g=309679,309680,309681`.  Hence

$$
 1,048,582\le d_6\le1,290,807.                    \tag{2.8}
$$

## 3. The low Johnson flank

At rank seven, let `N_7=d_7=R+g-eta`.  The common-zero Johnson compiler has

$$
 h=g,
 \qquad
 \alpha=d_7-d_1=g-w-1-\eta-q_1.                  \tag{3.1}
$$

Positive `eta` and `q_1` improve the bound.  The weakest specialization is
`eta=q_1=0`, where

$$
 J_7(g)=
 \left\lfloor
 {(R+g)(w+1)
  \over
  g^2-(R+g)(g-w-1)}
 \right\rfloor                                    \tag{3.2}
$$

when the denominator is positive.  Exact exhaustion gives

$$
 J_7(72,427)=4,735,771<L,                          \tag{3.3}
$$

while the denominator at `g=72428` is `-898676`.  Thus all legal union
sizes through 72,427 are excluded and this compiler has no positive
denominator at the next integer.

Inside the residual, Johnson still pays profiles with sufficiently large
`q_1`.  Put

$$
 D_0(g)=g^2-(R+g)(g-w-1).                          \tag{3.4}
$$

The least paying value is

$$
 q_J(g)=\max\left\{0,
 \left\lfloor
 {(R+g)(w+1)-L D_0(g)
  \over (L-1)(R+g)}
 \right\rfloor+1\right\}.                         \tag{3.5}
$$

Every survivor therefore satisfies `q_1<q_J(g)`.  In particular,

$$
 q_J(72,428)=1,
 \quad q_J(72,858)=374,
 \quad q_J(72,859)=375.                            \tag{3.6}
$$

At the first residual union, the minimum distance is forced to its exact
generalized-Singleton value `q_1=0`.

## 4. The high codimension-one flank

Choose a six-dimensional `d_6`-minimizing subcode `V<W_c`.  It is support-
saturated.  The exact map into the proved MDS-soft codimension-one compiler
is

| compiler symbol | rank-seven packet |
|---|---|
| `j` | 6 |
| `m` | `a=K+w` |
| `t=n-m` | `R` |
| hyperplane support `d` | `d_6(W_c)` |
| support layer `e` | `d_7-d_6` |
| outside common mismatch `b_0` | `eta` |

At `eta=0`, its profile is

$$
 \Pi_b=(d-R+b)\prod_{i=1}^{5}(w+i+b),
 \qquad Q=w+1.                                    \tag{4.1}
$$

The sufficient profile-interpolation margin is

$$
 5Q-(d-R)
 \ge269,787-q_6
 \ge27,562>0.                                     \tag{4.2}
$$

Thus interpolation is uniformly authorized.  With `e=R+g-d`, the whole
rank-seven chart obeys

$$
 C_7(g,d)=\left\lfloor
 {d_{\underline6}
  \over(d-R)\prod_{i=1}^{5}(w+i)}
 +
 {d_{\underline7}
  \over(w+1)g\prod_{i=1}^{5}(w+i+e)}
 \right\rfloor.                                   \tag{4.3}
$$

This is a whole-chart count, not a per-coset estimate.

The `d` optimization does not assume that the sum in (4.3) is monotone.
Call its two rational terms `T_0,T_1`.  Exact adjacent ratios show that
`T_0` decreases through

$$
 d_*=1,177,354                                     \tag{4.4}
$$

and increases thereafter, while `T_1` increases everywhere.  Therefore:

- on `[d_6^{min},d_*]`, use the safe separate majorant
  `T_0(d_6^{min})+T_1(d_*,g)`;
- on `[d_*,d_6^{max}(g)]`, both terms are increasing, so use the right
  endpoint.

Exhausting all legal `g` and their exact `q_6` caps gives

$$
\begin{array}{c|r|r}
g&\text{low-piece majorant}&\text{whole-chart majorant}\\ \hline
354,998&14,336,564&15,776,141,\\
354,999&14,336,558&15,775,924.
\end{array}                                        \tag{4.5}
$$

The first value exceeds the required family by 208, while the second is
nine below it.  Every larger union is also paid.  This proves the high
flank in (0.2).

## 5. Exact first-match residual

Apply the following order:

1. common-zero Johnson;
2. truncated-weight codimension-one;
3. fixed-`G` Johnson or the already-proved endpoint peeling owner;
4. mixed-`G` near-MDS terminal;
5. fixed-`G` ordinary-RS-middle-or-mixed-`G` terminal.

The first two owners leave exactly (0.3).  More precisely, a primitive
profile satisfies

$$
\begin{gathered}
r=7,
\qquad72,428\le g\le354,998,\\
0\le q_1\le q_6\le Q_6(g),
\qquad q_1<q_J(g),\\
C_7(g,d_6)\ge15,775,933.                           \tag{5.1}
\end{gathered}
$$

### Low mixed-locator sliver

For one fixed locator of degree `m`, restriction to `E0` is an ordinary
`RS(R,m-w)` list.  For `m<=72858`, its exact Johnson cap is

$$
 J_G(m)=\left\lfloor
 {R(w+1)\over m^2-R(m-w-1)}
 \right\rfloor.                                   \tag{5.2}
$$

The existing agreement-shortening endpoint theorem gives cap 2,310,492 at
`m=72859`.  Consequently every fixed-`G` slice is paid throughout
`72428<=g<=72859`.  Any surviving family must use at least

$$
\begin{array}{c|r|r}
g&\text{largest fixed-}G\text{ cap}&\text{distinct }G\text{ required}\\ \hline
72,428&183&86,208,\\
72,858&174,019&91,\\
72,859&2,310,492&7.
\end{array}                                        \tag{5.3}
$$

This is the terminal

```text
UNPAID_RANK7_MIXED_G_NEAR_MDS_LOCATOR_INCIDENCE.
```

The cross-block inequality does not pay it: before fixed-`G` ownership,
`m_i=g` has zero cross-block cost, and after that slice is removed the
`m_i=g-1` branch still has enormous slack.

### Deterministic ordinary-RS middle

For

$$
 72,860\le g\le354,998,                            \tag{5.4}
$$

the full-union fixed-`G` slice has ordinary-RS dimension

$$
 5,413\le d=g-w\le287,551.                         \tag{5.5}
$$

This lies inside the proved universal fixed-`G` obstruction
`5413<=d<=840822`.  A valid successor cannot assume that the locators vary:
the fixed-`G` adapter embeds arbitrary deterministic punctured-RS received
words after one common translation.  The terminal is

```text
UNPAID_RANK7_FIXED_G_ORDINARY_RS_MIDDLE_OR_MIXED_G.
```

Closing rank seven therefore requires both a deterministic rank-seven
post-Johnson ordinary-RS theorem and a source-bound mixed-locator incidence
theorem, or one theorem that handles both without using locator variation.

## 6. Audit and nonclaims

- **Proved here:** the rank-uniform truncated generalized-weight inequality,
  exact rank-seven `q_6` envelope, uniform profile interpolation, and both
  paid flanks.
- **Imported:** source reconstruction, shallow/deep split, ranks one through
  six, affine-fiber caps, support saturation, common-zero Johnson,
  codimension-one recursion, fixed-`G` embedding, and endpoint peeling.
- **Exact computation:** all displayed deployed transitions are exhaustive
  integer/rational specializations of proved formulas.
- **Unproved:** the two primitive rank-seven terminals, every rank at least
  eight, and the complete M31 row.
- **Numerical evidence:** no random or asymptotic experiment is used.  Exact
  scans certify finite inequalities; they do not construct codeword
  families.
- **Layer cake / dyadic summability:** not applicable.
- **Moment / Markov / Chebyshev:** not applicable.  “Chebyshev” elsewhere
  names the evaluation domain, not a probabilistic inequality.
- **Ledger:** movement zero; no official endpoint or score moves.

The next maximal theorem is now falsifiable: every reconstructed rank-seven
family satisfying (5.1) and the canonical common-`V` Wronskian gates has at
most 15,775,932 members.  Its first-match proof must pay the fixed-`G`
ordinary-RS middle and the mixed-`G` near-MDS incidence separately, or emit
an actual primitive component without forcing an owner.

## Replay

From the repository root:

```bash
python3 experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_v1.py --check
python3 -O experimental/scripts/verify_m31_rank7_truncated_weight_flag_route_cut_v1.py --check
```
