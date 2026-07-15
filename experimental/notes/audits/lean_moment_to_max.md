# Lean: moment-to-max proof packets

## Status

PROVED. The `moment_to_max` default Lake target builds on the pinned
Lean/Mathlib 4.28 toolchain.

## Source correspondence

The package covers three separate statements:

- `MomentToMax.lean` retains the finite Q-to-SP transfer example for
  `lem:q-to-sp-detail`.
- `MomentToMax/MomentMapMaxFiber.lean` formalizes the proved R2 theorem of
  `experimental/notes/thresholds/moment_map_max_fiber.md`.
- `MomentToMax/PowerWeightedConcentrationFloor.lean` formalizes the proved
  second-moment floor in
  `experimental/notes/thresholds/cap25_v13_q_pw2_concentration_floor.md`.

### Moment-map largest fibre

For the interval block `{0,...,b-1}`, the module defines the exact
degree-two signature `(|S|, sum S, sum x^2)`, its finite signature box, all
Boolean-subset fibres, and their maximum. It proves

```
2^b <= B(b) * fstar(b) <= b^6 * fstar(b)    (b >= 2),
log(fstar(b)) / b -> log 2.
```

It then defines the supremum of the fibre rates over all nonempty finite
nonnegative-integer blocks and proves `phiStar = log 2`. A separate compiler
shows that any broader global block rate with the universal `log 2` ceiling
and containing the interval family must equal `log 2`.

### Power-weighted concentration floor

For a nonnegative finite target family `X`, the module proves the cleared
Cauchy--Schwarz inequality

```
(totalMass X)^2 <= |support| * secondMoment X.
```

It provides an exact natural-count form and permits any cardinality upper bound
`P`. For `P > 0`, it derives the normalized real statement

```
totalMass X / sqrt P <= sqrt (secondMoment X).
```

The literal two-step theorem also retains the intermediate nonzero-support
denominator `sqrt |s|`. Specializing `P = p^w` gives the source note's
power-weighted floor. Its per-stratum contrapositive proves that mass greater than `T * sqrt P` forces
the square-root second moment above `T`; equivalently, a proposed nonnegative
`r=2` certificate below the floor cannot upper-bound the second moment.

## Nonclaims

The moment-map note's local-CLT refinement
`fstar = Theta(2^b / b^(9/2))` is measured, not proved. For the concentration
floor, deployed-row bit margins and toy censuses remain independent verifier
computations. The empirical typical-stratum mass assertion and the open signed-
`L¹` inverse/sparsity route are not promoted by the Lean module.

## Verification

- `lake build`: PASS, 8031 jobs.
- `python3 experimental/scripts/verify_moment_map_max_fiber.py`: PASS, 39/39.
- `python3 experimental/scripts/verify_q_pw2_concentration_floor.py`: PASS,
  66/66.
- Principal axiom reports for the general Mathlib theorems contain only
  `propext`, `Classical.choice`, and `Quot.sound`; the exact PTE histogram also
  reports the expected compiler-backed decision axioms.
- `python3 experimental/scripts/verify_pte_cluster_packing.py`: PASS, 48/48.
- `python3 experimental/scripts/verify_comb_trade_champion.py`: PASS, 34/34.
- `python3 experimental/scripts/verify_comb_trade_champion_k5.py --check`:
  PASS, 40/40; tamper self-test PASS, 3/3.

### PTE cluster packing

`MomentToMax/PTEClusterPacking.lean` formalizes the finite affine-invariance,
common-complement trade, collision-deletion deficit, and unconditional
three-coordinate Vandermonde cap. It exhaustively checks the named 14-point
block's sorted signature histogram `(fstar,L1)=(12,12239)` and proves its
cleared objective/tensor arithmetic. The local-CLT tensor limit, optimizer
symmetry, measured trends, and global supremum remain explicit nonclaims; see
`PTE_CLUSTER_PACKING_AUDIT.md`.

### Combinatorial-trade champion

`MomentToMax/CombTradeChampion.lean` proves the exact six-aggregate expansion
and cleared large-shift decoder for common-shift combs, verifies the minimal
Prouhet gadget and the sufficient `s>219` threshold, and checks exact
cross-power rate comparisons for the reported `k=2`--`k=5` census rows.
The large histogram values remain independent computed inputs; searched-window
optimality, decimal/asymptotic rates, and global supremum claims are not
promoted. See `COMB_TRADE_CHAMPION_AUDIT.md`.
