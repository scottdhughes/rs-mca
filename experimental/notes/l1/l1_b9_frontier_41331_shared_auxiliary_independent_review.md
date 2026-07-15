# Independent Review: 41331 Shared Auxiliary-Johnson Ledger

## Statement audited

The implication from the proved fixed-`(D_0,R_0)` auxiliary Johnson theorem
to the shared `d=4,r=1` ledger payment:

```text
15 profile cells with post-32221 charge 416,020
    -> 2*36 = 72,
```

represented by one 72-unit carrier and fourteen zero-increment bookkeeping
rows.

## Files and commands read

The reviewer read `agents.md`, the Johnson and fixed-layer statements in
`experimental/cap25_cap_v13_raw.tex`, the complete new owner and shared-ledger
verifiers, both new certificates, the focused theorem-scope note, the prior
32221 ledger replay, the v5 common-cap source, the profile enumerator, and all
modified-file diffs.

The following commands passed:

```text
python3 experimental/scripts/verify_l1_b9_frontier_41331_owner_partition.py
python3 experimental/scripts/verify_l1_b9_frontier_41331_owner_partition.py --tamper-selftest
python3 experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py
python3 experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py --tamper-selftest
PYTHONPATH=experimental/scripts python3 experimental/scripts/verify_l1_b9_frontier_32221_reduced_crt_ledger.py
python3 -m py_compile experimental/scripts/verify_l1_b9_frontier_41331_owner_partition.py experimental/scripts/verify_l1_b9_frontier_41331_shared_auxiliary_ledger.py
git diff --check
```

## Dependencies

- PROVEN: the concrete quotient map injects the entire fixed
  `(D_0,R_0)` layer into degree-`<=4` polynomials.
- PROVEN: the auxiliary list bound is 36 per layer because
  `|T|=12`, `a=7`, `a^2-4|T|=1`, and `|T|(a-4)=36`.
- EXACT: `d=4` gives one missed-core choice and `r=1` gives two exact
  retained-background choices.
- EXACT: the fifteen profiles exhaust the nonincreasing two- or three-petal
  hit vectors in `{1,2,3,4}` with total at least seven.
- IMPORTED AND REPLAYED: the banked 32221 ledger contains 75 rows, all-profile
  total `1,192,927`, and unresolved subtotal `357,763`.

No unverified algebraic or literature lemma is introduced.

## Scope, disjointness, and edge cases

- Exact agreement data make the fifteen profile cells disjoint.
- The two exact `r=1` background layers are disjoint; a codeword agreeing at
  both background points belongs to `r=2`, not both `r=1` layers.
- Since `d=ell=4`, there is no restored-core refinement.
- A one-petal profile is impossible because seven petal agreements are
  required and one petal has size four.
- The fourteen zeroes are incremental charges under one envelope, not
  standalone zero bounds.
- The unique periodic support is already contained in the auxiliary envelope,
  so no extra `+1` is added.
- The unresolved subtotal intentionally retains the 72 carrier under the
  existing route convention.

## Independent arithmetic

An independent reconstruction, without importing either new verifier, gave:

```text
total rows:                         75
shared-scope rows:                  15
shared-scope support patterns:   3,172
shared current charge:         416,020
shared unresolved charge:      145,080
regrouped all-profile total:    776,979
regrouped unresolved subtotal:  212,755
next largest row: (4,4,0,3,(3,3,2)), charge 103,968
```

Every recorded SHA-256 link matched its current file. All normal and mutation
runs passed.

## Verdict

**GREEN - proof obligation appears satisfied with dependencies verified.**

No semantic, arithmetic, enumeration, hash-link, or certificate bug was
found.

## Ledger authorization

**YES.** Authorize the local regrouping and banking after this review and a
fresh cross-model review are persisted and hash-linked. This does not
authorize a global mixed-petal theorem.

## Remaining risks

- This does not pay the next `d=4,r=0` row.
- The possible stronger cross-`R_0` bound 36 remains unbanked.
- Positive unresolved mass remains.
- No `m>2`, PR `#763`, Lean, or global theorem consequence follows.

## Minimal next action

Persist and hash-link the fresh cross-model review, flip only the pending
ledger fields to banked GREEN, regenerate the certificate, rerun all normal
and mutation modes, and package the local bank as a small PR stacked on #775.

Files modified by this review: none.
