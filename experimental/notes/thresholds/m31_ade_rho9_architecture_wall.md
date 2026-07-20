# M31 two-shell frontier: the exact rho-nine ADE architecture wall

**Status:** `PROVED` for the abstract countercertificate, the two-level
`A`-type integer jump, and the binary-rectangle lemma below.  The deployed
M31 list row remains `OPEN`; this packet moves no ledger atom.

**Scope:** This is the sharp successor to
`m31_ade_component_sensitive_refinement.md`.  That packet proves the
common-height ADE exclusion for `rho<9` and stops at
`(kappa,t,e1,e2)=(2,276415,276415,552830)`, where `rho(t)>9`.  Here we prove
that the stop is intrinsic to the frozen ADE/rank consequences: they admit an
exact M31-sized model.  We then prove that the canonical model is not an
actual binary support family.  Thus the next proof must use binary
realizability or the full prefix equations, not another ADE threshold
optimization with the same hypotheses.

Replay:

```text
python3 experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --check
python3 -O experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --check
python3 experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --tamper-selftest
python3 -O experimental/scripts/verify_m31_ade_rho9_architecture_wall.py --tamper-selftest
sage experimental/scripts/verify_m31_ade_rho9_architecture_wall.sage
```

## 1. Frozen M31 boundary

Use

```text
p  = 2^31-1,
N  = 2^21,
m  = 981129,
w  = 67447,
d0 = N-w = 2029705,
L  = 2^24 = 16777216,
R  = m(N-m),
t  = 276415.
```

The component-sensitive predecessor uses

```text
rho(t)=Nt/(2Nt-R).
```

At the first unclassified row,

```text
2Nt-R = 64406010193 > 0,
rho(t) = 579684270080/64406010193
       = 9.000468564... > 9.                         (1)
```

The frozen consequences used by the ADE route are:

1. `L` distinct norm-two roots in an ADE lattice of real rank at most `N`;
2. distinct selected-root inner products in `{0,1}`;
3. a dual vector of common height one and squared norm at most `rho(t)`;
4. the selected Gram matrix has rank at most `d0` over `F_p`.

They are necessary consequences of an actual two-shell prefix fiber.  They
are not sufficient to reconstruct one.

## 2. Exact abstract countercertificate

Put

```text
q = ceil(L/9) = 1864136,
v = q+9       = 1864145,
r = v-1       = 1864144.
```

In the standard realization of `A_{v-1}`, split the `v` coordinates into
sets `P,Q` of sizes `9,q`.  For every directed edge `(i,j) in P x Q`, take

```text
alpha_ij = e_i-e_j.
```

Delete the eight edges from the first eight vertices of `P` to one fixed
vertex of `Q`.  The remaining graph has

```text
9q-8 = L
```

edges and is connected: the edge connectivity of `K_{9,q}` is nine.  Hence
the selected roots span `A_{v-1}` and have real rank `r`.  Two distinct roots
have inner product one when their edges share an endpoint and zero otherwise.

Define

```text
z_i = q/v   for i in P,
z_j = -9/v for j in Q.
```

The coordinates sum to zero, all coordinate differences are integral, so
`z` lies in `A_{v-1}^*`, and

```text
<alpha_ij,z> = 1,
||z||^2 = 9q/v
          = 9-81/v
          = 16777224/1864145
          = 8.999956548... < 9 < rho(t).                (2)
```

The Gram rank over `F_p` is also `r`.  Indeed, the selected connected-edge
incidence vectors span the sum-zero hyperplane, whose standard bilinear form
is nondegenerate modulo `p` because its discriminant is `v` and
`0<v<p`.  Finally,

```text
r = 1864144 <= d0 = 2029705
```

with gap `165561`.  Thus all four frozen ADE/rank consequences are
simultaneously feasible at the first residual row.  No argument using only
those consequences can extend the predecessor exclusion across `rho=9`.

The model also realizes the entire centered Euclidean interface preceding
the ADE classification.  Put `h^2=1/rho(t)` and extend the root space by one
orthogonal unit vector.  Since `h^2||z||^2<1`, choose a unit vector `e` whose
projection to the root span is `hz`, and set

```text
y_alpha=sqrt(t)(alpha-he).
```

Then `y_alpha` is orthogonal to `e`, shared-endpoint and disjoint-endpoint
pairs have exchange distances `t` and `2t`, respectively, and

```text
tQ=YY^T+(2t-R/N)J.
```

Thus the countercertificate defeats the frozen post-incidence
Euclidean/ADE/rank package.  What it does not provide is a binary factor
`X` of the required constant-weight Gram matrix or any prefix-syndrome data.

There is no conflict with the proved predecessor boundary.  At `t=276416`,

```text
rho(276416) = 579686367232/64410204497 < 9,
||z||^2-rho(276416)
            = 4985688279688/120069960662060065 > 0.
```

The countercertificate becomes admissible exactly on the uncertified side of
that boundary.

### Why nine is the exact two-level jump

For one connected two-level `A` component with smaller part `a` and rank at
most `d0`, the root capacity is at most

```text
a(d0+1-a).
```

For `a<=8` this is maximized at eight, but

```text
8(d0+1-8) = 16237584 < L
```

by `539632`.  Part size nine is the first possible integer in this connected
two-level class, and its smallest other part is `q=ceil(L/9)`.  Its squared
dual norm is exactly the value in (2).  This is the integral mechanism behind
the predecessor's strict `rho<9` boundary.  No corresponding optimality is
claimed for disconnected or multilevel `A` configurations.

## 3. Binary-rectangle lemma

The abstract witness is not an RS support family.  The obstruction follows
from a general exact lemma.

> **Binary-rectangle lemma.**  Let `a,b>=2`, `t>0`, and let
> `x_ij in {0,1}^N`.  Suppose the Hamming distance is `2t` when exactly one
> of the two indices agrees and is `4t` when neither index agrees.  Then
>
> ```text
> N >= max(2t,a-1)+max(2t,b-1).                        (3)
> ```

For constant-weight supports in the application, exchange distance is half
the Hamming distance.  Fix any two rows and columns.  The four corresponding
binary vectors have side squared distances
`2t` and diagonal squared distances `4t`.  If the two side vectors from one
corner are `u,v`, then `u.v=0`.  The opposite corner has inner product
`2t` with each of `u,v` and squared norm `4t`, hence equals `u+v`.  Therefore
every two-by-two affine minor vanishes:

```text
x_ij+x_i'j' = x_ij'+x_i'j.                              (4)
```

Apply (4) coordinatewise.  A `{0,1}`-valued matrix with all affine
two-by-two minors zero is constant, row-only, or column-only: simultaneous
nonzero row and column variation would create a value outside `{0,1}`.
Thus the coordinates partition into constant, row, and column blocks.

The `a` row words are pairwise equidistant at Hamming distance `2t`.
Consequently their block has length at least `2t`, while their centered Gram
matrix (equivalently, the Gram matrix of differences from one word) has rank
`a-1`; its length is at least `max(2t,a-1)`.  The same
argument gives column-block length at least `max(2t,b-1)`.  The two blocks
are disjoint, proving (3).

## 4. The canonical ADE model fails binary realization

The eight deleted edges all meet the last vertex of `Q`.  The selected roots
therefore contain a complete `9 x (q-1)` rectangle with `L-1` roots.  If they
came from actual binary supports at the boundary row, (3) would require

```text
N >= 2t+(q-1)-1
  = 2416964.
```

But the deployed domain has `N=2097152`, a contradiction with exact margin

```text
2416964-2097152 = 319812.                                (5)
```

This does **not** exclude the source-grid row.  It excludes only this
canonical complete-rectangle realization of the abstract countercertificate.
An arbitrary height-one `A` component may select a dense nonrectangular
edge set, may use several adjacent coordinate levels, and may coexist with
other ADE components.

## 5. Exact verdict and next theorem

The result is a sharp architecture route cut:

- **proved:** the common-height ADE/rank hypotheses alone cannot cross the
  first `rho>=9` row;
- **proved:** the extremal two-level complete-rectangle model cannot be an
  actual M31 binary support family;
- **open:** classify every dense height-one `A`-component edge graph allowed
  by `||z||^2<=rho(276415)` and the `L`-root load;
- **open:** combine that classification with binary realizability and then
  with the full weight-plus-power-sum prefix equations;
- **not claimed:** an actual prefix fiber, exclusion of `t=276415`, a bound on
  `U_Q`, a deployed safe row, or any ledger movement.

The next load-bearing statement is therefore a dense-`A` binary-realization
dichotomy: every admissible height-one edge graph either contains a complete
rectangle large enough for (3), decomposes into a paid few-shell/quotient
owner, or is recorded as an explicit primitive residual.  More optimization
of the same ADE norm envelope cannot supply that statement.
