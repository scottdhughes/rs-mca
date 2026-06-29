# M1 a=327 Balanced Target MILP Codeword Solver

Status: `TESTED_TARGET_SYSTEMS_NO_A327 / PARTIAL / EXPERIMENTAL`

This note records a balanced target-selection layer for the `a=327`
interleaved-list search over

```text
RS[F_17^32, H, 256].
```

It is not a board update, not an MCA row, and not a global upper-bound result.

## Motivation

The previous joint target/codeword solver showed:

```text
best raw capacity upper bound: 454
best proxy rescheduled max-min: 311
```

So raw value-class capacity was not the immediate bottleneck. The failure was
post-solve balance: the induced value classes did not credit all seven
witnesses evenly under the global received-word rescheduler.

This packet changes the target-selection rule. Instead of fixed coordinate
orders, it uses a MILP search helper to choose partial received-word target
constraints with explicit balance objectives.

## Model

Anchor:

```text
P_1 = 0
D_i = P_i - P_1,  i = 2,...,7.
```

Variables are six degree `<256` difference polynomials. Target constraints
are partial value-class equalities selected from all-pair-boundary source
embeddings.

The MILP selects target coordinates under row budgets:

```text
384, 448, 512
```

using objectives:

```text
max_min_credit
min_variance
penalize_six_of_seven
fiber_diversity
hybrid_balance
```

After target selection, the scanner solves the induced homogeneous coefficient
system over `GF(12289)`, samples nullspace vectors, evaluates all seven
codewords on `H`, and runs the exact proxy value-class max-min rescheduler.

## Search Layer

Scanner:

```text
experimental/scripts/scan_m1_a327_balanced_target_milp_codeword_solver.py
```

Data:

```text
experimental/data/m1_a327_balanced_target_milp_codeword_solver.json
```

The first run tested:

```text
source embeddings:       8
row budgets:             3
selection objectives:    5
target systems:          120
nullspace samples/system: 16
codeword tuples sampled: 1,920
proxy field:             GF(12289)
```

Best result:

```text
target system: all_pair_boundary_bit_reversal__B512__fiber_diversity
raw capacity upper bound: 457
proxy rescheduled max-min: 319
agreement vector: [319, 320, 319, 319, 319, 319, 319]
failure mode: HIGH_CAPACITY_IMBALANCED
```

This improves the previous joint-solver best proxy max-min from `311` to
`319`, but it still does not reach `327`.

## Failure Modes

The sampled tuples split as:

```text
HIGH_CAPACITY_IMBALANCED: 484
LOW_CAPACITY:             1436
```

This is useful diagnostic evidence: balanced target selection moved the
rescheduler in the right direction, but the live failure remains imbalance
among high-capacity value-class geometries.

## Exact-Audit Boundary

Sage wrapper:

```text
experimental/scripts/audit_m1_a327_balanced_target_milp_codeword_solver.sage
```

Exact-audit data:

```text
experimental/data/m1_a327_balanced_target_milp_codeword_solver_exact_audit.json
```

The exact audit is gated:

```text
run exact GF(17^32) extraction only if the proxy search reaches a>=327.
```

No proxy target system reached `a=327`, so the Sage wrapper records:

```text
NO_EXACT_AUDIT_TRIGGERED
```

This is therefore a proxy-search checkpoint, not an exact `GF(17^32)` route
cut for all balanced target systems.

## Verification

Verifier:

```text
experimental/scripts/verify_m1_a327_balanced_target_milp_codeword_solver.py
```

The verifier checks the target-system count, sample count, objectives, row
budgets, failure-mode counts, best proxy max-min value, source linkage, and
no-trigger exact-audit boundary.

## Non-Claims

Not claimed:

- `a=327` interleaved-list certificate;
- global `Lambda_mu(C,327) <= 6`;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`;
- improvement over PR #133.

The denominator remains `|F| = 17^32`, and `mca_counted = false`.

## Next Step

This is the first constructive layer in a while that materially improves the
post-reschedule score. A next run should refine around the best
`B512 / fiber_diversity` and `hybrid_balance` systems, increasing nullspace
samples and adding a local target-coordinate mutation objective aimed at
pushing the current proxy agreement vector

```text
[319, 320, 319, 319, 319, 319, 319]
```

toward `327` without losing the high raw capacity.
