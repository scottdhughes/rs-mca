# M1 a327 mu8 Rank-3 No-Singleton Projective Keys

Status:

`EXACT_EXTRACTION_NO_A327 / MU8_RANK3_LOWROW_NO_SUPPORT_PAIR_PASS / PARTIAL / EXPERIMENTAL`

Track:

`INTERLEAVED_LIST`, denominator `17^32`, `mca_counted=false`.

## Purpose

The current rank-3 `mu_8` menus repeatedly pass support/pair by selecting
singleton projective-key `POINT` groups, and exact Sage audits then find
full-rank interpolation systems.  This audit adds the structural CP-SAT
constraint:

```text
for every projective key k:
  selected_count(k) = 0 or selected_count(k) >= 2
```

This is stronger than rewarding repeated keys or forbidding individual mined
pivot cores. It removes singleton projective-key choices as a class.

In the compact PR packet, the raw schedule ledgers are not included directly;
their sizes and SHA-256 hashes are recorded in
`experimental/data/m1_a327_mu8_rank3_route_cut_certificate_summary.json`.

## Evidence

Input menu:

```text
experimental/data/m1_a327_mu8_rank3_balanced_key_bundle_multicorepenalty50k_augmented_menu.json
```

Core no-good file:

```text
experimental/data/m1_a327_mu8_rank3_generic_core_nogoods.json
```

Broad run:

```text
experimental/data/m1_a327_mu8_rank3_no_singleton_projective_key_schedule.json
```

Result:

```text
subspaces_solved = 8
support_pair_candidates = 0
forbid_core_subsets = true
forbid_singleton_projective_keys = true
solver statuses = 7 INFEASIBLE, 1 UNKNOWN
```

The one bounded `UNKNOWN` case was rerun directly:

```text
experimental/data/m1_a327_mu8_rank3_no_singleton_projective_key_blockkey001_schedule.json
```

Focused result:

```text
subspace = rank3_blockkey_001
solver_status = INFEASIBLE
support_pair_candidates = 0
singleton_key_forbid_constraints = 613
```

Thus, for the tested augmented rank-3 menu, forbidding singleton projective-key
selections eliminates the support/pair front.

## Interpretation

This is a local menu obstruction, not a global theorem and not an `a=327`
witness.  It explains the latest repeated full-rank behavior:

```text
allow singleton projective keys -> support/pair passes, exact rank full
forbid singleton projective keys -> support/pair fails
```

The next construction should synthesize a new menu family where repeated
projective keys are support-balanced by construction, rather than trying to
repair this fixed menu after scheduling.

## Verification

```text
python3 experimental/scripts/verify_m1_a327_mu8_rank3_no_singleton_projective_keys.py --json
```

## Non-claims

- No MCA numerator.
- No protocol soundness claim.
- No ordinary list-decoding statement beyond the stated interleaved-list
  predicate.
- No global `Lambda_mu(C,327) <= 6`.
- No exact `Lambda_mu`.
- No exact `delta*_C`.
