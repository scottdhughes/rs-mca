# Route-D owner-typed forest-to-complementary-cell compiler v1

STATUS: PROVED

## Result

This packet proves the finite-set compiler

```text
ROUTE_D_OWNER_TYPED_FOREST_TO_COMPLEMENTARY_CELL_COMPILER.
```

Fix a primitive prefix target `z`. After the exact named first-match
deletions, route every actual all-maximal-minors-vanishing incidence once to
`DEEP_MCA_RANK_DROP`, preserving `z`, the literal common core `G`, and
every carried key. Suppose the remaining full-rank primitive packets embed as
the edges of a fixed-`z` marked bipartite forest. Root each component once.
The parent edge is then in canonical bijection with its nonroot child vertex.

If generated supports inject into a marked cell set

```text
E_z subset Fin(t) x F_p
```

and the nonroot marked vertices inject into its complement, the primitive
edges inherit a complementary injection. The complementary-cell theorem at
commit `19c061ee094388e3261e8151e6c799826801ae12`, note blob
`c1bceae338a55c3f94381bf8f71d8b1584f05e95`, then gives

```text
|G_gen(z)| + |D_prim(z)| <= t*p.
```

At the KoalaBear MCA Route-D row,

```text
t=67472,
p=2130706433,
t*p=143763024447376.
```

Thus the desired primitive support certificate follows from the stated
interfaces. The abstract compiler is proved; those deployed interfaces are
not currently constructed.

## 1. Exact owner-typed domain

Start with one fixed primitive target `z` after the literal first-match order

```text
generated_field,
quotient_planted,
sparse_pade_hankel,
m1_window_shadow,
rank_drop_pivot,
bc_chart,
sp_shift_pair,
extension_slope.
```

For every residual marked packet retain

```text
(z,G,carriedBase,f,g,gamma,S,T),
```

where `G` is the literal common-core mark and `carriedBase` contains the full
prefix, fixed Rule-2 key, normalization, cell, and every other first-match
datum used by recovery.
At minimum, `carriedBase` contains `(r,c,U0,H,beta,G)` plus every
actual first-match and owner tag used by recovery; carrying `G` separately in
the displayed packet is intentional marked redundancy. This is **not** the
source contact weight
`kappa_contact = 1_(A0 cap G) - 1_(R0 cap G)`.

The owner partition is:

1. The packet is an actual finite noncontained incidence and every maximal
   minor of its field-native `t x (j+1)` Hankel matrix vanishes. Route it
   exactly once to `DEEP_MCA_RANK_DROP`, without changing `(z,G,carriedBase)`.
2. At least one actual maximal minor is nonzero. Retain the packet in
   `D_prim(z)`; a canonical nonzero minor may select a chart but supplies no
   support payment.

The all-minors equivalence and type-correct conditional route are pinned at
commit `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
`f24ce928df7e7170c1b4f3228d5fe9b184be50b4`. The distinct-slope owner is
defined at commit `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`, note blob
`ddfce00907f34128b324a64041f4e0ec8957b7d3`. This compiler does not
recharge its slopes per packet, support, core, chart, or minor.

Actual-incidence typing is load-bearing. One selected zero minor is not rank
drop. A raw fold determinant or toy pivot is not an actual owner matrix.

## 2. Fixed-target marked compatibility forest

Let `P_z=D_prim(z)`. For each `d in P_z`, define complete marked endpoint
keys

```text
L(d)=(z,G,carriedBase,u(d)),
R(d)=(z,G,carriedBase,sigma(d)).
```

The endpoint key may contain additional actual chart data, provided the same
complete carried base is preserved. It may not erase `z`, `G`, the full
prefix, or any datum required by the decoder.

Assume:

```text
EDGE INJECTIVITY:
  d -> (L(d),R(d)) is injective.

FOREST:
  the simple bipartite graph Gamma_z with edges d joining L(d) to R(d)
  is a forest.
```

Square-fold reconstruction at commit
`f64e03a1215653eeafe3186df55269273d9f7653`, note blob
`301144d04458027131779907f7f74aa5a6682bf4`, proves one route to edge
injectivity when both even occupancy and odd signed data are carried with
literal `G`. It does not prove the deployed post-deletion forest hypothesis.

The fixed-target clause cannot be projected away. A compatibility graph
formed after erasing `z` is not the graph counted by `D_prim(z)`.
The target-preserving pseudoforest criterion and its exact projection audit
are pinned at commit `fe34ed4dbbd4564d3f8af5c5de3fdf78c589e0d1`, note blob
`58c722cac2655aabf8ec887837607db7c79d6987`, verifier blob
`597524e7f639bd4abc90e12986c67eb84c7fce10`, and Lean blob
`14d2975fd4e9897748c863d7f7383bba104d51d4`. Its counterexample is to
target erasure: the target-tagged fixture is a pseudoforest and admits an
endpoint assignment. It does not prove or refute the deployed fixed-`z`
forest transfer required here.

## 3. Forest edge-to-nonroot bijection

Choose one deterministic root in each component of `Gamma_z` and orient
every tree away from its root. Assign an edge to its child endpoint.

**Lemma (rooted-forest child bijection).** The child map is a bijection

```text
P_z -> V(Gamma_z) minus Roots(Gamma_z).
```

**Proof.** Every nonroot vertex in a rooted tree has exactly one parent edge,
so it is the child of exactly one edge. Every tree edge connects a parent to a
child, so every edge has exactly one child. Applying this independently in
each component proves both injectivity and surjectivity. In particular,

```text
|P_z|=|V(Gamma_z)|-number_of_components.
```

The lemma controls edge multiplicity. It does not construct a cell label or
an owner map.

## 4. Complementary cell composition

Put

```text
C_z=Fin(t) x F_p.
```

Assume a subset `E_z subset C_z` and injections

```text
gamma_z : G_gen(z) -> E_z,
nu_z    : V(Gamma_z) minus Roots(Gamma_z) -> C_z minus E_z.
```

The map `nu_z` must be support-level and decode the complete marked vertex,
including literal `G`; an image label is insufficient.

Define

```text
delta_z(d)=nu_z(child(d)).
```

The child bijection and injectivity of `nu_z` make `delta_z` injective.
Its image lies outside `E_z`, while the generated image lies inside
`E_z`. Therefore

```text
gamma_z disjoint_union delta_z :
  G_gen(z) disjoint_union D_prim(z) -> C_z
```

is injective. Hence

```text
|G_gen(z)|+|D_prim(z)|
  <= |C_z|
  = t*p
  = 67472*2130706433
  = 143763024447376.
```

This is exactly the arbitrary-cell form of the theorem at commit
`19c061ee094388e3261e8151e6c799826801ae12`, note blob
`c1bceae338a55c3f94381bf8f71d8b1584f05e95`; No scalar-only separation is
required.

## 5. Saturating finite fixture

The deterministic verifier uses a six-cell universe

```text
Fin(2) x F_3.
```

One owner-typed record has a `2 x 3` matrix whose three maximal minors all
vanish. It is routed once to `DEEP_MCA_RANK_DROP`, preserving the fixed
fixture target and `G={7}`. Four full-rank primitive records form the path

```text
u0 -- sigma0 -- u1 -- sigma1 -- u2.
```

The path has four edges, five vertices, one root, and four nonroot vertices.
Two generated supports inject into

```text
E_z={(0,0),(0,1)}.
```

The four nonroot vertices inject into the four complementary cells. The
combined charge has size six and saturates the universe. This is a finite
schema fixture for the abstract theorem, not a claim that a deployed
survivor-to-actual-incidence compiler exists.

## 6. Exact raw F23 negative control

The verifier independently rebuilds the exact raw family pinned at commit
`f64e03a1215653eeafe3186df55269273d9f7653`, verifier blob
`2507f09115c7eefbc86025dbaf204ea83c744283`. It reproduces:

```text
75 packets,
56 fixed-H comparisons,
1 extension deletion,
55 primitive nonextension rows,
all-fold digest
  f6ac27af0adff1a4e864c0b565c9e3b3e524c08ab7bfac9ac940e7f1583b8877,
ordered base-graph digest
  620013449005471279d314a991283f139d2f31169d084b6ff1cdf2c1058018b5.
```

The graph on `(G,u)` and `(G,sigma)` is a forest:

```text
edges=55,
left vertices=55,
right vertices=52,
components=52,
cycle rank=0.
```

The left projection is injective, so a multiplicity-one forest orientation
exists. Nevertheless,

```text
55 > 2*23 = 46.
```


All 55 rows share the fixed one-coordinate prefix analogue `beta=(10)` and
the incomplete printed key `(r,c,U0,H,beta)`. Their literal `G` varies over
21 values, and the maximum fixed-`G` fiber is 5. Thus `55>46` is a
fixed-analogue-prefix/incomplete-key floor, not a fixed-complete-base or
deployed-fixed-`z` floor.

Thus forest orientation alone cannot manufacture a `Fin(2) x F_23` cell
injection. The cell-map hypothesis is genuine.

This is raw, pre-first-match algebra. It has fixed analogue `beta=(10)`, but it
is not the deployed target `z in F_p^67471`; it
does not execute the named deletion mask, and it does not refute the deployed
certificate. Its nonzero determinant is only the predecessor's toy
diagnostic; it is never routed or identified with an actual RIM pivot.

## 7. Missing deployed interfaces

The compiler application remains conditional on exactly:

1. an executable implementation of the eight named first-match deletions;
2. a Route-D survivor-to-actual-incidence compiler;
3. a post-deletion fixed-`z` marked compatibility-forest theorem;
4. a generated-support injection into `E_z`;
5. a nonroot complete marked-vertex injection into `C_z minus E_z`.

The executor gap is pinned at commit
`8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67`, note blob
`fdeabf0708cb8806feefae9322ed9002339332cf`. A primitive target exceeding
`t*p`, a post-deletion nonforest component that defeats the selected
compiler, or an actual all-minors-vanishing family not routed to the named
owner is a new obstruction, not a proved row.

## 8. Provenance

- primitive support target: commit
  `e83962ae5ad7bacb391b691ffd37f0abef977b83`, note blob
  `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
- marked-incidence common-core guardrail: commit
  `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`, note blob
  `a7f2bf4f1338d0b31d999c86a29859317033113f`;
- actual all-minors adapter: commit
  `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
  `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`;
- actual rank-drop owner: commit
  `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`, note blob
  `ddfce00907f34128b324a64041f4e0ec8957b7d3`;
- square-fold reconstruction and raw F23 corpus: commit
  `f64e03a1215653eeafe3186df55269273d9f7653`, note blob
  `301144d04458027131779907f7f74aa5a6682bf4`, verifier blob
  `2507f09115c7eefbc86025dbaf204ea83c744283`, Lean blob
  `ab061b3c53a320fbb8881bab4e6fa8e573f83248`;
- complementary-cell add-back: commit
  `19c061ee094388e3261e8151e6c799826801ae12`, note blob
  `c1bceae338a55c3f94381bf8f71d8b1584f05e95`;
- target-preserving pseudoforest criterion and target-erasure audit: commit
  `fe34ed4dbbd4564d3f8af5c5de3fdf78c589e0d1`, note blob
  `58c722cac2655aabf8ec887837607db7c79d6987`, verifier blob
  `597524e7f639bd4abc90e12986c67eb84c7fce10`, Lean blob
  `14d2975fd4e9897748c863d7f7383bba104d51d4`.

Every cross-work reference is pinned by a full commit and, where consumed,
the exact note or verifier blob.

## 9. Nonclaims

- The deployed primitive support certificate is not proved here.
- No unavailable first-match deletion is claimed executable.
- No raw packet is called an admitted deployed survivor.
- No toy pivot is called an actual pivot or routed to rank drop.
- No selected-minor vanishing is treated as rank drop.
- No low-moment, Johnson-packing, mode-at-null, image-only, or zero-defect
  shortcut is used.
- Literal `G`, fixed `z`, and complete carried keys are never projected
  away in the theorem.

## 10. Reproduction and formalization

```bash
python3 experimental/scripts/verify_route_d_owner_typed_forest_cell_compiler_v1.py
python3 -O experimental/scripts/verify_route_d_owner_typed_forest_cell_compiler_v1.py
python3 experimental/scripts/verify_route_d_owner_typed_forest_cell_compiler_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_owner_typed_forest_cell_compiler_v1.py --tamper
(cd experimental/lean/route_d_owner_typed_forest_cell_compiler_v1 && lake build)
```

The standalone Lean layer proves the finite cardinality composition,
edge/nonroot count transport, complementary add-back arithmetic, deployed
capacity pin, and owner-preservation interface. The Python verifier performs
the exact graph and F23 finite replays.
