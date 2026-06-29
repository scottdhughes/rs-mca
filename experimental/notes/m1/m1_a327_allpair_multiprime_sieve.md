# M1 a=327 All-Pair Multi-Prime Sieve

Status: `TESTED_EMBEDDINGS_NO_MULTIPRIME_PROXY_ANOMALY / PARTIAL / EXPERIMENTAL`

This note records a multi-prime proxy sieve for the all-pair-boundary
incidence embeddings used in the `a=327` interleaved-list search.

It is not a board update, not an exact `GF(17^32)` route cut, and not a global
upper-bound theorem.

## Target

The search stays on the interleaved-list row

```text
RS[F_17^32, H, 256]
```

with target agreement

```text
a = 327
```

The all-pair-boundary incidence multiset has:

```text
7 supports of size 327
all 21 pair intersections at 255
```

The question tested here is whether any embedding of that fixed multiset shows
a reduced scalar-locator rank anomaly across many proxy fields.

## Prime List

The proxy primes were generated with PARI/GP:

```gp
v=[]; n=1; while(#v<23, n=nextprime(n+1); if(n%512==1, v=concat(v,[n]))); print(v)
```

This produced:

```text
7681, 10753, 11777, 12289, 13313, 15361, 17921, 18433,
19457, 23041, 25601, 26113, 32257, 36353, 37889, 39937,
40961, 45569, 50177, 51713, 58369, 59393, 61441
```

Each prime is `1 mod 512`, so each proxy field has a subgroup of order 512.

## Sieve

Scanner:

```text
experimental/scripts/scan_m1_a327_allpair_multiprime_sieve.py
```

Data:

```text
experimental/data/m1_a327_allpair_multiprime_sieve.json
```

The scanner evaluated:

```text
all-pair-boundary embeddings: 515
proxy primes:                 23
rank evaluations:             11,845
```

Result:

```text
rank anomalies:       0
capacity anomalies:   0
exact-audit triggers: 0
```

Every tested embedding had reduced scalar-locator rank `6` over every proxy
prime.

## Exact-Audit Policy

Sage wrapper:

```text
experimental/scripts/audit_m1_a327_allpair_multiprime_sieve.sage
```

Exact-audit data:

```text
experimental/data/m1_a327_allpair_multiprime_sieve_exact_audit.json
```

The policy for this packet is:

```text
exact-audit only candidates that show rank or capacity anomalies across primes
```

Since the multi-prime proxy sieve found no anomalies, no exact `GF(17^32)`
candidate was audited. The Sage wrapper records this as:

```text
NO_EXACT_AUDIT_TRIGGERED
```

## Verification

Verifier:

```text
experimental/scripts/verify_m1_a327_allpair_multiprime_sieve.py
```

The verifier checks the prime list, candidate count, rank-evaluation count,
all-full-rank proxy records, zero anomaly count, and no-trigger Sage audit
ledger.

## Interpretation

This is a proxy-level route cut for the tested multi-prime all-pair-boundary
scalar-locator sieve:

```text
515 embeddings x 23 proxy fields
all reduced ranks full
```

It does not prove that the corresponding matrices are full rank over
`GF(17^32)` for all embeddings, and it does not rule out non-scalar residual
factors, non-all-pair-boundary incidence profiles, or joint codeword /
received-word constructions.

## Non-Claims

Not claimed:

- `a=327` interleaved-list certificate;
- global `Lambda_mu(C,327) <= 6`;
- MCA `N_bad`;
- protocol soundness failure;
- ordinary list-decoding theorem beyond the stated interleaved-list predicate;
- exact `Lambda_mu`;
- exact `delta*_C`;
- improvement over PR #133.

The denominator remains `|F| = 17^32`, and `mca_counted = false`.

## Next Step

All-pair-boundary scalar locator embeddings look stable across many proxy
fields. The next constructive search should leave this scalar-locator model:
use higher-degree residuals, non-boundary value-class profiles, or a solver
that jointly constructs codeword coefficients and received-word classes.
