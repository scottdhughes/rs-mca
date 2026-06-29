# M1 a=327 Joint Target/Codeword Solver

Status: `TESTED_TARGET_SYSTEMS_NO_A327 / PARTIAL / EXPERIMENTAL`

This note records a first bounded joint target/codeword search for the
`a=327` interleaved-list target over

```text
RS[F_17^32, H, 256].
```

It is not a board update, not an MCA row, and not a global upper-bound result.

## Model

Anchor

```text
P_1 = 0
D_i = P_i - P_1,  i = 2,...,7.
```

For a bounded set of target received-word value classes, the scanner imposes
linear equality constraints on the six degree `<256` difference polynomials.
It then samples the resulting nullspace over proxy field `GF(12289)`, evaluates
the induced seven codewords on `H`, and globally reschedules the received word
with the exact value-class max-min assignment solver.

This differs from the earlier support/RIM route because the target constraints
are deliberately partial. The search asks whether a partial received-word
template can guide low-degree codewords toward a new global schedule.

## Search Layer

Scanner:

```text
experimental/scripts/scan_m1_a327_joint_target_codeword_solver.py
```

Data:

```text
experimental/data/m1_a327_joint_target_codeword_solver.json
```

The bounded layer uses eight all-pair-boundary source embeddings and five
target-selection strategies:

```text
target systems:          40
rows per target system:  384
nullspace samples:       8 per system
codeword tuples tested:  320
proxy field:             GF(12289)
```

The best tested tuple had high capacity:

```text
capacity upper bound: 454
```

but the exact proxy received-word rescheduler gave only:

```text
max-min agreement: 311 < 327.
```

No sampled target system reached the `a=327` proxy threshold.

## Exact-Audit Boundary

Sage wrapper:

```text
experimental/scripts/audit_m1_a327_joint_target_codeword_solver.sage
```

Exact-audit data:

```text
experimental/data/m1_a327_joint_target_codeword_solver_exact_audit.json
```

The exact audit is intentionally gated:

```text
run exact GF(17^32) extraction only if a proxy target system reaches a>=327.
```

Since the proxy search found no such target system, the Sage wrapper records:

```text
NO_EXACT_AUDIT_TRIGGERED
```

This means the current checkpoint is a bounded proxy search result, not an
exact `GF(17^32)` route cut for all joint target/codeword systems.

## Verification

Verifier:

```text
experimental/scripts/verify_m1_a327_joint_target_codeword_solver.py
```

The verifier checks the target-system count, sample count, best capacity,
best proxy max-min value, absence of exact triggers, JSON source linkage, and
non-claims.

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

The first joint layer shows that partial target systems can generate high
capacity but still fail after global rescheduling. A next constructive layer
should use a stronger target-set chooser, for example CP-SAT or MILP, to select
constraints by predicted post-reschedule balance rather than by fixed
coordinate-order heuristics.
