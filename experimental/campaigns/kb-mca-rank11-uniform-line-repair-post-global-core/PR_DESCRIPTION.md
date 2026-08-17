## Summary

This is a one-commit successor to exact parent
`d01c546f4dca70e256c18c142873821b3bb48ab5`.

A hostile cross-check found an omitted terminal branch in the parent
rank-eleven presentation: a rank-one family may drop to a fixed-pair
subfamily before the ambient dimension reaches one, and the guaranteed
subfamily can be below the fixed-pair capacity.

This PR repairs the gap by bounding the **entire rank-one family at every
residual dimension**. Its agreement conditions form a weighted affine-line
arrangement, including vertical lines at nonuniversal zeros of the direction
polynomial. Universal coordinates are used only as a count and are not
silently inserted into exact supports.

The exact all-dimension result is

```text
uniform rank-one cap       4,070,947
forced rank-one load       5,201,865
contradiction slack        1,130,918
```

The maximum occurs at residual dimension one, and the cap is nonincreasing
through all `1,048,576` residual dimensions. Thus the parent rank-eleven
terminal is closed without following another proper drop.

## Rank-twelve boundary

The same descent from nominal explanation rank eleven reaches a rank-two
family of `5,170,912` slopes. Across every ambient dimension, a proper
rank-two drop guarantees at most `2,751,700` rank-one slopes, still
`1,319,247` below the new cap. This PR does **not** claim affine error rank
12 or 13 paid. The next theorem must control the aggregate rank-two
proper-drop forest.

## Scope

- rank-eleven terminal gap: repaired;
- complete affine-error-rank-11 payment: restored after composition with the
  exact parent descent;
- active-v4 ledger movement: `0`;
- affine error rank 12: not paid;
- KoalaBear closure: not claimed.

## Verification

- exact all-dimension verifier: PASS;
- hostile mutations: `8/8` rejected;
- independent implementation: PASS;
- finite convexity controls: `1,334`;
- rank-twelve early-drop cells: `10,485,705`;
- Wolfram exact replay: PASS;
- Python/JSON and standalone TeX checks: PASS;
- no external theorem is load-bearing.

Canonical payload: `219e715b40879a13d12b6e32e02203c4b0e448d6635093080380970fa27e713b`.
