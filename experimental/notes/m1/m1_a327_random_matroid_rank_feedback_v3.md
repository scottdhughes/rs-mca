# M1 a327 random-matroid rank-feedback v3

Status: EXACT_EXTRACTION_NO_A327 / RANK_FEEDBACK_PROXY_FULL_RANK /
PARTIAL / EXPERIMENTAL.

This packet follows `2dcae46` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, and not a global `Lambda_mu(C,327) <= 6`
claim.

## Objective

The v2 branch showed that nearby random-matroid mutation can repair the
functional span rank:

```text
v2 systems tested = 14
best template = random_matroid_feedback_seed_1_m6
functional span rank = 6
best proxy rank/nullity over GF(12289) = 1086 / 0
```

This v3 branch keeps the search in proxy-land and makes quotient nullity the
primary gate. It generates a broader deterministic random-matroid neighborhood,
rejects candidates unless they pass the structural filters, and tests multiple
functional-basis profiles over `GF(12289)` before any exact Sage work.

## Result

The bounded v3 sweep tested:

```text
templates tested = 24
systems tested = 96
structural-pass candidates = 84
proxy-ranked candidates = 8
proxy-ranked basis profiles = 16
proxy-positive candidates = 0
```

The best candidate was:

```text
template = random_matroid_v3_seed_017_m6
assignment = sorted_block
supports = [327,327,327,327,327,327,327]
pair7 counts = [233,233,233,233,233]
max pair count = 233
functional classes = 39
functional span rank = 6
annihilator dimension = 0
best basis = deterministic_random_basis_2
best quotient matrix = 1589 x 1348
proxy rank/nullity over GF(12289) = 1348 / 0
failure = RANK_FEEDBACK_PROXY_FULL_RANK
```

The failure ledger is:

```text
RANK_FEEDBACK_LOW_FUNCTIONAL_SPAN = 12
RANK_FEEDBACK_PROXY_FULL_RANK = 8
RANK_FEEDBACK_PROXY_PENDING = 76
```

`RANK_FEEDBACK_PROXY_PENDING` is an execution-scope label for structurally
valid candidates outside the bounded proxy budget. It is not a mathematical
negative for those 76 candidates.

## Interpretation

This branch makes real progress on scope and filtering, but not on nullity:

- the search expanded from 14 systems to 96 systems;
- most candidates passed the structural filters;
- the best candidate had stronger pair7 slack than v2;
- multiple basis profiles were tested per proxy-ranked candidate;
- every tested proxy quotient remained full rank.

No exact `GF(17^32)` Sage audit was run, because the required proxy-positive
gate did not appear.

## Tool choice

Python and NumPy remain the right first-line tools here: generation, structural
screening, vectorized modular rank over `GF(12289)`, and JSON ledgers. Sage
should only be used after a proxy-positive quotient appears. Macaulay2,
Singular, and `msolve` become useful only if the next branch changes the
question into a module, syzygy, or determinantal proxy for rank rigidity.
PARI/GP and Wolfram are secondary sanity/prototyping tools, not certificate
tools for this checkpoint.

## Next step

The next branch should not simply widen this same sweep. The tested random
matroid neighborhood produces many structurally valid systems but no tested
proxy nullity. The next move should either:

- add a proxy-nullity-aware generator that explicitly engineers dependent
  nonbasis constraints, or
- start a rank-rigidity audit explaining why these functional quotient matrices
  stay full rank under the random-matroid template family.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
