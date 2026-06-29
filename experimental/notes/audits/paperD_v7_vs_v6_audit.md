# Paper D v7 versus v6 audit

- **Status:** AUDIT / VERSION-PROMOTION / PROVED_PAPERD_V7_CAP.
- **Agent/model:** Codex.
- **Date:** 2026-06-29.
- **Files compared:** `tex/cs25_cap_v6.tex` and `tex/cs25_cap_v7.tex`.

## Verdict

`cs25_cap_v7.tex` is strictly better than `cs25_cap_v6.tex` as the public Paper
D source.

The v6 universal fixed-divisor MCA cap is preserved:

```text
delta*_C(2^-128) <= 1 - rho - 2^-9   for rho in {1/2,1/4,1/8},
delta*_C(2^-128) <= 1 - rho - 2^-10  for rho = 1/16.
```

v7 additionally proves a stronger first-grid cap for large official-envelope
rows.  For rates `1/2, 1/4, 1/8, 1/16`, if respectively
`k >= 127, 78, 58, 47`, with `k <= 2^40`, `q < 2^256`, and `q>n`, then

```text
delta*_C(2^-128) <= 1 - rho - 1/n.
```

## Improvements over v6

1. The deep-point list-to-CA conversion now reaches the endpoint
   `floor(delta n) <= n-k-1`, rather than the v6 strict range.
2. The standalone conversion statement now explicitly assumes `q>n`, matching
   the proof's averaging over `F \\ D` and the multiplicative-domain
   applications.
3. A new quotient-remainder locator-prefix lemma handles supports built from
   full quotient fibers plus a residual set.
4. The augmented slack-one quotient floor gives the universal first-grid list
   floor `binom(n,k+1)` for `C^+` at the word `x^(k+1)`.
5. The first-grid deep-point cap converts that list floor into CA/MCA failure
   at `delta=1-rho-1/n` under the printed binomial/field hypotheses.
6. The large challenge-envelope corollary checks the finite `k` thresholds for
   the four official rates.

## Non-claims

- v7 does not determine the exact safe threshold.
- v7 does not prove the missing aperiodic M1 or arbitrary-word L1 local limits.
- v7 does not turn the cap into a protocol soundness theorem.
- The first-grid cap has the printed large-row and `q>n` hypotheses; the older
  fixed-divisor universal cap remains useful as a uniform theorem statement.

## Checks

`tectonic -X compile tex/cs25_cap_v7.tex --outdir /tmp/cs25v7` compiled
successfully after the endpoint remark was aligned with the theorem statement.

The public references should therefore point to v7.  Scanner/source labels for
verified fixed-divisor Paper D rows should use `PROVED_PAPERD_V7_CAP`; the new
first-grid leaderboard rows use `PROVED_PAPERD_V7_FIRST_GRID`.
