# Paper D v6 versus v5 audit

- **Status:** AUDIT / VERSION-PROMOTION.
- **Agent/model:** Codex.
- **Date:** 2026-06-29.
- **Files compared:** `tex/cs25_cap_v5.tex` and `tex/cs25_cap_v6.tex`.

## Verdict

`cs25_cap_v6.tex` is strictly better than `cs25_cap_v5.tex` as the public Paper
D source.

The numerical cap theorem is not weakened: v6 preserves the same headline
universal MCA cap,

```text
delta*_C(2^-128) <= 1 - rho - 2^-9   for rho in {1/2,1/4,1/8},
delta*_C(2^-128) <= 1 - rho - 2^-10  for rho = 1/16,
```

with the same `2^-86` uniform error floor and the same `2^-42` improvement when
`|F| >= 2n`.

## Improvements over v5

1. The title and abstract now make the result explicitly prize-facing: a
   negative band/cap, not a full threshold determination.
2. The deep-point conversion proof keeps the sharper intermediate denominator
   `q-n+k(L-1)` before relaxing to the older `q-n+kL` bound.  This does not
   change the final advertised constants, but it is a genuine tightening of the
   proof derivation.
3. A new `Prize-facing status and a completion program` section states the
   exact integer-staircase problem.
4. The new one-step threshold certificate isolates the unsafe/safe transition
   at consecutive integer agreements.
5. The conditional MCA and interleaved-list completion theorems separate the
   remaining proof obligations: quotient-profile union ledgers, aperiodic
   Hankel packing, extension-line accounting, arbitrary-word locator fibers,
   curve/projective ledgers, scanner output, and formal finite cores.
6. The bibliography now cites the Proximity Prize page directly.

## Non-changes

- v6 does not claim a tighter numerical universal cap than v5.
- v6 does not claim the full Proximity Prize threshold.
- v6 does not close the error-one profile problem.
- v6 does not prove the missing aperiodic M1 or arbitrary-word L1 local limits.

## Checks

`tectonic cs25_cap_v6.tex` compiled successfully from `tex/`.

The public references should therefore point to v6 while retaining the same
leaderboard cap constants.  Scanner/source labels should use
`PROVED_PAPERD_V6_CAP` for rows satisfying Paper D's printed
divisor/binomial/subfield hypotheses.
