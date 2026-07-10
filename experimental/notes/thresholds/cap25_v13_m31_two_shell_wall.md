Continues PR #476; the M31 Chebyshev domain and signed-`e_m` target are from PR #434.

# M31 two-shell fibers: exact integral-ratio/high-multiplicity wall and exact smaller-toy maxima

Status per claim: `PROVED` (integral shell ratio, `k<=774`, the exact surviving
parameter lattice, the M31 prefix `p`-rank obstruction, and three construction
exclusions) / `PROVED-AT-TOYS` (global maxima at `p=31,n=8` and
`p=127,n=16`; an inclusion-maximal witness at `p=127,n=32`) / `OPEN` (the
unrestricted deployed two-shell bound).

Verifier: `experimental/scripts/verify_m31_two_shell_wall.py` (zero argument,
stdlib only). Data: `experimental/data/cap25_v13_m31_two_shell_wall.json`.

## 1. Verdict: exit 4, with an exact wall

PR #476 proved that an `s`-shell subfamily of one prefix fiber has size at most
`binom(n-w-1+s,s)`. It paid `s=1` at M31 but left `s=2` open. This packet does
not decide all of `s=2`. It reduces every possible counterexample to the named
cell

```text
M31-TWO-SHELL-INTEGRAL-RATIO-HIGH-MULTIPLICITY.
```

Precisely, let `F` be a family of `m`-subsets in one M31 prefix fiber and suppose
its two exchange distances are `e1<e2`. If `|F|>B*`, then, for some integers
`k,t`,

```text
e1=(k-1)t, e2=kt, 2<=k<=774,
67448<=e1<=522118, e2<=981129,                         (1.1)
dim_Fp ker(A+kI) >= 14747511 at |F|=B*+1,              (1.2)
```

where `A` joins pairs at distance `e1`. The exact lattice in (1.1) contains
`3254885` pairs `(k,t)`. Any proof must exclude those graphs; any falsifier can
print one such incidence/adjacency certificate. Generic two-distance algebra
cannot silently bypass this exceptional integral-ratio branch.

The deployed constants are

```text
p=2^31-1=2147483647, n=2^21=2097152,
m=981129, w=67447, B*=2^24-1=16777215,
L0=B*+1=2^24=16777216=8n.
```

## 2. The integral-ratio reduction is elementary  `PROVED`

Let `L=|F|`, let `X` be the `L x n` incidence matrix, put
`t=e2-e1`, and let `A` be the adjacency matrix for distance `e1`. Define the
rational number `k=e2/t`. Entry by entry,

```text
M := A+kI = t^(-1) X X^T + (e2-m)t^(-1) J.             (2.1)
```

Indeed, `XX^T` is `m` on the diagonal, `m-e1` on an edge, and `m-e2`
otherwise. Because every row of `X` has weight `m`,

```text
1_L = m^(-1) X 1_n.
```

Consequently the columns of both terms on the right of (2.1) lie in
`col(X)`, and `rank_R M<=rank_R X<=n`. If `L>B*`, then `L>=L0>n`, so `M`
is singular. Thus `-k` is an eigenvalue of the integral matrix `A`. A rational
algebraic integer is an integer, hence `k` is an integer, `k>=2`, and

```text
e1=(k-1)t, e2=kt.                                      (2.2)
```

This proves the ratio conclusion directly; no imported
Larman--Rogers--Seidel theorem is needed.

## 3. The exact Seidel cutoff `k<=774`  `PROVED`

Set

```text
S = 2A-(J-I).
```

It has zero diagonal and off-diagonal entries in `{+1,-1}`, so
`tr S=0` and `tr S^2=L(L-1)`. Also

```text
2M-J = S+(2k-1)I
```

has column space in `col(X)`, hence rank at most `n`. Therefore
`-(2k-1)` is an eigenvalue of `S` with multiplicity at least `L-n`.
Cauchy--Schwarz on the remaining at most `n` eigenvalues, using their sum to
cancel the repeated eigenvalue in `tr S=0`, gives

```text
(2k-1)^2 <= n(L-1)/(L-n).                                (3.1)
```

The right side decreases with `L`. At the first violating size `L0=8n`, it is
the exact integer

```text
n(L0-1)/(L0-n) = (L0-1)/7 = 2396745.
1548^2=2396304 <=2396745 <2399401=1549^2.
```

Since `2k-1` is odd, (3.1) gives `2k-1<=1547`, hence

```text
2<=k<=774.                                               (3.2)
```

The repeated real eigenvalue has multiplicity at least
`L0-n=14680064`.

## 4. Prefix rigidity and the exact surviving lattice  `PROVED`

If two supports in one depth-`w` fiber exchange `e` points and `e<=w`, cancel
their common part. The two remaining `e`-sets have equal first `e` power sums;
Newton identities give equal locator polynomials and hence equal sets, a
contradiction. Thus

```text
e1>=w+1=67448.                                           (4.1)
```

For a support `A`, center its incidence vector as
`y_A=1_A-(m/n)1`. Its squared norm is

```text
r0=m(n-m)/n=1094962529967/2097152,
floor(r0)=522118.
```

If `e1>r0`, every distinct centered pair has negative inner product
`r0-e(A,B)`. Nonzero vectors with all pairwise inner products negative have
size at most their ambient dimension plus one, here at most `n`, already below
`B*`. For completeness, if more than `d+1` such vectors existed, a nonzero linear dependence with coefficient sum zero would express one vector as positive combinations of each sign; taking their inner product would make its squared norm negative. Therefore a counterexample has `e1<=522118`. Also `e2<=m=981129`.

Combining these facts with (2.2)--(3.2), the exact unresolved grid is

```text
2<=k<=774,
ceil(67448/(k-1)) <= t
 <= min(floor(981129/k),
        floor(1094962529967/(2097152*(k-1)))).             (4.2)
```

All `773` values of `k` occur and (4.2) contains exactly `3254885` integer
pairs. Its endpoint rows are

```text
k=2:   67448<=t<=490564  (423117 values),
k=774:    88<=t<=675     (588 values).
```

## 5. The M31 prefix forces enormous `p`-nullity  `PROVED`

Over `F_p`, all rows of `X` lie in one affine prefix fiber. The `w` moment rows
plus the weight row have rank `w+1`, so

```text
rank_Fp X <= n-w = 2029705.                                (5.1)
```

Here `m,t` are nonzero modulo `p`. Identity (2.1) remains valid over `F_p`,
and the same column-space argument gives

```text
rank_Fp(A+kI) <= rank_Fp X <=2029705.                       (5.2)
```

At `L0`, the root `-k` must consequently have geometric multiplicity at least

```text
L0-(n-w)=16777216-2029705=14747511.                         (5.3)
```

Equations (4.2) and (5.3) are the exact smallest statement left open.

## 6. Three standard large constructions do not enter the wall  `PROVED`

### 6a. Quasi-symmetric 2-designs

Suppose the blocks form a `2-(n,m,lambda)` design with `b<p`, replication
number `r`, and all have the same first moment on the distinct domain values
`v=(x)_{x in D}`. Then

```text
Xv=z 1_b,
X^T X=(r-lambda)I+lambda J.
```

Multiplying the first identity by `X^T` says `(r-lambda)v` is constant modulo
`p`. But `0<r-lambda<=r<=b<p`, so this forces all entries of `v` equal, contrary
to the distinct points of `D`. Hence no target-scale quasi-symmetric design
with `B*<b<p` lies in even a depth-one M31 fiber.

### 6b. Affine binary/two-weight-code constructions

Let an affine binary space `x0+C subset {0,1}^n` lie in one M31 prefix fiber.
Fourier-expand each coordinate function on the additive group `C`. For every
used nonzero character pattern, its Fourier coefficient is a nonzero signed
`{+1,-1}` vector killed by moments `0,...,w`. Its positive and negative
supports therefore have the same first `w` power sums. The Newton argument
from (4.1) forces at least `w+1` points of each sign, hence at least

```text
2(w+1)=134896
```

coordinates per used nonzero pattern. The patterns are disjoint, so at most

```text
floor(n/134896)=15
```

are used. They must span `C*` (otherwise a nonzero direction of `C` changes no
coordinate), so `dim C<=15` and

```text
|x0+C|<=2^15=32768 << B*.
```

This excludes affine-binary and binary linear two-weight-code
realizations inside the M31 prefix fiber.

### 6c. Common-core/all-pairs construction

The standard triangular-graph model uses a common core and all unions of two
out of `v` disjoint atoms of size `t`; its shells are `{t,2t}` and it has
`binom(v,2)` blocks. The first `v` beating `B*` is `5794`:

```text
binom(5793,2)=16776528 <=B*,
binom(5794,2)=16782321 >B*.
```

Its ground length is `m+(v-2)t`. At M31, `v=5794` forces

```text
t<=floor((n-m)/5792)=192,
```

whereas (4.1) requires `t=e1>=67448`. Thus the extremal all-pairs model cannot
fit the moment-rigid shell scale.

## 7. Exact toy census  `PROVED-AT-TOYS`

The verifier exhausts every prefix fiber and every allowed shell pair on the
two smaller faithful twin-coset domains.

```text
p=31, n=8, m=4, w=2:
  global maximum = 2;
  unique collision fiber (p1,p2)=(0,2), shell {4}.

p=127, n=16, m=8, w=1:
  global maximum = 23;
  attained in fiber p1=28 with shells {2,4}.
```

For PR #476's main faithful toy `p=127,n=32,m=15,w=2`, an exact meet-in-the-
middle replay gives a size-`17` family in fiber `(45,115)` with shell histogram

```text
{7:58, 8:78}.
```

Scanning all `34359` members of that fiber finds no further member compatible
with all 17 supports, so this witness is inclusion-maximal. It is **not** proved globally maximum.

The scaling read is negative but precise: exact maxima `2` and `23` at the
smaller domains do not expose a growing two-shell construction, while the
main-toy search already becomes an implicit maximum-clique problem over
`565722720` supports and `16129` fibers. This is why the global main-toy maximum
and the deployed integral-ratio cell remain `OPEN`.

## 8. Falsifier target and nonclaims

An exact deployed falsifier should print:

```text
(k,t) satisfying (4.2);
a 2^24 x 2^21 constant-weight incidence description;
the two distances ((k-1)t,kt);
one common M31 prefix syndrome;
an F_p certificate that nullity(A+kI)>=14747511.
```

No such construction was found.

Nonclaims:

- This packet does not prove the unrestricted two-shell bound `|F|<=B*`.
- It does not construct a deployed family larger than `B*`.
- It does not claim that the size-17 `p=127,n=32` witness is globally maximum.
- The exact toy searches are `PROVED-AT-TOYS`, not deployed theorems.
- The design and affine-binary exclusions do not classify every graph in the
  integral-ratio/high-multiplicity wall.

## 9. Reproduce

```text
ulimit -v 2097152; python3 experimental/scripts/verify_m31_two_shell_wall.py
```

The verifier recomputes every displayed number, replays both global smaller-toy
maxima and the main-toy maximality certificate, and runs corruption self-tests.
