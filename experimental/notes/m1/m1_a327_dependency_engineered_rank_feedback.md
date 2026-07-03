# M1 a327 dependency-engineered rank feedback

Status: EXACT_EXTRACTION_NO_A327 / DEPENDENCY_PROXY_FULL_RANK /
PARTIAL / EXPERIMENTAL.

This packet follows `614bf1c` and remains strictly INTERLEAVED_LIST work:
denominator `17^32`, `mca_counted=false`. It is not an MCA row, not protocol
soundness, not exact `Lambda_mu`, not exact `delta*_C`, and not a global
`Lambda_mu(C,327) <= 6` claim.

## Objective

The v3 random-matroid sweep found many structurally valid systems, but every
tested proxy quotient stayed full column rank. The rank-rigidity audit then
showed:

```text
audited proxy basis profiles = 16
full column rank profiles = 16
row surplus = 241
proxy-positive profiles = 0
```

This branch keeps the search in Python/NumPy proxy-land, but changes the
generator objective. Instead of only mutating templates, it assigns selected
classes to coordinates using dependency-oriented layouts:

- signature fiber blocks;
- signature residue blocks;
- pair7 signature blocks;
- dependency twin interleaving;
- fiber factor packing;
- seeded dependency shuffles.

The intended effect is to create duplicate or nested functional support sets,
shared factors, and repeated row geometry before proxy rank is computed.

## Result

The bounded dependency-engineered sweep tested:

```text
templates tested = 18
systems tested = 108
structural-pass candidates = 96
proxy-ranked candidates = 8
proxy-ranked basis profiles = 24
proxy-positive candidates = 0
```

The best candidate was:

```text
template = random_matroid_v3_seed_007_m6
assignment = signature_fiber_blocks
supports = [327,327,327,327,327,327,327]
pair7 counts = [233,233,233,233,233]
max pair count = 233
functional classes = 47
functional span rank = 6
annihilator dimension = 0
forced functional identities = 0
best basis = deterministic_random_basis_10
best quotient matrix = 1626 x 1385
proxy rank/nullity over GF(12289) = 1385 / 0
failure = DEPENDENCY_PROXY_FULL_RANK
```

The support-dependency metrics for the best candidate were:

```text
duplicate support groups = 14
duplicate support pairs = 51
nested support pairs = 66
support overlap total = 2347
```

So the dependency assignment did change the functional support geometry. It did
not produce proxy quotient nullity in the bounded front.

Failure counts:

```text
DEPENDENCY_LOW_FUNCTIONAL_SPAN = 12
DEPENDENCY_PROXY_FULL_RANK = 8
DEPENDENCY_PROXY_PENDING = 88
```

`DEPENDENCY_PROXY_PENDING` is an execution-scope label for structurally valid
candidates outside the bounded proxy budget. It is not a mathematical negative
for those candidates.

## Interpretation

The branch confirms that support-set duplication and nesting alone are not
enough. The best candidate had clear support-level dependency signals, but its
ranked quotient basis profiles still had full column rank.

The obstruction is now more specific:

```text
support geometry can be made dependent,
but the nonbasis quotient rows remain independent over GF(12289).
```

No exact `GF(17^32)` Sage audit was run, because the proxy-positive gate did
not appear.

## Tool direction

Python/NumPy remains the right tool for proxy generation and modular rank. The
next move should not be another blind widening of assignment strategies. It
should either engineer dependencies directly in the quotient-row coordinates or
switch to the module/syzygy proxy branch with Macaulay2 or Singular.

Sage should still wait until proxy nullity appears. PARI/GP and Wolfram remain
secondary sanity/prototyping tools, not final certificate tools here.

## Non-claims

This packet does not claim:

- an `a=327` certificate;
- MCA `N_bad`;
- protocol soundness;
- ordinary list decoding beyond the stated interleaved-list predicate;
- global `Lambda_mu(C,327) <= 6`;
- exact `Lambda_mu`;
- exact `delta*_C`.
