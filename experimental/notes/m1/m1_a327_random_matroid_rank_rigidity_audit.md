# M1 a327 random-matroid rank-rigidity audit

Status: AUDIT / RANK_RIGIDITY_PROXY_FRONT / PARTIAL / EXPERIMENTAL.

This packet follows `f50b089` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Scope

The v3 rank-feedback branch tested a broader random-matroid neighborhood:

```text
systems tested = 96
structural-pass candidates = 84
proxy-ranked candidates = 8
proxy basis profiles = 16
proxy-positive candidates = 0
```

This audit characterizes only those 16 proxy basis profiles. It is not a global
rank-rigidity theorem and does not say that unranked structural-pass candidates
or other template families cannot have proxy nullity.

## Result

All 16 proxy basis profiles were full column rank over `GF(12289)`:

```text
full column rank profiles = 16
proxy positive profiles = 0
row surplus = 241 for every audited profile
q-variable range = 1348 .. 1475
```

The matrix-shape distribution was:

```text
1589 x 1348: 4
1629 x 1388: 4
1672 x 1431: 4
1716 x 1475: 4
```

The basis-profile distribution was:

```text
deterministic_random_basis_2: 4
deterministic_random_basis_4: 4
deterministic_random_basis_7: 8
```

The best audited profile came from `random_matroid_v3_seed_017_m6`:

```text
basis = deterministic_random_basis_2
matrix = 1589 x 1348
proxy rank/nullity = 1348 / 0
pair7 counts = [233,233,233,233,233]
max pair count = 233
functional span rank = 6
```

## Interpretation

The tested random-matroid proxy front is not failing because of support,
pair-guard, forced-identity, or span-rank issues. It is failing at the quotient
rank layer: the audited basis quotients all have a fixed surplus of 241 rows and
still achieve full column rank.

That suggests the next constructive generator should explicitly create row
dependencies among nonbasis constraints, rather than continuing to mutate
templates that merely pass the structural filters.

## Tool implication

Python/NumPy remains the right tool for broader proxy search and rank-front
summaries. Sage remains reserved for exact `GF(17^32)` candidates after proxy
nullity appears. Macaulay2, Singular, or `msolve` become relevant if the next
branch reformulates this repeated full-rank phenomenon as a module, syzygy, or
determinantal-rank proxy over `GF(12289)`.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`;
- global rank rigidity outside the tested proxy front.
