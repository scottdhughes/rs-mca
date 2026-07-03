# M1 a327 random-matroid rank-feedback v2

Status: EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_PROXY_FULL_RANK /
PARTIAL / EXPERIMENTAL.

This packet follows `3d6bfd4` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Objective

The previous random-matroid functional-lift target had:

```text
template = random_matroid_seeded_0_m6
functional classes = 35
functional span rank = 5
best quotient matrix = 1211 x 714
proxy rank/nullity over GF(12289) = 714 / 0
exact GF(17^32) attempt = timeout
```

This branch tests nearby `random_matroid_seeded_0_m6`-style templates before
doing any exact Sage audit. The search objective is to repair the functional
span and find proxy-positive quotient nullity while preserving the selected
support ledger.

## Result

The bounded v2 front tested:

```text
templates tested = 7
systems tested = 14
proxy cases tested = 6
proxy-positive candidates = 0
```

The best candidate was:

```text
template = random_matroid_feedback_seed_1_m6
assignment = sorted_block
supports = [327,327,327,327,327,327,327]
pair7 counts = [204,204,204,204,204]
max pair count = 204
functional classes = 49
functional span rank = 6
annihilator dimension = 0
best quotient matrix = 1327 x 1086
proxy rank/nullity over GF(12289) = 1086 / 0
failure = RANK_FEEDBACK_PROXY_FULL_RANK
```

This is useful because the best v2 template fixes the rank-5 functional-span
issue from `3d6bfd4`. It does not yet give a lift: the best proxy quotient is
still full rank.

The failure ledger is:

```text
RANK_FEEDBACK_PROXY_FULL_RANK = 6
RANK_FEEDBACK_DIAGONAL_ANNIHILATOR = 4
RANK_FEEDBACK_PROXY_NOT_RUN = 4
```

`RANK_FEEDBACK_PROXY_NOT_RUN` is an auxiliary execution label for candidates
outside the six-case proxy budget. It is not a mathematical conclusion about
those four candidates.

## Tool choice

This branch uses Python for the bounded proxy screen and a vectorized modular
row-echelon rank over `GF(12289)`. Sage remains the certificate tool for any
future exact `GF(17^32)` candidate, but no exact Sage audit is justified until a
proxy-positive quotient appears.

PARI/GP, Singular, Macaulay2, and `msolve` remain useful secondary tools if the
rank-feedback problem is reformulated as a module, syzygy, or determinantal
proxy problem. They are not first-line tools for this checkpoint because the
current object is a structured finite-field linear quotient, not a nonlinear
polynomial solve.

## Interpretation

This branch does not prove a selected-class obstruction. It says:

- nearby random-matroid mutations can repair functional span rank to `6`;
- the tested proxy quotients are still full rank;
- no proxy-positive candidate was found in the six-case proxy front;
- no exact Sage `GF(17^32)` audit was run in this branch.

The next search should bias harder toward quotient nullity, not merely full
functional span. Good next levers are basis-profile diversity, lower
`q_variable_count` with deliberately dependent nonbasis constraints, and
template mutations scored directly by proxy nullity before any exact-field work.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
