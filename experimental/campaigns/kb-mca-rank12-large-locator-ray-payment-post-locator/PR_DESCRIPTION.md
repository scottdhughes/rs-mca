## Summary

Stacked on exact parent
`ed556ccb7527e1c54e58b8d151ccefd8539000ac`.

The parent proves that every proper rank-two drop carries a source-bound
common pair-core locator.  This PR pays the complete large-locator interval.
For `K>=858,619`, the locator leaves at most `174,762` coordinates of omission
excess.  Second divided differences of six frozen supports then force every
exceptional explanation into one affine correction ray.

A hostile audit caught and repairs an important monotonicity trap: a larger
actual common core can increase the rank-one capacity, so the capacity at the
minimum locator floor cannot cap the rank-one part.  This PR instead uses the
proved global all-dimension rank-one maximum.

The exact accounting is

```text
rank-one global cap          4,070,947
universal-core-aware ray cap   796,620
---------------------------------------
proper-drop cap              4,867,567
rank-two load                5,170,912
slack                          303,345
```

Hence a proper drop is impossible for every
`858,619<=K<=1,048,576`.  The whole family shortens intact through all
`189,958` top dimensions and reaches `K<=858,618`.

## Universal-core-aware ray theorem

After translating the affine ray, each nonuniversal coordinate is an affine
line in the `(gamma,c)` parameter plane.  If `u` ray-universal coordinates
occur, put `M=m-u` and `N=M+r`.  Because `N<2K`, at most one graph clone class
has weight at least `K`; it owns at most `r+1` points.  Every residual support
has at least

```text
B_K(M) = M-1                         if M<=K-1,
         (K-1)(M-K+1)                if M>=K
```

heterogeneous coordinate pairs, and each such pair belongs to at most one
parameter point.  The remaining one-variable optimization is convex on each
side of `M=K`, so only `M=D+1,K-1,K,K+D` need be checked.

The exact ray maximum is `796,620`, uniquely at `K=858,619`.

## Exact adjacent wall

At `K=858,618`, the locator floor is `806,341`, giving omission excess
`174,763` and

```text
6r = 1,048,578 = (R+1)+1.
```

The six-support minimum-distance synchronization fails by one coordinate.
This is a method wall, not an unsafe certificate.

## Scope

- large-locator proper-drop branch: paid;
- affine error rank 12: not yet paid;
- active-v4 ledger movement: `0`;
- KoalaBear closure: not claimed.

## Verification

- exact scan of all `189,958` ambient cells;
- exact four-endpoint ray optimization at every cell;
- independent exact reconstruction: PASS;
- bounded exhaustive endpoint controls: `5,400` in the independent audit;
- primary finite endpoint/cross-pair/large-clone controls: PASS;
- hostile mutations: `8/8` rejected;
- Wolfram selected-cell and convexity replay: PASS;
- no external theorem is load-bearing.

The next target is the adjacent `K=858,618` near-MDS obstruction: classify a
possible `W`-valued difference supported on `R+1` or `R+2` coordinates.
