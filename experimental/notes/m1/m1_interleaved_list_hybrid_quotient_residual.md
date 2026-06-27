# M1 interleaved-list hybrid quotient-residual certificate

Status: PROOF_RECORD / LOWER_BOUND / ROUTE_CUT / PARTIAL / EXPERIMENTAL

This note improves the interleaved-list row

```text
C = RS[F_17^32,H,256],    |H| = 512
```

from the pure quotient-fiber agreement `a=320` to a hybrid
quotient-residual agreement `a=326`.

This is an `INTERLEAVED_LIST` result only.  It is not an MCA `N_bad` row and
does not claim protocol soundness, ordinary list decoding, exact
`Lambda_mu(C,326)`, or exact `delta*_C`.

## Gate and track

The interleaved-list denominator is

```text
|F| = 17^32.
```

The list-track gate is

```text
2^128 L_lower > |F|.
```

Since

```text
floor(17^32 / 2^128) = 6,
```

it suffices to construct seven retained interleaved-list witnesses.

## Quotient core

Use the quotient map

```text
x -> x^32
```

on the order-512 subgroup `H`.  The fibers have size `32`, the quotient has
size `16`, and quotient subsets of size `10` give the base agreement

```text
10 * 32 = 320.
```

The high-coefficient pigeonhole fiber used in the pure quotient packet contains
`32` quotient witnesses.  The pure quotient construction already proves
`Lambda_mu(C,320) >= 28`.

## Hybrid residual schedule

Select seven witnesses from that 32-witness quotient packet.  Instead of using
only the quotient received word, choose received-word values inside quotient
fibers according to a value-class schedule.  The key point is that a received
word on `H` may choose different values at different points inside a quotient
fiber, as long as every coordinate chooses one value.

The verifier records the selected witnesses and the per-quotient schedule.  The
resulting agreement counts are

```text
327, 327, 327, 326, 326, 326, 327.
```

Therefore

```text
Lambda_mu(C,326) >= 7.
```

This clears the interleaved-list numerical gate over `|F| = 17^32`.

## Packet upper bound

For this same 32-witness quotient packet, the verifier also computes a
value-class total-agreement upper bound over every 7-subset of the 32 quotient
witnesses.  The maximum possible total agreement is

```text
2304.
```

Seven witnesses all agreeing at level `a` would require total agreement at
least `7a`.  Hence this specific quotient packet cannot produce seven
witnesses at any agreement

```text
a >= 330.
```

The narrow interval

```text
327 <= a <= 329
```

remains open for this quotient packet, and other non-quotient or more general
hybrid families are not exhausted.

## Sage audit

The Sage audit independently reconstructs:

- `GF(17^32)`;
- the order-512 subgroup `H`;
- the selected seven degree-`<256` codewords;
- the explicit received word on `H`;
- the agreement counts above;
- distinct witness descriptors and hashes.

## Status ledger

PROOF_RECORD / LOWER_BOUND:

- `Lambda_mu(C,326) >= 7` for the standard interleaved-list predicate.

ROUTE_CUT:

- Within the same 32-witness quotient packet, value-class total agreement rules
  out seven witnesses at `a >= 330`.

PARTIAL:

- `327 <= a <= 329` remains open inside this quotient packet.
- `330 <= a <= 372` remains open for other hybrid or non-quotient families.

NOT CLAIMED:

- MCA `N_bad`.
- Protocol soundness failure.
- Ordinary list-decoding theorem beyond the stated interleaved-list predicate.
- Exact `Lambda_mu(C,326)`.
- Exact `delta*_C`.
- Exhaustion of non-quotient or other hybrid families.
