# Rank-16 fixed-pair active-pencil occupancy cap 130

## Status

`PROVED` as a local theorem under the frozen fixed-pair tail and
DPW/extactic/Chern-stripping interfaces in the accompanying certificate
packet.

## Theorem

For every core `0 <= c <= 832`, fix a surviving rank-16 fixed-pair active
pencil and its complete actual tails.  Under the source interface

```text
d = 5,116-c,
b = 62,356+c,
sum_P |T_P| >= 131b,
|union_P T_P| <= 913,633,
```

with row and column degree at most 14 and the printed characteristic-valid
DPW/extactic/Chern-stripping theorem, the active-pencil occupancy is at most
130.

The exact scan covers all 28 legal selected-131 grid profiles, including every
nonsquare profile, and all 833 cores.  Its unique minimum occurs at `c=0` and
the `13x13` profile:

```text
need     = 8,168,636
capacity = 8,166,421
margin   = 2,215
```

An adjacent selected-130 negative control has margin `-29,445`.  This proves
only that the present relaxation stops at cap 130; it does not exhibit a
source configuration of occupancy 130 and does not prove cap 129.

## Verification

The certificate directory contains the two consumed theorem objects, their
hostile audits, the source-normalized cap-130 proof, a Python claimant replay,
and an independent Ruby reconstruction.  Both Python modes and the Ruby audit
byte-match their frozen expected outputs.

## Nonclaims And Remaining Wall

This theorem supplies no active-hyperplane owner bound, no rank-16 parent or
recurrence payment, and no official-score change.  The next consumer must
combine cap 130 with a separately proved source-valid owner/mass theorem; that
compiler is intentionally absent from this packet.
