# M1 a327 mu8 Rank-3 Generic-Core No-Goods

Status:

`EXACT_EXTRACTION_NO_A327 / MU8_RANK3_GENERIC_CORE_NOGOODS / PARTIAL / EXPERIMENTAL`

Track:

`INTERLEAVED_LIST`, denominator `17^32`, `mca_counted=false`.

## Purpose

The current rank-3 `mu_8` front can satisfy support and pair caps, but exact
Sage audits over `GF(17^32)` repeatedly find full-rank active interpolation
systems. The pivot-core barrier audit showed that many of these full-rank
systems admit a dependency-last pivot core made only from generic `POINT` and
`ZERO` option groups.

This packet converts those dependency-free full-rank cores into CP-SAT
no-good constraints:

```text
for each mined full-rank pivot core C:
  sum(selected option groups in C) <= |C|-1
```

The goal is constructive. Future schedules should not be allowed to reproduce
known generic full-rank escape cores before exact Sage rank is run.

## Scope

This is not an `a=327` witness and not a global obstruction. It is a local
generator guard for the tested rank-3 `mu_8` menus and pressure ledgers.

Useful next tests:

1. Run the rank-3 low-row scheduler with `--forbid-core-subsets`.
2. Check whether support/pair feasibility survives after forbidding known
   generic cores.
3. If it survives, run exact Sage interpolation and pair-projection audits.
4. If it fails, record the result as a local menu/core-avoidance obstruction.

## Smoke Result

The first guarded run used:

```text
experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multicorepenalty50k_augmented_menu.json
experimental/data/m1_a327_mu8_rank3_generic_core_nogoods.json
```

with hard `--forbid-core-subsets`.

Result:

```text
support_pair_candidates = 2
best_min_support = 327
best_total_incidence = 2293
best_pair_count_max = 255
best_core_nogood_constraints = 1
```

The exact Sage audit over `GF(17^32)` then tested those two candidates:

```text
systems_tested = 2
matrix shapes = 152 x 96
rank/nullity = 96 / 0 for both systems
positive_nullity_systems = 0
```

Interpretation:

Forbidding the previously mined generic pivot cores is not enough for this
menu. Support/pair feasibility survives, but the exact system still finds a
different full-rank core. The next generator must prevent dependency-free
`POINT/ZERO` pivot cores as a structural class, not merely block the first
mined core signatures.

## Follow-up Pressure Audit

The guarded candidates were then rerun through row-dependency pressure mining:

```text
experimental/data/m1_a327_mu8_rank3_core_nogood_row_dependency_pressure.json
```

Result:

```text
systems_tested = 2
matrix shapes = 152 x 96
rank/nullity = 96 / 0 for both systems
positive_nullity_systems = 0
critical_group_count = 0 for both systems
rank_drop_histogram = {0: 62} for both systems
```

Both selected schedules still have only singleton projective keys:

```text
max_projective_key_support = 1
projective_key_support_histogram = {1: 34}
```

Pivot-core mining found fresh full-rank cores. In one candidate, the
`dependency_last` core has no dependency groups. In the other, all tested pivot
core orderings have no dependency groups. Thus the no-good layer blocked known
core signatures but did not force the scheduler into repeated-function
dependency structure.

This strengthens the local route cut: for this menu, forbidding individual
generic cores is too weak. A future generator needs a structural constraint
against singleton projective-key full-rank cores, or it needs a different
dependency-producing menu family.

## Non-claims

- No MCA numerator.
- No protocol soundness claim.
- No ordinary list-decoding statement beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6`.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
