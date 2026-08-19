# ArkLib / proximityprize transfer audit for rs-mca

## 1. Canonical source and status

The old ArkLib project board and issue thread are archival.  The campaign
moved on 2026-08-15 to `elizaOS/proximityprize`; the audited current main is
`983069a332de36fd3d6ef6f33fccadafa01b0ff5`.

The current tracker says the production δ* problem remains open/on-BGK.
That global analytic wall is not the right next tool for the finite
`K = 662,479` rs-mca residual.

## 2. Results that transfer

The useful landed interfaces are:

- `RatioCensusWeightIdentity.lean`: exact zero/ratio decomposition,
  `sum ratioMult = support`, and the per-fixed-line Markov bound.
- `LineListReduction.lean`: bad-scalar/appearing-codeword incidence,
  support-adjusted line-list reductions, and MDS uniqueness of a coordinate
  fiber once at least `k` coordinates are prescribed.
- `LineListAppearanceFiber.lean`: exact profiles filtered to codewords that
  actually occur on the affine line.
- `LineListSupportRatioFiber.lean`: every appearing codeword has a heavy
  support-ratio fiber; raw interpolation completions are replaced by actual
  line appearances with one large ratio fiber.
- `LineListIncidenceMultiplicity.lean` and
  `LineListSingletonDefectGeometry.lean`: the exact bipartite incidence graph
  and localization by exact zero-agreement profile.
- `LineListMCAWeld.lean`: the prize-facing weld is now landed; badness gives
  witness farness, codeword shifts preserve the event, and the remaining
  obligations are far-line lists plus the large-zero/low-profile branch.
- `RatioMultiplicityBridge.lean`: on a genuinely polynomial ratio line, the
  low-weight scalar set is empty or one degenerate scalar under the exact
  degree inequality.

These are finite ownership and fiber tools.  They fit the current rs-mca
owner compiler far better than the broad character-sum programme.

## 3. Results that must not be imported

- A uniform second-witness multiplicity floor is refuted.  Extremal hard lines
  can have every bad scalar witnessed by exactly one codeword.
- `RegionMiddleExclusion` is refuted over `ZMod 23`; it is not a valid
  production bridge.
- Ratio-census conservation alone cannot impose a degree cap: arbitrary ratio
  profiles are realizable by full-support affine lines.
- The global production problem remains open and requires more than a bare BGK
  supremum estimate.

Accordingly, the next rs-mca theorem must use the actual four-block polynomial
and support provenance, not generic witness multiplicity or a support-only
ratio argument.

## 4. Direct coupling at the adjacent wall

At `K = 662,479`, the old relaxed dirty profile is

```text
r = 394,382
eta = 58,813
y = r + eta = 453,195
(d1,d2,d3,d4) = (0, 2 eta, r, r)
```

The two active ray owners have

```text
(k1,rho1) = (268,097, 117,626)
(k2,rho2) = (385,723, 0)
```

and their dominant two-block fixed-pair owner needs

```text
h = eta = 58,813
```

dirty support coordinates.

Let `U` be the dirty coordinates where the fixed pair itself agrees with the
received pair, and `u = |U|`.  Same-support pair noncontainment gives
`0 <= u <= h-1`.

The fixed-pair class obeys

```text
P(u) <= floor((y-u)/(h-u)).
```

Inside either ray parameter plane, every coordinate in `U` has parameter line
equal to the fixed-pair graph.  Once the fixed-pair owner is removed, those
coordinates cannot occur in off-graph ray supports.  Therefore the ray outside
excesses fall from `rho_i` to `rho_i-u`; a ray is empty when this becomes
negative.

At `u=0`, the pair plus two-ray bound is `470,347`.  For positive `u`, the
second ray disappears and an exact scan gives a unique maximum

```text
u = h-1 = 58,812
pair + remaining ray = 593,696.
```

All other pair and triplet owners contribute `4 eta + 8 = 235,260`.
Hence the exact coupled cap for this profile is

```text
235,260 + 593,696 = 828,956.
```

The previously independent cap was `1,099,983`.

## 5. Strongest next theorem

Define a shared-fiber joint owner compiler for every feasible dirty profile:

1. choose each active pair of one-block rays;
2. retain the exact simultaneous-agreement set `U` of their fixed-pair
   intersection;
3. replace the independent charge
   `N_ij + R_i + R_j` by the maximum over `u=|U|` of the pair count plus
   ray envelopes with outside excess reduced by `u`;
4. optimize the resulting symmetric convex/piecewise-convex objective over
   the dirty-incidence polytope.

The remaining proof obligation is a majorization or certified branch-and-bound
showing that the global maximum is attained on a finite list of incidence
vertices.  ArkLib's exact-profile and appearance-fiber vocabulary supplies the
right abstraction for that step.

A generic second-witness discount must not be used.
