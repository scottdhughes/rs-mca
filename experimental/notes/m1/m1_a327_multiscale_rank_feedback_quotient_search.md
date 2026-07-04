# M1 a327 multiscale rank-feedback quotient search

Status:

EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_FULL_RANK_FRONT / PARTIAL / EXPERIMENTAL

This packet remains strictly INTERLEAVED_LIST work: denominator `17^32`,
`mca_counted=false`. It is not an MCA row, not protocol evidence, and not a
global obstruction.

## Objective

The previous multiscale quotient branch showed that order 16 and order 32 pass
the block-count guards, but the first feasible schedules have full-rank
quotient interpolation matrices. This branch adds RANK_FEEDBACK: after each
fully guarded schedule is audited, the scanner adds a no-good cut for that
active partition pattern and asks CP-SAT for a different schedule.

## Method

For each order, the scanner:

1. checks whether a row-count structural-defect schedule is feasible;
2. solves the fully constrained block-count model;
3. audits the quotient interpolation matrix;
4. adds a no-good cut forbidding the same active partition pattern;
5. repeats for a bounded number of samples.

The target is positive nullity at the quotient interpolation layer. A Sage
`GF(17^32)` lift/audit is still not claimed here.

## Result

The bounded run is recorded in the JSON ledger.

```text
orders tested = 16, 32
samples per order = 4
total schedules audited = 8
positive nullity schedules = 0

order 16:
  structural-defect screen = INFEASIBLE
  audited ranks/nullities = 48/0, 48/0, 48/0, 48/0

order 32:
  structural-defect screen = INFEASIBLE
  audited ranks/nullities = 96/0, 96/0, 96/0, 96/0

status = EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_FULL_RANK_FRONT / PARTIAL / EXPERIMENTAL
```

The tested rank-feedback front did generate distinct fully guarded schedules,
but all audited quotient interpolation matrices were full rank.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track rank-feedback quotient
  search;
- global obstruction outside the tested rank-feedback quotient schedules.
