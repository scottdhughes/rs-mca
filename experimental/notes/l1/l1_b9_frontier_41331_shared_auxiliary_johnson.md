# L1 B9 Frontier 41331: Shared Auxiliary-Johnson Owner

## Status

PROVED-LOCAL / EXACT THEOREM-SCOPE AUDIT / FRESH INDEPENDENT AND CROSS-MODEL
GREEN / BANKED.

This note treats only the frozen sequential row

```text
(q,n,k,sigma,ell,M,b) = (19,18,5,3,4,3,2).
```

It closes the existing-owner audit for

```text
(ell,d,r,t,a_i) = (4,4,1,3,(3,3,1)),
(G2,GR)          = (2,4),
```

and records the correct scope of the already-proved fixed-`(D_0,R_0)`
auxiliary-Johnson owner.  It does not prove a new CRT or rank lemma, does not
extend to `m>2`, and does not apply anything to PR `#763`.

## Exact 41331 owner partition

The target row has

```text
binom(2,1) * (3!/2!) * binom(4,3)^2 * binom(4,1) = 384
```

canonical labelled support assignments.  Because `d=ell=4`, the missed core
is the entire four-point core.  Hence there is no restored-core refinement:
the selected eight-point cofactor support is already the full agreement
support.

In the frozen first-match order

```text
PAID_PERIODIC_SUPPORT_COUNT
PAID_INVARIANT_QUOTIENT_DESCENT
PAID_AUXILIARY_JOHNSON
PAID_GLOBAL_JOHNSON
PAID_B11_G2
PAID_B11_GR
UNPAID_PRIMITIVE
```

the exact histogram is

```text
PAID_PERIODIC_SUPPORT_COUNT:       1
PAID_INVARIANT_QUOTIENT_DESCENT:   0
PAID_AUXILIARY_JOHNSON:          383
PAID_GLOBAL_JOHNSON:               0
PAID_B11_G2:                       0
PAID_B11_GR:                       0
UNPAID_PRIMITIVE:                  0
```

The unique periodic support is

```text
{4,5,6,8,13,14,15,17},
```

fixed by shift nine.  Quotient descent remains fail-closed: support
periodicity alone does not certify descent of the evaluation domain, received
data, or explaining polynomial.

This pattern partition is diagnostic.  Its periodic first-match label does
not create an additional charge: every target codeword is already contained
in the shared auxiliary-list envelope below.

## The layer-level owner

Corollary `cor:capf-pma-johnson` in
`experimental/cap25_cap_v13_raw.tex` bounds a whole fixed
`(D_0,R_0)` layer, not one support pattern or one occupancy profile.  For
`d=4,r=1`,

```text
|T| = M*ell = 12,
a   = sigma+d+1-r = 7,
a^2-d|T| = 49-48 = 1,
floor(|T|(a-d)/(a^2-d|T|)) = 36.
```

There is one missed-core choice and two retained-background choices:

```text
binom(4,4) * binom(2,1) = 2.
```

Therefore all codewords with these exact `d,r` coordinates satisfy

```text
# {d=4,r=1 codewords} <= 2*36 = 72.
```

The injection is profile-blind.  For each fixed layer, the quotient

```text
G_P = (P-P_star)/L_{Y\D_0}
```

determines `P` and agrees with the same auxiliary word on at least seven
points of the same twelve-point petal domain.  Thus the bound applies once to
the union over every admissible `t` and occupancy multiset `a_i` in the
layer.

## Exact shared scope

The frozen profile ledger contains fifteen admissible `d=4,r=1` cells.  They
are disjoint exact-agreement cells and together exhaust the non-planted
`d=4,r=1` layer represented by the ledger.

| `t` | `a_i` | prior route | current charge |
|---:|---|---|---:|
| 2 | `(4,4)` | full petal | 114 |
| 2 | `(4,3)` | unresolved | 912 |
| 3 | `(4,4,4)` | full petal | 38 |
| 3 | `(4,4,3)` | global Johnson | 456 |
| 3 | `(4,4,2)` | global Johnson | 684 |
| 3 | `(4,4,1)` | global Johnson | 456 |
| 3 | `(4,3,3)` | global Johnson | 1,824 |
| 3 | `(4,3,2)` | global Johnson | 5,472 |
| 3 | `(4,3,1)` | global Johnson | 3,648 |
| 3 | `(4,2,2)` | global Johnson | 4,104 |
| 3 | `(4,2,1)` | unresolved | 5,472 |
| 3 | `(3,3,3)` | global Johnson | 46,208 |
| 3 | `(3,3,2)` | global Johnson | 207,936 |
| 3 | `(3,3,1)` | unresolved | 138,624 |
| 3 | `(3,2,2)` | unresolved / existing carrier | 72 |

Their post-32221 ledger charges sum to `416,020`.  The previous `72` was
attached only to `(3,2,2)`, although the theorem cited there already bounds
the full fixed layer.  The corrected bookkeeping keeps that `72` once as a
shared-envelope carrier and gives the other fourteen cells zero incremental
charge:

```text
416,020 -> 72.
```

The zeroes are not standalone profile bounds.  They mean only that those
disjoint cells are covered by the common envelope whose single charge is
carried on `(3,2,2)`.

## Ledger consequence

After exact certificate replay and fresh independent and Claude cross-model
GREEN reviews, the post-32221 finite ledger banks

```text
all-profile: 1,192,927 -> 776,979,
unresolved:    357,763 -> 212,755.
```

The unresolved subtotal follows the existing ledger convention: the shared
`72` carrier remains attached to an original B11-unresolved row, so it is
included once.  Excluding paid-owner charges entirely would give a different
quantity and is not claimed here.

The next largest unchanged unresolved cell is

```text
(ell,d,r,t,a_i) = (4,4,0,3,(3,3,2)),
(G2,GR)          = (2,5),
charge           = 288*19^2 = 103,968.
```

Its owner status is a separate next obligation.  No payment for that row is
banked in this note.

The load-bearing review records are

- `experimental/notes/l1/l1_b9_frontier_41331_shared_auxiliary_independent_review.md`;
- `experimental/notes/l1/l1_b9_frontier_41331_shared_auxiliary_cross_model_review.md`.

Both authorize the local ledger and are content-addressed by the frozen
shared-ledger certificate.

## Reproducibility and stop conditions

The owner-partition verifier must certify all 384 ordered assignments, the
absence of restored-core refinements, the unique periodic mask, the strict
auxiliary margin, and zero unpaid patterns.  The shared-ledger verifier must
reconstruct the post-32221 rows, select exactly the fifteen `d=4,r=1` cells,
content-address the prior `72` certificate, charge the common envelope once,
and reject at least the following mutations:

- duplicate or missing profile cells;
- a false restored-core refinement;
- a mutated periodic mask or owner order;
- a non-strict Johnson margin;
- multiplication of `36` by patterns or profiles;
- a duplicate `+72` charge;
- drift in the prior ledger or theorem-source link.

Stop if the deterministic census, layer identity, or independent review does
not pass.  Do not replace the shared envelope by per-pattern charges, do not
add the periodic `+1`, and do not promote this local bookkeeping correction
to a global theorem.
