# M1 a=327 Robust-Proxy Constrained Extraction

Status:

`CONSTRAINED_SCHEDULE_PROXY_A327 / PARTIAL / EXPERIMENTAL`

Track:

`INTERLEAVED_LIST`

Row:

`RS[F_17^32,H,256]`

Agreement target:

`a = 327`

## Summary

This packet continues from:

`bf374dc add M1 a327 proxy-positive exact extraction`

That checkpoint showed that all 13 proxy-positive target systems from
`10ad190` remain proxy-positive over five primes:

`7681, 10753, 11777, 12289, 13313`.

This branch asks whether the proxy-positive systems share stable pivot/free
structure and whether small constrained schedules can preserve the `a>=327`
proxy behavior.

## Proxy Pivot and Free-Column Stability

For all 13 robust proxy systems:

- rank: `640`
- nullity: `896`
- common pivot columns across all five primes: `640`
- common free columns across all five primes: `896`
- pivot order stable: yes
- free-column order stable: yes
- pivot-row order stable: yes

Thus the robust proxy behavior is not only a rank/nullity coincidence.  The
echelon structure is stable across all five tested proxy fields.

## Constrained Free-Column Schedules

The scanner tested deterministic free-column schedules built from:

- common free columns;
- per-witness-block common free columns;
- proxy-candidate support intersected with common free columns;
- deterministic random common-free subsets.

Best schedule:

`proxy_support_common_free_24`

Result:

- systems with constrained-schedule proxy `a>=327`: `13 / 13`
- best schedule candidate prime count: `5 / 5`
- best proxy schedule max-min: `329`
- best proxy schedule capacity upper bound: `459`

This strengthens the interpretation that the proxy hit comes from a stable
free-column mechanism, not an unstable sample accident.

## Exact GF(17^32) Bounded Audit

The Sage audit checks the top robust system over `GF(17^32)`:

- exact row subsets:
  - `proxy_pivot_rows_64`
  - `fiber_diverse_rows_64`
- both subsets have full row rank `64`;
- no exact row-subset rank drop was found.

The audit also solves the 64-row `proxy_pivot_rows_64` subsystem using the
first 64 stable pivot columns and the best 24-column free schedule.  Direct
evaluation over `GF(17^32)` gives:

- partial solve status: `PARTIAL_SOLVE_OK`
- exact direct-evaluation status: `EXACT_DEGENERATE_CODEWORDS`
- exact capacity upper bound: `438`
- exact rescheduled max-min: `256`

So this bounded exact constrained solve does not produce an `a=327` witness.

## Interpretation

The positive proxy signal is now highly structured:

- robust across five proxy primes;
- stable pivot columns;
- stable free columns;
- stable pivot rows;
- constrained free-column schedules preserve proxy `a>=327`.

But the first exact constrained lift still collapses to degenerate codewords.
This suggests that the next extraction step must solve a larger or differently
chosen exact subsystem, rather than simply lifting the most obvious free-column
schedule.

## Proof Status

Valid:

- The 13 proxy-positive systems have identical stable pivot/free structure
  across the tested proxy primes.
- The best constrained schedule reaches proxy `a>=327` over all five tested
  primes.
- The bounded exact `GF(17^32)` audit finds full row rank in two meaningful
  64-row subsets and no exact witness from the first partial solve.

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

Use the stable proxy pivot/free-column data to try deeper exact constrained
extraction:

1. solve larger proxy-pivot subsystems, such as 96 or 128 rows, if tractable;
2. vary free-column values rather than fixing all chosen free columns to `1`;
3. test schedules with 1, 2, and 4 free columns per witness block;
4. use the stable proxy pivot rows to build block or quotient-aware exact
   elimination;
5. evaluate exact vectors directly and run the received-word rescheduler before
   attempting any board-facing claim.
