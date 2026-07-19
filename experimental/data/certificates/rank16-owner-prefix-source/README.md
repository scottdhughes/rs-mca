# Rank-16 owner-prefix source certificate

This certificate supports only the finite branch-qualified owner-prefix
statement in
`experimental/notes/l2/rank16_owner_prefix_source.md`.

Run from the repository root:

```sh
python3 experimental/scripts/verify_rank16_owner_prefix_source.py
python3 -O experimental/scripts/verify_rank16_owner_prefix_source.py
python3 experimental/scripts/verify_rank16_owner_prefix_source.py --self-test-mutations
```

The normal and optimized outputs must both equal
`verify_rank16_owner_prefix_source.expected.txt` byte-for-byte. The mutation
self-test must catch all seven named mutations.

The verifier is Python-standard-library only. It reconstructs the three
dyadic profile counts, the exact source A-rank and profile-restricted
lexicographic rank, both local collision caps, both congruence-cover deficits,
the inherited first-match subtotal from the pinned source compiler, the
exact-F prefix, the terminal exact-F rank, and the endpoint margins.

The scalar stage is conditional on the literal fixed core `C0` at PR #890
head `a5b98c75d0e3732e9659d8fd220c821329e572e4`; the frozen patch digest is
`d967f805d1e70074eced0599a0e70e261d3317047e10ec78e419059156642307`.
This dependency is not a claim that PR #890 is merged.

The theorem is cardinality accounting only. It does not construct a
source-incidence matching, cover the complete residual, or move the official
score from `0/2`.
