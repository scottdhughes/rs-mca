# Lean: syndrome-line proof packets

## Status

PROVED finite theorems / AUDIT. The `syndrome_line` default Lake target builds
on the pinned Lean/Mathlib 4.28 toolchain.

## Source correspondence

The package contains three layers:

- `SyndromeLine.lean` retains the original enumerated `F_5` syndrome-line
  uniqueness toy for `prop:syndrome-line-normal-form`.
- `SyndromeLine/ExchangeExcessPoleSeparation.lean` formalizes the finite
  pole-separation kernel from
  `experimental/notes/thresholds/exchange_excess_pole_separation.md`.
- `SyndromeLine/InteriorChartCopyDecomposition.lean` formalizes the exact
  excess-one chart decomposition from
  `experimental/notes/thresholds/cap25_v13_bc_l4_interior_chart_to_q.md`.

### Exchange-excess pole separation

The module defines monic support locators, literal depth-`w` locator prefixes,
exchange distance and excess, the common-core reduced gap, and the off-domain
collision set. It proves literal prefix-to-degree cancellation, exact
common-core factorization, the reduced-gap degree and root-count bounds by
exchange excess, minimum-exchange separation, finite collision-mass double
counting, and the exact floor-average pole witness.

This covers Theorem 2.1, Corollary 2.2, and weighted-pole statements (4)--(5)
of the source note.

### Excess-one interior chart

For coefficient data `a_j(T)` and planted prefix `z_j`, the module defines
the recurrence curve

```
phi_0(s) = s,
phi_(j+1)(s) = z_(j+1) + (s-z_0) * phi_j(s).
```

It proves that, after fixing `a_0(T)=s`, the twisted excess-one equations are
equivalent to ordinary prefix equality along `phi(s)`. Therefore each
first-coefficient slice equals the corresponding ordinary prefix fibre, and

```
#valid = sum_(s in B) #prefixFiber(phi(s))
       <= |B| * maxPrefixFiber.
```

A final compiler transfers the same bound to any ray count bounded by the
number of valid supports. This is the source theorem's exact `|B|`-copy
decomposition and row-sharp-Q reduction.

## Nonclaims

For the exchange-excess packet, the later distinct-value Cauchy bounds,
geometry cap, coordinate-load identity, received-line MCA compiler, challenge
shear, and identity-prefix floor are not claimed. No universal large
low-excess subfamily is asserted.

For the interior-chart packet, deployed L4 arithmetic remains verifier output.
The module does not claim heuristic curve equidistribution, the row-sharp-Q
max-fibre bound itself, non-planted/general-line charts, or deeper excess
profiles. The retained `F_5` syndrome-line declarations remain a toy rather
than a general RS incidence proof.

## Verification

- `lake build`: PASS, 8029 jobs.
- `python3 -W error experimental/scripts/verify_exchange_excess_pole_separation.py`:
  PASS, 18,195 checks.
- `python3 experimental/scripts/verify_bc_l4_interior_chart_to_q.py`:
  PASS, 83/83.
- The interior-chart `--tamper-selftest`: PASS, 45/45 perturbations caught.
- Fourteen principal axiom reports contain only `propext`,
  `Classical.choice`, and `Quot.sound`.
- Placeholder and custom-axiom scans: clean.
