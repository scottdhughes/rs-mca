# Prefix Rigidity and Johnson Packing Correspondence

Status: **PROVED** for the exact finite prefix-rigidity distance and Johnson
packing cap in equation (4.4).

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, proposition
`prop:prefix-rigidity-full` and equation `eq:packing-fiber-cap` (4.4).

## Statement map

| Frontiers argument | Lean declaration |
| --- | --- |
| Johnson sphere and closed ball on the uniform slice | `GrandeFinale.PrefixRigidityPacking.johnsonSphere`, `GrandeFinale.PrefixRigidityPacking.johnsonBall` |
| Delete/insert parametrization of a sphere | `GrandeFinale.PrefixRigidityPacking.johnsonSphereEquiv` |
| Exact sphere size `choose m i * choose (n-m) i` | `GrandeFinale.PrefixRigidityPacking.johnsonSphere_card` |
| Exact radius-`t` ball volume | `GrandeFinale.PrefixRigidityPacking.johnsonBall_card` |
| Balls at center distance greater than `2t` are disjoint | `GrandeFinale.PrefixRigidityPacking.disjoint_johnsonBall_of_two_mul_lt` |
| Prefix-fiber Johnson distance at least `w+1` | `GrandeFinale.PrefixRigidityPacking.coefficientFiber_johnsonDistance` |
| Pairwise disjoint balls at `t = floor(w/2)` | `GrandeFinale.PrefixRigidityPacking.coefficientFiber_johnsonBalls_pairwiseDisjoint` |
| Multiplication form of the packing cap | `GrandeFinale.PrefixRigidityPacking.coefficientFiber_mul_johnsonVolume_le` |
| Displayed natural-division form of (4.4) | `GrandeFinale.PrefixRigidityPacking.coefficientFiber_card_le_div_johnsonVolume` |

## Statement comparison

Lean writes the prefix depth as `w = m - K`, using the coefficient fiber

`PrefixPigeonhole.coefficientFiber D K m z`.

For two distinct members `S` and `T`, equality of their coefficient prefixes
gives

`degree (locator S - locator T) < K`.

The existing locator factorization and rigidity theorem then yields

`m - K + 1 <= (S \ T).card`,

which is exactly Johnson distance at least `w + 1` because every fiber member
has cardinality `m`.

For a center `M`, a point of the radius-`i` sphere is represented uniquely by
an `i`-subset deleted from `M` and an `i`-subset inserted from `D \ M`.  Lean
packages this as an explicit equivalence and obtains the exact sphere size

`m.choose i * (D.card - m).choose i`.

Summing the disjoint spheres for `0 <= i <= t`, with
`t = (m - K) / 2`, gives the source denominator.  The fiber balls are pairwise
disjoint and lie in `D.powersetCard m`, so the generic finite packing kernel
proves

```text
fiber.card *
    (sum i in range (t + 1),
      m.choose i * (D.card - m).choose i)
  <= D.card.choose m.
```

Positivity of the radius-zero summand then gives the displayed natural-number
division cap without a rational coercion.

## Scope boundaries

This is the complete exact finite distance-and-packing portion of
`prop:prefix-rigidity-full`.  The source's final asymptotic observation that
the ball volume has logarithm `o(n)` when
`w` is on the order of `n / log |B|` is not asserted here: it requires an
explicit sequence model, polynomial-field hypotheses, and an asymptotic
logarithm estimate.

The packing cap is deliberately not presented as the row-sharp Q bound.  As
the source notes, Johnson packing alone does not supply the random
`|B|^(-w)` factor.

## Verification

```text
lake env lean GrandeFinale/PrefixRigidityPacking.lean
```

The module prints the axioms of its five principal results.  The audit reports
only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; no proof
placeholder or added axiom occurs.
