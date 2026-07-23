---
workboard_item: M1/L
row: Mersenne-31 list at 2^-100
object: LIST
target_epsilon: 2^-100
agreement: 1116023
B_star: 16777215
architecture: M31_BASE_FIELD_BOUNDARY_RANK6_WEIGHT_HIERARCHY_CODIM_ONE_COMPILER_V1
parent_payload_sha256: 28f18608d3552ffe42e6dc8fcb6c03c1338fd349e1d52a0a3f52de6629bcbf6b
atom_or_cell: Direct M31 boundary diagnostic; no v4 atom value or owner payment.
direct_statement: Every reconstructed base-field boundary shallow family of affine codeword-span rank six is contained in a whole affine chart of size at most 908116.
quantifier: Every subfamily of reconstructed base-field boundary shallow triples satisfying the common-unit theorem and the parent rank-six window.
projection_and_unit: Distinct actual base-field codewords per received word. Ordered independent evaluation five-tuples are incidence witnesses only; the codimension-one compiler counts the whole codeword chart.
claimed_bound: A reconstructed shallow family of affine codeword-span rank six lies in a whole affine chart of size at most 908116, contradicting the required 15775933 members. Therefore every forbidden shallow family has rank at least seven.
status: PROVED_BASE_FIELD_BOUNDARY_SHALLOW_RANK6_EXCLUDED_RANK_GE7_OPEN
terminal: UNPAID_RANK_GE7_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE
impact: ROUTE_CUT
ledger_mode: DIRECT
partition_digest: DIRECT_ROUTE_NOT_APPLICABLE
falsifier: A reconstructed rank-six family violating the generalized marked-line inequality; a d5-minimizing hyperplane that is not support-saturated; failure of b0=eta; failure of the imported codimension-one hypotheses; or a whole rank-six chart with more than 908116 listed codewords.
replay: Exact Python big-integer and rational arithmetic, independent Sage arithmetic and exhaustive GF(7) source control, hostile mutations, predecessor replay, and fresh proof review.
---

# M31 rank-six generalized-weight/codimension-one closure

## Status and exact scope

This packet closes the rank-six branch left by the marked-basis predecessor.
It uses two source-compatible facts together:

1. the affine-line marked-basis count can retain the actual generalized
   Hamming weights of the hypothetical six-dimensional codeword span; and
2. a generalized-weight-minimizing hyperplane is support-saturated, so the
   proved two-resource codimension-one compiler counts its whole affine chart
   without a field-size or coset factor.

The exact conclusion is

$$
|{c in W_c : agr(U,c) >= a}| <= 908,116.             (0.1)
$$

The inherited shallow family has 15,775,933 distinct actual codewords in
that chart. Thus affine codeword-span rank six is impossible, and every
forbidden shallow family has rank at least seven.

This is a direct-route closure of one rank stratum. It does not prove the
complete M31 LIST bound, close any rank at least seven, or move a Grande
Finale v4 ledger atom. The successor terminal is
`UNPAID_RANK_GE7_SPLIT_RATIONAL_FIXED_SYNDROME_INCIDENCE`.

## 1. Inherited source-bound family

The deployed integers are

$$
p=2^31-1=2,147,483,647,
n=2,097,152,
K=1,048,576,
a=1,116,023,
R=n-a=981,129,
w=a-K=67,447,
B_*=16,777,215.                                      (1.1)
$$

In particular,

$$
n=2K,  R+w=n-K=K.                                   (1.2)
$$

The sealed predecessor at payload
`28f18608d3552ffe42e6dc8fcb6c03c1338fd349e1d52a0a3f52de6629bcbf6b`
proves the following implication. If a forbidden boundary list exists, it
contains a shallow family I of

$$
L=15,775,933                                         (1.3)
$$

distinct nonanchor base-field codewords, all for one received word U, with
excesses 0 <= s_i <= 366,886. After translating the zero anchor, write

$$
W_c=span_Fp{c_i : i in I},  r=dim(W_c).              (1.4)
$$

For rank six the predecessor also proves

$$
781,458 <= g <= 1,033,227,                           (1.5)
$$

where g is the numerator-root union size. Let eta be the common
denominator-zero count on E_0. We use eta, rather than the predecessor's e,
because the imported codimension-one theorem calls its new support-layer
length e. The common-zero set of W_c has size

$$
z=a-g+eta,                                           (1.6)
$$

so the full support of a rank-six span is

$$
d_6(W_c)=n-z=R+g-eta.                               (1.7)
$$

Every unit in this section is an actual distinct codeword. No abstract
support, marked key, scalar profile, syndrome representation, or locator is
being substituted for a codeword.

## 2. Generalized-weight marked-line refinement

Let d_j=d_j(W_c) be the generalized Hamming weights of W_c. Put

$$
d_j=(n-K)+j+q_j,  1 <= j <= 6.                      (2.1)
$$

The generalized Singleton lower bound and strictness of generalized weights
give

$$
0 <= q_1 <= q_2 <= q_3 <= q_4 <= q_5.              (2.2)
$$

### Theorem 2.1 (generalized-weight marked-line inequality)

Every reconstructed rank-six shallow family obeys

$$
sum_i (g+s_i) prod_{j=2}^5 (w+eta+j+q_j+s_i)
 <= 15 (R+g-eta)_{falling 5}.                       (2.3)
$$

### Proof

Represent evaluation on W_c by one column in its six-dimensional dual at
each domain coordinate. The zero columns are exactly the z common-zero
coordinates. Fix a listed word c_i. It has exactly g+s_i agreement
coordinates outside the common-zero set.

Choose an ordered independent five-tuple of those agreement columns. Suppose
k in {1,2,3,4} independent columns have already been chosen. Their span has
an annihilator of dimension 6-k in W_c. That annihilator subcode has support
at least d_{6-k}. Consequently at most

$$
n-d_{6-k}-z=d_6-d_{6-k}                             (2.4)
$$

active columns lie in the old span. The number of extending agreement
columns is therefore at least

$$
g+s_i-(d_6-d_{6-k})
 =w+eta+s_i+6-k+q_{6-k}.                            (2.5)
$$

Multiplying (2.5) for k=1,2,3,4, together with the free first agreement
coordinate, gives the summand in (2.3).

An independent five-tuple cuts the six-dimensional coefficient space in an
affine line. The predecessor's source-compatible affine-line theorem gives

$$
floor((n-K+1)/(w+1))=floor(1,048,577/67,448)=15.     (2.6)
$$

There are at most (d_6)_{falling 5} ordered active five-tuples, and each
fixed tuple owns at most fifteen listed codewords. Summing proves (2.3).
Different tuples may define the same affine line, but this does not create a
duplicate-owner problem: the multiplicity bound is applied to each fixed
tuple.

## 3. Exact q_5 and d_5 windows

Drop s_i, q_2, q_3, q_4, and eta from (2.3) only in the weakening direction.
Every rank-six family must satisfy

$$
L g (w+2)(w+3)(w+4)(w+5+q_5)
 <= 15 (R+g)_{falling 5}.                           (3.1)
$$

For F(g)=(R+g)_{falling 5}/g, the adjacent ratio is at least one exactly
when

$$
4(g+1) >= R.                                        (3.2)
$$

At g=781,458 the margin is 2,144,707. Thus F is increasing throughout
(1.5), and the weakest endpoint is g=1,033,227. There

$$
B_q=L g(w+2)(w+3)(w+4)
   =5,001,919,080,889,225,518,537,772,050,           (3.3)
$$

$$
N_q=15(R+g)_{falling 5}
   =497,473,825,631,213,850,211,072,067,356,800,     (3.4)
$$

and exact Euclidean division gives

$$
N_q=99,456 B_q
 +2,961,522,295,037,039,379,410,352,000.             (3.5)
$$

Since w+5=67,452,

$$
q_5 <= 32,004.                                      (3.6)
$$

The exact slack at q_5=32,005 is

$$
-2,040,396,785,852,186,139,127,420,050.             (3.7)
$$

Therefore

$$
1,048,581 <= d_5(W_c) <= 1,080,585.                (3.8)
$$

The Python replay exhausts every one of the 251,770 integer union sizes in
(1.5), rather than testing only the printed endpoints.

## 4. Exact codimension-one compiler map

Choose a five-dimensional subcode V<W_c with support size
d=|supp(V)|=d_5(W_c). A generalized-weight minimizer is support-saturated:

$$
V={v in W_c : supp(v) subset supp(V)}.               (4.1)
$$

Otherwise adjoining a word outside V whose support stayed inside supp(V)
would give a six-dimensional subcode with support at most d_5, contradicting
the strict inequality d_6>d_5.

Let

$$
ell=d_6-d >= 1                                      (4.2)
$$

be the support increment from V to W_c. Apply the proved MDS-soft
codimension-one compiler in `experimental/grande_finale.tex` to the affine
chart 0+W_c. The exact source-to-target dictionary is:

| compiler symbol | present packet |
|---|---|
| j | 5 |
| m | a=K+w |
| t=n-m | R |
| hyperplane support d | d_5(W_c) |
| support layer e | ell=d_6-d_5 |
| outside common mismatch b_0 | eta |

The last line is load-bearing. Outside supp(W_c), the common chart value is
zero. There are a-g points of S_0 where the received word U is also zero,
and exactly eta points of E_0 where U is nonzero. Hence b_0=eta, not zero
and not ell.

The MDS-soft profile is

$$
Pi_b=(d-R+eta+b) prod_{i=1}^4(w+i+eta+b),
Q=w+1+eta.                                          (4.3)
$$

At the full support layer, ell=R+g-eta-d, so

$$
Pi_ell=g prod_{i=1}^4(w+i+R+g-d).                  (4.4)
$$

In particular Pi_ell is independent of eta.

### Profile interpolation

The largest intercept in (4.3) is

$$
A_profile=d-R+eta=w+5+q_5+eta.                     (4.5)
$$

The imported profile-interpolation lemma applies because

$$
4Q-A_profile >= 170,336+3 eta > 0.                 (4.6)
$$

The whole-chart compiler therefore gives

$$
|{c in W_c : agr(U,c)>=a}|
 <= floor(d_{falling 5}/Pi_0
          +d_{falling 6}/(Q Pi_ell)).               (4.7)
$$

This is not a per-coset estimate. There is no multiplicative factor p.

## 5. Uniform endpoint relaxation

Put d_0=1,048,581 and d_1=1,080,585. Positive eta decreases both terms in
(4.7). At eta=0, the first term is

$$
T_0(d)=d_{falling 5}/((d-R) prod_{i=1}^4(w+i)).     (5.1)
$$

Its adjacent ratio is at most one exactly when

$$
5R-4d-4 >= 0.                                      (5.2)
$$

At d_1 the margin is 583,301, so T_0 decreases throughout the interval and
is maximized at d_0.

After (4.4), the second term is

$$
T_1(d,g,eta)=d_{falling 6}/
 ((w+1+eta) g prod_{i=1}^4(w+i+R+g-d)).             (5.3)
$$

All factors are positive. This expression increases with d, decreases with
g, and decreases with eta. It is maximized at
(d,g,eta)=(d_1,781,458,0). The corresponding support layer is 682,002>0.
Taking the maxima of the two terms separately only enlarges the feasible set,
so it is a valid uniform upper bound.

The exact endpoint fractions are

$$
T_0(d_0)=
13,595,760,770,200,795,755,215,673 /
14,972,954,495,361,184,520,                         (5.4)
$$

and

$$
T_1(d_1,781,458,0)=
10,050,609,557,311,530,989,539,114,985,523 /
104,976,882,945,190,479,108,637,352,042.            (5.5)
$$

Their exact sum has floor

$$
908,116.                                             (5.6)
$$

Since

$$
15,775,933-908,116=14,867,817,                      (5.7)
$$

the inherited shallow family cannot have rank six. Together with the
parent's rank-one-through-five exclusion, every forbidden shallow family
has rank at least seven.

## 6. Independent exact control

The independent Sage replay recomputes all deployed integers and fractions.
It also exhausts a literal GF(7) Reed-Solomon source with

$$
(n,K,a,R,w)=(7,6,6,1,0).                            (6.1)
$$

For the received table U(x)=x^6, exactly seven degree-<6 codewords agree on
at least six points. Their affine span has dimension six. The
five-dimensional subcode of polynomials divisible by X has support six, is
support-saturated in the full support-seven code, and the two-resource
compiler is sharp:

$$
6+1=7.                                              (6.2)
$$

The translated six nonanchor words also satisfy the generalized marked-line
count with exact sides

$$
4,320 <= 5,040.                                     (6.3)
$$

This finite-field census is a falsification and orientation control only. It
is not evidence for a deployed asymptotic or incidence bound.

## 7. Audit and nonclaims

- Rigorous proof: the generalized-weight double count, exact compiler
  substitution, monotonicity, and rational floor above.
- Exact computation: finite integer sweeps and rational reductions replay the
  displayed symbolic inequalities; they are not empirical evidence.
- Heuristic reasoning: none is used.
- Conjectural content: ranks at least seven and the full M31 row remain open.
- Layer cake / dyadic summability: not applicable.
- Moment / Markov / Chebyshev: not applicable.
- Parameter dependence: all constants are the displayed finite M31 row
  integers. No hidden asymptotic parameter occurs.
- Ledger: `ledger movement=0`; no official endpoint or score changes.

The next maximal proof target is the complete rank-at-least-seven
fixed-syndrome/secant incidence, compiled at the actual-codeword source
level. Another scalar profile or unowned support count cannot close it.

## Replay

From the repository root, run the primary Python verifier in normal,
optimized, tamper, and check modes; the Sage replay; and the packet verifier
in normal and tamper modes. Exact commands are listed in the certificate
README.
