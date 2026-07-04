# M1 a327 quotient-subgroup rank-aware schedule generator

Status:

EXACT_EXTRACTION_NO_A327 / RANK_AWARE_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The previous packet only permuted labels for one fixed aggregate `s=4` schedule.
This branch puts rank feedback earlier by generating new aggregate schedules
with different CP-SAT objectives, then proxy-ranking labelled schedules over
`GF(257)`.

The generator still enforces:

```text
s = 4
quotient length = 128
support_i = 327 for all seven witnesses
pair equality on H <= 255
pair-to-7 selected counts >= 142
```

## Tested objectives

The bounded generator tests:

```text
pair7_slack
min_equation_count
min_pair_equal
min_active_equation
```

For every feasible schedule, it tests grouped, round-robin, residue-spread, and
random labelled quotient assignments, then ranks the quotient equality matrix
over `GF(257)`.

## Result

The bounded run did not find a proxy-positive schedule:

```text
schedules tested = 4
CP-feasible schedules = 1
proxy-positive schedules = 0
best objective = pair7_slack
best equation count = 515
best active partition count = 39
best matrix = [515,384]
best rank/nullity = 384/0
failure = RANK_AWARE_PROXY_FULL_RANK
```

This is not a proof that the quotient-subgroup construction fails. It only says
that the tested rank-aware objectives and bounded labelling samples did not
produce positive quotient nullity.

## Next

The next stronger move is either:

- increase the rank-aware generator budget and add structural-rank objectives;
- rerun unresolved `s=8`, `s=16`, and `s=32` screens with longer CP-SAT budgets;
- switch to quotient-pattern realization directly using the public `a=326`
  packet as a seed.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track quotient-subgroup proxy;
- global obstruction outside the tested rank-aware quotient schedule generator.
