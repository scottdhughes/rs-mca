# M1 a327 mu8 rank2 selected-front route-cut summary

Status: experimental, interleaved-list only.

This packet compresses the selected rank-2 `mu_8` carrier fronts into a small,
hash-addressed summary.  It is not a global rank-2 obstruction.  Its scope is
only the tested carrier-plane libraries, local menu grammars, CP-SAT schedulers,
and one adaptive near-front exact diagnostic.

## Model

The rank-2 carrier ansatz is:

```text
q(Y) = u F(Y) + v G(Y),    deg F, deg G < 32.
```

This gives a 64-variable rational interpolation system after a selected
schedule fixes ratio or zero conditions at quotient points.

## Frontier

The selected fronts improved but did not cross the support/pair gate:

```text
greedy carrier schedule:
  best min support = 286
  best selected incidence = 2032

CP-SAT width-4 with row-cap gate:
  best min support = 291
  best selected incidence = 2041

full-menu width ablation:
  best min support = 313
  best selected incidence = 2193

adaptive ratio-column selected front:
  best min support = 314
  best selected incidence = 2202
```

The target is:

```text
min support >= 327
selected incidence >= 2289
pair count max <= 255
```

So the best selected rank-2 front is still short by:

```text
13 on weakest support
87 selected incidences
```

No support/pair-passing rank-2 schedule was produced in this selected front.

## Exact diagnostic

The best adaptive near-front candidate was:

```text
rank2_plane_0148_adaptive_seed_w04
```

It has:

```text
support vector = [314, 315, 317, 314, 314, 314, 314]
selected incidence = 2202
pair count max = 255
row cost = 92
```

This candidate is not witness-relevant because it misses the support target,
but it was exact-audited as a diagnostic over `GF(17^32)`:

```text
matrix shape = [92, 64]
rank/nullity = 64 / 0
positive-nullity systems = 0
forced global ratio lines = []
rank-one collapse risk = false
```

The diagnostic says that the nearest selected adaptive front is also
interpolation-full-rank.  It does not prove that rank-2 carriers cannot work.

## Interpretation

The route cut is local:

1. The tested rank-2 selected fronts did not reach support/pair.
2. The nearest adaptive front was exact full rank.
3. Further progress needs a different carrier/menu generator, not more
   squeezing of this selected front.

No exact lift, witness, MCA, protocol, global list bound, exact `Lambda_mu`, or
exact `delta*_C` claim is made.
