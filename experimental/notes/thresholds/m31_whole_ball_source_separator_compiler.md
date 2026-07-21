# M31 whole-ball source-to-separator compiler and four-face CRT compression

## Status

**PROVED exact whole-ball closure contract / PROVED four-face
Forney--Pluecker defect-window and reduced-CRT compression / PROVED exact toy
rank-drop controls / UNIVERSAL M31 SOURCE BRIDGE OPEN / LEDGER MOVEMENT
ZERO.**

This packet is stacked on PR #1002 at
`4958c2f95a9e3dd16bb28a13c919ff87811611a4`.  It prevents the scoped
four-flat separator from being promoted into a deployed row claim without a
source-valid whole-ball theorem, and it compresses every rank-deficient
factorized four-face to one of only `137` exact Pluecker-defect cells.

The conclusions are deliberately split.

1. A closing direct-list theorem must cover every exact error support of
   weight at most `R`, not only the boundary shell and not only the binary
   pseudo-family from PR #1001.
2. Pairwise-coprime equal-degree factors force separator surjectivity at every
   truncation `D>=2r`.  The deployed truncation is only `137` degrees below
   that universal threshold.
3. Every deployed rank drop has an exact parameter `0<=tau<=136`, cokernel
   defect `h=137-tau`, and six nonzero primitive Pluecker quotients of degree
   at most `tau` satisfying four linear identities and one quadratic identity.
4. A bounded global syzygy is equivalent to six explicit reduced-CRT
   congruences on the six disjoint factor locators.
5. Pairwise-disjoint roots do not by themselves eliminate the rank-drop
   locus: an exhaustive `GF(7)`, degree-one census has `1,344` primitive
   rank-three points among `5,040` labelled disjoint sextuples.

The fifth item is a toy-scale falsifier for a proposed field-uniform
full-rank lemma.  It is not a deployed M31 survivor.  No `U_Q`,
`U_list-int`, or other completion atom is supplied here.

The exact replay files are

```text
experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py
experimental/scripts/verify_m31_whole_ball_source_separator_compiler.sage
experimental/data/certificates/m31-whole-ball-source-separator-compiler/manifest.json
```

## 1. Exact deployed target

Throughout,

```text
p       = 2^31-1       = 2,147,483,647,
n       = 2^21         = 2,097,152,
K       = 2^20         = 1,048,576,
a       = 1,116,023,
sigma   = a-K          = 67,447,
R       = n-a          = 981,129,
B*      = floor(p^4/2^100)=16,777,215,
L       = B*+1         = 16,777,216.
```

Let `D=Z_Fp(T_n)`, let `C=RS_Fp(D,K)`, and put `V=C^perp`.  For
`E subset D`, retain

```text
W_E={v in V:supp(v) subset D\E}.
```

For a nonzero syndrome hyperplane `H`, define

```text
z_H(E)=1
```

exactly when

```text
W_E subset H,
W_(E\{x}) not subset H       for every x in E.             (1.1)
```

The direct prime-field closure target is

```text
max_H sum_(E subset D, |E|<=R) z_H(E) <= B*.               (1.2)
```

The sum in (1.2) has exactly `R+1=981,130` weight layers.  The zero syndrome
has list size one and is separate.  A proof of (1.2), together with the
already proved unsafe side and scalar descent, closes the adjacent M31 list
row over the prime and quartic fields.

## 2. Why boundary and frozen-face certificates do not close (1.2)

PR #1002 proves a separator for four boundary supports in one declared
complete-`T_1024`-fibre embedding.  A hypothetical list counted by (1.2)
need not have either property.

An interior exact error support `E`, `|E|<R`, can be enlarged to a boundary
set by discarding agreement points, and containment then survives:

```text
E subset E'  implies  W_(E') subset W_E subset H.
```

The one-point escapes do not survive for the newly added points.  Thus this
is not an escape-preserving boundary reduction.

Likewise, the `2^24` binary family in PR #1001 is a consistent pseudo-model
showing that pairwise, scalar-shell, and local-line invariants are
insufficient.  It is not a source theorem saying that every family counted
by (1.2) contains that binary model or one of its two-dimensional faces.

Consequently a closing certificate must supply one of the following
universal bridges:

```text
WHOLE_BALL_DIRECT_BOUND,
EXHAUSTIVE_SOURCE_SELECTION_AND_FIRST_MATCH_OWNER_MAP,
ACTUAL_HYPERPLANE_SURVIVOR_OF_SIZE_AT_LEAST_L.
```

A boundary-only or frozen-embedding-only atlas supplies none of them.

## 3. Exact four-face Forney imbalance

This section isolates the strongest field-uniform algebraic consequence of
the factorized parity face.

Let `F` be any field.  Fix six monic, pairwise coprime polynomials

```text
A_0,A_1,B_0,B_1,C_0,C_1 in F[X]
```

of common degree `r`.  In the intended support application their roots are
six pairwise-disjoint subsets of the evaluation domain.  Define

```text
P_00=A_0 B_0 C_0,
P_10=A_1 B_0 C_1,
P_01=A_0 B_1 C_1,
P_11=A_1 B_1 C_0.                                      (3.1)
```

No factor divides all four entries, so the row `P=(P_00,P_10,P_01,P_11)`
is primitive and has degree

```text
e=3r.
```

For `D>=0`, define

```text
Theta_D: direct_sum_(ab) F[X]_<D -> F[X]_<(e+D),
Theta_D((H_ab))=sum_(ab) H_ab P_ab.                     (3.2)
```

Let

```text
mu_1<=mu_2<=mu_3
```

be the Forney indices of the syzygy module of `P`.  Primitivity and the
predictable-degree property give

```text
mu_1+mu_2+mu_3=e,                                      (3.3)
dim ker Theta_D=sum_j max(0,D-mu_j).                   (3.4)
```

Subtracting the rank of (3.2) from its target dimension and using (3.3)
gives the exact cokernel identity

```text
dim coker Theta_D=sum_j max(0,mu_j-D).                  (3.5)
```

In particular,

```text
Theta_D is onto  iff  mu_3<=D.                          (3.6)
```

For the PR #1002 parity face,

```text
r=33*1,024=33,792,
e=3r=101,376,
D=sigma=67,447.
```

If `Theta_sigma` is not onto, (3.5) forces

```text
mu_3>=sigma+1=67,448,
mu_1+mu_2<=e-(sigma+1)=33,928,
mu_1<=floor(33,928/2)=16,964.                           (3.7)
```

Thus every rank-deficient factorized face has a nonzero syzygy

```text
sum_(ab) H_ab P_ab=0,
max_(ab) deg H_ab<=16,964.                              (3.8)
```

This replaces an `168,823`-row maximal-minor problem by one bounded Padé/CRT
incidence with `4(16,964+1)=67,860` coefficient unknowns.

The existence of one such low syzygy is necessary, not sufficient, for rank
drop. The exact two-row criterion is

```text
Theta_sigma is not onto
iff there are two F[X]-independent syzygies S,T with
    deg S+deg T<=33,928.                                (3.9)
```

The forward direction takes the first two rows of a sorted row-reduced
basis. Conversely, the exterior predictable-degree property gives
`mu_1+mu_2<=deg S+deg T`; hence (3.9) forces
`mu_3=3r-mu_1-mu_2>=sigma+1`.

If `Theta_sigma` is onto, the weighted-dual locator bridge from PR #1002
gives

```text
sum_(ab) W_(E_ab)=W_(E_core),
```

and the four exact supports contradict one-point escape.  Hence only the
rank-deficient branch (3.7)--(3.9) can survive that separator.

## 4. Six reduced-CRT equations

For any row `H=(H_ab)` with `max deg H_ab<3r`, the global equation
`sum H_ab P_ab=0` is equivalent to the following six congruences:

```text
H_10 B_0 C_1 + H_11 B_1 C_0 = 0 mod A_0,               (4.1)
H_00 B_0 C_0 + H_01 B_1 C_1 = 0 mod A_1,               (4.2)
H_01 A_0 C_1 + H_11 A_1 C_0 = 0 mod B_0,               (4.3)
H_00 A_0 C_0 + H_10 A_1 C_1 = 0 mod B_1,               (4.4)
H_10 A_1 B_0 + H_01 A_0 B_1 = 0 mod C_0,               (4.5)
H_00 A_0 B_0 + H_11 A_1 B_1 = 0 mod C_1.               (4.6)
```

Necessity follows by reducing (3.8) modulo each factor and cancelling the
other factors, which are units by pairwise coprimality.

Conversely, let `S_H=sum H_ab P_ab`. Equations (4.1)--(4.6) say that every
one of the six pairwise-coprime degree-`r` factors divides `S_H`. Their product
of degree `6r=202,752` therefore divides `S_H`. But

```text
deg S_H<3r+3r=6r.                                       (4.7)
```

Hence `S_H=0`, proving sufficiency. In particular, both rows in the exact
criterion (3.9) satisfy the bound because each has degree at most
`33,928<3r`; after ordering by degree, the first row satisfies the sharper
`16,964` bound. No generic saturation or enormous maximal minor is needed to
state the exact residual incidence.

For one row `H`, (4.1)--(4.6) characterize that row being a syzygy; their
solvability alone is not equivalent to rank drop. The exact deployed algebra
problem is to classify two independent rows satisfying (3.9), equivalently
the Pluecker system in the next section, under split pairwise-disjoint roots
in the actual Chebyshev domain. Every compatible component must be eliminated
by escape, assigned a source-valid globally disjoint owner, or recorded as an
actual primitive survivor.

## 5. Exact Pluecker defect window

The six congruences compress the entire non-surjective branch much further.
Keep the vertex order

```text
0=00, 1=10, 2=01, 3=11.
```

Let `S=(s_i)` and `T=(t_i)` be the first two rows of a row-reduced syzygy
basis, ordered by vector degree, and put

```text
Delta_ij=s_i t_j-s_j t_i,       i<j.
```

Applying the same reduced-CRT equation to `S` and `T`, and eliminating the
two coefficients, gives the exact divisibilities

```text
A_0 divides Delta_13,       A_1 divides Delta_02,
B_0 divides Delta_23,       B_1 divides Delta_01,
C_0 divides Delta_12,       C_1 divides Delta_03.        (5.1)
```

At least one minor is nonzero because `S,T` are independent. Every nonzero
minor in (5.1) has degree at least `r`, whereas row-reducedness gives

```text
max_(i<j) deg Delta_ij=mu_1+mu_2.                        (5.2)
```

Consequently, pairwise coprimality alone proves

```text
mu_1+mu_2>=r,
mu_3=3r-(mu_1+mu_2)<=2r.                                (5.3)
```

Thus `Theta_D` is automatically onto for every `D>=2r`. In the deployed
face, `sigma=67,447=2r-137`. Combining (5.3) with the non-surjective upper
bound (3.7), define `tau=mu_1+mu_2-r`. Then the whole rank-drop branch is
the exact finite window

```text
0<=tau<=136,
mu_1+mu_2=r+tau=33,792+tau,
mu_3=2r-tau=67,584-tau,
h=dim coker Theta_sigma=137-tau.                         (5.4)
```

Equivalently, there are exactly `137` possible `(tau,h)` cells. Their exact
matrix dimensions are

```text
dim ker Theta_sigma = 101,102-tau,
rank Theta_sigma    = 168,686+tau,
dim coker            = 137-tau.                         (5.5)
```

Define the six Pluecker quotients, with signs fixed by the declared vertex
order, by

```text
q_A0=Delta_13/A_0,       q_A1=Delta_02/A_1,
q_B0=Delta_23/B_0,       q_B1=Delta_01/B_1,
q_C0=Delta_12/C_0,       q_C1=Delta_03/C_1.             (5.6)
```

They satisfy

```text
deg q_*<=tau,             max_* deg q_*=tau,             (5.7)
```

the four exact contraction identities

```text
A_0 q_A1+B_0 q_B1+C_0 q_C1=0,                           (5.8)
-A_1 q_A0+B_0 q_B1-C_1 q_C0=0,                          (5.9)
A_0 q_A1-B_1 q_B0+C_1 q_C0=0,                           (5.10)
A_1 q_A0+B_1 q_B0+C_0 q_C1=0,                           (5.11)
```

and the Pluecker identity

```text
B_0B_1 q_B0q_B1-A_0A_1 q_A0q_A1+C_0C_1 q_C0q_C1=0.    (5.12)
```

Only three of (5.8)--(5.11) are independent: subtracting (5.9) and
(5.10) from (5.8) gives (5.11). The identities follow by contracting
`S wedge T` with the parity-product row `P`; (5.12) is the ordinary
Pluecker relation.

In the deployed window, all six quotients in (5.6) are nonzero. Indeed, if
one vanishes, one of
(5.8)--(5.11) becomes an equality between two coprime degree-`r` locators
times quotients of degree less than `r`. Both quotients must vanish. The
four vertex identities propagate this vanishing around the connected
tetrahedron until all six minors vanish, contradicting independence of
`S,T`. Hence the `2 x 4` matrix with rows `S,T` is `[4,2,3]` MDS over
`F(X)`.

The six quotients are primitive as a family:

```text
gcd(q_A0,q_A1,q_B0,q_B1,q_C0,q_C1)=1.                  (5.13)
```

To see this, use `gcd(P_00,P_10,P_01,P_11)=1` to split the map
`P:F[X]^4 -> F[X]`. The three-row syzygy basis together with a Bezout
section is a unimodular basis of `F[X]^4`; in particular the first two rows
span a direct summand, so their `2 x 2` minors generate the unit ideal. A
common divisor of the six `q_*` would divide every minor, proving (5.13).

Two useful support restrictions follow without any domain hypothesis. A
nonzero syzygy with one zero coordinate has degree at least `r`, and one with
two zero coordinates has degree at least `2r`; this follows by reducing at
the complementary factors, or directly cancelling the unique common factor
of two parity products. Therefore `S` has four nonzero coordinates and `T`
has at least three.

If the locators are additionally squarefree and split, each designated minor
has an exact simple locator zero at at least

```text
r-tau>=33,656                                             (5.14)
```

roots of its locator: only the at most `tau` roots of the corresponding
`q_*` can increase the multiplicity. This is the strongest current
domain-facing invariant. Equations (5.8)--(5.12) are necessary compression
conditions; they are not asserted sufficient to lift arbitrary quotients to
two polynomial syzygies, a source-valid received word, or one-point escapes.

## 6. Exact toy rank-drop controls

Disjointness alone cannot prove the reduced-CRT system empty.  Take `r=1`
and write the six factors as `X-a_0`, ..., `X-c_1`.  The determinant of
`Theta_1` factors over the integers as

```text
(a_1-a_0)(b_1-b_0)(c_0-c_1) Phi,                        (6.1)
```

where

```text
Phi = a_0 a_1 b_0 + a_0 a_1 b_1
    - a_0 b_0 b_1 - a_1 b_0 b_1
    - a_0 a_1 c_0 + b_0 b_1 c_0
    - a_0 a_1 c_1 + b_0 b_1 c_1
    + a_0 c_0 c_1 + a_1 c_0 c_1
    - b_0 c_0 c_1 - b_1 c_0 c_1.                       (6.2)
```

The three displayed linear factors are excluded by pairwise disjointness,
but `Phi` is not.  Exhausting all labelled pairwise-distinct sextuples in
`GF(7)` gives

```text
7*6*5*4*3*2 = 5,040 total,
3,696 with rank(Theta_1)=4,
1,344 with rank(Theta_1)=3,
0 with smaller rank.                                    (6.3)
```

For example,

```text
(a_0,a_1,b_0,b_1,c_0,c_1)=(0,1,2,3,4,6)
```

has the constant syzygy

```text
P_00+3P_10+6P_01+4P_11=0 mod 7,                         (6.4)
```

and Forney profile `(0,1,2)`. A second row-reduced syzygy is

```text
(1,X,3+3X,3X),
```

and its six quotients in (5.6) are

```text
(q_A0,q_A1,q_B0,q_B1,q_C0,q_C1)=(5,3,6,1,3,3).         (6.5)
```

Thus the example realizes `tau=0` in the abstract hypothesis class and has
defect `h=1` at the toy truncation `D=2r-1`; it does not instantiate the
deployed formula (5.4), where `tau=0` gives `h=137`. It verifies every sign
in (5.8)--(5.12) and proves that the lower bound `mu_1+mu_2>=r` is sharp.
This is an explicit rank-drop point on the coprime-factor toy locus. It
proves that any deployed emptiness theorem
must use more than factor disjointness; the Chebyshev-domain/source/escape
conditions are load-bearing.

A second exact control removes support symmetry as a generic explanation.
Over `GF(23)`, take the twelve-point support

```text
{1,2,4,5,7,8,10,12,13,15,19,20}
```

and the six quadratic locator root sets

```text
A_0={1,2},    A_1={10,12},
B_0={4,20},   B_1={8,19},
C_0={5,15},   C_1={7,13}.                               (6.6)
```

Its Forney profile is `(0,2,4)`, the ranks of `Theta_D` for `D=1,...,6`
are

```text
(3,6,8,10,11,12),                                      (6.7)
```

and `Theta_3` has cokernel defect one while `Theta_4` is onto. A constant
syzygy is `(1,9,18,18)`. Deterministic enumeration of all

```text
|PGL_2(GF(23))|=23(23^2-1)=12,144
```

normalized projective matrices finds that only the identity preserves the
twelve-point support. Thus this rank drop is not generated by a
nontrivial projective support stabilizer.

Both controls are exact toy-scale route cuts. They neither lift to the
deployed Chebyshev domain nor construct an M31 received word.

## 7. Fail-closed whole-ball compiler contract

A future closing candidate must declare one canonical priority partition of
the universe in (1.2).  Every cell must have exactly one terminal:

```text
ESCAPE_KILLED,
PAID_OWNER,
ACTUAL_HYPERPLANE_SURVIVOR,
UNPAID_PRIMITIVE.
```

Closure is permitted only if all of the following hold:

```text
weight interval is exactly [0,R],
all R+1 layers are covered,
source selection is proved and hash-bound,
every containment and every one-point escape is retained,
owners are first-match disjoint,
owner/add-back maps use one common source key,
there is no UNPAID_PRIMITIVE or survivor terminal,
all exact charges sum to at most B*.
```

The present artifact intentionally fails the source-selection, interior,
boundary-classification, owner, and add-back gates.  Its exact output is

```text
UNIVERSAL_SOURCE_BRIDGE_REQUIRED.                        (7.1)
```

not `SAFE` and not a counterexample.

There is one further M31-specific route cut.  Since

```text
p=2,147,483,647>B*=16,777,215,
```

a direct component charge containing a factor `p^eY` with `eY>=1` already
exceeds the entire budget.  A positive-dimensional primitive component must
therefore be eliminated, transferred to a non-direct structured owner with a
proved add-back theorem, or retained as unpaid.  It cannot be closed by a
direct root-union count.

## 8. Ledger and PR-worthy endpoints

```text
whole-ball source selection:                 open
interior weights 0 through R-1:              open
boundary rank-16 h=1 classification:         open
four-face 137-cell Pluecker/CRT compression:   proved
pairwise-disjointness-only full-rank claim:  false in toy model
U_paid:                                      null
U_Q:                                         null
U_list-int:                                  null
U_new:                                       null
ledger movement:                             0
prime-field M31 list row closed:              false
quartic-field M31 list row closed:            false
prize claim:                                  false
```

The next result is bankable only if it reaches one of:

```text
WHOLE_BALL_BOUND_LE_16777215,
COMPILER_COMPATIBLE_DISJOINT_LEDGER_LE_16777215,
ACTUAL_M31_HYPERPLANE_SURVIVOR,
UNIVERSAL_ROUTE_CUT_WITH_EXACT_MISSING_INVARIANT.
```

Another isolated fibre-aligned determinant is not a completion atom.

## 9. Replay

```text
python3 experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --check
python3 -O experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --check
python3 experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_whole_ball_source_separator_compiler.py --tamper-selftest
sage experimental/scripts/verify_m31_whole_ball_source_separator_compiler.sage
```

The Python verifier uses only the standard library.  It reconstructs the
deployed arithmetic, the `137`-cell Forney--Pluecker window, every reduced-CRT
equation, the full `GF(7)` census, both explicit primitive controls, the
`GF(23)` projective stabilizer, and the fail-closed whole-ball contract. The
Sage replay independently factors (6.1), repeats the census with native
finite-field matrices, recovers the toy Forney profiles and Pluecker
quotients, and checks all CRT residues and the projective stabilizer.
