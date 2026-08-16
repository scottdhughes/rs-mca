# Pull request title

[MCA] Pay affine error rank eleven by global-core descent

# Pull request body

## Summary

This is a one-commit successor to PR #1173 at exact parent
`2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`.

It pays the complete KoalaBear affine-error-rank-eleven branch.  The proof
uses complete minimizing-pair cores rather than summing the rich-flat
terminals emitted by #1173.

For a selected family in shortened row `(R+K,K,d+K)`, the inherited pointwise
support-margin theorem gives

```text
sum theta_gamma <= C_s(K),
|H_gamma| >= d+K-theta_gamma.
```

A heavy coordinate has a dichotomy.  If its incident pair-difference span is
proper, gauging by one incident pair and complete-agreement locator shortening
drops direction rank.  If the span is full, the entire direction code
vanishes there, so every selected minimizing pair equals the received pair at
that coordinate and the complete family shortens without losing a slope.

Exact evaluation over every legal shortened dimension proves that delaying a
rank drop until `K=s` is the worst case.  Starting from the unsafe post-near
load

```text
274,980,728,111,260,144
```

the rank `10 -> ... -> 1` descent forces

```text
5,201,865
```

slopes in the final row `(1,048,577,1,67,473)`.

At rank one, coordinates are weighted affine lines in the
`(slope,constant)` plane.  Cross-clone pair counting bounds points without a
majority clone class by `483`.  Dominant-line resource counting, followed by
an exact convex endpoint reduction over 271 feasible deficiency vectors,
bounds the remaining points by `4,070,464`.  Hence

```text
rank-one upper bound   4,070,947
forced rank-one load   5,201,865
contradiction slack    1,130,918
```

Restoring the disjoint near-rational charge `134,944` pays the complete affine
error rank eleven branch.

## Scope

- post-near affine error rank eleven: paid;
- complete affine error rank eleven branch: paid;
- active-v4 ledger movement: `0`;
- affine error rank twelve: open;
- KoalaBear closure: not claimed.

The shortening proof uses complete scalar agreement domains.  It does not
swap coordinates into arbitrary exact supports, transport stale minimizing
pairs as optimizers, sum nested rank loads, or sum unrelated rich-flat
certificates.

## Verification

- primary exact verifier: PASS;
- all deployed rank/dimension cells checked with no monotonicity decrease;
- separate exact product/recurrence audit: PASS;
- rank-one endpoint enumeration: PASS;
- 138 small low-dominant compositions: PASS;
- 1,500 small weighted high-resource controls: PASS;
- hostile mutations: `8/8` rejected;
- Wolfram exact recurrence and endpoint replay: PASS;
- standalone source-integration fragment compile: PASS;
- manifest and file hashes: PASS;
- adversarial mathematics audit: GREEN for the stated branch;
- literature sweep: no external theorem is load-bearing.

Canonical payload is recorded in
`experimental/data/certificates/kb-mca-rank11-global-core-descent-v1/manifest.json`.

## Dependency and next theorem

This PR must integrate after #1173.

The strongest successor is the affine-error-rank-twelve analogue.  The first
complete-core descent produces large rank-ten hyperplane families.  A useful
next theorem must exploit their common-core provenance jointly—most plausibly
through two-coordinate synchronization or a Wronskian/subspace-design
incidence inequality.  The generic rank-ten split alone is insufficient.

## Review boundary

- head repository: `scottdhughes/rs-mca`
- head branch: `codex/kb-mca-rank11-global-core-descent-post-1173`
- exact parent: `2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804`
