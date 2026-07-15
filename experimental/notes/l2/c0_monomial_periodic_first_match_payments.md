# Monomial c=0 periodic cells after the footprint-31 owner

**Status:** PROVED local first-match payments for the deployed monomial
`g=X^67472` owner.  These are cell payments, not a complete `c=0` parent
bound and not an official-score claim.

## The first-match rule

Work over the deployed field

```text
p = 2130706433,  n = 2097152,  t = 981105,  a = 67472.
```

The current main ledger first assigns every support whose q64 footprint has
size at most 31 to the proved q64-footprint owner.  Only the following
previously unowned periodic cells are charged here.

1. At q64 full-fiber weight `f=29`, retain only residual supports meeting at
   least three further q64 fibers.  Their total q64 footprint is at least 32.
2. At q64 full-fiber weight `f=28`, retain only residual supports meeting at
   least four further q64 fibers.  Their total q64 footprint is at least 32.
3. At q128 full-fiber weight `f=59`, delete antipodal singleton counts
   `b=1,3`, which are exactly the coarse q64 `f=29,28` cells.  Retain only
   `b=5,7`.  Writing `b+2d=59`, their minimum coarse q64 footprints are
   `d+b=32,33`, respectively, so neither returns to the first owner.

The q32 `f=14` description is a useful alternate-scale corollary but adds no
new first-match owner: every such support is already q64 `f=29` or q64
`f=28`.  It is therefore not charged in this packet.

## Exact payments

The frozen three-invariant Hahn theorem gives a fixed-residual cap for every
q64 full-fiber weight `0..29`.  Projective residual ownership at `f=29` and
the residual-pencil theorem at `f=28` give, for every projective residue ray,

```text
q64 f=29, residual footprint >=3:       1,619,679,744
q64 f=28, residual footprint >=4:      83,970,774,720
```

Restricting to the unowned residual footprints can only lower these complete
stratum caps.  The q128 odd-moment certificate gives the disjoint new cells

```text
q128 f=59, b in {5,7}:          16,501,819,170,137,728.
```

Consequently their local first-match union has cap

```text
16,501,904,760,592,192
  < 274,854,110,496,187,592 = T,
```

with exact margin

```text
258,352,205,735,595,400.
```

The proof of each component, its claimant verifier, canonical output, and an
independently written hostile replay are frozen under
`experimental/data/certificates/c0-monomial-periodic-first-match/`.

## What this does not prove

- No q64 `f<=27` aggregate is paid.
- No q128 `f=59` cell with `b>=9` is paid.
- No q128 `f=54..58`, arbitrary monic `g`, arbitrary syndrome, or complete
  `c=0` parent is paid.
- The displayed cap is per projective residue ray and cannot be multiplied or
  added globally without the corresponding source owner/compiler.
- Neither official question changes; the score remains `0/2`.

The immediate periodic wall remains the lower q64 weights and the q128
`b>=9` cells.  Later q128 `b=45,47,49` candidates are intentionally excluded
from this packet because one load-bearing size-16 census lacks a second
literal full replay and one exported dependency was misclassified.
