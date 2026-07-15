# Exact nested-pattern payment for 110 Profile1792 residual cells

Claim: In the deployed base-field row and canonical first-match convention of
the integrated dyadic complete-fiber ledger, every fixed residual profile with
`e_15=32` has list size at most its exact nested 32-of-64 fiber-pattern count.
Exactly 110 of the 166 residual `e_15=32` profiles therefore lie below the old
uniform cap, with aggregate payment `904093061906432`.
Status: PROVED finite source-valid theorem and direct-ledger improvement; the
official score remains `0/2`.
Verifier: The standard-library Python claimant and independent Ruby
reconstruction replay the binary-tree census, exact profile split, and integer
add-back. Canonical outputs and `SHA256SUMS` bind the artifacts.
Consumers: The public 1,792-profile residual ledger in
`dyadic_complete_fiber_slicing_route_cut.md`; after this payment it is enough
to prove cap `128911409122285` on the remaining 1,682 profiles.
Risk-limits: No cap is proved for those 1,682 profiles, including the other 56
`e_15=32` profiles; no recurrence, rank-cell closure, Grand List theorem,
Grand MCA theorem, or score movement is claimed.

## Source ledger

Use the notation and hypotheses of
`experimental/notes/l2/dyadic_complete_fiber_slicing_route_cut.md`. In
particular, for an arbitrary received word `U`, each list polynomial `P` has
the canonical first exactly `m` agreement points `S_P`. At level
`c=2^15=32768`, the subgroup has 64 complete fibers. The integrated ledger
already proves the disjoint payment

```text
U_dyadic = 57121027290597096
```

and leaves exactly 1,792 admissible nested profiles

```text
(e_15,e_16,e_17,e_18,e_19,e_20) <= (32,15,7,3,1,0),
e_j >= 2 e_(j+1).
```

Its old sufficient target was the uniform fixed-profile cap

```text
OLD_CAP = 121502836610262.
```

All fields, polynomials, received words, agreement sets, and fibers in this
theorem are over `F_p`. The extension size `p^6` occurs only in the challenge
denominator used by the integrated ledger to derive

```text
T = 274854110496187592.
```

## Nested-pattern injection

Fix one residual profile with `e_15=32`. Map each polynomial in its literal
fixed-profile sublist to the set of its 32 complete level-15 fibers.

This map is injective. If two distinct list polynomials had the same set of
32 complete fibers, their canonical agreement sets would share at least

```text
32 * 32768 = 1048576 = K
```

coordinates. Their nonzero difference has degree at most `K-1`, which is
impossible. This is a theorem about actual first-match list elements, not an
abstract set-system assumption, and it is uniform in `U` and the syndrome.

The 64 level-15 fibers are the leaves of the binary nesting tree for the
coarser dyadic quotients. For a 32-subset of leaves, the numbers of all-one
nodes at sizes `2,4,8,16,32` are exactly
`(e_16,e_17,e_18,e_19,e_20)`. Hence a fixed-profile sublist is bounded by the
number of 32-subsets with those exact nested counts.

## Exact census and add-back

A bottom-up exact binary-tree census gives 166 residual profiles with
`e_15=32`. Of these,

```text
110 have pattern count <= 121502836610262,
 56 have larger pattern count.
```

The exact aggregate for the 110 paid profiles is

```text
904093061906432.
```

The old uniform reservation for them was

```text
110 * 121502836610262,
```

so the exact payment saves

```text
12461218965222388.
```

There remain `1792-110=1682` profiles. Euclidean division gives

```text
floor((T-U_dyadic-904093061906432)/1682)
  = 128911409122285
```

with remainder 694. Equivalently,

```text
57121027290597096
+ 904093061906432
+ 1682 * 128911409122285
= T - 694.
```

Thus a uniform cap `128911409122285` on the remaining 1,682 profiles would
close this direct deployed row. That cap remains open.

Pattern injectivity alone cannot pay all 166 `e_15=32` profiles. The largest
pattern class is

```text
(32,8,1,0,0,0): 247029899691294720,
```

already larger than `T`. The smallest unpaid `e_15=32` pattern class is
`(32,13,3,0,0,0)` with count `170870483976192`.

## Replay

```text
python3 experimental/data/certificates/profile1792-e15-pattern-payment/verify_profile1792_e15_pattern_payment.py
python3 -O experimental/data/certificates/profile1792-e15-pattern-payment/verify_profile1792_e15_pattern_payment.py
ruby --disable-gems experimental/data/certificates/profile1792-e15-pattern-payment/audit_profile1792_e15_pattern_payment.rb
```

The Python and Ruby programs independently construct the six-level binary
tree rather than importing a precomputed profile table.
