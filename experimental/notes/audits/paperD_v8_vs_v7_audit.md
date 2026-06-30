# Paper D v8 versus v7 audit

- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V8_CAP.
- **Agent/model:** Codex.
- **Date:** 2026-06-30.
- **Files compared:** `tex/cs25_cap_v7.tex` and `tex/cs25_cap_v8.tex`.

## Verdict

`cs25_cap_v8.tex` is strictly better than `cs25_cap_v7.tex` as the public Paper
D source, after restoring two endpoint fixes that v8 initially regressed:

```text
Theorem A assumes q > n.
The integer-radius condition is floor(delta n) <= n-k-1.
```

The v7 universal fixed-divisor cap and first-grid cap are preserved.  The new
material is safe-side proof infrastructure: quotient-remainder support ledgers
and distinct-parameter quotient image ledgers.

## Improvements over v7

1. Adds a conservative quotient-support upper ledger: one support pays for at
   most one finite line parameter, at most `d` degree-`d` curve parameters, and
   at most one interleaved tuple.
2. Instantiates the ledger on quotient-remainder support families across a
   divisor set, with both exact union and safe-sum accounting.
3. Adds a syndrome/Hankel support-locator recurrence for support explanations.
4. Gives exact affine/projective line support-image maps and an exact
   distinct-parameter quotient ledger for declared quotient branches.
5. Gives the corresponding degree-`d` curve image ledger.
6. Adds a quotient image certificate template for future scanner/certificate
   work.

## Non-claims

- v8 does not add a new numerical leaderboard cap beyond v7's universal and
  first-grid caps.
- v8 does not prove that all bad parameters are quotient-periodic.
- v8 does not prove the aperiodic Hankel-packing theorem or the full safe-side
  M1 theorem.
- v8 does not determine an exact Proximity Prize threshold.

## Checks

`tectonic -X compile tex/cs25_cap_v8.tex --outdir /tmp/cs25v8` compiled
successfully.  Tectonic reported only an underfull hbox warning.

The public references should point to v8.  Verified fixed-divisor scanner rows
should use `PROVED_PAPERD_V8_CAP`; first-grid rows should use
`PROVED_PAPERD_V8_FIRST_GRID`.
