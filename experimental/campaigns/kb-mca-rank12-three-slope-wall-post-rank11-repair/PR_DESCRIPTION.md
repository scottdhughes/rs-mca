## Summary

Stacked on exact parent `8911e26e78c8d91173c413f079a13f88a04701fe`.

This PR sharpens the affine-error-rank-12 route by comparing every proper
rank-two drop with the rank-one cap at the **same shortened dimension**.  A
heavy/light stability analysis of the weighted-line endpoint proves that a
proper drop is impossible at every ambient dimension `K>=262,712`.

The exact first surviving cell is

```text
ambient dimension                 262,711
guaranteed rank-one subfamily   1,301,847
dimension-matched cap           1,301,850
shortfall                               3
```

At the adjacent cell `K=262,712`, the guarantee is `1,301,850` against cap
`1,301,848`, giving slack `2`.  The entire rank-two family must therefore
whole-shorten through that cell.

## Scope

- result: proved dimension-matched route cut;
- affine error rank 12: not paid;
- affine error rank 13: not paid;
- active-v4 ledger movement: `0`;
- KoalaBear closure: not claimed.

The next theorem must classify or exclude the near-extremal two-dominant-line
configuration at `K=262,711`; another endpoint-only estimate is insufficient.

## Verification

- every ambient cell `262,711..1,048,576`: exact scan;
- every endpoint profile in the active window: exact scan;
- independent selected-cell and direct endpoint audit: PASS;
- hostile mutations: `8/8` rejected;
- Wolfram exact boundary replay: PASS;
- no external theorem is load-bearing.

Canonical payload: `bdcc5cd976b51ace6cf5567a6008c49e4a0099d86c240b5dfd0b12373bcb8a90`.
