# M1 a=327 Proxy-Positive Exact Extraction

Status:

`MULTIPRIME_ROBUST_PROXY_CANDIDATE / PARTIAL / EXPERIMENTAL`

Track:

`INTERLEAVED_LIST`

Row:

`RS[F_17^32,H,256]`

Agreement target:

`a = 327`

## Summary

This packet follows the first proxy-positive incumbent-guided target mutation
checkpoint:

`10ad190 add M1 a327 incumbent guided target mutation`

That checkpoint found proxy target/codeword tuples over `GF(12289)` with:

- best proxy max-min: `329`
- best proxy agreement vector: `[329,330,329,329,329,329,329]`
- proxy-positive systems: `13`
- proxy candidate samples: `52`

This branch asks whether those proxy hits are single-prime artifacts or robust
across several unrelated proxy fields.

## Multi-Prime Diagnostic

Proxy fields tested:

- `GF(7681)`
- `GF(10753)`
- `GF(11777)`
- `GF(12289)`
- `GF(13313)`

All primes satisfy `p == 1 mod 512`, so each has a multiplicative subgroup of
order `512` for the proxy Reed-Solomon row.

Result:

- proxy-positive systems tested: `13`
- proxy candidate samples represented by the source packet: `52`
- multi-prime robust systems: `13`
- rank-drop systems relative to the `GF(12289)` source rank: `0`
- rank/nullity across all tested systems and primes: `640 / 896`

Every source proxy-positive system remains proxy-positive over all five tested
proxy primes.  The best systems retain proxy max-min `329`, and the lower
robust systems retain proxy max-min at least `327`.

This makes the simplest explanation, "the `GF(12289)` hit is just a
single-prime accident," unlikely.

## Exact-Field Prefix Audit

The Sage audit reconstructs the top robust system over `GF(17^32)` and checks
small exact row prefixes:

- audited robust systems: `1`
- exact prefix row counts: `16, 32`
- prefix rank drops: `0`

The audited prefixes are full row rank:

- `16` rows have rank `16`
- `32` rows have rank `32`

This is only a sanity check.  It does not replace full exact nullspace
extraction over `GF(17^32)`.

## Interpretation

The proxy-positive target systems are multi-prime robust.  This strengthens the
case that the incumbent-guided mutation found a real structural pattern in the
target equations, not just a random proxy-field coincidence.

However, no exact `GF(17^32)` codeword tuple has been extracted.  The prior
bounded lift audit showed that reducing proxy coefficients mod `17` and
evaluating them over `GF(17^32)` produces degenerate codewords and no
`a=327` witness.  The current packet does not solve that extraction problem.

## Proof Status

Valid:

- The 13 source proxy-positive target systems are robust over five
  `p == 1 mod 512` proxy fields.
- The top robust system has no immediate rank drop in the first 16 or 32 exact
  `GF(17^32)` target rows.

Not claimed:

- no `a=327` interleaved-list proof record;
- no global `Lambda_mu(C,327) <= 6`;
- no MCA `N_bad`;
- no protocol soundness failure;
- no ordinary list-decoding theorem beyond the stated interleaved-list
  predicate;
- no exact `Lambda_mu`;
- no exact `delta*_C`;
- no improvement over PR `#133`;
- no full `GF(17^32)` nullspace extraction.

## Next Step

The next attack should stay focused on exact extraction for these robust
systems:

1. use the shared rank/nullity and pivot structure across proxy primes to choose
   free-column schedules;
2. solve exact constrained systems over `GF(17^32)` without dense full RREF;
3. evaluate any exact samples directly, even if they do not satisfy every
   target row;
4. run the exact received-word rescheduler;
5. promote only if Sage verifies seven distinct degree-`<256` codewords and one
   received word with agreement at least `327` for every witness.
