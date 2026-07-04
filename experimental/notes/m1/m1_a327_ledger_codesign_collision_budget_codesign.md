# M1 a327 ledger-codesign collision-budget codesign

Status:

EXACT_EXTRACTION_NO_A327 / CBUDGET_PROXY_FULL_RANK / PARTIAL / EXPERIMENTAL

This packet follows `2939690` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
evidence, and not a global obstruction.

## Motivation

The exact row-collision branch found `438` exact-collision profiles, but none
also cleared the `q_variable_count >= 350` budget floor. The best exact
collision had only `271` q variables. That showed a collision/q-budget tradeoff
when collisions are forced after the ledger has already been built.

This branch moves the collision constraint into the basis-selection/codesign
step: force a candidate-level support collision group into the nonbasis rows
while choosing low-support basis classes first.

## Search

The bounded run reused the ledger-codesign front and tested four collision
budget preferences:

```text
low_support_basis
low_support_not_group_support
mid_support_rank
q_budget_then_span
```

Results:

```text
structural-pass systems = 360
candidates scanned = 60
candidates with collision groups = 60
candidate collision groups = {support: 60}
basis profiles constructed = 240
exact-collision profiles = 240
q-budget profiles = 240
collision-budget profiles = 240
proxy ranked profiles = 12
proxy positive profiles = 0
```

The best collision-budget profile was:

```text
template = lcodesign_0002_basis_simple
basis = collbudget_low_support_basis_support_0_11_6_7_10_5_2
preference = low_support_basis
forced group type = support
forced group nonbasis count = 2
forced group classes = [8,9]
support = [327,327,327,327,327,327,327]
pair7 counts = [253,253,253,253,253]
max pair count = 253
functional classes = 12
functional span rank = 6
forced functional identities = 0
matrix shape = 1092 x 851
best q-variable count = 851
repeated support pairs = 1
repeated coordinate pairs = 0
repeated support-coordinate pairs = 0
proxy rank/nullity = 851 / 0
```

## Interpretation

This branch fixes the immediate failure from `2939690`: exact support collision
and q-budget are now compatible in the tested front. The previous best
collision had `q=271`; this branch constructs collision-budget profiles with
`q=851`.

The remaining obstruction is again algebraic rank. The top `12`
collision-budget profiles are full column rank over the proxy field. So the
current state is:

```text
exact support collision: achieved
q-variable budget: achieved
pair/support guards: achieved
proxy nullity: not achieved
```

No Sage `GF(17^32)` audit is warranted from this packet because no proxy
positive profile was found.

## Next Step

The next constructive branch should add a second rank-defect mechanism on top
of the successful collision-budget gate. A reasonable next branch is:

```text
m1-a327-collision-budget-syzygy-search
```

Objective:

- start from collision-budget profiles with `q_variable_count >= 350`;
- preserve exact support collisions in the nonbasis rows;
- search for repeated or linearly dependent small row blocks among the nonbasis
  constraints;
- proxy-rank only profiles with collision-budget and syzygy evidence.

Python/NumPy remain first-line. Macaulay2 or Singular become more relevant now:
the collision-budget gate is cleared, and the next object is naturally a
module/syzygy condition on the nonbasis row block. Sage should still wait for a
proxy-positive or small exact certificate.

## Non-claims

This packet does not claim:

- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- Sage `GF(17^32)` exact lift;
- any MCA/protocol consequence from this list-track proxy;
- global obstruction outside the tested ledger-codesign collision-budget front.
